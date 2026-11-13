# Game board

One page per slate: click a game and everything for it is there. It is rebuilt automatically after every pregame
packet refresh (Tuesday, Thursday, Saturday, Sunday and Monday; see `.github/workflows/nfl-pregame-packets.yml`).

## What a game shows

| Tab | What is on it | Source |
| --- | --- | --- |
| Overview | Rank edges both ways, pass-catcher roles, defenders to attack, QB against the blitz, injuries that matter, last meeting | all below |
| What the defense allows | Per game to WRs, TEs and RBs (targets, receptions, yards, TDs, explosives), passing, situational; each against what the offense gets and the league average, with ranks and an 8-game trend; who hurt this defense each week; run direction; pass zones | nflverse play-by-play |
| Defenders | Every coverage defender with position, targets, completions, yards, yards per target, TDs, INTs, missed tackles and a target / avoid grade; pass rushers; last season's man/zone mix and coverage shells | Pro Football Reference, NGS participation (last season) |
| Quarterback | Against the blitz and without it, play action, out of the pocket, pressure rate, red zone, third down; last season against man and zone, under pressure and clean | FTN charting, PFR, NGS participation |
| Receivers & backs | Target and carry share, per-game volume, depth, red-zone looks, snaps, game-by-game trend, baseline median, forecast-adjusted yards; role tags | nflverse, PFR snap counts |
| Injuries | Official report and ESPN, snap share, starter slot and next man up; players back from a missed game and whether they are still working back in; roster moves | nflverse, ESPN, snap counts |
| Last meeting | Score by quarter, team box, leaders, what carries over (same QB, coach change, who is still on the team), highlights link, recent meetings against the spread and total | nflverse schedules and play-by-play |
| Odds | Every book's spread, total and moneyline with no-vig and hold, best price, line movement, props inside 36 hours, the research simulation | The Odds API, pipeline snapshots |
| Weather & rest | Forecast, a plain verdict (including NWS alerts such as hurricane warnings), rain-adjusted passing, rest days, short week, bye, coming off an international game, time zones, body clock | NWS, nflverse schedules |
| Copy for Grok | The whole game as one paste, with the instruction to run `pregame/ANALYST_PROMPT.md` | this board |

Role tags: Primary (top target share), Volume (7+ targets a game), Deep threat (13+ yard average depth), Possession (short
targets caught 72%+), Boom-bust / Steady (how much yardage swings game to game), Rising / Falling (last three games against
the window), Red-zone #1, Most on field, Lead back (60%+ of carries), Committee, Goal-line back.

Man/zone and coverage shells are only published free through last season, so those panels say which season they use.

## Files

- `dashboard/data/<game_id>.json`: one file per game, everything on the board. ChatGPT or Grok can read these from the repository.
- `dashboard/site/index.html`: the page (built in the workflow and published to GitHub Pages; not committed).
- Build locally: `python3 -m dashboard.build`, then open `dashboard/site/index.html`.

GitHub Pages must be switched on once: repository Settings > Pages > Source: **GitHub Actions**. After that every scheduled
run publishes the board.

Research only. Nothing on the board is a validated projection or a bet recommendation.
