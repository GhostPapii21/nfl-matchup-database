# NFL matchup database

Public research snapshots; `manifest.json` records the current build time, coverage and table counts. Download the database and query it locally with Python or SQLite. The maintainer’s local automation checks for changed data daily at 9:00 AM Eastern. See [SYNC.md](SYNC.md) for operation and availability limits.

## Get the data

```sh
git clone https://github.com/GhostPapii21/nfl-matchup-database.git
cd nfl-matchup-database
python3 prepare.py
python3 query.py --tables
python3 query.py --sql 'SELECT game_id,date,status FROM games ORDER BY date DESC LIMIT 12'
python3 query.py --schema games                      # columns of one table
python3 query.py --sql 'SELECT * FROM games WHERE date >= ?' --param 2026-10-01 --format csv
```

Or download **nfl_matchups.sqlite.gz** from this repository and decompress it. `manifest.json` contains table counts, snapshot time and SHA-256 checksums. `schema.sql` documents the database structure. Python tools use only the standard library.

### Use with Grok or another research tool

Connect this repository through your tool's GitHub connector, or download the files above. Start by reading `manifest.json`, `schema.sql` and `DATA_GAPS.md`. Connecting a repository does not establish that a tool can decompress or query SQLite: verify that capability before relying on its analysis. If the tool can execute Python, run `prepare.py` and the read-only `query.py` commands. Otherwise, query a local copy and supply the relevant JSON output with its snapshot timestamp and source limitations.

A useful first request is: "Read this repository's manifest, schema and data-gap report. State the snapshot time and game count. If you can query the SQLite archive, list the latest 12 games and show the query used. If you cannot, say so. Keep recorded source facts separate from inferred profiles; do not replace missing values with zero or claim the model is validated."

## Automatic pregame packets

For every Thursday, Sunday and Monday game, a scheduled workflow builds a research packet from current public data: what each defense allows by position, explosive plays, pass rush, each offense's usage and form, injuries, depth charts, roster moves, matchup edges, and research-only projections, with the 15-phase ledger showing what is filled and what is missing. Start at [pregame/packets/INDEX.md](pregame/packets/INDEX.md). To have ChatGPT or Grok turn a packet into a breakdown with a brainstorm and a critical review, paste [pregame/ANALYST_PROMPT.md](pregame/ANALYST_PROMPT.md). Details and limits: [pregame/README.md](pregame/README.md). Research only; `projection_ready` is false.

## Projection pipeline: goal vs current status (NFL-56)

### Goal: what this repository is meant to do

The repository is the single source of truth for every step from pulling data to running simulations. Bots fetch and run everything from here: source pulls, freshness checks, news, injuries, inactives, weather, four-book prices, all 15 phases, and a 100,000-trial simulation that runs only when every input is present and fresh. Routines keep it current, so nobody has to keep a session open. Picks are allowed only after the NFL-49 acceptance gate passes and Rico sets `projection_ready`.

### Current status: what works now and what is blocked

**Works now**

- Pulls: scheduled pregame packets (`.github/workflows/nfl-pregame-packets.yml`).
- Per-phase checks: `python -m pipeline.phases --game <id> --phase <n>`. Each of the 15 phases is marked AUTO, PARTIAL, MISSING, STALE or NOT_YET, with the missing inputs named. See [docs/PHASE_WORKFLOWS.md](docs/PHASE_WORKFLOWS.md).
- Freshness windows for each source: [docs/DATA_FRESHNESS.md](docs/DATA_FRESHNESS.md).
- The 100k entry point, `python -m pipeline.sim100k --game <id>`. It is fail-closed: it exits 2 with a plain reason whenever any required input is missing or stale, and it has no override.
- A scheduled workflow that runs after every packet build and after inactives post, and commits [pipeline/ledgers/INDEX.md](pipeline/ledgers/INDEX.md). It is written and ready, but **not installed yet**: it sits in `pipeline/workflow_to_install/` until the owner moves it into `.github/workflows/`, because the building bot's GitHub access cannot write workflow files. Until then, run `python -m pipeline.slate` by hand.

**Blocked or pending**

| Piece | Status | Owner |
| --- | --- | --- |
| `projection_ready` | **false** (only Rico flips it, through NFL-49) | Rico |
| 100k runs | **Refused today.** `DEFERRED_100K` is true. | — |
| NFL-43 penalties, returns, overtime | **Pending dependency.** Unsupported, and `SEMANTICS_BOUNDS.md` does not exist yet. | BetGuru |
| `rocket` validation command | **Pending dependency.** The hook `ROCKET_COMMAND` is unset. | BetGuru |
| Four-book price feed (FanDuel, DraftKings, Hard Rock, Caesars) | **Pending dependency.** It is on an unmerged branch. Until a freeze file exists for a game, phase 13 is MISSING. | Blitz |
| Official inactives (phase 15) | **No source yet.** NOT_YET before T-90, MISSING after. | unassigned (NFL-46 / NFL-49) |
| Calibration, pristine holdout, end-to-end run | Not done (NFL-44, NFL-45, NFL-49) | BetGuru / NFL-49 |
| Man/zone, routes, line grades, defender assignment | No free source. Shown as not available, never filled in. | — |

## Coverage

The initial release covers all 93 games in Weeks 1–6 and 13 Week 7 games, including all 12 October 25 games. Consult `manifest.json` for the latest game counts and dates. Layers include ESPN play-by-play and player/box-score statistics, offensive and defensive profiles, external observations and gaps, supplemental public datasets, and official NGS chart URL indexes.

Supplemental coverage is strongest for Weeks 1–6: FTN charting, snap counts, PFR advanced statistics, weekly injuries, NGS aggregate statistics, pregame depth charts and Sharp advanced box scores. Do not assume every layer covers every game. Query tables and inspect source timestamps before combining records.

The initial NGS indexes include 187 targeted receiving charts and 182 carry charts; current counts are in `manifest.json`. Targeted charts are not complete route trees. NFL chart images, user video, screenshots and raw webpage archives are not bundled; original source links remain available. Local filesystem paths have been removed from this public copy. Original private working files remain separate.

## Interpretation and gaps

Verified source inputs and inferred profiles are separate layers. Player ID namespaces differ by provider. Null/missing is not zero. Season aggregates are scouting context, not game-specific measurements. Retrospective retrieval does not establish what was known before kickoff.

Complete route participation, TPRR/YPRR by coverage, comprehensive RB run concepts, coverage shells, player-level assignments, film attribution and daily injury chronology remain incomplete. Phase 9 environmental/situational requirements are documented requirements, not a complete implemented context pipeline. Source freshness and missing mandatory checks still block full readiness. Phase 10G policy weights are uncalibrated rules, not validated predictions. This repository provides research data, not betting recommendations.

See `DATA_GAPS.md` for the recorded source audit. In-database `external_gaps` and source timestamps provide detailed evidence. No automated green-card readiness is certified.

The October 29 publication review also records open credited-play-yardage, returning-player workload, participation-denominator and QB-rushing defects. Treat derived explosive counts and affected baseline projections as provisional. This package publishes the research database and access utilities; the projection model remains subject to separate fixes, regression tests and independent evaluation before release.

## Sources and reuse

See [SOURCES.md](SOURCES.md). Third-party data retain their original ownership and applicable source terms; this repository does not relicense those data. In particular FTN charting distributed through nflverse requires its source attribution and applicable share-alike license. Cite original providers and this snapshot when using derived results.

## Model checkpoint (not production-validated)

The matchup snapshot above is unchanged. A portable research checkpoint of the possession and period engines is added beside it. **`projection_ready` is false.** This is not a betting engine, and it does not produce picks.

| Claim | Current state |
| --- | --- |
| Production validation | Not validated. Acceptance is fail-closed. |
| `projection_ready` | false |
| Validation entrypoint | Not enforced. `core/possession_engine_v0/runs/dal_ind_suite_fix_2026-11-06/validate.py` is the historical contaminated validator (`sha256 29b6b0c2644f256a705b09b5e1a56716dd355d79eb07a6187b9c3df495ff93e9`). Do not promote it. See NFL-42. |
| Penalties, returns, official overtime | Unsupported. See NFL-43. |
| Calibration | Not fitted. Quotes are `NOLINE` until authenticated book access exists. See NFL-45. |
| Pristine evaluation | Protocol incomplete. Weeks already inspected are development evidence, not an untouched holdout. See NFL-44. |
| 100k trials and the 15-phase ledger | Ledger and fail-closed 100k entry point exist (`pipeline/`, NFL-56). 100k runs are still refused (`DEFERRED_100K`, NFL-43, `rocket`, four-book feed, inactives). Phase 15 inactives are `NOT_YET`. See "Projection pipeline: goal vs current status". |
| ORCA / FTN model mirrors | `ACCESS_UNKNOWN`. No quotes are invented. NFL-53, NFL-54, NFL-55. |
| Pinnacle and other books | No actionable lines are published. Pinnacle Q2–Q4 spreads were already absent in the saved research set. Odds-bridge still needs authentication. NFL-25, NFL-45. |

Open work, with live issue URLs, is in [OPEN_LINEAR_ITEMS.md](OPEN_LINEAR_ITEMS.md) (22 items, including NFL-16 and NFL-54). Source access and the public refresh steps are in [docs/SOURCE_STATUS.md](docs/SOURCE_STATUS.md) and [docs/DATA_UPDATE.md](docs/DATA_UPDATE.md). The proposed routine is documentation only: [docs/PROPOSED_ROUTINE_BOOTSTRAP.md](docs/PROPOSED_ROUTINE_BOOTSTRAP.md). The parent applies any saved routine after this commit is verified. The scheduled GitHub Actions workflows (pregame packets, NFL-56 ledgers) run at fixed times; nothing runs on a continuous loop.

Bounded check, after `python3 -m pip install -r requirements-smoke.txt`:

```sh
bash scripts/smoke_offline.sh
```

That runs two offline pytest modules. It does not fetch data, fit a model, or certify the 15-phase or 100k workflows.

Every offline suite (root, period and possession engines, gamebooks, team DB, market calibration, source-run gate) runs with `pip install -r requirements-test.txt && bash scripts/test_offline.sh`, and on every pull request through `.github/workflows/offline-tests.yml`. Tests that need unpublished local inputs (the saved quote CSVs, the optional Outlier export) are reported as skipped with the reason, not passed. The security review and the hash-only exclusion list are `inventory/PUBLIC_SECURITY_REVIEW.md` and `inventory/EXCLUSIONS.json`. Archive hashes are in `inventory/RESTORE_VERIFICATION.json`.
