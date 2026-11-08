# 15-phase nfl-game-script-run — ENGINEERING market/calibration task
**Game/slate:** N/A — adapter build for shared sim market matching (not a kickoff card)
**Kickoff:** N/A
**Pulled_et:** 2026-11-06 06:20 ET
**Input cutoff for quotes used:** historical cached r6 pulls (2026-11-04 ~14:59–15:00 ET) + cleared FD/DK grades files (2026-11-05 night)
**Checklist path:** this file
**Brainstorm:** loaded `betting-game-brainstorm` before this checklist; engineering task → no edge sentence / no legs (see Phase notes).

## Source map log (actual attempts)
See `SOURCE_INVENTORY_2026-11-06.md`. Summary:
| Source | Attempt | Status |
|---|---|---|
| ESPN | LIVE curl homepage | SUCCESS http 200 |
| nflverse | LIVE github page | SUCCESS http 200 |
| PFR | LIVE curl homepage | LIVE_HTTP_403 (blocked to curl; cached PFR copies elsewhere not re-pulled this turn) |
| NGS | LIVE curl | SUCCESS http 200 |
| PFF | LIVE curl public | SUCCESS http 200 (paid grades NOT pulled) |
| FanDuel | LIVE curl | LIVE_HTTP_403 shell; **CACHED** FD quotes used from r6/cleared CSVs |
| DraftKings | LIVE curl | SUCCESS http 200; **CACHED** DK quotes used |
| Pinnacle | LIVE curl | SUCCESS http 200; **CACHED** Pin Q1/H1+team_totals; Q2–Q4 spreads **NOLINE** |
| Odds API | env key SET; **no network call** (budget/no-history policy) | NOLINE_NEW_PULL_BY_POLICY |

## Phase rows (engineering — explicit N/A where not a projected leg)

| Scope | Phase | Status | Number / note | Source | Pulled (ET) |
|---|---|---|---|---|---|
| ENG-adapter | 1 Data pull/reconcile | PASS (partial) | Saved FD/DK/Pin CSVs loaded by matcher; no new Odds API pull | cached r6 + cleared CSVs | 2026-11-06 06:20 |
| ENG-adapter | 2 Opportunity gate | N/A | No player leg; engineering market/calib package | — | — |
| ENG-adapter | 3 Defensive profile | N/A | No projected receiving/rushing leg this task | — | — |
| ENG-adapter | 4 Defender coverage | N/A | No WR/TE/RB receiving leg; defender evidence not invented | — | — |
| ENG-adapter | 5 Pressure/blitz | N/A | No QB/receiver leg | — | — |
| ENG-adapter | 6 QB grade card | N/A | No slate QB pricing this task | — | — |
| ENG-adapter | 7 Role/RB rules | N/A | No RB market this task | — | — |
| ENG-adapter | 8 Injuries | N/A | Engineering; injury recheck belongs to live game runs | — | — |
| ENG-adapter | 9 NGS | N/A | Route/sep not required for quote matcher unit tests | NGS live probe 200 only | 06:20 |
| ENG-adapter | 10 Film | N/A | No film claims | — | — |
| ENG-adapter | 11 Environment | N/A | No open-air kickoff card | — | — |
| ENG-adapter | 12 Source audit | PASS | Inventory file written; cached vs live distinguished; Pin Q2–Q4 NOLINE logged | SOURCE_INVENTORY_*.md | 06:20 |
| ENG-adapter | 13 Script/underdog gate | N/A | No underdog legs | — | — |
| ENG-adapter | 14 Models/price/edge | PASS (plumbing) / NOT MEASURED (edge) | Matcher + no-vig helpers + settlement; 100k MC/Bias/GR **not** re-run this engineering pass (policy: no heavy local sims). Bias status UNIMPLEMENTED_NO_FITTED_CALIB. Raw vs anchored separate. | market_calibration tests 93 passed | 06:20 parent verify |
| ENG-adapter | 15 Inactives | N/A | No live card; TNF already final | — | — |

### Summary
- Legs published: **0** (engineering only)
- CUT: n/a
- Gaps: PFR/FD LIVE curl 403; Odds API no new pull; Pin Q2–Q4 period spreads NOLINE in cached set; Bias unfitted; Blitz core opportunity model still separate
- Seeds/sims: unit tests only; no 100k forecast claim
- Mismatch hypotheses (beyond averages): identity/line/period/time cutoff mismatches → NOLINE; one-sided books → NOLINE; TNF-as-holdout forbidden; raw≠anchored without shared identity
- Defender evidence: **not invented**

VETTED: pending Ghost6 final integrated vet (BetGuru parent handoff)
