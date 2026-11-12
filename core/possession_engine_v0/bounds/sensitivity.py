"""NFL-43 review D6: reproduce the SEMANTICS_BOUNDS.md section 4 sensitivity table.

    python3 core/possession_engine_v0/bounds/sensitivity.py                  # n=6000 per arm, seed 777, writes JSON
    python3 core/possession_engine_v0/bounds/sensitivity.py --n 300 --out /tmp/s.json   # quick check

Arms (same config, same seed, same committed W1-9 PBP):
  legacy            no cfg["semantics"] (all three paths UNSUPPORTED)
  penalties_only    penalties canonical_log_v1
  returns_only      returns asof_league_v1 (league kick/punt return-TD rate + league defensive-return pool)
  official_ot_only  overtime official_2025_regular_season
  all_nfl43         all three
  DIAG_all_nfl43_h2h_off   all three, head-to-head defense conditioning switched off IN MEMORY for this run only
                           (diagnostic for review D7; the engine default is unchanged)

Never a 100k run (n is capped at 20,000). No network, no API credits. Output label: research only, not validated.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ENGINE = HERE.parent
REPO = HERE.parents[2]
CFG = ENGINE / "config/was_nyg_2026-11-12_data_only_nfl43.json"
PBP = REPO / "data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet"
OUT = HERE / "sensitivity_was_nyg_w10.json"
MAX_N = 20_000
ALL = {"penalties": "canonical_log_v1", "returns": "asof_league_v1", "overtime": "official_2025_regular_season"}
ARMS = {
    "legacy": None,
    "penalties_only": {"penalties": "canonical_log_v1"},
    "returns_only": {"returns": "asof_league_v1"},
    "official_ot_only": {"overtime": "official_2025_regular_season"},
    "all_nfl43": ALL,
    "DIAG_all_nfl43_h2h_off": ALL,
}


def _run_arm(args):
    name, sem, n, seed = args
    sys.path.insert(0, str(ENGINE))
    from config_load import load_config
    import simulate
    cfg = copy.deepcopy(load_config(CFG))
    if sem is None:
        cfg.pop("semantics", None)
    else:
        cfg["semantics"] = dict(sem)
    if name.startswith("DIAG_") and "h2h_off" in name:
        simulate.PlayCatalog.enable_defense_conditioning = lambda self, enabled=True: setattr(self, "_defense_cond", False)
    out = simulate.simulate_games(cfg, pbp_path=str(PBP), n=n, seed=seed)
    A = out["arrays"]
    h, a = cfg["game"]["home"], cfg["game"]["away"]
    hp, ap = A["fg_home"].astype(float), A["fg_away"].astype(float)
    ev = out["evidence_summary"]
    return name, {
        "n": n, "seed": seed, "semantics": sem or "LEGACY_UNSUPPORTED",
        f"{h}_pts": round(hp.mean(), 2), f"{a}_pts": round(ap.mean(), 2), "total": round((hp + ap).mean(), 2),
        f"{h}_margin": round((hp - ap).mean(), 2), f"P_{h}_win": round(float((hp > ap).mean()), 3),
        "P_tie": round(float((hp == ap).mean()), 3), "P_ot": round(float(A["went_ot"].mean()), 3),
        "flags_per_game": round(float(A["n_pen"].mean()), 2),
        f"pen_yds_{h}": round(float(A["pen_yds_home"].mean()), 1), f"pen_yds_{a}": round(float(A["pen_yds_away"].mean()), 1),
        "kick_punt_return_tds_per_game": round(float((A["ret_td_home"] + A["ret_td_away"]).mean()), 4),
        "def_return_tds_per_game": round(float((A["def_td_home"] + A["def_td_away"]).mean()), 4),
        "se_total": round(float((hp + ap).std(ddof=1) / np.sqrt(n)), 3),
        "se_margin": round(float((hp - ap).std(ddof=1) / np.sqrt(n)), 3),
        "def_cond_snap_flags_per_game": round(ev["defense_cond_flag_events"] / n, 1),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=6000)
    ap.add_argument("--seed", type=int, default=777)
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args(argv)
    if a.n > MAX_N:
        print(f"refused: n={a.n} > {MAX_N}; this script never runs 100k (NFL-43 AC4).")
        return 2
    jobs = [(k, v, a.n, a.seed) for k, v in ARMS.items()]
    with ProcessPoolExecutor(max_workers=a.workers) as ex:
        res = dict(ex.map(_run_arm, jobs))
    try:
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
    except OSError:
        head = "unknown"
    doc = {"label": "research only, not validated",
           "generated_by": "core/possession_engine_v0/bounds/sensitivity.py",
           "run_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "code_head": head, "config": str(CFG.relative_to(REPO)),
           "pbp": str(PBP.relative_to(REPO)), "pbp_sha256": hashlib.sha256(PBP.read_bytes()).hexdigest(),
           "pbp_pulled_et": "2026-11-12 11:16 AM ET",
           "note": ("Arms differ only in cfg['semantics']; the DIAG arm also turns off head-to-head defense "
                    "conditioning in memory. Nothing tuned, no weights changed."),
           "arms": res}
    Path(a.out).write_text(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(doc, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
