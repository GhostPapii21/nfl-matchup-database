"""Best-bet finder: for every player prop, every book's line and price, our probability at that exact line, and the single
best bet.

For each (player, market) and each book's (line, side, price):
  p_model   the board's simulated chance at that exact line (opportunity chance tables, calibrated; interpolated on the
            logit scale between table lines; integer stats read directly: over 4.5 receptions = P(5 or more))
  p_market  the market's fair (no-vig) chance at that line: Pinnacle if it posts that line, else the median of 2+ books
            that post it two-sided (one book alone is never "the market"); otherwise the nearest such line is shifted by our model's
            shape on the logit scale: logit p_market(L) = logit p_market(L0) + logit p_model(L) - logit p_model(L0)
  p_bet     average of p_model and p_market on the logit scale (the model alone lost money in testing; the blend did not)
  edge      p_bet - break_even(price);   EV per $1 = p_bet * decimal_odds - 1
The best bet per prop is the candidate with the highest EV. Line shopping shows up as a better line at the same price,
price shopping as a better price at the same line.

Prices pulled 3+ hours before the newest price for the same prop are dropped as not live; long shots (break-even under
20%) are never the pick. Alt-ladder rungs can be picked: their market chance is the book's own ladder price less the
ladder's vig (measured at the rung nearest the main line), so our tails never set the price. Unders carry a 3-point
handicap in the ranking (owner's preference: alt lines and overs over plain unders). Timing flags: every price carries its pull time. A pick is flagged when (a) the books it is compared with were pulled more
than 30 minutes apart, or (b) its line differs from the market's main line by 3+ (yards) / 1+ (receptions, carries) and it
came through an aggregator (StartWho) or the Grok files rather than the book's own feed: confirm it on the book first.
Research only."""
from __future__ import annotations

import math
import re
import statistics
from datetime import datetime, timedelta

MODEL = {"receiving_yards": ("receivers", "yards"), "alt_receiving_yards": ("receivers", "yards"), "receptions": ("receivers", "receptions"),
         "rushing_yards": ("rushers", "yards"), "alt_rushing_yards": ("rushers", "yards"), "carries": ("rushers", "carries")}
INTEGER = {"receptions", "carries"}
OWN_FEED = {"fanduel", "pinnacle"}          # pulled from the book's own site; others in direct_lines come through StartWho
GAP = {"yards": 3.0, "receptions": 1.0, "carries": 1.0}
MAX_SPREAD_MIN = 30
STALE_MIN = 180          # a price pulled 3+ hours before the newest pull for the same prop is not treated as live
MIN_BREAK_EVEN = 0.20
ROLE_GAP = 0.15
UNDER_PENALTY = 0.03     # owner's preference: an under is picked over an over/alt line only when it is clearly better
LADDER_DEFAULT = 1.08    # alt-ladder overround when it cannot be measured          # model vs market at the main line; bigger than this is usually a role/injury read, which lost money in testing    # long shots (+400 and longer) are listed in the counts but never chosen as the pick
EPS = 1e-4


def _norm(s):
    return " ".join(w for w in re.sub(r"[^a-z ]", "", str(s or "").lower().replace("-", " ")).split() if w not in {"jr", "sr", "ii", "iii", "iv", "v"})


def _logit(p):
    p = min(max(p, EPS), 1 - EPS)
    return math.log(p / (1 - p))


def _sig(z):
    return 1 / (1 + math.exp(-z))


def implied(a):
    a = float(a)
    return 100 / (a + 100) if a > 0 else -a / (-a + 100)


def decimal(a):
    a = float(a)
    return 1 + (a / 100 if a > 0 else 100 / -a)


def _utc(s):
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


def p_over(table: dict | None, line: float, integer: bool) -> float | None:
    """P(stat > line) from a chance table {threshold: P(stat >= threshold)}; None outside the table's range."""
    if not table:
        return None
    pts = sorted((float(k), v) for k, v in table.items() if v is not None)
    if not pts:
        return None
    if integer:
        k = math.floor(line) + 1
        hit = [v for t, v in pts if t == k]
        return float(hit[0]) if hit else None
    x = line + 0.5 if float(line).is_integer() else line            # whole-number line: over needs line + 1
    if x < pts[0][0] or x > pts[-1][0]:
        return None
    for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
        if t0 <= x <= t1:
            if t1 == t0:
                return float(v0)
            w = (x - t0) / (t1 - t0)
            return _sig((1 - w) * _logit(v0) + w * _logit(v1))
    return float(pts[-1][1]) if x == pts[-1][0] else None


def _model_entries(side: dict) -> dict:
    opp = side.get("opportunity") or {}
    out = {}
    for kind in ("receivers", "rushers"):
        for e in opp.get(kind) or []:
            if e.get("status"):
                continue
            out.setdefault(_norm(e.get("player")), {})[kind] = e
    return out


def r_is_ladder(c):
    """Alt-ladder rungs (anchored to the book's own ladder) may be picked; one-sided rungs inside a main market may not."""
    return bool(c.get("ladder"))


def _source(r):
    return "grok" if r.get("source") == "grok" else ("own feed" if r.get("book") in OWN_FEED else "StartWho")


def side_best_bets(side: dict, rows: list[dict], min_edge: float = 0.0) -> dict:
    """Best bet per player prop for one board side. `rows` are pregame.direct_books.load_rows() rows for the game."""
    ents = _model_entries(side)
    by = {}
    for r in rows:
        m = r.get("market")
        if m not in MODEL or r.get("side") not in ("Over", "Under") or r.get("line") is None or r.get("american") is None:
            continue
        nm = _norm(r.get("player"))
        kind, stat = MODEL[m]
        ent = (ents.get(nm) or {}).get(kind)
        if not ent:
            continue
        base = m.replace("alt_", "")
        by.setdefault((nm, base), {"entry": ent, "stat": stat, "rows": []})["rows"].append(dict(r, line=float(r["line"]), american=float(r["american"])))
    picks = []
    for (nm, base), g in by.items():
        ent, stat, rs = g["entry"], g["stat"], g["rows"]
        newest = max((t for t in (_utc(r.get("retrieved_utc")) for r in rs) if t), default=None)
        if newest:
            rs = [r for r in rs if (_utc(r.get("retrieved_utc")) or newest) >= newest - timedelta(minutes=STALE_MIN)]
        table, integer = ent.get(stat), stat in INTEGER or base in INTEGER
        # market fair chance at each two-sided line (main markets only)
        two = {}
        for r in rs:
            if not r["market"].startswith("alt_"):
                two.setdefault((r["book"], r["line"]), {})[r["side"]] = r["american"]
        fair = {}
        for (bk, ln), s in two.items():
            if "Over" in s and "Under" in s:
                qo, qu = implied(s["Over"]), implied(s["Under"])
                if 0 <= qo + qu - 1 <= 0.15:
                    fair.setdefault(ln, {})[bk] = qo / (qo + qu)
        if not fair:
            continue
        main = max(fair, key=lambda ln: (len(fair[ln]), "pinnacle" in fair[ln]))
        # reference lines: Pinnacle's, and any line two or more books post; a lone book's own price is never "the market"
        ref = {ln: (f["pinnacle"] if "pinnacle" in f else statistics.median(f.values())) for ln, f in fair.items() if "pinnacle" in f or len(f) >= 2}
        if not ref:
            ref = {main: statistics.median(fair[main].values())}

        def mkt_over(ln):
            if ln in ref:
                return ref[ln]
            near = min(ref, key=lambda x: abs(x - ln))
            p0, p1 = p_over(table, near, integer), p_over(table, ln, integer)
            if p0 is None or p1 is None:
                return None
            return _sig(_logit(ref[near]) + _logit(p1) - _logit(p0))     # shift on the logit scale: tails stay sane
        times = [t for t in (_utc(r.get("retrieved_utc")) for r in rs) if t]
        spread_min = (max(times) - min(times)).total_seconds() / 60 if times else None
        # alt ladders: each book's rungs are anchored to the book's own ladder (its price less the ladder's measured vig),
        # not to our tails. The vig is measured at the rung nearest the market's main line.
        ladder = {}
        for bk in {r["book"] for r in rs if r["market"].startswith("alt_")}:
            rungs = [r for r in rs if r["book"] == bk and r["market"].startswith("alt_") and r["side"] == "Over"]
            r0 = min(rungs, key=lambda r: abs(r["line"] - main))
            fair0 = mkt_over(r0["line"])
            ladder[bk] = min(max(implied(r0["american"]) / fair0, 1.0), 1.25) if fair0 and abs(r0["line"] - main) <= 10 else LADDER_DEFAULT
        cands = []
        for r in rs:
            if r["book"] == "pinnacle":
                continue
            po = p_over(table, r["line"], integer)
            pm = mkt_over(r["line"])
            if r["market"].startswith("alt_") and r["side"] == "Over":
                pm = min(0.99, implied(r["american"]) / ladder.get(r["book"], LADDER_DEFAULT))
            if po is None or pm is None:
                continue
            pmod, pmk = (po, pm) if r["side"] == "Over" else (1 - po, 1 - pm)
            pb = _sig((_logit(pmod) + _logit(pmk)) / 2)
            be = implied(r["american"])
            cands.append({"book": r["book"], "side": r["side"], "line": r["line"], "american": int(r["american"]), "break_even": round(be, 4),
                          "p_model": round(pmod, 3), "p_market": round(pmk, 3), "p_bet": round(pb, 3), "edge": round(pb - be, 4),
                          "ev_per_dollar": round(pb * decimal(r["american"]) - 1, 4), "source": _source(r), "retrieved_utc": r.get("retrieved_utc"),
                          "alt": r["market"].startswith("alt_") or "Over" not in two.get((r["book"], r["line"]), {}) or "Under" not in two.get((r["book"], r["line"]), {}),
                          "ladder": r["market"].startswith("alt_")})
        if not cands:
            continue
        live = [c for c in cands if c["break_even"] >= MIN_BREAK_EVEN and (not c["alt"] or r_is_ladder(c))]
        if not live:
            continue
        best = max(live, key=lambda c: c["ev_per_dollar"] - (UNDER_PENALTY if c["side"] == "Under" else 0.0))
        if best["edge"] < min_edge:
            continue
        same = [c for c in cands if c["side"] == best["side"] and c["line"] == best["line"] and not c["alt"]]
        fd = next((c for c in cands if c["book"] == "fanduel" and c["side"] == best["side"] and not c["alt"] and c["line"] == main), None)
        flags = []
        if spread_min is not None and spread_min > MAX_SPREAD_MIN:
            flags.append(f"prices pulled {spread_min:.0f} min apart")
        pm_main, pk_main = p_over(table, main, integer), mkt_over(main)
        role_gap = None if pm_main is None or pk_main is None else pm_main - pk_main
        if role_gap is not None and abs(role_gap) > ROLE_GAP:
            flags.append(f"model and market disagree on his role (model {pm_main:.0%} vs market {pk_main:.0%} over {main:g}): check injury news and his role before betting")
        gap = abs(best["line"] - main)
        if gap >= GAP["yards" if stat == "yards" else stat] and best["source"] != "own feed":
            flags.append(f"line {best['line']:g} vs market {main:g} came via {best['source']}: confirm on {best['book']}")
        picks.append({"player": ent.get("player"), "player_id": ent.get("player_id"), "pos": ent.get("pos"), "market": base, "best": best,
                      "market_line": main, "market_fair_over_at_main": round(mkt_over(main), 3), "books": sorted({c["book"] for c in cands}),
                      "n_prices": len(cands), "same_line_prices": len(same),
                      "vs_fanduel_main": ({"fanduel_line": fd["line"], "fanduel_american": fd["american"], "ev_gain": round(best["ev_per_dollar"] - fd["ev_per_dollar"], 4)}
                                          if fd else None),
                      "flags": flags})
    picks.sort(key=lambda x: (bool(x["flags"]), -x["best"]["ev_per_dollar"]))      # clean picks first
    return {"picks": picks, "method": "p_bet = logit average of model and market fair chance at the exact line; best = highest EV per $1"}
