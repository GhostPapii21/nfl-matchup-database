# Defensive gate and pressure/blitz matchups for the 80-yard stars (Nov 23, 2026)

Owner's idea: star the player, then upgrade or downgrade him through the defense he faces (what it allows to his
position) and, for receivers, the pass rush (pressure and blitz rates against how his QB plays under pressure and against
the blitz). `python3 study.py --data DIR` -> `results.json`. Fit 2022-24, held out 2025-26 (pressure/blitz: 2025, the
last season with NGS participation data). Bar to be added: held-out log loss and Brier both better and |z| >= 2.

## Already in the star weights
Receivers: projected targets (target share x team pass volume), his yards a game, team implied points, team pass volume,
the defense's 20+ yard completion rate, and the 80-yard games the defense allowed to his position. Backs: carries, yards a
carry, spread, implied points, RB yards a game the defense allows, and (new today) the other back's carries.

## Results
| Candidate | Who | Held-out log loss / Brier vs base | z | Added? |
|---|---|---|---|---|
| Yards a game allowed to his position (relative) | receivers | 0.26885 / 0.07822 vs 0.26911 / 0.07834 | 1.85 | No (just short of the bar) |
| Defense in the 5 most generous vs his position | receivers | 0.26877 / 0.07819 | 1.79 | No (just short) |
| Yards a carry allowed to backs | backs | worse | 1.0 | No |
| 5 most generous vs backs | backs | worse | 0.4 | No |
| QB's expected YPA at the defense's pressure rate | receivers | no gain | -2.9 (wrong direction) | No |
| QB's expected YPA at the defense's blitz rate | receivers | no gain | -0.5 | No |
| Defense pressure / blitz rate | receivers | no gain | 1.9 / 1.4 | No |

Players already starred (30%+), by defense third, held out:
| Defense | Starred receivers: predicted / hit | Starred backs: predicted / hit |
|---|---|---|
| Tough | 39.7% / 37.5% | 39.6% / 43.2% |
| Middle | 41.2% / 33.8% | 40.9% / 47.5% |
| Soft | 40.7% / 42.3% | 43.9% / 36.2% |

Starred receivers against soft defenses already hit about what the model says, so an upgrade on top would over-state
them; for backs a soft run defense did not help at all. Game script (trailing teams throw more, leading teams less) was
tested in `research/qb_script_2026-11-22`: underdogs did not throw more and favourites barely less.

## On the board
Each star now shows its gate (soft / middle / tough, the defense's rank vs his position and yards allowed) and, when the
defense blitzes a lot and the QB is 1+ yard an attempt better or worse against it, a pressure note. Context only; the
receivers' gate (z 1.8) will be re-tested after the season with 2026 added. Research only.
