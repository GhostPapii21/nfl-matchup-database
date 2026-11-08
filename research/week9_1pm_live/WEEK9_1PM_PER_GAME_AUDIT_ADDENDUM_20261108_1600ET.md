# Week 9 1 PM game audit addendum — current board snapshot

**Captured:** 2026-11-08 16:00:22 ET / 21:00:22 UTC.  
**Purpose:** record the user's per-game review fields in downloadable tables and refresh live quarter status. This is a snapshot addendum to the initial 15:52 ET audit, not a replacement for the earlier timestamped source capture.

## Current score and quarter state

The DraftKings Scores connector returned one final game and six live games at this capture. Q4 scores shown for live games are partial. The full quarter-by-quarter score record, current score, clock, and source request ID are in [WEEK9_1PM_QUARTER_SCORES_20261108_1600ET.csv](../WEEK9_1PM_QUARTER_SCORES_20261108_1600ET.csv).

| Game | Current score | Q1 margin | Q2 margin | Q3 margin | Q4 margin at capture | State |
|---|---:|---:|---:|---:|---:|---|
| CLE–NO | CLE 13–9 | NO +3 | CLE +3 | Tie | CLE +4 partial | Live, 2:00 |
| DAL–IND | DAL 20–17 | IND +4 | DAL +14 | IND +7 | Tie partial | Live, 9:54 |
| DEN–CAR | DEN 26–14 | DEN +10 | CAR +4 | CAR +7 | DEN +13 partial | Live, 3:58 |
| DET–MIA | DET 19–9 final | Tie | DET +3 | DET +7 | Tie | Final |
| NYG–PHI | NYG 16–8 | PHI +2 | Tie | NYG +7 | NYG +3 partial | Live, 5:04 |
| NYJ–KC | KC 28–12 | NYJ +6 | KC +8 | KC +14 | Tie partial | Live, 5:17 |
| LAR–WAS | LAR 20–13 | Tie | WAS +4 | LAR +4 | LAR +7 partial | Live, 6:32 |

Quarter margin means the points scored in that quarter minus the opponent's points in that quarter. It is not the running game spread. For completed-game quarter winners/spreads, only DET–MIA can be finalized from this snapshot; the other six need a final capture.

## Receiver results against pregame history

A row-level CSV now records each available target/reception/yards line, rushing role where applicable, 20+ yard explosive count/yards, baseline and difference, the underlying PBP URL, and limitations. See [WEEK9_1PM_RECEIVER_USAGE_20261108_1552ET.csv](../WEEK9_1PM_RECEIVER_USAGE_20261108_1552ET.csv). Values remain the earlier CBS box/PBP snapshot; CBS was behind the live score feed in four games, so do not combine these rows with the 16:00 current scores as if they were synchronized.

## Defense and explosive-play read by game

Explosive threshold: **20+ yards on one scrimmage play**. The event-level CSV remains the event source. Its current 14-play provisional set summarizes as follows:

| Defense | Explosives allowed in captured set | Offensive positions / player examples | What this can support now |
|---|---:|---|---|
| NO | 1 / 60 yards | WR Denzel Boston, 60 | A WR produced a long explosive; individual cover attribution unknown |
| IND | 3 / 89 yards | WRs Jonathan Mingo 23, CeeDee Lamb 22 and 44 | Three WR explosive gains in one game; repeated WR production signal, one game only |
| DEN | 3 / 64 yards | WR Tetairoa McMillan 20; RB Chuba Hubbard 23 rush; TE Darren Waller 21 | Explosives came from three position groups; inspect TE/RB exposure separately |
| DET | 2 / 66 yards | WR Caleb Douglas 20; RB Keaton Allen 46 receiving | Miami WR and RB both produced explosives |
| MIA | 1 / 31 yards | WR Jameson Williams 31 | Detroit WR explosive |
| NYG | 1 / 20 yards | WR Darius Cooper 20 | One PHI WR explosive; TE Isaiah Likely led PHI receiving yardage in captured box snapshot |
| NYJ | 1 / 25 yards | RB Kenneth Walker III 25 receiving TD | RB receiving explosive |
| LAR | 1 / 45 yards | RB Rachaad White 45 PBP gain (41 box yards) | RB receiving explosive; source stat discrepancy retained |
| WAS | 1 / 21 yards | WR Puka Nacua 21 | WR explosive; Puka's volume/yardage also exceeded L5 baseline in captured box |

These totals answer which **team defense** allowed the play and which offensive player/position produced. They do not establish who individually “gave up” the yards. PBP contact/tackle names are retained separately in the event ledger; they are not coverage assignments. No individual defender allowed-yards or receptions figure is asserted without charted assignment evidence.

## Per-game diagnostic fields already captured

The per-game audit records QB line, team yards, third-down conversions/attempts, red-zone trips/results, available sack totals, receiving opportunity versus Week 1–8 L5 baseline, and quarter score/margin. The player-level comparison is now also downloadable in the receiver usage CSV.

## Open data needed to finish the matchup cause

- Man/zone and middle-open/middle-closed rates with snap denominators.
- Blitz and pressure rates, pressure timing at the QB's decision point, and pressure outcome.
- Verified route participation/route tree and target-per-route.
- Defensively charted assignment (including shared zone responsibilities) for each explosive and target; video review must log the clip/timecode and confidence, not infer assignment from a tackle.
- Final score and complete Q4 PBP/stat refresh for the six live games at this timestamp.
- After finals: compare the frozen player/market projections with observed usage and results; classify misses as opportunity, QB/pressure, receiver conversion, matchup, role, game script, or data-source/timing.

Coverage shells, pressure/blitz rates, and individual allowed stats are not estimated or backfilled from standard PBP. Calibration and production-readiness flags remain false.
