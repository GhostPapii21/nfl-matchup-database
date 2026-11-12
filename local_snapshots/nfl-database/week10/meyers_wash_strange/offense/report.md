# JAX offense half: Meyers / P. Washington / Strange vs BAL (TNF Thu Nov 5, 2026)
Built 2026-11-04 ~17:45 ET on branch mws-matchup-2026-11-04. Research inputs only, not picks. Scenario-first; game logs are a cross-check. Passing-yards legs are off slips.

**Sources (pull times ET)**
- [N] nflverse 2026 local snapshot (pbp, FTN charting, snap_counts, roster_weekly), CC-BY, pulled 2026-11-03 08:04 ET: `sources/nflverse/`. Computed by `runA/build_a.py` (Codex run A), outputs in `runA/*.csv`.
- [E] ESPN game logs, fetched 2026-11-04 17:10 ET: Meyers https://www.espn.com/nfl/player/gamelog/_/id/3916433/type/nfl/year/2026 , Washington .../id/4432620/... , Strange .../id/4430539/... ; schedule https://www.espn.com/nfl/team/schedule/_/name/jax/season/2026 (Codex run B, `runB/raw/`, `runB/fetch_log.csv`).
- [P] Free PFF matchup/player pages already in repo: `week10/pff_jax_bal/receiver_matchups.csv` (https://www.pff.com/tools/matchups), pulled Nov 3-4.
- [G] Existing NGS route-chart screenshots `week10/ngs/*.png` (capture time not recorded).
- Blocked this run: PFR (all pages HTTP 403 "Just a moment" challenge, 17:10 ET), NGS stat tables (404 or JS shell with no data, 17:10 ET).

## 1. Routes, alignment, field areas
NGS 2026 route-type counts (go/slant/out/curl/cross/screen) are **UNAVAILABLE**: NGS stat pages return a JS shell with no data, and nflverse 2026 participation (route field) was a 404/corrupt. What we have instead:

| Player | Alignment snaps 2026 [P] | Screen targets [N/FTN] | Target areas, Lawrence tgts (location/air yds) [N] | NGS chart, one game [G] |
|---|---|---|---|---|
| Washington | Wide 179 / Slot 145 | 2 of 48 | **Left side 29 of 48** (left 5-14: 15 tgt 11-114; left 15+: 10 tgt 4-84); middle 7; right 12 | Wk6: shallow crossers, intermediate breaks both sides, deep stems both sides |
| Meyers | Wide 229 / Slot 102 | 3 of 31 | Left 12 (left 15+: 3-3-88), **middle 10** (5-14: 7 tgt 5-71; 15+: 3 tgt 2-44), right 9 | Wk3 vs NE: crossers/in-breakers + outs, short/intermediate, TD intermediate middle |
| Strange | Inline 171 / Slot 80 / Wide 39 / Backfield 38 | 2 of 35 | Spread: left 14, **middle 5-14: 9 tgt 5-76**, right 11 (mostly short 1-14) | Wk4 vs CIN: flats/underneath, intermediate diagonals/crossers, outs |
Route types from screenshots are visual reads of one game each, not counts.

**NGS Weeks 1-6 aggregates (nflverse NGS file `week8/defense/raw/ngs_receiving.parquet` / `ngs_passing.parquet`, pulled 2026-10-29 06:04 ET, week 0 = season row).** Verified: NGS targets 46/33/28 equal nflverse pbp Wks 1-6 targets for Washington/Strange/Meyers exactly. No Week 8.
| Player | NGS tgt (Wk1-6) | Avg cushion (Wk1-6 only) | Avg separation (Wk1-6 only) | Intended air yds/tgt | Share of team intended air yds |
|---|---|---|---|---|---|
| Washington | 46 | 6.7 | **2.1 (lowest)** | 12.8 | **37.7%** |
| Meyers | 28 | 7.8 | **3.2** | 11.9 | 21.4% |
| Strange | 33 | 7.3 | 3.1 | 7.7 | 16.2% |
Lawrence NGS time to throw (Wk1-6, 184 att): **2.72 s**, aggressiveness 16.3%; by week 2.98/2.80/2.71/2.48/2.65/2.72. Not split by blitz/pressure (NGS doesn't publish that).

**Field-area map vs Blitz's defense read (BAL leakiest = middle; tightest = short outside, per Blitz's defense half and week10/brainstorm_layers/L6_bal_allowed_by_pos_area.csv: WR deep middle 19.8 YPT on 13 tgt, middle int 11.5; short middle 1.6).** Lawrence targets by area [N]:
| Player | Middle (any depth) | Outside short (<=4 air yds, L+R) | Outside 5-14 | Outside 15+ |
|---|---|---|---|---|
| Washington (48) | 7 (15%) | 7 | 20 | 14 |
| Meyers (31) | 10 (32%) | 5 | 13 | 3 |
| Strange (35) | 10 (29%) | 11 | 10 | 4 |
Targets are not routes run. By targeted area, Meyers and Strange get the most middle work; Washington is targeted mostly outside (left 5-14 and deep). Strange's 11 short-outside targets sit in BAL's tightest zone.

## 2. Snaps, Weeks 1-8 (7 games, Wk7 bye) [N snap_counts]
| Player | Wk1 | 2 | 3 | 4 | 5 | 6 | 8 | Avg snaps | Avg snap % |
|---|---|---|---|---|---|---|---|---|---|
| Meyers | 37 (65%) | 53 (90) | 50 (81) | 50 (82) | 61 (85) | 53 (75) | 29 (54) | 47.6 | 76.0% |
| Washington | 35 (61) | 48 (81) | 50 (81) | 49 (80) | 59 (82) | 52 (73) | 36 (67) | 47.0 | 75.0% |
| Strange | 39 (68) | 49 (83) | 48 (77) | 53 (87) | 58 (81) | 54 (76) | 28 (52) | 47.0 | 74.9% |
| B. Thomas Jr. (context) | 20 (35) | 32 (54) | 23 (37) | 38 (62) | 37 (51) | 15 (21) | 28 (52) | 27.6 | 44.6% |
Wk8 was a 42-7 blowout (backups late), so Wks 2-6 (~75-90%) is the better normal-game read.

## 3. Lawrence target share, Weeks 1-8 (192 targeted Lawrence attempts) [N], cross-checked vs [E]
| Rank | Receiver | Tgt | Rec | Yds | Share | aDOT |
|---|---|---|---|---|---|---|
| 1 | Parker Washington | 48 | 27 | 432 | 25.0% | 12.9 |
| 2 | Brenton Strange | 35 | 28 | 334 | 18.2% | 7.9 |
| 3 | Jakobi Meyers | 31 | 22 | 309 | 16.1% | 10.5 |
| 4 | Brian Thomas Jr. | 21 | 10 | 117 | 10.9% | 12.2 |
| 5 | Bhayshul Tuten | 16 | 15 | 181 | 8.3% | -3.1 |
| 6 | Josh Cameron | 12 | 8 | 117 | 6.3% | 4.9 |
| 7 | Nate Boerkircher | 9 | 7 | 83 | 4.7% | 6.6 |
| 8 | Travis Hunter | 7 | 6 | 76 | 3.6% | 4.3 |
| 9 | LeQuint Allen Jr. | 5 | 2 | 9 | 2.6% | 2.6 |
| 10= | Chris Rodriguez Jr. / Ameer Abdullah | 3 / 3 | 2 / 2 | 23 / 2 | 1.6% each | |
| 12 | Quintin Morris | 2 | 1 | 7 | 1.0% | |
Weekly targets (Wk1-6, 8): Washington 6,12,5,3,9,11,2; Strange 3,2,5,8,8,7,2; Meyers 2,1,8,4,3,10,3. **ESPN per-week targets/rec/yds match nflverse exactly for all three players (21 of 21 player-weeks).** All-QB version (incl. Ewers' 3 Wk8 attempts): 195 targets, same top 3.

## 4. BAL pressure and Lawrence under it [N: pbp + FTN charting]
| BAL defense, Wks 1-8 (source: FTN charting via nflverse + pbp, NOT PFR) | BAL | League | N (BAL) |
|---|---|---|---|
| Blitz rate (FTN n_blitzers>0) | 33.0% | 31.8% | 99 / 300 FTN-charted dropbacks (303 total BAL dropbacks; 3 uncharted) |
| 5+ rushers | 33.0% | 31.8% | 99 / 300 |
| Sack rate | 5.6% on all 303 dropbacks (5.7% = 17/300 FTN-charted) | 6.2% | 17 / 303 |
| QB hit (incl. sacks per pbp flag) | 17.0% | 15.2% | 51 / 300 |
PFR blitz%/pressure%/hurries and NGS pressure: UNAVAILABLE (PFR 403, NGS shell). BAL is about league average, slightly more blitz.

| Lawrence split | Dropbacks | Att | Cmp% | YPA | Sacks (rate) | EPA/db |
|---|---|---|---|---|---|---|
| All | 219 | 197 | 66.0% | 8.58 | 13 (5.9%) | +0.28 |
| vs blitz | 67 | 62 | 58.1% | 7.02 | 4 (6.0%) | +0.15 |
| no blitz | 152 | 135 | 69.6% | 9.30 | 9 (5.9%) | +0.34 |
| pressured (proxy) | 65 | 43 | 51.2% | 7.60 | 13 (20.0%, circular: sacks define proxy) | -0.26 |
| clean (proxy) | 154 | 154 | 70.1% | 8.85 | 0 | +0.51 |
Pressure proxy = qb_hit OR sack OR FTN out-of-pocket OR scramble (nflverse pbp has no `was_pressure` field). Because sacks define the proxy, the pressured sack rate is circular. **Time to throw: UNAVAILABLE** (NGS only).

**Who he throws to** [N]
| Receiver | vs blitz (60 tgt) | Under pressure proxy (39 tgt) | Short-target proxy, air yds <=2 (51 all / 16 pressured; includes screens/designed flats) |
|---|---|---|---|
| Washington | **17 (28.3%)** | **10 (25.6%)** | 5 / 2 |
| Strange | 13 (21.7%) | 5 (12.8%) | 6 / 1 |
| Meyers | 11 (18.3%) | 8 (20.5%) | 3 / 0 |
| Tuten | 5 (8.3%) | 5 (12.8%) | **16 (31.4%) / 5 (31.3%)** |
| Cameron | 6 (10.0%) | 2 | 5 / 2 |
Denominators are targeted throws with an identified receiver. (Bugfix 2026-11-04 ~17:30 ET: build_a.py mapped null receiver IDs to "Al-Jay Henderson"; earlier 62/43/53 denominators and the Henderson row were wrong. Found by Blitz, verified by rerun.)
**Short/at-LOS target leader (check-down proxy) = RB Tuten** (16 of 51 at-or-near-LOS targets, 31.4%). Tuten is questionable (3 straight DNPs); if out, that role likely spreads to Allen/Rodriguez (hypothesis, tiny n).

## 5. Meyers' timing
Meyers is on JAX in every 2026 week of nflverse roster_weekly and pbp (Wks 1-6, 8), and ESPN labels his whole 2026 log "JAX". The LV->JAX trade happened in the 2025 season (from memory of public reporting, not re-fetched this run), so **there is no short 2026 JAX sample**: 7 games, same as the others. He had no injury designation on the final Wednesday report per the parent brief.

## Scenario notes (hypotheses, not picks)
- Washington: the clear WR1 and the top target both vs blitz and under pressure; left-side intermediate/deep. Pairs with the defense half (Wiggins Q -> Awuzie outside; Hamilton from the slot).
- Meyers: the middle-of-field guy (5-14 and 15+ middle), BAL's deep-middle area; steady 76% snaps; volume swingy (1-10 tgt).
- Strange: safest volume (top 3 among all JAX targets in all 7 games, per week10/jax_usage/targets_season.csv), but mostly short/intermediate; under pressure his share drops (21.7% vs blitz -> 12.8% under pressure). Check-downs go to the RB, not him.

## Gaps and flags
1. NGS route-type counts UNAVAILABLE (NGS pages JS shell/404 2026-11-04 17:10 ET). Separation/cushion/TTT come from the Oct 29 nflverse NGS file (Wks 1-6 only, no Wk8). Blitz's `scratch_offense_aborted/ws3/ngs_2026_receiving.parquet` is a 9-byte 'Not Found' body, not data; not used. Route reads use location x air-yards proxy + one screenshot per player.
2. PFR advanced (BAL blitz%/pressure%/hurries, Lawrence pressure%/bad throw%, player advanced receiving): UNAVAILABLE, HTTP 403 challenge. Not bypassed.
3. Pressure is a pbp/FTN proxy, not charted pressure; sack rate under "pressure" is definitional. Samples small: 65 pressured dropbacks, 43 targets; 62 blitz targets.
4. Alignment uses free PFF season splits (pulled Nov 3-4), not per-route data; no per-week alignment.
5. FTN has no route/alignment fields (column list in runA/ftn_columns.csv).
6. Wk8 blowout depresses snaps/targets; Ewers took 3 attempts.
7. nflverse snapshot is ~33 h old (pulled 2026-11-03 08:04 ET); fine for Wks 1-8, nothing newer exists.
8. ESPN schedule calls this game Week 9; directory naming retains week10.
9. Tuten (check-down RB) questionable; Wiggins Q recheck at Thu 6:50 PM ET inactives.
10. (Resolved) The "Al-Jay Henderson" targets were a null-ID mapping bug, now fixed.

## Review results
- Codex runs: A (nflverse build, `runA/`), B (public-page pulls, `runB/`). PFR all 403, NGS pages empty shells.
- Superpowers-style bug pass (`review/bugpass_recompute.txt`): independent recompute matches Lawrence targets (192; 48/35/31), snap averages and BAL blitz 33%; confirms pbp has no `was_pressure` field; ESPN per-week logs match pbp 21/21; NGS Wk1-6 targets match pbp; Blitz NGS parquet is a 9-byte "Not Found" file.
- OpenAI review (`review/review_openai.md`, gpt-5.5): 12 issues, no numeric errors found. Fixed: denominator labels (300 charted vs 303), circular pressured sack rate labeled, "check-down" renamed to short-target proxy, NGS table relabeled Wks 1-6, BAL area claim sourced, "top 3" scope stated, targets != routes. Left as flags: blitz rate == 5+ rushers (FTN n_blitzers appears defined as rushers beyond 4, so identical by construction), PFF alignment is third-party, Meyers trade date unsourced.
