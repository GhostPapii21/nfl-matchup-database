# FIXES applied after Ghost6 "VETTED WITH CHANGES" (4:10 PM AST, Sat Nov 21)

Applied Sat Nov 21 about 4:35 PM AST. The generator is `_work/gen.py` with content in `_work/manual.py`. Pre-fix copies are kept as `_work/gen_v1.py`, `_work/manual_v1.py` and `_work/SUMMARY_v1.md`.

1. **Emmett Johnson:** removed from WATCH in ARI@KC report section 3a, the shadow SGP and the script text. The review row now reads DROP (N1 fail: shares 0.13, 0.04, 0.21, 0.88, 1 of 4 at 60%+). He is added to ARI@KC/checklist.md as a CUT leg with Phase 7 FAIL and Phase 2 FAIL. The old generic "3 of 4" text is replaced by per-leg gate data in all checklists.
2. **Rice 80+ row:** stamped "WATCH / do-not-play; no verified main defender; weather flag; #3 WR ban; STALE edge (Nov 20 prices; board model built Thu night, pre-Beck/Walker)" in ARI@KC section 7. Every 80+ row in all reports now carries the same stamp logic.
3. **Henry Phase 7:** BAL@CAR checklist now shows the RB 60% carry gate, PASS 3 of 4 (shares 0.68, 0.65, 0.52, 0.67), with the 52% game disclosed. It is also disclosed in report section 3a.
4. **Lawrence:** the count is corrected to 5 of 9 and 2 of 4 at 10.5 (4 of 9 and 1 of 4 at FD 8.5) in JAX@NYG section 3a, the review and SUMMARY. JAX checklist Phase 7 reads "QB rush market; RB 60% gate does not apply" for Lawrence and McCarthy.
5. **Beck:** the section 3e rush-under row is now VOID (OUT) in ARI@KC. A Status column was added to 3e in all reports, and OUT players are VOID.
6. **Cook 79.5:** one label everywhere, sections 3a and 3c alike: "RESEARCH LEAN (paper only; sims not run; STALE price DK -192, re-check at kickoff; 69.5 rung for the blowout trim)". The repo selective-edge caveat on alt floors was added to the evidence.
7. **MIN@SF U46.5:** downgraded to WATCH (until a Cousins-adjusted script projection exists) in section 3a, the review and SUMMARY. Addison (OUT) is removed from the matchup and opportunity tables. OUT players are filtered from those tables in all reports.
8. **Totals:** every total number is labeled "season-average cross-check, not a projection" in the five-line summary, sections 3a and 3b, and SUMMARY. Section 3b adds each team's actual 2026 game totals (nflverse pbp) vs the posted total, plus a caveat block: no miss audit, the PR #25 backtest, the selective-edge study. JAX caveat: 1.5 points is noise; the lean rests on rain and the JAX defense. CIN caveat: last-4 form of 37.5 a game puts the cross-check near 52.4, and the label is now "KEEP (thin)".
9. **"Gated" and "star-under" wording:** dropped. I checked the 18-5 history (backtests/selective_under_alt_2026-11-12, research/runs/2026-11-13_selective_edge_phase4): it required the RB 60% gate (QBs exempt) plus a model edge vs no-vig of +5 points or more. No model ran, so no spot can be shown to qualify. Labels now read "QB/RB rush-yard under; 18-5 study criteria NOT shown: no model edge" (Henry, Allen, Mayfield, Nix). "Star-under reason" became "Matchup reason". Checklist Phase 14 states this too.
10. **Checklists:**
    - St. Brown (TB@DET) and Kittle (MIN@SF) were added; all receiving leans are now included.
    - MIN Phase 11 reads "BORDERLINE (recheck)", not FAIL. The MIN_SF weather flag no longer cuts receiving; the report phase table shows the same.
    - Summary blocks are rebuilt per leg from the actual phase statuses, which fixes the MIN summary.
11. **NYG starter:** flagged as unconfirmed (McCarthy per the depth chart; nflverse pbp shows Winston with 6 appearances, Weeks 2-6 and 9, vs McCarthy 4, Weeks 6, 7, 9, 10). The flag is in JAX@NYG injuries, the script, the McCarthy row and SUMMARY. McCarthy under stays NO PLAY.
12. **STALE labels:** every report header has a STALE price banner. Price columns in 3c, 3d and 3e are headed STALE, checklist Phase 12 says it, every checklist leg title carries "(price STALE)", and the SUMMARY banner repeats it. All re-check at kickoff.

## Final changes after the Ghost6 re-check (VETTED 4:18 PM AST), applied Sat about 4:25 PM AST
- (a) **Cook 79.5 is now WATCH.** The evidence is the Phase 4 study (rush alt-over floors ran about -10 to -13 points vs break-even), the -192 juice and the stale price. Updated in:
  - the MIA@BUF report (sections 3a and 3c, the shadow SGP and the review row), where the five-line summary now names Allen U27.5 as the strongest lean;
  - the MIA@BUF checklist leg title;
  - SUMMARY (the lean table, now 7 leans, the downgrade list and the game section).
  - Allen U27.5 is the MIA@BUF research lean.
- (b) **Vet line** in SUMMARY.md, every report header and every checklist: "VETTED by Ghost6 4:18 PM AST, paper only, research only until NFL-49/56 pass; re-check props at kickoff".
- SUMMARY.md.sha256 regenerated.
