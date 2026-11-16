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

## Running backs: do a defense's tackling numbers predict rushing yards? (`test_rb.py`)

1,855 lead-back games (10+ carries a game coming in), 2022 to week 10 of 2026; fit 2022-24, held out 2025-26.
Lead backs hit 80+ rushing yards in 28% of games and 100+ in 16%; backs with 15+ carries a game, 38% and 23%.

| Added to carries, yards per carry, spread and team total | Odds of 80+ per standard deviation | z |
| --- | --- | --- |
| Missed tackles a game (PFR) | -8% | -1.2 |
| Tackles broken by backs a game (PFR) | +2% | 0.3 |
| Yards after contact per carry allowed | +16% | 2.2 |
| Yards before contact per carry allowed | +24% | 3.0 |
| Yards per carry allowed to backs | +35% | 4.4 |
| Runs of 10+ allowed a game | +35% | 4.4 |
| RB rushing yards allowed a game | +37% | 4.7 |

Missed and broken tackle counts carry no signal. What a run defense has actually allowed does: by thirds of RB rushing
yards allowed, lead backs hit 80+ in 24% / 27% / 34% of games (58 / 62 / 68 yards). On the held-out seasons the tough
third is still lowest (26%) but the middle and soft thirds are not separated (33% / 31%).

Backs with 15+ carries: favored by 3+ against a soft run defense, 49% hit 80+ and 31% hit 100+ (173 games; 40% and 22% on
the 50 held-out games); underdog by 3+ against a tough one, 31% and 15% (24% held out).

Model used for `rb_week11.json` (all seasons): logit P(80+) = -15.60 + 2.39 ln(carries) + 2.39 ln(yards per carry)
+ 0.018 spread - 0.020 implied + 1.14 ln(RB yards the defense allows a game), with carries = 0.6 season + 0.4 last three
and yards per carry shrunk toward the league with 40 carries. Fit on 2022-24 it was calibrated on 2025-26 by fifths:
predicted 12 / 20 / 27 / 34 / 48%, happened 18 / 20 / 27 / 37 / 47%. Research only; not graded against prices.
