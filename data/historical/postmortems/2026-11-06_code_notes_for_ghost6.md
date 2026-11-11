# Code notes for Ghost6 — Friday grading TNF JAX@BAL (2026-11-06)
Held files not edited (run_gate, assemble, rico*_rules, press_tier, rulebook, sims). door.py/rulebook.py exist; read-only.

1. **pbp_live tacklers parser (live ingest):** Washington 50-yd TD stored `tacklers="No Huddle, Shotgun"` (formation tokens). Ledger builder had to treat as unattributed. Fix: strip leading formation parentheticals before writing `tacklers`; never accept formation strings as defender names.
2. **Carry forward 2026-11-05 notes #2–#3:** period/1H game-line model; BACKUP_QB §7 exemption for smash spots when miss-audit clears opponent explosives. JAX 1H −6.5 was wrongly cut and hit 17–3.
3. **TE hierarchy / Strange volume prior:** SCHEME_EDGE on Hawkins OUT over-weighted Strange. Actual Strange 2 tgts; Boerkircher took the 52-yd chunk. Proposal: if TE's last game ≤2 targets OR a TE2 has recent 20+ catches, Strange overs are FLAG-only max until route/snap confirmation — not top-leg SCHEME_EDGE.
4. **Main-vs-alt carding:** Washington o63.5 had model oppose + §7 fail but stayed on Rico4 needing override; 40+ hit. Proposal: when model edge ≤ −5 AND §7 fails on main, proposed slip auto-swaps to lowest alt that passes (or drops the player).
5. **offense_db.csv rebuild:** defense_db got JAX@BAL game-scope rows from ledger; offense_db season sections need `teams/build_team_db.py` after nflverse week-10 pbp lands. Do not hand-edit season aggregates.
6. **Totals garbage / home-run RB:** Game U39.5 lost at 43 on Hill 65 TD while BAL TT U14.5 and skill unders hit. Optional door flag: heavy favorite + opponent change-of-pace RB with explosive prior → soften game-under confidence / require larger number.
7. **Passing-yards ban still not coded in door** (carry 11-03 note #5 / 11-05 context): Lawrence 242 would have cleared 200+; ban was manual. Still need NO_PASS_YDS in door.
