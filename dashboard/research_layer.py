"""Attach the session's research layers to built boards (owner, Nov 25, 2026) and re-render the site.

For each board in dashboard/data/<game>.json, when the research exists, adds b["research"] with:
  reads       hand-written picks and avoids (research/projections_2026_w12/reads.json)
  adjusted    injury-rule / recent-role / Sharp projection (research/projections_2026_w12/<game>.json)
  roles       each defense: yards by role (WR1 / WR2 / WR3+ / TE / RB rec / RB rush) vs usual, season and last 5, ranks
  targets     each offense: target share overall, when blitzed, when hit or out of the pocket (FTN + play-by-play)
  zones       each defense: depth x side zones allowing the most and least vs league
  profile     each side: Sharp scheme rows (season / last 5) and coverage shell
Fail-soft: a game without research keeps its board as it was.

    python3 -m dashboard.research_layer            # all boards; rewrites dashboard/site/index.html and board.html
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "research" / "projections_2026_w12"
C = ROOT / "pregame" / ".cache"
SHARP_CODE = {"LA": "LAR"}


def _mod(name):
    spec = importlib.util.spec_from_file_location(name, RES / f"{name}.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def _r(x, n=3):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return None
    return round(float(x), n)


def targets_split(team):
    p = pd.read_parquet(C / "play_by_play_2026.parquet", columns=["season_type", "game_id", "play_id", "posteam", "qb_dropback", "pass_attempt", "sack",
                                                                  "receiver_player_name", "receiving_yards", "complete_pass", "qb_hit"])
    f = pd.read_parquet(C / "ftn_charting_2026.parquet", columns=["nflverse_game_id", "nflverse_play_id", "n_blitzers", "is_qb_out_of_pocket"])
    p = p[(p.season_type == "REG") & (p.posteam == team) & (p.qb_dropback == 1)].merge(f, left_on=["game_id", "play_id"], right_on=["nflverse_game_id", "nflverse_play_id"], how="left")
    t = p[(p.pass_attempt == 1) & (p.sack != 1) & p.receiver_player_name.notna()].copy()
    t["yds"] = t.receiving_yards.fillna(0)
    out = {}
    for lab, x in (("all", t), ("blitzed", t[t.n_blitzers.fillna(0) > 0]), ("pressured", t[(t.qb_hit == 1) | (t.is_qb_out_of_pocket == True)])):  # noqa: E712
        g = x.groupby("receiver_player_name").agg(tg=("yds", "size"), rec=("complete_pass", "sum"), yds=("yds", "sum"))
        g = g[g.tg >= 3].sort_values("tg", ascending=False).head(6)
        out[lab] = {"targets": int(len(x)), "rows": [{"player": n, "share": _r(r.tg / max(len(x), 1)), "catch": _r(r.rec / r.tg), "ypt": _r(r.yds / r.tg, 1)} for n, r in g.iterrows()]}
    return out


def main(argv=None) -> int:
    reads = json.loads((RES / "reads.json").read_text()).get("games", {})
    DB, Z, TP = _mod("defense_breakdown"), _mod("zones"), _mod("team_profile")
    g_roles, _ = DB.load()
    season, last5 = DB.table(g_roles), DB.table(g_roles, 5)
    pz = Z.load()
    t_sharp = TP.sharp()
    cov = pd.read_csv(ROOT / "data" / "coverage" / "sharp_coverage_2026.csv").set_index("team")
    boards = []
    for f in sorted((ROOT / "dashboard" / "data").glob("2026_*.json")):
        b = json.loads(f.read_text())
        gid = b["game"]["game_id"]
        adj = RES / f"{gid}.json"
        if gid in reads or adj.exists():
            try:
                r = {"reads": reads.get(gid), "adjusted": json.loads(adj.read_text()) if adj.exists() else None, "roles": {}, "targets": {}, "zones": {}, "profile": {}}
                for s in b["sides"].values():
                    off, dfn = s["offense"], s["defense"]
                    rows = {}
                    for lab, tb in (("season", season), ("last5", last5)):
                        x = tb[tb.defteam == dfn].set_index("role")
                        rows[lab] = {role: {"yds_vs_usual": _r(x.loc[role, "yds_vs_usual"], 1), "rec_vs_usual": _r(x.loc[role, "rec_vs_usual"], 1), "rank": int(x.loc[role, "rank"])}
                                     for role in ("WR1", "WR2", "WR3+", "TE", "RB rec", "RB rush") if role in x.index}
                    r["roles"][dfn] = rows
                    r["targets"][off] = targets_split(off)
                    zz = Z.profile(pz, dfn)
                    zz = zz[zz.tgt >= 8].reset_index()
                    zz["zone"] = zz.band.astype(str) + " " + zz.side.astype(str)
                    pick = lambda d: [{"zone": z.zone, "targets": int(z.tgt), "catch": _r(z.cmp), "lg_catch": _r(z.lg_cmp), "ypt_vs_lg": _r(z.ypt_vs_lg, 1), "around": z.around_the_ball} for z in d.itertuples()]
                    r["zones"][dfn] = {"leaks": pick(zz.sort_values("ypt_vs_lg", ascending=False).head(3)), "tight": pick(zz.sort_values("ypt_vs_lg").head(3))}
                    so, sd = SHARP_CODE.get(off, off), SHARP_CODE.get(dfn, dfn)
                    keys = ["aDOT", "deep_rate", "pressure", "blitz", "man", "pass_rate"]
                    prof = {}
                    for lab, d in (("off_season", t_sharp[t_sharp.team == so]), ("off_last5", t_sharp[t_sharp.team == so].sort_values("week").tail(5)),
                                   ("def_season", t_sharp[t_sharp.opp == sd]), ("def_last5", t_sharp[t_sharp.opp == sd].sort_values("week").tail(5)), ("league", t_sharp)):
                        rr = TP.rates(d)
                        prof[lab] = {k: _r(rr.get(k)) for k in keys}
                    if sd in cov.index:
                        c = cov.loc[sd]
                        prof["shell"] = {"man": float(c.man_pct), "zone": float(c.zone_pct), "one_high": float(c.mofc_pct), "two_high": float(c.mofo_pct)}
                    r["profile"][f"{off}_vs_{dfn}"] = prof
                b["research"] = r
                f.write_text(json.dumps(b, indent=1, allow_nan=False) + "\n")
                print(f"research: attached to {gid}")
            except Exception as e:  # noqa: BLE001
                print(f"research: {gid} skipped ({e!r})")
        boards.append(b)
    sys.path.insert(0, str(ROOT))
    from dashboard import build as BU
    slate = json.loads((ROOT / "dashboard" / "data" / "slate.json").read_text())
    ids = [x["game_id"] for x in slate["games"]]
    boards = [b for b in boards if b["game"]["game_id"] in ids]
    html = BU.render_site(boards, slate["built_utc"])
    (ROOT / "dashboard" / "site" / "index.html").write_text("<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
                                                           "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">"
                                                           "</head><body>\n" + html + "\n</body></html>\n")
    (ROOT / "dashboard" / "site" / "board.html").write_text(html)
    print(f"research: site re-rendered with {len(boards)} games")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
