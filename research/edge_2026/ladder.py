"""Price NFL yardage alt ladders with a historical zero-inflated gamma model.

The model is research-only. It uses 2022 and 2024 nflverse play-by-play to fit
shape parameters, and strictly pregame player history for each prediction.
"""
from __future__ import annotations

import json
import math
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import gamma

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
NV = ROOT / "data" / "historical" / "nflverse"
DIRECT_LINES = ROOT / "pregame" / "direct_lines"
GRADE_CSV = ROOT / "data" / "odds_history" / "alt_ladders_wk8_9" / "backtest" / "graded_rungs.csv"
MIN_GROUP_N = 30
BOOT_REPS = 5000
BOOT_SEED = 20261119
POSITION_SET = {"QB", "RB", "WR", "TE"}
MARKET_FILES = {
    2022: "pbp_2022.parquet",
    2024: "play_by_play_2024.parquet",
    2026: "pbp_2026_w1_9_pulled_20261112T1116ET.parquet",
}


def norm_name(name: str) -> str:
    name = (name or "").lower().replace("-", " ")
    name = re.sub(r"[^a-z ]", "", name)
    return " ".join(part for part in name.split() if part not in {"jr", "sr", "ii", "iii", "iv", "v"})


def _write_json(payload: dict[str, Any], path: Path, compact_arrays: set[str]) -> None:
    """Keep per-rung arrays one JSON object per line for compact, reviewable diffs."""
    lines = ["{"]
    items = list(payload.items())
    for index, (key, value) in enumerate(items):
        comma = "," if index < len(items) - 1 else ""
        if key in compact_arrays and isinstance(value, list):
            lines.append(f" {json.dumps(key)}: [")
            for row_index, row in enumerate(value):
                row_comma = "," if row_index < len(value) - 1 else ""
                lines.append("  " + json.dumps(row, separators=(",", ":"), ensure_ascii=False, allow_nan=False) + row_comma)
            lines.append(" ]" + comma)
        else:
            encoded = json.dumps(value, indent=1, ensure_ascii=False, allow_nan=False).replace("\n", "\n ")
            lines.append(f" {json.dumps(key)}: {encoded}{comma}")
    lines.append("}")
    path.write_text("\n".join(lines) + "\n")


def implied(american: float) -> float:
    value = float(american)
    return 100 / (value + 100) if value > 0 else -value / (-value + 100)


def adot_band(adot: float | None) -> str:
    if adot is None or not math.isfinite(float(adot)):
        return "unknown"
    if float(adot) < 7:
        return "low"
    if float(adot) <= 10:
        return "mid"
    return "high"


def asof_rows(frame: pd.DataFrame, event_week: int, week_col: str = "week") -> pd.DataFrame:
    """Return only observations strictly earlier than the event week."""
    return frame.loc[pd.to_numeric(frame[week_col], errors="coerce") < int(event_week)].copy()


def _position_map() -> dict[str, str]:
    players = pd.read_parquet(NV / "derived_pit" / "players_slim_shared_src_20261102.parquet")
    mapping = dict(zip(players["gsis_id"].astype(str), players["position_group"].fillna("UNK").astype(str)))
    stats = pd.read_parquet(NV / "stats_player_week_2024.parquet")
    for row in stats[["player_id", "position"]].dropna().drop_duplicates("player_id").itertuples(index=False):
        mapping[str(row.player_id)] = str(row.position)
    roster_path = NV / "roster_weekly_2026_w1_10_pulled_20261113T1633Z.parquet"
    if roster_path.exists():
        roster = pd.read_parquet(roster_path)
        for row in roster[["gsis_id", "position"]].dropna().drop_duplicates("gsis_id").itertuples(index=False):
            mapping[str(row.gsis_id)] = str(row.position)
    return mapping


def player_games_from_pbp(path: Path, position_map: dict[str, str]) -> pd.DataFrame:
    """Build opportunity-level player-game yardage from nflverse play-by-play."""
    pbp = pd.read_parquet(path)
    pbp = pbp.loc[pbp["season_type"].astype(str).eq("REG")].copy()
    if "two_point_attempt" in pbp:
        pbp = pbp.loc[pd.to_numeric(pbp["two_point_attempt"], errors="coerce").fillna(0).ne(1)]

    records: list[pd.DataFrame] = []
    target = pbp.loc[pbp["receiver_player_id"].notna()].copy()
    if not target.empty:
        target["player_id"] = target["receiver_player_id"].astype(str)
        target["yards"] = pd.to_numeric(target["receiving_yards"], errors="coerce").fillna(0.0)
        target["air"] = pd.to_numeric(target["air_yards"], errors="coerce").fillna(0.0)
        rec = target.groupby(["season", "week", "game_id", "player_id"], as_index=False).agg(
            yards=("yards", "sum"), opportunities=("player_id", "size"), air_yards=("air", "sum")
        )
        rec["market"] = "receiving_yards"
        records.append(rec)

    rush_mask = pd.to_numeric(pbp["rush_attempt"], errors="coerce").fillna(0).eq(1) & pbp["rusher_player_id"].notna()
    rush = pbp.loc[rush_mask].copy()
    if not rush.empty:
        rush["player_id"] = rush["rusher_player_id"].astype(str)
        rush["yards"] = pd.to_numeric(rush["rushing_yards"], errors="coerce").fillna(0.0)
        rush["air"] = 0.0
        ru = rush.groupby(["season", "week", "game_id", "player_id"], as_index=False).agg(
            yards=("yards", "sum"), opportunities=("player_id", "size"), air_yards=("air", "sum")
        )
        ru["market"] = "rushing_yards"
        records.append(ru)

    if not records:
        return pd.DataFrame(columns=["season", "week", "game_id", "player_id", "market", "yards", "opportunities", "air_yards", "position"])
    result = pd.concat(records, ignore_index=True)
    result["position"] = result["player_id"].map(position_map).fillna("UNK")
    result = result.loc[result["position"].isin(POSITION_SET)].copy()
    result["season"] = pd.to_numeric(result["season"], errors="coerce").astype(int)
    result["week"] = pd.to_numeric(result["week"], errors="coerce").astype(int)
    return result.sort_values(["season", "player_id", "week", "market"]).reset_index(drop=True)


def _feature_observations(games: pd.DataFrame) -> list[dict[str, Any]]:
    """Make normalized yardage observations using each player's prior games only."""
    rows: list[dict[str, Any]] = []
    for (season, pid), player in games.groupby(["season", "player_id"], sort=False):
        previous: dict[str, list[float]] = {"receiving_yards": [], "rushing_yards": []}
        prior_air = 0.0
        prior_targets = 0
        for week, weekly in player.groupby("week", sort=True):
            adot = prior_air / prior_targets if prior_targets else None
            for row in weekly.itertuples(index=False):
                prior = previous[row.market]
                if len(prior) >= 2:
                    baseline = float(np.mean(prior))
                    if baseline > 0:
                        rows.append({
                            "season": int(season), "player_id": str(pid), "week": int(week),
                            "market": row.market, "position": row.position,
                            "adot_band": adot_band(adot), "ratio": float(row.yards) / baseline,
                        })
            for row in weekly.itertuples(index=False):
                previous[row.market].append(float(row.yards))
                if row.market == "receiving_yards":
                    prior_air += float(row.air_yards)
                    prior_targets += int(row.opportunities)
    return rows


def _fit_group(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    ratios = np.asarray([r["ratio"] for r in rows], dtype=float)
    ratios = ratios[np.isfinite(ratios) & (ratios >= 0)]
    positive = ratios[ratios > 0]
    if len(ratios) < MIN_GROUP_N or len(positive) < 15:
        return None
    shape, _loc, scale = gamma.fit(positive, floc=0)
    if not np.isfinite(shape) or shape <= 0:
        return None
    return {
        "n": int(len(ratios)), "n_positive": int(len(positive)),
        "zero_mass": round(float(np.mean(ratios == 0)), 6),
        "shape": round(float(shape), 6), "ratio_scale_mle": round(float(scale), 6),
    }


def fit_shape_model(training: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in training:
        market, position, band = row["market"], row["position"], row["adot_band"]
        grouped[f"{market}|{position}|{band}"].append(row)
        grouped[f"{market}|{position}|all"].append(row)
        grouped[f"{market}|all|all"].append(row)
    models = {}
    for key, rows in sorted(grouped.items()):
        fitted = _fit_group(rows)
        if fitted:
            models[key] = fitted
    return models


def resolve_shape(model: dict[str, Any], market: str, position: str | None, adot: float | None) -> tuple[dict[str, Any] | None, str | None]:
    pos = position if position in POSITION_SET else "UNK"
    band = adot_band(adot)
    for key in (f"{market}|{pos}|{band}", f"{market}|{pos}|all", f"{market}|all|all"):
        params = model.get(key)
        if params:
            return params, key
    return None, None


def tail_probability(model: dict[str, Any], market: str, position: str | None, adot: float | None,
                     median: float, rung: float) -> tuple[float | None, str | None]:
    """P(yards > rung) under a zero-inflated gamma with the requested median."""
    params, key = resolve_shape(model, market, position, adot)
    if not params or not math.isfinite(float(median)) or float(median) <= 0:
        return None, key
    zero_mass = float(params["zero_mass"])
    if zero_mass >= 0.5:
        return None, key
    shape = float(params["shape"])
    conditional_median = (0.5 - zero_mass) / (1.0 - zero_mass)
    gamma_median = float(gamma.ppf(conditional_median, a=shape, scale=1.0))
    if not math.isfinite(gamma_median) or gamma_median <= 0:
        return None, key
    scale = float(median) / gamma_median
    if float(rung) < 0:
        return 1.0, key
    probability = (1.0 - zero_mass) * float(gamma.sf(float(rung), a=shape, scale=scale))
    return min(1.0, max(0.0, probability)), key


def _hold_estimates(docs: list[dict[str, Any]]) -> tuple[dict[str, float], dict[str, int], dict[str, dict[str, float]]]:
    paired: dict[tuple[str, str, str, float], dict[str, float]] = defaultdict(dict)
    for doc in docs:
        gid = str(doc.get("game_id", ""))
        for row in doc.get("rows", []):
            if row.get("book") != "fanduel" or row.get("market") not in {"receiving_yards", "rushing_yards"}:
                continue
            if row.get("line") is None or row.get("american") is None:
                continue
            paired[(gid, norm_name(row.get("player", "")), row["market"], float(row["line"]))][row.get("side", "")] = float(row["american"])
    holds: dict[str, list[float]] = defaultdict(list)
    game_holds: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for (gid, _player, market, _line), sides in paired.items():
        if "Over" not in sides or "Under" not in sides:
            continue
        hold = implied(sides["Over"]) + implied(sides["Under"]) - 1.0
        if 0 <= hold < 0.25:
            holds[market].append(hold)
            game_holds[gid][market].append(hold)
    mean_hold = {market: float(np.mean(values)) for market, values in holds.items() if values}
    counts = {market: len(values) for market, values in holds.items()}
    by_game = {
        gid: {market: float(np.mean(values)) for market, values in markets.items() if values}
        for gid, markets in game_holds.items()
    }
    return mean_hold, counts, by_game


def _roster_contexts(docs: list[dict[str, Any]], games_2026: pd.DataFrame) -> dict[str, dict[str, Any]]:
    roster_path = NV / "roster_weekly_2026_w1_10_pulled_20261113T1633Z.parquet"
    roster = pd.read_parquet(roster_path) if roster_path.exists() else pd.DataFrame()
    if not roster.empty:
        roster["_norm"] = roster["full_name"].map(norm_name)
    contexts: dict[str, dict[str, Any]] = {}
    history_by_player = {str(pid): frame for pid, frame in games_2026.groupby("player_id", sort=False)}
    adot_by_player_week = _adot_by_player_week(games_2026)
    games_2026 = games_2026.loc[games_2026["season"].eq(2026)]
    for doc in docs:
        gid = str(doc.get("game_id", ""))
        try:
            week = int(gid.split("_")[1])
            teams = set(gid.split("_")[2:4])
        except (IndexError, ValueError):
            continue
        players = {norm_name(row.get("player", "")): row.get("player", "") for row in doc.get("rows", []) if row.get("player")}
        for name_norm, display_name in players.items():
            position = None
            pid = None
            if not roster.empty:
                candidates = roster.loc[roster["_norm"].eq(name_norm) & roster["team"].isin(teams) & (roster["week"] < week)]
                if not candidates.empty:
                    latest_week = candidates["week"].max()
                    latest = candidates.loc[candidates["week"].eq(latest_week)].drop_duplicates("gsis_id")
                    if len(latest) == 1:
                        pid = str(latest.iloc[0]["gsis_id"])
                        position = str(latest.iloc[0]["position"])
            history = history_by_player.get(pid, pd.DataFrame()) if pid else pd.DataFrame()
            adot = adot_by_player_week.get((pid, week)) if pid else None
            prior_history = history.loc[history["week"].lt(week)] if not history.empty else history
            contexts[f"{gid}|{name_norm}"] = {
                "player": display_name, "player_id": pid, "position": position,
                "adot": round(adot, 4) if adot is not None else None,
                "adot_band": adot_band(adot),
                "feature_max_week": int(prior_history["week"].max()) if not prior_history.empty else None,
            }
    return contexts


def _adot_by_player_week(games: pd.DataFrame) -> dict[tuple[str, int], float | None]:
    """Compute cumulative aDOT as of each week without looking at that week's plays."""
    result: dict[tuple[str, int], float | None] = {}
    receiving = games.loc[games["market"].eq("receiving_yards")]
    for pid, player in receiving.groupby("player_id", sort=False):
        by_week = player.groupby("week", as_index=False).agg(
            targets=("opportunities", "sum"), air=("air_yards", "sum")
        )
        for week in range(1, 19):
            prior = by_week.loc[by_week["week"].lt(week)]
            targets = int(prior["targets"].sum()) if not prior.empty else 0
            air = float(prior["air"].sum()) if not prior.empty else 0.0
            result[(str(pid), week)] = air / targets if targets else None
    return result


def _cluster_bootstrap_brier(rows: list[dict[str, Any]], reps: int = BOOT_REPS) -> dict[str, Any]:
    if not rows:
        return {"clusters": 0, "dist_minus_book_ci95": [None, None], "blend_minus_book_ci95": [None, None]}
    frame = pd.DataFrame(rows)
    cluster_cols = [c for c in ["game_id", "gsis_id", "market"] if c in frame]
    grouped = frame.groupby(cluster_cols, dropna=False).agg(
        n=("actual_hit", "size"),
        book=("err_book", "sum"), dist=("err_dist", "sum"), blend=("err_blend", "sum"),
    )
    if len(grouped) < 2:
        return {"clusters": int(len(grouped)), "dist_minus_book_ci95": [None, None], "blend_minus_book_ci95": [None, None]}
    rng = np.random.default_rng(BOOT_SEED)
    sizes = grouped["n"].to_numpy(float)
    book = grouped["book"].to_numpy(float)
    dist = grouped["dist"].to_numpy(float)
    blend = grouped["blend"].to_numpy(float)
    idx = rng.integers(0, len(grouped), size=(reps, len(grouped)))
    denominator = sizes[idx].sum(axis=1)
    d = (dist[idx].sum(axis=1) - book[idx].sum(axis=1)) / denominator
    b = (blend[idx].sum(axis=1) - book[idx].sum(axis=1)) / denominator
    return {
        "clusters": int(len(grouped)),
        "dist_minus_book_ci95": [round(float(x), 6) for x in np.quantile(d, [0.025, 0.975])],
        "blend_minus_book_ci95": [round(float(x), 6) for x in np.quantile(b, [0.025, 0.975])],
        "method": "percentile bootstrap resampling player-game-market clusters",
        "reps": reps, "seed": BOOT_SEED,
    }


def _load_direct_docs() -> list[dict[str, Any]]:
    docs = []
    for path in sorted(DIRECT_LINES.glob("20*.json")):
        try:
            docs.append(json.loads(path.read_text()))
        except (OSError, json.JSONDecodeError):
            continue
    return docs


def _backtest(model: dict[str, Any], hold_by_market: dict[str, float], games_2026: pd.DataFrame) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rung_rows: list[dict[str, Any]] = []
    if not GRADE_CSV.exists():
        return rung_rows, {"status": "no archived alt ladder grades", "n": 0}
    grade = pd.read_csv(GRADE_CSV)
    excluded = {"missing_pregame_median": 0, "missing_hold_proxy": 0, "unsupported_distribution": 0}
    adot_map = _adot_by_player_week(games_2026)
    for row in grade.itertuples(index=False):
        market = "receiving_yards" if row.market == "rec" else "rushing_yards"
        hold = hold_by_market.get(market)
        try:
            median = float(row.trail_mean)
            american = float(row.price)
            rung = float(row.rung)
            actual = float(row.actual)
        except (TypeError, ValueError):
            continue
        if not math.isfinite(median) or median <= 0:
            excluded["missing_pregame_median"] += 1
            continue
        if hold is None:
            excluded["missing_hold_proxy"] += 1
            continue
        adot = adot_map.get((str(row.gsis_id), int(row.week)))
        pdist, model_key = tail_probability(model, market, str(row.pos), adot, median, rung)
        if pdist is None:
            excluded["unsupported_distribution"] += 1
            continue
        p_raw = implied(american)
        p_book = min(1.0, max(0.0, p_raw / (1.0 + hold)))
        hit = 1.0 if actual > rung else 0.0
        blend = (p_book + pdist) / 2.0
        item = {
            "game_id": str(row.game_id), "week": int(row.week), "player": str(row.player),
            "gsis_id": str(row.gsis_id), "market": market, "rung": rung,
            "american": american, "p_book": round(p_book, 6), "p_dist": round(pdist, 6),
            "gap": round(pdist - p_book, 6), "actual_hit": hit,
            "median": median, "median_source": "pregame trailing mean from preregistered grade file; historical main line unavailable",
            "adot": round(adot, 4) if adot is not None else None,
            "model_group": model_key, "hold_proxy": round(hold, 6),
        }
        item["err_book"] = (p_book - hit) ** 2
        item["err_dist"] = (pdist - hit) ** 2
        item["err_blend"] = (blend - hit) ** 2
        rung_rows.append(item)
    if not rung_rows:
        return rung_rows, {"status": "no rows had complete pregame median, shape, and hold inputs", "n": 0}
    frame = pd.DataFrame(rung_rows)
    brier = {
        "book_fair": float(frame["err_book"].mean()),
        "distribution": float(frame["err_dist"].mean()),
        "blend": float(frame["err_blend"].mean()),
    }
    brier["distribution_minus_book"] = brier["distribution"] - brier["book_fair"]
    brier["blend_minus_book"] = brier["blend"] - brier["book_fair"]
    interval = _cluster_bootstrap_brier(rung_rows)
    def excludes_zero(bounds: list[float | None]) -> bool:
        return bounds[0] is not None and (bounds[0] > 0 or bounds[1] < 0)

    significant = {
        "distribution_vs_book": excludes_zero(interval["dist_minus_book_ci95"]),
        "blend_vs_book": excludes_zero(interval["blend_minus_book_ci95"]),
    }
    direction = {
        "distribution_vs_book": "worse" if significant["distribution_vs_book"] and brier["distribution_minus_book"] > 0 else ("better" if significant["distribution_vs_book"] else "not significant"),
        "blend_vs_book": "worse" if significant["blend_vs_book"] and brier["blend_minus_book"] > 0 else ("better" if significant["blend_vs_book"] else "not significant"),
    }
    summary = {
        "status": "backtested with an explicit trailing-mean median proxy",
        "n_rungs": len(rung_rows), "n_player_games": int(frame[["game_id", "gsis_id", "market"]].drop_duplicates().shape[0]),
        "coverage": {
            "source_rungs": int(len(grade)), "scored_rungs": int(len(rung_rows)),
            "excluded_rungs": int(len(grade) - len(rung_rows)), "exclusions": excluded,
        },
        "weeks": sorted(int(x) for x in frame["week"].unique()),
        "brier": {k: round(float(v), 6) for k, v in brier.items()},
        "brier_difference_ci95": interval, "significant_brier_difference": significant,
        "brier_difference_direction": direction,
        "warning": "Week 8-9 archived alt files contain no contemporaneous main line or two-way alt prices. The model median is the archived pregame trailing mean; book probabilities are de-vigged with the available FanDuel main-line average hold proxy. This is not a main-line-matched or true no-vig alt-ladder backtest.",
    }
    return rung_rows, summary


def _current_rungs(docs: list[dict[str, Any]], model: dict[str, Any], contexts: dict[str, dict[str, Any]],
                   hold_by_market: dict[str, float], hold_by_game: dict[str, dict[str, float]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for doc in docs:
        gid = str(doc.get("game_id", ""))
        rows = doc.get("rows", [])
        main: dict[tuple[str, str], float] = {}
        for row in rows:
            if row.get("book") != "fanduel" or row.get("market") not in {"receiving_yards", "rushing_yards"} or row.get("line") is None:
                continue
            main[(norm_name(row.get("player", "")), row["market"])] = float(row["line"])
        for row in rows:
            market = {"alt_receiving_yards": "receiving_yards", "alt_rushing_yards": "rushing_yards"}.get(row.get("market"))
            if row.get("book") != "fanduel" or not market or row.get("side") != "Over" or row.get("line") is None or row.get("american") is None:
                continue
            name = norm_name(row.get("player", ""))
            median = main.get((name, market))
            context = contexts.get(f"{gid}|{name}", {})
            if median is None:
                continue
            hold = hold_by_game.get(gid, {}).get(market, hold_by_market.get(market))
            if hold is None:
                continue
            p_dist, model_key = tail_probability(model, market, context.get("position"), context.get("adot"), median, float(row["line"]))
            if p_dist is None:
                continue
            p_book = implied(float(row["american"])) / (1.0 + hold)
            results.append({
                "game_id": gid, "player": row.get("player"), "market": market,
                "rung": float(row["line"]), "american": float(row["american"]),
                "quote_retrieved_utc": doc.get("retrieved_utc"),
                "p_book": round(p_book, 6), "p_dist": round(p_dist, 6), "gap": round(p_dist - p_book, 6),
                "median": median, "median_source": "FanDuel main line", "position": context.get("position"),
                "adot": context.get("adot"), "model_group": model_key, "hold_proxy": round(float(hold), 6),
            })
    return results


def main() -> dict[str, Any]:
    position_map = _position_map()
    training_parts = [player_games_from_pbp(NV / MARKET_FILES[year], position_map) for year in (2022, 2024)]
    training_games = pd.concat(training_parts, ignore_index=True)
    training = _feature_observations(training_games)
    model = fit_shape_model(training)
    docs = _load_direct_docs()
    hold_by_market, hold_counts, hold_by_game = _hold_estimates(docs)
    current_games = player_games_from_pbp(NV / MARKET_FILES[2026], position_map)
    contexts = _roster_contexts(docs, current_games)
    historical_rungs, backtest = _backtest(model, hold_by_market, current_games)
    current_rungs = _current_rungs(docs, model, contexts, hold_by_market, hold_by_game)
    shape_summaries = {
        key: value for key, value in sorted(model.items())
    }
    result = {
        "schema_version": 1,
        "status": "complete" if training and model else "insufficient historical data",
        "data": {
            "fit_seasons": [2022, 2024], "missing_expected_seasons": [2023],
            "historical_player_game_rows": int(len(training_games)),
            "normalized_training_observations": int(len(training)),
            "shape_groups": len(model),
            "model_inputs": [MARKET_FILES[2022], MARKET_FILES[2024]],
            "hold_source": "mean FanDuel main-market two-way overround from available pregame/direct_lines snapshots",
            "hold_sample_count": hold_counts,
            "hold_by_market": {k: round(v, 6) for k, v in hold_by_market.items()},
            "direct_line_games": len(docs), "player_contexts": len(contexts),
        },
        "model": model,
        "model_summary": shape_summaries,
        "player_contexts": contexts,
        "rungs": current_rungs,
        "archived_backtest_rows": [
            {key: row[key] for key in (
                "game_id", "week", "player", "market", "rung", "american",
                "p_book", "p_dist", "gap", "actual_hit", "median", "median_source",
            )}
            for row in historical_rungs
        ],
        "backtest": backtest,
        "limitations": [
            "The repository does not contain 2023 play-by-play; shape fitting uses the available 2022 and 2024 seasons.",
            "Weeks 8-9 FanDuel alt snapshots are one-sided and have no matching main-line snapshots. The archived backtest uses the prior trailing mean as its median proxy and the available FanDuel main-line average overround as a hold proxy.",
            "Current direct-line rungs are quoted outputs only; they are not backtested because the included 2026 play-by-play ends at Week 9.",
        ],
    }
    _write_json(result, OUT / "ladder.json", {"rungs", "archived_backtest_rows"})
    print(json.dumps({"status": result["status"], "data": result["data"], "backtest": result["backtest"], "current_rungs": len(current_rungs)}, indent=1))
    return result


if __name__ == "__main__":
    main()
