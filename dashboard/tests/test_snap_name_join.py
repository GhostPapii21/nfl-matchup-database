"""Snap shares are keyed by PFR's player name ("D.K. Metcalf", "Brian Thomas", "Luther Burden") but looked up by
roster / injury-report names ("DK Metcalf", "Brian Thomas Jr.", "Luther Burden III"). The lookup silently returned
None for 38 of 593 2026 skill players with snaps (6.4%), so "Most on field" tags and injury snap impact skipped them.
Fix: key by the roster full name through PFR id -> roster. refs NFL-75."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from dashboard import extras as X  # noqa: E402
from pregame import packet as PK  # noqa: E402

SNAPS = pd.DataFrame([
    dict(game_id="g1", week=1, team="PIT", player="D.K. Metcalf", pfr_player_id="MetcDK00", offense_snaps=60, offense_pct=0.9, defense_pct=0.0),
    dict(game_id="g1", week=1, team="PIT", player="Unmapped Guy", pfr_player_id="UnmaGu00", offense_snaps=10, offense_pct=0.2, defense_pct=0.0),
    dict(game_id="g1", week=1, team="PIT", player="T.J. Watt", pfr_player_id="WattTJ99", offense_snaps=0, offense_pct=0.0, defense_pct=0.85),
])
ROSTERS = pd.DataFrame([dict(gsis_id="00-1", full_name="DK Metcalf", pfr_id="MetcDK00", team="PIT", week=1),
                        dict(gsis_id="00-2", full_name="TJ Watt", pfr_id="WattTJ99", team="PIT", week=1)])


def test_offense_snap_share_uses_roster_names_when_ids_map():
    s = PK.snap_shares("PIT", SNAPS, [1], ROSTERS)
    assert s["DK Metcalf"] == 0.9 and "D.K. Metcalf" not in s
    assert s["Unmapped Guy"] == 0.2                       # no id match: keep PFR's name rather than drop the player


def test_offense_snap_share_without_rosters_is_unchanged():
    assert PK.snap_shares("PIT", SNAPS, [1]) == {"D.K. Metcalf": 0.9, "Unmapped Guy": 0.2}


def test_roles_find_the_snap_share_by_roster_name():
    players = {"receivers": [{"player": "D.Metcalf", "player_id": "00-1", "games": 1, "targets": 8, "receptions": 5, "yards": 70,
                              "target_share": 0.3, "log": [{"targets": 8, "yards": 70}]}], "rushers": []}
    r = X.receiver_roles(players, PK.snap_shares("PIT", SNAPS, [1], ROSTERS), {"00-1": "DK Metcalf"})
    rec = r["receivers"][0] if isinstance(r, dict) and "receivers" in r else r
    got = rec["snap_share"] if isinstance(rec, dict) else None
    assert got == 0.9


def test_defense_snap_share_uses_roster_names_when_ids_map():
    d = X.defense_snap_share(SNAPS, "PIT", ["g1"], ROSTERS)
    assert d == {"TJ Watt": 0.85}
    assert X.defense_snap_share(SNAPS, "PIT", ["g1"]) == {"T.J. Watt": 0.85}
