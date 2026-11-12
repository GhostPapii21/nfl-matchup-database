# Phase 1 rerun v2 (Rico-approved pull done; raw in backtests/yardage_markets_wk3_8/raw/w{week}_{eventid}.json, Odds API historical format {timestamp,data:{bookmakers:[...]}})
NO network. Never read/print env keys. Do not git commit. Work in backtests/yardage_markets_wk3_8/v2/ (new files; keep v1 files untouched).
STAGE A (this run, unless told STAGE B):
1. Build candidates from ALL saved raw (old sources + new raw/). MAIN lines only (drop alts entirely). Markets rushyds, recyds, rushrecyds. Point-in-time features only (weeks < w from pbp; spread/total from saved pre-kick game odds if present else from consensus none). Sharp Oct27 = HINDSIGHT column only.
2. coverage.csv by week x market (events, quotes, books).
3. Collapse to ONE leg per player-market-side-week (consensus main line = median line; price = median price at that line) -> legs.csv. Also a 'model edge' = directional (prior_yds_avg - line) for unders reversed.
4. grading_train.csv (wk3-6) by market x side: n, hit%, $10 P/L, ROI. DO NOT compute or print any wk7-8 outcomes in stage A.
5. traits.md from train only (edge buckets, line size, price, carry/target share, spread/implied total, opp allowance).
6. rules.py + locked_rules.json + RULES.md: market-side rules from TRAIN ONLY, <=3 conditions, min train n>=30 per kept cell, positive train ROI. Pre-registered VARIANT 'edgecap': identical but exclude legs with model edge > +15 yds (red flag), written now.
7. slip_method.md: one leg per player (pick highest-edge market-side for that player), 3-4 leg yardage-only slips, max 2 per game, deterministic order, $10/slip, product-of-odds payout. Same method for both variants.
8. grade.py written but NOT run on holdout. Print summary. 
STAGE B: run grade.py: singles (one per player) and slips for train and holdout, by market x side and by week, both variants, Sharp ON/OFF; judge vs target (holdout n>=100, hit>=57%, ROI>=+3%, each holdout week P/L>=0). Write results.md.
