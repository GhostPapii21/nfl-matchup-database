# Week 8 (2026-11-01) BetGuru postmortem: Gibbs (MIN@DET) and the Ravens' QB collapse (BAL@BUF)
Research only, no picks. Sources: ESPN summary data as stored by Blitz in playlogs/2026_wk8/ (MIN_DET_*, BAL_BUF_*; read-only), ESPN athlete gamelog API (Gibbs id 4429795, season 2026), week8/qb_screen/QB_SCREEN.md. UNVERIFIED = no source on the box or public API checked.

## 1) Jahmyr Gibbs, MIN 15 @ DET 19 (event 401873030)
**Correction to the premise:** ESPN box has Gibbs at **2 rec / 4 targets / 15 yds**, not 1 catch. The prop was O5.5 (Blitz leg grade), so it lost by 4.

**Rico's 4-5 claim (ESPN gamelog):**
| Wk | Opp | Car-Yds | Rec/Tgt |
|---|---|---|---|
| 1 | NO | 29-156 | 5/5 |
| 2 | BUF | 16-52 | 6/8 |
| 3 | NYJ | 20-99 | 7/8 |
| 4 | CAR | 15-46 | 4/7 |
| 5 | ARI | 25-151 | 5/6 |
| 7 | GB | 29-116 | 5/6 |
| 8 | MIN | 23-153 | 2/4 |
Weeks 1-7: 32 rec in 6 games (5.3/g), 4+ every game, 6+ in only 2 of 6. **The claim holds for 4+; a 5.5 line had cleared only 2 of 6 (wk2, wk3)**, and both were higher-pass games (a loss and a shootout). Targets averaged 6.7/g, today 4.

**Why:**
- Volume: DET threw only 25 times (+4 sacks = 29 dropbacks), 43% pass rate, 39 rushes, 35:43 TOP. Gibbs' 4 targets = 16% share, close to normal; the team total collapsed (season ~6-8 RB targets needs ~33+ dropbacks).
- Targets by quarter (PBP): Q1 2 (Q1 7:21 inc, Q1 2:28 inc), Q2 1 (0:32, 2 yds), Q3 1 (13:51, 13 yds), Q4 0. Score: 0-3, 7-6, 7-12, 15-19, a close slog, never a catch-up script.
- Goff target mix: St. Brown 8 (32%), J. Williams 6, LaPorta 5, Gibbs 4, Conklin 1, Vaki 1. 23 of 27 Goff pass plays logged "short", 5 "deep". The quick game went to St. Brown (7 catches, 6.6 avg) on short outs, so the outlet role went to the slot WR instead of checkdowns to the RB.
- Pressure: MIN 4 sacks, 9 QB hits on 29 dropbacks (31% sack+hit proxy); Van Ginkel 2.5 sacks. Blitz rate/Flores scheme: **UNVERIFIED** (the public ESPN box has no blitz or pressure rate).
- Rushing replaced receiving? Partly. 23 carries for 153 with a lead most of the 2nd half, and Vaki took 11 carries + 1 target. But wk1 and wk7 also had 29 carries and he still caught 5, so carries alone don't explain it. **The driver was low team dropbacks.**
- Snap/route split vs Vaki (Montgomery isn't on the 2026 DET box): **UNVERIFIED**, no snap or route data in the ESPN API.
- MIN RB targets allowed this season, QB-adjusted: **NOT COMPUTED** (no time this pass; needs W1-7 boxes). MIN allowed today: Gibbs 4 + Vaki 1 = 5 RB targets.
- Sharp/public popularity of the leg: **UNKNOWN**, no source checked.
- Pregame line: DET -3.5, total 45.5. A low total plus a favored run team pointed to fewer dropbacks.

**Lesson:** an RB reception over at 5.5 needs a projected team dropback count, not a "clears every week" hit rate. 4+ was a 6/6 trend; 5.5 was 2/6.

## 2) Ravens QB collapse, BAL 10 @ BUF 36 (event 401873026)
**Timeline (ESPN PBP):**
- **Lamar Jackson:** hurt on his 1st dropback, **Q1 10:04** (incomplete to Flowers; "BLT-L.Jackson was injured during the play"). 0/1. Flowers 1 target, 0 catches.
- **Tyler Huntley:** Q1 10:00 to Q2 14:10. 2/4, 0 yds, 1 sack, plus a fumble lost on the Q2 14:10 Bishop strip-sack. Flowers 0 targets. ESPN PBP has **no explicit injury tag for Huntley**. His exit after the strip-sack is inferred from the play sequence; the injury itself is from the parent brief, **unverified in PBP**.
- **Joe Fagnano:** from **Q2 9:39** to the end. 10/21, 91 yds, 0 TD, 1 INT, 3 sacks. Flowers 4 targets, 0 catches; the INT (Igbinosun, Q2 1:21) was intended for Flowers.
- Flowers final: 0/5. Legs: rec O6 (PP25), yds O49.5 (UD20), yds O59.5 (FD7/FD8). All missed.

**Who Fagnano threw to (by depth label):** Justice Hill 6 (all short), Andrews 4 short, Flowers 4 short, Bateman 1 short + 2 deep, Lane 1 short + 1 deep, Cuevas, Henry, Hibner 1 each. 18 of 21 short. Hill led the team with 8 targets: it became a checkdown/RB offense.

**Script and BUF defense:** BUF -3, total 54.5. Score 7-10, 7-16, 10-23, 10-36. BAL 145 total yds, 2.3 yds per pass, 3 turnovers. BUF had 4 sacks and 12 QB hits on 30 dropbacks (40% proxy); Rousseau had 3 hits and was the defender on 2 Flowers targets, Ed Oliver 3 hits. Blitz's script file cites a 35% BUF blitz rate; that number isn't from public ESPN data, so **source unverified**. Coverage shell: **UNVERIFIED**.

**Pregame signals:**
- QB_SCREEN.md: "Jackson returns from a three-game absence" and "Huntley's team-level results are not his baseline", but also "No current QB injury row in feed; starter per saved Friday depth chart." Our feed showed **no designation**. Lamar's actual practice/injury status during the week: **UNVERIFIED** (not re-pulled).
- Huntley's pregame status and the exact BAL depth chart (was Fagnano QB3, or active as emergency QB?): **UNVERIFIED**.
- The backup gap was known: Huntley started the 3 games Lamar missed, and the screen itself warned not to use Huntley's numbers.

**Lesson:** an in-game injury on the first series can't be priced, but **a QB just back from a multi-week absence** is a known re-injury and rust risk, and WR1 overs are the most fragile legs under a backup (targets shift to RB/TE checkdowns: Hill 8, Flowers 0 catches).

## What our process should change (PROPOSALS for Rico, via Ghost6; not adopted)
1. **Team dropback gate for RB reception overs:** project team dropbacks from spread + total + run rate. If projected dropbacks are under 32, require the line to be at or below the player's 4+ floor (e.g., take 3.5, not 5.5). Backtest W1-8 first.
2. **Line-vs-hit-rate check:** always grade the trend at the actual line ("4+ in 6/6" doesn't support "5.5"). Show the hit rate at the line on every card.
3. **Low-total favorite flag:** for favorites with a total under 46 and a run-heavy identity, shrink their pass-catcher reception projections (St. Brown, LaPorta and Gibbs all missed or barely cleared).
4. **QB-return / injury-designation WR1 cap:** if the starting QB is (a) listed Q/D, (b) in his first game back from 2+ missed games, or (c) backed up by a QB whose season EPA is well below the starter's, cap WR1 exposure at 1 leg per ticket, no WR1 in multiple slips, and prefer RB/TE reception unders or alternatives.
5. **Correlated-exposure limit:** Flowers sat in 4 slips (PP25, UD20, FD7, FD8), so one injury killed four tickets. Proposal: max 2 tickets carry the same player.
6. **Data gaps to fill:** snap/route counts (nflverse/PFF), blitz/pressure rates (NGS/PFF), the official injury report pulled Friday and Sunday morning, and backup-QB depth tracked in the feed.
