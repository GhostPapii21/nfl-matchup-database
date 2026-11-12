# STAGED — Genuine period engine implementation & validation plan
**Status:** REVIEW ONLY — no live code/skill edits in this package.  
**Date:** 2026-11-05 ~12:54 America/New_York  
**Context:** Ghost6 already saved `football-period-game-flow` and linked it into `betting-game-brainstorm`, `nfl-betting-script`, and `nfl-game-script-run`. **Do not duplicate those skill amendments.**

Companion audit: `/workspace/nfl-database/runs/2026-11-05_JAX@BAL_r6_gamesim_audit/`  
(`FINDINGS.md` blocker + `SCREENSHOT_QUOTE_CORRECTION.md`)

---

## 1. What is already covered (no skill rewrite needed)
`football-period-game-flow` already requires: exact market/settlement distinctions; scenario-first Q1–Q4 flow; conditional historical clears with sample sizes; injury/QB/home-road/kickoff/weather as flags not invented coefficients; verified period engine; three real model families ≠ seeds; no-vig + actual SGP; gate without fabricating PASS; driver ledger. Linked one-liners exist in the three NFL checklists.

## 2. Actual missing requirements (engine / data / PHASE_SCRIPT)
| Gap | Why it blocks | Needed |
|---|---|---|
| No period markets in `tools/sim_v6.py` | Only `passyds/rec/recyds/rushyds/rushrec` | Separate period engine (do not bolt UNVERIFIED wrappers onto sim_v6) |
| `drive_sim.py` is scenario ESTIMATES | base/rico/flip ≠ MC/Bias/GR | Keep as scenario sensitivity only |
| Prior 1H wrapper UNVERIFIED | Same formula + seeds; failed gate | Do not revive as pricing |
| PHASE_SCRIPT silent on period markets | Projection model authority has no period section | Optional **approved** PHASE_SCRIPT addendum *after* engine exists (not staged as live text here) |
| Odds API incomplete vs book UI | 1H −2.5 was NO_QUOTE while FD offered it | Screenshot / book UI path as quote source; API not sole authority |
| Assemble/gate have no sanctioned period fields | Cannot PASS period legs without schema + real p | New input schema + tests before any gate PASS |
| No leakage-safe as-of period features | Conditional splits need pregame-known labels | Feature store with `as_of` cutoffs |
| No OOS calibration for period markets | Skill forbids claiming calibrated edge without it | Walk-forward backtest before gate enable |

## 3. Engine design (three genuine structures — not seeds)
**New module (proposed name):** `tools/period_sim_v1.py` (+ `period_sim_v1_calib.json`).  
**Do not edit** held `sim_v6.py`, `run_gate.py`, `rico*_rules.py`, `press_tier.py`, `door.py`, or existing `assemble.py` until Rico approves a merge plan.

### Outputs (per game, per market)
For each of Q1, Q2, Q3, Q4 standalone and H1/H2 cumulative:
- team points in period, margin, total  
- 2-way cover / 3-way winner+tie probabilities  
- medians + calibrated intervals  
- opening-possession flag; defensive/ST scoring share (sourced)

### Model family A — Monte Carlo possession chain
Drive-level state: field position, down/distance proxies from as-of rates, score differential → play-call lean, period clock. Sample drives until period ends. Distinct generative process.

### Model family B — Bias / calibrated residual
Start from MC period scores; apply **fitted** per-market multipliers from walk-forward residuals (period points, period margins), analogous to sim_v6 Bias — coefficients from data, never hand-set “proven” constants.

### Model family C — Game Randomness
Shared game-level shocks (pace, finishing variance, weather flag multiplier band) applied once per sim world, then period slices inherit the same shock (correlation across Q1–H1 automatic). Not a reseed of A.

**Forbidden:** labeling `base/rico/flip` or `SEED+i` as the three models.

### Settlement logic (hard-coded tests)
- Standalone Qn margin ≠ cumulative H1 margin  
- 3-way: tie wins the Tie ticket; favorite/underdog lose  
- 2-way integer spread: push when margin == line (book rules)  
- OT: excluded from Q1–Q4 / H1 unless market text says otherwise  

## 4. Data & leakage
- Inputs: nflverse pbp through **prior week only** for features; kickoff-week injuries/weather/odds stamped with `pulled_et`  
- Labels: period scores from same pbp, joined after feature cutoff  
- Conditional tables: always print **n / N** and filter list; reject auto-use of subsets with n below a Rico-set floor (propose n&lt;20 → FLAG only)  
- No causal claim from “team was X–Y when Injured Player out” without mechanism + second source  

## 5. Validation plan & tests
1. **Unit:** settlement helpers (Q-only vs H1; 3-way vs 2-way; push) against hand-built scoreboards.  
2. **Replay:** reconstruct period scores for 2024–2026 REG; assert match to box/pbp aggregates.  
3. **Calibration walk-forward:** weeks W use data ≤W−1; report Brier / log-loss / reliability by market family (Q1 spread, H1 spread, H1 3-way, TT).  
4. **Anti-leakage:** test that future injuries/odds cannot enter feature matrix.  
5. **Parity:** three models disagree on structure (different medians under controlled shock); identical seeds alone must not be accepted as “three models” in CI.  
6. **Price contract:** both-side no-vig required for edge claim; screenshot quotes allowed with hash + ET; API NO_QUOTE ≠ market missing.  
7. **Gate dry-run:** feed real period outputs through adapter; expect FAIL on missing coverage/etc., never silent PASS; refuse placeholder p.  
8. **Card rule:** if engine MISSING or calibration fail → **zero period legs**, no padding to 3 cards / 4 legs.

## 6. Approval boundaries (do not cross without Rico)
| Allowed now | Needs explicit Rico OK |
|---|---|
| Research code in isolated worktree / `skill_draft/proposals` | Editing live skills further |
| Screenshot quotes in run audit notes | Enabling period legs in `run_gate` |
| Scenario narrative + historical clear counts as FLAGS | Claiming Phase 14 PASS on period markets |
| Reading `football-period-game-flow` | Merging `period_sim_v1` into production tools |
| Holding TNF cards through inactives | Treating drive_sim or old 1H wrapper as calibrated |

## 7. Suggested next implementation order (after approval)
1. Settlement + pbp period reconstruction library + unit tests  
2. MC possession chain v0 (no Bias/GR yet) + replay accuracy  
3. Fit Bias + GR from residuals; freeze calib JSON with season/week stamp  
4. Odds/screenshot quote adapter (both sides)  
5. Gate adapter schema + FAIL-closed dry runs  
6. Only then: optional PHASE_SCRIPT period subsection + skill touch-ups if gaps remain  

## 8. Tonight (JAX@BAL) implication
Period skill can guide **qualitative** Q/H flow and miss audits. **Quantitative PASS still blocked** — same engine gap as `FINDINGS.md`. Screenshot correction restores 1H −2.5 / 3-way quotes for price discussion only.

---

## 9. APPEND 2026-11-05 ~12:55 ET — Market mirror (Pinnacle + broader) to avoid manufactured edges
**Source:** Ghost6 relay of Rico follow-up. Spec/report requirements only; **no engine build, no live skill/code change, no odds spend in this append.**

### 9.1 Required report fields (always preserve raw)
For every period candidate, the priced report MUST show **separately labeled** columns/blocks — never overwrite or silently replace:

| Field | Definition | Rule |
|---|---|---|
| `raw_model_p` | Each of MC / Bias / GR hit probabilities at the exact period/line/settlement | **Preserve always.** Never shrink, blend-away, or replace with a market number. |
| `pinnacle_novig_p` | Multiplicative no-vig from **exact matching** Pinnacle two-way (or three-way) | Two-way: normalize the two sides only. **Three-way: normalize all three outcomes** (home/away/tie or favorite/dog/tie). Never pretend a 3-way is a 2-way by dropping Tie. |
| `consensus_novig_p` | Broader-market consensus no-vig on the **same** period/line/settlement (document books + method) | Same 2-way vs 3-way rule. Record book set and pull timestamps. |
| `market_anchored_p` | Separately labeled estimate that starts from market (Pin and/or consensus) and may apply a **validated** adjustment | Must be tagged `market_anchored_p` — not presented as `raw_model_p`. |

### 9.2 Blend / shrink bans
- **No invented blend weights** in production output.
- **Do not revive** the retired 30% pull-to-50% shrink (Rico Nov 2, 2026).
- Any weights that mix `raw_model_p` with Pin/consensus MUST either:
  - be **fit on time-separated held-out validation** (train ≤ W−k, validate on later weeks; leakage-safe), **or**
  - be shown only as **sensitivity / proposed weights** with status **`PENDING_VALIDATION`** — never as the production probability used for edge PASS.
- Until validation passes, edge claims use `raw_model_p` vs `pinnacle_novig_p` (and consensus as cross-check), not an unvalidated anchored blend.

### 9.3 Matching & missing-quote flags
Flag (do not invent prices) when any of these fail:
- **Period mismatch** (e.g. model Q1-only vs book H1 cumulative)
- **Line mismatch** (e.g. −2.5 vs −6.5)
- **Timestamp / stale** (odds older than run policy; unknown stamp = STALE)
- **Settlement mismatch** (3-way vs 2-way; push rules; OT treatment)
- **Missing Pinnacle quote** for that exact market → `PINNACLE_MISSING`; still show raw model p and any other books; **no manufactured Pin no-vig**

Screenshot / soft-book quotes remain valid quote evidence when API gaps exist, but they do **not** substitute for `pinnacle_novig_p` unless the screenshot is actually Pinnacle.

### 9.4 Divergence handling (anti-manufactured-edge)
When `|raw_model_p − pinnacle_novig_p|` (or vs consensus) is **large** (threshold TBD in calibration; propose start at ≥10 pts absolute for review):
- Trigger **input / calibration audit** (settlement identity, sample leak, period definition, injury as-of, clock model).
- **Do not** auto-promote a giant “edge.”
- **Do not** auto-cut the scenario read solely on the gap; scenario stays a flag with both sides written (per brainstorm / period-flow skills).
- Preserve raw outputs in the audit artifact.

Same rule if model and market agree on side but disagree wildly on magnitude.

### 9.5 Added tests (extend §5)
9. **Raw preservation:** report writer fails CI if `raw_model_p` missing or overwritten by anchored/blend fields.  
10. **Pin two-way no-vig:** given O/U or spread both sides, multiplicative no-vig matches fixture; vig-in ≠ no-vig.  
11. **Pin three-way no-vig:** given three American prices, normalized probs sum to 1.0; dropping Tie and renormalizing two sides must **FAIL** the test (forbidden path).  
12. **Settlement identity:** pairing Q1 model p with H1 Pin line → `PERIOD_MISMATCH` flag; pairing 3-way model with 2-way Pin → `SETTLEMENT_MISMATCH`.  
13. **Missing Pin:** fixture with FD-only quote → `PINNACLE_MISSING`; no fake `pinnacle_novig_p`.  
14. **Pending weights:** any blend with `PENDING_VALIDATION` cannot set `edge_basis=production` or gate PASS.  
15. **No shrink regression:** pipeline must not apply 0.5+0.7(p−0.5) or equivalent to period probs.  
16. **Divergence audit hook:** synthetic |raw−Pin|≥10 pts emits audit record; does not auto-set leg CUT or PRESS solely from that gap; does not auto-PASS.  
17. **Consensus method stamp:** consensus block requires `books[]`, `method`, `pulled_et` or test fails.

### 9.6 Gap row (add to §2 conceptually)
| Gap | Why it blocks | Needed |
|---|---|---|
| No Pin/consensus mirror contract for period markets | Soft-book SGP product can manufacture edges vs true price | Spec §9 fields + tests before any period edge PASS |
| Unvalidated anchored blends | Look like edges without held-out fit | `PENDING_VALIDATION` or fit on time-separated holdout |

### 9.7 Approval boundary addendum
| Allowed in research staging | Needs Rico OK |
|---|---|
| Logging raw vs Pin vs consensus side-by-side on historical fixtures | Using `market_anchored_p` as production p |
| Proposing blend weights under `PENDING_VALIDATION` | Enabling period gate PASS on Pin-mirrored edges |
| Flagging Pin missing / mismatch | Inventing Pin lines from FD or SGP screenshots |
