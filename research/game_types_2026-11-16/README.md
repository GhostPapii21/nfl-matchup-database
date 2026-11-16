# Receiver tiers, game types and defense profiles (Nov 16, 2026)

    python3 research/game_types_2026-11-16/test_tiers.py                    # tier_results.json (2022 to week 9 of 2026)
    python3 research/game_types_2026-11-16/slate.py --data DIR --week 11    # slate_week11.json

Tiers, from what a receiver had done before each game: **alpha** = 8+ targets and 70+ yards a game; **tier B** = 7+
targets and 55+ yards a game.

| Tier | Player-games | A week | Hit 80+ | Hit 100+ |
| --- | --- | --- | --- | --- |
| Alpha | 643 | about 10 | 40.9% | 26.1% |
| Tier B | 817 | about 12 | 29.7% | 17.1% |
| Everyone else | 8,541 | about 129 | 7.4% | 3.1% |

Alphas, by thirds of each factor (80+ rate, lowest / middle / highest third):

| Factor | Lowest | Middle | Highest |
| --- | --- | --- | --- |
| Team implied total (19.7 / 23.9 / 27.5) | 31.5% | 41.7% | 50.0% |
| Game total (41.3 / 45.8 / 50.6) | 32.9% | 45.9% | 44.3% |
| Own team's pass volume | 37.7% | 40.8% | 44.4% |
| Defense's rate of 20+ yard completions allowed | 40.5% | 46.3% | 36.0% |
| Yards the defense allowed to opposing lead receivers | 44.8% | 35.7% | 40.3% |

The tiers and the game type separate outcomes. A defense's big-play rate and what it allowed to other lead receivers
do not, for alphas or tier B, early or late in the season. `slate.py` therefore sets an alpha's 80+ estimate from his
team's implied total (31.5 / 41.7 / 50%), tier B likewise (26 / 31 / 32.5%), and takes 7 points off against a defense
in the lowest third for 80+ games allowed to the position (research/coverage_db_2026-11-16). Defense big-play rate,
missed tackles and broken tackles are shown as context, not used. The running-back tackle numbers are untested.
