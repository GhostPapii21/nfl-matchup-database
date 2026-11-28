"""NFL-85: the PHASE_SCRIPT sim_v6 entrypoint is absent and is not another engine.

These tests inspect identity. They do not run a substitute simulation.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from evaluation.sim_v6_authority import (
    BIAS_LABEL,
    DOCUMENTED_COMMAND,
    VERDICT_ABSENT,
    _const_int,
    audit,
)

ROOT = Path(__file__).resolve().parents[2]


def test_semicolon_line_constants_are_read_as_integers():
    packed = "N=100_000; SEED=20261101; SD_MARGIN=13.5; SHRINK_K=30; K_BIAS=30; MIN_N=20\n"
    assert _const_int(packed, "N") == 100_000
    assert _const_int(packed, "SEED") == 20261101
    assert _const_int(packed, "SHRINK_K") == 30
    assert _const_int(packed, "K_BIAS") == 30
    unequal = "N=100_000; SHRINK_K=30; K_BIAS=5\n"
    assert _const_int(unequal, "K_BIAS") == 5
    assert _const_int(unequal, "SHRINK_K") == 30
    assert (_const_int(unequal, "K_BIAS") == _const_int(unequal, "SHRINK_K")) is False
    assert _const_int("", "K_BIAS") is None


def test_each_scratch_file_keeps_its_own_semicolon_constants():
    """A start-of-line regex misses both names and then treats the misses as equal."""
    v6 = (ROOT / "calibration/simv56/engines/cc_sim_v6.py").read_text(encoding="utf-8")
    fix = (ROOT / "calibration/simv56/engines/cc_sim_v6_fix.py").read_text(encoding="utf-8")
    assert _const_int(v6, "SHRINK_K") == 30
    assert _const_int(v6, "K_BIAS") == 30
    assert _const_int(fix, "SHRINK_K") == 30
    assert _const_int(fix, "K_BIAS") == 5
    assert _const_int(fix, "K_BIAS") != _const_int(v6, "K_BIAS")
    report = audit(ROOT)
    scratch = report["systems"]["scratch_cc_sim_v6"]
    fixed = report["systems"]["scratch_cc_sim_v6_fix"]
    assert scratch["shrink_k"] == 30 and scratch["k_bias"] == 30
    assert scratch["k_bias_equals_shrink_k"] is True
    assert scratch["bias_fit_uses_mc_predictions"] is True
    assert fixed["shrink_k"] == 30 and fixed["k_bias"] == 5
    assert fixed["k_bias_equals_shrink_k"] is False
    assert fixed["bias_win"] == 4
    assert fixed["bias_fit_uses_own_predictions"] is True
    assert fixed["is_phase_script_entrypoint"] is False
    assert fixed["promoted"] is False
    assert fixed["sha256_matches_pin"] is True
    assert report["verdict"] == VERDICT_ABSENT
    assert report["calibrated_bias"] == BIAS_LABEL
    assert "cc_sim_v6.py has SHRINK_K=30 and K_BIAS=30" in " ".join(report["blockers"])
    assert "cc_sim_v6_fix.py has SHRINK_K=30 and K_BIAS=5" in " ".join(report["blockers"])


def test_documented_sim_v6_command_is_absent():
    report = audit(ROOT)
    assert report["verdict"] == VERDICT_ABSENT
    assert report["production_integration"] == "BLOCKED"
    assert report["calibrated_bias"] == BIAS_LABEL
    assert report["projection_ready_changed"] is False
    assert report["documented_command"] == DOCUMENTED_COMMAND
    assert report["documented_path_exists"] is False
    assert not (ROOT / "tools" / "sim_v6.py").exists()
    assert report["runtime"]["process_started"] is False
    assert report["runtime"]["benchmark"] is None
    assert report["methods"]["authoritative_implementation"] is None


def test_sim100k_and_simv56_stay_separate_systems():
    report = audit(ROOT)
    sim100k = report["systems"]["pipeline_sim100k"]
    simv56 = report["systems"]["simv56_ensemble"]
    scratch = report["systems"]["scratch_cc_sim_v6"]
    assert sim100k["is_phase_script_entrypoint"] is False
    assert sim100k["trials"] == 100_000
    assert sim100k["engine"] == "core/possession_engine_v0"
    assert sim100k["names_monte_carlo_in_default_engine"] is False
    assert sim100k["names_sim_v6"] is False
    assert simv56["is_phase_script_entrypoint"] is False
    assert simv56["n_trials"] == 20_000
    assert simv56["engines"] == ["sim_v5", "sim_v6", "sim_v6_fix"]
    assert simv56["empty_backtest_calib_is_none"] is True
    assert scratch["is_phase_script_entrypoint"] is False
    assert scratch["scratch_banner"] is True
    assert scratch["declared_n"] == 100_000
    assert scratch["declared_seed"] == 20261101
    assert scratch["shrink_k"] == 30
    assert scratch["k_bias"] == 30
    assert scratch["k_bias_equals_shrink_k"] is True
    assert scratch["missing_calib_multiplier_is_one"] is True
    assert scratch["bias_fit_uses_mc_predictions"] is True
    assert scratch["sha256_matches_pin"] is True
    assert 15 not in scratch["percentile_levels_emitted"]
    assert scratch["scenario_branches_retained"] is False
    assert scratch["edge_averages_three_probabilities"] is True
    assert report["systems"]["other_models"]["explicit_adapter_to_sim_v6"] is None
    assert report["systems"]["other_models"]["lightning"]["exists_in_this_repo"] is False
    assert "season_empirical" in report["systems"]["other_models"]["main_empirical"]["models_named"]


def test_calibrated_bias_has_no_committed_artifact_and_backtest_is_raw():
    report = audit(ROOT)
    evidence = report["calibration_evidence"]
    assert evidence["label"] == "EXPERIMENTAL_UNVALIDATED"
    assert evidence["sim_v6_calib_json_present"] is False
    assert evidence["holdout_or_walk_forward_scorecard"] is None
    backtest = evidence["backtest_csv"]
    assert backtest["rows"] == 1096
    assert list(backtest["weeks"]) == ["4", "5", "6", "7"]
    assert backtest["rows_pred_mc_ne_pred_bias"] > 0


def test_run_gate_cannot_load_and_audit_command_exits_blocked():
    gate = audit(ROOT)["systems"]["run_gate"]
    assert gate["exists"] is True
    assert gate["repo_root_tools_run_gate_exists"] is False
    assert gate["models"] == ["monte_carlo", "bias", "game_randomness"]
    assert gate["imports_rules_rulebook"] is True
    assert gate["rulebook_py_exists"] is False
    proc = subprocess.run(
        [sys.executable, "-m", "evaluation.sim_v6_authority"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 2
    payload = json.loads(proc.stdout)
    assert payload["verdict"] == VERDICT_ABSENT
    assert payload["production_integration"] == "BLOCKED"
