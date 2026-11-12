# Test D — no passing yards + game lines, Weeks 6–8 + MNF (TEST ONLY)
Requested by Rico directly (Nov 3, 6:17 AM ET). Base: 57d1eb8 replay pool + Test C (87d39b1). **Zero Odds API credits, no network calls.** Only saved prices were used. No held files were edited.

## Method
- `run_test_d.py` uses the same slip/door code as grade_slips.py and Test C, copied verbatim. Only the pool changes. The method is unchanged: one leg per player, sort by raw edge, M1 cross-game greedy + M2 chunks, $10/slip, product of prices.
- Sizes: A = 3 and 4, C = 4 and 5, B = 6 and 7. The 4-leg slips are shared by A and C, the same as in the original tests.
- Pools: **nopass** = 463 − every passyds leg (main + alt, over + under) = 437. **combined** = nopass + the game-line legs that pass the gate = 438.
- `game_lines.py` builds the price inventory and the game-line candidates. `summarize.py` builds the tables.

## (a) Removing passing yards alone
| | legs | W–L | hit | P/L |
|---|---|---|---|---|
| pool before | 463 | 241–222 | 52.1% | −$569.78 |
| removed (passyds) | 26 (22 over, 4 under) | 6–20 | 23.1% | −$152.30 |
| pool after | 437 | 235–202 | 53.8% | −$417.48 |

| test | original | no passyds |
|---|---|---|
| A 3–4 | 245, 20 won, 8.2%, −$1,070.42 (−43.7%) | 236, 29 won, 12.3%, −$354.06 (−15.0%) |
| C 4–5 | 187, 8 won, 4.3%, −$987.79 (−52.8%) | 180, 11 won, 6.1%, −$725.17 (−40.3%) |
| B 6–7 | 124, 2 won, 1.6%, −$428.71 (−34.6%) | 118, 0 won, 0%, −$1,180.00 (−100%) |

## (b) Game-line legs on their own
Only **1** game-line leg passed: **CHI@SEA (MNF) game total Over 46.5, FD −110**. It had raw edge +5.4, model p .585/.504/.574, model medians 50/47/50, and it was priced in the pre-kickoff sim at 7:45 AM ET Nov 2. It **won** (final 34–17 = 51): 1–0, +$9.09.
- O44.5 and O45.5 also cleared the bar. They were not added because the rule is one leg per game-market (highest edge). They also won.
- **Weeks 6–8, 0 game-line legs. There is no team-level model.** sim_v6 draws the game margin as Normal(−market spread, 13.5) and uses it only to tilt player volume. Its projection is the market itself, so edge against no-vig is 0 by construction. No game total model exists either. The run manifests' game_script_rb has only the market fav_spread.
- **MNF spread and ML: no independent margin model.** total_sim.py tilts team scores toward the market spread.
- Half/quarter: no prices were saved and no model exists (see f), so **N3 was never triggered**.

## (c) Combined pool (no passyds + game lines)
| test | slips | won | hit | P/L | ROI |
|---|---|---|---|---|---|
| A 3–4 | 237 | 30 | 12.7% | −$307.80 | −13.0% |
| C 4–5 | 180 | 11 | 6.1% | −$725.17 | −40.3% |
| B 6–7 | 119 | 0 | 0% | −$1,190.00 | −100% |

The only difference from nopass is the MNF game-total leg, which landed in two slips. It was in a 3-leg M2 slip that won (+$46.26) and a 6-leg M2 slip that lost on another leg.

**By week**

| week | A | C | B |
|---|---|---|---|
| 6 | 70, 11, −$1.65 | 53, 3, −$241.45 | 35, 0, −$350 |
| 7 | 90, 8, −$376.34 | 68, 3, −$400.50 | 46, 0, −$460 |
| 8 | 74, 10, +$43.93 | 57, 5, −$63.22 | 37, 0, −$370 |
| MNF | 3, 1, +$26.26 | 2, 0, −$20 | 1, 0, −$10 |

**Slip killers** (combined pool; slips killed / slips where it was the only loser; leg hit rate)

| market | A | C | B |
|---|---|---|---|
| rec under | 89 / 28, 52.1% | 82 / 13, 52.3% | 66 / 5, 52.8% |
| recyds over | 73 / 26, 44.2% | 71 / 13, 44.0% | 66 / 1, 41.7% |
| recyds under | 60 / 7, 58.3% | 56 / 1, 57.2% | 43 / 0, 58.1% |
| rec over | 43 / 17, 52.3% | 41 / 11, 53.2% | 39 / 2, 52.8% |
| rushyds over | 28 / 5, 59.4% | 28 / 1, 58.8% | 28 / 1, 57.6% |
| rushyds under | 20 / 0, 75.0% | 19 / 0, 75.6% | 16 / 0, 78.4% |
| game_total over | 0 (1–0) | — | 0 (1–0) |

## (d) Comparison
| test | original | no passyds | combined |
|---|---|---|---|
| A 3–4 | 20/245, −$1,070.42, −43.7% | 29/236, −$354.06, −15.0% | 30/237, −$307.80, −13.0% |
| C 4–5 | 8/187, −$987.79, −52.8% | 11/180, −$725.17, −40.3% | 11/180, −$725.17, −40.3% |
| B 6–7 | 2/124, −$428.71, −34.6% | 0/118, −$1,180, −100% | 0/119, −$1,190, −100% |

- Dropping passyds cut Test A losses by about $716.
- The original B result was two long-shot hits. Without them, B goes 0-for-all.
- No size is profitable over Weeks 6–8.

## (e) Door stamps
- **Strict reading: 0 slips stamped.** Every slip is blocked on GATE_PASS because the replay has no film source.
- **Leg-level reading:**
  - A: 236 pass, plus 1 blocked (the MNF slip containing the game leg).
  - C: 101 pass (the 4-leg slips); the 79 5-leg slips are blocked on SLIP_SIZE.
  - B: all blocked on SLIP_SIZE.
- **The door has no schema for game-line legs.** The harness gives the door only the player legs and stamps NO_GAMELINE_SCHEMA as a block. A door change would have to wait for Ghost6's hold to lift.

## (f) Game-line price coverage (gameline_inventory.csv)
- **Full-game h2h, spreads and totals:** saved for **42 of 42** events (pre-kickoff −30 min snapshot, 11 US books).
- **Alt spreads/totals and team totals:** MNF only (7:43 AM ET Nov 2 pull).
- **1H/2H/quarter spreads, totals and ML:** **0 of 42 saved** anywhere under /workspace/nfl-database.
- **Estimated cost to pull the missing lines (historical event odds = 10 credits × market × region):**
  - Full set (h1/h2 spread+total+h1 ML, q1–q4 spread+total = 13 markets): 130/event × 42 = **≈5,460 credits**. That is more than the ~5,449 left.
  - Minimum set (1H and 1Q spread + total = 4 markets): 40/event × 42 = **≈1,680 credits**.
  - Both break the lean budget (no history pulls until December, NFL ~250/week).
- **A model is needed even if the prices are pulled.** Nothing produces independent team score/margin distributions for Weeks 6–8 or for halves/quarters. Without one, game lines cannot clear the +3 bar, so pulling prices alone gives 0 legs.

## Caveats (carried over)
- Sharp man/zone is hindsight for Weeks 6–7 and stale for Week 8.
- Credits were under the floor in the original pull, so some alt events are missing.
- The MNF Bears RB sim was skipped.
- M2 prices same-game legs as a product.
- Alt no-vig is a proxy.
- The game-line sample is n=1.

Files: run_test_d.py, game_lines.py, summarize.py, slips_graded.csv, comparison.csv, by_week.csv, by_market.csv, game_candidates.csv, game_legs.csv, gameline_inventory.csv.
