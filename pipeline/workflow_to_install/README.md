# Workflows waiting to be installed

The bots that build these can't write to `.github/workflows/`, because their GitHub token lacks the `workflow` scope
(checked Nov 12 2026: scopes are `gist`, `read:org`, `repo`). To turn them on, the repo owner copies them into place
(or uses GitHub's web editor with the same contents):

    git mv pipeline/workflow_to_install/nfl-source-of-truth.yml .github/workflows/nfl-source-of-truth.yml
    git mv pipeline/workflow_to_install/rocket-ci.yml .github/workflows/rocket-ci.yml

| File | What it does | Triggers |
| --- | --- | --- |
| `nfl-source-of-truth.yml` | NFL-56 scheduled automation: pulls Phase 15 official inactives for games inside [T-120m, kickoff] (`python -m phase15.official_inactives --slate`), writes phase ledgers (each with a Phase 15 AUTO / NOT_YET / MISSING block, source and pull time) and the 100k gate result, commits `pipeline/ledgers` and `phase15/inactives`. | after the pregame-packet workflow, plus T-90 crons |
| `rocket-ci.yml` | NFL-49 CI job: runs `./rocket` (R1 NFL-42 entrypoint, R2 NFL-43, R3 safety, R4 test suites) and fails the check on non-zero exit. Read-only. | every pull request, pushes to main, manual |

Neither passes secrets or spends Odds API credits. Schedule and `workflow_run` triggers only fire once the file is on
`main`.
