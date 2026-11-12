"""Grade one finished game's pregame packet against the result and the last saved pre-kickoff prices.

    python -m grading.grade --game 2026_10_WAS_NYG --write

What it grades, from the packet committed before kickoff:
  * every flagged prop (packet books.prop_check rows; side = sign of baseline_minus_line)
  * every research player projection (matchup.*.player_baselines)
  * the research team projection (team_projection samplers: points, margin, total, and model probabilities)
Against:
  * the actual result from nflverse (free public releases; same source the packet builder uses)
  * the closing line: the latest saved snapshot before kickoff from the same book (packet books section,
    pregame/line_history, saved price freezes). If none exists it is "unknown" and never estimated.
Writes grading/results/<game>.jsonl (one row per graded item) and <game>.summary.json.

Refuses (exit 2, nothing written) if the game is not final or no packet was generated before kickoff.
Costs nothing: no Odds API or other paid call. Never touches projection_ready, model weights or formulas.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import core as C
from . import sources as S

ROOT = S.ROOT
RESULTS = ROOT / "grading" / "results"
CONFIG = json.loads((ROOT / "grading" / "config.json").read_text())
EXIT_REFUSED = 2


def load_graded_rows(results_dir: Path) -> list[dict]:
    rows = []
    for f in sorted(results_dir.glob("*.jsonl")):
        for ln in f.read_text().splitlines():
            if ln.strip():
                rows.append(json.loads(ln))
    return rows


def _baselines(pk: dict) -> dict:
    """{(team, short_key): baseline} from the packet; duplicate keys (e.g. a back listed as receiver and rusher) merge."""
    out = {}
    for side, m in (pk.get("matchup") or {}).items():
        team = side.split("_offense_vs_")[0]
        for pl in ((m or {}).get("player_baselines") or {}).get("players") or []:
            k = (team, S.short_key(pl.get("player", "")))
            out.setdefault(k, {}).update(pl)
    return out


def grade_game(game_id: str, pk: dict, pk_source: str, pk_pulled: str, kickoff: datetime, actuals,
               snapshots: list[dict], history: list[dict], cfg: dict = CONFIG, now: datetime | None = None) -> list[dict]:
    now = now or datetime.now(timezone.utc)
    g = pk.get("game") or {}
    home, away = g.get("home"), g.get("away")
    books = (pk.get("books") or {})
    bk_src, bk_pulled = f"{pk_source}#books", books.get("retrieved_utc")
    markets = books.get("markets") or {}
    ref_books = cfg["reference_books"]
    min_n, min_games = cfg["min_holdout_props_per_market_type"], cfg["min_volume_games"]
    pbp_src, pbp_pulled = actuals.src("pbp")
    games_src, games_pulled = actuals.src("games")
    base = _baselines(pk)
    records: dict[str, dict] = {}

    def record(mt):
        if mt not in records:
            records[mt] = C.clv_record(history, mt, kickoff, game_id, min_n)
        return records[mt]

    def common(kind, mt, key, side, extra):
        return {"schema": "grading.v1", "game_id": game_id, "kickoff_utc": kickoff.isoformat(), "graded_utc": now.isoformat(timespec="seconds"),
                "kind": kind, "market_type": mt, "market_key": key, "side": C.u(side), "projection_ready": False,
                "packet": {"source": pk_source, "generated_utc": C.u(pk_pulled)}, **extra}

    def closing(key, book, side, bet_line, bet_prices, market):
        cq = C.closing_quote(snapshots, key, book, kickoff) if C.known(book) else None
        mins = C.UNKNOWN
        if cq:
            mins = round((kickoff - C.parse_utc(cq["snapshot_utc"])).total_seconds() / 60, 1)
        close_price = (cq.get("prices") or {}).get(side) if cq else None
        return (C.fig(cq.get("line") if cq else None, cq.get("source") if cq else None, cq.get("snapshot_utc") if cq else None,
                      minutes_before_kickoff=mins, book=book, book_quote_utc=cq.get("quote_utc") if cq else None,
                      note="latest snapshot saved in this repo before kickoff; not claimed to be the true close"),
                C.fig(close_price, cq.get("source") if cq else None, cq.get("snapshot_utc") if cq else None),
                C.clv(market, side, home, bet_line, bet_prices, cq, bet_utc=bk_pulled))

    rows = []

    # 1. flagged props -----------------------------------------------------------------------------
    for r in ((books.get("prop_check") or {}).get("rows") or []):
        stat, player, book, line = r.get("stat"), r.get("player"), r.get("book"), r.get("line")
        key = f"{stat}|{player}"
        diff = r.get("baseline_minus_line")
        side = ("Over" if diff > 0 else "Under" if diff < 0 else None) if C.known(diff) else None
        who = actuals.resolve_full(player)
        team = who.get("team")
        actual = actuals.stat(who.get("gsis_id"), player, team, stat)
        bet_prices = r.get("prices") or {}
        bet_price = bet_prices.get(side) if side else None
        mq = markets.get(key) or {}
        best = C.best_retail_break_even(mq.get("books"), stat, side, line, home, ref_books) if side else C.best_retail_break_even({}, stat, "", None, home, ref_books)
        model_prob = r.get(f"model_prob_{side.lower()}") if side else None
        bl = base.get((team, S.abbrev(player))) if C.known(team) else None
        vol = C.volume_check(bl, stat, side, line, min_games)
        close_line, close_price, clv = closing(key, book, side, line, bet_prices, stat)
        rows.append(common("flagged_prop", stat, key, side, {
            "player": player, "team": C.u(team), "player_match": who.get("reason") or "full name + team (nflverse roster)",
            "book": book,
            "projection": C.fig(r.get("baseline_weighted_mean"), f"{pk_source}#books.prop_check", pk_pulled, kind="baseline_weighted_mean"),
            "model_prob": C.fig(model_prob, f"{pk_source}#books.prop_check" if C.known(model_prob) else None, pk_pulled if C.known(model_prob) else None,
                                note="" if C.known(model_prob) else "packet carries no model probability for this prop"),
            "bet_line": C.fig(line, bk_src, bk_pulled), "bet_price": C.fig(bet_price, bk_src, bk_pulled),
            "bet_break_even": C.fig(C.break_even(bet_price), bk_src, bk_pulled),
            "best_retail_break_even": C.fig(best["break_even"], bk_src, bk_pulled, book=best["book"], price=best["price"]),
            "actual": C.fig(actual, pbp_src, pbp_pulled), "result": C.prop_result(actual, side, line),
            "closing_line": close_line, "closing_price": close_price, "clv": clv,
            "edge_rule": C.edge_decision(model_prob, best["break_even"], vol, record(stat), cfg),
        }))

    # 2. research player projections ---------------------------------------------------------------
    for (team, skey), pl in base.items():
        who = actuals.resolve_short(pl.get("player", ""), team)
        for stat in ("receiving_yards", "receptions", "targets", "rushing_yards", "carries", "passing_yards", "pass_attempts"):
            b = pl.get(stat)
            if not isinstance(b, dict):
                continue
            actual = actuals.stat(who.get("gsis_id"), who.get("full_name"), team, stat)
            proj = b.get("weighted_mean")
            err = round(float(actual) - float(proj), 2) if C.known(actual) and C.known(proj) else C.UNKNOWN
            rows.append(common("player_projection", stat, f"{stat}|{pl.get('player')}", None, {
                "player": pl.get("player"), "team": team, "player_match": who.get("reason") or "short name + team (nflverse roster)",
                "projection": C.fig(proj, f"{pk_source}#matchup.player_baselines", pk_pulled, p50=b.get("p50"), games=b.get("games")),
                "actual": C.fig(actual, pbp_src, pbp_pulled), "error_actual_minus_projection": err,
                "label": cfg["research_label"],
            }))

    # 3. research team projection ------------------------------------------------------------------
    tp = pk.get("team_projection") or {}
    mk = pk.get("market") or {}
    hs, as_ = actuals.score(home), actuals.score(away)
    actual_team = {"home_points": hs, "away_points": as_,
                   "total": hs + as_ if C.known(hs) and C.known(as_) else C.UNKNOWN,
                   "home_margin": hs - as_ if C.known(hs) and C.known(as_) else C.UNKNOWN}
    for name, smp in (tp.get("samplers") or {}).items():
        src = f"{pk_source}#team_projection.samplers.{name}"
        for q, a in actual_team.items():
            proj = smp.get(q)
            err = round(float(a) - float(proj), 2) if C.known(a) and C.known(proj) else C.UNKNOWN
            rows.append(common("team_projection", q, f"{q}|{name}", None, {
                "projection": C.fig(proj, src, pk_pulled), "actual": C.fig(a, games_src, games_pulled),
                "error_actual_minus_projection": err, "label": cfg["research_label"]}))
        for market, pkey, line, sides in (("spread", "home_covers_market_spread", mk.get("home_spread"), (home, away)),
                                          ("total", "over_market_total", mk.get("total"), ("Over", "Under")),
                                          ("moneyline", "home_win", None, (home, away))):
            p = smp.get(pkey)
            if not C.known(p):
                side, prob = None, None
            elif market == "moneyline":
                side, prob = (home, p) if p >= smp.get("away_win", 1 - p) else (away, smp.get("away_win", round(1 - p, 3)))
            else:
                side, prob = (sides[0], p) if p >= 0.5 else (sides[1], round(1 - p, 3))
            mq = markets.get(market) or {}
            best = C.best_retail_break_even(mq.get("books"), market, side, line, home, ref_books) if side else {"break_even": C.UNKNOWN, "book": C.UNKNOWN, "price": C.UNKNOWN}
            book = best["book"]
            bq = (mq.get("books") or {}).get(book) if C.known(book) else None
            bet_line = (bq or {}).get("line") if market != "moneyline" else None
            bet_prices = (bq or {}).get("prices") or {}
            close_line, close_price, clv = closing(market, book, side, bet_line, bet_prices, market)
            if market == "spread":
                res = C.spread_result(hs, as_, line, side, home)
            elif market == "total":
                res = C.prop_result(actual_team["total"], side, line)
            else:
                res = C.moneyline_result(hs, as_, side, home)
            rows.append(common("team_market", market, f"{market}|{name}", side, {
                "model_prob": C.fig(prob, src, pk_pulled, field=pkey,
                                    note="decisive (no-push) probability at the packet's schedule line" if market != "moneyline" else ""),
                "model_line": C.fig(line, f"{pk_source}#market ({mk.get('source', C.UNKNOWN)})", pk_pulled),
                "book": book, "bet_line": C.fig(bet_line, bk_src if bq else None, bk_pulled if bq else None),
                "bet_price": C.fig(bet_prices.get(side) if side else None, bk_src if bq else None, bk_pulled if bq else None),
                "best_retail_break_even": C.fig(best["break_even"], bk_src, bk_pulled, book=book, price=best["price"]),
                "actual": C.fig(actual_team["home_margin"] if market != "total" else actual_team["total"], games_src, games_pulled),
                "result": res, "closing_line": close_line, "closing_price": close_price, "clv": clv,
                "edge_rule": C.edge_decision(prob, best["break_even"],
                                             {"supports": False, "reason": "volume condition applies to player props only"},
                                             record(market), cfg),
            }))
    return rows


def summarize(game_id: str, rows: list[dict], kickoff: datetime, pk_source: str, actuals) -> dict:
    by = {}
    for r in rows:
        k = by.setdefault(r["kind"], {"rows": 0, "actual_known": 0, "closing_known": 0, "edges": 0})
        k["rows"] += 1
        k["actual_known"] += C.known((r.get("actual") or {}).get("value"))
        k["closing_known"] += C.known((r.get("closing_line") or {}).get("value")) if "closing_line" in r else 0
        k["edges"] += bool((r.get("edge_rule") or {}).get("edge"))
    hold = {}
    for r in rows:
        rec = ((r.get("edge_rule") or {}).get("c3_positive_clv_record_on_holdout") or {})
        if rec.get("market_type"):
            hold[rec["market_type"]] = {k: rec[k] for k in ("n", "beat_close", "did_not_beat", "min_n", "holdout_ready", "positive")}
    any_ready = any(v["holdout_ready"] for v in hold.values())
    return {"schema": "grading.summary.v1", "game_id": game_id, "kickoff_utc": kickoff.isoformat(),
            "graded_utc": rows[0]["graded_utc"] if rows else C.UNKNOWN, "packet_source": pk_source,
            "actual_sources": {k: {"url": v.get("url"), "sha256": v.get("sha256"), "retrieved_utc": v.get("retrieved_utc"), "status": v.get("status")}
                               for k, v in actuals.prov.items()},
            "counts": by, "holdout_by_market_type": hold,
            "validation": "holdout met for some market types" if any_ready else CONFIG["research_label"],
            "projection_ready": False}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", required=True, help="nflverse game id, e.g. 2026_10_WAS_NYG")
    ap.add_argument("--cache", default="/tmp/nfl_grading_cache", help="where nflverse files are cached")
    ap.add_argument("--offline", action="store_true", help="use cached nflverse files only")
    ap.add_argument("--write", action="store_true", help="write grading/results/<game>.jsonl and .summary.json")
    a = ap.parse_args(argv)
    season = int(a.game.split("_")[0])
    actuals = S.load_actuals(a.game, season, Path(a.cache), offline=a.offline)
    kickoff = S.kickoff_from_games(actuals.games_df, a.game)
    if kickoff is None:
        print(f"grading: REFUSED {a.game}: kickoff unknown in nflverse schedule; nothing graded"); return EXIT_REFUSED
    if not actuals.final():
        print(f"grading: REFUSED {a.game}: game not final in nflverse (score or play-by-play missing); nothing graded"); return EXIT_REFUSED
    pk, pk_source, pk_pulled = S.packet_before_kickoff(a.game, kickoff)
    if pk is None:
        print(f"grading: REFUSED {a.game}: {pk_source}; nothing graded"); return EXIT_REFUSED
    g = pk.get("game") or {}
    snaps = (S.packet_snapshots(pk, pk_source) + S.line_history_snapshots(a.game)
             + S.freeze_snapshots(g.get("away", ""), g.get("home", "")))
    history = load_graded_rows(RESULTS)
    rows = grade_game(a.game, pk, pk_source, pk_pulled, kickoff, actuals, snaps, history)
    summ = summarize(a.game, rows, kickoff, pk_source, actuals)
    print(json.dumps({k: summ[k] for k in ("game_id", "kickoff_utc", "packet_source", "counts", "validation")}, indent=1))
    if a.write:
        RESULTS.mkdir(parents=True, exist_ok=True)
        (RESULTS / f"{a.game}.jsonl").write_text("".join(json.dumps(r, sort_keys=True, default=str) + "\n" for r in rows))
        (RESULTS / f"{a.game}.summary.json").write_text(json.dumps(summ, indent=1, sort_keys=True, default=str) + "\n")
        print(f"grading: wrote grading/results/{a.game}.jsonl ({len(rows)} rows) and .summary.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
