"""Player-by-player opportunity board for one game.

Connects the pregame usage table, depth chart, snap shares and injury report to the
dashboard.opportunity distribution engines. Volume (targets, carries) is kept apart from
efficiency (catch rate, yards per catch, yards per carry). A missing input blocks or
downgrades only the projection that needs it. No stand-in rate is written in its place.

Model identities stay separate. player_baselines are attached for comparison and are not
fed into the draws. The possession-engine opportunity recorder, the joint producer and the
period engine are not executed.

Research only. projection_ready stays false.

    python3 -m sunday.player_board \\
        --packet pregame/packets/2026_12_DEN_PIT/packet.json \\
        --pbp data/historical/nflverse/pbp_2026_w1_11_pulled_20261124T1717ET.parquet \\
        --rosters data/historical/nflverse/roster_weekly_2026.parquet \\
        --snaps data/historical/nflverse/snaps_2026.parquet \\
        --out sunday/replays/2026_12_DEN_PIT
"""
from __future__ import annotations

import argparse
import json
import subprocess
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

from dashboard import extras as X
from dashboard import opportunity as O

SCHEMA = "sunday-player-board/1"
ROOT = Path(__file__).resolve().parents[1]

# Questionable skill players' snap share vs their usual, fit in research/projections_2026_w12/project.py.
# No default is applied for a position that is not in this map.
QUESTIONABLE_SNAP_SHARE = {"RB": 0.69, "TE": 0.89, "WR": 0.91}
QUESTIONABLE_SNAP_SOURCE = "research/projections_2026_w12/project.py QF"

OUT_STATUSES = {"out", "doubtful", "injured reserve", "ir", "suspension", "suspended"}
QUESTIONABLE_STATUSES = {"questionable"}
MIN_TARGETS = 8
MIN_CARRIES = 8
MIN_GAMES_FOR_DISPERSION = 3
ROLE_SHARE_SHIFT = 0.08
CHECKDOWN_AIR_LT = 5.0
CHECKDOWN_SHARE = 0.25
CHECKDOWN_MIN = 8
EXPLOSIVE_RATE = 0.15
EXPLOSIVE_MIN_TARGETS = 20

PBP_COLUMNS = (
    "posteam", "defteam", "week", "game_id", "play_type", "down", "season_type", "two_point_attempt",
    "pass_attempt", "sack", "qb_hit", "air_yards", "yardline_100", "receiver_player_id", "receiver_player_name",
    "rusher_player_id", "rusher_player_name", "passer_player_id", "passer_player_name",
    "third_down_converted", "third_down_failed", "home_team", "yards_gained", "complete_pass",
    "rush_attempt", "qb_scramble", "receiving_yards", "rushing_yards",
)

NOT_INVOKED = (
    ("core.possession_engine_v0.opportunity.OpportunityRecorder",
     "Snap-level role draws and red-zone event allocation. Not executed, so no TD probability is taken from it."),
    ("core.possession_engine_v0.joint_producer.OpportunityModel",
     "Frozen usage-cell producer. Not executed."),
    ("core.period_engine_v0.monte_carlo",
     "Team quarter-score engine. It does not project a player."),
)


def _r(x, nd=3):
    try:
        x = float(x)
    except (TypeError, ValueError):
        return None
    if x != x or x in (float("inf"), float("-inf")):
        return None
    return round(x, nd)


def _num(s):
    return pd.to_numeric(s, errors="coerce")


def aliases(name) -> set[str]:
    """Join keys for 'Jaylen Waddle', 'J.Waddle' and 'J.K. Dobbins'."""
    raw = str(name or "").strip()
    if not raw:
        return set()
    parts = [p for p in raw.replace(".", " ").replace("'", "").replace("’", "").split()
             if p.upper() not in {"JR", "SR", "II", "III", "IV", "V"}]
    out = {raw.lower(), "".join(parts).lower()}
    if len(parts) >= 2:
        out.add((parts[0][0] + parts[-1]).lower())
        out.add(f"{parts[0][0]}.{parts[-1]}".lower())
    return {a for a in out if a}


def _index_named(rows: list[dict], field: str) -> dict:
    buckets: dict[str, list] = {}
    for row in rows or []:
        for key in aliases(row.get(field)):
            buckets.setdefault(key, []).append(row)
    clean = {}
    for key, group in buckets.items():
        if len({id(r) for r in group}) == 1:
            clean[key] = group[0]
    return clean


def _lookup(name, index: dict):
    for key in aliases(name):
        if key in index:
            return index[key]
    return None


def _status_rank(status) -> int:
    s = str(status or "").strip().lower()
    if s in OUT_STATUSES:
        return 3
    if s in QUESTIONABLE_STATUSES:
        return 2
    if not s or s in {"none", "nan"}:
        return 0
    return 1


def availability(name, official: list[dict] | None, espn: list[dict] | None) -> dict:
    """The stronger of the official report and the ESPN list. Not-listed is not 'healthy'."""
    off = _lookup(name, _index_named(official or [], "player"))
    live = _lookup(name, _index_named(espn or [], "player"))
    sources = []
    if off:
        sources.append({"source": off.get("source") or "nflverse official report", "game_status": off.get("game_status"),
                        "practice_status": off.get("practice_status"), "injury": off.get("injury"), "matched": off.get("player")})
    if live:
        sources.append({"source": "espn_live", "game_status": live.get("status"), "comment": live.get("comment"),
                        "matched": live.get("player"), "date": live.get("date")})
    best = max(sources, key=lambda r: _status_rank(r.get("game_status")), default=None)
    if best is None:
        return {"state": "not_listed", "game_status": None,
                "note": "Not on the official report or the ESPN list. That is unknown, not a healthy designation.",
                "sources": []}
    state = {_status_rank(best.get("game_status")): "out"}.get(_status_rank(best.get("game_status")), "other")
    rank = _status_rank(best.get("game_status"))
    if rank >= 3:
        state = "out"
    elif rank == 2:
        state = "questionable"
    elif rank == 1:
        state = "other"
    else:
        state = "practice_only"
    return {"state": state, "game_status": best.get("game_status"), "sources": sources}


def _blend_share(log, weeks_map, stat_key, stored):
    """60/40 season-and-last-3 blend used by dashboard.opportunity.board_side. None when it cannot be measured."""
    if not weeks_map or not log:
        return stored, None, "stored_share_only"
    played = sum(weeks_map.get(x.get("week"), 0) or 0 for x in log)
    if not played:
        return stored, None, "stored_share_only"
    share = sum(x.get(stat_key, 0) or 0 for x in log) / played
    last3 = log[-3:]
    den3 = sum(weeks_map.get(x.get("week"), 0) or 0 for x in last3)
    share3 = (sum(x.get(stat_key, 0) or 0 for x in last3) / den3) if den3 else None
    if share3 is not None and len(log) >= 5:
        return 0.6 * share + 0.4 * share3, share3, "blend_60_40"
    return share, share3, "season_share_in_window"


def _group(pos) -> str:
    p = (pos or "").upper()
    if p in {"RB", "FB", "HB"}:
        return "RB"
    if p == "TE":
        return "TE"
    return "WR"


def allocate_receiving(rows: list[dict], weeks_map, out_ids: set, questionable: dict[str, str]) -> list[dict]:
    """Target shares after the teammate-out rule and the questionable-snap factors.

    Teammate-out uses dashboard.opportunity.OUT_TOP_SAME / OUT_REST_SAME / OUT_OTHER_GROUP.
    Questionable factors apply only for positions in QUESTIONABLE_SNAP_SHARE.
    """
    included = [r for r in rows if (r.get("targets") or 0) >= MIN_TARGETS and r.get("player_id") not in out_ids]
    out_rows = [r for r in rows if (r.get("targets") or 0) >= MIN_TARGETS and r.get("player_id") in out_ids]
    missing = sum(r.get("target_share") or 0 for r in out_rows)
    healthy = sum(r.get("target_share") or 0 for r in included) or 1.0
    miss_by, top = {}, {}
    for r in out_rows:
        g = _group(r.get("pos"))
        miss_by[g] = miss_by.get(g, 0.0) + (r.get("target_share") or 0)
    for r in included:
        g = _group(r.get("pos"))
        share = r.get("target_share") or 0
        if share > top.get(g, (None, -1))[1]:
            top[g] = (r.get("player_id"), share)

    def bump(r):
        if not missing:
            return 0.0
        own = r.get("target_share") or 0
        same = miss_by.get(_group(r.get("pos")), 0.0)
        other = missing - same
        prop = own / healthy
        if r.get("player_id") == top.get(_group(r.get("pos")), (None,))[0]:
            return max(O.OUT_TOP_SAME, O.OUT_REST_SAME * prop) * same + O.OUT_OTHER_GROUP * other * prop
        return O.OUT_REST_SAME * same * prop + O.OUT_OTHER_GROUP * other * prop

    built = []
    for r in included:
        blended, last3, how = _blend_share(r.get("log") or [], weeks_map, "targets", r.get("target_share") or 0)
        built.append({"row": r, "blended": blended or 0.0, "last3": last3, "how": how, "bump": bump(r),
                      "q_factor": None, "q_source": None, "unassigned": 0.0})
    for b in built:
        pid = b["row"].get("player_id")
        if questionable.get(pid) != "questionable":
            continue
        pos = (b["row"].get("pos") or "").upper()
        factor = QUESTIONABLE_SNAP_SHARE.get(pos)
        if factor is None:
            b["q_factor"] = None
            b["q_note"] = f"Questionable {pos or 'unknown position'} has no fitted snap factor; none was applied."
            continue
        # The fitted factor scales the share he would have had, including redistributed work.
        base = b["blended"] + b["bump"]
        freed = base * (1 - factor)
        b["blended"] = base * factor
        b["bump"] = 0.0
        b["q_factor"] = factor
        b["q_source"] = QUESTIONABLE_SNAP_SOURCE
        mates = [m for m in built if m is not b and _group(m["row"].get("pos")) == _group(b["row"].get("pos"))]
        tot = sum(m["blended"] + m["bump"] for m in mates)
        if tot <= 0:
            b["unassigned"] = freed
            continue
        for m in mates:
            m["bump"] += freed * ((m["blended"] + m["bump"]) / tot)
    total = sum(b["blended"] + b["bump"] for b in built)
    scale = min(1.0, 1.0 / total) if total > 1 else 1.0
    for b in built:
        b["share_used"] = (b["blended"] + b["bump"]) * scale
        b["scale"] = scale
        b["share_sum"] = total
    return built


def allocate_rushing(rows: list[dict], weeks_map, out_ids: set, questionable: dict[str, str], team_carries: float | None) -> list[dict]:
    included = [r for r in rows if (r.get("carries") or 0) >= MIN_CARRIES and r.get("pos") == "RB" and r.get("player_id") not in out_ids]
    out_rows = [r for r in rows if (r.get("carries") or 0) >= MIN_CARRIES and r.get("pos") == "RB" and r.get("player_id") in out_ids]
    missing = sum(r.get("carry_share") or 0 for r in out_rows)
    healthy = sum(r.get("carry_share") or 0 for r in included) or 1.0
    top = max(included, key=lambda r: r.get("carry_share") or 0, default=None)

    def bump(r):
        if not missing:
            return 0.0
        if top is not None and r.get("player_id") == top.get("player_id"):
            return O.OUT_TOP_RB * missing
        return O.OUT_REST_RB * missing * ((r.get("carry_share") or 0) / healthy)

    built = []
    for r in included:
        blended, last3, how = _blend_share(r.get("log") or [], weeks_map, "carries", r.get("carry_share") or 0)
        built.append({"row": r, "blended": blended or 0.0, "last3": last3, "how": how, "bump": bump(r),
                      "q_factor": None, "unassigned": 0.0})
    for b in built:
        pid = b["row"].get("player_id")
        if questionable.get(pid) != "questionable":
            continue
        factor = QUESTIONABLE_SNAP_SHARE.get("RB")
        base = b["blended"] + b["bump"]
        freed = base * (1 - factor)
        b["blended"] = base * factor
        b["bump"] = 0.0
        b["q_factor"] = factor
        b["q_source"] = QUESTIONABLE_SNAP_SOURCE
        mates = [m for m in built if m is not b]
        tot = sum(m["blended"] + m["bump"] for m in mates)
        if tot <= 0:
            b["unassigned"] = freed
            continue
        for m in mates:
            m["bump"] += freed * ((m["blended"] + m["bump"]) / tot)
    raw = []
    for b in built:
        raw.append(min(0.95, b["blended"] + b["bump"]))
    listed = [r for r in rows if r.get("pos") == "RB"]
    listed_carries = sum(r.get("carries") or 0 for r in listed)
    rb_cap = None
    if team_carries:
        rb_cap = min(0.95, listed_carries / team_carries)
    total = sum(raw)
    if rb_cap and total > rb_cap:
        scale = rb_cap / total
        cap_note = "dashboard.opportunity RB share of team carries"
    elif total > 1:
        scale = 1.0 / total
        cap_note = "shares scaled to 1; RB cap not measurable"
    else:
        scale = 1.0
        cap_note = None
    for b, base in zip(built, raw):
        b["share_used"] = base * scale
        b["scale"] = scale
        b["share_sum"] = total
        b["rb_cap"] = rb_cap
        b["cap_note"] = cap_note
    return built


def _seed(game_id, player_id, kind, base) -> int:
    return (zlib.crc32(f"{game_id}|{player_id}|{kind}".encode()) ^ int(base)) & 0xFFFFFFFF


def _target_distribution(exp_targets, k, n, seed) -> dict:
    rng = np.random.default_rng(seed)
    draws = O._volume(rng, exp_targets, "rec", k, n)
    return _draw_summary(draws, (4, 6, 8, 10), None)


def _carry_distribution(exp_carries, k, n, seed) -> dict:
    rng = np.random.default_rng(seed)
    draws = O._volume(rng, exp_carries, "rush", k, n)
    return _draw_summary(draws, O.CARRY_THRESHOLDS, "carries")


def _draw_summary(draws, thresholds, stat) -> dict:
    return {"mean": _r(draws.mean(), 1), "p25": _r(np.percentile(draws, 25), 1), "p50": _r(np.percentile(draws, 50), 1),
            "p75": _r(np.percentile(draws, 75), 1), "thresholds": O.chances(draws, thresholds, stat),
            "uncertainty": "p25/p50/p75 and threshold rates are the engine draws, not a point-estimate interval."}


def _efficiency(own_num, own_den, league_rate, prior, minimum):
    if own_den is None or own_den <= 0 or own_num is None:
        return None, "BLOCKED", "no denominator for this rate"
    if league_rate is not None:
        return O.shrink(own_num, own_den, league_rate, prior), "OK", "dashboard.opportunity.shrink"
    if own_den >= minimum:
        return own_num / own_den, "DOWNGRADED", "league rate missing; raw rate used and shrink was not applied"
    return None, "BLOCKED", f"league rate missing and denominator {own_den:g} is under {minimum}"


def _matchup(player_rate, def_rate, league_rate):
    if player_rate is None:
        return None, {"status": "BLOCKED", "reason": "player rate is missing, so no matchup factor was applied", "model": "dashboard.opportunity.def_factor"}
    if def_rate is None or league_rate is None:
        return player_rate, {"status": "BLOCKED", "reason": "opponent positional rate or league rate is missing; no factor was applied",
                             "model": "dashboard.opportunity.def_factor", "factor": None}
    factor = O.def_factor(def_rate, league_rate)
    return player_rate * factor, {"status": "APPLIED", "model": "dashboard.opportunity.def_factor", "factor": _r(factor, 3),
                                  "defense_rate": _r(def_rate, 3), "league_rate": _r(league_rate, 3),
                                  "cap": "0.80 to 1.20"}


def project_receiving(game_id, player, share, *, team_attempts, margin, pools, defense, n, seed_base) -> dict:
    """One simulate_receiver draw when efficiency and a yard pool exist. Otherwise targets only, or neither."""
    pid = player.get("player_id")
    pos = (player.get("pos") or "WR").upper()
    if pos not in {"WR", "TE", "RB"}:
        pos = "WR"
    lg = (pools or {}).get("catch_rate", {}).get(pos)
    lg_ypr = (pools or {}).get("ypr", {}).get(pos)
    cr, cr_status, cr_how = _efficiency(player.get("receptions"), player.get("targets"), lg, O.PRIOR_TARGETS, 20)
    ypr, ypr_status, ypr_how = _efficiency(player.get("yards"), player.get("receptions"), lg_ypr, O.PRIOR_CATCHES, 10)
    d = defense or {}
    d_tg, d_rec, d_yds = d.get(f"{pos.lower()}_targets_pg"), d.get(f"{pos.lower()}_receptions_pg"), d.get(f"{pos.lower()}_rec_yards_pg")
    d_cr = (d_rec / d_tg) if d_tg else None
    d_ypr = (d_yds / d_rec) if d_rec else None
    cr_adj, cr_match = _matchup(cr, d_cr, lg)
    ypr_adj, ypr_match = _matchup(ypr, d_ypr, lg_ypr)
    efficiency = {"catch_rate": {"status": cr_status, "value": _r(cr_adj, 3), "method": cr_how, "matchup": cr_match,
                                 "numerator": player.get("receptions"), "denominator": player.get("targets")},
                  "yards_per_catch": {"status": ypr_status, "value": _r(ypr_adj, 2), "method": ypr_how, "matchup": ypr_match,
                                      "numerator": player.get("yards"), "denominator": player.get("receptions")}}
    pool = (pools or {}).get("catch", {}).get(pos)
    blocked = {"status": "BLOCKED", "model": "dashboard.opportunity.simulate_receiver"}
    volume = {"status": "BLOCKED", "model": "dashboard.opportunity._volume"}
    if team_attempts is None:
        volume["reason"] = "team pass attempts per game are missing; the 0.55 default pass rate was not used"
        return {"volume": volume, "efficiency": efficiency, "receptions": {**blocked, "reason": volume["reason"]},
                "receiving_yards": {**blocked, "reason": volume["reason"]}}
    if share is None:
        volume["reason"] = "target share is missing"
        return {"volume": volume, "efficiency": efficiency, "receptions": {**blocked, "reason": volume["reason"]},
                "receiving_yards": {**blocked, "reason": volume["reason"]}}
    exp = team_attempts * share
    thin = len(player.get("log") or []) < MIN_GAMES_FOR_DISPERSION
    if thin:
        volume = {"status": "DOWNGRADED", "model": "dashboard.opportunity._volume", "share_used": _r(share, 3),
                  "team_pass_attempts": _r(team_attempts, 2), "accounting_mean": _r(exp, 2),
                  "reason": "fewer than 3 games; the engine default dispersion was not used, and no threshold rate was produced"}
        return {"volume": volume, "efficiency": efficiency,
                "receptions": {**blocked, "reason": volume["reason"]}, "receiving_yards": {**blocked, "reason": volume["reason"]}}
    k = O._dispersion([x.get("targets") for x in player.get("log") or []], exp)
    can_receive = cr_adj is not None and ypr_adj is not None and pool is not None and len(pool) > 0
    if can_receive:
        seed = _seed(game_id, pid, "receive", seed_base)
        tg, rec, yds = O.simulate_receiver(exp_targets=exp, k=k, catch_rate=cr_adj, ypr=ypr_adj,
                                           pool=np.asarray(pool, dtype=float), n=n, seed=seed)
        summary = O.summary_receiver(tg, rec, yds, cr_adj * ypr_adj)
        volume = {"status": "OK", "model": "dashboard.opportunity.simulate_receiver", "share_used": _r(share, 3),
                  "team_pass_attempts": _r(team_attempts, 2), "raw_mean": _r(exp, 3), "dispersion_k": _r(k, 2),
                  "dispersion_source": "player game-to-game target counts",
                  "distribution": _draw_summary(tg, (4, 6, 8, 10), None),
                  "engine_inputs": {"exp_targets": exp, "k": k, "catch_rate": cr_adj, "ypr": ypr_adj, "pool": pos,
                                    "n": n, "seed": seed}}
        receptions = {"status": "DOWNGRADED" if cr_match["status"] != "APPLIED" else "OK",
                      "model": "dashboard.opportunity.simulate_receiver", "mean": summary["receptions_mean"],
                      "thresholds": summary["receptions"], "matchup": cr_match,
                      "uncertainty": "threshold rates are the same simulate_receiver draws, passed through dashboard.opportunity.calibrate where a fitted range exists"}
        yards = {"status": "DOWNGRADED" if ypr_match["status"] != "APPLIED" else "OK",
                 "model": "dashboard.opportunity.simulate_receiver", "mean": summary["yards_mean"], "median": summary["yards_median"],
                 "p25_p75": summary["yards_p25_p75"], "thresholds": summary["yards"], "matchup": ypr_match,
                 "uncertainty": "p25/p75 and threshold rates are those same draws"}
        if cr_match["status"] != "APPLIED" or ypr_match["status"] != "APPLIED":
            receptions["downgrade"] = "unadjusted efficiency; positional matchup factor was not applied"
            yards["downgrade"] = receptions["downgrade"]
        return {"volume": volume, "efficiency": efficiency, "receptions": receptions, "receiving_yards": yards}
    seed = _seed(game_id, pid, "targets", seed_base)
    volume = {"status": "OK", "model": "dashboard.opportunity._volume", "share_used": _r(share, 3),
              "team_pass_attempts": _r(team_attempts, 2), "raw_mean": _r(exp, 3), "dispersion_k": _r(k, 2),
              "distribution": _target_distribution(exp, k, n, seed),
              "engine_inputs": {"exp_targets": exp, "k": k, "n": n, "seed": seed, "kind": "rec"}}
    reason = "catch rate or yards per catch is blocked" if cr_adj is None or ypr_adj is None else "no catch-yard pool for this position; receptions were not drawn without it"
    return {"volume": volume, "efficiency": efficiency, "receptions": {**blocked, "reason": reason},
            "receiving_yards": {**blocked, "reason": reason}}


def project_rushing(game_id, player, share, *, team_carries, pools, defense, n, seed_base) -> dict:
    pid = player.get("player_id")
    volume = {"status": "BLOCKED", "model": "dashboard.opportunity._volume"}
    if team_carries is None:
        volume["reason"] = "team rush attempts per game are missing; no default rush rate was used"
    elif share is None:
        volume["reason"] = "carry share is missing"
    elif len(player.get("log") or []) < MIN_GAMES_FOR_DISPERSION:
        volume["status"] = "DOWNGRADED"
        volume["reason"] = "fewer than 3 games; the engine default dispersion was not used"
        volume["accounting_mean"] = _r(team_carries * share, 2)
    else:
        k = O._dispersion([x.get("carries") for x in player.get("log") or []], team_carries * share)
        seed = _seed(game_id, pid, "carries", seed_base)
        dist = _carry_distribution(team_carries * share, k, n, seed)
        volume = {"status": "OK", "model": "dashboard.opportunity._volume", "share_used": _r(share, 3),
                  "team_rush_attempts": _r(team_carries, 2), "raw_mean": _r(team_carries * share, 3),
                  "dispersion_k": _r(k, 2), "distribution": dist,
                  "engine_inputs": {"exp_carries": team_carries * share, "k": k, "n": n, "seed": seed, "kind": "rush"}}
    lg = (pools or {}).get("ypc")
    ypc, ypc_status, ypc_how = _efficiency(player.get("yards"), player.get("carries"), lg, O.PRIOR_CARRIES, 20)
    d_ypc = (defense or {}).get("rb_yards_per_carry")
    ypc_adj, match = _matchup(ypc, d_ypc, lg)
    efficiency = {"yards_per_carry": {"status": ypc_status, "value": _r(ypc_adj, 2), "method": ypc_how, "matchup": match,
                                      "numerator": player.get("yards"), "denominator": player.get("carries")}}
    yards = {"status": "BLOCKED", "model": "dashboard.opportunity.simulate_rusher"}
    pool = (pools or {}).get("carry")
    attempts = {"status": volume.get("status"), "model": volume.get("model"), "distribution": volume.get("distribution"),
                "accounting_mean": volume.get("accounting_mean"), "reason": volume.get("reason")}
    if volume.get("status") != "OK":
        yards["reason"] = "rushing draws need a carry distribution from the volume engine"
    elif ypc_adj is None:
        yards["reason"] = "yards per carry is blocked"
    elif pool is None or len(pool) == 0:
        yards["reason"] = "no carry-yard pool; rushing yards were not drawn without it"
    else:
        seed = _seed(game_id, pid, "rush", seed_base)
        k = volume["engine_inputs"]["k"]
        exp = volume["engine_inputs"]["exp_carries"]
        car, yds = O.simulate_rusher(exp_carries=exp, k=k, ypc=ypc_adj, pool=np.asarray(pool, dtype=float), n=n, seed=seed)
        summary = O.summary_rusher(car, yds)
        volume = {**volume, "model": "dashboard.opportunity.simulate_rusher", "distribution": _draw_summary(car, O.CARRY_THRESHOLDS, "carries"),
                  "engine_inputs": {**volume["engine_inputs"], "ypc": ypc_adj, "seed": seed}}
        attempts = {"status": "OK", "model": "dashboard.opportunity.simulate_rusher", "mean": summary["carries_mean"],
                    "thresholds": summary["carries"], "distribution": volume["distribution"]}
        yards = {"status": "DOWNGRADED" if match["status"] != "APPLIED" else "OK",
                 "model": "dashboard.opportunity.simulate_rusher", "mean": summary["yards_mean"], "median": summary["yards_median"],
                 "p25_p75": summary["yards_p25_p75"], "thresholds": summary["yards"], "matchup": match,
                 "uncertainty": "p25/p75 and threshold rates are the same simulate_rusher draws"}
        if match["status"] != "APPLIED":
            yards["downgrade"] = "unadjusted efficiency; defensive yards per carry were not applied"
    return {"volume": volume, "efficiency": efficiency, "rush_attempts": attempts, "rushing_yards": yards}


def _ratio(numerator, denominator, source):
    if denominator in (None, 0):
        reason = "denominator missing or zero"
    elif numerator is None:
        reason = "this count was not measured for this player; it was not filled with zero"
    else:
        return {"status": "OK", "value": _r(numerator / denominator, 3), "numerator": numerator, "denominator": denominator, "source": source}
    return {"status": "BLOCKED", "numerator": numerator, "denominator": denominator, "source": source, "reason": reason}


def _blocked(reason, source):
    return {"status": "BLOCKED", "reason": reason, "source": source, "value": None}


def role_tags(player, situational, extras_row, opp_label) -> list[dict]:
    """Issue tags, each traced to an existing label or a measured count. No tag is filled in for a missing split."""
    tags = []
    seen = set()

    def add(tag, why, source):
        if tag in seen:
            return
        seen.add(tag)
        tags.append({"tag": tag, "why": why, "source": source})

    for item in (extras_row or {}).get("tags") or []:
        name = item.get("tag")
        why = item.get("why")
        if name in {"Volume", "Primary"}:
            add("volume", why, "dashboard.extras.receiver_roles")
        elif name == "Deep threat":
            add("explosive", why, "dashboard.extras.receiver_roles")
        elif name in {"Red-zone #1", "Goal-line back"}:
            add("red-zone", why, "dashboard.extras.receiver_roles")
        elif name == "Rising":
            add("expanding", why, "dashboard.extras.receiver_roles")
        elif name == "Falling":
            add("shrinking", why, "dashboard.extras.receiver_roles")
    label = (opp_label or {}).get("label")
    why = (opp_label or {}).get("why")
    mapped = {"expanding": "expanding", "shrinking": "shrinking", "volume-supported": "volume", "efficiency-driven": "efficiency-dependent"}
    if label in mapped:
        add(mapped[label], why, "dashboard.extras.opportunity_label")
    targets = player.get("targets") or 0
    explosive = player.get("explosive")
    if targets >= EXPLOSIVE_MIN_TARGETS and explosive is not None and explosive / targets >= EXPLOSIVE_RATE:
        add("explosive", f"{explosive} explosive plays on {targets} targets ({explosive / targets:.0%}); rule {EXPLOSIVE_RATE:.0%} and at least {EXPLOSIVE_MIN_TARGETS} targets",
            "sunday.player_board explosive count / targets")
    sit = situational or {}
    check = sit.get("checkdown_targets")
    air_den = sit.get("third_down_targets_with_air")
    adot = player.get("avg_depth_of_target")
    if check is None or not targets or air_den is None:
        pass
    elif check >= CHECKDOWN_MIN and check / targets >= CHECKDOWN_SHARE and adot is not None and adot < 8:
        add("checkdown", f"{check} third-down targets with air yards under {CHECKDOWN_AIR_LT:g} ({check / targets:.0%} of {targets} targets)",
            "sunday.player_board measured third-down air yards")
    return tags


def _warnings(player, avail, snap, share_how, last3, blended, situational, inactive: bool) -> list[dict]:
    out = []
    if avail.get("state") == "out":
        out.append({"warning": "out", "detail": f"{avail.get('game_status')} — projections blocked", "sources": avail.get("sources")})
    elif avail.get("state") == "questionable":
        out.append({"warning": "questionable", "detail": "limited-snap factor only if this position has a fitted share", "sources": avail.get("sources")})
    elif avail.get("state") == "practice_only":
        out.append({"warning": "practice", "detail": "practice note without a game status; not treated as out", "sources": avail.get("sources")})
    if snap.get("status") == "MISSING":
        out.append({"warning": "snap_share_missing", "detail": "no snap row matched this player; snap share was not set to zero"})
    if inactive:
        out.append({"warning": "role_change", "detail": "no touch in the team's last two window games; left out of the active share split"})
    if last3 is not None and blended is not None and abs(last3 - blended) >= ROLE_SHARE_SHIFT:
        out.append({"warning": "role_change", "detail": f"last-3 share {last3:.3f} vs window share {blended:.3f} (threshold {ROLE_SHARE_SHIFT})"})
    depth = player.get("_depth") or {}
    share = player.get("target_share") or player.get("carry_share") or 0
    if depth.get("status") == "second_string" and (share >= 0.15 or (snap.get("offense_snap_share") or 0) >= 0.5):
        out.append({"warning": "role_change", "detail": f"listed {depth.get('slot')} second string with share {share:.3f}"})
    if depth.get("status") == "starter" and snap.get("offense_snap_share") is not None and snap["offense_snap_share"] < 0.25 and (player.get("games") or 0) >= 4:
        out.append({"warning": "limited_snap", "detail": f"listed starter, offensive snap share {snap['offense_snap_share']:.3f}"})
    sit = situational or {}
    if sit.get("return_status"):
        out.append({"warning": "return", "detail": sit["return_status"]})
    if share_how == "stored_share_only":
        out.append({"warning": "recent_share", "detail": "team targets by week were missing, so the last-three blend was not applied"})
    return out


def _depth_for(name, depth: dict) -> dict:
    if not depth or depth.get("status") == "UNAVAILABLE":
        return {"status": "UNAVAILABLE", "reason": "depth chart not in the inputs", "slot": None}
    starters = _index_named(depth.get("starters") or [], "player")
    second = _index_named(depth.get("second_string") or [], "player")
    hit = _lookup(name, starters)
    if hit:
        return {"status": "starter", "slot": hit.get("slot"), "group": hit.get("group"), "as_of": depth.get("as_of"), "matched": hit.get("player")}
    hit = _lookup(name, second)
    if hit:
        return {"status": "second_string", "slot": hit.get("slot"), "as_of": depth.get("as_of"), "matched": hit.get("player")}
    return {"status": "unlisted", "slot": None, "as_of": depth.get("as_of"), "reason": "no starter or second-string row matched this name"}


def _snap_for(name, shares: dict) -> dict:
    if not shares:
        return {"status": "UNAVAILABLE", "reason": "snap shares were not supplied", "offense_snap_share": None,
                "denominator": "mean offense_pct over the packet window", "source": "pregame.packet.snap_shares"}
    index = {}
    for person, value in shares.items():
        for key in aliases(person):
            index.setdefault(key, (person, value))
    hit = None
    for key in aliases(name):
        if key in index:
            hit = index[key]
            break
    if hit is None:
        return {"status": "MISSING", "reason": "no snap row matched this player; share was not filled with zero",
                "offense_snap_share": None, "source": "pregame.packet.snap_shares"}
    return {"status": "OK", "offense_snap_share": _r(hit[1], 3), "matched": hit[0],
            "denominator": "mean offense_pct over the weeks in the packet window", "source": "pregame.packet.snap_shares"}


def _site_splits(log, by_game, stat_key) -> dict:
    if not by_game or not log:
        return _blocked("no per-game site on the offense log", "pregame.metrics.game_log")
    site = {}
    for g in by_game:
        opp = str(g.get("opp") or "")
        if opp.startswith("@"):
            site[g.get("week")] = "away"
        elif opp.startswith("vs"):
            site[g.get("week")] = "home"
    if not site:
        return _blocked("game log has no home/away marker", "pregame.metrics.game_log")
    buckets = {"home": [], "away": []}
    skipped = 0
    for row in log:
        where = site.get(row.get("week"))
        if where is None:
            skipped += 1
            continue
        buckets[where].append(row.get(stat_key, 0) or 0)
    def mean(vals):
        return _r(sum(vals) / len(vals), 2) if vals else None
    return {"status": "OK", "source": "pregame.metrics.game_log opp marker joined to the player log",
            "home_games": len(buckets["home"]), "home_per_game": mean(buckets["home"]),
            "away_games": len(buckets["away"]), "away_per_game": mean(buckets["away"]),
            "games_without_site": skipped, "stat": stat_key}


def _last_two(by_game) -> set:
    weeks = sorted({g.get("week") for g in by_game or [] if g.get("week") is not None})
    return set(weeks[-2:])


def _person_records(team: dict) -> list[dict]:
    players = team.get("players") or {}
    merged: dict = {}
    order = []
    for kind, rows in (("receiver", players.get("receivers") or []), ("rusher", players.get("rushers") or []),
                       ("quarterback", players.get("quarterbacks") or [])):
        for row in rows:
            pid = row.get("player_id") or row.get("player")
            if pid not in merged:
                merged[pid] = {"player_id": row.get("player_id"), "player": row.get("player"), "pos": row.get("pos") or ("QB" if kind == "quarterback" else None),
                               "receiving": None, "rushing": None, "passing": None}
                order.append(pid)
            slot = {"receiver": "receiving", "rusher": "rushing", "quarterback": "passing"}[kind]
            merged[pid][slot] = row
            if kind == "quarterback":
                merged[pid]["pos"] = merged[pid]["pos"] or "QB"
            elif row.get("pos"):
                merged[pid]["pos"] = row.get("pos")
    return [merged[i] for i in order]


def _situational_block(sit: dict | None) -> dict:
    sit = sit or {}
    if not sit:
        missing = "play-by-play situational counts were not supplied"
        return {"red_zone": _blocked(missing, "pbp"), "goal_line": _blocked(missing, "pbp"),
                "third_down": _blocked(missing, "pbp"), "checkdown": _blocked(missing, "pbp"),
                "pressure_targets": {**_blocked(missing, "pbp"), "evidence_tier": "unavailable", "charting": "unavailable"},
                "opponent_quality": _blocked(missing, "pbp"),
                "routes": {**_blocked("route participation is not in nflverse play-by-play", "pbp"), "evidence_tier": "unavailable"},
                "route_participation": {**_blocked("route participation is not in nflverse play-by-play", "pbp"), "evidence_tier": "unavailable"},
                "coverage_route_access": {**_blocked("no player-route coverage assignment is on the play-by-play", "pbp"),
                                          "evidence_tier": "unavailable", "charting": "unavailable"}}
    routes = sit.get("routes_status") or _blocked("route participation is not in nflverse play-by-play", "pbp")
    coverage = sit.get("coverage_status") or _blocked("no player-route coverage assignment is on the play-by-play", "pbp")
    if isinstance(routes, dict):
        routes = {**routes, "evidence_tier": routes.get("evidence_tier") or "unavailable"}
    if isinstance(coverage, dict):
        coverage = {**coverage, "evidence_tier": "unavailable" if coverage.get("status") != "OK" else coverage.get("evidence_tier") or "measured",
                    "charting": "unavailable",
                    "evidence_note": "No verified player-route coverage assignment is in this extract. Depth-chart names are not an assignment."}
    return {
        "red_zone": _ratio(sit.get("red_zone_targets"), sit.get("team_red_zone_targets"), "pbp yardline_100 <= 20"),
        "goal_line": {"targets": _ratio(sit.get("goal_line_targets"), sit.get("team_goal_line_targets"), "pbp yardline_100 <= 5"),
                      "carries": _ratio(sit.get("goal_line_carries"), sit.get("team_goal_line_carries"), "pbp yardline_100 <= 5"),
                      "definition": "yardline_100 <= 5"},
        "third_down": _ratio(sit.get("third_down_targets"), sit.get("team_third_down_targets"), "pbp third_down_converted + third_down_failed > 0"),
        "checkdown": _ratio(sit.get("checkdown_targets"), sit.get("third_down_targets_with_air"),
                            f"third-down targets with air_yards < {CHECKDOWN_AIR_LT:g}"),
        "pressure_targets": {
            **_ratio(sit.get("pressure_targets"), sit.get("team_pressure_targets"), "target on a sack or qb_hit play"),
            "evidence_tier": "inferred",
            "charting": "unavailable",
            "evidence_note": "A sack or qb_hit on the target play is a result proxy. It is not charted decision-time pressure.",
        },
        "opponent_quality": ({"status": "OK", "entering_pass_yards_allowed_per_game": _r(sit.get("opponent_pass_yards_allowed_entering"), 1),
                              "games": sit.get("opponent_quality_games"),
                              "definition": "mean of the opponent's prior-week pass yards allowed per game, weeks strictly before each of his games"}
                             if sit.get("opponent_pass_yards_allowed_entering") is not None else
                             _blocked("no prior opponent pass-yards sample", "pbp")),
        "routes": routes if isinstance(routes, dict) else _blocked(str(routes), "pbp"),
        "route_participation": routes if isinstance(routes, dict) else _blocked(str(routes), "pbp"),
        "coverage_route_access": coverage if isinstance(coverage, dict) else _blocked(str(coverage), "pbp"),
        "season_targets": sit.get("targets"), "season_carries": sit.get("carries"), "season_games": sit.get("games"),
    }


def _team_attempts(produced: dict, margin):
    """Own pass and rush attempts per game, times the script multipliers only when a margin is present."""
    passes = produced.get("pass_att_pg") if produced else None
    rushes = produced.get("rush_att_pg") if produced else None
    if passes is None and rushes is None:
        return None, None, {"status": "BLOCKED", "reason": "team pass and rush attempts per game are missing; 0.55 was not used",
                            "model": "dashboard.opportunity.script_multipliers"}
    script = {"status": "NOT_PROVIDED", "model": "dashboard.opportunity.script_multipliers",
              "reason": "no implied margin; the team's own attempt rates were used and no script multiplier was applied"}
    pmul = rmul = None
    if margin is not None:
        pmul, rmul = O.script_multipliers(margin)
        script = {"status": "APPLIED", "model": "dashboard.opportunity.script_multipliers", "implied_margin": _r(margin, 2),
                  "pass_multiplier": _r(pmul, 4), "rush_multiplier": _r(rmul, 4)}
        if passes is not None:
            passes = passes * pmul
        if rushes is not None:
            rushes = rushes * rmul
    return passes, rushes, script


def assemble(spec: dict, *, n: int = 2000, seed: int = 89) -> dict:
    """Build the board from an explicit spec. `pools` may hold numpy arrays and are not copied into the result."""
    game_id = spec.get("game_id")
    home, away = spec.get("home"), spec.get("away")
    spread = spec.get("home_spread")
    pools = spec.get("pools")
    situational = spec.get("situational") or {}
    sit_meta = situational.get("_meta") or {}
    players_out = []
    invoked = {"simulate_receiver": False, "simulate_rusher": False, "def_factor": False, "script": False,
               "teammate_out": False, "qfactor": False, "receiver_roles": False, "opportunity_label": False}
    teams_out = []
    for abbr, team in (spec.get("teams") or {}).items():
        opponent = team.get("opponent")
        if spread is None or home is None:
            margin = None
        else:
            margin = -spread if abbr == home else spread
        passes, rushes, script = _team_attempts(team.get("produced") or {}, margin)
        if script["status"] == "APPLIED":
            invoked["script"] = True
        by_game = team.get("by_game") or []
        weeks_targets = None
        weeks_carries = None
        if by_game and any("wr_targets" in g or "carries" in g for g in by_game):
            weeks_targets = {g.get("week"): (g.get("wr_targets") or 0) + (g.get("te_targets") or 0) + (g.get("rb_targets") or 0) for g in by_game}
            weeks_carries = {g.get("week"): g.get("carries") or 0 for g in by_game}
        official = (team.get("injuries") or {}).get("official_report")
        espn = (team.get("injuries") or {}).get("espn_live")
        people = _person_records(team)
        avail_by = {}
        out_ids = set()
        q_state = {}
        for person in people:
            avail = availability(person["player"], official, espn)
            avail_by[person["player_id"] or person["player"]] = avail
            if avail["state"] == "out":
                out_ids.add(person["player_id"])
            q_state[person["player_id"]] = avail["state"]
        rec_rows = [p["receiving"] for p in people if p["receiving"]]
        rush_rows = [p["rushing"] for p in people if p["rushing"]]
        allocated_rec = {b["row"].get("player_id"): b for b in allocate_receiving(rec_rows, weeks_targets, out_ids, q_state)}
        team_carries = None
        if weeks_carries:
            team_carries = float(sum(weeks_carries.values()))
        allocated_rush = {b["row"].get("player_id"): b for b in allocate_rushing(rush_rows, weeks_carries, out_ids, q_state, team_carries)}
        if any(b["bump"] for b in list(allocated_rec.values()) + list(allocated_rush.values())):
            invoked["teammate_out"] = True
        if any(b.get("q_factor") for b in list(allocated_rec.values()) + list(allocated_rush.values())):
            invoked["qfactor"] = True
        snap_map = team.get("snap_share") or {}
        snap_for_roles = {}
        for person, value in snap_map.items():
            snap_for_roles[person] = value
            for key in aliases(person):
                snap_for_roles.setdefault(key, value)
        for person in people:
            found = _snap_for(person["player"], snap_map)
            if found.get("matched"):
                snap_for_roles[person["player"]] = found["offense_snap_share"]
        role_view = X.receiver_roles({"receivers": rec_rows, "rushers": rush_rows}, snap_for_roles, {})
        invoked["receiver_roles"] = True
        extras_by = {}
        for row in role_view["receivers"] + role_view["rushers"]:
            extras_by[row.get("player_id") or row.get("player")] = row
            if row.get("opportunity"):
                invoked["opportunity_label"] = True
        recent = _last_two(by_game)
        defense = team.get("defense_allowed") or {}
        sit_team = situational.get(abbr) or {}
        board_players = []
        for person in people:
            pid = person["player_id"]
            avail = avail_by[pid or person["player"]]
            snap = _snap_for(person["player"], snap_map)
            depth = _depth_for(person["player"], team.get("depth_chart") or {})
            sit = dict(sit_team.get(pid) or {})
            sit.setdefault("routes_status", sit_meta.get("routes"))
            sit.setdefault("coverage_status", sit_meta.get("coverage"))
            rec_alloc = allocated_rec.get(pid)
            rush_alloc = allocated_rush.get(pid)
            receiving = rushing = None
            if person["receiving"] and avail["state"] != "out":
                if rec_alloc is None:
                    receiving = {"volume": {"status": "BLOCKED", "reason": f"under {MIN_TARGETS} targets in the window; dashboard.opportunity does not project this role",
                                            "model": "dashboard.opportunity inclusion"}}
                else:
                    receiving = project_receiving(game_id, person["receiving"], rec_alloc["share_used"], team_attempts=passes, margin=margin,
                                                  pools=pools, defense=defense, n=n, seed_base=seed)
                    if receiving["receptions"]["status"] != "BLOCKED":
                        invoked["simulate_receiver"] = True
                    if (receiving["efficiency"]["catch_rate"]["matchup"]["status"] == "APPLIED" or
                            receiving["efficiency"]["yards_per_catch"]["matchup"]["status"] == "APPLIED"):
                        invoked["def_factor"] = True
            elif person["receiving"]:
                receiving = {"volume": {"status": "BLOCKED", "reason": "ruled out, doubtful, injured reserve or suspended", "model": None},
                             "receptions": {"status": "BLOCKED", "reason": "availability"}, "receiving_yards": {"status": "BLOCKED", "reason": "availability"}}
            if person["rushing"] and person["rushing"].get("pos") == "RB" and avail["state"] != "out":
                if rush_alloc is None:
                    rushing = {"volume": {"status": "BLOCKED", "reason": f"under {MIN_CARRIES} carries or not an RB; the rush engine was not applied",
                                          "model": "dashboard.opportunity inclusion"}}
                else:
                    rushing = project_rushing(game_id, person["rushing"], rush_alloc["share_used"], team_carries=rushes, pools=pools,
                                              defense=defense, n=n, seed_base=seed)
                    if rushing["rushing_yards"]["status"] != "BLOCKED":
                        invoked["simulate_rusher"] = True
                    if rushing["efficiency"]["yards_per_carry"]["matchup"]["status"] == "APPLIED":
                        invoked["def_factor"] = True
            elif person["rushing"] and person["rushing"].get("pos") == "RB":
                rushing = {"volume": {"status": "BLOCKED", "reason": "ruled out, doubtful, injured reserve or suspended"},
                           "rush_attempts": {"status": "BLOCKED", "reason": "availability"},
                           "rushing_yards": {"status": "BLOCKED", "reason": "availability"}}
            elif person["rushing"]:
                rushing = {"volume": {"status": "BLOCKED", "reason": "dashboard.opportunity rush engine is for RB carries; this player's carries stay descriptive",
                                      "model": "dashboard.opportunity.simulate_rusher"},
                           "descriptive_carries": person["rushing"].get("carries"), "descriptive_games": person["rushing"].get("games")}
            passing = {"status": "BLOCKED", "model": None,
                       "reason": "no passing distribution engine was executed",
                       "models_not_invoked": [m[0] for m in NOT_INVOKED],
                       "descriptive_attempts_per_game": _r((person["passing"] or {}).get("attempts", 0) / (person["passing"] or {}).get("games"), 2)
                       if person["passing"] and person["passing"].get("games") else None}
            both_yards = None
            joint = {"status": "BLOCKED", "reason": "rush and receiving were not both drawn; a missing side was not treated as zero"}
            if receiving and rushing and receiving.get("receiving_yards", {}).get("mean") is not None and rushing.get("rushing_yards", {}).get("mean") is not None:
                both_yards = _r(receiving["receiving_yards"]["mean"] + rushing["rushing_yards"]["mean"], 1)
                joint = {"status": "DOWNGRADED", "mean_sum_of_independent_engines": both_yards,
                         "distribution": {"status": "BLOCKED", "reason": "simulate_receiver and simulate_rusher are separate draws; no joint engine was executed"}}
            td = {"status": "VOLUME_ONLY", "historical_touchdowns": (person["receiving"] or person["rushing"] or {}).get("td"),
                  "historical_games": (person["receiving"] or person["rushing"] or {}).get("games"),
                  "red_zone_targets": (person["receiving"] or {}).get("red_zone_targets"),
                  "red_zone_carries": (person["rushing"] or {}).get("red_zone_carries"),
                  "probability": {"status": "BLOCKED", "reason": "no player TD distribution engine was executed",
                                  "models_not_invoked": [m[0] for m in NOT_INVOKED]}}
            window_row = person["receiving"] or person["rushing"] or person["passing"] or {}
            log = window_row.get("log") or []
            inactive = bool(recent) and bool(log) and not any(x.get("week") in recent for x in log)
            alloc = rec_alloc or rush_alloc or {}
            person_view = person["receiving"] or person["rushing"] or {}
            person_view = dict(person_view)
            person_view["_depth"] = depth
            tags = role_tags(person_view, sit, extras_by.get(pid) or extras_by.get(person["player"]),
                             (extras_by.get(pid) or extras_by.get(person["player"]) or {}).get("opportunity"))
            warnings = _warnings(person_view, avail, snap, alloc.get("how"), alloc.get("last3"), alloc.get("blended"), sit, inactive)
            if alloc.get("q_factor"):
                warnings.append({"warning": "limited_snap", "detail": f"questionable snap factor {alloc['q_factor']:.0%} from {QUESTIONABLE_SNAP_SOURCE}"})
            elif avail["state"] == "questionable" and not alloc.get("q_factor"):
                warnings.append({"warning": "limited_snap", "detail": "questionable, and this position has no fitted snap factor, so volume was not scaled"})
            usage = _usage_block(person, sit, snap, depth)
            trend_stat = "targets" if person["receiving"] else ("carries" if person["rushing"] else "att")
            trends = {"window_games": window_row.get("games"), "window_is_full_season": team.get("season_games_played") in (None, team.get("window_games")),
                      "season_games_played": team.get("season_games_played"),
                      "recent": _recent(log, trend_stat),
                      "home_away": _site_splits(log, by_game, trend_stat),
                      "opponent_quality": _situational_block(sit).get("opponent_quality"),
                      "full_season": ({"status": "OK", "targets": sit.get("targets"), "carries": sit.get("carries"), "games": sit.get("games"),
                                       "source": "pbp weeks before this game, which can be wider than the packet window"}
                                      if sit.get("targets") is not None or sit.get("carries") is not None else
                                      _blocked("full-season counts were not measured; the packet window was not relabeled as a full season", "pbp"))}
            if team.get("season_games_played") and team.get("window_games") and team["season_games_played"] > team["window_games"]:
                trends["full_season_note"] = (f"packet window is {team['window_games']} games; the team has {team['season_games_played']} scored games before this week. "
                                              "Projection shares use the window, not a silent full-season average.")
            board_players.append({
                "player": person["player"], "player_id": pid, "pos": person["pos"], "team": abbr,
                "projection_ready": False,
                "availability": avail, "depth_chart": depth, "snaps": snap,
                "usage": usage, "situational": _situational_block(sit), "trends": trends,
                "role_tags": tags, "warnings": warnings,
                "share": {"receiving": _share_view(rec_alloc), "rushing": _share_view(rush_alloc)},
                "projections": {"receiving": receiving, "rushing": rushing, "passing": passing,
                                "rush_plus_receiving": joint, "td_opportunity": td},
            })
        teams_out.append({"team": abbr, "opponent": opponent, "site": team.get("site"),
                          "script": script, "team_pass_attempts": _r(passes, 2), "team_rush_attempts": _r(rushes, 2),
                          "separate_models": {"pregame.packet.player_baselines": team.get("baselines")},
                          "players": board_players})
        players_out.extend(board_players)
    models = _models(invoked, pools)
    return {"schema": SCHEMA, "projection_ready": False, "research_only": True, "game_id": game_id,
            "season": spec.get("season"), "week": spec.get("week"), "home": home, "away": away,
            "as_of": spec.get("as_of"), "home_spread": spread,
            "models": models, "blocked_everywhere": _global_blocks(sit_meta),
            "teams": teams_out, "player_count": len(players_out)}


def _share_view(alloc) -> dict | None:
    if not alloc:
        return None
    return {"share_used": _r(alloc.get("share_used"), 3), "bump": _r(alloc.get("bump"), 3), "blend": alloc.get("how"),
            "last3_share": _r(alloc.get("last3"), 3), "questionable_factor": alloc.get("q_factor"),
            "questionable_source": alloc.get("q_source"), "unassigned_share": _r(alloc.get("unassigned"), 3),
            "scale": _r(alloc.get("scale"), 3), "models": ["dashboard.opportunity teammate-out constants", QUESTIONABLE_SNAP_SOURCE]}


def _usage_block(person, sit, snap, depth) -> dict:
    rec, rush = person.get("receiving") or {}, person.get("rushing") or {}
    passing = person.get("passing") or {}
    touches = None
    if rec and rush and rec.get("receptions") is not None and rush.get("carries") is not None:
        touches = {"status": "OK", "value": (rec.get("receptions") or 0) + (rush.get("carries") or 0),
                   "definition": "receptions plus designed carries", "source": "pregame.metrics.offense_players"}
    elif rec and not rush:
        touches = _blocked("carries are not on the rusher table for this player; receptions were not treated as his touches", "pregame.metrics.offense_players")
    elif rush and not rec:
        touches = {"status": "OK", "value": rush.get("carries"), "definition": "designed carries; no receiver row", "source": "pregame.metrics.offense_players"}
    return {
        "depth_chart": depth, "snaps": snap,
        "targets": {"status": "OK", "count": rec.get("targets"), "games": rec.get("games"),
                    "share": _r(rec.get("target_share"), 3),
                    "denominator": "team targets in the packet window; share is the stored ratio from offense_players",
                    "source": "pregame.metrics.offense_players"} if rec else _blocked("no receiver row", "pregame.metrics.offense_players"),
        "target_share": {"status": "OK" if rec.get("target_share") is not None else "BLOCKED", "value": _r(rec.get("target_share"), 3),
                         "source": "pregame.metrics.offense_players"} if rec else _blocked("no receiver row", "pregame.metrics.offense_players"),
        "target_depth": {"status": "OK" if rec.get("avg_depth_of_target") is not None else "BLOCKED",
                         "avg_depth_of_target": _r(rec.get("avg_depth_of_target"), 2),
                         "air_yards_share": _r(rec.get("air_yards_share"), 3),
                         "denominator": "targets in the packet window", "source": "pregame.metrics.offense_players"} if rec else _blocked("no receiver row", "pregame.metrics.offense_players"),
        "carries": {"status": "OK", "value": rush.get("carries"), "share": _r(rush.get("carry_share"), 3),
                    "source": "pregame.metrics.offense_players"} if rush else _blocked("no rusher row; carries were not filled with zero", "pregame.metrics.offense_players"),
        "touches": touches,
        "routes": _blocked("route counts are not on the play-by-play or the packet", "pbp"),
        "route_participation": _blocked("route participation is not on the play-by-play or the packet", "pbp"),
        "passing_volume": {"attempts": passing.get("attempts"), "games": passing.get("games"), "sacks": passing.get("sacks"),
                           "pressure_rate_faced": _r(passing.get("pressure_rate_faced"), 3),
                           "source": "pregame.metrics.offense_players"} if passing else _blocked("no quarterback row", "pregame.metrics.offense_players"),
    }


def _recent(log, key) -> dict:
    if not log:
        return _blocked("no game log", "pregame.metrics.offense_players")
    vals = [x.get(key, 0) or 0 for x in log]
    last = vals[-3:]
    return {"status": "OK", "source": "pregame.metrics.offense_players log", "stat": key,
            "window_per_game": _r(sum(vals) / len(vals), 2), "games": len(vals),
            "last3_per_game": _r(sum(last) / len(last), 2), "last3_games": len(last)}


def _models(invoked, pools) -> list[dict]:
    rows = [
        {"id": "pregame.metrics.offense_players", "invoked": True, "role": "targets, carries, depth of target, red-zone counts, game logs"},
        {"id": "pregame.packet.snap_shares", "invoked": True, "role": "offensive snap share over the packet window"},
        {"id": "pregame.packet.depth_chart", "invoked": True, "role": "starter and second-string labels"},
        {"id": "pregame.packet.injuries_for", "invoked": True, "role": "official report and ESPN availability"},
        {"id": "dashboard.opportunity._volume", "invoked": True, "role": "gamma-Poisson target and carry draws, including the fitted volume correction"},
        {"id": "dashboard.opportunity.simulate_receiver", "invoked": invoked["simulate_receiver"], "role": "reception and receiving-yard draws"},
        {"id": "dashboard.opportunity.simulate_rusher", "invoked": invoked["simulate_rusher"], "role": "carry and rushing-yard draws"},
        {"id": "dashboard.opportunity.shrink", "invoked": bool(pools), "role": "catch rate, yards per catch and yards per carry shrunk toward the league"},
        {"id": "dashboard.opportunity.def_factor", "invoked": invoked["def_factor"], "role": "positional yards and catch rate versus this defense"},
        {"id": "dashboard.opportunity.script_multipliers", "invoked": invoked["script"], "role": "pass and rush attempt multipliers from the implied margin"},
        {"id": "dashboard.opportunity.teammate_out", "invoked": invoked["teammate_out"], "role": "OUT_TOP_SAME, OUT_REST_SAME, OUT_OTHER_GROUP, OUT_TOP_RB, OUT_REST_RB"},
        {"id": QUESTIONABLE_SNAP_SOURCE, "invoked": invoked["qfactor"], "role": "questionable snap factors for RB, TE and WR only"},
        {"id": "dashboard.extras.receiver_roles", "invoked": invoked["receiver_roles"], "role": "existing role labels mapped onto the issue tags"},
        {"id": "dashboard.extras.opportunity_label", "invoked": invoked["opportunity_label"], "role": "expanding, shrinking, volume-supported, efficiency-driven"},
        {"id": "pregame.packet.player_baselines", "invoked": False, "role": "attached under separate_models; not an input to the draws"},
    ]
    for mid, role in NOT_INVOKED:
        rows.append({"id": mid, "invoked": False, "role": role})
    return rows


def _global_blocks(meta: dict) -> list[dict]:
    routes = meta.get("routes") or {"status": "BLOCKED", "reason": "nflverse play-by-play has no route or route-participation column"}
    coverage = meta.get("coverage") or {"status": "BLOCKED", "reason": "nflverse play-by-play has no coverage-assignment column; defender totals are not this player's route access"}
    return [{"input": "routes", **routes}, {"input": "coverage_route_access", **coverage}]


def from_packet(packet: dict, *, situational: dict | None = None, pools: dict | None = None, snap_note: dict | None = None,
                n: int = 2000, seed: int = 89) -> dict:
    game = packet["game"]
    home, away = game["home"], game["away"]
    spec = {"game_id": game.get("game_id"), "season": game.get("season"), "week": game.get("week"), "home": home, "away": away,
            "as_of": f"packet generated {packet.get('generated_utc')}; usage is the pregame window, weeks before {game.get('week')}",
            "home_spread": (packet.get("market") or {}).get("home_spread"), "pools": pools, "situational": situational or {},
            "teams": {}}
    for abbr, opponent, site in ((away, home, "away"), (home, away, "home")):
        block = packet["teams"][abbr]
        off = block.get("offense") or {}
        opp = packet["teams"][opponent]
        key = f"{abbr}_offense_vs_{opponent}_defense"
        baselines = ((packet.get("matchup") or {}).get(key) or {}).get("player_baselines")
        freshness = (packet.get("data_freshness") or {}).get(abbr) or {}
        spec["teams"][abbr] = {
            "opponent": opponent, "site": site, "window_games": (off.get("window") or block.get("window") or {}).get("games") or (off.get("produced") or {}).get("games"),
            "season_games_played": freshness.get("games_played"),
            "produced": off.get("produced") or {}, "by_game": off.get("by_game") or [],
            "defense_allowed": (opp.get("defense") or {}).get("allowed") or {},
            "snap_share": off.get("offense_snap_share") or {},
            "depth_chart": block.get("depth_chart") or {"status": "UNAVAILABLE"},
            "injuries": block.get("injuries") or {},
            "players": off.get("players") or {},
            "baselines": baselines, "snap_note": snap_note,
        }
    board = assemble(spec, n=n, seed=seed)
    board["packet_generated_utc"] = packet.get("generated_utc")
    board["packet_status"] = packet.get("status")
    if snap_note:
        board["snap_file"] = snap_note
    return board


def measure_situational(pbp: pd.DataFrame, teams: set[str], before_week: int) -> dict:
    """Third-down, goal-line, pressure-target, home/away and prior opponent pass-yards from play-by-play.

    Routes and coverage assignments are reported blocked when those columns are absent.
    Counts use weeks strictly below `before_week`.
    """
    required = ["posteam", "defteam", "week", "game_id", "play_type", "down", "pass_attempt", "sack", "qb_hit",
                "air_yards", "yardline_100", "receiver_player_id", "rusher_player_id", "third_down_converted",
                "third_down_failed", "home_team", "yards_gained", "complete_pass", "rush_attempt", "qb_scramble"]
    missing = [c for c in required if c not in pbp.columns]
    route_cols = [c for c in pbp.columns if "route" in c.lower()]
    coverage_cols = [c for c in pbp.columns if "coverage" in c.lower()]
    meta = {"routes": _blocked("no route column on this play-by-play; route participation was not imputed from snaps", "pbp")
            if not route_cols else {"status": "OK", "columns": route_cols},
            "coverage": _blocked("no coverage column on this play-by-play; team defender totals were not used as a player route adjustment", "pbp")
            if not coverage_cols else {"status": "OK", "columns": coverage_cols},
            "before_week": before_week}
    if missing:
        return {"_meta": {**meta, "status": "BLOCKED", "reason": f"missing columns: {missing}"}}
    df = pbp[pbp.week < before_week]
    if "season_type" in df.columns:
        df = df[df.season_type.astype(str).isin(["REG", "reg"])]
    if "two_point_attempt" in df.columns:
        df = df[_num(df.two_point_attempt).fillna(0) == 0]
    scr = df[df.play_type.isin(["pass", "run"]) & df.down.notna()].copy()
    sack = _num(scr.sack).fillna(0) == 1
    att = (_num(scr.pass_attempt).fillna(0) == 1) & ~sack
    scr = scr.assign(
        tgt=att & scr.receiver_player_id.notna(),
        carry_f=(_num(scr.rush_attempt).fillna(0) == 1) & (_num(scr.qb_scramble).fillna(0) != 1),
        third_f=(_num(scr.third_down_converted).fillna(0) + _num(scr.third_down_failed).fillna(0)) > 0,
        pressure_f=sack | (_num(scr.qb_hit).fillna(0) == 1),
        air_f=_num(scr.air_yards),
        yl=_num(scr.yardline_100),
        complete_f=_num(scr.complete_pass).fillna(0) == 1,
        yards_f=_num(scr.yards_gained).fillna(0),
    )
    comp = scr[scr.complete_f]
    hist: dict[str, list] = {}
    if len(comp):
        gy = comp.groupby(["defteam", "game_id"], as_index=False).agg(yards=("yards_f", "sum"), week=("week", "min"))
        for row in gy.itertuples():
            hist.setdefault(row.defteam, []).append((int(row.week), float(row.yards)))
    games = scr.groupby(["posteam", "game_id"], as_index=False).agg(week=("week", "min"), opp=("defteam", "first"), home=("home_team", "first"))
    qual = {}
    for row in games.itertuples():
        prior = [y for w, y in hist.get(row.opp, []) if w < int(row.week)]
        qual[(row.posteam, row.game_id)] = (sum(prior) / len(prior)) if prior else None
    out = {"_meta": meta}
    name_col_rec = "receiver_player_name" if "receiver_player_name" in scr.columns else None
    for team in teams:
        sub = scr[scr.posteam == team]
        team_targets = int(sub.tgt.sum())
        team_carries = int(sub.carry_f.sum())
        team_third = int((sub.tgt & sub.third_f).sum())
        team_rz = int((sub.tgt & (sub.yl <= 20)).sum())
        team_gl_t = int((sub.tgt & (sub.yl <= 5)).sum())
        team_gl_c = int((sub.carry_f & (sub.yl <= 5)).sum())
        team_pressure = int((sub.tgt & sub.pressure_f).sum())
        players: dict[str, dict] = {}

        def slot(pid, name):
            if pid is None or pid != pid:
                return None
            pid = str(pid)
            row = players.setdefault(pid, {"player_id": pid, "player": name, "games": set(), "home_games": set(), "away_games": set()})
            if name and not row.get("player"):
                row["player"] = name
            return row

        def ensure(item, keys):
            for key in keys:
                item.setdefault(key, 0)

        target_keys = ("targets", "third_down_targets", "checkdown_targets", "third_down_targets_with_air",
                       "goal_line_targets", "red_zone_targets", "pressure_targets", "home_targets", "away_targets")
        tgt_rows = sub[sub.tgt]
        for row in tgt_rows.itertuples():
            item = slot(row.receiver_player_id, getattr(row, name_col_rec, None) if name_col_rec else None)
            if item is None:
                continue
            ensure(item, target_keys)
            item["targets"] += 1
            item["games"].add(row.game_id)
            home = row.home_team == team
            item["home_targets" if home else "away_targets"] += 1
            item["home_games" if home else "away_games"].add(row.game_id)
            if row.third_f:
                item["third_down_targets"] += 1
                if row.air_f == row.air_f:
                    item["third_down_targets_with_air"] += 1
                    if row.air_f < CHECKDOWN_AIR_LT:
                        item["checkdown_targets"] += 1
            if row.yl == row.yl and row.yl <= 20:
                item["red_zone_targets"] += 1
            if row.yl == row.yl and row.yl <= 5:
                item["goal_line_targets"] += 1
            if row.pressure_f:
                item["pressure_targets"] += 1
        carries = sub[sub.carry_f]
        for row in carries.itertuples():
            item = slot(row.rusher_player_id, getattr(row, "rusher_player_name", None) if "rusher_player_name" in sub.columns else None)
            if item is None:
                continue
            ensure(item, ("carries", "goal_line_carries"))
            item["carries"] += 1
            item["games"].add(row.game_id)
            if row.yl == row.yl and row.yl <= 5:
                item["goal_line_carries"] += 1
        if "passer_player_id" in sub.columns:
            drop = (_num(sub.pass_attempt).fillna(0) == 1) | (_num(sub.sack).fillna(0) == 1) | (_num(sub.qb_scramble).fillna(0) == 1)
            name_col = "passer_player_name" if "passer_player_name" in sub.columns else None
            for row in sub[drop].itertuples():
                item = slot(row.passer_player_id, getattr(row, name_col, None) if name_col else None)
                if item is None:
                    continue
                item["games"].add(row.game_id)
                item["passer_dropbacks"] = item.get("passer_dropbacks", 0) + 1
        for item in players.values():
            vals = [qual[(team, g)] for g in item["games"] if qual.get((team, g)) is not None]
            if vals:
                item["opponent_pass_yards_allowed_entering"] = sum(vals) / len(vals)
                item["opponent_quality_games"] = len(vals)
        clean = {}
        for pid, item in players.items():
            item["games"] = len(item["games"])
            item["home_games"] = len(item["home_games"])
            item["away_games"] = len(item["away_games"])
            item.pop("qual", None)
            item["team_targets"] = team_targets
            item["team_carries"] = team_carries
            item["team_third_down_targets"] = team_third
            item["team_red_zone_targets"] = team_rz
            item["team_goal_line_targets"] = team_gl_t
            item["team_goal_line_carries"] = team_gl_c
            item["team_pressure_targets"] = team_pressure
            clean[pid] = item
        out[team] = clean
    return out


def load_pools(pbp: pd.DataFrame, rosters: pd.DataFrame | None, source: str, before_week: int | None = None) -> dict:
    df = pbp if before_week is None else pbp[pbp.week < before_week]
    if "season_type" in df.columns:
        df = df[df.season_type.astype(str).isin(["REG", "reg"])]
    roster_note = "no roster; league_pools falls back to all catches when a position has fewer than 200 charted catches"
    if rosters is not None and len(rosters):
        use = rosters if before_week is None or "week" not in rosters.columns else rosters[rosters.week < before_week]
        roster_note = f"roster weeks {int(use.week.min())}-{int(use.week.max())}" if "week" in use.columns and len(use) else "roster supplied"
        rosters = use
    raw = O.league_pools(df, rosters)
    raw["source"] = source
    raw["roster_note"] = roster_note
    return raw


def render_markdown(board: dict) -> str:
    lines = [f"# Player board {board.get('game_id')}", "",
             f"Schema `{board.get('schema')}`. projection_ready={board.get('projection_ready')}. Research only.",
             f"As of: {board.get('as_of')}.", ""]
    lines.append("## Models")
    for row in board.get("models") or []:
        flag = "ran" if row.get("invoked") else "not run"
        lines.append(f"- `{row['id']}` — {flag}. {row['role']}")
    lines.append("")
    lines.append("## Blocked for every player")
    for row in board.get("blocked_everywhere") or []:
        lines.append(f"- {row.get('input')}: {row.get('reason')}")
    lines.append("")
    for team in board.get("teams") or []:
        lines.append(f"## {team['team']} offense vs {team.get('opponent')}")
        script = team.get("script") or {}
        lines.append(f"Team pass attempts {team.get('team_pass_attempts')}, rush attempts {team.get('team_rush_attempts')}. Script: {script.get('status')}.")
        lines.append("")
        lines.append("| Player | Pos | Depth | Snap | Targets | Share used | Tags | Receiving | Rushing | Warnings |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        for p in team.get("players") or []:
            rec = (p.get("projections") or {}).get("receiving") or {}
            rush = (p.get("projections") or {}).get("rushing") or {}
            rec_txt = _proj_text(rec.get("receiving_yards"), rec.get("receptions"), "yds", "catches")
            rush_txt = _proj_text(rush.get("rushing_yards"), rush.get("rush_attempts"), "yds", "carries")
            tags = ", ".join(t["tag"] for t in p.get("role_tags") or []) or "—"
            warns = ", ".join(w["warning"] for w in p.get("warnings") or []) or "—"
            share = ((p.get("share") or {}).get("receiving") or {}).get("share_used")
            if share is None:
                share = ((p.get("share") or {}).get("rushing") or {}).get("share_used")
            targets = ((p.get("usage") or {}).get("target_share") or {}).get("value")
            depth = (p.get("depth_chart") or {}).get("status")
            snap = (p.get("snaps") or {}).get("offense_snap_share")
            lines.append(f"| {p.get('player')} | {p.get('pos') or ''} | {depth} | {snap if snap is not None else '—'} | {targets if targets is not None else '—'} | {share if share is not None else '—'} | {tags} | {rec_txt} | {rush_txt} | {warns} |")
        lines.append("")
        lines.append("Target column is the window target share. Receiving and rushing cells are engine means, or BLOCKED with the reason on the JSON row.")
        lines.append("")
    lines.append("Baselines from `pregame.packet.player_baselines` are stored on each team under `separate_models` and are not the numbers above.")
    return "\n".join(lines) + "\n"


def _proj_text(yards, counts, label, count_label) -> str:
    if not yards and not counts:
        return "—"
    if yards and yards.get("status") == "BLOCKED":
        return "BLOCKED"
    if yards and yards.get("mean") is not None:
        mean = counts.get("mean") if counts else None
        extra = f", {mean} {count_label}" if mean is not None else ""
        flag = yards.get("status")
        return f"{yards['mean']} {label} ({flag}){extra}"
    if counts and counts.get("distribution"):
        return f"{counts['distribution'].get('mean')} volume ({counts.get('status')})"
    return counts.get("status") if counts else "—"


def _jsonable(value):
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items() if k != "pools"}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, np.ndarray):
        return None
    return value


def replay(packet_path: Path, *, pbp_path: Path | None = None, roster_path: Path | None = None, snaps_path: Path | None = None,
           out_dir: Path | None = None, n: int = 2000, seed: int = 89) -> dict:
    packet = json.loads(Path(packet_path).read_text())
    game = packet["game"]
    week = int(game["week"])
    teams = {game["away"], game["home"]}
    situational = None
    pools = None
    if pbp_path:
        columns = [c for c in PBP_COLUMNS if c]
        frame = pd.read_parquet(pbp_path, columns=columns)
        situational = measure_situational(frame, teams, week)
        rosters = pd.read_parquet(roster_path) if roster_path else None
        pools = load_pools(frame, rosters, source=str(pbp_path), before_week=week)
    snap_note = None
    if snaps_path and Path(snaps_path).exists():
        snaps = pd.read_parquet(snaps_path, columns=["week"])
        snap_max = int(snaps.week.max()) if len(snaps) else None
        window_weeks = []
        for abbr in teams:
            window_weeks.extend(((packet["teams"][abbr].get("offense") or {}).get("produced") or {}).get("weeks") or [])
        window_max = max(window_weeks) if window_weeks else None
        if snap_max is not None and window_max is not None and snap_max < window_max:
            snap_note = {"status": "BLOCKED", "on_disk_max_week": snap_max, "packet_window_max_week": window_max,
                         "reason": f"on-disk snap counts end at week {snap_max}, before the packet window reaches week {window_max}. "
                                   "Return and week-to-week snap changes after that were not inferred. The packet's stored snap shares are still shown."}
        else:
            snap_note = {"status": "OK", "on_disk_max_week": snap_max}
    board = from_packet(packet, situational=situational, pools=pools, snap_note=snap_note, n=n, seed=seed)
    try:
        board["code_revision"] = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        board["code_revision"] = None
    board["command"] = {"packet": str(packet_path), "pbp": str(pbp_path) if pbp_path else None,
                        "rosters": str(roster_path) if roster_path else None, "snaps": str(snaps_path) if snaps_path else None,
                        "n": n, "seed": seed}
    if pools:
        board["pool_source"] = {"source": pools.get("source"), "roster_note": pools.get("roster_note"),
                                "positions": sorted((pools.get("catch") or {}).keys())}
    if out_dir:
        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "player_board.json").write_text(json.dumps(_jsonable(board), indent=1) + "\n")
        (out / "player_board.md").write_text(render_markdown(board))
    return board


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description="Assemble one game's player opportunity board. Research only.")
    parser.add_argument("--packet", required=True)
    parser.add_argument("--pbp")
    parser.add_argument("--rosters")
    parser.add_argument("--snaps")
    parser.add_argument("--out")
    parser.add_argument("--n", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=89)
    args = parser.parse_args(argv)
    board = replay(Path(args.packet), pbp_path=Path(args.pbp) if args.pbp else None,
                   roster_path=Path(args.rosters) if args.rosters else None,
                   snaps_path=Path(args.snaps) if args.snaps else None,
                   out_dir=Path(args.out) if args.out else None, n=args.n, seed=args.seed)
    print(f"{board['game_id']}: {board['player_count']} players, projection_ready={board['projection_ready']}")


if __name__ == "__main__":
    main()
