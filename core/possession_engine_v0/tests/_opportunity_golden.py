"""Shared harness for test_opportunity.py (NFL-75 Phase 2, player opportunity model).

Golden digests were computed on main 6bc0c54 (PR #36 merged, BEFORE the opportunity model existed) with this same
harness: every output block of simulate_games that existed on main, INCLUDING the name-locked player_box recorder
output (columns, per-trial values, team ledger, reconciliation). The opportunity model is opt-in; with it off the
output must be byte-identical, and with it on every one of these blocks must still be byte-identical (it only adds a
new "player_box_opportunity" block from its own RNG stream)."""
from __future__ import annotations
import hashlib
import json

import _player_box_golden as PBG

VARIANTS = PBG.VARIANTS
SEEDS = PBG.SEEDS
N = PBG.N
BLOCKS = PBG.BLOCKS + ("player_box",)


def digest(out: dict) -> dict:
    return {b: hashlib.sha256(json.dumps(PBG._jsonable(out.get(b)), sort_keys=True).encode()).hexdigest()[:16]
            for b in BLOCKS}


def run(name: str, n: int, seed: int, **kw) -> dict:
    return PBG.run(name, n, seed, **kw)


if __name__ == "__main__":  # print golden digests (run on main 6bc0c54 before the opportunity model existed)
    out = {}
    for name in VARIANTS:
        for seed in SEEDS:
            out[f"{name}|{seed}"] = digest(run(name, N, seed))
    print(json.dumps({"computed_on": "main 6bc0c54 (2026-11-13, PR #36 merged, before the NFL-75 Phase 2 "
                      "opportunity model existed)", "harness": "tests/_opportunity_golden.py", "n": N,
                      "digests": out}, indent=1, sort_keys=True))
