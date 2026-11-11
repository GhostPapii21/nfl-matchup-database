# Period ledger definitions

Scope is regular-season 2026, weeks 1 through 8 inclusive. A completed schedule row has finite, nonnegative integer home and away scores and a game date no later than the requested as-of date in America/New_York. Schedule scores are the completion authority; PBP must independently reconcile to them before period scores are published. Rows from week 9, including JAX@BAL, never enter the ledger. No expected count is hard-coded: 121 is only the task estimate until the actual schedule is fetched.

## Source and retained evidence

Acquisition uses `nflreadpy.load_schedules(2026)` and `nflreadpy.load_pbp(2026)`. Free public nflverse release URLs are recorded in `data/raw/manifest.json`. Each successful snapshot records its SHA-256, row count, library version, and pull time. Schedule snapshots retain all original columns for W1–8 regular-season rows, including available quote fields. PBP snapshots retain the W1–8 identity, ordering, cumulative-score, and boundary-marker columns needed by this builder. No premium services, authentication, access bypass, production tools, or outside-workspace notes are used.

The `source=nflverse_pbp+schedules` field identifies the intended reconstruction pipeline. Per-game `scoreboard_status`, `pbp_source`, and `source_identity_status` distinguish successful reconstruction from missing evidence. A source URL alone does not establish successful acquisition: consult the manifest and build status. `pull_utc` is the acquisition-run start time, never an odds quote timestamp. Each feed also has its own attempt time in the manifest. An offline replay retains the original pull time.

Official references:

- [nflreadpy loader API](https://nflreadpy.nflverse.com/api/load_functions/)
- [nflverse PBP dictionary](https://raw.githubusercontent.com/nflverse/nflreadr/main/data-raw/dictionary_pbp.csv)
- [nflverse schedule dictionary](https://raw.githubusercontent.com/nflverse/nflreadr/main/data-raw/dictionary_schedules.csv)

## Quarter reconstruction and missingness

Within each game, sort by numeric `play_id`; use `qtr` to group regulation quarters 1–4. Conflicting duplicate play IDs, identity mismatches, decreasing cumulative scores or quarters, missing quarter endpoints, and schedule/PBP final-score disagreement invalidate period reconstruction. Identical duplicate boundary records are harmless. Administrative rows with unusable quarter, play ID, or scores are excluded; if this removes a required endpoint, reconstruction remains missing.

`total_home_score` and `total_away_score` are read on the terminal administrative row of each quarter. The nflverse dictionary describes these as start-of-play scores. At an end-of-quarter or end-of-game administrative row they include all preceding scoring plays in that quarter. The builder does **not** treat a scoring play's starting score as its ending score. It requires a terminal `quarter_end` flag or an explicit END QUARTER/HALF/GAME description. For the final game endpoint it requires an END GAME/OVERTIME description (or an explicit `game_end` flag if that column exists). The PBP dictionary does not promise a `game_end` column, so descriptions are retained. A terminal scoring play without a scored administrative endpoint is insufficient and is marked MISSING.

Let C(q) be that quarter endpoint and C(0)=(0,0). Quarter points are C(q)−C(q−1), separately for each team. All rows in the quarter remain in play order, so touchdowns, subsequent PATs and two-point attempts, defensive scores and safeties are reflected through the scoreboard; touchdown counts are never used as a score substitute. Quarters scoring zero have explicit zeroes only when endpoint evidence supports them. The final scored PBP endpoint must equal both schedule final scores. Incomplete or inconsistent PBP leaves **all eight period panels MISSING** for that game; schedule final scores, game winner and tie remain available. This deliberately avoids partial panels whose internal boundaries cannot be verified.

## Halves, regulation and overtime

- H1 = Q1+Q2.
- H2 = Q3+Q4. **OT is excluded from H2.**
- REG = Q1+Q2+Q3+Q4.
- OT = all periods with `qtr > 4`, combined; measured as final score minus REG. It includes every OT if the source has multiple OT periods.
- Final = H1+H2+OT = REG+OT, separately for each team.

Every completed game has eight period rows. Verified games without OT have an explicit OT (0,0) row. OT flags use the schedule's binary `overtime` value, supplemented by observed `qtr > 4`. A schedule false flag conflicting with OT PBP makes reconstruction missing. Schedule true without OT PBP also makes it missing. When neither the schedule nor complete PBP establishes OT status, the flag is blank and `ot_status=MISSING`. OT is never inferred solely from a close score or a tie.

`cumulative_home/away` are scores through the end of the represented interval: Q1–Q4 through that quarter, H1 through Q2, H2/REG through Q4, OT through the final game endpoint. Thus H2 cumulative includes H1, while H2 points do not. Period rows overlap: do **not** add Q1–Q4, halves and REG together. `period_winner` is the team abbreviation with more points in the interval, `TIE` for equal points, or blank when missing. Overall `winner` and `tie` use schedule final scores including OT. Period winners are scoreboard outcomes, never betting covers. `kickoff` is the schedule's Eastern gametime with its date-specific UTC offset; blank if unavailable.

## Market grading

Retained, finite numeric schedule `spread_line` is required to grade spread, and retained, finite positive `total_line` is required to grade total. Each market qualifies independently. Moneylines or spread prices alone cannot establish the spread; final scores alone cannot establish any line. No quote is carried across games or inferred from PBP. If the required quote is absent, malformed or unretained, that market is **NOLINE**, with blank grading result. No period spread or total grades are produced.

The schedule's spread convention represents the expected home margin. Home spread grade compares `(home_score − away_score) − spread_line`: positive COVER, zero PUSH, negative NO_COVER. Total compares final combined points to total_line: OVER, PUSH, UNDER. Both use final scores including OT. Available moneylines, spread prices, total prices and line fields are preserved in the ledger and original schedule snapshot; they are not fabricated when absent.

**nflverse schedule lines are retained historic values, NOT verified closers.** Their original quote time and sportsbook are unverified. `quote_timestamp` is blank, `quote_verified_closer=False`, and the limitation is repeated in each ledger row. `GRADED` means a result against the retained quote only; it does not certify market-close provenance. A parquet checksum proves what this run retained, not when the market quote was originally observed.

## PFF and run state

No W1–8 public PFF scrape exists in this workspace at initialization. This builder performs no optional PFF crawl, so every built game has `pff_overview=MISSING`, blank `pff_source`, and `pff_attempt_status=NOT_ATTEMPTED`. Schedule PFF IDs do not count as overview evidence. AI/PFF Key Takeaways are out of scope. The outside-workspace W9 note is not imported.

Booleans serialize as True/False; blank numeric/boolean/result fields mean missing, not zero or false. `data/build_status.json` and `reviews/COUNTS.md` are authoritative about run completeness. If schedule acquisition fails, CSVs have headers only and expected games/panels/teams remain UNKNOWN. Header-only CSVs and synthetic unit fixtures never establish actual coverage. Builder exit code 2 and a failing real-source completeness test expose the blocked/incomplete state; exit code 0 requires fetched sources, at least one completed game and complete period reconstruction for every built game.
