
from pathlib import Path
import hashlib
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import expit, logit

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)
np.random.seed(7)
STAKE, RIDGE = 10.0, 20.0
FILES = ["lines_wk3_8.csv", "player_games_2026.csv"]
HASHES = {f: hashlib.sha256((ROOT / "data" / f).read_bytes()).hexdigest()
          for f in FILES}

def decimal(a):
    return np.where(a > 0, 1 + a / 100, 1 + 100 / np.abs(a))

def label(d):
    a, l = d.actual.to_numpy(), d.line.to_numpy()
    return np.where(d.side.eq("over"), a > l, a < l).astype(float)

def grade(d):
    d = d.copy()
    d["void"] = d.actual.isna()
    d["push"] = d.actual.notna() & d.actual.eq(d.line)
    d["graded"] = ~(d.void | d.push)
    d["y"] = label(d)
    d.loc[~d.graded, "y"] = np.nan
    d["stake"] = STAKE
    d["profit"] = np.where(d.graded, np.where(
        d.y.eq(1), STAKE * (d.dec - 1), -STAKE), 0.0)
    return d

raw = pd.read_csv(ROOT / "data" / FILES[0],
                  dtype={"game_id": str, "gsis": str})
logs = pd.read_csv(ROOT / "data" / FILES[1],
                   dtype={"game_id": str, "gsis": str})
for c in ["week", "line", "price", "actual"]:
    raw[c] = pd.to_numeric(raw[c], errors="coerce")
raw["snap"] = pd.to_datetime(raw.snap, utc=True, errors="coerce")
raw["kickoff"] = pd.to_datetime(raw.kickoff, utc=True, errors="coerce")
logs["week"] = pd.to_numeric(logs.week, errors="raise")
for c in ["car", "rushyds", "tgt", "recyds", "rushrecyds",
          "team_dropbacks", "team_rushes"]:
    logs[c] = pd.to_numeric(logs[c], errors="coerce")
assert not logs.duplicated(["game_id", "gsis"]).any(), "Duplicate player logs"
valid = (raw.book.eq("fanduel") & raw.market.isin(
    ["rushyds", "recyds", "rushrecyds"]) & raw.side.isin(["over", "under"])
    & raw.week.between(3, 8) & raw.price.notna() & raw.price.ne(0)
    & np.isfinite(raw.price) & raw.line.notna())
fd = raw.loc[valid].copy()
assert fd.snap.notna().all() and fd.kickoff.notna().all()
assert (fd.snap < fd.kickoff).all(), "Non-prekick quote"
fd["dec"] = decimal(fd.price.to_numpy())
assert (fd.dec > 1).all()
key = ["game_id", "player", "market", "line"]
fd = fd.sort_values(key + ["side", "snap", "dec"], kind="mergesort")
fd = fd.drop_duplicates(key + ["side"], keep="last")
fd["rid"] = np.arange(len(fd))
prices = fd.pivot(index=key, columns="side", values="dec").reset_index()
for c in ["over", "under"]:
    if c not in prices:
        prices[c] = np.nan
prices = prices.dropna(subset=["over", "under"])
prices["q_over"] = (1 / prices.over) / (1 / prices.over + 1 / prices.under)
m = fd.merge(prices[key + ["q_over"]], on=key, how="inner")
m = m[m.gsis.notna()].copy().reset_index(drop=True)
m["q"] = np.where(m.side.eq("over"), m.q_over, 1 - m.q_over)
m = grade(m)
m["y_over"] = np.where(m.graded, m.actual.gt(m.line).astype(float), np.nan)
# A contract's two sides must agree on outcome, including unresolved status.
for _, g in m.groupby(key, sort=False):
    assert g.actual.nunique(dropna=False) == 1, "Inconsistent paired outcomes"

def features(row):
    # No outcome, supplied prior_*, or future log columns are read here.
    h = logs[(logs.gsis == row.gsis) & (logs.week < row.week)]
    assert h.empty or (h.week < row.week).all(), "Future feature log"
    h = h.sort_values(["week", "game_id"], kind="mergesort")
    if h.empty:
        return [0.0, 0.0, 0.0, 0.0]
    y = h[row.market].dropna()
    scale = max(abs(float(row.line)), 10.0)
    level = (y.tail(4).mean() - row.line) / scale if len(y) else 0.0
    trend = (y.tail(2).mean() - y.mean()) / scale if len(y) else 0.0
    last = h.tail(4)
    rush = last.car / last.team_rushes.replace(0, np.nan)
    target = last.tgt / last.team_dropbacks.replace(0, np.nan)
    share = rush if row.market == "rushyds" else target
    if row.market == "rushrecyds":
        share = rush + target
    return [level, trend, share.mean(), min(len(h), 8) / 8]

X = np.asarray([features(r) for r in m.itertuples()], dtype=float)
X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0).reshape(-1, 4)
m["p"] = np.nan
m["train_n"] = 0
for w in range(5, 9):
    tr = m.week.lt(w) & m.side.eq("over") & m.graded
    te = m.week.eq(w)
    assert (m.loc[tr, "week"] < w).all(), "Future training label"
    n = int(tr.sum())
    po = m.loc[te, "q_over"].to_numpy()
    if n >= 30 and te.any():
        a, b = X[tr], X[te]
        mu, sd = a.mean(axis=0), a.std(axis=0)
        sd[sd < 1e-6] = 1.0
        A = np.c_[np.ones(n), np.clip((a - mu) / sd, -5, 5)]
        B = np.c_[np.ones(len(b)), np.clip((b - mu) / sd, -5, 5)]
        off = logit(np.clip(m.loc[tr, "q_over"].to_numpy(), 1e-6, 1-1e-6))
        y = m.loc[tr, "y_over"].to_numpy()
        def objective(beta):
            z = off + A @ beta
            loss = np.logaddexp(0, z).sum() - y @ z
            return (loss + RIDGE * (beta @ beta) / 2,
                    A.T @ (expit(z) - y) + RIDGE * beta)
        fit = minimize(objective, np.zeros(5), jac=True, method="L-BFGS-B",
                       options={"maxiter": 1000, "ftol": 1e-12})
        assert fit.success, fit.message
        po = expit(logit(np.clip(po, 1e-6, 1-1e-6)) + B @ fit.x)
    m.loc[te, "p"] = np.where(m.loc[te, "side"].eq("over"), po, 1-po)
    m.loc[te, "train_n"] = n

test = m[m.week.between(5, 8)].copy()
test["edge"] = test.p - test.q
test["ev"] = test.p * test.dec - 1
chosen = test[(test.edge >= .03) & (test.ev >= .02)].copy()
chosen = chosen.sort_values(
    ["week", "edge", "ev", "game_id", "player", "market", "side", "line"],
    ascending=[True, False, False, True, True, True, True, True],
    kind="mergesort")
chosen = chosen.drop_duplicates(["week", "game_id", "player"])
test["selected"] = test.rid.isin(chosen.rid)
baseline = grade(fd[fd.week.between(5, 8) & fd.market.eq("rushyds")
                    & fd.side.eq("under")].copy())
eligible = test[test.market.eq("rushyds") & test.side.eq("under")]
test.to_csv(OUT / "legs.csv", index=False)

slips = []
for w in range(5, 9):
    pool = chosen[chosen.week.eq(w)].reset_index(drop=True)
    seen = set()
    for shift in range(len(pool)):
        if len(seen) >= 5:
            break
        legs, games, players = [], set(), set()
        for j in list(range(shift, len(pool))) + list(range(shift)):
            r = pool.iloc[j]
            if r.game_id in games or r.player in players:
                continue
            legs.append(r); games.add(r.game_id); players.add(r.player)
            if len(legs) == 4:
                break
        if len(legs) < 3:
            continue
        ident = tuple(sorted(int(r.rid) for r in legs))
        if ident in seen:
            continue
        seen.add(ident)
        active = [r for r in legs if r.graded]
        lost = any(r.y == 0 for r in active)
        fd_mult = float(np.prod([r.dec for r in active]))
        fd_return = 0.0 if lost else STAKE * fd_mult
        pp_void = len(active) != len(legs)
        pp_return = STAKE if pp_void else (
            0.0 if lost else STAKE * {3: 6, 4: 10}[len(legs)])
        slips.append(dict(week=w, slip=len(seen), n=len(legs),
            leg_ids="|".join(map(str, ident)), active=len(active),
            stake=STAKE, fd_odds_full=float(np.prod([r.dec for r in legs])),
            fd_profit=fd_return-STAKE, pp_profit=pp_return-STAKE,
            pp_refund=pp_void, fd_all_refund=len(active) == 0))
slipcols = ["week", "slip", "n", "leg_ids", "active", "stake", "fd_odds_full",
            "fd_profit", "pp_profit", "pp_refund", "fd_all_refund"]
s = pd.DataFrame(slips, columns=slipcols)
s.to_csv(OUT / "slips.csv", index=False)

def stats(d):
    g = d[d.graded]
    result = dict(bets=len(d), graded=len(g), wins=int(g.y.sum()),
        pushes=int(d.push.sum()), voids=int(d.void.sum()),
        hit=g.y.mean(), profit=d.profit.sum(),
        roi=d.profit.sum() / (STAKE * len(d)) if len(d) else np.nan)
    for name in ["p", "q"]:
        z = g[g[name].notna()] if name in g else g.iloc[:0]
        if len(z):
            p = np.clip(z[name].to_numpy(), 1e-9, 1-1e-9)
            y = z.y.to_numpy()
            result[name+"_brier"] = np.mean((p-y)**2)
            result[name+"_logloss"] = -np.mean(y*np.log(p)+(1-y)*np.log(1-p))
        else:
            result[name+"_brier"] = result[name+"_logloss"] = np.nan
    return result

def grouped(d, col):
    return pd.DataFrame([dict(group=k, **stats(g))
                         for k, g in d.groupby(col)], columns=["group"] +
                        list(stats(d).keys()))

def table(df):
    # Markdown without requiring the optional tabulate package.
    df = df.copy()
    if df.empty:
        return "_No rows._"
    for c in df:
        df[c] = df[c].map(lambda v: f"{v:.4f}" if isinstance(
            v, (float, np.floating)) else str(v))
    return ("| " + " | ".join(map(str, df.columns)) + " |\n| " +
            " | ".join(["---"]*len(df.columns)) + " |\n" +
            "\n".join("| " + " | ".join(row) + " |"
                      for row in df.astype(str).to_numpy()))

universe = test[test.side.eq("over")]
comparison = pd.DataFrame([
    dict(strategy=name, **stats(d)) for name, d in [
        ("Selected singles", chosen), ("Eligible rush unders", eligible),
        ("All priced FD rush unders", baseline),
        ("Paired universe: over scoring", universe)]])
a, b, c, u = [stats(d) for d in [chosen, eligible, baseline, universe]]
success = (a["bets"] > 0 and b["bets"] > 0 and c["bets"] > 0
    and a["roi"] > 0 and a["roi"] > b["roi"] and a["roi"] > c["roi"]
    and u["p_brier"] < u["q_brier"])
weekly_slips = []
for w in range(5, 9):
    z = s[s.week.eq(w)]
    ids = [i for text in z.leg_ids for i in text.split("|")]
    weekly_slips.append(dict(week=w, slips=len(z), unique_legs=len(set(ids)),
        reused_slots=len(ids)-len(set(ids)), stake=STAKE*len(z),
        fd_profit=z.fd_profit.sum(), pp_profit=z.pp_profit.sum(),
        fd_roi=z.fd_profit.sum()/(STAKE*len(z)) if len(z) else np.nan,
        pp_roi=z.pp_profit.sum()/(STAKE*len(z)) if len(z) else np.nan))
report = [
    "# v7 locked development backtest",
    "**Predeclared result: " + ("PASS" if success else "FAIL") + "**",
    "Weeks 5–8 only. $10 flat stakes; ROI includes refunded stakes. "
    "Brier/log-loss exclude voids and pushes; universe scores only overs. "
    "Paired contracts have both FanDuel sides at the identical line. "
    "No CLV is available. This is not an independent confirmatory sample.",
    "Fixed model: market-logit offset; ridge 20; minimum 30 training overs; "
    "prior-log features; train-only scaling/clipping; edge >= .03, EV >= .02.",
    "## Baseline comparison and probability scores", table(comparison)]
for scope, d in [("Selected", chosen), ("All eligible quotes", test)]:
    for col in ["week", "market", "side"]:
        report += [f"## {scope}: by {col}", table(grouped(d, col))]
report += ["## Slips by week", table(pd.DataFrame(weekly_slips)),
    "FanDuel uses product odds after removing void/push legs. PP is a "
    "hypothetical same-line Power assumption: 3 picks 6x, 4 picks 10x; "
    "any void/push refunds the entire PP slip. Slips overlap and are not "
    "independent. Singles and slip bankrolls are separate.",
    "Historical rush-under +2.8% is not directly comparable to this FD-only "
    "Weeks 5–8 test. Small, dependent development samples cannot prove edge.",
    "## Input SHA-256", "\n".join(f"- `{k}`: `{v}`" for k, v in HASHES.items())]
(OUT / "results.md").write_text("\n\n".join(report) + "\n", encoding="utf-8")
print(f"Wrote {OUT}; predeclared result: {'PASS' if success else 'FAIL'}")
