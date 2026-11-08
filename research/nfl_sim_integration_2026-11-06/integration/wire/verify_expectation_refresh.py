"""Run local post-rebind checks; all authored writes stay in integration/."""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

WIRE = Path(__file__).resolve().parent
OUT = WIRE.parent
ROOT = OUT.parent
EVIDENCE = OUT / "INTEGRATION_EXPECTATION_REFRESH_EVIDENCE.json"
CURRENT = "6471e69b97b19b85ce0a4b8e4c25117b0e40ceefa1a225ee06d7c1b7440e8367"
EXAMPLE = "50be826a2bc1cf67db052aa8095ae0d7b3e75d674ef31c65165a5fbe3c881cdd"


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def write(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n")


def inventory(root):
    return [dict(path=str(p), sha256=digest(p), bytes=p.stat().st_size)
            for p in sorted(root.rglob("*")) if p.is_file()
            and not any(x in p.parts for x in ("__pycache__", ".pytest_cache", ".git"))]


def compare(before, after):
    b, a = ({r["path"]: r["sha256"] for r in rows} for rows in (before, after))
    changes = [dict(path=p, before_sha256=b.get(p), after_sha256=a.get(p))
               for p in sorted(b.keys() | a.keys()) if b.get(p) != a.get(p)]
    return dict(unchanged=not changes, before_count=len(b), after_count=len(a), changes=changes)


def record_artifact_changes(evidence, before):
    """Separate our authored artifacts from observed concurrent integration work."""
    def retained(entry):
        p = Path(entry["path"])
        return p != EVIDENCE and not any(part.startswith(("pytest_tmp", "tmp_")) for part in p.relative_to(OUT).parts)
    changes = compare([e for e in before["integration_files"] if retained(e)],
                      [e for e in inventory(OUT) if retained(e)])["changes"]
    def ours(entry):
        relative = Path(entry["path"]).relative_to(OUT).as_posix()
        return (relative in {"GHOST_ACCEPTANCE_PACKET.md", "build_acceptance_packet.py",
                "integration_adversarial_tests.py", "market_calibration_file_hashes.json",
                "wire/producer_revision_expectations_post_rebind.json", "wire/verify_expectation_refresh.py"}
                or relative.startswith(("tests/historical/", "wire/expectation_refresh_")))
    evidence["integration_changes"] = changes
    evidence["integration_changes_note"] = "All observed differences; authorship is separated below. Runtime fixtures and the self-referential evidence file are excluded from hashes."
    evidence["authored_integration_changes"] = [e for e in changes if ours(e)]
    evidence["concurrent_external_changes"]["integration_changes"] = [e for e in changes if not ours(e)]
    evidence["scope"]["authored_paths"] = [e["path"] for e in changes if ours(e)] + [str(EVIDENCE)]
    market = "/workspace/wt-market-calibration/research/market_calibration"
    adapter_path = str(Path(market) / "joint_trial_adapter.py")
    entry = next(e for e in before["protected"][market] if e["path"] == adapter_path)
    current = digest(adapter_path)
    evidence["adapter_before_after"] = dict(path=adapter_path, before_sha256=entry["sha256"],
                                           after_sha256=current, unchanged=current == entry["sha256"])
    assert evidence["adapter_before_after"]["unchanged"], "Adapter changed since initial task snapshot"
    evidence["packet"] = dict(path=str(OUT / "GHOST_ACCEPTANCE_PACKET.md"), sha256=digest(OUT / "GHOST_ACCEPTANCE_PACKET.md"))


def main():
    started = now()
    # Captured before expectation edits. Never replace this baseline on a rerun.
    baseline_path = WIRE / "expectation_refresh_before_snapshot.json"
    before = json.loads(baseline_path.read_text())
    def protected_snapshot():
        return dict(captured_utc=now(), protected={p: inventory(Path(p)) for p in before["protected"]},
                    protected_single_files=[dict(e, sha256=digest(e["path"]))
                                            for e in before["protected_single_files"]])
    execution_before = protected_snapshot()
    execution_before_path = WIRE / "expectation_refresh_verification_pre_snapshot.json"
    write(execution_before_path, execution_before)
    env_pins = dict(PYTHONDONTWRITEBYTECODE="1", GIT_OPTIONAL_LOCKS="0",
        PYTHONPATH="/workspace/wt-nfl-sim-core-2026-11-06/research/possession_engine_v0:"
        "/workspace/wt-nfl-sim-core-2026-11-06:/workspace/wt-market-calibration:" + str(ROOT))
    env = dict(os.environ, **env_pins)
    runs = []
    for name, target in [
        ("DIRECT", "integration/integration_adversarial_tests.py::test_DIRECT_actual_producer_to_market_acceptance"),
        ("adversarial", "integration/integration_adversarial_tests.py"),
        ("historical", "integration/tests/historical"),
    ]:
        prefix = WIRE / ("expectation_refresh_" + name)
        log, junit = prefix.with_suffix(".log"), prefix.with_suffix(".xml")
        command = [sys.executable, "-m", "pytest", target, "-q", "-rs", "-p", "no:cacheprovider",
                   "-o", "junit_family=legacy", "--basetemp=" + str(WIRE / ("pytest_tmp_refresh_" + name)),
                   "--junitxml=" + str(junit)]
        record = dict(name=name, command=command, cwd=str(ROOT), environment=env_pins,
                      started_utc=now(), log=str(log), junit=str(junit))
        with log.open("wb") as stream:
            result = subprocess.run(command, cwd=ROOT, env=env, stdout=stream, stderr=subprocess.STDOUT)
        record.update(ended_utc=now(), exit_code=result.returncode, stdout_stderr=log.read_text(),
                      log_sha256=digest(log), junit_sha256=digest(junit))
        counts = {k: 0 for k in ("tests", "failures", "errors", "skipped")}
        for suite in ET.parse(junit).getroot().iter("testsuite"):
            for k in counts:
                counts[k] += int(suite.get(k, 0))
        counts["passed"] = counts["tests"] - sum(counts[k] for k in ("failures", "errors", "skipped"))
        record["counts"] = counts
        runs.append(record)
        print(name, result.returncode, counts, flush=True)
    after = protected_snapshot()
    after_path = WIRE / "expectation_refresh_after_snapshot.json"
    write(after_path, after)
    protected = {p: compare(rows, after["protected"][p]) for p, rows in execution_before["protected"].items()}
    protected["contract_and_wire_companion"] = compare(execution_before["protected_single_files"], after["protected_single_files"])
    task_baseline_comparisons = {p: compare(rows, after["protected"][p]) for p, rows in before["protected"].items()}
    task_baseline_comparisons["contract_and_wire_companion"] = compare(before["protected_single_files"], after["protected_single_files"])
    market = json.loads((OUT / "market_calibration_file_hashes.json").read_text())
    mismatches = [e["path"] for e in market["files"] if digest(e["path"]) != e["sha256"]]
    archived = {e["path"]: e for e in before["integration_files"]}
    frozen = [dict(path=str(WIRE / n), before_sha256=archived[str(WIRE / n)]["sha256"],
                   after_sha256=digest(WIRE / n)) for n in (
        "producer_joint_trial_example_v1.jsonl", "WIRE_SCHEMA_V1_META.json",
        "CONTRACT_BINDING_AUTHORIZATION_2026-11-06.md", "PARENT_VERIFY_POST_REBIND.json",
        "parent_verify_adversarial_post_rebind.log", "INTEGRATION_WIRE_EVIDENCE.json")]
    historical_inventory = json.loads((OUT / "tests/historical/market_calibration_file_hashes.json.pre_refresh.txt").read_text())
    revision = json.loads((WIRE / "producer_revision_expectations_post_rebind.json").read_text())
    checks = dict(
        DIRECT_green=runs[0]["exit_code"] == 0 and runs[0]["counts"]["passed"] == 1,
        full_adversarial_green=runs[1]["exit_code"] == 0 and runs[1]["counts"]["tests"] > 0
        and runs[1]["counts"]["skipped"] == 0,
        historical_separate=runs[2]["exit_code"] == 0 and runs[2]["counts"]["skipped"] == 6
        and runs[2]["counts"]["tests"] == 6,
        protected_inputs_unchanged_during_verification=all(c["unchanged"] for c in protected.values()),
        market_inventory_matches=not mismatches,
        authorized_contract=digest(ROOT / "core_contract.md") == CURRENT,
        immutable_example=digest(WIRE / "producer_joint_trial_example_v1.jsonl") == EXAMPLE,
        frozen_records_unchanged=all(e["before_sha256"] == e["after_sha256"] for e in frozen))
    evidence = dict(document_type="INTEGRATION_EXPECTATION_REFRESH", started_utc=started, ended_utc=now(),
        direct_transport="GREEN" if checks["DIRECT_green"] else "RED",
        ghost_final_acceptance="NOT_CLAIMED", source_readiness="OPEN_NOT_READY", actionable_status="NOLINE",
        bias="UNIMPLEMENTED_NO_FITTED_CALIB", impact="NOT_MEASURED", predictive_claims=False, projection_ready=False,
        scope=dict(write_root=str(OUT), market_adapter_edits=False, core_edits=False, source_gate_edits=False,
                   original_producer_evidence_edits=False, network_requests=0, spend=0, new_simulations=0, bias_fit_calls=0),
        contract=dict(expected_sha256=CURRENT, actual_sha256=digest(ROOT / "core_contract.md"),
                      historical_sha256="d6a4689f55bbc1231205dccf1d19de51019c40d87a7f7c1fd4ba5238cec836b9",
                      authorization="integration/wire/CONTRACT_BINDING_AUTHORIZATION_2026-11-06.md",
                      path_override=False, DIRECT_trial_remap=False),
        before_results=dict(source="integration/wire/PARENT_VERIFY_POST_REBIND.json",
                            DIRECT=dict(passed=1, failed=0), adversarial=dict(passed=51, failed=9),
                            note="Prior captured counts; original pipeline masked exit status. Original logs preserved."),
        pytest=runs, checks=checks, protected_comparisons=protected,
        task_baseline_comparisons=task_baseline_comparisons,
        concurrent_external_changes=dict(
            note="External owner work observed after the initial task snapshot. No external files were edited or reverted by this refresh. Verification uses a fresh immediate pre/post comparison; initial drift is preserved separately.",
            first_attempt="integration/wire/expectation_refresh_attempt1/INTEGRATION_EXPECTATION_REFRESH_EVIDENCE.json",
            changes=[e for c in task_baseline_comparisons.values() for e in c["changes"]]),
        snapshots=[dict(path=str(p), sha256=digest(p)) for p in (baseline_path, execution_before_path, after_path)],
        frozen_records=frozen, producer_revision_changes=revision["changes"],
        inventory_refresh=dict(path=str(OUT / "market_calibration_file_hashes.json"),
            sha256=digest(OUT / "market_calibration_file_hashes.json"),
            historical_path="integration/tests/historical/market_calibration_file_hashes.json.pre_refresh.txt",
            before_count=len(historical_inventory["files"]), after_count=len(market["files"]),
            changes=compare(historical_inventory["files"], market["files"])["changes"], mismatches=mismatches),
        historical_suite=dict(path="integration/tests/historical/test_historical_pre_rebind.py",
                              reason="HISTORICAL_PRE_REBIND_RECORD", gates_live_acceptance=False),
        limits=["Synthetic SCENARIO_ONLY retained rows; zero adapter-usable trials.",
                "DIRECT is score transport only; adapter full CORE accounting acceptance remains NOT_RUN.",
                "Certified as-of sources, canonical joins and workflow completion remain open.",
                "No fitted Bias, untouched-holdout validation or same-evaluation predictive metrics."])
    write(EVIDENCE, evidence)
    if not all(checks.values()):
        raise SystemExit("Refresh checks failed; inspect evidence/logs. Packet not rebuilt.")
    subprocess.run([sys.executable, str(OUT / "build_acceptance_packet.py")], cwd=ROOT, env=env, check=True)
    record_artifact_changes(evidence, before)
    write(EVIDENCE, evidence)


if __name__ == "__main__":
    main()
