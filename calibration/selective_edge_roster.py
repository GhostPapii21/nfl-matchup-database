"""Phase 4 live: join a sourced roster + play-by-play usage onto live legs (stacked on PR #40, refs NFL-75).

For every leg (week, game_id, player) this adds
    gsis, position, team, roster_week, roster_match (gsis_preset | name | ambiguous | no_match),
    season_car, season_team_car, season_carry_share, season_games,
    roster_source, roster_pulled_utc, pbp_source, pbp_pulled_utc
Rules (no guessing; missing data stays unknown, never zero):
  * Only the two teams in the game_id (nflverse format 2026_WW_AWAY_HOME) are searched.
  * Roster row = the player's latest nflverse weekly-roster row with week <= leg week.
  * Names match after lower-casing, dropping punctuation and suffixes (Jr, Sr, II, III, IV, V); full_name or
    football_name + last_name. Zero or more than one distinct gsis -> gsis/position unknown.
  * Season carry share = player's carries / team carries over REG games in weeks < leg week in which he had a carry
    or a target (kneels and two-point tries excluded, same definitions as selective_edge.player_game_table).
  * A roster or pbp without a pull time is refused.
The frozen classifier then labels an unmatched rushing leg INSUFFICIENT EVIDENCE (position_unknown). The N1 gate
itself still reads carry_n_prior / carry_n60 from selective_edge.attach_context (last 4 prior games). Research only."""
from __future__ import annotations

import re

import numpy as np
import pandas as pd

from calibration import selective_edge as se

SUFFIX = re.compile(r"\b(jr|sr|ii|iii|iv|v)\b")


class RosterJoinError(RuntimeError):
    pass


def norm_name(s) -> str:
    if s is None or (isinstance(s, float) and np.isnan(s)):
        return ""
    s = re.sub(r"[.'`’,]", "", str(s).lower()).replace("-", " ")
    s = SUFFIX.sub(" ", s)
    return " ".join(s.split())


def game_teams(game_id: str) -> tuple[str, ...]:
    parts = str(game_id).split("_")
    return tuple(parts[2:4]) if len(parts) >= 4 else ()


def _usage(pbp: pd.DataFrame) -> pd.DataFrame:
    return se.player_game_table(pbp)


def join_roster(legs: pd.DataFrame, roster: pd.DataFrame, pbp: pd.DataFrame, *, roster_source: str,
                roster_pulled_utc: str, pbp_source: str, pbp_pulled_utc: str) -> pd.DataFrame:
    for k, v in (("roster_source", roster_source), ("roster_pulled_utc", roster_pulled_utc),
                 ("pbp_source", pbp_source), ("pbp_pulled_utc", pbp_pulled_utc)):
        if v is None or str(v).strip() == "":
            raise RosterJoinError(f"{k} is required: every roster/usage figure needs a source and a pull time")
    need = {"team", "position", "full_name", "gsis_id", "week"}
    if not need <= set(roster.columns):
        raise RosterJoinError(f"roster lacks columns {sorted(need - set(roster.columns))}")
    R = roster.copy()
    R["k_full"] = R.full_name.map(norm_name)
    R["k_fb"] = (R.get("football_name", pd.Series("", index=R.index)).fillna("").astype(str) + " "
                 + R.get("last_name", pd.Series("", index=R.index)).fillna("").astype(str)).map(norm_name)
    t = _usage(pbp)
    out = legs.copy().reset_index(drop=True)
    cols = dict(gsis=[], position=[], team=[], roster_week=[], roster_match=[], season_car=[], season_team_car=[],
                season_carry_share=[], season_games=[])
    for _, r in out.iterrows():
        wk = int(r.week)
        teams = game_teams(r.game_id)
        cand = R[R.team.isin(teams) & (R.week <= wk)]
        preset = r.get("gsis")
        if preset is not None and not (isinstance(preset, float) and np.isnan(preset)) and str(preset).strip():
            hit, how = cand[cand.gsis_id == preset], "gsis_preset"
        else:
            k = norm_name(r.get("player"))
            hit = cand[(cand.k_full == k) | (cand.k_fb == k)] if k else cand.iloc[0:0]
            how = "name"
        ids = hit.gsis_id.dropna().unique()
        if len(ids) != 1:
            for c in ("gsis", "position", "team", "roster_week", "season_car", "season_team_car",
                      "season_carry_share", "season_games"):
                cols[c].append(np.nan)
            cols["roster_match"].append("ambiguous" if len(ids) > 1 else "no_match")
            continue
        row = hit[hit.gsis_id == ids[0]].sort_values("week").iloc[-1]
        g = ids[0]
        h = t[(t.gsis == g) & (t.week < wk)]
        played = h  # player_game_table has a row only for games with a carry or a target
        car, tcar = float(played.car.sum()), float(played.team_car.fillna(0).sum())
        cols["gsis"].append(g)
        cols["position"].append(str(row.position).strip().upper() if pd.notna(row.position) else np.nan)
        cols["team"].append(row.team)
        cols["roster_week"].append(int(row.week))
        cols["roster_match"].append(how)
        cols["season_car"].append(car if len(played) else np.nan)
        cols["season_team_car"].append(tcar if len(played) else np.nan)
        cols["season_carry_share"].append(car / tcar if len(played) and tcar > 0 else np.nan)
        cols["season_games"].append(int(played.game_id.nunique()) if len(played) else np.nan)
    for c, v in cols.items():
        out[c] = v
    out["roster_source"], out["roster_pulled_utc"] = roster_source, roster_pulled_utc
    out["pbp_source"], out["pbp_pulled_utc"] = pbp_source, pbp_pulled_utc
    return out
