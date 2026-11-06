"""Dated forward-only QB/injury adjustment layer — no fabricated histories."""
from __future__ import annotations
from typing import Any
import pandas as pd


def apply_forward_qb_filter(df: pd.DataFrame, adjustments: dict[str, Any]) -> tuple[pd.DataFrame, dict]:
    """Filter pass plays for forward sims. Does not mutate historical meaning of W1–8 rows used as catalog.
    When enabled, BAL pass catalog becomes starter-only (Fagnano); Lamar excluded; Huntley excluded from starter pool.
    Fabrication forbidden.
    """
    meta: dict[str, Any] = {}
    if not adjustments or not adjustments.get("enabled"):
        return df.copy(), {"enabled": False}
    out = df.copy()
    qb = adjustments.get("qb", {})
    for team, spec in qb.items():
        team_pass = out[(out["posteam"] == team) & (out["play_type"] == "pass")]
        n_before = int(len(team_pass))
        out_passers = list(spec.get("out") or [])
        doubtful = list(spec.get("doubtful_excluded_from_starter_pool") or [])
        starter = spec.get("starter")
        filt = spec.get("pass_play_filter")
        fabricated = bool(spec.get("fabricate_replacement_history", False))
        if fabricated:
            raise RuntimeError("fabricate_replacement_history must be false")
        excluded = out_passers + doubtful
        if filt == "starter_only_when_adjustments_enabled" and starter:
            # keep non-pass rows; for pass rows keep only starter passer
            keep_mask = ~((out["posteam"] == team) & (out["play_type"] == "pass")) | (
                out["passer_player_name"] == starter
            )
            out = out[keep_mask].copy()
        elif excluded:
            keep_mask = ~((out["posteam"] == team) & (out["play_type"] == "pass") & out["passer_player_name"].isin(excluded))
            out = out[keep_mask].copy()
        team_pass_after = out[(out["posteam"] == team) & (out["play_type"] == "pass")]
        meta[team] = {
            "starter": starter,
            "excluded_passers": out_passers,
            "doubtful_excluded": doubtful,
            "n_pass_before": n_before,
            "n_pass_after": int(len(team_pass_after)),
            "fabricated": False,
            "forward_only": True,
            "asof_et": adjustments.get("asof_et"),
            "sparse_qb": int(len(team_pass_after)) < 50,
        }
    meta["enabled"] = True
    meta["do_not_apply_retroactively_to_w1_8_history_rows"] = adjustments.get(
        "do_not_apply_retroactively_to_w1_8_history_rows", True
    )
    return out, meta
