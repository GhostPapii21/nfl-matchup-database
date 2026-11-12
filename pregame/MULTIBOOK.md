# Book prices, same-line consensus and price freezes

Research only; `projection_ready` stays false and nothing here is a pick.

**Usage.** Everything lives in `pregame/odds.py`, the same pull path the packet builder uses, so one pull feeds both the packet's
"Book prices and no-vig" section and a timestamped freeze (no second credit spend). Books are FanDuel, DraftKings, Hard Rock Bet and
Caesars (`williamhill_us`), plus Pinnacle as a reference that is never counted. Each paid call is estimated first (game lines 3
credits for the whole slate; props up to 7 per game: pass yds, pass attempts, completions, rush yds, rush attempts, receiving yds,
receptions) after a free `/events` balance read, and is refused if it would leave fewer than `ODDS_CREDIT_FLOOR` (default 800) or if
the balance is unknown; every run prints `odds credits used this run=… remaining=…` ("unknown" when the provider did not report it).
`odds.consensus(markets, odds.roster_from_packet(packet))` gives each book's own line and a consensus only from books at the same
line (the line most books quote, with `n_books_at_line`); fewer than two books on one line, a tie between lines, or a player not
matched on full name + team gives the literal `no consensus` with a reason. Labels carry the real count (for example
`three-book prop consensus` when Caesars has `no props`). Passing yards are stored as reference fields flagged `never_a_leg`.
Between packet runs, `python -m pregame.multibook --game 2026_10_WAS_NYG [--compare <earlier freeze_*.json>]` writes
`pregame/price_freezes/<ET date>_<AWAY>@<HOME>/{raw,freeze,table}_<UTC>.*` using the packet's player list (`--dry-run` prints the
cost plan for 0 credits; `--movement OLD NEW` compares two freezes offline). For the end-to-end run, read `consensus` from the newest
`freeze_*.json` (schema `price-freeze/2`). The workflow change that adds `pregame/price_freezes` to the commit and sets the floor is
in `pregame/install/nfl-pregame-packets.yml`: copy it over `.github/workflows/nfl-pregame-packets.yml` (needs a token with the
`workflow` scope). Tests: `pregame/tests/test_multibook.py`.
