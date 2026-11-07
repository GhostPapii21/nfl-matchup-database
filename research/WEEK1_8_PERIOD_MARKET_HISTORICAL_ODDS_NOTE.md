# Historical Sportsbook Lines for Quarter / Half Markets — Availability Note

**Status:** RESEARCH_ONLY. No claim of matched odds + outcomes or backtest readiness.

## Verifiable Public Information

- **The Odds API** documents historical odds for period markets (e.g., `h2h_q1`, `spreads_q1`, `totals_q1`, `h2h_h1`, `spreads_h1`, `totals_h1` and equivalents) available from **May 3, 2023** onward.
  - Snapshots at 5- or 10-minute intervals.
  - Requires paid API key for full historical access; free tier does not expose complete archive.
  - Event-level historical endpoint returns closest snapshot ≤ requested timestamp, including book, market, line/price.
- **Settlement rules (standard, from Odds-API.io / The Odds API documentation):**
  - Quarter and half markets settle on that period only. Overtime does **not** count toward Q1–Q4 or first-half results.
  - Whole-number lines push (stake returned) when the period result lands exactly on the line.
  - Quarter-lines use half-win / half-loss conventions where applicable.
  - Void rules for cancelled or incomplete periods follow standard sportsbook practice (stake returned).
- **Other sources:** Sportsbook Review and Action Network provide some line-movement history and limited Bet Labs historical half data, but not a complete free timestamped archive of all quarter/half prices across multiple books for every 2026 Week 1–8 game.

## Recorded Fields When Verifiable

| Field | Availability |
|-------|--------------|
| Book | Yes (via paid Odds API or SBR line history) |
| Market | Yes (q1/h1 etc.) |
| Line / Price | Yes with timestamped snapshots (paid) |
| Timestamp | Yes (snapshot time) |
| Push / Void rules | Documented as above; game-specific application requires the exact line |

## Explicit Non-Claims

- No prices have been reconstructed or imputed.
- No complete matched set of timestamped lines + final period outcomes exists in free public form for the full 121-game sample.
- Therefore, **backtest readiness is not claimed**. Any future calibration would require purchased historical odds matched to the verified period scores.

Sources: https://the-odds-api.com/historical-odds-data/ (retrieved 2026-11-07), Odds-API.io settlement docs, SBR line history pages.
