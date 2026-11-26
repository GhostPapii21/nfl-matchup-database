"""Backfill market grades for 2026 NFL Weeks 1-9 (refs NFL-49, NFL-56). Research only.

Why this exists: `python -m grading.grade` refuses every W1-9 game (exit 2) because no pregame packet was
committed before those kickoffs (packets start in Week 10). The grader is NOT changed. This script grades the
game-line markets that do have saved prices, and writes to grading/backfill_w1_9/ (NOT grading/results/, so
these rows never enter the grader's packet CLV holdout).

Grades full game, halves and quarters: spread, total, moneyline.
  Actuals : nflverse play-by-play in this repo (data/historical/nflverse/pbp_2026_w1_11_pulled_20261124T1717ET.parquet),
            cross-checked against a fresh nflverse games.parquet and, for W1-8, data/historical/period_w1_8.
  Prices  : (a) nflverse closing consensus already in the repo: period_w1_8 coverage ledger (W1-8) and
            data/lines/lines_wk04_09_2026.csv consensus rows (W9). Sportsbook and quote time unverified.
            (b) named-book quotes: latest verified pre-kickoff snapshot per game x book x market x period x line in
            the local inventory sportsbook_observations.csv (pregame_status == verified_capture_before_start).
Missing prices are "unknown"; nothing is estimated. No paid API is called. projection_ready is always false.
Conventions: FT and H2 include overtime, Q4 excludes it. A 2-way moneyline tie is graded "push" (void);
the book's own tie rule was not verified.
"""
from __future__ import annotations
import hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "grading" / "backfill_w1_9"
PBP = ROOT / "data/historical/nflverse/pbp_2026_w1_11_pulled_20261124T1717ET.parquet"
PBP_PULLED = "2026-11-24T22:17:40+00:00"
LEDGER = ROOT / "data/historical/period_w1_8/data/coverage_ledger_w1_8.csv"
P18 = ROOT / "data/historical/period_w1_8/data/games_w1_8.csv"
LINES = ROOT / "data/lines/lines_wk04_09_2026.csv"
OBS = Path("/workspace/research/historical_nfl_odds_inventory_2026-11-07/sportsbook_observations.csv")
GAMES = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/nfl_grading_cache/games.parquet")
U = "unknown"
PERIODS = ["FT", "H1", "H2", "Q1", "Q2", "Q3", "Q4"]
KINDS = ["spread", "total", "moneyline"]
NAMES = {"Arizona Cardinals": "ARI", "Atlanta Falcons": "ATL", "Baltimore Ravens": "BAL", "Buffalo Bills": "BUF",
         "Carolina Panthers": "CAR", "Chicago Bears": "CHI", "Cincinnati Bengals": "CIN", "Cleveland Browns": "CLE",
         "Dallas Cowboys": "DAL", "Denver Broncos": "DEN", "Detroit Lions": "DET", "Green Bay Packers": "GB",
         "Houston Texans": "HOU", "Indianapolis Colts": "IND", "Jacksonville Jaguars": "JAX", "Kansas City Chiefs": "KC",
         "Las Vegas Raiders": "LV", "Los Angeles Chargers": "LAC", "Los Angeles Rams": "LA", "Miami Dolphins": "MIA",
         "Minnesota Vikings": "MIN", "New England Patriots": "NE", "New Orleans Saints": "NO", "New York Giants": "NYG",
         "New York Jets": "NYJ", "Philadelphia Eagles": "PHI", "Pittsburgh Steelers": "PIT", "San Francisco 49ers": "SF",
         "Seattle Seahawks": "SEA", "Tampa Bay Buccaneers": "TB", "Tennessee Titans": "TEN", "Washington Commanders": "WAS"}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


def fig(v, src, pulled, **kw):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return U
    return {"value": v, "source": src, "pulled_utc": pulled, **kw}


def period_scores(pbp: pd.DataFrame) -> dict:
    out = {}
    for gid, d in pbp.groupby("game_id"):
        d = d.sort_values(["qtr", "play_id"])
        cum, prev = {}, (0, 0)
        for q in range(1, 6):
            dq = d[d.qtr <= q]
            last = dq.dropna(subset=["total_home_score"]).iloc[-1] if len(dq) else None
            cum[q] = (int(last.total_home_score), int(last.total_away_score)) if last is not None else prev
            prev = cum[q]
        per = {}
        p0 = (0, 0)
        for q in range(1, 6):
            per[q] = (cum[q][0] - p0[0], cum[q][1] - p0[1]); p0 = cum[q]
        ft = cum[5]
        out[gid] = {"Q1": per[1], "Q2": per[2], "Q3": per[3], "Q4": per[4],
                    "H1": (per[1][0] + per[2][0], per[1][1] + per[2][1]),
                    "H2": (per[3][0] + per[4][0] + per[5][0], per[3][1] + per[4][1] + per[5][1]),
                    "FT": ft, "OT": per[5]}
    return out


def grade(kind, sel, line, hs, as_, home, away):
    """sel is the team code for spread/moneyline, 'over'/'under' for total."""
    if kind == "total":
        t = hs + as_
        if line is None or pd.isna(line):
            return U
        d = t - line if sel == "over" else line - t
    else:
        m = hs - as_ if sel == home else as_ - hs
        if kind == "moneyline":
            return "win" if m > 0 else "loss" if m < 0 else "push"
        if line is None or pd.isna(line):
            return U
        d = m + line
    return "win" if d > 0 else "loss" if d < 0 else "push"


def main() -> int:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    games = pd.read_parquet(GAMES)
    games = games[(games.season == 2026) & (games.week <= 9) & (games.game_type == "REG")].copy()
    games_pulled = (GAMES.parent / (GAMES.name + ".retrieved_utc")).read_text().strip() if (GAMES.parent / (GAMES.name + ".retrieved_utc")).exists() else U
    games_src = f"nflverse games.parquet (https://github.com/nflverse/nflverse-data/releases/download/schedules/games.parquet) sha256={sha(GAMES)}"
    games["kick"] = pd.to_datetime(games.gameday + " " + games.gametime).dt.tz_localize("America/New_York").dt.tz_convert("UTC")
    pbp = pd.read_parquet(PBP, columns=["game_id", "week", "qtr", "play_id", "total_home_score", "total_away_score"])
    pbp = pbp[pbp.week <= 9]
    scores = period_scores(pbp)
    pbp_src = f"{rel(PBP)} sha256={sha(PBP)}"
    p18 = pd.read_csv(P18).set_index("game_id")
    checks = []
    for g in games.itertuples():
        s = scores.get(g.game_id)
        ok = s is not None and s["FT"] == (int(g.home_score), int(g.away_score))
        if g.game_id in p18.index:
            r = p18.loc[g.game_id]
            for q in (1, 2, 3, 4):
                ok = ok and s[f"Q{q}"] == (int(r[f"q{q}_home"]), int(r[f"q{q}_away"]))
        checks.append({"game_id": g.game_id, "pbp_matches_games_and_period_w1_8": bool(ok)})
    bad = [c["game_id"] for c in checks if not c["pbp_matches_games_and_period_w1_8"]]

    # --- prices -------------------------------------------------------------------------------------
    quotes = []  # dicts: game_id, period, kind, book, sel, line, price, src, pulled, line_type
    led = pd.read_csv(LEDGER)
    led_src = f"{rel(LEDGER)} (nflverse schedule values; ledger quote_limitation: NOT verified closing lines, sportsbook and quote time unverified) sha256={sha(LEDGER)}"
    for r in led.itertuples():
        pulled, home, away = r.pull_utc, r.home, r.away
        # nflverse spread_line: positive = home favored, so home handicap = -spread_line
        if not pd.isna(r.spread_line):
            quotes += [dict(game_id=r.game_id, period="FT", kind="spread", book="consensus", sel=home, line=-r.spread_line, price=r.home_spread_odds, src=led_src, pulled=pulled, line_type="close (nflverse consensus)"),
                       dict(game_id=r.game_id, period="FT", kind="spread", book="consensus", sel=away, line=r.spread_line, price=r.away_spread_odds, src=led_src, pulled=pulled, line_type="close (nflverse consensus)")]
        if not pd.isna(r.total_line):
            quotes += [dict(game_id=r.game_id, period="FT", kind="total", book="consensus", sel="over", line=r.total_line, price=r.over_odds, src=led_src, pulled=pulled, line_type="close (nflverse consensus)"),
                       dict(game_id=r.game_id, period="FT", kind="total", book="consensus", sel="under", line=r.total_line, price=r.under_odds, src=led_src, pulled=pulled, line_type="close (nflverse consensus)")]
        if not pd.isna(r.home_moneyline):
            quotes += [dict(game_id=r.game_id, period="FT", kind="moneyline", book="consensus", sel=home, line=None, price=r.home_moneyline, src=led_src, pulled=pulled, line_type="close (nflverse consensus)"),
                       dict(game_id=r.game_id, period="FT", kind="moneyline", book="consensus", sel=away, line=None, price=r.away_moneyline, src=led_src, pulled=pulled, line_type="close (nflverse consensus)")]
    lines = pd.read_csv(LINES)
    lines_src = f"{rel(LINES)} consensus row (source column: nflverse games.csv (nfldata); sportsbook unverified) sha256={sha(LINES)}"
    gi = games.set_index("game_id")
    for r in lines[(lines.week == 9) & (lines.book == "consensus")].itertuples():
        home, away = gi.loc[r.game_id, "home_team"], gi.loc[r.game_id, "away_team"]
        lt = f"{r.line_type} (nflverse consensus)"
        if not pd.isna(r.home_spread):
            quotes += [dict(game_id=r.game_id, period="FT", kind="spread", book="consensus", sel=home, line=r.home_spread, price=None, src=lines_src, pulled=r.pulled_utc, line_type=lt),
                       dict(game_id=r.game_id, period="FT", kind="spread", book="consensus", sel=away, line=-r.home_spread, price=None, src=lines_src, pulled=r.pulled_utc, line_type=lt)]
        if not pd.isna(r.total):
            quotes += [dict(game_id=r.game_id, period="FT", kind="total", book="consensus", sel=s, line=r.total, price=None, src=lines_src, pulled=r.pulled_utc, line_type=lt) for s in ("over", "under")]
        if not pd.isna(r.home_ml):
            quotes += [dict(game_id=r.game_id, period="FT", kind="moneyline", book="consensus", sel=home, line=None, price=r.home_ml, src=lines_src, pulled=r.pulled_utc, line_type=lt),
                       dict(game_id=r.game_id, period="FT", kind="moneyline", book="consensus", sel=away, line=None, price=r.away_ml, src=lines_src, pulled=r.pulled_utc, line_type=lt)]
    obs_note = U
    if OBS.exists():
        obs_sha = sha(OBS)
        o = pd.read_csv(OBS, low_memory=False)
        o = o[(o.pregame_status == "verified_capture_before_start") & o.player.isna() & (o.week <= 9)]
        kmap = {"spreads": "spread", "spread": "spread", "alternate_spreads": "spread", "totals": "total", "total": "total",
                "alternate_totals": "total", "h2h": "moneyline", "moneyline": "moneyline"}
        def kind_of(m):
            base = m.split("_")[0] if m.split("_")[-1] in ("h1", "h2", "q1", "q2", "q3", "q4") else m
            if m.startswith("alternate_spreads"): return "spread"
            if m.startswith("alternate_totals"): return "total"
            return kmap.get(base)
        o["kind"] = o.market.map(kind_of)
        o = o[o.kind.notna() & o.period.isin(PERIODS)]
        o["ts"] = pd.to_datetime(o.snapshot_timestamp, utc=True)
        o["alt"] = o.market.str.startswith("alternate")
        for r in o.itertuples():
            pass
        rows = []
        for r in o.itertuples():
            home, away = r.home_team, r.away_team
            s = str(r.selection)
            sel = {"home": home, "away": away, "over": "over", "under": "under", "Over": "over", "Under": "under"}.get(s, NAMES.get(s))
            if sel is None:
                continue
            rows.append((r.game_id, r.period, r.kind, r.bookmaker, sel, r.line, r.price, r.ts, r.snapshot_timestamp, r.upstream_source, r.source_filepath, r.alt))
        od = pd.DataFrame(rows, columns=["game_id", "period", "kind", "book", "sel", "line", "price", "ts", "snap", "up", "fp", "alt"])
        # main markets: latest snapshot per game x book x period x kind x selection; alt lines: latest per line too
        main = od[~od.alt].sort_values("ts").groupby(["game_id", "book", "period", "kind", "sel"]).tail(1)
        alt = od[od.alt].sort_values("ts").groupby(["game_id", "book", "period", "kind", "sel", "line"]).tail(1)
        for r in pd.concat([main, alt]).itertuples():
            src = f"local inventory {OBS} sha256={obs_sha} (upstream {r.up}; file {r.fp})"
            quotes.append(dict(game_id=r.game_id, period=r.period, kind=r.kind, book=r.book, sel=r.sel, line=r.line,
                               price=r.price, src=src, pulled=pd.Timestamp(r.ts).isoformat(), alt=bool(r.alt),
                               line_type="alt line, latest verified pre-kickoff snapshot" if r.alt else "latest verified pre-kickoff snapshot (not a certified closer)"))
        obs_note = f"{OBS} sha256={obs_sha}"

    # --- grade --------------------------------------------------------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    qdf = {}
    for q in quotes:
        qdf.setdefault(q["game_id"], []).append(q)
    summary = {"generated_utc": now, "projection_ready": False, "grader_used": False,
               "why_not_grader": "python -m grading.grade refuses all W1-9 games: no pregame/packets/<game>/packet.json committed before kickoff (packets start Week 10). grading/ code unchanged.",
               "actuals": {"pbp": pbp_src, "pbp_pulled_utc": PBP_PULLED, "games": games_src, "games_pulled_utc": games_pulled,
                           "cross_check_failures": bad},
               "price_sources": {"consensus_w1_8": led_src, "consensus_w9": lines_src, "named_books": obs_note},
               "conventions": "FT and H2 include OT; Q4 excludes OT; 2-way ML tie = push (book tie rule unverified); spread lines are the selection's own handicap",
               "per_week": {}, "per_game": {}}
    for g in games.sort_values(["week", "kick"]).itertuples():
        gid, home, away, kick = g.game_id, g.home_team, g.away_team, g.kick
        s = scores[gid]
        out = []
        for q in qdf.get(gid, []):
            hs, as_ = s[q["period"]]
            pulled = pd.Timestamp(q["pulled"]).tz_convert("UTC") if pd.Timestamp(q["pulled"]).tzinfo else pd.Timestamp(q["pulled"]).tz_localize("UTC")
            mbk = round((kick - pulled).total_seconds() / 60, 1)
            res = grade(q["kind"], q["sel"], q["line"], hs, as_, home, away)
            note = []
            if q["book"] == "consensus" and mbk < 0:
                note.append("consensus file fetched after kickoff by design (retrospective closing line); quote time unknown")
            if q["kind"] == "moneyline" and res == "push":
                note.append("tie: 2-way moneyline treated as void; book rule unverified")
            out.append({"game_id": gid, "week": int(g.week), "period": q["period"], "market": q["kind"], "book": q["book"],
                        "selection": q["sel"], "line_type": q["line_type"], "alt_line": q.get("alt", False),
                        "line": fig(None if q["kind"] == "moneyline" else float(q["line"]) if q["line"] is not None and not pd.isna(q["line"]) else None, q["src"], q["pulled"], minutes_before_kickoff=mbk),
                        "price": fig(None if q["price"] is None or pd.isna(q["price"]) else float(q["price"]), q["src"], q["pulled"], minutes_before_kickoff=mbk),
                        "actual": {"value": {"home": hs, "away": as_, "home_team": home, "away_team": away}, "source": pbp_src, "pulled_utc": PBP_PULLED},
                        "result": res, "notes": note, "projection_ready": False, "graded_utc": now})
        have = {(r["period"], r["market"]) for r in out if r["result"] != U}
        for p in PERIODS:
            for k in KINDS:
                if (p, k) not in have:
                    why = ("no saved pre-kickoff price for this period/market in the repo or local inventory"
                           if p != "FT" else "no saved price (named-book W1-5 verified pregame quotes are a known gap; consensus missing)")
                    out.append({"game_id": gid, "week": int(g.week), "period": p, "market": k, "book": U, "selection": U,
                                "line": U, "price": U, "actual": {"value": {"home": s[p][0], "away": s[p][1], "home_team": home, "away_team": away}, "source": pbp_src, "pulled_utc": PBP_PULLED},
                                "result": U, "reason": why, "projection_ready": False, "graded_utc": now})
        (OUT / f"{gid}.markets.jsonl").write_text("".join(json.dumps(r, sort_keys=True, default=str) + "\n" for r in out))
        graded = sorted({f"{p}:{k}" for p, k in have})
        nb = sorted({r["book"] for r in out if r["result"] != U and r["book"] != "consensus"})
        summary["per_game"][gid] = {"week": int(g.week), "final": {away: s["FT"][1], home: s["FT"][0]}, "kickoff_utc": kick.isoformat(),
                                    "quote_rows_graded": sum(r["result"] != U for r in out),
                                    "period_markets_graded": len(have), "period_markets_unknown": 21 - len(have),
                                    "graded_period_markets": graded, "named_books": nb}
    for gid, v in summary["per_game"].items():
        w = summary["per_week"].setdefault(str(v["week"]), {"games": 0, "period_markets_graded": 0, "period_markets_unknown": 0,
                                                            "quote_rows_graded": 0, "games_with_named_book_quotes": 0})
        w["games"] += 1; w["period_markets_graded"] += v["period_markets_graded"]; w["period_markets_unknown"] += v["period_markets_unknown"]
        w["quote_rows_graded"] += v["quote_rows_graded"]; w["games_with_named_book_quotes"] += bool(v["named_books"])
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1, sort_keys=True, default=str) + "\n")
    print(json.dumps({"per_week": summary["per_week"], "cross_check_failures": bad}, indent=1))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
