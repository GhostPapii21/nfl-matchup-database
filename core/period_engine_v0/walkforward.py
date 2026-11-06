"""Walk-forward Weeks 1–8 2026. Accuracy only — no period-price edge claims.

Labels:
  split=test for each kickoff-week prediction (as-of pool = train features only).
  Previous ceb6ab3 metrics preserved under artifacts/pre_fix_v0_ceb6ab3/.
  Development vs untouched: entire W1–8 remains the inspected development test set
  (Ghost6: no second untouched season). Do not retune to beat baselines.
"""
from __future__ import annotations
import json, shutil
from pathlib import Path
import numpy as np
import pandas as pd
from reconstruct import load_pbp, period_table_from_pbp, as_of_mask
from monte_carlo import simulate_game, STATUS, stable_seed

ROOT = Path(__file__).resolve().parent
ART = ROOT / "artifacts"
ART.mkdir(exist_ok=True)
PRE = ART / "pre_fix_v0_ceb6ab3"

PERIODS_EVAL = [
    ("q1", "q1_home", "q1_away"),
    ("q2", "q2_home", "q2_away"),
    ("q3", "q3_home", "q3_away"),
    ("q4", "q4_home", "q4_away"),
    ("h1", "h1_home", "h1_away"),
    ("reg", "reg_home", "reg_away"),
    ("fg", "fg_home", "fg_away"),
]


def brier(p, y):
    p = np.asarray(p, float); y = np.asarray(y, float)
    return float(np.mean((p - y) ** 2))


def logloss(p, y, eps=1e-6):
    p = np.clip(np.asarray(p, float), eps, 1 - eps)
    y = np.asarray(y, float)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def build_history():
    p26 = period_table_from_pbp(load_pbp(ROOT / "data/play_by_play_2026.parquet"))
    p25 = period_table_from_pbp(load_pbp(ROOT / "data/play_by_play_2025.parquet"))
    return pd.concat([p25, p26], ignore_index=True), p26


def league_mean_totals(asof: pd.DataFrame, period: str):
    ph, pa = f"{period}_home", f"{period}_away"
    if asof.empty:
        return None, None
    return float(asof[ph].mean()), float(asof[pa].mean())


def baseline_home_win(asof: pd.DataFrame, period: str):
    ph, pa = f"{period}_home", f"{period}_away"
    if asof.empty:
        return None, None
    m = asof[ph].to_numpy() - asof[pa].to_numpy()
    return float((m > 0).mean()), float((m == 0).mean())


def run_walkforward(n_sims: int = 20_000, seed: int = 20261105):
    # preserve prior summary if present and not already archived
    PRE.mkdir(exist_ok=True)
    for name in ("walkforward_2026_w1_8_summary.json", "walkforward_2026_w1_8_by_week.csv", "walkforward_2026_w1_8_detail.csv"):
        src = ART / name
        if src.exists() and not (PRE / name).exists():
            shutil.copy2(src, PRE / name)

    hist, p26 = build_history()
    rows = []
    missing = []
    for _, g in p26.sort_values(["week", "game_id"]).iterrows():
        season, week = int(g.season), int(g.week)
        home, away = g.home_team, g.away_team
        asof = hist[as_of_mask(hist, season, week)]
        prior_n = int((asof.season < season).sum()) if len(asof) else 0
        same_n = int((asof.season == season).sum()) if len(asof) else 0
        note = []
        if week == 1 and prior_n == 0:
            note.append("WEEK1_NO_PRIOR_SEASON")
        s = stable_seed(seed, week, str(g.game_id))
        sim = simulate_game(asof, home, away, n=n_sims, seed=s, apply_gr=False)
        if sim.get("error"):
            missing.append(dict(game_id=g.game_id, week=week, reason=sim["error"]))
            continue
        st = sim["status"]
        for period, ch, ca in PERIODS_EVAL:
            if period not in sim["summaries"]:
                continue
            pred_h = sim["summaries"][period]["home_mean"]
            pred_a = sim["summaries"][period]["away_mean"]
            act_h = float(g[ch]); act_a = float(g[ca])
            Ah, Aa = sim["arrays"][f"{period}_home"], sim["arrays"][f"{period}_away"]
            p_side = float(((Ah - Aa) > 0).mean())
            p_tie = float(((Ah - Aa) == 0).mean())
            y_side = 1.0 if act_h > act_a else 0.0  # binary: ties as non-wins (documented)
            y_tie = 1.0 if act_h == act_a else 0.0
            base_p, base_tie = baseline_home_win(asof, period)
            lm_h, lm_a = league_mean_totals(asof, period)
            team_emp_h = float(pd.concat([
                asof.loc[asof.home_team == home, f"{period}_home"],
                asof.loc[asof.away_team == home, f"{period}_away"],
            ]).mean()) if st["home_games_asof"] else None
            team_emp_a = float(pd.concat([
                asof.loc[asof.home_team == away, f"{period}_home"],
                asof.loc[asof.away_team == away, f"{period}_away"],
            ]).mean()) if st["away_games_asof"] else None
            rows.append(dict(
                game_id=g.game_id, week=week, home=home, away=away, period=period,
                status="OK",
                seed=s,
                mae_home=abs(pred_h - act_h), mae_away=abs(pred_a - act_a),
                mae_margin=abs((pred_h - pred_a) - (act_h - act_a)),
                mae_total=abs((pred_h + pred_a) - (act_h + act_a)),
                mae_total_league_mean=(abs((lm_h + lm_a) - (act_h + act_a)) if lm_h is not None else None),
                mae_total_team_empirical=(abs((team_emp_h + team_emp_a) - (act_h + act_a)) if team_emp_h is not None and team_emp_a is not None else None),
                brier_home_win=brier([p_side], [y_side]),
                logloss_home_win=logloss([p_side], [y_side]),
                baseline_brier=brier([base_p], [y_side]) if base_p is not None else None,
                p_home_win=p_side, p_tie=p_tie, actual_home_win=y_side, actual_tie=y_tie,
                pred_home=pred_h, actual_home=act_h, pred_away=pred_a, actual_away=act_a,
                asof_home_games=st["home_games_asof"], asof_away_games=st["away_games_asof"],
                prior_season_games_in_pool=prior_n, same_season_prior_weeks_games=same_n,
                went_ot=bool(g.get("went_ot", False)),
                score_scope=g.get("score_scope_fg") if period == "fg" else ("regulation_only" if period != "fg" else None),
                notes=";".join(note) if note else "",
                split="test_asof_walkforward",
                set_label="development_inspected_w1_8_not_untouched_holdout",
                train_pool="asof_games_only_strictly_before_kickoff_week",
            ))
    df = pd.DataFrame(rows)
    summary = []
    for week, wdf in df.groupby("week"):
        ok = wdf[wdf.status == "OK"]
        summary.append(dict(
            week=int(week), n_rows=len(wdf), n_ok=len(ok), n_games=wdf.game_id.nunique(),
            mae_q1_total=float(ok[ok.period=="q1"].mae_total.mean()) if len(ok[ok.period=="q1"]) else None,
            mae_h1_total=float(ok[ok.period=="h1"].mae_total.mean()) if len(ok[ok.period=="h1"]) else None,
            mae_reg_total=float(ok[ok.period=="reg"].mae_total.mean()) if len(ok[ok.period=="reg"]) else None,
            mae_fg_total=float(ok[ok.period=="fg"].mae_total.mean()) if len(ok[ok.period=="fg"]) else None,
            mae_fg_league=float(ok[ok.period=="fg"].mae_total_league_mean.mean()) if len(ok[ok.period=="fg"]) else None,
            brier_h1=float(ok[ok.period=="h1"].brier_home_win.mean()) if len(ok[ok.period=="h1"]) else None,
            baseline_brier_h1=float(ok[ok.period=="h1"].baseline_brier.mean()) if len(ok[ok.period=="h1"]) else None,
            brier_q1=float(ok[ok.period=="q1"].brier_home_win.mean()) if len(ok[ok.period=="q1"]) else None,
            baseline_brier_q1=float(ok[ok.period=="q1"].baseline_brier.mean()) if len(ok[ok.period=="q1"]) else None,
            brier_q4=float(ok[ok.period=="q4"].brier_home_win.mean()) if len(ok[ok.period=="q4"]) else None,
            baseline_brier_q4=float(ok[ok.period=="q4"].baseline_brier.mean()) if len(ok[ok.period=="q4"]) else None,
        ))
    summ_df = pd.DataFrame(summary)
    overall = {
        "engine": "period_engine_v0_post_ghost6_fix",
        "model_status": STATUS.__dict__,
        "n_sims_per_game": n_sims,
        "seed_base": seed,
        "seed_fn": "stable_seed=sha256(base|week|game_id)",
        "games_2026": int(p26.game_id.nunique()),
        "rows": int(len(df)),
        "ok_rows": int((df.status == "OK").sum()),
        "missing_games": missing,
        "mae_by_period": {p: float(df[df.period==p].mae_total.mean()) for p, _, _ in PERIODS_EVAL},
        "mae_league_mean_by_period": {p: float(df[df.period==p].mae_total_league_mean.mean()) for p, _, _ in PERIODS_EVAL},
        "brier_home_win_by_period": {p: float(df[df.period==p].brier_home_win.mean()) for p, _, _ in PERIODS_EVAL},
        "baseline_brier_home_win_by_period": {p: float(df[df.period==p].baseline_brier.mean()) for p, _, _ in PERIODS_EVAL},
        "pre_fix_artifact_dir": str(PRE),
        "set_label": "development_inspected_w1_8_not_untouched_holdout",
        "limitations": [
            "NO historical period market prices — accuracy only; NO profitability/edge",
            "Bias UNIMPLEMENTED; GR UNFITTED and not used in walk-forward",
            "Binary home-win Brier treats ties as non-wins (not full 3-way grade)",
            "Independent team bootstrap; no opponent interaction / possession clock",
            "League-mean baseline reported honestly — MC is not claimed better",
            "W1–8 is development/inspected test; no untouched second-season holdout",
            "Previous ceb6ab3 failures/results preserved under artifacts/pre_fix_v0_ceb6ab3/",
            "fg = official final incl OT; reg = end Q4; do not map reg to FG book totals",
        ],
        "split_policy": "For each 2026 week W game, history uses only (season,week) strictly before (2026,W). 2025 REG for Week1+.",
    }
    df.to_csv(ART / "walkforward_2026_w1_8_detail.csv", index=False)
    summ_df.to_csv(ART / "walkforward_2026_w1_8_by_week.csv", index=False)
    (ART / "walkforward_2026_w1_8_summary.json").write_text(json.dumps(overall, indent=2) + "\n")
    # comparison vs pre-fix
    if (PRE / "walkforward_2026_w1_8_summary.json").exists():
        prev = json.loads((PRE / "walkforward_2026_w1_8_summary.json").read_text())
        cmp = {"pre_fix_mae": prev.get("mae_by_period"), "post_fix_mae": overall["mae_by_period"],
               "pre_fix_brier": prev.get("brier_home_win_by_period"), "post_fix_brier": overall["brier_home_win_by_period"],
               "league_mae_post": overall["mae_league_mean_by_period"]}
        (ART / "walkforward_pre_vs_post_fix.json").write_text(json.dumps(cmp, indent=2) + "\n")
    print(json.dumps({k: overall[k] for k in overall if k != "missing_games"}, indent=2))
    print(summ_df.to_string(index=False))
    return df, summ_df, overall


if __name__ == "__main__":
    run_walkforward()
