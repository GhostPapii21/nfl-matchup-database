"""Grade PRESS legs in press_live_2026.csv. Reads only: ESPN box scores (playlogs/<wk>/*_box.json, preferred and
complete) or play-log CSVs (playlogs/<wk>/*.csv, fallback; may be partial). Markets: pass yds (QB), rush yds, rec yds,
receptions. Usage: python3 grade_press.py playlogs/2026_wk9/*_box.json"""
import csv, json, re, sys
from collections import defaultdict
from press_live import FIELDS, TRACKER
MK = {"pass yds": "pyds", "rush yds": "ryds", "rec yds": "recyds", "receptions": "rec", "rec": "rec"}
def _f(x):
    try: return float(str(x).replace(",", ""))
    except ValueError: return 0.0
def totals(paths):
    t = defaultdict(float)
    for p in paths:
        if p.endswith(".json"):
            for tm in json.load(open(p, encoding="utf-8")).get("teams", {}).values():
                for r in tm.get("passing", []): t[(r["player"], "pyds")] += _f(r.get("YDS"))
                for r in tm.get("rushing", []): t[(r["player"], "ryds")] += _f(r.get("YDS"))
                for r in tm.get("receiving", []): t[(r["player"], "recyds")] += _f(r.get("YDS")); t[(r["player"], "rec")] += _f(r.get("REC"))
            continue
        for r in csv.DictReader(open(p, encoding="utf-8")):
            y = _f(r.get("yds") or 0)
            if r.get("kind") == "rush": t[(r["fullname"], "ryds")] += y
            if r.get("kind") == "rec": t[(r["fullname"], "recyds")] += y; t[(r["fullname"], "rec")] += 1
    return t
def grade(tracker=TRACKER, paths=()):
    t = totals(paths); rows = list(csv.DictReader(open(tracker))); n = 0
    for r in rows:
        if r["result"]: continue
        m = re.match(r"(.+?) (pass yds|rush yds|rec yds|receptions|rec) ([ou])([\d.]+)", r["leg"])
        if not m: continue
        key = (m.group(1), MK[m.group(2)])
        if key not in t: continue
        v = t[key]; hit = v > float(m.group(4)) if m.group(3) == "o" else v < float(m.group(4))
        r["result"] = f"{'HIT' if hit else 'MISS'} ({v:g})"; n += 1
    with open(tracker, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    return n
if __name__ == "__main__": print(f"graded {grade(paths=sys.argv[1:])} PRESS legs")
