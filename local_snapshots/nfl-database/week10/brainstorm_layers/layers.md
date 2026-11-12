# JAX@BAL (Thu Nov 5, 2026) brainstorm layers, Weeks 1-8 (read-only)
Sources: nflverse pbp_2026 (wk1-8, 21,191 plays) + FTN charting 2026 (n_blitzers/n_pass_rushers/out_of_pocket/screen/throwaway), roster_2026, free PFF pages in ../pff_jax_bal/, ../jax_usage/, ../bal_def_snapshot/. Script: build.py.
UNAVAILABLE: NGS (nextgenstats.nfl.com fetch timed out; /tmp NGS file is a 404 body) -> no time-to-throw, no NGS route charts. Participation file corrupt (/tmp parquet bad magic) -> no coverage shell / man-zone / MOFO-MOFC. PFF true pressure, per-route data = Premium, not used.

## L1 Possession script (L1_drives.csv, L1_pace.csv, L1_bal_qbs.csv)
- BAL drives all: 7.33 plays, 2:44, 3-and-out 24.4%, score 36.7% (90 drives). Wk7-8: 26.1% 3&O, score 21.7% (23). Fagnano drives: 6.25 plays, 2:08, 3&O 37.5%, score 12.5% (n=8 drives — tiny). League 20.9% / 39.1%.
- JAX: 7.80 plays/drive, 3:05, 3&O 16.9%, score 46.5% (71 drives, 7 games). 58.3 off plays/g, 31.2 min TOP/g.
- Fagnano wk8: 24 dropbacks, 91 yds, 3 sacks, EPA/db -0.43.
- Estimate (hypothesis, not data): BAL 3&O ~30-35%, ~6.5 plays/drive -> JAX ~62-66 offensive plays, ~32-34 min TOP. Yes, JAX likely holds the ball most of the game; caveat 8-drive Fagnano sample and a big-favorite run-out lowers late pass volume.

## L2 Lawrence vs pressure/blitz (L2_*.csv)
- BAL blitz (FTN, 5+ rushers): 33.0% vs league 31.8% (300 charted dropbacks). Sack 5.7% (lg 6.2%), hit-or-sack 17.0% (lg 15.6%). Roughly league-average pressure.
- Lawrence vs blitz (66 db): 58.1% cmp, 7.02 YPA, sack 6.1%, EPA/db +0.15, 3rd-down conv 47% (n=17). No blitz (144): 69.6%, 9.30, 6.2%, +0.35, 35% (n=34).
- Pressure is a PROXY (qb_hit/sack/out-of-pocket/scramble): pressured 56 db: 51.2% cmp, 7.60 YPA, sack 23%, EPA -0.33, ball out 76.8%, 3rd conv 29% (n=17). Clean 154: 70.1%, 8.85, EPA +0.51.
- Time to throw: UNAVAILABLE (NGS).
- Read: blitz costs him efficiency but he still gets it out 94% and converts 3rd downs fine; real damage only when hit/flushed.
- Under pressure targets (proxy, n=38): Washington 10, Meyers 8, Strange 5, Tuten 5. Vs blitz: Washington 17, Strange 13, Meyers 11, Cameron 6, Tuten 5, BTJ 4.

## L3 Target ladder (../jax_usage/targets_season.csv, 7 games, 195 tgts)
1 P.Washington 48 tgt 24.6% (6.9/g, aDOT 12.9) | 2 B.Strange 35, 17.9% (5.0/g, aDOT 7.9, top-3 all 7 games) | 3 J.Meyers 31, 15.9% (4.4/g, aDOT 10.5; Q). Then BTJ 21 (10.8%), Tuten 16 (8.2%, 9 screens).

## L4 Route areas (L4_route_proxy.csv; pbp pass_location x air_yards PROXY — NGS route trees UNAVAILABLE)
- Washington: left-heavy (31 of 48 left), left int 15, left deep 10; PFF align Wide 179/Slot 145.
- Strange: middle int5-14 9, spread short both sides; PFF Inline 171/Slot 80/Wide 39.
- Meyers: left int 8, middle int 7, deep middle 3; Wide 229/Slot 102.
- BTJ: outside only, right deep 5/int 5, left deep 3; Wide 148/Slot 45.
- Tuten: behind LOS both sides (13 of 16), 9 screens. Rodriguez 3 tgt, Allen 6 (short middle/right) — too few.

## L5 Who covers (free PFF, ../pff_jax_bal/; injury: Hawkins OUT, Wiggins Q)
- Wiggins (wide CB 431 snaps): 21 rec, 10.6 YPR, rating 103.3. Humphrey (wide 382): 23 rec, 15.8 YPR, 92.3. Hamilton (Box 178/Slot 162): 22 rec, 8.3 YPR, 91.7 — but Hamilton test (bal_def_snapshot/hamilton_test.md) found slot/TE opponents beat norms 11 of 18 -> treat PFF slot strength as not real. LB/S allowed stats beyond these: UNAVAILABLE free. Hawkins replacement: UNAVAILABLE.
- PFF matchup tool: Washington vs Wiggins/Humphrey 7.5 snaps each, Hamilton 13.5 (slot); Meyers vs CBs 11.2 each; BTJ vs CBs 10.6; Strange mostly safety 11.5 / LB 7.9. If Wiggins sits, the backup outside CB is UNAVAILABLE.
- Left side for Washington: BAL allows left int 8.2 YPT / left deep 10.2 to WRs.

## L6 Shell and leaks (L6_bal_allowed_by_pos_area.csv, ../bal_def_snapshot/zone_allowed.csv)
- MOFO/MOFC, man/zone: UNAVAILABLE (participation corrupt; no free public source fetched).
- Leaks to WRs: deep middle 19.8 YPT (13 tgt), deep right 15.7, middle int 11.5. Short middle shut down (1.6 YPT WR, 2.9 TE).
- TE in middle: only 15 tgt, 62 yds — TE middle is NOT a leak in pbp. TEs hurt BAL on the right short/int (16 tgt, 171 yds, 10.7 YPT). This contradicts the earlier "TE up the seam" read.
- RBs: 46 tgt, 142 yds, all short — RB receiving is suppressed.

## Ranked hypotheses (not picks)
1. Washington receptions/yards UP: #1 target, top target vs blitz and pressure, left int/deep where BAL allows 8-10 YPT, extra JAX volume.
2. Meyers yards (if active): middle int/deep middle = BAL's worst area (11.5/19.8 YPT); #2 target under pressure.
3. Strange yards: steady 5 tgt, but his middle-short work hits BAL's best area; right-side TE leak helps. Neutral-to-slight up.
4. BTJ: only outside deep looks, 3 tgt/g; deep right leak 15.7 YPT but volume low — longest-play type angle only.
5. RB receiving (Tuten/Allen) DOWN: BAL holds RB targets to 3.1 YPT.
6. JAX rush volume UP in a lead script; Rodriguez only if Tuten out (see jax_usage).
