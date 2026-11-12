# IND @ JAX game script

Final: IND 7, JAX 42 (margin JAX +35)
Pregame (DraftKings close, ESPN pickcenter): JAX -10.5, total 45.5. Favorite JAX result vs spread: +35 vs -10.5 → covered. Total 49 vs 45.5: OVER.
Weather actuals: 75-77F, wind 6-10 mph (gusts to 20), precip 1.1 mm over 1-4 PM ET (Open-Meteo hourly model analysis, not a stadium sensor)

**Script label: favorite blowout, clock-kill second half**

## Score state by quarter
- end Q1: IND 0-JAX 7
- end Q2: IND 0-JAX 28
- end Q3: IND 7-JAX 42
- end Q4: IND 7-JAX 42

## Run/pass and pace
| Team | Rush att | Pass att | Sacks taken | Dropbacks | Pass rate | Total plays | TOP | Yards | Turnovers |
|---|---|---|---|---|---|---|---|---|---|
| IND | 26 | 30 | 4 | 34 | 57% | 60 | 30:22 | 243 | 3 |
| JAX | 33 | 17 | 3 | 20 | 38% | 53 | 29:38 | 366 | 1 |

## Backfield
- IND: lead Jonathan Taylor 8 car 23 yds 0 TD (31% of team rushes); RB2 DJ Giddens 6 car 43 yds 0 TD
- JAX: lead Bhayshul Tuten 16 car 104 yds 1 TD (48% of team rushes); RB2 Chris Rodriguez Jr. 6 car 41 yds 1 TD

## Target shares
- IND (30 targets): Tyler Warren 10 tgt (33%) 4-18; Keenan Allen 7 tgt (23%) 7-67; Jonathan Taylor 5 tgt (17%) 4-24; Josh Downs 5 tgt (17%) 4-23; Laquon Treadwell 2 tgt (7%) 1-18; Deion Burks 1 tgt (3%) 1-2
- JAX (17 targets): Jakobi Meyers 3 tgt (18%) 2-24; Bhayshul Tuten 2 tgt (12%) 2-55; Brenton Strange 2 tgt (12%) 2-55; Parker Washington 2 tgt (12%) 1-16; Brian Thomas Jr. 2 tgt (12%) 1-12; Nate Boerkircher 1 tgt (6%) 1-31; Chris Rodriguez Jr. 1 tgt (6%) 1-17; Tanner Koziol 1 tgt (6%) 1-8; Travis Hunter 1 tgt (6%) 0-0; Josh Cameron 1 tgt (6%) 0-0; LeQuint Allen Jr. 1 tgt (6%) 0-0

## Pressure on each QB (ESPN gives sacks and QB hits; no pressure rate in public box)
- IND QB: 4 sacks, 11 QB hits on 34 dropbacks (sack+hit rate proxy 32%; ESPN QB hits include sacks)
- JAX QB: 3 sacks, 4 QB hits on 20 dropbacks (sack+hit rate proxy 20%; ESPN QB hits include sacks)

## TD scorers / scoring plays

## Who disappeared and why
- Daniel Jones Pass Yds Over 192.5: 144.0 (efficiency: volume came but yards/catches did not; defender coverage / matchup input)
- Jonathan Taylor Rush Yds Over 50.5: 23.0 (game script: team trailed by 35; spread/script input (negative script for RB overs))
- Jonathan Taylor Rush+Rec Yds Over 70.5: 47.0 (game script: team trailed by 35; spread/script input (negative script for RB overs))
- Josh Downs Rec Yds Over 32.5: 23.0 (efficiency: volume came but yards/catches did not; defender coverage / matchup input)
- Tyler Warren Rec Yds Over 39.5: 18.0 (efficiency: volume came but yards/catches did not; defender coverage / matchup input)
- Tyler Warren Receptions Over 4.5: 4.0 (efficiency: volume came but yards/catches did not; defender coverage / matchup input)
- Parker Washington Rec Yds Over 59.5: 16.0 (volume: only 2 targets; target-share/QB-volume input (team led by 35))
- Brenton Strange Receptions Over 2.5: 2.0 (volume: only 2 targets; target-share/QB-volume input (team led by 35))
- Parker Washington recyds O39.5: 16.0 (2 targets. JAX led by 35 and threw only 17 times. The JAX -10.5 blowout script should have capped WR2 volume; spread/script input (judgment))

## Leg grades (runs folder legs and user slip legs)
| Group | Source | Leg | Actual | Result | Input that should have caught the miss |
|---|---|---|---|---|---|
| cut | runs/IND@JAX | Daniel Jones Pass Yds Over 192.5 | 144.0 | MISS | efficiency: volume came but yards/catches did not; defender coverage / matchup input |
| cut | runs/IND@JAX | Jonathan Taylor Rush Yds Over 50.5 | 23.0 | MISS | game script: team trailed by 35; spread/script input (negative script for RB overs) |
| cut | runs/IND@JAX | Jonathan Taylor Rush+Rec Yds Over 70.5 | 47.0 | MISS | game script: team trailed by 35; spread/script input (negative script for RB overs) |
| cut | runs/IND@JAX | Josh Downs Rec Yds Over 32.5 | 23.0 | MISS | efficiency: volume came but yards/catches did not; defender coverage / matchup input |
| cut | runs/IND@JAX | Josh Downs Receptions Over 3.5 | 4.0 | HIT |  |
| cut | runs/IND@JAX | Keenan Allen Rec Yds Over 35.5 | 67.0 | HIT |  |
| cut | runs/IND@JAX | Keenan Allen Receptions Over 4.5 | 7.0 | HIT |  |
| cut | runs/IND@JAX | Tyler Warren Rec Yds Over 39.5 | 18.0 | MISS | efficiency: volume came but yards/catches did not; defender coverage / matchup input |
| cut | runs/IND@JAX | Tyler Warren Receptions Over 4.5 | 4.0 | MISS | efficiency: volume came but yards/catches did not; defender coverage / matchup input |
| cut | runs/IND@JAX | Trevor Lawrence Pass Yds Under 237.5 | 210.0 | HIT |  |
| cut | runs/IND@JAX | Bhayshul Tuten Rush Yds Over 59.5 | 104.0 | HIT |  |
| cut | runs/IND@JAX | Bhayshul Tuten Rush+Rec Yds Over 83.5 | 159.0 | HIT |  |
| cut | runs/IND@JAX | Parker Washington Rec Yds Over 59.5 | 16.0 | MISS | volume: only 2 targets; target-share/QB-volume input (team led by 35) |
| cut | runs/IND@JAX | Parker Washington Receptions Under 4.5 | 1.0 | HIT |  |
| cut | runs/IND@JAX | Brenton Strange Rec Yds Under 41.5 | 55.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/IND@JAX | Brenton Strange Receptions Over 2.5 | 2.0 | MISS | volume: only 2 targets; target-share/QB-volume input (team led by 35) |
| slip | FD7/FD8 | Parker Washington recyds O39.5 | 16.0 | MISS | 2 targets. JAX led by 35 and threw only 17 times. The JAX -10.5 blowout script should have capped WR2 volume; spread/script input (judgment) |
