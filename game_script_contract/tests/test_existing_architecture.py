"""READ-ONLY audit of the existing architecture against the game-script contract.

These tests import or parse existing modules and committed artifacts; they change nothing. A test marked
xfail(strict=True) records a VERIFIED gap ("AUDIT FINDING"): it fails today, so the suite stays green, and it turns into
an XPASS failure the day the gap is closed, forcing the marker (and docs/audits/game_script_integrity_audit.md) to be
updated. Details and line references: docs/audits/game_script_integrity_audit.md.
"""
from __future__ import annotations

import ast
import glob
import json
from pathlib import Path

import numpy as np
import pytest

from game_script_contract.allocation import errors, validate_payload
from game_script_contract.partition import partition_score_arrays
from game_script_contract.schema import BRANCH_IDS

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "docs/audits/game_script_integrity_audit.md"


def src(rel: str) -> str:
    return (ROOT / rel).read_text()


def func_source(rel: str, name: str, cls: str | None = None) -> str:
    text = src(rel)
    tree = ast.parse(text)
    scope = tree.body
    if cls:
        scope = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == cls).body
    node = next(n for n in scope if isinstance(n, ast.FunctionDef) and n.name == name)
    return ast.get_source_segment(text, node)


def finding(msg: str):
    return pytest.mark.xfail(strict=True, raises=AssertionError, reason=f"AUDIT FINDING: {msg}")


# ------------------------------------------------------------------------------------------------- sim_v6 absence
def test_sim_v6_is_referenced_but_absent_and_documented():
    if (ROOT / "tools/sim_v6.py").exists():
        pytest.skip("tools/sim_v6.py now exists: re-run the game-script audit against it")
    assert "sim_v6.py" in src("source_adapters/tools/run_gate.py")
    assert "tools/sim_v6.py" in src("workflows/operational_specs/PHASE_SCRIPT.md")
    assert "SCRATCH COPY" in src("calibration/simv56/engines/cc_sim_v6.py").splitlines()[0]
    assert "tools/sim_v6.py" in REPORT.read_text() and "absent" in REPORT.read_text()


# ------------------------------------------------------------------------- what the architecture CAN carry (passes)
def test_joint_producer_context_exposes_score_margin_and_range_conditions():
    body = func_source("core/possession_engine_v0/joint_producer.py", "context", cls="OpportunityModel")
    assert '"score_margin"' in body
    m = func_source("core/possession_engine_v0/joint_producer.py", "matches")
    assert '_min' in m and '_max' in m        # usage cells can condition on score_margin ranges


def test_joint_producer_keeps_every_trial():
    body = func_source("core/possession_engine_v0/joint_producer.py", "write_forecast")
    assert "trials.jsonl" in body


def test_sim100k_keeps_per_trial_player_lines_and_scores():
    body = func_source("pipeline/sim100k.py", "default_engine")
    assert '"player_box_trials"' in body
    npz = sorted(glob.glob(str(ROOT / "snapshots/*/*/sim_arrays.npz")))
    assert npz, "no committed per-trial arrays"
    z = np.load(npz[-1])
    assert {"fg_home", "fg_away", "q1_home", "q4_away", "reg_home"} <= set(z.files)
    assert len(z["fg_home"]) == 100_000


def test_committed_engine_trials_can_be_partitioned_into_a_valid_three_branch_payload():
    """Derivability check: real committed per-trial scores -> branch payload that satisfies the contract.
    Favorite = the side the engine itself makes the favorite (mean margin); labelled as such, not a market read."""
    path = sorted(glob.glob(str(ROOT / "snapshots/2026_11_CIN_WAS/*/sim_arrays.npz")))[-1]
    z = dict(np.load(path))
    home_fav = (z["fg_home"].astype(float) - z["fg_away"]).mean() > 0
    p = partition_score_arrays(z, game_id="2026_11_CIN_WAS", home="WAS", away="CIN",
                               favorite="WAS" if home_fav else "CIN", favorite_source="engine_mean_margin",
                               definition={"classifier_variable": "final_margin_favorite",
                                           "favorite_controls_min_margin": 9, "underdog_chases_max_margin": -9},
                               source_engine="core/possession_engine_v0 (committed snapshot)",
                               source_ref=str(Path(path).relative_to(ROOT)), limit=5000)
    f = validate_payload(p)
    assert errors(f) == [], [str(x) for x in errors(f)]
    assert abs(sum(p["branches"][b]["probability"] for b in BRANCH_IDS) - 1) < 1e-9
    status = {d: v["status"] for d, v in p["branches"]["competitive"]["dimension_status"].items()}
    assert status["score_distribution"] == "derived" and status["pass_run"] == "not_modeled"


# -------------------------------------------------------------------------------------- verified gaps (strict xfail)
@finding("possession engine play selection (PlayCatalog.sample_snap) keys on team/down/distance/field position only; "
         "score margin and clock never enter, so branches cannot change play calling")
def test_possession_engine_play_selection_conditions_on_game_state():
    body = func_source("core/possession_engine_v0/simulate.py", "sample_snap", cls="PlayCatalog")
    assert "score" in body or "game_seconds_remaining" in body


@finding("fitted usage cells are conditioned on team and down only; fit_prospective_usage.py says score/period are "
         "'deliberately unconditioned', so joint_producer's score_margin hook is never used")
def test_fitted_usage_cells_condition_on_score_margin():
    keys = set()
    for f in glob.glob(str(ROOT / "core/possession_engine_v0/runs/**/model.json"), recursive=True):
        for c in json.loads(Path(f).read_text()).get("usage_cells", []):
            keys |= set(c.get("when", {}))
    assert any(k.startswith("score_margin") for k in keys), sorted(keys)


@finding("committed 100k engine runs show Q4 margin ~independent of the margin after Q3 (corr ~ -0.01..-0.04) vs "
         "real NFL 2022 regular season (~ -0.23): no game-state response in the trials")
def test_engine_q4_scoring_responds_to_game_state_like_real_games():
    import pandas as pd
    pbp = pd.read_parquet(ROOT / "data/historical/nflverse/pbp_2022.parquet",
                          columns=["game_id", "season_type", "qtr", "total_home_score", "total_away_score", "play_id"])
    pbp = pbp[pbp.season_type == "REG"].sort_values(["game_id", "play_id"])
    q3 = pbp[pbp.qtr <= 3].groupby("game_id")[["total_home_score", "total_away_score"]].last()
    q4 = pbp[pbp.qtr <= 4].groupby("game_id")[["total_home_score", "total_away_score"]].last()
    m3 = q3.total_home_score - q3.total_away_score
    m4 = (q4.total_home_score - q4.total_away_score).loc[m3.index] - m3
    real = float(np.corrcoef(m3, m4)[0, 1])
    assert real < -0.1, real
    sims = []
    for f in sorted(glob.glob(str(ROOT / "snapshots/*/*/sim_arrays.npz"))):
        z = np.load(f)
        s3 = sum(z[f"q{i}_home"].astype(float) - z[f"q{i}_away"] for i in (1, 2, 3))
        sims.append(float(np.corrcoef(s3, z["q4_home"].astype(float) - z["q4_away"])[0, 1]))
    assert np.median(sims) <= 0.5 * real, (np.median(sims), real)


@finding("snapshots/lock.summarize collapses all trials into one summary (means, pooled percentiles); no branch blocks")
def test_engine_summary_emits_three_branch_blocks():
    import sys
    sys.path.insert(0, str(ROOT))
    from snapshots import lock
    n = 1000
    rng = np.random.default_rng(0)
    arrays = {k: rng.integers(0, 14, n) for k in ("fg_home", "fg_away", "h1_home", "h1_away", "h2_home", "h2_away",
                                                  "q1_home", "q1_away", "q2_home", "q2_away", "q3_home", "q3_away",
                                                  "q4_home", "q4_away")}
    arrays["went_ot"] = np.zeros(n, bool)
    s = lock.summarize(arrays, {}, "HOME", "AWAY", "Home", "Away")
    assert all(b in json.dumps(s) for b in BRANCH_IDS)


@finding("dashboard/opportunity.py turns the spread into ONE deterministic pass/rush multiplier (script_multipliers) "
         "before simulating player volume, i.e. the script is collapsed to its expectation before props are priced")
def test_board_prices_player_volume_per_branch():
    import sys
    sys.path.insert(0, str(ROOT))
    from dashboard import opportunity
    out = opportunity.script_multipliers(7.0)
    assert isinstance(out, dict) and set(out) == set(BRANCH_IDS), out


@finding("research/runs/2026-11-12_TNF_WAS_NYG_layers/script_layer.py averages scenario scores by weight (W) and "
         "prices markets from normal(pooled mean) - pooling before pricing")
def test_script_layer_prices_from_branch_distributions():
    text = src("research/runs/2026-11-12_TNF_WAS_NYG_layers/script_layer.py")
    pooled = "W=lambda i: sum(v[0]*v[i] for v in S.values())" in text and "norm.cdf(1.5, m, SDm)" in text
    assert not pooled


def test_script_layer_pooling_changes_the_price():
    """Quantifies the finding with the script's OWN analyst inputs (weights, scores, SDm): mixture vs pooled normal."""
    import math

    class norm:  # scipy is not in requirements-test.txt; normal CDF via erf
        @staticmethod
        def cdf(x, mu, sd):
            return 0.5 * (1 + math.erf((x - mu) / (sd * math.sqrt(2))))
    tree = ast.parse(src("research/runs/2026-11-12_TNF_WAS_NYG_layers/script_layer.py"))
    S = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
             and getattr(n.targets[0], "id", None) == "S")
    sd = 13.5
    pooled_m = sum(w * (a - b) for w, a, b, *_ in S.values())
    pooled = 1 - norm.cdf(2.5, pooled_m, sd)
    mixture = sum(w * (1 - norm.cdf(2.5, a - b, sd)) for w, a, b, *_ in S.values())
    assert abs(sum(w for w, *_ in S.values()) - 1) < 1e-12
    assert abs(mixture - pooled) > 0.002, (mixture, pooled)


@finding("research/third_down/mnf_week9_route_opportunity_scenarios.py has four named scenarios with no "
         "probabilities (by design: 'NO fitted probabilities'); they cannot be allocated to 100%")
def test_mnf_route_scenarios_carry_branch_probabilities():
    tree = ast.parse(src("research/third_down/mnf_week9_route_opportunity_scenarios.py"))
    node = next(n for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "SCENARIOS")
    names = [k.value for k in node.value.keys]
    assert len(names) == 3 and "probability" in ast.get_source_segment(src(
        "research/third_down/mnf_week9_route_opportunity_scenarios.py"), node)


@finding("calibration/simv56/engines/cc_sim_v6.py (vendored sim_v6 copy) draws a continuous margin per trial in its "
         "'gr' mode only and returns pooled mean/median/p10/p90/rungs per mode; no branch-separated output")
def test_simv56_engine_returns_branch_separated_rungs():
    text = src("calibration/simv56/engines/cc_sim_v6.py")
    assert any(b in text for b in BRANCH_IDS)
