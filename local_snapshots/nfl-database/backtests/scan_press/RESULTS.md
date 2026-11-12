# Scan / Press / Pass-volume cap: combined backtest report (2026-11-01 ET)
Build and backtest only. Nothing is live, and no messages or bets were sent. All new modules are opt-in and OFF by default.

## Method
- **Walk-forward:** week w uses only data from weeks < w.
- **Stand-in lines:** floor(prior median)+0.5, with at least 2 prior games. Real Week 8 lines come from runs/2026-11-01_* manifests (the `real` column).
- **Prices:** ROI is computed at -110, -130 and -160.
- **Models check (wk4-7):** raw sim_v6_backtest medians, with no calibration, because the calibration was fitted on wk4-7 and would leak.
- **§7 on stand-in rows:** uses a labelled proxy of ≥2 of the last 4 above the line. The true rule is 3 of 4, but that can never fire against a self-median line. Week 3/4 rows can't pass this structurally (2-3 priors).

## Arms (full numbers in summary.txt / results.json / per-arm CSVs)
| table | arm | n | hit | ROI -110 | -130 | -160 |
|-|-|-|-|-|-|-|
| wk4-7 models | current | 133 | .519 | -1.0% | -8.2% | -15.7% |
| | current+cap | 125 | .512 | -2.3% | -9.4% | -16.8% |
| | scan_only | 134 | .522 | -0.3% | -7.6% | -15.1% |
| | scan+press k2 | 136 | .522 | -0.3% | -7.6% | -15.2% |
| | scan+press k3 | 134 | .522 | -0.3% | -7.6% | -15.1% |
| | **PRESS tier only, k=2** | 16 | .812 | +55% | +44% | +32% |
| | **PRESS tier only, k=3** | 14 | .857 | +64% | +52% | +39% |
| wk3-8 form only | current | 596 | .451 | -13.8% | -20.1% | -26.7% |
| | current+cap | 565 | .448 | -14.5% | | |
| | scan_only | 664 | .459 | -12.3% | -18.7% | -25.4% |

- **Stability:** per-week hit and stability are in summary.txt.
- **PRESS k2, per week:** w5 5/.80, w6 3/1.00, w7 8/.75. The 90% CI is .61-.92.
- **Reading:** PRESS is a sizing tier on legs that already pass, not a new selection. The full arms move by ±2 legs.

## 2-of-3 vs 3-of-3 (Rico)
- k=2 adds 2 legs over k=3, and 1 of the 2 hit.
- Both samples are tiny: 14-16 legs, all on stand-in lines, over 3 weeks. That is suggestive, not proof.
- **Default:** k=2 is the default. One model alone always raises an error.

## Pass-volume cap (team favored by ≥6: QB pass-yd overs and WR2 receiving overs)
- **wk4-7 models:** killed 8 legs, 5 winners and 3 losers. Hit rate fell from .522 to .516 and ROI got worse.
- **wk3-8 form:** killed 33 legs, 16 winners and 17 losers. Roughly neutral.
- **Sanity cases (real Week 8 lines):**
  - Stafford o250.5 finished at 157 on 25 attempts. Miss, so the cap avoided a loss.
  - Burrow o272.5 finished at 462. Hit, so the cap killed a winner.
  - Maye o239.5 finished at 199. Miss.
  - JAX WR2 (Meyers) o38.5 finished at 24. Miss. JAX threw only 17 times. P. Washington is not JAX's WR2 by the target role, so the cap doesn't touch him.
- **Verdict:** the cap does not earn promotion. It catches the Stafford/JAX-type losses but kills about as many winners.

## Week 8 misses surfaced pregame by the scan (no leakage; ranks are out of 262)
| player | role/trigger | leg | rank | actual |
|-|-|-|-|-|
| Gainwell | RB2, weather | ryds o15.5 | 60 | 140 |
| Braelon Allen | RB1 (Hall OUT) | ryds o59.5 | 32 | 147 |
| Mitchell | WR2, starter_out | recyds o60.5 | 86 | 142 |
| Chase Brown | RB1 | rec o3.5 | 254 | 8 |
| Emmett Johnson | RB2, dog_receiving | recyds o17.5 | 128 | 128 |

All 5 are surfaced, but only Allen ranks highly. The scan finds them; it doesn't prioritize them.

## RULE5_CONFLICT (decision for Rico, rule untouched)
- 67 RB2 rush candidates hit 36 times (54%) before the form check.
- With the form check: 25 candidates hit 13 times (52%).
- Rule 5 blocks all of them. That is not a clear edge, so it's Rico's call. The WR #3/#4 ban is kept.

## HOLD bug fix (the one gate-behavior change)
See BUGLOG.md. MISSING price now triggers a re-pull; if that fails the leg is HOLD (blocked, fail-closed) and is no longer cut silently. Gate output plus exit code is byte-identical to the backup on all 16 runs/2026-11-01_* dirs.

## Tests
- tools/tests went from 114 OK before to **143 OK** after.
- New: test_hold (7), test_slate_scan (13, including a regression test for an s_allow bug found today), test_press_tier (9).

## Files
- **New:**
  - tools/slate_scan.py, tools/press_tier.py, tools/price_hold.py, tools/scan_data.py
  - this folder, including slate_scan_wk8.csv
- **Edited:** tools/run_gate.py and runs/2026-11-01_shared_src/assemble.py. Both have .pre_scanpress.bak backups.

## Honest verdict
- Nothing clears the bar for going live.
- Scan widens the pool for +0.3pt hit.
- The cap is neutral to negative.
- PRESS-tier is the only strong signal, at n=14-16 on stand-in lines. It needs real-line confirmation over weeks 9+.

---
# Update 2026-11-01 21:42 ET: PRESS tier ON for Week 9 (user-approved)
- Config: tools/gate_config.json sets `press_tier.enabled=true`, `enabled_from="2026-11-05"`, `models_required=2`, `pass_volume_cap.enabled=false`. Rule 5 is untouched.
- PRESS requires all five context checks (matchup, coverage, script, QB, §7) plus 2 of 3 sim medians. These override PRESS (BLOCKED): weather stop, injury/inactive, §11 conflict, WR rank 3/4.
- Tagging: the gate writes `press_tier` into each live leg of run_manifest.json, adds a "## PRESS legs" section to report.md, and appends to press_live_2026.csv. Pass/fail is unchanged.
- Grading: `python3 tools/grade_press.py playlogs/2026_wk9/*.csv` fills `result` (reads play logs only).
- Scan weights: walk-forward logistic fit on weeks 3-7, applied only to week 8 and later (fit_weights.py, scan_weights_wk8.json). Week 8 ranks out of 262 (old → new):
  - Allen: 32 → 47
  - Gainwell: 60 → 22
  - Mitchell: 86 → 5
  - E. Johnson: 128 → 108
  - C. Brown rec: 254 → 230
- Top-50 per week (walk-forward), old vs new:
  - Week 8 hit: .52 → .56. ROI at -110/-130/-160: -0.7/-8.0/-15.5% → +6.9/-0.9/-9.0%.
  - Pooled weeks 5-8 (n=200): .505 → .500. ROI at -110: -3.6% → -4.5%.
  - The new weights are unstable week to week (wk7 .36). The scan stays candidate-only.
