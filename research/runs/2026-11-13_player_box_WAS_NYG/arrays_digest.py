import sys, json, hashlib
root = sys.argv[1]; n = int(sys.argv[2])
sys.path[:0] = [root, root + "/core/possession_engine_v0"]
from snapshots import lock as L
from config_load import load_config
from simulate import stable_seed
import numpy as np
cfg = load_config(root + "/core/possession_engine_v0/config/was_nyg_2026-11-12_data_only_nfl43.json")
g = cfg["game"]
seed = stable_seed(int(cfg["seed_base"]), int(g["week_asof_exclusive"]), cfg["config_id"])
sim = L.run_sim(cfg, root + "/data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet", n, seed, 4)
a = sim["arrays"]
d = {k: hashlib.sha256(np.ascontiguousarray(a[k]).tobytes()).hexdigest()[:16] for k in sorted(a)}
allh = hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest()[:16]
joint = hashlib.sha256(json.dumps(sim["joint"], sort_keys=True).encode()).hexdigest()[:16]
print(json.dumps({"root": root, "n": sim["n"], "seed": seed, "arrays_digest": allh, "joint_digest": joint,
                  "fg_home_sum": int(a["fg_home"].sum()), "fg_away_sum": int(a["fg_away"].sum()),
                  "has_player_box": bool(sim.get("player_box"))}))
