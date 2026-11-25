# Does a blitz-heavy defense move targets to TEs and backs? (2026 Weeks 3-10)

Asked after MNF Nov 23 (Washington blitzed Burrow all night). Data: Sharp advanced box scores (PR #122) plus nflverse
targets by position. Each offense is compared with its own earlier games. The defense's blitz rate comes from its earlier
games only, so this is what the board could have known. 228 team-games. `python3 research/blitz_targets_2026-11-24/study.py`.

| Per 10 points more blitz (defense's earlier rate) | Effect | z |
|---|---|---|
| RB+TE target share | +0.3 point | 2.2 |
| WR1 target share | -0.3 point | -2.4 |
| aDOT | -0.22 yards | -7.9 |
| Deep-target rate | -1.1 points | -13.0 |
| Time to throw | -0.016 sec | -4.6 |

- Blitzing is a trait: a defense's earlier rate correlates 0.58 with its rate this game.
- What pays fastest is depth, not target share. Throws come out shorter and fewer go deep. That hits WR1 yards and
  long-catch props, not his catch count. The TE/RB target bump is real but tiny (about a tenth of a target a game).
- Man coverage moves more targets off the WR1 than blitz does (-0.7 point per 10 points of man, z -4.6). Pressure does not.
- By defense-blitz third, RB+TE share barely moves (+0.8 / -0.2 / +0.9 points); aDOT goes +0.4 -> -0.3 yards.

Brief changes: the WR1 flag now says fade yards, not catches. No TE/RB catches boost was added, because the test does
not support one. Each defense shows its blitz game by game (how many games at 35%+, and the range). One season, ten
weeks: re-check at year end.
