"""How do Bovada's player lines do against the result, next to the other books? (asked Nov 23, 2026)

Lines: every book's main line (two-sided, no-vig Over nearest 50%) for receiving yards, receptions and rushing yards,
taken from the last committed pregame/direct_lines snapshot pulled before ESPN's kickoff. Every game we have player
lines for (StartWho feed, from Nov 16: Week 10 Monday through Week 11). Results: ESPN box scores (final games only).
Per book: how often the Over won at its own line, pushes, and average miss |actual - line|. Then the props where
Bovada's line differs from the other books' median: whose line was closer, and which side of the consensus line won.

    python3 research/bovada_2026-11-23/study.py         # writes results.json and rows.csv
"""
from __future__ import annotations

import csv
import json
import statistics
import subprocess
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from dashboard.bestbet import _norm, implied  # noqa: E402

STAT = {"receiving_yards": ("receiving", "receivingYards"), "receptions": ("receiving", "receptions"), "rushing_yards": ("rushing", "rushingYards")}
ALIAS = {"WSH": "WAS", "LAR": "LA"}


def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "research"}), timeout=25))


def utc(s):
    return datetime.fromisoformat(str(s).replace("Z", "+00:00"))


def events(dates):
    ev = {}
    for d in dates:
        for e in get(f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates={d}")["events"]:
            c = e["competitions"][0]
            t = {x["homeAway"]: ALIAS.get(x["team"]["abbreviation"], x["team"]["abbreviation"]) for x in c["competitors"]}
            ev[f"{t['away']}_{t['home']}"] = {"id": e["id"], "kickoff": utc(e["date"]), "status": c["status"]["type"]["name"]}
    return ev


def snapshot_before(path: str, kickoff: datetime):
    """The last committed version of the file whose retrieved_utc is before kickoff."""
    shas = subprocess.run(["git", "log", "--format=%h", "--", path], cwd=ROOT, capture_output=True, text=True).stdout.split()
    for h in shas:
        try:
            d = json.loads(subprocess.run(["git", "show", f"{h}:{path}"], cwd=ROOT, capture_output=True, text=True).stdout)
        except ValueError:
            continue
        if d.get("retrieved_utc") and utc(d["retrieved_utc"]) < kickoff:
            return d
    return None


def main_lines(rows):
    two = {}
    for r in rows:
        if r.get("player") and r.get("market") in STAT and r.get("side") in ("Over", "Under") and r.get("line") is not None:
            two.setdefault((_norm(r["player"]), r["market"], r["book"], float(r["line"])), {})[r["side"]] = float(r["american"])
    best = {}
    for (p, m, b, ln), s in two.items():
        if "Over" in s and "Under" in s:
            qo, qu = implied(s["Over"]), implied(s["Under"])
            d = abs(qo / (qo + qu) - 0.5)
            k = (p, m, b)
            if k not in best or d < best[k][1]:
                best[k] = (ln, d, s["Over"], s["Under"])
    return best


def actuals(eid):
    s = get(f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={eid}")
    out = {}
    for tm in s["boxscore"]["players"]:
        for cat in tm["statistics"]:
            for a in cat["athletes"]:
                st = dict(zip(cat["keys"], a["stats"]))
                for m, (c, k) in STAT.items():
                    if cat["name"] == c and k in st:
                        try:
                            out[(_norm(a["athlete"]["displayName"]), m)] = float(st[k])
                        except ValueError:
                            pass
    return out


def main():
    files = sorted((ROOT / "pregame" / "direct_lines").glob("2026_1[01]_*.json"))
    ev = events(["20261116", "20261117", "20261119", "20261120", "20261122", "20261123", "20261124"])
    rows = []
    for f in files:
        gid = f.stem
        pair = "_".join(gid.split("_")[-2:])
        e = ev.get(pair)
        if not e or e["status"] != "STATUS_FINAL":
            continue
        snap = snapshot_before(str(f.relative_to(ROOT)), e["kickoff"])
        if not snap:
            continue
        act = actuals(e["id"])
        for (p, m, b), (ln, _, po, pu) in main_lines(snap["rows"]).items():
            if (p, m) in act:
                rows.append({"game": gid, "pulled_utc": snap["retrieved_utc"], "player": p, "market": m, "book": b, "line": ln,
                             "over": po, "under": pu, "actual": act[(p, m)]})
    with open(HERE / "rows.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

    def summ(rs):
        o = sum(r["actual"] > r["line"] for r in rs); u = sum(r["actual"] < r["line"] for r in rs); p = len(rs) - o - u
        return {"props": len(rs), "over_won": o, "under_won": u, "push": p, "over_pct": round(o / max(o + u, 1), 3),
                "avg_miss": round(statistics.mean(abs(r["actual"] - r["line"]) for r in rs), 2) if rs else None}
    books = sorted({r["book"] for r in rows})
    res = {"games": sorted({r["game"] for r in rows}), "by_book": {b: summ([r for r in rows if r["book"] == b]) for b in books},
           "by_book_market": {f"{b}|{m}": summ([r for r in rows if r["book"] == b and r["market"] == m]) for b in books for m in STAT
                              if any(r["book"] == b and r["market"] == m for r in rows)}}
    # Bovada vs the other books on the same prop
    cons = {}
    for r in rows:
        if r["book"] not in ("bovada", "pinnacle"):
            cons.setdefault((r["game"], r["player"], r["market"]), []).append(r["line"])
    cmp_rows = []
    for r in rows:
        if r["book"] != "bovada":
            continue
        others = cons.get((r["game"], r["player"], r["market"]))
        if not others or len(others) < 2:
            continue
        med = statistics.median(others)
        gap = r["line"] - med
        cmp_rows.append(dict(r, consensus=med, gap=gap, bov_closer=abs(r["actual"] - r["line"]) < abs(r["actual"] - med),
                             cons_closer=abs(r["actual"] - med) < abs(r["actual"] - r["line"]),
                             went_bovada_way=(r["actual"] > med) if gap > 0 else (r["actual"] < med) if gap < 0 else None))
    def grp(rs):
        if not rs:
            return {"props": 0}
        way = [x["went_bovada_way"] for x in rs if x["went_bovada_way"] is not None and x["actual"] != x["consensus"]]
        return {"props": len(rs), "bovada_line_closer": sum(x["bov_closer"] for x in rs), "consensus_closer": sum(x["cons_closer"] for x in rs),
                "result_went_bovada_way_vs_consensus": f"{sum(way)} of {len(way)}",
                "bovada_avg_miss": round(statistics.mean(abs(x['actual'] - x['line']) for x in rs), 2),
                "consensus_avg_miss": round(statistics.mean(abs(x['actual'] - x['consensus']) for x in rs), 2)}
    res["bovada_vs_consensus"] = {
        "same_line": grp([x for x in cmp_rows if x["gap"] == 0]),
        "differs_small": grp([x for x in cmp_rows if 0 < abs(x["gap"]) <= (1 if x["market"] == "receptions" else 7.5)]),
        "differs_big (the board's outliers)": grp([x for x in cmp_rows if abs(x["gap"]) > (1 if x["market"] == "receptions" else 7.5)]),
        "bovada_higher_big": grp([x for x in cmp_rows if x["gap"] > (1 if x["market"] == "receptions" else 7.5)]),
        "bovada_lower_big": grp([x for x in cmp_rows if x["gap"] < -(1 if x["market"] == "receptions" else 7.5)])}
    res["big_gap_examples"] = sorted(({k: x[k] for k in ("game", "player", "market", "line", "consensus", "actual")} for x in cmp_rows
                                      if abs(x["gap"]) > (1 if x["market"] == "receptions" else 7.5)), key=lambda x: -abs(x["line"] - x["consensus"]))[:40]
    (HERE / "results.json").write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k != "big_gap_examples"}, indent=1))
    for x in res["big_gap_examples"][:25]:
        print(x)


if __name__ == "__main__":
    main()
