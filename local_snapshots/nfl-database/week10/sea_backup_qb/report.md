# SEA backup QB profile — ARI@SEA, Sun Nov 8 2026 4:25 PM ET (built 2026-11-04 ~3:00 PM ET)
Note: media (CBS/PFT/Seahawks Wire) call this "Week 9"; repo folder is week10. Same game: Sun Nov 8 vs ARI at SEA.
Sources: nflverse pbp 2026 (../bal_secondary/raw/play_by_play_2026.parquet, wks 1-8) via build.py -> pbp_summary.txt, throw_log.csv. News: Seattle Times (Booth, 11/4 10:57 AM), CBS (Dajani 11/4 2:13 PM ET), PFT (11/4 2:05 PM), Seahawks Wire (11/4). Milroe: seahawks.com 2026 pre stats, footballdb, FOX game log. Participation = 404 (skipped).

## 6) Who starts (LATEST)
- **Macdonald: "The plan is for Drew to start. Jalen will be ready to back up."** Darnold out (quad, week-to-week, no IR; also cracked rib in MNF).
- Lock elbow (right; hurt in rainy practice ~2 wks ago, emergency QB wks 7-8): "He's able to throw. How much, we're working through that... not going to take 8,000 throws." Lock/Milroe split reps early in week. Team may sign another QB for depth.
- => Base = Lock starts (~ESTIMATE 80%); Milroe branch ~20% (Lock setback/limited throws). Recheck Wed 5 PM report + Fri status.

## 1) Lock 2026 (pbp)
| | Wk1 vs NE (relief) | Wk2 @ARI (start, W 31-7) |
|---|---|---|
| cmp/att | 16/22 (72.7%) | 19/26 (73.1%) |
| yds / YPA | 187 / 8.50 | 235 / 9.04 |
| TD/INT | 1/0 | 3/0 |
| sacks / qb_hit | 1 / 5 | 1 / 3 |
| aDOT | 6.3 | 8.7 |
| 15+ air att (cmp) | 3 (2) | 5 (2) |
| behind LOS | 3 | 6 |
| 3rd-down dropbacks -> conv | 7 -> 2 | 9 -> 5 |
| targets | JSN 10, Kupp 3, Russell 2, Barner 2, Shaheed 2, Price 2, Holani 1 | JSN 11, Shaheed 6, Kupp 2, Price 2, 5 others 1 |
| catches-yds | JSN 7-109, Kupp 2-35 | JSN 9-155, Shaheed 3-35, Kupp 2-20 |
Lock rush: 2 runs wk1, 0 wk2 (pbp). Totals match CBS/PFT (35/48, 422, 4 TD, 0 INT).
Wk2 SEA drives (10): TD 4, punt 2, turnover on downs 2, turnover 1, FG 1. Run/pass wk2: 67 plays, 40.3% pass (53.7% neutral) — 40 runs: E.Wilson 21, Price 13, Holani 4.
Note: pbp posteam_score_post max shows 30 for wk2 (final 31 per news; last score not captured by that column).

## 2) Milroe
- 2026 regular season: **0 snaps with a pass or rush in pbp wks 1-8** (no throws, no designed runs).
- 2026 preseason (seahawks.com/footballdb): 3 GP, 27/45 (60.0%), 311 yds, 6.9 Y/A, 1 TD, 2 INT, **6 sacks** (59 yds), rtg 69.8; rush 13-72 (5.5), long 20, 0 TD. Game log bits (FOX): @KC 16/26 223; 8/23 @TEN 6/11 52 2 INT; vs DAL 5/8 36.
- 2025 regular season/preseason: NOT pulled this run (gap — unsourced, don't use). Designed-run vs scramble split: not in public box scores (gap).
- Read: sack-prone (6 sk / 51 dropbacks ≈ 11.8%, preseason), 13 rushes on ~64 plays ≈ runs on ~20% of his snaps. ESTIMATE if he starts: 7-10 QB rushes, 40-60 rush yds, ~25 att, sacks 3+.

## 3) SEA offense: Lock wks1-2 vs Darnold wks3-8 (pbp)
| wk | plays | pass% | neutral pass% | sec/play |
|---|---|---|---|---|
|1|47|.553|.480|68.9|
|2 (Lock)|67|.403|.537|51.1|
|3|64|.719|.674|53.4|
|4|56|.446|.480|62.0|
|5|60|.567|.538|58.1|
|6|81|.679|.579|44.3|
|7|69|.406|.424|49.0|
|8|57|.667|.591|60.6|
Rush att by wk (RBs): wk2 E.Wilson 21/Price 13/Holani 4; wk7 Wilson 24, Holani 5, V.Jones 5; **wk8 Price 10, Charbonnet 6, Holani 1, Wilson 0** (Charbonnet back; trailing script).
Target share — Lock throws vs Darnold wks3-8: JSN 43.8% vs 33.5%; Shaheed 16.7 vs 11.0 (Shaheed OUT now); Kupp 10.4 vs 12.5; Barner 6.2 vs 15.5; Horton 0 vs 8.5 (7 tgts wk8); Price 8.3 vs 3.5; Holani 4.2 vs 6.0. Lock = more concentrated on JSN; tiny sample (48 att).
SEA injury (10/31 report, last week): Cross T OUT, Shaheed OUT, V.Jones OUT, Bradford G Q. This week's list not out yet.

## 4) ARI defense (pbp wks 1-8)
Pts allowed by wk: 14, 30(SEA), 35, 27, 45, 15, 30, 30. Rush yds allowed: 81,162(SEA),141,89,163,92,161,94. Sacks 23 total; sack% 7.6, qb_hit% 14.3; EPA/play allowed +0.073, rush EPA −0.088.
Wk2 vs SEA: 235 pass, 162 rush (4.05 ypc), 1 sack.
Current ARI D injuries (BetIQ 10/30 = last week's report; this week's not out): DT Walter Nolen III ankle OUT/Q (ESPN: Q), CB Max Melton knee Q, S Andrew Wingard knee Q; CB Will Johnson IR (neck), DT Kaleb Proctor IR, DT Zachary Carter IR. Wed report pending.

## 5) Implications (ESTIMATES)
- **Spread SEA −11.5 (stale, pre-news): lean ARI / pass on SEA.** Lock base is still competent (wk2 9.0 YPA vs this D) but elbow-limited throwing volume + Cross out + Shaheed out; Milroe branch is a big downgrade. ESTIMATE fair ~SEA −8 to −9.5 (Lock), −5 to −6 (Milroe). Don't bet until line moves/settles.
- **Total 41.5: lean under** both branches (run-heavier script, wk2 pass rate 40%). No bet until re-line.
- **Rush-under baseline candidates:** ARI RBs (Allgeier/Knight — Knight concussion protocol; Love/Conner IR) vs SEA run D: candidate, needs lines. SEA RB unders NOT recommended — run share rises with backup QB; Price/Charbonnet split unclear post-Charbonnet return (wk8 10/6) => hold, role risk. Milroe rush UNDER = no (rush overs his profile).
- **Hold SEA pass-catcher legs:** hold ALL until Friday status (Lock throw volume). If Lock confirmed full: JSN receptions/yds are the only ones with support (43.8% Lock share); Kupp/Barner/Horton = hold (low Lock share, small sample). If Milroe: kill all SEA pass-catcher overs; JSN unders become candidates.
- Passing-yards legs banned; no TD legs.
## Gaps
2025 Milroe data; designed-run split; ARI coverage/blitz rates (not in pbp); this week's injury reports; no odds pulled (no credits used).
