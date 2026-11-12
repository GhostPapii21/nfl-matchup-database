# BetGuru — PHASE 5 — IMMUTABLE OUTPUT AND DATABASE HISTORY (Sun Nov 1, 2026 slate)
Written Sat Oct 31, 2026, 7:43 PM ET. Nothing placed or posted. No keys printed.

## Run folder (new, unique, read-only)
`runs/betguru_20261031T194324/` — created 7:43:24 PM ET, chmod a-w. Earlier Phase 1–4 files are copied in as-is; no earlier file was overwritten.
Append-only history: `runs/MASTER.md` (one line added for this run; earlier lines untouched).

## Locked contents
| Item | Locked artifact |
|---|---|
| Request | User 7:37 PM ET: run Phases 5–10G; separate Gibbs 60+/50+ rush and Lamb 5+ edges; 3 sims × 100k; median + no-vig edge 3–15; Ghost6 10G underdog gate; FD sbapi prices only; Ticket 2 exact-prop bar; Higgins SGP flag; Gibbs 90+ R+R (Rico) in 10G |
| Game identity | Sun Nov 1, 2026 REG week 8 (nflverse game_ids carry wk 8). Games touched: MIN@DET, BAL@BUF, KC@DEN, TEN@CIN, LAC@LAR, ARI@DAL, IND@JAX, PHI@WSH, CLE@PIT, LV@NYJ, ATL@TB |
| Conditional lineups | All pool players ACTIVE per ESPN injuries API re-pull 7:4x PM ET (`espn_inj_20261031_eve.json`): Gibbs (shoulder, full Thu), St. Brown (ankle, full Thu), Chase full, Rice no designation, Kelce no designation, Kincaid Q (BUF), Davante Adams IR (LAR). Lineups remain CONDITIONAL until Sunday inactives |
| Market snapshot | FanDuel sbapi via existing `fd_pull_all.py`, pulled 7:37:54 PM ET Oct 31 (13,137 rows) → `fd_snapshot_20261031_1937.csv`. Prior file preserved as `fd_now_prev_1937.csv`. Odds API not used (401, 0 requests) |
| Forecast | `bg_sims.json` + `bg_price_table.csv` (requested BetGuru sims — NOT outputs/nfl.py) |
| Code/spec/config/input hashes | `SHA256SUMS` (pbp e61a4040…, same file hash as Ghost6's snapshot; players, NGS ×3, GAME_SCRIPT 95d3666f…) |
| Seed / trials | base seed 20261101, per leg/model offset = md5("player|market|model")[:6]; N = 100,000 per leg per model |
| Source snapshot | nflverse pbp 2026 wks 1–7 (+wk8 TNF), NGS season rows, FD 7:37 PM, NWS hourly ~7:40 PM, ESPN injuries ~7:45 PM |

## Engine status
`outputs/nfl.py` does **not exist** on the box (checked 7:3x PM ET). Per the MODEL section: **SIMULATION NOT RUN (engine)**. The three sims below are the user-requested BetGuru sims (`sims/bg_sim.py`), UNCALIBRATED (independent calibration NOT PASSED).

## 60 required checks
`outputs/workflow_control/contract.json` is not on the box, so the 60 check IDs cannot be enumerated. Status for all 60: **UNAVAILABLE** (reason: contract file absent; `outputs/nfl.py verify` cannot run). P4.slip_comparison and P6.live_policy are the only IDs allowed NOT_APPLICABLE; P6.live_policy = NOT_APPLICABLE (see Phase 6). Nothing silently converted to PASS.

## Public export
None. No credentials, raw media or local paths published.

## Pool carried from Phase 4 (cuts applied)
Cut: Tyler Warren recyds (GAP). 24 legs carried + requested extras (Gibbs 60/50 rush, Lamb 5+, Gibbs 90+ R+R) + Ghost6 comparison legs (Flournoy 3+, Tuten 60+, A. Williams 3+; **not walked through our Phases 1–4 → comparison only, not eligible for our card**).
