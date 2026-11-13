"""NFL-75 Phase 2b refit for eval weeks (python3 -m calibration.opportunity_fit2b 4 5 6 7 8 9 10): carry/target slots
with the point-in-time depth signal (staged search starting from the frozen Phase 2 fit for the same week), EB m with
the extended grid (past 5000). Dropback and availability unchanged. Writes phase2b/params/params_2026_wNN.json.
Uses only data before each eval week (train_set / lik_rows leakage guards). Research only; zero network or credits."""
import json, sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parents[1]))
from concurrent.futures import ProcessPoolExecutor
from calibration import opportunity_fit as F
RUN = F.ROOT / "research/runs/2026-11-13_opportunity_phase2"
OUT = F.ROOT / "research/runs/2026-11-13_opportunity_phase2b/params"
def one(w):
    p = json.loads((RUN / f"params/params_2026_w{w:02d}.json").read_text())
    p["phase"] = "2b"; p["phase2_params_sha_source"] = f"research/runs/2026-11-13_opportunity_phase2/params/params_2026_w{w:02d}.json"
    for slot in ("carry", "target"):
        p["slots"][slot] = F.fit_slot_depth(F.train_set(2026, w, slot), p["slots"][slot])
    rows = F.lik_rows(2026, w)
    for slot in F.SLOTS:
        p["lik"][slot] = F.fit_m(rows, slot, 2026, w)
    return w, p


def main(argv=None):
    ws = [int(x) for x in (argv if argv is not None else sys.argv[1:])]
    if any(w > F.HOLDOUT_FIRST_WEEK for w in ws):
        raise SystemExit("eval weeks > 10 are not fitted here (week 10 = the frozen pregame fit on data <= week 9)")
    OUT.mkdir(parents=True, exist_ok=True)
    with ProcessPoolExecutor(len(ws)) as ex:
        for w, p in ex.map(one, ws):
            (OUT / f"params_2026_w{w:02d}.json").write_text(json.dumps(p, indent=1, default=str) + "\n")
            print("froze", w, flush=True)


if __name__ == "__main__":
    main()
