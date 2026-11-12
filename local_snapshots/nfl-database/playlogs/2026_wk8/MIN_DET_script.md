# MIN @ DET game script

Final: MIN 15, DET 19 (margin DET +4)
Pregame (DraftKings close, ESPN pickcenter): DET -3.5, total 45.5. Favorite DET result vs spread: +4 vs -3.5 → covered. Total 34 vs 45.5: UNDER.
Weather actuals: dome (indoor)

**Script label: favorite close win / defensive slog (under by 10+)**

## Score state by quarter
- end Q1: MIN 0-DET 3
- end Q2: MIN 7-DET 6
- end Q3: MIN 7-DET 12
- end Q4: MIN 15-DET 19

## Run/pass and pace
| Team | Rush att | Pass att | Sacks taken | Dropbacks | Pass rate | Total plays | TOP | Yards | Turnovers |
|---|---|---|---|---|---|---|---|---|---|
| MIN | 18 | 29 | 3 | 32 | 64% | 50 | 24:17 | 266 | 1 |
| DET | 39 | 25 | 4 | 29 | 43% | 68 | 35:43 | 384 | 1 |

## Backfield
- MIN: lead Jordan Mason 8 car 20 yds 0 TD (44% of team rushes); RB2 Aaron Jones Sr. 5 car 22 yds 0 TD
- DET: lead Jahmyr Gibbs 23 car 153 yds 1 TD (59% of team rushes); RB2 Sione Vaki 11 car 65 yds 0 TD

## Target shares
- MIN (28 targets): Justin Jefferson 9 tgt (32%) 5-33; Jordan Addison 8 tgt (29%) 3-66; T.J. Hockenson 5 tgt (18%) 4-58; Ben Yurosek 2 tgt (7%) 1-24; Aaron Jones Sr. 2 tgt (7%) 2-18; Jauan Jennings 2 tgt (7%) 2-11
- DET (25 targets): Amon-Ra St. Brown 8 tgt (32%) 7-46; Jameson Williams 6 tgt (24%) 4-70; Sam LaPorta 5 tgt (20%) 3-33; Jahmyr Gibbs 4 tgt (16%) 2-15; Tyler Conklin 1 tgt (4%) 1-7; Sione Vaki 1 tgt (4%) 1-5

## Pressure on each QB (ESPN gives sacks and QB hits; no pressure rate in public box)
- MIN QB: 3 sacks, 6 QB hits on 32 dropbacks (sack+hit rate proxy 19%; ESPN QB hits include sacks)
- DET QB: 4 sacks, 9 QB hits on 29 dropbacks (sack+hit rate proxy 31%; ESPN QB hits include sacks)

## TD scorers / scoring plays

## Who disappeared and why
- Jordan Mason Rush Yds Over 49.5: 20.0 (efficiency/share: 8 car for 20; run-defense matchup / RB-share input)
- Aaron Jones Rush Yds Over 29.5: 22.0 (efficiency/share: 5 car for 22; run-defense matchup / RB-share input)
- Aaron Jones Rush+Rec Yds Over 43.5: 40.0 (efficiency/share: 5 car for 22; run-defense matchup / RB-share input)
- Amon-Ra St. Brown recyds O49.5: 46.0 (7 catches but 6.6 yds each. DET threw only 25 times (43% pass rate) while Gibbs ran 23 times. DET's run lean as a favorite and MIN's pressure (4 sacks) capped his ceiling; team pass-volume input (judgment))
- Amon-Ra St. Brown targets O9.5: 8.0 (8 of DET's 25 targets (32% share, normal). The team total was too small; pass-attempt projection at DET -3.5 indoors, with the run lean, should have caught it (judgment))
- Jared Goff fantasy O17: 10.04 (176 yds, 1 TD, 1 INT, sacked 4 times. MIN pressure plus DET's 39 rushes; opponent pressure-rate and run-lean script inputs (judgment))
- Jahmyr Gibbs rec O5.5: 2.0 (2-for-4. Used as the lead runner (23 carries, 153 yds) with DET ahead, so he ran instead of catching. Positive script lowers RB targets; script input (judgment))
- Sam LaPorta rec O5: 3.0 (3-for-5. 20% share of only 25 targets. Same DET pass-volume cap; team pass-attempt input (judgment))

## Leg grades (runs folder legs and user slip legs)
| Group | Source | Leg | Actual | Result | Input that should have caught the miss |
|---|---|---|---|---|---|
| cut | runs/MIN@DET | Kyler Murray Pass Yds Under 224.5 | 210.0 | HIT |  |
| cut | runs/MIN@DET | Jordan Mason Rush Yds Over 49.5 | 20.0 | MISS | efficiency/share: 8 car for 20; run-defense matchup / RB-share input |
| cut | runs/MIN@DET | Aaron Jones Rush Yds Over 29.5 | 22.0 | MISS | efficiency/share: 5 car for 22; run-defense matchup / RB-share input |
| cut | runs/MIN@DET | Aaron Jones Rush+Rec Yds Over 43.5 | 40.0 | MISS | efficiency/share: 5 car for 22; run-defense matchup / RB-share input |
| cut | runs/MIN@DET | Justin Jefferson Rec Yds Under 75.5 | 33.0 | HIT |  |
| cut | runs/MIN@DET | Justin Jefferson Receptions Under 5.5 | 5.0 | HIT |  |
| cut | runs/MIN@DET | Jordan Addison Rec Yds Over 37.5 | 66.0 | HIT |  |
| cut | runs/MIN@DET | Jordan Addison Receptions Under 3.5 | 3.0 | HIT |  |
| cut | runs/MIN@DET | T.J. Hockenson Rec Yds Under 40.5 | 58.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/MIN@DET | T.J. Hockenson Receptions Under 4.5 | 4.0 | HIT |  |
| cut | runs/MIN@DET | Jared Goff Pass Yds Under 259.5 | 176.0 | HIT |  |
| cut | runs/MIN@DET | Jahmyr Gibbs Rush Yds Over 87.5 | 153.0 | HIT |  |
| cut | runs/MIN@DET | Jahmyr Gibbs Rush+Rec Yds Over 121.5 | 168.0 | HIT |  |
| cut | runs/MIN@DET | Amon-Ra St. Brown Rec Yds Under 77.5 | 46.0 | HIT |  |
| cut | runs/MIN@DET | Amon-Ra St. Brown Receptions Under 6.5 | 7.0 | MISS | volume: 8 targets; target-share / injury-redistribution input |
| cut | runs/MIN@DET | Jameson Williams Rec Yds Under 51.5 | 70.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/MIN@DET | Jameson Williams Receptions Over 3.5 | 4.0 | HIT |  |
| cut | runs/MIN@DET | Sam LaPorta Rec Yds Under 45.5 | 33.0 | HIT |  |
| cut | runs/MIN@DET | Sam LaPorta Receptions Under 4.5 | 3.0 | HIT |  |
| slip | PP40 | Amon-Ra St. Brown rec O5.5 | 7.0 | HIT |  |
| slip | UD20 | Amon-Ra St. Brown recyds O49.5 | 46.0 | MISS | 7 catches but 6.6 yds each. DET threw only 25 times (43% pass rate) while Gibbs ran 23 times. DET's run lean as a favorite and MIN's pressure (4 sacks) capped his ceiling; team pass-volume input (judgment) |
| slip | PP25 | Amon-Ra St. Brown rec O7 | 7.0 | PUSH | landed exactly 7; PrizePicks whole-number line, so the pick is removed |
| slip | PP chat | Amon-Ra St. Brown targets O9.5 | 8.0 | MISS | 8 of DET's 25 targets (32% share, normal). The team total was too small; pass-attempt projection at DET -3.5 indoors, with the run lean, should have caught it (judgment) |
| slip | PP chat | Jared Goff fantasy O17 | 10.04 | MISS | 176 yds, 1 TD, 1 INT, sacked 4 times. MIN pressure plus DET's 39 rushes; opponent pressure-rate and run-lean script inputs (judgment) |
| slip | PP chat | Jameson Williams fantasy O10.5 | 17.0 | HIT |  |
| slip | PP chat | Jahmyr Gibbs rec O5.5 | 2.0 | MISS | 2-for-4. Used as the lead runner (23 carries, 153 yds) with DET ahead, so he ran instead of catching. Positive script lowers RB targets; script input (judgment) |
| slip | PP chat | Sam LaPorta rec O5 | 3.0 | MISS | 3-for-5. 20% share of only 25 targets. Same DET pass-volume cap; team pass-attempt input (judgment) |
