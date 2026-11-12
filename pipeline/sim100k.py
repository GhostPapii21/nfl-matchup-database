"""The single 100k-trial entry point (NFL-56 item 3). Fails closed.

    python -m pipeline.sim100k --game 2026_10_WAS_NYG

It refuses, printing every reason and exiting 2, unless ALL of these pass:
  G1 flags      known_flags/KNOWN_LIMITATIONS.json readable and "DEFERRED_100K" is false
  G2 NFL-43     SEMANTICS_BOUNDS.md exists and no semantics are listed unsupported (BetGuru)
  G3 packet     pregame/packets/<game>/packet.json exists
  G4 freshness  every source in pipeline/freshness.py is FRESH or NOT_REQUIRED, including the newest four-book
                price freeze (Blitz) and official inactives pulled after T-90
  G5 phases     phases 1-13 and 15 are not MISSING / STALE / NOT_YET
  G6 rocket     BetGuru's `rocket` validation command exits 0 for this game (pipeline/hooks.py ROCKET_COMMAND)
                -- run only after G1-G5 pass, so a refusal never costs a validation run
There is no override flag, environment variable or "force" switch, by design. The trial count is fixed at 100,000.

Only when every gate passes does it run the existing period engine (core/period_engine_v0/monte_carlo.simulate_game,
unchanged) for 100,000 trials and write pipeline/ledgers/<game>.sim100k.json. Output stays research only and
projection_ready stays false; flipping it is Rico's decision through NFL-49, never this script's.
No network, no API credits.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import freshness, hooks, phases as PH

TRIALS = 100_000
SEED = 20261112
EXIT_REFUSED = 2
GATE_PHASES = [n for n in PH.PHASES if n != 14]   # 14 is this entry point itself


def preflight(pk: dict | None, now: datetime | None = None, flags: dict | None = None, hook_impls=None,
              include_phases: bool = True, rocket_impl=None, rocket_command=None, root: Path | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    flags = hooks.known_flags() if flags is None else flags
    reasons, gates = [], {}

    if "_error" in flags:
        gates["G1_flags"] = "REFUSED"; reasons.append(f"G1: {flags['_error']}")
    elif flags.get("DEFERRED_100K") is not False:
        gates["G1_flags"] = "REFUSED"; reasons.append("G1: DEFERRED_100K is set in known_flags/KNOWN_LIMITATIONS.json (100k runs are deferred).")
    else:
        gates["G1_flags"] = "PASS"

    sem = hooks.nfl43_semantics(flags, root=root or hooks.ROOT)
    gates["G2_nfl43"] = "PASS" if sem["status"] == "OK" else "REFUSED"
    if sem["status"] != "OK":
        reasons.append("G2: " + sem["reason"])

    if not pk:
        gates["G3_packet"] = "REFUSED"; reasons.append("G3: no pregame packet for this game.")
    else:
        gates["G3_packet"] = "PASS"
        rows = freshness.check(pk, now, hook_impls)
        bad = freshness.blocking(rows)
        gates["G4_freshness"] = "PASS" if not bad else "REFUSED"
        reasons += [f"G4: {r['source']} {r['status']}: {r['reason']}" for r in bad]
        if include_phases:
            led = PH.ledger(pk, now, phases=GATE_PHASES, hook_impls=hook_impls, gate={"ran": True})
            badp = [p for p in led["phases"] if p["status"] in PH.BLOCKING]
            gates["G5_phases"] = "PASS" if not badp else "REFUSED"
            reasons += [f"G5: phase {p['phase']} ({p['name']}) is {p['status']}" for p in badp]

    if reasons:
        gates["G6_rocket"] = "NOT_RUN (earlier gates refused)"
    else:
        gid = (pk.get("game") or {}).get("game_id")
        r = hooks.rocket_validation(gid, impl=rocket_impl, command=rocket_command)
        gates["G6_rocket"] = "PASS" if r.get("status") == "PASS" else "REFUSED"
        if r.get("status") != "PASS":
            reasons.append("G6: " + r.get("reason", "rocket did not pass"))
    return {"ran": not reasons, "ok": not reasons, "gates": gates, "reasons": reasons, "checked_utc": now.isoformat(timespec="seconds")}


def default_engine(pk: dict, trials: int, seed: int) -> dict:
    """Existing period engine, called exactly as pregame/packet.py does, only with 100k trials. Formulas unchanged."""
    import pandas as pd  # noqa: F401  (engine dependency)
    root = hooks.ROOT
    sys.path.insert(0, str(root / "core" / "period_engine_v0"))
    from reconstruct import load_pbp, period_table_from_pbp, as_of_mask, resolve_pbp_path
    from monte_carlo import simulate_game
    g = pk["game"]
    pbp = resolve_pbp_path(root / "core" / "period_engine_v0" / "data" / f"play_by_play_{g['season']}.parquet")
    hist = period_table_from_pbp(load_pbp(pbp))
    asof = hist[as_of_mask(hist, g["season"], g["week"])]
    sim = simulate_game(asof, g["home"], g["away"], n=trials, seed=seed, sampling="matchup_pair")
    if sim.get("error"):
        raise RuntimeError(sim["error"])
    return {"engine": "core/period_engine_v0 matchup_pair", "summaries": sim["summaries"]}


def run(game_id: str, packet: Path | None = None, engine=default_engine, **kw) -> tuple[int, dict]:
    try:
        pk = PH.load_packet(game_id, packet)
    except (OSError, ValueError):
        pk = None
    pf = preflight(pk, **kw)
    report = {"schema": "nfl56-sim100k/1", "game_id": game_id, "trials_requested": TRIALS, "projection_ready": False,
              "research_only": True, **pf}
    if not pf["ok"]:
        report["status"] = "REFUSED"
        return EXIT_REFUSED, report
    try:
        report["result"] = engine(pk, TRIALS, SEED)
        report["status"] = "RAN_RESEARCH_ONLY"
        return 0, report
    except Exception as e:  # engine failure is a refusal too, never a partial result
        report.update(status="REFUSED", ran=False, ok=False, reasons=[f"engine failed: {e!r}"])
        return EXIT_REFUSED, report


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="NFL-56 fail-closed 100k entry point (no override).")
    ap.add_argument("--game", required=True)
    ap.add_argument("--packet", type=Path)
    ap.add_argument("--write", action="store_true", help="write pipeline/ledgers/<game>.sim100k.json")
    a = ap.parse_args(argv)
    code, rep = run(a.game, a.packet)
    if rep["status"] == "REFUSED":
        print(f"sim100k: REFUSED for {a.game}. Nothing was simulated. Reasons:")
        for r in rep["reasons"]:
            print(f"  - {r}")
    else:
        print(f"sim100k: ran {TRIALS:,} trials for {a.game} (research only; projection_ready stays false).")
    if a.write:
        PH.LEDGERS.mkdir(parents=True, exist_ok=True)
        (PH.LEDGERS / f"{a.game}.sim100k.json").write_text(json.dumps(rep, indent=1, default=str) + "\n")
    return code


if __name__ == "__main__":
    sys.exit(main())
