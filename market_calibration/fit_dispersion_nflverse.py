"""NFL-75 item 5: fit margin/total SDs and player-yard lognormal sigmas from nflverse play-by-play (research only).

    python3 -m market_calibration.fit_dispersion_nflverse --pbp-dir <folder of play_by_play_YYYY.parquet> \
        --players <nflverse players.parquet> [--train-end-season 2026 --train-end-week 9]

Source: nflverse-data release assets `pbp/play_by_play_{2018..2026}.parquet` and `players/players.parquet`
(https://github.com/nflverse/nflverse-data/releases). Nothing is typed in: every number in the output JSON is computed
from those files, and the output records each file's sha256.

What is fitted (regular season only, per game):
  * margin residual  = (home_score - away_score) - spread_line      (nflverse spread_line: + = home favoured)
    SD by |spread_line| bin.
  * total residual   = (home_score + away_score) - total_line, SD by total_line bin.
  * player yards (receiving by WR/TE/RB, rushing by RB/QB, passing by QB): "line size" = the player's trailing mean
    over his previous <= 8 regular-season games with >= 1 opportunity (>= 3 needed). Historical prop lines are not in
    any source used here, so the trailing mean is a declared PROXY for the line. Within each (stat, position, line bin):
      p0          = share of opportunity-games with yards <= 0
      med_ratio   = exp(mean(log(y / trailing_mean)))  over y > 0
      sigma       = sd(log(y / trailing_mean))          over y > 0   (lognormal MLE, ddof=1)
    Player-games with no target/carry do not appear in play-by-play, so p0 is conditional on >= 1 opportunity.

Walk-forward: --train-end-season/--train-end-week bound the training rows (inclusive), so a backtest on 2026 week w fits
on everything strictly before it. Research only; does not change any default.
"""
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path
import numpy as np
import pandas as pd

SEASONS = list(range(2018, 2027))
SPREAD_BINS = [0.0, 3.0, 7.0, 10.0, 99.0]          # |spread_line|
TOTAL_BINS = [0.0, 41.0, 45.0, 49.0, 99.0]         # total_line
YARD_BINS = {"rec": [0, 30, 50, 70, 999], "rush": [0, 30, 50, 70, 999], "pass": [0, 200, 240, 270, 999]}
STAT_POS = {"rec": ("WR", "TE", "RB"), "rush": ("RB", "QB"), "pass": ("QB",)}
TRAIL_N, TRAIL_MIN = 8, 3
PBP_COLS = ["game_id", "season", "week", "season_type", "home_team", "away_team", "home_score", "away_score",
            "spread_line", "total_line", "play_type", "receiver_player_id", "receiving_yards", "rusher_player_id",
            "rushing_yards", "passer_player_id", "passing_yards", "complete_pass", "pass_attempt", "rush_attempt",
            "sack", "two_point_attempt"]


def sha256(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load_pbp(pbp_dir: Path, seasons=SEASONS) -> tuple[pd.DataFrame, dict]:
    frames, meta = [], {}
    for s in seasons:
        f = Path(pbp_dir) / f"play_by_play_{s}.parquet"
        import pyarrow.parquet as pq
        cols = [c for c in PBP_COLS if c in pq.ParquetFile(f).schema_arrow.names]
        d = pd.read_parquet(f, columns=cols)
        frames.append(d[d.season_type == "REG"])
        rt = f.with_suffix(".parquet.retrieved_utc")
        meta[f.name] = {"sha256": sha256(f), "retrieved_utc": rt.read_text().strip() if rt.exists() else None}
    return pd.concat(frames, ignore_index=True), meta


def game_table(pbp: pd.DataFrame) -> pd.DataFrame:
    g = pbp.groupby("game_id").agg(season=("season", "first"), week=("week", "first"), home=("home_team", "first"),
                                    away=("away_team", "first"), home_score=("home_score", "max"),
                                    away_score=("away_score", "max"), spread_line=("spread_line", "first"),
                                    total_line=("total_line", "first")).reset_index()
    g = g.dropna(subset=["home_score", "away_score", "spread_line", "total_line"])
    g["margin"] = g.home_score - g.away_score
    g["total"] = g.home_score + g.away_score
    g["margin_resid"] = g.margin - g.spread_line
    g["total_resid"] = g.total - g.total_line
    return g


def player_games(pbp: pd.DataFrame, players: pd.DataFrame) -> pd.DataFrame:
    p = pbp[pbp.two_point_attempt.fillna(0) == 0]
    out = []
    rec = p[(p.pass_attempt == 1) & p.receiver_player_id.notna()]
    out.append(rec.groupby(["receiver_player_id", "game_id"]).receiving_yards.sum(min_count=1).fillna(0)
               .rename("yards").reset_index().rename(columns={"receiver_player_id": "pid"}).assign(stat="rec"))
    ru = p[(p.rush_attempt == 1) & p.rusher_player_id.notna()]
    out.append(ru.groupby(["rusher_player_id", "game_id"]).rushing_yards.sum(min_count=1).fillna(0)
               .rename("yards").reset_index().rename(columns={"rusher_player_id": "pid"}).assign(stat="rush"))
    pa = p[(p.pass_attempt == 1) & p.passer_player_id.notna()]
    cnt = pa.groupby(["passer_player_id", "game_id"]).size().rename("n")
    py = pa.groupby(["passer_player_id", "game_id"]).passing_yards.sum(min_count=1).fillna(0).rename("yards")
    pq_ = pd.concat([py, cnt], axis=1).reset_index().rename(columns={"passer_player_id": "pid"})
    out.append(pq_[pq_.n >= 10].drop(columns="n").assign(stat="pass"))  # starter-ish passing games only
    pg = pd.concat(out, ignore_index=True)
    gm = pbp.groupby("game_id").agg(season=("season", "first"), week=("week", "first")).reset_index()
    pg = pg.merge(gm, on="game_id")
    pos = players.set_index("gsis_id")["position"]
    pg["pos"] = pg.pid.map(pos)
    pg = pg.sort_values(["stat", "pid", "season", "week"]).reset_index(drop=True)
    pg["trail_mean"] = trailing_mean(pg)
    return pg


def trailing_mean(pg: pd.DataFrame) -> pd.Series:
    """Mean of the player's previous <= TRAIL_N games (>= TRAIL_MIN); never includes the game itself.
    pg must be sorted by stat, pid, season, week."""
    return pg.groupby(["stat", "pid"]).yards.transform(
        lambda s: s.shift(1).rolling(TRAIL_N, min_periods=TRAIL_MIN).mean())


def _bin_label(edges, i):
    return f"[{edges[i]:g},{edges[i+1]:g})"


def _bin(x, edges):
    i = int(np.searchsorted(edges, x, side="right") - 1)
    return min(max(i, 0), len(edges) - 2)


def _mask_train(df, end_season, end_week):
    return (df.season < end_season) | ((df.season == end_season) & (df.week <= end_week))


def fit(games: pd.DataFrame, pg: pd.DataFrame, end_season: int, end_week: int) -> dict:
    g = games[_mask_train(games, end_season, end_week)]
    res = {"train_window": {"seasons": f"2018..{end_season}", "last_week_inclusive_of_last_season": end_week,
                            "season_type": "REG"}}
    m = {"all": {"n": int(len(g)), "sd": float(g.margin_resid.std(ddof=1)), "mean": float(g.margin_resid.mean())}}
    a = g.spread_line.abs()
    for i in range(len(SPREAD_BINS) - 1):
        s = g[(a >= SPREAD_BINS[i]) & (a < SPREAD_BINS[i + 1])]
        m[_bin_label(SPREAD_BINS, i)] = {"n": int(len(s)), "sd": float(s.margin_resid.std(ddof=1)),
                                         "mean": float(s.margin_resid.mean())}
    t = {"all": {"n": int(len(g)), "sd": float(g.total_resid.std(ddof=1)), "mean": float(g.total_resid.mean())}}
    for i in range(len(TOTAL_BINS) - 1):
        s = g[(g.total_line >= TOTAL_BINS[i]) & (g.total_line < TOTAL_BINS[i + 1])]
        t[_bin_label(TOTAL_BINS, i)] = {"n": int(len(s)), "sd": float(s.total_resid.std(ddof=1)),
                                        "mean": float(s.total_resid.mean())}
    res["margin_sd_by_abs_spread"] = {"bins": SPREAD_BINS, "values": m}
    res["total_sd_by_total_line"] = {"bins": TOTAL_BINS, "values": t}
    p = pg[_mask_train(pg, end_season, end_week) & pg.trail_mean.notna() & (pg.trail_mean > 0)]
    yards = {}
    for stat, poss in STAT_POS.items():
        edges = YARD_BINS[stat]
        for pos in poss:
            s0 = p[(p.stat == stat) & (p.pos == pos)]
            cells = {}
            for i in range(len(edges) - 1):
                s = s0[(s0.trail_mean >= edges[i]) & (s0.trail_mean < edges[i + 1])]
                pos_y = s[s.yards > 0]
                lr = np.log(pos_y.yards / pos_y.trail_mean)
                cells[_bin_label(edges, i)] = {"n": int(len(s)), "n_pos": int(len(pos_y)),
                                               "p0": float((s.yards <= 0).mean()) if len(s) else None,
                                               "med_ratio": float(np.exp(lr.mean())) if len(lr) > 1 else None,
                                               "sigma": float(lr.std(ddof=1)) if len(lr) > 1 else None}
            yards[f"{stat}:{pos}"] = {"bins": edges, "cells": cells}
    res["player_yards_lognormal"] = yards
    return res


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pbp-dir", required=True)
    ap.add_argument("--players", required=True)
    ap.add_argument("--train-end-season", type=int, default=2026)
    ap.add_argument("--train-end-week", type=int, default=9)
    ap.add_argument("--out", default=str(Path(__file__).parent / "fitted/dispersion_fit_nflverse_v1.json"))
    a = ap.parse_args(argv)
    pbp, meta = load_pbp(Path(a.pbp_dir))
    players = pd.read_parquet(a.players, columns=["gsis_id", "position"])
    pm = Path(a.players)
    rt = pm.with_suffix(".parquet.retrieved_utc")
    meta[pm.name] = {"sha256": sha256(pm), "retrieved_utc": rt.read_text().strip() if rt.exists() else None}
    games, pg = game_table(pbp), player_games(pbp, players)
    doc = {"label": "research only, not validated; fitted from nflverse play-by-play", "mode": "fitted_nflverse_v1",
           "generated_by": "market_calibration/fit_dispersion_nflverse.py",
           "sources": {"release": "https://github.com/nflverse/nflverse-data/releases", "files": meta},
           "line_size_proxy": "player trailing mean of previous <=8 REG games (>=3); no historical prop lines used",
           "player_sigma_reference": "trailing_mean",
           "player_sigma_note": ("sigma = sd(log(y / trailing_mean)); centre = trailing_mean * med_ratio, with p0. NOT "
                                 "centred on a book line; not valid as a drop-in for legs.py line-centred sigmas."),
           **fit(games, pg, a.train_end_season, a.train_end_week)}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(doc, indent=1) + "\n")
    print(json.dumps({k: doc[k] for k in ("margin_sd_by_abs_spread", "total_sd_by_total_line")}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
