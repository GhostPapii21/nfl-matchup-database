#!/usr/bin/env python3
"""Sanctioned public ESPN live PBP updater for NFL TNF/SNF logs.

Sources (public HTTPS, documented ESPN site/core APIs — same feed as sports-leader):
  - https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={eid}
  - https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{eid}/competitions/{eid}/plays?limit=300

Rules:
  - Append + dedupe by play_id
  - Tackler from PBP parentheses / participant type=tackler is NOT coverage loser
  - confirmed_coverage_defender only when source explicitly attributes coverage; else UNKNOWN
  - Explosive: pass/reception >=20 yards; rush >=10 yards (statYardage / parsed yards)
  - No odds spend; no undocumented private APIs

Usage:
  python3 espn_live_pbp_updater.py --event-id 401873037 --outdir /workspace/nfl-database/live/2026-11-05_JAX_BAL
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
import os
import re
import urllib.request
from typing import Any

PASS_EXPLOSIVE = 20
RUSH_EXPLOSIVE = 10

CSV_FIELDS = [
    "play_id",
    "sequence",
    "source",
    "source_timestamp_utc",
    "ingested_at_et",
    "quarter",
    "clock",
    "possession",
    "down",
    "distance",
    "yardline_start",
    "play_type",
    "play_text",
    "passer",
    "rusher",
    "target_receiver",
    "outcome",
    "yards",
    "air_depth",  # short/deep/middle direction phrase if ESPN text explicit; else blank
    "yac_if_explicit",
    "tacklers",
    "confirmed_coverage_defender",
    "coverage_attribution_note",
    "explosive_pass",
    "explosive_rush",
    "home_score",
    "away_score",
    "is_scoring",
]

NAME_CACHE: dict[str, str] = {}


def now_et() -> str:
    # Box clock is America/New_York
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S ET")


def fetch_json(url: str) -> Any:
    req = urllib.request.Request(url, headers={"User-Agent": "nfl-live-pbp-updater/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def athlete_name(athlete_ref: str | None, summary_athletes: dict[str, str]) -> str:
    if not athlete_ref:
        return ""
    m = re.search(r"/athletes/(\d+)", athlete_ref)
    if not m:
        return ""
    aid = m.group(1)
    if aid in summary_athletes:
        return summary_athletes[aid]
    if aid in NAME_CACHE:
        return NAME_CACHE[aid]
    # Best-effort public athlete endpoint (optional; failures stay blank)
    try:
        data = fetch_json(
            f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes/{aid}?lang=en&region=us"
        )
        name = data.get("displayName") or data.get("shortName") or ""
        NAME_CACHE[aid] = name
        return name
    except Exception:
        return aid


def parse_air_depth(text: str) -> str:
    t = text.lower()
    m = re.search(r"pass (incomplete )?(short|deep) (left|right|middle)", t)
    if m:
        return f"{m.group(2)} {m.group(3)}"
    m = re.search(r"pass (short|deep) (left|right|middle)", t)
    if m:
        return f"{m.group(1)} {m.group(2)}"
    return ""


def parse_tacklers_from_text(text: str) -> str:
    # Names in final parentheses are tacklers / return tacklers — NOT coverage.
    # Skip penalty notes like (Illegal Contact).
    ms = re.findall(r"\(([^)]+)\)", text)
    if not ms:
        return ""
    last = ms[-1]
    # Heuristic: player initials.Last pattern
    parts = [p.strip() for p in re.split(r"[;]", last)]
    keep = []
    for p in parts:
        if re.match(r"^[A-Z]\.[\w'\-]+", p) or re.match(r"^[A-Z][\w'\-]+ [A-Z]", p):
            # filter obvious non-player phrases
            if any(w in p.lower() for w in ("illegal", "holding", "pass interference", "delay", "false start")):
                continue
            keep.append(p)
    return "; ".join(keep)


def outcome_from(play: dict, text: str) -> str:
    typ = (play.get("type") or {}).get("text") or ""
    tl = text.lower()
    if "touchdown" in tl and "no play" not in tl:
        if "pass" in tl:
            return "pass_td"
        if "rush" in typ.lower() or "left" in tl or "right" in tl or "middle" in tl or "guard" in tl or "tackle" in tl:
            return "rush_td"
        return "td"
    if "incomplete" in tl:
        return "incomplete"
    if "intercept" in tl:
        return "interception"
    if typ.lower() == "pass reception" or "pass" in tl and " to " in tl:
        return "complete"
    if typ.lower() == "rush" or "rush" in typ.lower():
        return "rush"
    if "kickoff" in typ.lower():
        return "kickoff"
    if "punt" in typ.lower():
        return "punt"
    if "field goal" in typ.lower():
        return "field_goal"
    if "coin toss" in typ.lower() or text.strip().upper() == "GAME":
        return "meta"
    return typ.lower().replace(" ", "_") or "other"


def yardline_label(start: dict) -> str:
    if not start:
        return ""
    # Prefer possessionText / downDistanceText fragments already on end/start
    return start.get("possessionText") or start.get("downDistanceText") or ""


def build_summary_athlete_map(summary: dict) -> dict[str, str]:
    out: dict[str, str] = {}
    for team_block in summary.get("boxscore", {}).get("players", []) or []:
        for stat in team_block.get("statistics", []) or []:
            for a in stat.get("athletes", []) or []:
                ath = a.get("athlete") or {}
                aid = str(ath.get("id") or "")
                name = ath.get("displayName") or ath.get("shortName") or ""
                if aid and name:
                    out[aid] = name
    # also leaders
    for lead in summary.get("leaders", []) or []:
        for cat in lead.get("leaders", []) or []:
            for row in cat.get("leaders", []) or []:
                ath = row.get("athlete") or {}
                aid = str(ath.get("id") or "")
                name = ath.get("displayName") or ""
                if aid and name:
                    out[aid] = name
    return out


def plays_from_summary(summary: dict) -> list[dict]:
    rows = []
    drives = summary.get("drives") or {}
    ordered = list(drives.get("previous") or [])
    if drives.get("current"):
        ordered.append(drives["current"])
    for dr in ordered:
        off = (dr.get("team") or {}).get("abbreviation") or ""
        for p in dr.get("plays") or []:
            p = dict(p)
            p["_possession_abbrev"] = off
            rows.append(p)
    return rows


def normalize_play(p: dict, source: str, summary_athletes: dict[str, str], possession_hint: str = "") -> dict:
    text = p.get("text") or p.get("alternativeText") or ""
    typ = (p.get("type") or {}).get("text") or ""
    start = p.get("start") or {}
    end = p.get("end") or {}
    clock = (p.get("clock") or {}).get("displayValue") or ""
    period = (p.get("period") or {}).get("number") or ""
    yards = p.get("statYardage")
    if yards is None:
        ym = re.search(r"for (-?\d+) yards?", text)
        yards = int(ym.group(1)) if ym else (0 if "no gain" in text.lower() else "")
    yac = p.get("yardsAfterCatch")
    if yac is None:
        yac = ""

    passer = rusher = receiver = ""
    tacklers_part = []
    for part in p.get("participants") or []:
        ptype = (part.get("type") or "").lower()
        # site summary embeds athlete object; core uses $ref
        ath = part.get("athlete") or {}
        if isinstance(ath, dict) and ath.get("displayName"):
            name = ath.get("displayName")
        else:
            ref = ath.get("$ref") if isinstance(ath, dict) else None
            name = athlete_name(ref, summary_athletes)
        if ptype == "passer":
            passer = name
        elif ptype == "rusher":
            rusher = name
        elif ptype == "receiver":
            receiver = name
        elif ptype in ("tackler", "assist"):
            if name:
                tacklers_part.append(name)

    # Fallback parse from text for receiver/passer if missing
    if not passer:
        m = re.search(r"([A-Z]\.[\w'\-]+) pass", text)
        if m:
            passer = m.group(1)
    if not receiver:
        m = re.search(r"pass (?:incomplete )?(?:short|deep)?\s*(?:left|right|middle)? ?(?:to|intended for) ([A-Z]\.[\w'\-]+(?: (?:Jr|III|II|IV)\.?)?)", text)
        if m:
            receiver = m.group(1)
    if not rusher and "rush" in typ.lower():
        m = re.search(r"^([A-Z]\.[\w'\-]+(?: (?:Jr|III|II)\.?)?)", text.strip())
        if m:
            rusher = m.group(1)

    tacklers = "; ".join(tacklers_part) if tacklers_part else parse_tacklers_from_text(text)

    outcome = outcome_from(p, text)
    air = parse_air_depth(text)

    # Possession: prefer drive team abbrev; else parse start team from possessionText
    poss = possession_hint or ""
    if not poss:
        pt = start.get("possessionText") or end.get("possessionText") or ""
        # often "JAX 23" — keep team token if present in text start
        if text.startswith("T.Lawrence") or "T.Lawrence" in text[:40]:
            poss = "JAX"
        elif "J.Moody" in text and "kick" in text.lower():
            poss = "BAL"  # kicking team; drive may be return

    try:
        y_int = int(yards) if yards != "" and yards is not None else None
    except Exception:
        y_int = None

    is_pass = outcome in ("complete", "incomplete", "pass_td", "interception") or "pass" in typ.lower()
    is_rush = outcome in ("rush", "rush_td") or typ.lower() == "rush"
    exp_pass = bool(is_pass and y_int is not None and y_int >= PASS_EXPLOSIVE and outcome in ("complete", "pass_td"))
    exp_rush = bool(is_rush and y_int is not None and y_int >= RUSH_EXPLOSIVE)

    wall = p.get("wallclock") or p.get("modified") or ""
    # Coverage: ESPN PBP does not confirm coverage defender; tackler ≠ beaten in coverage
    cov = "UNKNOWN"
    cov_note = "No confirmed coverage attribution in ESPN PBP; tackler listed separately and must not be treated as coverage loser."

    return {
        "play_id": str(p.get("id") or ""),
        "sequence": str(p.get("sequenceNumber") or p.get("order") or ""),
        "source": source,
        "source_timestamp_utc": wall,
        "ingested_at_et": now_et(),
        "quarter": str(period),
        "clock": clock,
        "possession": poss or p.get("_possession_abbrev") or "",
        "down": str(start.get("down") if start.get("down") is not None else ""),
        "distance": str(start.get("distance") if start.get("distance") is not None else ""),
        "yardline_start": start.get("downDistanceText") or yardline_label(start),
        "play_type": typ,
        "play_text": text,
        "passer": passer,
        "rusher": rusher,
        "target_receiver": receiver,
        "outcome": outcome,
        "yards": "" if y_int is None else y_int,
        "air_depth": air,
        "yac_if_explicit": yac if yac != "" else "",
        "tacklers": tacklers,
        "confirmed_coverage_defender": cov,
        "coverage_attribution_note": cov_note,
        "explosive_pass": "1" if exp_pass else "0",
        "explosive_rush": "1" if exp_rush else "0",
        "home_score": p.get("homeScore", ""),
        "away_score": p.get("awayScore", ""),
        "is_scoring": "1" if p.get("scoringPlay") else "0",
    }


def load_existing(csv_path: str) -> dict[str, dict]:
    if not os.path.exists(csv_path):
        return {}
    out = {}
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            if row.get("play_id"):
                out[row["play_id"]] = row
    return out


def write_csv(path: str, rows: list[dict]) -> None:
    rows_sorted = sorted(rows, key=lambda r: (int(r["sequence"] or 0), r["play_id"]))
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        w.writeheader()
        for r in rows_sorted:
            w.writerow({k: r.get(k, "") for k in CSV_FIELDS})


def write_markdown(path: str, rows: list[dict], meta: dict) -> None:
    rows_sorted = sorted(rows, key=lambda r: (int(r["sequence"] or 0), r["play_id"]))
    targets = [r for r in rows_sorted if r.get("target_receiver") and r.get("outcome") in ("complete", "incomplete", "pass_td", "interception")]
    explosives = [r for r in rows_sorted if r.get("explosive_pass") == "1" or r.get("explosive_rush") == "1"]
    lines = []
    lines.append(f"# Live PBP — {meta.get('title','JAX @ BAL')}")
    lines.append("")
    lines.append(f"- Generated: **{now_et()}** (America/New_York)")
    lines.append(f"- ESPN event id: `{meta.get('event_id')}`")
    lines.append(f"- Game status at pull: **{meta.get('status')}** — score **{meta.get('score')}**")
    lines.append(f"- Primary source: ESPN public site/core APIs (sports-leader-compatible)")
    lines.append(f"- Definitions: explosive pass ≥{PASS_EXPLOSIVE} yds; explosive rush ≥{RUSH_EXPLOSIVE} yds")
    lines.append("- **Tackler ≠ coverage defender.** `confirmed_coverage_defender` is UNKNOWN unless a source explicitly attributes coverage.")
    lines.append("")
    lines.append("## Target / explosive summary")
    lines.append("")
    lines.append(f"- Targeted pass plays logged: **{len(targets)}**")
    lines.append(f"- Explosive plays logged: **{len(explosives)}** (pass={sum(r.get('explosive_pass')=='1' for r in explosives)}, rush={sum(r.get('explosive_rush')=='1' for r in explosives)})")
    lines.append("")
    if targets:
        lines.append("| Q | clock | target | outcome | yds | air_depth | tackler(s) | coverage |")
        lines.append("|---|-------|--------|---------|-----|-----------|------------|----------|")
        for r in targets:
            lines.append(
                f"| {r['quarter']} | {r['clock']} | {r['target_receiver']} | {r['outcome']} | {r['yards']} | {r['air_depth'] or '—'} | {r['tacklers'] or '—'} | {r['confirmed_coverage_defender']} |"
            )
        lines.append("")
    if explosives:
        lines.append("### Explosives")
        lines.append("")
        for r in explosives:
            kind = "PASS" if r.get("explosive_pass") == "1" else "RUSH"
            lines.append(f"- **{kind}** Q{r['quarter']} {r['clock']}: {r['play_text']} (tackler: {r['tacklers'] or '—'}; coverage: UNKNOWN)")
        lines.append("")
    lines.append("## Full play log")
    lines.append("")
    lines.append("| Q | clock | poss | D&D | type | outcome | yds | target/rusher | tacklers | coverage | explosive |")
    lines.append("|---|-------|------|-----|------|---------|-----|---------------|----------|----------|-----------|")
    for r in rows_sorted:
        if r.get("outcome") == "meta":
            continue
        who = r.get("target_receiver") or r.get("rusher") or "—"
        exp = []
        if r.get("explosive_pass") == "1":
            exp.append("PASS")
        if r.get("explosive_rush") == "1":
            exp.append("RUSH")
        lines.append(
            f"| {r['quarter']} | {r['clock']} | {r['possession']} | {r['yardline_start'] or (str(r['down'])+'&'+str(r['distance']))} | {r['play_type']} | {r['outcome']} | {r['yards']} | {who} | {r['tacklers'] or '—'} | {r['confirmed_coverage_defender']} | {','.join(exp) or '—'} |"
        )
    lines.append("")
    lines.append("## Provenance / gaps")
    lines.append("")
    lines.append("- Screenshot seed path from task was not present on disk at ingest; screenshot contents were seeded from the user-provided play text and cross-checked against ESPN.")
    lines.append("- BALLDONTLIE `nfl_get_plays` not used for this live snap (week query returned upcoming Week 10 slate; TNF game not resolved in that response).")
    lines.append("- StatsHawk contest found but `get_play_by_play` returned NOT_FOUND for live contest (no units wasted beyond search).")
    lines.append("- Air depth only when ESPN text explicitly says short/deep + direction.")
    lines.append("")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--event-id", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--title", default="JAX @ BAL")
    args = ap.parse_args()
    os.makedirs(os.path.join(args.outdir, "raw"), exist_ok=True)

    eid = args.event_id
    summary_url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={eid}"
    plays_url = f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{eid}/competitions/{eid}/plays?limit=300"

    summary = fetch_json(summary_url)
    core = fetch_json(plays_url)

    ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(os.path.join(args.outdir, "raw", f"espn_summary_{eid}_{ts}.json"), "w") as f:
        json.dump(summary, f)
    with open(os.path.join(args.outdir, "raw", f"espn_plays_{eid}_{ts}.json"), "w") as f:
        json.dump(core, f)
    # also refresh canonical latest
    with open(os.path.join(args.outdir, "raw", f"espn_summary_{eid}.json"), "w") as f:
        json.dump(summary, f)
    with open(os.path.join(args.outdir, "raw", f"espn_plays_{eid}.json"), "w") as f:
        json.dump(core, f)

    athletes = build_summary_athlete_map(summary)
    by_id: dict[str, dict] = {}

    # Prefer site summary drive plays (richer athlete objects + possession)
    for p in plays_from_summary(summary):
        row = normalize_play(p, "espn_site_summary", athletes, possession_hint=p.get("_possession_abbrev") or "")
        if row["play_id"]:
            by_id[row["play_id"]] = row

    # Merge core items for any missing fields / plays
    for p in core.get("items") or []:
        pid = str(p.get("id") or "")
        row = normalize_play(p, "espn_core_plays", athletes)
        if not pid:
            continue
        if pid not in by_id:
            by_id[pid] = row
        else:
            # fill blanks
            for k, v in row.items():
                if (not by_id[pid].get(k)) and v not in (None, ""):
                    by_id[pid][k] = v
            # keep richer source tag if merged
            by_id[pid]["source"] = "espn_site_summary+core"

    csv_path = os.path.join(args.outdir, "pbp_live.csv")
    md_path = os.path.join(args.outdir, "pbp_live.md")
    existing = load_existing(csv_path)
    # preserve any screenshot-only rows not in ESPN yet
    for pid, row in existing.items():
        if pid not in by_id:
            by_id[pid] = row
        else:
            # if existing was screenshot seed, keep provenance note in source
            if "screenshot" in (row.get("source") or ""):
                by_id[pid]["source"] = by_id[pid]["source"] + "+screenshot_seed"

    rows = list(by_id.values())
    write_csv(csv_path, rows)

    hc = summary["header"]["competitions"][0]
    status = hc["status"]["type"]["detail"]
    score = " ".join(f"{c['team']['abbreviation']} {c.get('score','?')}" for c in sorted(hc["competitors"], key=lambda x: 0 if x.get("homeAway")=="away" else 1))
    write_markdown(md_path, rows, {"title": args.title, "event_id": eid, "status": status, "score": score})

    # meta sidecar
    meta = {
        "event_id": eid,
        "pulled_at_et": now_et(),
        "status": status,
        "score": score,
        "n_plays": len(rows),
        "csv": csv_path,
        "md": md_path,
        "explosive_pass_threshold": PASS_EXPLOSIVE,
        "explosive_rush_threshold": RUSH_EXPLOSIVE,
        "sources": [summary_url, plays_url],
    }
    with open(os.path.join(args.outdir, "live_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)

    print(json.dumps(meta, indent=2))

    # Rebuild quarter / drive / conversion logs from the same summary snapshot
    try:
        import subprocess
        builder = os.path.join(os.path.dirname(__file__), "build_quarter_drive_logs.py")
        if os.path.isfile(builder):
            subprocess.run([sys.executable, builder], check=False)
    except Exception as e:
        print(json.dumps({"builder_error": str(e)}))


if __name__ == "__main__":
    main()
