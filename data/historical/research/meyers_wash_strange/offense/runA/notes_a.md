# JAX offense, Weeks 1–8, 2026



Source: local nflverse CC-BY snapshot, pulled 2026-11-03 08:04 ET. Recomputed from the four supplied files; reference build.py informed the join and split logic, with no copied results. Run: `python3 week10/meyers_wash_strange/offense/runA/build_a.py`.



Seven JAX games: Weeks 1–6 and 8; Week 7 bye. Regular season only. PBP excludes two-point attempts, no-play rows and deleted plays. Attempts exclude sacks; named/identified receivers define targets, excluding untargeted throwaways/spikes. Lawrence attribution uses passer T.Lawrence for throws/sacks or rusher T.Lawrence for scrambles; no other-QB sacks are assigned to him. QB splits use qb_dropback=1, which excludes one Lawrence clock spike; the attempt/target tables retain official pass attempts including that untargeted spike.



All rates are fractions, with denominator `_n` columns (or att/dropbacks/targets_n); counts appear alongside rates. aDOT uses non-null air yards; YPA treats null passing yards on incomplete passes as zero. EPA is mean per dropback with epa_n. Receiving yards are summed. Snap averages are arithmetic means of source game percentages over source appearances (games played), not snap-weighted percentages. Source offense_pct is rounded and has no exact team-snap denominator; games_n and offense_pct_source_games_n accompany it.



## Snap averages

| player            |   offense_snaps |   offense_pct |   games_n |   offense_pct_source_games_n | row_type             |
|:------------------|----------------:|--------------:|----------:|-----------------------------:|:---------------------|
| Brenton Strange   |         47      |      0.748571 |         7 |                            7 | average_games_played |
| Brian Thomas Jr.  |         27.5714 |      0.445714 |         7 |                            7 | average_games_played |
| Jakobi Meyers     |         47.5714 |      0.76     |         7 |                            7 | average_games_played |
| Parker Washington |         47      |      0.75     |         7 |                            7 | average_games_played |



## Targets

| scope       | receiver            |   rank |   targets |   receptions |   yards |   targets_n |   target_share |     adot |   adot_n |
|:------------|:--------------------|-------:|----------:|-------------:|--------:|------------:|---------------:|---------:|---------:|
| Lawrence    | Parker Washington   |      1 |        48 |           27 |     432 |         192 |     0.25       | 12.875   |       48 |
| Lawrence    | Brenton Strange     |      2 |        35 |           28 |     334 |         192 |     0.182292   |  7.88571 |       35 |
| Lawrence    | Jakobi Meyers       |      3 |        31 |           22 |     309 |         192 |     0.161458   | 10.5484  |       31 |
| Lawrence    | Brian Thomas Jr.    |      4 |        21 |           10 |     117 |         192 |     0.109375   | 12.2381  |       21 |
| Lawrence    | Bhayshul Tuten      |      5 |        16 |           15 |     181 |         192 |     0.0833333  | -3.0625  |       16 |
| Lawrence    | Josh Cameron        |      6 |        12 |            8 |     117 |         192 |     0.0625     |  4.91667 |       12 |
| Lawrence    | Nate Boerkircher    |      7 |         9 |            7 |      83 |         192 |     0.046875   |  6.55556 |        9 |
| Lawrence    | Travis Hunter       |      8 |         7 |            6 |      76 |         192 |     0.0364583  |  4.28571 |        7 |
| Lawrence    | LeQuint Allen Jr.   |      9 |         5 |            2 |       9 |         192 |     0.0260417  |  2.6     |        5 |
| Lawrence    | Ameer Abdullah      |     10 |         3 |            2 |       2 |         192 |     0.015625   | -4       |        3 |
| Lawrence    | Chris Rodriguez Jr. |     10 |         3 |            2 |      23 |         192 |     0.015625   |  2.33333 |        3 |
| Lawrence    | Quintin Morris      |     12 |         2 |            1 |       7 |         192 |     0.0104167  |  2.5     |        2 |
| team_all_QB | Parker Washington   |      1 |        48 |           27 |     432 |         195 |     0.246154   | 12.875   |       48 |
| team_all_QB | Brenton Strange     |      2 |        35 |           28 |     334 |         195 |     0.179487   |  7.88571 |       35 |
| team_all_QB | Jakobi Meyers       |      3 |        31 |           22 |     309 |         195 |     0.158974   | 10.5484  |       31 |
| team_all_QB | Brian Thomas Jr.    |      4 |        21 |           10 |     117 |         195 |     0.107692   | 12.2381  |       21 |
| team_all_QB | Bhayshul Tuten      |      5 |        16 |           15 |     181 |         195 |     0.0820513  | -3.0625  |       16 |
| team_all_QB | Josh Cameron        |      6 |        13 |            8 |     117 |         195 |     0.0666667  |  6.69231 |       13 |
| team_all_QB | Nate Boerkircher    |      7 |         9 |            7 |      83 |         195 |     0.0461538  |  6.55556 |        9 |
| team_all_QB | Travis Hunter       |      8 |         7 |            6 |      76 |         195 |     0.0358974  |  4.28571 |        7 |
| team_all_QB | LeQuint Allen Jr.   |      9 |         6 |            2 |       9 |         195 |     0.0307692  |  3.5     |        6 |
| team_all_QB | Ameer Abdullah      |     10 |         3 |            2 |       2 |         195 |     0.0153846  | -4       |        3 |
| team_all_QB | Chris Rodriguez Jr. |     10 |         3 |            2 |      23 |         195 |     0.0153846  |  2.33333 |        3 |
| team_all_QB | Quintin Morris      |     12 |         2 |            1 |       7 |         195 |     0.0102564  |  2.5     |        2 |
| team_all_QB | Tanner Koziol       |     13 |         1 |            1 |       8 |         195 |     0.00512821 |  1       |        1 |



## Meyers timing

Meyers is JAX in every available roster week (1–6, 8), and receiving PBP posteam is JAX in those same seven games. There is no within-2026 team transition in this snapshot. A trade to JAX may predate this sample, but these files cannot establish a transaction or trade date. Week 7 has no roster/receiving entry and is JAX’s bye; it is not evidence of a team change. Only seven JAX games are observed.



## Pressure

FTN n_blitzers > 0 and n_pass_rushers >= 5 are distinct measures, each using its own non-null charted dropback denominator. Sack and QB-hit rates use all eligible dropbacks with known respective PBP flags. League includes BAL; league_ex_BAL is also supplied.

| row_type   | scope         |   dropbacks |   games_n |   blitz_rate_n |   blitz_rate_count |   blitz_rate |   rush5plus_rate_n |   rush5plus_rate_count |   rush5plus_rate |   sack_rate_n |   sack_rate_count |   sack_rate |   qb_hit_rate_n |   qb_hit_rate_count |   qb_hit_rate | split_axis     | split          |   att |   completions |    cmp_pct |   cmp_pct_n |   passing_yards |       ypa |   ypa_n |   sacks |        epa |   epa_n |
|:-----------|:--------------|------------:|----------:|---------------:|-------------------:|-------------:|-------------------:|-----------------------:|-----------------:|--------------:|------------------:|------------:|----------------:|--------------------:|--------------:|:---------------|:---------------|------:|--------------:|-----------:|------------:|----------------:|----------:|--------:|--------:|-----------:|--------:|
| defense    | BAL           |         300 |         8 |            300 |                 99 |     0.33     |                300 |                     99 |         0.33     |           300 |                17 |   0.0566667 |             300 |                  51 |      0.17     | nan            | nan            |   nan |           nan | nan        |         nan |             nan | nan       |     nan |     nan | nan        |     nan |
| defense    | league        |        8962 |       121 |           8887 |               2827 |     0.318105 |               8887 |                   2828 |         0.318218 |          8962 |               557 |   0.0621513 |            8962 |                1366 |      0.152421 | nan            | nan            |   nan |           nan | nan        |         nan |             nan | nan       |     nan |     nan | nan        |     nan |
| defense    | league_ex_BAL |        8662 |       121 |           8587 |               2728 |     0.31769  |               8587 |                   2729 |         0.317806 |          8662 |               540 |   0.0623413 |            8662 |                1315 |      0.151813 | nan            | nan            |   nan |           nan | nan        |         nan |             nan | nan       |     nan |     nan | nan        |     nan |
| QB         | T.Lawrence    |         219 |       nan |            nan |                nan |   nan        |                nan |                    nan |       nan        |           219 |               nan |   0.0593607 |             nan |                 nan |    nan        | all            | all            |   197 |           130 |   0.659898 |         197 |            1690 |   8.57868 |     197 |      13 |   0.282899 |     219 |
| QB         | T.Lawrence    |          67 |       nan |            nan |                nan |   nan        |                nan |                    nan |       nan        |            67 |               nan |   0.0597015 |             nan |                 nan |    nan        | blitz          | blitz          |    62 |            36 |   0.580645 |          62 |             435 |   7.01613 |      62 |       4 |   0.146624 |      67 |
| QB         | T.Lawrence    |         152 |       nan |            nan |                nan |   nan        |                nan |                    nan |       nan        |           152 |               nan |   0.0592105 |             nan |                 nan |    nan        | blitz          | no_blitz       |   135 |            94 |   0.696296 |         135 |            1255 |   9.2963  |     135 |       9 |   0.342967 |     152 |
| QB         | T.Lawrence    |         154 |       nan |            nan |                nan |   nan        |                nan |                    nan |       nan        |           154 |               nan |   0         |             nan |                 nan |    nan        | pressure_proxy | clean_proxy    |   154 |           108 |   0.701299 |         154 |            1363 |   8.85065 |     154 |       0 |   0.510742 |     154 |
| QB         | T.Lawrence    |          65 |       nan |            nan |                nan |   nan        |                nan |                    nan |       nan        |            65 |               nan |   0.2       |             nan |                 nan |    nan        | pressure_proxy | pressure_proxy |    43 |            22 |   0.511628 |          43 |             327 |   7.60465 |      43 |      13 |  -0.256915 |      65 |



PBP was_pressure column present: False. Proxy = qb_hit OR sack OR FTN is_qb_out_of_pocket OR qb_scramble. Positive known signals establish proxy pressure; clean requires all four known and false. Otherwise unknown. This proxy includes movement and is not a direct pressure measure. If was_pressure exists it additionally supplies the primary pressure split; proxy remains separately available.



Time to throw is not in PBP. qb_location/read_thrown are not time-to-throw or receiver alignment/route measurements.



## Shallow target / check-down proxy

air_yards <= 2 includes designed screens and short throws; it does not prove a progression check-down. Targets with null air yards cannot qualify. All tied rank-1 receivers below are leaders.

| receiver       |   targets | split_axis     | split          |   targets_n |    share |   rank |
|:---------------|----------:|:---------------|:---------------|------------:|---------:|-------:|
| Bhayshul Tuten |        16 | air_yards_le_2 | all            |          51 | 0.313725 |      1 |
| Bhayshul Tuten |         5 | air_yards_le_2 | pressure_proxy |          16 | 0.3125   |      1 |



## Route-area proxy and FTN coverage

route_area_proxy.csv uses pass_location × depth: <=0, 1–4, 5–14, >=15 air yards, plus unknowns. These are targeted-pass areas, not routes run or slot/outside alignments. Both Lawrence and team-all-QB versions are supplied. screens.csv counts FTN screen-target flags with charted N. FTN alignment/route fields found: none.



FTN columns: ftn_game_id, nflverse_game_id, season, week, ftn_play_id, nflverse_play_id, starting_hash, qb_location, n_offense_backfield, n_defense_box, is_no_huddle, is_motion, is_play_action, is_screen_pass, is_rpo, is_trick_play, is_qb_out_of_pocket, is_interception_worthy, is_throw_away, read_thrown, is_catchable_ball, is_contested_ball, is_created_reception, is_drop, is_qb_sneak, n_blitzers, n_pass_rushers, is_qb_fault_sack, date_pulled.



## Verification

Assertions passed: unique PBP/FTN join keys; one-to-one join; seven expected JAX weeks; 28 selected snap rows and seven appearances per player; target shares/counts reconcile; Lawrence blitz groups partition all dropbacks.



## Anomalies and limitations (final audit)

- Brian Thomas Jr. is Brian Thomas in snaps and Bri.Thomas in PBP. IDs distinguish him from DE Bryan Thomas Jr.; identities are normalized using GSIS/PFR IDs.

- QB attempt counts: {'Q.Ewers': 3, 'T.Lawrence': 198}; all-QB and Lawrence target tables therefore differ.

- JAX target nulls: air_yards=0; pass_location=0; attempts without named/identified receiver=6.

- Lawrence dropbacks=219; FTN unmatched=0; missing n_blitzers=0; missing n_pass_rushers=0; missing out-of-pocket=0; pressure-proxy unknown=0.

- JAX dropbacks with null passer: 9; all nine are Lawrence scrambles attributed using rusher identity and included in his dropbacks.

- Snap and PBP game counts match for all four players (7 each); roster has no Week 7 JAX entries. Snapshot cannot answer later weeks or establish an exact historical trade date.

- Missing FTN observations are never interpreted as no blitz. Small split samples and seven-game player samples limit conclusions. No receiver route/alignment or time-to-throw data supplied.
