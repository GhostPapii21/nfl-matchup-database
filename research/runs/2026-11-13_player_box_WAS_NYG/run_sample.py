"""NFL-75 sample: per-player box lines from the 100k engine path for 2026_10_WAS_NYG, n=20,000, vs the ESPN box.

Same config, as-of PBP and seed derivation as pipeline.sim100k.default_engine (snapshots/lock.run_sim ->
simulate.simulate_games), called directly because the game is over and sim100k's preflight correctly refuses
post-kickoff runs. n=20,000 is a sample, not a 100k. Research only; projection_ready stays false.
The ESPN box (event 401873052) is NOT committed (third-party data): save
https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event=401873052 next to this script as
espn_box_401873052.json (+ .retrieved_utc) to rebuild the comparison table; the committed table cites it.

  python research/runs/2026-11-13_player_box_WAS_NYG/run_sample.py [--n 20000] [--workers 4]"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ENGINE = ROOT / "core" / "possession_engine_v0"
sys.path[:0] = [str(ROOT), str(ENGINE)]
CFG = ENGINE / "config/was_nyg_2026-11-12_data_only_nfl43.json"
PBP = ROOT / "data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet"

# ESPN display name -> nflverse name in the W1-9 history (checked against the box columns; None = not found)
STATS = [("pass_att", "ATT"), ("pass_cmp", "CMP"), ("pass_yds", "PASS YDS"), ("sacks_taken", "SACKED"),
         ("int_thrown", "INT"), ("targets", "TGT"), ("rec", "REC"), ("rec_yds", "REC YDS"),
         ("carries", "CAR"), ("rush_yds", "RUSH YDS")]


def espn_lines(path: Path) -> dict:
    d = json.loads(path.read_text())
    out: dict = {}
    for t in d["boxscore"]["players"]:
        ab = {"WSH": "WAS"}.get(t["team"]["abbreviation"], t["team"]["abbreviation"])
        for cat in t["statistics"]:
            lab = cat["labels"]
            for a in cat["athletes"]:
                nm, s = a["athlete"]["displayName"], dict(zip(lab, a["stats"]))
                rec = out.setdefault((ab, nm), {})
                if cat["name"] == "passing":
                    c, att = s["C/ATT"].split("/")
                    rec.update(pass_cmp=int(c), pass_att=int(att), pass_yds=int(s["YDS"]), int_thrown=int(s["INT"]),
                               sacks_taken=int(s["SACKS"].split("-")[0]))
                elif cat["name"] == "rushing":
                    rec.update(carries=int(s["CAR"]), rush_yds=int(s["YDS"]))
                elif cat["name"] == "receiving":
                    rec.update(rec=int(s["REC"]), rec_yds=int(s["YDS"]), targets=int(s["TGTS"]))
    return {k: v for k, v in out.items() if v}


def nflverse_name(display: str, known: set) -> str | None:
    parts = [p for p in display.replace(".", ". ").split() if p not in ("Jr.", "II", "III", "Sr.")]
    cand = f"{parts[0][0]}.{parts[-1]}"
    return cand if cand in known else None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20000)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args(argv)
    from snapshots import lock as L
    from config_load import load_config
    from simulate import stable_seed
    import player_box as PB
    cfg = load_config(CFG)
    g = cfg["game"]
    seed = stable_seed(int(cfg["seed_base"]), int(g["week_asof_exclusive"]), cfg["config_id"])
    sim = L.run_sim(cfg, str(PBP), a.n, seed, a.workers)
    pb = sim["player_box"]
    rec = pb["reconciliation"]
    summ = PB.summarize(pb["columns"], pb["values"])
    tsum = PB.summarize([[t, "TEAM", s] for t, s in pb["team_columns"]], pb["team_values"])
    head = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    h, aw = sim["arrays"]["fg_home"], sim["arrays"]["fg_away"]
    meta = {"game_id": g["game_id"], "config_id": cfg["config_id"], "pbp": PBP.name, "n": sim["n"], "seed": seed,
            "chunks": sim["chunks"], "chunk_seeds": sim["chunk_seeds"], "workers": a.workers, "code_commit": head,
            "runtime_sec": sim["runtime_sec"], "reconciliation": rec, "n_box_columns": len(pb["columns"]),
            "points_mean": {g["home"]: float(h.mean()), g["away"]: float(aw.mean())},
            "espn_event": 401873052, "espn_retrieved_utc": (HERE / "espn_box_401873052.retrieved_utc").read_text().strip(),
            "research_only": True, "projection_ready": False}
    (HERE / "player_box_summary_n20000.json").write_text(json.dumps(
        {"meta": meta, "players": summ, "team": tsum}, indent=1, sort_keys=True) + "\n")
    espn = espn_lines(HERE / "espn_box_401873052.json")
    known = {(t, p) for t, p, _ in pb["columns"]}
    rows = ["| Team | Player (ESPN) | Engine name | Stat | ESPN actual | Sim median | Sim mean | Sim p10-p90 |",
            "|---|---|---|---|---|---|---|---|"]
    for (team, disp), act in sorted(espn.items(), key=lambda kv: (kv[0][0], -kv[1].get("targets", 0) - kv[1].get("carries", 0) - kv[1].get("pass_att", 0))):
        nv = nflverse_name(disp, {p for t, p in known if t == team})
        for stat, lab in STATS:
            if stat not in act:
                continue
            if nv is None:
                rows.append(f"| {team} | {disp} | not in W1-9 history | {lab} | {act[stat]} | n/a | n/a | n/a |")
                continue
            s = summ.get(team, {}).get(nv, {}).get(stat)
            if s is None:
                rows.append(f"| {team} | {disp} | {nv} | {lab} | {act[stat]} | 0 | 0.00 | 0-0 |")
            else:
                rows.append(f"| {team} | {disp} | {nv} | {lab} | {act[stat]} | {s['median']:g} | {s['mean']:.2f} | "
                            f"{s['p10']:g}-{s['p90']:g} |")
    (HERE / "sanity_table_n20000.md").write_text("\n".join(rows) + "\n")
    print(json.dumps(meta, indent=1))
    print("\n".join(rows))


if __name__ == "__main__":
    main()
