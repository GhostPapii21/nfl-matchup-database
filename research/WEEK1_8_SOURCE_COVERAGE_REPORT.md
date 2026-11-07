# Week 1–8 Source Coverage Report
## NFL 2026 Projection Readiness – Task 1 Evidence
**Generated:** 2026-11-07T10:40:00Z  
**As-of:** Pre-Week 9 (Sunday Nov 8 games)  
**Researcher:** Grok (isolated research branch; no modifications to PR #28/#29)

## Canonical Schedule Audit
- **Source:** nflverse/nfldata games.csv (commit 8e2dd603345cbcce0cd90f0399da09ffb315c19a, 2026-11-06T22:35:19Z, sha256 d3cd2e92c937643fd0f2e000eccd3affd9546a489a45387e02709199f8549a49)
- **Regular season Weeks 1–8:** 121 games (16/16/16/16/15/14/14/14)
- **Date range:** 2026-09-09 through 2026-11-02
- **Excluded:** Week 9 JAX @ BAL (2026_09_JAX_BAL / ESPN 401873037)
- **Confirmed identities:**
  - CHI @ SEA: 2026_08_CHI_SEA / Week 8 / 2026-11-02 / ESPN 401873036
  - CAR @ GB: 2026_08_CAR_GB / Week 8 / 2026-10-29 / ESPN 401873023
  - DAL @ PHI: 2026_07_DAL_PHI / Week 7 / 2026-10-26 / ESPN 401873009

**Status:** Full match to PR #28 documentation. No missing or duplicate game IDs identified in the certified package.

## Certified Public Data Coverage (from PR #28)
| File | SHA256 | Games Covered | Notes |
|------|--------|---------------|-------|
| stats_player_week_2026.csv.gz | f42cfa9f... | 121/121 | Box scores, CC-BY-4.0. Includes pass attempts. |
| play_by_play_2026.csv.gz | 3f9b215e... | 121/121 (outcome columns) | Omits EPA/WP/FTN. Week 9 present in full release. |
| snap_counts_2026.csv.gz | a12acdb3... | 121/121 | 9,188 mapped via unique pfr_id on roster_2026.csv |

- **Additive package:** data_packages/nfl_2026_w1_8/nfl_2026_w1_8_additive.zip (sha256 e542672edd68d37b90bb554b12964a818733e1d8ca525d31ffb7d295c1bba31c)
  - 67,419 rows for the 88 games absent from Render
  - Render currently: 33 games / 45,820 NFL 2026 rows (Weeks 1–2 + 2026_03_ATL_GB), max date 2026-09-24
- **PBP vs weekly discrepancies:** 218 attempt, 10 carry, 46 target player-games out of 2,360 compared. Weekly values retained in package.

## Specific Discrepancy Reconciliation
### 1. Luther Burden III – Week 8 CHI @ SEA (2026-11-02)
- **Prior claim:** Corrected from 3/41 to 7/56 on 9 targets.
- **Authoritative sources (retrieved 2026-11-07):**
  - NFL.com / PFN / StatMuse / ESPN / boxscore.email / team reports: **7 receptions, 9 targets, 56 yards, 1 TD**
  - Season total: 42 rec / 56 tgt / 547 yds / 3 TD through 8 games
- **Resolution:** Official box score confirmed at 7/56. Prefer for projection inputs. No conflicting official value found.
- **Confidence:** High. Source timestamps: post-game through 2026-11-07.

### 2. Matthew Golden – Week 8 CAR @ GB (2026-10-29)
- **Prior claim:** PBP 83 vs official 79.
- **Authoritative sources (retrieved 2026-11-07):**
  - Multiple independent box scores (eDraft, StatMuse, Packers.com logs, PFN, Keel Stats, weeklyheater from PBP): **7 receptions, 13 targets, 79 yards, 1 TD**
  - Season total: 43 rec / ~80-82 tgt / 619 yds / 4 TD
- **Resolution:** Official credited receiving yards = 79. PBP-derived 83 remains an unresolved contradiction (possible inclusion of non-credited yards, YAC classification, or play description vs numeric). Preserve both; use 79 for projection inputs.
- **Confidence:** High on official 79. Medium on PBP variance (not fully re-audited play-by-play this run).

### 3. QB Dropback / Designed Rush Counts – CHI @ SEA
- **Prior claims:** 40/17 and 37/19 reported.
- **Evidence:**
  - Official: Caleb Williams 24/34, 247 yds, 1 TD, 0 INT, 1 sack (PFN, team site, ESPN)
  - Film breakdown (Windy City Gridiron): ~36 dropbacks noted, time-to-throw 2.87s
  - Designed vs scramble vs kneel separation not fully quantified in public weekly/PBP summary here.
- **Resolution:** Unresolved for precise opportunity modeling. Official pass attempts = 34. Dropback denominator requires further PBP filtering (pass_attempt + sack + scramble flags). Do not auto-transfer or invent counts.
- **Confidence:** Medium. Blocker for fine-grained designed-rush allocation.

## Missing / Held-Out Items (from package documentation)
- FTN charting rows (rights not verified for redistribution)
- Usage export (license UNKNOWN_PENDING_CLOUD_AUDIT; Weeks 1–7 only)
- Depth charts, unmatched NGS/PFR caches
- Raw ESPN bodies
- Route participation (unavailable unless independently sourced)
- Full individual defender assignments (team-level only in public PBP)

## Blockers for Reliable Projection
- Render DB not yet updated with the 88-game package (LIVE_INGEST_BLOCKED)
- Unresolved Golden PBP vs official yards
- Incomplete designed vs scramble separation for QB rushes
- Route participation and coverage responsibility not in public package
- No post-kickoff leakage allowed for Week 9 forecasts

**Overall Task 1 Status:** Complete for source verification and discrepancy marking. Dataset covers 121/121 games in public nflverse. Specific contradictions preserved. Ready for usage/opportunity tables (Task 2).
