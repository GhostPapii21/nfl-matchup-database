"""Layered team profiles for a matchup (owner, Nov 25, 2026): offense scheme, QB vs blitz, defense coverage and pressure,
season vs last 5, rest and travel. Sources: Sharp advanced box scores (Weeks 1-10, per team-game), Sharp public coverage
table (man / zone / one-high / two-high), FTN charting via nflverse (blitzers on every dropback, through Week 11),
nflverse play-by-play and schedule. Context layers: shown, not yet weighted into the simulation (see README).

    python3 research/projections_2026_w12/team_profile.py GB LA
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
C = ROOT / "pregame" / ".cache"
CODE = {"LA": "LAR"}


def sharp():
    rows = [json.loads(l) for l in open(ROOT / "data_packages" / "sharp_advanced_2026_w1_10" / "team_games.jsonl")]
    return pd.DataFrame([{"week": r["week"], "team": r["team"], "opp": r["opponent"], **r["metrics"]} for r in rows])


def rates(d):
    s = d.sum(numeric_only=True)
    f = lambda a, b: s[a] / s[b] if s.get(b) else np.nan
    return {"plays_pg": s["plays"] / len(d), "epa_play": f("epa", "epa_n") if "epa_n" in s else d.epa.mean() if "epa" in d else np.nan,
            "pass_rate": f("att", "plays") if "att" in s else np.nan, "p11": f("p11", "plays"), "p12": f("p12", "plays"),
            "play_action": f("pa", "db") if "pa" in s else np.nan, "shotgun": f("shotgun", "plays"), "no_huddle": f("nh", "plays"),
            "aDOT": f("air", "att"), "deep_rate": f("deep", "att"), "ttt": f("ttt", "ttt_n"), "pressure": f("prsr", "db"),
            "blitz": f("blitz", "db"), "man": f("man", "cov"), "sack": f("sack", "db") if "sack" in s else np.nan,
            "explosive": f("explo", "plays") if "explo" in s else np.nan}


def qb_blitz(team=None, defense=None):
    p = pd.read_parquet(C / "play_by_play_2026.parquet", columns=["season_type", "week", "game_id", "play_id", "posteam", "defteam", "qb_dropback",
                                                                  "pass_attempt", "sack", "complete_pass", "yards_gained", "epa", "passer_player_name"])
    f = pd.read_parquet(C / "ftn_charting_2026.parquet", columns=["nflverse_game_id", "nflverse_play_id", "n_blitzers", "is_qb_out_of_pocket"])
    p = p[(p.season_type == "REG") & (p.qb_dropback == 1)].merge(f, left_on=["game_id", "play_id"], right_on=["nflverse_game_id", "nflverse_play_id"])
    p["blitz"] = p.n_blitzers.fillna(0) > 0
    def summ(d):
        return {"dropbacks": int(len(d)), "epa": round(float(d.epa.mean()), 3), "yds_per_db": round(float(d.yards_gained.mean()), 2),
                "comp": round(float(d.loc[d.pass_attempt == 1, "complete_pass"].mean()), 3), "sack": round(float(d.sack.mean()), 3)}
    out = {}
    if team:
        d = p[p.posteam == team]
        out["offense"] = {"vs_blitz": summ(d[d.blitz]), "no_blitz": summ(d[~d.blitz]), "blitz_faced": round(float(d.blitz.mean()), 3),
                          "qb": d.passer_player_name.value_counts().head(2).to_dict()}
    if defense:
        d = p[p.defteam == defense]
        out["defense"] = {"when_blitzing": summ(d[d.blitz]), "no_blitz": summ(d[~d.blitz]), "blitz_rate": round(float(d.blitz.mean()), 3)}
    out["league"] = {"vs_blitz": summ(p[p.blitz]), "no_blitz": summ(p[~p.blitz])}
    return out


def rest(team, gid):
    g = pd.read_parquet(C / "games.parquet")
    g = g[(g.season == 2026) & (g.game_type == "REG")]
    r = g[g.game_id == gid].iloc[0]
    days = r.away_rest if r.away_team == team else r.home_rest
    prev = g[((g.home_team == team) | (g.away_team == team)) & (g.gameday < r.gameday)].sort_values("gameday").tail(2)
    trips = [f"wk{int(x.week)} {x.stadium} ({x.location})" for x in prev.itertuples()]
    return {"days_rest": int(days), "last_two": trips}


def show(off, dfn, gid):
    t = sharp()
    so, sd = CODE.get(off, off), CODE.get(dfn, dfn)
    cov = pd.read_csv(ROOT / "data" / "coverage" / "sharp_coverage_2026.csv").set_index("team")
    o_all, o_l5 = t[t.team == so], t[t.team == so].sort_values("week").tail(5)
    d_all, d_l5 = t[t.opp == sd], t[t.opp == sd].sort_values("week").tail(5)
    lg = rates(t)
    keys = ["plays_pg", "pass_rate", "p11", "p12", "play_action", "shotgun", "aDOT", "deep_rate", "ttt", "pressure", "blitz", "man", "explosive"]
    tab = pd.DataFrame({f"{off} off season": rates(o_all), f"{off} off last5": rates(o_l5), f"{dfn} def season": rates(d_all),
                        f"{dfn} def last5": rates(d_l5), "league": lg}).loc[keys]
    print(f"\n######## {off} offense vs {dfn} defense  ({gid})")
    print("Sharp advanced (defense columns = what offenses did against it):")
    print(tab.round(3).to_string())
    if sd in cov.index:
        c = cov.loc[sd]
        print(f"{dfn} coverage shell (Sharp, {c.source_updated}): man {c.man_pct}%  zone {c.zone_pct}%  one-high {c.mofc_pct}%  two-high {c.mofo_pct}%")
    q = qb_blitz(off, dfn)
    print(f"{off} QB {list(q['offense']['qb'])}: vs blitz {q['offense']['vs_blitz']}  |  no blitz {q['offense']['no_blitz']}  |  blitzed on {q['offense']['blitz_faced']:.0%}")
    print(f"{dfn} defense: when blitzing {q['defense']['when_blitzing']}  |  not {q['defense']['no_blitz']}  |  blitz rate {q['defense']['blitz_rate']:.0%}")
    print(f"league: vs blitz {q['league']['vs_blitz']}  |  no blitz {q['league']['no_blitz']}")
    print(f"rest/travel: {off} {rest(off, gid)}  |  {dfn} {rest(dfn, gid)}")


if __name__ == "__main__":
    a, b = sys.argv[1], sys.argv[2]
    g = pd.read_parquet(C / "games.parquet")
    wk = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    gid = g[(g.season == 2026) & (g.week == wk) & (((g.away_team == a) & (g.home_team == b)) | ((g.away_team == b) & (g.home_team == a)))].game_id.iloc[0]
    show(a, b, gid); show(b, a, gid)
