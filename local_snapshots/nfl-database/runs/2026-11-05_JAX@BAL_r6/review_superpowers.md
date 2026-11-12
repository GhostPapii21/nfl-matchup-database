# Superpowers review: JAX@BAL r6 full run_gate package

Reviewed `a717d91c5d1cffd97874d914bdc7a481879b1362..cced7246fc3d2eefaf07c5414f4b0bf2ca27ab3d` against `briefs/CONTRACT.md`, `briefs/codex.md`, `briefs/codex2.md`, `tools/README_run_gate.md`, the executable gate/rules, source artifacts, and `review_openai.md`. References below are repository-relative and point to the final working tree. This review includes authorized fixes, without a commit.

The requested Superpowers paths were absent. Read the installed equivalents at `/home/box/sand-data/plugins/cache/cursor-public/superpowers/d884ae04edebef577e82ff7c4e143debd0bbec99/skills/requesting-code-review/code-reviewer.md` and `skills/systematic-debugging/SKILL.md`. Followed the template and investigated/reproduced causes before changes. The user's explicit instruction to fix r6 bugs governs the template's otherwise read-only review restriction.

## Strengths

- **NOT A BUG — Reproducible native player simulations:** `runs/2026-11-05_JAX@BAL_r6/codex/run_sims.py:17` uses the unchanged sim_v6 engine, 100,000 draws, seed 20261104, and sourced Fagnano estimate scenarios. A fresh offline execution reproduced both `sims.json` and `sims_audit.json` byte-for-byte against `codex/verification_hashes.json`. This establishes reproducibility, not model calibration for the unsupported half-spread extension.
- **NOT A BUG — Coverage numbers reconcile:** `runs/2026-11-05_JAX@BAL_r6/codex/build_inputs.py:45` matches `week10/bal_secondary/defender_table.csv`: Hamilton 34 targets, .706 completion fraction, 6.0 YPT; Humphrey 42/.595/8.5; Wiggins 36/.556/6.1. These are rounded source rates, not newly estimated assignments. `primary=false` and Hamilton suppression NOT COUNTED remain correct.
- **NOT A BUG — Target-pool arithmetic:** `runs/2026-11-05_JAX@BAL_r6/grok/target_share_pool.json:12` reconciles to 195 named JAX targets and 96 in weeks 5/6/8. Washington is 48/195 season and 22/96 in the last-three current-QB-week window, the only player qualifying at .22. Strange is 35/195 and 17/96. Including all targets in Lawrence's selected weeks follows `tools/rico4_rules.py:52`; it is not an accidental substitution of QB-only attempts. Slip B has an explicit Washington skip reason; slip C's alternate Strange leg is explained.
- **NOT A BUG — Film retrieval evidence exists:** `runs/2026-11-05_JAX@BAL_r6/grok/film_verified.json:1` lists five existing nonempty MP4s. ffprobe confirms all are 720p; URL/title/date/channel match saved `.info.json` metadata and the official NFL channel ID. `grok/film_play_matches.json:1` matches Strange play 1151 (Q2 11:33, 9 yards) and Washington play 1711 (Q2 03:57, 16 yards, Latu QB hit) in IND@JAX; caption timestamps exist. This is local metadata/caption/pbp reconciliation, not new web verification or a full film/coverage study.
- **NOT A BUG — Honest live evaluation:** `runs/2026-11-05_JAX@BAL_r6/assemble.py:77` preserves every requested leg as PASS for evaluation; all three slips retain their exact four legs. Checklist disagreements and absent evidence still fail the gate. No leg was CUT/HOLD to manufacture approval.

## Critical

1. **FIXED — Provenance-only validation could credit absent measurements or unverified pricing.** `runs/2026-11-05_JAX@BAL_r6/assemble.py:29` and `assemble.py:85`. Root cause: `tools/run_gate.py:99` checks source and time in coverage/pressure blocks, without inspecting `status` or numeric values; the prior assembler always emitted empty leg gaps. Merely normalizing the MISSING blocks' keys would remove their direct gate failures. Similarly, the 1H wrapper's `pricing_engine=UNVERIFIED` was commentary rather than an enforced gate condition. Added explicit leg gaps for missing numeric coverage/pressure values, unverified simulation pricing, missing input artifacts, and fewer than three current-QB form games. No measurements were filled. Regression `review_checks.py:133` demonstrates that fresh MISSING provenance passes the primitive stamp check, but still causes a gate miss even with every checklist row changed to PASS. This was a latent false-PASS route; the original complete package already failed on other blockers.

2. **FIXED — Henry recent form bypassed the current-QB requirement.** `runs/2026-11-05_JAX@BAL_r6/gate_adapter.py:13`. Root cause: the adapter labeled four mixed-QB games `(any; rush leg)`, although README and gate §7 require current-QB games for every live leg. Pbp shows Huntley led weeks 5–7 and Fagnano led week 8. Henry now has `[53]`, game `2026_08_BAL_BUF`, QB `J.Fagnano`. The three-game requirement cannot pass. The explicit form gap also makes this visible despite the gate's early continuation when Henry's no-vig is missing. The old yards were accurate historical numbers; their eligibility label was wrong.

## Important

1. **FIXED — Receiver ranks were computed nowhere in this package.** `runs/2026-11-05_JAX@BAL_r6/codex/build_inputs.py:28` and `assemble.py:78`. Root cause: `legs_extra.json` only contained Henry's carry share; no rank/depth fields reached the manifest. Wired the existing `depth_wiring` current-QB window and TE rank helper, plus equivalent WR position-target ranking, with pbp provenance/games/counts. Strange is TE1 with 25 targets, Washington WR1 with 25 targets in weeks 4/5/6/8. Missing-rank gate misses disappear legitimately. These are historical target ranks under the helper convention, not invented current depth-chart designations. Neither player triggers depth-only script/defender/rung exceptions at rank 1.

2. **FIXED — MISSING blocks used the wrong schema keys.** `runs/2026-11-05_JAX@BAL_r6/codex/build_inputs.py:43`. Root cause: the shared missing-block constructor emitted `evidence_file/observed_et`; the gate expects `source/pulled_et`. Replaced these with the existing evidence file/time and `value:null`, retaining `status:MISSING` and reasons. The source identifies the inspected gap evidence, not a measured rate. Critical item 1 ensures that this normalization cannot approve missing coverage or time-to-throw.

3. **FIXED — Henry N1 used a mixed-QB window.** `runs/2026-11-05_JAX@BAL_r6/codex/build_inputs.py:15`. Independently verified 69/85=.8117647059 for the four historical BAL games, but `tools/depth_wiring.py:26` specifies games led by the current QB. Correct current-QB numerator/denominator is 11/16=.6875 in week 8. Kept 69/85 as explicitly historical context, added current QB and sample, and updated the opportunity row. N1 still clears 60%; this does not establish three-game form or a stable Fagnano-era estimate.

4. **FIXED — Offline rebuilds could falsely refresh injuries/news and pbp-derived provenance.** `runs/2026-11-05_JAX@BAL_r6/grok/build_deliverables.py:7` and `build_deliverables.py:24`. Root cause: `datetime.now()` was exported as a new source pull time while the script only reread saved HTML and parquet. Preserved the saved injury inspection time on rebuild and used the pbp file's existing pull time for the target pool and its source entry. No network acquisition is implied. Added the pre-kickoff pbp cutoff so a later feed update cannot add game/future results to this run.

5. **FIXED — Film PASS did not depend on downloads remaining present.** `runs/2026-11-05_JAX@BAL_r6/grok/build_deliverables.py:50` and `build_deliverables.py:117`. Root cause: the generator recorded `downloaded=false` if an MP4 disappeared but still unconditionally credited the film category and receiving Phase 10 rows. They now remain MISSING unless at least three metadata-backed downloads exist and all indexed files are present. All five are present in this workspace. Ignored MP4s are local artifacts; a clean checkout without them will need those source artifacts restored, not a fabricated PASS.

6. **FIXED — Qualitative N3 read was not exported to the gate schema.** `runs/2026-11-05_JAX@BAL_r6/grok/build_deliverables.py:55`. The existing `miss_audit_1H.md:7` and saved narrative supply a JAX early-control thesis, but no `script_read.expected_winner/source` was produced. Exported that qualitative read and source separately. N3 now recognizes it; the quantitative model remains MISSING and the unverified-pricing gaps still block the half-spread leg.

7. **DATA GAP (cannot fix without new source) — Actual matchup/NGS and final readiness evidence remains absent.** `runs/2026-11-05_JAX@BAL_r6/codex/coverage.json:22`, `codex/pressure_inputs.json:31`, and `grok/build_deliverables.py:93`. No verified man/zone rates, MOFO/MOFC rates, Lawrence time-to-throw, or primary defender assignments were found in the supplied files. Route screenshots do not supply fresh numeric NGS coverage; final inactives/pre-kick checks are outstanding. These remain MISSING or UNVERIFIED with leg gaps and failed phases. Fresh measurements, assignment evidence, and final availability sources are needed; no surrogate numbers or primary flags were invented.

8. **DATA GAP (cannot fix without new source) — Unsupported half-spread pricing and missing exact-rung opposite prices.** `runs/2026-11-05_JAX@BAL_r6/codex/run_sims.py:70`, `gate_adapter.py:10`, and `gate_adapter.py:13`. sim_v6 does not implement native spread_h1; the wrapper's half-allocation estimates are not calibrated half-spread pricing, and MC/bias lack distinct fitted half-spread calibration. Existing full-game estimates do not fix that gap. Strange o39.5 receiving yards and Henry o39.5 rushing lack exact-rung two-way no-vig prices. Preserve the unverified sensitivities and null no-vig values. Do not infer missing fair prices from one-sided alt odds, another rung, or a new paid API pull.

9. **NOT A BUG — GAME/spread_h1 is supported by the actual period-spread rules.** `runs/2026-11-05_JAX@BAL_r6/gate_adapter.py:12`; `tools/rico_nov2_rules.py:22` explicitly recognizes GAME/SPREAD and half/quarter markets. The README example is incomplete, not a rejecting schema. `review_openai.md`'s proposed removal/retyping of the user-requested JAX leg is unwarranted. Retained it with honest model limitations.

10. **NOT A BUG — Missing no-vig, depth rank, primary defender, and bad checklist phases are legitimate blocks.** `runs/2026-11-05_JAX@BAL_r6/gate_A/gate_output.txt:7`; see `tools/run_gate.py:455`, `tools/depth_rule.py:21`, and `tools/rico_nov2_rules.py:39`. A missing fair-price input cannot establish the edge inequality. Depth/N2 are approved executable rules despite README omissions. Bad phases/NGS gaps with live legs must fail. Contrary suggestions in `review_openai.md` do not authorize weakening the gate or changing legs to CUT.

## Minor

1. **FIXED — Premature no-vig rounding at strict edge thresholds.** `runs/2026-11-05_JAX@BAL_r6/gate_adapter.py:8` and `grok/build_deliverables.py:100`. Three-decimal constants could change a decision near +.03. Replaced them with full-precision arithmetic from the saved Pinnacle two-way prices: Strange receptions .5147710487444609; Washington yards .5063197809142617; JAX 1H .4874783717329934. Regression reconciles the values to the CSV. This run's verdict does not flip. FD -122 for Strange main receptions is correct; the -125 alternate listing is a separate CSV market.

2. **NOT A BUG — Pressure figures use explicitly different definitions.** `runs/2026-11-05_JAX@BAL_r6/codex/pressure_inputs.json:12` versus `grok/build_deliverables.py:89`. Reconciled .33 blitz over 300 charted BAL dropbacks; .243333 sack/hit/scramble proxy over 300; .2171717 checkdown proxy over 198 Lawrence attempts; and 39 pressure-proxy targets (Washington 10, Strange 5), with 56 proxy dropbacks. The checklist's .17 is the narrower hit-or-sack rate in `L2_bal_pressure.csv`, so it need not equal .243333. No numeric correction warranted; proxies remain labeled.

3. **NOT A BUG — Duplicate coverage source descriptions and additional defender fields.** `runs/2026-11-05_JAX@BAL_r6/grok/sources.json:2` and `codex/coverage.json:10`. Both descriptions reference genuine PFR extraction evidence; extras such as completions, alignment, and `primary=false` do not violate a schema. Deduplication is optional and would not supply missing coverage rates or change SRC-5. Retained.

4. **NOT A BUG — Plus-money Strange yards cushion handling and schedule week.** `runs/2026-11-05_JAX@BAL_r6/gate_adapter.py:10` and `assemble.py:98`. +114 remains a §14 note-only band; the actual blocks are missing no-vig and a GR median below 39.5. The saved ESPN event identifies week 9; `week10/` is a workspace label, with results through week 8. No invented week relabeling applied.

## Validation and assessment

Executed the input builder, GROK offline builder, fixed-seed simulation wrapper, and final `python3 runs/2026-11-05_JAX@BAL_r6/assemble.py`. The simulation outputs matched both recorded SHA-256 values. `python3 runs/2026-11-05_JAX@BAL_r6/review_checks.py` passed all nine source-reconciliation/regression tests, including an all-PASS-checklist adversarial fixture. Existing unclosed-file ResourceWarnings originate in the read-only gate tool and did not fail tests. `git diff --check -- runs/2026-11-05_JAX@BAL_r6` passed.

**Ready to merge / approve slips? No.** Confirmed wiring/provenance bugs are fixed, but data gaps and actual form/model disagreement still block all slips. The first-half model limitation is a significant unmet contract requirement, not cured by the `tools/sim_v6.py` label. Saved forecast remains 25% precip, 3 mph wind, 9.2 mph gusts (no flag); it was not refreshed or substituted for pre-kick availability. No Odds API call, key output, tool/other-run edit, cut-to-pass change, commit, or branch movement was performed. Existing unrelated working-tree changes were left alone.

Recommendations: obtain the missing primary assignments, shell/NGS/TTT and final availability sources; obtain real exact-rung opposing prices; use a supported/calibrated first-half model before treating its numerical sensitivity as pricing. Preserve the explicit gaps until that evidence exists.

## Final per-slip gate misses

Final assembly returned exit 1, with every requested leg still live. N1 recognizes Henry's sourced 11/16 share, receiver missing-rank misses are resolved, and N3 recognizes the sourced qualitative JAX read. Henry's one-game form gap remains explicit; the gate's missing-no-vig early continuation means its form block appears through Phase 7 and leg gaps rather than a separate §7 line.

| Slip | Result | Exit | Gate misses |
|---|---|---|---|
| A | FAIL | 1 | 26 |
| B | FAIL | 1 | 19 |
| C | FAIL | 1 | 27 |

### Slip A: 26 misses

Source: `runs/2026-11-05_JAX@BAL_r6/gate_A/gate_output.txt:7`. 2026-11-04 15:57 ET evaluation.

- leg JAX 1H -6.5: phases [2, 4, 6, 7, 9, 10, 12, 14, 15] flagged FAIL/MISSING/STALE/UNVERIFIED/HOLD but leg not CUT/HOLD
- leg JAX 1H -6.5: has flagged gaps ['UNVERIFIED monte_carlo pricing for JAX 1H -6.5', 'UNVERIFIED bias pricing for JAX 1H -6.5', 'UNVERIFIED game_randomness pricing for JAX 1H -6.5'] but leg not CUT
- leg Strange 4+ rec (o3.5): phases [4, 9, 12, 15] flagged FAIL/MISSING/STALE/UNVERIFIED/HOLD but leg not CUT/HOLD
- leg Strange 4+ rec (o3.5): has flagged gaps ['MISSING coverage.man_zone numeric rates', 'MISSING coverage.mof numeric rates', 'MISSING pressure_inputs.time_to_throw'] but leg not CUT
- leg Washington rec yds o63.5: phases [2, 4, 7, 9, 12, 13, 14, 15] flagged FAIL/MISSING/STALE/UNVERIFIED/HOLD but leg not CUT/HOLD
- leg Washington rec yds o63.5: has flagged gaps ['MISSING coverage.man_zone numeric rates', 'MISSING coverage.mof numeric rates', 'MISSING pressure_inputs.time_to_throw'] but leg not CUT
- leg Henry 40+ rush (o39.5): phases [3, 6, 7, 9, 10, 12, 13, 14, 15] flagged FAIL/MISSING/STALE/UNVERIFIED/HOLD but leg not CUT/HOLD
- leg Henry 40+ rush (o39.5): has flagged gaps ['MISSING recent_form: fewer than three games with current QB'] but leg not CUT
- category ngs gap flagged but legs ['Henry 40+ rush (o39.5)', 'JAX 1H -6.5', 'Strange 4+ rec (o3.5)', 'Washington rec yds o63.5'] not CUT
- leg Henry 40+ rush (o39.5): edge-rule inputs missing (need no_vig, line, side, 3 model p)
- leg JAX 1H -6.5: edge avg(p)-no_vig = -6.9 pts < +3
- leg JAX 1H -6.5: edge a model p 0.414 < .45
- leg JAX 1H -6.5: edge sim median 5.0 does not clear over 6.5
- leg JAX 1H -6.5: edge sim median 4.0 does not clear over 6.5
- leg JAX 1H -6.5: edge sim median 4.0 does not clear over 6.5
- leg JAX 1H -6.5: §7 FAIL over 6.5 hit 2 of 4 last games with current QB [10, -7, -3, 28]
- leg Washington rec yds o63.5: edge avg(p)-no_vig = -8.7 pts < +3
- leg Washington rec yds o63.5: edge a model p 0.417 < .45
- leg Washington rec yds o63.5: edge sim median 54.931037421680244 does not clear over 63.5
- leg Washington rec yds o63.5: edge sim median 54.931037421680244 does not clear over 63.5
- leg Washington rec yds o63.5: edge sim median 53.14267525703374 does not clear over 63.5
- leg Washington rec yds o63.5: §7 FAIL over 63.5 hit 2 of 4 last games with current QB [7, 124, 64, 16]
- leg Washington rec yds o63.5: §14 FAIL at -114 last-4 median 40.0 < 25% over line 63.5 (need 79.4)
- leg Washington rec yds o63.5: §14 FAIL at -114 cleared line by 10%+ (69.9) in only 1 of 4
- leg Strange 4+ rec (o3.5): N2 no verified primary defender (receiving legs can't go on a slip without one; WR3 team-profile fallback no longer enough)
- leg Washington rec yds o63.5: N2 no verified primary defender (receiving legs can't go on a slip without one; WR3 team-profile fallback no longer enough)

### Slip B: 19 misses

Source: `runs/2026-11-05_JAX@BAL_r6/gate_B/gate_output.txt:7`. 2026-11-04 15:57 ET evaluation.

- leg Henry 40+ rush (o39.5): phases [3, 6, 7, 9, 10, 12, 13, 14, 15] flagged FAIL/MISSING/STALE/UNVERIFIED/HOLD but leg not CUT/HOLD
- leg Henry 40+ rush (o39.5): has flagged gaps ['MISSING recent_form: fewer than three games with current QB'] but leg not CUT
- leg Strange 40+ rec yds (o39.5): phases [2, 4, 9, 12, 14, 15] flagged FAIL/MISSING/STALE/UNVERIFIED/HOLD but leg not CUT/HOLD
- leg Strange 40+ rec yds (o39.5): has flagged gaps ['MISSING coverage.man_zone numeric rates', 'MISSING coverage.mof numeric rates', 'MISSING pressure_inputs.time_to_throw'] but leg not CUT
- leg Strange 4+ rec (o3.5): phases [4, 9, 12, 15] flagged FAIL/MISSING/STALE/UNVERIFIED/HOLD but leg not CUT/HOLD
- leg Strange 4+ rec (o3.5): has flagged gaps ['MISSING coverage.man_zone numeric rates', 'MISSING coverage.mof numeric rates', 'MISSING pressure_inputs.time_to_throw'] but leg not CUT
- leg JAX 1H -6.5: phases [2, 4, 6, 7, 9, 10, 12, 14, 15] flagged FAIL/MISSING/STALE/UNVERIFIED/HOLD but leg not CUT/HOLD
- leg JAX 1H -6.5: has flagged gaps ['UNVERIFIED monte_carlo pricing for JAX 1H -6.5', 'UNVERIFIED bias pricing for JAX 1H -6.5', 'UNVERIFIED game_randomness pricing for JAX 1H -6.5'] but leg not CUT
- category ngs gap flagged but legs ['Henry 40+ rush (o39.5)', 'JAX 1H -6.5', 'Strange 4+ rec (o3.5)', 'Strange 40+ rec yds (o39.5)'] not CUT
- leg Henry 40+ rush (o39.5): edge-rule inputs missing (need no_vig, line, side, 3 model p)
- leg JAX 1H -6.5: edge avg(p)-no_vig = -6.9 pts < +3
- leg JAX 1H -6.5: edge a model p 0.414 < .45
- leg JAX 1H -6.5: edge sim median 5.0 does not clear over 6.5
- leg JAX 1H -6.5: edge sim median 4.0 does not clear over 6.5
- leg JAX 1H -6.5: edge sim median 4.0 does not clear over 6.5
- leg JAX 1H -6.5: §7 FAIL over 6.5 hit 2 of 4 last games with current QB [10, -7, -3, 28]
- leg Strange 40+ rec yds (o39.5): edge-rule inputs missing (need no_vig, line, side, 3 model p)
- leg Strange 4+ rec (o3.5): N2 no verified primary defender (receiving legs can't go on a slip without one; WR3 team-profile fallback no longer enough)
- leg Strange 40+ rec yds (o39.5): N2 no verified primary defender (receiving legs can't go on a slip without one; WR3 team-profile fallback no longer enough)

### Slip C: 27 misses

Source: `runs/2026-11-05_JAX@BAL_r6/gate_C/gate_output.txt:7`. 2026-11-04 15:57 ET evaluation.

- leg JAX 1H -6.5: phases [2, 4, 6, 7, 9, 10, 12, 14, 15] flagged FAIL/MISSING/STALE/UNVERIFIED/HOLD but leg not CUT/HOLD
- leg JAX 1H -6.5: has flagged gaps ['UNVERIFIED monte_carlo pricing for JAX 1H -6.5', 'UNVERIFIED bias pricing for JAX 1H -6.5', 'UNVERIFIED game_randomness pricing for JAX 1H -6.5'] but leg not CUT
- leg Henry 40+ rush (o39.5): phases [3, 6, 7, 9, 10, 12, 13, 14, 15] flagged FAIL/MISSING/STALE/UNVERIFIED/HOLD but leg not CUT/HOLD
- leg Henry 40+ rush (o39.5): has flagged gaps ['MISSING recent_form: fewer than three games with current QB'] but leg not CUT
- leg Washington rec yds o63.5: phases [2, 4, 7, 9, 12, 13, 14, 15] flagged FAIL/MISSING/STALE/UNVERIFIED/HOLD but leg not CUT/HOLD
- leg Washington rec yds o63.5: has flagged gaps ['MISSING coverage.man_zone numeric rates', 'MISSING coverage.mof numeric rates', 'MISSING pressure_inputs.time_to_throw'] but leg not CUT
- leg Strange 40+ rec yds (o39.5): phases [2, 4, 9, 12, 14, 15] flagged FAIL/MISSING/STALE/UNVERIFIED/HOLD but leg not CUT/HOLD
- leg Strange 40+ rec yds (o39.5): has flagged gaps ['MISSING coverage.man_zone numeric rates', 'MISSING coverage.mof numeric rates', 'MISSING pressure_inputs.time_to_throw'] but leg not CUT
- category ngs gap flagged but legs ['Henry 40+ rush (o39.5)', 'JAX 1H -6.5', 'Strange 40+ rec yds (o39.5)', 'Washington rec yds o63.5'] not CUT
- leg Henry 40+ rush (o39.5): edge-rule inputs missing (need no_vig, line, side, 3 model p)
- leg JAX 1H -6.5: edge avg(p)-no_vig = -6.9 pts < +3
- leg JAX 1H -6.5: edge a model p 0.414 < .45
- leg JAX 1H -6.5: edge sim median 5.0 does not clear over 6.5
- leg JAX 1H -6.5: edge sim median 4.0 does not clear over 6.5
- leg JAX 1H -6.5: edge sim median 4.0 does not clear over 6.5
- leg JAX 1H -6.5: §7 FAIL over 6.5 hit 2 of 4 last games with current QB [10, -7, -3, 28]
- leg Strange 40+ rec yds (o39.5): edge-rule inputs missing (need no_vig, line, side, 3 model p)
- leg Washington rec yds o63.5: edge avg(p)-no_vig = -8.7 pts < +3
- leg Washington rec yds o63.5: edge a model p 0.417 < .45
- leg Washington rec yds o63.5: edge sim median 54.931037421680244 does not clear over 63.5
- leg Washington rec yds o63.5: edge sim median 54.931037421680244 does not clear over 63.5
- leg Washington rec yds o63.5: edge sim median 53.14267525703374 does not clear over 63.5
- leg Washington rec yds o63.5: §7 FAIL over 63.5 hit 2 of 4 last games with current QB [7, 124, 64, 16]
- leg Washington rec yds o63.5: §14 FAIL at -114 last-4 median 40.0 < 25% over line 63.5 (need 79.4)
- leg Washington rec yds o63.5: §14 FAIL at -114 cleared line by 10%+ (69.9) in only 1 of 4
- leg Strange 40+ rec yds (o39.5): N2 no verified primary defender (receiving legs can't go on a slip without one; WR3 team-profile fallback no longer enough)
- leg Washington rec yds o63.5: N2 no verified primary defender (receiving legs can't go on a slip without one; WR3 team-profile fallback no longer enough)
