```
GATE: PASS  run=/workspace/nfl-database/runs/2026-11-01_FD7_REPLACEMENTS  checked_at=2026-11-01 07:46 ET
Live legs: ['Jahan Dotson Rec Yds Under 25.5', 'Jordan Addison Receptions Under 3.5', 'Puka Nacua Receptions Over 7.5', 'Stefon Diggs Rec Yds Over 42.5', 'Stefon Diggs Receptions Over 3.5', 'Tre Tucker Receptions Over 3.5', 'Xavier Worthy Rec Yds Over 29.5']
Cut legs: ['Rashee Rice Receptions Over 3.5', 'Rashee Rice Receptions Over 4.5', 'Rashee Rice Receptions Over 5.5', 'Stefon Diggs Receptions Over 4.5', 'Xavier Worthy Receptions Over 3.5']
APPROVED EXCEPTIONS:
  - leg Jahan Dotson Rec Yds Under 25.5 defender Zyon McCollum: coverage.defenders from /workspace/nfl-sim/mnf12/pfr_def_adv_2026.html (staleness waived; approved by Rico on 2026-11-01, valid 2026-11-01, scope receiving legs) — misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only
  - leg Jordan Addison Receptions Under 3.5 defender D.J. Reed: coverage.defenders from /workspace/nfl-sim/mnf12/pfr_def_adv_2026.html (staleness waived; approved by Rico on 2026-11-01, valid 2026-11-01, scope receiving legs) — misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only
  - leg Puka Nacua Receptions Over 7.5 defender Donte Jackson: coverage.defenders from /workspace/nfl-sim/mnf12/pfr_def_adv_2026.html (staleness waived; approved by Rico on 2026-11-01, valid 2026-11-01, scope receiving legs) — misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only
  - leg Stefon Diggs Rec Yds Over 42.5 defender Cooper DeJean: coverage.defenders from /workspace/nfl-sim/mnf12/pfr_def_adv_2026.html (staleness waived; approved by Rico on 2026-11-01, valid 2026-11-01, scope receiving legs) — misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only
  - leg Stefon Diggs Receptions Over 3.5 defender Cooper DeJean: coverage.defenders from /workspace/nfl-sim/mnf12/pfr_def_adv_2026.html (staleness waived; approved by Rico on 2026-11-01, valid 2026-11-01, scope receiving legs) — misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only
  - leg Tre Tucker Receptions Over 3.5 defender Azareye'h Thomas: coverage.defenders from /workspace/nfl-sim/mnf12/pfr_def_adv_2026.html (staleness waived; approved by Rico on 2026-11-01, valid 2026-11-01, scope receiving legs) — misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only
  - leg Xavier Worthy Rec Yds Over 29.5 defender Riley Moss: coverage.defenders from /workspace/nfl-sim/mnf12/pfr_def_adv_2026.html (staleness waived; approved by Rico on 2026-11-01, valid 2026-11-01, scope receiving legs) — misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only
Notes:
  - Jahan Dotson Rec Yds Under 25.5: avg p 0.595, no-vig 0.500, edge +9.5, shrunk +6.7
  - Jordan Addison Receptions Under 3.5: avg p 0.689, no-vig 0.575, edge +11.4, shrunk +5.7
  - Puka Nacua Receptions Over 7.5: avg p 0.593, no-vig 0.542, edge +5.1, shrunk +2.3
  - Stefon Diggs Rec Yds Over 42.5: avg p 0.586, no-vig 0.500, edge +8.6, shrunk +6.0
  - Stefon Diggs Receptions Over 3.5: avg p 0.649, no-vig 0.583, edge +6.7, shrunk +2.2
  - Tre Tucker Receptions Over 3.5: avg p 0.591, no-vig 0.510, edge +8.0, shrunk +5.3
  - Xavier Worthy Rec Yds Over 29.5: avg p 0.580, no-vig 0.500, edge +8.0, shrunk +5.6
```

# FD 7-leg (+694) TD-slot replacements — game-script run (Sunday Nov 1, 2026)

**For Ghost6 vetting only — not for Rico until VETTED.**

## 1. Header
- Ticket: /workspace/nfl-database/week8/slips/slips_2026-11-01.md (FD_7leg_694.png). Kept legs: Higgins 4+ rec, Bowers 50+ yds, Flowers 60+ yds, P. Washington 40+ yds, Lamb 50+ yds.
- Candidates are legs that passed all 15 phases in their game folders (2026-11-01_<game>/checklist.md); odds FanDuel 07:30 ET via The Odds API (stale 08:30 ET). Checklist: /workspace/nfl-database/runs/2026-11-01_FD7_REPLACEMENTS/checklist.md

## 2. Phases run
- All 15 phases PASS for all 6 candidates (rows copied from game checklists).

## 3. Sources used, by category
- Same as the game folders (union in run_manifest.json): nflverse pbp/snaps, ESPN, PFR cache (Rico exception), Sharp coverage schemes, FTN charting, nflverse NGS BACKUP, official NFL YouTube film, ESPN injuries, NWS/Open-Meteo, FanDuel/Pinnacle/DK/PrizePicks via The Odds API, PFF props cross-check.

## 4. Simulations
- Monte Carlo, Bias and Game Randomness, 100,000 sims each, seed 20261101, /workspace/nfl-database/runs/2026-11-01_shared_src/sim_v5.py. Edge decision on MC+GR average (bias excluded pending fix).

## 5. Projections and picks
### Slot 1 — replaces Kyren/Corum anytime TD (-280); needs -280 or longer
1. Xavier Worthy Rec Yds Over 29.5 @ -113 (FD main, line 29.5): no-vig 0.500; MC p 0.618/med 37.32, GR p 0.588/med 36.08, Bias p 0.534/med 30.73 (recorded, excluded); MC+GR edge +10.3, shrunk +7.2. Correlation: KC@DEN: no game/team overlap with Higgins (CIN), Bowers (LV), Flowers (BAL), P. Washington (JAX), Lamb (DAL); none of the excluded players
2. Jahan Dotson Rec Yds Under 25.5 @ -113 (FD main, line 25.5): no-vig 0.500; MC p 0.573/med 22.49, GR p 0.576/med 22.49, Bias p 0.636/med 19.36 (recorded, excluded); MC+GR edge +7.4, shrunk +5.2. Correlation: ATL@TB: no overlap; an under, mildly negatively tied to nothing on the ticket
3. Jordan Addison Receptions Under 3.5 @ -160 (FD main, line 3.5): no-vig 0.575; MC p 0.670/med 3.0, GR p 0.668/med 2.0, Bias p 0.729/med 2.0 (recorded, excluded); MC+GR edge +9.4, shrunk +4.3. Correlation: MIN@DET: no overlap with the five legs; price -160 only eligible for Slot 1

### Slot 2 — replaces Walker anytime TD (-140); needs -140 or longer
1. Stefon Diggs Rec Yds Over 42.5 @ -113 (FD main, line 42.5): no-vig 0.500; MC p 0.631/med 52.35, GR p 0.618/med 51.04, Bias p 0.509/med 43.51 (recorded, excluded); MC+GR edge +12.4, shrunk +8.7. Correlation: PHI@WSH: no overlap with the five legs; not an excluded player
2. Jahan Dotson Rec Yds Under 25.5 @ -113 (FD main, line 25.5): no-vig 0.500; MC p 0.573/med 22.49, GR p 0.576/med 22.49, Bias p 0.636/med 19.36 (recorded, excluded); MC+GR edge +7.4, shrunk +5.2. Correlation: ATL@TB: no overlap; an under, mildly negatively tied to nothing on the ticket
3. Puka Nacua Receptions Over 7.5 @ -138 (FD main, line 7.5): no-vig 0.542; MC p 0.622/med 9.0, GR p 0.626/med 9.0, Bias p 0.531/med 8.0 (recorded, excluded); MC+GR edge +8.2, shrunk +4.5. Correlation: LAC@LAR: no overlap with the five legs (the replaced Kyren/Corum TD was LAR); CAUTION same-player stack with Rico UD Puka o69.5 rec yds; Donte Jackson Q

- Recommended pair (matches Ghost6): Worthy 30+ (Slot 1) + Diggs 43+ (Slot 2). Dotson appears in both lists; use him in only one.
- Backup: Tre Tucker Receptions Over 3.5 @ -120 (FD main, line 3.5): no-vig 0.510; MC p 0.636/med 4.0, GR p 0.592/med 4.0, Bias p 0.544/med 4.0 (recorded, excluded); MC+GR edge +10.4, shrunk +7.0. Correlation: LV@NYJ: SAME TEAM as Bowers 50+ (LV passing volume shared) - CORRELATED, backup only
- Placed status of the FD 7-leg is still UNCONFIRMED.

### Cut legs
- None of the six candidates cut. Not considered: excluded players (Lamb, Bowers, Walker, St. Brown, Flowers, Higgins), TD markets, and every game-folder leg that is CUT.

## 6. Risks and checks still to come
- Approved exception: per-defender numbers from pfr_def_adv_2026.html (Oct 29 06:02 ET cache), Rico, Nov 1 receiving legs only.
- NGS from nflverse published copy (BACKUP, data through 2026-10-29 (2026 Week 8 TNF)), accepted by Ghost6 for Nov 1 only.
- Bias model excluded pending fix (BUGLOG BUG-2026-11-01-BIAS); gate still checks all three models.
- PFF props cross-check (pick side only, book unknown): Worthy O29.5 agrees; Dotson U25.5 agrees; Tucker: PFF picks rec yds UNDER 48.5 (soft conflict); no PFF rows for Diggs, Puka, Addison.
- Odds from 07:30 ET go stale 08:30 ET; reprice before any later decision. Inactives 11:30 AM ET (Puka: Donte Jackson Q).
- Pressure is PROXY; Sharp schemes data through Oct 27.

## 07:50 ET ADD-ON — FD7 TD slots as RECEPTIONS (Rico via Ghost6; for Ghost6 only, not VETTED)
Odds re-pulled 07:44 ET (The Odds API, FanDuel price of record + Pinnacle; odds_r0750.csv); stale 08:44 ET. Same seed 20261101, 100,000 sims x 3 models (rec_r0750.py on sim_v5.py). Gate edge = 3-model average; MC+GR shown alongside because bias is broken (BUG-2026-11-01-BIAS).

Rashee Rice status: ACTIVE, no injury designation. Hamstring injured in Q1 of Wk4 at LV, missed Wk5-7 (KCTV5 2026-10-16; Yahoo); Reid said he will play Wk8 (NBC Sports 2026-10-30; ESPN injuries API 07:44 ET citing Chiefs.com Matt McMullen 2026-10-30 18:15Z).

| Leg | FD price | no-vig | p MC/Bias/GR | medians | gate edge/shrunk | MC+GR edge/shrunk | PFF | Status |
|---|---|---|---|---|---|---|---|---|
| Rice O4.5 (5+) | -106 | .481 | .353/.292/.338 | 3/3/3 | -15.3/-10.1 | -13.5/-8.9 | rec yds UNDER 51.5 (proj 39.5) | CUT P2, P14 |
| Rice O5.5 (6+) | +182 | .331 | .240/.193/.268 | 3/3/3 | -9.8/-1.8 | -7.7/-0.4 | same | CUT P2, P14 |
| Rice O3.5 (4+) | -230 | .651 | .496/.425/.423 | 3/3/3 | -20.3/-18.8 | -19.2/-18.0 | same | CUT P2, P14 |
| Worthy O3.5 (4+) | +116 | .433 | .356/.290/.353 | 3/2/3 | -10.0/-5.0 | -7.9/-3.5 | rec yds OVER 29.5 | CUT P2, P14 |
| Diggs O3.5 (4+) | -166 | .583 | .682/.595/.671 | 4/4/4 | +6.7/+2.2 | +9.4/+4.1 | no row; ~5.6 tgt | PASS (Slot A only) |
| Diggs O4.5 (5+) | +130 | .406 | .500/.404/.494 | 4/4/4 | +6.0/+7.1 | +9.1/+9.2 | no row | CUT P14 (median 4 < 4.5, bias p .404) |
| Tucker O3.5 | -120 | .510 | .636/.544/.592 | 4/4/4 | +8.0/+5.3 | +10.4/+7.0 | rec yds UNDER 48.5 | PASS, but LV = Bowers correlation (excluded game) |
| Puka O7.5 | -138 | .542 | .622/.531/.626 | 9/8/9 | +5.1/+2.3 | +8.2/+4.5 | no rec row | PASS (stacks UD Puka o69.5) |
| Addison U3.5 | -160 | .575 | .670/.729/.668 | 3/2/2 | +11.4/+5.7 | +9.4/+4.3 | no row | PASS (Slot A only) |

Slot A (-280 or longer): 1) Addison U3.5 -160 (gate +11.4; MC+GR +9.4); 2) Diggs 4+ -166 (gate +6.7; MC+GR +9.4). Puka O7.5 also eligible.
Slot B (-140 or longer): 1) Puka O7.5 -138 (gate +5.1; MC+GR +8.2). No second clean leg: Tucker O3.5 -120 (gate +8.0) is in the excluded LV game (Bowers). Diggs 5+ fails the median/p floor.

## Risks (07:50 add-on)
- Approved exception still applies: per-defender numbers from pfr_def_adv_2026.html (Rico, Nov 1 receiving legs).
- Rice/Worthy sims use a Rice-active split (KC wk1-3 only, n=3, LOW-SAMPLE); KC pass attempts in those games were 29/49/24, so volume may be understated. Rice median 3 vs market 4.5 is MODEL-SUSPECT territory; the cut also stands on the Phase 2 catches-over rule (Rice had 5+ targets in only 2 of 3 games).
- Bias model broken; gate still averages it. Unders read rich (Addison), overs read low (Diggs, Puka, Tucker).
- Diggs 4+ margin is thin: projected 4.0-4.7 rec; PFF's ~5.6 targets x .61 = ~3.4.
- Odds 07:44 ET; reprice after 08:44 ET and at inactives.
