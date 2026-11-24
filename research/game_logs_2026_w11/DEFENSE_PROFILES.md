# Defensive coverage profiles from Week 11 games (built 2026-11-24 01:05 AM EST by Blitz, refs NFL-56)

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

## ARI defense vs KC (ARI@KC, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Kei'Trel Clark | CB | 4 | 4 | 63 | 0 | 0 | 0 | 0 | tackler x4 | R.Rice 1, J.Downs 2, E.Johnson 1 | J.Downs 26 short_left Q2 |
| Jack Gibbens | LB | 4 | 4 | 50 | 0 | 0 | 0 | 0 | tackler x4 | E.Johnson 1, N.Gray 1, C.Allen 1, X.Worthy 1 | X.Worthy 20 short_middle Q3 |
| Budda Baker | S | 3 | 3 | 27 | 0 | 0 | 0 | 0 | tackler x3 | T.Kelce 1, N.Gray 2 |  |
| Kalen King | CB | 2 | 2 | 26 | 0 | 0 | 0 | 0 | tackler x2 | R.Rice 1, J.Downs 1 |  |
| Denzel Burke | CB | 3 | 2 | 19 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x2 | T.Kelce 2, A.Armstrong 1 |  |
| Ma.Wilson (name unresolved) | unknown | 3 | 3 | 19 | 0 | 0 | 0 | 0 | tackler x3 | J.Downs 1, R.Rice 2 |  |
| Zaven Collins | LB | 2 | 2 | 14 | 0 | 0 | 0 | 0 | tackler x2 | R.Rice 1, E.Johnson 1 |  |
| Roy Lopez | DT | 2 | 1 | 12 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | N.Gray 1, T.Kelce 1 |  |
| W.Williams (name unresolved) | unknown | 1 | 1 | 11 | 0 | 0 | 0 | 0 | tackler x1 | R.Rice 1 |  |
| Cody Simon | LB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | tackler x1 | E.Johnson 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 14/21 for 191 yds, 1 TD; TE 9/12 for 95 yds, 2 TD; RB 4/4 for 38 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 4/2
Pass rush: sacks W.Nolen 1; QB hits J.Sweat 2, J.Gibbens 1, D.Robinson 1
Video (highlight transcript) mentions: none found / not checked
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### ARI season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 29.6% | 10.8% |
| Zone | 70.4% | 81.2% |
| MOF closed (single-high) | 44.1% | 33.6% |
| MOF open (two-high) | 55.9% | 60.1% |
| Blitz | 35.3% | 30.2% |
| Cover 0 | 3.3% | not published |
| Cover 1 | 18.9% | not published |
| Cover 2 | 28.7% | not published |
| Cover 2-Man | 7.5% | not published |
| Cover 3 | 22.5% | not published |
| Cover 4 | 8.5% | not published |
| Cover 6 | 7.8% | not published |
| Cover 9 | 1.6% | not published |
| Coverage snaps | 307 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/ari). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 29.6% vs Sharp 10.8% (+18.8 pts); Zone: StatRankings 70.4% vs Sharp 81.2% (-10.8 pts); MOF closed (single-high): StatRankings 44.1% vs Sharp 33.6% (+10.5 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): MOF closed (single-high): gap +10.5 pts is +7.8 vs the median gap; rank 27 StatRankings vs 30 Sharp
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## KC defense vs ARI (ARI@KC, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Drue Tranquill | LB | 4 | 4 | 38 | 0 | 0 | 0 | 0 | tackler x4 | H.Long 1, T.McBride 2, H.Wallace 1 |  |
| Jadon Canady | CB | 2 | 2 | 35 | 0 | 0 | 0 | 0 | tackler x2 | H.Wallace 2 | H.Wallace 25 deep_left Q2 |
| Jack Cochrane | LB | 1 | 1 | 17 | 0 | 0 | 0 | 0 | tackler x1 | Z.Jones 1 |  |
| Kristian Fulton | CB | 3 | 2 | 13 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x2 | T.McBride 2, S.Fehoko 1 |  |
| Nick Bolton | LB | 2 | 1 | 12 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | H.Wallace 2 |  |
| Nohl Williams | CB | 4 | 2 | 10 | 0 | 2 | 0 | 0 | VERIFIED x2, tackler x2 | E.Higgins 1, T.McBride 1, S.Fehoko 1, H.Wallace 1 |  |
| Ashton Gillotte | DE | 1 | 1 | 10 | 0 | 0 | 0 | 0 | tackler x1 | Z.Knight 1 |  |
| Jaden Hicks | S | 1 | 1 | 8 | 0 | 0 | 0 | 0 | tackler x1 | T.McBride 1 |  |
| Jeffrey Bassa | LB | 1 | 1 | 7 | 0 | 0 | 0 | 0 | tackler x1 | T.McBride 1 |  |
| Chris Roland-Wallace | CB | 1 | 1 | 3 | 0 | 0 | 0 | 0 | tackler x1 | T.McBride 1 |  |
| Chris Jones | DT | 1 | 0 | 0 | 0 | 1 | 0 | 0 | VERIFIED x1 | T.McBride 1 |  |
| Felix Anudike-Uzomah | DE | 1 | 1 | 0 | 0 | 0 | 0 | 0 | tackler x1 | T.McBride 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 6/14 for 76 yds, 1 TD; TE 11/16 for 69 yds, 0 TD; RB 1/1 for 10 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 1/0
Pass rush: sacks G.Karlaftis (half) 1, C.Jones (half) 1, G.Karlaftis 2; QB hits N.Williams 1, G.Karlaftis 3
Video (highlight transcript) mentions: none found / not checked
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### KC season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 43.8% | 18.4% |
| Zone | 55.0% | 77.9% |
| MOF closed (single-high) | 46.8% | 39.9% |
| MOF open (two-high) | 53.2% | 57.3% |
| Blitz | 28.6% | 27.1% |
| Cover 0 | 5.3% | not published |
| Cover 1 | 24.3% | not published |
| Cover 2 | unknown | not published |
| Cover 2-Man | 14.2% | not published |
| Cover 3 | unknown | not published |
| Cover 4 | 14.2% | not published |
| Cover 6 | unknown | not published |
| Cover 9 | unknown | not published |
| Coverage snaps | 338 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/kc). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 43.8% vs Sharp 18.4% (+25.4 pts); Zone: StatRankings 55.0% vs Sharp 77.9% (-22.9 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): Zone: gap -22.9 pts is -13.5 vs the median gap; rank 27 StatRankings vs 11 Sharp
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## BAL defense vs CAR (BAL@CAR, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Kyle Hamilton | S | 5 | 5 | 85 | 0 | 0 | 0 | 0 | tackler x5 | T.McMillan 2, M.Evans 1, J.Coker 1, D.Waller 1 | J.Coker 35 deep_left Q1; T.McMillan 29 deep_right Q3 |
| T.J. Tampa | CB | 2 | 1 | 27 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | D.Waller 1, J.Coker 1 | D.Waller 27 deep_middle Q3 |
| Malaki Starks | S | 2 | 2 | 25 | 0 | 0 | 0 | 0 | tackler x2 | J.Coker 1, J.Metchie 1 |  |
| Trenton Simpson | LB | 1 | 1 | 18 | 0 | 0 | 0 | 0 | tackler x1 | T.Tremble 1 |  |
| Roquan Smith | LB | 2 | 2 | 16 | 0 | 0 | 0 | 0 | tackler x2 | M.Evans 1, T.McMillan 1 |  |
| Chidobe Awuzie | CB | 2 | 2 | 15 | 0 | 0 | 0 | 0 | tackler x2 | D.Waller 1, T.Etienne 1 |  |
| Nate Wiggins | CB | 3 | 2 | 13 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x2 | M.Evans 1, J.Coker 2 |  |
| K'Von Wallace | CB | 1 | 1 | 13 | 0 | 0 | 0 | 0 | tackler x1 | T.McMillan 1 |  |
| Keyon Martin | CB | 2 | 2 | 6 | 0 | 0 | 0 | 0 | tackler x2 | T.McMillan 1, M.Evans 1 |  |
| Mike Green | LB | 1 | 1 | 6 | 0 | 0 | 0 | 0 | tackler x1 | B.Tremayne 1 |  |
| Trey Hendrickson | LB | 1 | 0 | 0 | 0 | 1 | 0 | 0 | VERIFIED x1 | T.McMillan 1 |  |
| David Olajiga | DT | 1 | 1 | 0 | 0 | 0 | 0 | 0 | tackler x1 | J.Coker 1 |  |
| Calais Campbell | DE | 1 | 0 | 0 | 0 | 1 | 0 | 0 | VERIFIED x1 | T.McMillan 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 12/19 for 143 yds, 1 TD; TE 9/9 for 104 yds, 1 TD; RB 1/1 for 7 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 4/3
Pass rush: sacks M.Green 2, T.Jones 1; QB hits T.Hendrickson 1, C.Campbell 1, D.Olajiga 1, R.Smith 1
Video (highlight transcript) mentions: none found / not checked
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### BAL season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 29.4% | 15.3% |
| Zone | 70.6% | 77.9% |
| MOF closed (single-high) | 43.6% | 38.4% |
| MOF open (two-high) | 56.4% | 59.0% |
| Blitz | 34.6% | 31.4% |
| Cover 0 | 7.6% | not published |
| Cover 1 | unknown | not published |
| Cover 2 | 30.9% | not published |
| Cover 2-Man | 7.6% | not published |
| Cover 3 | 24.8% | not published |
| Cover 4 | 5.5% | not published |
| Cover 6 | 6.1% | not published |
| Cover 9 | 3.4% | not published |
| Coverage snaps | 327 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/bal). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 29.4% vs Sharp 15.3% (+14.1 pts); Zone: StatRankings 70.6% vs Sharp 77.9% (-7.3 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): none
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## CAR defense vs BAL (BAL@CAR, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Tre'von Moehrig | S | 2 | 2 | 40 | 0 | 0 | 0 | 0 | tackler x2 | D.Henry 1, D.Walker 1 | D.Walker 34 deep_right Q2 |
| Zakee Wheatley | S | 3 | 3 | 38 | 0 | 0 | 0 | 0 | tackler x3 | Z.Flowers 3 | Z.Flowers 25 deep_middle Q2 |
| W.Lee (name unresolved) | unknown | 3 | 2 | 32 | 0 | 1 | 0 | 1 | VERIFIED x2, tackler x2 | J.Lane 1, Z.Flowers 1, D.Henry 2 | Z.Flowers 26 short_left Q2 |
| Tyrel Dodson | LB | 4 | 4 | 23 | 0 | 0 | 0 | 0 | tackler x4 | M.Hibner 1, J.Hill 2, M.Andrews 1 |  |
| Chau Smith-Wade | CB | 3 | 2 | 23 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x2 | J.Hill 1, R.Bateman 1, Z.Flowers 1 |  |
| Mike Jackson | CB | 4 | 2 | 19 | 0 | 2 | 0 | 0 | VERIFIED x2, tackler x2 | R.Bateman 2, Z.Flowers 2 |  |
| Devin Lloyd | LB | 2 | 2 | 16 | 0 | 0 | 0 | 0 | tackler x2 | Z.Flowers 1, J.Hill 1 |  |
| P.Jones (name unresolved) | unknown | 2 | 2 | 16 | 0 | 0 | 0 | 0 | tackler x2 | M.Hibner 1, J.Cuevas 1 |  |
| Derrick Brown | DT | 3 | 2 | 5 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x2 | D.Henry 1, Z.Flowers 2 |  |

Yards allowed by target position (WR slot/outside unknown): WR 11/17 for 198 yds, 1 TD; RB 7/10 for 41 yds, 0 TD; TE 5/8 for 34 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 4/4
Pass rush: sacks P.Umanmielen (half) 1, D.Lloyd (half) 2, T.Gipson (half) 1, P.Umanmielen 1; QB hits T.Wharton 2, P.Jones 1
Video (highlight transcript) mentions: none found / not checked
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### CAR season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 25.5% | 10.1% |
| Zone | 74.5% | 84.7% |
| MOF closed (single-high) | 59.2% | 57.0% |
| MOF open (two-high) | 40.8% | 39.0% |
| Blitz | 34.5% | 34.4% |
| Cover 0 | 3.6% | not published |
| Cover 1 | 21.2% | not published |
| Cover 2 | 20.9% | not published |
| Cover 2-Man | unknown | not published |
| Cover 3 | 34.5% | not published |
| Cover 4 | 7.3% | not published |
| Cover 6 | 9.7% | not published |
| Cover 9 | 1.8% | not published |
| Coverage snaps | 330 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/car). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 25.5% vs Sharp 10.1% (+15.4 pts); Zone: StatRankings 74.5% vs Sharp 84.7% (-10.2 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): none
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## CIN defense vs WSH (CIN@WSH, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Josh Newton | CB | 5 | 4 | 88 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x4 | S.Diggs 3, T.Burks 1, C.Okonkwo 1 | C.Okonkwo 32 deep_middle Q2; S.Diggs 29 deep_middle Q4 |
| DJ Turner II | CB | 5 | 5 | 74 | 0 | 0 | 0 | 0 | tackler x5 | A.Ekeler 1, T.Burks 1, C.Okonkwo 1, S.Diggs 1, A.Williams 1 | A.Williams 42 deep_middle Q4 |
| Bryan Cook | S | 2 | 2 | 35 | 0 | 0 | 0 | 0 | tackler x2 | C.Okonkwo 1, A.Williams 1 | A.Williams 22 deep_middle Q4 |
| Dax Hill | CB | 2 | 2 | 22 | 0 | 0 | 0 | 1 | VERIFIED x1, tackler x2 | A.Ekeler 1, T.Burks 1, A.Williams 1 | A.Williams 20 short_middle Q4 |
| Barrett Carter | LB | 3 | 3 | 22 | 0 | 0 | 0 | 0 | tackler x3 | J.Croskey-Merritt 1, S.Diggs 1, A.Williams 1 |  |
| Jordan Battle | S | 2 | 2 | 18 | 0 | 0 | 0 | 0 | tackler x2 | A.Williams 2 |  |
| Demetrius Knight Jr. | LB | 3 | 3 | 16 | 0 | 0 | 0 | 0 | tackler x3 | A.Williams 1, C.Okonkwo 1, J.Croskey-Merritt 1 |  |
| Cedric Johnson | DE | 1 | 1 | 8 | 0 | 0 | 0 | 0 | tackler x1 | A.Williams 1 |  |
| Myles Murphy | DE | 1 | 1 | 6 | 0 | 0 | 0 | 0 | tackler x1 | A.Williams 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 15/21 for 197 yds, 0 TD; TE 4/5 for 66 yds, 0 TD; RB 4/6 for 26 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 5/2
Pass rush: sacks B.Mafe 3; QB hits D.Lawrence 1, J.Allen 1
Video (highlight transcript) mentions: Dax Hill (CB) @9:30 ">> Joe: THIRD DOWN AND FOUR. CONTACT, NO FLAGS. BURKS, COVERED BY DAX HILL. AND THE FIELD GOAL TEAM WILL BALL GAME. HERE IS A 40-YARD TRY NOW." [coverage word: COVERED]; Dax Hill (CB) @5:09 ">> Joe: THIRD DOWN AND FOUR. CONTACT, NO FLAGS. BURKS, COVERED BY DAX HILL. AND THE FIELD GOAL TEAM WILL CHAINS. >> Joe: HALF A MINUTE TO GO IN" [coverage word: COVERED]; Barrett Carter (LB) @6:19 "DIGGS. THIRD AND SHORT COMING UP, STRONG TACKLE BY BARRETT CARTER. SAW DIGGS FRUSTRATED ON THE HIGH SNAP. DANIELS, END ZONE, IT'S NOT" [coverage word: ZONE]; Boye Mafe (DE) @6:32 "THERE. WILLIAMS, THE CLOSEST ONE TO IT, BUT BIG-TIME PRESSURE BY BOYE MAFE, WHO HAS ALREADY GOT THREE ABLE TO KEEP THE SCORES DOWN, HAS BEEN DOWN IN THE RED ZONE." [coverage word: ZONE]
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### CIN season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 45.4% | 27.4% |
| Zone | 53.4% | 65.9% |
| MOF closed (single-high) | 58.4% | 54.0% |
| MOF open (two-high) | 41.6% | 41.7% |
| Blitz | 18.1% | 16.7% |
| Cover 0 | 4.2% | not published |
| Cover 1 | 34.6% | not published |
| Cover 2 | 25.1% | not published |
| Cover 2-Man | 6.6% | not published |
| Cover 3 | 18.5% | not published |
| Cover 4 | unknown | not published |
| Cover 6 | unknown | not published |
| Cover 9 | 2.4% | not published |
| Coverage snaps | 335 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/cin). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 45.4% vs Sharp 27.4% (+18.0 pts); Zone: StatRankings 53.4% vs Sharp 65.9% (-12.5 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): none
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## WSH defense vs CIN (CIN@WSH, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Jeremy Reaves | S | 5 | 4 | 91 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x4 | M.Gesicki 3, D.Sample 1, S.Perine 1 | S.Perine 44 short_middle Q2; M.Gesicki 32 deep_right Q4 |
| Frankie Luvu | LB | 5 | 5 | 38 | 0 | 0 | 0 | 0 | tackler x5 | S.Perine 2, J.Endries 3 |  |
| Rasul Douglas | CB | 7 | 5 | 29 | 0 | 2 | 0 | 0 | VERIFIED x2, tackler x5 | J.Chase 5, C.Young 1, C.Brown 1 |  |
| Sonny Styles | LB | 4 | 4 | 29 | 0 | 0 | 0 | 0 | tackler x4 | C.Brown 1, M.Gesicki 2, D.Meyers 1 |  |
| Quan Martin | S | 1 | 1 | 19 | 0 | 0 | 0 | 0 | tackler x1 | M.Gesicki 1 |  |
| Trey Amos | CB | 3 | 3 | 15 | 0 | 0 | 0 | 1 | VERIFIED x1, tackler x3 | C.Brown 1, J.Chase 2, J.Endries 1 |  |
| Nick Cross | S | 1 | 1 | 12 | 0 | 0 | 0 | 0 | tackler x1 | T.Higgins 1 |  |
| K'Lavon Chaisson | LB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | tackler x1 | C.Brown 1 |  |
| Mike Sainristil | CB | 1 | 1 | 6 | 0 | 0 | 0 | 0 | tackler x1 | C.Brown 1 |  |

Yards allowed by target position (WR slot/outside unknown): TE 10/12 for 119 yds, 0 TD; RB 9/12 for 101 yds, 0 TD; WR 9/15 for 80 yds, 2 TD; unknown 0/1 for 0 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 3/0
Pass rush: sacks T.Settle (half) 1, K.Chaisson (half) 1, T.Settle 1, N.Cross (half) 1, K.Medrano (half) 1; QB hits C.Omenihu 1, K.Chaisson 1, J.Josephs 2, F.Luvu 1
Video (highlight transcript) mentions: Nick Cross (S) @2:18 "SAFETIES AND CORNERS BOTH HAVE BEEN ATTACKING. >> Joe: NICK CROSS COMING ON THE BLITZ. BURROW IS ABLE TO FIND PERINE -- DROPPED IT!" [coverage word: BLITZ]; Trey Amos (CB) @5:37 "I MEAN HE MAKES THESE LOOK ROUTE. TREY AMOS IN COVERAGE, A LOOK AT THE END OF IT, ENDS UP CATCHING IT WITH ONE HAND, DOESN'T SUES HIS RIGHT HAND." [coverage word: COVERAGE]
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### WSH season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 19.4% | 13.8% |
| Zone | 80.3% | 77.6% |
| MOF closed (single-high) | 38.3% | 33.4% |
| MOF open (two-high) | 61.7% | 60.7% |
| Blitz | 44.2% | 40.4% |
| Cover 0 | 4.6% | not published |
| Cover 1 | unknown | not published |
| Cover 2 | 36.3% | not published |
| Cover 2-Man | 5.7% | not published |
| Cover 3 | 26.6% | not published |
| Cover 4 | 12.6% | not published |
| Cover 6 | unknown | not published |
| Cover 9 | 1.4% | not published |
| Coverage snaps | 350 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/was). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** none at 7+ pts
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): Zone: gap +2.7 pts is +12.2 vs the median gap; rank 2 StatRankings vs 13 Sharp
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## IND defense vs HOU (IND@HOU, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CJ Allen | LB | 6 | 6 | 41 | 0 | 0 | 0 | 0 | tackler x6 | X.Hutchinson 1, M.Klein 1, E.Demercado 2, K.Boutte 1, N.Collins 1 | K.Boutte 20 short_middle Q2 |
| Bryce Boettcher | LB | 2 | 2 | 12 | 0 | 0 | 0 | 0 | tackler x2 | M.Klein 1, F.Moreau 1 |  |
| Johnathan Edwards | CB | 1 | 1 | 11 | 0 | 0 | 0 | 0 | tackler x1 | D.Schultz 1 |  |
| Austin Ajiake | LB | 3 | 2 | 11 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x2 | N.Collins 1, D.Montgomery 2 |  |
| Arden Key | DE | 1 | 1 | 10 | 0 | 0 | 0 | 0 | tackler x1 | T.Dell 1 |  |
| Kapena Gushiken | CB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | tackler x1 | T.Dell 1 |  |
| A.J. Haulcy | S | 1 | 1 | 9 | 0 | 0 | 0 | 0 | tackler x1 | D.Montgomery 1 |  |
| Justin Walley | CB | 1 | 1 | 3 | 0 | 0 | 0 | 0 | tackler x1 | D.Montgomery 1 |  |
| Hunter Wohler | S | 1 | 1 | 3 | 0 | 0 | 0 | 0 | tackler x1 | M.Klein 1 |  |
| Caden Curry | LB | 1 | 1 | 2 | 0 | 0 | 0 | 0 | tackler x1 | X.Hutchinson 1 |  |
| Jaylahn Tuimoloau | DE | 1 | 0 | 0 | 0 | 1 | 0 | 0 | VERIFIED x1 | X.Hutchinson 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 10/13 for 142 yds, 2 TD; TE 6/6 for 43 yds, 1 TD; RB 5/6 for 13 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 3/2
Pass rush: sacks A.Adebawore 1; QB hits none
Video (highlight transcript) mentions: A.J. Haulcy (S) @1:44 "HAVE BEEN PICKED AFTER A DOUBLE TAP. AJ. HAULCY ABLE TO COME UP WITH IT. LOOKED LIKE IT WAS BATTED" [coverage word: PICKED]; Cam Bynum (S) @2:00 "HE'S RUNNING BACK. HE GOES OFF OF HIS HELMET. HE ENDS UP INTERCEPTING IT. GOES OFF OF BYNUM BACK TO INTERCEPTION. SECOND AND NINE." [coverage word: INTERCEPTING]; Cameron Ball (DT) @6:14 "IF HE MISSES THIS WITH HIS FIELD POSITION AND THE TEXANS GETTING THE BALL TO START THE SECOND HALF. YEAH, THEY GET THE BALL ON THE OTHER SIDE OF THE 50 AND" [coverage word: MISSES]; Austin Ajiake (LB) @7:17 "PRESSURE THROWS INCOMPLETE. INTENDED FOR MONTGOMERY. GOOD COVERAGE THAT TIME. AJIAKE IN THE MIDDLE. SO IT'S FOURTH DOWN AND SIX. IN COMES THE FIELD GOAL" [coverage word: COVERAGE]; Cam Bynum (S) @10:22 "AND MEANWHILE THE PRESSURE WAS PUT ON THAT TIME BLITZ COMING IN FORCING THAT THROW CAM BYNUM PUT IT ON. ALMOST HAD THAT PICK BEFORE BUT IT WAS OVERTURNED THAT" [coverage word: BLITZ]; Bryce Boettcher (LB) @11:40 "CORNER? HE CAN NOT. AND THAT TIME IT'S BRYCE BOETTCHER THE ROOKIE OUT OF OREGON WHO STOPS HIM TURNED THE BALL OVER ON DOWNS WITH" [coverage word: CORNER]
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### IND season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 44.3% | 24.0% |
| Zone | 55.5% | 69.7% |
| MOF closed (single-high) | 56.0% | 49.1% |
| MOF open (two-high) | 44.0% | 46.4% |
| Blitz | 22.7% | 21.6% |
| Cover 0 | 8.0% | not published |
| Cover 1 | 28.7% | not published |
| Cover 2 | 23.0% | not published |
| Cover 2-Man | 7.5% | not published |
| Cover 3 | 21.0% | not published |
| Cover 4 | unknown | not published |
| Cover 6 | 4.6% | not published |
| Cover 9 | 1.4% | not published |
| Coverage snaps | 348 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/ind). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 44.3% vs Sharp 24.0% (+20.3 pts); Zone: StatRankings 55.5% vs Sharp 69.7% (-14.2 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): none
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## HOU defense vs IND (IND@HOU, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Reed Blankenship | S | 3 | 3 | 41 | 0 | 0 | 0 | 0 | tackler x3 | A.Dulin 1, A.Gould 1, J.Taylor 1 | A.Gould 31 short_left Q1 |
| Jalen Pitre | S | 1 | 1 | 26 | 0 | 0 | 0 | 0 | tackler x1 | Q.Watkins 1 | Q.Watkins 26 deep_right Q1 |
| D.Stingley (name unresolved) | unknown | 1 | 1 | 25 | 0 | 0 | 0 | 0 | tackler x1 | A.Dulin 1 | A.Dulin 25 short_middle Q1 |
| Henry To'oTo'o | LB | 3 | 3 | 25 | 0 | 0 | 0 | 0 | tackler x3 | S.McGowan 1, T.Warren 1, J.Taylor 1 | T.Warren 22 deep_right Q2 |
| Calen Bullock | S | 2 | 1 | 17 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | A.Gould 1, A.Dulin 1 |  |
| Wade Woodaz | LB | 2 | 2 | 11 | 0 | 0 | 0 | 0 | tackler x2 | D.Giddens 1, J.Taylor 1 |  |
| Kamari Lassiter | CB | 1 | 0 | 0 | 0 | 1 | 0 | 0 | VERIFIED x1 | D.Burks 1 |  |
| Jake Hansen | LB | 2 | 0 | 0 | 0 | 2 | 0 | 0 | VERIFIED x2 | T.Warren 2 |  |
| Tommy Togiai | DT | 2 | 1 | -1 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | J.Taylor 1, T.Warren 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 5/13 for 104 yds, 0 TD; TE 1/5 for 22 yds, 0 TD; RB 6/7 for 18 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 4/0
Pass rush: sacks J.Clowney 1, W.Anderson 1; QB hits W.Anderson 3, L.Hall 1
Video (highlight transcript) mentions: Jalen Pitre (S) @3:34 "THEY'LL SPOT IT AT THE 48. WELL THE RIGHT TIME TO CALL THIS SCREEN BECAUSE OF THE BLITZ RIGHT HERE FROM PITRE. WITH THE THIRD AND 19. COLTS DOWN 7 TO 3." [coverage word: BLITZ]; Calen Bullock (S) @10:57 "ZONE AND DOUBLE COVERAGE. BROKEN UP. INCOMPLETE. INTENDED FOR DULIN BULLOCK BUT THE TALENT IS HERE. PRESSURE AGAIN." [coverage word: ZONE]
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### HOU season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 31.9% | 13.9% |
| Zone | 67.8% | 81.8% |
| MOF closed (single-high) | 52.1% | 55.6% |
| MOF open (two-high) | 47.9% | 43.0% |
| Blitz | 24.5% | 23.5% |
| Cover 0 | 3.7% | not published |
| Cover 1 | 22.5% | not published |
| Cover 2 | 23.8% | not published |
| Cover 2-Man | 5.8% | not published |
| Cover 3 | 27.0% | not published |
| Cover 4 | 8.6% | not published |
| Cover 6 | 7.3% | not published |
| Cover 9 | unknown | not published |
| Coverage snaps | 382 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/hou). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 31.9% vs Sharp 13.9% (+18.0 pts); Zone: StatRankings 67.8% vs Sharp 81.8% (-14.0 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): Zone: gap -14.0 pts is -4.6 vs the median gap; rank 15 StatRankings vs 5 Sharp
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## JAX defense vs NYG (JAX@NYG, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Travis Hunter | WR | 6 | 6 | 49 | 0 | 0 | 0 | 0 | tackler x6 | M.Nabers 5, X.Gipson 1 |  |
| Brenden Bates (last-name match) | TE | 3 | 3 | 48 | 0 | 0 | 0 | 0 | tackler x3 | C.Manhertz 1, T.Johnson 1, M.Fields 1 |  |
| Kaevon Merriweather | S | 2 | 1 | 35 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | I.Likely 1, C.Skattebo 1 | I.Likely 35 short_middle Q3 |
| Jourdan Lewis | CB | 1 | 1 | 11 | 0 | 0 | 0 | 0 | tackler x1 | C.Skattebo 1 |  |
| Montaric Brown | CB | 2 | 1 | 6 | 0 | 1 | 0 | 1 | VERIFIED x2, tackler x1 | M.Fields 2, J.Hyatt 1 |  |
| Dennis Gardeck | LB | 1 | 1 | 5 | 0 | 0 | 0 | 0 | tackler x1 | D.Singletary 1 |  |
| Foyesade Oluokun | LB | 2 | 1 | 4 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | C.Skattebo 1, J.Hyatt 1 |  |
| A.Johnson (name unresolved) | unknown | 3 | 1 | 4 | 0 | 2 | 0 | 0 | VERIFIED x2, tackler x1 | M.Nabers 1, I.Likely 1, M.Fields 1 |  |
| Josh Hines-Allen | DE | 2 | 1 | 2 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | C.Skattebo 2 |  |
| Ventrell Miller | LB | 1 | 1 | 1 | 0 | 0 | 0 | 0 | tackler x1 | C.Skattebo 1 |  |
| Travon Walker | DE | 2 | 0 | 0 | 0 | 2 | 0 | 0 | VERIFIED x2 | M.Nabers 2 |  |
| Arik Armstead | DT | 1 | 0 | 0 | 0 | 1 | 0 | 0 | VERIFIED x1 | D.Mooney 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 12/24 for 98 yds, 1 TD; TE 3/5 for 64 yds, 0 TD; RB 4/8 for 19 yds, 0 TD; unknown 0/1 for 0 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 1/1
Pass rush: sacks J.Hines-Allen 1; QB hits F.Oluokun 1, T.Walker 1
Video (highlight transcript) mentions: none found / not checked
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### JAX season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 26.2% | 17.2% |
| Zone | 73.8% | 77.7% |
| MOF closed (single-high) | 47.5% | 45.8% |
| MOF open (two-high) | 52.5% | 51.2% |
| Blitz | 32.6% | 27.4% |
| Cover 0 | 5.0% | not published |
| Cover 1 | 18.6% | not published |
| Cover 2 | 26.8% | not published |
| Cover 2-Man | unknown | not published |
| Cover 3 | 24.0% | not published |
| Cover 4 | 10.4% | not published |
| Cover 6 | 7.3% | not published |
| Cover 9 | 5.0% | not published |
| Coverage snaps | 317 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/jax). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 26.2% vs Sharp 17.2% (+9.0 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): none
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## NYG defense vs JAX (JAX@NYG, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Jevon Holland | S | 8 | 7 | 95 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x7 | P.Washington 4, J.Meyers 2, T.Hunter 1, B.Tuten 1 | P.Washington 21 deep_left Q2; J.Meyers 23 short_left Q3 |
| Ar'Darius Washington | S | 5 | 3 | 55 | 0 | 2 | 0 | 0 | VERIFIED x2, tackler x3 | J.Cameron 3, J.Meyers 2 | J.Meyers 26 deep_middle Q4 |
| Deonte Banks | CB | 5 | 3 | 37 | 0 | 2 | 0 | 0 | VERIFIED x2, tackler x3 | P.Washington 3, Bri.Thomas 1, J.Cameron 1 |  |
| Dru Phillips (last-name match) | CB | 7 | 4 | 31 | 0 | 3 | 0 | 0 | VERIFIED x3, tackler x4 | B.Strange 2, J.Meyers 2, B.Tuten 1, P.Washington 2 | P.Washington 21 deep_right Q4 |
| Paulson Adebo | CB | 4 | 1 | 23 | 0 | 3 | 0 | 0 | VERIFIED x3, tackler x1 | J.Meyers 2, P.Washington 2 | J.Meyers 23 deep_middle Q4 |
| Arvell Reese | LB | 4 | 4 | 21 | 0 | 0 | 0 | 0 | tackler x4 | P.Washington 2, B.Strange 1, L.Allen 1 |  |
| Micah McFadden | LB | 2 | 2 | 21 | 0 | 0 | 0 | 0 | tackler x2 | B.Tuten 1, C.Rodriguez 1 |  |
| G.Newsome (name unresolved) | unknown | 1 | 0 | 0 | 0 | 1 | 0 | 0 | VERIFIED x1 | P.Washington 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 16/33 for 235 yds, 0 TD; RB 5/5 for 32 yds, 0 TD; unknown 1/3 for 18 yds, 1 TD; TE 3/4 for 16 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 5/0
Pass rush: sacks D.Reader 1, A.Carter 2; QB hits A.Reese 1, A.Carter 3, D.Reader 1, S.Harris 1, B.Okoye 1, J.Kelly 1
Video (highlight transcript) mentions: Kayvon Thibodeaux (LB) @13:50 "BUYING TIME, SLIPS IT, PICKED OFF IN THE END ZONE BY THIBODEAUX. >> J.J.: THERE YOU GO. NOT HAPPY, YOU HAVE TO FIND A WAY TO BURN SOME O'CLOCK." [coverage word: PICKED]
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### NYG season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 47.2% | 25.6% |
| Zone | 52.1% | 69.1% |
| MOF closed (single-high) | 52.5% | 47.9% |
| MOF open (two-high) | 47.5% | 49.4% |
| Blitz | 42.9% | 38.4% |
| Cover 0 | 11.1% | not published |
| Cover 1 | 31.5% | not published |
| Cover 2 | 25.2% | not published |
| Cover 2-Man | 4.6% | not published |
| Cover 3 | unknown | not published |
| Cover 4 | unknown | not published |
| Cover 6 | 6.9% | not published |
| Cover 9 | unknown | not published |
| Coverage snaps | 305 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/nyg). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 47.2% vs Sharp 25.6% (+21.6 pts); Zone: StatRankings 52.1% vs Sharp 69.1% (-17.0 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): none
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## LV defense vs DEN (LV@DEN, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Eric Stokes | CB | 3 | 3 | 43 | 0 | 0 | 0 | 1 | VERIFIED x1, tackler x3 | J.Coleman 1, J.Waddle 3 | J.Waddle 24 deep_right Q2 |
| Nakobe Dean | LB | 4 | 3 | 37 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x3 | E.Engram 2, J.Waddle 1, J.Coleman 1 |  |
| Jeremy Chinn | S | 1 | 1 | 36 | 0 | 0 | 0 | 0 | tackler x1 | M.Mims 1 | M.Mims 36 deep_left Q2 |
| Taron Johnson | CB | 3 | 3 | 32 | 0 | 0 | 0 | 0 | tackler x3 | P.Bryant 3 | P.Bryant 20 deep_left Q1 |
| Jermod McCoy | CB | 4 | 3 | 32 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x3 | J.Waddle 2, E.Engram 2 |  |
| Quay Walker | LB | 4 | 4 | 23 | 0 | 0 | 0 | 0 | tackler x4 | J.Coleman 2, N.Adkins 1, E.Engram 1 |  |
| Treydan Stukes | S | 2 | 1 | 21 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | J.Waddle 1, E.Engram 1 | E.Engram 21 short_left Q4 |
| Maxx Crosby | DE | 2 | 0 | 0 | 0 | 2 | 0 | 0 | VERIFIED x2 | C.Sutton 1, M.Mims 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 7/16 for 129 yds, 0 TD; TE 8/11 for 78 yds, 1 TD; RB 4/5 for 18 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 4/0
Pass rush: sacks N.Dean 1; QB hits M.Koonce 1, M.Crosby 1
Video (highlight transcript) mentions: Jermod McCoy (CB) @2:04 "AT WADDLE -- GOOD COVERAGE ON THE PLAY. THE ROOKIE OUT OF TENNESSEE. >> Logan: McCOY DRAWING A TOUGH WILL LUTZ. OUT OF THE HOLD OF THE PUNTER," [coverage word: COVERAGE]
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### LV season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 34.2% | 21.9% |
| Zone | 65.8% | 69.4% |
| MOF closed (single-high) | 48.8% | 47.5% |
| MOF open (two-high) | 51.2% | 47.5% |
| Blitz | 30.2% | 24.9% |
| Cover 0 | 7.8% | not published |
| Cover 1 | 20.1% | not published |
| Cover 2 | 29.2% | not published |
| Cover 2-Man | 6.3% | not published |
| Cover 3 | 23.8% | not published |
| Cover 4 | unknown | not published |
| Cover 6 | 6.9% | not published |
| Cover 9 | 1.9% | not published |
| Coverage snaps | 319 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/lv). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 34.2% vs Sharp 21.9% (+12.3 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): none
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## DEN defense vs LV (LV@DEN, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D.Key (name unresolved) | unknown | 2 | 2 | 47 | 0 | 0 | 0 | 0 | tackler x2 | T.Tucker 1, A.Jeanty 1 | T.Tucker 39 deep_left Q4 |
| Ja'Quan McMillian | CB | 3 | 3 | 28 | 0 | 0 | 0 | 0 | tackler x3 | A.Jeanty 1, M.Mayer 1, J.Bech 1 |  |
| Justin Strnad | LB | 3 | 3 | 22 | 0 | 0 | 0 | 0 | tackler x3 | A.Jeanty 1, J.Bech 2 |  |
| Riley Moss | CB | 2 | 2 | 21 | 0 | 0 | 0 | 0 | tackler x2 | J.Bech 2 |  |
| Jahdae Barron | CB | 1 | 1 | 19 | 0 | 0 | 0 | 0 | tackler x1 | J.Bech 1 |  |
| Talanoa Hufanga | S | 2 | 1 | 16 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | J.Nailor 1, T.Tucker 1 |  |
| P.Surtain (name unresolved) | unknown | 1 | 1 | 11 | 0 | 0 | 0 | 0 | tackler x1 | T.Tucker 1 |  |
| Alex Singleton | LB | 2 | 1 | 5 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | M.Mayer 1, J.Bech 1 |  |
| Jonathon Cooper | LB | 2 | 1 | 4 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | A.Jeanty 1, M.Mayer 1 |  |
| Zach Allen | DE | 3 | 0 | 0 | 0 | 3 | 0 | 0 | VERIFIED x3 | T.Tucker 1, J.Bech 1, A.Jeanty 1 |  |
| D.J. Jones | DT | 1 | 0 | 0 | 0 | 1 | 0 | 0 | VERIFIED x1 | A.Jeanty 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 12/24 for 164 yds, 2 TD; RB 5/8 for 90 yds, 1 TD; TE 2/5 for 23 yds, 1 TD
Explosives allowed (pass 20+/rush 15+): 2/1
Pass rush: sacks J.Cooper 2, A.Singleton 1, Z.Allen (half) 1, N.Bonitto (half) 1, M.Roach 1; QB hits J.Cooper 1, D.Tillman 1, J.Strnad 1, Q.Robinson 1, Z.Allen 1, T.Hufanga 1
Video (highlight transcript) mentions: Ja'Quan McMillian (CB) @16:18 "COMPLETES IT TO BECH. [WHISTLE] >> Andrew: OUT OF BOUNDS, WITH McMILLIAN ON THE COVERAGE. THROW THIS BALL OFF. WE'LL SEE IF HE CAN KEEP THESE" [coverage word: COVERAGE]
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### DEN season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 45.6% | 25.1% |
| Zone | 52.8% | 70.2% |
| MOF closed (single-high) | 56.4% | 48.6% |
| MOF open (two-high) | 43.6% | 47.5% |
| Blitz | 35.2% | 33.9% |
| Cover 0 | 4.3% | not published |
| Cover 1 | 33.4% | not published |
| Cover 2 | unknown | not published |
| Cover 2-Man | 7.8% | not published |
| Cover 3 | unknown | not published |
| Cover 4 | 8.6% | not published |
| Cover 6 | 6.5% | not published |
| Cover 9 | 2.7% | not published |
| Coverage snaps | 371 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/den). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 45.6% vs Sharp 25.1% (+20.5 pts); Zone: StatRankings 52.8% vs Sharp 70.2% (-17.4 pts); MOF closed (single-high): StatRankings 56.4% vs Sharp 48.6% (+7.8 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): none
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## MIA defense vs BUF (MIA@BUF, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Jacob Rodriguez | LB | 7 | 7 | 67 | 0 | 0 | 0 | 0 | tackler x7 | D.Moore 2, T.Johnson 3, J.Cook 1, K.Shakir 1 | D.Moore 20 short_left Q2 |
| Michael Taaffe | S | 2 | 2 | 61 | 0 | 0 | 0 | 0 | tackler x2 | D.Knox 1, K.Shakir 1 | D.Knox 23 short_middle Q1; K.Shakir 38 deep_right Q3 |
| Zayne Anderson | S | 6 | 4 | 58 | 0 | 2 | 0 | 0 | VERIFIED x2, tackler x4 | K.Shakir 2, D.Moore 1, K.Latu 1, D.Knox 1, T.Johnson 1 | K.Shakir 32 deep_right Q1 |
| J.Marshall (name unresolved) | unknown | 4 | 4 | 40 | 0 | 0 | 0 | 0 | tackler x4 | D.Moore 2, K.Coleman 1, T.Johnson 1 |  |
| Malik Washington | WR | 1 | 1 | 30 | 0 | 0 | 0 | 0 | tackler x1 | K.Latu 1 | K.Latu 30 deep_middle Q1 |
| Chris Johnson | CB | 6 | 5 | 28 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x5 | K.Shakir 2, R.Davis 1, T.Johnson 1, K.Coleman 1, J.Cook 1 |  |
| JuJu Brents | CB | 3 | 2 | 27 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x2 | D.Moore 2, K.Coleman 1 |  |
| D.Baker (name unresolved) | unknown | 1 | 1 | 12 | 0 | 0 | 0 | 0 | tackler x1 | K.Shakir 1 |  |
| Kyle Louis | LB | 1 | 1 | 7 | 0 | 0 | 0 | 0 | tackler x1 | T.Johnson 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 15/24 for 209 yds, 1 TD; RB 10/12 for 64 yds, 0 TD; TE 3/6 for 61 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 5/0
Pass rush: sacks J.Brooks 1, Z.Anderson 1, K.Cooper 1; QB hits C.Robinson 1, K.Cooper 1, J.Brooks 1
Video (highlight transcript) mentions: none found / not checked
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### MIA season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 25.7% | 15.0% |
| Zone | 74.3% | 76.4% |
| MOF closed (single-high) | 47.9% | 42.6% |
| MOF open (two-high) | 52.1% | 51.9% |
| Blitz | 24.3% | 19.3% |
| Cover 0 | 4.7% | not published |
| Cover 1 | 19.5% | not published |
| Cover 2 | 33.9% | not published |
| Cover 2-Man | unknown | not published |
| Cover 3 | 24.1% | not published |
| Cover 4 | 6.2% | not published |
| Cover 6 | 5.8% | not published |
| Cover 9 | 3.9% | not published |
| Coverage snaps | 257 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/mia). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 25.7% vs Sharp 15.0% (+10.7 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): none
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## BUF defense vs MIA (MIA@BUF, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Davison Igbinosun | CB | 4 | 2 | 29 | 0 | 2 | 0 | 1 | VERIFIED x3, tackler x2 | C.Douglas 3, M.Washington 1, C.Bell 1 | M.Washington 21 deep_left Q3 |
| Jalon Kilgore | S | 2 | 2 | 24 | 0 | 0 | 0 | 0 | tackler x2 | G.Dulcich 1, J.Tolbert 1 |  |
| Maxwell Hairston | CB | 2 | 1 | 16 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | C.Douglas 2 |  |
| Amani Hooker | S | 2 | 1 | 14 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | C.Douglas 1, G.Dulcich 1 |  |
| Cole Bishop | S | 2 | 1 | 7 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | D.Herman 1, G.Dulcich 1 |  |
| Jordan Hancock | CB | 3 | 2 | 6 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x2 | M.Washington 1, G.Dulcich 1, O.Gordon 1 |  |
| Kaleb Elarms-Orr | LB | 1 | 1 | 5 | 0 | 0 | 0 | 0 | tackler x1 | G.Dulcich 1 |  |
| Dee Alford | CB | 2 | 1 | 4 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | M.Washington 2 |  |
| Deone Walker | DT | 1 | 0 | 0 | 0 | 1 | 0 | 0 | VERIFIED x1 | M.Washington 1 |  |
| Tre'Davious White | CB | 1 | 0 | 0 | 0 | 1 | 0 | 0 | VERIFIED x1 | K.Coleman 1 |  |
| Shaq Thompson | LB | 1 | 0 | 0 | 0 | 1 | 0 | 0 | VERIFIED x1 | C.Douglas 1 |  |
| Ed Oliver | DT | 1 | 1 | -3 | 0 | 0 | 0 | 0 | tackler x1 | O.Gordon 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 7/21 for 85 yds, 0 TD; TE 2/7 for 12 yds, 0 TD; RB 3/4 for 5 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 1/2
Pass rush: sacks G.Rousseau 2; QB hits L.Jackson 1, B.Chubb 2, A.Hooker 1, J.Solomon 1, D.Carter 1
Video (highlight transcript) mentions: none found / not checked
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### BUF season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 27.5% | 17.9% |
| Zone | 72.3% | 74.7% |
| MOF closed (single-high) | 48.4% | 46.5% |
| MOF open (two-high) | 51.6% | 49.2% |
| Blitz | 38.0% | 28.9% |
| Cover 0 | unknown | not published |
| Cover 1 | unknown | not published |
| Cover 2 | 25.0% | not published |
| Cover 2-Man | 6.9% | not published |
| Cover 3 | 27.5% | not published |
| Cover 4 | 11.5% | not published |
| Cover 6 | 4.9% | not published |
| Cover 9 | 2.2% | not published |
| Coverage snaps | 364 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/buf). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 27.5% vs Sharp 17.9% (+9.6 pts); Blitz: StatRankings 38.0% vs Sharp 28.9% (+9.1 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): Blitz: gap +9.1 pts is +5.7 vs the median gap; rank 9 StatRankings vs 14 Sharp
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## MIN defense vs SF (MIN@SF, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| James Pierre | CB | 3 | 3 | 47 | 0 | 0 | 0 | 0 | tackler x3 | D.Samuel 1, M.Evans 1, C.McCaffrey 1 | M.Evans 29 short_right Q2 |
| Blake Cashman | LB | 4 | 4 | 42 | 0 | 0 | 0 | 0 | tackler x4 | M.Evans 2, K.Juszczyk 1, L.Farrell 1 |  |
| B.Murphy (name unresolved) | unknown | 4 | 3 | 35 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x3 | M.Evans 1, K.Allen 3 |  |
| Theo Jackson | S | 1 | 1 | 34 | 0 | 0 | 0 | 0 | tackler x1 | M.Evans 1 | M.Evans 34 deep_middle Q1 |
| Andrew Van Ginkel | LB | 2 | 2 | 19 | 0 | 0 | 0 | 0 | tackler x2 | K.Juszczyk 1, C.McCaffrey 1 |  |
| Domonique Orange | DT | 1 | 1 | 19 | 0 | 0 | 0 | 0 | tackler x1 | J.Watkins 1 |  |
| Harrison Smith | S | 1 | 1 | 17 | 0 | 0 | 0 | 0 | tackler x1 | K.Allen 1 |  |
| Joshua Metellus | S | 1 | 1 | 9 | 0 | 0 | 0 | 0 | tackler x1 | G.Kittle 1 |  |
| I.Pace (name unresolved) | unknown | 1 | 1 | 7 | 0 | 0 | 0 | 0 | tackler x1 | K.Black 1 |  |
| Jak.Thomas (name unresolved) | unknown | 1 | 1 | 5 | 0 | 0 | 0 | 0 | tackler x1 | D.Samuel 1 |  |
| Kyle Van Noy | LB | 1 | 0 | 0 | 0 | 1 | 0 | 0 | VERIFIED x1 | C.McCaffrey 1 |  |
| Elijah Williams | DE | 1 | 1 | -3 | 0 | 0 | 0 | 0 | tackler x1 | D.Samuel 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 13/16 for 186 yds, 1 TD; TE 4/4 for 41 yds, 2 TD; RB 5/6 for 33 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 2/1
Pass rush: sacks E.Wilson 1; QB hits J.Redmond 2, A.Van Ginkel 2
Video (highlight transcript) mentions: Harrison Smith (S) @7:55 "IN THE BACK CORNER WORKING ONE-ON-ONE AGAINST HARRISON SMITH. IT WAS A BEAUTIFUL MOVE. A LOT OF SPACE BACK THERE. AND SO FAR, THESE VETERAN" [coverage word: CORNER]; Harrison Smith (S) @2:43 "IN THE BACK CORNER WORKING ONE-ON-ONE AGAINST HARRISON SMITH. IT WAS A BEAUTIFUL MOVE. A LOT OF SPACE BACK THERE. AND SO FAR, THESE VETERAN" [coverage word: CORNER]
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### MIN season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 26.7% | 5.2% |
| Zone | 73.0% | 86.9% |
| MOF closed (single-high) | 40.3% | 28.2% |
| MOF open (two-high) | 59.7% | 65.6% |
| Blitz | 74.4% | 69.2% |
| Cover 0 | unknown | not published |
| Cover 1 | unknown | not published |
| Cover 2 | 32.7% | not published |
| Cover 2-Man | 10.7% | not published |
| Cover 3 | 25.3% | not published |
| Cover 4 | 11.3% | not published |
| Cover 6 | unknown | not published |
| Cover 9 | unknown | not published |
| Coverage snaps | 300 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/min). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 26.7% vs Sharp 5.2% (+21.5 pts); Zone: StatRankings 73.0% vs Sharp 86.9% (-13.9 pts); MOF closed (single-high): StatRankings 40.3% vs Sharp 28.2% (+12.1 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): MOF closed (single-high): gap +12.1 pts is +9.4 vs the median gap; rank 30 StatRankings vs 32 Sharp
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## SF defense vs MIN (MIN@SF, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Renardo Green | CB | 9 | 9 | 64 | 0 | 0 | 0 | 0 | tackler x9 | T.Hockenson 1, J.Jefferson 4, T.Felton 1, J.Jennings 2, M.Price 1 |  |
| Deommodore Lenoir | CB | 4 | 2 | 54 | 0 | 2 | 0 | 0 | VERIFIED x2, tackler x2 | J.Jennings 2, J.Jefferson 2 | J.Jefferson 29 deep_left Q1; J.Jefferson 25 deep_left Q3 |
| Upton Stout | CB | 2 | 2 | 42 | 0 | 0 | 0 | 0 | tackler x2 | T.Hockenson 1, M.Price 1 | T.Hockenson 20 short_right Q1; M.Price 22 deep_right Q4 |
| Garret Wallow | LB | 3 | 3 | 25 | 0 | 0 | 0 | 0 | tackler x3 | T.Hockenson 2, D.Dallas 1 |  |
| Malik Mustapha | S | 3 | 3 | 22 | 0 | 0 | 0 | 0 | tackler x3 | J.Jennings 1, T.Felton 2 |  |
| Ji'Ayir Brown | S | 2 | 2 | 16 | 0 | 0 | 0 | 0 | tackler x2 | A.Jones 1, T.Hockenson 1 |  |
| Ephesians Prysock | CB | 2 | 2 | 15 | 0 | 0 | 0 | 0 | tackler x2 | T.Felton 1, J.Jefferson 1 |  |
| Fred Warner | LB | 2 | 1 | 8 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | T.Felton 2 |  |
| Siran Neal | S | 1 | 1 | 8 | 0 | 0 | 0 | 0 | tackler x1 | J.Jones 1 |  |
| Jaden Dugger | LB | 1 | 1 | 5 | 0 | 0 | 0 | 0 | tackler x1 | G.Bartholomew 1 |  |
| Osa Odighizuwa | DT | 1 | 1 | 1 | 0 | 0 | 0 | 0 | tackler x1 | T.Hockenson 1 |  |
| Marques Sigle | S | 1 | 0 | 0 | 0 | 1 | 0 | 0 | VERIFIED x1 | T.Felton 1 |  |
| DeForest Buckner | DT | 1 | 1 | -1 | 0 | 0 | 0 | 0 | tackler x1 | J.Mason 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 19/29 for 182 yds, 0 TD; TE 7/10 for 60 yds, 0 TD; RB 3/3 for 22 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 4/1
Pass rush: sacks O.Odighizuwa (half) 1, D.Buckner (half) 1; QB hits O.Odighizuwa 1, N.Bosa 2, M.Williams 1, C.West 1
Video (highlight transcript) mentions: Deommodore Lenoir (CB) @4:12 ">> Cris: I THINK COUSINS IS ANNOYED A LITTLE BIT, TOO. IN FOR THE TOUCHDOWN. HE DROVE LENOIR INTO THE END ZONE. >> Cris: THE OUTSIDE ZONE COMING" [coverage word: ZONE]; Deommodore Lenoir (CB) @4:08 "CUTS IT BACK AND LOST THE BALL. IT'S PICKED UP BY DEOMMODORE LENOIR. HE'S COMING BACK THE OTHER WAY. TILLMAN. HE'S THE NEW GUY THAT PUNCHES" [coverage word: PICKED]
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### SF season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 29.6% | 11.2% |
| Zone | 69.3% | 82.8% |
| MOF closed (single-high) | 59.0% | 56.2% |
| MOF open (two-high) | 41.0% | 39.5% |
| Blitz | 31.8% | 26.8% |
| Cover 0 | unknown | not published |
| Cover 1 | 25.0% | not published |
| Cover 2 | unknown | not published |
| Cover 2-Man | 3.2% | not published |
| Cover 3 | 29.9% | not published |
| Cover 4 | 8.6% | not published |
| Cover 6 | 7.8% | not published |
| Cover 9 | 2.6% | not published |
| Coverage snaps | 348 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/sf). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 29.6% vs Sharp 11.2% (+18.4 pts); Zone: StatRankings 69.3% vs Sharp 82.8% (-13.5 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): none
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## NO defense vs CHI (NO@CHI, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Jonas Sanker | S | 4 | 4 | 52 | 0 | 0 | 0 | 0 | tackler x4 | L.Burden 2, Z.Thomas 1, C.Loveland 1 | Z.Thomas 40 deep_left Q3 |
| Julian Blackmon | S | 2 | 2 | 33 | 0 | 0 | 0 | 0 | tackler x2 | S.Roush 1, K.Raymond 1 |  |
| Kool-Aid McKinstry | CB | 5 | 4 | 31 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x4 | D.Swift 1, R.Odunze 2, K.Raymond 1, Z.Thomas 1 |  |
| Jordan Howden | S | 2 | 1 | 16 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | K.Raymond 1, R.Odunze 1 |  |
| Anfernee Jennings | LB | 1 | 1 | 12 | 0 | 0 | 0 | 0 | tackler x1 | C.Loveland 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 9/13 for 125 yds, 0 TD; TE 4/4 for 48 yds, 1 TD; RB 2/3 for 8 yds, 1 TD
Explosives allowed (pass 20+/rush 15+): 1/2
Pass rush: sacks C.Young 1, C.Wooden 1, J.Sanker 1, J.Ridgeway 1; QB hits A.Jennings 1
Video (highlight transcript) mentions: none found / not checked
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### NO season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 38.2% | 16.7% |
| Zone | 59.6% | 73.9% |
| MOF closed (single-high) | 64.9% | 64.3% |
| MOF open (two-high) | 35.1% | 31.8% |
| Blitz | 39.1% | 33.9% |
| Cover 0 | 3.1% | not published |
| Cover 1 | 30.1% | not published |
| Cover 2 | unknown | not published |
| Cover 2-Man | 5.0% | not published |
| Cover 3 | 28.6% | not published |
| Cover 4 | 5.0% | not published |
| Cover 6 | 5.0% | not published |
| Cover 9 | 2.5% | not published |
| Coverage snaps | 322 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/no). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 38.2% vs Sharp 16.7% (+21.5 pts); Zone: StatRankings 59.6% vs Sharp 73.9% (-14.3 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): none
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## CHI defense vs NO (NO@CHI, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Cam Lewis | CB | 4 | 4 | 49 | 0 | 0 | 0 | 0 | tackler x4 | D.Vele 3, C.Olave 1 |  |
| Jaylon Johnson | CB | 5 | 5 | 48 | 0 | 0 | 0 | 0 | tackler x5 | C.Olave 3, D.Vele 2 |  |
| Devin Bush | LB | 4 | 4 | 31 | 0 | 0 | 0 | 0 | tackler x4 | O.Delp 1, D.Vele 2, N.Fant 1 |  |
| T.J. Edwards | LB | 4 | 4 | 25 | 0 | 0 | 0 | 0 | tackler x4 | C.Olave 2, C.Donaldson 2 |  |
| N.Sewell (name unresolved) | unknown | 1 | 1 | 24 | 0 | 0 | 0 | 0 | tackler x1 | C.Olave 1 | C.Olave 24 deep_left Q2 |
| T.Stevenson (name unresolved) | unknown | 4 | 3 | 22 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x3 | J.Tyson 1, C.Olave 2, C.Donaldson 1 |  |
| C.Phillips (name unresolved) | unknown | 3 | 2 | 8 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x2 | C.Donaldson 1, J.Tyson 1, N.Fant 1 |  |
| Austin Booker | DE | 2 | 0 | 0 | 0 | 2 | 0 | 0 | VERIFIED x2 | J.Johnson 1, T.Etienne 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 17/24 for 184 yds, 0 TD; TE 3/6 for 25 yds, 0 TD; RB 5/7 for 13 yds, 1 TD; unknown 0/1 for 0 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 1/2
Pass rush: sacks J.Simmons 3, C.Lewis 1, M.Sweat 1, C.Phillips 1; QB hits A.Booker 1, N.Gallimore 1, M.Sweat 2
Video (highlight transcript) mentions: none found / not checked
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### CHI season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 36.2% | 27.2% |
| Zone | 63.4% | 68.8% |
| MOF closed (single-high) | 50.7% | 50.5% |
| MOF open (two-high) | 49.3% | 45.8% |
| Blitz | 38.6% | 32.4% |
| Cover 0 | unknown | not published |
| Cover 1 | 26.6% | not published |
| Cover 2 | 29.7% | not published |
| Cover 2-Man | 6.6% | not published |
| Cover 3 | 21.4% | not published |
| Cover 4 | 5.2% | not published |
| Cover 6 | 5.2% | not published |
| Cover 9 | 1.7% | not published |
| Coverage snaps | 290 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/chi). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 36.2% vs Sharp 27.2% (+9.0 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): Man: gap +9.0 pts is -6.5 vs the median gap; rank 14 StatRankings vs 4 Sharp
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## NYJ defense vs LAC (NYJ@LAC, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Minkah Fitzpatrick | S | 2 | 2 | 35 | 0 | 0 | 0 | 0 | tackler x2 | D.Njoku 1, T.Harris 1 | T.Harris 22 short_right Q4 |
| Jamien Sherwood | LB | 3 | 2 | 17 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x2 | Q.Johnston 1, L.McConkey 2 |  |
| Kingsley Enagbare | LB | 1 | 1 | 15 | 0 | 0 | 0 | 0 | tackler x1 | K.Vidal 1 |  |
| Demario Davis | LB | 2 | 2 | 14 | 0 | 0 | 0 | 0 | tackler x2 | C.Kolar 1, T.Harris 1 |  |
| Brandon Stephens | CB | 2 | 2 | 12 | 0 | 0 | 0 | 0 | tackler x2 | O.Hampton 1, D.Njoku 1 |  |
| Azareye'h Thomas | CB | 3 | 2 | 10 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x2 | K.Mitchell 1, D.Njoku 1, L.McConkey 1 |  |
| D'Angelo Ponds | CB | 1 | 1 | 3 | 0 | 0 | 0 | 0 | tackler x1 | K.Vidal 1 |  |
| David Bailey | LB | 1 | 0 | 0 | 0 | 1 | 0 | 0 | VERIFIED x1 | L.McConkey 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 6/10 for 60 yds, 1 TD; TE 3/4 for 29 yds, 0 TD; RB 4/4 for 28 yds, 0 TD; unknown 0/2 for 0 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 1/2
Pass rush: sacks D.Bailey 2, H.Phillips 1, J.Briggs 1, J.Heflin (half) 1, D.Jackson (half) 1, J.Sherwood 1, J.Briggs (half) 1, M.Fitzpatrick (half) 1; QB hits D.Bailey 1
Video (highlight transcript) mentions: Minkah Fitzpatrick (S) @7:50 "AND IT IS HAMPTON ALONG THE EDGE WITH THE BEST L.A. RUN OF THE DAY. FITZPATRICK THE TACKLE DOWN IN THE RED ZONE. >> Drew: YEAH." [coverage word: ZONE]
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### NYJ season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 38.5% | 26.8% |
| Zone | 61.5% | 63.7% |
| MOF closed (single-high) | 46.3% | 46.1% |
| MOF open (two-high) | 53.7% | 48.8% |
| Blitz | 40.4% | 38.3% |
| Cover 0 | 3.8% | not published |
| Cover 1 | 26.1% | not published |
| Cover 2 | 30.6% | not published |
| Cover 2-Man | 8.6% | not published |
| Cover 3 | unknown | not published |
| Cover 4 | 6.4% | not published |
| Cover 6 | 5.1% | not published |
| Cover 9 | unknown | not published |
| Coverage snaps | 314 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/nyj). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 38.5% vs Sharp 26.8% (+11.7 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): none
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## LAC defense vs NYJ (NYJ@LAC, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Elijah Molden | CB | 2 | 2 | 29 | 0 | 0 | 0 | 0 | tackler x2 | M.Taylor 1, K.Sadiq 1 |  |
| Marlowe Wax | LB | 2 | 2 | 28 | 0 | 0 | 0 | 0 | tackler x2 | B.Allen 1, G.Wilson 1 |  |
| Cam Hart | CB | 2 | 2 | 21 | 0 | 0 | 0 | 0 | tackler x2 | A.Mitchell 1, G.Wilson 1 |  |
| Del'Shawn Phillips | LB | 2 | 2 | 19 | 0 | 0 | 0 | 0 | tackler x2 | G.Wilson 1, K.Sadiq 1 |  |
| RJ Mickens | S | 1 | 1 | 9 | 0 | 0 | 0 | 0 | tackler x1 | K.Sadiq 1 |  |
| Tony Jefferson | S | 1 | 1 | 6 | 0 | 0 | 0 | 0 | tackler x1 | M.Taylor 1 |  |
| Donte Jackson | CB | 1 | 1 | 5 | 0 | 0 | 0 | 0 | tackler x1 | T.Patrick 1 |  |
| Caleb Murphy | LB | 1 | 1 | 4 | 0 | 0 | 0 | 0 | tackler x1 | B.Hall 1 |  |
| Denzel Perryman | LB | 1 | 1 | 3 | 0 | 0 | 0 | 0 | tackler x1 | B.Hall 1 |  |
| Deane Leonard | CB | 1 | 0 | 0 | 0 | 1 | 0 | 0 | VERIFIED x1 | G.Wilson 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 8/10 for 98 yds, 2 TD; TE 5/5 for 55 yds, 0 TD; RB 4/4 for 23 yds, 1 TD; unknown 0/1 for 0 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 1/2
Pass rush: sacks T.Dye 1, C.Murphy 1; QB hits none
Video (highlight transcript) mentions: Donte Jackson (CB) @2:35 "THE BACK OF THE END ZONE. AND HIS EYES GOING THERE, JUST FREEZES DONTE JACKSON JUST ENOUGH TO ALLOW BREECE HALL TO >> Adam: THANKS FOR BREAKING THAT DOWN." [coverage word: ZONE]
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### LAC season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 32.7% | 13.4% |
| Zone | 67.0% | 74.5% |
| MOF closed (single-high) | 50.4% | 44.6% |
| MOF open (two-high) | 49.6% | 50.5% |
| Blitz | 26.2% | 23.9% |
| Cover 0 | 5.4% | not published |
| Cover 1 | 20.9% | not published |
| Cover 2 | 22.9% | not published |
| Cover 2-Man | 6.4% | not published |
| Cover 3 | 24.6% | not published |
| Cover 4 | 9.4% | not published |
| Cover 6 | 6.1% | not published |
| Cover 9 | 3.7% | not published |
| Coverage snaps | 297 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/lac). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 32.7% vs Sharp 13.4% (+19.3 pts); Zone: StatRankings 67.0% vs Sharp 74.5% (-7.5 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): Man: gap +19.3 pts is +3.8 vs the median gap; rank 16 StatRankings vs 26 Sharp
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## PIT defense vs PHI (PIT@PHI, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Jamel Dean | CB | 6 | 6 | 40 | 0 | 0 | 0 | 0 | tackler x6 | M.Lemon 1, D.Smith 4, D.Cooper 1 |  |
| KJ Henry | LB | 1 | 1 | 38 | 0 | 0 | 0 | 0 | tackler x1 | D.Goedert 1 | D.Goedert 38 short_left Q1 |
| Robert Spears-Jennings | S | 1 | 1 | 14 | 0 | 0 | 0 | 0 | tackler x1 | D.Cooper 1 |  |
| Patrick Queen | LB | 1 | 1 | 11 | 0 | 0 | 0 | 0 | tackler x1 | D.Smith 1 |  |
| Daylen Everette | CB | 2 | 1 | 9 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | D.Cooper 2 |  |
| Payton Wilson | LB | 1 | 0 | 0 | 0 | 1 | 0 | 0 | VERIFIED x1 | D.Smith 1 |  |
| Jalen Ramsey | CB | 1 | 0 | 0 | 0 | 1 | 0 | 0 | VERIFIED x1 | D.Smith 1 |  |
| Cameron Heyward | DT | 1 | 0 | 0 | 0 | 1 | 0 | 0 | VERIFIED x1 | D.Smith 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 10/19 for 103 yds, 0 TD; TE 1/1 for 38 yds, 0 TD; unknown 0/1 for 0 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 2/1
Pass rush: sacks A.Highsmith 2, J.Sawyer 1; QB hits none
Video (highlight transcript) mentions: T.J. Watt (LB) @0:28 "LITTLE NOD TO MAKE IT SEEM LIKE HE IS GOING TO HAVE A PEEL BACK BLOCK, HE IS ABLE TO AVOID IT. WATT MISSES BY GOING AROUND THAT BLOCK. BARKLEY, IT'S A RACE AT THAT" [coverage word: MISSES]
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### PIT season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 17.7% | 11.9% |
| Zone | 81.8% | 81.3% |
| MOF closed (single-high) | 45.3% | 43.6% |
| MOF open (two-high) | 54.7% | 51.4% |
| Blitz | 28.2% | 27.3% |
| Cover 0 | 3.7% | not published |
| Cover 1 | unknown | not published |
| Cover 2 | 22.8% | not published |
| Cover 2-Man | unknown | not published |
| Cover 3 | 30.2% | not published |
| Cover 4 | 16.8% | not published |
| Cover 6 | 10.0% | not published |
| Cover 9 | 1.4% | not published |
| Coverage snaps | 351 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/pit). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** none at 7+ pts
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): none
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## PHI defense vs PIT (PIT@PHI, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Marcus Epps | S | 7 | 7 | 70 | 0 | 0 | 0 | 0 | tackler x7 | G.Bernard 3, R.Dowdle 1, P.Freiermuth 1, R.Wilson 1, M.Hurleman 1 | R.Wilson 33 deep_left Q3 |
| J.Trotter (name unresolved) | unknown | 4 | 4 | 36 | 0 | 0 | 0 | 0 | tackler x4 | P.Freiermuth 1, R.Dowdle 1, D.Washington 1, M.Hurleman 1 |  |
| Cooper DeJean | CB | 3 | 2 | 24 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x2 | G.Bernard 2, P.Freiermuth 1 |  |
| Andrew Mukuba | S | 4 | 3 | 22 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x3 | D.Washington 1, R.Wilson 1, M.Hurleman 1, G.Bernard 1 |  |
| Jonathan Jones | CB | 7 | 4 | 21 | 0 | 3 | 0 | 0 | VERIFIED x3, tackler x4 | M.Hurleman 3, P.Freiermuth 1, R.Wilson 3 |  |
| DeVonta Smith (last-name match) | WR | 2 | 2 | 11 | 0 | 0 | 0 | 0 | tackler x2 | P.Freiermuth 1, G.Bernard 1 |  |
| Jihaad Campbell | LB | 3 | 3 | 10 | 0 | 0 | 0 | 0 | tackler x3 | J.Warren 2, R.Dowdle 1 |  |
| Jalyx Hunt | LB | 1 | 1 | 7 | 0 | 0 | 0 | 0 | tackler x1 | G.Bernard 1 |  |
| Riq Woolen (last-name match) | CB | 1 | 1 | 3 | 0 | 0 | 0 | 0 | tackler x1 | R.Dowdle 1 |  |
| Quinyon Mitchell | CB | 3 | 1 | 2 | 0 | 2 | 0 | 0 | VERIFIED x2, tackler x1 | D.Metcalf 3 |  |
| Arnold Ebiketie | LB | 1 | 1 | 1 | 0 | 0 | 0 | 0 | tackler x1 | D.Washington 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 16/27 for 146 yds, 1 TD; TE 8/8 for 61 yds, 0 TD; RB 6/8 for 20 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 2/0
Pass rush: sacks J.Hunt 1, B.Young 2, J.Greenard 1, N.Smith 1, G.Hall 1; QB hits M.Ojomo 1
Video (highlight transcript) mentions: none found / not checked
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### PHI season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 38.1% | 18.2% |
| Zone | 61.9% | 73.1% |
| MOF closed (single-high) | 58.1% | 52.1% |
| MOF open (two-high) | 41.9% | 41.6% |
| Blitz | 29.8% | 25.1% |
| Cover 0 | 5.0% | not published |
| Cover 1 | 28.9% | not published |
| Cover 2 | unknown | not published |
| Cover 2-Man | 4.1% | not published |
| Cover 3 | 24.2% | not published |
| Cover 4 | 8.5% | not published |
| Cover 6 | 10.4% | not published |
| Cover 9 | unknown | not published |
| Coverage snaps | 318 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/phi). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 38.1% vs Sharp 18.2% (+19.9 pts); Zone: StatRankings 61.9% vs Sharp 73.1% (-11.2 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): none
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## TB defense vs DET (TB@DET, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Tykee Smith | S | 4 | 3 | 62 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x3 | S.LaPorta 2, T.Conklin 1, J.Gibbs 1 | S.LaPorta 47 deep_right Q1 |
| Benjamin Morrison | CB | 3 | 3 | 60 | 0 | 0 | 0 | 0 | tackler x3 | J.Williams 2, B.Wright 1 | B.Wright 27 deep_left Q2 |
| Alex Anzalone | LB | 5 | 5 | 37 | 0 | 0 | 0 | 0 | tackler x5 | S.LaPorta 1, S.Vaki 1, A.St. Brown 2, J.Gibbs 1 |  |
| Josiah Trotter | LB | 4 | 4 | 21 | 0 | 0 | 0 | 0 | tackler x4 | A.St. Brown 2, S.LaPorta 1, J.Gibbs 1 |  |
| David Walker | LB | 1 | 1 | 15 | 0 | 0 | 0 | 0 | tackler x1 | B.Wright 1 |  |
| Kevin Knowles | CB | 1 | 1 | 10 | 0 | 0 | 0 | 0 | tackler x1 | J.Gibbs 1 |  |
| Keionte Scott | CB | 2 | 1 | 3 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | S.LaPorta 1, J.Williams 1 |  |
| Yaya Diaby | LB | 1 | 0 | 0 | 0 | 1 | 0 | 0 | VERIFIED x1 | J.Gibbs 1 |  |
| Vita Vea | DT | 1 | 0 | 0 | 0 | 1 | 0 | 0 | VERIFIED x1 | I.TeSlaa 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 9/13 for 130 yds, 2 TD; TE 6/9 for 122 yds, 0 TD; RB 5/6 for 27 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 3/1
Pass rush: sacks D.Walker 1; QB hits Y.Diaby 1, V.Vea 1, R.Nunez-Roches 1, C.Kancey 1, D.Walker 1
Video (highlight transcript) mentions: Benjamin Morrison (CB) @0:25 "TAMPA BAY. THERE'S OUTSIDE LEVERAGE BY BENJAMIN MORRISON. SOMETHING IS NOT RIGHT THERE." [coverage word: LEVERAGE]
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### TB season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 31.1% | 16.2% |
| Zone | 68.3% | 79.2% |
| MOF closed (single-high) | 64.6% | 62.0% |
| MOF open (two-high) | 35.4% | 36.5% |
| Blitz | 45.4% | 42.2% |
| Cover 0 | 4.3% | not published |
| Cover 1 | 22.2% | not published |
| Cover 2 | 18.8% | not published |
| Cover 2-Man | 4.6% | not published |
| Cover 3 | 37.8% | not published |
| Cover 4 | 7.1% | not published |
| Cover 6 | unknown | not published |
| Cover 9 | 1.8% | not published |
| Coverage snaps | 325 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/tb). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 31.1% vs Sharp 16.2% (+14.9 pts); Zone: StatRankings 68.3% vs Sharp 79.2% (-10.9 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): none
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## DET defense vs TB (TB@DET, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Rock Ya-Sin | CB | 6 | 6 | 51 | 0 | 0 | 0 | 0 | tackler x6 | E.Egbuka 1, T.Johnson 1, C.Godwin 1, T.Hurst 2, K.Gainwell 1 |  |
| Derrick Barnes | LB | 3 | 3 | 26 | 0 | 0 | 0 | 0 | tackler x3 | K.Gainwell 2, C.Otton 1 |  |
| Brian Branch | S | 4 | 2 | 17 | 0 | 2 | 0 | 1 | VERIFIED x3, tackler x2 | C.Godwin 1, E.Egbuka 1, K.Gainwell 1, B.Irving 1, T.Hurst 1 |  |
| Christian Izien | S | 1 | 1 | 16 | 0 | 0 | 0 | 0 | tackler x1 | B.Irving 1 |  |
| Chuck Clark | S | 2 | 1 | 12 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | T.Hurst 1, E.Egbuka 1 |  |
| Roger McCreary | CB | 2 | 1 | 10 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | T.Hurst 2 |  |
| DJ Wonnum | LB | 2 | 1 | 9 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | T.Johnson 1, B.Irving 1 |  |
| Kerby Joseph | S | 1 | 1 | 8 | 0 | 0 | 0 | 1 | VERIFIED x1, tackler x1 | C.Godwin 1, B.Sharp 1 |  |
| Malcolm Rodriguez | LB | 2 | 1 | 7 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | K.Gainwell 1, B.Irving 1 |  |
| Khalil Dorsey | CB | 1 | 1 | 5 | 0 | 0 | 0 | 0 | tackler x1 | T.Johnson 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 12/18 for 104 yds, 2 TD; RB 7/9 for 76 yds, 0 TD; TE 1/4 for 8 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 1/1
Pass rush: sacks D.Wonnum 1, C.Clark 1, T.Nowaske 1, D.Moore (half) 1, M.Rodriguez (half) 1; QB hits D.Wonnum 1, A.McNeill 1
Video (highlight transcript) mentions: none found / not checked
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### DET season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 38.2% | 19.5% |
| Zone | 59.2% | 75.6% |
| MOF closed (single-high) | 60.7% | 49.4% |
| MOF open (two-high) | 39.3% | 47.8% |
| Blitz | 30.4% | 22.2% |
| Cover 0 | 5.0% | not published |
| Cover 1 | 25.2% | not published |
| Cover 2 | 20.4% | not published |
| Cover 2-Man | 8.0% | not published |
| Cover 3 | 29.2% | not published |
| Cover 4 | unknown | not published |
| Cover 6 | 4.0% | not published |
| Cover 9 | 1.9% | not published |
| Coverage snaps | 377 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/det). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 38.2% vs Sharp 19.5% (+18.7 pts); Zone: StatRankings 59.2% vs Sharp 75.6% (-16.4 pts); MOF closed (single-high): StatRankings 60.7% vs Sharp 49.4% (+11.3 pts); MOF open (two-high): StatRankings 39.3% vs Sharp 47.8% (-8.5 pts); Blitz: StatRankings 30.4% vs Sharp 22.2% (+8.2 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): Zone: gap -16.4 pts is -6.9 vs the median gap; rank 25 StatRankings vs 15 Sharp; MOF closed (single-high): gap +11.3 pts is +8.6 vs the median gap; rank 4 StatRankings vs 12 Sharp; MOF open (two-high): gap -8.5 pts is -9.2 vs the median gap; rank 29 StatRankings vs 16 Sharp; Blitz: gap +8.2 pts is +4.8 vs the median gap; rank 17 StatRankings vs 28 Sharp
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## TEN defense vs DAL (TEN@DAL, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Joshua Williams | CB | 9 | 9 | 143 | 0 | 0 | 0 | 0 | tackler x9 | C.Lamb 3, J.Mitchell 1, G.Pickens 5 | J.Mitchell 27 short_middle Q1; G.Pickens 31 deep_middle Q3; G.Pickens 30 deep_left Q3 |
| A.Hill (name unresolved) | unknown | 2 | 2 | 34 | 0 | 0 | 0 | 0 | tackler x2 | C.Lamb 1, J.Corbin 1 | C.Lamb 29 deep_right Q2 |
| K.Winston (name unresolved) | unknown | 3 | 3 | 25 | 0 | 0 | 0 | 0 | tackler x3 | J.Mitchell 1, C.Lamb 1, B.Spann-Ford 1 |  |
| Micah Robinson | CB | 1 | 1 | 24 | 0 | 0 | 0 | 0 | tackler x1 | C.Lamb 1 | C.Lamb 24 deep_left Q3 |
| Cor'Dale Flott | CB | 2 | 2 | 17 | 0 | 0 | 0 | 0 | tackler x2 | R.Flournoy 1, C.Lamb 1 |  |
| Cedric Gray | LB | 2 | 2 | 17 | 0 | 0 | 0 | 0 | tackler x2 | C.Lamb 1, G.Pickens 1 |  |
| Isaiah Oliver | S | 2 | 2 | 15 | 0 | 0 | 0 | 0 | tackler x2 | C.Lamb 2 |  |
| Keldric Faulk | DE | 1 | 1 | 7 | 0 | 0 | 0 | 0 | tackler x1 | J.Williams 1 |  |
| J.Johnson (name unresolved) | unknown | 1 | 1 | 6 | 0 | 0 | 0 | 0 | tackler x1 | L.Schoonmaker 1 |  |
| Jacob Martin | DE | 1 | 1 | 6 | 0 | 0 | 0 | 0 | tackler x1 | J.Williams 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 20/25 for 245 yds, 2 TD; TE 5/5 for 51 yds, 1 TD; RB 4/4 for 29 yds, 1 TD
Explosives allowed (pass 20+/rush 15+): 5/3
Pass rush: sacks none; QB hits S.Thomas 1
Video (highlight transcript) mentions: none found / not checked
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### TEN season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 27.7% | 17.4% |
| Zone | 71.4% | 75.3% |
| MOF closed (single-high) | 45.5% | 48.8% |
| MOF open (two-high) | 54.5% | 47.1% |
| Blitz | 24.9% | 23.7% |
| Cover 0 | 4.6% | not published |
| Cover 1 | 20.4% | not published |
| Cover 2 | 24.3% | not published |
| Cover 2-Man | unknown | not published |
| Cover 3 | 21.0% | not published |
| Cover 4 | 11.9% | not published |
| Cover 6 | 10.6% | not published |
| Cover 9 | 3.3% | not published |
| Coverage snaps | 329 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/ten). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 27.7% vs Sharp 17.4% (+10.3 pts); MOF open (two-high): StatRankings 54.5% vs Sharp 47.1% (+7.4 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): MOF closed (single-high): gap -3.3 pts is -6.0 vs the median gap; rank 25 StatRankings vs 14 Sharp; MOF open (two-high): gap +7.4 pts is +6.6 vs the median gap; rank 8 StatRankings vs 20 Sharp
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

## DAL defense vs TEN (TEN@DAL, FINAL)

| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Cobie Durant | CB | 3 | 3 | 41 | 0 | 0 | 0 | 0 | tackler x3 | C.Dike 2, E.Ayomanor 1 | C.Dike 22 deep_right Q1 |
| Justin Barron | LB | 5 | 5 | 37 | 0 | 0 | 0 | 0 | tackler x5 | G.Helm 1, D.Bellinger 1, C.Dike 2, M.Carter 1 |  |
| S.Revel (name unresolved) | unknown | 2 | 2 | 30 | 0 | 0 | 0 | 0 | tackler x2 | C.Ridley 2 | C.Ridley 21 deep_middle Q4 |
| Malik Hooker | S | 3 | 2 | 27 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x2 | E.Ayomanor 1, C.Ridley 2 |  |
| Ameer Speed | CB | 2 | 1 | 11 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | C.Dike 1, C.Ridley 1 |  |
| Shemar James | LB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | tackler x1 | C.Dike 1 |  |
| DeMarvion Overshown | LB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | tackler x1 | C.Dike 1 |  |
| Caleb Downs | S | 1 | 1 | 5 | 0 | 0 | 0 | 1 | VERIFIED x1, tackler x1 | C.Tate 1, G.Helm 1 |  |
| Derion Kendrick | CB | 1 | 1 | 5 | 0 | 0 | 0 | 0 | tackler x1 | X.Restrepo 1 |  |
| J.Porter (name unresolved) | unknown | 2 | 1 | 4 | 0 | 1 | 0 | 0 | VERIFIED x1, tackler x1 | C.Tate 1, E.Ayomanor 1 |  |
| Quinnen Williams | DT | 1 | 0 | 0 | 0 | 1 | 0 | 0 | VERIFIED x1 | G.Helm 1 |  |
| Dee Winters | LB | 1 | 1 | -1 | 0 | 0 | 0 | 0 | tackler x1 | C.Tate 1 |  |

Yards allowed by target position (WR slot/outside unknown): WR 17/22 for 227 yds, 2 TD; TE 3/4 for 19 yds, 0 TD; RB 1/2 for 2 yds, 0 TD
Explosives allowed (pass 20+/rush 15+): 3/0
Pass rush: sacks J.Houston 3, E.Garcia (half) 1, D.Ezeiruaku (half) 1, Q.Williams 2; QB hits Q.Williams 2, J.Houston 1
Video (highlight transcript) mentions: none found / not checked
Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).

#### DAL season coverage rates (public, season-level; NOT game-level)

| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |
|---|---|---|
| Man | 46.7% | 23.4% |
| Zone | 51.9% | 68.5% |
| MOF closed (single-high) | 59.6% | 57.8% |
| MOF open (two-high) | 40.4% | 37.9% |
| Blitz | 26.2% | 20.4% |
| Cover 0 | 5.5% | not published |
| Cover 1 | 37.5% | not published |
| Cover 2 | 19.6% | not published |
| Cover 2-Man | 3.7% | not published |
| Cover 3 | unknown | not published |
| Cover 4 | 7.5% | not published |
| Cover 6 | 5.8% | not published |
| Cover 9 | 2.0% | not published |
| Coverage snaps | 347 | not published |

Sources: StatRankings = StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST (https://statrankings.com/nfl/coverage/team/dal). Sharp = Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST (https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/; blitz from the Sharp defensive-tendencies page, same update day).
The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.
**Source disagreement (7+ pts):** Man: StatRankings 46.7% vs Sharp 23.4% (+23.3 pts); Zone: StatRankings 51.9% vs Sharp 68.5% (-16.6 pts)
**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): none
Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).

