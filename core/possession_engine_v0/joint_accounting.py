"""Exact integer event credits and fail-closed joint trial validation."""
from __future__ import annotations

from collections import defaultdict

from joint_inputs import canonical, integer

TEAM_COUNTS = ("dropbacks", "dropback_pass_attempts", "non_dropback_pass_attempts", "pass_attempts",
               "sacks", "scrambles", "aborted_dropbacks_no_attempt", "eligible_target_attempts",
               "throwaways", "spikes", "other_untargeted_attempts", "completions", "rush_attempts",
               "designed_rushes", "kneels", "credited_aborted_rushes")
PLAYER_STATS = ("targets", "catches", "carries", "pass_attempts", "sacks_taken", "pass_yards", "rec_yards", "rush_yards")
RESIDUALS = ("targets", "catches", "carries", "pass_attempts", "sacks", "pass_yards", "rec_yards", "rush_yards")
TEAM_STATS = TEAM_COUNTS + tuple("unassigned_" + k for k in RESIDUALS) + (
    "gross_pass_yards", "receiving_yards", "rush_yards", "sack_loss_yards", "net_pass_yards",
    "pass_receiving_credit_adjustment", "points", "turnovers", "field_advance_yards", "possession_seconds")
TARGETED = {"targeted_pass", "non_dropback_targeted_pass"}
UNTARGETED = {"throwaway", "spike", "other_untargeted_attempt"}
RUSHES = {"designed_rush", "scramble", "kneel", "credited_aborted_rush"}
TERMINALS = TARGETED | UNTARGETED | RUSHES | {"sack", "aborted_dropback_no_attempt", "no_play", "punt", "field_goal", "period_end_runoff"}


def zeros(keys):
    return dict.fromkeys(keys, 0)


def player_key(row):
    return (row["team_id"], row["player_id_namespace"], row["player_id"])


def allocate(terminal, team, *, passer=None, receiver=None, runner=None):
    """Allocate official attempts/opportunities. Called BEFORE any outcome/yard RNG."""
    if terminal not in TERMINALS:
        raise ValueError(f"UNSUPPORTED terminal {terminal}")
    t = zeros(TEAM_STATS)
    players = {}

    def credit(identity, stat, value):
        if identity is None or identity.get("player_id") is None:
            residual = "sacks" if stat == "sacks_taken" else stat
            t["unassigned_" + residual] += value
        else:
            key = (identity["player_id_namespace"], identity["player_id"])
            p = players.setdefault(key, {"team_id": team, **identity, "stats": zeros(PLAYER_STATS)})
            p["stats"][stat] += value

    if terminal in TARGETED | UNTARGETED | {"sack", "scramble", "aborted_dropback_no_attempt"}:
        if terminal != "non_dropback_targeted_pass":
            t["dropbacks"] += 1
    if terminal in TARGETED | UNTARGETED:
        t["pass_attempts"] += 1
        t["non_dropback_pass_attempts" if terminal == "non_dropback_targeted_pass" else "dropback_pass_attempts"] += 1
        credit(passer, "pass_attempts", 1)
    if terminal in TARGETED:
        t["eligible_target_attempts"] += 1
        credit(receiver, "targets", 1)
    elif terminal in UNTARGETED:
        t[{"throwaway": "throwaways", "spike": "spikes", "other_untargeted_attempt": "other_untargeted_attempts"}[terminal]] += 1
    elif terminal == "sack":
        t["sacks"] += 1
        credit(passer, "sacks_taken", 1)
    elif terminal == "aborted_dropback_no_attempt":
        t["aborted_dropbacks_no_attempt"] += 1
    if terminal in RUSHES:
        t["rush_attempts"] += 1
        t[{"designed_rush": "designed_rushes", "scramble": "scrambles", "kneel": "kneels",
           "credited_aborted_rush": "credited_aborted_rushes"}[terminal]] += 1
        credit(runner, "carries", 1)
    return t, players, credit


def sum_stats(rows, keys):
    result = zeros(keys)
    for row in rows:
        for stat in keys:
            result[stat] += row[stat]
    return result


def derive_tables(events, game, roster, periods, complete=True):
    teams = (game["home_team_id"], game["away_team_id"])
    team = {(t, p): zeros(TEAM_STATS) for p in periods for t in teams}
    player = {(r["team_id"], r["player_id_namespace"], r["player_id"], p): zeros(PLAYER_STATS)
              for p in periods for r in roster if r.get("player_id") is not None}
    for event in events:
        period = event["period_id"]
        for t, stats in event["team_credits"].items():
            bucket = team[(t, period)]
            for k, v in stats.items():
                bucket[k] += v
        for row in event["player_credits"]:
            bucket = player[(*player_key(row), period)]
            for k, v in row["stats"].items():
                bucket[k] += v
    def period_status(p):
        return "KNOWN" if complete or p != periods[-1] else "INCOMPLETE"
    def row_provenance(t, p):
        return {"derivation": "EVENT_LEDGER_SUM_V1", "event_ids": [e["event_id"] for e in events
                 if e["period_id"] == p and t in e["team_credits"]], "roster_ref": "registry"}
    team_rows = [{"team_id": t, "period_id": p, "stat_status": period_status(p), "stats": stats,
                  "provenance": row_provenance(t, p)} for (t, p), stats in team.items()]
    player_rows = [{"team_id": t, "player_id_namespace": ns, "player_id": pid, "period_id": p,
                    "stat_status": period_status(p), "stats": stats, "provenance": row_provenance(t, p)}
                   for (t, ns, pid, p), stats in player.items()]
    scopes = {"H1": ["Q1", "Q2"], "H2": ["Q3", "Q4"], "REG": ["Q1", "Q2", "Q3", "Q4"],
              "OT": [p for p in periods if p.startswith("OT")], "FG": periods}
    team_agg, player_agg = [], []
    # An unplayed future regulation period must never be interpreted as a known zero.
    for scope, primitive in scopes.items():
        known = (all(p in periods for p in primitive)
                 and (complete or periods[-1] not in primitive)
                 and (scope not in {"FG", "OT"} or complete))
        for t in teams:
            team_agg.append({"team_id": t, "period_id": scope, "status": "KNOWN" if known else "INCOMPLETE",
                             "provenance": {"derivation": "PRIMITIVE_PERIOD_SUM_V1", "period_ids": primitive},
                             "stats": sum_stats([team[(t, p)] for p in primitive], TEAM_STATS) if known else None})
        for row in roster:
            if row.get("player_id") is None:
                continue
            key = player_key(row)
            player_agg.append({**dict(zip(("team_id", "player_id_namespace", "player_id"), key)),
                               "period_id": scope, "status": "KNOWN" if known else "INCOMPLETE",
                               "provenance": {"derivation": "PRIMITIVE_PERIOD_SUM_V1", "period_ids": primitive},
                               "stats": sum_stats([player[(*key, p)] for p in primitive], PLAYER_STATS) if known else None})
    scores = {}
    for scope in scopes:
        rows = [r for r in team_agg if r["period_id"] == scope]
        scores[scope] = ({"total": sum(r["stats"]["points"] for r in rows),
                          "home_margin": rows[0]["stats"]["points"] - rows[1]["stats"]["points"]}
                         if all(r["stats"] is not None for r in rows) else None)
    return team_rows, player_rows, {"team": team_agg, "player": player_agg, "scores": scores}


def validate_trial(trial):
    """Recompute from the ledger, check identities/types/clocks/stages and ALL §5 equations.

    Returns INVALID on absent or malformed evidence; no declaration counts as a check.
    """
    checks = []

    def check(name, expected, actual):
        checks.append({"name": name, "expected": expected, "actual": actual, "pass": expected == actual})

    try:
        canonical(trial)  # rejects nonfinite values anywhere
        required = {"contract_version", "forecast_id", "trial_id", "trial_index", "game", "freeze", "engine", "rng",
                    "status", "latent_state", "events", "possessions", "team_periods", "player_periods", "aggregates",
                    "feature_availability", "provenance", "flags", "validation"}
        check("required_objects", [], sorted(required - trial.keys()))
        types = {"contract_version": str, "forecast_id": str, "trial_id": str, "trial_index": int,
                 **dict.fromkeys(("game", "freeze", "engine", "rng", "status", "latent_state", "aggregates",
                                  "feature_availability", "provenance", "validation"), dict),
                 **dict.fromkeys(("events", "possessions", "team_periods", "player_periods", "flags"), list)}
        for field, kind in types.items():
            check("type/" + field, kind.__name__, type(trial[field]).__name__)
        for field in ("game_id", "game_id_namespace", "season_type", "home_team_id", "away_team_id", "team_id_namespace", "crosswalk_ref"):
            check("game/" + field, True, isinstance(trial["game"][field], str) and bool(trial["game"][field]))
        integer(trial["game"]["season"], "season", 1)
        integer(trial["game"]["week"], "week", 1)
        for field in ("environment", "roles", "provenance"):
            check("latent/" + field, True, isinstance(trial["latent_state"][field], dict) and bool(trial["latent_state"][field]))
        check("trial_id", f"{trial['forecast_id']}/trial/{trial['trial_index']}", trial["trial_id"])
        integer(trial["trial_index"], "trial_index", 0)
        from joint_inputs import SEED_VERSION, CONTRACT_VERSION, utc
        import hashlib
        import re
        check("contract_version", CONTRACT_VERSION, trial["contract_version"])
        for field in (trial["forecast_id"], trial["freeze"]["input_content_hash"]):
            check("hash_format", True, bool(re.fullmatch(r"sha256:[0-9a-f]{64}", field)))
        for field in ("cutoff_utc", "frozen_at_utc", "generated_at_utc"):
            utc(trial["freeze"][field])
        check("pregame_cutoff", True, utc(trial["freeze"]["cutoff_utc"]) < utc(trial["game"]["kickoff_utc"]))
        check("mode", True, trial["freeze"]["mode"] in {"data_only", "script_adjusted", "market_informed"})
        for field in ("engine_version", "component_version", "source_content_hash", "dirty_patch_hash", "dependencies",
                      "ot_rule_profile", "stat_credit_profile", "limitations"):
            check("engine/" + field, True, bool(trial["engine"][field]))
        for field in ("seed", "trial_seed"):
            check("rng/" + field, True, isinstance(trial["rng"][field], str) and bool(re.fullmatch(r"0|[1-9][0-9]*", trial["rng"][field])))
        check("rng/derivation", SEED_VERSION, trial["rng"]["seed_derivation_version"])
        check("rng/algorithm", "PCG64", trial["rng"]["rng_algorithm"])
        seed_values = [SEED_VERSION, trial["rng"]["seed"], trial["game"]["game_id_namespace"], trial["game"]["game_id"],
                       trial["trial_index"]]
        check("rng/trial_seed", str(int.from_bytes(hashlib.sha256(canonical(seed_values)).digest()[:8], "big")), trial["rng"]["trial_seed"])
        events = trial["events"]
        check("events_nonempty", True, bool(events))
        check("event_ids_unique", len(events), len({e["event_id"] for e in events}))
        check("event_order", list(range(len(events))), [e["event_seq"] for e in events])
        periods = list(dict.fromkeys(e["period_id"] for e in events))
        check("period_order", ["Q1", "Q2", "Q3", "Q4", "OT1"][:len(periods)], periods)
        prev = None
        elapsed = defaultdict(int)
        for e in events:
            check("event_id_namespace", f"{trial['trial_id']}/event/{e['event_seq']}", e["event_id"])
            check("possession_id_namespace", True, e["possession_id"].startswith(trial["trial_id"] + "/possession/"))
            integer(e["elapsed_clock_seconds"], "elapsed", 0)
            integer(e["pre_period_seconds_remaining"], "pre_clock", 0)
            integer(e["post_period_seconds_remaining"], "post_clock", 0)
            length = 900 if e["period_kind"] == "REG" else 600
            check(e["event_id"] + "/bounds", True, 0 <= e["post_period_seconds_remaining"] <= e["pre_period_seconds_remaining"] <= length)
            check(e["event_id"] + "/clock", e["elapsed_clock_seconds"], e["pre_period_seconds_remaining"] - e["post_period_seconds_remaining"])
            check(e["event_id"] + "/pre_clock_state", e["pre_period_seconds_remaining"], e["pre_state"]["period_seconds_remaining"])
            check(e["event_id"] + "/post_clock_state", e["post_period_seconds_remaining"], e["post_state"]["period_seconds_remaining"])
            check(e["event_id"] + "/period_kind", "REG" if e["period_id"].startswith("Q") else "OT", e["period_kind"])
            check(e["event_id"] + "/possession_pre", e["pre_state"]["possession"], e["pre_possession"])
            check(e["event_id"] + "/possession_post", e["post_state"]["possession"], e["post_possession"])
            for team in (trial["game"]["home_team_id"], trial["game"]["away_team_id"]):
                delta = e["post_state"]["score"][team] - e["pre_state"]["score"][team]
                check(e["event_id"] + "/score_delta/" + team, delta, e["score_delta"][team])
                check(e["event_id"] + "/score_credits/" + team, delta, e["team_credits"].get(team, zeros(TEAM_STATS))["points"])
            q = int(e["period_id"][1:]) if e["period_kind"] == "REG" else 5
            for side in ("pre", "post"):
                check(e["event_id"] + "/" + side + "_reg_clock", (4-q)*900 + e[f"{side}_period_seconds_remaining"] if q <= 4 else 0,
                      e[f"{side}_state"]["regulation_seconds_remaining"])
            if prev and prev["period_id"] == e["period_id"]:
                check(e["event_id"] + "/continuity", prev["post_state"], e["pre_state"])
            elif prev:
                check(e["event_id"] + "/previous_period_exhausted", 0, prev["post_period_seconds_remaining"])
                check(e["event_id"] + "/reset", length, e["pre_period_seconds_remaining"])
                check(e["event_id"] + "/boundary", "period_start", e["type"])
                for field in ("score", "down", "ydstogo", "yardline_100", "possession"):
                    check(e["event_id"] + "/boundary_state/" + field, prev["post_state"][field], e["pre_state"][field])
            else:
                check("opening_clock", 900, e["pre_period_seconds_remaining"])
                check("opening_score", dict.fromkeys((trial["game"]["home_team_id"], trial["game"]["away_team_id"]), 0), e["pre_state"]["score"])
            elapsed[e["period_id"]] += e["elapsed_clock_seconds"]
            prev = e
            check(e["event_id"] + "/features", trial["feature_availability"], e["feature_availability"])
            for stats in e["team_credits"].values():
                check(e["event_id"] + "/team_stat_keys", sorted(TEAM_STATS), sorted(stats))
                for stat, value in stats.items():
                    integer(value, stat, 0 if stat in TEAM_COUNTS or stat.startswith("unassigned_") and not stat.endswith("yards") or stat in {"points", "turnovers", "sack_loss_yards", "possession_seconds"} else None)
            for row in e["player_credits"]:
                for stat in PLAYER_STATS:
                    integer(row["stats"][stat], stat, 0 if stat in PLAYER_STATS[:5] else None)
            check(e["event_id"] + "/time_partition", e["elapsed_clock_seconds"],
                  sum(s["possession_seconds"] for s in e["team_credits"].values()) + e["unattributed_clock_seconds"])
            if e["type"] == "snap":
                trace = e["generation_trace"]
                check(e["event_id"] + "/causal_stages", ["PRE_SNAP", "OPPORTUNITY", "CATCH", "YARDS"], [r["generation_stage"] for r in trace])
                for field, value in e["pre_state"].items():
                    check(e["event_id"] + "/presnap_context/" + field, value, trace[0]["context"][field])
                for step in trace:
                    check(e["event_id"] + "/provenance/" + step["generation_stage"], True,
                          bool(step["provenance_refs"]) and bool(step["model_version"]) and "MODELED" in step["flags"])
                    check(e["event_id"] + "/sample_size_reason", True, step["sample_size"] is not None or bool(step["sample_size_reason"]))
                    check(e["event_id"] + "/provenance_resolves", True, set(step["provenance_refs"]) <= set(trial["provenance"]["input_refs"]))
                t, p, _ = allocate(e["terminal_category"], e["acting_team_id"], **e["assignments"])
                check(e["event_id"] + "/opportunity_allocation", t, trace[1]["team_counts"])
                check(e["event_id"] + "/opportunity_players", sorted(p.values(), key=player_key), sorted(trace[1]["player_counts"], key=player_key))
                final_players = {player_key(row): row for row in e["player_credits"]}
                check(e["event_id"] + "/player_keys_unique", len(e["player_credits"]), len(final_players))
                expected_players = {player_key(row): row for row in p.values()}
                for key in sorted(final_players.keys() | expected_players.keys()):
                    for stat in ("targets", "carries", "pass_attempts", "sacks_taken"):
                        check(e["event_id"] + "/player_opportunity/" + stat,
                              expected_players.get(key, {"stats": zeros(PLAYER_STATS)})["stats"][stat],
                              final_players.get(key, {"stats": zeros(PLAYER_STATS)})["stats"][stat])
                catch = trace[2]["outcome"]
                final_team = e["team_credits"][e["acting_team_id"]]
                check(e["event_id"] + "/catch_stage", int(catch == "COMPLETE"), final_team["completions"])
                receiver = e["assignments"]["receiver"]
                receiver_key = (e["acting_team_id"], receiver["player_id_namespace"], receiver["player_id"]) if receiver else None
                for key, row in final_players.items():
                    check(e["event_id"] + "/catch_recipient", int(catch == "COMPLETE" and key == receiver_key), row["stats"]["catches"])
                check(e["event_id"] + "/unassigned_catch", int(catch == "COMPLETE" and receiver_key is None), final_team["unassigned_catches"])
                realized = trace[3]["realized_yards"]
                integer(realized, "realized_yards")
                check(e["event_id"] + "/yard_stage/gross", realized if catch == "COMPLETE" else 0, final_team["gross_pass_yards"])
                check(e["event_id"] + "/yard_stage/rush", realized if e["terminal_category"] in RUSHES else 0, final_team["rush_yards"])
                check(e["event_id"] + "/yard_stage/sack", -realized if e["terminal_category"] == "sack" else 0, final_team["sack_loss_yards"])
                if (final_team["pass_receiving_credit_adjustment"] or
                        e["field_advance_yards"] != realized or trace[3]["raw_outcome"].get("receiving_credits")):
                    check(e["event_id"] + "/adjustment_evidence", True, bool(e["credit_adjustments"]))
                    for adjustment in e["credit_adjustments"]:
                        check(e["event_id"] + "/adjustment_event", e["event_id"], adjustment["event_id"])
                        check(e["event_id"] + "/adjustment_reason", True, bool(adjustment["explanation"]) and bool(adjustment["provenance_refs"]))
                        check(e["event_id"] + "/signed_adjustment", final_team["pass_receiving_credit_adjustment"], adjustment["signed_pass_receiving_adjustment"])
                for stat in ("unassigned_targets", "unassigned_carries", "unassigned_pass_attempts", "unassigned_sacks"):
                    check(e["event_id"] + "/residual_allocation/" + stat, t[stat], e["team_credits"][e["acting_team_id"]][stat])
                check(e["event_id"] + "/field_advance", e["field_advance_yards"], e["team_credits"][e["acting_team_id"]]["field_advance_yards"])
                for stat in TEAM_COUNTS:
                    if stat != "completions":
                        check(e["event_id"] + "/terminal/" + stat, t[stat], e["team_credits"][e["acting_team_id"]][stat])
                if e["terminal_category"] == "no_play":
                    check(e["event_id"] + "/no_play", zeros(TEAM_STATS), {**e["team_credits"][e["acting_team_id"]], "possession_seconds": 0})
        complete = trial["status"]["completion_reason"] != "final_max_steps"
        reason = trial["status"]["completion_reason"]
        check("termination_reason_supported", True, reason in {"regulation_complete", "ot_expiration_tie", "ot_first_score_approximation", "final_max_steps"})
        check("termination_event", "final" if complete else "final_max_steps", events[-1]["type"])
        terminal = events[-1]["post_state"]
        tied = len(set(terminal["score"].values())) == 1
        if reason == "regulation_complete":
            check("regulation_termination", ("Q4", 0, False), (terminal["period_id"], terminal["period_seconds_remaining"], tied))
        elif reason == "ot_expiration_tie":
            check("ot_expiration_termination", ("OT1", 0, True), (terminal["period_id"], terminal["period_seconds_remaining"], tied))
        elif reason == "ot_first_score_approximation":
            check("ot_score_termination", ("OT1", False), (terminal["period_id"], tied))
        check("completion_state", "COMPLETE" if complete else "INCOMPLETE", trial["status"]["state"] if trial["status"]["state"] != "INVALID" else "INVALID")
        check("terminal_state", events[-1]["post_state"], trial["status"]["terminal_state"])
        check("went_ot", "OT1" in periods, trial["status"]["went_ot"])
        if complete:
            for period in ("Q1", "Q2", "Q3", "Q4"):
                check("clock/" + period, 900, elapsed[period])
            check("regulation_clock", 3600, sum(elapsed[p] for p in ("Q1", "Q2", "Q3", "Q4")))
        else:
            check("cap_is_incomplete", "INCOMPLETE", trial["status"]["state"])
        roster = trial["provenance"]["roster"]
        expected = derive_tables(events, trial["game"], roster, periods, complete=complete)
        for name, value, actual in zip(("team_periods", "player_periods", "aggregates"), expected,
                                      (trial["team_periods"], trial["player_periods"], trial["aggregates"])):
            check(name + "/ledger_reconciliation", value, actual)
        rows = trial["team_periods"] + trial["aggregates"]["team"]
        prows = trial["player_periods"] + trial["aggregates"]["player"]
        for row in rows:
            if row.get("stats") is None:
                continue
            t = row["stats"]
            players = [p["stats"] for p in prows if p["team_id"] == row["team_id"] and p["period_id"] == row["period_id"]]
            def eq(name, left, right):
                check(f"{row['team_id']}/{row['period_id']}/{name}", left, right)
            eq("dropbacks", t["dropbacks"], t["dropback_pass_attempts"] + t["sacks"] + t["scrambles"] + t["aborted_dropbacks_no_attempt"])
            eq("pass_attempts", t["pass_attempts"], t["dropback_pass_attempts"] + t["non_dropback_pass_attempts"])
            eq("attempt_partition", t["pass_attempts"], t["eligible_target_attempts"] + t["throwaways"] + t["spikes"] + t["other_untargeted_attempts"])
            eq("rush_partition", t["rush_attempts"], t["designed_rushes"] + t["scrambles"] + t["kneels"] + t["credited_aborted_rushes"])
            for total, stat, residual in (("eligible_target_attempts", "targets", "targets"), ("completions", "catches", "catches"),
                ("rush_attempts", "carries", "carries"), ("pass_attempts", "pass_attempts", "pass_attempts"),
                ("sacks", "sacks_taken", "sacks"), ("gross_pass_yards", "pass_yards", "pass_yards"),
                ("receiving_yards", "rec_yards", "rec_yards"), ("rush_yards", "rush_yards", "rush_yards")):
                eq(total + "/players", t[total], sum(p[stat] for p in players) + t["unassigned_" + residual])
            eq("net_pass_yards", t["net_pass_yards"], t["gross_pass_yards"] - t["sack_loss_yards"])
            eq("pass_receive_credit", t["gross_pass_yards"], t["receiving_yards"] + t["pass_receiving_credit_adjustment"])
            eq("eligible_bounds", True, 0 <= t["completions"] <= t["eligible_target_attempts"] <= t["pass_attempts"])
            eq("unassigned_catch_bounds", True, 0 <= t["unassigned_catches"] <= t["unassigned_targets"])
            for p in players:
                eq("player_catch_bounds", True, 0 <= p["catches"] <= p["targets"])
        from joint_producer import missing_features, derive_possessions
        check("missing_features", missing_features(), trial["feature_availability"])
        check("possessions", derive_possessions(events), trial["possessions"])
        check("possession_ids_unique", len(trial["possessions"]), len({p["possession_id"] for p in trial["possessions"]}))
        check("ot_only_on_tie", True, not trial["status"]["went_ot"] or len({r["stats"]["points"] for r in trial["aggregates"]["team"] if r["period_id"] == "REG"}) == 1)
        final_points = {r["team_id"]: r["stats"]["points"] for r in trial["aggregates"]["team"] if r["period_id"] == "FG" and r["stats"] is not None}
        if complete:
            check("final_score", final_points, events[-1]["post_state"]["score"])
    except (KeyError, TypeError, ValueError, IndexError) as exc:
        check("schema_or_unsupported", "well-formed supported ledger", f"{type(exc).__name__}: {exc}")
    failed = [c["name"] for c in checks if not c["pass"]]
    return {"status": "INVALID" if failed else "PASS", "checks": checks, "failed_invariants": failed}


def finalize_validation(trial):
    trial["validation"] = validate_trial(trial)
    if trial["validation"]["status"] != "PASS":
        trial["status"]["state"] = "INVALID"
    residuals = any(any(row.get("stats", {}).get("unassigned_" + k, 0) != 0 for k in RESIDUALS)
                    for row in trial.get("team_periods", []))
    reasons = []
    if trial["status"]["state"] != "COMPLETE":
        reasons.append("TRIAL_" + trial["status"]["state"])
    if residuals:
        reasons.append("PLAYER_ID_UNRESOLVED")
    if "SCENARIO_ONLY" in trial["flags"]:
        reasons.append("SCENARIO_ONLY")
    trial["status"]["adapter_projection_allowed"] = not reasons
    trial["status"]["projection_blockers"] = reasons
    return trial
