"""Situational opportunity + conditional success tables (team-only W1–8)."""
from __future__ import annotations
from typing import Any
import numpy as np
import pandas as pd


def _rate(num: int, den: int) -> float | None:
    return float(num) / den if den else None


def third_down_table(df: pd.DataFrame) -> dict[str, Any]:
    out = {"by_team": {}, "n_total": 0}
    snaps = df[df["down"] == 3].copy()
    out["n_total"] = int(len(snaps))
    for team, g in snaps.groupby("posteam"):
        # prefer explicit flags when present
        if "third_down_converted" in g.columns:
            opp = g[g["play_type"].isin(["pass", "run", "qb_kneel", "qb_spike"])]
            conv = int((opp["third_down_converted"] == 1).sum())
            fail = int((opp["third_down_failed"] == 1).sum()) if "third_down_failed" in opp.columns else int(len(opp) - conv)
            den = conv + fail if (conv + fail) > 0 else int(len(opp))
        else:
            opp = g[g["play_type"].isin(["pass", "run"])]
            conv = int((opp["first_down"] == 1).sum())
            den = int(len(opp))
            fail = den - conv
        out["by_team"][team] = {
            "n_opportunities": den,
            "n_conversions": conv,
            "n_failures": fail,
            "p_convert_given_opportunity": _rate(conv, den),
            "status": "OK" if den >= 20 else "SPARSE",
        }
    return out


def red_zone_table(df: pd.DataFrame) -> dict[str, Any]:
    out = {"by_team": {}, "n_total": 0}
    rz = df[df["yardline_100"] <= 20].copy()
    rz = rz[rz["play_type"].isin(["pass", "run", "field_goal"])]
    out["n_total"] = int(len(rz))
    for team, g in rz.groupby("posteam"):
        # opportunity ≈ unique game+drive in RZ if drive col present else plays
        if "drive" in g.columns:
            trips = g.groupby(["game_id", "drive"]).agg(
                td=("touchdown", "max"),
                fg=("play_type", lambda s: int((s == "field_goal").any())),
            )
            n_trips = int(len(trips))
            n_td = int((trips["td"] == 1).sum())
            out["by_team"][team] = {
                "n_rz_trips": n_trips,
                "n_rz_td_drives": n_td,
                "p_td_given_rz_trip": _rate(n_td, n_trips),
                "n_rz_plays": int(len(g)),
                "status": "OK" if n_trips >= 8 else "SPARSE",
            }
        else:
            out["by_team"][team] = {"n_rz_plays": int(len(g)), "status": "SPARSE", "note": "no drive col"}
    return out


def qb_hit_completion(df: pd.DataFrame) -> dict[str, Any]:
    """PROXY: qb_hit split — NOT true pressure/blitz."""
    out = {"proxy_label": "qb_hit_NOT_measured_pressure_or_blitz", "by_passer": {}, "n_total": 0}
    passes = df[df["play_type"] == "pass"].copy()
    if "qb_hit" not in passes.columns:
        return {"status": "MISSING_COLUMN", "proxy_label": out["proxy_label"]}
    out["n_total"] = int(len(passes))
    for (team, qb), g in passes.groupby(["posteam", "passer_player_name"]):
        if not isinstance(qb, str):
            continue
        hit = g[g["qb_hit"] == 1]
        no = g[g["qb_hit"] != 1]
        def _comp(x):
            if "complete_pass" not in x.columns or len(x) == 0:
                return None, 0
            return _rate(int((x["complete_pass"] == 1).sum()), int(len(x))), int(len(x))
        c_hit, n_hit = _comp(hit)
        c_no, n_no = _comp(no)
        out["by_passer"][f"{team}:{qb}"] = {
            "n_hit": n_hit,
            "comp_given_hit": c_hit,
            "n_no_hit": n_no,
            "comp_given_no_hit": c_no,
            "status": "SPARSE" if (n_hit + n_no) < 20 else "PROXY_OK",
        }
    out["status"] = "PROXY"
    return out


def rb_ypc_vs_defense(df: pd.DataFrame, games_df: pd.DataFrame | None = None) -> dict[str, Any]:
    """Opponent-adjusted RB YPC: offense runs grouped by defteam (team-only window)."""
    runs = df[df["play_type"] == "run"].copy()
    out = {"by_offense_vs_def": {}, "status": "OK"}
    if runs.empty or "defteam" not in runs.columns:
        return {"status": "MISSING", "by_offense_vs_def": {}}
    for (off, deff), g in runs.groupby(["posteam", "defteam"]):
        ypc = float(pd.to_numeric(g["yards_gained"], errors="coerce").mean())
        out["by_offense_vs_def"][f"{off}_vs_{deff}"] = {
            "n_carries": int(len(g)),
            "ypc": ypc,
            "status": "OK" if len(g) >= 10 else "SPARSE",
        }
    # Highlight JAX vs BAL and BAL vs JAX if present
    out["matchup_jax_vs_bal"] = out["by_offense_vs_def"].get("JAX_vs_BAL", {"status": "SPARSE", "n_carries": 0, "note": "no W1–8 H2H in window"})
    out["matchup_bal_vs_jax"] = out["by_offense_vs_def"].get("BAL_vs_JAX", {"status": "SPARSE", "n_carries": 0, "note": "no W1–8 H2H in window"})
    return out


def pass_location_counts(df: pd.DataFrame) -> dict[str, Any]:
    """Field zone attempt frequencies only — NOT routes vs CB."""
    passes = df[df["play_type"] == "pass"]
    if "pass_location" not in passes.columns:
        return {"status": "MISSING"}
    out = {"by_team": {}, "label": "pass_location_NOT_route_or_coverage"}
    for team, g in passes.groupby("posteam"):
        vc = g["pass_location"].value_counts(dropna=False).to_dict()
        out["by_team"][team] = {str(k): int(v) for k, v in vc.items()}
    out["status"] = "OK_LOCATION_ONLY"
    return out


def build_situational_report(df: pd.DataFrame, games_df: pd.DataFrame | None = None) -> dict[str, Any]:
    td = third_down_table(df)
    rz = red_zone_table(df)
    qh = qb_hit_completion(df)
    rb = rb_ypc_vs_defense(df, games_df)
    loc = pass_location_counts(df)
    return {
        "third_down": td,
        "red_zone": rz,
        "qb_hit_completion_proxy": qh,
        "rb_ypc_vs_defense": rb,
        "pass_location_not_coverage": loc,
        "missing_explicit": [
            "blitz", "was_pressure", "number_of_pass_rushers",
            "defense_man_zone_type", "defense_coverage_type", "route",
            "primary_cb_assignment", "middle_field_open_closed",
            "DT_replacement_effects",
        ],
        "ns": {
            "third_down_n": td.get("n_total"),
            "rz_n": rz.get("n_total"),
            "qb_hit_n": qh.get("n_total"),
        },
    }
