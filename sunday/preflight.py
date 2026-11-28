"""Sunday preflight (NFL-92).

Uses pipeline.freshness for source age. Does not fetch, does not simulate, and does not change projection_ready.

Result words:
  PASS     every critical and required check passed, and every declared research layer returned OK
  PARTIAL  critical checks passed; a required input or a declared layer is incomplete and is named
  BLOCKED  a critical check failed (identity, leakage, roles, engine, disk, or odds when --market)

Official inactives that are NOT_YET before T-90 are accepted. They are not a made-up inactive list.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

from pipeline import freshness, hooks

CODE_ROOT = Path(__file__).resolve().parents[1]
# FRESH is the pipeline's pass word. PASS is this command's own pass word.
ACCEPTABLE = {"PASS", "FRESH", "NOT_REQUIRED", "NOT_YET"}
SKEW = freshness.CLOCK_SKEW
GAME_ID = re.compile(r"^[0-9]{4}_[0-9]{2}_[A-Z]{2,3}_[A-Z]{2,3}$")
FREEZE_STAMP = re.compile(r"freeze_(\d{8}T\d{6}Z)")
LOCK_STAMP = re.compile(r"^\d{8}T\d{6}Z$")
SKILL = {"QB", "RB", "WR", "TE", "FB"}
LAYERS = (
    ("NFL-87", "sunday.layers.orchestration", "Per-game orchestration registry"),
    ("NFL-88", "sunday.layers.matchup", "Coverage and advanced-stat research"),
    ("NFL-89", "sunday.layers.players", "Player opportunity board"),
    ("NFL-90", "sunday.layers.scripts", "Three game scripts and independent model runs"),
    ("NFL-91", "sunday.layers.market_board", "Market comparison and adversarial board"),
)
ENGINE_FILES = (
    "core/possession_engine_v0/simulate.py",
    "core/possession_engine_v0/config_load.py",
    "core/possession_engine_v0/SEMANTICS_BOUNDS.md",
    "known_flags/KNOWN_LIMITATIONS.json",
)
# Directories this command lists and does not read. Postgame grades, final plays, and gamebooks live here.
POSTGAME_DIRS = (
    "grading/results",
    "data/historical/playlogs",
    "data/historical/projections",
    "data/gamebooks",
)
SLIM_FRESHNESS = ("source", "status", "reason", "retrieved_utc", "as_of_utc", "as_of_basis",
                  "age_minutes", "max_age_minutes", "cadence")


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat()


def parse_as_of(value: str) -> datetime:
    got = freshness.parse_utc(value)
    if got is None:
        raise ValueError(f"as-of {value!r} is not a timestamp")
    return got.astimezone(timezone.utc).replace(microsecond=0)


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def git_sha(code: Path = CODE_ROOT) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(code), "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL, timeout=5).strip()
    except (OSError, subprocess.SubprocessError):
        return None


def check(cid: str, level: str, status: str, detail: str) -> dict:
    return {"id": cid, "level": level, "status": status, "detail": detail}


def rollup(checks: list[dict], layers: list[dict]) -> tuple[str, list[str], list[str], list[str]]:
    critical = [c["id"] for c in checks if c["level"] == "critical" and c["status"] not in ACCEPTABLE]
    required = [c["id"] for c in checks if c["level"] == "required" and c["status"] not in ACCEPTABLE]
    layer_gaps = [layer["issue"] for layer in layers if layer.get("status") != "OK"]
    if critical:
        result = "BLOCKED"
    elif required or layer_gaps:
        result = "PARTIAL"
    else:
        result = "PASS"
    return result, critical, required, layer_gaps


def canonical_dumps(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def with_hash(body: dict) -> dict:
    """Identity of the projection, excluding runtime, memory, and output paths."""
    hashed = {k: v for k, v in body.items() if k not in {"runtime", "artifacts", "canonical_sha256"}}
    out = dict(body)
    out["canonical_sha256"] = sha256_bytes(canonical_dumps(hashed).encode())
    return out


def valid_game_id(game_id: str) -> bool:
    return bool(GAME_ID.fullmatch(game_id or ""))


def probe_layers() -> list[dict]:
    rows = []
    for issue, mod, what in LAYERS:
        try:
            spec = importlib.util.find_spec(mod)
        except (ModuleNotFoundError, ValueError):
            spec = None
        if spec is None:
            rows.append({"issue": issue, "module": mod, "status": "UNAVAILABLE",
                         "detail": f"{what}. No module is registered, so nothing was executed."})
        else:
            rows.append({"issue": issue, "module": mod, "status": "PRESENT_NOT_CALLED",
                         "detail": f"{what}. The module imports. Import is not a completed analysis, so it was not called."})
    return rows


def _slot(row: dict) -> str:
    return str(row.get("slot") or row.get("position") or "").upper()


def role_report(pk: dict | None) -> tuple[list[dict], dict]:
    """Critical structure check plus a required listed-QB check. Returns (checks, summary)."""
    if not pk:
        return [check("roles", "critical", "FAIL", "No pregame packet, so roles cannot be read."),
                check("listed_qb", "required", "FAIL", "No pregame packet.")], {}
    game = pk.get("game") or {}
    teams = pk.get("teams") if isinstance(pk.get("teams"), dict) else {}
    listed = game.get("listed_qbs") if isinstance(game.get("listed_qbs"), dict) else {}
    problems, qb_gaps, summary = [], [], {}
    for abbr in (game.get("away"), game.get("home")):
        if not abbr:
            problems.append("schedule is missing a team code")
            continue
        block = teams.get(abbr)
        if not isinstance(block, dict):
            problems.append(f"{abbr}: no team block")
            continue
        depth = block.get("depth_chart") if isinstance(block.get("depth_chart"), dict) else {}
        starters = depth.get("starters") if isinstance(depth.get("starters"), list) else []
        if depth.get("status") != "OK" or not starters:
            problems.append(f"{abbr}: depth chart missing or not OK")
        slots = {_slot(row) for row in starters if isinstance(row, dict)}
        qbs = [row.get("player") for row in starters if isinstance(row, dict) and _slot(row) == "QB" and row.get("player")]
        if "QB" not in slots:
            problems.append(f"{abbr}: no QB starter")
        if not (slots & {"RB", "WR", "TE"}):
            problems.append(f"{abbr}: no RB, WR, or TE starter")
        injuries = block.get("injuries")
        if not isinstance(injuries, dict):
            problems.append(f"{abbr}: no injury/availability block")
            injuries = {}
        name = listed.get(abbr)
        if not name:
            problems.append(f"{abbr}: listed quarterback missing")
        elif qbs and str(name).casefold() not in {str(q).casefold() for q in qbs}:
            qb_gaps.append(f"{abbr}: listed QB {name} is not a QB starter ({', '.join(qbs)})")
        report = injuries.get("official_report") if isinstance(injuries.get("official_report"), list) else []
        flagged = []
        for row in report:
            if not isinstance(row, dict):
                continue
            game_status = str(row.get("game_status") or "")
            practice = str(row.get("practice_status") or "")
            if game_status in {"Out", "Doubtful", "Questionable"} or "Did Not Participate" in practice:
                flagged.append({"player": row.get("player"), "position": row.get("position"),
                                "game_status": row.get("game_status"), "practice_status": row.get("practice_status")})
        flagged.sort(key=lambda r: (str(r.get("player") or ""), str(r.get("position") or "")))
        skill = [{"slot": _slot(row), "player": row.get("player")} for row in starters
                 if isinstance(row, dict) and _slot(row) in SKILL]
        skill.sort(key=lambda r: (r["slot"], str(r.get("player") or "")))
        summary[abbr] = {"listed_qb": name, "qb_starters": qbs, "skill_starters": skill,
                         "starter_count": len(starters), "availability_flags": flagged,
                         "depth_chart_as_of": depth.get("as_of")}
    roles = check("roles", "critical", "FAIL" if problems else "PASS",
                  "; ".join(problems) if problems else "Both clubs have a depth chart, a QB, a skill starter, and an availability block.")
    listed_check = check("listed_qb", "required", "FAIL" if qb_gaps else "PASS",
                         "; ".join(qb_gaps) if qb_gaps else "Listed quarterback is a QB starter on the depth chart.")
    return [roles, listed_check], summary


def _stamp_from_freeze_name(path: Path) -> datetime | None:
    match = FREEZE_STAMP.search(path.name)
    if not match:
        return None
    return datetime.strptime(match.group(1), "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)


def list_freeze_files(pk: dict, base: Path) -> list[Path]:
    game = pk.get("game") or {}
    away, home, date = game.get("away"), game.get("home"), str(game.get("date") or "")
    if not base.is_dir() or not away or not home:
        return []
    dirs = [d for d in base.glob(f"*_{away}@{home}") if d.is_dir() and (not date or d.name.startswith(date))]
    return sorted((f for d in dirs for f in d.glob("freeze_*.json")), key=lambda f: f.name)


def classify_freezes(pk: dict, repo: Path, as_of: datetime) -> tuple[Path | None, list[dict]]:
    """Newest freeze whose filename stamp is at or before as-of. Later files are not opened."""
    chosen = None
    skipped = []
    for path in list_freeze_files(pk, repo / "pregame" / "price_freezes"):
        stamp = _stamp_from_freeze_name(path)
        if stamp is None or stamp > as_of + SKEW:
            skipped.append({"path": rel(repo, path), "reason": "freeze filename is after as-of or has no stamp; not opened"})
            continue
        chosen = path
    return chosen, skipped


def staged_freeze_status(pk: dict, chosen: Path | None, skipped: list[dict]) -> dict:
    """Call the existing four-book hook on the eligible file only."""
    if chosen is None:
        why = "No price freeze at or before as-of."
        if skipped:
            why += " Later freeze files were not opened."
        return {"status": "MISSING", "reason": why}
    with tempfile.TemporaryDirectory() as tmp:
        game = pk.get("game") or {}
        dest = Path(tmp) / f"{game.get('date')}_{game.get('away')}@{game.get('home')}"
        dest.mkdir(parents=True)
        (dest / chosen.name).write_bytes(chosen.read_bytes())
        return hooks.four_book_prices(pk, base=Path(tmp))


def source_times(pk: dict) -> list[tuple[str, str]]:
    """Retrieval and publication stamps. Kickoff is a schedule fact and is not a source stamp."""
    found = []

    def add(label, value):
        if value:
            found.append((label, str(value)))

    add("packet.generated_utc", pk.get("generated_utc"))
    for name, rec in (pk.get("sources") or {}).items():
        if isinstance(rec, dict):
            for key in ("retrieved_utc", "source_updated_at", "as_of_utc"):
                add(f"sources.{name}.{key}", rec.get(key))
    books = pk.get("books") if isinstance(pk.get("books"), dict) else {}
    add("books.retrieved_utc", books.get("retrieved_utc"))
    for book, stamp in (books.get("book_retrieved_utc") or {}).items():
        add(f"books.book_retrieved_utc.{book}", stamp)
    markets = books.get("markets") if isinstance(books.get("markets"), dict) else {}
    for market, block in markets.items():
        if not isinstance(block, dict):
            continue
        for bname, row in (block.get("books") or {}).items():
            if isinstance(row, dict):
                add(f"books.markets.{market}.{bname}.last_update", row.get("last_update"))
    weather = pk.get("weather") if isinstance(pk.get("weather"), dict) else {}
    for key in ("retrieved_utc", "source_updated_at"):
        add(f"weather.{key}", weather.get(key))
    for team, block in (pk.get("teams") or {}).items():
        if isinstance(block, dict):
            depth = block.get("depth_chart") if isinstance(block.get("depth_chart"), dict) else {}
            add(f"teams.{team}.depth_chart.as_of", depth.get("as_of"))
    return found


def leakage_times(pk: dict | None, as_of: datetime) -> list[str]:
    if not pk:
        return []
    late = []
    for label, raw in source_times(pk):
        got = freshness.parse_utc(raw)
        if got is not None and got > as_of + SKEW:
            late.append(f"{label} {raw} is after as-of {iso(as_of)}")
    return late


def postgame_files(repo: Path, game_id: str, away: str | None, home: str | None) -> list[dict]:
    """Names only. File contents are not read."""
    tokens = {game_id}
    if away and home:
        tokens.update({f"{away}_{home}", f"{home}_{away}", f"{away}@{home}", f"{home}@{away}"})
    found = []
    for folder in POSTGAME_DIRS:
        root = repo / folder
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if path.is_file() and any(token in path.name for token in tokens):
                found.append({"path": rel(repo, path), "reason": "postgame or final-stat path; not read"})
    runs = repo / "runs"
    if runs.is_dir() and away and home:
        for path in runs.iterdir():
            if path.is_dir() and away in path.name and home in path.name:
                for child in path.rglob("*"):
                    if child.is_file():
                        found.append({"path": rel(repo, child),
                                      "reason": "game run folder sits beside postgame files; not read"})
    found.sort(key=lambda row: row["path"])
    return found


def _lock_stamp(directory: Path) -> datetime | None:
    if not LOCK_STAMP.fullmatch(directory.name):
        return None
    return datetime.strptime(directory.name, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)


def snapshot_cite(repo: Path, game_id: str, as_of: datetime, kickoff: datetime | None) -> tuple[dict, list[dict], list[str]]:
    """Cite a lock only when its directory stamp is at or before as-of and before kickoff. Later locks are not opened."""
    base = repo / "snapshots" / game_id
    excluded: list[dict] = []
    opened: list[str] = []
    if not base.is_dir():
        return {"status": "ABSENT", "detail": "No snapshots directory for this game."}, excluded, opened
    chosen = None
    for lock in sorted(base.glob("*/LOCK.json")):
        stamp = _lock_stamp(lock.parent)
        if stamp is None or stamp > as_of + SKEW or (kickoff is not None and stamp >= kickoff):
            excluded.append({"path": rel(repo, lock.parent),
                             "reason": "snapshot directory is after as-of or at/after kickoff; not opened"})
            continue
        chosen = lock
    if chosen is None:
        return {"status": "EXCLUDED", "detail": "No locked snapshot at or before as-of.",
                "excluded": [row["path"] for row in excluded]}, excluded, opened
    opened.append(rel(repo, chosen))
    try:
        data = json.loads(chosen.read_text())
    except (OSError, ValueError) as e:
        return {"status": "EXCLUDED", "detail": f"{chosen.name} unreadable: {e}"}, excluded, opened
    locked = freshness.parse_utc(data.get("locked_utc"))
    if locked is None or locked > as_of + SKEW or (kickoff is not None and locked >= kickoff):
        excluded.append({"path": rel(repo, chosen), "reason": "LOCK.json timestamp is after the cutoff"})
        return {"status": "EXCLUDED", "detail": "Lock file timestamp is after the cutoff. Summary was not read."}, excluded, opened
    if data.get("projection_ready") is not False:
        return {"status": "EXCLUDED", "detail": "Lock does not keep projection_ready false. Summary was not read."}, excluded, opened
    summary_path = chosen.parent / "summary.json"
    points = None
    if summary_path.is_file():
        opened.append(rel(repo, summary_path))
        try:
            summary = json.loads(summary_path.read_text())
            points = summary.get("points")
        except (OSError, ValueError):
            points = None
    sim = data.get("sim") if isinstance(data.get("sim"), dict) else {}
    return {"status": "CITED_NOT_RERUN", "path": rel(repo, chosen.parent), "locked_utc": data.get("locked_utc"),
            "n": sim.get("n"), "seed": sim.get("seed"), "config_id": data.get("config_id"), "points": points,
            "projection_ready": False,
            "detail": "Locked at or before as-of and before kickoff. This command did not re-simulate."}, excluded, opened


def cite_team_projection(pk: dict | None, as_of: datetime) -> dict:
    if not pk or not isinstance(pk.get("team_projection"), dict):
        return {"status": "ABSENT", "detail": "Packet has no team_projection block."}
    generated = freshness.parse_utc(pk.get("generated_utc"))
    if generated is None or generated > as_of + SKEW:
        return {"status": "EXCLUDED", "detail": "team_projection belongs to a packet generated after as-of."}
    block = pk["team_projection"]
    samplers = {}
    for name, sample in (block.get("samplers") or {}).items():
        if isinstance(sample, dict):
            samplers[name] = {key: sample.get(key) for key in
                              ("home_points", "away_points", "home_margin", "total", "home_win", "away_win")}
    return {"status": "CITED_NOT_RERUN", "engine": block.get("engine"), "trials": block.get("trials"),
            "projection_status": block.get("status"), "samplers": samplers,
            "detail": "Copied from the pregame packet. This command did not re-simulate."}


def engine_checks(code: Path, away: str | None, home: str | None) -> tuple[list[dict], list[str]]:
    opened = []
    missing = [name for name in ENGINE_FILES if not (code / name).is_file()]
    flags_path = code / "known_flags" / "KNOWN_LIMITATIONS.json"
    ready_ok = False
    detail = f"Python {sys.version.split()[0]}."
    if missing:
        detail += " Missing " + ", ".join(missing) + "."
    elif sys.version_info < (3, 11):
        detail += " Python 3.11 or newer is required."
    else:
        try:
            flags = json.loads(flags_path.read_text())
            opened.append(rel(code, flags_path))
            ready_ok = flags.get("projection_ready") is False
            if not ready_ok:
                detail += " known_flags projection_ready is not false. This command will not change it."
            else:
                detail += " Possession-engine files are present and projection_ready is false."
        except (OSError, ValueError) as e:
            detail += f" known_flags unreadable: {e}."
    engine = check("engine", "critical", "PASS" if ready_ok and not missing and sys.version_info >= (3, 11) else "FAIL", detail)
    config = None
    folder = code / "core" / "possession_engine_v0" / "config"
    if away and home and folder.is_dir():
        hits = [p for p in sorted(folder.glob("*.json"))
                if away.casefold() in p.name.casefold() and home.casefold() in p.name.casefold()]
        config = hits[-1] if hits else None
    if config is None:
        config_check = check("engine_config", "required", "MISSING",
                             "No possession-engine config file for this matchup. The research packet is still written; nothing is simulated.")
    else:
        digest = sha256_bytes(config.read_bytes())
        opened.append(rel(code, config))
        config_check = check("engine_config", "required", "PASS",
                             f"{rel(code, config)} sha256 {digest}. Not loaded into a simulation.")
    return [engine, config_check], opened


def disk_and_runtime(out_dir: Path, min_free_mb: int) -> tuple[list[dict], int | None]:
    free = None
    try:
        free = shutil.disk_usage(out_dir).free
    except OSError as e:
        disk = check("disk", "critical", "FAIL", f"Could not read free space: {e}")
    else:
        need = min_free_mb * 1024 * 1024
        disk = check("disk", "critical", "PASS" if free >= need else "FAIL",
                     "Output directory has the requested free space." if free >= need
                     else f"Free space is below the requested {min_free_mb} MB.")
    probe = out_dir / ".sunday_probe"
    try:
        probe.write_text("ok", encoding="utf-8")
        ok = probe.read_text(encoding="utf-8") == "ok"
    except OSError as e:
        runtime = check("runtime", "critical", "FAIL", f"Output directory is not writable: {e}")
        ok = False
    else:
        runtime = check("runtime", "critical", "PASS" if ok else "FAIL",
                        "Wrote and read a probe file in the output directory." if ok else "Probe file did not round-trip.")
    finally:
        try:
            probe.unlink(missing_ok=True)
        except OSError:
            pass
    return [disk, runtime], free


def identity_check(pk: dict | None, game_id: str, entry: dict | None, as_of: datetime,
                   load_error: str | None) -> tuple[dict, datetime | None]:
    if load_error or not pk:
        return check("identity", "critical", "FAIL", load_error or "Pregame packet could not be read."), None
    game = pk.get("game") if isinstance(pk.get("game"), dict) else {}
    reasons = []
    if game.get("game_id") != game_id:
        reasons.append(f"packet game_id is {game.get('game_id')!r}, not {game_id}")
    for field in ("away", "home", "date", "kickoff_et", "week", "season"):
        if game.get(field) in (None, ""):
            reasons.append(f"schedule field {field} is missing")
    if entry is None:
        reasons.append("game is not on the schedule index")
    else:
        for field in ("away", "home", "date", "week"):
            if str(entry.get(field)) != str(game.get(field)):
                reasons.append(f"index {field} {entry.get(field)!r} does not match packet {game.get(field)!r}")
    kickoff = freshness.kickoff_utc(pk)
    if kickoff is None:
        reasons.append("kickoff could not be resolved")
    elif as_of >= kickoff:
        reasons.append(f"as-of {iso(as_of)} is at or after kickoff {iso(kickoff)}")
    detail = "; ".join(reasons) if reasons else f"Schedule identity matches. Kickoff {iso(kickoff)}."
    return check("identity", "critical", "FAIL" if reasons else "PASS", detail), kickoff


def phase_check(pk: dict | None, inactives_status: str | None) -> dict:
    if not pk or not isinstance(pk.get("phase_ledger"), list) or not pk["phase_ledger"]:
        return check("phases", "required", "MISSING", "Packet has no phase ledger.")
    gaps = []
    for phase in pk["phase_ledger"]:
        if not isinstance(phase, dict):
            gaps.append("unreadable phase row")
            continue
        status = phase.get("status")
        if phase.get("phase") == 15 and inactives_status == "NOT_YET" and status in {"PENDING", "NOT_YET"}:
            continue
        if status not in {"AUTO", "NOT_REQUIRED"}:
            gaps.append(f"phase {phase.get('phase')} {status}")
    if gaps:
        return check("phases", "required", "GAP", "; ".join(gaps))
    return check("phases", "required", "PASS", "Phase ledger is AUTO, or phase 15 is still before T-90.")


def odds_market_check(pk: dict | None, market: bool) -> dict | None:
    if not market:
        return None
    books = pk.get("books") if pk and isinstance(pk.get("books"), dict) else {}
    markets = books.get("markets") if isinstance(books.get("markets"), dict) else {}
    if "spread" in markets or "total" in markets:
        return check("odds_snapshot", "critical", "PASS", "Packet odds snapshot has a spread or a total.")
    return check("odds_snapshot", "critical", "FAIL", "Market comparison was requested and the packet has no spread or total snapshot.")


def slim_freshness(rows: list[dict], market: bool) -> tuple[list[dict], list[dict]]:
    stored, checks = [], []
    for row in rows:
        stored.append({key: row.get(key) for key in SLIM_FRESHNESS})
        level = "critical" if market and row.get("source") == "odds" else "required"
        checks.append(check(f"freshness.{row.get('source')}", level, str(row.get("status") or "MISSING"),
                            str(row.get("reason") or "")))
    return stored, checks


def fresh_rows(pk: dict, as_of: datetime, freeze_res: dict) -> list[dict]:
    return freshness.check(pk, as_of, {"four_book_prices": lambda _pk: freeze_res})


def evaluate(*, repo: Path, game_id: str, pk: dict | None, packet_sha: str | None, packet_rel: str | None,
             load_error: str | None, entry: dict | None, as_of: datetime, market: bool, out_dir: Path,
             min_free_mb: int, code: Path = CODE_ROOT, command: str) -> dict:
    identity, kickoff = identity_check(pk, game_id, entry, as_of, load_error)
    role_checks, roles = role_report(pk)
    game_block = (pk or {}).get("game") if isinstance((pk or {}).get("game"), dict) else {}
    away = game_block.get("away") if pk else (entry or {}).get("away")
    home = game_block.get("home") if pk else (entry or {}).get("home")
    late = leakage_times(pk, as_of)
    freeze_chosen, freeze_skipped = (None, [])
    freeze_res = {"status": "MISSING", "reason": "No packet, so no price freeze was considered."}
    if pk:
        freeze_chosen, freeze_skipped = classify_freezes(pk, repo, as_of)
        freeze_res = staged_freeze_status(pk, freeze_chosen, freeze_skipped)
        pulled = freshness.parse_utc(freeze_res.get("retrieved_utc"))
        if pulled is not None and pulled > as_of + SKEW:
            late.append(f"price freeze pulled_utc {freeze_res.get('retrieved_utc')} is after as-of")
            freeze_res = {"status": "MISSING", "reason": "Eligible freeze filename was opened and its pulled_utc is after as-of. Not used."}
    rows = fresh_rows(pk, as_of, freeze_res) if pk else []
    stored, fresh_checks = slim_freshness(rows, market)
    inactives = next((row.get("status") for row in rows if row.get("source") == "official_inactives"), None)
    snap, snap_excluded, snap_opened = snapshot_cite(repo, game_id, as_of, kickoff) if valid_game_id(game_id) else (
        {"status": "ABSENT", "detail": "Game id is not a schedule id."}, [], [])
    excluded = postgame_files(repo, game_id, away, home) + freeze_skipped + snap_excluded
    excluded.sort(key=lambda row: row["path"])
    leak = check("leakage", "critical", "FAIL" if late else "PASS",
                 "; ".join(late) if late else "Source stamps are at or before as-of. Postgame paths were listed and not read.")
    engine, engine_opened = engine_checks(code, away, home)
    space, free_bytes = disk_and_runtime(out_dir, min_free_mb)
    phases = phase_check(pk, inactives)
    odds = odds_market_check(pk, market)
    checks = [identity, *role_checks, leak, *engine, *space, phases, *fresh_checks]
    if odds is not None:
        checks.append(odds)
    layers = probe_layers()
    result, critical_ids, required_ids, layer_gaps = rollup(checks, layers)
    inputs = []
    if entry is not None:
        inputs.append("pregame/packets/latest.json")
    if packet_rel and packet_sha is not None:
        inputs.append(packet_rel)
    if freeze_chosen is not None:
        inputs.append(rel(repo, freeze_chosen))
    inputs.extend(engine_opened)
    inputs.extend(snap_opened)
    inputs = sorted(set(inputs))
    game = game_block
    body = {
        "schema": "sunday-projection/1",
        "projection_ready": False,
        "research_only": True,
        "result": result,
        "game_id": game_id,
        "as_of_utc": iso(as_of),
        "kickoff_utc": iso(kickoff) if kickoff else None,
        "command": command,
        "git_sha": git_sha(code),
        "scheduler": {"status": "NOT_THIS_COMMAND",
                      "detail": "Manual local execution. GitHub Actions is not invoked and no schedule is registered."},
        "game": {"game_id": game_id, "season": (game or {}).get("season"), "week": (game or {}).get("week"),
                 "away": (game or {}).get("away"), "home": (game or {}).get("home"), "date": (game or {}).get("date"),
                 "kickoff_et": (game or {}).get("kickoff_et"), "slot": (entry or {}).get("slot"),
                 "listed_qbs": (game or {}).get("listed_qbs")},
        "source_packet": {"path": packet_rel, "sha256": packet_sha, "generated_utc": (pk or {}).get("generated_utc"),
                          "load_error": load_error},
        "checks": checks,
        "critical_ids": critical_ids,
        "required_ids": required_ids,
        "layer_gaps": layer_gaps,
        "freshness": stored,
        "roles": roles,
        "leakage": {"status": "FAIL" if late else "PASS", "late_stamps": late, "excluded": excluded,
                    "inputs_read": inputs},
        "layers": layers,
        "cited_outputs": {"team_projection": cite_team_projection(pk, as_of), "locked_snapshot": snap,
                          "hundred_k": {"status": "NOT_RUN",
                                        "detail": "This command does not call pipeline.sim100k and does not start trials."}},
        "market_comparison_requested": market,
    }
    packet = with_hash(body)
    packet["_disk_free_bytes"] = free_bytes  # stripped by the writer before the file is hashed again; see execute
    return packet
