"""WAS@NYG Nov 12 (2026 Week 10) sanity table: name-locked recorder (main) vs the Phase 2 opportunity model, same
engine run, n=20,000, seed 20261112, config core/possession_engine_v0/config/was_nyg_2026-11-12_data_only_nfl43.json,
model models/model_2026_w10_WAS_NYG.json (fit on data through 2026 Week 9). PROJECTION ONLY: no Week 10 actual is
read or graded here (Weeks 10-12 are the untouched holdout).
    python3 research/runs/2026-11-13_opportunity_phase2/run_sanity_was_nyg.py
Research only. projection_ready stays false."""
from __future__ import annotations
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
ENG = REPO / "core/possession_engine_v0"
sys.path.insert(0, str(ENG))
import simulate  # noqa: E402

N, SEED = 20_000, 20261112
CFG = ENG / "config/was_nyg_2026-11-12_data_only_nfl43.json"
PBP = REPO / "data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet"
MODEL = HERE / "models/model_2026_w10_WAS_NYG.json"


def col(box, t, p, s):
    for j, c in enumerate(box["columns"]):
        if tuple(c) == (t, p, s):
            return box["values"][:, j]
    return np.zeros(box["values"].shape[0])


def tcol(box, t, s):
    for j, c in enumerate(box["team_columns"]):
        if tuple(c) == (t, s):
            return box["team_values"][:, j]
    return np.zeros(box["team_values"].shape[0])


def main():
    cfg = json.loads(CFG.read_text())
    model = json.loads(MODEL.read_text())
    t0 = time.time()
    o = simulate.simulate_games(cfg, pbp_path=str(PBP), n=N, seed=SEED, opportunity_model=model)
    nb, ob = o["player_box"], o["player_box_opportunity"]
    L = ["# WAS@NYG 2026-11-12 sanity table (projection only, Week 10 never graded)", "",
         f"Same engine run for both columns: n={N}, seed={SEED}, runtime {time.time() - t0:.0f}s. Model "
         f"`{MODEL.name}` sha256 {hashlib.sha256(MODEL.read_bytes()).hexdigest()[:16]} (fit on 2024-2025 + 2026 Weeks 1-9). "
         f"Reconciliation failures: name-locked {nb['reconciliation']['failures']}/{N}, opportunity "
         f"{ob['reconciliation']['failures']}/{N}. Game arrays are byte-identical with the model on or off (tests).", ""]
    for team in ("NYG", "WAS"):
        L += [f"## {team}", "", "Team totals per game (identical in both recorders): pass_att "
              f"{tcol(nb, team, 'pass_att').mean():.1f}, targets {tcol(nb, team, 'targets').mean():.1f}, carries "
              f"{tcol(nb, team, 'carries').mean():.1f}.", "",
              "| player | pos | report status | pass_att main | pass_att opp | P(INT>=1) main | P(INT>=1) opp | carries main | carries opp | targets main | targets opp | rz targets opp | i5 carries opp | P(any TD) opp |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        cands = {}
        for slot, lst in model["teams"][team]["candidates"].items():
            for c in lst:
                cands.setdefault(c["name"], c)
        names = {c[1] for c in nb["columns"] if c[0] == team} | {c[1] for c in ob["columns"] if c[0] == team}
        rows = []
        for p in names:
            vals = {s: (col(nb, team, p, s).mean(), col(ob, team, p, s).mean())
                    for s in ("pass_att", "carries", "targets")}
            if max(max(v) for v in vals.values()) < 0.5:
                continue
            pint = ((col(nb, team, p, "int_thrown") > 0).mean(), (col(ob, team, p, "int_thrown") > 0).mean())
            td = (col(ob, team, p, "rec_td") + col(ob, team, p, "rush_td") > 0).mean()
            c = cands.get(p, {})
            rows.append((-(vals["pass_att"][1] * 3 + vals["carries"][1] + vals["targets"][1]),
                         f"| {p} | {c.get('pos', 'not a candidate')} | {c.get('status') or ('-' if c else 'n/a')} | "
                         f"{vals['pass_att'][0]:.1f} | {vals['pass_att'][1]:.1f} | {pint[0]:.3f} | {pint[1]:.3f} | "
                         f"{vals['carries'][0]:.1f} | {vals['carries'][1]:.1f} | {vals['targets'][0]:.1f} | "
                         f"{vals['targets'][1]:.1f} | {col(ob, team, p, 'rz_targets').mean():.2f} | "
                         f"{col(ob, team, p, 'i5_carries').mean():.2f} | {td:.3f} |"))
        L += [r for _, r in sorted(rows)] + [""]
    L += ["UNASSIGNED (main) = rows whose names the engine nulled (foreign rows) or that had no name; UNLISTED (opp) = "
          "the fitted share for players outside the candidate list. Snaps: unknown (no snap model; nflverse snap "
          "counts in the repo stop at Week 7).", ""]
    (HERE / "sanity_was_nyg_n20000.md").write_text("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
