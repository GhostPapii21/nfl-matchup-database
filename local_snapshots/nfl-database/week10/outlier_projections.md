# Week 10 NFL Outlier Projections

> **Updated 2026-11-05 ~10:14 AM ET** — Weekly Outlier routine merge.
>
> TNF Outlier props **merged** from `outlier/outlier_props_2026-11-05.csv` (**83 rows**, 18 players: JAC/BAL full-ish + CIN@ATL partial). Other Sunday + MNF **not covered** (Outlier UI slowness — see `outlier/outlier_props_2026-11-05_notes.md`). PFR advanced defense at `defense/pfr_defense_advanced_2026-11-05.csv` (787 rows; live 403 → Nov 4 cache). Key players refreshed at `key_players.md` + `week10/key_players.csv`. Do not place bets from this file alone — full gate still required. No bets placed this run.


## Meta / sources (cite freshness)

| Source | Path | Freshness |
|---|---|---|
| Matchup cards (PRIMARY) | `cards/2026-11-05_thu0600.md` | Built 2026-11-05T06:10 ET |
| ESPN DK consensus lines | cards + `runs/2026-11-05_matchup_run/lines.json` | 2026-11-05T06:08 ET |
| Practice digest | `digests/practice_2026-11-04.md` | ~5:05 PM ET Nov 4 |
| Injury sweep | `week10/injury_sweep_2026-11-04.md` | Nov 4 12:10 + 5:00 PM ET |
| TNF r6 research | `runs/2026-11-05_JAX@BAL_r6/` | Odds pull ~2:59 PM ET Nov 4 (12 credits) |
| Fagnano / Henry / BAL secondary / JAX usage / Hamilton IR / SEA backup QB | `week10/{fagnano,bal_secondary,jax_usage,davon_hamilton,sea_backup_qb,...}` | Nov 4 AM–PM |
| Player type labels | `week8/player_types/USER_LABELS.md` | Week 8 taxonomy (still authoritative types) |
| Key players list | `key_players.md` + `week10/key_players.csv` | **Refreshed 2026-11-05 ~10:10 AM ET** |
| Outlier props | `outlier/outlier_props_2026-11-05.csv` | **83 rows** — TNF + partial CIN@ATL; rest skipped |
| PFR advanced defense | `defense/pfr_defense_advanced_2026-11-05.csv` (+ `_latest.csv`) | Cache ~Nov 4 07:02 ET; live pull 403 |

## Standing Rico rules applied in every section

- **Passing yards OFF** all slips (overs/unders/alts). Pass volume may appear for script only.
- Backs under **60% carries** = do-not-play on rush overs.
- No receiving leg without a **verified main defender** (flag **MISSING** if numbers absent).
- **Questionable** = one-rung drop / flag for 90-min check, not auto-cut.
- Backup/new QB flags: **BAL Fagnano, PHI Milton, SEA Lock, CLE Sanders?, ARI Minshew** — pass-catcher overs caution.
- **SCHEME_EDGE / +1/+3 tiers are flags, not cuts.**
- Anytime TDs on separate slips.
- Half/quarter spreads must match script.

## Outlier status

- **TNF (JAX@BAL):** Merged — see game §1 “Outlier vs model disagreement”.
- **CIN @ ATL (Madrid):** Partial (~34 rows) in CSV — see short note under §10. Not a full market set.
- **All other Sunday + MNF:** **Not covered** this pull (Outlier Prop Finder virtual-scroll / dropdown flaky). Use card/DK consensus; fill L5/L10 from game logs if needed before Sunday slips.
- Gaps: H2H mostly blank; PP often −119; Fagnano & Rodriguez Jr. have no Outlier props; Flowers rec-yds Over side missing from scroll capture.
- Notes file: `outlier/outlier_props_2026-11-05_notes.md`.

---

## Global Q-player watchlist (90-minute / Friday designation check)

**TNF (inactives ~6:50 PM ET tonight):**
- JAX: Bhayshul Tuten (RB, DNP 3 straight), Travon Walker (DE)
- BAL: Nate Wiggins (CB — FP on NFL.com / Q illness on ESPN conflict), Calais Campbell (DT DNP Wed)

**Sunday / SNF / MNF (held to Fri designations + 90-min):**
- CLE: Deshaun Watson (QB, concussion) → Sanders start watch
- SEA: Drew Lock (QB, elbow Q) — starts planned; throw-volume check
- DAL: George Pickens (WR), Jake Ferguson (TE), Tyler Smith (G), many others Q
- DET: Amon-Ra St. Brown (WR, ribs), Jack Campbell (LB Doubtful), D.J. Reed (CB)
- KC: Rashee Rice (WR), Travis Kelce (TE)
- NYJ: Garrett Wilson (WR, concussion), Breece Hall (RB), Mason Taylor (TE)
- NE: A.J. Brown (WR), TreVeyon Henderson (RB), Hunter Henry (TE)
- PHI: DeVonta Smith (WR), Dontayvion Wicks (WR), Saquon Barkley (RB)
- TB: Emeka Egbuka (WR), Kenny Gainwell (RB)
- MIA: Jaylen Wright (RB), Zach Sieler (DT), Chop Robinson (LB)
- NYG: Cam Skattebo (RB), Andrew Thomas / Jermaine Eluemunor (OT)
- ARI: Bam Knight (RB), Michael Wilson (WR)
- SF: Christian McCaffrey, Mike Evans, Deebo Samuel (all DNP Wed)
- ATL: Brian Robinson Jr. (RB)
- BUF: DJ Moore, Joshua Palmer (WR); Spencer Brown (OT)
- MIN: Christian Darrisaw (OT), Kyler Murray (QB) listed Q on ESPN card — verify role
- Plus full card Q lists per game below

---

# 1. JAX @ BAL — Thu Nov 5, 8:15 PM ET  ★ DEEPEST

**Line (ESPN DK 06:08 ET):** JAX −10 / BAL +10, total **39.5**.  
**Weather:** Open, 66–68°F, wind ~3 mph, precip chance up to 34%.  
**Script lean:** JAX **BLOWOUT FAVORITE** (pass early → run late; late-clock JAX pass overs blocked). BAL **big underdog** with backup QB → run-lean / short-pass / limited scoring.  
**Starter flags:** BAL **Joe Fagnano** (UDFA) starts; Huntley season-ending; Lamar out indefinitely. JAX Lawrence healthy. Hawkins (BAL S) **OUT**. DaVon Hamilton (JAX DT) + Eric Murray (JAX S) **IR**.

### Key players — types + low / mid / high (card opportunity + r6/research; ESTIMATE)

| Player | Type label | Stat | Low | Mid | High | Notes |
|---|---|---|---|---|---|---|
| Derrick Henry | POWER/VOLUME BACK (BAL lean-run) | rush yds | 35 | **50–55** | 70 | ~14–16 car base; JAX 3.4 YPC allow (stale +0.15–0.35 post-Hamilton IR). N1 OK (≥60% carries). |
| Derrick Henry | | rush+rec | 40 | 55–60 | 80 | Rec limited vs JAX RB allow 3.2 YPT |
| Justice Hill | SAFETY VALVE | targets / rec | 3/2 | **5–6 / 3–4** | 8/5 | Fagnano checkdown magnet (wk8 6 tgt) |
| Zay Flowers | WR HIGH-VOLUME | targets / rec / rec yds | 5/2/25 | 7/4/**44** | 10/6/70 | **Backup-QB flag**; Flowers 0/4 from Fagnano wk8 |
| Mark Andrews | TE (no USER TE-AS-REC label) | targets / rec / rec yds | 2/1/8 | 4/2–3/**18** | 6/4/35 | Backup-QB flag; JAX hard on TE (4.8 YPT) |
| Rashod Bateman | WR EXPLOSIVE | targets / rec yds | 2/10 | 3–4/**26** | 5/45 | Deep-right fit vs JAX leak; tiny Fagnano sample |
| Parker Washington | WR EXPLOSIVE (JAX WR1) | targets / rec / rec yds | 5/3/40 | **7–9 / 5 / 64–76** | 11/7/100 | L3 share ~23%; BAL deep-middle / Humphrey leak |
| Brenton Strange | TE-AS-RECEIVER | targets / rec / rec yds | 4/3/30 | **6 / 5 / 49–58** | 8/7/80 | Top-3 every game; vs Starks / Hawkins replacement |
| Jakobi Meyers | WR (no high-vol label) | targets / rec yds | 2/15 | 3–4 / **26–31** | 6/50 | LP Wed, no designation; volume x0.64 injury |
| Bhayshul Tuten [Q] | — | rush yds | 0 (out) | 35–45 if limited | 70 | **60% rule risk**; DNP 3 straight |
| Chris Rodriguez Jr. | — | rush yds | 20 | **50–60 if Tuten OUT** | 75 | Lead-back candidate if Tuten sits |
| Trevor Lawrence | — | rush yds | 0 | 8–12 | 25 | Pass yds noted only (~208–246) — **NOT a slip** |

Pass volume note only: JAX ~29 dropbacks / BAL ~37 — **passing-yards props stay off**.

### Targets to pursue (actionable for TNF)

| Player | Prop | Side | Suggested rung | Reason | Flags |
|---|---|---|---|---|---|
| Brenton Strange | Receptions | **OVER 3.5 (4+)** | Full / mid | r6: Pin −119, model p .550, §7 3/4 PASS, last-2 DOWNGRADE only. Primary defenders: Starks (12.2 YPT) + Hawkins OUT → Wallace/Jackson. | last-2 downgrade; OUTLIER_PENDING |
| Brenton Strange | Rec yards | **OVER 35.5** | Full | r6 Pin −113, model .561, §7 4/4. 40+ alt (+114 FD) best value per bal_secondary. | OUTLIER_PENDING |
| Derrick Henry | Rush yards | **UNDER 69.5** | Mid (edge thinner) | r6 FD −114, model p .735, §7 3/4, N1 exempt (under). Scenario = carry-count + Fagnano script. | Hamilton/Murray IR flag (+explosive risk); OUTLIER_PENDING |
| Derrick Henry | Rush yards | **40+ (o39.5)** floor | Low rung only | §7 4/4; hits −130 cap at DK −598 — price caution, not a primary. | Cap130; OUTLIER_PENDING |
| BAL team total | Under 14.5 | UNDER | Mid / secondary | r6 FD −122, §7 3/4 [30,10,13,10]. Matches Fagnano drive sim (~13.5 pts Rico case). | No game model p; OUTLIER_PENDING |
| JAX 1Q | −2.5 / 1Q ML | JAX | Low / singles-only | §7 3/4 PASS but last-2 DOWNGRADE. Script = Fagnano pressure early. | Downgrade; half/Q must match script |
| Parker Washington | Rec yards | Lean OVER low alt only | Low / hold main | Volume WR1 vs BAL deep leak; main o63.5 **FAILS §7 2/4** and model opposes (−8.4). o39.5 passes no-Wk8 window only + hits −130. | §7 fail on main; OUTLIER_PENDING |
| Jakobi Meyers | Rec yards | UNDER ~40.5 if priced | Low | Injury volume cut; LP no designation. Defender map OK if he plays. | Q-ish / 90-min; OUTLIER_PENDING |

### Cuts / holds

| Item | Reason |
|---|---|
| **All BAL pass-catcher overs** (Flowers, Andrews, Bateman, Lane, Hill overs as primary) | **Backup-QB flag (Fagnano)**; Flowers 0 catches on 4 Fagnano targets wk8. Hill/Bateman only as low-rung if Rico overrides sample. |
| **Any passing-yards leg** (Lawrence / Fagnano) | Rico ban — off completely. |
| **Tuten rush overs** | Q + likely fails 60% carry rule if active in a split; void/risk if out. |
| **JAX rush yards overs** (team / CRod unless Tuten OUT confirmed) | Card caution: BAL run suppression 3.64 YPC; committee risk. |
| **BAL rush overs / Henry o59.5+** | JAX run D still below league even post-IR; model fails §7 on o59.5. |
| **JAX −10 / −9.5 / 1H −6.5** | §7 FAIL; 1H −6.5 needs override. |
| **Washington o63.5 / 5+ rec** | §7 FAIL + model against. |
| **BAL TE yards overs** | JAX allows only 4.8 YPT to TEs. |
| Anytime TD legs | Separate slips only; not mixed here. |

### Defenders (PFR `pfr_defense_advanced_2026-11-05.csv`, cache ~Nov 4)

**BAL coverage leaks for JAX receivers:** Marlon Humphrey CB 42 tgt / 8.5 YPT / 359 yds; Malaki Starks S 20 / **12.2** / 244; Nate Wiggins 36 / 6.1 / 221; Kyle Hamilton 34 / 6.0 / 204. Hawkins OUT → Starks/Wallace/Jackson over the top is the seam/deep-middle path for Strange + Washington posts.

**JAX coverage (BAL receivers — mostly for fade context under backup QB):** Jarrian Jones CB 50 / 7.1 / 357; Montaric Brown CB 18 / **14.2** / 256 (small-n bomb); Oluokun LB 36 / 6.4 / 232.

### Outlier vs model disagreement (MERGED 2026-11-05 ~10:15 AM ET)

Source: `outlier/outlier_props_2026-11-05.csv` — **49 rows, 9 players, TNF JAX@BAL only so far** (Sunday/MNF still appending from browser). Books view: FanDuel / PrizePicks / DraftKings. Full-game props preferred.

| Player | Market | Outlier line / side shown | L5 / L10 / 2026 | Model / card lean | Verdict |
|---|---|---|---|---|---|
| Derrick Henry | Rushing Yards | o67.5 (−110 DK), L5 **40%** / L10 **70%** / 2026 63% | Card mid **50–55**; r6 lean **UNDER 69.5** (p~.735) | **DISAGREE:** Outlier L10 favors the over at 67.5; model/script still lean under on carry-count + Fagnano. Edge thinner post Hamilton/Murray IR — flag, not cut. Prefer U69.5 only if price ≥ −115; else pass. |
| Derrick Henry | Rush + Rec Yds | o78.5 (−113 FD), L5 40% / L10 70% | Mid 55–60 | Same disagreement as rush — Outlier L10 hot, model mid below line. Soft pass / wait inactives. |
| Derrick Henry | Rushing Attempts | u17.5 (−140 FD) L5 60% / L10 40% | Card ~14–16 carries | Aligned with under on attempts; supports rush-under script more than rush-over. |
| Brenton Strange | Receptions | o3.5 (−122 FD), L5 **60%** / L10 **40%** / 2026 43% | r6 OVER 3.5 (4+), model .550, §7 3/4 | **PARTIAL AGREE on side, L10 soft.** Last-2 downgrade already flagged. Still top TNF receiving target; Starks 12.2 YPT + Hawkins OUT. |
| Brenton Strange | Receiving Yards | o35.5 (−113 FD), L5 **80%** / L10 **60%** / 2026 57% | r6 OVER 35.5, model .561, §7 4/4 | **AGREE.** Strongest Outlier confirm of the card. 40+ alt still best value. |
| Brenton Strange | Receiving Targets | u5.0, L5 20% / L10 30% | Mid ~6 targets | Outlier under on 5.0 targets conflicts with mid-6 proj — treat targets market as noisy; use rec/yds. |
| Parker Washington | Receiving Yards | o63.5 (−113 FD), L5 40% / L10 **70%** / 2026 57% | Main o63.5 **§7 FAIL** + model against; low alts only | **DISAGREE with Outlier L10.** Keep main cut; Outlier L10 alone doesn't clear §7. Low alt (o39.5) only. |
| Parker Washington | Receptions | o4.5 (−102), L5 20% / L10 60% | Mid ~5 rec | Borderline; L5 weak. Prefer Strange. |
| Jakobi Meyers | Receiving Yards | u39.5 (−113 DK), L5 60% / L10 60% | Mid 26–31 (injury x0.64) | **AGREE under** on 39.5 — volume thinned; not a primary. |
| Jakobi Meyers | Receptions | u3.5 (−166 FD) favored; o3.5 +124 | Mid 3–4 | Market prices under; skip both sides at this juice. |
| Zay Flowers | Receptions | o4.5 (−108 FD), L5 80% / L10 70% / 2026 86% | Backup-QB flag; Flowers 0/4 from Fagnano Wk8 | **DISAGREE / FADE.** Outlier hit rates are Lamar-era. Backup-QB flag cuts overs. |
| Mark Andrews | Receptions | o2.5 (−130 FD), L5 80% / L10 80% / 2026 88% | Backup-QB + JAX hard on TE 4.8 YPT | **DISAGREE / FADE** same as Flowers — Lamar-era rates. Low rung only if Fagnano checkdowns spike. |
| Mark Andrews | Receiving Yards | o18.5 (−113 FD), L5 60% / L10 70% | Mid 18 | Line ≈ mid; juice not worth with backup QB + tough TE matchup. |
| Bhayshul Tuten | Rushing Yards | o63.5 / u63.5 both listed; L5 over 80% / under 20% | Q, DNP 3 straight; 60% rule risk | **HOLD to 6:50 PM inactives.** If active, likely DNP rush overs. Rodriguez lead if OUT. |
| Trevor Lawrence | Passing Yards | 235.5 both sides ~50% | Pass yds **OFF slips** (Rico) | Ignore for slips; script note only (~208–246 mid). |
| Trevor Lawrence | Rushing Yards | o12.5 (−113), L5 40% / L10 40% | Mid 8–12 | No clear edge; skip. |

**TNF Outlier confirm ranking after merge:** (1) Strange o35.5 rec yds, (2) Strange o3.5 rec (L10 soft), (3) Henry U69.5 still model-side but Outlier L10 fights it — thinner, (4) Washington main CUT despite L10, (5) Flowers/Andrews overs FADE (backup QB).


### Key players — low / mid / high

| Player | Type | Stat | Low | Mid | High | Notes |
|---|---|---|---|---|---|---|
| Tyler Allgeier | SAFETY VALVE → de facto RB1 | rush yds | 25 | **45–55** | 75 | Love IR, Conner IR; carry share up but SEA run D 3.39 YPC — **rush UNDER lean** vs SEA |
| Bam Knight [Q] | — | rush yds | 0 | 20–30 | 45 | Q; split risk → 60% rule fail if both active |
| Trey McBride | TE-AS-RECEIVER | targets / rec yds | 6/40 | **9–11 / 65–75** | 14/100 | Minshew flag; SEA hard on TE (5.6 YPT) |
| Jaxon Smith-Njigba | — (SEA WR1) | targets / rec / rec yds | 6/4/50 | **10–11 / 7–8 / 90–110** | 14/10/150 | 44% of Lock targets wk2; **HOLD overs until Fri Lock throw volume** |
| Emanuel Wilson / SEA RB | — | rush yds | 40 | **60–75** | 100 | Backup-QB → run share up; role split (Wilson/Price/Charbonnet) unclear |
| Cooper Kupp / AJ Barner | — | rec yds | low | mid hold | — | Low Lock share historically |

### Targets to pursue

| Player | Prop | Side | Rung | Reason | Flags |
|---|---|---|---|---|---|
| ARI RB (Allgeier / Knight) | Rush yards | **UNDER** (line TBD) | Mid candidate | SEA run suppression 3.39 YPC; card caution cut ARI rush. Need live line + 60% check. | OUTLIER_PENDING; Knight Q |
| Game total | Under ~39.5–41.5 | UNDER lean | Flag only until re-line | Lock elbow + run script; sea_backup_qb lean under | Backup QB both sides-ish; OUTLIER_PENDING |
| SEA −8.5 | Lean ARI / pass | — | Do not chase stale −11.5; fair ~−8 to −9.5 Lock / −5–6 Milroe | Lock Q elbow |

### Cuts / holds

- **ALL SEA pass-catcher overs** held to Friday Lock status; if Milroe → kill overs, consider JSN unders.
- **ARI pass-catcher overs** — Minshew/new-QB flag + SEA coverage (Witherspoon 4.9 YPT) stout.
- **SEA RB unders** — not recommended (run share rises with backup QB).
- Passing yards off.

### Defenders (PFR)

SEA: Josh Jobe 37/6.6/246; Witherspoon 47/**4.9**/232; Ernest Jones LB 42/5.0/210.  
ARI: Mack Wilson LB 27/**10.0**/269; Budda Baker 27/7.3/197; Denzel Burke 33/6.4/210.

### Outlier vs model

**OUTLIER_PENDING**

---

# 3. NYJ @ KC — Sun Nov 8, 1:00 PM ET  ★ PRIORITY (blowout)

**Line:** KC −10, total **47.5**.  
**Weather:** Open, 64–67°F, wind ~8 mph, dry.  
**Script lean:** KC **BLOWOUT FAVORITE** (late pass overs blocked). NYJ **big underdog**.  
**Injuries:** NYJ Garrett Wilson Q (concussion), Breece Hall Q, Mason Taylor Q. KC Rice Q, Kelce Q, Omarr Norman-Lott OUT.

### Key players

| Player | Type | Stat | Low | Mid | High | Notes |
|---|---|---|---|---|---|---|
| Kenneth Walker III | POWER + RUSH-RECEIVE | rush yds | 60 | **90–110** | 140 | ~90% carry share L3 ≈ 21 car; clears 60% |
| Xavier Worthy | — | targets / rec yds | 4/30 | 6/**50–60** | 9/90 | Rice Q → share up if Rice sits |
| Travis Kelce [Q] | TE-AS-RECEIVER | targets / rec yds | 0 | 5–6 / 45–55 | 8/80 | **Held to Fri**; ankle |
| Braelon Allen | — | rush yds | 30 | 55–70 | 90 | ~77% L3 if Hall limited — **recheck 60%** vs Hall split |
| Garrett Wilson [Q] | WR HIGH-VOLUME | — | HOLD | HOLD | HOLD | Concussion protocol |
| Omar Cooper Jr. | WR EXPLOSIVE | targets | 3 | 5–7 if Wilson out | 10 | WR1 candidate if Wilson sits |

### Targets to pursue

| Player | Prop | Side | Rung | Reason | Flags |
|---|---|---|---|---|---|
| Kenneth Walker III | Rush yards | OVER (line TBD) | Mid–full if priced ~75–85 | Blowout script + 90% share + NYJ 3.91 YPC allow | Need defender N/A for rush; OUTLIER_PENDING |
| NYJ rush yards / Hall-Allen | Rush | **CUT overs** | — | KC run suppression **3.36 YPC**; Hall+Allen split → 60% do-not-play | Split |
| Worthy | Rec yards / rec | Lean OVER if Rice out | Low–mid | Share bump; map vs Stephens / Thomas | Rice 90-min; MISSING primary if not mapped; OUTLIER_PENDING |

### Cuts / holds

- Wilson, Kelce, Rice, Mason Taylor — held.
- NYJ RB overs — KC run D + 60% rule.
- KC late pass / passing yards — blowout + ban.
- Passing yards off.

### Defenders (PFR)

KC: Sneed 44/7.8/341; Delane 26/**9.5**/248; Bolton LB 23/7.9/182.  
NYJ: Stephens 42/7.5/315; Thomas 44/4.5/199; Fitzpatrick S 15/**12.7**/191 (small n).

### Outlier vs model

**OUTLIER_PENDING**

---

# 4. DET @ MIA — Sun Nov 8, 1:00 PM ET  ★ PRIORITY

**Line:** DET −7, total **50.5**.  
**Weather:** Open/canopy, **82–83°F**, wind ~10 mph.  
**Script lean:** DET **BLOWOUT FAVORITE**; MIA big underdog. Soft MIA WR/TE YPT (9.8 / 8.6).  
**Injuries:** Amon-Ra St. Brown Q (ribs); Kerby Joseph OUT; Jack Campbell Doubtful; MIA Wright Q, many DL Q.

### Key players

| Player | Type | Stat | Low | Mid | High | Notes |
|---|---|---|---|---|---|---|
| Jahmyr Gibbs | POWER + RUSH-RECEIVE | rush yds | 70 | **95–110** | 140 | ~76% carries ≈ 21; clears 60% |
| Jahmyr Gibbs | | rush+rec | 90 | 120–140 | 180 | ~6 tgt L3 |
| Amon-Ra St. Brown [Q] | WR HIGH-VOLUME | targets / rec yds | 0 / HOLD | 9–11 / 80–95 | 14/120 | **Held to Fri**; if out → Jamo + LaPorta up |
| Jameson Williams | WR EXPLOSIVE | targets / rec yds | 4/40 | 7/**60–75** | 10/110 | Soft MIA WR YPT 9.8; primary CB Chris Johnson 9.8 YPT |
| Sam LaPorta | — | targets / rec yds | 3/25 | 5/**45–55** | 8/80 | MIA TE YPT 8.6 soft |
| Ollie Gordon II | — | rush yds | 40 | **60–75** | 100 | ~71% if Wright sits — **60% check** |
| Greg Dulcich / Malik Washington | — | targets | 4 | 6–7 | 9 | DET TE YPT 8.6 soft for Dulcich |

### Targets to pursue

| Player | Prop | Side | Rung | Reason | Flags |
|---|---|---|---|---|---|
| Jahmyr Gibbs | Rush / rush+rec | OVER | Mid–full | Volume + blowout script; MIA 4.09 YPC | OUTLIER_PENDING |
| Jameson Williams | Rec yards | OVER (if ARSB limited/out) | Low–mid | Soft MIA; Johnson 30 tgt / 9.8 YPT | ARSB 90-min; verify main defender; OUTLIER_PENDING |
| Sam LaPorta | Rec yards | Lean OVER | Low | Soft TE matchup | Need line; OUTLIER_PENDING |
| Ollie Gordon | Rush | OVER if Wright out + ≥60% | Low | Carry bump | Wright Q; 60% gate |

### Cuts / holds

- St. Brown until Friday.
- DET late pass overs (blowout).
- Passing yards off.
- MIA OL Proctor Q + DET pressure 18% → MIA pass volume caution.

### Defenders (PFR)

MIA: Chris Johnson 30/**9.8**/293; Taaffe S 22/**11.6**/256; Jason Marshall 23/**10.9**/250.  
DET: D.J. Reed 38/**9.5**/361 (Q himself); McCreary 46/7.6/348; Jack Campbell LB 41/7.1/290 (Doubtful).

### Outlier vs model

**OUTLIER_PENDING**

---

# 5. DAL @ IND — Sun Nov 8, 1:00 PM ET  ★ PRIORITY

**Line:** DAL −5.5, total **51.5**. Retractable roof (status TBD), 52–55°F.  
**Script lean:** DAL moderate favorite; IND moderate underdog. Soft IND run D (4.76 YPC) and DAL run D (5.06).  
**Injuries:** Pickens Q, Ferguson Q, many DAL Q; IND Pierce on IR → Downs/Allen/Warren up.

### Key players

| Player | Type | Stat | Low | Mid | High | Notes |
|---|---|---|---|---|---|---|
| CeeDee Lamb | WR HIGH-VOLUME | targets / rec yds | 9/70 | **12–14 / 95–110** | 16/140 | 39% L3 share; Pickens Q bump |
| George Pickens [Q] | WR HIGH-VOLUME | — | HOLD | HOLD | HOLD | Fri check |
| Javonte Williams | POWER/VOLUME | rush yds | 50 | **70–85** | 110 | ~70% carries; IND soft run D |
| Jonathan Taylor | POWER/VOLUME | rush yds | 45 | **65–80** | 110 | L3 carry **59% — FAILS 60% rule** for rush overs unless share clears |
| Keenan Allen / Josh Downs | — | targets | 6 | 8–9 | 12 | Pierce IR bump; map vs Bland (8.8 YPT) |
| Jake Ferguson [Q] | — | — | HOLD | — | — | Spann-Ford backup-TE only under depth rule |

### Targets to pursue

| Player | Prop | Side | Rung | Reason | Flags |
|---|---|---|---|---|---|
| CeeDee Lamb | Rec / rec yds | OVER | Mid | Volume king; IND Walley 7.4 YPT / Sauce 9.4 YPT (pick matchup) | Verify main defender (Walley Q); OUTLIER_PENDING |
| Javonte Williams | Rush yards | OVER | Mid | Soft IND run D + 70% share | OL Tyler Smith Q flag; OUTLIER_PENDING |
| Jonathan Taylor | Rush | **HOLD / cut overs** until ≥60% | — | L3 59% + McGowan 25% | 60% rule |

### Cuts / holds

- Pickens, Ferguson held.
- Taylor rush overs until carry share clears 60%.
- Passing yards off.
- Two-WR same QB: not banned (Rico rejected that rule) but price-shop.

### Defenders (PFR)

IND: Walley 40/7.4/295 (Q); Sauce 27/**9.4**/254; Davis-Gaither LB 22/8.6/190.  
DAL: Bland 43/**8.8**/380; Downs DB 23/**9.9**/227 (DNP Wed — file update).

### Outlier vs model

**OUTLIER_PENDING**

---

# 6. NYG @ PHI — Sun Nov 8, 1:00 PM ET  ★ PRIORITY

**Line:** PHI +3.5 (!), total **38.5** — NYG −3.5 favorite.  
**Weather:** Open, 58–59°F, wind **~12 mph gusts 19**.  
**Script lean:** NYG moderate favorite; PHI moderate underdog with **Joe Milton** starting (backup-QB flag on all PHI pass catchers). Low total → run/short game.  
**Injuries:** Saquon Q, Smith Q, Wicks Q; NYG Skattebo Q, both starting OTs Q.

### Key players

| Player | Type | Stat | Low | Mid | High | Notes |
|---|---|---|---|---|---|---|
| Malik Nabers | — | targets / rec yds | 8/60 | **11–12 / 85–100** | 15/130 | 36% share; PHI Woolen 8.9 YPT leak |
| Saquon Barkley [Q] | — | rush yds | 0 | 40–55 if limited | 80 | L3 only **32%** carries — **fails 60%** even if active; Dameon Pierce 42% |
| Dallas Goedert | TE-AS-RECEIVER | targets / rec yds | 3/20 | 5–6 / 40 | 8/65 | **Backup-QB + NYG hard on TE (5.4 YPT)** → cut overs |
| Makai Lemon | SAFETY VALVE | targets | 4 | 7–8 | 11 | Milton checkdowns; Smith/Wicks out bump |
| Cam Skattebo [Q] | — | rush | HOLD | — | — | DNP; backfield murky |
| Isaiah Likely (NYG TE?) | — | — | card lists Likely 23% NYG — verify roster/label | | | Card anomaly — confirm before any leg |

### Targets to pursue

| Player | Prop | Side | Rung | Reason | Flags |
|---|---|---|---|---|---|
| Malik Nabers | Rec yards / rec | OVER | Mid | Volume + Woolen/Mukuba leaks (Mukuba S 12.2 YPT) | Wind flag; OUTLIER_PENDING |
| PHI pass catchers | Any over | **CUT / hold** | — | Milton backup-QB flag | Backup QB |
| Saquon rush overs | — | **CUT** | — | <60% L3 + Q | 60% rule |
| Game total Under 38.5 | UNDER lean | Low–mid | Backup QB + wind + OL injuries both sides | OUTLIER_PENDING |

### Cuts / holds

- All PHI receiving overs (Milton).
- Saquon rush overs (share + Q).
- PHI TE yards (NYG 5.4 YPT).
- Passing yards off.
- NYG OL both Q → sacks/pressure lean vs NYG pass volume.

### Defenders (PFR)

PHI: Woolen 45/**8.9**/401; Mukuba S 23/**12.2**/281; Mitchell 50/5.7/286; DeJean 38/5.7/218.  
NYG: Newsome 29/6.7/193; Nubin 18/8.5/153; Banks 32/4.7/149 (stout).

### Outlier vs model

**OUTLIER_PENDING**

---

# 7. LAR @ WSH — Sun Nov 8, 1:00 PM ET  ★ PRIORITY

**Line:** LAR −5.5, total **47.5**. Wind ~12 mph gusts 19.  
**Script lean:** LAR moderate favorite. **WSH both starting DTs season-ending (Kinlaw, Payne)** → run-D flag for LAR RBs. Card still lists WSH 3.53 YPC allow (pre-injury stale — **boost LAR rush**).  
**Caution:** WSH blitz 44% / Panthers-rule lean unders on LAR pass volume; LAR hard on TE (5.3 YPT).

### Key players

| Player | Type | Stat | Low | Mid | High | Notes |
|---|---|---|---|---|---|---|
| Kyren Williams | RUSH-RECEIVE + SAFETY VALVE | rush yds | 45 | **65–75** | 100 | L3 carry **51%** — **fails 60%** alone; committee with Corum 45% |
| Blake Corum | — | rush yds | 35 | 50–60 | 85 | 45% L3 — also fails 60% solo |
| Puka Nacua | WR HIGH-VOLUME | targets / rec yds | 8/70 | **11–12 / 95–110** | 15/140 | Primary vs Robertson/Douglas |
| Colby Parkinson [Q] | — | — | HOLD | Soft WSH TE 9.4 YPT if active | Q |

### Targets to pursue

| Player | Prop | Side | Rung | Reason | Flags |
|---|---|---|---|---|---|
| LAR RB rush (Kyren or Corum) | Rush | **Committee caution** — prefer rush+rec Kyren or wait clear lead | Low | DT injuries open run; but 51/45 split = 60% do-not-play on solo rush overs | 60% rule; OUTLIER_PENDING |
| Puka Nacua | Rec / rec yds | OVER lean | Mid | Volume; WSH Amik 6.9 YPT / Douglas 6.8 — not a huge leak; blitz → checkdowns help Puka | Panthers-rule pass volume; OUTLIER_PENDING |
| WSH TE (Okonkwo) | Rec yards | **CUT overs** | — | LAR 5.3 YPT vs TE | |

### Cuts / holds

- Solo Kyren/Corum rush overs until one clears 60%.
- WSH rush overs (LAR 3.54 YPC).
- WSH TE overs.
- Passing yards off.

### Defenders (PFR)

WSH: Robertson 52/6.9/361; Douglas 35/6.8/237; Styles LB 32/6.7/214.  
LAR: Lake 46/6.1/279; Watson CB OUT; Curl S 19/9.0/171 (Q).

### Outlier vs model

**OUTLIER_PENDING**

---

# 8. TB @ CHI — Sun Nov 8, 8:20 PM ET (SNF)  ★ PRIORITY

**Line:** CHI −6, total **47.5**. 50–51°F, light wind.  
**Script lean:** CHI moderate favorite; TB underdog. CHI blitz 41% / TB blitz 40% — Panthers-rule lean checkdowns both QBs. TB run D 3.61 → cut CHI rush overs caution. Soft CHI WR/TE YPT (8.9 / 8.2) but Jaylon Johnson **13.0 YPT** is a massive CB leak.

### Key players

| Player | Type | Stat | Low | Mid | High | Notes |
|---|---|---|---|---|---|---|
| Bucky Irving | POWER/VOLUME | rush yds | 50 | **70–85** | 110 | L3 **57%** — **fails 60%** with Gainwell 34% |
| Emeka Egbuka [Q] | — | — | HOLD | DNP Wed foot | |
| Chris Godwin Jr. | — | targets / rec yds | 5/40 | **7–8 / 65–80** | 11/110 | Egbuka out bump; vs Johnson/Stevenson leaks |
| D'Andre Swift | — | rush yds | 55 | **80–95** | 120 | ~72% clears 60%; but TB 3.61 YPC caution |
| Colston Loveland | — | targets / rec yds | 5/40 | 8–10 / 60–75 | 12/100 | 29% L3; TB TE ~6.9 YPT |
| Rome Odunze / Luther Burden | — | mid | | | |

### Targets to pursue

| Player | Prop | Side | Rung | Reason | Flags |
|---|---|---|---|---|---|
| Chris Godwin | Rec yards | OVER if Egbuka out | Mid | CHI CB leaks (Johnson 13.0, Stevenson 10.6 YPT) | Egbuka 90-min; map primary; OUTLIER_PENDING |
| D'Andre Swift | Rush | Lean UNDER or pass | Low | TB run suppression 3.61; card caution | OUTLIER_PENDING |
| Bucky Irving | Rush overs | **CUT** until ≥60% | — | 57% L3 | 60% rule |

### Cuts / holds

- Egbuka held; Irving rush overs (share); CHI rush overs caution vs TB.
- Passing yards off.
- Diaby OUT (TB) — slight CHI OL help.

### Defenders (PFR)

CHI: Jaylon Johnson **38/13.0/495**; Stevenson 30/10.6/317; Muhammad 31/8.4/259.  
TB: Parrish 48/7.5/359; Anzalone LB 44/7.4/324; McCollum 45/5.8/263.

### Outlier vs model

**OUTLIER_PENDING**

---

# 9. BUF @ MIN — Mon Nov 9, 8:15 PM ET (MNF)  ★ PRIORITY

**Line:** BUF −3.5, total **45.5**. Dome.  
**Script lean:** BUF moderate favorite. **MIN blitz 73% / pressure 28%** — extreme Panthers-rule on BUF pass volume (checkdowns / Cook). BUF run D 3.63 → cut MIN rush.  
**Injuries:** Darrisaw Q (MIN OT); BUF Brown OT Q; Gardner-Johnson released (BUF S) → TE/slot file update for MIN.

### Key players

| Player | Type | Stat | Low | Mid | High | Notes |
|---|---|---|---|---|---|---|
| James Cook | POWER/VOLUME | rush yds | 60 | **90–105** | 140 | ~75% clears 60%; MIN soft run 4.46 YPC |
| Dalton Kincaid | — | targets / rec yds | 3/25 | 5–6 / 45 | 8/70 | MIN TE 6.2 YPT stout-ish; blitz → TE seams |
| Khalil Shakir | — | targets / rec yds | 3/25 | 5 / 45–55 | 8/80 | Checkdown beneficiary under MIN pressure |
| Justin Jefferson | — | targets / rec yds | 7/60 | **9–10 / 85–100** | 13/130 | Map vs Benford / Igbinosun / Bishop |
| Aaron Jones | POWER/VOLUME | rush yds | 35 | 50–60 | 85 | L3 **57%** — fails 60% with Mason 34%; BUF 3.63 YPC |

### Targets to pursue

| Player | Prop | Side | Rung | Reason | Flags |
|---|---|---|---|---|---|
| James Cook | Rush yards | OVER | Mid–full | Soft MIN run D + clear lead back | OUTLIER_PENDING |
| Khalil Shakir / Kincaid | Rec | Lean OVER low | Low | MIN blitz forces quick game | Verify defender; OUTLIER_PENDING |
| Aaron Jones rush overs | — | **CUT** | — | <60% + BUF run D | 60% rule |
| BUF pass volume / deep WRs | — | Caution / unders lean | — | 73% blitz | Panthers rule |

### Cuts / holds

- Jones rush overs; MIN rush overs; deep BUF WR overs into blitz.
- Passing yards off.
- Confirm Kyler Murray Q listing (card) — unlikely starter; verify.

### Defenders (PFR)

MIN: Byron Murphy 40/7.8/310; Metellus 32/**8.9**/285; Rodgers 24/5.3/128 (stout).  
BUF: Benford 40/5.6/223; Bishop S 31/6.9/214; Bernard LB 33/5.9/196; Igbinosun 33/5.9/194. (Gardner-Johnson released — remove from files.)

### Outlier vs model

**OUTLIER_PENDING**

---

# 10. CIN @ ATL — Sun Nov 8, 9:30 AM ET (Madrid)

**Line:** CIN −3, total **52.5**. Bernabéu retractable TBD, 56–58°F, precip ~47%.  
**Script:** Toss-up both. Soft ATL run D (4.57); soft CIN TE (9.0 YPT).

### Key players (abbrev)

| Player | Type | Mid projection | Flags |
|---|---|---|---|
| Ja'Marr Chase | WR HIGH-VOL | ~12 tgt / 90–110 rec yds | vs Hughes 9.0 YPT |
| Tee Higgins | WR HIGH-VOL | ~8 tgt / 70–90 | |
| Chase Brown | RUSH-RECEIVE | ~10 car (**56% — fails 60%**) + ~6 tgt | rush overs CUT |
| Bijan Robinson | POWER + RUSH-RECEIVE | ~19 car / **95–110 rush** | clears 60%; CIN 4.43 YPC soft |
| Drake London | WR HIGH-VOL | ~9 tgt / 80–95 | vs Hill/Battle |
| Kyle Pitts | — | ~5–6 tgt / 45–55 | CIN TE 9.0 soft |

### Targets / cuts

- **Pursue:** Bijan rush OVER; Pitts rec yards OVER; Chase/Higgins overs with mapped defenders (Hughes / Watts).
- **Cut:** Chase Brown rush overs (56% share); Perine committee.
- Q: Battle, Dugger, Turner (CIN D) — softens ATL pass; Brian Robinson Jr. Q (Bijan share watch).
- Passing yards off. **OUTLIER_PENDING**

### Defenders (PFR)

ATL: Hughes 42/9.0/379; Watts 29/9.1/264; Deablo LB 18/**10.3**/186 (Q).  
CIN: Hill 37/8.0/297; Battle 36/7.8/279 (Q); Carter LB 36/7.3/263.

---


### Outlier vs model (partial CIN@ATL pull)

| Player | Market | Outlier | Model/card | Verdict |
|---|---|---|---|---|
| Chase Brown | Rush yds o49.5 / o52.5 | L10 **70%** on overs | L3 carry share **56%** — fails 60% rule for rush overs | **CUT rush overs** despite Outlier L10. Rec / rush+rec only if opportunity clears. |
| Chase Brown | Rush att u14.5 | L5 100% / L10 70% under | ~10 carries mid | Aligns with under on attempts. |
| Bijan Robinson | Rush yds u92.5 | L5 80% / L10 70% under | Mid high 80s–90s; B. Robinson Jr. Q share watch | Lean under 92.5 if line holds; recheck if BRJ out (Bijan volume up → over path). |
| Tee Higgins | Rec yds o77.5 | L5 80% / L10 **50%** | Soft ATL WR YPT 8.0; mid targets ~8 | L10 soft — not a primary without defender map + §7. |
| Ja'Marr Chase | Rec o6.5 | L5 40% / L10 60%, juice −148 | High-volume WR mid ~7–8 | Juice too heavy; skip or find better rung. |
| Drake London | Rec yds u78.5 | L5 60% / L10 70% under | Mid ~70–80 | Soft lean under; CIN CB Q list (Battle/Turner) is the flip risk. |
| Kyle Pitts | Rec yds u42.5 | L5 60% / L10 70% under | Mid ~40; CIN TE YPT **9.0** soft | **DISAGREE slightly** — soft TE matchup argues against hard under; low priority either side. |

Passing yards (Burrow/Penix) appear in CSV — **off slips**.


# 11. DEN @ CAR — Sun Nov 8, 1:00 PM ET

**Line:** DEN −2.5, total **44.5**. Dry, 63–64°F.  
**Script:** Toss-up. CAR OL multiple Q + DEN sack+hit 22% → Panthers-rule on CAR pass. Soft CAR run D 4.62.

### Key / targets (short)

- Chuba Hubbard (~83% carries) rush OVER candidate vs DEN 4.39 YPC — clears 60%.
- Tetairoa McMillan / Jalen Coker — volume WRs; map vs McMillian/Moss/Surtain (Surtain stout 5.9 YPT — avoid his side).
- DEN RB committee (Dobbins 43% / Coleman 29%) — **rush overs CUT** (under 60%).
- Sutton / Waddle mid; Engram modest.
- Passing yards off. **OUTLIER_PENDING**

### Defenders (PFR)

CAR: Will Lee 47/7.0/327; Evans 31/**9.3**/287.  
DEN: Brandon Jones S 26/**10.9**/283 (Q); Singleton 42/6.4/269; McMillian 38/6.9/263.

---

# 12. CLE @ NO — Sun Nov 8, 1:00 PM ET

**Line:** NO −3, total **42.5**. Dome.  
**Script:** Toss-up. **Watson concussion → Shedeur Sanders likely** — CLE pass-catcher **backup/new-QB flag**. Soft NO run D 4.80; soft CLE run D 4.67.

### Key / targets (short)

- **Hold all CLE pass-catcher overs** until QB confirmed; Judkins receiving held.
- Judkins rush: L3 **44%** — fails 60%; committee. Lean NO run game instead.
- Kendre Miller (~56%) — fails 60% if Kamara active; if Kamara out, Miller lead — recheck.
- Kamara [Q] held.
- Chris Olave / Devaughn Vele overs with Harden (7.7 YPT) / Hickman (9.5) mapped.
- Passing yards off. **OUTLIER_PENDING**

### Defenders (PFR)

NO: Sanker 37/7.2/267; Riley 32/7.7/245; Reid 29/8.0/231 (Q); McKinstry 31/6.7/209.  
CLE: Harden 50/7.7/385 (Q); Schwesinger LB 27/**10.0**/270 (Q); Campbell 27/9.5/257; Hickman 22/9.5/208.

---

# 13. HOU @ LAC — Sun Nov 8, 4:05 PM ET

**Line:** HOU −4.5, total **40.5**. Indoor.  
**Script:** HOU moderate favorite. **David Montgomery OUT** → Woody Marks (~67%) lead. Soft LAC TE 8.7; soft-ish LAC run 4.35. HOU run D 3.82 → cut LAC rush overs. LAC backfield split Hampton 42% / Vidal 32% — both fail 60%.

### Key / targets (short)

- Woody Marks rush OVER candidate (clears 60%, Monty out).
- Nico Collins / Schultz mid; Schultz TE vs LAC 8.7 soft.
- LAC rush overs CUT (split + HOU run D).
- Njoku designated to return — watch Gadsden share.
- OL both sides Q (Smith / Awosika) + high pressure — pass volume caution.
- Passing yards off. **OUTLIER_PENDING**

### Defenders (PFR)

LAC: Hart 24/**9.2**/221; Still 25/7.5/187; Henley 21/8.4/176 (Q).  
HOU: Lassiter 46/8.5/389; Blankenship 33/9.1/299 (Q); Bullock 32/9.0/289; Stingley 38/7.4/282.

---

# 14. LV @ SF — Sun Nov 8, 4:25 PM ET

**Line:** SF −10, total **52.5**. 70–73°F dry.  
**Script:** SF **BLOWOUT FAVORITE**. Soft LV WR YPT 9.3 + run D **5.20**. SF McCaffrey/Evans/Deebo all DNP Wed — **held**. SF run suppression 3.55 → cut LV rush.

### Key / targets (short)

- Brock Bowers (TE-AS-REC) volume mid but SF hard on TE (5.5 YPT) — caution overs.
- Ashton Jeanty rush+rec; LV rush overs CUT vs SF.
- SF rush/receive: wait CMC status; if out, Kaelon Black / committee — 60% check.
- Kittle mid if SF passers healthy.
- Soft LV defense → SF skill overs **if** starters active Friday.
- Passing yards off. **OUTLIER_PENDING**

### Defenders (PFR)

SF: Stout 30/7.7/231 (Q); Green 31/6.8/210; Warner 30/6.9/207; Lenoir 32/6.2/198.  
LV: Stokes 44/7.3/319; Stukes S 25/**9.8**/245; Masses 29/7.0/202; Chinn 22/9.0/199.

---

# 15. GB @ NE — Sun Nov 8, 4:25 PM ET

**Line:** NE −3.5, total **45.5**. 44–46°F, gusts ~18.  
**Script:** NE moderate favorite. Both OL battered → Panthers-rule both ways. Parsons OUT (PUP return individual only).

### Key / targets (short)

- Josh Jacobs L3 **46%** — rush overs CUT (Lloyd 25%).
- Matthew Golden volume WR (~13 tgt proj) vs Marcus Jones 8.3 YPT / Woods 8.8.
- Rhamondre Stevenson (~51%) — fails 60% with Kiner 29%; **if Henderson out**, Stevenson lead → OVER candidate pending 60% clear.
- A.J. Brown / Hunter Henry / Henderson — **held** (DNP Wed).
- Douglas / Raridon bump if Brown/Henry sit (depth rule for Raridon).
- Passing yards off. **OUTLIER_PENDING**

### Defenders (PFR)

NE: Marcus Jones 38/**8.3**/314; Woodson S 25/**9.2**/230; Woods 26/**8.8**/228; Gonzalez 33/6.1/200 (stout).  
GB: Nixon 58/5.8/335 (Q); Cisse 38/**8.2**/313; Bullard 38/4.5/170.

---

# Summary tables

## Top TNF targets (actionable tonight) — after Outlier merge

1. **Brenton Strange rec yards o35.5** (or 40+ alt) — §7 4/4 + Outlier L5 80% / L10 60% **confirm**.
2. **Brenton Strange 4+ receptions (o3.5)** — still #1 receiving leg; Outlier L10 only 40% → last-2 downgrade stays.
3. **Derrick Henry rush U69.5** — model still under; **Outlier L10 70% on o67.5 fights it** → thinner, flag not cut; skip if juice worse than −115.
4. **BAL TT U14.5** — secondary / correlated with Henry U.
5. **JAX 1Q −2.5 / 1Q ML** — singles only, last-2 downgrade.
6. **Washington** — main o63.5 still CUT (§7 + model) despite Outlier L10 70%.
7. **Flowers / Andrews overs** — FADE (Outlier hit rates are Lamar-era; backup-QB flag).
8. **Rodriguez rush** — only if Tuten ruled OUT at ~6:50 PM ET inactives.

## Biggest open data gaps

1. **Outlier coverage thin** — TNF + partial CIN@ATL only (83 rows); rest of Sunday + MNF missing.
2. **`key_players.md` refreshed** for Week 10 (2026-11-05).
3. **PFR live pull 403** — using Nov 4 cache (usable, not same-morning); see `defense/README.md`.
4. **No FanDuel live prop pull this morning** (Odds API budget) — Sunday lines = ESPN DK consensus only; TNF r6 odds are ~19h stale by kick.
5. **NGS route/gap not refreshed**; participation/man-zone from free sources still limited.
6. **Gate PASS stamps:** none this card run — props need full gate before any slip to Rico.
7. **CLE QB / SEA Lock throw volume / many Fri designations** still open.

## Q-player watchlist (compact)

**TNF 90-min / inactives:** Tuten, Walker, Wiggins (conflict), Campbell (BAL DT).  
**Fri + 90-min Sunday:** Watson, Lock, Pickens, Ferguson, ARSB, Rice, Kelce, G. Wilson, Hall, A.J. Brown, Henderson, H. Henry, Smith, Wicks, Saquon, Egbuka, Wright, Skattebo, Knight, M. Wilson, CMC, Evans, Deebo, B. Robinson Jr., Darrisaw, plus full per-game ESPN Q lists in cards.

---

*Finalized 2026-11-05 10:18 AM ET. TNF Outlier merged; CIN@ATL partial; rest of slate Outlier-missing. No bets placed. No external messages.*
