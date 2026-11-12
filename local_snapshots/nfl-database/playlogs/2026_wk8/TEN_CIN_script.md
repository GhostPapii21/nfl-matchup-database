# TEN @ CIN game script

Final: TEN 36, CIN 43 (margin CIN +7)
Pregame (DraftKings close, ESPN pickcenter): CIN -13.5, total 45.5. Favorite CIN result vs spread: +7 vs -13.5 → did not cover. Total 79 vs 45.5: OVER.
Weather actuals: 68-70F, wind 1-2 mph (gusts to 5), precip 0.0 mm over 1-4 PM ET (Open-Meteo hourly model analysis, not a stadium sensor)

**Script label: overtime shootout: 13.5-pt favorite CIN won 43-36 in OT, 34 over the total**

## Score state by quarter
- end Q1: TEN 13-CIN 0
- end Q2: TEN 13-CIN 14
- end Q3: TEN 21-CIN 23
- end Q4: TEN 36-CIN 36
- end Q5: TEN 36-CIN 43

## Run/pass and pace
| Team | Rush att | Pass att | Sacks taken | Dropbacks | Pass rate | Total plays | TOP | Yards | Turnovers |
|---|---|---|---|---|---|---|---|---|---|
| TEN | 28 | 40 | 2 | 42 | 60% | 70 | 32:11 | 440 | 2 |
| CIN | 19 | 48 | 3 | 51 | 73% | 70 | 32:12 | 510 | 4 |

## Backfield
- TEN: lead Tony Pollard 21 car 117 yds 2 TD (75% of team rushes); RB2 none
- CIN: lead Chase Brown 12 car 55 yds 0 TD (63% of team rushes); RB2 Samaje Perine 4 car 10 yds 0 TD

## Target shares
- TEN (39 targets): Gunnar Helm 9 tgt (23%) 5-76; Wan'Dale Robinson 7 tgt (18%) 6-57; Chimere Dike 6 tgt (15%) 5-71; Elic Ayomanor 5 tgt (13%) 3-34; Tony Pollard 5 tgt (13%) 3-20; Daniel Bellinger 4 tgt (10%) 3-36; Calvin Ridley 3 tgt (8%) 1-10
- CIN (47 targets): Ja'Marr Chase 16 tgt (34%) 11-141; Tee Higgins 11 tgt (23%) 10-155; Chase Brown 9 tgt (19%) 8-46; Mike Gesicki 6 tgt (13%) 4-76; Dohnte Meyers 3 tgt (6%) 3-34; Samaje Perine 1 tgt (2%) 1-9; Jack Endries 1 tgt (2%) 1-1

## Pressure on each QB (ESPN gives sacks and QB hits; no pressure rate in public box)
- TEN QB: 2 sacks, 7 QB hits on 42 dropbacks (sack+hit rate proxy 17%; ESPN QB hits include sacks)
- CIN QB: 3 sacks, 9 QB hits on 51 dropbacks (sack+hit rate proxy 18%; ESPN QB hits include sacks)

## TD scorers / scoring plays

## Who disappeared and why
- none among graded over legs

## Leg grades (runs folder legs and user slip legs)
| Group | Source | Leg | Actual | Result | Input that should have caught the miss |
|---|---|---|---|---|---|
| cut | runs/TEN@CIN | Cam Ward Pass Yds Under 192.5 | 304.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/TEN@CIN | Tony Pollard Rush Yds Over 65.5 | 117.0 | HIT |  |
| cut | runs/TEN@CIN | Tony Pollard Rush+Rec Yds Under 84.5 | 137.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/TEN@CIN | Joe Burrow Pass Yds Over 249.5 | 462.0 | HIT |  |
| cut | runs/TEN@CIN | Chase Brown Rush Yds Under 58.5 | 55.0 | HIT |  |
| cut | runs/TEN@CIN | Chase Brown Rush+Rec Yds Under 81.5 | 101.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/TEN@CIN | Ja'Marr Chase Rec Yds Under 79.5 | 141.0 | MISS | volume: 16 targets; target-share / injury-redistribution input |
| cut | runs/TEN@CIN | Ja'Marr Chase Receptions Under 6.5 | 11.0 | MISS | volume: 16 targets; target-share / injury-redistribution input |
| cut | runs/TEN@CIN | Tee Higgins Rec Yds Over 69.5 | 155.0 | HIT |  |
| cut | runs/TEN@CIN | Tee Higgins Receptions Over 4.5 | 10.0 | HIT |  |
| cut | runs/TEN@CIN | Mike Gesicki Rec Yds Under 22.5 | 76.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/TEN@CIN | Mike Gesicki Receptions Under 2.5 | 4.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| slip | PP40 | Tee Higgins fantasy O14.5 | 37.5 | HIT |  |
| slip | PP20 | Tee Higgins recyds O68.5 | 155.0 | HIT |  |
| slip | FD7/FD8 | Tee Higgins rec O3.5 | 10.0 | HIT |  |
