# INFERRED coverage attribution — method, validation, and what each source actually gave (2026-11-27)

Everything in `defender_attribution_inferred.csv`, `defender_inferred_coverage_totals.csv`, `upcoming_receiver_vs_likely_defender.csv`
and the "INFERRED coverage attribution" section of each profile is **INFERRED**. It is not a verified defender. The rule that a receiving leg needs a
verified main defender (named on a PBU, INT or DPI) is unchanged. `projection_ready` stays false.

## Method (attribution.py)
For each 2026 targeted pass with a pbp direction (weeks 1–12, 10,494 targets; 10,493 attributed), candidates are the defense's CB/S/DB/LB with defensive
snaps in that game (about 12.5 per team-game). Score = snap % × P(position group | receiver position, zone) × the defender's own side/depth lean
(his verified PBU/INT/DPI and tackle-after-catch zones vs his group's) × same-game links to that receiver (boosted for man-heavy teams, StatRankings man %)
× a safety factor on deep throws from StatRankings two-high/single-high %. Scores are normalised per play.
Zones are pbp `pass_length` (short/deep) × `pass_location` (left/middle/right, offense's view). Corners' sides come out of their own play history
(LCB/RCB in effect); there is no labelled LCB/RCB/nickel field in any free source.

Tiers (set on weeks 1–8): high = top probability ≥ 0.50; med = ≥ 0.35 or ≥ 2.5× the second choice; low = the rest.
Params were picked on weeks 1–8 from a 20-config grid; weeks 9–12 were not used for any choice.

## Validation: hold out each verified PBU/INT play
The play's own link is removed from the defender's tendencies and receiver links (leave-one-play-out). The position prior is refit without that week.
DPI plays are excluded because they're "no play" rows with no target record. Top-1 = the inferred defender is the one named.

| Split | Tier | Plays | Top-1 | Top-2 |
|---|---|---|---|---|
| Test wk 9–12 | high | 45 | 35.6% | 48.9% |
| Test wk 9–12 | med | 102 | 31.4% | 48.0% |
| Test wk 9–12 | low | 217 | 19.8% | 35.5% |
| Test wk 9–12 | all | 364 | 25.0% | 40.7% |
| Train wk 1–8 | all | 916 | 28.9% | 47.6% |
| Baseline snap % × position only, test | all | 364 | 23.4% | 40.7% |
| Random pick among candidates | all | — | about 8% | — |

Reading: the free-data method beats a random pick about 3× but adds only about 1.5 points over "most-snapped player of the right position". Even
"high" is right only about 1 time in 3 out of sample. PBU/INT plays are tight-coverage plays, so accuracy on ordinary catches is unknown and probably not better.
**This layer cannot stand in for a verified defender.** At most it's a context flag.

Known biases: tackle-after-catch links (inferred) drive much of the same-game receiver affinity, so a defender who tackles a receiver a lot after
the catch gets credited with covering him (e.g. Cobie Durant on DeVonta Smith, W12). Upcoming-game shares are close to flat (top defender usually 20–28%),
so they don't identify a shadow corner.

## What each requested source actually provides
- **Play-by-play (nflverse)**: direction, depth, air yards, receiver, PBU/INT/DPI names, tacklers. Used. No alignment, no coverage assignment.
- **NGS**: the nflverse `ngs_receiving` file is season/week aggregates per receiver (cushion, separation, intended air yards, YAC). It has
  **no per-play routes, no player tracking, no catch x/y and no defender positions.** The public nextgenstats.nfl.com route charts are images of one
  receiver's routes per game (catch/incompletion/TD/INT marks). They draw **no defenders**, the page is a JS app, and the repo policy
  (`.github/workflows/ngs-charts.yml`) keeps those images out of the repo. The NGS data API host failed TLS from this box. We do **not** have tracking data,
  so "route + defender alignment + catch location → nearest CB/S" can't be computed from free data.
- **PFF (free only)**: `pff.com/tools/matchups` publishes projected WR/TE vs CB/S matchups before games (W11 saved in
  `nfl-database/pff_matchups/2026_w11`). These are projections, not post-game charting. Free game recap "Key Takeaways" pages (W1–8 saved in repo
  `data/pff_captures_w1_8`) carry no coverage or alignment. The man/zone report and per-defender coverage grades are paywalled and weren't used.
  `pff.com/nfl/games` returned 404 from the box.
- **Game highlights**: not automatable here (video; no free per-play text naming the coverage defender). Use the manual protocol below.
- **"GEMP chart"**: not found anywhere in our files, the repo or the skills (the only matches were random base64 strings). Best guesses are the NGS route chart,
  Sharp's coverage-scheme tables, or the PFF matchup chart. **Unclear, so we're asking Rico** what he means.

## Manual spot-check protocol (key games, free sources only)
1. Pick the receiving legs under consideration and pull their targets from `defender_attribution_inferred.csv` (the game, quarter, clock, zone and inferred defender).
2. Open the official NFL/team highlight video on YouTube or NFL.com (free, no login) for that game. For each target shown, note the defender closest at
   the catch point and his jersey number. Map the number with `nflverse roster_weekly` for that week.
3. Log it in `manual_spotcheck.csv` (game_id, play_id, observer, video URL + timestamp, defender seen, confidence) as **OBSERVED-VIDEO**: a third label,
   neither verified (pbp) nor inferred (model).
4. Don't use All-22 / NFL+ / PFF premium, and don't bypass a login or paywall. If no free clip shows the play, record "not visible".
5. After about 50 plays, compare OBSERVED-VIDEO with the inferred pick to measure accuracy on ordinary catches.
