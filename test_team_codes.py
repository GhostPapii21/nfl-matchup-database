"""Team-code consistency (refs NFL-75). Canonical codes are nflverse's (LA, WAS, JAX, LV, LAC, ARI ...).

Bug (2026-11-22 data audit): the defender ledger, the CB/S profile files, the Sharp man/zone table and the Blitz team
database use LAR/WSH, while play-by-play, schedules, packets and the season context use LA/WAS. Joining them drops
every Rams and Commanders row without an error. These tests pin one normalizer applied when those files are read.
"""
import csv
import glob
import json
from pathlib import Path

import pandas as pd
import pytest

from source_adapters import team_codes as tc

ROOT = Path(__file__).resolve().parent
SCHEDULE = ROOT / "research/season_context_2026/games.csv"

# Files read for coverage / defense work that carry team codes (path, team columns).
ALIAS_CODED_TABLES = [
    ("data/historical/ledgers/defender_ledger.csv", ["team"]),
    ("research/week9_cb_safety_profiles/DEFENDER_PROFILES.csv", ["team", "opponent_team_code"]),
    ("research/week9_cb_safety_profiles/DEFENDER_GAME_OBSERVATIONS.csv", ["team", "opponent"]),
    ("research/week9_cb_safety_profiles/DEFENDER_RECEIVER_OBSERVATIONS.csv", ["team"]),
    ("research/WEEK9_COVERAGE_SCHEMES_TEAM.csv", ["team"]),
    ("data/redistributable/teams/defense/defense_db.csv", ["team"]),
    ("data/redistributable/teams/offense/offense_db.csv", ["team"]),
]


def test_canonical_set_is_the_32_nflverse_codes():
    assert len(tc.CANONICAL) == 32
    assert {"LA", "WAS", "JAX", "LV", "LAC", "ARI"} <= tc.CANONICAL
    assert not ({"LAR", "WSH", "JAC", "OAK", "SD", "ARZ"} & tc.CANONICAL)


@pytest.mark.parametrize("raw,want", [
    ("LAR", "LA"), ("WSH", "WAS"), ("JAC", "JAX"), ("OAK", "LV"), ("LVR", "LV"), ("SD", "LAC"), ("STL", "LA"),
    ("ARZ", "ARI"), ("BLT", "BAL"), ("CLV", "CLE"), ("HST", "HOU"), ("GNB", "GB"), ("KAN", "KC"), ("NWE", "NE"),
    ("NOR", "NO"), ("SFO", "SF"), ("TAM", "TB"), ("WFT", "WAS"), (" lar ", "LA"), ("la", "LA"), ("KC", "KC"),
])
def test_canon_maps_every_known_alias(raw, want):
    assert tc.canon(raw) == want


@pytest.mark.parametrize("bad", ["XXX", "", "L.A.", "Rams", None, 7])
def test_canon_refuses_unknown_codes(bad):
    with pytest.raises(ValueError):
        tc.canon(bad)


def test_assert_canonical_names_the_bad_codes():
    with pytest.raises(ValueError, match="LAR"):
        tc.assert_canonical(["KC", "LAR", "WAS"], where="probe")
    tc.assert_canonical(["KC", "LA", "WAS"], where="probe")


def test_canon_game_string():
    assert tc.canon_game("BUF@LAR") == "BUF@LA"
    assert tc.canon_game("WSH@NYG") == "WAS@NYG"


def test_frame_normalizes_named_columns_and_leaves_missing_values():
    df = pd.DataFrame({"team": ["LAR", "WSH", None], "opp": ["SEA", "LAR", "DAL"], "x": [1, 2, 3]})
    out = tc.canon_frame(df, ["team", "opp"])
    assert out.team.tolist()[:2] == ["LA", "WAS"] and pd.isna(out.team.iloc[2])
    assert out.opp.tolist() == ["SEA", "LA", "DAL"]
    assert df.team.iloc[0] == "LAR"          # input not mutated


def _schedule_teams():
    g = pd.read_csv(SCHEDULE)
    return set(g.away) | set(g.home)


@pytest.mark.parametrize("path,cols", ALIAS_CODED_TABLES)
def test_raw_coverage_tables_lose_rows_on_join_without_normalizing(path, cols):
    """Documents the bug: the raw files carry codes the schedule does not, so an inner join drops rows."""
    raw = pd.read_csv(ROOT / path, dtype=str, low_memory=False)
    teams = _schedule_teams()
    assert (~raw[cols[0]].isin(teams) & raw[cols[0]].notna()).any(), f"{path}: no alias rows left; drop this case"


@pytest.mark.parametrize("path,cols", ALIAS_CODED_TABLES)
def test_read_team_table_keeps_every_row_on_schedule_join(path, cols):
    df = tc.read_team_table(ROOT / path, cols)
    teams = _schedule_teams()
    for c in cols:
        v = df[c].dropna()
        tc.assert_canonical(v, where=f"{path}:{c}")
        assert v.isin(teams).all()
    joined = df.merge(pd.DataFrame({cols[0]: sorted(teams)}), on=cols[0], how="inner")
    assert len(joined) == df[cols[0]].notna().sum(), f"{path}: rows lost on join"
    raw = pd.read_csv(ROOT / path, dtype=str, low_memory=False)
    if (raw[cols[0]] == "LAR").any():
        assert (df[cols[0]] == "LA").sum() == (raw[cols[0]] == "LAR").sum() + (raw[cols[0]] == "LA").sum()
    if (raw[cols[0]] == "WSH").any():
        assert (df[cols[0]] == "WAS").sum() == (raw[cols[0]] == "WSH").sum() + (raw[cols[0]] == "WAS").sum()


def test_read_team_table_normalizes_game_strings():
    df = tc.read_team_table(ROOT / "data/historical/ledgers/defender_ledger.csv", ["team"], game_cols=["game"])
    sides = set(df.game.str.split("@").explode().dropna())
    tc.assert_canonical(sides, where="defender_ledger.game")


# Datasets whose contract is canonical codes: they must already be canonical on disk (catches drift at the source).
CANONICAL_BY_CONTRACT = [
    ("research/season_context_2026/games.csv", ["away", "home"]),
    ("research/season_context_2026/team_games.csv", ["team", "opp"]),
    ("research/season_context_2026/team_profile.csv", ["team"]),
]


@pytest.mark.parametrize("path,cols", CANONICAL_BY_CONTRACT)
def test_canonical_datasets_have_no_alias_codes(path, cols):
    df = pd.read_csv(ROOT / path, dtype=str)
    for c in cols:
        tc.assert_canonical(df[c].dropna(), where=f"{path}:{c}")


def test_pregame_packets_use_canonical_codes():
    files = sorted(glob.glob(str(ROOT / "pregame/packets/*/packet.json")))
    if not files:
        pytest.skip("no packets checked out")
    for f in files:
        pk = json.loads(Path(f).read_text())
        g = pk.get("game") or {}
        tc.assert_canonical([g.get("away"), g.get("home"), *(pk.get("teams") or {}).keys()], where=f)
