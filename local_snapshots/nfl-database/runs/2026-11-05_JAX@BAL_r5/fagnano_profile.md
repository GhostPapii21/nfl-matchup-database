# Fagnano profile vs BUF (2026_08_BAL_BUF), his dropbacks only (n=24)
Source: nflverse play_by_play_2026.parquet (CC-BY 4.0) + nflverse FTN charting (n_blitzers, n_pass_rushers; FTN data via nflverse, CC-BY-SA 4.0). Local copies are in r2/src, pulled 2026-11-02.
- Blitz = FTN n_blitzers > 0 (24/24 charted).
- Pressure = PROXY (sack OR qb_hit OR qb_scramble). **FTN has no is_qb_pressured field (MISSING)**, and true pressure isn't in pbp. Because the proxy includes sacks, it overstates how bad things look under pressure.
- Air bands: short <10, intermediate 10-19, deep 20+ (air_yards). He threw **0 deep** passes.
- PFF cross-check only: under-pressure rating 51.3 (PFF definition). Our proxy rating is 45.1 (2/6, 22 yds, 0 TD, 0 INT). Different definitions, so the two are not comparable.
1-GAME SAMPLE.

## Splits
| split   | value              |   db |   att |   cmp |   cmp_pct |   sacks |   sack_rate |   ypa |   INT |
|:--------|:-------------------|-----:|------:|------:|----------:|--------:|------------:|------:|------:|
| blitz   | blitzed            |   14 |    12 |     6 |      50   |       2 |        14.3 |   5.2 |     0 |
| blitz   | not blitzed        |   10 |     9 |     4 |      44.4 |       1 |        10   |   3.1 |     1 |
| press   | clean PROXY        |   15 |    15 |     8 |      53.3 |       0 |         0   |   4.6 |     1 |
| press   | pressure PROXY     |    9 |     6 |     2 |      33.3 |       3 |        33.3 |   3.7 |     0 |
| air     | intermediate 10-19 |    5 |     5 |     3 |      60   |       0 |         0   |  10   |     1 |
| air     | no target          |    3 |     0 |     0 |     nan   |       3 |       100   | nan   |     0 |
| air     | short <10          |   16 |    16 |     7 |      43.8 |       0 |         0   |   2.6 |     0 |
| all     | all                |   24 |    21 |    10 |      47.6 |       3 |        12.5 |   4.3 |     1 |

## Targets by player (sacks excluded)
| receiver_player_name   |   tgt |   rec |   yds |   tgt_blitzed |   tgt_pressure |   short |   inter |   deep |   aDOT |
|:-----------------------|------:|------:|------:|--------------:|---------------:|--------:|--------:|-------:|-------:|
| J.Hill                 |     6 |     3 |    21 |             3 |              2 |       6 |       0 |      0 |   -3.3 |
| M.Andrews              |     4 |     3 |    14 |             2 |              1 |       4 |       0 |      0 |    3.5 |
| Z.Flowers              |     4 |     0 |     0 |             3 |              0 |       3 |       1 |      0 |    7   |
| R.Bateman              |     3 |     1 |    22 |             1 |              2 |       1 |       2 |      0 |   12   |
| J.Lane                 |     1 |     1 |    13 |             1 |              0 |       0 |       1 |      0 |   13   |
| J.Cuevas               |     1 |     1 |    15 |             1 |              1 |       0 |       1 |      0 |   15   |
| D.Henry                |     1 |     1 |     6 |             0 |              0 |       1 |       0 |      0 |    2   |
| M.Hibner               |     1 |     0 |     0 |             1 |              0 |       1 |       0 |      0 |    2   |
