"""Provenance, ledger double-count guards, situational opportunity tables, market isolation."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config_load import load_config
from pbp_filter import load_team_history
from situational import build_situational_report
from provenance import build_default_registry
from adjustment_ledger import build_ledger

ROOT = Path(__file__).resolve().parents[1]
PBP = ROOT.parent / "period_engine_v0/data/play_by_play_2026.parquet"


def test_situational_has_opportunity_and_conditional():
    hist = load_team_history(PBP, teams=["JAX", "BAL"], season=2026, weeks=(1, 8))
    rep = build_situational_report(hist["df"], hist.get("games_df"))
    assert rep["third_down"]["n_total"] > 0
    for team, row in rep["third_down"]["by_team"].items():
        assert "n_opportunities" in row and "p_convert_given_opportunity" in row
    assert "qb_hit_NOT_measured_pressure_or_blitz" in rep["qb_hit_completion_proxy"]["proxy_label"]
    assert "blitz" in rep["missing_explicit"]
    assert rep["pass_location_not_coverage"]["label"] == "pass_location_NOT_route_or_coverage"
    # JAX vs BAL H2H likely sparse in W1-8
    assert rep["rb_ypc_vs_defense"]["matchup_jax_vs_bal"]["status"] in {"OK", "SPARSE"}


def test_provenance_statuses_not_trust_scores():
    hist = load_team_history(PBP, teams=["JAX", "BAL"], season=2026, weeks=(1, 8))
    rep = build_situational_report(hist["df"])
    rows = build_default_registry(hist_evidence=hist["evidence"], adj_meta={"BAL": {"n_pass_after": 24, "sparse_qb": True}}, situational_ns=rep["ns"])
    assert any(r.status == "MISSING" and r.input_id == "coverage_routes_man_zone" for r in rows)
    assert any(r.status == "PROXY" for r in rows)
    # no numeric trust_score field
    for r in rows:
        assert "trust_score" not in r.to_dict()


def test_ledger_market_not_active_on_data_only():
    cfg = load_config(ROOT / "config/jax_bal_tnf_2026-11-05_data_only.json")
    led = build_ledger(cfg)
    m = [e for e in led if e.group == "market_conditioning"][0]
    assert m.status == "SEPARATE_ONLY"
    assert m.applied_in == "none"
    qb = [e for e in led if e.group == "qb_injury_role"][0]
    assert qb.status == "INACTIVE_DATA_ONLY"


def test_ledger_qb_active_script_adjusted_forbids_double_count():
    cfg = load_config(ROOT / "config/jax_bal_tnf_2026-11-05_script_adjusted.json")
    led = build_ledger(cfg)
    qb = [e for e in led if e.group == "qb_injury_role"][0]
    assert qb.status == "ACTIVE"
    assert "fabricated_fagnano_career" in qb.forbids
    assert "market_implied_qb_downgrade_as_second_hit" in qb.forbids


def test_market_informed_config_isolated():
    m = load_config(ROOT / "config/jax_bal_tnf_2026-11-05_market_informed.json")
    d = load_config(ROOT / "config/jax_bal_tnf_2026-11-05_data_only.json")
    assert m["mode"] == "market_informed" and d["mode"] == "data_only"
    assert m["market_conditioning"]["contaminates_data_only"] is False
    assert m["market_conditioning"]["enabled"] is True
    assert "market_conditioning" not in d
    led = build_ledger(m)
    assert [e for e in led if e.group == "market_conditioning"][0].status == "ACTIVE"


def test_scenario_fagnano_not_verified_probability():
    sc = json.loads((ROOT / "scenarios/bal_upset_fagnano_200_sensitivity.json").read_text())
    assert sc["label"].startswith("SCENARIO_ONLY")
    assert "fabricated_completion_percentage_boost" in sc["forbidden"]
