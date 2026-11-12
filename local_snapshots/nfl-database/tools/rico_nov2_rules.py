"""Rico's three rules, approved in Betting Hub 2026-11-02 23:31 ET ("Yes").
N1  RB legs: carry share must be sourced; a back under 60% of team RB carries is DO NOT PLAY (cut).
N2  Receiving legs: need a verified PRIMARY defender (coverage.defenders[i].primary is True with a source).
    Overrides the WR3_TEAM_COV team-profile fallback.
N3  Half/quarter spreads must match the game-script read for that period (leg.script_read.expected_winner == leg.team).
Applies to runs with game_date >= NOV2_FROM. Weather, inactives, sec 11, depth-receiver rule still apply on top.
"""
import re, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rules import rulebook as _rb
NOV2_FROM = _rb.rule("N1")["effective"]
RB_SHARE_MIN = _rb.param("N1","min_share")
PERIOD_RX = re.compile(r"\b(1H|2H|1st half|2nd half|first half|second half|Q[1-4]|[1-4](st|nd|rd|th) quarter)\b", re.I)
SPREAD_RX = re.compile(r"spread|[+-]\d+(\.\d)?\b", re.I)

def _share(l):
    cs = l.get("carry_share")
    if isinstance(cs, dict) and isinstance(cs.get("value"), (int, float)) and cs.get("source"): return float(cs["value"])
    return None

def is_period_spread(l):
    mk = str(l.get("market", "")) + " " + str(l.get("name", ""))
    return (str(l.get("type", "")).upper() in ("SPREAD", "GAME") or "spread" in mk.lower()) and bool(PERIOD_RX.search(mk)) and bool(SPREAD_RX.search(mk))

def check(gate, m, legs, live):
    if not _rb.active("N1", getattr(gate, "game_date", ""), getattr(gate, "now", None)): return
    notes = gate.__dict__.setdefault("nov2_notes", [])
    for n in sorted(live):
        l = legs[n]
        if str(l.get("type", "")).upper() == "RB":
            s = _share(l)
            if s is None: gate.fail(f"leg {n}: N1 RB carry share missing or unsourced (carry_share {{value, source}} required)")
            elif s < RB_SHARE_MIN: gate.fail(f"leg {n}: N1 DO NOT PLAY, RB carry share {s:.0%} < 60% (committee back)")
            else: notes.append(f"{n}: N1 carry share {s:.0%} (>= 60%)")
        if l.get("receiving") or str(l.get("type", "")).upper() in ("WR", "TE"):
            ds = (l.get("coverage") or {}).get("defenders") or []
            prim = [d for d in ds if d.get("primary") is True and (d.get("source") or d.get("url_or_file"))]
            if not prim: gate.fail(f"leg {n}: N2 no verified primary defender (receiving legs can't go on a slip without one; WR3 team-profile fallback no longer enough)")
            else: notes.append(f"{n}: N2 primary defender {prim[0].get('name')} ({prim[0].get('source') or prim[0].get('url_or_file')})")
        if is_period_spread(l):
            sr = l.get("script_read") or {}
            if not sr.get("expected_winner") or not sr.get("source"):
                gate.fail(f"leg {n}: N3 half/quarter spread without a sourced game-script read for that period")
            elif sr["expected_winner"] != l.get("team"):
                gate.fail(f"leg {n}: N3 half/quarter spread on {l.get('team')} but the script read expects {sr['expected_winner']} to win that period")
            else: notes.append(f"{n}: N3 period spread matches script read ({sr['expected_winner']})")

