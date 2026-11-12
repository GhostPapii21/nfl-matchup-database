"""Phase 15 official inactives: parsing, timing window, fail-closed hook. Offline (fixtures inline)."""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from phase15 import official_inactives as oi

KO = datetime(2026, 11, 13, 1, 15, tzinfo=timezone.utc)
GIANTS = """<html><script type="application/ld+json">{"datePublished":"2026-11-12T23:45:00.000Z"}</script>
<h1>Inactives: Who's in, who's out for Giants vs. Commanders</h1>
<p><strong>GIANTS INACTIVES</strong></p><ul><li>TE Thomas Fidone II</li><li>CB Nikko Reed</li></ul>
<p><strong>COMMANDERS INACTIVES</strong></p><ul><li>C Lucas Patrick</li><li>TE Colson Yankoff</li></ul>
<ul><li>PRO SHOP</li></ul></html>"""
COMMANDERS = """<html><script>{"datePublished":"2026-11-12T23:44:10.13Z"}</script>
<ul><li>No. 13 WR Treylon Burks</li><li>No. 16 QB Athan Kaliakmanis (Emergency QB)</li><li>NFL Shop</li></ul></html>"""
INDEX_G = '<a href="/news/inactives-giants-commanders-week-10">x</a><a href="/news/other">y</a>'
INDEX_W = '<a href="/news/inactives-commanders-vs-giants-week-10">x</a>'


def fake_get(pages):
    def g(url, timeout=20):
        for k, v in pages.items():
            if url.endswith(k):
                return v
        raise OSError(f"404 {url}")
    return g


PAGES = {"giants.com/news/": INDEX_G, "/news/inactives-giants-commanders-week-10": GIANTS,
         "football-news-archive": INDEX_W, "/news/inactives-commanders-vs-giants-week-10": COMMANDERS}


def test_section_parse_takes_only_own_team():
    assert [p["name"] for p in oi.parse_inactives(GIANTS, "GIANTS")] == ["Thomas Fidone II", "Nikko Reed"]


def test_single_team_article_and_notes():
    ps = oi.parse_inactives(COMMANDERS, "COMMANDERS")
    assert [p["name"] for p in ps] == ["Treylon Burks", "Athan Kaliakmanis"]
    assert ps[1]["note"] == "Emergency QB"


def test_pull_writes_timestamped_ok_file_and_hook_reads_it(tmp_path):
    now = KO - timedelta(minutes=80)
    f = oi.pull("2026_10_WAS_NYG", KO, now=now, getter=fake_get(PAGES), out_dir=tmp_path)
    rec = json.loads(f.read_text())
    assert rec["status"] == "OK" and rec["retrieved_utc"].startswith("2026-11-12T23:55")
    assert rec["inactives"]["NYG"] == ["Thomas Fidone II", "Nikko Reed"]
    assert all(v["url"] and v["sha256"] and v["published_utc"] for v in rec["teams"].values())
    h = oi.hook({"game": {"game_id": "2026_10_WAS_NYG"}}, out_dir=tmp_path)
    assert h["status"] == "OK" and set(h["inactives"]) == {"WAS", "NYG"}


def test_last_weeks_article_is_not_accepted(tmp_path):
    old = GIANTS.replace("2026-11-12T23:45", "2026-11-08T16:30")
    pages = dict(PAGES); pages["/news/inactives-giants-commanders-week-10"] = old
    f = oi.pull("2026_10_WAS_NYG", KO, now=KO - timedelta(minutes=80), getter=fake_get(pages), out_dir=tmp_path)
    rec = json.loads(f.read_text())
    assert rec["status"] == "INCOMPLETE" and rec["teams"]["NYG"]["status"] == "MISSING"
    assert oi.hook({"game": {"game_id": "2026_10_WAS_NYG"}}, out_dir=tmp_path)["status"] == "INCOMPLETE"


def test_hook_missing_fails_closed(tmp_path):
    assert oi.hook({"game": {"game_id": "2026_10_WAS_NYG"}}, out_dir=tmp_path)["status"] == "MISSING"


def test_network_error_is_missing_not_crash(tmp_path):
    f = oi.pull("2026_10_WAS_NYG", KO, now=KO, getter=fake_get({}), out_dir=tmp_path)
    assert json.loads(f.read_text())["status"] == "INCOMPLETE"


def test_every_team_has_a_club_site():
    assert len(oi.CLUB_SITES) == 32
