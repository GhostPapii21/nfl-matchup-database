"""NFL-75 item 6: opt-in weather and injury (availability) adjustments for the possession engine. Research only.

Both are OFF unless a config asks for them AND the call names them in simulate_games(research_unaccepted=...), with
n <= RESEARCH_MAX_N. Off (absent key, None or "off") changes nothing: no extra RNG draws, no catalog change, no new
output keys, so default output is bit-identical to main 3dad900 (tests/test_environment_adjust.py).

Status: both stay OFF (no config enables them) until a forecast-based weather version exists -- the only backtest so
far used kickoff weather observations, which is optimistic -- and injury evidence has known publication times.

Weather  cfg["environment"]["weather"] = {
    "mode": "rain_wind_v1", "rain": R (0..1), "wind_mph": float,
    "effects_path": repo-relative path to a fit_rain_effects.py JSON (uses its "pooled" any_rain / wind10 model),
    "evidence": {"source": ..., "asof": ...}}                 # required; refused without it
  Applied per completed, non-sack pass row drawn from the catalog (team-level efficiency only):
    W = max(0, wind_mph - 10) / 10
    keep-completion probability  = 1 + c_rain*R + c_wind*W   (completion_pct pct_of_baseline)
    completed yards              = round(yards * (1 + y_rain*R + y_wind*W))  for yards > 0 (yards_per_completion)
  A coefficient is used only when the fit marks it "clear" (|change| > 1.96 SE); otherwise 0.
  Not modelled (declared): pass-rate / attempts change, interception and sack rates (not clear in the fit), deep-share.

Availability  cfg["availability"] = {
    "mode": "injury_report_out_v1", "out_player_ids": {TEAM: [gsis_id, ...]},
    "evidence": {"source": ..., "asof": ...}}                 # required; refused without it
  Removes the listed players' history rows (as passer, rusher or receiver) from their team's offense catalog, so the
  team's remaining plays are resampled in their place. If removing a passer would leave the team < 50 pass rows
  (the existing adjustments.py sparse-QB threshold) the passer rows are kept and the team is flagged
  SPARSE_QB_KEPT. No replacement history is fabricated.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Optional
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
WEATHER_MODES = ("off", "rain_wind_v1")
AVAIL_MODES = ("off", "injury_report_out_v1")
RESEARCH_NAMES = {"weather": "weather_rain_wind_v1", "availability": "injury_report_out_v1"}
ID_COLS = ("passer_player_id", "rusher_player_id", "receiver_player_id")
SPARSE_QB_MIN = 50


def _mode(spec, allowed, what) -> str:
    if spec is None:
        return "off"
    m = spec.get("mode") if isinstance(spec, dict) else spec
    m = "off" if m in (None, False, "off") else m
    if m not in allowed:
        raise ValueError(f"unknown {what} mode {m!r}; allowed {allowed}")
    return m


def weather_mode(cfg: dict) -> str:
    return _mode((cfg.get("environment") or {}).get("weather"), WEATHER_MODES, "weather")


def availability_mode(cfg: dict) -> str:
    return _mode(cfg.get("availability"), AVAIL_MODES, "availability")


def _need_evidence(spec: dict, what: str) -> None:
    ev = spec.get("evidence") or {}
    if not ev.get("source") or not ev.get("asof"):
        raise ValueError(f"UNSUPPORTED: {what} adjustment needs evidence.source and evidence.asof (point-in-time)")


def build_weather(cfg: dict) -> Optional[dict]:
    if weather_mode(cfg) == "off":
        return None
    spec = cfg["environment"]["weather"]
    _need_evidence(spec, "weather")
    R = float(spec["rain"]); wind = float(spec.get("wind_mph") or 0.0)
    if not 0.0 <= R <= 1.0 or wind < 0:
        raise ValueError("weather rain must be in [0,1] and wind_mph >= 0")
    path = REPO / spec["effects_path"]
    fit = json.loads(path.read_text())
    pooled = fit["pooled"]

    def coef(metric, term):
        e = pooled[metric][term]
        return float(e["pct_of_baseline"]) if e.get("clear") else 0.0
    W = max(0.0, wind - 10.0) / 10.0
    keep = 1.0 + coef("completion_pct", "any_rain") * R + coef("completion_pct", "wind10") * W
    ypc = 1.0 + coef("yards_per_completion", "any_rain") * R + coef("yards_per_completion", "wind10") * W
    import hashlib
    return {"mode": "rain_wind_v1", "rain": R, "wind_mph": wind, "W": W,
            "keep_completion": float(np.clip(keep, 0.0, 1.0)), "ypc_factor": float(max(ypc, 0.0)),
            "effects_path": spec["effects_path"], "effects_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "effects_seasons": fit.get("seasons"), "evidence": spec["evidence"]}


def apply_weather_row(rng: np.random.Generator, wx: dict, row):
    """Return the (possibly modified copy of the) sampled row. Draws one uniform per completed non-sack pass only."""
    if str(row["play_type"]) != "pass":
        return row
    cp, sk = row.get("complete_pass"), row.get("sack")
    if cp is None or pd.isna(cp) or int(cp) != 1 or (sk is not None and not pd.isna(sk) and int(sk) == 1):
        return row
    u = rng.random()
    r = row.copy()
    if u >= wx["keep_completion"]:
        r["complete_pass"] = 0
        r["incomplete_pass"] = 1
        r["yards_gained"] = 0.0
        r["fumble_lost"] = 0  # an incompletion cannot be a lost fumble
        r["_wx"] = "incomplete"
        return r
    y = row.get("yards_gained")
    if y is not None and not pd.isna(y) and float(y) > 0:
        r["yards_gained"] = float(round(float(y) * wx["ypc_factor"]))
    r["_wx"] = "scaled"
    return r


def apply_availability(df: pd.DataFrame, cfg: dict) -> tuple[pd.DataFrame, dict]:
    if availability_mode(cfg) == "off":
        return df, {"mode": "off"}
    spec = cfg["availability"]
    _need_evidence(spec, "availability")
    missing = [c for c in ID_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"UNSUPPORTED: availability needs history columns {missing}")
    out = df
    meta: dict[str, Any] = {"mode": "injury_report_out_v1", "evidence": spec["evidence"], "teams": {}}
    for team, ids in sorted((spec.get("out_player_ids") or {}).items()):
        ids = set(ids or ())
        t = out["posteam"] == team
        hit_rr = out["rusher_player_id"].isin(ids) | out["receiver_player_id"].isin(ids)
        hit_pass = out["passer_player_id"].isin(ids) & (out["play_type"] == "pass")
        n_pass = int((t & (out["play_type"] == "pass")).sum())
        n_pass_after = int((t & (out["play_type"] == "pass") & ~hit_pass & ~hit_rr).sum())
        kept_qb = n_pass_after < SPARSE_QB_MIN and bool((t & hit_pass).any())
        drop = t & (hit_rr | (hit_pass if not kept_qb else False))
        meta["teams"][team] = {"out_ids": sorted(ids), "rows_removed": int(drop.sum()), "team_rows": int(t.sum()),
                               "pass_rows_before": n_pass, "passer_rows_kept_sparse": kept_qb}
        out = out[~drop]
    return out.reset_index(drop=True), meta


def check_research_call(cfg: dict, research_unaccepted: tuple, n: int, cap: int) -> list[str]:
    """Names of the enabled adjustments; refuse unless each is named in research_unaccepted and n <= cap."""
    on = []
    if weather_mode(cfg) != "off":
        on.append(RESEARCH_NAMES["weather"])
    if availability_mode(cfg) != "off":
        on.append(RESEARCH_NAMES["availability"])
    for name in on:
        if name not in tuple(research_unaccepted or ()):
            raise ValueError(f"UNSUPPORTED: {name} is research only; pass research_unaccepted=({name!r},) with n <= {cap}")
    if on and int(n) > cap:
        raise ValueError(f"research_unaccepted runs are capped at n={cap} (got {n}); never 100k")
    return on
