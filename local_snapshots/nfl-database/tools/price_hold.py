"""Missing model/price handling: re-pull, then conservative derivation, then HOLD (never a silent cut/pass).
HOLD is fail-closed: run_gate treats a HOLD leg as not live."""
def resolve_price(side, line, quotes, repull=None):
    note = []; attempted = repull is not None
    if repull is not None:
        try:
            q = repull()
            k = "nv_over" if side == "over" else "nv_under"
            if q and q.get("point") == line and isinstance(q.get(k), (int, float)):
                return dict(status="PASS", nv=float(q[k]), note="re-pull found price at line", repull_attempted=True)
            note.append("re-pull returned no price at line")
        except Exception as e: note.append(f"re-pull failed: {e}")
    k = "nv_over" if side == "over" else "nv_under"
    rungs = [r for r in (quotes or {}).get("rungs", []) if isinstance(r.get(k), (int, float))]
    # conservative: over -> nearest rung at/below line (higher over prob = harder edge bar); under -> at/above
    c = [r for r in rungs if (r["point"] <= line if side == "over" else r["point"] >= line)]
    if c:
        r = max(c, key=lambda r: r["point"]) if side == "over" else min(c, key=lambda r: r["point"])
        return dict(status="DERIVED", nv=float(r[k]), note="; ".join(note + [f"no-vig from conservative rung {r['point']}"]), repull_attempted=attempted)
    return dict(status="HOLD", nv=None, note="; ".join(note + ["no price after re-pull: HOLD (fail-closed)"]), repull_attempted=attempted)
