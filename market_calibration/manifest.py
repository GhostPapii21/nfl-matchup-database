"""Fail closed on result claims this implementation cannot support."""
import json
from pathlib import Path

from .calibration import UNFITTED
from .joint_trial_adapter import contract_info


def validate_manifest(manifest, root):
    contract = contract_info()
    expected = {"calibration": UNFITTED, "anchored": "PENDING_VALIDATION",
                "validation": "NO_UNTOUCHED_HOLDOUT_VALIDATION", "quotes": "SAVED_ONLY",
                "adapter": contract["status"]}
    for section, status in expected.items():
        if manifest.get(section, {}).get("status") != status:
            raise ValueError(f"unsupported {section} result claim")
    if manifest.get("implementation_status") != "IMPLEMENTED_UNIT_TESTED_RESEARCH_ONLY":
        raise ValueError("unsupported implementation claim")
    # These declarations also describe results; a correct section status must
    # not mask contradictory actionable, source, or producer claims.
    declarations = {
        "quotes": {"network": False, "actionable_status": "NOLINE",
                   "identity_namespace": "SOURCE_EVENT_ALIAS_UNMAPPED",
                   "canonical_crosswalk": "ABSENT_NO_CANONICAL_JOIN_CLAIM",
                   "rule_compatibility": "UNVERIFIED_RESEARCH_PAIRING_ONLY",
                   "pinnacle_q2_q3_q4_spreads": "NOLINE"},
        "adapter": {"producer_simulations": "NOT_RUN", "player_targets": "NOT_DEFINED"},
        "raw_outputs": {"status": "NO_RAW_MODEL_OUTPUT_PROVIDED"},
    }
    for section, fields in declarations.items():
        for key, value in fields.items():
            actual = manifest.get(section, {}).get(key)
            if actual != value or type(actual) is not type(value):
                raise ValueError(f"unsupported {section}.{key} result claim")
    if manifest["calibration"].get("coefficients") is not None or manifest["calibration"].get("fitted") is not False:
        raise ValueError("no fitted calibration exists")
    if manifest["anchored"].get("edge_eligible") is not False or manifest["anchored"].get("predictions_provided") is not False:
        raise ValueError("pending empty anchor cannot be edge eligible or claim predictions")
    if manifest["adapter"].get("contract_sha256") != contract["sha256"]:
        raise ValueError("adapter contract digest mismatch")
    if manifest["adapter"].get("full_core_acceptance") != "NOT_RUN":
        raise ValueError("full core acceptance was not run")
    if manifest["validation"].get("model_performance_claim") != "NONE":
        raise ValueError("model performance not validated")
    policy = manifest.get("data_policy", {})
    if policy.get("weeks_1_8_2026") != "development_inspected" or policy.get("tnf_jax_bal") != "development_inspected":
        raise ValueError("inspected data must not be untouched holdout")
    if policy.get("fit_on_holdout") != "FORBIDDEN":
        raise ValueError("holdout fit must be forbidden")
    if manifest.get("scoring_labels") != ["baseline", "hindsight"]:
        raise ValueError("baseline and hindsight must remain separately labelled")
    artifacts = manifest.get("artifacts", [])
    required = {"artifacts/raw_model_outputs.json", "artifacts/market_anchored_outputs.json"}
    if not required <= set(artifacts):
        raise ValueError("manifest must separately enumerate raw and anchored artifacts")
    root = Path(root).resolve()
    for path in artifacts:
        target = (root / path).resolve()
        if not target.is_relative_to(root) or not target.is_file():
            raise ValueError(f"missing or out-of-scope artifact: {path}")
    raw = json.loads((root / "artifacts/raw_model_outputs.json").read_text())
    anchored = json.loads((root / "artifacts/market_anchored_outputs.json").read_text())
    if raw.get("status") != "NO_RAW_MODEL_OUTPUT_PROVIDED" or raw.get("prediction_family") != "RAW" or raw.get("predictions") != []:
        raise ValueError("raw artifact must honestly report no supplied model run")
    if (anchored.get("status") != "PENDING_VALIDATION" or anchored.get("prediction_family") != "MARKET_ANCHORED"
            or anchored.get("edge_eligible") is not False or anchored.get("predictions") != []
            or anchored.get("coefficients") is not None):
        raise ValueError("anchored artifact falsely claims usable results")
    return True
