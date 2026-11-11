# Washington pass defense vs the air, and Week 5 credits on Nabers and Likely

Research only for Thursday Night Football, November 12, 2026, Commanders at Giants. No picks. No model changes. `projection_ready` was not set. Passing-yard legs stay off the user's slips; pass-defense numbers here are descriptive only.

As of 2026-11-10 10:45 AM ET. Week 7 was Washington's bye.

## What this is, and what it is not

This memo answers three questions with sourced numbers:

1. What Washington has allowed through the air, game by game in Weeks 1-9, grouped by secondary look.
2. Whether the defense is mostly single-high (MOFC) or two-high (MOFO), and man or zone. Weekly charted coverage from nflverse does not exist for 2026. The answer uses public season and last-1/3/5 rates, labeled by source and date.
3. In the Week 5 27-27 OT game at Northwest Stadium, every official target to Malik Nabers and Isaiah Likely, with the official gamebook credit (tackler, pass defender, or interceptor), and whether that person is still in the current secondary.

Named defenders on those plays are official credits, not verified coverage assignments. No public 2026 charted coverage file (nflverse participation, FTN coverage type, NGS assignment, or PFF) was available play by play.

## 1. Pass defense allowed, game by game

Official counting stats are from nflverse `stats_team_week` (opponent offense vs WAS, plus WAS defensive sack / QB-hit / INT / PBU totals), pulled from the 2026-11-10 13:45 UTC nflverse-data release (local copy 10:26 AM ET). Gross passing yards do not subtract sacks. YPA is gross yards / official attempts. EPA per dropback and 20-yard receptions are from nflverse `play_by_play_2026.parquet` through Week 9 (same release). EPA/dropback uses every play with `qb_dropback=1` (sacks and some scrambles are included), so it will not always equal official `passing_epa` divided by attempts plus sacks. Official vs PBP attempts, yards, and 20-yard completions match in every WAS game in this file.

True weekly pressures are not in public PBP. The table has sacks, QB hits, and FTN pass-rush / blitz counts instead. NFL Savant has only a season pressure rate, and even that site has two different season figures (15.0% and 18.6%) on the same team page — neither is used as a weekly number. FTN charting matched every Washington dropback in Weeks 1-9.

Secondary eras are from snap shares, not from coverage charting:

- **Weeks 1-2, Sainristil nickel:** Mike Sainristil 98% and 82%. Trey Amos on reserve. Nick Cross every-down.
- **Weeks 3-6, transition:** Sainristil's share collapsed. Cross missed Weeks 3-5 (illness); Quan Martin was every-down those three games. Amos was activated in Week 6 only (58%). This is not the same look as Weeks 1-2 or Weeks 8-9.
- **Weeks 8-9, Amos / Robertson:** After the bye. Amos 87% then 97% and started Week 9. Robertson every-down. Sainristil 0% and 1%. Douglas down to 46% then 24%. Cross back every-down.

| Wk | Opp | Result | Era | Cmp/Att | Gross yds | TD | INT | YPA | Sacks | QB hits | 20+ rec | EPA/dropback | WR rec-yds-TD | TE rec-yds-TD | RB rec-yds-TD | Sainristil% | Amos% | Douglas% | Cross% |
| ---: | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| 1 | PHI away | L 22-24 | Sainristil nickel | 14/25 (56.0%) | 203 | 3 | 0 | 8.12 | 3 | 5 | 3 | 0.166 | 8-121-1 | 4-77-2 | 2-5-0 | 98 | — | 31 | 98 |
| 2 | DAL away | L 20-37 | Sainristil nickel | 26/31 (83.9%) | 279 | 4 | 0 | 9.0 | 2 | 6 | 4 | 0.462 | 19-216-2 | 4-43-2 | 3-20-0 | 82 | — | 44 | 100 |
| 3 | SEA home | W 33-31 | Transition (Cross out) | 32/46 (69.6%) | 393 | 4 | 2 | 8.54 | 0 | 6 | 4 | 0.141 | 19-236-3 | 6-82-1 | 7-75-0 | 39 | — | 67 | — |
| 4 | IND home | L 13-30 | Transition (Cross out) | 19/34 (55.9%) | 143 | 0 | 1 | 4.21 | 2 | 6 | 1 | -0.371 | 12-93-0 | 5-41-0 | 2-9-0 | 8 | — | 85 | — |
| 5 | NYG home | T 27-27 OT | Transition (Cross out) | 33/54 (61.1%) | 326 | 3 | 0 | 6.04 | 2 | 7 | 4 | 0.244 | 15-155-1 | 13-129-2 | 5-42-0 | 48 | — | 98 | — |
| 6 | SF away | L 17-23 | Transition (Amos debut) | 21/29 (72.4%) | 264 | 1 | 0 | 9.1 | 2 | 3 | 4 | 0.111 | 5-129-0 | 5-69-1 | 11-66-0 | 11 | 58 | 58 | 89 |
| 8 | PHI home | W 27-10 | Amos/Robertson | 23/34 (67.6%) | 212 | 0 | 1 | 6.24 | 5 | 8 | 3 | -0.213 | 10-93-0 | 7-83-0 | 6-36-0 | 0 | 87 | 46 | 100 |
| 9 | LA home | L 13-20 | Amos/Robertson | 26/43 (60.5%) | 228 | 1 | 1 | 5.3 | 1 | 5 | 1 | -0.028 | 18-186-1 | 5-26-0 | 3-16-0 | 1 | 97 | 24 | 100 |

Net passing yards (gross minus sack yards) and FTN rush/blitz rates are in `was_pass_def_allowed_by_game.csv` and `ftn_pass_rush_blitz_by_game.csv`.

### By era (small samples)

- **Weeks 1-2, Sainristil nickel (2 games, PHI and DAL):** 40/56 (71.4%), 482 gross pass yards (241.0/g), 7 TD, 0 INT, 8.61 YPA, 5 sacks, 11 QB hits, 7 completions of 20+, EPA/dropback 0.32. This window includes the 37-point game in Dallas (26/31, 279 yards, 4 TD, +0.462 EPA/dropback). It is a two-game sample and was a poor pass-defense stretch, especially versus tight ends (8 catches, 120 yards, 4 TD).
- **Weeks 3-6, transition (4 games):** 105/163 (64.4%), 1126 gross pass yards (281.5/g), 8 TD, 3 INT, 6.91 YPA, 6 sacks, 22 QB hits, 13 completions of 20+, EPA/dropback 0.066. Includes the 393-yard, 4-TD game vs Seattle (0 sacks) and the Giants' 33/54, 326, 3 TD in overtime. Also includes the best game in the window, Indianapolis (19/34, 143, 0 TD, 1 INT, -0.371 EPA/dropback).
- **Weeks 8-9, Amos / Robertson (2 games, PHI and LAR):** 49/77 (63.6%), 440 gross pass yards (220.0/g), 1 TD, 2 INT, 5.71 YPA, 6 sacks, 13 QB hits, 4 completions of 20+, EPA/dropback -0.119. Fewer explosive completions and a negative EPA/dropback compared with the first two weeks, but it is also only two games, and Week 8 vs Philadelphia (23/34, 212, 0 TD, 1 INT, 5 sacks, -0.213 EPA/dropback) drives a lot of the improvement.

Same opponent, different look — the only clean-ish comparison is Philadelphia:

- Week 1 at PHI (Sainristil nickel): 14/25, 203 yards, 3 TD, 0 INT, 8.12 YPA, 3 sacks, 5 QB hits, 3 completions of 20+, EPA/dropback 0.166. Washington lost 22-24. WRs 8-121-1, TEs 4-77-2.
- Week 8 vs PHI (Amos/Robertson): 23/34, 212 yards, 0 TD, 1 INT, 6.24 YPA, 5 sacks, 8 QB hits, 3 completions of 20+, EPA/dropback -0.213. Washington won 27-10. WRs 10-93-0, TEs 7-83-0.

That is one opponent pair, not a proof that the new secondary is fixed. Game script, pass rush (Omenihu was also back in Week 8), and Philadelphia's own offense all changed. It is the best same-opponent snapshot in the file.

**Through the air vs the current look (Weeks 8-9 only):** opponents completed 49 of 77 (63.6%) for 440 gross yards (5.71 YPA), 1 TD, 2 INT, 6 sacks, 4 official 20-yard completions, and EPA/dropback -0.119. In those two games Washington allowed 28-279-1 to WRs (6.49 yards per target), 12-109-0 to TEs (6.81), and 9-52-0 to RBs (3.71). Tight ends were a season-long leak on Sharp's November 3 table (9.4 yards per target allowed, before Week 9).

## 2. MOFC vs MOFO, man vs zone

**There is no 2026 nflverse participation file, and public FTN charting does not include coverage type.** `pbp_participation_2026` was not on the nflverse-data participation release as of November 10, 2026 (files stop at 2025, last updated February 10, 2026). The 2026 FTN file is current through Week 9, but its columns are box count, rushers, blitzers, and play-action/screen flags — not `defense_coverage_type` or `defense_man_zone_type`. NFL Savant's WAS pages also have `identity_coverage_participation=false` and empty coverage arrays. So there is no play-by-play or official weekly shell mix from those sources.

What is public is season-level (and some last-1/3/5) charting from Sharp Football and StatRankings. Those are third-party charts, not official NFL, and the two sources do not use the same snap universe.

**Season answer:** Washington is a two-high / MOFO, zone-heavy defense in 2026, not a single-high / MOFC, man-heavy one.

- Sharp Football, updated November 3, 2026 (through Week 8; Week 9 vs LAR had not been played): Washington man 12.2%, zone 78.4%, middle closed (MOFC) 32.1%, middle open (MOFO) 61.0%. URL: https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/
- StatRankings CoverageIQ, fetched November 10, 2026 (includes Week 9; labeled vs WR, 313 coverage snaps): man 17.9% (32nd), zone 81.8% (1st), single-high 38.2% (31st), two-high 61.8% (2nd), blitz 44.4% (3rd). URL: https://statrankings.com/nfl/coverage/team/was
- StatRankings two-high page, updated November 10, 2026: Washington 2nd at 61.8% two-high (Cover 2 / 4 / 6 family). Last 1 (Week 9 vs LAR): 61.0%. Last 3 (Weeks 6, 8, 9): 59.1%. Last 5: 55.7%.
- StatRankings zone page, updated November 10, 2026: Washington 1st at 81.8% zone. Last 1: 77.3%. Last 3: 86.0%. Last 5: 80.1%.
- StatRankings Cover 4 page, updated November 10, 2026: Washington 3rd at only 14.1% Cover 4, and 4.5% in the last game. A 61.8% two-high rate with a 14.1% Cover 4 rate means most two-high snaps are not quarters — they are other two-high families (Cover 2 / Cover 6 / similar). A preseason Hogs Haven preview expected a Cover-4-heavy Daronte Jones / Flores-tree look; the midseason public Cover 4 rate does not show that.

The StatRankings last-1/3/5 tables did not print team names in the fetched HTML. Washington was identified from the accompanying prose and from season rates that uniquely matched the CoverageIQ page. Treat those weekly splits as labeled third-party estimates, not official weekly charting.

Man-rate disagreement (Sharp 12.2% vs StatRankings 17.9%) is expected: different update dates, and StatRankings' team page is vs WR rather than all coverage snaps. Both still put Washington among the most zone-heavy, least man-heavy teams in the league. Jones replaced Joe Whitt under Dan Quinn; ESPN's offseason preview (story 48913350) said the 2026 defense would play much more zone than the Quinn/Whitt years. The midseason rates are consistent with that preview. They are not a play-by-play answer for Thursday.

FTN weekly pass-rush / blitz rates (not coverage) are in `ftn_pass_rush_blitz_by_game.csv`. StatRankings also has Washington among the highest blitz rates (44.4%, 3rd on the Nov 10 vs-WR page). In the FTN file, the share of dropbacks with at least one blitzer was 0.394 and 0.472 in Weeks 1-2, and 0.326 and 0.364 in Weeks 8-9 — a lower blitz rate in the two most recent games, not a higher one.

## 3. Week 5 at Northwest Stadium: every Nabers and Likely target

Official gamebook: [NFL.com Game Center, Giants at Commanders 2026 REG 5](https://www.nfl.com/games/giants-at-commanders-2026-reg-5), PDF https://static.www.nfl.com/gamecenter/aa94b906-4feb-11f1-abca-2c54536568a9.pdf (sha256 `7af620491c84cce23d2ed3cfa482b6d4ff3ff9b4f323a2bacdf3a3cf7c6c0982`, 23 pages, saved under `gamebook/`). The nfl-matchup-database repo only has Week 9 gamebooks on main, so this Week 5 book was downloaded from the same NFL Game Center "Download Game Book" URL pattern, not from that repo.

Final: Giants 27, Commanders 27, overtime. Official receiving (gamebook box and nflverse player week, and this parser) agree:

- **Malik Nabers:** 11 catches on 20 official targets, 121 yards, 1 TD (long 28).
- **Isaiah Likely:** 11 catches on 13 official targets, 94 yards, 2 TDs (3 yards in the third quarter, 17 yards in the fourth after a replay reversal).

Washington's Week 5 starting defense in the gamebook: OLB Chaisson, DT Payne, DT Settle, DT Kinlaw, OLB Oweh, LB Styles, LB Luvu, CB Douglas, CB Robertson, S Reaves, S Martin. **Nick Cross and Trey Amos were not in this game** (Cross inactive / illness; Amos still on reserve). Mike Sainristil and Fabian Moreau were substitutes (Sainristil 48% snaps, Moreau 29%). Quan Martin and Rasul Douglas were every-down that day (99% and 98%).

Two no-plays are listed below and are not official targets: a first-quarter Likely catch wiped out by an illegal-shift penalty on Likely, and a third-quarter McCarthy-to-Nabers 14-yard catch wiped out by an illegal-shift penalty on New York. A late third-quarter pass intended for Likely was intercepted by Amik Robertson and then nullified by defensive pass interference on Robertson. That is also a no-play, with the credit going to Robertson as the interceptor, not as a coverage assignment.

**Credit rule, repeated on every row:** the name in parentheses is the official tackler or pass-defense credit. Brackets are QB hits. Those are not proven coverage assignments.

### Malik Nabers, official targets (20) plus the no-play

- Q1 7:55, 3-19 at WAS 39: J.Winston to Malik Nabers (short right), complete, 7 yards. Named credit: Q.Martin.
- Q1 2:35, 1-10 at NYG 45: J.Winston to Malik Nabers (deep left), complete, 20 yards. Named credit: A.Robertson.
- Q2 :24, 1-10 at WAS 39: J.Winston to Malik Nabers (short left), incomplete. Named credit: (none named).
- Q2 :20, 2-10 at WAS 39: J.Winston to Malik Nabers (deep right), incomplete. Named credit: (none named).
- Q3 12:48, 2-10 at WAS 45: J.McCarthy to Malik Nabers (short left), no_play. Named credit: S.Styles; NO PLAY — not an official target.
- Q3 6:45, 1-10 at WAS 49: J.Winston to Malik Nabers (short middle), incomplete. Named credit: (none named); QB hit: K.Chaisson.
- Q3 4:09, 2-5 at WAS 17: J.Winston to Malik Nabers (short right), complete, 6 yards. Named credit: R.Douglas.
- Q3 1:36, 1-1 at WAS 1: J.Winston to Malik Nabers (short middle), incomplete. Named credit: S.Styles.
- Q4 9:30, 1-10 at WAS 39: J.Winston to Malik Nabers (short right), complete, 12 yards. Named credit: A.Robertson.
- Q4 8:15, 2-15 at WAS 24: J.Winston to Malik Nabers (deep left), incomplete. Named credit: (none named).
- Q4 4:25, 2-4 at NYG 34: J.Winston to Malik Nabers (short right), complete, 6 yards. Named credit: S.Styles; A.Robertson.
- Q4 3:56, 1-10 at NYG 40: J.Winston to Malik Nabers (short right), complete, 3 yards. Named credit: F.Moreau.
- Q4 3:25, 2-7 at NYG 43: J.Winston to Malik Nabers (deep right), incomplete. Named credit: (none named).
- Q4 3:18, 3-7 at NYG 43: J.Winston to Malik Nabers (short left), complete, 16 yards. Named credit: F.Moreau.
- Q4 2:00, 1-10 at WAS 31: J.Winston to Malik Nabers (deep right), incomplete. Named credit: (none named).
- Q4 1:48, 1-10 at WAS 17: J.Winston to Malik Nabers (deep middle), touchdown, 17 yards, TD. Named credit: (none named).
- OT 9:27, 1-10 at WAS 45: J.Winston to Malik Nabers (short left), incomplete. Named credit: (none named).
- OT 9:24, 2-10 at WAS 45: J.Winston to Malik Nabers (short right), incomplete. Named credit: F.Moreau.
- OT 5:29, 2-10 at NYG 9: J.Winston to Malik Nabers (short middle), complete, 8 yards. Named credit: R.Douglas.
- OT 4:40, 1-10 at NYG 36: J.Winston to Malik Nabers (deep middle), complete, 28 yards. Named credit: Q.Martin.
- OT 4:01, 1-10 at WAS 36: J.Winston to Malik Nabers (short right), complete, -2 yards. Named credit: R.Douglas.

Parser totals match the official line: 11-121-1 on 20 official targets.

Who is named most often on official Nabers targets (parentheses credits only, not coverage):

- Amik Robertson (A.Robertson): named on 3 official targets (3 catches, 38 yards, 0 TD).
- Fabian Moreau (F.Moreau): named on 3 official targets (2 catches, 19 yards, 0 TD).
- Rasul Douglas (R.Douglas): named on 3 official targets (3 catches, 12 yards, 0 TD).
- Quan Martin (Q.Martin): named on 2 official targets (2 catches, 35 yards, 0 TD).
- Sonny Styles (S.Styles): named on 2 official targets (1 catches, 6 yards, 0 TD).
- No named tackler/pass defender on 8 official targets.

The 17-yard Nabers touchdown has no defender named in the gamebook. Eight official Nabers targets have no parentheses credit, mostly incompletes.

### Isaiah Likely, official targets (13), plus no-plays

- Q1 10:23, 3-13 at NYG 40: J.Winston to Isaiah Likely (short left), complete, 15 yards. Named credit: R.Douglas.
- Q1 9:03, 1-15 at WAS 35: J.Winston to Isaiah Likely (short left), no_play. Named credit: A.Robertson; NO PLAY — not an official target.
- Q1 4:26, 3-6 at NYG 28: J.Winston to Isaiah Likely (short left), complete, 4 yards. Named credit: J.Reaves.
- Q2 :56, 1-10 at NYG 35: J.Winston to Isaiah Likely (short middle), complete, 9 yards. Named credit: S.Styles; replay reversal; yards and result are the official reversed ruling.
- Q2 :31, 1-10 at NYG 49: J.Winston to Isaiah Likely (short right), complete, 12 yards. Named credit: A.Robertson.
- Q3 14:57, 1-10 at NYG 33: J.Winston to Isaiah Likely (short middle), complete, 11 yards. Named credit: J.Reaves.
- Q3 12:54, 1-10 at WAS 45: J.Winston to Isaiah Likely (deep right), incomplete. Named credit: R.Douglas.
- Q3 4:48, 1-10 at WAS 22: J.Winston to Isaiah Likely (short right), complete, 5 yards. Named credit: D.Armstrong; F.Luvu.
- Q3 1:46, 3-9 at WAS 10: J.Winston to Isaiah Likely (short middle), interception_nullified_no_play. Named credit: (none named); INT credited to A.Robertson; WAS penalty: A.Robertson (Defensive Pass Interference); NO PLAY — not an official target.
- Q3 :47, 3-3 at WAS 3: J.Winston to Isaiah Likely (short right), touchdown, 3 yards, TD. Named credit: (none named).
- Q4 11:00, 1-10 at NYG 25: J.Winston to Isaiah Likely (short left), complete, 10 yards. Named credit: R.Douglas.
- Q4 7:24, 4-8 at WAS 17: J.Winston to Isaiah Likely (short middle), touchdown_after_replay_reversal, 17 yards, TD. Named credit: (none named); QB hit: K.Chaisson; replay reversal; yards and result are the official reversed ruling.
- Q4 4:56, 1-10 at NYG 28: J.Winston to Isaiah Likely (short middle), complete, 6 yards. Named credit: S.Styles; Q.Martin.
- OT 8:47, 1-10 at WAS 30: J.Winston to Isaiah Likely (short right), complete, 2 yards. Named credit: F.Luvu.
- OT 8:10, 2-8 at WAS 28: J.Winston to Isaiah Likely (deep middle), incomplete. Named credit: (none named); QB hit: D.Armstrong.

Parser totals match the official line: 11-94-2 on 13 official targets. The second-quarter catch at 0:56 was reversed from 10 yards to 9 yards; the official 9-yard ruling is the one counted.

Who is named most often on official Likely targets (parentheses credits only):

- Rasul Douglas (R.Douglas): named on 3 official targets (2 catches, 25 yards, 0 TD).
- Jeremy Reaves (J.Reaves): named on 2 official targets (2 catches, 15 yards, 0 TD).
- Sonny Styles (S.Styles): named on 2 official targets (2 catches, 15 yards, 0 TD).
- Frankie Luvu (F.Luvu): named on 2 official targets (2 catches, 7 yards, 0 TD).
- Amik Robertson (A.Robertson): named on 1 official targets (1 catches, 12 yards, 0 TD).
- Quan Martin (Q.Martin): named on 1 official targets (1 catches, 6 yards, 0 TD).
- Dorance Armstrong (D.Armstrong): named on 1 official targets (1 catches, 5 yards, 0 TD).
- No named tackler/pass defender on 3 official targets.

The 17-yard Likely touchdown in the fourth quarter was first ruled a 16-yard catch, fumble, and Washington recovery / touchback, with Q.Martin and R.Douglas named as the tacklers. Replay reversed it to a touchdown. The final gamebook text has no tackler and lists K.Chaisson only as a QB hit. Both versions are in the play text; the official result is the touchdown, and the availability table does not treat the reversed fumble credits as the final named tackler.

Combined, the defenders named most often in parentheses on official Nabers + Likely targets are Rasul Douglas (6), Amik Robertson (4), Sonny Styles (4), Quan Martin (3), and Fabian Moreau (3). Mike Sainristil does not appear as a parentheses credit on these Nabers/Likely targets (he is named on other Giants plays that day, including a Tracy catch and a Skattebo run). nflverse PBP tackle / `pass_defense_*` fields for the same plays are in `week5_nabers_likely_targets_pbp.csv` and the crosswalk (36 of 36 plays matched). Those fields are the same kind of official credit, not coverage assignments.

## 4. Are those Week 5 defenders available Thursday?

Injury status as of November 10, 2026: ESPN screenshots from Nov 9-10 (IR: Payne, Kinlaw, Jean-Baptiste, Chenal, Dyami Brown; questionable: Tuttle). nflverse injuries are only through the Week 9 report; there is not yet a Week 10 practice report in that file. Snap shares are Weeks 8-9.

- **Rasul Douglas:** named on 6 official Nabers/Likely targets (3 Nabers, 3 Likely). Week 5 snaps 98%; Week 8 46%; Week 9 24%. Active now: True. Not on the Nov 10 ESPN IR list (Payne, Kinlaw, Jean-Baptiste, Chenal, Dyami Brown). No Week 10 nflverse injury-report game status for this player. Active, but not the Week 5 every-down starter. Snap share fell from 98% in Week 5 to 46% (W8) and 24% (W9). Week 9 gamebook: substitute, not a starter (Amos and Robertson started). ESPN still lists him as starting LCB; that does not match Weeks 8-9 usage.
- **Amik Robertson:** named on 4 official Nabers/Likely targets (3 Nabers, 1 Likely). Week 5 snaps 98%; Week 8 99%; Week 9 96%. Active now: True. Not on the Nov 10 ESPN IR list (Payne, Kinlaw, Jean-Baptiste, Chenal, Dyami Brown). No Week 10 nflverse injury-report game status for this player. Active and still every-down. 99% Week 8, 96% Week 9. Official Week 9 starting CB. ESPN lists him as starting nickel. Highest-usage corner on the current roster.
- **Sonny Styles:** named on 4 official Nabers/Likely targets (2 Nabers, 2 Likely). Week 5 snaps 100%; Week 8 99%; Week 9 97%. Active now: True. Not on the Nov 10 ESPN IR list (Payne, Kinlaw, Jean-Baptiste, Chenal, Dyami Brown). No Week 10 nflverse injury-report game status for this player. Active, every-down ILB. 99% Week 8, 97% Week 9. Official Week 9 starting LB.
- **Quan Martin:** named on 3 official Nabers/Likely targets (2 Nabers, 1 Likely). Week 5 snaps 99%; Week 8 46%; Week 9 56%. Active now: True. Not on the Nov 10 ESPN IR list (Payne, Kinlaw, Jean-Baptiste, Chenal, Dyami Brown). No Week 10 nflverse injury-report game status for this player. Active, reduced role after Cross returned. He was every-down in Week 5 (99%) because Cross was out. Weeks 8-9: 46% and 56%. ESPN lists him as the FS backup behind Reaves.
- **Fabian Moreau:** named on 3 official Nabers/Likely targets (3 Nabers, 0 Likely). Week 5 snaps 29%; Week 8 —%; Week 9 —%. Active now: uncertain. Not on the ESPN IR list. Inactive in the Week 9 official gamebook. No Week 10 injury report in nflverse. Do not assume he is active Thursday until the inactive list posts. Played Weeks 3-5 only (30%, 39%, 29%), including Week 5 vs NYG. Inactive in the official Week 9 gamebook. No Week 8 defensive snaps. nflverse Week 8 practice: full (knee); no Week 9/10 game-status tag. ESPN lists him as Douglas's backup. Do not assume he is active Thursday until the inactive list posts.
- **Jeremy Reaves:** named on 2 official Nabers/Likely targets (0 Nabers, 2 Likely). Week 5 snaps 97%; Week 8 93%; Week 9 60%. Active now: True. Not on the Nov 10 ESPN IR list (Payne, Kinlaw, Jean-Baptiste, Chenal, Dyami Brown). No Week 10 nflverse injury-report game status for this player. Active. Official Week 9 starting safety and ESPN starting FS. 93% Week 8, season-low 60% in Week 9.
- **Frankie Luvu:** named on 2 official Nabers/Likely targets (0 Nabers, 2 Likely). Week 5 snaps 100%; Week 8 100%; Week 9 100%. Active now: True. Not on the Nov 10 ESPN IR list (Payne, Kinlaw, Jean-Baptiste, Chenal, Dyami Brown). No Week 10 nflverse injury-report game status for this player. Active, every-down ILB. 100% in Weeks 8 and 9. Official Week 9 starting LB.
- **Dorance Armstrong:** named on 1 official Nabers/Likely targets (0 Nabers, 1 Likely). Week 5 snaps 49%; Week 8 58%; Week 9 53%. Active now: True. Not on the Nov 10 ESPN IR list (Payne, Kinlaw, Jean-Baptiste, Chenal, Dyami Brown). No Week 10 nflverse injury-report game status for this player. Active, rotational OLB/edge. 58% Week 8, 53% Week 9. ESPN lists him as starting SLB, but Chaisson started Week 9 and has the higher season snap share.
- **K'Lavon Chaisson:** named on 0 official Nabers/Likely targets (0 Nabers, 0 Likely). Week 5 snaps 65%; Week 8 71%; Week 9 61%. Active now: True. Not on the Nov 10 ESPN IR list (Payne, Kinlaw, Jean-Baptiste, Chenal, Dyami Brown). No Week 10 nflverse injury-report game status for this player. Active, starter-level edge. 71% Week 8, 61% Week 9. Official Week 9 starting OLB. On the Week 5 Nabers/Likely plays he is credited only as a QB hit (brackets), not as a tackler or pass defender.

The practical overlap with Thursday's likely secondary:

- **Still every-down, and actually credited in Week 5:** Amik Robertson (still 96-99%). Sonny Styles and Frankie Luvu (linebackers, still every-down). Jeremy Reaves is still the starting FS, with a lighter Week 9 share (60%).
- **Credited often in Week 5, but not in the same role now:** Rasul Douglas was a 98% starter that day and is down to 24% (Week 9 substitute). Quan Martin was a 99% starter only because Cross was out; he is a 46-56% backup now that Cross is back.
- **Credited in Week 5, availability not assumed:** Fabian Moreau had three official Nabers credits (including a pass breakup) and 29% snaps that day, then disappeared from the defense and was inactive in the Week 9 gamebook.
- **Not in the Week 5 game at all, but central now:** Trey Amos (current starting CB, 97% in Week 9) and Nick Cross (current every-down SS). There is no Week 5 Nabers/Likely credit for either, because they did not play. This memo cannot say Amos or Cross was the one on Nabers or Likely in Week 5.

So the question "will the guys who were named on Nabers and Likely be available again?" — Robertson, Styles, Luvu, and Reaves should be, unless Thursday's inactives say otherwise. Douglas is on the roster but may not be on the field much. Martin is a backup behind a now-healthy Cross. Moreau is the open question. Amos and Cross, the two biggest secondary additions since that game, have no Week 5 assignment evidence against these two receivers.

## Gaps (do not fill these in)

- No 2026 nflverse `pbp_participation` file, so no play-level `defense_coverage_type` or `defense_man_zone_type`, and no weekly man/zone/shell mix from that source.
- Public FTN 2026 charting has no coverage-shell column.
- NFL Savant 2026 coverage participation is false; no defender-vs-receiver charting there.
- No public NGS coverage table was used.
- Sharp's MOFC/MOFO rates are through November 3 (Week 8), not Week 9. StatRankings last-1/3/5 fills some of that, but those pages did not print team names in the fetched tables; Washington was identified from the accompanying prose and matching season rates. Cover 2 / Cover 3 / Cover 6 rates for Washington were not captured as named rows (only Cover 4 among the individual shells).
- Named Week 5 defenders are credits, not coverage assignments. Several official Nabers incompletes and his 17-yard TD have no defender named.
- No Week 10 official injury report or Thursday inactive list in nflverse yet. Moreau's Thursday status is unverified. Tuttle is questionable but is a defensive tackle, not a Week 5 Nabers/Likely credit.
- Weekly true pressures are unavailable. Do not invent them from sacks or QB hits.
- Passing-yard props are out of scope for slips; nothing in this folder is a bet recommendation.

## Files

- `gamebook/2026_05_NYG_WAS_gamebook.pdf` and `.txt` — official Week 5 game book.
- `was_pass_def_allowed_by_game.csv` — Weeks 1-9 (no Week 7) pass defense allowed, with era labels and secondary snap shares.
- `was_pass_def_allowed_by_era.csv` — rolled-up eras, plus pre-bye and season totals.
- `was_pass_def_allowed_by_position_game.csv` / `_era.csv` — WR/TE/RB production allowed.
- `was_pass_def_phi_w1_vs_w8.csv` — same-opponent snapshot.
- `ftn_pass_rush_blitz_by_game.csv` — FTN rushers/blitzers/box, not coverage.
- `coverage_shell_sources.csv` — every coverage source, date, figure, and gap.
- `week5_nabers_likely_targets_gamebook.csv` — the play list.
- `week5_nabers_likely_targets_pbp.csv` and `week5_nabers_likely_targets_crosswalk.csv`.
- `week5_named_defender_counts.csv` and `week5_named_defenders_availability.csv`.
- `week5_gamebook_lineups_defense.csv`.
- `gaps.csv` and `provenance.json`.
