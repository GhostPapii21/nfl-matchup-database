"""Reconstruct actual period scores from PBP; grade vs as-of sim predictions."""
from __future__ import annotations
from pathlib import Path
from typing import Any
import sys
import numpy as np
import pandas as pd

# reuse period_engine reconstruct (sibling module)
_PEER = Path(__file__).resolve().parents[1].parent / "period_engine_v0"
if str(_PEER) not in sys.path:
    sys.path.insert(0, str(_PEER))
from reconstruct import load_pbp, period_table_from_pbp  # type: ignore

from simulate import PlayCatalog, simulate_one, stable_seed, build_catalog
from validation.asof_grade import build_asof_history_for_game
from config_load import load_config


_PERIOD_KEYS = [
    "q1_home", "q1_away", "q2_home", "q2_away", "q3_home", "q3_away", "q4_home", "q4_away",
    "h1_home", "h1_away", "h2_home", "h2_away", "reg_home", "reg_away", "fg_home", "fg_away",
]


def reconstruct_actual_periods(pbp_path: str | Path, game_id: str) -> dict[str, Any]:
    t = period_table_from_pbp(load_pbp(pbp_path))
    hit = t[t["game_id"] == game_id]
    if hit.empty:
        return {"status": "MISSING_GAME", "game_id": game_id}
    r = hit.iloc[0]
    out = {"status": "OK", "game_id": game_id}
    for k in _PERIOD_KEYS:
        out[k] = int(r[k]) if k in r.index and pd.notna(r[k]) else None
    # reconcile
    if out["h1_home"] is not None:
        out["recon_h1"] = (out["q1_home"] + out["q2_home"] == out["h1_home"]) and (
            out["q1_away"] + out["q2_away"] == out["h1_away"]
        )
        out["recon_reg"] = (out["h1_home"] + out["h2_home"] == out["reg_home"]) and (
            out["h1_away"] + out["h2_away"] == out["reg_away"]
        )
    return out


def _brier_home_win(pred_h: np.ndarray, pred_a: np.ndarray, actual_h: float, actual_a: float) -> float:
    """Brier for P(home period points > away); ties → outcome 0 (non-win), pred = P(h>a)."""
    p = float(np.mean(pred_h > pred_a))
    y = 1.0 if actual_h > actual_a else 0.0
    return (p - y) ** 2


def grade_periods_for_games(
    pbp_path: str | Path,
    grade_rows: list[dict],
    *,
    n_sims: int = 150,
    seed_base: int = 20261105,
    config_path: str | Path | None = None,
) -> dict[str, Any]:
    """For each GRADED_FULL row, resim with period snapshots; compare to reconstructed actuals."""
    root = Path(__file__).resolve().parents[1]
    cfg_path = Path(config_path) if config_path else root / "config/jax_bal_tnf_2026-11-05_data_only.json"
    base_cfg = load_config(cfg_path)
    by_game = []
    # collectors for metrics
    err = {k: [] for k in [
        "q1_home", "q1_away", "h1_home", "h1_away", "h2_home", "h2_away",
        "reg_home", "reg_away", "fg_home", "fg_away",
    ]}
    brier = {"h1": [], "h2": [], "reg": [], "fg": []}

    for g in grade_rows:
        if g.get("grade_status") != "GRADED_FULL":
            by_game.append({**g, "period_grade_status": "SKIPPED_NOT_GRADED_FULL"})
            continue
        act = reconstruct_actual_periods(pbp_path, g["game_id"])
        if act["status"] != "OK":
            by_game.append({**g, "period_grade_status": "ACTUAL_PERIODS_MISSING", "actual_periods": act})
            continue
        asof = build_asof_history_for_game(
            pbp_path, home=g["home"], away=g["away"], season=2026, week=g["week"]
        )
        if asof["status"] != "OK":
            by_game.append({**g, "period_grade_status": f"ASOF_{asof['status']}"})
            continue
        cfg = dict(base_cfg)
        cfg["game"] = {"home": g["home"], "away": g["away"], "season": 2026, "week_asof_exclusive": g["week"]}
        cat, _prov = build_catalog(asof["df"], cfg, games_df=asof.get("def_df"))
        seed = stable_seed(seed_base, g["week"], g["game_id"] + "|period")
        rng = np.random.default_rng(seed)
        snaps = []
        for _ in range(n_sims):
            st = simulate_one(asof["df"], cat, cfg, np.random.default_rng(int(rng.integers(0, 2**31 - 1))))
            snap = st.period_snapshot()
            if st.reg_score_home is not None:
                snap["reg_home"] = st.reg_score_home
                snap["reg_away"] = st.reg_score_away
            snaps.append(snap)
        pred = {k: float(np.mean([s[k] for s in snaps])) for k in err}
        # arrays for brier
        arr = {k: np.asarray([s[k] for s in snaps]) for k in ("h1_home", "h1_away", "h2_home", "h2_away", "reg_home", "reg_away", "fg_home", "fg_away")}
        row_err = {}
        for k in err:
            row_err[f"pred_{k}"] = pred[k]
            row_err[f"actual_{k}"] = act[k]
            row_err[f"abs_err_{k}"] = abs(pred[k] - act[k]) if act[k] is not None else None
            if row_err[f"abs_err_{k}"] is not None:
                err[k].append(row_err[f"abs_err_{k}"])
        row_brier = {
            "brier_h1_home_win": _brier_home_win(arr["h1_home"], arr["h1_away"], act["h1_home"], act["h1_away"]),
            "brier_h2_home_win": _brier_home_win(arr["h2_home"], arr["h2_away"], act["h2_home"], act["h2_away"]),
            "brier_reg_home_win": _brier_home_win(arr["reg_home"], arr["reg_away"], act["reg_home"], act["reg_away"]),
            "brier_fg_home_win": _brier_home_win(arr["fg_home"], arr["fg_away"], act["fg_home"], act["fg_away"]),
        }
        brier["h1"].append(row_brier["brier_h1_home_win"])
        brier["h2"].append(row_brier["brier_h2_home_win"])
        brier["reg"].append(row_brier["brier_reg_home_win"])
        brier["fg"].append(row_brier["brier_fg_home_win"])
        by_game.append({
            **{k: g[k] for k in ("game_id", "week", "home", "away", "grade_status")},
            "period_grade_status": "GRADED_PERIODS",
            "n_sims": n_sims,
            "seed": seed,
            "actual_recon_h1": act.get("recon_h1"),
            "actual_recon_reg": act.get("recon_reg"),
            **row_err,
            **row_brier,
        })

    metrics = {
        "n_games_period_graded": sum(1 for r in by_game if r.get("period_grade_status") == "GRADED_PERIODS"),
        "mae_q1_home": float(np.mean(err["q1_home"])) if err["q1_home"] else None,
        "mae_q1_away": float(np.mean(err["q1_away"])) if err["q1_away"] else None,
        "mae_h1_home": float(np.mean(err["h1_home"])) if err["h1_home"] else None,
        "mae_h1_away": float(np.mean(err["h1_away"])) if err["h1_away"] else None,
        "mae_h2_home": float(np.mean(err["h2_home"])) if err["h2_home"] else None,
        "mae_h2_away": float(np.mean(err["h2_away"])) if err["h2_away"] else None,
        "mae_reg_home": float(np.mean(err["reg_home"])) if err["reg_home"] else None,
        "mae_reg_away": float(np.mean(err["reg_away"])) if err["reg_away"] else None,
        "mae_fg_home": float(np.mean(err["fg_home"])) if err["fg_home"] else None,
        "mae_fg_away": float(np.mean(err["fg_away"])) if err["fg_away"] else None,
        "brier_h1_home_win": float(np.mean(brier["h1"])) if brier["h1"] else None,
        "brier_h2_home_win": float(np.mean(brier["h2"])) if brier["h2"] else None,
        "brier_reg_home_win": float(np.mean(brier["reg"])) if brier["reg"] else None,
        "brier_fg_home_win": float(np.mean(brier["fg"])) if brier["fg"] else None,
        "label": "development_w1_8_period_grade_not_untouched_holdout",
        "note": "Period MAE/Brier reported separately from FG; ties count as home non-win for Brier",
    }
    return {"by_game": by_game, "metrics": metrics, "n_sims": n_sims}
