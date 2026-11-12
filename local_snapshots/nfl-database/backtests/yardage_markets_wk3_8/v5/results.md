# v5 graded results

$10 flat/leg at saved main-line prices. UNRESOLVED = no PBP participation (excluded). Slips: ≤5/week, 3–4 legs, 1 leg/game/slip, 1 leg/player, independent product price (estimate).

## By tag

```
               tag  won  lost  push  unresolved  unpriced     pl     roi
GROK_ON_SAVED_GAME    4    12     0           0         4 -84.91 -0.5307
     RECONSTRUCTED   60    59     0           3        31 -64.70 -0.0544
        SAVED_READ    5     3     0           0         6  13.50  0.1687
```

## By tag x split

```
               tag        split  won  lost  push  unresolved  unpriced      pl     roi
GROK_ON_SAVED_GAME holdout(7-8)    1     3     0           0         0  -21.15 -0.5288
GROK_ON_SAVED_GAME   train(3-6)    3     9     0           0         4  -63.76 -0.5313
     RECONSTRUCTED holdout(7-8)   25    14     0           0         9   78.63  0.2016
     RECONSTRUCTED   train(3-6)   35    45     0           3        22 -143.33 -0.1792
        SAVED_READ holdout(7-8)    0     1     0           0         2  -10.00 -1.0000
        SAVED_READ   train(3-6)    5     2     0           0         4   23.50  0.3357
```

## By tag x week

```
               tag  week  won  lost  push  unresolved  unpriced     pl     roi
GROK_ON_SAVED_GAME     5    3     8     0           0         3 -53.76 -0.4887
GROK_ON_SAVED_GAME     6    0     1     0           0         1 -10.00 -1.0000
GROK_ON_SAVED_GAME     7    1     3     0           0         0 -21.15 -0.5288
     RECONSTRUCTED     3    8    14     0           0        10 -69.69 -0.3168
     RECONSTRUCTED     4   10    14     0           2         6 -52.35 -0.2181
     RECONSTRUCTED     5    8     5     0           0         2  20.39  0.1569
     RECONSTRUCTED     6    9    12     0           1         4 -41.69 -0.1985
     RECONSTRUCTED     7   13     7     0           0         3  43.63  0.2181
     RECONSTRUCTED     8   12     7     0           0         6  35.00  0.1842
        SAVED_READ     5    5     1     0           0         4  33.50  0.5583
        SAVED_READ     6    0     1     0           0         0 -10.00 -1.0000
        SAVED_READ     7    0     1     0           0         2 -10.00 -1.0000
```

## By tag x market

```
               tag     market  side  won  lost  push  unresolved  unpriced     pl     roi
GROK_ON_SAVED_GAME     recyds  over    0     7     0           0         3 -70.00 -1.0000
GROK_ON_SAVED_GAME rushrecyds  over    0     0     0           0         1   0.00     NaN
GROK_ON_SAVED_GAME rushrecyds under    1     1     0           0         0  -1.15 -0.0575
GROK_ON_SAVED_GAME    rushyds  over    1     3     0           0         0 -21.23 -0.5307
GROK_ON_SAVED_GAME    rushyds under    2     1     0           0         0   7.47  0.2490
     RECONSTRUCTED     recyds  over   26    26     0           1        13 -32.24 -0.0620
     RECONSTRUCTED     recyds under    3     5     0           0         5 -23.21 -0.2901
     RECONSTRUCTED rushrecyds  over    6     3     0           1         4  22.48  0.2498
     RECONSTRUCTED rushrecyds under    3     3     0           0         1  -4.05 -0.0674
     RECONSTRUCTED    rushyds  over   19    15     0           1         7  16.00  0.0470
     RECONSTRUCTED    rushyds under    3     7     0           0         1 -43.68 -0.4368
        SAVED_READ     recyds  over    2     2     0           0         4  -2.89 -0.0724
        SAVED_READ     recyds under    1     0     0           0         1   8.77  0.8772
        SAVED_READ rushrecyds  over    0     0     0           0         1   0.00     NaN
        SAVED_READ    rushyds  over    2     0     0           0         0  17.62  0.8811
        SAVED_READ    rushyds under    0     1     0           0         0 -10.00 -1.0000
```

## PRIMARY by split

```
       split  won  lost  push  unresolved  unpriced      pl     roi
holdout(7-8)   25    15     0           0        11   68.63  0.1716
  train(3-6)   40    47     0           3        26 -119.83 -0.1377
```

## PRIMARY by week

```
 week  won  lost  push  unresolved  unpriced     pl     roi
    3    8    14     0           0        10 -69.69 -0.3168
    4   10    14     0           2         6 -52.35 -0.2181
    5   13     6     0           0         6  53.89  0.2836
    6    9    13     0           1         4 -51.69 -0.2349
    7   13     8     0           0         5  33.63  0.1601
    8   12     7     0           0         6  35.00  0.1842
```

## PRIMARY by market

```
    market  side  won  lost  push  unresolved  unpriced     pl     roi
    recyds  over   28    28     0           1        17 -35.14 -0.0627
    recyds under    4     5     0           0         6 -14.44 -0.1604
rushrecyds  over    6     3     0           1         5  22.48  0.2498
rushrecyds under    3     3     0           0         1  -4.05 -0.0674
   rushyds  over   21    15     0           1         7  33.62  0.0934
   rushyds under    3     8     0           0         1 -53.68 -0.4880
```

## ZONE_MOF by split

```
       split  won  lost  push  unresolved  unpriced      pl     roi
holdout(7-8)   23    13     0           0        11   71.24  0.1979
  train(3-6)   36    44     0           3        23 -124.97 -0.1562
```

## PRO_EDGE-pass subset by split

```
       split  won  lost  push  unresolved  unpriced     pl     roi
holdout(7-8)   14     7     0           0         4  52.86  0.2517
  train(3-6)    4     7     0           0         2 -35.19 -0.3199
```

## PRO_EDGE-pass by week

```
 week  won  lost  push  unresolved  unpriced     pl     roi
    6    4     7     0           0         2 -35.19 -0.3199
    7    7     3     0           0         2  31.41  0.3141
    8    7     4     0           0         2  21.45  0.1950
```

## ZONE_MOF by week

```
 week  won  lost  push  unresolved  unpriced     pl     roi
    3    7    13     0           0         9 -68.39 -0.3420
    4    8    13     0           2         6 -60.05 -0.2860
    5   12     6     0           0         4  45.16  0.2509
    6    9    12     0           1         4 -41.69 -0.1985
    7   12     6     0           0         5  44.93  0.2496
    8   11     7     0           0         6  26.31  0.1461
```

## Baseline rush-under by split

```
       split  won  lost  push  unresolved  unpriced     pl     roi
holdout(7-8)   70    62     1           9        34  -8.49 -0.0064
  train(3-6)  161   128     4           7        78 124.94  0.0432
```

## Baseline by week

```
 week  won  lost  push  unresolved  unpriced     pl     roi
    3   37    37     0           2        21 -43.40 -0.0586
    4   48    33     1           2        14  93.21  0.1151
    5   42    30     1           1        17  68.69  0.0954
    6   34    28     2           2        26   6.43  0.0104
    7   34    32     0           5        18 -22.91 -0.0347
    8   36    30     1           4        16  14.42  0.0219
```

## Slips PRIMARY by week

```
      slips  won      pl
week                    
3         5    0  -50.00
4         5    0  -50.00
5         5    1   72.53
6         5    0  -50.00
7         5    1   15.23
8         4    2  207.62
total pl 145.38
```

## Slips ZONE_MOF by week

```
      slips  won      pl
week                    
3         5    0  -50.00
4         5    0  -50.00
5         4    1   82.53
6         5    0  -50.00
7         4    1   83.67
8         4    2  207.62
total pl 223.82
```

## Slips PRO_EDGE by week

```
      slips  won      pl
week                    
6         2    0  -20.00
7         2    1  102.67
8         3    0  -30.00
total pl 52.67
```

## Rico placed legs (outcomes.csv, leg hit rate; leg prices mostly unknown)

```
                                        count   sum   mean
week market                                               
5    NFL 1st qtr rushing yds                1   1.0  1.000
     NFL 30+ rush & 10+ rec each half       1   0.0  0.000
     NFL anytime TD                         4   2.0  0.500
     NFL anytime TD (either player)         1   1.0  1.000
     NFL each 20+ rec yds each half         1   0.0  0.000
     NFL each 25+ rec yds each half         1   0.0  0.000
     NFL each 5+ rush yds each quarter      1   1.0  1.000
     NFL pass yds                           4   2.0  0.500
     NFL rec yds                            7   5.0  0.714
     NFL receiving yds                     20  18.0  0.900
     NFL receptions                        12   7.0  0.583
     NFL receptions (under)                 1   1.0  1.000
     NFL rush yds                          13   3.0  0.231
     NFL rush+rec yds                      14  12.0  0.857
6    2+ TDs                                 1   0.0  0.000
     Alt spread                             2   0.0  0.000
     Alt total                              1   1.0  1.000
     Alt total under                        2   2.0  1.000
     Anytime TD                            10   6.0  0.600
     Combined TDs                           1   0.0  0.000
     Moneyline                              1   0.0  0.000
     NFL 1Q rec yds                         3   3.0  1.000
     NFL 3Q rec yds                         2   2.0  1.000
     NFL anytime TD                         7   0.0  0.000
     NFL game total                         1   1.0  1.000
     NFL pass TDs                           1   0.0  0.000
     NFL pass yds                           5   4.0  0.800
     NFL rec yds                           23  22.0  0.957
     NFL receptions                        29  23.0  0.793
     NFL rush yds                          12   6.0  0.500
     NFL rush+rec yds                       9   5.0  0.556
     NFL sacks taken                        1   1.0  1.000
     PP fantasy pts under                   2   2.0  1.000
     Spread                                 2   0.0  0.000
7    NFL anytime TD                         1   1.0  1.000
     NFL game total                         1   1.0  1.000
     NFL rec yds                            7   5.0  0.714
     NFL receptions                         5   3.0  0.600
     NFL rush+rec yds                       1   1.0  1.000
     PP anytime TD                          1   1.0  1.000
     PP pass yds                            1   1.0  1.000
     PP rec yds                             4   2.0  0.500
     PP receptions                          4   2.0  0.500
     alt rec yds                            1   0.0  0.000
     alt rush yds                           1   0.0  0.000
8    anytime TD                             1   1.0  1.000
     fantasy score                          2   1.0  0.500
     moneyline                              1   1.0  1.000
     rec targets                            1   0.0  0.000
     rec yds                                6   5.0  0.833
     receptions                            18   9.0  0.500
     rush yds                               2   1.0  0.500
     rush+rec yds                           2   2.0  1.000
     total points                           1   1.0  1.000

By market:
                                   count   sum   mean
market                                               
2+ TDs                                 1   0.0  0.000
Alt spread                             2   0.0  0.000
Alt total                              1   1.0  1.000
Alt total under                        2   2.0  1.000
Anytime TD                            10   6.0  0.600
Combined TDs                           1   0.0  0.000
Moneyline                              1   0.0  0.000
NFL 1Q rec yds                         3   3.0  1.000
NFL 1st qtr rushing yds                1   1.0  1.000
NFL 30+ rush & 10+ rec each half       1   0.0  0.000
NFL 3Q rec yds                         2   2.0  1.000
NFL anytime TD                        12   3.0  0.250
NFL anytime TD (either player)         1   1.0  1.000
NFL each 20+ rec yds each half         1   0.0  0.000
NFL each 25+ rec yds each half         1   0.0  0.000
NFL each 5+ rush yds each quarter      1   1.0  1.000
NFL game total                         2   2.0  1.000
NFL pass TDs                           1   0.0  0.000
NFL pass yds                           9   6.0  0.667
NFL rec yds                           37  32.0  0.865
NFL receiving yds                     20  18.0  0.900
NFL receptions                        46  33.0  0.717
NFL receptions (under)                 1   1.0  1.000
NFL rush yds                          25   9.0  0.360
NFL rush+rec yds                      24  18.0  0.750
NFL sacks taken                        1   1.0  1.000
PP anytime TD                          1   1.0  1.000
PP fantasy pts under                   2   2.0  1.000
PP pass yds                            1   1.0  1.000
PP rec yds                             4   2.0  0.500
PP receptions                          4   2.0  0.500
Spread                                 2   0.0  0.000
alt rec yds                            1   0.0  0.000
alt rush yds                           1   0.0  0.000
anytime TD                             1   1.0  1.000
fantasy score                          2   1.0  0.500
moneyline                              1   1.0  1.000
rec targets                            1   0.0  0.000
rec yds                                6   5.0  0.833
receptions                            18   9.0  0.500
rush yds                               2   1.0  0.500
rush+rec yds                           2   2.0  1.000
total points                           1   1.0  1.000

Tickets:       count     sum
week               
5         9  197.72
6        14   18.53
7        14 -193.87
8         4 -104.50
```
