# CLE @ PIT game script

Final: CLE 6, PIT 27 (margin PIT +21)
Pregame (DraftKings close, ESPN pickcenter): PIT -3.5, total 38.5. Favorite PIT result vs spread: +21 vs -3.5 → covered. Total 33 vs 38.5: UNDER.
Weather actuals: 66-70F, wind 4-5 mph (gusts to 11), precip 0.0 mm over 1-4 PM ET (Open-Meteo hourly model analysis, not a stadium sensor)

**Script label: favorite blowout, clock-kill second half**

## Score state by quarter
- end Q1: CLE 0-PIT 7
- end Q2: CLE 6-PIT 20
- end Q3: CLE 6-PIT 27
- end Q4: CLE 6-PIT 27

## Run/pass and pace
| Team | Rush att | Pass att | Sacks taken | Dropbacks | Pass rate | Total plays | TOP | Yards | Turnovers |
|---|---|---|---|---|---|---|---|---|---|
| CLE | 15 | 41 | 8 | 49 | 77% | 64 | 30:15 | 319 | 2 |
| PIT | 33 | 25 | 1 | 26 | 44% | 59 | 29:45 | 361 | 1 |

## Backfield
- CLE: lead Quinshon Judkins 11 car 25 yds 0 TD (73% of team rushes); RB2 Dylan Sampson 1 car 7 yds 0 TD
- PIT: lead Jaylen Warren 17 car 143 yds 1 TD (52% of team rushes); RB2 Rico Dowdle 15 car 56 yds 1 TD

## Target shares
- CLE (40 targets): Harold Fannin Jr. 12 tgt (30%) 10-154; Denzel Boston 11 tgt (28%) 6-37; Dylan Sampson 8 tgt (20%) 6-62; KC Concepcion 4 tgt (10%) 3-37; Quinshon Judkins 2 tgt (5%) 2-24; Blake Whiteheart 1 tgt (2%) 1-9; Tylan Wallace 1 tgt (2%) 1-3; Jerry Jeudy 1 tgt (2%) 0-0
- PIT (22 targets): DK Metcalf 6 tgt (27%) 1-4; Darnell Washington 5 tgt (23%) 3-94; Germie Bernard 5 tgt (23%) 5-30; Pat Freiermuth 2 tgt (9%) 2-35; Jaylen Warren 2 tgt (9%) 1-0; Brandon Johnson 1 tgt (5%) 1-9; Riley Nowakowski 1 tgt (5%) 0-0

## Pressure on each QB (ESPN gives sacks and QB hits; no pressure rate in public box)
- CLE QB: 8 sacks, 13 QB hits on 49 dropbacks (sack+hit rate proxy 27%; ESPN QB hits include sacks)
- PIT QB: 1 sacks, 2 QB hits on 26 dropbacks (sack+hit rate proxy 8%; ESPN QB hits include sacks)

## TD scorers / scoring plays

## Who disappeared and why
- Quinshon Judkins Rush Yds Over 47.5: 25.0 (game script: team trailed by 21; spread/script input (negative script for RB overs))
- Quinshon Judkins Rush+Rec Yds Over 61.5: 49.0 (game script: team trailed by 21; spread/script input (negative script for RB overs))
- Jerry Jeudy Rec Yds Over 21.5: 0.0 (pass-rush script: QB sacked 8x, offense leaned run, game margin -21; opponent pressure-rate + run-lean script input)
- Jerry Jeudy Receptions Over 2.5: 0.0 (pass-rush script: QB sacked 8x, offense leaned run, game margin -21; opponent pressure-rate + run-lean script input)
- Germie Bernard Rec Yds Over 43.5: 30.0 (efficiency: volume came but yards/catches did not; defender coverage / matchup input)

## Leg grades (runs folder legs and user slip legs)
| Group | Source | Leg | Actual | Result | Input that should have caught the miss |
|---|---|---|---|---|---|
| cut | runs/CLE@PIT | Deshaun Watson Pass Yds Under 210.5 | 324.0 | MISS | game script: team trailed by 21 and threw late; spread/negative-script input |
| cut | runs/CLE@PIT | Quinshon Judkins Rush Yds Over 47.5 | 25.0 | MISS | game script: team trailed by 21; spread/script input (negative script for RB overs) |
| cut | runs/CLE@PIT | Quinshon Judkins Rush+Rec Yds Over 61.5 | 49.0 | MISS | game script: team trailed by 21; spread/script input (negative script for RB overs) |
| cut | runs/CLE@PIT | Jerry Jeudy Rec Yds Over 21.5 | 0.0 | MISS | pass-rush script: QB sacked 8x, offense leaned run, game margin -21; opponent pressure-rate + run-lean script input |
| cut | runs/CLE@PIT | Jerry Jeudy Receptions Over 2.5 | 0.0 | MISS | pass-rush script: QB sacked 8x, offense leaned run, game margin -21; opponent pressure-rate + run-lean script input |
| cut | runs/CLE@PIT | KC Concepcion Rec Yds Under 46.5 | 37.0 | HIT |  |
| cut | runs/CLE@PIT | KC Concepcion Receptions Under 4.5 | 3.0 | HIT |  |
| cut | runs/CLE@PIT | Denzel Boston Rec Yds Under 47.5 | 37.0 | HIT |  |
| cut | runs/CLE@PIT | Denzel Boston Receptions Under 3.5 | 6.0 | MISS | volume: 11 targets; target-share / injury-redistribution input |
| cut | runs/CLE@PIT | Harold Fannin Jr. Rec Yds Under 34.5 | 154.0 | MISS | volume: 12 targets; target-share / injury-redistribution input |
| cut | runs/CLE@PIT | Harold Fannin Jr. Receptions Under 3.5 | 10.0 | MISS | volume: 12 targets; target-share / injury-redistribution input |
| cut | runs/CLE@PIT | Aaron Rodgers Pass Yds Under 218.5 | 172.0 | HIT |  |
| cut | runs/CLE@PIT | Jaylen Warren Rush Yds Over 64.5 | 143.0 | HIT |  |
| cut | runs/CLE@PIT | Jaylen Warren Rush+Rec Yds Over 91.5 | 143.0 | HIT |  |
| cut | runs/CLE@PIT | DK Metcalf Rec Yds Under 52.5 | 4.0 | HIT |  |
| cut | runs/CLE@PIT | DK Metcalf Receptions Under 4.5 | 1.0 | HIT |  |
| cut | runs/CLE@PIT | Germie Bernard Rec Yds Over 43.5 | 30.0 | MISS | efficiency: volume came but yards/catches did not; defender coverage / matchup input |
| cut | runs/CLE@PIT | Germie Bernard Receptions Under 4.5 | 5.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/CLE@PIT | Darnell Washington Rec Yds Under 20.5 | 94.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/CLE@PIT | Darnell Washington Receptions Under 2.5 | 3.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| slip | UD20 | Denzel Boston recyds O29.5 | 37.0 | HIT |  |
| slip | PP25 | Jaylen Warren rushrec O69.5 | 143.0 | HIT |  |
| slip | PP chat | Jaylen Warren fantasy O14.5 | 21.3 | HIT |  |
