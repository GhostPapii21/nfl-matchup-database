"""Three game-script branches and independent model records for one game (NFL-90).

Connects existing entrypoints to the game-level packet. It does not replace their
algorithms, average their outputs, or rename one engine as another.

Branches are a partition of each engine's own trials. The cut points are the
margin edges already used in research/qb_script_2026-11-22/study.py (-3, 3, 10).
Realized favorite margin is favorite points minus underdog points:

  favorite_controls   margin >= 10
  underdog_chases     3 <= margin < 10
                      (the underdog is behind, short of the 10-point bin)
  competitive         -3 <= margin < 3
  residual            margin < -3
                      (kept, and not copied into the three branches)

The board's pass/rush multipliers from that study are disclosed at those edges
and are not applied on top of the simulated plays.

    python -m sunday.script_models replay --game 2026_12_DEN_PIT --out <dir>

Research only. projection_ready stays false.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Optional

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
BRANCHES = ("favorite_controls", "underdog_chases", "competitive")
RESIDUAL = "residual"
ENGINE_IDS = (
    "period_engine_v0",
    "possession_engine_v0",
    "pipeline.sim100k",
    "simv56",
    "sim_v6",
    "main",
    "lightning",
)
# Methods an engine is allowed to mark simulated. Anything else is a mislabel.
SIMULATED_METHODS = {
    "period_engine_v0": {"monte_carlo", "game_randomness"},
    "possession_engine_v0": {"simulate_games"},
    "pipeline.sim100k": {"default_engine"},
    "simv56": set(),
    "sim_v6": set(),
    "main": set(),
    "lightning": set(),
}
FORBIDDEN_KEYS = {
    "pooled_mean",
    "branch_average",
    "consensus_probability",
    "blended_branch",
    "branch_weights",
    "method_average",
}
PLAYER_STATS = (
    "targets", "carries", "pass_att", "pass_yds", "rush_yds", "rec_yds", "rec",
    "pass_td", "rush_td", "rec_td",
)
DOCUMENTED_SIM_V6 = "tools/sim_v6.py"
DOCUMENTED_SIM_V6_COMMAND = "python3 tools/sim_v6.py run <legs.json> <out.json>"


def pass_multiplier(margin: float) -> float:
    """Board rule: pass attempts x (1 - 0.01 x margin), margin capped at +/-10."""
    m = max(-10.0, min(10.0, float(margin)))
    return 1.0 - 0.01 * m


def rush_multiplier(margin: float) -> float:
    """Board rule: rush attempts x (1 + 0.012 x margin), margin capped at +/-10."""
    m = max(-10.0, min(10.0, float(margin)))
    return 1.0 + 0.012 * m


def assign_branches(favorite_margin: np.ndarray) -> dict[str, np.ndarray]:
    """Mutually exclusive masks. Every finite trial lands in exactly one bin."""
    m = np.asarray(favorite_margin, dtype=float)
    if m.ndim != 1:
        raise ValueError("favorite margin must be one-dimensional")
    if np.isnan(m).any():
        raise ValueError("favorite margin has NaN; refusing to drop trials into another branch")
    masks = {
        "favorite_controls": m >= 10,
        "underdog_chases": (m >= 3) & (m < 10),
        "competitive": (m >= -3) & (m < 3),
        RESIDUAL: m < -3,
    }
    covered = np.zeros(len(m), dtype=int)
    for mask in masks.values():
        covered += mask.astype(int)
    if not np.all(covered == 1):
        raise RuntimeError("branch masks are not a partition of the trials")
    return masks


def favorite_from_home_spread(home: str, away: str, home_spread: float) -> tuple[str, str, bool]:
    """Packet home_spread is negative when the home team is the favorite (pregame.packet)."""
    if home_spread is None:
        raise ValueError("no home spread; a favorite cannot be named")
    spread = float(home_spread)
    if spread < 0:
        return home, away, True
    if spread > 0:
        return away, home, False
    raise ValueError("pick'em spread; a favorite cannot be named")


def favorite_margin(fg_home, fg_away, favorite_is_home: bool) -> np.ndarray:
    home = np.asarray(fg_home, dtype=float)
    away = np.asarray(fg_away, dtype=float)
    if home.shape != away.shape:
        raise ValueError("home and away score arrays differ in shape")
    return (home - away) if favorite_is_home else (away - home)


def _dist(values) -> Optional[dict]:
    x = np.asarray(values, dtype=float)
    x = x[np.isfinite(x)]
    if len(x) == 0:
        return None
    return {
        "n": int(len(x)),
        "mean": float(x.mean()),
        "p10": float(np.percentile(x, 10)),
        "p50": float(np.percentile(x, 50)),
        "p90": float(np.percentile(x, 90)),
    }


def _reject_pooling_keys(obj, path="") -> None:
    if isinstance(obj, dict):
        bad = FORBIDDEN_KEYS.intersection(obj)
        if bad:
            raise ValueError(f"refusing pooling key(s) {sorted(bad)} at {path or '<root>'}")
        for k, v in obj.items():
            _reject_pooling_keys(v, f"{path}.{k}" if path else str(k))
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            _reject_pooling_keys(v, f"{path}[{i}]")


def _json_default(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        raise TypeError("refusing to write a raw array; summarize it first")
    raise TypeError(f"not JSON serializable: {type(o).__name__}")


class ArtifactStore:
    """Write each relative path once. A second write is an overwrite, not a merge."""

    def __init__(self, root: Path):
        self.root = Path(root)
        if self.root.exists() and any(self.root.iterdir()):
            raise FileExistsError(f"refusing to write into non-empty {self.root}")
        self.root.mkdir(parents=True, exist_ok=True)
        self.written: set[str] = set()

    def write(self, rel: str, obj: dict) -> str:
        _reject_pooling_keys(obj)
        if rel in self.written:
            raise FileExistsError(f"refusing to overwrite {rel}")
        path = self.root / rel
        if path.exists():
            raise FileExistsError(f"refusing to overwrite {rel}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(obj, indent=1, allow_nan=False, default=_json_default) + "\n")
        self.written.add(rel)
        return rel


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _code_revision(root: Path) -> Optional[str]:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def _indices(mask: np.ndarray) -> list[int]:
    return [int(i) for i in np.flatnonzero(mask)]


def _score_block(arrays: dict, mask: np.ndarray, favorite_is_home: bool) -> dict:
    if int(mask.sum()) == 0:
        return {"n_trials": 0, "final": None, "quarters": {q: None for q in ("q1", "q2", "q3", "q4")}}
    home = np.asarray(arrays["fg_home"])[mask]
    away = np.asarray(arrays["fg_away"])[mask]
    quarters = {}
    for q in ("q1", "q2", "q3", "q4"):
        hk, ak = f"{q}_home", f"{q}_away"
        if hk not in arrays or ak not in arrays:
            quarters[q] = {"supported": False}
        else:
            quarters[q] = {
                "supported": True,
                "home": _dist(np.asarray(arrays[hk])[mask]),
                "away": _dist(np.asarray(arrays[ak])[mask]),
            }
    return {
        "n_trials": int(mask.sum()),
        "final": {
            "home": _dist(home),
            "away": _dist(away),
            "favorite_margin": _dist(favorite_margin(home, away, favorite_is_home)),
        },
        "quarters": quarters,
    }


def _trial_sum(columns, values, team: str, stat: str) -> np.ndarray:
    cols = [tuple(c) for c in columns]
    acc = np.zeros(values.shape[0], dtype=float)
    found = False
    for j, (t, _player, s) in enumerate(cols):
        if t == team and s == stat:
            acc += values[:, j]
            found = True
    if not found:
        return np.full(values.shape[0], np.nan)
    return acc


def _team_opportunity(box: dict, mask: np.ndarray, teams: tuple[str, str]) -> dict:
    if not box or int(mask.sum()) == 0:
        return {t: None for t in teams}
    values = np.asarray(box["values"], dtype=float)[mask]
    team_values = np.asarray(box["team_values"], dtype=float)[mask]
    team_columns = [tuple(c) for c in box["team_columns"]]
    out = {}
    for team in teams:
        plays = None
        for j, (t, stat) in enumerate(team_columns):
            if t == team and stat == "plays":
                plays = _dist(team_values[:, j])
        pa = _trial_sum(box["columns"], values, team, "pass_att")
        ca = _trial_sum(box["columns"], values, team, "carries")
        denom = pa + ca
        rate = np.full(len(pa), np.nan)
        ok = np.isfinite(denom) & (denom > 0) & np.isfinite(pa)
        rate[ok] = pa[ok] / denom[ok]
        out[team] = {
            "plays": plays,
            "pass_att": _dist(pa),
            "carries": _dist(ca),
            "pass_share_of_pass_and_carry": _dist(rate),
            "source": "possession player box summed inside this branch's trials",
            "board_rule_applied": False,
        }
    return out


def _players(box: dict, mask: np.ndarray) -> list[dict]:
    if not box or int(mask.sum()) == 0:
        return []
    values = np.asarray(box["values"], dtype=float)[mask]
    grouped: dict[tuple[str, str], dict] = {}
    for j, (team, player, stat) in enumerate(tuple(c) for c in box["columns"]):
        if stat not in PLAYER_STATS:
            continue
        dist = _dist(values[:, j])
        if dist is not None:
            grouped.setdefault((team, player), {})[stat] = dist
    rows = []
    volume = ("targets", "carries", "pass_att", "pass_yds", "rush_yds", "rec_yds", "rec")
    for (team, player), stats in sorted(grouped.items()):
        active = [stats[k] for k in volume if k in stats and (stats[k]["mean"] != 0 or stats[k]["p90"] != 0)]
        if not active:
            continue
        rows.append({
            "team": team,
            "player": player,
            "targets": stats.get("targets"),
            "carries": stats.get("carries"),
            "yards": {k: stats[k] for k in ("pass_yds", "rush_yds", "rec_yds", "rec") if k in stats},
            "td_opportunity": {k: stats[k] for k in ("pass_td", "rush_td", "rec_td") if k in stats},
            "pass_att": stats.get("pass_att"),
        })
    return rows


def _board_rule(branch: str) -> dict:
    edges = {
        "favorite_controls": (10.0,),
        "underdog_chases": (3.0, 10.0),
        "competitive": (-3.0, 0.0),
    }[branch]

    def side(margin: float) -> dict:
        return {
            "margin": margin,
            "pass_attempts_multiplier": pass_multiplier(margin),
            "rush_attempts_multiplier": rush_multiplier(margin),
        }

    return {
        "source": "research/qb_script_2026-11-22/study.py current_rule",
        "applied_to_simulated_plays": False,
        "favorite": [side(m) for m in edges],
        "underdog": [side(-m) for m in edges],
        "note": (
            "The existing board rule evaluated at this branch's margin edges. "
            "10 is the study cap and belongs to favorite_controls; it is not a trial in underdog_chases. "
            "Simulated plays are the engine's own trials."
        ),
    }


def _branch_definition(branch: str) -> str:
    return {
        "favorite_controls": "Realized favorite margin >= 10 (study big-favorite edge).",
        "underdog_chases": (
            "Realized favorite margin in [3, 10). The underdog is behind, and the lead is short of "
            "the 10-point favorite-controls bin. Trials where the underdog is ahead stay in residual."
        ),
        "competitive": "Realized favorite margin in [-3, 3), the study close bin.",
        RESIDUAL: "Realized favorite margin < -3. Stored so those trials are not folded into a named branch.",
    }[branch]


def branch_artifact(
    *,
    engine_id: str,
    method: str,
    sampling: Optional[str],
    branch: str,
    arrays: dict,
    mask: np.ndarray,
    favorite_is_home: bool,
    teams: tuple[str, str],
    player_box: Optional[dict],
    supports_plays: bool,
    seed: int,
    n_parent: int,
) -> dict:
    idx = _indices(mask)
    art = {
        "schema": "sunday-script-branch/1",
        "engine_id": engine_id,
        "method": method,
        "sampling": sampling,
        "branch": branch,
        "definition": _branch_definition(branch),
        "algorithm": "partition of this engine's own trials",
        "replacement_algorithm": False,
        "pooled_with_other_branches": False,
        "projection_ready": False,
        "research_only": True,
        "seed": seed,
        "n_parent_trials": n_parent,
        "n_trials": len(idx),
        "trial_indices": idx,
        "score": _score_block(arrays, mask, favorite_is_home),
        "board_rule_disclosure": None if branch == RESIDUAL else _board_rule(branch),
    }
    if supports_plays and player_box is not None:
        art["pace_and_plays"] = _team_opportunity(player_box, mask, teams)
        art["players"] = _players(player_box, mask)
        art["plays_supported"] = True
        art["player_opportunity_supported"] = True
    else:
        art["pace_and_plays"] = None
        art["players"] = None
        art["plays_supported"] = False
        art["player_opportunity_supported"] = False
        art["unsupported_reason"] = (
            "This engine's trials have score and quarter outcomes only. "
            "Play counts and player opportunity are not copied from another engine."
        )
    return art


def validate_model_record(rec: dict, seen: set) -> None:
    eid = rec.get("engine_id")
    if eid not in SIMULATED_METHODS:
        raise ValueError(f"unknown engine_id {eid}")
    method = rec.get("method")
    key = (eid, method, rec.get("sampling"))
    if key in seen:
        raise ValueError(f"refusing to overwrite model record {key}")
    if eid == "sim_v6":
        if rec.get("simulated") or rec.get("three_method_sim_v6_ran"):
            raise ValueError("documented sim_v6 did not run; refusing a three-method claim")
        if method not in (None, "absent"):
            raise ValueError(f"refusing to label method {method!r} as sim_v6")
    if rec.get("simulated") and method not in SIMULATED_METHODS[eid]:
        raise ValueError(f"method {method!r} is not a simulated method of {eid}")
    if rec.get("projection_ready") is True:
        raise ValueError("model record cannot set projection_ready")
    seen.add(key)


def _file_version(path: Path) -> dict:
    return {"path": str(path.relative_to(ROOT)) if path.is_absolute() and str(path).startswith(str(ROOT)) else str(path),
            "sha256": _sha256(path) if path.is_file() else None, "exists": path.is_file()}


def _period_calls(period_simulate, asof, home, away, n, seed):
    """Same two calls as monte_carlo.raw_probs_mc_and_gr, plus the independent sampler team_projection already keeps."""
    calls = []
    for sampling in ("matchup_pair", "independent"):
        sim = period_simulate(asof, home, away, n=n, seed=seed, apply_gr=False, sampling=sampling)
        calls.append(("monte_carlo", sampling, seed, False, sim))
    gr = period_simulate(asof, home, away, n=n, seed=seed + 1, apply_gr=True, sampling="matchup_pair",
                         gr_scale="within_game_covariance")
    calls.append(("game_randomness", "matchup_pair", seed + 1, True, gr))
    return calls


def _default_period_simulate():
    sys.path.insert(0, str(ROOT / "core" / "period_engine_v0"))
    from monte_carlo import simulate_game
    return simulate_game


def _load_period_history(pbp: Path, season: int, week: int, root: Path = ROOT):
    sys.path.insert(0, str(root / "core" / "period_engine_v0"))
    import pandas as pd
    from reconstruct import as_of_mask, load_pbp, period_table_from_pbp, resolve_pbp_path
    parts = [period_table_from_pbp(load_pbp(pbp))]
    prior_path = resolve_pbp_path(root / "core" / "period_engine_v0" / "data" / f"play_by_play_{season - 1}.parquet")
    prior = Path(prior_path).is_file()
    if prior:
        parts.append(period_table_from_pbp(load_pbp(prior_path)))
    hist = pd.concat(parts, ignore_index=True)
    asof = hist[as_of_mask(hist, season, week)].copy()
    same = asof[asof.season == season]
    if len(same) and int(same.week.max()) >= week:
        raise ValueError("period history includes the target week")
    return asof, prior


def _assert_pbp_excludes_game(pbp: Path, game_id: str, week: int) -> dict:
    import pandas as pd
    d = pd.read_parquet(pbp, columns=["game_id", "week"])
    if (d.game_id == game_id).any():
        raise ValueError(f"{pbp.name} contains the target game {game_id}")
    later = sorted({int(w) for w in d.week.unique() if int(w) >= week})
    if later:
        raise ValueError(f"{pbp.name} contains week >= {week}: {later}")
    return {"pbp": pbp.name, "max_week": int(d.week.max()), "target_week_excluded": True, "target_game_excluded": True}


def _possession_default(cfg, pbp, n, seed):
    eng = ROOT / "core" / "possession_engine_v0"
    sys.path.insert(0, str(eng))
    from simulate import simulate_games
    if int(n) > 20_000:
        raise ValueError("possession research runs are capped at 20000")
    return simulate_games(cfg, pbp_path=str(pbp), n=int(n), seed=int(seed), record_players=True)


def _sim100k_default(game_id: str, packet_path: Optional[Path]):
    from pipeline.sim100k import run
    return run(game_id, packet_path)


def _sim_v6_record() -> dict:
    entry = ROOT / DOCUMENTED_SIM_V6
    calib = list(ROOT.glob("**/sim_v6_calib.json"))
    scratch = ROOT / "calibration" / "simv56" / "engines" / "cc_sim_v6.py"
    from tools.sim_v6 import acceptance_receipt
    receipt = acceptance_receipt() if entry.is_file() else None
    refused = bool(receipt and receipt["status"] == "REFUSED")
    return {
        "engine_id": "sim_v6",
        "method": "absent",
        "sampling": None,
        "entrypoint": DOCUMENTED_SIM_V6,
        "documented_command": DOCUMENTED_SIM_V6_COMMAND,
        "version": _file_version(entry),
        "called": False,
        "simulated": False,
        "three_method_sim_v6_ran": False,
        "trials": 0 if refused else None,
        "trials_required": None if receipt is None else receipt["trials_required"],
        "seed": None,
        "calibration_status": "UNVALIDATED",
        "bias_calibration_status": "MISSING" if refused else "UNVALIDATED_NO_ENTRYPOINT",
        "calibration_artifact": [str(p.relative_to(ROOT)) for p in calib],
        "status": "REFUSED" if refused else ("BLOCKED_ENTRYPOINT_ABSENT" if not entry.is_file() else "PRESENT"),
        "blocker": None if receipt is None else receipt["reason"],
        "acceptance_receipt": receipt,
        "not_used_as_substitute": [
            "calibration/simv56/engines/cc_sim_v6.py",
            "calibration/simv56/engines/cc_sim_v6_fix.py",
            "calibration/simv56_pmodel.py",
            "pipeline/sim100k.py",
            "core/period_engine_v0/monte_carlo.py",
            "core/possession_engine_v0/simulate.py",
        ],
        "scratch_file_present_not_the_entrypoint": scratch.is_file(),
        "inputs": {"legs": None},
        "artifact": None,
        "projection_ready": False,
        "limitations": [
            "No three-method sim_v6 claim.",
            "cc_sim_v6.py is a vendored scratch file used by the simv56 ensemble, not tools/sim_v6.py.",
        ],
    }


def _simv56_record() -> dict:
    entry = ROOT / "calibration" / "simv56_pmodel.py"
    sys.path.insert(0, str(ROOT))
    from calibration.simv56_pmodel import ENGINES, N_TRIALS, verify_engines
    try:
        sums = verify_engines()
        verify_status = "PASS"
        verify_error = None
    except Exception as exc:
        sums = None
        verify_status = "FAILED"
        verify_error = f"{type(exc).__name__}: {exc}"
    return {
        "engine_id": "simv56",
        "method": "verify_engines",
        "sampling": None,
        "entrypoint": "calibration/simv56_pmodel.py",
        "command": "python -m calibration.simv56_pmodel run --legs <legs.csv> --week <W> --sources <dir> --out <dir>",
        "version": _file_version(entry),
        "called": True,
        "simulated": False,
        "trials": None,
        "trials_if_run_all_invoked": N_TRIALS,
        "seed": None,
        "calibration_status": "NOT_EVALUATED_THIS_RUN",
        "status": "ENTRYPOINT_PRESENT_NOT_INVOKED",
        "verify_engines": verify_status,
        "verify_error": verify_error,
        "engine_file_sha256": sums,
        "engines_inside_ensemble": list(ENGINES),
        "distinct_from_sim_v6": True,
        "reason": (
            "verify_engines ran. run_all did not: this replay has no rush-yards legs file. "
            "The ensemble is sim_v5, cc_sim_v6 and cc_sim_v6_fix at 20000 trials. It is not tools/sim_v6.py."
        ),
        "inputs": {"legs": None},
        "artifact": None,
        "projection_ready": False,
        "limitations": ["No prop legs were invented in order to force a simv56 run."],
    }


def _external_model_record(engine_id: str, where: str) -> dict:
    return {
        "engine_id": engine_id,
        "method": "absent",
        "sampling": None,
        "entrypoint": None,
        "version": None,
        "called": False,
        "simulated": False,
        "trials": None,
        "seed": None,
        "calibration_status": "NOT_IN_THIS_REPOSITORY",
        "status": "NOT_CALLABLE_IN_THIS_REPOSITORY",
        "reason": where,
        "inputs": None,
        "artifact": None,
        "projection_ready": False,
        "limitations": ["Not substituted by the possession engine, the period engine, simv56, or sim100k."],
    }


def _scoring_conservation(player_box: Optional[dict]) -> dict:
    """The possession box already reconciles offensive TDs to the engine's touchdown events.

    A missing box is unavailable. It is not filled with a points-versus-touchdown estimate.
    """
    recon = (player_box or {}).get("reconciliation") if isinstance(player_box, dict) else None
    if not isinstance(recon, dict):
        return {
            "status": "UNAVAILABLE",
            "evidence_tier": "unavailable",
            "reason": "The possession result did not include the player-box touchdown reconciliation.",
        }
    failures = int(recon.get("failures") or 0)
    return {
        "status": "MEASURED" if failures == 0 else "FAILED",
        "evidence_tier": "measured",
        "trials": recon.get("trials"),
        "failures": failures,
        "checks": recon.get("checks"),
        "first_failures": recon.get("first_failures"),
        "definition": (
            "rush_td + rec_td + other_td equals the engine touchdown events for that team, "
            "and player stat sums equal the team ledger. Passing and rushing touchdowns are not pooled."
        ),
    }


def _write_branches(store, *, engine_id, method, sampling, arrays, favorite_is_home, teams, player_box,
                    supports_plays, seed) -> list[str]:
    margin = favorite_margin(arrays["fg_home"], arrays["fg_away"], favorite_is_home)
    masks = assign_branches(margin)
    paths = []
    n_parent = int(len(margin))
    for branch in (*BRANCHES, RESIDUAL):
        art = branch_artifact(
            engine_id=engine_id, method=method, sampling=sampling, branch=branch, arrays=arrays,
            mask=masks[branch], favorite_is_home=favorite_is_home, teams=teams, player_box=player_box,
            supports_plays=supports_plays, seed=seed, n_parent=n_parent,
        )
        rel = f"branches/{engine_id}/{method}/{sampling or 'none'}/{branch}.json"
        paths.append(store.write(rel, art))
    return paths


def run_historical_replay(
    packet: dict,
    out_dir: Path,
    *,
    root: Path = ROOT,
    possession_n: int = 24,
    period_n: int = 2000,
    packet_path: Optional[Path] = None,
    period_simulate: Optional[Callable] = None,
    possession_simulate: Optional[Callable] = None,
    sim100k_run: Optional[Callable] = None,
    include_external_identity: bool = True,
) -> dict:
    """Write separate branch artifacts and one record per engine. Returns the manifest."""
    game = packet["game"]
    game_id, home, away = game["game_id"], game["home"], game["away"]
    season, week = int(game["season"]), int(game["week"])
    home_spread = (packet.get("market") or {}).get("home_spread")
    favorite, underdog, favorite_is_home = favorite_from_home_spread(home, away, home_spread)
    store = ArtifactStore(Path(out_dir))
    seen: set = set()
    models = []

    def add_model(rec: dict) -> dict:
        rec.setdefault("projection_ready", False)
        validate_model_record(rec, seen)
        rel = f"models/{rec['engine_id']}"
        if rec.get("method") not in (None, "absent"):
            rel += f"__{rec['method']}"
        if rec.get("sampling"):
            rel += f"__{rec['sampling']}"
        rel += ".json"
        rec["artifact"] = rel
        store.write(rel, rec)
        label = rec["engine_id"]
        if rec.get("method") not in (None, "absent"):
            label += ":" + rec["method"]
        if rec.get("sampling"):
            label += ":" + rec["sampling"]
        models.append(label)
        return rec

    # --- period engine ---
    sys.path.insert(0, str(root / "core" / "period_engine_v0"))
    from monte_carlo import STATUS, stable_seed as period_seed
    pbp = _select_pbp(root, season, week)
    leakage = _assert_pbp_excludes_game(pbp, game_id, week)
    asof, prior = _load_period_history(pbp, season, week, root)
    seed = period_seed(20261105, week, game_id)
    simulate = period_simulate or _default_period_simulate()
    period_inputs = {
        "pbp": leakage,
        "includes_prior_season": prior,
        "history_games": int(len(asof)),
        "home": home,
        "away": away,
        "favorite": favorite,
        "underdog": underdog,
        "home_spread": home_spread,
        "spread_source": "packet.market.home_spread",
    }
    period_version = _file_version(root / "core" / "period_engine_v0" / "monte_carlo.py")
    for method, sampling, call_seed, apply_gr, sim in _period_calls(simulate, asof, home, away, period_n, seed):
        if sim.get("error"):
            add_model({
                "engine_id": "period_engine_v0", "method": method, "sampling": sampling,
                "entrypoint": "core/period_engine_v0/monte_carlo.py:simulate_game",
                "version": period_version, "called": True, "simulated": False, "trials": 0,
                "seed": call_seed, "apply_gr": apply_gr, "calibration_status": STATUS.bias,
                "status": sim.get("error"), "inputs": period_inputs, "projection_ready": False,
                "limitations": ["Period-engine call returned an error. No other engine filled this record."],
            })
            continue
        paths = _write_branches(
            store, engine_id="period_engine_v0", method=method, sampling=sampling, arrays=sim["arrays"],
            favorite_is_home=favorite_is_home, teams=(home, away), player_box=None, supports_plays=False,
            seed=call_seed,
        )
        add_model({
            "engine_id": "period_engine_v0",
            "method": method,
            "sampling": sampling,
            "entrypoint": "core/period_engine_v0/monte_carlo.py:simulate_game",
            "version": period_version,
            "called": True,
            "simulated": True,
            "trials": int(sim.get("n", period_n)),
            "seed": call_seed,
            "apply_gr": apply_gr,
            "calibration_status": sim.get("status", {}).get("bias", STATUS.bias),
            "game_randomness_status": sim.get("status", {}).get("game_randomness"),
            "status": "RAN_RESEARCH_ONLY",
            "inputs": period_inputs,
            "branch_artifacts": paths,
            "projection_ready": False,
            "not_sim_v6": True,
            "limitations": [
                "Bias on this engine is UNIMPLEMENTED_NO_FITTED_CALIB.",
                "Quarter bootstrap only. Plays and player opportunity are unsupported here.",
                "matchup_pair and independent stay in separate records.",
            ],
        })
    add_model({
        "engine_id": "period_engine_v0",
        "method": "bias",
        "sampling": None,
        "entrypoint": "core/period_engine_v0/monte_carlo.py:ModelStatus.bias",
        "version": period_version,
        "called": True,
        "simulated": False,
        "trials": None,
        "seed": None,
        "calibration_status": STATUS.bias,
        "status": STATUS.bias,
        "inputs": period_inputs,
        "projection_ready": False,
        "not_sim_v6": True,
        "limitations": ["Period-engine Bias was not given a fitted calibration by its own module."],
    })

    # --- possession engine (research n, not the 100k gate) ---
    from pipeline.sim100k import engine_config
    ec = engine_config(game_id, root)
    poss_version = _file_version(root / "core" / "possession_engine_v0" / "simulate.py")
    if ec["status"] != "OK":
        add_model({
            "engine_id": "possession_engine_v0", "method": "simulate_games", "sampling": None,
            "entrypoint": "core/possession_engine_v0/simulate.py:simulate_games",
            "version": poss_version, "called": False, "simulated": False, "trials": None, "seed": None,
            "calibration_status": "NOT_A_CALIBRATED_MODEL", "status": ec["status"],
            "reason": ec.get("reason"), "inputs": {"game_id": game_id}, "projection_ready": False,
            "limitations": ["No data_only possession config. sim100k was not used in its place."],
        })
    else:
        sys.path.insert(0, str(root / "core" / "possession_engine_v0"))
        from config_load import load_config
        from simulate import stable_seed as poss_seed
        cfg = load_config(ec["path"])
        poss_seed_v = poss_seed(int(cfg["seed_base"]), int(cfg["game"]["week_asof_exclusive"]), cfg["config_id"])
        runner = possession_simulate or _possession_default
        result = runner(cfg, pbp, possession_n, poss_seed_v)
        poss_inputs = {
            "config": str(ec["path"].relative_to(root)) if str(ec["path"]).startswith(str(root)) else str(ec["path"]),
            "config_sha256": _sha256(ec["path"]),
            "mode": cfg.get("mode"),
            "pbp": leakage,
            "research_n_cap": 20_000,
            "not_the_sim100k_gate": True,
        }
        if result.get("arrays") is None or "fg_home" not in result.get("arrays", {}):
            add_model({
                "engine_id": "possession_engine_v0", "method": "simulate_games", "sampling": None,
                "entrypoint": "core/possession_engine_v0/simulate.py:simulate_games",
                "version": poss_version, "called": True, "simulated": False, "trials": result.get("n_completed"),
                "seed": poss_seed_v, "calibration_status": "NOT_A_CALIBRATED_MODEL",
                "status": result.get("status"), "inputs": poss_inputs, "projection_ready": False,
                "limitations": result.get("limitations") or ["Possession call did not return score arrays."],
            })
        else:
            paths = _write_branches(
                store, engine_id="possession_engine_v0", method="simulate_games", sampling="data_only",
                arrays=result["arrays"], favorite_is_home=favorite_is_home, teams=(home, away),
                player_box=result.get("player_box"), supports_plays=result.get("player_box") is not None,
                seed=poss_seed_v,
            )
            add_model({
                "engine_id": "possession_engine_v0",
                "method": "simulate_games",
                "sampling": "data_only",
                "entrypoint": "core/possession_engine_v0/simulate.py:simulate_games",
                "version": poss_version,
                "called": True,
                "simulated": True,
                "trials": int(result.get("n_completed", possession_n)),
                "seed": poss_seed_v,
                "calibration_status": "NOT_A_CALIBRATED_MODEL",
                "status": result.get("status"),
                "pooling_silently_applied": result.get("pooling_silently_applied"),
                "inputs": poss_inputs,
                "branch_artifacts": paths,
                "projection_ready": False,
                "not_sim_v6": True,
                "not_pipeline_sim100k": True,
                "scoring_conservation": _scoring_conservation(result.get("player_box")),
                "limitations": list(result.get("limitations") or []) + [
                    "Research trial count only. The 100k gate is a separate record.",
                ],
            })

    # --- pipeline.sim100k, its own name, usually a refusal on a historical replay ---
    try:
        code, report = (sim100k_run or _sim100k_default)(game_id, packet_path)
        sim_status = report.get("status")
        reasons = list(report.get("reasons") or [])
    except Exception as exc:
        code, sim_status, reasons = None, "CALL_FAILED", [f"{type(exc).__name__}: {exc}"]
        report = {}
    ran = sim_status == "RAN_RESEARCH_ONLY"
    add_model({
        "engine_id": "pipeline.sim100k",
        "method": "default_engine" if ran else "preflight",
        "sampling": None,
        "entrypoint": "pipeline/sim100k.py:run",
        "command": f"python -m pipeline.sim100k --game {game_id}",
        "version": _file_version(root / "pipeline" / "sim100k.py"),
        "called": True,
        "simulated": ran,
        "trials": 100_000 if ran else None,
        "trials_requested": 100_000,
        "seed": None,
        "exit_code": code,
        "calibration_status": "NOT_RUN" if sim_status != "RAN_RESEARCH_ONLY" else "SEE_ENGINE_RESULT",
        "status": sim_status,
        "gates": report.get("gates"),
        "reasons": reasons,
        "inputs": {"game_id": game_id, "packet": str(packet_path) if packet_path else None},
        "projection_ready": False,
        "not_possession_engine_research_call": True,
        "not_sim_v6": True,
        "limitations": [
            "This record is the fail-closed 100k entrypoint. A research possession run is not copied here.",
            "A historical replay is after kickoff, so the as-of gate refuses. That refusal is the result.",
        ],
    })

    if include_external_identity:
        add_model(_simv56_record())
        add_model(_sim_v6_record())
        add_model(_external_model_record(
            "main",
            "The production Main network is not in this repository. "
            "pregame.packet.player_baselines is a separate research baseline and was not labeled Main. "
            "See data/historical/research/nfl56_status_2026-11-09/lightning/LIGHTNING_REPORT.md.",
        ))
        add_model(_external_model_record(
            "lightning",
            "Lightning is not in this repository. It lives on sportsbook-odds-bridge "
            "experiments/nfl_opportunity_lightning.py. No Lightning weights were run. "
            "See data/historical/research/nfl56_status_2026-11-09/lightning/LIGHTNING_REPORT.md.",
        ))

    manifest = {
        "schema": "sunday-script-models/1",
        "issue": "NFL-90",
        "game_id": game_id,
        "favorite": favorite,
        "underdog": underdog,
        "home_spread": home_spread,
        "branches": list(BRANCHES),
        "residual_retained": True,
        "branches_pooled": False,
        "methods_pooled": False,
        "sim_v6_three_method_claimed": False,
        "projection_ready": False,
        "research_only": True,
        "code_revision": _code_revision(root),
        "connector": _file_version(Path(__file__)),
        "models": models,
        "component": "sunday.script_models.attach_to_packet",
    }
    store.write("manifest.json", manifest)
    return manifest


def _select_pbp(root: Path, season: int, week: int) -> Path:
    """The as-of file sim100k would require: pbp_<season>_w1_<week-1>_pulled_*.parquet, newest name."""
    files = sorted((root / "data" / "historical" / "nflverse").glob(f"pbp_{season}_w1_{week - 1}_pulled_*.parquet"))
    if not files:
        raise FileNotFoundError(f"no as-of pbp for season {season} week {week}")
    return files[-1]


def attach_to_packet(
    packet: dict,
    *,
    root: Path = ROOT,
    out_dir: Path,
    possession_n: int = 24,
    period_n: int = 2000,
    packet_path: Optional[Path] = None,
    **replay_kw,
) -> dict:
    """Game-level hook. Adds script_models and does not replace team_projection or any other block."""
    if packet.get("projection_ready") is True:
        raise ValueError("refusing to attach script models when projection_ready is true")
    manifest = run_historical_replay(
        packet, out_dir, root=root, possession_n=possession_n, period_n=period_n,
        packet_path=packet_path, **replay_kw,
    )
    packet["projection_ready"] = False
    packet["script_models"] = {
        "component": "sunday.script_models",
        "issue": "NFL-90",
        "manifest": str(Path(out_dir) / "manifest.json"),
        "branches": manifest["branches"],
        "models": manifest["models"],
        "branches_pooled": False,
        "sim_v6_three_method_claimed": False,
        "projection_ready": False,
    }
    return packet


def _load_packet(path: Path) -> dict:
    return json.loads(Path(path).read_text())


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="NFL-90 replay: three script branches and independent model records")
    sub = ap.add_subparsers(dest="cmd", required=True)
    rp = sub.add_parser("replay", help="historical game replay")
    rp.add_argument("--game", required=True)
    rp.add_argument("--packet", type=Path, help="defaults to pregame/packets/<game>/packet.json")
    rp.add_argument("--out", type=Path, required=True)
    rp.add_argument("--possession-n", type=int, default=24)
    rp.add_argument("--period-n", type=int, default=2000)
    a = ap.parse_args(argv)
    packet_path = a.packet or (ROOT / "pregame" / "packets" / a.game / "packet.json")
    packet = _load_packet(packet_path)
    if packet["game"]["game_id"] != a.game:
        raise SystemExit(f"packet game_id {packet['game']['game_id']} != {a.game}")
    manifest = run_historical_replay(
        packet, a.out, packet_path=packet_path, possession_n=a.possession_n, period_n=a.period_n,
    )
    print(json.dumps({"out": str(a.out), "models": manifest["models"], "sim_v6_three_method_claimed": False,
                      "projection_ready": False}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
