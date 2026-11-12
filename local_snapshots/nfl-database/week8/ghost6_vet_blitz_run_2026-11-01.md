# Ghost6 vet of Blitz Week 8 run, Nov 1 2026 (written ~07:40 ET, read-only)
Files read (mtime ET): eval_final.json 07:31:16; sims_final.json 07:31:05; sim_v5.py 07:16:01; assemble.py 07:30:49; game checklists 07:31:10-07:31:17; run_gate.py 01:03:41; test_run_gate.py 01:03:27; slips_2026-11-01.md 02:07:47.
Blitz was editing his folders during this vet, so these gate results are PROVISIONAL. Rerun the gate after he re-gates.

## Gate
- Tests: 30/30 OK (unittest; pytest isn't installed).
- run_gate.py exit 0 on all 13 folders (about 07:35 ET).
- In all 13 manifests, approved_exceptions covers only coverage.defenders, valid_for_date 2026-11-01, using the PFR Oct 29 cache. Reports mention it.

## Systematic low bias (MAJOR)
- sim_v5.py's "bias" model hard-codes haircuts: volume x0.92, catch x0.97, yards x0.95.
- Across 199 legs, compared with the line:
  - bias median is -17% on average and below the line 85% of the time
  - MC: -1.7% (52% below)
  - GR: -4.1% (57% below)
- Averaging the bias model into p pushes every under up and every over down by about 3-10 pts. That explains 127 of 199 legs and 15 of the 19 passes being unders.
- Fix: recalibrate the bias model to be mean-neutral, or treat it only as a floor check. Below I re-score the 19 on the MC+GR average.

## The 19 passes (as Blitz scored them / MC+GR only)
| Leg | Price | Blitz edge/shrunk | MC+GR edge/shrunk | Verdict |
|---|---|---|---|---|
| Henry rush U78.5 | -113 | +12.9/+9.0 | +8.7/+6.1 | REJECT: primary-star under |
| Addison rec U3.5 | -160 | +11.4/+5.7 | +9.4/+4.3 | VETTED |
| J. Williams rec yds U51.5 | -113 | +7.1/+5.0 | +4.1/+2.9 | REJECT: primary WR under; edge thin without bias |
| Tucker rec O3.5 | -120 | +8.0/+5.3 | +10.4/+7.0 | VETTED (LV, same game as stacked Bowers) |
| G. Wilson rec yds U63.5 | -113 | +7.6/+5.3 | +4.7/+3.3 | REJECT: primary-star under |
| G. Wilson rec U5.5 | -125 | +14.9/+9.8 | +12.5/+8.2 | REJECT: primary-star under |
| O. Cooper rec U3.5 | -148 | +3.0/+0.3 | +1.4/-0.9 | REJECT: edge exactly at the +3 floor; fails once the bias model is removed |
| Watson pass U210.5 | -113 | +8.8/+6.1 | +2.0/+1.4 | REJECT: edge comes entirely from the bias model |
| Concepcion rec yds U46.5 | -113 | +11.3/+7.9 | +8.6/+6.0 | VETTED |
| Boston rec U3.5 | -174 | +8.7/+3.3 | +6.3/+1.6 | REJECT: conflicts with placed UD Boston o29.5 rec yds |
| Penix pass U229.5 | -113 | +11.7/+8.2 | +5.5/+3.8 | REJECT: conflicts with London's placed overs |
| London rec yds U79.5 | -113 | +6.0/+4.2 | +2.2/+1.6 | REJECT: primary-star under, conflicts with placed tickets, edge <3 |
| Dotson rec yds U25.5 | -113 | +9.5/+6.7 | +7.5/+5.2 | VETTED |
| Dotson rec U2.5 | -180 | +14.2/+6.9 | +12.5/+5.8 | VETTED (same player as the yds leg; pick one) |
| Irving rush U70.5 | -113 | +6.0/+4.2 | +2.6/+1.8 | REJECT: primary RB under, edge <3 without bias |
| Puka rec O7.5 | -138 | +5.1/+2.3 | +8.2/+4.5 | VETTED with caution: stacks on UD Puka o69.5; Donte Jackson is Q; defender data is the Oct 29 cache |
| Worthy rec yds O29.5 | -113 | +8.0/+5.6 | +10.3/+7.2 | VETTED |
| Ollie Gordon rush U64.5 | -113 | +10.9/+7.6 | +8.5/+5.9 | VETTED with caution: MC median 55.3 vs Pinnacle 60.5 |
| Diggs rec yds O42.5 | -113 | +8.6/+6.0 | +12.5/+8.7 | VETTED |

Notes on the rule checks:
- As Blitz scored them, all 19 meet the rule: every model p >= .45, all three medians clear the line, and shrunk edge > 0. Cooper is the borderline case.
- Overs: Puka is #1 by targets over the last 3. Opportunity, coverage and pressure phases all PASS in the checklists.
- No-vig 0.500 on the -113 legs is two-way -113/-113 pricing, not a placeholder.

## TD replacements for the FD 7-leg (non-TD, not a stacked player)
1. Diggs 43+ rec yds, FD -113 (needs -140 or longer, and this qualifies). This replaces Walker TD.
2. Worthy 30+ rec yds, FD -113 (can replace either leg).
- Alternate: Tucker 4+ rec, -120. He's in Bowers' LV game, so the two are correlated.
- Puka 8+ rec, -138, only if Rico accepts stacking it on his UD Puka over.
- Prices are FanDuel main lines from the 07:30 pull, stale at 08:30. Check whether the FD 7-leg was actually placed.

## Ticket conflicts (Rico decides)
- London rec yds U79.5 runs against UD London o5.5 rec and Ticket 2 London 5+.
- Penix pass U229.5 runs against the same London overs.
- Boston rec U3.5 runs against UD Boston o29.5 rec yds.
- Puka rec O7.5 is a same-player stack with UD Puka o69.5 rec yds.
- Panthers rule: on an over, if the defense is top-10 in blitz rate or top-10 in pressure (PROXY), or there's an OL absence or a weak QB vs-blitz grade, the leg is marked CAUTION/UNVERIFIED for the user to decide. Affected legs, all already cut for other reasons: Aaron Jones, Goedert, Dulcich, Addison o37.5, M. Washington.
