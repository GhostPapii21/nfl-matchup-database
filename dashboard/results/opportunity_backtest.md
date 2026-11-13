# Opportunity check backtest (2024, 2025, 2026, weeks 5+)

Every projection uses only earlier weeks. Brier score: lower is better; the baseline is the player's own hit rate in his previous games.

## Pass catchers: 6379 player-games, average yardage miss 20.36 yards

| Stat | Line | Hit rate | Avg predicted | Brier (simulation) | Brier (own history) |
| --- | --- | --- | --- | --- | --- |
| yards | 40+ | 30.6% | 28.0% | 0.1644 | 0.1722 |
| yards | 60+ | 16.9% | 15.4% | 0.1129 | 0.118 |
| yards | 70+ | 12.4% | 11.4% | 0.09 | 0.096 |
| yards | 80+ | 9.2% | 8.4% | 0.0718 | 0.0773 |
| yards | 100+ | 4.4% | 4.6% | 0.0387 | 0.0441 |
| receptions | 4+ | 31.7% | 30.0% | 0.1657 | 0.1736 |
| receptions | 6+ | 13.2% | 12.5% | 0.0931 | 0.098 |

Calibration (when the simulation said this, it happened this often):

- yards 40+: [0.0, 0.1) said 6%, hit 7% (n=1490), [0.1, 0.2) said 15%, hit 16% (n=1404), [0.2, 0.3) said 25%, hit 27% (n=987), [0.3, 0.4) said 35%, hit 40% (n=768), [0.4, 0.5) said 45%, hit 47% (n=620), [0.5, 0.6) said 55%, hit 60% (n=459), [0.6, 0.7) said 65%, hit 70% (n=355), [0.7, 0.8) said 74%, hit 83% (n=241), [0.8, 0.9) said 84%, hit 78% (n=54), [0.9, 1.0) said 91%, hit 100% (n=1)
- yards 60+: [0.0, 0.1) said 4%, hit 4% (n=3284), [0.1, 0.2) said 15%, hit 17% (n=1253), [0.2, 0.3) said 25%, hit 28% (n=745), [0.3, 0.4) said 35%, hit 40% (n=473), [0.4, 0.5) said 45%, hit 48% (n=324), [0.5, 0.6) said 55%, hit 62% (n=198), [0.6, 0.7) said 64%, hit 63% (n=83), [0.7, 0.8) said 73%, hit 47% (n=19)
- yards 70+: [0.0, 0.1) said 3%, hit 4% (n=3989), [0.1, 0.2) said 14%, hit 16% (n=1084), [0.2, 0.3) said 24%, hit 29% (n=614), [0.3, 0.4) said 35%, hit 36% (n=361), [0.4, 0.5) said 45%, hit 50% (n=210), [0.5, 0.6) said 54%, hit 49% (n=96), [0.6, 0.7) said 64%, hit 52% (n=23), [0.7, 0.8) said 71%, hit 0% (n=2)
- yards 80+: [0.0, 0.1) said 3%, hit 3% (n=4566), [0.1, 0.2) said 14%, hit 16% (n=944), [0.2, 0.3) said 24%, hit 28% (n=445), [0.3, 0.4) said 34%, hit 35% (n=267), [0.4, 0.5) said 44%, hit 41% (n=121), [0.5, 0.6) said 54%, hit 42% (n=31), [0.6, 0.7) said 63%, hit 60% (n=5)
- yards 100+: [0.0, 0.1) said 2%, hit 2% (n=5395), [0.1, 0.2) said 14%, hit 15% (n=641), [0.2, 0.3) said 24%, hit 19% (n=236), [0.3, 0.4) said 34%, hit 26% (n=87), [0.4, 0.5) said 44%, hit 22% (n=18), [0.5, 0.6) said 51%, hit 50% (n=2)
- receptions 4+: [0.0, 0.1) said 6%, hit 6% (n=1424), [0.1, 0.2) said 15%, hit 18% (n=1222), [0.2, 0.3) said 25%, hit 26% (n=985), [0.3, 0.4) said 35%, hit 34% (n=775), [0.4, 0.5) said 45%, hit 50% (n=702), [0.5, 0.6) said 55%, hit 55% (n=509), [0.6, 0.7) said 65%, hit 71% (n=370), [0.7, 0.8) said 75%, hit 78% (n=264), [0.8, 0.9) said 84%, hit 86% (n=118), [0.9, 1.0) said 92%, hit 70% (n=10)
- receptions 6+: [0.0, 0.1) said 3%, hit 3% (n=3784), [0.1, 0.2) said 15%, hit 17% (n=1136), [0.2, 0.3) said 24%, hit 24% (n=674), [0.3, 0.4) said 35%, hit 37% (n=357), [0.4, 0.5) said 44%, hit 45% (n=214), [0.5, 0.6) said 54%, hit 56% (n=145), [0.6, 0.7) said 64%, hit 64% (n=56), [0.7, 0.8) said 73%, hit 80% (n=10), [0.8, 0.9) said 81%, hit 33% (n=3)

## Running backs: 1880 player-games, average yardage miss 23.99 yards

| Stat | Line | Hit rate | Avg predicted | Brier (simulation) | Brier (own history) |
| --- | --- | --- | --- | --- | --- |
| yards | 50+ | 37.0% | 34.3% | 0.1715 | 0.1853 |
| yards | 70+ | 22.4% | 20.4% | 0.1414 | 0.1476 |
| yards | 90+ | 13.0% | 11.6% | 0.0974 | 0.1029 |
| carries | 12+ | 40.6% | 35.2% | 0.1588 | 0.1677 |
| carries | 15+ | 26.3% | 23.2% | 0.1452 | 0.151 |

Calibration (when the simulation said this, it happened this often):

- yards 50+: [0.0, 0.1) said 6%, hit 8% (n=399), [0.1, 0.2) said 15%, hit 17% (n=344), [0.2, 0.3) said 25%, hit 23% (n=226), [0.3, 0.4) said 35%, hit 44% (n=162), [0.4, 0.5) said 45%, hit 49% (n=166), [0.5, 0.6) said 55%, hit 63% (n=207), [0.6, 0.7) said 65%, hit 65% (n=189), [0.7, 0.8) said 75%, hit 75% (n=109), [0.8, 0.9) said 84%, hit 83% (n=59), [0.9, 1.0) said 92%, hit 95% (n=19)
- yards 70+: [0.0, 0.1) said 4%, hit 6% (n=806), [0.1, 0.2) said 14%, hit 17% (n=303), [0.2, 0.3) said 25%, hit 28% (n=225), [0.3, 0.4) said 35%, hit 42% (n=227), [0.4, 0.5) said 44%, hit 39% (n=153), [0.5, 0.6) said 55%, hit 57% (n=89), [0.6, 0.7) said 64%, hit 66% (n=44), [0.7, 0.8) said 75%, hit 70% (n=27), [0.8, 0.9) said 84%, hit 60% (n=5), [0.9, 1.0) said 94%, hit 100% (n=1)
- yards 90+: [0.0, 0.1) said 3%, hit 4% (n=1120), [0.1, 0.2) said 15%, hit 17% (n=342), [0.2, 0.3) said 24%, hit 26% (n=235), [0.3, 0.4) said 35%, hit 34% (n=102), [0.4, 0.5) said 44%, hit 44% (n=45), [0.5, 0.6) said 56%, hit 60% (n=25), [0.6, 0.7) said 63%, hit 50% (n=8), [0.7, 0.8) said 75%, hit 50% (n=2), [0.8, 0.9) said 85%, hit 100% (n=1)
- carries 12+: [0.0, 0.1) said 4%, hit 8% (n=536), [0.1, 0.2) said 14%, hit 19% (n=244), [0.2, 0.3) said 25%, hit 23% (n=168), [0.3, 0.4) said 35%, hit 36% (n=121), [0.4, 0.5) said 45%, hit 59% (n=153), [0.5, 0.6) said 55%, hit 67% (n=168), [0.6, 0.7) said 65%, hit 74% (n=199), [0.7, 0.8) said 75%, hit 79% (n=168), [0.8, 0.9) said 84%, hit 86% (n=107), [0.9, 1.0) said 92%, hit 94% (n=16)
- carries 15+: [0.0, 0.1) said 3%, hit 5% (n=800), [0.1, 0.2) said 15%, hit 15% (n=227), [0.2, 0.3) said 25%, hit 34% (n=181), [0.3, 0.4) said 35%, hit 43% (n=185), [0.4, 0.5) said 45%, hit 47% (n=189), [0.5, 0.6) said 55%, hit 60% (n=151), [0.6, 0.7) said 65%, hit 66% (n=89), [0.7, 0.8) said 74%, hit 69% (n=48), [0.8, 0.9) said 84%, hit 70% (n=10)

