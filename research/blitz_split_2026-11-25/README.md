# Does the blitz decide who gets the ball? Player-level tests (Nov 25, 2026)

Owner's point after MNF: with Burrow under heavy blitz in the rain, short routes and the tight ends got the ball, not Chase.
The league-average test (research/blitz_targets_2026-11-24) found only +0.3 point of RB+TE share per 10 points of blitz.
Two player-level versions, 2026 Weeks 4-11, FTN blitz marks on every dropback, earlier weeks only:

1. `study.py`: each receiver's own target share on blitzed vs non-blitzed dropbacks, mixed by the defense's blitz rate.
   908 receiver-games. Error vs plain season share: all games +0.4%; vs blitz-heavy defenses -0.3% (CI includes 0).
   **No gain.** A player's blitz split is mostly noise at this sample size.
2. `depth_study.py`: yards per target vs his own norm, by his usual depth and the defense's blitz rate. Deep receivers
   vs blitz-heavy defenses: -0.35 yards per target (CI -1.4 to +0.6); short receivers: -0.26. **No clear pattern.**

What does hold (tested, already in the projections): a blitz-heavy defense shortens throws (aDOT -0.22 yd and deep rate
-1.1 pts per 10 points of blitz), and man coverage moves targets off the WR1 (-0.66 pt share per 10 points of man).
MNF looks like Washington's game plan (bracketing Chase, per postgame reporting) plus rain plus McLaurin's absence, more
than blitz alone. Next: track the blitz flag forward from Week 12 and re-test at the end of the season. Research only.
