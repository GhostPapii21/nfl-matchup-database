"""Season scorecard: how our pregame calls did, rebuilt from git history every week (runs in nfl-season-data.yml).

1. 80-yard stars: for every completed game, the last committed board (dashboard/data/<game>.json) before kickoff is read
   from git history; every receiver/rusher the board priced (p80, stars, FanDuel 80+ price) is graded against final
   play-by-play. Reports hit rate vs predicted by star level and the flat-stake ROI of betting the FanDuel 80+ price
   on (a) every starred player and (b) every player where blend - break-even >= 0.03.
2. Player baselines: grading/results/*.jsonl (python -m grading.grade) summarized per market: n, mean error (bias),
   mean absolute error, share of players who beat their median.
Writes grading/results/SCORECARD.md and grading/results/scorecard_stars.csv. Research only."""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "grading" / "results"
C = ROOT / "pregame" / ".cache"


def _git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True).stdout


def pregame_board(gid: str, kickoff: datetime):
    for line in _git("log", "--format=%H %cI", "--", f"dashboard/data/{gid}.json").splitlines():
        sha, t = line.split()
        if datetime.fromisoformat(t) < kickoff:
            try:
                return json.loads(_git("show", f"{sha}:dashboard/data/{gid}.json"))
            except ValueError:
                return None
    return None


def american_profit(a: float) -> float:
    return a / 100 if a > 0 else 100 / -a


def stars_table():
    g = pd.read_parquet(C / "games.parquet")
    g = g[(g.season == 2026) & g.home_score.notna()]
    p = pd.read_parquet(C / "play_by_play_2026.parquet", columns=["game_id", "receiver_player_id", "receiving_yards", "rusher_player_id", "rushing_yards", "complete_pass"])
    rec = p.groupby(["game_id", "receiver_player_id"]).receiving_yards.sum()
    rus = p.groupby(["game_id", "rusher_player_id"]).rushing_yards.sum()
    catches = p.groupby(["game_id", "receiver_player_id"]).complete_pass.sum()
    carries = p[p.rusher_player_id.notna()].groupby(["game_id", "rusher_player_id"]).size()
    actual_of = {"receiving_yards": rec, "rushing_yards": rus, "receptions": catches, "carries": carries}
    rows, picks, gpicks = [], [], []
    qp = pd.read_parquet(C / "play_by_play_2026.parquet", columns=["game_id", "qtr", "total_home_score", "total_away_score"])
    qend = qp.groupby(["game_id", "qtr"])[["total_home_score", "total_away_score"]].max()
    for r in g.itertuples():
        try:
            ko = datetime.fromisoformat(f"{r.gameday}T{r.gametime}:00-05:00").astimezone(timezone.utc)
        except ValueError:
            continue
        b = pregame_board(r.game_id, ko)
        if not b:
            continue
        if r.game_id in qend.index.get_level_values(0):
            e = qend.loc[r.game_id]
            cum = {int(q): (int(v.total_home_score), int(v.total_away_score)) for q, v in e.iterrows()}
            prev, per_q = (0, 0), {}
            for q in sorted(cum):
                per_q[q] = (cum[q][0] - prev[0], cum[q][1] - prev[1])
                prev = (max(prev[0], cum[q][0]), max(prev[1], cum[q][1]))
            span = {"": (1, 2, 3, 4, 5), "h1_": (1, 2), "h2_": (3, 4), "q1_": (1,), "q2_": (2,), "q3_": (3,), "q4_": (4,)}
            for gp in (b.get("game_bets") or {}).get("picks") or []:
                bb, mk = gp["best"], gp["market"]
                base = mk.split("_")[-1]
                pre = mk[: -len(base)]
                hp = sum(per_q.get(q, (0, 0))[0] for q in span.get(pre, ()))
                ap = sum(per_q.get(q, (0, 0))[1] for q in span.get(pre, ()))
                home, away = b["game"]["home"], b["game"]["away"]
                if base == "total":
                    x = (hp + ap - bb["line"]) * (1 if bb["side"] == "Over" else -1)
                else:
                    x = (hp - ap if bb["side"] == home else ap - hp) + (bb["line"] or 0)
                res = 1 if x > 0 else (0.5 if x == 0 else 0)
                gpicks.append({"game_id": r.game_id, "week": r.week, "market": mk, "period": gp["period"], "side": bb["side"], "line": bb["line"],
                               "book": bb["book"], "american": bb["american"], "p_bet": bb["p_bet"], "ev": bb["ev_per_dollar"], "alt": bb.get("alt"),
                               "flagged": bool(gp.get("flags")), "result": res})
        for side in (b.get("sides") or {}).values():
            for pk in (side.get("best_bets") or {}).get("picks") or []:
                bb, ser = pk["best"], actual_of.get(pk["market"])
                v = None if ser is None else ser.get((r.game_id, pk.get("player_id")))
                won = None if v is None or pd.isna(v) else int((v > bb["line"]) if bb["side"] == "Over" else (v < bb["line"]))
                picks.append({"game_id": r.game_id, "week": r.week, "player": pk.get("player"), "market": pk["market"], "side": bb["side"], "line": bb["line"],
                              "book": bb["book"], "american": bb["american"], "p_bet": bb["p_bet"], "ev": bb["ev_per_dollar"], "flagged": bool(pk.get("flags")),
                              "actual": v, "won": won})
            w = side.get("watch") or {}
            for kind, actual in (("receivers", rec), ("rushers", rus)):
                for e in w.get(kind) or []:
                    pid = e.get("player_id")
                    y = actual.get((r.game_id, pid))
                    bk = e.get("book80") or {}
                    rows.append({"game_id": r.game_id, "week": r.week, "player": e.get("player"), "kind": kind, "p80": e.get("p80"),
                                 "stars": e.get("stars", 0), "actual_yards": None if y is None or pd.isna(y) else float(y),
                                 "hit80": None if y is None or pd.isna(y) else int(y >= 80), "fd_american": bk.get("american"),
                                 "break_even": bk.get("break_even"), "blend": bk.get("blend")})
    return pd.DataFrame(rows), pd.DataFrame(picks), pd.DataFrame(gpicks)


def roi(x):
    x = x[x.fd_american.notna() & x.hit80.notna()]
    if not len(x):
        return None, 0
    pnl = np.where(x.hit80 == 1, x.fd_american.map(american_profit), -1.0)
    return round(float(pnl.mean()), 3), len(x)


def main():
    L = ["# Season scorecard (rebuilt weekly)", ""]
    s, bp, gp = stars_table()
    if len(gp):
        gp.to_csv(RES / "scorecard_game_bets.csv", index=False)
        g2 = gp[gp.ev >= 0.02]
        if len(g2):
            def gl(x, label):
                pnl = np.where(x.result == 1, x.american.map(american_profit), np.where(x.result == 0, -1.0, 0.0))
                return f"| {label} | {len(x)} | {(x.result == 1).mean():.0%} | {(x.result == 0.5).mean():.0%} | {pnl.mean():+.2f} |"
            L += [f"## Game-market picks (EV +2% or more before kickoff): {len(g2)} graded", "", "| Group | Bets | Won | Pushed | ROI per $1 |",
                  "|---|---|---|---|---|", gl(g2, "All")]
            for lab, m in (("Alt lines", g2.alt == True), ("Main lines", g2.alt != True), ("Quarters", g2.period.str.contains("quarter")),  # noqa: E712
                           ("Halves", g2.period.str.contains("half")), ("Full game", g2.period == "Game")):
                if m.any():
                    L.append(gl(g2[m], lab))
            L += [""]
    if len(bp):
        bp.to_csv(RES / "scorecard_best_bets.csv", index=False)
        g = bp[bp.won.notna() & (bp.ev >= 0.02)]
        if len(g):
            def line(x, label):
                pnl = np.where(x.won == 1, x.american.map(american_profit), -1.0)
                return f"| {label} | {len(x)} | {x.won.mean():.0%} | {x.p_bet.mean():.0%} | {pnl.mean():+.2f} |"
            L += [f"## Best-bet picks (EV +2% or more on the board before kickoff): {len(g)} graded", "",
                  "| Group | Bets | Won | Our chance | ROI per $1 |", "|---|---|---|---|---|", line(g, "All")]
            for lab, m in (("Overs", g.side == "Over"), ("Unders", g.side == "Under"), ("No flag", ~g.flagged), ("Flagged (check line)", g.flagged)):
                if m.any():
                    L.append(line(g[m], lab))
            L += [""]
    if len(s):
        s.to_csv(RES / "scorecard_stars.csv", index=False)
        g = s[s.hit80.notna()]
        L += [f"## 80-yard calls: {len(g)} graded player-games in {g.game_id.nunique()} games", "",
              "| Stars | Players | Predicted 80+ | Actual 80+ | FanDuel bets | ROI per $1 |", "|---|---|---|---|---|---|"]
        for k in (3, 2, 1, 0):
            x = g[g.stars == k]
            if len(x):
                r, n = roi(x)
                L.append(f"| {k or 'none'} | {len(x)} | {x.p80.mean():.0%} | {x.hit80.mean():.0%} | {n} | {'' if r is None else f'{r:+.2f}'} |")
        r, n = roi(g[g.stars > 0])
        r2, n2 = roi(g[(g.blend - g.break_even) >= 0.03])
        L += ["", f"- Bet every starred player at the FanDuel 80+ price: {n} bets, ROI {'n/a' if r is None else f'{r:+.2f}'} per $1.",
              f"- Bet only where the model+book blend beats the price by 3+ points: {n2} bets, ROI {'n/a' if r2 is None else f'{r2:+.2f}'} per $1.",
              "- Fewer than ~300 bets cannot separate skill from luck; read these as a running record.", ""]
    rows = [json.loads(l) for f in sorted(RES.glob("*.jsonl")) if not f.name.endswith(".research.jsonl") for l in f.read_text().splitlines() if l.strip()]
    pp = pd.DataFrame([r for r in rows if r.get("kind") == "player_projection" and r.get("error_actual_minus_projection") is not None])
    if len(pp):
        L += [f"## Player baselines (packet medians): {len(pp)} player-markets in {pp.game_id.nunique()} games", "",
              "| Market | n | Mean error (actual - median) | Mean absolute error | Beat the median |", "|---|---|---|---|---|"]
        for m, x in pp.groupby("market_type"):
            e = pd.to_numeric(x.error_actual_minus_projection, errors="coerce").dropna()
            if not len(e):
                continue
            L.append(f"| {m} | {len(e)} | {e.mean():+.1f} | {e.abs().mean():.1f} | {(e > 0).mean():.0%} |")
    led = ROOT / "grading" / "bets" / "LEDGER.csv"
    b = pd.read_csv(led) if led.exists() else pd.DataFrame()
    b = b[b.get("result", pd.Series(dtype=str)).isin(["W", "L", "P"])] if len(b) else b
    if len(b):
        stake = b.stake.astype(float)
        profit = np.where(b.result == "W", stake * b.american.astype(float).map(american_profit), np.where(b.result == "L", -stake, 0.0))
        imp = lambda a: 100 / (a + 100) if a > 0 else -a / (-a + 100)
        c = b[b.closing_american.notna()]
        clv = (c.closing_american.astype(float).map(imp) - c.american.astype(float).map(imp)).mean() if len(c) else None
        L += ["", f"## Real bets ({len(b)} settled)", "", f"- Won {int((b.result == 'W').sum())}, lost {int((b.result == 'L').sum())}, pushed {int((b.result == 'P').sum())}.",
              f"- Profit {profit.sum():+.2f} on {stake.sum():.2f} staked (ROI {profit.sum() / stake.sum():+.1%}).",
              f"- Closing-line value: {'n/a' if clv is None else f'{clv * 100:+.1f} points of break-even on {len(c)} bets (positive = you beat the close)'}."]
        for m, x in b.groupby("market"):
            st = x.stake.astype(float)
            pr = np.where(x.result == "W", st * x.american.astype(float).map(american_profit), np.where(x.result == "L", -st, 0.0))
            L.append(f"  - {m}: {len(x)} bets, ROI {pr.sum() / st.sum():+.1%}")
    (RES / "SCORECARD.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
