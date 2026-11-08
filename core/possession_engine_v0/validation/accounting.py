"""Game accounting / realism checks on simulated games (development diagnostic)."""
from __future__ import annotations
from pathlib import Path
from typing import Any
import numpy as np
from simulate import simulate_games, stable_seed, PlayCatalog, simulate_one, build_catalog
from pbp_filter import load_team_history
from adjustments import apply_forward_qb_filter


def _event_counts(st) -> dict:
    from collections import Counter
    c = Counter(e.get("type") for e in st.events)
    snaps = sum(1 for e in st.events if e.get("type") == "snap")
    passes = sum(1 for e in st.events if e.get("type") == "snap" and e.get("play_type") == "pass")
    runs = sum(1 for e in st.events if e.get("type") == "snap" and e.get("play_type") == "run")
    # possessions ~ kickoffs + after turnovers/punts approximate
    poss = c.get("kickoff", 0)
    return {
        "n_events": len(st.events),
        "n_snap": snaps,
        "n_pass_snap": passes,
        "n_run_snap": runs,
        "n_punt": c.get("punt", 0),
        "n_td": c.get("touchdown", 0),
        "n_fg": c.get("field_goal", 0),
        "n_turnover": c.get("turnover", 0) + c.get("turnover_on_downs", 0),
        "n_kickoff": c.get("kickoff", 0),
        "n_halftime": c.get("halftime", 0),
        "n_ot_start": c.get("ot_start", 0),
        "score_h": st.score_home,
        "score_a": st.score_away,
        "reg_h": st.reg_score_home,
        "reg_a": st.reg_score_away,
        "in_ot": st.in_ot,
        "sparse_flags_n": len(st.sparse_flags),
    }


def run_accounting_checks(cfg: dict, *, pbp_path: str | Path, n: int = 50, seed: int = 11) -> dict[str, Any]:
    out = simulate_games(cfg, pbp_path=pbp_path, n=n, seed=seed)
    hist = load_team_history(
        pbp_path,
        teams=cfg["history"]["teams"],
        season=cfg["history"]["season"],
        weeks=(cfg["history"]["weeks_inclusive"][0], cfg["history"]["weeks_inclusive"][-1]),
    )
    df = hist["df"]
    if cfg.get("adjustments", {}).get("enabled"):
        df, _ = apply_forward_qb_filter(df, cfg["adjustments"])
    cat, _prov = build_catalog(df, cfg, games_df=hist.get("games_df"))
    # detailed counts on a batch of games
    rng = np.random.default_rng(seed)
    details = [_event_counts(simulate_one(df, cat, cfg, np.random.default_rng(int(rng.integers(0, 1_000_000))))) for _ in range(min(n, 40))]
    mean_plays = float(np.mean([d["n_snap"] for d in details]))
    mean_punts = float(np.mean([d["n_punt"] for d in details]))
    mean_td = float(np.mean([d["n_td"] for d in details]))
    mean_ko = float(np.mean([d["n_kickoff"] for d in details]))
    pct_ot = float(np.mean([d["in_ot"] for d in details]))
    # player-to-team: joint yards should be finite
    pj = out.get("player_joint") or {}
    joint_ok = isinstance(pj, dict)

    checks = []
    def add(name, ok, detail):
        checks.append({"name": name, "ok": bool(ok), "detail": detail})

    add("reg_clock_target_declared_3600", False,
        "UNIMPLEMENTED in legacy diagnostic: a declared 4x900 target is not measured elapsed-clock reconciliation")
    add("halftime_present_rate", float(np.mean([d["n_halftime"] >= 1 for d in details])) > 0.9,
        f"halftime_rate={float(np.mean([d['n_halftime']>=1 for d in details])):.3f}")
    add("q_sum_reg_scores_recorded", all(k in out.get("arrays", {}) for k in ("reg_home", "reg_away")),
        "array presence only; measured reconciliation checked separately")
    add("shared_contract_opportunity_and_player_accounting", False,
        "UNIMPLEMENTED legacy yard-row bootstrap; use frozen joint_producer path for checked event ledger")
    add("mean_snaps_in_band", 80 <= mean_plays <= 160, f"mean_snaps={mean_plays:.1f} (band 80-160 diagnostic)")
    add("kickoffs_ge_tds", float(np.mean([d["n_kickoff"] >= d["n_td"] for d in details])) > 0.85,
        "kickoff count should cover TDs+opening")
    add("sparse_rate_reported", out["evidence_summary"]["sparse_rate"] is not None,
        f"sparse_rate={out['evidence_summary']['sparse_rate']}")
    add("player_joint_present", joint_ok, "player_joint dict")
    A = out["arrays"]
    has_q = all(k in A for k in ("q1_home","q2_home","q3_home","q4_home","h1_home","h2_home"))
    recon = False
    if has_q:
        recon = bool(
            np.array_equal(A["h1_home"], A["q1_home"]+A["q2_home"])
            and np.array_equal(A["reg_home"], A["h1_home"]+A["h2_home"])
            and np.array_equal(A["h1_away"], A["q1_away"]+A["q2_away"])
            and np.array_equal(A["h2_home"], A["q3_home"]+A["q4_home"])
            and np.array_equal(A["h2_away"], A["q3_away"]+A["q4_away"])
            and np.array_equal(A["reg_away"], A["h1_away"]+A["h2_away"])
            and np.array_equal(A["fg_home"], A["reg_home"]+A["ot_home"])
            and np.array_equal(A["fg_away"], A["reg_away"]+A["ot_away"])
        )
    add("period_quarter_scores_in_sim", has_q and recon, "Q1-Q4/H1/H2/reg/fg arrays + reconciliation")
    add("ot_only_if_reg_tie", bool(np.all(~out["arrays"]["went_ot"] | (out["arrays"]["reg_home"] == out["arrays"]["reg_away"]))),
        "OT flag only when reg tied")

    n_fail = sum(1 for c in checks if not c["ok"])
    n_pass = sum(1 for c in checks if c["ok"])
    overall = "PASS" if n_fail == 0 else ("MIXED" if n_pass else "FAIL")
    if any(c["name"] == "period_quarter_scores_in_sim" and not c["ok"] for c in checks):
        overall = "MIXED"  # known unsupported feature

    return {
        "overall_status": overall,
        "regulation_clock_sec_target": 3600,
        "n_sims": n,
        "seed": seed,
        "config_id": cfg["config_id"],
        "mean_plays_approx": mean_plays,
        "mean_punts": mean_punts,
        "mean_tds": mean_td,
        "mean_kickoffs": mean_ko,
        "p_ot_sample": pct_ot,
        "score_means": {
            "fg_home": float(out["arrays"]["fg_home"].mean()),
            "fg_away": float(out["arrays"]["fg_away"].mean()),
        },
        "sparse_rate": out["evidence_summary"]["sparse_rate"],
        "checks": checks,
        "n_checks_pass": n_pass,
        "n_checks_fail": n_fail,
        "label": "development_in_sample_diagnostic_not_accuracy",
    }
