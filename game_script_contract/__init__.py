"""Game-script scenario contract (research only).

Three independent branches per game -- favorite_controls, competitive, underdog_chases -- with their own
distributions for every dimension, a probability-allocation contract (branch probabilities total 100%), and detectors
for branch pooling and duplicated scenario outputs. This package is a CONTRACT and VALIDATOR only: it is not a
simulation engine, it does not touch model weights, projections or betting-readiness controls, and nothing in the
existing engines imports it. See docs/specs/game_script_probability_contract.md and
docs/audits/game_script_integrity_audit.md.
"""
from .schema import (  # noqa: F401
    BRANCH_IDS, DEFAULT_BRANCH_DEFINITION, DIMENSIONS, SCHEMA_PATH, SCHEMA_VERSION,
)
from .allocation import (  # noqa: F401
    ContractError, Finding, TOLERANCE, check_prop_probability, classify_trial, classify_trials,
    detect_branch_pooling, detect_duplicate_branches, prop_probability, validate_allocation,
    validate_payload,
)
