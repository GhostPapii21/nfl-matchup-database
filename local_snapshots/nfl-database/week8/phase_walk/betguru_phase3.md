# BetGuru — PHASE 3 (Offense, player type, opportunity) — Sun Nov 1, 2026
Script lines 302–408. Phases 4+ NOT run. src/phase3.py. Alive legs = Phase 2 PASS and 8A not GAP/FAIL (+ Bowers/McBride/Goedert/T. Warren held PENDING on LB/S mapping per parent). **DK Metcalf 40+: ALIVE** (corrected chart INSUFFICIENT FILM; no shadow; mapped Tyson Campbell; film GAP disclosed).
Sources: nflverse pbp/snap counts 2026 (Oct 31 7:17 PM ET); nflverse NGS passing/receiving/rushing season rows (https://github.com/nflverse/nflverse-data/releases/download/nextgen_stats/ngs_*.parquet); FTN charting (blitz); ESPN WR/CB sheet; ESPN injuries + depth charts (Oct 31 ~7:30 PM ET); PFR cache Oct 29 (fresh pull 403); Sharp coverage schemes (Updated Oct 27) + StatRankings man/zone coverage rate (thru Oct 30, upd 10/31) https://statrankings.com/nfl/advanced/teams/coverage/man-coverage-rate.
Gates: 60% L3 snap gate (user rule); target/carry share L3 not down >15% vs season; missing input = GAP.

|Player|Market|Opp|Phase 3|Gate notes|
|-|-|-|-|-|
|Aaron Jones|rushyds|DET|PASS|—|
|Amon-Ra St. Brown|rec|MIN|PASS|—|
|Bijan Robinson|rushyds|TB|PASS|—|
|Braelon Allen|rushyds|LV|PASS|—|
|Brock Bowers|rec|NYJ|PASS (8A PENDING)|—|
|Brock Bowers|recyds|NYJ|PASS (8A PENDING)|—|
|CeeDee Lamb|rec|ARI|PASS|—|
|DK Metcalf|recyds|CLE|PASS (alive; no shadow evidence, mapped T. Campbell; film GAP disclosed)|—|
|Dallas Goedert|rec|WAS|PASS (8A PENDING)|—|
|Drake London|recyds|TB|PASS|—|
|Garrett Wilson|recyds|LV|PASS|—|
|Jahmyr Gibbs|rushyds|MIN|PASS — CAUTION (pbp/FTN)|MIN #1 vs edge runs, fewer light boxes; film UNVERIFIED|
|James Cook|rushyds|BAL|PASS|—|
|Javonte Williams|rushyds|ARI|PASS|—|
|Jonathan Taylor|rushyds|JAX|PASS|—|
|Justin Jefferson|recyds|DET|PASS|—|
|Kenneth Walker III|rushyds|DEN|PASS|—|
|Parker Washington|recyds|IND|PASS|—|
|Puka Nacua|rec|LAC|PASS|—|
|Puka Nacua|recyds|LAC|PASS|—|
|Tee Higgins|recyds|TEN|PASS|—|
|Trey McBride|rec|DAL|PASS (8A PENDING)|film UNVERIFIED; alignment GAP (disclosed)|
|Trey McBride|recyds|DAL|PASS (8A PENDING)|film UNVERIFIED; alignment GAP (disclosed)|
|Tyler Warren|recyds|JAX|GAP|INJURY RETURN after missing wks [6, 7] — no post-return sample; role-regime unverified|
|Zay Flowers|recyds|BUF|PASS|—|

### Aaron Jones (MIN vs DET) — rushyds · rung None @ None
- **PHASE 3: PASS** — role, participation and opportunity verified
- Window: declared baseline = all 6 MIN games (wks [1, 2, 3, 4, 5, 7]); L3 = player's last 3 ACTIVE games, wks [4, 5, 7] (inactive weeks excluded, not counted as zeros). Missed/absent: none (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 65%, L3 62% (per wk 1:46%, 2:81%, 3:80%, 4:73%, 5:87%, 7:25%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: Active — Jones (knee) doesn't have an injury designation for Sunday's game against the Lions, Dane Mizutani of the St. Paul Pione [ESPN injuries API 7:30 PM ET]
- Opportunity: carries 105 (L3 53); RB carry share season 72.9%, L3 74.6%; GL carries (≤5) 1; targets 19, catches 13; receiving routes GAP [pbp].
- Efficiency/explosive: YPC 4.15; success 35.2%; ≤0 yds 17.1%; 15+ runs 7; NGS: RYOE/att -0.60, 8+ box 21.0%, time to LOS 2.70s [pbp, NGS].
- Run direction/gap (carry direction, not concept): {'right': np.int64(47), 'left': np.int64(35), 'middle': np.int64(23)} / {'guard': np.int64(35), 'tackle': np.int64(32), 'end': np.int64(15)}. Concept: GAP.
- Archetype: early-down RB. Trend: L3 carry share 74.6% vs 72.9% → stable/up.
- QB (MIN; primary K.Murray): 198 dropbacks, 163 att, cmp 65.0%, YPA 6.67, EPA/db -0.022, sacks 18 (9.1%), scrambles 17 [pbp]. vs blitz (FTN n_blitzers>0, n=72): sack 6.9%, yds/db 5.06; no blitz (n=126): sack 10.3%, yds/db 5.95. NGS: Kyler Murray TTT 2.91s, CPOE +0.7, intended air 7.2. OL now: LT Christian Darrisaw, LG Joe Huber, C Blake Brandel, RG Will Fries, RT Brian O'Neill; OL injuries: Brian O'Neill OT Active; Joe Huber G Active; Caleb Tiernan OT Active; Christian Darrisaw OT Active; Michael Jurgens C Active [ESPN].
- Teammate injuries / redistribution: none (skill) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.
- Partial games (snap <40%, treated as in-game exit, not role change): wks [7].

### Amon-Ra St. Brown (DET vs MIN) — rec · rung None @ None
- **PHASE 3: PASS** — role, participation and opportunity verified
- Window: declared baseline = all 6 DET games (wks [1, 2, 3, 4, 5, 7]); L3 = player's last 3 ACTIVE games, wks [4, 5, 7] (inactive weeks excluded, not counted as zeros). Missed/absent: none (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 87%, L3 87% (per wk 1:90%, 2:95%, 3:74%, 4:96%, 5:86%, 7:78%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: Active — St. Brown (ankle) practiced in full Thursday. [ESPN injuries API 7:30 PM ET]
- Alignment/routes (ESPN WR/CB sheet, season-to-date): align tag S, LWR/slot/RWR 25%/49%/26%; routes 209; targets/route 31%; YPRR 0.56. Route participation per dropback: GAP (no free per-game routes; nflverse 2026 participation 404).
- Opportunity: targets 68 (L3 33); target share (player tgt / team receiver tgt) season 31.1%, L3 29.7% — share of pass attempts is not used. Receptions 46 (L3 23). aDOT 8.9; RZ tgt 16; 3rd-down tgt 22 (42% of team 3rd-down tgt); 2-min (≤120s left in half) tgt 7 [pbp].
- Conversion/efficiency/explosive: catch rate 67.6%; YPT 7.72; YAC/rec 3.8; 20+ yd catches 7; NGS: sep 2.77, cushion 6.69, YAC 4.04 vs exp 4.43, share of team intended air yds 32.4% [pbp, NGS].
- Archetype (supported by numbers above): volume/possession + red-zone option. Trend: L3 share 29.7% vs season 31.1% → stable/up.
- Scheme: Sharp (Updated Oct 27; page modified 2026-10-29 15:53 ET) man 5.3/zone 86.5/MOFC 31.6/MOFO 61.2 (man rank #32 of 32). StatRankings (thru Oct 30, upd 10/31): man not in top-25 list (bottom 7) % rank 26-32, zone 78.9% — both put it in the low-man group
- PFR: **PFR cache Oct 29 (fresh pull 403)**.
- 8A status: PENDING_FILM; film route/alignment read counts only if every cited play matches pbp, otherwise UNVERIFIED → GAP (disclosed).
- QB (DET; primary J.Goff): 240 dropbacks, 223 att, cmp 67.3%, YPA 8.02, EPA/db +0.282, sacks 12 (5.0%), scrambles 5 [pbp]. vs blitz (FTN n_blitzers>0, n=78): sack 6.4%, yds/db 7.42; no blitz (n=162): sack 4.3%, yds/db 6.99. NGS: Jared Goff TTT 2.84s, CPOE +1.7, intended air 8.4. OL now: LT Penei Sewell, LG Christian Mahogany, C Cade Mays, RG Tate Ratledge, RT Blake Miller; OL injuries: Seth McLaughlin C Active; Cade Mays C Active; Ben Bartch G Injured Reserve [ESPN].
- Teammate injuries / redistribution: Isiah Pacheco (RB, Injured Reserve) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.

### Bijan Robinson (ATL vs TB) — rushyds · rung None @ None
- **PHASE 3: PASS** — role, participation and opportunity verified
- Window: declared baseline = all 7 ATL games (wks [1, 2, 3, 4, 5, 6, 7]); L3 = player's last 3 ACTIVE games, wks [5, 6, 7] (inactive weeks excluded, not counted as zeros). Missed/absent: none (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 71%, L3 80% (per wk 1:77%, 2:51%, 3:72%, 4:60%, 5:81%, 6:78%, 7:81%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: not on ESPN injury report [ESPN injuries API 7:30 PM ET]
- Opportunity: carries 131 (L3 46); RB carry share season 70.4%, L3 80.7%; GL carries (≤5) 7; targets 32, catches 25; receiving routes GAP [pbp].
- Efficiency/explosive: YPC 5.37; success 46.6%; ≤0 yds 12.2%; 15+ runs 8; NGS: RYOE/att +1.20, 8+ box 22.1%, time to LOS 2.75s [pbp, NGS].
- Run direction/gap (carry direction, not concept): {'left': np.int64(62), 'right': np.int64(39), 'middle': np.int64(30)} / {'guard': np.int64(37), 'tackle': np.int64(36), 'end': np.int64(28)}. Concept: GAP.
- Archetype: early-down + goal-line + receiving RB. Trend: L3 carry share 80.7% vs 70.4% → stable/up.
- QB (ATL; primary M.Penix): 224 dropbacks, 200 att, cmp 64.0%, YPA 7.39, EPA/db -0.101, sacks 16 (7.1%), scrambles 8 [pbp]. vs blitz (FTN n_blitzers>0, n=90): sack 7.8%, yds/db 6.71; no blitz (n=134): sack 6.7%, yds/db 6.16. NGS: Michael Penix Jr. TTT 2.53s, CPOE +0.1, intended air 7.3. OL now: LT Jake Matthews, LG Matthew Bergeron, C Ryan Neuzil, RG Chris Lindstrom, RT Jawaan Taylor; OL injuries: Jawaan Taylor OT Active [ESPN].
- Teammate injuries / redistribution: Beaux Collins (WR, Injured Reserve); Olamide Zaccheaus (WR, Questionable); Brian Robinson Jr. (RB, Out) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.

### Braelon Allen (NYJ vs LV) — rushyds · rung None @ None
- **PHASE 3: PASS** — role, participation and opportunity verified
- Window: declared baseline = all 7 NYJ games (wks [1, 2, 3, 4, 5, 6, 7]); L3 = player's last 3 ACTIVE games, wks [5, 6, 7] (inactive weeks excluded, not counted as zeros). Missed/absent: none (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 67%, L3 84% (per wk 1:40%, 2:31%, 3:52%, 4:94%, 5:86%, 6:87%, 7:78%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: Active — Allen (ankle) was a full participant at Thursday's practice. [ESPN injuries API 7:30 PM ET]
- Opportunity: carries 91 (L3 58); RB carry share season 59.9%, L3 85.3%; GL carries (≤5) 2; targets 20, catches 15; receiving routes GAP [pbp].
- Efficiency/explosive: YPC 4.59; success 41.8%; ≤0 yds 17.6%; 15+ runs 7; NGS: RYOE/att +0.97, 8+ box 25.3%, time to LOS 2.70s [pbp, NGS].
- Run direction/gap (carry direction, not concept): {'right': np.int64(36), 'left': np.int64(34), 'middle': np.int64(21)} / {'guard': np.int64(35), 'tackle': np.int64(26), 'end': np.int64(9)}. Concept: GAP.
- Archetype: early-down + receiving RB. Trend: L3 carry share 85.3% vs 59.9% → stable/up.
- QB (NYJ; primary G.Smith): 237 dropbacks, 206 att, cmp 70.4%, YPA 7.88, EPA/db +0.100, sacks 21 (8.9%), scrambles 10 [pbp]. vs blitz (FTN n_blitzers>0, n=63): sack 14.3%, yds/db 7.27; no blitz (n=174): sack 6.9%, yds/db 5.94. NGS: Geno Smith TTT 2.92s, CPOE +6.4, intended air 7.0. OL now: LT Olu Fashanu, LG Dylan Parham, C Josh Myers, RG Joe Tippmann, RT Armand Membou; OL injuries: Max Mitchell OT Out; Dylan Parham G Questionable [ESPN].
- Teammate injuries / redistribution: Breece Hall (RB, Questionable) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.
- Partial games (snap <40%, treated as in-game exit, not role change): wks [2].

### Brock Bowers (LV vs NYJ) — rec · rung 6 @ -158
- **PHASE 3: PASS (8A PENDING)** — role, participation and opportunity verified
- Window: declared baseline = all 7 LV games (wks [1, 2, 3, 4, 5, 6, 7]); L3 = player's last 3 ACTIVE games, wks [5, 6, 7] (inactive weeks excluded, not counted as zeros). Missed/absent: [1, 2] (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 83%, L3 84% (per wk 3:79%, 4:82%, 5:70%, 6:98%, 7:84%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: Active — Bowers (calf) was a full practice participant Thursday. [ESPN injuries API 7:30 PM ET]
- Alignment/routes (ESPN WR/CB sheet, season-to-date): align tag S, LWR/slot/RWR 21%/57%/21%; routes 168; targets/route 28%; YPRR 0.54. Route participation per dropback: GAP (no free per-game routes; nflverse 2026 participation 404).
- Opportunity: targets 51 (L3 27); target share (player tgt / team receiver tgt) season 20.1%, L3 22.9% — share of pass attempts is not used. Receptions 34 (L3 18). aDOT 10.2; RZ tgt 7; 3rd-down tgt 21 (30% of team 3rd-down tgt); 2-min (≤120s left in half) tgt 6 [pbp].
- Conversion/efficiency/explosive: catch rate 66.7%; YPT 8.92; YAC/rec 4.1; 20+ yd catches 6; NGS: sep 2.34, cushion 5.74, YAC 4.33 vs exp 3.60, share of team intended air yds 25.7% [pbp, NGS].
- Archetype (supported by numbers above): primary target + red-zone option. Trend: L3 share 22.9% vs season 20.1% → stable/up.
- Scheme: Sharp (Updated Oct 27; page modified 2026-10-29 15:53 ET) man 23.8/zone 66.6/MOFC 45.2/MOFO 50.0 (man rank #8 of 32). StatRankings (thru Oct 30, upd 10/31): man 37.5% rank 12, zone 62.5% — rank order AGREES (within 5 spots)
- PFR: **PFR cache Oct 29 (fresh pull 403)**.
- 8A status: PENDING (Rico ruling on TE/slot→LB/S mapping). Candidate defenders (PFR cache Oct 29, fresh pull 403): Jamien Sherwood (LB, NYJ, G5): 18-15-163, cmp 83.3%, YPT 9.1, rat 122.9 | Demario Davis (LB, NYJ, G5): 18-12-133, cmp 66.7%, YPT 7.4, rat 88.4 | Dane Belton (S, NYJ, G5): 13-7-78, cmp 53.8%, YPT 6.0, rat 72.0
- QB (LV; primary K.Cousins): 279 dropbacks, 263 att, cmp 63.9%, YPA 7.37, EPA/db +0.127, sacks 10 (3.6%), scrambles 6 [pbp]. vs blitz (FTN n_blitzers>0, n=80): sack 0.0%, yds/db 6.45; no blitz (n=199): sack 5.0%, yds/db 6.96. NGS: Kirk Cousins TTT 2.89s, CPOE +2.7, intended air 8.5. OL now: LT Kolton Miller, LG Spencer Burford, C Tyler Linderbaum, RG Caleb Rogers, RT DJ Glaze; OL injuries: DJ Glaze OT Active; Jackson Powers-Johnson G Questionable; Bryce Cabeldue G Active [ESPN].
- Teammate injuries / redistribution: Carter Runyon (TE, Injured Reserve) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.
- Injury return: back since wk 3 (5 active games post-return).

### Brock Bowers (LV vs NYJ) — recyds · rung None @ None
- **PHASE 3: PASS (8A PENDING)** — role, participation and opportunity verified
- Window: declared baseline = all 7 LV games (wks [1, 2, 3, 4, 5, 6, 7]); L3 = player's last 3 ACTIVE games, wks [5, 6, 7] (inactive weeks excluded, not counted as zeros). Missed/absent: [1, 2] (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 83%, L3 84% (per wk 3:79%, 4:82%, 5:70%, 6:98%, 7:84%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: Active — Bowers (calf) was a full practice participant Thursday. [ESPN injuries API 7:30 PM ET]
- Alignment/routes (ESPN WR/CB sheet, season-to-date): align tag S, LWR/slot/RWR 21%/57%/21%; routes 168; targets/route 28%; YPRR 0.54. Route participation per dropback: GAP (no free per-game routes; nflverse 2026 participation 404).
- Opportunity: targets 51 (L3 27); target share (player tgt / team receiver tgt) season 20.1%, L3 22.9% — share of pass attempts is not used. Receptions 34 (L3 18). aDOT 10.2; RZ tgt 7; 3rd-down tgt 21 (30% of team 3rd-down tgt); 2-min (≤120s left in half) tgt 6 [pbp].
- Conversion/efficiency/explosive: catch rate 66.7%; YPT 8.92; YAC/rec 4.1; 20+ yd catches 6; NGS: sep 2.34, cushion 5.74, YAC 4.33 vs exp 3.60, share of team intended air yds 25.7% [pbp, NGS].
- Archetype (supported by numbers above): primary target + red-zone option. Trend: L3 share 22.9% vs season 20.1% → stable/up.
- Scheme: Sharp (Updated Oct 27; page modified 2026-10-29 15:53 ET) man 23.8/zone 66.6/MOFC 45.2/MOFO 50.0 (man rank #8 of 32). StatRankings (thru Oct 30, upd 10/31): man 37.5% rank 12, zone 62.5% — rank order AGREES (within 5 spots)
- PFR: **PFR cache Oct 29 (fresh pull 403)**.
- 8A status: PENDING (Rico ruling on TE/slot→LB/S mapping). Candidate defenders (PFR cache Oct 29, fresh pull 403): Jamien Sherwood (LB, NYJ, G5): 18-15-163, cmp 83.3%, YPT 9.1, rat 122.9 | Demario Davis (LB, NYJ, G5): 18-12-133, cmp 66.7%, YPT 7.4, rat 88.4 | Dane Belton (S, NYJ, G5): 13-7-78, cmp 53.8%, YPT 6.0, rat 72.0
- QB (LV; primary K.Cousins): 279 dropbacks, 263 att, cmp 63.9%, YPA 7.37, EPA/db +0.127, sacks 10 (3.6%), scrambles 6 [pbp]. vs blitz (FTN n_blitzers>0, n=80): sack 0.0%, yds/db 6.45; no blitz (n=199): sack 5.0%, yds/db 6.96. NGS: Kirk Cousins TTT 2.89s, CPOE +2.7, intended air 8.5. OL now: LT Kolton Miller, LG Spencer Burford, C Tyler Linderbaum, RG Caleb Rogers, RT DJ Glaze; OL injuries: DJ Glaze OT Active; Jackson Powers-Johnson G Questionable; Bryce Cabeldue G Active [ESPN].
- Teammate injuries / redistribution: Carter Runyon (TE, Injured Reserve) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.
- Injury return: back since wk 3 (5 active games post-return).

### CeeDee Lamb (DAL vs ARI) — rec · rung None @ None
- **PHASE 3: PASS** — role, participation and opportunity verified
- Window: declared baseline = all 7 DAL games (wks [1, 2, 3, 4, 5, 6, 7]); L3 = player's last 3 ACTIVE games, wks [5, 6, 7] (inactive weeks excluded, not counted as zeros). Missed/absent: none (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 79%, L3 75% (per wk 1:81%, 2:75%, 3:82%, 4:86%, 5:57%, 6:88%, 7:81%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: Active — Lamb brought in five of 12 targets for 74 yards and two touchdowns in the Cowboys' 38-21 win over the Eagles on Monday n [ESPN injuries API 7:30 PM ET]
- Alignment/routes (ESPN WR/CB sheet, season-to-date): align tag R, LWR/slot/RWR 28%/38%/34%; routes 237; targets/route 33%; YPRR 0.63. Route participation per dropback: GAP (no free per-game routes; nflverse 2026 participation 404).
- Opportunity: targets 81 (L3 35); target share (player tgt / team receiver tgt) season 30.5%, L3 28.7% — share of pass attempts is not used. Receptions 53 (L3 16). aDOT 10.6; RZ tgt 14; 3rd-down tgt 22 (35% of team 3rd-down tgt); 2-min (≤120s left in half) tgt 15 [pbp].
- Conversion/efficiency/explosive: catch rate 65.4%; YPT 8.04; YAC/rec 3.5; 20+ yd catches 8; NGS: sep 2.86, cushion 6.49, YAC 3.58 vs exp 3.39, share of team intended air yds 40.8% [pbp, NGS].
- Archetype (supported by numbers above): primary target + red-zone option. Trend: L3 share 28.7% vs season 30.5% → stable/up.
- Scheme: Sharp (Updated Oct 27; page modified 2026-10-29 15:53 ET) man 9.1/zone 70.9/MOFC 21.9/MOFO 56.7 (man rank #30 of 32). StatRankings (thru Oct 30, upd 10/31): man not in top-25 list (bottom 7) % rank 26-32, zone 74.3% — both put it in the low-man group
- PFR: **PFR cache Oct 29 (fresh pull 403)**.
- 8A status: PENDING_FILM; film route/alignment read counts only if every cited play matches pbp, otherwise UNVERIFIED → GAP (disclosed).
- QB (DAL; primary D.Prescott): 293 dropbacks, 273 att, cmp 65.2%, YPA 6.78, EPA/db +0.154, sacks 7 (2.4%), scrambles 13 [pbp]. vs blitz (FTN n_blitzers>0, n=96): sack 2.1%, yds/db 5.26; no blitz (n=197): sack 2.5%, yds/db 7.04. NGS: Dak Prescott TTT 2.78s, CPOE +1.2, intended air 8.2. OL now: LT Tyler Guyton, LG Tyler Smith, C Cooper Beebe, RG Tyler Booker, RT Terence Steele; OL injuries: Drew Shelton OT Active; Broderick Jones OT Active; Tyler Guyton OT Active [ESPN].
- Teammate injuries / redistribution: KaVontae Turpin (WR, Out); George Pickens (WR, Questionable); Luke Schoonmaker (TE, Questionable) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.

### DK Metcalf (PIT vs CLE) — recyds · rung 40 @ -225
- **PHASE 3: PASS** — role, participation and opportunity verified
- Window: declared baseline = all 7 PIT games (wks [1, 2, 3, 4, 5, 6, 7]); L3 = player's last 3 ACTIVE games, wks [5, 6, 7] (inactive weeks excluded, not counted as zeros). Missed/absent: none (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 95%, L3 93% (per wk 1:96%, 2:97%, 3:95%, 4:97%, 5:92%, 6:95%, 7:92%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: Active — Metcalf two of six targets for 56 yards in Sunday's 16-10 win over the Saints. [ESPN injuries API 7:30 PM ET]
- Alignment/routes (ESPN WR/CB sheet, season-to-date): align tag L, LWR/slot/RWR 47%/21%/32%; routes 280; targets/route 20%; YPRR 0.28. Route participation per dropback: GAP (no free per-game routes; nflverse 2026 participation 404).
- Opportunity: targets 58 (L3 25); target share (player tgt / team receiver tgt) season 23.6%, L3 24.5% — share of pass attempts is not used. Receptions 32 (L3 16). aDOT 12.7; RZ tgt 4; 3rd-down tgt 19 (33% of team 3rd-down tgt); 2-min (≤120s left in half) tgt 5 [pbp].
- Conversion/efficiency/explosive: catch rate 55.2%; YPT 6.45; YAC/rec 3.2; 20+ yd catches 4; NGS: sep 2.48, cushion 4.41, YAC 3.90 vs exp 3.58, share of team intended air yds 39.8% [pbp, NGS].
- Archetype (supported by numbers above): explosive/deep. Trend: L3 share 24.5% vs season 23.6% → stable/up.
- Scheme: Sharp (Updated Oct 27; page modified 2026-10-29 15:53 ET) man 42.4/zone 54.0/MOFC 72.6/MOFO 24.4 (man rank #1 of 32). StatRankings (thru Oct 30, upd 10/31): man 55.8% rank 1, zone n/a% — rank order AGREES (within 5 spots)
- PFR: **PFR cache Oct 29 (fresh pull 403)**.
- 8A status: PENDING_FILM; film route/alignment read counts only if every cited play matches pbp, otherwise UNVERIFIED → GAP (disclosed).
- QB (PIT; primary A.Rodgers): 289 dropbacks, 262 att, cmp 61.8%, YPA 6.48, EPA/db -0.104, sacks 22 (7.6%), scrambles 5 [pbp]. vs blitz (FTN n_blitzers>0, n=88): sack 12.5%, yds/db 3.82; no blitz (n=201): sack 5.5%, yds/db 6.07. NGS: Aaron Rodgers TTT 2.74s, CPOE -1.3, intended air 7.0. OL now: LT Troy Fautanu, LG Mason McCormick, C Zach Frazier, RG Brock Hoffman, RT Max Iheanachor; OL injuries: none listed [ESPN].
- Teammate injuries / redistribution: Ben Skowronek (WR, Questionable) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.

### Dallas Goedert (PHI vs WAS) — rec · rung None @ None
- **PHASE 3: PASS (8A PENDING)** — role, participation and opportunity verified
- Window: declared baseline = all 7 PHI games (wks [1, 2, 3, 4, 5, 6, 7]); L3 = player's last 3 ACTIVE games, wks [5, 6, 7] (inactive weeks excluded, not counted as zeros). Missed/absent: [3, 4] (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 69%, L3 74% (per wk 1:95%, 2:25%, 5:69%, 6:81%, 7:73%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: not on ESPN injury report [ESPN injuries API 7:30 PM ET]
- Alignment/routes: GAP (not on ESPN WR/CB sheet; TE sheet 404). PENDING_FILM.
- Opportunity: targets 31 (L3 24); target share (player tgt / team receiver tgt) season 14.1%, L3 21.1% — share of pass attempts is not used. Receptions 22 (L3 17). aDOT 5.5; RZ tgt 3; 3rd-down tgt 10 (14% of team 3rd-down tgt); 2-min (≤120s left in half) tgt 3 [pbp].
- Conversion/efficiency/explosive: catch rate 71.0%; YPT 7.35; YAC/rec 4.2; 20+ yd catches 1; NGS: sep 2.85, cushion 4.98, YAC 4.34 vs exp 3.73, share of team intended air yds 10.7% [pbp, NGS].
- Archetype (supported by numbers above): secondary target. Trend: L3 share 21.1% vs season 14.1% → stable/up.
- Scheme: Sharp (Updated Oct 27; page modified 2026-10-29 15:53 ET) man 12.9/zone 76.9/MOFC 29.6/MOFO 62.8 (man rank #25 of 32). StatRankings (thru Oct 30, upd 10/31): man not in top-25 list (bottom 7) % rank 26-32, zone 81.7%
- PFR: **PFR cache Oct 29 (fresh pull 403)**.
- 8A status: PENDING (Rico ruling on TE/slot→LB/S mapping). Candidate defenders (PFR cache Oct 29, fresh pull 403): Frankie Luvu (LB, WAS, G3): 6-4-17, cmp 66.7%, YPT 2.8, rat 70.1 | Sonny Styles (LB, WAS, G5): 13-6-84, cmp 46.2%, YPT 6.5, rat 35.4 | Nick Cross (S, WAS, G2): 6-5-57, cmp 83.3%, YPT 9.5, rat 145.8
- QB (PHI; primary J.Hurts): 266 dropbacks, 235 att, cmp 58.7%, YPA 5.78, EPA/db -0.103, sacks 18 (6.8%), scrambles 13 [pbp]. vs blitz (FTN n_blitzers>0, n=96): sack 8.3%, yds/db 3.99; no blitz (n=170): sack 5.9%, yds/db 5.63. NGS: Jalen Hurts TTT 3.04s, CPOE -2.4, intended air 7.9. OL now: LT Jordan Mailata, LG Landon Dickerson, C Drew Kendall, RG Tyler Steen, RT Markel Bell; OL injuries: Jake Majors C Active [ESPN].
- Teammate injuries / redistribution: Britain Covey (WR, Out); Dontayvion Wicks (WR, Out); DeVonta Smith (WR, Out); Dameon Pierce (RB, Injured Reserve) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.
- Injury return: back since wk 5 (3 active games post-return).
- Partial games (snap <40%, treated as in-game exit, not role change): wks [2].

### Drake London (ATL vs TB) — recyds · rung 60 @ -270
- **PHASE 3: PASS** — role, participation and opportunity verified
- Window: declared baseline = all 7 ATL games (wks [1, 2, 3, 4, 5, 6, 7]); L3 = player's last 3 ACTIVE games, wks [5, 6, 7] (inactive weeks excluded, not counted as zeros). Missed/absent: none (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 89%, L3 93% (per wk 1:98%, 2:62%, 3:93%, 4:89%, 5:98%, 6:100%, 7:81%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: not on ESPN injury report [ESPN injuries API 7:30 PM ET]
- Alignment/routes (ESPN WR/CB sheet, season-to-date): align tag L, LWR/slot/RWR 37%/38%/25%; routes 193; targets/route 27%; YPRR 0.51. Route participation per dropback: GAP (no free per-game routes; nflverse 2026 participation 404).
- Opportunity: targets 56 (L3 31); target share (player tgt / team receiver tgt) season 29.2%, L3 31.3% — share of pass attempts is not used. Receptions 38 (L3 18). aDOT 9.9; RZ tgt 4; 3rd-down tgt 21 (38% of team 3rd-down tgt); 2-min (≤120s left in half) tgt 3 [pbp].
- Conversion/efficiency/explosive: catch rate 67.9%; YPT 11.00; YAC/rec 7.3; 20+ yd catches 10; NGS: sep 3.16, cushion 6.80, YAC 7.61 vs exp 5.96, share of team intended air yds 43.2% [pbp, NGS].
- Archetype (supported by numbers above): volume/possession. Trend: L3 share 31.3% vs season 29.2% → stable/up.
- Scheme: Sharp (Updated Oct 27; page modified 2026-10-29 15:53 ET) man 17.2/zone 78.0/MOFC 58.6/MOFO 39.6 (man rank #17 of 32). StatRankings (thru Oct 30, upd 10/31): man 32.3% rank 20, zone 66.9% — rank order AGREES (within 5 spots)
- PFR: **PFR cache Oct 29 (fresh pull 403)**.
- 8A status: PENDING_FILM; film route/alignment read counts only if every cited play matches pbp, otherwise UNVERIFIED → GAP (disclosed).
- QB (ATL; primary M.Penix): 224 dropbacks, 200 att, cmp 64.0%, YPA 7.39, EPA/db -0.101, sacks 16 (7.1%), scrambles 8 [pbp]. vs blitz (FTN n_blitzers>0, n=90): sack 7.8%, yds/db 6.71; no blitz (n=134): sack 6.7%, yds/db 6.16. NGS: Michael Penix Jr. TTT 2.53s, CPOE +0.1, intended air 7.3. OL now: LT Jake Matthews, LG Matthew Bergeron, C Ryan Neuzil, RG Chris Lindstrom, RT Jawaan Taylor; OL injuries: Jawaan Taylor OT Active [ESPN].
- Teammate injuries / redistribution: Beaux Collins (WR, Injured Reserve); Olamide Zaccheaus (WR, Questionable); Brian Robinson Jr. (RB, Out) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.

### Garrett Wilson (NYJ vs LV) — recyds · rung None @ None
- **PHASE 3: PASS** — role, participation and opportunity verified
- Window: declared baseline = all 7 NYJ games (wks [1, 2, 3, 4, 5, 6, 7]); L3 = player's last 3 ACTIVE games, wks [5, 6, 7] (inactive weeks excluded, not counted as zeros). Missed/absent: none (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 90%, L3 92% (per wk 1:75%, 2:88%, 3:94%, 4:100%, 5:93%, 6:98%, 7:85%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: Active — Wilson said Wednesday that he won't ask to be traded from the Jets, Zack Rosenblatt of The Athletic reports. [ESPN injuries API 7:30 PM ET]
- Alignment/routes (ESPN WR/CB sheet, season-to-date): align tag R, LWR/slot/RWR 42%/22%/36%; routes 221; targets/route 22%; YPRR 0.44. Route participation per dropback: GAP (no free per-game routes; nflverse 2026 participation 404).
- Opportunity: targets 51 (L3 20); target share (player tgt / team receiver tgt) season 25.9%, L3 23.0% — share of pass attempts is not used. Receptions 37 (L3 13). aDOT 9.6; RZ tgt 3; 3rd-down tgt 17 (33% of team 3rd-down tgt); 2-min (≤120s left in half) tgt 4 [pbp].
- Conversion/efficiency/explosive: catch rate 72.5%; YPT 8.71; YAC/rec 3.0; 20+ yd catches 6; NGS: sep 2.65, cushion 4.02, YAC 3.11 vs exp 2.84, share of team intended air yds 35.0% [pbp, NGS].
- Archetype (supported by numbers above): volume/possession. Trend: L3 share 23.0% vs season 25.9% → stable/up.
- Scheme: Sharp (Updated Oct 27; page modified 2026-10-29 15:53 ET) man 21.4/zone 70.0/MOFC 47.2/MOFO 47.2 (man rank #11 of 32). StatRankings (thru Oct 30, upd 10/31): man 34.3% rank 16, zone 65.7% — rank order AGREES (within 5 spots)
- PFR: **PFR cache Oct 29 (fresh pull 403)**.
- 8A status: PENDING_FILM; film route/alignment read counts only if every cited play matches pbp, otherwise UNVERIFIED → GAP (disclosed).
- QB (NYJ; primary G.Smith): 237 dropbacks, 206 att, cmp 70.4%, YPA 7.88, EPA/db +0.100, sacks 21 (8.9%), scrambles 10 [pbp]. vs blitz (FTN n_blitzers>0, n=63): sack 14.3%, yds/db 7.27; no blitz (n=174): sack 6.9%, yds/db 5.94. NGS: Geno Smith TTT 2.92s, CPOE +6.4, intended air 7.0. OL now: LT Olu Fashanu, LG Dylan Parham, C Josh Myers, RG Joe Tippmann, RT Armand Membou; OL injuries: Max Mitchell OT Out; Dylan Parham G Questionable [ESPN].
- Teammate injuries / redistribution: Breece Hall (RB, Questionable) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.

### Jahmyr Gibbs (DET vs MIN) — rushyds · rung 70 @ -250
- **PHASE 3: PASS** — role, participation and opportunity verified
- Window: declared baseline = all 6 DET games (wks [1, 2, 3, 4, 5, 7]); L3 = player's last 3 ACTIVE games, wks [4, 5, 7] (inactive weeks excluded, not counted as zeros). Missed/absent: none (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 79%, L3 82% (per wk 1:74%, 2:83%, 3:69%, 4:87%, 5:70%, 7:90%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: Active — Gibbs (shoulder) practiced fully Thursday. [ESPN injuries API 7:30 PM ET]
- Opportunity: carries 134 (L3 69); RB carry share season 89.3%, L3 90.8%; GL carries (≤5) 13; targets 40, catches 32; receiving routes GAP [pbp].
- Efficiency/explosive: YPC 4.63; success 50.0%; ≤0 yds 20.9%; 15+ runs 10; NGS: RYOE/att +0.56, 8+ box 18.7%, time to LOS 2.90s [pbp, NGS].
- Run direction/gap (carry direction, not concept): {'right': np.int64(51), 'middle': np.int64(44), 'left': np.int64(39)} / {'tackle': np.int64(50), 'end': np.int64(21), 'guard': np.int64(19)}. Concept: GAP.
- Archetype: early-down + goal-line + receiving RB. Trend: L3 carry share 90.8% vs 89.3% → stable/up.
- QB (DET; primary J.Goff): 240 dropbacks, 223 att, cmp 67.3%, YPA 8.02, EPA/db +0.282, sacks 12 (5.0%), scrambles 5 [pbp]. vs blitz (FTN n_blitzers>0, n=78): sack 6.4%, yds/db 7.42; no blitz (n=162): sack 4.3%, yds/db 6.99. NGS: Jared Goff TTT 2.84s, CPOE +1.7, intended air 8.4. OL now: LT Penei Sewell, LG Christian Mahogany, C Cade Mays, RG Tate Ratledge, RT Blake Miller; OL injuries: Seth McLaughlin C Active; Cade Mays C Active; Ben Bartch G Injured Reserve [ESPN].
- Teammate injuries / redistribution: Isiah Pacheco (RB, Injured Reserve) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.

### James Cook (BUF vs BAL) — rushyds · rung None @ None
- **PHASE 3: PASS** — role, participation and opportunity verified
- Window: declared baseline = all 6 BUF games (wks [1, 2, 3, 4, 5, 6]); L3 = player's last 3 ACTIVE games, wks [4, 5, 6] (inactive weeks excluded, not counted as zeros). Missed/absent: none (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 67%, L3 62% (per wk 1:72%, 2:74%, 3:67%, 4:59%, 5:62%, 6:66%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: not on ESPN injury report [ESPN injuries API 7:30 PM ET]
- Opportunity: carries 117 (L3 59); RB carry share season 93.6%, L3 90.8%; GL carries (≤5) 8; targets 14, catches 10; receiving routes GAP [pbp].
- Efficiency/explosive: YPC 5.36; success 50.4%; ≤0 yds 11.1%; 15+ runs 11; NGS: RYOE/att +0.93, 8+ box 23.1%, time to LOS 2.53s [pbp, NGS].
- Run direction/gap (carry direction, not concept): {'middle': np.int64(40), 'left': np.int64(39), 'right': np.int64(38)} / {'guard': np.int64(38), 'tackle': np.int64(30), 'end': np.int64(9)}. Concept: GAP.
- Archetype: early-down + goal-line RB. Trend: L3 carry share 90.8% vs 93.6% → stable/up.
- QB (BUF; primary J.Allen): 200 dropbacks, 171 att, cmp 66.7%, YPA 8.80, EPA/db +0.340, sacks 12 (6.0%), scrambles 17 [pbp]. vs blitz (FTN n_blitzers>0, n=66): sack 9.1%, yds/db 8.17; no blitz (n=134): sack 4.5%, yds/db 8.10. NGS: Josh Allen TTT 2.97s, CPOE +2.4, intended air 8.7. OL now: LT Dion Dawkins, LG Alec Anderson, C Connor McGovern, RG O'Cyrus Torrence, RT Spencer Brown; OL injuries: Spencer Brown OT Questionable; Jude Bowry OT Active; Ar'maj Reed-Adams G Active [ESPN].
- Teammate injuries / redistribution: Dalton Kincaid (TE, Questionable); DJ Moore (WR, Questionable); Tyrell Shavers (WR, Out) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.

### Javonte Williams (DAL vs ARI) — rushyds · rung None @ None
- **PHASE 3: PASS** — role, participation and opportunity verified
- Window: declared baseline = all 7 DAL games (wks [1, 2, 3, 4, 5, 6, 7]); L3 = player's last 3 ACTIVE games, wks [5, 6, 7] (inactive weeks excluded, not counted as zeros). Missed/absent: none (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 75%, L3 74% (per wk 1:71%, 2:80%, 3:76%, 4:74%, 5:85%, 6:73%, 7:65%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: Active — Williams rushed 25 times for 155 yards and a touchdown in the Cowboys' 38-21 win over the Eagles on Monday night. [ESPN injuries API 7:30 PM ET]
- Opportunity: carries 110 (L3 48); RB carry share season 78.6%, L3 77.4%; GL carries (≤5) 17; targets 22, catches 19; receiving routes GAP [pbp].
- Efficiency/explosive: YPC 4.29; success 47.3%; ≤0 yds 15.5%; 15+ runs 6; NGS: RYOE/att +0.38, 8+ box 18.2%, time to LOS 2.78s [pbp, NGS].
- Run direction/gap (carry direction, not concept): {'left': np.int64(41), 'middle': np.int64(37), 'right': np.int64(32)} / {'tackle': np.int64(34), 'guard': np.int64(31), 'end': np.int64(8)}. Concept: GAP.
- Archetype: early-down + goal-line + receiving RB. Trend: L3 carry share 77.4% vs 78.6% → stable/up.
- QB (DAL; primary D.Prescott): 293 dropbacks, 273 att, cmp 65.2%, YPA 6.78, EPA/db +0.154, sacks 7 (2.4%), scrambles 13 [pbp]. vs blitz (FTN n_blitzers>0, n=96): sack 2.1%, yds/db 5.26; no blitz (n=197): sack 2.5%, yds/db 7.04. NGS: Dak Prescott TTT 2.78s, CPOE +1.2, intended air 8.2. OL now: LT Tyler Guyton, LG Tyler Smith, C Cooper Beebe, RG Tyler Booker, RT Terence Steele; OL injuries: Drew Shelton OT Active; Broderick Jones OT Active; Tyler Guyton OT Active [ESPN].
- Teammate injuries / redistribution: KaVontae Turpin (WR, Out); George Pickens (WR, Questionable); Luke Schoonmaker (TE, Questionable) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.

### Jonathan Taylor (IND vs JAX) — rushyds · rung None @ None
- **PHASE 3: PASS** — role, participation and opportunity verified
- Window: declared baseline = all 7 IND games (wks [1, 2, 3, 4, 5, 6, 7]); L3 = player's last 3 ACTIVE games, wks [5, 6, 7] (inactive weeks excluded, not counted as zeros). Missed/absent: none (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 80%, L3 73% (per wk 1:89%, 2:94%, 3:85%, 4:71%, 5:73%, 6:78%, 7:67%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: Active — Taylor is being made available via trade by the Colts, Adam Schefter of ESPN  reports. [ESPN injuries API 7:30 PM ET]
- Opportunity: carries 140 (L3 54); RB carry share season 81.4%, L3 73.0%; GL carries (≤5) 13; targets 26, catches 17; receiving routes GAP [pbp].
- Efficiency/explosive: YPC 4.19; success 40.0%; ≤0 yds 17.9%; 15+ runs 6; NGS: RYOE/att -0.00, 8+ box 18.6%, time to LOS 2.74s [pbp, NGS].
- Run direction/gap (carry direction, not concept): {'right': np.int64(63), 'left': np.int64(55), 'middle': np.int64(21)} / {'tackle': np.int64(52), 'end': np.int64(33), 'guard': np.int64(33)}. Concept: GAP.
- Archetype: early-down + goal-line + receiving RB. Trend: L3 carry share 73.0% vs 81.4% → stable/up.
- QB (IND; primary D.Jones): 266 dropbacks, 239 att, cmp 59.8%, YPA 5.85, EPA/db -0.158, sacks 19 (7.1%), scrambles 8 [pbp]. vs blitz (FTN n_blitzers>0, n=95): sack 12.6%, yds/db 3.75; no blitz (n=171): sack 4.1%, yds/db 5.58. NGS: Daniel Jones TTT 2.82s, CPOE -2.1, intended air 7.7. OL now: LT Bernhard Raimann, LG Jalen Farmer, C Tanor Bortolini, RG Matt Goncalves, RT Jalen Travis; OL injuries: Matt Goncalves G Active; Dalton Tucker G Active [ESPN].
- Teammate injuries / redistribution: Anthony Gould (WR, Out); Drew Ogletree (TE, Questionable); Alec Pierce (WR, Injured Reserve) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.

### Justin Jefferson (MIN vs DET) — recyds · rung None @ None
- **PHASE 3: PASS** — role, participation and opportunity verified
- Window: declared baseline = all 6 MIN games (wks [1, 2, 3, 4, 5, 7]); L3 = player's last 3 ACTIVE games, wks [3, 5, 7] (inactive weeks excluded, not counted as zeros). Missed/absent: [4] (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 77%, L3 65% (per wk 1:92%, 2:100%, 3:12%, 5:89%, 7:93%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: Active —  [ESPN injuries API 7:30 PM ET]
- Alignment/routes (ESPN WR/CB sheet, season-to-date): align tag L, LWR/slot/RWR 43%/18%/39%; routes 121; targets/route 25%; YPRR 0.59. Route participation per dropback: GAP (no free per-game routes; nflverse 2026 participation 404).
- Opportunity: targets 31 (L3 16); target share (player tgt / team receiver tgt) season 20.3%, L3 20.5% — share of pass attempts is not used. Receptions 23 (L3 12). aDOT 10.9; RZ tgt 5; 3rd-down tgt 16 (27% of team 3rd-down tgt); 2-min (≤120s left in half) tgt 3 [pbp].
- Conversion/efficiency/explosive: catch rate 74.2%; YPT 9.74; YAC/rec 3.4; 20+ yd catches 5; NGS: sep 2.81, cushion 5.57, YAC 3.55 vs exp 2.48, share of team intended air yds 31.2% [pbp, NGS].
- Archetype (supported by numbers above): primary target. Trend: L3 share 20.5% vs season 20.3% → stable/up.
- Scheme: Sharp (Updated Oct 27; page modified 2026-10-29 15:53 ET) man 18.2/zone 76.4/MOFC 47.6/MOFO 49.0 (man rank #14 of 32). StatRankings (thru Oct 30, upd 10/31): man 37.6% rank 11, zone 61.7% — rank order AGREES (within 5 spots)
- PFR: **PFR cache Oct 29 (fresh pull 403)**.
- 8A status: PENDING_FILM; film route/alignment read counts only if every cited play matches pbp, otherwise UNVERIFIED → GAP (disclosed).
- QB (MIN; primary K.Murray): 198 dropbacks, 163 att, cmp 65.0%, YPA 6.67, EPA/db -0.022, sacks 18 (9.1%), scrambles 17 [pbp]. vs blitz (FTN n_blitzers>0, n=72): sack 6.9%, yds/db 5.06; no blitz (n=126): sack 10.3%, yds/db 5.95. NGS: Kyler Murray TTT 2.91s, CPOE +0.7, intended air 7.2. OL now: LT Christian Darrisaw, LG Joe Huber, C Blake Brandel, RG Will Fries, RT Brian O'Neill; OL injuries: Brian O'Neill OT Active; Joe Huber G Active; Caleb Tiernan OT Active; Christian Darrisaw OT Active; Michael Jurgens C Active [ESPN].
- Teammate injuries / redistribution: none (skill) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.
- Injury return: back since wk 5 (2 active games post-return).
- Partial games (snap <40%, treated as in-game exit, not role change): wks [3].

### Kenneth Walker III (KC vs DEN) — rushyds · rung None @ None
- **PHASE 3: PASS** — role, participation and opportunity verified
- Window: declared baseline = all 6 KC games (wks [1, 2, 3, 4, 6, 7]); L3 = player's last 3 ACTIVE games, wks [4, 6, 7] (inactive weeks excluded, not counted as zeros). Missed/absent: none (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 74%, L3 74% (per wk 1:68%, 2:82%, 3:73%, 4:75%, 6:74%, 7:74%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: Active — Walker rushed 14 times for 36 yards while catching four of five targets for 21 yards in Sunday's 20-3 loss to the Seahaw [ESPN injuries API 7:30 PM ET]
- Opportunity: carries 120 (L3 55); RB carry share season 86.3%, L3 94.8%; GL carries (≤5) 11; targets 27, catches 18; receiving routes GAP [pbp].
- Efficiency/explosive: YPC 5.84; success 45.0%; ≤0 yds 16.7%; 15+ runs 10; NGS: RYOE/att +2.26, 8+ box 25.0%, time to LOS 2.80s [pbp, NGS].
- Run direction/gap (carry direction, not concept): {'left': np.int64(44), 'middle': np.int64(44), 'right': np.int64(31)} / {'guard': np.int64(30), 'end': np.int64(25), 'tackle': np.int64(20)}. Concept: GAP.
- Archetype: early-down + goal-line + receiving RB. Trend: L3 carry share 94.8% vs 86.3% → stable/up.
- QB (KC; primary P.Mahomes): 210 dropbacks, 191 att, cmp 64.9%, YPA 7.72, EPA/db +0.135, sacks 7 (3.3%), scrambles 12 [pbp]. vs blitz (FTN n_blitzers>0, n=57): sack 3.5%, yds/db 7.96; no blitz (n=153): sack 3.3%, yds/db 6.86. NGS: Patrick Mahomes TTT 2.79s, CPOE -2.1, intended air 6.2. OL now: LT Kahlil Benson, LG Kingsley Suamataia, C Creed Humphrey, RG Trey Smith, RT Jaylon Moore; OL injuries: Jaylon Moore OT Active [ESPN].
- Teammate injuries / redistribution: Brashard Smith (RB, Injured Reserve) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.

### Parker Washington (JAX vs IND) — recyds · rung None @ None
- **PHASE 3: PASS** — role, participation and opportunity verified
- Window: declared baseline = all 6 JAX games (wks [1, 2, 3, 4, 5, 6]); L3 = player's last 3 ACTIVE games, wks [4, 5, 6] (inactive weeks excluded, not counted as zeros). Missed/absent: none (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 76%, L3 78% (per wk 1:61%, 2:81%, 3:81%, 4:80%, 5:82%, 6:73%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: Active — Washington caught four of 11 targets for 64 yards in Sunday's 34-31 loss to the Texans. [ESPN injuries API 7:30 PM ET]
- Alignment/routes (ESPN WR/CB sheet, season-to-date): align tag S, LWR/slot/RWR 30%/46%/24%; routes 170; targets/route 26%; YPRR 0.54. Route participation per dropback: GAP (no free per-game routes; nflverse 2026 participation 404).
- Opportunity: targets 46 (L3 23); target share (player tgt / team receiver tgt) season 25.8%, L3 22.5% — share of pass attempts is not used. Receptions 26 (L3 11). aDOT 13.0; RZ tgt 8; 3rd-down tgt 15 (35% of team 3rd-down tgt); 2-min (≤120s left in half) tgt 6 [pbp].
- Conversion/efficiency/explosive: catch rate 56.5%; YPT 9.04; YAC/rec 4.8; 20+ yd catches 6; NGS: sep 2.11, cushion 6.70, YAC 5.15 vs exp 3.94, share of team intended air yds 37.7% [pbp, NGS].
- Archetype (supported by numbers above): explosive/deep + red-zone option. Trend: L3 share 22.5% vs season 25.8% → stable/up.
- Scheme: Sharp (Updated Oct 27; page modified 2026-10-29 15:53 ET) man 26.2/zone 66.5/MOFC 50.2/MOFO 44.7 (man rank #5 of 32). StatRankings (thru Oct 30, upd 10/31): man 49.6% rank 3, zone n/a% — rank order AGREES (within 5 spots)
- PFR: **PFR cache Oct 29 (fresh pull 403)**.
- 8A status: PENDING_FILM; film route/alignment read counts only if every cited play matches pbp, otherwise UNVERIFIED → GAP (disclosed).
- QB (JAX; primary T.Lawrence): 200 dropbacks, 183 att, cmp 65.6%, YPA 8.09, EPA/db +0.275, sacks 10 (5.0%), scrambles 7 [pbp]. vs blitz (FTN n_blitzers>0, n=64): sack 4.7%, yds/db 6.09; no blitz (n=136): sack 5.1%, yds/db 7.82. NGS: Trevor Lawrence TTT 2.72s, CPOE +3.6, intended air 8.7. OL now: LT Walker Little, LG Emmanuel Pregnon, C Robert Hainsey, RG Ezra Cleveland, RT Cole Van Lanen; OL injuries: Anton Harrison OT Injured Reserve [ESPN].
- Teammate injuries / redistribution: Jakobi Meyers (WR, Questionable) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.

### Puka Nacua (LA vs LAC) — rec · rung None @ None
- **PHASE 3: PASS** — role, participation and opportunity verified
- Window: declared baseline = all 7 LA games (wks [1, 2, 3, 4, 5, 6, 7]); L3 = player's last 3 ACTIVE games, wks [5, 6, 7] (inactive weeks excluded, not counted as zeros). Missed/absent: [2, 3] (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 84%, L3 87% (per wk 1:70%, 4:90%, 5:85%, 6:90%, 7:85%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: Active — Nacua brought in eight of 10 targets for 68 yards and a touchdown and rushed twice for 10 yards in the Rams' 35-21 win o [ESPN injuries API 7:30 PM ET]
- Alignment/routes (ESPN WR/CB sheet, season-to-date): align tag R, LWR/slot/RWR 24%/24%/52%; routes 169; targets/route 35%; YPRR 0.59. Route participation per dropback: GAP (no free per-game routes; nflverse 2026 participation 404).
- Opportunity: targets 62 (L3 41); target share (player tgt / team receiver tgt) season 22.9%, L3 35.7% — share of pass attempts is not used. Receptions 45 (L3 31). aDOT 8.9; RZ tgt 7; 3rd-down tgt 17 (30% of team 3rd-down tgt); 2-min (≤120s left in half) tgt 6 [pbp].
- Conversion/efficiency/explosive: catch rate 72.6%; YPT 7.82; YAC/rec 5.7; 20+ yd catches 6; NGS: sep 2.90, cushion 6.39, YAC 5.75 vs exp 3.81, share of team intended air yds 25.5% [pbp, NGS].
- Archetype (supported by numbers above): primary target + red-zone option. Trend: L3 share 35.7% vs season 22.9% → stable/up.
- Scheme: Sharp (Updated Oct 27; page modified 2026-10-29 15:53 ET) man 10.6/zone 58.0/MOFC 33.9/MOFO 40.7 (man rank #29 of 32). StatRankings (thru Oct 30, upd 10/31): man 34.6% rank 15, zone 65.4% — rank order DIFFERS (Sharp #29 vs SR #15)
- PFR: **PFR cache Oct 29 (fresh pull 403)**.
- 8A status: PENDING_FILM; film route/alignment read counts only if every cited play matches pbp, otherwise UNVERIFIED → GAP (disclosed).
- QB (LA; primary M.Stafford): 294 dropbacks, 278 att, cmp 68.0%, YPA 7.20, EPA/db +0.099, sacks 11 (3.7%), scrambles 5 [pbp]. vs blitz (FTN n_blitzers>0, n=89): sack 5.6%, yds/db 6.13; no blitz (n=205): sack 2.9%, yds/db 6.85. NGS: NGS GAP. OL now: LT Alaric Jackson, LG Steve Avila, C Coleman Shelton, RG Kevin Dotson, RT Warren McClendon Jr.; OL injuries: Coleman Shelton C Questionable; Bill Murray G Active; Keagen Trost OT Active [ESPN].
- Teammate injuries / redistribution: Jordan Whittington (WR, Questionable); Colby Parkinson (TE, Questionable); Terrance Ferguson (TE, Injured Reserve); Davante Adams (WR, Injured Reserve) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.
- Injury return: back since wk 4 (4 active games post-return).

### Puka Nacua (LA vs LAC) — recyds · rung 70 @ -290
- **PHASE 3: PASS** — role, participation and opportunity verified
- Window: declared baseline = all 7 LA games (wks [1, 2, 3, 4, 5, 6, 7]); L3 = player's last 3 ACTIVE games, wks [5, 6, 7] (inactive weeks excluded, not counted as zeros). Missed/absent: [2, 3] (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 84%, L3 87% (per wk 1:70%, 4:90%, 5:85%, 6:90%, 7:85%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: Active — Nacua brought in eight of 10 targets for 68 yards and a touchdown and rushed twice for 10 yards in the Rams' 35-21 win o [ESPN injuries API 7:30 PM ET]
- Alignment/routes (ESPN WR/CB sheet, season-to-date): align tag R, LWR/slot/RWR 24%/24%/52%; routes 169; targets/route 35%; YPRR 0.59. Route participation per dropback: GAP (no free per-game routes; nflverse 2026 participation 404).
- Opportunity: targets 62 (L3 41); target share (player tgt / team receiver tgt) season 22.9%, L3 35.7% — share of pass attempts is not used. Receptions 45 (L3 31). aDOT 8.9; RZ tgt 7; 3rd-down tgt 17 (30% of team 3rd-down tgt); 2-min (≤120s left in half) tgt 6 [pbp].
- Conversion/efficiency/explosive: catch rate 72.6%; YPT 7.82; YAC/rec 5.7; 20+ yd catches 6; NGS: sep 2.90, cushion 6.39, YAC 5.75 vs exp 3.81, share of team intended air yds 25.5% [pbp, NGS].
- Archetype (supported by numbers above): primary target + red-zone option. Trend: L3 share 35.7% vs season 22.9% → stable/up.
- Scheme: Sharp (Updated Oct 27; page modified 2026-10-29 15:53 ET) man 10.6/zone 58.0/MOFC 33.9/MOFO 40.7 (man rank #29 of 32). StatRankings (thru Oct 30, upd 10/31): man 34.6% rank 15, zone 65.4% — rank order DIFFERS (Sharp #29 vs SR #15)
- PFR: **PFR cache Oct 29 (fresh pull 403)**.
- 8A status: PENDING_FILM; film route/alignment read counts only if every cited play matches pbp, otherwise UNVERIFIED → GAP (disclosed).
- QB (LA; primary M.Stafford): 294 dropbacks, 278 att, cmp 68.0%, YPA 7.20, EPA/db +0.099, sacks 11 (3.7%), scrambles 5 [pbp]. vs blitz (FTN n_blitzers>0, n=89): sack 5.6%, yds/db 6.13; no blitz (n=205): sack 2.9%, yds/db 6.85. NGS: NGS GAP. OL now: LT Alaric Jackson, LG Steve Avila, C Coleman Shelton, RG Kevin Dotson, RT Warren McClendon Jr.; OL injuries: Coleman Shelton C Questionable; Bill Murray G Active; Keagen Trost OT Active [ESPN].
- Teammate injuries / redistribution: Jordan Whittington (WR, Questionable); Colby Parkinson (TE, Questionable); Terrance Ferguson (TE, Injured Reserve); Davante Adams (WR, Injured Reserve) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.
- Injury return: back since wk 4 (4 active games post-return).

### Tee Higgins (CIN vs TEN) — recyds · rung None @ None
- **PHASE 3: PASS** — role, participation and opportunity verified
- Window: declared baseline = all 6 CIN games (wks [1, 2, 3, 4, 5, 7]); L3 = player's last 3 ACTIVE games, wks [4, 5, 7] (inactive weeks excluded, not counted as zeros). Missed/absent: none (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 79%, L3 78% (per wk 1:72%, 2:72%, 3:93%, 4:79%, 5:69%, 7:87%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: Active — Higgins secured six of seven targets for 148 yards and a touchdown in the Bengals' 35-13 win over the Ravens on Sunday. [ESPN injuries API 7:30 PM ET]
- Alignment/routes (ESPN WR/CB sheet, season-to-date): align tag R, LWR/slot/RWR 43%/14%/43%; routes 195; targets/route 25%; YPRR 0.51. Route participation per dropback: GAP (no free per-game routes; nflverse 2026 participation 404).
- Opportunity: targets 50 (L3 27); target share (player tgt / team receiver tgt) season 23.4%, L3 24.1% — share of pass attempts is not used. Receptions 33 (L3 19). aDOT 14.2; RZ tgt 3; 3rd-down tgt 12 (23% of team 3rd-down tgt); 2-min (≤120s left in half) tgt 7 [pbp].
- Conversion/efficiency/explosive: catch rate 66.0%; YPT 11.42; YAC/rec 4.0; 20+ yd catches 8; NGS: sep 2.43, cushion 5.54, YAC 4.11 vs exp 2.79, share of team intended air yds 43.8% [pbp, NGS].
- Archetype (supported by numbers above): explosive/deep. Trend: L3 share 24.1% vs season 23.4% → stable/up.
- Scheme: Sharp (Updated Oct 27; page modified 2026-10-29 15:53 ET) man 16.5/zone 77.2/MOFC 45.6/MOFO 51.2 (man rank #19 of 32). StatRankings (thru Oct 30, upd 10/31): man 27.8% rank 24, zone 71.8% — rank order AGREES (within 5 spots)
- PFR: **PFR cache Oct 29 (fresh pull 403)**.
- 8A status: PENDING_FILM; film route/alignment read counts only if every cited play matches pbp, otherwise UNVERIFIED → GAP (disclosed).
- QB (CIN; primary J.Burrow): 236 dropbacks, 219 att, cmp 71.7%, YPA 7.55, EPA/db +0.207, sacks 10 (4.2%), scrambles 7 [pbp]. vs blitz (FTN n_blitzers>0, n=63): sack 6.3%, yds/db 6.25; no blitz (n=173): sack 3.5%, yds/db 7.13. NGS: Joe Burrow TTT 2.64s, CPOE +5.2, intended air 7.6. OL now: LT Orlando Brown Jr., LG Dylan Fairchild, C Ted Karras, RG Dalton Risner, RT Amarius Mims; OL injuries: Connor Lew C Active; Myles Hinton OT Active [ESPN].
- Teammate injuries / redistribution: Andrei Iosivas (WR, Injured Reserve); Erick All Jr. (TE, Injured Reserve) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.

### Trey McBride (ARI vs DAL) — rec · rung 7 @ -225
- **PHASE 3: PASS (8A PENDING)** — role, participation and opportunity verified
- Window: declared baseline = all 7 ARI games (wks [1, 2, 3, 4, 5, 6, 7]); L3 = player's last 3 ACTIVE games, wks [5, 6, 7] (inactive weeks excluded, not counted as zeros). Missed/absent: none (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 91%, L3 93% (per wk 1:80%, 2:88%, 3:91%, 4:97%, 5:90%, 6:97%, 7:93%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: Active — McBride caught 10 of 13 targets for 111 yards and a touchdown in Sunday's 30-16 loss to the Broncos. [ESPN injuries API 7:30 PM ET]
- Alignment/routes: GAP (not on ESPN WR/CB sheet; TE sheet 404). PENDING_FILM.
- Opportunity: targets 78 (L3 32); target share (player tgt / team receiver tgt) season 28.7%, L3 25.8% — share of pass attempts is not used. Receptions 59 (L3 26). aDOT 5.9; RZ tgt 17; 3rd-down tgt 22 (29% of team 3rd-down tgt); 2-min (≤120s left in half) tgt 13 [pbp].
- Conversion/efficiency/explosive: catch rate 75.6%; YPT 6.05; YAC/rec 3.0; 20+ yd catches 4; NGS: sep 2.43, cushion 5.24, YAC 3.08 vs exp 2.77, share of team intended air yds 23.8% [pbp, NGS].
- Archetype (supported by numbers above): volume/possession + red-zone option. Trend: L3 share 25.8% vs season 28.7% → stable/up.
- Scheme: Sharp (Updated Oct 27; page modified 2026-10-29 15:53 ET) man 21.3/zone 69.9/MOFC 60.2/MOFO 35.7 (man rank #12 of 32). StatRankings (thru Oct 30, upd 10/31): man 46.5% rank 4, zone n/a% — rank order DIFFERS (Sharp #12 vs SR #4)
- PFR: **PFR cache Oct 29 (fresh pull 403)**.
- 8A status: PENDING (Rico ruling on TE/slot→LB/S mapping). Candidate defenders (PFR cache Oct 29, fresh pull 403): Shemar James (LB, DAL, G5): 1-1-14, cmp 100.0%, YPT 14.0, rat 118.7 | DeMarvion Overshown (LB, DAL, G1): 4-4-38, cmp 100.0%, YPT 9.5, rat 145.8 | Caleb Downs (DB, DAL, G5): 10-9-71, cmp 90.0%, YPT 7.1, rat 129.6. DAL: Dee Winters OUT (calf) per ESPN injuries API; ESPN depth chart RILB next = Shemar James.
- QB (ARI; primary J.Brissett): 303 dropbacks, 281 att, cmp 65.5%, YPA 5.72, EPA/db -0.007, sacks 15 (5.0%), scrambles 7 [pbp]. vs blitz (FTN n_blitzers>0, n=83): sack 9.6%, yds/db 4.20; no blitz (n=220): sack 3.2%, yds/db 5.60. NGS: Jacoby Brissett TTT 2.63s, CPOE +5.4, intended air 7.4. OL now: LT Jayden Williams, LG Isaac Seumalo, C Hjalte Froholdt, RG Jon Gaines II, RT Elijah Wilkinson; OL injuries: Jon Gaines II G Out; Elijah Wilkinson OT Active; Hjalte Froholdt C Questionable; Albert Reese IV OT Active [ESPN].
- Teammate injuries / redistribution: Jalen Brooks (WR, Injured Reserve); Tip Reiman (TE, Out); James Conner (RB, Injured Reserve) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.

### Trey McBride (ARI vs DAL) — recyds · rung None @ None
- **PHASE 3: PASS (8A PENDING)** — role, participation and opportunity verified
- Window: declared baseline = all 7 ARI games (wks [1, 2, 3, 4, 5, 6, 7]); L3 = player's last 3 ACTIVE games, wks [5, 6, 7] (inactive weeks excluded, not counted as zeros). Missed/absent: none (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 91%, L3 93% (per wk 1:80%, 2:88%, 3:91%, 4:97%, 5:90%, 6:97%, 7:93%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: Active — McBride caught 10 of 13 targets for 111 yards and a touchdown in Sunday's 30-16 loss to the Broncos. [ESPN injuries API 7:30 PM ET]
- Alignment/routes: GAP (not on ESPN WR/CB sheet; TE sheet 404). PENDING_FILM.
- Opportunity: targets 78 (L3 32); target share (player tgt / team receiver tgt) season 28.7%, L3 25.8% — share of pass attempts is not used. Receptions 59 (L3 26). aDOT 5.9; RZ tgt 17; 3rd-down tgt 22 (29% of team 3rd-down tgt); 2-min (≤120s left in half) tgt 13 [pbp].
- Conversion/efficiency/explosive: catch rate 75.6%; YPT 6.05; YAC/rec 3.0; 20+ yd catches 4; NGS: sep 2.43, cushion 5.24, YAC 3.08 vs exp 2.77, share of team intended air yds 23.8% [pbp, NGS].
- Archetype (supported by numbers above): volume/possession + red-zone option. Trend: L3 share 25.8% vs season 28.7% → stable/up.
- Scheme: Sharp (Updated Oct 27; page modified 2026-10-29 15:53 ET) man 21.3/zone 69.9/MOFC 60.2/MOFO 35.7 (man rank #12 of 32). StatRankings (thru Oct 30, upd 10/31): man 46.5% rank 4, zone n/a% — rank order DIFFERS (Sharp #12 vs SR #4)
- PFR: **PFR cache Oct 29 (fresh pull 403)**.
- 8A status: PENDING (Rico ruling on TE/slot→LB/S mapping). Candidate defenders (PFR cache Oct 29, fresh pull 403): Shemar James (LB, DAL, G5): 1-1-14, cmp 100.0%, YPT 14.0, rat 118.7 | DeMarvion Overshown (LB, DAL, G1): 4-4-38, cmp 100.0%, YPT 9.5, rat 145.8 | Caleb Downs (DB, DAL, G5): 10-9-71, cmp 90.0%, YPT 7.1, rat 129.6. DAL: Dee Winters OUT (calf) per ESPN injuries API; ESPN depth chart RILB next = Shemar James.
- QB (ARI; primary J.Brissett): 303 dropbacks, 281 att, cmp 65.5%, YPA 5.72, EPA/db -0.007, sacks 15 (5.0%), scrambles 7 [pbp]. vs blitz (FTN n_blitzers>0, n=83): sack 9.6%, yds/db 4.20; no blitz (n=220): sack 3.2%, yds/db 5.60. NGS: Jacoby Brissett TTT 2.63s, CPOE +5.4, intended air 7.4. OL now: LT Jayden Williams, LG Isaac Seumalo, C Hjalte Froholdt, RG Jon Gaines II, RT Elijah Wilkinson; OL injuries: Jon Gaines II G Out; Elijah Wilkinson OT Active; Hjalte Froholdt C Questionable; Albert Reese IV OT Active [ESPN].
- Teammate injuries / redistribution: Jalen Brooks (WR, Injured Reserve); Tip Reiman (TE, Out); James Conner (RB, Injured Reserve) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.

### Tyler Warren (IND vs JAX) — recyds · rung None @ None
- **PHASE 3: GAP** — INJURY RETURN after missing wks [6, 7] — no post-return sample; role-regime unverified
- Window: declared baseline = all 7 IND games (wks [1, 2, 3, 4, 5, 6, 7]); L3 = player's last 3 ACTIVE games, wks [3, 4, 5] (inactive weeks excluded, not counted as zeros). Missed/absent: [6, 7] (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 91%, L3 91% (per wk 1:93%, 2:89%, 3:94%, 4:85%, 5:94%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: Active — Warren (groin) is good to go for Sunday's game against the Jaguars, Mike Chappell of FOX59 reports. [ESPN injuries API 7:30 PM ET]
- Alignment/routes: GAP (not on ESPN WR/CB sheet; TE sheet 404). PENDING_FILM.
- Opportunity: targets 36 (L3 24); target share (player tgt / team receiver tgt) season 16.0%, L3 22.4% — share of pass attempts is not used. Receptions 30 (L3 21). aDOT 4.0; RZ tgt 4; 3rd-down tgt 6 (11% of team 3rd-down tgt); 2-min (≤120s left in half) tgt 3 [pbp].
- Conversion/efficiency/explosive: catch rate 83.3%; YPT 5.92; YAC/rec 4.3; 20+ yd catches 2; NGS: sep 3.82, cushion 6.48, YAC 4.55 vs exp 5.22, share of team intended air yds 8.3% [pbp, NGS].
- Archetype (supported by numbers above): secondary target. Trend: L3 share 22.4% vs season 16.0% → stable/up.
- Scheme: Sharp (Updated Oct 27; page modified 2026-10-29 15:53 ET) man 21.0/zone 73.4/MOFC 46.0/MOFO 51.1 (man rank #13 of 32). StatRankings (thru Oct 30, upd 10/31): man 29.1% rank 23, zone 70.9% — rank order DIFFERS (Sharp #13 vs SR #23)
- PFR: **PFR cache Oct 29 (fresh pull 403)**.
- 8A status: PENDING (Rico ruling on TE/slot→LB/S mapping). Candidate defenders (PFR cache Oct 29, fresh pull 403): Foyesade Oluokun (LB, JAX, G5): 18-14-108, cmp 77.8%, YPT 6.0, rat 52.1 | Ventrell Miller (LB, JAX, G5): 14-11-111, cmp 78.6%, YPT 7.9, rat 99.7 | Eric Murray (S, JAX, G4): 1-0-9, cmp 0.0%, YPT 9.0, rat 64.6
- QB (IND; primary D.Jones): 266 dropbacks, 239 att, cmp 59.8%, YPA 5.85, EPA/db -0.158, sacks 19 (7.1%), scrambles 8 [pbp]. vs blitz (FTN n_blitzers>0, n=95): sack 12.6%, yds/db 3.75; no blitz (n=171): sack 4.1%, yds/db 5.58. NGS: Daniel Jones TTT 2.82s, CPOE -2.1, intended air 7.7. OL now: LT Bernhard Raimann, LG Jalen Farmer, C Tanor Bortolini, RG Matt Goncalves, RT Jalen Travis; OL injuries: Matt Goncalves G Active; Dalton Tucker G Active [ESPN].
- Teammate injuries / redistribution: Anthony Gould (WR, Out); Drew Ogletree (TE, Questionable); Alec Pierce (WR, Injured Reserve) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.

### Zay Flowers (BAL vs BUF) — recyds · rung None @ None
- **PHASE 3: PASS** — role, participation and opportunity verified
- Window: declared baseline = all 7 BAL games (wks [1, 2, 3, 4, 5, 6, 7]); L3 = player's last 3 ACTIVE games, wks [5, 6, 7] (inactive weeks excluded, not counted as zeros). Missed/absent: [2] (verified via snap file absence; injury reason not adjudicated).
- Participation: snap % season 65%, L3 85% (per wk 1:29%, 3:33%, 4:73%, 5:82%, 6:88%, 7:85%) [nflverse snap counts]. 60% snap gate: PASS.
- Availability: Active — Flowers brought in eight of 11 targets for 137 yards and a touchdown in the Ravens' 35-13 loss to the Bengals on Sunday. [ESPN injuries API 7:30 PM ET]
- Alignment/routes (ESPN WR/CB sheet, season-to-date): align tag S, LWR/slot/RWR 24%/54%/22%; routes 148; targets/route 34%; YPRR 0.71. Route participation per dropback: GAP (no free per-game routes; nflverse 2026 participation 404).
- Opportunity: targets 53 (L3 31); target share (player tgt / team receiver tgt) season 26.8%, L3 32.3% — share of pass attempts is not used. Receptions 40 (L3 22). aDOT 8.2; RZ tgt 7; 3rd-down tgt 14 (25% of team 3rd-down tgt); 2-min (≤120s left in half) tgt 9 [pbp].
- Conversion/efficiency/explosive: catch rate 75.5%; YPT 11.47; YAC/rec 7.8; 20+ yd catches 9; NGS: sep 3.05, cushion 6.07, YAC 8.22 vs exp 5.04, share of team intended air yds 26.1% [pbp, NGS].
- Archetype (supported by numbers above): volume/possession + red-zone option. Trend: L3 share 32.3% vs season 26.8% → stable/up.
- Scheme: Sharp (Updated Oct 27; page modified 2026-10-29 15:53 ET) man 16.8/zone 74.9/MOFC 45.8/MOFO 49.2 (man rank #18 of 32). StatRankings (thru Oct 30, upd 10/31): man 26.3% rank 25, zone 73.7% — rank order DIFFERS (Sharp #18 vs SR #25)
- PFR: **PFR cache Oct 29 (fresh pull 403)**.
- 8A status: PENDING_FILM; film route/alignment read counts only if every cited play matches pbp, otherwise UNVERIFIED → GAP (disclosed).
- QB (BAL; primary T.Huntley): 237 dropbacks, 200 att, cmp 71.0%, YPA 8.47, EPA/db +0.198, sacks 18 (7.6%), scrambles 19 [pbp]. vs blitz (FTN n_blitzers>0, n=71): sack 14.1%, yds/db 7.38; no blitz (n=166): sack 4.8%, yds/db 7.28. NGS: Tyler Huntley TTT 2.82s, CPOE -2.7, intended air 6.1. OL now: LT Ronnie Stanley, LG John Simpson, C Cam Jurgens, RG Olaivavega Ioane, RT Roger Rosengarten; OL injuries: Olaivavega Ioane G Out; John Simpson G Active; Ronnie Stanley OT Active; Andrew Vorhees G Active; Cam Jurgens C Active [ESPN].
- Teammate injuries / redistribution: Adam Randall (RB, Injured Reserve) [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.
- Injury return: back since wk 3 (5 active games post-return).
- Partial games (snap <40%, treated as in-game exit, not role change): wks [1, 3].

## Film charts: reliability rule applied (README_RELIABILITY.md, Oct 31 7:35 PM ET)
Rule: a film route or alignment read counts for 8A only if every catch or target it cites matches an nflverse pbp play (quarter/clock, receiver, yards). Otherwise it is UNVERIFIED, the item stays a GAP, and the leg carries it as a disclosed gap, not a pass. Match log: src/film_pbp_match.txt (±15 s clock, ±3 yds).
- **Gibbs chart: UNVERIFIED.** 5 of 11 plays match; Q4 5:03 "~20" was actually 3 yds; 5 of the 6 GB@DET plays don't match; the "lost fumble Q3 1:26 at ARI" is wrong (his only lost fumble was 10/25 Q2 0:30, 4 yds). The OZ/IZ pattern is not used. The MIN matchup **CAUTION stands on pbp/FTN alone**: MIN vs edge runs 23 att, 2.26 YPC (#1); light-box (≤6) rate 37.6% vs league 44.4%. Gibbs edge 5.71 YPC.
- **McBride chart: UNVERIFIED.** 2 of 6 plays match. Alignment was unclear anyway → 8A alignment GAP (disclosed), still PENDING Rico's TE mapping ruling.
- **Puka, Bowers, Lamb summaries: UNVERIFIED** (implausible play counts; Lamb's two 40-yd TDs at PHI conflict with his 5-74). Their alignment/route 8A item = GAP (disclosed).
- **Metcalf:** PENDING_FILM_RECHECK; Phase 3 profile is included above.
