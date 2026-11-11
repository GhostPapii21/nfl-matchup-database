# Henry vs JAX run D, JAX explosive passes, Fagnano drive read (2026-11-04 ~8:10 AM ET). ESTIMATES marked.
Raw output: hd_raw.txt, drive_sim.txt; code drive_sim.py. Source: nflverse 2026 pbp (wks1-8), ESPN roster/injury JSON.
## Box-score check vs pbp
All 7 match on the numbers given, except: IND pbp team passing 21/30 152, 4 sacks (D.Jones' own 19/28 144 2 INT 3 sk is consistent; backup took the rest). CLE: Watson also ran 6-38 (team rush 22-87 includes it). CIN Brown had 11 tgt/11 rec. JAX had a Wk7 bye; 7 games.
## Run D
JAX allows 3.25 YPC on designed runs (lg 3.95, -18%); 10+ run rate 7.5% (lg 9.1%). Every lead back ran below his own ex-JAX YPC except Dobbins (+0.4) and Marks (+0.3):
Taylor 8-23 2.88 vs 4.19 own (−1.31; one 19-yd run); Judkins 2.75 vs 3.47; Stevenson 3.14 vs 3.88; Henderson 2.88 vs 4.09; C.Brown 1.11 vs 3.88; Pierce 1.27 vs 3.15; Coleman 3.9 vs 4.75. Taylor's 4.19 is ordinary, so the JAX game was partly Taylor too, but every back fell short.
Gaps: JAX's leak = left tackle 6.25 (12 att); stout middle 3.02 (46), left/right guard 2.8-3.0, right tackle 3.45. Henry: best LT 4.80, RE 4.61; middle 3.05, LG 2.56. LT overlap is the one path.
Henry 2026: 159-634, 3.99 YPC, 15 runs of 10+, 3 of 20+, 31 stuffs (≤0). Week-by-week: 144/68/89/73/104/58/45/53; last three 2.65-4.82. Leading 3.85 / trailing 4.13 YPC. With Huntley 3 g 59-207 (3.5); with Fagnano wk8 11-53.
Front: Hines-Allen DE (20 run tackles, 3 TFL), Oluokun LB 22, V.Miller LB 21, Hamilton DT 11 (IR), A.Johnson DT 10, Armstead DT 9. Questionable: Travon Walker DE, Branson Combs LB. NGS box-count/RYOE and PFR not fetched (PFR returned a 5 KB block page) → gap.
Henry projection (ESTIMATE: resampled own carries ×0.90 for JAX):
base 14 car/50 yds: >49.5 46%, >59.5 29%, >69.5 17% (U69.5 83%); long median 10, P(15+) 29%.
Rico 3&out case 12/43: U69.5 90%. flip 18/66: >49.5 74%, >69.5 41%.
## Explosive passes allowed (21 of 20+ in 7 g)
Deep right 8, deep middle 4, deep left 3, short (YAC) 6. Deep middle 30.5 Y/A (6 att), deep right 15.6 Y/A. 80+ receivers: Waddle 138, Higgins 157, Noel 107, Hollins 87, Meyers 82. Defender not named in pbp (gap).
BAL fit: Flowers (deep middle/YAC) and Bateman (deep right; his 22-yd catch wk8 was deep right) fit. Lane/Hill are short. Fagnano threw deep twice in wk8.
## Drive sim (ESTIMATE)
JAX by down: sack% 7.3/2.0/6.0; QB-hit 13.5/11.1/23.9% (3rd-down hit rate doubles: supports Rico). Cmp% allowed 3rd down 52%. Fagnano 3rd down 3/8 37, 1 sk; 5 of his 10 drives had 0 first downs. JAX opp 3&out 28%; BAL 34%.
base (42% 3&out): 10.5 drives, 4.4 3&outs, 1.5 TO, 56 plays, 16.0 pts (sim runs above the yaml's 13.4 TT).
Rico (50% 3&out, 17% TO): 11 drives, 5.5 3&outs, 1.9 TO, 13.5 pts, P(<13.5) 54%.
flip: 3.5 3&outs, 20 pts.
"Jacoby Lane" = Ja'Kobi Lane, WR #6 (14 tgt 9-89 season; 1-13 from Fagnano).
Targets (base / Rico): Hill 4.6/4.9 tgt, 3.1/3.3 rec, 17-18 yds (o1.5 rec 82%, o2.5 61%, o14.5 yds 43%); Bateman 3.4 tgt 2.0 rec 26 yds (o1.5 60%, o14.5 56%, o16.5 52%); Lane 2.6 tgt 1.7 rec 16 (o1.5 50%); Flowers 6.9 tgt 4.0 rec 44 (u4.5 rec 63%); Andrews 4.0 tgt 2.6 rec 18 (u18.5 64%).
JAX side: BAL plays stay ~55-56 in every case; more short drives offset by more drives. JAX at 64 plays holds; Rico case adds maybe +1-2 JAX plays and a shorter field from 1.9 TO (estimate). No rerun of Lawrence/Washington/Strange needed.
## Lines
Saved: Henry rush 69.5 (FD -114/-114, DK u -114, Pinnacle 70.5 u-118); Bateman rec 1.5 (DK o-110, FD o-106), yds 14.5 (DK/FD), Pinnacle 16.5 o-107; Flowers rec 4.5 (FD u-172, DK u-140, Pinnacle u-160); Andrews yds 18.5 (FD). Needed: Hill and Lane props, Henry alt rushing lines/longest rush, BAL TT, Fagnano INT/sacks, JAX D sacks.
