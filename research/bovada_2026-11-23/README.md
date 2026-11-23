# Do Bovada's player lines hit more often than the other books'? (Nov 23, 2026)

`python3 study.py` -> `results.json`, `rows.csv`. Lines: each book's main line (two-sided, nearest even money) from the
last snapshot pulled before kickoff; player lines exist from Nov 16 (StartWho feed), so this is 12 final games: Week 10
Monday (LAC@BAL) and Week 11 through the Sunday 4:25 games. Results: ESPN box scores. 296 Bovada props (receiving
yards, receptions, rushing yards).

| Book | Props | Over won | Over's fair chance from the price | Avg miss (yds/catches) |
|---|---|---|---|---|
| Bovada | 296 | 45% | 46% | 11.9 |
| DraftKings | 298 | 48% | 49% | 11.7 |
| FanDuel | 352 | 51% | 49% | 11.9 |
| BetMGM | 280 | 49% | 49% | 11.9 |
| Pinnacle | 314 | 49% | 49% | 11.6 |

Bovada's line against the other books on the same prop:
- Same line (185 props): identical to everyone else.
- Bovada 8+ yards (or 1+ catch) higher (74 props; never lower): these are not a different opinion. They are posted at
  about +150 over / -200 under, i.e. an alternate rung. The over won 35% where the price said 37% (break-even 39%);
  the under won 65% where break-even was 67%. Betting either side lost money (over -8.6%, under -2.8%). The other books'
  line was closer to the result 42 times, Bovada's 32.

Conclusion: Bovada's lines hit about as often as their prices say, like every other book. No sign of a different
"wavelength". Small sample (12 games); re-run weekly. The board now keeps lopsided-only lines (fair chance outside
40-60%) out of the main-line columns (`dashboard/book_lines.py`, `alt_only_books`). Research only.
