"""Per-team, per-defender coverage profiles for all 32 NFL defenses (2026). Research only.

    python3 data/coverage/defender_profiles_2026/build.py --raw <dir> [--through-week N]

Inputs (all free/public; see SOURCES.md and MANIFEST.json for URLs, pull times and sha256):
  nflverse play_by_play_2026, advstats_week_def_2026 (PFR weekly advanced defense), snap_counts_2026,
  roster_weekly_2026, ngs_receiving (NFL Next Gen Stats via nflverse), ftn_charting_2026 (via nflverse),
  Sharp Football Analysis public tables (coverage schemes, defensive tendencies, coverage stats by position),
  StatRankings CoverageIQ public team-page chips.

--through-week N keeps only games with week <= N in every nflverse-derived table (leak-free backtests).
Sharp and StatRankings are season snapshots with no week filter: they are only leak-free for games played after
their as-of date (written into every row).

Nothing here is a coverage ASSIGNMENT. Labels:
  PFR_charted   targets/yards charged by PFR charters to the nearest defender (nflverse pfr_advstats weekly)
  verified      defender named in pbp as PBU (pass_defense_*), interceptor, or flagged for DPI
  inferred      defender named only as the tackler after a catch (or pushed out of bounds in play text)
Slot vs outside alignment per defender: MISSING (no free per-defender source). Team-level outside/slot YPT is from Sharp.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
TEAMS = ["ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE", "DAL", "DEN", "DET", "GB", "HOU", "IND", "JAX", "KC",
         "LA", "LAC", "LV", "MIA", "MIN", "NE", "NO", "NYG", "NYJ", "PHI", "PIT", "SEA", "SF", "TB", "TEN", "WAS"]
SHARP_NAME = {"Arizona Cardinals": "ARI", "Atlanta Falcons": "ATL", "Baltimore Ravens": "BAL", "Buffalo Bills": "BUF",
              "Carolina Panthers": "CAR", "Chicago Bears": "CHI", "Cincinnati Bengals": "CIN", "Cleveland Browns": "CLE",
              "Dallas Cowboys": "DAL", "Denver Broncos": "DEN", "Detroit Lions": "DET", "Green Bay Packers": "GB",
              "Houston Texans": "HOU", "Indianapolis Colts": "IND", "Jacksonville Jaguars": "JAX", "Kansas City Chiefs": "KC",
              "Los Angeles Rams": "LA", "Los Angeles Chargers": "LAC", "Las Vegas Raiders": "LV", "Miami Dolphins": "MIA",
              "Minnesota Vikings": "MIN", "New England Patriots": "NE", "New Orleans Saints": "NO", "New York Giants": "NYG",
              "New York Jets": "NYJ", "Philadelphia Eagles": "PHI", "Pittsburgh Steelers": "PIT", "Seattle Seahawks": "SEA",
              "San Francisco 49ers": "SF", "Tampa Bay Buccaneers": "TB", "Tennessee Titans": "TEN", "Washington Commanders": "WAS"}
SR_CODE = {"LAR": "LA"}
COVER_POS = {"CB": "CB", "S": "S", "SS": "S", "FS": "S", "SAF": "S", "DB": "DB", "LB": "LB", "ILB": "LB", "OLB": "LB", "MLB": "LB"}


def r(x, d=1):
    if x is None:
        return None
    try:
        x = float(x)
    except (TypeError, ValueError):
        return None
    return None if not np.isfinite(x) else round(x, d)


def passer_rating(att, cmp_, yds, td, ints):
    """NFL passer rating formula, computed from summed PFR-charted totals (label: computed)."""
    if not att:
        return None
    a = min(max((cmp_ / att - 0.3) * 5, 0), 2.375)
    b = min(max((yds / att - 3) * 0.25, 0), 2.375)
    c = min(max(td / att * 20, 0), 2.375)
    d = min(max(2.375 - ints / att * 25, 0), 2.375)
    return round((a + b + c + d) / 6 * 100, 1)


def load(raw: Path, through: int | None):
    p = pd.read_parquet(raw / "play_by_play_2026.parquet")
    p = p[(p.season_type == "REG")]
    a = pd.read_parquet(raw / "advstats_week_def_2026.parquet")
    a = a[a.game_type == "REG"]
    s = pd.read_parquet(raw / "snap_counts_2026.parquet")
    s = s[s.game_type == "REG"]
    ro = pd.read_parquet(raw / "roster_weekly_2026.parquet")
    ngs = pd.read_parquet(raw / "ngs_receiving.parquet")
    ngs = ngs[(ngs.season == 2026) & (ngs.season_type == "REG") & (ngs.week > 0)]
    ftn = pd.read_parquet(raw / "ftn_charting_2026.parquet")
    if through:
        p, a, s, ro, ngs, ftn = (x[x.week <= through] for x in (p, a, s, ro, ngs, ftn))
    return p, a, s, ro, ngs, ftn


def id_maps(ro: pd.DataFrame, s: pd.DataFrame):
    ro = ro.sort_values("week")
    last = ro.dropna(subset=["gsis_id"]).groupby("gsis_id").last()
    pos_snap = s.sort_values("week").groupby("pfr_player_id").position.last()
    pfr2gsis = ro.dropna(subset=["pfr_id", "gsis_id"]).groupby("pfr_id").gsis_id.last()
    gsis2pfr = ro.dropna(subset=["pfr_id", "gsis_id"]).groupby("gsis_id").pfr_id.last()

    def cover_pos(gsis):
        pfr = gsis2pfr.get(gsis)
        sp = pos_snap.get(pfr) if pfr is not None else None
        if sp in COVER_POS:
            return COVER_POS[sp]
        if gsis in last.index:
            dc = last.loc[gsis, "depth_chart_position"]
            if dc in COVER_POS:
                return COVER_POS[dc]
            return COVER_POS.get(last.loc[gsis, "position"], last.loc[gsis, "position"])
        return None

    off_pos = last.position.to_dict()
    names = last.full_name.to_dict()
    return cover_pos, off_pos, names, pfr2gsis, gsis2pfr, pos_snap


def target_plays(p: pd.DataFrame, off_pos: dict) -> pd.DataFrame:
    t = p[(p.pass_attempt == 1) & (p.sack != 1) & (p.two_point_attempt != 1) & p.receiver_player_id.notna()].copy()
    t["yds"] = t.receiving_yards.fillna(0)
    t["rpos"] = t.receiver_player_id.map(off_pos).replace({"FB": "RB", "HB": "RB"})
    t["zone"] = t.pass_length.fillna("unk") + "_" + t.pass_location.fillna("unk")
    t["td"] = (t.pass_touchdown == 1).astype(int)
    t["cmp"] = (t.complete_pass == 1).astype(int)
    t["int"] = (t.interception == 1).astype(int)
    return t


def defender_links(p: pd.DataFrame, t: pd.DataFrame, off_pos: dict | None = None) -> pd.DataFrame:
    """One row per (play, defender) link with verified/inferred label."""
    rows = []
    cols = ["game_id", "week", "play_id", "defteam", "posteam", "qtr", "time", "receiver_player_id", "receiver_player_name",
            "rpos", "cmp", "yds", "td", "int", "air_yards", "zone", "desc"]
    base = t[cols]
    for c, kind in (("pass_defense_1_player", "PBU"), ("pass_defense_2_player", "PBU"), ("interception_player", "INT")):
        m = t[f"{c}_id"].notna()
        if kind == "PBU":
            m &= t.interception != 1  # INT plays also list the interceptor as pass_defense; count once as INT
        x = base[m].copy()
        x["def_id"], x["def_name"], x["link"], x["label"] = t.loc[m, f"{c}_id"], t.loc[m, f"{c}_name"], kind, "verified"
        rows.append(x)
    # DPI: penalty plays are often not pass_attempt rows with a receiver, so take them from full pbp.
    d = p[(p.penalty_type == "Defensive Pass Interference") & p.penalty_player_id.notna() & (p.penalty_team == p.defteam)].copy()
    if len(d):
        # receiver: pbp field when present, else the "to X.Name" target in the play text
        named = d.desc.str.extract(r" to (?:\d+-)?([A-Z][A-Za-z]*\.[A-Za-z'\-\.]+?(?: (?:Jr|Sr|II|III)\.?)?)[\.,]? (?:PENALTY|\[|\()")[0]
        zl = d.desc.str.extract(r"pass (?:incomplete |complete )?(short|deep) (left|middle|right)")
        d["pass_length"] = d.pass_length.fillna(zl[0])
        d["pass_location"] = d.pass_location.fillna(zl[1])
        d["receiver_player_name"] = d.receiver_player_name.fillna(named)
        d["rpos"] = d.receiver_player_id.map(off_pos) if off_pos else None
        d["cmp"], d["td"], d["int"] = 0, 0, 0
        d["yds"] = d.penalty_yards
        d["zone"] = d.pass_length.fillna("unk") + "_" + d.pass_location.fillna("unk")
        x = d[cols].copy()
        x["def_id"], x["def_name"], x["link"], x["label"] = d.penalty_player_id, d.penalty_player_name, "DPI", "verified"
        rows.append(x)
    # inferred: first tackler on a completion
    c = t[t.cmp == 1]
    tk = c[["solo_tackle_1_player_id", "tackle_with_assist_1_player_id", "assist_tackle_1_player_id"]].bfill(axis=1).iloc[:, 0]
    tn = c[["solo_tackle_1_player_name", "tackle_with_assist_1_player_name", "assist_tackle_1_player_name"]].bfill(axis=1).iloc[:, 0]
    m = tk.notna()
    x = base.loc[c.index[m]].copy()
    x["def_id"], x["def_name"], x["link"], x["label"] = tk[m], tn[m], "TACKLE_AFTER_CATCH", "inferred"
    rows.append(x)
    out = pd.concat(rows, ignore_index=True)
    out["explosive20"] = ((out.cmp == 1) & (out.yds >= 20)).astype(int)
    return out


def team_tables(t: pd.DataFrame, games: pd.DataFrame):
    g = games.groupby("defteam").game_id.nunique()
    pos = t[t.rpos.isin(["WR", "TE", "RB"])].groupby(["defteam", "rpos"]).agg(
        tgt=("play_id", "size"), rec=("cmp", "sum"), yds=("yds", "sum"), td=("td", "sum"), ints=("int", "sum"),
        epa=("epa", "mean")).reset_index()
    pos["games"] = pos.defteam.map(g)
    pos["ypt"] = (pos.yds / pos.tgt).round(2)
    pos["yds_pg"] = (pos.yds / pos.games).round(1)
    pos["tgt_pg"] = (pos.tgt / pos.games).round(1)
    pos["epa_per_tgt"] = pos.epa.round(3)
    pos = pos.drop(columns="epa")
    pos["yds_pg_rank_most_allowed"] = pos.groupby("rpos").yds_pg.rank(ascending=False, method="min").astype(int)
    pos["ypt_rank_most_allowed"] = pos.groupby("rpos").ypt.rank(ascending=False, method="min").astype(int)

    z = t[t.pass_length.notna() & t.pass_location.notna()]
    zone = z.groupby(["defteam", "pass_length", "pass_location"]).agg(
        tgt=("play_id", "size"), rec=("cmp", "sum"), yds=("yds", "sum"), td=("td", "sum"), ints=("int", "sum"),
        epa=("epa", "mean")).reset_index()
    lg = z.groupby(["pass_length", "pass_location"]).agg(lg_yds=("yds", "sum"), lg_tgt=("play_id", "size"), lg_epa=("epa", "mean")).reset_index()
    zone = zone.merge(lg, on=["pass_length", "pass_location"])
    zone["ypt"] = (zone.yds / zone.tgt).round(2)
    zone["lg_ypt"] = (zone.lg_yds / zone.lg_tgt).round(2)
    zone["ypt_vs_lg"] = (zone.ypt - zone.lg_ypt).round(2)
    zone["epa_per_tgt"] = zone.epa.round(3)
    zone["lg_epa_per_tgt"] = zone.lg_epa.round(3)
    zone = zone.drop(columns=["epa", "lg_epa", "lg_yds", "lg_tgt"])
    zone["share_of_team_tgts"] = (zone.tgt / zone.groupby("defteam").tgt.transform("sum")).round(3)
    zone["ypt_rank_most_allowed"] = zone.groupby(["pass_length", "pass_location"]).ypt.rank(ascending=False, method="min").astype(int)
    zone["weak_zone_flag"] = (zone.ypt_rank_most_allowed <= 8) & (zone.tgt >= 12)
    return pos, zone


def ngs_separation(ngs: pd.DataFrame, p: pd.DataFrame):
    """Target-weighted avg separation/cushion of NGS-qualified receivers in games vs each defense (proxy, receiver-level)."""
    sched = p.groupby(["week", "posteam"]).defteam.first().reset_index().rename(columns={"posteam": "team_abbr", "defteam": "opp"})
    n = ngs.merge(sched, on=["week", "team_abbr"], how="left").dropna(subset=["opp"])
    n = n[n.targets > 0]
    agg = n.groupby("opp").apply(lambda x: pd.Series({
        "ngs_receiver_games": len(x), "ngs_targets": int(x.targets.sum()),
        "sep_allowed_tw": np.average(x.avg_separation, weights=x.targets),
        "cushion_tw": np.average(x.avg_cushion, weights=x.targets),
        "wr_sep_allowed_tw": np.average(x[x.player_position == "WR"].avg_separation, weights=x[x.player_position == "WR"].targets) if (x.player_position == "WR").any() else np.nan,
        "te_sep_allowed_tw": np.average(x[x.player_position == "TE"].avg_separation, weights=x[x.player_position == "TE"].targets) if (x.player_position == "TE").any() else np.nan,
        "last_week": int(x.week.max())}), include_groups=False).reset_index().rename(columns={"opp": "team"})
    lg = np.average(n.avg_separation, weights=n.targets)
    agg["lg_sep_tw"] = round(lg, 2)
    for c in ("sep_allowed_tw", "cushion_tw", "wr_sep_allowed_tw", "te_sep_allowed_tw"):
        agg[c] = agg[c].round(2)
    agg["sep_rank_most_allowed"] = agg.sep_allowed_tw.rank(ascending=False, method="min").astype(int)
    return agg


def scheme_table(raw: Path, ftn: pd.DataFrame, p: pd.DataFrame, meta: dict):
    sh = {}
    for page in ("nfl-coverage-schemes", "nfl-defensive-tendencies", "nfl-coverage-stats-by-position"):
        df = pd.read_html(raw / f"sharp_{page}.html")[0]
        df["team"] = df.Team.map(SHARP_NAME)
        sh[page] = df.drop(columns="Team").set_index("team")
    s = sh["nfl-coverage-schemes"].join(sh["nfl-defensive-tendencies"]).join(sh["nfl-coverage-stats-by-position"])
    s.columns = ["sharp_" + re.sub(r"[^a-z]+", "_", c.lower()).strip("_") for c in s.columns]
    sr = pd.read_csv(raw / "statrankings_team_cov.csv")
    sr["team"] = sr.team.replace(SR_CODE)
    sr = sr.set_index("team")[["cov_snaps", "man", "zone", "single_high", "two_high", "blitz"]].add_prefix("sr_")
    # FTN charting (via nflverse): share of dropbacks with >=1 blitzer; defteam from pbp join
    f = ftn.merge(p[["game_id", "play_id", "defteam", "qb_dropback"]], left_on=["nflverse_game_id", "nflverse_play_id"],
                  right_on=["game_id", "play_id"], how="inner")
    f = f[f.qb_dropback == 1]
    fb = f.groupby("defteam").agg(ftn_dropbacks=("play_id", "size"), ftn_blitz_pct=("n_blitzers", lambda x: round(100 * (x > 0).mean(), 1)),
                                   ftn_avg_rushers=("n_pass_rushers", lambda x: round(x.mean(), 2)), ftn_last_week=("week", "max"))
    out = s.join(sr, how="outer").join(fb, how="outer").reset_index().rename(columns={"index": "team"})
    out["man_conflict_pts"] = (out.sharp_man_rate - out.sr_man).round(1)
    out["blitz_conflict_pts"] = (out.sharp_blitz_rate - out.sr_blitz).round(1)
    # Sharp man rates run systematically lower than StatRankings (different charting), so raw-point gaps flag almost
    # every team. The conflict flag compares league RANKS instead (1 = most man / most blitz); raw gaps kept for reference.
    for a_, b_, n_ in (("sharp_man_rate", "sr_man", "man"), ("sharp_blitz_rate", "sr_blitz", "blitz")):
        out[f"sharp_{n_}_rank"] = out[a_].rank(ascending=False, method="min")
        out[f"sr_{n_}_rank"] = out[b_].rank(ascending=False, method="min")
        out[f"{n_}_rank_gap"] = (out[f"sharp_{n_}_rank"] - out[f"sr_{n_}_rank"]).abs()
    out["source_conflict_flag"] = (out.man_rank_gap >= 8) | (out.blitz_rank_gap >= 8)
    for k, v in meta.items():
        out[k] = v
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True, type=Path)
    ap.add_argument("--through-week", type=int)
    ap.add_argument("--out", type=Path, default=HERE)
    args = ap.parse_args()
    raw, out = args.raw, args.out
    out.mkdir(parents=True, exist_ok=True)
    pulls = json.loads((raw / "PULLS.json").read_text())
    p, a, s, ro, ngs, ftn = load(raw, args.through_week)
    cover_pos, off_pos, names, pfr2gsis, gsis2pfr, pos_snap = id_maps(ro, s)
    pbp_last = p.groupby("week").game_date.max()
    stamp = {"through_week_pbp": int(p.week.max()), "last_game_date_pbp": str(p.game_date.max()),
             "through_week_pfr": int(a.week.max()), "through_week_ngs": int(ngs.week.max()), "through_week_ftn": int(ftn.week.max())}

    t = target_plays(p, off_pos)
    links = defender_links(p, t, off_pos)
    links["def_pos"] = links.def_id.map(cover_pos)
    links["def_full_name"] = links.def_id.map(names)
    links.sort_values(["week", "game_id", "play_id"]).to_csv(out / "defender_target_log_pbp.csv", index=False,
        columns=["week", "game_id", "play_id", "defteam", "posteam", "qtr", "time", "def_id", "def_name", "def_full_name", "def_pos",
                 "link", "label", "receiver_player_name", "rpos", "cmp", "yds", "td", "int", "explosive20", "air_yards", "zone", "desc"])

    # ---- per-defender (CB/S/DB + LB) ----
    s2 = s[s.position.isin(["CB", "S", "DB", "LB", "SS", "FS"]) & (s.defense_snaps > 0)]
    snaps = s2.groupby(["pfr_player_id", "team"]).agg(player=("player", "last"), snap_pos=("position", "last"), games=("game_id", "nunique"),
                                                     def_snaps=("defense_snaps", "sum"), avg_def_pct=("defense_pct", "mean"),
                                                     last_week=("week", "max")).reset_index()
    last_pct = s2.sort_values("week").groupby(["pfr_player_id", "team"]).defense_pct.last().rename("last_def_pct")
    snaps = snaps.join(last_pct, on=["pfr_player_id", "team"])
    for c in ("def_targets", "def_completions_allowed", "def_yards_allowed", "def_receiving_td_allowed", "def_ints", "def_air_yards_completed", "def_yards_after_catch"):
        a[c] = pd.to_numeric(a[c], errors="coerce").fillna(0)
    a["_adot_w"] = pd.to_numeric(a.def_adot, errors="coerce") * a.def_targets
    pf = a.groupby(["pfr_player_id", "team"]).agg(pfr_name=("pfr_player_name", "last"), pfr_games=("week", "nunique"), tgt=("def_targets", "sum"),
                                                 cmp=("def_completions_allowed", "sum"), yds=("def_yards_allowed", "sum"),
                                                 td=("def_receiving_td_allowed", "sum"), ints=("def_ints", "sum"),
                                                 air_yds_cmp=("def_air_yards_completed", "sum"), yac=("def_yards_after_catch", "sum"),
                                                 adot_w=("_adot_w", "sum"), pfr_last_week=("week", "max"),
                                                 g50=("def_yards_allowed", lambda x: int((x >= 50).sum())),
                                                 g70=("def_yards_allowed", lambda x: int((x >= 70).sum())),
                                                 worst_game_yds=("def_yards_allowed", "max")).reset_index()
    pf["cmp_pct"] = (100 * pf.cmp / pf.tgt).round(1)
    pf["ypt"] = (pf.yds / pf.tgt).round(2)
    pf["rating_allowed_computed"] = [passer_rating(*v) for v in pf[["tgt", "cmp", "yds", "td", "ints"]].itertuples(index=False)]
    pf["adot"] = (pf.adot_w / pf.tgt).round(1)
    pf = pf.drop(columns="adot_w")
    d = snaps.merge(pf, on=["pfr_player_id", "team"], how="outer")
    d["player"] = d.player.fillna(d.pfr_name)
    d["gsis_id"] = d.pfr_player_id.map(pfr2gsis)
    d["pos"] = d.snap_pos.map(COVER_POS).fillna(d.pfr_player_id.map(pos_snap).map(COVER_POS))
    d = d[d.pos.isin(["CB", "S", "DB", "LB"])]
    # pbp verified/inferred counts, by (gsis, defteam)
    lk = links.groupby(["def_id", "defteam"]).apply(lambda x: pd.Series({
        "pbu": int((x.link == "PBU").sum()), "int_pbp": int((x.link == "INT").sum()),
        "dpi": int((x.link == "DPI").sum()), "dpi_yds": int(x.loc[x.link == "DPI", "yds"].fillna(0).sum()),
        "tackle_after_catch": int((x.link == "TACKLE_AFTER_CATCH").sum()),
        "tac_yds": int(x.loc[x.link == "TACKLE_AFTER_CATCH", "yds"].sum()),
        "tac_explosive20": int(x.loc[x.link == "TACKLE_AFTER_CATCH", "explosive20"].sum()),
        "verified_plays": int((x.label == "verified").sum()),
        "receivers_linked": "; ".join(f"{k}x{v}" for k, v in x.receiver_player_name.dropna().value_counts().head(6).items())}),
        include_groups=False).reset_index().rename(columns={"def_id": "gsis_id", "defteam": "team"})
    d = d.merge(lk, on=["gsis_id", "team"], how="left")
    for c in ("pbu", "int_pbp", "dpi", "dpi_yds", "tackle_after_catch", "tac_yds", "tac_explosive20", "verified_plays"):
        d[c] = d[c].fillna(0).astype(int)
    d["alignment_slot_vs_outside"] = "MISSING"
    d["src_snaps"] = "nflverse snap_counts (PFR)"
    d["src_coverage"] = "PFR charted via nflverse pfr_advstats weekly; rating computed with NFL formula from summed totals"
    d["src_pbu_int_dpi"] = "nflverse pbp (verified)"
    d["src_tackle_after_catch"] = "nflverse pbp first tackler (inferred, not assignment)"
    d["pulled_utc"] = pulls["nflverse"]["pulled_utc"]
    for k, v in stamp.items():
        d[k] = v
    d["team"] = d.team.replace({"LAR": "LA"})
    d = d.sort_values(["team", "pos", "def_snaps"], ascending=[True, True, False])
    keep = ["team", "player", "pos", "pfr_player_id", "gsis_id", "games", "def_snaps", "avg_def_pct", "last_def_pct", "last_week",
            "pfr_games", "tgt", "cmp", "cmp_pct", "yds", "ypt", "td", "ints", "rating_allowed_computed", "adot", "air_yds_cmp", "yac",
            "g50", "g70", "worst_game_yds", "pfr_last_week", "pbu", "int_pbp", "dpi", "dpi_yds", "verified_plays", "tackle_after_catch",
            "tac_yds", "tac_explosive20", "receivers_linked", "alignment_slot_vs_outside", "src_snaps", "src_coverage",
            "src_pbu_int_dpi", "src_tackle_after_catch", "pulled_utc"] + list(stamp)
    d["avg_def_pct"] = (d.avg_def_pct * 100).round(1)
    d["last_def_pct"] = (d.last_def_pct * 100).round(1)
    d[keep].to_csv(out / "defenders_cb_s_lb.csv", index=False)

    # weekly defender log (PFR weekly + pbp verified per game)
    wk = a.copy()
    wk["gsis_id"] = wk.pfr_player_id.map(pfr2gsis)
    lw = links.groupby(["def_id", "game_id"]).apply(lambda x: pd.Series({
        "pbu": int((x.link == "PBU").sum()), "int_pbp": int((x.link == "INT").sum()), "dpi": int((x.link == "DPI").sum()),
        "tackle_after_catch": int((x.link == "TACKLE_AFTER_CATCH").sum()),
        "receivers_verified": "; ".join(sorted(set(x.loc[x.label == "verified", "receiver_player_name"].dropna()))),
        "receivers_inferred": "; ".join(sorted(set(x.loc[x.label == "inferred", "receiver_player_name"].dropna())))}),
        include_groups=False).reset_index().rename(columns={"def_id": "gsis_id"})
    wk = wk.merge(lw, on=["gsis_id", "game_id"], how="left")
    wk["pos"] = wk.pfr_player_id.map(pos_snap).map(COVER_POS)
    wk = wk[wk.pos.isin(["CB", "S", "DB", "LB"])]
    wk[["season", "week", "game_id", "team", "opponent", "pfr_player_name", "pos", "pfr_player_id", "gsis_id", "def_targets",
        "def_completions_allowed", "def_yards_allowed", "def_receiving_td_allowed", "def_ints", "def_passer_rating_allowed",
        "def_adot", "pbu", "int_pbp", "dpi", "tackle_after_catch", "receivers_verified", "receivers_inferred"]].sort_values(
        ["team", "pfr_player_name", "week"]).to_csv(out / "defender_weekly_log.csv", index=False)

    pos, zone = team_tables(t, t)
    pos.to_csv(out / "team_allowed_by_position.csv", index=False)
    zone.to_csv(out / "team_allowed_by_zone.csv", index=False)
    sep = ngs_separation(ngs, p)
    sep.to_csv(out / "team_ngs_separation_allowed.csv", index=False)
    sch = scheme_table(raw, ftn, p, {"sharp_as_of": pulls["sharp"]["as_of"], "sharp_pulled_utc": pulls["sharp"]["pulled_utc"],
                                     "sr_as_of": pulls["statrankings"]["as_of"], "sr_pulled_utc": pulls["statrankings"]["pulled_utc"]})
    sch.to_csv(out / "team_scheme_rates.csv", index=False)

    # ---- markdown profiles ----
    pdir = out / "profiles"
    pdir.mkdir(exist_ok=True)
    for tm in TEAMS:
        write_profile(pdir / f"{tm}.md", tm, d[d.team == tm], pos[pos.defteam == tm], zone[zone.defteam == tm],
                      sep[sep.team == tm], sch[sch.team == tm], links[(links.defteam == tm)], stamp, pulls)
    summary = {"teams": int(d.team.nunique()), "defenders_total": int(len(d)), "by_pos": d.pos.value_counts().to_dict(),
               "cb_s_db_with_pfr_targets": int(((d.pos != "LB") & (d.tgt > 0)).sum()),
               "cb_s_db_rows": int((d.pos != "LB").sum()), "links": links.label.value_counts().to_dict(),
               "links_by_type": links.link.value_counts().to_dict(), **stamp}
    (out / "BUILD_SUMMARY.json").write_text(json.dumps(summary, indent=1, default=int))
    print(json.dumps(summary, indent=1, default=int))


def fmt(v, d=1):
    return "—" if v is None or (isinstance(v, float) and not np.isfinite(v)) else (f"{v:.{d}f}" if isinstance(v, float) else str(v))


def write_profile(path, tm, d, pos, zone, sep, sch, links, stamp, pulls):
    L = [f"# {tm} defense — coverage profile (2026, research only)", "",
         f"Built from free/public sources. nflverse pbp through week {stamp['through_week_pbp']} (last game {stamp['last_game_date_pbp']}); "
         f"PFR charted coverage through week {stamp['through_week_pfr']}; NGS through week {stamp['through_week_ngs']}; FTN charting through week {stamp['through_week_ftn']}. "
         f"nflverse pulled {pulls['nflverse']['pulled_utc']}.", "",
         "Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. "
         "**inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).", ""]
    L += ["## Scheme rates (two charting sources; do not mix on one slip)", "",
          "| Metric | Sharp | StatRankings | FTN via nflverse |", "|---|---|---|---|"]
    if len(sch):
        x = sch.iloc[0]
        L += [f"| Man % | {fmt(x.get('sharp_man_rate'))} | {fmt(x.get('sr_man'))} | — |",
              f"| Zone % | {fmt(x.get('sharp_zone_rate'))} | {fmt(x.get('sr_zone'))} | — |",
              f"| Single-high / MOFC % | {fmt(x.get('sharp_middle_closed_rate'))} | {fmt(x.get('sr_single_high'))} | — |",
              f"| Two-high / MOFO % | {fmt(x.get('sharp_middle_open_rate'))} | {fmt(x.get('sr_two_high'))} | — |",
              f"| Blitz % | {fmt(x.get('sharp_blitz_rate'))} | {fmt(x.get('sr_blitz'))} | {fmt(x.get('ftn_blitz_pct'))} (dropbacks with 1+ blitzer, thru wk {fmt(x.get('ftn_last_week'),0)}) |",
              f"| Light / heavy box %, sub package % | {fmt(x.get('sharp_light_box_rate'))} / {fmt(x.get('sharp_heavy_box_rate'))}, {fmt(x.get('sharp_sub_package_rate'))} | — | — |",
              "", f"Sharp YPT allowed: WR {fmt(x.get('sharp_ypt_allowed_wr'))}, TE {fmt(x.get('sharp_ypt_allowed_te'))}, RB {fmt(x.get('sharp_ypt_allowed_rb'))}, "
              f"**outside {fmt(x.get('sharp_ypt_allowed_outside'))} vs slot {fmt(x.get('sharp_ypt_allowed_slot'))}** (team-level alignment split; the only free slot/outside number).",
              f"Sharp as of {pulls['sharp']['as_of']} (pulled {pulls['sharp']['pulled_utc']}); StatRankings as of {pulls['statrankings']['as_of']} (pulled {pulls['statrankings']['pulled_utc']}).",
              f"Source check: man rank Sharp #{fmt(x.get('sharp_man_rank'),0)} vs StatRankings #{fmt(x.get('sr_man_rank'),0)}; blitz rank Sharp #{fmt(x.get('sharp_blitz_rank'),0)} vs SR #{fmt(x.get('sr_blitz_rank'),0)} "
              f"(raw gaps: man {fmt(x.get('man_conflict_pts'))} pts, blitz {fmt(x.get('blitz_conflict_pts'))} pts; Sharp man % runs lower than SR league-wide)" +
              (" → **CONFLICT FLAG (rank gap ≥8)**" if bool(x.get("source_conflict_flag")) else " → ranks agree (gap <8)"), ""]
    L += ["## Allowed by receiver position (nflverse pbp)", "", "| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |", "|---|---|---|---|---|---|---|"]
    for _, x in pos.sort_values("rpos", ascending=False).iterrows():
        L.append(f"| {x.rpos} | {x.tgt_pg} | {x.yds_pg} | {x.ypt} | {int(x.td)} | {x.epa_per_tgt} | {int(x.yds_pg_rank_most_allowed)} |")
    L += ["", "## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)", "",
          "| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |", "|---|---|---|---|---|---|---|---|---|---|"]
    for _, x in zone.sort_values(["pass_length", "pass_location"]).iterrows():
        L.append(f"| {x.pass_length} {x.pass_location} | {int(x.tgt)} | {int(x.rec)} | {int(x.yds)} | {int(x.td)} | {int(x.ints)} | {x.ypt} | {x.lg_ypt} | {int(x.ypt_rank_most_allowed)} | {'**WEAK**' if x.weak_zone_flag else ''} |")
    L += ["", "Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.", ""]
    if len(sep):
        x = sep.iloc[0]
        L += ["## NGS separation allowed (proxy)", "",
              f"Target-weighted avg separation of NGS-qualified receivers vs {tm}: **{x.sep_allowed_tw} yds** (league {x.lg_sep_tw}; rank {x.sep_rank_most_allowed}/32 most allowed). "
              f"WR {fmt(x.wr_sep_allowed_tw,2)}, TE {fmt(x.te_sep_allowed_tw,2)}, cushion {x.cushion_tw}. Sample: {int(x.ngs_receiver_games)} receiver-games, {int(x.ngs_targets)} targets. "
              "NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.", ""]
    L += ["## Every CB and S (PFR charted + pbp verified/inferred)", "",
          "| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for _, x in d[d.pos != "LB"].iterrows():
        L.append(f"| {x.player} | {x.pos} | {fmt(x.games,0)} | {fmt(x.avg_def_pct)} ({fmt(x.last_def_pct)} wk{fmt(x.last_week,0)}) | {fmt(x.tgt,0)} | {fmt(x.cmp,0)} | {fmt(x.yds,0)} | {fmt(x.td,0)} | {fmt(x.ints,0)} | "
                 f"{fmt(x.ypt,2)} | {fmt(x.rating_allowed_computed)} | {fmt(x.adot)} | {fmt(x.g70,0)} | {x.pbu} | {x.dpi} | {x.verified_plays} | {x.tackle_after_catch} ({x.tac_yds}) | MISSING |")
    L += ["", "## Linebackers in coverage (PFR charted)", "", "| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |", "|---|---|---|---|---|---|---|---|---|"]
    for _, x in d[(d.pos == "LB") & (d.tgt.fillna(0) >= 10)].sort_values("tgt", ascending=False).iterrows():
        L.append(f"| {x.player} | {fmt(x.games,0)} | {fmt(x.tgt,0)} | {fmt(x.cmp,0)} | {fmt(x.yds,0)} | {fmt(x.td,0)} | {fmt(x.ypt,2)} | {fmt(x.rating_allowed_computed)} | {x.pbu} |")
    v = links[links.label == "verified"].sort_values(["week", "play_id"], ascending=False).head(15)
    L += ["", "## Most recent verified defender plays (pbp: PBU / INT / DPI)", "", "| Wk | Opp | Defender | Type | Receiver | Zone |", "|---|---|---|---|---|---|"]
    for _, x in v.iterrows():
        L.append(f"| {x.week} | {x.posteam} | {x.def_name} | {x.link} | {x.receiver_player_name if isinstance(x.receiver_player_name, str) else '—'} | {x.zone} |")
    L += ["", "Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.", ""]
    path.write_text("\n".join(L))


if __name__ == "__main__":
    main()
