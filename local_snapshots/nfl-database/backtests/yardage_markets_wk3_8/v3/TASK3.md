# v3 yardage backtest (TEST ONLY). NO network, never read/print env keys, no git commits. Work only in v3/ (read v2/, raw/, ../../runs, week folders, /tmp parquet read-only).
Reuse v2 legs.csv consensus (main lines only, one leg per player-market-side-week) as the leg universe.
STAGE A:
1. Point-in-time features (only weeks < w, or saved pre-kickoff data): RB carry share and snap share (snap counts if saved, else log gap), second-back share (committee threat), opp rush yds/game and yds/carry allowed, opp rec yds allowed to player's position (WR/TE/RB from players.parquet), target share, spread/implied team total/favored flag from saved pre-kick game odds (check raw folders for h2h/spreads/totals; list which weeks lack them), injuries as of kickoff (/tmp/inj26.parquet if it has report dates <= kickoff; else gap), weather (saved weather json; open-air only; else gap). Write features.csv + GAPS.md (gaps and leakage risks).
2. Baseline: all main rushyds unders (no filter) and the one-leg-per-player version, by week, train wk3-6 ONLY in stage A.
3. traits.md from train only.
4. rules.py/locked_rules.json/RULES.md: per market-side rules from TRAIN ONLY, max 3-4 conditions, train n>=30, positive train ROI; must include 60% carry rule (RB overs require prior carry share>=60%). Plain-words description with train n/hit/P/L/ROI.
5. slip_method.md = v2 method (3-4 legs, one leg per player, max 2 per game, product-of-odds, estimates).
6. grade.py written, NOT run on holdout. Don't compute any wk7-8 outcome. frozen_sha256.json.
STAGE B: run grade.py unchanged: singles one-per-player and slips, train and holdout, by market x side and by week (won/lost/P/L $10/ROI), baseline by week train+holdout with per-rule beats-baseline comparison, target judgment (holdout n>=100, hit>=57%, ROI>=3%, each holdout week P/L>=0). results.md.
