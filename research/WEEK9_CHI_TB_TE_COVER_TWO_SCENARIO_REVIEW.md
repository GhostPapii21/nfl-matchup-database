# NFL Week 9 example: Chicago tight-end middle-field coverage vs Tampa Bay

**Date:** 2026-11-07 · **Game:** TB @ CHI, Nov 8 Sunday night · **Status:** SOURCE-VERIFIED MECHANISM ONLY. **NO PROBABILITY / PRICE / BET.**

## Strongest primary-source evidence

The [Buccaneers' official matchup article](https://www.buccaneers.com/news/buccaneers-bears-top-storylines-key-matchups-in-week-nine) identifies **Colston Loveland vs Buccaneers LB Alex Anzalone** as a key tactical matchup. In Tampa Bay's Cover Two, an inside linebacker has responsibility for carrying a TE up the middle seam. The club notes a previous Week 7 long seam TD by Darren Waller on a play **when Anzalone was not on the field**, which is a contextual caution, NOT proof that Anzalone would have allowed/prevented it. The club says other defenders will also cover Loveland; this is **NOT a confirmed every-snap shadow**.

The [club's second preview](https://www.buccaneers.com/news/5-bucs-to-watch-against-bears-week-nine-2026) explicitly mentions expected one-on-one coverage with Loveland and Anzalone's interceptions against Atlanta. Those interceptions do not independently measure his man/zone target-allowed success rate or how often he will carry the seam.

## Verified historical source values (not an upcoming forecast)

- Loveland: stable **GSIS `00-0040126`**, Chicago, **51 targets, 33 receptions** in 8 observed games. Official club preview separately reports 33 receptions and 309 receiving yards through Week 8. This matches Render's nflverse W1–8 raw outcome dataset. Do not infer 51 exact future targets over eight games if his route share or QB usage changes.
- Anzalone: Tampa Bay 2026 defender, stable GSIS resolved in the source audit. The source claims a *projected* coverage role but there is no sampled route-to-defender chart; probability of direct individual coverage remains unknown.
- Tampa Bay's allowed team-level public play flags through Weeks 1–8: **17 completed explosive-pass plays (20+) among 287 opponent pass-attempt flags**, descriptive rate **5.92%**; **16 sack flags** among 303 pass-attempt-plus-sack play proxies, **5.28%**. These do **NOT** separately measure blitz pressure, LB target-allowed, or Cover Two seam efficiency.
- Grok's `WEEK9_PLAYER_USAGE.csv` reports Loveland 93% of Week 8 snaps, 51 targets and ~20% target share, but does not provide a per-row primary source URL or exact denominator. Snap and target share remain **unverified numerical inputs** even when season target total is correct.
- Grok's `WEEK9_DEFENSIVE_MATCHUPS.csv` flags this as `verified`, but it contains **no numeric coverage denominator, target count, success rate, post-snap shell share or play IDs**. Our [`WEEK9_TE_DEFENSIVE_ASSIGNMENT_AUDIT_20261107.csv`](WEEK9_TE_DEFENSIVE_ASSIGNMENT_AUDIT_20261107.csv) downgrades the field to **published *expected* matchup, no confirmed full-game assignment**.

## Researcher's plausible mechanisms
1. **Cover Two with inside LB seam carry:** Loveland attacks the middle; if zone spacing opens behind the LB or QB progression holds the safety, a seam throw is possible. This mechanism requires actual seam route share, coverage snapshots and QB decision data to assign a probability.
2. **Anzalone/secondary executes underneath+deep coverage:** the seam may be closed and targets redirected to Burden, Odunze, RBs or shorter crossers. Do **not** automatically transfer his targets without measured redistribution.
3. **Tampa rush affects Caleb Williams:** an early sack/quick pressure can reduce pass attempts and route completion; lower QB passing output and lower TE opportunities may follow even when the TE coverage mismatch seems appealing. Current aggregate sacks are not enough to estimate this causal chain.
4. **Chicago substantially leads or trails by the fourth quarter:** the offensive pace/attempt and TE target allocation may change. Quantify only after a verified game-state/quarter scoring model.

## Skeptic's case
- A media key matchup is not a charted shadow and changes with personnel (11/12, Cover Two/quarters/man, LB substitution).
- A seven- or eight-game target sample and weekly TE snap rates are not automatically the next week's routes; player injuries, TE blocking duty and QB pressure can suppress raw targets.
- One visible seam TD without Anzalone on field does not establish what would happen with him present.
- The opponent's low aggregate 20+ pass flags may be driven by opponent quality or game script. No reliable defender-assignment coverage probability can yet be estimated.

## Adjudication
**Keep as an evidence-backed hypothesis and a scenario to simulate, NOT a positive-EV prop.** Missing:
- 2026 Loveland routes by seam/slot and first-read target share for same personnel;
- Tampa Cover Two usage and actual post-snap linebacker/seam responsibility across comparable games;
- Chicago QB pressure-to-sack-to-throw rates versus Tampa front and OL;
- confirmed inactive list and updated starters before kickoff;
- prospectively calibrated opportunity and yards distribution and exact sportsbook line/price.

This game case demonstrates the intended behavior of `skills/nfl-scenario-pro-bets`: a strong mechanism can coexist with insufficient opportunity or uncertainty to recommend a bet.
