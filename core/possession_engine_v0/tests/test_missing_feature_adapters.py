import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from effects.missing_feature_adapters import GATES, FeatureGate


def test_missing_pressure_rejects_fitted_claim():
    g = [x for x in GATES if x.feature_id == "true_pressure_qbp"][0]
    r = g.accept_scenario({"label": "SCENARIO_test", "claim_fitted": True})
    assert r["accepted"] is False


def test_scenario_accepted_but_not_sim_effect():
    g = [x for x in GATES if x.feature_id == "man_zone_mofo"][0]
    r = g.accept_scenario({"label": "SCENARIO_parent_chart"})
    assert r["accepted"] is True and r["mode"] == "scenario_only" and r["applies_to_sim"] is False
