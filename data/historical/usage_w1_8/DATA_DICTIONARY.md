# Data dictionary: WEEK9_PLAYER_USAGE.csv (long format; one row per gsis_id x window x metric)
- gsis_id: nflverse GSIS id (from roster_weekly W9; never name-guessed). player_name, team (current W9 roster team), opponent (W9 Sunday opponent), position (roster).
- window: SEASON_W1_8 = all player games W1-8; L5_PLAYER_GAMES = player's last 5 ACTUAL games (not calendar weeks); L10_AVAILABLE_MAX8 = last up-to-10 games, only 8 weeks exist so n_games<=8 (equals season).
- value: blank = missing/unsourced (never zero-filled); 0 = observed zero. unit; n_games = games in window; n_plays_or_opps for opportunity metrics.
- denominator / denominator_definition: for shares/rates. coverage_numerator/denominator: games with the input present (snaps).
- source/source_url/source_sha256/source_asof (nflverse release asset updated_at, UTC)/retrieved_at (ET)/observation_through/metric_method/missing_flag/missing_reason/availability_role_evidence.
## Definitions
- PBP: canonical 121 W1-8 REG game_ids; two_point_attempt==0; play_type 'no_play' excluded except *_incl_no_play.
- pbp_dropbacks: qb_dropback==1 keyed passer_player_id, else rusher_player_id (435 null-passer scrambles); includes sacks and scrambles. pbp_scrambles: qb_scramble==1 keyed rusher. pbp_designed_rushes: play_type run & qb_scramble0 & qb_kneel0. pbp_kneels qb_kneel==1; pbp_spikes qb_spike==1. QB opps = dropbacks + designed rushes (disjoint).
- pbp_pass_attempts: pass_attempt==1 & sack==0 & play_type pass. Stats vs PBP attempt differences are reported (attempts_stats_minus_pbp, QA_ATTEMPT_MISMATCH.csv), not resolved.
- targets (stats) vs pbp_targets (play_type pass & receiver_player_id notnull). target_share = player targets / team targets (team sum of stats targets, same games). carry_share analog with carries.
- reported_snap_share_game_mean = mean of source-reported offense_pct (nflverse snap_counts). snap_share_derived_estimated_denominator = offense_snaps / ESTIMATED team snaps (median offense_snaps/offense_pct of players >=50%); not observed. Game logs include reported_offense_pct per game.
- adot = sum air_yards / pbp targets with non-null air_yards. deep target: air_yards>=20. RZ target: yardline_100<=20; also <=10.
- pbp_targets_pass_location_*: PBP pass_location (throw direction), NOT slot/outside alignment.
- RB pbp_carries_run_location_* / run_gap_*: PBP-recorded direction/gap; NOT run concept. Goal-line carries: yardline_100<=5 and <=2; RZ carries <=20.
- routes_run, route_participation, slot_rate, outside_alignment_rate, run_concept_split, coverage_splits: always blank, UNSOURCED_NOT_ESTIMATED.

V2 metadata: qb_starter_confirmation and qb_starter_source_url reference the latest official starter evidence or explicit lack of confirmation; roster membership is not confirmation of game-day active status.
