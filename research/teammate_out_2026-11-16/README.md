# When a teammate is out, who gets his work? (Nov 16, 2026)

Asked after Week 10, when several receivers had target spikes with a teammate out (Collins 16, Pickens 18, Wilson 14)
and a backup running back (Emmett Johnson) got 22 carries the board had projected for a starter ESPN already listed out.

    python3 research/teammate_out_2026-11-16/study.py    # 2022-2026; rows_*.parquet (ignored) and results.json

A player is "out" when he had a real role (8%+ of team targets or 15%+ of running-back carries over 3+ games), played
one of the team's last two games, is not active on that week's roster and has no target or carry in the game.
761 team-games had a target earner out; 364 had a ball carrier out. Fit on 2022-24, checked on 2025-26.

## Targets

| Who | Games | Share before | Share in the game | Gain as a share of the missing work |
| --- | --- | --- | --- | --- |
| Top healthy player at the missing player's position | 830 | 16.8% | 18.7% | 9% |
| Second at that position | 634 | 11.5% | 12.6% | 5% |
| Third or lower at that position | 695 | 7.2% | 7.6% | 2% |
| Top player at another position | 1,403 | 16.1% | 15.8% | none |
| Everyone else at another position | 2,180 | 8.1% | 6.8% | none |

- The top same-position player gains about 2 share points on average (about 3 against a control that drifts down 1), and
  about 5 points when 25%+ of the team's targets are missing.
- Spikes are more likely, not typical: his share rose 10+ points in 17% of games with 15-25% missing and 27% with 25%+
  missing, against 8-10% with nobody out.
- Most of the missing work goes to replacements with no history: players without a baseline took 16% of targets when 20%+
  was missing, against 8% normally.
- The board's old rule (spread 80% of the missing share over everyone in proportion) was worse than no adjustment on
  2025-26 (share error 0.061 against 0.057). The fitted rule is 0.056-0.058 and removes the under-projection of the top
  same-position player (bias -1.9 points with no adjustment, +1.8 with the old rule, -0.7 fitted).

## Carries

| Missing carry share | Games | Top healthy back before | In the game | Gain as a share of the missing work |
| --- | --- | --- | --- | --- |
| 15-35% | 138 | 64% | 65% | 5% |
| 35-55% | 91 | 50% | 64% | 32% |
| 55%+ | 131 | 34% | 63% | 41% |

- When a lead back is out, the next back ends up with about 63-65% of the carries (about 13 a game) whatever he had before.
- Share error on 2025-26: 0.210 with no adjustment, 0.184 with the old rule, 0.165 fitted. The old rule over-projected the
  next back by 14 share points; the fitted rule is within 2-4.

## Rule now in `dashboard/opportunity.py`

Targets: top healthy player at the position gets at least 18% of the missing share; others there get 90% of it times
their slice of the healthy share; other positions get 20% of it times their slice. Carries: top healthy back 42% of the
missing share; other backs 51% of it times their slice. `dashboard/extras.py` now treats a player as out when either
the official report or ESPN says so, and `dashboard/build.py` adds the official game-day inactives when a verified pull
exists.

Week 10 check on Saturday's data: Emmett Johnson goes from 4.2 projected carries (1% for 80+ yards) to 12.3 (22%); he
had 22 for 101. The receiver spikes are not caught: Collins stays at 5.6 projected targets and Pickens at 7.1. Research only.
