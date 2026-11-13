VERDICT: APPROVE

1. **Pass-3 P3 — RESOLVED — `simulate.py:1280,1345`.** Results aggregate kind/class/band counts and `all|all|band` totals, explicitly disclose that whole-pool fallback has no distance bound, and omit both new keys when rare mode is off.

2. **Punt-rate pooling — SOUND — `rare_plays.py:338–359`.** Verified **25/7,840 = 0.3189%**, versus current-season **0/866**. Pooling matches the formation-rate population, retains the eligible non-touchback denominator, excludes flagged/blocked punts, and preserves point-in-time filtering and provenance. Keeping non-onside kickoff rates current-season is consistent with the kickoff-era distinction.

3. **Earlier P1/P2 findings — status unchanged.** Live down/distance handling, return-TD denominators, and research-budget enforcement remain resolved. Boundary enforcement outside exact-LOS matches remains an accepted, disclosed research limitation; this approval does not establish lock readiness.

No new actionable findings. **33 targeted tests passed**, including off-mode golden reproduction. No files modified or network used.