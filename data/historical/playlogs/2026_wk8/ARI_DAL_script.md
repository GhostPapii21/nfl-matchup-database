# ARI @ DAL game script

Final: ARI 33, DAL 30 (margin DAL -3)
Pregame (DraftKings close, ESPN pickcenter): DAL -7, total 54.5. Favorite DAL result vs spread: -3 vs -7.0 → did not cover. Total 63 vs 54.5: OVER.
Weather actuals: dome (indoor)

**Script label: overtime underdog upset: ARI threw 46 times and won 33-30 in OT; DAL leaned run (39 rushes)**

## Score state by quarter
- end Q1: ARI 0-DAL 7
- end Q2: ARI 3-DAL 14
- end Q3: ARI 10-DAL 17
- end Q4: ARI 30-DAL 30
- end Q5: ARI 33-DAL 30

## Run/pass and pace
| Team | Rush att | Pass att | Sacks taken | Dropbacks | Pass rate | Total plays | TOP | Yards | Turnovers |
|---|---|---|---|---|---|---|---|---|---|
| ARI | 27 | 46 | 5 | 51 | 65% | 78 | 33:25 | 467 | 2 |
| DAL | 39 | 29 | 4 | 33 | 46% | 72 | 33:42 | 261 | 0 |

## Backfield
- ARI: lead Tyler Allgeier 11 car 147 yds 1 TD (41% of team rushes); RB2 Jeremiyah Love 9 car 23 yds 0 TD
- DAL: lead Javonte Williams 24 car 56 yds 0 TD (62% of team rushes); RB2 Tyler Goodson 7 car 14 yds 0 TD

## Target shares
- ARI (41 targets): Michael Wilson 15 tgt (37%) 8-111; Trey McBride 8 tgt (20%) 7-72; Tyler Allgeier 5 tgt (12%) 5-44; Elijah Higgins 4 tgt (10%) 2-10; Kendrick Bourne 2 tgt (5%) 1-29; Devin Duvernay 2 tgt (5%) 2-14; Bam Knight 2 tgt (5%) 1-10; Reggie Virgil 2 tgt (5%) 0-0; Simi Fehoko 1 tgt (2%) 1-17
- DAL (28 targets): CeeDee Lamb 11 tgt (39%) 7-58; Brevyn Spann-Ford 5 tgt (18%) 4-31; George Pickens 4 tgt (14%) 2-48; Ryan Flournoy 4 tgt (14%) 3-38; Tyler Goodson 2 tgt (7%) 2-19; Javonte Williams 2 tgt (7%) 1-1

## Pressure on each QB (ESPN gives sacks and QB hits; no pressure rate in public box)
- ARI QB: 5 sacks, 11 QB hits on 51 dropbacks (sack+hit rate proxy 22%; ESPN QB hits include sacks)
- DAL QB: 4 sacks, 6 QB hits on 33 dropbacks (sack+hit rate proxy 18%; ESPN QB hits include sacks)

## TD scorers / scoring plays

## Who disappeared and why
- Bam Knight Rush Yds Over 19.5: 8.0 (efficiency/share: 3 car for 8; run-defense matchup / RB-share input)
- Trey McBride Receptions Over 7.5: 7.0 (efficiency: volume came but yards/catches did not; defender coverage / matchup input)
- CeeDee Lamb Rec Yds Over 80.5: 58.0 (pass-rush script: QB sacked 4x, offense leaned run, game margin -3; opponent pressure-rate + run-lean script input)
- George Pickens Rec Yds Over 59.5: 48.0 (pass-rush script: QB sacked 4x, offense leaned run, game margin -3; opponent pressure-rate + run-lean script input)
- George Pickens Receptions Over 3.5: 2.0 (pass-rush script: QB sacked 4x, offense leaned run, game margin -3; opponent pressure-rate + run-lean script input)
- Ryan Flournoy Receptions Over 3.5: 3.0 (pass-rush script: QB sacked 4x, offense leaned run, game margin -3; opponent pressure-rate + run-lean script input)
- CeeDee Lamb rec O7.5: 7.0 (7 catches on 11 targets (39% share, so volume was there). DAL threw only 29 times with Pollard running for 137 and Prescott sacked 4 times. A 7.5 line needs about 30+ attempts or an 70%+ catch rate on deeper looks. The input was DAL's run lean as a 7-pt favorite (team pass-attempt projection); 7.5 was a high rung (judgment))

## Leg grades (runs folder legs and user slip legs)
| Group | Source | Leg | Actual | Result | Input that should have caught the miss |
|---|---|---|---|---|---|
| cut | runs/ARI@DAL | Jacoby Brissett Pass Yds Under 258.5 | 119.0 | HIT |  |
| cut | runs/ARI@DAL | Tyler Allgeier Rush Yds Over 13.5 | 147.0 | HIT |  |
| cut | runs/ARI@DAL | Bam Knight Rush Yds Over 19.5 | 8.0 | MISS | efficiency/share: 3 car for 8; run-defense matchup / RB-share input |
| cut | runs/ARI@DAL | Michael Wilson Rec Yds Under 56.5 | 111.0 | MISS | volume: 15 targets; target-share / injury-redistribution input |
| cut | runs/ARI@DAL | Michael Wilson Receptions Under 4.5 | 8.0 | MISS | volume: 15 targets; target-share / injury-redistribution input |
| cut | runs/ARI@DAL | Trey McBride Rec Yds Under 71.5 | 72.0 | MISS | volume: 8 targets; target-share / injury-redistribution input |
| cut | runs/ARI@DAL | Trey McBride Receptions Over 7.5 | 7.0 | MISS | efficiency: volume came but yards/catches did not; defender coverage / matchup input |
| cut | runs/ARI@DAL | Dak Prescott Pass Yds Under 271.5 | 195.0 | HIT |  |
| cut | runs/ARI@DAL | Javonte Williams Rush Yds Under 76.5 | 56.0 | HIT |  |
| cut | runs/ARI@DAL | Javonte Williams Rush+Rec Yds Under 92.5 | 57.0 | HIT |  |
| cut | runs/ARI@DAL | CeeDee Lamb Rec Yds Over 80.5 | 58.0 | MISS | pass-rush script: QB sacked 4x, offense leaned run, game margin -3; opponent pressure-rate + run-lean script input |
| cut | runs/ARI@DAL | CeeDee Lamb Receptions Over 6.5 | 7.0 | HIT |  |
| cut | runs/ARI@DAL | George Pickens Rec Yds Over 59.5 | 48.0 | MISS | pass-rush script: QB sacked 4x, offense leaned run, game margin -3; opponent pressure-rate + run-lean script input |
| cut | runs/ARI@DAL | George Pickens Receptions Over 3.5 | 2.0 | MISS | pass-rush script: QB sacked 4x, offense leaned run, game margin -3; opponent pressure-rate + run-lean script input |
| cut | runs/ARI@DAL | Ryan Flournoy Rec Yds Over 36.5 | 38.0 | HIT |  |
| cut | runs/ARI@DAL | Ryan Flournoy Receptions Over 3.5 | 3.0 | MISS | pass-rush script: QB sacked 4x, offense leaned run, game margin -3; opponent pressure-rate + run-lean script input |
| cut | runs/ARI@DAL | Jake Ferguson Rec Yds Over 14.5 | DNP/no stat line | VOID/NO ACTION | player had no box line; check inactive/active input |
| cut | runs/ARI@DAL | Jake Ferguson Receptions Over 1.5 | DNP/no stat line | VOID/NO ACTION | player had no box line; check inactive/active input |
| slip | PP40 | CeeDee Lamb rec O4.5 | 7.0 | HIT |  |
| slip | UD20 | CeeDee Lamb rec O4.5 | 7.0 | HIT |  |
| slip | PP20 | CeeDee Lamb rec O4.5 | 7.0 | HIT |  |
| slip | PP25 | CeeDee Lamb rec O6.5 | 7.0 | HIT |  |
| slip | PP chat | CeeDee Lamb rec O7.5 | 7.0 | MISS | 7 catches on 11 targets (39% share, so volume was there). DAL threw only 29 times with Pollard running for 137 and Prescott sacked 4 times. A 7.5 line needs about 30+ attempts or an 70%+ catch rate on deeper looks. The input was DAL's run lean as a 7-pt favorite (team pass-attempt projection); 7.5 was a high rung (judgment) |
| slip | FD7/FD8 | CeeDee Lamb recyds O49.5 | 58.0 | HIT |  |
