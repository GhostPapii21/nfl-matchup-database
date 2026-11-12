"""Load team-only history — never silent league/future fallback."""
from __future__ import annotations
from pathlib import Path
from typing import Sequence
import pandas as pd

COLS = [
    "game_id", "season", "week", "home_team", "away_team", "posteam", "defteam",
    "qtr", "down", "ydstogo", "yardline_100", "game_seconds_remaining",
    "play_type", "yards_gained", "touchdown", "interception", "fumble_lost",
    "field_goal_result", "extra_point_result", "two_point_conv_result",
    "kickoff_attempt", "punt_attempt", "passer_player_name", "rusher_player_name",
    "receiver_player_name", "complete_pass", "incomplete_pass", "sack",
    "first_down", "fixed_drive_result", "drive", "play_id", "desc",
    "total_home_score", "total_away_score", "epa", "air_yards",
    "qb_scramble",
    "drive_inside20",
    "pass_location",
    "qb_hit",
    "third_down_failed",
    "third_down_converted",
    # punt net distance (yards_gained is always 0 on punts in nflfastR)
    "kick_distance",
    "return_yards",
    "return_touchdown",
    "touchback",
    "punt_in_endzone",
]


def load_team_history(
    pbp_path: str | Path,
    *,
    teams: Sequence[str],
    season: int,
    weeks: tuple[int, int],
) -> dict:
    path = Path(pbp_path)
    if not path.exists():
        return {"status": "PBP_MISSING", "df": None, "evidence": {}}
    import pyarrow.parquet as pq
    available = set(pq.ParquetFile(path).schema_arrow.names)
    use = [c for c in COLS if c in available]
    df = pd.read_parquet(path, columns=use)
    w0, w1 = weeks
    # Games involving either team, weeks in range, season match
    invol = df["home_team"].isin(teams) | df["away_team"].isin(teams)
    mask = invol & (df["season"] == season) & (df["week"] >= w0) & (df["week"] <= w1)
    games = df.loc[mask].copy()
    # Offense rows: posteam in teams (team-only offense catalog)
    off = games[games["posteam"].isin(teams)].copy()
    if off.empty:
        return {"status": "EMPTY_TEAM_HISTORY", "df": off, "evidence": {"n_games": 0, "n_plays": 0}}
    # Guard: no future weeks
    if off["week"].max() > w1 or off["week"].min() < w0:
        return {"status": "WEEK_FILTER_FAILED", "df": off, "evidence": {}}
    return {
        "status": "OK",
        "df": off.reset_index(drop=True),
        "games_df": games.reset_index(drop=True),
        "evidence": {
            "n_games": int(games["game_id"].nunique()),
            "n_plays": int(len(off)),
            "teams": list(teams),
            "weeks": [w0, w1],
            "season": season,
            "source": str(path),
        },
    }


def load_involvement_plays(pbp_path, *, teams, season, weeks):
    """All plays from games involving teams (includes opponent offense vs our defense)."""
    import pyarrow.parquet as pq
    from pathlib import Path
    path = Path(pbp_path)
    available = set(pq.ParquetFile(path).schema_arrow.names)
    use = [c for c in COLS if c in available]
    df = __import__("pandas").read_parquet(path, columns=use)
    w0, w1 = weeks
    invol = df["home_team"].isin(teams) | df["away_team"].isin(teams)
    mask = invol & (df["season"] == season) & (df["week"] >= w0) & (df["week"] <= w1)
    return df.loc[mask].reset_index(drop=True)
