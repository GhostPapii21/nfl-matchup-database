# NFL-68 book rules: Firecrawl addendum (Nov 7 2026, 07:03 ET). Model NOT READY.
This adds to the first pull; the original files are unchanged. 3 Firecrawl searches with page scraping, no extra page reads, no proxy or stealth options, and no blocked URL retried. Raw results are in `.firecrawl/`.

## DraftKings: official text retrieved (the page names the Virginia platform; other states unverified; no effective date shown)
- Push ([general rules](https://sportsbook.draftkings.com/help/general-betting-rules/general-rules)): settled "as neither won nor lost ... only the stake amount of the bet is returned". In a parlay or SGP, a pushed leg's stake stays "on the Parlay with the remaining number of legs."
- Participation ([football rules](https://sportsbook.draftkings.com/help/sport-rules/football)): "Participation shall mean playing in at least one play in the applicable Event."
- SGP ([market rules](https://sportsbook.draftkings.com/help/general-betting-rules/market-rules)): voided or pushed legs are removed and the SGP "will be repriced based on the remaining legs".
- [MA Gaming Commission copy, Aug 1 2024](https://massgaming.com/wp-content/uploads/DraftKings-House-Rules-8.1.24.pdf) (stale): a player listed "inactive" or "did not play" → "bets on that player/market will be void"; settled on official NFL statistics.
- Inference: the push definition is generic (its examples are moneyline and spread). Applying it to a player-yardage line landing exactly on a whole number is an inference.

## BetMGM: official regulator copy only ([MA Gaming Commission PDF, Aug 10 2023](https://massgaming.com/wp-content/uploads/BetMGM-House-Rules-8.10.23.pdf)); current site text still not retrieved
- "must play at least one snap"; "cancelled where ... listed as inactive"; QB markets "must start the game"; "Passing yardage props are settled as per gross passing yards."
- SGP: "If any selection within a SGP is voided, then the entire SGP is voided." This is the opposite of DK and FD repricing.
- Still missing: an explicit push/refund rule for whole-number player props, the ordinary-parlay push rule, and confirmation that this is the current version.

## FanDuel: unchanged
Only the game-level whole-number Total refund rule, now also found in the official [CO](https://www.fanduel.com/fanduel-sportsbook-house-rules-co) (effective Sep 30 2026) and [OH](https://www.fanduel.com/fanduel-sportsbook-house-rules-oh) (effective Oct 29 2026) rules. Parlay or SGP with every leg void except one → settled as a straight bet. No player-prop push sentence found.

## Remaining
- [ ] Current BetMGM rule text
- [ ] DK/FD/MGM state applicability for the user's jurisdiction
- [ ] Market-specific whole-number prop push text (all three books)
- [ ] Zero/negative yards: no rule found for any book, so they stay fail-closed
- [ ] Other books: fail-closed

Secondary only (not confirmation): Action Network, RotoGrinders.
