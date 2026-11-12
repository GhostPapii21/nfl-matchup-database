# Ghost6 independent run — CHI @ SEA, MNF Mon Nov 2 2026, 8:15 PM ET, Lumen Field (Seattle)
Data pulled 2026-11-02 05:04–05:10 ET. Checklist: checklist.md. Sims: sim_v6, 3 models x 100,000, seed 20261101 (sims.json). Independent: no Blitz/BetGuru files for this game were opened.

## Game / market (The Odds API, FanDuel, 05:05 ET, pregame only)
SEA -3 (-120) / CHI +3 (-102); total 46.5 (-110/-110); ML SEA -178 / CHI +150.

## Weather (NWS + Open-Meteo, 05:04 ET)
Lumen Field open-air (partial roof). Precip 3%, wind 4.1 mph, gusts 4.7 mph. No flag.

## Injuries (ESPN core API, 05:05 ET)
SEA OUT: LT Charles Cross (ankle), WR Rashid Shaheed (knee), RB Velus Jones. RB Jadarian Price on IR (but FanDuel still posts a 28.5 rush line — CONFLICT, treat as inactive). QB Drew Lock Q (backup). LB Uchenna Nwosu Doubtful. Charbonnet (knee) no designation — returning.
CHI OUT: RB Kyle Monangai. IR: TE Cole Kmet, S Coby Bryant, OT Braxton Jones, DE Odeyingbo. Q: CB Malik Muhammad II, LB D'Marco Jackson. Loveland (neck) cleared.

## Team script
SEA controls via defense: allows 5.17 YPT and 3.48 YPC (both elite), so CHI is pushed toward Williams dropbacks into a 22% blitz/high-zone (90%) shell where explosives dry up. SEA moves the ball through JSN against a CHI secondary that is the softest in the matchup (8.57 YPT allowed; J. Johnson 14.4, Stevenson 11.5); CHI blitzes 41% (#4), but Darnold is positive EPA vs blitz. Close game (-3), so no RB game-script boost; Cross's absence raises sack/pressure risk on SEA dropbacks.

## Edges (avg p of 3 models vs multiplicative no-vig) — see edges_table.txt
| Leg | Price | nv | p (MC/Bias/GR) | Median | Edge | Shrunk | Models | Verdict |
|---|---|---|---|---|---|---|---|---|
| JSN o89.5 rec yds | -166 | .588 | .711/.715/.647 | 119/119/115 | +10.3 | +4.6 | 3/3 | PASS (press BLOCKED: Sharp-only coverage) |
| JSN o99.5 | -114 | .502 | .640/.642/.592 | 119 | +12.3 | +8.5 | 3/3 | CUT §14 form (L4 median 118 < 124.4) |
| JSN o79.5 | -245 | .669 | .773/.776/.708 | 119 | +8.3 | +0.7 | 2/3 | not needed; 89.5 is the rung |
| Others | | | | | | | | CUT — see below |

### Case against JSN o89.5 (pre-mortem)
- CHI blitzes 41% and SEA is missing LT Cross: sacks/hurries cut Darnold's dropbacks, and JSN's share drops when CHI blitzes (29.7% vs 33.9%).
- SEA leads early and runs (Wilson/Charbonnet) while its defense smothers CHI, so Darnold throws only ~22-26 times (he threw 22 at LAC in Wk4, when JSN had 76 yds).
- Jaylon Johnson shadows JSN, or CHI rolls two-high and gives up underneath catches only.
Survives: JSN cleared 89.5 in 3 of his last 4 games with Darnold (76, 102, 134, 150); medians 115-119; 3 of 3 models clear even at a 26% buffer. Biggest risk is low volume in a lopsided SEA lead.

## Cut legs
Odunze o38.5 (edge -1.9; SEA 5.17 YPT); Burden o51.5 (edge -4.5; Witherspoon 4.1 YPT); Swift o81.5 rush+rec (edge -5.5; SEA 3.48 YPC); Swift o49.5 rush (-10.3); Loveland o39.5 (§7 2/4, edge -19.5); Barner o24.5 (§7 1/4, -10.5); Kupp o24.5 (+0.6, #3 receiver role); JSN o6.5 receptions (§7 2/4); Wilson o19.5 (MODEL-SUSPECT median 63, sim cannot see Charbonnet's return; Rule 5 backup RB; mixed role).

## Slips
Only ONE leg passes. Main slips need 3-4 legs; padding is not allowed → **NO SLIP from this game**. JSN o89.5 (-166) is available as a single or as a leg in a cross-game slip, subject to §11.

## Bugs / data issues
1. Shared runs/2026-11-01_shared_src pbp stops at 2026-10-29 (no Nov 1 games). Fixed for this run by pulling fresh nflverse pbp (thru 11-01). Not a numbers issue for CHI/SEA (both last played Wk7), but other runs pointing at shared_src are stale.
2. sim_v6 'bias' model uses the same calibration multipliers as MC (sim_v6_calib.json mc == bias for every market), so Bias ≈ MC (identical medians). The 3-model check is effectively 2 models + GR. Not fixed (tool change needs sign-off); flagged.
3. sim_v6 uses all 7 games incl. non-current QB (Lock Wk1-2, Keenum/Bagent CHI Wk3-5); §7 recent_form uses the current QB only.
4. sim_v6 has no input for a returning RB (Charbonnet) → Wilson median 63 vs market 19.5 (MODEL-SUSPECT, cut).
5. Data conflict: J. Price is on IR per ESPN but FanDuel still lists a rush prop.
6. Sharp coverage data "Updated Oct 27" (data-through Wk7); no second public man/zone source → SRC-3 SHARP CAUTION, PRESS blocked. nflverse participation 2026 file not published (404 body).

## Risks
Inactives recheck ~6:45 PM ET (Muhammad Q, Charbonnet status, Lock Q). Re-price if JSN line moves >0.5 or 20 cents. Pressure rate is PROXY.

## Gate
`python3 tools/run_gate.py runs/2026-11-02_SEA_CHI_ghost6/ --press-tier` → GATE: PASS, exit 0 (05:08 ET). First run crashed (AttributeError) on a weather block written without a `roof` key: run_gate.check_weather crashes instead of failing closed on that shape (bug 7, gate robustness; fixed in my manifest, not in the tool). Second run failed on a film timestamp I had set ahead of the clock; corrected to the real pull time.
