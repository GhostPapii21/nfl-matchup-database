# Week 8 proposal backtest: 2026 Weeks 1-8 (analysis only, NOTHING LIVE)
Run 2026-11-01 ET. Harness: `harness.py`; tests: `tests/test_harness.py` (7 pass, `python3 -m unittest discover -s tests`). Raw output: `results.json`, one CSV per proposal.
run_gate.py, sim_v6.py, PHASE_SCRIPT.md and the rules were not edited.

## Data and method caveats (read first)
- **There are 0 real-lined samples. All lines are proxy lines.** No prop lines or odds for Weeks 1-7 are stored on the box; the only odds are the Nov 1 pulls. Proxy line = floor(the player's median in prior 2026 games) + 0.5, with at least 2 prior games. Because yardage is right-skewed, this proxy sits a little above what books usually post, so the **universe** hit rates run about 41-47%. Read the *deltas against current* on the same set; the absolute ROI matters less. ROI is computed from hit rate at a flat -110, -130 or -160.
- pbp = nflverse play_by_play_2026.parquet (runs/2026-11-01_shared_src), through 2026-10-29: Weeks 1-7 plus Week 8 TNF. **Week 8 Sunday is not in it**, so today's games are out of sample. Spread = nflverse spread_line (closing). Weather = nflverse weather string/wind (no gusts or PoP). Positions come from roster_weekly_2026. pbp_participation is still unreadable (BUGLOG, OPEN) and was not used.
- Walk-forward: every input for week w uses only weeks before w. RB roles need at least 2 prior games, so legs start in Week 3.
- P2 and P3 need 3-model medians, which exist only in tools/sim_v6_backtest.csv (Weeks 4-7, calibrated by sim_v6_calib M). That file has medians but not each model's p, so P3 rebuilds p from a normal residual SD fit on prior weeks only.
- "Current" is a simplified replica of the gate on proxy lines, not a full run_gate replay (no coverage, freshness or no-vig gates). P1 current = RB1 + §7 form (≥3 of last 4 over the line). P2 current = all 3 medians clear + underdog block. P3 current = global 0.7 shrink, bet when p' > .5238. P4 current = τ .392 projection ≥ 1.10× line. P5 current = banned (0 legs).

## Summary table
| # | Proposal | n (prop.) | Hit | ROI -110 / -130 / -160 | vs current (same set) | 90% CI | Verdict |
|-|-|-|-|-|-|-|-|
| 1 | Carries leader + RB2 on weather/promotion trigger | 18 (cur 6) | 61.1% | +16.7% / +8.1% / -0.7% | +12 legs added at 58.3%, 0 removed; net hit 66.7%→61.1%, ROI@-110 +27.3%→+16.7% (more units won: +1.4u) | .42-.77 | Promising but SMALL SAMPLE (16 trigger games). Track it; don't adopt on this alone. |
| 2 | 2-of-3 medians; drop the underdog block when all 3 clear (**RECONSIDERATION: Rico declined option C today**) | 52 (cur 20) | 59.6% | +13.8% / +5.5% / -3.1% | +32 added at 59.4%, 0 removed; net hit 60.0%→59.6%, ROI flat (+14.5→+13.8) | .48-.70 | More volume at about the same hit rate. Profitable to about -130 only. Rico's call, since he already declined it. |
| 3 | Per-market calibrated shrink + RB receiving cap | 131 (cur 125) | 50.4% | -3.8% / -10.9% / -18.1% | +6 added at 33%, 0 removed; net ROI -2.3%→-3.8% | .43-.58 | No improvement. The fitted rushing shrink came out 0.70-0.90 (≈ current 0.7), and the RB-rec cap fit to 1.0 (no overprojection in Wk4-6). Reject as written. |
| 4 | Injury-promotion re-projection (τ .75) vs kept τ .392 (CI .28-.50) | 12 (cur 11) | 58.3% | +11.4% / +3.2% / -5.2% | +1 leg (hit), 0 removed | .36-.78 | Indistinguishable (only 12 2026 promotion games). Keep .392; no evidence to change. |
| 5 | WR3/TE1 vs weak pass D (**EXCEPTION to Rico's #3/#4 ban**) | 112 (cur 0) | 48.2% | -8.0% / -14.7% / -21.7% | +112 added at 48.2% (universe 44.5%) | .41-.56 | Weak-D filter lifts the hit rate about 4 pts but stays unprofitable. Ban holds; don't take the exception. |

ROI break-even: -110 = 52.4%, -130 = 56.5%, -160 = 61.5%. **No proposal clears -160.**

## Notes per proposal
1. Triggers: 14 weather team-games, 10 promotions, 2 both. RB-rushing universe on proxy lines hit 47%. CSV: P1_carries_leader_rb2.csv.
2. The underdog-waiver arm (all 3 clear while a dog) added only a few legs. Most of the gain is the 2-of-3 arm. CSV: P2_two_of_three_medians.csv.
3. Walk-forward fitted s: rushyds .90/.70/.70 (Wk5/6/7), rec .95-1.0, recyds .65-.80. The Week 8 finding ("rushing medians run low") is not visible in Weeks 4-7 medians beyond what calibration M already fixes. CSV: P3_per_market_shrink_rbcap.csv.
4. Projection columns for both τ are in P4_injury_promotion.csv. Supplementing with 2025 pbp would raise n (the τ fit used 66 cases from 2025 and 2026); not done here because the scope was 2026 Wk1-8.
5. "Weak" = opponent's prior-weeks WR+TE yards/target ≥ 1.10× league average. This is **team-level**, because no week-by-week defender history exists before Week 8 (defender_ledger is current-season snapshots). CSV: P5_wr3_te_weak_def.csv.
