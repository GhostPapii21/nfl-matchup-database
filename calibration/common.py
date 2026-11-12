"""Shared helpers for NFL-49 calibration / diagnostics (research only, not validated)."""
from __future__ import annotations
import copy, hashlib, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "core/possession_engine_v0"
TEMPLATE = ENGINE / "config/was_nyg_2026-11-12_data_only_nfl43.json"
PBP = ROOT / "data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet"
PBP_PULLED_ET = "2026-11-12 11:16 AM ET"  # nflverse play_by_play_2026 release asset, pulled by BetGuru (13d83e4)
MAX_N = 20_000
LABEL = "research only, not validated"
H2H_ARMS = {"off": "off", "shrunk": {"mode": "shrunk"}, "legacy": "legacy_always"}


def engine_path():
    if str(ENGINE) not in sys.path:
        sys.path.insert(0, str(ENGINE))


def sha256(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git(*args) -> str:
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    except OSError:
        return "unknown"


def engine_version() -> dict:
    """Records exactly which engine produced an output, so a rerun on a later engine is comparable."""
    files = sorted(p for p in ENGINE.glob("*.py"))
    h = hashlib.sha256()
    for p in files:
        h.update(p.name.encode()); h.update(p.read_bytes())
    dirty = git("status", "--porcelain", "--", str(ENGINE.relative_to(ROOT)))
    return {"git_head": git("rev-parse", "HEAD"), "engine_tree": git("rev-parse", f"HEAD:{ENGINE.relative_to(ROOT)}"),
            "engine_py_sha256": h.hexdigest(), "engine_dirty": bool(dirty), "simulate_sha256": sha256(ENGINE / "simulate.py")}


def make_cfg(home: str, away: str, week: int, *, h2h="off", season: int = 2026, semantics: bool = True) -> dict:
    """Same settings as the TNF NFL-43 lock config; only teams, as-of week and h2h policy differ.
    History = weeks 1..week-1 only (point in time)."""
    if week < 2:
        raise ValueError("need at least one prior week")
    t = json.loads(TEMPLATE.read_text())
    t["config_id"] = f"nfl49_bt_{season}_{week:02d}_{away}_{home}"
    t["game"] = {"home": home, "away": away, "season": season, "week_asof_exclusive": week,
                 "game_id": f"{season}_{week:02d}_{away}_{home}"}
    t["history"]["teams"] = sorted([home, away])
    t["history"]["season"] = season
    t["history"]["weeks_inclusive"] = list(range(1, week))
    t["defense_interaction"] = copy.deepcopy(t.get("defense_interaction") or {"mode": "h2h_only"})
    t["defense_interaction"]["h2h"] = h2h
    t["set_label"] = "nfl49_walk_forward_BACKTEST_already_seen_data"
    if not semantics:
        t.pop("semantics", None)
    return t
