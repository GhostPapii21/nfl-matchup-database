# BUF @ MIN, Monday Night Football — projection report (r2) — UNVETTED, NOT PICKS

**Top-line status: SIMULATION NOT RUN. Not every source category was used (NGS, film, coverage scheme/per-defender: MISSING). Ghost6 vet required before anything here can be shown as picks. projection_ready=false (unchanged).**

## 1. Header
- Game: 2026 season, Week 9 (not Week 10), game_id `2026_09_BUF_MIN`, ESPN event 401873051. Kickoff Mon Nov 9, 2026, 8:15 PM ET, U.S. Bank Stadium (dome).
- Date note: the request said "today's games (Week 9, Sunday Nov 8)". Today is Monday Nov 9. Sunday's Week 9 games are final. The only game today is this MNF game, which is the last Week 9 game.
- Data pulled: 5:25–5:30 PM ET Nov 9. Input cutoff: 5:30 PM ET. Odds snapshot: 5:26 PM ET.
- Model source: GhostPapii21/nfl-matchup-database main `9e789b5` (3:22 PM ET Nov 9, verified via GitHub read API). PR 1 merged earlier.
- Checklist: `/workspace/nfl-database/runs/2026-11-09_BUF@MIN_r2/checklist.md`.

## 2. Phases run (5 legs × 15 phases = 75 rows)
| Phase | Result across 5 legs |
|---|---|
| 1 Data reconcile | 5 PASS |
| 2 Opportunity | 3 PASS, 1 PASS-FLAG (Moore), 1 FAIL (Coleman: #3/#4 WR ban) |
| 3 Defensive profile | 2 PASS, 1 FAIL-FLAG (Moore: outside WR YPT 5.45 hard), 1 PASS (Cook: soft RB YPC), 1 MISSING (red-zone D for ATD) |
| 4 Defender coverage | 3 MISSING (receiving legs; no per-defender coverage source, no stand-ins), 2 N/A |
| 5 Pressure/blitz | 2 PASS, 1 FAIL-FLAG (Moore's share drops when blitzed), 2 N/A |
| 6 QB card | 5 MISSING (§15 card not run) |
| 7 Role/RB rules | 4 PASS, 1 FAIL (Coleman) |
| 8 Injuries | 5 PASS-FLAG (OL questionables, feed conflicts) |
| 9 NGS | 5 MISSING |
| 10 Film | 5 MISSING |
| 11 Environment | 5 PASS (dome, INDOOR) |
| 12 Source audit | 5 FAIL (category gaps) |
| 13 Game script / 10G | 5 PASS (BUF moderate favorite) |
| 14 Models/price/edge | 5 MISSING (SIMULATION NOT RUN; ATD also NOLINE) |
| 15 Inactives | 5 NOT_YET (checked 5:30 PM ET; list expected ~6:45 PM ET) |

## 3. Sources used, by category
- **Core stats and play-by-play:** nflverse `play_by_play_2026.parquet` (release pulled 5:25 PM ET; data through Nov 8, Week 9), nflverse snap counts (through Week 9), nflverse games.csv (schedule, roof, lines), ESPN depth charts (BUF, MIN). PFR advanced and gamebooks were not pulled.
- **Coverage schemes and matchups:** FTN charting through nflverse (box count, blitzers; date_pulled Nov 9 7:02 AM ET). **Man/zone and MOF: MISSING.** FTN's nflverse release has no coverage field, and the 2026 nflverse participation file is not published (HTTP stub). Sharp, StatRankings, PropsMadness and SumerSports were not used. Per-defender coverage is **MISSING**. The local `defender_ledger.csv` MIN rows are tacklers after the catch, which are banned stand-ins.
- **Next Gen Stats:** MISSING. Not pulled this run.
- **Film:** MISSING.
- **Injuries and news:** ESPN game summary injuries (entries stamped Nov 7–9; pulled 5:25 PM ET); NFL.com official Week 9 injury report (pulled ~5:29 PM ET). Team sites and team X were not used.
- **Weather:** `tools/weather_forecast.py --week 9` (NWS + Open-Meteo, SRC-1) at 5:25 PM ET. Roof is dome, so the result is INDOOR with no flag. ESPN's AccuWeather field is ignored under SRC-1.
- **Odds and props:** The Odds API via `tools/pull_odds.py`, one pull at 5:26 PM ET (FanDuel, DraftKings, Pinnacle, PrizePicks, Underdog). That used 35 credits: 2,309 remaining before, 2,274 after (floor 2,000). Anytime-TD markets are not in the puller's market set, so they are NOLINE.

## 4. Simulations
**SIMULATION NOT RUN.** Monte Carlo, Bias and Game Randomness: 0 trials, no seed.
- Blocker 1 (documented entrypoint): main `9e789b5` README says production validation is "Not validated. Acceptance is fail-closed." It also lists `projection_ready` false and the "100k trials and the 15-phase ledger: Deferred… not implemented" (NFL-56). PROPOSED_ROUTINE_BOOTSTRAP step 5 says not to start a batch simulation while projection_ready is false. The local blocker packet marks `DEFERRED_100K`, and the NFL-49 final acceptance is not met.
- Blocker 2 (data): local `tools/sim_v6.py` reads `runs/2026-11-01_shared_src/play_by_play_2026.parquet`, which has data through 2026-10-29. That is STALE (more than 48 h old, and missing BUF Week 8 and MIN Week 8). Running it would breach the STALE rule.
- No other engine was substituted. Research branch `research/wentz-2025-third-down-drive-audit` has a 900k conditional BUF@MIN sim (seed 20261109). It is **research-only, not accepted output**, and is not used here.

## 5. Projections (deterministic Phase 2 math, not simulation output) and leg verdicts
**James Cook rushing.** Projected BUF team rushes are about 31: the season average is 31.0 per game (7 games), and BUF is favored by 3, so no trailing trim applies. Cook's share of team rushes over the last 3 games is 63.6% (68 of 107), which gives **about 20 carries (range 17–23)**. YPC bracket: his away YPC is 4.38. Applying the MIN opponent factor (4.56 RB YPC allowed ÷ 4.16 league) to the league average gives 4.56. That puts the projection at **about 86–90 rush yards**. The market is FD 83.5 and DK 86.5. Wentz game management: MIN was 2-0 in Wentz's two starts (Weeks 1–2, 23 attempts each, 39-22 and 9-3). That supports a low-possession, run-leaning MIN script, which caps BUF's play volume rather than its share. This is a scenario note, not a fitted adjustment.

**Josh Allen pass attempts.** He averages 29.9 attempts per game for the season (sacks excluded) and 29.3 over the last 3, so the projection is **about 30 (range 26–35)**. He has gone under 30 twice (26 in Week 3, 20 in Week 5).
- Target tree, season share: Shakir 19.7%, Kincaid 18.1%, Moore 14.0% (18.6% in the games he played), Coleman 14.0%, Cook 8.8%, Ty Johnson 7.8%. Palmer (6.2%) is on IR, so his targets are vacated.
- On about 28 team targets: Shakir ~5.5, Kincaid ~5.1, Moore ~5.2 if active, Coleman ~3.9, Cook ~2.5.
- Vs MIN's blitz (#1 at 72.8%), Allen's blitzed targets shift to Shakir 22.9%, Kincaid 18.6% and Coleman 18.6%, with Moore at 11.4%.
- "Primary targets vs man" cannot be computed because no man/zone source was available (MISSING).

| Leg | Projection | FD line/price | DK | No-vig (FD) | Edge | Verdict / cut phase |
|---|---|---|---|---|---|---|
| Shakir 3+ rec | 5.3 tgt × .71 = 3.8 rec | O2.5 −360 | −367 | .732 | MISSING (no model p) | CUT: P4 MISSING, P14 MISSING (+ common gaps) |
| DJ Moore 30+ rec yds | ~50 yds (5.2 tgt × 9.6 YPT) | O29.5 −275 | −313 | .691 | MISSING | CUT: P3/P5 FAIL-FLAG, P4 MISSING, P14 MISSING |
| Keon Coleman 2+ rec | 3.9 tgt × .74 = 2.9 rec | O1.5 −220 | −210 | .643 | MISSING | CUT: P2 FAIL (#3/#4 WR over ban), P4 MISSING |
| Cook 60+ rush yds | ~20 car, ~86–90 yds | O59.5 −360 | −411 | .738 | MISSING | CUT: P14 MISSING (+ common P6/P9/P10/P12/P15) |
| Allen OR Cook anytime TD | Allen 9 rush TD and Cook 7 in 7 games | NOLINE | NOLINE | — | — | CUT: P14 NOLINE; P3 red-zone MISSING |

Common gaps on every leg: P6, P9 and P10 MISSING; P12 FAIL; P15 NOT_YET. **No card: 0 qualifying legs. No alternates or fades are offered, because none can pass P14 without sims.** Scenario leans are worth Ghost6 review once sims are allowed: Cook rushing volume clears the 59.5 rung by about 26 yards on the deterministic math, and Shakir's blitz-driven share rise supports his reception floor. These are not picks.

## 6. Risks and checks still to come
- Inactives are NOT_YET; recheck at about 6:45 PM ET.
- Wentz is not officially confirmed. ESPN's depth chart still lists Murray QB1 and Wentz QB2, with Murray OUT on both ESPN and NFL.com.
- BUF OL: LT Dion Dawkins is Q (DNP, rib) and Alec Anderson is Q (ESPN lists him OT, NFL.com G).
- Feed conflicts: Shavers is OUT on ESPN but Q on NFL.com. Hancock is on IR per ESPN but Q per NFL.com. Greg Gaines (DT, Q) is on NFL.com only.
- MIN safeties Theo Jackson and Jay Ward are Q.
- The pressure input is a PROXY. Blitzed samples: Allen n=73.
- Desk-data mismatches are listed in `desk_verification.md`.
