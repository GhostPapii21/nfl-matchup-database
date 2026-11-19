# Edge research 2026

## Task 1: Pinnacle fair price vs other books (done, `fair_price.py`)
Pinnacle's two sides with the vig removed give a fair probability; every other book's price on the **same player, market
and line** is compared with it. Snapshot of Nov 19, 2026 (Week 11 lines, posted Thursday):

| Book | Prices compared | Average vs fair | Best | Share better than fair |
|---|---|---|---|---|
| DraftKings | 252 | -2.9 pts | +1.1 | 4% |
| FanDuel | 438 | -3.4 | +1.7 | 1% |
| BetMGM | 212 | -3.5 | +1.5 | 4% |
| Bovada | 244 | -3.4 | +1.0 | 3% |
| BetOnline | 324 | -3.2 | 0.0 | 0% |
| BetRivers | 70 | -3.9 | -0.2 | 0% |

- **No price was 2+ points better than fair.** On the same line, books copy each other and charge about the normal vig.
- 1,218 prices sit on a **different line** from Pinnacle's (e.g. 64.5 vs 66.5). Those are where the differences hide, and
  pricing them needs the yards distribution from Task 3.
- One snapshot early in the week. Edges are expected around news (inactives, injuries); the game-day hourly pulls will show
  it. Run `python3 research/edge_2026/fair_price.py` after any pull; it writes `edges_latest.json`.
