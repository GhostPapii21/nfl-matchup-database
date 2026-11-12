"""NFL-42: the single validation entrypoint. Routes only to the decontaminated protocol.

* ``run_validation()`` verifies the registry: authorized decontam validator bytes (sha256), the contaminated
  validator bytes UNCHANGED (immutable historical evidence), and loads the decontam policy metrics. It never
  executes the contaminated validator and never sets ``accepted_policy`` (the decontam result is ``null``).
* ``load_role_policy(path)`` is the consumer helper: it refuses any denied file (by path or sha256) and any
  metrics carrying a non-null ``accepted_policy`` / ``gate_passed=true`` (W7-8 promotion).
* ``invoke(path)`` is the only sanctioned way to run a validator file; denied paths raise ``ContaminatedEntrypoint``.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1]
REPO = ENGINE.parents[1]
REGISTRY = Path(__file__).with_name("ENTRYPOINT_REGISTRY.json")


class ContaminatedEntrypoint(RuntimeError):
    pass


def _sha(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def registry() -> dict:
    return json.loads(REGISTRY.read_text())


def _denied(path: Path, reg: dict) -> dict | None:
    path = Path(path).resolve()
    digest = _sha(path) if path.exists() else None
    for d in reg["deny"]:
        if path == (REPO / d["path"]).resolve() or (digest and digest == d["sha256"]):
            return d
    return None


def invoke(path, reg: dict | None = None):
    reg = reg or registry()
    d = _denied(Path(path), reg)
    if d:
        raise ContaminatedEntrypoint(f"REJECTED {d['path']}: {d['reason']} (NFL-42)")
    auth = REPO / reg["authorized"]["path"]
    if Path(path).resolve() != auth.resolve():
        raise ContaminatedEntrypoint(f"REJECTED {path}: not the registered validation_entrypoint target")
    if _sha(auth) != reg["authorized"]["sha256"]:
        raise ContaminatedEntrypoint("REJECTED: authorized decontam validator bytes changed")
    return auth


def load_role_policy(path, reg: dict | None = None) -> dict:
    reg = reg or registry()
    path = Path(path)
    d = _denied(path, reg)
    if d:
        raise ContaminatedEntrypoint(f"REJECTED metrics {d['path']}: {d['reason']}")
    m = json.loads(path.read_text())
    if m.get("accepted_policy") is not None or m.get("gate_passed") is True:
        raise ContaminatedEntrypoint(f"REJECTED metrics {path}: promotes accepted_policy={m.get('accepted_policy')!r} "
                                     f"gate_passed={m.get('gate_passed')!r} (W7-8 promotion is not allowed)")
    return m


def run_validation() -> dict:
    reg = registry()
    checks = {}
    for d in reg["deny"]:
        p = REPO / d["path"]
        checks[f"deny_bytes_unchanged:{d['path']}"] = p.exists() and _sha(p) == d["sha256"]
    auth = invoke(REPO / reg["authorized"]["path"], reg)
    checks["authorized_sha256"] = _sha(auth) == reg["authorized"]["sha256"]
    m = load_role_policy(REPO / reg["authorized"]["metrics"], reg)
    checks["decontam_status"] = m.get("status") == reg["authorized"]["required_status"]
    checks["accepted_policy_null"] = m.get("accepted_policy") is None
    ok = all(checks.values())
    return {"status": "PASS" if ok else "FAIL", "checks": checks, "accepted_policy": None,
            "policy_status": m.get("status"), "entrypoint": reg["validation_entrypoint"]}


if __name__ == "__main__":
    r = run_validation()
    print(json.dumps(r, indent=1))
    raise SystemExit(0 if r["status"] == "PASS" else 1)
