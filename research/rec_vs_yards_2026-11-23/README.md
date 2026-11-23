# Catches or yards? (Nov 23, 2026)

Asked after Week 11: Malik Nabers had the volume (12 targets, 7 catches) but 55 yards with J.J. McCarthy (18 of 38).
A receiver can clear his catches line and miss his yards line, so the board should say which one our edge is in.

## 1. Does the starter's style move catches or yards? (`study.py`, 5,135 receiver-games 2022-2026)
Starter's depth of throw (aDOT) and accuracy (CPOE) over his last 600 attempts, against the passers whose throws built the
receiver's averages that season:

| Starter vs the receiver's usual passers | 2022-24 catch rate / yards per catch vs his norm | 2025-26 |
|---|---|---|
| 1+ yard shorter | 0.99 / **0.95** (133 games) | 0.98 / 1.00 (47) |
| Similar | 0.99 / 0.99 | 0.99 / 1.02 |
| 1+ yard deeper | 0.99 / **1.04** (225) | 1.02 / **1.17** (73) |

Catch rate barely moves with the QB's depth or accuracy. Yards per catch moves in the expected direction, but the fitted
slopes are weak (z about 1). Shown on the board as context, not applied to projections. A veteran's bad day (McCarthy) is
not held against veterans as a group (research/qb_script_2026-11-22).

## 2. The lean (`dashboard/book_lines.py`, `catch_or_yards_lean`)
At the books' main lines: edge = our chance of the over minus the market's fair chance, for catches and for yards.
Lean **catches** when the catches edge is 5+ points bigger, **yards** when the yards edge is. Week 11 (71 receivers with both
lines, too few to prove anything): catch leans (5) had the catches over win 40% vs yards 20%; yard leans (13) yards 62% vs
catches 54%. A split result (catches over, yards under or the reverse) happened for 14 of 71.
To be graded every week before it moves any pick. Research only.
