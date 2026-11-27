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

---

# v2: coverage-window ("zone of responsibility") credit — coverage_sim.py (2026-11-27)

Rico's rule: whoever's window the ball was caught in gave up the play. A 30-yard catch near safety X counts against X. Everything here is **INFERRED**.

1. **Shell mix per defense**: StatRankings public Cover 0/1/2/2-man/3/4/6 rates (through 2026-11-20). When a team isn't on one of the public top-25 lists,
   that shell is set to 0.8 × the lowest listed value (IMPUTED; per-team list in `team_shell_mix.json`). Rates are normalised.
2. **Roles each game** come from that game's snap counts plus roster depth-chart position:
   - The top-2 CBs are the outside corners. Each one's side (offense's left/right) comes from his own verified and tackle-zone history.
   - CB3 (35%+ snaps) is the nickel.
   - Of the top-2 safeties, the deeper one is FS and the other is SS. The more-left safety takes the left half in two-high shells.
   - The top-2 LBs are MLB and LB2.
3. **Field grid** (offense's view): depth bands are behind the LOS, 0–9, 10–19 and 20+ (air yards = catch point). Width is L / L-slot / M / R-slot / R.
   pbp only says left/middle/right, so outside vs slot is sampled (WR 60% outside, TE 15%, RB 30%).
4. **Simulation**: each target gets 10,000 draws of (shell, width, strength side, middle split) from the team's mix. For each draw:
   - Zone shells: the owner of that window under that shell.
   - Man shells: the defender matched to that receiver's alignment (outside WR → that side's CB, slot WR → nickel, TE → SS, RB → MLB). The FS owns deep middle in Cover 1.
   - A defender's ownership probability is his share of the draws.
5. **Tackler blend** (completions):
   - YAC under 10 and the tackler is a role player: credit = 0.7 × window + 0.3 × tackler.
   - YAC 10+: the window owner keeps the credit, and a different tackler is logged as `help_defender`.
   - Rushing 10+ yards: the tackler is logged in `rush_explosives_10plus_tackler.csv` (pursuit evidence only; there's no window model for runs).

## v2 validation: held out verified PBU/INT, weeks 9–12 (same 364 plays as v1)
Tendencies were rebuilt without any week 9–12 verified play. StatRankings shell rates are season-to-date through Nov 20, so they include some of the test weeks
(mild scheme-rate leakage).

| Method | Exact defender top-1 | Top-2 | Window class (CB-left / CB-right / nickel / S / LB) | Position group (CB/S/LB) |
|---|---|---|---|---|
| v1 (same strict holdout) | 22.5% | 42.6% | 26.9% | 50.8% |
| v2 window simulator | 24.2% | 39.3% | **32.1%** | 50.5% |
| v2 × v1 hybrid | 24.7% | 41.2% | 30.5% | 50.8% |
| Majority-class baseline | — | — | 20.3% | 44.0% |

(The v1 number in the first half of this doc, 25.0% / 40.7%, used a looser leave-one-play-out holdout.)

v2 tiers (window probability): high ≥ 0.6 → 41% exact / 50% window (n=22); med 0.4–0.6 → 24% / 32% (n=284); low → 19% / 24% (n=58).
19% of verified defenders aren't in any of the 9 role slots (3rd LB, rotational backs, DL batted balls). Those plays can't be credited correctly.

**Reading**: the window class is right about 1 time in 3 (vs 1 in 5 by always guessing the most common class). The exact defender is right about 1 in 4, the
same as v1. It's a vicinity estimate, as Rico framed it, not an assignment. Credit on any single play is a coin flip among 2–3 nearby players. Season
totals (window yards, 20+ credit) average that noise out better than single plays do, but they're still unverified.

Also: PBU/INT plays are contested throws, so the test says nothing direct about clean catches. Cornerbacks travel and flip sides by formation, which free
data doesn't show. The man-to-alignment map is a template, not a game plan.

Outputs: `defender_window_credit_inferred.csv`, `defender_explosives_allowed_inferred.csv`, `rush_explosives_10plus_tackler.csv`,
`upcoming_w12_window_matchups_inferred.csv`, `team_shell_mix.json`, `attribution_v2_validation_*.csv`, `charts/*.png`, and the v2 section in every profile.
Rebuild: `python3 coverage_sim.py --raw <dir>` (needs `sr_cover_types_2026-11-22.csv` and `games.csv` in the raw dir) and `python3 validate_v2.py --raw <dir>`.
