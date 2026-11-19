"""Compare book prices with Pinnacle fair probability at the same yardage line.

Exact lines use Pinnacle's de-vigged two-way market. Different lines are shifted
with the Task 3 yardage distribution while retaining Pinnacle's fair baseline.
"""
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


def game_edges(doc: dict, min_edge: float = MIN_EDGE, distribution: dict | None = None,
               player_contexts: dict | None = None) -> tuple[list, list, dict]:
    rows = [r for r in doc.get("rows", []) if r.get("market") in PLAYER_MARKETS and r.get("side") in ("Over", "Under")
            and r.get("line") is not None and r.get("american") is not None]
    pin: dict = {}
    for r in rows:
        if r["book"] == "pinnacle":
            pin.setdefault((norm_name(r["player"]), r["market"]), {}).setdefault(float(r["line"]), {})[r["side"]] = r["american"]
    fair, edges, counts = [], [], {
        "compared": 0, "line_mismatch": 0, "no_pinnacle": 0,
        "line_shifted": 0, "distribution_unavailable": 0,
    }
    fair_at = {}
    pin_by_player_market: dict[tuple[str, str], list[tuple[float, dict[str, float]]]] = {}
    for (pl, mk), by_line in pin.items():
        for line, s in by_line.items():
            if "Over" in s and "Under" in s:
                po, pu = devig(s["Over"], s["Under"])
                fair_at[(pl, mk, line)] = {"Over": po, "Under": pu}
                pin_by_player_market.setdefault((pl, mk), []).append((line, {"Over": po, "Under": pu}))
                fair.append({"player": pl, "market": mk, "line": line, "p_fair_over": round(po, 4), "p_fair_under": round(pu, 4)})
    for r in rows:
        if r["book"] == "pinnacle":
            continue
        pl, mk, line = norm_name(r["player"]), r["market"], float(r["line"])
        f = fair_at.get((pl, mk, line))
        reference_line = line
        if f is None:
            counts["line_mismatch"] += 1
            candidates = pin_by_player_market.get((pl, mk), [])
            if not candidates:
                counts["no_pinnacle"] += 1
                continue
            if not distribution:
                counts["distribution_unavailable"] += 1
                continue
            reference_line, f = min(candidates, key=lambda item: (abs(item[0] - line), item[0]))
            context = (player_contexts or {}).get(f'{doc.get("game_id")}|{pl}', {})
            if not context:
                counts["distribution_unavailable"] += 1
                continue
            try:
                from ladder import tail_probability

                p_at_book, _ = tail_probability(distribution, mk, context.get("position"), context.get("adot"), reference_line, line)
                p_at_pin, _ = tail_probability(distribution, mk, context.get("position"), context.get("adot"), reference_line, reference_line)
            except (ImportError, ValueError, TypeError):
                p_at_book = p_at_pin = None
            if p_at_book is None or p_at_pin is None:
                counts["distribution_unavailable"] += 1
                continue
            shift = p_at_book - p_at_pin
            f = {
                "Over": min(1.0, max(0.0, f["Over"] + shift)),
                "Under": min(1.0, max(0.0, f["Under"] - shift)),
            }
            counts["line_shifted"] += 1
        counts["compared"] += 1
        be = r.get("break_even") or implied(r["american"])
        e = f[r["side"]] - be
        if e >= min_edge:
            edges.append({"game_id": doc.get("game_id"), "player": r["player"], "market": mk, "book": r["book"], "side": r["side"],
                          "line": line, "american": r["american"], "break_even": round(be, 4), "p_fair": round(f[r["side"]], 4),
                          "edge": round(e, 4), "line_shifted": reference_line != line,
                          "pinnacle_line": reference_line, "line_snapshot_utc": doc.get("retrieved_utc")})
    for x in fair:
        x["game_id"] = doc.get("game_id")
    return fair, edges, counts


def main() -> dict:
    all_fair, all_edges, tot = [], [], {"compared": 0, "line_mismatch": 0, "no_pinnacle": 0, "games": 0}
    tot.update({"line_shifted": 0, "distribution_unavailable": 0})
    artifact = {}
    artifact_path = OUT / "ladder.json"
    if artifact_path.exists():
        try:
            artifact = json.loads(artifact_path.read_text())
        except json.JSONDecodeError:
            artifact = {}
    distribution = artifact.get("model", {})
    player_contexts = artifact.get("player_contexts", {})
    for f in sorted(glob.glob(str(LINES / "20*.json"))):
        doc = json.loads(Path(f).read_text())
        doc.setdefault("game_id", Path(f).stem)
        fa, ed, c = game_edges(doc, distribution=distribution, player_contexts=player_contexts)
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
