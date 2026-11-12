"""DEPTH_RECEIVER rule (rules/rulebook.py) - replaces the old #3/#4 WR ban (press_tier, rico4 pool, snf WR4).
A depth receiver (WR rank 3/4, or TE2+) may be a live OVER leg only when ALL of these hold, each with a source:
  depth.script_pass  {ok, source}   game script calls for passing
  depth.target_share {value, source} QB's target share to him >= min_target_share (5%)
  depth.defender_giving {ok, source} his defender / coverage has been giving it up
  rung low (leg.rung == "low"), real price (price + no_vig), no weather stop, injury status OK.
The four checks / §7 / edge still run in run_gate. Unders on depth guys are not affected. Cap of 1 per slip = WARN (door)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rules import rulebook as _rb

def is_depth(leg):
    t = str(leg.get("type", "")).upper()
    return (t == "WR" and leg.get("wr_rank") in _rb.param("DEPTH_RECEIVER", "ranks")) or (t == "TE" and (leg.get("te_rank") or 1) >= 2)

def evaluate(leg):
    """-> (ok, [plain-word reasons it fails])"""
    if str(leg.get("side", "")).lower() != "over": return True, []
    t = str(leg.get("type", "")).upper()   # fail CLOSED: a WR/TE over with no rank can't be cleared as a non-depth receiver (Ghost6 audit 2026-11-03)
    if t == "WR" and leg.get("wr_rank") in (None, ""): return False, ["wr_rank missing - can't tell if he is a depth receiver (fail closed)"]
    if t == "TE" and leg.get("te_rank") in (None, ""): return False, ["te_rank missing - can't tell if he is a depth receiver (fail closed)"]
    if not is_depth(leg): return True, []
    d, why = leg.get("depth") or {}, []
    sp = d.get("script_pass") or {}
    if not (sp.get("ok") is True and sp.get("source")): why.append("game script does not call for passing (depth.script_pass ok+source missing)")
    ts = d.get("target_share") or {}; mn = _rb.param("DEPTH_RECEIVER", "min_target_share")
    if ts.get("value") is None or not ts.get("source"): why.append("QB target share to him missing (depth.target_share value+source) - fail closed")
    elif float(ts["value"]) < mn: why.append(f"QB target share {float(ts['value']):.1%} < {mn:.0%}")
    dg = d.get("defender_giving") or {}
    if not (dg.get("ok") is True and dg.get("source")): why.append("his defender/coverage has not been shown giving it up (depth.defender_giving ok+source)")
    if str(leg.get("rung", "")).lower() != "low": why.append(f"depth receiver must be the low rung (rung={leg.get('rung')!r})")
    if leg.get("price", leg.get("price_fd")) in (None, "") or leg.get("no_vig") in (None, ""): why.append("no real book price / no-vig price")
    if leg.get("weather_stop"): why.append("weather stop")
    if str(leg.get("injury_status", "")).lower() in _rb.param("INJURY", "bad"): why.append(f"injury status {leg.get('injury_status')}")
    return (not why), why

def check_depth(self, m, legs, live):
    for n in sorted(live):
        ok, why = evaluate(legs[n])
        if not ok: self.fail(f"leg {n}: DEPTH_RECEIVER not met: " + "; ".join(why))

def install(G): G.check_depth = check_depth
