# NFL-49 Pillar 1: quote feed for scoring (verification request for Ghost6, NFL-75)

**Owner decision (Rico, Nov 22, 2026, in session):** accept the free public game-line feed below as the quote feed for
scoring, in place of the authenticated feed the docs previously required.

**Requested of the reviewer:** verify the checks below; if they hold, check the NFL-75 box and change
`known_flags/KNOWN_LIMITATIONS.json` `"quotes"` from `"NOLINE"` with a `quotes_note` citing this file and the commit (same
process as `Phase15`). Nothing in this folder changes a flag; readiness P1 stays FAIL until the flag file is edited.

## The feed
| Piece | Where | What it does |
|---|---|---|
| Game lines, 6 books | `pregame/sportsbooks.py actionnetwork()` | Action Network public scoreboard JSON (no key): full-game spread, total, moneyline for DraftKings, FanDuel, BetMGM, Caesars (williamhill_us), BetRivers, bet365; its consensus and opening line kept reference-only |
| FanDuel, Pinnacle | `fanduel()`, `pinnacle()` | FanDuel's own feed (primary for FanDuel); Pinnacle guest feed as the reference (never counted) |
| Raw provenance | `pregame/direct_lines/raw/*.json.gz`, `latest.json` `fetch` | exact response bytes saved gzipped; URL, sha256, byte count and fetch time recorded |
| Freeze | `pregame/direct_books.py write_freeze` (schema `price-freeze/direct-2`) | multibook row format read by `snapshots/lock.py` and `evaluation/protocol.py`; `meta.books` = books with full-game lines; `meta.source_files` (sha256 of every source file); `meta.fetch_log` |
| Gate | `pipeline/hooks.py four_book_prices`, `REQUIRED_BOOKS` | counts only books with full-game lines (props never fill a book); required: FanDuel, DraftKings, BetMGM, Caesars |
| Merged | PR #93 (merge `1a4de36`) | |

## Checks (all reproducible)
1. **Feed works from GitHub runners:** run `NFL direct book lines` on main, then read `pregame/direct_lines/latest.json`:
   `books.actionnetwork.status == "OK"`. Observed Nov 22 12:39 UTC: 504 rows, response sha256 `6564b56b8411...`.
2. **Hash chain:** `git show origin/main:pregame/direct_lines/raw/actionnetwork_20261122T123952Z_6564b56b8411.json.gz | gunzip | sha256sum`
   starts with `6564b56b8411` (checked).
3. **A live freeze passes the gate and the locker:** `evidence.json` and `freeze/` in this folder, built from main's
   Nov 22 lines for TB@DET. Gate four-book check `OK` with fanduel, draftkings, betmgm, williamhill_us (+ betrivers, bet365);
   `snapshots.lock.market_lines` reads 8 spread, 9 total and 9 moneyline rows.
4. **Tests:** `pregame/tests/test_quote_feed.py` (`test_freeze_rows_are_in_the_locker_format`,
   `test_gate_counts_only_books_with_game_lines`) and `pipeline/tests/test_pipeline.py::test_four_book_freeze_*`.

## Known limits (stated, not hidden)
- The feeds are public website JSON, not a licensed API. A format change makes a book fail loudly (status FAILED in
  `latest.json`); nothing is filled in.
- No per-price update time is published; a book's as-of time is its pull time (`meta.as_of_note`).
- DraftKings and Caesars refuse direct requests (403); they come through Action Network only. No block is worked around.
- NFL-45 (market_calibration actionable quotes, `calibration_fitted_claim`) is a separate decision and is unchanged.
