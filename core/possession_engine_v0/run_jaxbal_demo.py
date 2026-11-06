"""Run bounded JAX@BAL possession sims under frozen configs; write artifacts. Research only."""
from __future__ import annotations
import json, time
from pathlib import Path
from config_load import load_config
from pbp_filter import load_team_history
from situational import build_situational_report
from provenance import build_default_registry, write_registry
from adjustment_ledger import build_ledger, write_ledger
from simulate import simulate_games, stable_seed
from adjustments import apply_forward_qb_filter

ROOT = Path(__file__).resolve().parent
PBP = ROOT.parent / "period_engine_v0/data/play_by_play_2026.parquet"
ART = ROOT / "artifacts"
ART.mkdir(exist_ok=True)


def main():
    hist = load_team_history(PBP, teams=["JAX", "BAL"], season=2026, weeks=(1, 8))
    sit = build_situational_report(hist["df"], hist.get("games_df"))
    (ART / "situational_jax_bal_w1_8.json").write_text(json.dumps(sit, indent=2) + "\n")

    results = {}
    # Practical N: try 10k; if slow report — target <120s for 10k
    # Practical N: ~20ms/game → 2k≈40s/config. 100k≈33min/config = RUNTIME_BLOCKER this session.
    PRACTICAL_N = 2000
    for cfg_name, n in [
        ("jax_bal_tnf_2026-11-05_data_only.json", PRACTICAL_N),
        ("jax_bal_tnf_2026-11-05_script_adjusted.json", PRACTICAL_N),
    ]:
        cfg = load_config(ROOT / "config" / cfg_name)
        seed = stable_seed(cfg["seed_base"], 9, cfg["config_id"])
        t0 = time.perf_counter()
        out = simulate_games(cfg, pbp_path=PBP, n=n, seed=seed)
        elapsed = time.perf_counter() - t0
        # strip large arrays to summary
        import numpy as np
        A = out["arrays"]
        summary = {
            k: v for k, v in out.items() if k not in ("arrays", "player_joint")
        }
        summary["runtime_sec"] = elapsed
        summary["score_means"] = {
            "fg_home": float(np.mean(A["fg_home"])),
            "fg_away": float(np.mean(A["fg_away"])),
            "reg_home": float(np.mean(A["reg_home"])),
            "reg_away": float(np.mean(A["reg_away"])),
            "p_ot": float(np.mean(A["went_ot"])),
        }
        summary["player_joint_top"] = {
            kind: {tm: dict(sorted(pl.items(), key=lambda x: -x[1])[:5]) for tm, pl in teams.items()}
            for kind, teams in out["player_joint"].items()
        }
        results[cfg["config_id"]] = summary
        write_ledger(ART / f"ledger_{cfg['config_id']}.json", build_ledger(cfg))
        print(cfg["config_id"], "n", out["n_completed"], "sec", round(elapsed, 2), "status", out["status"], "means", summary["score_means"])

    # provenance with script_adjusted meta
    cfg_adj = load_config(ROOT / "config/jax_bal_tnf_2026-11-05_script_adjusted.json")
    _, adj_meta = apply_forward_qb_filter(hist["df"], cfg_adj["adjustments"])
    reg = build_default_registry(hist_evidence=hist["evidence"], adj_meta=adj_meta, situational_ns=sit["ns"])
    write_registry(ART / "input_provenance_registry.json", reg)

    # market informed: document only (sampler not conditioned yet)
    cfg_m = load_config(ROOT / "config/jax_bal_tnf_2026-11-05_market_informed.json")
    write_ledger(ART / f"ledger_{cfg_m['config_id']}.json", build_ledger(cfg_m))
    results["market_informed_note"] = {
        "config_id": cfg_m["config_id"],
        "sampler_conditioned": False,
        "quotes_status": cfg_m["market_conditioning"]["quotes_status"],
        "contaminates_data_only": False,
        "note": "Config frozen separate; conditioning not wired to sampler — avoids false baseline contamination",
    }

    results["run_size_policy"] = {
        "practical_n": PRACTICAL_N,
        "per_game_ms_approx": 20,
        "n_100k_status": "RUNTIME_BLOCKER",
        "n_100k_est_sec_per_config": 2000,
        "note": "Do not fabricate 100k outputs; re-run when compute budget allows",
        "score_level_limitation": "Vertical slice empirical offense bootstrap overstates mean points vs NFL norms — not calibrated; research only",
    }
    (ART / "sim_jaxbal_summary.json").write_text(json.dumps(results, indent=2) + "\n")
    print("wrote artifacts to", ART)


if __name__ == "__main__":
    main()
