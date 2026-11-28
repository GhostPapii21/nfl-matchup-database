# Week 12 game logs - index (GB@LAR only so far) (built 2026-11-26 03:43 AM EST, Blitz, refs NFL-56, refs NFL-49)

Research only. projection_ready stays false. No picks. Sources and pull times are inside each game file.

| Game | Status | Quarter winners (Q1-Q4) | 1H | Close (AN consensus) | ATS | Total | RZ trips (TD) | Game target leader | Most yds on a named defender (tackler tag, inferred) | Most VERIFIED-PBU/INT/DPI credits | Verified / tackler / unattributed pass plays |
|---|---|---|---|---|---|---|---|---|---|---|---|
| GB@LAR | FINAL | Q1 LAR, Q2 GB, Q3 LAR, Q4 LAR | TIE 13-13 | LAR -2.5, 43.5 | LAR | 39 UNDER | GB 1 (1); LAR 4 (2) | Matthew Golden (GB) 5 | GB: K.Nixon 6-52; LAR: K.Curl 2-71 | GB: B.Cisse PBU 0/INT 0/DPI 1; LAR: K.Kinchens PBU 2/INT 0/DPI 0 | 10/31/10 |

Not played yet at pull time (later runs log them): CHI @ DET (11/26 - 1:00 PM EST), PHI @ DAL (11/26 - 4:30 PM EST), KC @ BUF (11/26 - 8:20 PM EST), DEN @ PIT (11/27 - 3:00 PM EST), NO @ CIN (11/29 - 1:00 PM EST), NYG @ IND (11/29 - 1:00 PM EST), NYJ @ MIA (11/29 - 1:00 PM EST), ATL @ MIN (11/29 - 1:00 PM EST), TEN @ JAX (11/29 - 1:00 PM EST), BAL @ HOU (11/29 - 1:00 PM EST), NE @ LAC (11/29 - 4:05 PM EST), WSH @ ARI (11/29 - 4:25 PM EST), SEA @ SF (11/29 - 4:25 PM EST), LV @ CLE (11/29 - 8:20 PM EST), CAR @ TB (11/30 - 8:15 PM EST)

Files: one `<AWAY>_at_<HOME>.md` per game, `pbp/` full play-by-play CSVs, `data/` JSON (pass-play defender log per game), DEFENSE_PROFILES.md, NGS_W12_SNAPSHOT.md, COVERAGE_MATRIX.md. Pregame lock grading and every read graded are inside GB_at_LAR.md.

## UNKNOWN / TODO (GB@LAR)

- Snap counts / snap shares: UNKNOWN. nflverse snap_counts_2026 last updated 2026-11-24 07:01 AM EST (before this game). TODO: re-pull and rerun tools/run_gblar.sh.
- Blitz / pass rushers, man/zone, MOF shell per play: UNKNOWN. nflverse ftn_charting_2026 max week is 11 at pull time. TODO: rerun after the next FTN update.
- True pressure rate: UNKNOWN; QB tables carry an ESTIMATE from sacks + nflverse QB hits only.
- Assigned coverage defender on completions and slot/outside alignment: UNKNOWN in free data (tackler tags are inferred only).
- Team-total and quarter/half prices at the lock: not in the freeze file; period grades use Action Network is_live=false pre-game lines pulled after the game.
- Official video defender evidence: not checked this run.
- NGS statboard: partial (3 receivers over threshold); re-pull after the full week-12 slate.
