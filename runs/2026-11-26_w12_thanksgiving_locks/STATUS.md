# W12 Thanksgiving pristine lock — status

- Checked: `2026-11-26T13:08:22+00:00` (08:08 AM America/New_York)
- Branch: `cursor/w12-thanksgiving-locks-9aff`
- CHI@DET decision: **NO_LOCK_YET** — Waiting for T-90 official inactives; FTN/PFR GAP for `2026_12_GB_LA` may still refuse after T-90
- Kickoff: 2026-11-26T18:00:00+00:00; T-90: 2026-11-26T16:30:00+00:00; window open: 2026-11-26T16:32:00+00:00
- Parent agent timer: `chi-det-t90-lock` (~16:48Z one-shot). Sibling [Lock CHI DET 100k](bc-0f93f51b-605f-5bdd-b832-d378801c419e) also scheduled ~16:28Z.

## Gate summary (post sportsbooks + freeze refresh)

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

- G4: ftn_charting GAP: missing completed `2026_12_GB_LA` (publisher max week 11)
- G4: pfr_defense GAP: same
- G4: official_inactives NOT_YET (~Thu 11:30 AM ET / T-90)
- G5: phases 7/8/9 GAP; phase 15 NOT_YET

## Cleared by prewarm

- Odds / four_book_prices: freeze `freeze_20261126T124745Z.json` pulled `2026-11-26T12:42:59Z`
- nflverse digest match after packet rebuild

## Notes

- GB@LAR FINAL — will not lock retroactively.
- Do not invent a lock under GAP. Re-check nflverse FTN/PFR assets at T-90.
- See `W12_ELIGIBILITY.md` for full slate table.
