# LV @ NYJ — Research pack, Sun Nov 1 2026, 1:00 PM ET (research only, no picks)
Built 2026-10-31 ~11:45 PM ET. Sources:
- [PBP] nflverse play_by_play_2026.parquet (phase_walk/src, file 2026-10-31 19:17 ET, weeks 1–7, REG). Script: /tmp/lvnyj.py, output /tmp/lvnyj_out.txt. Rank 1 = most allowed. Positions from nflverse players.parquet.
- [PFR] /workspace/nfl-sim/mnf12/pfr_def_adv_2026.html — cache file dated 2026-10-29 06:02 ET; NYJ defenders show G=5 (≈ thru wk5–6). Team totals summed from per-defender rows.
- [DEF] week8/defense/LV_at_NYJ.md (Sharp Football scheme page Oct 27, FTN, ESPN win rates, NGS) — built Oct 29.
- [ESPN] depth chart (core API teams/13/depthcharts) + league injuries API, pulled 2026-10-31 ~11:40 PM ET.
- [FD] betguru_2026-11-01_raw/fd_alts_20261031T2018.csv (pulled 2026-10-31 20:18 ET). Prices stale vs kickoff.

## QB verification
- ESPN depth chart QB order: Kirk Cousins, Fernando Mendoza, Aidan O'Connell. ESPN injury list: Cousins "Active" (no designation). Cousins threw 272 of 281 LV passes, all 7 games [PBP]. => Cousins confirmed starter (Rico correct).

## 1) NYJ allowed per game [PBP]
- Season (7 g): pass/rec yds 202.9/g (rank 28 → 5th fewest); rush yds 127.7/g (rank 9).
- Last 3 (wk5 CLE 155 rec/96 rush; wk6 NE 235/148; wk7 MIA 208/156): rec 199.3/g (rank 25), rush 133.3/g (rank 10).

## 2) Blitz / pressure
- Sharp blitz 40.0% (rank 4 most) [DEF]; FTN blitz 38.4% (n=250) [DEF].
- PFR (cache Oct 29): 65 blitzes, 34 pressures, 9 hurries, 17 sacks → blitz/dropback ≈28.0% (rank 8), pressure ≈14.7% (rank 18). Caveat: PFR counts thru ~wk5–6 divided by wk1–7 PBP dropbacks → understated; ranks approximate.
- PBP proxies: sack% 8.2 (rank 4), hit+sack% 22.8 (rank 13), 232 dropbacks. Opp-Sharp pressure proxy 28.8% (rank 16) [DEF]. ESPN pass-rush win rate 48.0 [DEF].
- True pressure rate (charted): UNAVAILABLE beyond above (no pressure column in PBP).

## 3) Cousins vs pressure / blitz
- PBP proxy, hit or sacked (43 db): 33 att, 27.3% cmp, 4.64 YPA, 10 sacks, 1 INT, EPA/db −0.615.
- Clean (no hit/sack, 229 db): 66.4% cmp, 7.54 YPA, 0 sacks, 4 INT, EPA/db +0.260.
- FTN: LV EPA/db vs blitz −0.01 vs no blitz +0.16; blitzed 29% [DEF]. NGS TTT 2.89s, aggressiveness 20.6%, CPOE +2.7, IAY 8.5 [DEF]. LV sack% allowed 3.5, ESPN pass-block WR 64.0 [DEF].
- Cousins comp%/YPA split by blitz specifically: UNAVAILABLE (PFR advanced passing not cached).

## 4) RBs vs NYJ + Jeanty [PBP]
- NYJ allows RBs 4.9 tgt / 3.4 rec / 21.6 yds per g (rec rank 26, yds rank 26 → stingy). Sharp RB YPT 4.4 (rank 25) [DEF]. RB rush 106.6/g, 4.08 YPC (rank 20) [DEF].
- Jeanty (7 g): 6.4 tgt, 4.9 rec, 44.6 rec yds/g, 16.6% tgt share; L3 6-3-50, 6-4-36, 8-8-61. Rushing 15.1 car, 46.9 yds/g, 3.09 YPC.

## 5) WR / TE vs NYJ [PBP]
- WR: 17.4 tgt, 10.7 rec, 133.3 yds/g (rec rank 17, yds rank 24). Sharp WR YPT 7.6 (rank 20).
- TE: 6.6 tgt, 4.7 rec, 48.0 yds/g (rec rank 22, yds rank 18). Sharp TE YPT 7.3 (rank 13).
- PFR coverage (cache): Sherwood LB 18 tgt-15-163, 9.1 YPT, 122.9 rtg; D. Davis LB 18-12-133; A. Thomas CB 24-17-139; B. Stephens CB 22-10-131; Brownlee 14-8-56; Belton S 13-7-78; Cisco S 12-6-75.

## 6) Explosives allowed [PBP]
- Rush 10+: 3.14/g (rank 12). Pass 20+: 2.43/g (rank 24). Total 5.57/g (rank 16).

## 7) LV target tree [PBP] (tgt/rec/yds per g, share, L3 wk5;wk6;wk7 tgt-rec-yds)
- Bowers (5 g): 10.4 / 6.8 / 91.0, 19.2% | 10-8-110; 9-4-70; 9-6-73
- Tucker (7 g): 6.7 / 4.1 / 67.7, 17.3% | 5-4-41; 7-5-97; 12-5-103
- Jeanty (7 g): 6.4 / 4.9 / 44.6, 16.6% | 6-3-50; 6-4-36; 8-8-61
- Mayer (7 g): 5.3 / 4.4 / 42.6, 13.7% | 1-1-2; 9-7-95; 3-3-32
- Nailor 4.2/1.6/15.0; C. White 2.9/1.1/16.0.
- Bowers leads targets, receptions and yards per game.

## 8) Cousins checkdowns [PBP]
- Air ≤0 (46 of 262 tgts): Jeanty 16 tgt-14 rec-96 yds; Bowers 6-3-5; Mayer 5-5-33; Tucker 4-3-4; Washington 3-2-4.
- Air 1–4 (51): Jeanty 14-10-90; Mayer 12-10-75; White 6-2-8; Tucker 5-2-46; Bowers 5-5-39.
- Throws with QB hit (33): Bowers 6-1-11; Jeanty 5-1-1; Tucker 5-2-63; Nailor 4-1-16.
- Main checkdown = Jeanty, then Mayer.

## 9) FanDuel (20:18 ET Oct 31) [FD]
- Bowers: rec yds 68.5 (−113/−113); alt 50+ −290, 60+ −178, 70+ −110, 80+ +138, 90+ +198, 100+ +280. Rec 5.5 (o−154/u+116); alt 5+ −310, 6+ −158, 7+ +122, 8+ +210.
- Tucker: rec yds 48.5 (−113/−113); alt 40+ −182, 50+ −108, 60+ +144, 70+ +205. Rec 3.5 (o−120/u−110); alt 3+ −300, 4+ −120, 5+ +182.
- Jeanty: rec yds 27.5 (−113); alt 20+ −220, 25+ −144, 30+ +100, 40+ +188. Rec 3.5 (o−125/u−106); alt 3+ −290, 4+ −128, 5+ +162. Rush 49.5 (−113); alt 40+ −215, 50+ −114, 60+ +148, 70+ +225. Rush+rec 81.5 (o−115/u−111); no alt ladder offered.
- Cousins pass yds 232.5 (−113); alt 225+ −138, 250+ +124.

## Injuries [ESPN, pulled ~11:40 PM ET Oct 31]
- NYJ pass rush/DL: Joseph Ossai DE OUT (ankle); David Bailey LB/edge DOUBTFUL (groin); T'Vondre Sweat DT IR (knee). Will McDonald active.
- NYJ secondary: none listed with designation (Fitzpatrick, Belton, Brownlee listed Active). NYJ OL: Max Mitchell OUT, Parham Q.
- LV OL: Jackson Powers-Johnson G QUESTIONABLE (back); DJ Glaze OT now Active. Bowers listed Active (was Q calf earlier in week). Patrick Johnson DE IR. Carter Runyon TE IR.
- Spread (ESPN, Oct 29): NYJ −1.5, O/U 45.5 [DEF].

## Coverage scheme
- Sharp: Man 23.8% / Zone 66.6%, MOF-closed 45.2% / MOF-open 50.0%; light box 43.4%, heavy 24.1% [DEF].
- StatRankings Oct 31 man-coverage rate: NYJ value not re-pulled for this pack → UNAVAILABLE here.

## Follow-up (Rico): Has Cousins faced blitz/pressure-heavy D? (added 2026-10-31 ~11:55 PM ET)
Sources: Sharp blitz rate = defense/raw/nfl-defensive-tendencies.html (retrieved 2026-10-29 05:08 ET); FTN blitz (n_blitzers>0) = defense/raw/ftn_charting_2026.parquet wk1–7 joined to [PBP]; hit-sack% = dropbacks with qb_hit OR sack [PBP]. Script /tmp/cous.py. Rank 1 = most.
Correction: Q2 above listed NYJ hit+sack 22.8% (rank 13) — that double-counted sacks that are also hits; union rate is 15.5% (rank 17). FTN blitz NYJ 38.4% (rank 7).

| Wk | Opp | Sharp blitz (rk) | FTN blitz (rk) | Hit-sack% (rk) | C/A | Yds | YPA | Sk | INT | EPA/db | Blitzed/db | Hit-or-sacked | Final | % LV att while trailing | LV att |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | MIA | 22.1 (27) | 25.8 (25) | 14.8 (20) | 21/30 | 160 | 5.33 | 0 | 2 | +0.013 | 10/30 | 2 | LV 27-13 | 0% | 30 |
| 2 | LAC | 21.7 (30) | 26.4 (23) | 18.7 (6) | 19/29 | 253 | 8.72 | 2 | 1 | +0.193 | 8/31 | 9 | LV 26-14 | 19% | 31 |
| 3 | NO | 31.9 (10) | 33.7 (11) | 13.5 (27) | 22/35 | 248 | 7.09 | 3 | 0 | +0.236 | 11/38 | 6 | LV 35-27 | 34% | 38 |
| 4 | KC | 26.8 (16) | 27.6 (19) | 14.5 (21) | 31/53 | 365 | 6.89 | 0 | 1 | +0.184 | 11/53 | 10 | LV 27-30 | 43% | 53 |
| 5 | NE | 40.2 (3) | 39.5 (6) | 17.3 (11) | 19/28 | 243 | 8.68 | 3 | 0 | +0.124 | 8/31 | 7 | LV 17-45 | 95% | 39 |
| 6 | BUF | 27.5 (14) | 34.9 (10) | 16.9 (13) | 23/41 | 313 | 7.63 | 0 | 1 | +0.280 | 17/41 | 6 | LV 30-33 | 88% | 41 |
| 7 | LA | 26.6 (17) | 30.3 (17) | 11.6 (29) | 26/46 | 295 | 6.41 | 2 | 0 | -0.153 | 13/48 | 3 | LV 21-35 | 90% | 49 |

(a) Yes. Top-10 blitz faced: NE (Sharp #3, FTN #6), NO (Sharp #10), BUF (FTN #10). Top-10 pressure: LAC (hit-sack #6). Avg yds in NE/NO/BUF games 268 (243/248/313) vs 268 in other four (160/253/365/295) — no drop, but NE and BUF were trailing scripts (95%/88% of attempts while behind). Season split [PBP+FTN]: blitzed 78 db: 53.8% cmp, 6.53 YPA, 0 sk, 2 INT, EPA +0.047; not blitzed 194 db: 64.7%, 7.43 YPA, 10 sk, 3 INT, EPA +0.152. No blitz team ranks as high as NYJ's Sharp #4 except NE.
(b) FALSE: Wk1 vs MIA 160 yds (21/30) per [PBP]. 200+ in 6 of 7.
(c) LV blitzed 28.1% of dropbacks; at NYJ FTN 38.4% on ~40 db → ~15 blitzed (vs ~11 avg). Hit-or-sacked: LV allowed 15.7%/db, NYJ 15.5% → ~6 hits/sacks expected (no change). Sacks: Cousins 10/272 db (3.7%) vs NYJ sack% 8.2 → ~2 sacks (avg ~1.4). Blitz YPA penalty ~0.9 × ~4 extra blitzed att ≈ −4 yds. Volume: NYJ −1.5, total 45.5 (ESPN Oct 29) → close script; in non-trailing games (wk1–3) LV threw 30–38 att and Cousins went 160–253. Range ~200–260 (center ~230 ≈ FD 232.5); basis 34–38 att × 6.5–7.0 YPA. Blitz effect small; volume/script is the driver. NYJ allows 202.9 completion yds/g (5th fewest).
(d) Career vs heavy-blitz teams 2024–25: UNAVAILABLE (not run; needs nflverse 2024–25 pbp + FTN pull).

## Follow-up 2 (Rico): Is 202.9 rec yds/g allowed real? (added 2026-10-31 ~11:58 PM ET)
Sources: [PBP] nflverse 2026 play-by-play, script /tmp/nyj.py. [ESPN] summary boxscore netPassingYards, event IDs 401872924/936/954/972/983/401873001/015, pulled ~11:57 PM ET. ESPN net matched [PBP] net exactly in all 7 games.
202.9 = GROSS receiving yds (completions only, sacks excluded). Net passing (sack yds subtracted) = 187.7/g. Both rank 28 of 32 (5th fewest).
Opp off rank = opponent's season gross passing yds/g [PBP].

| Wk | Opp | QB | Rec yds (gross) | Net pass (ESPN) | Att | Sk | Opp off rk (yds/g) | Final | % opp att trailing |
|---|---|---|---|---|---|---|---|---|---|
| 1 | TEN | Cam Ward | 140 | 127 | 32 | 3 | 32 (168.4) | TEN 10-23 NYJ | 100% |
| 2 | GB | Jordan Love | 145 | 136 | 29 | 3 | 4 (280.8) | NYJ 17-20 GB | 28% |
| 3 | DET | Jared Goff | 269 | 250 | 32 | 2 | 1 (298.0) | DET 31-24 NYJ | 26% |
| 4 | CHI | Tyson Bagent | 268 | 260 | 34 | 1 | 10 (254.9) | CHI 23-12 NYJ | 0% |
| 5 | CLE | Deshaun Watson | 155 | 102 | 33 | 8 | 23 (211.7) | NYJ 17-12 CLE | 90% |
| 6 | NE | Drake Maye | 235 | 235 | 32 | 0 | 9 (261.4) | NE 26-19 NYJ | 9% |
| 7 | MIA | Malik Willis | 208 | 204 | 21 | 2 | 30 (176.2) | NYJ 25-28 MIA | 0% |

Top-half passing offenses (GB #4, DET #1, CHI #10, NE #9): 229.3 rec yds/g allowed, vs those offenses' own 273.8 avg (about 84%). Bottom half (TEN #32, CLE #23, MIA #30): 167.7.
LV passing offense: #5 (276.9 gross / 269.3 net per game) [PBP].
Fair LV expectation: 276.9 × ~0.84 ≈ 232 gross receiving yds; range ~210–250.
Verdict: Rico is mostly right. The 202.9 is real, but bottom-half offenses drag it down. Against good passing teams NYJ allows about 229 (DET 269, CHI 268, NE 235). Exception: GB (#4) got only 145. Note CHI's QB was Tyson Bagent.

## Follow-up 3 (Rico): Cousins last 3 + blitz split; NYJ YPA/aDOT allowed (added 2026-10-31 ~midnight ET)
Sources: nflverse 2026 PBP (attempts exclude sacks; yards = completion yards_gained; aDOT = mean air_yards on all attempts) + FTN charting n_blitzers>0 (defense/raw/ftn_charting_2026.parquet). Script /tmp/c3.py.

- wk5 NE: 19/28, 243 yds, YPA 8.68, aDOT 6.1; blitzed 8 att 59 yds YPA 7.38 | not 20 att 184 yds YPA 9.20; trailing on 93% att
- wk6 BUF: 23/41, 313 yds, YPA 7.63, aDOT 8.6; blitzed 17 att 99 yds YPA 5.82 | not 24 att 214 yds YPA 8.92; trailing on 88% att
- wk7 LA: 26/46, 295 yds, YPA 6.41, aDOT 7.5; blitzed 13 att 48 yds YPA 3.69 | not 33 att 247 yds YPA 7.48; trailing on 89% att
- L3 total: 68/115, 851 yds, YPA 7.40, aDOT 7.6; per game 283.7 yds; blitzed 38 att 206 yds YPA 5.42 | not 77 att 645 yds YPA 8.38
- Season (7 g): 161/262, 1877 yds, YPA 7.16, aDOT 8.1; per game 268.1; blitzed 78 att 509 yds YPA 6.53 | not 184 att 1368 yds YPA 7.43
- NYJ wk1 vs TEN: YPA allowed 4.38, aDOT 5.9, air yds/att (completed) 1.9, YAC/comp 4.1
- NYJ wk2 vs GB: YPA allowed 5.00, aDOT 7.4, air yds/att (completed) 1.8, YAC/comp 5.9
- NYJ wk3 vs DET: YPA allowed 8.41, aDOT 6.0, air yds/att (completed) 4.5, YAC/comp 5.0
- NYJ wk4 vs CHI: YPA allowed 7.88, aDOT 6.3, air yds/att (completed) 3.9, YAC/comp 5.4
- NYJ wk5 vs CLE: YPA allowed 4.70, aDOT 9.0, air yds/att (completed) 3.5, YAC/comp 2.6
- NYJ wk6 vs NE: YPA allowed 7.34, aDOT 8.2, air yds/att (completed) 4.9, YAC/comp 4.3
- NYJ wk7 vs MIA: YPA allowed 9.90, aDOT 5.0, air yds/att (completed) 3.4, YAC/comp 9.8
- NYJ season: YPA allowed 6.67, aDOT 6.9- Verdict on Rico's 'GB threw short' point: NOT supported. GB's aDOT vs NYJ was 7.4, above NYJ's season-average aDOT allowed of 6.9. GB's low total came from low YPA (5.00), not short throws.
- All three of Cousins's last 3 games were trailing scripts (88–93% of attempts). His L3 per-game yards (283.7) are inflated by volume (38 att/g vs 33 att/g in wk1–4).

## Follow-up 4 (Rico t256u): Coverage, alignment, defenders, physicals, Jeanty checkdowns (added 2026-11-01 ~12:15 AM ET)
Sources: Sharp coverage page (cached Oct 29 5:08 AM ET); nflverse pbp wk1-7 + FTN charting (n_blitzers); nflverse NGS receiving 2026; ESPN Week 8 WR/CB cheat sheet; ESPN NYJ depth chart (pulled ~12:10 AM ET Nov 1); PFR adv defense (cache Oct 29, only ~5 G, fresh pull 403).
**1. Coverage:** Sharp: zone 66.6 / man 23.8; MOF-open 50.0 / closed 45.2. Cover 1/2/3/4/6 breakdown: UNCONFIRMED (FTN public charting has no coverage-type field; no free source found). NYJ blitz 38% of dropbacks (FTN). Not blitzing: 5.81 YPA, 58% cmp, aDOT 7.4. Blitzing: 8.06 YPA, 69% cmp, aDOT 6.2; vs blitz 20+ air yd throws went 5/6 for 134. Coverage-shell-when-blitzing: UNCONFIRMED.
NYJ allowed by depth (7 G): behind LOS 48 tgt-174 yds; 1-9 yds 104-657; 10-19 43 tgt, 18 cmp, 315; 20+ 18 tgt, 9 cmp, 274. Per catch: left 10.3, middle 11.9, right 10.5.
**2. Alignment/routes:** Bowers: 57% slot, 21% LWR, 21% RWR (ESPN); 28% targets/route. NGS 2026: aDOT 10.5, cushion 5.7, sep 2.3 (lower than 2024's 3.5). PBP: 10.4 tgt/g (5 G), 34-455; 10-19 yds is his zone (21 tgt, 14-249); left 18/mid 17/right 16 tgt. Vs blitz: 18 tgt 9-137; no blitz 34 tgt 25-318.
Tucker: 35% LWR, 23% slot, 41% RWR; 19% targets/route; NGS aDOT 13.0, sep 2.5. 6.7 tgt/g; 20+ yds 9 tgt 5-170; vs blitz only 14 tgt 7-70 (no blitz 33 tgt 22-404). Left side 20 tgt 197 yds.
Jeanty: 6.4 tgt/g, 34-312, aDOT 2.2; 41 of 45 targets are behind LOS or 1-9 yds; 5 drops (FTN). Only 5 targets vs blitz.
**3. Jets defenders (ESPN depth):** LCB Azareye'h Thomas (6-1/197) 24-17-139, 2 TD, 113.0 rating; RCB Brandon Stephens (6-0/206) 22-10-131, 64.8; nickel Jarvis Brownlee Jr. (ESPN starter) 14-8-56, 2 TD, 106.0; D'Angelo Ponds (5-9/170, the ESPN sheet's match for Bowers) has 0 PFR targets. LB Jamien Sherwood 18-15-163, 1 TD, 122.9 = most yards allowed. Demario Davis 18-12-133, 88.4. S Fitzpatrick 6-5-108 (18.0/tgt); Belton 13-7-78; Cisco 12-6-75. Sauce Gardner is not on NYJ roster/depth chart. No DB injury designations (see Injuries). Likely: Tucker is at RWR 41%, so he sees LCB Thomas most; at LWR he sees Stephens. Bowers in the slot sees the nickel (Brownlee/Ponds) plus Sherwood/Davis in zone.
**4. Physicals:** Bowers 6-3/243 vs Ponds 5-9/170, Brownlee (size unconfirmed), Sherwood (unconfirmed). Tucker 5-8/182 vs Thomas 6-1/197 and Stephens 6-0/206. Combine 40s: Tucker 4.40 (2023), Bowers about 4.53 (pro day). Neither figure was re-verified this session, so treat both as UNCONFIRMED. Defender 40s UNCONFIRMED. Catch rate: Bowers 65%, 1 drop; Tucker 62%, 2 drops; Jeanty 76%, 5 drops.
**5. RB receiving allowed by NYJ:** 5.4 tgt/g, 31.9 yds/g; DET alone 13-12-125. Without DET about 16 yds/g. The other QBs faced (TEN, GB, CLE, etc.) were weak or conservative. Adjusted read: below average except vs a heavy RB-target offense.

## Follow-up 5 (Rico t257u): Bowers 25+ rec yds in EACH half (added 2026-11-01 ~12:20 AM ET), for Ghost6 to vet, not a pick
**FD (sbapi pull 12:10 AM ET Nov 1):** "Bowers 25+ Receiving Yds in Each Half" +125 (implied 44.4%; one-sided special, est. no-vig ~40% at ~10% hold, UNCONFIRMED hold). FD has no standalone 1H or 2H receiving-yards markets for him. Full game: O/U 68.5 at -113/-113; alts 50+ -290, 60+ -178, 70+ -110, 80+ +138. Related: 50+ each half +700; Bowers+G.Wilson 25+ each half +480.
**Half splits [nflverse pbp; OT counted in H2]:** 2026 (5 G) H1/H2 yards: NO 87/29, KC 41/45, NE 69/41, BUF 0/70, LA 21/52. 25+ H1 3/5, H2 5/5, both 3/5. 2025 (12 G): H1 42%, H2 58%, both 2/12 (17%). Correlation between halves: about 0 in 2025, -0.96 in 2026. One big half tends to come with a quiet half.
**Model:** full-game median ~70 (lognormal, calibrated to the FD ladder: P50 .70, P90 .31), 4% dud risk, half share Beta(1.5 to 2), which matches his empirical share SD of ~0.25-0.28. Each half alone ~.62-.65; both p≈0.34-0.38, mid 0.36. Jets context (blitz leakage, slot vs Ponds/Sherwood, close game, Cousins at 33-35 attempts) is already priced in the 68.5 line. No extra bump.
**Shrink:** p'=0.5+0.7(0.36-0.5)=0.402. Edge vs ~40% no-vig ≈ 0 pts; vs 44.4% implied = -4.2. **FAIL** (needs 3+). Note: the shrink pulls a sub-50% p up, which flatters this leg; the raw edge is clearly negative.
**Rules:** not on Ticket 2 ✓. 8A ✓ (PFR per-defender + Sharp MOF/man-zone in pack). Snaps 79/82/70/98/84%, so the 60% gate passes ✓. Injury: was Q (calf, limited Wed); the pack shows Active Oct 31. Re-check at the 90-minute inactives.
