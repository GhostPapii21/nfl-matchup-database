# Pregame packets

Automatic research files for every Thursday, Sunday and Monday game. Research only: `projection_ready`
stays false, nothing is priced or recommended, and nothing here has been validated against the market.

## What happens automatically

`.github/workflows/nfl-pregame-packets.yml` runs on a schedule (Tuesday morning for the new week, then again
before each Thursday, Sunday and Monday kickoff window). Each run:

1. Reads the NFL schedule and finds the upcoming games.
2. Downloads current public data: play-by-play, weekly rosters, official injury reports, depth charts, snap
   counts, FTN charting (blitz, play-action), Pro Football Reference defender stats (all via nflverse), and
   the ESPN live injury list when it can be reached, the National Weather Service kickoff forecast for outdoor
   games, and (when the `ODDS_API_KEY` secret is set) Pinnacle, DraftKings and FanDuel prices.
3. Builds one packet per game and commits it under `pregame/packets/<game_id>/`:
   - `brief.md`: readable breakdown.
   - `packet.json`: the same data for tools.
4. Rewrites `pregame/packets/INDEX.md` and `latest.json` to point at the current slate.

Scheduled runs only fire once this workflow is on the default branch. It can also be started by hand from
the Actions tab ("Run workflow"), with an optional week number.

## What is in a packet

For each team, over its last eight games:

- **Defense, what it allows:** points; passing and rushing yards; yards per carry; receptions and yards to wide
  receivers, tight ends and running backs; explosive passes (20+) and runs (15+); sack, pressure and blitz
  rates; third-down and red-zone rates; all with league rank, plus a game-by-game table, the best receiving
  and rushing line allowed in each game, run defense by direction, per-defender coverage numbers and pass-rush
  leaders.
- **Offense, what it does:** the same measures produced; quarterback line and game log; every receiver's
  targets, target share, air-yards share, depth of target and red-zone looks; every rusher's carries and share;
  run game by direction; snap shares.
- **People:** depth-chart lines, official injury report with starters marked, ESPN live injuries, players who
  arrived from or left for another team in the last four weeks.
- **Weather:** kickoff temperature, wind and precipitation chance, with flags for wind 15+, precipitation 50%+
  and freezing.
- **Book prices and no-vig:** spread, total and moneyline at Pinnacle, DraftKings and FanDuel, each with its
  no-vig probability and hold, the best retail price per side with its break-even, and the line's movement
  since the first snapshot. Player props (passing, rushing and receiving yards, receptions, carries) are pulled
  for games inside 36 hours of kickoff and shown beside the research baseline.
- **Formation and pass-zone splits:** each offense by formation and by pass zone (short or deep, left / middle /
  right), and what each defense allows in the same cells. NFL Savant's season download was checked and is the
  same nflverse play-by-play, so no second download is made.
- **Keyed connectors:** which API keys the run could see and whether each one answered. Names and statuses
  only; never a key.
- **Rain-adjusted passing:** for outdoor games, each team's passing line and every receiver's targets, receptions and
  yards for dry, rain and the forecast, from measured rain and wind effects (`research/weather/README.md`).
- **Matchup edges:** where a top-10 unit meets a bottom-10 unit.
- **Projections (research only):** period-engine team scores from two samplers, and per-player baselines with
  the Floor / MAIN / Median percentile labels from `workflows/operational_specs/PHASE_SCRIPT.md`.
- **Phase ledger:** the 15 phases, each marked AUTO, PARTIAL, BLOCKED or PENDING with what is missing.

## Using it with ChatGPT or Grok

1. Connect this repository through the tool's GitHub connector.
2. Paste `pregame/ANALYST_PROMPT.md` as the first message (or save it as the project's instructions).
3. Say "run Monday night", "run the slate", or name a game.

The prompt makes the model pull the packet, walk the 15 phases, write the breakdown, brainstorm angles, then
attack each angle in a critical review before giving projections with a confidence label.

The chat tools do not start on their own: GitHub refreshes the files on schedule, and the model reads them when
asked. To have the analysis arrive without asking, create a scheduled task inside the chat tool itself
(ChatGPT "Tasks", Grok "Tasks") with the instruction "Follow pregame/ANALYST_PROMPT.md for today's games in
GhostPapii21/nfl-matchup-database", timed shortly after the workflow's run times.

## One-time setup

1. Merge this into the default branch so the schedule runs.
2. For book prices: Settings, Secrets and variables, Actions, add `ODDS_API_KEY` (the-odds-api.com). Without it
   the packets still build and say "no book prices". Rough credit use: about 6 credits per run for main lines,
   plus about 5 per game for props inside 36 hours of kickoff (`--props-within-hours 0` turns props off).
   Optional: `NFL_BDL_API_KEY` (BallDontLie; used to double-check the slate) and `NFL_API_SPORTS_KEY` (access
   check only). Keys connected inside ChatGPT or Grok are not visible to GitHub: they must be saved here as
   repository secrets. Each packet's "Keyed connectors in this run" table shows what the run could see.
3. Connect the repository to ChatGPT or Grok and save `ANALYST_PROMPT.md` as the instructions.

## What the packet cannot do

- Final inactives (about 90 minutes before kickoff) are not fetched. The prompt tells the model to check live.
- Weather covers outdoor games at US home stadiums only; neutral-site and international games are marked
  NOT_MAPPED.
- Line movement starts at the first snapshot this pipeline took, not the true opening line.
- PFF and the FTN betting model sit behind logins and are not pulled. The prompt uses them only when the owner
  pastes them into the chat.
- No man/zone coverage, coverage shells, route participation or line grades: no free source carries them.
- "Pressure rate" is sacks plus quarterback hits, a floor on true pressure.
- Player baselines use only games in which the player had a target or carry, and do not adjust for injuries,
  role changes or game script. That is the analyst's job.

## Run it yourself

    pip install -r requirements-test.txt
    python3 -m pregame.build_packets                     # next Thursday/Sunday/Monday slate
    python3 -m pregame.build_packets --game 2026_10_LAC_BAL
    python3 -m pregame.build_packets --week 11 --weekdays all
    python3 -m pytest pregame/tests -q

## Sources

nflverse (github.com/nflverse/nflverse-data): play-by-play, schedules, rosters, injuries, depth charts, snap
counts, PFR advanced defense. FTN charting via nflverse is FTN Data, CC-BY-SA 4.0, and must be attributed when
reused. ESPN public injury feed. Each packet lists the files used with retrieval time and SHA-256. Third-party
data keep their own terms; see `SOURCES.md`.
