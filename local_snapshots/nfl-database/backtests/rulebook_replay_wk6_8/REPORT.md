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
