# GB @ LAR postgame log and grades (Wed Nov 25, 2026)

**Final: Rams 26, Packers 13** (LAR 6-7-7-6, GB 3-10-0-0). Source: ESPN game summary (`GB_LA_espn_summary_final.json`).
Rams 373 yds (241 rushing), possession 40:40. Packers 244 yds, 3 turnovers (2 INT, 1 fumble), 29 passes. Watson hurt in the 3rd quarter.

## Key box lines
| Player | Line |
|---|---|
| Blake Corum | 32 carries, 184 yds, TD; 2 catches, 21 yds |
| Kyren Williams | 12-46, TD; 4 catches, 19 yds |
| Konata Mumpfield | 4 catches (5 tgts), 69 yds |
| Tyler Higbee / Colby Parkinson | 1-14 (3 tgts) / 2 for -1 |
| Matthew Golden | **1 catch (5 tgts), 39 yds** |
| Christian Watson | 4-65, TD (4 tgts; hurt) |
| Tucker Kraft | 3-24 (5 tgts) |
| Chris Brooks | 4-22 (5 tgts) |
| Kaleb Johnson | 8-13 rushing; 1-19 |
| Savion Williams / MarShawn Lloyd | 1-3 receiving, 2-18 rushing / 1-6 receiving |
| Jordan Love | 17/29, 198, 1 TD, 2 INT, 1 sack |

## Owner's slip (7-leg SGP, +618 boosted): 6 of 7, lost on Golden
| Leg | Result |
|---|---|
| Golden 4+ catches | **LOSS** (1) |
| Watson 3+ catches | WIN (4) |
| Kraft 3+ catches | WIN (3) |
| Mumpfield 3+ catches | WIN (4) |
| Corum 40+ rushing | WIN (184) |
| Kyren or Corum TD | WIN (both) |
| Under 58.5 | WIN (39) |
The earlier version of the slip would also have gone 6 of 7 (Golden the miss; Corum 50+ rush+rec, Higbee under 3.5, Watson 50+ all won).

## Our final read (dashboard), graded
| Read | Result |
|---|---|
| Corum over 1.5 catches | WIN (2) |
| Higbee under 31.5 yds | WIN (14) |
| Corum over 57.5 rushing | WIN (184) |
| Kyren under 54.5 rushing | WIN (46) |
| Higbee under 3.5 catches / Parkinson under 20.5 yds | WIN (1 / -1) |
| Atwell over 1.5 catches | no stat recorded (did not appear in the box score) |
| Golden 4+ catches | LOSS (1) |
| Kraft over 3.5 catches | LOSS (3) |
| Watson over 4.5 catches | LOSS (4; injured) |
| Savion Williams over 18.5 rec yds | LOSS (3) |
| Lloyd over 8.5 rec yds / 1.5 catches | LOSS (6 / 1) |
**5 wins, 5 losses, 1 no-stat.** Avoids that saved us: Watson 73.5 yds (65), Mumpfield under (4 catches, 69), Kraft yards.

## What we learned
1. **The run read was the best read.** Corum 184 on 32 carries: the Rams leaned on the run without Nacua/Adams and Green Bay's run defense (21st) gave way once the Rams led. We called Corum over and the Kyren/Corum split right; the board's model had both rushing unders at 27% over (model miss on role, as the audit warned).
2. **Golden: the per-game WR1 evidence was right; the slot-volume switch was wrong.** WR1s vs the Rams averaged 3.3 catches (under usual in 6 of 9) and McDuffie/Forbes allow under 3 yds/target. We had Golden catches as a pass, then moved to 4+ after the outside video's slot claim. Lesson: weight direct game-by-game results against a defense over an outside alignment claim we cannot verify (route charts would have settled it).
3. **Green Bay's back receiving went to Chris Brooks (4 catches), not Lloyd.** The leak to backs was real; we picked the wrong back.
4. **Game script decided the rest.** Rams 40:40 possession: Green Bay had 29 passes, 3 turnovers, Watson hurt. Low pass volume sank the Savion, Kraft 3.5 and Lloyd overs.
5. **The quick-throw read held early** (Love 12/18, 0 sacks in the 1st half) but the turnovers and Rams ball control limited volume.

Research only. Each read above was written before kickoff (reads.json history, commits 388253d9 to dedf49e2).
