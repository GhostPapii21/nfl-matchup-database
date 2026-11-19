"""Task 1: Pinnacle fair price (vig removed) compared with every other book's price on the same player, market and line.
Reads pregame/direct_lines/<game>.json; writes research/edge_2026/edges_latest.json and fair_prices_latest.json.
Lines that differ from Pinnacle's are left out for now (counted as 'line_mismatch'); Task 3's distribution will shift them."""
from __future__ import annotations

import glob
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LINES = ROOT / "pregame" / "direct_lines"
OUT = Path(__file__).resolve().parent
PLAYER_MARKETS = {"receptions", "receiving_yards", "rushing_yards", "rush_rec_yards"}
MIN_EDGE = 0.02


def implied(american: float) -> float:
    a = float(american)
    return 100 / (a + 100) if a > 0 else -a / (-a + 100)


def devig(over_american: float, under_american: float) -> tuple[float, float]:
    """Multiplicative de-vig: each side's implied probability divided by their sum."""
    qo, qu = implied(over_american), implied(under_american)
    return qo / (qo + qu), qu / (qo + qu)


def norm_name(n: str) -> str:
    n = re.sub(r"[^a-z ]", "", (n or "").lower().replace("-", " "))
    return " ".join(w for w in n.split() if w not in {"jr", "sr", "ii", "iii", "iv", "v"})


def game_edges(doc: dict, min_edge: float = MIN_EDGE) -> tuple[list, list, dict]:
    rows = [r for r in doc.get("rows", []) if r.get("market") in PLAYER_MARKETS and r.get("side") in ("Over", "Under")
            and r.get("line") is not None and r.get("american") is not None]
    pin: dict = {}
    for r in rows:
        if r["book"] == "pinnacle":
            pin.setdefault((norm_name(r["player"]), r["market"]), {}).setdefault(float(r["line"]), {})[r["side"]] = r["american"]
    fair, edges, counts = [], [], {"compared": 0, "line_mismatch": 0, "no_pinnacle": 0}
    fair_at = {}
    for (pl, mk), by_line in pin.items():
        for line, s in by_line.items():
            if "Over" in s and "Under" in s:
                po, pu = devig(s["Over"], s["Under"])
                fair_at[(pl, mk, line)] = {"Over": po, "Under": pu}
                fair.append({"player": pl, "market": mk, "line": line, "p_fair_over": round(po, 4), "p_fair_under": round(pu, 4)})
    for r in rows:
        if r["book"] == "pinnacle":
            continue
        pl, mk, line = norm_name(r["player"]), r["market"], float(r["line"])
        f = fair_at.get((pl, mk, line))
        if f is None:
            counts["line_mismatch" if (pl, mk) in pin else "no_pinnacle"] += 1
            continue
        counts["compared"] += 1
        be = r.get("break_even") or implied(r["american"])
        e = f[r["side"]] - be
        if e >= min_edge:
            edges.append({"game_id": doc.get("game_id"), "player": r["player"], "market": mk, "book": r["book"], "side": r["side"],
                          "line": line, "american": r["american"], "break_even": round(be, 4), "p_fair": round(f[r["side"]], 4),
                          "edge": round(e, 4), "line_shifted": False})
    for x in fair:
        x["game_id"] = doc.get("game_id")
    return fair, edges, counts


def main() -> dict:
    all_fair, all_edges, tot = [], [], {"compared": 0, "line_mismatch": 0, "no_pinnacle": 0, "games": 0}
    for f in sorted(glob.glob(str(LINES / "20*.json"))):
        doc = json.loads(Path(f).read_text())
        doc.setdefault("game_id", Path(f).stem)
        fa, ed, c = game_edges(doc)
        all_fair += fa
        all_edges += ed
        tot["games"] += 1
        for k in c:
            tot[k] += c[k]
    all_edges.sort(key=lambda x: -x["edge"])
    summary = {"counts": tot, "edges": len(all_edges), "min_edge": MIN_EDGE,
               "by_book": {b: sum(1 for e in all_edges if e["book"] == b) for b in sorted({e["book"] for e in all_edges})}}
    (OUT / "edges_latest.json").write_text(json.dumps({"summary": summary, "edges": all_edges}, indent=1))
    (OUT / "fair_prices_latest.json").write_text(json.dumps(all_fair, indent=1))
    return summary


if __name__ == "__main__":
    s = main()
    print(json.dumps(s, indent=1))
    for e in json.loads((OUT / "edges_latest.json").read_text())["edges"][:15]:
        print(f'{e["edge"]:+.3f} {e["book"]:<12} {e["player"]:<22} {e["market"]:<16} {e["side"]:<5} {e["line"]:>5} {e["american"]:>5}  fair {e["p_fair"]:.3f}')
