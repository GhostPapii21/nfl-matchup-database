# Slip vet — Rico FD SGP, CHI@SEA MNF 2026-11-02 (Tag: fixed-model, copies only). NOT VETTED by Ghost6.
Sim: tools/sim_v6_fix via slip_vet/sims.py (subclass scales target column only; engine unedited), MC/Bias/GR x 100k, seed 20261101, SEA -3. Raw: raw_sims.json.
Odds: The Odds API FanDuel, pulled 8:25 AM ET (odds_m0825.csv, 0 in-play rows). Fresh until 9:25 AM ET.
No-vig = alt implied / main-market overround (Loveland rec 4.5 +116/-154 → 1.069; JSN rec 7.5 +106/-140 → 1.069; Kupp yds 29.5 & Burden yds 51.5 -113/-113 → 1.061).
Edges in pp: raw = avg p − nv; G6 = 0.5+0.7(p−0.5) − nv; x0.7 = 0.7·raw. Shaheed-OUT boosts x1.07/x1.144 (loeb_followups) applied to JSN and Kupp.
§7 from src/play_by_play_2026.parquet (Darnold Wk4-7; Caleb Wk1,2,6,7).

| Leg | FD alt | nv | MC/Bias/GR p (med) | raw | G6 | x0.7 | §7 | Opportunity | Defender | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| Loveland 3+ rec (O2.5) | -490 | .777 | .599/.545/.576 (3/3/3) | -20.3 | -22.5 | -14.2 | 2/4 (0,1,6,7) FAIL | mixed (tgt 6.5/g wtd, 0-1 rec Wk1-2) FAIL | SEA TE defender not mapped → MISSING; SEA allows 4.7 TE rec/g, 34.4 ypg (stingy) | CUT |
| Kupp 15+ yds (O14.5) base | -390 | .750 | .733/.636/.747 (30/24/31) | -4.5 | -10.6 | -3.1 | 3/4 (13,15,50,20) PASS | tgts 2,3,10,2 → mixed FAIL; #3 SEA WR/TE target earner (JSN .318, Barner .15) → WR3 over ban (CHI not missing 2 CBs) | — | CUT |
| Kupp 15+ x1.07 / x1.144 | -390 | .750 | .752/.655/.770 ; .767/.673/.793 | -2.4 / -0.6 | -9.2 / -7.9 | -1.7 / -0.4 | same | same | — | CUT |
| JSN 6+ rec (O5.5) base | -320 | .713 | .770/.679/.724 (8/7/8) | +1.1 | -5.6 | +0.8 | 2/4 (5,5,12,9) FAIL | PASS: tgts 6,8,16,12 (5+ in 3/4); 11.5 wtd tgt/g; no teammate ≥28% | Muhammad (Q) 54.8% comp allowed → catches-over CAUTION | CUT |
| JSN 6+ x1.07 | -320 | .713 | .812/.725/.766 (8/8/8) | +5.5 | -2.6 | +3.8 | FAIL | PASS | caution | CUT |
| JSN 6+ x1.144 | -320 | .713 | .847/.766/.801 (9/8/9) | +9.2 | 0.0 (not >0) | +6.4 | FAIL | PASS | caution | CUT (closest; §7 + shrunk edge fail) |
| Burden 30+ yds (O29.5) | -420 | .761 | .789/.759/.772 (53/49/53) | +1.2 | -7.0 | +0.8 | 4/4 (63,32,95,130) PASS | PASS (6.1 wtd tgt/g, co-leader 24 tgts w/ Caleb) | SEA slot allows fewest slot catches (4.5/g, Loeb) — defender per burden_yds.md | CUT on price (< +3); true lean, no edge |

Note: Burden main has moved to 51.5 (was ~47 earlier). JSN main receptions 7.5 (+106/-140).

## Correlation / SGP context
- JSN 6+ rec and JSN 100+ yds are strongly positively correlated (same player; at JSN's ~13-15 ypc, 100+ yds almost always comes with 6+ catches — 3 of his 3 Darnold 100-yd games had 5,12,9 rec, so not strictly nested). Same-player different-stat stack → flag for Rico; FD SGP prices the correlation in, so stacking adds little value.
- Rico's slip (7 legs): Swift 50+ rush+rec (passed §7 4/4 per Ghost6), Loveland 3+ (CUT), Kupp 15+ (CUT, WR3 ban/mixed volume), JSN 6+ (CUT, §7 2/4), JSN ATD (pulled earlier: book .51 vs models .36-.42), Burden 30+ (lean, no edge at -420), E. Wilson O19.5 rush (CUT, RB committee). None of the 4 vetted legs clears. Positive correlations within slip: JSN legs (rec/ATD); Swift & Burden both CHI pass-game. Negative: Wilson rush vs JSN volume mildly.
- Low-rung legs (-390 to -490) add little payout while adding fail risk; 7-leg / $125 stake exceeds 3-4 leg cap and $100 bankroll.
