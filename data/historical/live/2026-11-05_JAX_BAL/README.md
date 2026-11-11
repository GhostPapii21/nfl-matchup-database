# JAX @ BAL live PBP — 2026-11-05 TNF

## Files
- `pbp_live.csv` / `pbp_live.md` — append/dedupe play log (targets, explosives)
- `live_meta.json` — last pull status/score/play count
- `meyers_focus.md` — Meyers targets vs lining-up (coverage UNKNOWN unless explicit)
- `quarter_results.csv` / `quarter_results.md` — independent quarter pts + winners/leaders
- `period_line_grades.csv` — grades vs stored r6 period lines only (no new odds pull)
- `drive_log.csv` / `drive_conversions.md` — both teams’ drives, TOP, ongoing flag
- `third_down_log.csv` — 3rd-down att/conv; NA_NO_PLAY excluded from denom
- `red_zone_log.csv` — RZ trips (yte 1–20); TD vs FG separate
- `team_conversion_summary.csv` — team TOP / 3rd / RZ + boxscore comparison
- `raw/` — ESPN JSON snapshots

## Refresh (no polling loop here)
```bash
python3 /workspace/nfl-database/live/tools/espn_live_pbp_updater.py \
  --event-id 401873037 \
  --outdir /workspace/nfl-database/live/2026-11-05_JAX_BAL
```
That updater also rebuilds quarter/drive/conversion logs via `build_quarter_drive_logs.py`.

Public ESPN only. Explosive: pass≥20, rush≥10. Tackler ≠ coverage.
RZ trip = play with yardsToEndzone 1–20 (timeouts with yte=0 excluded).

## FINAL (2026-11-05 night)
Confirmed **JAX 33 – BAL 10**. See `FINALIZED.json`, `audit_findings.md`, `defensive_coverage_profile.md`,
`possessions_final.csv`, `period_lines_cleared_ledger.csv`, `period_q1_q2_q3_fd_dk_cleared.csv`.
Routine should be paused/deleted by parent (game over).
