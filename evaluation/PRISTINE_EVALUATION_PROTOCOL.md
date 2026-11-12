# Pristine evaluation protocol (NFL-44)

This protocol scores locked pre-kickoff snapshots of future games only. The machine-readable version is
`PRISTINE_EVALUATION_PROTOCOL.json`. `PROTOCOL_FREEZE.json` pins its sha256 and the hash of every lock that
existed before any outcome was known.

- **No historical pristine claim.** `historical_pristine_claim` is `false`. Weeks 1-9 of 2026 were used in
  development, so they are not holdout evidence.
- **Eligible snapshot:** the lock was made before kickoff and is either hashed in the freeze or made after it, with n = 100,000,
  `code_dirty` false, as-of checks PASS and `projection_ready` false.
- **Unscorable reasons** form a closed list (see the JSON). A game with no frozen quote is `NOLINE`, and its
  market comparisons are not scored.
- **Coverage:** below 30 scored games across 3 weeks, the aggregate status is
  `UNSCORABLE_INSUFFICIENT_COVERAGE`. Per-game numbers are still written, but they are not calibration evidence.
- **Comparison:** the raw model is compared with each book's no-vig probability. No market-anchored output is
  produced, so `independently_calibrated` stays `false` (NFL-45).

Commands:

    python3 -m evaluation.protocol freeze      # writes PROTOCOL_FREEZE.json (refuses if any listed game is already final)
    python3 -m evaluation.protocol evaluate    # aggregates SCORE.json files under the protocol
