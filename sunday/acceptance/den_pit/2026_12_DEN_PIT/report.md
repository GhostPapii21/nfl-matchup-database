# 2026_12_DEN_PIT research packet

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Status: COMPLETE
- Run: `20261128T020928Z_83a8f574`
- Command: `python -m sunday replay --game 2026_12_DEN_PIT --trials 200 --out sunday/acceptance/den_pit`
- Code: 3586e4d03d3e4f1a5e47927140471fa7a7f2554b dirty=False
- As of: 2026-11-27T04:31:50+00:00
- Kickoff: 2026-11-27T20:00:00+00:00
- DEN at PIT, season 2026 week 12

## Fan-out

| Component | Status | Ran | Seconds |
| --- | --- | --- | --- |
| engine_roster | OK | True | 0.0 |
| packet_research | OK | True | 0.003 |
| market_lines | OK | True | 0.003 |
| phase_ledger | OK | True | 0.026 |
| matchup_fields | OK | True | 0.239 |
| period | OK | True | 0.724 |
| sim100k_preflight | REFUSED | True | 0.807 |
| possession | OK | True | 6.99 |

## Game scripts

Favorite is the side laid the points (home spread < 0 means home is favored). underdog_chases: favorite led by 8+ at half and the final favorite margin is 3 or less. favorite_controls: favorite led by 7+ at half and won by 7+. competitive: final favorite margin within 7 and halftime margin within 10, and not already classed. other_unclassified: the rest. Regulation scores. Buckets do not overlap.

Favorite DEN, underdog PIT, n=200.

| Script | Trials | Share | Home reg mean | Away reg mean |
| --- | --- | --- | --- | --- |
| underdog_chases | 7 | 0.035 | 24.4286 | 26.0 |
| favorite_controls | 45 | 0.225 | 14.2222 | 29.2222 |
| competitive | 72 | 0.36 | 19.1667 | 18.5278 |
| other_unclassified | 76 | 0.38 | 25.4605 | 16.0789 |

Play, pass/run, and player-opportunity distributions: NOT_SUPPORTED on these buckets.

## Models

- Documented sim_v6 (`tools/sim_v6.py`): ran=False. PHASE_SCRIPT.md and the source run gate require tools/sim_v6.py for the three-method triad. That file is not in this revision, so the triad did not run.
- Lightning: ran=False.
- Main: no separate entrypoint. Possession is not relabeled Main.
- simv56 scratch: ran=False (not used as sim_v6).
- Possession `den_pit_2026-11-27_data_only_nfl43` n=200 seed=1969908846 status=OK. Regulation mean home 20.63, away 20.265.
- Period `matchup_pair` n=200 seed=20463131 ran=True reg home mean 21.205 away mean 20.65.
- Period `independent` n=200 seed=20463132 ran=True reg home mean 20.86 away mean 22.83.
- Period `game_randomness` n=200 seed=20463133 ran=True reg home mean 21.175 away mean 21.12.
- Period bias: UNIMPLEMENTED_NO_FITTED_CALIB ran=False.

## Disagreement

Home-cover span across methods: 0.105 (material=True). Methods are listed, not blended.
- possession_engine_v0 simulate_games p_home_cover=0.65 n=200 seed=1969908846
- period_engine_v0 matchup_pair p_home_cover=0.695 n=200 seed=20463131
- period_engine_v0 independent p_home_cover=0.59 n=200 seed=20463132
- period_engine_v0 game_randomness p_home_cover=0.67 n=200 seed=20463133

## Red team

- [no_play] The required three-method sim_v6 triad did not run.
- [gap] Lightning was not executed.
- [no_play] Probabilities are not a fitted calibration.
- [gap] The gated 100k entry point refused this game.
- [gap] One or more packet sources are not fresh at this as-of.
- [gap] Defender assignment or route fields have no accepted source.
- [gap] Coverage shells were not produced by a shell model.
- [fragility] The packet's stored team projection includes a prior season. This command's period run does not use that object.
- [fragility] Executed methods disagree by 8 points or more on the home cover probability.
- [fragility] The schedule consensus total and the timestamped Pinnacle total are different numbers.
- [fragility] The possession engine published its own limitations on this run.
- [gap] Script buckets have scores only. They do not carry play, pass/run, or player-opportunity distributions.
- [no_play] projection_ready is false. This packet is research, not a pick.

## Board

Strong reads and soft leans stay empty while projection_ready is false. Method probabilities stay on the model layer and are not promoted.

Strong reads: 0. Soft leans: 0. Avoids: 10. No plays: 5.
- No play: spread PIT cover — research-only; projection_ready is false
- No play: spread DEN cover — research-only; projection_ready is false
- No play: total over — research-only; projection_ready is false
- No play: total under — research-only; projection_ready is false
- No play: player_props all listed props — tools/sim_v6.py did not run, so no player threshold probability was executed

## Reproducible

Manifest sha256 `68fa1cda6b606ce41639ae024782322607ee60f3fd7cb1f0d1109236957a7794`.
