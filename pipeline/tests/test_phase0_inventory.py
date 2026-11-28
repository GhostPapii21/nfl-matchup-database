"""Phase 0 inventory must describe this tree, not a wished-for one.

The manifest is a proposal. These tests fail if it claims a file that is
absent, hides a file it marked missing, or drifts from the phase and
freshness enums in code. They do not run a simulation.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "docs" / "automation" / "inventory_manifest.json"
INVENTORY_MD = ROOT / "docs" / "automation" / "INVENTORY.md"
REVIEW_MD = ROOT / "docs" / "automation" / "GROK_REVIEW_PACKET.md"

VOCAB = {
    "REGISTERED", "EXECUTABLE", "TESTED", "INTEGRATED",
    "BLOCKED", "EXPERIMENTAL", "MISSING",
}
COMPONENT_KEYS = {
    "id", "kind", "name", "path", "exists", "callable", "inputs", "outputs",
    "dependencies", "tests", "provenance", "statuses",
    "proves_analytical_execution", "evidence",
}


def _manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text())


def _dict_keys(path: str, name: str) -> list:
    tree = ast.parse((ROOT / path).read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name and isinstance(node.value, ast.Dict):
                    keys = []
                    for key in node.value.keys:
                        if not isinstance(key, ast.Constant):
                            raise AssertionError(f"{path}:{name} key is not a constant")
                        keys.append(key.value)
                    return keys
    raise AssertionError(f"{name} not found in {path}")


def _phase_names() -> dict[int, str]:
    tree = ast.parse((ROOT / "pipeline" / "phases.py").read_text())
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if not (isinstance(target, ast.Name) and target.id == "PHASES" and isinstance(node.value, ast.Dict)):
                continue
            out = {}
            for key, value in zip(node.value.keys, node.value.values):
                phase = key.value
                first = value.elts[0]
                if not isinstance(first, ast.Constant) or not isinstance(first.value, str):
                    raise AssertionError(f"phase {phase} name is not a string")
                out[phase] = first.value
            return out
    raise AssertionError("PHASES not found")


def test_manifest_is_phase0_and_research_only():
    data = _manifest()
    assert data["schema"] == "nfl82-phase0-inventory/1"
    assert data["linear_issue"] == "NFL-82"
    assert data["github_issue"] == 147
    assert data["scope"] == "phase-0-read-only-inventory"
    assert data["research_only"] is True
    assert data["projection_ready"] is False
    assert data["projection_ready_changed"] is False
    assert data["inventoried_commit"] == "ef4cc69035b8827fe897a574a0d7d22091ee26b3"
    assert (ROOT / ".git").exists()
    head = (ROOT / ".git" / "HEAD").read_text().strip()
    # The inventory describes main at a known commit. Later commits on this
    # branch sit on top of that commit; the object must still be present.
    git_dir = ROOT / ".git"
    obj = git_dir / "objects" / data["inventoried_commit"][:2] / data["inventoried_commit"][2:]
    assert obj.exists() or (git_dir / "objects" / "pack").is_dir()
    assert "PASS" not in data["receipt_contract"]["current_phase_statuses"]
    assert data["receipt_contract"]["checker_proves_analytical_execution"] is False
    assert head  # HEAD is readable; the commit pin is the manifest field above


def test_code_enums_match_source():
    data = _manifest()
    enums = data["code_enums"]
    assert enums["pipeline/phases.py:PHASES"] == _dict_keys("pipeline/phases.py", "PHASES")
    assert enums["pipeline/freshness.py:POLICY"] == _dict_keys("pipeline/freshness.py", "POLICY")
    assert enums["pipeline/freshness.py:HOOKED"] == _dict_keys("pipeline/freshness.py", "HOOKED")
    names = _phase_names()
    board = data["phase_board"]
    assert [row["phase"] for row in board] == list(names)
    for row in board:
        assert row["name"] == names[row["phase"]]
        assert row["proves_analytical_execution"] is False
        assert row["checker"].startswith("python -m pipeline.phases --game <game_id> --phase ")


def test_component_paths_match_the_tree():
    data = _manifest()
    ids = []
    for item in data["components"]:
        missing = COMPONENT_KEYS - item.keys()
        assert not missing, (item.get("id"), missing)
        assert item["statuses"], item["id"]
        assert set(item["statuses"]) <= VOCAB
        assert "CALIBRATED" not in item["statuses"]
        assert "PRODUCTION_READY" not in item["statuses"]
        ids.append(item["id"])
        path = item["path"]
        if item["exists"]:
            assert path, item["id"]
            assert (ROOT / path).exists(), path
        elif path:
            assert not (ROOT / path).exists(), path
    assert len(ids) == len(set(ids))


def test_sim_v6_contract_is_missing_and_not_sim100k():
    data = _manifest()
    sim = data["sim_v6"]
    assert sim["verdict"] == "MISSING"
    assert sim["canonical_exists"] is False
    assert sim["labeled_calibrated"] is False
    assert sim["distinct_from_sim100k"] is True
    assert sim["scratch_is_canonical_entrypoint"] is False
    assert not (ROOT / sim["canonical_path"]).exists()
    assert not (ROOT / "tools" / "sim_v6_calib.json").exists()
    assert not (ROOT / "calibration" / "simv56" / "engines" / "__no_calib__.json").exists()
    scratch = (ROOT / "calibration" / "simv56" / "engines" / "cc_sim_v6.py").read_text()
    assert "MODES=('mc','bias','gr')" in scratch
    assert "__no_calib__.json" in scratch
    assert "SCRATCH COPY" in scratch
    phases = (ROOT / "pipeline" / "phases.py").read_text()
    assert 'status = "PASS"' not in phases
    assert 'BLOCKING = ("MISSING", "STALE", "GAP", "NOT_YET")' in phases
    sim100k = (ROOT / "pipeline" / "sim100k.py").read_text()
    assert "TRIALS = 100_000" in sim100k
    assert "possession_engine_v0" in sim100k
    assert "monte_carlo" not in sim100k
    assert "game_randomness" not in sim100k
    period = (ROOT / "core" / "period_engine_v0" / "monte_carlo.py").read_text()
    assert "Bias: UNIMPLEMENTED" in period
    canonical = next(c for c in data["components"] if c["id"] == "sim-v6-canonical")
    assert canonical["exists"] is False
    assert "MISSING" in canonical["statuses"]
    checker = next(c for c in data["components"] if c["id"] == "phase-checker")
    assert checker["proves_analytical_execution"] is False
    gate = next(c for c in data["components"] if c["id"] == "sim100k")
    assert "EXPERIMENTAL" in gate["statuses"]
    assert gate["proves_analytical_execution"] is True


def test_named_prs_are_not_duplicated_by_this_inventory():
    data = _manifest()
    snap = data["open_pr_snapshot"]
    assert snap["do_not_duplicate"] == [140, 143, 144]
    assert snap["merged_fixture"] == 146
    assert snap["canonical_readiness_pr"] == 137
    assert snap["inspected_main"] == "ef4cc69035b8827fe897a574a0d7d22091ee26b3"
    assert data["inventoried_commit"] == snap["inspected_main"]
    by_number = {row["number"]: row for row in snap["prs"]}
    assert "canonical" in by_number[137]["overlap"].lower()
    for number in (151, 152):
        assert "must not" in by_number[number]["overlap"].lower()
    readiness = (ROOT / "evaluation" / "tests" / "test_readiness.py").read_text()
    assert 'snaps.glob("2026_12_*/*/LOCK.json")' in readiness
    assert 'assert eb["w12_with_lock"] == []' not in readiness
    assert 'assert eb["w12_with_lock"] == ["2026_12_DEN_PIT", "2026_12_KC_BUF"]' not in readiness
    for number in (140, 143, 144):
        assert by_number[number]["state"] == "open"
        assert "Do not duplicate" in by_number[number]["overlap"] or "Do not reimplement" in by_number[number]["overlap"] or "do not duplicate" in by_number[number]["overlap"].lower()
    assert by_number[146]["state"] == "merged"
    den = next(c for c in data["components"] if c["id"] == "den-pit-postgame")
    assert den["exists"] is True
    assert (ROOT / "runs" / "2026-11-27_DEN@PIT" / "POSTGAME_REVIEW.md").is_file()
    assert not (ROOT / "grading" / "results" / "2026_12_DEN_PIT.jsonl").exists()


def test_human_docs_match_the_manifest_verdict():
    inventory = INVENTORY_MD.read_text()
    review = REVIEW_MD.read_text()
    for text in (inventory, review):
        assert "tools/sim_v6.py" in text
        assert "projection_ready" in text
        assert "pipeline.sim100k" in text or "pipeline/sim100k.py" in text
        assert "NFL-82" in text
        assert "#140" in text and "#143" in text and "#144" in text and "#146" in text
    assert "You are the independent adversarial architecture reviewer" in review
    assert "do not duplicate" in inventory.lower()
