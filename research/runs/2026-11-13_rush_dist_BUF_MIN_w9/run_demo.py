"""NFL-75 demo: per-player rushing-yards distribution artifact for Week 9 BUF@MIN (2026_09_BUF_MIN), n<=20,000.

The game is over and has no committed engine config, so this builds a RESEARCH config in memory from the Week 10
data_only/NFL-43 template (buf_nyj_2026-11-15_data_only_nfl43.json: same semantics, same history scope) with
home MIN, away BUF, history weeks 1-8 (the engine filters the committed W1-9 PBP to those weeks; the target game is
week 9 and is never read as history). It calls snapshots/lock.run_sim exactly as pipeline.sim100k.default_engine does,
then pipeline.rush_dist on the per-player box lines. Nothing is written to core/ or pipeline/ledgers/.

Smoke test only (one game, a handful of players): actual = nflverse rushing_yards for the game incl. kneels
(official-stat convention), from the committed W1-9 PBP. Optional --odds reads FanDuel's main rush-yd lines from the
Week 9 alt-test raw pull (draft PR #41, data/odds_history/alt_test_week9/raw/2026_09_BUF_MIN_*.json); 0 new credits.

    python research/runs/2026-11-13_rush_dist_BUF_MIN_w9/run_demo.py [--n 20000] [--workers 6] [--odds <raw json>]
Research only; projection_ready stays false."""
from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ENGINE = ROOT / "core" / "possession_engine_v0"
sys.path[:0] = [str(ROOT), str(ENGINE)]
TEMPLATE = ENGINE / "config/buf_nyj_2026-11-15_data_only_nfl43.json"
PBP = ROOT / "data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet"
GAME = "2026_09_BUF_MIN"


def research_cfg() -> dict:
    c = copy.deepcopy(json.loads(TEMPLATE.read_text()))
    c["config_id"] = "research_buf_min_2026-11-09_w9_rushdist"
    c["frozen_at_et"] = None
    c["game"] = {"home": "MIN", "away": "BUF", "season": 2026, "week_asof_exclusive": 9,
                 "kickoff_et": "2026-11-09T20:15:00-05:00", "game_id": GAME}
    c["history"]["teams"] = ["BUF", "MIN"]
    c["history"]["weeks_inclusive"] = list(range(1, 9))
    c["seed_base"] = 20261109
    c["set_label"] = "research_retro_week9_demo_not_prospective"
    return c


def actuals() -> dict:
    p = pd.read_parquet(PBP, columns=["game_id", "rush_attempt", "rusher_player_id", "rusher_player_name", "posteam",
                                      "rushing_yards", "two_point_attempt"])
    p = p[(p.game_id == GAME) & (p.rush_attempt == 1) & (p.two_point_attempt.fillna(0) != 1)]
    g = p.groupby(["posteam", "rusher_player_name"]).rushing_yards.sum()
    return {k: float(v) for k, v in g.items()}


def fd_lines(path: Path) -> dict:
    d = json.loads(path.read_text())
    data = d.get("response", d)
    data = data.get("data", data)
    out = {}
    for bk in data.get("bookmakers", []):
        if bk["key"] != "fanduel":
            continue
        for m in bk["markets"]:
            if m["key"] != "player_rush_yds":
                continue
            for o in m["outcomes"]:
                out.setdefault(o["description"], {})[o["name"]] = (o["point"], o["price"])
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20000)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--odds", type=Path)
    a = ap.parse_args(argv)
    if a.n > 20000:
        raise SystemExit("research demo is capped at n=20,000")
    from snapshots import lock as L
    from simulate import stable_seed
    from pipeline import rush_dist as RD
    cfg = research_cfg()
    seed = stable_seed(int(cfg["seed_base"]), int(cfg["game"]["week_asof_exclusive"]), cfg["config_id"])
    sim = L.run_sim(cfg, str(PBP), a.n, seed, a.workers)
    pb = sim["player_box"]
    assert pb["reconciliation"]["failures"] == 0 and pb["reconciliation"]["trials"] == a.n, pb["reconciliation"]
    head = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    meta = {"n": sim["n"], "seed": seed, "config_id": cfg["config_id"], "pbp": PBP.name, "code_commit": head,
            "chunks": sim["chunks"], "chunk_seeds": sim["chunk_seeds"], "runtime_sec": sim["runtime_sec"],
            "reconciliation": {k: pb["reconciliation"][k] for k in ("trials", "failures")},
            "points_mean": {"MIN": float(sim["arrays"]["fg_home"].mean()), "BUF": float(sim["arrays"]["fg_away"].mean())},
            "note": "retro Week 9 research demo (n<=20k), not a prospective run"}
    d = RD.build_from_box(pb["columns"], pb["values"], GAME, pbp_path=PBP, meta=meta)
    RD.write(d, HERE)
    act = actuals()
    lines = fd_lines(a.odds) if a.odds else {}
    rows, pits = [], []
    s = d["summary"]
    for r in s.sort_values(["team", "carries_mean"], ascending=[True, False]).itertuples():
        y = act.get((r.team, r.player))
        if y is None and r.p_any_carry < 0.5:
            continue
        pr = RD.p_under(d["cdf"], team=r.team, player=r.player, line=y) if y is not None else None
        pit = (pr["p_under"] + 0.5 * pr["p_push"]) if pr else np.nan
        if pr:
            pits.append(pit)
        fl = lines.get(r.full_name) if isinstance(r.full_name, str) else None
        ln = pu = nv = res = ""
        if fl and "Under" in fl and "Over" in fl:
            L_, pu_ = fl["Under"][0], RD.p_under(d["cdf"], team=r.team, player=r.player, line=fl["Under"][0])
            iu, io = (1 / (1 + (100 / -p if p < 0 else p / 100)) for p in (fl["Under"][1], fl["Over"][1]))
            ln, pu, nv = f"{L_:g}", f"{pu_['p_under']:.3f}", f"{iu / (iu + io):.3f}"
            res = "" if y is None else ("U" if y < L_ else "O")
        rows.append(f"| {r.team} | {r.player} | {r.position or '?'} | {r.carries_mean:.1f} | {r.mean:.1f} | "
                    f"{r.q10:g} / {r.q50:g} / {r.q90:g} | {'' if y is None else f'{y:g}'} | "
                    f"{'' if np.isnan(pit) else f'{pit:.3f}'} | {ln} | {pu} | {nv} | {res} |")
    in80 = float(np.mean([(0.1 <= p <= 0.9) for p in pits])) if pits else np.nan
    md = ["# Week 9 BUF@MIN rush-yards distribution demo (research only, n=%d)" % sim["n"], "",
          "Smoke test on ONE game; not a calibration result. PIT = P(X<actual)+0.5P(X=actual); a calibrated model "
          "puts PITs roughly uniform, ~80% inside [0.1, 0.9].", "",
          f"seed {seed}, chunks {sim['chunks']}, runtime {sim['runtime_sec']}s, box reconciliation failures "
          f"{pb['reconciliation']['failures']}/{pb['reconciliation']['trials']}; points mean MIN "
          f"{meta['points_mean']['MIN']:.1f} BUF {meta['points_mean']['BUF']:.1f}.", "",
          "| Team | Player | Pos | Car mean | Rush yds mean | p10 / p50 / p90 | Actual | PIT | FD line | P(under) model | "
          "FD no-vig under | Result |", "|---|---|---|---|---|---|---|---|---|---|---|---|", *rows, "",
          f"Players with an actual: {len(pits)}; PIT inside [0.1, 0.9]: {in80:.0%}; mean PIT {np.mean(pits):.3f} "
          "(0.5 = unbiased).", "",
          "FD lines: draft PR #41 data/odds_history/alt_test_week9/raw (historical snapshot, 0 new credits)."
          if lines else "No --odds file given: line columns blank."]
    (HERE / "demo_table.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
