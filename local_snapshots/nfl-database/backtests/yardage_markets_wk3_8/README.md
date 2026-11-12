# Yardage W3–8 offline backtest

Run from repository root with Python 3, pandas, numpy, pyarrow and lxml:

```
python3 backtests/yardage_markets_wk3_8/build.py
python3 backtests/yardage_markets_wk3_8/validate.py
```

The first command reproduces the pre-lock artifacts and training-only rule search. Do not rerun it to retune based on holdout. The grading command added after the lock is `python3 backtests/yardage_markets_wk3_8/grade.py`.

All writes stay here. Inputs are read-only saved local files. No fetching code, API clients, environment access or network requests. Source inventory records accepted/rejected timestamp availability; candidate source/snapshot preserve quote provenance. Quotes without verifiable pre-kickoff timestamps are excluded. No synthesized rush+receiving odds.

Read GAPS.md before interpreting results. Missing weeks/markets cannot be inferred from covered weeks. STEP 3 baseline holdout aggregates are produced as requested, but rule selection reads only the training dataframe. Selected-rule holdout evaluation occurs only after the first commit.

Observed raw inventory has usable prices only in weeks 6–8 and only rush and receiving yardage. Thus the requested W3–6 training partition is effectively week 6 alone; rush+receiving and weeks 3–5 have no admissible quotes. This is a partial-coverage experiment, not a complete six-week backtest.
