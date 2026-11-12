# Workflow waiting to be installed

`nfl-source-of-truth.yml` is the NFL-56 scheduled automation. The bot that built it can't write to
`.github/workflows/`, because its GitHub access lacks the `workflow` scope. To turn it on, the repo owner copies it
into place on this branch or after merge:

    git mv pipeline/workflow_to_install/nfl-source-of-truth.yml .github/workflows/nfl-source-of-truth.yml

You can also use GitHub's web editor and create `.github/workflows/nfl-source-of-truth.yml` with the same
contents. It passes no secrets and spends no Odds API credits. Its schedule and `workflow_run` triggers start
firing once it is on `main`.
