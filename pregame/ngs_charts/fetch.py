"""Download Next Gen Stats route and carry charts for chosen teams (owner, Nov 25, 2026).

Each NGS route chart draws a receiver's targeted routes in one game (catch, incompletion, TD, INT); a carry chart draws
each carry. Matched to play-by-play by week, depth, side and yards, they add route shape to the zone matchup profile
(research/projections_2026_w12/zones.py). Images stay NFL's: this runs on GitHub's runners (the session sandbox cannot
reach the NGS hosts) and the images are kept as a short-lived private workflow artifact, never committed.

How: a headless browser opens each team's public chart list (nextgenstats.nfl.com/charts/list/type/<team>/<season>/week),
scrolls it, and records every chart image it shows plus any JSON the page loads. The 900px version of each route and
carry chart in the chosen weeks is then downloaded once.

    python -m pregame.ngs_charts.fetch --teams GB,LA --season 2026 --weeks 6-11 --out ngs_charts_out
"""
from __future__ import annotations

import argparse
import json
import re
import time
import urllib.request
from pathlib import Path

SLUG = {"ARI": "arizona-cardinals", "ATL": "atlanta-falcons", "BAL": "baltimore-ravens", "BUF": "buffalo-bills",
        "CAR": "carolina-panthers", "CHI": "chicago-bears", "CIN": "cincinnati-bengals", "CLE": "cleveland-browns",
        "DAL": "dallas-cowboys", "DEN": "denver-broncos", "DET": "detroit-lions", "GB": "green-bay-packers",
        "HOU": "houston-texans", "IND": "indianapolis-colts", "JAX": "jacksonville-jaguars", "KC": "kansas-city-chiefs",
        "LV": "las-vegas-raiders", "LAC": "los-angeles-chargers", "LA": "los-angeles-rams", "LAR": "los-angeles-rams",
        "MIA": "miami-dolphins", "MIN": "minnesota-vikings", "NE": "new-england-patriots", "NO": "new-orleans-saints",
        "NYG": "new-york-giants", "NYJ": "new-york-jets", "PHI": "philadelphia-eagles", "PIT": "pittsburgh-steelers",
        "SF": "san-francisco-49ers", "SEA": "seattle-seahawks", "TB": "tampa-bay-buccaneers", "TEN": "tennessee-titans",
        "WAS": "washington-commanders"}
IMG = re.compile(r"static-charts/\d+/(route|carry)-chart_([A-Z0-9]+)_(\d{4})-(REG|POST|PRE)-(\d+)_(\d+)\.jpe?g")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def weeks_of(spec: str) -> set[int]:
    out = set()
    for part in spec.split(","):
        a, _, b = part.partition("-")
        out |= set(range(int(a), int(b or a) + 1))
    return out


def parse_cards(cards: list[dict]) -> list[dict]:
    """cards: [{'src': img src, 'href': link, 'text': card text}] -> chart rows (deduplicated by image)."""
    rows, seen = [], set()
    for c in cards:
        m = IMG.search(c.get("src") or "")
        if not m:
            continue
        kind, pid, season, stype, week, stamp = m.groups()
        key = (kind, pid, season, stype, week, stamp)
        if key in seen:
            continue
        seen.add(key)
        text = " ".join((c.get("text") or "").split())
        name = text.split(" ")[0:3]
        slug = (c.get("href") or "").rstrip("/").split("/")
        rows.append({"type": kind, "ngs_id": pid, "season": int(season), "season_type": stype, "week": int(week),
                     "player_slug": slug[-2] if len(slug) >= 2 else None, "card_text": text,
                     "url": "https://" + c["src"].split("://", 1)[-1].split("/static-charts/")[0] + f"/static-charts/900/{kind}-chart_{pid}_{season}-{stype}-{week}_{stamp}.jpeg"})
    return rows


def collect(team: str, season: int, page, log) -> tuple[list[dict], list[str]]:
    jsons = []

    def on_response(r):
        try:
            if "json" in (r.headers.get("content-type") or "") and "nfl.com" in r.url:
                jsons.append({"url": r.url, "body": r.json()})
        except Exception:  # noqa: BLE001
            pass
    page.on("response", on_response)
    url = f"https://nextgenstats.nfl.com/charts/list/type/{SLUG[team]}/{season}/week"
    page.goto(url, wait_until="networkidle", timeout=90000)
    last = -1
    for _ in range(40):                                   # the list grows as it scrolls
        page.mouse.wheel(0, 20000)
        time.sleep(1.2)
        n = page.locator("img").count()
        if n == last:
            break
        last = n
    cards = page.evaluate("""() => Array.from(document.querySelectorAll('a')).filter(a => a.querySelector('img'))
        .map(a => ({href: a.href, text: a.innerText, src: Array.from(a.querySelectorAll('img')).map(i => i.src).find(s => s.includes('static-charts')) || ''}))""")
    page.remove_listener("response", on_response)
    log.append({"team": team, "page": url, "cards": len(cards), "json_urls": sorted({j["url"].split("?")[0] for j in jsons})})
    return cards, jsons


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--teams", required=True)
    ap.add_argument("--season", type=int, default=2026)
    ap.add_argument("--weeks", default="1-18")
    ap.add_argument("--types", default="route,carry")
    ap.add_argument("--out", default="ngs_charts_out")
    a = ap.parse_args(argv)
    from playwright.sync_api import sync_playwright
    out = Path(a.out); (out / "img").mkdir(parents=True, exist_ok=True)
    wk, types = weeks_of(a.weeks), set(a.types.split(","))
    index, log = [], []
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        page = br.new_page(user_agent=UA, viewport={"width": 1400, "height": 2000})
        for team in [t.strip().upper() for t in a.teams.split(",") if t.strip()]:
            try:
                cards, jsons = collect(team, a.season, page, log)
            except Exception as e:  # noqa: BLE001
                log.append({"team": team, "error": repr(e)}); continue
            (out / f"raw_{team}.json").write_text(json.dumps({"cards": cards, "json": jsons}, default=str)[:20_000_000])
            for r in parse_cards(cards):
                if r["season"] == a.season and r["week"] in wk and r["type"] in types:
                    r["team"] = team
                    index.append(r)
        br.close()
    seen = set()
    for r in index:
        f = out / "img" / f"{r['team']}_w{r['week']:02d}_{r['type']}_{r['player_slug'] or r['ngs_id']}.jpeg"
        r["file"] = str(f.relative_to(out))
        if r["url"] in seen:
            continue
        seen.add(r["url"])
        try:
            req = urllib.request.Request(r["url"], headers={"User-Agent": UA, "Referer": "https://nextgenstats.nfl.com/"})
            f.write_bytes(urllib.request.urlopen(req, timeout=30).read())
            r["downloaded"] = True
        except Exception as e:  # noqa: BLE001
            r["downloaded"] = False; r["error"] = repr(e)
        time.sleep(0.3)
    (out / "index.json").write_text(json.dumps({"teams": a.teams, "season": a.season, "weeks": a.weeks, "pages": log, "charts": index}, indent=1))
    ok = sum(1 for r in index if r.get("downloaded"))
    print(json.dumps({"pages": log, "charts_found": len(index), "downloaded": ok}, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
