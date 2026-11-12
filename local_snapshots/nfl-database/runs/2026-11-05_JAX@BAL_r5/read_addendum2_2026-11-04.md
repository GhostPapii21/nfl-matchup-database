# Read addendum 2, 2026-11-04 (pre-kick; counts as a locked read). BAL D snapshot mapped onto JAX as HYPOTHESES.
Input: week10/bal_def_snapshot/snapshot.md (Ghost6, brainstorm Step 4b). Locked read 76b563a3 and addendum 1 (4c6f0999) are untouched.

## Data sources
- **Alignment: still ball-location only (FLAG).**
  - I tried to re-download nflverse participation from the public release. https://github.com/nflverse/nflverse-data/releases/download/pbp_participation/pbp_participation_2026.parquet returns 404. The release lists no 2026 asset (newest is 2025), so there's nothing to checksum.
  - Every "side" below comes from pbp pass_location (where the ball went), not where the receiver lined up. offense_formation and route are unavailable.
- **Hawkins (S, BAL): PENDING.**
  - The official NFL Week 9 report (nfl.com/injuries, Tuesday) lists him DNP with a knee injury and no game status yet. Russell Street Report has the Ravens PR Tuesday report: DNP (knee). He was inactive at BUF.
  - The snapshot's "OUT" is an ESPN label, not the official designation.
  - Caution: the baltimoreravens.com injury-report page currently shows an older week's table, so I did not use it.
- **JAX injuries (official, Tuesday):** Tuten RB DNP (ankle/foot), Rodriguez RB limited, Meyers WR limited.

## Hypotheses vs data
| hypothesis | data (nflverse pbp Wk1-8, last 4 = CIN, PHI, HOU, IND) | verdict |
|---|---|---|
| BTJ is the outside WR1 who goes off | **BTJ is not JAX's WR1.** 22 targets in 7 games; last 4: 3-2-17, 3-0-0, 2-0-0, 2-1-12. aDOT 12.2. The market agrees (rec yds 10.5 FD/Pin, 11.5 DK). **Parker Washington fits the WR1 pattern:** 48 targets, aDOT 12.9, 29 of 48 to the offense's left (Humphrey's side), 11 targets at 10-20 air yards outside | REFUTED for BTJ. The pattern points to Washington |
| Strange on the seam (deep middle 18.4 ypt; Hawkins out) vs PFF CAUTION (BAL top 5 vs TE) | Strange: aDOT 7.9, **0 deep-middle 15+ targets**, 7 middle targets at 10+, 7.6 yds per middle target. Last 4 rec yds 95/68/44/55 | PARTIAL. His volume fits (overs pass §3), but he isn't a seam/deep player, so the deep-middle leak doesn't map onto him. PFF CAUTION is a cross-check flag only. Resolution: the overs ride his volume, not the seam story, and the data can't settle BAL-vs-TE |
| Washington vs Hamilton in the slot -> Washington under | Washington lines up mostly outside per PFF free (wide 179 / slot 145) and draws left-side targets, which is Humphrey, not Hamilton. Without alignment data I can't put him on Hamilton | **CONFLICT.** The snapshot's own WR1 pattern argues for Washington volume, against the under. The under rests on his §3 3/4 receptions record, not this matchup |
| JAX run game vs 3.6+ YPC allowed (Lawrence / Etienne rush) | **Etienne has no 2026 JAX carries in pbp.** The JAX RBs are Tuten (DNP Tue) and Rodriguez. Lead backs got 5+ YPC vs BAL. No JAX RB rush props are in the odds file (NO_QUOTE). Lawrence rush U12.5 is a QB leg, so RB YPC allowed doesn't bear on it | No conflict with the locked read (the slip story is "JAX controls"). The Etienne premise is wrong. Any JAX RB leg is NO_QUOTE and waits on Tuten's status |

## Legs built from addendum 2 (normal checks)
| leg | best price | §3-of-4 | last-2 | anchored | tier | flags |
|---|---|---|---|---|---|---|
| BTJ rec yds o10.5 | FD/Pin -114 (DK o11.5 -110) | FAIL 2/4 [17,0,0,12] | DOWNGRADE | n/a (not in sim set) | CUT | hypothesis refuted; former +7 (depth WR) |
| BTJ rec u1.5 | DK -195 | PASS 3/4 [2,0,0,1] | OK | n/a | CUT (no model edge) | opposite of the hypothesis |
| BTJ longest reception | NO_QUOTE (market not in file; no credits spent) | - | - | - | CUT | - |
| Strange rec yds o35.5 | FD -114 | PASS 4/4 | OK | -0.23 | CUT | off-read; PFF CAUTION; seam story not supported |
| Washington rec u4.5 | DK -125 | PASS 3/4 [1,6,4,1] | OK | -0.17 | CUT | off-read; matchup CONFLICT (WR1 pattern) |
| Lawrence rush U12.5 | FD/Pin -114 | PASS 3/4 (any-QB window, Rico's call) | OK | -0.05 | CUT | on the locked read; snapshot doesn't conflict |
None of these clears +1, so none plays under the tiers.
