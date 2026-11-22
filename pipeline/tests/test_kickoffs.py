"""ESPN kickoff cross-check: a swapped schedule slot must not open the window late or let a lock pass after kickoff."""
import json
from datetime import datetime, timezone

from pipeline import freshness, kickoffs, window

BOARD = {"events": [
    {"date": "2026-11-22T18:00Z", "competitions": [{"competitors": [
        {"homeAway": "home", "team": {"abbreviation": "PHI"}}, {"homeAway": "away", "team": {"abbreviation": "PIT"}}]}]},
    {"date": "2026-11-24T01:15Z", "competitions": [{"competitors": [
        {"homeAway": "home", "team": {"abbreviation": "WSH"}}, {"homeAway": "away", "team": {"abbreviation": "CIN"}}]}]},
]}
SWAPPED = {"game": {"game_id": "2026_11_PIT_PHI", "date": "2026-11-22", "kickoff_et": "16:25"}}


def _write(games):
    kickoffs.path().write_text(json.dumps({"games": games}))


def test_parse_maps_espn_codes():
    g = kickoffs.parse(BOARD)
    assert g == {"PIT_PHI": "2026-11-22T18:00:00+00:00", "CIN_WAS": "2026-11-24T01:15:00+00:00"}


def test_refresh_fail_soft_keeps_nothing_on_error():
    def boom(u):
        raise OSError("offline")
    assert kickoffs.refresh(datetime(2026, 11, 22, 15, tzinfo=timezone.utc), get=boom) == {}
    assert not kickoffs.path().exists()


def test_refresh_writes_file():
    rec = kickoffs.refresh(datetime(2026, 11, 22, 15, tzinfo=timezone.utc), get=lambda u: json.dumps(BOARD).encode())
    assert rec["games"]["PIT_PHI"].startswith("2026-11-22T18:00")
    assert json.loads(kickoffs.path().read_text())["source"] == "ESPN public scoreboard"


def test_espn_overrides_swapped_packet_kickoff():
    assert freshness.kickoff_utc(SWAPPED) == datetime(2026, 11, 22, 21, 25, tzinfo=timezone.utc)      # no file: packet time
    _write({"PIT_PHI": "2026-11-22T18:00:00+00:00"})
    assert freshness.kickoff_utc(SWAPPED) == datetime(2026, 11, 22, 18, 0, tzinfo=timezone.utc)


def test_lookup_ignores_a_different_week_rematch():
    _write({"PIT_PHI": "2026-12-20T18:00:00+00:00"})
    assert freshness.kickoff_utc(SWAPPED) == datetime(2026, 11, 22, 21, 25, tzinfo=timezone.utc)


def test_window_opens_on_the_real_kickoff(tmp_path):
    pk = tmp_path / "pregame" / "packets"
    (pk / "2026_11_PIT_PHI").mkdir(parents=True)
    (pk / "latest.json").write_text(json.dumps({"games": [{"game_id": "2026_11_PIT_PHI"}]}))
    (pk / "2026_11_PIT_PHI" / "packet.json").write_text(json.dumps(SWAPPED))
    _write({"PIT_PHI": "2026-11-22T18:00:00+00:00"})
    rows = window.evaluate(now=datetime(2026, 11, 22, 16, 50, tzinfo=timezone.utc), root=tmp_path)["games"]
    assert rows[0]["kickoff_utc"].startswith("2026-11-22T18:00") and rows[0]["minutes_to_kickoff"] == 70.0


def test_lock_uses_the_earlier_kickoff():
    from snapshots import lock
    g = {"game_id": "2026_11_PIT_PHI", "kickoff_et": "2026-11-22T16:25:00-05:00"}
    assert lock.effective_kickoff(g)[0] == datetime(2026, 11, 22, 21, 25, tzinfo=timezone.utc)
    _write({"PIT_PHI": "2026-11-22T18:00:00+00:00"})
    used, cfg, espn = lock.effective_kickoff(g)
    assert used == espn == datetime(2026, 11, 22, 18, 0, tzinfo=timezone.utc) and cfg > used
    _write({"PIT_PHI": "2026-11-22T23:00:00+00:00"})          # ESPN later than config: still the config time
    assert lock.effective_kickoff(g)[0] == datetime(2026, 11, 22, 21, 25, tzinfo=timezone.utc)
