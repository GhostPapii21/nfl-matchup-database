"""Grade the live stars against the side-by-side candidate for every saved game that is final (ESPN box scores).

    python3 research/shadow_2026-11-23/grade.py          # writes graded.json; cumulative over all saved games
Brier score (lower is better) on the 80+ yard outcome for every receiver; plus hits among each version's stars.
The candidate replaces nothing until it beats the live stars over several weeks."""
import json
import re
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
AL = {"WSH": "WAS", "LAR": "LA"}


def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "research"}), timeout=25))


def norm(s):
    return " ".join(w for w in re.sub(r"[^a-z ]", "", s.lower().replace("-", " ")).split() if w not in {"jr", "sr", "ii", "iii", "iv"})


def main():
    rows = []
    for f in sorted((HERE / "live").glob("*.json")):
        snap = json.loads(f.read_text())
        d = snap["kickoff_utc"][:10].replace("-", "")
        away, home = snap["game_id"].split("_")[-2:]
        ev = None
        for day in (d, str(int(d) - 1)):
            for e in get(f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates={day}")["events"]:
                c = e["competitions"][0]
                t = {x["homeAway"]: AL.get(x["team"]["abbreviation"], x["team"]["abbreviation"]) for x in c["competitors"]}
                if t.get("away") == away and t.get("home") == home:
                    ev = (e["id"], c["status"]["type"]["name"])
        if not ev or ev[1] != "STATUS_FINAL":
            continue
        s = get(f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={ev[0]}")
        yds = {}
        for tm in s["boxscore"]["players"]:
            for cat in tm["statistics"]:
                if cat["name"] == "receiving":
                    i = cat["keys"].index("receivingYards")
                    for a in cat["athletes"]:
                        yds[norm(a["athlete"]["displayName"])] = int(a["stats"][i])
        for r in snap["receivers"]:
            if r.get("p80_shadow") is None:
                continue
            y = yds.get(norm(r["player"]), 0)
            rows.append(dict(r, game=snap["game_id"], yards=y, hit80=int(y >= 80)))
    if not rows:
        print("grade: no final games yet"); return
    brier = lambda k: round(sum((r[k] - r["hit80"]) ** 2 for r in rows) / len(rows), 5)
    stars = lambda k: {"starred": sum(1 for r in rows if r[k]), "hit": sum(r["hit80"] for r in rows if r[k])}
    out = {"games": sorted({r["game"] for r in rows}), "receivers": len(rows), "hit80": sum(r["hit80"] for r in rows),
           "brier_live": brier("p80_live"), "brier_shadow": brier("p80_shadow"),
           "stars_live": stars("stars_live"), "stars_shadow": stars("stars_shadow"),
           "changed": [{k: r[k] for k in ("game", "player", "p80_live", "p80_shadow", "stars_live", "stars_shadow", "yards")} for r in rows if r["stars_live"] != r["stars_shadow"]]}
    (HERE / "graded.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
