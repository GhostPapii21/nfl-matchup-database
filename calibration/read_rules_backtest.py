"""Backtest Rico's three Week 13 read rules (flags only) against the NFL-75 rushing-under baseline. 0 credits.

    SELECTIVE_EDGE_WORK=/tmp/read_rules_bt_work python3 -m calibration.selective_edge_run build   # box-local legs
    SELECTIVE_EDGE_WORK=/tmp/read_rules_bt_work python3 -m calibration.read_rules_backtest

Data (all already on the box / in the repo; no network, no Odds API):
  * legs_w4_9.csv built by calibration.selective_edge_run (real saved prices: main unders = one book's two-sided
    price ~34 min pre-kick; alt overs = best real one-sided pre-kick alt price). Its sha256 is checked against the
    Phase 4 freeze manifest, so the baseline rows are the frozen ones.
  * data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet (pinned in the same manifest) for the
    walk-forward rule features (weeks < leg week only) and the kickoff weather fields.
Baseline = Phase 4 STRONG UNDER rushyds (frozen params_w4_7.json): W4-7 is the fit sample, W8-9 the OOS sample.
The rules were written after Thanksgiving and have no fitted parameters, so for them W4-9 are all out of sample,
but W8-9 had already been looked at by earlier studies.

Rule 3 limitation: no saved hourly NWS / Open-Meteo forecasts cover Weeks 4-9 on the box. The only weather here is
the nflverse kickoff observation (`weather` text, `wind`, `roof`): not hourly, not a forecast, no rain RATE, so the
hourly grade itself cannot be backtested. The proxy grades precipitation as reported / not reported.

Every cell reports n; n < 30 or a CI that crosses zero is written "insufficient sample". Research only; nothing here
changes a label, a weight or projection_ready.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from calibration import selective_edge as se
from calibration.selective_edge_freeze import RUN as PHASE4, load_params, sha256
from pipeline.read_rules import CUTS_ENABLED, assert_flags_only
from pipeline.read_rules import defense_allowed as DA
from pipeline.read_rules import targets_first as TF
from pipeline.read_rules.common import ROOT, load_positions

WORK = Path(os.environ.get("SELECTIVE_EDGE_WORK", "/tmp/read_rules_bt_work"))
PBP = ROOT / "data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet"
OUT = ROOT / "research/runs/2026-11-26_read_rules_flags"
OM_WK6_8 = Path(os.environ.get("READ_RULES_OM_WK6_8",
                               "/workspace/vet_scratch/repo/backtests/rulebook_replay_wk6_8/weather_wk6_8.json"))
MIN_N = 30
B = int(os.environ.get("READ_RULES_BOOT_B", se.BOOT_B))
PRECIP_WORDS = ("rain", "shower", "drizzle", "snow", "sleet", "storm", "thunder", "precip")


def verdict(s: dict) -> str:
    if s["n"] < MIN_N:
        return "insufficient sample (n<30)"
    if not (np.isfinite(s["margin_lo"]) and s["margin_lo"] > 0):
        return "insufficient sample (CI includes 0)" if s["margin"] > 0 else "no edge shown"
    return "margin CI > 0"


def summ(df: pd.DataFrame, **tags) -> dict:
    s = se.summarize(df, B=B)
    return dict(tags, n=s["n"], W=s["W"], L=s["L"], P=s["P"], hit=s["hit"], be=s["be"], margin=s["margin"],
                margin_lo=s["margin_lo"], margin_hi=s["margin_hi"], roi=s["roi"], roi_lo=s["roi_lo"],
                roi_hi=s["roi_hi"], verdict=verdict(s))


def diff_ci(base: pd.DataFrame, keep: pd.Series, B: int = B, seed: int = 0) -> dict:
    """Game-cluster bootstrap of (margin of the kept subset) - (margin of the whole baseline). Paired resamples."""
    d = base[base.win.notna()].copy()
    k = keep.reindex(d.index).fillna(False).astype(bool).values
    if k.sum() == 0 or len(d) == 0:
        return dict(diff=np.nan, diff_lo=np.nan, diff_hi=np.nan)
    be = 1 / d.dec.values
    w = (d.win.values == 1).astype(float)
    g = pd.DataFrame(dict(game=d.game_id.values, w=w, be=be, n=1.0, kw=w * k, kbe=be * k, kn=k.astype(float)))
    S = g.groupby("game")[["w", "be", "n", "kw", "kbe", "kn"]].sum().values
    full = lambda s: (s[..., 0] - s[..., 1]) / s[..., 2]   # noqa: E731
    sub = lambda s: (s[..., 3] - s[..., 4]) / np.where(s[..., 5] > 0, s[..., 5], np.nan)  # noqa: E731
    point = float(sub(S.sum(0)) - full(S.sum(0)))
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(S), (B, len(S)))
    T = S[idx].sum(1)
    dd = sub(T) - full(T)
    dd = dd[np.isfinite(dd)]
    return dict(diff=point, diff_lo=float(np.percentile(dd, 2.5)), diff_hi=float(np.percentile(dd, 97.5)))


def kickoff_weather(pbp: pd.DataFrame) -> pd.DataFrame:
    g = pbp.groupby("game_id").agg(roof=("roof", "first"), wind=("wind", "first"), weather=("weather", "first")).reset_index()
    txt = g.weather.fillna("").str.lower()
    wind_txt = txt.str.extract(r"wind:\s*\w*\s*(\d+)\s*mph")[0].astype(float)
    g["wind_mph"] = g.wind.where(g.wind.notna(), wind_txt)
    indoor = g.roof.fillna("").isin(["dome", "closed"])
    precip = txt.apply(lambda t: any(w in t for w in PRECIP_WORDS))
    g["wx_precip"] = np.where(indoor, "indoor", np.where(g.weather.isna(), "unknown", np.where(precip, "precip_reported", "none_reported")))
    g["wx_wind15"] = np.where(indoor, "indoor", np.where(g.wind_mph.isna(), "unknown", np.where(g.wind_mph >= 15, "wind>=15", "wind<15")))
    g["wx_bad"] = np.where(indoor, "indoor", np.where((g.wx_precip == "precip_reported") | (g.wx_wind15 == "wind>=15"), "bad",
                                                      np.where((g.wx_precip == "unknown") & (g.wx_wind15 == "unknown"), "unknown", "not_bad")))
    return g[["game_id", "roof", "wind_mph", "wx_precip", "wx_wind15", "wx_bad"]]


def open_meteo_wk6_8(path: Path = OM_WK6_8) -> pd.DataFrame:
    """Box-local saved Open-Meteo HISTORICAL-FORECAST pulls for W6-8 kickoff windows (max sustained wind, max gust,
    max precip probability over kickoff..+3.5h). The rain AMOUNT was fetched but not saved, so no rain-rate grade."""
    cols = ["game_id", "om_wind", "om_gust", "om_precip_pct", "om_grade"]
    if not path.exists():
        return pd.DataFrame(columns=cols)
    rows = []
    for v in json.loads(path.read_text()).values():
        k = v.get("kickoff", {})
        indoor = str(v.get("roof", "")).lower() in ("dome", "closed")
        if indoor:
            gr = "indoor"
        elif k.get("status") != "OK" or k.get("wind_mph") is None:
            gr = "unknown"
        else:
            gr = "windy" if (k["wind_mph"] >= 15 or (k.get("gust_mph") or 0) >= 25) else "not_windy"
        rows.append(dict(game_id=v["game_id"], om_wind=k.get("wind_mph"), om_gust=k.get("gust_mph"),
                         om_precip_pct=k.get("precip_pct"), om_grade=gr))
    return pd.DataFrame(rows, columns=cols)


def add_features(L: pd.DataFrame, pbp: pd.DataFrame, positions: dict) -> pd.DataFrame:
    players, team_t = TF.target_table(pbp)
    roles = {w: DA.role_allowed(pbp, positions, w) for w in sorted(L.week.unique())}
    run = {w: DA.run_allowed(pbp, w) for w in sorted(L.week.unique())}
    keys = L[["week", "game_id", "gsis", "position", "market"]].drop_duplicates()
    feats = []
    for r in keys.itertuples(index=False):
        away, home = r.game_id.split("_")[2:4]
        h = players[(players.gsis == r.gsis) & (players.week < r.week)].sort_values("week")
        team = str(h.posteam.iloc[-1]) if len(h) else None
        opp = home if team == away else away if team == home else None
        pos = str(r.position).upper()
        t = TF.evaluate(r.gsis, r.week, pos, opp, players, team_t, roles[r.week]) if r.market in TF.RECEIVING_MARKETS else {"status": TF.NA}
        role = "WR" if pos == "WR" else DA.role_of(pos)
        soft_role = DA.soft_vs_role(roles[r.week], opp, role) if opp else "unknown"
        rr = run[r.week]
        rk = rr[rr.defteam == opp].ypc_rank if opp else pd.Series(dtype=float)
        soft_run = "unknown" if not len(rk) or pd.isna(rk.iloc[0]) else ("soft" if rk.iloc[0] <= DA.SOFT_RANK else "not_soft")
        feats.append(dict(week=r.week, game_id=r.game_id, gsis=r.gsis, market=r.market, rr_tf=t["status"],
                          rr_share=t.get("share"), rr_opp=opp or "unknown", rr_def_role=soft_role, rr_def_run=soft_run))
    F = pd.DataFrame(feats)
    out = L.merge(F, on=["week", "game_id", "gsis", "market"], how="left", validate="many_to_one")
    assert len(out) == len(L), "feature join must not add or drop legs"
    return out


def _f(x, pct=True):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "-"
    return f"{100 * x:+.1f}" if pct else f"{x:.3f}"


def render_report(R: pd.DataFrame, D: pd.DataFrame, meta: dict) -> str:
    L = ["# Read rules (flags only) vs the rushing-under baseline: backtest", "",
         "Research only. projection_ready=false. 0 Odds API credits. refs NFL-56.", "",
         f"Generated by `python3 -m calibration.read_rules_backtest`. legs sha256 `{meta['legs_sha256'][:12]}...` "
         f"(frozen `{str(meta['frozen_legs_sha256'])[:12]}...`), pbp `{meta['pbp']}`, game-cluster bootstrap "
         f"B={meta['bootstrap_B']} seed 0. Margin = hit rate - mean break-even of the real price (points). "
         "ROI per 1-unit stake at the real decimal price. Verdict: n<30 or CI incl. 0 = insufficient sample.", "",
         "## Per-rule cells (Weeks 4-9 combined; W4-7 and W8-9 splits are in results_by_rule.csv)", "",
         "| rule | view | group | n | W-L | hit | BE | margin [95% CI] | ROI | verdict |", "|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in R[R.weeks == "W4-9"].iterrows():
        L.append(f"| {r.rule} | {r.view} | {r.group} | {r.n} | {r.W}-{r.L} | {100 * r.hit:.1f}% | {100 * r.be:.1f}% | "
                 f"{_f(r.margin)} [{_f(r.margin_lo)}, {_f(r.margin_hi)}] | {_f(r.roi)}% | {r.verdict} |")
    L += ["", "## Rule used as a filter on the baseline (what a cut would do), paired game bootstrap", "",
          "| filter | weeks | n base | n kept | hit kept | margin kept | diff vs baseline [95% CI] | beats baseline |",
          "|---|---|---|---|---|---|---|---|"]
    for _, r in D.iterrows():
        if r.get("n_kept") == "n/a":
            L.append(f"| {r['filter']} | {r.weeks} | {r.n_base} | n/a | - | - | {r.note} | no |")
            continue
        L.append(f"| {r['filter']} | {r.weeks} | {r.n_base} | {r.n_kept} | {100 * r.hit_kept:.1f}% | {_f(r.margin_kept)} | "
                 f"{_f(r['diff'])} [{_f(r.diff_lo)}, {_f(r.diff_hi)}] | {'yes' if r.beats_baseline else 'no'} |")
    L += ["", "## Limits", "",
          "- Receiving legs: main lines in this data are unders only; overs exist only as alt rungs (many rungs per player, "
          "heavily correlated; the game-cluster bootstrap absorbs part of that).",
          "- Rule 1 cannot filter the baseline (the baseline is rushing legs).",
          "- Rule 2 here uses play-by-play only (by-role yards allowed, run YPC rank), walk-forward. Sharp coverage shares "
          "are season-to-date as of Nov 24 and would leak, so they are not backtested. Slot/outside alignment is unknown.",
          "- Rule 3: no saved hourly rain-RATE forecasts (NWS or Open-Meteo) cover Weeks 4-9; the first proxy is the nflverse kickoff observation "
          "(precip words in the weather text, wind >= 15 mph). No rain rate, not hourly, not a forecast: the hourly grade "
          "itself is untested. `2026_MNF_CHI_SEA` has no play-by-play game row, so its weather is unknown.",
          "- Rule 3 second proxy: box-local saved Open-Meteo historical-forecast kickoff-window pulls for Weeks 6-8 "
          "(42 games; max sustained wind, max gust, max precip probability). The rain amount was not saved, so this is "
          "wind/gust only; still not the hourly rain-rate grade.",
          "- Weeks 8-9 were already looked at by earlier studies; W4-7 is the baseline's fit sample.",
          "", "Conclusion rule: a rule may become a cut only when its filter beats the baseline with n>=30 and a paired "
          "diff CI lower bound > 0, and Rico approves. All three stay flags.", ""]
    return "\n".join(L)


def main() -> int:
    assert_flags_only()
    legs_path = WORK / "legs_w4_9.csv"
    man = json.loads((PHASE4 / "freeze_manifest.json").read_text())
    want = man.get("inputs_sha256", {}).get("legs_w4_9.csv (built)")
    got = sha256(legs_path)
    if want and got != want:
        raise SystemExit(f"legs_w4_9.csv sha256 {got} != frozen {want}; rebuild with selective_edge_run build")
    params = load_params()
    L = pd.read_csv(legs_path, low_memory=False)
    G = se.settle(se.classify(L, params))
    pbp = pd.read_parquet(PBP)
    pbp = pbp[pbp.season_type.fillna("REG") == "REG"]
    pos = load_positions()
    G = add_features(G, pbp, pos)
    G = G.merge(kickoff_weather(pbp), on="game_id", how="left")
    G = G.merge(open_meteo_wk6_8(), on="game_id", how="left")
    G["om_grade"] = np.where(G.week.between(6, 8), G.om_grade.fillna("unknown"), "not_covered (W6-8 only)")
    for c in ("wx_precip", "wx_wind15", "wx_bad"):   # e.g. 2026_MNF_CHI_SEA has no pbp game row -> unknown, never "dry"
        G[c] = G[c].fillna("unknown")
    G["wset"] = np.where(G.week <= 7, "W4-7", "W8-9")
    base = G[(G.label == se.STRONG_UNDER) & (G.market == "rushyds")]
    rows, diffs = [], []

    def cells(df, rule, view, by):
        for wset in ("W4-7", "W8-9", "W4-9"):
            d = df if wset == "W4-9" else df[df.wset == wset]
            if by is None:
                rows.append(summ(d, rule=rule, view=view, weeks=wset, group="all"))
                continue
            for k, g in d.groupby(by, dropna=False):
                rows.append(summ(g, rule=rule, view=view, weeks=wset, group=str(k)))

    cells(base, "baseline", "STRONG UNDER rushyds (frozen Phase 4)", None)
    cells(base, "baseline", "STRONG UNDER rushyds by position", "position")
    # Rule 1: receiving legs (all priced, any model edge) split by targets-first status
    rec_main = G[(G.kind == "main") & G.market.isin(TF.RECEIVING_MARKETS) & G.position.isin(["WR", "TE"]) & G.dec.gt(1)]
    rec_alt = G[(G.kind == "alt") & G.market.isin(TF.RECEIVING_MARKETS) & G.position.isin(["WR", "TE"]) & G.dec.gt(1)]
    cells(rec_main, "1 targets_first", "WR/TE receiving MAIN UNDERS, all priced", "rr_tf")
    cells(rec_main[rec_main.edge_study.fillna(-1) >= 0], "1 targets_first", "WR/TE receiving MAIN UNDERS, model edge >= 0", "rr_tf")
    cells(rec_alt, "1 targets_first", "WR/TE receiving ALT OVERS, all priced rungs", "rr_tf")
    # Rule 2: defense-allowed
    cells(base, "2 defense_allowed", "baseline split by opponent run-defense YPC rank (soft = top-10 allowed)", "rr_def_run")
    cells(rec_main, "2 defense_allowed", "WR/TE receiving MAIN UNDERS by opponent yards-allowed-to-role", "rr_def_role")
    cells(rec_alt, "2 defense_allowed", "WR/TE receiving ALT OVERS by opponent yards-allowed-to-role", "rr_def_role")
    # Rule 3: weather proxy
    cells(base, "3 weather (kickoff proxy)", "baseline by kickoff weather (precip reported or wind>=15 = bad)", "wx_bad")
    cells(base, "3 weather (kickoff proxy)", "baseline by kickoff precip text", "wx_precip")
    cells(rec_main, "3 weather (kickoff proxy)", "WR/TE receiving MAIN UNDERS by kickoff weather", "wx_bad")
    b68 = base[base.week.between(6, 8)]
    cells(b68, "3 weather (Open-Meteo W6-8)", "baseline W6-8 by saved Open-Meteo historical-forecast wind (sustained>=15 or gust>=25 = windy)", "om_grade")
    r68 = rec_main[rec_main.week.between(6, 8)]
    cells(r68, "3 weather (Open-Meteo W6-8)", "WR/TE receiving MAIN UNDERS W6-8 by Open-Meteo wind grade", "om_grade")

    # Rule-as-filter on top of the baseline (what "cut" would do), paired game bootstrap vs the full baseline
    filters = {
        "1 targets_first": None,  # does not apply to rushing legs
        "2 defense_allowed: drop legs vs soft run defense": base.rr_def_run != "soft",
        "2 defense_allowed: keep only legs vs not_soft run defense (unknown dropped)": base.rr_def_run == "not_soft",
        "3 weather proxy: keep only bad-weather games": base.wx_bad == "bad",
        "3 weather proxy: drop bad-weather games": base.wx_bad != "bad",
    }
    for name, keep in filters.items():
        for wset in ("W4-7", "W8-9", "W4-9"):
            b = base if wset == "W4-9" else base[base.wset == wset]
            if keep is None:
                diffs.append(dict(filter=name, weeks=wset, n_base=int(b.win.notna().sum()), n_kept="n/a",
                                  note="rule 1 applies only to receiving legs; it cannot filter rushing unders"))
                continue
            k = keep.reindex(b.index)
            s = summ(b[k.fillna(False)], weeks=wset)
            dci = diff_ci(b, k)
            diffs.append(dict(filter=name, weeks=wset, n_base=int(b.win.notna().sum()), n_kept=s["n"], hit_kept=s["hit"],
                              margin_kept=s["margin"], roi_kept=s["roi"], **dci,
                              beats_baseline=bool(np.isfinite(dci["diff_lo"]) and dci["diff_lo"] > 0 and s["n"] >= MIN_N)))
    for name, keep in (("3 Open-Meteo: keep only windy games", b68.om_grade == "windy"),
                       ("3 Open-Meteo: drop windy games", b68.om_grade != "windy")):
        s = summ(b68[keep], weeks="W6-8")
        dci = diff_ci(b68, keep)
        diffs.append(dict(filter=name, weeks="W6-8", n_base=int(b68.win.notna().sum()), n_kept=s["n"], hit_kept=s["hit"],
                          margin_kept=s["margin"], roi_kept=s["roi"], **dci,
                          beats_baseline=bool(np.isfinite(dci["diff_lo"]) and dci["diff_lo"] > 0 and s["n"] >= MIN_N)))
    R, D = pd.DataFrame(rows), pd.DataFrame(diffs)
    OUT.mkdir(parents=True, exist_ok=True)
    R.to_csv(OUT / "results_by_rule.csv", index=False, float_format="%.4f")
    D.to_csv(OUT / "results_filter_vs_baseline.csv", index=False, float_format="%.4f")
    counts = G.groupby(["kind", "rr_tf"], dropna=False).size().rename("n_legs").reset_index()
    counts.to_csv(OUT / "targets_first_status_counts.csv", index=False)
    meta = dict(legs_sha256=got, frozen_legs_sha256=want, pbp=str(PBP.relative_to(ROOT)), pbp_sha256=sha256(PBP),
                params=str((PHASE4 / "params_w4_7.json").relative_to(ROOT)), bootstrap_B=B, bootstrap_seed=0,
                open_meteo_wk6_8=str(OM_WK6_8), open_meteo_wk6_8_sha256=sha256(OM_WK6_8) if OM_WK6_8.exists() else None,
                min_n=MIN_N, cuts_enabled=CUTS_ENABLED, projection_ready=False, odds_api_credits=0)
    (OUT / "run_meta.json").write_text(json.dumps(meta, indent=1) + "\n")
    (OUT / "REPORT.md").write_text(render_report(R, D, meta))
    pd.set_option("display.width", 250)
    pd.set_option("display.max_rows", 500)
    c = ["rule", "view", "weeks", "group", "n", "W", "L", "hit", "be", "margin", "margin_lo", "margin_hi", "roi", "verdict"]
    print(R[c].round(3).to_string(index=False))
    print(D.round(3).to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
