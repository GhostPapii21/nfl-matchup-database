"""THE RULEBOOK. Single source of truth for every NFL betting rule (Locked Door, Rico 2026-11-03 00:32 ET).
Changing a rule = edit this file WITH Rico's dated approval (approved_by/approved_at/approval_text). Code reads ids/params from here.
Activation: a rule is ON when max(manifest game_date, real/run clock date) >= effective. The door always uses the real clock,
so a backdated manifest cannot switch a rule off. effective=None => always on."""
import hashlib, os

R = "Rico"
RULES = {
 # ---- edge / pricing ----
 "NOSHRINK": dict(sev="BLOCK", text="Legs are judged on the raw average of the 3 model probabilities vs the no-vig price; the old 30% shrink is gone. Edge must be +3 pts or more.",
                  approved_by=R, approved_at="2026-11-02T21:13", effective=None, params=dict(min_edge=0.03, min_model_p=0.45)),
 "SCHEME_EDGE": dict(sev="FLAG", text="When matchup, scheme fit, game script and form trend all line up (each with a source), averages / 3-of-4 / sims can't cut the leg: under +3 is a FLAG, Ghost6 checks it at the real price and Rico gets the full breakdown. A plain-words edge explanation is required.",
                  approved_by=R, approved_at="2026-11-02T23:52", effective=None, params=dict(keys=("matchup", "scheme_fit", "script", "form_trend"))),
 "SCHEME_EDGE_LAST2": dict(sev="WARN", text="On a SCHEME_EDGE leg that misses 3-of-4, the last 2 games not clearing is a warning only.",
                  approved_by=R, approved_at="2026-11-03T00:31", effective=None, params={}),
 "MIRROR_OVER": dict(sev="BLOCK", text="Every under cut for a non-stop reason gets a mirror over candidate (or a logged no-rung reason).",
                  approved_by=R, approved_at="2026-11-02T21:13", effective="2026-11-02", params={}),
 "FAIR_PRICE": dict(sev="BLOCK", text="Every leg needs a real book price and no-vig fair price.", approved_by=R, approved_at="2026-11-01T12:00", effective=None, params={}),
 "SHORT_PRICE": dict(sev="FLAG", text="A leg priced -250 or shorter is flagged for Rico.", approved_by=R, approved_at="2026-11-01T12:00", effective=None, params=dict(price=-250)),
 # ---- Rico Nov 2 23:31 ----
 "N1": dict(sev="BLOCK", text="An RB with under 60% of his team's RB carries is DO NOT PLAY.", approved_by=R, approved_at="2026-11-02T23:31", effective="2026-11-02", params=dict(min_share=0.60)),
 "N2": dict(sev="BLOCK", text="A receiving leg needs a verified primary defender (with a source) or it is cut.", approved_by=R, approved_at="2026-11-02T23:31", effective="2026-11-02", params={}),
 "N3": dict(sev="BLOCK", text="Half and quarter spreads must match the game-script read for that period.", approved_by=R, approved_at="2026-11-02T23:31", effective="2026-11-02", params={}),
 # ---- depth receivers ----
 "DEPTH_RECEIVER": dict(sev="BLOCK", text="A #3/#4 WR or backup TE is in play only when the script calls for passing, the QB targets him 5%+ and his defender/coverage has been giving it up; low rung only; four checks, real price, weather and injuries still apply.",
                  approved_by=R, approved_at="2026-11-02T23:59", effective=None, params=dict(min_target_share=0.05, ranks=(3, 4))),
 "DEPTH_CAP": dict(sev="WARN", text="More than one depth receiver on a slip is a warning only (cap NOT approved by Rico).", approved_by="Ghost6 (proposal, not approved)", approved_at=None, effective=None, params=dict(max=1)),
 # ---- hard stops ----
 "WEATHER": dict(sev="BLOCK", text="Weather-flagged open-air games cut passing/receiving overs; multi-day forecast required at slip build.", approved_by=R, approved_at="2026-11-01T12:00", effective=None, params=dict(precip=50, gust=20, wind=15, forecast_max_h=24)),
 "FORECAST": dict(sev="BLOCK", text="Multi-day forecast block required, pulled within 24h.", approved_by=R, approved_at="2026-11-01T12:00", effective="2026-11-05", params={}),
 "INJURY": dict(sev="BLOCK", text="Out/Doubtful/IR/inactive players can't be on a slip.", approved_by=R, approved_at="2026-11-01T12:00", effective=None,
                  params=dict(bad=("out", "doubtful", "inactive", "ir", "injured reserve", "suspended", "pup", "nfi"))),
 "FORM_3OF4": dict(sev="BLOCK", text="The leg clears the exact line in 3 of the last 4 games with the current QB (unless SCHEME_EDGE).", approved_by=R, approved_at="2026-11-01T12:00", effective=None, params=dict(need=3, window=4)),
 "RB_TRAIL": dict(sev="BLOCK", text="RB rushing over: 60%+ carry share in 3 of last 4, and 4+ targets per game when his team may trail.", approved_by=R, approved_at="2026-11-01T12:00", effective=None, params=dict(share=0.60, need=3, tgt=4.0)),
 "COVERAGE_AGE": dict(sev="BLOCK", text="Defender coverage data must be 48 hours old or less.", approved_by=R, approved_at="2026-11-01T12:00", effective=None, params=dict(max_h=48)),
 "RECENT_DATA": dict(sev="BLOCK", text="Recent game data (feeds through last week) is required.", approved_by=R, approved_at="2026-11-01T12:00", effective=None, params={}),
 "SIMV6": dict(sev="BLOCK", text="Runs must be priced by tools/sim_v6.py.", approved_by=R, approved_at="2026-11-01T12:00", effective="2026-11-05", params={}),
 "COVPROF": dict(sev="BLOCK", text="Passing legs need the defense man/zone + MOF profile.", approved_by=R, approved_at="2026-11-01T12:00", effective="2026-11-05", params={}),
 "SNF": dict(sev="BLOCK", text="SNF postmortem rules S1-S4.", approved_by=R, approved_at="2026-11-02T08:14", effective="2026-11-02", params={}),
 "RICO4": dict(sev="BLOCK", text="Rico four rules R1-R4 (PRESS manual review, mirror over, 22% pool, QB return).", approved_by=R, approved_at="2026-11-02T05:01", effective="2026-11-02", params=dict(share_min=0.22)),
 # ---- slip rules ----
 "GATE_PASS": dict(sev="BLOCK", text="Every leg must come from a run that passed run_gate on the real clock, and be live in it.", approved_by=R, approved_at="2026-11-03T00:32", effective=None, params={}),
 "SLIP_SIZE": dict(sev="BLOCK", text="Main slips have 3 or 4 legs.", approved_by=R, approved_at="2026-11-01T12:00", effective=None, params=dict(min=3, max=4)),
 "NO_TD": dict(sev="BLOCK", text="Main slips have no touchdown legs.", approved_by=R, approved_at="2026-11-01T12:00", effective=None, params={}),
 "NO_PASS_YDS": dict(sev="BLOCK", text="Passing-yards legs (main or alt) are off all slips.", approved_by=R, approved_at="2026-11-03T06:17", effective=None, params={},
                  approval_text="Passing yards are off slips completely (Rico, Nov 3, 6:17 AM ET) - wired per Ghost6 audit 2026-11-03."),
 "TEAM_FILES": dict(sev="BLOCK", text="Both teams' database files are loaded into every build; a missing team file stops the build.", approved_by=R, approved_at="2026-11-02T23:59", effective=None,
                  params=dict(path="teams/{team}.json")),   # path = Blitz's team files; update when postmortems/2026-11-03_code_notes_for_ghost6.md lands (needs Rico-dated edit)
 "LEDGER": dict(sev="BLOCK", text="Every logged game must be in defender_ledger.csv; a skipped game stops the build.", approved_by=R, approved_at="2026-11-03T00:32", effective=None, params={}),
 "TEST_SUITE": dict(sev="BLOCK", text="The full test suite must have passed on the current code before any stamp (door.py test).", approved_by=R, approved_at="2026-11-03T00:32", effective=None, params={}),
 # ---- NBA (Rico 2026-11-03) ----
 "NBA_ONE_MARKET": dict(sev="BLOCK", text="NBA: one market per player per night (pts/reb/ast/combos/alt rungs, overs or unders). Keep only the best leg by raw no-shrink edge vs no-vig, worst-case edge as tiebreak; a slip with one player in two markets on the same night is blocked.",
                  approved_by=R, approved_at="2026-11-03T01:41", effective=None, params=dict(sport="NBA"),
                  approval_text="Rico approved exactly ONE v2.2 change (1:41 AM ET Nov 3): one market per player per night. (approved by Rico directly in Betting Hub)"),
 "NBA_ROLE_BUMP": dict(sev="FLAG", text="NBA: when a teammate averaging 28+ min is ruled out, his minutes/usage are spread over the rotation (games without him if 3+, else position/rotation share); every moved leg carries a visible ROLE BUMP flag naming the absent teammate and the minutes/stat bump.",
                  approved_by=R, approved_at="2026-11-03T01:42", effective=None, params=dict(sport="NBA", min_minutes=28.0, min_games_without=3),
                  approval_text="Second approved change from Rico (1:42 AM ET): build the teammate-out role bump into the NBA model. (approved by Rico directly in Betting Hub)"),
 "OVERRIDE": dict(sev="BLOCK", text="Overrides need Rico's recorded approval text and time; bots can't self-approve; relayed approvals don't count.", approved_by=R, approved_at="2026-11-03T00:32", effective=None, params=dict(approvers=("Rico",))),
}

def one_market_violations(legs):
    """NBA_ONE_MARKET: (player, date) pairs that appear in more than one leg."""
    seen = {}
    for l in legs: seen[(l["player"], str(l["date"])[:10])] = seen.get((l["player"], str(l["date"])[:10]), 0) + 1
    return [k for k, n in seen.items() if n > 1]

def rule(i): return RULES[i]
def param(i, k): return RULES[i]["params"][k]
def active(i, game_date=None, now=None):
    eff = RULES[i]["effective"]
    if not eff: return True
    ds = [str(game_date)[:10] if game_date else "", str(now)[:10] if now else ""]
    return max(ds) >= eff

def version():
    return hashlib.sha256(open(os.path.abspath(__file__).replace(".pyc", ".py"), "rb").read()).hexdigest()[:16]
