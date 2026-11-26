# W12 Thanksgiving pristine lock — status

- Checked: `2026-11-26T12:48:26+00:00`
- Branch: `cursor/w12-thanksgiving-locks-9aff` @ `32a7937f2839`
- CHI@DET decision: **NO_LOCK_YET** — Waiting for T-90 official inactives; remaining blockers after prewarm listed in refusal_reasons
- Kickoff: 2026-11-26T18:00:00+00:00; T-90: 2026-11-26T16:30:00+00:00; window open: 2026-11-26T16:32:00+00:00

## Gate summary

| Gate | Status |
|---|---|
| G0_entrypoint | PASS |
| G1_flags | PASS |
| G2_nfl43 | PASS |
| G3_packet | PASS |
| G4_freshness | REFUSED |
| G5_phases | REFUSED |
| G7_asof | PASS |
| G6_rocket | NOT_RUN (earlier gates refused) |

## Remaining refusals

- G4: ftn_charting GAP: latest published asset (as-of 2026-11-26T00:02:05+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.
- G4: pfr_defense GAP: latest published asset (as-of 2026-11-26T12:02:42+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.
- G4: official_inactives NOT_YET: Inactives post about Thu 11:30 AM ET (T-90); not available yet.
- G5: phase 7 (Coverage structure and shell) is GAP
- G5: phase 8 (Defender assignment and explosive allowance) is GAP
- G5: phase 9 (QB pressure, blitz, scramble) is GAP
- G5: phase 15 (Final inactive pregame freeze) is NOT_YET

## Notes

- GB@LAR FINAL — will not lock retroactively.
- FTN charting / PFR defense GAP on completed `2026_12_GB_LA` may keep `pipeline.sim100k` REFUSED even after T-90; `snapshots.lock` asof gates currently PASS (same pattern as W11 CIN@WAS).
- Timer subscribed to resume at ~16:28Z.
