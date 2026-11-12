# TDs allowed (SEA, CHI) + Loveland. pbp through Wk8 (both teams played 7 games). Pulled 7:21 AM ET. Script: td_allowed.py

## TDs allowed by SEA
|   week | posteam   | td_player_name   | pos   | kind   |   yds | rz    | in5   | expl   |
|-------:|:----------|:-----------------|:------|:-------|------:|:------|:------|:-------|
|      1 | NE        | E.Raridon        | TE    | rec    |     2 | True  | True  | False  |
|      2 | ARI       | T.McBride        | TE    | rec    |     2 | True  | True  | False  |
|      3 | WAS       | R.White          | RB    | rec    |     6 | True  | False | False  |
|      3 | WAS       | T.Burks          | WR    | rec    |    11 | True  | False | False  |
|      3 | WAS       | T.McLaurin       | WR    | rec    |    30 | False | False | True   |
|      4 | LAC       | K.Vidal          | RB    | rec    |     9 | True  | False | False  |
|      4 | LAC       | O.Hampton        | RB    | rush   |     2 | True  | True  | False  |
|      5 | SF        | M.Evans          | WR    | rec    |     2 | True  | True  | False  |
|      5 | SF        | C.McCaffrey      | RB    | rush   |    11 | True  | False | True   |
|      5 | SF        | B.Cooks          | WR    | rec    |     7 | True  | False | False  |
|      6 | DEN       | J.Dobbins        | RB    | rush   |     4 | True  | True  | False  |
|      6 | DEN       | R.Harvey         | RB    | rush   |     1 | True  | True  | False  |
SEA: games 7, TDs 12, rush 4 (0.57/g), rec 8 (1.14/g); by pos {'RB': 6, 'WR': 4, 'TE': 2}; rec by pos {'WR': 4, 'TE': 2, 'RB': 2}; RZ-origin 11, outside-RZ 1, explosive 2; RZ trips 15 (2.14/g), RZ TD% 80.0%

## TDs allowed by CHI
|   week | posteam   | td_player_name   | pos   | kind   |   yds | rz    | in5   | expl   |
|-------:|:----------|:-----------------|:------|:-------|------:|:------|:------|:-------|
|      1 | CAR       | C.Hubbard        | RB    | rec    |     4 | True  | True  | False  |
|      1 | CAR       | J.Coker          | WR    | rec    |    51 | False | False | True   |
|      1 | CAR       | C.Hubbard        | RB    | rush   |     2 | True  | True  | False  |
|      1 | CAR       | J.Coker          | WR    | rec    |     8 | True  | False | False  |
|      3 | PHI       | J.Hurts          | QB    | rush   |     1 | True  | True  | False  |
|      4 | NYJ       | I.Williams       | WR    | rec    |    58 | False | False | True   |
|      5 | GB        | C.Watson         | WR    | rec    |    42 | False | False | True   |
|      5 | GB        | M.Lloyd          | RB    | rush   |     7 | True  | False | False  |
|      5 | GB        | C.Watson         | WR    | rec    |    53 | False | False | True   |
|      5 | GB        | M.Lloyd          | RB    | rush   |     4 | True  | True  | False  |
|      6 | ATL       | J.Dotson         | WR    | rec    |    13 | True  | False | False  |
|      6 | ATL       | K.Pitts          | TE    | rec    |    10 | True  | False | False  |
|      6 | ATL       | K.Pitts          | TE    | rec    |     5 | True  | True  | False  |
|      7 | NE        | R.Stevenson      | RB    | rec    |    48 | False | False | True   |
|      7 | NE        | E.Raridon        | TE    | rec    |    30 | False | False | True   |
CHI: games 7, TDs 15, rush 4 (0.57/g), rec 11 (1.57/g); by pos {'WR': 6, 'RB': 5, 'TE': 3, 'QB': 1}; rec by pos {'WR': 6, 'TE': 3, 'RB': 2}; RZ-origin 9, outside-RZ 6, explosive 6; RZ trips 24 (3.43/g), RZ TD% 62.5%
LEAGUE: TD/team-game 2.42, rush 0.89 rec 1.53, RZ trips/g 3.90, RZ TD% 61.9%, rec TD pos share {'WR': 0.57, 'TE': 0.32, 'RB': 0.1, 'FB': 0.01, 'CB': 0.0}

## TEs vs SEA
|   week | posteam   | receiver_player_name   |   tgt |   rec |   yds |   td |
|-------:|:----------|:-----------------------|------:|------:|------:|-----:|
|      1 | NE        | E.Raridon              |     1 |     1 |     2 |    1 |
|      1 | NE        | H.Henry                |     3 |     3 |    26 |    0 |
|      2 | ARI       | T.McBride              |    10 |     8 |    41 |    1 |
|      3 | WAS       | B.Sinnott              |     1 |     0 |     0 |    0 |
|      3 | WAS       | C.Yankoff              |     2 |     1 |     2 |    0 |
|      3 | WAS       | J.Bates                |     1 |     1 |     9 |    0 |
|      4 | LAC       | O.Gadsden              |     8 |     5 |    36 |    0 |
|      5 | SF        | G.Kittle               |     6 |     5 |    24 |    0 |
|      5 | SF        | L.Farrell              |     1 |     0 |     0 |    0 |
|      6 | DEN       | E.Engram               |     2 |     2 |    13 |    0 |
|      7 | KC        | N.Gray                 |     3 |     3 |    44 |    0 |
|      7 | KC        | T.Kelce                |     8 |     4 |    44 |    0 |
{'tgt': 6.6, 'rec': 4.7, 'yds': 34.4, 'td': 0.3}
SEA rank (1=most allowed): {'rec': 4.7, 'yds': 34.4, 'yrk': 31.0, 'rrk': 25.0} league avg {'rec': 5.5, 'yds': 55.4, 'yrk': 16.5, 'rrk': 16.5}

## Loveland
|   week |   tgt |   rec |   yds |   td |   rz_tgt |   share | qb         |
|-------:|------:|------:|------:|-----:|---------:|--------:|:-----------|
|      1 |     2 |     0 |     0 |    0 |        1 |   0.069 | C.Williams |
|      2 |     3 |     1 |     3 |    0 |        1 |   0.086 | C.Williams |
|      3 |     4 |     4 |    31 |    0 |        1 |   0.118 | C.Keenum   |
|      4 |     9 |     6 |    57 |    0 |        3 |   0.265 | T.Bagent   |
|      5 |     5 |     2 |    19 |    0 |        0 |   0.125 | T.Bagent   |
|      6 |     7 |     6 |    65 |    1 |        3 |   0.194 | C.Williams |
|      7 |    12 |     7 |    69 |    1 |        1 |   0.364 | C.Williams |
Kmet tgts by wk {1: 3, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 3}

## Loveland lines (odds_m0721.csv, FD 7:21 / DK 7:21 AM ET) and sims (fixed-model, copies only; raw_loveland.json)
No anytime-TD market is in our Odds API pull (player_anytime_td not requested), so TD prices are NOT pulled.
Shrink: p' = .5 + .7(p - .5). No-vig for alts is alt implied / main overround.
| Rung | FD price / nv | DK | MC | Bias | GR | Raw edge (M/B/G) | Shrunk edge | Clear +3 (raw/shrunk) | §7 Caleb (rec 0,1,6,7; yds 0,3,65,69) |
|---|---|---|---|---|---|---|---|---|---|
| Rec O2.5 | -490 / .777 | -456 | .713 | .875 | .666 | -6.4/+9.8/-11.1 | -12.8/+3.5/-16.1 | 1/3 , 1/3 | 2/4 FAIL |
| Rec O3.5 | -198 / .621 | -179 | .542 | .739 | .528 | -7.9/+11.8/-9.3 | -4.2/+9.6/-5.1 | 1/3 , 1/3 | 2/4 FAIL |
| Rec O4.5 | +116 main / .433 | +118 | .385 | .568 | .403 | -4.8/+13.5/-3.0 | -1.4/+11.5/-0.1 | 1/3 , 1/3 | 2/4 FAIL |
| Yds O39.5 | -138 / .546 | -127 | .352 | .504 | .362 | -19.4/-4.2/-18.4 | n/a | 0/3 | 2/4 FAIL |
| Yds O42.5 | -113 main / .500 | 41.5 -114 | .301 | .439 | .320 | -19.9/-6.1/-18.0 | n/a | 0/3 | 2/4 FAIL |
Medians: rec 4/5/4, yds 30/40/29. Only Bias (recency-weighted: Wk6-7 had 7/12 targets) likes the catches.
Kmet: not on the latest injury report in our data. He averaged 2 targets/g. Out status is UNVERIFIED (Loeb only).
Verdict: all Loveland rungs are CUT (fail §7 with Caleb at 2/4, and only 1/3 models clear). Rico's "SEA gives up a lot to TEs" is REFUTED: 4.7 rec / 34.4 yds per game to TEs (25th / 31st most; league avg 5.5 / 55.4). Loeb's numbers verify exactly. Most catches were McBride 8-41 and Gadsden 5-36. Most TE yards were KC's 2 TEs at 88 combined.
TD read: SEA allows only 1.71 TD/g (league 2.42), but 80% RZ TD% (league 61.9%). 11 of 12 TDs came from the red zone, with only 1 explosive. RBs scored 6 of 12, WRs 4, TEs 2 (both 2-yd goal-line). CHI allows 2.14/g with 1.57 rec TD/g, 6 of 15 from outside the RZ, and 6 explosive (WRs 42-58 yds), but a league-average RZ TD% of 62.5%.
