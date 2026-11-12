# Pressure / Charbonnet / Darnold U / Barner — CHI@SEA MNF 2026-11-02 (fixed-model, copies only)
Written ~8:45 AM ET. Odds: The Odds API pulled 8:35 AM ET (odds_p0835.csv; book stamps 8:30 AM ET) -> STALE after 9:35 AM ET. Sims: sims.py, s2.py (tools/sim_v6_fix unedited, 3x100k, seed 20261101, SEA -3). Pressure input: Ghost6's numbers (../../2026-11-02_SEA_CHI_ghost6/src, read-only). NOT VETTED.

## 1. Charbonnet workload + Wilson rush O19.5
- Macdonald (seahawks.com, Emerald City Spectrum, Oct 31): "We have a plan for Zach"; he plays on a "pitch count". No snap or carry number given. He also called Charbonnet's pass pro "as good as they get" and said he can be a three-down back (Yahoo/SBR recap).
- Comps: Breece Hall 2023 Wk1 (ACL): 17 snaps, 10 car-127, pitch count, Cook got 13 car (nfl.com, CBS). Josh Jacobs 2026: 52% snaps, 11-36. Not verified this turn (from memory): Dobbins 2022 Wk3 ~7 car, James Robinson 2022 Wk1 ~11 car. Range: 7-11 carries, about 25-50% snaps.
- CHI rushing allowed 2026 Wk1-7 pbp, no scrambles: 4.19 YPC (n=129). Non-QB rushers: 4.31. Rico's ~4.0 roughly holds (a bit higher).
- Wilson O19.5, FD -113/-113, no-vig .500. Each cell is p (median):
| Scenario | MC | Bias | GR | avg | raw | G6 30% shrink | x0.7 |
|---|---|---|---|---|---|---|---|
| base | .950 (64) | .998 (76) | .915 (64) | .954 | +45.4 | +31.8 | +31.8 |
| Charb capped, W 45% RB car | .868 (44) | .970 (53) | .831 (44) | .890 | +39.0 | +27.3 | +27.3 |
| Charb capped, W 40% | .826 (40) | .945 (47) | .791 (39) | .854 | +35.4 | +24.8 | +24.8 |
| Charb full, W 35% | .773 (34) | .900 (40) | .738 (34) | .804 | +30.4 | +21.3 | +21.3 |
- Verdict: STILL CUT, unchanged. Every median is 20-56 yds over a 19.5 line, so it's MODEL-SUSPECT. The book prices Wilson at ~5-7 carries. §7 actuals with Darnold, Wk4-7: 81/61/52/100 yds on 21/20/14/24 carries = 4/4, so §7 passes. But he never had Charbonnet behind him. But the committee gate fails (60% carry share in only 2 of the last 4 games). Press/manual review isn't live until 11-05. The new SNF rule (1) covers model-suspect UNDERS only.
- The capped scenario helps the thesis, but the model can't see what the market sees. With Price possibly active and Holani in the mix, a 3-4 back split is likely. If Price is activated at 4 PM: .663/.787/.640, still flagged.

## 2. Darnold pass yds U238.5 (FD -113/-113; DK 236.5 -111/-113)
- Models, P(over 238.5) -> under: MC .517 (med 245) -> U .483; Bias .575 (261) -> .425; GR .566 (259) -> .434. Avg U .447. No-vig .500, raw -5.3, after G6 shrink -3.7, so it misses the +3 bar.
- Pressure adjustment (post-hoc, approximate). Ghost6: pressured 3.9 Y/DB vs clean 8.5. If CHI pushes his proxy pressure rate from ~38% to 45%, Y/DB x0.95, so medians drop ~12 to ~233-249. That gives an under p of ~.50-.53, a raw edge of 0 to +3, and after shrink 0 to +2. Still under the bar.
- FD alts are overs only (199.5 -310, 224.5 -166, 249.5 +114). No under alt is posted.
- §7, last 4 with Darnold: 168, 195, 278, 257 = 2/4 under. FAIL.
- Rico's claim: in 11+ sack+hit games he threw 168 (LAC) and 195 (SF), but 278 vs DEN (20 sk+hit, 57 dropbacks while trailing). Per-game corr (pass yds vs sk+hit) = +0.22. Under pressure the volume goes UP when SEA trails, so the claim is 2 of 3, not a rule.
- Context: total 46.5, SEA -3. Shaheed OUT, Cross OUT (Josh Jones at LT).
- Verdict: CUT (§7 2/4, below bar).

## 3. Barner receptions (FD 3.5 +126/-168, overround 1.069; alts 1.5 -670, 2.5 -210, 4.5 +265)
| Rung | MC | Bias | GR | avg | nv | raw | shrink |
|---|---|---|---|---|---|---|---|
| 2.5 (-210) | .581 | .488 | .545 | .538 | .633 | -9.5 | -10.7 |
| 3.5 (+126) | .361 | .273 | .370 | .335 | .414 | -7.9 | -2.9 |
| 4.5 (+265) | .193 | .130 | .236 | .186 | .257 | -7.1 | |
- Medians: 2.9 / 2.5 / 2.8 receptions.
- §7, Wk4-7 receptions 1, 3, 3, 4: 3.5 is 1/4 FAIL, 2.5 is 3/4 pass.
- Named defender: not done this turn, so P4 is MISSING.
- Pressure does shift targets to him: Ghost6 has 31% of pressured targets vs 9% clean; BetGuru's FTN has 28% when blitzed vs 8%. But it's all short (~2 aDOT, 6/15 for 60 yds). The models already miss the price.
- Verdict: CUT.

## 4. Gate notes
- Kupp (WR3) overs: CHI corners out not verified as 2+, and he's 15% of pressured targets. Exception not shown, so banned.
- JSN: share falls when pressured (19% vs 40%). Pressure is a headwind for JSN 100+ and the receptions over.
- SGP conflict: a Darnold under and JSN 100+ are negatively correlated, since JSN is ~36-40% of his yards. Don't pair them.
