"""Player simulations for the Sunday slate: the restored sim_v6 and the sim_v6r1 replacement triad.

    python -m sunday sim --date 2026-11-29 --as-of 2026-11-29T12:00:00+00:00 --trials 100000 --concurrency 4

For each game, a separate process:
  * Builds the leg universe with sim_v6.universe() (the original usage thresholds) for both teams. A player is kept
    only if he appeared in his team's most recent game, which stands in for inactives. No week-12 injury file is
    committed.
  * Runs every ACCEPTED sim_v6r1 method at --trials trials for each of the four margin scenarios (three named plus the
    residual upset bin). Acceptance is read from research/sim_v6_recovery/validation.json, and the multipliers from
    tools/sim_v6r1_calib.json.
  * Runs the restored sim_v6 (mc, bias, gr) at --trials trials, unconditional, with tools/sim_v6_calib.json, as the
    labelled original reference.
  * Records wall time and peak RSS (the child's ru_maxrss).
A missing calibration or validation file blocks the run. Nothing is substituted.

The spread is the packet's market.home_spread (pregame/packets/<game>/packet.json). Data is the committed nflverse PBP
through week 11, cut at the --as-of date.
Research only. projection_ready stays false. No betting rule, lock or grade is read or written.
"""
from __future__ import annotations

import hashlib
import json
import os
import resource
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
CALIB_R1 = TOOLS / "sim_v6r1_calib.json"
CALIB_V6 = TOOLS / "sim_v6_calib.json"
VALIDATION = ROOT / "research" / "sim_v6_recovery" / "validation.json"
SCHEMA = "sunday-sim-triad/1"


class Blocked(Exception):
    pass


def accepted_methods(validation: Path | None = None) -> tuple[list[str], dict]:
    validation = validation or VALIDATION
    if not validation.exists():
        raise Blocked(f"validation file missing: {validation}")
    v = json.loads(validation.read_text())["verdict"]["sim_v6r1"]
    return [k.split(":", 1)[1] for k, d in v.items() if d["accepted"]], v


def load_calib(path: Path) -> dict:
    if not path.exists():
        raise Blocked(f"calibration file missing: {path}")
    return json.loads(path.read_text())["multipliers"]


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def legs_for_game(E, V6, home: str, away: str, home_spread: float, game_id: str) -> list[dict]:
    p = E.p
    last_gid = {t: E.tg[E.tg.posteam == t].sort_values("date").game_id.iloc[-1] for t in (home, away)}
    names = V6._PL.set_index("gsis_id").display_name.to_dict()
    legs = []
    for g, mkt in V6.universe(E):
        q = p[(p.passer_player_id == g) | (p.receiver_player_id == g) | (p.rusher_player_id == g)]
        if q.empty:
            continue
        last = q.sort_values("game_date").iloc[-1]
        team = last.posteam
        if team not in (home, away) or last.game_id != last_gid[team]:
            continue
        opp = away if team == home else home
        spread = float(home_spread) if team == home else -float(home_spread)
        legs.append(dict(player=g, gsis=g, name=names.get(g, g), team=team, opp=opp, market=mkt, spread=spread,
                         team_is_fav=(spread < 0) or (spread == 0 and team == home), rungs=[], game_id=game_id))
    return legs


def run_one(job: dict) -> dict:
    """Runs in a child process (max_tasks_per_child=1), so ru_maxrss is this game's peak."""
    t0 = time.perf_counter()
    sys.path.insert(0, str(TOOLS))
    import simsrc
    src = simsrc.prepare()
    import sim_v6_ab2144f0 as V6
    import sim_v6r1 as R
    gid, out = job["game_id"], Path(job["out"])
    out.mkdir(parents=True, exist_ok=True)
    n = int(job["trials"]); methods = job["methods"]
    Er = R.Engine(cutoff=job["cutoff"], n=n, calib=job["calib_r1"])
    E6 = V6.Engine(cutoff=job["cutoff"], calib=job["calib_v6"], n=n)
    legs = legs_for_game(Er, V6, job["home"], job["away"], job["home_spread"], gid)
    scen = R.NAMED + ("residual",)
    res_r1, res_v6, errors = [], [], []
    trials = {"sim_v6r1": 0, "sim_v6": 0}
    for leg in legs:
        try:
            o, info = Er.sim_r1(dict(leg), scenarios=scen, methods=methods)
            probs = R.scenario_probs(leg["spread"], leg["team_is_fav"])
            for m in o:
                o[m]["mixture_mean"] = float(sum(probs[s] * o[m][s]["mean"] for s in scen))
            res_r1.append(dict(leg=leg, scenario_probs=probs, methods=o, info=info))
            trials["sim_v6r1"] += n * len(methods) * len(scen)
        except Exception as e:  # one leg's failure is recorded, the rest still run
            errors.append(dict(leg=leg, engine="sim_v6r1", error=repr(e)))
        try:
            o6, i6 = E6.sim(dict(leg))
            res_v6.append(dict(leg=leg, modes=o6, info=i6)); trials["sim_v6"] += n * len(V6.MODES)
        except Exception as e:
            errors.append(dict(leg=leg, engine="sim_v6", error=repr(e)))
    wall = time.perf_counter() - t0
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    common = dict(game_id=gid, as_of=job["as_of"], cutoff=job["cutoff"], home=job["home"], away=job["away"],
                  home_spread=job["home_spread"], spread_source=job["spread_source"], inputs=src,
                  projection_ready=False, inactives="UNVERIFIED (appeared in team's last game)")
    r1 = dict(schema=SCHEMA, engine="sim_v6r1", is_original_sim_v6=False, not_sim_v6=True, methods=methods,
              scenarios=list(scen), trials_per_method_per_scenario=n, legs=len(res_r1), results=res_r1,
              calib_file=str(CALIB_R1.relative_to(ROOT)), calib_sha256=job["calib_r1_sha"],
              code_sha256=_sha(TOOLS / "sim_v6r1.py"), **common)
    v6 = dict(schema=SCHEMA, engine="sim_v6", is_original_sim_v6=True, modes=list(V6.MODES), scenarios=["unconditional"],
              trials_per_mode=n, legs=len(res_v6), results=res_v6, calib_file=str(CALIB_V6.relative_to(ROOT)),
              calib_sha256=job["calib_v6_sha"], code_sha256=_sha(TOOLS / "sim_v6_ab2144f0.py"),
              note="original engine, unchanged; mc and bias ignore game script, so it has no scenario split", **common)
    (out / "sim_v6r1.json").write_text(json.dumps(r1, default=float))
    (out / "sim_v6.json").write_text(json.dumps(v6, default=float))
    bench = dict(game_id=gid, legs=len(legs), errors=len(errors), trials=trials, wall_seconds=round(wall, 2),
                 peak_rss_mb=round(rss / 1024, 1), result="PASS" if legs and not errors else ("PARTIAL" if legs else "BLOCKED"))
    (out / "errors.json").write_text(json.dumps(errors, default=float))
    (out / "benchmark.json").write_text(json.dumps(bench))
    return bench


def run_slate(entries: list[dict], *, repo: Path, out: Path, as_of: datetime, trials: int = 100_000,
              concurrency: int = 4, methods: list[str] | None = None) -> dict:
    accepted, verdict = accepted_methods()
    chosen = methods or accepted
    rejected = [m for m in chosen if m not in accepted]
    if rejected:
        raise Blocked(f"methods not accepted by validation: {rejected}")
    if not chosen:
        raise Blocked("no sim_v6r1 method is accepted")
    if not entries:
        raise Blocked("no games to run")
    calib_r1, calib_v6 = load_calib(CALIB_R1), load_calib(CALIB_V6)
    cutoff = as_of.date().isoformat()
    jobs = []
    for e in entries:
        pk = json.loads((repo / "pregame" / "packets" / e["game_id"] / "packet.json").read_text())
        hs = (pk.get("market") or {}).get("home_spread")
        if hs is None:
            raise Blocked(f"{e['game_id']}: packet has no market.home_spread")
        jobs.append(dict(game_id=e["game_id"], home=e["home"], away=e["away"], home_spread=float(hs),
                         spread_source=f"pregame/packets/{e['game_id']}/packet.json market.home_spread "
                                       f"(packet generated {pk.get('generated_utc')})",
                         as_of=as_of.isoformat(), cutoff=cutoff, trials=trials, methods=chosen,
                         calib_r1=calib_r1, calib_v6=calib_v6, calib_r1_sha=_sha(CALIB_R1), calib_v6_sha=_sha(CALIB_V6),
                         out=str(out / e["game_id"])))
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()
    workers = max(1, min(concurrency, 8, len(jobs)))
    with ProcessPoolExecutor(max_workers=workers, max_tasks_per_child=1) as ex:
        games = list(ex.map(run_one, jobs))
    wall = time.perf_counter() - t0
    summary = dict(schema=SCHEMA, as_of=as_of.isoformat(), trials_per_method_per_scenario=trials, methods=chosen,
                   validation_verdict=verdict, concurrency=workers, slate_wall_seconds=round(wall, 2),
                   cpu_count=os.cpu_count(), games=games,
                   total_trials={k: sum(g["trials"][k] for g in games) for k in ("sim_v6r1", "sim_v6")},
                   max_peak_rss_mb=max(g["peak_rss_mb"] for g in games), projection_ready=False,
                   result="PASS" if all(g["result"] == "PASS" for g in games) else "PARTIAL")
    (out / "benchmark.json").write_text(json.dumps(summary, indent=1))
    lines = [f"# Sunday sims, as of {as_of.isoformat()}", "",
             f"sim_v6r1 methods {', '.join(chosen)} at {trials:,} trials per method per scenario (4 scenarios); "
             f"restored sim_v6 at {trials:,} per mode. Concurrency {workers}. Slate wall {wall:.0f}s. "
             "projection_ready false.", "",
             "| Game | Legs | Errors | sim_v6r1 trials | sim_v6 trials | Wall s | Peak RSS MB | Result |",
             "|---|---|---|---|---|---|---|---|"]
    for g in games:
        lines.append(f"| {g['game_id']} | {g['legs']} | {g['errors']} | {g['trials']['sim_v6r1']:,} | "
                     f"{g['trials']['sim_v6']:,} | {g['wall_seconds']} | {g['peak_rss_mb']} | {g['result']} |")
    (out / "INDEX.md").write_text("\n".join(lines) + "\n")
    return summary
