"""NFL-75 Phase 4: selective-edge classifier (Rico's Nov 13 12:25 AM spec, "Selective Edge and Alternate-Line Repair").

Labels every candidate player-prop leg as one of
    STRONG UNDER | ALT-LINE CANDIDATE | STANDARD-LINE CANDIDATE | INSUFFICIENT EVIDENCE | NO EDGE
with a machine-readable `reason` and an `edge_tier` flag.

Rico's rules, encoded as gates (checked in this order):
  1. Passing-yards markets (any market starting with "pass") are excluded -> NO EDGE (excluded_market_passing).
  2. RB/FB rushing legs: the back needs >=60% of team carries in at least 3 of his last 4 prior games
     (same gate as backtests/selective_under_alt_2026-11-12, the gate behind the 18-5 OOS result).
     Fewer than 3 prior games -> INSUFFICIENT EVIDENCE; gate fails -> NO EDGE (do_not_play_rb_carry_lt_60).
  3. Receiving legs (recyds, rec, rushrec) need a verified main defender, else INSUFFICIENT EVIDENCE.
  4. Real prices only. A missing price (or missing price_source) is INSUFFICIENT EVIDENCE; nothing is ever filled in.
  5. A missing model probability is INSUFFICIENT EVIDENCE.
  6. Edge = p_model - no-vig (two-sided main line) or p_model - 1/decimal (one-sided alt). The +1 / +3 point tiers
     are FLAGS (`edge_tier`), never cuts. A negative edge (model favours the other side) is NO EDGE.
  7. Main-line Under in a market the W4-7 fit marked strong -> STRONG UNDER; any other main-line leg ->
     STANDARD-LINE CANDIDATE.
  8. Alt Over rungs are alt-floor legs only when the rung is at or below the player's usual output (median of his last
     4 prior games, needs >=3) AND the cushion (usual - rung) / usual is >= the fitted minimum -> ALT-LINE CANDIDATE.

`fit` refuses any row outside Weeks 4-7; `evaluate` refuses anything but Weeks 8-9. Weeks 10-12 are holdout and are
graded only by calibration/selective_edge_live.py after the freeze manifest check. `graduation` is report-only and
never changes projection_ready. Research only, not validated."""
from __future__ import annotations

import numpy as np
import pandas as pd

STRONG_UNDER = "STRONG UNDER"
ALT_LINE = "ALT-LINE CANDIDATE"
STANDARD = "STANDARD-LINE CANDIDATE"
INSUFFICIENT = "INSUFFICIENT EVIDENCE"
NO_EDGE = "NO EDGE"
LABELS = (STRONG_UNDER, ALT_LINE, STANDARD, INSUFFICIENT, NO_EDGE)
CANDIDATE_LABELS = (STRONG_UNDER, ALT_LINE, STANDARD)
SPOT_READY = "spot-ready, research"
NOT_YET = "not yet"

TRAIN_WEEKS = (4, 5, 6, 7)
EVAL_WEEKS = (8, 9)
HOLDOUT_WEEKS = (10, 11, 12)
RUSH_MARKETS = ("rushyds", "rushrec")          # RB carry gate applies
RECEIVING_MARKETS = ("recyds", "rec", "rushrec")  # defender gate applies
PROP_MARKETS = ("rushyds", "recyds", "rec", "rushrec")
RB_POSITIONS = ("RB", "FB")
CARRY_SHARE_MIN = 0.60
CARRY_LAST_N, CARRY_NEED = 4, 3
USUAL_LAST_N, USUAL_NEED = 4, 3
STRONG_MIN_N, STRONG_MIN_MARGIN = 30, 0.03
CUSHION_GRID = (0.10, 0.20, 0.30, 0.40, 0.50)
GRAD_MIN_N, GRAD_MIN_MARGIN = 30, 0.03
BOOT_B, BOOT_SEED = 10000, 0


class HoldoutError(RuntimeError):
    pass


def american_to_decimal(a):
    a = np.asarray(a, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(a > 0, 1 + a / 100, 1 + 100 / -a)


def _tier(e: float) -> str:
    if not np.isfinite(e):
        return ""
    return "+3" if e >= 0.03 - 1e-12 else ("+1" if e >= 0.01 - 1e-12 else "")


# ---------------------------------------------------------------- point-in-time context from nflverse PBP
def _reg(pbp: pd.DataFrame) -> pd.DataFrame:
    if "season_type" in pbp:
        pbp = pbp[pbp.season_type.fillna("REG") == "REG"]
    if "two_point_attempt" in pbp:
        pbp = pbp[pbp.two_point_attempt.fillna(0) != 1]
    return pbp


def player_game_table(pbp: pd.DataFrame) -> pd.DataFrame:
    """One row per (week, game, team, player): carries, team carries, carry share, rushyds, recyds, rec."""
    cols = ["week", "game_id", "posteam", "gsis", "car", "team_car", "share", "rushyds", "recyds", "rec"]
    if pbp is None or len(pbp) == 0:
        return pd.DataFrame(columns=cols)
    p = _reg(pbp)
    ru = p[(p.rush_attempt == 1) & (p.qb_kneel.fillna(0) != 1)]
    tc = ru.groupby(["game_id", "posteam"]).size().rename("team_car")
    r = (ru.groupby(["week", "game_id", "posteam", "rusher_player_id"])
         .agg(car=("rush_attempt", "size"), rushyds=("rushing_yards", "sum")).reset_index()
         .rename(columns={"rusher_player_id": "gsis"}))
    pa = p[(p.pass_attempt == 1) & p.receiver_player_id.notna()]
    rc = (pa.groupby(["week", "game_id", "posteam", "receiver_player_id"])
          .agg(recyds=("receiving_yards", lambda s: s.fillna(0).sum()), rec=("complete_pass", "sum")).reset_index()
          .rename(columns={"receiver_player_id": "gsis"}))
    t = r.merge(rc, how="outer", on=["week", "game_id", "posteam", "gsis"])
    t = t.merge(tc.reset_index(), on=["game_id", "posteam"], how="left")
    for c in ("car", "rushyds", "recyds", "rec"):
        t[c] = t[c].fillna(0.0)
    t["share"] = t.car / t.team_car
    return t[cols]


def attach_context(legs: pd.DataFrame, pbp: pd.DataFrame) -> pd.DataFrame:
    """Adds carry_n_prior, carry_n60, carry_share and usual using ONLY games in weeks < leg week (point in time)."""
    t = player_game_table(pbp)
    out = []
    for g, w, m in zip(legs.gsis, legs.week, legs.market):
        h = t[(t.gsis == g) & (t.week < w)].sort_values("week")
        hc = h.tail(CARRY_LAST_N)
        n_prior = len(hc)
        n60 = int((hc.share >= CARRY_SHARE_MIN - 1e-12).sum())
        share = float(hc.share.mean()) if n_prior else np.nan
        hu = h.tail(USUAL_LAST_N)
        if m == "rushrec":
            vals = hu.rushyds + hu.recyds
        elif m in ("rushyds", "recyds", "rec"):
            vals = hu[m]
        else:
            vals = pd.Series(dtype=float)
        usual = float(np.median(vals)) if len(vals) >= USUAL_NEED else np.nan
        out.append((n_prior if n_prior else np.nan, n60 if n_prior else np.nan, share, usual))
    legs = legs.copy()
    legs["carry_n_prior"], legs["carry_n60"], legs["carry_share"], legs["usual"] = (
        list(x) for x in zip(*out)) if out else ([], [], [], [])
    return legs


# ---------------------------------------------------------------- classifier
def _classify_row(r, strong, cushion_min):
    m, kind, side = str(r.market), str(r.kind), str(r.side)
    dec = r.dec
    if m.startswith("pass"):
        return NO_EDGE, "excluded_market_passing", np.nan, np.nan
    if m not in PROP_MARKETS:
        return INSUFFICIENT, "unsupported_market", np.nan, np.nan
    if m in RUSH_MARKETS and str(r.position) in RB_POSITIONS:
        n_prior = r.carry_n_prior
        if not (pd.notna(n_prior) and n_prior >= CARRY_NEED):
            return INSUFFICIENT, "carry_history_unknown", np.nan, np.nan
        if not (pd.notna(r.carry_n60) and r.carry_n60 >= CARRY_NEED):
            return NO_EDGE, "do_not_play_rb_carry_lt_60", np.nan, np.nan
    if m in RECEIVING_MARKETS and not (r.defender_verified is True or r.defender_verified == 1):
        return INSUFFICIENT, "main_defender_unverified", np.nan, np.nan
    real = pd.notna(dec) and dec > 1 and pd.notna(r.price_source) and str(r.price_source).strip() != ""
    if not real:
        return INSUFFICIENT, ("alt_price_missing" if kind == "alt" else "price_missing"), np.nan, np.nan
    if pd.isna(r.p_model):
        return INSUFFICIENT, "model_prob_missing", np.nan, np.nan
    be = 1.0 / dec
    if kind == "main":
        edge = (r.p_model - r.p_nv) if pd.notna(r.p_nv) else (r.p_model - be)
        if edge < 0:
            return NO_EDGE, "model_disagrees", edge, np.nan
        if side == "Under" and m in strong:
            return STRONG_UNDER, "gated_under_strong_market", edge, np.nan
        return STANDARD, "main_line_positive_edge", edge, np.nan
    if kind != "alt":
        return INSUFFICIENT, "unsupported_kind", np.nan, np.nan
    if side != "Over":
        return INSUFFICIENT, "under_alt_untested", np.nan, np.nan
    edge = r.p_model - be
    usual = r.usual
    if pd.isna(usual) or usual <= 0:
        return INSUFFICIENT, "usual_output_unknown", edge, np.nan
    cushion = (usual - r.line) / usual
    if r.line > usual:
        return NO_EDGE, "alt_above_usual_output", edge, cushion
    if cushion_min is None:
        return NO_EDGE, "alt_floor_not_shown_in_train", edge, cushion
    if cushion < cushion_min - 1e-12:
        return NO_EDGE, "cushion_below_min", edge, cushion
    if edge < 0:
        return NO_EDGE, "model_disagrees", edge, cushion
    return ALT_LINE, "alt_floor_cushion_ok", edge, cushion


def classify(legs: pd.DataFrame, params: dict) -> pd.DataFrame:
    df = legs.copy()
    for c, v in (("p_nv", np.nan), ("defender_verified", False), ("carry_n_prior", np.nan), ("carry_n60", np.nan),
                 ("usual", np.nan), ("price_source", None), ("p_model", np.nan), ("dec", np.nan)):
        if c not in df:
            df[c] = v
    strong = set(params.get("strong_markets") or [])
    cm = params.get("alt_min_cushion")
    res = [_classify_row(r, strong, cm) for r in df.itertuples(index=False)]
    df["label"] = [x[0] for x in res]
    df["reason"] = [x[1] for x in res]
    df["edge"] = [x[2] for x in res]
    df["cushion"] = [x[3] for x in res]
    df["edge_tier"] = [_tier(e) for e in df.edge]
    df["be"] = np.where(df.dec > 1, 1.0 / df.dec, np.nan)
    df["projection_ready"] = False
    return df


# ---------------------------------------------------------------- settlement / summary
def settle(df: pd.DataFrame) -> pd.DataFrame:
    """win (1/0, NaN on push or unknown) and push (0/1). Uses `actual` when present, else existing win/push."""
    df = df.copy()
    if "actual" in df and df.actual.notna().any():
        a, ln = df.actual.astype(float), df.line.astype(float)
        under = df.side.astype(str).eq("Under")
        push = (a == ln) & a.notna()
        win = np.where(under, a < ln, a > ln).astype(float)
        win = np.where(push | a.isna(), np.nan, win)
        if "win" in df:  # keep pre-settled rows (backtest candidates) where actual is unknown
            win = np.where(a.isna(), df.win, win)
            push = np.where(a.isna(), df.get("push", 0), push)
        df["win"], df["push"] = win, np.asarray(push).astype(int)
    else:
        df["push"] = df.get("push", 0)
        df["push"] = pd.Series(df["push"]).fillna(0).astype(int).values
    return df


def summarize(df: pd.DataFrame, B: int = BOOT_B, seed: int = BOOT_SEED) -> dict:
    """Hit rate vs mean break-even of the real graded price; margin CI by game-cluster bootstrap."""
    d = df[df.win.notna() | (df.push == 1)]
    n = int(len(d))
    if n == 0:
        return dict(n=0, W=0, L=0, P=0, hit=np.nan, be=np.nan, margin=np.nan, margin_lo=np.nan, margin_hi=np.nan,
                    roi=np.nan)
    nonpush = (d.push != 1).values
    w = int(((d.win == 1).values & nonpush).sum())
    l_ = int(((d.win == 0).values & nonpush).sum())
    be = 1.0 / d.dec.values
    hit = w / max(w + l_, 1)
    beb = float(be[nonpush].mean()) if nonpush.any() else np.nan
    prof = np.where(~nonpush, 0.0, np.where(d.win.values == 1, d.dec.values - 1, -1.0))
    out = dict(n=n, W=w, L=l_, P=n - w - l_, hit=hit, be=beb, margin=hit - beb, roi=float(prof.mean()))
    g = pd.DataFrame(dict(game_id=d.game_id.values, np_=nonpush.astype(int), w=((d.win.values == 1) & nonpush)
                          .astype(int), beN=be * nonpush))
    S = g.groupby("game_id")[["np_", "w", "beN"]].sum().values
    rng = np.random.default_rng(seed)
    k = len(S)
    idx = rng.integers(0, k, (B, k))
    s = S[idx].sum(axis=1)
    ok = s[:, 0] > 0
    m = s[ok, 1] / s[ok, 0] - s[ok, 2] / s[ok, 0]
    out["margin_lo"] = float(np.percentile(m, 2.5)) if len(m) else np.nan
    out["margin_hi"] = float(np.percentile(m, 97.5)) if len(m) else np.nan
    return out


def table(df: pd.DataFrame, by=("label", "market", "side"), **kw) -> pd.DataFrame:
    rows = []
    for k, g in df.groupby(list(by), dropna=False):
        k = k if isinstance(k, tuple) else (k,)
        rows.append(dict(zip(by, k), **summarize(g, **kw)))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- fit / evaluate (holdout-refusing)
def _weeks_guard(df: pd.DataFrame, allowed, what: str):
    wk = set(int(w) for w in pd.Series(df.week).dropna().unique())
    hold = sorted(wk & set(HOLDOUT_WEEKS)) or sorted(w for w in wk if w >= 10)
    if hold:
        raise HoldoutError(f"{what} refuses holdout weeks {hold}: Weeks 10-12 are graded only by the frozen live grader")
    bad = sorted(wk - set(allowed))
    if bad:
        raise HoldoutError(f"{what} accepts only weeks {list(allowed)}; got {bad}")


def fit(legs: pd.DataFrame, B: int = 2000) -> dict:
    """Fit on Weeks 4-7 only: (a) which markets are STRONG UNDER markets (n>=30 and margin >= +3 pts over the real
    price's break-even, gated legs with non-negative model edge); (b) the minimum alt-floor cushion (smallest grid value
    with n>=30 and margin >= +3 pts); None if no cushion qualifies. Edge tiers are not fit; they stay flags."""
    _weeks_guard(legs, TRAIN_WEEKS, "fit")
    every = {"strong_markets": list(PROP_MARKETS), "alt_min_cushion": 0.0}
    c = settle(classify(legs, every))
    strong, strong_rows = [], []
    su = c[(c.label == STRONG_UNDER)]
    for m, g in su.groupby("market"):
        s = summarize(g, B=B)
        strong_rows.append(dict(market=m, **s))
        if s["n"] >= STRONG_MIN_N and s["margin"] >= STRONG_MIN_MARGIN - 1e-12:
            strong.append(m)
    cush, cush_rows = None, []
    al = c[c.label == ALT_LINE]
    for cm in CUSHION_GRID:
        g = al[al.cushion >= cm - 1e-12]
        s = summarize(g, B=B) if len(g) else dict(n=0)
        cush_rows.append(dict(cushion=cm, **s))
        if cush is None and s["n"] >= STRONG_MIN_N and s["margin"] >= STRONG_MIN_MARGIN - 1e-12:
            cush = cm
    clean = lambda rows: [{k: (None if isinstance(v, float) and not np.isfinite(v) else v) for k, v in r.items()}
                          for r in rows]
    return {"schema": "nfl75-selective-edge-params/1", "train_weeks": list(TRAIN_WEEKS),
            "strong_markets": sorted(strong), "alt_min_cushion": cush,
            "rules": {"carry_share_min": CARRY_SHARE_MIN, "carry_last_n": CARRY_LAST_N, "carry_need": CARRY_NEED,
                      "usual_last_n": USUAL_LAST_N, "usual_need": USUAL_NEED, "strong_min_n": STRONG_MIN_N,
                      "strong_min_margin": STRONG_MIN_MARGIN, "cushion_grid": list(CUSHION_GRID),
                      "edge_tiers": "flags only (+1 >= 0.01, +3 >= 0.03); not cuts",
                      "excluded_markets": "pass*", "receiving_needs_verified_defender": True},
            "train_strong_under_by_market": clean(strong_rows), "train_alt_floor_by_cushion": clean(cush_rows),
            "n_train_legs": int(len(legs)), "projection_ready": False}


def evaluate(legs: pd.DataFrame, params: dict) -> pd.DataFrame:
    """Score the frozen params on Weeks 8-9 only."""
    _weeks_guard(legs, EVAL_WEEKS, "evaluate")
    return settle(classify(legs, params))


# ---------------------------------------------------------------- graduation (report-only)
def graduation(graded: pd.DataFrame, sources=("live",), min_n: int = GRAD_MIN_N, min_margin: float = GRAD_MIN_MARGIN,
               B: int = BOOT_B, seed: int = BOOT_SEED) -> pd.DataFrame:
    """Per (label, market, side): 'spot-ready, research' when n >= 30 settled legs at real prices from `sources`,
    margin >= +3 pts over break-even and the 95% game-cluster bootstrap CI lower bound > 0. Report only:
    projection_ready is always False and nothing here writes it."""
    g = graded[graded.label.isin(CANDIDATE_LABELS)]
    if "source" in g:
        g = g[g.source.isin(sources)]
    real = (g.dec > 1) & g.dec.notna()
    if "price_source" in g:
        real &= g.price_source.notna() & (g.price_source.astype(str).str.strip() != "")
    rows = []
    for k, grp in g.groupby(["label", "market", "side"]):
        r = real.loc[grp.index]
        s = summarize(grp[r], B=B, seed=seed)
        ok = (s["n"] >= min_n and np.isfinite(s["margin"]) and s["margin"] >= min_margin - 1e-12
              and np.isfinite(s["margin_lo"]) and s["margin_lo"] > 0)
        why = [] if ok else [x for x, bad in (("n<%d" % min_n, s["n"] < min_n),
                                             ("margin<+%d pts" % round(min_margin * 100),
                                              not (np.isfinite(s["margin"]) and s["margin"] >= min_margin - 1e-12)),
                                             ("CI lower bound <= 0",
                                              not (np.isfinite(s.get("margin_lo", np.nan)) and s["margin_lo"] > 0)))
                                 if bad]
        rows.append(dict(label=k[0], market=k[1], side=k[2], sources="+".join(sources), **s,
                         excluded_no_real_price=int((~r).sum()), status=SPOT_READY if ok else NOT_YET,
                         why_not="; ".join(why), projection_ready=False))
    return pd.DataFrame(rows)
