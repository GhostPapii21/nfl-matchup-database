"""Live play-by-play tracker for every NFL game on a date (ESPN public JSON; no key).

Every run (the workflow polls every 5 minutes while games are on) rewrites, per game under research/live_<season>_w<WW>/<game_id>/:
  plays.jsonl          every play: quarter, clock, offense, type, yards, scoring, passer/receiver/rusher, defenders named
  box.json             ESPN box score (passing, rushing, receiving incl. targets)
  coverage.csv         per defender and evidence label (column `evidence`):
                         VERIFIED-PBU/INT/DPI   named on an incompletion (breakup credit), as the interceptor, or on a
                                                defensive pass interference flag; these are the only coverage counts
                         tackler, not coverage  ESPN names only a tackler on the catch; the first tackler is written,
                                                inferred, and kept out of the verified coverage counts
                       targets, catches and yards on those plays, breakups/INTs, DPI flags (`dpi`), to whom
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


VERIFIED = "VERIFIED-PBU/INT/DPI"
TACKLER = "tackler, not coverage"
_NAME = r"[A-Z][\w.'\-]+(?: [A-Z][\w.'\-]+)?"
_NOT_DEF = re.compile(r"Shotgun|No Huddle|kick|punt|^\s*Timeout #\d+\.?\s*$|^\s*\d{1,2}:\d{2}\s*$", re.I)


def _names(group):
    if group is None or _NOT_DEF.search(group):
        return []
    return [x.strip().rstrip(".") for x in group.split(";") if x.strip()]


def attribute(text):
    """Defenders the play text names, by evidence. Looks anywhere in the text, not only at the end.

    Returns {"pbu": name|None, "int": name|None, "dpi": [names], "tacklers": [names], "catch_yards": int|None}.
    When a replay reverses the ruling, only the text after the last "REVERSED." is read. Tacklers are only read off a
    completed pass (the first parentheses right after "for N yards"/"for no gain"); interception returns are never read
    for tacklers. A snap wiped out by an accepted penalty ("No Play") never happened: no tackler, breakup or INT is
    read from it, so it writes no tackler or coverage rows. The one exception is the defender flagged for defensive
    pass interference on it, which is the coverage event itself. A declined penalty leaves the play and its rows as is.
    """
    t = text or ""
    if "REVERSED." in t:
        t = t.rsplit("REVERSED.", 1)[1]
    out = {"pbu": None, "int": None, "dpi": [], "tacklers": [], "catch_yards": None, "no_play": False}
    out["no_play"] = bool(re.search(r"\bNo Play\b", t))
    for md in re.finditer(r"PENALTY on [A-Z]{2,3}-(" + _NAME + r"),\s*Defensive Pass Interference", t, re.I):
        nm = md.group(1).rstrip(".")
        if nm not in out["dpi"]:
            out["dpi"].append(nm)
    if out["no_play"]:
        return out  # accepted penalty wiped the snap out: no tackler, breakup or INT credit (a DPI flag still counts)
    mi = re.search(r"INTERCEPTED by (" + _NAME + ")", t)
    if mi:
        out["int"] = mi.group(1).rstrip(".")
    else:
        mp = re.search(r"\bpass incomplete[^()]*? (?:to|intended for) " + _NAME + r"\s*\(([^()]*)\)", t)
        if mp and _names(mp.group(1)):
            out["pbu"] = _names(mp.group(1))[0]
        elif not re.search(r"\bpass incomplete\b", t):
            mt = re.search(r"\bpass\b.*?\bfor (-?\d+ yards?|no gain)\s*(?:,\s*TOUCHDOWN\.?\s*)?\(([^()]*)\)", t)
            if mt and _names(mt.group(2)):
                out["tacklers"] = _names(mt.group(2))
                out["catch_yards"] = 0 if mt.group(1) == "no gain" else int(mt.group(1).split()[0])
    return out


def plays_of(summary):
    dr = summary.get("drives") or {}
    out = []
    for d in (dr.get("previous") or []) + ([dr["current"]] if dr.get("current") else []):
        team = ((d.get("team") or {}).get("abbreviation"))
        for p in d.get("plays") or []:
            parts = {x.get("type"): (x.get("athlete") or {}).get("displayName") for x in p.get("participants") or []}
            text = p.get("text") or ""
            att = attribute(text)
            named = [x for x in [att["int"], att["pbu"], *att["dpi"], *att["tacklers"]] if x]
            if not parts.get("receiver"):
                mr = re.search(r"\bpass(?: incomplete)?(?: (?:short|deep))?(?: (?:left|right|middle))? (?:to|intended for) ([A-Z][\w.'\-]+(?: [A-Z][\w.'\-]+)?)", text)
                if mr:
                    rcv = re.split(r"\.(?=[A-Z]{2,})", mr.group(1))[0]
                    rcv = " ".join(w for w in rcv.split() if not re.fullmatch(r"[A-Z]{2,}\.?", w))
                    parts["receiver"] = rcv.rstrip(".")
            out.append({"id": p.get("id"), "seq": int(p.get("sequenceNumber") or 0), "quarter": (p.get("period") or {}).get("number"),
                        "clock": (p.get("clock") or {}).get("displayValue"), "offense": FIX.get(team, team),
                        "type": (p.get("type") or {}).get("text"), "yards": p.get("statYardage"), "scoring": bool(p.get("scoringPlay")),
                        "passer": parts.get("passer"), "receiver": parts.get("receiver"), "rusher": parts.get("rusher"),
                        "defenders_named": named, "attribution": att, "text": text})
    seen, uniq = set(), []
    for p in sorted(out, key=lambda x: x["seq"]):
        if p["id"] not in seen:
            seen.add(p["id"])
            uniq.append(p)
    return uniq


def coverage(plays):
    """Rows keyed (offense, defender, evidence). Only VERIFIED rows are coverage counts; TACKLER rows are inferred."""
    rows = defaultdict(lambda: {"targets_against": 0, "catches_allowed": 0, "yards_allowed": 0, "breakups_or_ints": 0, "dpi": 0,
                                "receivers": defaultdict(int)})
    for p in plays:
        t = p["type"] or ""
        att = p.get("attribution") or attribute(p.get("text"))
        if not p["receiver"]:
            continue
        caught = t.startswith("Pass Reception") or t == "Passing Touchdown"
        yds = int(p["yards"] or 0)
        verified = {}
        for nm, kind in [(att["int"], "int"), (att["pbu"], "pbu"), *[(d, "dpi") for d in att["dpi"]]]:
            if nm:
                verified.setdefault(nm, set()).add(kind)
        hits = [(nm, VERIFIED, kinds) for nm, kinds in verified.items()]
        if not hits and att["tacklers"]:
            hits = [(att["tacklers"][0], TACKLER, set())]
        for nm, ev, kinds in hits:
            r = rows[(p["offense"], nm, ev)]
            r["targets_against"] += 1
            r["breakups_or_ints"] += 1 if kinds & {"pbu", "int"} else 0
            r["dpi"] += 1 if "dpi" in kinds else 0
            if caught:
                r["catches_allowed"] += 1
                r["yards_allowed"] += yds
                r["receivers"][p["receiver"]] += yds
    return rows


COVERAGE_HEADER = ["defense_vs_offense", "defender", "targets_against", "catches_allowed", "yards_allowed", "breakups_or_ints",
                   "receivers_yards", "evidence", "dpi"]


def coverage_rows(cov):
    for (off, dname, ev), r in sorted(cov.items(), key=lambda kv: -kv[1]["yards_allowed"]):
        yield [f"vs {off}", dname, r["targets_against"], r["catches_allowed"], r["yards_allowed"], r["breakups_or_ints"],
               "; ".join(f"{k} {v}" for k, v in sorted(r["receivers"].items(), key=lambda kv: -kv[1])), ev, r["dpi"]]


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
             "Coverage counts are VERIFIED-PBU/INT/DPI only (named on a breakup, as the interceptor, or on a DPI flag). A defender ESPN names only as the tackler on a catch is labeled \"tackler, not coverage\" (inferred) and is not a coverage count.", ""]
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
            w.writerow(COVERAGE_HEADER)
            w.writerows(coverage_rows(cov))
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
                  f"{len(pl)} plays. Verified coverage (PBU/INT/DPI): " +
                  (", ".join([f"{dn} ({r['targets_against']} tgt, {r['breakups_or_ints']} PBU/INT, {r['dpi']} DPI)" for (o, dn, ev), r in
                             sorted(cov.items(), key=lambda kv: -kv[1]["targets_against"]) if ev == VERIFIED][:4]) or "none") +
                  ". Most catch yards where ESPN names only a tackler (tackler, not coverage): " +
                  ", ".join([f"{dn} ({r['catches_allowed']}/{r['targets_against']}, {r['yards_allowed']} yds)" for (o, dn, ev), r in
                            sorted(cov.items(), key=lambda kv: -kv[1]["yards_allowed"]) if ev == TACKLER][:4]), ""]
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
