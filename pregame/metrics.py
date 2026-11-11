"""Matchup metrics from play-by-play. Every number is a count or ratio of recorded plays; nothing is inferred.

Conventions (workflows/operational_specs/MASTER_PROMPT.md, phase 2): explosive pass = completion of 20+ yards,
explosive rush = run of 15+ yards. Scrambles count as QB rushing, not designed runs. Kneels and spikes are
excluded. Two-point tries are excluded. A missing value is None, never 0.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

EXPLOSIVE_PASS = 20
EXPLOSIVE_RUSH = 15
POS_GROUPS = ("WR", "TE", "RB")
# (key, label, higher value is better for the DEFENSE when it is the one allowing it?)  False = lower is better
RANKED = {
    "points_pg": False, "pass_yards_pg": False, "rush_yards_pg": False, "yards_per_carry": False, "rb_rush_yards_pg": False,
    "explosive_pass_pg": False, "explosive_rush_pg": False, "explosive_total_pg": False,
    "wr_rec_yards_pg": False, "te_rec_yards_pg": False, "rb_rec_yards_pg": False,
    "wr_receptions_pg": False, "te_receptions_pg": False, "rb_receptions_pg": False,
    "sack_rate": True, "pressure_rate": True, "third_down_rate": False, "red_zone_td_rate": False,
    "pass_epa_per_dropback": False, "rush_epa_per_carry": False, "takeaways_pg": True, "yards_per_pass_attempt": False,
}


def _num(s):
    return pd.to_numeric(s, errors="coerce").fillna(0.0)


def prepare(pbp: pd.DataFrame, rosters: pd.DataFrame, ftn: pd.DataFrame | None = None) -> pd.DataFrame:
    """Scrimmage plays with the flag columns every table below sums."""
    p = pbp[pbp.play_type.isin(["pass", "run"]) & pbp.down.notna()].copy()
    if "two_point_attempt" in p:
        p = p[_num(p.two_point_attempt) == 0]
    pos = (rosters.sort_values("week").drop_duplicates("gsis_id", keep="last").set_index("gsis_id").position
           .replace({"FB": "RB"}))
    p["rec_pos"] = p.receiver_player_id.map(pos)
    p["rush_pos"] = p.rusher_player_id.map(pos)
    yg = _num(p.yards_gained)
    sack = _num(p.sack) == 1
    scr = _num(p.qb_scramble) == 1
    p["dropback"] = (_num(p.qb_dropback) == 1).astype(float)
    p["att"] = ((_num(p.pass_attempt) == 1) & ~sack).astype(float)
    p["cmp"] = (_num(p.complete_pass) == 1).astype(float)
    p["pass_yds"] = np.where(p.cmp == 1, yg, 0.0)
    p["pass_td"] = (_num(p.pass_touchdown) == 1).astype(float)
    p["int"] = (_num(p.interception) == 1).astype(float)
    p["fum_lost"] = (_num(p.fumble_lost) == 1).astype(float)
    p["sack_f"] = sack.astype(float)
    p["qb_hit_f"] = (_num(p.qb_hit) == 1).astype(float)
    p["pressure"] = (sack | (_num(p.qb_hit) == 1)).astype(float)       # sacks + hits: a floor on true pressure
    p["scramble"] = scr.astype(float)
    p["scramble_yds"] = np.where(scr, yg, 0.0)
    p["air"] = np.where(p.att == 1, _num(p.air_yards), 0.0)
    p["deep_att"] = ((p.att == 1) & (_num(p.air_yards) >= 20)).astype(float)
    p["deep_cmp"] = ((p.cmp == 1) & (_num(p.air_yards) >= 20)).astype(float)
    p["xpl_pass"] = ((p.cmp == 1) & (yg >= EXPLOSIVE_PASS)).astype(float)
    carry = (_num(p.rush_attempt) == 1) & ~scr
    p["carry"] = carry.astype(float)
    p["rush_yds"] = np.where(carry, yg, 0.0)
    p["rush_td"] = (carry & (_num(p.rush_touchdown) == 1)).astype(float)
    p["xpl_rush"] = (((carry | scr)) & (yg >= EXPLOSIVE_RUSH)).astype(float)
    p["rb_carry"] = (carry & (p.rush_pos == "RB")).astype(float)
    p["rb_rush_yds"] = np.where(p.rb_carry == 1, yg, 0.0)
    p["qb_carry"] = (carry & (p.rush_pos == "QB")).astype(float)
    p["qb_rush_yds"] = np.where(p.qb_carry == 1, yg, 0.0) + p.scramble_yds
    tgt = (p.att == 1) & p.receiver_player_id.notna()
    p["tgt"] = tgt.astype(float)
    for g in POS_GROUPS:
        m = tgt & (p.rec_pos == g)
        p[f"{g}_tgt"] = m.astype(float)
        p[f"{g}_rec"] = (m & (p.cmp == 1)).astype(float)
        p[f"{g}_yds"] = np.where(m, p.pass_yds, 0.0)
        p[f"{g}_td"] = (m & (p.pass_td == 1)).astype(float)
        p[f"{g}_xpl"] = (m & (p.xpl_pass == 1)).astype(float)
    p["epa_db"] = np.where(p.dropback == 1, _num(p.epa), 0.0)
    p["epa_carry"] = np.where(carry, _num(p.epa), 0.0)
    p["third_att"] = (_num(p.third_down_converted) + _num(p.third_down_failed) > 0).astype(float)
    p["third_conv"] = (_num(p.third_down_converted) == 1).astype(float)
    neutral = (p.down <= 2) & (_num(p.score_differential).abs() <= 8) & (p.qtr <= 3)
    p["neutral"] = neutral.astype(float)
    p["neutral_pass"] = (neutral & (p.dropback == 1)).astype(float)
    p["play"] = 1.0
    p["blitz"] = np.nan
    p["play_action"] = np.nan
    if ftn is not None and len(ftn):
        f = ftn.rename(columns={"nflverse_game_id": "game_id", "nflverse_play_id": "play_id"})[["game_id", "play_id", "n_blitzers", "is_play_action"]]
        p = p.merge(f, on=["game_id", "play_id"], how="left")
        charted = p.n_blitzers.notna() & (p.dropback == 1)
        p["blitz"] = np.where(charted, (_num(p.n_blitzers) > 0).astype(float), np.nan)
        p["play_action"] = np.where(charted, _num(p.is_play_action), np.nan)
    p["db_charted"] = p.blitz.notna().astype(float)
    p["blitz_f"] = p.blitz.fillna(0.0)
    p["pa_f"] = p.play_action.fillna(0.0)
    p["blitz_sack"] = ((p.blitz == 1) & sack).astype(float)
    return p


SUMS = ["play", "dropback", "att", "cmp", "pass_yds", "pass_td", "int", "fum_lost", "sack_f", "qb_hit_f", "pressure", "scramble",
        "scramble_yds", "air", "deep_att", "deep_cmp", "xpl_pass", "carry", "rush_yds", "rush_td", "xpl_rush", "rb_carry",
        "rb_rush_yds", "qb_carry", "qb_rush_yds", "tgt", "epa_db", "epa_carry", "third_att", "third_conv", "neutral",
        "neutral_pass", "db_charted", "blitz_f", "pa_f", "blitz_sack",
        *[f"{g}_{k}" for g in POS_GROUPS for k in ("tgt", "rec", "yds", "td", "xpl")]]


def team_games(p: pd.DataFrame, games: pd.DataFrame, side: str) -> pd.DataFrame:
    """One row per team-game. side='defteam' = what the team ALLOWED; 'posteam' = what its offense produced."""
    t = p.groupby([side, "game_id"], as_index=False)[SUMS].sum().rename(columns={side: "team"})
    # red zone: drives that reached the 20, and how many ended in a touchdown
    d = p.groupby([side, "game_id", "fixed_drive"], as_index=False).agg(
        rz=("yardline_100", lambda s: float((s <= 20).any())), res=("fixed_drive_result", "first"))
    d["rz_td"] = ((d.rz == 1) & (d.res == "Touchdown")).astype(float)
    rz = d.groupby([side, "game_id"], as_index=False)[["rz", "rz_td"]].sum().rename(columns={side: "team", "rz": "rz_drives"})
    t = t.merge(rz, on=["team", "game_id"], how="left")
    g = games[["game_id", "week", "gameday", "home_team", "away_team", "home_score", "away_score"]]
    t = t.merge(g, on="game_id", how="left")
    is_home = t.team == t.home_team
    t["opp"] = np.where(is_home, t.away_team, t.home_team)
    own, other = np.where(is_home, t.home_score, t.away_score), np.where(is_home, t.away_score, t.home_score)
    t["points"] = other if side == "defteam" else own          # allowed for a defence, scored for an offence
    t["loc"] = np.where(is_home, "vs", "@")
    return t.sort_values(["team", "gameday", "game_id"])


def last_n(t: pd.DataFrame, n: int) -> pd.DataFrame:
    return t.groupby("team", group_keys=False).tail(n)


def _div(a, b):
    return float(a) / float(b) if b else None


def summarize(tn: pd.DataFrame) -> dict:
    """Totals over a team's window -> per-game and rate metrics."""
    s = tn[SUMS + ["rz_drives", "rz_td"]].sum()
    g = len(tn)
    pg = lambda v: _div(v, g)
    out = {
        "games": g, "weeks": [int(w) for w in tn.week], "points_pg": pg(tn.points.sum()),
        "plays_pg": pg(s.play), "pass_yards_pg": pg(s.pass_yds), "pass_att_pg": pg(s.att), "completions_pg": pg(s.cmp),
        "yards_per_pass_attempt": _div(s.pass_yds, s.att), "completion_rate": _div(s.cmp, s.att), "pass_td": int(s.pass_td),
        "interceptions": int(s.int), "fumbles_lost": int(s.fum_lost), "takeaways_pg": pg(s.int + s.fum_lost),
        "sacks": int(s.sack_f), "sack_rate": _div(s.sack_f, s.dropback), "qb_hits": int(s.qb_hit_f),
        "pressure_rate": _div(s.pressure, s.dropback), "avg_depth_of_target": _div(s.air, s.att),
        "deep_attempts_pg": pg(s.deep_att), "deep_completion_rate": _div(s.deep_cmp, s.deep_att),
        "rush_att_pg": pg(s.carry), "rush_yards_pg": pg(s.rush_yds), "yards_per_carry": _div(s.rush_yds, s.carry), "rush_td": int(s.rush_td),
        "rb_carries_pg": pg(s.rb_carry), "rb_rush_yards_pg": pg(s.rb_rush_yds), "rb_yards_per_carry": _div(s.rb_rush_yds, s.rb_carry),
        "qb_rush_yards_pg": pg(s.qb_rush_yds), "scrambles_pg": pg(s.scramble),
        "explosive_pass": int(s.xpl_pass), "explosive_rush": int(s.xpl_rush),
        "explosive_pass_pg": pg(s.xpl_pass), "explosive_rush_pg": pg(s.xpl_rush), "explosive_total_pg": pg(s.xpl_pass + s.xpl_rush),
        "third_down_rate": _div(s.third_conv, s.third_att), "red_zone_drives": int(s.rz_drives), "red_zone_td_rate": _div(s.rz_td, s.rz_drives),
        "pass_epa_per_dropback": _div(s.epa_db, s.dropback), "rush_epa_per_carry": _div(s.epa_carry, s.carry),
        "neutral_pass_rate": _div(s.neutral_pass, s.neutral),
        "blitz_rate": _div(s.blitz_f, s.db_charted), "play_action_rate": _div(s.pa_f, s.db_charted),
        "sack_rate_when_blitzing": _div(s.blitz_sack, s.blitz_f), "dropbacks_charted": int(s.db_charted),
    }
    for grp in POS_GROUPS:
        k = grp.lower()
        out.update({f"{k}_targets_pg": pg(s[f"{grp}_tgt"]), f"{k}_receptions_pg": pg(s[f"{grp}_rec"]), f"{k}_rec_yards_pg": pg(s[f"{grp}_yds"]),
                    f"{k}_rec_td": int(s[f"{grp}_td"]), f"{k}_yards_per_target": _div(s[f"{grp}_yds"], s[f"{grp}_tgt"]),
                    f"{k}_explosive": int(s[f"{grp}_xpl"]), f"{k}_target_share": _div(s[f"{grp}_tgt"], s.tgt)})
    return out


def game_log(tn: pd.DataFrame) -> list[dict]:
    """Per-game rows, oldest first: the trend table."""
    rows = []
    for r in tn.itertuples():
        rows.append({"week": int(r.week), "opp": f"{r.loc} {r.opp}", "points": None if pd.isna(r.points) else int(r.points),
                     "pass_yards": int(r.pass_yds), "rush_yards": int(r.rush_yds), "carries": int(r.carry),
                     "rb_rush_yards": int(r.rb_rush_yds), "sacks": int(r.sack_f),
                     "explosive_pass": int(r.xpl_pass), "explosive_rush": int(r.xpl_rush),
                     **{f"{g.lower()}_{lab}": int(getattr(r, f"{g}_{col}")) for g in POS_GROUPS
                        for lab, col in (("targets", "tgt"), ("receptions", "rec"), ("rec_yards", "yds"), ("rec_td", "td"))}})
    return rows


def league_table(t: pd.DataFrame, n: int) -> pd.DataFrame:
    tn = last_n(t, n)
    return pd.DataFrame({team: summarize(x) for team, x in tn.groupby("team")}).T


def ranks(league: pd.DataFrame, team: str, *, defense: bool) -> dict:
    """Rank 1 = best at that job. For a defence 'best' is allowing the least (or pressuring the most);
    for an offence it is producing the most (or allowing the least pressure)."""
    out = {}
    for key, higher_good_for_defense in RANKED.items():
        if key not in league:
            continue
        col = pd.to_numeric(league[key], errors="coerce")
        if col.isna().all() or pd.isna(col.get(team)):
            continue
        best_is_high = higher_good_for_defense if defense else not higher_good_for_defense
        out[key] = {"rank": int(col.rank(ascending=not best_is_high, method="min")[team]), "of": int(col.notna().sum()),
                    "league_avg": float(col.mean())}
    return out


def top_lines_allowed(p: pd.DataFrame, team: str, game_ids: list[str], games: pd.DataFrame) -> list[dict]:
    """Best receiving and rushing line allowed in each game: 'who hurt this defence'."""
    d = p[(p.defteam == team) & p.game_id.isin(game_ids)]
    wk = games.set_index("game_id").week
    out = []
    for gid in game_ids:
        x = d[d.game_id == gid]
        row = {"week": int(wk[gid]), "opp": x.posteam.iloc[0] if len(x) else None}
        r = x[x.tgt == 1].groupby(["receiver_player_name", "rec_pos"], dropna=False).agg(t=("tgt", "sum"), c=("cmp", "sum"), y=("pass_yds", "sum"), td=("pass_td", "sum"))
        if len(r):
            b = r.sort_values("y").iloc[-1]; nm, ps = b.name
            row["top_receiver"] = {"player": nm, "pos": None if pd.isna(ps) else ps, "targets": int(b.t), "receptions": int(b.c), "yards": int(b.y), "td": int(b.td)}
        r = x[x.carry == 1].groupby(["rusher_player_name", "rush_pos"], dropna=False).agg(c=("carry", "sum"), y=("rush_yds", "sum"), td=("rush_td", "sum"))
        if len(r):
            b = r.sort_values("y").iloc[-1]; nm, ps = b.name
            row["top_rusher"] = {"player": nm, "pos": None if pd.isna(ps) else ps, "carries": int(b.c), "yards": int(b.y), "td": int(b.td)}
        out.append(row)
    return out


def run_direction(p: pd.DataFrame, team: str, game_ids: list[str], side: str) -> list[dict]:
    d = p[(p[side] == team) & p.game_id.isin(game_ids) & (p.carry == 1) & p.run_location.notna()].copy()
    d["where"] = np.where(d.run_location == "middle", "middle", d.run_location.astype(str) + " " + d.run_gap.fillna("").astype(str))
    r = d.groupby("where").agg(carries=("carry", "sum"), yards=("rush_yds", "sum"), explosive=("xpl_rush", "sum"))
    r["ypc"] = r.yards / r.carries
    return [{"direction": k.strip(), "carries": int(v.carries), "yards": int(v.yards), "ypc": round(float(v.ypc), 2), "explosive": int(v.explosive)}
            for k, v in r.sort_values("carries", ascending=False).iterrows()]


def offense_players(p: pd.DataFrame, team: str, game_ids: list[str], games: pd.DataFrame) -> dict:
    """Usage and production for the team's skill players over the window, with per-game logs."""
    d = p[(p.posteam == team) & p.game_id.isin(game_ids)]
    wk = games.set_index("game_id").week
    order = sorted(game_ids, key=lambda g: wk[g])
    team_tgt, team_carry, team_air = d.tgt.sum(), d.carry.sum(), d.air[d.tgt == 1].sum()
    rz = d.yardline_100 <= 20
    rec = d[d.tgt == 1].groupby(["receiver_player_id", "receiver_player_name", "rec_pos"], dropna=False)
    recs = []
    for (pid, nm, ps), x in rec:
        by = x.groupby("game_id").agg(t=("tgt", "sum"), c=("cmp", "sum"), y=("pass_yds", "sum"))
        log = [{"week": int(wk[g]), "targets": int(by.t.get(g, 0)), "receptions": int(by.c.get(g, 0)), "yards": int(by.y.get(g, 0))} for g in order if g in by.index]
        recs.append({"player": nm, "player_id": pid, "pos": None if pd.isna(ps) else ps, "games": len(log), "targets": int(x.tgt.sum()), "receptions": int(x.cmp.sum()),
                     "yards": int(x.pass_yds.sum()), "td": int(x.pass_td.sum()), "target_share": _div(x.tgt.sum(), team_tgt),
                     "air_yards_share": _div(x.air.sum(), team_air), "avg_depth_of_target": _div(x.air.sum(), x.tgt.sum()),
                     "yards_per_target": _div(x.pass_yds.sum(), x.tgt.sum()), "explosive": int(x.xpl_pass.sum()),
                     "red_zone_targets": int(x.tgt[rz.loc[x.index]].sum()), "log": log})
    rush = d[d.carry == 1].groupby(["rusher_player_id", "rusher_player_name", "rush_pos"], dropna=False)
    rushers = []
    for (pid, nm, ps), x in rush:
        by = x.groupby("game_id").agg(c=("carry", "sum"), y=("rush_yds", "sum"))
        log = [{"week": int(wk[g]), "carries": int(by.c.get(g, 0)), "yards": int(by.y.get(g, 0))} for g in order if g in by.index]
        rushers.append({"player": nm, "player_id": pid, "pos": None if pd.isna(ps) else ps, "games": len(log), "carries": int(x.carry.sum()), "yards": int(x.rush_yds.sum()),
                        "td": int(x.rush_td.sum()), "carry_share": _div(x.carry.sum(), team_carry), "yards_per_carry": _div(x.rush_yds.sum(), x.carry.sum()),
                        "explosive": int(((x.rush_yds >= EXPLOSIVE_RUSH)).sum()), "red_zone_carries": int(x.carry[rz.loc[x.index]].sum()), "log": log})
    qb = d[d.dropback == 1].groupby(["passer_player_id", "passer_player_name"], dropna=True)
    qbs = []
    for (pid, nm), x in qb:
        by = x.groupby("game_id").agg(a=("att", "sum"), c=("cmp", "sum"), y=("pass_yds", "sum"), td=("pass_td", "sum"), i=("int", "sum"), s=("sack_f", "sum"))
        log = [{"week": int(wk[g]), "att": int(by.a[g]), "cmp": int(by.c[g]), "yards": int(by.y[g]), "td": int(by.td[g]), "int": int(by.i[g]), "sacks": int(by.s[g])} for g in order if g in by.index]
        qbs.append({"player": nm, "player_id": pid, "games": len(log), "attempts": int(x.att.sum()), "completions": int(x.cmp.sum()), "yards": int(x.pass_yds.sum()),
                    "td": int(x.pass_td.sum()), "int": int(x.int.sum()), "sacks": int(x.sack_f.sum()), "yards_per_attempt": _div(x.pass_yds.sum(), x.att.sum()),
                    "avg_depth_of_target": _div(x.air.sum(), x.att.sum()), "epa_per_dropback": _div(x.epa_db.sum(), x.dropback.sum()),
                    "pressure_rate_faced": _div(x.pressure.sum(), x.dropback.sum()), "log": log})
    key = lambda k: (lambda r: -r[k])
    return {"receivers": sorted(recs, key=key("targets"))[:9], "rushers": sorted(rushers, key=key("carries"))[:5],
            "quarterbacks": sorted(qbs, key=key("attempts"))[:2]}
