# ESPN Week 8 inputs (attributed to ESPN, Fantasy Playbook + WR/CB cheat sheet, pulled 2026-10-29)
These are ESPN's numbers, used as inputs only.

## The only projected shadow (ESPN "S" flag)
- TEN Carnell Tate vs CIN DJ Turner II, about 3/4 of routes. ESPN calls it a downgrade (shadowed WRs scored 8.8 PPG). Our coverage file already had Turner as TOUGH, so the model median stays as is. The leans are flagged CAUTION (rec 4+ −250, yds 40+ −220).
- NE@MIA: ESPN calls a Gonzalez shadow on Caleb Douglas *possible*, not flagged. We have no bet there already.

## CAR@GB: changes from ESPN alignment (charted route alignment beats our target-side proxy)
- McMillan routes are L38/S31/R31. Mixed defenders: Cisse (RCB 100%, 0.40 FP/route allowed), Bullard, and Nixon. We had assumed mostly Nixon. Median 76→79 rec yds, rec 5.9→6.0. Still a pass.
- Coker is S45 vs Bullard (0.23 FP/route). We had assumed Cisse/soft. Rec yds 61→56, rec 4.7→4.4. NEW LEAN under 62.5 (P 0.67 vs 0.50); rec u4.5 borderline (0.60 vs 0.44).
- Savion is S59 vs Moehrig (0.10 FP/route). Rec yds 25→22, rec 2.4→2.2. Under 2.5 rec gets stronger (0.70 vs 0.47).
- Watson is R37 vs Will Lee (0.28, neutral). No change. Risk: ESPN projects 23% target share vs our 20%.
- Golden's primary CB (Evans) is OUT. This matches our soft read.

## Sunday coverage matchups where ESPN's primary defender differs from ours (coverage.json now has an `espn` field per receiver; backup is coverage.pre_espn.json)
- Supports our leans: Malik Washington (vs slot Marcus Jones 0.48, not Gonzalez), Lamb (vs Burke, not G. Williams), Nacua (vs Donte Jackson 0.50), Shakir (Keyon Martin 0.37), Pickens (Melton 0.32).
- Cuts against our leans (flag only, medians unchanged): Egbuka o4.5 rec (vs A.J. Terrell 0.23, not Hughes/soft), Antonio Williams o32.5 (vs Quinyon Mitchell 0.25, not Woolen), Diggs u4.5 rec (vs DeJean 0.39, softer than we had). McConkey u (vs Josh Wallace 0.21, not J. Watson) is still tough, so the lean holds.
