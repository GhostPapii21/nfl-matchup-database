# LAC @ LAR game script

Final: LAC 9, LAR 24 (margin LAR +15)
Pregame (DraftKings close, ESPN pickcenter): LAR -6.5, total 45.5. Favorite LAR result vs spread: +15 vs -6.5 → covered. Total 33 vs 45.5: UNDER.
Weather actuals: dome (indoor)

**Script label: favorite blowout, clock-kill second half / defensive slog (under by 10+)**

## Score state by quarter
- end Q1: LAC 3-LAR 3
- end Q2: LAC 9-LAR 10
- end Q3: LAC 9-LAR 24
- end Q4: LAC 9-LAR 24

## Run/pass and pace
| Team | Rush att | Pass att | Sacks taken | Dropbacks | Pass rate | Total plays | TOP | Yards | Turnovers |
|---|---|---|---|---|---|---|---|---|---|
| LAC | 25 | 32 | 2 | 34 | 58% | 59 | 32:24 | 295 | 2 |
| LAR | 27 | 25 | 1 | 26 | 49% | 53 | 27:36 | 281 | 1 |

## Backfield
- LAC: lead Omarion Hampton 9 car 20 yds 0 TD (36% of team rushes); RB2 Kimani Vidal 8 car 23 yds 0 TD
- LAR: lead Kyren Williams 16 car 56 yds 1 TD (59% of team rushes); RB2 Blake Corum 11 car 73 yds 1 TD

## Target shares
- LAC (30 targets): Ladd McConkey 6 tgt (20%) 4-86; Oronde Gadsden 5 tgt (17%) 5-52; Quentin Johnston 4 tgt (13%) 4-37; Charlie Kolar 4 tgt (13%) 1-20; Tre' Harris 3 tgt (10%) 3-31; Keaton Mitchell 3 tgt (10%) 3-17; Omarion Hampton 3 tgt (10%) 2-7; Kimani Vidal 2 tgt (7%) 2-7
- LAR (25 targets): Puka Nacua 12 tgt (48%) 11-80; Tutu Atwell 4 tgt (16%) 2-52; Tyler Higbee 2 tgt (8%) 1-14; Davis Allen 2 tgt (8%) 2-8; Konata Mumpfield 2 tgt (8%) 0-0; Kyren Williams 1 tgt (4%) 1-3; Blake Corum 1 tgt (4%) 0-0; Jordan Whittington 1 tgt (4%) 0-0

## Pressure on each QB (ESPN gives sacks and QB hits; no pressure rate in public box)
- LAC QB: 2 sacks, 4 QB hits on 34 dropbacks (sack+hit rate proxy 12%; ESPN QB hits include sacks)
- LAR QB: 1 sacks, 2 QB hits on 26 dropbacks (sack+hit rate proxy 8%; ESPN QB hits include sacks)

## TD scorers / scoring plays
- Q2 0:19 LAR: Kyren Williams 1 Yd Rush (Brandon McManus Kick) (LAC 9-LAR 10)
- Q3 10:42 LAR: Blake Corum 23 Yd Rush (Brandon McManus Kick) (LAC 9-LAR 17)
- Q3 3:41 LAR: Puka Nacua 18 Yd pass from Matthew Stafford (Brandon McManus Kick) (LAC 9-LAR 24)

## Who disappeared and why
- Omarion Hampton Rush Yds Over 31.5: 20.0 (game script: team trailed by 15; spread/script input (negative script for RB overs))
- Omarion Hampton Rush+Rec Yds Over 40.5: 27.0 (game script: team trailed by 15; spread/script input (negative script for RB overs))
- Matthew Stafford Pass Yds Over 248.5: 157.0 (game script: team led by 15, clock-kill; spread/pass-rate input)
- Puka Nacua Rec Yds Over 91.5: 80.0 (efficiency: volume came but yards/catches did not; defender coverage / matchup input)
- Matthew Stafford completions O22.5: 17.0 (LAR led 24-9 and ran 27 times, so Stafford threw only 25 passes (17 completions). The projected lead (LAR -6.5) should have capped pass volume; the -6.5 spread / pass-rate input should have caught it (judgment))
- Matthew Stafford completions O22.5: 17.0 (LAR led 24-9 and ran 27 times, so Stafford threw only 25 passes (17 completions). The projected lead (LAR -6.5) should have capped pass volume; the -6.5 spread / pass-rate input should have caught it (judgment))
- K. Walker III + K. Williams TDs combo O1.5: 1.0 (Walker 0 TD: KC scored all 3 TDs through the air (Rice, E. Johnson, Gray); TD variance / red-zone usage input)

## Leg grades (runs folder legs and user slip legs)
| Group | Source | Leg | Actual | Result | Input that should have caught the miss |
|---|---|---|---|---|---|
| cut | runs/LAC@LAR | Justin Herbert Pass Yds Under 205.5 | 257.0 | MISS | game script: team trailed by 15 and threw late; spread/negative-script input |
| cut | runs/LAC@LAR | Omarion Hampton Rush Yds Over 31.5 | 20.0 | MISS | game script: team trailed by 15; spread/script input (negative script for RB overs) |
| cut | runs/LAC@LAR | Omarion Hampton Rush+Rec Yds Over 40.5 | 27.0 | MISS | game script: team trailed by 15; spread/script input (negative script for RB overs) |
| cut | runs/LAC@LAR | Ladd McConkey Rec Yds Under 47.5 | 86.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/LAC@LAR | Ladd McConkey Receptions Under 3.5 | 4.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/LAC@LAR | Quentin Johnston Rec Yds Under 33.5 | 37.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/LAC@LAR | Quentin Johnston Receptions Under 2.5 | 4.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/LAC@LAR | Oronde Gadsden II Rec Yds Under 15.5 | 52.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/LAC@LAR | Oronde Gadsden II Receptions Under 1.5 | 5.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| cut | runs/LAC@LAR | Matthew Stafford Pass Yds Over 248.5 | 157.0 | MISS | game script: team led by 15, clock-kill; spread/pass-rate input |
| cut | runs/LAC@LAR | Kyren Williams Rush Yds Under 58.5 | 56.0 | HIT |  |
| cut | runs/LAC@LAR | Kyren Williams Rush+Rec Yds Under 85.5 | 59.0 | HIT |  |
| cut | runs/LAC@LAR | Blake Corum Rush Yds Under 46.5 | 73.0 | MISS | game script: team led by 15, clock-kill carries; spread/positive-script input |
| cut | runs/LAC@LAR | Blake Corum Rush+Rec Yds Under 56.5 | 73.0 | MISS | game script: team led by 15, clock-kill carries; spread/positive-script input |
| cut | runs/LAC@LAR | Puka Nacua Rec Yds Over 91.5 | 80.0 | MISS | efficiency: volume came but yards/catches did not; defender coverage / matchup input |
| cut | runs/LAC@LAR | Puka Nacua Receptions Over 7.5 | 11.0 | HIT |  |
| cut | runs/LAC@LAR | Tyler Higbee Rec Yds Under 36.5 | 14.0 | HIT |  |
| cut | runs/LAC@LAR | Tyler Higbee Receptions Under 3.5 | 1.0 | HIT |  |
| slip | PP40 | Matthew Stafford completions O22.5 | 17.0 | MISS | LAR led 24-9 and ran 27 times, so Stafford threw only 25 passes (17 completions). The projected lead (LAR -6.5) should have capped pass volume; the -6.5 spread / pass-rate input should have caught it (judgment) |
| slip | PP20 | Matthew Stafford completions O22.5 | 17.0 | MISS | LAR led 24-9 and ran 27 times, so Stafford threw only 25 passes (17 completions). The projected lead (LAR -6.5) should have capped pass volume; the -6.5 spread / pass-rate input should have caught it (judgment) |
| slip | UD20 | Puka Nacua recyds O69.5 | 80.0 | HIT |  |
| slip | PP chat | Puka Nacua recyds O69.5 | 80.0 | HIT |  |
| slip | FD8 | Puka Nacua recyds O59.5 | 80.0 | HIT |  |
| slip | PP25 | Kyren Williams td O0.5 | 1.0 | HIT |  |
| slip | PP20 | K. Walker III + K. Williams TDs combo O1.5 | 1.0 | MISS | Walker 0 TD: KC scored all 3 TDs through the air (Rice, E. Johnson, Gray); TD variance / red-zone usage input |
| slip | FD7 | Kyren Williams or Blake Corum anytime TD | 1 | HIT |  |
