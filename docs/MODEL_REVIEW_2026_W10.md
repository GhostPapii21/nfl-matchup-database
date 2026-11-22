# NFL model review after Week 10 (2026)

Written Nov 22, 2026 (Week 11 Sunday). This is the model we carry into next season, so each item says whether to change it
now or let it run. Numbers come from files in this repo; each section names where.

## 1. Is the data complete? Yes.
`research/season_context_2026/AUDIT.md` (rebuilt every Tuesday):
- 150 of 150 games in Weeks 1-10: final scores, full play-by-play, quarter scores that add up to every final.
- Official NFL game books for all 150 games (`data/gamebooks/2026/wk01`-`wk10`). Before today only Week 9 was in.
- Second source check: game book quarter scores equal play-by-play quarter scores in all 150 games.
- Season context database: quarter/half winners, rain and bad weather, international, byes, short weeks, key players
  out, QB changes during games, injury factor in losses, first- vs second-half adjustments, top-5/bottom-5 defenses,
  team profiles and player splits (`research/season_context_2026/README.md`).

## 2. What the model does right
| Piece | Evidence |
|---|---|
| Yardage simulation (targets x catch x yards, script, injuries, weather) | Beats each player's own history at every threshold on 8,259 player-games 2024-2026, and on the 2026 holdout (`dashboard/results/opportunity_backtest.md`) |
| Rain/wind equation | Measured on 211 rain team-games since 2018; cuts WR yards about 15% in rain. Re-checked today on 13,526 receiver-games: rain -16% (CI -9% to -23%). Correct and firing |
| Teammate-out rule | Refit on 2022-2025 (`research/teammate_out_2026-11-16`); next back gets about 63-65% of carries, as observed |
| 80-yard stars | Calibrated on held-out 2025-26: 3 stars hit 51%, 2 stars 43%, 1 star 35% |
| Accuracy vs the books | Model and FanDuel are equally accurate (Brier 0.1136 each); averaging the two is better (0.1118) |

## 3. What is wrong or weak (and what was fixed today)
| # | Problem | Status |
|---|---|---|
| 1 | The 80-yard stars ignored weather: the yardage simulation applied rain/wind, the star formula used raw averages | **Fixed today** (`dashboard/watch.py`, test added) |
| 2 | Game-day gate blocked every game: Odds API at 0 credits, then below the 800 floor | **Fixed** (#68): prices from the free direct pulls; four books = FanDuel, DraftKings, BetMGM, Bovada |
| 3 | GitHub started the gate hours late and missed Thursday's window | **Fixed**: cron-job.org starts it at exact times |
| 4 | Post-game grading ran for 1 game all season, so there was no record of what worked | **Fixed today**: every game graded every Tuesday + `grading/scorecard.py` (stars by level, ROI at the FanDuel price, baseline bias) |
| 5 | Game books for Weeks 1-8 and 10 missing | **Fixed today** (all 150) + weekly fetch |
| 6 | Simulation slightly low in the middle of the range: 12+ carries said 45-55%, happened 59-67%; WR 40+ yards said 30%, happened 34% in 2026 | **Fix now** (handoff Phase 3, item A): calibration layer fit on 2024-25, tested on 2026 |
| 7 | 100+ yard chances run high at the top: said 34-44%, happened 22-26% (small n) | **Fix now** with item 6 |
| 8 | Next Gen Stats and PFR advanced receiving/rushing were not pulled | **Pulled from today** (`pregame/sources.py`); using them is handoff item B |
| 9 | No ledger of real bets (book, price, stake, closing price, result) | **Start now** (section 5) |
| 10 | Packet text still names Hard Rock and Caesars as the bettable books | Cosmetic; fix with item B |

All 984 tests across 9 suites pass.

## 4. What the season taught us (situations)
Team results (`research/season_context_2026/team_profile.csv`, 2026 only):
- Off a bye 13-3 (+8.7 margin). After an international game 8-5. Short week 9-9.
- QB changed during the game 5-15 (-13.8). Starting QB out 11-17.
- Rain games average 36.6 points vs 46.2 overall.
- The first-half winner won 108 of 139 games.

Player effects on top of the projection, 13,526 receiver-games 2022-2026 (`research/context_effects_2026-11-22`):
| Situation | Receiving yards | Targets | Use it? |
|---|---|---|---|
| Rain/snow | -16% (significant, both periods) | -7% | Already in the model |
| Wind 15+ mph | -8% (significant) | -2% | Already in the model (wind dial) |
| Team on a 2+ game losing streak | -5% (significant) | -4% | Candidate: confirm on 2026 second half, then add |
| Short week | +6% (borderline) | +5% | Watch |
| Off bye, international, after international, home, divisional, new QB | no reliable effect | | Do not add |

So bye and international help teams win, but they don't change a receiver's share of the offense. Use them for sides
and totals, not player props.

## 5. Betting: what worked, what didn't, what to change
What the record shows:
- **No proven edge yet.** The model equals the book. On the same line, books price within their vig of Pinnacle's fair
  price: 0 of 1,588 prices beat fair by 2+ points (`research/edge_2026/README.md`).
- Starred players at FanDuel 80+ prices: +8.7% ROI on 68 bets (weeks 8-9). That's inside the noise.
- Betting where the model is 3+ points above the price: -47% ROI. The model alone is not a bettor.
- Long same-game parlays stack the hold of every leg and assume the legs are independent. A QB injury (Maye to DeVito)
  sinks every receiver leg at once.

Change now:
1. **Log every real bet** (date, book, market, line, price, stake, our probability, closing price, result). Without it,
   ROI and closing-line value can't be measured. The scorecard can read it.
2. **Bet the blend, not the model:** average model and book on the logit scale (`watch.blend_with_book`), and bet only
   when the blend beats the best of eight books by 3+ points.
3. **Shop the line:** the best of eight books instead of one adds 1-3 points of break-even on many props.
4. **Fewer, correlated legs:** 2-3 legs from the same game script (QB + his WR1), not 4-6 unrelated legs.
5. **Judge by closing-line value**, not win/loss. It settles in about 100 bets, not 1,000.

Let play out (until about 300 graded bets): star cutoffs, the losing-streak factor, the 3-point blend threshold.

## 6. Data sources
Pulled today: nflverse play-by-play, schedules, rosters, injuries, depth charts, snap counts, FTN charting, PFR defense,
**PFR receiving/rushing, Next Gen Stats receiving/rushing/passing (new)**, ESPN injuries, weather forecasts, NFL game books,
and FanDuel, Pinnacle, DraftKings, BetMGM, Bovada and others plus Grok files for lines.

Found through Firecrawl, worth adding (handoff item C):
| Source | What it adds | Access |
|---|---|---|
| NFL.com official injury/practice reports (Firecrawl provider `nfl-com`) | Wednesday-Friday DNP/limited/full practice | Free via Firecrawl |
| NFL Savant (nflsavant.com) | Routes and usage, rush yards over expected, referee flags/game, coaches' 4th-down habits | Free site |
| StatRankings (statrankings.com/nfl/coverage) | Targets per route, true target share, separation, yards per route by man/zone and Cover 0-9 | Free site |
| DraftSharks (Firecrawl provider) | Floor / median / ceiling projections to compare ours against | Free via Firecrawl |
| FTN | Coverage and route charting | Paid; the free nflverse FTN file is already in |

## 7. Plan for next season
1. Now through Week 18: items 6-9 above; grade every week; keep the bet ledger.
2. After the season: refit every equation on 2022-2026 including this season, with the context database as inputs.
   Add the coverage-type splits (man/zone) once a full season is collected. Re-test bye, international and losing streaks
   with 2026 included.
3. Next August: run the whole pipeline on the preseason to check the gates before Week 1.
