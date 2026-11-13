"""Shared harness for test_player_box.py: full-output digests of simulate_games (game results and every pre-existing
output block) so the NFL-75 per-player box recorder can be shown to be observational only.

Golden digests were computed on main 3dad900 (before the recorder existed) with this same harness."""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parents[1]
PBP = REPO / "data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet"
CFG_WAS_NYG = HERE / "config/was_nyg_2026-11-12_data_only_nfl43.json"
CFG_DEF_ALLOWED = HERE / "config/research_variant_def_allowed_w05.json"


def _jsonable(x):
    if isinstance(x, np.ndarray):
        return [_jsonable(v) for v in x.tolist()]
    if isinstance(x, dict):
        return {str(k): _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating, float)):
        return repr(float(x))
    if isinstance(x, (np.bool_,)):
        return bool(x)
    return x


def variant_cfg(name: str) -> tuple[dict, tuple]:
    """(cfg, research_unaccepted) for a named golden variant."""
    if name == "def_allowed_w05":
        return json.loads(CFG_DEF_ALLOWED.read_text()), ()
    c = json.loads(CFG_WAS_NYG.read_text())
    if name == "was_nyg_lock":
        return c, ()
    if name == "was_nyg_h2h_legacy":  # h2h pool every snap + legacy accounting (kneels/spikes stay in the pool)
        c.setdefault("defense_interaction", {})["h2h"] = "legacy_always"
        c["accounting"] = "legacy"
        return c, ()
    if name == "was_nyg_rare_research":
        c["semantics"]["rare_plays"] = "asof_league_v1"
        return c, ("rare_plays",)
    raise KeyError(name)


VARIANTS = ("was_nyg_lock", "was_nyg_h2h_legacy", "def_allowed_w05", "was_nyg_rare_research")
SEEDS = (20261112, 7)
N = 100

# Output blocks that existed on main 3dad900. The recorder must leave every one of them byte-identical.
BLOCKS = ("arrays", "special_teams_counts", "player_joint", "player_samples", "evidence_summary", "status",
          "n_completed", "seed", "rare_band_usage")


def digest(out: dict) -> dict:
    return {b: hashlib.sha256(json.dumps(_jsonable(out.get(b)), sort_keys=True).encode()).hexdigest()[:16]
            for b in BLOCKS}


def run(name: str, n: int, seed: int, **kw) -> dict:
    sys.path.insert(0, str(HERE))
    import simulate
    cfg, ru = variant_cfg(name)
    return simulate.simulate_games(cfg, pbp_path=str(PBP), n=n, seed=seed, research_unaccepted=ru, **kw)


if __name__ == "__main__":  # print golden digests (run on main before the recorder existed)
    out = {}
    for name in VARIANTS:
        for seed in SEEDS:
            out[f"{name}|{seed}"] = digest(run(name, N, seed))
    print(json.dumps(out, indent=1, sort_keys=True))
