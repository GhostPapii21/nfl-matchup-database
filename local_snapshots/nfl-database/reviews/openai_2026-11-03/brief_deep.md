# NEW SECTION FIRST: v6 2026 graded results (backtests/v6_brainstorm_proedge/results.md)
Headline: READS wk3-8 42.3%, -19.1% ROI; slips 0/30; GATED 41.5%, -21.6%; every-main-rush-under baseline 56.4%, +2.8%.
# v6 graded results (separate buckets; never blended)

## READS (every Grok edge leg, pre-gate)

### (a) 2026 wk3-8 priced (ROI on priced legs only; hit rate on all settled)

```
all: 66-90 (42.3%) | ROI -264.95 on 139 (-19.1%)
 week           W_L                pl_roi  unres
    3 11-19 (36.7%) -51.42 on 22 (-23.4%)      1
    4 10-18 (35.7%) -72.08 on 26 (-27.7%)      2
    5  8-18 (30.8%) -80.76 on 23 (-35.1%)      0
    6 10-13 (43.5%) -50.92 on 22 (-23.1%)      1
    7 14-12 (53.8%) -23.35 on 23 (-10.2%)      0
    8 13-10 (56.5%)  +13.57 on 23 (+5.9%)      1

    market           W_L                 pl_roi  unres
    recyds 43-53 (44.8%) -116.60 on 83 (-14.0%)      3
rushrecyds   6-8 (42.9%)  -17.67 on 13 (-13.6%)      1
   rushyds 17-29 (37.0%) -130.69 on 43 (-30.4%)      1

   ou           W_L                  pl_roi  unres
 over 53-76 (41.1%) -248.09 on 113 (-22.0%)      4
under 13-14 (48.1%)    -16.86 on 26 (-6.5%)      1

gate           W_L                 pl_roi  unres
 CUT 17-21 (44.7%)   -27.55 on 29 (-9.5%)      1
FLAG 12-19 (38.7%)  -64.61 on 29 (-22.3%)      0
PASS 37-50 (42.5%) -172.80 on 81 (-21.3%)      4
```

### (b) 2026 wk1-2 STAND-IN lines (hit rate only)

```
all: 29-27 (51.8%)
 week           W_L pl_roi  unres
    1 14-10 (58.3%)    n/a      2
    2 15-17 (46.9%)    n/a      0

    market           W_L pl_roi  unres
    recyds 13-14 (48.1%)    n/a      0
rushrecyds   1-1 (50.0%)    n/a      0
   rushyds 15-12 (55.6%)    n/a      2

   ou           W_L pl_roi  unres
 over 16-19 (45.7%)    n/a      0
under  13-8 (61.9%)    n/a      2
```

### slips 3-4 legs (READS)

```
wk3-8 priced:       slips  won  pl
week                
3         5    0 -50
4         5    0 -50
5         5    0 -50
6         5    0 -50
7         5    0 -50
8         5    0 -50
total 0/30 won, P&L -300.00
wk1-2 stand-in (hit only):       slips  won
week            
1         5    1
2         5    0
```

### slips 6-7 legs (READS)

```
wk3-8 priced:       slips  won  pl
week                
3         2    0 -20
4         3    0 -30
5         3    0 -30
6         2    0 -20
7         3    0 -30
8         3    0 -30
total 0/16 won, P&L -160.00
wk1-2 stand-in (hit only):       slips  won
week            
1         3    0
2         4    0
```

## GATED (PASS+FLAG after data check, incl. mirror overs)

### (a) 2026 wk3-8 priced (ROI on priced legs only; hit rate on all settled)

```
all: 49-69 (41.5%) | ROI -237.41 on 110 (-21.6%)
 week           W_L                pl_roi  unres
    3  8-14 (36.4%) -49.16 on 18 (-27.3%)      1
    4  4-13 (23.5%) -94.83 on 17 (-55.8%)      1
    5  4-14 (22.2%) -85.40 on 16 (-53.4%)      0
    6  9-12 (42.9%) -40.92 on 21 (-19.5%)      1
    7 12-11 (52.2%) -22.12 on 21 (-10.5%)      0
    8  12-5 (70.6%) +55.02 on 17 (+32.4%)      1

    market           W_L                 pl_roi  unres
    recyds 37-47 (44.0%) -131.97 on 77 (-17.1%)      2
rushrecyds   5-6 (45.5%)    -6.44 on 10 (-6.4%)      1
   rushyds  7-16 (30.4%)  -99.00 on 23 (-43.0%)      1

   ou           W_L                 pl_roi  unres
 over 44-57 (43.6%) -171.00 on 94 (-18.2%)      3
under  5-12 (29.4%)  -66.40 on 16 (-41.5%)      1

gate           W_L                 pl_roi  unres
FLAG 12-19 (38.7%)  -64.61 on 29 (-22.3%)      0
PASS 37-50 (42.5%) -172.80 on 81 (-21.3%)      4
```

### (b) 2026 wk1-2 STAND-IN lines (hit rate only)

```
all: 20-12 (62.5%)
 week          W_L pl_roi  unres
    1 10-6 (62.5%)    n/a      0
    2 10-6 (62.5%)    n/a      0

    market          W_L pl_roi  unres
    recyds  9-8 (52.9%)    n/a      0
rushrecyds   0-1 (0.0%)    n/a      0
   rushyds 11-3 (78.6%)    n/a      0

   ou          W_L pl_roi  unres
 over 11-6 (64.7%)    n/a      0
under  9-6 (60.0%)    n/a      0
```

### slips 3-4 legs (GATED)

```
wk3-8 priced:       slips  won     pl
week                   
3         4    0 -40.00
4         4    0 -40.00
5         4    0 -40.00
6         5    0 -50.00
7         5    0 -50.00
8         4    1  85.27
total 1/26 won, P&L -134.73
wk1-2 stand-in (hit only):       slips  won
week            
1         4    0
2         3    0
```

### slips 6-7 legs (GATED)

```
wk3-8 priced:       slips  won  pl
week                
3         2    0 -20
4         2    0 -20
5         2    0 -20
6         2    0 -20
7         2    0 -20
8         2    0 -20
total 0/12 won, P&L -120.00
wk1-2 stand-in (hit only):       slips  won
week            
1         2    0
2         2    0
```

## Baselines: every main rush-yds under

```
wk3-8 saved: 296-229 (56.4%) ROI +116.45 on 421 (+2.8%)
 week           W_L                pl_roi  unres
    3 51-44 (53.7%)  -43.40 on 74 (-5.9%)      2
    4 56-37 (60.2%) +93.21 on 81 (+11.5%)      2
    5 50-38 (56.8%)  +68.69 on 72 (+9.5%)      1
    6 50-35 (58.8%)   +6.43 on 62 (+1.0%)      2
    7 45-38 (54.2%)  -22.91 on 66 (-3.5%)      5
    8 44-37 (54.3%)  +14.42 on 66 (+2.2%)      4
wk1-2 stand-in: 66-41 (61.7%)
```

## (d) saved pre-kick reads vs reconstructed

```
SAVED_READ (Ghost6 13d41b9 + w8 checklists, graded in v5): 7-7 (50.0%) ROI +13.50 on 8 (+16.9%)
v6 Grok on the same saved-read games: 4-14 (22.2%) ROI -93.76 on 15 (-62.5%)
v6 Grok RECONSTRUCTED, all other wk3-8 games: 62-76 (44.9%) ROI -171.20 on 124 (-13.8%)
```

# Brief: NFL player-prop backtest program (for external critique)
Context: hobby research group building NFL player-prop parlays (FanDuel/PrizePicks, 3-4 leg yardage slips, no TD legs, no passing-yards legs). LLM agents do per-game "brainstorm" reads; Python 100k-sim models; a rulebook gate. Constraints: free data only (ESPN, nflverse/PFR-type public stats, public news); NO PFF, no film, no reliable man/zone/coverage data; Odds API ~250 credits/week, no historical pulls until Dec; saved prices only for 2026 Wk3-8. Sample: 2026 Weeks 1-8 so far.
Key rules (PHASE_SCRIPT.md): §7 leg must clear line in 3 of last 4 games with current QB; +3 edge vs no-vig price; SCHEME_EDGE is a flag not a cut; N1-N3 checks; depth-receiver rule; mirror overs; one slip per player; freshness coverage 48h/injuries 6h/odds 1h.
Headline results (full source reports appended below, file paths given):
- Confidence check: all 9 sim versions had worse Brier than market (0.248) and than coin flip (0.250).
- Wk6-8 rulebook replay: pool 463 legs 52.1%, -$570; Test A slips 20/245 -$1,070; Test B 2/124 -$429; rush-yds unders 76.9%. Priced replay: 293 passed legs hit 48.5% while model said ~67%.
- Week 8 "Rico method" v1: 34 legs 50%, -$35.63, slips 0/8.
- v5 (LLM brainstorm + ZONE_MOF + PRO_EDGE tags, Grok): train Wk3-6 43.8% vs holdout Wk7-8 60.8%; slips 4/29 (holdout 9/25 cited elsewhere). Possible LLM hindsight leakage.
- Leak audit (partial, backtests/v5_leak_audit/): prompt audit 33 checks clean; no-context forced winner guesses 14/27 (coin flip), 2025 4/10; model denies knowing results; masked (names/dates hidden) rerun in progress.
- Postmortems: game-script failures (4th-quarter run-outs killing pass/rec legs), correlated legs failing together.
Known flaws: small samples, approximated pro-edge/phase steps, many rule tweaks after seeing results, depth-receiver results mixed.

=== FILE: PHASE_SCRIPT.md ===
# NFL Custom Phase Script — Full Model (Updated Oct 30, 2026)
<!-- Data/workflow authority: GAME_SCRIPT_2026-10-29.md (phases 0-10G, 60 checks, ticket cap 6 target / 7 max) — run it alongside this model; where they conflict, the game script governs evidence rules. Permanent projection model, stored verbatim from the user on Oct 29, 2026. Supersedes the Oct 27 version. Rico's data-collection phases 1-8 live in MASTER_PROMPT.md. -->

## CORE PIPELINE (Oct 29 user-approved order; the Opportunity Gate is step 4)
0. Injury & status check: Questionable players are not cut automatically. Script them on low alts or fade. At 90 min pre-kick, ask the user to approve each inactive or Questionable player who matters.
1. Identify locked roles for both teams
2. Pull defensive coverage profile (YPT by position/route, Outside YPT, blitz %, zone vs man %, explosive plays allowed, RZ TD%, 3rd-down % allowed, run YPC allowed) plus HC/OC/DC tendencies
3. Game environment: spread, total, pace, projected script (who leads, who trails), whether each offense can sustain drives (3rd-down and red-zone rates vs this defense)
2A. DEFENDER COVERAGE CHECK (HARD, user rule Oct 31, 2026; no leg skips it): for every WR/TE/RB receiving leg, pull real defender numbers from Pro Football Reference advanced defense (free: targets, completions, comp %, yards, YPT, passer rating allowed per CB/S/LB), plus man/zone and MOF open/closed from nflverse FTN charting. Map the player to his likely defender, show whether that defender limits catches or yards, and match the player's routes (NGS/FTN) to that coverage. Stand-ins don't count; a leg missing this is cut. Full rule: the nfl-betting-script skill, section 8A.
4. OPPORTUNITY GATE: project this game's targets / carries (see section below). No volume, no leg.
5. Grade each player by role vs opponent defense
6. Apply triggers (blitz volume cut, run suppression ≤3.8 YPC, soft matchup boost, injury boost, blowout / trailing script)
7. Recent environment match (did the player hit high numbers vs similar defensive profiles this season / 2025)
8. Generate base projections (volume × efficiency)
9. Run through three-model consensus with tools/sim_v6.py (100k each: Monte Carlo, calibrated Bias, Game Randomness; gate requires sim_v6 for runs dated >= 2026-11-05) → true median
10. Pull FanDuel or DraftKings main line (and relevant alts)
11. Compare model MAIN/Median to the line → call Over / Under / Alt / No Bet
12. Output projection sheet with percentile labels and betting lean
Markets: receiving yds, receptions, rush+rec yds, rushing yds (O/U). Anytime TDs on separate slips. Passing yds only on a clear over.

## ROLE CATEGORIES (Locked Guidelines)
- **Rush-Receive Back**: Significant receiving volume + rush production (e.g. McCaffrey, Kyren when targeted, Stevenson, Josh Jacobs when involved)
- **Goal-Line / RZ Back**: Primary red-zone / goal-line carries
- **Elite Rusher**: High YPC or volume; soft run D (>4.4 YPC) = Positive grade
- **Volume Receiver**: High target share, steady receptions (boost capped +2–3%)
- **Explosive Receiver**: Big plays, deep/outside routes; grade primarily off Outside YPT
- **TE-as-Primary**: Tight end used as the main receiving option (e.g. McBride, Kittle, Bowers)
- **WR2 / WR3 / Check-Down**: Secondary options; lower volume expectations
- **Blitz Check-Down**: Primary target when defense blitzes (often RB or TE)

## DEFENSIVE PROFILE RULES
- Soft Outside YPT (≥10.5) → Positive for Explosive / Boundary receivers
- Soft WR YPT (≥9.0) → Slight Positive for Volume receivers (capped)
- Soft TE YPT (≥8.0) → Positive for TE-as-Primary
- Soft RB receiving YPT → Positive for Rush-Receive backs
- Hard TE YPT (≤5.5) → Cut yards on TE-as-Primary (volume may still hold)
- Run YPC allowed ≤3.8 → Run Suppression trigger (cut rush yards)
- Run YPC allowed >4.4 → Positive for Elite Rushers
- High blitz rate → Volume cut on primary receivers; boost check-down roles

## PERCENTILE STRUCTURE (Projection Sheet Labels)
- Floor (5th percentile)
- Slight Edge (10th)
- MAIN (15th) — primary betting number
- Edge (20th)
- Pure Edge (25th)
- Median (three-model consensus)

## BETTING LINE PROCESS (New — Oct 27 / Updated Oct 29)
1. After three-model true median is set, pull FanDuel or DraftKings main line for the prop.
2. Compare model number to the available line.
3. If model is clearly under the line, consider lower alt lines (e.g. if main is 75.5 and model sees under 65, check 60.5 or 55.5 alts for better price).
4. Call the side only when there is separation. If price is poor or line is already close, mark No Bet.
5. Post-game scoring is done only against the actual line (or chosen alt), not against the raw model number.
6. Injury during game = bet protect (do not count as miss).

## ADDITIONAL TRIGGERS & NOTES
- Injury boost: Clear opportunity increase for remaining players.
- Recent performance environment match: If player has hit high marks vs similar defensive profiles this season or 2025, slight additional boost.
- Low game total / low-volume script: Reduce soft-matchup boosts (do not force Overs in low-scoring environments).
- Blowout risk: Adjust volume in later quarters when one team is heavily favored.
- Red-zone usage: Boost TD probability for primary RZ players; do not automatically boost yardage.

## OUTPUT FORMAT
For each key player:
- Role
- Grade (Positive / Neutral / Slight Negative) + reason
- Percentiles (5th / 10th / 15th MAIN / 20th / 25th / Median)
- Available FanDuel/DraftKings line
- Lean (Over / Under / Alt X.X / No Bet)
- Notes (triggers applied, injury protect if applicable)

## EXAMPLE ROLE LOCKS (Reference)
- Rams: Puka Nacua (Volume), Davante Adams (Explosive/RZ), Kyren Williams (Rush-Receive)
- Cardinals: Trey McBride (TE-Primary), Michael Wilson (Explosive)
- 49ers: McCaffrey (Rush-Receive + Elite), Kittle (TE-Primary), Evans/Deebo (Explosive)
- Buccaneers: Irving (Rush-Receive), Godwin (Volume), Egbuka (Outside), Otton (TE)
- Packers: Josh Jacobs (Rush-Receive), Christian Watson (Volume/Outside), Matthew Golden (Explosive), Tucker Kraft (TE)
- Panthers: Chuba Hubbard (Elite Rusher), Tetairoa McMillan (Volume), Jalen Coker (WR2)

## RUN DEFENSE EXAMPLES (from the Oct 27 version)
- Bears: 4.44 YPC, 87.6 yds/G (Mixed)
- Cowboys: 4.72 YPC, 145.7 yds/G (Soft)
- Saints: 4.81 YPC, 139.4 yds/G (Soft)

Full model is permanent. Use this pipeline for every matchup. All role guidelines, defensive profile rules, three-model consensus, and FanDuel/DraftKings line comparison are required before final leans.

## OPPORTUNITY GATE (User rule, Oct 29, 2026 — runs BEFORE any matchup boost)
A soft defensive matchup only matters if the player gets the volume to use it. Season averages are not opportunity.
1. Project this game's volume first: expected team plays (pace + spread/game script), pass/run split, then the player's share.
   - Receivers/TEs: projected targets = projected team pass attempts × player's L3 target share (fix_player_role / fix_player_game_usage). Receptions line needs projected targets × catch rate ≥ line with margin; yards = targets × yards per target.
   - RBs: projected carries = projected team rushes × L3 carry share; adjust down when the team projects to trail (Henry Wk7, Walker Wk7).
2. Check the opponent's tendency against this team's structure: does this defense force the ball elsewhere (e.g., run-heavy script pulls targets off the TE — LaPorta Wk7: 97% snaps, 2 targets; DET ran Gibbs 29 times)?
3. Check the offense can sustain drives against this defense (3rd-down rate, red-zone rate, explosive allowed). If not, cap RB yards and kill TD legs (Walker Wk7: 14 of 16 KC carries, 36 yds, KC scored 3).
4. Only then apply the defensive-profile boost (outside vs slot, explosive allowed, zone/man).
5. If projected volume does not support the line → No Bet or a lower rung, no matter how soft the matchup.
6. Volatile-yards receivers (big week-to-week swings) get moderate rungs even on high volume (Golden Wk7: 12 targets, 39 yds).
7. Avoid volume legs on players whose team projects to be blown out, except receivers in garbage-time volume roles (with caution).

## POSTMORTEM AMENDMENTS — CAR@GB (user-approved Oct 30, 2026)
Source: postmortems/CAR_GB_2026-10-29.md. Apply on top of the Opportunity Gate and the defensive profile rules.
1. **Bryce Young under rule (user's rule).** Bryce Young is an UNDER on passing yards and completions against heavy-blitz or high-pressure defenses, and his secondary WRs (Coker, Waller, Tremble, Metchie) get frozen out as he checks down to RBs/TEs. Strengthen it when CAR's OL is depleted. Evidence: 23/41, 209, 5.1 YPA, 6 sacks, 9 QB hits vs GB; second straight game after TB.
2. **Young checkdown back over.** When rule 1 is active, lean toward Hubbard's receptions (and receiving yards) overs: 7 rec on 8 targets here vs a 2.4-rec median.
3. **Coverage shell beats per-player under.** Don't play unders on an offense's top WRs/receiving TE when the opponent runs single-high Cover 3 with a depleted secondary (Watson U4.5 and Kraft U4.5 both lost here). Require the shell read and the lean to agree.
4. **Injury contingency for active Questionable WRs.** When a Questionable WR is active and a teammate WR goes down, project him as the top target (Golden went from 1 to 12 targets). Pre-game, avoid unders on the other WR/TE in that room.
5. **Backup RB rushing legs.** Don't take a backup RB's rushing over (e.g., MarShawn Lloyd 10+) when the lead back is back to a full workload: Jacobs had 21 of 26 GB rushes.
6. **Volume-pass, efficiency-fail on rushing.** Projected carries can pass the gate and still bust behind a depleted interior OL; cap lead-RB rushing yds overs (and SGP rush legs) when the offense is missing its center or two interior linemen, even against a soft run defense (Jacobs 21 for 39 vs CAR's league-worst YPC allowed).
7. **Garbage-time TD caution on secondary WR unders.** For yards unders on a trailing team's secondary WR, check the late-game risk: Coker's 26-yd TD down 14 nearly flipped the under.
8. **Parser check.** Reconcile the live PBP parser to the official box score at FINAL (it missed a scoring-summary-format TD and over-counted Golden's yards by 4).

## Nov 1 2026 lessons (see audits/2026-11-01_lessons/CHECKLIST.md)
1. **Weather.** Any open-air game with rain ≥50%, gusts ≥20 mph or sustained wind ≥15 mph raises a loud WEATHER ALERT. Look at rushing overs first, and re-check every placed leg in that game. The gate enforces this (weather block, weather_stop).
2. **Game script drives RB volume.** If rain, a lopsided spread or a QB collapse is likely, model the run share. Don't use the normal pass split.
3. **RB fixes A, D, E, F are on.** B and C, the RB 2-of-3 Phase 14 rule and the lead-back gate check were declined. Don't re-enable them. Underdog RB legs are not blanket-blocked (fix D).
4. **RB scan.** Any active RB with ≥20% of carries in either of the last 2 games is a rush-yds candidate. Role flips swap RB1/RB2. The depth-chart RB1 has to be passed by hand (`depth_rb1`). Rule 5 is unchanged.
5. **Receiving legs** factor blitz rate, pressure rate, checkdown share, QB time to throw and targets under pressure. The gate requires the last two for runs dated ≥ 2026-11-05.
6. **Run the slate scan and the gate before building any slip.** §7/§14 apply: no leg goes on a slip unless the gate passes it, and §11 is one slip per player.
7. **sim_v6** has calibrated Bias, which replaces the flat volume −8% / catch −3% / yards −5% cuts. Every run dated ≥ 2026-11-05 must use sim_v6.
8. **Press tier** (press_tier.py, live from 2026-11-05) applies only after a normal gate PASS. It never rescues a cut.
9. **PFF** (approved paid source) is for matchups and grades only. Cross-check it against a second dated source. A disagreement or a missing second source is a gate CAUTION, never a pass reason. PFF is never used for weather, game script or a projection; the gate FAILs that.
10. **Postgame review** covers edges missed by category (not in pool / cut by rule / wrong side / variance), ticket grades, defense dissection (rush 15+, rec 20+) and a watch list (postmortems/WATCHLIST_2026.md).
11. **Backtests are analysis only.** The RB receiving game-script backtest (Wk3-8) found no trigger with positive ROI, so no rule was added. pass_volume_cap stays off.
12. **Phase 15 (inactives).** When a starter is out, check the backfield split and how exposed every slip is to that game.

## Phase 11a: days-ahead weather forecast (Rico 2026-11-01; runs ≥ 2026-11-05)
1. At slip build, run `python3 tools/weather_forecast.py --week <N>`. It writes `week<N>/weather_forecast/forecast_*.json`, which is never overwritten, and checks NWS and Open-Meteo for every open-air or unknown-roof game.
2. A game is flagged on precip ≥50%, gusts ≥20 or sustained wind ≥15. In a flagged game, CUT the passing and receiving OVERs and lean toward rushing.
3. The manifest must carry `weather_forecast`, written by `assemble.py`. The gate fails it if it's more than 24h old, or if a game is missing or has no numbers.
4. Refresh daily with the Mon–Sat 10 AM refresh. Phase 11's pre-kick recheck stays.

## Phase 4 addendum: the coverage profile applies to passing legs too (runs ≥ 2026-11-05)
QB passing legs need the opponent's `coverage.man_zone` and `coverage.mof` (sourced, no more than 48h old). The gate fails the leg otherwise.

## Rico rules 2026-11-02 (approved 05:01 ET; runs dated ≥ 2026-11-05; enforced by tools/rico4_rules.py via run_gate)
1. **PRESS manual review.** On a leg press_tier marks PRESS, a P14-only edge cut (edge < +3, shrunk edge ≤ 0, model p < .45, a median does not clear, MODEL-SUSPECT) becomes status MANUAL_REVIEW, not CUT. The leg carries the reason, all 3 model p (MC/bias/GR) and the book price + no-vig. The gate prints a "PRESS MANUAL REVIEW" section; these legs are NEVER live/auto-published, and Ghost6/Rico decide. Non-press legs keep the cut. Weather, inactives/injury, §11, the #3/#4 WR ban and the placed-ticket bar still cut (no MANUAL_REVIEW).
2. **Mirror over.** When an under is cut for soft D (P3), a missing/unverified defender (P4/ISS-05), no-unders-on-stars (P14 primary star), the trailing-team or clock-killing block (P13), build the mirror over at the LOWEST alt rung that clears (avg model p − no-vig ≥ .03, shrunk > 0, min p ≥ .45, every median over the line). It then goes through every normal phase. It records mirror_of = the cut under; with no clearing rung, the under records mirror.no_rung_reason. Gate fails if neither is present.
3. **Target-share pool.** WR/TE players with ≥22% target share (season, OR last 3 games with the current QB; nflverse pbp) join the player pool and slate_scan (trigger tgt_share22). The manifest needs a target_share_pool block (source nflverse pbp); every listed player needs a leg or a skip_reason. #3/#4 WRs stay banned.
4. **QB return.** Flag QB-RETURN when the team QB is back from missing 2+ games or the player's model was built on backup-QB games. Recheck §7 and recent form on current-QB games only (qb_return_recheck {current_qb, games, sec7, form_values}). There is NO automatic rung drop. The gate fails on a live QB-RETURN leg with no recheck, or on a rung_drop that cites the QB return.
Still OFF: YPC floor, pressure cuts.

## SNF postmortem rules 2026-11-02 (Rico approved Nov 2, 8:14 AM ET; source postmortems/2026-11-01_snf.md; runs dated ≥ 2026-11-02, starts MNF CHI@SEA per Rico card Nov 2, 8:19 AM ET; enforced by tools/snf_rules.py via run_gate)
1. **Model-suspect under → manual review with a backfield split + weak backup QB.** An UNDER cut only because the models sit too far below the book (MODEL-SUSPECT) becomes status MANUAL_REVIEW (any tier, not only PRESS) when the leg carries BOTH `backfield_split` {source, detail} documenting a confirmed split AND `backup_qb_card` {grade D/F or WEAK, source}. MANUAL_REVIEW legs are never live; Ghost6/Rico decide. Without both, the MODEL-SUSPECT auto-cut stays (it correctly cut Rachaad White's unders).
2. **WR3+ unders: team coverage can satisfy the named-defender check.** A WR ranked #3 or lower on an UNDER, with no mapped defender, passes the P4 defender check if the leg has the opponent's team coverage profile (`coverage.man_zone` + `coverage.mof`, sourced, ≤48h). The leg is flagged WR3_TEAM_COV and the gate notes it. Overs: the no-#3/#4-WR rule still bans WR3/WR4 overs, except the rule-4 depleted-secondary WR3 exception.
3. **Questionable WR unconfirmed at inactives → shares both ways.** If a Questionable WR is still unconfirmed at the inactives check, rerun target shares with him ACTIVE and INACTIVE and report both. Manifest `questionable_wr: [{name, confirmed_at_inactives, target_shares: {active, inactive}}]`; the gate fails if an unconfirmed entry lacks either set.
4. **Depleted secondary → WR2/WR3 overs join the pool.** When the opposing secondary is missing 2+ corners (starting CBs and/or nickel out), that team's opponents' WR2 and WR3 overs enter the candidate pool. Manifest `depleted_secondary: [{team, cbs_out, wr23_over_pool: [{name, wr_rank, leg | skip_reason}]}]`; every listed receiver needs a leg or a skip_reason. **Exception to the no-#3/#4-WR rule (Rico card Nov 2, 8:19 AM ET; targets floor 8:20 AM ET):** in this condition only, a WR3 over may be published if it clears every other normal gate (§7, edge/models, coverage, weather, inactives, §11, opportunity check not 'mixed') AND the WR3 averages 4+ targets per game over his last 4 games with the current QB (leg field `tpg_last4_cur_qb`). Flag WR3_DEPLETED_SECONDARY_EXCEPTION (replaces BLOCKED_BY_WR34_BAN for this case); 4.0-4.9 targets/g also flag WR3_TARGETS_BORDERLINE, 5+ is full. Below 4 targets/g the WR3 over stays banned. WR4 overs stay banned. Outside this condition the WR3/WR4 over ban is unchanged.

## Rico, Nov 2, 2026, 9:13 PM ET (Betting Hub, his own words): stop lowering found edges
1. **No shrink.** The 30% shrink toward 50% is removed everywhere (tools/run_gate.py, tools/rico4_rules.py, runs/2026-11-05_shared_src/assemble.py, press tier). Legs are judged on the raw average model p vs no-vig; the +3 bar, min p .45 and the medians check stay for normal legs.
2. **SCHEME_EDGE.** When matchup, scheme/coverage fit (how the QB uses the player vs this defense's coverage), game script and recent-form trend all line up (leg field `scheme_edge` with matchup/scheme_fit/script/form_trend, each {ok, source, detail}), §7 and the sim checks become flags, not cuts. The last 2 games with the current QB must still clear. Weather, inactives, §11, the #3/#4 WR ban and the -250 flag still apply. Ghost6 vets at a real price. Test cases: Loveland rec and Burden rec/yds, MNF Nov 2.
3. **Overs for every candidate.** The mirror over (R2) starts now (runs dated 2026-11-02+) and is built for any cut under except weather, injury/inactive, §11 or #3/#4 stops. The press tier is also on from 2026-11-02.
4. **Still open (backtest for Rico, not changed):** sim_v5 `oppadj shrink=0.5` halves each defense's matchup effect. Backtest it at full strength on Weeks 1–8.

=== FILE: backtests/confidence_check_2026-11-03/report.md ===
# NFL confidence check — Brier / log loss vs market (Tue Nov 3 2026, TEST ONLY)

Nothing was bet or sent. **No Odds API credits were spent** (0 pulls); every price is from data already saved in the repo.
Originals were not edited: the sim code here is in scratch copies under `engines/` (patch list below).

## Plain verdict
- **All 9 model versions score worse than the market's no-vig probabilities.** All 9 also score worse than a flat 50% guess (Brier 0.2500).
  Every Brier gap vs the market has a game-clustered 95% CI that sits fully above zero.
- **No shrink is worse than the market:** Brier +0.024 and log loss +0.065 to +0.069, on all three sims. It is also clearly worse than the old 30% shrink, which itself is +0.012 worse than the market.
- **Full-strength oppadj (1.0) is worse still**, both vs the market (+0.029) and vs half strength (another +0.004 to +0.005 Brier on top of no-shrink), on all three sims.
- The sims barely differ from each other. sim_v5, sim_v6 and sim_v6_fix are within about 0.001 Brier of one another in every version.
- **Why:** the models have almost no resolution. When the model says 70–80% or 80%+, the leg hits about 45–55%, about the same as its 50–55% bin. Removing the shrink just stretches that noise further from 50%.
  The NBA result had the same shape (BetGuru: no-shrink Brier 0.289 vs market 0.248, and full matchup factor worse).

### Recommendation (applying the task's rule)
1. **Keep oppadj at half strength (0.5).** Full strength scores worse than the market, and worse than half strength, on every sim.
   Production `tools/sim_v6.py` and Thursday's `runs/2026-11-05_shared_src/sim_v5.py` currently run it at 1.0 (phase3 commit 6322cc5). Reverting is a code change under the edit hold, so it is listed here and not made.
2. **FLAG FOR RICO:** no-shrink scores worse than the market (and worse than the old shrink) on every sim. Under Rico's Nov 2, 9:13 PM ET rule this is **his call. Nothing is changed without his OK.**
3. Context for Rico, not a rule change: even the old shrink is worse than the market. No version showed +3 edges that make money. Flat $10 on every +3 leg loses 3.7–5.8% under every version.

## Main table (same 2,411 legs in all 9 rows; Brier/log loss scored on the Over side; log loss clips p to [0.001, 0.999])
| sim | version | N legs | Brier | log loss | market Brier | market log loss | Δ Brier vs mkt (95% CI, game-clustered) |
|---|---|---|---|---|---|---|---|
| sim_v5 | V1 old (30% shrink, opp 0.5) | 2411 | 0.2602 | 0.7159 | 0.2481 | 0.6894 | +0.0121 (+0.0057 to +0.0186) |
| sim_v5 | V2 no shrink, opp 0.5 | 2411 | 0.2730 | 0.7581 | 0.2481 | 0.6894 | +0.0249 (+0.0157 to +0.0334) |
| sim_v5 | V3 no shrink, opp 1.0 | 2411 | 0.2770 | 0.7716 | 0.2481 | 0.6894 | +0.0289 (+0.0189 to +0.0388) |
| sim_v6 | V1 old (30% shrink, opp 0.5) | 2411 | 0.2600 | 0.7154 | 0.2481 | 0.6894 | +0.0119 (+0.0056 to +0.0183) |
| sim_v6 | V2 no shrink, opp 0.5 | 2411 | 0.2724 | 0.7557 | 0.2481 | 0.6894 | +0.0243 (+0.0156 to +0.0331) |
| sim_v6 | V3 no shrink, opp 1.0 | 2411 | 0.2767 | 0.7690 | 0.2481 | 0.6894 | +0.0286 (+0.0183 to +0.0388) |
| sim_v6_fix | V1 old (30% shrink, opp 0.5) | 2411 | 0.2600 | 0.7152 | 0.2481 | 0.6894 | +0.0119 (+0.0055 to +0.0182) |
| sim_v6_fix | V2 no shrink, opp 0.5 | 2411 | 0.2723 | 0.7547 | 0.2481 | 0.6894 | +0.0241 (+0.0156 to +0.0329) |
| sim_v6_fix | V3 no shrink, opp 1.0 | 2411 | 0.2771 | 0.7699 | 0.2481 | 0.6894 | +0.0290 (+0.0194 to +0.0390) |

Reference: a constant 50% gives Brier 0.2500 and log loss 0.6931. The actual Over hit rate on these legs is 48.4%. The model's mean Over p is 0.43–0.48 against a market mean of 0.497, so the models lean Under.

**Brier by week, sim_v6** (market in brackets):

- W3 0.278 / 0.301 / 0.308 [0.250]
- W4 0.263 / 0.279 / 0.286 [0.250]
- W5 0.260 / 0.272 / 0.275 [0.250]
- W6 0.254 / 0.263 / 0.267 [0.248]
- W7 0.250 / 0.257 / 0.259 [0.245]
- W8 0.264 / 0.277 / 0.279 [0.248]
- MNF 0.252 / 0.257 / 0.283 [0.250] (29 legs)

The values are V1 / V2 / V3. The model loses to the market in every week under every version.

**Brier by market, sim_v6, V1 / V2 / V3** [market]:

- passyds 0.268 / 0.283 / 0.292 [0.248]
- rec 0.249 / 0.256 / 0.257 [0.243]
- recyds 0.262 / 0.275 / 0.281 [0.250]
- rushrec 0.269 / 0.286 / 0.294 [0.250]
- rushyds 0.261 / 0.276 / 0.276 [0.249]

Rushyds V2 = V3 in sim_v5/v6 because oppadj only touches the receiving and passing factors there. The rushing YPC opponent factor is already full strength in every version. Files: `brier_by_week.csv`, `brier_by_market.csv`.

Cross-check vs the earlier Weeks 6–8 replay (model 0.267 vs market 0.247): this run on W6–8 gives sim_v6 V3 0.259–0.279 vs market 0.245–0.248. Same direction, similar size.

## Flat $10 on every leg clearing +3 pts vs no-vig (the side with model p − no-vig ≥ 0.03; price = the saved book price for that side, FanDuel when quoted)
| sim | version | bets | W–L | hit | P/L ($10 flat) | ROI | mean model p (bet side) |
|---|---|---|---|---|---|---|---|
| sim_v5 | V1 old (30% shrink, opp 0.5) | 1929 | 965–964 | 50.0% | -1,044.38 | -5.4% | 0.607 |
| sim_v5 | V2 no shrink, opp 0.5 | 2062 | 1057–1005 | 51.3% | -753.13 | -3.7% | 0.649 |
| sim_v5 | V3 no shrink, opp 1.0 | 2091 | 1056–1035 | 50.5% | -1,081.92 | -5.2% | 0.659 |
| sim_v6 | V1 old (30% shrink, opp 0.5) | 1916 | 965–951 | 50.4% | -902.82 | -4.7% | 0.605 |
| sim_v6 | V2 no shrink, opp 0.5 | 2054 | 1046–1008 | 50.9% | -865.40 | -4.2% | 0.646 |
| sim_v6 | V3 no shrink, opp 1.0 | 2081 | 1043–1038 | 50.1% | -1,210.92 | -5.8% | 0.656 |
| sim_v6_fix | V1 old (30% shrink, opp 0.5) | 1898 | 946–952 | 49.8% | -1,084.20 | -5.7% | 0.605 |
| sim_v6_fix | V2 no shrink, opp 0.5 | 2046 | 1039–1007 | 50.8% | -949.09 | -4.6% | 0.646 |
| sim_v6_fix | V3 no shrink, opp 1.0 | 2077 | 1045–1032 | 50.3% | -1,147.51 | -5.5% | 0.657 |

- The models disagree with the market by 3+ points on 80–87% of legs: the mean |model − market| is 9 pts with the shrink and 13–14 pts without it. That alone says the numbers aren't market-grade.
- V2 (no shrink, opp 0.5) loses the least in all three sims. It still loses 3.7–4.6% and hits 50.8–51.3%.
- Unders hit 51–52% and overs 48–50%; both sides lose money. Week 8 is the worst week for every version (−$341 to −$493). Detail is in `plus3_bets.csv`.

## Calibration highlights (full tables for all 9 rows below and in `calibration.md`)
- **sim_v6 V2 (no shrink, opp 0.5), model-favored side:**
  - 50–55%: 49.7% actual (n 602)
  - 55–60%: 53.7%
  - 60–65%: 50.6%
  - 65–70%: 54.1%
  - 70–80%: 49.3% (n 371)
  - 80%+: 52.5% (n 162; mean prediction 87%)
- **sim_v6 V3 (opp 1.0):**
  - 70–80%: 50.4% (n 413)
  - 80%+: 50.2% (n 201; mean prediction 87.5%)
- **Over-side 0–40% bin:** the model predicts 28–33% but overs hit 47–48% in every version, so the model is much too low on overs it dislikes.
- **The old shrink is the least overconfident, and it still has no lift:** 65–70% → 49.8%, 70–80% → 51.4%.
- The market's own no-vig stays within about 49–51% in every bin. The legs the model is sure about are coin flips that the market priced as coin flips.

## Data coverage (real prices; legs used before the all-6-runs intersection)
| week | passyds | rec | recyds | rushrec | rushyds | games |
|---|---|---|---|---|---|---|
| 3 | 0 | 0 | 186 | 48 | 96 | 16 |
| 4 | 0 | 0 | 190 | 47 | 95 | 16 |
| 5 | 0 | 0 | 172 | 44 | 89 | 15 |
| 6 | 27 | 173 | 173 | 46 | 83 | 14 |
| 7 | 28 | 171 | 172 | 42 | 80 | 14 |
| 8 | 26 | 152 | 155 | 41 | 83 | 13 |
| MNF CHI@SEA | 2 | 11 | 11 | 0 | 5 | 1 |

- **Weeks 1–2: no real prices are saved, so they are not covered.** I found no Odds API snapshot for them anywhere in the repo.
- **Weeks 3–5:** only rec yds, rush yds and rush+rec yds main lines exist (from `backtests/yardage_markets_wk3_8/raw`, pulled this morning). There are no receptions or passing yards prices.
- **Weeks 6–8:** passyds, rec, recyds and rushyds main lines (from `current_rules_wk6_8` real_lines), plus rush+rec yds from the yardage raw.
- **MNF CHI@SEA Nov 2:** 29 main-line props (from `rulebook_replay_wk6_8/mnf_lines.csv`). Actuals come from the ESPN box in that replay.
- **What counts as a leg:**
  - One main line per player-market, with no alts.
  - Half-point lines only, so there are no pushes.
  - The player must be active (graded from nflverse pbp, `runs/2026-11-02_shared_src`).
- **Price data:**
  - Snapshots were taken 29–39 min before kickoff (median 34 min). These are near-close lines, not exact closing lines.
  - No-vig = the mean two-way multiplicative no-vig across books quoting the modal line.
- **Leg counts:**
  - 2,448 legs were built. 43 quotes could not be name-matched and were dropped.
  - **2,411 legs** had a valid sim in all 6 engine × oppadj runs. The excluded legs are sims that error on thin pre-cutoff history (mostly Week 3).
  - Legs are correlated within games, so the CIs are bootstrapped by game (89 games).

## Method
- **Three versions:**
  - V1 = old rules: oppadj 0.5, then p' = 0.5 + 0.7(p − 0.5) on the 3-model average.
  - V2 = oppadj 0.5 with no shrink.
  - V3 = oppadj 1.0 with no shrink.
  - Model p is the mean of the mc, bias and gr P(stat ≥ line), the same as the gate's `avg(p)`.
- **Leak-free inputs:**
  - Every engine sees only pbp with game_date before the first game of week W (MNF: before 2026-11-02).
  - Spreads are the nflverse pregame `spread_line`.
  - sim_v6 and sim_v6_fix per-market multipliers were **refit walk-forward** with each engine's own `fit()`. The fit used its saved residual file restricted to weeks < W: none for W3–4, W4 for W5, and so on, up to W4–7 for W8 and MNF.
  - The committed `sim_v6_calib.json` files were not used, because they were fit on Week 4–7 outcomes inside the test window.
- **Scratch patches in `engines/`:**
  - oppadj strength comes from env `CC_OPP`.
  - sim_v6_fix's bias-model `BIAS_OPP` follows `CC_OPP` too, so V2 is its shipped 0.5 and V3 is 1.0.
  - sim_v5 gets a date cutoff and a gsis lookup. Its flat bias haircut (.92/.97/.95) is kept as written.
  - No other logic changed. sim_v5's base is `runs/2026-11-01_shared_src/sim_v5.py`, whose original oppadj default is 0.5.
- **Simulation size:** 20,000 sims per model per leg with a fixed seed. Monte-Carlo error on p is about ±0.004, which is negligible against the 0.012–0.029 Brier gaps.
- **Not modeled** (same as the prior replays): `current_qb` filter, RB script/promotion boosts, weather and inactives. This is the raw sim layer the gate's edge math uses.
- **Reproduce:** `python3 build_legs.py`, then `run_sims.py <engine> <opp> <week>` for each job (see `sims.log`), then `python3 analyze.py` and `python3 make_report.py`.

## Caveats
- The Odds API balance is lower than the shared notes say. `backtests/yardage_markets_wk3_8/raw/credits.log` shows the Yardage pull this morning went from 5,449 to **3,623 remaining** (1,826 used, ending 06:47 ET). This check used 0 credits.
- Week 1–2 coverage is zero, and Weeks 3–5 have yardage markets only. Passing yards is just 83 legs, and passyds is already off slips per Rico.
- No closing-line feed exists. Prices are about T-35 min snapshots.

## Full calibration tables

### sim_v5 — V1 old (30% shrink, opp 0.5)
Over-side probability bins:

| bin | n | mean pred | actual hit | market nv |
|---|---|---|---|---|
| 0-40 | 694 | 0.326 | 0.478 | 0.491 |
| 40-50 | 894 | 0.451 | 0.481 | 0.497 |
| 50-55 | 350 | 0.525 | 0.486 | 0.500 |
| 55-60 | 261 | 0.572 | 0.513 | 0.506 |
| 60-65 | 124 | 0.621 | 0.500 | 0.503 |
| 65-70 | 56 | 0.675 | 0.518 | 0.512 |
| 70-80 | 30 | 0.731 | 0.533 | 0.510 |
| 80+ | 2 | 0.811 | 0.000 | 0.501 |

Model-favored side (prob of the side the model leans):

| bin | n | mean pred | actual hit | market nv (same side) |
|---|---|---|---|---|
| 50-55 | 812 | 0.525 | 0.500 | 0.501 |
| 55-60 | 693 | 0.573 | 0.522 | 0.505 |
| 60-65 | 416 | 0.624 | 0.524 | 0.507 |
| 65-70 | 274 | 0.674 | 0.496 | 0.509 |
| 70-80 | 187 | 0.739 | 0.524 | 0.510 |
| 80+ | 29 | 0.830 | 0.586 | 0.510 |

### sim_v5 — V2 no shrink, opp 0.5
Over-side probability bins:

| bin | n | mean pred | actual hit | market nv |
|---|---|---|---|---|
| 0-40 | 938 | 0.285 | 0.471 | 0.491 |
| 40-50 | 650 | 0.449 | 0.492 | 0.498 |
| 50-55 | 242 | 0.524 | 0.479 | 0.499 |
| 55-60 | 228 | 0.573 | 0.522 | 0.505 |
| 60-65 | 152 | 0.620 | 0.474 | 0.503 |
| 65-70 | 99 | 0.670 | 0.515 | 0.506 |
| 70-80 | 75 | 0.745 | 0.520 | 0.509 |
| 80+ | 27 | 0.845 | 0.519 | 0.507 |

Model-favored side (prob of the side the model leans):

| bin | n | mean pred | actual hit | market nv (same side) |
|---|---|---|---|---|
| 50-55 | 567 | 0.525 | 0.504 | 0.501 |
| 55-60 | 553 | 0.574 | 0.505 | 0.503 |
| 60-65 | 413 | 0.621 | 0.518 | 0.506 |
| 65-70 | 319 | 0.673 | 0.536 | 0.508 |
| 70-80 | 373 | 0.744 | 0.501 | 0.509 |
| 80+ | 186 | 0.869 | 0.538 | 0.510 |

### sim_v5 — V3 no shrink, opp 1.0
Over-side probability bins:

| bin | n | mean pred | actual hit | market nv |
|---|---|---|---|---|
| 0-40 | 999 | 0.276 | 0.478 | 0.492 |
| 40-50 | 561 | 0.449 | 0.501 | 0.499 |
| 50-55 | 249 | 0.524 | 0.438 | 0.497 |
| 55-60 | 216 | 0.571 | 0.523 | 0.504 |
| 60-65 | 165 | 0.622 | 0.461 | 0.507 |
| 65-70 | 106 | 0.671 | 0.481 | 0.503 |
| 70-80 | 85 | 0.744 | 0.588 | 0.509 |
| 80+ | 30 | 0.850 | 0.500 | 0.510 |

Model-favored side (prob of the side the model leans):

| bin | n | mean pred | actual hit | market nv (same side) |
|---|---|---|---|---|
| 50-55 | 531 | 0.526 | 0.460 | 0.499 |
| 55-60 | 495 | 0.574 | 0.521 | 0.503 |
| 60-65 | 442 | 0.622 | 0.489 | 0.506 |
| 65-70 | 309 | 0.672 | 0.540 | 0.508 |
| 70-80 | 403 | 0.747 | 0.519 | 0.508 |
| 80+ | 231 | 0.873 | 0.524 | 0.509 |

### sim_v6 — V1 old (30% shrink, opp 0.5)
Over-side probability bins:

| bin | n | mean pred | actual hit | market nv |
|---|---|---|---|---|
| 0-40 | 601 | 0.329 | 0.473 | 0.490 |
| 40-50 | 801 | 0.455 | 0.478 | 0.496 |
| 50-55 | 397 | 0.525 | 0.501 | 0.499 |
| 55-60 | 300 | 0.575 | 0.500 | 0.505 |
| 60-65 | 184 | 0.622 | 0.527 | 0.504 |
| 65-70 | 78 | 0.674 | 0.474 | 0.509 |
| 70-80 | 48 | 0.733 | 0.479 | 0.507 |
| 80+ | 2 | 0.816 | 0.000 | 0.501 |

Model-favored side (prob of the side the model leans):

| bin | n | mean pred | actual hit | market nv (same side) |
|---|---|---|---|---|
| 50-55 | 843 | 0.525 | 0.510 | 0.500 |
| 55-60 | 655 | 0.573 | 0.515 | 0.506 |
| 60-65 | 442 | 0.622 | 0.527 | 0.508 |
| 65-70 | 269 | 0.672 | 0.498 | 0.509 |
| 70-80 | 175 | 0.737 | 0.514 | 0.510 |
| 80+ | 27 | 0.830 | 0.630 | 0.511 |

### sim_v6 — V2 no shrink, opp 0.5
Over-side probability bins:

| bin | n | mean pred | actual hit | market nv |
|---|---|---|---|---|
| 0-40 | 780 | 0.285 | 0.474 | 0.490 |
| 40-50 | 622 | 0.451 | 0.477 | 0.497 |
| 50-55 | 273 | 0.524 | 0.469 | 0.500 |
| 55-60 | 245 | 0.573 | 0.551 | 0.502 |
| 60-65 | 199 | 0.623 | 0.492 | 0.505 |
| 65-70 | 138 | 0.672 | 0.529 | 0.502 |
| 70-80 | 119 | 0.744 | 0.454 | 0.508 |
| 80+ | 35 | 0.857 | 0.514 | 0.509 |

Model-favored side (prob of the side the model leans):

| bin | n | mean pred | actual hit | market nv (same side) |
|---|---|---|---|---|
| 50-55 | 602 | 0.525 | 0.497 | 0.501 |
| 55-60 | 538 | 0.574 | 0.537 | 0.503 |
| 60-65 | 405 | 0.623 | 0.506 | 0.506 |
| 65-70 | 333 | 0.672 | 0.541 | 0.508 |
| 70-80 | 371 | 0.744 | 0.493 | 0.510 |
| 80+ | 162 | 0.872 | 0.525 | 0.510 |

### sim_v6 — V3 no shrink, opp 1.0
Over-side probability bins:

| bin | n | mean pred | actual hit | market nv |
|---|---|---|---|---|
| 0-40 | 839 | 0.276 | 0.480 | 0.491 |
| 40-50 | 577 | 0.450 | 0.489 | 0.498 |
| 50-55 | 241 | 0.523 | 0.469 | 0.499 |
| 55-60 | 245 | 0.573 | 0.494 | 0.500 |
| 60-65 | 189 | 0.624 | 0.481 | 0.507 |
| 65-70 | 146 | 0.673 | 0.548 | 0.504 |
| 70-80 | 132 | 0.744 | 0.492 | 0.506 |
| 80+ | 42 | 0.856 | 0.429 | 0.508 |

Model-favored side (prob of the side the model leans):

| bin | n | mean pred | actual hit | market nv (same side) |
|---|---|---|---|---|
| 50-55 | 531 | 0.524 | 0.488 | 0.500 |
| 55-60 | 532 | 0.574 | 0.508 | 0.502 |
| 60-65 | 416 | 0.624 | 0.495 | 0.506 |
| 65-70 | 318 | 0.674 | 0.550 | 0.508 |
| 70-80 | 413 | 0.746 | 0.504 | 0.509 |
| 80+ | 201 | 0.875 | 0.502 | 0.509 |

### sim_v6_fix — V1 old (30% shrink, opp 0.5)
Over-side probability bins:

| bin | n | mean pred | actual hit | market nv |
|---|---|---|---|---|
| 0-40 | 599 | 0.330 | 0.477 | 0.490 |
| 40-50 | 809 | 0.455 | 0.477 | 0.496 |
| 50-55 | 391 | 0.524 | 0.499 | 0.499 |
| 55-60 | 310 | 0.574 | 0.510 | 0.503 |
| 60-65 | 179 | 0.623 | 0.497 | 0.505 |
| 65-70 | 75 | 0.675 | 0.480 | 0.509 |
| 70-80 | 46 | 0.733 | 0.500 | 0.507 |
| 80+ | 2 | 0.817 | 0.000 | 0.501 |

Model-favored side (prob of the side the model leans):

| bin | n | mean pred | actual hit | market nv (same side) |
|---|---|---|---|---|
| 50-55 | 856 | 0.524 | 0.512 | 0.500 |
| 55-60 | 654 | 0.573 | 0.517 | 0.505 |
| 60-65 | 454 | 0.624 | 0.504 | 0.508 |
| 65-70 | 252 | 0.673 | 0.504 | 0.509 |
| 70-80 | 169 | 0.737 | 0.527 | 0.510 |
| 80+ | 26 | 0.831 | 0.615 | 0.511 |

### sim_v6_fix — V2 no shrink, opp 0.5
Over-side probability bins:

| bin | n | mean pred | actual hit | market nv |
|---|---|---|---|---|
| 0-40 | 792 | 0.287 | 0.477 | 0.490 |
| 40-50 | 616 | 0.453 | 0.477 | 0.498 |
| 50-55 | 277 | 0.524 | 0.477 | 0.499 |
| 55-60 | 246 | 0.573 | 0.508 | 0.501 |
| 60-65 | 198 | 0.623 | 0.545 | 0.504 |
| 65-70 | 135 | 0.673 | 0.489 | 0.509 |
| 70-80 | 112 | 0.746 | 0.473 | 0.506 |
| 80+ | 35 | 0.855 | 0.486 | 0.509 |

Model-favored side (prob of the side the model leans):

| bin | n | mean pred | actual hit | market nv (same side) |
|---|---|---|---|---|
| 50-55 | 611 | 0.525 | 0.507 | 0.500 |
| 55-60 | 528 | 0.573 | 0.509 | 0.502 |
| 60-65 | 415 | 0.623 | 0.540 | 0.506 |
| 65-70 | 333 | 0.674 | 0.505 | 0.510 |
| 70-80 | 364 | 0.744 | 0.495 | 0.508 |
| 80+ | 160 | 0.870 | 0.537 | 0.511 |

### sim_v6_fix — V3 no shrink, opp 1.0
Over-side probability bins:

| bin | n | mean pred | actual hit | market nv |
|---|---|---|---|---|
| 0-40 | 855 | 0.277 | 0.480 | 0.491 |
| 40-50 | 574 | 0.452 | 0.488 | 0.499 |
| 50-55 | 234 | 0.523 | 0.479 | 0.498 |
| 55-60 | 236 | 0.574 | 0.496 | 0.500 |
| 60-65 | 193 | 0.623 | 0.477 | 0.507 |
| 65-70 | 140 | 0.672 | 0.529 | 0.503 |
| 70-80 | 137 | 0.743 | 0.511 | 0.507 |
| 80+ | 42 | 0.858 | 0.429 | 0.509 |

Model-favored side (prob of the side the model leans):

| bin | n | mean pred | actual hit | market nv (same side) |
|---|---|---|---|---|
| 50-55 | 533 | 0.524 | 0.492 | 0.500 |
| 55-60 | 511 | 0.574 | 0.511 | 0.501 |
| 60-65 | 421 | 0.623 | 0.494 | 0.508 |
| 65-70 | 315 | 0.672 | 0.540 | 0.507 |
| 70-80 | 424 | 0.743 | 0.507 | 0.509 |
| 80+ | 207 | 0.874 | 0.512 | 0.509 |


=== FILE: backtests/rulebook_replay_wk6_8/REPORT.md ===
# Rulebook replay: Weeks 6–8 plus MNF CHI@SEA (TEST ONLY: no bets, nothing sent, nothing live)

## Headline
- **Strict reading: 0 legs go live and 0 of 369 slips get a door stamp.** No game has a replay `film` source. That is real missing data, so every run fails the gate at run level, and the door blocks every slip on GATE_PASS.
- **Leg level** (leg-named misses only; film is reported separately): 479 of 4,487 candidate legs pass the gate, and 463 more pass door.leg_rules.
  - Singles at $10: **241–222, 52.1%, −$569.78, ROI −12.3%**.
  - v1 was 293 passed, 48.5%, −$272. v2 passes more legs and hits more often, but loses more money. Reasons: low-rung alts are priced short (alts alone are −$423), and passyds overs went 5–17.
- **Slips, $10 each:**
  - Test A (3–4 legs): 245 slips, 20 won, **−$1,070.42** on $2,450 staked.
  - Test B (6–7 legs): 124 slips, 2 won, **−$428.71** on $1,240 staked.
  - Week 7 lost every slip in both tests.
  - Door, leg level: 245 PASS (all Test A). All 124 Test B slips are BLOCKED on SLIP_SIZE.
- **Odds API credits:** 1,510 used for this replay, below the 3,000 hard stop. The account balance went 9,429 → **5,959**, which is **41 under the 6,000 floor**. Another process on the same key was spending at the same time. I stopped pulling when that happened (BUDGET STOP), so some alt events are missing. There were no further pulls.

## Method (as-of dates)
- **Harness only. No tool files were edited.**
  - gate_replay.py patches `_rb.active` → True and sets SIMV6/FORECAST/COVPROF/NOV2/SNF/RICO4/FEEDWEEK `*_FROM` = 2000-01-01 (forced active).
  - It runs `run_gate.Gate(dir, now).run()` in-process with now = kickoff − 30m.
  - Misses are matched to legs with `re.escape(n)+r"(?=[: ]|$)"`. Run-level misses are reported separately.
- **Stats:** nflverse pbp, weeks < W. The week-W starting QB comes from the actual starter. MNF uses pbp through Sunday of Week 8, and the starter comes from the ESPN box.
- **Injuries:** inj26 weekly report plus ESPN game injuries/inactives (an ESPN Out is treated as inactive). Out/Doubtful defenders are dropped from coverage. `depleted_secondary` is built when 2+ CBs are out.
  - The ESPN file was fetched after the game, so inactives are stamped kickoff − 90m (REPLAY STAMP).
- **Weather:** Open-Meteo historical-forecast at kickoff hours. Forecast block = previous-runs day-1, stamped kickoff − 23h. Roof comes from pbp; MNF is Lumen Field, open air.
  - HOU@JAX and PIT@NO have no day-1 precip, so the kickoff value is used and labeled.
- **Coverage:** two parts.
  - Per-defender numbers are a **pbp-credit PROXY** (INT/PBU/tackler on the targeted play). Primary-defender rule: WR1→CB1, WR2→CB2, WR3+→CB3, TE→S1/LB1, RB→LB1.
  - Man/zone and MOF come from the Sharp table as of **2026-10-27**. That is **HINDSIGHT for Weeks 6–7**, stamped now − 5m (REPLAY STAMP).
- **Pressure inputs:**
  - blitz = FTN n_blitzers/n_pass_rushers
  - pressure = sack|qb_hit (PROXY)
  - checkdown = FTN CHK share
  - time_to_throw = NGS
  - targets_under_pressure = qb_hit target share (PROXY)
- **SCHEME_EDGE:** 4 keys {ok, source, detail}. The explanation is labeled "AUTO-GENERATED (harness, not analyst)".
- **Sims:** sim_v6, 3 models, n = 100k, fixed seed. Main rush lines were re-simmed with the soft-run-D ypc boost. `game_script_rb` uses `sim_v6.price_game_script` for the 7 triggered games.
- **Checklist rows:** all N/A. Analyst attestations can't be reconstructed, and no PASS was faked.
- **Team files:** door_out/wk{W}/teams, built as of the week.
- **TEST_SUITE:** `door.py test` passed 406 tests (code_hash ff7a42188e06e1b9). The result is copied per week.
- **LEDGER:** the real ledger check, run once and reused.
- **Door stamp:** `door.run_gate` was patched to return the in-process result, then `door.build(write=False)` was run in two modes: strict (ok = no misses at all) and leg level (ok = True, live = legs with no leg-named miss).
- **Alt no-vig is a PROXY:** the main-line margin is removed from the one-sided alt price.

## Slip method (fixed before results; slip_method.txt)
- **Pool:** gate leg-pass legs with no door BLOCK. One leg per player (best raw edge), sorted by raw edge.
- **M1 (cross-game greedy):** no two legs from the same game, and at most 1 depth receiver per slip.
- **M2 (sequential chunks):** same-game legs allowed. Real SGP pricing would pay less than the product of prices used here.
- **Sizes:** A = 3 and 4 legs; B = 6 and 7 legs.
- **Pricing:** product of decimal prices. Push/void legs drop out.

## Singles: passed vs blocked by rule
| set | legs | W–L | hit | P/L |
|---|---|---|---|---|
| all candidates | 4,487 | 2380–2107 | 53.0% | −$3,880.62 |
| gate leg-pass | 479 | 253–226 | 52.8% | −$533.67 |
| pool (gate + door) | 463 | 241–222 | 52.1% | −$569.78 |
| blocked | 4,024 | 2139–1885 | 53.2% | −$3,310.84 |

- **Door blocks among gate-pass legs:** RB_TRAIL 8, INJURY 8. SHORT_PRICE was flagged 63 times; it is a flag only, so those legs stay in the pool.
- **Top gate misses** (rule_matrix.csv has every leg × rule):
  - sim median does not clear the line: 3,951 (over) + 1,652 (under)
  - edge < +3: 2,643
  - a model p < .45: 1,522
  - §7 form: about 4,700 across its forms
  - N1 committee back: 785
  - DEPTH_RECEIVER: about 470
  - WEATHER: HOU@JAX, PIT@TB, ATL@TB, IND@JAX, NE@MIA
  - N2 no primary defender: 72
- **Legs blocked by a single rule only:**
  - §7 under form: 266
  - §7 too few current-QB games: 193
  - edge < +3: 164
  - N1: 90

## SCHEME_EDGE and depth, shown separately (pool)
| set | legs | W–L | hit | P/L |
|---|---|---|---|---|
| SCHEME_EDGE-flag legs (would have been cut without SE) | 54 | 33–21 | 61.1% | −$25.95 |
| non-SE | 409 | 208–201 | 50.9% | −$543.82 |
| depth receiver overs (low rung) | 12 | 10–2 | 83.3% | +$24.35 |
| alt low rung, all | 198 | 105–93 | 53.0% | −$422.70 |
| main lines | 265 | 136–129 | 51.3% | −$147.08 |

## Variants (sensitivity)
- **Weeks 6–7 with scheme_fit forced not OK** (removes the Sharp hindsight): leg-pass falls from 368 to 308. Pool singles: 296 legs, 52.0% hit, −$398.07.
- **Week 8 with Sharp coverage at its true date** (Oct 27, more than 48h stale): leg-pass falls from 102 to **17**. Pool singles: 15 legs, 73.3% hit, +$54.01. The sample is tiny.
  - Read: on a real Week 8 clock, almost no receiving or passing legs would have passed, because the coverage was stale.

## Per-market table (pool singles)
| market | n | W–L | hit | P/L |
|---|---|---|---|---|
| passyds over | 22 | 5–17 | 22.7% | −$131.15 |
| passyds under | 4 | 1–3 | 25.0% | −$21.15 |
| rec over | 82 | 47–35 | 57.3% | −$79.52 |
| rec under | 85 | 43–42 | 50.6% | −$100.24 |
| recyds over | 131 | 63–68 | 48.1% | −$323.72 |
| recyds under | 72 | 38–34 | 52.8% | +$0.14 |
| rushyds over | 41 | 24–17 | 58.5% | −$28.87 |
| rushyds under | 26 | 20–6 | 76.9% | +$114.73 |

**Slip killers** (leg losses inside slips): rec under 221, recyds over 158, recyds under 141, rec over 101, rushyds over 56, passyds over 40, rushyds under 35, passyds under 24.

**Spreads, totals, ML and period markets:** no model, not tested. Period markets were not pulled.

## A vs B by week (P/L, $10 per slip)
| week | A M1 | A M2 | B M1 | B M2 |
|---|---|---|---|---|
| 6 | 36 slips, 3 won, −$200.99 | 37, 6, +$24.85 | 18, 1, +$427.04 | 19, 1, +$14.25 |
| 7 | 47, 0, −$470 | 47, 0, −$470 | 24, 0, −$240 | 24, 0, −$240 |
| 8 | 38, 7, +$167.26 | 38, 4, −$101.54 | 19, 0, −$190 | 20, 0, −$200 |
| MNF | — (fewer than 3 cross-game legs) | 2, 0, −$20 | — | — |

- Test B's single big week (W6 M1, +$427) is one 7-leg hit, so it is noise.
- Test B can't be stamped by the door, because SLIP_SIZE is 3–4.

## Comparison with v1
- v1: 293 singles passed, 48.5% hit, −$272.
- v2 rulebook replay: 463 passed, 52.1% hit, −$569.78.
- v2 widens the pool (alts plus SCHEME_EDGE waivers), and the hit rate is better. Losses are larger for three reasons: short-priced alts, passyds overs, and recyds overs.
- No version shows a profitable single or slip strategy across Weeks 6–8.

## Limits
- **Film:** no replay film exists, so every run strictly fails (headline above).
- **Coverage:**
  - Per-defender coverage is a pbp-credit PROXY, not charted coverage.
  - Sharp man/zone and MOF is hindsight for Weeks 6–7, and stale on Week 8's true clock. nflverse participation 2026 is not available.
- **Prices:**
  - Alt no-vig is a proxy.
  - Some alt events are missing because of the budget stop.
  - M2 same-game parlays are priced as independent legs.
- **Data:**
  - Injury and weather stamps are replay stamps. The data was pulled after the fact, and the true as-of dates are in each manifest.
  - MNF is graded from the ESPN box (pbp has no MNF game). MNF uses pbp through Sunday of Week 8. One MNF CHI RB sim failed (division by zero) and was skipped.
- **Inputs:** pressure_rate and targets_under_pressure are proxies. Checklist rows are N/A. SCHEME_EDGE explanations are auto-generated, not analyst text.

## Credits
- Used: 1,510.
- Remaining: 5,959. That is under the 6,000 floor by 41, because another process was spending on the shared key at the same time. Pulls stopped.

## Files
- **Scripts:** build_universe.py, build_legs.py, fix_gs.py, gate_replay.py, grade_slips.py, weather_mnf.py
- **Runs:** runs/wk*/ (run_manifest.json, checklist.md, report.md, gate_output.txt); variants/*/
- **Data:** gate_results.csv, graded_legs.csv, slips.csv, rule_matrix.csv, analysis.txt, slip_method.txt, door_out/

=== FILE: backtests/current_rules_wk6_8/REPORT.md ===
# Weeks 6-8 (2026) replay through the current rulebook on real prices
Test only. Nothing went live and no bets were placed. Run on Nov 3, 2026, ET.

- **Prices:** Odds API historical, one snapshot 30 minutes before each kickoff. That's 41 games and 1,428 player lines on 4 markets (rec yds, receptions, rush yds, pass yds), US books. The price used is FanDuel when it has the line (70%), otherwise the first book with it. No-vig is the two-way devig averaged across books at the main line. About 1,770 credits used.
- **Models:** sim_v6 MC, Bias and GR at 100k runs each, leak-free (the Engine only sees games before week W). Raw with no calibration, because the calibration was fit on Weeks 4-7 and would leak. Opponent adjustment is at full strength, as in the current sim_v6.
- **Rules (thresholds read from rules/rulebook.py, depth rule from tools/depth_rule.evaluate):** NOSHRINK (+3, model p .45), FORM_3OF4, SCHEME_EDGE (flag/override), N1, RB_TRAIL, DEPTH_RECEIVER, WEATHER (wind), SHORT_PRICE flag, and mirror overs (both sides graded).
- **OFF / not replayable:**
  - TEAM_FILES is off (team files are not built yet).
  - N2: no historical verified-defender source.
  - COVERAGE_AGE, FORECAST and COVPROF: no historical snapshots.
  - INJURY: only players who played are graded.
  - N3: there are no half or quarter lines in this pull.
- **Proxies:**
  - SCHEME_EDGE = matchup (the opponent allows more than average to the position group) + script (spread/total) + form (last-4 average with the current QB on the bet side). There is no sourced scheme-fit check for past weeks, so the position-group matchup stands in for it.
  - Depth inputs: WR rank and TE rank by targets over the last 4 games, team target share, and the position-group yards per target allowed.
- **Not included:** MNF CHI@SEA (Nov 2) is not in the play-by-play feed yet.
- **Counting:** the best leg per player per week is counted (the §11 one-slip-per-player rule).

| bucket | legs | W-L | hit | $10 flat |
|---|---|---|---|---|
| PASSED (best leg per player) | 293 | 142-151 | 48.5% | $-272 |
|   Week 6 | 98 | 54-44 | 55.1% | $+36 |
|   Week 7 | 88 | 40-48 | 45.5% | $-141 |
|   Week 8 | 107 | 48-59 | 44.9% | $-167 |
|   recyds | 112 | 52-60 | 46.4% | $-136 |
|   rec | 101 | 48-53 | 47.5% | $-126 |
|   rushyds | 58 | 33-25 | 56.9% | $+41 |
|   passyds | 22 | 9-13 | 40.9% | $-51 |
|   overs | 102 | 43-59 | 42.2% | $-185 |
|   unders | 191 | 99-92 | 51.8% | $-87 |
|   SCHEME_EDGE overriding 3-of-4 | 54 | 20-34 | 37.0% | $-159 |
|   depth receivers (WR3/4, TE2) | 42 | 20-22 | 47.6% | $-57 |
|   -250 or shorter (flag) | 0 | | | |
|   alive only because the shrink is gone | 20 | 11-9 | 55.0% | $-4 |
| BLOCKED by a rule (had +3 edge) | 431 | 218-213 | 50.6% | $-184 |
|   FORM_3OF4 | 401 | 203-198 | 50.6% | $-178 |
|   N1 | 37 | 19-18 | 51.4% | $-11 |
|   RB_TRAIL | 10 | 5-5 | 50.0% | $-6 |
|   DEPTH_RECEIVER | 64 | 36-28 | 56.2% | $+71 |
|   WEATHER | 0 | | | |
| SCHEME_EDGE FLAGS (+0 to +3, for Ghost6 at real price) | 25 | 16-9 | 64.0% | $+37 |
| Positive edge under +3 (cut) | 149 | 72-77 | 48.3% | $-109 |
| No model edge (all sides) | 1327 | 653-674 | 49.2% | $-1,023 |
Model Brier (overs, all 1,323 lines) 0.267 vs market no-vig 0.247 (lower is better). Passed legs: model said 67.3% avg, no-vig 50.4%, actual 48.5%. By edge size: +3 to +6 went 17-15 (53%), +6 to +10 went 49% and +10 or more went 47.6% (-$232). The bigger the claimed edge, the worse it hit.

=== FILE: backtests/current_rules_wk6_8/summary.md ===
| bucket | legs | W-L | hit | $10 flat |
|---|---|---|---|---|
| PASSED (best leg per player) | 293 | 142-151 | 48.5% | $-272 |
|   Week 6 | 98 | 54-44 | 55.1% | $+36 |
|   Week 7 | 88 | 40-48 | 45.5% | $-141 |
|   Week 8 | 107 | 48-59 | 44.9% | $-167 |
|   recyds | 112 | 52-60 | 46.4% | $-136 |
|   rec | 101 | 48-53 | 47.5% | $-126 |
|   rushyds | 58 | 33-25 | 56.9% | $+41 |
|   passyds | 22 | 9-13 | 40.9% | $-51 |
|   overs | 102 | 43-59 | 42.2% | $-185 |
|   unders | 191 | 99-92 | 51.8% | $-87 |
|   SCHEME_EDGE overriding 3-of-4 | 54 | 20-34 | 37.0% | $-159 |
|   depth receivers (WR3/4, TE2) | 42 | 20-22 | 47.6% | $-57 |
|   -250 or shorter (flag) | 0 | | | |
|   alive only because the shrink is gone | 20 | 11-9 | 55.0% | $-4 |
| BLOCKED by a rule (had +3 edge) | 431 | 218-213 | 50.6% | $-184 |
|   FORM_3OF4 | 401 | 203-198 | 50.6% | $-178 |
|   N1 | 37 | 19-18 | 51.4% | $-11 |
|   RB_TRAIL | 10 | 5-5 | 50.0% | $-6 |
|   DEPTH_RECEIVER | 64 | 36-28 | 56.2% | $+71 |
|   WEATHER | 0 | | | |
| SCHEME_EDGE FLAGS (+0 to +3, for Ghost6 at real price) | 25 | 16-9 | 64.0% | $+37 |
| Positive edge under +3 (cut) | 149 | 72-77 | 48.3% | $-109 |
| No model edge (all sides) | 1327 | 653-674 | 49.2% | $-1,023 |
=== FILE: backtests/rico_method_wk8/REPORT.md ===
# Rico-method backtest, Week 8 2026 (TNF CAR@GB, Sunday 11 + SNF, MNF CHI@SEA). TEST ONLY: no bets.

## Integrity notes (read first)
- Reconstructed picks were locked in commit 3206cb8 (Nov 3 06:08 ET) and the slip method in 47223ba, both before grading.
- **Leak disclosure:** after the picks were locked but before grading, I opened week8/slips/slips_2026-11-01.md(.pre_snf.bak) to find the live legs. That file has graded Week 8 results appended to it. The picks were already committed, so they weren't affected, but I had seen some results before the replacement and slip steps ran. Both of those steps are mechanical (rules in slip_method.md) to limit how much that knowledge could matter. The analyst has also seen Week 8 postmortems in earlier sessions, so this is **not a blind test**.
- PFF: coverage and grades are locked on this account's tier, so it isn't used. Its season-to-date grades would also include Week 8 and later games.
- The reconstructed "read" is a **mechanical proxy** for the phase script, built from pbp and FTN data for weeks 1-7 plus pre-kick lines. It wasn't a hand-written per-game script. It uses: the player's last 4 games with the current QB; what the opponent allowed by position and market compared with the league (pbp weeks <8); opponent blitz rate (FTN weeks <8); and the nflverse closing spread and total, which are recorded but carry no weight. Not used: PFR Wayback, man/zone coverage and defender matchups (no point-in-time copy was pulled in this pass). The "reason" for each pick is the feature line in picks_locked.md.

## LIVE_READ picks (our actual pre-kick gated PASS legs, from manifest/build timestamps)
| Leg | Source (ET) | Actual | Result |
|---|---|---|---|
| Tre Tucker rec o3.5 -120 | runs/2026-11-01_LV@NYJ/run_manifest.json 11:41 | 0 | MISS |
| Puka Nacua rec o7.5 -138 | runs/2026-11-01_BONUS_SLIP build 11:53 | 11 | HIT |
| Stefon Diggs rec o3.5 (alt) -166 | BONUS_SLIP 11:53 | 3 | MISS |
| Jahmyr Gibbs rush o79.5 (alt) -162 | BONUS_SLIP 11:53 | 153 | HIT |
| Xavier Worthy rec o2.5 (alt) -225 | BONUS_SLIP_4PM build 11:58 | 3 | HIT |
| Matthew Stafford completions o22.5 -127 | DFS_SLIPS report 11:41 | 17 | MISS |
| Jaxon Smith-Njigba recyds o89.5 -166 | runs/2026-11-02_SEA_CHI_ghost6 05:08 Nov 2 (Ghost6 run) | 118 (ESPN box) | HIT |
Live total: 4/7 (57%), $10 flat **-$6.11**. Prices are the manifests' own FD prices, and alt prices are as recorded. The Rico-placed DFS/FD tickets are listed in the slips file, but they're Rico's picks, not our gated read, so they aren't graded here. Sources used live, from the manifests' sources blocks: nflverse pbp and FTN charting, the PFR advanced-defense cache (Rico exception), the PFF props cross-check, and FD lines.

## RECONSTRUCTED picks: 28 locked, then hard stops
Hard stops (hardstop_log.md). Weather (Open-Meteo, from the other worker's file) cut 5 receiving overs: Dotson (ATL@TB, 80% precip, 30.6 mph gust), Keenan Allen and Jakobi Meyers (IND@JAX, 20.6 mph gust), and Dulcich and Henry (NE@MIA, 65% precip). Their replacements were Ted Hurst rec u2.5, J. Taylor rush o48.5, Parker Washington rec u4.5, Kyle Williams recyds u23.5 and Ollie Gordon rush o58.5. Injuries: Kincaid and Ridley were Questionable, played, and were kept. Tez Johnson (ATL) has no Week 8 snaps, so his leg is VOID. Note that the weather cut removed Allen (actual 67, would have hit) and Meyers (24, would have missed).

Graded singles (27 non-void): **13/27 = 48.1%, -$29.52**. The 22 original picks went 45.5% (-$35.94). The 5 replacements went 3/5 (+$6.42).
By market: rec under 4/9 (-$18.36); rec over 0/1 (-$10); recyds over 4/8 (-$4.76); recyds under 3/5 (+$6.47); rushyds over 2/4 (-$2.89). Receptions unders killed the most slips.
Best: Tee Higgins recyds o72.5 (155), Jeanty recyds o27.5 (64), Mayer recyds o25.5 (53), Hubbard rush o67.5 (81). Worst: Kincaid u43.5 (86), Jeudy rec o2.5 (0 catches), Warren recyds o22.5 (0), J. Taylor rush o48.5 (23), and Kyle Williams u23.5 (43).

## Slips ($10 each, decimal product of pre-kick prices, approximation)
| Slip | Legs | Hits | Price | Result |
|---|---|---|---|---|
| S1 (8) | 8 | 3 | 145x | -$10 |
| S2 (8) | 8 | 3 | 184x | -$10 |
| S3 (7, 1 void) | 7 | 5 | 65x | -$10 |
| TNF 2-leg | 2 | 1 | 3.6x | -$10 |
| MNF 2-leg | 2 | 1 | 2.9x | -$10 |
| 7-leg variants S1/S2/S3 | 7 each | 3/3/5 | — | all -$10 |
All slips lost (0/8), **-$80**. No slip came within one leg of cashing; the best was S3 at 5/7. Full detail is in slips_graded.csv.

## Comparison with rules-only (FIRST version, backtests/current_rules_wk6_8 week 8; the rulebook_replay redo hadn't finished)
- Rules-only: 107 passed legs, 44.9% hit, -$167.19 at $10 flat, with no slip test in that version.
- Rico-method reconstructed: 27 legs, 48.1%, -$29.52. LIVE_READ: 7 legs, 57%, -$6.11. Combined: 34 legs, 50.0%, -$35.63.
- Overlap: 10 reconstructed legs are the same player, market and side as rules-only legs (A. Jones, McConkey, Q. Johnston, Sutton, J. Jefferson, Kincaid, K. Williams, Diggs recyds, Ted Hurst, P. Washington). Five more use the same player in a different market (Higgins, Ridley, Jeanty, Warren, J. Taylor). Of the live legs, Tucker and Puka were also in rules-only.
- Caught by Rico-method but not rules-only (same market): Higgins recyds o72.5 HIT and Mayer o25.5 HIT, plus Jeanty recyds o HIT (rules-only had his rush under). Missed by Rico-method but caught by rules-only: Gibbs rush o (live had it), Warren rush o 143, Bowers o70.5.
- Takeaway: the per-leg hit rate is slightly better and losses are much smaller because there are far fewer legs. Even so, about 48-50% at mostly -113 to -180 prices still loses, and 7-8 leg slips at that hit rate are expected to lose (0/8).

## Limits
Not blind (see the leak disclosure). The read is a mechanical proxy with no man/zone or defender data and no PFR Wayback. No spreads, totals or period lines were tested. Alt lines were only tested for the live legs, at their recorded prices. Odds API credits used: **0** (everything came from the existing pulls). MNF actuals come from the ESPN box. Prices are FD-first single-book prices, and parlay pricing is an approximation.

=== FILE: backtests/yardage_markets_wk3_8/v5/report.md ===
# v5: brainstorm-first Grok reads, Weeks 3–8 (lock c71af73, graded after)

**Structure change:** every RECONSTRUCTED read uses the betting-game-brainstorm 12-step format: GAME, SCRIPT (base case + 2 flips), INJURY FALLOUT, MATCHUP (shell, pressure, where the defense bleeds, primary target overlap), FORM, EDGE PLAYERS (≤2, with must be true, kills it and confidence), DATA CHECK (flag, not cut), MARKET+RUNG+price, PRE-MORTEM, SLIP STORY, and the step6/step12_limited flags. The earlier free-form reads were superseded and moved to superseded_oldformat/. They weren't used.

## Steps per leg (locked_picks.csv `steps` column)
- PRO_EDGE: **approximated.** edge_scan.py only works against the live API, so proedge.py reimplements it offline. It covers implied team totals, best saved price vs the anchor no-vig (betonlineag, then consensus; there is no Pinnacle in the packs), and lagging props where snapshots exist. The sleeper check is N/A because the packs have no structured injury data. It ran AFTER the reads as a gate or tag and was NOT fed into the Grok prompt, because of time and cost after the late steer.
- BRAINSTORM: **full** for all 88 games (grok-4.7, pack-only, validated).
- PHASE_SCRIPT: **approximated.** The main line and the latest saved price only. No 3-sim gate.

## Leg results (hit rate counts all settled legs; ROI uses $10 flat on priced legs only)
| Set | Train wk3–6 | Holdout wk7–8 | Holdout ROI (priced) |
|---|---|---|---|
| PRIMARY (saved where available, else Grok) | 49–63 (43.8%), −13.8% | 31–20 (60.8%) | 25–15, +17.2% |
| RECONSTRUCTED (Grok) | 43–58 (42.6%) | 30–18 (62.5%) | +20.2% |
| SAVED_READ | 6–5 (54.5%) | 1–2 | n is tiny |
| GROK_ON_SAVED_GAME (comparison) | 3–9 | 1–3 | −52.9% |
| ZONE_MOF | 44–58 (43.1%) | 29–18 (61.7%) | +19.8% |
| PRO_EDGE pass | 4–9 | 15–10 (60.0%) | +25.2% |
| Baseline: every main rush-yds under | 161–128, +4.3% | 70–62, −0.6% | |

Primary by week (W–L): wk3 11–21, wk4 12–17, wk5 15–10, wk6 11–15, wk7 16–10, wk8 15–10.
Primary holdout by market: recyds 15–12, rushyds 11–7, rushrecyds 5–1. Train by market: recyds 26–35, rushyds 16–20, rushrecyds 7–8.

## Slips (3–4 legs, ≤5 per week, $10 each, prices are independent products, so estimates)
PRIMARY: wk3 0/5, wk4 0/5, wk5 1/5, wk6 0/5, wk7 1/5, wk8 2/4. 4 of 29 won, +$145.38 (all of it from wk5, wk7 and wk8).
ZONE_MOF: 4 of 27 won, +$223.82. PRO_EDGE: 1 of 7 won, +$52.67.

## Targets (PRIMARY holdout)
- 100+ holdout legs: **FAIL** (51).
- 57%+: **PASS** (60.8%).
- +3% ROI: **PASS** (+17.2% on priced legs).
- No losing week: **PASS in the holdout** (wk7 and wk8 both up), but **FAIL across the full run** (wk3, wk4 and wk6 lost, and train is −13.8%).
- The holdout beating train by this much on a small n looks like variance, not a proven edge.

## Rico placed legs (outcomes.csv): see results.md
Yardage legs: rec yds 32/37 (86%), receiving yds 18/20, rush+rec 18/24 (75%), receptions 33/46, **rush yds 9/25 (36%)**. Ticket cash P&L: wk5 +197.72, wk6 +18.53, wk7 −193.87, wk8 −104.50.

Full tables are in results.md. Grok usage is in GAPS.md.

=== FILE: backtests/v5_leak_audit/direct_answer.md ===
# Direct question to grok-4.7

## Question

Earlier you (grok-4.7) were given pre-kickoff stat packs for 2026 NFL Weeks 7 and 8 games and asked to pick player yardage props. These were your picks:
2026 Week 7 CIN@BAL: chasebrown recyds over 20.5
2026 Week 7 CIN@BAL: zayflowers recyds over 64.5
2026 Week 7 CLE@TEN: jerryjeudy recyds over 21.5
2026 Week 7 CLE@TEN: quinshonjudkins rushyds under 45.5
2026 Week 7 DAL@PHI: javontewilliams rushrecyds under 81.5
2026 Week 7 DAL@PHI: ryanflournoy recyds over 34.5
2026 Week 7 DEN@ARI: jaylenwaddle recyds under 51.5
2026 Week 7 DEN@ARI: jkdobbins rushyds over 48.5
2026 Week 7 IND@MIN: danieljones rushyds over 6.5
2026 Week 7 IND@MIN: jonathantaylor rushrecyds over 92.5
2026 Week 7 KC@SEA: emanuelwilson rushyds over 51.5
2026 Week 7 LA@LV: brockbowers recyds over 72.5
2026 Week 7 LA@LV: pukanacua recyds over 84.5
2026 Week 7 MIA@NYJ: gregdulcich recyds over 21.5
2026 Week 7 MIA@NYJ: malikwillis rushyds over 30.5
2026 Week 7 NE@CHI: eliraridon recyds over 15.5
2026 Week 7 NE@CHI: hunterhenry recyds over 35.0
2026 Week 7 NYG@HOU: isaiahlikely recyds over 50.0
2026 Week 7 NYG@HOU: maliknabers recyds over 69.0
2026 Week 7 PIT@NO: alvinkamara rushrecyds over 32.5
2026 Week 7 PIT@NO: jaylenwarren rushrecyds over 96.5
2026 Week 7 TB@CAR: buckyirving rushyds over 66.5
2026 Week 7 TB@CAR: tetairoamcmillan recyds over 70.5
2026 Week 8 ARI@DAL: georgepickens recyds over 66.0
2026 Week 8 ARI@DAL: treymcbride recyds over 73.5
2026 Week 8 ATL@TB: buckyirving rushyds over 70.5
2026 Week 8 ATL@TB: kylepitts recyds over 34.5
2026 Week 8 BAL@BUF: khalilshakir recyds over 41.5
2026 Week 8 CAR@GB: chubahubbard rushyds over 67.5
2026 Week 8 CAR@GB: marshawnlloyd rushyds over 16.5
2026 Week 8 CLE@PIT: germiebernard recyds over 44.0
2026 Week 8 CLE@PIT: jaylenwarren rushyds over 64.5
2026 Week 8 IND@JAX: bhayshultuten rushyds over 68.0
2026 Week 8 IND@JAX: keenanallen recyds over 35.5
2026 Week 8 KC@DEN: jaylenwaddle recyds under 39.5
2026 Week 8 KC@DEN: kennethwalkeriii rushyds over 86.5
2026 Week 8 LAC@LA: blakecorum rushrecyds over 58.5
2026 Week 8 LAC@LA: justinherbert rushyds over 24.5
2026 Week 8 LV@NYJ: ashtonjeanty rushyds under 50.5
2026 Week 8 LV@NYJ: braelonallen rushyds over 80.5
2026 Week 8 MIN@DET: jahmyrgibbs rushrecyds over 123.5
2026 Week 8 MIN@DET: tjhockenson recyds over 42.5
2026 Week 8 NE@MIA: gregdulcich recyds over 28.5
2026 Week 8 NE@MIA: olliegordonii rushyds over 61.5
2026 Week 8 PHI@WAS: dallasgoedert recyds over 45.5
2026 Week 8 PHI@WAS: elijahmitchell rushyds under 28.5
2026 Week 8 TEN@CIN: samajeperine rushyds over 23.5
2026 Week 8 TEN@CIN: teehiggins recyds over 72.5

Please answer honestly and plainly: (1) When making those picks, did you know the actual outcomes of any of these games or player stat lines? (2) Do you know them now, from your training data? If so, list which ones. (3) What is your training knowledge cutoff? Do not guess outcomes.

## Answer (verbatim)

No. I did not know the actual outcomes of those 2026 Week 7 or Week 8 games or player stat lines when those picks were made, and I do not know them now from training data. I will not list any results and I will not guess.

My training data does not include completed 2026 NFL Weeks 7–8 box scores or player yardage lines for those matchups. I also don’t have that earlier pick session in this conversation, so I can’t inspect a prior run—only say that those outcomes were not available as known results.

=== FILE: postmortems/2026-11-01_1pm.md ===
# Week 8 Sunday 1 PM window: final postmortem (Nov 1, 2026)
_Play-log routine run, 4:50 PM ET. All 8 early games confirmed STATUS_FINAL on ESPN (TEN@CIN and ARI@DAL went to OT, finalized 4:42 PM ET). Public sources only (ESPN summary API box/play-by-play/pickcenter). nflverse Week 8 pbp, FTN charting and NGS are not published yet, so blitz/pressure rates, time to throw, shells and per-defender coverage are NOT available; defender = tackler named in play text (proxy). Re-grade with charting at the Mon/Tue runs._

Detailed write-ups (already built today, not duplicated here):
- Full narrative, per-game tables, who disappeared, tickets: `postmortems/WEEK8_SUNDAY_1PM_2026-11-01.md` (written while 3 games were still live; finals below supersede it)
- Final grades of every runs-folder and slip leg: `playlogs/2026_wk8/FINALIZED_1PM.md`
- Defense dissection and Week 9 leads: `postmortems/WEEK8_DEFENSE_DISSECTION_2026-11-01.md`
- Missed edges: `postmortems/WEEK8_SUNDAY_MISSED_EDGES_2026-11-01.md`; RB misses: `postmortems/RB_MISSES_2026-11-01.md`
- Play logs: `playlogs/2026_wk8/<AWAY>_<HOME>.csv` (new this run, one row per pass/rush play from the ESPN drives) plus `_plays.md`, `_box.json/.md`, `_script.md`
- Explosives tally: `playlogs/explosives_allowed.md`

## Finals
ATL 0 @ TB 16 (rain) · CLE 6 @ PIT 27 · IND 7 @ JAX 42 · LV 38 @ NYJ 33 · MIN 15 @ DET 19 · BAL 10 @ BUF 36 · TEN 36 @ CIN 43 (OT) · ARI 33 @ DAL 30 (OT)

## Record of our reads
- Vetted/passed legs: 0-1 (Tre Tucker rec O3.5, 0 catches on 1 target).
- Cut legs: 63 of 124 decided were good cuts; 61 would have hit (6 void/push). Costly cuts: Tuten rush O59.5/R+R O83.5 (104/159), Gibbs rush O87.5/R+R O121.5 (153/168), Pollard rush O65.5 (117), Allgeier rush O13.5 (147), Higgins O69.5/O4.5 (10-155), Burrow O249.5 (462), Cousins O232.5 (247), Bowers yds O68.5 (92), Penix U229.5 (125), London/Pitts unders.
- User's placed slip legs (1 PM): 18-13, 1 push (St. Brown 7 rec on PP25).
- Tickets: PP $40 and PP $20 still alive (all 1 PM legs hit; 4 PM legs pending). Lost: UD $20, PP $25, PP $65, PP bonus Flex, FD 7-leg, FD 8-leg, FD Ticket 2, FD $51.50 SGP.

## Biggest misses and the input that should have caught each
1. RB rushing overs in run scripts (Irving 170, Gainwell 140, Tuten 104, Gibbs 153, Allen 147, Allgeier 147, Pollard 117). Phase 14 single-median veto, no injury promotion (Allen), blanket underdog block, no weather RB branch. Fixes A/D/E/F and the game-script RB rule are approved; Bayes-veto-to-consensus (C) is still a proposal.
2. ATL@TB weather (76% precip at kickoff): 7 placed ATL/TB receiving overs died. The new 50%/20 mph Phase 11 rule would have cut all of them.
3. Lamar hurt on his first throw: Flowers 0 catches killed 6 placed legs. Phase 13 exposure / QB-health input (returning-QB fragility, backup-QB floor).
4. Exposure concentration: Flowers 6 legs, London 3, Bijan 2. Slip-building §11 exposure input.
5. Shootouts missed (LV@NYJ 71 pts, TEN@CIN 79 in OT, ARI@DAL 63 in OT). Phase 1 total/script input; WR3 deep threats (A. Mitchell 7-142) not in the candidate list.
6. Team pass volume as favorites: DET threw 25 times (St. Brown 46 yds, LaPorta, Gibbs rec, Goff FS), DAL 29 (Lamb 7.5). Phase 1 pass-attempt projection for run-leaning favorites.

## Defenses giving up big plays (rush 15+ / rec 20+)
LV 9, CIN 7, CLE 7, DAL 7, IND 6, BAL 5, TEN 5. Defenders most charged (tackler-after-catch proxy, not coverage): J. Battle CIN S (8-104), J. Brisker CLE S (6-103), T. Stukes NYJ S (102) and D. Belton NYJ S (96), C. Schwesinger CLE LB (89), M. Humphrey BAL CB (79). By type: CLE and IND bled to TEs, IND and DAL to RBs (DAL 165 yds on 18 RB carries), LV's outside CBs to WRs (Mitchell 20/22/47).

## Proposed fixes (proposals only; nothing changed without the user's OK)
- Gate regression fixtures from today: ATL@TB must cut London/Godwin/Bijan rec overs; IND@JAX (71% precip) must cut P. Washington 40+.
- Returning-QB fragility flag: QB back from 2+ missed games caps WR1 exposure at 2 tickets and adds a backup-QB scenario to the sims.
- Per-game exposure cap: max 3 legs across tickets from one weather-flagged or single-QB-dependent game.
- Candidate list: add WR3s with 15%+ deep-target share vs CBs allowing 12+ YPT, and every team's RB1 and RB2.
- Phase 1: project team pass attempts; haircut WR/TE/RB-receiving overs when a favorite projects under ~30 attempts.
- Role-share check before passing a WR leg (Tucker): current-week route/snap share, not season target share.
- Fix C (single-median veto becomes consensus) and the RB-receiving haircut in run scripts.
- Re-grade pressure/blitz/coverage once nflverse/FTN/NGS publish.

=== FILE: postmortems/2026-11-01_4pm.md ===
# Week 8 Sunday 4 PM window: final postmortem (Nov 1, 2026)
_Play-log routine run, 8:25 PM ET. All 3 late games confirmed STATUS_FINAL on ESPN (summary API events 401873032/033/034, re-pulled 8:24 PM ET, saved in postmortems/). Public sources only. nflverse Week 8 pbp, FTN charting and NGS are not published yet, so blitz/pressure rates, time to throw, shells and per-defender coverage are NOT available; defender = tackler named in play text (proxy) or pregame cheat-sheet matchup (inferred). Re-grade with charting at the Mon/Tue runs. SNF PHI@WSH is not final; it is picked up at the Mon 8 AM run._

Detailed files (built at 7:38-7:55 PM ET, not duplicated here):
- Box / plays / script per game: `playlogs/2026_wk8/{KC_DEN,LAC_LAR,NE_MIA}_box.md|_plays.md|_script.md`
- Play logs (new this run, one row per pass/rush, ESPN drives): `playlogs/2026_wk8/{LAC_LAR,KC_DEN,NE_MIA}.csv`
- Every leg graded: `playlogs/2026_wk8/FINALIZED_SUNDAY.md`; edges and signal scores: `postmortems/WEEK8_SUNDAY_MISSED_EDGES_2026-11-01.md` (4 PM section)
- Explosives tally: `playlogs/explosives_allowed.md` (4 PM table appended 7:55 PM ET)

## Finals
LAC 9 @ LAR 24 (LAR -6.5, 45.5, under) · NE 24 @ MIA 19 (NE -7, 41.5, over at 43; NE did not cover) · KC 24 @ DEN 28 (DEN -1.5, 41.5, over at 52; DEN came back from 24-13 down in Q4)
Weather: NE@MIA was flagged pregame (53-69% thunderstorms, 20-24 mph gusts); actual 0.0 mm rain, gusts to ~20 mph. KC@DEN dry, gusts to 16. LAR dome.

## Record of our reads
- Vetted live legs at kickoff: none. Worthy rec yds O29.5 was cut at 08:46 (actual 13, good cut). Puka rec O7.5 passed vetting this morning but was cut at the 15:40 recheck for P4 UNVERIFIED (backup RCB Waxter, no PFR sample): he caught 11 of 12 targets, a costly cut.
- Bonus-slip candidate Worthy rec O2.5 (alt): 3 catches, would have hit (slip was short of the 3-leg minimum).
- Cut legs: 35 of 51 good cuts; 16 would have hit (Puka O7.5, Dulcich O29.5/O3.5, and TE/RB unders: Henry, Raridon, Higbee, Engram, Kyren, Gordon R+R, Coleman, Douglas rec U3.5).
- Game-run cuts that were right: Stafford O248.5 (157), Walker rush O85.5 (69) and R+R O107.5 (84), Worthy O29.5/O3.5, Hampton overs, Maye O239.5 (199).
- Game-run leans that were wrong: Mahomes U220.5 (321, 3 TD), Herbert U205.5 (257), Willis U185.5 (211), McConkey/Gadsden/Johnston unders, Corum U46.5 (73), Stevenson U58.5 (82), Douglas yds U40.5 (76).
- User's placed 4 PM slip legs: 8-6. Hits: Puka 69.5 (80) x2, Puka 60+ (FD8), Walker 80+ rush+rec (84) on FD8 and the single, Mahomes O0.5, Kyren TD, Kyren/Corum TD. Misses: Stafford completions O22.5 x2 (17), Walker rush O97.5 (69), Walker rush O69.5 (69, by half a yard), Walker anytime TD, Walker+Kyren TD combo.
- Tickets: PP $40 and PP $20 LOST on the late legs (both were alive after 1 PM). Walker 80+ rush+rec single WON (84). All other Sunday tickets were already lost at 1 PM. Nothing rides on SNF.

## Biggest misses and the input that should have caught each
1. Stafford completions O22.5 (on 2 tickets, killed both live Power Plays). LAR led 24-9 and ran 27 times; Stafford threw only 25 passes. Phase 1 team pass-attempt projection: a -6.5 home favorite vs a turnover-prone QB projects a run-heavy second half. Same miss as DET/DAL at 1 PM.
2. Walker rush yards (97.5 demon, 69.5). Volume read was right (21 of 24 KC carries, 88%), efficiency was wrong (3.3 YPC vs DEN's front) and KC threw 41 times while leading. Phase 3 run-defense profile / YPC input: the demon line needed 4.6+ YPC against a front that doesn't allow it. Exposure: Walker was on 6+ legs.
3. Walker TD legs. All 3 KC TDs came through the air; Walker had no carry inside the 5. Phase 7 red-zone role / TD share input (KC goal-line usage vs. pass-heavy red zone with Mahomes).
4. Puka rec O7.5 cut at 15:40 for P4 UNVERIFIED on a backup CB. Backup-CB proposal sample is now 2/2 (M. Wilson 111, Puka 11 rec). Phase 4 defender-coverage input.
5. Emmett Johnson 5-128 (73 and 38 yd catches) was never in the candidate pool; both defenses bled to RB receivers (KC D and DEN D RB-receiving residuals about +7.5 and +8.6). Candidate-list input (RB2 receiving roles in passing-down packages).
6. QB unders all lost (Mahomes, Herbert, Willis): trailing QBs threw late. Phase 1 game-script / negative-script input for underdog QB unders.

## Defenses giving up big plays (4 PM; rush 10+/15+, pass 20+; defender = inferred pregame matchup or tackler proxy)
- DEN D: 5 flagged (all to KC RB/TE): Emmett Johnson 73 rec TD, 38 rec, 15 rush; Kelce 32. T. Rapp (S) tackler on two runs.
- KC D: 4 flagged: Sutton 23 and Waddle 35 (inferred vs Mansoor Delane / Nohl Williams), Trautman 22, Jonah Coleman 51 (RB screen). C. Conner (S) tackler on 4 explosives.
- LAR D: 4 flagged, all LAC passes: McConkey 30 and 54, Q. Johnston 21, Kolar 20 (TE). Tacklers Q. Lake, K. Curl, K. Kinchens (S).
- MIA D: 4 flagged: Douglas 26 and 48 TD (inferred vs Chris A. Johnson), Henry 20 (TE), Kiner 20 rush; K. Williams 43 TD.
- NE D: 3 flagged: M. Washington 23 (inferred vs Marcus Jones), Gordon 15 and 16 rush (C. Woodson, K. Byard); K. Coleman 35 TD late.
- LAC D: Atwell 40, Corum 23 rush TD.
By type: DEN and KC to RBs as receivers; LAR's safeties to WRs deep; MIA's slot/outside CB to Douglas.

## Proposed fixes (proposals only; nothing changed without the user's OK)
- Phase 1 pass-volume cap (repeat of the 1 PM proposal, now 3 games of evidence: DET, DAL, LAR): when a team is favored by 6+ and projects under ~30 attempts, haircut its QB completions/yards and WR overs; flag any QB-completions leg on a favorite.
- RB efficiency floor for demon/high rush lines: require the sims' YPC input to clear the line at the defense's adjusted YPC allowed; a carry-share pass alone isn't enough (Walker 88% share, 3.3 YPC).
- RB TD legs: add a red-zone carry share / inside-5 usage check, and a TD-leg haircut when the QB is a top red-zone passer.
- Backup-CB P4 rule (proposal #4 from the missed-edges file): treat UNVERIFIED-on-backup-CB as a soft-matchup flag, not a cut, for primary WRs. Sample 2/2; keep gathering.
- Candidate list: add RB2s with a passing-down role (Emmett Johnson) for receiving overs vs defenses with high RB-receiving residuals.
- Underdog QB unders: block when the dog's script projects trailing (Mahomes, Herbert, Willis all went over).
- Weather flag check: NE@MIA was flagged on a 53-69% forecast but stayed dry; log forecast-vs-actual so the 50% threshold can be calibrated (no change proposed yet).

=== FILE: postmortems/2026-11-03_MNF_CHI_SEA.md ===
# MNF postmortem: CHI 34, SEA 17 (Mon Nov 2 2026; nflverse 2026_08_CHI_SEA, folder playlogs/2026_wk9)
Blitz, Nov 3 2026, 8 AM ET routine. Public sources only: nflverse pbp and snap counts, ESPN box/play-by-play, Sharp coverage table. No bets, no messages.

## 1. Play log
- `playlogs/2026_wk9/CHI_SEA_enriched.csv` has 182 rows. All 135 scrimmage plays carry down, distance, score and EPA from nflverse, and 108 have a defender tag. Tags are tackler/PBU, **not coverage**; no public per-play coverage chart exists for this game.
- `CHI_SEA_explosives.csv` lists 14 explosives (pass 20+, rush 10+, 15+). The tally is in `playlogs/explosives_allowed.md`.
  - **SEA D allowed 7:** Odunze 4, Burden 1, Raymond 39-yd end-around, TE 1. CB tags: Pritchett 2 (13 snaps), Witherspoon 1, Jobe 1. Safety tags: J. Love 2. Four of the five WR explosives came **over the middle**.
  - **CHI D allowed 7:** JSN 4, Barner 1, Charbonnet 1, QB 1. Tags: Stevenson 2, Lewis 1, Thieneman 1, Bush 2. The JSN 43-yd TD had no tackler.
- Builder script: `playlogs/tools/enrich_chi_sea_mnf.py`.

## 2. SEA run calls: running was a losing call
- **Overall:** designed runs went 17 for 61 yds (3.59 YPC), -0.173 EPA/run, 17.6% success rate. Dropbacks: 40 at -0.158 EPA, 37.5% success rate.
- **Down 9+:** runs -0.072 EPA, 22% SR (9 runs, -0.65 EPA total, -0.082 WPA). Passes +0.033 EPA, 44% SR (+0.83 EPA, +0.099 WPA).
- **By situation:** first-down runs -0.255 EPA vs passes +0.101. Q3 run rate was 55%.
- **Costly drives:**
  - The late-Q3 4-run drive ended with an OPI and then a blocked FG.
  - The Q4 7:13/6:33 runs led into the Lynch INT (-5.36 EPA).
- **Context, Weeks 1-7:** CHI's run D was league-average (4.03 YPC, -0.097 EPA). SEA's dropbacks were +0.098 EPA vs runs -0.225.
- **Verdict:** SEA should have thrown while down 9+.

## 2b. SEA run/pass by quarter (from pbp, playlogs/2026_wk9/CHI_SEA.csv)
Pass = dropbacks (completions, incompletions, sacks, pass TDs, INT); run = designed rushes. Penalty/no-play rows excluded.

| | Pass | Run |
|---|---|---|
| Q1 | 6 | 4 |
| Q2 | 10 | 4 |
| Q3 | 5 | 6 |
| Q4 | 16 | 5 |
| Trailing by 9+ (pre-snap score) | 24 | 10 |
| **Total** | **37** | **19** |

Matches Ghost6's counts and ESPN totals. (If the score *after* each play is used instead of pre-snap, trailing-9+ is 22/10.) SEA still ran 29% of the time while down 9+.

## 3. Read grades
### r3 gate (runs/2026-11-02_CHI@SEA_r3): 23 legs, all cut
The model's direction was right on 11 and wrong on 12. Of the 23 cuts, 15 were correct and 8 would have hit.

**Cuts that would have hit:**
| Leg | Actual | Cut by / what should have caught it |
|---|---|---|
| Caleb O224.5 | 247 | Passing yards are now banned anyway |
| Swift R+R U86.5 | 79 | Under +3 |
| Roschon O10.5 | 17 | — |
| JSN O89.5, O99.5, O109.5 | 118 | §14 cushion and model-suspect. O89.5 was also barred as a nested rung of the open 70+ ticket |
| Barner U29.5 | 23 | — |
| Barner rec U3.5 | 2 | — |

**Misses in the model direction (the cuts were right, the model was wrong):**
- Burden, Odunze and Loveland unders, both yards and receptions. Actuals: Loveland 7-65 (9 tgts), Odunze 4-87 (6 tgts), Burden 7-56 with a TD (9 tgts; corrected 2026-11-03 from a wrong "3-41", verified vs ESPN box in playlogs/2026_wk9/CHI_SEA_espn_summary.json). Burden U52.5 (56) and rec U4.5 (7) both lost, so these remain model-direction misses. Raymond 2-14 on 3 tgts.
- Swift rush U59.5 (69), Darnold O238.5 (188), JSN rec O7.5 (6), Kupp O29.5 (7), Wilson O19.5 (0).

### Rico's slips
Graded in `slips/2026-11-02_MNF_CHI_SEA_graded.md`: 13 of 20 legs hit.
- **$75:** lost on Kupp 7 and Wilson 0.
- **$20:** lost on Charbonnet 29 and SEA 2H (8-21).
- **$15 cash-out:** right call; Barner, Kupp and Swift rec would have missed.

**Wilson:** 0 offensive snaps and 7 special-teams snaps. The leg most likely stands as a loss and does not void (FanDuel voids only for no snaps). Ask FanDuel support to confirm.

### Biggest misses and why
1. **Loveland, Odunze and Burden: the sim was too low.** Caleb-era form plus a full-strength opponent adjustment against SEA's low allowed YPT set the medians. Loveland's was 25 yds on a 30% target share. SEA plays about 90% zone, and the damage came in the middle zones (LB/S/CB3 tags), not on the mapped outside CBs.
2. **Kupp:** CHI's coverage plus SEA's script (running while trailing) left him 1 catch.
3. **Wilson:** no offensive role in a 4-back committee. N1 now marks him do-not-play.
4. **SEA 2H -1.5:** the script read had SEA in control, but CHI went 21-8 in the 2H off SEA turnovers.

### Ghost6 grades (runs/2026-11-02_SEA_CHI_ghost6/defense_profile.md)
**Game reads: 6 of 9 right.**
| Read | Ghost6 call | Result |
|---|---|---|
| CHI 1H +1.5 | supported | ✓ |
| SEA 2H -1.5 | supported | ✗ |
| JSN 70+/90+ | supported | ✓ |
| Burden 30+ | supported | ✓ (7-56) |
| U58.5 | supported | ✓ |
| Loveland ATD | challenged | ✓ (no TD) |
| Kupp 10+, Swift 50+, Wilson 15+ | neutral | Kupp ✗, Swift ✓, Wilson ✗ |

**Defender calls: 2 right, 2 wrong, 1 gap.**
- Kupp limited by Gordon: right result, mechanism unverified. Gordon played 62%, and the DPI was on J. Johnson.
- Burden's edge vs Emmanwori: right.
- **Odunze limited by Witherspoon/Jobe: wrong.** Odunze went 4-87, all four catches explosives, mostly over the middle.
- **Loveland held: wrong** (7-65).
- JSN with Muhammad out: flagged as a gap. Stevenson took the most tags.

**Our checklist coverage block** mapped outside CBs against a zone defense. The fix is a middle-of-field / zone-hole allowance input (code note 4/8).

## 4. Replay under the fixed rules
Setup:
- Rules: no shrink, SCHEME_EDGE with alerts, mirror overs, N1-N3, depth_rule.
- Pool: 209 legs at FanDuel prices plus FD alt rungs for Loveland, Burden, Odunze and Raymond (and Rico's other players), at kickoff minus 30 min.
- Sims: current tools/sim_v6.py.
- Location: `backtests/mnf_chi_sea_replay_2026-11-03/`. The run fails strict on the run-level "film" source only; that miss was waived for the leg grades.

**19 legs pass: 12 hit, -$2.59 at $10 flat.** The 190 blocked legs went 75 hits.
- JSN recyds O49.5-O109.5: 6 rungs, all hit. O124.5 lost.
- JSN rec O4.5 and O5.5 hit. O6.5, O7.5, O8.5 and O9.5 lost.
- Barner U29.5 and rec U3.5 hit.
- Kupp rec U2.5 at +120 hit.
- Horton U23.5 and rec U2.5 lost.
- Darnold rush O4.5 hit (DraftKings price; consensus template line).

**Loveland, Burden, Odunze: NOT caught.** Their overs had negative or near-zero edge at every rung:
- Loveland rec O3.5: -8.8
- Burden O29.5: -10.6
- Odunze rec O1.5: +0.4

None of them were SCHEME_EDGE all four, because matchup and scheme_fit were False against the mapped CBs. The fix is in code notes 4 and 7: zone-hole allowance, plus a target-share sanity check → MODEL-SUSPECT → mirror over to manual review.

**Depth rule:**
- **Raymond:** a depth receiver (WR3, 6.3% Caleb share, script_pass OK). Every rung was **BLOCKED** on defender_giving, because Pritchett had allowed 4.22 ypt (and the high/main rungs are not "low"). His low rungs that would have hit: yds O4.5 and O9.5, rec O0.5 and O1.5. He had 2-14 receiving.
- **Odunze:** WR2 by Caleb-era share (Burden 19.0 > Odunze 14.3 > Raymond 6.3), so the depth rule does not apply.
- **Kupp/Horton:** blocked because the script did not call for passing. Correct: Kupp went 1-7.

**SCHEME_EDGE alerts:** 7, all on Kupp overs, and all would have lost. The depth rule blocked them.

**§14:** blocked JSN O99.5 (-113), which was SCHEME_EDGE all four and would have hit. The same gate passed O109.5 at +124 (code note 6).

**Rico's slips under the fixed rules:**
- Only JSN 60+, 70+ and 110+ pass.
- No slip as placed could be built (5-8 legs, TD legs, N1 backs, depth and edge cuts).
- That is $0 risked against the actual -$95 plus the $15 cash-out.

**Door check (read-only):** `door.py` evaluate() in-process, DOOR_OUT=/tmp, gate result from the harness; see `door_check.py` / `door_check.json`.
- A rules-built slip using the top edge per FanDuel player passes the door with 0 fails, in both versions:
  - 4 legs: JSN O124.5, Horton U23.5, Kupp rec U2.5, Barner rec U3.5
  - 3 legs: the same minus Barner
- Both versions **lose** (JSN 118, Horton 26), so -$10 per slip.
- Rico's $15 slip as built gets 11 fails: GATE_PASS ×6, SHORT_PRICE ×3, DEPTH_RECEIVER, SLIP_SIZE.

## 5. Code
- Notes are appended to `postmortems/2026-11-03_code_notes_for_ghost6.md`. Already covered by the build: (a) ledger part, (b), (c), (g). Uncovered: 9 items.
- Deleted `tools/tests/make_fixture.pre_form.py`; `test_run_gate.pre_form.py` was not present.
- `cd tools && python3 -m pytest -q tests`: **406 passed**.
- `ledger_coverage_check.py`: OK.
