"""Frozen local inputs for the opportunity-first producer. No data acquisition."""
from __future__ import annotations

import copy
import hashlib
import json
import platform
import re
import subprocess
from datetime import datetime
from pathlib import Path

import numpy as np

CONTRACT_VERSION = "1.0.0"
SERIALIZER = "python-json-sorted-compact-utf8-v1"
SEED_VERSION = "sha256-game-index-common-random-v2"
COMPONENT_VERSION = "opportunity-first-v1"


def canonical(value) -> bytes:
    """Wire numbers are integers; fractional model weights use JSON finite floats."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")


def digest(value) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def byte_digest(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def utc(value: str) -> datetime:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z", value):
        raise ValueError("UTC instant must be explicit RFC3339 ending in Z")
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def integer(value, name, minimum=None):
    if type(value) is not int or (minimum is not None and value < minimum):
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def safe_path(root: Path, relative: str) -> Path:
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts or "market_calibration" in rel.parts:
        raise ValueError("input/output paths must be logical relative paths outside excluded trees")
    resolved = (root / rel).resolve()
    if not resolved.is_relative_to(root.resolve()) or "market_calibration" in resolved.parts or "wt-market-calibration" in resolved.parts:
        raise ValueError("path escapes root or enters excluded tree")
    return resolved


def validate_splits(splits: dict, game: dict) -> str:
    for key in ("split_manifest_id", "policy_version", "created_at_utc", "status"):
        if not splits.get(key):
            raise ValueError(f"split manifest missing {key}")
    utc(splits["created_at_utc"])
    names = ("train", "dev", "holdout")
    if splits["status"] == "UNASSIGNED":
        if any(splits.get(f"{name}_game_ids") is not None for name in names):
            raise ValueError("UNASSIGNED splits require null ID lists")
        return "UNASSIGNED"
    if splits["status"] != "FROZEN" or not splits.get("frozen_before_selection"):
        raise ValueError("split membership must be frozen before selection")
    seen = set()
    membership = "UNASSIGNED"
    inspected = {(r["namespace"], r["game_id"]) for r in splits.get("inspected_game_ids", [])}
    for name in names:
        rows = splits[f"{name}_game_ids"]
        for row in rows:
            key = (row["namespace"], row["game_id"])
            if key in seen:
                raise ValueError("split game IDs must be disjoint including duplicates")
            seen.add(key)
            if name == "holdout" and (key in inspected or key in {
                (r["namespace"], r["game_id"]) for r in splits.get("evidence_only_game_ids", [])
            }):
                raise ValueError("inspected/evidence game cannot be untouched holdout")
            if key == (game["game_id_namespace"], game["game_id"]):
                membership = name
    return membership


def source_files(package):
    """Generated replay snapshots are artifacts, never executable source inputs."""
    return [p for p in sorted(package.rglob("*.py"))
            if not {"tests", "runs", "artifacts", "__pycache__"}.intersection(p.relative_to(package).parts)]


def engine_identity() -> dict:
    package = Path(__file__).resolve().parent
    # Path-limited git commands never inspect the excluded calibration trees.
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=package, text=True).strip()
    patch = subprocess.check_output(["git", "diff", "HEAD", "--", "research/possession_engine_v0"],
                                    cwd=package.parents[1])
    source = {p.relative_to(package).as_posix(): byte_digest(p.read_bytes())
              for p in source_files(package)}
    return {"engine_version": head, "component_version": COMPONENT_VERSION,
            "source_content_hash": digest(source),
            "dirty_patch_hash": digest({"tracked_diff_sha256": byte_digest(patch), "source_file_hashes": source}),
            "dependencies": {"python": platform.python_version(), "numpy": np.__version__}}


def freeze_run(spec: dict, input_root: str | Path, inputs: list[dict], *, n: int, seed: int) -> dict:
    """Load exact file bytes once; reject unverified as-of and independent/market mixing.

    Inputs require logical_input_id, path, source, selected_record_ids, schema_version,
    usage, source_event_time_utc, available_at_utc, retrieved_at_utc, asof_evidence_ref.
    Three logical IDs are required: registry, model, splits. No mutable external reads
    are performed during simulation.
    """
    spec = copy.deepcopy(spec)
    integer(n, "n", 1)
    integer(seed, "seed", 0)
    integer(spec.get("trial_start", 0), "trial_start", 0)
    cutoff = utc(spec["cutoff_utc"])
    if utc(spec["frozen_at_utc"]) < cutoff or utc(spec["generated_at_utc"]) < utc(spec["frozen_at_utc"]):
        raise ValueError("freeze/generation timestamps are out of order")
    if spec["mode"] not in {"data_only", "script_adjusted", "market_informed"}:
        raise ValueError("unknown mode")
    if not spec.get("config_id"):
        raise ValueError("config_id required")
    game = spec["game"]
    for key in ("game_id", "game_id_namespace", "season", "season_type", "week",
                "home_team_id", "away_team_id", "team_id_namespace", "kickoff_utc", "crosswalk_ref"):
        if game.get(key) is None or game[key] == "":
            raise ValueError(f"canonical game missing {key}; shared export blocked")
    for key in ("game_id", "game_id_namespace", "home_team_id", "away_team_id", "team_id_namespace"):
        if not isinstance(game[key], str) or not game[key]:
            raise ValueError("canonical IDs/namespaces must preserve source strings")
    integer(game["season"], "season", 1)
    integer(game["week"], "week", 1)
    if game["home_team_id"] == game["away_team_id"] or cutoff >= utc(game["kickoff_utc"]):
        raise ValueError("invalid teams or non-pregame cutoff")
    entries, loaded, blobs = [], {}, {}
    root = Path(input_root).resolve()
    if "market_calibration" in root.parts or "wt-market-calibration" in root.parts:
        raise ValueError("excluded input root")
    for item in sorted(inputs, key=lambda row: row["logical_input_id"]):
        item = copy.deepcopy(item)
        key = item["logical_input_id"]
        if key in loaded:
            raise ValueError("duplicate logical input ID")
        for required in ("source", "selected_record_ids", "schema_version", "usage", "asof_evidence_ref"):
            if item.get(required) is None or item[required] == "":
                raise ValueError(f"input {key} missing {required}: ASOF_UNVERIFIED")
        if item["usage"] not in {"PREDICTIVE", "SCENARIO", "MARKET"}:
            raise ValueError("postgame/evidence-only input cannot enter predictive manifest")
        if item["usage"] == "MARKET" and spec["mode"] != "market_informed":
            raise ValueError("market input forbidden in independent mode")
        for clock in ("source_event_time_utc", "available_at_utc", "retrieved_at_utc"):
            utc(item[clock])
        if utc(item["source_event_time_utc"]) > utc(item["available_at_utc"]):
            raise ValueError("publication before source event")
        if utc(item["available_at_utc"]) > cutoff:
            raise ValueError("post-cutoff input blocked")
        if utc(item["retrieved_at_utc"]) > utc(spec["frozen_at_utc"]):
            raise ValueError("retrieval after freeze")
        if utc(item["retrieved_at_utc"]) < utc(item["available_at_utc"]):
            raise ValueError("retrieval precedes source availability")
        # Late extraction is allowed only with explicit verifiable as-of evidence.
        if utc(item["retrieved_at_utc"]) > cutoff and item.get("asof_verified") is not True:
            raise ValueError("ASOF_UNVERIFIED: later retrieval requires verified as-of contents")
        data = safe_path(root, item["path"]).read_bytes()
        loaded[key] = json.loads(data)
        blobs[key] = data
        entries.append({**item, "byte_size": len(data), "sha256": byte_digest(data),
                        "normalized_timestamps": {k: item[k] for k in (
                            "source_event_time_utc", "available_at_utc", "retrieved_at_utc")}})
    if not {"registry", "model", "splits"} <= loaded.keys():
        raise ValueError("registry/model/splits frozen files required")
    registry = loaded["registry"]
    if (registry["game"] != game or not registry.get("evidence_refs") or not registry.get("alias_map_version")
            or not registry.get("team_alias_map")):
        raise ValueError("canonical game registry/crosswalk evidence missing or mismatched")
    roster = registry["players"]
    identities = set()
    for row in roster:
        if row["team_id"] not in {game["home_team_id"], game["away_team_id"]}:
            raise ValueError("roster team mismatch")
        if row.get("player_id") is not None:
            key = (row["player_id_namespace"], row["player_id"])
            if not all(isinstance(part, str) and part for part in key) or key in identities or not row.get("evidence_ref"):
                raise ValueError("ambiguous/unevidenced player identity")
            identities.add(key)
        elif row.get("identity_status") != "UNRESOLVED":
            raise ValueError("null player identity requires UNRESOLVED status")
    aliases = set()
    for row in registry["crosswalk"]:
        key = (row["entity"], row["source_namespace"], row["source_id"])
        if key in aliases or not row.get("evidence_ref"):
            raise ValueError("ambiguous/unevidenced crosswalk")
        aliases.add(key)
        if row["entity"] == "player" and (row["canonical_namespace"], row["canonical_id"]) not in identities:
            raise ValueError("crosswalk player absent from frozen roster")
    membership = validate_splits(loaded["splits"], game)
    if utc(loaded["splits"]["created_at_utc"]) > cutoff:
        raise ValueError("split manifest created after cutoff")
    model = loaded["model"]
    # Every consumed model has explicit taint metadata, independently checked from file usage.
    if (type(model["uses_market"]) is not bool
            or model["uses_market"] != (spec["mode"] == "market_informed")
            or spec["mode"] != "market_informed" and "market_informed" in model["lineage_modes"]):
        raise ValueError("model market lineage/mode mismatch")
    if model["uses_market"] and not any(e["usage"] == "MARKET" for e in entries):
        raise ValueError("market-informed model requires frozen market input")
    if any(e["usage"] == "SCENARIO" for e in entries) and spec.get("purpose") != "SYNTHETIC_TEST" and spec["mode"] != "script_adjusted":
        raise ValueError("scenario inputs require separately labeled script_adjusted run")
    if any(e["usage"] == "SCENARIO" for e in entries) or "SCENARIO_ONLY" in model.get("flags", []):
        if spec.get("purpose") != "SYNTHETIC_TEST" and spec["mode"] != "script_adjusted":
            raise ValueError("scenario-only model requires labeled script_adjusted run")
    if game["game_id_namespace"] == "synthetic_test" and spec.get("purpose") != "SYNTHETIC_TEST":
        raise ValueError("synthetic identity cannot be promoted to real forecast")
    manifest = {"serializer_version": SERIALIZER, "entries": entries,
                "hash_exclusions": ["manifest_creation_time", "self_hash"]}
    input_hash = digest(manifest)
    engine = engine_identity()
    package = Path(__file__).resolve().parent
    code_snapshot = {p.relative_to(package).as_posix(): p.read_bytes()
                     for p in source_files(package)}
    if digest({name: byte_digest(data) for name, data in code_snapshot.items()}) != engine["source_content_hash"]:
        raise ValueError("code changed during freeze")
    modeling_spec = {k: v for k, v in spec.items() if k not in {"generated_at_utc", "frozen_at_utc"}}
    run_spec = {"contract_version": CONTRACT_VERSION, "serializer_version": SERIALIZER,
                "hash_exclusions": ["generated_at_utc", "frozen_at_utc", "forecast_id"],
                "input_content_hash": input_hash, "spec": modeling_spec, "engine": engine,
                "ot_rule_profile": model["ot_rule_profile"], "stat_credit_profile": model["stat_credit_profile"],
                "trial_indices": list(range(spec.get("trial_start", 0), spec.get("trial_start", 0) + n)),
                "rng": {"seed": str(seed), "rng_algorithm": "PCG64", "rng_version": np.__version__,
                        "seed_derivation_version": SEED_VERSION}}
    return {"forecast_id": digest(run_spec), "run_spec": run_spec, "input_manifest": manifest,
            "input_content_hash": input_hash, "spec": spec, "loaded": loaded, "blobs": blobs,
            "code_snapshot": code_snapshot,
            "split_membership": membership}


def verify_frozen(frozen):
    """Detect mutation of a prepared run before execution or artifact publication."""
    if digest(frozen["run_spec"]) != frozen["forecast_id"] or digest(frozen["input_manifest"]) != frozen["input_content_hash"]:
        raise ValueError("frozen run/manifest hash mismatch")
    spec = {k: v for k, v in frozen["spec"].items() if k not in {"generated_at_utc", "frozen_at_utc"}}
    if spec != frozen["run_spec"]["spec"]:
        raise ValueError("frozen specification mutated")
    if digest({name: byte_digest(data) for name, data in frozen["code_snapshot"].items()}) != frozen["run_spec"]["engine"]["source_content_hash"]:
        raise ValueError("frozen code content mutated")
    package = Path(__file__).resolve().parent
    current = {p.relative_to(package).as_posix(): byte_digest(p.read_bytes())
               for p in source_files(package)}
    if digest(current) != frozen["run_spec"]["engine"]["source_content_hash"]:
        raise ValueError("runtime code differs from frozen source")
    if frozen["run_spec"]["engine"]["dependencies"] != {"python": platform.python_version(), "numpy": np.__version__}:
        raise ValueError("runtime dependency/RNG version differs from freeze")
    for entry in frozen["input_manifest"]["entries"]:
        key = entry["logical_input_id"]
        blob = frozen["blobs"][key]
        if byte_digest(blob) != entry["sha256"] or len(blob) != entry["byte_size"] or canonical(json.loads(blob)) != canonical(frozen["loaded"][key]):
            raise ValueError("frozen input content mutated")


def trial_seed(frozen: dict, index: int) -> str:
    integer(index, "trial_index", 0)
    spec = frozen["run_spec"]
    game = spec["spec"]["game"]
    values = [SEED_VERSION, spec["rng"]["seed"], game["game_id_namespace"], game["game_id"],
              index]
    return str(int.from_bytes(hashlib.sha256(canonical(values)).digest()[:8], "big"))
