# LV @ NYJ game script

Final: LV 38, NYJ 33 (margin NYJ -5)
Pregame (DraftKings close, ESPN pickcenter): NYJ -1.5, total 46.5. Favorite NYJ result vs spread: -5 vs -1.5 → did not cover. Total 71 vs 46.5: OVER.
Weather actuals: 61-62F, wind 2-4 mph (gusts to 8), precip 0.0 mm over 1-4 PM ET (Open-Meteo hourly model analysis, not a stadium sensor)

**Script label: underdog upset / shootout (over by 10+)**

## Score state by quarter
- end Q1: LV 7-NYJ 6
- end Q2: LV 14-NYJ 23
- end Q3: LV 28-NYJ 30
- end Q4: LV 38-NYJ 33

## Run/pass and pace
| Team | Rush att | Pass att | Sacks taken | Dropbacks | Pass rate | Total plays | TOP | Yards | Turnovers |
|---|---|---|---|---|---|---|---|---|---|
| LV | 33 | 26 | 1 | 27 | 45% | 60 | 29:58 | 333 | 0 |
| NYJ | 27 | 32 | 2 | 34 | 56% | 61 | 30:02 | 439 | 1 |

## Backfield
- LV: lead Mike Washington Jr. 25 car 83 yds 0 TD (76% of team rushes); RB2 Ashton Jeanty 2 car 9 yds 0 TD
- NYJ: lead Braelon Allen 21 car 147 yds 1 TD (78% of team rushes); RB2 Isaiah Davis 5 car 15 yds 0 TD

## Target shares
- LV (25 targets): Brock Bowers 10 tgt (40%) 7-92; Michael Mayer 6 tgt (24%) 5-53; Ashton Jeanty 4 tgt (16%) 3-64; Jalen Nailor 4 tgt (16%) 4-38; Tre Tucker 1 tgt (4%) 0-0
- NYJ (31 targets): Garrett Wilson 12 tgt (39%) 6-83; Adonai Mitchell 9 tgt (29%) 7-142; Mason Taylor 5 tgt (16%) 3-19; Kenyon Sadiq 2 tgt (6%) 1-22; Braelon Allen 2 tgt (6%) 2-6; Isaiah Williams 1 tgt (3%) 1-18

## Pressure on each QB (ESPN gives sacks and QB hits; no pressure rate in public box)
- LV QB: 1 sacks, 6 QB hits on 27 dropbacks (sack+hit rate proxy 22%; ESPN QB hits include sacks)
- NYJ QB: 2 sacks, 3 QB hits on 34 dropbacks (sack+hit rate proxy 9%; ESPN QB hits include sacks)

## TD scorers / scoring plays

## Who disappeared and why
- Tre Tucker Rec Yds Over 48.5: 0.0 (volume: only 1 targets; target-share/QB-volume input (team led by 5))
- Tre Tucker Receptions Over 3.5: 0.0 (1 official target (plus a DPI no-play) in a 26-attempt game where Bowers got 10. The gate passed it on season target share without a current-week route/role check. Role-share input (snap/route data was not in the folder) (judgment))

## Score check
The user's screenshot at 2:00 in Q4 showed LV 35-33. That matches the play log: the Jason Sanders 31-yd FG at 4:31 Q4 made it 35-33. Matt Gay's 53-yd FG at 0:27 Q4 made the final LV 38-33 (ESPN STATUS_FINAL, re-checked).

## Leg grades (runs folder legs and user slip legs)
| Group | Source | Leg | Actual | Result | Input that should have caught the miss |
|---|---|---|---|---|---|
| cut | runs/LV@NYJ | Kirk Cousins Pass Yds Over 232.5 | 247.0 | HIT |  |
| cut | runs/LV@NYJ | Brock Bowers Rec Yds Over 68.5 | 92.0 | HIT |  |
| cut | runs/LV@NYJ | Brock Bowers Receptions Under 5.5 | 7.0 | MISS | volume: 10 targets; target-share / injury-redistribution input |
| cut | runs/LV@NYJ | Tre Tucker Rec Yds Over 48.5 | 0.0 | MISS | volume: only 1 targets; target-share/QB-volume input (team led by 5) |
| passed | runs/LV@NYJ | Tre Tucker Receptions Over 3.5 | 0.0 | MISS | 1 official target (plus a DPI no-play) in a 26-attempt game where Bowers got 10. The gate passed it on season target share without a current-week route/role check. Role-share input (snap/route data was not in the folder) (judgment) |
| cut | runs/LV@NYJ | Geno Smith Pass Yds Under 225.5 | 290.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/LV@NYJ | Garrett Wilson Rec Yds Under 63.5 | 83.0 | MISS | volume: 12 targets; target-share / injury-redistribution input |
| cut | runs/LV@NYJ | Garrett Wilson Receptions Under 5.5 | 6.0 | MISS | volume: 12 targets; target-share / injury-redistribution input |
| cut | runs/LV@NYJ | Omar Cooper Jr. Rec Yds Over 41.5 | DNP/no stat line | VOID/NO ACTION | player had no box line; check inactive/active input |
| cut | runs/LV@NYJ | Omar Cooper Jr. Receptions Under 3.5 | DNP/no stat line | VOID/NO ACTION | player had no box line; check inactive/active input |
| slip | PP40 | Brock Bowers targets O8.5 | 10.0 | HIT |  |
| slip | UD20 | Brock Bowers recyds O49.5 | 92.0 | HIT |  |
| slip | PP20 | Brock Bowers halves w/25+ rec yds O1.5 | 2 (H1 40, H2 52) | HIT |  |
| slip | FD7/FD8 | Brock Bowers recyds O49.5 | 92.0 | HIT |  |
