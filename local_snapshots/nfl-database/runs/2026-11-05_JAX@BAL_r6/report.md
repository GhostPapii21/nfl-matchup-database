# r6: TNF JAX@BAL price re-pull + Rico 4-leg slip (2026-11-04, pulled 14:59 ET)
Go: Rico via Ghost6, 2026-11-04 14:59 ET. A single event-odds pull (pull_r6.py) covering FD/DK/Pinnacle and 12 markets. **Credits used: 12** (x-requests-last). **3,527 remaining.**
There's no sack market from the API (Fagnano sacks = NO_QUOTE), no 1H player-yards market (Strange 1H yds = NO_QUOTE), and Fagnano INT is DK only.
Gates: §7 3-of-4 (last 4 played), last-2 = downgrade only, N1, best price. Tiers and edges are FLAGS only. Model p = r2 sim mean (raw, not anchored); NONE when that line wasn't simulated. Product-of-singles pricing; the FD SGP will differ.
Files: prop_legs_r6.csv, game_legs.csv, game_lines_out.txt, odds/odds_r6.csv.

## Rico 4-leg slip
| leg | best | FD | no-vig | model p | §7 | last-2 | flags |
|---|---|---|---|---|---|---|---|
| Strange 4+ rec (o3.5) | Pin -119 | -122 | .515 Pin | .550 | PASS 3/4 [7,7,5,2] | DOWNGRADE (2 in Wk8) | |
| Washington rec yds o63.5 | FD -114 | -114 | .506 Pin | .422 | **FAIL 2/4** both windows | OK no-Wk8 / DOWN w/ Wk8 | needs Rico override; model opposes (-8.4 raw) |
| JAX 1H -6.5 | Pin -101 | -110 | .488 Pin | NONE (no game model) | **FAIL 2/4** [10,-7,-3,28] | DOWNGRADE | needs Rico override (same as r5) |
| Henry 40+ rush (o39.5) | DK -598 | -700 | no two-way | NONE | PASS 4/4 [102,58,45,53] | OK | N1 OK (76/89/68/65% carries); would hit the -130 cap (not approved) |
Product: best books **+702** (8.03); FD-only **+645**. Swapping in Strange 40+ yds (FD +114, 4/4, last-2 OK) gives +833 / FD +776.
Strange 1H yds: NO_QUOTE (last 4 1H yds [49,27,29,55], for reference).
Washington alts: only o39.5 and lower (and 3+ rec) pass, and only on the no-Wk8 window; with Wk8 nothing offered passes. o39.5 is DK -346 / FD -360 and hits the -130 cap.

## Other priced legs: see prop_legs_r6.csv and game_legs.csv. Wed ~5 PM injury report not yet out at write time.

## Follow-up (15:05 ET): run_gate.py on slips A/B/C + 1H miss audit
- Adapter folders gate_A/B/C (gate_adapter.py) with real r6 data only. **run_gate.py stamp: FAIL (exit 1) on A, B and C**, 92 misses each: JAX@BAL never had the 15-phase checklist, coverage/NGS/film/injury/weather sources, pressure inputs, sim_v6 100k sims, wr/te_rank, primary defender (N2), 1H game-script read (N3), or weather blocks.
- §11: run_gate.py has no one-slip-per-player check (only a STOP regex in rico4_rules.py). B (Strange twice) was **not** flagged; this needs a manual call.
- Miss audit: miss_audit_1H.md
