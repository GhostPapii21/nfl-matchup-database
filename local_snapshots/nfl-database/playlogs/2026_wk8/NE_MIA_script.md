# NE @ MIA game script

Final: NE 24, MIA 19 (margin MIA -5)
Pregame (DraftKings close, ESPN pickcenter): NE -7, total 41.5. Favorite NE result vs spread: +5 vs -7.0 → did not cover. Total 43 vs 41.5: OVER.
Weather actuals: 75-77F, wind 5-9 mph (gusts to 20), precip 0.0 mm over 4-7 PM ET (Open-Meteo hourly model analysis, not a stadium sensor)

**Script label: favorite close win**

## Score state by quarter
- end Q1: NE 3-MIA 3
- end Q2: NE 3-MIA 13
- end Q3: NE 17-MIA 13
- end Q4: NE 24-MIA 19

## Run/pass and pace
| Team | Rush att | Pass att | Sacks taken | Dropbacks | Pass rate | Total plays | TOP | Yards | Turnovers |
|---|---|---|---|---|---|---|---|---|---|
| NE | 36 | 20 | 3 | 23 | 39% | 59 | 31:57 | 313 | 1 |
| MIA | 23 | 32 | 5 | 37 | 62% | 60 | 28:03 | 269 | 1 |

## Backfield
- NE: lead Rhamondre Stevenson 19 car 82 yds 0 TD (53% of team rushes); RB2 Corey Kiner 7 car 38 yds 0 TD
- MIA: lead Ollie Gordon II 19 car 69 yds 0 TD (83% of team rushes); RB2 Jaylen Wright 2 car 5 yds 0 TD

## Target shares
- NE (19 targets): Efton Chism III 5 tgt (26%) 5-37; Eli Raridon 4 tgt (21%) 1-5; DeMario Douglas 3 tgt (16%) 3-76; Hunter Henry 3 tgt (16%) 3-30; Rhamondre Stevenson 3 tgt (16%) 3-8; Kyle Williams 1 tgt (5%) 1-43
- MIA (30 targets): Greg Dulcich 6 tgt (20%) 4-43; Caleb Douglas 6 tgt (20%) 4-43; Malik Washington 6 tgt (20%) 5-40; Chris Bell 5 tgt (17%) 4-31; Kevin Coleman Jr. 3 tgt (10%) 3-46; Jalen Tolbert 1 tgt (3%) 1-8; Jaylen Wright 1 tgt (3%) 0-0; Ollie Gordon II 1 tgt (3%) 0-0; Will Kacmarek 1 tgt (3%) 0-0

## Pressure on each QB (ESPN gives sacks and QB hits; no pressure rate in public box)
- NE QB: 3 sacks, 3 QB hits on 23 dropbacks (sack+hit rate proxy 13%; ESPN QB hits include sacks)
- MIA QB: 5 sacks, 9 QB hits on 37 dropbacks (sack+hit rate proxy 24%; ESPN QB hits include sacks)

## TD scorers / scoring plays
- Q2 0:08 MIA: Malik Washington 1 Yd pass from Malik Willis (Zane Gonzalez Kick) (NE 3-MIA 13)
- Q3 9:23 NE: Kyle Williams 43 Yd pass from Drake Maye (Andy Borregales Kick) (NE 10-MIA 13)
- Q3 0:59 NE: Drake Maye 2 Yd Rush (Andy Borregales Kick) (NE 17-MIA 13)
- Q4 12:39 NE: DeMario Douglas 48 Yd pass from Drake Maye (Andy Borregales Kick) (NE 24-MIA 13)
- Q4 2:04 MIA: Kevin Coleman Jr. 35 Yd pass from Malik Willis (Two-Point Pass Conversion Failed) (NE 24-MIA 19)

## Who disappeared and why
- Drake Maye Pass Yds Over 239.5: 199.0 (efficiency: volume came but yards/catches did not; defender coverage / matchup input)
- Malik Washington Rec Yds Over 41.5: 40.0 (pass-rush script: QB sacked 5x, offense leaned run, game margin -5; opponent pressure-rate + run-lean script input)

## Leg grades (runs folder legs and user slip legs)
| Group | Source | Leg | Actual | Result | Input that should have caught the miss |
|---|---|---|---|---|---|
| cut | runs/NE@MIA | Drake Maye Pass Yds Over 239.5 | 199.0 | MISS | efficiency: volume came but yards/catches did not; defender coverage / matchup input |
| cut | runs/NE@MIA | Rhamondre Stevenson Rush Yds Under 58.5 | 82.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/NE@MIA | Rhamondre Stevenson Rush+Rec Yds Under 87.5 | 90.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/NE@MIA | DeMario Douglas Rec Yds Under 40.5 | 76.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/NE@MIA | DeMario Douglas Receptions Under 3.5 | 3.0 | HIT |  |
| cut | runs/NE@MIA | Hunter Henry Rec Yds Under 45.5 | 30.0 | HIT |  |
| cut | runs/NE@MIA | Hunter Henry Receptions Under 4.5 | 3.0 | HIT |  |
| cut | runs/NE@MIA | Eli Raridon Rec Yds Under 27.5 | 5.0 | HIT |  |
| cut | runs/NE@MIA | Eli Raridon Receptions Under 2.5 | 1.0 | HIT |  |
| cut | runs/NE@MIA | Malik Willis Pass Yds Under 185.5 | 211.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/NE@MIA | Ollie Gordon II Rush Yds Under 64.5 | 69.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/NE@MIA | Ollie Gordon II Rush+Rec Yds Under 78.5 | 69.0 | HIT |  |
| cut | runs/NE@MIA | Malik Washington Rec Yds Over 41.5 | 40.0 | MISS | pass-rush script: QB sacked 5x, offense leaned run, game margin -5; opponent pressure-rate + run-lean script input |
| cut | runs/NE@MIA | Malik Washington Receptions Under 4.5 | 5.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/NE@MIA | Greg Dulcich Rec Yds Over 29.5 | 43.0 | HIT |  |
| cut | runs/NE@MIA | Greg Dulcich Receptions Over 3.5 | 4.0 | HIT |  |
