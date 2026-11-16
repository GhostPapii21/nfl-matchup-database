# Coverage database and whether it moves the 80-yard projection (Nov 16, 2026)

Built after Week 10 to answer: who did each 80-yard receiver beat, does that defender get beat often, and should that
change a top candidate's number.

    python3 -m dashboard.coverage_db --season 2026                    # dashboard/results/coverage_db_2026.json
    python3 -m dashboard.coverage_db_render <db.json> <out.html> [extra_week.json] [value_results.json]
    python3 research/coverage_db_2026-11-16/test_value.py --data DIR  # DIR: advdef_<y>.parquet, snaps_<y>.parquet (2022-2026)

The database has two sources, kept apart: Pro Football Reference's charted coverage (yards charged to the nearest
defender, published a few days after each week) and the play-by-play record of which defender finished each catch
(available the next morning). Neither is an assignment.

## Test (WR and TE games 2022 to week 9 of 2026; fit 2022-24, held out 2025-26)

Each piece of a defense's record, using only earlier games, added to the base projection (targets, yards per game,
team implied total):

| Added | Odds of 80+ per one standard deviation | Standard error | Holds up? |
| --- | --- | --- | --- |
| 80+ games the defense has allowed to his position, per game | +11% | 5% | Yes, small |
| Share of cornerback games charged with 70+ yards | +2% | 4% | No |
| Cornerbacks' charted yards per target | 0% | 5% | No |
| Worst regular cornerback's charted yards per target | -4% | 5% | No |

Ranking accuracy on the held-out seasons is 0.8009 without any of them and 0.8012 with all four.

Top candidates only (base model 35%+, all seasons, 489 games; they hit 80+ 41.5% of the time):

| Split | Hit 80+ | Hit 100+ |
| --- | --- | --- |
| Defense rarely allows 80+ games to the position (lowest third) | 35.6% | 21.1% |
| Middle third | 47.3% | 30.1% |
| Highest third | 42.9% | 27.6% |
| Best "weak link" cornerback (lowest third of yards per target) | 42.1% | 25.0% |
| Worst "weak link" cornerback (highest third) | 41.7% | 30.1% |

On the 2025-26 holdout alone the "weak link" split looked large (66% against 34%, 41 games each); across all seasons it
is flat, so that was noise.

Read: how often a defense has allowed 80-yard games to a position is a small real signal, mostly as a headwind when the
defense rarely allows them. Individual defender records do not move the projection. Research only.
