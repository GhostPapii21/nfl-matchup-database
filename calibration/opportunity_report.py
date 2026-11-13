"""NFL-75 Phase 2: metrics from research/runs/2026-11-13_opportunity_phase2/backtest_raw.json.
    python3 -m calibration.opportunity_report
Per position: opportunity calibration (targets / carries / attempts) for the name-locked recorder (main) and the
opportunity model: mean error (sim mean - actual), MAE, coverage of the sim p10-p90 interval (nominal 80%); Brier on
reception / yard thresholds; 95% CIs by game-cluster bootstrap (2,000 resamples, seed 75). Player universe per stat:
player-games where the player had >= 1 actual opportunity of that kind or either model projected a mean >= 1.
Missing actual line = 0 opportunities (the player recorded none in the PBP); missing model line = 0 in every trial
(the model never gave him one). Research only. projection_ready stays false."""
from __future__ import annotations
import json
from collections import defaultdict

import numpy as np

from calibration import opportunity_fit as F
from calibration.opportunity_backtest import OUT, OPP_BY_GROUP, THRESH

B = 2000
EXCL = {"UNASSIGNED", "UNLISTED"}
BRIER_GROUPS = {"rec": ("RB", "WR", "TE"), "rec_yds": ("RB", "WR", "TE"), "rush_yds": ("RB", "QB")}
BRIER_OPP = {"rec": "targets", "rec_yds": "targets", "rush_yds": "carries"}


def name_pos() -> dict:
    o = F.opp_rows(2026).dropna(subset=["pid"])
    pos = F.positions()
    m = {}
    for (t, n), g in o.groupby(["team", "name"]):
        m[(t, n)] = F.group(pos.get(g["pid"].mode().iat[0], "UNK"))
    return m


def _boot(gidx, vals, fn, rng):
    """Cluster bootstrap over games. vals: dict of arrays aligned with gidx."""
    games = np.unique(gidx)
    rows_by = {g: np.where(gidx == g)[0] for g in games}
    est = fn({k: v for k, v in vals.items()})
    bs = []
    for _ in range(B):
        pick = rng.choice(games, size=len(games), replace=True)
        ix = np.concatenate([rows_by[g] for g in pick])
        bs.append(fn({k: v[ix] for k, v in vals.items()}))
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return [round(float(est), 4), round(float(lo), 4), round(float(hi), 4)]


def build_rows(raw) -> list:
    npos = name_pos()
    rows = []
    for g in raw["games"]:
        act = raw["actual"][str(g["week"])]
        for team in (g["home"], g["away"]):
            keys = {k for k in list(act) + list(g["name_locked"]) + list(g["opportunity"])
                    if k.split("|", 1)[0] == team and k.split("|", 1)[1] not in EXCL}
            for k in keys:
                nm = k.split("|", 1)[1]
                rows.append({"game": g["game_id"], "week": g["week"], "team": team, "name": nm,
                             "grp": npos.get((team, nm), "UNK"), "act": act.get(k, {}),
                             "base": g["name_locked"].get(k, {}), "opp": g["opportunity"].get(k, {})})
    return rows


def _get(d, stat, key):
    return float(d.get(stat, {}).get(key, 0.0))


def metrics(raw) -> dict:
    rng = np.random.default_rng(75)
    rows = build_rows(raw)
    out = {"opportunity": [], "brier": []}
    for grp, stats in OPP_BY_GROUP.items():
        for stat in stats:
            sel = [r for r in rows if r["grp"] == grp and (r["act"].get(stat, 0) >= 1 or _get(r["base"], stat, "mean") >= 1
                                                         or _get(r["opp"], stat, "mean") >= 1)]
            if not sel:
                continue
            gidx = np.array([r["game"] for r in sel])
            a = np.array([float(r["act"].get(stat, 0)) for r in sel])
            rec = {"group": grp, "stat": stat, "n_player_games": len(sel), "n_games": int(len(np.unique(gidx))),
                   "actual_mean": round(float(a.mean()), 3)}
            for mdl in ("base", "opp"):
                mu = np.array([_get(r[mdl], stat, "mean") for r in sel])
                p10 = np.array([_get(r[mdl], stat, "p10") for r in sel])
                p90 = np.array([_get(r[mdl], stat, "p90") for r in sel])
                cov = ((a >= p10) & (a <= p90)).astype(float)
                v = {"e": mu - a, "ae": np.abs(mu - a), "c": cov}
                rec[mdl] = {"mean_error": _boot(gidx, v, lambda d: d["e"].mean(), rng),
                            "mae": _boot(gidx, v, lambda d: d["ae"].mean(), rng),
                            "coverage_p10_p90": _boot(gidx, v, lambda d: d["c"].mean(), rng)}
                rec[mdl]["_ae"], rec[mdl]["_c"] = v["ae"], cov
            d = {"dae": rec["opp"].pop("_ae") - rec["base"].pop("_ae"), "dc": rec["opp"].pop("_c") - rec["base"].pop("_c")}
            rec["opp_minus_base"] = {"mae": _boot(gidx, d, lambda x: x["dae"].mean(), rng),
                                     "coverage": _boot(gidx, d, lambda x: x["dc"].mean(), rng)}
            out["opportunity"].append(rec)
    for stat, thrs in THRESH.items():
        for grp in BRIER_GROUPS[stat]:
            opp = BRIER_OPP[stat]
            sel = [r for r in rows if r["grp"] == grp and (r["act"].get(opp, 0) >= 1 or _get(r["base"], opp, "mean") >= 1
                                                         or _get(r["opp"], opp, "mean") >= 1)]
            if not sel:
                continue
            gidx = np.array([r["game"] for r in sel])
            for thr in thrs:
                y = np.array([float(r["act"].get(stat, 0) >= thr) for r in sel])
                pb = np.array([_get(r["base"], stat, f"p_ge{thr}") for r in sel])
                po = np.array([_get(r["opp"], stat, f"p_ge{thr}") for r in sel])
                v = {"b": (pb - y) ** 2, "o": (po - y) ** 2}
                out["brier"].append({
                    "group": grp, "stat": stat, "threshold": f">= {thr}", "n_player_games": len(sel),
                    "base_rate": round(float(y.mean()), 4),
                    "brier_base": _boot(gidx, v, lambda d: d["b"].mean(), rng),
                    "brier_opp": _boot(gidx, v, lambda d: d["o"].mean(), rng),
                    "opp_minus_base": _boot(gidx, v, lambda d: (d["o"] - d["b"]).mean(), rng),
                    "climatology_brier": round(float(y.mean() * (1 - y.mean())), 4)})
    below = [f"{r['group']} {r['stat']} {r['threshold']}" for r in out["brier"] if r["opp_minus_base"][2] < 0]
    above = [f"{r['group']} {r['stat']} {r['threshold']}" for r in out["brier"] if r["opp_minus_base"][1] > 0]
    out["brier_summary"] = {"thresholds": len(out["brier"]), "ci_fully_below_zero": len(below),
                            "ci_fully_below_zero_list": below, "ci_fully_above_zero": len(above),
                            "point_estimate_le_zero": int(sum(1 for r in out["brier"] if r["opp_minus_base"][0] <= 0))}
    out["int_zero"] = int_zero_table(raw, rows)
    out["recon"] = {"games": len(raw["games"]),
                    "name_locked_failed_trials": int(sum(g["recon"]["name_locked_failures"] for g in raw["games"])),
                    "opportunity_failed_trials": int(sum(g["recon"]["opportunity_failures"] for g in raw["games"]))}
    out["unknown_position_player_games"] = int(sum(1 for r in rows if r["grp"] == "UNK"))
    return out


def team_pool_int_rows(team: str, week: int) -> int:
    """Interception dropback rows in the team's own 2026 history before `week` (the engine's team row pool)."""
    o = F.opp_rows(2026)
    d = o[(o["team"] == team) & (o["week"] < week) & (o["slot"] == "dropback")]
    return int(d["feat"].fillna("").str.endswith("|int").sum())


def int_zero_table(raw, rows=None, min_att: int = 10) -> dict:
    """History-capped events check: QB-games with >= min_att actual attempts; how many get P(INT>=1)=0 per model,
    how many of those had an actual INT, mean P, actual rate, Brier (descriptive, no CI). For the opportunity model's
    zero-probability games the reason is classified: QB not a candidate (no opportunity line) vs team row pool without
    any INT row before the eval week (engine-level cap)."""
    rows = rows if rows is not None else build_rows(raw)
    q = [r for r in rows if r["grp"] == "QB" and r["act"].get("pass_att", 0) >= min_att]
    y = np.array([float(r["act"].get("int_thrown", 0) >= 1) for r in q])
    out = {"qb_games": len(q), "min_actual_attempts": min_att, "models": {}}
    for m, lab in (("base", "name_locked_main"), ("opp", "opportunity")):
        p = np.array([float(r[m].get("int_thrown", {}).get("p_ge1", 0.0)) for r in q])
        z = p == 0
        out["models"][lab] = {"p_zero_games": int(z.sum()), "p_zero_with_actual_int": int(y[z].sum()),
                              "mean_p": round(float(p.mean()), 4), "actual_rate": round(float(y.mean()), 4),
                              "brier": round(float(np.mean((p - y) ** 2)), 4)}
    zl = []
    for r in q:
        if float(r["opp"].get("int_thrown", {}).get("p_ge1", 0.0)) == 0:
            att = float(r["opp"].get("pass_att", {}).get("mean", 0.0))
            pool = team_pool_int_rows(r["team"], r["week"])
            zl.append({"game": r["game"], "team": r["team"], "qb": r["name"], "opp_mean_att": round(att, 1),
                       "team_pool_int_rows": pool,
                       "reason": "not_a_candidate" if att == 0 else ("team_pool_no_int_rows" if pool == 0 else "other")})
    out["opportunity_p_zero_games"] = zl
    out["reason_counts"] = {k: sum(1 for z in zl if z["reason"] == k) for k in ("not_a_candidate", "team_pool_no_int_rows", "other")}
    return out


def fmt(x):
    return f"{x[0]:+.3f} [{x[1]:+.3f}, {x[2]:+.3f}]"


def fmtp(x):
    return f"{x[0]:.3f} [{x[1]:.3f}, {x[2]:.3f}]"


def markdown(m, raw) -> str:
    L = ["# Phase 2 opportunity model: walk-forward Weeks 4-9 (2026), name-locked (main) vs opportunity model", "",
         f"n = {raw['n']} trials per game, {m['recon']['games']} games, seed {raw['seed']}; engine git head "
         f"{raw['engine']['git_head'][:7]} (engine dirty={raw['engine']['engine_dirty']}). 95% CIs: game-cluster bootstrap "
         f"({B} resamples). Reconciliation failures: name-locked {m['recon']['name_locked_failed_trials']}, "
         f"opportunity {m['recon']['opportunity_failed_trials']}. Research only, not validated; projection_ready=false.", "",
         "## Opportunity calibration (sim vs actual per player-game)", "",
         "| pos | stat | player-games | actual mean | ME main | ME opp | MAE main | MAE opp | MAE opp-main | p10-p90 cov main | p10-p90 cov opp | cov opp-main |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in m["opportunity"]:
        L.append(f"| {r['group']} | {r['stat']} | {r['n_player_games']} | {r['actual_mean']} | {fmt(r['base']['mean_error'])} | "
                 f"{fmt(r['opp']['mean_error'])} | {fmtp(r['base']['mae'])} | {fmtp(r['opp']['mae'])} | "
                 f"{fmt(r['opp_minus_base']['mae'])} | {fmtp(r['base']['coverage_p10_p90'])} | "
                 f"{fmtp(r['opp']['coverage_p10_p90'])} | {fmt(r['opp_minus_base']['coverage'])} |")
    L += ["", "Nominal p10-p90 coverage is 0.80 (counts are discrete and the interval is inclusive, so a calibrated "
          "model can sit somewhat above 0.80).", "", "## Brier on reception / yard thresholds", "",
          "| pos | stat | threshold | player-games | base rate | Brier main | Brier opp | opp-main | climatology |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in m["brier"]:
        L.append(f"| {r['group']} | {r['stat']} | {r['threshold']} | {r['n_player_games']} | {r['base_rate']} | "
                 f"{fmtp(r['brier_base'])} | {fmtp(r['brier_opp'])} | {fmt(r['opp_minus_base'])} | {r['climatology_brier']} |")
    bs = m["brier_summary"]
    L += ["", "Negative opp-main = the opportunity model is better (lower MAE / Brier). A CI that crosses 0 is not a "
          "demonstrated difference.", "",
          f"Brier summary (computed): {bs['ci_fully_below_zero']} of {bs['thresholds']} thresholds have a 95% CI fully "
          f"below 0 ({', '.join(bs['ci_fully_below_zero_list'])}); {bs['ci_fully_above_zero']} fully above 0; "
          f"{bs['point_estimate_le_zero']} of {bs['thresholds']} point estimates <= 0.", ""]
    iz = m["int_zero"]
    L += [f"## History-capped events: QB interceptions (QBs with >= {iz['min_actual_attempts']} actual attempts)", "",
          "| model | QB-games | games with P(INT>=1)=0 | of those, actual INT games | mean P(INT>=1) | actual rate | Brier |",
          "|---|---|---|---|---|---|---|"]
    for lab, v in iz["models"].items():
        L.append(f"| {lab} | {iz['qb_games']} | {v['p_zero_games']} | {v['p_zero_with_actual_int']} | {v['mean_p']:.3f} | "
                 f"{v['actual_rate']:.3f} | {v['brier']:.4f} |")
    rc = iz["reason_counts"]
    L += ["", f"INT Brier is slightly WORSE with the opportunity model ({iz['models']['opportunity']['brier']:.4f} vs "
          f"{iz['models']['name_locked_main']['brier']:.4f}); the gain is only in the zero-probability column. Do not price "
          "INT props from this model.", "",
          f"Opportunity-model P(INT>=1)=0 games by reason: not a candidate {rc['not_a_candidate']}, team row pool had no "
          f"INT row before the eval week {rc['team_pool_no_int_rows']} (engine-level cap), other {rc['other']}:", "",
          "| game | team | QB | opp mean att | team pool INT rows | reason |", "|---|---|---|---|---|---|"]
    for z in iz["opportunity_p_zero_games"]:
        L.append(f"| {z['game']} | {z['team']} | {z['qb']} | {z['opp_mean_att']} | {z['team_pool_int_rows']} | {z['reason']} |")
    L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    raw = json.loads((OUT / "backtest_raw.json").read_text())
    m = metrics(raw)
    (OUT / "metrics.json").write_text(json.dumps(m, indent=1) + "\n")
    (OUT / "metrics.md").write_text(markdown(m, raw))
    print(markdown(m, raw))
