# Workflows waiting to be installed

The bots that build these can't write to `.github/workflows/`, because their GitHub token lacks the `workflow` scope
(checked Nov 12 2026: scopes are `gist`, `read:org`, `repo`). To turn one on, someone with that scope moves it into place.

| File | Status | What it does |
| --- | --- | --- |
| `rocket-ci.yml` | **Installed Nov 15 2026** at `.github/workflows/rocket-ci.yml` | NFL-49 CI job: runs `./rocket` (R1 NFL-42 entrypoint, R2 NFL-43, R3 safety, R4 test suites) on every pull request and push to main, and fails the check on a non-zero exit. Read-only. |
| `nfl-source-of-truth.yml` | Superseded, left here for reference | Ran inactives and the phase ledgers after each packet build, with no keys. It could not pass a game: it pulled no prices, locked no snapshot, and relied on GitHub's scheduler, which starts jobs 4 to 7 hours late on this repo. |

## What replaced it: `.github/workflows/nfl-gameday-gate.yml`

The 100k entry point needs, for one game, all of these to be true at the same moment, before kickoff:

1. official inactives pulled after they post (T-90 minutes);
2. the packet's data, news, weather and prices fresh (prices under 20 minutes old inside two hours of kickoff);
3. a four-book price freeze;
4. a locked 100k snapshot (`./rocket <game>` check R5), locked before kickoff, after the price pull;
5. `./rocket <game>` passing.

The game-day workflow runs those in that order, one parallel job per game:

    python -m pipeline.window                        # which games are 40-88 minutes from kickoff and not yet run
    python -m phase15.official_inactives --game G    # free; if a club has not posted yet, stop here and retry next tick
    python -m pregame.build_packets --game G --no-index      # fresh packet + price freeze (up to 10 credits)
    python -m snapshots.lock --config ... --pbp ... --price-freeze ... --packet ...
    python -m pregame.build_packets --game G --no-index      # only if the lock took more than 10 minutes
    python -m pipeline.sim100k --game G --write --rush-dist  # the gate; runs ./rocket G; 100,000 trials if it passes
    python -m pipeline.slate --game G --from-report --expect G   # ledger; exits 2 if the game was refused

It ticks every 15 minutes on game days and decides for itself what is due, so a late start still lands inside a
window. A tick with nothing due spends no credits. Each game's files are committed by its own job; a refusal is
committed too and fails that job. `python -m pipeline.slate --index-only` then rebuilds `pipeline/ledgers/INDEX.md`.

Credits: about 10 per game per attempt, up to 20 when prices are refreshed, so roughly 150-300 for a full week. Nothing
is spent below the credit floor: the manual `credit_floor` input, else the repository variable `ODDS_CREDIT_FLOOR`,
else 800 (the default in `pregame/odds.py`). The workflow never lowers the floor on its own.

Scheduled triggers only fire once the file is on `main`, and a new workflow can only be started by hand
(`workflow_dispatch`) once it is on `main` too.
