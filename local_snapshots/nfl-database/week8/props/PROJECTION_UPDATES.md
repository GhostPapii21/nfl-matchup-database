# Week 8 projection updates (props pass, Oct 29 2026)

Only changes with a concrete data reason. Nothing moved toward a line.

## Rules
- A: missing-participation denominator (GAME_SCRIPT_2026-10-29 issue #3). Weeks with no offensive snaps in `fixes/src/snap_counts_2026.parquet` are dropped from the L3/season averages. Applied when |f-1| >= 0.08, capped at 4.0. Applied only if he played the last game, or he is Questionable and returning (then the projection assumes he plays).
- B: small-sample efficiency. With fewer than 20 season targets, yards/target is regressed to position average (WR 8.1, TE 6.9, RB 5.4) with a 20-target prior. Defense multiplier kept.
- Scope: only players whose FD main line was more than 25% from the median were audited.
- compare.py also releases the production-verdict-NO block only for rule-A players (the verdict was computed on the deflated volume), and sets NO BET for anyone with fewer than 3 games with snaps.

## Changes (tgt / rec / rec yds / car / rush yds)

- BAL@BUF|Ja'Kobi Lane: 3.0/2.0/18/0/0 -> 5.2/3.5/38/0.0/0.0. A: 4 absent-row week(s) with no offensive snaps (snap_counts_2026) removed from denominator; volume x1.73 ; B: 13 season targets, YPT 5.8 regressed to 7.2 (prior 8.1, 20 tgt)
- BAL@BUF|Josh Cuevas: 2.9/2.2/36/0/0 -> 2.9/2.2/28/0/0. B: 11 season targets, YPT 10.8 regressed to 8.3 (prior 6.9, 20 tgt)
- BAL@BUF|DJ Moore: 1.8/1.1/18/0.5/1 -> 3.3/2.0/33.0/0.9/2.0. A: 2 absent-row week(s) with no offensive snaps (snap_counts_2026) removed from denominator; volume x1.85 (Questionable, returning from absence: projection assumes he plays; confirm active)
- BAL@BUF|James Cook III: 2.2/1.4/12/19.7/102 -> 2.2/1.4/11/19.7/102. B: 14 season targets, YPT 6.4 regressed to 5.8 (prior 5.4, 20 tgt)
- BAL@BUF|Ty Johnson: 2.5/2.3/27/0.5/2 -> 2.9/2.7/20/0.6/2.0. A: 2 absent-row week(s) with no offensive snaps (snap_counts_2026) removed from denominator; volume x1.17 ; B: 12 season targets, YPT 12.9 regressed to 8.2 (prior 5.4, 20 tgt)
- BAL@BUF|Joshua Palmer: 2.3/0.8/25/0/0 -> 3.4/1.2/33/0.0/0.0. A: 2 absent-row week(s) with no offensive snaps (snap_counts_2026) removed from denominator; volume x1.50 ; B: 12 season targets, YPT 9.8 regressed to 8.7 (prior 8.1, 20 tgt)
- TEN@CIN|Gunnar Helm: 2.6/1.7/14/0/0 -> 2.6/1.7/18/0/0. B: 18 season targets, YPT 4.7 regressed to 5.8 (prior 6.9, 20 tgt)
- ARI@DAL|Brevyn Spann-Ford: 2.5/1.9/18/0/0 -> 2.5/1.9/19/0/0. B: 13 season targets, YPT 6.1 regressed to 6.6 (prior 6.9, 20 tgt)
- MIN@DET|Jordan Addison: 4.2/2.3/30/0.4/0 -> 5.7/3.1/41.0/0.5/0.0. A: 1 absent-row week(s) with no offensive snaps (snap_counts_2026) removed from denominator; volume x1.36
- MIN@DET|Justin Jefferson: 5.9/4.5/55/0.2/-2 -> 8.1/6.2/75.0/0.3/-3.0. A: 1 absent-row week(s) with no offensive snaps (snap_counts_2026) removed from denominator; volume x1.37
- LV@NYJ|Mason Taylor: 5.2/4.2/29/0/0 -> 5.7/4.6/32.0/0.0/0.0. A: 2 absent-row week(s) with no offensive snaps (snap_counts_2026) removed from denominator; volume x1.10
- LV@NYJ|Omar Cooper Jr.: 3.8/3.3/84/0/0 -> 6.4/5.6/92/0.0/0.0. A: 4 absent-row week(s) with no offensive snaps (snap_counts_2026) removed from denominator; volume x1.70 ; B: 13 season targets, YPT 19.1 regressed to 12.4 (prior 8.1, 20 tgt)
- LV@NYJ|Adonai Mitchell: 2.0/1.0/16/0/0 -> 5.2/2.6/46/0.0/0.0. A: 4 absent-row week(s) with no offensive snaps (snap_counts_2026) removed from denominator; volume x2.58 ; B: 18 season targets, YPT 6.8 regressed to 7.5 (prior 8.1, 20 tgt)
- CLE@PIT|Quinshon Judkins: 2.5/2.3/14/9.9/31 -> 3.4/3.1/19.0/13.4/42.0. A: 1 absent-row week(s) with no offensive snaps (snap_counts_2026) removed from denominator; volume x1.35
- IND@JAX|Bhayshul Tuten: 2.6/2.2/27/19.6/89 -> 2.6/2.2/21/19.6/89. B: 14 season targets, YPT 9.0 regressed to 6.9 (prior 5.4, 20 tgt)
- IND@JAX|Chris Rodriguez Jr.: 0.5/0.2/2/7.6/36 -> 0.5/0.2/3/7.6/36. B: 2 season targets, YPT 3.0 regressed to 5.2 (prior 5.4, 20 tgt)
- LAC@LA|Ladd McConkey: 2.4/1.6/22/0/0 -> 3.1/2.1/24/0.0/0.0. A: 1 absent-row week(s) with no offensive snaps (snap_counts_2026) removed from denominator; volume x1.30 ; B: 18 season targets, YPT 11.1 regressed to 9.5 (prior 8.1, 20 tgt)
- LAC@LA|Puka Nacua: 12.5/9.8/103/1.0/4 -> 14.0/11.0/115.0/1.1/4.0. A: 2 absent-row week(s) with no offensive snaps (snap_counts_2026) removed from denominator; volume x1.12
- LAC@LA|Blake Corum: 2.4/1.5/14/10.9/56 -> 2.4/1.5/12/10.9/56. B: 14 season targets, YPT 7.1 regressed to 6.1 (prior 5.4, 20 tgt)
- KC@DEN|RJ Harvey: 3.7/3.4/31/3.4/11 -> 4.0/3.7/34.0/3.7/12.0. A: 1 absent-row week(s) with no offensive snaps (snap_counts_2026) removed from denominator; volume x1.09
- KC@DEN|J.K. Dobbins: 1.9/1.8/6/12.0/34 -> 1.9/1.8/9/12.0/34. B: 9 season targets, YPT 3.0 regressed to 4.7 (prior 5.4, 20 tgt)
- KC@DEN|Jonah Coleman: 0.9/0.9/6/2.6/11 -> 2.5/2.5/14/7.1/30.0. A: 4 absent-row week(s) with no offensive snaps (snap_counts_2026) removed from denominator; volume x2.75 ; B: 5 season targets, YPT 6.8 regressed to 5.7 (prior 5.4, 20 tgt)
- NE@MIA|A.J. Brown: 4.6/2.2/26/0/0 -> 7.9/3.8/45.0/0.0/0.0. A: 4 absent-row week(s) with no offensive snaps (snap_counts_2026) removed from denominator; volume x1.72
- NE@MIA|Caleb Douglas: 2.0/1.5/28/0/0 -> 4.8/3.6/50/0.0/0.0. A: 3 absent-row week(s) with no offensive snaps (snap_counts_2026) removed from denominator; volume x2.41 ; B: 13 season targets, YPT 14.1 regressed to 10.5 (prior 8.1, 20 tgt)
- NE@MIA|Chris Bell: 4.3/2.0/26/0.2/5 -> 4.3/2.0/30/0.2/5. B: 19 season targets, YPT 6.2 regressed to 7.2 (prior 8.1, 20 tgt)
- NE@MIA|Ollie Gordon II: 2.2/1.6/4/13.7/68 -> 2.2/1.6/10/13.7/68. B: 8 season targets, YPT 1.8 regressed to 4.4 (prior 5.4, 20 tgt)
- PHI@WAS|Rachaad White: 2.4/2.3/12/6.3/27 -> 3.3/3.1/16.0/8.6/37.0. A: 1 absent-row week(s) with no offensive snaps (snap_counts_2026) removed from denominator; volume x1.36
- PHI@WAS|Jeremy McNichols: 0.0/0.0/0/1.7/5 -> 0.0/0.0/0.0/6.4/19.0. A: 5 absent-row week(s) with no offensive snaps (snap_counts_2026) removed from denominator; volume x3.75
- CAR@GB|John Metchie III: 4.4/2.3/23/0/0 -> 4.4/2.3/29/0/0. B: 18 season targets, YPT 5.6 regressed to 6.9 (prior 8.1, 20 tgt)
- CAR@GB|Brycen Tremayne: 1.7/1.1/18/0/0 -> 1.7/1.1/14/0/0. B: 10 season targets, YPT 11.5 regressed to 9.2 (prior 8.1, 20 tgt)
- CAR@GB|Savion Williams: 2.0/1.8/19/2.0/6 -> 3.9/3.5/29/3.9/12.0. A: 5 absent-row week(s) with no offensive snaps (snap_counts_2026) removed from denominator; volume x1.94 ; B: 7 season targets, YPT 11.3 regressed to 8.9 (prior 8.1, 20 tgt)
- CAR@GB|MarShawn Lloyd: 2.1/1.5/7/8.6/23 -> 2.1/1.5/8/8.6/23. B: 16 season targets, YPT 4.1 regressed to 4.8 (prior 5.4, 20 tgt)
- CAR@GB|Josh Jacobs: 2.0/1.4/13/3.0/10 -> 7.8/5.4/39/11.7/39.0. A: 6 absent-row week(s) with no offensive snaps (snap_counts_2026) removed from denominator; volume x3.89 ; B: 7 season targets, YPT 7.9 regressed to 6.0 (prior 5.4, 20 tgt)

## >25% gaps left unchanged

- BAL@BUF Keon Coleman rec_yds: FD 29.5 vs 64 (+117%). No participation or sample issue in the data.
- PHI@WSH Treylon Burks rec_yds: FD 22.5 vs 43 (+91%). No participation or sample issue in the data. Questionable.
- TEN@CIN Elic Ayomanor rec_yds: FD 18.5 vs 35 (+89%). No participation or sample issue in the data.
- TEN@CIN Dohnte Meyers receptions: FD 1.5 vs 2.7 (+80%). No participation or sample issue in the data.
- BAL@BUF Rashod Bateman rec_yds: FD 24.5 vs 44 (+80%). No participation or sample issue in the data.
- TEN@CIN Dohnte Meyers rec_yds: FD 18.5 vs 31 (+68%). No participation or sample issue in the data.
- ARI@DAL Jake Ferguson receptions: FD 1.5 vs 2.5 (+67%). No participation or sample issue in the data.
- ARI@DAL Kendrick Bourne rec_yds: FD 32.5 vs 54 (+66%). No participation or sample issue in the data.
- NE@MIA DeMario Douglas receptions: FD 2.5 vs 4.1 (+64%). No participation or sample issue in the data.
- TEN@CIN Tee Higgins rec_yds: FD 68.5 vs 112 (+64%). No participation or sample issue in the data.
- BAL@BUF Justice Hill rec_yds: FD 10.5 vs 17 (+62%). No participation or sample issue in the data.
- NE@MIA Greg Dulcich rec_yds: FD 28.5 vs 46 (+61%). No participation or sample issue in the data. Questionable.
- CAR@GB Chuba Hubbard rec_yds: FD 15.5 vs 25 (+61%). No participation or sample issue in the data.
- BAL@BUF Justice Hill receptions: FD 1.5 vs 2.4 (+60%). No participation or sample issue in the data.
- LV@NYJ Kenyon Sadiq receptions: FD 1.5 vs 2.4 (+60%). No participation or sample issue in the data.
- ARI@DAL Kendrick Bourne receptions: FD 3.5 vs 5.5 (+57%). No participation or sample issue in the data.
- ATL@TB Chris Godwin Jr. rec_yds: FD 29.5 vs 46 (+56%). No participation or sample issue in the data.
- MIN@DET T.J. Hockenson rec_yds: FD 38.5 vs 60 (+56%). No participation or sample issue in the data.
- IND@JAX Jonathan Taylor rec_yds: FD 17.5 vs 27 (+54%). No participation or sample issue in the data.
- BAL@BUF Derrick Henry rec_yds: FD 6.5 vs 10 (+54%). No participation or sample issue in the data.
- CAR@GB Darren Waller rec_yds: FD 19.5 vs 30 (+54%). No participation or sample issue in the data.
- LV@NYJ Michael Mayer rec_yds: FD 25.5 vs 39 (+53%). No participation or sample issue in the data.
- KC@DEN Kenneth Walker III rush_yds: FD 86.5 vs 132 (+53%). No participation or sample issue in the data.
- NE@MIA DeMario Douglas rec_yds: FD 31.5 vs 48 (+52%). No participation or sample issue in the data.
- BAL@BUF Keon Coleman receptions: FD 2.5 vs 3.8 (+52%). No participation or sample issue in the data.
- NE@MIA Jaylen Wright rush_yds: FD 16.5 vs 8 (-52%). No participation or sample issue in the data.
- LV@NYJ Garrett Wilson rec_yds: FD 55.5 vs 84 (+51%). No participation or sample issue in the data.
- BAL@BUF Zay Flowers rec_yds: FD 81.5 vs 122 (+50%). No participation or sample issue in the data.
- CLE@PIT Jaylen Warren rec_yds: FD 25.5 vs 38 (+49%). No participation or sample issue in the data.
- BAL@BUF Khalil Shakir rec_yds: FD 38.5 vs 57 (+48%). No participation or sample issue in the data.
- LV@NYJ Michael Mayer receptions: FD 2.5 vs 3.7 (+48%). No participation or sample issue in the data.
- CLE@PIT Jaylen Warren rush_yds: FD 64.5 vs 95 (+47%). No participation or sample issue in the data.
- NE@MIA Hunter Henry rec_yds: FD 39.5 vs 58 (+47%). No participation or sample issue in the data.
- PHI@WSH Treylon Burks receptions: FD 1.5 vs 2.2 (+47%). No participation or sample issue in the data. Questionable.
- TEN@CIN Chase Brown rec_yds: FD 20.5 vs 30 (+46%). No participation or sample issue in the data.
- ATL@TB Chris Godwin Jr. receptions: FD 3.5 vs 5.1 (+46%). No participation or sample issue in the data.
- NE@MIA Malik Washington rec_yds: FD 40.5 vs 59 (+46%). No participation or sample issue in the data. Questionable.
- CLE@PIT Jerry Jeudy rec_yds: FD 23.5 vs 34 (+45%). No participation or sample issue in the data.
- MIN@DET T.J. Hockenson receptions: FD 4.5 vs 6.5 (+44%). No participation or sample issue in the data.
- CAR@GB Tetairoa McMillan rec_yds: FD 71.5 vs 103 (+44%). No participation or sample issue in the data.
- CLE@PIT Jaylen Warren receptions: FD 2.5 vs 3.6 (+44%). No participation or sample issue in the data.
- CLE@PIT Pat Freiermuth receptions: FD 2.5 vs 3.6 (+44%). No participation or sample issue in the data.
- CAR@GB Tetairoa McMillan receptions: FD 5.5 vs 7.9 (+44%). No participation or sample issue in the data.
- BAL@BUF Justice Hill rush_yds: FD 10.5 vs 15 (+43%). No participation or sample issue in the data.
- PHI@WSH Antonio Williams rec_yds: FD 32.5 vs 46 (+42%). No participation or sample issue in the data.
- TEN@CIN Chase Brown receptions: FD 3.5 vs 4.9 (+40%). No participation or sample issue in the data.
- TEN@CIN Elic Ayomanor receptions: FD 1.5 vs 2.1 (+40%). No participation or sample issue in the data.
- CLE@PIT Jaylen Warren rush_rec_yds: FD 95.5 vs 133 (+39%). No participation or sample issue in the data.
- LAC@LAR Kyren Williams rush_yds: FD 59.5 vs 82 (+38%). No participation or sample issue in the data.
- IND@JAX Brenton Strange receptions: FD 3.5 vs 4.8 (+37%). No participation or sample issue in the data.
- NE@MIA Rhamondre Stevenson rec_yds: FD 17.5 vs 24 (+37%). No participation or sample issue in the data.
- CAR@GB Tommy Tremble rec_yds: FD 15.5 vs 21 (+36%). No participation or sample issue in the data.
- LV@NYJ Ashton Jeanty rec_yds: FD 27.5 vs 37 (+34%). No participation or sample issue in the data.
- NE@MIA Hunter Henry receptions: FD 3.5 vs 4.7 (+34%). No participation or sample issue in the data.
- ARI@DAL Javonte Williams receptions: FD 1.5 vs 2.0 (+33%). No participation or sample issue in the data.
- IND@JAX Brenton Strange rec_yds: FD 37.5 vs 50 (+33%). No participation or sample issue in the data.
- KC@DEN Kenneth Walker III rush_rec_yds: FD 109.5 vs 146 (+33%). No participation or sample issue in the data.
- KC@DEN Travis Kelce rec_yds: FD 46.5 vs 62 (+33%). No participation or sample issue in the data.
- CLE@PIT Jerry Jeudy receptions: FD 2.5 vs 3.3 (+32%). No participation or sample issue in the data.
- IND@JAX Jakobi Meyers rec_yds: FD 39.5 vs 52 (+32%). No participation or sample issue in the data. Questionable.
- KC@DEN Kenneth Walker III receptions: FD 3.5 vs 2.4 (-31%). No participation or sample issue in the data.
- CAR@GB Matthew Golden rec_yds: FD 59.5 vs 78 (+31%). No participation or sample issue in the data. Questionable.
- NE@MIA Malik Washington receptions: FD 4.5 vs 5.9 (+31%). No participation or sample issue in the data. Questionable.
- TEN@CIN Carnell Tate receptions: FD 4.5 vs 5.9 (+31%). No participation or sample issue in the data. Questionable.
- ARI@DAL Trey McBride receptions: FD 7.5 vs 9.8 (+31%). No participation or sample issue in the data.
- LV@NYJ Ashton Jeanty rush_yds: FD 49.5 vs 35 (-29%). No participation or sample issue in the data.
- LV@NYJ Garrett Wilson receptions: FD 4.5 vs 5.8 (+29%). No participation or sample issue in the data.
- TEN@CIN Wan'Dale Robinson receptions: FD 4.5 vs 5.8 (+29%). No participation or sample issue in the data.
- TEN@CIN Carnell Tate rec_yds: FD 51.5 vs 66 (+28%). No participation or sample issue in the data. Questionable.
- BAL@BUF Zay Flowers receptions: FD 6.5 vs 8.3 (+28%). No participation or sample issue in the data.
- CLE@PIT Harold Fannin Jr. rec_yds: FD 35.5 vs 45 (+27%). No participation or sample issue in the data.
- ARI@DAL Michael Wilson receptions: FD 4.5 vs 5.7 (+27%). No participation or sample issue in the data. Questionable.
- CLE@PIT Germie Bernard receptions: FD 4.5 vs 5.7 (+27%). No participation or sample issue in the data.
- BAL@BUF Justice Hill rush_rec_yds: FD 24.5 vs 31 (+26%). No participation or sample issue in the data.
- MIN@DET Jahmyr Gibbs rush_yds: FD 86.5 vs 109 (+26%). No participation or sample issue in the data. Questionable.
- LV@NYJ Tre Tucker rec_yds: FD 49.5 vs 62 (+25%). No participation or sample issue in the data.

## Calibration caveat
Median edge across all 254 props is +21.8% (rec yds +28.6%). The model runs above FanDuel across the board. Read the leans as a ranking, not as a calibrated win rate. Projections were not shaded toward the lines to fix this.

## P(over) method
Lognormal: median = model median; 25th/75th = median x (lo/tot, hi/tot); sigma = (ln q75 - ln q25)/1.349, floored at rec yds 0.55, rush 0.40, rush+rec 0.40, receptions 0.40. Lean OVER if P >= 0.60 and edge >= 10%; UNDER if P <= 0.40 and edge <= -10%. Rung = highest FD alt rung with model P >= 0.68 (0.80 if Q or volatile), model P > implied, and odds no shorter than -250.