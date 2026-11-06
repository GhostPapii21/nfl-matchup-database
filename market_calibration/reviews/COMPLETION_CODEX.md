# BetGuru MARKET/CALIBRATION completion

Implemented in `/workspace/wt-market-calibration`, branch `betguru-market-calibration-2026-11-06`,
base commit `3448ad77ef3ce46488b4cccfb0cd7478c4d4b6b6`. All work from this session stays under
`research/market_calibration/`; no commit was created. Existing interrupted-session
logs and concurrently created tracking/parent-review files were preserved.

## Delivered

- `quotes.py`: exactly three saved CSVs, FD/DK/Pinnacle normalization, exact
  identity/timing/cutoff and coherent two/three-sided no-vig pairing, source
  hashes/rows/raw quote fields/IDs, conflict suppression and absent-line flags.
- `settlement.py`: standalone quarters, H1/H2/REG/FG, explicit unknown versus
  zero OT, pushes, three-way Tie, and full quote identity before score-only PASS.
- `calibration.py`: namespaced provenance, inspected development policy,
  holdout/development fit refusals, honest unfitted status, separately labelled
  baseline/hindsight raw scoring, raw/anchor deep-copy and identity/basis gates.
- `joint_trial_adapter.py`: contract 1.0.0 score transport, retained trial IDs,
  string seeds/derived seeds, source rows, feature missingness, population/order
  checks, no independent draws or invented player fields.
- `manifest.py`, `audit.py`, tests, README, honest MANIFEST and three artifacts.

## TDD execution

The container provides Python 3.13.5 as `python3`, without a `python` executable.
The initial command availability failure was corrected before implementation by
using this shell wrapper; subsequent red/green logs contain actual pytest runs:

```bash
export PYTHONDONTWRITEBYTECODE=1
python() { python3 "$@"; }
python -m pytest research/market_calibration/tests -q
```

The local pytest configuration disables cache writes. Evidence sequence:

| Log | Observed result |
| --- | --- |
| `pytest_initial_red.txt` | 4 collection errors: required modules absent |
| `pytest_implementation.txt` | 2 failed, 69 passed: core contract appeared |
| `pytest_contract_red.txt` | 3 failed, 71 passed: contract alignment tests |
| `pytest_first_green.txt` | 74 passed in 0.09s |
| `pytest_second_review_red.txt` | 17 failed, 76 passed: adversarial second review |
| `pytest_second_review_green.txt` | 93 passed in 0.11s after fixes |
| `pytest_saved_audit_red.txt` | 1 collection error: saved-audit module absent |
| `pytest_saved_audit_green.txt` | 96 passed in 0.14s |
| `pytest_final.txt` | 97 passed in 0.15s, including independent grade arithmetic |

Final required command output, exit code 0:

```text
........................................................................ [ 74%]
.........................                                                [100%]
97 passed in 0.15s
```

## Second self-review and fixes

After the first green run, a separate adversarial test module reproduced:
raw outputs from a different game/period/side/line/namespace/settlement being
blendable; absent raw identity; development or TNF being accepted as train;
anchored provenance entering raw scoring; game-level split bypass by changing
season; unchecked manifest success fields; missing feature metadata, effects
on missing routes, and inconsistent base seeds within a forecast.

Those paths were fixed, then the full suite was rerun to green. No findings
were left as an issue list. Raw outputs now require exact quote identity and
probability basis before any pending research blend. Fit gates accept only
uninspected train provenance and still produce no coefficients. Manifest checks
bind the contract hash and inspect separate empty raw/anchor artifacts.

## Independent saved-data validation

The saved audit covers 132 actual quote rows: all 132 have complete coherent
research pairs. An independent implied-probability formula checks each no-vig
result without calling the engine's no-vig helper. A separate direct arithmetic
test checks every one of the 100 available saved W/L/P labels without calling
the settlement helper. All agree. The other 32 raw CSV rows have no saved grade
and remain NOT_PRESENT. Pinnacle Q2/Q3/Q4 spreads have zero source rows and each
returns NOLINE. H1 is derived from standalone Q1+Q2; Q4 and OT stay unknown.

`python3 -m research.market_calibration.audit` generated the saved audit. A final
read-only verification rebuilt it in memory and confirmed exact JSON equality,
validated MANIFEST, checked the branch/base, and confirmed every git-status path
was under the allowed subtree and no tracked engine sources changed.

## Evidence boundaries

The core contract was initially absent and appeared during implementation.
It was then read in full and the adapter was aligned to its score-transport
schema and bound to SHA-256 `d6a4689f55bbc1231205dccf1d19de51019c40d87a7f7c1fd4ba5238cec836b9`.
No integration/core/Blitz files were edited. No simulations or network/odds
requests were run. All fixture forecasts are synthetic transport tests, never
claims of real forecasts, player targets, defenders, prices, or fitted parameters.

Quote MATCHED is explicitly scoped to research pairing. Actionable status is
NOLINE because canonical crosswalks, sportsbook rule compatibility and the
shared producer population have not been verified. Score PASS is explicitly a
hindsight score-convention audit with book_rules_verified=false. Full producer
accounting/event/clock acceptance is NOT_RUN; transport preserves the supplied
source and never upgrades that status. The source-event ID is not relabelled as
a canonical registry ID.

Calibration remains UNIMPLEMENTED_NO_FITTED_CALIB. Anchors remain
PENDING_VALIDATION and RAW_ONLY is the edge basis. Raw and anchored artifacts
are separately labelled and honestly empty because no model output was supplied.
W1–8 2026 and TNF JAX@BAL remain development_inspected. No holdout validation,
TNF fitting, baseline model performance, or successful full-core acceptance is
claimed. Baseline/hindsight descriptive scoring remains separately labelled;
immutable forecast/as-of verification is explicitly outside timestamp checks.

Completed UTC: 2026-11-06T11:24:27.843649+00:00
