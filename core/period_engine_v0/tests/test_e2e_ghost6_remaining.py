"""END-TO-END regressions for Ghost6 re-vet remaining HIGH bugs. Written to FAIL first."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
from reconstruct import load_pbp, period_table_from_pbp, as_of_mask
from monte_carlo import simulate_game, raw_probs_from_sim, raw_probs_mc_and_gr
from market import build_mirror, edge_basis_allowed
import demo_jaxbal_report as demo


ROOT = Path(__file__).resolve().parents[1]


def _asof_w9():
    hist = pd.concat([
        period_table_from_pbp(load_pbp(ROOT / "data/play_by_play_2025.parquet")),
        period_table_from_pbp(load_pbp(ROOT / "data/play_by_play_2026.parquet")),
    ], ignore_index=True)
    return hist[as_of_mask(hist, 2026, 9)]


def test_e2e_mc_and_gr_propagates_push_and_decisive():
    asof = _asof_w9()
    out = raw_probs_mc_and_gr(
        asof, "BAL", "JAX", n=4000, seed=1,
        period="h1", market="spread_2way", line=-3.0, side="home",
    )
    assert out.get("p_push") is not None and out["p_push"] > 0
    assert "p_win" in out and "p_lose" in out and "p_win_decisive" in out
    assert abs(out["p_win"] + out["p_push"] + out["p_lose"] - 1.0) < 1e-6
    # unconditional monte_carlo retained
    assert out["monte_carlo"] == out["p_win"]
    # GR branch also carries push fields when implemented
    assert out.get("p_win_decisive_gr") is not None or (out.get("gr_detail") or {}).get("p_win_decisive") is not None


def test_e2e_demo_mirror_uses_decisive_for_two_way_compare_basis():
    """Demo report must expose comparison_basis and not blend on unconditional alone silently."""
    # Run a minimal slice of demo logic
    asof = _asof_w9()
    raw = raw_probs_mc_and_gr(
        asof, "BAL", "JAX", n=3000, seed=2,
        period="h1", market="spread_2way", line=-6.5, side="away",
    )
    # build mirror as demo should: pass decisive for divergence when two-way
    assert raw.get("p_win_decisive") is not None
    m = build_mirror(
        {
            "monte_carlo": raw["monte_carlo"],
            "monte_carlo_decisive": raw["p_win_decisive"],
            "p_win": raw["p_win"],
            "p_push": raw["p_push"],
            "p_lose": raw["p_lose"],
            "bias": "UNIMPLEMENTED",
            "game_randomness": raw["game_randomness"],
        },
        pinnacle_two_way=None,
        consensus_two_ways=[("fanduel_screenshot", -105, -115)],
        consensus_side_index=0,
        consensus_pulled_et="2026-11-05 12:50",
        comparison_basis="decisive_two_way",
    )
    d = m.to_dict()
    assert d.get("comparison_basis") == "decisive_two_way"
    assert "p_push" in d["raw_model_p"] or d["raw_model_p"].get("p_push") == raw["p_push"]


def test_e2e_identity_blocked_suppresses_pin_and_anchor_numbers():
    m = build_mirror(
        {"monte_carlo": 0.55, "monte_carlo_decisive": 0.58},
        pinnacle_two_way=(-110, -110),
        identity_flags=["PERIOD_MISMATCH", "LINE_MISMATCH"],
        proposed_blend_weight=0.3,
        comparison_basis="decisive_two_way",
    )
    assert m.pinnacle_status == "IDENTITY_BLOCKED"
    assert m.pinnacle_novig_p is None  # suppressed — not a usable number
    assert m.market_anchored_p is None
    assert m.market_anchored_status in {"ABSENT", "SUPPRESSED_IDENTITY_BLOCKED"}
    # may keep pin_novig_raw for audit under a clearly named field
    assert getattr(m, "pinnacle_novig_p_raw_blocked", None) is not None or "PIN_VALUE_SUPPRESSED" in m.flags


def test_e2e_fg_joint_coherent_with_regulation():
    asof = _asof_w9()
    sim = simulate_game(asof, "BAL", "JAX", n=15000, seed=7, apply_gr=False)
    A = sim["arrays"]
    qsum_h = A["q1_home"] + A["q2_home"] + A["q3_home"] + A["q4_home"]
    qsum_a = A["q1_away"] + A["q2_away"] + A["q3_away"] + A["q4_away"]
    assert np.array_equal(qsum_h, A["reg_home"])
    assert np.array_equal(qsum_a, A["reg_away"])
    assert np.all(A["fg_home"] >= A["reg_home"]) and np.all(A["fg_away"] >= A["reg_away"])
    # no OT scoring unless regulation tied
    ot_mask = (A["fg_home"] > A["reg_home"]) | (A["fg_away"] > A["reg_away"])
    reg_tie = A["reg_home"] == A["reg_away"]
    assert np.all(~ot_mask | reg_tie)
    # metadata
    assert "settlement_paths" in sim or "outcome_meta" in sim
    meta = sim.get("outcome_meta") or sim.get("settlement_paths")
    assert meta.get("reg_scope") == "regulation_only"
    assert meta.get("fg_scope") == "includes_ot_if_reg_tied"
    # fg < reg must be impossible
    assert float((A["fg_home"] < A["reg_home"]).mean()) == 0.0


def test_e2e_demo_report_json_retains_decisive_fields():
    """After demo run, artifact must retain push/decisive for two-way markets."""
    # invoke main lightly
    from demo_jaxbal_report import main
    main()
    rep = json.loads((ROOT / "artifacts/demo_jaxbal_period_report.json").read_text())
    assert rep.get("outcome_meta", {}).get("fg_scope") == "includes_ot_if_reg_tied"
    assert "league_team_quarter_bootstrap" in (rep.get("source_composition") or "")
    two_way = [m for m in rep["markets"] if "3-way" not in m["market"]]
    assert two_way, "expected two-way markets"
    for m in two_way:
        assert "p_win_decisive" in m["raw"], m["market"]
        assert "p_push" in m["raw"], m["market"]
        assert m["raw"]["monte_carlo"] is not None
        # half-point lines: push mass ~0 but field present
        assert m["mirror"].get("comparison_basis") == "decisive_two_way"
