"""Live play-by-play tracker for every NFL game on a date (ESPN public JSON; no key).

Every run (the workflow polls every 5 minutes while games are on) rewrites, per game under research/live_<season>_w<WW>/<game_id>/:
  plays.jsonl          every play: quarter, clock, offense, type, yards, scoring, passer/receiver/rusher, defenders named
  box.json             ESPN box score (passing, rushing, receiving incl. targets)
  coverage.csv         per defender: catches allowed (he made the tackle on a completed pass), yards after those catches,
                       targets allowed, pass breakups/INTs (named on an incompletion/interception), to whom
  vs_projection.csv    per player: live receptions / receiving / rushing / rush+rec yards vs the pregame projection
                       (research/projections_<season>_w<WW>/projections.csv) and the book line
and a slate-wide LIVE.md. Defender attribution is what the play text names: on a catch that is the tackler (often, not
always, the man in coverage); on an incompletion it is the defender credited with the breakup. It is labeled as such.

    python scripts/live_pbp.py [--date 20261122]
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SB = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates={d}"
SUM = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={e}"
UA = {"User-Agent": "nfl-matchup-database live tracker (research)"}
FIX = {"WSH": "WAS", "LAR": "LA", "JAC": "JAX"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def _nm(s):
    return re.sub(r"[^a-z]", "", str(s or "").lower())


def plays_of(summary):
    dr = summary.get("drives") or {}
    out = []
    for d in (dr.get("previous") or []) + ([dr["current"]] if dr.get("current") else []):
        team = ((d.get("team") or {}).get("abbreviation"))
        for p in d.get("plays") or []:
            parts = {x.get("type"): (x.get("athlete") or {}).get("displayName") for x in p.get("participants") or []}
            text = p.get("text") or ""
            m = re.search(r"\(([^()]*)\)\s*\.?\s*(?:PENALTY.*)?$", text.strip())
            named = [x.strip() for x in m.group(1).split(";")] if m and not re.search(r"Shotgun|No Huddle|kick|punt", m.group(1), re.I) else []
            if not parts.get("receiver"):
                mr = re.search(r"\bpass(?: incomplete)?(?: (?:short|deep))?(?: (?:left|right|middle))? (?:to|intended for) ([A-Z][\w.'\-]+(?: [A-Z][\w.'\-]+)?)", text)
                if mr:
                    parts["receiver"] = mr.group(1).rstrip(".")
            out.append({"id": p.get("id"), "seq": int(p.get("sequenceNumber") or 0), "quarter": (p.get("period") or {}).get("number"),
                        "clock": (p.get("clock") or {}).get("displayValue"), "offense": FIX.get(team, team),
                        "type": (p.get("type") or {}).get("text"), "yards": p.get("statYardage"), "scoring": bool(p.get("scoringPlay")),
                        "passer": parts.get("passer"), "receiver": parts.get("receiver"), "rusher": parts.get("rusher"),
                        "defenders_named": named, "text": text})
    seen, uniq = set(), []
    for p in sorted(out, key=lambda x: x["seq"]):
        if p["id"] not in seen:
            seen.add(p["id"])
            uniq.append(p)
    return uniq


def coverage(plays):
    rows = defaultdict(lambda: {"targets_against": 0, "catches_allowed": 0, "yards_allowed": 0, "breakups_or_ints": 0, "receivers": defaultdict(int)})
    for p in plays:
        t = p["type"] or ""
        if not p["receiver"] or not p["defenders_named"]:
            continue
        d = p["defenders_named"][0]
        r = rows[(p["offense"], d)]
        r["targets_against"] += 1
        if t.startswith("Pass Reception") or t == "Passing Touchdown":
            r["catches_allowed"] += 1
            r["yards_allowed"] += int(p["yards"] or 0)
            r["receivers"][p["receiver"]] += int(p["yards"] or 0)
        elif "Incompletion" in t or "Interception" in t:
            r["breakups_or_ints"] += 1
    return rows


def box_players(summary):
    out = defaultdict(dict)
    for team in (summary.get("boxscore") or {}).get("players") or []:
        ab = FIX.get(team["team"]["abbreviation"], team["team"]["abbreviation"])
        for cat in team.get("statistics") or []:
            keys = cat.get("keys") or []
            for a in cat.get("athletes") or []:
                nm = a["athlete"]["displayName"]
                vals = dict(zip(keys, a.get("stats") or []))
                rec = out[(ab, nm)]
                if cat["name"] == "receiving":
                    rec.update(receptions=vals.get("receptions"), rec_yds=vals.get("receivingYards"), targets=vals.get("receivingTargets"))
                elif cat["name"] == "rushing":
                    rec.update(carries=vals.get("rushingAttempts"), rush_yds=vals.get("rushingYards"))
    return out


def num(x):
    try:
        return float(str(x).replace(",", ""))
    except (TypeError, ValueError):
        return 0.0


def run(date: str):
    sb = get(SB.format(d=date))
    evs = sb.get("events") or []
    if not evs:
        print("no games on", date)
        return
    wk = (sb.get("week") or {}).get("number") or evs[0].get("week", {}).get("number")
    season = (sb.get("season") or {}).get("year") or int(date[:4])
    base = ROOT / "research" / f"live_{season}_w{int(wk):02d}"
    proj_f = ROOT / "research" / f"projections_{season}_w{int(wk)}" / "projections.csv"
    proj = list(csv.DictReader(proj_f.open())) if proj_f.exists() else []
    lines = [f"# Live tracker, Week {wk} ({datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC)", "",
             "Defender = the defender the play text names: on a catch, the tackler (often, not always, the man in coverage); on an incompletion, the defender credited with the breakup.", ""]
    for e in evs:
        comp = e["competitions"][0]
        st = comp["status"]["type"]
        if st.get("state") == "pre":
            continue
        teams = {c["homeAway"]: FIX.get(c["team"]["abbreviation"], c["team"]["abbreviation"]) for c in comp["competitors"]}
        score = {c["homeAway"]: c.get("score") for c in comp["competitors"]}
        gid = f"{season}_{int(wk):02d}_{teams['away']}_{teams['home']}"
        try:
            s = get(SUM.format(e=e["id"]))
        except Exception as ex:  # noqa: BLE001
            lines.append(f"## {gid}: fetch failed {ex!r}")
            continue
        d = base / gid
        d.mkdir(parents=True, exist_ok=True)
        pl = plays_of(s)
        (d / "plays.jsonl").write_text("".join(json.dumps(p) + "\n" for p in pl))
        bx = box_players(s)
        (d / "box.json").write_text(json.dumps({f"{t}|{n}": v for (t, n), v in bx.items()}, indent=1) + "\n")
        cov = coverage(pl)
        with (d / "coverage.csv").open("w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["defense_vs_offense", "defender", "targets_against", "catches_allowed", "yards_allowed", "breakups_or_ints", "receivers_yards"])
            for (off, dname), r in sorted(cov.items(), key=lambda kv: -kv[1]["yards_allowed"]):
                w.writerow([f"vs {off}", dname, r["targets_against"], r["catches_allowed"], r["yards_allowed"], r["breakups_or_ints"],
                            "; ".join(f"{k} {v}" for k, v in sorted(r["receivers"].items(), key=lambda kv: -kv[1]))])
        vs = []
        for pr in [x for x in proj if x["game"] == f"{teams['away']}@{teams['home']}"]:
            live = next((v for (t, n), v in bx.items() if t == pr["team"] and _nm(n) == _nm(pr["player"])), {})
            ry, uy = num(live.get("rec_yds")), num(live.get("rush_yds"))
            vs.append({"team": pr["team"], "player": pr["player"], "receptions": num(live.get("receptions")), "proj_receptions": pr["receptions"],
                       "line_receptions": pr["line_receptions"], "rec_yds": ry, "proj_rec_yds_median": pr["rec_yds_median"], "line_rec_yds": pr["line_rec_yds"],
                       "rush_yds": uy, "proj_rush_yds_median": pr["rush_yds_median"], "line_rush_yds": pr["line_rush_yds"],
                       "rush_rec_yds": ry + uy, "proj_rush_rec_yds_mean": pr["rush_rec_yds_mean"], "line_rush_rec_yds": pr["line_rush_rec_yds"]})
        if vs:
            with (d / "vs_projection.csv").open("w", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=list(vs[0]))
                w.writeheader()
                w.writerows(vs)
        lines += [f"## {teams['away']} {score['away']} @ {teams['home']} {score['home']} ({st.get('shortDetail')})", "",
                  f"{len(pl)} plays. Top yards allowed by a named defender: " +
                  ", ".join(f"{dn} ({r['catches_allowed']}/{r['targets_against']}, {r['yards_allowed']} yds)" for (o, dn), r in
                            sorted(cov.items(), key=lambda kv: -kv[1]["yards_allowed"])[:4]), ""]
        top = sorted(vs, key=lambda v: -(v["rush_rec_yds"]))[:6]
        if top:
            lines += ["| Player | Rec | Proj | Rec yds | Proj (med) | Line | Rush yds | Proj (med) | Line |", "|---|---|---|---|---|---|---|---|---|"]
            lines += [f"| {v['player']} ({v['team']}) | {v['receptions']:.0f} | {v['proj_receptions']} | {v['rec_yds']:.0f} | {v['proj_rec_yds_median']} | {v['line_rec_yds']} | "
                      f"{v['rush_yds']:.0f} | {v['proj_rush_yds_median']} | {v['line_rush_yds']} |" for v in top]
            lines.append("")
    base.mkdir(parents=True, exist_ok=True)
    (base / "LIVE.md").write_text("\n".join(lines) + "\n")
    states = [e["competitions"][0]["status"]["type"].get("state") for e in evs]
    print(f"live: {len(evs)} games, states {dict((s, states.count(s)) for s in set(states))}")
    (base / "_state.json").write_text(json.dumps({"updated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                                                  "states": states}, indent=1) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now(timezone.utc).astimezone().strftime("%Y%m%d"))
    run(ap.parse_args().date)
