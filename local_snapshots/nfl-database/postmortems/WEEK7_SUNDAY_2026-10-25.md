# Postmortem: Week 7 Sunday slips (Oct 25, 2026), from user's FanDuel screenshots sent Oct 29. Stats from /workspace/nfl-database/fixes/fixes.sqlite (nflverse, fetched Oct 29 4:53 AM ET).
Tickets: $50 SEA SGP (JSN 3rd-qtr 10+ lost), $20 bonus 7-leg (cashed out $139.46; Walker TD lost), $25 bonus 10-leg, $125 bonus 12-leg, $15 bonus 10-leg (all lost).
Scores: SEA 20 KC 3; DET 20 GB 17; CIN 35 BAL 13 (BAL led 13-0 at half); TB 43 CAR 13; NYG 27 HOU 21 OT.
Misses:
- Kenneth Walker III (KC): 14 of 16 team carries, 36 rush yds (2.6 YPC), 21 rec; Wk6 had 19-128. KC scored no TD. Cause: offense shut down / game script, not role.
- Sam LaPorta: 97% snaps, 2 of 31 targets, 18 yds. DET ran Gibbs 29-116 + 6 tgts.
- Matthew Golden: 12 targets, 85% snaps, 39 yds (prior 123, 104). High rungs (50+/70+) on a volatile yards profile.
- Derrick Henry: 17-45; BAL outscored 35-0 after half (trailing rule).
- Tetairoa McMillan: 6 tgts, 40 yds (40+ hit, 80+ missed). CAR lost by 30.
- Nico Collins: 5 tgts, 6 yds.
- Bryce Young 200+ passing missed (CAR blown out; QB played 77% snaps).
Hits: JSN 150, Kittle 88, McBride 13 tgts/111, Nabers 111, Watson 57, Gibbs, McCaffrey, Bijan, Golden 4+ catches.
Lessons: RB legs depend on offense sustaining drives — grade the offense vs the defense first (KC vs SEA). TE yards need a target-share check vs the run-heavy script (DET leaned Gibbs). Use moderate rungs for volatile-yards WRs even with high volume. Avoid stars on teams projected to get blown out.
