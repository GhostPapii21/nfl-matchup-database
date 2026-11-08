NFL GAME SCRIPT — CURRENT CONSOLIDATED WORKFLOW
Version date: October 29, 2026

STATUS
This document defines the complete required workflow.
It does not certify that every feature is implemented or every source is available.

Contract: workflow-v1 — 60 required checks.
Accepted revision: 20261028T132748605447.
Model: opportunity-v2-experimental.
Independent probability calibration: NOT PASSED.

Database repository:
https://github.com/GhostPapii21/nfl-matchup-database

Latest verified database publication:
107 games, with game data through October 26, 2026.


PURPOSE

For every requested NFL matchup, follow the same workflow to evaluate:

• Offensive opportunities and player workloads.
• Defensive strengths, weaknesses and coverage tendencies.
• Injuries, personnel, weather and game environment.
• Passing volume and changing game scripts.
• Player outcome distributions.
• Standard props, alternate lines and supported game totals.
• Prediction errors and evidence-based improvements.

Cover quarterbacks, running backs, wide receivers and tight ends,
including secondary players with meaningful participation.

Keep measured facts, inferred explanations, conditional scenarios
and model projections separate.

Never invent missing inputs, source reads, simulations or probabilities.


0. STARTUP, IDENTITY AND SOURCE VALIDATION

Before analysis:

1. Verify the exact season, game date, kickoff, venue, teams and game ID.
2. Do not mix different meetings, seasons or player-ID namespaces.
3. Read manifest.json, schema.sql and DATA_GAPS.md.
4. Verify the database archive checksum and table counts.
5. Confirm that the receiving tool can actually query SQLite.
   A GitHub connection alone does not establish database access.
6. In the original project, read:
   outputs/NFL_MATCHUP_DATABASE_MASTER_SPEC.md
   outputs/workflow_control/contract.json
   outputs/workflow_control/README.md
7. Run outputs/nfl.py verify before generating a forecast.

The game command uses existing evidence.
It does not automatically refresh every external source.

HISTORICAL AND PROSPECTIVE RULES

• Historical development requires an explicit as-of timestamp.
• Never obtain a completed game's result to form its forecast.
• A forecast created after the game remains retrospective,
  even when its input cutoff is set before kickoff.
• Prospective evaluation requires the exact intended game ID
  and a locked forecast created before kickoff.
• Supplied lineups remain conditional scenarios until verified
  against the exact game and timestamped source evidence.

SOURCE AND DATA RULES

• Protect original SQLite, raw evidence and append-only MASTER files.
• Use a source backup and audited ingestion.
• Never repair source facts by guessing.
• Missing, malformed and nonfinite required values are gaps, not zero.
• Legal lateral receiving yards can exist without a reception.
• Distinguish publication time, data-through date and retrieval time.
• Retrieving an old page does not make its information fresh.
• Unknown publication timestamps mean freshness UNKNOWN.

Each observation should retain:

source_id
exact source_url
retrieved_at
source_updated_at
data_through
season and season_type
week or declared window
entity_type
stable team/player ID
canonical metric
value and unit
numerator and denominator
sample_size
statistical scope
freshness_status
access_status
raw_snapshot_hash
missing-data reason

Prefer official NFL gamebooks/play-by-play, official NGS and
official team/NFL injury reports for their respective fields.

Use ESPN boxes/PBP as documented alternatives.
Use licensed charting only when actually available.
Fallback sources must provide equivalent metrics and windows.
Label non-equivalent proxies.

Do not bypass paid access or verification restrictions.

REPORTING STATUSES

Every report must include all 60 required checks, each with:

PASS
PARTIAL
UNAVAILABLE
UNIMPLEMENTED
STALE
BLOCKED
NOT_APPLICABLE

Every status needs a reason and supporting evidence when available.

Under the current contract, NOT_APPLICABLE is permitted only for:
P4.slip_comparison
P6.live_policy

Never silently convert missing evidence into PASS.


PHASE 1 — COLLECT AND RECONCILE GAME DATA

For every game in the declared sample, collect the complete box score
and play-by-play. Do not select only favorable examples.

PLAY-BY-PLAY

Record:
• Period and game clock.
• Down and distance.
• Field position and possession.
• Score state.
• Play type and result.
• Penalties and nullified plays.
• Player participation and credited gains where available.

QUARTERBACKS

Record:
• Completions and attempts.
• Gross passing yards.
• Passing touchdowns and interceptions.
• Sacks and sack yards.
• Designed runs, scrambles and kneels separately.
• Down/distance and supported pressure context.

Distinguish QB gross passing yards from team net passing yards.

SKILL PLAYERS

Record:
• Targets.
• Receptions.
• Receiving yards.
• Air yards where available.
• Carries and rushing yards.
• Touchdowns.
• Red-zone targets.
• Goal-line carries.
• Final-two-minute targets in one-score fourth quarters.

DEFENSE AND OFFENSIVE LINE

Record:
• Tackles and assists.
• Sacks, hits and pressures.
• Supported pressure attribution.
• Clean versus coverage sacks only when evidenced.
• OL starting five.
• Snap counts, substitutions and injuries.
• Left-tackle and right-tackle status.

CREDIT RECONCILIATION

Reconcile numeric play gains, descriptions and player credits against
authoritative records.

Penalty movement is not automatically a player's credited gain.
Preserve unresolved differences instead of forcing agreement.

REGULATION VERSUS OVERTIME

Separate regulation and overtime for:
• Team scoring.
• Player statistics.
• Model outputs.
• Postgame assessment.

Never compare a regulation-only forecast with full-game actuals
as though their scopes match.

Missing player-level overtime splits remain explicit gaps.


PHASE 2 — BUILD BOTH DEFENSIVE PROFILES

For each team, identify the opponent, date and statistical window.

TEAM DEFENSE

Measure:
• Points allowed.
• Passing yards allowed, with gross/net definition.
• Rushing yards allowed.
• Sacks, QB hits and pressures.
• Blitz rate.
• Last-three-game pressure trend.

POSITIONAL RECEIVING ALLOWANCES

Measure separately for WRs, TEs and RBs:
• Targets allowed.
• Receptions allowed.
• Receiving yards allowed.
• Per-game averages.
• Totals, denominators and sample sizes.

Do not substitute receiving yards for receptions or vice versa.

COVERAGE AND ALIGNMENT

Where verified, record:
• Outside versus slot efficiency.
• Man versus zone.
• Middle-open versus middle-closed.
• Press versus off coverage.
• YAC allowed per completion.

EXPLOSIVE PLAYS

Receiving explosive:
At least 20 credited total receiving yards.

Rushing explosive:
At least 15 credited rushing yards.

Keep separate:
• Air-yard depth.
• Total credited gain.
• Explosive-play count.
• Total yards gained on explosive plays.

RUN DEFENSE

Measure:
• RB-only rushing volume and efficiency.
• Rushing success.
• Negative carries.
• Carries gaining zero or fewer yards.
• Run direction and verified gap/concept.
• Box count, front and personnel.
• Down, half and score-state splits.

Carries of zero or fewer yards are a stuff proxy unless the source
provides a specific stuff definition.

Carry direction alone does not identify inside zone, power or counter.

INDIVIDUAL DEFENDERS

Where supported, record:
• Coverage snaps.
• Targets faced.
• Receptions and yards allowed.
• Explosives allowed.
• Breakups and interceptions.
• Tackles, sacks and fumble events.

A tackler is not automatically the responsible coverage defender.

WEAKNESS IDENTIFICATION

Identify a weak position, alignment or player only with:
• Comparable metrics.
• A suitable comparison baseline.
• Adequate sample information.
• Explicit uncertainty.

Test claims such as “soft against the run” using:
• Volume versus efficiency.
• Opponent RB quality.
• Game state.
• Relevant defensive injuries.
• League context.

RB receiving yards per target is not rushing yards per carry.


PHASE 3 — OFFENSE, PLAYER TYPE AND OPPORTUNITY

Build both offensive profiles and include all meaningful participants.

QUARTERBACK PROFILE

Evaluate:
• Attempts and dropbacks.
• Completion and passing efficiency.
• Sacks and pressure response.
• Blitz-package response.
• Time to throw.
• Scramble behavior.
• Offensive-line health.

WR, TE AND RECEIVING-RB PROFILE

Where available, evaluate:
• Snaps.
• Routes run.
• Route participation.
• Targets and receptions.
• Target share.
• Alignment.
• Target depth.
• YAC.
• Red-zone usage.
• Third-down and two-minute usage.

RUNNING-BACK PROFILE

Evaluate separately:
• Carries and carry share.
• Receiving routes.
• Targets and catches.
• Rushing efficiency.
• Receiving efficiency.
• Goal-line work.
• Run-concept and gap usage.

TARGET-SHARE DEFINITIONS

Target share =
player targets / recorded team receiver targets.

Targets / pass attempts is a different metric.
Reception share is not target share.

Compare the last three recorded games with a declared longer baseline.

Distinguish:
• Verified active zero production.
• Verified inactivity.
• Missing records.
• Injury return.
• Role changes.

PLAYER ARCHETYPES

Classify only when supported:
• Volume/possession receiver.
• Explosive/deep receiver.
• Slot receiver.
• Boundary receiver.
• Screen/YAC receiver.
• Checkdown option.
• Red-zone option.
• Early-down running back.
• Receiving running back.
• Goal-line running back.

A player may hold several roles.

ABILITY VERSUS OPPORTUNITY

Do not treat every player as interchangeable.

Separate:
• Participation.
• Opportunity.
• Conversion.
• Yardage efficiency.
• Explosive ability.
• Availability.

Season target rank measures volume, not isolated talent.
Use comparable qualified samples and role-adjusted/career evidence
when available.

Four historical catches do not establish four future targets or catches.
Forecast targets and receptions separately.

INJURIES AND REDISTRIBUTION

A teammate's absence does not automatically transfer targets or carries.

Verify:
• The beneficiary's established role.
• Current participation.
• Compatible defensive matchup.
• Evidence of redistribution.

Returning starters require a role-regime review.
Do not dilute their current role with unverified absent-game zeros.
Do not invent a full-workload rebound.


PHASE 4 — CROSS-REFERENCE AND ALERTS

Compare supplied slips only when a slip is supplied.
Otherwise mark slip comparison NOT_APPLICABLE.

Postgame screening examples:
• 60+ receiving yards.
• 100+ rushing yards.
• 2+ touchdowns.
• 5+ receptions.

These are review triggers, not proof that a pregame value opportunity
existed.

Flag:
• OL/rusher mismatches.
• Injuries and replacement uncertainty.
• Backup-QB effects.
• Game-flow sensitivity.
• Unstable workloads.
• Source discrepancies.
• Unsupported model mechanics.

Separate possible errors into:
• Opportunity.
• Efficiency.
• Availability.
• Execution.
• Source quality.
• Model capability.

Do not assign causation from the final box score alone.

Create stable issues for material data/model defects.
Include evidence and acceptance criteria.


PHASE 5 — IMMUTABLE OUTPUT AND DATABASE HISTORY

Create a unique run folder.
Never overwrite an earlier forecast or report.

Include:
• Request and exact game identity.
• Offensive and defensive profiles.
• Player roles.
• Matchup card.
• Film notes.
• Context and injury evidence.
• Source gaps.
• Alert tables.
• Simulation results.
• All 60 check statuses.

Before assessment, lock:
• Request.
• Conditional lineups.
• Market snapshot.
• Forecast.
• Model/code/spec/config/input hashes.
• Seed.
• Trial count.
• Consistent source snapshot.

Preserve original SQLite, raw evidence and append-only MASTER history.

Append versioned enrichments.
Do not overwrite historical game/team records.

Store canonical metrics once and reference their observation IDs.

Public exports must follow the curated whitelist.
Do not publish credentials, raw media, local paths or private work files.


PHASE 6 — LIVE MONITORING POLICY

Canceled polling remains canceled.

A matchup request does not authorize:
• Restarting the old 15-minute game checks.
• Changing weekly source audits.
• Creating new schedules.

State monitoring applicability explicitly.
Use only separately authorized monitoring.


PHASE 7 — NFL NEXT GEN STATS AND MATCHUP OVERLAP

Check NGS for BOTH teams.
Log unavailable fields honestly.

7A — RECEIVING ROUTES

Where available, collect:
• Complete routes run.
• Slants, outs, curls, digs, posts, corners and go routes.
• Screens, checkdowns and option routes.
• Targets by route.
• Catch rate by route.
• Separation and target depth.
• Red-zone route usage.
• YAC and expected YAC.

Targeted charts do not establish:
• Complete routes run.
• The all-route denominator.
• Open but untargeted routes.

7B — RUSHING CONCEPTS AND GAPS

Collect verified:
• Concept and gap distribution.
• Yards per carry.
• Success rate.
• Yards before and after contact.
• Defensive allowance by A/B/C gap, edge and side.
• Down/distance splits.

Match established RB usage to measured defensive weaknesses.

7C — DEFENSIVE STRENGTH MAP

Map left, middle and right:
• Pass rush.
• Run fits and stops.
• Double teams and stunts.
• Corner coverage.
• Safety support.
• Current personnel.

Retain uncertainty where assignments are not established.

7D — RB SUPPRESSION

Compare:
• Overall rushing efficiency.
• Opponent-quality-adjusted efficiency.
• League and player baselines.
• First versus second half.
• Down and score state.

Low efficiency does not automatically override high volume.
Evaluate both.

7E — CORNERBACK SUPPRESSION

Where verified, compare:
• Coverage grades.
• Coverage snaps.
• Targets, catches and yards allowed.
• Explosives.
• Breakups and interceptions.
• Man/zone and press/off performance.
• Deep-target success.

Team coverage averages do not establish individual assignments.

7F — QB VERSUS BLITZ

Evaluate the declared recent sample, including:
• Completion rate.
• Sack rate.
• Interception rate.
• Rating.
• Time to throw.
• Scramble rate.
• Edge/interior/zone/full-pressure packages.
• OL protection and quick-game answers.

Compare with the opponent's:
• Blitz rate and success.
• Down/distance tendencies.
• Individual rushers.

THE PANTHERS RULE

Before clearing a QB prop, check:
1. Opposing top-ten blitz rate.
2. Opposing top-ten pass-rush win rate.
3. Offensive-line injuries.
4. QB response to the specific pressure package.

Verified pressure/OL risk plus poor QB response requires an explicit
CAUTION review.

Missing required evidence cannot count as safe.

7G — MATCHUP CARD

Include:
• Defensive strength map.
• Player roles, routes and gaps.
• Supported offense-defense overlap.
• QB/blitz/OL interaction.
• Injury window.
• Candidate flags.
• Historical opportunity review.
• Film notes.
• Uncertainty.

One favorable comparison cannot clear the complete card.


PHASE 8 — OFFICIAL FILM, PERSONNEL AND MISSED OPPORTUNITIES

Primary highlight source:
https://www.youtube.com/@NFL

Verify exact game, date, season and official channel.

Supplement with:
• Official gamebooks.
• NFL/ESPN recaps.
• Team recaps.
• Additional properly identified film.

For each observation, log:
• Source URL.
• Timestamp.
• Play reviewed.
• Review method.
• Confidence and limitations.

Distinguish:
• Visual review.
• Transcript review.
• Recap reporting.
• Charted data.

Transcript-only review is not a completed visual film review.

PERSONNEL

Track supported:
• Offensive 10/11/12/13/21 packages.
• Drive-level changes.
• Defensive base, nickel, dime and goal-line packages.
• Matchups between offensive and defensive personnel.

Identify measured versus estimated usage.

SCHEME

Where visible, review:
• Cover 0/1/2/3 and Quarters.
• Coverage rotations.
• Safety depth.
• Press/off technique.
• Fronts and box counts.
• Simulated pressure.
• Run fits.
• Down/distance context.

PLAYERS AND CONCEPTS

Review:
• Scoring involvement.
• Defensive stops.
• OL wins/losses.
• Returnees, rookies and replacements.
• Runs, play-action, quick game, deep shots, screens, RPOs and tricks.

MISSED OPPORTUNITIES

Review drops, inaccurate throws, pressure, failed plays and missed reads
only where evidenced.

Highlights omit plays and often hide routes.
Do not claim complete route, personnel or defender coverage from
a few clips.

Append timestamped film notes and a short scheme summary.
Missing all-22 evidence remains unavailable.


PHASE 9 — ENVIRONMENT, SITUATION AND AVAILABILITY

9A — WEATHER

Verify:
• Venue and roof status.
• Kickoff location/time.
• Temperature.
• Sustained wind and gusts separately.
• Wind direction.
• Precipitation.
• Humidity.

Retain review flags:
• Wind above 15 mph.
• Wind 10–15 mph as a soft review.
• Temperature below 32 F.
• Heat above 95 F with a defined humidity condition.

These are review hypotheses, not automatic fitted yardage changes.
Do not change a verified player role solely because of weather.

9B — REST AND TRAVEL

Measure:
• Actual elapsed hours and calendar days between kickoffs.
• Bye.
• Prior primetime game.
• Back-to-back road games.
• Event-date time zones.

Distinguish estimated venue distance from verified travel.
Do not invent flights, return-home trips or fatigue coefficients.

9C — STAKES AND MOTIVATION

Verify:
• Standings.
• Divisional status.
• Head-to-head history.
• Mathematical clinching/elimination.

Treat revenge, rivalry, trap and effort interpretations as reviewed
hypotheses, not established numerical effects.

9D — INJURIES

Check dated official evidence for:
• QB.
• RB.
• WR.
• TE.
• OL.
• Edge and interior DL.
• LB.
• CB.
• Safety.

Keep separate:
• Practice participation.
• Game designation.
• Inactive status.
• Expected workload limitation.
• Replacement evidence.

DNP, questionable and inactive are different.
No designation does not prove full workload.
A return does not prove a restriction.

Refresh exact-game availability before final clearance.

9E — TURNOVERS

Use a declared rolling window.

Turnovers committed =
interceptions thrown + fumbles lost.

Track total fumbles separately.
Track takeaways and net margin separately.

Distinguish single-game spikes from longer trends.
Causal responsibility requires evidence.
Net margin alone is not turnover luck.

Declare team-game coverage and league comparison methods.

9F — SITUATIONAL EFFICIENCY

Measure:
• Completion rate by down.
• Third-down conversions.
• Third-down passing.
• Red-zone trips and touchdowns.
• Red-zone targets.
• Top-three red-zone target shares.

Declare denominators.
Sacks are not pass attempts.

Red-zone target share uses eligible targets on plays beginning
inside the opponent's 20.

Undefined denominators return null.

9G — UNCLASSIFIED CONTEXT

Review supported:
• Officiating.
• Crowd.
• Field.
• Altitude.
• Coaching changes.
• Other unusual circumstances.

Surface unresolved context.
Do not invent modifiers or silently ignore it.


PHASE 10 — EXTERNAL SOURCE AUDIT

Check every source independently.

Record:
• Actual columns available.
• Player and team coverage.
• Statistical window.
• Access limits.
• Publication/data-through/retrieval times.
• Freshness.

Existing weekly audit schedules remain unchanged.

Under the current 48-hour policy:
• Older required evidence remains STALE.
• Unknown timestamps cannot be certified fresh.

SOURCE 1 — ESPN WIN RATES

Pass-rush and pass-block win-rate leaderboards.

Use actual player/team rates and relevant tackle/rusher identities.
Record pressures and sacks only when supplied.
Win rate does not establish pressure or sack counts.

SOURCE 2 — SHARP POSITIONAL/ALIGNMENT COVERAGE

https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-stats-by-position/

Fields:
• WR YPT allowed.
• TE YPT allowed.
• RB YPT allowed.
• Outside YPT allowed.
• Slot YPT allowed.

SOURCE 3 — SHARP COVERAGE SCHEMES

https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/

Fields:
• Man rate.
• Zone rate.
• Middle-open rate.
• Middle-closed rate.

SOURCE 4 — SHARP DEFENSIVE TENDENCIES

https://www.sharpfootballanalysis.com/stats-nfl/nfl-defensive-tendencies/

Fields:
• Blitz rate.
• Light-box rate.
• Heavy-box rate.
• Sub-package rate.

SOURCE 5 — SHARP ADVANCED BOX SCORES

https://www.sharpfootballanalysis.com/analysis/nfl-advanced-box-scores/

Use only verified available fields:
• EPA per play.
• Success rate.
• Dropback and rush EPA.
• Explosive rate.
• Pressure rate allowed.
• Turnover EPA.
• Red-zone TD rate.
• Average depth of target.
• Deep-target rate.
• Sack rate.
• Blitz rate faced.
• Play-action rate and EPA.
• Time to throw.
• Man coverage faced.

SOURCE 6 — INDIVIDUAL COVERAGE SOURCES

Use verified accessible material from:
• Raiders Rundown.
• StatRankings.
• Hashtag Football.

Where supplied:
• YPT allowed.
• Targets faced.
• Provider grade/trend.
• Explosive count or rate.
• aDOT allowed.
• Perimeter targets.
• Coverage snaps.
• Catch rate allowed.
• YAC allowed.
• Pass breakups.

Discovery-only and paid/inaccessible rows remain gaps.

INTERPRETATION CORRECTIONS

• Lower defensive YPT means stronger coverage.
• Slot and outside are not interchangeable.
• Zone rate alone does not prove seam weakness.
• Sub-package rate does not prove blitz rate.
• Preserve unclassified snaps.
• Do not force man plus zone to equal 100%.
• Preserve provider EPA signs and definitions.
• A team average does not establish a particular player,
  route or replacement weakness.


PHASE 10G — REVIEWED GAME-SCRIPT GATE

Use comparable eligible evidence for BOTH teams:

1. Sharp matchup evidence.
2. Verified game-level EPA per play.
3. Dated stakes/motivation evidence.

Classification requires reviewed justification or a versioned
validated method.

Numerical class thresholds were not supplied.
Do not invent them.

RETAINED LEGACY POLICY WEIGHTS

BLOWOUT FAVORITE:
Policy weight 1.00.

MODERATE FAVORITE:
Deep-ball weight 0.90.
Possession weight 1.00.

TOSS-UP:
Policy weight 0.85.
Identify the supported swing variable.

UNDERDOG:
Block unless the OPPONENT has a verified, reviewed
ELIMINATED/TRAP RISK exception.
Exception weight 0.80 with written justification.

These are retained policy hypotheses.
They are not calibrated probabilities, projected-yardage changes
or betting-stake adjustments.

Important:
• A blowout can reduce passing volume.
• Defensive YPT difference multiplied by all QB attempts
  is not a valid receiver forecast.
• RB receiving YPT cannot block an RB rushing market.
• Script PASS cannot override hard flags, missing evidence
  or calibration requirements.

Output:
SCRIPT classification and method.
Candidate status.
Cited evidence.
Swing variable.
Exceptions.
Policy weight.
Unresolved flags.

Missing required inputs means INSUFFICIENT DATA.


MODEL — EXECUTABLE SIMULATION

Use the existing executable workflow.
Do not invent a different simulation during analysis.

Original entry point:
outputs/nfl.py game TEAM_A TEAM_B

Default run:
100,000 trials.

Record:
• Exact game identity.
• Input cutoff.
• Accepted revision.
• Seed.
• Actual trial count.
• Input/code/spec/config hashes.
• Lineup assumptions.
• All phase statuses.

A receiving agent without the engine/code/data must state:
SIMULATION NOT RUN.

SIMULATION REQUIREMENTS

Keep implemented relationships coherent across:
• Possessions.
• Plays.
• Score state.
• Passing attempts.
• Sacks.
• Rushes.
• Player shares.
• Player outcomes.

Unsupported mechanics remain capability gaps.

PASSING VOLUME

Evaluate leading, trailing and close-game behavior separately.
A favorable efficiency matchup does not automatically create
more passing attempts.

PLAYER PROJECTIONS

Separate:
• Participation.
• Opportunity.
• Conversion.
• Yardage efficiency.

QB:
Passing versus rushing.

RB:
Carries versus receiving targets.

WR/TE:
Targets versus catches versus depth/YAC.

Stress-test:
• Fewer possessions.
• Fewer pass attempts.
• Reduced carries/targets.
• Uncertain participation.
• Adverse efficiency.

Conditional scenarios are not calibrated scenario likelihoods.

OUTPUTS

Report supported:
• Mean.
• Median.
• Prediction intervals.
• Threshold frequencies.
• Assumptions.
• Scope.
• Limitations.

Raw simulation frequencies remain UNCALIBRATED until independent
evaluation passes.

Regulation scoring stays separate from overtime.
Full-game forecasts require supported overtime mechanics.

Do not manufacture unsupported touchdown, alternate-total,
lateral or settlement probabilities.


MARKETS, ALTERNATE LINES AND TOTALS

Read actual FanDuel/DraftKings markets when available.
Alternatively, transcribe supplied screenshots with timestamps.

Keep screenshot quotes separate from verified current prices.

Record:
• Event/player ID.
• Market.
• Side.
• Threshold.
• Odds.
• Source and timestamp.
• Regulation/full-game/overtime scope.
• Push and void rules.

Review available:
• Receiving yards.
• Receptions.
• Rushing yards.
• Rush plus receiving yards.
• Passing yards.
• Supported team/game totals.
• Relevant alternate lines.

If the engine cannot price a market, mark it unsupported.
Do not invent a probability.

Compare model probability with price-implied break-even probability
only when model readiness/calibration supports that comparison.

Historical threshold hit rate is descriptive.
An alternate line is not automatically good value.

ESTABLISHED-ROLE ELIGIBILITY

Require:
• Established key/high-usage role.
• Supporting participation and usage sample.
• A specific compatible defensive weakness.

Reputation alone is insufficient.
A teammate absence alone is insufficient.
A defensive injury alone is insufficient.

Undefined eligibility cutoffs remain unset.

TICKET RULES

• Target six legs.
• Hard maximum seven.
• Never pad.
• Fewer selections or no ticket is acceptable.
• Do not add uncertain replacements merely to raise payout.
• Review shared volume and game-script assumptions.
• Use aligned joint simulation outcomes where supported.
• Never multiply marginal probabilities to claim a same-game
  ticket probability.

No automatic wagers, entries or unsupported settlement claims.


POSTGAME ASSESSMENT AND LEARNING

Assess the locked forecast using:
outputs/nfl.py assess RUN_ID --game-id EXACT_FINAL_GAME_ID

Verify:
• Exact matchup.
• Locked request.
• Artifact hashes.
• Compatible statistical scope.
• Actual source evidence.

Preserve the original forecast.

Report separately:
• Opportunity error.
• Efficiency error.
• Availability error.
• Yardage error.
• Individual threshold outcomes.
• Complete-ticket outcomes.

Statistical hits/misses do not automatically establish sportsbook
settlement.

Missing participation is not zero or automatically void.
Show exclusions and coverage counts.

DEVELOPMENT VERSUS UNTOUCHED TESTING

All 107 previously inspected games and supplied examples are
development evidence.

Do not call them untouched validation.

Keep separate chronological blocks for:
• Development.
• Calibration.
• Final untouched testing.

Fit calibration only on earlier designated data.

Predeclare:
• Thresholds.
• Reliability bins.
• Cohorts.
• Counting rules.
• Baseline comparison.

Do not tune on final-test outcomes.

EVALUATION

Use:
• Brier score.
• Clipped log loss.
• Fixed reliability bins:
  [0,.2), [.2,.4), [.4,.6), [.6,.8), [.8,1].
• Sample sizes.
• Game-cluster uncertainty.
• Role/market breakdowns.
• Comparable baseline cohorts.

The 70–80% individual-selection goal is an aspiration to measure.
It is not a promise or a six/seven-leg ticket probability.

A favorable example or small pilot cannot certify calibration.


ONE-CHANGE-AT-A-TIME IMPROVEMENT

For every model change:

1. Record the issue and evidence.
2. Define acceptance criteria.
3. Scope the implementation.
4. Preserve source facts and prior reports.
5. Run meaningful regression tests.
6. Perform dated frozen-baseline evaluation.
7. Review the result.
8. Accept a new locked revision when justified.

Revision acceptance is not automatic production promotion.

Never rewrite an old forecast or self-promote a model after a win.


AGENT AND LINEAR WORKFLOW

When delegation is authorized, each task must include:
• Stable issue ID.
• Objective.
• Exact allowed files.
• Acceptance criteria.
• Required tests.

Completion brief must include:
• Changed files.
• Tests and results.
• Artifact links.
• Unresolved gaps.
• Verification evidence.

Coordinator independently verifies completion.
An agent's self-report is not proof.

No paid service, subscription or background run is assumed authorized.

Mirror verified issue status to Linear when readable.
If unavailable, preserve the local append-only journal and pending update.

Linear tracks work.
It does not itself execute fixes or replace the source database.


CURRENT OPEN FIX ORDER — OCTOBER 29, 2026

1. CREDITED PLAY YARDAGE

Issue:
ISS-ebcc83ddaf58bbde92e64b5c260b3e215c47332a1f10ef04d67d6d43ebce6fcc

Example:
Golden play 401873007411 has numeric yardage 7 versus a described
37-yard catch followed by a penalty.

Reconcile against authoritative gamebooks before trusting affected:
• Explosive counts.
• Stuff counts.
• Simulation yardage templates.

Do not repair by text parsing alone.

2. RETURNING-PLAYER ALLOCATION

Issue:
ISS-776429323d7fceffc2dfb4a3936b85f3b8d2dadfc18029b96cb54cf3b508fc94

Audit Jacobs/Savion participation and current role regimes.

3. MISSING-PARTICIPATION DENOMINATOR

Issue:
ISS-1eb28b14b506fd56de4656150ed4ac8810586389e17bd7707e607ec00d71ec9b

Audit Coker's recorded appearances without absent-row zeros.

4. QB RUSHING

Issue:
ISS-ff1caad18347c10f7c7a299a7af8cf6991261bd0771604a5e7a6540a9caf6114

Separate QB-specific:
• Scrambles.
• Designed runs.
• Kneels.

Do not substitute generic team rushing templates.

5. REQUIRED EVIDENCE

Complete current:
• Coverage.
• Routes.
• Personnel.
• Broader film review.

Retain stale and unavailable flags.

6. MODEL EVALUATION

Evaluate separately:
• Passing-volume behavior.
• Receiving opportunity.
• Receiving efficiency.
• Untouched probability calibration.
• Selection rules.

Complete player OT splits and OT simulation remain uncertified.


REQUIRED REPORT ORDER

1. Run identity, cutoff, scope, revision, seed/trials and readiness.
2. All-phase checklist with reasons, evidence and gaps.
3. Both defensive profiles and positional allowances.
4. Both offensive profiles and role/opportunity evidence.
5. NGS, film, context and injuries.
6. SCRIPT gate and volume-sensitive scenarios.
7. Supported projections and market/alternate-line comparisons.
8. Correlation review and qualifying shortlist, or no-ticket result.
9. Open issues, next work and reproducibility artifacts.


60-CHECK MANIFEST

Assign a status, reason and evidence to EVERY item.

[ ] P1.pbp — Historical PBP, downs, distance and results.
[ ] P1.boxscores — QB, receiving and rushing boxes.
[ ] P1.tackles_sacks — Supported tackle/sack attribution.
[ ] P1.pressure — Pressure generator and clean/coverage attribution.
[ ] P1.ol_snaps — OL starters, substitutions and snaps.
[ ] P1.air_yards — Target depth and air yards.
[ ] P1.redzone — Red-zone targets and goal-line carries.
[ ] P1.scrambles — Explicit scramble events and limitations.

[ ] P2.team_defense — Production and explosive counts.
[ ] P2.coverage — Coverage and YAC definitions.
[ ] P2.individual_assignments — Verified defender allowances.
[ ] P2.weakest_link — Supported weakest alignment/player.
[ ] P2.pressure_trend — Recent pressure and opponent context.

[ ] P3.team_offense — QB and team production.
[ ] P3.player_roles — Role, uncertainty and ability evidence.
[ ] P3.ol_health — Lineup and OL injury window.
[ ] P3.target_hierarchy — Recent hierarchy and supported changes.
[ ] P3.routes_gaps — Verified routes and running gaps.
[ ] P3.qb_blitz — QB response to opposing blitz packages.

[ ] P4.slip_comparison — Supplied slip comparison.
[ ] P4.injury_alerts — Injury and rusher mismatch alerts.
[ ] P4.script_risk — Backup-QB and workload/script risk.

[ ] P5.bundle — Complete versioned report bundle.
[ ] P5.provenance — Database/input/code/model/spec hashes.
[ ] P5.source_preservation — Protected SQLite and MASTER history.

[ ] P6.live_policy — Monitoring applicability; canceled polling stays off.

[ ] P7.ngs_targeted_charts — Both teams' published chart evidence.
[ ] P7.all_routes — Complete route participation.
[ ] P7.run_concepts — Verified concepts and gaps.
[ ] P7.strength_map — Defensive side/personnel strengths.
[ ] P7.rb_suppression — RB quality, efficiency and game state.
[ ] P7.cb_suppression — Verified individual coverage suppression.
[ ] P7.panthers_rule — Exact QB/OL/pass-rush/blitz review.

[ ] P8.film — Official highlights/recaps actually reviewed.
[ ] P8.personnel — Packages and uncertainty.
[ ] P8.scheme — Coverage, front and run-fit evidence.
[ ] P8.missed_looks — Supported missed opportunities.
[ ] P8.film_notes — Cited notes and unresolved hypotheses.

[ ] P9.weather — Verified kickoff/venue conditions.
[ ] P9.rest_travel — Rest/time zones without invented itineraries.
[ ] P9.stakes — Verified stakes and uncertainty.
[ ] P9.injury_spikes — Exact-game roster availability.
[ ] P9.turnovers — Rolling turnovers and supported interpretation.
[ ] P9.situational_efficiency — Down/red-zone efficiency.
[ ] P9.unclassified — Other context explicitly reviewed.

[ ] P10.espn — Win-rate evidence and requested columns.
[ ] P10.position — Positional/alignment coverage.
[ ] P10.scheme — Coverage schemes.
[ ] P10.tendencies — Defensive tendencies.
[ ] P10.advanced — Game-level advanced efficiency/EPA.
[ ] P10.individual_db — Individual coverage sources.

[ ] P10G.script_gate — Reviewed script gate and policy limitations.

[ ] MODEL.inputs — Valid numbers and resolved identities.
[ ] MODEL.lineup — Specified QB, role and limitations.
[ ] MODEL.simulation — Versioned coherent simulation.
[ ] MODEL.calibration — Independent chronological validation.

[ ] TICKET.markets — Real lines, odds and settlement rules.
[ ] TICKET.roles_matchups — Established role plus compatible weakness.
[ ] TICKET.correlation — Supported joint outcomes.
[ ] TICKET.cap — Six-leg target, seven maximum, no filler.


ORIGINAL-WORKSPACE COMMANDS

Use the project's bundled Python as PYTHON.
Replace capitalized placeholders with verified values.

PYTHON outputs/nfl.py verify

PYTHON outputs/nfl.py game TEAM_A TEAM_B \
  --game-id EXACT_GAME_ID \
  --as-of ISO_TIMESTAMP \
  --trials 100000 \
  --seed INTEGER \
  --run-id UNIQUE_RUN_ID

Optional game inputs:
--lineups FILE.json
--selections FILE.json
--script-input FILE.json

PYTHON outputs/nfl.py assess UNIQUE_RUN_ID \
  --game-id EXACT_FINAL_GAME_ID

PYTHON outputs/nfl.py scoreboard

PYTHONPATH=outputs PYTHON -m unittest discover \
  -s outputs -p 'test_*.py' -v

The public database repository contains database access utilities.
It does not contain the complete local projection engine.

A receiving agent must obtain the appropriate executable code or
explicitly state that it cannot run the simulation.


FINAL OPERATING RULE

No omitted phase.
No unsupported green card.
No fabricated source read.
No invented simulation.
No guessed source repair.
No silent model change.
No automatic entry.

END CURRENT GAME SCRIPT