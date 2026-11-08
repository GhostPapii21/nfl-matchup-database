"""Opportunity-first local CORE producer for nfl-sim-core-contract-v1.

Opt-in frozen model tables, never inferred from historical yard-row assignments.
This is a structural research model, not a fitted forecast or official OT engine.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import numpy as np

from joint_inputs import (CONTRACT_VERSION, canonical, digest, freeze_run, integer, safe_path, trial_seed, verify_frozen)
from joint_accounting import (PLAYER_STATS, TEAM_STATS, TARGETED, UNTARGETED, RUSHES, TERMINALS,
                              allocate, derive_tables, finalize_validation, zeros)

OT_PROFILE = {"id": "single_possession_approx_declared_limitation", "period_length_seconds": 600,
              "possession_entitlement": "NOT_OFFICIAL; no guaranteed matching possession",
              "termination": "first score or expiration", "tie_behavior": "tie at expiration",
              "applicability": "research_approximation_only", "limitations": ["NOT_VERIFIED_OFFICIAL_OT"]}
STAT_PROFILE = {"id": "core_integer_offense_v1", "yard_unit": "integer_yards",
                "kneels": "rushing_attempt", "scrambles": "dropback_and_rushing_attempt",
                "sack_loss": "nonnegative_magnitude", "no_play": "no_official_offense_credits",
                "turnovers": "interceptions_plus_lost_fumbles_plus_turnover_on_downs_excluding_punts_and_missed_fg",
                "provider": "MODELED_CONTRACT_PROFILE_NOT_PROVIDER_SETTLEMENT"}


def missing_features():
    features = {name: {"status": "UNKNOWN" if name == "coverage" else "MISSING", "value": None,
                   "allows_sim_effect": False, "evidence_scope": "UNAVAILABLE_NOT_ZERO",
                   "source_refs": [], "asof_refs": []}
            for name in ("coverage", "routes", "personnel_11", "personnel_12", "personnel_13")}
    for name in ("penalties", "returns", "official_overtime"):
        features[name] = {"status": "UNSUPPORTED", "value": None, "allows_sim_effect": False,
                          "evidence_scope": "NOT_FITTED", "source_refs": [], "asof_refs": []}
    return features


def choose(rng, distribution):
    if not distribution:
        raise ValueError("empty distribution: UNSUPPORTED")
    weights = np.array([row["weight"] for row in distribution], dtype=float)
    if not np.all(np.isfinite(weights)) or np.any(weights < 0) or weights.sum() <= 0:
        raise ValueError("invalid distribution weights")
    return deepcopy(distribution[int(rng.choice(len(distribution), p=weights / weights.sum()))]["value"])


def provenance(model, stage, **fields):
    return {"generation_stage": stage, "provenance_refs": model["provenance_refs"],
            "model_version": model["model_version"], "sample_size": model["sample_size"],
            "sample_size_reason": model.get("sample_size_reason"),
            "flags": ["MODELED", *model.get("flags", [])], **fields}


def matches(when, context):
    for key, value in when.items():
        if key.endswith("_min"):
            if context[key[:-4]] < value:
                return False
        elif key.endswith("_max"):
            if context[key[:-4]] > value:
                return False
        elif context[key] != value:
            return False
    return True


class OpportunityModel:
    def __init__(self, frozen, rng):
        self.model = frozen["loaded"]["model"]
        self.rng = rng
        # Fixed one-draw split: attribution never consumes the team stream.
        self.role_rng = np.random.default_rng(int(rng.integers(0, 2**63)))
        self.roster = frozen["loaded"]["registry"]["players"]
        self.by_ref = {r["record_id"]: r for r in self.roster}
        if len(self.by_ref) != len(self.roster):
            raise ValueError("duplicate roster record ID")
        model = self.model
        if model.get("role_efficiency_coupling", False):
            raise ValueError("UNSUPPORTED explicit role efficiency coupling; not fitted")
        role_keys = {"passer_ref", "receiver_ref", "runner_ref", "role_state_id"}
        for cell in model["usage_cells"] + model["outcome_cells"]:
            if any(k.removesuffix("_min").removesuffix("_max") in role_keys for k in cell["when"]):
                raise ValueError("role-conditioned efficiency requires justified coupling")
        if model["ot_rule_profile"] != OT_PROFILE or model["stat_credit_profile"] != STAT_PROFILE:
            raise ValueError("UNSUPPORTED OT/stat profile; consumer must check approximation")
        if not model["provenance_refs"] or not model["model_version"]:
            raise ValueError("decision provenance/model version required")
        if model["sample_size"] is None and not model.get("sample_size_reason"):
            raise ValueError("missing sample size requires a reason")
        self.environment = choose(rng, model["environments"])
        self.roles = {team: choose(rng, rows) for team, rows in model["role_states"].items()}
        self.live_team = {}
        self.live_player = {}
        for team, state in self.roles.items():
            for ref in state["available"]:
                if ref not in self.by_ref or self.by_ref[ref]["team_id"] != team:
                    raise ValueError("availability contains foreign/unknown roster reference")
            # No silent uniform role fallback, depth/rotation/charted features are distinct.
            for role in ("passer", "target", "carry"):
                if role not in state["rotation_weights"]:
                    raise ValueError("availability/depth/rotation distribution MISSING")
            if "depth_chart_state" not in state or not state["target_depth_distribution"]:
                raise ValueError("depth-chart/target-depth uncertainty MISSING")

    def context(self, state):
        return {**state, "score_margin": state["score"][state["possession"]] - state["score"][self.other(state)],
                "team_id": state["possession"], "environment_id": self.environment["environment_id"],
                "role_state_id": self.roles[state["possession"]]["state_id"]}

    @staticmethod
    def other(state):
        return next(t for t in state["score"] if t != state["possession"])

    def identity(self, ref):
        if ref is None:
            return None
        row = self.by_ref[ref]
        if row["player_id"] is None:
            return None
        return {"player_id_namespace": row["player_id_namespace"], "player_id": row["player_id"]}

    def role(self, team, role, modifiers, period_id="Q1"):
        state = self.roles[team]
        candidates = []
        half = "1" if period_id in ("Q1", "Q2") else "2"
        weights = state.get("rotation_by_half", {}).get(half, state["rotation_weights"])
        for ref, weight in weights[role].items():
            if ref == "UNASSIGNED":
                candidates.append({"value": None, "weight": weight})
            elif ref in state["available"]:
                if self.by_ref[ref]["team_id"] != team:
                    raise ValueError("foreign role player")
                candidates.append({"value": ref, "weight": weight * modifiers.get(role, {}).get(ref, 1)})
        if not candidates:
            # Explicit unassigned bucket, never an invented named player.
            return None
        return choose(self.role_rng, candidates)

    def opportunity(self, state):
        context = self.context(state)
        cell = next((c for c in self.model["usage_cells"] if matches(c["when"], context)), None)
        if cell is None:
            raise ValueError("UNSUPPORTED pre-snap state; no silent fallback")
        terminal = choose(self.rng, cell["terminals"])
        if terminal not in TERMINALS:
            raise ValueError(f"UNSUPPORTED terminal {terminal}")
        team = state["possession"]
        modifiers = cell.get("role_weight_multipliers", {})
        passer = self.role(team, "passer", modifiers, state["period_id"]) if terminal in TARGETED | UNTARGETED | {"sack", "scramble", "aborted_dropback_no_attempt"} else None
        receiver = self.role(team, "target", modifiers, state["period_id"]) if terminal in TARGETED else None
        runner = passer if terminal == "scramble" else self.role(team, "carry", modifiers, state["period_id"]) if terminal in RUSHES else None
        assignments = {"passer": self.identity(passer), "receiver": self.identity(receiver), "runner": self.identity(runner)}
        depth = choose(self.rng, self.roles[team]["target_depth_distribution"]) if terminal in TARGETED else None
        t, p, credit = allocate(terminal, team, **assignments)
        trace = [provenance(self.model, "PRE_SNAP", context=context, usage_cell_id=cell["cell_id"],
                            cell_evidence={k: cell[k] for k in ("sample_size", "uncertainty", "flags", "pooling") if k in cell},
                            role_state=self.roles[team], conditional_role_weights=modifiers, target_depth=depth),
                 provenance(self.model, "OPPORTUNITY", team_counts=deepcopy(t), player_counts=deepcopy(list(p.values())))]
        # These increments occur in the execution path before outcome() can draw anything.
        live = self.live_team.setdefault(team, zeros(TEAM_STATS))
        for k in TEAM_STATS:
            live[k] += t[k]
        for key, row in p.items():
            bucket = self.live_player.setdefault((team, *key), zeros(PLAYER_STATS))
            for k in PLAYER_STATS:
                bucket[k] += row["stats"][k]
        return {"terminal": terminal, "team": team, "team_credits": t, "players": p, "credit": credit,
                "assignments": assignments, "trace": trace,
                "context": {**context, "terminal": terminal, "target_depth": depth,
                            "passer_ref": passer, "receiver_ref": receiver, "runner_ref": runner}}

    def outcome(self, opportunity):
        terminal = opportunity["terminal"]
        catch = choose(self.rng, self.model["catch_distributions"][terminal]) if terminal in TARGETED else "NA"
        if catch not in {"COMPLETE", "INCOMPLETE", "INTERCEPTION", "NA"} or terminal in TARGETED and catch == "NA":
            raise ValueError("unsupported catch outcome")
        opportunity["trace"].append(provenance(self.model, "CATCH", outcome=catch,
            cell_evidence=self.model.get("catch_evidence", {}).get(terminal, {})))
        context = {**opportunity["context"], "catch": catch}
        cell = next((c for c in self.model["outcome_cells"] if matches(c["when"], context)), None)
        if cell is None:
            raise ValueError("UNSUPPORTED outcome state")
        outcome = choose(self.rng, cell["distribution"])
        for key in ("yards", "elapsed_seconds"):
            integer(outcome[key], key, 0 if key == "elapsed_seconds" else None)
        if catch in {"INCOMPLETE", "INTERCEPTION"} or terminal in UNTARGETED | {"no_play", "aborted_dropback_no_attempt", "punt", "field_goal", "period_end_runoff"}:
            if outcome["yards"] != 0:
                raise ValueError("non-yard-bearing outcome must have zero offense yards")
        if terminal == "sack" and outcome["yards"] > 0:
            raise ValueError("sack cannot have positive yards")
        opportunity["trace"].append(provenance(self.model, "YARDS", outcome_cell_id=cell["cell_id"],
                                               cell_evidence={k: cell[k] for k in ("sample_size", "uncertainty", "flags", "pooling") if k in cell},
                                               raw_outcome=deepcopy(outcome)))
        return catch, outcome


def derive_possessions(events):
    possessions = {}
    for e in events:
        pid = e["possession_id"]
        p = possessions.setdefault(pid, {"possession_id": pid, "team_id": e["pre_state"]["possession"],
                                        "start_event_id": e["event_id"], "end_event_id": None,
                                        "end_cause": None, "period_segments": [], "clock_seconds": 0,
                                        "field_advance_yards": 0, "points": 0, "turnovers": 0,
                                        "definitions": {"points": "possession_team_credited_points_only",
                                                        "field_advance_yards": "offensive_advancement_excluding_special_teams"}})
        if p["end_cause"] is not None:
            raise ValueError("possession continues after termination")
        if not p["period_segments"] or p["period_segments"][-1]["period_id"] != e["period_id"]:
            p["period_segments"].append({"period_id": e["period_id"], "clock_seconds": 0})
        p["period_segments"][-1]["clock_seconds"] += e["elapsed_clock_seconds"]
        p["clock_seconds"] += e["elapsed_clock_seconds"]
        t = e["team_credits"].get(p["team_id"], zeros(TEAM_STATS))
        p["field_advance_yards"] += t["field_advance_yards"]
        p["points"] += t["points"]
        p["turnovers"] += t["turnovers"]
        p["end_event_id"] = e["event_id"]
        if e.get("possession_end_cause"):
            p["end_cause"] = e["possession_end_cause"]
    return list(possessions.values())


def simulate_trial(frozen, index, *, model_class=OpportunityModel):
    verify_frozen(frozen)
    if index not in frozen["run_spec"]["trial_indices"]:
        raise ValueError("trial_index not assigned in frozen run specification")
    run = frozen["run_spec"]
    spec = frozen["spec"]
    game = spec["game"]
    seed = trial_seed(frozen, index)
    model = model_class(frozen, np.random.Generator(np.random.PCG64(int(seed))))
    trial_id = f"{frozen['forecast_id']}/trial/{index}"
    features = missing_features()
    teams = [game["home_team_id"], game["away_team_id"]]
    state = {"period_id": "Q1", "period_seconds_remaining": 900, "regulation_seconds_remaining": 3600,
             "possession": teams[1], "down": 1, "ydstogo": 10, "yardline_100": 75,
             "score": dict.fromkeys(teams, 0)}
    events = []
    possession_index = 0
    went_ot = False
    reason = "final_max_steps"
    final = False
    limit = integer(spec.get("max_steps", 1000), "max_steps", 1)
    periods = []

    def clock():
        q = int(state["period_id"][1:]) if state["period_id"].startswith("Q") else 5
        state["regulation_seconds_remaining"] = (4-q)*900 + state["period_seconds_remaining"] if q <= 4 else 0

    def emit(kind, pre, *, t=None, players=None, trace=None, terminal=None, assignments=None, cause=None, adjustments=None, outcome=None, boundary=None):
        seq = len(events)
        elapsed = pre["period_seconds_remaining"] - state["period_seconds_remaining"]
        events.append({"event_id": f"{trial_id}/event/{seq}", "event_seq": seq,
                       "possession_id": f"{trial_id}/possession/{possession_index}",
                       "type": kind, "period_id": pre["period_id"],
                       "boundary": boundary,
                       "period_kind": "REG" if pre["period_id"].startswith("Q") else "OT",
                       "pre_period_seconds_remaining": pre["period_seconds_remaining"],
                       "post_period_seconds_remaining": state["period_seconds_remaining"],
                       "elapsed_clock_seconds": elapsed, "unattributed_clock_seconds": 0,
                       "pre_possession": pre["possession"], "post_possession": state["possession"],
                       "pre_state": pre, "post_state": deepcopy(state), "acting_team_id": pre["possession"],
                       "terminal_category": terminal, "assignments": assignments or {},
                       "stat_ledger": "TRY" if kind == "try" else "SPECIAL_TEAMS" if terminal in {"punt", "field_goal"} else "OFFENSE" if kind == "snap" else "TRANSITION",
                       "field_advance_yards": (t or {}).get(pre["possession"], {}).get("field_advance_yards", 0),
                       "orthogonal_flags": {"penalty": "UNSUPPORTED" if (outcome or {}).get("penalty") else False,
                                            "nullified": terminal == "no_play", "interception": bool(trace and trace[2]["outcome"] == "INTERCEPTION"),
                                            "fumble_lost": bool((outcome or {}).get("fumble_lost", False)),
                                            "lateral": bool((outcome or {}).get("receiving_credits")),
                                            "stat_eligible": terminal != "no_play", "rush_design": (outcome or {}).get("rush_design")},
                       "team_credits": t or {}, "player_credits": list((players or {}).values()),
                       "generation_trace": trace or [], "score_delta": {team: state["score"][team] - pre["score"][team] for team in teams},
                       "possession_end_cause": cause, "credit_adjustments": adjustments or [],
                       "feature_availability": deepcopy(features), "flags": ["MODELED"],
                       "provenance_refs": model.model["provenance_refs"]})

    def transition(receiving, cause, *, kickoff=False):
        nonlocal possession_index
        pre = deepcopy(state)
        state["possession"] = receiving
        state["yardline_100"] = 75 if kickoff else max(1, min(99, 100 - state["yardline_100"]))
        state["down"], state["ydstogo"] = 1, min(10, state["yardline_100"])
        emit("possession_transition", pre, cause=cause)
        possession_index += 1

    emit("period_start", deepcopy(state), boundary={"from_period_id": None, "to_period_id": "Q1", "cause": "opening", "reset_clock_seconds": 900})
    periods.append("Q1")
    steps = 0
    while not final and steps < limit:
        if state["period_seconds_remaining"] == 0:
            old = state["period_id"]
            if old == "Q4" and state["score"][teams[0]] != state["score"][teams[1]] or old == "OT1":
                reason = "regulation_complete" if old == "Q4" else "ot_expiration_tie"
                emit("final", deepcopy(state), cause=reason)
                final = True
                break
            if old == "Q2":
                transition(teams[0], "halftime", kickoff=True)
            if old == "Q4":
                transition(teams[1], "ot_reset", kickoff=True)
                new, length = "OT1", 600
                went_ot = True
            else:
                new, length = f"Q{int(old[1:]) + 1}", 900
            state["period_id"] = new
            state["period_seconds_remaining"] = length
            clock()
            emit("period_start", deepcopy(state), boundary={"from_period_id": old, "to_period_id": new,
                 "cause": "halftime" if old == "Q2" else "ot_reset" if old == "Q4" else "quarter_end",
                 "reset_clock_seconds": length})
            periods.append(new)
            continue
        steps += 1
        pre = deepcopy(state)
        op = model.opportunity(deepcopy(state))
        catch, outcome = model.outcome(op)  # allocations and counts already exist here
        if outcome.get("penalty") or outcome.get("untimed_down") or outcome.get("defensive_return_yards") or outcome.get("return_yards"):
            raise ValueError("UNSUPPORTED penalty/untimed/return profile; no invented credits")
        terminal, team = op["terminal"], op["team"]
        t, p, credit = op["team_credits"], op["players"], op["credit"]
        raw = outcome["yards"]
        # This version's ordinary outcomes stop at a goal line. Explicit stat/field
        # differences (lateral/fumble/provider adjustment) retain separate credits.
        yards = min(raw, state["yardline_100"]) if raw > 0 else max(raw, -(100-state["yardline_100"]))
        advance = outcome.get("field_advance_yards", yards)
        integer(advance, "field_advance_yards")
        if not -(100-state["yardline_100"]) <= advance <= state["yardline_100"]:
            raise ValueError("unsupported out-of-field advancement")
        adjustments = []
        if advance != yards or "receiving_credits" in outcome or outcome.get("pass_receiving_credit_adjustment", 0):
            if not outcome.get("credit_explanation") or not outcome.get("credit_provenance_refs"):
                raise ValueError("field/stat/lateral difference requires explicit evidence and explanation")
            adjustments.append({"event_id": f"{trial_id}/event/{len(events)}", "field_advance_yards": advance,
                                "credited_yards": yards, "signed_pass_receiving_adjustment": outcome.get("pass_receiving_credit_adjustment", 0),
                                "explanation": outcome["credit_explanation"], "provenance_refs": outcome["credit_provenance_refs"]})
        if catch == "COMPLETE":
            t["completions"] += 1
            credit(op["assignments"]["receiver"], "catches", 1)
            t["gross_pass_yards"] += yards
            credit(op["assignments"]["passer"], "pass_yards", yards)
            rec_rows = outcome.get("receiving_credits", [{"player_ref": op["context"]["receiver_ref"], "yards": yards}])
            for rec in rec_rows:
                integer(rec["yards"], "receiving_credit")
                if rec["player_ref"] is not None and model.by_ref[rec["player_ref"]]["team_id"] != team:
                    raise ValueError("lateral recipient is on another team")
                t["receiving_yards"] += rec["yards"]
                credit(model.identity(rec["player_ref"]), "rec_yards", rec["yards"])
            t["pass_receiving_credit_adjustment"] = outcome.get("pass_receiving_credit_adjustment", 0)
        elif terminal == "sack":
            t["sack_loss_yards"] = -yards
        if terminal in RUSHES:
            t["rush_yards"] += yards
            credit(op["assignments"]["runner"], "rush_yards", yards)
        t["net_pass_yards"] = t["gross_pass_yards"] - t["sack_loss_yards"]
        t["field_advance_yards"] = advance
        cost = min(state["period_seconds_remaining"], outcome["elapsed_seconds"])
        state["period_seconds_remaining"] -= cost
        clock()
        t["possession_seconds"] = cost
        op["trace"][-1]["realized_yards"] = yards
        op["trace"][-1]["field_bound_profile"] = "goal_line_stops_v1"
        turnover = catch == "INTERCEPTION" or bool(outcome.get("fumble_lost", False))
        end_cause = None
        scoring_team = None
        if terminal == "punt":
            net = integer(outcome["punt_net_yards"], "punt net", 0)
            state["yardline_100"] = max(20, state["yardline_100"] - net) if net >= state["yardline_100"] else state["yardline_100"] - net
            end_cause = "punt"
        elif terminal == "field_goal":
            if outcome["made"]:
                t["points"] = 3
                scoring_team = team
                end_cause = "score"
            else:
                # Spot of kick or own 20; no quote/settlement rule is involved.
                state["yardline_100"] = max(20, state["yardline_100"] + 7)
                end_cause = "missed_field_goal"
        elif terminal not in {"no_play", "period_end_runoff"}:
            state["yardline_100"] -= advance
            if turnover:
                t["turnovers"] = 1
                end_cause = "turnover"
                if state["yardline_100"] <= 0:
                    state["yardline_100"] = 20  # modeled no-return touchback
            elif state["yardline_100"] >= 100:
                scoring_team = model.other(state)
                end_cause = "safety"
            elif state["yardline_100"] <= 0:
                t["points"] = 6
                scoring_team = team
                end_cause = "touchdown"
            else:
                if advance >= state["ydstogo"]:
                    state["down"], state["ydstogo"] = 1, min(10, state["yardline_100"])
                else:
                    state["down"] += 1
                    state["ydstogo"] = max(1, state["ydstogo"] - advance)
                    if state["down"] > 4:
                        end_cause = "turnover_on_downs"
                        t["turnovers"] = 1
        credits = {team: t}
        if end_cause == "safety":
            credits[scoring_team] = zeros(TEAM_STATS)
            credits[scoring_team]["points"] = 2
        for who, values in credits.items():
            state["score"][who] += values["points"]
        emit("period_end_runoff" if terminal == "period_end_runoff" else "snap", pre, t=credits, players=p, trace=op["trace"], terminal=terminal,
             assignments=op["assignments"], adjustments=adjustments, outcome=outcome)
        if end_cause == "touchdown":
            pre = deepcopy(state)
            points = choose(model.rng, model.model["try_points"])
            integer(points, "try points", 0)
            if points > 2:
                raise ValueError("unsupported try")
            state["score"][team] += points
            tc = zeros(TEAM_STATS)
            tc["points"] = points
            emit("try", pre, t={team: tc})  # required linked event stays in starting period at 0:00
        if state["period_id"] == "OT1" and scoring_team is not None:
            reason = "ot_first_score_approximation"
            emit("final", deepcopy(state), cause=reason)
            final = True
        elif end_cause:
            receiving = scoring_team if end_cause == "safety" else model.other(state)
            transition(receiving, end_cause, kickoff=scoring_team is not None)
    if not final:
        emit("final_max_steps", deepcopy(state), cause="final_max_steps")
    team_periods, player_periods, aggregates = derive_tables(events, game, model.roster, periods, complete=final)
    freeze = {k: spec[k] for k in ("cutoff_utc", "frozen_at_utc", "generated_at_utc", "mode", "config_id")}
    freeze.update({"input_content_hash": frozen["input_content_hash"], "input_manifest_ref": "input_manifest.json",
                   "input_manifest_digest": digest(frozen["input_manifest"]),
                   "split_manifest_id": frozen["loaded"]["splits"]["split_manifest_id"],
                   "split_manifest_hash": digest(frozen["loaded"]["splits"]), "split_membership": frozen["split_membership"],
                   "split_dependent_claims_allowed": frozen["split_membership"] != "UNASSIGNED"})
    flags = ["MODELED", "NOT_VERIFIED_OFFICIAL_OT"]
    if spec.get("purpose") == "SYNTHETIC_TEST" or model.model.get("flags") and "SCENARIO_ONLY" in model.model["flags"]:
        flags.append("SCENARIO_ONLY")
    trial = {"contract_version": CONTRACT_VERSION, "forecast_id": frozen["forecast_id"], "trial_id": trial_id,
             "trial_index": index, "game": deepcopy(game), "freeze": freeze,
             "engine": {**run["engine"], "ot_rule_profile": OT_PROFILE, "stat_credit_profile": STAT_PROFILE,
                        "source_artifact_ref": "engine_source_manifest.json",
                        "limitations": ["MODEL_PREDICTIVE_VALIDATION_NOT_MEASURED", "NO_RETURN_YARDS", "NO_UNTIMED_PENALTY_PROFILE", "NO_OFFICIAL_OT_CLAIM"]},
             "rng": {**run["rng"], "trial_seed": seed}, "status": {"state": "COMPLETE" if final else "INCOMPLETE",
              "completion_reason": reason, "terminal_state": deepcopy(state), "went_ot": went_ot},
             "latent_state": {"environment": model.environment, "roles": model.roles,
                              "provenance": provenance(model.model, "TRIAL_LATENT")},
             "events": events, "possessions": derive_possessions(events), "team_periods": team_periods,
             "player_periods": player_periods, "aggregates": aggregates, "feature_availability": features,
             "provenance": {"roster": model.roster, "crosswalk_hash": digest(frozen["loaded"]["registry"]["crosswalk"]),
                            "input_refs": [e["logical_input_id"] for e in frozen["input_manifest"]["entries"]],
                            "evidence_only_refs": [{"source_ref": "not_included/actual_role_coverage_audit.md",
                                                    "usage": "EVIDENCE_ONLY_POSTGAME", "predictive_input": False,
                                                    "note": "Contract reference only; not read or used for fitting by this producer"}]},
             "flags": flags, "validation": {}}
    return finalize_validation(trial)


def _write_once(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as stream:
            stream.write(data)
    except FileExistsError:
        if path.read_bytes() != data:
            raise ValueError(f"immutable artifact conflict: {path.name}")


def write_forecast(output_root, frozen, trials):
    """Durable content-addressed run plus frozen bytes and separate forecast ledger."""
    verify_frozen(frozen)
    expected_ids = [f"{frozen['forecast_id']}/trial/{i}" for i in frozen["run_spec"]["trial_indices"]]
    if [t["trial_id"] for t in trials] != expected_ids:
        raise ValueError("joint trial population/order mismatch; no implicit exclusions")
    for trial in trials:
        finalize_validation(trial)  # stale caller-supplied PASS/projection flags never authorize publication
    root = Path(output_root)
    directory = safe_path(root, frozen["forecast_id"].replace(":", "_"))
    directory.mkdir(parents=True, exist_ok=True)
    artifacts = {"run_spec.json": canonical(frozen["run_spec"]), "input_manifest.json": canonical(frozen["input_manifest"]),
                 "trials.jsonl": b"".join(canonical(t) + b"\n" for t in trials)}
    from joint_inputs import byte_digest
    artifacts["engine_source_manifest.json"] = canonical({name: byte_digest(data) for name, data in frozen["code_snapshot"].items()})
    for name, data in frozen["code_snapshot"].items():
        artifacts["engine_source/" + name] = data
    for entry in frozen["input_manifest"]["entries"]:
        artifacts["inputs/" + entry["path"]] = frozen["blobs"][entry["logical_input_id"]]
    for name, data in artifacts.items():
        _write_once(safe_path(directory, name), data)
    hashes = {name: byte_digest(data) for name, data in artifacts.items()}
    spec = frozen["spec"]
    ledger = {"forecast_id": frozen["forecast_id"], "game_id": spec["game"]["game_id"],
              "cutoff_utc": spec["cutoff_utc"], "engine_version": frozen["run_spec"]["engine"]["engine_version"],
              "input_content_hash": frozen["input_content_hash"], "mode": spec["mode"],
              "split_manifest_id": frozen["loaded"]["splits"]["split_manifest_id"],
              "split_manifest_hash": digest(frozen["loaded"]["splits"]),
              "split_membership": frozen["split_membership"], "trial_ids": [t["trial_id"] for t in trials],
              "artifact_hashes": hashes, "result_evidence_ids": [], "impact": "NOT MEASURED"}
    _write_once(directory / "forecast_ledger.json", canonical(ledger))
    return str(directory)


def simulate_joint_games(spec, *, input_root, inputs, n, seed, output_root):
    frozen = freeze_run(spec, input_root, inputs, n=n, seed=seed)
    trials = [simulate_trial(frozen, i) for i in frozen["run_spec"]["trial_indices"]]
    counts = {name: sum(t["status"]["state"] == name for t in trials) for name in ("COMPLETE", "INCOMPLETE", "INVALID")}
    usable = [t["trial_id"] for t in trials if t["status"]["adapter_projection_allowed"]]
    artifact = write_forecast(output_root, frozen, trials)
    return {"forecast_id": frozen["forecast_id"], "input_content_hash": frozen["input_content_hash"],
            "n_requested": n, "n_completed": counts["COMPLETE"], "n_incomplete": counts["INCOMPLETE"],
            "n_invalid": counts["INVALID"], "n_usable": len(usable), "retained_trial_ids": usable,
            "excluded_trials": [{"trial_id": t["trial_id"], "reasons": t["status"]["projection_blockers"]}
                                for t in trials if not t["status"]["adapter_projection_allowed"]],
            "conditioning_basis": "complete valid identified non-scenario trials; exclusions explicit; no resampling",
            "trials": trials, "artifact_directory": artifact, "mode": spec["mode"],
            "status": "INVALID" if counts["INVALID"] else "INCOMPLETE" if counts["INCOMPLETE"] else "OK"}
