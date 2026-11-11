# BAL secondary vs JAX pass game — TNF JAX@BAL, Thu Nov 5 2026
Built Wed Nov 4 ~07:15 ET. Scripts: build_explosives.py, build_defenders.py (this folder). Projection: branch scenario-projector-2026-11-04 @62c8acc; drivers: branch driver-ledger-2026-11-04 @d314606.

## Data and sources
- nflverse play_by_play_2026 (re-downloaded 2026-11-04 07:00 ET). It has every BAL game through BAL@BUF on Nov 1. nflverse labels that game week 8; BAL has played 8 games, so these are the calendar Weeks 1-9 games.
- FTN charting through nflverse: blitz and rusher counts only.
- PFR 2026 advanced defense (public, fetched 2026-11-04): coverage targets, completions, yards, TDs and rating allowed per defender.
- Free PFF pages already saved in ../pff_jax_bal: alignment and matchup-tool snap projections.
- Injury reports: baltimoreravens.com and jaguars.com (Mon/Tue), russellstreetreport.com (Ravens PR, Nov 3), and baltimoreravens.com Ryan Mink (Nov 3).
- **Not available:**
  - Coverage shell (MOFO/MOFC) and man/zone. The nflverse participation file for 2026 is still "Not Found" upstream.
  - Per-play coverage defender. PFR, nflverse and FTN don't publish it free, so every explosive play is marked **unattributed** in coverage. The ball-carrier tackler is listed as a proxy only.
  - Receiver alignment per play (FTN free has none). I used season PFF alignment shares instead.
  - NGS time-to-throw. NGS route charts exist only as 3 images in ../ngs.

## 1. Explosive-play map (explosives_bal_wk1_9.csv, 24 passes of 20+ and 14 rushes of 10+)
| | BAL per game | League per defense-game | Rank |
|---|---|---|---|
| Completions of 20+ | 3.00 (89.9 yds) | 2.89 (87.8 yds) | 13th most |
| Non-QB runs of 10+ | 1.75 | 2.29 | 25th (better than average) |

**What this means:** BAL is about league-average on explosive passes overall. The leak is concentrated, not broad.

By area (20+ completions per game, BAL vs league):
| Area | BAL | League | Read |
|---|---|---|---|
| **Deep middle** | **0.88** (7 plays, 221 yds, all WRs) | 0.52 | **1.7x league, the main leak** |
| Deep left | 0.75 (6) | 0.71 | about league |
| Deep right | 0.50 (4) | 0.77 | better than league |
| Short right | 0.50 (4: YAC catch-and-runs incl. 2 TE) | 0.16 | small-n leak |

By position:
- WRs: 20 explosive catches, 2.5/g vs league 2.08.
- TEs: 4, 0.5/g vs league 0.56. Two were deep left (Kincaid), two short right (J. Johnson).
- RBs: 0.

Context:
- 16 of 24 came vs no blitz.
- 12 of 24 came in Q4, mostly with the offense trailing or tied (prevent and catch-up). JAX should be leading, which cuts some of that exposure (flag, not a cut).
- Run explosives: 8 of 14 at left tackle.

## 2. Defender table (defender_table.csv; PFR coverage allowed, BAL G=8)
League benchmark (PFR, defenders with 15+ targets): CB 6.96 Y/T, 58.5% completions; S 7.33 Y/T, 59.1%; LB 6.16 Y/T, 68.8%.

| Defender | Pos / role (PFF free alignment) | Def snaps | Tgt | Cmp | Yds | Y/T | TD | Rating | DADOT | 20+ tackled (proxy) |
|---|---|---|---|---|---|---|---|---|---|---|
| **Malaki Starks** | S, starter (alignment not in free pull) | 509 | 20 | 17 (85%) | 244 | **12.2** | **3** | **157.1** | 9.0 | 4 |
| Jaylinn Hawkins (OUT-trend) | S | 315 | 18 | 12 | 188 | 10.4 | 1 | 119.7 | 6.6 | 2 |
| K'Von Wallace (replacement) | S | 66 | 4 | 4 | 70 | 17.5 (**small n**) | 0 | 118.7 | 15.0 | 1 |
| Keondre Jackson (replacement) | S | 34 | 3 | 2 | 32 | 10.7 (**small n**) | 1 | 141.7 | 4.0 | 1 |
| Kyle Hamilton | S, box 178 / slot 162 / FS 69 | 503 | 34 | 24 | 204 | 6.0 | 1 | 83.5 | 4.7 | 4 |
| **Marlon Humphrey** | CB, wide 382 | 410 | 42 | 25 | 359 | **8.5** | 0 | 87.3 | **14.0** | 5 |
| Nate Wiggins | CB, wide 431 | 487 | 36 | 20 | 221 | 6.1 | 1 | 83.2 | 9.5 | 2 |
| Chandler Rivers | CB, nickel early; 0 snaps Wk6-7, inactive at BUF | 104 | 16 | 11 | 132 | 8.3 | 1 | 114.6 | 8.0 | 1 |
| Chidobe Awuzie | CB, 52% at BUF | 128 | 10 | 6 | 52 | 5.2 | 0 | 73.7 | 12.1 | 0 |
| Keyon Martin | CB/nickel, 24-38% recently | 82 | 8 | 7 | 47 | 5.9 | **2** | 130.7 | 3.6 | 1 |
| Roquan Smith | LB | 485 | 29 | 16 | 183 | 6.3 | 0 | 60.0 | 3.0 | 1 |
| Trenton Simpson | LB | 321 | 22 | 14 | 83 | 3.8 | 0 | 51.9 | 2.0 | 0 |

**Leaks:**
1. **Starks**: 12.2 Y/T, 85% completions, 3 TDs. That's 1.7x the league safety Y/T.
2. The Hawkins slot (out) goes to Wallace or K. Jackson. Both have tiny samples, and both allowed 10+ Y/T.
3. **Humphrey**: 8.5 Y/T on deep targets (DADOT 14, 14.4 yards per catch). He gives up the deep ball more than he gives up catches (59.5%).

**Not leaks:**
- Wiggins (6.1 Y/T).
- Hamilton (6.0 Y/T by PFR). Caveat: ../bal_def_snapshot/hamilton_test.md found slot and TE opponents beat their norms 11 of 18, so treat this as unresolved.
- The LBs: Simpson 3.8 and Smith 6.3 Y/T. Short middle is shut down (1.6 Y/T to WRs, from L6).

## 3. Thursday availability (BAL, practice report)
| Player | Mon | Tue | Note |
|---|---|---|---|
| S Jaylinn Hawkins (knee) | DNP | DNP | Hasn't practiced since Oct 21 (Mink, baltimoreravens.com, Nov 3). Inactive at BUF (Hensley on X). **Expect OUT.** |
| CB Nate Wiggins (stinger) | FP | FP | Played 65% at BUF. Expected to play. |
| LB Roquan Smith (foot) | LP | FP | Expected to play. |
| CB Marlon Humphrey | not listed | not listed | Only 56% of snaps at BUF; reason not found (gap). |
| CB Chandler Rivers | not listed | not listed | Inactive at BUF. Role now unclear. |

**Hawkins's replacement:** K'Von Wallace (32% / 57% of snaps the last 2 games), with Keondre Jackson (40% / 15%).
- Small samples: 7 targets, 102 yds, 14.6 Y/T, 1 TD combined, vs Hawkins at 10.4 Y/T.
- So the replacement is **no better, likely worse deep** (small-n flag).
- The Wed Nov 4 official report and Thursday statuses were not yet posted when built. Re-check.

## 4. Matchup grid (alignment from free PFF; routes from L4 pbp location x depth proxy and ../ngs images)
| JAX player | Lines up | Route / target areas | Likely BAL defenders (PFF projected snaps) | What they allow | Leak? |
|---|---|---|---|---|---|
| P. Washington | Wide 179 / Slot 145 | Left-heavy (31 of 48): left int 15, left deep 10, deep middle 3. aDOT 12.9 | Hamilton 13.5 (slot), Wiggins 7.5, Humphrey 7.5. Starks/Wallace over the top | Weighted primary defender Y/T 6.7. BAL WR left deep 10.2 and deep middle 19.8 Y/T | **Deep only**: if he gets Humphrey or the post vs Starks/Wallace. Short and intermediate vs Hamilton/Wiggins is not a leak |
| B. Strange | Inline 171 / Slot 80 / Wide 39 / Backfield 38 | Middle int 9, short both sides | Safeties 11.5 (Starks, Hamilton, Wallace), LBs 7.9 (Smith, Simpson), CBs 6.1 | Safety group 8.9 Y/T (Starks 85% completions); LBs 5.2; TE right short/int leak 10.7 Y/T | **Yes, vs Starks and the Hawkins replacement**. Not vs the LBs |
| J. Meyers (LP hamstring/ankle) | Wide 229 / Slot 102 | Left int 8, middle int 7, deep middle 3 | Hamilton 12.4, Wiggins 11.2, Humphrey 11.2 | Weighted 6.8. Middle int 11.5 and deep middle 19.8 to WRs | Middle/deep middle yes. Volume capped by injury (x0.64) |
| B. Thomas Jr. (active, not on JAX report) | Wide 148 / Slot 45 | Right int 5, right deep 5, left deep 3. aDOT 12.2 | Wiggins 10.6, Humphrey 10.6, Hamilton 8.2 | Weighted 6.9. Deep right 15.7 Y/T, but BAL is below league on deep-right explosives | Only on deep shots vs Humphrey. Low volume, 48% catch rate |
| J. Cameron (6.7% target share, 5 games) | Unknown | Unknown | Unknown | — | Can't map (gap) |

**Which can go off together:**
- Most likely pair: **Washington + Strange**. They attack different defenders. Washington goes outside and deep vs Humphrey and over the top. Strange works the middle and seams vs Starks and Wallace. Both are the top targets vs the blitz.
- Meyers stacks with Strange (both middle) only if healthy.
- BTJ is a one-catch deep-ball type.
- The real "all go off" path is the **deep-middle safety leak**: Washington post, Meyers deep middle, Strange seam. That hits the same weakness and is volume-limited by JAX leading.

## 5. Updated scenario (one link per factor)
Changes:
- **Yards link only.** Defense Y/T is now 0.5 x the area table plus 0.5 x the defender-weighted Y/T: Washington 6.68, Strange 7.42, Meyers 6.84, BTJ 6.94, Cameron 7.0 (**ESTIMATE**).
- Volume, target share and catch links are unchanged.
- Hawkins out is reflected in Strange's safety group (Wallace in for Hawkins).
- BTJ and Cameron are now modeled; other_share is cut from 0.226 to 0.051 to compensate.
- Volume: base 64 plays, flip 62. Lawrence 31.2 attempts base, 26.3 flip.

| Player | Base proj | Flip proj | Line (price saved) | Base P | Flip P | Implied P | Verdict |
|---|---|---|---|---|---|---|---|
| Washington | 8.9 tgt / 5.0 rec / 76 yds | 7.5 / 4.2 / 64 | 4+ rec (−245) | 62% | 53% | 71% | No acceptable price (cut by price only) |
| | | | 5+ rec (−108) | 49% | 39% | 52% | Flag: thin |
| | | | o63.5 yds (−114) | 50% | 42% | 53% | Flag: thin. Was 54% before the defender update |
| Strange | 6.5 / 5.2 / 58 | 5.5 / 4.4 / 49 | 4+ rec (−125) | 64% | 55% | 56% | **Supported** |
| | | | o35.5 yds (−114) | 63% | 55% | 53% | **Supported** |
| | | | 40+ yds (+112) | 59% | 51% | 47% | **Supported, best value** |
| Meyers | 3.4 / 2.4 / 31 | 2.9 / 2.0 / 26 | 3+ rec | 40% | 32% | price not in my files | Over not supported (injury volume) |
| | | | u40.5 yds | 70% | 76% | price not in my files | Supported if priced |
| BTJ | 3.8 / 1.8 / 26 | 3.2 / 1.5 / 22 | 2+ rec / 25+ / 40+ (thresholds, **no line**) | 49% / 40% / 25% | 42% / 34% / 20% | — | No line. Lean no over |
| Cameron | 2.4 / 1.5 / 20 | 2.0 / 1.2 / 17 | 2+ rec / 20+ (thresholds, **no line**) | 40% / 38% | 33% / 33% | — | Below house rule (no defender leak mapped) |
| Lawrence | 31.2 att / 246 yds | 26.3 / 208 | 200+ | 74% | 53% | price not in my files | Supported base, flip is the risk |
| | | | o238.5 | 53% | 31% | — | Flag |

Full table with sources: scenario_out_JAX@BAL_copy.md. The form cross-check is in the branch's week10/scenario_out/JAX@BAL_form.csv.

**Rule outcome:**
- Strange overs are the legs the defender evidence supports most. He's the JAX player whose coverage, Starks and the Hawkins replacement, leaks.
- Washington's case rests on volume, not his coverage matchup. Only the 4+ fails, and it fails on price.
- No hard cuts other than price. Meyers and Tuten statuses are pending; a confirmed inactive would be a hard cut.

## 6. Estimates (labeled)
- Cameron's defender Y/T (7.0).
- Thresholds for BTJ and Cameron.
- The 50/50 area/defender and player/defense blends.
- Safety help over the top is not weighted in the defender Y/T. The PFF matchup tool lists only the primary defender, so the deep-middle leak enters only through the area table.
- Everything flagged ESTIMATE in the scenario estimates list: H2 pass rate, BAL plays, Rodriguez share, dispersion, BAL TT sd.

## 7. Gaps
- No coverage shell or man/zone. Participation file unpublished.
- No per-play coverage defender. All 24 explosives are unattributed in coverage.
- Cameron's alignment and routes.
- Reason for Humphrey's 56% of snaps at BUF.
- Wednesday's official injury report and game statuses (Hawkins, Meyers, Tuten).
- Lines still needed:
  - BTJ rec and yds.
  - Cameron.
  - Meyers prices.
  - Lawrence 200+ price.
  - Washington and Strange re-pull before kickoff.
  - JAX RB lines.
- No Odds API credits were spent.
