# Source access status

As of the 2026-11-06 public checkpoint. No credential is stored in this repository. A missing source stays missing. Do not invent ORCA, FTN, or Pinnacle quotes.

| Source | Status | Usable for projection now | Where to look |
| --- | --- | --- | --- |
| Pinnacle | `NOLINE` for actionable use. Saved research noted Q2–Q4 spreads absent. | No | NFL-45, NFL-7 |
| DraftKings | `NOLINE`. Odds-bridge is unauthenticated. | No | NFL-45, NFL-25 |
| FanDuel | `NOLINE`. Same connector limit. | No | NFL-45 |
| Other books | `NOLINE`. Full-book coverage is unverified. | No | NFL-25, NFL-45 |
| ORCA lines | `ACCESS_UNKNOWN`. Identity of the feed is unresolved. | No | [NFL-53](https://linear.app/nfl-database/issue/NFL-53/orca-lines-mirror-benchmark-accesslicense-unknown-until-retrieved), [NFL-54](https://linear.app/nfl-database/issue/NFL-54/unresolved-source-orca-lines-identityaccess-missing-book-adapters) |
| FTN NFL model mirror | `ACCESS_UNKNOWN`. | No | [NFL-55](https://linear.app/nfl-database/issue/NFL-55/ftn-nfl-models-mirror-benchmark-accesslicense-unknown-until-retrieved) |
| FTN charting / NGS coverage effects | Missing. Effects stay disabled. Charting parquet is hash-only. | No | NFL-47 |
| PFF | `NOT_READY_NO_DUPLICATE`. No second browser scrape from this package. | No | NFL-48 |
| nflverse play-by-play, rosters, games, depth charts | Public files that are already materialized are included, with the nflverse license. | Research inputs only | NFL-50, [SOURCES.md](../SOURCES.md) |
| ESPN injuries and depth for Phase 15 | `NOT_YET`. Raw ESPN response bodies are hash-only. | No | NFL-46 |
| NWS weather | Adapter is documented. A fresh pull needs the network and is not a certified freeze. | No | NFL-56, NFL-57 |
| odds-bridge | `needsAuth`. | No | NFL-25, NFL-45 |

The packaged registry copy is `docs/source_registry/SOURCE_REGISTRY.md`. This page is the public status to use when they differ: the corrected Linear index adds NFL-54, and raw quote bodies are not in the tree.

## Owner-supplied gamebook (ingested 2026-11-10)

| Source | Status | Usable for projection now | Where to look |
| --- | --- | --- | --- |
| Official NFL Game Summaries, 2026 Week 9, all 15 games (nflverse ids in `data/gamebooks/2026/wk09/MANIFEST.csv`) | Owner-supplied PDFs plus `pdftotext -layout` text. Tidy per-game CSVs and week-level `combined/` tables are a research extract. NFL media-use restriction applies. | No | `data/gamebooks/2026/wk09/` |

This row does not change `projection_ready`, model weights, formulas, or simulators. `manifest.json` is still the sqlite snapshot and was not rebuilt. The 2026-11-06 source-registry and source-run-gate manifests were not edited.
