# Ghost acceptance packet — post-rebind integration expectations

**DIRECT GREEN. Ghost FINAL NOT CLAIMED. Source readiness OPEN / NOT READY.**
Actionable status **NOLINE**. Bias **UNIMPLEMENTED_NO_FITTED_CALIB** (unfitted,
null coefficients). Impact **NOT_MEASURED**. No projection permission or predictive
claim follows from these engineering results.

Captured 2026-11-06T12:21:05.895503+00:00 through 2026-11-06T12:21:08.407664+00:00 (UTC).
Authorized live contract SHA-256:
`6471e69b97b19b85ce0a4b8e4c25117b0e40ceefa1a225ee06d7c1b7440e8367`. The canonical path remains `core_contract.md` in the integration root;
DIRECT uses no override and no remap. Authority:
[CORE authorization](wire/CONTRACT_BINDING_AUTHORIZATION_2026-11-06.md) and
[BetGuru completion](/workspace/wt-market-calibration/research/market_calibration/reviews/BINDING_REBIND_COMPLETION.md).
Producer wire remains `1.0.0-producer` / `nfl-sim-joint-trial-producer-wire`.
Immutable example SHA-256 remains
`50be826a2bc1cf67db052aa8095ae0d7b3e75d674ef31c65165a5fbe3c881cdd`.

| Executed selection | Result | Evidence |
| --- | --- | --- |
| DIRECT unchanged actual producer → market | 1 passed, 0 failed; exit 0 | [log](wire/expectation_refresh_DIRECT.log) |
| Full live adversarial suite | 69 collected; 69 passed, 0 failed, 0 errors, 0 skipped; exit 0 | [log](wire/expectation_refresh_adversarial.log), [JUnit](wire/expectation_refresh_adversarial.xml) |
| Separate historical record | 6 skipped, explicit HISTORICAL_PRE_REBIND_RECORD; exit 0 | [log](wire/expectation_refresh_historical.log) |

Previous parent verification was DIRECT 1 passed and adversarial 51 passed /
9 failed. Those failures were stale binding, inventory, producer-test hash,
old wire-blocker expectations and flat-only score mutations. They are preserved
in [the parent record](wire/PARENT_VERIFY_POST_REBIND.json) and its original log.
BetGuru separately reports market 179 passed, binding 6 passed and DIRECT 1 passed;
those market suites were not rerun here. These counts measure engineering checks.

The refreshed live suite rejects conflicting freeze/dependency/status aliases,
INCOMPLETE or incomplete status objects, inconsistent OT flags/types, OT without
a regulation tie, noncontiguous OT, conflicting flat/nested points and invalid
score types. Agreeing aliases accept with native scores retained. Score sensitivity
checks native nested `stats.points` and agreeing legacy aliases, keeping both
spellings synchronized when both exist. Corrupted-score probes test consumer
arithmetic only; they are not valid producer draws.

DIRECT reads two unchanged durable synthetic producer trials and independently
retained ordered IDs. The immutable example also passes direct transport with
its frozen expected ID. Input/source equality and copied ownership are checked.
Both smoke trials remain COMPLETE / SCENARIO_ONLY, split UNASSIGNED, with
`adapter_projection_allowed=false` and zero adapter-usable trials. Native rows
revalidate with the CORE validator. Legacy diagnostic views remain disclosed
compatibility probes and do not participate in DIRECT.

The [market protected inventory](market_calibration_file_hashes.json) now pins
114 post-rebind files (previously 72); SHA-256
`3547c096e9c48ef2b742113b0e923b8d0dd6f4059c72181ce9160ff994e3398e`. All pinned entries match. Fresh verification pre/post
snapshots show market, CORE, source-gate, original producer review evidence and
contract/companion bytes unchanged during the final runs. Concurrent external
owner changes since the initial task snapshot are disclosed separately in the
machine evidence; the original snapshot and first attempt are preserved. Added
external files after inventory capture are not included in its pinned set.
No adapter code was edited by this refresh. The current producer `files_touched`
expectation for `test_joint_producer.py` is
`0496d8b619e29376c021973caec5b6ec1a0b50f70399539ab1c865c35c60f275`, matching
the phase4 wire pin evidence. The integration-local revision inventory preserves
the original smoke and retained IDs; `reviews/EVIDENCE_CODEX.json` is untouched.

Intentional pre-rebind SHA and five missing-field-stage expectations remain in
[the separate historical module](tests/historical/test_historical_pre_rebind.py),
all skipped with `HISTORICAL_PRE_REBIND_RECORD`. Original suite, packet, builder
and inventory bytes are archived alongside it. Frozen wire metadata and earlier
JSON/log evidence retain their historical binding and are not live authority.

Remaining acceptance blockers are open:

- B01 transport is resolved for the retained producer smoke and immutable example.
  Full CORE accounting acceptance in the adapter remains NOT_RUN; opaque invalid
  declarations/player counts can be copied while transport remains NOLINE.
- Canonical crosswalks and an alias-wide inspection registry are absent. Known
  inspected TNF aliases / 2026 W1–8 cannot become untouched holdout; the documented
  unseen-alias gap remains. Postgame artifacts stay EVIDENCE_ONLY_POSTGAME.
- Population enforcement requires independently retained ordered expected IDs.
  The library argument remains optional; omitting it can accept a truncated batch.
- Source readiness remains open for Ghost acceptance: source certification,
  canonical joins, approved workflow evidence and completion of all 15 phases
  are not established by this refresh. Concurrent source-packet work remains
  separate from this acceptance scope. Source-gate checks retain
  `projection_ready=false`; synthetic fixtures cannot be promoted to live evidence.
- Saved quotes remain SAVED_ONLY / NOLINE. Missing Pinnacle Q2–Q4 spreads remain
  NOLINE; rules are unverified (`book_rules_verified=false`), and no actionable
  joined quote/core envelope exists. Synthetic IDs are not relabeled for settlement.
- Market player targets/carries remain MARKET_STAT_UNSUPPORTED. Official OT,
  penalty/untimed-down and return acceptance, eligible legacy PBP export, fitted
  Bias, untouched holdout, predictive evaluation and Ghost final vet remain open.

[Machine evidence](INTEGRATION_EXPECTATION_REFRESH_EVIDENCE.json) contains exact
commands, environment, timestamps, exit codes, merged pytest output, before/after
hashes, inventory changes and protected-file comparisons. All authored writes are
under `integration/`; bytecode/cache writes are disabled and test fixtures live
under `integration/wire/`. No network requests, spend, odds pulls, new simulations,
Bias fitting or TNF fit-as-validation occurred.

Reproduce the three selections and rebuild this packet:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 integration/wire/verify_expectation_refresh.py
```

To rebuild only from captured evidence:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 integration/build_acceptance_packet.py
```

Ghost FINAL remains **NOT_CLAIMED**. NOLINE; Bias UNIMPLEMENTED; impact NOT_MEASURED.

### Status snapshot 2026-11-06 ~07:24 ET

- **DIRECT transport:** GREEN (parent + independent verify). Contract binding `6471e69b…`.
- **Adversarial live suite:** 69 passed after expectation refresh + inventory regen post anomaly-guard; historical pre-rebind suite preserved separately (6 skipped archival).
- **Source readiness:** `projection_ready=false`; gate BLOCKED; usable SUCCESS=0; diagnostic packet under `integration/certified_asof/` (`SOURCE_READINESS_EVIDENCE.json`).
- **Close quotes (held):** Pinnacle/DK/FD in `closes/CERTIFIED_CLOSE_PINNACLE_FD_DK.json`; book registry `BOOK_SOURCE_REGISTRY.json` (3 retrieved / 10 unavailable in hierarchy).
- **40pp delivery guard:** single-book guard landed (235 market tests); **consensus-across-books follow-up in flight** per Rico 07:17 (`MARKET_INTERFACE_CONSENSUS_ANOMALY.md`).
- **Ghost FINAL:** NOT claimed. NOLINE. Bias UNIMPLEMENTED. Impact NOT_MEASURED.
- Planning ETA (not deadline): eng 4–8h; calib/validation 1–2d conditional usable as-of.
