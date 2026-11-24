# Injury context for the 80-yard stars (Nov 23, 2026)

Owner's points: (1) a defense starting backups in the secondary (for WRs/TEs) or at linebacker should help the receivers
and backs facing it; (2) don't project 80+ for a player just off a Questionable listing, concussion protocol or a long
absence. `python3 study.py --data DIR` -> `results.json`. Snap counts 2024-26, injury reports 2025-26. Base: the board's
star models fit on 2022-24, so 2025-26 is held out.

## 1. Defense missing starters (played 70%+ of snaps before, no snaps this game)
| | Weight per missing starter (fit 2024) | z | Held-out log loss / Brier, base -> with it |
|---|---|---|---|
| Receivers vs missing CB/S (TEs: + LB) | +0.16 | 1.5 | 0.2691 -> 0.2716 / 0.0783 -> 0.0791 (worse) |
| Backs vs missing LB/DB | +0.01 | 0.0 | no change |

2025-26 receivers: 0 missing 11.2% hit (11.5% predicted); 1 missing 8.1% (10.4%); 2+ missing 9.0% (10.9%). Teams lean on
backups less than it seems (rotations, the next man was already playing). Not added.

## 2. The player's own status (2025-26, hit 80+ vs the model's prediction)
| Spot | Receiver games | Predicted | Hit | Starred: predicted / hit |
|---|---|---|---|---|
| First game back after missing 1-2 games | 99 | 9.3% | 9.1% | 40% / 67% (6) |
| First game back after missing 3+ | 28 | 10.5% | 17.9% | 42% / 0% (2) |
| Listed Questionable that week | 103 | 16.4% | 14.6% | 40% / 32% (19) |
| Concussion listing in the previous 3 weeks | 46 | 9.0% | 13.0% | 1 player |
| Backs listed Questionable | 26 | 23.9% | 15.4% | 37% / 25% (8) |

Players coming back from missed games or a concussion did about what the model said; their pre-injury averages held.
Questionable players lean lower (starred: 30% hit vs 39% predicted, 27 players) -- not proven, and the bigger risk is
that about a quarter of Questionable players do not play.

## On the board
Each star shows a tag: Q / D (wait for the inactives; Doubtful players usually sit), concussion, or back from injury (games
missed and last game's snap share vs before). Tags only, no automatic downgrade: the data does not support one yet.
Re-test after the season. Research only.
