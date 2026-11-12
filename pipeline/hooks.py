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
                                            have "unsupported_semantics" empty and "DEFERRED_100K" false; no function hook

Spends nothing: no hook here makes a network call or uses an API key.
"""
from __future__ import annotations

import importlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLAGS = ROOT / "known_flags" / "KNOWN_LIMITATIONS.json"
# Odds API book keys used in Blitz's freezes: Hard Rock Bet = hardrockbet, Caesars = williamhill_us.
REQUIRED_BOOKS = ("fanduel", "draftkings", "hardrockbet", "williamhill_us")
PRICE_FREEZE_DIR = ROOT / "pregame" / "price_freezes"
SEMANTICS_BOUNDS_NAME = "SEMANTICS_BOUNDS.md"

# >>> ROCKET HOOK (BetGuru, NFL-49) <<<
# When BetGuru's `rocket` validation command lands, set this to its argv in a reviewed PR, e.g.
# ["python3", "-m", "<module>", "rocket"] or ["./rocket"]. The 100k gate runs it with the game id appended and
# requires exit code 0. None = not built yet = the gate refuses.
ROCKET_COMMAND: list[str] | None = None

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


def nfl43_semantics(flags: dict | None = None, root: Path = ROOT) -> dict:
    """NFL-43 (BetGuru). Supported only when SEMANTICS_BOUNDS.md exists AND the flags no longer list unsupported semantics."""
    flags = known_flags() if flags is None else flags
    found = sorted(p for p in Path(root).rglob(SEMANTICS_BOUNDS_NAME) if ".git" not in p.parts)
    why = []
    if not found:
        why.append(f"{SEMANTICS_BOUNDS_NAME} does not exist yet")
    uns = flags.get("unsupported_semantics")
    if uns is None or uns:
        why.append("known_flags lists unsupported semantics: " + (", ".join(uns) if uns else "flag missing"))
    if why:
        return {"status": "UNSUPPORTED", "reason": "NFL-43 (penalties, returns, overtime) not closed: " + "; ".join(why) + "."}
    return {"status": "OK", "files": [str(p.relative_to(root)) for p in found]}


def known_flags(path: Path = FLAGS) -> dict:
    """Read-only. NFL-56 never writes this file."""
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError) as e:
        return {"_error": f"cannot read {path}: {e}"}
