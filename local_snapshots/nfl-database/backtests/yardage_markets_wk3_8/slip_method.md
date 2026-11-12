# Frozen yardage slip method

Passing rules are in rules.py and locked_rules.json. For singles and slips choose one priced leg per player per week by directional form edge descending, then American price descending (higher return), then stable candidate ID ascending. No simulated edge is used. This favors high prices and needs holdout scrutiny.

For each week, greedily take up to four legs in that order, maximum two per game. A remaining group of three makes one 3-leg slip; groups below three abstain. Remove used players and repeat: number of slips is therefore determined by eligible count and game cap, with no arbitrary weekly target. Stake $10 per slip, also $10 per selected single. No player is reused across slips that week. All legs are rush, receiving or rush+receiving yardage.

Sharp OFF uses no Sharp fields. Sharp ON applies the same frozen rules plus this explicitly HINDSIGHT sensitivity filter: overs require opponent Sharp Oct27 man >=30%; unders require <30%; missing Sharp abstains. This filter is specified without evaluating holdout results. It is not deployable point-in-time evidence.

Illustrative parlay payout multiplies American-to-decimal odds. Push legs reduce to decimal 1; all pushes refund; any loss loses the stake; any ungraded leg leaves the slip ungraded. Correlation, bookmaker SGP repricing, limits and void/participation rules are unavailable. Singles/slips are not additive independent portfolios.
