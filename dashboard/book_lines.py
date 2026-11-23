"""Every book's main line for each player prop, set against the board's projection.

For each player and market (receiving yards, rushing yards, receptions) and each book: the main line is the book's
two-sided line (Over and Under both posted) whose no-vig Over chance is nearest 50%. Alt ladders are listed by book
(only books whose own feed we pull carry them: FanDuel today). The comparison is the projection's median minus the
median of the books' main lines. Prices pulled 3+ hours before the newest for that prop are dropped as stale.
Research only."""
from __future__ import annotations

import statistics
from datetime import timedelta

from dashboard.bestbet import STALE_MIN, _norm, _utc, implied

MARKETS = ("receiving_yards", "rushing_yards", "receptions")
SHOWN = ("draftkings", "betmgm", "williamhill_us", "fanduel")      # columns on the board; the rest count in the median


def player_lines(rows: list[dict]) -> dict:
    """{norm player: {market: {"books": {book: line}, "median": x, "n": k, "alt_books": [...]}}}"""
    by = {}
    for r in rows:
        m = r.get("market") or ""
        base = m.replace("alt_", "")
        if base not in MARKETS or not r.get("player") or r.get("line") is None or r.get("side") not in ("Over", "Under"):
            continue
        try:
            line, a = float(r["line"]), float(r["american"])
        except (KeyError, TypeError, ValueError):
            continue
        by.setdefault((_norm(r["player"]), base), []).append(dict(r, line=line, american=a, alt=m.startswith("alt_")))
    out = {}
    for (nm, base), rs in by.items():
        newest = max((t for t in (_utc(r.get("retrieved_utc")) for r in rs) if t), default=None)
        if newest:
            rs = [r for r in rs if (_utc(r.get("retrieved_utc")) or newest) >= newest - timedelta(minutes=STALE_MIN)]
        two = {}
        for r in rs:
            if not r["alt"]:
                two.setdefault((r["book"], r["line"]), {})[r["side"]] = r["american"]
        books = {}
        for (bk, ln), s in two.items():
            if "Over" in s and "Under" in s:
                qo, qu = implied(s["Over"]), implied(s["Under"])
                d = abs(qo / (qo + qu) - 0.5)
                if bk not in books or d < books[bk][1]:
                    books[bk] = (ln, d)
        if not books:
            continue
        lines = {bk: v[0] for bk, v in sorted(books.items())}
        med = statistics.median(lines.values())
        # a line far from every other book is usually a different market filed under this name (Bovada, Week 11): listed
        # but kept out of the median
        tol = 1.5 if base == "receptions" else max(8.0, 0.15 * med)
        odd = sorted(bk for bk, ln in lines.items() if abs(ln - med) > tol) if len(lines) >= 3 else []
        good = [ln for bk, ln in lines.items() if bk not in odd]
        out.setdefault(nm, {})[base] = {"books": lines, "median": statistics.median(good) if good else med, "n": len(good),
                                       "outliers": odd, "alt_books": sorted({r["book"] for r in rs if r["alt"]})}
    return out


def attach(side: dict, rows: list[dict]) -> None:
    """Adds `book_lines` to each projected receiver and rusher: every book's main line and projection minus the median."""
    pl = player_lines(rows)
    opp = side.get("opportunity") or {}
    for kind, market in (("receivers", "receiving_yards"), ("rushers", "rushing_yards")):
        for e in opp.get(kind) or []:
            if e.get("status"):
                continue
            mk = pl.get(_norm(e.get("player"))) or {}
            res = {}
            for m in ((market, "receptions") if kind == "receivers" else (market,)):
                x = mk.get(m)
                if not x:
                    continue
                proj = e.get("yards_median") if m != "receptions" else e.get("receptions_mean")
                res[m] = dict(x, model=proj, model_minus_median=None if proj is None else round(proj - x["median"], 1))
            if res:
                e["book_lines"] = res
