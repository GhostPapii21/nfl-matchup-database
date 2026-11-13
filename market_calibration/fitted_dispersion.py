"""Opt-in fitted dispersion (NFL-75 item 5). Research only.

Default mode is "fixed": it returns exactly the hand-set values used today, so nothing changes unless a caller asks
for mode="fitted_nflverse_v1" (or sets NFL_DISPERSION_MODE=fitted_nflverse_v1).

fixed values (hand-set, NOT fitted) and where they come from:
  margin SD 13.5, total SD 13.0  research/runs/2026-11-12_TNF_WAS_NYG_layers/script_layer.py ("structural, not fitted")
  rec:WR 0.70, rec:TE 0.75, rush:RB 0.45  lognormal sigmas typed in research/runs/2026-11-12_TNF_WAS_NYG_layers/legs.py
                                          (Nabers / Likely / Skattebo rows; also script_layer.py Nabers 0.70)
fitted values: market_calibration/fitted/dispersion_fit_nflverse_v1.json, written by fit_dispersion_nflverse.py.
"""
from __future__ import annotations
import json, os
from functools import lru_cache
from pathlib import Path
import numpy as np

FIXED = "fixed"
FITTED = "fitted_nflverse_v1"
MODES = (FIXED, FITTED)
DEFAULT_MODE = FIXED
FIT_PATH = Path(__file__).parent / "fitted/dispersion_fit_nflverse_v1.json"
FIXED_VALUES = {"margin_sd": 13.5, "total_sd": 13.0,
                "yard_sigma": {"rec:WR": 0.70, "rec:TE": 0.75, "rush:RB": 0.45}}


def resolve_mode(mode: str | None = None) -> str:
    m = mode or os.environ.get("NFL_DISPERSION_MODE") or DEFAULT_MODE
    if m not in MODES:
        raise ValueError(f"unknown dispersion mode {m!r}; allowed {MODES}")
    return m


@lru_cache(maxsize=8)
def _load(path: str) -> dict:
    return json.loads(Path(path).read_text())


def _cell(edges, values: dict, x: float):
    i = int(np.searchsorted(edges, x, side="right") - 1)
    i = min(max(i, 0), len(edges) - 2)
    return values[f"[{edges[i]:g},{edges[i+1]:g})"]


def margin_sd(abs_spread: float, mode: str | None = None, fit: dict | None = None) -> float:
    if resolve_mode(mode) == FIXED:
        return FIXED_VALUES["margin_sd"]
    f = (fit or _load(str(FIT_PATH)))["margin_sd_by_abs_spread"]
    return float(_cell(f["bins"], f["values"], abs(float(abs_spread)))["sd"])


def total_sd(total_line: float, mode: str | None = None, fit: dict | None = None) -> float:
    if resolve_mode(mode) == FIXED:
        return FIXED_VALUES["total_sd"]
    f = (fit or _load(str(FIT_PATH)))["total_sd_by_total_line"]
    return float(_cell(f["bins"], f["values"], float(total_line))["sd"])


def yard_sigma(stat: str, pos: str, line: float, mode: str | None = None, fit: dict | None = None) -> float:
    key = f"{stat}:{pos}"
    if resolve_mode(mode) == FIXED:
        if key not in FIXED_VALUES["yard_sigma"]:
            raise KeyError(f"no fixed sigma for {key}")
        return FIXED_VALUES["yard_sigma"][key]
    f = (fit or _load(str(FIT_PATH)))["player_yards_lognormal"][key]
    c = _cell(f["bins"], f["cells"], float(line))
    if c["sigma"] is None:
        raise KeyError(f"no fitted sigma for {key} line {line}")
    return float(c["sigma"])


def yard_cell(stat: str, pos: str, line: float, fit: dict | None = None) -> dict:
    """Fitted (p0, med_ratio, sigma, n) cell for a stat/position/line-size bin."""
    f = (fit or _load(str(FIT_PATH)))["player_yards_lognormal"][f"{stat}:{pos}"]
    return dict(_cell(f["bins"], f["cells"], float(line)))
