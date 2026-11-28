#!/usr/bin/env python3
"""DEN@PIT live poller. Research only. No Odds API. Stops on FINAL."""
from __future__ import annotations

import csv
import json
import re
import shutil
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
EVENT = "401873083"
RUN = Path("/workspace/nfl-database/runs/2026-11-27_DEN@PIT")
PBP = RUN / "pbp"
PLAYLOG = Path("/workspace/nfl-database/playlogs/2026_wk12/DEN_PIT.csv")
LOG = PBP / "poll.log"
PIDFILE = PBP / "poll.pid"
FINAL_FLAG = PBP / "GAME_FINAL"
INTERVAL = 150  # 2.5 minutes
UA = "BlitzNFLResearch/1.0 (DEN-PIT live pbp logger)"
SUMMARY_URL = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={EVENT}"
CORE_URL = (
    "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl"
    f"/events/{EVENT}/competitions/{EVENT}/plays?limit=400"
)
HOME, AWAY = "PIT", "DEN"

# Rico legs (unique rows; slips noted)
LEGS = [
    {"id": "coleman_atd", "slips": "A,B", "player": "Jonah Coleman", "market": "anytime TD", "threshold": 1, "kind": "atd"},
    {"id": "freiermuth_2rec", "slips": "A,B", "player": "Pat Freiermuth", "market": "2+ receptions", "threshold": 2, "kind": "rec"},
    {"id": "coleman_70rr", "slips": "A,B", "player": "Jonah Coleman", "market": "70+ rush+rec yds", "threshold": 70, "kind": "rr"},
    {"id": "sutton_15recyds", "slips": "A,B", "player": "Courtland Sutton", "market": "15+ rec yds", "threshold": 15, "kind": "recyds"},
    {"id": "engram_2rec", "slips": "A,B", "player": "Evan Engram", "market": "2+ receptions", "threshold": 2, "kind": "rec"},
    {"id": "warren_60rr", "slips": "A,B", "player": "Jaylen Warren", "market": "60+ rush+rec yds", "threshold": 60, "kind": "rr"},
    {"id": "sutton_30recyds", "slips": "C", "player": "Courtland Sutton", "market": "30+ rec yds", "threshold": 30, "kind": "recyds"},
    {"id": "engram_o2p5rec", "slips": "C", "player": "Evan Engram", "market": "over 2.5 receptions", "threshold": 3, "kind": "rec"},
    {"id": "warren_2rec", "slips": "C", "player": "Jaylen Warren", "market": "2+ receptions", "threshold": 2, "kind": "rec"},
    {"id": "warren_atd", "slips": "C", "player": "Jaylen Warren", "market": "anytime TD", "threshold": 1, "kind": "atd"},
    {"id": "coleman_1h_atd", "slips": "C", "player": "Jonah Coleman", "market": "1st-half anytime TD", "threshold": 1, "kind": "atd_1h"},
    {"id": "metcalf_15recyds", "slips": "C", "player": "DK Metcalf", "market": "15+ rec yds", "threshold": 15, "kind": "recyds"},
    {"id": "u51p5", "slips": "C", "player": "", "market": "alternate game total Under 51.5", "threshold": 51.5, "kind": "total_under"},
]

PLAYER_ALIASES = {
    "Jonah Coleman": ["jonah coleman", "j.coleman", "j. coleman", "coleman"],
    "Pat Freiermuth": ["pat freiermuth", "p.freiermuth", "p. freiermuth", "freiermuth"],
    "Courtland Sutton": ["courtland sutton", "c.sutton", "c. sutton", "sutton"],
    "Evan Engram": ["evan engram", "e.engram", "e. engram", "engram"],
    "Jaylen Warren": ["jaylen warren", "j.warren", "j. warren", "warren"],
    "DK Metcalf": ["dk metcalf", "d.k. metcalf", "d.k metcalf", "d.metcalf", "d. metcalf", "metcalf"],
}

# Last-name-only aliases that are unsafe if another player shares the name.
UNSAFE_LAST = {"coleman"}  # only use if box has exactly one Coleman


def now_et() -> datetime:
    return datetime.now(ET)


def stamp_human() -> str:
    n = now_et()
    return n.strftime("%Y-%m-%d ") + n.strftime("%I:%M:%S %p").lstrip("0") + " ET"


def stamp_file() -> str:
    return now_et().strftime("%Y%m%d_%H%M%S")


def log(msg: str) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    line = f"{stamp_human()} {msg}"
    with LOG.open("a") as f:
        f.write(line + "\n")
    print(line, flush=True)


def fetch(url: str, dest: Path, timeout: int = 25) -> bool:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
        dest.write_bytes(data)
        return True
    except Exception as e:
        log(f"fetch failed {url} err={e}")
        return False


def norm(s: str) -> str:
    s = (s or "").lower()
    s = s.replace("d.k.", "dk").replace("d.k", "dk")
    s = re.sub(r"[^a-z0-9. ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def name_matches(full: str, candidate: str, box_last_counts: dict[str, int] | None = None) -> bool:
    c = norm(candidate)
    f = norm(full)
    if not c:
        return False
    if c == f or f in c or c in f:
        return True
    for a in PLAYER_ALIASES.get(full, []):
        if c == a or c.endswith(" " + a) or c.startswith(a + " "):
            if a in UNSAFE_LAST:
                last = a
                if box_last_counts and box_last_counts.get(last, 0) > 1:
                    return False
            return True
    # initial + last: "j.coleman"
    parts = f.split()
    if len(parts) >= 2:
        ini_last = f"{parts[0][0]}.{parts[-1]}"
        ini_sp = f"{parts[0][0]}. {parts[-1]}"
        if c == ini_last or c == ini_sp or c.endswith(parts[-1]) and parts[0][0] in c:
            if parts[-1] in UNSAFE_LAST and box_last_counts and box_last_counts.get(parts[-1], 0) > 1:
                return False
            if parts[-1] in c:
                return True
    return False


def header_status(summary: dict):
    comp = summary["header"]["competitions"][0]
    st = comp["status"]
    typ = st.get("type") or {}
    scores = {}
    home_abbr = away_abbr = None
    for c in comp["competitors"]:
        abbr = c["team"]["abbreviation"]
        scores[abbr] = int(c.get("score") or 0)
        if c.get("homeAway") == "home":
            home_abbr = abbr
        else:
            away_abbr = abbr
    completed = bool(typ.get("completed")) or typ.get("name") in ("STATUS_FINAL", "STATUS_FINAL_OVERTIME")
    return {
        "name": typ.get("name") or "",
        "detail": typ.get("detail") or typ.get("shortDetail") or "",
        "state": typ.get("state") or "",
        "completed": completed,
        "period": (st.get("period") or typ.get("period") or (comp.get("status") or {}).get("period")),
        "clock": (st.get("displayClock") or ""),
        "scores": scores,
        "home": home_abbr or HOME,
        "away": away_abbr or AWAY,
    }


def iter_drives(summary: dict):
    """Yield unique drives. ESPN often repeats the current drive inside previous."""
    prev = list((summary.get("drives") or {}).get("previous") or [])
    cur = (summary.get("drives") or {}).get("current") or {}
    seen = set()
    drives = []

    def drive_key(d):
        if d.get("id"):
            return ("id", str(d.get("id")))
        plays = d.get("plays") or []
        pids = tuple(str(p.get("id") or "") for p in plays if p.get("id"))
        if pids:
            return ("plays", pids)
        team = (d.get("team") or {}).get("abbreviation") or ""
        start = (plays[0].get("clock") or {}).get("displayValue") if plays else ""
        text0 = (plays[0].get("text") if plays else "") or ""
        return ("fb", team, start, text0, len(plays))

    for d in prev:
        k = drive_key(d)
        if k in seen:
            continue
        seen.add(k)
        drives.append(d)
    if cur.get("plays"):
        k = drive_key(cur)
        if k not in seen:
            drives.append(cur)
    for i, drv in enumerate(drives):
        yield i, drv


def offense_of(drv: dict, play: dict, teams: dict) -> str:
    team = (drv.get("team") or {}).get("abbreviation") or ""
    if team:
        return team
    # fallback via start.team id
    start = play.get("start") or {}
    tid = (start.get("team") or {}).get("id")
    if tid and tid in teams:
        return teams[tid]
    return team


def team_id_map(summary: dict) -> dict:
    m = {}
    for c in summary["header"]["competitions"][0]["competitors"]:
        m[str(c["team"]["id"])] = c["team"]["abbreviation"]
        m[str(c["id"])] = c["team"]["abbreviation"]
    return m


def parse_tacklers(text: str) -> list[str]:
    # trailing (...) often tacklers, but also penalties. Prefer last paren group before penalty lines.
    if not text:
        return []
    # drop trailing penalty sentences for the tackle group on the first sentence
    first = text.split("Penalty")[0].split("PENALTY")[0]
    groups = re.findall(r"\(([^()]{1,80})\)", first)
    if not groups:
        return []
    g = groups[-1]
    # skip clock-only or formation already stripped; skip if looks like shotgun already consumed
    if re.fullmatch(r"\d+:\d+", g.strip()) or g.strip().lower() in {"shotgun", "no huddle", "no huddle shotgun"}:
        return []
    if re.match(r"^\d", g.strip()):  # clock at start of play
        return []
    parts = re.split(r";|,| and ", g)
    out = []
    for p in parts:
        p = p.strip()
        if not p or p.lower() in {"shotgun", "no huddle"}:
            continue
        # "tackled by X" already inside
        p = re.sub(r"^(tackled by|tackle by)\s+", "", p, flags=re.I)
        out.append(p)
    return out


def parse_pass_location(text: str) -> str:
    t = text or ""
    m = re.search(r"pass (incomplete )?(short|deep|middle)?\s*(left|right|middle)?", t, re.I)
    if m:
        bits = [x for x in (m.group(2), m.group(3)) if x]
        return " ".join(bits).strip().lower()
    m = re.search(r"\b(short|deep)\s+(left|right|middle)\b", t, re.I)
    if m:
        return f"{m.group(1)} {m.group(2)}".lower()
    return ""


def parse_rush_location(text: str) -> str:
    t = text or ""
    m = re.search(
        r"(up the middle|left end|right end|left guard|right guard|left tackle|right tackle|middle)",
        t,
        re.I,
    )
    return m.group(1).lower() if m else ""


def parse_target(text: str) -> str:
    t = text or ""
    m = re.search(r"pass (?:incomplete )?(?:short |deep |middle )?(?:left |right |middle )?to ([A-Z][A-Za-z'.\-]+(?:\s[A-Z][A-Za-z'.\-]+)?)", t)
    if m:
        return m.group(1)
    m = re.search(r"pass incomplete.*for ([A-Z][A-Za-z'.\-]+(?:\s[A-Z][A-Za-z'.\-]+)?)", t)
    if m:
        return m.group(1)
    return ""


def parse_rusher(text: str, typ: str) -> str:
    t = text or ""
    # "J.Gibbs up the middle" / "J.Gibbs left end" / "J.Coleman scrambles"
    m = re.match(r"^(?:\([^)]+\)\s*)+([A-Z][A-Za-z'.\-]+(?:\s[A-Z][A-Za-z'.\-]+)?)\s+", t)
    # better: after optional formation parens
    t2 = re.sub(r"^(?:\([^)]+\)\s*)+", "", t).strip()
    m = re.match(r"^([A-Z]\.?[A-Za-z'.\-]*(?:\s+[A-Z][A-Za-z'.\-]+)?)\s+", t2)
    if m and typ.lower().find("pass") == -1:
        name = m.group(1)
        if name.lower() not in {"penalty", "timeout", "two"}:
            return name
    return ""


def coverage_and_pressure(text: str, typ: str) -> dict:
    t = (text or "")
    tl = t.lower()
    typ_l = (typ or "").lower()
    ev = {"coverage": "unknown", "coverage_evidence": "unsupported — ESPN PBP does not name man/zone on this play",
          "blitz": "no", "blitz_evidence": "unsupported — no blitz language in play text",
          "pressure": "no", "pressure_evidence": "unsupported — no sack/hurry/hit language in play text"}
    # supported coverage only if explicit
    if re.search(r"\bman coverage\b|\bin man\b|\bpress man\b", tl):
        ev["coverage"] = "man"
        ev["coverage_evidence"] = "supported — play text names man coverage"
    elif re.search(r"\bzone coverage\b|\bcover[- ]?[0-6]\b|\btwo-high\b|\bsingle-high\b|\bin zone\b", tl):
        ev["coverage"] = "zone"
        ev["coverage_evidence"] = "supported — play text names zone/cover shell"
    if re.search(r"\bblitz", tl) or re.search(r"\bblitzed\b|\bblitzes\b|\bthe blitz\b", tl):
        ev["blitz"] = "yes"
        ev["blitz_evidence"] = "supported — play text names a blitz"
    if "sacked" in tl or typ_l == "sack":
        ev["pressure"] = "sack"
        ev["pressure_evidence"] = "supported — sack in play type/text"
    elif re.search(r"hurried|under pressure|pressured|hit as he threw|qb hit|as he was hit", tl):
        ev["pressure"] = "yes"
        ev["pressure_evidence"] = "supported — hurry/pressure/hit language in play text"
    return ev


def is_explosive(typ: str, text: str, yards) -> tuple[str | None, int | None]:
    try:
        y = int(yards) if yards not in (None, "") else 0
    except Exception:
        y = 0
    typ_l = (typ or "").lower()
    tl = (text or "").lower()
    # ignore kickoffs, punts, returns, penalties-only
    if typ_l in {"kickoff", "punt", "field goal", "extra point", "timeout", "end of quarter", "end of half", "end of game", "coin toss", "two-minute warning"}:
        return None, y
    if "kickoff" in typ_l or "punt" in typ_l or "field goal" in typ_l:
        return None, y
    if typ_l in {"penalty", "no play"} and "pass" not in tl and "rush" not in tl and "up the middle" not in tl:
        return None, y
    is_pass = ("pass" in typ_l) or ("pass" in tl and typ_l not in {"rush", "scrambles"})
    is_rush = typ_l in {"rush", "rushing touchdown", "scrambles", "qb kneel"} or (
        not is_pass and re.search(r"up the middle|left end|right end|left guard|right guard|left tackle|right tackle|scrambles", tl)
    )
    if typ_l == "sack" or "sacked" in tl:
        return None, y
    if is_pass and y >= 20:
        return "PASS_20", y
    if is_rush and y >= 10:
        return "RUSH_10", y
    return None, y


def box_index(summary: dict) -> tuple[dict, dict[str, int]]:
    """player displayName -> {rush_yds, rush_td, rec, rec_yds, rec_td, ret_td, team}"""
    out = {}
    last_counts: dict[str, int] = {}
    players = ((summary.get("boxscore") or {}).get("players") or [])
    for team_block in players:
        team = (team_block.get("team") or {}).get("abbreviation") or ""
        by_cat = {}
        for stat in team_block.get("statistics") or []:
            cat = stat.get("name")
            keys = stat.get("keys") or []
            for ath in stat.get("athletes") or []:
                name = (ath.get("athlete") or {}).get("displayName") or ""
                vals = ath.get("stats") or []
                kv = {}
                for i, k in enumerate(keys):
                    if i < len(vals):
                        kv[k] = vals[i]
                by_cat.setdefault(name, {})[cat] = kv
                last = name.split()[-1].lower() if name else ""
                if last:
                    last_counts[last] = last_counts.get(last, 0)  # filled below uniquely
        for name, cats in by_cat.items():
            rush = cats.get("rushing") or {}
            rec = cats.get("receiving") or {}
            krem = cats.get("kickReturns") or {}
            prem = cats.get("puntReturns") or {}
            defn = cats.get("defensive") or {}
            ints = cats.get("interceptions") or {}
            def _i(d, *ks):
                for k in ks:
                    v = d.get(k)
                    if v in (None, "", "--"):
                        continue
                    try:
                        if isinstance(v, str) and "/" in v:
                            return int(v.split("/")[0])
                        if isinstance(v, str) and "-" in v and k.startswith("sacks"):
                            return int(float(v.split("-")[0]))
                        return int(float(v))
                    except Exception:
                        continue
                return 0
            rec_td = _i(rec, "receivingTouchdowns")
            rush_td = _i(rush, "rushingTouchdowns")
            ret_td = _i(krem, "kickReturnTouchdowns") + _i(prem, "puntReturnTouchdowns")
            out[name] = {
                "team": team,
                "rush_att": _i(rush, "rushingAttempts"),
                "rush_yds": _i(rush, "rushingYards"),
                "rush_td": rush_td,
                "rec": _i(rec, "receptions"),
                "rec_yds": _i(rec, "receivingYards"),
                "rec_td": rec_td,
                "tgt": _i(rec, "receivingTargets"),
                "ret_td": ret_td,
                "atd": rush_td + rec_td + ret_td,
            }
            last = name.split()[-1].lower()
            last_counts[last] = last_counts.get(last, 0) + 1
    return out, last_counts


def find_player(box: dict, full: str, last_counts: dict) -> dict | None:
    # exact first
    if full in box:
        return box[full]
    for name, row in box.items():
        if name_matches(full, name, last_counts):
            return row
    return None


def scoring_tds_1h(summary: dict, full: str, last_counts: dict) -> int:
    n = 0
    for sp in summary.get("scoringPlays") or []:
        period = (sp.get("period") or {}).get("number") or sp.get("period")
        try:
            period = int(period)
        except Exception:
            period = 99
        typ = ((sp.get("type") or {}).get("abbreviation") or (sp.get("type") or {}).get("text") or "").lower()
        text = sp.get("text") or ""
        # TD only, not FG/XP/SF
        is_td = "touchdown" in typ or typ in {"td", "std", "pass", "rush"} or "touchdown" in text.lower()
        if typ in {"fg", "field goal", "xp", "extra point", "sf", "safety", "2pt"}:
            continue
        if not is_td and typ not in {"td", "passing touchdown", "rushing touchdown", "return touchdown"}:
            # ESPN often uses type text "Passing Touchdown"
            if "td" not in typ and "touchdown" not in typ and "touchdown" not in text.lower():
                continue
        if period and period > 2:
            continue
        # athlete
        ath = ((sp.get("athlete") or {}).get("displayName") or "")
        if ath and name_matches(full, ath, last_counts):
            n += 1
            continue
        # fallback text match
        if player_in_text(full, text, last_counts):
            # avoid kicking TDs attributed wrongly
            n += 1
    return n


def player_in_text(full: str, text: str, last_counts: dict) -> bool:
    if not text:
        return False
    # strip formation parens then look for initials/name
    t = text
    if name_matches(full, t, last_counts):
        return True
    # token scan
    t2 = re.sub(r"^(?:\([^)]+\)\s*)+", "", t)
    m = re.match(r"^([A-Z]\.?[A-Za-z'.\-]*(?:\s+[A-Z][A-Za-z'.\-]+)?)", t2)
    if m and name_matches(full, m.group(1), last_counts):
        return True
    tgt = parse_target(t)
    if tgt and name_matches(full, tgt, last_counts):
        return True
    return False


def half_over(status: dict, summary: dict) -> bool:
    if status["completed"]:
        return True
    name = (status["name"] or "").upper()
    detail = (status["detail"] or "").lower()
    if "HALFTIME" in name or "half" in detail and "end" in detail:
        return True
    period = status.get("period")
    try:
        if period is not None and int(period) >= 3:
            return True
    except Exception:
        pass
    return False


def build_plays(summary: dict) -> list[dict]:
    teams = team_id_map(summary)
    rows = []
    seen_plays = set()
    for i, drv in iter_drives(summary):
        team = (drv.get("team") or {}).get("abbreviation") or ""
        result = drv.get("displayResult") or drv.get("result") or drv.get("description") or ""
        for p in drv.get("plays") or []:
            pid = str(p.get("id") or "")
            if pid:
                if pid in seen_plays:
                    continue
                seen_plays.add(pid)
            typ = (p.get("type") or {}).get("text") or ""
            per = (p.get("period") or {}).get("number")
            clk = (p.get("clock") or {}).get("displayValue") or ""
            start = p.get("start") or {}
            text = p.get("text") or ""
            off = team or offense_of(drv, p, teams)
            yds = p.get("statYardage") if p.get("statYardage") is not None else ""
            rows.append({
                "quarter": per,
                "clock": clk,
                "down": start.get("down") if start.get("down") not in (None, 0) else "",
                "distance": start.get("distance") if start.get("down") not in (None, 0) else "",
                "down_distance": start.get("downDistanceText") or "",
                "yardline": start.get("possessionText") or "",
                "yards_to_endzone": start.get("yardsToEndzone") if start.get("yardsToEndzone") is not None else "",
                "offense": off,
                "play_type": typ,
                "play_text": text,
                "yards": yds,
                "scoring": "1" if p.get("scoringPlay") else "0",
                "away_score": p.get("awayScore"),
                "home_score": p.get("homeScore"),
                "named_participants": "",
                "drive": i,
                "drive_result": result,
                "yac": p.get("yardsAfterCatch") if p.get("yardsAfterCatch") is not None else "",
                "_raw": p,
            })
    return rows


def write_pbp_csv(rows: list[dict], path: Path) -> None:
    fields = [
        "quarter", "clock", "down", "distance", "down_distance", "yardline", "offense",
        "play_type", "play_text", "yards", "scoring", "away_score", "home_score",
        "named_participants", "drive", "drive_result",
    ]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def write_playlog(rows: list[dict], home: str, away: str) -> None:
    PLAYLOG.parent.mkdir(parents=True, exist_ok=True)
    fields = ["off", "q", "clock", "down", "dist", "yds", "type", "hs", "aw", "text"]
    with PLAYLOG.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            # hs = home score, aw = away score. Summary uses homeScore/awayScore.
            w.writerow({
                "off": r.get("offense") or "",
                "q": r.get("quarter") or "",
                "clock": r.get("clock") or "",
                "down": r.get("down") or "",
                "dist": r.get("distance") or "",
                "yds": r.get("yards") if r.get("yards") not in (None,) else "",
                "type": r.get("play_type") or "",
                "hs": r.get("home_score") if r.get("home_score") is not None else "",
                "aw": r.get("away_score") if r.get("away_score") is not None else "",
                "text": r.get("play_text") or "",
            })


def defense_of(offense: str) -> str:
    if offense == HOME:
        return AWAY
    if offense == AWAY:
        return HOME
    return ""


def write_explosives(rows: list[dict], dest: Path) -> list[dict]:
    fields = [
        "quarter", "clock", "down_distance", "yardline", "offense", "defense",
        "explosive_type", "player", "role", "yards", "yac", "location_depth",
        "tackler_defender", "play_type", "play_text", "evidence",
    ]
    out = []
    for r in rows:
        typ = r.get("play_type") or ""
        text = r.get("play_text") or ""
        kind, y = is_explosive(typ, text, r.get("yards"))
        if not kind:
            continue
        loc = parse_pass_location(text) if kind == "PASS_20" else parse_rush_location(text)
        if kind == "PASS_20":
            player = parse_target(text) or ""
            role = "receiver"
        else:
            player = parse_rusher(text, typ) or ""
            role = "rusher"
        tacklers = parse_tacklers(text)
        off = r.get("offense") or ""
        rec = {
            "quarter": r.get("quarter") or "",
            "clock": r.get("clock") or "",
            "down_distance": r.get("down_distance") or "",
            "yardline": r.get("yardline") or "",
            "offense": off,
            "defense": defense_of(off),
            "explosive_type": kind,
            "player": player,
            "role": role,
            "yards": y if y is not None else r.get("yards"),
            "yac": r.get("yac") or "",
            "location_depth": loc,
            "tackler_defender": "; ".join(tacklers),
            "play_type": typ,
            "play_text": text,
            "evidence": "supported — yards and play type/text from ESPN PBP",
        }
        out.append(rec)
    with dest.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(out)
    return out


def write_defense(rows: list[dict], explosives: list[dict], status: dict, dest: Path) -> None:
    # per-play defensive snapshot and per-drive / team totals
    per_team = {
        HOME: {"plays": 0, "rush_exp": 0, "pass_exp": 0, "sacks": 0, "pressures_supported": 0, "blitz_supported": 0, "man_supported": 0, "zone_supported": 0, "coverage_unknown": 0},
        AWAY: {"plays": 0, "rush_exp": 0, "pass_exp": 0, "sacks": 0, "pressures_supported": 0, "blitz_supported": 0, "man_supported": 0, "zone_supported": 0, "coverage_unknown": 0},
    }
    drive_rows = []
    play_lines = []
    for r in rows:
        typ = r.get("play_type") or ""
        typ_l = typ.lower()
        if typ_l in {"kickoff", "timeout", "end of quarter", "end of half", "end of game", "coin toss", "two-minute warning", "punt", "field goal", "extra point"}:
            # still note special teams briefly? skip coverage profile for non-scrimmage
            if typ_l in {"kickoff", "timeout", "end of quarter", "end of half", "end of game", "coin toss", "two-minute warning"}:
                continue
        text = r.get("play_text") or ""
        ev = coverage_and_pressure(text, typ)
        off = r.get("offense") or ""
        dfn = defense_of(off)
        if dfn in per_team and typ_l not in {"punt", "field goal", "extra point", "penalty"}:
            # count scrimmage-ish plays
            if typ_l or text:
                per_team[dfn]["plays"] += 1
                if ev["coverage"] == "man":
                    per_team[dfn]["man_supported"] += 1
                elif ev["coverage"] == "zone":
                    per_team[dfn]["zone_supported"] += 1
                else:
                    per_team[dfn]["coverage_unknown"] += 1
                if ev["blitz"] == "yes":
                    per_team[dfn]["blitz_supported"] += 1
                if ev["pressure"] in {"yes", "sack"}:
                    per_team[dfn]["pressures_supported"] += 1
                if ev["pressure"] == "sack":
                    per_team[dfn]["sacks"] += 1
        kind, _ = is_explosive(typ, text, r.get("yards"))
        if kind == "RUSH_10" and dfn in per_team:
            per_team[dfn]["rush_exp"] += 1
        if kind == "PASS_20" and dfn in per_team:
            per_team[dfn]["pass_exp"] += 1
        play_lines.append(
            f"- Q{r.get('quarter')} {r.get('clock')} {off or '?'} {r.get('down_distance') or ''} | {typ} | {r.get('yards')} yds | "
            f"cov {ev['coverage']} ({ev['coverage_evidence']}) | blitz {ev['blitz']} ({ev['blitz_evidence']}) | "
            f"pressure {ev['pressure']} ({ev['pressure_evidence']}) | {text}"
        )

    # per-drive summaries
    by_drive: dict[int, list] = {}
    for r in rows:
        by_drive.setdefault(int(r.get("drive") or 0), []).append(r)
    for di, plays in by_drive.items():
        if not plays:
            continue
        off = plays[0].get("offense") or ""
        dfn = defense_of(off)
        result = plays[0].get("drive_result") or ""
        exp_n = 0
        sacks = 0
        blitz = 0
        press = 0
        for p in plays:
            typ = p.get("play_type") or ""
            text = p.get("play_text") or ""
            ev = coverage_and_pressure(text, typ)
            k, _ = is_explosive(typ, text, p.get("yards"))
            if k:
                exp_n += 1
            if ev["pressure"] == "sack":
                sacks += 1
            if ev["blitz"] == "yes":
                blitz += 1
            if ev["pressure"] in {"yes", "sack"}:
                press += 1
        drive_rows.append(
            f"| {di} | {off} | {dfn} | {len(plays)} | {exp_n} | {sacks} | {press} | {blitz} | {result} |"
        )

    lines = []
    lines.append(f"# LIVE DEFENSE — DEN @ PIT")
    lines.append("")
    lines.append(f"**Snapshot:** {stamp_human()} (America/New_York)")
    lines.append(f"**Game:** {status['detail']} | {AWAY} {status['scores'].get(AWAY, 0)}, {HOME} {status['scores'].get(HOME, 0)}")
    lines.append("**Source:** ESPN summary/PBP event 401873083. Research only. Paper / unvetted.")
    lines.append("**Coverage rule:** man/zone and blitz are recorded as **supported** only when the play text names them. Otherwise they are left unknown (not invented). Pressure is **supported** on sack / hurry / hit language. Inferred values, if any, are labeled inferred.")
    lines.append("")
    lines.append("## Team defensive snapshot this game")
    lines.append("| Defense | Scrimmage plays tagged | Expl. rush 10+ allowed | Expl. pass 20+ allowed | Sacks (text/type) | Pressures supported | Blitz supported | Man supported | Zone supported | Coverage unknown |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for team in (HOME, AWAY):
        t = per_team[team]
        lines.append(
            f"| {team} | {t['plays']} | {t['rush_exp']} | {t['pass_exp']} | {t['sacks']} | "
            f"{t['pressures_supported']} | {t['blitz_supported']} | {t['man_supported']} | {t['zone_supported']} | {t['coverage_unknown']} |"
        )
    lines.append("")
    lines.append("## Explosives allowed")
    if not explosives:
        lines.append("None yet (rush 10+ / pass 20+ from ESPN PBP yards).")
    else:
        lines.append("| Q | Clock | Def | Type | Player | Yds | Location/depth | Tackler/defender | Text |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for e in explosives:
            lines.append(
                f"| {e['quarter']} | {e['clock']} | {e['defense']} | {e['explosive_type']} | {e['player']} | "
                f"{e['yards']} | {e['location_depth']} | {e['tackler_defender']} | {e['play_text']} |"
            )
    lines.append("")
    lines.append("## Per drive")
    lines.append("| Drive | Offense | Defense | Plays | Explosives | Sacks | Pressures (supported) | Blitz (supported) | Result |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    lines.extend(drive_rows or ["| — | — | — | 0 | 0 | 0 | 0 | 0 | no drives yet |"])
    lines.append("")
    lines.append("## Strong leans tracker")
    lines.append("")
    lines.append("PR #141 and `PREGAME_PROJECTION.md` labeled **no strong leans and no vetted leans**. Player outputs were withheld; `projection_ready=false`; Ghost6 has not vetted. This tracker does not invent leans.")
    lines.append("")
    lines.append("Comparison items published in the lock (not lean labels), plus Rico's Under 51.5 projection, are tracked live below:")
    lines.append("")
    den = status["scores"].get(AWAY, 0)
    pit = status["scores"].get(HOME, 0)
    total = den + pit
    margin_home = pit - den  # PIT minus DEN
    # PIT +4.5 covers if margin_home >= -4
    pit_cover_live = "covering" if margin_home >= -4 else "not covering"
    u515 = "still under" if total <= 51 else "OVER — would miss"
    lines.append(f"- **Score now:** DEN {den}, PIT {pit} (total {total}). Lock means were DEN 20.22, PIT 20.01, median total 40.")
    lines.append(f"- **PIT +4.5 (lock model 63.08% cover, comparison only):** home margin {margin_home:+d}. Live: **{pit_cover_live}**.")
    lines.append(f"- **Lock vs FD Over 36.5 (model 61.60% Over, comparison only):** current total {total}. Live vs 36.5: {'over' if total >= 37 else 'under so far'}.")
    lines.append(f"- **Rico projection / Slip C alt U51.5 (lock arrays 84.08%):** current total {total}. Live: **{u515}**.")
    lines.append("- **Moneyline comparison (lock flagged LARGE_DIVERGENCE / treat as model error):** not a lean. Live winner is whoever leads now, or none if tied.")
    lines.append("")
    lines.append("Rico's other legs are tracked in `LIVE_LEGS.md` as **Rico's projections**, not as our leans.")
    lines.append("")
    lines.append("## Per-play coverage / pressure log")
    lines.append("")
    lines.extend(play_lines or ["- No scrimmage plays yet."])
    lines.append("")
    dest.write_text("\n".join(lines) + "\n")


def write_legs(summary: dict, status: dict, dest: Path) -> None:
    box, last_counts = box_index(summary)
    half_done = half_over(status, summary)
    completed = status["completed"]
    den = status["scores"].get(AWAY, 0)
    pit = status["scores"].get(HOME, 0)
    total = den + pit
    started = status["name"] not in ("STATUS_SCHEDULED", "STATUS_POSTPONED") or total > 0 or any(box.values())

    def val_for(leg):
        kind = leg["kind"]
        if kind == "total_under":
            return total
        row = find_player(box, leg["player"], last_counts)
        if kind == "rec":
            return 0 if row is None else row["rec"]
        if kind == "recyds":
            return 0 if row is None else row["rec_yds"]
        if kind == "rr":
            return 0 if row is None else (row["rush_yds"] + row["rec_yds"])
        if kind == "atd":
            return 0 if row is None else row["atd"]
        if kind == "atd_1h":
            # prefer scoring plays in 1H
            n = scoring_tds_1h(summary, leg["player"], last_counts)
            return n
        return None

    def status_for(leg, val):
        kind = leg["kind"]
        thr = leg["threshold"]
        if kind == "total_under":
            if val >= 52:
                return "MISS", f"total {val} already over 51.5"
            if completed:
                return "HIT", f"final total {val} ≤ 51"
            if not started:
                return "PENDING", "game not started"
            return "LIVE", f"current total {val}, must stay ≤ 51"
        # overs
        if val is None:
            return "PENDING", "no projection / no value"
        hit_now = val >= thr
        if kind == "atd_1h":
            if hit_now:
                return "HIT", f"{val} first-half TD already"
            if half_done:
                return "MISS", "first half over, no TD"
            if not started:
                return "PENDING", "game not started"
            return "LIVE", "no first-half TD yet"
        if hit_now:
            return "HIT", f"{val} already clears {thr}"
        if completed:
            return "MISS", f"final {val} short of {thr}"
        if not started:
            return "PENDING", "game not started"
        return "LIVE", f"{val} vs {thr}"

    lines = []
    lines.append("# LIVE LEGS — DEN @ PIT")
    lines.append("")
    lines.append(f"**Snapshot:** {stamp_human()} (America/New_York)")
    lines.append(f"**Game:** {status['detail']} | {AWAY} {den}, {HOME} {pit} | period={status.get('period')} clock={status.get('clock')}")
    lines.append("**Source:** ESPN boxscore + scoring plays + PBP, event 401873083. Research only. Paper / unvetted.")
    lines.append("Rico's three slips are **Rico's projections** (`RICO_SLIPS_LOCK.md`). Our freeze is `PREGAME_PROJECTION.md`. Both grade postgame head to head.")
    lines.append("")
    lines.append("## Current values")
    lines.append("| Slips | Leg | Threshold | Current | Status | Note |")
    lines.append("|---|---|---|---|---|---|")
    slip_hits = {"A": [], "B": [], "C": []}
    for leg in LEGS:
        val = val_for(leg)
        st, note = status_for(leg, val)
        cur = val if val is not None else "—"
        label = (leg["player"] + " " + leg["market"]).strip()
        lines.append(
            f"| {leg['slips']} | {label} | {leg['threshold']} | {cur} | **{st}** | {note} |"
        )
        for s in leg["slips"].split(","):
            slip_hits[s.strip()].append(st)

    def slip_status(keys):
        sts = [x for k, vs in slip_hits.items() if k in keys for x in vs]
        # wait, wrong. keys is one slip
        return ""

    lines.append("")
    lines.append("## Slip status")
    for slip, n_need in (("A", 6), ("B", 6), ("C", 7)):
        sts = slip_hits[slip]
        n_hit = sts.count("HIT")
        n_miss = sts.count("MISS")
        if n_miss:
            overall = "LOST (a leg has already missed)"
        elif n_hit == len(sts) and all(s == "HIT" for s in sts):
            overall = "HIT (all legs already cleared; total under only official at FINAL)"
            if slip == "C" and "LIVE" in sts:
                overall = "LIVE"
        else:
            overall = "LIVE" if started else "PENDING"
        lines.append(f"- **Slip {slip}:** {n_hit}/{len(sts)} legs HIT, {n_miss} MISS, remainder LIVE/PENDING — **{overall}**.")
    lines.append("")
    # box crumbs
    lines.append("## Box crumbs (tracked players)")
    lines.append("| Player | Team | Rush att-yds-TD | Rec-yds-TD (tgt) | Rush+rec yds | Anytime TDs |")
    lines.append("|---|---|---|---|---|---|")
    tracked = ["Jonah Coleman", "Pat Freiermuth", "Courtland Sutton", "Evan Engram", "Jaylen Warren", "DK Metcalf"]
    for name in tracked:
        row = find_player(box, name, last_counts)
        if not row:
            lines.append(f"| {name} | — | 0-0-0 | 0-0-0 (0) | 0 | 0 |")
        else:
            lines.append(
                f"| {name} | {row['team']} | {row['rush_att']}-{row['rush_yds']}-{row['rush_td']} | "
                f"{row['rec']}-{row['rec_yds']}-{row['rec_td']} ({row['tgt']}) | "
                f"{row['rush_yds']+row['rec_yds']} | {row['atd']} |"
            )
    lines.append("")
    dest.write_text("\n".join(lines) + "\n")


def copy_final(ts: str, status: dict) -> None:
    for src, dst in [
        (PBP / f"summary_{ts}.json", PBP / "summary_FINAL.json"),
        (PBP / f"coreplays_{ts}.json", PBP / "coreplays_FINAL.json"),
        (PBP / f"plays_{ts}.csv", PBP / "plays_FINAL.csv"),
        (PBP / "plays_latest.csv", PBP / "plays_FINAL.csv"),
        (RUN / "LIVE_LEGS.md", RUN / "LIVE_LEGS_FINAL.md"),
        (RUN / "LIVE_DEFENSE.md", RUN / "LIVE_DEFENSE_FINAL.md"),
        (RUN / "LIVE_EXPLOSIVES.csv", RUN / "LIVE_EXPLOSIVES_FINAL.csv"),
    ]:
        if src.exists() and src != dst:
            try:
                shutil.copy(src, dst)
            except Exception as e:
                log(f"final copy {src} -> {dst} failed: {e}")
    scores = " ".join(f"{k} {v}" for k, v in status["scores"].items())
    FINAL_FLAG.write_text(f"{ts}\n{status['detail']}\n{scores} Final\n")
    # keep playlog as the final week file too
    log("GAME FINAL flag written")


def one_pull() -> bool:
    """Return True if game is final."""
    ts = stamp_file()
    sum_path = PBP / f"summary_{ts}.json"
    core_path = PBP / f"coreplays_{ts}.json"
    if not fetch(SUMMARY_URL, sum_path):
        return False
    fetch(CORE_URL, core_path)  # best-effort
    try:
        summary = json.loads(sum_path.read_text())
    except Exception as e:
        log(f"json parse failed: {e}")
        return False
    status = header_status(summary)
    log(f"pull {ts} {status['name']} {status['detail']} completed={status['completed']} "
        f"{' '.join(f'{k} {v}' for k,v in status['scores'].items())}")
    rows = build_plays(summary)
    write_pbp_csv(rows, PBP / "plays_latest.csv")
    shutil.copy(PBP / "plays_latest.csv", PBP / f"plays_{ts}.csv")
    write_playlog(rows, status["home"], status["away"])
    explosives = write_explosives(rows, RUN / "LIVE_EXPLOSIVES.csv")
    write_defense(rows, explosives, status, RUN / "LIVE_DEFENSE.md")
    write_legs(summary, status, RUN / "LIVE_LEGS.md")
    if status["completed"]:
        copy_final(ts, status)
        return True
    return False


def main() -> int:
    PBP.mkdir(parents=True, exist_ok=True)
    PLAYLOG.parent.mkdir(parents=True, exist_ok=True)
    PIDFILE.write_text(str(__import__("os").getpid()) + "\n")
    log(f"poller start pid={__import__('os').getpid()} interval={INTERVAL}s event={EVENT}")
    if FINAL_FLAG.exists():
        log("already final, exiting")
        return 0
    try:
        while True:
            try:
                done = one_pull()
            except Exception as e:
                log(f"pull exception: {e}")
                done = False
            if done or FINAL_FLAG.exists():
                log("detected final, exiting poll")
                return 0
            time.sleep(INTERVAL)
    finally:
        log("poller exit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
