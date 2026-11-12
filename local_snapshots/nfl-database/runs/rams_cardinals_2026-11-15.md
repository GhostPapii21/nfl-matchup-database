# Rams @ Cardinals — NFL Custom Phase Script run (Oct 29, 2026 model)
Run: Thu Oct 29, 2026 ~4:15 AM ET. Data/code: ./rams_cardinals_2026-11-15/ (profile.py, sim.py, defense_profile.json, projections.csv, player_logs.json)

## Game
- Week 10, Sun Nov 15, 2026, 4:05 PM ET, State Farm Stadium, Glendale (retractable roof). Sources: statefarmstadium.com event page (2:05 PM local), nfl.com/games/rams-at-cardinals-2026-reg-10, NFL Football Ops 2026 schedule.
- Most recent meeting: Week 6, Oct 18, 2026 at SoFi (ARI@LA).
- Game lines (look-ahead, pulled Oct 29 ~4:10 AM ET via statsniper.com / scoresandodds.com): DraftKings LAR -10.5, total 47.5, ML LAR -470 / ARI +360. Implied team totals ~29 LA / ~18.5 ARI.
- PLAYER PROPS: NOT POSTED for this game (statsniper: "Player prop lines have not been posted for this matchup yet"). Every lean below = LINE PENDING / No Bet.

## Data & freshness
- nflverse 2026 PBP/FTN/weekly stats/snaps, refreshed Oct 29 ~4:05 AM ET; PBP through Week 7; player weekly stats through Week 6 for these teams (Week 7 and Week 8 box scores not yet in the public files — missing).
- Official injury report for Week 10: not issued yet (comes Nov 11–13). Latest available: Week 8 (ESPN via whosstarting.com, Oct 28 7:31 PM ET).
- Percentile interpretation: 5th–25th are LOW-SIDE percentiles = the number the player clears 95/90/85/80/75% of the time. MAIN = 15th (clears 85%).
- Three-model consensus: Monte Carlo 10k (bootstrap 2026 70% / 2025 30%, lognormal noise), Bayesian normal-normal (2025 prior, 8-game weight), Game-randomness (2026 games × N(1,0.15) script factor). Percentiles from pooled 30k draws; median = median of the three model medians. Heuristic, not backtested.

## Defensive profiles (2026, Weeks 1–7, computed from nflverse PBP)
| Metric | LA D (faces ARI) | ARI D (faces LA) |
|---|---|---|
| WR YPT | 6.68 | 9.71 |
| Outside WR YPT (left/right) | 6.04 | 9.77 |
| TE YPT | 5.03 | 8.20 |
| RB rec YPT / RB rec yds pg | 6.70 / 45.0 | 6.67 / 31.4 |
| Deep (20+ air) YPT | 5.45 | 13.33 |
| Run YPC (non-scramble) / RB YPC | 3.68 / 3.77 | 4.21 / 4.29 |
| RB rush yds pg | 85.7 | 103.6 |
| Blitz % (5+ rushers, FTN) | 29.4 (rank 17) | 30.4 (rank 16) |
| Pressure rate (PFR) | 19.3% (rank 26) | 19.6% (rank 25) |
| Explosive pass 20+ / rush 15+ | 14 / 12 | 23 / 9 |
| RZ TD% allowed (drives) | 46.2 (26 trips) | 70.8 (24 trips) |
| 3rd-down conv allowed | 32.2% | 41.0% |
| Man/zone (2025 only; 2026 not free) | 25/75 | 28/72 |
| Two-high (2025 only) | 52% | 54% |
| Pass-rush win rate, PFF coverage grades | MISSING (paid) | MISSING (paid) |

Coaching: ARI HC Mike LaFleur; 2026 PROE ARI -1.0%, LA +0.3%; play-action LA 26%, ARI 17%; motion LA 68%, ARI 62%.

## QB cards / gates
- Stafford 2026: vs blitz 60.2% / 7.05 YPA / 5.6% sack; no-blitz 71.4% / 7.31. ARI blitz 30% (<35%) → no blitz gate. OK.
- Brissett 2026: vs blitz 57.5% / 5.04 YPA / 9.6% sack (weak); no-blitz 68.1% / 5.95. LA blitz 29% (not top 10, not ≥35%). Panthers rule: not triggered on available data (blitz rank 17, OL Jon Gaines II only Questionable in Wk8, PRWR MISSING) — recheck Week 10 report. Weak blitz card noted as a soft negative for Wilson/McBride yards.
- Game script: LA -10.5 → ARI likely trails (feeds McBride volume; ARI RB carries dry up); blowout risk trims late Puka/Adams volume, adds Corum late carries.

## Player sheet (lines all PENDING)
| Player | Role | Grade | Stat | 5th | 10th | 15th MAIN | 20th | 25th | Median | Line | Lean |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Puka Nacua (LA) | Volume | Slight Positive (ARI WR YPT 9.71 ≥9.0, capped +3%) | Rec | 4 | 5 | 5 | 5 | 6 | 7.8 | pending | line pending |
| | | | Rec yds | 45.6 | 59.9 | 67.3 | 72.7 | 77.2 | 103.0 | pending | line pending |
| Davante Adams (LA) | Explosive/RZ | Neutral (ARI outside WR YPT 9.77 <10.5; deep YPT 13.3 + RZ TD% 70.8 = TD upside) | Rec | 2 | 3 | 3 | 3 | 3 | 4.5 | pending | line pending |
| | | | Rec yds | 22.6 | 26.5 | 29.5 | 32.7 | 35.8 | 49.3 | pending | line pending |
| Kyren Williams (LA) | Rush-Receive | Neutral rush (ARI RB YPC 4.29, not >4.4); Neutral rec (ARI RB rec 6.67 YPT, 31.4 yds pg allowed); favorite script + | Rush yds | 36.7 | 41.4 | 44.8 | 47.9 | 51.0 | 67.3 | pending | line pending |
| | | | Rec | 1 | 2 | 2 | 2 | 2 | 3.3 | pending | line pending |
| | | | Rec yds | 3.0 | 9.1 | 11.3 | 12.9 | 14.6 | 25.0 | pending | line pending |
| Blake Corum (LA) | RB2 | Neutral (same run D; 15–45% snaps) | Rush yds | 5.9 | 11.7 | 13.5 | 14.8 | 16.2 | 33.3 | pending | line pending |
| Trey McBride (ARI) | TE-Primary | Slight Negative (LA TE YPT 5.03 ≤5.5 → yards cut 12%; volume holds, trailing script) | Rec | 5 | 5 | 6 | 6 | 7 | 7.9 | pending | line pending |
| | | | Rec yds | 22.1 | 26.7 | 30.3 | 33.7 | 37.1 | 53.6 | pending | line pending |
| Michael Wilson (ARI) | Explosive | Slight Negative (LA outside WR YPT 6.04, deep YPT 5.45; Brissett weak vs blitz) | Rec | 1 | 2 | 2 | 2 | 3 | 4.5 | pending | line pending |
| | | | Rec yds | 0.2 | 12.6 | 16.3 | 19.5 | 23.8 | 40.6 | pending | line pending |
| Jeremiyah Love (ARI) | RB1 (committee) | Slight Negative (LA run YPC 3.68 ≤3.8 → run suppression -10%; trailing script). Q (ankle) Wk8; missed Wk6 | Rush yds | 14.6 | 18.1 | 20.5 | 22.6 | 24.8 | 37.3 | pending | line pending |
| Tyler Allgeier (ARI) | RB2 (committee) | Slight Negative (run suppression) | Rush yds | 0 | 0 | 2.8 | 5.6 | 6.7 | 20.4 | pending | line pending |

Low-sample/secondary markets (Love/Allgeier/Corum receiving) in projections.csv.

## Status / injuries
- Week 8 report (not official for Wk10): Jeremiyah Love Questionable (ankle, limited Wed); ARI QB Brissett starts, Minshew 2, Beck emergency 3rd; James Conner IR; Tip Reiman OUT; Jalen Brooks IR. Rams: Trent McDuffie (CB) was OUT Wk6; Colby Parkinson on Wk8 report. Puka missed Weeks 2–3 (4 games logged). No Week 10 OUT/IR edges yet → no injury boosts applied.

## Strongest provisional leans (not bets until FD/DK lines post and pass section 10/18 gates)
1. McBride receptions — volume holds (8.2/gm, 22–39% target share, ≥7 rec in 5 of 6) vs hard TE yards defense: favor receptions over his yards line.
2. McBride/Wilson receiving yards UNDER lean — LA TE YPT 5.03 and outside WR YPT 6.04 are top-tier stingy; but trailing-script rule (sec 14) bans TE check-down yards unders on a team that could trail → McBride yards under is BLOCKED; Wilson yards under allowed only with a real line.
3. Puka Nacua receiving yards OVER — soft ARI WR YPT 9.71, deep YPT 13.3, RZ TD% 70.8; median 103.
4. ARI RB rushing UNDER (Love) — LA RB YPC 3.77 + ARI as 10.5-pt dog.

## Missing data
- All FD/DK player props for this game (not posted). Week 10 official injury report. Week 7–8 player box scores in public nflverse files. Week 8 game results not incorporated. 2026 man/zone & coverage shells (2025 used). PFF coverage grades, pass-rush win rate (paid). Public NGS page pull not done separately (nflverse NGS cache exists but not used in grades). Weather n/a (retractable roof; status decided game day).
