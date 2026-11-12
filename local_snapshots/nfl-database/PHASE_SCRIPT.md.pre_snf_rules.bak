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
