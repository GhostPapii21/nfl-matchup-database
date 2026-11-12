"""Re-grade a calibration.backtest per-game CSV against the close (lines file read from a copy whose sha256 matches
data/lines/README.md). Used because commit ba83615 is not in this checkout's object store."""
import sys, json, hashlib
sys.path.insert(0, sys.argv[1])
import pandas as pd
from calibration import backtest as bt
lines_path, per_csv, out = sys.argv[2], sys.argv[3], sys.argv[4]
raw = open(lines_path, 'rb').read(); h = hashlib.sha256(raw).hexdigest()
assert h == bt.LINES_SHA256, h
lines = pd.read_csv(lines_path, dtype={"game_id": str, "book": str, "line_type": str})
close = bt.close_for_games(lines)
per = pd.read_csv(per_csv)
actual = {r.game_id: {"home": int(r.act_home), "away": int(r.act_away)} for r in per.itertuples()}
keep = ["game_id","arm","week","home","away","n","status","sim_home","sim_away","sim_total","sim_margin","sim_total_sd","sim_margin_sd","p_home_win"]
rows = per[keep].to_dict("records")
g = bt.grade(rows, actual, close)
res = {k: v for k, v in g["by_arm"]["new_off"].items()}
doc = {"label": "research only, not validated", "regraded_from": per_csv.split('/')[-1], "lines_sha256": h, "lines_ref": "ba83615:data/lines/lines_wk04_09_2026.csv",
       "games_with_close": len([x for x in actual if x in close]), "results_new_off": res}
open(out, "w").write(json.dumps(doc, indent=1, default=float) + "\n")
r = res
print({k: (round(r[k], 4) if isinstance(r.get(k), float) else r.get(k)) for k in ["games","brier_model","brier_close_devig","logloss_model","logloss_close_devig","mae_total","mae_total_close","mae_margin","mae_margin_close","total_bias_sim_minus_actual","mean_sim_total","corr_model_total_vs_close","corr_model_margin_vs_close"]})
