"""When a target earner or ball carrier is out, who gets his work? (2022-2025 fit, 2026 weeks 1-10 check)

A player is "out" for a game when he had a real role coming in (played-games share of team targets >= 8%, or of
running-back carries >= 15%, over 3+ games), played one of the team's last two games, and is not active on that week's
roster (nflverse weekly rosters: status != ACT) and has no target or carry in the game.

For every teammate who did play, the table holds his baseline share (0.6 season + 0.4 last three, played games only),
his actual share in the game, the missing share M split into same position group and other, and his rank among the
healthy players. Everything is known before kickoff except the actual share.

    python3 research/teammate_out_2026-11-16/study.py     # writes rows.parquet (ignored) and results.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = Path(__file__).resolve().parent
C = HERE.parents[1] / "pregame" / ".cache"
MIN_SHARE_T, MIN_SHARE_C, MIN_GAMES = 0.08, 0.15, 3


def r3(x):
    return None if x is None or not np.isfinite(x) else round(float(x), 3)


def season_rows(y: int, pbp_path: Path | None = None):
    p = pd.read_parquet(pbp_path or C / f"play_by_play_{y}.parquet")
    p = p[(p.season_type == "REG") & (p.two_point_attempt != 1)]
    ro = pd.read_parquet(C / f"roster_weekly_{y}.parquet")
    pos = dict(zip(ro.gsis_id, ro.position))
    active = set(zip(ro[ro.status == "ACT"].week, ro[ro.status == "ACT"].team, ro[ro.status == "ACT"].gsis_id))
    t = p[(p.pass_attempt == 1) & (p.sack != 1) & p.receiver_player_id.notna()]
    c = p[(p.rush_attempt == 1) & p.rusher_player_id.notna() & (p.qb_kneel != 1)]
    c = c[c.rusher_player_id.map(pos) == "RB"]
    out = {"tgt": [], "car": []}
    for kind, d, idc, minshare in (("tgt", t, "receiver_player_id", MIN_SHARE_T), ("car", c, "rusher_player_id", MIN_SHARE_C)):
        pg = d.groupby(["posteam", "week", idc]).size().rename("n").reset_index()
        team = d.groupby(["posteam", "week"]).size().rename("team_n")
        for tm, g in pg.groupby("posteam"):
            weeks = sorted(g.week.unique())
            for wi, w in enumerate(weeks):
                prior = g[g.week < w]
                if prior.week.nunique() < MIN_GAMES:
                    continue
                last2 = weeks[max(0, wi - 2):wi]
                base = {}
                for pid, h in prior.groupby(idc):
                    if h.week.nunique() < MIN_GAMES:
                        continue
                    tt = team.loc[tm].reindex(h.week).sum()
                    l3 = h.sort_values("week").tail(3)
                    s = h.n.sum() / tt
                    s3 = l3.n.sum() / team.loc[tm].reindex(l3.week).sum()
                    base[pid] = (0.6 * s + 0.4 * s3 if h.week.nunique() >= 5 else s, h.week.max())
                now = g[g.week == w].set_index(idc).n
                team_now = team.loc[(tm, w)]
                outs = {pid: b for pid, (b, last) in base.items()
                        if b >= minshare and last in last2 and pid not in now.index and (w, tm, pid) not in active}
                healthy = {pid: b for pid, (b, _) in base.items() if pid not in outs and (pid in now.index or (w, tm, pid) in active)}
                if not healthy:
                    continue
                H = sum(healthy.values())
                grp = lambda pid: "RB" if pos.get(pid) == "RB" else ("TE" if pos.get(pid) == "TE" else "WR")
                order = sorted(healthy, key=lambda k: -healthy[k])
                for pid, b in healthy.items():
                    same = sum(v for k, v in outs.items() if grp(k) == grp(pid))
                    oth = sum(outs.values()) - same
                    same_rank = [k for k in order if grp(k) == grp(pid)].index(pid) + 1
                    out[kind].append({"season": y, "week": w, "team": tm, "player": pid, "pos": pos.get(pid), "grp": grp(pid),
                                      "base": b, "H": H, "prop": b / H, "actual": now.get(pid, 0) / team_now, "n": int(now.get(pid, 0)),
                                      "team_n": int(team_now), "M": sum(outs.values()), "M_same": same, "M_other": oth,
                                      "rank": order.index(pid) + 1, "rank_in_group": same_rank, "n_out": len(outs)})
    return pd.DataFrame(out["tgt"]), pd.DataFrame(out["car"])


def fit(df, label):
    """actual - base = prop * (a_same * M_same + a_other * M_other) + extra for the top healthy player of the same group."""
    d = df.copy()
    d["delta"] = d.actual - d.base
    d["x_same"] = d.prop * d.M_same
    d["x_other"] = d.prop * d.M_other
    d["x_top_same"] = np.where(d.rank_in_group == 1, d.M_same, 0.0)
    X = d[["x_same", "x_other", "x_top_same"]]
    m = sm.OLS(d.delta, sm.add_constant(X)).fit(cov_type="cluster", cov_kwds={"groups": d.team.astype(str) + d.season.astype(str) + d.week.astype(str)})
    return {"label": label, "n": int(len(d)), "n_with_out": int((d.M > 0).sum()),
            "coef": {k: r3(v) for k, v in m.params.items()}, "se": {k: r3(v) for k, v in m.bse.items()}}, m


def tables(df):
    d = df[df.M >= 0.08].copy()
    d["delta"] = d.actual - d.base
    d["ratio_of_M"] = d.delta / d.M
    rows = []
    for lab, m in (("top healthy player, same position group as the missing one", (d.rank_in_group == 1) & (d.M_same >= 0.08)),
                   ("second in that group", (d.rank_in_group == 2) & (d.M_same >= 0.08)),
                   ("third or lower in that group", (d.rank_in_group >= 3) & (d.M_same >= 0.08)),
                   ("top player of a different group", (d.rank_in_group == 1) & (d.M_same < 0.02)),
                   ("everyone else in a different group", (d.rank_in_group >= 2) & (d.M_same < 0.02))):
        x = d[m]
        rows.append({"who": lab, "n": int(len(x)), "base_share": r3(x.base.mean()), "actual_share": r3(x.actual.mean()),
                     "gain_pts": r3((x.actual - x.base).mean()), "missing_share": r3(x.M.mean()),
                     "gain_as_share_of_missing": r3((x.actual - x.base).sum() / x.M.sum())})
    return rows


def evaluate(df, coef, top_extra, label):
    """Share error on games with someone out: no bump, the current rule (80% proportional), the fitted rule."""
    d = df[df.M >= 0.08]
    none = d.base
    cur = d.base + 0.8 * d.M * d.prop
    new = d.base + d.prop * (coef["x_same"] * d.M_same + coef["x_other"] * d.M_other) + np.where(d.rank_in_group == 1, top_extra * d.M_same, 0.0)
    mae = lambda pr: r3(np.abs(pr - d.actual).mean())
    bias_top = lambda pr: r3((pr - d.actual)[(d.rank_in_group == 1) & (d.M_same >= 0.08)].mean())
    return {"label": label, "n": int(len(d)), "mae": {"no_bump": mae(none), "current_80pct": mae(cur), "fitted": mae(new)},
            "bias_top_same_group": {"no_bump": bias_top(none), "current_80pct": bias_top(cur), "fitted": bias_top(new)}}


def main():
    T, K = [], []
    for y in (2022, 2023, 2024, 2025, 2026):
        newest = HERE.parents[1] / "pregame" / ".cache" / f"play_by_play_{y}.parquet"
        a, b = season_rows(y, newest)
        T.append(a); K.append(b)
        print(y, len(a), len(b), flush=True)
    T, K = pd.concat(T), pd.concat(K)
    T.to_parquet(HERE / "rows_targets.parquet"); K.to_parquet(HERE / "rows_carries.parquet")
    res = {}
    for name, df in (("targets", T), ("carries", K)):
        tr, te = df[df.season <= 2024], df[df.season >= 2025]
        f, m = fit(tr, f"{name}: fit 2022-2024")
        res[name] = {"fit": f, "who_gains_2022_2026": tables(df),
                     "test_2025_2026": evaluate(te, f["coef"], f["coef"]["x_top_same"], "holdout 2025-2026"),
                     "games_with_someone_out": int(df[df.M >= 0.08].groupby(["season", "week", "team"]).ngroups),
                     "team_volume_when_out": r3(df[df.M >= 0.08].drop_duplicates(["season", "week", "team"]).team_n.mean()),
                     "team_volume_otherwise": r3(df[df.M == 0].drop_duplicates(["season", "week", "team"]).team_n.mean())}
    (HERE / "results.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
