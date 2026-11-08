# ≥40pp anomaly delivery guard completion

Implemented Rico's 2026-11-06 requirement in `research/market_calibration/` only.
`delivery_guard.guard_edge_delivery` quarantines absolute RAW versus market
no-vig gaps ≥0.40 as `DIAGNOSTIC_ANOMALY`. `surfaceable_payload` is null on
quarantine; original raw/model/market values and provenance remain available
for diagnostics. No probability conversion, clipping, shrink or fitting occurs.

## Delivery contract and wiring

- Exported `guard_edge_delivery` and `ANOMALY_EDGE_PP_THRESHOLD` from the package.
- `calibration.separate_outputs` always adds `delivery_guard`, even without a
  caller-proposed weight. It checks the raw gap, so a blended gap below 40pp
  cannot conceal a raw anomaly. Consumers must inspect this envelope and use
  only `surfaceable_payload` immediately before any edge display or delivery.
- No separate edge delivery entrypoint exists in this package. Direct consumers
  must call the exported guard. README documents the call site and input schema.
- All five diagnostic codes are implemented: `ID_CHECK`, `UNITS_CHECK`,
  `PRICE_TIME_CHECK`, `CALIBRATION_CHECK`, `EDGE_GAP_GE_40PP`. Checks accumulate
  independently; the threshold cannot suppress other diagnostic categories.
- Identity includes namespace/game, player when applicable, team, market,
  period, side, signed line and settlement. Probability bases must explicitly
  match. Invalid raw probability inputs now return a quarantined envelope from
  `separate_outputs`, with no proposed blend, instead of raising and discarding
  the diagnostic transport. Invalid caller weights still raise.
- Quote provenance retains American price, source/hash, retrieval/update times,
  line timing and in-play state. Missing time, explicit STALE, future retrieval
  relative to declared as-of, declared age excess and open/close timing mismatch
  all quarantine. In-play requires explicit opt-in. No arbitrary freshness limit
  is invented: caller declares as-of/maximum age; absent policy is recorded as
  `NOT_DECLARED`, with null age.
- RAW object and checked scalar/basis/identity must agree. Explicit anchored
  lineage and false fitted claims are quarantined. Caller declarations do not
  establish independent model lineage, canonical joins or validated prices.

## Separation and honest claims

Quarantine flags exist on the delivery envelope, without modifying the raw or
market-anchored research objects. Both are independently deep-copied. Existing
caller-proposed arithmetic is retained even on a threshold anomaly; it cannot
be selected as a fitted edge or release quarantine.

- Bias: `UNIMPLEMENTED_NO_FITTED_CALIB`, fitted=false, no coefficients.
- Anchored: `PENDING_VALIDATION`; supplied weight
  `CALLER_PROPOSED_NOT_FITTED`, otherwise `ABSENT`.
- Edge basis: `RAW_ONLY`. Actionable: `NOLINE`, including surfaceable research.
- Predictive/calibration/historical impact: `NOT_MEASURED`.
- Ghost final: `NOT_CLAIMED`. No integration acceptance claim.
- This task used no network, spending, simulations or new data acquisition.

## Validation

TDD RED was captured before implementation: `test_delivery_guard.py` failed
collection because the exported guard did not exist. First GREEN: 58 guard
tests passed. Additional payload-consistency, player, near-boundary and explicit
policy cases brought the guard coverage to 67 tests.

Final command from `/workspace/wt-market-calibration`:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest research/market_calibration/tests -q
235 passed in 0.36s
```

Logs: `pytest_anomaly_guard_red.txt`, `pytest_anomaly_guard_first_green.txt`,
`pytest_anomaly_guard_market_suite.txt`. Machine evidence:
`codex_anomaly_guard_evidence.json`.

Coverage includes both directions at 39.9pp, exactly 40pp (including `.7-.3`),
50pp, immediately below threshold, percent/odds/nonfinite inputs, every identity
field, missing/stale/future quotes, declared age limit and open/close policy,
unfitted status, contradictory payloads, raw/anchor deep-copy separation, and
quarantine regardless of caller weight. Fixtures are synthetic diagnostics,
not performance evidence.

## Scope and remaining work

All writes by this task were confined to the market package. No CORE producer,
core contract, or integration adversarial test was edited by this task. The
pre-change hash inventory is `anomaly_guard_scope_before.json`; comparison
observed concurrent external integration and market tracking/review changes,
including the external adversarial test. Those files were preserved. The JSON
evidence distinguishes those observations from the explicit task write list;
it does not assert the entire shared integration tree stayed unchanged.

Consumers outside this package must adopt the documented delivery guard at
their actual surface. Licensing, usable as-of data, fit, historical validation,
canonical identity and book rules remain separate work. Parent's planning
estimate (engineering 4–8h, calibration/historical validation 1–2 days conditional
on usable as-of data) is not a deadline or a validation claim. No license or
historical validation requirement was waived by these unit tests.
