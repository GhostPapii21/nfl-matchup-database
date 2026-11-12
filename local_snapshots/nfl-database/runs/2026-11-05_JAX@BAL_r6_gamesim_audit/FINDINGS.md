# JAX@BAL game/quarter sim audit — BLOCKED
**Run path:** `/workspace/nfl-database/runs/2026-11-05_JAX@BAL_r6_gamesim_audit/`  
**Requested:** BAL TT U13.5; JAX 1Q −2.5; JAX 1H −2.5 / 1H 3-way only if existing drive sim supports  
**When:** 2026-11-05 ~12:51–12:55 America/New_York  
**Worktree note:** `/workspace/nfl-database` is on `mws-matchup-2026-11-04` (not `r6-full-gate-2026-11-04`). `/workspace/wt-jaxbal` is on `research-jax-bal-coverage-2026-11-04`. Left `backtests/v6_brainstorm_proedge/reads.log` alone. No production edits. No Odds API calls. No Cursor cloud spend. No bet/publish/merge.

## Verdict
**BLOCKED — cannot produce three GENUINELY DISTINCT calibrated models (Monte Carlo / Bias / Game Randomness, 100k each) for BAL team total or JAX quarter/half spreads.**

Reporting a true blocker rather than inventing calibration, inventing quarter allocation, or relabeling scenario cases / RNG seeds as models.

## What was inspected
| Artifact | Path | Finding |
|---|---|---|
| sim_v6 engine | `tools/sim_v6.py` | Native markets only: `passyds`, `rec`, `recyds`, `rushyds`, `rushrec`. No `team_total`, `spread_h1`, `spread_q1`, `h2h_h1`, `h2h_q1`. |
| Prior r6 1H wrapper | `runs/.../r6/codex/run_sims.py` + `sims.json` | Explicitly labeled `UNVERIFIED wrapper extension; sim_v6.nb + profile_v2; not native spread_h1`. MC/bias share the same half structure; no distinct fitted half-spread bias calibration. Prior notes forbid elevating it to pricing. |
| drive_sim | `week10/fagnano/drive_sim.py` + `drive_sim.txt` | Full-game BAL **scenario ESTIMATES** (`base` / `rico` / `flip`). Not MC/Bias/GR. No quarter margins. No half margins. |
| N3 1H read | `runs/.../r6/grok/n3_1h_script.md` | Qualitative only. Status **MISSING** for quantitative 1H model. Explicit: do not divide full-game points by two. |
| game_lines.py | `runs/.../r6/game_lines.py` | §7 / last-2 flag-only on historical margins. Edge field: `no game model -> no anchored p`. |
| Prior gate | `gate_A/B/C/gate_output.txt` | FAIL exit 1; 1H pricing UNVERIFIED; coverage/NGS/primary defender/TTT/form gaps remain. |
| Live FD prices | `runs/.../r6/odds/odds_live_fd_2026-11-05.{csv,json}` | Existing BetGuru pull; **no new credits**. |

## Requested markets — capability matrix
| Market | Native sim_v6 | Calibrated 3-model (MC/Bias/GR) | Existing drive_sim support | Action taken |
|---|---|---|---|---|
| BAL TT U13.5 | NO | NO | Full-game BAL pts scenario cases only (base/rico/flip) | Scenario re-verify only; **not** promoted to 3-model |
| JAX 1Q −2.5 | NO | NO | NONE (no quarter engine) | **BLOCKED** |
| JAX 1H −2.5 | NO | NO | NONE; prior wrapper was −6.5 and UNVERIFIED; FD API has no 1H −2.5 | **BLOCKED / not supported** |
| JAX 1H 3-way winner | NO | NO | NONE as priced model | **BLOCKED** (FD has 1H ML −380 as price only) |

## Model distinction (required vs available)
**Required (Phase 14 / Rico):** three distinct engines at 100k each — Monte Carlo, calibrated Bias (`sim_v6_calib.json`), Game Randomness (shared game-level shock + spread tilt). Seeds alone are not models.

**Available for player props:** `sim_v6.Engine.sim` with those three modes.

**Available for game/quarter:** none of the three. Prior r6 half extension used separate RNG streams on the **same** unverified allocation formula — seeds ≠ models, and it was already rejected as pricing.

**drive_sim cases are script scenarios, not models:**
- `base` = mid 3-and-out / mid TD-FG rates
- `rico` = higher 3-and-out / lower TD (Fagnano quiet script)
- `flip` = BAL finds more scoring

## drive_sim re-verify (existing held code; ESTIMATES)
Command:
```
cd /workspace/nfl-database/week10/fagnano && python3 drive_sim.py
```
Output saved: `drive_sim_rerun_2026-11-05_1251ET.txt` (byte-matches prior `drive_sim.txt` for the headline pts/P lines; seed 9, N=100000).

| Case | mean BAL pts | P(pts < 13.5) | mean Henry car | notes |
|---|---|---|---|---|
| base | 16.0 | 0.43 | 14.0 | ESTIMATE |
| rico | 13.5 | 0.54 | 12.0 | ESTIMATE; Fagnano quiet |
| flip | 20.0 | 0.30 | 18.0 | ESTIMATE |

These are **not** Monte Carlo / Bias / Game Randomness. Sampling uncertainty within a case is binomial on estimated rates; **model uncertainty across the three calibrated engines does not exist** for this market. Median score/quarter outputs for 1Q/1H are unavailable.

## Verified prices (existing pull — no new API)
Source: `odds/odds_live_fd_2026-11-05.json`  
`pulled_utc`: **2026-11-05T17:35:33Z** = **2026-11-05 12:35 PM America/New_York**  
Book: FanDuel only. Credits on that prior pull: `x-requests-last=9` (already spent; this audit used the saved file).

| Market | Side | Point | Price (vig-in) | Two-way no-vig (multiplicative) |
|---|---|---|---|---|
| BAL team total | Under | 13.5 | **−108** | **0.4896** (Over −118 → 0.5104) |
| JAX spreads_q1 | JAX | −2.5 | **−124** | **0.5279** (BAL +2.5 +102 → 0.4721) |
| JAX spreads_h1 | JAX | −6.5 | **−105** | 0.4892 (BAL +6.5 −115 → 0.5108) |
| JAX h2h_h1 | JAX ML | — | **−380** | 0.7505 (BAL +280 → 0.2495) |
| JAX 1H −2.5 | — | — | **NO_QUOTE in this FD pull** | — |

Single-side prices are vig-in, not no-vig (stated). Exact-rung two-way used above where both sides exist.

## Scenario vs market (flag only — not a model edge)
- BAL U13.5 no-vig under ≈ **0.49**. drive_sim rico case P(<13.5)=**0.54**; base **0.43**; flip **0.30**. Scenario-dependent; cannot claim +3 vs no-vig across three models.
- JAX 1Q −2.5 no-vig ≈ **0.53**. **No model p exists.** Historical §7 from `game_lines_out.txt`: PASS-DOWNGRADE 3/4 margins `[3,7,-7,7]` — flag only, not anchored p.
- Prior UNVERIFIED 1H −6.5 wrapper avg p ≈ **0.419** vs no-vig ≈ **0.49** (live −105/−115) → raw edge negative; already gate-failed. Not extended to −2.5.

## Gate status (existing; not re-run with invented game outputs)
Held existing assemble/gate not re-fed with placeholder game sims (would violate “no placeholders / no relaxing rules”).

| Slip | Path | Exit | Misses (from saved output) |
|---|---|---|---|
| A | `runs/.../r6/gate_A/gate_output.txt` | **FAIL (1)** | 28 listed in file header block |
| B | `gate_B/gate_output.txt` | **FAIL (1)** | 19 (per review_superpowers) |
| C | `gate_C/gate_output.txt` | **FAIL (1)** | 27 (per review_superpowers) |

### Exact remaining structural failures relevant to this ask
1. **No native / calibrated game or period sim** → cannot satisfy Phase 14 three-model requirement for BAL TT / JAX 1Q / JAX 1H.
2. Prior JAX 1H −6.5: `UNVERIFIED monte_carlo/bias/game_randomness pricing` gaps; edge fails (+avg p − no-vig < +3; model p < .45; medians do not clear 6.5); §7 FAIL 2/4.
3. **Coverage / primary defender / phase inputs still MISSING** (unchanged; no invented fills):
   - `coverage.man_zone` numeric rates
   - `coverage.mof` numeric rates
   - `pressure_inputs.time_to_throw`
   - N2 verified primary defender (Strange / Washington)
   - Numeric NGS (separation/cushion/RYOE/TTT)
   - Henry recent_form < 3 games with current QB (Fagnano)
   - Final inactives / pre-kick weather (Phase 15)
4. Assemble/gate **cannot accept** BAL TT / JAX 1Q as priced legs through the sanctioned interface without either (a) genuine calibrated engine outputs that do not exist, or (b) a prohibited production edit to `tools/run_gate.py` / `assemble.py` / `sim_v6.py`. **Suggested patch is notes-only below — not applied.**

### Suggested patch notes only (NOT applied)
To support game/period markets later would need a **new calibrated engine** (not a seed fork of drive_sim) with:
- distinct MC / Bias / GR definitions and backtested calibration for team points and period margins;
- sanctioned assemble fields for `team_total` / `spread_q1` / `spread_h1` / `h2h_h1`;
- gate recognition that UNVERIFIED wrappers cannot PASS Phase 14.
That is a Rico-approved model/rule change — out of scope for this audit.

## Commands / tests run
```
# inspect markets
rg -n "passyds|recyds|rushyds|mkt ==" /workspace/nfl-database/tools/sim_v6.py

# re-verify existing drive_sim (no code change)
cd /workspace/nfl-database/week10/fagnano && python3 drive_sim.py \
  > /workspace/nfl-database/runs/2026-11-05_JAX@BAL_r6_gamesim_audit/drive_sim_rerun_2026-11-05_1251ET.txt

# price source (read-only)
python3 -c '...'  # multiplicative no-vig on odds_live_fd_2026-11-05.csv

# prior 1H wrapper numbers
python3 -c 'import json; ...'  # reads codex/sims.json
```
No `run_gate.py` re-execution with new game legs (would require fabricated model p).

## Plain-language findings for Ghost6 vet
1. **We cannot honestly price BAL U13.5 or JAX 1Q −2.5 with the three required models today.** sim_v6 only does player props; drive_sim is a Fagnano scenario sketch for full-game BAL points, not MC/Bias/GR.
2. **Do not use the old JAX 1H wrapper as a model.** It was marked UNVERIFIED, failed the gate, and does not support 1H −2.5 (FD doesn’t even offer 1H −2.5 — only −6.5 and 1H ML).
3. **Closest scenario read for BAL quiet:** rico-case mean ~13.5 pts and P(<13.5)≈0.54 sits near the live U13.5 (~no-vig 0.49). That is a **script flag**, not a cleared edge. Base/flip disagree hard.
4. **JAX early script remains qualitative** (N3 + miss audit): Fagnano tape supports pressure / stalled BAL drives; 1Q −2.5 historically 3/4 with a last-2 downgrade — still **no anchored model p**.
5. **Locked door stays FAIL.** Coverage shells, primary defenders, TTT/NGS, Henry current-QB form, and inactives are still open. Feeding placeholders to force PASS was refused.
6. **Card implication:** keep holding until inactives; if Rico still wants a game-line leg tonight, it needs an explicit override that these are **scenario/price flags only**, not gate-cleared three-model edges — or wait for a real period engine.

## Files in this audit folder
- `FINDINGS.md` (this file)
- `drive_sim_rerun_2026-11-05_1251ET.txt`
