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
    p = pd.read_parquet(C / "play_by_play_2026.parquet", columns=["game_id", "receiver_player_id", "receiving_yards", "rusher_player_id", "rushing_yards"])
    rec = p.groupby(["game_id", "receiver_player_id"]).receiving_yards.sum()
    rus = p.groupby(["game_id", "rusher_player_id"]).rushing_yards.sum()
    rows = []
    for r in g.itertuples():
        try:
            ko = datetime.fromisoformat(f"{r.gameday}T{r.gametime}:00-05:00").astimezone(timezone.utc)
        except ValueError:
            continue
        b = pregame_board(r.game_id, ko)
        if not b:
            continue
        for side in (b.get("sides") or {}).values():
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
    return pd.DataFrame(rows)


def roi(x):
    x = x[x.fd_american.notna() & x.hit80.notna()]
    if not len(x):
        return None, 0
    pnl = np.where(x.hit80 == 1, x.fd_american.map(american_profit), -1.0)
    return round(float(pnl.mean()), 3), len(x)


def main():
    L = ["# Season scorecard (rebuilt weekly)", ""]
    s = stars_table()
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
