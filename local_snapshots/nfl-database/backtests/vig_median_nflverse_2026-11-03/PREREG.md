# PREREG — vig / median / nflverse backtest (2026-11-03, written before any test result was computed)
Backtest only. 0 Odds API credits (saved prices only). No live changes, no merges, no skill edits, no held files touched.
Approved by Rico 4:43 PM ET (relayed by Ghost6). Report goes to Ghost6 to vet first.

## Data
- Props: `backtests/confidence_check_2026-11-03/legs_with_probs.csv` (md5 b8e9cb59...), 2026 Weeks 3-8, one bettable single-book line per leg (same file the review-branch replay used).
- Baseline: bet every rushyds under in that file, Weeks 3-8, $1 flat at the saved under price = 517 legs, 288-229, +4.77% ROI (review branch `backtests/replay_2026-11-03/replay.py`, commit c155e67). Pushes: none in file.
- Split: FIT = Weeks 3-6, HOLDOUT = Weeks 7-8. Anything fitted (power vs mult has no fit; margins, Platt, feature weights) uses FIT only. Features use only data from games before the leg's week.
- CI: paired bootstrap, resampling GAMES (game_id clusters), 10,000 reps, seed 0, 95% percentile interval.

## Pass bars (each test judged on HOLDOUT Weeks 7-8 unless stated)
**T1 power vs multiplicative de-vig.** Legs with both prices. PASS if holdout Brier(power) − Brier(mult) < 0 with CI entirely below 0. Log loss reported alongside. FAIL if CI entirely above 0 or point ≥ 0. Otherwise INSUFFICIENT (no detectable difference). By-market tables are descriptive only.
**T2 median vs mean.** Projections from the three sim engines (sim_v5, sim_v6, sim_v6_fix, opp 0.5, leak-free cutoffs as in confidence_check run_sims.py), rerun to save mean and median. Rules: (a) MEAN rule: bet over if mean > line, else under; (b) MEDIAN rule: over if median > line, else under; (c) SKEW-ADJ median: median shifted by the FIT-set per-market median of (actual − sim median) — i.e. bias-corrected median; side by sign vs line. Each also with a minimum margin m chosen on FIT from {0, 2.5%, 5%, 10%} of line by FIT ROI. PASS if the rule's holdout ROI minus the rush-under baseline's holdout ROI (Weeks 7-8 rush unders) has CI entirely above 0. Also report full Weeks 3-8 vs 288-229 for reference (not the bar, since margins are fit on 3-6).
  Skew hypothesis: rushyds legs, skew = (sim mean − sim median)/line. PASS (hypothesis supported) if logistic regression of under-hit on skew has slope CI (bootstrap) entirely above 0 on Weeks 3-8, AND under hit rate in top skew tercile > bottom tercile. Otherwise NOT SUPPORTED / INSUFFICIENT.
**T3a nflverse features over market.** Only if license allows. Features (prior weeks only): player's last-2 snap share (snap_counts), opponent defense blitz rate, box count, pass-rusher count, play-action/motion rate faced (FTN charting). Coverage shell / man-zone / alignment (C2 fields) are in pbp_participation, which is published only through 2025; if absent for 2026, those fields are reported as a DATA GAP. Model: logit(p) = logit(p_nv_mult) + a + Σ b_k·feature_k (L2=1, standardized on FIT). PASS if holdout Brier(model) − Brier(market) has CI entirely below 0.
**T3b Platt on closing lines (nfldata games.csv).** Markets: home moneyline (win), home spread (cover; pushes dropped), total over (pushes dropped). Raw = multiplicative no-vig from the closing odds. Fit Platt (logit(p) = a + b·logit(p_nv)) on seasons ≤ 2017, test 2018-2025 (time split, no 2026). PASS per market if test Brier(Platt) − Brier(raw) has CI entirely below 0 (bootstrap over games).

## Spend cap
Grok: $0 planned (pure data analysis); hard cap $3. Odds API: 0 credits.
