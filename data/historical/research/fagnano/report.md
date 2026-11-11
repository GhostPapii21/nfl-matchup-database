# Joe Fagnano (ESPN id 4429582) — splits + JAX@BAL projection (built 2026-11-04 ~7:55 AM ET)
Raw: raw/splits.json, gamelog.json, stats.json, bal_roster.json (ESPN public site JSON). splits.html came back empty (0 bytes) — JSON used instead.
## ESPN splits (career = 1 game, wk8 @BUF, L 10-36, entered AS SUB in Q2)
All: 10/21, 91 yds, 47.6%, 4.3 Y/A, 0 TD, 1 INT, long 22, 3 sacks, rtg 40.0, QBR 7.4; rush 3-3.
Away/Outdoors/Sunday/vs AFC/vs BUF/Behind = identical (one game). 1st half (Q2 only): 5/8 50 yds, INT, 3 sacks. 2nd half: 5/13 41 (Q3 2/8 28, Q4 3/5 13).
Downs: 1st 2/5 28 INT 2 sk; 2nd 5/7 26; 3rd 3/8 37 1 sk; 4th 0/1. Red zone (Opp 19-goal): 1/4 6 yds, 1 sk. Last 2 min half: 2/3 16, INT.
No ESPN splits exist for home, NFC, leading/tied, surface, distance.
## Throw log (throw_log.csv, nflverse pbp; no blitz/pressure-type columns in this pbp file → qb_hit used)
24 dropbacks + 1 scramble: 21 att, 3 sacks (all Q2, 2 in/near red zone), qb_hit on 11 of 25. Targets: J.Hill (RB) 6, Andrews 4, Flowers 4 (0 catches, INT), Bateman 3 (1/22 deep), others 4. Only 2 deep attempts (both Bateman, right). Air yards mostly 0-8; 3 throws behind the line.
Story: came in cold at -6, hit two quick left-side throws, then got sacked 3 times in 7 dropbacks. After that he lived on checkdowns to Hill and short outs; Flowers got 4 looks, all incomplete, one picked. Under hits he went short/right; the one good play was a 3rd-and-6 deep shot to Bateman. Trailing 13-26 the whole second half.
## JAX defense (pbp wks 1-9, 7 games)
Dropbacks faced 38.6/g; sack% 5.6 (lg 6.2), qb_hit% 15.6; 2.1 sacks/g. Cmp% allowed 66.5, Y/A 7.64 (lg 7.03), 264 pass yds/g, 3.0 20+ passes/g, 1.29 INT/g + 0.43 fum lost/g. Rush 78 yds/g, scramble 9 yds/g. RZ TD% allowed 71% (14 trips; small).
Vs weaker QBs: Watson 205/5 sk/1 INT, D.Jones 144/3 sk/2 INT, Maye 199/2 INT. Blitz/coverage rates: NOT available in this pbp (gap). JAX defensive injuries: not checked this run (gap).
## Projection (project.py, 100k sims; every rate is an ESTIMATE)
Chain: BAL plays/pass rate from scenario yaml (base 54 @58%, flip 56 @65%, BAL TT ~13.4, unchanged) → sack 8.5% (blend JAX 5.6 / his 12.5; link: sacks) → scramble 3% → cmp% 58.5% (rookie, JAX allows 66.5; link: cmp%) → 10.6 yds/comp (JAX Y/A +0.6 over lg; link: yds) → INT 2.7%/att (JAX 1.29/g; link: INT).
| | att | cmp | pass yds | TD | INT | sacks | rush |
|base|27.5|16.1|171|0.9*|0.7|2.6|~2/7|
|flip|32.1|18.8|199|1.0*|0.9|3.1|~2/8|
*TD likely high for TT 13.4; read ~0.7.
P(clear): pass yds 149.5 63/80, 160.5 54/73, 162.5 53/72, 175.5 43/63, 199.5 27/46; cmp 15.5 55/77; INT 0.5 52/57; 3+ sacks 50/59; rush yds 9.5 30/35 (base/flip %).
Targets (base 27.5 att, est.): Flowers ~24% (6-7), Andrews+Likely ~20% (5-6), RBs Hill/Henry ~18% (5), Bateman ~13% (3-4), rest.
Miss audit (wk8): 4.3 Y/A came with 3 early sacks + BUF pass rush, cold relief entry — partly present (JAX less pressure than BUF, full week of 1st-team reps → absent). Tiny sample, context only.
## Lines saved (r5 odds, no new credits)
Fagnano pass yds DK 162.5 -112/-112, FD 160.5 -114, PP/UD 160.5-161.5; DK alts o149.5 -159, o169.5 +108, o199.5 +235; PP cmp 15.5. Flowers rec 4.5 (DK +110/-140), yds 44.5-47.5; Andrews rec 2.5, yds 18.5-21.5; Bateman 1.5/14.5; Henry rush 69.5.
Needed: Fagnano INT, attempts, TD, rush yds, sacks; BAL TT; Likely props.
