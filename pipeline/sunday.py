"""Sunday research slice: one local command, existing engines only.

Composes the packet, the period-engine team bootstrap, the neighbor
cross-check, the opportunity board, and an optional small possession-engine
cross-check. This is not tools/sim_v6.py and it is not the 100,000-trial
pipeline.sim100k gate. projection_ready stays false.

    python -m pipeline.sunday --game 2026_12_DEN_PIT
    python -m pipeline.sunday --slate

A missing packet, spread, total, or as-of play-by-play file is a refusal
(exit 2). A file that contains the target week is a refusal. History that
stops before the prior week is a warning, not a silent pass.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dashboard import gamemodel as GM  # noqa: E402
from dashboard import opportunity as OP  # noqa: E402
from dashboard.build import implied_points, side  # noqa: E402
from dashboard.extras import receiver_roles  # noqa: E402
from pipeline.sim100k import engine_config  # noqa: E402

PBP_DIR = ROOT / "data" / "historical" / "nflverse"
PACKETS = ROOT / "pregame" / "packets"
POOL_COLUMNS = [
    "season_type", "week", "complete_pass", "receiving_yards", "two_point_attempt",
    "pass_attempt", "sack", "receiver_player_id", "rush_attempt", "qb_scramble",
    "rushing_yards", "rusher_player_id",
]
EXIT_REFUSED = 2


def _utc(now: datetime | None = None) -> datetime:
    now = now or datetime.now(timezone.utc)
    return now if now.tzinfo else now.replace(tzinfo=timezone.utc)


def asof_pbp_path(season: int, week: int, root: Path = ROOT) -> Path | None:
    """Newest committed file named for history through the week before this game."""
    files = sorted((root / "data" / "historical" / "nflverse").glob(
        f"pbp_{season}_w1_{week - 1}_pulled_*.parquet"))
    return files[-1] if files else None


def _kickoff(pk: dict) -> datetime | None:
    g = pk.get("game") or {}
    raw = g.get("kickoff_utc") or g.get("kickoff")
    if raw and "T" in str(raw):
        try:
            return datetime.fromisoformat(str(raw).replace("Z", "+00:00")).astimezone(timezone.utc)
        except ValueError:
            return None
    date, hhmm = g.get("date"), g.get("kickoff_et")
    if not date or not hhmm:
        return None
    try:
        from zoneinfo import ZoneInfo
        local = datetime.strptime(f"{date} {hhmm}", "%Y-%m-%d %H:%M").replace(tzinfo=ZoneInfo("America/New_York"))
        return local.astimezone(timezone.utc)
    except ValueError:
        return None


def preflight(pk: dict, *, pbp: Path | None, now: datetime) -> dict:
    """Refuse only inputs that would make the team distribution or the packet unusable."""
    g = pk.get("game") or {}
    reasons = []
    week = g.get("week")
    if not g.get("game_id") or not g.get("home") or not g.get("away") or week is None:
        reasons.append("packet game id, home, away, or week is missing")
    imp = implied_points(pk)
    if imp is None:
        reasons.append("market spread and total are missing; team points and scripts have no anchor")
    path = pbp
    leak = None
    through = None
    if path is None or not path.is_file():
        reasons.append(f"no committed as-of play-by-play pbp_{g.get('season')}_w1_{int(week or 0) - 1}_pulled_*.parquet")
    else:
        weeks = pd.read_parquet(path, columns=["week"])
        through = int(weeks.week.max())
        if week is not None and through >= int(week):
            leak = through
            reasons.append(f"as-of play-by-play max week {through} includes target week {week}")
        elif week is not None and through < int(week) - 1:
            # Still runnable. The manifest records the gap; it is not filled with later weeks.
            pass
    ko = _kickoff(pk)
    mode = "historical_replay" if ko is not None and now >= ko else "research_pregame"
    return {
        "ok": not reasons,
        "reasons": reasons,
        "implied": imp,
        "pbp": str(path) if path else None,
        "pbp_max_week": through,
        "leak_week": leak,
        "mode": mode,
        "kickoff_utc": ko.isoformat() if ko else None,
        "projection_ready": False,
    }


def _period(pbp: Path, home: str, away: str, season: int, week: int, n: int, seed: int) -> dict:
    eng = ROOT / "core" / "period_engine_v0"
    if str(eng) not in sys.path:
        sys.path.insert(0, str(eng))
    from monte_carlo import STATUS, simulate_game
    from reconstruct import as_of_mask, load_pbp, period_table_from_pbp

    table = period_table_from_pbp(load_pbp(pbp))
    asof = table[as_of_mask(table, season, week)]
    if "week" in asof.columns and len(asof) and int(asof.week.max()) >= week:
        raise RuntimeError(f"period as-of mask kept week {int(asof.week.max())}")
    sim = simulate_game(asof, home, away, n=n, seed=seed, sampling="matchup_pair", apply_gr=False)
    fg = sim["summaries"]["fg"]
    return {
        "engine": "core/period_engine_v0/monte_carlo.py simulate_game",
        "label": "period-engine empirical bootstrap. Not sim_v6. Bias is unimplemented.",
        "n": sim["n"],
        "seed": sim["seed"],
        "sampling": "matchup_pair",
        "asof_rows": int(len(asof)),
        "status": sim["status"],
        "model_status": {"monte_carlo": STATUS.monte_carlo, "bias": STATUS.bias, "game_randomness": STATUS.game_randomness},
        "final": {k: fg[k] for k in ("home_mean", "away_mean", "home_median", "away_median", "total_mean", "total_median", "margin_home_mean")},
        "not_sim_v6": True,
        "projection_ready": False,
    }


def _neighbors(home: str, away: str, implied: dict, home_spread: float, total: float) -> dict:
    home_imp, away_imp = float(implied[home]), float(implied[away])
    nb = GM.neighbors(home_imp, away_imp)
    hp, ap = GM.period_points(nb, "")
    margin = hp - ap
    favorite = home if home_imp >= away_imp else away
    # Margin from the favorite's side so the three labels do not depend on home/away.
    fav_margin = margin if favorite == home else -margin
    bands = {
        "favorite_controls": fav_margin >= 8,
        "competitive": np.abs(fav_margin) <= 7,
        "underdog_chases": fav_margin <= -8,
    }
    total = len(nb)
    scripts = []
    centers = {"favorite_controls": 8.0, "competitive": 0.0, "underdog_chases": -8.0}
    for name, mask in bands.items():
        count = int(mask.sum())
        p_pass, p_rush = OP.script_multipliers(centers[name] if favorite == home else -centers[name])
        # script_multipliers expects the offense's implied margin. Store both teams' multipliers at the band center.
        scripts.append({
            "name": name,
            "label": "empirical share of dashboard.gamemodel neighbors. Not a fitted script model.",
            "probability": round(count / total, 4) if total else None,
            "neighbors": count,
            "favorite": favorite,
            "favorite_margin_center": centers[name],
            "home_pass_multiplier": round(OP.script_multipliers(centers[name] if favorite == home else -centers[name])[0], 4),
            "home_rush_multiplier": round(OP.script_multipliers(centers[name] if favorite == home else -centers[name])[1], 4),
            "away_pass_multiplier": round(OP.script_multipliers(-centers[name] if favorite == home else centers[name])[0], 4),
            "away_rush_multiplier": round(OP.script_multipliers(-centers[name] if favorite == home else centers[name])[1], 4),
        })
        del p_pass, p_rush
    spread = GM.outcome(nb, "spread", home, float(home_spread), home, away)
    over = GM.outcome(nb, "total", "Over", float(total), home, away)
    probs = [s["probability"] or 0 for s in scripts]
    return {
        "engine": "dashboard/gamemodel.py neighbors",
        "k": int(len(nb)),
        "implied": {home: home_imp, away: away_imp},
        "scripts": scripts,
        "script_probability_sum": round(sum(probs), 4),
        "home_spread_result": {"p_win": spread[0], "p_push": spread[1], "p_lose": spread[2]} if spread else None,
        "total_over_result": {"p_win": over[0], "p_push": over[1], "p_lose": over[2]} if over else None,
        "not_sim_v6": True,
        "projection_ready": False,
    }


def _slim_player(row: dict, kind: str) -> dict:
    keep = ("player", "pos", "status", "targets_mean", "receptions_mean", "carries_mean", "yards_mean", "yards_median")
    out = {k: row[k] for k in keep if k in row}
    out["kind"] = kind
    return out


def _board(pk: dict, pbp: Path, week: int, implied: dict, margin_shift: float, seed: int) -> dict:
    cols = pd.read_parquet(pbp, columns=POOL_COLUMNS)
    cols = cols[(cols.season_type == "REG") & (cols.week < week)]
    pools = OP.league_pools(cols, None)
    g = pk["game"]
    home, away = g["home"], g["away"]
    shifted = {
        home: implied[home] + margin_shift / 2,
        away: implied[away] - margin_shift / 2,
    }
    sides = {}
    for off, dfn in ((away, home), (home, away)):
        players = pk["teams"][off]["offense"]["players"]
        roles = receiver_roles(players, pk["teams"][off]["offense"].get("offense_snap_share") or {}, {})
        qbs = players.get("quarterbacks") or [{}]
        built = side(pk, off, dfn, {"roles": roles, "qb": qbs[0] if qbs else {}, "offense_injuries": [], "returning": {}})
        raw = OP.board_side(built, g, shifted, pools, set(), seed=seed + sum(map(ord, off)))
        sides[off] = {
            "team_pass_attempts": raw.get("team_pass_attempts"),
            "team_rush_attempts": raw.get("team_rush_attempts"),
            "implied_margin": raw.get("implied_margin"),
            "script_pass_multiplier": raw.get("script_pass_multiplier"),
            "receivers": [_slim_player(r, "receiver") for r in raw.get("receivers") or []],
            "rushers": [_slim_player(r, "rusher") for r in raw.get("rushers") or []],
        }
    return {
        "engine": "dashboard/opportunity.py board_side",
        "pool": "as-of regular-season plays in the committed pbp, week < target. No roster file, so position pools fall back together when ids are missing.",
        "n_sims_per_player": OP.N_SIMS,
        "sides": sides,
        "not_sim_v6": True,
        "projection_ready": False,
    }


def _possession(game_id: str, pbp: Path, n: int, seed: int) -> dict:
    if n <= 0:
        return {"status": "NOT_RUN", "reason": "possession-n is 0", "not_sim100k": True, "not_sim_v6": True}
    ec = engine_config(game_id, ROOT)
    if ec["status"] != "OK":
        return {"status": ec["status"], "reason": ec.get("reason"), "not_sim100k": True, "not_sim_v6": True, "projection_ready": False}
    eng = ROOT / "core" / "possession_engine_v0"
    if str(eng) not in sys.path:
        sys.path.insert(0, str(eng))
    from simulate import simulate_games
    out = simulate_games(ec["cfg"], pbp_path=str(pbp), n=n, seed=seed)
    arrays = out.get("arrays") or {}
    def mean(key):
        arr = arrays.get(key)
        return None if arr is None else round(float(np.mean(arr)), 2)
    return {
        "engine": "core/possession_engine_v0/simulate.py simulate_games",
        "label": "Direct call. Not pipeline.sim100k, not the 100000-trial gate, not sim_v6.",
        "gate": "BYPASSED_DIRECT_CALL",
        "config": str(ec["path"].relative_to(ROOT)) if ec.get("path") else None,
        "status": out.get("status"),
        "n_completed": out.get("n_completed"),
        "n_requested": out.get("n_requested"),
        "seed": out.get("seed"),
        "final": {"home_mean": mean("fg_home"), "away_mean": mean("fg_away")},
        "not_sim100k": True,
        "not_sim_v6": True,
        "projection_ready": False,
    }


def _market(pk: dict, period: dict, neighbors: dict) -> dict:
    books = ((pk.get("books") or {}).get("markets")) or {}
    market = pk.get("market") or {}
    return {
        "packet_home_spread": market.get("home_spread"),
        "packet_total": market.get("total"),
        "book_spread": (books.get("spread") or {}).get("reference"),
        "book_total": (books.get("total") or {}).get("reference"),
        "period_final": period.get("final"),
        "neighbor_spread": neighbors.get("home_spread_result"),
        "neighbor_total_over": neighbors.get("total_over_result"),
        "note": "Comparison only. No pick and no stake.",
    }


def _warnings(gate: dict, period: dict, pools_note: str) -> list[str]:
    out = [
        "projection_ready is false. Research only.",
        "This run is not the sim_v6 Monte Carlo / calibrated Bias / Game Randomness contract. tools/sim_v6.py is absent.",
        f"Period-engine bias status: {period['model_status']['bias']}.",
        "Game Randomness was not applied on the period-engine call. Its implemented shock is unfitted and is not sim_v6.",
        pools_note,
        "dashboard.build was not used: pregame/.cache is not required here, and the full site board needs that cache.",
    ]
    if gate["mode"] == "historical_replay":
        out.append("Kickoff is already past. This manifest is a historical replay, not a pregame forecast.")
    if gate.get("pbp_max_week") is not None:
        out.append(f"Play-by-play data-through week is {gate['pbp_max_week']}.")
    return out


def run_game(game_id: str, *, n: int, possession_n: int, out_dir: Path, pbp: Path | None, now: datetime) -> dict:
    path = PACKETS / game_id / "packet.json"
    if not path.is_file():
        return {"game_id": game_id, "status": "REFUSED", "reasons": [f"missing {path}"], "projection_ready": False}
    pk = json.loads(path.read_text())
    g = pk["game"]
    week, season = int(g["week"]), int(g["season"])
    chosen = pbp or asof_pbp_path(season, week)
    gate = preflight(pk, pbp=chosen, now=now)
    if not gate["ok"]:
        return {"game_id": game_id, "status": "REFUSED", "preflight": gate, "projection_ready": False}
    seed = 20261128 + week
    period = _period(Path(gate["pbp"]), g["home"], g["away"], season, week, n, seed)
    market = pk.get("market") or {}
    home, away = g["home"], g["away"]
    spread = market.get("home_spread")
    total = market.get("total")
    if spread is None:
        spread = gate["implied"][away] - gate["implied"][home]
    if total is None:
        total = gate["implied"][home] + gate["implied"][away]
    neighbors = _neighbors(home, away, gate["implied"], spread, total)
    # Market script is the packet implied margin. The other two boards shift that margin by the band center.
    boards = {}
    for script in neighbors["scripts"]:
        center = script["favorite_margin_center"]
        favorite_is_home = script["favorite"] == g["home"]
        shift = center if favorite_is_home else -center
        boards[script["name"]] = _board(pk, Path(gate["pbp"]), week, gate["implied"], shift - (gate["implied"][g["home"]] - gate["implied"][g["away"]]), seed)
    possession = _possession(game_id, Path(gate["pbp"]), possession_n, seed)
    manifest = {
        "schema": "sunday-research-slice/1",
        "game_id": game_id,
        "ran_utc": now.isoformat(timespec="seconds"),
        "packet": str(path.relative_to(ROOT)),
        "packet_generated_utc": pk.get("generated_utc"),
        "mode": gate["mode"],
        "status": "OK",
        "projection_ready": False,
        "research_only": True,
        "not_sim_v6": True,
        "not_sim100k": True,
        "preflight": {k: v for k, v in gate.items() if k != "implied"},
        "primary_team_engine": period,
        "cross_check_neighbors": neighbors,
        "cross_check_possession": possession,
        "player_boards_by_script": boards,
        "market": _market(pk, period, neighbors),
        "warnings": _warnings(gate, period, boards["competitive"]["pool"]),
    }
    dest = out_dir / game_id
    dest.mkdir(parents=True, exist_ok=True)
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    file = dest / f"manifest_{stamp}.json"
    file.write_text(json.dumps(manifest, indent=1) + "\n")
    manifest["manifest_path"] = str(file)
    return manifest


def slate_ids() -> list[str]:
    latest = json.loads((PACKETS / "latest.json").read_text())
    return [g["game_id"] for g in latest.get("games") or []]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--game", help="one game id, for example 2026_12_DEN_PIT")
    ap.add_argument("--slate", action="store_true", help="every game in pregame/packets/latest.json")
    ap.add_argument("--n", type=int, default=2000, help="period-engine trials. Not 100000 and not sim_v6.")
    ap.add_argument("--possession-n", type=int, default=200, help="possession-engine cross-check trials. 0 skips it. Not the sim100k gate.")
    ap.add_argument("--out", type=Path, default=ROOT / "runs" / "sunday")
    ap.add_argument("--pbp", type=Path, help="override the committed as-of parquet (still refused if it contains the target week)")
    ap.add_argument("--now", help="UTC ISO timestamp for the replay label")
    a = ap.parse_args(argv)
    if bool(a.game) == bool(a.slate):
        print("sunday: pass exactly one of --game or --slate")
        return EXIT_REFUSED
    now = _utc(datetime.fromisoformat(a.now.replace("Z", "+00:00")) if a.now else None)
    ids = slate_ids() if a.slate else [a.game]
    refused = 0
    for gid in ids:
        result = run_game(gid, n=a.n, possession_n=a.possession_n, out_dir=a.out, pbp=a.pbp, now=now)
        if result.get("status") == "REFUSED":
            refused += 1
            print(f"REFUSED {gid}: {'; '.join(result.get('reasons') or result.get('preflight', {}).get('reasons') or [])}")
        else:
            final = result["primary_team_engine"]["final"]
            print(f"OK {gid} {result['mode']} home {final['home_mean']} away {final['away_mean']} -> {result['manifest_path']}")
    if refused:
        print(f"sunday: {refused} of {len(ids)} refused")
        return EXIT_REFUSED
    return 0


if __name__ == "__main__":
    sys.exit(main())
