# BetGuru — PHASE 4 (Cross-reference and alerts) — Sun Nov 1, 2026
Script lines 409–444. Phases 5+ NOT run. src/phase4.py. Legs = every Phase 3 survivor, plus Metcalf 40+ (alive per corrected chart: INSUFFICIENT FILM, no shadow, mapped Tyson Campbell).
Sources: nflverse pbp/snaps 2026 (Oct 31 7:17 PM ET); ESPN injuries API (~7:30 PM ET); ESPN scoreboard odds Nov 1 (defense/espn_scoreboard_20261101.json); PFR cache Oct 29 (fresh pull 403); Phase 3 file.
**Slip comparison: NOT_APPLICABLE** — no slip supplied for comparison. **Postgame screening triggers (60+ rec yds, 100+ rush, 2+ TD, 5+ rec): NOT_APPLICABLE**; games not played. These are review triggers, not proof of value.
**8A film rule (all rows):** a film route/alignment read counts only if every cited catch/target matches an nflverse pbp play (quarter/clock, receiver, yards). Unmatched = UNVERIFIED → GAP, disclosed. All current charts (Metcalf, Gibbs, McBride, Puka, Bowers, Lamb, Higgins) are UNVERIFIED; A. Williams has no film (GAP).
Flag thresholds: opp sack-rate top 8 or OL starter Out/Doubtful; RB on a ≥6-pt dog / pass-catcher on a ≥7-pt favorite / total ≤41; weekly CV >0.45 or a week <50% of median.

|Player|Market|Opp|Phase 3|Phase 4|#Flags|Flags|
|-|-|-|-|-|-|-|
|Aaron Jones|rushyds|DET|PASS|CAUTION|3|OL/rusher; Backup-QB; Workload|
|Amon-Ra St. Brown|rec|MIN|PASS|PASS|1|OL/rusher|
|Bijan Robinson|rushyds|TB|PASS|CAUTION|3|Injuries/replacement; Backup-QB; Workload|
|Braelon Allen|rushyds|LV|PASS|CAUTION|3|OL/rusher; Injuries/replacement; Workload|
|Brock Bowers|rec|NYJ|PASS (8A PENDING)|PASS|1|OL/rusher|
|Brock Bowers|recyds|NYJ|PASS (8A PENDING)|PASS|1|OL/rusher|
|CeeDee Lamb|rec|ARI|PASS|CAUTION|3|Injuries/replacement; Game flow; Workload|
|DK Metcalf|recyds|CLE|PASS (alive; no shadow evidence, mapped T. Campbell; film GAP disclosed)|CAUTION|4|OL/rusher; Injuries/replacement; Game flow; Workload|
|Dallas Goedert|rec|WAS|PASS (8A PENDING)|CAUTION|4|Injuries/replacement; Backup-QB; Game flow; Workload|
|Drake London|recyds|TB|PASS|CAUTION|3|Injuries/replacement; Backup-QB; Workload|
|Garrett Wilson|recyds|LV|PASS|CAUTION|3|OL/rusher; Injuries/replacement; Workload|
|Jahmyr Gibbs|rushyds|MIN|PASS — CAUTION (pbp/FTN)|CAUTION|1|OL/rusher|
|James Cook|rushyds|BAL|PASS|PASS|1|Injuries/replacement|
|Javonte Williams|rushyds|ARI|PASS|PASS|1|Injuries/replacement|
|Jonathan Taylor|rushyds|JAX|PASS|CAUTION|2|Injuries/replacement; Game flow|
|Justin Jefferson|recyds|DET|PASS|CAUTION|3|OL/rusher; Backup-QB; Workload|
|Kenneth Walker III|rushyds|DEN|PASS|CAUTION|2|OL/rusher; Game flow|
|Parker Washington|recyds|IND|PASS|CAUTION|3|Injuries/replacement; Game flow; Workload|
|Puka Nacua|rec|LAC|PASS|CAUTION|2|Injuries/replacement; Workload|
|Puka Nacua|recyds|LAC|PASS|CAUTION|2|Injuries/replacement; Workload|
|Tee Higgins|recyds|TEN|PASS|CAUTION|2|Game flow; Workload|
|Trey McBride|rec|DAL|PASS (8A PENDING)|CAUTION|2|OL/rusher; Injuries/replacement|
|Trey McBride|recyds|DAL|PASS (8A PENDING)|CAUTION|2|OL/rusher; Injuries/replacement|
|Tyler Warren|recyds|JAX|GAP|GAP|1|Injuries/replacement|
|Zay Flowers|recyds|BUF|PASS|CAUTION|2|OL/rusher; Backup-QB|

## Same-player correlation with placed Ticket 2 (barred markets, not re-bet)
- Jahmyr Gibbs live leg overlaps placed **Gibbs rec**. Exposure stacks on one player; disclose in sizing.
- Amon-Ra St. Brown live leg overlaps placed **St. Brown recyds**. Exposure stacks on one player; disclose in sizing.
- Drake London live leg overlaps placed **London rec**. Exposure stacks on one player; disclose in sizing.
- CeeDee Lamb live leg overlaps placed **Lamb recyds**. Exposure stacks on one player; disclose in sizing.
- Zay Flowers live leg overlaps placed **Flowers rec**. Exposure stacks on one player; disclose in sizing.
- James Cook live leg overlaps placed **Cook rushrec**. Exposure stacks on one player; disclose in sizing.

## Stable issues (material data/model defects)
- **ISS-01 Film charts unreliable.** Evidence: Metcalf INTs were really Pittman/R. Wilson targets; Lamb 2×40-yd TDs vs actual 5-74; Gibbs 5/11 match; McBride 2/6; Higgins 2 TDs vs 1. Acceptance: every cited play joins to an nflverse play_id on qtr/clock ±15 s, receiver and yds ±3; otherwise UNVERIFIED.
- **ISS-02 PFR coverage cache stale (Oct 29; fresh pull 403; G≈5).** Acceptance: re-pull with G equal to games played, or label every row cache-dated.
- **ISS-03 Scheme source disagreement (Sharp vs StatRankings; DAL #12 vs #4, JAX #13 vs #23).** Acceptance: state both sources; no man/zone-based edge unless their ranks agree within 5.
- **ISS-04 No free route participation (nflverse 2026 participation 404).** Acceptance: participation file published, or routes stay GAP.
- **ISS-05 TE/slot→LB/S mapping unruled (Bowers, McBride, Goedert, Warren).** Acceptance: Rico ruling recorded; 8A re-run.
- **ISS-06 Run concept absent (OZ/IZ).** Acceptance: a verified concept source; until then run_location/run_gap proxy is labeled.
- **ISS-07 Metcalf chart graphic "3 REC 65 YDS" vs pbp 5-115.** Acceptance: treat the graphic as in-game, the pbp as final.

## Pending for later phases (noted, not run)
- Price and evaluate Gibbs 60+ rush (50+ fallback) and Lamb 5+ rec on their own edge (Phase 7+).
- 10G end: side-by-side vs Ghost6's card (~+735: Flournoy 3+ rec, Tuten 60+ rush, Metcalf 40+, Puka 70+, A. Williams 3+ rec, Gibbs 60+ rush), with sims, edge vs no-vig, and where we disagree and why.

### Aaron Jones (MIN vs DET) — rushyds · rung None @ None
- **PHASE 4: CAUTION** (3 flags) · Phase 3: PASS
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: MIN OL on report none; DET defense sack rate 7.3% (rank 7/32); MIN OL allows 9.1% [pbp, ESPN] → FLAG
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q none (IR excluded: already in baseline); redistribution unverified (no boost) → ok
- Backup-QB: primary passer by week {1: 'C.Wentz', 2: 'C.Wentz', 3: 'K.Murray', 4: 'K.Murray', 5: 'K.Murray', 7: 'K.Murray'}; QBs on report none → FLAG (starter changed this season)
- Game flow: spread +3 total 46.5 [ESPN scoreboard / leg file] → ok
- Workload: weekly carries {1: 12, 2: 23, 3: 17, 4: 20, 5: 25, 7: 8} (CV 0.37); weekly yds {1: 40, 2: 105, 3: 58, 4: 94, 5: 113, 7: 26} → FLAG unstable
- Source discrepancies: none found
- Unsupported model mechanics: run concept (OZ/IZ) not in free data; run_location/gap proxy only → disclosed, no mechanic credited
- 8A film read: n/a (rushing)
- Possible-error buckets: Efficiency, Opportunity, Model capability. No causation assigned (no box score).

### Amon-Ra St. Brown (DET vs MIN) — rec · rung None @ None
- **PHASE 4: PASS** (1 flags) · Phase 3: PASS
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: DET OL on report [('Ben Bartch', 'G', 'Injured Reserve')]; MIN defense sack rate 10.2% (rank 1/32); DET OL allows 5.0% [pbp, ESPN] → FLAG
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q none (IR excluded: already in baseline); redistribution unverified (no boost) → ok
- Backup-QB: primary passer by week {1: 'J.Goff', 2: 'J.Goff', 3: 'J.Goff', 4: 'J.Goff', 5: 'J.Goff', 7: 'J.Goff'}; QBs on report none → ok
- Game flow: spread -3 total 46.5 [ESPN scoreboard / leg file] → ok
- Workload: weekly targets {1: 14, 2: 13, 3: 8, 4: 11, 5: 11, 7: 11} (CV 0.18); weekly yds {1: 67, 2: 142, 3: 19, 4: 75, 5: 69, 7: 153} → ok
- Source discrepancies: PFR cache Oct 29 (fresh pull 403); PFR G≈5 lags pbp
- Unsupported model mechanics: route participation per dropback GAP (2026 participation 404) → disclosed, no mechanic credited
- 8A film read: UNVERIFIED → alignment/route item GAP (disclosed); counts only if every cited play matches nflverse pbp (qtr/clock, receiver, yds)
- Possible-error buckets: Efficiency, Source quality, Model capability. No causation assigned (no box score).

### Bijan Robinson (ATL vs TB) — rushyds · rung None @ None
- **PHASE 4: CAUTION** (3 flags) · Phase 3: PASS
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: ATL OL on report none; TB defense sack rate 6.0% (rank 18/32); ATL OL allows 7.1% [pbp, ESPN] → ok
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q [('Olamide Zaccheaus', 'WR', 'Questionable'), ('Brian Robinson Jr.', 'RB', 'Out')] (IR excluded: already in baseline); redistribution unverified (no boost) → FLAG
- Backup-QB: primary passer by week {1: 'C.Rush', 2: 'C.Rush', 3: 'M.Penix', 4: 'M.Penix', 5: 'M.Penix', 6: 'M.Penix', 7: 'M.Penix'}; QBs on report none → FLAG (starter changed this season)
- Game flow: spread +2.5 total 44.5 [ESPN scoreboard / leg file] → ok
- Workload: weekly carries {1: 21, 2: 16, 3: 29, 4: 19, 5: 17, 6: 9, 7: 20} (CV 0.32); weekly yds {1: 83, 2: 72, 3: 194, 4: 145, 5: 86, 6: 61, 7: 63} → FLAG unstable
- Source discrepancies: none found
- Unsupported model mechanics: run concept (OZ/IZ) not in free data; run_location/gap proxy only → disclosed, no mechanic credited
- 8A film read: n/a (rushing)
- Possible-error buckets: Opportunity, Model capability. No causation assigned (no box score).

### Braelon Allen (NYJ vs LV) — rushyds · rung None @ None
- **PHASE 4: CAUTION** (3 flags) · Phase 3: PASS
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: NYJ OL on report [('Max Mitchell', 'OT', 'Out'), ('Dylan Parham', 'G', 'Questionable')]; LV defense sack rate 6.4% (rank 16/32); NYJ OL allows 8.9% [pbp, ESPN] → FLAG
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q [('Breece Hall', 'RB', 'Questionable')] (IR excluded: already in baseline); redistribution unverified (no boost) → FLAG
- Backup-QB: primary passer by week {1: 'G.Smith', 2: 'G.Smith', 3: 'G.Smith', 4: 'G.Smith', 5: 'G.Smith', 6: 'G.Smith', 7: 'G.Smith'}; QBs on report none → ok
- Game flow: spread -1.5 total 45.5 [ESPN scoreboard / leg file] → ok
- Workload: weekly carries {1: 10, 2: 5, 3: 4, 4: 14, 5: 24, 6: 17, 7: 17} (CV 0.55); weekly yds {1: 40, 2: 7, 3: 14, 4: 59, 5: 116, 6: 78, 7: 104} → FLAG unstable
- Source discrepancies: none found
- Unsupported model mechanics: run concept (OZ/IZ) not in free data; run_location/gap proxy only → disclosed, no mechanic credited
- 8A film read: n/a (rushing)
- Possible-error buckets: Efficiency, Opportunity, Model capability. No causation assigned (no box score).

### Brock Bowers (LV vs NYJ) — rec · rung 6 @ -158
- **PHASE 4: PASS** (1 flags) · Phase 3: PASS (8A PENDING)
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: LV OL on report [('Jackson Powers-Johnson', 'G', 'Questionable')]; NYJ defense sack rate 7.6% (rank 5/32); LV OL allows 3.6% [pbp, ESPN] → FLAG
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q none (IR excluded: already in baseline); redistribution unverified (no boost) → ok
- Backup-QB: primary passer by week {1: 'K.Cousins', 2: 'K.Cousins', 3: 'K.Cousins', 4: 'K.Cousins', 5: 'K.Cousins', 6: 'K.Cousins', 7: 'K.Cousins'}; QBs on report none → ok
- Game flow: spread +1.5 total 45.5 [ESPN scoreboard / leg file] → ok
- Workload: weekly targets {3: 13, 4: 11, 5: 10, 6: 9, 7: 8} (CV 0.19); weekly yds {3: 116, 4: 86, 5: 110, 6: 70, 7: 73} → ok
- Source discrepancies: PFR cache Oct 29 (fresh pull 403); PFR G≈5 lags pbp; film: summary UNVERIFIED (implausible 62-play count).
- Unsupported model mechanics: route participation per dropback GAP (2026 participation 404); TE alignment GAP; TE/slot→LB/S 8A mapping awaiting Rico ruling → disclosed, no mechanic credited
- 8A film read: UNVERIFIED → alignment/route item GAP (disclosed); counts only if every cited play matches nflverse pbp (qtr/clock, receiver, yds)
- Possible-error buckets: Efficiency, Source quality, Model capability. No causation assigned (no box score).

### Brock Bowers (LV vs NYJ) — recyds · rung None @ None
- **PHASE 4: PASS** (1 flags) · Phase 3: PASS (8A PENDING)
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: LV OL on report [('Jackson Powers-Johnson', 'G', 'Questionable')]; NYJ defense sack rate 7.6% (rank 5/32); LV OL allows 3.6% [pbp, ESPN] → FLAG
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q none (IR excluded: already in baseline); redistribution unverified (no boost) → ok
- Backup-QB: primary passer by week {1: 'K.Cousins', 2: 'K.Cousins', 3: 'K.Cousins', 4: 'K.Cousins', 5: 'K.Cousins', 6: 'K.Cousins', 7: 'K.Cousins'}; QBs on report none → ok
- Game flow: spread +1.5 total 45.5 [ESPN scoreboard / leg file] → ok
- Workload: weekly targets {3: 13, 4: 11, 5: 10, 6: 9, 7: 8} (CV 0.19); weekly yds {3: 116, 4: 86, 5: 110, 6: 70, 7: 73} → ok
- Source discrepancies: PFR cache Oct 29 (fresh pull 403); PFR G≈5 lags pbp; film: summary UNVERIFIED (implausible 62-play count).
- Unsupported model mechanics: route participation per dropback GAP (2026 participation 404); TE alignment GAP; TE/slot→LB/S 8A mapping awaiting Rico ruling → disclosed, no mechanic credited
- 8A film read: UNVERIFIED → alignment/route item GAP (disclosed); counts only if every cited play matches nflverse pbp (qtr/clock, receiver, yds)
- Possible-error buckets: Efficiency, Source quality, Model capability. No causation assigned (no box score).

### CeeDee Lamb (DAL vs ARI) — rec · rung None @ None
- **PHASE 4: CAUTION** (3 flags) · Phase 3: PASS
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: DAL OL on report none; ARI defense sack rate 6.7% (rank 15/32); DAL OL allows 2.4% [pbp, ESPN] → ok
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q [('KaVontae Turpin', 'WR', 'Out'), ('George Pickens', 'WR', 'Questionable'), ('Luke Schoonmaker', 'TE', 'Questionable')] (IR excluded: already in baseline); redistribution unverified (no boost) → FLAG
- Backup-QB: primary passer by week {1: 'D.Prescott', 2: 'D.Prescott', 3: 'D.Prescott', 4: 'D.Prescott', 5: 'D.Prescott', 6: 'D.Prescott', 7: 'D.Prescott'}; QBs on report none → ok
- Game flow: spread -7 total 54.5 [ESPN scoreboard / leg file] → FLAG: ≥7-pt favorite; second-half pass volume may drop
- Workload: weekly targets {1: 8, 2: 9, 3: 8, 4: 21, 5: 5, 6: 18, 7: 12} (CV 0.51); weekly yds {1: 44, 2: 153, 3: 112, 4: 189, 5: 9, 6: 70, 7: 74} → FLAG unstable
- Source discrepancies: PFR cache Oct 29 (fresh pull 403); PFR G≈5 lags pbp; film: summary UNVERIFIED (two 40-yd TDs at PHI vs actual 5-74).
- Unsupported model mechanics: route participation per dropback GAP (2026 participation 404) → disclosed, no mechanic credited
- 8A film read: UNVERIFIED → alignment/route item GAP (disclosed); counts only if every cited play matches nflverse pbp (qtr/clock, receiver, yds)
- Possible-error buckets: Opportunity, Source quality, Model capability. No causation assigned (no box score).

### DK Metcalf (PIT vs CLE) — recyds · rung 40 @ -225
- **PHASE 4: CAUTION** (4 flags) · Phase 3: PASS (alive; no shadow evidence, mapped T. Campbell; film GAP disclosed)
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: PIT OL on report none; CLE defense sack rate 7.5% (rank 6/32); PIT OL allows 7.6% [pbp, ESPN] → FLAG
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q [('Ben Skowronek', 'WR', 'Questionable')] (IR excluded: already in baseline); redistribution unverified (no boost) → FLAG
- Backup-QB: primary passer by week {1: 'A.Rodgers', 2: 'A.Rodgers', 3: 'A.Rodgers', 4: 'A.Rodgers', 5: 'A.Rodgers', 6: 'A.Rodgers', 7: 'A.Rodgers'}; QBs on report none → ok
- Game flow: spread -3.5 total 39.5 [ESPN scoreboard / leg file] → FLAG: low total 39.5
- Workload: weekly targets {1: 10, 2: 9, 3: 5, 4: 9, 5: 4, 6: 15, 7: 6} (CV 0.45); weekly yds {1: 40, 2: 27, 3: 31, 4: 115, 5: 12, 6: 93, 7: 56} → FLAG unstable
- Source discrepancies: PFR cache Oct 29 (fresh pull 403); PFR G≈5 lags pbp; film: CORRECTED chart: INSUFFICIENT FILM; no shadow evidence; mapped Tyson Campbell (PFR cache Oct 29: CB CLE G4, 12-9-179, YPT 14.9, rat 116.7). Chart graphic "3 REC 65 YDS" vs pbp 5-115 (likely in-game graphic) — discrepancy logged.
- Unsupported model mechanics: route participation per dropback GAP (2026 participation 404) → disclosed, no mechanic credited
- 8A film read: UNVERIFIED → alignment/route item GAP (disclosed); counts only if every cited play matches nflverse pbp (qtr/clock, receiver, yds)
- Possible-error buckets: Efficiency, Opportunity, Source quality, Model capability. No causation assigned (no box score).

### Dallas Goedert (PHI vs WAS) — rec · rung None @ None
- **PHASE 4: CAUTION** (4 flags) · Phase 3: PASS (8A PENDING)
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: PHI OL on report none; WAS defense sack rate 4.5% (rank 24/32); PHI OL allows 6.8% [pbp, ESPN] → ok
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q [('Britain Covey', 'WR', 'Out'), ('Dontayvion Wicks', 'WR', 'Out'), ('DeVonta Smith', 'WR', 'Out')] (IR excluded: already in baseline); redistribution unverified (no boost) → FLAG
- Backup-QB: primary passer by week {1: 'J.Hurts', 2: 'J.Hurts', 3: 'J.Hurts', 4: 'J.Hurts', 5: 'J.Hurts', 6: 'T.McKee', 7: 'T.McKee'}; QBs on report none → FLAG (starter changed this season)
- Game flow: spread +6 total 40.5 [ESPN scoreboard / leg file] → note: underdog; pass volume up, efficiency risk; FLAG: low total 40.5
- Workload: weekly targets {1: 5, 2: 2, 5: 9, 6: 8, 7: 7} (CV 0.45); weekly yds {1: 77, 2: 4, 5: 38, 6: 61, 7: 48} → FLAG unstable
- Source discrepancies: PFR cache Oct 29 (fresh pull 403); PFR G≈5 lags pbp
- Unsupported model mechanics: route participation per dropback GAP (2026 participation 404); TE alignment GAP; TE/slot→LB/S 8A mapping awaiting Rico ruling → disclosed, no mechanic credited
- 8A film read: UNVERIFIED → alignment/route item GAP (disclosed); counts only if every cited play matches nflverse pbp (qtr/clock, receiver, yds)
- Possible-error buckets: Opportunity, Source quality, Model capability. No causation assigned (no box score).

### Drake London (ATL vs TB) — recyds · rung 60 @ -270
- **PHASE 4: CAUTION** (3 flags) · Phase 3: PASS
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: ATL OL on report none; TB defense sack rate 6.0% (rank 18/32); ATL OL allows 7.1% [pbp, ESPN] → ok
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q [('Olamide Zaccheaus', 'WR', 'Questionable'), ('Brian Robinson Jr.', 'RB', 'Out')] (IR excluded: already in baseline); redistribution unverified (no boost) → FLAG
- Backup-QB: primary passer by week {1: 'C.Rush', 2: 'C.Rush', 3: 'M.Penix', 4: 'M.Penix', 5: 'M.Penix', 6: 'M.Penix', 7: 'M.Penix'}; QBs on report none → FLAG (starter changed this season)
- Game flow: spread +2.5 total 44.5 [ESPN scoreboard / leg file] → ok
- Workload: weekly targets {1: 4, 2: 5, 3: 10, 4: 6, 5: 11, 6: 10, 7: 10} (CV 0.36); weekly yds {1: 29, 2: 51, 3: 194, 4: 96, 5: 118, 6: 62, 7: 66} → FLAG unstable
- Source discrepancies: PFR cache Oct 29 (fresh pull 403); PFR G≈5 lags pbp
- Unsupported model mechanics: route participation per dropback GAP (2026 participation 404) → disclosed, no mechanic credited
- 8A film read: UNVERIFIED → alignment/route item GAP (disclosed); counts only if every cited play matches nflverse pbp (qtr/clock, receiver, yds)
- Possible-error buckets: Opportunity, Source quality, Model capability. No causation assigned (no box score).

### Garrett Wilson (NYJ vs LV) — recyds · rung None @ None
- **PHASE 4: CAUTION** (3 flags) · Phase 3: PASS
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: NYJ OL on report [('Max Mitchell', 'OT', 'Out'), ('Dylan Parham', 'G', 'Questionable')]; LV defense sack rate 6.4% (rank 16/32); NYJ OL allows 8.9% [pbp, ESPN] → FLAG
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q [('Breece Hall', 'RB', 'Questionable')] (IR excluded: already in baseline); redistribution unverified (no boost) → FLAG
- Backup-QB: primary passer by week {1: 'G.Smith', 2: 'G.Smith', 3: 'G.Smith', 4: 'G.Smith', 5: 'G.Smith', 6: 'G.Smith', 7: 'G.Smith'}; QBs on report none → ok
- Game flow: spread -1.5 total 45.5 [ESPN scoreboard / leg file] → ok
- Workload: weekly targets {1: 7, 2: 7, 3: 13, 4: 4, 5: 11, 6: 6, 7: 3} (CV 0.49); weekly yds {1: 79, 2: 57, 3: 107, 4: 27, 5: 104, 6: 44, 7: 26} → FLAG unstable
- Source discrepancies: PFR cache Oct 29 (fresh pull 403); PFR G≈5 lags pbp
- Unsupported model mechanics: route participation per dropback GAP (2026 participation 404) → disclosed, no mechanic credited
- 8A film read: UNVERIFIED → alignment/route item GAP (disclosed); counts only if every cited play matches nflverse pbp (qtr/clock, receiver, yds)
- Possible-error buckets: Efficiency, Opportunity, Source quality, Model capability. No causation assigned (no box score).

### Jahmyr Gibbs (DET vs MIN) — rushyds · rung 70 @ -250
- **PHASE 4: CAUTION** (1 flags) · Phase 3: PASS — CAUTION (pbp/FTN)
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: DET OL on report [('Ben Bartch', 'G', 'Injured Reserve')]; MIN defense sack rate 10.2% (rank 1/32); DET OL allows 5.0% [pbp, ESPN] → FLAG
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q none (IR excluded: already in baseline); redistribution unverified (no boost) → ok
- Backup-QB: primary passer by week {1: 'J.Goff', 2: 'J.Goff', 3: 'J.Goff', 4: 'J.Goff', 5: 'J.Goff', 7: 'J.Goff'}; QBs on report none → ok
- Game flow: spread -3 total 46.5 [ESPN scoreboard / leg file] → ok
- Workload: weekly carries {1: 29, 2: 16, 3: 20, 4: 15, 5: 25, 7: 29} (CV 0.28); weekly yds {1: 156, 2: 52, 3: 99, 4: 46, 5: 151, 7: 116} → ok
- Source discrepancies: film: chart UNVERIFIED (5/11 plays match; fumble attribution wrong).
- Unsupported model mechanics: run concept (OZ/IZ) not in free data; run_location/gap proxy only → disclosed, no mechanic credited
- 8A film read: n/a (rushing)
- Possible-error buckets: Efficiency, Source quality, Model capability. No causation assigned (no box score).

### James Cook (BUF vs BAL) — rushyds · rung None @ None
- **PHASE 4: PASS** (1 flags) · Phase 3: PASS
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: BUF OL on report [('Spencer Brown', 'OT', 'Questionable')]; BAL defense sack rate 6.1% (rank 17/32); BUF OL allows 6.0% [pbp, ESPN] → ok
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q [('Dalton Kincaid', 'TE', 'Questionable'), ('DJ Moore', 'WR', 'Questionable'), ('Tyrell Shavers', 'WR', 'Out')] (IR excluded: already in baseline); redistribution unverified (no boost) → FLAG
- Backup-QB: primary passer by week {1: 'J.Allen', 2: 'J.Allen', 3: 'J.Allen', 4: 'J.Allen', 5: 'J.Allen', 6: 'J.Allen'}; QBs on report none → ok
- Game flow: spread -3 total 54.5 [ESPN scoreboard / leg file] → ok
- Workload: weekly carries {1: 13, 2: 21, 3: 24, 4: 12, 5: 25, 6: 22} (CV 0.29); weekly yds {1: 57, 2: 135, 3: 154, 4: 75, 5: 111, 6: 95} → ok
- Source discrepancies: none found
- Unsupported model mechanics: run concept (OZ/IZ) not in free data; run_location/gap proxy only → disclosed, no mechanic credited
- 8A film read: n/a (rushing)
- Possible-error buckets: Model capability. No causation assigned (no box score).

### Javonte Williams (DAL vs ARI) — rushyds · rung None @ None
- **PHASE 4: PASS** (1 flags) · Phase 3: PASS
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: DAL OL on report none; ARI defense sack rate 6.7% (rank 15/32); DAL OL allows 2.4% [pbp, ESPN] → ok
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q [('KaVontae Turpin', 'WR', 'Out'), ('George Pickens', 'WR', 'Questionable'), ('Luke Schoonmaker', 'TE', 'Questionable')] (IR excluded: already in baseline); redistribution unverified (no boost) → FLAG
- Backup-QB: primary passer by week {1: 'D.Prescott', 2: 'D.Prescott', 3: 'D.Prescott', 4: 'D.Prescott', 5: 'D.Prescott', 6: 'D.Prescott', 7: 'D.Prescott'}; QBs on report none → ok
- Game flow: spread -7 total 54.5 [ESPN scoreboard / leg file] → note: big favorite; positive script for rush volume
- Workload: weekly carries {1: 12, 2: 12, 3: 19, 4: 19, 5: 12, 6: 11, 7: 25} (CV 0.34); weekly yds {1: 41, 2: 30, 3: 98, 4: 62, 5: 45, 6: 41, 7: 155} → ok
- Source discrepancies: none found
- Unsupported model mechanics: run concept (OZ/IZ) not in free data; run_location/gap proxy only → disclosed, no mechanic credited
- 8A film read: n/a (rushing)
- Possible-error buckets: Model capability. No causation assigned (no box score).

### Jonathan Taylor (IND vs JAX) — rushyds · rung None @ None
- **PHASE 4: CAUTION** (2 flags) · Phase 3: PASS
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: IND OL on report none; JAX defense sack rate 4.7% (rank 23/32); IND OL allows 7.1% [pbp, ESPN] → ok
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q [('Anthony Gould', 'WR', 'Out'), ('Drew Ogletree', 'TE', 'Questionable')] (IR excluded: already in baseline); redistribution unverified (no boost) → FLAG
- Backup-QB: primary passer by week {1: 'D.Jones', 2: 'D.Jones', 3: 'D.Jones', 4: 'D.Jones', 5: 'D.Jones', 6: 'D.Jones', 7: 'D.Jones'}; QBs on report none → ok
- Game flow: spread +10 total 46.5 [ESPN scoreboard / leg file] → FLAG: RB on a ≥6-pt underdog (negative script risk)
- Workload: weekly carries {1: 19, 2: 24, 3: 23, 4: 20, 5: 15, 6: 21, 7: 18} (CV 0.15); weekly yds {1: 98, 2: 92, 3: 68, 4: 95, 5: 45, 6: 94, 7: 95} → ok
- Source discrepancies: Sharp vs StatRankings man-rank DIFFERS for JAX
- Unsupported model mechanics: run concept (OZ/IZ) not in free data; run_location/gap proxy only → disclosed, no mechanic credited
- 8A film read: n/a (rushing)
- Possible-error buckets: Opportunity, Source quality, Model capability. No causation assigned (no box score).

### Justin Jefferson (MIN vs DET) — recyds · rung None @ None
- **PHASE 4: CAUTION** (3 flags) · Phase 3: PASS
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: MIN OL on report none; DET defense sack rate 7.3% (rank 7/32); MIN OL allows 9.1% [pbp, ESPN] → FLAG
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q none (IR excluded: already in baseline); redistribution unverified (no boost) → ok
- Backup-QB: primary passer by week {1: 'C.Wentz', 2: 'C.Wentz', 3: 'K.Murray', 4: 'K.Murray', 5: 'K.Murray', 7: 'K.Murray'}; QBs on report none → FLAG (starter changed this season)
- Game flow: spread +3 total 46.5 [ESPN scoreboard / leg file] → ok
- Workload: weekly targets {1: 9, 2: 6, 3: 2, 5: 7, 7: 7} (CV 0.42); weekly yds {1: 92, 2: 55, 3: 32, 5: 79, 7: 44} → FLAG unstable
- Source discrepancies: PFR cache Oct 29 (fresh pull 403); PFR G≈5 lags pbp
- Unsupported model mechanics: route participation per dropback GAP (2026 participation 404) → disclosed, no mechanic credited
- 8A film read: UNVERIFIED → alignment/route item GAP (disclosed); counts only if every cited play matches nflverse pbp (qtr/clock, receiver, yds)
- Possible-error buckets: Efficiency, Opportunity, Source quality, Model capability. No causation assigned (no box score).

### Kenneth Walker III (KC vs DEN) — rushyds · rung None @ None
- **PHASE 4: CAUTION** (2 flags) · Phase 3: PASS
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: KC OL on report none; DEN defense sack rate 7.1% (rank 8/32); KC OL allows 3.3% [pbp, ESPN] → FLAG
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q none (IR excluded: already in baseline); redistribution unverified (no boost) → ok
- Backup-QB: primary passer by week {1: 'P.Mahomes', 2: 'P.Mahomes', 3: 'P.Mahomes', 4: 'P.Mahomes', 6: 'P.Mahomes', 7: 'P.Mahomes'}; QBs on report none → ok
- Game flow: spread -1.5 total 40.5 [ESPN scoreboard / leg file] → FLAG: low total 40.5
- Workload: weekly carries {1: 23, 2: 24, 3: 18, 4: 22, 6: 19, 7: 14} (CV 0.19); weekly yds {1: 173, 2: 117, 3: 70, 4: 177, 6: 128, 7: 36} → ok
- Source discrepancies: none found
- Unsupported model mechanics: run concept (OZ/IZ) not in free data; run_location/gap proxy only → disclosed, no mechanic credited
- 8A film read: n/a (rushing)
- Possible-error buckets: Efficiency, Opportunity, Model capability. No causation assigned (no box score).

### Parker Washington (JAX vs IND) — recyds · rung None @ None
- **PHASE 4: CAUTION** (3 flags) · Phase 3: PASS
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: JAX OL on report [('Anton Harrison', 'OT', 'Injured Reserve')]; IND defense sack rate 5.5% (rank 22/32); JAX OL allows 5.0% [pbp, ESPN] → ok
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q [('Jakobi Meyers', 'WR', 'Questionable')] (IR excluded: already in baseline); redistribution unverified (no boost) → FLAG
- Backup-QB: primary passer by week {1: 'T.Lawrence', 2: 'T.Lawrence', 3: 'T.Lawrence', 4: 'T.Lawrence', 5: 'T.Lawrence', 6: 'T.Lawrence'}; QBs on report none → ok
- Game flow: spread -10 total 46.5 [ESPN scoreboard / leg file] → FLAG: ≥7-pt favorite; second-half pass volume may drop
- Workload: weekly targets {1: 6, 2: 12, 3: 5, 4: 3, 5: 9, 6: 11} (CV 0.46); weekly yds {1: 83, 2: 98, 3: 40, 4: 7, 5: 124, 6: 64} → FLAG unstable
- Source discrepancies: PFR cache Oct 29 (fresh pull 403); PFR G≈5 lags pbp
- Unsupported model mechanics: route participation per dropback GAP (2026 participation 404) → disclosed, no mechanic credited
- 8A film read: UNVERIFIED → alignment/route item GAP (disclosed); counts only if every cited play matches nflverse pbp (qtr/clock, receiver, yds)
- Possible-error buckets: Opportunity, Source quality, Model capability. No causation assigned (no box score).

### Puka Nacua (LA vs LAC) — rec · rung None @ None
- **PHASE 4: CAUTION** (2 flags) · Phase 3: PASS
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: LA OL on report [('Coleman Shelton', 'C', 'Questionable')]; LAC defense sack rate 5.8% (rank 19/32); LA OL allows 3.7% [pbp, ESPN] → ok
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q [('Jordan Whittington', 'WR', 'Questionable'), ('Colby Parkinson', 'TE', 'Questionable')] (IR excluded: already in baseline); redistribution unverified (no boost) → FLAG
- Backup-QB: primary passer by week {1: 'M.Stafford', 2: 'M.Stafford', 3: 'M.Stafford', 4: 'M.Stafford', 5: 'M.Stafford', 6: 'M.Stafford', 7: 'M.Stafford'}; QBs on report none → ok
- Game flow: spread -6.5 total 45.5 [ESPN scoreboard / leg file] → ok
- Workload: weekly targets {1: 9, 4: 12, 5: 24, 6: 7, 7: 10} (CV 0.54); weekly yds {1: 74, 4: 125, 5: 138, 6: 80, 7: 68} → FLAG unstable
- Source discrepancies: PFR cache Oct 29 (fresh pull 403); PFR G≈5 lags pbp; film: summary UNVERIFIED (implausible 40-play count).
- Unsupported model mechanics: route participation per dropback GAP (2026 participation 404) → disclosed, no mechanic credited
- 8A film read: UNVERIFIED → alignment/route item GAP (disclosed); counts only if every cited play matches nflverse pbp (qtr/clock, receiver, yds)
- Possible-error buckets: Opportunity, Source quality, Model capability. No causation assigned (no box score).

### Puka Nacua (LA vs LAC) — recyds · rung 70 @ -290
- **PHASE 4: CAUTION** (2 flags) · Phase 3: PASS
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: LA OL on report [('Coleman Shelton', 'C', 'Questionable')]; LAC defense sack rate 5.8% (rank 19/32); LA OL allows 3.7% [pbp, ESPN] → ok
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q [('Jordan Whittington', 'WR', 'Questionable'), ('Colby Parkinson', 'TE', 'Questionable')] (IR excluded: already in baseline); redistribution unverified (no boost) → FLAG
- Backup-QB: primary passer by week {1: 'M.Stafford', 2: 'M.Stafford', 3: 'M.Stafford', 4: 'M.Stafford', 5: 'M.Stafford', 6: 'M.Stafford', 7: 'M.Stafford'}; QBs on report none → ok
- Game flow: spread -6.5 total 45.5 [ESPN scoreboard / leg file] → ok
- Workload: weekly targets {1: 9, 4: 12, 5: 24, 6: 7, 7: 10} (CV 0.54); weekly yds {1: 74, 4: 125, 5: 138, 6: 80, 7: 68} → FLAG unstable
- Source discrepancies: PFR cache Oct 29 (fresh pull 403); PFR G≈5 lags pbp; film: summary UNVERIFIED (implausible 40-play count).
- Unsupported model mechanics: route participation per dropback GAP (2026 participation 404) → disclosed, no mechanic credited
- 8A film read: UNVERIFIED → alignment/route item GAP (disclosed); counts only if every cited play matches nflverse pbp (qtr/clock, receiver, yds)
- Possible-error buckets: Opportunity, Source quality, Model capability. No causation assigned (no box score).

### Tee Higgins (CIN vs TEN) — recyds · rung None @ None
- **PHASE 4: CAUTION** (2 flags) · Phase 3: PASS
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: CIN OL on report none; TEN defense sack rate 6.8% (rank 12/32); CIN OL allows 4.2% [pbp, ESPN] → ok
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q none (IR excluded: already in baseline); redistribution unverified (no boost) → ok
- Backup-QB: primary passer by week {1: 'J.Burrow', 2: 'J.Burrow', 3: 'J.Burrow', 4: 'J.Burrow', 5: 'J.Burrow', 7: 'J.Burrow'}; QBs on report none → ok
- Game flow: spread -12.5 total 46.5 [ESPN scoreboard / leg file] → FLAG: ≥7-pt favorite; second-half pass volume may drop
- Workload: weekly targets {1: 6, 2: 10, 3: 7, 4: 16, 5: 4, 7: 7} (CV 0.51); weekly yds {1: 59, 2: 95, 3: 90, 4: 157, 5: 22, 7: 148} → FLAG unstable
- Source discrepancies: PFR cache Oct 29 (fresh pull 403); PFR G≈5 lags pbp; film: chart UNVERIFIED: cites 2 TDs at BAL (pbp: 1 TD, 6-148, long 44) and 3 catches + drop at MIA (pbp: 2-22); clips carry video timestamps, not game clock → cannot match.
- Unsupported model mechanics: route participation per dropback GAP (2026 participation 404) → disclosed, no mechanic credited
- 8A film read: UNVERIFIED → alignment/route item GAP (disclosed); counts only if every cited play matches nflverse pbp (qtr/clock, receiver, yds)
- Possible-error buckets: Opportunity, Source quality, Model capability. No causation assigned (no box score).

### Trey McBride (ARI vs DAL) — rec · rung 7 @ -225
- **PHASE 4: CAUTION** (2 flags) · Phase 3: PASS (8A PENDING)
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: ARI OL on report [('Jon Gaines II', 'G', 'Out'), ('Hjalte Froholdt', 'C', 'Questionable')]; DAL defense sack rate 4.1% (rank 26/32); ARI OL allows 5.0% [pbp, ESPN] → FLAG
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q [('Tip Reiman', 'TE', 'Out')] (IR excluded: already in baseline); redistribution unverified (no boost) → FLAG
- Backup-QB: primary passer by week {1: 'J.Brissett', 2: 'J.Brissett', 3: 'J.Brissett', 4: 'J.Brissett', 5: 'J.Brissett', 6: 'J.Brissett', 7: 'J.Brissett'}; QBs on report none → ok
- Game flow: spread +7 total 54.5 [ESPN scoreboard / leg file] → note: underdog; pass volume up, efficiency risk
- Workload: weekly targets {1: 13, 2: 10, 3: 11, 4: 12, 5: 10, 6: 9, 7: 13} (CV 0.14); weekly yds {1: 95, 2: 41, 3: 75, 4: 31, 5: 66, 6: 53, 7: 111} → ok
- Source discrepancies: PFR cache Oct 29 (fresh pull 403); PFR G≈5 lags pbp; Sharp vs StatRankings man-rank DIFFERS for DAL; film: chart UNVERIFIED (2/6 match); alignment unclear.
- Unsupported model mechanics: route participation per dropback GAP (2026 participation 404); TE alignment GAP; TE/slot→LB/S 8A mapping awaiting Rico ruling → disclosed, no mechanic credited
- 8A film read: UNVERIFIED → alignment/route item GAP (disclosed); counts only if every cited play matches nflverse pbp (qtr/clock, receiver, yds)
- Possible-error buckets: Efficiency, Source quality, Model capability. No causation assigned (no box score).

### Trey McBride (ARI vs DAL) — recyds · rung None @ None
- **PHASE 4: CAUTION** (2 flags) · Phase 3: PASS (8A PENDING)
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: ARI OL on report [('Jon Gaines II', 'G', 'Out'), ('Hjalte Froholdt', 'C', 'Questionable')]; DAL defense sack rate 4.1% (rank 26/32); ARI OL allows 5.0% [pbp, ESPN] → FLAG
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q [('Tip Reiman', 'TE', 'Out')] (IR excluded: already in baseline); redistribution unverified (no boost) → FLAG
- Backup-QB: primary passer by week {1: 'J.Brissett', 2: 'J.Brissett', 3: 'J.Brissett', 4: 'J.Brissett', 5: 'J.Brissett', 6: 'J.Brissett', 7: 'J.Brissett'}; QBs on report none → ok
- Game flow: spread +7 total 54.5 [ESPN scoreboard / leg file] → note: underdog; pass volume up, efficiency risk
- Workload: weekly targets {1: 13, 2: 10, 3: 11, 4: 12, 5: 10, 6: 9, 7: 13} (CV 0.14); weekly yds {1: 95, 2: 41, 3: 75, 4: 31, 5: 66, 6: 53, 7: 111} → ok
- Source discrepancies: PFR cache Oct 29 (fresh pull 403); PFR G≈5 lags pbp; Sharp vs StatRankings man-rank DIFFERS for DAL; film: chart UNVERIFIED (2/6 match); alignment unclear.
- Unsupported model mechanics: route participation per dropback GAP (2026 participation 404); TE alignment GAP; TE/slot→LB/S 8A mapping awaiting Rico ruling → disclosed, no mechanic credited
- 8A film read: UNVERIFIED → alignment/route item GAP (disclosed); counts only if every cited play matches nflverse pbp (qtr/clock, receiver, yds)
- Possible-error buckets: Efficiency, Source quality, Model capability. No causation assigned (no box score).

### Tyler Warren (IND vs JAX) — recyds · rung None @ None
- **PHASE 4: GAP** (1 flags) · Phase 3: GAP
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: IND OL on report none; JAX defense sack rate 4.7% (rank 23/32); IND OL allows 7.1% [pbp, ESPN] → ok
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q [('Anthony Gould', 'WR', 'Out'), ('Drew Ogletree', 'TE', 'Questionable')] (IR excluded: already in baseline); redistribution unverified (no boost) → FLAG
- Backup-QB: primary passer by week {1: 'D.Jones', 2: 'D.Jones', 3: 'D.Jones', 4: 'D.Jones', 5: 'D.Jones', 6: 'D.Jones', 7: 'D.Jones'}; QBs on report none → ok
- Game flow: spread +10 total 46.5 [ESPN scoreboard / leg file] → note: underdog; pass volume up, efficiency risk
- Workload: weekly targets {1: 5, 2: 7, 3: 10, 4: 5, 5: 9} (CV 0.32); weekly yds {1: 13, 2: 21, 3: 55, 4: 41, 5: 83} → ok
- Source discrepancies: PFR cache Oct 29 (fresh pull 403); PFR G≈5 lags pbp; Sharp vs StatRankings man-rank DIFFERS for JAX
- Unsupported model mechanics: route participation per dropback GAP (2026 participation 404); TE alignment GAP; TE/slot→LB/S 8A mapping awaiting Rico ruling → disclosed, no mechanic credited
- 8A film read: UNVERIFIED → alignment/route item GAP (disclosed); counts only if every cited play matches nflverse pbp (qtr/clock, receiver, yds)
- Possible-error buckets: Source quality, Model capability. No causation assigned (no box score).

### Zay Flowers (BAL vs BUF) — recyds · rung None @ None
- **PHASE 4: CAUTION** (2 flags) · Phase 3: PASS
- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame).
- OL/rusher: BAL OL on report [('Olaivavega Ioane', 'G', 'Out')]; BUF defense sack rate 4.2% (rank 25/32); BAL OL allows 7.6% [pbp, ESPN] → FLAG
- Injuries/replacement: player active (not on report); skill teammates Out/Doubtful/Q none (IR excluded: already in baseline); redistribution unverified (no boost) → ok
- Backup-QB: primary passer by week {1: 'L.Jackson', 2: 'L.Jackson', 3: 'L.Jackson', 4: 'L.Jackson', 5: 'T.Huntley', 6: 'T.Huntley', 7: 'T.Huntley'}; QBs on report none → FLAG (starter changed this season)
- Game flow: spread +3 total 54.5 [ESPN scoreboard / leg file] → ok
- Workload: weekly targets {1: 6, 3: 6, 4: 10, 5: 9, 6: 11, 7: 11} (CV 0.26); weekly yds {1: 150, 3: 84, 4: 118, 5: 53, 6: 66, 7: 137} → ok
- Source discrepancies: PFR cache Oct 29 (fresh pull 403); PFR G≈5 lags pbp
- Unsupported model mechanics: route participation per dropback GAP (2026 participation 404) → disclosed, no mechanic credited
- 8A film read: UNVERIFIED → alignment/route item GAP (disclosed); counts only if every cited play matches nflverse pbp (qtr/clock, receiver, yds)
- Possible-error buckets: Efficiency, Source quality, Model capability. No causation assigned (no box score).