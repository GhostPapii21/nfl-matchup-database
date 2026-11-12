# The 15 phases: what runs each one (NFL-56)

**Pull** is the existing builder, `python -m pregame.build_packets`, which runs on a schedule in
`.github/workflows/nfl-pregame-packets.yml` and writes `pregame/packets/<game>/packet.json` with its own
phase ledger. **Check** is the NFL-56 layer, `python -m pipeline.phases --game <game_id> --phase <n>`, which
re-checks that phase input by input and against the freshness windows in [DATA_FRESHNESS.md](DATA_FRESHNESS.md),
then lists what is FILLED, MISSING, STALE or NOT_YET. `--write` saves `pipeline/ledgers/<game>.json/.md`, and
`--strict` exits 3 if any selected phase is not filled. `python -m pipeline.slate` does every game in
`pregame/packets/latest.json` and writes `pipeline/ledgers/INDEX.md`.

| # | Phase | Inputs checked (both teams where relevant) | Freshness sources | Not in any free source (shown, never faked) |
| --- | --- | --- | --- | --- |
| 1 | Slate, schedule, venue | kickoff, date, site, roof, listed QBs | schedule | |
| 2 | Player identity and position | offense players | rosters | |
| 3 | Verified player game history | offense players, by-game logs | play-by-play | |
| 4 | Role, snaps, routes, opportunity | players, snap shares | snap counts | routes run / route participation |
| 5 | Team offense/defense baselines | allowed, produced, ranks | play-by-play | |
| 6 | Opponent context and game script | market spread and total | schedule | the script call (analyst) |
| 7 | Coverage structure and shell | charted dropbacks (blitz, play-action) | FTN | man/zone, shell |
| 8 | Defender assignment and explosives | per-defender PFR rows | PFR defense | who covers whom |
| 9 | QB pressure, blitz, scramble | defense allowed | play-by-play, FTN | true pressure rate |
| 10 | Offensive line, pass rush, coaching | depth chart, coaches | depth charts | line grades |
| 11 | Injury and depth chart | official report, ESPN live, depth chart | official injuries, news, depth charts | |
| 12 | Weather, roof, travel | roof, weather status | weather | |
| 13 | Timestamped book prices | packet book markets | odds, four-book freeze | true opening line |
| 14 | Projection and simulation (100k) | team projection | (the gate in `pipeline/sim100k.py`) | |
| 15 | Final inactive pregame freeze | n/a | official inactives | |

Phase 14's command is the 100k entry point, `python -m pipeline.sim100k --game <game_id>`. It is NOT_YET
whenever that entry point refuses. See the README section "Projection pipeline: goal vs current status".
When every gate passes it runs the NFL-43 possession engine (`core/possession_engine_v0` `simulate_games`, through
`snapshots/lock.py` `run_sim`, the same call the snapshot locker makes) for exactly 100,000 trials, on the game's single
`data_only` config and the newest committed as-of PBP `data/historical/nflverse/pbp_<season>_w1_<wk-1>_pulled_*.parquet`.
G2 also checks that config's `semantics` block (penalties / returns / overtime modes must each be documented in the
reviewed `SEMANTICS_BOUNDS.md`, `ot_rule` must equal the overtime mode), and G7 checks the as-of inputs (no target game
or week >= target in the PBP, every history week present, before kickoff). After the run, a trial count other than
100,000, a non-OK chunk, or engine-reported semantics different from the gated config is a refusal.

## Hooks for pieces other owners are building (`pipeline/hooks.py`)

| Hook | Owner | Until it lands |
| --- | --- | --- |
| NFL-43 semantics: `SEMANTICS_BOUNDS.md` present, `known_flags/KNOWN_LIMITATIONS.json` with `unsupported_semantics` empty and `DEFERRED_100K` false, `known_flags/NFL43_REVIEW.json` ACCEPTED for the current bounds file, and the engine config's `semantics` modes documented in it | BetGuru / reviewer | 100k gate G1/G2 refuse |
| `ROCKET_COMMAND`, the `rocket` validation command, run with the game id and required to exit 0 | BetGuru | 100k gate G6 refuses |
| Four-book freeze: newest `pregame/price_freezes/*_<AWAY>@<HOME>/freeze_*.json`, read only, Blitz's module never imported | Blitz | phase 13 MISSING; gate G4/G5 refuse |
| `official_inactives` in `REGISTRY` | no owner yet (NFL-46 / NFL-49) | phase 15 NOT_YET or MISSING; gate refuses |

Binding a hook is a reviewed pull request that also updates `test_shipped_hooks_fail_closed`. Neither an
environment variable nor a flag can bind one.
