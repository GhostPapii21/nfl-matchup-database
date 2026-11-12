# Yardage markets backtest Wk3-8 (TEST ONLY, Rico-approved 2026-11-03 6:22 AM ET)
Work ONLY in backtests/yardage_markets_wk3_8/. Markets: player rush yds, rec yds, rush+rec yds (no passing).
HARD RULES: ZERO network calls to the Odds API (no ODDS_API_KEY use, never print any env key). Use only saved files on disk
(backtests/rulebook_replay_wk6_8 incl. legs_all.pkl, alt_candidates.csv, raw/, graded_legs.csv; backtests/current_rules_wk6_8; runs/; outlier/; week8/ week9/; matchup_master.*; defender_ledger.csv; playlogs/; /tmp/*.parquet).
Do NOT edit tools/, rules/, runs/*/assemble.py, nfl-sim/, sb-fix/, sb-grades. Read-only elsewhere.
Steps (write python scripts here, save outputs here):
1. coverage.csv: by week (3-8) x market: # priced props (main/alt), books, fields available. List gaps in GAPS.md with est credit cost (historical event odds ~10 credits per market per region per event; estimate events x markets).
2. candidates.csv: full candidate set where prices exist; each row: week, game, player, team, market, side, tier(main/alt), line, price(american), result stat (from saved box scores/playlogs/espn), win/loss/push, features known PRE-kickoff only: spread, total, implied team total, prior-weeks carry/target share & yds avg (weeks < current only), opp defense allowance from prior weeks only, man/zone (flag Sharp Oct27 table as HINDSIGHT column separately), line size, price bucket. Tag any feature that cannot be cut by week.
3. grading_train.csv / grading_holdout.csv: market x side x tier: n, hit%, $10 flat P/L (to-win by american price), ROI. Train=Wk3-6, holdout=Wk7-8.
4. traits.md: what train winners share vs losers (univariate splits with n, hit%, ROI).
5. rules.py + RULES.md: market-specific rules derived from TRAIN ONLY, simple (<=3 conditions per market-side), min n>=15 per rule cell. Also slip_method.md: 3-4 leg yardage-only parlays from passing legs, one leg per player, max 2 legs per game, deterministic ordering (by edge/score), how many slips per week, $10 per slip. Then STOP and git commit these with: git -c user.name=Blitz -c user.email=blitz@local commit -m "Yardage wk3-8: rules + slip method locked before holdout" (add only this folder).
6. Then apply blind to holdout: singles + slips results for train and holdout, with sharp-hindsight ON and OFF variants. results.md. Commit again "Yardage wk3-8: holdout graded".
Print a concise summary at end including both commit hashes.
