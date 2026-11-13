"""Pure grading maths: prices, closing line, CLV, volume support, holdout record and the edge rule.

Rules that hold everywhere in this module:
  * Missing data is the string "unknown", never 0 and never estimated.
  * Every reported figure travels with the source it came from and the time that source was pulled.
  * Nothing here changes a model weight or formula; it only reads what the pregame packet already says.
"""
from __future__ import annotations

import math
from datetime import datetime, timezone

UNKNOWN = "unknown"
RESEARCH_LABEL = "research only, not validated"

# Which packet volume field backs each market type (Rico item 6, condition 2).
VOLUME_FOR = {
    "receiving_yards": "targets", "receptions": "targets", "targets": "targets",
    "rushing_yards": "carries", "carries": "carries", "rush_attempts": "carries",
    "passing_yards": "pass_attempts", "pass_attempts": "pass_attempts", "completions": "pass_attempts",
}
TEAM_MARKETS = ("spread", "total", "moneyline")


def known(x) -> bool:
    if x is None or x == UNKNOWN:
        return False
    if isinstance(x, float) and math.isnan(x):
        return False
    return True


def u(x):
    """Normalise a missing value to "unknown"."""
    return x if known(x) else UNKNOWN


def fig(value, source=None, pulled_utc=None, **extra) -> dict:
    """A reported figure with its provenance. Missing value, source or time all read "unknown"."""
    out = {"value": u(value), "source": u(source), "pulled_utc": u(pulled_utc)}
    out.update({k: u(v) for k, v in extra.items()})
    return out


def parse_utc(s) -> datetime | None:
    if not known(s):
        return None
    try:
        d = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except ValueError:
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def break_even(price):
    """Implied probability of an American price (the win rate needed to break even). Unknown in, unknown out."""
    if not known(price):
        return UNKNOWN
    p = float(price)
    if p == 0:
        return UNKNOWN
    return round(-p / (-p + 100.0), 4) if p < 0 else round(100.0 / (p + 100.0), 4)


def no_vig(prices: dict, side: str):
    """Two-way proportional de-vig of one book's own prices. Needs both sides; otherwise unknown."""
    if not isinstance(prices, dict) or side not in prices or len(prices) != 2:
        return UNKNOWN
    imps = {s: break_even(p) for s, p in prices.items()}
    if not all(known(v) for v in imps.values()):
        return UNKNOWN
    tot = sum(imps.values())
    return round(imps[side] / tot, 4) if tot > 0 else UNKNOWN


def side_line(market: str, line, side: str, home: str):
    """The line from the bettor's side. Spread lines are stored as the home team's handicap."""
    if not known(line):
        return UNKNOWN if market != "moneyline" else None
    if market == "spread":
        return float(line) if side == home else -float(line)
    return float(line)


def same_line(a, b) -> bool:
    if a is None and b is None:
        return True
    return known(a) and known(b) and abs(float(a) - float(b)) < 1e-9


# ---------------------------------------------------------------- snapshots and closing line
def closing_quote(snapshots: list[dict], market_key: str, book: str, kickoff: datetime):
    """Latest saved quote for this market and book strictly before kickoff, or None (closing line unknown).

    A snapshot is {market_key, book, line, prices, snapshot_utc, source, quote_utc}. "Closing" means the last
    snapshot this repository saved before kickoff; it is not claimed to be the true market close.
    """
    best = None
    for s in snapshots:
        if s.get("market_key") != market_key or s.get("book") != book:
            continue
        t = parse_utc(s.get("snapshot_utc"))
        if t is None or t >= kickoff:
            continue
        if best is None or t > parse_utc(best["snapshot_utc"]):
            best = s
    return best


def clv(market: str, side: str, home: str, bet_line, bet_prices: dict, close: dict | None, bet_utc=None) -> dict:
    """Closing-line value of a bet against the latest pre-kickoff snapshot from the same book.

    line_points: points gained versus the close from the bettor's side (positive = beat the close).
    prob: closing no-vig probability minus bet-time no-vig probability, only when the line did not move.
    positive: True / False, or "unknown" when the close is unknown or nothing can be compared.
    bet_utc: when given, the close must be a snapshot saved strictly after the bet quote; otherwise CLV is
    unknown (a bet compared with itself would read as a zero-CLV tie and bias the holdout).
    """
    if not close or not known(side):
        return {"line_points": UNKNOWN, "prob": UNKNOWN, "positive": UNKNOWN,
                "reason": "closing line unknown (no saved pre-kickoff snapshot for this book)" if not close else "side unknown"}
    bt, ct = parse_utc(bet_utc), parse_utc(close.get("snapshot_utc"))
    if bet_utc is not None and (bt is None or ct is None or ct <= bt):
        return {"line_points": UNKNOWN, "prob": UNKNOWN, "positive": UNKNOWN,
                "reason": "no saved snapshot later than the bet quote; CLV cannot be measured"}
    bl = side_line(market, bet_line, side, home)
    cl = side_line(market, close.get("line"), side, home)
    if market == "moneyline":
        pts = 0.0
    elif not (known(bl) and known(cl)):
        return {"line_points": UNKNOWN, "prob": UNKNOWN, "positive": UNKNOWN, "reason": "bet or closing line unknown"}
    elif market == "spread":
        pts = round(bl - cl, 2)
    elif side == "Over":
        pts = round(cl - bl, 2)
    elif side == "Under":
        pts = round(bl - cl, 2)
    else:
        return {"line_points": UNKNOWN, "prob": UNKNOWN, "positive": UNKNOWN, "reason": f"side {side} not gradable"}
    prob = UNKNOWN
    if pts == 0:
        a, b = no_vig(close.get("prices") or {}, side), no_vig(bet_prices or {}, side)
        if known(a) and known(b):
            prob = round(a - b, 4)
    if pts > 0:
        pos = True
    elif pts < 0:
        pos = False
    elif known(prob):
        pos = prob > 0
    else:
        pos = UNKNOWN
    return {"line_points": pts if market != "moneyline" else UNKNOWN, "prob": prob, "positive": pos, "reason": ""}


def best_retail_break_even(books: dict, market: str, side: str, line, home: str, reference_books) -> dict:
    """Lowest break-even among retail books quoting exactly this line for this side (reference books excluded)."""
    best = None
    for bk, q in (books or {}).items():
        if bk in reference_books or not isinstance(q, dict):
            continue
        ql = q.get("line")
        if market == "moneyline":
            ok = True
        else:
            ok = known(ql) and known(line) and same_line(side_line(market, ql, side, home), side_line(market, line, side, home))
        price = (q.get("prices") or {}).get(side)
        be = break_even(price)
        if ok and known(be) and (best is None or be < best["break_even"]):
            best = {"break_even": be, "book": bk, "price": price}
    return best or {"break_even": UNKNOWN, "book": UNKNOWN, "price": UNKNOWN}


# ---------------------------------------------------------------- results
def prop_result(actual, side, line):
    if not (known(actual) and known(line)) or side not in ("Over", "Under"):
        return UNKNOWN
    a, l = float(actual), float(line)
    if a == l:
        return "push"
    return "win" if (a > l) == (side == "Over") else "loss"


def spread_result(home_score, away_score, home_line, side, home):
    if not (known(home_score) and known(away_score) and known(home_line)) or not known(side):
        return UNKNOWN
    m = float(home_score) + float(home_line) - float(away_score)
    if m == 0:
        return "push"
    return "win" if (m > 0) == (side == home) else "loss"


def moneyline_result(home_score, away_score, side, home):
    if not (known(home_score) and known(away_score)) or not known(side):
        return UNKNOWN
    if home_score == away_score:
        return "push"
    return "win" if (home_score > away_score) == (side == home) else "loss"


# ---------------------------------------------------------------- edge rule
def volume_check(baseline: dict | None, stat: str, side, line, min_games: int) -> dict:
    """Condition 2: does the packet's projected volume support the number?

    Rate = the player's own stat per unit of volume from the same packet baseline (weighted means); the volume
    needed to reach the line is line / rate. An Over is supported only if the player's median game volume (p50)
    is above that; an Under only if it is below. Any missing field, or fewer than min_games of volume history,
    fails the check (never assumed).
    """
    def fail(reason):
        return {"supports": False, "reason": reason, "volume_field": VOLUME_FOR.get(stat, UNKNOWN),
                "volume_p50": UNKNOWN, "needed_volume": UNKNOWN}
    vf = VOLUME_FOR.get(stat)
    if vf is None:
        return fail(f"no volume field defined for market type {stat}")
    if not baseline:
        return fail("no packet baseline for this player")
    if side not in ("Over", "Under") or not known(line):
        return fail("side or line unknown")
    vol = baseline.get(vf)
    if not isinstance(vol, dict):
        return fail(f"packet has no {vf} volume for this player")
    games, p50, vmean = vol.get("games"), vol.get("p50"), vol.get("weighted_mean")
    if not (known(games) and known(p50) and known(vmean)):
        return fail(f"{vf} volume incomplete in packet (games/p50/weighted_mean)")
    if games < min_games:
        return fail(f"only {games} games of {vf} history (minimum {min_games})")
    if stat == vf or stat == "rush_attempts":
        rate = 1.0
    else:
        st = baseline.get(stat)
        smean = st.get("weighted_mean") if isinstance(st, dict) else None
        if not known(smean) or float(vmean) <= 0:
            return fail(f"packet has no {stat} baseline to convert volume")
        rate = float(smean) / float(vmean)
    if rate <= 0:
        return fail("non-positive per-opportunity rate")
    needed = round(float(line) / rate, 2)
    ok = float(p50) > needed if side == "Over" else float(p50) < needed
    return {"supports": bool(ok), "volume_field": vf, "volume_p50": p50, "needed_volume": needed,
            "reason": f"{side}: median {vf} {p50} vs {needed} needed at line {line} -> "
                      + ("supports" if ok else "does not support")}


def clv_record(rows: list[dict], market_type: str, before: datetime, exclude_game: str, min_n: int) -> dict:
    """Condition 3: closing-line record for one market type over the holdout.

    Holdout = props graded in earlier games only (kickoff before this game, this game excluded), one entry per
    (game, market, side): the quote with the lowest bet break-even. Record is positive only when at least min_n
    such props have a known CLV and more of them beat the close than did not.
    """
    picked = {}
    for r in rows:
        if r.get("kind") != "flagged_prop" or r.get("market_type") != market_type or r.get("game_id") == exclude_game:
            continue
        t = parse_utc(r.get("kickoff_utc"))
        if t is None or t >= before:
            continue
        pos = (r.get("clv") or {}).get("positive")
        if pos not in (True, False):
            continue
        key = (r["game_id"], r.get("market_key"), r.get("side"))
        be = (r.get("bet_break_even") or {}).get("value")
        be = be if known(be) else 9.0
        if key not in picked or be < picked[key][0]:
            picked[key] = (be, pos)
    n = len(picked)
    beat = sum(1 for _, p in picked.values() if p is True)
    ready = n >= min_n
    return {"market_type": market_type, "n": n, "beat_close": beat, "did_not_beat": n - beat, "min_n": min_n,
            "holdout_ready": ready, "positive": bool(ready and beat > n - beat)}


def edge_decision(model_prob, best_be, volume: dict, record: dict, labels: dict | None = None) -> dict:
    """The edge-label rule, exactly: edge only if all three conditions hold. Unknown never passes."""
    labels = labels or {}
    c1 = known(model_prob) and known(best_be) and float(model_prob) > float(best_be)
    c2 = (volume or {}).get("supports") is True
    c3 = (record or {}).get("positive") is True and (record or {}).get("holdout_ready") is True
    edge = bool(c1 and c2 and c3)
    if edge:
        label = labels.get("edge_label", "edge")
    elif not (record or {}).get("holdout_ready"):
        label = labels.get("research_label", RESEARCH_LABEL)
    else:
        label = labels.get("not_edge_label", "not an edge")
    return {
        "c1_model_beats_best_retail_break_even": {"pass": c1, "model_prob": u(model_prob), "best_retail_break_even": u(best_be)},
        "c2_volume_supports_number": {"pass": c2, **(volume or {"reason": "not evaluated"})},
        "c3_positive_clv_record_on_holdout": {"pass": c3, **(record or {"reason": "not evaluated"})},
        "edge": edge, "label": label,
    }
