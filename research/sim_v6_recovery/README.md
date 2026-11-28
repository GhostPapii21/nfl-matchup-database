# sim_v6 recovery and the sim_v6r1 replacement triad (Nov 28, 2026)

Research only. `projection_ready` stays false. No betting rule, lock, projection or grade was changed.

## 1. The original sim_v6 is recovered and verified

- **`tools/sim_v6_ab2144f0.py`** is git blob `ab2144f03f6ca3b57950a1f2528e305193e723cd`, byte for byte. A test checks the
  blob hash.
- **It is the engine that made the committed 1,096-row `calibration/simv56/engines/sim_v6_backtest.csv`.** Run with the
  opponent factor at 0.5 (`CC_OPP=0.5`, the setting before the NOSHRINK rule), it reproduces all 282 week-4 rows to
  1e-13 on `pred_mc`, `pred_bias` and `pred_gr`. The test checks 12 of them. The blob's own default factor is 1.0.
- **Its missing pieces are now committed:**
  - `tools/sim_v6_calib.json` and `tools/sim_v6_backtest.csv` come from the original `python3 sim_v6.py fit`
    (weeks 4-7, 4,000 trials, blob defaults).
  - `tools/rb_script_boost.json` and `tools/rb_miss_fit.json` are copied from the sha-pinned files in
    `calibration/simv56/engines`.
  - `tools/simsrc.py` builds the `$SIMV6_SRC` input directory, which was never committed. It uses symlinks to
    committed nflverse files.
- **The entry point works:** `python3 tools/sim_v6.py run <legs.json> <out.json>` now runs the unmodified original.
  With no argument, `tools/sim_v6.py` still prints the PR #163 refusal receipt.
- **Still blocked:**
  - `report` / `legs_today()` needs `legs_final.json`, which was never committed.
  - `source_adapters/tools/run_gate.py` needs `rules/rulebook.py`, which is missing.

**Why the original alone cannot be the triad.** Its `bias` method is the `mc` draw with another seed. The multipliers are
fitted on `pred_mc` with `K_BIAS == SHRINK_K == 30`, so the calibration file gives `bias` exactly the `mc` multipliers. Its
`mc` ignores the spread, so only `gr` reacts to game script. On the held-out weeks, `mc` and `bias` correlate 0.99987,
with a 1.06% median difference.

## 2. sim_v6r1: an explicitly versioned replacement (`tools/sim_v6r1.py`), not sim_v6

`VERSION = "sim_v6r1"` and `IS_ORIGINAL_SIM_V6 = False`. Every artifact carries `not_sim_v6: true`. It reuses sim_v6's data
preparation and opponent factors.

| Method | Volume | Outcomes | Script |
|---|---|---|---|
| `mc_nb` | sim_v6 negative binomial | binomial catches, resampled catch yards | volume mean x E[exp(b(M-mu)) given scenario] |
| `gr_share` | sim_v6 beta share x lognormal pace | same as sim_v6 gr | margin drawn from N(mu, 13.5) truncated to the scenario |
| `eb_boot` (new) | bootstrap of the player's prior games' per-play rates x league team-games in the scenario | joint per-target and per-carry bootstrap | empirical volume index of league games in that margin bin |

- **Scenarios** use the favorite-margin edges from PR #159:
  - `favorite_controls`: 10 or more.
  - `underdog_chases`: 3 to 10.
  - `competitive`: -3 to 3.
  - `residual`: below -3, the upset bin.
- **The residual bin is run too,** so the four bins add up to the whole game.

## 3. Leakage-safe validation (`tools/sim_v6_validate.py`, `validation.json`, `rows.csv`)

**Data**
- 2,156 player-markets from 2026 weeks 4-11. That is weeks 4-7 (the 1,096-row universe) plus weeks 8-11.
- Each week uses only play-by-play before that week's first game. Both engines run on the same rows at 4,000 trials.

**Calibration**
- Multipliers for week W are fitted only on weeks before W, using sim_v6's rule.
- Scored on weeks 5-11 (1,872-1,874 rows per method).
- The spread is nflverse `spread_line`. That is a closing line, which adds mild optimism.
- The line L is a proxy: floor of the player's 0.6 season / 0.4 last-3 mean, plus 0.5. Real book lines were not used.

**The acceptance rule** was written into the file before scoring. The distinctness test was then made pairwise, which is
stricter, and that only changed sim_v6's mc/bias verdicts.

Pooled over weeks 5-11 (pred is the calibrated median):

| Method | Median signed err % | MAE | 80% coverage | Brier at L | Player hit-rate Brier | Verdict |
|---|---|---|---|---|---|---|
| sim_v6 mc | +4.1 | 22.85 | 0.762 | 0.2438 | 0.2542 | rejected: not distinct from bias |
| sim_v6 bias | +4.0 | 22.79 | 0.762 | 0.2435 | 0.2542 | rejected: not distinct from mc |
| sim_v6 gr | +3.5 | 22.76 | 0.800 | 0.2410 | 0.2542 | accepted |
| **sim_v6r1 mc_nb** | +4.0 | 22.84 | 0.755 | 0.2438 | 0.2542 | **accepted** |
| **sim_v6r1 gr_share** | +3.3 | 22.75 | 0.809 | 0.2415 | 0.2542 | **accepted** |
| **sim_v6r1 eb_boot** | +2.6 | 22.72 | 0.787 | 0.2410 | 0.2542 | **accepted** |

**sim_v6r1 pairwise differences:**

| Pair | Correlation | Median difference |
|---|---|---|
| mc_nb vs gr_share | 0.9990 | 2.3% |
| mc_nb vs eb_boot | 0.9961 | 4.7% |
| gr_share vs eb_boot | 0.9957 | 4.9% |

**Weak spots:**
- **Passing yards:** every method's Brier is slightly worse than the QB's own hit rate. For example, eb_boot scores
  0.2632 against 0.2603.
- **Rushing yards:** 80% intervals cover only 66-69%, so rushing outcomes are too narrow.
- **All markets:** medians run 2-7% high after calibration.
- **Committed 1,096 rows, scored forward on weeks 5-7:** receiving yards were +8.8 to +10.7% high and rushing yards
  +7 to +8% high.

## 4. Sunday Nov 29 slate: 100,000 trials per method per scenario

```
python3 -m sunday sim --date 2026-11-29 --as-of 2026-11-29T12:00:00+00:00 --trials 100000 --concurrency 4 \
  --out research/sim_v6_recovery/sunday_2026-11-29
```

**Coverage**
- 10 games, 198 player-markets, all PASS, 0 errors.
- sim_v6r1 ran 237,600,000 trials: 198 legs x 3 methods x 4 scenarios x 100,000.
- The restored sim_v6 ran 59,400,000 (198 x 3 x 100,000, with no scenario split).

**Benchmark**

| Measure | Result |
|---|---|
| Slate wall time | 115.6 s (4 processes, 4 CPUs) |
| Time per game | 28.7-46.9 s |
| Peak memory per game | 665-688 MB |
| Re-run | identical results (sha256 of results matched on ATL@MIN) |

Per game: `sunday_2026-11-29/<game>/{sim_v6r1.json, sim_v6.json, benchmark.json, errors.json}`. Slate:
`sunday_2026-11-29/{benchmark.json, INDEX.md}`.

**Inputs and limits**
- Play-by-play is the committed nflverse file for weeks 1-11. Thursday/Friday week-12 games are not in it.
- Spreads come from each packet's `market.home_spread`.
- **Inactives are UNVERIFIED.** A player is kept if he appeared in his team's last game. No week-12 injury file is
  committed (`inj26.parquet` stops at week 5).
