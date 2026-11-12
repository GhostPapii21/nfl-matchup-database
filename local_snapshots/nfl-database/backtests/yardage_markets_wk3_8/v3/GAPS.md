# Gaps and leakage risks

No network or environment keys used. v2 outcomes, features and Sharp hindsight excluded; only identity/consensus quote columns reused. Prior-week features use weeks strictly <w; week 7 statistics may inform week 8 features, but no week 7–8 market outcomes are computed. Training settlement aggregates only weeks 3–6.

Snap share: saved /tmp/snap_counts_2026.parquet, linked by players.parquet pfr_id; player offensive snaps / sum of team per-game maximum offensive snaps, including missed games. Missing identity/participation remains missing. RB carry share uses all team carries including QB; second-back share is second largest RB share of all team carries. Targets exclude sacks and require identified receiver. Position allowance uses static players.parquet position and all opponent prior games. Static position/identity metadata and retrospective corrections to historical pbp/snaps can introduce revision bias. v2 team identity retained; v2 derived it from prior participation.

Injuries: /tmp/inj26.parquet inspected; no report dates or publication timestamps. All injury features missing; week alone is insufficient proof of availability as of kickoff.

Weather: saved weather JSON files inventoried in weather_inventory.txt. Use shared_src weather hourly Open-Meteo entries only where saved _pulled_et/pulled_et (America/New_York) <= kickoff, home-team linkage matches, roof is open, and forecast valid hour is within one hour of kickoff. Latest issuance then nearest hour wins. Missing weeks/games remain missing; no indoor weather used. Snapshot issuance is a locally recorded collection timestamp, not independently audited. Array-only matchup forecasts are unused because valid hours are absent.

Odds: saved h2h/spreads/totals scanned in allowed raw/run/week roots; require snapshot and market update <=kickoff, latest per book/market/outcome, median across books. Kickoff exact match and teams required. Odds use pre-kick data but may be later than prop consensus snapshot, so strategy assumes decision at kickoff. Consensus prices are estimates, potentially unquoted median; missing prices abstain. No closing-only odds invented.

Overfit risk: five thresholds per cell, univariate traits exploratory, no validation beyond train. Product slip odds ignore correlation and SGP repricing. Source coverage and unknown players limit interpretation.

Week 3 saved pre-kick coverage: h2h 0/16 games, spreads 0/16 games, totals 0/16 games. Zero means week lacks that market; partial coverage leaves remaining games missing.

Week 4 saved pre-kick coverage: h2h 0/16 games, spreads 0/16 games, totals 0/16 games. Zero means week lacks that market; partial coverage leaves remaining games missing.

Week 5 saved pre-kick coverage: h2h 0/15 games, spreads 0/15 games, totals 0/15 games. Zero means week lacks that market; partial coverage leaves remaining games missing.

Week 6 saved pre-kick coverage: h2h 14/14 games, spreads 14/14 games, totals 14/14 games. Zero means week lacks that market; partial coverage leaves remaining games missing.

Week 7 saved pre-kick coverage: h2h 14/14 games, spreads 14/14 games, totals 14/14 games. Zero means week lacks that market; partial coverage leaves remaining games missing.

Week 8 saved pre-kick coverage: h2h 13/13 games, spreads 13/13 games, totals 13/13 games. Zero means week lacks that market; partial coverage leaves remaining games missing.

Feature missing counts by week:

      position  prior_games  prior_carry_share  prior_snap_share  second_back_share  prior_target_share  opp_rush_yds_game  opp_rush_yds_carry  opp_rec_yds_position_game  prior_yds_avg  spread  total  implied_team_total  favored  injury_status  weather_temp  weather_wind
week                                                                                                                                                                                                                                                                           
3            0            0                 22                22                 22                  22                 22                  22                         82             22     684    684                 684      684            684           684           684
4            0            0                 10                12                 10                  10                 10                  10                         74             10     696    696                 696      696            696           696           696
5            0            0                 10                12                 10                  10                 10                  10                         70             10     632    632                 632      632            632           632           632
6            0            0                 18                20                 18                  18                 18                  18                         78             18      18     18                  18       18            650           650           650
7            4            0                 22                24                 22                  22                 22                  22                         80             22      22     22                  22       22            634           634           634
8            4            0                 14                14                 14                  14                 14                  14                         66             14      14     14                  14       14            596           236           236
