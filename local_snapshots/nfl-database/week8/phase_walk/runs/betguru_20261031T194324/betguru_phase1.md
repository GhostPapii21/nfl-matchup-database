# BetGuru — PHASE 1 (Collect and reconcile game data) — Sunday Nov 1, 2026 pool
Script: /workspace/nfl-database/GAME_SCRIPT_2026-10-29.md lines 134–207. Later phases NOT run. Generated 2026-10-31 07:19 PM ET by src/phase1.py.

## Sources (free/public; no keys, no sign-ins)
- nflverse play-by-play 2026 (pulled fresh 2026-10-31 7:17 PM ET): https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet — targets, receptions, yards, air yards, carries, RZ/GL, final-two-minute, OT split, QB designed/scramble/kneel fields.
- nflverse snap counts 2026 (PFR-sourced): https://github.com/nflverse/nflverse-data/releases/download/snap_counts/snap_counts_2026.parquet — snaps, snap %, OL top-5 by offensive snaps per game (used as starting-five PROXY; true "started" flag not in feed).
- nflverse players: https://github.com/nflverse/nflverse-data/releases/download/players/players.parquet — gsis/pfr id mapping.
- ESPN summary API box scores, every completed 2026 REG game wks 1–8: https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={id} (cached src/espn_summary/, parsed src/espn_box.json; event id per row in leg detail) — cross-source credit check.
- ESPN depth chart API: https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2026/teams/{id}/depthcharts — current projected OL five (src/espn_ol_depth.json).
Definitions: target = pass_attempt with receiver, excl. sacks; nullified (no_play) plays excluded; RZ = yardline_100 ≤ 20; GL = ≤ 5; F2M = Q4, ≤120 s left, |score diff| ≤ 8.
Not collected per leg (team-level Phase 1 items, outside the skill-leg ask): tackles/pressures attribution, clean vs coverage sacks — GAP at team level.
Placed Ticket 2 markets barred: Gibbs rec, St. Brown recyds, Godwin rec, London rec, Cook rushrec, Flowers rec, Pickens rec, Lamb recyds.

## Summary
|Player|Market|Rung|Price|Phase 1|Reason|# credit diffs|
|-|-|-|-|-|-|-|
|Aaron Jones|rushyds|None|None|PASS|all Phase 1 fields collected; sources reconcile|0|
|Amon-Ra St. Brown|rec|None|None|PASS|all Phase 1 fields collected; sources reconcile|0|
|Amon-Ra St. Brown|recyds|None|None|FAIL|exact placed Ticket 2 market (off-limits)|0|
|Ashton Jeanty|rushrec|None|None|PASS|all Phase 1 fields collected; credit diffs preserved|1|
|Bijan Robinson|rushrec|None|None|PASS|all Phase 1 fields collected; credit diffs preserved|1|
|Bijan Robinson|rushyds|None|None|PASS|all Phase 1 fields collected; credit diffs preserved|1|
|Braelon Allen|rushrec|None|None|PASS|all Phase 1 fields collected; sources reconcile|0|
|Braelon Allen|rushyds|None|None|PASS|all Phase 1 fields collected; sources reconcile|0|
|Brock Bowers|rec|6|-158|PASS|all Phase 1 fields collected; credit diffs preserved|2|
|Brock Bowers|recyds|None|None|PASS|all Phase 1 fields collected; credit diffs preserved|2|
|Bucky Irving|rushrec|None|None|PASS|all Phase 1 fields collected; sources reconcile|0|
|CeeDee Lamb|rec|None|None|PASS|all Phase 1 fields collected; credit diffs preserved|2|
|CeeDee Lamb|recyds|60|-280|FAIL|exact placed Ticket 2 market (off-limits)|2|
|Chase Brown|rushrec|None|None|PASS|all Phase 1 fields collected; sources reconcile|0|
|Chris Godwin Jr.|rec|None|None|FAIL|exact placed Ticket 2 market (off-limits)|0|
|DK Metcalf|recyds|40|-225|PASS|all Phase 1 fields collected; sources reconcile|0|
|Dallas Goedert|rec|None|None|PASS|all Phase 1 fields collected; credit diffs preserved|1|
|Drake London|rec|None|None|FAIL|exact placed Ticket 2 market (off-limits)|2|
|Drake London|recyds|60|-270|PASS|all Phase 1 fields collected; credit diffs preserved|2|
|Garrett Wilson|recyds|None|None|PASS|all Phase 1 fields collected; credit diffs preserved|1|
|Jahmyr Gibbs|rushrec|None|None|PASS|all Phase 1 fields collected; credit diffs preserved|1|
|Jahmyr Gibbs|rushyds|70|-250|PASS|all Phase 1 fields collected; credit diffs preserved|1|
|James Cook|rushrec|None|None|FAIL|exact placed Ticket 2 market (off-limits)|0|
|James Cook|rushyds|None|None|PASS|all Phase 1 fields collected; sources reconcile|0|
|Javonte Williams|rushyds|None|None|PASS|all Phase 1 fields collected; sources reconcile|0|
|Jaylen Warren|rushrec|None|None|PASS|all Phase 1 fields collected; credit diffs preserved|1|
|Jonathan Taylor|rushrec|None|None|PASS|all Phase 1 fields collected; sources reconcile|0|
|Jonathan Taylor|rushyds|None|None|PASS|all Phase 1 fields collected; sources reconcile|0|
|Justin Jefferson|recyds|None|None|PASS|all Phase 1 fields collected; credit diffs preserved|1|
|Kenneth Walker III|rushyds|None|None|PASS|all Phase 1 fields collected; credit diffs preserved|1|
|Kyren Williams|rushrec|None|None|PASS|all Phase 1 fields collected; sources reconcile|0|
|Parker Washington|recyds|None|None|PASS|all Phase 1 fields collected; sources reconcile|0|
|Puka Nacua|rec|None|None|PASS|all Phase 1 fields collected; sources reconcile|0|
|Puka Nacua|recyds|70|-290|PASS|all Phase 1 fields collected; sources reconcile|0|
|Tee Higgins|recyds|None|None|PASS|all Phase 1 fields collected; sources reconcile|0|
|Tony Pollard|rushrec|None|None|PASS|all Phase 1 fields collected; sources reconcile|0|
|Trey McBride|rec|7|-225|PASS|all Phase 1 fields collected; sources reconcile|0|
|Trey McBride|recyds|None|None|PASS|all Phase 1 fields collected; sources reconcile|0|
|Tyler Warren|recyds|None|None|PASS|all Phase 1 fields collected; sources reconcile|0|
|Zay Flowers|rec|None|None|FAIL|exact placed Ticket 2 market (off-limits)|0|
|Zay Flowers|recyds|None|None|PASS|all Phase 1 fields collected; sources reconcile|0|

## Per-leg detail

### Aaron Jones (MIN vs DET) — rushyds · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; sources reconcile
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Aaron_Jones_rushyds.json` · status: active (not on report)
- Sample rule: every 2026 REG game MIN has played (weeks 1, 2, 3, 4, 5, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|GB|30 (46%)|1|0|0|4|12|40|1|0|1|0|N|1/0/0/12/40 (ev 401872927)|match|Brandel 65, Jackson 65, Fries 65, Darrisaw 65, O'Neill 65|
|2|2026-09-20|CHI|42 (81%)|0|0|0|0|23|105|0|0|0|0|N|0/0/0/23/105 (ev 401872937)|match|Fries 52, Brandel 52, Jackson 52, O'Neill 52, Darrisaw 52|
|3|2026-09-27|TB|47 (80%)|6|5|34|-11|17|58|0|0|0|1|N|6/5/34/17/58 (ev 401872959)|match|Brandel 59, Jackson 59, Fries 59, Darrisaw 59, O'Neill 59|
|4|2026-10-04|MIA|57 (73%)|8|4|34|6|20|94|0|2|0|0|N|8/4/34/20/94 (ev 401872974)|match|Brandel 78, Fries 78, O'Neill 78, Huber 71, Darrisaw 42|
|5|2026-10-11|NO|62 (87%)|3|3|4|-4|25|113|1|0|0|0|N|3/3/4/25/113 (ev 401872987)|match|Demark 71, Brandel 71, Huber 71, Fries 68, O'Neill 68|
|7|2026-10-25|IND|15 (25%)|1|1|0|0|8|26|0|1|0|0|N|1/1/0/8/26 (ev 401873014)|match|Brandel 59, Huber 59, Fries 59, O'Neill 59, Darrisaw 59|

- Totals (nflverse, 6 games played): tgt 19, rec 13, rec yds 72, air yds -5, car 105, rush yds 436. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Christian Darrisaw, LG Joe Huber, C Blake Brandel, RG Will Fries, RT Brian O'Neill
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.

### Amon-Ra St. Brown (DET vs MIN) — rec · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; sources reconcile
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Amon-Ra_St_Brown_rec.json` · status: active (not on report)
- Sample rule: every 2026 REG game DET has played (weeks 1, 2, 3, 4, 5, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|NO|69 (90%)|14|10|67|70|0|0|2|4|0|1|Y: 1tg/0car|14/10/67/0/0 (ev 401872923)|match|Sewell 77, Miller 77, Ratledge 77, Scruggs 77, Bartch 66|
|2|2026-09-17|BUF|62 (95%)|13|9|142|148|0|0|2|2|0|0|N|13/9/142/0/0 (ev 401872932)|match|Bartch 65, Ratledge 65, Borom 65, Scruggs 65, Sewell 65|
|3|2026-09-27|NYJ|48 (74%)|8|4|19|57|0|0|1|3|0|0|N|8/4/19/0/0 (ev 401872954)|match|Ratledge 65, Miller 65, Mahogany 65, Scruggs 65, Sewell 65|
|4|2026-10-04|CAR|68 (96%)|11|8|75|98|0|0|0|3|0|0|N|11/8/75/0/0 (ev 401872978)|match|Ratledge 71, Miller 71, Scruggs 71, Mahogany 71, Sewell 71|
|5|2026-10-11|ARI|57 (86%)|11|6|69|92|0|0|0|4|0|0|N|11/6/69/0/0 (ev 401872991)|match|Miller 66, Mahogany 66, Ratledge 63, Scruggs 63, Sewell 63|
|7|2026-10-25|GB|53 (78%)|11|9|153|139|1|-1|0|0|0|0|N|11/9/153/1/-1 (ev 401873020)|match|Mahogany 68, Miller 68, Ratledge 68, Mays 68, Sewell 68|

- Totals (nflverse, 6 games played): tgt 68, rec 46, rec yds 525, air yds 604, car 1, rush yds -1. OT-only portion: {'tg': 1, 'rec': 1, 'ryd': 4, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Penei Sewell, LG Christian Mahogany, C Cade Mays, RG Tate Ratledge, RT Blake Miller
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.

### Amon-Ra St. Brown (DET vs MIN) — recyds · rung None @ None
- **PHASE 1: FAIL** — exact placed Ticket 2 market (off-limits)
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Amon-Ra_St_Brown_recyds.json` · status: active (not on report)
- Sample rule: every 2026 REG game DET has played (weeks 1, 2, 3, 4, 5, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|NO|69 (90%)|14|10|67|70|0|0|2|4|0|1|Y: 1tg/0car|14/10/67/0/0 (ev 401872923)|match|Sewell 77, Miller 77, Ratledge 77, Scruggs 77, Bartch 66|
|2|2026-09-17|BUF|62 (95%)|13|9|142|148|0|0|2|2|0|0|N|13/9/142/0/0 (ev 401872932)|match|Bartch 65, Ratledge 65, Borom 65, Scruggs 65, Sewell 65|
|3|2026-09-27|NYJ|48 (74%)|8|4|19|57|0|0|1|3|0|0|N|8/4/19/0/0 (ev 401872954)|match|Ratledge 65, Miller 65, Mahogany 65, Scruggs 65, Sewell 65|
|4|2026-10-04|CAR|68 (96%)|11|8|75|98|0|0|0|3|0|0|N|11/8/75/0/0 (ev 401872978)|match|Ratledge 71, Miller 71, Scruggs 71, Mahogany 71, Sewell 71|
|5|2026-10-11|ARI|57 (86%)|11|6|69|92|0|0|0|4|0|0|N|11/6/69/0/0 (ev 401872991)|match|Miller 66, Mahogany 66, Ratledge 63, Scruggs 63, Sewell 63|
|7|2026-10-25|GB|53 (78%)|11|9|153|139|1|-1|0|0|0|0|N|11/9/153/1/-1 (ev 401873020)|match|Mahogany 68, Miller 68, Ratledge 68, Mays 68, Sewell 68|

- Totals (nflverse, 6 games played): tgt 68, rec 46, rec yds 525, air yds 604, car 1, rush yds -1. OT-only portion: {'tg': 1, 'rec': 1, 'ryd': 4, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Penei Sewell, LG Christian Mahogany, C Cade Mays, RG Tate Ratledge, RT Blake Miller
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.

### Ashton Jeanty (LV vs NYJ) — rushrec · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; credit diffs preserved
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Ashton_Jeanty_rushrec.json` · status: active (not on report)
- Sample rule: every 2026 REG game LV has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|MIA|50 (74%)|6|6|45|18|23|102|2|4|0|0|N|6/6/45/23/102 (ev 401872928)|match|Glaze 68, Burford 68, Miller 68, Powers-Johnson 68, Linderbaum 68|
|2|2026-09-20|LAC|51 (81%)|7|4|15|2|21|48|0|0|4|0|N|7/4/15/21/48 (ev 401872941)|match|Burford 63, Powers-Johnson 63, Glaze 63, Miller 63, Linderbaum 63|
|3|2026-09-27|NO|59 (84%)|4|3|37|13|19|56|0|1|2|0|N|3/3/37/19/56 (ev 401872961)|DIFF tg E3/N4|Burford 70, Glaze 70, Miller 70, Linderbaum 70, Powers-Johnson 65|
|4|2026-10-04|KC|56 (67%)|8|6|68|10|15|58|0|2|0|1|N|8/6/68/15/58 (ev 401872976)|match|Burford 84, Glaze 84, Rogers 84, Miller 84, Linderbaum 84|
|5|2026-10-11|NE|32 (53%)|6|3|50|8|10|27|0|0|1|0|N|6/3/50/10/27 (ev 401872986)|match|Burford 60, Miller 60, Powers-Johnson 60, Glaze 60, Linderbaum 60|
|6|2026-10-18|BUF|38 (58%)|6|4|36|19|10|22|1|1|2|0|N|6/4/36/10/22 (ev 401873005)|match|Burford 66, Rogers 66, Miller 66, Glaze 66, Linderbaum 66|
|7|2026-10-25|LA|49 (72%)|8|8|61|28|8|15|1|3|0|0|N|8/8/61/8/15 (ev 401873021)|match|Rogers 68, Burford 68, Miller 68, Glaze 68, Linderbaum 68|

- Totals (nflverse, 7 games played): tgt 45, rec 34, rec yds 312, air yds 98, car 106, rush yds 328. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Kolton Miller, LG Spencer Burford, C Tyler Linderbaum, RG Caleb Rogers, RT DJ Glaze
- Unresolved credit differences (preserved, not forced): Wk3: tg E3/N4. Likely causes: nullified/penalty plays, laterals, 2-pt tries, or ESPN stat corrections; not adjudicated.

### Bijan Robinson (ATL vs TB) — rushrec · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; credit diffs preserved
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Bijan_Robinson_rushrec.json` · status: active (not on report)
- Sample rule: every 2026 REG game ATL has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|PIT|46 (77%)|10|8|90|-30|21|83|1|0|0|0|N|10/8/90/21/83 (ev 401872658)|match|Matthews 60, Bergeron 60, Taylor 60, Neuzil 60, Lindstrom 51|
|2|2026-09-20|CAR|35 (51%)|4|3|9|12|16|72|0|0|0|0|N|4/3/9/16/72 (ev 401872933)|match|Matthews 69, Bergeron 69, Neuzil 69, Lindstrom 59, Taylor 43|
|3|2026-09-24|GB|51 (72%)|2|2|19|-10|29|194|2|0|5|0|N|2/2/19/29/194 (ev 401872948)|match|Bergeron 71, Matthews 71, Neuzil 71, Lindstrom 71, Taylor 71|
|4|2026-10-05|NO|34 (60%)|2|1|2|-5|19|145|2|1|1|0|N|2/1/2/19/145 (ev 401872979)|match|Bergeron 57, Neuzil 57, Taylor 57, Lindstrom 57, Jerrell 46|
|5|2026-10-11|BAL|52 (81%)|7|4|32|2|17|86|0|1|1|1|Y: 0tg/0car|7/4/32/17/86 (ev 401872993)|match|Bergeron 64, Neuzil 64, Lindstrom 64, Taylor 64, Matthews 63|
|6|2026-10-18|CHI|43 (78%)|2|2|-8|-11|9|61|0|0|0|0|N|2/2/-8/9/61 (ev 401872999)|match|Bergeron 55, Neuzil 55, Matthews 55, Taylor 55, Lindstrom 55|
|7|2026-10-25|SF|55 (81%)|5|5|45|1|20|63|0|0|0|0|N|5/5/59/20/63 (ev 401873017)|DIFF yd E59/N45|Bergeron 68, Neuzil 68, Matthews 68, Lindstrom 68, Taylor 68|

- Totals (nflverse, 7 games played): tgt 32, rec 25, rec yds 189, air yds -41, car 131, rush yds 704. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Jake Matthews, LG Matthew Bergeron, C Ryan Neuzil, RG Chris Lindstrom, RT Jawaan Taylor
- Unresolved credit differences (preserved, not forced): Wk7: yd E59/N45. Likely causes: nullified/penalty plays, laterals, 2-pt tries, or ESPN stat corrections; not adjudicated.

### Bijan Robinson (ATL vs TB) — rushyds · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; credit diffs preserved
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Bijan_Robinson_rushyds.json` · status: active (not on report)
- Sample rule: every 2026 REG game ATL has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|PIT|46 (77%)|10|8|90|-30|21|83|1|0|0|0|N|10/8/90/21/83 (ev 401872658)|match|Matthews 60, Bergeron 60, Taylor 60, Neuzil 60, Lindstrom 51|
|2|2026-09-20|CAR|35 (51%)|4|3|9|12|16|72|0|0|0|0|N|4/3/9/16/72 (ev 401872933)|match|Matthews 69, Bergeron 69, Neuzil 69, Lindstrom 59, Taylor 43|
|3|2026-09-24|GB|51 (72%)|2|2|19|-10|29|194|2|0|5|0|N|2/2/19/29/194 (ev 401872948)|match|Bergeron 71, Matthews 71, Neuzil 71, Lindstrom 71, Taylor 71|
|4|2026-10-05|NO|34 (60%)|2|1|2|-5|19|145|2|1|1|0|N|2/1/2/19/145 (ev 401872979)|match|Bergeron 57, Neuzil 57, Taylor 57, Lindstrom 57, Jerrell 46|
|5|2026-10-11|BAL|52 (81%)|7|4|32|2|17|86|0|1|1|1|Y: 0tg/0car|7/4/32/17/86 (ev 401872993)|match|Bergeron 64, Neuzil 64, Lindstrom 64, Taylor 64, Matthews 63|
|6|2026-10-18|CHI|43 (78%)|2|2|-8|-11|9|61|0|0|0|0|N|2/2/-8/9/61 (ev 401872999)|match|Bergeron 55, Neuzil 55, Matthews 55, Taylor 55, Lindstrom 55|
|7|2026-10-25|SF|55 (81%)|5|5|45|1|20|63|0|0|0|0|N|5/5/59/20/63 (ev 401873017)|DIFF yd E59/N45|Bergeron 68, Neuzil 68, Matthews 68, Lindstrom 68, Taylor 68|

- Totals (nflverse, 7 games played): tgt 32, rec 25, rec yds 189, air yds -41, car 131, rush yds 704. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Jake Matthews, LG Matthew Bergeron, C Ryan Neuzil, RG Chris Lindstrom, RT Jawaan Taylor
- Unresolved credit differences (preserved, not forced): Wk7: yd E59/N45. Likely causes: nullified/penalty plays, laterals, 2-pt tries, or ESPN stat corrections; not adjudicated.

### Braelon Allen (NYJ vs LV) — rushrec · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; sources reconcile
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Braelon_Allen_rushrec.json` · status: active (not on report)
- Sample rule: every 2026 REG game NYJ has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|TEN|27 (40%)|1|0|0|0|10|40|0|1|0|0|N|1/0/0/10/40 (ev 401872924)|match|Membou 67, Tippmann 67, Parham 67, Fashanu 67, Myers 67|
|2|2026-09-20|GB|23 (31%)|1|1|8|3|5|7|1|1|1|0|Y: 0tg/0car|1/1/8/5/7 (ev 401872936)|match|Membou 74, Parham 74, Tippmann 74, Fashanu 74, Myers 74|
|3|2026-09-27|DET|34 (52%)|3|3|3|-5|4|14|0|1|0|2|N|3/3/3/4/14 (ev 401872954)|match|Membou 66, Fashanu 66, Tippmann 66, Myers 66, Parham 38|
|4|2026-10-04|CHI|30 (94%)|2|2|8|0|14|59|0|0|0|0|N|2/2/8/14/59 (ev 401872972)|match|Myers 32, Tippmann 32, Fashanu 32, Meredith 32, Membou 31|
|5|2026-10-11|CLE|60 (86%)|4|1|0|-9|24|116|1|1|0|0|N|4/1/0/24/116 (ev 401872983)|match|Tippmann 70, Myers 70, Membou 70, Fashanu 70, Meredith 70|
|6|2026-10-18|NE|54 (87%)|2|2|26|3|17|78|0|0|0|0|N|2/2/26/17/78 (ev 401873001)|match|Tippmann 62, Myers 62, Fashanu 62, Membou 62, Meredith 62|
|7|2026-10-25|MIA|46 (78%)|7|6|30|11|17|104|0|1|1|0|N|7/6/30/17/104 (ev 401873015)|match|Myers 59, Membou 59, Tippmann 59, Fashanu 59, Meredith 59|

- Totals (nflverse, 7 games played): tgt 20, rec 15, rec yds 75, air yds 3, car 91, rush yds 418. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Olu Fashanu, LG Dylan Parham, C Josh Myers, RG Joe Tippmann, RT Armand Membou
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.

### Braelon Allen (NYJ vs LV) — rushyds · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; sources reconcile
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Braelon_Allen_rushyds.json` · status: active (not on report)
- Sample rule: every 2026 REG game NYJ has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|TEN|27 (40%)|1|0|0|0|10|40|0|1|0|0|N|1/0/0/10/40 (ev 401872924)|match|Membou 67, Tippmann 67, Parham 67, Fashanu 67, Myers 67|
|2|2026-09-20|GB|23 (31%)|1|1|8|3|5|7|1|1|1|0|Y: 0tg/0car|1/1/8/5/7 (ev 401872936)|match|Membou 74, Parham 74, Tippmann 74, Fashanu 74, Myers 74|
|3|2026-09-27|DET|34 (52%)|3|3|3|-5|4|14|0|1|0|2|N|3/3/3/4/14 (ev 401872954)|match|Membou 66, Fashanu 66, Tippmann 66, Myers 66, Parham 38|
|4|2026-10-04|CHI|30 (94%)|2|2|8|0|14|59|0|0|0|0|N|2/2/8/14/59 (ev 401872972)|match|Myers 32, Tippmann 32, Fashanu 32, Meredith 32, Membou 31|
|5|2026-10-11|CLE|60 (86%)|4|1|0|-9|24|116|1|1|0|0|N|4/1/0/24/116 (ev 401872983)|match|Tippmann 70, Myers 70, Membou 70, Fashanu 70, Meredith 70|
|6|2026-10-18|NE|54 (87%)|2|2|26|3|17|78|0|0|0|0|N|2/2/26/17/78 (ev 401873001)|match|Tippmann 62, Myers 62, Fashanu 62, Membou 62, Meredith 62|
|7|2026-10-25|MIA|46 (78%)|7|6|30|11|17|104|0|1|1|0|N|7/6/30/17/104 (ev 401873015)|match|Myers 59, Membou 59, Tippmann 59, Fashanu 59, Meredith 59|

- Totals (nflverse, 7 games played): tgt 20, rec 15, rec yds 75, air yds 3, car 91, rush yds 418. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Olu Fashanu, LG Dylan Parham, C Josh Myers, RG Joe Tippmann, RT Armand Membou
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.

### Brock Bowers (LV vs NYJ) — rec · rung 6 @ -158
- **PHASE 1: PASS** — all Phase 1 fields collected; credit diffs preserved
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Brock_Bowers_rec.json` · status: active (not on report)
- Sample rule: every 2026 REG game LV has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|MIA|DNP/absent|–|–|–|–|–|–|–|–|–|–|N|(none)|missed|Glaze 68, Burford 68, Miller 68, Powers-Johnson 68, Linderbaum 68|
|2|2026-09-20|LAC|DNP/absent|–|–|–|–|–|–|–|–|–|–|N|(none)|missed|Burford 63, Powers-Johnson 63, Glaze 63, Miller 63, Linderbaum 63|
|3|2026-09-27|NO|55 (79%)|13|10|116|106|0|0|1|3|0|0|N|14/10/116/0/0 (ev 401872961)|DIFF tg E14/N13|Burford 70, Glaze 70, Miller 70, Linderbaum 70, Powers-Johnson 65|
|4|2026-10-04|KC|69 (82%)|11|6|86|148|0|0|1|1|0|0|N|11/6/86/0/0 (ev 401872976)|match|Burford 84, Glaze 84, Rogers 84, Miller 84, Linderbaum 84|
|5|2026-10-11|NE|42 (70%)|10|8|110|69|0|0|1|1|0|0|N|10/8/110/0/0 (ev 401872986)|match|Burford 60, Miller 60, Powers-Johnson 60, Glaze 60, Linderbaum 60|
|6|2026-10-18|BUF|65 (98%)|9|4|70|115|0|0|0|2|0|0|N|9/4/70/0/0 (ev 401873005)|match|Burford 66, Rogers 66, Miller 66, Glaze 66, Linderbaum 66|
|7|2026-10-25|LA|57 (84%)|9|6|73|81|0|0|0|1|0|0|N|8/6/73/0/0 (ev 401873021)|DIFF tg E8/N9|Rogers 68, Burford 68, Miller 68, Glaze 68, Linderbaum 68|

- Totals (nflverse, 5 games played): tgt 52, rec 34, rec yds 455, air yds 519, car 0, rush yds 0. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Kolton Miller, LG Spencer Burford, C Tyler Linderbaum, RG Caleb Rogers, RT DJ Glaze
- Unresolved credit differences (preserved, not forced): Wk3: tg E14/N13 | Wk7: tg E8/N9. Likely causes: nullified/penalty plays, laterals, 2-pt tries, or ESPN stat corrections; not adjudicated.

### Brock Bowers (LV vs NYJ) — recyds · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; credit diffs preserved
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Brock_Bowers_recyds.json` · status: active (not on report)
- Sample rule: every 2026 REG game LV has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|MIA|DNP/absent|–|–|–|–|–|–|–|–|–|–|N|(none)|missed|Glaze 68, Burford 68, Miller 68, Powers-Johnson 68, Linderbaum 68|
|2|2026-09-20|LAC|DNP/absent|–|–|–|–|–|–|–|–|–|–|N|(none)|missed|Burford 63, Powers-Johnson 63, Glaze 63, Miller 63, Linderbaum 63|
|3|2026-09-27|NO|55 (79%)|13|10|116|106|0|0|1|3|0|0|N|14/10/116/0/0 (ev 401872961)|DIFF tg E14/N13|Burford 70, Glaze 70, Miller 70, Linderbaum 70, Powers-Johnson 65|
|4|2026-10-04|KC|69 (82%)|11|6|86|148|0|0|1|1|0|0|N|11/6/86/0/0 (ev 401872976)|match|Burford 84, Glaze 84, Rogers 84, Miller 84, Linderbaum 84|
|5|2026-10-11|NE|42 (70%)|10|8|110|69|0|0|1|1|0|0|N|10/8/110/0/0 (ev 401872986)|match|Burford 60, Miller 60, Powers-Johnson 60, Glaze 60, Linderbaum 60|
|6|2026-10-18|BUF|65 (98%)|9|4|70|115|0|0|0|2|0|0|N|9/4/70/0/0 (ev 401873005)|match|Burford 66, Rogers 66, Miller 66, Glaze 66, Linderbaum 66|
|7|2026-10-25|LA|57 (84%)|9|6|73|81|0|0|0|1|0|0|N|8/6/73/0/0 (ev 401873021)|DIFF tg E8/N9|Rogers 68, Burford 68, Miller 68, Glaze 68, Linderbaum 68|

- Totals (nflverse, 5 games played): tgt 52, rec 34, rec yds 455, air yds 519, car 0, rush yds 0. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Kolton Miller, LG Spencer Burford, C Tyler Linderbaum, RG Caleb Rogers, RT DJ Glaze
- Unresolved credit differences (preserved, not forced): Wk3: tg E14/N13 | Wk7: tg E8/N9. Likely causes: nullified/penalty plays, laterals, 2-pt tries, or ESPN stat corrections; not adjudicated.

### Bucky Irving (TB vs ATL) — rushrec · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; sources reconcile
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Bucky_Irving_rushrec.json` · status: active (not on report)
- Sample rule: every 2026 REG game TB has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|CIN|35 (61%)|7|7|48|-25|8|45|1|0|0|0|N|7/7/48/8/45 (ev 401872925)|match|Bredeson 57, Wirfs 57, Mauch 57, Goedeke 57, Barton 57|
|2|2026-09-20|CLE|51 (78%)|4|4|1|-22|17|89|0|2|0|0|N|4/4/1/17/89 (ev 401872935)|match|Wirfs 65, Mauch 65, Bredeson 65, Goedeke 65, Barton 65|
|3|2026-09-27|MIN|36 (52%)|4|2|12|14|15|46|0|2|0|0|N|4/2/12/15/46 (ev 401872959)|match|Wirfs 69, Bredeson 69, Mauch 69, Goedeke 69, Barton 69|
|4|2026-10-04|GB|37 (59%)|0|0|0|0|16|61|0|0|0|0|N|0/0/0/16/61 (ev 401872968)|match|Mauch 63, Wirfs 63, Goedeke 63, Bredeson 63, Barton 63|
|5|2026-10-08|DAL|39 (54%)|3|2|10|1|21|165|2|1|1|0|N|3/2/10/21/165 (ev 401872980)|match|Bredeson 72, Goedeke 72, Barton 72, Mauch 71, Wirfs 71|
|6|2026-10-18|PIT|63 (85%)|3|2|3|-9|19|46|0|0|0|0|Y: 2tg/1car|3/2/3/19/46 (ev 401873002)|match|Mauch 74, Bredeson 74, Wirfs 74, Goedeke 74, Barton 74|
|7|2026-10-25|CAR|37 (59%)|2|1|4|-6|24|106|2|1|3|0|N|2/1/4/24/106 (ev 401873018)|match|Chukwuma 63, Barton 63, Mauch 57, Wirfs 57, Bredeson 57|

- Totals (nflverse, 7 games played): tgt 23, rec 18, rec yds 78, air yds -47, car 120, rush yds 558. OT-only portion: {'tg': 2, 'rec': 1, 'ryd': 2, 'car': 1, 'rush': 1}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Tristan Wirfs, LG Ben Bredeson, C Graham Barton, RG Cody Mauch, RT Luke Goedeke
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.

### CeeDee Lamb (DAL vs ARI) — rec · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; credit diffs preserved
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_CeeDee_Lamb_rec.json` · status: active (not on report)
- Sample rule: every 2026 REG game DAL has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|NYG|47 (81%)|8|5|44|90|1|0|1|2|0|0|N|8/5/44/1/0 (ev 401872930)|match|Bass 58, Guyton 58, Booker 58, Steele 58, Beebe 58|
|2|2026-09-20|WAS|41 (75%)|9|8|153|136|0|0|2|1|0|0|N|9/8/153/0/0 (ev 401872944)|match|Steele 55, Bass 55, Guyton 55, Booker 55, Beebe 55|
|3|2026-09-27|BAL|61 (82%)|9|7|112|85|0|0|0|1|0|1|N|8/7/112/0/0 (ev 401872960)|DIFF tg E8/N9|Guyton 74, Bass 74, Booker 74, Beebe 74, Steele 73|
|4|2026-10-04|HOU|67 (86%)|21|17|189|159|1|-6|1|3|0|4|N|21/17/189/1/-6 (ev 401872967)|match|Bass 78, Beebe 78, Steele 78, Guyton 78, Booker 78|
|5|2026-10-08|TB|34 (57%)|5|2|9|56|0|0|0|0|0|0|N|5/2/9/0/0 (ev 401872980)|match|Beebe 60, Booker 60, Steele 60, Smith 60, Guyton 52|
|6|2026-10-18|GB|69 (88%)|19|9|70|153|0|0|0|5|0|0|N|18/9/70/0/0 (ev 401873007)|DIFF tg E18/N19|Smith 78, Beebe 78, Guyton 78, Steele 78, Booker 78|
|7|2026-10-26|PHI|55 (81%)|12|5|74|176|0|0|2|4|0|0|N|12/5/74/0/0 (ev 401873009)|match|Smith 68, Beebe 68, Booker 68, Guyton 68, Steele 68|

- Totals (nflverse, 7 games played): tgt 83, rec 53, rec yds 651, air yds 855, car 2, rush yds -6. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Tyler Guyton, LG Tyler Smith, C Cooper Beebe, RG Tyler Booker, RT Terence Steele
- Unresolved credit differences (preserved, not forced): Wk3: tg E8/N9 | Wk6: tg E18/N19. Likely causes: nullified/penalty plays, laterals, 2-pt tries, or ESPN stat corrections; not adjudicated.

### CeeDee Lamb (DAL vs ARI) — recyds · rung 60 @ -280
- **PHASE 1: FAIL** — exact placed Ticket 2 market (off-limits)
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_CeeDee_Lamb_recyds.json` · status: active (not on report)
- Sample rule: every 2026 REG game DAL has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|NYG|47 (81%)|8|5|44|90|1|0|1|2|0|0|N|8/5/44/1/0 (ev 401872930)|match|Bass 58, Guyton 58, Booker 58, Steele 58, Beebe 58|
|2|2026-09-20|WAS|41 (75%)|9|8|153|136|0|0|2|1|0|0|N|9/8/153/0/0 (ev 401872944)|match|Steele 55, Bass 55, Guyton 55, Booker 55, Beebe 55|
|3|2026-09-27|BAL|61 (82%)|9|7|112|85|0|0|0|1|0|1|N|8/7/112/0/0 (ev 401872960)|DIFF tg E8/N9|Guyton 74, Bass 74, Booker 74, Beebe 74, Steele 73|
|4|2026-10-04|HOU|67 (86%)|21|17|189|159|1|-6|1|3|0|4|N|21/17/189/1/-6 (ev 401872967)|match|Bass 78, Beebe 78, Steele 78, Guyton 78, Booker 78|
|5|2026-10-08|TB|34 (57%)|5|2|9|56|0|0|0|0|0|0|N|5/2/9/0/0 (ev 401872980)|match|Beebe 60, Booker 60, Steele 60, Smith 60, Guyton 52|
|6|2026-10-18|GB|69 (88%)|19|9|70|153|0|0|0|5|0|0|N|18/9/70/0/0 (ev 401873007)|DIFF tg E18/N19|Smith 78, Beebe 78, Guyton 78, Steele 78, Booker 78|
|7|2026-10-26|PHI|55 (81%)|12|5|74|176|0|0|2|4|0|0|N|12/5/74/0/0 (ev 401873009)|match|Smith 68, Beebe 68, Booker 68, Guyton 68, Steele 68|

- Totals (nflverse, 7 games played): tgt 83, rec 53, rec yds 651, air yds 855, car 2, rush yds -6. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Tyler Guyton, LG Tyler Smith, C Cooper Beebe, RG Tyler Booker, RT Terence Steele
- Unresolved credit differences (preserved, not forced): Wk3: tg E8/N9 | Wk6: tg E18/N19. Likely causes: nullified/penalty plays, laterals, 2-pt tries, or ESPN stat corrections; not adjudicated.

### Chase Brown (CIN vs TEN) — rushrec · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; sources reconcile
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Chase_Brown_rushrec.json` · status: active (not on report)
- Sample rule: every 2026 REG game CIN has played (weeks 1, 2, 3, 4, 5, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|TB|46 (72%)|6|5|22|-12|16|56|1|1|3|0|N|6/5/22/16/56 (ev 401872925)|match|Risner 64, Mims 64, Jr. 64, Karras 64, Fairchild 64|
|2|2026-09-20|HOU|42 (70%)|5|3|2|-15|20|80|0|0|0|0|N|5/3/2/20/80 (ev 401872934)|match|Risner 60, Jr. 60, Karras 60, Fairchild 60, Mims 57|
|3|2026-09-27|PIT|40 (70%)|2|2|8|-1|13|61|0|0|0|1|N|2/2/8/13/61 (ev 401872950)|match|Risner 57, Mims 57, Jr. 57, Karras 57, Fairchild 57|
|4|2026-10-04|JAX|60 (79%)|11|11|71|8|9|10|0|0|0|1|N|11/11/71/9/10 (ev 401872969)|match|Karras 76, Mims 76, Jr. 76, Fairchild 76, Risner 76|
|5|2026-10-11|MIA|39 (60%)|4|3|21|-4|13|39|0|2|1|0|N|4/3/21/13/39 (ev 401872982)|match|Karras 65, Fairchild 65, Jr. 65, Risner 65, Mims 62|
|7|2026-10-25|BAL|40 (75%)|5|4|19|-2|11|39|0|0|0|0|N|5/4/19/11/39 (ev 401873012)|match|Fairchild 53, Jr. 53, Karras 50, Mims 50, Risner 50|

- Totals (nflverse, 6 games played): tgt 33, rec 28, rec yds 143, air yds -26, car 82, rush yds 285. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Orlando Brown Jr., LG Dylan Fairchild, C Ted Karras, RG Dalton Risner, RT Amarius Mims
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.

### Chris Godwin Jr. (TB vs ATL) — rec · rung None @ None
- **PHASE 1: FAIL** — exact placed Ticket 2 market (off-limits)
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Chris_Godwin_Jr_rec.json` · status: active (not on report)
- Sample rule: every 2026 REG game TB has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|CIN|49 (86%)|4|4|40|3|1|3|0|0|0|0|N|4/4/40/1/3 (ev 401872925)|match|Bredeson 57, Wirfs 57, Mauch 57, Goedeke 57, Barton 57|
|2|2026-09-20|CLE|56 (86%)|3|3|46|33|1|12|0|0|0|0|N|3/3/46/1/12 (ev 401872935)|match|Wirfs 65, Mauch 65, Bredeson 65, Goedeke 65, Barton 65|
|3|2026-09-27|MIN|43 (62%)|4|3|25|16|0|0|0|0|0|0|N|4/3/25/0/0 (ev 401872959)|match|Wirfs 69, Bredeson 69, Mauch 69, Goedeke 69, Barton 69|
|4|2026-10-04|GB|56 (89%)|7|6|31|16|0|0|0|0|0|0|N|7/6/31/0/0 (ev 401872968)|match|Mauch 63, Wirfs 63, Goedeke 63, Bredeson 63, Barton 63|
|5|2026-10-08|DAL|63 (88%)|3|3|37|5|1|3|0|1|0|0|N|3/3/37/1/3 (ev 401872980)|match|Bredeson 72, Goedeke 72, Barton 72, Mauch 71, Wirfs 71|
|6|2026-10-18|PIT|68 (92%)|8|4|37|54|0|0|0|0|0|1|Y: 2tg/0car|8/4/37/0/0 (ev 401873002)|match|Mauch 74, Bredeson 74, Wirfs 74, Goedeke 74, Barton 74|
|7|2026-10-25|CAR|46 (73%)|5|4|27|-8|0|0|0|2|0|0|N|5/4/27/0/0 (ev 401873018)|match|Chukwuma 63, Barton 63, Mauch 57, Wirfs 57, Bredeson 57|

- Totals (nflverse, 7 games played): tgt 34, rec 27, rec yds 243, air yds 119, car 3, rush yds 18. OT-only portion: {'tg': 2, 'rec': 1, 'ryd': 9, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Tristan Wirfs, LG Ben Bredeson, C Graham Barton, RG Cody Mauch, RT Luke Goedeke
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.

### DK Metcalf (PIT vs CLE) — recyds · rung 40 @ -225
- **PHASE 1: PASS** — all Phase 1 fields collected; sources reconcile
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_DK_Metcalf_recyds.json` · status: active (not on report)
- Sample rule: every 2026 REG game PIT has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|ATL|64 (96%)|10|4|40|204|0|0|0|0|0|0|N|10/4/40/0/0 (ev 401872658)|match|McCormick 67, Cook 67, Anderson 67, Frazier 67, Fautanu 66|
|2|2026-09-20|NE|68 (97%)|9|4|27|62|0|0|0|0|0|0|N|9/4/27/0/0 (ev 401872946)|match|McCormick 70, Frazier 70, Fautanu 70, Cook 67, Anderson 67|
|3|2026-09-27|CIN|59 (95%)|5|3|31|73|0|0|1|1|0|0|N|5/3/31/0/0 (ev 401872950)|match|McCormick 62, Hoffman 62, Iheanachor 62, Fautanu 62, Frazier 62|
|4|2026-10-01|CLE|70 (97%)|9|5|115|155|0|0|0|0|0|0|N|9/5/115/0/0 (ev 401872964)|match|McCormick 72, Hoffman 72, Fautanu 72, Iheanachor 72, Frazier 72|
|5|2026-10-11|IND|55 (92%)|4|3|12|15|1|11|0|0|0|0|N|4/3/12/1/11 (ev 401872985)|match|McCormick 60, Hoffman 60, Fautanu 60, Iheanachor 60, Frazier 60|
|6|2026-10-18|TB|75 (95%)|15|11|93|118|0|0|0|2|0|1|Y: 3tg/0car|15/11/93/0/0 (ev 401873002)|match|Hoffman 79, McCormick 79, Fautanu 79, Iheanachor 79, Frazier 79|
|7|2026-10-25|NO|59 (92%)|6|2|56|110|0|0|0|1|0|0|N|6/2/56/0/0 (ev 401873011)|match|Fautanu 64, McCormick 64, Hoffman 64, Iheanachor 64, Frazier 64|

- Totals (nflverse, 7 games played): tgt 58, rec 32, rec yds 374, air yds 737, car 1, rush yds 11. OT-only portion: {'tg': 3, 'rec': 3, 'ryd': 30, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Troy Fautanu, LG Mason McCormick, C Zach Frazier, RG Brock Hoffman, RT Max Iheanachor
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.

### Dallas Goedert (PHI vs WAS) — rec · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; credit diffs preserved
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Dallas_Goedert_rec.json` · status: active (not on report)
- Sample rule: every 2026 REG game PHI has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|WAS|52 (95%)|5|4|77|52|0|0|2|2|0|0|N|5/4/77/0/0 (ev 401872929)|match|Steen 55, Mailata 55, Dickerson 55, Jurgens 55, Johnson 55|
|2|2026-09-20|TEN|19 (25%)|2|1|4|4|0|0|0|0|0|0|N|3/1/4/0/0 (ev 401872939)|DIFF tg E3/N2|Kendall 76, Steen 76, Mailata 76, Johnson 76, Jurgens 76|
|3|2026-09-28|CHI|DNP/absent|–|–|–|–|–|–|–|–|–|–|N|(none)|missed|Kendall 50, Mailata 50, Steen 50, Jurgens 50, Johnson 50|
|4|2026-10-04|LA|DNP/absent|–|–|–|–|–|–|–|–|–|–|N|(none)|missed|Bell 61, Kendall 61, Steen 61, Mailata 61, Jurgens 61|
|5|2026-10-11|JAX|43 (69%)|9|6|38|36|0|0|0|0|0|2|N|9/6/38/0/0 (ev 401872981)|match|Bell 62, Mailata 62, Majors 62, Lampkin 62, Steen 48|
|6|2026-10-18|CAR|52 (81%)|8|6|61|54|0|0|0|0|0|0|N|8/6/61/0/0 (ev 401872998)|match|Bell 64, Steen 64, Mailata 64, Majors 64, Lampkin 64|
|7|2026-10-26|DAL|48 (73%)|7|5|48|25|0|0|0|1|0|0|N|7/5/48/0/0 (ev 401873009)|match|Bell 66, Mailata 66, Steen 66, Kendall 66, Dickerson 66|

- Totals (nflverse, 5 games played): tgt 31, rec 22, rec yds 228, air yds 171, car 0, rush yds 0. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Jordan Mailata, LG Landon Dickerson, C Drew Kendall, RG Tyler Steen, RT Markel Bell
- Unresolved credit differences (preserved, not forced): Wk2: tg E3/N2. Likely causes: nullified/penalty plays, laterals, 2-pt tries, or ESPN stat corrections; not adjudicated.

### Drake London (ATL vs TB) — rec · rung None @ None
- **PHASE 1: FAIL** — exact placed Ticket 2 market (off-limits)
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Drake_London_rec.json` · status: active (not on report)
- Sample rule: every 2026 REG game ATL has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|PIT|59 (98%)|4|2|29|22|1|6|0|0|0|0|N|5/2/29/1/6 (ev 401872658)|DIFF tg E5/N4|Matthews 60, Bergeron 60, Taylor 60, Neuzil 60, Lindstrom 51|
|2|2026-09-20|CAR|43 (62%)|5|4|51|23|1|-2|0|0|0|0|N|5/4/51/1/-2 (ev 401872933)|match|Matthews 69, Bergeron 69, Neuzil 69, Lindstrom 59, Taylor 43|
|3|2026-09-24|GB|66 (93%)|10|9|194|97|0|0|0|0|0|0|N|10/9/194/0/0 (ev 401872948)|match|Bergeron 71, Matthews 71, Neuzil 71, Lindstrom 71, Taylor 71|
|4|2026-10-05|NO|51 (89%)|6|5|96|66|0|0|0|0|0|0|N|6/5/96/0/0 (ev 401872979)|match|Bergeron 57, Neuzil 57, Taylor 57, Lindstrom 57, Jerrell 46|
|5|2026-10-11|BAL|63 (98%)|11|7|118|119|0|0|0|0|0|0|Y: 2tg/0car|11/7/118/0/0 (ev 401872993)|match|Bergeron 64, Neuzil 64, Lindstrom 64, Taylor 64, Matthews 63|
|6|2026-10-18|CHI|55 (100%)|11|4|62|143|0|0|0|3|0|0|N|10/4/62/0/0 (ev 401872999)|DIFF tg E10/N11|Bergeron 55, Neuzil 55, Matthews 55, Taylor 55, Lindstrom 55|
|7|2026-10-25|SF|55 (81%)|10|7|66|86|0|0|1|2|0|0|N|10/7/66/0/0 (ev 401873017)|match|Bergeron 68, Neuzil 68, Matthews 68, Lindstrom 68, Taylor 68|

- Totals (nflverse, 7 games played): tgt 57, rec 38, rec yds 616, air yds 556, car 2, rush yds 4. OT-only portion: {'tg': 2, 'rec': 1, 'ryd': 20, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Jake Matthews, LG Matthew Bergeron, C Ryan Neuzil, RG Chris Lindstrom, RT Jawaan Taylor
- Unresolved credit differences (preserved, not forced): Wk1: tg E5/N4 | Wk6: tg E10/N11. Likely causes: nullified/penalty plays, laterals, 2-pt tries, or ESPN stat corrections; not adjudicated.

### Drake London (ATL vs TB) — recyds · rung 60 @ -270
- **PHASE 1: PASS** — all Phase 1 fields collected; credit diffs preserved
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Drake_London_recyds.json` · status: active (not on report)
- Sample rule: every 2026 REG game ATL has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|PIT|59 (98%)|4|2|29|22|1|6|0|0|0|0|N|5/2/29/1/6 (ev 401872658)|DIFF tg E5/N4|Matthews 60, Bergeron 60, Taylor 60, Neuzil 60, Lindstrom 51|
|2|2026-09-20|CAR|43 (62%)|5|4|51|23|1|-2|0|0|0|0|N|5/4/51/1/-2 (ev 401872933)|match|Matthews 69, Bergeron 69, Neuzil 69, Lindstrom 59, Taylor 43|
|3|2026-09-24|GB|66 (93%)|10|9|194|97|0|0|0|0|0|0|N|10/9/194/0/0 (ev 401872948)|match|Bergeron 71, Matthews 71, Neuzil 71, Lindstrom 71, Taylor 71|
|4|2026-10-05|NO|51 (89%)|6|5|96|66|0|0|0|0|0|0|N|6/5/96/0/0 (ev 401872979)|match|Bergeron 57, Neuzil 57, Taylor 57, Lindstrom 57, Jerrell 46|
|5|2026-10-11|BAL|63 (98%)|11|7|118|119|0|0|0|0|0|0|Y: 2tg/0car|11/7/118/0/0 (ev 401872993)|match|Bergeron 64, Neuzil 64, Lindstrom 64, Taylor 64, Matthews 63|
|6|2026-10-18|CHI|55 (100%)|11|4|62|143|0|0|0|3|0|0|N|10/4/62/0/0 (ev 401872999)|DIFF tg E10/N11|Bergeron 55, Neuzil 55, Matthews 55, Taylor 55, Lindstrom 55|
|7|2026-10-25|SF|55 (81%)|10|7|66|86|0|0|1|2|0|0|N|10/7/66/0/0 (ev 401873017)|match|Bergeron 68, Neuzil 68, Matthews 68, Lindstrom 68, Taylor 68|

- Totals (nflverse, 7 games played): tgt 57, rec 38, rec yds 616, air yds 556, car 2, rush yds 4. OT-only portion: {'tg': 2, 'rec': 1, 'ryd': 20, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Jake Matthews, LG Matthew Bergeron, C Ryan Neuzil, RG Chris Lindstrom, RT Jawaan Taylor
- Unresolved credit differences (preserved, not forced): Wk1: tg E5/N4 | Wk6: tg E10/N11. Likely causes: nullified/penalty plays, laterals, 2-pt tries, or ESPN stat corrections; not adjudicated.

### Garrett Wilson (NYJ vs LV) — recyds · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; credit diffs preserved
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Garrett_Wilson_recyds.json` · status: active (not on report)
- Sample rule: every 2026 REG game NYJ has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|TEN|50 (75%)|7|6|79|77|0|0|0|0|0|0|N|7/6/79/0/0 (ev 401872924)|match|Membou 67, Tippmann 67, Parham 67, Fashanu 67, Myers 67|
|2|2026-09-20|GB|65 (88%)|7|5|57|75|0|0|1|1|0|0|Y: 0tg/0car|7/5/57/0/0 (ev 401872936)|match|Membou 74, Parham 74, Tippmann 74, Fashanu 74, Myers 74|
|3|2026-09-27|DET|62 (94%)|14|10|107|132|0|0|1|1|0|2|N|13/10/107/0/0 (ev 401872954)|DIFF tg E13/N14|Membou 66, Fashanu 66, Tippmann 66, Myers 66, Parham 38|
|4|2026-10-04|CHI|32 (100%)|4|3|27|31|0|0|0|0|0|0|N|4/3/27/0/0 (ev 401872972)|match|Myers 32, Tippmann 32, Fashanu 32, Meredith 32, Membou 31|
|5|2026-10-11|CLE|65 (93%)|11|7|104|92|0|0|1|1|0|0|N|11/7/104/0/0 (ev 401872983)|match|Tippmann 70, Myers 70, Membou 70, Fashanu 70, Meredith 70|
|6|2026-10-18|NE|61 (98%)|6|4|44|56|0|0|0|1|0|0|N|6/4/44/0/0 (ev 401873001)|match|Tippmann 62, Myers 62, Fashanu 62, Membou 62, Meredith 62|
|7|2026-10-25|MIA|50 (85%)|3|2|26|25|0|0|0|0|0|0|N|3/2/26/0/0 (ev 401873015)|match|Myers 59, Membou 59, Tippmann 59, Fashanu 59, Meredith 59|

- Totals (nflverse, 7 games played): tgt 52, rec 37, rec yds 444, air yds 488, car 0, rush yds 0. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Olu Fashanu, LG Dylan Parham, C Josh Myers, RG Joe Tippmann, RT Armand Membou
- Unresolved credit differences (preserved, not forced): Wk3: tg E13/N14. Likely causes: nullified/penalty plays, laterals, 2-pt tries, or ESPN stat corrections; not adjudicated.

### Jahmyr Gibbs (DET vs MIN) — rushrec · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; credit diffs preserved
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Jahmyr_Gibbs_rushrec.json` · status: active (not on report)
- Sample rule: every 2026 REG game DET has played (weeks 1, 2, 3, 4, 5, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|NO|57 (74%)|5|5|30|-4|29|156|2|0|5|0|Y: 1tg/5car|5/5/30/29/156 (ev 401872923)|match|Sewell 77, Miller 77, Ratledge 77, Scruggs 77, Bartch 66|
|2|2026-09-17|BUF|54 (83%)|8|6|61|34|16|52|1|2|0|0|N|8/6/61/16/52 (ev 401872932)|match|Bartch 65, Ratledge 65, Borom 65, Scruggs 65, Sewell 65|
|3|2026-09-27|NYJ|45 (69%)|8|7|65|4|20|99|3|3|2|0|N|8/7/65/20/99 (ev 401872954)|match|Ratledge 65, Miller 65, Mahogany 65, Scruggs 65, Sewell 65|
|4|2026-10-04|CAR|62 (87%)|7|4|22|22|15|46|1|1|1|0|N|7/4/31/15/46 (ev 401872978)|DIFF yd E31/N22|Ratledge 71, Miller 71, Scruggs 71, Mahogany 71, Sewell 71|
|5|2026-10-11|ARI|46 (70%)|6|5|56|-7|25|151|2|0|5|0|N|6/5/56/25/151 (ev 401872991)|match|Miller 66, Mahogany 66, Ratledge 63, Scruggs 63, Sewell 63|
|7|2026-10-25|GB|61 (90%)|6|5|27|-12|29|116|0|1|0|0|N|6/5/27/29/116 (ev 401873020)|match|Mahogany 68, Miller 68, Ratledge 68, Mays 68, Sewell 68|

- Totals (nflverse, 6 games played): tgt 40, rec 32, rec yds 261, air yds 37, car 134, rush yds 620. OT-only portion: {'tg': 1, 'rec': 1, 'ryd': 7, 'car': 5, 'rush': 28}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Penei Sewell, LG Christian Mahogany, C Cade Mays, RG Tate Ratledge, RT Blake Miller
- Unresolved credit differences (preserved, not forced): Wk4: yd E31/N22. Likely causes: nullified/penalty plays, laterals, 2-pt tries, or ESPN stat corrections; not adjudicated.

### Jahmyr Gibbs (DET vs MIN) — rushyds · rung 70 @ -250
- **PHASE 1: PASS** — all Phase 1 fields collected; credit diffs preserved
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Jahmyr_Gibbs_rushyds.json` · status: active (not on report)
- Sample rule: every 2026 REG game DET has played (weeks 1, 2, 3, 4, 5, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|NO|57 (74%)|5|5|30|-4|29|156|2|0|5|0|Y: 1tg/5car|5/5/30/29/156 (ev 401872923)|match|Sewell 77, Miller 77, Ratledge 77, Scruggs 77, Bartch 66|
|2|2026-09-17|BUF|54 (83%)|8|6|61|34|16|52|1|2|0|0|N|8/6/61/16/52 (ev 401872932)|match|Bartch 65, Ratledge 65, Borom 65, Scruggs 65, Sewell 65|
|3|2026-09-27|NYJ|45 (69%)|8|7|65|4|20|99|3|3|2|0|N|8/7/65/20/99 (ev 401872954)|match|Ratledge 65, Miller 65, Mahogany 65, Scruggs 65, Sewell 65|
|4|2026-10-04|CAR|62 (87%)|7|4|22|22|15|46|1|1|1|0|N|7/4/31/15/46 (ev 401872978)|DIFF yd E31/N22|Ratledge 71, Miller 71, Scruggs 71, Mahogany 71, Sewell 71|
|5|2026-10-11|ARI|46 (70%)|6|5|56|-7|25|151|2|0|5|0|N|6/5/56/25/151 (ev 401872991)|match|Miller 66, Mahogany 66, Ratledge 63, Scruggs 63, Sewell 63|
|7|2026-10-25|GB|61 (90%)|6|5|27|-12|29|116|0|1|0|0|N|6/5/27/29/116 (ev 401873020)|match|Mahogany 68, Miller 68, Ratledge 68, Mays 68, Sewell 68|

- Totals (nflverse, 6 games played): tgt 40, rec 32, rec yds 261, air yds 37, car 134, rush yds 620. OT-only portion: {'tg': 1, 'rec': 1, 'ryd': 7, 'car': 5, 'rush': 28}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Penei Sewell, LG Christian Mahogany, C Cade Mays, RG Tate Ratledge, RT Blake Miller
- Unresolved credit differences (preserved, not forced): Wk4: yd E31/N22. Likely causes: nullified/penalty plays, laterals, 2-pt tries, or ESPN stat corrections; not adjudicated.

### James Cook (BUF vs BAL) — rushrec · rung None @ None
- **PHASE 1: FAIL** — exact placed Ticket 2 market (off-limits)
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_James_Cook_rushrec.json` · status: active (not on report)
- Sample rule: every 2026 REG game BUF has played (weeks 1, 2, 3, 4, 5, 6); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|HOU|42 (72%)|4|3|12|-4|13|57|0|1|0|0|N|4/3/12/13/57 (ev 401872660)|match|Anderson 58, Torrence 58, Brown 58, Dawkins 58, McGovern 58|
|2|2026-09-17|DET|55 (74%)|3|1|4|1|21|135|1|1|2|0|N|3/1/4/21/135 (ev 401872932)|match|Anderson 74, Dawkins 74, Brown 74, Torrence 74, McGovern 74|
|3|2026-09-27|LAC|44 (67%)|1|0|0|-2|24|154|1|0|2|0|N|1/0/0/24/154 (ev 401872953)|match|Anderson 66, Torrence 66, Dawkins 66, Brown 66, McGovern 66|
|4|2026-10-04|NE|35 (59%)|2|2|8|-3|12|75|1|0|0|0|N|2/2/8/12/75 (ev 401872971)|match|Anderson 59, Torrence 59, Dawkins 59, Brown 59, McGovern 59|
|5|2026-10-12|LA|40 (62%)|1|1|7|2|25|111|2|0|3|0|Y: 0tg/4car|1/1/7/25/111 (ev 401872994)|match|Anderson 64, Torrence 64, Dawkins 64, McGovern 64, Grable 48|
|6|2026-10-18|LV|45 (66%)|3|3|58|-8|22|95|1|0|1|0|N|3/3/58/22/95 (ev 401873005)|match|Anderson 68, Dawkins 68, Torrence 68, McGovern 68, Brown 68|

- Totals (nflverse, 6 games played): tgt 14, rec 10, rec yds 89, air yds -14, car 117, rush yds 627. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 4, 'rush': 6}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Dion Dawkins, LG Alec Anderson, C Connor McGovern, RG O'Cyrus Torrence, RT Spencer Brown
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.

### James Cook (BUF vs BAL) — rushyds · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; sources reconcile
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_James_Cook_rushyds.json` · status: active (not on report)
- Sample rule: every 2026 REG game BUF has played (weeks 1, 2, 3, 4, 5, 6); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|HOU|42 (72%)|4|3|12|-4|13|57|0|1|0|0|N|4/3/12/13/57 (ev 401872660)|match|Anderson 58, Torrence 58, Brown 58, Dawkins 58, McGovern 58|
|2|2026-09-17|DET|55 (74%)|3|1|4|1|21|135|1|1|2|0|N|3/1/4/21/135 (ev 401872932)|match|Anderson 74, Dawkins 74, Brown 74, Torrence 74, McGovern 74|
|3|2026-09-27|LAC|44 (67%)|1|0|0|-2|24|154|1|0|2|0|N|1/0/0/24/154 (ev 401872953)|match|Anderson 66, Torrence 66, Dawkins 66, Brown 66, McGovern 66|
|4|2026-10-04|NE|35 (59%)|2|2|8|-3|12|75|1|0|0|0|N|2/2/8/12/75 (ev 401872971)|match|Anderson 59, Torrence 59, Dawkins 59, Brown 59, McGovern 59|
|5|2026-10-12|LA|40 (62%)|1|1|7|2|25|111|2|0|3|0|Y: 0tg/4car|1/1/7/25/111 (ev 401872994)|match|Anderson 64, Torrence 64, Dawkins 64, McGovern 64, Grable 48|
|6|2026-10-18|LV|45 (66%)|3|3|58|-8|22|95|1|0|1|0|N|3/3/58/22/95 (ev 401873005)|match|Anderson 68, Dawkins 68, Torrence 68, McGovern 68, Brown 68|

- Totals (nflverse, 6 games played): tgt 14, rec 10, rec yds 89, air yds -14, car 117, rush yds 627. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 4, 'rush': 6}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Dion Dawkins, LG Alec Anderson, C Connor McGovern, RG O'Cyrus Torrence, RT Spencer Brown
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.

### Javonte Williams (DAL vs ARI) — rushyds · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; sources reconcile
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Javonte_Williams_rushyds.json` · status: active (not on report)
- Sample rule: every 2026 REG game DAL has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|NYG|41 (71%)|5|5|31|-11|12|41|2|2|3|0|N|5/5/31/12/41 (ev 401872930)|match|Bass 58, Guyton 58, Booker 58, Steele 58, Beebe 58|
|2|2026-09-20|WAS|44 (80%)|4|3|20|-12|12|30|0|1|1|0|N|4/3/20/12/30 (ev 401872944)|match|Steele 55, Bass 55, Guyton 55, Booker 55, Beebe 55|
|3|2026-09-27|BAL|56 (76%)|3|2|5|-9|19|98|1|0|2|0|N|3/2/5/19/98 (ev 401872960)|match|Guyton 74, Bass 74, Booker 74, Beebe 74, Steele 73|
|4|2026-10-04|HOU|58 (74%)|5|5|21|1|19|62|3|0|5|1|N|5/5/21/19/62 (ev 401872967)|match|Bass 78, Beebe 78, Steele 78, Guyton 78, Booker 78|
|5|2026-10-08|TB|51 (85%)|3|2|17|5|12|45|1|0|2|0|N|3/2/17/12/45 (ev 401872980)|match|Beebe 60, Booker 60, Steele 60, Smith 60, Guyton 52|
|6|2026-10-18|GB|57 (73%)|2|2|9|-10|11|41|1|0|2|0|N|2/2/9/11/41 (ev 401873007)|match|Smith 78, Beebe 78, Guyton 78, Steele 78, Booker 78|
|7|2026-10-26|PHI|44 (65%)|0|0|0|0|25|155|1|0|2|0|N|0/0/0/25/155 (ev 401873009)|match|Smith 68, Beebe 68, Booker 68, Guyton 68, Steele 68|

- Totals (nflverse, 7 games played): tgt 22, rec 19, rec yds 103, air yds -36, car 110, rush yds 472. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Tyler Guyton, LG Tyler Smith, C Cooper Beebe, RG Tyler Booker, RT Terence Steele
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.

### Jaylen Warren (PIT vs CLE) — rushrec · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; credit diffs preserved
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Jaylen_Warren_rushrec.json` · status: active (not on report)
- Sample rule: every 2026 REG game PIT has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|ATL|25 (37%)|6|5|27|-6|10|46|0|2|0|0|N|6/5/27/10/46 (ev 401872658)|match|McCormick 67, Cook 67, Anderson 67, Frazier 67, Fautanu 66|
|2|2026-09-20|NE|50 (71%)|4|2|34|-11|11|43|0|0|0|0|N|4/2/34/11/43 (ev 401872946)|match|McCormick 70, Frazier 70, Fautanu 70, Cook 67, Anderson 67|
|3|2026-09-27|CIN|56 (90%)|4|3|49|-2|17|127|0|1|0|0|N|4/3/49/17/127 (ev 401872950)|match|McCormick 62, Hoffman 62, Iheanachor 62, Fautanu 62, Frazier 62|
|4|2026-10-01|CLE|70 (97%)|7|3|33|4|17|93|0|2|0|0|N|6/3/33/17/93 (ev 401872964)|DIFF tg E6/N7|McCormick 72, Hoffman 72, Fautanu 72, Iheanachor 72, Frazier 72|
|5|2026-10-11|IND|52 (87%)|6|6|87|-23|15|101|2|0|0|0|N|6/6/87/15/101 (ev 401872985)|match|McCormick 60, Hoffman 60, Fautanu 60, Iheanachor 60, Frazier 60|
|6|2026-10-18|TB|59 (75%)|4|2|28|4|14|50|0|0|1|0|Y: 1tg/4car|4/2/28/14/50 (ev 401873002)|match|Hoffman 79, McCormick 79, Fautanu 79, Iheanachor 79, Frazier 79|
|7|2026-10-25|NO|40 (62%)|4|3|36|-7|18|101|0|0|0|0|N|4/3/36/18/101 (ev 401873011)|match|Fautanu 64, McCormick 64, Hoffman 64, Iheanachor 64, Frazier 64|

- Totals (nflverse, 7 games played): tgt 35, rec 24, rec yds 294, air yds -41, car 102, rush yds 561. OT-only portion: {'tg': 1, 'rec': 1, 'ryd': 12, 'car': 4, 'rush': 13}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Troy Fautanu, LG Mason McCormick, C Zach Frazier, RG Brock Hoffman, RT Max Iheanachor
- Unresolved credit differences (preserved, not forced): Wk4: tg E6/N7. Likely causes: nullified/penalty plays, laterals, 2-pt tries, or ESPN stat corrections; not adjudicated.

### Jonathan Taylor (IND vs JAX) — rushrec · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; sources reconcile
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Jonathan_Taylor_rushrec.json` · status: active (not on report)
- Sample rule: every 2026 REG game IND has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|BAL|48 (89%)|4|3|23|0|19|98|2|0|3|0|N|4/3/23/19/98 (ev 401872659)|match|Goncalves 54, Travis 54, Bortolini 54, Nelson 54, Raimann 54|
|2|2026-09-20|KC|61 (94%)|4|4|40|-1|24|92|2|0|2|0|Y: 0tg/2car|4/4/40/24/92 (ev 401872945)|match|Travis 65, Goncalves 65, Bortolini 65, Nelson 65, Raimann 65|
|3|2026-09-27|HOU|60 (85%)|3|2|4|-13|23|68|0|1|0|0|N|3/2/4/23/68 (ev 401872951)|match|Goncalves 71, Travis 71, Raimann 71, Bortolini 71, Nelson 71|
|4|2026-10-04|WAS|47 (71%)|4|1|2|-12|20|95|2|0|2|0|N|4/1/2/20/95 (ev 401872965)|match|Goncalves 66, Travis 66, Bortolini 66, Nelson 63, Raimann 59|
|5|2026-10-11|PIT|52 (73%)|4|3|37|0|15|45|0|1|4|0|N|4/3/37/15/45 (ev 401872985)|match|Goncalves 71, Raimann 71, Nelson 71, Bortolini 71, Travis 67|
|6|2026-10-18|TEN|65 (78%)|4|2|57|-1|21|94|1|0|2|1|N|4/2/57/21/94 (ev 401873003)|match|Travis 83, Goncalves 83, Raimann 83, Bortolini 83, Nelson 83|
|7|2026-10-25|MIN|41 (67%)|3|2|15|-8|18|95|1|0|0|0|N|3/2/15/18/95 (ev 401873014)|match|Travis 61, Goncalves 61, Raimann 61, Nelson 61, Bortolini 61|

- Totals (nflverse, 7 games played): tgt 26, rec 17, rec yds 178, air yds -35, car 140, rush yds 587. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 2, 'rush': -3}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Bernhard Raimann, LG Jalen Farmer, C Tanor Bortolini, RG Matt Goncalves, RT Jalen Travis
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.

### Jonathan Taylor (IND vs JAX) — rushyds · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; sources reconcile
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Jonathan_Taylor_rushyds.json` · status: active (not on report)
- Sample rule: every 2026 REG game IND has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|BAL|48 (89%)|4|3|23|0|19|98|2|0|3|0|N|4/3/23/19/98 (ev 401872659)|match|Goncalves 54, Travis 54, Bortolini 54, Nelson 54, Raimann 54|
|2|2026-09-20|KC|61 (94%)|4|4|40|-1|24|92|2|0|2|0|Y: 0tg/2car|4/4/40/24/92 (ev 401872945)|match|Travis 65, Goncalves 65, Bortolini 65, Nelson 65, Raimann 65|
|3|2026-09-27|HOU|60 (85%)|3|2|4|-13|23|68|0|1|0|0|N|3/2/4/23/68 (ev 401872951)|match|Goncalves 71, Travis 71, Raimann 71, Bortolini 71, Nelson 71|
|4|2026-10-04|WAS|47 (71%)|4|1|2|-12|20|95|2|0|2|0|N|4/1/2/20/95 (ev 401872965)|match|Goncalves 66, Travis 66, Bortolini 66, Nelson 63, Raimann 59|
|5|2026-10-11|PIT|52 (73%)|4|3|37|0|15|45|0|1|4|0|N|4/3/37/15/45 (ev 401872985)|match|Goncalves 71, Raimann 71, Nelson 71, Bortolini 71, Travis 67|
|6|2026-10-18|TEN|65 (78%)|4|2|57|-1|21|94|1|0|2|1|N|4/2/57/21/94 (ev 401873003)|match|Travis 83, Goncalves 83, Raimann 83, Bortolini 83, Nelson 83|
|7|2026-10-25|MIN|41 (67%)|3|2|15|-8|18|95|1|0|0|0|N|3/2/15/18/95 (ev 401873014)|match|Travis 61, Goncalves 61, Raimann 61, Nelson 61, Bortolini 61|

- Totals (nflverse, 7 games played): tgt 26, rec 17, rec yds 178, air yds -35, car 140, rush yds 587. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 2, 'rush': -3}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Bernhard Raimann, LG Jalen Farmer, C Tanor Bortolini, RG Matt Goncalves, RT Jalen Travis
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.

### Justin Jefferson (MIN vs DET) — recyds · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; credit diffs preserved
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Justin_Jefferson_recyds.json` · status: active (not on report)
- Sample rule: every 2026 REG game MIN has played (weeks 1, 2, 3, 4, 5, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|GB|60 (92%)|10|8|92|80|0|0|2|3|0|0|N|9/8/92/0/0 (ev 401872927)|DIFF tg E9/N10|Brandel 65, Jackson 65, Fries 65, Darrisaw 65, O'Neill 65|
|2|2026-09-20|CHI|52 (100%)|6|3|55|91|0|0|0|1|0|0|N|6/3/55/0/0 (ev 401872937)|match|Fries 52, Brandel 52, Jackson 52, O'Neill 52, Darrisaw 52|
|3|2026-09-27|TB|7 (12%)|2|2|32|18|0|0|0|0|0|0|N|2/2/32/0/0 (ev 401872959)|match|Brandel 59, Jackson 59, Fries 59, Darrisaw 59, O'Neill 59|
|4|2026-10-04|MIA|DNP/absent|–|–|–|–|–|–|–|–|–|–|N|(none)|missed|Brandel 78, Fries 78, O'Neill 78, Huber 71, Darrisaw 42|
|5|2026-10-11|NO|63 (89%)|7|6|79|74|1|-11|1|1|0|0|N|7/6/79/1/-11 (ev 401872987)|match|Demark 71, Brandel 71, Huber 71, Fries 68, O'Neill 68|
|7|2026-10-25|IND|55 (93%)|7|4|44|75|0|0|0|1|0|0|N|7/4/44/0/0 (ev 401873014)|match|Brandel 59, Huber 59, Fries 59, O'Neill 59, Darrisaw 59|

- Totals (nflverse, 5 games played): tgt 32, rec 23, rec yds 302, air yds 338, car 1, rush yds -11. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Christian Darrisaw, LG Joe Huber, C Blake Brandel, RG Will Fries, RT Brian O'Neill
- Unresolved credit differences (preserved, not forced): Wk1: tg E9/N10. Likely causes: nullified/penalty plays, laterals, 2-pt tries, or ESPN stat corrections; not adjudicated.

### Kenneth Walker III (KC vs DEN) — rushyds · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; credit diffs preserved
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Kenneth_Walker_III_rushyds.json` · status: active (not on report)
- Sample rule: every 2026 REG game KC has played (weeks 1, 2, 3, 4, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-14|DEN|47 (68%)|6|3|18|-2|23|173|2|1|1|0|N|6/3/18/23/173 (ev 401872931)|match|Suamataia 69, Smith 69, Benson 69, Humphrey 69, Moore 68|
|2|2026-09-20|IND|66 (82%)|10|6|61|13|24|117|0|2|3|0|Y: 2tg/7car|10/6/61/24/117 (ev 401872945)|match|Suamataia 80, Smith 80, Benson 80, Humphrey 80, Moore 79|
|3|2026-09-27|MIA|38 (73%)|2|2|3|-7|18|70|2|2|1|0|N|2/2/3/18/70 (ev 401872952)|match|Suamataia 52, Smith 52, Benson 52, Humphrey 52, Moore 51|
|4|2026-10-04|LV|45 (75%)|2|1|2|-5|22|177|2|1|3|0|N|1/1/2/22/177 (ev 401872976)|DIFF tg E1/N2|Benson 60, Humphrey 60, Caliendo 60, Smith 60, Moore 60|
|6|2026-10-18|LAC|45 (74%)|3|2|11|-10|19|128|2|1|3|0|N|3/2/11/19/128 (ev 401873006)|match|Benson 61, Humphrey 61, Smith 61, Suamataia 55, Moore 31|
|7|2026-10-25|SEA|39 (74%)|5|4|21|-3|14|36|0|0|0|0|N|5/4/21/14/36 (ev 401873022)|match|Humphrey 53, Benson 53, Smith 53, Ezeudu 53, Suamataia 53|

- Totals (nflverse, 6 games played): tgt 28, rec 18, rec yds 116, air yds -14, car 120, rush yds 701. OT-only portion: {'tg': 2, 'rec': 1, 'ryd': 22, 'car': 7, 'rush': 29}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Kahlil Benson, LG Kingsley Suamataia, C Creed Humphrey, RG Trey Smith, RT Jaylon Moore
- Unresolved credit differences (preserved, not forced): Wk4: tg E1/N2. Likely causes: nullified/penalty plays, laterals, 2-pt tries, or ESPN stat corrections; not adjudicated.

### Kyren Williams (LA vs LAC) — rushrec · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; sources reconcile
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Kyren_Williams_rushrec.json` · status: active (not on report)
- Sample rule: every 2026 REG game LA has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-10|SF|39 (64%)|3|3|24|7|11|41|1|0|2|0|N|3/3/24/11/41 (ev 401872657)|match|Jackson 61, Avila 61, McClendon 61, Shelton 61, Dotson 59|
|2|2026-09-21|NYG|34 (55%)|2|2|12|5|12|85|1|1|0|0|N|2/2/12/12/85 (ev 401872947)|match|Jackson 62, McClendon 62, Avila 62, Shelton 62, Dotson 62|
|3|2026-09-27|DEN|61 (71%)|7|6|70|44|15|88|0|0|0|2|N|7/6/70/15/88 (ev 401872962)|match|Avila 86, Jackson 86, Shelton 86, McClendon 86, Dotson 85|
|4|2026-10-04|PHI|70 (83%)|13|10|67|46|16|80|2|1|1|0|N|13/10/67/16/80 (ev 401872970)|match|Jackson 84, Avila 84, McClendon 84, Dotson 84, Shelton 84|
|5|2026-10-12|BUF|60 (73%)|8|6|27|1|16|49|1|2|3|3|Y: 1tg/2car|8/6/27/16/49 (ev 401872994)|match|Jackson 82, Avila 82, Shelton 82, Dotson 82, McClendon 82|
|6|2026-10-18|ARI|42 (72%)|6|3|17|3|10|50|0|1|0|1|N|6/3/17/10/50 (ev 401873004)|match|McClendon 58, Avila 58, Dotson 58, Quessenberry 58, Shelton 58|
|7|2026-10-25|LV|37 (51%)|2|2|22|-2|16|99|1|0|1|0|N|2/2/22/16/99 (ev 401873021)|match|Shelton 72, McClendon 72, Avila 69, Jackson 69, Dotson 69|

- Totals (nflverse, 7 games played): tgt 41, rec 32, rec yds 239, air yds 104, car 96, rush yds 492. OT-only portion: {'tg': 1, 'rec': 0, 'ryd': 0, 'car': 2, 'rush': 3}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Alaric Jackson, LG Steve Avila, C Coleman Shelton, RG Kevin Dotson, RT Warren McClendon Jr.
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.

### Parker Washington (JAX vs IND) — recyds · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; sources reconcile
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Parker_Washington_recyds.json` · status: active (not on report)
- Sample rule: every 2026 REG game JAX has played (weeks 1, 2, 3, 4, 5, 6); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|CLE|35 (61%)|6|5|83|102|0|0|1|0|0|0|N|6/5/83/0/0 (ev 401872922)|match|Harrison 57, Pregnon 57, Cleveland 50, Hainsey 50, Lanen 36|
|2|2026-09-20|DEN|48 (81%)|12|7|98|177|0|0|0|0|0|0|N|12/7/98/0/0 (ev 401872940)|match|Cleveland 59, Harrison 59, Pregnon 59, Lanen 59, Hainsey 59|
|3|2026-09-27|NE|50 (81%)|5|3|40|50|0|0|1|3|0|0|N|5/3/40/0/0 (ev 401872957)|match|Harrison 62, Pregnon 62, Hainsey 59, Lanen 59, Cleveland 57|
|4|2026-10-04|CIN|49 (80%)|3|1|7|38|1|3|0|1|0|1|N|3/1/7/1/3 (ev 401872969)|match|Pregnon 61, Harrison 61, Cleveland 61, Hainsey 61, Lanen 61|
|5|2026-10-11|PHI|59 (82%)|9|6|124|79|0|0|2|2|0|0|N|9/6/124/0/0 (ev 401872981)|match|Cleveland 72, Pregnon 72, Lanen 72, Hainsey 72, Harrison 42|
|6|2026-10-18|HOU|52 (73%)|11|4|64|153|0|0|0|2|0|0|N|11/4/64/0/0 (ev 401872996)|match|Pregnon 71, Little 71, Cleveland 71, Lanen 71, Hainsey 71|

- Totals (nflverse, 6 games played): tgt 46, rec 26, rec yds 416, air yds 599, car 1, rush yds 3. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Walker Little, LG Emmanuel Pregnon, C Robert Hainsey, RG Ezra Cleveland, RT Cole Van Lanen
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.

### Puka Nacua (LA vs LAC) — rec · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; sources reconcile
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Puka_Nacua_rec.json` · status: active (not on report)
- Sample rule: every 2026 REG game LA has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-10|SF|43 (70%)|9|5|74|115|0|0|0|1|0|0|N|9/5/74/0/0 (ev 401872657)|match|Jackson 61, Avila 61, McClendon 61, Shelton 61, Dotson 59|
|2|2026-09-21|NYG|DNP/absent|–|–|–|–|–|–|–|–|–|–|N|(none)|missed|Jackson 62, McClendon 62, Avila 62, Shelton 62, Dotson 62|
|3|2026-09-27|DEN|DNP/absent|–|–|–|–|–|–|–|–|–|–|N|(none)|missed|Avila 86, Jackson 86, Shelton 86, McClendon 86, Dotson 85|
|4|2026-10-04|PHI|76 (90%)|12|9|125|136|1|2|1|0|1|1|N|12/9/125/1/2 (ev 401872970)|match|Jackson 84, Avila 84, McClendon 84, Dotson 84, Shelton 84|
|5|2026-10-12|BUF|70 (85%)|24|17|138|184|2|9|1|3|0|2|Y: 3tg/0car|24/17/138/2/9 (ev 401872994)|match|Jackson 82, Avila 82, Shelton 82, Dotson 82, McClendon 82|
|6|2026-10-18|ARI|52 (90%)|7|6|80|60|0|0|0|0|0|1|N|7/6/80/0/0 (ev 401873004)|match|McClendon 58, Avila 58, Dotson 58, Quessenberry 58, Shelton 58|
|7|2026-10-25|LV|61 (85%)|10|8|68|57|2|10|1|3|0|0|N|10/8/68/2/10 (ev 401873021)|match|Shelton 72, McClendon 72, Avila 69, Jackson 69, Dotson 69|

- Totals (nflverse, 5 games played): tgt 62, rec 45, rec yds 485, air yds 552, car 5, rush yds 21. OT-only portion: {'tg': 3, 'rec': 2, 'ryd': 26, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Alaric Jackson, LG Steve Avila, C Coleman Shelton, RG Kevin Dotson, RT Warren McClendon Jr.
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.

### Puka Nacua (LA vs LAC) — recyds · rung 70 @ -290
- **PHASE 1: PASS** — all Phase 1 fields collected; sources reconcile
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Puka_Nacua_recyds.json` · status: active (not on report)
- Sample rule: every 2026 REG game LA has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-10|SF|43 (70%)|9|5|74|115|0|0|0|1|0|0|N|9/5/74/0/0 (ev 401872657)|match|Jackson 61, Avila 61, McClendon 61, Shelton 61, Dotson 59|
|2|2026-09-21|NYG|DNP/absent|–|–|–|–|–|–|–|–|–|–|N|(none)|missed|Jackson 62, McClendon 62, Avila 62, Shelton 62, Dotson 62|
|3|2026-09-27|DEN|DNP/absent|–|–|–|–|–|–|–|–|–|–|N|(none)|missed|Avila 86, Jackson 86, Shelton 86, McClendon 86, Dotson 85|
|4|2026-10-04|PHI|76 (90%)|12|9|125|136|1|2|1|0|1|1|N|12/9/125/1/2 (ev 401872970)|match|Jackson 84, Avila 84, McClendon 84, Dotson 84, Shelton 84|
|5|2026-10-12|BUF|70 (85%)|24|17|138|184|2|9|1|3|0|2|Y: 3tg/0car|24/17/138/2/9 (ev 401872994)|match|Jackson 82, Avila 82, Shelton 82, Dotson 82, McClendon 82|
|6|2026-10-18|ARI|52 (90%)|7|6|80|60|0|0|0|0|0|1|N|7/6/80/0/0 (ev 401873004)|match|McClendon 58, Avila 58, Dotson 58, Quessenberry 58, Shelton 58|
|7|2026-10-25|LV|61 (85%)|10|8|68|57|2|10|1|3|0|0|N|10/8/68/2/10 (ev 401873021)|match|Shelton 72, McClendon 72, Avila 69, Jackson 69, Dotson 69|

- Totals (nflverse, 5 games played): tgt 62, rec 45, rec yds 485, air yds 552, car 5, rush yds 21. OT-only portion: {'tg': 3, 'rec': 2, 'ryd': 26, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Alaric Jackson, LG Steve Avila, C Coleman Shelton, RG Kevin Dotson, RT Warren McClendon Jr.
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.

### Tee Higgins (CIN vs TEN) — recyds · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; sources reconcile
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Tee_Higgins_recyds.json` · status: active (not on report)
- Sample rule: every 2026 REG game CIN has played (weeks 1, 2, 3, 4, 5, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|TB|46 (72%)|6|3|59|117|0|0|0|0|0|0|N|6/3/59/0/0 (ev 401872925)|match|Risner 64, Mims 64, Jr. 64, Karras 64, Fairchild 64|
|2|2026-09-20|HOU|43 (72%)|10|5|95|93|0|0|0|0|0|0|N|10/5/95/0/0 (ev 401872934)|match|Risner 60, Jr. 60, Karras 60, Fairchild 60, Mims 57|
|3|2026-09-27|PIT|53 (93%)|7|6|90|92|0|0|1|1|0|0|N|7/6/90/0/0 (ev 401872950)|match|Risner 57, Mims 57, Jr. 57, Karras 57, Fairchild 57|
|4|2026-10-04|JAX|60 (79%)|16|11|157|219|0|0|0|1|0|0|N|16/11/157/0/0 (ev 401872969)|match|Karras 76, Mims 76, Jr. 76, Fairchild 76, Risner 76|
|5|2026-10-11|MIA|45 (69%)|4|2|22|52|0|0|0|0|0|0|N|4/2/22/0/0 (ev 401872982)|match|Karras 65, Fairchild 65, Jr. 65, Risner 65, Mims 62|
|7|2026-10-25|BAL|46 (87%)|7|6|148|137|0|0|1|1|0|0|N|7/6/148/0/0 (ev 401873012)|match|Fairchild 53, Jr. 53, Karras 50, Mims 50, Risner 50|

- Totals (nflverse, 6 games played): tgt 50, rec 33, rec yds 571, air yds 710, car 0, rush yds 0. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Orlando Brown Jr., LG Dylan Fairchild, C Ted Karras, RG Dalton Risner, RT Amarius Mims
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.

### Tony Pollard (TEN vs CIN) — rushrec · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; sources reconcile
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Tony_Pollard_rushrec.json` · status: active (not on report)
- Sample rule: every 2026 REG game TEN has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|NYJ|26 (52%)|2|1|-1|24|7|35|0|0|0|0|N|2/1/-1/7/35 (ev 401872924)|match|Skoronski 50, Moore 50, Latham 50, Carmona 50, Schlottmann 50|
|2|2026-09-20|PHI|29 (55%)|1|1|1|-7|14|64|0|0|1|0|N|1/1/1/14/64 (ev 401872939)|match|Skoronski 53, Moore 53, Latham 53, Schlottmann 53, Carmona 53|
|3|2026-09-27|NYG|32 (53%)|4|4|22|2|17|74|0|0|1|0|N|4/4/22/17/74 (ev 401872956)|match|Skoronski 60, Moore 60, Latham 60, Schlottmann 60, Slater 59|
|4|2026-10-04|BAL|34 (53%)|4|2|2|-3|16|48|1|0|4|0|N|4/2/2/16/48 (ev 401872973)|match|Skoronski 64, Moore 64, Latham 64, Schlottmann 64, Mafi 64|
|5|2026-10-11|HOU|30 (48%)|1|0|0|10|14|52|0|0|0|0|N|1/0/0/14/52 (ev 401872984)|match|Skoronski 63, Moore 63, Latham 63, Schlottmann 63, Mafi 63|
|6|2026-10-18|IND|35 (76%)|1|0|0|-7|19|76|0|0|0|0|N|1/0/0/19/76 (ev 401873003)|match|Latham 46, Skoronski 46, Moore 46, Mafi 46, Schlottmann 46|
|7|2026-10-25|CLE|47 (75%)|3|3|26|3|25|129|3|0|3|0|N|3/3/26/25/129 (ev 401873013)|match|Skoronski 63, Moore 63, Latham 63, Schlottmann 63, Mafi 63|

- Totals (nflverse, 7 games played): tgt 16, rec 11, rec yds 50, air yds 22, car 112, rush yds 478. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Dan Moore Jr., LG Peter Skoronski, C Austin Schlottmann, RG Atonio Mafi, RT JC Latham
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.

### Trey McBride (ARI vs DAL) — rec · rung 7 @ -225
- **PHASE 1: PASS** — all Phase 1 fields collected; sources reconcile
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Trey_McBride_rec.json` · status: active (not on report)
- Sample rule: every 2026 REG game ARI has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|LAC|60 (80%)|13|9|95|89|0|0|1|4|0|0|N|13/9/95/0/0 (ev 401872926)|match|Johnson 75, Gaines 75, Wilkinson 75, Froholdt 75, Seumalo 72|
|2|2026-09-20|SEA|44 (88%)|10|8|41|36|0|0|1|2|0|0|N|10/8/41/0/0 (ev 401872943)|match|Johnson 50, Adams 50, Seumalo 50, Wilkinson 50, Froholdt 50|
|3|2026-09-27|SF|79 (91%)|11|9|75|57|0|0|0|2|0|0|N|11/9/75/0/0 (ev 401872958)|match|Adams 87, Johnson 87, Seumalo 87, Wilkinson 87, Froholdt 87|
|4|2026-10-04|NYG|64 (97%)|12|7|31|70|0|0|0|1|0|5|N|12/7/31/0/0 (ev 401872966)|match|Seumalo 66, Wilkinson 66, Froholdt 66, Johnson 65, Gaines 38|
|5|2026-10-11|DET|66 (90%)|10|9|66|75|0|0|1|2|0|0|N|10/9/66/0/0 (ev 401872991)|match|Gaines 73, Williams 73, Wilkinson 73, Froholdt 73, Seumalo 72|
|6|2026-10-18|LA|70 (97%)|9|7|53|28|0|0|0|2|0|0|N|9/7/53/0/0 (ev 401873004)|match|Gaines 72, Williams 72, Wilkinson 72, Seumalo 72, Froholdt 72|
|7|2026-10-25|DEN|75 (93%)|13|10|111|106|0|0|1|4|0|0|N|13/10/111/0/0 (ev 401873019)|match|Williams 81, Seumalo 81, Wilkinson 81, Conner 81, Froholdt 81|

- Totals (nflverse, 7 games played): tgt 78, rec 59, rec yds 472, air yds 461, car 0, rush yds 0. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Jayden Williams, LG Isaac Seumalo, C Hjalte Froholdt, RG Jon Gaines II, RT Elijah Wilkinson
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.

### Trey McBride (ARI vs DAL) — recyds · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; sources reconcile
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Trey_McBride_recyds.json` · status: active (not on report)
- Sample rule: every 2026 REG game ARI has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|LAC|60 (80%)|13|9|95|89|0|0|1|4|0|0|N|13/9/95/0/0 (ev 401872926)|match|Johnson 75, Gaines 75, Wilkinson 75, Froholdt 75, Seumalo 72|
|2|2026-09-20|SEA|44 (88%)|10|8|41|36|0|0|1|2|0|0|N|10/8/41/0/0 (ev 401872943)|match|Johnson 50, Adams 50, Seumalo 50, Wilkinson 50, Froholdt 50|
|3|2026-09-27|SF|79 (91%)|11|9|75|57|0|0|0|2|0|0|N|11/9/75/0/0 (ev 401872958)|match|Adams 87, Johnson 87, Seumalo 87, Wilkinson 87, Froholdt 87|
|4|2026-10-04|NYG|64 (97%)|12|7|31|70|0|0|0|1|0|5|N|12/7/31/0/0 (ev 401872966)|match|Seumalo 66, Wilkinson 66, Froholdt 66, Johnson 65, Gaines 38|
|5|2026-10-11|DET|66 (90%)|10|9|66|75|0|0|1|2|0|0|N|10/9/66/0/0 (ev 401872991)|match|Gaines 73, Williams 73, Wilkinson 73, Froholdt 73, Seumalo 72|
|6|2026-10-18|LA|70 (97%)|9|7|53|28|0|0|0|2|0|0|N|9/7/53/0/0 (ev 401873004)|match|Gaines 72, Williams 72, Wilkinson 72, Seumalo 72, Froholdt 72|
|7|2026-10-25|DEN|75 (93%)|13|10|111|106|0|0|1|4|0|0|N|13/10/111/0/0 (ev 401873019)|match|Williams 81, Seumalo 81, Wilkinson 81, Conner 81, Froholdt 81|

- Totals (nflverse, 7 games played): tgt 78, rec 59, rec yds 472, air yds 461, car 0, rush yds 0. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Jayden Williams, LG Isaac Seumalo, C Hjalte Froholdt, RG Jon Gaines II, RT Elijah Wilkinson
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.

### Tyler Warren (IND vs JAX) — recyds · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; sources reconcile
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Tyler_Warren_recyds.json` · status: active (not on report)
- Sample rule: every 2026 REG game IND has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|BAL|50 (93%)|5|3|13|23|0|0|1|1|0|0|N|5/3/13/0/0 (ev 401872659)|match|Goncalves 54, Travis 54, Bortolini 54, Nelson 54, Raimann 54|
|2|2026-09-20|KC|58 (89%)|7|6|21|-13|1|3|1|2|0|1|Y: 0tg/0car|7/6/21/1/3 (ev 401872945)|match|Travis 65, Goncalves 65, Bortolini 65, Nelson 65, Raimann 65|
|3|2026-09-27|HOU|67 (94%)|10|9|55|28|1|2|0|0|0|0|N|10/9/55/1/2 (ev 401872951)|match|Goncalves 71, Travis 71, Raimann 71, Bortolini 71, Nelson 71|
|4|2026-10-04|WAS|56 (85%)|5|5|41|21|0|0|0|0|0|0|N|5/5/41/0/0 (ev 401872965)|match|Goncalves 66, Travis 66, Bortolini 66, Nelson 63, Raimann 59|
|5|2026-10-11|PIT|67 (94%)|9|7|83|86|1|1|1|1|1|0|N|9/7/83/1/1 (ev 401872985)|match|Goncalves 71, Raimann 71, Nelson 71, Bortolini 71, Travis 67|
|6|2026-10-18|TEN|DNP/absent|–|–|–|–|–|–|–|–|–|–|N|(none)|missed|Travis 83, Goncalves 83, Raimann 83, Bortolini 83, Nelson 83|
|7|2026-10-25|MIN|DNP/absent|–|–|–|–|–|–|–|–|–|–|N|(none)|missed|Travis 61, Goncalves 61, Raimann 61, Nelson 61, Bortolini 61|

- Totals (nflverse, 5 games played): tgt 36, rec 30, rec yds 213, air yds 145, car 3, rush yds 6. OT-only portion: {'tg': 0, 'rec': 0, 'ryd': 0, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Bernhard Raimann, LG Jalen Farmer, C Tanor Bortolini, RG Matt Goncalves, RT Jalen Travis
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.

### Zay Flowers (BAL vs BUF) — rec · rung None @ None
- **PHASE 1: FAIL** — exact placed Ticket 2 market (off-limits)
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Zay_Flowers_rec.json` · status: active (not on report)
- Sample rule: every 2026 REG game BAL has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|IND|20 (29%)|6|5|150|91|0|0|1|0|0|0|N|6/5/150/0/0 (ev 401872659)|match|Simpson 68, Rosengarten 68, Ioane 68, Stanley 68, Gwyn 68|
|2|2026-09-20|NO|DNP/absent|–|–|–|–|–|–|–|–|–|–|N|(none)|missed|Rosengarten 58, Simpson 58, Ioane 58, Gwyn 58, Stanley 46|
|3|2026-09-27|DAL|21 (33%)|6|5|84|55|1|20|0|2|0|2|N|6/5/84/1/20 (ev 401872960)|match|Vinson 64, Rosengarten 64, Ioane 64, Simpson 64, Gwyn 46|
|4|2026-10-04|TEN|47 (73%)|10|8|118|78|0|0|1|2|0|0|N|10/8/118/0/0 (ev 401872973)|match|Simpson 64, Rosengarten 64, Ioane 64, Stanley 62, Jones 36|
|5|2026-10-11|ATL|62 (82%)|9|8|53|43|1|13|0|1|0|1|Y: 2tg/0car|9/8/53/1/13 (ev 401872993)|match|Simpson 76, Jones 76, Ioane 76, Stanley 76, Rosengarten 74|
|6|2026-10-18|CLE|50 (88%)|11|6|66|106|1|1|0|0|0|0|N|11/6/66/1/1 (ev 401872997)|match|Rosengarten 57, Ioane 57, Jones 57, Simpson 57, Stanley 56|
|7|2026-10-25|CIN|57 (85%)|11|8|137|62|0|0|1|2|0|0|N|11/8/137/0/0 (ev 401873012)|match|Rosengarten 67, Simpson 67, Jurgens 67, Stanley 67, Jones 51|

- Totals (nflverse, 6 games played): tgt 53, rec 40, rec yds 608, air yds 435, car 3, rush yds 34. OT-only portion: {'tg': 2, 'rec': 2, 'ryd': 7, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Ronnie Stanley, LG John Simpson, C Cam Jurgens, RG Olaivavega Ioane, RT Roger Rosengarten
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.

### Zay Flowers (BAL vs BUF) — recyds · rung None @ None
- **PHASE 1: PASS** — all Phase 1 fields collected; sources reconcile
- Leg file: `/workspace/nfl-database/week8/betguru_2026-11-01_raw/leg_Zay_Flowers_recyds.json` · status: active (not on report)
- Sample rule: every 2026 REG game BAL has played (weeks 1, 2, 3, 4, 5, 6, 7); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.

|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|2026-09-13|IND|20 (29%)|6|5|150|91|0|0|1|0|0|0|N|6/5/150/0/0 (ev 401872659)|match|Simpson 68, Rosengarten 68, Ioane 68, Stanley 68, Gwyn 68|
|2|2026-09-20|NO|DNP/absent|–|–|–|–|–|–|–|–|–|–|N|(none)|missed|Rosengarten 58, Simpson 58, Ioane 58, Gwyn 58, Stanley 46|
|3|2026-09-27|DAL|21 (33%)|6|5|84|55|1|20|0|2|0|2|N|6/5/84/1/20 (ev 401872960)|match|Vinson 64, Rosengarten 64, Ioane 64, Simpson 64, Gwyn 46|
|4|2026-10-04|TEN|47 (73%)|10|8|118|78|0|0|1|2|0|0|N|10/8/118/0/0 (ev 401872973)|match|Simpson 64, Rosengarten 64, Ioane 64, Stanley 62, Jones 36|
|5|2026-10-11|ATL|62 (82%)|9|8|53|43|1|13|0|1|0|1|Y: 2tg/0car|9/8/53/1/13 (ev 401872993)|match|Simpson 76, Jones 76, Ioane 76, Stanley 76, Rosengarten 74|
|6|2026-10-18|CLE|50 (88%)|11|6|66|106|1|1|0|0|0|0|N|11/6/66/1/1 (ev 401872997)|match|Rosengarten 57, Ioane 57, Jones 57, Simpson 57, Stanley 56|
|7|2026-10-25|CIN|57 (85%)|11|8|137|62|0|0|1|2|0|0|N|11/8/137/0/0 (ev 401873012)|match|Rosengarten 67, Simpson 67, Jurgens 67, Stanley 67, Jones 51|

- Totals (nflverse, 6 games played): tgt 53, rec 40, rec yds 608, air yds 435, car 3, rush yds 34. OT-only portion: {'tg': 2, 'rec': 2, 'ryd': 7, 'car': 0, 'rush': 0}. Regulation = totals minus OT.
- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): LT Ronnie Stanley, LG John Simpson, C Cam Jurgens, RG Olaivavega Ioane, RT Roger Rosengarten
- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.