# Week 11 kickoff notes (documentation only; no LOCK.json or frozen file edited) refs NFL-49
Pristine scoring uses ESPN's real kickoff (`SCORE.json final.kickoff_espn_utc`, snapshots/score.py + evaluation/protocol.py), not LOCK.json.
- JAX@NYG: LOCK.json kickoff_utc 2026-11-22T18:00Z is wrong; ESPN 2026-11-22T21:25Z. Lock 13:21:12Z is pre-kickoff either way.
- PIT@PHI: LOCK.json kickoff_utc 21:25Z; ESPN 18:00Z. Lock 15:46:13Z is pre-kickoff either way.
Scorer needed no override (it only uses LOCK kickoff for the ET date lookup, same date here).
Scored lock per game = last lock before real kickoff; earlier locks are DUPLICATE/NOT_FINAL by design.
- CIN@WAS (MNF): three locks; scored the last pre-kickoff one, 20261124T004416Z (locked 00:44:16Z, kickoff ESPN 2026-11-24T01:15Z). Earlier locks 20261122T134034Z / 162606Z are DUPLICATE by design. Final CIN 20, WAS 22 (nflverse). refs NFL-49
- IND@HOU never locked: skipped.
