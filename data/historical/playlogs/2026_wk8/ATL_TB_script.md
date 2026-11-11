# ATL @ TB game script

Final: ATL 0, TB 16 (margin TB +16)
Pregame (DraftKings close, ESPN pickcenter): TB -2.5, total 43.5. Favorite TB result vs spread: +16 vs -2.5 → covered. Total 16 vs 43.5: UNDER.
Weather actuals: 73-75F, wind 7-12 mph (gusts to 26), precip 5.7 mm over 1-4 PM ET (Open-Meteo hourly model analysis, not a stadium sensor)

**Script label: rain run-fest: TB 56 rushes vs 3 passes, ATL QB collapse (4 INT); defensive slog, shutout**

## Score state by quarter
- end Q1: ATL 0-TB 6
- end Q2: ATL 0-TB 9
- end Q3: ATL 0-TB 16
- end Q4: ATL 0-TB 16

## Run/pass and pace
| Team | Rush att | Pass att | Sacks taken | Dropbacks | Pass rate | Total plays | TOP | Yards | Turnovers |
|---|---|---|---|---|---|---|---|---|---|
| ATL | 28 | 24 | 0 | 24 | 46% | 52 | 24:44 | 224 | 4 |
| TB | 56 | 3 | 1 | 4 | 7% | 60 | 35:16 | 322 | 1 |

## Backfield
- ATL: lead Bijan Robinson 19 car 76 yds 0 TD (68% of team rushes); RB2 Khalil Herbert 4 car 12 yds 0 TD
- TB: lead Bucky Irving 27 car 170 yds 1 TD (48% of team rushes); RB2 Kenny Gainwell 25 car 140 yds 0 TD

## Target shares
- ATL (23 targets): Drake London 6 tgt (26%) 1-8; Jahan Dotson 5 tgt (22%) 2-95; Kyle Pitts Sr. 5 tgt (22%) 2-6; Olamide Zaccheaus 2 tgt (9%) 1-4; Charlie Woerner 2 tgt (9%) 0-0; Austin Hooper 1 tgt (4%) 1-9; Khalil Herbert 1 tgt (4%) 1-3; Bijan Robinson 1 tgt (4%) 0-0
- TB (3 targets): Chris Godwin Jr. 1 tgt (33%) 0-0; Kenny Gainwell 1 tgt (33%) 0-0; Ted Hurst III 1 tgt (33%) 0-0

## Pressure on each QB (ESPN gives sacks and QB hits; no pressure rate in public box)
- ATL QB: 0 sacks, 0 QB hits on 24 dropbacks (sack+hit rate proxy 0%; ESPN QB hits include sacks)
- TB QB: 1 sacks, 1 QB hits on 4 dropbacks (sack+hit rate proxy 25%; ESPN QB hits include sacks)

## TD scorers / scoring plays

## Who disappeared and why
- Drake London rec O5.5: 1.0 (rain plus a bad Penix day (8/24, 4 INT, 2 of the INTs on balls to London by Anzalone and Parrish). The 5.7 mm rain forecast and Penix's turnover form should have put a QB-floor flag on any ATL catch line (judgment))
- Bijan Robinson rec O3.5: 0.0 (1 target. ATL went run-first (Bijan 19 carries) and Penix threw deep and outside, not to the back. RB target-share trend plus the rain pass-volume cut should have caught it (judgment))
- Drake London rec O4.5: 1.0 (rain plus a bad Penix day (8/24, 4 INT, 2 of the INTs on balls to London by Anzalone and Parrish). The 5.7 mm rain forecast and Penix's turnover form should have put a QB-floor flag on any ATL catch line (judgment))
- Bijan Robinson rec O2.5: 0.0 (1 target. ATL went run-first (Bijan 19 carries) and Penix threw deep and outside, not to the back. RB target-share trend plus the rain pass-volume cut should have caught it (judgment))

## Leg grades (runs folder legs and user slip legs)
| Group | Source | Leg | Actual | Result | Input that should have caught the miss |
|---|---|---|---|---|---|
| cut | runs/ATL@TB | Michael Penix Jr. Pass Yds Under 229.5 | 125.0 | HIT |  |
| cut | runs/ATL@TB | Bijan Robinson Rush Yds Under 80.5 | 76.0 | HIT |  |
| cut | runs/ATL@TB | Bijan Robinson Rush+Rec Yds Under 117.5 | 76.0 | HIT |  |
| cut | runs/ATL@TB | Drake London Rec Yds Under 79.5 | 8.0 | HIT |  |
| cut | runs/ATL@TB | Drake London Receptions Under 6.5 | 1.0 | HIT |  |
| cut | runs/ATL@TB | Jahan Dotson Rec Yds Under 25.5 | 95.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/ATL@TB | Jahan Dotson Receptions Under 2.5 | 2.0 | HIT |  |
| cut | runs/ATL@TB | Kyle Pitts Rec Yds Under 35.5 | 6.0 | HIT |  |
| cut | runs/ATL@TB | Kyle Pitts Receptions Under 3.5 | 2.0 | HIT |  |
| cut | runs/ATL@TB | Baker Mayfield Pass Yds Under 215.5 | 0.0 | HIT |  |
| cut | runs/ATL@TB | Bucky Irving Rush Yds Under 70.5 | 170.0 | MISS | game script: team led by 16, clock-kill carries; spread/positive-script input |
| cut | runs/ATL@TB | Bucky Irving Rush+Rec Yds Under 90.5 | 170.0 | MISS | game script: team led by 16, clock-kill carries; spread/positive-script input |
| cut | runs/ATL@TB | Chris Godwin Jr. Rec Yds Under 39.5 | 0.0 | HIT |  |
| cut | runs/ATL@TB | Chris Godwin Jr. Receptions Under 4.5 | 0.0 | HIT |  |
| cut | runs/ATL@TB | Cade Otton Rec Yds Under 33.5 | DNP/no stat line | VOID/NO ACTION | player had no box line; check inactive/active input |
| cut | runs/ATL@TB | Cade Otton Receptions Under 3.5 | DNP/no stat line | VOID/NO ACTION | player had no box line; check inactive/active input |
| slip | UD20 | Drake London rec O5.5 | 1.0 | MISS | rain plus a bad Penix day (8/24, 4 INT, 2 of the INTs on balls to London by Anzalone and Parrish). The 5.7 mm rain forecast and Penix's turnover form should have put a QB-floor flag on any ATL catch line (judgment) |
| slip | PP25 | Bijan Robinson rec O3.5 | 0.0 | MISS | 1 target. ATL went run-first (Bijan 19 carries) and Penix threw deep and outside, not to the back. RB target-share trend plus the rain pass-volume cut should have caught it (judgment) |
| slip | FD8 | Drake London rec O4.5 | 1.0 | MISS | rain plus a bad Penix day (8/24, 4 INT, 2 of the INTs on balls to London by Anzalone and Parrish). The 5.7 mm rain forecast and Penix's turnover form should have put a QB-floor flag on any ATL catch line (judgment) |
| slip | PP chat | Bijan Robinson rec O2.5 | 0.0 | MISS | 1 target. ATL went run-first (Bijan 19 carries) and Penix threw deep and outside, not to the back. RB target-share trend plus the rain pass-volume cut should have caught it (judgment) |
