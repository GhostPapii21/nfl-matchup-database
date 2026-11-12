# BetGuru — PHASE 7 — NGS AND ANALYTICS CHECKS
Written Oct 31, 2026, ~7:55 PM ET. Source: nflverse NGS parquets (season rows, week=0, 2026) + nflverse pbp 2026 (sha e61a4040…). Receiving legs: **PFR cache Oct 29 (fresh pull 403)**.

## 7A Team EPA/play (pbp pass+run, both teams per game; rank of 32)
| Game | Offense EPA (rank) | Defense EPA allowed (rank) |
|---|---|---|
| MIN@DET | DET +.140 (4) / MIN −.096 (29) | DET +.134 (31) / **MIN −.193 (1)** |
| BAL@BUF | BUF +.204 (1) / BAL +.081 (8) | BUF +.128 (29) / BAL +.011 (17) |
| KC@DEN | KC +.118 (5) / DEN −.041 (22) | KC −.056 (6) / DEN −.049 (7) |
| TEN@CIN | CIN +.109 (7) / TEN −.135 (31) | CIN −.041 (10) / TEN +.057 (24) |
| LAC@LAR | LA +.059 (9) / LAC −.225 (32) | LA −.057 (5) / LAC −.036 (12) |
| ARI@DAL | DAL +.114 (6) / ARI −.034 (19) | DAL +.138 (32) / ARI +.095 (27) |
| IND@JAX | JAX +.155 (3) / IND −.068 (27) | JAX −.036 (13) / IND +.048 (22) |
| PHI@WSH | WAS −.014 (18) / PHI −.116 (30) | WAS +.067 (25) / PHI +.112 (28) |
| CLE@PIT | PIT −.048 (25) / CLE −.050 (26) | PIT −.044 (8) / CLE −.037 (11) |

## 7B RB NGS (rush att, % vs 8+ box, RYOE/att, efficiency, time to LOS)
| RB | Att | 8+ box | RYOE/att | Eff | TLOS |
|---|---|---|---|---|---|
| Gibbs | 134 | 18.7% | +0.56 | 4.00 | 2.90 |
| Cook | 117 | 23.1% | +0.93 | 3.17 | 2.53 |
| Walker | 120 | 25.0% | **+2.26** | 3.24 | 2.80 |
| Tuten | 94 | 14.9% | +0.08 | 4.73 | 2.99 |
| Javonte | 110 | 18.2% | +0.38 | 3.45 | 2.78 |

## 7C Receiver NGS (targets, separation, cushion, aDOT, YAC+/exp, air-yard share)
| WR/TE | Tgt | Sep | Cush | aDOT | YAC+ | AY share |
|---|---|---|---|---|---|---|
| Puka | 62 | 2.90 | 6.39 | 8.9 | +1.94 | 25.5% |
| Lamb | 81 | 2.86 | 6.49 | 11.0 | +0.19 | 40.8% |
| Higgins | 50 | 2.43 | 5.54 | 14.2 | +1.32 | 43.8% |
| St. Brown | 68 | 2.77 | 6.69 | 8.8 | −0.39 | 32.4% |
| Metcalf | 58 | 2.48 | 4.41 | 11.8 | +0.31 | 39.8% |
| Flournoy | 40 | 3.14 | 6.75 | 7.3 | +1.41 | 13.3% |
| A. Williams | 26 | 3.21 | 7.03 | 12.0 | +0.29 | 17.8% |
Gibbs receiving: not NGS-qualifying → GAP.

## 7D QB context (TTT, aggressiveness, IAY, CPOE)
Goff 2.84/20.2%/8.4/+1.7 · Allen 2.97/12.9/8.7/+2.4 · Mahomes 2.79/6.8/6.2/−2.1 · Burrow 2.64/13.2/7.6/+5.2 · Stafford 2.73/14.4/7.9/+2.0 · Prescott 2.78/21.2/8.2/+1.2 · Rodgers 2.74/16.3/7.0/−1.3 · Lawrence 2.72/16.3/8.7/+3.6 · Daniels 2.94/13.8/8.6/+3.5.

## 7E Defensive direction map (pbp, opponent allowed)
- Run D: MIN left 5.4 ypc/+.071 EPA, middle 2.8, right 3.1/−.396 · BAL L 4.6, M 3.2, R 3.3 · DEN L 6.2/+.119, M 4.1, R 4.0 · IND L 6.8/+.271, M 3.6, R 4.3.
- Pass D: TEN L 8.5/+.341, M 7.2/+.377, R 7.3 · LAC L 8.0, M 7.2/−.141, R 7.4 · ARI 8.3–8.6 all directions (+.32–.52) · PHI 7.1–7.2.

## 7F Read-through
- **Gibbs vs MIN**: MIN is #1 defense by EPA. Strongest counter-evidence on our board; our v3 opponent adjustment only used MIN RB ypc allowed (shrunk) → model may under-weight MIN. CAUTION carried to 10G.
- **Walker**: best RYOE/att of the pool (+2.26) despite 25% 8+ boxes; DEN run D allows 6.2 ypc to the left.
- **Cook**: +0.93 RYOE; BAL middle run D strong (3.2), edges 3.3–4.6.
- **Higgins**: 43.8% air-yard share, aDOT 14.2 vs TEN (pass D 24th, +.34 left). Supports yardage, not catches.
- **Puka**: 2.90 sep, +1.94 YAC; Adams IR adds target share (not modeled → conservative).
- **Metcalf**: lowest cushion (4.41), sep 2.48 → press-heavy, weak for 40+ at −225.

## 7G Panthers Rule
NOT_APPLICABLE — no QB legs in pool.

## Phase 7 cuts
None added (cuts already made on edge later). Gibbs tagged CAUTION (MIN #1 D).
