# TNF JAX@BAL post-inactives check — 2026-11-05 ~7:02 PM ET
Routine: TNF JAX@BAL post-inactives check (Nov 5). Read only. No bets placed. Gates = flags only; Rico decides.

## Official inactives (~6:52–6:55 PM ET)
Sources: [@Jaguars](https://x.com/i/status/2118489818074144804) / [@JaguarsPR](https://x.com/i/status/2118489901088075894); [@Ravens](https://x.com/i/status/2118490642632655307). Graphics saved under `runs/2026-11-05_JAX_BAL/inactives/`.

**JAX inactive:** WR C.J. Williams, CB Alijah Huzzie, S Cam'Ron Silmon-Craig, DE Wesley Williams.
**JAX ACTIVE (were Q):** RB Bhayshul Tuten, DE Travon Walker, WR Jakobi Meyers.

**BAL inactive:** CB Nate Wiggins, WR Elijah Sarratt, FS Jaylinn Hawkins, G Emery Jones, DT Aeneas Peebles, QB Kedon Slovis (3rd QB).
**BAL QB:** Joe Fagnano starts; Austin Reed is No. 2.

## Rule triggers from this routine
- **Tuten OUT?** No — Tuten is **ACTIVE**. Short-throw redistribution to other backs (not Strange) does **not** fire.
- **Wiggins OUT?** Yes. **Chidobe Awuzie** is the conditional matchup on Parker Washington (FLAG only).
- Hawkins already out (3rd straight) — middle/seam help for Strange still on.

## FanDuel reprice (pull ~7:02 PM ET, 14 credits, remaining 2346)
File: `odds/odds_post_inactives_fd_2026-11-05_1902.csv` (vs noon live FD + Nov 4 r6).

| Leg (Rico proposed / r6) | Noon FD | Now FD | Note |
|---|---:|---:|---|
| Strange 40+ rec yds | +116 | **+122** | juice improved |
| Strange 4+ rec (o3.5) | −122 | **−108** | juice improved |
| Washington 40+ yds | −340 | **−310** | still −130-cap heavy |
| Washington o63.5 | −114 (r6) | **NO_QUOTE** | main moved to **60.5 −113** |
| Henry U69.5 | −114 (r6) | **NO_QUOTE at 69.5** | main moved to **U71.5 −113**; alt O69.5 −120 |
| Henry 40+ | −700 (r6) | **−580** | still −130-cap |
| Meyers 25+ yds | −270 | −270 | flat vs noon |
| Hill 2+ rec | −300 | **−340** | juice worse |
| Andrews 2+ rec | −390 | **−400** | juice worse |
| Flowers U4.5 | −130 | **−114** | juice improved |
| Bateman U15.5 | — | **NO_QUOTE** | main **U12.5 −113**; alt O14.5 +104 |
| BAL TT Under | U13.5 −108 | **U14.5 −120** | number up 1 |
| JAX 1H −6.5 | −105 | **+100** | better |
| JAX 1Q −2.5 | −124 | **−120** | slight better |
| Game total 39.5 | — | O−115 / U−105 | |
| Spread | — | JAX −9.5 −110 | |

Tuten rush main now posted: **61.5 −113** (was NOLINE while Q). Not on Rico proposed cards.

## Weather (from Phase 15 6:55 PM NWS)
Kickoff hour precip **~76%**. Receiving overs on proposed Slips A/B stay **weather FLAG**. Rush/under legs not weather-cut.

## Proposed 3×4 impact (slips_rico_3/PROPOSED.md) — flags only
- **Slip A** (Strange 40+ / Wash 40+ / JAX 1H / Andrews 2+): Wiggins OUT mildly helps Washington/Strange overs via Awuzie matchup FLAG; weather still flags receiving overs. Strange 40+ price better (+122). Andrews 2+ slightly worse (−400).
- **Slip B** (Meyers 25+ / Hill 2+ / Henry under / JAX 1Q): Meyers ACTIVE confirms. Henry under must use **U71.5 −113** (69.5 gone). Hill 2+ juice worse. Tuten ACTIVE means no short-throw shift into Hill/Rodriguez from the Tuten-out rule.
- **Slip C** (Flowers U4.5 / Bateman under / BAL TT U / game U39.5): Flowers under juice better (−114). Bateman line down to 12.5. BAL TT now **U14.5 −120**.

## assemble.py
Re-ran `python3 runs/2026-11-05_JAX@BAL_r6/assemble.py --now 2026-11-05T19:02` after this pull. See `proactive/assemble_post_inactives_1902.log` and gate_A/B/C outputs.

## Disposition
No bets placed. No auto-cuts. Rico decides overrides / swaps.
