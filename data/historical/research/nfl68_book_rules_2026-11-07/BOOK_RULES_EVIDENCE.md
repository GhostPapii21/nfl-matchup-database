# NFL-68 book-rule evidence: integer yardage (Nov 7 2026, ~7:00 AM ET)
Research only. **Model: NOT READY.** Rule evidence does not certify EV code. Raw pages and fetch log are in `raw/`; `book_rules_evidence.json` holds the full quotes.

## FanDuel: PARTIAL official confirmation (Massachusetts only)
Source: https://www.fanduel.com/fanduel-sportsbook-house-rules-ma. Effective date shown: Nov 5, 2026. Retrieved 06:59 EST. Massachusetts (MGC) only; other states unverified.
- Void (singles): "For player prop markets, only when a player does not play a snap in that game are the selections voided. All other bets will stand." Kicking-points props are an exception: they stand if the player is active but plays no snap.
- Whole number (game-level totals): "...& Total betting, where the index (value) of the market is a whole number, bets are void and will be refunded where the score lands on that number." I found no player-prop-specific push sentence, so an exact-line refund on yardage props is an **inference** from this rule.
- Parlay: a void leg is removed ("a treble including one void leg will become a double"). SGP: "If a selection within the wager is voided, the wager odds will be re-calculated using the remaining legs." I found no quote on how a player-prop push settles inside a parlay.
- Stats come from the league's governing body. No negative-yardage rule found.

## DraftKings: user-confirmed, official text NOT retrieved
I tried four official URLs (help/sport-rules/football, help/sports-betting-rules/football, help/general-betting-rules, support KB0010795). Each returned a 403 or a JavaScript shell with no rule text. Third-party quotes are not counted as confirmation. Jurisdiction unknown.

## BetMGM: user-confirmed, official text NOT retrieved
I tried four official URLs (house-rules returned 404; sports-betting-rules NJ, mobileportal/houserules and the NJ help page returned JS shells or 404). Per Action Network only (not confirmed): QB markets require the QB to start, and passing yards are settled as gross. Both matter for EV but are unverified.

## Others: unconfirmed, fail closed.

## Minimum gate checklist (still open)
- [ ] Official DK and BetMGM text for push/refund on integer player-prop O/U singles, saved via a browser-rendered capture of the official page (needs approval; the browser was excluded this pass)
- [ ] An explicit FD player-prop push rule, or accept the inference from the game-level totals rule
- [ ] Parlay/SGP push and void repricing kept separate from singles (FD void quoted; DK/MGM pending)
- [ ] State applicability for each book (only FD Massachusetts proven)
- [ ] BetMGM QB-start rule and gross-yards basis from the official page
- [ ] Zero/negative-yard lines: no rule found for any book, so keep them blocked. Pick'em/alt X+ markets are out of scope.
