# Market interface — consensus anomaly guard (CORE ↔ BetGuru)

**Rico 2026-11-06 ~07:17 ET:** ≥40 percentage-point model−market gaps are anomalies vs **consensus across books**, not a single Pinnacle quote.

## Ownership
| Concern | Owner |
| --- | --- |
| Quote acquisition + consensus construction | **BetGuru** (`market_calibration`) |
| Source registry / provenance of retrieved vs unavailable | **CORE** (`integration/certified_asof/BOOK_SOURCE_REGISTRY.json`) |
| Producer wire / as-of cutoff identity | **CORE** |
| Delivery quarantine (≥40pp vs consensus) | **BetGuru** delivery_guard (coordinate schema with CORE) |

## Consensus rules (no guessed consensus)
1. Join only rows with **identical** `event` (or verified alias), `stat/market`, `period`, `line/point`, `side` semantics, and **cutoff/as-of** ≤ freeze.
2. Use **only retrieved** books from the registry. Missing Circa/BetCRIS/… stay MISSING — do not impute.
3. Hierarchy for consensus weighting/selection (BetGuru implements; CORE does not invent weights):
   - Primary: Pinnacle, Circa
   - Sharp: BetCRIS, Bookmaker
   - Secondary: DK, FD, BetMGM, Caesars, PointsBet, HardRock
   - Other: Bet365, BetOnline, Bovada
4. If fewer than a BetGuru-declared minimum of consensus-eligible quotes exist for that exact key, **do not invent consensus** — status `CONSENSUS_INSUFFICIENT` / NOLINE; anomaly guard may still quarantine vs available single-book only as `DIAGNOSTIC_SINGLE_BOOK_NOT_CONSENSUS` (not a surfaced edge).
5. `|model_p − consensus_p| ≥ 0.40` → quarantine `DIAGNOSTIC_ANOMALY` with inspection checklist: ID / units / prices / time / calibration. Preserve raw research values; independent vs anchored separation; Bias UNIMPLEMENTED; no fake shrink.

## Held JAX@BAL evidence (no new spend)
See `BOOK_SOURCE_REGISTRY.json` and `closes/CERTIFIED_CLOSE_PINNACLE_FD_DK.json`.
Retrieved in bounded selection: **pinnacle, draftkings, fanduel** only.
Unavailable in selection: Circa, BetCRIS, Bookmaker, BetMGM, Caesars, PointsBet, HardRock, Bet365, BetOnline, Bovada.

## CORE will not
Duplicate Odds API / Firecrawl book pulls BetGuru owns; fabricate consensus; claim Ghost final acceptance from transport tests alone.
