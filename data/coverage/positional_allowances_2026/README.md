# 2026 positional defensive allowances, by window, opponent-adjusted (research only)

Built 2026-11-27 by Blitz for Rico's 12-priority mission (refs NFL-47). `projection_ready` stays **false**. Nothing here
changes a betting rule, gate, weight, skill or any `pregame/*.py` file. Nothing feeds the engine. No paid source, no
Odds API, no PFF.

This extends, and does not replace, the season-level tables in PR #143 (`data/coverage/defender_profiles_2026/`:
`team_allowed_by_position.csv`, `team_allowed_by_zone.csv`, `team_scheme_rates.csv`). Season WR/TE/RB targets,
catches, yards and TDs here reconcile **exactly** with PR #143's `team_allowed_by_position.csv` for all 32 defenses
(max difference 0 on every column; checked 2026-11-27). What is new: WR1/WR2/WR3 split, last-10/5/3 windows,
leave-one-out opponent adjustment, short/intermediate/deep and middle/outside splits, RB rushing + screen allowances,
QB allowances (scrambles vs designed runs), situational splits, and Sharp per-game man/blitz/pressure windows.

## Rebuild

```sh
python3 data/coverage/positional_allowances_2026/build_allowances.py --raw /path/to/raw [--through-week N]
python3 -m pytest -q data/coverage/positional_allowances_2026/tests
```

`--raw` holds the four nflverse files listed in `MANIFEST.json`. The builder checks each sha256 and stops on a mismatch.
`--through-week N` filters every nflverse input, for leak-free backtests of an earlier week. The Sharp package has no
week filter beyond its own weeks 1-10.

## Files

| File | Grain | What |
|---|---|---|
| `team_game_allowed.csv` | defense x game x group (WR1, WR2, WR3, WR_other, TE, RB, other, QB) | targets, catches, receiving yards, TD, INT, 20+ catches, red-zone targets, short/intermediate/deep and middle/outside targets and yards; RB rushing att/yds/TD/10+/20+/success, RB screen targets (FTN) and behind-the-line targets; QB dropbacks, attempts, completions, pass yards/TD/INT, sacks, scrambles + yards, designed QB runs + yards |
| `allowances_windows.csv` | defense x group x window (season, L10, L5, L3) | per-game averages, `_oa_pg` opponent-adjusted per game, totals, catch rate, yards/target, yards/catch, YPC, success and 10+ rates, completion %, sack rate, league rank (1 = most allowed) for raw and adjusted values |
| `allowance_trends.csv` | defense x group | L5 and L3 minus season for the headline yardage stat, rough z, flag UP / DOWN only at abs(z) >= 2 |
| `situational_allowed.csv` | defense x window x split | early down, 3rd down, 3rd-and-7+, red zone, shotgun, under center, FTN play-action, FTN blitz / no blitz: plays, pass rate faced, yards/play, EPA/play, success, EPA/dropback, 3rd-down conversion; `low_sample` under 30 plays |
| `sharp_defense_windows.csv` | defense x window | from Sharp advanced box scores, weeks 1-10: man rate, blitz rate, pressure rate, aDOT allowed, deep-target rate, play-action rate faced, EPA/dropback, explosive rate; change vs season |
| `MANIFEST.json` | build | input hashes, URLs, pull time, row counts, WR-rank stats |

## Definitions

- **Target**: pass attempt, not a sack, with a receiver id. Yards are the receiver's `receiving_yards` on catches
  (box-score basis: lateral yards are not credited; 14 catches this season where play yards and receiver yards differ, all 14 are laterals). Explosive catch = 20+ yards.
- **Depth** from `air_yards`: short < 10 (behind the line included), intermediate 10-19, deep 20+. Missing = unknown,
  kept as its own count.
- **Location** from nflverse `pass_location`, offense's view: middle vs outside (left or right). **This is not slot vs
  outside alignment.** No free 2026 source gives per-play receiver alignment (see gaps).
- **WR1/WR2/WR3** per offense per game: WRs with an offensive snap that game (snap counts) or a target, ranked by that
  player's targets for that team in **earlier** games; ties by that game's snaps. Week-1 ranks are snap-based (32
  offense-games). Active WRs mapped to gsis ids this build: all of them (0 unmapped).
- **Opponent adjustment**: for each defense-game, allowed minus the offense's own average for that group in its other
  games inside the build window (leave-one-out). Window value = mean over the window's games. A positive number means
  the defense gave up more than that offense usually gets. It uses the offense's games both before and after the
  defense-game, so it is only leak-free relative to the `--through-week` cut, not game by game.
- **Windows**: the defense's last 3, 5 and 10 games played, plus full season. `partial_window` is true when a team has
  fewer games than the window size.
- **RB screens** use FTN `is_screen_pass`; FTN is charted through week 11 only, so week-12 screens are not counted.
  "Behind the line" (air yards <= 0) is a plain, checkable stand-in for checkdowns; it is not a label FTN provides.
- **Sharp windows** pool sums over the defense's opponents' rows (`man` / `cov`, `blitz` / `db`, `prsr` / `db`). Sharp
  writes the Rams as LAR; mapped to LA.

## Example outputs (2026 through Nov 26)

**1. Rams (LA) defense vs opposing WR1s**, season vs L3 (weeks 9, 10, 12):

| Window | Tgt/g | Rec/g | Yds/g | Opp-adj yds/g | Rank (1 = most) | Middle yds/g | Outside yds/g | Deep yds/g |
|---|---|---|---|---|---|---|---|---|
| Season (11 g) | 5.3 | 2.8 | 37.6 | -13.8 | 30th | 11.0 | 26.6 | 7.4 |
| L3 | 3.3 | 1.3 | 30.0 | -31.1 | 29th | 0.0 | 30.0 | 27.0 |

Slot vs outside for the same defense is only available as Sharp's season-level yards per target (page updated Nov 24):
outside 7.1, slot 8.5. No window version exists in free data.

**2. Dallas defense vs opposing QBs** (descriptive; the no-passing-yards-legs rule is unchanged):

| Window | Dropbacks/g | Pass yds/g | Opp-adj | Cmp % | Sack rate | Rank |
|---|---|---|---|---|---|---|
| Season (12 g) | 36.6 | 258.4 | +41.6 | 68.1% | 7.3% | 4th |
| L5 | 39.2 | 291.0 | +88.8 | 67.3% | 11.2% | 2nd |
| L3 | 36.0 | 322.7 | +113.5 | 72.7% | 13.9% | 2nd |

Sharp box scores (weeks 1-10 only) show Dallas's man rate rising: season 30.1%, L5 33.7%, L3 35.9%. Sharp's season
slot vs outside YPT for Dallas: slot 10.3, outside 8.2. The trend z for the L3 jump is below 2, so it is flagged
"noise", not a confirmed shift.

**3. Washington defense vs tight ends**:

| Window | Tgt/g | Rec/g | Yds/g | Opp-adj | RZ tgt/g | Short yds/g | Inter yds/g | Rank raw / adj |
|---|---|---|---|---|---|---|---|---|
| Season (10 g) | 9.1 | 6.9 | 80.4 | +34.1 | 2.1 | 44.7 | 29.0 | 1st / 1st |
| L3 | 11.7 | 8.3 | 93.3 | +35.5 | 2.0 | 50.7 | 32.0 | 1st / 1st |

## Data-quality notes

- Week 12 is partial: only the four Thanksgiving games (Nov 26) are in. Most defenses have 10-11 games.
- Sharp box-score windows stop at week 10. Pooled man rate from the box scores tracks Sharp's season page (Nov 17
  pull) closely: correlation 0.95, mean absolute gap 3.6 points; biggest gaps KC +9.0, NE +7.9, NYG +6.7, DEN -4.1.
- Sharp and StatRankings chart differently (PR #143 notes Sharp man % runs about 15 points lower). This folder uses Sharp
  only. Do not mix the two on one read.
- L3 samples are 3 games. The trend z treats the L3 games as independent of the season mean they sit inside, so it
  overstates confidence; with abs(z) >= 2 required, no defense-group was flagged UP or DOWN this build.
- Opponent adjustment uses raw per-game means; it does not adjust for game script, pace or the offense's injuries.
