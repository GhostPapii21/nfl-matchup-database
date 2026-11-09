# NFL Sunday, Nov 8, 2026: final research rescan and matched shadow backtest

**Completed Nov 9, 2026**. This is a READ-ONLY audit and retrospective experimental scorecard. **Not a production model upgrade or guaranteed betting edge.** NFL only; no NBA files or models changed.

## Scope and source verifications

- All **13 Sunday games** reconciled to the **live public ESPN final scoreboard** and archived NFL gamebook-reconciled Sunday results. Cleveland-New Orleans is the one overtime game; player statistics for evaluation are **regulation only**.
- Archived research ledger contains **1,599** model/line grade rows and **1,315** player-stat rows, not 1,599 unique player prop bets. Gamebooks, period scoring and regulation/OT boundary were verified by the [original Sunday final rollup](../research/WEEK9_SUNDAY_POSTGAME_ROLLUP_20261108.md).
- [Completed source integrity report](WEEK9_20261108_RESCAN_20261109.json) verified six frozen prospective artifacts and 13 ESPN results. There is no new sportsbook line implied by this audit.
- [Credential-access probe](NFL_LIVE_CONNECTOR_STATUS_20261109.json): BALLDONTLIE NFL and API-SPORTS NFL keys are **not configured** in the isolated Actions environment. Those provider calls were **not successfully ingested**. Cloudbet remains disabled/unvalidated.
- [SportsDataverse public-source parity](NFL_SPORTSDATAVERSE_SOURCE_STATUS_20261109.json): actual 2026 weekly source contains **274 Week 9 records** with 254 uniquely mapped Sunday player/game records spanning **all 13 Sunday games**. Its stable stats schema has no game_id, so game identity is reconstructed only from an unambiguous verified Week 9 team/opponent pair. **840 archived player-market final values match**, **31 are missing/unmatched**, and **two values disagree by 1 yard**. The provider remains quarantined from automated model ingestion until reconciled; no fallback zeros or invented pregame source timestamps.
- Existing archived ESPN/gamebook final data is ingested in research and available for scoring. This does **not** mean that all paid or third-party connectors are active or that a production database was updated.

### Two exact one-yard source conflicts

| Game | Player / market | Archived gamebook/ESPN final | SportsDataverse/nflverse weekly |
|---|---|---:|---:|
| LAR@WAS | Jayden Daniels passing yards | **274** | 273 |
| LAR@WAS | Chig Okonkwo receiving yards | **57** | 56 |

Independent public [CBS box](https://www.cbssports.com/nfl/gametracker/boxscore/NFL_20261108_LAR%40WAS/) and [Football Database box](https://www.footballdb.com/games/boxscore/los-angeles-rams-vs-washington-commanders-2026110804) agree with the archived 274 and 57. These may represent a provider stat-revision lag. Preserve both source values and the discrepancy: do not silently overwrite either. `source_verified_for_research=false` and `result_eligible_for_automated_model_ingest=false` until an explicit dated reconciliation.

## True side-by-side evaluation: Lightning opportunity counts, NOT yards

The Lightning neural model trained on earlier 2024-2026 game opportunities, with 2026 Week 8 used for validation. Week 9 results were held out as labels, but the experiment was evaluated **after the games** and participant selection is retrospective, not a perfectly blind prospective forecast.

| Opportunity | Week 9 player test rows | Lightning MAE | Rolling 5-game MAE | Lightning RMSE | Rolling RMSE |
|---|---:|---:|---:|---:|---:|
| player_rush_attempts | 79 | 2.616 | 2.756 | 3.961 | 4.127 |
| receiver_targets | 164 | 1.599 | 1.670 | 2.222 | 2.264 |

**Data availability:** 243 matched opportunity labels, all 13 games, but 18 ambiguous or missing pregame player identity, 47 insufficient player prior games, 8 source not gamebook verified were not eligible. Only observed participants with traceable IDs are included. No active-roster coverage rate can be inferred.

## Like-for-like prop comparison: same DK player, market, threshold, regulation outcome

This additional comparison uses archived book lines and each model's **point-mean direction relative to the line**, not the original forecast model's often contradictory raw `p_over` versus `p_under` decision. For the Lightning column, an intentionally simple **pre-Week-9 five-game historical efficiency ratio** converts neural **targets → receiving yards/receptions** and **rushing attempts → rushing yards**. It is a *separate deterministic bridge*, **not a learned neural yardage distribution**. No Lightning QB passing-yard projection exists yet.

Total **248 matching DraftKings prop instances across 13 games**: main mean direction **134/248 (54.0%)**, Lightning bridge **131/248 (52.8%)**. Neither is ROI or calibrated expected value.

| Matched market | Props | Main mean MAE | Lightning bridge MAE | Main correct | Lightning correct |
|---|---:|---:|---:|---:|---:|
| rushing_yards | 45 | 16.52 | 17.49 | 22 | 23 |
| receiving_yards | 113 | 21.57 | 22.19 | 61 | 58 |
| receptions | 90 | 1.53 | 1.56 | 51 | 50 |

**MAE units:** yard markets = yards; receptions = catches. Don't average mixed units into one model-accuracy number.

### All 13 Sunday games, identical matched pregame props

| Game | Props matched | Main correct | Lightning bridge correct |
|---|---:|---:|---:|
| ARI@SEA | 7 | 4 | 4 |
| CIN@ATL | 23 | 8 | 14 |
| CLE@NO | 26 | 16 | 15 |
| DAL@IND | 29 | 15 | 14 |
| DEN@CAR | 33 | 16 | 17 |
| DET@MIA | 23 | 8 | 6 |
| GB@NE | 6 | 4 | 4 |
| HOU@LAC | 8 | 4 | 5 |
| LAR@WAS | 28 | 14 | 12 |
| LV@SF | 8 | 6 | 5 |
| NYG@PHI | 20 | 13 | 14 |
| NYJ@KC | 26 | 17 | 12 |
| TB@CHI | 11 | 9 | 9 |

### Selected key opportunity/yardage mismatches

| Player | Game | Archived DK line | Main mean | Lightning bridge mean | Actual regulation |
|---|---|---:|---:|---:|---:|
| CeeDee Lamb | DAL@IND | 93.5 | 88.5 | 72.1 | 195 |
| Amon-Ra St. Brown | DET@MIA | 79.5 | 81.6 | 62.6 | 86 |
| Puka Nacua | LAR@WAS | 93.5 | 94.2 | 76.6 | 150 |
| Ja'Marr Chase | CIN@ATL | 76.5 | 69.8 | 54.2 | 155 |
| Tee Higgins | CIN@ATL | 76.5 | 103.8 | 85.3 | 32 |
| Jaxon Smith-Njigba | ARI@SEA | 93.5 | 118.7 | 100.9 | 51 |

The strong variation between player target volume, catch efficiency and explosive yards remains the primary research gap. There is no verified full-game named-defender assignment or post-snap man/zone + pressure chart in these forecasts. Ordinary PBP tacklers are NOT automatically coverage responsibility.

**Original pregame probability-call grade is different:** the Madrid+1 p.m. frozen season empirical model was 119/248 (48.0%) on DraftKings using its **larger stated probability** for over/under. The mean-direction matched comparison above is a new, equal-population scoring rule. Neither may be sold as a validated betting edge.

## Full safety and code-run rescan

[Current fail-closed NFL forecast gate](NFL_WEEK9_FORECAST_RELEASE_GATE_20261109.json) deliberately denies production promotion:

- **1299/1299** 1 p.m. simulation rows already identified as not bet-gradeable;
- **48** model/book forecast rows with fewer than 3 prior player games;
- **101** raw probability values at exact 0% or 100%;
- **825** records where the diagnostic calibration correction was not applied;
- **6/6** archived Shedeur Sanders passing-yard projections near 1 yard despite a market threshold near 191.5.

The 1-yard output is a concrete model-data problem and should trigger `NO_PROJECTION/ABSTAIN`, not a betting recommendation. The original frozen files are preserved unchanged for reproducibility.

**Relevant new checks passed**: NFL-only provider boundary tests, ESPN 13-game source rescan, Lightning 2024-26 experiment, Week 9 Lightning shadow evaluation, matched prop comparison, and fail-closed forecast gate. This does **not** imply all historical GitHub Actions passed. Prior main-repository builds include older failed package-import and board-artifact-upload jobs, and some current experiment workflow runs show `action_required`. Those require separate infrastructure/permission triage.

### Release decision

**HOLD / RESEARCH ONLY.** No model weights, production baseline, sportsbook integrations or source databases were changed. Do not merge experimental predictions into production. To qualify for promotion: securely configure provider keys and licensed feeds, inspect source availability by real historical timestamps, complete accurate routes/snap/coverage and quarterback-designed-versus-scramble labels, reject zero-stat inactive samples, obtain multiple truly prospective future slates, run same-market evaluation and probability calibration/ROI net of vig.

## Supporting experiment files

- [Lightning Sunday opportunity holdout](https://github.com/GhostPapii21/sportsbook-odds-bridge/blob/experiment/nfl-lightning-opportunity-v1/outputs/nfl_lightning_research/week9_shadow_scores.json)
- [Full row-by-row matched 248-prop comparison](https://github.com/GhostPapii21/sportsbook-odds-bridge/blob/experiment/nfl-lightning-opportunity-v1/outputs/nfl_lightning_research/week9_main_vs_lightning_matched_props.json)
- [Main original frozen Sunday projection and lines](WEEK9_SUNDAY_FINAL_FORECAST_GRADES_20261108.csv)

