# Week 8 defense dissection (2026-11-01)
Scope: the 8 final 1 PM games (ARI@DAL, ATL@TB, BAL@BUF, CLE@PIT, IND@JAX, LV@NYJ, MIN@DET, TEN@CIN), both defenses. 4 PM/SNF games (KC@DEN, LAC@LAR, NE@MIA, PHI@WSH) have STUB blocks only.
Tools: playlogs/tools/defense_dissect_wk8.py and write_dissect_wk8.py. Raw output: playlogs/2026_wk8/_dissect_*.json.

## Explosives at the new threshold (rush 15+, reception 20+): 73 total
| Defense | Rush 15+ | Rec 20+ | Total |
|---|---|---|---|
| ARI | 0 | 2 | 2 |
| ATL | 4 | 0 | 4 |
| BAL | 1 | 4 | 5 |
| BUF | 0 | 1 | 1 |
| CIN | 2 | 5 | 7 |
| CLE | 4 | 3 | 7 |
| DAL | 3 | 4 | 7 |
| DET | 1 | 3 | 4 |
| IND | 2 | 4 | 6 |
| JAX | 2 | 0 | 2 |
| LV | 4 | 5 | 9 |
| MIN | 3 | 1 | 4 |
| NYJ | 1 | 3 | 4 |
| PIT | 0 | 4 | 4 |
| TB | 1 | 1 | 2 |
| TEN | 0 | 5 | 5 |

Confidence (73 plays): receptions 45 → inferred 22, unknown 23, confirmed 0. Rushes 28 → tackler-of-record 21, confirmed (penalty-named) 1, unknown 6.
"Confirmed" = a defender named in ESPN play text for a penalty, INT or PBU (single source). "Inferred" = the pregame primary matchup for that WR (ESPN cheat sheet plus coverage.json). Two sources agree on a pregame matchup, but nothing confirms coverage on the play. TE and RB catches stay unknown because there's no free alignment or matchup source.

## Methods
- Defense = the non-possession team on the ESPN drive.
- Shell: Week 8 FTN and participation data aren't published (nflverse has only CAR@GB). Every shell shown is the defense's pregame season tendency from Sharp (man/zone/MOFC/MOFO) and is labeled as a tendency. It's stale under the 48h coverage rule.
- Alignment for WRs is the pregame target-side proxy plus the ESPN season alignment split, labeled. TE is "not charted"; RB is the backfield default.
- QB-adjusted position allowances use the residual method in runs/2026-11-01_shared_src/features.py: YPT vs this defense minus the passer's own Week 1–7 YPT to that group. If he has fewer than 8 targets to the group, the league mean is used.
- WR outside vs middle uses the ESPN pass_location proxy, the same proxy as the season profile.
- Defender lines: per-defender targets are not public for free (PFF and FTN premium only, not authorized). Catches and yards are charged to the first tackler after the catch, as in the CAR_secondary.md method. PBU = named on an incompletion. These are proxies, not coverage charting.

## Top defenders charged (tackler-after-catch proxy)
- J.Battle (CIN S): 8 rec, 104 yds, 2 explosives, 2 PBU
- J.Brisker (CLE S): 6 rec, 103 yds, 2 explosives
- T.Stukes (NYJ S): 102 yds, 2 explosives; D.Belton (NYJ S): 96 yds, 2 explosives
- A.Hill (CIN LB): 94 yds
- C.Schwesinger (CLE LB): 89 yds, 2 explosives
- M.Humphrey (BAL CB): 79 yds, 2 explosives

## Limited their man or made plays (single source)
- A.Hooker (TEN): 3 INT
- D.Reed (DET): 2 PBU, 1 INT, though penalized earlier
- A.Anzalone (TB): 2 INT
- D.Burke (ARI): 2 PBU, though charged for Lamb's 27
- E.Stokes (NYJ), A.Gardner (IND), G.Rousseau and R.Smith (BUF): 2 PBU each

## Top 5 exploitable for Week 9 (RESEARCH LEADS ONLY; not picks)
1. **LV outside CB (Darien Porter, inferred) → LV vs SF.**
   - A.Mitchell went 20/22/47 against his pregame side.
   - LV's WR_out QB-adjusted residual was +3.16 on 19 targets for 225 yards.
   - Basis: single game, inferred.
2. **CLE vs TEs (Brisker, Schwesinger) → CLE @ NO.**
   - TE residual +12.08: 129 yards on 7 targets, with Washington 24/58 and Freiermuth 28.
   - Season-to-date context is in week8/defense/CLE_at_PIT.md.
3. **IND vs TE and RB receiving → DAL @ IND.**
   - TE residual +15.6 (Strange 46, Boerkircher 31).
   - RB receiving residual +8.7 (Tuten 30/25), plus Tuten's 39 run and Rodriguez's 28.
   - Note: the JAX offense did this, and IND's season numbers were better.
4. **CIN safeties and LB (Battle, A.Hill) and outside CBs → CIN vs ATL.**
   - 5 explosive catches allowed: TE residual +4.68, WR_out +1.69.
   - Caveat: ATL scored 0 in Week 8 and Penix threw 4 INTs.
5. **DAL run fits and middle of the field → DAL @ IND (Taylor).**
   - Allowed 165 rush yards on 18 RB carries, including Allgeier's 63 and 52.
   - WR_mid residual +6.72. Mi.Wilson had 3 catches of 20+ against the inferred CB J.Porter Jr.
- Honorable mention: BAL vs TE (Kincaid 40/23), relevant for JAX @ BAL. NYJ allowed 145 TE yards on 16 targets, but the residual is only +0.42; relevant for NYJ @ KC.

## Data gaps
- No Week 8 FTN, participation, or NGS coverage data, so no shells or coverage defenders on any play.
- Per-defender targets aren't public.
- Every play-text item is single source (ESPN).
- MIN A.Jones (7 plays): position isn't resolved in nflverse; he's treated as unknown in the position split.
- test_explosives.py FAILs on a row that was already in explosives_allowed.md before this work: ARI@DAL OT, "Q5 5:13", no drive match. It's an OT-label issue and wasn't caused by this append.
- I didn't rerun build_edges_wk8.py, because rerunning would overwrite the manual EDGE and returns sections. The 8-game v2 table was appended instead.

## Files updated (backups: *.pre_wk8dissect.bak)
- defenders/ARI_secondary.md
- defenders/ATL_secondary.md
- defenders/BAL_secondary.md
- defenders/BUF_secondary.md
- defenders/CIN_secondary.md
- defenders/CLE_secondary.md
- defenders/DAL_secondary.md
- defenders/DET_secondary.md
- defenders/IND_secondary.md
- defenders/JAX_secondary.md
- defenders/LV_secondary.md
- defenders/MIN_secondary.md
- defenders/NYJ_secondary.md
- defenders/PIT_secondary.md
- defenders/TB_secondary.md
- defenders/TEN_secondary.md
- week8/defense/ARI_at_DAL.md
- week8/defense/ATL_at_TB.md
- week8/defense/BAL_at_BUF.md
- week8/defense/CLE_at_PIT.md
- week8/defense/IND_at_JAX.md
- week8/defense/KC_at_DEN.md
- week8/defense/LAC_at_LAR.md
- week8/defense/LV_at_NYJ.md
- week8/defense/MIN_at_DET.md
- week8/defense/NE_at_MIA.md
- week8/defense/PHI_at_WSH.md
- week8/defense/TEN_at_CIN.md
- playlogs/explosives_allowed.md (appended v2 table)
- defender_ledger.csv (+319 dated rows)
