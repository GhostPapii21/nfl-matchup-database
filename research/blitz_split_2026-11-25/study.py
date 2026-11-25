"""Does a receiver's own target share when his QB is blitzed predict who gets the ball against a blitz-heavy defense?
(owner, Nov 25, 2026: "if we'd known the pressure Burrow would face, we'd have known the short routes and the tight ends
would get the ball, not Chase.")

The league-wide test (research/blitz_targets_2026-11-24) found blitz barely moves target shares on average. This tests the
player-specific version. FTN charting (via nflverse) marks blitzers on every 2026 dropback.

For each team-game from Week 4 on, every receiver with 15+ earlier targets:
  A  season share               his share of the team's targets in earlier games
  B  blitz-mix share            p * (his share on earlier blitzed dropbacks) + (1-p) * (his share on non-blitzed ones),
                                p = the defense's blitz rate in its earlier games; each split shrunk toward A
                                (20 targets of A's weight), then scaled so the team's shares add to the same total as A.
Score: target-weighted squared error vs his actual share that game, all games and against blitz-heavy defenses (33%+).

    python3 research/blitz_split_2026-11-25/study.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
C = HERE.parents[1] / "pregame" / ".cache"
K = 20.0


def load():
    p = pd.read_parquet(C / "play_by_play_2026.parquet", columns=["season_type", "week", "game_id", "play_id", "posteam", "defteam", "qb_dropback",
                                                                  "receiver_player_id", "receiver_player_name", "pass_attempt", "sack"])
    f = pd.read_parquet(C / "ftn_charting_2026.parquet", columns=["nflverse_game_id", "nflverse_play_id", "n_blitzers"])
    p = p[(p.season_type == "REG") & (p.qb_dropback == 1)].merge(f, left_on=["game_id", "play_id"], right_on=["nflverse_game_id", "nflverse_play_id"])
    p["bl"] = p.n_blitzers.fillna(0) > 0
    return p


def main():
    p = load()
    t = p[(p.pass_attempt == 1) & (p.sack != 1) & p.receiver_player_id.notna()]
    rows = []
    for (gid, wk, off, dfn), g in t.groupby(["game_id", "week", "posteam", "defteam"]):
        if wk < 4:
            continue
        prior = t[(t.posteam == off) & (t.week < wk)]
        dprior = p[(p.defteam == dfn) & (p.week < wk)]
        if len(prior) < 60 or len(dprior) < 60:
            continue
        pb = dprior.bl.mean()
        nb, nn = prior.bl.sum(), (~prior.bl).sum()
        tot = prior.receiver_player_id.value_counts()
        cb = prior[prior.bl].receiver_player_id.value_counts()
        cn = prior[~prior.bl].receiver_player_id.value_counts()
        act = g.receiver_player_id.value_counts() / len(g)
        cand = tot[tot >= 15].index
        A = {i: tot[i] / len(prior) for i in cand}
        B = {}
        for i in cand:
            sb = (cb.get(i, 0) + K * A[i]) / (nb + K)
            sn = (cn.get(i, 0) + K * A[i]) / (nn + K)
            B[i] = pb * sb + (1 - pb) * sn
        s = sum(A.values()) / sum(B.values())
        names = prior.drop_duplicates("receiver_player_id").set_index("receiver_player_id").receiver_player_name
        for i in cand:
            rows.append({"game": gid, "week": wk, "off": off, "def": dfn, "def_blitz": pb, "player": names.get(i), "A": A[i], "B": B[i] * s,
                         "actual": act.get(i, 0.0), "n": len(g), "split_gap": (cb.get(i, 0) / max(nb, 1)) - (cn.get(i, 0) / max(nn, 1))})
    d = pd.DataFrame(rows)
    def err(x, col):
        return float(np.average((x[col] - x.actual) ** 2, weights=x.n))
    res = {"player_games": len(d), "team_games": int(d.game.nunique() * 1)}
    for lab, x in (("all games", d), ("vs blitz-heavy defenses (33%+)", d[d.def_blitz >= 0.33]), ("vs blitz-light defenses (<25%)", d[d.def_blitz < 0.25])):
        a, b = err(x, "A"), err(x, "B")
        # paired bootstrap by team-game
        gs = x.game.unique(); rng = np.random.default_rng(3); diffs = []
        grp = {gg: x[x.game == gg] for gg in gs}
        for _ in range(1000):
            s_ = pd.concat([grp[gg] for gg in rng.choice(gs, len(gs))])
            diffs.append(err(s_, "B") - err(s_, "A"))
        res[lab] = {"rows": int(len(x)), "season_share_err": round(a * 1e4, 3), "blitz_mix_err": round(b * 1e4, 3),
                    "change_pct": round(100 * (b - a) / a, 2), "ci95_of_change_x1e4": [round(np.percentile(diffs, 2.5) * 1e4, 3), round(np.percentile(diffs, 97.5) * 1e4, 3)]}
    # stability: is a player's blitz split a trait? first half vs second half of his targets
    res["split_gap_examples"] = d[d.week == d.week.max()].sort_values("split_gap").iloc[[0, 1, 2, -3, -2, -1]][["player", "off", "split_gap"]].round(3).to_dict("records")
    mnf = d[d.game == "2026_11_CIN_WAS"][["player", "off", "def_blitz", "A", "B", "actual"]].sort_values(["off", "A"], ascending=[True, False]).round(3)
    res["mnf_cin_was"] = mnf.to_dict("records")
    (HERE / "results.json").write_text(json.dumps(res, indent=1, default=str) + "\n")
    print(json.dumps(res, indent=1, default=str))


if __name__ == "__main__":
    main()
