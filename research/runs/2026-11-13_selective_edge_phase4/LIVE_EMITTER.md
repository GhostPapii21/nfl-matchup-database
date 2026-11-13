# Phase 4 live: roster join + pre-kickoff flag emitter (stacked on PR #40; refs NFL-75)

**Research only, not picks, not vetted. `projection_ready` stays false. 0 Odds API credits.**
The frozen classifier files and `params_w4_7.json` are not edited here; `pregame/` and `.github/` are untouched.

## Roster join (`calibration/selective_edge_roster.py`)
Adds `gsis, position, team, roster_week, roster_match, season_car, season_team_car, season_carry_share, season_games`
plus `roster_source, roster_pulled_utc, pbp_source, pbp_pulled_utc` to every leg.
- Only the two teams in the game_id are searched; the player's latest weekly-roster row with week <= leg week is used.
- Names are matched after dropping case, punctuation and Jr/Sr/II/III/IV/V. No match or two different ids -> gsis and
  position stay **unknown**, and the frozen classifier labels the rushing leg INSUFFICIENT EVIDENCE (`position_unknown`).
- Season carry share = carries / team carries over REG games in weeks < leg week in which he had a carry or target.
  It is informational; the N1 gate still uses >=60% in >=3 of the last 4 prior games (`selective_edge.attach_context`).
- A roster or PBP without a pull time is refused.
- Roster committed: `data/historical/nflverse/roster_weekly_2026_w1_10_pulled_20261113T1633Z.parquet` (nflverse,
  pulled 2026-11-13 16:33:47 UTC = 11:33 AM EST, provenance JSON alongside).
- Smoke on the real WAS@NYG freeze_v2 (72 legs): 72/72 matched by name, positions populated, so the RB gate now runs on
  the live path (before: position blank on 72/72).

## Probabilities: schema `nfl75-rush-dist/1` (draft PR #43, `pipeline/rush_dist.py`)
The emitter reads `<game>.rush_dist.cdf.csv` (`game_id, team, player, gsis, position, line, p_under, p_over`, half-yard
lines, `p_under = P(rush_yds < line)`), checks the `.json` sidecar schema, and fills `p_model` on rushyds legs by
**(game_id, gsis) only**: `p_model = P(side) / (P(under) + P(over))` at the leg line (integer line L: P(X<L) =
p_under(L-0.5), P(X>L) = p_over(L+0.5)). Unlike PR #43's `attach_p_model`, there is no name fallback; an unmatched leg
keeps p_model blank -> INSUFFICIENT EVIDENCE (`model_prob_missing`). A legs row with a preset p_model is never overwritten.

## Emitter (`calibration/selective_edge_emit.py`)
```bash
python3 -m calibration.selective_edge_emit --date 2026-11-15 \
  --freeze pregame/price_freezes/<date>_<AWAY>@<HOME>/freeze_v2_<stamp>.json [--freeze ...] \
  --probs pipeline/ledgers            # dir of <game>.rush_dist.cdf.csv, or the files themselves
  --roster data/historical/nflverse/roster_weekly_2026_w1_10_pulled_20261113T1633Z.parquet \
  --pbp data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet \
  [--prob-source sim_v5_v6_ensemble --qb-override-applied]
  [--commit] [--push]
```
Pull times default to the `<file>.retrieved_utc` sidecar or `<file>.provenance.json`; pass `--roster-pulled-utc` /
`--pbp-pulled-utc` otherwise. Per game it refuses: kickoff unknown, now >= kickoff (`kicked_off`), price pull time
unknown, at/after kickoff, or in the future. If no game survives nothing is written. Weeks outside 10-12 are refused and
`grade_live` checks the freeze manifest before labeling (frozen params, no refit).

Writes (never overwrites) `research/runs/<date>_live_flags/flags_<UTCstamp>.{csv,json,md}`: every leg with label,
reason, edge, price, provenance, `emitted_utc`, `emitted_et`, `kickoff_utc`, `kickoff_et`, `minutes_to_kickoff`,
`price_minutes_before_kickoff`, `countable`, `prob_source`, `countable_reason`; the JSON has run time UTC + ET, input
sha256s, emitter code sha256s, the freeze manifest sha256, per-game refusals, and the countable stamp. `--commit`
stages only that run's files on the current `research/*` branch (refuses any other path, and refuses pregame/ or
.github/); `--push` pushes that branch only after checking the branch diff vs origin/main does not touch pregame/ or
.github/. Commit messages say "refs NFL-75".

## Countable stamp
Every flag gets `countable`, `prob_source` and `countable_reason`. `countable=true` only when the caller declares
`--prob-source sim_v5_v6_ensemble` (the legacy sim_v5/v6 ensemble the Phase 4 classifier was fit on) AND
`--qb-override-applied` (depth-chart/inactives QB override). Missing or unknown sources, and PR #43's
`nfl75-rush-dist/1` possession-engine output, are fail-closed `countable=false` (reasons:
`prob_source_missing`, `prob_source_unknown`, `prob_source_not_fit_ensemble`, `qb_override_missing`). STRONG UNDER
labels are still written; the markdown summary marks non-countable flags `[NOT COUNTABLE: <reason>]`. The default CLI
path (no `--prob-source`) is not countable.

## Still blocking a countable Sunday spot
1. Sunday freeze_v2 price files (a paid Odds API pull that needs approval; none exist for Sunday yet).
2. Per-game probabilities from the legacy sim_v5/v6 ensemble the classifier was fit on, with the depth-chart/inactives
   QB override applied. The only source wired today is PR #43's `rush_dist` CDFs; those flags stay `countable=false`
   (`prob_source_not_fit_ensemble`) even if they print STRONG UNDER. PR #43 also notes that starter identity comes from
   history, not the depth chart, and that player means sit far from the market.
3. Receiving legs stay INSUFFICIENT EVIDENCE until a main-defender source exists.
