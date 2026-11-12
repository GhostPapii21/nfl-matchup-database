# Locked train matchup/script/role rules

Pre-specified grid: 1–3 conditions on distinct features per market-side. Each numeric feature offers only low (<= train 1/3 quantile) and high (>= train 2/3 quantile) tails. Cutpoints use available weeks 3–6 feature values within each market-side before guards, with linear interpolation. Favored and available injury/weather flags offer equality conditions. No missing-value conditions. Numeric grid: prior_carry_share, prior_snap_share, second_back_share, opp_rush_yds_game, opp_rush_yds_carry, opp_rec_yds_position_game, prior_target_share, spread, implied_team_total, model_edge, weather_temp, weather_wind.

At least one condition must use a matchup/script/role feature; the prior-average gap is optional and can appear at most once. Keep only graded train cells with n>=30 and ROI>0. Pick highest ROI*n/(n+50); ties favor larger n, fewer conditions, then fixed grid order. Every tested/qualifying cell count and full-precision cutpoint is recorded in locked_rules.json.

All RB overs require prior carry share >=60%, in addition to the 1–3 searched conditions. Missing position on overs, required values or valid price abstains. Statistics use $10 stakes before cross-rule player deduplication; hit rate excludes pushes. Injury/weather data are unavailable in train and yield no conditions. This expanded search remains exploratory and subject to selection overfit.

Single-player and slip ordering remains directional prior-average gap, price, candidate ID, without outcomes; the gap is not an implicit eligibility filter.

recyds over: prior offensive snap share at least 0.68939394 AND opponent rushing yards allowed per game at most 100 AND prior team target share at least 0.16071429. Train n=39, wins/losses/pushes=26/13/0, hit=66.67%, P/L=$98.39, ROI=25.23%; shrinkage score=11.0545.

recyds under: prior offensive snap share at least 0.68939394 AND opponent rushing yards allowed per game at least 120.33333. Train n=44, wins/losses/pushes=32/12/0, hit=72.73%, P/L=$161.25, ROI=36.65%; shrinkage score=17.1541.

rushrecyds under: prior team carry share at most 0.27582594. Train n=34, wins/losses/pushes=22/12/0, hit=64.71%, P/L=$72.95, ROI=21.46%; shrinkage score=8.6844.

rushyds over: opponent rushing yards allowed per game at least 120.5 AND prior team target share at most 0. Train n=31, wins/losses/pushes=20/11/0, hit=64.52%, P/L=$68.11, ROI=21.97%; shrinkage score=8.4091.

rushyds under: opponent rushing yards allowed per carry at most 3.84375 AND prior team target share at most 0. Train n=37, wins/losses/pushes=27/10/0, hit=72.97%, P/L=$137.72, ROI=37.22%; shrinkage score=15.8302.

rushrecyds over: no qualifying cell; no bets.
