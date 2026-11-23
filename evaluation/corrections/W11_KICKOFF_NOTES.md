# Week 11 kickoff notes (documentation only; no LOCK.json or frozen file edited) refs NFL-49
Pristine scoring uses ESPN's real kickoff (`SCORE.json final.kickoff_espn_utc`, snapshots/score.py + evaluation/protocol.py), not LOCK.json.
- JAX@NYG: LOCK.json kickoff_utc 2026-11-22T18:00Z is wrong; ESPN 2026-11-22T21:25Z. Lock 13:21:12Z is pre-kickoff either way.
- PIT@PHI: LOCK.json kickoff_utc 21:25Z; ESPN 18:00Z. Lock 15:46:13Z is pre-kickoff either way.
Scorer needed no override (it only uses LOCK kickoff for the ET date lookup, same date here).
Scored lock per game = last lock before real kickoff; earlier locks are DUPLICATE/NOT_FINAL by design.
