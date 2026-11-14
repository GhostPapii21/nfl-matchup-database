"""NFL-75 closing-line tracking: the primary scorecard for flagged legs (refs NFL-75).

Game-day closing-price pull *plan* for flagged legs only, plus CLV recording used in grading.
This module does not call The Odds API and does not import pregame/*.py. A paid pull is a documented
follow-up that would wire this plan into the existing pregame odds client. Until then, every path
is dry-run / fixture-only, so building and testing this module uses 0 Odds API credits.

Plan rules (applied BEFORE any pull, and printed first):
  - Estimate credits as n_markets * ceil(n_books / 10) per game (The Odds API event-odds pricing).
  - Refuse if remaining is unknown, or if remaining - estimate would drop below the Sunday 950
    credit reserve, or below the 800 hard floor. Meeting the 950 reserve implies the 800 floor.
  - Never print API keys (or apiKey= query values). Redact them from any status / error string.

CLV (memo item 6): same line and same book as the decision-time price. The no-vig-close EV is
    ev_at_close = p_nv_close * (dec_taken - 1) - (1 - p_nv_close)
A missing close, a different line, or a different book is status "unknown", never 0.

projection_ready stays false; this module does not write it.

FOLLOW-UP (not in this PR): wire plan_closing_pull / execute_closing_pull into pregame game-day
flow so a real Odds API event-odds fetch (flagged legs' markets only) runs after the printed plan
and credit check. Do not edit pregame/*.py in this change.
"""
from __future__ import annotations

import argparse
import math
import os
import re
import sys
from typing import Callable

import numpy as np
import pandas as pd

SUNDAY_RESERVE = 950
HARD_FLOOR = 800
DEFAULT_N_BOOKS = 5          # Pinnacle + FanDuel, DraftKings, Hard Rock, Caesars — one region-unit
DRY_RUN = True               # default: never a paid call

# Flagged-leg labels (same strings as calibration.selective_edge; kept local so this module
# does not depend on the frozen classifier file).
STRONG_UNDER = "STRONG UNDER"
ALT_LINE = "ALT-LINE CANDIDATE"
STANDARD = "STANDARD-LINE CANDIDATE"
CANDIDATE_LABELS = (STRONG_UNDER, ALT_LINE, STANDARD)

# selective-edge market names -> The Odds API event-odds market keys
MARKET_TO_ODDS = {
    "rushyds": "player_rush_yds",
    "rushatt": "player_rush_attempts",
    "rushrec": "player_rush_yds",          # rush+rec is not a native Odds API market; plan rush yds as a lower bound
    "recyds": "player_reception_yds",
    "rec": "player_receptions",
    "passyds": "player_pass_yds",
    "passatt": "player_pass_attempts",
    "cmp": "player_pass_completions",
}

# Explicit allowlist (the string "false" is not flagged).
_TRUE = {True, 1, "true", "1", "yes"}


def is_flagged_value(v) -> bool:
    if v is True or v == 1:
        return True
    return isinstance(v, str) and v.strip().lower() in {"true", "1", "yes"}


def flagged_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Flagged legs only. If a `flagged` column is present, it is the allowlist; otherwise a candidate label."""
    if df is None or len(df) == 0:
        return df.iloc[0:0].copy() if df is not None else pd.DataFrame()
    if "flagged" in df.columns:
        return df.loc[df["flagged"].map(is_flagged_value)].copy()
    if "label" in df.columns:
        return df.loc[df["label"].astype(str).isin(CANDIDATE_LABELS)].copy()
    return df.iloc[0:0].copy()


def redact(text) -> str:
    """Strip API keys and apiKey query values so they never appear in a printed plan or error."""
    s = "" if text is None else str(text)
    s = re.sub(r"(?i)(api[_-]?key\s*[=:]\s*)([^\s&\"']+)", r"\1***", s)
    # long token-looking values next to Odds / key wording
    env = os.environ.get("ODDS_API_KEY", "")
    if env and env in s:
        s = s.replace(env, "***")
    return s


def implied(american: float) -> float:
    a = float(american)
    if -100 < a < 100:
        raise ValueError(f"invalid American price {american!r}")
    return 100 / (a + 100) if a > 0 else -a / (-a + 100)


def devig(price_a: float, price_b: float) -> tuple[float, float, float]:
    """Two-way no-vig: (fair_a, fair_b, hold)."""
    pa, pb = implied(price_a), implied(price_b)
    return pa / (pa + pb), pb / (pa + pb), pa + pb - 1.0


def american_to_dec(american: float) -> float:
    a = float(american)
    if -100 < a < 100:
        raise ValueError(f"invalid American price {american!r}")
    return 1 + (a / 100.0) if a > 0 else 1 + (100.0 / -a)


def estimate_event_cost(n_markets: int, n_books: int = DEFAULT_N_BOOKS) -> int:
    """Upper-bound credits for one event-odds call: markets × region units (10 books = 1 unit)."""
    if n_markets <= 0:
        return 0
    return int(n_markets) * max(1, math.ceil(int(n_books) / 10))


def credit_allows(remaining, estimate: int, reserve: int = SUNDAY_RESERVE, floor: int = HARD_FLOOR) -> tuple[bool, str]:
    """Fail closed: unknown balance, or a pull that would leave fewer than `reserve` or `floor` credits, is refused."""
    if remaining is None:
        return False, "SKIPPED_UNKNOWN_BALANCE: credit balance unknown; paid call refused"
    try:
        rem = int(remaining)
        est = int(estimate)
    except (TypeError, ValueError):
        return False, "SKIPPED_UNKNOWN_BALANCE: credit balance unknown; paid call refused"
    after = rem - est
    # Check the stricter of the two thresholds; say which rule failed (reserve is the usual stopper).
    if after < reserve:
        return False, f"SKIPPED_SUNDAY_RESERVE: {rem} - {est} < reserve {reserve}"
    if after < floor:
        return False, f"SKIPPED_CREDIT_FLOOR: {rem} - {est} < floor {floor}"
    return True, f"OK: {rem} - {est} = {after} >= reserve {reserve} and floor {floor}"


def _odds_markets(markets) -> list[str]:
    out, seen = [], set()
    for m in markets:
        key = MARKET_TO_ODDS.get(str(m).strip(), None)
        if key and key not in seen:
            seen.add(key)
            out.append(key)
        elif not key and str(m).startswith("player_") and str(m) not in seen:
            seen.add(str(m))
            out.append(str(m))
    return out


def _book_from_price_source(src) -> str:
    if src is None or (isinstance(src, float) and not np.isfinite(src)):
        return ""
    s = str(src).strip()
    if s.lower().startswith("book:"):
        s = s.split(":", 1)[1]
    return s.strip().lower()


def plan_closing_pull(legs: pd.DataFrame, remaining_credits=None, n_books: int = DEFAULT_N_BOOKS,
                      reserve: int = SUNDAY_RESERVE, floor: int = HARD_FLOOR, dry_run: bool = DRY_RUN) -> dict:
    """Build and describe a game-day close pull for flagged legs only. Does not fetch.

    The returned plan always includes estimate_credits, remaining, remaining_after, allowed, reason, and
    a printable `report` that must be shown before any execute step.
    """
    flagged = flagged_rows(legs)
    games = []
    total = 0
    if len(flagged) and "game_id" in flagged.columns:
        for gid, g in flagged.groupby("game_id", dropna=False):
            mk = _odds_markets(g["market"].tolist() if "market" in g.columns else [])
            cost = estimate_event_cost(len(mk), n_books)
            total += cost
            games.append({"game_id": gid, "n_flagged_legs": int(len(g)), "markets": mk,
                          "n_markets": len(mk), "estimate_credits": cost})
    allowed, reason = credit_allows(remaining_credits, total, reserve=reserve, floor=floor)
    after = None if remaining_credits is None else (int(remaining_credits) - total)
    plan = {
        "schema": "nfl75-clv-close-plan/1",
        "flagged_legs_only": True,
        "n_flagged_legs": int(len(flagged)),
        "n_games": len(games),
        "games": games,
        "n_books": int(n_books),
        "estimate_credits": int(total),
        "remaining_credits": None if remaining_credits is None else int(remaining_credits),
        "remaining_after": after,
        "reserve": int(reserve),
        "floor": int(floor),
        "allowed": bool(allowed),
        "reason": reason,
        "dry_run": bool(dry_run),
        "credits_used": 0,
        "projection_ready": False,
        "follow_up": "Wiring this plan into pregame/*.py for a real Odds API pull is a follow-up; this PR does not edit pregame.",
    }
    plan["report"] = format_plan(plan)
    return plan


def format_plan(plan: dict) -> str:
    """Human-readable plan, including the credit estimate. Must be printed before any pull. Keys are redacted."""
    lines = [
        "CLOSING-LINE PULL PLAN (flagged legs only)",
        f"  games: {plan.get('n_games', 0)}   flagged legs: {plan.get('n_flagged_legs', 0)}",
        f"  books: {plan.get('n_books', DEFAULT_N_BOOKS)}   estimate: {plan.get('estimate_credits', 0)} credits",
        f"  remaining: {plan.get('remaining_credits')}   after: {plan.get('remaining_after')}",
        f"  Sunday reserve: {plan.get('reserve', SUNDAY_RESERVE)}   hard floor: {plan.get('floor', HARD_FLOOR)}",
        f"  decision: {'ALLOWED' if plan.get('allowed') else 'REFUSED'} — {plan.get('reason')}",
        f"  mode: {'DRY-RUN (no paid call; credits_used=0)' if plan.get('dry_run', True) else 'EXECUTE (injected fetch only)'}",
    ]
    for g in plan.get("games") or []:
        lines.append(f"    game {g.get('game_id')}: {g.get('n_flagged_legs')} legs, markets={g.get('markets')} "
                     f"-> {g.get('estimate_credits')} credits")
    lines.append(f"  follow-up: {plan.get('follow_up', '')}")
    return redact("\n".join(lines))


def execute_closing_pull(plan: dict, fetch: Callable | None = None, dry_run: bool | None = None) -> dict:
    """Run a close pull only after the plan (with cost) has been formed.

    Default dry_run=True: fetch is never called, credits_used stays 0.
    A live network client is intentionally not provided here (pregame follow-up). Even with
    dry_run=False, a pull happens only when `fetch` is injected and the plan was already allowed.
    The plan report is always included in the result so callers can print it first.
    """
    out = dict(plan)
    out["report"] = format_plan(out)
    use_dry = plan.get("dry_run", DRY_RUN) if dry_run is None else bool(dry_run)
    out["dry_run"] = use_dry
    if use_dry:
        out["status"] = "DRY_RUN"
        out["credits_used"] = 0
        out["closes"] = []
        return out
    if not plan.get("allowed"):
        out["status"] = "REFUSED"
        out["credits_used"] = 0
        out["closes"] = []
        return out
    if fetch is None:
        out["status"] = "NO_FETCH_INJECTED: no Odds API client in this module; pregame wiring is a follow-up"
        out["credits_used"] = 0
        out["closes"] = []
        return out
    closes = []
    for g in plan.get("games") or []:
        payload = fetch(g)
        if payload:
            closes.append(payload)
    out["status"] = "FETCHED_FIXTURE"
    out["credits_used"] = 0          # injected fetch is a fixture; this module never bills the API
    out["closes"] = closes
    return out


def _line_eq(a, b) -> bool:
    try:
        return abs(float(a) - float(b)) < 1e-9
    except (TypeError, ValueError):
        return False


def record_clv(legs: pd.DataFrame, closes: pd.DataFrame | None) -> pd.DataFrame:
    """Attach CLV columns for flagged legs. Unknown (missing / different line or book) is not written as 0.

    `closes` rows need: game_id, market, line, book, and either
      - p_nv_close already, plus american_close or dec_close, or
      - american_close and american_opp so no-vig can be computed for the taken side.
    A gsis or player column, when present on both frames, is part of the match. side is always matched.
    """
    out = legs.copy()
    for c in ("clv_status", "dec_taken", "dec_close", "p_nv_close", "ev_at_close",
              "close_american", "close_book", "close_line", "clv_note"):
        if c not in out.columns:
            out[c] = "" if c in ("clv_status", "clv_note", "close_book") else np.nan
    flag_idx = flagged_rows(out).index
    out.loc[out.index.difference(flag_idx), "clv_status"] = "not_flagged"
    if closes is None or len(closes) == 0:
        out.loc[flag_idx, "clv_status"] = "unknown"
        out.loc[flag_idx, "clv_note"] = "no closing price"
        return out

    def match_row(r):
        c = closes
        if "game_id" in c.columns:
            c = c[c.game_id.astype(str) == str(r.get("game_id"))]
        if "market" in c.columns and "market" in r.index:
            c = c[c.market.astype(str) == str(r.get("market"))]
        if "side" in c.columns and "side" in r.index:
            c = c[c.side.astype(str).str.lower() == str(r.get("side", "")).lower()]
        if "gsis" in c.columns and "gsis" in r.index and pd.notna(r.get("gsis")):
            c = c[c.gsis.astype(str) == str(r.get("gsis"))]
        elif "player" in c.columns and "player" in r.index and pd.notna(r.get("player")):
            c = c[c.player.astype(str).str.lower() == str(r.get("player", "")).lower()]
        if len(c) == 0:
            return "unknown", "no closing price", c
        book = _book_from_price_source(r.get("price_source") if "price_source" in r.index else r.get("book"))
        if book and "book" in c.columns:
            same_book = c[c.book.astype(str).str.lower() == book]
            if len(same_book) == 0:
                return "unknown", "different book or book missing", c.iloc[0:0]
            c = same_book
        # same line required
        if "line" in c.columns and "line" in r.index and pd.notna(r.get("line")):
            same_line = c[c.line.map(lambda x, want=r.get("line"): _line_eq(x, want))]
            if len(same_line) == 0:
                return "unknown", "different line", c.iloc[0:0]
            c = same_line
        if len(c) == 0:
            return "unknown", "no closing price", c
        return "ok", "", c.iloc[[0]]

    for i in flag_idx:
        r = out.loc[i]
        status, note, hit = match_row(r)
        dec_taken = r["dec"] if "dec" in r.index and pd.notna(r.get("dec")) else np.nan
        out.at[i, "dec_taken"] = dec_taken
        if status != "ok":
            out.at[i, "clv_status"] = "unknown"
            out.at[i, "clv_note"] = note
            # leave numeric CLV fields as NaN — never fill 0 for unknown
            continue
        h = hit.iloc[0]
        am = h["american_close"] if "american_close" in hit.columns and pd.notna(h.get("american_close")) else np.nan
        dec_close = h["dec_close"] if "dec_close" in hit.columns and pd.notna(h.get("dec_close")) else (
            american_to_dec(am) if pd.notna(am) else np.nan)
        p_nv = h["p_nv_close"] if "p_nv_close" in hit.columns and pd.notna(h.get("p_nv_close")) else np.nan
        if not np.isfinite(p_nv) and pd.notna(am) and "american_opp" in hit.columns and pd.notna(h.get("american_opp")):
            # taken side is price_a
            p_nv, _, _ = devig(am, float(h["american_opp"]))
        ev = np.nan
        if np.isfinite(p_nv) and np.isfinite(dec_taken):
            ev = float(p_nv) * (float(dec_taken) - 1.0) - (1.0 - float(p_nv))
        out.at[i, "clv_status"] = "ok"
        out.at[i, "clv_note"] = ""
        out.at[i, "dec_close"] = dec_close
        out.at[i, "p_nv_close"] = p_nv
        out.at[i, "ev_at_close"] = ev
        out.at[i, "close_american"] = am
        out.at[i, "close_book"] = h["book"] if "book" in hit.columns else book_or_empty(h)
        out.at[i, "close_line"] = h["line"] if "line" in hit.columns else r.get("line")
    return out


def book_or_empty(h) -> str:
    return h["book"] if "book" in getattr(h, "index", []) else ""


def _cli(argv=None) -> int:
    p = argparse.ArgumentParser(description="Plan a flagged-leg closing-price pull (dry-run; 0 credits).")
    p.add_argument("--legs", required=True, help="CSV of legs; only flagged / candidate-label rows are planned")
    p.add_argument("--remaining", type=int, default=None, help="Credits remaining (required to allow a pull)")
    p.add_argument("--n-books", type=int, default=DEFAULT_N_BOOKS)
    p.add_argument("--execute", action="store_true", help="Ignored without an injected fetch; still spends 0 credits")
    args = p.parse_args(argv)
    legs = pd.read_csv(args.legs)
    plan = plan_closing_pull(legs, remaining_credits=args.remaining, n_books=args.n_books, dry_run=not args.execute)
    # Print the plan (with cost) first, always.
    print(plan["report"])
    result = execute_closing_pull(plan, fetch=None, dry_run=not args.execute)
    if result["status"] != "DRY_RUN":
        print(redact(f"status={result['status']} credits_used={result['credits_used']}"))
    return 0 if (plan["allowed"] or plan["dry_run"]) else 2


if __name__ == "__main__":
    sys.exit(_cli())
