# sim_v7 — three-method × three-script NFL simulation (research only)

**This is a new engine, not the original sim_v6.** The original is recovered verbatim in
`engines/sim_v6_recovered/` (blob `ab2144f03f6ca3b57950a1f2528e305193e723cd` verified, from
`research/matchup-database-local-2026-11-12@dc36f7f2`). It runs (100K, 1.1 s for one leg), but its `bias` mode
is the MC sampler with a per-market multiplier (same median and M as `mc` in the re-run), and it has no game-script
axis, so it cannot satisfy the 3×3 contract. Status of all outputs: `RESEARCH_ONLY_NOT_PROJECTION_READY`.

## Methods (genuinely different samplers)
| method | how it samples | correlation mechanism |
|---|---|---|
| `mc` | Team TD/FG ~ Poisson around market-implied points; per-team efficiency shock; shared pace; scores allocated to quarters; pass/rush volume from simulated margin (league-fitted log-linear slopes); Beta/multinomial target & carry shares; Beta catch rate; Gamma yards; TDs allocated from team TDs by red-zone share | player TDs ⊂ team TDs ⊂ points; QB yards = Σ receiver yards; volume follows margin; yards share the efficiency shock with points |
| `bias` | `mc` draws mapped through a per-market PIT recalibration map fitted on chronological walk-forward residuals (shrunk to identity by n/(n+K), K chosen on validation) | monotone per-draw transform → joint structure with team score preserved |
| `gr` | Possession engine: alternating drives on a 60-min clock (half-time possession switch); each drive resampled from the team's real last-8-game drives in the same state bucket (trail 8+/within 7/lead 8+) × half; each drive carries its real duration, points and every player's real production | everything comes from the same real drives, so script, score, quarter score and player lines are jointly empirical |

Scenarios (favorite perspective, disjoint, by rejection sampling until 100,000 accepted per cell):
`favorite_controls` H>0 and F≥10 · `competitive` |H|≤6 and |F|≤7 · `underdog_chases` H≥7 and F<10
(H = first-half margin, F = final regulation margin). `scenario_acceptance_rate` = that method's unconditional
probability of the script. **Line probabilities are conditional on the scenario.**

## Run
```bash
pip install pyarrow pandas numpy pytest
python3 -m pytest -q engines/sim_v7/tests                      # 7 tests
python3 -m engines.sim_v7.cli smoke                            # determinism check (2,000 trials)
python3 -m engines.sim_v7.cli run --slate 2026-11-29 --n 100000 --out runs/sim_v7_2026-11-28/out
python3 -m engines.sim_v7.cli run --game 2026_12_NO_CIN --n 100000 --out <dir>
# re-fit calibration
python3 -m engines.sim_v7.calibration backtest --season 2025 --weeks 5-18 --out bt25.csv
python3 -m engines.sim_v7.calibration backtest --season 2026 --weeks 3-11 --out bt26.csv
python3 -m engines.sim_v7.calibration fit --rows bt25.csv bt26.csv --out engines/sim_v7/calibration_v7.json
```
Python: `from engines.sim_v7.cli import simulate_game; doc = simulate_game("2026_12_NO_CIN", n=100_000)`.

## JSON contract (`records[]`)
`game_id, player_id, player_name, team, position, market, method, scenario, trial_count, seed, distribution
{p5,p10,p15,p20,p25,median,mean,sd,p75,p90,p95}, line_probabilities[{book,line,p_over,p_under,p_push}],
calibration_status, input_hash, source_cutoff, execution_status, scenario_acceptance_rate, raw_trials_generated`.
Player markets: QB `pass_att, pass_cmp, pass_yds, pass_td, rush_att, rush_yds, rush_td`; RB/WR/TE `targets,
receptions, rec_yds, rec_td, rush_att, rush_yds, rush_td, rush_rec_yds, anytime_td`. Game markets: team points,
total, home margin (with book spread cover), Q1–Q4 points, 1H points, `q1..q4_winner`, `1h_winner`,
`game_winner_regulation` (home/away/tie). `meta` carries players modeled, history game ids, excluded (Out/IR)
players, calibration artifact as_of, file sha256 provenance, runtime.

Inputs: nflverse pbp 2024, 2025, 2026 wk1-11 (`source_cutoff` 2026-11-24, exclusive), `dashboard/data/<game>.json`
(consensus spread/total, book prop lines retrieved 2026-11-27T04:26Z, injury lists). Nothing is written to a
database; nothing is promoted.

## Historical validation (actually executed, `calibration_v7.json`)
Train 2025 wk5–18 (17,173 rows) · validation 2026 wk3–7 (5,898) · walk-forward test 2026 wk8–11 (3,359 rows,
42 games). 16 games named in `*LOCK*.json` files excluded from every phase. Structural zeros (MC P90 = 0) dropped
using pre-game info only. Model inputs for week W use only plays before week W's first kickoff. K=200 selected.
`bias` column below = median − actual. Brier is at a **proxy line** (player's trailing median + 0.5), not a
sportsbook line — historical book prop lines were not available for this run.

| market | status | n | MAE mc / cal / gr | bias mc / cal / gr | CRPS mc / cal / gr | Brier mc / cal / gr | 80% cov mc / cal / gr |
|---|---|---|---|---|---|---|---|
| pass_att | VALIDATED | 70 | 7.22 / 7.30 / 8.31 | 2.45 / 1.73 / 0.16 | 5.50 / 5.39 / 6.06 | .244 / .243 / .268 | .76 / .79 / .70 |
| pass_cmp | VALIDATED | 70 | 5.56 / 5.15 / 5.73 | 2.64 / 1.32 / 0.19 | 4.20 / 3.94 / 4.24 | .273 / .250 / .271 | .71 / .79 / .73 |
| pass_yds | VALIDATED | 70 | 71.0 / 70.7 / 69.3 | 8.8 / 4.9 / −10.3 | 51.3 / 50.9 / 51.1 | .281 / .278 / .264 | .79 / .70 / .67 |
| pass_td | EXPERIMENTAL_UNVALIDATED | 70 | 1.03 / 1.02 / 1.06 | −.23 / −.23 / −.20 | .742 / .736 / .705 | .260 / .261 / .247 | .94 / .94 / .89 |
| targets | EXPERIMENTAL_UNVALIDATED | 569 | 1.77 / 1.76 / 1.93 | −.63 / −.25 / −.58 | 1.33 / 1.32 / 1.43 | .237 / .237 / .245 | .89 / .88 / .81 |
| receptions | EXPERIMENTAL_UNVALIDATED | 569 | 1.39 / 1.37 / 1.48 | −.41 / −.15 / −.42 | 1.04 / 1.03 / 1.11 | .227 / .227 / .247 | .92 / .90 / .81 |
| rec_yds | VALIDATED | 569 | 19.1 / 18.9 / 19.9 | −8.9 / −5.3 / −7.7 | 14.25 / 14.15 / 14.88 | .244 / .243 / .259 | .85 / .86 / .77 |
| rec_td | EXPERIMENTAL_UNVALIDATED | 320 | .263 / .266 / .281 | −.26 / −.26 / −.19 | .211 / .212 / .227 | .160 / .160 / .171 | .98 / .98 / .93 |
| rush_att | VALIDATED | 406 | 2.40 / 2.43 / 2.52 | −1.11 / −1.26 / −1.07 | 1.82 / 1.82 / 1.95 | .266 / .261 / .235 | .87 / .89 / .81 |
| rush_yds | EXPERIMENTAL_UNVALIDATED | 406 | 12.2 / 12.3 / 12.9 | −6.4 / −7.2 / −5.0 | 9.48 / 9.48 / 10.03 | .225 / .223 / .226 | .84 / .85 / .77 |
| rush_td | EXPERIMENTAL_UNVALIDATED | 156 | .353 / .357 / .372 | −.25 / −.25 / −.19 | .256 / .258 / .277 | .177 / .175 / .190 | .99 / .99 / .94 |
| team_points | EXPERIMENTAL_UNVALIDATED | 84 | 8.32 / 8.20 / 8.21 | −1.27 / −.18 / .45 | 6.12 / 6.09 / 5.94 | .251 / .253 / .248 | .87 / .81 / .75 |

Favorite-win Brier: validation (75 games) MC .236 / GR .259; test (42 games) MC .213 / GR .189. 2026 wk7+
schedule rows have no spread/total in `games.csv`, so MC used derived (non-market) implied points there — this
understates MC in the test phase (mean p .55 vs observed .81).

Read honestly: calibration gains are small; GR is under-dispersed (80% coverage ~.77); MC TD and yardage
markets are over-dispersed (coverage > .80). QB markets rest on only 70 test QB-games; this is research
execution, not certification.

## Known limitations / blockers
- GR has no opponent-defense adjustment (own-offense drives only) and no special-teams/defensive TDs beyond
  drive-level "Opp touchdown"/safety; roles that changed inside the 8-game window are under-weighted.
- No overtime in either sampler; full-game winner is regulation (tie reported).
- Historical sportsbook prop lines not wired into validation (proxy line used).
- Monday CAR@TB not run (Sunday slate only); Thursday/Friday wk12 games excluded (already played).
