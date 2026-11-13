VERDICT: REQUEST CHANGES

1. **P1 must-fix — Pass-1 finding 1 NOT RESOLVED — [simulate.py:873](/tmp/wt-rare-plays/core/possession_engine_v0/simulate.py:873).** Automatic-first-down inference mistakes an ordinary defensive foul on historical first down for an automatic first down. The committed pool contains a field-goal-formation row starting at first-and-10, gaining five yards, and remaining first-and-5. Applied at live fourth-and-8, it incorrectly awards first-and-10. Require evidence that the historical foul actually reset the down. The fake-play portion is resolved.

2. **P2 should-fix — Pass-1 finding 2 NOT RESOLVED — [simulate.py:951](/tmp/wt-rare-plays/core/possession_engine_v0/simulate.py:951).** LOS bands reduce translation error but do not preserve boundary enforcement, even within the narrowest band. The committed punt outcome from LOS 67 with receiving spot 90 and shift 57 produces spot 89 from live LOS 68. This error occurs without clipping; the unrestricted fallback also retains the original large-error cases. The declared residual-clipping limitation therefore does not adequately describe or resolve the problem. Preserve boundary/enforcement information when applying these outcomes.

3. **P2 — Pass-1 finding 3 RESOLVED — [rare_plays.py:332](/tmp/wt-rare-plays/core/possession_engine_v0/rare_plays.py:332).** The clean punt return-TD denominator now excludes touchbacks and punts into the end zone; an empty population remains unknown.

4. **P2 — Pass-1 finding 4 RESOLVED — [simulate.py:1457](/tmp/wt-rare-plays/core/possession_engine_v0/simulate.py:1457), [simulate.py:1049](/tmp/wt-rare-plays/core/possession_engine_v0/simulate.py:1049).** Direct attachment requires a validated research count, and simulation consumes the model’s budget and refuses further games at zero.

Validation: **31 tests passed**, including off-mode golden reproduction. No files modified or network used.