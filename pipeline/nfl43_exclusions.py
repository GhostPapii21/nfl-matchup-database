"""NFL-43 residual R2: enforce known_flags nfl43.still_unsupported.

The three exclusions stay in force after the bounds review flips to ACCEPTED. A run or
snapshot whose config enables any of them is refused; the list is always recorded in
hook / rocket / sim outputs. No network, no credits. Research only, not validated.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CANONICAL = (
    "kick-play fouls",
    "joint_producer penalties/return yards",
    "blocked kicks/onside/fakes",
)

# Config paths that would turn an exclusion on. Values in FALSEY are treated as off.
ENABLE_PATHS: dict[str, tuple[tuple[str, ...], ...]] = {
    "kick-play fouls": (
        ("semantics", "kick_play_fouls"),
        ("semantics", "kick-play fouls"),
        ("semantics", "include_kick_play_fouls"),
        ("semantics", "penalties_include_kick_plays"),
        ("semantics", "rare_plays"),  # NFL-75 rare_plays.py covers kick-play fouls
        ("kick_play_fouls",),
    ),
    "joint_producer penalties/return yards": (
        ("semantics", "joint_producer_penalties"),
        ("semantics", "joint_producer_return_yards"),
        ("semantics", "joint_producer"),
        ("joint_producer", "penalties"),
        ("joint_producer", "return_yards"),
        ("joint_producer_penalties",),
        ("joint_producer_return_yards",),
    ),
    "blocked kicks/onside/fakes": (
        ("semantics", "blocked_kicks"),
        ("semantics", "onside"),
        ("semantics", "onside_kicks"),
        ("semantics", "fakes"),
        ("semantics", "fake_punts"),
        ("semantics", "blocked kicks/onside/fakes"),
        ("semantics", "rare_plays"),  # NFL-75 rare_plays.py covers blocked kicks / onside / fakes
        ("blocked_kicks",),
        ("onside_kicks",),
        ("fake_punts",),
    ),
}

FALSEY = {False, 0, 0.0, "0", "false", "off", "no", "none", "unsupported", None, ""}
_MISSING = object()


def _norm(s: str) -> str:
    return " ".join(str(s).lower().replace("_", " ").replace("-", " ").split())


# Allow a later edit of still_unsupported to use a close synonym of a canonical name.
_ALIASES = {_norm(n): n for n in CANONICAL}
_ALIASES.update({
    _norm("kick play fouls"): "kick-play fouls",
    _norm("joint producer"): "joint_producer penalties/return yards",
    _norm("joint_producer penalties/return yards"): "joint_producer penalties/return yards",
    _norm("blocked kicks"): "blocked kicks/onside/fakes",
    _norm("onside kicks"): "blocked kicks/onside/fakes",
    _norm("fake punts"): "blocked kicks/onside/fakes",
})


def canonicalize(name: str) -> str:
    return _ALIASES.get(_norm(name), name)


def is_enabled(value: Any) -> bool:
    if isinstance(value, str) and value.strip().lower() in FALSEY:
        return False
    if isinstance(value, dict):
        mode = value.get("mode", value.get("status", value.get("enabled", value)))
        if mode is value:
            return any(is_enabled(v) for v in value.values())
        return is_enabled(mode)
    return value not in FALSEY


def _walk(cfg: dict, path: tuple[str, ...]):
    cur: Any = cfg
    for p in path:
        if not isinstance(cur, dict) or p not in cur:
            return _MISSING
        cur = cur[p]
    return cur


def load_exclusions(flags: dict | None) -> dict:
    """Read nfl43.still_unsupported. Missing / unreadable -> fail closed."""
    if not isinstance(flags, dict) or flags.get("_error"):
        return {"status": "FAILED", "exclusions": [],
                "reason": "known_flags unreadable; nfl43.still_unsupported cannot be enforced"}
    nfl43 = flags.get("nfl43")
    if not isinstance(nfl43, dict) or "still_unsupported" not in nfl43:
        return {"status": "FAILED", "exclusions": [],
                "reason": "nfl43.still_unsupported is missing from known_flags/KNOWN_LIMITATIONS.json; "
                          "the three exclusions would go unenforced after review acceptance"}
    raw = nfl43.get("still_unsupported")
    if not isinstance(raw, list) or not raw:
        return {"status": "FAILED", "exclusions": [],
                "reason": "nfl43.still_unsupported must be a non-empty list "
                          f"(got {type(raw).__name__ if not isinstance(raw, list) else 'empty list'})"}
    return {"status": "OK", "exclusions": [canonicalize(x) if isinstance(x, str) else x for x in raw],
            "reason": None}


def enabled_in_config(cfg: dict | None, exclusions: list[str]) -> list[str]:
    if not isinstance(cfg, dict):
        return []
    hit: list[str] = []
    for name in exclusions:
        paths = ENABLE_PATHS.get(name, ())
        for path in paths:
            val = _walk(cfg, path)
            if val is not _MISSING and is_enabled(val):
                hit.append(name)
                break
    return hit


def iter_repo_configs(root: Path) -> list[tuple[str, dict]]:
    """Committed (and working-tree) engine configs plus snapshot input configs that look like engine configs."""
    root = Path(root)
    found: list[tuple[str, dict]] = []
    patterns = (
        "core/possession_engine_v0/config/*.json",
        "snapshots/*/*/inputs/*.json",
    )
    for pat in patterns:
        for p in sorted(root.glob(pat)):
            try:
                d = json.loads(p.read_text())
            except (OSError, ValueError):
                continue
            if not isinstance(d, dict):
                continue
            if "semantics" in d or "config_id" in d or "joint_producer" in d:
                rel = str(p.relative_to(root)) if p.is_relative_to(root) else str(p)
                found.append((rel, d))
    return found


def check(flags: dict | None, cfg: dict | None = None,
          configs: list[tuple[str, dict]] | None = None, *, scan_root: Path | None = None) -> dict:
    """OK only if the exclusions are listed and no provided/scanned config enables one.

    The exclusions are always included in the result so callers can record them in outputs.
    """
    loaded = load_exclusions(flags)
    base = {"exclusions": loaded.get("exclusions") or [], "enabled": [], "sources": [],
            "policy": "UNSUPPORTED (not invented): refuse any run or snapshot whose config enables one"}
    if loaded["status"] != "OK":
        return {**base, "status": "FAILED", "reason": loaded["reason"]}
    pairs = list(configs or [])
    if cfg is not None:
        pairs = [("cfg", cfg), *pairs]
    if scan_root is not None:
        pairs = [*pairs, *iter_repo_configs(scan_root)]
    enabled: list[str] = []
    sources: list[dict] = []
    for label, c in pairs:
        hit = enabled_in_config(c, loaded["exclusions"])
        if hit:
            enabled.extend(hit)
            sources.append({"source": label, "enabled": hit})
    if enabled:
        uniq = sorted(set(enabled))
        return {**base, "status": "REFUSED", "enabled": uniq, "sources": sources,
                "reason": "config enables still-unsupported NFL-43 semantics: " + ", ".join(uniq)}
    return {**base, "status": "OK", "reason": None, "recorded": True}
