# BAL @ BUF game script

Final: BAL 10, BUF 36 (margin BUF +26)
Pregame (DraftKings close, ESPN pickcenter): BUF -3, total 54.5. Favorite BUF result vs spread: +26 vs -3.0 → covered. Total 46 vs 54.5: UNDER.
Weather actuals: 66-70F, wind 4-9 mph (gusts to 11), precip 0.0 mm over 1-4 PM ET (Open-Meteo hourly model analysis, not a stadium sensor)

**Script label: favorite blowout, clock-kill second half**

## Score state by quarter
- end Q1: BAL 7-BUF 10
- end Q2: BAL 7-BUF 16
- end Q3: BAL 10-BUF 23
- end Q4: BAL 10-BUF 36

## Run/pass and pace
| Team | Rush att | Pass att | Sacks taken | Dropbacks | Pass rate | Total plays | TOP | Yards | Turnovers |
|---|---|---|---|---|---|---|---|---|---|
| BAL | 19 | 26 | 4 | 30 | 61% | 49 | 22:24 | 145 | 3 |
| BUF | 41 | 34 | 1 | 35 | 46% | 76 | 37:36 | 426 | 2 |

## Backfield
- BAL: lead Derrick Henry 11 car 53 yds 1 TD (58% of team rushes); RB2 Justice Hill 3 car 15 yds 0 TD
- BUF: lead James Cook III 21 car 80 yds 1 TD (51% of team rushes); RB2 Ray Davis 6 car 30 yds 0 TD

## Target shares
- BAL (26 targets): Justice Hill 8 tgt (31%) 4-20; Zay Flowers 5 tgt (19%) 0-0; Mark Andrews 4 tgt (15%) 3-14; Rashod Bateman 3 tgt (12%) 1-22; Josh Cuevas 2 tgt (8%) 1-15; Derrick Henry 2 tgt (8%) 2-7; Ja'Kobi Lane 1 tgt (4%) 1-13; Matt Hibner 1 tgt (4%) 0-0
- BUF (33 targets): DJ Moore 7 tgt (21%) 4-82; Dalton Kincaid 6 tgt (18%) 4-86; Khalil Shakir 6 tgt (18%) 5-64; James Cook III 3 tgt (9%) 2-21; Ty Johnson 3 tgt (9%) 3-19; Keon Coleman 3 tgt (9%) 1-4; Jackson Hawes 2 tgt (6%) 1-7; Dawson Knox 2 tgt (6%) 1-6; Joshua Palmer 1 tgt (3%) 0-0

## Pressure on each QB (ESPN gives sacks and QB hits; no pressure rate in public box)
- BAL QB: 4 sacks, 12 QB hits on 30 dropbacks (sack+hit rate proxy 40%; ESPN QB hits include sacks)
- BUF QB: 1 sacks, 5 QB hits on 35 dropbacks (sack+hit rate proxy 14%; ESPN QB hits include sacks)

## TD scorers / scoring plays

## Who disappeared and why
- Zay Flowers Rec Yds Over 82.5: 0.0 (efficiency: volume came but yards/catches did not; defender coverage / matchup input)
- Zay Flowers Receptions Over 6.5: 0.0 (efficiency: volume came but yards/catches did not; defender coverage / matchup input)
- Rashod Bateman Rec Yds Over 23.5: 22.0 (volume: only 3 targets; target-share/QB-volume input (team trailed by 26))
- Mark Andrews Rec Yds Over 27.5: 14.0 (volume: only 4 targets; target-share/QB-volume input (team trailed by 26))
- Keon Coleman Rec Yds Over 29.5: 4.0 (volume: only 3 targets; target-share/QB-volume input (team led by 26))
- Keon Coleman Receptions Over 2.5: 1.0 (volume: only 3 targets; target-share/QB-volume input (team led by 26))
- Zay Flowers rec O6: 0.0 (0-for-5. Lamar Jackson got hurt on his first throw (Q1 10:04, 0/1). Fagnano (10/21, 91 yds; one INT on a ball to Flowers, by Igbinosun) and Huntley (2/4, 0 yds) finished. You can't price in-game QB injury pregame, but BAL's backup-QB floor plus BUF's 35% blitz (the 'Panthers-rule risk' already flagged on the slip) made a WR1 over fragile. QB-health and backup-floor input (judgment))
- Zay Flowers recyds O49.5: 0.0 (0-for-5. Lamar Jackson got hurt on his first throw (Q1 10:04, 0/1). Fagnano (10/21, 91 yds; one INT on a ball to Flowers, by Igbinosun) and Huntley (2/4, 0 yds) finished. You can't price in-game QB injury pregame, but BAL's backup-QB floor plus BUF's 35% blitz (the 'Panthers-rule risk' already flagged on the slip) made a WR1 over fragile. QB-health and backup-floor input (judgment))
- Zay Flowers recyds O59.5: 0.0 (0-for-5. Lamar Jackson got hurt on his first throw (Q1 10:04, 0/1). Fagnano (10/21, 91 yds; one INT on a ball to Flowers, by Igbinosun) and Huntley (2/4, 0 yds) finished. You can't price in-game QB injury pregame, but BAL's backup-QB floor plus BUF's 35% blitz (the 'Panthers-rule risk' already flagged on the slip) made a WR1 over fragile. QB-health and backup-floor input (judgment))

## Leg grades (runs folder legs and user slip legs)
| Group | Source | Leg | Actual | Result | Input that should have caught the miss |
|---|---|---|---|---|---|
| cut | runs/BAL@BUF | Lamar Jackson Pass Yds Under 237.5 | 0.0 | HIT |  |
| cut | runs/BAL@BUF | Derrick Henry Rush Yds Under 78.5 | 53.0 | HIT |  |
| cut | runs/BAL@BUF | Derrick Henry Rush+Rec Yds Under 89.5 | 60.0 | HIT |  |
| cut | runs/BAL@BUF | Zay Flowers Rec Yds Over 82.5 | 0.0 | MISS | efficiency: volume came but yards/catches did not; defender coverage / matchup input |
| cut | runs/BAL@BUF | Zay Flowers Receptions Over 6.5 | 0.0 | MISS | efficiency: volume came but yards/catches did not; defender coverage / matchup input |
| cut | runs/BAL@BUF | Rashod Bateman Rec Yds Over 23.5 | 22.0 | MISS | volume: only 3 targets; target-share/QB-volume input (team trailed by 26) |
| cut | runs/BAL@BUF | Rashod Bateman Receptions Under 2.5 | 1.0 | HIT |  |
| cut | runs/BAL@BUF | Mark Andrews Rec Yds Over 27.5 | 14.0 | MISS | volume: only 4 targets; target-share/QB-volume input (team trailed by 26) |
| cut | runs/BAL@BUF | Mark Andrews Receptions Under 3.5 | 3.0 | HIT |  |
| cut | runs/BAL@BUF | Josh Allen Pass Yds Under 247.5 | 289.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/BAL@BUF | James Cook Rush Yds Under 82.5 | 80.0 | HIT |  |
| cut | runs/BAL@BUF | James Cook Rush+Rec Yds Under 96.5 | 101.0 | MISS | game script: team led by 26, clock-kill carries; spread/positive-script input |
| cut | runs/BAL@BUF | DJ Moore Rec Yds Over 49.5 | 82.0 | HIT |  |
| cut | runs/BAL@BUF | DJ Moore Receptions Under 4.5 | 4.0 | HIT |  |
| cut | runs/BAL@BUF | Khalil Shakir Rec Yds Under 41.5 | 64.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/BAL@BUF | Khalil Shakir Receptions Under 3.5 | 5.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/BAL@BUF | Keon Coleman Rec Yds Over 29.5 | 4.0 | MISS | volume: only 3 targets; target-share/QB-volume input (team led by 26) |
| cut | runs/BAL@BUF | Keon Coleman Receptions Over 2.5 | 1.0 | MISS | volume: only 3 targets; target-share/QB-volume input (team led by 26) |
| cut | runs/BAL@BUF | Dalton Kincaid Rec Yds Under 46.5 | 86.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/BAL@BUF | Dalton Kincaid Receptions Under 3.5 | 4.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| slip | PP25 | Zay Flowers rec O6 | 0.0 | MISS | 0-for-5. Lamar Jackson got hurt on his first throw (Q1 10:04, 0/1). Fagnano (10/21, 91 yds; one INT on a ball to Flowers, by Igbinosun) and Huntley (2/4, 0 yds) finished. You can't price in-game QB injury pregame, but BAL's backup-QB floor plus BUF's 35% blitz (the 'Panthers-rule risk' already flagged on the slip) made a WR1 over fragile. QB-health and backup-floor input (judgment) |
| slip | UD20 | Zay Flowers recyds O49.5 | 0.0 | MISS | 0-for-5. Lamar Jackson got hurt on his first throw (Q1 10:04, 0/1). Fagnano (10/21, 91 yds; one INT on a ball to Flowers, by Igbinosun) and Huntley (2/4, 0 yds) finished. You can't price in-game QB injury pregame, but BAL's backup-QB floor plus BUF's 35% blitz (the 'Panthers-rule risk' already flagged on the slip) made a WR1 over fragile. QB-health and backup-floor input (judgment) |
| slip | FD7/FD8 | Zay Flowers recyds O59.5 | 0.0 | MISS | 0-for-5. Lamar Jackson got hurt on his first throw (Q1 10:04, 0/1). Fagnano (10/21, 91 yds; one INT on a ball to Flowers, by Igbinosun) and Huntley (2/4, 0 yds) finished. You can't price in-game QB injury pregame, but BAL's backup-QB floor plus BUF's 35% blitz (the 'Panthers-rule risk' already flagged on the slip) made a WR1 over fragile. QB-health and backup-floor input (judgment) |
| slip | PP chat | James Cook rushyds O59.5 | 80.0 | HIT |  |
