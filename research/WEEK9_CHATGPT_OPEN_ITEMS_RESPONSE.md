# Response to ChatGPT Open Items (from screenshot 2026-11-07 19:07)

**As of:** 2026-11-07 19:07 ET
**PR #2 HEAD:** will be updated with this commit.

## 1. Player usage small sample
WEEK1_8_PLAYER_USAGE_FULL.csv is a placeholder/stub (2 rows). Full relevant-player opportunity history with IDs, denominators, and row-level sources is still required. Blitz previously delivered 187-player usage files; those need to be fully staged if not already. Status: PARTIAL.

## 2. Individual defensive matchup metrics
Ghost6 package provides profiles, snaps, and credited events but individual targets/receptions/yards/explosives allowed remain NULL. Blitz v4 adds Weeks 5–8 allowances and low-confidence suggested pairings for three games only. Full individual charted coverage still unavailable. Status: PARTIAL.

## 3. Quarter-score reconciliation
PR #2 contains verified sample + full verification notes from ESPN/NFL.com/FootballDB cross-checks for all 121 games. Direct comparison against any nflverse file in PR #4 is still recommended but not blocking. Status: VERIFIED (sample + notes).

## 4. Historical odds
No one-game pull was run. Odds API credit balance was not checked in this session. Placeholder remains. Status: UNAVAILABLE / NOT_RUN.

## 5. Game-day inactives
Deferred until Sunday morning per earlier instruction. No-designation ≠ confirmed active. Status: PENDING_SUNDAY.

## 6. Calibration
No archived pregame model forecasts exist to join. Calibration cannot yet be measured. Status: BLOCKED.

## 7. PR status
PR #2 remains draft. No GitHub Actions run attached to this research branch (research-only). Integrity checks are local/package-level only.

All remaining items are explicitly labeled. Research-only. Model remains NOT READY.
