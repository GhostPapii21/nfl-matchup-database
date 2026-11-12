# JAX offensive usage, 2026 Wks 1-8 (bye Wk7) — brainstorm input for JAX@BAL TNF Nov 5
Read-only. Sources: nflverse pbp_2026 + snap_counts_2026 (sources/nflverse/), jaguars.com injury report, Jaguars Wire / SI (Nov 3). Script: build.py. CSVs: targets_by_game.csv, targets_season.csv, rush_by_game.csv, rb_snaps.csv. Hypotheses, not picks.

## Context
- QB: Lawrence started all 7. Wk8 was a 42-7 blowout of IND; Ewers took the last 10 snaps (3 dropbacks). Every Wk8 volume number is low because of garbage time (only 17 targets).
- No Etienne on the 2026 roster. The RB room is Tuten, C. Rodriguez Jr., LeQuint Allen and Abdullah.

## (1) Targets: top 3 each game (tgt-rec-yds, air yards, share)
| Wk | #1 | #2 | #3 |
|---|---|---|---|
|1 CLE|P.Washington 6-5-83, 102 air, 29%|Strange 3-2-23|B.Thomas 3-3-40|
|2 @DEN|P.Washington 12-7-98, 177, 43%|B.Thomas 8-3-40, 82|Strange 2-2-17|
|3 NE|Meyers 8-7-64, 30%|Strange 5-3-32|P.Washington 5-3-40|
|4 @CIN|Strange 8-7-95, 35%|Meyers 4-3-33|P.Washington 3-1-7|
|5 PHI|P.Washington 9-6-124, 24%|Strange 8-7-68|Cameron 6-3-43|
|6 HOU|P.Washington 11-4-64, 153 air, 27%|Meyers 10-5-83, 117|Strange 7-5-44|
|8 IND|Meyers 3-2-24|Strange 2-2-55|Tuten 2-2-55 (B.Thomas also 2)|

Season totals (share / tgt per game / aDOT / top1-top2-top3 finishes in 7 games):
- **P. Washington is the WR1: 48 tgt, 24.6%, 6.9/g, aDOT 12.9, 27-432. Finished 4-4-6.** He's the downfield volume guy, not a short slot guy.
- **Strange is the most stable: 35 tgt, 17.9%, 5.0/g, aDOT 7.9, 28-334. Top 3 in all 7 games (1-5-7).**
- **Meyers: 31 tgt, 15.9%, 4.4/g, aDOT 10.5. Finished 2-4-4.** He's LP Mon/Tue with a hamstring/ankle.
- **Brian Thomas Jr. is NOT a target earner: 21 tgt, 10.8%, 3.0/g, 10-117, finished 0-1-2.** His snap share is only 21-62%.
- Tuten has 16 tgt (2.3/g, 15-181, short throws). Cameron has 13 and Boerkircher 9.
- Snap shares (Wks 2-6): Meyers, Washington and Strange about 75-90%. Thomas 21-62%.

## (2) Rushing
| Wk | Tuten car-yds (YPC), carry share, snap% | Rodriguez | Allen / Abdullah |
|---|---|---|---|
|1|15-66 (4.4), 47%, 49%|6-23, 40% snaps|Abd 4-32|
|2|13-65 (5.0), 54%, 51%|6-13, 22%|Abd 3-11|
|3|15-73 (4.9), 50%, 48%|8-37, 21%|Abd 3-2|
|4|17-73 (4.3), 63%, 59%|6-35, 25%|-|
|5|22-72 (3.3), 82%, 68%|2-5, 12%|-|
|6|12-39 (3.3), 44%, 58%|**11-55 (5.0), 41%, 30%**|Allen 1-1|
|8|16-104 (6.5), 49%, 50%|6-41, 22%|Abd 6-13|
- Tuten: 110-492, 4.47 YPC, 15.7 car/g, about 56% carry share, about 55% snaps.
- **Rodriguez is the RB2 / next man up: 45-209, 4.64 YPC, 6.4 car/g, 22-30% snaps. His career-high workload this year was Wk6 HOU, 11-55.** He also has a 3-TD goal-line role.
- RB3: Allen (6-18% snaps, the receiving back, about 1 carry all year) and Abdullah (16-58 on 3.6 YPC, mostly garbage time).
- **Status (jaguars.com, as of Tue): Tuten (ankle/foot) DNP Mon and DNP Tue.** Game status is "unspecified" until the Wed report. "Questionable" is media framing, not official yet. **Rodriguez is himself LP (hand).**
- **HYPOTHESIS, if Tuten is out:** Rodriguez gets 13-17 carries for about 50-75 yds (center about 60, at 3.8-4.6 YPC vs a BAL D that held committee or non-elite backs to 2.4-3.8). Allen picks up passing-down snaps and Abdullah about 4-6 carries. **If Tuten plays limited:** a split around Tuten 10-12 / CRod 8-10. Script risk: a big JAX lead adds late CRod and Abdullah carries.

## (3) Fit vs BAL leaks (bal_def_snapshot)
- Outside WR1 at 10-20 aDOT (Humphrey's side): **P. Washington** fits (12.9 aDOT, 618 air yards, team-high). Thomas has the profile but not the volume.
- TE seam / intermediate middle: **Strange** fits, but his aDOT is 7.9, so he gets more short/underneath work than seam work. The deep-middle leak suits Washington and Meyers more.
- Short middle is shut down (2.5 yds/tgt): this hurts Strange's underneath work and RB checkdowns (Tuten/Allen).
- Note: Washington isn't primarily the slot guy Hamilton would be covering. The "Hamilton in the slot" logic behind Washington's catches under is weaker than assumed, because Washington is the team's WR1.

## (4) Conflicts with the current card
- **P. Washington rec u4.5: CONFLICT.** He's the clear WR1 (6.9 tgt/g, top 3 in 6 of 7). His receptions go 5,7,3,1,6,4,1, so 4 of 7 under. The Wk8 1 is a blowout artifact. The fit with the BAL leak points the other way. Revisit.
- **Strange rec yds o35.5: SUPPORTED by volume.** He's top 3 every game and went 95/68/44/55 in the last 4 (4/4). The leak (TE seam) supports it. The risk is that his aDOT is short into a locked short middle, and PFF has BAL top 5 vs TEs.
- **Lawrence rush u12.5: no conflict.** Per game: 3,6,25,0,25,11,10, so 5 of 7 under. The two 25s were scramble games (3 scrambles in Wk5).
- **BAL TT under: no conflict.** It's a JAX-offense-independent leg. A Tuten absence is mild for JAX game control, not for BAL scoring.
- New angle: a Rodriguez rush prop if Tuten is ruled out. Tuten's own props are void or risky.
