# Bengals–Falcons 9:30 ET pregame projection lock

**Frozen:** 2026-11-08 09:08 ET, before scheduled 09:30 ET kickoff. **Status:** prospective research artifact; not a calibrated forecast or bet recommendation.

## Reproduce the run

From this directory, run:

```bash
python run_cin_atl_930.py
```

The runner reads only the four frozen CSV inputs in this directory and writes `simulation_100k_20261108_0908ET.csv`. It makes 100,000 bootstrap draws per market/book/model row (183 rows; 18.3 million total draws), with fixed seeds stored in the output. The draws resample the player's Weeks 1–8 values only from games with a positive recorded market opportunity; zero statistical outcomes in an eligible opportunity game stay in the sample. The rolling model uses the last five such games. The third candidate applies a capped, opponent team-level allowed-rate factor to those five outcomes. It is a sensitivity model, not a fitted or validated adjustment.

The player history is a pregame extract of verified nflverse-derived player-game records. Team-defense inputs are the pregame Week 1–8 aggregate snapshot. The line file is an aggregator capture retrieved at 09:08 ET; its underlying sportsbook quote timestamps were not exposed. Prices therefore are a working snapshot, not authenticated live sportsbook API quotes. Line-source URLs and limitations are preserved in the line CSV.

## How to interpret the output

`p_over`, `p_push`, and `p_under` are finite-sample resampling frequencies. They are not calibrated probabilities. `historical_hit_rate_at_current_line` applies today's line to the player's Weeks 1–8 outcomes; this is descriptive and in-sample, not a forward backtest. With only six to eight games, candidate estimates are noisy and discrete. Large differences between models indicate instability; do not treat the largest probability as the preferred estimate.

The prior model trial file in `research/WEEK9_DAY1_MODEL_TRIALS_20261108.md` showed that the opponent adjustment did not consistently improve Weeks 7–8 point-forecast MAE, and there are no historical prop lines in this package to compute Brier score, log loss, or probability calibration. Today's final results must be joined to this frozen forecast before scoring the prospective run.

## Pregame evidence and limits

- NFL official schedule listed Cincinnati at Atlanta for 09:30 ET at Bernabéu Stadium in Madrid. Official inactive report was published at 08:05 ET. Cincinnati inactives: S Kyle Dugger, C Connor Lew, OT Myles Hinton, DT Landon Robinson. Atlanta inactives: QB Andy Dalton (emergency third QB), QB Jack Strand, WR Zachariah Branch, DB Billy Bowman, DB Robert Longerbeam, DE Drake Jackson. Atlanta RB Brian Robinson was already on injured reserve. These lists confirm availability status; they do not establish snap limits for active players.
- Coarse W1–8 team defense snapshot: Atlanta allowed 237.5 passing yards, 118.25 rushing yards, and 23.25 receptions per game across eight completed games; Cincinnati allowed 261.0 passing yards, 122.29 rushing yards, and 22.0 receptions per game across seven games.
- The defense input has no pressure/blitz rate, man/zone split, MOFO/MOFC chart, explosive-pass count, or individual defender responsibility. Do not infer a CB/S assignment or an individual defender's yards/receptions allowed from these team totals.
- A Madrid forecast retrieved at 09:19 ET showed cloudy conditions near kickoff and about 62°F around 4 p.m. local. A Bengals article reported that center Ted Karras expected Bernabéu's retractable roof to be closed, but I found no confirmation of its actual game-day position. I therefore apply no weather adjustment; if closed, outdoor wind/rain would not affect the field.
- The bootstrap does not model team play volume, share competition, game script, injuries beyond the inactive check, route participation, target depth, or correlations among players/markets. Its output is a conditional historical-outcome benchmark, not a full structural player projection.

## Source links

- NFL Week 9 official inactives: <https://www.nfl.com/news/nfl-week-9-inactives-players-ruled-out-sunday-2026-season>
- Bengals official inactives: <https://www.bengals.com/news/bengals-falcons-inactives-week-9-2026>
- Falcons official inactives: <https://www.atlantafalcons.com/news/atlanta-falcons-week-9-inactives-cincinnati-bengals>
- Official schedule and venue: <https://operations.nfl.com/calendar-events/nfl-important-dates>
- Bengals travel / stadium article on expected roof position: <https://www.bengals.com/news/bengals-madrid-travel-logistics-falcons-nfl-international-series-2026>
- nflverse data repository and CC-BY 4.0 attribution: <https://github.com/nflverse/nflverse-data> and <https://github.com/nflverse/nflverse-data/blob/main/LICENSE.md>

## Frozen input SHA-256

- `book_lines_20261108_0908ET.csv`: `4a3a6057bd11170920fa9ebdcb10e4251aaa7a63b0a769c9d06374ba553065bf`
- `defense_inputs_pre_game_w1_w8.csv`: `b6494082c46a345a68bad572ecff8a295baa732345b54a591e576f14fdc5a87a`
- `player_game_history_w1_w8.csv`: `8255d62577a00de31708bbe9967e62c36c4ebd2401d603cfddc0e81a642aee38`
- `run_cin_atl_930.py`: `e057663fd16115c06290b3c93851dd578b48317b37ea7b0a7383c9ae3c4f9de1`
- `simulation_100k_20261108_0908ET.csv`: `fdcd0c4b5d6eb69b24159b8ef83ff66d15833eb87b290203ef6cce8f087ad3cc`
