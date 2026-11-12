# TNF JAX@BAL Friday automation report — 2026-11-06 ~8 AM ET
Blitz NFL Research. Quiet run. No bets. No outside messages.

## Final score and confirmation sources
- **JAX 33 – BAL 10**, finalized **2026-11-05 23:14:40 ET**
- Sources: `live/2026-11-05_JAX_BAL/FINALIZED.json` (sports-leader get_scoreboard + get_game_summary); ESPN refresh 23:12:08 ET; linescores JAX 10|7|3|13, BAL 3|0|0|7
- Live audit folder: `/workspace/nfl-database/live/2026-11-05_JAX_BAL/`

## Playlog
- Path: `/workspace/nfl-database/playlogs/2026_wk10/JAX_BAL.csv`
- Row count: **165** (Coin Toss skipped; CHI_SEA-style headers `off,q,clock,down,dist,yds,type,hs,aw,text`; hs=BAL, aw=JAX)
- Companions: `JAX_BAL_enriched.csv`, `JAX_BAL_explosives.csv`

## Ledger check output
```
LEDGER COVERAGE: OK, every logged game is in the ledger
```
- Appended 27 `JAX@BAL` rows to `defender_ledger.csv` (tackler/PBU/INT from pbp_live/ESPN text; **not coverage**). Washington 50 TD unattributed.

## Read record
- Placement: **No bets placed** (post-inactives proactive). Graded proposed only.
- Rico 4-leg (r6 report): **2-2**
- Slip A proposed: **3-1**
- Slip B proposed: **4-0**
- Slip C proposed: **3-1**
- **Aggregate proposed legs: 12-4**
- Lawrence 200+ kept off (ban); would have hit at 242.

### Biggest misses / why
1. **Strange 4+ / 40+** — only 2 targets / 22 yds; Boerkircher took the 52-yd TE chunk. Hawkins-OUT scheme prior overstated Strange volume.
2. **Washington o63.5** — 61 (miss by 2.5); 40+ was the right rung; model had opposed the main.
3. **Game U39.5** — final 43 on Hill 65 TD + late JAX scores (BAL TT U and skill unders still hit).
4. **Wrongly-cut hit:** JAX 1H −6.5 (CUT §7 / no period model) won 17–3.

## Defenses giving up big plays this game
- **BAL D:** 6 flagged — Boerkircher 52 (Humphrey tag), Washington 50 TD (unattributed), Meyers 16/17/18 (Awuzie / Hamilton / Tampa), Strange 15 (Starks). WR 4, TE 2.
- **JAX D:** 1 flagged — Hill 65 rush TD (Q4). No pass20 allowed.

## Team DB files touched
- `/workspace/nfl-database/teams/defense/BAL.md`
- `/workspace/nfl-database/teams/defense/JAX.md`
- `/workspace/nfl-database/teams/offense/BAL.md`
- `/workspace/nfl-database/teams/offense/JAX.md`
- `/workspace/nfl-database/teams/defense/defense_db.csv` (16 game-scope rows)
- `offense_db.csv` not hand-edited (needs build_team_db rebuild post-nflverse wk10)

## Code notes appended (path)
- `/workspace/nfl-database/postmortems/2026-11-06_code_notes_for_ghost6.md`
- Held files untouched (run_gate, assemble, rico*_rules, press_tier, sims, rulebook).

## Proposed fixes
- Period / 1H game-line model (stop P14 MISSING on JAX 1H −6.5-class legs)
- BACKUP_QB §7 exemption when miss-audit clears opponent explosives
- TE hierarchy: low recent Strange volume + TE2 explosives → FLAG only, not top SCHEME_EDGE
- Auto-swap to passing alt when model opposes and §7 fails on receiving main
- Totals garbage / home-run RB soft flag for game unders
- Rebuild offense_db after nflverse week-10
- Fix live tacklers parser (strip formation tokens)
- Code NO_PASS_YDS into door (still manual)

## Betting Hub summary (copy-ready)
TNF JAX 33 BAL 10 is fully graded. Proposed-only card (no bets placed) went 12-4 across Rico’s 4-leg and the three 4-leg proposals: Slip B swept 4-0 (Meyers 25+, Hill 2+, Henry U69.5, JAX 1Q −2.5); Rico 4-leg split 2-2 with Strange 4+ and Washington o63.5 missing while JAX 1H −6.5 and Henry 40+ hit — and 1H −6.5 had been wrongly cut by §7. Biggest lesson: Strange volume never showed (2 catches, 22 yards) even with Hawkins out; Boerkircher took the chunk TE play. Playlog/ledger/explosives and BAL/JAX team files are updated; door/held code untouched; notes for Ghost6 filed.

## User / Grok-chat summary (copy-ready)
Thursday night is closed out: JAX beat BAL 33–10. I built the Week 10 playlog, appended the defender ledger (coverage check OK), logged the explosives, updated the Ravens and Jaguars team files, and graded every proposed leg from the r6 card — 12-4 overall, with the under/short BAL script (Slip B and most of Slip C) looking best and Strange being the clear miss. No held code was edited; Ghost6 has a short fix list. Full write-up is in the Friday TNF postmortem.

## Absolute paths
- Postmortem: `/workspace/nfl-database/postmortems/2026-11-06_TNF.md`
- This report: `/workspace/nfl-database/postmortems/2026-11-06_TNF_automation_report.md`
- Slips graded: `/workspace/nfl-database/slips/2026-11-05_THU.json`
- Code notes: `/workspace/nfl-database/postmortems/2026-11-06_code_notes_for_ghost6.md`
- Playlog: `/workspace/nfl-database/playlogs/2026_wk10/JAX_BAL.csv`
