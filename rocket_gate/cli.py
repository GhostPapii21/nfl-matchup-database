"""`rocket`: the one validation command (NFL-49). Fail-closed: exit 0 only if EVERY check passes.

    ./rocket                      # repo-wide checks (R1-R4)
    ./rocket 2026_10_WAS_NYG      # + locked-snapshot checks for that game (R5)
    ./rocket --skip-pytest ...    # used only by rocket's own tests (never by the 100k gate)
    ./rocket --json out.json ...  # also write the report

Checks
  R1 nfl42_entrypoint   single validation entrypoint routes to the decontam protocol; contaminated bytes unchanged
  R2 nfl43_semantics    SEMANTICS_BOUNDS.md present, known_flags consistent, DEFERRED_100K false, the NFL-43 bounds
                        review ACCEPTED for the current bounds file (known_flags/NFL43_REVIEW.json via
                        pipeline.hooks.nfl43_semantics), and nfl43.still_unsupported listed and not enabled by any
                        engine/snapshot config (those exclusions stay in force after review). While review is pending
                        R2 FAILS, so rocket (and the 100k gate G6 that runs it) refuses.
  R3 safety             projection_ready false everywhere; no money/stake keys in snapshot/config/phase15 files
  R4 test_suites        pytest: possession engine, period engine, pipeline, phase15, snapshots, rocket
  R5 snapshot <game>    newest snapshots/<game>/*/LOCK.json: every file hash matches, locked before kickoff,
                        n == 100,000, code commit is an ancestor of HEAD, as-of checks passed, price freeze
                        pulled before the lock, projection_ready false, and locked under ACCEPTED NFL-43 review
                        (locks made before review are flagged KNOWN_MODEL_ERROR_UNREVIEWED_BOUNDS)
No network, no API keys, no credits. Never flips projection_ready.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = ("\"stake", "bankroll", "\"wager", "units_risked", "bet_amount", "\"payout")
SUITES = ["core/possession_engine_v0/tests", "core/period_engine_v0/tests", "pipeline/tests", "phase15/tests",
          "snapshots/tests", "rocket_gate/tests", "evaluation/tests"]
TRIALS = 100_000


def _ok(name, passed, detail=None):
    return {"check": name, "status": "PASS" if passed else "FAIL", "detail": detail}


def r1_entrypoint():
    sys.path.insert(0, str(ROOT / "core" / "possession_engine_v0"))
    try:
        from validation.entrypoint import run_validation
        r = run_validation()
        return _ok("R1_nfl42_entrypoint", r["status"] == "PASS" and r["accepted_policy"] is None, r["checks"])
    except Exception as e:
        return _ok("R1_nfl42_entrypoint", False, repr(e))


def r2_semantics(root: Path = ROOT):
    why = []
    recorded = []
    bounds = root / "core/possession_engine_v0/SEMANTICS_BOUNDS.md"
    if not bounds.exists():
        why.append("SEMANTICS_BOUNDS.md missing")
    try:
        flags = json.loads((root / "known_flags/KNOWN_LIMITATIONS.json").read_text())
    except Exception as e:
        return _ok("R2_nfl43_semantics", False, f"flags unreadable: {e!r}")
    if flags.get("unsupported_semantics"):
        why.append(f"unsupported_semantics={flags['unsupported_semantics']}")
    if flags.get("DEFERRED_100K") is not False:
        why.append("DEFERRED_100K is not false (100k deferred pending NFL-43 bounds review)")
    sem = (root / "core/possession_engine_v0/semantics.py")
    if not sem.exists() or "official_2025_regular_season" not in sem.read_text():
        why.append("semantics.py missing or lacks official OT")
    try:
        sys.path.insert(0, str(root))
        from pipeline import hooks
        rv = hooks.nfl43_review(root)
        if rv["status"] != "OK":
            why.append("REVIEW_PENDING: " + rv["reason"])
        h = hooks.nfl43_semantics(flags, root=root, scan_repo=True)
        if h["status"] != "OK" and rv["status"] == "OK":
            why.append(h.get("reason"))
        ex = hooks.nfl43_still_unsupported(flags, root=root, scan_repo=True)
        recorded = ex.get("exclusions") or []
        if ex["status"] != "OK":
            why.append("STILL_UNSUPPORTED: " + ex["reason"])
    except Exception as e:
        why.append(f"pipeline.hooks.nfl43_semantics failed: {e!r}")
    detail = why or {"ok": True, "still_unsupported": recorded}
    return _ok("R2_nfl43_semantics", not why, detail)


def r3_safety(root: Path = ROOT):
    why = []
    try:
        if json.loads((root / "known_flags/KNOWN_LIMITATIONS.json").read_text()).get("projection_ready") is not False:
            why.append("known_flags projection_ready is not false")
    except Exception as e:
        why.append(repr(e))
    for p in sorted((root / "pregame/packets").glob("*/packet.json")):
        try:
            if json.loads(p.read_text()).get("projection_ready") is not False:
                why.append(f"{p.relative_to(root)} projection_ready not false")
        except ValueError:
            why.append(f"{p.relative_to(root)} unreadable")
    for p in sorted((root / "snapshots").glob("*/*/LOCK.json")):
        if json.loads(p.read_text()).get("projection_ready") is not False:
            why.append(f"{p.relative_to(root)} projection_ready not false")
    # no player numbers published from snapshots (team-bootstrap credits are not a player model)
    for p in sorted((root / "snapshots").glob("*/*/summary.json")):
        if "player_mean_yards_top" in json.loads(p.read_text()):
            why.append(f"{p.relative_to(root)} publishes player numbers")
    for p in sorted((root / "snapshots").glob("*/*/inputs/*.json")):
        d = json.loads(p.read_text())
        if isinstance(d, dict) and (any(r.get("player") for r in d.get("rows") or [] if isinstance(r, dict))
                                    or "team_projection" in d or "consensus" in (d.get("meta") or {})):
            why.append(f"{p.relative_to(root)} republishes player rows / packet projections")
    scan = [*(root / "snapshots").rglob("*.json"), *(root / "snapshots").rglob("*.md"),
            *(root / "phase15").rglob("*.json"), *(root / "core/possession_engine_v0/config").glob("*.json")]
    for p in scan:
        t = p.read_text(errors="replace").lower()
        hit = [k for k in FORBIDDEN if k in t]
        if hit:
            why.append(f"{p.relative_to(root)} contains money/stake key(s) {hit}")
    return _ok("R3_safety", not why, why or "OK")


def r4_suites(root: Path = ROOT):
    res, bad = {}, []
    for s in SUITES:
        d = root / s
        if not d.is_dir():
            res[s] = "MISSING"; bad.append(s); continue
        import os
        env = {**os.environ, "ROCKET_ACTIVE": "1"}
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(d)], cwd=root,
                           capture_output=True, text=True, timeout=1500, env=env)
        tail = (p.stdout.strip().splitlines() or [""])[-1]
        res[s] = f"exit {p.returncode}: {tail}"
        if p.returncode != 0:
            bad.append(s)
    return _ok("R4_test_suites", not bad, res)


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def r5_snapshot(game_id: str, root: Path = ROOT):
    locks = sorted((root / "snapshots" / game_id).glob("*/LOCK.json"))
    if not locks:
        return _ok("R5_snapshot", False, f"no snapshots/{game_id}/*/LOCK.json (lock with python3 -m snapshots.lock before kickoff)")
    f = locks[-1]
    d = f.parent
    lk = json.loads(f.read_text())
    why = []
    for rel, h in (lk.get("files") or {}).items():
        p = d / rel
        if not p.exists() or _sha(p) != h:
            why.append(f"hash mismatch/missing: {rel}")
    if not lk.get("files"):
        why.append("LOCK.json lists no files")
    try:
        if datetime.fromisoformat(lk["locked_utc"]) >= datetime.fromisoformat(lk["kickoff_utc"]):
            why.append("locked at/after kickoff")
        pulled = (lk.get("inputs") or {}).get("price_freeze_pulled_utc")
        if pulled and datetime.fromisoformat(pulled.replace("Z", "+00:00")) > datetime.fromisoformat(lk["locked_utc"]):
            why.append("price freeze pulled after lock")
    except Exception as e:
        why.append(f"bad timestamps: {e!r}")
    if (lk.get("sim") or {}).get("n") != TRIALS:
        why.append(f"sim n={lk.get('sim', {}).get('n')} != {TRIALS}")
    if lk.get("projection_ready") is not False:
        why.append("projection_ready not false")
    if lk.get("asof_checks") != "PASS":
        why.append("as-of checks not PASS")
    if lk.get("nfl43_review") != "ACCEPTED":
        why.append("KNOWN_MODEL_ERROR_UNREVIEWED_BOUNDS: locked while the NFL-43 bounds review was not ACCEPTED "
                   f"(LOCK nfl43_review={lk.get('nfl43_review')!r})")
    still_unsupported = lk.get("still_unsupported") or []
    try:
        sys.path.insert(0, str(root))
        from pipeline import hooks
        flags = json.loads((root / "known_flags/KNOWN_LIMITATIONS.json").read_text())
        cfgs = []
        for cf in sorted((d / "inputs").glob("*.json")):
            try:
                data = json.loads(cf.read_text())
            except (OSError, ValueError):
                continue
            if isinstance(data, dict) and ("semantics" in data or "config_id" in data or "joint_producer" in data):
                cfgs.append((str(cf.relative_to(root)) if cf.is_relative_to(root) else str(cf), data))
        ex = hooks.nfl43_exclusions.check(flags, configs=cfgs)
        still_unsupported = ex.get("exclusions") or still_unsupported
        if ex["status"] != "OK":
            why.append("STILL_UNSUPPORTED: " + ex["reason"])
    except Exception as e:
        why.append(f"still_unsupported check failed: {e!r}")
    if lk.get("code_dirty"):
        why.append("sim ran on uncommitted engine code")
    c = lk.get("code_commit", "")
    anc = subprocess.run(["git", "merge-base", "--is-ancestor", c, "HEAD"], cwd=root, capture_output=True)
    if anc.returncode != 0:
        why.append(f"code commit {c[:10]} is not an ancestor of HEAD")
    detail = {"lock": str(f.relative_to(root)), "still_unsupported": still_unsupported}
    if why:
        detail["problems"] = why
    return _ok("R5_snapshot", not why, detail)


def run(game_id: str | None = None, skip_pytest: bool = False, root: Path = ROOT) -> dict:
    import os
    if os.environ.get("ROCKET_ACTIVE") and not skip_pytest:
        # rocket's own pytest run reached a test that shells out to rocket: refuse instead of recursing.
        return {"schema": "rocket/1", "game_id": game_id, "status": "FAIL", "projection_ready": False,
                "checks": [_ok("R0_recursion_guard", False, "rocket invoked inside rocket's own test run")]}
    checks = [r1_entrypoint(), r2_semantics(root), r3_safety(root)]
    checks.append(_ok("R4_test_suites", True, "SKIPPED (--skip-pytest; rocket self-test only)") if skip_pytest else r4_suites(root))
    if game_id:
        checks.append(r5_snapshot(game_id, root))
    status = "PASS" if all(c["status"] == "PASS" for c in checks) and not skip_pytest else ("PASS_SELFTEST" if all(c["status"] == "PASS" for c in checks) else "FAIL")
    return {"schema": "rocket/1", "game_id": game_id, "status": status, "checks": checks, "projection_ready": False}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="rocket", description="NFL-49 one validation command (fail closed)")
    ap.add_argument("game_id", nargs="?")
    ap.add_argument("--skip-pytest", action="store_true")
    ap.add_argument("--json", type=Path)
    a = ap.parse_args(argv)
    r = run(a.game_id, a.skip_pytest)
    for c in r["checks"]:
        print(f"{c['status']:4}  {c['check']}  {json.dumps(c['detail'], default=str)[:300]}")
    print(f"rocket: {r['status']}")
    if a.json:
        a.json.write_text(json.dumps(r, indent=1, default=str) + "\n")
    return 0 if r["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
