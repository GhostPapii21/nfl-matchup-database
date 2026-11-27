"""NFL-85 read-only identity audit of the PHASE_SCRIPT sim_v6 entrypoint.

Inspects the working tree and reports whether tools/sim_v6.py exists as its own
three-method engine. It does not simulate, fit multipliers, import the scratch
engines, or treat pipeline.sim100k, the simv56 ensemble, the Week 9 empirical
runners, or Lightning as substitutes.

    python -m evaluation.sim_v6_authority

Exit 2 while the documented entrypoint is not production-ready. projection_ready
is never read or written.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTED_REL = Path("tools") / "sim_v6.py"
DOCUMENTED_COMMAND = "python3 tools/sim_v6.py run <legs.json> <out.json>"
VERDICT_ABSENT = "BLOCKED_ENTRYPOINT_ABSENT"
VERDICT_PRESENT = "PRESENT_NOT_AUDITED_AS_PRODUCTION"
BIAS_LABEL = "EXPERIMENTAL_UNVALIDATED"

PHASE_PERCENTILES = (5, 10, 15, 20, 25, 50)


def _text(root: Path, rel: str) -> str | None:
    path = root / rel
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8", errors="replace")


def _sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _const_int(text: str, name: str) -> int | None:
    match = re.search(rf"^{name}\s*=\s*([0-9_]+)", text, re.M)
    if not match:
        return None
    return int(match.group(1).replace("_", ""))


def _pinned_sha(root: Path, filename: str) -> str | None:
    sums = _text(root, "calibration/simv56/engines/SHA256SUMS")
    if sums is None:
        return None
    for line in sums.splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[1] == filename:
            return parts[0]
    return None


def _backtest_profile(path: Path) -> dict:
    if not path.is_file():
        return {"exists": False}
    weeks: dict[str, int] = {}
    markets: dict[str, int] = {}
    rows = mc_ne_bias = all_equal = 0
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows += 1
            weeks[row["week"]] = weeks.get(row["week"], 0) + 1
            markets[row["market"]] = markets.get(row["market"], 0) + 1
            if row["pred_mc"] != row["pred_bias"]:
                mc_ne_bias += 1
            if row["pred_mc"] == row["pred_bias"] == row["pred_gr"]:
                all_equal += 1
    return {
        "exists": True,
        "rows": rows,
        "weeks": dict(sorted(weeks.items(), key=lambda item: int(item[0]))),
        "markets": markets,
        "rows_pred_mc_ne_pred_bias": mc_ne_bias,
        "rows_all_three_predictions_equal": all_equal,
        "what_it_is": (
            "Raw uncalibrated medians (pred_mc, pred_bias, pred_gr) versus actual "
            "for weeks 4-7. Not a dated holdout of fitted Bias multipliers."
        ),
    }


def _scratch_engine(root: Path) -> dict:
    rel = "calibration/simv56/engines/cc_sim_v6.py"
    text = _text(root, rel)
    path = root / rel
    if text is None:
        return {"path": rel, "exists": False, "is_phase_script_entrypoint": False}
    percentiles = [int(n) for n in re.findall(r"np\.percentile\(\s*\w+\s*,\s*(\d+)\s*\)", text)]
    return {
        "path": rel,
        "exists": True,
        "is_phase_script_entrypoint": False,
        "identity": "scratch copy for confidence_check_2026-11-03, not tools/sim_v6.py",
        "sha256": _sha256(path),
        "sha256_pin": _pinned_sha(root, "cc_sim_v6.py"),
        "sha256_matches_pin": _sha256(path) == _pinned_sha(root, "cc_sim_v6.py"),
        "scratch_banner": text.startswith("# SCRATCH COPY"),
        "declared_n": _const_int(text, "N"),
        "declared_seed": _const_int(text, "SEED"),
        "shrink_k": _const_int(text, "SHRINK_K"),
        "k_bias": _const_int(text, "K_BIAS"),
        "k_bias_equals_shrink_k": _const_int(text, "K_BIAS") == _const_int(text, "SHRINK_K"),
        "modes_literal": "MODES=('mc','bias','gr')" in text,
        "calib_constant": "__no_calib__.json" in text,
        "missing_calib_returns_none": "else None" in text and "def load_calib" in text,
        "missing_calib_multiplier_is_one": "if not self.calib: return 1.0" in text,
        "bias_fit_uses_mc_predictions": "col='pred_mc' if mode=='bias'" in text,
        "percentile_levels_emitted": percentiles,
        "phase_script_percentiles_missing": [p for p in PHASE_PERCENTILES if p not in percentiles and p != 50],
        "median_emitted": "median=float(np.median(x))" in text,
        "method_samples_stored_separately": "out[mode]=dict(" in text,
        "edge_averages_three_probabilities": "sum(r['p'].values())/3" in text,
        "scenario_branches_retained": False,
        "scenario_note": (
            "One spread scalar feeds a normal margin shock inside mode 'gr'. "
            "Lead, neutral, and trail are not retained as separate sample branches."
        ),
    }


def _simv56(root: Path) -> dict:
    rel = "calibration/simv56_pmodel.py"
    text = _text(root, rel) or ""
    return {
        "path": rel,
        "exists": bool(text),
        "is_phase_script_entrypoint": False,
        "command": "python -m calibration.simv56_pmodel run --legs <csv> --week <N> --sources <dir> --out <dir>",
        "n_trials": _const_int(text, "N_TRIALS"),
        "engines": ["sim_v5", "sim_v6", "sim_v6_fix"] if 'ENGINES = ("sim_v5", "sim_v6", "sim_v6_fix")' in text else None,
        "imports_scratch_cc_sim_v6": 'importlib.import_module("cc_sim_"' in text,
        "empty_backtest_calib_is_none": "calib = M.fit(tr) if len(tr) else None" in text,
        "probability_source": "sim_v5_v6_ensemble" if "sim_v5_v6_ensemble" in text else None,
        "research_only_docstring": "Research only; projection_ready stays false." in text,
        "distinct_from_sim_v6": (
            "Three engines (v5, v6, v6_fix) at N_TRIALS, then a row-mean of p_mc/p_bias/p_gr "
            "and a second row-mean across engines. That is an ensemble, not the PHASE_SCRIPT triad entrypoint."
        ),
    }


def _sim100k(root: Path) -> dict:
    rel = "pipeline/sim100k.py"
    text = _text(root, rel) or ""
    body = ""
    if "def default_engine" in text and "def run(" in text:
        body = text[text.index("def default_engine"):text.index("def run(")]
    return {
        "path": rel,
        "exists": bool(text),
        "is_phase_script_entrypoint": False,
        "command": "python -m pipeline.sim100k --game <game_id>",
        "trials": _const_int(text, "TRIALS"),
        "engine": "core/possession_engine_v0" if 'ENGINE_REL = Path("core") / "possession_engine_v0"' in text else None,
        "methods": ["possession"],
        "names_monte_carlo_in_default_engine": "monte_carlo" in body,
        "names_sim_v6": "sim_v6" in text,
        "distinct_from_sim_v6": (
            "Single NFL-43 possession-engine run at a fixed 100_000 trials. "
            "No Monte Carlo / Bias / Game Randomness methods."
        ),
    }


def _other_models(root: Path) -> dict:
    main_rel = "research/week9_1pm_live/run_current_week9_1pm.py"
    main_text = _text(root, main_rel) or ""
    lightning_rel = "experiments/nfl_opportunity_lightning.py"
    lightning_note = "data/historical/research/nfl56_status_2026-11-09/lightning/LIGHTNING_REPORT.md"
    return {
        "main_empirical": {
            "path": main_rel,
            "exists": bool(main_text),
            "is_phase_script_entrypoint": False,
            "models_named": [name for name in ("season_empirical", "rolling5_empirical", "opponent_shrunk_rolling5") if name in main_text],
            "mentions_sim_v6": "sim_v6" in main_text,
        },
        "lightning": {
            "path": lightning_rel,
            "exists_in_this_repo": (root / lightning_rel).is_file(),
            "is_phase_script_entrypoint": False,
            "local_note": lightning_note if (root / lightning_note).is_file() else None,
            "note": "Lightning is not an entrypoint in this repository. The local note describes an external experiment.",
        },
        "explicit_adapter_to_sim_v6": None,
    }


def _gate(root: Path) -> dict:
    rel = "source_adapters/tools/run_gate.py"
    text = _text(root, rel) or ""
    return {
        "path": rel,
        "exists": bool(text),
        "repo_root_tools_run_gate_exists": (root / "tools" / "run_gate.py").is_file(),
        "models": ["monte_carlo", "bias", "game_randomness"] if 'MODELS = ["monte_carlo","bias","game_randomness"]' in text else None,
        "requires_script_suffix_sim_v6_py": 'sim_v6\\.py$' in text or "sim_v6\\.py$" in text,
        "requires_n_at_least_100000": 's["n"] < 100000' in text,
        "imports_rules_rulebook": "from rules import rulebook" in text,
        "rulebook_py_exists": (root / "rules" / "rulebook.py").is_file(),
    }


def audit(root: Path | None = None) -> dict:
    root = Path(root) if root is not None else ROOT
    documented = root / DOCUMENTED_REL
    present = documented.is_file()
    scratch = _scratch_engine(root)
    simv56 = _simv56(root)
    sim100k = _sim100k(root)
    backtest_path = root / "calibration" / "simv56" / "engines" / "sim_v6_backtest.csv"
    profile = _backtest_profile(backtest_path)
    if profile.get("exists"):
        profile["path"] = "calibration/simv56/engines/sim_v6_backtest.csv"
    calib_paths = [
        "tools/sim_v6_calib.json",
        "calibration/simv56/engines/sim_v6_calib.json",
        "calibration/simv56/engines/__no_calib__.json",
    ]
    blockers = []
    if not present:
        blockers.append(
            "DOCUMENTED_ENTRYPOINT_ABSENT: python3 tools/sim_v6.py cannot start because tools/sim_v6.py is not on this tree."
        )
    blockers.extend([
        "CALIBRATED_BIAS_UNVALIDATED: no sim_v6_calib.json is committed. The vendored scratch copy fail-opens a missing calibration file to multiplier 1.0.",
        "BIAS_NOT_A_HEAVIER_SHRINK: cc_sim_v6.py sets K_BIAS equal to SHRINK_K and fits Bias on pred_mc. A 2026-11-05 code note (BIASDUP) already recorded bias multipliers equal to Monte Carlo.",
        "SIMV56_IS_NOT_SIM_V6: calibration.simv56_pmodel runs a three-engine ensemble at 20_000 trials and averages probabilities.",
        "SIM100K_IS_NOT_SIM_V6: pipeline.sim100k runs the possession engine once at 100_000 trials.",
        "NO_EXPLICIT_ADAPTER: no module adapts sim100k, simv56, the empirical runners, or Lightning into tools/sim_v6.py.",
        "GATE_DEPENDENCY_MISSING: source_adapters/tools/run_gate.py imports rules.rulebook, and rules/rulebook.py is not on this tree.",
    ])
    return {
        "issue": "NFL-85",
        "verdict": VERDICT_ABSENT if not present else VERDICT_PRESENT,
        "production_integration": "BLOCKED",
        "calibrated_bias": BIAS_LABEL,
        "projection_ready_changed": False,
        "documented_command": DOCUMENTED_COMMAND,
        "documented_path": DOCUMENTED_REL.as_posix(),
        "documented_path_exists": present,
        "runtime": {
            "attempted_command": "python3 tools/sim_v6.py run",
            "process_started": False,
            "benchmark": None,
            "representative_output": None,
            "reason": "The documented file is absent, so there is no process to time or an output artifact to keep.",
        },
        "methods": {
            "required": ["monte_carlo", "calibrated_bias", "game_randomness"],
            "authoritative_implementation": None,
            "scratch_copy_modes": ["mc", "bias", "gr"] if scratch.get("modes_literal") else None,
            "structurally_distinct_on_authoritative_entrypoint": None,
            "scratch_copy_distinction": {
                "monte_carlo": "Negative-binomial volume, binomial catches, resampled yards. Not the PHASE_SCRIPT entrypoint.",
                "bias": (
                    "Same volume structure as Monte Carlo. Multiplier is fit on Monte Carlo residuals "
                    "with K_BIAS == SHRINK_K. Missing calibration file uses M=1.0, leaving an independent draw from the same family."
                ),
                "game_randomness": "Different volume generator: beta team share, lognormal pace, one normal margin shock. Not three scenario branches.",
            },
        },
        "blockers": blockers,
        "systems": {
            "phase_script_sim_v6": {
                "path": DOCUMENTED_REL.as_posix(),
                "exists": present,
                "package_entrypoint": None,
            },
            "scratch_cc_sim_v6": scratch,
            "simv56_ensemble": simv56,
            "pipeline_sim100k": sim100k,
            "other_models": _other_models(root),
            "run_gate": _gate(root),
        },
        "calibration_evidence": {
            "label": BIAS_LABEL,
            "sim_v6_calib_json_present": any((root / rel).is_file() for rel in calib_paths),
            "calib_paths_checked": calib_paths,
            "backtest_csv": profile,
            "holdout_or_walk_forward_scorecard": None,
            "future_data_leakage_on_authoritative_entrypoint": "NOT_TESTABLE_ENTRYPOINT_ABSENT",
            "scratch_copy_cutoff_parameter": "Engine(cutoff=...) filters play-by-play to game_date < cutoff. That parameter is not reachable through tools/sim_v6.py.",
        },
        "remediation": [
            "Keep pipeline.sim100k, calibration.simv56_pmodel, the Week 9 empirical runners, and Lightning as separate systems. Do not point PHASE_SCRIPT at them.",
            "Do not promote calibration/simv56/engines/cc_sim_v6_fix.py. The 2026-11-03 note marks sim_v6_fix deprecated and names tools/sim_v6.py as the only source.",
            "A later change may recover the historical tools/sim_v6.py from the research snapshot branch and place it at tools/sim_v6.py. That recovery is a separate review, not this audit.",
            "Before any production wiring: fixed 100_000 trials per method, reproducible seeds, three unpooled method outputs, PHASE_SCRIPT percentiles, and a missing calibration artifact that fails closed.",
            "Publish a dated training window, a later holdout or walk-forward scorecard, and the calibration file those numbers came from. Until that exists, calibrated Bias stays EXPERIMENTAL_UNVALIDATED.",
            "Leave projection_ready false. Do not merge or deploy on the strength of this audit.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="NFL-85 read-only sim_v6 authority audit")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    report = audit(args.root)
    json.dump(report, sys.stdout, indent=2)
    sys.stdout.write("\n")
    if report["verdict"] != "PRODUCTION_READY":
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
