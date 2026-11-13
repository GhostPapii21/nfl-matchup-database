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


def test_status_update_active_and_inactive(tmp_path):
    import json as _j
    from phase15.status_update import update
    g = "2026_10_WAS_NYG"
    (tmp_path / "phase15/status" / g).mkdir(parents=True)
    (tmp_path / "phase15/inactives" / g).mkdir(parents=True)
    base = {"team": "NYG", "official_inactives": {"status": "PENDING"}, "publishes_numbers": False}
    (tmp_path / "phase15/status" / g / "skattebo.json").write_text(_j.dumps(base))
    inv = {"retrieved_utc": "2026-11-12T23:50:00+00:00", "status": "OK", "teams": {
        "NYG": {"status": "OK", "url": "u", "published_utc": "p", "players": [{"name": "Some One"}]}}}
    (tmp_path / "phase15/inactives" / g / "inactives_1.json").write_text(_j.dumps(inv))
    assert update(g, "Cam Skattebo", tmp_path)["status"].startswith("ACTIVE")
    inv["teams"]["NYG"]["players"].append({"name": "Cam Skattebo"})
    (tmp_path / "phase15/inactives" / g / "inactives_2.json").write_text(_j.dumps(inv))
    assert update(g, "Cam Skattebo", tmp_path)["status"].startswith("INACTIVE")
    inv["teams"]["NYG"] = {"status": "MISSING", "reason": "not yet"}
    (tmp_path / "phase15/inactives" / g / "inactives_3.json").write_text(_j.dumps(inv))
    assert update(g, "Cam Skattebo", tmp_path)["status"] == "NO_DESIGNATION_PENDING_INACTIVES"


# ---- NFL-46: hook detail for the per-game ledger, slate puller ----

def test_ok_hook_carries_sources_published_and_file(tmp_path):
    oi.pull("2026_10_WAS_NYG", KO, now=KO - timedelta(minutes=80), getter=fake_get(PAGES), out_dir=tmp_path)
    h = oi.hook({"game": {"game_id": "2026_10_WAS_NYG"}}, out_dir=tmp_path)
    assert h["status"] == "OK" and h["file"].endswith(".json")
    assert h["sources"]["NYG"].startswith("https://www.giants.com/news/inactives")
    assert h["sources"]["WAS"].startswith("https://www.commanders.com/news/inactives")
    assert h["published_utc"]["NYG"].startswith("2026-11-12T23:45")


def test_incomplete_hook_keeps_pull_time_and_sources(tmp_path):
    pages = dict(PAGES); del pages["/news/inactives-giants-commanders-week-10"]
    oi.pull("2026_10_WAS_NYG", KO, now=KO - timedelta(minutes=80), getter=fake_get(pages), out_dir=tmp_path)
    h = oi.hook({"game": {"game_id": "2026_10_WAS_NYG"}}, out_dir=tmp_path)
    assert h["status"] == "INCOMPLETE" and h["retrieved_utc"] and h["file"]
    assert h["sources"]["WAS"].startswith("https://www.commanders.com/news/inactives")
    assert h["sources"]["NYG"] == oi.CLUB_SITES["NYG"][0]   # index page tried; no article -> not a source of names


def test_unreadable_pull_file_is_incomplete(tmp_path):
    d = tmp_path / "2026_10_WAS_NYG"; d.mkdir()
    (d / "inactives_20261113T000000Z.json").write_text("{broken")
    assert oi.hook({"game": {"game_id": "2026_10_WAS_NYG"}}, out_dir=tmp_path)["status"] == "INCOMPLETE"


def test_pull_file_for_other_game_is_not_ok(tmp_path):
    f = oi.pull("2026_10_WAS_NYG", KO, now=KO - timedelta(minutes=80), getter=fake_get(PAGES), out_dir=tmp_path)
    d = tmp_path / "2026_10_DAL_PHI"; d.mkdir()
    (d / f.name).write_text(f.read_text())
    assert oi.hook({"game": {"game_id": "2026_10_DAL_PHI"}}, out_dir=tmp_path)["status"] == "INCOMPLETE"


def test_slate_pulls_only_inside_window(tmp_path, monkeypatch):
    idx = tmp_path / "latest.json"
    idx.write_text(json.dumps({"games": [{"game_id": "2026_10_WAS_NYG"}, {"game_id": "2026_10_DAL_PHI"}, {"game_id": "2026_10_X_Y"}]}))
    kos = {"2026_10_WAS_NYG": KO, "2026_10_DAL_PHI": KO + timedelta(days=3), "2026_10_X_Y": None}
    monkeypatch.setattr(oi, "_kickoff_from_packet", lambda g: kos[g])
    rows = oi.slate(now=KO - timedelta(minutes=80), getter=fake_get(PAGES), out_dir=tmp_path / "out", index=idx)
    by = {r["game_id"]: r for r in rows}
    assert by["2026_10_WAS_NYG"]["action"] == "PULLED" and by["2026_10_WAS_NYG"]["status"] == "OK"
    assert by["2026_10_DAL_PHI"]["action"] == "SKIPPED" and by["2026_10_X_Y"]["action"] == "SKIPPED"
    assert not (tmp_path / "out" / "2026_10_DAL_PHI").exists()


def test_slate_never_pulls_after_kickoff(tmp_path, monkeypatch):
    idx = tmp_path / "latest.json"
    idx.write_text(json.dumps({"games": [{"game_id": "2026_10_WAS_NYG"}]}))
    monkeypatch.setattr(oi, "_kickoff_from_packet", lambda g: KO)
    def no_net(*a, **k):
        raise AssertionError("network used outside window")
    rows = oi.slate(now=KO + timedelta(minutes=1), getter=no_net, out_dir=tmp_path / "out", index=idx)
    assert rows[0]["action"] == "SKIPPED"


def test_kickoff_from_packet_uses_date_and_et_for_indoor(tmp_path, monkeypatch):
    g = "2026_10_DAL_DET"
    d = tmp_path / "pregame" / "packets" / g; d.mkdir(parents=True)
    (d / "packet.json").write_text(json.dumps({"game": {"date": "2026-11-15", "kickoff_et": "13:00"}, "weather": {"status": "INDOOR"}}))
    monkeypatch.setattr(oi, "ROOT", tmp_path)
    assert oi._kickoff_from_packet(g) == datetime(2026, 11, 15, 18, 0, tzinfo=timezone.utc)
