# OPEN Linear items (LIVE corrected index)
**As of:** 2026-11-26 03:30 EST (America/New_York)
**Source:** Linear workspace `NFL Database` via API (not the Nov 6 static packaging set).
**Note:** Many packaging blockers from the Nov 6 index are now Done on Linear; readiness flags on main still gate `projection_ready`.

## Production-readiness gate (flags on main still fail closed)

| Flag / pillar | Main value | Linear | Notes |
|---|---|---|---|
| projection_ready | false | NFL-75 (Done checklist; flag not flipped) | Only Rico flips |
| NFL-49 P1 freshness/quotes | PASS | NFL-49 Done | quotes=FREE_FEED_ACCEPTED |
| NFL-49 P2 accounting | PASS | NFL-42/43 Done | entrypoint_enforced; NFL-43 bounds ACCEPTED |
| NFL-49 P3 calibration | FAIL | NFL-45 Done on Linear; claim still false | no fitted calibration; no market meets Rico's rule |
| NFL-49 P4 e2e / holdout | FAIL | NFL-7 In Progress; PR #119 draft | 14 scored / weeks 10–11; 0 W12 snapshot LOCKs; even 14+15 remaining W12 = 29 (need W13); GB@LAR post-kickoff cannot be locked |
| pristine_protocol_complete | false | NFL-44 In Progress | aggregation rules now in protocol; Ghost6 verify pending |
| production_validated | false | NFL-7 | calendar-bound through Week 12 MNF |
| PFF | NOT_READY_NO_DUPLICATE | NFL-47/48 | needs access or Rico waiver |
| Source-of-truth workflow install | blocked | NFL-56 In Progress | needs Rico workflow-scope token |

## Active Linear issues (non-Done, NFL-relevant)

| ID | Status | Title | URL |
|---|---|---|---|
| NFL-16 | In Progress | NFL Sim Model: Autonomous Iteration & Validation Tracking | https://linear.app/nfl-database/issue/NFL-16/nfl-sim-model-autonomous-iteration-and-validation-tracking |
| NFL-7 | In Progress | Freeze prospective evaluation and measure the 70–80% individual-selection goal | https://linear.app/nfl-database/issue/NFL-7/freeze-prospective-evaluation-and-measure-the-70-80percent-individual |
| NFL-10 | In Progress | Resolve stale and partial external-source coverage with equivalent verified evidence | https://linear.app/nfl-database/issue/NFL-10/resolve-stale-and-partial-external-source-coverage-with-equivalent |
| NFL-13 | In Progress | Separate overtime outcomes from regulation-only model evaluation | https://linear.app/nfl-database/issue/NFL-13/separate-overtime-outcomes-from-regulation-only-model-evaluation |
| NFL-25 | Todo | Suave Bets source readiness: odds-bridge needs authentication | https://linear.app/nfl-database/issue/NFL-25/suave-bets-source-readiness-odds-bridge-needs-authentication-full-book |
| NFL-40 | In Progress | Market/source gaps: quote inventory, timestamps, no Pinnacle, auth blockers | https://linear.app/nfl-database/issue/NFL-40/marketsource-gaps-quote-inventory-timestamps-no-pinnacle-auth-blockers |
| NFL-44 | In Progress | Complete pristine future evaluation protocol (aggregation/min_coverage/unscorable) | https://linear.app/nfl-database/issue/NFL-44/complete-pristine-future-evaluation-protocol-aggregationmin |
| NFL-47 | In Progress | Coverage/NGS/FTN source gaps — effects remain disabled until verified | https://linear.app/nfl-database/issue/NFL-47/coveragengsftn-source-gaps-effects-remain-disabled-until-verified |
| NFL-48 | Todo | PFF takeaways + W1–8 PFF gaps — authorized refresh only | https://linear.app/nfl-database/issue/NFL-48/pff-takeaways-w1-8-pff-gaps-authorized-refresh-only-no-duplicate |
| NFL-54 | In Progress | Unresolved source: Orca lines identity/access + missing book adapters | https://linear.app/nfl-database/issue/NFL-54/unresolved-source-orca-lines-identityaccess-missing-book-adapters |
| NFL-55 | Todo | FTN NFL models mirror benchmark — access/license unknown | https://linear.app/nfl-database/issue/NFL-55/ftn-nfl-models-mirror-benchmark-accesslicense-unknown-until-retrieved |
| NFL-56 | In Progress | GitHub source-of-truth completeness: 15-phase + news/weather + 100k | https://linear.app/nfl-database/issue/NFL-56/github-source-of-truth-completeness-15-phase-newsweather-100k |
| NFL-60 | In Progress | Cross-model probability correctness, market integrity & evidence-gated validation | https://linear.app/nfl-database/issue/NFL-60/cross-model-probability-correctness-market-integrity-and-evidence |
| NFL-62 | In Progress | Correct push-conditioned NFL prop probability and integer-line EV | https://linear.app/nfl-database/issue/NFL-62/correct-push-conditioned-nfl-prop-probability-and-integer-line-ev |
| NFL-64 | Todo | Validate NFL fixed SD/CV/negative-binomial kappa by market | https://linear.app/nfl-database/issue/NFL-64/validate-nfl-fixed-sdcvnegative-binomial-kappa-by-market-before |
| NFL-65 | In Progress | Align NFL walk-forward backtest with merged push-aware prop probabilities | https://linear.app/nfl-database/issue/NFL-65/align-nfl-walk-forward-backtest-with-merged-push-aware-prop |
| NFL-67 | In Progress | Suave prop cards: reject mismatched sportsbook lines and books in no-vig pairs | https://linear.app/nfl-database/issue/NFL-67/suave-prop-cards-reject-mismatched-sportsbook-lines-and-books-in-no |
| NFL-68 | In Progress | NFL Nov 8 Sunday readiness gate: probability, exact-market EV, CI and as-of sources | https://linear.app/nfl-database/issue/NFL-68/nfl-nov-8-sunday-readiness-gate-probability-exact-market-ev-ci-and-as |

## Open GitHub PRs (not merged; most draft — human/Ghost6 approval required)

| PR | Title | Draft |
|---|---|---|
| #131 | W12 GB@LAR research/grade + price freeze (NOT a pristine LOCK; no snapshots/2026_12_GB_LA) | yes |
| #130 | NFL-44 aggregation rules + readiness docs (this track) | no |
| #120 | W11 late game log: MNF CIN@WSH + defense profiles | yes |
| #119 | NFL-49 P4: score Week 11 holdout (12 games) | yes |
| #116 | Board: exclude IR/out on 80+ watch | yes |
| #113 | NFL-56 W11 Monday gap-fill | yes |
| #107 | Live tracker: defender parser + coverage labels | yes |
| #69 | W11 focus-9 research packet | yes |
| #64 | Add NFL player prop edge research | no |
| #63 | TNF W11 IND@HOU blocked run report | yes |
| #55 | LAC@BAL MNF scheduled-edge Ghost6 vet fixes | yes |
| #41 | Week 9 alt-line historical test pulls | yes |
| #39 | NFL-75 Phase 2b depth/INT pooling | yes |
| #30 | docs: SEMANTICS_BOUNDS clock and rare plays | yes |
| #18 | Draft: local nfl-database snapshot (do not merge) | yes |
| #14 | Week 10 WAS-NYG DK/FD odds snapshot | no |
