"""Per-game fan-out (NFL-87). Research only. These tests do not set projection_ready."""
from __future__ import annotations

import json
import threading
import time
from pathlib import Path

from pipeline.orchestrator import ModuleResult, ModuleSpec, default_registry, run_games
from pipeline.orchestrator.runner import main as orchestrator_main


AS_OF = "2026-11-27T16:00:00Z"
REV = "testdeadbeef"


def _game(gid="2026_12_DEN_PIT", away="DEN", home="PIT", **extra):
    pkt = {"game": {"game_id": gid, "away": away, "home": home, "season": 2026, "week": 12,
                    "date": "2026-11-27", "kickoff_et": "15:00"}}
    pkt.update(extra)
    return {"game_id": gid, "packet": pkt}


def _run(tmp_path, games, registry, **kw):
    kw.setdefault("as_of", AS_OF)
    kw.setdefault("code_revision", REV)
    kw.setdefault("command", "python -m pipeline.orchestrator --game TEST --as-of " + AS_OF)
    return run_games(games, registry=registry, out_dir=tmp_path, **kw)


def _mod(gid, manifest):
    game = next(g for g in manifest["games"] if g["game_id"] == gid)
    return {m["module_id"]: m for m in game["modules"]}, game


def test_independent_modules_run_concurrently(tmp_path):
    barrier = threading.Barrier(3, timeout=2)
    order = []
    lock = threading.Lock()

    def make(name):
        def fn(call):
            with lock:
                order.append((name, "start"))
            barrier.wait()
            with lock:
                order.append((name, "end"))
            return ModuleResult(status="PASS", output={"module": name})
        return fn

    registry = [
        ModuleSpec(module_id=name, execution_class="analytical", fn=make(name), timeout_sec=3, retries=0,
                   output_contract="name", inputs=("game.game_id",))
        for name in ("alpha", "beta", "gamma")
    ]
    manifest = _run(tmp_path, [_game()], registry)
    starts = [i for i, (_name, phase) in enumerate(order) if phase == "start"]
    ends = [i for i, (_name, phase) in enumerate(order) if phase == "end"]
    assert starts and ends
    assert max(starts) < min(ends)
    mods, game = _mod("2026_12_DEN_PIT", manifest)
    assert [m for m in game["modules"]] == sorted(game["modules"], key=lambda m: m["module_id"])
    assert set(mods) == {"alpha", "beta", "gamma"}


def test_game_contexts_and_artifacts_stay_isolated(tmp_path):
    shared = {"seen": []}

    def fn(call):
        call.context["seen"].append(call.game_id)
        (call.artifact_dir / "who.txt").write_text(call.game_id)
        return ModuleResult(status="PASS", output={"seen": list(call.context["seen"])})

    registry = [ModuleSpec("worker", "analytical", fn, output_contract="seen", inputs=("game.game_id",))]
    games = [
        {**_game("2026_12_AAA_BBB", "AAA", "BBB"), "context": shared},
        {**_game("2026_12_CCC_DDD", "CCC", "DDD"), "context": shared},
    ]
    manifest = _run(tmp_path, games, registry)
    assert shared["seen"] == []
    dirs = set()
    for gid in ("2026_12_AAA_BBB", "2026_12_CCC_DDD"):
        mods, game = _mod(gid, manifest)
        assert mods["worker"]["output"]["seen"] == [gid]
        who = Path(game["artifact_dir"]) / "modules" / "worker" / "who.txt"
        assert who.read_text() == gid
        dirs.add(game["artifact_dir"])
        assert gid in game["artifact_dir"]
    assert len(dirs) == 2


def test_one_game_failure_does_not_drop_the_other_game(tmp_path):
    def fn(call):
        if call.game_id.endswith("BAD"):
            raise RuntimeError("identity exploded")
        return ModuleResult(status="PASS", output={"ok": call.game_id})

    registry = [ModuleSpec("identity", "adapter", fn, critical=True, retries=0, output_contract="ok",
                           inputs=("game.game_id",))]
    manifest = _run(tmp_path, [_game("2026_12_BAD_BAD", "BAD", "BAD"), _game("2026_12_GOOD_OK", "GOOD", "OK")], registry)
    ids = [g["game_id"] for g in manifest["games"]]
    assert ids == ["2026_12_BAD_BAD", "2026_12_GOOD_OK"]
    bad_mods, bad = _mod("2026_12_BAD_BAD", manifest)
    good_mods, good = _mod("2026_12_GOOD_OK", manifest)
    assert bad["status"] == "FAIL_CLOSED"
    assert "identity exploded" in json.dumps(bad_mods["identity"]["attempts"])
    assert good["status"] == "COMPLETE"
    assert good_mods["identity"]["output"]["ok"] == "2026_12_GOOD_OK"
    assert manifest["status"] == "FAIL_CLOSED"
    assert manifest["projection_ready"] is False


def test_noncritical_failure_is_a_visible_warning(tmp_path):
    def soft(call):
        raise RuntimeError("optional source unavailable")

    def analytical(call):
        return ModuleResult(status="PASS", output={"equation_id": "unit.edge", "value": 1})

    registry = [
        ModuleSpec("optional_source", "adapter", soft, critical=False, retries=0, output_contract="source",
                   inputs=("sources.optional",), freshness=("odds",)),
        ModuleSpec("edge", "analytical", analytical, critical=False, retries=0, output_contract="equation_id",
                   inputs=("teams",)),
    ]
    _mods, game = _mod("2026_12_DEN_PIT", _run(tmp_path, [_game()], registry))
    assert game["status"] == "PARTIAL"
    assert any("optional source unavailable" in w for w in game["warnings"])
    assert game["analytical_executed"] == ["edge"]
    assert "optional_source" not in game["analytical_executed"]


def test_missing_critical_input_fails_closed_and_skips_dependents(tmp_path):
    calls = []

    def ident(call):
        calls.append("ident")
        return ModuleResult(status="PASS", output={"game_id": call.game_id})

    def child(call):
        calls.append("child")
        return ModuleResult(status="PASS", output={"ran": True})

    registry = [
        ModuleSpec("game_identity", "adapter", ident, critical=True, required_inputs=("game.game_id", "game.away", "game.home"),
                   output_contract="game_id", inputs=("game.game_id", "game.away", "game.home")),
        ModuleSpec("matchup_edges", "analytical", child, depends_on=("game_identity",), output_contract="rows",
                   inputs=("teams",)),
    ]
    pkt = _game()
    del pkt["packet"]["game"]["away"]
    mods, game = _mod("2026_12_DEN_PIT", _run(tmp_path, [pkt], registry))
    assert calls == []
    assert game["status"] == "FAIL_CLOSED"
    assert mods["game_identity"]["invoked"] is False
    assert "game.away" in mods["game_identity"]["output"]["missing"]
    assert mods["matchup_edges"]["status"] == "SKIPPED"
    assert mods["matchup_edges"]["invoked"] is False
    assert game["analytical_executed"] == []


def test_retries_keep_every_failed_attempt(tmp_path):
    def flaky(call):
        if call.attempt < 3:
            raise RuntimeError(f"fail-{call.attempt}")
        return ModuleResult(status="PASS", output={"attempt": call.attempt, "equation_id": "unit.retry"})

    registry = [ModuleSpec("worker", "analytical", flaky, retries=2, timeout_sec=2, output_contract="attempt",
                           inputs=("game.game_id",))]
    mods, game = _mod("2026_12_DEN_PIT", _run(tmp_path, [_game()], registry))
    attempts = mods["worker"]["attempts"]
    assert [a["n"] for a in attempts] == [1, 2, 3]
    assert [a["status"] for a in attempts] == ["FAILED", "FAILED", "PASS"]
    assert "fail-1" in attempts[0]["error"]
    assert "fail-2" in attempts[1]["error"]
    root = Path(game["artifact_dir"]) / "modules" / "worker"
    for n in (1, 2, 3):
        body = json.loads((root / f"attempt-{n:03d}.json").read_text())
        assert body["n"] == n
    assert mods["worker"]["output"]["attempt"] == 3


def test_timeout_is_recorded_and_retried(tmp_path):
    def slow(call):
        if call.attempt == 1:
            time.sleep(0.6)
            return ModuleResult(status="PASS", output={"late": True})
        return ModuleResult(status="PASS", output={"attempt": call.attempt, "equation_id": "unit.timeout"})

    registry = [ModuleSpec("worker", "analytical", slow, retries=1, timeout_sec=0.15, output_contract="attempt",
                           inputs=("game.game_id",))]
    mods, _game_row = _mod("2026_12_DEN_PIT", _run(tmp_path, [_game()], registry))
    assert [a["status"] for a in mods["worker"]["attempts"]] == ["TIMEOUT", "PASS"]
    assert mods["worker"]["output"]["attempt"] == 2


def test_duplicate_invocation_reuses_the_same_run(tmp_path):
    calls = []

    def fn(call):
        calls.append(call.attempt)
        return ModuleResult(status="PASS", output={"equation_id": "unit.once", "n": len(calls)})

    registry = [ModuleSpec("worker", "analytical", fn, output_contract="n", inputs=("game.game_id",))]
    first = _run(tmp_path, [_game()], registry)
    second = _run(tmp_path, [_game()], registry)
    assert calls == [1]
    g1, g2 = first["games"][0], second["games"][0]
    assert g1["run_id"] == g2["run_id"]
    assert g1["join_digest"] == g2["join_digest"]
    assert g2["duplicate"] is True
    assert g1["as_of"] == AS_OF
    assert g1["code_revision"] == REV
    assert "python -m pipeline.orchestrator" in g1["command"]
    stored = json.loads((Path(g1["artifact_dir"]) / "manifest.json").read_text())
    assert stored["run_id"] == g1["run_id"]
    assert stored["duplicate"] is False


def test_join_order_and_digest_ignore_completion_order(tmp_path):
    def make(name, delay):
        def fn(call):
            time.sleep(delay)
            return ModuleResult(status="PASS", output={"name": name, "equation_id": name})
        return fn

    registry = [
        ModuleSpec("z_mod", "analytical", make("z_mod", 0.05), output_contract="name", inputs=("game.game_id",)),
        ModuleSpec("a_mod", "analytical", make("a_mod", 0.0), output_contract="name", inputs=("game.game_id",)),
        ModuleSpec("m_mod", "analytical", make("m_mod", 0.02), output_contract="name", inputs=("game.game_id",)),
    ]
    one = _run(tmp_path / "one", [_game()], registry)
    two = _run(tmp_path / "two", [_game()], registry)
    ids = [m["module_id"] for m in one["games"][0]["modules"]]
    assert ids == ["a_mod", "m_mod", "z_mod"]
    assert ids == [m["module_id"] for m in two["games"][0]["modules"]]
    assert one["games"][0]["join_digest"] == two["games"][0]["join_digest"]
    assert one["games"][0]["run_id"] == two["games"][0]["run_id"]


def test_adapter_and_stub_never_count_as_analytical_execution(tmp_path):
    def adapter(call):
        return ModuleResult(status="PASS", output={"rows": 4})

    def stub(call):
        return ModuleResult(status="BLOCKED", output={"receipt_only": True, "reason": "MODULE_ABSENT"})

    def mislabeled(call):
        return ModuleResult(status="PASS", output={"receipt_only": True, "equation_id": "not.really"})

    def real(call):
        return ModuleResult(status="PASS", output={"equation_id": "pregame.packet.edges", "rows": [{"area": "points"}]})

    registry = [
        ModuleSpec("source_adapter", "adapter", adapter, output_contract="rows", inputs=("sources",)),
        ModuleSpec("sim_v6_contract", "stub", stub, output_contract="reason", inputs=("tools/sim_v6.py",)),
        ModuleSpec("fake_analytical", "analytical", mislabeled, output_contract="equation_id", inputs=("packet",)),
        ModuleSpec("matchup_edges", "analytical", real, output_contract="rows", inputs=("teams",)),
    ]
    mods, game = _mod("2026_12_DEN_PIT", _run(tmp_path, [_game()], registry))
    assert game["analytical_executed"] == ["matchup_edges"]
    assert mods["source_adapter"]["analytical_executed"] is False
    assert mods["sim_v6_contract"]["analytical_executed"] is False
    assert mods["fake_analytical"]["analytical_executed"] is False
    assert mods["matchup_edges"]["analytical_executed"] is True
    assert any("receipt-only" in w for w in mods["fake_analytical"]["warnings"])


def test_default_registry_declares_contracts():
    registry = default_registry()
    ids = {spec.module_id for spec in registry}
    assert {
        "game_identity", "freshness_check", "phase_ledger", "matchup_edges", "rain_adjustment",
        "ngs_matchup", "sim100k_preflight", "sim_v6_contract",
    } <= ids
    for spec in registry:
        assert spec.execution_class in {"analytical", "adapter", "freshness", "gate", "stub"}
        assert spec.output_contract
        assert spec.timeout_sec > 0
        assert spec.retries >= 0
        assert isinstance(spec.depends_on, tuple)
        assert isinstance(spec.freshness, tuple)
        assert isinstance(spec.inputs, tuple)
    by = {spec.module_id: spec for spec in registry}
    assert by["game_identity"].critical is True
    assert by["sim_v6_contract"].execution_class == "stub"
    assert by["matchup_edges"].execution_class == "analytical"
    assert by["rain_adjustment"].execution_class == "analytical"
    assert by["freshness_check"].execution_class == "freshness"
    assert by["phase_ledger"].execution_class == "freshness"
    assert by["sim100k_preflight"].execution_class == "gate"
    assert by["ngs_matchup"].execution_class == "adapter"
    assert "game_identity" in by["matchup_edges"].depends_on


def test_single_game_run_invokes_real_components(tmp_path):
    from pipeline.phases import load_packet

    packet = load_packet("2026_12_DEN_PIT")
    manifest = run_games(
        [{"game_id": "2026_12_DEN_PIT", "packet": packet}],
        registry=default_registry(),
        out_dir=tmp_path,
        as_of=AS_OF,
        code_revision=REV,
        command="python -m pipeline.orchestrator --game 2026_12_DEN_PIT --as-of " + AS_OF,
    )
    mods, game = _mod("2026_12_DEN_PIT", manifest)
    invoked = [mid for mid, row in mods.items() if row["invoked"]]
    assert len(invoked) >= 4
    assert game["projection_ready"] is False
    assert game["research_only"] is True
    assert game["code_revision"] == REV
    assert game["as_of"] == AS_OF
    assert "python -m pipeline.orchestrator" in game["command"]
    assert "matchup_edges" in game["analytical_executed"]
    assert "rain_adjustment" in game["analytical_executed"]
    for banned in ("freshness_check", "phase_ledger", "ngs_matchup", "sim100k_preflight", "sim_v6_contract", "game_identity"):
        assert banned not in game["analytical_executed"]
    assert mods["matchup_edges"]["output"]["entrypoint"] == "pregame.packet.edges"
    assert mods["matchup_edges"]["output"]["directions"]
    assert mods["rain_adjustment"]["output"]["equation_id"] == "pregame.rain_model.factor"
    assert "attempts" in mods["rain_adjustment"]["output"]["factors"]
    assert mods["phase_ledger"]["output"]["schema"] == "nfl56-phase-ledger/1"
    assert mods["phase_ledger"]["analytical_executed"] is False
    assert mods["freshness_check"]["output"]["rows"]
    assert mods["sim100k_preflight"]["output"]["ran"] is False
    assert mods["sim100k_preflight"]["status"] == "REFUSED"
    assert mods["sim100k_preflight"]["analytical_executed"] is False
    assert mods["sim_v6_contract"]["status"] == "BLOCKED"
    assert mods["sim_v6_contract"]["output"]["reason"] == "MODULE_ABSENT"
    assert mods["sim_v6_contract"]["output"]["subject_invoked"] is False
    assert (Path(game["artifact_dir"]) / "manifest.json").is_file()
    # A second identical invocation must not execute the real modules again.
    again = run_games(
        [{"game_id": "2026_12_DEN_PIT", "packet": packet}],
        registry=default_registry(),
        out_dir=tmp_path,
        as_of=AS_OF,
        code_revision=REV,
        command="python -m pipeline.orchestrator --game 2026_12_DEN_PIT --as-of " + AS_OF,
    )
    assert again["games"][0]["duplicate"] is True
    assert again["games"][0]["join_digest"] == game["join_digest"]


def test_cli_runs_one_real_game_and_keeps_research_only(tmp_path):
    code = orchestrator_main([
        "--game", "2026_12_DEN_PIT",
        "--as-of", AS_OF,
        "--out", str(tmp_path),
        "--revision", REV,
    ])
    assert code == 0
    manifests = list(tmp_path.glob("2026_12_DEN_PIT/*/manifest.json"))
    assert len(manifests) == 1
    body = json.loads(manifests[0].read_text())
    assert body["projection_ready"] is False
    assert "matchup_edges" in body["analytical_executed"]
    assert "sim_v6_contract" not in body["analytical_executed"]
    slate_files = list((tmp_path / "slate").glob("*/manifest.json"))
    assert len(slate_files) == 1
    slate = json.loads(slate_files[0].read_text())
    assert slate["games"][0]["game_id"] == "2026_12_DEN_PIT"
    assert slate["projection_ready"] is False
    assert slate["scheduler"] == "cursor-local"


def test_missing_packet_does_not_suppress_another_game(tmp_path):
    def fn(call):
        return ModuleResult(status="PASS", output={"equation_id": "unit.ok", "game_id": call.game_id})

    registry = [ModuleSpec("worker", "analytical", fn, output_contract="game_id", inputs=("game.game_id",))]
    manifest = _run(
        tmp_path,
        [{"game_id": "2026_12_DOES_NOT_EXIST"}, _game("2026_12_GOOD_OK", "GOOD", "OK")],
        registry,
    )
    ids = [g["game_id"] for g in manifest["games"]]
    assert ids == ["2026_12_DOES_NOT_EXIST", "2026_12_GOOD_OK"]
    missing = next(g for g in manifest["games"] if g["game_id"] == "2026_12_DOES_NOT_EXIST")
    good = next(g for g in manifest["games"] if g["game_id"] == "2026_12_GOOD_OK")
    assert missing["status"] == "FAIL_CLOSED"
    assert good["status"] == "COMPLETE"
    assert good["modules"][0]["output"]["game_id"] == "2026_12_GOOD_OK"


def test_wrong_game_id_inside_packet_fails_closed(tmp_path):
    def fn(call):
        return ModuleResult(status="PASS", output={"equation_id": "unit.ok"})

    registry = [
        ModuleSpec("game_identity", "adapter", fn, critical=True, required_inputs=("game.game_id", "game.away", "game.home"),
                   output_contract="game_id", inputs=("game.game_id",)),
        ModuleSpec("child", "analytical", fn, depends_on=("game_identity",), output_contract="equation_id", inputs=("game.game_id",)),
    ]
    pkt = _game("2026_12_DEN_PIT")
    pkt["game_id"] = "2026_12_OTHER_GAME"
    mods, game = _mod("2026_12_OTHER_GAME", _run(tmp_path, [pkt], registry))
    assert game["status"] == "FAIL_CLOSED"
    assert mods["game_identity"]["invoked"] is False
    assert mods["child"]["status"] == "SKIPPED"
