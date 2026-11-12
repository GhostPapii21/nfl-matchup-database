"""Fail-closed hooks for pieces other owners are building. NFL-56 does not implement any of them.

Each hook is bound in REGISTRY as "module:function" once its owner ships it. Unbound, or if the bound function
raises or returns anything but status OK/PASS, the hook reports PENDING/FAILED and every gate that depends on it
refuses. Binding a hook is a reviewed code change (pull request), never an environment variable or a flag.

  hook                 owner     ticket   contract (what the function returns)
  four_book_prices     Blitz     NFL-49   NOT a function hook: read-only check of the newest
                                            pregame/price_freezes/<ET date>_<AWAY>@<HOME>/freeze_*.json written by
                                            `python -m pregame.multibook` (Blitz's module is never imported or edited)
  rocket_validation    BetGuru   NFL-49   ROCKET_COMMAND: argv list; the gate runs it and requires exit code 0
  official_inactives   unassigned NFL-46/49 {"status": "OK", "retrieved_utc": iso, "inactives": {team: [names]}}  fn(packet)
  nfl43_semantics      BetGuru   NFL-43   SEMANTICS_BOUNDS.md must exist in the repo AND known_flags/KNOWN_LIMITATIONS.json must
                                            have "unsupported_semantics" empty and "DEFERRED_100K" false AND the review
                                            status file known_flags/NFL43_REVIEW.json must say ACCEPTED for the sha256 of
                                            the current SEMANTICS_BOUNDS.md (the reviewer flips it) AND nfl43.still_unsupported
                                            (kick-play fouls, joint_producer penalties/return yards, blocked kicks/onside/fakes)
                                            must be present and not enabled by the run/snapshot config; no function hook

Spends nothing: no hook here makes a network call or uses an API key.
"""
from __future__ import annotations

import importlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from . import nfl43_exclusions

ROOT = Path(__file__).resolve().parents[1]
FLAGS = ROOT / "known_flags" / "KNOWN_LIMITATIONS.json"
# Odds API book keys used in Blitz's freezes: Hard Rock Bet = hardrockbet, Caesars = williamhill_us.
REQUIRED_BOOKS = ("fanduel", "draftkings", "hardrockbet", "williamhill_us")
PRICE_FREEZE_DIR = ROOT / "pregame" / "price_freezes"
SEMANTICS_BOUNDS_NAME = "SEMANTICS_BOUNDS.md"
SEMANTICS_BOUNDS_PATH = "core/possession_engine_v0/SEMANTICS_BOUNDS.md"
NFL43_REVIEW_NAME = "known_flags/NFL43_REVIEW.json"

# >>> ROCKET HOOK (BetGuru, NFL-49) <<<
# When BetGuru's `rocket` validation command lands, set this to its argv in a reviewed PR, e.g.
# ["python3", "-m", "<module>", "rocket"] or ["./rocket"]. The 100k gate runs it with the game id appended and
# requires exit code 0. None = not built yet = the gate refuses.
ROCKET_COMMAND: list[str] | None = ["python3", "rocket"]  # BetGuru NFL-49: ./rocket [game_id] (rocket_gate/cli.py)

# Bind each to "package.module:function" in a reviewed PR when the owner's piece lands. None = not built yet.
REGISTRY: dict[str, str | None] = {
    # BetGuru (NFL-49 Phase 15): reads the newest phase15/inactives/<game>/inactives_*.json written by
    # `python -m phase15.official_inactives --game <id>` (club official "Inactives" articles). No network in the hook.
    "official_inactives": "phase15.official_inactives:hook",
}
PENDING_REASON = {
    "official_inactives": "No official-inactives pull exists yet (NFL-46 / NFL-49); Phase 15 stays NOT_YET.",
}


def _resolve(name: str, impl=None):
    if impl is not None:
        return impl
    target = REGISTRY.get(name)
    if not target:
        return None
    mod, _, fn = target.partition(":")
    return getattr(importlib.import_module(mod), fn)


def _call(name: str, impl, *args, ok=("OK",)) -> dict:
    try:
        fn = _resolve(name, impl)
    except Exception as e:  # a broken binding must fail closed, not crash the gate
        return {"status": "FAILED", "reason": f"{name} hook could not be loaded: {e!r}"}
    if fn is None:
        return {"status": "PENDING", "reason": PENDING_REASON[name]}
    try:
        res = fn(*args)
    except Exception as e:
        return {"status": "FAILED", "reason": f"{name} hook raised {e!r}"}
    if not isinstance(res, dict) or res.get("status") not in ok:
        status = res.get("status") if isinstance(res, dict) else type(res).__name__
        return {"status": "FAILED", "reason": f"{name} hook returned {status!r}, not {'/'.join(ok)}.",
                **({"detail": res} if isinstance(res, dict) else {})}
    return res


def _team_pair(pk: dict):
    g = pk.get("game") or {}
    return g.get("away"), g.get("home")


def newest_price_freeze(pk: dict, base: Path | None = None) -> Path | None:
    """Newest freeze_*.json for this game under pregame/price_freezes/<ET date>_<AWAY>@<HOME>/ (name sorts by UTC stamp)."""
    away, home = _team_pair(pk)
    base = Path(base or PRICE_FREEZE_DIR)
    if not (away and home) or not base.is_dir():
        return None
    date = str((pk.get("game") or {}).get("date") or "")
    dirs = [d for d in base.glob(f"*_{away}@{home}") if d.is_dir() and (not date or d.name.startswith(date))]
    files = sorted((f for d in dirs for f in d.glob("freeze_*.json")), key=lambda f: f.name)
    return files[-1] if files else None


def four_book_prices(pk: dict, impl=None, base: Path | None = None) -> dict:
    """Read-only check of Blitz's newest price freeze for this game. Never imports pregame.multibook, never pulls."""
    if impl is not None:
        return _call("four_book_prices", impl, pk)
    f = newest_price_freeze(pk, base)
    away, home = _team_pair(pk)
    if f is None:
        return {"status": "MISSING", "reason": f"No pregame/price_freezes/*_{away}@{home}/freeze_*.json for this game "
                "(run Blitz's `python -m pregame.multibook`; see pregame/MULTIBOOK.md once merged)."}
    try:
        d = json.loads(f.read_text())
    except (OSError, ValueError) as e:
        return {"status": "FAILED", "reason": f"{f.name} unreadable: {e}"}
    meta = d.get("meta") or {}
    if meta.get("status") != "OK":
        return {"status": "FAILED", "reason": f"{f.name} status is {meta.get('status')!r}, not OK.", "file": str(f)}
    books = {r.get("book") for r in d.get("rows") or [] if not r.get("reference_only")}
    return {"status": "OK", "file": str(f.relative_to(ROOT)) if f.is_relative_to(ROOT) else str(f),
            "retrieved_utc": meta.get("pulled_utc"), "books": {b: True for b in sorted(b for b in books if b)},
            "props_missing": meta.get("props_missing")}


def official_inactives(pk: dict, impl=None) -> dict:
    return _call("official_inactives", impl, pk)


def rocket_validation(game_id: str, impl=None, command: list[str] | None = None) -> dict:
    """>>> ROCKET HOOK <<< Runs BetGuru's `rocket` once ROCKET_COMMAND is set; refuses until then."""
    if impl is not None:
        return _call("rocket_validation", impl, game_id, ok=("PASS",))
    cmd = command if command is not None else ROCKET_COMMAND
    if not cmd:
        return {"status": "PENDING", "reason": "The `rocket` validation command is not built yet (BetGuru, NFL-49); "
                "ROCKET_COMMAND in pipeline/hooks.py is unset."}
    try:
        p = subprocess.run([*cmd, game_id], cwd=ROOT, capture_output=True, text=True, timeout=1800)
    except (OSError, subprocess.SubprocessError) as e:
        return {"status": "FAILED", "reason": f"`rocket` could not run: {e!r}"}
    tail = (p.stdout + p.stderr).strip()[-400:]
    if p.returncode != 0:
        return {"status": "FAILED", "reason": f"`rocket` exited {p.returncode}.", "detail": tail}
    return {"status": "PASS", "detail": tail}


def nfl43_review(root: Path = ROOT) -> dict:
    """NFL-43 AC4 review guard. OK only if known_flags/NFL43_REVIEW.json says ACCEPTED and its accepted_bounds_sha256
    equals the sha256 of the current SEMANTICS_BOUNDS.md. Missing/unreadable file, PENDING, NOT_ACCEPTED, or a bounds
    file edited after acceptance -> PENDING_REVIEW (every 100k path refuses). Read-only; never flips the file."""
    import hashlib
    root = Path(root)
    f, bounds = root / NFL43_REVIEW_NAME, root / SEMANTICS_BOUNDS_PATH
    try:
        rv = json.loads(f.read_text())
    except (OSError, ValueError) as e:
        return {"status": "PENDING_REVIEW", "reason": f"NFL-43 bounds review status unreadable ({NFL43_REVIEW_NAME}): {e!r}"}
    st = rv.get("status")
    if st != "ACCEPTED":
        return {"status": "PENDING_REVIEW", "reason": f"NFL-43 bounds review is {st!r} in {NFL43_REVIEW_NAME}, not ACCEPTED; "
                "no 100k run until the reviewer accepts the bounds."}
    if not bounds.exists():
        return {"status": "PENDING_REVIEW", "reason": f"{SEMANTICS_BOUNDS_PATH} missing"}
    cur = hashlib.sha256(bounds.read_bytes()).hexdigest()
    if rv.get("accepted_bounds_sha256") != cur:
        return {"status": "PENDING_REVIEW", "reason": "SEMANTICS_BOUNDS.md changed after the accepted review "
                f"(accepted {str(rv.get('accepted_bounds_sha256'))[:12]}, current {cur[:12]}); needs re-review."}
    return {"status": "OK", "accepted_commit": rv.get("accepted_commit"), "bounds_sha256": cur}



def nfl43_still_unsupported(flags: dict | None = None, cfg: dict | None = None, root: Path = ROOT,
                            *, scan_repo: bool = False) -> dict:
    """NFL-43 residual R2: honor known_flags nfl43.still_unsupported even after the review flips.

    Missing list -> FAILED (fail closed). A config that enables one of the three exclusions -> REFUSED.
    OK still includes the exclusion list so callers can record it in outputs. scan_repo=True also
    checks engine configs and snapshot input configs under root.
    """
    flags = known_flags() if flags is None else flags
    return nfl43_exclusions.check(flags, cfg=cfg, scan_root=(Path(root) if scan_repo else None))


def nfl43_semantics(flags: dict | None = None, root: Path = ROOT, cfg: dict | None = None,
                     *, scan_repo: bool = False) -> dict:
    """NFL-43 (BetGuru). Supported only when SEMANTICS_BOUNDS.md exists, the flags no longer list unsupported semantics,
    DEFERRED_100K is false, the bounds review (nfl43_review) is ACCEPTED for the current bounds file, and
    nfl43.still_unsupported is present and not enabled by cfg (those three exclusions stay in force after review)."""
    flags = known_flags() if flags is None else flags
    found = sorted(p for p in Path(root).rglob(SEMANTICS_BOUNDS_NAME) if ".git" not in p.parts)
    why = []
    if not found:
        why.append(f"{SEMANTICS_BOUNDS_NAME} does not exist yet")
    uns = flags.get("unsupported_semantics")
    if uns is None or uns:
        why.append("known_flags lists unsupported semantics: " + (", ".join(uns) if uns else "flag missing"))
    if flags.get("DEFERRED_100K") is not False:
        why.append("DEFERRED_100K is not false (100k deferred pending NFL-43 bounds review)")
    rv = nfl43_review(root)
    if rv["status"] != "OK":
        why.append(rv["reason"])
    # R2: still_unsupported stays enforced after the review flips. Presence is required; enabling one is a refusal.
    ex = nfl43_still_unsupported(flags, cfg=cfg, root=root, scan_repo=scan_repo)
    if ex["status"] != "OK":
        why.append(ex["reason"])
    if why:
        return {"status": "UNSUPPORTED", "review": rv["status"],
                "still_unsupported": ex.get("exclusions") or [],
                "still_unsupported_status": ex["status"],
                "reason": "NFL-43 (penalties, returns, overtime) not closed: " + "; ".join(why) + "."}
    return {"status": "OK", "review": "ACCEPTED", "files": [str(p.relative_to(root)) for p in found],
            "still_unsupported": ex["exclusions"], "still_unsupported_status": "OK"}


def known_flags(path: Path = FLAGS) -> dict:
    """Read-only. NFL-56 never writes this file."""
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError) as e:
        return {"_error": f"cannot read {path}: {e}"}
