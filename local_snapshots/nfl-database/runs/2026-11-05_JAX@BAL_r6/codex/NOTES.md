# CODEX r6 notes

Start ET: 2026-11-04T15:11:45 (CODEX launcher log creation).
End ET: 2026-11-04T15:38:51.
All times ET naive ISO. No commit, merge, Odds API call, tool-code edit, or edit to another run directory.

## Delivered

- `gate_adapter.py`: Henry carry_share now loads a sourced numeric block from `codex/legs_extra.json`; compatible adapter execution invokes the complete assembler. Pull timestamps use America/New_York rather than machine local time.
- `codex/build_inputs.py`: reproducible local-source input extraction. Henry last four games: 69 / 85 BAL RB designed carries = 0.8117647059. QB runs/kneels excluded. Per-game numerators/denominators are recorded. N1 passes in all gates.
- `codex/coverage.json`: PFR targets/completion fraction/YPT for Hamilton, Humphrey, Wiggins; PFF alignment and matchup sources; r5 addendum 3 recorded. Hamilton suppression NOT COUNTED. Assignments remain hypotheses, primary=false, rather than asserting a verified shadow matchup.
- `codex/pressure_inputs.json`: BAL >=5-rusher rate 33.0% (300 FTN-charted dropbacks); pressure proxy 24.33% (300); Lawrence checkdown proxy 21.72% (198 attempts); targets under the broader hit/sack/scramble/out-of-pocket proxy 39 (Washington 10, Strange 5), with receiver counts/definitions. This file uses the specified r2 pbp, so its named-target counts can differ from later Week10 copies; it does not silently merge incompatible samples.
- `codex/run_sims.py`, `sims.json`, `sims_audit.json`: 100,000 draws per model and all five legs, seed 20261104. Native sim_v6 player markets, unmodified calibration and engine; Fagnano clock/lead/carry context from `week10/fagnano`, `profile_v2/rico_sim.py`, `drive_sim.py`. Base in manifest; rico and flip sensitivities in audit. All source scenario rates remain ESTIMATES. Audit includes code, calibration and pbp SHA-256 hashes.
- `assemble.py`: reads CODEX/GROK JSON, uses exact adapter leg/slip definitions and recent_form for Phase 7, merges season/week/data_week provenance, target pool, forecast and weather, writes manifest/checklist/report for A/B/C, executes tools/run_gate.py, saves gate_output.txt and prepends the gate output to reports. Returns 1 when gates fail. Works from any current directory. No statistical disagreement automatically changes a leg to CUT.

## Explicit limitations / MISSING

- **No native spread_h1 in sim_v6.** The first-half entry is an UNVERIFIED, uncalibrated wrapper extension using the sourced Fagnano profile and observed JAX/BAL first-half scoring timing fractions. It is a sensitivity estimate, not supported native sim_v6 pricing. MC/bias share the same half-spread structure with separate fixed RNG streams; no distinct fitted half-spread bias calibration exists. Native engine use is identified separately in each half entry, the reports and audit. GROK's quantitative N3 model remains MISSING. Do not interpret the manifest script label as native first-half support.
- No actual BAL man/zone or MOFO/MOFC rates exist in the inspected r2-r5, snapshot, layers or free PFF files. Missing blocks retain evidence references and no fake values or pull timestamps.
- No valid Lawrence time-to-throw source; NGS screenshots are receiving routes, not time-to-throw. True pressure unavailable: pressure measures are labelled PROXY.
- No verified PRIMARY defender assignment: Hamilton/Strange and Humphrey/Wiggins/Washington are plausible mappings, not charted coverage. Addendum 3 specifically says not to count Hamilton suppression. N2 remains unmet.
- `grok/checklist_rows.json` absent at final assembly; all non-7 rows are explicitly MISSING. Re-run assemble when GROK supplies it. Other GROK files present were consumed; this task did not edit GROK files.
- GROK sources label injuries/weather data_week=8 although ESPN scoreboard identifies JAX@BAL as week 9. These supplied stamps are preserved and SRC-5 flags them. Week10 directory naming is not evidence the game is week 10.
- Strange yards and Henry alt prices lack no_vig in adapter; never infer a fair probability from one-sided prices. TE rank/depth evidence and final inactives remain missing. Forecast does not replace pre-kick weather checks. Placed legs unknown.

## Verification and outcome

- Fixed-seed rerun: sims.json and sims_audit.json byte-identical; hashes in verification_hashes.json.
- Missing-GROK integration check: removed all GROK inputs in a temporary r6-only fixture; all three manifests/reports/checklists/gate outputs were written without crashing, with MISSING fields. Fixture removed.
- Legacy gate_adapter entry point executed successfully through assembler. Every slip has four correct legs, three models and 60 phase rows (1-15 per leg). All five unique legs have numeric p/median in every simulation.
- Final A/B/C gates: FAIL, no auto-cuts. N1 passes; coverage/NGS/checklist/price/N3/depth/SRC-5 gaps and model/form disagreement remain exposed. Gate failure is the expected fail-closed result, not an approved card.

Rebuild: `python3 runs/2026-11-05_JAX@BAL_r6/codex/build_inputs.py`; `python3 runs/2026-11-05_JAX@BAL_r6/codex/run_sims.py`; `python3 runs/2026-11-05_JAX@BAL_r6/assemble.py`.

## Superpowers review corrections (2026-11-04)

Receiver target ranks are now wired with pbp evidence (Strange TE1, Washington WR1). Henry's N1 current-QB sample is 11/16 (Fagnano-led week 8 only); the 69/85 mixed-QB sample is retained as historical context. Henry recent_form is [53] with Fagnano, so the three-game form requirement remains unmet. MISSING blocks now use source/pulled_et with null values; assembly propagates explicit numeric-data and unverified-pricing gaps. N3 qualitative read is wired separately from the still-MISSING quantitative model. See review_superpowers.md for the final audit and gate misses; earlier delivery-time statements above are superseded where they differ.
