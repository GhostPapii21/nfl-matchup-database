"""Fetch missing official NFL game books (Game Summary PDFs) for completed 2026 games, then parse them with
parse_nfl_game_summary.py into data/gamebooks/{season}/wk{WW}/{game_id}/ (same layout as Week 9).

How a PDF is found: the NFL.com game page https://www.nfl.com/games/{away-nickname}-at-{home-nickname}-{season}-reg-{week}
links "Download Game Book (PDF)" at static.www.nfl.com/.../gamecenter/<id>.pdf. Nothing is guessed: if the page or the
link is not found, the game is recorded as NOT_FOUND with the reason in the week's MANIFEST.csv and retried next run.
Games that already have parsed/ are skipped. NFL game summaries are media-use documents (see each game's README)."""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
import subprocess
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
UA = {"User-Agent": "Mozilla/5.0 (research; nfl-matchup-database)", "Accept": "text/html,application/pdf"}
PDF_RE = re.compile(r"https://static\.www\.nfl\.com/image/upload/[^\"'\s<>]*?/gamecenter/[0-9a-f-]{36}\.pdf")
NICK = {"ARI": "cardinals", "ATL": "falcons", "BAL": "ravens", "BUF": "bills", "CAR": "panthers", "CHI": "bears", "CIN": "bengals",
        "CLE": "browns", "DAL": "cowboys", "DEN": "broncos", "DET": "lions", "GB": "packers", "HOU": "texans", "IND": "colts",
        "JAX": "jaguars", "KC": "chiefs", "LA": "rams", "LAC": "chargers", "LV": "raiders", "MIA": "dolphins", "MIN": "vikings",
        "NE": "patriots", "NO": "saints", "NYG": "giants", "NYJ": "jets", "PHI": "eagles", "PIT": "steelers", "SEA": "seahawks",
        "SF": "49ers", "TB": "buccaneers", "TEN": "titans", "WAS": "commanders"}
FIELDS = ["game_id", "away", "home", "date", "source_url", "http_status", "sha256", "pages", "final_score_from_pdf", "status", "reason"]


def get(url, timeout=60):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return r.status, r.read()


def find_pdf(season, week, away, home):
    page = f"https://www.nfl.com/games/{NICK[away]}-at-{NICK[home]}-{season}-reg-{week}"
    try:
        st, html = get(page)
    except Exception as e:  # noqa: BLE001
        return None, page, f"game page not reachable: {type(e).__name__}: {e}"[:200]
    m = PDF_RE.search(html.decode("utf-8", "replace"))
    return (m.group(0), page, "linked from the game page") if m else (None, page, f"no game book link on the page (HTTP {st})")


def one(season, row, out_week: Path):
    gid = row.game_id
    d = out_week / gid
    if (d / "parsed").exists():
        return None
    url, page, why = find_pdf(season, int(row.week), row.away_team, row.home_team)
    rec = {"game_id": gid, "away": row.away_team, "home": row.home_team, "date": row.gameday, "source_url": url or page,
           "http_status": "", "sha256": "", "pages": "", "final_score_from_pdf": "", "status": "NOT_FOUND", "reason": why}
    if not url:
        return rec
    try:
        st, pdf = get(url, 120)
    except Exception as e:  # noqa: BLE001
        rec.update(reason=f"PDF download failed: {e}"[:200])
        return rec
    if not pdf.startswith(b"%PDF"):
        rec.update(http_status=st, reason="response is not a PDF")
        return rec
    d.mkdir(parents=True, exist_ok=True)
    pf, tf = d / f"{gid}_gamebook.pdf", d / f"{gid}_gamebook.txt"
    pf.write_bytes(pdf)
    subprocess.run(["pdftotext", "-layout", str(pf), str(tf)], check=True)
    pages = subprocess.run(["pdfinfo", str(pf)], capture_output=True, text=True).stdout
    npages = int(re.search(r"Pages:\s+(\d+)", pages).group(1)) if "Pages:" in pages else None
    r = subprocess.run([sys.executable, str(HERE / "parse_nfl_game_summary.py"), "--text", str(tf), "--pdf", str(pf), "--out", str(d / "parsed"),
                        "--provenance-out", str(d / "provenance.json"), "--game-id", gid, "--week", str(int(row.week)),
                        "--ingested-date", date.today().isoformat(), "--source-url", url] + (["--pdf-pages", str(npages)] if npages else []),
                       capture_output=True, text=True)
    rec.update(http_status=st, sha256=hashlib.sha256(pdf).hexdigest(), pages=npages or "")
    if r.returncode != 0:
        rec.update(status="PARSE_FAILED", reason=(r.stderr or r.stdout)[-200:])
        return rec
    rec.update(status="FOUND", reason=f"Official NFL Game Summary PDF {why}: {page}")
    return rec


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--season", type=int, default=2026)
    ap.add_argument("--weeks", default="", help="e.g. 1-10 (blank = every completed week)")
    ap.add_argument("--max-games", type=int, default=200)
    a = ap.parse_args(argv)
    g = pd.read_parquet(ROOT / "pregame" / ".cache" / "games.parquet")
    g = g[(g.season == a.season) & (g.game_type == "REG") & g.home_score.notna()]
    if a.weeks:
        lo, _, hi = a.weeks.partition("-")
        g = g[g.week.between(int(lo), int(hi or lo))]
    done = tried = 0
    for w, x in g.groupby("week"):
        out_week = HERE / str(a.season) / f"wk{int(w):02d}"
        man = out_week / "MANIFEST.csv"
        old = {r["game_id"]: r for r in csv.DictReader(man.open())} if man.exists() else {}
        for row in x.itertuples():
            if tried >= a.max_games:
                break
            rec = one(a.season, row, out_week)
            if rec is None:
                continue
            tried += 1
            done += rec["status"] == "FOUND"
            old[row.game_id] = rec
            print(f"{row.game_id}: {rec['status']} - {rec['reason'][:120]}")
            time.sleep(1.5)
        if old:
            out_week.mkdir(parents=True, exist_ok=True)
            with man.open("w", newline="") as f:
                wr = csv.DictWriter(f, fieldnames=FIELDS)
                wr.writeheader()
                for k in sorted(old):
                    wr.writerow({c: old[k].get(c, "") for c in FIELDS})
    print(f"game books: {done} fetched and parsed, {tried - done} not found or failed, of {tried} tried")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
