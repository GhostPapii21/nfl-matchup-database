#!/usr/bin/env python3
"""Build Washington 2026 pass-defense research tables. Research only."""
from __future__ import annotations
import hashlib, json, re
from collections import defaultdict
from pathlib import Path
import pandas as pd

OUT = Path("/workspace/was_pass_def_2026-11-10")
RAW = OUT / "raw"
GB = OUT / "gamebook"
PBP_PATH = RAW / "play_by_play_2026.parquet"
FTN_PATH = RAW / "ftn_charting_2026.parquet"
TEAM_WEEK = Path("/tmp/nflverse_2026/stats_team_week_2026.csv.gz")
PLAYER_WEEK = Path("/tmp/nflverse_2026/stats_player_week_2026.csv.gz")
SNAPS_WIDE = Path("/workspace/was_def_depth_2026-11-10/was_def_snaps_weekly_wide.csv")
GB_TXT = GB / "2026_05_NYG_WAS_gamebook.txt"
GB_PDF = GB / "2026_05_NYG_WAS_gamebook.pdf"
ASOF_ET = "2026-11-10 10:45 AM ET"
SEASON = 2026
GAME_ID_W5 = "2026_05_NYG_WAS"

ERA_LABELS = {
    1: "early_sainristil_nickel",
    2: "early_sainristil_nickel",
    3: "transition_cross_out_sainristil_down",
    4: "transition_cross_out_sainristil_down",
    5: "transition_cross_out_sainristil_down",
    6: "transition_amos_activated",
    8: "amos_robertson_starting",
    9: "amos_robertson_starting",
}
ERA_NOTES = {
    "early_sainristil_nickel": "Weeks 1-2. Sainristil every-down nickel (98%, 82%). Amos on reserve. Cross every-down SS.",
    "transition_cross_out_sainristil_down": "Weeks 3-5. Sainristil snaps collapsed (39%, 8%, 48%). Cross out (illness). Martin every-down (87-99%). Douglas starter-level in W4-5 (85%, 98%). Amos still on reserve. Not the W1-2 look and not the W8-9 look.",
    "transition_amos_activated": "Week 6 only. Amos activated (58%). Cross returned (89%). Sainristil 11%. Douglas 58%. One-game sample.",
    "amos_robertson_starting": "Weeks 8-9 after the bye. Amos 87% then 97% and started W9. Robertson every-down. Sainristil 0% and 1%. Douglas 46% then 24%. Cross 100%.",
}
NAME_MAP = {
    "R.Douglas": "Rasul Douglas", "A.Robertson": "Amik Robertson", "Q.Martin": "Quan Martin",
    "J.Reaves": "Jeremy Reaves", "S.Styles": "Sonny Styles", "F.Luvu": "Frankie Luvu",
    "F.Moreau": "Fabian Moreau", "D.Armstrong": "Dorance Armstrong", "K.Chaisson": "K'Lavon Chaisson",
    "M.Sainristil": "Mike Sainristil", "O.Oweh": "Odafe Oweh", "D.Wise": "Deatrich Wise",
    "D.Payne": "Daron Payne", "J.Kinlaw": "Javon Kinlaw", "T.Settle": "Tim Settle",
    "S.Tuttle": "Shy Tuttle", "J.Josephs": "Joshua Josephs",
}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def era_for(week: int) -> str:
    return ERA_LABELS[week]

SCHEDULE = {
    1: ("PHI", "away", "2026-09-13", "L 22-24"),
    2: ("DAL", "away", "2026-09-20", "L 20-37"),
    3: ("SEA", "home", "2026-09-27", "W 33-31"),
    4: ("IND", "home", "2026-10-04", "L 13-30"),
    5: ("NYG", "home", "2026-10-11", "T 27-27 OT"),
    6: ("SF", "away", "2026-10-19", "L 17-23"),
    8: ("PHI", "home", "2026-11-01", "W 27-10"),
    9: ("LA", "home", "2026-11-08", "L 13-20"),
}

def official_allowed(tw: pd.DataFrame) -> pd.DataFrame:
    opp = tw[(tw.opponent_team == "WAS") & (tw.season_type == "REG")].copy()
    was = tw[(tw.team == "WAS") & (tw.season_type == "REG")].copy()
    keep_opp = ["week","game_id","team","completions","attempts","passing_yards","passing_tds",
                "passing_interceptions","sacks_suffered","sack_yards_lost","passing_epa",
                "passing_20","passing_16","passing_10","passing_cpoe","passing_air_yards",
                "passing_yards_after_catch","passing_first_downs"]
    keep_was = ["week","game_id","opponent_team","def_sacks","def_sack_yards","def_qb_hits",
                "def_interceptions","def_pass_defended"]
    return opp[keep_opp].merge(was[keep_was], on=["week","game_id"], how="outer").sort_values("week")

def pbp_pass_defense(pbp: pd.DataFrame) -> pd.DataFrame:
    was = pbp[(pbp.season == SEASON) & (pbp.defteam == "WAS") & (pbp.season_type == "REG")].copy()
    was["is_dropback"] = was["qb_dropback"].fillna(0).astype(int).eq(1)
    was["is_pass_play"] = was["play_type"].eq("pass")
    was["is_official_att"] = (
        was["pass_attempt"].fillna(0).eq(1)
        & was["sack"].fillna(0).eq(0)
        & ~was["desc"].fillna("").str.contains("No Play", case=False)
    )
    was["is_complete"] = was["complete_pass"].fillna(0).eq(1) & was["is_official_att"]
    was["is_int"] = was["interception"].fillna(0).eq(1) & was["is_official_att"]
    was["is_td"] = was["pass_touchdown"].fillna(0).eq(1)
    was["is_sack"] = was["sack"].fillna(0).eq(1) & was["is_pass_play"]
    was["yards_gained_num"] = pd.to_numeric(was["yards_gained"], errors="coerce")
    was["is_explosive_rec_20"] = was["is_complete"] & was["yards_gained_num"].ge(20)
    return was

def ftn_for_was(ftn: pd.DataFrame, pbp_was: pd.DataFrame) -> pd.DataFrame:
    f = ftn[ftn.nflverse_game_id.astype(str).str.contains("WAS")].copy()
    keys = pbp_was.loc[pbp_was.is_dropback, ["game_id","play_id","week","epa"]].copy()
    keys["play_id"] = pd.to_numeric(keys["play_id"], errors="coerce")
    f["nflverse_play_id"] = pd.to_numeric(f["nflverse_play_id"], errors="coerce")
    return keys.merge(f, left_on=["game_id","play_id"], right_on=["nflverse_game_id","nflverse_play_id"], how="left")

def position_allowed(pbp_was: pd.DataFrame, pw: pd.DataFrame) -> pd.DataFrame:
    tgt = pbp_was[pbp_was.is_official_att & pbp_was.receiver_player_id.notna()].copy()
    pos = pw[(pw.season == SEASON) & (pw.opponent_team == "WAS") & (pw.season_type == "REG")][
        ["week","player_id","position","position_group"]
    ].copy()
    anypos = (
        pw[(pw.season == SEASON)][["player_id","position","position_group"]]
        .dropna(subset=["player_id"]).drop_duplicates("player_id")
        .rename(columns={"position":"position_any","position_group":"position_group_any"})
    )
    tgt = tgt.merge(pos.rename(columns={"player_id":"receiver_player_id"}), on=["week","receiver_player_id"], how="left")
    tgt = tgt.merge(anypos.rename(columns={"player_id":"receiver_player_id"}), on="receiver_player_id", how="left")
    tgt["pos_group"] = tgt["position_group"].fillna(tgt["position_group_any"]).fillna("UNKNOWN")
    return tgt

def snap_pct(snaps, name, week):
    r = snaps[snaps.player_name == name]
    if r.empty:
        return None
    col = f"w{week}_snap_pct"
    if col not in r.columns:
        return None
    v = r.iloc[0][col]
    return None if pd.isna(v) else float(v)

def summarize_games(pbp_was, official, ftn_j, pos_tgt, snaps) -> pd.DataFrame:
    rows = []
    for _, off in official.iterrows():
        week = int(off.week)
        if week == 7:
            continue
        g = pbp_was[pbp_was.week == week]
        week_col = "week" if "week" in ftn_j.columns else ("week_x" if "week_x" in ftn_j.columns else None)
        fj = ftn_j[ftn_j[week_col] == week] if week_col else ftn_j[ftn_j.game_id == off.game_id]
        drop = g[g.is_dropback]
        att = int(off.attempts); cmp_ = int(off.completions); yds = int(off.passing_yards)
        tds = int(off.passing_tds); ints = int(off.passing_interceptions)
        sacks_off = int(off.def_sacks) if pd.notna(off.def_sacks) else int(off.sacks_suffered)
        sack_yds = int(off.def_sack_yards) if pd.notna(off.def_sack_yards) else int(abs(off.sack_yards_lost))
        qb_hits = int(off.def_qb_hits) if pd.notna(off.def_qb_hits) else None
        pds = int(off.def_pass_defended) if pd.notna(off.def_pass_defended) else None
        official_expl = int(off.passing_20) if pd.notna(off.passing_20) else None
        dropbacks = int(drop.shape[0])
        epa_sum = float(drop["epa"].sum()) if dropbacks else None
        epa_per = float(drop["epa"].mean()) if dropbacks else None
        succ = float(drop["success"].mean()) if dropbacks and "success" in drop.columns else None
        pbp_att = int(g.is_official_att.sum()); pbp_cmp = int(g.is_complete.sum())
        pbp_yds = float(g.loc[g.is_complete, "yards_gained_num"].sum())
        pbp_td = int(g.is_td.sum()); pbp_int = int(g.is_int.sum()); pbp_sack = int(g.is_sack.sum())
        pbp_expl = int(g.is_explosive_rec_20.sum())
        ftn_drop = fj[fj["n_pass_rushers"].notna()] if "n_pass_rushers" in fj.columns else fj.iloc[0:0]
        ftn_matched = int(len(ftn_drop))
        mean_rushers = float(ftn_drop["n_pass_rushers"].mean()) if len(ftn_drop) else None
        mean_blitzers = float(ftn_drop["n_blitzers"].mean()) if len(ftn_drop) and "n_blitzers" in ftn_drop.columns else None
        mean_box = float(ftn_drop["n_defense_box"].mean()) if len(ftn_drop) and "n_defense_box" in ftn_drop.columns else None
        pct_blitz = float((ftn_drop["n_blitzers"] >= 1).mean()) if len(ftn_drop) and "n_blitzers" in ftn_drop.columns else None
        pct_rush5 = float((ftn_drop["n_pass_rushers"] >= 5).mean()) if len(ftn_drop) else None
        pt = pos_tgt[pos_tgt.week == week]
        def pg(grp):
            sub = pt[pt.pos_group == grp]
            return int(sub.shape[0]), int(sub.is_complete.sum()), float(sub.loc[sub.is_complete, "yards_gained_num"].sum()), int(sub.is_td.sum()), int(sub.is_explosive_rec_20.sum())
        wr, te, rb = pg("WR"), pg("TE"), pg("RB")
        unknown = int(pt[~pt.pos_group.isin(["WR","TE","RB"])].shape[0])
        opp, loc, date, result = SCHEDULE[week]
        rows.append({
            "season": SEASON, "week": week, "game_id": off.game_id, "game_date": date,
            "opponent": opp, "home_away": loc, "result": result,
            "secondary_era": era_for(week), "era_note": ERA_NOTES[era_for(week)],
            "sainristil_def_snap_pct": snap_pct(snaps, "Mike Sainristil", week),
            "amos_def_snap_pct": snap_pct(snaps, "Trey Amos", week),
            "robertson_def_snap_pct": snap_pct(snaps, "Amik Robertson", week),
            "douglas_def_snap_pct": snap_pct(snaps, "Rasul Douglas", week),
            "cross_def_snap_pct": snap_pct(snaps, "Nick Cross", week),
            "reaves_def_snap_pct": snap_pct(snaps, "Jeremy Reaves", week),
            "martin_def_snap_pct": snap_pct(snaps, "Quan Martin", week),
            "official_cmp": cmp_, "official_att": att,
            "official_cmp_pct": round(100 * cmp_ / att, 1) if att else None,
            "official_pass_yds_gross": yds, "official_pass_tds": tds, "official_int": ints,
            "official_ypa_gross": round(yds / att, 2) if att else None,
            "official_sacks": sacks_off, "official_sack_yds": sack_yds,
            "official_net_pass_yds": yds - sack_yds, "official_qb_hits": qb_hits,
            "official_pass_defended": pds, "official_completions_20plus": official_expl,
            "official_passing_epa": float(off.passing_epa) if pd.notna(off.passing_epa) else None,
            "pbp_official_att": pbp_att, "pbp_completions": pbp_cmp, "pbp_rec_yds": pbp_yds,
            "pbp_pass_tds": pbp_td, "pbp_int": pbp_int, "pbp_sacks": pbp_sack,
            "pbp_dropbacks": dropbacks,
            "pbp_epa_per_dropback": round(epa_per, 3) if epa_per is not None else None,
            "pbp_epa_sum_dropbacks": round(epa_sum, 3) if epa_sum is not None else None,
            "pbp_dropback_success_rate": round(succ, 3) if succ is not None else None,
            "pbp_explosive_rec_20plus": pbp_expl,
            "weekly_true_pressures": "unavailable — PBP has sacks and qb_hits only; Savant pressure is season-level; no pbp_participation_2026",
            "ftn_dropbacks_matched": ftn_matched,
            "ftn_mean_pass_rushers": round(mean_rushers, 2) if mean_rushers is not None else None,
            "ftn_mean_blitzers": round(mean_blitzers, 2) if mean_blitzers is not None else None,
            "ftn_pct_dropbacks_blitzers_ge1": round(pct_blitz, 3) if pct_blitz is not None else None,
            "ftn_pct_dropbacks_rushers_ge5": round(pct_rush5, 3) if pct_rush5 is not None else None,
            "ftn_mean_defenders_in_box_on_dropbacks": round(mean_box, 2) if mean_box is not None else None,
            "wr_targets_allowed": wr[0], "wr_rec_allowed": wr[1], "wr_yds_allowed": wr[2], "wr_td_allowed": wr[3], "wr_expl20_allowed": wr[4],
            "te_targets_allowed": te[0], "te_rec_allowed": te[1], "te_yds_allowed": te[2], "te_td_allowed": te[3], "te_expl20_allowed": te[4],
            "rb_targets_allowed": rb[0], "rb_rec_allowed": rb[1], "rb_yds_allowed": rb[2], "rb_td_allowed": rb[3], "rb_expl20_allowed": rb[4],
            "unknown_position_targets": unknown,
            "pbp_vs_official_att_diff": pbp_att - att,
            "pbp_vs_official_yds_diff": pbp_yds - yds,
            "pbp_vs_official_expl20_diff": (pbp_expl - official_expl) if official_expl is not None else None,
        })
    return pd.DataFrame(rows)

def summarize_eras(games: pd.DataFrame) -> pd.DataFrame:
    groups = {
        "early_sainristil_nickel_w1_2": games[games.week.isin([1, 2])],
        "transition_w3_6": games[games.week.isin([3, 4, 5, 6])],
        "amos_robertson_w8_9": games[games.week.isin([8, 9])],
        "pre_bye_w1_6": games[games.week.isin([1, 2, 3, 4, 5, 6])],
        "season_w1_9": games,
    }
    notes = {
        "early_sainristil_nickel_w1_2": ERA_NOTES["early_sainristil_nickel"],
        "transition_w3_6": ERA_NOTES["transition_cross_out_sainristil_down"] + " " + ERA_NOTES["transition_amos_activated"],
        "amos_robertson_w8_9": ERA_NOTES["amos_robertson_starting"],
        "pre_bye_w1_6": "All six games before the Week 7 bye. Mixed looks; not a clean single-look sample.",
        "season_w1_9": "All eight games through Week 9 (bye in Week 7).",
    }
    rows = []
    for name, g in groups.items():
        att = int(g.official_att.sum()); cmp_ = int(g.official_cmp.sum()); yds = int(g.official_pass_yds_gross.sum())
        dropbacks = int(g.pbp_dropbacks.sum()); epa_sum = float(g.pbp_epa_sum_dropbacks.sum())
        sacks = int(g.official_sacks.sum())
        rows.append({
            "era": name, "games": int(g.week.nunique()),
            "weeks": ",".join(str(w) for w in sorted(g.week)),
            "opponents": " | ".join(f"W{w} {o}" for w, o in zip(g.week, g.opponent)),
            "official_cmp": cmp_, "official_att": att,
            "official_cmp_pct": round(100 * cmp_ / att, 1) if att else None,
            "official_pass_yds_gross": yds,
            "official_pass_yds_per_game": round(yds / len(g), 1),
            "official_pass_tds": int(g.official_pass_tds.sum()),
            "official_int": int(g.official_int.sum()),
            "official_ypa_gross": round(yds / att, 2) if att else None,
            "official_sacks": sacks, "official_sack_yds": int(g.official_sack_yds.sum()),
            "official_sack_rate_per_dropback": round(sacks / dropbacks, 3) if dropbacks else None,
            "official_net_pass_yds": int(g.official_net_pass_yds.sum()),
            "official_qb_hits": int(g.official_qb_hits.sum()),
            "official_completions_20plus": int(g.official_completions_20plus.sum()),
            "official_expl20_per_game": round(g.official_completions_20plus.sum() / len(g), 2),
            "pbp_dropbacks": dropbacks,
            "pbp_epa_per_dropback": round(epa_sum / dropbacks, 3) if dropbacks else None,
            "pbp_explosive_rec_20plus": int(g.pbp_explosive_rec_20plus.sum()),
            "wr_targets": int(g.wr_targets_allowed.sum()), "wr_rec": int(g.wr_rec_allowed.sum()),
            "wr_yds": float(g.wr_yds_allowed.sum()), "wr_td": int(g.wr_td_allowed.sum()),
            "te_targets": int(g.te_targets_allowed.sum()), "te_rec": int(g.te_rec_allowed.sum()),
            "te_yds": float(g.te_yds_allowed.sum()), "te_td": int(g.te_td_allowed.sum()),
            "rb_targets": int(g.rb_targets_allowed.sum()), "rb_rec": int(g.rb_rec_allowed.sum()),
            "rb_yds": float(g.rb_yds_allowed.sum()), "rb_td": int(g.rb_td_allowed.sum()),
            "ftn_mean_pass_rushers_unweighted_game_avg": round(g.ftn_mean_pass_rushers.mean(), 2),
            "ftn_mean_pct_blitzers_ge1_unweighted_game_avg": round(g.ftn_pct_dropbacks_blitzers_ge1.mean(), 3),
            "sample_caution": "Small samples. Early era and Amos/Robertson era are 2 games each. Only same-opponent pair is PHI in Week 1 vs Week 8.",
            "note": notes[name],
        })
    return pd.DataFrame(rows)

def position_by_game(pos_tgt: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (week, gid, grp), sub in pos_tgt.groupby(["week","game_id","pos_group"]):
        rows.append({
            "week": int(week), "game_id": gid, "secondary_era": era_for(int(week)),
            "position_group": grp, "targets": int(sub.shape[0]),
            "receptions": int(sub.is_complete.sum()),
            "yards": float(sub.loc[sub.is_complete, "yards_gained_num"].sum()),
            "tds": int(sub.is_td.sum()), "explosive_rec_20plus": int(sub.is_explosive_rec_20.sum()),
            "ypa_on_targets": round(float(sub.loc[sub.is_complete, "yards_gained_num"].sum()) / sub.shape[0], 2) if len(sub) else None,
            "catch_rate": round(float(sub.is_complete.mean()), 3) if len(sub) else None,
        })
    return pd.DataFrame(rows).sort_values(["week","position_group"])

PLAY_START = re.compile(
    r"^\s*(\d)-(\d+|goal|Goal)\s*[-–]\s*([A-Z]{2,3})\s+(\d+)\s+\(([^)]+)\)\s*(.*)$"
)

def parse_gamebook_plays(text: str) -> list[dict]:
    lines = text.splitlines()
    chunks = []
    current = []
    in_pbp = False
    qtr = None
    for i, line in enumerate(lines, 1):
        mhead = re.search(r"^Play By Play\s+(First Quarter|Second Quarter|Third Quarter|Fourth Quarter|Overtime)", line)
        if mhead:
            if current:
                chunks.append((qtr, current))
            qtr = mhead.group(1)
            in_pbp = True
            current = []
            continue
        if in_pbp:
            if re.search(r"Miscellaneous Statistics|Ten Longest Plays|Final Individual Statistics|Final Team Statistics", line):
                in_pbp = False
                continue
            current.append((i, line))
    if current:
        chunks.append((qtr, current))
    plays = []
    for qtr, clines in chunks:
        buf = ""; start_line = None
        for i, line in clines:
            if PLAY_START.match(line) or re.match(r"^\s*\d-\d+\s*[-–]\s*([A-Z]{2,3}\s+)?\d+\s+\(\d", line):
                if buf:
                    plays.append(_finish_play(qtr, start_line, buf))
                buf = line.rstrip(); start_line = i
            elif buf:
                stripped = line.strip()
                if not stripped or stripped.startswith("\x0c"):
                    continue
                if stripped.startswith("Play By Play") or stripped.startswith("New York Giants vs") or stripped.startswith("Timeout at"):
                    continue
                if re.match(r"^END OF QUARTER|^Washington Commanders (at|continued)|^New York Giants at|^Two-Minute Warning|^Timeout #|^\*\* Injury", stripped):
                    continue
                if re.match(r"^D\.(Zvada|Stevens) (kicks|extra)", stripped):
                    continue
                if re.match(r"^(Score\s+Poss|New York Giants\s+\d+|Washington Commanders\s+\d+|Miscellaneous|Ten Longest|END OF GAME)", stripped):
                    continue
                # do not swallow a following play that the starter regex missed
                if re.match(r"^\d-\d+", stripped) and re.search(r"\(\d+:\d+\)|\(:\d+\)", stripped):
                    if buf:
                        plays.append(_finish_play(qtr, start_line, buf))
                    buf = line.rstrip(); start_line = i
                    continue
                buf += " " + stripped
        if buf:
            plays.append(_finish_play(qtr, start_line, buf))
    return [p for p in plays if p]

def _finish_play(qtr, start_line, buf):
    m = PLAY_START.match(buf)
    if not m:
        return {}
    down, dist, side, yrd, clock, rest = m.groups()
    text = rest
    return {
        "qtr_label": qtr,
        "quarter": {"First Quarter":1,"Second Quarter":2,"Third Quarter":3,"Fourth Quarter":4,"Overtime":5}.get(qtr),
        "src_line": start_line, "down": int(down), "distance": dist,
        "spot_side": side, "spot_yard": int(yrd), "clock": clock,
        "raw": re.sub(r"\s+", " ", buf).strip(),
        "description": re.sub(r"\s+", " ", text).strip(),
        "no_play": bool(re.search(r"No Play", text, re.I)),
        "reversed": bool(re.search(r"play was REVERSED", text, re.I)),
    }

def extract_named_defenders(desc: str) -> dict:
    qb_hit_names = []
    for block in re.findall(r"\[([^\]]+)\]", desc):
        for part in re.split(r"[;,]", block):
            part = part.strip()
            if re.match(r"[A-Z]\.[A-Za-z][-A-Za-z']+", part):
                qb_hit_names.append(part)
    int_m = re.search(r"INTERCEPTED by\s+([A-Z]\.[A-Za-z][-A-Za-z']+)", desc)
    # drop the return-tackler clause after an interception (often the intended receiver or an offensive player)
    desc_for_paren = re.sub(r"INTERCEPTED by .+?(?=PENALTY|$)", "INTERCEPTED. ", desc, flags=re.I|re.S)
    credit = []
    for block in re.findall(r"\(([^)]+)\)", desc_for_paren):
        if re.match(r"^(Shotgun|No Huddle|No Huddle, Shotgun|\d+:\d+)$", block):
            continue
        if re.search(r"[A-Z]\.[A-Za-z]", block):
            for p in re.split(r"[;,]", block):
                m = re.match(r"([A-Z]\.[A-Za-z][-A-Za-z']+)", p.strip())
                if m:
                    credit.append(m.group(1))
    pens = re.findall(r"PENALTY on WAS-([A-Z]\.[A-Za-z][-A-Za-z']+),\s*([^,]+)", desc)
    return {
        "named_in_parentheses": credit,
        "interception_credited": int_m.group(1) if int_m else None,
        "qb_hits_brackets": qb_hit_names,
        "penalties_on": [(a, b.strip()) for a, b in pens],
    }

def effective_desc(desc, reversed_):
    """For reviewed plays, official result is the text after 'the play was REVERSED.'"""
    if not reversed_:
        return desc
    parts = re.split(r"the play was REVERSED\.?", desc, flags=re.I)
    return parts[-1].strip() if len(parts) > 1 else desc

def classify_pass_result(desc, no_play, reversed_):
    used = effective_desc(desc, reversed_)
    inc = bool(re.search(r"pass incomplete", used, re.I))
    intercepted_raw = bool(re.search(r"INTERCEPTED", used))
    td = bool(re.search(r"TOUCHDOWN", used)) and not no_play
    yds = None
    m_td = re.search(r"for (\d+) yards?, TOUCHDOWN", used)
    m = re.search(r"for (-?\d+) yards?", used)
    if m_td:
        yds = int(m_td.group(1))
    elif m and not inc:
        yds = int(m.group(1))
    if intercepted_raw and no_play:
        result, complete = "interception_nullified_no_play", False
    elif intercepted_raw and not no_play:
        result, complete = "interception", False
    elif no_play:
        result, complete = "no_play", False
    elif inc:
        result, complete = "incomplete", False
    elif td and reversed_:
        result, complete = "touchdown_after_replay_reversal", True
    elif td:
        result, complete = "touchdown", True
    else:
        result, complete = "complete", True
    return {"result": result, "complete": complete, "yards": yds, "is_td": bool(td and not no_play)}

def nabers_likely_from_gamebook(plays):
    rows = []
    for p in plays:
        desc = p["description"]
        to_nabers = bool(re.search(r"(to|intended for)\s+M\.Nabers\b", desc))
        to_likely = bool(re.search(r"(to|intended for)\s+I\.Likely\b", desc))
        if not (to_nabers or to_likely):
            continue
        if "pass" not in desc.lower() and "INTERCEPTED" not in desc:
            continue
        target = "Malik Nabers" if to_nabers else "Isaiah Likely"
        used = effective_desc(desc, p["reversed"])
        names = extract_named_defenders(used)
        names_all = extract_named_defenders(desc)
        res = classify_pass_result(desc, p["no_play"], p["reversed"])
        loc = None
        mloc = re.search(r"pass (incomplete )?(short|deep) (left|middle|right)", desc)
        if mloc:
            loc = f"{mloc.group(2)} {mloc.group(3)}"
        mp = re.search(r"([A-Z]\.[A-Za-z]+)\s+pass ", desc)
        official_target = (not p["no_play"]) and ("pass" in desc.lower() or "INTERCEPTED" in desc)
        rows.append({
            "game_id": GAME_ID_W5, "game_date": "2026-10-11",
            "site": "Northwest Stadium, Landover, MD",
            "quarter": p["quarter"], "quarter_label": p["qtr_label"], "clock": p["clock"],
            "down": p["down"], "distance": p["distance"],
            "spot": f"{p['spot_side']} {p['spot_yard']}",
            "passer": mp.group(1) if mp else None, "target": target,
            "target_abbr": "M.Nabers" if to_nabers else "I.Likely",
            "pass_location": loc, "result": res["result"],
            "official_target": official_target, "complete": res["complete"] if official_target else False,
            "yards": res["yards"] if official_target else None,
            "touchdown": res["is_td"] if official_target else False,
            "no_play": p["no_play"], "replay_reversal": p["reversed"],
            "named_tackler_or_pass_defender": "; ".join(names["named_in_parentheses"]) if names["named_in_parentheses"] else "",
            "named_interception": names["interception_credited"] or "",
            "named_qb_hit_brackets": "; ".join(names["qb_hits_brackets"]) if names["qb_hits_brackets"] else "",
            "penalty_on_was": "; ".join(f"{a} ({b})" for a,b in names["penalties_on"]) if names["penalties_on"] else "",
            "coverage_assignment_available": False,
            "credit_caveat": "Named defender is the official gamebook credit (tackler or pass defender in parentheses, or interceptor). Not a verified coverage assignment.",
            "gamebook_line": p["src_line"], "play_text": p["raw"],
        })
    return pd.DataFrame(rows)

def pbp_targets_week5(pbp: pd.DataFrame) -> pd.DataFrame:
    g = pbp[(pbp.game_id == GAME_ID_W5) & (pbp.posteam == "NYG")].copy()
    mask = g.receiver_player_name.isin(["M.Nabers","I.Likely"])
    desc_mask = g.desc.fillna("").str.contains(r"M\.Nabers|I\.Likely", regex=True) & g.desc.fillna("").str.contains("pass", case=False)
    rows = []
    for _, r in g[mask | desc_mask].iterrows():
        desc = str(r.desc)
        if "pass" not in desc.lower() and "INTERCEPTED" not in desc:
            continue
        is_no_play = "No Play" in desc
        name = r.receiver_player_name if pd.notna(r.receiver_player_name) else ("M.Nabers" if "M.Nabers" in desc else ("I.Likely" if "I.Likely" in desc else None))
        if name not in ("M.Nabers","I.Likely"):
            continue
        full = "Malik Nabers" if name == "M.Nabers" else "Isaiah Likely"
        tacklers = [str(r[c]) for c in ["solo_tackle_1_player_name","solo_tackle_2_player_name","assist_tackle_1_player_name","assist_tackle_2_player_name","tackle_with_assist_1_player_name","tackle_with_assist_2_player_name"] if c in r and pd.notna(r[c])]
        pds = [str(r[c]) for c in ["pass_defense_1_player_name","pass_defense_2_player_name"] if c in r and pd.notna(r[c])]
        rows.append({
            "game_id": r.game_id, "play_id": r.play_id,
            "quarter": int(r.qtr) if pd.notna(r.qtr) else None, "clock": r.time,
            "down": int(r.down) if pd.notna(r.down) else None,
            "ydstogo": int(r.ydstogo) if pd.notna(r.ydstogo) else None,
            "yardline": r.yrdln, "passer": r.passer_player_name, "target": full,
            "complete": bool(r.complete_pass == 1) and not is_no_play,
            "yards_gained": r.yards_gained if not is_no_play else None,
            "air_yards": r.air_yards if pd.notna(r.air_yards) else None,
            "yards_after_catch": r.yards_after_catch if pd.notna(r.yards_after_catch) else None,
            "pass_length": r.pass_length, "pass_location": r.pass_location,
            "touchdown": bool(r.pass_touchdown == 1) and not is_no_play,
            "interception": bool(r.interception == 1) and not is_no_play,
            "no_play": is_no_play, "epa": r.epa if pd.notna(r.epa) else None,
            "pbp_tacklers": "; ".join(tacklers), "pbp_pass_defense": "; ".join(pds),
            "pbp_interception_player": r.interception_player_name if pd.notna(r.interception_player_name) else "",
            "pbp_qb_hit": r.qb_hit_1_player_name if "qb_hit_1_player_name" in r and pd.notna(r.qb_hit_1_player_name) else "",
            "coverage_assignment_available": False,
            "credit_caveat": "nflverse tackle / pass_defense fields are official-stat credits, not coverage assignments.",
            "desc": desc,
        })
    return pd.DataFrame(rows)

def _clock_sec(c):
    if pd.isna(c):
        return None
    s = str(c).strip()
    if ":" in s:
        a,b = s.split(":")
        try:
            return int(a)*60+int(b)
        except Exception:
            return None
    return None

def crosswalk(gb, pbp):
    pbp = pbp.copy(); gb = gb.copy()
    pbp["clock_sec"] = pbp["clock"].map(_clock_sec)
    gb["clock_sec"] = gb["clock"].map(_clock_sec)
    rows = []; used = set()
    for i, g in gb.iterrows():
        cand = pbp[(pbp.target == g.target) & (pbp.quarter == g.quarter)]
        best = None
        for j, p in cand.iterrows():
            if j in used:
                continue
            if g.down and p.down and int(g.down) != int(p.down):
                continue
            if g.clock_sec is not None and p.clock_sec is not None and abs(g.clock_sec - p.clock_sec) > 2:
                continue
            best = j; break
        if best is None:
            for j, p in cand.iterrows():
                if j in used:
                    continue
                if g.down and p.down and int(g.down) == int(p.down):
                    best = j; break
        rec = {"quarter": g.quarter, "clock": g.clock, "down": g.down, "distance": g.distance,
               "target": g.target, "gamebook_result": g.result, "gamebook_yards": g.yards,
               "gamebook_td": g.touchdown, "gamebook_official_target": g.official_target,
               "gamebook_named_tackler_or_pd": g.named_tackler_or_pass_defender,
               "gamebook_named_int": g.named_interception, "gamebook_qb_hit": g.named_qb_hit_brackets,
               "gamebook_no_play": g.no_play, "matched_pbp": best is not None}
        if best is not None:
            used.add(best); p = pbp.loc[best]
            rec.update({"pbp_play_id": p.play_id, "pbp_complete": p.complete, "pbp_yards": p.yards_gained,
                        "pbp_td": p.touchdown, "pbp_tacklers": p.pbp_tacklers, "pbp_pass_defense": p.pbp_pass_defense,
                        "pbp_epa": p.epa, "pbp_no_play": p.no_play})
        else:
            rec.update({k: None for k in ["pbp_play_id","pbp_complete","pbp_yards","pbp_td","pbp_tacklers","pbp_pass_defense","pbp_epa","pbp_no_play"]})
        rows.append(rec)
    return pd.DataFrame(rows)

def defender_counts(gb):
    official = gb[gb.official_target].copy()
    rows = []
    for target, sub in official.groupby("target"):
        counter = defaultdict(lambda: {"plays":0,"paren":0,"comp":0,"yards":0,"tds":0,"incs":0,"hits":0})
        for _, r in sub.iterrows():
            names = [n.strip() for n in str(r.named_tackler_or_pass_defender).split(";") if n.strip()]
            hits = [n.strip() for n in str(r.named_qb_hit_brackets).split(";") if n.strip()]
            if not names:
                key = "(no named tackler/pass defender)"
                counter[key]["plays"] += 1
                if r.complete:
                    counter[key]["comp"] += 1; counter[key]["yards"] += r.yards or 0
                if r.touchdown:
                    counter[key]["tds"] += 1
            else:
                for n in list(dict.fromkeys(names)):
                    counter[n]["plays"] += 1; counter[n]["paren"] += 1
                    if r.complete:
                        counter[n]["comp"] += 1; counter[n]["yards"] += r.yards or 0
                    if r.touchdown:
                        counter[n]["tds"] += 1
                    if r.result == "incomplete":
                        counter[n]["incs"] += 1
            for n in hits:
                if n not in names:
                    counter[n]["hits"] += 1
        for n,c in counter.items():
            rows.append({"target": target, "defender_abbr": n, "defender_full": NAME_MAP.get(n, n),
                         "official_targets_where_named_in_parentheses": c["plays"] if (n.startswith("(") or c["paren"] or c["plays"]) else 0,
                         "paren_credits": c["paren"], "completions_when_named": c["comp"],
                         "yards_when_named": c["yards"], "tds_when_named": c["tds"],
                         "incompletes_when_named": c["incs"], "qb_hit_only_credits": c["hits"],
                         "credit_is_not_coverage_assignment": True})
    return pd.DataFrame(rows)

ROLE_NOW = {
    "Rasul Douglas": "Active, but not the Week 5 every-down starter. Snap share fell from 98% in Week 5 to 46% (W8) and 24% (W9). Week 9 gamebook: substitute, not a starter (Amos and Robertson started). ESPN still lists him as starting LCB; that does not match Weeks 8-9 usage.",
    "Amik Robertson": "Active and still every-down. 99% Week 8, 96% Week 9. Official Week 9 starting CB. ESPN lists him as starting nickel. Highest-usage corner on the current roster.",
    "Quan Martin": "Active, reduced role after Cross returned. He was every-down in Week 5 (99%) because Cross was out. Weeks 8-9: 46% and 56%. ESPN lists him as the FS backup behind Reaves.",
    "Jeremy Reaves": "Active. Official Week 9 starting safety and ESPN starting FS. 93% Week 8, season-low 60% in Week 9.",
    "Sonny Styles": "Active, every-down ILB. 99% Week 8, 97% Week 9. Official Week 9 starting LB.",
    "Frankie Luvu": "Active, every-down ILB. 100% in Weeks 8 and 9. Official Week 9 starting LB.",
    "Fabian Moreau": "Played Weeks 3-5 only (30%, 39%, 29%), including Week 5 vs NYG. Inactive in the official Week 9 gamebook. No Week 8 defensive snaps. nflverse Week 8 practice: full (knee); no Week 9/10 game-status tag. ESPN lists him as Douglas's backup. Do not assume he is active Thursday until the inactive list posts.",
    "Dorance Armstrong": "Active, rotational OLB/edge. 58% Week 8, 53% Week 9. ESPN lists him as starting SLB, but Chaisson started Week 9 and has the higher season snap share.",
    "K'Lavon Chaisson": "Active, starter-level edge. 71% Week 8, 61% Week 9. Official Week 9 starting OLB. On the Week 5 Nabers/Likely plays he is credited only as a QB hit (brackets), not as a tackler or pass defender.",
}

def _status(full):
    if full in {"Daron Payne","Javon Kinlaw","Javontae Jean-Baptiste","Leo Chenal","Dyami Brown"}:
        return False, "Injured reserve (ESPN list as of Nov 10, 2026)."
    if full == "Shy Tuttle":
        return True, "Questionable (shoulder) on ESPN Nov 9-10 screenshots. Week 10 official report not in nflverse yet. Not a Week 5 Nabers/Likely credit."
    if full == "Fabian Moreau":
        return "uncertain", "Not on the ESPN IR list. Inactive in the Week 9 official gamebook. No Week 10 injury report in nflverse. Do not assume he is active Thursday until the inactive list posts."
    return True, "Not on the Nov 10 ESPN IR list (Payne, Kinlaw, Jean-Baptiste, Chenal, Dyami Brown). No Week 10 nflverse injury-report game status for this player."

def build_availability_table(gb, snaps):
    names = []
    for _, r in gb.iterrows():
        for part in str(r.named_tackler_or_pass_defender).split(";"):
            if part.strip():
                names.append(part.strip())
        if r.named_interception:
            names.append(str(r.named_interception).strip())
        for part in str(r.named_qb_hit_brackets).split(";"):
            if part.strip():
                names.append(part.strip())
    uniq = list(dict.fromkeys(names))
    official = gb[gb.official_target]
    rows = []
    for abbr in uniq:
        if abbr not in NAME_MAP:
            continue  # skip offensive players (e.g. return tackler D.Mooney on a nullified INT)
        full = NAME_MAP[abbr]
        n_nab = int(((official.target=="Malik Nabers") & official.named_tackler_or_pass_defender.fillna("").str.contains(re.escape(abbr))).sum())
        n_lik = int(((official.target=="Isaiah Likely") & official.named_tackler_or_pass_defender.fillna("").str.contains(re.escape(abbr))).sum())
        act, inj = _status(full)
        rows.append({
            "defender_abbr": abbr, "defender_full": full,
            "appeared_on_week5_nabers_likely_gamebook_credits": True,
            "official_nabers_targets_named_in_parentheses": n_nab,
            "official_likely_targets_named_in_parentheses": n_lik,
            "official_combined_paren_credits": n_nab + n_lik,
            "interception_credits_including_no_play": int((gb.named_interception == abbr).sum()),
            "qb_hit_bracket_credits": int(gb.named_qb_hit_brackets.fillna("").str.contains(re.escape(abbr)).sum()),
            "week5_def_snap_pct": snap_pct(snaps, full, 5),
            "week8_def_snap_pct": snap_pct(snaps, full, 8),
            "week9_def_snap_pct": snap_pct(snaps, full, 9),
            "active_now_as_of_nov10": act,
            "injury_or_ir_as_of_nov10": inj,
            "current_role": ROLE_NOW.get(full, ""),
            "credit_is_not_coverage_assignment": True,
            "note": "Week 5 Washington secondary is not the current one. Cross and Amos were not in this game. Douglas and Martin were every-down that day and are not every-down now. Robertson is the main every-down overlap.",
        })
    return pd.DataFrame(rows).sort_values("official_combined_paren_credits", ascending=False)

def coverage_sources_table():
    rows = [
        {"source":"nflverse pbp_participation_2026","as_of":"Checked 2026-11-10 vs https://github.com/nflverse/nflverse-data/releases/tag/pbp_participation","status":"DOES NOT EXIST. Release has files through 2025 only (pbp_participation_2025 last updated 2026-02-10). No play-level defense_coverage_type or defense_man_zone_type.","was_figure":"","used_as":"gap"},
        {"source":"nflverse ftn_charting_2026.parquet","as_of":"Release updated 2026-11-10 12:14 UTC; date_pulled max 2026-11-10 12:14:09 UTC; Weeks 1-9, all 8 WAS games (1,394 rows)","status":"EXISTS through Week 9, but public columns have no coverage shell or man/zone. Has n_blitzers, n_pass_rushers, n_defense_box, motion/play-action/screen flags only.","was_figure":"Used only for weekly pass-rush/blitz/box counts.","used_as":"rush/blitz/box proxy only"},
        {"source":"NFL Savant WAS defense / situational","as_of":"Fetched 2026-11-10 in /workspace/nfl_savant_nyg_was_2026-11-10/","status":"identity_coverage_participation=False. Situational feed coverage_participation=False, empty top_coverage arrays.","was_figure":"Season-level only: sack rate 5.43% (23rd); pressure 15.0% (22nd) on one field and 18.6% on dst_prs_pct — do not treat those as the same metric. Pass yards allowed 256.0 YPG (28th).","used_as":"season pressure/sack context; not weekly coverage"},
        {"source":"Sharp Football Analysis, NFL Coverage Scheme Stats","as_of":"Updated November 3, 2026 (2026-11-03T09:29:56-05:00). Through Week 8; Week 9 vs LAR (Nov 8) is after this update. https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/","status":"Published season totals. No weekly table.","was_figure":"WAS: man 12.2%, zone 78.4%, middle closed (MOFC) 32.1%, middle open (MOFO) 61.0%. Man+zone=90.6% (remainder unclassified on that table). High-MOFO, low-man group.","used_as":"best public season MOFC/MOFO and man/zone rates before Week 9"},
        {"source":"Sharp Football Analysis, positional coverage","as_of":"Updated November 3, 2026","status":"Season totals through the Nov 3 update (not including Week 9).","was_figure":"WAS allowed 7.8 YPT to WRs, 9.4 YPT to TEs, 5.1 YPT to RBs, 9.1 YPT outside, 6.6 YPT in the slot.","used_as":"season positional context, pre-Week 9"},
        {"source":"StatRankings CoverageIQ, WAS team page","as_of":"Fetched 2026-11-10. Live page; 313 coverage snaps vs WR. https://statrankings.com/nfl/coverage/team/was","status":"Season rates. Page is labeled pass defense vs WR, not all coverage snaps, so rates can differ from Sharp. Split tables did not render numeric cells in the fetch.","was_figure":"Man 17.9% (32nd), zone 81.8% (1st), single-high 38.2% (31st), two-high 61.8% (2nd), blitz 44.4% (3rd).","used_as":"current season two-high/zone lean, including Week 9; note vs-WR scope"},
        {"source":"StatRankings Zone Coverage Rate","as_of":"Last updated 11/10/26; prose through games played November 10, 2026","status":"HTML table did not print team names in the fetch; prose identifies Washington as #1 at 81.8%, matching the rank-1 row and CoverageIQ.","was_figure":"WAS #1 zone 81.8%; last 1 77.3%; last 3 86.0%; last 5 80.1%; home 79.2%; away 88.0%; 2025 was 69.2%. Last 1 = Week 9 vs LAR. Last 3 = Weeks 6, 8, 9. Last 5 = Weeks 4-6 and 8-9.","used_as":"only public near-weekly zone split found"},
        {"source":"StatRankings Two High Rate","as_of":"Last updated 11/10/26. Two high = Cover 2, Cover 4, and Cover 6 family.","status":"Same caveat on missing table team names; prose says Washington is second at 61.8%, matching CoverageIQ.","was_figure":"WAS #2 two-high 61.8%; last 1 61.0%; last 3 59.1%; last 5 55.7%; home 58.3%; away 69.7%.","used_as":"only public near-weekly two-high split found"},
        {"source":"StatRankings Cover 4 (Quarters) Rate","as_of":"Last updated 11/10/26","status":"Prose identifies Washington as third at 14.1%. That is well below the 61.8% two-high rate, so most two-high snaps are not Cover 4.","was_figure":"WAS #3 Cover 4 14.1%; last 1 4.5%; last 3 15.8%; last 5 15.5%. A preseason Hogs Haven preview expected a Cover-4-heavy look; the midseason public rate does not show that.","used_as":"season Cover 4 context; Cover 2/3/6 named rows were not obtained"},
        {"source":"ESPN offseason feature, story id 48913350","as_of":"Offseason 2026. Not a midseason chart.","status":"Qualitative preview: Jones's defense would play much more zone than the Quinn/Whitt years.","was_figure":"Preview only.","used_as":"scheme context, clearly preseason"},
        {"source":"Hogs Haven 2026 secondary / Jones preview","as_of":"Preseason scheme preview, not midseason charting","status":"Projected a Flores-tree two-high mix (Cover 4/2/0). Used 2025 Vikings Sharp rates, not WAS 2026 rates.","was_figure":"n/a (preview)","used_as":"scheme context only; do not treat as 2026 rates"},
        {"source":"Public NGS (nextgenstats.nfl.com)","as_of":"Searched 2026-11-10","status":"No public NGS page was found that publishes WAS 2026 man/zone or MOFC/MOFO rates in a usable table.","was_figure":"","used_as":"gap"},
    ]
    return pd.DataFrame(rows)

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pbp = pd.read_parquet(PBP_PATH)
    ftn = pd.read_parquet(FTN_PATH)
    tw = pd.read_csv(TEAM_WEEK, low_memory=False)
    pw = pd.read_csv(PLAYER_WEEK, low_memory=False)
    snaps = pd.read_csv(SNAPS_WIDE)
    official = official_allowed(tw)
    pbp_was = pbp_pass_defense(pbp)
    ftn_j = ftn_for_was(ftn, pbp_was)
    pos_tgt = position_allowed(pbp_was, pw)
    games = summarize_games(pbp_was, official, ftn_j, pos_tgt, snaps)
    eras = summarize_eras(games)
    pos_game = position_by_game(pos_tgt)
    era_map = {1:"early_sainristil_nickel_w1_2",2:"early_sainristil_nickel_w1_2",3:"transition_w3_6",4:"transition_w3_6",5:"transition_w3_6",6:"transition_w3_6",8:"amos_robertson_w8_9",9:"amos_robertson_w8_9"}
    pos_era = (pos_game.assign(era=lambda d: d.week.map(lambda w: era_map[int(w)]))
               .groupby(["era","position_group"], as_index=False)
               .agg(targets=("targets","sum"), receptions=("receptions","sum"), yards=("yards","sum"), tds=("tds","sum"), explosive_rec_20plus=("explosive_rec_20plus","sum")))
    pos_era["ypa_on_targets"] = (pos_era.yards / pos_era.targets).round(2)
    phi_cols = ["week","game_id","opponent","home_away","result","secondary_era","official_cmp","official_att","official_cmp_pct","official_pass_yds_gross","official_pass_tds","official_int","official_ypa_gross","official_sacks","official_qb_hits","official_completions_20plus","pbp_epa_per_dropback","wr_rec_allowed","wr_yds_allowed","wr_td_allowed","te_rec_allowed","te_yds_allowed","te_td_allowed"]
    phi = games[games.week.isin([1,8])][phi_cols]
    ftn_game = games[["week","game_id","opponent","secondary_era","pbp_dropbacks","ftn_dropbacks_matched","ftn_mean_pass_rushers","ftn_mean_blitzers","ftn_pct_dropbacks_blitzers_ge1","ftn_pct_dropbacks_rushers_ge5","ftn_mean_defenders_in_box_on_dropbacks","official_sacks","official_qb_hits","weekly_true_pressures"]]
    gb = nabers_likely_from_gamebook(parse_gamebook_plays(GB_TXT.read_text(errors="replace")))
    pbp_t = pbp_targets_week5(pbp)
    xw = crosswalk(gb, pbp_t)
    counts = defender_counts(gb)
    avail = build_availability_table(gb, snaps)
    cov = coverage_sources_table()
    lineups = pd.DataFrame([
        {"team":"WAS","unit":"defense","role":"starter","player":n,"pos":p,"source":"Week 5 official gamebook starting defense"}
        for n,p in [("K'Lavon Chaisson","OLB"),("Daron Payne","DT"),("Tim Settle","DT"),("Javon Kinlaw","DT"),("Odafe Oweh","OLB"),("Sonny Styles","LB"),("Frankie Luvu","LB"),("Rasul Douglas","CB"),("Amik Robertson","CB"),("Jeremy Reaves","S"),("Quan Martin","S")]
    ] + [
        {"team":"WAS","unit":"defense","role":"not_active","player":"Nick Cross","pos":"S","source":"Week 5 official gamebook Not Active (illness; missed Weeks 3-5)"},
        {"team":"WAS","unit":"defense","role":"not_on_gamebook / reserve","player":"Trey Amos","pos":"CB","source":"On reserve Weeks 1-5; not in this gamebook"},
        {"team":"WAS","unit":"defense","role":"not_active","player":"Percy Butler","pos":"S","source":"Week 5 official gamebook Not Active"},
        {"team":"WAS","unit":"defense","role":"not_active","player":"Charles Omenihu","pos":"DE","source":"Week 5 official gamebook Not Active"},
        {"team":"WAS","unit":"defense","role":"substitution","player":"Mike Sainristil","pos":"CB","source":"Week 5 substitutions; 48% defensive snaps. Not named on Nabers/Likely official targets."},
        {"team":"WAS","unit":"defense","role":"substitution","player":"Fabian Moreau","pos":"CB","source":"Week 5 substitutions; 29% defensive snaps. Named on several Nabers targets."},
    ])
    gaps = pd.DataFrame([
        {"gap":"No pbp_participation_2026","detail":"nflverse-data participation release has no 2026 asset (through 2025 only, updated 2026-02-10)."},
        {"gap":"FTN 2026 has no coverage-type column","detail":"ftn_charting_2026.parquet through Week 9 has rushers/blitzers/box, not defense_coverage_type."},
        {"gap":"NFL Savant coverage participation false","detail":"Team and situational WAS defense pages expose no coverage assignments for 2026."},
        {"gap":"No public NGS coverage rates used","detail":"No usable public NGS man/zone or MOFC/MOFO table for WAS 2026 was included."},
        {"gap":"No weekly official coverage mix","detail":"Sharp is season-level through Nov 3 (Week 8). StatRankings last-1/3/5 is the only near-weekly public split; table fetches omitted team names and were matched via prose."},
        {"gap":"Week 5 credits are not coverage assignments","detail":"Gamebook parentheses and nflverse tackle/pass_defense fields are official credits only."},
        {"gap":"No Week 10 injury report in nflverse","detail":"File goes through Week 9. Thursday inactives are not posted. Moreau's availability is uncertain. Tuttle Q-tag is from ESPN Nov 9-10 screenshots."},
        {"gap":"No weekly true pressures","detail":"Public PBP has sacks and QB hits only. Savant pressure is season-level and internally inconsistent (15.0% vs 18.6%)."},
        {"gap":"Week 5 gamebook not in nfl-matchup-database","detail":"Repo main has Week 9 gamebooks only. Week 5 PDF was downloaded from NFL.com Game Center."},
        {"gap":"Amos and Cross have no Week 5 Nabers/Likely credits","detail":"They did not play in Week 5, so this game cannot describe how they match up with those receivers."},
    ])
    games.to_csv(OUT/"was_pass_def_allowed_by_game.csv", index=False)
    eras.to_csv(OUT/"was_pass_def_allowed_by_era.csv", index=False)
    pos_game.to_csv(OUT/"was_pass_def_allowed_by_position_game.csv", index=False)
    pos_era.to_csv(OUT/"was_pass_def_allowed_by_position_era.csv", index=False)
    phi.to_csv(OUT/"was_pass_def_phi_w1_vs_w8.csv", index=False)
    ftn_game.to_csv(OUT/"ftn_pass_rush_blitz_by_game.csv", index=False)
    cov.to_csv(OUT/"coverage_shell_sources.csv", index=False)
    gb.to_csv(OUT/"week5_nabers_likely_targets_gamebook.csv", index=False)
    pbp_t.to_csv(OUT/"week5_nabers_likely_targets_pbp.csv", index=False)
    xw.to_csv(OUT/"week5_nabers_likely_targets_crosswalk.csv", index=False)
    counts.to_csv(OUT/"week5_named_defender_counts.csv", index=False)
    avail.to_csv(OUT/"week5_named_defenders_availability.csv", index=False)
    lineups.to_csv(OUT/"week5_gamebook_lineups_defense.csv", index=False)
    gaps.to_csv(OUT/"gaps.csv", index=False)
    (OUT/"_qa_summary.json").write_text(json.dumps({
        "gamebook_official": gb[gb.official_target].groupby("target").agg(targets=("official_target","sum"), rec=("complete","sum"), yds=("yards","sum"), td=("touchdown","sum")).reset_index().to_dict("records"),
        "no_plays": gb[gb.no_play][["target","result","clock","quarter"]].to_dict("records"),
        "unmatched_crosswalk": int((~xw.matched_pbp).sum()),
        "crosswalk_n": int(len(xw)),
        "games_weeks": [int(w) for w in games.week],
        "era": eras[["era","games","official_cmp","official_att","official_pass_yds_gross","official_ypa_gross","pbp_epa_per_dropback"]].to_dict("records"),
        "nabers_plays": int((gb.target=="Malik Nabers").sum()),
        "likely_plays": int((gb.target=="Isaiah Likely").sum()),
    }, indent=2, default=str))
    prov = {
        "created_et": ASOF_ET, "research_only": True, "projection_ready_unchanged": True,
        "game": "2026 Week 10 TNF, WAS at NYG, kickoff Thursday Nov 12, 2026",
        "sources": {
            "nflverse_pbp": {"path": str(PBP_PATH), "sha256": sha256(PBP_PATH), "release": "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet", "updated_utc": "2026-11-10T13:45:24Z", "weeks": "1-9"},
            "nflverse_ftn": {"path": str(FTN_PATH), "sha256": sha256(FTN_PATH), "release": "https://github.com/nflverse/nflverse-data/releases/download/ftn_charting/ftn_charting_2026.parquet", "updated_utc": "2026-11-10T12:14:16Z"},
            "week5_gamebook_pdf": {"path": str(GB_PDF), "sha256": sha256(GB_PDF), "url": "https://static.www.nfl.com/gamecenter/aa94b906-4feb-11f1-abca-2c54536568a9.pdf", "game_center": "https://www.nfl.com/games/giants-at-commanders-2026-reg-5", "pages": 23},
            "pbp_participation_2026": "not published as of 2026-11-10",
        },
    }
    (OUT/"provenance.json").write_text(json.dumps(prov, indent=2))
    print(open(OUT/"_qa_summary.json").read())

if __name__ == "__main__":
    main()
