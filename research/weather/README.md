# Rain and wind: what they do to passing

Measured from nflverse play-by-play, seasons 2018 to 2026: 4,487 team-games, of which
211 were played in rain. Each rainy game is compared with the same team's dry games in the
same season, and rain and wind are fitted together (rainy games are windier, and wind hurts passing by itself).
Research only; nothing here has been tested against prices.

## The equation

    R = 1 if it rains (or the chance of rain, 0 to 1, for an expected value)
    W = max(0, wind in mph - 10) / 10

    attempts'        = attempts        x (1 + a_rain R + a_wind W)
    targets_i'       = attempts' x target share_i x (1 + s_wind W)
    catch rate_i'    = catch rate_i    x (1 + c_rain R + c_wind W)
    yards/target_i'  = yards/target_i  x (1 + y_rain R + y_wind W)

    receptions_i'    = targets_i' x catch rate_i'
    yards_i'         = targets_i' x yards/target_i'

The player's own numbers (target share, catch rate, yards per target) come from his recent games; the bracketed
factors come from the table below, by position. Code: `pregame/rain_model.py`. Every outdoor game's pregame packet
carries the result as "Rain-adjusted passing".

## Measured effects

| Measure | Dry baseline | In rain | Per 10 mph of wind above 10 |
|---|---|---|---|
| Pass attempts | 33.8 | -4.3% | -4.2% |
| Completion rate | 0.652 | -6.0% | -3.4% |
| Yards per attempt | 7.29 | -12.0% | -8.4% |
| Team pass yards | 243 | -14.6% | -11.8% |
| Yards per completion | 11.2 | -5.7% | -5.1% |
| Yards after catch per completion | 5.27 | -9.0% | no clear change (+1.0%) |
| Depth of target | 7.88 | no clear change (-1.4%) | -5.6% |
| Share of deep passes (20+ air yards) | 0.117 | no clear change (-1.1%) | -12.9% |
| Pass rate (dropbacks / plays) | 0.611 | -3.3% | no clear change (-1.8%) |
| Interception rate | 0.0227 | no clear change (+9.0%) | no clear change (-2.1%) |
| Sack rate | 0.0638 | no clear change (+1.9%) | no clear change (+5.1%) |
| WR target share | 0.59 | no clear change (-1.4%) | no clear change (+1.3%) |
| TE target share | 0.217 | no clear change (+1.0%) | -7.5% |
| RB target share | 0.191 | no clear change (+2.8%) | +5.1% |
| WR catch rate | 0.635 | -6.5% | -3.2% |
| TE catch rate | 0.7 | -6.9% | -7.1% |
| RB catch rate | 0.775 | -3.9% | no clear change (-2.6%) |
| WR yards per target | 8.18 | -11.3% | -11.5% |
| TE yards per target | 7.37 | -11.5% | -12.4% |
| RB yards per target | 5.87 | -12.9% | no clear change (+2.6%) |

"No clear change" means the measured change is smaller than about two standard errors; the model leaves those at zero.

What it says in plain terms:

- Rain costs about 4 completion points and about 12% of yards per attempt. Team passing yards fall about 15%.
- Teams throw only slightly less (about 4% fewer attempts). Rain hurts efficiency much more than volume.
- Who gets the ball does not change in rain: wide receiver, tight end and running back target shares stay put.
  Wind is different: tight ends lose share and running backs gain a little.
- Rain does not make teams throw shorter (depth of target is unchanged). The yards lost are missed catches and
  less running after the catch. Wind is what shortens throws: deep passes drop about 13% per 10 mph.
- Interceptions and sacks do not clearly change.

## Light, moderate and heavy rain

The data cannot separate them. Game records are free text written by team staff, almost always just "Rain"
(137 team-games); only 46 say light rain, drizzle or showers, and almost none say heavy. When the
tiers are fitted separately the "light" games do not come out milder than the rest, which means the labels are
noise, not a scale. So the model uses one rain step and lets wind carry severity: a calm drizzle is R = 1, W = 0;
a driving rain at 20 mph is R = 1, W = 1. To grade rain by intensity you would need hourly rainfall for each
game, which is not in any source this repository uses.

## Limits

- The weather text describes kickoff, not the whole game.
- A forecast "74% chance of rain" is used as R = 0.74, an average of the dry and rain cases. It will either rain or not.
- The effects are league averages. A quarterback with small hands or a receiver with poor hands in the wet may differ;
  there is not enough data per player to measure that (most players have two or three rain games).
- Player baselines are recent averages. Injuries, a quarterback change and game script are not in the equation.

Refit: `python3 research/weather/fit_rain_effects.py <folder of play_by_play_YYYY.parquet> ...` (files from nflverse).
