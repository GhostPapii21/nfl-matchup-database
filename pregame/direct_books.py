"""Book prices for the packet and the game-day gate from the free direct pulls (pregame/direct_lines/) and, when present,
the Grok bots' files (pregame/grok_lines/). No Odds API credits.

Reliability rules applied to every price before it is used:
  1. Valid American odds only (|odds| >= 100) and a two-sided pair at the same line for main markets.
  2. Hold sanity: 0 <= hold <= 15% on a two-sided pair (hold = p_over + p_under - 1). Outside that = a bad read, dropped.
  3. Outlier guard: at one line, a book whose no-vig probability is more than 0.12 from the median of the other books
     (with at least 2 others) is dropped as a stale or mistyped price.
  4. Freshness: a book counts only if its own retrieval time is known; the freeze is stamped with the OLDEST retrieval
     among the gate's required books, so the gate's age limit applies to the stalest book it relies on.
Consensus at a line = mean no-vig probability of the books at the modal line (same line only; lines are never averaged).
"""
from __future__ import annotations

import argparse
import json
import statistics
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECT, GROK = ROOT / "pregame" / "direct_lines", ROOT / "pregame" / "grok_lines"
BOOK_KEY = {"caesars": "williamhill_us", "williamhill": "williamhill_us", "hardrock": "hardrockbet", "hardrocksportsbook": "hardrockbet"}
MARKET_LABEL = {"receptions": "receptions", "receiving_yards": "receiving_yards", "rushing_yards": "rushing_yards",
                "rush_rec_yards": "rush_rec_yards"}
MAX_HOLD, OUTLIER = 0.15, 0.12


def implied(a: float) -> float:
    a = float(a)
    return 100 / (a + 100) if a > 0 else -a / (-a + 100)


def _utc(s):
    try:
        d = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return None


def load_rows(game_id: str, direct: Path = DIRECT, grok: Path = GROK) -> list[dict]:
    """Every usable row for one game, each stamped with its own retrieval time and source."""
    out = []
    for src, base in (("direct", direct), ("grok", grok)):
        f = base / f"{game_id}.json"
        if not f.exists():
            continue
        try:
            d = json.loads(f.read_text())
        except ValueError:
            continue
        per_book = {k: (v or {}).get("retrieved_utc") for k, v in (d.get("books") or {}).items()} if src == "grok" else {}
        for r in d.get("rows") or []:
            try:
                a = float(r["american"])
            except (KeyError, TypeError, ValueError):
                continue
            if abs(a) < 100 or r.get("side") is None:
                continue
            book = str(r.get("book", "")).lower()
            out.append(dict(r, book=BOOK_KEY.get(book, book), american=a, source=src,
                            retrieved_utc=per_book.get(book) or d.get("retrieved_utc")))
    # One source per book: keep only that book's newest pull, so an older file never drags a fresh book's age up
    newest = {}
    for r in out:
        t = _utc(r["retrieved_utc"])
        if t and (r["book"] not in newest or t > newest[r["book"]][0]):
            newest[r["book"]] = (t, r["source"])
    return [r for r in out if r["book"] in newest and r["source"] == newest[r["book"]][1]]


def _team(name, home, away):
    from pregame import sportsbooks as S
    n = str(name or "").lower()
    ab = S.ABBR.get(n) or S.team_of(n)
    return ab if ab in (home, away) else None


def pairs(rows: list[dict], home: str, away: str) -> list[dict]:
    """Two-sided pairs: {label, line, book, sides, prices, retrieved_utc, source}. Alt (one-sided) rungs are skipped."""
    grp = {}
    for r in rows:
        m = r.get("market")
        if m in MARKET_LABEL and r.get("player"):
            label, side = f"{MARKET_LABEL[m]}|{r['player']}", r["side"]
        elif m == "total":
            label, side = "total", r["side"]
        elif m in ("spread", "moneyline"):
            label, side = m, _team(r["side"], home, away)
        else:
            continue
        if side is None:
            continue
        line = None if m == "moneyline" else (float(r["line"]) if r.get("line") is not None else None)
        if m == "spread" and side == away and line is not None:
            line = -line                                      # store spreads from the home side, like the Odds API path
        grp.setdefault((label, line, r["book"]), {"t": r.get("retrieved_utc"), "src": r.get("source"), "p": {}})["p"][side] = r["american"]
    out = []
    for (label, line, book), g in grp.items():
        want = ("Over", "Under") if label == "total" or "|" in label else (home, away)
        if all(s in g["p"] for s in want):
            out.append({"label": label, "line": line, "book": book, "sides": list(want), "prices": {s: g["p"][s] for s in want},
                        "retrieved_utc": g["t"], "source": g["src"]})
    return out


def clean(prs: list[dict]) -> tuple[list[dict], list[dict]]:
    """Apply the hold and outlier rules. Returns (kept, dropped-with-reason)."""
    kept, dropped = [], []
    for p in prs:
        a, b = p["sides"]
        qa, qb = implied(p["prices"][a]), implied(p["prices"][b])
        hold = qa + qb - 1
        if not 0 <= hold <= MAX_HOLD:
            dropped.append(dict(p, reason=f"hold {hold:.3f} outside 0..{MAX_HOLD}"))
            continue
        kept.append(dict(p, no_vig={a: qa / (qa + qb), b: qb / (qa + qb)}, hold=hold))
    by = {}
    for p in kept:
        by.setdefault((p["label"], p["line"]), []).append(p)
    final = []
    for grp in by.values():
        for p in grp:
            a = p["sides"][0]
            others = [o["no_vig"][a] for o in grp if o is not p and o["book"] != "pinnacle"]
            if len(others) >= 2 and abs(p["no_vig"][a] - statistics.median(others)) > OUTLIER:
                dropped.append(dict(p, reason=f"no-vig {p['no_vig'][a]:.3f} vs median {statistics.median(others):.3f} of other books"))
            else:
                final.append(p)
    return final, dropped


def markets(prs: list[dict]) -> dict:
    """Same shape as pregame.odds.summarize_event: label -> sides, books{book: line, prices, no_vig, hold}, reference,
    best price per side, and a same-line consensus."""
    mk = {}
    for p in prs:
        m = mk.setdefault(p["label"], {"sides": p["sides"], "books": {}})
        cur = m["books"].get(p["book"])
        if cur is None or abs(cur["no_vig"][p["sides"][0]] - 0.5) > abs(p["no_vig"][p["sides"][0]] - 0.5):   # keep the book's main line
            m["books"][p["book"]] = {"line": p["line"], "prices": p["prices"], "no_vig": {k: round(v, 4) for k, v in p["no_vig"].items()},
                                     "hold": round(p["hold"], 4), "last_update": p["retrieved_utc"], "source": p["source"]}
    for m in mk.values():
        a, b = m["sides"]
        ref = m["books"].get("pinnacle")
        m["reference"] = {"book": "pinnacle", "line": ref["line"], "no_vig": ref["no_vig"]} if ref else {"book": None, "note": "Pinnacle did not list this market"}
        retail = {k: v for k, v in m["books"].items() if k != "pinnacle"}
        lines = [v["line"] for v in retail.values()]
        m["books_agree_on_line"] = len(set(lines)) <= 1
        if lines:
            modal = max(set(lines), key=lines.count)
            at = [v["no_vig"][a] for v in retail.values() if v["line"] == modal]
            m["consensus"] = {"line": modal, "n_books_at_line": len(at), "no_vig": {a: round(statistics.mean(at), 4), b: round(1 - statistics.mean(at), 4)}}
        m["best_retail_price"] = {s: (lambda c: {"book": c[1], "price": c[0], "line": c[2], "break_even": round(implied(c[0]), 4)})(
            max(((v["prices"][s], k, v["line"]) for k, v in retail.items()), key=lambda c: 1 / implied(c[0]))) for s in (a, b) if retail}
    return mk


def books_block(game_id: str, home: str, away: str, required: tuple, **kw) -> dict | None:
    """The packet's `books` record built from the direct pulls; None when there is nothing usable."""
    kept, dropped = clean(pairs(load_rows(game_id, **kw), home, away))
    if not kept:
        return None
    t = {}
    for p in kept:
        got = _utc(p["retrieved_utc"])
        if got and (p["book"] not in t or got < t[p["book"]]):
            t[p["book"]] = got
    req = [t[b] for b in required if b in t]
    stamp = min(req) if len(req) == len(required) else (min(t.values()) if t else None)
    return {"status": "OK_DIRECT", "source": "direct pulls (pregame/direct_lines) + Grok files when present; no Odds API",
            "retrieved_utc": stamp.strftime("%Y-%m-%dT%H:%M:%SZ") if stamp else None,
            "book_retrieved_utc": {b: v.strftime("%Y-%m-%dT%H:%M:%SZ") for b, v in sorted(t.items())},
            "markets": markets(kept), "dropped": [{k: d[k] for k in ("label", "line", "book", "reason")} for d in dropped][:200],
            "props_status": "OK"}


def write_freeze(game_id: str, date: str, away: str, home: str, block: dict, out_dir: Path) -> Path:
    """Price freeze in the format pipeline.hooks.four_book_prices reads (meta.status, meta.pulled_utc, rows[].book)."""
    now = datetime.now(timezone.utc)
    d = Path(out_dir) / f"{date}_{away}@{home}"
    d.mkdir(parents=True, exist_ok=True)
    rows = [{"book": b, "market": lab, "line": v["line"], "prices": v["prices"], "no_vig": v["no_vig"], "reference_only": b == "pinnacle"}
            for lab, m in block["markets"].items() for b, v in m["books"].items()]
    f = d / f"freeze_{now:%Y%m%dT%H%M%SZ}.json"
    f.write_text(json.dumps({"meta": {"status": "OK", "schema": "price-freeze/direct-1", "game_id": game_id, "game": f"{away}@{home}",
                                      "pulled_utc": block["retrieved_utc"], "written_utc": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                      "source": block["source"], "book_retrieved_utc": block["book_retrieved_utc"],
                                      "dropped": len(block["dropped"]), "research_only": True},
                             "rows": rows, "markets": block["markets"]}, indent=1, sort_keys=True) + "\n")
    return f


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Write a price freeze for one game from the direct pulls (+ Grok files).")
    ap.add_argument("--game", required=True)
    a = ap.parse_args(argv)
    from pipeline import hooks as H, phases as P
    pk = P.load_packet(a.game)
    g = pk.get("game") or {}
    away, home = a.game.split("_")[2], a.game.split("_")[3]
    blk = books_block(a.game, home, away, H.REQUIRED_BOOKS)
    if not blk:
        print(f"{a.game}: no usable direct lines")
        return 1
    f = write_freeze(a.game, str(g.get("date")), away, home, blk, H.PRICE_FREEZE_DIR)
    have = sorted(blk["book_retrieved_utc"])
    miss = [b for b in H.REQUIRED_BOOKS if b not in have]
    print(f"{a.game}: freeze {f.relative_to(ROOT)}; books {', '.join(have)}; required missing: {', '.join(miss) or 'none'}; "
          f"stamped {blk['retrieved_utc']}; dropped {len(blk['dropped'])} bad prices")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
