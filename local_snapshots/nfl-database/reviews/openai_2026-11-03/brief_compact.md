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

=== FILE (excerpt): PHASE_SCRIPT.md ===
# NFL Custom Phase Script — Full Model (Updated Oct 30, 2026)
<!-- Data/workflow authority: GAME_SCRIPT_2026-10-29.md (phases 0-10G, 60 checks, ticket cap 6 target / 7 max) — run it alongside this model; where they conflict, the game script governs evidence rules. Permanent projection model, stored verbatim from the user on Oct 29, 2026. Supersedes the Oct 27 version. Rico's data-collection phases 1-8 live in MASTER_PROMPT.md. -->

## CORE PIPELINE (Oct 29 user-approved order; the Opportunity Gate is step 4)
0. Injury & status check: Questionable players are not cut automatically. Script them on low alts or fade. At 90 min pre-kick, ask the user to approve each inactive or Questionable player who matters.
1. Identify locked roles for both teams
2. Pull defensive coverage profile (YPT by position/route, Outside YPT, blitz %, zone vs man %, explosive plays allowed, RZ TD%, 3rd-down % allowed, run YPC allowed) plus HC/OC/DC tendencies
3. Game environment: spread, total, pace, projected script (who leads, who trails), whether each offense can sustain drives (3rd-down and red-zone rates vs this defense)
2A. DEFENDER COVERAGE CHECK (HARD, user rule Oct 31, 2026; no leg skips it): for every WR/TE/RB receiving leg, pull real defender numbers from Pro Football Reference advanced defense (free: targets, completions, comp %, yards, YPT, passer rating allowed per CB/S/LB), plus man/zone and MOF open/closed from nflverse FTN charting. Map the player to his likely defender, show whether that defender limits catches or yards, and match the player's routes (NGS/FTN) to that coverage. Stand-ins don't count; a leg missing this is cut. Full rule: the nfl-betting-script skill, section 8A.
4.
=== FILE (excerpt): backtests/confidence_check_2026-11-03/report.md ===
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
   Production `tools/sim_v6.py` and Thursday's `runs/2026-11-05_shared_src/sim_v5.py` currently run it at 1.0 (phase3 commit 6322cc5). R
=== FILE (excerpt): backtests/rulebook_replay_wk6_8/REPORT.md ===
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
  - Misses are matched to legs
=== FILE (excerpt): backtests/current_rules_wk6_8/REPORT.md ===
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
  - Depth inputs: WR rank and TE rank by targets over the last 4 
=== FILE (excerpt): backtests/current_rules_wk6_8/summary.md ===
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
=== FILE (excerpt): backtests/rico_method_wk8/REPORT.md ===
# Rico-method backtest, Week 8 2026 (TNF CAR@GB, Sunday 11 + SNF, MNF CHI@SEA). TEST ONLY: no bets.

## Integrity notes (read first)
- Reconstructed picks were locked in commit 3206cb8 (Nov 3 06:08 ET) and the slip method in 47223ba, both before grading.
- **Leak disclosure:** after the picks were locked but before grading, I opened week8/slips/slips_2026-11-01.md(.pre_snf.bak) to find the live legs. That file has graded Week 8 results appended to it. The picks were already committed, so they weren't affected, but I had seen some results before the replacement and slip steps ran. Both of those steps are mechanical (rules in slip_method.md) to limit how much that knowledge could matter. The analyst has also seen Week 8 postmortems in earlier sessions, so this is **not a blind test**.
- PFF: coverage and grades are locked on this account's tier, so it isn't used. Its season-to-date grades would also include Week 8 and later games.
- The reconstructed "read" is a **mechanical proxy** for the phase script, built from pbp and FTN data for weeks 1-7 plus pre-kick lines. It wasn't a hand-written per-game script. It uses: the player's last 4 games with the current QB; what the opponent allowed by position and market compared with the league (pbp weeks <8); opponent blitz rate (FTN weeks <8); and the nflverse closing spread and total, which are recorded but carry no weight. Not used: PFR Wayback, man/zone coverage and defender matchups (no point-in-time copy was pulled in this pass). The "reason" for each pick is the feature line in picks_locked.md.

## LIVE_READ picks (our actual pre-kick gated PASS legs, from manifest/build timestamps)
| Leg | Source (ET) | Actual | Result |
|--
=== FILE (excerpt): backtests/yardage_markets_wk3_8/v5/report.md ===
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
| GROK_ON_SAVED_GAME (compa
=== FILE (excerpt): backtests/v5_leak_audit/direct_answer.md ===
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
2026 Week 8 CAR@GB: marsh
=== FILE (excerpt): postmortems/2026-11-01_1pm.md ===
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
- Cut legs: 63 of 124 decided were good cuts; 61 would have hit (6 void/push). Costly cuts: Tuten rush O59.5/R+R O83.5 (104/159), Gibbs rush O87.5/R+R O121.5 (153/168), P
=== FILE (excerpt): postmortems/2026-11-01_4pm.md ===
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
- Vetted live legs at kickoff: none. Worthy rec yds O29.5 was cut at 08:46 (actual 13, good cut). Puka rec O7.5 passed vetting this morning but was cut at the 15:40 recheck for P4 UNVERIFIED (backup RCB Wax
=== FILE (excerpt): postmortems/2026-11-03_MNF_CHI_SEA.md ===
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
- **Context, Weeks 1-7:** CHI's run D was league-average (4.03 YPC, -0.