"""Contract-aligned score transport, not a full producer acceptance validator.

No resampling, player synthesis, canonical-ID guessing, or consumer exclusions.
All input rows are preserved or the entire batch is rejected. The adapter can
inspect scores while full accounting validation remains NOT_RUN. Such transport
is never an actionable quote/trial MATCHED result under contract section 8.
"""
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from copy import deepcopy
import json
import re

from .quotes import utc
from .settlement import ScoreCard

CORE_CONTRACT = Path(__file__).resolve().parents[1] / "research/nfl_sim_integration_2026-11-06/core_contract.md"
CONTRACT_SHA256 = "6471e69b97b19b85ce0a4b8e4c25117b0e40ceefa1a225ee06d7c1b7440e8367"
HASH_PATTERN = r"sha256:[0-9a-f]{64}"
WIRE_AGREEMENT_ID = "market-producer-wire-v1.0.1"


def contract_info():
    if not CORE_CONTRACT.exists():
        return {"path": str(CORE_CONTRACT), "status": "PROVISIONAL_NO_CORE_CONTRACT", "sha256": None}
    content = CORE_CONTRACT.read_bytes()
    digest = sha256(content).hexdigest()
    return {"path": str(CORE_CONTRACT), "status": "CONTRACT_SCORE_TRANSPORT_ONLY" if digest == CONTRACT_SHA256
            else "CORE_CONTRACT_REQUIRES_ALIGNMENT", "sha256": digest, "text": content.decode()}


@dataclass(frozen=True)
class JointTrial:
    trial_id: str
    seed: str
    scorecard: ScoreCard
    trial_seed: str
    forecast_id: str
    input_content_hash: str
    trial_index: int
    source: dict
    interface_status: str = "CONTRACT_SCORE_TRANSPORT_ONLY"
    actionable_status: str = "NOLINE"
    reasons: tuple[str, ...] = ("FULL_CORE_ACCEPTANCE_NOT_RUN", "QUOTE_RULE_COMPATIBILITY_NOT_VERIFIED")


def require_fields(obj, fields, name):
    if not isinstance(obj, dict) or not set(fields) <= obj.keys():
        raise ValueError(f"missing {name} fields")


def hash_value(value):
    return isinstance(value, str) and re.fullmatch(HASH_PATTERN, value) is not None


def wire_alias(obj, primary, legacy, name):
    """Read either spelling without changing the row; reject ambiguity."""
    if primary not in obj and legacy not in obj:
        raise ValueError(f"missing {name} fields: {primary} or {legacy}")
    if primary in obj and legacy in obj and (
            type(obj[primary]) is not type(obj[legacy]) or obj[primary] != obj[legacy]):
        raise ValueError(f"conflicting {name}: {primary} and {legacy}")
    return obj[primary] if primary in obj else obj[legacy]


def completion_status(row):
    """Read producer status natively, retaining legacy scalar compatibility."""
    status = row["status"]
    fields = ("completion_reason", "terminal_state", "went_ot")
    if isinstance(status, dict):
        require_fields(status, ("state", *fields), "status")
        state = status["state"]
        for field in fields:
            if field in row and (type(row[field]) is not type(status[field]) or row[field] != status[field]):
                raise ValueError(f"conflicting status field: {field}")
    else:
        require_fields(row, fields, "trial status")
        state, status = status, row
    if state != "COMPLETE":
        raise ValueError("unsupported contract or incomplete/invalid trial; no silent exclusion")
    return status


def derive_trial_seed(row):
    rng, game, freeze = row["rng"], row["game"], row["freeze"]
    material = [rng["seed_derivation_version"], rng["seed"], game["game_id_namespace"],
                game["game_id"], freeze["input_content_hash"], row["trial_index"]]
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()
    return str(int.from_bytes(sha256(encoded).digest()[:8], "big"))


def scorecard_from_trial(row):
    game = row["game"]
    home, away = game["home_team_id"], game["away_team_id"]
    periods = {}
    if not isinstance(row["team_periods"], list):
        raise ValueError("inline team_periods rows required for score transport")
    for record in row["team_periods"]:
        require_fields(record, ("team_id", "period_id"), "team_periods")
        team, period = record["team_id"], record["period_id"]
        stats = record.get("stats")
        nested_points = isinstance(stats, dict) and "points" in stats
        if "points" not in record and not nested_points:
            raise ValueError("missing team_periods points or stats.points")
        points = record["points"] if "points" in record else stats["points"]
        if nested_points and (type(stats["points"]) is not int or stats["points"] != points):
            raise ValueError("conflicting or invalid team period points")
        if team not in {home, away} or not isinstance(period, str) or not re.fullmatch(r"Q[1-4]|OT[1-9][0-9]*", period):
            raise ValueError("unexpected team or primitive period")
        key = team, period
        if key in periods or type(points) is not int or points < 0:
            raise ValueError("duplicate or invalid team period score")
        periods[key] = points
    quarters = {}
    for period in ("Q1", "Q2", "Q3", "Q4"):
        if any((team, period) not in periods for team in (home, away)):
            raise ValueError("missing regulation score")
        quarters[period] = (periods[home, period], periods[away, period])
    ot_periods = {period for _, period in periods if period.startswith("OT")}
    went_ot = completion_status(row)["went_ot"]
    if type(went_ot) is not bool or bool(ot_periods) != went_ot:
        raise ValueError("OT unknown or inconsistent")
    if ot_periods != {f"OT{i}" for i in range(1, len(ot_periods) + 1)}:
        raise ValueError("noncontiguous OT periods")
    if any((team, period) not in periods for team in (home, away) for period in ot_periods):
        raise ValueError("missing OT team score")
    if ot_periods and sum(quarters[q][0] - quarters[q][1] for q in quarters) != 0:
        raise ValueError("OT requires regulation tie")
    overtime = tuple(sum(periods[team, period] for period in ot_periods) for team in (home, away))
    return ScoreCard(game["game_id"], home, away, quarters, overtime)


def adapt_joint_trials(rows, *, expected_trial_ids=None):
    info = contract_info()
    if info["status"] != "CONTRACT_SCORE_TRANSPORT_ONLY":
        raise ValueError("bound core contract absent or changed; alignment required")
    result, seen, population = [], set(), None
    required = ("contract_version", "forecast_id", "trial_id", "trial_index", "game", "freeze", "engine", "rng",
        "status", "latent_state", "events", "possessions",
        "team_periods", "player_periods", "aggregates", "feature_availability", "provenance", "flags", "validation")
    for row in rows:
        require_fields(row, required, "trial")
        try:
            json.dumps(row, allow_nan=False)
        except (TypeError, ValueError) as exc:
            raise ValueError("trial must be finite JSON-compatible data") from exc
        if row["contract_version"] != "1.0.0":
            raise ValueError("unsupported contract or incomplete/invalid trial; no silent exclusion")
        completion_status(row)
        if type(row["trial_index"]) is not int or row["trial_index"] < 0 or not hash_value(row["forecast_id"]):
            raise ValueError("invalid forecast/index")
        trial_id = f'{row["forecast_id"]}/trial/{row["trial_index"]}'
        if row["trial_id"] != trial_id or trial_id in seen:
            raise ValueError("trial_id derivation mismatch or duplicate")
        seen.add(trial_id)
        game, freeze, rng = row["game"], row["freeze"], row["rng"]
        require_fields(game, ("game_id", "game_id_namespace", "season", "season_type", "week", "home_team_id",
                             "away_team_id", "kickoff_utc", "crosswalk_ref"), "game")
        if any(not isinstance(game[k], str) or not game[k] for k in
               ("game_id", "game_id_namespace", "home_team_id", "away_team_id", "crosswalk_ref")):
            raise ValueError("unresolved game/team identity")
        require_fields(freeze, ("cutoff_utc", "frozen_at_utc", "generated_at_utc", "input_content_hash",
            "input_manifest_ref", "mode", "config_id", "split_manifest_id", "split_manifest_hash"), "freeze")
        manifest_digest = wire_alias(freeze, "input_manifest_digest", "input_manifest_hash", "freeze manifest")
        for digest in (freeze["input_content_hash"], manifest_digest, freeze["split_manifest_hash"]):
            if not hash_value(digest):
                raise ValueError("invalid freeze hash")
        for timestamp in (freeze["cutoff_utc"], freeze["frozen_at_utc"], freeze["generated_at_utc"], game["kickoff_utc"]):
            if not isinstance(timestamp, str) or not timestamp.endswith("Z"):
                raise ValueError("contract clocks require UTC Z timestamps")
            utc(timestamp)
        if not utc(freeze["cutoff_utc"]) <= utc(freeze["frozen_at_utc"]) <= utc(freeze["generated_at_utc"]):
            raise ValueError("freeze clock ordering mismatch")
        if utc(freeze["cutoff_utc"]) >= utc(game["kickoff_utc"]):
            raise ValueError("pregame score transport requires pre-kickoff cutoff")
        if freeze["mode"] not in {"data_only", "script_adjusted", "market_informed"}:
            raise ValueError("unknown model mode")
        require_fields(row["engine"], ("engine_version", "ot_rule_profile", "stat_credit_profile", "limitations"), "engine")
        if not {"component_version", "component_versions"} & row["engine"].keys():
            raise ValueError("missing engine fields: component_version or component_versions")
        wire_alias(row["engine"], "dependencies", "dependency_versions", "engine dependencies")
        if not row["engine"]["ot_rule_profile"] or not row["engine"]["stat_credit_profile"]:
            raise ValueError("unknown OT/stat profile")
        require_fields(rng, ("seed", "trial_seed", "rng_algorithm", "rng_version", "seed_derivation_version"), "rng")
        for key in ("seed", "trial_seed"):
            if not isinstance(rng[key], str) or not re.fullmatch(r"0|[1-9][0-9]*", rng[key]):
                raise ValueError("lossless decimal seed strings required")
        if rng["trial_seed"] != derive_trial_seed(row):
            raise ValueError("trial_seed derivation mismatch")
        features = row["feature_availability"]
        require_fields(features, ("coverage", "routes", "personnel_11", "personnel_12", "personnel_13"), "feature_availability")
        for feature in features.values():
            require_fields(feature, ("status", "value", "allows_sim_effect"), "feature")
            if feature["status"] in {"UNKNOWN", "MISSING", "UNSUPPORTED"} and (
                    feature["value"] is not None or feature["allows_sim_effect"] is not False):
                raise ValueError("missing/unknown feature cannot invent a value or allow an effect")
        # Forecast metadata must be identical across trials. Only the derived
        # trial seed and trial index/ID may vary under the same forecast ID.
        frozen_population = {"forecast_id": row["forecast_id"], "game": game, "freeze": freeze,
                             "engine": row["engine"], "rng": {k: v for k, v in rng.items() if k != "trial_seed"}}
        identity = json.dumps(frozen_population, sort_keys=True, separators=(",", ":"), allow_nan=False)
        if population is not None and identity != population:
            raise ValueError("mixed forecast/game/input population")
        population = identity
        card = scorecard_from_trial(row)
        result.append(JointTrial(trial_id, rng["seed"], card, rng["trial_seed"], row["forecast_id"],
                                 freeze["input_content_hash"], row["trial_index"], deepcopy(row)))
    if not result:
        raise ValueError("empty joint population")
    if expected_trial_ids is not None and list(expected_trial_ids) != [t.trial_id for t in result]:
        raise ValueError("trial population/order mismatch")
    return result
