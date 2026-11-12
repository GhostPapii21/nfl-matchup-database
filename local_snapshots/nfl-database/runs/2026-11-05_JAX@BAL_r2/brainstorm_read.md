# Brainstorm read — TNF JAX @ BAL, Thu 2026-11-05 8:15 PM ET, M&T Bank Stadium (open air)
Written Tue 2026-11-03 ~7:20 PM ET by Blitz, BEFORE any prop pricing. Locked hypothesis (sha256 in brainstorm_read.sha256). Zero Grok/OpenAI calls.

## 1. Slate snapshot
ESPN scoreboard (DraftKings) pulled 2026-11-03 19:13 ET: JAX -10, O/U 40.5 (Nov 3 09:58 was -9.5 / 41.5: moved toward JAX and down). Implied: JAX 25.25, BAL 15.25. Short week both sides. Weather: forecast re-pull pending (Phase 11).
Market question: books expect JAX to lead comfortably and BAL to score ~15.

## 2. Game script
BASE: JAX leads by halftime (a 10-14 pt lead), BAL's undrafted 3rd-string QB Joe Fagnano (1st start) can't sustain drives; JAX goes run-lean in the 2H and kills clock. BAL trails, so pass share rises but efficiency is poor (short throws, sacks). Low-to-mid total.
FLIP A (slog): JAX offense stalls too in a short-week low-event game; under 40.5, both sides' yardage lines die, JAX wins 17-10ish.
FLIP B (BAL competitive): BAL's D (pressure rank #4 PROXY) harasses Lawrence, BAL leans heavily on Henry/Lamar-less run game, stays within one score into Q4 -> more Henry carries, JAX spread fails.

## 3. Injury fallout (ESPN injuries 2026-11-03 19:14 ET; baltimoreravens.com, NFL.com, ESPN Hensley 11/3)
- BAL: Lamar Jackson OUT (thumb, IR expected); Huntley Doubtful (toe); Fagnano confirmed starter by HC Minter Tue, full practice w/ taped ankle. Backups Slovis/Reed newly signed. All BAL passing-dependent legs = backup-QB legs (+7 bar).
- BAL OL: RG Rosengarten Q (LP), LG Simpson Q (LP) -> more pressure on a rookie, weaker interior run blocking (caps Henry overs). NT Jenkins Q. S Hawkins Q (DNP est).
- JAX: RB Tuten Q (DNP Tue, foot) -> backfield split Rodriguez (Q, LP)/LeQuint Allen; no leg that needs Tuten to sit. WR Meyers Q (LP). DT Hamilton IR, S Eric Murray IR (helps BAL deep shots marginally, but Fagnano aDOT 4.3).

## 4. Matchup
- JAX D (nflverse pbp + FTN wk1-8): blitz 30.4% (16th; last-4 29.7%), pressure PROXY 21.5% (10th), EPA/db -0.050 (6th). Run D elite: RB YPC 3.28 on 123 (league 4.16), rush EPA -0.208. Gives up WR yards: 9.72 YPT to WR (n141, league 8.02), deep zones leak; stingy to TE (4.81 YPT, n47) and short-left/right.
- Coverage shell man/zone and MOF: MISSING (FTN has no man/zone column; PFF premium locked) -> flag only.
- Fagnano vs BUF (24 dropbacks, LOW-SAMPLE): 10/21 91 yds, 1 INT, 3 sacks, EPA/db -0.43. aDOT 4.3, 24% of attempts behind LOS, Justice Hill 6 tgts (29%, aDOT -3.3) = checkdown habit. Blitzed 14 db: 6/12 63 yds; not blitzed 10 db: 4/9 28. Pressured (PROXY) 9 db: 2/6, 3 sacks. Flowers 4 targets, 0 catches (incl. the INT) - Rico's "no throws to Flowers" is not literally right; he was targeted 4x but never connected (5 per ESPN with Huntley's).
- BAL D: blitz 33.3% (last4 36.1%), pressure PROXY 24.1% (4th); allows TE 7.48 YPT (n50, league 7.17) and WR 9.18.

## 5. Form
BAL lost 3 straight; JAX beat IND 42-7. Strange 2 tgts/55 last game (blowout, low volume). Fagnano 1 NFL game.

## 6. Weather: to be confirmed via tools/weather_forecast.py (NWS/Open-Meteo). Read assumes no flag.

## 7. Edge players (max 2)
1. **Derrick Henry rush yds UNDER** — Edge: elite JAX run D (3.28 RB YPC) + 10-pt dog script + stacked boxes vs a QB who can't punish them + 2 Q interior OL. Must be true: BAL trails, ≤16 carries. Kills it: Flip B (close game, 20+ carries) or one 40-yd run. Confidence: LEAN-STRONG. Fits the validated rush-under baseline.
2. **Justice Hill receptions/receiving OVER (BAL checkdown back)** — Edge: rookie QB checked down to him 6x (29%), JAX allows 81.8% catch rate to RBs, trailing script feeds checkdowns. Must be true: Hill active (Q groin, LP) and keeps the 3rd-down role. Kills it: Hill limited/inactive, BAL runs more. Confidence: LEAN; injury-role/backup-QB leg -> +7 bar.
Secondary (team markets): JAX -10 / 1H JAX consistent with base; BAL team total under consistent with base + Flip A.
Avoid: Flowers/Bateman yardage overs (QB can't get him the ball; Flowers 0/4), any JAX WR yards over in a run-out script.

## 8-10. Data check, market, pre-mortem: after pricing (report.md). Pre-mortem seed: Henry under dies if BAL's D keeps it close and Minter leans on Henry 22+ times to protect the rookie — the most likely loss path.
## 11. Slip story: "JAX controls, BAL offense stalls": Henry rush under + BAL team total under/JAX spread + Lawrence rush under; no overs that need BAL passing volume except checkdown RB catches.
