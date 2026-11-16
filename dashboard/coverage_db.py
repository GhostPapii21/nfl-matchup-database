"""Coverage database: which defenders give up yards, how often, and to whom.

    python3 -m dashboard.coverage_db --season 2026 [--pbp PATH] [--advdef PATH] [--snaps PATH]

Two free sources, both imperfect, kept separate and labelled:

  charted   Pro Football Reference weekly advanced defense (nflverse pfr_advstats): targets, completions and yards
            charged to the nearest defender in coverage. Published a few days after each week.
  tackle    nflverse play-by-play: the defender credited with the tackle (or the pass defensed) on each target. This is
            who finished the play, which is usually but not always who was covering. Touchdowns with no tackle and
            catches out of bounds with no defender named have no link. Available the morning after.

Output: dashboard/results/coverage_db_<season>.json with
  defenders   one row per defender: charted per-game numbers, how many of his games allowed 50+/70+/100+ yards, his
              catches of 20+ ended (tackle link), and the receivers who had 70+ yard games with 30+ of them against him
  teams       per defense: receivers with 70+/80+/100+ games against it, by position, and catches of 20+ per game
  week        for the newest week, every 80+ yard receiver: yards by the defender who finished each catch
Research only. Nobody publishes who was assigned to whom for free; nothing here is an assignment.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "pregame" / ".cache"
OUT = ROOT / "dashboard" / "results"
COVER = {"CB": "CB", "DB": "CB", "S": "S", "FS": "S", "SS": "S", "SAF": "S", "LB": "LB", "ILB": "LB", "OLB": "LB", "MLB": "LB"}
EXPLOSIVE = 20


def _r(x, d=1):
    return None if x is None or (isinstance(x, float) and not np.isfinite(x)) else round(float(x), d)


def load(season: int, pbp=None, advdef=None, snaps=None):
    p = pd.read_parquet(pbp or CACHE / f"play_by_play_{season}.parquet")
    p = p[(p.season_type == "REG") & (p.two_point_attempt != 1)]
    a = pd.read_parquet(advdef or CACHE / f"advstats_week_def_{season}.parquet")
    s = pd.read_parquet(snaps or CACHE / f"snap_counts_{season}.parquet")
    ro = pd.read_parquet(CACHE / f"roster_weekly_{season}.parquet").dropna(subset=["gsis_id"]).sort_values("week")
    return p, a, s, ro


def targets(p: pd.DataFrame, pos: dict, short: dict | None = None) -> pd.DataFrame:
    """One row per target with the defender who finished the play (tackle, shared tackle, or pass defensed)."""
    t = p[(p.pass_attempt == 1) & (p.sack != 1) & p.receiver_player_id.notna()].copy()
    t["yds"] = t.receiving_yards.fillna(0)
    t["rpos"] = t.receiver_player_id.map(pos)
    first = lambda cols: t[cols].bfill(axis=1).iloc[:, 0]
    t["def_id"] = first(["solo_tackle_1_player_id", "tackle_with_assist_1_player_id", "assist_tackle_1_player_id", "pass_defense_1_player_id"])
    t["def_name"] = first(["solo_tackle_1_player_name", "tackle_with_assist_1_player_name", "assist_tackle_1_player_name", "pass_defense_1_player_name"])
    # Catches pushed or run out of bounds name the defender only in the play text: "... pushed ob at PIT 32 for 27 yards (P.Wilson)."
    if short is not None:
        named = t.desc.str.extract(r"for -?\d+ yards? \(([A-Z][A-Za-z\.\-' ]+?)[;\)]")[0]
        fill = t.def_id.isna() & named.notna()
        ids = [short.get((d, n)) for d, n in zip(t.defteam[fill], named[fill])]
        t.loc[fill, "def_id"] = ids
        t.loc[fill, "def_name"] = np.where(pd.notna(ids), named[fill], None)
    t["dpos"] = t.def_id.map(pos).map(COVER)
    t["explosive"] = (t.complete_pass == 1) & (t.yds >= EXPLOSIVE)
    return t


def charted_defenders(a: pd.DataFrame, s: pd.DataFrame) -> pd.DataFrame:
    sp = s.sort_values("week").groupby("pfr_player_id").agg(position=("position", "last"), snap_pct=("defense_pct", "mean"),
                                                              last_snap_pct=("defense_pct", "last"))
    a = a.copy()
    for c in ("def_targets", "def_completions_allowed", "def_yards_allowed", "def_receiving_td_allowed", "def_ints", "def_missed_tackles"):
        a[c] = a[c].fillna(0)
    g = a.groupby(["pfr_player_id", "pfr_player_name"]).agg(
        team=("team", "last"), games=("week", "nunique"), tgt=("def_targets", "sum"), rec=("def_completions_allowed", "sum"),
        yds=("def_yards_allowed", "sum"), td=("def_receiving_td_allowed", "sum"), ints=("def_ints", "sum"),
        g50=("def_yards_allowed", lambda x: int((x >= 50).sum())), g70=("def_yards_allowed", lambda x: int((x >= 70).sum())),
        g100=("def_yards_allowed", lambda x: int((x >= 100).sum())), worst=("def_yards_allowed", "max")).reset_index()
    wk = a.loc[a.groupby("pfr_player_id").def_yards_allowed.idxmax()][["pfr_player_id", "week", "opponent"]].rename(
        columns={"week": "worst_week", "opponent": "worst_opp"})
    g = g.merge(wk, on="pfr_player_id", how="left").join(sp, on="pfr_player_id")
    g["grp"] = g.position.map(COVER)
    return g[g.grp.notna()]


def build(season: int, pbp=None, advdef=None, snaps=None) -> dict:
    p, a, s, ro = load(season, pbp, advdef, snaps)
    pos = dict(zip(ro.gsis_id, ro.position))
    dc = ro[ro.depth_chart_position.isin(list(COVER))]                      # CB / FS / SS / LB instead of the roster's "DB"
    pos.update(dict(zip(dc.gsis_id, dc.depth_chart_position)))
    full = dict(zip(ro.gsis_id, ro.full_name))
    short = {}                                                               # (team, "J.Ramsey") -> gsis id, defenders only
    for r in ro[ro.position.isin(["DB", "LB", "CB", "S", "DL", "DE", "DT"])].itertuples():
        if isinstance(r.first_name, str) and isinstance(r.last_name, str) and r.first_name:
            short.setdefault((r.team, f"{r.first_name[0]}.{r.last_name}"), r.gsis_id)
    t = targets(p, pos, short)
    weeks = sorted(int(w) for w in t.week.unique())
    last = weeks[-1]
    ch = charted_defenders(a, s)
    # ---- tackle links per defender
    comp = t[t.complete_pass == 1]
    rg = t.groupby(["game_id", "week", "posteam", "defteam", "receiver_player_id"]).agg(
        receiver=("receiver_player_name", "first"), rpos=("rpos", "first"), tgt=("yds", "size"), rec=("complete_pass", "sum"),
        yds=("yds", "sum"), ex=("explosive", "sum")).reset_index()
    link = comp[comp.def_id.notna()].groupby(["game_id", "week", "defteam", "def_id", "receiver_player_id"]).agg(
        def_name=("def_name", "first"), dpos=("dpos", "first"), rec=("yds", "size"), yds=("yds", "sum"), ex=("explosive", "sum"),
        long=("yds", "max")).reset_index().merge(rg[["game_id", "receiver_player_id", "receiver", "rpos", "posteam", "yds"]].rename(
            columns={"yds": "game_yds"}), on=["game_id", "receiver_player_id"])
    dgames = t.groupby("defteam").week.nunique()
    tk = {}
    for did, g in link.groupby("def_id"):
        big = g[(g.game_yds >= 70) & (g.yds >= 30)].sort_values("yds", ascending=False)
        ex = comp[(comp.def_id == did) & comp.explosive]
        tk[did] = {"catches_ended": int(g.rec.sum()), "yards_on_them": int(g.yds.sum()), "explosive_ended": int(len(ex)),
                   "explosive_yards": int(ex.yds.sum()),
                   "big_games": [{"week": int(r.week), "receiver": r.receiver, "team": r.posteam, "pos": r.rpos, "game_yards": int(r.game_yds),
                                  "vs_him": int(r.yds), "long": int(r.long)} for r in big.head(8).itertuples()],
                   "n_big_games": int(len(big)), "n_big_100": int((big.game_yds >= 100).sum())}
    # ---- defenders table: charted rows, joined to tackle links by name + team
    names = {}
    for did, g in link.groupby("def_id"):
        names[(full.get(did, "").lower(), g.defteam.iloc[-1])] = did
        names[(full.get(did, "").lower(), None)] = did
    defenders = []
    for r in ch.itertuples():
        did = names.get((r.pfr_player_name.lower(), r.team)) or names.get((r.pfr_player_name.lower(), None))
        k = tk.get(did, {})
        team_games = int(dgames.get(r.team, r.games))
        defenders.append({
            "player": r.pfr_player_name, "team": r.team, "pos": r.grp, "games": int(r.games), "snap_pct": _r(r.snap_pct * 100, 0) if pd.notna(r.snap_pct) else None,
            "last_snap_pct": _r(r.last_snap_pct * 100, 0) if pd.notna(r.last_snap_pct) else None,
            "tgt_pg": _r(r.tgt / r.games), "rec_pg": _r(r.rec / r.games), "yds_pg": _r(r.yds / r.games),
            "ypt": _r(r.yds / r.tgt) if r.tgt else None, "cmp_pct": _r(100 * r.rec / r.tgt, 0) if r.tgt else None,
            "td": int(r.td), "ints": int(r.ints), "g50": int(r.g50), "g70": int(r.g70), "g100": int(r.g100),
            "worst": int(r.worst), "worst_week": int(r.worst_week) if pd.notna(r.worst_week) else None, "worst_opp": r.worst_opp,
            "explosive_ended": k.get("explosive_ended"), "explosive_ended_pg": _r(k.get("explosive_ended", 0) / team_games, 2) if k else None,
            "explosive_yards": k.get("explosive_yards"), "n_big_games": k.get("n_big_games"), "n_big_100": k.get("n_big_100"),
            "big_games": k.get("big_games", [])})
    # ---- team units
    teams = {}
    tex = t.groupby("defteam").explosive.sum()
    for d, g in rg.groupby("defteam"):
        n = int(dgames[d])
        row = {"games": n, "explosive_pg": _r(tex[d] / n, 2)}
        for thr in (70, 80, 100):
            row[f"g{thr}"] = int((g.yds >= thr).sum())
            row[f"g{thr}_by_pos"] = {ps: int(((g.yds >= thr) & (g.rpos == ps)).sum()) for ps in ("WR", "TE", "RB")}
        row["who_80"] = [{"week": int(x.week), "receiver": x.receiver, "team": x.posteam, "pos": x.rpos, "tgt": int(x.tgt), "rec": int(x.rec),
                          "yards": int(x.yds), "explosive": int(x.ex)} for x in g[g.yds >= 80].sort_values("week").itertuples()]
        teams[d] = row
    for key in ("explosive_pg", "g80", "g100"):
        order = sorted(teams, key=lambda d: -(teams[d][key] / (1 if key == "explosive_pg" else teams[d]["games"])))
        for i, d in enumerate(order, 1):
            teams[d][f"{key}_rank"] = i
    # ---- newest week: every 80+ receiver, yards by the defender who finished the catch
    week = []
    cw = t[t.week == last]
    chd = {(x["player"].lower(), x["team"]): x for x in defenders}
    for r in rg[(rg.week == last) & (rg.yds >= 80)].sort_values("yds", ascending=False).itertuples():
        c = cw[(cw.receiver_player_id == r.receiver_player_id) & (cw.game_id == r.game_id)]
        cc = c[c.complete_pass == 1]
        by = []
        for did, g in cc.groupby(cc.def_id.fillna("none")):
            nm = full.get(did) or (g.def_name.iloc[0] if did != "none" else "no tackler named (touchdown or out of bounds)")
            row = chd.get((str(nm).lower(), r.defteam), {})
            by.append({"defender": nm, "pos": COVER.get(pos.get(did), pos.get(did)) if did != "none" else None, "catches": int(len(g)),
                       "yards": int(g.yds.sum()), "long": int(g.yds.max()), "catches_20": int((g.yds >= EXPLOSIVE).sum()),
                       "season": {k: row.get(k) for k in ("games", "yds_pg", "rec_pg", "ypt", "g70", "g100", "td", "explosive_ended", "n_big_games", "last_snap_pct")} if row else None})
        by.sort(key=lambda x: -x["yards"])
        tm = teams.get(r.defteam, {})
        week.append({"receiver": full.get(r.receiver_player_id, r.receiver), "pos": r.rpos, "team": r.posteam, "defense": r.defteam,
                     "targets": int(r.tgt), "rec": int(r.rec), "yards": int(r.yds), "explosive": int(r.ex), "by_defender": by,
                     "defense_before": {"g80": tm.get("g80", 0) - 1, "games": tm.get("games", 1) - 1, "explosive_pg_rank": tm.get("explosive_pg_rank")}})
    return {"season": season, "through_week": last, "charted_through_week": int(a.week.max()),
            "generated_utc": pd.Timestamp.now("UTC").isoformat(timespec="seconds"),
            "defenders": sorted(defenders, key=lambda x: -(x["yds_pg"] or 0)), "teams": teams, "week": week}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--season", type=int, default=2026)
    ap.add_argument("--pbp"); ap.add_argument("--advdef"); ap.add_argument("--snaps")
    a = ap.parse_args(argv)
    res = build(a.season, a.pbp, a.advdef, a.snaps)
    OUT.mkdir(parents=True, exist_ok=True)
    f = OUT / f"coverage_db_{a.season}.json"
    f.write_text(json.dumps(res, indent=1, default=str))
    print(f, len(res["defenders"]), "defenders;", len(res["week"]), "receivers with 80+ in week", res["through_week"])


if __name__ == "__main__":
    main()
