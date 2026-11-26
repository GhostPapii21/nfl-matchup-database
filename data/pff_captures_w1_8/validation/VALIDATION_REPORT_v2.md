# PFF 2026 W1–8 — second-source reconciliation v2 (2026-11-06 ET)
Second source: **ESPN public site API** (scoreboard + summary per event), 2026 REG W1–8, 121/121 events, retrieved 2026-11-06 19:08 EST; URLs per game in `games_reconciliation_v2_espn.json`. ESPN is a media box score, **not the NFL.com official gamebook** (not accessed). nflverse PBP (GSIS-derived; local copy mtime 07:34 ET ≠ retrieval) and PFR snaps retained as a separate third reference. Originals untouched; v1 outputs kept; v2 files versioned.

## Parser/join fixes before blaming PFF
- v1 box-card parser bled values across cards (Javonte Williams 7 vs 24, Henry, Schultz, McCaffrey, Flowers): **QA bug**, fixed by card-marker split (v2).
- Initial+last name keys collided (Bijan/Brian Robinson etc.): **QA bug**, fixed with full-name keys; remaining ambiguous rows "unverifiable".
- Deebo Samuel 30648 80 yds/0 rec: **PFF matches ESPN** (0 REC, 80 YDS, 1 TD); the nflverse-derived 0 was my PBP-aggregation gap.

## Results vs ESPN
- Finals 120/121 match; **30658 NYJ@CHI: ESPN 12-23** (missed XP per PBP) → PFF recap header 13 is wrong; PFF schedule correct.
- INT returns confirmed by ESPN box: 30722 LAR Lake 45 + McDuffie 26 = 71, LAC Still 0 → PFF takeaway team inverted. 30718 JAX Lane 92 TD + Combs 9 = 101, IND none → PFF "Colts 99" inverted and 2 yds off.
- Player fields 14,134: **13,307 match (94.1%)**, 687 mismatch, 140 unverifiable. In 666/687 mismatches ESPN = nflverse, i.e. PFF differs from both.
  - Pass INT/rec TD/rush TD: 0 mismatches. Pass att 5, cmp 3, TD 1 mismatch.
  - Yards: pass 60, rush 111, rec 126 mismatches; QB rush yards typically PFF lower/negative (possible kneel/scramble basis, unproven).
  - Targets: 343 mismatches, PFF lower in 328 (mean −1.06) — systematic; cause undocumented, not assumed.
  - 38 diffs ≥5 remain open (e.g. Gunnar Helm 51 vs 76, Juwan Johnson 35 vs 66, Drake Maye 362 vs 374).
- Team totals (242 team-games): offensive plays 237 match; first downs 40 match (PFF lower by 1–6, penalty-first-down basis differs); total yards 49 match; rush att 197; rush yds 141. Definitions not reconciled → **team totals not verified**.
- Snaps: no official second source. 14 conflict games (mostly Week 2): PFF top offense snaps ≈ ESPN plays (+0.5) while in other games PFF ≈ PFR (~+3.3, penalty plays included) → PFF used a different snap basis in these games. Quarantined, cause unknown.

## Not validated (PFF-native)
Grades, pressures/hits/hurries, BTT/TWP, adj. comp%, YBC/YCO/MTF, EPA/percentiles, blocking/run-D/coverage cards, takeaways.

## Files (v2)
`reconcile_v2.py`, `reconcile_espn_v2.py`, `team_totals_v2.py`, `field_reconciliation_v2_espn.csv` (PFF/ESPN/nflverse per field, ESPN athlete IDs), `field_reconciliation_v2_nflverse.csv`, `games_reconciliation_v2_espn.json`, `team_totals_v2_espn.csv`, `snap_ceiling_diagnostic_v2.csv`, `quarantine_v2.json`, `validation_summary_v2.json`, `espn_box_extract/` (header+boxscore only), `espn_raw/` (full, 68 MB, local only).
