# How fresh each pregame input has to be (NFL-56)

The policy lives in code, `pipeline/freshness.py` (`POLICY`), and this page mirrors it. If they disagree, the code
governs and this page is the bug. A test checks the main limits (`pipeline/tests/test_pipeline.py`).

Age is measured from the source's own `retrieved_utc` stamp, the time this repository pulled it, against the
check time. A source with no stamp, or with a status other than OK, counts as **MISSING**, never as fresh.
Limits tighten as kickoff approaches. The tightest window that applies wins.

| Input | Where it comes from | Max age | Tighter near kickoff |
| --- | --- | --- | --- |
| Schedule (kickoff, site, listed QBs) | nflverse `games.parquet`, packet `sources.games` | 24 h | none |
| Play-by-play | nflverse, `sources.pbp` | 24 h, **and** every completed game must be in it (`data_freshness` OK) | none |
| Rosters | nflverse weekly rosters | 24 h | none |
| Depth charts | nflverse | 24 h | 12 h inside 48 h |
| Snap counts | nflverse | 24 h | none |
| FTN charting | nflverse (CC-BY-SA) | 24 h | none |
| PFR defenders | nflverse PFR advanced defense | 24 h | none |
| Official injury report | nflverse injuries | 12 h | 6 h inside 48 h |
| News / live injuries | ESPN public injury list (the only news feed wired today) | 6 h | 2 h inside 6 h; 45 min inside 2 h |
| Weather | National Weather Service hourly forecast (outdoor games only; indoor = NOT_REQUIRED) | 6 h | 3 h inside 12 h; 90 min inside 3 h |
| Book prices in the packet | Odds API via the existing packet builder | 6 h | 60 min inside 6 h; 20 min inside 2 h |
| Four-book prices (FanDuel, DraftKings, Hard Rock, Caesars) | newest `pregame/price_freezes/<ET date>_<AWAY>@<HOME>/freeze_*.json` from Blitz's `python -m pregame.multibook`, using `meta.pulled_utc`; all four books must appear | same as book prices | same as book prices |
| Official inactives | none wired yet (hook `official_inactives` in `pipeline/hooks.py`) | must be pulled **after** they post, about 90 min before kickoff | before T-90 the status is NOT_YET |

## What happens when data is stale or missing

- **Phase ledger** (`python -m pipeline.phases`): every phase that depends on the input is marked STALE, MISSING
  or NOT_YET, with the reason and the age. Nothing is skipped or filled in.
- **100k entry point** (`python -m pipeline.sim100k`): refuses, exits 2 and lists the stale input. There is no
  override.
- **Scheduled refresh**: the pregame-packet workflow re-pulls on its schedule. The NFL-56 workflow (once installed, see `pipeline/workflow_to_install/`) then re-checks
  the ledger and commits it, so a stale input clears on the next pull without anyone stepping in. The four-book
  freeze is **not** pulled on a schedule, because each pull spends paid Odds API credits (about 5 per game). Blitz
  or the owner runs it, and until then the four-book row stays MISSING or STALE.
- A stale or missing input is never replaced with zero, an older value or a guess.

## Known gaps

- There is no general news adapter (beat reports, coach quotes). The ESPN injury list is the only automated news
  input, and the analyst prompt still checks news by hand.
- Official inactives have no source in this repository. Phase 15 stays NOT_YET before T-90 and MISSING after.
- Weather covers US outdoor stadiums only. Neutral-site and international games come back NOT_MAPPED and so
  count as MISSING.
