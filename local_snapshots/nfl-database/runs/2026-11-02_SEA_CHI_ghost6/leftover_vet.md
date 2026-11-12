# Leftover leg vet — CHI @ SEA MNF, Nov 2 2026 (Lumen Field, open air). Written ~3:45 PM ET. NOT VETTED (needs Ghost6 sign-off). No bets placed.
Odds: The Odds API pulled 3:35 PM ET (book stamps 3:30 PM ET) -> leftover/odds_m1535.csv, 0 in-play rows. FD = price of record, DK/Pinnacle comparison. Fresh until ~4:35 PM ET.
Sims: leftover/sims.py (tools/sim_v6_fix unedited, MC/Bias/GR 3x100k, seed 20261101) -> raw_sims.json. Fantasy + sacks have no sim_v6 market -> leftover/custom.py (same 3-model design, 100k each, seed 20261101; SELF-DERIVED APPROXIMATION) -> custom_sims.json.
Game logs: nflverse pbp 2026 Wk1-7 (src/play_by_play_2026.parquet). Darnold games = Wk3-7 (last 4 = Wk4-7); Caleb games = Wk1,2,6,7.
Weather: src/forecast 5:04 AM ET + Blitz 7:55 AM ET (NWS + Open-Meteo): 2-4% rain, gusts <=7 mph -> no flag. Recheck at 6:45 PM ET inactives.
Rules: edge = avg p - no-vig >= +3; shrunk p' = .5+.7(p-.5) must beat no-vig; every p >= .45; every median clears; alt nv = implied / main overround (FD -113/-113 = 1.061).

| # | Leg | Last 4 (cur QB) | §7 | Book / no-vig | MC / Bias / GR (medians) | Edge raw / shrunk | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | Darnold 225+ pass yds | 168, 195, 278, 257 | 2/4 FAIL | FD alt 224.5 -166 -> nv .588 | .555 / .620 / .612 (245/261/259) | +0.8 / -2.1 | CUT |
| 2 | Caleb 175+ pass yds | 269, 138, 305, 308 | 3/4 | FD alt 174.5 -470 -> nv .777 (FLAG < -250) | .811 / .811 / .792 (227/228/228) | +2.8 / -6.4 | CUT |
| 3 | Charbonnet 30+ rush+rec | 0 games in 2026 | NO SAMPLE FAIL | FD R+R 39.5 -115/-111; DK alt 24.5 -305 / 39.5 -119; no 29.5 rung | SIMULATION NOT RUN (no active games) | n/a | CUT |
| 4 | Charbonnet 1.5 rec (More) | 0 games 2026 (2025: 2+ rec in 7/16) | FAIL | FD 1.5 +134/-180 -> nv over .399 | NOT RUN (2025 base .44, capped workload, Holani is receiving back) | ~+4 on 2025 rate, not modelable | CUT |
| 5a | Darnold sacks MORE 2 (push at 2) | 3, 5, 5, 0 | 3/4 | NOLINE at FD/DK (only Leonard Williams sacks); PrizePicks 2.0 only | P(3+): .630 / .545 / .602; push .20-.24; λ 2.9-3.2 | vs pick'em .50 (no-push basis .79/.71/.75) — no book no-vig = MISSING | LEAN |
| 5b | Darnold sacks LESS 2 | same | 1/4 FAIL | same | P(<=1): .166 / .220 / .194 | negative | CUT |
| 6 | E. Wilson 22.5 rush yds | 81, 61, 52, 100 (14-24 car) | 4/4 | DK 22.5 -109/-115 -> nv .494; Pinnacle 18.5 -164/+134; FD NOLINE | Price IR+Charb capped: .826/.959/.791 (44/53/45); Price active: .591/.740/.574 (27/32/27) | +36 / +25 (IR); +14 / +8 (active) | CUT |
| 7 | Kupp 1.5 rec (More) | 1, 2, 5, 2 (tgt 2,3,10,2) | 3/4 | FD main 2.5 -160/+120 (nv over .575); no 1.5 rung at FD/DK -> NOLINE | .667 / .563 / .692 (2/2/2) | no-vig MISSING | CUT |
| 8 | JSN 21 PP fantasy | 12.6, 21.2, 25.4, 30.0 | 3/4 | No book market; market proxy from FD rec 7.5 / yds 99.5 / alt 59.5 + .45 ATD -> .466 | .549 / .467 / .530 (22.4/20.0/22.1) | +5.0 / +4.5 | LEAN |
| 9 | JSN 60+ rec yds | 76, 102, 134, 150 | 4/4 | FD alt 59.5 -650 -> nv .817 (FLAG < -250) | .865 / .788 / .820 (114/99/112) | +0.7 / -9.0 | CUT |
| 10 | Swift 15+ rec yds | 10, 54, 26, 12 | 2/4 FAIL | FD alt 14.5 -230 -> nv .657 | .645 / .574 / .600 (20/18/19) | -5.0 / -5.3 | CUT |

## Reasons (one line each)
1. Darnold 225+: §7 2/4 and the -166 alt is priced past every model after shrink.
2. Caleb 175+: models agree he clears (~80%) but -470 already prices that; -6 after shrink, and it's a < -250 leg.
3. Charbonnet 30+ R+R: zero 2026 games (activated 10/22, pitch count per Macdonald) -> no §7 sample, sim can't run, P4 defender check MISSING.
4. Charbonnet 1.5 rec: same no-sample cut; he's the 2-down back (5% tgt share 2025), Holani owns RB targets, CHI is man-heavy (RB tgt rate falls vs man).
5. Darnold sacks: all three models lean MORE (λ ~3, CHI 8.8% sack rate, Darnold 6.8%, LT Cross OUT), §7 3/4 — but no sportsbook sack market exists so the edge rule can't be checked: LEAN, needs Rico's override. LESS is a CUT. Note: MORE works against SEA passing legs on placed tickets (JSN 70+) — correlation flag.
6. Wilson 22.5: HARD fails — committee gate (60%+ carry share in only 2 of last 4) and could-trail rule (SEA -3 counts; Wilson ~1 tgt/g, needs 4+). Medians 20-30 yds over the line = MODEL-SUSPECT. Price-active split still +8 shrunk but the hard gates don't change. Re-check after the 4 PM Price decision (Charb 9-12 / Wilson 7-11 / Holani 3-5 / Price 3-6 car).
7. Kupp 1.5 rec: no book price for the 1.5 rung, ≤3 targets in 3 of last 4 (one-catch coin-flip rule), and the room already cut Kupp as a #3-type option.
8. JSN 21 fantasy: §7 3/4, edge clears vs a self-derived market proxy, but Bias median (20.0) sits below 21 -> 2 of 3 only, and the proxy isn't a real book line; also same-player stack with placed JSN 70+ (and JSN TD) -> flag for Rico. LEAN.
9. JSN 60+: 4/4 but -650 is nested under the placed JSN 70+ (placed-ticket bar) and has no edge (-9 shrunk). CUT.
10. Swift 15+ rec yds: §7 2/4 with Caleb and models below the -230 price. (Swift 4+ catches remains our cleared Swift leg.)

## Summary
PASS: none. LEAN: Darnold sacks MORE 2 (no book line), JSN 21 fantasy (2 of 3 + placed-ticket stack). CUT: 1, 2, 3, 4, 5b, 6, 7, 9, 10.
Gaps: no sportsbook market for sacks/fantasy (self-derived proxies), Charbonnet sample, PFR coverage pull is from 5:06 AM (fresh <48h), Price IR status pending 4 PM.

## Addendum: Charbonnet on a 2025 proxy (EXCEPTION to §7: 2025 sample, Rico decides)
Sources: nflverse stats_player_week/pbp/snap_counts 2025. Cross-check: ESPN (Oct 22 2026) gives 730 rush yds for 2025, which matches the nflverse sum of 730. Script: leftover/charb2025.py, output in charb2025_sims.json.
Injury: tore his left ACL Jan 17 2026 (DIV vs SF, 5 carries/15% snaps that day). Surgery Feb 12. Activated from PUP Oct 22. Held out vs KC as "part of the plan". Tonight is his first game back (NFL.com/ESPN/NBC).
2025 REG (QB Darnold every game): 30+ R+R in 15/16 games and 4/4 in the last 4 (Wks 15-18: 31/54/122/97). 2+ catches 7/16, and 3/4 in the last 4. Leading ≥50% of plays: 9/9 R+R, 4/9 rec. Trailing: 6/7 R+R, 3/7 rec. Snap share <45%: 6/6 R+R, 2/6 rec. Walker was active in every game, so there is no inactive split (Walker is now in KC).
Sim: 2025 run/catch bootstrap, YPC regressed 30% to the league average, CHI half-strength, ~1.1 targets (pitch-count snaps). 3x100k.
| Leg | Price IR (9-12 car) mc/bias/gr | Price active (8-11) | no-vig | edge (shrunk, worst model) | verdict |
|---|---|---|---|---|---|
| 30+ R+R | .849/.775/.815, med 48/43/49 | .793/.702/.769, med 44/39/45 | ~.64 (interp. DK 24.5 -305 ÷1.06 → .71; FD 39.5 → .497) | IR +5.3 / Active −4.9 | LEAN only if Price is inactive; CUT if Price is active. Flag the committee gate (never had a 60% carry share in 2025) |
| PP 2+ rec | .233/.173/.235, med 1 | .235/.172/.237 | .399 | negative | CUT |

## Head-to-head SEA vs CHI
No 2025 meeting. Last meeting: 2024 Wk17, Dec 26 2024, SEA 6 @ CHI 3. Source is nflverse pbp only (PFR fetch blocked/timed out, so this is UNVERIFIED by a second source).
QBs: Geno Smith (SEA), Caleb Williams (CHI). SEA 160 pass/122 rush. CHI 122 pass/103 rush, and Caleb was sacked 7 times.
Lines: Charbonnet 15-57 + 3/3-19 (76 R+R, with Walker OUT). JSN 6 tgt, 3-32. Swift 12-53 + 4/5-28 (4 rec). Odunze 1/4-15. Caleb 5-37 rushing. Darnold, Kupp, Burden, Loveland, Raymond and Wilson did not play for these teams in that game.
Changes since: SEA QB Geno → Darnold, and the OC has changed. CHI went from interim HC Thomas Brown to Ben Johnson (new scheme). Metcalf, Lockett, Moore and Allen are gone. Low relevance overall.
Impact: JSN 100+ — the 2024 line is pre-breakout under a different QB/OC, so not informative and no change. Swift 4+ rec — he hit it (4) in that game, a mild support, no change. Leans (sacks MORE 2, JSN 21 FP) — the 7-sack game supports sacks MORE only weakly, because it was Caleb as a rookie under a different OC. Charbonnet — 76 R+R as the lead back, but that is not comparable to tonight.
