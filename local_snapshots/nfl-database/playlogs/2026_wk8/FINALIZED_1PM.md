# Week 8 Sunday early window: finalized

Updated 2026-11-01 16:43 ET
Every game was re-checked as STATUS_FINAL on ESPN before writing. Lines are the DraftKings close from ESPN pickcenter. Rows tagged "(judgment)" in the miss column are written per leg; the others come from auto rules (runs-folder legs only).

## Games
| Game | Final | Close | Script label | Files |
|---|---|---|---|---|
| ATL@TB | ATL 0, TB 16 | TB -2.5, O/U 43.5 | rain run-fest: TB 56 rushes vs 3 passes, ATL QB collapse (4 INT); defensive slog, shutout | ATL_TB_box.json/.md, ATL_TB_plays.md, ATL_TB_script.md |
| CLE@PIT | CLE 6, PIT 27 | PIT -3.5, O/U 38.5 | favorite blowout, clock-kill second half | CLE_PIT_box.json/.md, CLE_PIT_plays.md, CLE_PIT_script.md |
| IND@JAX | IND 7, JAX 42 | JAX -10.5, O/U 45.5 | favorite blowout, clock-kill second half | IND_JAX_box.json/.md, IND_JAX_plays.md, IND_JAX_script.md |
| LV@NYJ | LV 38, NYJ 33 | NYJ -1.5, O/U 46.5 | underdog upset / shootout (over by 10+) | LV_NYJ_box.json/.md, LV_NYJ_plays.md, LV_NYJ_script.md |
| MIN@DET | MIN 15, DET 19 | DET -3.5, O/U 45.5 | favorite close win / defensive slog (under by 10+) | MIN_DET_box.json/.md, MIN_DET_plays.md, MIN_DET_script.md |
| BAL@BUF | BAL 10, BUF 36 | BUF -3, O/U 54.5 | favorite blowout, clock-kill second half | BAL_BUF_box.json/.md, BAL_BUF_plays.md, BAL_BUF_script.md |
| TEN@CIN | TEN 36, CIN 43 | CIN -13.5, O/U 45.5 | overtime shootout: 13.5-pt favorite CIN won 43-36 in OT, 34 over the total | TEN_CIN_box.json/.md, TEN_CIN_plays.md, TEN_CIN_script.md |
| ARI@DAL | ARI 33, DAL 30 | DAL -7, O/U 54.5 | overtime underdog upset: ARI threw 46 times and won 33-30 in OT; DAL leaned run (39 rushes) | ARI_DAL_box.json/.md, ARI_DAL_plays.md, ARI_DAL_script.md |

LV@NYJ score check: the user's 2:00 Q4 screenshot showed 35-33; Matt Gay hit a 53-yd FG at 0:27 for the final 38-33.

All 8 early-window games are final and logged; none left. TEN@CIN and ARI@DAL went to OT and were finalized at 16:42 ET.

## Hit rates (decided legs; pushes and voids not counted)
| Group | Hit | Push/void |
|---|---|---|
| passed | 0/1 (0%) | 0 |
| cut | 61/124 (49%) | 6 |
| slip | 18/32 (56%) | 1 |

## All grades
| Game | Source | Group | Leg | Actual | Result | Input that should have caught the miss |
|---|---|---|---|---|---|---|
| ATL@TB | runs/ATL@TB | cut | Michael Penix Jr. Pass Yds Under 229.5 | 125.0 | HIT |  |
| ATL@TB | runs/ATL@TB | cut | Bijan Robinson Rush Yds Under 80.5 | 76.0 | HIT |  |
| ATL@TB | runs/ATL@TB | cut | Bijan Robinson Rush+Rec Yds Under 117.5 | 76.0 | HIT |  |
| ATL@TB | runs/ATL@TB | cut | Drake London Rec Yds Under 79.5 | 8.0 | HIT |  |
| ATL@TB | runs/ATL@TB | cut | Drake London Receptions Under 6.5 | 1.0 | HIT |  |
| ATL@TB | runs/ATL@TB | cut | Jahan Dotson Rec Yds Under 25.5 | 95.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| ATL@TB | runs/ATL@TB | cut | Jahan Dotson Receptions Under 2.5 | 2.0 | HIT |  |
| ATL@TB | runs/ATL@TB | cut | Kyle Pitts Rec Yds Under 35.5 | 6.0 | HIT |  |
| ATL@TB | runs/ATL@TB | cut | Kyle Pitts Receptions Under 3.5 | 2.0 | HIT |  |
| ATL@TB | runs/ATL@TB | cut | Baker Mayfield Pass Yds Under 215.5 | 0.0 | HIT |  |
| ATL@TB | runs/ATL@TB | cut | Bucky Irving Rush Yds Under 70.5 | 170.0 | MISS | game script: team led by 16, clock-kill carries; spread/positive-script input |
| ATL@TB | runs/ATL@TB | cut | Bucky Irving Rush+Rec Yds Under 90.5 | 170.0 | MISS | game script: team led by 16, clock-kill carries; spread/positive-script input |
| ATL@TB | runs/ATL@TB | cut | Chris Godwin Jr. Rec Yds Under 39.5 | 0.0 | HIT |  |
| ATL@TB | runs/ATL@TB | cut | Chris Godwin Jr. Receptions Under 4.5 | 0.0 | HIT |  |
| ATL@TB | runs/ATL@TB | cut | Cade Otton Rec Yds Under 33.5 | DNP/no stat line | VOID/NO ACTION | player had no box line; check inactive/active input |
| ATL@TB | runs/ATL@TB | cut | Cade Otton Receptions Under 3.5 | DNP/no stat line | VOID/NO ACTION | player had no box line; check inactive/active input |
| CLE@PIT | runs/CLE@PIT | cut | Deshaun Watson Pass Yds Under 210.5 | 324.0 | MISS | game script: team trailed by 21 and threw late; spread/negative-script input |
| CLE@PIT | runs/CLE@PIT | cut | Quinshon Judkins Rush Yds Over 47.5 | 25.0 | MISS | game script: team trailed by 21; spread/script input (negative script for RB overs) |
| CLE@PIT | runs/CLE@PIT | cut | Quinshon Judkins Rush+Rec Yds Over 61.5 | 49.0 | MISS | game script: team trailed by 21; spread/script input (negative script for RB overs) |
| CLE@PIT | runs/CLE@PIT | cut | Jerry Jeudy Rec Yds Over 21.5 | 0.0 | MISS | pass-rush script: QB sacked 8x, offense leaned run, game margin -21; opponent pressure-rate + run-lean script input |
| CLE@PIT | runs/CLE@PIT | cut | Jerry Jeudy Receptions Over 2.5 | 0.0 | MISS | pass-rush script: QB sacked 8x, offense leaned run, game margin -21; opponent pressure-rate + run-lean script input |
| CLE@PIT | runs/CLE@PIT | cut | KC Concepcion Rec Yds Under 46.5 | 37.0 | HIT |  |
| CLE@PIT | runs/CLE@PIT | cut | KC Concepcion Receptions Under 4.5 | 3.0 | HIT |  |
| CLE@PIT | runs/CLE@PIT | cut | Denzel Boston Rec Yds Under 47.5 | 37.0 | HIT |  |
| CLE@PIT | runs/CLE@PIT | cut | Denzel Boston Receptions Under 3.5 | 6.0 | MISS | volume: 11 targets; target-share / injury-redistribution input |
| CLE@PIT | runs/CLE@PIT | cut | Harold Fannin Jr. Rec Yds Under 34.5 | 154.0 | MISS | volume: 12 targets; target-share / injury-redistribution input |
| CLE@PIT | runs/CLE@PIT | cut | Harold Fannin Jr. Receptions Under 3.5 | 10.0 | MISS | volume: 12 targets; target-share / injury-redistribution input |
| CLE@PIT | runs/CLE@PIT | cut | Aaron Rodgers Pass Yds Under 218.5 | 172.0 | HIT |  |
| CLE@PIT | runs/CLE@PIT | cut | Jaylen Warren Rush Yds Over 64.5 | 143.0 | HIT |  |
| CLE@PIT | runs/CLE@PIT | cut | Jaylen Warren Rush+Rec Yds Over 91.5 | 143.0 | HIT |  |
| CLE@PIT | runs/CLE@PIT | cut | DK Metcalf Rec Yds Under 52.5 | 4.0 | HIT |  |
| CLE@PIT | runs/CLE@PIT | cut | DK Metcalf Receptions Under 4.5 | 1.0 | HIT |  |
| CLE@PIT | runs/CLE@PIT | cut | Germie Bernard Rec Yds Over 43.5 | 30.0 | MISS | efficiency: volume came but yards/catches did not; defender coverage / matchup input |
| CLE@PIT | runs/CLE@PIT | cut | Germie Bernard Receptions Under 4.5 | 5.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| CLE@PIT | runs/CLE@PIT | cut | Darnell Washington Rec Yds Under 20.5 | 94.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| CLE@PIT | runs/CLE@PIT | cut | Darnell Washington Receptions Under 2.5 | 3.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| IND@JAX | runs/IND@JAX | cut | Daniel Jones Pass Yds Over 192.5 | 144.0 | MISS | efficiency: volume came but yards/catches did not; defender coverage / matchup input |
| IND@JAX | runs/IND@JAX | cut | Jonathan Taylor Rush Yds Over 50.5 | 23.0 | MISS | game script: team trailed by 35; spread/script input (negative script for RB overs) |
| IND@JAX | runs/IND@JAX | cut | Jonathan Taylor Rush+Rec Yds Over 70.5 | 47.0 | MISS | game script: team trailed by 35; spread/script input (negative script for RB overs) |
| IND@JAX | runs/IND@JAX | cut | Josh Downs Rec Yds Over 32.5 | 23.0 | MISS | efficiency: volume came but yards/catches did not; defender coverage / matchup input |
| IND@JAX | runs/IND@JAX | cut | Josh Downs Receptions Over 3.5 | 4.0 | HIT |  |
| IND@JAX | runs/IND@JAX | cut | Keenan Allen Rec Yds Over 35.5 | 67.0 | HIT |  |
| IND@JAX | runs/IND@JAX | cut | Keenan Allen Receptions Over 4.5 | 7.0 | HIT |  |
| IND@JAX | runs/IND@JAX | cut | Tyler Warren Rec Yds Over 39.5 | 18.0 | MISS | efficiency: volume came but yards/catches did not; defender coverage / matchup input |
| IND@JAX | runs/IND@JAX | cut | Tyler Warren Receptions Over 4.5 | 4.0 | MISS | efficiency: volume came but yards/catches did not; defender coverage / matchup input |
| IND@JAX | runs/IND@JAX | cut | Trevor Lawrence Pass Yds Under 237.5 | 210.0 | HIT |  |
| IND@JAX | runs/IND@JAX | cut | Bhayshul Tuten Rush Yds Over 59.5 | 104.0 | HIT |  |
| IND@JAX | runs/IND@JAX | cut | Bhayshul Tuten Rush+Rec Yds Over 83.5 | 159.0 | HIT |  |
| IND@JAX | runs/IND@JAX | cut | Parker Washington Rec Yds Over 59.5 | 16.0 | MISS | volume: only 2 targets; target-share/QB-volume input (team led by 35) |
| IND@JAX | runs/IND@JAX | cut | Parker Washington Receptions Under 4.5 | 1.0 | HIT |  |
| IND@JAX | runs/IND@JAX | cut | Brenton Strange Rec Yds Under 41.5 | 55.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| IND@JAX | runs/IND@JAX | cut | Brenton Strange Receptions Over 2.5 | 2.0 | MISS | volume: only 2 targets; target-share/QB-volume input (team led by 35) |
| LV@NYJ | runs/LV@NYJ | cut | Kirk Cousins Pass Yds Over 232.5 | 247.0 | HIT |  |
| LV@NYJ | runs/LV@NYJ | cut | Brock Bowers Rec Yds Over 68.5 | 92.0 | HIT |  |
| LV@NYJ | runs/LV@NYJ | cut | Brock Bowers Receptions Under 5.5 | 7.0 | MISS | volume: 10 targets; target-share / injury-redistribution input |
| LV@NYJ | runs/LV@NYJ | cut | Tre Tucker Rec Yds Over 48.5 | 0.0 | MISS | volume: only 1 targets; target-share/QB-volume input (team led by 5) |
| LV@NYJ | runs/LV@NYJ | passed | Tre Tucker Receptions Over 3.5 | 0.0 | MISS | 1 official target (plus a DPI no-play) in a 26-attempt game where Bowers got 10. The gate passed it on season target share without a current-week route/role check. Role-share input (snap/route data was not in the folder) (judgment) |
| LV@NYJ | runs/LV@NYJ | cut | Geno Smith Pass Yds Under 225.5 | 290.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| LV@NYJ | runs/LV@NYJ | cut | Garrett Wilson Rec Yds Under 63.5 | 83.0 | MISS | volume: 12 targets; target-share / injury-redistribution input |
| LV@NYJ | runs/LV@NYJ | cut | Garrett Wilson Receptions Under 5.5 | 6.0 | MISS | volume: 12 targets; target-share / injury-redistribution input |
| LV@NYJ | runs/LV@NYJ | cut | Omar Cooper Jr. Rec Yds Over 41.5 | DNP/no stat line | VOID/NO ACTION | player had no box line; check inactive/active input |
| LV@NYJ | runs/LV@NYJ | cut | Omar Cooper Jr. Receptions Under 3.5 | DNP/no stat line | VOID/NO ACTION | player had no box line; check inactive/active input |
| MIN@DET | runs/MIN@DET | cut | Kyler Murray Pass Yds Under 224.5 | 210.0 | HIT |  |
| MIN@DET | runs/MIN@DET | cut | Jordan Mason Rush Yds Over 49.5 | 20.0 | MISS | efficiency/share: 8 car for 20; run-defense matchup / RB-share input |
| MIN@DET | runs/MIN@DET | cut | Aaron Jones Rush Yds Over 29.5 | 22.0 | MISS | efficiency/share: 5 car for 22; run-defense matchup / RB-share input |
| MIN@DET | runs/MIN@DET | cut | Aaron Jones Rush+Rec Yds Over 43.5 | 40.0 | MISS | efficiency/share: 5 car for 22; run-defense matchup / RB-share input |
| MIN@DET | runs/MIN@DET | cut | Justin Jefferson Rec Yds Under 75.5 | 33.0 | HIT |  |
| MIN@DET | runs/MIN@DET | cut | Justin Jefferson Receptions Under 5.5 | 5.0 | HIT |  |
| MIN@DET | runs/MIN@DET | cut | Jordan Addison Rec Yds Over 37.5 | 66.0 | HIT |  |
| MIN@DET | runs/MIN@DET | cut | Jordan Addison Receptions Under 3.5 | 3.0 | HIT |  |
| MIN@DET | runs/MIN@DET | cut | T.J. Hockenson Rec Yds Under 40.5 | 58.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| MIN@DET | runs/MIN@DET | cut | T.J. Hockenson Receptions Under 4.5 | 4.0 | HIT |  |
| MIN@DET | runs/MIN@DET | cut | Jared Goff Pass Yds Under 259.5 | 176.0 | HIT |  |
| MIN@DET | runs/MIN@DET | cut | Jahmyr Gibbs Rush Yds Over 87.5 | 153.0 | HIT |  |
| MIN@DET | runs/MIN@DET | cut | Jahmyr Gibbs Rush+Rec Yds Over 121.5 | 168.0 | HIT |  |
| MIN@DET | runs/MIN@DET | cut | Amon-Ra St. Brown Rec Yds Under 77.5 | 46.0 | HIT |  |
| MIN@DET | runs/MIN@DET | cut | Amon-Ra St. Brown Receptions Under 6.5 | 7.0 | MISS | volume: 8 targets; target-share / injury-redistribution input |
| MIN@DET | runs/MIN@DET | cut | Jameson Williams Rec Yds Under 51.5 | 70.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| MIN@DET | runs/MIN@DET | cut | Jameson Williams Receptions Over 3.5 | 4.0 | HIT |  |
| MIN@DET | runs/MIN@DET | cut | Sam LaPorta Rec Yds Under 45.5 | 33.0 | HIT |  |
| MIN@DET | runs/MIN@DET | cut | Sam LaPorta Receptions Under 4.5 | 3.0 | HIT |  |
| BAL@BUF | runs/BAL@BUF | cut | Lamar Jackson Pass Yds Under 237.5 | 0.0 | HIT |  |
| BAL@BUF | runs/BAL@BUF | cut | Derrick Henry Rush Yds Under 78.5 | 53.0 | HIT |  |
| BAL@BUF | runs/BAL@BUF | cut | Derrick Henry Rush+Rec Yds Under 89.5 | 60.0 | HIT |  |
| BAL@BUF | runs/BAL@BUF | cut | Zay Flowers Rec Yds Over 82.5 | 0.0 | MISS | efficiency: volume came but yards/catches did not; defender coverage / matchup input |
| BAL@BUF | runs/BAL@BUF | cut | Zay Flowers Receptions Over 6.5 | 0.0 | MISS | efficiency: volume came but yards/catches did not; defender coverage / matchup input |
| BAL@BUF | runs/BAL@BUF | cut | Rashod Bateman Rec Yds Over 23.5 | 22.0 | MISS | volume: only 3 targets; target-share/QB-volume input (team trailed by 26) |
| BAL@BUF | runs/BAL@BUF | cut | Rashod Bateman Receptions Under 2.5 | 1.0 | HIT |  |
| BAL@BUF | runs/BAL@BUF | cut | Mark Andrews Rec Yds Over 27.5 | 14.0 | MISS | volume: only 4 targets; target-share/QB-volume input (team trailed by 26) |
| BAL@BUF | runs/BAL@BUF | cut | Mark Andrews Receptions Under 3.5 | 3.0 | HIT |  |
| BAL@BUF | runs/BAL@BUF | cut | Josh Allen Pass Yds Under 247.5 | 289.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| BAL@BUF | runs/BAL@BUF | cut | James Cook Rush Yds Under 82.5 | 80.0 | HIT |  |
| BAL@BUF | runs/BAL@BUF | cut | James Cook Rush+Rec Yds Under 96.5 | 101.0 | MISS | game script: team led by 26, clock-kill carries; spread/positive-script input |
| BAL@BUF | runs/BAL@BUF | cut | DJ Moore Rec Yds Over 49.5 | 82.0 | HIT |  |
| BAL@BUF | runs/BAL@BUF | cut | DJ Moore Receptions Under 4.5 | 4.0 | HIT |  |
| BAL@BUF | runs/BAL@BUF | cut | Khalil Shakir Rec Yds Under 41.5 | 64.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| BAL@BUF | runs/BAL@BUF | cut | Khalil Shakir Receptions Under 3.5 | 5.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| BAL@BUF | runs/BAL@BUF | cut | Keon Coleman Rec Yds Over 29.5 | 4.0 | MISS | volume: only 3 targets; target-share/QB-volume input (team led by 26) |
| BAL@BUF | runs/BAL@BUF | cut | Keon Coleman Receptions Over 2.5 | 1.0 | MISS | volume: only 3 targets; target-share/QB-volume input (team led by 26) |
| BAL@BUF | runs/BAL@BUF | cut | Dalton Kincaid Rec Yds Under 46.5 | 86.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| BAL@BUF | runs/BAL@BUF | cut | Dalton Kincaid Receptions Under 3.5 | 4.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| TEN@CIN | runs/TEN@CIN | cut | Cam Ward Pass Yds Under 192.5 | 304.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| TEN@CIN | runs/TEN@CIN | cut | Tony Pollard Rush Yds Over 65.5 | 117.0 | HIT |  |
| TEN@CIN | runs/TEN@CIN | cut | Tony Pollard Rush+Rec Yds Under 84.5 | 137.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| TEN@CIN | runs/TEN@CIN | cut | Joe Burrow Pass Yds Over 249.5 | 462.0 | HIT |  |
| TEN@CIN | runs/TEN@CIN | cut | Chase Brown Rush Yds Under 58.5 | 55.0 | HIT |  |
| TEN@CIN | runs/TEN@CIN | cut | Chase Brown Rush+Rec Yds Under 81.5 | 101.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| TEN@CIN | runs/TEN@CIN | cut | Ja'Marr Chase Rec Yds Under 79.5 | 141.0 | MISS | volume: 16 targets; target-share / injury-redistribution input |
| TEN@CIN | runs/TEN@CIN | cut | Ja'Marr Chase Receptions Under 6.5 | 11.0 | MISS | volume: 16 targets; target-share / injury-redistribution input |
| TEN@CIN | runs/TEN@CIN | cut | Tee Higgins Rec Yds Over 69.5 | 155.0 | HIT |  |
| TEN@CIN | runs/TEN@CIN | cut | Tee Higgins Receptions Over 4.5 | 10.0 | HIT |  |
| TEN@CIN | runs/TEN@CIN | cut | Mike Gesicki Rec Yds Under 22.5 | 76.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| TEN@CIN | runs/TEN@CIN | cut | Mike Gesicki Receptions Under 2.5 | 4.0 | MISS | explosive/efficiency outlier; defense explosives-allowed input |
| ARI@DAL | runs/ARI@DAL | cut | Jacoby Brissett Pass Yds Under 258.5 | 119.0 | HIT |  |
| ARI@DAL | runs/ARI@DAL | cut | Tyler Allgeier Rush Yds Over 13.5 | 147.0 | HIT |  |
| ARI@DAL | runs/ARI@DAL | cut | Bam Knight Rush Yds Over 19.5 | 8.0 | MISS | efficiency/share: 3 car for 8; run-defense matchup / RB-share input |
| ARI@DAL | runs/ARI@DAL | cut | Michael Wilson Rec Yds Under 56.5 | 111.0 | MISS | volume: 15 targets; target-share / injury-redistribution input |
| ARI@DAL | runs/ARI@DAL | cut | Michael Wilson Receptions Under 4.5 | 8.0 | MISS | volume: 15 targets; target-share / injury-redistribution input |
| ARI@DAL | runs/ARI@DAL | cut | Trey McBride Rec Yds Under 71.5 | 72.0 | MISS | volume: 8 targets; target-share / injury-redistribution input |
| ARI@DAL | runs/ARI@DAL | cut | Trey McBride Receptions Over 7.5 | 7.0 | MISS | efficiency: volume came but yards/catches did not; defender coverage / matchup input |
| ARI@DAL | runs/ARI@DAL | cut | Dak Prescott Pass Yds Under 271.5 | 195.0 | HIT |  |
| ARI@DAL | runs/ARI@DAL | cut | Javonte Williams Rush Yds Under 76.5 | 56.0 | HIT |  |
| ARI@DAL | runs/ARI@DAL | cut | Javonte Williams Rush+Rec Yds Under 92.5 | 57.0 | HIT |  |
| ARI@DAL | runs/ARI@DAL | cut | CeeDee Lamb Rec Yds Over 80.5 | 58.0 | MISS | pass-rush script: QB sacked 4x, offense leaned run, game margin -3; opponent pressure-rate + run-lean script input |
| ARI@DAL | runs/ARI@DAL | cut | CeeDee Lamb Receptions Over 6.5 | 7.0 | HIT |  |
| ARI@DAL | runs/ARI@DAL | cut | George Pickens Rec Yds Over 59.5 | 48.0 | MISS | pass-rush script: QB sacked 4x, offense leaned run, game margin -3; opponent pressure-rate + run-lean script input |
| ARI@DAL | runs/ARI@DAL | cut | George Pickens Receptions Over 3.5 | 2.0 | MISS | pass-rush script: QB sacked 4x, offense leaned run, game margin -3; opponent pressure-rate + run-lean script input |
| ARI@DAL | runs/ARI@DAL | cut | Ryan Flournoy Rec Yds Over 36.5 | 38.0 | HIT |  |
| ARI@DAL | runs/ARI@DAL | cut | Ryan Flournoy Receptions Over 3.5 | 3.0 | MISS | pass-rush script: QB sacked 4x, offense leaned run, game margin -3; opponent pressure-rate + run-lean script input |
| ARI@DAL | runs/ARI@DAL | cut | Jake Ferguson Rec Yds Over 14.5 | DNP/no stat line | VOID/NO ACTION | player had no box line; check inactive/active input |
| ARI@DAL | runs/ARI@DAL | cut | Jake Ferguson Receptions Over 1.5 | DNP/no stat line | VOID/NO ACTION | player had no box line; check inactive/active input |
| MIN@DET | PP40 | slip | Amon-Ra St. Brown rec O5.5 | 7.0 | HIT |  |
| LV@NYJ | PP40 | slip | Brock Bowers targets O8.5 | 10.0 | HIT |  |
| LV@NYJ | UD20 | slip | Brock Bowers recyds O49.5 | 92.0 | HIT |  |
| ATL@TB | UD20 | slip | Drake London rec O5.5 | 1.0 | MISS | rain plus a bad Penix day (8/24, 4 INT, 2 of the INTs on balls to London by Anzalone and Parrish). The 5.7 mm rain forecast and Penix's turnover form should have put a QB-floor flag on any ATL catch line (judgment) |
| MIN@DET | UD20 | slip | Amon-Ra St. Brown recyds O49.5 | 46.0 | MISS | 7 catches but 6.6 yds each. DET threw only 25 times (43% pass rate) while Gibbs ran 23 times. DET's run lean as a favorite and MIN's pressure (4 sacks) capped his ceiling; team pass-volume input (judgment) |
| CLE@PIT | UD20 | slip | Denzel Boston recyds O29.5 | 37.0 | HIT |  |
| LV@NYJ | PP20 | slip | Brock Bowers halves w/25+ rec yds O1.5 | 2 (H1 40, H2 52) | HIT |  |
| ATL@TB | PP25 | slip | Bijan Robinson rec O3.5 | 0.0 | MISS | 1 target. ATL went run-first (Bijan 19 carries) and Penix threw deep and outside, not to the back. RB target-share trend plus the rain pass-volume cut should have caught it (judgment) |
| MIN@DET | PP25 | slip | Amon-Ra St. Brown rec O7 | 7.0 | PUSH | landed exactly 7; PrizePicks whole-number line, so the pick is removed |
| CLE@PIT | PP25 | slip | Jaylen Warren rushrec O69.5 | 143.0 | HIT |  |
| LV@NYJ | FD7/FD8 | slip | Brock Bowers recyds O49.5 | 92.0 | HIT |  |
| IND@JAX | FD7/FD8 | slip | Parker Washington recyds O39.5 | 16.0 | MISS | 2 targets. JAX led by 35 and threw only 17 times. The JAX -10.5 blowout script should have capped WR2 volume; spread/script input (judgment) |
| ATL@TB | FD8 | slip | Drake London rec O4.5 | 1.0 | MISS | rain plus a bad Penix day (8/24, 4 INT, 2 of the INTs on balls to London by Anzalone and Parrish). The 5.7 mm rain forecast and Penix's turnover form should have put a QB-floor flag on any ATL catch line (judgment) |
| ATL@TB | PP chat | slip | Bijan Robinson rec O2.5 | 0.0 | MISS | 1 target. ATL went run-first (Bijan 19 carries) and Penix threw deep and outside, not to the back. RB target-share trend plus the rain pass-volume cut should have caught it (judgment) |
| MIN@DET | PP chat | slip | Amon-Ra St. Brown targets O9.5 | 8.0 | MISS | 8 of DET's 25 targets (32% share, normal). The team total was too small; pass-attempt projection at DET -3.5 indoors, with the run lean, should have caught it (judgment) |
| CLE@PIT | PP chat | slip | Jaylen Warren fantasy O14.5 | 21.3 | HIT |  |
| MIN@DET | PP chat | slip | Jared Goff fantasy O17 | 10.04 | MISS | 176 yds, 1 TD, 1 INT, sacked 4 times. MIN pressure plus DET's 39 rushes; opponent pressure-rate and run-lean script inputs (judgment) |
| MIN@DET | PP chat | slip | Jameson Williams fantasy O10.5 | 17.0 | HIT |  |
| MIN@DET | PP chat | slip | Jahmyr Gibbs rec O5.5 | 2.0 | MISS | 2-for-4. Used as the lead runner (23 carries, 153 yds) with DET ahead, so he ran instead of catching. Positive script lowers RB targets; script input (judgment) |
| MIN@DET | PP chat | slip | Sam LaPorta rec O5 | 3.0 | MISS | 3-for-5. 20% share of only 25 targets. Same DET pass-volume cap; team pass-attempt input (judgment) |
| BAL@BUF | PP25 | slip | Zay Flowers rec O6 | 0.0 | MISS | 0-for-5. Lamar Jackson got hurt on his first throw (Q1 10:04, 0/1). Fagnano (10/21, 91 yds; one INT on a ball to Flowers, by Igbinosun) and Huntley (2/4, 0 yds) finished. You can't price in-game QB injury pregame, but BAL's backup-QB floor plus BUF's 35% blitz (the 'Panthers-rule risk' already flagged on the slip) made a WR1 over fragile. QB-health and backup-floor input (judgment) |
| BAL@BUF | UD20 | slip | Zay Flowers recyds O49.5 | 0.0 | MISS | 0-for-5. Lamar Jackson got hurt on his first throw (Q1 10:04, 0/1). Fagnano (10/21, 91 yds; one INT on a ball to Flowers, by Igbinosun) and Huntley (2/4, 0 yds) finished. You can't price in-game QB injury pregame, but BAL's backup-QB floor plus BUF's 35% blitz (the 'Panthers-rule risk' already flagged on the slip) made a WR1 over fragile. QB-health and backup-floor input (judgment) |
| BAL@BUF | FD7/FD8 | slip | Zay Flowers recyds O59.5 | 0.0 | MISS | 0-for-5. Lamar Jackson got hurt on his first throw (Q1 10:04, 0/1). Fagnano (10/21, 91 yds; one INT on a ball to Flowers, by Igbinosun) and Huntley (2/4, 0 yds) finished. You can't price in-game QB injury pregame, but BAL's backup-QB floor plus BUF's 35% blitz (the 'Panthers-rule risk' already flagged on the slip) made a WR1 over fragile. QB-health and backup-floor input (judgment) |
| ARI@DAL | PP40 | slip | CeeDee Lamb rec O4.5 | 7.0 | HIT |  |
| ARI@DAL | UD20 | slip | CeeDee Lamb rec O4.5 | 7.0 | HIT |  |
| ARI@DAL | PP20 | slip | CeeDee Lamb rec O4.5 | 7.0 | HIT |  |
| ARI@DAL | PP25 | slip | CeeDee Lamb rec O6.5 | 7.0 | HIT |  |
| ARI@DAL | PP chat | slip | CeeDee Lamb rec O7.5 | 7.0 | MISS | 7 catches on 11 targets (39% share, so volume was there). DAL threw only 29 times with Pollard running for 137 and Prescott sacked 4 times. A 7.5 line needs about 30+ attempts or an 70%+ catch rate on deeper looks. The input was DAL's run lean as a 7-pt favorite (team pass-attempt projection); 7.5 was a high rung (judgment) |
| ARI@DAL | FD7/FD8 | slip | CeeDee Lamb recyds O49.5 | 58.0 | HIT |  |
| BAL@BUF | PP chat | slip | James Cook rushyds O59.5 | 80.0 | HIT |  |
| TEN@CIN | PP40 | slip | Tee Higgins fantasy O14.5 | 37.5 | HIT |  |
| TEN@CIN | PP20 | slip | Tee Higgins recyds O68.5 | 155.0 | HIT |  |
| TEN@CIN | FD7/FD8 | slip | Tee Higgins rec O3.5 | 10.0 | HIT |  |

## Pending slip legs (games not final or later window)
- Puka, Stafford, K. Walker, K. Williams/Corum, Mahomes legs (4 PM games)

## Shared files
- ../game_scripts_2026.csv
- ../explosives_allowed.md
