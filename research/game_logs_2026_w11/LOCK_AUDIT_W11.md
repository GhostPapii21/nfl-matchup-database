# Week 11 lock audit (2026-11-23, Blitz; refs NFL-49, refs NFL-56)

Checked every `snapshots/2026_11_*/*/LOCK.json` on origin/main against the ESPN scoreboard kickoff (site.api.espn.com week 11, pulled 2026-11-23 07:09 AM AST). Valid = locked_utc earlier than the actual ESPN kickoff. No lock was created, edited or re-timed; locked prices and timestamps are untouched.

| Game | locked_utc | Locked (AST) | ESPN kickoff (AST) | Status | Notes |
|---|---|---|---|---|---|
| ARI_KC | 2026-11-22T12:40:43Z | Sun Nov 22 08:40 AM AST | Sun Nov 22 02:00 PM AST | VALID (pre-kickoff) | price_status PACKET_TWO_BOOK_NOT_FOUR_BOOK; asof_checks PASS; projection_ready False |
| BAL_CAR | 2026-11-22T13:01:29Z | Sun Nov 22 09:01 AM AST | Sun Nov 22 02:00 PM AST | VALID (pre-kickoff) | price_status PACKET_TWO_BOOK_NOT_FOUR_BOOK; asof_checks PASS; projection_ready False |
| CIN_WAS | 2026-11-22T13:40:34Z | Sun Nov 22 09:40 AM AST | Mon Nov 23 09:15 PM AST | VALID (pre-kickoff) | price_status PACKET_TWO_BOOK_NOT_FOUR_BOOK; asof_checks PASS; projection_ready False |
| CIN_WAS | 2026-11-22T16:26:06Z | Sun Nov 22 12:26 PM AST | Mon Nov 23 09:15 PM AST | VALID (pre-kickoff) | price_status PACKET_TWO_BOOK_NOT_FOUR_BOOK; asof_checks PASS; projection_ready False |
| IND_HOU | none |  | Thu Nov 19 09:15 PM AST | MISSING | No LOCK.json under snapshots/2026_11_IND_HOU on main or any remote branch. Earliest pregame artifact (pregame/packets packet.json generated_utc 2026-11-20T03:39:41Z) is after kickoff. A lock now would be post-kickoff and invalid, so none was created. |
| JAX_NYG | 2026-11-22T13:21:12Z | Sun Nov 22 09:21 AM AST | Sun Nov 22 05:25 PM AST | VALID (pre-kickoff) | LOCK kickoff_utc field says 2026-11-22T18:00Z but ESPN kickoff is 2026-11-22T21:25Z; metadata error only (locked_utc is before both); price_status PACKET_TWO_BOOK_NOT_FOUR_BOOK; asof_checks PASS; projection_ready False |
| LV_DEN | 2026-11-22T14:15:16Z | Sun Nov 22 10:15 AM AST | Sun Nov 22 05:25 PM AST | VALID (pre-kickoff) | price_status PACKET_TWO_BOOK_NOT_FOUR_BOOK; asof_checks PASS; projection_ready False |
| LV_DEN | 2026-11-22T15:24:49Z | Sun Nov 22 11:24 AM AST | Sun Nov 22 05:25 PM AST | VALID (pre-kickoff) | price_status PACKET_TWO_BOOK_NOT_FOUR_BOOK; asof_checks PASS; projection_ready False |
| LV_DEN | 2026-11-22T20:28:26Z | Sun Nov 22 04:28 PM AST | Sun Nov 22 05:25 PM AST | VALID (pre-kickoff) | price_status OK; asof_checks PASS; projection_ready False |
| MIA_BUF | 2026-11-22T12:32:34Z | Sun Nov 22 08:32 AM AST | Sun Nov 22 02:00 PM AST | VALID (pre-kickoff) | price_status PACKET_TWO_BOOK_NOT_FOUR_BOOK; asof_checks PASS; projection_ready False |
| MIA_BUF | 2026-11-22T13:40:38Z | Sun Nov 22 09:40 AM AST | Sun Nov 22 02:00 PM AST | VALID (pre-kickoff) | price_status PACKET_TWO_BOOK_NOT_FOUR_BOOK; asof_checks PASS; projection_ready False |
| MIN_SF | 2026-11-22T13:49:18Z | Sun Nov 22 09:49 AM AST | Sun Nov 22 09:20 PM AST | VALID (pre-kickoff) | price_status PACKET_TWO_BOOK_NOT_FOUR_BOOK; asof_checks PASS; projection_ready False |
| MIN_SF | 2026-11-22T16:05:35Z | Sun Nov 22 12:05 PM AST | Sun Nov 22 09:20 PM AST | VALID (pre-kickoff) | price_status PACKET_TWO_BOOK_NOT_FOUR_BOOK; asof_checks PASS; projection_ready False |
| NO_CHI | 2026-11-22T12:51:28Z | Sun Nov 22 08:51 AM AST | Sun Nov 22 02:00 PM AST | VALID (pre-kickoff) | price_status PACKET_TWO_BOOK_NOT_FOUR_BOOK; asof_checks PASS; projection_ready False |
| NO_CHI | 2026-11-22T14:00:56Z | Sun Nov 22 10:00 AM AST | Sun Nov 22 02:00 PM AST | VALID (pre-kickoff) | price_status PACKET_TWO_BOOK_NOT_FOUR_BOOK; asof_checks PASS; projection_ready False |
| NYJ_LAC | 2026-11-22T14:24:13Z | Sun Nov 22 10:24 AM AST | Sun Nov 22 05:05 PM AST | VALID (pre-kickoff) | price_status PACKET_TWO_BOOK_NOT_FOUR_BOOK; asof_checks PASS; projection_ready False |
| NYJ_LAC | 2026-11-22T15:03:40Z | Sun Nov 22 11:03 AM AST | Sun Nov 22 05:05 PM AST | VALID (pre-kickoff) | price_status PACKET_TWO_BOOK_NOT_FOUR_BOOK; asof_checks PASS; projection_ready False |
| NYJ_LAC | 2026-11-22T20:33:23Z | Sun Nov 22 04:33 PM AST | Sun Nov 22 05:05 PM AST | VALID (pre-kickoff) | price_status OK; asof_checks PASS; projection_ready False |
| PIT_PHI | 2026-11-22T14:05:29Z | Sun Nov 22 10:05 AM AST | Sun Nov 22 02:00 PM AST | VALID (pre-kickoff) | LOCK kickoff_utc field says 2026-11-22T21:25Z but ESPN kickoff is 2026-11-22T18:00Z; metadata error only (locked_utc is before both); price_status PACKET_TWO_BOOK_NOT_FOUR_BOOK; asof_checks PASS; projection_ready False |
| PIT_PHI | 2026-11-22T15:46:13Z | Sun Nov 22 11:46 AM AST | Sun Nov 22 02:00 PM AST | VALID (pre-kickoff) | LOCK kickoff_utc field says 2026-11-22T21:25Z but ESPN kickoff is 2026-11-22T18:00Z; metadata error only (locked_utc is before both); price_status PACKET_TWO_BOOK_NOT_FOUR_BOOK; asof_checks PASS; projection_ready False |
| TB_DET | 2026-11-22T13:10:09Z | Sun Nov 22 09:10 AM AST | Sun Nov 22 02:00 PM AST | VALID (pre-kickoff) | price_status PACKET_TWO_BOOK_NOT_FOUR_BOOK; asof_checks PASS; projection_ready False |
| TB_DET | 2026-11-22T14:21:18Z | Sun Nov 22 10:21 AM AST | Sun Nov 22 02:00 PM AST | VALID (pre-kickoff) | price_status PACKET_TWO_BOOK_NOT_FOUR_BOOK; asof_checks PASS; projection_ready False |
| TEN_DAL | 2026-11-22T13:01:34Z | Sun Nov 22 09:01 AM AST | Sun Nov 22 02:00 PM AST | VALID (pre-kickoff) | price_status PACKET_TWO_BOOK_NOT_FOUR_BOOK; asof_checks PASS; projection_ready False |
| TEN_DAL | 2026-11-22T14:43:05Z | Sun Nov 22 10:43 AM AST | Sun Nov 22 02:00 PM AST | VALID (pre-kickoff) | price_status PACKET_TWO_BOOK_NOT_FOUR_BOOK; asof_checks PASS; projection_ready False |

## kickoff_utc metadata errors (not fixed in LOCK.json on purpose)

`evaluation/protocol.py` records the sha256 of each LOCK.json when it freezes the protocol, and `snapshots/score.py` reads LOCK.json. Editing the file would change its hash, so the correct kickoff is recorded next to the audit in `lock_kickoff_corrections.csv` instead. `snapshots/score.py` only uses the kickoff date to find the ESPN game, and both dates are right, so scoring is unaffected. `evaluation/protocol.py` compares locked_utc with the lock's own kickoff_utc; both locks pass that check with either kickoff.

| LOCK.json | kickoff_utc in lock | ESPN kickoff | locked_utc |
|---|---|---|---|
| snapshots/2026_11_JAX_NYG/20261122T132112Z/LOCK.json | 2026-11-22T18:00:00+00:00 | 2026-11-22T21:25+00:00 | 2026-11-22T13:21:12+00:00 |
| snapshots/2026_11_PIT_PHI/20261122T140529Z/LOCK.json | 2026-11-22T21:25:00+00:00 | 2026-11-22T18:00+00:00 | 2026-11-22T14:05:29+00:00 |
| snapshots/2026_11_PIT_PHI/20261122T154613Z/LOCK.json | 2026-11-22T21:25:00+00:00 | 2026-11-22T18:00+00:00 | 2026-11-22T15:46:13+00:00 |

## CIN@WAS (MNF, kickoff Mon Nov 23 09:15 PM AST = 2026-11-24T01:15Z)

Two valid pre-kickoff locks are on main: 20261122T134034Z and 20261122T162606Z (Sun Nov 22 09:40 AM and 12:26 PM AST). They were taken about 33-36 hours before kickoff, so they pre-date Monday's final injury reports and the inactive list (about 90 minutes before kickoff). Nothing on the box will make a fresher lock: no cron entry and no background process. Scheduled app routines can't be seen from the box. Whether to take another pre-kickoff lock today is Rico's call. If he wants one, it must be committed before 01:15Z.
