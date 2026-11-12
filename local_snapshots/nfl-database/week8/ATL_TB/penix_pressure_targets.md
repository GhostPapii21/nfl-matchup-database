# Penix under pressure: London vs Bijan vs Pitts (2026, ESPN PBP)
Built by week8/ATL_TB/pp.py from raw/dropbacks.json (ESPN summary API). Only Penix dropbacks are counted.
Penix started Wk3-7 (5 games). Wk1-2 were Cooper Rush/Jack Strand, and Tua threw 3 passes in Wk5. Those are excluded.

**DEFINITIONS (no free 2026 per-play blitz tags were found; no PFF):**
- **PLAY proxy** = a target with a QB hit [bracket] in the PBP. Sacks and scrambles are pressure dropbacks with no target.
- **GAME proxy** = HIGH-PRESSURE games, BAL Wk5 and CHI Wk6, with 8 sack/scramble/hit events each. LOW games are GB, NO and SF, with 1 each.
- Season blitz rate: Sharp, as used earlier: Penix blitzed 44.7%, 22.7% comp under pressure. TB blitzes about 43%.

| Wk | Opp | Date | Score | Penix | Pressure events (sk/scr/hit) | London tgt-rec-yds | Bijan | Pitts |
|---|---|---|---|---|---|---|---|---|
| 3 | @GB | 9/25 | W 35-14 | 18/25, 256, 1 TD, 1 INT, 0 sk | 1 | 10-9-194 | 2-2-19 | 2-1-5 |
| 4 | @NO | 10/6 | W 45-24 | 15/20, 223, 1 TD, 1 sk | 1 | 6-5-96 | 2-1-2 | 3-3-47 |
| 5 | BAL | 10/12 | L 23-30 | 19/32, 240, 1 TD, 3 sk | **8** | 9-6-98 | 6-3-18 | 6-5-42 |
| 6 | CHI | 10/18 | L 23-31 | 19/33, 225, 3 TD, 5 sk | **8** | 10-4-62 | 2-2-(-8) | 7-5-60 |
| 7 | SF | 10/25 | W 29-20 | 25/34, 213, 3 TD, 0 sk | 1 | 10-7-66 | 5-5-45 | 5-5-21 |
| **Total** | | | | 156 dropbacks | 19 | **45-31-516 (31% share)** | 17-13-76 (12%) | 23-19-175 (16%) |

## Split A: GAME proxy (high-pressure BAL/CHI vs low GB/NO/SF)
| | London | Bijan | Pitts | Penix |
|---|---|---|---|---|
| High-pressure (2 games) | 19-10-160 (80/g, 53% catch) | 8-5-10 (2.5 rec/g, 5 yds/g) | 13-10-102 (51/g) | 232.5 yds/g, 8 sacks |
| Low pressure (3 games) | 26-21-356 (119/g) | 9-8-66 (2.7 rec/g) | 10-9-73 (24/g) | 230.7 yds/g |

## Split B: PLAY proxy (targets thrown while hit)
Only 6 such targets: London 1-0-0, Pitts 1-0-0 (deep middle), Bijan 0, others 4. The 13 sacks and scrambles produced no target. The sample is too small to show a hot read, but it does show that **under pressure Penix eats sacks (8 total) or scrambles instead of checking down.**

## 3rd downs (all Penix 3rd-down targets)
- All 3rd downs: London 18-15-249 (44% share), Pitts 5-4-38 (12%), Bijan 3-1-19 (7%).
- 3rd-and-7+: London 10-9-106 (45%), Pitts 3-2-23, Bijan 0 targets.
- 4 of 6 3rd-down sacks/scrambles came in the BAL and CHI games.

## Conclusion vs TB (blitz ~43%; Egbuka OUT is TB-side context only)
- **Who he goes to:** London, clearly. That holds on 3rd down and in pressure games (10 targets per game either way), but efficiency drops: 53% catch rate and 80 yds/g in pressure games vs 119 yds/g in clean ones.
- **Pitts** becomes the #2 read under pressure (6.5 tgt/g, 51 yds/g).
- **Bijan is not a pressure checkdown:** 2.5 rec and 5 yds per game in pressure games, 0 third-and-long targets.
- **London 79.5:** at the pressure-game pace, both games came in at or under it (98 and 62). Lean under or a low rung.
- **Bijan 27.5 rec yds:** he went under in 4 of 5 Penix games (19, 2, 18, -8, 45). Lean under. **4+ receptions** happened only 1/5 times with Penix (Wk7 vs SF, a low-pressure game). That conflicts with the earlier note of "2 of 5", which likely counted a non-Penix throw or a different game set; re-check against the box. 3+ receptions: 2/5. Fade the 4+, and treat 3+ as a coin flip at best.
- **Penix under 229.5:** yardage didn't drop in pressure games (240 and 225, both trailing so passing volume went up) because of 8 sacks and the extra volume. The under is mostly supported by pressure games landing near the line and sacks killing drives; the risk is a trailing game script. **Lean under, but it's marginal.**
