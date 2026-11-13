"""The single 100k-trial entry point (NFL-56 item 3). Fails closed.

    python -m pipeline.sim100k --game 2026_10_WAS_NYG

It refuses, printing every reason and exiting 2, unless ALL of these pass:
  G0 entrypoint NFL-42 single validation entrypoint enforced (pipeline/hooks.py nfl42_entrypoint): the registry routes
                only to the decontam validator, run_validation() is PASS with accepted_policy null, and every
                deny-listed contaminated suite_fix file is rejected by invoke(). Checked again inside the engine call.
  G1 flags      known_flags/KNOWN_LIMITATIONS.json readable and "DEFERRED_100K" is false
  G2 NFL-43     SEMANTICS_BOUNDS.md exists, no semantics are listed unsupported, the bounds review is ACCEPTED for the
                current bounds file (BetGuru / reviewer), AND the engine config this entry point will actually run
                (core/possession_engine_v0/config/*.json, mode data_only, game.game_id == <game>, exactly one) carries a
                ``semantics`` block whose penalties / returns / overtime modes are each the mode documented in the
                reviewed SEMANTICS_BOUNDS.md, with ``ot_rule`` equal to the overtime mode
  G3 packet     pregame/packets/<game>/packet.json exists
  G4 freshness  every source in pipeline/freshness.py is FRESH or NOT_REQUIRED, including the newest four-book
                price freeze (Blitz) and official inactives pulled after T-90
  G5 phases     phases 1-13 and 15 are not MISSING / STALE / NOT_YET
  G7 as-of      the committed as-of play-by-play (data/historical/nflverse/pbp_<season>_w1_<wk-1>_pulled_*.parquet,
                newest pull) exists, covers every history week, contains no week >= the target week and not the target
                game, the config's history weeks are strictly before the target week, and now is before kickoff
                (same checks as snapshots/lock.py asof_checks)
  G6 rocket     BetGuru's `rocket` validation command exits 0 for this game (pipeline/hooks.py ROCKET_COMMAND)
                -- run only after G1-G5 and G7 pass, so a refusal never costs a validation run
There is no override flag, environment variable or "force" switch, by design. The trial count is fixed at 100,000.

Only when every gate passes does it run the NFL-43 possession engine (core/possession_engine_v0/simulate.simulate_games
via snapshots/lock.py run_sim, the same call the snapshot locker makes; model weights unchanged) for exactly 100,000
trials and write pipeline/ledgers/<game>.sim100k.json. The run is a refusal (exit 2, no result) if it completes a
different trial count, any chunk status is not OK, or the engine reports semantics other than the ones G2 checked.
(NFL-56: before this change it ran the older core/period_engine_v0 matchup_pair engine, Ghost6 review d65ad98.) Output stays research only and
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
EXIT_REFUSED = 2
GATE_PHASES = [n for n in PH.PHASES if n != 14]   # 14 is this entry point itself
ENGINE_REL = Path("core") / "possession_engine_v0"
CONFIG_REL = ENGINE_REL / "config"
PBP_REL = Path("data") / "historical" / "nflverse"
SEMANTICS_KEYS = ("penalties", "returns", "overtime")


def engine_config(game_id: str | None, root: Path) -> dict:
    """The one possession-engine config this entry point runs for the game. Read-only. Never picks among several."""
    if not game_id:
        return {"status": "MISSING", "reason": "no game id"}
    hits = []
    for f in sorted((Path(root) / CONFIG_REL).glob("*.json")):
        try:
            c = json.loads(f.read_text())
        except (OSError, ValueError):
            continue
        if (c.get("game") or {}).get("game_id") == game_id and c.get("mode") == "data_only":
            hits.append((f, c))
    if not hits:
        return {"status": "MISSING", "reason": f"no data_only possession-engine config for {game_id} under {CONFIG_REL}"}
    if len(hits) > 1:
        return {"status": "AMBIGUOUS", "reason": f"{len(hits)} data_only configs for {game_id}: "
                + ", ".join(f.name for f, _ in hits) + " (refusing to choose)"}
    f, c = hits[0]
    return {"status": "OK", "path": f, "cfg": c}


def engine_semantics_check(ec: dict, root: Path) -> list[str]:
    """G2 part 2: the semantics the engine will actually run must be the reviewed ones."""
    if ec["status"] != "OK":
        return [ec["reason"]]
    cfg, why = ec["cfg"], []
    sem = cfg.get("semantics")
    if not isinstance(sem, dict):
        return [f"engine config {ec['path'].name} has no semantics block (legacy path: penalties/returns unsupported, "
                "single-possession OT)"]
    try:
        bounds = (Path(root) / hooks.SEMANTICS_BOUNDS_PATH).read_text()
    except OSError:
        bounds = ""
    for k in SEMANTICS_KEYS:
        mode = sem.get(k)
        if not mode:
            why.append(f"engine config {ec['path'].name} semantics.{k} is not set")
        elif f"`{mode}`" not in bounds:
            why.append(f"engine config {ec['path'].name} semantics.{k}={mode!r} is not a mode documented in "
                       f"{hooks.SEMANTICS_BOUNDS_PATH}")
    if cfg.get("ot_rule") != sem.get("overtime"):
        why.append(f"engine config {ec['path'].name} ot_rule {cfg.get('ot_rule')!r} != semantics.overtime {sem.get('overtime')!r}")
    return why


def _utc(s: str) -> datetime:
    return datetime.fromisoformat(str(s).replace("Z", "+00:00")).astimezone(timezone.utc)


def asof_pbp(cfg: dict, root: Path) -> Path | None:
    g = cfg["game"]
    season, wk = int(g.get("season", cfg["history"]["season"])), int(g["week_asof_exclusive"])
    files = sorted((Path(root) / PBP_REL).glob(f"pbp_{season}_w1_{wk - 1}_pulled_*.parquet"), key=lambda f: f.name)
    return files[-1] if files else None


def asof_check(ec: dict, now: datetime, root: Path) -> tuple[list[str], dict]:
    """G7: the as-of inputs the engine reads. Same rules as snapshots/lock.py asof_checks plus week coverage."""
    if ec["status"] != "OK":
        return [f"engine config unavailable ({ec['reason']})"], {}
    cfg = ec["cfg"]
    g, why = cfg["game"], []
    try:
        kickoff = _utc(g["kickoff_et"])
    except (KeyError, ValueError) as e:
        return [f"config kickoff_et unreadable: {e!r}"], {}
    wk = int(g["week_asof_exclusive"])
    weeks = list(cfg["history"]["weeks_inclusive"])
    if now >= kickoff:
        why.append(f"now {now.isoformat(timespec='seconds')} is not before kickoff {kickoff.isoformat()} (no post-kickoff runs)")
    if max(weeks) >= wk:
        why.append("config history weeks are not strictly before the target week")
    pbp = asof_pbp(cfg, root)
    if pbp is None:
        why.append(f"no committed as-of play-by-play {PBP_REL}/pbp_{g.get('season')}_w1_{wk - 1}_pulled_*.parquet")
        return why, {}
    import pandas as pd
    try:
        d = pd.read_parquet(pbp, columns=["game_id", "week", "season"])
    except Exception as e:  # unreadable input is a refusal
        return why + [f"as-of play-by-play {pbp.name} unreadable: {e!r}"], {}
    d = d[d["season"] == int(g.get("season", cfg["history"]["season"]))]
    have = set(int(w) for w in d["week"].unique())
    if (d["game_id"] == g.get("game_id")).any():
        why.append(f"as-of play-by-play contains the target game {g.get('game_id')} (leakage)")
    if any(w >= wk for w in have):
        why.append(f"as-of play-by-play contains week >= {wk} (leakage)")
    miss = sorted(set(weeks) - have)
    if miss:
        why.append(f"as-of play-by-play {pbp.name} is missing history weeks {miss} (stale)")
    return why, {"pbp": pbp, "kickoff_utc": kickoff.isoformat()}


def preflight(pk: dict | None, now: datetime | None = None, flags: dict | None = None, hook_impls=None,
              include_phases: bool = True, rocket_impl=None, rocket_command=None, root: Path | None = None,
              game_id: str | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    root = Path(root or hooks.ROOT)
    flags = hooks.known_flags() if flags is None else flags
    reasons, gates = [], {}
    gid = game_id or ((pk or {}).get("game") or {}).get("game_id")

    # G0 (NFL-42): the validation entrypoint is checked in the real repo code (hooks.ROOT), never a test root, so a
    # fixture root cannot stand in for the enforced registry. No injection parameter (tests monkeypatch hooks).
    try:
        ep = hooks.nfl42_entrypoint()
    except Exception as e:  # fail closed
        ep = {"status": "FAILED", "reason": f"NFL-42 entrypoint check raised {e!r}"}
    if not isinstance(ep, dict):
        ep = {"status": "FAILED", "reason": f"NFL-42 entrypoint check returned {type(ep).__name__}"}
    gates["G0_entrypoint"] = "PASS" if ep.get("status") == "OK" else "REFUSED"
    if ep.get("status") != "OK":
        reasons.append("G0: " + str(ep.get("reason", "NFL-42 entrypoint not enforced")))

    if "_error" in flags:
        gates["G1_flags"] = "REFUSED"; reasons.append(f"G1: {flags['_error']}")
    elif flags.get("DEFERRED_100K") is not False:
        gates["G1_flags"] = "REFUSED"; reasons.append("G1: DEFERRED_100K is set in known_flags/KNOWN_LIMITATIONS.json (100k runs are deferred).")
    else:
        gates["G1_flags"] = "PASS"

    ec = engine_config(gid, root)
    sem = hooks.nfl43_semantics(flags, root=root, cfg=(ec.get("cfg") if ec["status"] == "OK" else None), scan_repo=True)
    sem_why = ([sem["reason"]] if sem["status"] != "OK" else []) + engine_semantics_check(ec, root)
    gates["G2_nfl43"] = "PASS" if not sem_why else "REFUSED"
    reasons += ["G2: " + w for w in sem_why]

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

    asof_why, asof = asof_check(ec, now, root)
    gates["G7_asof"] = "PASS" if not asof_why else "REFUSED"
    reasons += ["G7: " + w for w in asof_why]

    if reasons:
        gates["G6_rocket"] = "NOT_RUN (earlier gates refused)"
    else:
        r = hooks.rocket_validation(gid, impl=rocket_impl, command=rocket_command)
        gates["G6_rocket"] = "PASS" if r.get("status") == "PASS" else "REFUSED"
        if r.get("status") != "PASS":
            reasons.append("G6: " + r.get("reason", "rocket did not pass"))
    out = {"ran": not reasons, "ok": not reasons, "gates": gates, "reasons": reasons, "checked_utc": now.isoformat(timespec="seconds"),
           "entrypoint": {k: ep.get(k) for k in ("status", "entrypoint", "authorized_sha256", "denied") if k in ep}}
    if not reasons:
        freeze = hooks.newest_price_freeze(pk, base=(hook_impls or {}).get("price_freeze_dir"))
        out["engine_inputs"] = {"config_path": ec["path"], "cfg": ec["cfg"], "pbp": asof["pbp"],
                                "kickoff_utc": asof["kickoff_utc"], "price_freeze": freeze}
    return out


def _sha256(p) -> str:
    import hashlib
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def default_engine(pk: dict, trials: int, inputs: dict, workers: int | None = None) -> dict:
    """NFL-43 possession engine, called exactly as snapshots/lock.py does (run_sim -> simulate.simulate_games), only
    from the gated inputs. Formulas and weights unchanged. Any mismatch after the run is a refusal."""
    import os
    root = hooks.ROOT
    ep = hooks.nfl42_entrypoint(root)  # NFL-42: re-checked at the engine call, not only in preflight
    if ep.get("status") != "OK":
        raise RuntimeError(ep.get("reason", "NFL-42 entrypoint not enforced"))
    sys.path.insert(0, str(root))
    sys.path.insert(0, str(root / ENGINE_REL))
    from snapshots import lock as L
    from config_load import load_config
    from simulate import stable_seed
    cfg = load_config(inputs["config_path"])
    g = cfg["game"]
    seed = stable_seed(int(cfg["seed_base"]), int(g["week_asof_exclusive"]), cfg["config_id"])
    sim = L.run_sim(cfg, str(inputs["pbp"]), trials, seed, workers or max(1, (os.cpu_count() or 2) - 1))
    if sim["n"] != trials:
        raise RuntimeError(f"engine completed {sim['n']} trials, not {trials}")
    if sim["statuses"] != ["OK"]:
        raise RuntimeError(f"engine chunk statuses {sim['statuses']}")
    used = sim.get("semantics") or {}
    want = cfg["semantics"]
    got = {"penalties": (used.get("penalties") or {}).get("mode") if isinstance(used.get("penalties"), dict) else used.get("penalties"),
           "returns": (used.get("returns") or {}).get("mode") if isinstance(used.get("returns"), dict) else used.get("returns"),
           "overtime": used.get("overtime")}
    if used.get("status") != "NFL43_SEMANTICS_V1" or any(got[k] != want.get(k) for k in SEMANTICS_KEYS):
        raise RuntimeError(f"engine ran semantics {got} (status {used.get('status')}), not the gated {want}")
    # NFL-75: per-player box lines must exist for every trial and reconcile exactly with the team ledger and the
    # engine's own events; anything else is a refusal (observational layer, game results unaffected).
    from player_box import summarize as _box_summary
    pb = sim.get("player_box") or {}
    rec = pb.get("reconciliation") or {}
    if rec.get("trials") != trials or rec.get("failures") != 0:
        raise RuntimeError(f"per-player box reconciliation failed or missing: {rec or 'no player_box'}")
    freeze = json.loads(Path(inputs["price_freeze"]).read_text()) if inputs.get("price_freeze") else None
    lines = L.market_lines(freeze, g.get("home_name"), g.get("away_name"))
    summary = L.summarize(sim["arrays"], lines, g["home"], g["away"], g.get("home_name"), g.get("away_name"))
    return {"engine": "core/possession_engine_v0 simulate_games + NFL-43 semantics (via snapshots/lock.py run_sim)",
            "config_id": cfg["config_id"], "config_path": str(Path(inputs["config_path"]).relative_to(root))
            if str(inputs["config_path"]).startswith(str(root)) else str(inputs["config_path"]),
            "config_sha256": _sha256(inputs["config_path"]), "semantics_used": got,
            "defense_interaction": cfg.get("defense_interaction"),
            "pbp": Path(inputs["pbp"]).name, "pbp_sha256": _sha256(inputs["pbp"]),
            "price_freeze": Path(inputs["price_freeze"]).name if inputs.get("price_freeze") else None,
            "price_freeze_pulled_utc": ((freeze or {}).get("meta") or {}).get("pulled_utc"),
            "n": sim["n"], "seed": seed, "chunks": sim["chunks"], "chunk_seeds": sim["chunk_seeds"],
            "runtime_sec": sim["runtime_sec"], "model_weights_changed": False,
            "nfl42_entrypoint": {"status": ep["status"], "authorized_sha256": ep.get("authorized_sha256")}, "summary": summary,
            "player_box": {"schema": pb.get("schema"), "reconciliation": rec, "n_columns": len(pb["columns"]),
                           "summary": _box_summary(pb["columns"], pb["values"]),
                           "team_summary": _box_summary([[t, "TEAM", s] for t, s in pb["team_columns"]],
                                                        pb["team_values"]),
                           "attribution": "core/possession_engine_v0/player_box.py docstring", "research_only": True},
            # per-trial lines (n x columns); main() writes them to an .npz with --write, never into the JSON report
            "player_box_trials": {"columns": pb["columns"], "values": pb["values"],
                                  "team_columns": pb["team_columns"], "team_values": pb["team_values"]}}


def run(game_id: str, packet: Path | None = None, engine=default_engine, **kw) -> tuple[int, dict]:
    try:
        pk = PH.load_packet(game_id, packet)
    except (OSError, ValueError):
        pk = None
    pf = preflight(pk, game_id=game_id, **kw)
    inputs = pf.pop("engine_inputs", None)
    report = {"schema": "nfl56-sim100k/2", "game_id": game_id, "trials_requested": TRIALS, "projection_ready": False,
              "research_only": True, **pf}
    if not pf["ok"]:
        report["status"] = "REFUSED"
        return EXIT_REFUSED, report
    try:  # NFL-42 recheck immediately before ANY engine call (default or injected)
        ep = hooks.nfl42_entrypoint()
    except Exception as e:
        ep = {"status": "FAILED", "reason": repr(e)}
    if not isinstance(ep, dict) or ep.get("status") != "OK":
        report.update(status="REFUSED", ran=False, ok=False,
                      reasons=["G0: " + str(ep.get("reason") if isinstance(ep, dict) else ep)])
        return EXIT_REFUSED, report
    try:
        report["result"] = engine(pk, TRIALS, inputs)
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
    ap.add_argument("--rush-dist", action="store_true",
                    help="NFL-75 opt-in: also write <game>.rush_dist.{json,cdf.csv,summary.csv} (per-player rushing-"
                         "yards distribution + P(under L)) from the per-player box lines; needs --write")
    a = ap.parse_args(argv)
    if a.rush_dist and not a.write:
        ap.error("--rush-dist needs --write")
    code, rep = run(a.game, a.packet)
    box_trials = (rep.get("result") or {}).pop("player_box_trials", None) if isinstance(rep.get("result"), dict) else None
    if rep["status"] == "REFUSED":
        print(f"sim100k: REFUSED for {a.game}. Nothing was simulated. Reasons:")
        for r in rep["reasons"]:
            print(f"  - {r}")
    else:
        print(f"sim100k: ran {TRIALS:,} trials for {a.game} (research only; projection_ready stays false).")
    if a.write:
        PH.LEDGERS.mkdir(parents=True, exist_ok=True)
        if box_trials is not None:  # NFL-75: per-trial per-player box lines, same trial order as the summary arrays
            import numpy as np
            np.savez_compressed(PH.LEDGERS / f"{a.game}.sim100k.player_box.npz",
                                columns=np.array(["|".join(c) for c in box_trials["columns"]]),
                                values=box_trials["values"].astype(np.float32),
                                team_columns=np.array(["|".join(c) for c in box_trials["team_columns"]]),
                                team_values=box_trials["team_values"].astype(np.float32))
        (PH.LEDGERS / f"{a.game}.sim100k.json").write_text(json.dumps(rep, indent=1, default=str) + "\n")
        if a.rush_dist and box_trials is not None and rep["status"] != "REFUSED":  # opt-in, observational only
            from . import rush_dist as RD
            res = rep.get("result") or {}
            pbp = res.get("pbp")
            pbp_path = (hooks.ROOT / PBP_REL / pbp) if pbp else None
            d = RD.build_from_box(box_trials["columns"], box_trials["values"], a.game,
                                  pbp_path=pbp_path if pbp_path and pbp_path.exists() else None,
                                  meta={k: res.get(k) for k in ("n", "seed", "config_id", "pbp") if k in res})
            RD.write(d, PH.LEDGERS)
    return code


if __name__ == "__main__":
    sys.exit(main())
