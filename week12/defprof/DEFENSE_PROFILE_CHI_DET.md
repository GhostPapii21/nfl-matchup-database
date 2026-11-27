# Defense coverage profiles: CHI @ DET (Thanksgiving, kickoff 2026-11-26T18:00Z / 1:00 PM ET, Ford Field, dome)

Written postgame (2026-11-27), using pregame-available data only. Research only. projection_ready=false. Profiles INFORM projections; they do NOT verify a main defender (P4 still requires a named PBU/INT/DPI).

This profile was not written before kickoff. The CHI@DET 8:58 AM ET run checklist had P6 coverage headline rates PASS and P9 NGS MISSING (not checked). Numbers below are from sources already on disk; nothing here is invented or back-filled from the game result.

## Sources (all free; no paywall/login bypass; only sources actually pulled)

| Source | What | Pulled |
|---|---|---|
| nflverse PBP 2026 REG (`_shared/nflverse/play_by_play_2026.parquet`, mtime 03:49 ET Nov 26) | Allowed to RB/WR/TE (targets, rec, yds, TD, PPR FP), QB rush allowed, explosives, RZ TD% — computed by `def_allowed.py` (ranks: 1 = stingiest, 32 = most allowed). Sample is 10 games thru W11. The parquet's only W12 game is GB@LA; CHI@DET is not in it. The computed JSON was written 1:30 PM ET (after CHI@DET kickoff) from that pre-kick PBP. | computed 13:3x ET from the 03:49 ET parquet |
| NFL Next Gen Stats via nflverse NGS mirror (`ngs_*.csv.gz`; nextgenstats.nfl.com API returned 401, not bypassed) | Separation/cushion allowed by position, RYOE allowed, CPOE allowed (opponent NGS qualifiers only). `ngs_def_out.txt` originally omitted CHI/DET; the CHI/DET lines in this profile were computed postgame with the same `ngs_def.py` used for PHI/DAL/KC/BUF. The gz files were pulled 1:31 PM ET (after CHI@DET kickoff). 2026 W12 NGS rows are only GB/LAR — CHI@DET is not in the extract. | see ngs_PULLED_UTC.txt; CHI/DET computed 2026-11-27 from those files |
| StatRankings CoverageIQ (vs WR) | man/zone/single-high/two-high/blitz rates from `_shared/coverage/statrankings_coverage.json` / `coverage_out.txt` | 03:59 ET |
| Sharp Football league coverage-schemes page (`_shared/coverage/sharp_cov.html`) | man/zone/MOF-closed/MOF-open headline rates for CHI and DET | 03:59 ET |
| Sharp Football CHI@DET game page + Hribar Worksheet | — | **NOT PULLED.** Unlike PHI@DAL and KC@BUF, there is no `sharp_chi_det.html` / `.txt` in `week12/defprof`. Paywalled Sharp RB/WR/TE sections, pts/drive, explosive-play, and QB-rush Sharp tables for this game are MISSING. |
| PFF | — | **NOT PULLED** (no free CHI@DET data page used) → MISSING |
| ESPN injuries API | statuses used in the 8:58 AM ET CHI@DET report (live check 9:00 AM ET). `week12/prekick/espn_inj_PULLED_UTC.txt` is timestamped 1:39 PM ET (after kickoff) and is not used as a pre-kick stamp. | 9:00 AM ET (report); no pre-kick file stamp |
| Official NFL.com inactives | `inactives_CHI_DET.md` was never saved in `week12/prekick` (PHI@DAL and KC@BUF have those files). `nfl_inactives.html` / `nfl_inactives_2000.html` in that folder include CHI@DET but were saved 2:46 PM / 3:00 PM ET, after kickoff, so they are not used here. | **MISSING as a pre-kick artifact** |

## DET defense (what Caleb/Swift/Monangai/CHI pass-catchers face)

- **Scheme:** StatRankings man 38.2% (#10), zone 59.2%, single-high 57.4% (#10), two-high 42.6%, **blitz 29.8% (#19)**. Sharp coverage-schemes page: man 20.3 / zone 74.8 / MOF-closed 48.5 / MOF-open 49.0. The two disagree on man level, so this is **SHARP CAUTION**; StatRankings is primary. Coverage splits (yds/route vs man/zone) were paywalled and not pulled → MISSING.
- **Vs RB: stingy on the ground, average in receiving.** 18.6 car / 69.3 rush yds per game (rk3), YPC 3.73, 5 RB rush TDs + 2 RB rec TDs allowed, 18.6 PPR FP/g (rk4). RB rec 32.4 yds/g (rk15). NGS RYOE allowed +0.55/att (rk24) despite 8+ box% faced 42.1 (high stacked-box rate) on 121 att — volume allowed is low; efficiency allowed is closer to average-soft.
- **Vs WR:** 20.0 tgt (rk24), 12.7 rec (rk29), 150.5 yds (rk19), 8 rec TDs, 32.8 PPR FP/g (rk21). NGS WR separation allowed 2.52 (rk2, tight) but CPOE allowed +2.53 (rk25): volume- and completion-driven, not separation-driven.
- **Vs TE: the weak spot.** 9.4 tgt (rk31, second-most), 74.0 yds (rk30), **11 TE rec TDs**, 20.8 PPR FP/g (**rk32, most allowed**). NGS TE separation allowed 3.03 (rk6, tight) — the leak is volume and TDs, not separation.
- **Vs QB rush:** 21.9 yds/g allowed on 4.2 car (rk29); scrambles 2.3/g. Softest QB-rush allowance of the three Thanksgiving defenses in this folder.
- **Who scores on them:** TEs (11: J.Johnson, Fant, Knox, Kincaid, Sadiq, Ruckert, Quitoriano 2, McBride, Kraft, Hockenson) and WRs (8: Vele, Palmer, McMillan 2, Jefferson, Hurst 2). RB rush 5 (Miller, Cook, Hubbard 2, Irving) and Allen 2 rush TDs (W2). RZ drive TD% .537 (rk24). Explosive pass 3.70/g (rk30).
- **Weak spot:** TE volume/TDs, plus QB rush and explosive passes. **Strength vs CHI:** run-defense volume (RB rush yds rk3, PPR rk4). **Availability (ESPN statuses as of the 8:58 AM ET report / 9:00 AM ET check, not official inactives):** CB Ennis Rakestraw OUT; DT Skyler Gill-Howard IR; C Cade Mays IR (offense). S Chuck Clark (hamstring) Q; DE/LB DJ Wonnum (back) Q. Official inactives were not saved pre-kick (see Sources).

## CHI defense (what Goff/Gibbs/St. Brown/LaPorta face)

- **Scheme:** StatRankings man 35.1% (#14), zone 64.3%, single-high 50.8% (#16), two-high 49.2%, **blitz 35.9% (#11)**. Sharp coverage-schemes page: man 25.6 / zone 69.9 / MOF-closed 48.3 / MOF-open 47.7 (man-level gap is smaller than DET's; still a cross-check only, not mixed in). Coverage splits by scheme were not pulled → MISSING.
- **Vs RB: below-average receiving, stingy carry volume.** 17.7 car (rk1, fewest RB carries allowed) / 77.1 rush yds/g (rk10), YPC 4.36 (rk21), 5 RB rush TDs + 3 RB rec TDs, 20.4 PPR FP/g (rk11). RB rec 36.2 yds/g (rk20). NGS RYOE allowed +0.17/att (rk16) on 116 att.
- **Vs WR:** 16.9 tgt (rk10), 10.0 rec (rk8), 151.1 yds (rk20), 8 rec TDs, Y/T 8.94 (rk25), 30.1 PPR FP/g (rk9). NGS WR separation allowed 2.54 (rk3, tight), CPOE allowed −0.99 (rk15). Deep YPA 19.36 (**rk31**) is the clear passing-efficiency leak in a defense that does not otherwise rank soft vs WR volume.
- **Vs TE: tough.** 6.6 tgt (rk10), 46.9 yds (rk11), 3 TDs, 10.8 PPR FP/g (rk7). NGS TE separation allowed 3.13 (rk9).
- **Vs QB rush:** 15.0 yds/g on 2.4 car (rk13; fewest QB carries allowed, rk1), scrambles 1.7/g.
- **Who scores on them:** WRs (8: Coker 2, Watson 2, I.Williams, Dotson, Smith-Njigba, Kupp) and RB rushers (5: Hubbard, Lloyd 2, Irving 2). RB rec 3 (Hubbard, Stevenson, Kamara); TEs 3 (Pitts 2, Raridon); QB rush 3 (Young, Hurts, Maye). RZ drive TD% .417 (rk8). Pts allowed 19.7/g (rk6).
- **Weak spot:** deep passes (deep YPA rk31) and WR yards per target (rk25), plus RB receiving TDs (rk26). **Strength vs DET:** overall points (rk6), TE PPR (rk7), red-zone TD rate (rk8), and low RB carry volume allowed. **Availability (same 9:00 AM ET ESPN check, not official inactives):** CB Kyler Gordon (nickel) OUT; RB Roschon Johnson OUT. CB Tyrique Stevenson (groin) Q; LB D'Marco Jackson (elbow) Q. Official inactives were not saved pre-kick (see Sources).

## Implications for candidate legs (inform only; written from the pregame profile, not from the result)

| Leg | Profile says | Effect |
|---|---|---|
| Caleb Williams rush U22.5 | DET QB rush allowed 21.9 yds/g (rk29) and single-high 57.4% (#10) are against the under (scramble risk). DET blitzes only 29.8% (#19), which matches Caleb's stronger no-blitz split in the run report. NGS RYOE allowed rk24. | No upgrade to the under; the 8:58 AM ET run already capped this at Lean / small because rush unders are the historically gated market |
| Gibbs rush | CHI allows the fewest RB carries (rk1) and 77.1 rush yds/g (rk10), RYOE rk16 — not a soft W1–W11 run D in this sample | No upgrade; stays WATCH / MANUAL_REVIEW as in the run. Do not pair an RB over with a same-game total under |
| CHI TE (Loveland) vs DET | DET TE is the weak spot (11 TD, rk32 PPR, rk31 targets) | Inform only. Receiving legs stay CUT at P4 (no verified main defender; no Sharp/PFF alignment page was pulled) |
| CHI / DET receivers | CHI deep YPA rk31 and DET WR volume (tgt rk24, rec rk29, CPOE rk25) are context only | Still CUT at P4 |
| Goff / pass volume vs CHI blitz | CHI blitz 35.9% (#11). No Sharp pts/drive or explosive-pass table was pulled for this game | No new leg from this profile |

Gaps carried forward: no CHI@DET Sharp game page or Hribar Worksheet; no PFF page; no official pre-kick inactives file; NGS for CHI/DET was not computed before kickoff (filled here postgame from the already-pulled mirror, with the late pull and GB@LA-only W12 leakage check disclosed above); coverage splits by man/zone remain MISSING.
