# Materiality and semantics
materiality_metrics.json uses the packet parquet restricted to W1–8. League rows counted once; DAL/IND scopes include both teams in their games. Rates use all PBP rows as denominator, including administrative rows. Missing return-yard observations are counted separately. These are descriptive exposure counts, not causal estimates of score changes.
Penalty yards and nullified rows expose omitted enforcement/clock/down effects. TD flags on penalty rows do not identify accepted or nullified scoring without adjudication. Exact scoring impact if ignored is NOT_IDENTIFIED. Return yard sums measure field-position displacement exposure, not fantasy credits. OT game rates and TD rows measure exposure; they do not identify a regulation-only counterfactual score.
Existing supported narrow field-position path: fit_prospective_usage.py uses kick_distance minus observed return_yards as punt_net_yards, rejecting missing kick distance and negative net. joint_producer.py flips field position using this net. No player return-yard fantasy credits are created. This does not support return distributions, return TDs, kickoff enforcement or defensive returns.
Penalties, returns and official_overtime remain UNSUPPORTED, allows_sim_effect=false. Injected return/penalty outcomes must raise; existing suite exercises rejection. No new supported semantics were added.
OT single_possession_approx is research-only, NOT_VERIFIED_OFFICIAL_OT: first score can end the trial without matching possession. Official Rule 16 permits both teams an opportunity subject to the regular-season 10-minute limit. Source checked: https://operations.nfl.com/the-rules/nfl-rulebook and https://operations.nfl.com/rules-officiating/featured-rules . This research approximation cannot claim fitted official OT. Modeled no-return touchbacks also remain a residual field-position risk; current official kickoff touchback provisions differ. No readiness inferred.

| Scope | PBP rows | Penalty rows | Penalty yards | Punt return yards | Kickoff return yards | OT games |
|---|---:|---:|---:|---:|---:|---:|
| DAL | 1456 | 136 (9.34%) | 1144.0 | 233.0 | 1620.0 | 1/8 (12.50%) |
| IND | 1364 | 101 (7.40%) | 788.0 | 197.0 | 1958.0 | 1/8 (12.50%) |
| league | 21191 | 1765 (8.33%) | 14262.0 | 3775.0 | 25724.0 | 11/121 (9.09%) |
