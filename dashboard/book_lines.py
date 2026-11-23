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
                    books[bk] = (ln, d, qo / (qo + qu))
        # a book whose only two-sided line is priced far from even (Bovada's +150/-200 rungs, research/bovada_2026-11-23)
        # is posting an alternate line, not a main line: listed separately, never in the main-line comparison
        alt_only = sorted(bk for bk, v in books.items() if v[1] > 0.10)
        books = {bk: v for bk, v in books.items() if v[1] <= 0.10}
        if not books:
            continue
        lines = {bk: v[0] for bk, v in sorted(books.items())}
        fairs = {bk: v[2] for bk, v in books.items()}
        med = statistics.median(lines.values())
        # a line far from every other book is usually a different market filed under this name (Bovada, Week 11): listed
        # but kept out of the median
        tol = 1.5 if base == "receptions" else max(8.0, 0.15 * med)
        odd = sorted(bk for bk, ln in lines.items() if abs(ln - med) > tol) if len(lines) >= 3 else []
        good = [ln for bk, ln in lines.items() if bk not in odd]
        cmed = statistics.median(good) if good else med
        near = sorted((abs(ln - cmed), bk) for bk, ln in lines.items() if bk not in odd)
        at = [fairs[bk] for dist, bk in near if dist == near[0][0]] if near else []
        out.setdefault(nm, {})[base] = {"books": lines, "median": cmed, "n": len(good),
                                       "fair_over": round(statistics.median(at), 3) if at else None,
                                       "fair_line": lines[near[0][1]] if near else None,
                                       "outliers": odd, "alt_only_books": alt_only, "alt_books": sorted({r["book"] for r in rs if r["alt"]})}
    return out


def attach(side: dict, rows: list[dict]) -> None:
    """Adds `book_lines` to each projected receiver and rusher: every book's main line and projection minus the median."""
    pl = player_lines(rows)
    opp = side.get("opportunity") or {}
    qb_note = _qb_depth_note(side)
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
                if kind == "receivers":
                    lean = catch_or_yards_lean(e, res)
                    if lean:
                        if qb_note:
                            lean["qb_depth"] = qb_note
                        e["lean"] = lean


LEAN_MIN = 0.05     # model-minus-market edge in one market at least 5 points bigger than in the other


def catch_or_yards_lean(e: dict, lines: dict) -> dict | None:
    """Reception lean vs yardage lean (asked after Week 11: Nabers 12 targets, 7 catches, 55 yards).

    edge = our chance of the over minus the market's fair chance, at the books' main line, for catches and for yards.
    Lean "receptions" when the catches edge is 5+ points better than the yards edge, "yards" the other way. It reads the
    model's own split between catches and yards per catch against the market's split. Week 11 check (71 receivers, tiny):
    reception leans had the catches over win 40% vs yards 20%; yardage leans had yards over 62% vs catches 54%.
    Tracked weekly (research/rec_vs_yards_2026-11-23); not yet validated."""
    from dashboard.bestbet import p_over
    r, y = lines.get("receptions"), lines.get("receiving_yards")
    if not r or not y or r.get("fair_over") is None or y.get("fair_over") is None:
        return None
    pr = p_over(e.get("receptions"), r["fair_line"], True)
    py = p_over(e.get("yards"), y["fair_line"], False)
    if pr is None or py is None:
        return None
    er, ey = pr - r["fair_over"], py - y["fair_over"]
    d = er - ey
    side = "receptions" if d >= LEAN_MIN else "yards" if d <= -LEAN_MIN else None
    return {"lean": side, "edge_receptions": round(er, 3), "edge_yards": round(ey, 3), "difference": round(d, 3),
            "receptions": {"line": r["fair_line"], "model": round(pr, 3), "market": r["fair_over"]},
            "yards": {"line": y["fair_line"], "model": round(py, 3), "market": y["fair_over"]}}


def _qb_depth_note(side: dict) -> str | None:
    """Context only: the starter throws 1+ yard shorter or deeper than the team's usual QB. On 2022-26 receiver-games a
    shorter thrower cut yards per catch about 2-5% and a deeper one added 4-17%; catch rate barely moved
    (research/rec_vs_yards_2026-11-23). Not applied to the projection."""
    q, qs = side.get("qb") or {}, [x for x in side.get("quarterbacks") or [] if x.get("games")]
    if not q.get("player") or len(qs) < 2:
        return None
    usual = max(qs, key=lambda x: x["games"])
    last = lambda n: str(n).replace(".", " ").split()[-1].lower()
    st = next((x for x in qs if last(x["player"]) == last(q["player"])), None)
    if not st or st is usual or st.get("avg_depth_of_target") is None or usual.get("avg_depth_of_target") is None:
        return None
    d = st["avg_depth_of_target"] - usual["avg_depth_of_target"]
    if abs(d) < 1.0:
        return None
    return (f"{q['player']} throws {abs(d):.1f} yards {'shorter' if d < 0 else 'deeper'} than {usual['player']}: "
            f"{'fewer yards per catch, catches hold' if d < 0 else 'more yards per catch'}")
