"""NFL-83: phase execution receipts. Freshness is a prerequisite, never proof of execution.

Research only. These tests do not run the 100k engine, write a production database, or set projection_ready.
"""
import json
from datetime import datetime, timedelta, timezone

import pytest

from pipeline.execution import (
    CONTRACT_VERSION,
    ExecutionPolicyError,
    ReceiptStore,
    accept_stored_run,
    aggregate_status,
    claim_not_applicable,
    config_hash,
    content_hash,
    contract_document,
    contract_problems,
    mandatory_task_ids,
    render_slate,
    run_game,
    slate_summary,
    validate_receipt_schema,
    verify_receipt,
)
from pipeline.execution.runner import default_registry

GAME = "2026_10_WAS_NYG"
RUN = "run-1"
REV = "rev-test"
NOW = datetime(2026, 11, 12, 18, 0, tzinfo=timezone.utc)
AS_OF = "2026-11-12T17:00:00+00:00"


def _packet(roof="outdoors"):
    team = lambda: {
        "offense": {
            "players": [{"name": "qb"}],
            "by_game": [{"week": 1, "plays": 60}],
            "offense_snap_share": {"qb": 1.0},
            "produced": {"pts": 24},
        },
        "defense": {
            "allowed": {"dropbacks_charted": 30, "pts": 21, "sacks": 2, "qb_hits": 4},
            "rank": {"pts": 8},
            "defenders": [{"name": "cb"}],
        },
        "depth_chart": {"QB": ["qb"], "OL": ["lt"]},
        "injuries": {"official_report": [{"player": "wr"}], "espn_live": [{"player": "wr"}]},
    }
    weather = (
        {"status": "INDOOR"}
        if roof != "outdoors"
        else {"status": "OK", "rain": 0.0, "wind_mph": 5, "source_updated_at": AS_OF}
    )
    return {
        "game": {
            "game_id": GAME, "season": 2026, "week": 10, "away": "WAS", "home": "NYG",
            "date": "2026-11-12", "kickoff_et": "20:15", "site": "MetLife", "roof": roof,
            "listed_qbs": {"WAS": "a", "NYG": "b"}, "coaches": {"WAS": "c", "NYG": "d"},
        },
        "market": {"home_spread": -3.0, "total": 44.5},
        "generated_utc": AS_OF,
        "books": {"status": "OK", "retrieved_utc": AS_OF, "markets": {"spread": {"home": -3.0}}},
        "weather": weather,
        "team_projection": {"status": "RESEARCH_ONLY_NOT_VALIDATED"},
        "teams": {"WAS": team(), "NYG": team()},
        "sources": {"games": {"status": "OK", "source_updated_at": AS_OF}},
        "phase_ledger": [{"phase": n, "status": "AUTO", "detail": ""} for n in range(1, 16)],
        "projection_ready": False,
        "research_only": True,
    }


def _sources():
    names = []
    for phase in contract_document()["phases"]:
        for source in phase["freshness_sources"]:
            if source not in names:
                names.append(source)
    return names


def _fresh(status="FRESH", *, as_of=AS_OF, drop_as_of=False):
    rows = []
    for source in _sources():
        row = {"source": source, "status": status, "reason": status, "as_of_utc": as_of}
        if drop_as_of:
            row.pop("as_of_utc")
        if source == "weather" and status == "FRESH":
            row["status"] = "FRESH"
        rows.append(row)
    return rows


def _ok_registry(*, boom=None, empty=None, bad_game=None, bad_run=None, omit=()):
    reg = {}

    def make(task):
        task_id = task["task_id"]

        def fn(ctx):
            if boom == task_id:
                raise RuntimeError(f"boom {task_id}")
            game_id = "OTHER" if bad_game == task_id else ctx["game_id"]
            run_id = "OTHER-RUN" if bad_run == task_id else ctx["run_id"]
            if empty == task_id:
                return {"game_id": game_id, "run_id": run_id, "rows": [], "denominator": 1}
            denominator = 100000 if task_id.startswith("phase14.") else 1
            return {
                "game_id": game_id,
                "run_id": run_id,
                "rows": [{"task": task_id, "site": (ctx["packet"].get("game") or {}).get("site")}],
                "denominator": denominator,
                "warnings": [],
            }

        return fn

    for phase in contract_document()["phases"]:
        for task in phase["tasks"]:
            if task["task_id"] in omit:
                continue
            if task["mandatory"] or task["task_id"] in {boom, empty, bad_game, bad_run}:
                reg[task["task_id"]] = make(task)
    return reg


def _valid_body():
    return {"game_id": GAME, "run_id": RUN, "rows": [{"ok": 1}], "denominator": 1}


def valid_receipt(**overrides):
    body = _valid_body()
    rec = {
        "schema": "nfl83-execution-receipt/1",
        "contract_version": CONTRACT_VERSION,
        "game_id": GAME,
        "phase_id": 1,
        "run_id": RUN,
        "attempt": 1,
        "started_at": "2026-11-12T18:00:00+00:00",
        "finished_at": "2026-11-12T18:00:01+00:00",
        "status": "PASS",
        "evidence_class": "VALIDATED",
        "code_revision": REV,
        "config_hash": "sha256:" + "ab" * 32,
        "command": f"python -m pipeline.execution --game {GAME} --run-id {RUN} --phase 1",
        "entrypoint": "pipeline.execution:run_game",
        "inputs": [{
            "artifact_id": "src:schedule",
            "content_hash": content_hash({"source": "schedule"}),
            "source": "schedule",
            "provenance": "packet.sources.games publisher as-of",
            "as_of": AS_OF,
        }],
        "prerequisite": {
            "kind": "freshness",
            "evidence_class": "FRESH",
            "satisfies_execution": False,
            "rows": [],
        },
        "invocations": [{
            "task_id": "phase01.slate_schedule_venue",
            "module": "pipeline.execution.analytics",
            "function": "analyze_slate",
            "mandatory": True,
            "command": f"python -m pipeline.execution --game {GAME} --run-id {RUN} --phase 1 --task phase01.slate_schedule_venue",
            "started_at": "2026-11-12T18:00:00+00:00",
            "finished_at": "2026-11-12T18:00:01+00:00",
            "status": "PASS",
            "evidence_class": "VALIDATED",
        }],
        "outputs": [{
            "artifact_id": "phase01.slate_schedule_venue",
            "content_hash": content_hash(body),
            "row_count": 1,
            "denominator": 1,
            "body": body,
        }],
        "validation": {"passed": True, "checks": [{"name": "min_rows", "passed": True}]},
        "warnings": [],
        "failure": None,
        "not_applicable": None,
        "projection_ready": False,
        "research_only": True,
    }
    rec.update(overrides)
    return rec


def _run(tmp_path, **kw):
    store = kw.pop("store", None) or ReceiptStore(tmp_path / "receipts")
    args = dict(
        run_id=RUN, store=store, registry=None, freshness_rows=_fresh(),
        now=NOW, code_revision=REV,
    )
    args.update(kw)
    return run_game(_packet(kw.pop("roof", "outdoors")) if "packet" not in args else args.pop("packet"), **args)


# --- schema, provenance, hashes, status ---

def test_contract_covers_all_fifteen_phases_and_is_versioned():
    doc = contract_document()
    assert doc["contract_version"] == CONTRACT_VERSION
    assert doc["projection_ready"] is False and doc["research_only"] is True
    assert [p["phase_id"] for p in doc["phases"]] == list(range(1, 16))
    assert contract_problems(doc) == []
    for phase in doc["phases"]:
        mandatory = [t for t in phase["tasks"] if t["mandatory"]]
        assert mandatory, phase["phase_id"]
        for task in phase["tasks"]:
            assert task["task_id"] and task["binding"] in {"canonical", "absent", "source_unavailable", "unbound"}
            policy = task.get("not_applicable_when")
            if policy:
                assert policy["when"] == "indoor" and policy["allows_phase_pass"] is True
                assert policy["policy_id"] and policy["reason"].strip()
    phase14 = next(t for p in doc["phases"] if p["phase_id"] == 14 for t in p["tasks"])
    assert phase14["canonical_path"] == "tools/sim_v6.py"
    assert phase14["module"] != "pipeline.sim100k"


def test_content_hash_is_stable_and_detects_change():
    assert content_hash({"b": 1, "a": 2}) == content_hash({"a": 2, "b": 1})
    assert content_hash({"a": 1}) != content_hash({"a": 2})
    assert content_hash({"a": 1}).startswith("sha256:")
    assert content_hash({"a": 1.0}) == content_hash({"a": 1.0})
    with pytest.raises(ValueError):
        content_hash({"metric": float("nan")})
    with pytest.raises(ValueError):
        content_hash({"metric": float("inf")})
    assert config_hash() == config_hash(contract_document())
    assert config_hash().startswith("sha256:")


def test_receipt_schema_rejects_missing_fields_and_projection_ready():
    rec = valid_receipt()
    assert validate_receipt_schema(rec) == []
    broken = dict(rec)
    del broken["finished_at"]
    assert validate_receipt_schema(broken)
    assert validate_receipt_schema(valid_receipt(projection_ready=True))
    assert validate_receipt_schema(valid_receipt(research_only=False))
    assert validate_receipt_schema(valid_receipt(status="AUTO"))
    inputs = [dict(rec["inputs"][0])]
    del inputs[0]["provenance"]
    assert validate_receipt_schema(valid_receipt(inputs=inputs))
    inputs = [dict(rec["inputs"][0], provenance="  ")]
    assert validate_receipt_schema(valid_receipt(inputs=inputs))


def test_pass_receipt_requires_provenance_as_of_and_cannot_be_merely_fresh():
    assert verify_receipt(valid_receipt(), game_id=GAME, run_id=RUN, code_revision=REV,
                          config_hash=valid_receipt()["config_hash"]) == []
    fresh = valid_receipt(evidence_class="FRESH")
    assert verify_receipt(fresh, game_id=GAME, run_id=RUN, code_revision=REV, config_hash=fresh["config_hash"])
    discovered = valid_receipt(evidence_class="DISCOVERED")
    assert verify_receipt(discovered, game_id=GAME, run_id=RUN, code_revision=REV,
                          config_hash=discovered["config_hash"])
    sat = valid_receipt()
    sat["prerequisite"] = dict(sat["prerequisite"], satisfies_execution=True)
    assert verify_receipt(sat, game_id=GAME, run_id=RUN, code_revision=REV, config_hash=sat["config_hash"])
    missing_as_of = valid_receipt()
    missing_as_of["inputs"] = [dict(missing_as_of["inputs"][0], as_of=None)]
    assert verify_receipt(missing_as_of, game_id=GAME, run_id=RUN, code_revision=REV,
                          config_hash=missing_as_of["config_hash"])


def test_status_transitions_keep_freshness_out_of_pass():
    mandatory_pass = {"mandatory": True, "status": "PASS", "allows_phase_pass": True}
    assert aggregate_status("FRESH", [mandatory_pass]) == "PASS"
    assert aggregate_status("DISCOVERED", [mandatory_pass]) == "BLOCKED"
    assert aggregate_status("STALE", [mandatory_pass]) == "STALE"
    assert aggregate_status("NOT_YET", [mandatory_pass]) == "NOT_YET"
    assert aggregate_status("MISSING", [mandatory_pass]) == "MISSING"
    assert aggregate_status("GAP", [mandatory_pass]) == "BLOCKED"
    assert aggregate_status("FRESH", [{"mandatory": True, "status": "FAILED", "allows_phase_pass": True}]) == "FAILED"
    assert aggregate_status("FRESH", [mandatory_pass, {"mandatory": False, "status": "FAILED", "allows_phase_pass": True}]) == "PARTIAL"
    assert aggregate_status("FRESH", [{"mandatory": True, "status": "NOT_APPLICABLE", "allows_phase_pass": False}]) == "NOT_APPLICABLE"
    mixed = [
        {"mandatory": True, "status": "NOT_APPLICABLE", "allows_phase_pass": False},
        mandatory_pass,
    ]
    assert aggregate_status("FRESH", mixed) == "FAILED"
    indoor = [
        mandatory_pass,
        {"mandatory": True, "status": "NOT_APPLICABLE", "allows_phase_pass": True},
    ]
    assert aggregate_status("FRESH", indoor) == "PASS"
    assert aggregate_status("FRESH", [{"mandatory": True, "status": "NOT_APPLICABLE", "allows_phase_pass": True}]) == "NOT_APPLICABLE"


def test_not_applicable_requires_policy_and_reason():
    with pytest.raises(ExecutionPolicyError):
        claim_not_applicable({"task_id": "x", "not_applicable_when": None}, "because")
    indoor = {"policy_id": "indoor-roof-weather", "reason": "dome", "when": "indoor", "allows_phase_pass": True}
    with pytest.raises(ExecutionPolicyError):
        claim_not_applicable({"task_id": "x", "not_applicable_when": indoor}, "   ")
    waived = {"policy_id": "routes-not-in-public-ngs", "reason": "no routes", "when": "always", "allows_phase_pass": True}
    with pytest.raises(ExecutionPolicyError):
        claim_not_applicable({"task_id": "phase04.routes_participation", "not_applicable_when": waived},
                             "Public NGS does not carry routes.")
    rec = claim_not_applicable({"task_id": "phase12.weather_adjust", "not_applicable_when": indoor},
                               "Roof is indoor, so the measured rain adjustment does not apply.")
    assert rec["status"] == "NOT_APPLICABLE"
    assert rec["policy_id"] == "indoor-roof-weather"
    assert rec["satisfies_execution"] is False
    bare = valid_receipt(status="NOT_APPLICABLE", evidence_class=None, not_applicable=None, invocations=[], outputs=[])
    assert validate_receipt_schema(bare)


# --- runner: invocation, fail closed, retries ---

def test_default_phase_invokes_the_rain_equation_not_a_count(tmp_path):
    res = run_game(_packet(), run_id=RUN, store=ReceiptStore(tmp_path / "r"), registry=None,
                   freshness_rows=_fresh(), now=NOW, code_revision=REV, phases=[12])
    phase = res["phases"][0]
    body = phase["outputs"][0]["body"]
    assert phase["status"] == "PASS"
    assert phase["evidence_class"] == "VALIDATED"
    assert phase["invocations"][0]["module"] == "pregame.rain_model"
    assert phase["invocations"][0]["function"] == "factor"
    assert body["equation_id"] == "pregame.rain_model.factor"
    assert body["module_id"] == "pregame.rain_model"
    import math
    from pregame.rain_model import coefficients, factor
    meta = coefficients()["_meta"]
    assert body["metrics"]["attempts_factor"] == factor("attempts", 0.0, 5.0)
    assert math.isfinite(body["metrics"]["attempts_factor"])
    assert body["denominator"] == int(meta["team_games"])
    assert body["denominator"] > 1
    assert "team-games" in body["provenance"]
    assert phase["prerequisite"]["satisfies_execution"] is False
    assert phase["prerequisite"]["evidence_class"] == "FRESH"
    assert phase["projection_ready"] is False and res["projection_ready"] is False
    assert res["research_only"] is True


def test_freshness_alone_does_not_pass_when_modules_are_not_invoked(tmp_path):
    res = run_game(_packet(), run_id=RUN, store=ReceiptStore(tmp_path / "r"), registry={},
                   freshness_rows=_fresh(), now=NOW, code_revision=REV, phases=[12])
    phase = res["phases"][0]
    assert phase["status"] == "FAILED"
    assert phase["failure"]["code"] == "NOT_INVOKED"
    assert phase["evidence_class"] != "VALIDATED"
    assert phase["prerequisite"]["evidence_class"] == "FRESH"
    assert phase["prerequisite"]["satisfies_execution"] is False
    assert res["accepted"] is False


def test_discovered_packet_is_not_execution(tmp_path):
    res = run_game(_packet(), run_id=RUN, store=ReceiptStore(tmp_path / "r"), registry=_ok_registry(),
                   now=NOW, code_revision=REV, phases=[1], discover_only=True)
    phase = res["phases"][0]
    assert phase["status"] == "BLOCKED"
    assert phase["failure"]["code"] == "DISCOVERED_NOT_EXECUTED"
    assert phase["prerequisite"]["evidence_class"] == "DISCOVERED"
    assert phase["invocations"] == []
    assert res["accepted"] is False


def test_all_fifteen_fresh_but_one_module_not_invoked_fails(tmp_path):
    skipped = "phase12.weather_adjust"
    assert skipped in mandatory_task_ids()
    res = _run(tmp_path, skip_tasks={skipped})
    assert res["accepted"] is False
    assert res["status"] == "FAILED"
    phase = next(p for p in res["phases"] if p["phase_id"] == 12)
    assert phase["status"] == "FAILED"
    assert phase["failure"]["code"] == "NOT_INVOKED"
    assert phase["prerequisite"]["evidence_class"] == "FRESH"
    assert all(p["status"] != "PASS" for p in res["phases"])
    assert skipped not in {i["task_id"] for p in res["phases"] for i in p["invocations"]}


def test_real_equation_validates_and_absent_modules_stay_blocked(tmp_path):
    res = _run(tmp_path)
    assert res["accepted"] is False
    weather = next(p for p in res["phases"] if p["phase_id"] == 12)
    assert weather["status"] == "PASS"
    assert verify_receipt(weather, game_id=GAME, run_id=RUN, code_revision=REV, config_hash=config_hash()) == []
    assert weather["outputs"][0]["body"]["equation_id"] == "pregame.rain_model.factor"
    for phase in res["phases"]:
        assert phase["projection_ready"] is False
        if phase["phase_id"] == 12:
            continue
        assert phase["status"] == "BLOCKED"
        assert phase["failure"]["code"] in {"MODULE_ABSENT", "SOURCE_UNAVAILABLE", "UNBOUND", "ANALYTIC_INPUT_ABSENT"}
        assert phase["blocked_tasks"]
        assert all(task["satisfies_execution"] is False for task in phase["blocked_tasks"])


def test_count_only_output_and_absent_module_cannot_pass(tmp_path, monkeypatch):
    import pipeline.sim100k as sim

    def boom(*_a, **_k):
        raise AssertionError("sim100k.run must not be called")

    monkeypatch.setattr(sim, "run", boom)

    def counts(ctx):
        return {"game_id": ctx["game_id"], "run_id": ctx["run_id"], "rows": [{"players": 3}], "denominator": 1,
                "metrics": {"players": 3}}

    counted = run_game(_packet(), run_id=RUN, store=ReceiptStore(tmp_path / "count"), registry={"phase12.weather_adjust": counts},
                       freshness_rows=_fresh(), now=NOW, code_revision=REV, phases=[12])
    assert counted["phases"][0]["status"] == "FAILED"
    assert counted["phases"][0]["failure"]["code"] in {"COUNT_ONLY", "ANALYTIC_OUTPUT_MISSING"}

    def rich(ctx):
        return {"game_id": ctx["game_id"], "run_id": ctx["run_id"], "equation_id": "tools.sim_v6.run",
                "module_id": "tools.sim_v6", "metrics": {"median": 1.0}, "denominator": 100000,
                "provenance": "placeholder", "rows": [{"median": 1.0}]}

    absent = run_game(_packet(), run_id=RUN, store=ReceiptStore(tmp_path / "absent"), registry={"phase14.sim_v6": rich},
                      freshness_rows=_fresh(), now=NOW, code_revision=REV, phases=[14])
    assert absent["phases"][0]["status"] == "BLOCKED"
    assert absent["phases"][0]["failure"]["code"] == "MODULE_ABSENT"
    assert "tools/sim_v6.py" in absent["phases"][0]["failure"]["message"]
    assert "pipeline.sim100k" in absent["phases"][0]["failure"]["message"]
    assert absent["phases"][0]["invocations"] == []

    shell = _run(tmp_path / "shell", phases=[7])
    assert shell["phases"][0]["status"] == "BLOCKED"
    assert shell["phases"][0]["failure"]["code"] == "SOURCE_UNAVAILABLE"
    assert shell["phases"][0]["status"] != "NOT_APPLICABLE"
    script = _run(tmp_path / "script", phases=[6])
    assert script["phases"][0]["status"] == "BLOCKED"
    assert script["phases"][0]["failure"]["code"] == "MODULE_ABSENT"
    assert "NOT_APPLICABLE" not in script["phases"][0]["failure"]["code"]


def test_module_throw_empty_output_and_id_mismatches(tmp_path):
    boom = _run(tmp_path / "boom", registry=_ok_registry(boom="phase12.weather_adjust"), phases=[12])
    assert boom["phases"][0]["status"] == "FAILED"
    assert boom["phases"][0]["failure"]["code"] == "TASK_RAISED"
    assert boom["phases"][0]["evidence_class"] == "EXECUTED"

    empty = _run(tmp_path / "empty", registry=_ok_registry(empty="phase12.weather_adjust"), phases=[12])
    assert empty["phases"][0]["failure"]["code"] == "EMPTY_OUTPUT"

    bad_game = _run(tmp_path / "game", registry=_ok_registry(bad_game="phase12.weather_adjust"), phases=[12])
    assert bad_game["phases"][0]["failure"]["code"] == "GAME_MISMATCH"

    bad_run = _run(tmp_path / "run", registry=_ok_registry(bad_run="phase12.weather_adjust"), phases=[12])
    assert bad_run["phases"][0]["failure"]["code"] == "RUN_MISMATCH"


def test_stale_inputs_block_execution(tmp_path):
    res = _run(tmp_path, freshness_rows=_fresh("STALE"), phases=[1])
    phase = res["phases"][0]
    assert phase["status"] == "STALE"
    assert phase["failure"]["code"] == "STALE_INPUT"
    assert phase["invocations"] == []
    assert phase["evidence_class"] != "VALIDATED"
    assert res["accepted"] is False


def test_missing_as_of_on_fresh_input_fails_provenance(tmp_path):
    res = _run(tmp_path, freshness_rows=_fresh(drop_as_of=True), phases=[1])
    assert res["phases"][0]["status"] == "FAILED"
    assert res["phases"][0]["failure"]["code"] == "PROVENANCE"


def test_hash_tamper_wrong_game_wrong_run_stale_code_and_config(tmp_path):
    res = _run(tmp_path, phases=[12])
    receipt = json.loads(json.dumps(res["phases"][0]))
    receipt["outputs"][0]["content_hash"] = "sha256:" + "00" * 32
    reasons = verify_receipt(receipt, game_id=GAME, run_id=RUN, code_revision=REV, config_hash=config_hash())
    assert any("HASH_MISMATCH" in r for r in reasons)
    assert verify_receipt(res["phases"][0], game_id="nope", run_id=RUN, code_revision=REV, config_hash=config_hash())
    assert verify_receipt(res["phases"][0], game_id=GAME, run_id="nope", code_revision=REV, config_hash=config_hash())
    assert verify_receipt(res["phases"][0], game_id=GAME, run_id=RUN, code_revision="other", config_hash=config_hash())
    assert verify_receipt(res["phases"][0], game_id=GAME, run_id=RUN, code_revision=REV, config_hash="sha256:" + "ff" * 32)


def test_retries_are_idempotent_and_keep_failed_attempts(tmp_path):
    store = ReceiptStore(tmp_path / "r")
    first = run_game(_packet(), run_id=RUN, store=store, registry=_ok_registry(boom="phase12.weather_adjust"),
                     freshness_rows=_fresh(), now=NOW, code_revision=REV, phases=[12])
    assert first["phases"][0]["status"] == "FAILED"
    assert first["phases"][0]["attempt"] == 1
    second = run_game(_packet(), run_id=RUN, store=store, registry=None,
                      freshness_rows=_fresh(), now=NOW + timedelta(seconds=5), code_revision=REV, phases=[12])
    assert second["phases"][0]["status"] == "PASS"
    assert second["phases"][0]["attempt"] == 2
    attempts = store.attempts(GAME, RUN, 12)
    assert [a["status"] for a in attempts] == ["FAILED", "PASS"]
    third = run_game(_packet(), run_id=RUN, store=store, registry=None,
                     freshness_rows=_fresh(), now=NOW + timedelta(seconds=9), code_revision=REV, phases=[12])
    assert third["replayed_phases"] == [12]
    assert len(store.attempts(GAME, RUN, 12)) == 2
    with pytest.raises(FileExistsError):
        store.write_new(attempts[0])


def test_orchestrator_fails_closed_on_missing_and_malformed_receipts(tmp_path):
    store = ReceiptStore(tmp_path / "r")
    missing = accept_stored_run(store, GAME, RUN, code_revision=REV, config_hash=config_hash())
    assert missing["accepted"] is False
    assert any("MISSING" in r for r in missing["reasons"])
    res = _run(tmp_path, store=store, phases=[12])
    ok = accept_stored_run(store, GAME, RUN, code_revision=REV, config_hash=config_hash(), phases=[12])
    assert ok["accepted"] is True and res["accepted"] is True
    path = store.path_for(res["phases"][0])
    blob = json.loads(path.read_text())
    del blob["finished_at"]
    path.write_text(json.dumps(blob))
    bad = accept_stored_run(store, GAME, RUN, code_revision=REV, config_hash=config_hash(), phases=[12])
    assert bad["accepted"] is False
    assert any("MALFORMED" in r for r in bad["reasons"])


def test_indoor_weather_not_applicable_is_explicit_and_outdoor_still_runs(tmp_path):
    indoor_rows = _fresh()
    for row in indoor_rows:
        if row["source"] == "weather":
            row["status"] = "NOT_REQUIRED"
            row["reason"] = "Indoor game."
    indoor = run_game(_packet("dome"), run_id=RUN, store=ReceiptStore(tmp_path / "in"), registry=None,
                      freshness_rows=indoor_rows, now=NOW, code_revision=REV, phases=[12])
    phase = indoor["phases"][0]
    assert phase["status"] == "NOT_APPLICABLE"
    assert indoor["accepted"] is False
    na = phase["tasks_not_applicable"]
    assert any(t["task_id"] == "phase12.weather_adjust" and t["policy_id"] == "indoor-roof-weather" and t["reason"].strip()
               for t in na)
    assert phase["invocations"] == []
    assert phase["not_applicable"]["policy_id"] == "indoor-roof-weather"

    outdoor = _run(tmp_path / "out", phases=[12])
    assert outdoor["phases"][0]["status"] == "PASS"
    assert {i["task_id"] for i in outdoor["phases"][0]["invocations"]} == {"phase12.weather_adjust"}
    assert outdoor["phases"][0]["tasks_not_applicable"] == []


def test_routes_source_gap_blocks_the_phase(tmp_path):
    res = _run(tmp_path, phases=[4])
    phase = res["phases"][0]
    assert phase["status"] == "BLOCKED"
    assert phase["status"] not in {"PASS", "NOT_APPLICABLE", "PARTIAL"}
    assert any(task["task_id"] == "phase04.routes_participation" and task["code"] == "SOURCE_UNAVAILABLE"
               for task in phase["blocked_tasks"])
    assert res["accepted"] is False


def test_default_binding_does_not_call_sim100k_or_flip_projection_ready(tmp_path, monkeypatch):
    import pipeline.sim100k as sim

    def boom(*_a, **_k):
        raise AssertionError("sim100k.run must not be called by the receipt layer")

    monkeypatch.setattr(sim, "run", boom)
    monkeypatch.setattr(sim, "preflight", boom)
    res = run_game(_packet(), run_id=RUN, store=ReceiptStore(tmp_path / "r"), registry=default_registry(),
                   freshness_rows=_fresh(), now=NOW, code_revision=REV, phases=[14])
    assert res["phases"][0]["status"] == "BLOCKED"
    assert res["projection_ready"] is False
    assert res["accepted"] is False
    assert "tools/sim_v6.py" in res["phases"][0]["failure"]["message"]
    assert "pipeline.sim100k" in res["phases"][0]["failure"]["message"]


def test_slate_separates_executed_from_merely_available_and_flags_partial(tmp_path):
    executed = _run(tmp_path / "ok", run_id="run-pass")
    available = run_game(_packet(), run_id="run-avail", store=ReceiptStore(tmp_path / "avail"), registry={},
                         freshness_rows=_fresh(), now=NOW, code_revision=REV)
    partial = {
        "game_id": GAME, "run_id": "run-part", "status": "PARTIAL",
        "phases": [{"phase_id": 4, "status": "PARTIAL", "evidence_class": "EXECUTED",
                    "prerequisite": {"evidence_class": "FRESH"}}],
    }
    summary = slate_summary([executed, available, partial])
    by_id = {g["game_id"] + g["run_id"]: g for g in summary["games"]}
    assert by_id[GAME + "run-pass"]["executed_phases"] == [12]
    assert by_id[GAME + "run-avail"]["executed_phases"] == []
    assert 12 in by_id[GAME + "run-avail"]["available_only_phases"]
    assert 6 in by_id[GAME + "run-avail"]["available_only_phases"]
    assert GAME in summary["refused_games"]
    partial_game = next(g for g in summary["games"] if g["run_id"] == "run-part" and 4 in g["partial_phases"])
    assert partial_game["game_id"] in summary["partial_games"]
    text = render_slate(summary)
    assert "Executed" in text and "Merely available" in text
    assert "PARTIAL GAMES" in text and "REFUSED GAMES" in text
    assert "projection_ready is false" in text


def test_cli_strict_fails_closed_when_the_mandatory_task_is_skipped(tmp_path):
    from pipeline.execution.__main__ import main

    packet_path = tmp_path / "packet.json"
    packet_path.write_text(json.dumps(_packet()))
    fresh_path = tmp_path / "fresh.json"
    fresh_path.write_text(json.dumps(_fresh()))
    code = main([
        "--game", GAME, "--packet", str(packet_path), "--run-id", RUN,
        "--receipt-dir", str(tmp_path / "rec"), "--code-revision", REV,
        "--freshness-json", str(fresh_path), "--phase", "12", "--strict",
        "--skip-task", "phase12.weather_adjust",
    ])
    assert code == 3


def test_cli_exits_zero_only_when_the_run_is_accepted(tmp_path):
    from pipeline.execution.__main__ import main

    packet_path = tmp_path / "packet.json"
    packet_path.write_text(json.dumps(_packet()))
    fresh_path = tmp_path / "fresh.json"
    fresh_path.write_text(json.dumps(_fresh()))
    refused = main([
        "--game", GAME, "--packet", str(packet_path), "--run-id", RUN,
        "--receipt-dir", str(tmp_path / "refused"), "--code-revision", REV,
        "--freshness-json", str(fresh_path), "--phase", "12",
        "--skip-task", "phase12.weather_adjust",
    ])
    assert refused == 3
    accepted = main([
        "--game", GAME, "--packet", str(packet_path), "--run-id", RUN + "-ok",
        "--receipt-dir", str(tmp_path / "accepted"), "--code-revision", REV,
        "--freshness-json", str(fresh_path), "--phase", "12",
    ])
    assert accepted == 0


def _rain_body(**changes):
    body = {
        "game_id": GAME, "run_id": RUN,
        "equation_id": "pregame.rain_model.factor", "module_id": "pregame.rain_model",
        "metrics": {"attempts_factor": 1.0}, "denominator": 100, "provenance": "rain_effects.json",
        "rows": [{"attempts_factor": 1.0}],
    }
    body.update(changes)
    return body


def test_required_metrics_must_be_finite_and_denominator_a_positive_int(tmp_path):
    cases = [
        ({"metrics": {}}, "COUNT_ONLY"),
        ({"metrics": {"attempts_factor": "1"}}, "ANALYTIC_OUTPUT_MISSING"),
        ({"metrics": {"attempts_factor": True}}, "ANALYTIC_OUTPUT_MISSING"),
        ({"metrics": {"attempts_factor": float("nan")}}, "ANALYTIC_OUTPUT_MISSING"),
        ({"metrics": {"attempts_factor": float("inf")}}, "ANALYTIC_OUTPUT_MISSING"),
        ({"metrics": {"attempts_factor": float("-inf")}}, "ANALYTIC_OUTPUT_MISSING"),
        ({"denominator": 0}, "DENOMINATOR"),
        ({"denominator": -3}, "DENOMINATOR"),
        ({"denominator": True}, "DENOMINATOR"),
        ({"denominator": 1.5}, "DENOMINATOR"),
    ]
    for change, code in cases:
        payload = _rain_body(**change)
        def respond(ctx, payload=payload):
            return payload
        res = run_game(_packet(), run_id=RUN, store=ReceiptStore(tmp_path / code / str(abs(hash(str(change))))),
                       registry={"phase12.weather_adjust": respond}, freshness_rows=_fresh(), now=NOW,
                       code_revision=REV, phases=[12])
        assert res["phases"][0]["status"] == "FAILED", change
        assert res["phases"][0]["failure"]["code"] == code, change


def test_feature_table_is_not_an_opportunity_pass(tmp_path, monkeypatch):
    import sys
    import types
    fake = types.ModuleType("core.possession_engine_v0.opportunity")
    seen = {}

    def load_opp_lookup(path, game_ids):
        seen["path"] = path
        seen["game_ids"] = list(game_ids)
        return {"WR|deep": {"a": 1, "b": 2}, "RB|rz": {"c": 3}}

    fake.load_opp_lookup = load_opp_lookup
    monkeypatch.setitem(sys.modules, "core.possession_engine_v0.opportunity", fake)
    packet = _packet()
    packet["opportunity_inputs"] = {"pbp_path": "asof.parquet", "game_ids": ["2026_10_WAS_NYG"]}
    res = run_game(packet, run_id=RUN, store=ReceiptStore(tmp_path / "opp"), registry=None,
                   freshness_rows=_fresh(), now=NOW, code_revision=REV, phases=[4])
    phase = res["phases"][0]
    assert seen["path"] == "asof.parquet"
    assert phase["status"] != "PASS"
    opp = next(task for task in phase["blocked_tasks"] if task["task_id"] == "phase04.opportunity")
    assert opp["code"] == "ANALYTIC_OUTPUT_MISSING"
    assert "feature" in opp["message"].lower()
    routes = next(task for task in phase["blocked_tasks"] if task["task_id"] == "phase04.routes_participation")
    assert routes["code"] == "SOURCE_UNAVAILABLE"


def test_baseline_does_not_invent_an_opponent_factor(tmp_path, monkeypatch):
    import sys
    import types
    fake = types.ModuleType("pregame.packet")

    def player_baselines(*_a, **_k):
        return {"method": "test baseline", "players": [
            {"player": "A", "pos": "WR", "receiving_yards": {"weighted_mean": 40.0, "games": 9}},
            {"player": "B", "pos": "RB", "rushing_yards": {
                "weighted_mean": 55.0, "opponent_factor": 1.04, "games": 6,
            }},
        ]}

    fake.player_baselines = player_baselines
    monkeypatch.setitem(sys.modules, "pregame.packet", fake)
    packet = _packet()
    packet["baseline_inputs"] = {"off_players": {"receivers": [], "rushers": [], "quarterbacks": []}}
    res = run_game(packet, run_id=RUN, store=ReceiptStore(tmp_path / "base-ok"), registry=None,
                   freshness_rows=_fresh(), now=NOW, code_revision=REV, phases=[5])
    phase = res["phases"][0]
    assert phase["status"] == "PASS"
    row = phase["outputs"][0]["body"]["rows"][0]
    assert row["player"] == "B" and row["stat"] == "rushing_yards"
    assert row["opponent_factor"] == 1.04
    assert phase["outputs"][0]["body"]["denominator"] == 6
    assert phase["outputs"][0]["body"]["metrics"]["weighted_mean"] == 55.0

    def missing_factor(*_a, **_k):
        return {"players": [{"player": "A", "pos": "WR", "receiving_yards": {"weighted_mean": 40.0, "games": 9}}]}

    fake.player_baselines = missing_factor
    missing = run_game(packet, run_id="run-miss", store=ReceiptStore(tmp_path / "base-miss"), registry=None,
                       freshness_rows=_fresh(), now=NOW, code_revision=REV, phases=[5])
    assert missing["phases"][0]["status"] == "BLOCKED"
    assert missing["phases"][0]["failure"]["code"] == "ANALYTIC_OUTPUT_MISSING"
    assert "1.0" in missing["phases"][0]["failure"]["message"]

    def zero_games(*_a, **_k):
        return {"players": [{"player": "A", "pos": "WR", "receiving_yards": {
            "weighted_mean": 40.0, "opponent_factor": 1.1, "games": 0,
        }}]}

    fake.player_baselines = zero_games
    zero = run_game(packet, run_id="run-zero", store=ReceiptStore(tmp_path / "base-zero"), registry=None,
                    freshness_rows=_fresh(), now=NOW, code_revision=REV, phases=[5])
    assert zero["phases"][0]["status"] == "BLOCKED"
    assert zero["phases"][0]["failure"]["code"] == "ANALYTIC_OUTPUT_MISSING"


def test_existing_freshness_ledger_is_unchanged_and_not_execution():
    """The NFL-56 checker still reports input freshness. AUTO is not an execution receipt."""
    from pipeline import phases as phases

    now = datetime(2026, 11, 13, 1, 15, tzinfo=timezone.utc) - timedelta(hours=30)
    stamp = now - timedelta(minutes=5)
    src = {k: {"status": "OK", "retrieved_utc": stamp.isoformat(), "source_updated_at": stamp.isoformat()} for k in
           ("games", "pbp", "rosters", "depth_charts", "snap_counts", "ftn", "pfr_def", "injuries",
            "ngs_passing", "ngs_receiving", "ngs_rushing")}
    src["espn_injuries"] = {"status": "OK", "retrieved_utc": stamp.isoformat()}
    team = {"offense": {"players": [{"name": "x"}], "by_game": [1], "offense_snap_share": {"x": 1}, "produced": {"pts": 1}},
            "defense": {"allowed": {"dropbacks_charted": 30, "pts": 1}, "rank": {"pts": 1}, "defenders": [{"n": "d"}]},
            "depth_chart": {"QB": ["x"]},
            "injuries": {"official_report": [{"p": "y"}], "espn_live": [{"p": "y"}]}}
    packet = {
        "game": {"game_id": GAME, "season": 2026, "week": 10, "away": "WAS", "home": "NYG", "date": "2026-11-12",
                 "kickoff_et": "20:15", "site": "Home", "roof": "outdoors", "listed_qbs": {"WAS": "a", "NYG": "b"},
                 "coaches": {"WAS": "c"}},
        "market": {"home_spread": 3.0, "total": 44.5}, "generated_utc": stamp.isoformat(),
        "books": {"status": "OK", "retrieved_utc": stamp.isoformat(), "markets": {"spread": {}}},
        "weather": {"status": "OK", "retrieved_utc": stamp.isoformat(), "source_updated_at": stamp.isoformat(),
                    "kickoff_utc": datetime(2026, 11, 13, 1, 15, tzinfo=timezone.utc).isoformat()},
        "teams": {"WAS": team, "NYG": team}, "team_projection": {"status": "RESEARCH_ONLY_NOT_VALIDATED"},
        "sources": src, "phase_ledger": [{"phase": n, "status": "AUTO", "detail": ""} for n in range(1, 16)],
    }
    led = phases.ledger(packet, now, phases=[1], gate={"ran": False, "reasons": ["not this test"]})
    assert led["schema"] == "nfl56-phase-ledger/1"
    assert led["projection_ready"] is False and led["research_only"] is True
    assert led["phases"][0]["status"] == "AUTO"
    assert "evidence_class" not in led["phases"][0]
