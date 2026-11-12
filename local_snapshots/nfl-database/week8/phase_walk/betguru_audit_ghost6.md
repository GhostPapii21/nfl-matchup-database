# BetGuru audit of Ghost6 consensus points — Sat Oct 31, 2026, ~7:55 PM ET
Re-run folder (new): `runs/betguru_audit_20261031T195019/` (bg_sim_v4.py, legs_audit.json, sims_v4.json, SHA256SUMS). Locked run `runs/betguru_20261031T194324/` untouched (note: it **does exist**; Ghost6's consensus says it was not found). Seeds unchanged (20261101 + md5 offset), N=100,000 × 3. FD prices/no-vig: 7:37 PM ET snapshot. Uncalibrated; nothing placed or posted; no keys printed.

## 1) Shrink-30 — REAL DIFFERENCE (our method was not the rule)
Ours shrank the per-play **yards** 30% toward the league position mean and re-simmed. Count markets (Puka receptions) have no per-play yards, so Puka came out unchanged at +5.1 — that's why. The rule is a probability shrink: p' = 0.5 + 0.7·(p − 0.5), then p' − no-vig. Our phase-10G "shrink-30" column is withdrawn and replaced below.

## 2) Rushing YPC — REAL BUG (unregressed)
v3 bootstrapped each RB's own carries (Gibbs 4.63, Cook 5.36, Walker 5.84 YPC on 117–134 carries) and applied only a 50%-shrunk, RB-only opponent factor. v4: regress player YPC toward league (4.17, all rushes) with k=100 carries, w=n/(n+100), then apply the full opponent YPC allowed (all rushes, 2026 pbp): MIN 4.16, BAL 3.80 (≈ your 3.82), DEN 4.57. The bootstrap is rescaled to the target mean, so its shape is kept. I couldn't reproduce the "MIN edge runs 2.26" figure from pbp (MIN allows left 5.4 / middle 2.8 / right 3.1), so I used MIN overall 4.16 — GAP noted.
| RB | FD main | v3 median MC/bias/GR | v4 median MC/bias/GR | v4 MC − main | YPC path |
|---|---|---|---|---|---|
| Gibbs | 87.5 | 100.2 / 87.6 / 97.2 | 96.5 / 84.4 / 93.7 | +9.0 | 4.63 on 134 car → w 0.57 → opp 4.16 → target 4.42 |
| Cook | 82.5 | 96.6 / 83.6 / 94.7 | 82.5 / 71.4 / 80.9 | +0.0 | 5.36 on 117 car → w 0.54 → opp 3.80 → target 4.38 |
| Walker | 85.5 | 107.9 / 93.7 / 105.9 | 99.2 / 86.1 / 97.3 | +13.7 | 5.84 on 120 car → w 0.55 → opp 4.57 → target 5.57 |
Cook now matches the market; Gibbs is still ~9 over and Walker ~14 over (volume of ~19–23 carries, not YPC, drives the rest; Ghost6 also has Walker ~100).

## 3) GR mean shift — NOT A CURRENT BUG (it was fixed in v2)
GR volume is rescaled to the MC weighted mean (`TV *= mean/(m_s·E[TV])`), and share and team volume are drawn independently, so E[GR volume] = E[MC volume]. Evidence, means MC vs GR:
| Leg | v3 MC mean | v3 GR mean | v4 MC mean | v4 GR mean |
|---|---|---|---|---|
| Jahmyr Gibbs | 103.7 | 103.7 | 99.9 | 99.9 |
| James Cook | 100.3 | 100.2 | 85.7 | 85.6 |
| Kenneth Walker III | 117.5 | 117.2 | 107.9 | 107.7 |
| Puka Nacua | 9.8 | 9.8 | 9.8 | 9.8 |
| Tee Higgins | 104.4 | 103.9 | 104.4 | 103.9 |
GR medians sit 1–3 below MC because GR is wider and right-skewed, not because the mean moved. The v1 mean inflation (Walker GR median 118 vs 104) was the real bug, and it was fixed before the card. No change made.

## 4) Re-run edges — one rule: raw edge ≥ +3 and shrink-30 edge > 0
| Leg | Version | FD | No-vig | MC/Bias/GR | Avg | Edge | p' | Shrink edge | Result |
|---|---|---|---|---|---|---|---|---|---|
| Gibbs 70+ rush | v3 old | -250 | 0.673 | 0.812/0.701/0.750 | 0.754 | +8.1 | 0.678 | +0.5 | PASS |
| Gibbs 70+ rush | v4 fixed | -250 | 0.673 | 0.786/0.668/0.723 | 0.726 | +5.3 | 0.658 | -1.5 | FAIL |
| Cook 70+ rush | v3 old | -210 | 0.638 | 0.774/0.654/0.736 | 0.722 | +8.4 | 0.655 | +1.7 | PASS |
| Cook 70+ rush | v4 fixed | -210 | 0.638 | 0.661/0.518/0.625 | 0.601 | -3.7 | 0.571 | -6.7 | FAIL |
| Walker 80+ rush | v3 old | -144 | 0.556 | 0.730/0.616/0.688 | 0.678 | +12.2 | 0.625 | +6.9 | PASS |
| Walker 80+ rush | v4 fixed | -144 | 0.556 | 0.676/0.552/0.640 | 0.623 | +6.7 | 0.586 | +3.0 | PASS |
| Puka 8+ rec | v3 old | -138 | 0.542 | 0.622/0.531/0.626 | 0.593 | +5.1 | 0.565 | +2.3 | PASS |
| Puka 8+ rec | v4 fixed | -138 | 0.542 | 0.622/0.531/0.626 | 0.593 | +5.1 | 0.565 | +2.3 | PASS |
| Higgins 60+ yds (BARRED, reference) | v3 old | -186 | 0.613 | 0.748/0.652/0.750 | 0.716 | +10.3 | 0.652 | +3.9 | PASS |
| Higgins 60+ yds (BARRED, reference) | v4 fixed | -186 | 0.613 | 0.748/0.652/0.750 | 0.716 | +10.3 | 0.652 | +3.9 | PASS (but BARRED) |

## Bottom line
- **Pass:** Walker 80+ (−144): v4 avg .623, +6.7 raw / +3.0 after shrink. Puka 8+ (−138): .593, +5.1 / +2.3.
- **Fail:** Gibbs 70+ (−250): +5.3 raw but −1.5 after shrink. Cook 70+ (−210): −3.7.
- **Higgins 60+:** +10.3 / +3.9, but barred (same Alt Receiving Yds market as the open SGP's 50+). Reference only.
- **We now agree with Ghost6's two-leg consensus**: Walker 80+ and Puka 8+, ≈ +192 (1.694 × 1.725). Our v4 Walker average (.623) now equals Ghost6's.
- Caveat: Walker's median is still ~14 yds above the FD main (85.5). Treat it as CAUTION, recheck inactives (KC RB split), and reprice on a 20-cent move.
