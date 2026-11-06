# Diagnostic identity handoff

Use player_aliases_certified_v2.json and game_aliases_certified_v2.json for this diagnostic packet. The staged v1 documents remain unchanged.

All 192 JAX/BAL player rows and supplied aliases were compared with the hash-verified saved nflverse roster. Matching uses exact ESPN athlete ID plus team; names, jersey numbers and position labels never create joins. Ambiguous matches remain unmatched. Roster status is saved context, not a current active/depth/workload assertion.

The four ESPN files contain 275 athlete observations across 161 distinct team/ESPN IDs. There are 203 matched observations and 72 unmatched observations, including repeated observations across files. The full matched and unmatched lists retain the source file. The original scan recursively visited nested objects and incorrectly treated colleges/positions as player candidates; the revised parser reads only athletes.items and entries.playerId. It does not hide or guess the remaining missing mappings.

ESPN event 401873037, balldontlie game 1392337 and the open-leagues nflverse alias 2026_09_JAX_BAL agree on diagnostic matchup, week 9 and kickoff 01:15Z. This is not a verified frozen schedule/PBP registry join. Canonical game ID remains null. The saved odds alias c75744790b7acf6260c78ba5e739c0e5 remains unmatched: its close kickoff says 01:20Z and some local metadata says week 10. Source values and the ambiguous open-leagues spread perspective remain explicit.

Identity source publication/pull eligibility at the historical cutoff is unverified. Both finalized documents are DIAGNOSTIC_IDENTITY and unusable for frozen pregame forecasts. No named-player projection or executable quote join is approved.
