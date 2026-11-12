# OpenAI review (gpt-5) 2026-11-04
Usage: 30053 in / 15107 out tokens

Below is a focused audit of the r6 JAX@BAL gate package against the run_gate README spec. I list concrete issues (file/field) and rank by severity. “Critical” means the package cannot legitimately pass the gate as-is or the tool is enforcing an undocumented fail. “High/Medium/Low” capture lesser severity or polish gaps.

A. Fail-closed blockers (spec violations or hard-gate requirements)
1) Unsupported leg type (“GAME”) and market (“spread_h1”)
- File: runs/2026-11-05_JAX@BAL_r6/gate_A/run_manifest.json
  - legs[2].type = "GAME"
  - legs[2].market = "spread_h1"
- Same in gate_B and gate_C manifests (the JAX 1H -6.5 leg).
- Spec mismatch: README’s legs[].type is enumerated WR|TE|RB|QB. “GAME” is not listed, and “spread_h1” is not a recognized player market in the spec example. This risks schema parsers rejecting the run or silently mis-parsing. Severity: Critical.

2) Live receiving legs missing required coverage.man_zone and coverage.mof (and wrong schema keys)
- Files: runs/2026-11-05_JAX@BAL_r6/gate_A/run_manifest.json
  - legs[0] (Strange 4+ rec) coverage.man_zone = {status,evidence_file,observed_et}, coverage.mof = {status,evidence_file,observed_et}
  - legs[1] (Washington rec yds) same
- Problems:
  - README: live receiving legs must have defenders (with targets/comp_pct/ypt), man_zone, and mof, each fresh/stamped within 48h. Your man_zone/mof are “MISSING” and use non-spec keys (evidence_file/observed_et) instead of source/pulled_et. Unknown/missing time = stale; these inputs therefore fail staleness and presence checks.
- Gate output corroboration:
  - gate_A/gate_output.txt:
    - “leg Strange 4+ rec (o3.5) man/zone: no source url/file”
    - “leg Strange 4+ rec (o3.5) MOF: no source url/file”
    - “leg Washington rec yds o63.5 man/zone: no source url/file”
    - “leg Washington rec yds o63.5 MOF: no source url/file”
- Severity: Critical.

3) Runs dated ≥ 2026-11-05: pressure_inputs.time_to_throw is required for live receiving legs
- File: runs/2026-11-05_JAX@BAL_r6/gate_A/run_manifest.json
  - pressure_inputs.time_to_throw = {status:"MISSING", reason, evidence_file, observed_et}
- README (“2026-11-01 lessons”): for runs dated ≥ 2026-11-05, live receiving legs need pressure_inputs.time_to_throw AND targets_under_pressure, each with a source and pulled_et. TTT is missing and uses “observed_et” (non-spec) instead of a pulled_et. Gate output flags “pressure input time_to_throw: no source url/file”.
- Severity: Critical.

4) Flagged gaps logic: NGS category missing but legs not CUT
- File: runs/2026-11-05_JAX@BAL_r6/gate_A/run_manifest.json
  - flagged_gaps includes {category:"ngs", reason:"No verified r6 source..."}
  - All legs have status "PASS"
- README: A missing category is allowed only if listed in flagged_gaps AND every leg is CUT. Gate correctly fails:
  - gate_A/gate_output.txt: “category ngs gap flagged but legs [...] not CUT”
- Severity: Critical.

5) Checklist rows have FAIL/MISSING/UNVERIFIED but legs are not CUT
- File: runs/2026-11-05_JAX@BAL_r6/gate_A/checklist.md
  - Many phases per leg are MISSING/FAIL/UNVERIFIED (e.g., JAX 1H: phases 2,4,6,7,9,10,12,14,15; Washington: 2,4,7,9,12,13,14,15; etc.)
- README: Any checklist FAIL/MISSING/STALE/UNVERIFIED row is allowed only if the leg status is CUT. Gate therefore fails closed. Severity: Critical.

B. Spec mismatches / undocumented gate behavior (could produce false FAILs)
6) Edge-rule “inputs missing” is not a documented fail case
- Gate output:
  - gate_A/gate_output.txt: “leg Henry 40+ rush (o39.5): edge-rule inputs missing (need no_vig, line, side, 3 model p)”
  - gate_B/gate_output.txt: “leg Strange 40+ rec yds (o39.5): edge-rule inputs missing (need no_vig, line, side, 3 model p)”
- In manifests:
  - Henry 40+: legs[*].no_vig = null (gate_A/B/C)
  - Strange 40+ rec yds: legs[*].no_vig = null (gate_B/C)
- README defines edge-rule calculations when inputs exist, but does not state “missing no_vig” itself is a fail condition. Enforcing this as a “MISS” is undocumented and could be a false fail reason (though this run would still fail for other reasons). Severity: High.

7) Undocumented N-rules: “DEPTH_RECEIVER” and “N2 no verified primary defender”
- Gate output (all three gates):
  - “DEPTH_RECEIVER not met: wr_rank/te_rank missing - can't tell if he is a depth receiver (fail closed)”
  - “N2 no verified primary defender (receiving legs can't go on a slip without one; …)”
- README contains no requirement to prove “depth receiver” via wr_rank/te_rank, nor a rule that a “verified primary defender” is required (the spec only requires defenders[] with targets/comp_pct/ypt and man_zone/mof). These appear to be extra gate rules not documented in the README. They can create false FAIL in otherwise compliant packages. Severity: High.

C. Additional format/data issues (contribute to failure or future fragility)
8) Wrong timestamp key in several objects: observed_et vs pulled_et
- Files: runs/2026-11-05_JAX@BAL_r6/gate_A/run_manifest.json
  - coverage.man_zone.observed_et used instead of pulled_et (also missing source)
  - coverage.mof.observed_et used instead of pulled_et (also missing source)
  - pressure_inputs.time_to_throw.observed_et used instead of pulled_et (also missing source)
- README: All times are ET naive ISO (“YYYY-MM-DDTHH:MM”), and inputs must have a source and a parseable pulled_et. Using observed_et plus no source is out of spec and fails staleness. Severity: High.

9) Duplicate/overlapping coverage_matchups sources
- File: runs/2026-11-05_JAX@BAL_r6/gate_A/run_manifest.json (top-level sources[])
  - Two entries reference /week10/bal_secondary/pfr_bal_defense_advanced.csv (one named “PFR BAL advanced defense (G=8)”, one “PFR BAL defender extraction (shell/man-zone missing)”).
- While not explicitly forbidden, duplicates can confuse SRC-5/week labeling and reviewers. Consider deduplicating or scoping with second_source if needed. Severity: Low.

10) Section 14 strict checks and price bands are being applied correctly to Washington rec yds; verify Strange 40+ rec yds handling stays “note only”
- Washington rec yds o63.5 has price_fd -114
  - gate_* outputs correctly fail §14 (median < 1.25×line and <3 of 4 ≥1.10×line).
- Strange 40+ rec yds o39.5 has price_fd 114 (plus-money), which per §14 should be “note only”; the gate did NOT fail it on §14 (good), but see item 6 where the tool flags edge-rule inputs missing (undocumented fail). Severity: Medium (ensure no unintended §14 fail is applied to plus-money overs).

11) Minor schema note: coverage.defenders include extra fields (completions, primary=false, assignment/alignment_source)
- Allowed (spec only requires name, targets, comp_pct, ypt, source, pulled_et); extras are fine, but ensure they don’t trigger SRC rules. Severity: Low.

12) Source-list SRC-5: per-source season and data_week
- PBP: season 2026, data_week 8; manifest week=9; scoreboard week source provided. This is consistent (historical feeds through wk8). No immediate fail noted, but keep labels consistent run-to-run. Severity: Low.

What to change (prioritized)
- Fix schema/type for the spread leg
  - If the tool must support game/quarter/half markets, update README to include type GAME (or an accepted value) and market spread_h1; otherwise, remove JAX 1H or move it to a separate non-gated analysis. As-is, it’s out of spec and risks parse errors.

- Provide coverage.man_zone and coverage.mof for receiving legs, with real sources and pulled_et
  - Replace the placeholder MISSING blocks with actual man/zone and MOF shell sources and stamps ≤48h old, or CUT all receiving legs. Using “evidence_file/observed_et” is non-compliant.

- Provide time_to_throw with a source and pulled_et (runs dated ≥ 2026-11-05)
  - For Strange/Washington legs, add pressure_inputs.time_to_throw {value, source, pulled_et}. Keep targets_under_pressure (already present) stamped.

- Reconcile “flagged_gaps: ngs” vs leg status
  - Either (a) add a compliant NGS source (or remove the category gap), or (b) CUT all legs. Per README, a missing category is only allowed when every leg is CUT.

- Align the gate’s behavior with the README
  - If “edge-rule inputs missing” (no_vig=null) is intended to be a fail, add this to README under “Fails if” (e.g., “edge-rule inputs incomplete on a live leg”). Otherwise, downgrade it to a warning.
  - If DEPTH_RECEIVER and “N2 verified primary defender” are intended gate rules, document them in the README. If not intended, disable them to prevent false FAILs.

- Normalize timestamp keys and presence
  - Replace observed_et/evidence_file with source/pulled_et on coverage.man_zone/mof and time_to_throw to satisfy the spec.

Concrete citations (examples)
- Unsupported leg type:
  - runs/2026-11-05_JAX@BAL_r6/gate_A/run_manifest.json: legs[2].type="GAME", legs[2].market="spread_h1"
  - Same in gate_B and gate_C.

- Missing/incorrect coverage keys:
  - runs/2026-11-05_JAX@BAL_r6/gate_A/run_manifest.json:
    - legs[0].coverage.man_zone = {"status":"MISSING","evidence_file":".../layers.md","observed_et":"2026-11-04T05:18"} (no source/pulled_et)
    - legs[0].coverage.mof = same pattern
    - legs[1].coverage.man_zone/mof = same pattern

- Missing time_to_throw:
  - runs/2026-11-05_JAX@BAL_r6/gate_A/run_manifest.json: pressure_inputs.time_to_throw = {"status":"MISSING","reason":"...","evidence_file":".../layers.md","observed_et":"2026-11-04T05:18"} (no source/pulled_et)

- Flagged gaps while legs are live:
  - runs/2026-11-05_JAX@BAL_r6/gate_A/run_manifest.json: flagged_gaps=[{"category":"ngs","reason":"No verified r6 source..."}] and all legs status="PASS"
  - Reflected in: runs/2026-11-05_JAX@BAL_r6/gate_A/gate_output.txt: “category ngs gap flagged but legs [...] not CUT”

- Undocumented/overfiring gate reasons:
  - runs/2026-11-05_JAX@BAL_r6/gate_B/gate_output.txt:
    - “leg Strange 40+ rec yds (o39.5): edge-rule inputs missing (need no_vig, line, side, 3 model p)”
    - “leg Strange 4+ rec (o3.5): DEPTH_RECEIVER not met...”
    - “leg Strange 4+ rec (o3.5): N2 no verified primary defender...”
  - runs/2026-11-05_JAX@BAL_r6/gate_A/gate_output.txt:
    - “leg Henry 40+ rush (o39.5): edge-rule inputs missing...”
    - plus same DEPTH_RECEIVER and N2 messages for receiving legs.

Bottom line
- The package is correctly failing closed today on multiple documented grounds (coverage man_zone/mof missing, time_to_throw missing for receiving legs on ≥2026-11-05 runs, NGS category gap while legs are live, many checklist phases failing without CUT). Those must be fixed to even attempt a PASS.
- Separately, the tool is enforcing additional rules not in the README (“edge-rule inputs missing,” DEPTH_RECEIVER, “verified primary defender”). Either document these as gate conditions or treat them as cautions only. As written, they can produce false FAIL reasons against the published spec.
- Finally, the JAX 1H leg is out-of-spec (type=GAME, market=spread_h1) relative to the README’s legs schema; either document support for game/half markets or remove it from the gated manifest.
