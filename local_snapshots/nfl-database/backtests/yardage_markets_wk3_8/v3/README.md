# v3 Stage A — test only

Offline artifacts built with `python3 build.py`. Audit with `python3 validate.py`. All writes stay in this directory. No network, environment-key access, or git commits are used.

`features.csv` preserves the v2 main consensus universe and rebuilds prior-week features. Only weeks 3–6 have settlement columns; weeks 7–8 remain withheld. `baseline_train.csv` contains the unfiltered rush-unders baselines by train week. Both baseline variants coincide because this universe already has one rush-under per player-week. `traits.md` is exploratory train-only analysis. `RULES.md` describes the train-fitted rules and their statistics. `GAPS.md` records missing data, saved odds coverage by week, and leakage limitations. `weather_inventory.txt` and `saved_game_odds_inventory.csv` document local input discovery.

`rules.py`, `locked_rules.json`, `slip_method.md`, and `grade.py` are frozen along with the feature/training artifacts in `frozen_sha256.json`. The manifest excludes itself and this README. Stage A parses `grade.py` but does not execute or import it. Stage B is a separate explicit action: run `python3 grade.py` unchanged. It verifies hashes before grading and writes results and baseline comparisons without refitting.
