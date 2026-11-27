# Defense coverage profiles: PHI @ DAL (Thanksgiving, kickoff 2026-11-26T21:30Z / 4:30 PM ET)
Research only. projection_ready=false. Profiles INFORM projections; they do NOT verify a main defender (P4 still requires a named PBU/INT/DPI).

## Sources (all free; no paywall/login bypass; PFF picks NOT used for edge)
| Source | What | Pulled |
|---|---|---|
| nflverse PBP 2026 REG W1–W11 (`_shared/nflverse/play_by_play_2026.parquet`, pulled 03:49 ET) | Allowed to RB/WR/TE (targets, rec, yds, TD, PPR FP), QB rush allowed, explosives, RZ TD% — computed by `def_allowed.py` (ranks: 1 = stingiest, 32 = most allowed) | computed 13:3x ET |
| NFL Next Gen Stats via nflverse NGS mirror (`ngs_*.csv.gz`; nextgenstats.nfl.com API returned 401, not bypassed) | Separation/cushion allowed by position, RYOE allowed, CPOE allowed (opponent NGS qualifiers only) | see ngs_PULLED_UTC.txt |
| StatRankings CoverageIQ (vs WR) | man/zone/single-high/blitz rates | 03:59 ET |
| Sharp Football coverage page + Hribar Worksheet (free portion; RB/WR/TE sections paywalled → MISSING) | man/zone/MOF; pts/drive, explosive plays, QB rush allowed, Mitchell coverage note | 03:59 ET / see sharp_phi_dal_PULLED_UTC.txt |
| PFF free article (pff.com/news/bet-eagles-cowboys-thanksgiving-same-game-parlay) | data points only: DAL last in EPA/run play allowed, 31st designed rush yds allowed. Its picks are NOT used | 13:5x ET |
| ESPN injuries API | statuses | see ../prekick/espn_inj_PULLED_UTC.txt |

## DAL defense (what Milton/Barkley/PHI pass-catchers face)
- **Scheme:** man 46.6% (#2 most), zone 51.8%, single-high 58.1% (#7), **blitz 25.1% (#27, rarely blitzes)** [StatRankings]. Sharp: man 22.3 / zone 69.3 / MOF-closed 55.7 (man-heavy vs league). New DC play-caller Mike Pettine (1 game).
- **Vs RB: worst-tier.** 23.8 car / 113.5 rush yds per game (rk30), YPC 4.77, **11 RB rush TDs + 5 RB rec TDs allowed**, 28.0 PPR FP/g to RBs (rk30). NGS RYOE allowed +1.09/att (rk31). PFF: last in EPA/run play allowed. Sharp: only defense with negative rush-defense EPA, 6.1 yds/play allowed (#32).
- **Vs WR:** 18.5 tgt (rk17), 163.8 yds (rk27), 12 rec TDs, 37.4 PPR FP/g (rk29). NGS WR separation allowed 2.82 (rk17), CPOE allowed +3.66 (rk29). Sharp: 67.1% comp (29th), 7.9 Y/A (27th), 4.6 20+ yd plays/g allowed (most in NFL).
- **Vs TE:** 7.0 tgt (rk12), 49.5 yds (rk14), 4 TDs, 12.4 PPR FP/g (rk15) — middle.
- **Vs QB rush:** 24.2 yds/g allowed on 4.5 car (rk30; Sharp shows the same 24.2, 30th). 8 opposing QBs reached double digits.
- **Who scores on them:** RBs (16 TDs total: McCaffrey 3, Henry 2, Allgeier 2, Barkley/Pierce W7) and WRs (12 rec TDs, spread out). RZ drive TD% .528 (rk22).
- **Weak spot:** run defense (RB and QB runs) + explosive passes. **Strength vs PHI:** low blitz rate meets Milton's worst split (no-blitz 4.15 YPA, n=64, LOW-SAMPLE); pressure rate 35.9% (14th).
- Availability: S Locke OUT, CB Bland IR, CB Moore (IR + 'questionable' conflict), S Thompson Q (off IR).

## PHI defense (what Dak/Javonte/Lamb/Pickens face)
- **Scheme:** man 39.5% (#9), zone 60.5%, single-high 57.7% (#8), **blitz 26.5% (#25)** [StatRankings]; Sharp man 17.5 / zone 74.3 → **level disagreement on man, SHARP CAUTION**. Pressure 12.3% (#29) in source packet; Inquirer/Eagles site say 4-man rush has 11 sacks over last 2 games.
- **Vs RB: strong in receiving, average on the ground.** RB rec 17.7 yds/g (rk2), 0 RB rec TDs; rush 102.3 yds/g (rk22), YPC 4.03, 6 RB rush TDs, 19.0 PPR FP/g (rk8). NGS RYOE allowed +0.14 (rk14). Run D improved since W7 (288 rush yds allowed over last 3 per DAL site), but Jordan Davis traded and Baun on IR.
- **Vs WR: the soft spot.** 21.8 WR tgt/g (rk32, most), 175.3 yds (rk31), **11 WR rec TDs**, 37.8 PPR FP/g (rk30). But NGS WR separation allowed 2.59 (rk6, tight) and CPOE allowed −2.12 (rk7): volume-driven, not separation-driven. Sharp: 61.1% comp (7th), 6.9 Y/A (14th).
- **Vs TE:** 6.1 tgt (rk1 fewest), 44.7 yds (rk8), 3 TDs, 10.9 PPR FP/g (rk8) — tough.
- **Vs QB rush:** 17.8 yds/g on 3.7 car (rk22), 3 QB rush TDs (Ward 2, Keenum), scrambles 2.1/g.
- **Who scores on them:** WRs (11 rec TDs; DAL W7: Lamb 2, Pickens 1), RB rushers (6). RZ drive TD% .488 (rk16).
- **Weak spot:** WR volume/TDs. **Key coverage note (Sharp, coverage-charting, NOT a PBU/INT/DPI verification):** in W7, DAL pass-catchers caught 3 of 8 targets for 24 yds in Quinyon Mitchell's coverage. ESPN 11/25 22:21Z: Mitchell has no injury designation (expected to play). CB Jonathan Jones OUT; DAL site says Woolen was benched. LB Ebiketie OUT, Baun IR.

## Implications for candidate legs (inform only)
| Leg | Profile says | Effect |
|---|---|---|
| Dak rush O9.5 | PHI QB rush allowed rk22 but low blitz/pressure → fewer forced scrambles; Dak cleared 9.5 in 4/10 games (14, 26, 19, 20; misses 7, 7, 8, 1, 7, 9) | No upgrade; stays REJECT |
| Pickens 80+ | PHI WR volume soft (rk31) but tight separation (rk6); Mitchell back and held DAL to 3/8-24 in W7 | Downgrade risk; stays WATCH |
| Barkley rush | DAL worst run D (RYOE rk31, 113.5 RB yds/g, 11 RB rush TD); passes 50% rule (61% of non-kneel carries in Milton starts) | Matchup up, script down (PHI +8.5). Conflict → no leg |
| Milton rush | DAL 24.2 QB rush yds/g allowed (rk30), man-heavy (#2) | Market already at 31.5/32.5; sim median 31.0 → no edge |
| Javonte rush | PHI RB rush rk22, improving | §9 favorite-under bar; no leg |
| DAL/PHI receivers | — | Still CUT at P4 (no verified main defender) |
