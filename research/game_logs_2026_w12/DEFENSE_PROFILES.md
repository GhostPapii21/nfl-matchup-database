# Defensive coverage profiles from Week 12 games (GB@LAR) (built 2026-11-26 03:42 AM EST by Blitz, refs NFL-56)

Sources: ESPN summary JSON play text (per game, pull time in each game file), ESPN team rosters for names/positions, official NFL YouTube highlight auto-captions where noted (labeled video). No PFF/FTN paid content.
**Evidence levels:** VERIFIED = play text names the defender who broke up/intercepted the pass or was flagged for DPI. tackler = defender named as tackler on a completion (not proof of coverage). video = a highlight-commentary mention (auto-captions; names can be misspelled). Man/zone, blitz and MOF shell per play are **unknown** in free data.

## Season coverage rates, all 32 teams (public; StatRankings primary, Sharp cross-check; never mixed)

StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST. Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST. Copies of the source CSV and source log: sources/team_coverage_rates.csv, sources/COVERAGE_SOURCES.md.

| Team | Man SR / Sharp | Zone SR / Sharp | MOF closed SR / Sharp | MOF open SR / Sharp | Blitz SR / Sharp | Flags |
|---|---|---|---|---|---|---|
| ARI | 29.6% / 10.8% | 70.4% / 81.2% | 44.1% / 33.6% | 55.9% / 60.1% | 35.3% / 30.2% | 7+ pts: Man +18.8, Zone -10.8, MOF closed (single-high) +10.5 ; OUTLIER: MOF closed (single-high) |
| ATL | 37.6% / 21.9% | 62.1% / 70.8% | 60.2% / 60.7% | 39.8% / 33.5% | 26.6% / 23.3% | 7+ pts: Man +15.7, Zone -8.7 |
| BAL | 29.4% / 15.3% | 70.6% / 77.9% | 43.6% / 38.4% | 56.4% / 59.0% | 34.6% / 31.4% | 7+ pts: Man +14.1, Zone -7.3 |
| BUF | 27.5% / 17.9% | 72.3% / 74.7% | 48.4% / 46.5% | 51.6% / 49.2% | 38.0% / 28.9% | 7+ pts: Man +9.6, Blitz +9.1 ; OUTLIER: Blitz |
| CAR | 25.5% / 10.1% | 74.5% / 84.7% | 59.2% / 57.0% | 40.8% / 39.0% | 34.5% / 34.4% | 7+ pts: Man +15.4, Zone -10.2 |
| CHI | 36.2% / 27.2% | 63.4% / 68.8% | 50.7% / 50.5% | 49.3% / 45.8% | 38.6% / 32.4% | 7+ pts: Man +9.0 ; OUTLIER: Man |
| CIN | 45.4% / 27.4% | 53.4% / 65.9% | 58.4% / 54.0% | 41.6% / 41.7% | 18.1% / 16.7% | 7+ pts: Man +18.0, Zone -12.5 |
| CLE | 54.8% / 44.4% | 44.6% / 51.5% | 68.6% / 72.3% | 31.4% / 24.5% | 29.6% / 28.5% | 7+ pts: Man +10.4 |
| DAL | 46.7% / 23.4% | 51.9% / 68.5% | 59.6% / 57.8% | 40.4% / 37.9% | 26.2% / 20.4% | 7+ pts: Man +23.3, Zone -16.6 |
| DEN | 45.6% / 25.1% | 52.8% / 70.2% | 56.4% / 48.6% | 43.6% / 47.5% | 35.2% / 33.9% | 7+ pts: Man +20.5, Zone -17.4, MOF closed (single-high) +7.8 |
| DET | 38.2% / 19.5% | 59.2% / 75.6% | 60.7% / 49.4% | 39.3% / 47.8% | 30.4% / 22.2% | 7+ pts: Man +18.7, Zone -16.4, MOF closed (single-high) +11.3, MOF open (two-high) -8.5, Blitz +8.2 ; OUTLIER: Zone, MOF closed (single-high), MOF open (two-high), Blitz |
| GB | 24.1% / 13.5% | 75.4% / 78.5% | 36.5% / 34.7% | 63.5% / 61.0% | 36.8% / 33.3% | 7+ pts: Man +10.6 |
| HOU | 31.9% / 13.9% | 67.8% / 81.8% | 52.1% / 55.6% | 47.9% / 43.0% | 24.5% / 23.5% | 7+ pts: Man +18.0, Zone -14.0 ; OUTLIER: Zone |
| IND | 44.3% / 24.0% | 55.5% / 69.7% | 56.0% / 49.1% | 44.0% / 46.4% | 22.7% / 21.6% | 7+ pts: Man +20.3, Zone -14.2 |
| JAX | 26.2% / 17.2% | 73.8% / 77.7% | 47.5% / 45.8% | 52.5% / 51.2% | 32.6% / 27.4% | 7+ pts: Man +9.0 |
| KC | 43.8% / 18.4% | 55.0% / 77.9% | 46.8% / 39.9% | 53.2% / 57.3% | 28.6% / 27.1% | 7+ pts: Man +25.4, Zone -22.9 ; OUTLIER: Zone |
| LAC | 32.7% / 13.4% | 67.0% / 74.5% | 50.4% / 44.6% | 49.6% / 50.5% | 26.2% / 23.9% | 7+ pts: Man +19.3, Zone -7.5 ; OUTLIER: Man |
| LAR | 40.1% / 22.3% | 59.3% / 70.8% | 45.7% / 37.8% | 54.3% / 57.9% | 30.4% / 26.6% | 7+ pts: Man +17.8, Zone -11.5, MOF closed (single-high) +7.9 |
| LV | 34.2% / 21.9% | 65.8% / 69.4% | 48.8% / 47.5% | 51.2% / 47.5% | 30.2% / 24.9% | 7+ pts: Man +12.3 |
| MIA | 25.7% / 15.0% | 74.3% / 76.4% | 47.9% / 42.6% | 52.1% / 51.9% | 24.3% / 19.3% | 7+ pts: Man +10.7 |
| MIN | 26.7% / 5.2% | 73.0% / 86.9% | 40.3% / 28.2% | 59.7% / 65.6% | 74.4% / 69.2% | 7+ pts: Man +21.5, Zone -13.9, MOF closed (single-high) +12.1 ; OUTLIER: MOF closed (single-high) |
| NE | 30.3% / 27.6% | 67.7% / 66.6% | 51.9% / 48.5% | 48.1% / 47.6% | 38.1% / 35.8% |  ; OUTLIER: Man, Zone |
| NO | 38.2% / 16.7% | 59.6% / 73.9% | 64.9% / 64.3% | 35.1% / 31.8% | 39.1% / 33.9% | 7+ pts: Man +21.5, Zone -14.3 |
| NYG | 47.2% / 25.6% | 52.1% / 69.1% | 52.5% / 47.9% | 47.5% / 49.4% | 42.9% / 38.4% | 7+ pts: Man +21.6, Zone -17.0 |
| NYJ | 38.5% / 26.8% | 61.5% / 63.7% | 46.3% / 46.1% | 53.7% / 48.8% | 40.4% / 38.3% | 7+ pts: Man +11.7 |
| PHI | 38.1% / 18.2% | 61.9% / 73.1% | 58.1% / 52.1% | 41.9% / 41.6% | 29.8% / 25.1% | 7+ pts: Man +19.9, Zone -11.2 |
| PIT | 17.7% / 11.9% | 81.8% / 81.3% | 45.3% / 43.6% | 54.7% / 51.4% | 28.2% / 27.3% |  |
| SEA | 20.7% / 9.8% | 79.3% / 85.4% | 43.0% / 41.2% | 57.0% / 56.9% | 24.9% / 22.4% | 7+ pts: Man +10.9 |
| SF | 29.6% / 11.2% | 69.3% / 82.8% | 59.0% / 56.2% | 41.0% / 39.5% | 31.8% / 26.8% | 7+ pts: Man +18.4, Zone -13.5 |
| TB | 31.1% / 16.2% | 68.3% / 79.2% | 64.6% / 62.0% | 35.4% / 36.5% | 45.4% / 42.2% | 7+ pts: Man +14.9, Zone -10.9 |
| TEN | 27.7% / 17.4% | 71.4% / 75.3% | 45.5% / 48.8% | 54.5% / 47.1% | 24.9% / 23.7% | 7+ pts: Man +10.3, MOF open (two-high) +7.4 ; OUTLIER: MOF closed (single-high), MOF open (two-high) |
| WSH | 19.4% / 13.8% | 80.3% / 77.6% | 38.3% / 33.4% | 61.7% / 60.7% | 44.2% / 40.4% |  ; OUTLIER: Zone |

**Systematic gap between the sources** (definitions differ; this is why they are never averaged):

| Rate | Median gap (StatRankings - Sharp) | SD of gap | Teams where StatRankings is higher |
|---|---|---|---|
| Man | +15.6 pts | 5.6 | 32/32 |
| Zone | -9.4 pts | 6.1 | 3/32 |
| MOF closed (single-high) | +2.7 pts | 3.9 | 28/32 |
| MOF open (two-high) | +0.8 pts | 3.7 | 20/32 |
| Blitz | +3.4 pts | 2.2 | 32/32 |

Because StatRankings man is higher than Sharp for all 32 teams, a raw 7+ point man gap is common. The OUTLIER flag marks gaps 2+ SD from the league-median gap, or ranks 10+ apart, which is the disagreement worth checking.

## GB defense vs LAR (GB@LAR, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Keisean Nixon | CB | 6 | 6 | 52 | 0 | 0 | 0 | 0 | tackler x6 | K.Williams 1, D.Allen 2, X.Smith 1, K.Mumpfield 2 | K.Mumpfield 20 deep_right Q3 |
| Evan Williams | S | 2 | 2 | 29 | 0 | 0 | 0 | 0 | tackler x2 | K.Mumpfield 1, T.Higbee 1 |  |
| Xavier McKinney | S | 2 | 2 | 25 | 0 | 0 | 0 | 0 | tackler x2 | K.Williams 1, K.Mumpfield 1 | K.Mumpfield 24 deep_right Q2 |
| Ty'Ron Hopper | LB | 3 | 2 | 19 | 0 | 0 | 1 | 0 | VERIFIED x1, tackler x2 | K.Williams 1, T.Higbee 1, B.Corum 1 |  |
| Isaiah McDuffie | LB | 3 | 3 | 14 | 0 | 0 | 0 | 0 | tackler x3 | K.Williams 1, B.Corum 1, C.Parkinson 1 |  |
| Devonte Wyatt | DT | 1 | 1 | 1 | 0 | 0 | 0 | 0 | tackler x1 | C.Parkinson 1 |  |
| Brandon Cisse | CB | 0 | 0 | 0 | 0 | 0 | 0 | 1 | VERIFIED x1 | X.Smith 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 5/6 for 73 yds, 0 TD; RB 6/8 for 40 yds, 0 TD; TE 5/7 for 27 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 2/1
Pass rush: sacks M.Parsons 1; QB hits I.McDuffie 1, M.Parsons 1, B.Cisse 2
Video (highlight transcript) mentions: none found / not checked
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### GB season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 24.1% | 13.5% |
| Zone | 75.4% | 78.5% |
| MOF closed (single-high) | 36.5% | 34.7% |
| MOF open (two-high) | 63.5% | 61.0% |
| Blitz | 36.8% | 33.3% |
| Cover 0 | 3.8% | not published |
| Cover 1 | unknown | not published |
| Cover 2 | 35.1% | not published |
| Cover 2-Man | 8.2% | not published |
| Cover 3 | 21.8% | not published |
| Cover 4 | 11.8% | not published |
| Cover 6 | unknown | not published |
| Cover 9 | unknown | not published |
| Coverage snaps | 390 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/gb). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 24.1% vs Sharp 13.5% (+10.6 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): none
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## LAR defense vs GB (GB@LAR, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Kam Curl | S | 2 | 2 | 71 | 0 | 0 | 0 | 0 | tackler x2 | C.Watson 1, M.Golden 1 | C.Watson 32 short_left Q1; M.Golden 39 deep_right Q2 |
| Trent McDuffie | CB | 3 | 2 | 31 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x2 | K.Johnson 1, M.Golden 1, B.Melton 1 |  |
| Emmanuel Forbes Jr. | CB | 4 | 3 | 22 | 0 | 0 | 1 | 0 | VERIFIED x1, tackler x3 | S.Williams 1, B.Melton 2, C.Brooks 1 |  |
| Quentin Lake | S | 4 | 2 | 13 | 0 | 2 | 0 | 0 | VERIFIED x2, tackler x2 | M.Golden 1, S.Williams 1, T.Kraft 1, C.Brooks 1 |  |
| Omar Speights | LB | 2 | 2 | 12 | 0 | 0 | 0 | 0 | tackler x2 | T.Kraft 1, M.Lloyd 1 |  |
| Nate Landman | LB | 1 | 1 | 10 | 0 | 0 | 0 | 0 | tackler x1 | T.Kraft 1 |  |
| Josh Wallace | CB | 1 | 1 | 6 | 0 | 0 | 0 | 0 | tackler x1 | C.Watson 1 |  |
| Josaiah Stewart | LB | 2 | 2 | 6 | 0 | 0 | 0 | 0 | tackler x2 | C.Brooks 2 |  |
| Kamren Kinchens | S | 2 | 0 | 0 | 0 | 2 | 0 | 0 | VERIFIED x2 | J.Sturdivant 1, T.Kraft 1 |  |
| Aaron Donald | DT | 1 | 0 | 0 | 0 | 1 | 0 | 0 | VERIFIED x1 | K.Johnson 1 |  |
| Jaylen McCollough | S | 1 | 0 | 0 | 0 | 0 | 1 | 0 | VERIFIED x1 | M.Golden 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 8/16 for 127 yds, 1 TD; RB 6/8 for 47 yds, 0 TD; TE 3/5 for 24 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 3/0
Pass rush: sacks B.Young 1; QB hits M.Garrett 2
Video (highlight transcript) mentions: none found / not checked
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### LAR season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 40.1% | 22.3% |
| Zone | 59.3% | 70.8% |
| MOF closed (single-high) | 45.7% | 37.8% |
| MOF open (two-high) | 54.3% | 57.9% |
| Blitz | 30.4% | 26.6% |
| Cover 0 | 4.5% | not published |
| Cover 1 | 28.8% | not published |
| Cover 2 | 28.5% | not published |
| Cover 2-Man | 6.8% | not published |
| Cover 3 | unknown | not published |
| Cover 4 | 9.2% | not published |
| Cover 6 | 5.6% | not published |
| Cover 9 | 2.4% | not published |
| Coverage snaps | 337 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/lar). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 40.1% vs Sharp 22.3% (+17.8 pts); Zone: StatRankings 59.3% vs Sharp 70.8% (-11.5 pts); MOF closed (single-high): StatRankings 45.7% vs Sharp 37.8% (+7.9 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): none
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

