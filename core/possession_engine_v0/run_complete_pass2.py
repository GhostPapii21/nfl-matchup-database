"""Completion pass 2 grading: accounting, matched-game pace/drive realism, as-of FG + period grades
(data_only vs research variant), baselines, game-bootstrap CIs, MC SE. Development W1-8, NOT holdout."""
from __future__ import annotations
import json, time, sys
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config_load import load_config
from validation.accounting import run_accounting_checks
from validation.realism import compare_sim_vs_actual_pace
from validation.asof_grade import grade_week_games
from validation.period_grade import grade_periods_for_games
from simulate import simulate_games

ROOT = Path(__file__).resolve().parent
PBP = ROOT.parent / "period_engine_v0/data/play_by_play_2026.parquet"
ART = ROOT / "artifacts/validation/pass2"
ART.mkdir(parents=True, exist_ok=True)
CFGS = {"data_only": ROOT / "config/jax_bal_tnf_2026-11-05_data_only.json",
        "variant_def_allowed_w05": ROOT / "config/research_variant_def_allowed_w05.json"}
N, SEED = 150, 20261105


def boot_ci(x, B=2000, seed=0):
    x = np.asarray([v for v in x if v is not None and not np.isnan(v)], float)
    if len(x) < 2:
        return None
    r = np.random.default_rng(seed)
    m = [r.choice(x, len(x)).mean() for _ in range(B)]
    return [float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))]


def paired_game_diffs(g: pd.DataFrame) -> np.ndarray:
    """One observation per game: mean of home/away (model - baseline) abs errors (paired)."""
    return (((g.abs_err_home - g.baseline_abs_err_home) + (g.abs_err_away - g.baseline_abs_err_away)) / 2).to_numpy()


def main():
    out = {"started_et": time.strftime("%Y-%m-%d %H:%M:%S %Z"), "label": "development_w1_8_inspected_NOT_holdout",
           "n_sims_per_game": N, "seed_base": SEED}
    t = time.time()
    acct = run_accounting_checks(load_config(CFGS["data_only"]), pbp_path=PBP, n=200, seed=SEED)
    out["accounting"] = {"checks": acct.get("checks"), "runtime_sec": round(time.time() - t, 1)}
    for name, cp in CFGS.items():
        cfg = load_config(cp)
        t = time.time()
        sg = simulate_games(cfg, pbp_path=PBP, n=300, seed=SEED)
        out[f"jaxbal_{name}"] = {
            "evidence_summary": sg["evidence_summary"], "effects_provenance": sg["effects_provenance"],
            "mean_fg_home_BAL": float(sg["arrays"]["fg_home"].mean()), "mean_fg_away_JAX": float(sg["arrays"]["fg_away"].mean()),
            "mc_se_fg_home": float(sg["arrays"]["fg_home"].std(ddof=1) / np.sqrt(300)),
            "n": 300, "seed": SEED, "runtime_sec": round(time.time() - t, 1)}
        t = time.time()
        pace = compare_sim_vs_actual_pace(cfg, pbp_path=PBP, n_sims=200, seed=11)
        out[f"pace_{name}"] = {**pace, "runtime_sec": round(time.time() - t, 1)}
        t = time.time()
        rows = grade_week_games(PBP, weeks=list(range(1, 9)), n_sims=N, seed_base=SEED, config_path=cp)
        df = pd.DataFrame(rows)
        df.to_csv(ART / f"asof_fg_{name}.csv", index=False)
        g = df[df.grade_status == "GRADED_FULL"]
        e = np.r_[g.abs_err_home, g.abs_err_away]; b = np.r_[g.baseline_abs_err_home, g.baseline_abs_err_away]
        out[f"asof_fg_{name}"] = {
            "n_games": int(len(df)), "n_graded": int(len(g)),
            "skips": df[df.grade_status != "GRADED_FULL"][["game_id", "grade_status"]].to_dict("records"),
            "mae_model": float(e.mean()), "mae_baseline_asof_ppg": float(b.mean()),
            "mae_diff_model_minus_baseline": float((e - b).mean()), "diff_boot95_game_unit": boot_ci(paired_game_diffs(g)),
            "runtime_sec": round(time.time() - t, 1)}
        t = time.time()
        per = grade_periods_for_games(PBP, rows, n_sims=N, seed_base=SEED, config_path=cp)
        pd.DataFrame(per["by_game"]).to_csv(ART / f"period_{name}.csv", index=False)
        pg = pd.DataFrame([r for r in per["by_game"] if r.get("period_grade_status") == "GRADED_PERIODS"])
        m = per["metrics"]
        # naive baselines: half = as-of PPG/2; Brier constant 0.5 -> 0.25
        gb = g.set_index("game_id")
        hb = []
        for _, r in pg.iterrows():
            bh, ba = gb.loc[r.game_id, "baseline_home_ppg"], gb.loc[r.game_id, "baseline_away_ppg"]
            hb += [abs(bh / 2 - r.actual_h1_home), abs(ba / 2 - r.actual_h1_away)]
        m["mae_h1_baseline_ppg_half"] = float(np.mean(hb)) if hb else None
        m["brier_baseline_coinflip"] = 0.25
        m["brier_reg_boot95"] = boot_ci(pg["brier_reg_home_win"]) if len(pg) else None
        m["mae_h1_model"] = float(np.mean(np.r_[pg.abs_err_h1_home, pg.abs_err_h1_away])) if len(pg) else None
        out[f"period_{name}"] = {**m, "runtime_sec": round(time.time() - t, 1)}
    # Prior-season descriptive pressure/coverage (NOT executed in sim)
    try:
        participation = Path(__file__).resolve().parents[2] / "data" / "licensed" / "pbp_participation_2025.parquet"
        p = pd.read_parquet(participation,
                            columns=["nflverse_game_id", "possession_team", "was_pressure", "defense_man_zone_type"])
        p["def"] = [(a.split("_")[3] if a.split("_")[2] == pt else a.split("_")[2]) for a, pt in zip(p.nflverse_game_id, p.possession_team.fillna(""))]
        desc = {}
        for tm in ("JAX", "BAL"):
            s = p[(p["def"] == tm) & (p.defense_man_zone_type != "")]
            desc[tm] = {"n": int(len(s)), "pressure_rate": float(s.was_pressure.mean()),
                        "man_rate": float((s.defense_man_zone_type == "MAN_COVERAGE").mean())}
        out["prior_season_2025_participation_descriptive"] = {
            "status": "DESCRIPTIVE_ONLY_NOT_EXECUTED", "source": "nflverse pbp_participation_2025 (FTN, CC-BY-SA 4.0)",
            "why_not_executed": "2026 participation not published until post-season; 2025 rosters/coaching differ; no fitted mapping",
            "defense": desc}
    except Exception as ex:
        out["prior_season_2025_participation_descriptive"] = {"status": "ERROR", "error": str(ex)}
    out["finished_et"] = time.strftime("%Y-%m-%d %H:%M:%S %Z")
    (ART / "pass2_metrics.json").write_text(json.dumps(out, indent=2, default=str))
    print(json.dumps({k: v for k, v in out.items() if not k.startswith("pace_")}, indent=1, default=str)[:9000])
    for name in CFGS:
        pc = out[f"pace_{name}"]
        print(name, "pace sim", pc["sim"]["mean_snaps_per_game"], "actual", pc["actual_combined_offense_snaps"]["mean_combined_offense_snaps"], "drive", pc["actual"]["drive_length_plays"])


if __name__ == "__main__":
    main()
