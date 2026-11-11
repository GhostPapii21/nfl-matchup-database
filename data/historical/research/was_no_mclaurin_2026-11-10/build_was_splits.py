#!/usr/bin/env python3
"""WAS 2026 W1-9 McLaurin/JCM research pack. Research only, no picks."""
from __future__ import annotations
import json, math
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUT = Path("/workspace/was_no_mclaurin_2026-11-10")
SAVANT = Path("/workspace/nfl_savant_nyg_was_2026-11-10")
STATS_PATH = Path("/tmp/nflverse_2026/stats_player_week_2026.parquet")
SNAPS_PATH = Path("/tmp/nflverse_2026/snap_counts_2026.parquet")
PBP_PATH = SAVANT / "raw" / "pbp-2026.csv"
PROPS_PATH = Path("/workspace/odds_freeze/2026_10_WAS_NYG/baseline_20261110_0902ET/props.csv")
NYG_DEF_PATH = SAVANT / "team_nyg_def.csv"
SAVANT_WEEKLY_PATH = SAVANT / "was_receivers_weekly.csv"

TEAM, SEASON = "WAS", 2026
GAMES_META = [
    dict(week=1, date="2026-09-13", weekday="SUN", opp="PHI", home=False, result="L", us=22, them=24, game_id="2026_01_WAS_PHI"),
    dict(week=2, date="2026-09-20", weekday="SUN", opp="DAL", home=False, result="L", us=20, them=37, game_id="2026_02_WAS_DAL"),
    dict(week=3, date="2026-09-27", weekday="SUN", opp="SEA", home=True, result="W", us=33, them=31, game_id="2026_03_SEA_WAS"),
    dict(week=4, date="2026-10-04", weekday="SUN", opp="IND", home=True, result="L", us=13, them=30, game_id="2026_04_IND_WAS"),
    dict(week=5, date="2026-10-11", weekday="SUN", opp="NYG", home=True, result="T", us=27, them=27, game_id="2026_05_NYG_WAS"),
    dict(week=6, date="2026-10-19", weekday="MON", opp="SF", home=False, result="L", us=17, them=23, game_id="2026_06_WAS_SF"),
    dict(week=7, date=None, weekday=None, opp="BYE", home=None, result="BYE", us=None, them=None, game_id=None),
    dict(week=8, date="2026-11-01", weekday="SUN", opp="PHI", home=True, result="W", us=27, them=10, game_id="2026_08_PHI_WAS"),
    dict(week=9, date="2026-11-08", weekday="SUN", opp="LAR", home=True, result="L", us=13, them=20, game_id="2026_09_LA_WAS"),
]
WITH_WEEKS = [1, 2, 3, 5]
LIMITED_WEEKS = [6]
WITHOUT_WEEKS = [4, 8, 9]
DANIELS_STARTED = [1, 2, 5, 6, 8, 9]
DANIELS_FULL = [1, 5, 6, 8, 9]
JCM_WEEKS = [1, 2, 3, 4, 5]
NO_JCM_WEEKS = [6, 8, 9]
SKILL_POS = {"QB", "RB", "WR", "TE", "FB"}
FOCUS_RECEIVERS = [
    "Terry McLaurin","Stefon Diggs","Antonio Williams","Chig Okonkwo","Treylon Burks",
    "Dyami Brown","Van Jefferson","Jaylin Lane","Luke McCaffrey","Jaden Bradley",
    "John Bates","Ben Sinnott","Colson Yankoff","Rachaad White","Austin Ekeler",
    "Jacory Croskey-Merritt","Jeremy McNichols","Kaytron Allen",
]

def status_from_snaps(snaps):
    if snaps is None or (isinstance(snaps, float) and math.isnan(snaps)):
        return "DNP"
    if snaps <= 0:
        return "dressed_0_off_snaps"
    return "played"

def load():
    st = pd.read_parquet(STATS_PATH)
    stats = st[(st.team == TEAM) & (st.season == SEASON) & (st.season_type == "REG")].copy()
    sn = pd.read_parquet(SNAPS_PATH)
    snaps = sn[(sn.team == TEAM) & (sn.season == SEASON) & (sn.game_type == "REG")].copy()
    pbp = pd.read_csv(PBP_PATH, usecols=["week","posteam","qb_kneel","rusher_player_name","rushing_yards","desc"], low_memory=False)
    k = pbp[(pbp.posteam == "WAS") & (pbp.qb_kneel == 1)]
    kneels = {}
    for _, r in k.iterrows():
        kneels.setdefault(int(r.week), []).append(dict(rusher=r.rusher_player_name, yards=float(r.rushing_yards), desc=r.desc))
    props = pd.read_csv(PROPS_PATH)
    return st, stats, snaps, kneels, props

def kneel_for(kneels, week, display_name):
    if week not in kneels:
        return 0, 0.0
    last = display_name.split()[-1]
    n, y = 0, 0.0
    for item in kneels[week]:
        rusher_last = str(item["rusher"]).split(".")[-1]
        if rusher_last.lower() == last.lower():
            n += 1
            y += item["yards"]
    return n, y


def build_indices(stats, snaps, kneels):
    skill_snaps = snaps[snaps.position.isin(SKILL_POS)].copy()
    snap_idx = {}
    for _, r in skill_snaps.iterrows():
        snap_idx[(int(r.week), r.player)] = dict(
            snaps=float(r.offense_snaps) if pd.notna(r.offense_snaps) else 0.0,
            snap_pct=float(r.offense_pct) if pd.notna(r.offense_pct) else 0.0,
            position=r.position,
        )
    team_off_snaps = snaps[snaps.offense_pct >= 0.99].groupby("week")["offense_snaps"].max().to_dict()
    team_targets = stats.groupby("week")["targets"].sum().to_dict()
    team_carries = stats.groupby("week")["carries"].sum().to_dict()
    team_rush_yds = stats.groupby("week")["rushing_yards"].sum().to_dict()
    kneel_att = {w: len(v) for w, v in kneels.items()}
    kneel_yds = {w: sum(x["yards"] for x in v) for w, v in kneels.items()}
    return skill_snaps, snap_idx, team_off_snaps, team_targets, team_carries, team_rush_yds, kneel_att, kneel_yds

def player_status(snap_idx, week, name):
    rec = snap_idx.get((week, name))
    if rec is None:
        return dict(status="DNP", snaps=0, snap_pct=0.0)
    return dict(status=status_from_snaps(rec["snaps"]), snaps=rec["snaps"], snap_pct=rec["snap_pct"])

def qb_info(week, skill_snaps, stats):
    qb_snaps = skill_snaps[(skill_snaps.week == week) & (skill_snaps.position == "QB")].sort_values("offense_snaps", ascending=False)
    qb_pass = stats[(stats.week == week) & (stats.position == "QB") & (stats.attempts.fillna(0) > 0)]
    rows = []
    for _, r in qb_snaps.iterrows():
        pr = qb_pass[qb_pass.player_display_name == r.player]
        rush = stats[(stats.week == week) & (stats.player_display_name == r.player)]
        rows.append(dict(
            name=r.player,
            snaps=int(r.offense_snaps),
            snap_pct=float(r.offense_pct),
            cmp=int(pr.completions.sum()) if len(pr) else 0,
            att=int(pr.attempts.sum()) if len(pr) else 0,
            pass_yds=int(pr.passing_yards.sum()) if len(pr) else 0,
            pass_td=int(pr.passing_tds.sum()) if len(pr) else 0,
            ints=int(pr.passing_interceptions.sum()) if len(pr) else 0,
            rush_att=int(rush.carries.sum()) if len(rush) else 0,
            rush_yds=int(rush.rushing_yards.sum()) if len(rush) else 0,
            rush_td=int(rush.rushing_tds.sum()) if len(rush) else 0,
        ))
    starter = rows[0]["name"] if rows else None
    note = None
    if week == 2:
        note = "Split QB: Daniels 39 snaps (55%), Mariota 32 snaps (45%). Daniels listed starter by snap lead."
    elif week == 3:
        note = "Daniels DNP. Mariota played 100% of offensive snaps."
    elif week == 4:
        note = "Daniels DNP. Kaliakmanis 54 snaps (84%), Mariota 10 snaps (16%)."
    elif week == 6:
        note = "Daniels 100% snaps. McLaurin limited to 7 snaps (10%)."
    return starter, rows, note

def bucket_for(week):
    if week in WITH_WEEKS:
        return "with_mclaurin"
    if week in LIMITED_WEEKS:
        return "mclaurin_limited"
    if week in WITHOUT_WEEKS:
        return "without_mclaurin"
    return "other"

def build_games(stats, skill_snaps, snap_idx, team_targets, team_carries, team_rush_yds, team_off_snaps, kneel_att, kneel_yds):
    rows = []
    for g in GAMES_META:
        w = g["week"]
        row = dict(season=SEASON, week=w, date=g["date"], weekday=g["weekday"], opponent=g["opp"],
                   home=g["home"], result=g["result"], score_was=g["us"], score_opp=g["them"], game_id=g["game_id"])
        if g["opp"] == "BYE":
            row.update(mclaurin_status="BYE", diggs_status="BYE", lane_status="BYE", jcm_status="BYE",
                       daniels_status="BYE", qb_starter=None, qb_note="Bye week", mclaurin_bucket="BYE")
            rows.append(row)
            continue
        def flags(name, prefix):
            s = player_status(snap_idx, w, name)
            return {f"{prefix}_status": s["status"], f"{prefix}_snaps": s["snaps"], f"{prefix}_snap_pct": round(s["snap_pct"]*100, 1)}
        row.update(flags("Terry McLaurin","mclaurin"))
        row.update(flags("Stefon Diggs","diggs"))
        row.update(flags("Jaylin Lane","lane"))
        row.update(flags("Jacory Croskey-Merritt","jcm"))
        row.update(flags("Jayden Daniels","daniels"))
        starter, qb_rows, qb_note = qb_info(w, skill_snaps, stats)
        qb_str = "; ".join(
            f"{q['name']} {q['snaps']} snaps ({q['snap_pct']*100:.0f}%) {q['cmp']}/{q['att']} {q['pass_yds']} yds {q['pass_td']} TD"
            + (f", {q['rush_att']} rush {q['rush_yds']} yds {q['rush_td']} TD" if q["rush_att"] else "")
            for q in qb_rows if q["snaps"] > 0
        )
        b = bucket_for(w)
        row.update(
            qb_starter=starter, qb_detail=qb_str, qb_note=qb_note, mclaurin_bucket=b,
            diggs_played_without_mclaurin=int(row["diggs_status"]=="played" and b=="without_mclaurin"),
            daniels_started=int(w in DANIELS_STARTED),
            team_targets=int(team_targets.get(w, 0)),
            team_carries_official=int(team_carries.get(w, 0)),
            team_rush_yds_official=int(team_rush_yds.get(w, 0)),
            kneels_att=(kneel_att.get(w) if w != 9 else None) if w != 9 else None,
            kneels_yds=(kneel_yds.get(w) if w != 9 else None) if w != 9 else None,
            team_off_snaps=int(team_off_snaps.get(w, 0)),
        )
        if w != 9:
            row["kneels_att"] = kneel_att.get(w, 0)
            row["kneels_yds"] = kneel_yds.get(w, 0)
        rows.append(row)
    return pd.DataFrame(rows)


def build_player_games(stats, skill_snaps, snap_idx, games_df, team_targets, team_carries, kneels, kneel_att):
    rec_gb, rush_gb = [], []
    rb_names = set(stats[stats.position=="RB"].player_display_name.unique()) | {
        "Rachaad White","Austin Ekeler","Jacory Croskey-Merritt","Jeremy McNichols","Kaytron Allen","Craig Reynolds"
    }
    for g in GAMES_META:
        w = g["week"]
        if g["opp"] == "BYE":
            continue
        week_stats = stats[stats.week == w]
        names = set(skill_snaps[skill_snaps.week==w].player) | set(week_stats[week_stats.position.isin(list(SKILL_POS))].player_display_name) | set(FOCUS_RECEIVERS)
        bucket = games_df[games_df.week==w].mclaurin_bucket.iloc[0]
        starter = games_df[games_df.week==w].qb_starter.iloc[0]
        for name in sorted(names):
            strow = week_stats[week_stats.player_display_name == name]
            recs = snap_idx.get((w, name))
            pos = strow.position.iloc[0] if len(strow) else (recs["position"] if recs else None)
            if recs:
                snaps_n, snap_pct = recs["snaps"], recs["snap_pct"]
                status = status_from_snaps(snaps_n)
            else:
                snaps_n, snap_pct, status = 0, 0.0, "DNP"
            if pos not in SKILL_POS and name not in FOCUS_RECEIVERS:
                continue
            tgt = int(strow.targets.sum()) if len(strow) else 0
            recn = int(strow.receptions.sum()) if len(strow) else 0
            yds = int(strow.receiving_yards.sum()) if len(strow) else 0
            td = int(strow.receiving_tds.sum()) if len(strow) else 0
            air = float(strow.receiving_air_yards.sum()) if len(strow) else 0.0
            car = int(strow.carries.sum()) if len(strow) else 0
            if pos == "QB":
                if car or name in ("Jayden Daniels","Marcus Mariota","Athan Kaliakmanis"):
                    k_n, k_y = kneel_for(kneels, w, name)
                    official_yds = int(strow.rushing_yards.sum()) if len(strow) else 0
                    official_td = int(strow.rushing_tds.sum()) if len(strow) else 0
                    rush_gb.append(dict(
                        season=SEASON, week=w, date=g["date"], opponent=g["opp"], player=name, position="QB",
                        status=status, off_snaps=snaps_n, off_snap_pct=round(snap_pct*100,1),
                        official_carries=car, official_rush_yards=official_yds, official_rush_td=official_td,
                        kneels=(k_n if w!=9 else None), kneel_yards=(k_y if w!=9 else None),
                        carries_ex_kneel=(car-k_n if w!=9 else None),
                        rush_yards_ex_kneel=(official_yds-k_y if w!=9 else None),
                        team_carries_official=int(team_carries.get(w,0)),
                        team_carries_ex_kneel=(int(team_carries.get(w,0)-kneel_att.get(w,0)) if w!=9 else None),
                        carry_share_official=(car/team_carries[w] if team_carries.get(w) else None),
                        ypc_official=(official_yds/car if car else None),
                        mclaurin_bucket=bucket, jcm_in=int(w in JCM_WEEKS),
                        source="nflverse official weekly (kneels from Savant pbp weeks 1-8 only)",
                    ))
                continue
            if status != "DNP" or tgt > 0 or name in FOCUS_RECEIVERS:
                played = status != "DNP"
                rec_gb.append(dict(
                    season=SEASON, week=w, date=g["date"], opponent=g["opp"], player=name, position=pos,
                    status=status, off_snaps=snaps_n, off_snap_pct=round(snap_pct*100,1),
                    route_share="unavailable_public_gap",
                    targets=(tgt if played or tgt else None),
                    receptions=(recn if played or recn else None),
                    rec_yards=(yds if played or yds else None),
                    rec_td=(td if played or td else None),
                    air_yards=(air if tgt or played else None),
                    adot=(round(air/tgt,2) if tgt else None),
                    target_share=(round(tgt/team_targets[w],4) if played and team_targets.get(w) else None),
                    team_targets=int(team_targets.get(w,0)),
                    mclaurin_bucket=bucket,
                    daniels_started=int(w in DANIELS_STARTED),
                    daniels_full_snaps=int(w in DANIELS_FULL),
                    qb_starter=starter,
                    source="nflverse official weekly + nflverse snap_counts",
                ))
            if (pos=="RB" or car>0) and name in rb_names:
                official_yds = int(strow.rushing_yards.sum()) if len(strow) else 0
                official_td = int(strow.rushing_tds.sum()) if len(strow) else 0
                played = status != "DNP"
                share = (car/team_carries[w] if played and car and team_carries.get(w) else (0.0 if played else None))
                if not played:
                    flag = "DNP"
                elif not car:
                    flag = "no_carries"
                elif share is not None and share >= 0.60:
                    flag = "clears_60pct_team_carries"
                else:
                    flag = "do_not_play_under_60pct_team_carries"
                rush_gb.append(dict(
                    season=SEASON, week=w, date=g["date"], opponent=g["opp"], player=name, position=pos or "RB",
                    status=status, off_snaps=snaps_n, off_snap_pct=round(snap_pct*100,1),
                    official_carries=(car if played or car else None),
                    official_rush_yards=(official_yds if played or car else None),
                    official_rush_td=(official_td if played or car else None),
                    targets=(tgt if played or tgt else None),
                    receptions=(recn if played else None),
                    rec_yards=(yds if played else None),
                    kneels=(0 if w!=9 else None), kneel_yards=(0.0 if w!=9 else None),
                    carries_ex_kneel=(car if played and w!=9 else (None if w==9 else (0 if played else None))),
                    rush_yards_ex_kneel=(official_yds if played and w!=9 else (None if w==9 else (0 if played else None))),
                    team_carries_official=int(team_carries.get(w,0)),
                    team_carries_ex_kneel=(int(team_carries.get(w,0)-kneel_att.get(w,0)) if w!=9 else None),
                    carry_share_official=share,
                    carry_share_ex_kneel=(car/(team_carries[w]-kneel_att.get(w,0)) if played and w!=9 and (team_carries.get(w,0)-kneel_att.get(w,0)) else None),
                    ypc_official=(official_yds/car if car else None),
                    mclaurin_bucket=bucket, jcm_in=int(w in JCM_WEEKS),
                    depth_usage_flag=flag,
                    source="nflverse official weekly (kneels from Savant pbp weeks 1-8 only)",
                ))
    rec_df = pd.DataFrame(rec_gb)
    rec_df = rec_df[rec_df.position.isin(["WR","TE","RB","FB"]) | rec_df.player.isin(FOCUS_RECEIVERS)]
    return rec_df, pd.DataFrame(rush_gb)


def split_row(player, pos, weeks, label, rec_df, require_daniels=False, require_diggs=False, exact_weeks=None):
    wks = list(weeks if exact_weeks is None else exact_weeks)
    if require_daniels:
        wks = [w for w in wks if w in DANIELS_STARTED]
    if require_diggs:
        dig = set(rec_df[(rec_df.player=="Stefon Diggs") & (rec_df.status=="played")].week)
        wks = [w for w in wks if w in dig]
    sub = rec_df[(rec_df.player==player) & (rec_df.week.isin(wks)) & (rec_df.status=="played")]
    n = len(sub)
    empty = dict(player=player, position=pos, split=label, games=0, weeks="", tgt_pg=None, rec_pg=None,
                 yds_pg=None, td_pg=None, target_share=None, target_share_unweighted_mean=None, adot=None,
                 snap_pct=None, games_4plus_rec=None, rec_list="", tgt_list="", yds_list="",
                 total_targets=0, total_receptions=0, total_yards=0, total_td=0)
    if n == 0:
        return empty
    tgt, recn, yds, td, air = sub.targets.fillna(0), sub.receptions.fillna(0), sub.rec_yards.fillna(0), sub.rec_td.fillna(0), sub.air_yards.fillna(0)
    tot_tgt = tgt.sum()
    return dict(
        player=player, position=pos, split=label, games=n,
        weeks=",".join(str(int(x)) for x in sorted(sub.week)),
        tgt_pg=round(float(tgt.mean()),2), rec_pg=round(float(recn.mean()),2),
        yds_pg=round(float(yds.mean()),2), td_pg=round(float(td.mean()),2),
        target_share=round(float(tot_tgt/sub.team_targets.sum()),4) if sub.team_targets.sum() else None,
        target_share_unweighted_mean=round(float(sub.target_share.mean()),4) if sub.target_share.notna().any() else None,
        adot=round(float(air.sum()/tot_tgt),2) if tot_tgt else None,
        snap_pct=round(float(sub.off_snap_pct.mean()),1),
        games_4plus_rec=int((recn>=4).sum()),
        rec_list="|".join(str(int(x)) for x in recn),
        tgt_list="|".join(str(int(x)) for x in tgt),
        yds_list="|".join(str(int(x)) for x in yds),
        total_targets=int(tot_tgt), total_receptions=int(recn.sum()),
        total_yards=int(yds.sum()), total_td=int(td.sum()),
    )

SPLIT_PLAYERS = [
    ("Terry McLaurin","WR"),("Stefon Diggs","WR"),("Antonio Williams","WR"),("Chig Okonkwo","TE"),
    ("Treylon Burks","WR"),("Dyami Brown","WR"),("Van Jefferson","WR"),("Jaylin Lane","WR"),
    ("Luke McCaffrey","WR"),("Jaden Bradley","WR"),("John Bates","TE"),("Ben Sinnott","TE"),
    ("Colson Yankoff","TE"),("Rachaad White","RB"),("Austin Ekeler","RB"),
    ("Jacory Croskey-Merritt","RB"),("Jeremy McNichols","RB"),
]
SPLIT_DEFS = [
    (WITH_WEEKS, "with_mclaurin_substantial_W1_2_3_5", False, False),
    (LIMITED_WEEKS, "mclaurin_limited_W6_7snaps", False, False),
    (WITHOUT_WEEKS, "without_mclaurin_W4_8_9", False, False),
    (WITHOUT_WEEKS, "without_mclaurin_AND_diggs_played_W4_8_9", False, True),
    (WITH_WEEKS, "daniels_started_with_mclaurin_substantial_W1_2_5", True, False),
    ([1,5], "daniels_100pct_with_mclaurin_substantial_W1_5", False, False),
    (LIMITED_WEEKS, "daniels_started_mclaurin_limited_W6", True, False),
    (WITHOUT_WEEKS, "daniels_started_without_mclaurin_W8_9", True, False),
    (WITH_WEEKS, "daniels_started_with_mclaurin_AND_diggs_played", True, True),
    (WITHOUT_WEEKS, "daniels_started_without_mclaurin_AND_diggs_played_W8_9", True, True),
]

def build_splits(rec_df):
    rows = []
    for player, pos in SPLIT_PLAYERS:
        for weeks, label, req_d, req_dig in SPLIT_DEFS:
            rows.append(split_row(player, pos, weeks, label, rec_df, req_d, req_dig))
    return pd.DataFrame(rows)

def build_hit_rates(rec_df, props):
    players = ["Antonio Williams","Stefon Diggs","Chig Okonkwo","Van Jefferson","Rachaad White","Austin Ekeler"]
    cons = props[(props.book=="CONSENSUS") & (props.market=="player_receptions") & (props.side=="Over")]
    line_map = {r.player: dict(line=float(r.point), price=int(r.price), n_books=r.n_books) for _, r in cons[cons.player.isin(players)].iterrows()}
    cons_yds = props[(props.book=="CONSENSUS") & (props.market=="player_reception_yds") & (props.side=="Over")]
    yds_map = {r.player: dict(line=float(r.point), price=int(r.price), n_books=r.n_books) for _, r in cons_yds[cons_yds.player.isin(players)].iterrows()}
    hit_splits = [
        (list(range(1,10)), "all_games_played"),
        (WITH_WEEKS, "with_mclaurin_substantial_W1_2_3_5"),
        (LIMITED_WEEKS, "mclaurin_limited_W6"),
        (WITHOUT_WEEKS, "without_mclaurin_W4_8_9"),
        ([1,2,5,6,8,9], "daniels_started_any"),
        ([1,5], "daniels_100pct_with_mclaurin_substantial_W1_5"),
        ([8,9], "daniels_started_without_mclaurin_W8_9"),
    ]
    rows = []
    for p in players:
        for weeks, label in hit_splits:
            sub = rec_df[(rec_df.player==p) & (rec_df.week.isin(weeks)) & (rec_df.status=="played")]
            line = line_map.get(p, {}).get("line")
            recs = list(sub.receptions.fillna(0).astype(int))
            yds = list(sub.rec_yards.fillna(0).astype(int))
            yline = yds_map.get(p, {}).get("line")
            over = int(sum(r > line for r in recs)) if line is not None and recs else (None if line is None else 0)
            y_over = int(sum(y > yline for y in yds)) if yline is not None and yds else (None if yline is None else 0)
            rows.append(dict(
                player=p, split=label, games=len(sub),
                weeks=",".join(str(int(w)) for w in sub.week),
                rec_list="|".join(str(r) for r in recs), yds_list="|".join(str(y) for y in yds),
                receptions_line=line, consensus_over_price=line_map.get(p,{}).get("price"),
                rec_overs=over, rec_hit_rate=(round(over/len(recs),3) if recs and over is not None else None),
                rec_games_ge_4=int(sum(r>=4 for r in recs)) if recs else None,
                rec_yards_line=yline, rec_yards_overs=y_over,
                rec_yards_hit_rate=(round(y_over/len(yds),3) if yds and y_over is not None else None),
                mean_rec=round(float(np.mean(recs)),2) if recs else None,
                mean_yds=round(float(np.mean(yds)),2) if yds else None,
                note="Historical counts only. Small sample. Not a projection or pick.",
            ))
    return pd.DataFrame(rows), line_map, yds_map


def rush_split(player, weeks, label, rush_df):
    sub = rush_df[(rush_df.player==player) & (rush_df.week.isin(weeks)) & (rush_df.status=="played")]
    att, yds = sub.official_carries.fillna(0), sub.official_rush_yards.fillna(0)
    return dict(
        player=player, split=label, games=len(sub),
        weeks=",".join(str(int(x)) for x in sorted(sub.week)),
        official_att_pg=round(float(att.mean()),2) if len(sub) else None,
        official_yds_pg=round(float(yds.mean()),2) if len(sub) else None,
        official_ypc=round(float(yds.sum()/att.sum()),2) if att.sum() else None,
        official_att_total=int(att.sum()) if len(sub) else 0,
        official_yds_total=int(yds.sum()) if len(sub) else 0,
        official_td=int(sub.official_rush_td.fillna(0).sum()) if len(sub) else 0,
        mean_official_carry_share=round(float(sub.carry_share_official.mean()),4) if sub.carry_share_official.notna().any() else None,
        max_official_carry_share=round(float(sub.carry_share_official.max()),4) if sub.carry_share_official.notna().any() else None,
        games_ge_60pct_team_carries=int((sub.carry_share_official.fillna(0)>=0.60).sum()) if len(sub) else 0,
        snap_pct=round(float(sub.off_snap_pct.mean()),1) if len(sub) else None,
        targets_pg=round(float(sub.targets.fillna(0).mean()),2) if len(sub) else None,
        rec_pg=round(float(sub.receptions.fillna(0).mean()),2) if len(sub) else None,
        rec_yds_pg=round(float(sub.rec_yards.fillna(0).mean()),2) if len(sub) else None,
        att_list="|".join(str(int(x)) for x in att),
        yds_list="|".join(str(int(x)) for x in yds),
        share_list="|".join(f"{x*100:.1f}%" for x in sub.carry_share_official.fillna(0)),
    )

def build_rush_splits(rush_df, team_carries, team_rush_yds, kneel_att, kneel_yds):
    rushers = ["Jacory Croskey-Merritt","Rachaad White","Austin Ekeler","Jeremy McNichols","Kaytron Allen","Craig Reynolds","Jayden Daniels"]
    rows = []
    for p in rushers:
        for weeks, label in [
            (JCM_WEEKS, "with_croskey_merritt_W1_5"),
            (NO_JCM_WEEKS, "without_croskey_merritt_W6_8_9"),
            ([8,9], "without_jcm_and_daniels_started_W8_9"),
            (list(range(1,10)), "all_games_played"),
        ]:
            rows.append(rush_split(p, weeks, label, rush_df))
    rsplit = pd.DataFrame(rows)
    team_rows = []
    for label, weeks in [("with_croskey_merritt_W1_5", JCM_WEEKS), ("without_croskey_merritt_W6_8_9", NO_JCM_WEEKS)]:
        yds = [team_rush_yds[w] for w in weeks]
        att = [team_carries[w] for w in weeks]
        att_ex = [team_carries[w]-kneel_att.get(w,0) for w in weeks if w!=9]
        yds_ex = [team_rush_yds[w]-kneel_yds.get(w,0) for w in weeks if w!=9]
        d = rush_df[(rush_df.player=="Jayden Daniels") & (rush_df.week.isin(weeks))]
        team_rows.append(dict(
            split=label, games=len(weeks), weeks=",".join(str(w) for w in weeks),
            team_rush_att_official_pg=round(float(np.mean(att)),2),
            team_rush_yds_official_pg=round(float(np.mean(yds)),2),
            team_ypc_official=round(sum(yds)/sum(att),2),
            team_rush_att_ex_kneel_pg=round(float(np.mean(att_ex)),2) if att_ex else None,
            team_rush_yds_ex_kneel_pg=round(float(np.mean(yds_ex)),2) if yds_ex else None,
            daniels_official_att_pg=round(float(d.official_carries.fillna(0).mean()),2) if len(d) else None,
            daniels_official_yds_pg=round(float(d.official_rush_yards.fillna(0).mean()),2) if len(d) else None,
            note="Week 9 official carries may include kneels (PBP not released). Weeks 1-8 kneels stripped in ex_kneel columns.",
        ))
    return rsplit, pd.DataFrame(team_rows)

def build_yardage(stats):
    rows = []
    for g in GAMES_META:
        w = g["week"]
        if g["opp"]=="BYE":
            continue
        wst = stats[stats.week==w]
        team_rush = int(wst.rushing_yards.sum())
        team_rec = int(wst.receiving_yards.sum())
        team_scrim = team_rush + team_rec
        daniels_rush = int(wst[wst.player_display_name=="Jayden Daniels"].rushing_yards.sum())
        other_qb_rush = int(wst[(wst.position=="QB") & (wst.player_display_name!="Jayden Daniels")].rushing_yards.sum())
        non_qb_rush = team_rush - daniels_rush - other_qb_rush
        mcl = int(wst[wst.player_display_name=="Terry McLaurin"].receiving_yards.sum())
        jcm_r = int(wst[wst.player_display_name=="Jacory Croskey-Merritt"].rushing_yards.sum())
        jcm_c = int(wst[wst.player_display_name=="Jacory Croskey-Merritt"].receiving_yards.sum())
        non_d = team_scrim - daniels_rush
        rows.append(dict(
            week=w, opponent=g["opp"], team_rush_official=team_rush, team_rec_official=team_rec,
            team_scrimmage=team_scrim, daniels_rush=daniels_rush, other_qb_rush=other_qb_rush,
            non_qb_rush=non_qb_rush, non_daniels_scrimmage=non_d,
            mclaurin_rec_yards=mcl, jcm_rush_yards=jcm_r, jcm_rec_yards=jcm_c,
            jcm_scrimmage=jcm_r+jcm_c, mclaurin_plus_jcm=mcl+jcm_r+jcm_c,
            mclaurin_plus_jcm_share_of_non_daniels_scrimmage=((mcl+jcm_r+jcm_c)/non_d if non_d else None),
            mclaurin_share_of_rec=(mcl/team_rec if team_rec else None),
            jcm_share_of_non_qb_rush=(jcm_r/non_qb_rush if non_qb_rush else None),
        ))
    return pd.DataFrame(rows)


def build_nyg_def(st_all):
    vs = st_all[(st_all.opponent_team=="NYG") & (st_all.season==SEASON) & (st_all.season_type=="REG")].copy()
    rec_vs = vs[vs.targets.fillna(0)>0]
    pos_game = (rec_vs[rec_vs.position.isin(["WR","TE","RB"])]
                .groupby(["week","team","position"])
                .agg(targets=("targets","sum"), receptions=("receptions","sum"),
                     yards=("receiving_yards","sum"), td=("receiving_tds","sum"))
                .reset_index())
    pos_avg = pos_game.groupby("position")[["targets","receptions","yards","td"]].mean().reset_index()
    pos_avg.insert(0, "stat", "per_game_allowed_average")
    pos_avg["games"] = pos_game.groupby("position").size().reindex(pos_avg.position).values
    top = rec_vs[rec_vs.position.isin(["WR","TE","RB"])][
        ["week","team","player_display_name","position","targets","receptions","receiving_yards","receiving_tds"]
    ].sort_values("receiving_yards", ascending=False)
    nyg_def = pd.read_csv(NYG_DEF_PATH)
    ctx = dict(
        source_team_page=str(NYG_DEF_PATH),
        nyg_record="5-2-1 through Week 9 (NFL Savant team page)",
        points_allowed_pg=float(nyg_def.PPG_All.iloc[0]),
        points_allowed_rank=int(nyg_def.PPG_All_rank.iloc[0]),
        pass_ypg_allowed=float(nyg_def.Pass_YPG.iloc[0]),
        pass_ypg_rank=int(nyg_def.Pass_YPG_rank.iloc[0]),
        rush_ypg_allowed=float(nyg_def.Rush_YPG.iloc[0]),
        rush_ypg_rank=int(nyg_def.Rush_YPG_rank.iloc[0]),
        success_pct_allowed=float(nyg_def.Success_pct.iloc[0]),
        success_pct_rank=int(nyg_def.Success_pct_rank.iloc[0]),
        epa_per_play=float(nyg_def.EPA_per_play.iloc[0]),
        epa_rank=int(nyg_def.EPA_per_play_rank.iloc[0]),
        pressure_pct=float(nyg_def.Pressure_pct.iloc[0]),
        pressure_rank=int(nyg_def.Pressure_pct_rank.iloc[0]),
        rz_stop_pct=float(nyg_def.RZ_Stop_pct.iloc[0]),
        rz_stop_rank=int(nyg_def.RZ_Stop_pct_rank.iloc[0]),
        takeaways=int(nyg_def.Takeaways.iloc[0]),
        note_coverage="NFL Savant has no individual defender targets-allowed / coverage matchups. Position allowed numbers are from nflverse official weekly stats, opponents vs NYG, Weeks 1-9 (NYG bye was Week 8).",
    )
    return pos_game, pos_avg, top, ctx

def build_discrepancies(rec_df, sav_path):
    sav = pd.read_csv(sav_path)
    disc = []
    for _, r in rec_df.iterrows():
        if r.status != "played" or r.position not in ("WR","TE") or not r.targets:
            continue
        s = sav[(sav.player_name==r.player) & (sav.week==r.week)]
        if len(s)==0:
            continue
        if pd.notna(s.tgt.iloc[0]) and int(s.tgt.iloc[0]) != int(r.targets or 0):
            disc.append(dict(week=int(r.week), player=r.player, field="targets", nflverse=int(r.targets),
                             savant_weekly=int(s.tgt.iloc[0]),
                             note="Prefer nflverse; Week 5 McLaurin also matches ESPN box 4-62-4"))
        if pd.notna(s.rec.iloc[0]) and int(s.rec.iloc[0]) != int(r.receptions or 0):
            disc.append(dict(week=int(r.week), player=r.player, field="receptions", nflverse=int(r.receptions),
                             savant_weekly=int(s.rec.iloc[0]), note=""))
        if pd.notna(s.yds.iloc[0]) and int(s.yds.iloc[0]) != int(r.rec_yards or 0):
            disc.append(dict(week=int(r.week), player=r.player, field="rec_yards", nflverse=int(r.rec_yards),
                             savant_weekly=int(s.yds.iloc[0]), note=""))
    ka = sav[(sav.player_name=="Kaytron Allen") & (sav.week==9)]
    if len(ka):
        disc.append(dict(
            week=9, player="Kaytron Allen", field="rushing_row",
            nflverse="not on WAS Week 9 snap chart or official stats",
            savant_weekly=f"opponent={ka.opponent.iloc[0]} result={ka.result.iloc[0]} att={ka.att.iloc[0]} yds={ka.yds.iloc[0]}",
            note="Rejected as a data error. WAS Week 9 opponent was LAR (L 13-20), not DET.",
        ))
    disc.append(dict(
        week=5, player="Jayden Daniels", field="rush_att_yds",
        nflverse="9 carries, 103 yards, 2 TD (official; ESPN box matches)",
        savant_weekly="PBP 8 rushes for 104 yards plus 1 kneel for -1",
        note="Official totals include the kneel. Ex-kneel columns use PBP for Weeks 1-8.",
    ))
    return pd.DataFrame(disc)

def build_odds_excerpt(props):
    players = ["Antonio Williams","Stefon Diggs","Chig Okonkwo","Van Jefferson","Rachaad White","Austin Ekeler","Jayden Daniels"]
    rows = []
    for p in players:
        for mkt, side in [("player_receptions","Over"),("player_reception_yds","Over"),
                          ("player_rush_attempts","Over"),("player_rush_yds","Over"),("player_anytime_td","Yes")]:
            sub = props[(props.player==p) & (props.market==mkt) & (props.side==side)]
            for _, r in sub.iterrows():
                rows.append(dict(book=r.book_title, player=p, market=mkt, side=side,
                                 line=r.point, price=r.price, n_books=r.n_books, pulled_et=r.pulled_et))
    return pd.DataFrame(rows)

def make_chart(rec_df, path):
    players = ["Stefon Diggs","Antonio Williams","Chig Okonkwo","Treylon Burks","Dyami Brown",
               "Van Jefferson","Rachaad White","Austin Ekeler","Terry McLaurin"]
    def mean_share(player, weeks):
        sub = rec_df[(rec_df.player==player) & (rec_df.week.isin(weeks)) & (rec_df.status=="played")]
        if sub.empty or sub.target_share.isna().all():
            return np.nan, 0
        return float(sub.target_share.mean())*100, len(sub)
    with_vals, with_n, wo_vals, wo_n, lim_vals, lim_n = [], [], [], [], [], []
    for p in players:
        v,n = mean_share(p, WITH_WEEKS); with_vals.append(v); with_n.append(n)
        v,n = mean_share(p, WITHOUT_WEEKS); wo_vals.append(v); wo_n.append(n)
        v,n = mean_share(p, LIMITED_WEEKS); lim_vals.append(v); lim_n.append(n)
    fig, ax = plt.subplots(figsize=(12, 6.2))
    x = np.arange(len(players)); width = 0.27
    b1 = ax.bar(x-width, with_vals, width, label="With McLaurin (Wks 1, 2, 3, 5)", color="#1f4e79")
    b2 = ax.bar(x, wo_vals, width, label="Without McLaurin (Wks 4, 8, 9)", color="#c45911")
    b3 = ax.bar(x+width, lim_vals, width, label="McLaurin limited, 7 snaps (Wk 6)", color="#7f8c8d")
    def annotate(bars, ns):
        for bar, n in zip(bars, ns):
            val = bar.get_height()
            if n==0 or (isinstance(val,float) and np.isnan(val)):
                ax.text(bar.get_x()+bar.get_width()/2, 0.4, "DNP", ha="center", va="bottom", fontsize=7, color="#555")
            else:
                ax.text(bar.get_x()+bar.get_width()/2, val+0.4, f"{val:.1f}%\nn={n}", ha="center", va="bottom", fontsize=7)
    annotate(b1, with_n); annotate(b2, wo_n); annotate(b3, lim_n)
    ax.set_ylabel("Average target share in games played (%)")
    ax.set_title("Washington target share by player, 2026 Weeks 1-9\nWith vs without Terry McLaurin  (unweighted mean of per-game shares; DNP games excluded)")
    ax.set_xticks(x)
    ax.set_xticklabels([p.replace(" ","\n") for p in players], fontsize=9)
    ax.set_ylim(0, 40)
    ax.legend(frameon=False, loc="upper right")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    fig.text(0.01, 0.01,
             "Week 7 bye omitted. Week 4 was without McLaurin but Jayden Daniels also sat (Kaliakmanis started). "
             "Diggs was out Week 5 (a with-McLaurin game). Okonkwo was out Weeks 2-3. "
             "Historical only; small samples; not a pick. Source: nflverse official weekly stats.",
             fontsize=7.5, ha="left", va="bottom")
    fig.tight_layout(rect=[0, 0.08, 1, 1])
    fig.savefig(path, dpi=160)
    plt.close()

def main():
    st_all, stats, snaps, kneels, props = load()
    skill_snaps, snap_idx, team_off_snaps, team_targets, team_carries, team_rush_yds, kneel_att, kneel_yds = build_indices(stats, snaps, kneels)
    games_df = build_games(stats, skill_snaps, snap_idx, team_targets, team_carries, team_rush_yds, team_off_snaps, kneel_att, kneel_yds)
    rec_df, rush_df = build_player_games(stats, skill_snaps, snap_idx, games_df, team_targets, team_carries, kneels, kneel_att)
    splits_df = build_splits(rec_df)
    compact_players = ["Stefon Diggs","Antonio Williams","Chig Okonkwo","Treylon Burks","Dyami Brown",
                       "Van Jefferson","Rachaad White","Austin Ekeler","John Bates","Terry McLaurin"]
    compact_splits = ["with_mclaurin_substantial_W1_2_3_5","mclaurin_limited_W6_7snaps","without_mclaurin_W4_8_9",
                      "daniels_100pct_with_mclaurin_substantial_W1_5","daniels_started_without_mclaurin_W8_9"]
    compact = splits_df[splits_df.player.isin(compact_players) & splits_df.split.isin(compact_splits)]
    hits_df, _, _ = build_hit_rates(rec_df, props)
    aw = rec_df[rec_df.player=="Antonio Williams"].sort_values("week")
    rsplit, team_rush = build_rush_splits(rush_df, team_carries, team_rush_yds, kneel_att, kneel_yds)
    yards_df = build_yardage(stats)
    pos_game, pos_avg, top, ctx = build_nyg_def(st_all)
    disc = build_discrepancies(rec_df, SAVANT_WEEKLY_PATH)
    odds = build_odds_excerpt(props)

    games_df.to_csv(OUT/"games_was_2026_wk1_9.csv", index=False)
    rec_df.to_csv(OUT/"receiving_game_by_game.csv", index=False)
    rush_df.to_csv(OUT/"rushing_game_by_game.csv", index=False)
    splits_df.to_csv(OUT/"splits_mclaurin.csv", index=False)
    compact.to_csv(OUT/"splits_mclaurin_compact.csv", index=False)
    hits_df.to_csv(OUT/"hit_rates_vs_baseline_lines.csv", index=False)
    aw.to_csv(OUT/"antonio_williams_game_log.csv", index=False)
    rsplit.to_csv(OUT/"splits_croskey_merritt.csv", index=False)
    team_rush.to_csv(OUT/"team_rushing_with_without_jcm.csv", index=False)
    yards_df.to_csv(OUT/"yardage_contribution.csv", index=False)
    pos_game.to_csv(OUT/"nyg_def_receiving_allowed_by_game_position.csv", index=False)
    pos_avg.to_csv(OUT/"nyg_def_receiving_allowed_averages.csv", index=False)
    top.to_csv(OUT/"nyg_def_receiving_allowed_player_games.csv", index=False)
    disc.to_csv(OUT/"source_discrepancies.csv", index=False)
    odds.to_csv(OUT/"baseline_props_excerpt.csv", index=False)
    with open(OUT/"nyg_defense_context.json","w") as f:
        json.dump(ctx, f, indent=2)
    make_chart(rec_df, OUT/"target_share.png")
    prov = dict(
        created_et="2026-11-10, America/New_York",
        research_only=True, projection_ready_untouched=True, no_picks=True,
        sources=dict(nflverse_stats=str(STATS_PATH), nflverse_snaps=str(SNAPS_PATH),
                     savant_pbp=str(PBP_PATH), odds_freeze=str(PROPS_PATH)),
        split_definitions=dict(with_mclaurin_substantial=WITH_WEEKS, mclaurin_limited=LIMITED_WEEKS,
                               without_mclaurin=WITHOUT_WEEKS, daniels_started=DANIELS_STARTED,
                               daniels_100pct=DANIELS_FULL, jcm_weeks=JCM_WEEKS),
        gaps=["weekly_route_share","week9_pbp_kneels","individual_NYG_coverage_targets_allowed"],
    )
    with open(OUT/"provenance.json","w") as f:
        json.dump(prov, f, indent=2)
    print("Wrote outputs to", OUT)
    for p in sorted(OUT.iterdir()):
        if p.suffix != ".py":
            print(f"  {p.name:55s} {p.stat().st_size:8d}")

if __name__ == "__main__":
    main()

