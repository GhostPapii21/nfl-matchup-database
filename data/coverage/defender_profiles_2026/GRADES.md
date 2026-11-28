# Defender quality grades — thresholds and sources (2026-11-27)

`grades.py` → `defender_grades.csv` (every CB/S with **20+ PFR-charted targets**: 171 players, 110 CB and 61 S, through week 11) and
`team_defense_summary.csv`. The grades are also in every `profiles/{TEAM}.md`. Rebuild with `--through-week N` (leak-free; the PBU counts use the same weeks).

## Columns and sources
- tgt / cmp / yds / TD / INT: PFR charting (nearest defender), weekly via nflverse `advstats_week_def_2026`.
- target share: his targets ÷ all CB+S targets for his team in the games he played (how much he gets picked on).
- catch %, yards per target, yards per catch, yards per game; rating allowed = NFL formula on his summed totals (computed).
- yards per snap: yards ÷ **all** defensive snaps (nflverse snap counts). Coverage snaps aren't public.
- PBU: pbp-verified; plays-on-ball rate = (PBU + INT) ÷ targets.
- `tackled_on_20plus_INFERRED`, `window_credit_20plus_INFERRED`: supporting model columns only.
- Nickel/slot: free data has no per-defender slot label, so there's no separate slot grade (CB vs S only).

## Percentiles and labels
Percentiles are within position (CB vs S), among graded players; 100 = best coverage. A player can carry several labels.

| Label | Rule |
|---|---|
| LOCKDOWN | rating-allowed percentile ≥ 80 **and** yards-per-target percentile ≥ 70 |
| LIMITS CATCHES | catch-% percentile ≥ 70 (bottom 30% catch rate allowed) |
| LIMITS YARDS | yards-per-target percentile ≥ 70 |
| GIVES UP EXPLOSIVES | yards-per-catch percentile ≤ 25 (top 25% yards per catch allowed; charted proxy for big plays) |
| TARGET MAGNET | target-share percentile ≥ 75 **and** yards-per-game percentile ≤ 25 (picked on and it works) |
| WEAK LINK | rating-allowed percentile ≤ 25 **and** yards-per-target percentile ≤ 30 |

Composite = mean of the catch %, YPT, rating and yards-per-game percentiles. The team's weakest link and best defender are the lowest and highest composite.
**Small sample**: 80 of 171 have fewer than 35 targets (flagged in `sample_note`).

## Sanity backtest (weeks 4–11; no saved receiving lines used)
WR/TE games where the receiver averaged 30+ yards in 3+ prior games. Benchmark = **the player's own prior average** (not a sportsbook line).
Grades were rebuilt through week w−1 for each week w.

| Opponent secondary | n | Beat own avg | Mean vs own avg | Median |
|---|---|---|---|---|
| LOCKDOWN, no weak link | 67 | 31.3% | −8.3 yds | −14.0 |
| WEAK LINK / TARGET MAGNET, no lockdown | 230 | 40.4% | −2.4 | −7.1 |
| Both | 100 | 34.0% | −6.6 | −14.5 |
| Neither | 195 | 41.5% | −3.1 | −8.4 |

Reading: a LOCKDOWN corner or safety on the roster lines up with about 9 points fewer receivers beating their average and about 6 fewer yards per receiver. A
WEAK LINK / MAGNET defense did **not** beat the "neither" group. The lockdown-vs-weak gap isn't statistically significant (z ≈ 1.4, small n). It's team-level
(any graded defender), not the actual matchup. Over-rates are under 50% everywhere because a player's own mean sits above his median.
