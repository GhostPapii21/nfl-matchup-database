# Week 9 1 p.m. ET: scoring and defensive explosive-play audit

**Retrieved:** 2026-11-08 15:12:48 ET  
**Coverage:** the seven 1 p.m. ET games: CLE–NO, DAL–IND, DEN–CAR, DET–MIA, NYG–PHI, NYJ–KC, and LAR–WAS.  
**Status:** rolling, in-game snapshot; not final game totals.

## Operational definition

For this audit, an explosive play is a **20+ yard scrimmage gain on one play**. This is an audit threshold for this file, not a claim that the model's final X threshold has been selected. Kickoff and punt returns are excluded. A touchdown is counted once at its play yardage.

The PBP sometimes names a defender at the end of the play. Those names are retained as the **reported contact/tackle names**. They do not prove that defender was assigned to cover the receiver or caused the gain. Individual coverage responsibility is unverified for every row here.

## Explosive-play production by offensive position

| Position of player credited with the gain | Plays | Scrimmage yards on those plays |
|---|---:|---:|
| WR | 8 | 230 |
| RB | 3 | 93 |
| TE | 1 | 21 |
| **Total** | **12** | **344** |

Eleven of the 12 plays were receiving gains (321 yards, including RB receptions); one was a 23-yard RB run. These are event totals from the captured PBP, not each player's full-game receiving/rushing totals.

## Explosives allowed by opposing defensive unit

| Defense | Opposing explosive plays | Yards on those plays |
|---|---:|---:|
| Indianapolis | 3 | 89 |
| Denver | 3 | 64 |
| New Orleans | 1 | 60 |
| Los Angeles Rams | 1 | 45 |
| New York Jets | 1 | 25 |
| Washington | 1 | 21 |
| Detroit | 1 | 20 |
| New York Giants | 1 | 20 |

Unit-level allowed totals are supported by the play-by-play. They are not defender-allowed coverage statistics.

## Verified explosive events

| Game | Offense and player | Play | Defense charged at team level | PBP contact names, if listed |
|---|---|---|---|---|
| Browns–Saints | CLE — Denzel Boston (WR), 60 yd | Deep reception, Q3 11:15 | Saints | K. McKinstry |
| Cowboys–Colts | DAL — Jonathan Mingo (WR), 23 yd | Reception, Q1 13:46 | Colts | K. Harris; H. Wohler |
| Cowboys–Colts | DAL — CeeDee Lamb (WR), 22 yd | Reception, Q2 0:38 | Colts | B. Boettcher |
| Cowboys–Colts | DAL — CeeDee Lamb (WR), 44 yd TD | Reception, Q2 0:28 | Colts | Not listed on scoring line |
| Broncos–Panthers | CAR — Tetairoa McMillan (WR), 20 yd | Reception, Q2 4:12 | Broncos | P. Surtain |
| Broncos–Panthers | CAR — Chuba Hubbard (RB), 23 yd | Rush, Q2 1:49 | Broncos | T. Rapp |
| Broncos–Panthers | CAR — Darren Waller (TE), 21 yd | Reception, Q3 15:00 | Broncos | J. Skinner |
| Lions–Dolphins | MIA — Caleb Douglas (WR), 20 yd | Reception, Q1 3:30 | Lions | R. McCreary; B. Branch |
| Giants–Eagles | PHI — Darius Cooper (WR), 20 yd | Reception, Q2 3:38 | Giants | A. Washington; A. Reese |
| Jets–Chiefs | KC — Kenneth Walker (RB), 25 yd TD | Receiving TD, Q2 5:45 | Jets | Not listed on scoring line |
| Rams–Commanders | WAS — Rachaad White (RB), 45 yd | Reception, Q2 15:00 | Rams | K. Curl; O. Speights |
| Rams–Commanders | LAR — Puka Nacua (WR), 21 yd | Reception, Q2 6:46 | Commanders | S. Styles |

## Scoring players logged

The refreshed scoring-play CSV now records the following touchdown scorers found in the game pages: Seth McGowan (RB), Jake Ferguson (TE), CeeDee Lamb (WR), Courtland Sutton (WR), Tommy Tremble (TE), Darren Waller (TE), Saquon Barkley (RB), Kenneth Walker (RB; two receiving TDs), Van Jefferson (WR), and Blake Corum (RB). It also logs the verified field goals and resolves Denver's previously unresolved second-quarter field goal to Wil Lutz.

The live page snapshots do not all advance on the same clock. The Chiefs game page's scoring recap did not reconcile with the scoreboard's quarter points at capture, so any additional Chiefs scoring identity remains pending rather than inferred.

## Defensive matchup interpretation

This record says **which offense produced the explosive play and which opposing defense allowed it**. It does not establish which corner, safety, linebacker, or zone responsibility surrendered a pass. A listed PBP contact name can be the tackler after a catch or a run. Use charted coverage assignments or tracking data before attributing a receiver's yards to a named defender.

Sources: each play's CBS Gametracker PBP URL and the position-reference URL are recorded row by row in `WEEK9_1PM_EXPLOSIVE_PLAYS_20261108_1512ET.csv`. Scoring events (with play-by-play source links) are recorded in `WEEK9_1PM_SCORING_PLAYS_20261108_1445ET.csv`.
