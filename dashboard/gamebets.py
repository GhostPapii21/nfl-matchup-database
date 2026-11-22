"""Best game bets: full game, halves and quarters; moneylines, spreads, totals and their alternate lines.

For every book's (market, side, line, price):
  model     dashboard/gamemodel.py: the 250 most similar real games by implied points; gives win / push / lose
  market    the fair (no-vig) chance at that line, conditional on no push: Pinnacle at that exact line if it posts it,
            else the median of 2+ books there; otherwise the nearest such line in the same market, shifted by the model on
            the logit scale (alternate spreads and totals are anchored to the market this way)
  bet       logit average of model and market (no-push chance), then the model's push chance is put back
  EV per $1 = p_win * (decimal - 1) - p_lose        (a push returns the stake)
Best bet per market (e.g. 1st-quarter spread) = highest EV. Pinnacle is the reference and never a pick. Long shots
(break-even under 20%) are never picked. Research only."""
from __future__ import annotations

import math
import statistics
from datetime import datetime, timedelta

from dashboard import gamemodel as G

EPS = 1e-4
MIN_BREAK_EVEN = 0.20
STALE_MIN = 180
PERIOD_LABEL = {"": "Game", "h1_": "1st half", "h2_": "2nd half", "q1_": "1st quarter", "q2_": "2nd quarter", "q3_": "3rd quarter", "q4_": "4th quarter"}


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


def _split(market):
    base = market.split("_")[-1]
    return market[: -len(base)], base


def _team(name, home, away):
    from pregame import sportsbooks as S
    n = str(name or "").lower()
    if n.upper() in (home, away):
        return n.upper()
    ab = S.ABBR.get(n) or S.team_of(n)
    return ab if ab in (home, away) else None


def normalize(rows, home, away):
    """Game-market rows -> {market, side (team code / Over / Under), line (bet side's view; None for moneyline), price, book, t}."""
    out = []
    for r in rows:
        m = r.get("market") or ""
        pre, base = _split(m)
        if base not in ("spread", "total", "moneyline") or pre not in G.PERIODS or r.get("player"):
            continue
        try:
            a = float(r["american"])
        except (KeyError, TypeError, ValueError):
            continue
        if abs(a) < 100:
            continue
        if base == "total":
            side = r.get("side") if r.get("side") in ("Over", "Under") else None
        else:
            side = _team(r.get("side"), home, away)
        line = None if base == "moneyline" else (float(r["line"]) if r.get("line") is not None else None)
        if side is None or (base != "moneyline" and line is None) or (base == "total" and line <= 0):
            continue
        out.append({"market": m, "side": side, "line": line, "american": a, "book": r.get("book"), "t": r.get("retrieved_utc"), "source": r.get("source")})
    newest = max((x for x in (_utc(r["t"]) for r in out) if x), default=None)
    if newest:
        out = [r for r in out if (_utc(r["t"]) or newest) >= newest - timedelta(minutes=STALE_MIN)]
    return out


def _key(r, home):
    """Market-side-invariant line key: totals by line; spreads from the home side; moneyline None."""
    pre, base = _split(r["market"])
    if base == "spread":
        return r["line"] if r["side"] == home else -r["line"]
    return r["line"]


def implied_points(norm, home):
    """(home_imp, away_imp) from the full-game main spread and total (the pair closest to even money, Pinnacle first)."""
    def main(market):
        pairs = {}
        for r in norm:
            if r["market"] == market:
                pairs.setdefault((r["book"], _key(r, home)), {})[r["side"]] = r["american"]
        best = None
        for (bk, k), s in pairs.items():
            if len(s) == 2:
                q = [implied(v) for v in s.values()]
                score = (bk != "pinnacle", abs(q[0] / sum(q) - 0.5))
                if best is None or score < best[0]:
                    best = (score, k)
        return best[1] if best else None
    sp, tot = main("spread"), main("total")
    if sp is None or tot is None:
        return None
    return (tot - sp) / 2, (tot + sp) / 2          # sp = home line (negative when home favored)


def game_best_bets(rows, home, away, nb=None, min_edge=0.0):
    norm = normalize(rows, home, away)
    imp = implied_points(norm, home)
    if not imp:
        return {"picks": [], "note": "no full-game spread and total posted yet"}
    nb = G.neighbors(*imp) if nb is None else nb
    by_market = {}
    for r in norm:
        by_market.setdefault(r["market"], []).append(r)
    picks = []
    for market, rs in by_market.items():
        pre, base = _split(market)
        # fair chance (no push) for the reference side at each line: home side for spread/moneyline, Over for totals
        ref_side = "Over" if base == "total" else home
        two = {}
        for r in rs:
            two.setdefault((r["book"], _key(r, home)), {})[r["side"]] = r["american"]
        fair = {}
        for (bk, k), s in two.items():
            if len(s) == 2 and ref_side in s:
                other = next(v for x, v in s.items() if x != ref_side)
                qa, qb = implied(s[ref_side]), implied(other)
                if 0 <= qa + qb - 1 <= 0.15:
                    fair.setdefault(k, {})[bk] = qa / (qa + qb)
        ref = {k: (f["pinnacle"] if "pinnacle" in f else statistics.median(f.values())) for k, f in fair.items() if "pinnacle" in f or len(f) >= 2}
        if not ref and fair:
            k0 = max(fair, key=lambda k: len(fair[k]))
            ref = {k0: statistics.median(fair[k0].values())}
        if not ref:
            continue

        def model_ref(k):
            line = k if base != "spread" else k                       # home-side line for spreads
            o = G.outcome(nb, market, ref_side, line if base != "moneyline" else None, home, away)
            return None if not o or o[0] + o[2] == 0 else o[0] / (o[0] + o[2])

        def market_ref(k):
            if k in ref:
                return ref[k]
            if base == "moneyline":
                return None
            near = min(ref, key=lambda x: abs((x or 0) - (k or 0)))
            m0, m1 = model_ref(near), model_ref(k)
            if m0 is None or m1 is None:
                return None
            return _sig(_logit(ref[near]) + _logit(m1) - _logit(m0))
        main_k = min(ref, key=lambda k: abs(ref[k] - 0.5))
        cands = []
        for r in rs:
            if r["book"] == "pinnacle":
                continue
            k = _key(r, home)
            o = G.outcome(nb, market, r["side"], r["line"], home, away)
            pm_ref = market_ref(k)
            if not o or pm_ref is None or o[0] + o[2] == 0:
                continue
            pw, pp, pl = o
            p_model = pw / (pw + pl)
            p_mkt = pm_ref if r["side"] == ref_side else 1 - pm_ref
            pb = _sig((_logit(p_model) + _logit(p_mkt)) / 2)
            win, lose = pb * (1 - pp), (1 - pb) * (1 - pp)
            be = implied(r["american"])
            ev = win * (decimal(r["american"]) - 1) - lose
            cands.append({"book": r["book"], "side": r["side"], "line": r["line"], "american": int(r["american"]), "break_even": round(be, 4),
                          "p_model": round(p_model, 3), "p_market": round(p_mkt, 3), "p_bet": round(pb, 3), "p_push": round(pp, 3),
                          "ev_per_dollar": round(ev, 4), "alt": k != main_k, "t": r["t"], "source": r["source"]})
        live = [c for c in cands if c["break_even"] >= MIN_BREAK_EVEN]
        if not live:
            continue
        best = max(live, key=lambda c: c["ev_per_dollar"])
        if best["ev_per_dollar"] < min_edge:
            continue
        fd = [c for c in cands if c["book"] == "fanduel" and c["side"] == best["side"] and not c["alt"]]
        flags = []
        if abs(best["p_model"] - best["p_market"]) > 0.12:
            flags.append(f"model {best['p_model']:.0%} vs market {best['p_market']:.0%}: a big disagreement, check news")
        picks.append({"market": market, "period": PERIOD_LABEL[pre], "kind": base, "best": best, "n_prices": len(cands),
                      "books": sorted({c["book"] for c in cands}), "main_line_home_or_over": main_k,
                      "vs_fanduel_main": ({"line": fd[0]["line"], "american": fd[0]["american"], "ev_gain": round(best["ev_per_dollar"] - fd[0]["ev_per_dollar"], 4)}
                                          if fd else None), "flags": flags})
    picks.sort(key=lambda x: (bool(x["flags"]), -x["best"]["ev_per_dollar"]))
    return {"picks": picks, "implied_points": {"home": round(imp[0], 1), "away": round(imp[1], 1)}, "neighbors": int(len(nb)),
            "method": "250 most similar games 2022-2026 by implied points, blended with the market's fair price at each line"}
