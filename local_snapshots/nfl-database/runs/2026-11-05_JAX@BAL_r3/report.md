# JAX @ BAL TNF — r3: Phase 4 PFF matchup update (2026-11-03 ~19:35 ET)
The locked read is unchanged and was not re-locked. The r2 brainstorm_read.md sha256 still matches 76b563a3…5685.
No new Odds API pull: r2 prices (19:15 ET) are under 1h old, and no leg's status moved enough to matter. 0 credits used; 3,575 remain.

## Phase 4: top-2 PFF defenders blended by projected snaps, cross-checked against SRC
SRC = nflverse + FTN position YPT allowed, Wk1–8. PFF counts only alongside this second source. Disagreement is CAUTION; agreement is never a reason to pass a leg.

| receiver | top-2 blend | PFF page | Phase 4 |
|---|---|---|---|
| Zay Flowers | Lewis 12.9 / M. Brown 9.9 snaps → 118.1 rating allowed, 14.9 YPR | 8th, GREAT | Cross-checked (JAX WR 9.72 YPT). **But** Fagnano's rating under pressure is 51.3, and our pbp shows Flowers **did** get 4 Fagnano targets vs BUF (0 catches, 1 INT). Not zero looks. The read still says avoid. |
| Rashod Bateman | M. Brown / Hunter (11.2 each) → 111.0, 17.2 YPR | 47th, FAIR | Cross-checked. Brown allows 155.2 / 20.2 YPR |
| Ja'Kobi Lane | M. Brown / Hunter (9.3 each) → 111.0, 17.2 | 64th, FAIR | Cross-checked |
| Mark Andrews | group level only: S 20th, LB 10th | 25th, FAIR | Cross-checked (JAX TE 4.81 tough vs PFF neutral) |
| Josh Cuevas | group level only: S 20th, CB 16th | 24th, FAIR | Cross-checked |
| Parker Washington | Hamilton 13.5 / Wiggins 7.5 → 95.8, 9.1 | 13th, GOOD | Cross-checked |
| Jakobi Meyers (Q) | Hamilton 12.4 / Wiggins 11.2 → 97.2, 9.4 | 34th, FAIR | Cross-checked; status pending |
| Brian Thomas Jr. | Wiggins / Humphrey (10.6 each) → 97.8, 13.2 | 98th, POOR | CAUTION: PFF page says POOR, the CB blend and SRC say favorable |
| Brenton Strange | group level only: BAL S 3rd, LB 4th, CB 5th | 7th, FAIR | **CAUTION**: PFF says tough, SRC says BAL TE 7.48 YPT (≥ league 7.17) |
| Nate Boerkircher | group level only | 44th, POOR | CAUTION |
| Justice Hill (RB rec) | no PFF RB matchup | — | PFF MISSING → FLAG; SRC: JAX allows 5.73 YPT and 81.8% catch rate to RBs |

Flags only, never cuts: targets/yards/TDs allowed, man/zone, team blitz/pressure (from PFF).

## Injuries
The team-site injury pages (jaguars.com, baltimoreravens.com), pulled 19:30 ET, still show the previous week's final report. **The official TNF report is not posted there yet.**
- **Jakobi Meyers:** official status PENDING. The ESPN feed (21:57Z, 4:57 PM ET) says Questionable (hamstring/ankle), limited participant Tuesday.
- **Jarrian Jones:** official status PENDING. ESPN shows Questionable, dated Nov 2 (carried over from last game).
- **Travon Walker:** official status PENDING. ESPN shows Questionable (ribs) from an in-game note on Nov 1 against the Colts.
- **Status change:** Justice Hill (groin) was a **full participant** Tuesday (ESPN 00:05Z, 7:05 PM ET). That helps his role, but his legs stay at the +7 bar as BAL backup-QB legs and still fail §7. Tuten was DNP Tuesday.

## Gate rerun with today's rules (anchored p, +5/+7, sims flag only)
All 112 prop rungs are cut, and game, half and quarter lines are cut too (edge 0). The best anchored edge is +0.47. Phase 4 only adds or removes CAUTION, so nothing changes. **The card stays NO CARD, same as r2.** Per-leg detail: policy_legs_r3.csv, checklist.md.

## Gaps
- Official TNF injury report pending.
- PFF premium splits pending.
- Man/zone and MOF MISSING.
- PFF files carry no date of their own; I used the file mtime, 2026-11-03 19:23 ET.

---
# r3 addendum: rule-application fix (parent steer 19:31 ET), policy_r3.py
- **Date gate 2026-11-10** (same as 3b3560b): until then, anchored and raw-sim edges only FLAG.
- **Hard checks:** locked read, N1 (hard cut), §7 3-of-4, last-2 (downgrade), depth/role.
- **+7 bar:** applies only to BAL passing and receiving legs.
- **Pricing:** best price shopped across FD, DK and Pinnacle at the same number. CLV open is logged at the best book.
- **PFF:** the 2-defender blend is a FLAG only.
- **Output:** N1 and last-2 are columns in policy_r3_legs.csv. The full table is in gate_table_r3.md.
- **Week label:** the official week is **9** (ESPN week.number=9). Labelled copies are in r3/odds/ with an nfl_week=9 column and meta data_week=9. The "week10" folder name is the mislabel. The r2 files are untouched.
- **§7 for rush legs:** I used the player's own last 4 games with any QB, because rush legs don't depend on the QB. This is my reading of the rule, flagged for Rico/Ghost6. BAL receiving legs still use current-QB games and come out MISSING.

Gate counts: 112 rungs. 2 PASS on the read, 7 PASS off-read (singles only), 8 PASS-DOWNGRADE, 95 CUT.

## Rush-under baseline
| leg | §7 | last-2 | best price | flags |
|---|---|---|---|---|
| Henry rush U69.5 | PASS 3/4 [102, 58, 45, 53] | OK | DK/FD -114 (Pinnacle U70.5 -118 is the better number) | raw +23.5, anchored +0.21 |
| Lawrence rush U12.5 | PASS 3/4 [0, 25, 11, 10] | OK | FD -114 (Pinnacle -114) | raw +13.8, anchored -0.05 |
| J. Hill rush U13.5 | **FAIL 2/4** [3, 73, 7, 15] | DOWNGRADE | -114 | **CUT**: raw +27.8 is a flag only and cannot save it |

## SLIP (one, 3 legs) — "JAX controls, BAL stalls"
1. Henry rush U69.5, -114 at DK or FD (shop to Pinnacle U70.5 -118)
2. Lawrence rush U12.5, -114 at FD
3. BAL team total U14.5, -120 at FD (Pinnacle has U16.5 -143)

Optional 4th leg: JAX -10, -104 at Pinnacle (DK -10 -108; FD -9.5 -120). It is correlated with leg 3.
§11: each player appears once. No TD legs, no passing-yards legs. Read-anchored; none of the edges clear a bar (flag only before Nov 10).

## Singles
- Henry U69.5
- Lawrence U12.5
- BAL TT U14.5
- JAX 1H -6.5, -102 at DK or Pinnacle
- Off-read, singles only: Strange rec yds O35.5 (FD -114; §7 4/4, last-2 OK; Phase 4 CAUTION) and P. Washington rec U4.5 (DK -125; §7 3/4, last-2 OK)
- Not playable: J. Hill rec O2.5 (EDGE2 in the read) is cut on §7 MISSING (1 Fagnano game).
