"""Empirical SD, CV, and negative-binomial kappa by market (NFL-64).

Frozen baseline values are the current suave-bets dist.ts defaults named in
NFL-64. They are recorded here and are not changed. Empirical moments are
computed only from sim outputs and saved lines already in this repository.
No model weights are updated. No fitted-calibration claim is made.
"""
from __future__ import annotations

from hashlib import sha256
import json
import math
from pathlib import Path
from typing import Iterable, Sequence

from .push_probability import PUSH_TOLERANCE, _as_floats, push_aware_probs

# Abbreviations used in snapshot summaries, plus the full names that appear on vs_market sides.
_TEAM_ALIASES = {
    "WAS": ("was", "wsh", "washington", "commanders"),
    "NYG": ("nyg", "giants", "new york giants"),
    "NYJ": ("nyj", "jets", "new york jets"),
    "BUF": ("buf", "buffalo", "bills"),
    "DAL": ("dal", "dallas", "cowboys"),
    "IND": ("ind", "indianapolis", "colts"),
    "JAX": ("jax", "jac", "jacksonville", "jaguars"),
    "BAL": ("bal", "baltimore", "ravens"),
}

_REPO = Path(__file__).resolve().parent.parent

# Frozen baseline from NFL-64 / suave-bets src/lib/odds/matchup-proj/dist.ts.
# These are documentation of the current code defaults, not fitted values.
FROZEN_BASELINE = {
    "source": "suave-bets/src/lib/odds/matchup-proj/dist.ts (as named in NFL-64)",
    "lognormal_cv": 0.55,
    "negative_binomial_kappa": {"default": 4.0, "alternate": 2.5},
    "normal_sd_rule": "max(mean * 0.22, 0.6)",
    "normal_cv": 0.22,
    "normal_sd_floor": 0.6,
    "status": "FROZEN_UNCHANGED",
    "weights_changed": False,
}

# Saved 100k score arrays already on main, plus the DAL@IND player-yard sample.
DEFAULT_SCORE_SNAPSHOTS = (
    "snapshots/2026_10_WAS_NYG/20261112T171258Z",
    "snapshots/2026_10_BUF_NYJ/20261112T172055Z",
)
DEFAULT_PLAYER_SUMMARY = (
    "research/nfl_sim_integration_2026-11-06/integration/"
    "prospective_wk10_2026-11-08/runs/sim_dal_ind_summary.json"
)


def frozen_normal_sd(mean: float) -> float:
    mean = float(mean)
    if not math.isfinite(mean):
        raise ValueError("mean must be finite")
    return max(abs(mean) * FROZEN_BASELINE["normal_cv"], FROZEN_BASELINE["normal_sd_floor"])


def moments(values: Iterable[float]) -> dict:
    """Population moments of a saved sim distribution (ddof=0), matching snapshot summaries."""
    sample = _as_floats(values)
    n = len(sample)
    if n == 0:
        raise ValueError("values must be nonempty")
    mean = sum(sample) / n
    var = sum((x - mean) ** 2 for x in sample) / n
    sd = math.sqrt(var)
    if abs(mean) < PUSH_TOLERANCE:
        cv = None
        cv_status = "UNDEFINED_MEAN_NEAR_ZERO"
    else:
        cv = sd / mean
        cv_status = "OK"
    return {
        "n": n,
        "mean": mean,
        "sd": sd,
        "variance": var,
        "cv": cv,
        "cv_status": cv_status,
        "sd_convention": "population_ddof_0",
    }


def nb_kappa_mom(mean: float, variance: float) -> dict:
    """Method-of-moments NB size: Var = mu + mu^2/kappa  =>  kappa = mu^2 / (var - mu)."""
    if not math.isfinite(mean) or not math.isfinite(variance):
        raise ValueError("mean and variance must be finite")
    if mean <= 0:
        return {"kappa": None, "status": "NOT_APPLICABLE_NONPOSITIVE_MEAN",
                "formula": "kappa = mean^2 / (variance - mean)"}
    if variance <= mean + PUSH_TOLERANCE:
        return {"kappa": None, "status": "NOT_OVERDISPERSED_VS_POISSON",
                "formula": "kappa = mean^2 / (variance - mean)"}
    return {
        "kappa": (mean * mean) / (variance - mean),
        "status": "METHOD_OF_MOMENTS",
        "formula": "kappa = mean^2 / (variance - mean)",
    }


def series_dispersion(values: Iterable[float], *, market: str, identity: str,
                      apply_kappa: bool = True) -> dict:
    stats = moments(values)
    report = {
        "market": market,
        "identity": identity,
        **stats,
        "frozen_baseline": FROZEN_BASELINE,
        "weights_changed": False,
        "challenger_status": "RESEARCH_ONLY_NOT_APPLIED",
        "validation_claim": "NONE",
    }
    if apply_kappa:
        report["kappa"] = nb_kappa_mom(stats["mean"], stats["variance"])
    else:
        report["kappa"] = {"kappa": None, "status": "NOT_APPLICABLE_SIGNED_OR_CONTINUOUS_MARKET",
                           "formula": "kappa = mean^2 / (variance - mean)"}
    return report


def _file_meta(path: Path, root: Path) -> dict:
    data = path.read_bytes()
    return {
        "path": path.resolve().relative_to(root.resolve()).as_posix(),
        "hash": sha256(data).hexdigest(),
        "bytes": len(data),
    }


def _load_summary(snapshot_dir: Path) -> dict:
    path = snapshot_dir / "summary.json"
    if not path.is_file():
        raise FileNotFoundError(path)
    return json.loads(path.read_text())


def _load_arrays(snapshot_dir: Path):
    path = snapshot_dir / "sim_arrays.npz"
    if not path.is_file():
        raise FileNotFoundError(path)
    import numpy as np
    return np.load(path, allow_pickle=False)


def resolve_listed_side(side: str, home: str, away: str) -> str:
    """Map a vs_market side string to 'home' or 'away'. Unknown sides stay unresolved."""
    text = " ".join(str(side or "").lower().split())
    if not text:
        return "unresolved"
    home = str(home or "").upper()
    away = str(away or "").upper()

    def matches(abbr: str) -> bool:
        if not abbr:
            return False
        token = abbr.lower()
        if text == token:
            return True
        for alias in _TEAM_ALIASES.get(abbr, (token,)):
            if text == alias or alias in text:
                return True
        return False

    home_hit, away_hit = matches(home), matches(away)
    if home_hit and not away_hit:
        return "home"
    if away_hit and not home_hit:
        return "away"
    return "unresolved"


def score_dispersion_from_snapshot(snapshot_dir: str | Path, *, repo_root: Path | None = None) -> dict:
    root = Path(repo_root or _REPO).resolve()
    directory = (root / snapshot_dir).resolve() if not Path(snapshot_dir).is_absolute() else Path(snapshot_dir)
    summary = _load_summary(directory)
    arrays = _load_arrays(directory)
    home = [float(x) for x in arrays["fg_home"]]
    away = [float(x) for x in arrays["fg_away"]]
    total = [h + a for h, a in zip(home, away)]
    margin = [h - a for h, a in zip(home, away)]
    home_id = summary.get("home") or "home"
    away_id = summary.get("away") or "away"
    markets = [
        series_dispersion(total, market="total", identity="fg_total", apply_kappa=True),
        series_dispersion(home, market="team_points", identity=f"{home_id}_home", apply_kappa=True),
        series_dispersion(away, market="team_points", identity=f"{away_id}_away", apply_kappa=True),
        series_dispersion(margin, market="margin", identity=f"{home_id}_home_margin", apply_kappa=False),
    ]
    lines = []
    for row in summary.get("vs_market") or []:
        if not isinstance(row, dict):
            continue
        market = str(row.get("market") or "")
        line = row.get("line")
        if line is None:
            continue
        if market == "total":
            values = total
        elif market == "spread":
            # Posted line is the listed side's handicap. Home margin is home-away.
            side = str(row.get("side") or "")
            listed = resolve_listed_side(side, home_id, away_id)
            if listed == "unresolved":
                lines.append({
                    "market": market, "book": row.get("book"), "side": side,
                    "line": float(line), "flag": "SIDE_UNRESOLVED",
                    "source_line": "snapshot_summary.vs_market",
                })
                continue
            values = margin if listed == "home" else [-m for m in margin]
            # P(side_margin > -handicap), push at exact -handicap.
            values_line = -float(line)
            probs = push_aware_probs(values, values_line)
            lines.append({
                "market": market,
                "book": row.get("book"),
                "side": side,
                "listed_side": listed,
                "line": float(line),
                "settlement_line_on_side_margin": values_line,
                "sim": {k: probs[k] for k in ("p_over", "p_push", "p_under", "n", "line_kind")},
                "saved_summary": {
                    "p_model_cover": row.get("p_model_cover"),
                    "p_model": row.get("p_model"),
                    "p_model_push": row.get("p_model_push"),
                    "p_book_novig": row.get("p_book_novig"),
                    "reference_only": row.get("reference_only"),
                },
                "source_line": "snapshot_summary.vs_market",
            })
            continue
        else:
            continue
        probs = push_aware_probs(values, float(line))
        lines.append({
            "market": market,
            "book": row.get("book"),
            "side": row.get("side"),
            "line": float(line),
            "sim": {k: probs[k] for k in ("p_over", "p_push", "p_under", "n", "line_kind")},
            "saved_summary": {
                "p_model_cover": row.get("p_model_cover"),
                "p_model": row.get("p_model"),
                "p_model_push": row.get("p_model_push"),
                "p_book_novig": row.get("p_book_novig"),
                "reference_only": row.get("reference_only"),
            },
            "source_line": "snapshot_summary.vs_market",
        })
    return {
        "source": _file_meta(directory / "sim_arrays.npz", root),
        "summary_source": _file_meta(directory / "summary.json", root),
        "n_declared": summary.get("n"),
        "home": home_id,
        "away": away_id,
        "markets": markets,
        "saved_lines": lines,
        "fitted_calibration": False,
        "weights_changed": False,
        "frozen_baseline": FROZEN_BASELINE,
        "validation_claim": "NONE",
        "split_note": "Saved research sim outputs already in the repository; not a live holdout grade.",
    }


def player_dispersion_from_summary(path: str | Path, *, repo_root: Path | None = None) -> dict:
    root = Path(repo_root or _REPO).resolve()
    target = (root / path).resolve() if not Path(path).is_absolute() else Path(path)
    payload = json.loads(target.read_text())
    samples = payload.get("player_samples")
    if not isinstance(samples, list) or not samples or not isinstance(samples[0], dict):
        raise ValueError("player_samples missing or not a list of mappings")
    series: dict[str, list[float]] = {}
    for row in samples:
        if not isinstance(row, dict):
            raise ValueError("player_samples row is not a mapping")
        for key, value in row.items():
            if value is None or value == "":
                continue
            series.setdefault(key, []).append(float(value))
    players = []
    by_market: dict[str, list] = {}
    for key, values in series.items():
        market, _, identity = key.partition("|")
        if not identity:
            market, identity = "unknown", key
        report = series_dispersion(values, market=market, identity=identity,
                                   apply_kappa=market.endswith("_yards") or market.endswith("_attempts"))
        # Yards are non-negative counts in this saved sample, so kappa is reported,
        # but lognormal CV is the frozen baseline named for yard tails.
        report["frozen_lognormal_cv"] = FROZEN_BASELINE["lognormal_cv"]
        players.append(report)
        by_market.setdefault(market, []).append(report)
    market_rollups = []
    for market, rows in sorted(by_market.items()):
        cvs = [row["cv"] for row in rows if row["cv"] is not None]
        kappas = [row["kappa"]["kappa"] for row in rows if row["kappa"].get("kappa") is not None]
        market_rollups.append({
            "market": market,
            "n_series": len(rows),
            "n_trials_each": rows[0]["n"] if rows else 0,
            "cv_unweighted_mean": (sum(cvs) / len(cvs)) if cvs else None,
            "kappa_unweighted_mean": (sum(kappas) / len(kappas)) if kappas else None,
            "note": "Unweighted mean across player series; not a pooled fit and not applied as a weight.",
        })
    return {
        "source": _file_meta(target, root),
        "n_completed": payload.get("n_completed"),
        "quotes": payload.get("quotes"),
        "players": players,
        "by_market": market_rollups,
        "fitted_calibration": False,
        "weights_changed": False,
        "frozen_baseline": FROZEN_BASELINE,
        "validation_claim": "NONE",
        "challenger_status": "RESEARCH_ONLY_NOT_APPLIED",
        "split_note": "DAL@IND prospective sample already in the repository; not a live holdout grade.",
    }


def dispersion_report(*, repo_root: Path | None = None,
                      snapshots: Sequence[str] = DEFAULT_SCORE_SNAPSHOTS,
                      player_summary: str = DEFAULT_PLAYER_SUMMARY) -> dict:
    root = Path(repo_root or _REPO).resolve()
    score = [score_dispersion_from_snapshot(path, repo_root=root) for path in snapshots]
    players = None
    player_path = root / player_summary
    if player_path.is_file():
        players = player_dispersion_from_summary(player_summary, repo_root=root)
    return {
        "fitted_calibration": False,
        "independently_calibrated": False,
        "weights_changed": False,
        "frozen_baseline": FROZEN_BASELINE,
        "validation_claim": "NONE",
        "score_snapshots": score,
        "player_summary": players,
        "note": (
            "Empirical SD/CV/kappa are descriptive moments of saved sim output. "
            "Frozen dist.ts defaults are unchanged. Do not treat challenger "
            "moments as production weights."
        ),
    }
