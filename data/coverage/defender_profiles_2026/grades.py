"""Per-defender coverage QUALITY grades (every CB/S with 20+ charted targets) + team summary. Research only.

    python3 data/coverage/defender_profiles_2026/grades.py --raw <dir> [--through-week N] [--backtest]

Charted numbers: PFR weekly advanced defense via nflverse (targets, completions, yards, TDs, INTs charged to the nearest
defender). Verified plays: nflverse pbp PBU/INT. Snaps: PFR snap counts via nflverse (ALL defensive snaps; true coverage
snaps are not public, so yards per snap uses all defensive snaps). Supporting INFERRED column: v2 window-credit 20+.
Labels are thresholds on league percentiles within position (CB vs S), documented in GRADES.md.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

import build as B

HERE = Path(__file__).resolve().parent
MIN_TGT = 20
SMALL = 35


def load_all(raw: Path):
    p, a, s, ro, ngs, ftn = B.load(raw, None)
    cover_pos, off_pos, names, pfr2gsis, gsis2pfr, pos_snap = B.id_maps(ro, s)
    t = B.target_plays(p, off_pos)
    links = B.defender_links(p, t, off_pos)
    dc = ro.dropna(subset=["pfr_id"]).sort_values("week").groupby("pfr_id").depth_chart_position.last()
    return dict(p=p, a=a, s=s, t=t, links=links, pfr2gsis=pfr2gsis, pos_snap=pos_snap, dc=dc, off_pos=off_pos)


def pos_of(pid, D):
    sp = D["pos_snap"].get(pid)
    if sp in ("CB", "S"):
        return sp
    return {"CB": "CB", "SS": "S", "FS": "S", "S": "S", "NB": "CB"}.get(D["dc"].get(pid))


def grades(D, through: int | None = None, window_credit: pd.DataFrame | None = None):
    a = D["a"].copy()
    s = D["s"].copy()
    links = D["links"]
    through = through or int(a.week.max())  # keep pbp PBUs on the same window as PFR charting
    if through:
        a, s, links = a[a.week <= through], s[s.week <= through], links[links.week <= through]
    for c in ("def_targets", "def_completions_allowed", "def_yards_allowed", "def_receiving_td_allowed", "def_ints"):
        a[c] = pd.to_numeric(a[c], errors="coerce").fillna(0)
    a["pos"] = [pos_of(x, D) for x in a.pfr_player_id]
    db = a[a.pos.isin(["CB", "S"])].copy()
    sec = db.groupby(["game_id", "team"]).def_targets.sum().rename("sec_tgts")
    db = db.join(sec, on=["game_id", "team"])
    g = db.groupby(["pfr_player_id", "team"]).agg(player=("pfr_player_name", "last"), pos=("pos", "last"), games=("week", "nunique"),
                                                 tgt=("def_targets", "sum"), cmp=("def_completions_allowed", "sum"), yds=("def_yards_allowed", "sum"),
                                                 td=("def_receiving_td_allowed", "sum"), ints=("def_ints", "sum"), sec_tgts=("sec_tgts", "sum"),
                                                 last_week=("week", "max")).reset_index()
    g = g[g.tgt >= MIN_TGT].copy()
    g["team"] = g.team.replace({"LAR": "LA"})
    snaps = s.groupby("pfr_player_id").defense_snaps.sum()
    g["def_snaps"] = g.pfr_player_id.map(snaps)
    g["gsis_id"] = g.pfr_player_id.map(D["pfr2gsis"])
    v = links[links.label == "verified"]
    pbu = v[v.link == "PBU"].groupby("def_id").size()
    g["pbu_pbp"] = g.gsis_id.map(pbu).fillna(0).astype(int)
    tac20 = links[(links.link == "TACKLE_AFTER_CATCH") & (links.explosive20 == 1)].groupby("def_id").size()
    g["tackled_on_20plus_INFERRED"] = g.gsis_id.map(tac20).fillna(0).astype(int)
    g["target_share_secondary"] = (g.tgt / g.sec_tgts).round(3)
    g["catch_pct"] = (100 * g.cmp / g.tgt).round(1)
    g["ypt"] = (g.yds / g.tgt).round(2)
    g["yds_per_cmp"] = (g.yds / g.cmp.replace(0, np.nan)).round(2)
    g["yds_per_game"] = (g.yds / g.games).round(1)
    g["yds_per_def_snap"] = (g.yds / g.def_snaps).round(3)
    g["rating_allowed"] = [B.passer_rating(*x) for x in g[["tgt", "cmp", "yds", "td", "ints"]].itertuples(index=False)]
    g["plays_on_ball_rate"] = ((g.pbu_pbp + g.ints) / g.tgt).round(3)
    if window_credit is not None:
        w = window_credit.groupby("gsis_id").explosive20_credit.sum()
        g["window_credit_20plus_INFERRED"] = g.gsis_id.map(w).round(2)
    # percentiles within position; *_pctl_good: 100 = best coverage, 0 = worst
    for pos, idx in g.groupby("pos").groups.items():
        x = g.loc[idx]
        good = lambda col: ((1 - x[col].rank(pct=True)) * 100).round(0)
        g.loc[idx, "catch_pct_pctl_good"] = good("catch_pct")
        g.loc[idx, "ypt_pctl_good"] = good("ypt")
        g.loc[idx, "rating_pctl_good"] = good("rating_allowed")
        g.loc[idx, "yds_per_cmp_pctl_good"] = good("yds_per_cmp")
        g.loc[idx, "yds_per_game_pctl_good"] = good("yds_per_game")
        g.loc[idx, "target_share_pctl"] = (x.target_share_secondary.rank(pct=True) * 100).round(0)
        g.loc[idx, "ball_pctl"] = (x.plays_on_ball_rate.rank(pct=True) * 100).round(0)
    g["composite_good"] = g[["catch_pct_pctl_good", "ypt_pctl_good", "rating_pctl_good", "yds_per_game_pctl_good"]].mean(axis=1).round(1)
    labs = []
    for _, x in g.iterrows():
        L = []
        if x.rating_pctl_good >= 80 and x.ypt_pctl_good >= 70:
            L.append("LOCKDOWN")
        if x.catch_pct_pctl_good >= 70:
            L.append("LIMITS CATCHES")
        if x.ypt_pctl_good >= 70:
            L.append("LIMITS YARDS")
        if x.yds_per_cmp_pctl_good <= 25:
            L.append("GIVES UP EXPLOSIVES")
        if x.target_share_pctl >= 75 and x.yds_per_game_pctl_good <= 25:
            L.append("TARGET MAGNET")
        if x.rating_pctl_good <= 25 and x.ypt_pctl_good <= 30:
            L.append("WEAK LINK")
        labs.append(", ".join(L))
    g["labels"] = labs
    g["sample_note"] = np.where(g.tgt < SMALL, f"small sample (<{SMALL} tgts)", "")
    g["source"] = "PFR charted weekly via nflverse; PBU from nflverse pbp; *_INFERRED columns are model estimates"
    g["through_week"] = int(a.week.max())
    return g.sort_values(["team", "pos", "composite_good"], ascending=[True, True, False])


def team_summary(g, out_dir: Path):
    pos = pd.read_csv(out_dir / "team_allowed_by_position.csv")
    zone = pd.read_csv(out_dir / "team_allowed_by_zone.csv")
    rows = []
    for tm in sorted(set(pos.defteam)):
        x = g[g.team == tm]
        r = {"team": tm}
        for rp in ("WR", "TE", "RB"):
            q = pos[(pos.defteam == tm) & (pos.rpos == rp)]
            if len(q):
                r[f"{rp}_yds_pg"], r[f"{rp}_ypt"], r[f"{rp}_rank_most"] = q.yds_pg.iloc[0], q.ypt.iloc[0], int(q.yds_pg_rank_most_allowed.iloc[0])
        wz = zone[(zone.defteam == tm) & zone.weak_zone_flag].sort_values("ypt_vs_lg", ascending=False)
        r["weak_zones"] = "; ".join(f"{a} {b} {c:.1f} ypt" for a, b, c in zip(wz.pass_length, wz.pass_location, wz.ypt))
        if len(x):
            o = x.sort_values("composite_good")
            w, l = o.iloc[0], o.iloc[-1]
            fmt = lambda y: f"{y.player} ({y.pos}) {int(y.tgt)} tgt, {y.catch_pct}% catch, {y.ypt} ypt, rating {y.rating_allowed}"
            r["weakest_link"], r["weakest_link_labels"] = fmt(w), w.labels
            r["best_defender"], r["best_defender_labels"] = fmt(l), l.labels
            r["has_LOCKDOWN"] = bool(x.labels.str.contains("LOCKDOWN").any())
            r["has_WEAK_or_MAGNET"] = bool(x.labels.str.contains("WEAK LINK|TARGET MAGNET").any())
        rows.append(r)
    return pd.DataFrame(rows)


MARK3 = "<!-- DEFENDER-GRADES -->"


def write_sections(pdir, g, ts):
    for f in pdir.glob("*.md"):
        tm = f.stem
        body = f.read_text().split(MARK3)[0].rstrip() + "\n\n" + MARK3 + "\n"
        x = g[g.team == tm]
        r = ts[ts.team == tm].iloc[0] if (ts.team == tm).any() else None
        L = ["## Defender quality grades (CB/S with 20+ charted targets)", "",
             "PFR charted (weekly via nflverse) + pbp PBU. Percentiles vs his position league-wide (100 = best). Labels: see GRADES.md.", ""]
        if r is not None:
            L += [f"**Weakest link:** {r.get('weakest_link', '—')} [{r.get('weakest_link_labels', '')}]",
                  f"**Best / lockdown:** {r.get('best_defender', '—')} [{r.get('best_defender_labels', '')}]",
                  f"**Weak zones:** {r.get('weak_zones') or 'none flagged'}", ""]
        L += ["| Player | Pos | G | Tgt | Tgt share | Catch % | YPT | Yds/cmp | Yds/snap | Rating | TD | INT | PBU | Composite | Labels | Note |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for _, y in x.iterrows():
            L.append(f"| {y.player} | {y.pos} | {y.games} | {int(y.tgt)} | {y.target_share_secondary:.0%} | {y.catch_pct} | {y.ypt} | {y.yds_per_cmp} | "
                     f"{y.yds_per_def_snap} | {y.rating_allowed} | {int(y.td)} | {int(y.ints)} | {y.pbu_pbp} | {y.composite_good} | {y.labels} | {y.sample_note} |")
        f.write_text(body + "\n".join(L) + "\n")


def backtest(D, out_dir: Path):
    """Weeks 4-11: WR/TE receiving yards vs the player's own prior average (no saved lines used), split by the opponent's
    grade status. Leak-free: grades rebuilt through week w-1 for each week w."""
    p = D["p"]
    rec = p[(p.pass_attempt == 1) & p.receiver_player_id.notna() & (p.two_point_attempt != 1)].copy()
    rec["rpos"] = rec.receiver_player_id.map(D["off_pos"])
    rec = rec[rec.rpos.isin(["WR", "TE"])]
    gm = rec.groupby(["week", "receiver_player_id", "receiver_player_name", "posteam", "defteam"]).agg(
        yds=("receiving_yards", lambda x: x.fillna(0).sum()), tgts=("play_id", "size")).reset_index()
    rows = []
    for w in range(4, 12):
        g = grades(D, through=w - 1)
        st = {tm: (x.labels.str.contains("WEAK LINK|TARGET MAGNET").any(), x.labels.str.contains("LOCKDOWN").any()) for tm, x in g.groupby("team")}
        prior = gm[gm.week < w].groupby("receiver_player_id").agg(avg=("yds", "mean"), n=("week", "nunique"))
        cur = gm[gm.week == w].join(prior, on="receiver_player_id")
        cur = cur[(cur.n >= 3) & (cur.avg >= 30)]
        for _, x in cur.iterrows():
            weak, lock = st.get(x.defteam, (False, False))
            grp = "WEAK/MAGNET only" if weak and not lock else "LOCKDOWN only" if lock and not weak else "both" if weak and lock else "neither"
            rows.append({"week": w, "receiver": x.receiver_player_name, "defteam": x.defteam, "yds": x.yds, "prior_avg": round(x.avg, 1),
                         "resid": round(x.yds - x.avg, 1), "over_own_avg": bool(x.yds > x.avg), "group": grp})
    bt = pd.DataFrame(rows)
    bt.to_csv(out_dir / "grade_backtest_w4_11_rows.csv", index=False)
    sm = bt.groupby("group").agg(n=("resid", "size"), over_rate=("over_own_avg", "mean"), mean_resid=("resid", "mean"),
                                 median_resid=("resid", "median")).round(3).reset_index()
    sm.to_csv(out_dir / "grade_backtest_w4_11_summary.csv", index=False)
    return sm


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True, type=Path)
    ap.add_argument("--through-week", type=int)
    ap.add_argument("--out", type=Path, default=HERE)
    ap.add_argument("--backtest", action="store_true")
    ap.add_argument("--no-profiles", action="store_true")
    a = ap.parse_args()
    D = load_all(a.raw)
    wcp = a.out / "defender_explosives_allowed_inferred.csv"
    g = grades(D, a.through_week, pd.read_csv(wcp) if wcp.exists() else None)
    g.to_csv(a.out / "defender_grades.csv", index=False)
    ts = team_summary(g, a.out)
    ts.to_csv(a.out / "team_defense_summary.csv", index=False)
    if not a.no_profiles:
        write_sections(a.out / "profiles", g, ts)
    print(json.dumps({"graded": int(len(g)), "by_pos": g.pos.value_counts().to_dict(),
                      "labels": {k: int(g.labels.str.contains(k).sum()) for k in ("LOCKDOWN", "LIMITS CATCHES", "LIMITS YARDS", "GIVES UP EXPLOSIVES", "TARGET MAGNET", "WEAK LINK")},
                      "small_sample": int((g.tgt < SMALL).sum()), "through_week": int(g.through_week.max())}, indent=1))
    if a.backtest:
        print(backtest(D, a.out).to_string(index=False))


if __name__ == "__main__":
    main()
