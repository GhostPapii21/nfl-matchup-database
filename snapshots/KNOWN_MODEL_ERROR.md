# Known model error: 100k locks made before NFL-43 bounds review

**Research only, not validated.** Added 2026-11-12 (BetGuru) after Ghost6's PR #19 review (commit d65ad98,
`docs/ACCEPTANCE_STATUS.md`, about 12:45 PM ET), which did not accept the NFL-43 bounds.

| Lock | Status | Why it is known model error |
|---|---|---|
| `snapshots/2026_10_WAS_NYG/20261112T171258Z/` (TNF, commit 8c2e602) | committed, kept for scoring | Ran under unreviewed NFL-43 bounds (c4c5616 un-deferred 100k before review), with head-to-head-only defense conditioning (100% of snaps drawn from the single W5 27-27 game) and the old two-team defensive-return path (0 defensive TDs over 100k) |
| `snapshots/2026_10_BUF_NYJ/20261112T172055Z/` (commit 08b8cee) | committed, kept for scoring | Same: unreviewed bounds, h2h conditioning, old defensive-return path |
| `snapshots/2026_10_CAR_NO/20261112T173412Z/` | **left uncommitted on purpose** (local only) | Same; the Sunday lock run was paused, not published |

These locks stay frozen (their hashes are their value as a pre-registration record) and will be scored, but their
outputs are not evidence of an edge. `rocket` R5 reports each as `KNOWN_MODEL_ERROR_UNREVIEWED_BOUNDS` because their
LOCK.json has no `nfl43_review: "ACCEPTED"`. No further 100k lock can run: `snapshots/lock.py`, `pipeline/sim100k.py`
(G1/G2) and `rocket` (R2) all refuse while `known_flags/NFL43_REVIEW.json` is not ACCEPTED or `DEFERRED_100K` is true.

Diagnosis: `core/possession_engine_v0/SEMANTICS_BOUNDS.md` section 5 and `bounds/sensitivity_was_nyg_w10.json`
(DIAG arm with h2h conditioning off: NYG 15.68 / WAS 17.48, P(NYG win) 0.439, n = 6,000).
