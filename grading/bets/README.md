# Bet ledger

One row per real bet in `LEDGER.csv`. `python -m grading.scorecard` reads it every Tuesday.
- `market`: receptions, receiving_yards, rushing_yards, rush_rec_yards, alt_receiving_yards, spread, total, moneyline, parlay.
- `american`: the price you got (e.g. -115). `closing_american`: the same bet's price just before kickoff (from
  `pregame/direct_lines` history or the book).
- `our_prob`: the blend probability the board showed (blank if none). `result`: W, L, P (push) or V (void).
- Parlays: one row, `market` = parlay, legs in `notes`.
