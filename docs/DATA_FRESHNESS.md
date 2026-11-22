# How fresh each pregame input has to be (NFL-56)

The policy lives in code, `pipeline/freshness.py` (`POLICY`) and `pipeline/cadence.py`. This page mirrors them. If
they disagree, the code governs and this page is the bug. Tests check the main limits and each status path
(`pipeline/tests/test_pipeline.py`, `pipeline/tests/test_newest_release.py`).

**Age is measured from the source's as-of time, not from when we fetched it** (NFL-56, changed 2026-11-22).

**Newest-release rule** (Rico, 2026-11-22): a weekly or sporadic source is **FRESH** if this copy is still the
latest published asset (GitHub release digest match, or the asset has not been re-published since our pull) **and**
it covers every completed game. Missing coverage of a completed game is **GAP**, not STALE. A copy that has been
superseded by a newer asset is **STALE**. There is no flat 24-hour (or 12-hour) clock on those files.

- *Publisher-dated* inputs use the publisher's own stamp for the exact copy in the packet: `source_updated_at` on
  the record, or a stamp proven by `pipeline/source_asof.py`. For an nflverse release asset, a sha256 digest match
  with our copy, or "asset not re-published since our pull", proves the asset's `updated_at`. For NWS,
  `updateTime` counts only if the forecast was not regenerated after our pull (it still matches the live grid).
  If it can't be proven, the input is **MISSING (UNKNOWN_NO_SOURCE_TIMESTAMP)**: never fresh, never zero.
- *Live endpoints* (book prices, ESPN live injury list) serve the current state at request time and carry no
  feed-level stamp, so the pull time is the quote time. Every row labels this `live_pull`. The **schedule** also
  keeps a pull-time / as-of window (it updates every few minutes).
- A stamp later than our pull, or in the future, is rejected. A record with no pull time is MISSING.
- The CLI entry points (`pipeline.window`, `pipeline.phases`, `pipeline.sim100k`) resolve stamps over free public
  APIs (GitHub releases API, api.weather.gov). Library calls and tests stay offline. Every freshness row carries
  `as_of_utc`, `as_of_basis`, `as_of_evidence` and `cadence` next to `retrieved_utc`.

A source with a status other than OK counts as **MISSING**, never as fresh.
For live-window sources, limits tighten as kickoff approaches. The tightest window that applies wins.

| Input | Where it comes from | Cadence rule | Current when |
| --- | --- | --- | --- |
| Schedule (kickoff, site, listed QBs) | nflverse `games.parquet`, packet `sources.games` | live window | pull within 24 h (the schedule asset updates every few minutes; pull time is the quote time) |
| Play-by-play | nflverse, `sources.pbp` | latest release + completed games (`data_freshness` OK) | latest asset and every completed game is in it; missing a completed game is GAP |
| Rosters | nflverse weekly rosters | latest release | latest `roster_weekly_*.parquet` asset |
| Depth charts | nflverse | latest release | latest depth-charts asset (the former 12 h-inside-48 h clock is not used) |
| Snap counts | nflverse / PFR | latest release + completed games | latest snap_counts asset and every completed game is in it |
| FTN charting | nflverse (CC-BY-SA) | latest release + completed games | latest ftn_charting asset and every completed game is in it |
| PFR defenders | nflverse PFR advanced defense | latest release + completed games | latest weekly def asset and every completed game is in it |
| Official injury report | nflverse injuries | latest release | latest injuries asset (official reports are due 4:00 p.m. New York time on the filing days in the 2026-27 important dates) |
| News / live injuries | ESPN public injury list (the only news feed wired today) | live window | pull within 6 h; 2 h inside 6 h of kickoff; 45 min inside 2 h |
| Weather | National Weather Service hourly forecast (outdoor games only; indoor = NOT_REQUIRED) | NWS live grid | packet `updateTime` matches the live grid (or is the stamp on this copy and has not been superseded). No max-age clock. |
| Book prices in the packet | direct lines or Odds API | live window | pull within 6 h; 60 min inside 6 h of kickoff; 20 min inside 2 h |
| Four-book prices | newest `pregame/price_freezes/<ET date>_<AWAY>@<HOME>/freeze_*.json`; all required books in `pipeline/hooks.py` `REQUIRED_BOOKS` (default FanDuel, DraftKings, BetMGM, Bovada) must appear | live window | same windows as book prices, dated from the oldest required book's pull |
| Public NGS passing / receiving / rushing | nflverse `nextgen_stats/ngs_*.parquet` (public access only; no NFL Pro). Packet `sources.ngs_*`, or `pregame/.cache` if the packet has no OK record | latest release + completed games | latest ngs asset and every completed game/week-team is in it |
| NGS main-defender inputs | derived check `ngs_defender_matchup` | field inventory + coverage | lists available public columns vs wanted route / throw-location / success-vs-defense / likely-defender fields. Wanted fields that public NGS does not carry are **MISSING/unknown, never zero**. Missing completed-game coverage is GAP. |
| Official inactives | hook `official_inactives` (`phase15.official_inactives:hook`, club official Inactives articles) | T-90 | must be pulled **after** they post, about 90 min before kickoff; before T-90 the status is NOT_YET |

## What happens when data is stale, missing, or a coverage gap

- **Phase ledger** (`python -m pipeline.phases`): every phase that depends on the input is marked STALE, GAP,
  MISSING or NOT_YET, with the reason and the age. Nothing is skipped or filled in.
- **100k entry point** (`python -m pipeline.sim100k`): refuses, exits 2 and lists the blocking input (STALE, GAP,
  MISSING or NOT_YET). There is no override.
- **Scheduled refresh**: the pregame-packet workflow re-pulls on its schedule. The NFL-56 workflow (once installed, see `pipeline/workflow_to_install/`) then re-checks
  the ledger and commits it, so a stale input clears on the next pull without anyone stepping in. The four-book
  freeze is **not** pulled on a schedule, because a paid Odds API pull spends credits. Blitz or the owner can also
  freeze free direct lines (`pregame.direct_books`) with no Odds API credits.
- A stale, missing or gapped input is never replaced with zero, an older value or a guess.

## Known gaps

- There is no general news adapter (beat reports, coach quotes). The ESPN injury list is the only automated news
  input, and the analyst prompt still checks news by hand.
- Official inactives come from each club's official Inactives article, pulled after T-90. Phase 15 stays NOT_YET
  before T-90 and MISSING after if the official pull is incomplete.
- Weather covers US outdoor stadiums only. Neutral-site and international games come back NOT_MAPPED and so
  count as MISSING.
- Public NGS weekly files (passing, receiving, rushing) do not include route type, target location, QB pass-location
  splits, success-by-location vs a defense, or likely defenders. Those fields are listed MISSING/unknown and are
  not filled with zero. Coverage is week/team (the files have no `game_id`).

## Main-defender matchup fields (pipeline/matchup_sources.py, refs NFL-47, refs NFL-56)

The `ngs_defender_matchup` row now carries a `matchup_fields` block with a status per field:

| Field | Source | Status |
|---|---|---|
| target_location, qb_pass_location, qb_success_vs_defense | nflverse play-by-play (`pass_location` x `pass_length`, `success`, `epa`), weeks before the target week | FILLED only when the play_by_play row is FRESH; otherwise it carries that row's STALE/GAP/MISSING |
| receiver_routes, rb_routes | nflverse `pbp_participation_<season>` `route` (2026 file not published as of 2026-11-22), else a PFF capture `routes_run` column | MISSING until one exists |
| likely_defenders | PFF matchups tool capture (local, never committed: the repo is public and PFF is paid) | PFF_PROJECTED (candidate, unverified); VERIFIED only on rows with `assignment_evidence` |

QB-vs-defense is shown side by side (QB's own zone rate next to the defense's allowed rate); no blended number is made.
Nothing is estimated: unfilled fields are MISSING / "unknown", never zero. The row's own status (and so the 100k gate)
is still decided by the public NGS files, as before.
