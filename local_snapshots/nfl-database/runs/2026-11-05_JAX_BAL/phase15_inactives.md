# Phase 15: Inactives + reprice — TNF JAX @ BAL, 2026-11-05 8:15 PM ET
Pulled: 2026-11-05 18:56 ET. Read only. No bets placed.

## Official inactives (posted ~6:52–6:55 PM ET)

**JAX** ([@JaguarsPR](https://x.com/i/status/2118489901088075894); graphic [@Jaguars](https://x.com/i/status/2118489818074144804)):
- WR CJ Williams
- CB Alijah Huzzie
- S Cam'Ron Silmon-Craig
- DE Wesley Williams

**Confirmed ACTIVE (were Q):** RB Bhayshul Tuten (ankle), DE Travon Walker (ribs), WR Jakobi Meyers. ([TravisDHolmes](https://x.com/TravisDHolmes/status/2118491933072850992); ESPN roster `didNotPlay=false`)

**BAL** ([@Ravens](https://x.com/i/status/2118490642632655307); [jeffzrebiec](https://x.com/i/status/2118490938641121435); [jamisonhensley](https://x.com/i/status/2118491251733373010)):
- CB Nate Wiggins (stinger/illness) — was Q
- S Jaylinn Hawkins (knee) — 3rd straight miss
- WR Elijah Sarratt
- G Emery Jones Jr.
- DT Aeneas Peebles
- QB Kedon Slovis (3rd QB)

**QB:** Joe Fagnano starts; Austin Reed (signed Mon) is No. 2 behind Fagnano (Slovis inactive). Lamar/Huntley remain IR.

Raw: `inactives/espn_summary_401873037.json`, `espn_bal_roster.json`, `espn_jax_roster.json`, `ravens_inactives.jpg`, `jaguars_inactives.png`, `nws_hourly_p15.json`.

## User tickets / exposure
- **No user-placed TNF tickets** found in `week8/slips/`, `week10/`, or `runs/2026-11-05_*` (gate report also: none found). Proposed slips only: `runs/2026-11-05_JAX@BAL_r6/slips_rico_3/PROPOSED.md` (not placed).
- **No Questionable-on-ticket trigger** → stay quiet with Rico.
- Week 8 Kenneth Walker III 80+ rush+rec (KC@DEN Nov 1) is **past** — N/A this run.
- Placed RB exposure this game: **0**.

## Backfield-split check (Phase 15 rule when starter status flips)
### JAX
- **Tuten ACTIVE** and listed as ESPN starter (jersey 33). FD now posts rush main **61.5 -113** (was NOLINE while Q).
- Depth: Chris Rodriguez Jr. has FD alts (9.5/14.5); no Etienne/Bigsby rush main in this pull. Checklist L4 carry share Tuten 74/100/52/57% → still only 2 of 4 at 60%+ (Phase 7 fail remains).
- Beat: no late report of a committee flip; Tuten expected lead if healthy (active confirms).
- **Impact:** Tuten rush over candidate HELPED (active + line up) but stays CUT on Phase 7 carry-share + prior gate. Not on any placed ticket. Backup if anyone needed a Tuten swap: Rodriguez Jr. alts only (thin).

### BAL
- Henry ACTIVE, ESPN starter. Hill ACTIVE (backup/receiving). Fagnano era still 1-game sample.
- Henry U71.5 stays CUT (§7 MISSING + MODEL-SUSPECT). No placed Henry leg.

## Live / checklist leg impacts

| Leg | Prior | Inactives impact | Reprice | Phase 15 |
|-----|-------|------------------|---------|----------|
| Lawrence rush U12.5 | LIVE PASS (HOLD P15) | Unchanged — Lawrence ACTIVE; Wiggins OUT N/A to rush under | FD 12.5 U -113 / O -113 (same as 16:49); Pin 12.5 -110/-110; DK 12.5 U -110. **No move >0.5 yd or 20¢** → no P14 reprice | **PASS** |
| Henry rush U71.5 | CUT | Henry ACTIVE; unchanged cut reasons | FD 71.5 -113/-113 | N/A (CUT) |
| Meyers rec U38.5 | CUT | Meyers ACTIVE; Wiggins OUT mildly helps WR overs vs BAL (not this under) | (not required) | N/A |
| Strange rec O32.5 / 4+ | CUT weather | Wiggins OUT = depleted CB help for overs, but **WEATHER still CUTS receiving overs** (NWS kickoff precip 76%) | — | N/A |
| Washington rec O60.5 | CUT weather | same as Strange | — | N/A |
| Flowers rec U4.5 | CUT §7 | Flowers ACTIVE; Fagnano still 1-game | — | N/A |
| Tuten rush O | CUT NOLINE+share | **ACTIVE**; line now FD 61.5 | line appeared | N/A (still CUT Phase 7) |
| Game lines | CUT no model | Wiggins OUT slight BAL D hit; Fagnano confirmed | FD JAX -9.5 -110 (was -120); total 39.5 O-115/U-105 | N/A |

## Weather recheck (SRC-1 NWS hourly, 2026-11-05 18:56 ET)
- Kickoff hour 8 PM ET: Showers/T-storms, **precip 76%**, wind 5 mph S, gusts not ≥20. Window 8–9 PM still 75–76%.
- **WEATHER FLAG HOLD.** Receiving overs stay cut. Rush/under legs not wx-cut.

## Odds pull
- File: `odds/odds_p15_1855.csv` (+ meta). Cost 9 credits; remaining ~2360.
- CLV open ref unchanged: FD Lawrence 12.5 -113 at 16:49; close still 12.5 -113 at 18:55.

## Flags for Ghost6
1. Live leg **Lawrence rush U12.5** Phase 15 **PASS** — price stable, player active, weather helps script (rain + big spread → kneels).
2. **SCRAMBLE_CONFLICT / MARKET_GAP** flags from afternoon run unchanged (not cuts).
3. **Wiggins OUT** → BAL secondary thinner (Awuzie likely RCB); would help Strange/Washington/Meyers overs if weather cleared — it has not.
4. **Tuten ACTIVE + FD 61.5** — watch only; Phase 7 still fails; no placed exposure.
5. Proposed slips A/B receiving overs remain weather-blocked; do not promote without Rico override.
6. No user swap needed.

## Recommended gate note
Update checklist Phase 15 Lawrence row HOLD → PASS. Re-run `tools/run_gate.py` optional (P15 was the only miss).

## Gate re-check
GATE: PASS at 2026-11-05 18:57 ET after odds_p15_1855 stamped into run_manifest. Output: gate_output_p15.txt
