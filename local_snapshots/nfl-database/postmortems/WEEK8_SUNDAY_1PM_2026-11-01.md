# Week 8 Sunday postmortem — 1 PM ET window (Nov 1, 2026)
_Built by Blitz from public sources: ESPN game summaries (box score, play-by-play, scoring plays, gameInfo weather), pulled 3:27–4:30 PM ET, plus our pregame run folders (`runs/2026-11-01_*`), `week8/inactives/phase15_1pm_2026-11-01.md`, `week8/slips/slips_2026-11-01.md` and `postmortems/RB_MISSES_2026-11-01.md` (folded in). Read-only. No bets, no outside messages._

**Data limits (stated, not filled in):** nflverse Week 8 play-by-play, FTN charting (blitz / pass rushers) and NGS (time to throw, pressure) aren't published for today's games yet. They usually land overnight to Tuesday. So **blitz rate, pressure rate, time to throw, per-defender coverage (who covered whom) and man/zone/MOF shells for today are NOT AVAILABLE.** What's below uses ESPN box sacks, defensive "QB HTS" and the play text. "Defender" in the explosives log is the **tackler named in the play text**, not charted coverage. It all gets re-graded when nflverse/FTN drop, through the scheduled play-log routine.

---
## ⚡ Why did Bijan Robinson have 0 catches? (ATL@TB, final TB 16–0)
**Verdict: the primary cause was game environment and play-calling. In a rain game, Atlanta barely threw to its backs, and Penix forced short throws to London, Pitts and Dotson instead. TB's pass rush was not the cause.**
- **Bijan's usage:** **1 target** all game (Q1 5:50, an incompletion on a short right throw), **0 catches**, plus **19 carries for 76 yards** (long 26). ATL's backs drew 3 of Penix's 24 targets (Bijan 1, Herbert 2). Route and snap counts aren't available until nflverse/FTN publish.
- **Penix's distribution:** 22 of 25 pass plays were tagged "short" and 3 "deep". Targets went London 6, Pitts 5, Dotson 5, Zaccheaus 2, Woerner 2, Herbert 1, Hooper 1, Bijan 1. All 4 INTs came on **short** throws (two short-middle, two short-right), into TB's underneath zone defenders. Anzalone (LB) had 2, plus Parrish (nickel) and McCollum (CB). That's the area where RB check-downs and option routes live, which points to TB's LBs sitting underneath rather than a spy, but there's no charting yet to confirm the shell.
- **Pressure: no.** Penix was **sacked 0 times, TB was credited with 0 QB hits**, and he had 1 scramble (7 yds). One roughing-the-passer penalty (A. Robinson, Q3). Without charting, **TB's blitz rate today is unknown**. Pregame, TB's season blitz rate was **41%** (FTN, L4 38%) and its pressure proxy was 16.4%.
- **Weather:** ESPN's game weather showed **rain, 74°F, 76% precipitation, gusts 14 mph**. Pregame NWS had 59–63% storm odds and gusts up to 29 mph. The play-by-play shows **no weather delay** (the only gap over 8 min was the normal halftime, 16 min). TB itself threw only 3 passes (0/3, −2 yds, 1 sack) with **52 rushes for 313 yds**, and Mayfield fumbled 3 times. That's the clearest sign of a wet ball and a run-only plan.
- **Game script:** TB led 6–0 after Q1 and 9–0 at the half, then 16–0 on Irving's 4-yd TD (Q3 3:47). ATL went 0-for-12 on third down and was trailing all day, which normally *raises* RB check-downs. They didn't come.
- **Pregame vs actual:** ATL's checkdown share was **32.2%**. Today only about 12% of Penix's targets (3/25) went to backs. Our model already leaned **under** on Bijan receptions: v6 P(over 3.5) was **.43/.44/.41**, and the 11:35 check marked it a **flag** ("market up, model down"). The PP25 Bijan 3.5 and $65 Bijan 2.5 legs were placed against that flag. TB's RB-receiving-allowed numbers weren't a gated input (Phase 4 has no LB/S mapping), which is a gap.

## 🌧️ Michael Penix Jr. (dedicated section)
| | Line |
|-|-|
|Comp/Att|**8/24 (33%)**|
|Yards / YPA|125 / **5.2** (76 of the 125 came on one Q4 throw to Dotson; **2.1 YPA on the other 23 attempts**)|
|TD / INT|**0 / 4**|
|Sacks / QB hits allowed|**0 / 0** (box)|
|Fumbles|1 (recovered by ATL, 0 lost)|
|Rushing|5–11 (incl. 1 scramble for 7)|
|Third down (team)|0/12|
- **Under pressure vs clean pocket, vs blitz, time to throw:** **not available yet** (needs FTN/NGS). The box is unambiguous on one thing: **0 sacks and 0 QB hits**. The user's read that "Penix is weak vs the blitz" can't be confirmed from today, and the evidence points the other way: he wasn't pressured into these mistakes. The 4 INTs were all short throws, **3 to the middle/underneath zone** (Anzalone x2, Parrish) plus 1 short-right to TE Woerner (McCollum). That looks like **throws into coverage**, worsened by a wet ball. A weather effect is likely but can't be separated cleanly. Where the user is **right:** the weather wrecked both passing games (TB went 0/3), and the check-downs didn't happen (3 RB targets).
- **TB's coverage and rush:** today's shell isn't charted. Pregame, TB was zone-heavy (Sharp: ~70% zone). The play text shows TB's LBs and nickel making plays underneath (Anzalone 2 INT, 2 PD; Parrish 1 INT, 3 PD; McCollum 1 INT).
- **Where his targets went and what it did to ATL props:** London 6 tgt, 1–8. Pitts 5 tgt, 2–6. Dotson 5 tgt, 2–95 (one 76-yd catch). Bijan 1 tgt, 0–0. Every ATL receiving over was dead.
- **Pregame vs actual:** Penix pass yds **under 229.5** had the model on the under (MC+GR p .555), and **we cut it only because of the Ghost6 "no unders on starting QB" rule**. It would have hit (125). London rec under 6.5 (p .60) **was cut because of the placed-ticket bar** (the user held London overs), and it would have hit. Pitts unders (p .58–.59) were cut as UNVERIFIED Phase 4 (TE mapping), and both would have hit (2 rec, 6 yds). Dotson under 25.5 was withdrawn on §7, and it lost (95 on one play).
- **User's placed legs in ATL@TB:** UD London 5.5 rec ❌ (1). FD8 London 5+ ❌. Ticket 2 London 4.5 rec ❌, Godwin 3.5 rec ❌ (0, 1 tgt). $51.50 SGP Godwin 2.5 rec ❌. PP25 Bijan 3.5 rec ❌ (0). $65 Bijan 2.5 rec ❌.
- **Would the new weather rule have flagged it?** **Yes.** The new Phase 11 fails closed at **50%+ precip OR 20+ mph gusts**. Pregame was 59–63% storm with 29 mph gusts, and ESPN's game reading was 76% precip. Under that rule **every ATL and TB passing/receiving over gets cut**: London 5+/5.5, Godwin 3+/4+, Bijan rec 2.5/3.5, Pitts/Dotson overs. The gate output would also list all 7 of the user's placed ATL/TB legs above for an alert. Under the old rule (sustained wind 15+ only), it passed.

### Missed TB run-script legs
- **Bucky Irving 27–170, TD (long 46).** We priced only his **unders** (rush U70.5, rush+rec U90.5). Both were cut (the "no unders on primary star" rule, and Phase 4 UNVERIFIED), and both would have lost. **No Irving rush over was ever built.**
- **Kenny Gainwell 25–140.** **Never priced.**
- Root cause: TB was only −2.5, so the new game-script RB rule (7+ fav) **would not** have fired on spread. It **would** fire under its weather-flag branch (rush overs modeled before pass overs, RB2 modeled), had the new weather threshold been in place pregame. ATL's run D: the 46-yarder by Irving was finished by **C. Henderson**. TB had 7 runs of 10+ yds against ATL (see log).

---
## ✈️ LV@NYJ — "we missed the mark" (Final: LV 38, NYJ 33)
**Pregame read:** total 45.5, NYJ −1.5. We expected a modest game and priced only pass-catcher legs plus Cousins/Geno yards. **The game went 71 points.**
- **Our only vetted leg, Tre Tucker rec O3.5, lost (0 catches, 1 target).** Tucker O3.5 also sat on the BONUS_SLIP and FD7_REPLACEMENTS list. Thankfully neither was placed.
- **Cousins pass yds O232.5** was cut on P14 (model p .395). **Actual 247 → it would have hit.** Bowers rec yds O68.5 was cut on the placed-ticket bar and P4 TE mapping. **Actual 92, 2 TD → it would have hit.** Bowers rec U5.5 was cut. Actual 7 → good cut. Geno pass U225.5 was cut. Actual 290 → good cut. Garrett Wilson unders were cut by the star rule. Actual 5 rec / 68 yds → over both lines, good cuts.
- **The user's Bowers legs all hit:** UD 49.5 ✅ (92), PP40 targets 8.5 ✅ (10), FD7/FD8 50+ ✅, PP20 halves with 25+ ✅ (40 in the 1st half, 52 in the 2nd).
- **Why we missed Braelon Allen (21–147, TD):** see the RB-misses section. LV@NYJ built **no NYJ RB legs**. Hall was out and Allen's role was never re-projected. In the bonus sweep he was cut at Phase 14 (.614 < .695 no-vig).
- **Why we missed Adonai Mitchell (7–142, TD on 9 targets):** he wasn't on our key-player list and was never priced (not a top-2 target earner pregame). Three of his catches went for 20+, all deep, against **T. Stukes** (47 yds, Q4), **J. McCoy** (22) and **E. Stokes** (20). The input that should catch this is a **CB weakness × WR3 deep-target check**. Our candidate list starts from target share, so a low-share deep threat vs a weak boundary CB slips through.
- **Mayer (5–53) and Jeanty (3–64 receiving, incl. a 45-yd catch-and-run):** never priced. Jeanty had just 2 carries; Mike Washington Jr. took 23. That's a **role change we didn't have**.
- **Pressure:** Cousins was sacked 1 time and Geno 2 times (box). Blitz and pressure rates aren't charted yet. Pregame NYJ's blitz rate was 38% and LV's 28%.
- **Explosives:** NYJ's D allowed 4 passes of 20+ (Bowers 27 and 23, both finished by **D. Belton**, plus Jeanty 45). LV's D allowed 5 passes of 20+ and 5 runs of 15+ (Allen x4, Stukes in on 3 of them). Full rows are in `playlogs/explosives_allowed.md`.
- **LV@NYJ verdict:** we got Bowers right on the user's tickets and dodged the Wilson/Geno unders, but **we missed the shootout script**. The underpriced inputs were the total, Allen's injury promotion, a WR3 deep threat vs a weak CB, and LV's backfield role change. The only vetted leg (Tucker) lost.

## 🦁 MIN@DET — Gibbs and Amon-Ra (Final: DET 19, MIN 15)
**What happened to Gibbs: 23 carries, 153 yds, TD (30-yd TD run, long 30); 2 catches on 4 targets for 15.**
- **Why the rush leg was cut:** Gibbs **rush O87.5** was cut in the MIN@DET run on **Phase 14, "a model median does not clear the line"** (MC+GR p .58). **Rush+rec O121.5** was cut on P4 UNVERIFIED (RB-receiving mapping), **P5 FAIL** (MIN is a top-10 blitz D and Gibbs' blitzed share drops) and P14 (model p .414). **Both would have hit** (153 / 168).
- **The good news:** the **bonus-slip Gibbs O79.5 alt was VETTED** (gate passed at 11:54). It was dropped **only because of §11 (one slip per player)**, since Gibbs was already on Ticket 2. It would have hit.
- **Would the new rules have fired?** The game-script RB rule (7+ fav): **no**, DET was only −3. The proposed soft-run-D boost (≥4.4 YPC allowed): it depends on MIN's YPC input (to be checked in the fix's TDD fixture). The Bayes-veto→consensus fix (C): **yes**, the P14 kill came from a single median.
- **Why Gibbs 5.5 rec (and Ticket 2 Gibbs 4.5) and Goff 17 fantasy failed:** a run-heavy script. DET ran it 23 times with Gibbs plus 10 with Vaki, and Goff threw **only 25 passes** (18/25, 176, 1 TD, 1 INT) and was **sacked 4 times for 22**. MIN's season blitz rate was **71%** (FTN, pregame), and Gibbs' receptions (2) suffered. Goff's PrizePicks fantasy came to about **10.0** (176×.04 + 4 − 1) vs 17.
- **St. Brown: 7 rec on 8 targets, 46 yds, 0 TD.** The red-zone work went to the run game (Gibbs' 30-yd TD, and DET kicked FGs) plus Jameson Williams (4–70, TD). We didn't price a St. Brown TD (TD legs go on separate slips). His yardage lines (49.5/59.5) missed by 3–13 yds, and his receptions (5.5) hit.
- **MIN defenders on the runs:** Gibbs' explosives were finished by **B. Murphy** (19, 14, 12), **J. Metellus** (17, 11) and **H. Smith**. The 30-yd TD had no tackler.
- **DET's D:** allowed Addison 51 (**K. Dorsey**), Yurosek 24 and Hockenson 22 (**B. Branch**), plus 7 runs of 10+ (Mason, Murray scrambles).
- **Pressure:** Goff was sacked 4 times (22 yds) and Murray 3 times (25). Pressure and blitz rates for today aren't charted yet.

---
## 🏃 RB pattern: we underprice the run-script RB rushing leg and overprice RB receiving
| RB | Game | Rush | Pregame status | Cause |
|-|-|-|-|-|
|Gibbs|MIN@DET|23–153, TD|O87.5 cut P14 (one median); O79.5 alt vetted, dropped §11|single-model veto; §11|
|Braelon Allen|LV@NYJ|21–147, TD|never in the run; O59.5/69.5 cut P14 in the bonus sweep|no injury promotion (Hall out)|
|Jaylen Warren|CLE@PIT|17–143, TD|O64.5 cut P14 (Bayes median 63.0)|single-model veto; split flag only|
|Tony Pollard|TEN@CIN|21–117, 2 TD|O65.5 cut P6/P7/P13 (dog blocks) though all 3 medians cleared|blanket underdog block; Spears out not promoted|
|Bhayshul Tuten|IND@JAX|16–104, TD (+2–55, TD rec)|O59.5 cut P7 carry share|carry-share solo-cut (now fixed by the game-script RB rule)|
|Bucky Irving|ATL@TB|27–170, TD|only unders priced|weather branch didn't exist; no over built|
|Kenny Gainwell|ATL@TB|25–140|never priced|RB2 never modeled|
And the RB receiving overs: Gibbs 4.5/5.5 rec ❌ (2), Bijan 2.5/3.5 rec ❌ (0), Warren rec 1 for 0.

**Proposed fix (proposal only, no changes made):** add a Phase 7/14 **"RB rush-first" rule**:
1. Every team's projected carries leader and RB2 get a rush leg evaluated (gate fails if missing; fix B in RB_MISSES).
2. For RB rushing, **cut on 2-of-3 medians, not 1** (fix C).
3. Injury promotion when an RB1 is out (fix A).
4. A soft-run-D boost at ≥4.4 YPC allowed regardless of spread (fix F).
5. A **receiving haircut for RBs** when the team is a favorite in a run script or a weather-flagged game (cap RB rec overs at the low rung or cut).

Regression fixtures: today's Gibbs, Allen, Warren, Pollard, Tuten and Irving rush overs must reach pricing, and Gibbs 5.5 rec / Bijan 3.5 rec must be flagged.

---
## IND@JAX (Final: JAX 42, IND 7)
- **Script:** JAX ran away early in rain (pregame JAX went from 14% to 71% rain). Lawrence threw only 14 times for 210 (10/14, TD to BTJ), and Ewers mopped up.
- **Tuten 16–104, TD + 2–55, TD rec.** Cut at Phase 7 → the game-script RB rule's regression fixture.
- **Parker Washington 1–16 on 2 targets → FD7 and FD8 40+ legs ❌.** Cause: game script (blowout, run-first) plus Meyers active (flagged mild hurt at 11:35). Weather (71%) would trip the new rule and cut it.
- **Our IND cuts were right:** Daniel Jones O192.5 cut → actual 144 ✅ good cut. Taylor rush O50.5 cut → 8–23 ✅ good cut. Tyler Warren rec O4.5 cut → 4 ✅ good cut. Downs/Allen/Pittman overs were all cut.

## CLE@PIT (Final: PIT 27, CLE 6)
- **Warren 17–143, TD; Dowdle 15–56, TD.** The user's PP25 Warren 69.5 rush+rec goblin ✅. $65 Warren 14.5 fantasy ✅ (~21.3).
- **Watson sacked 7 times** (box), 24/36 for 261. Fannin 10–154 on 12 targets (never priced; P4 TE rule cuts TE legs). **Denzel Boston 6–37 on 11 targets → UD 29.5 ✅ hit.** DK Metcalf 1–4 on 6 targets: he **disappeared** (coverage detail not charted yet).

## Other games (auto tables below). ⚠️ ARI@DAL (30–30, 0:06 Q4), BAL@BUF (BUF 36–10, 2:00 Q4) and TEN@CIN (36–36, 1:17 Q4) were **still live at the last pull (~4:20 PM ET)**. Their stats are near-final and get re-graded on the next refresh.
ARI@DAL (Lamb 7–58 on 10 targets; Pickens 2–48), BAL@BUF (**Lamar Jackson hurt on his first pass, Q1 10:04**; Fagnano/Huntley took over; **Zay Flowers 0 catches on 5 targets**) and TEN@CIN (TEN led 13–0, back-and-forth, **tied 36–36 with 1:17 left at last pull**. Burrow 4 TD passes; Higgins 7–100, TD; Chase 8–93, TD; Pollard 2 rush TD but also a safety) are in the per-game tables. See "who disappeared".

---
## Who disappeared, and why
| Player | Line(s) | Actual | Cause |
|-|-|-|-|
|Zay Flowers|49.5/60+ yds, 6 rec|0 rec on 5 tgt|**Injury to QB**: Lamar hurt Q1. Backups Fagnano/Huntley combined 11/24 for 83. 6 placed legs died.|
|Drake London|5.5 rec|1–8 on 6 tgt|Weather (rain), Penix's 4 INTs (2 targeted London), 0/12 on 3rd down|
|Bijan Robinson|3.5/2.5 rec|0 on 1 tgt|No RB throws in a weather/run plan (see top)|
|Chris Godwin|2.5/3.5 rec|0 on 1 tgt|TB threw 3 passes all game|
|Parker Washington|40+ yds|1–16|Blowout + run script + rain; Meyers active|
|Jonathan Taylor|O50.5 rush (cut)|8–23|IND trailed 42–7; JAX's run D|
|DK Metcalf|—|1–4 on 6 tgt|Coverage detail not charted yet|
|Jerry Jeudy|—|0 on 1 tgt|Volume went to Fannin/Boston|
|Gibbs (receiving)|4.5/5.5 rec|2 on 4 tgt|Run-heavy script; MIN 71% blitz D → quick throws went elsewhere|

## Placed tickets graded (1 PM legs; 4 PM legs pending)
| Ticket | 1 PM legs | Status |
|-|-|-|
|PP $40 Power|Higgins FS 14.5 ✅ (≈23), Lamb 4.5 rec ✅ (7), Bowers 8.5 tgt ✅ (10), St. Brown 5.5 rec ✅ (7)|**alive** (Higgins FS from a near-final box; Stafford comp, Walker 97.5 pending)|
|UD $20|Bowers 49.5 ✅, Lamb 4.5 ✅, London 5.5 ❌, Flowers 49.5 ❌, St. Brown 49.5 ❌ (46), Boston 29.5 ✅ (37)|**lost**|
|PP $20 Power|Higgins 68.5 ✅ (100), Lamb 4.5 ✅, Bowers halves ✅ (40/52)|**alive** (Kyren+Walker TD combo, Stafford, Mahomes pending)|
|PP $25 Power|Flowers 6 ❌ (0), Bijan 3.5 ❌ (0), Lamb 6.5 ✅ (7), St. Brown 7 → **7 (push if the line was 7; miss if 7.5)**, Warren 69.5 ✅ (143)|**lost**|
|PP $300 bonus Flex|Lamb 6.5 ✅, Goff 17 FS ❌ (≈10.0), Jameson Williams 10.5 FS ✅ (≈17.0), St. Brown 9.5 tgt ❌ (8), Gibbs 5.5 rec ❌ (2), LaPorta 5 rec ❌ (3)|**lost** (2/6)|
|PP $65 Power|Lamb 7.5 rec ❌ (7), Cook 59.5 rush ✅ (80), Bijan 2.5 ❌, Warren 14.5 FS ✅ (≈21.3), Puka 69.5 (4 PM)|**lost**|
|FD 7-leg / FD 8-leg|Flowers 60+ ❌, P. Washington 40+ ❌, Higgins 4+ ✅, Bowers 50+ ✅, Lamb 50+ ✅ (58), London 5+ ❌ (FD8)|**both lost**|
|FD Ticket 2 SGP+ $63|Gibbs 5+ ❌, St. Brown 60+ ❌, Godwin 4+ ❌, London 5+ ❌, Flowers 5+ ❌, Pickens 4+ ❌ (2), Lamb 60+ ❌ (58)|**lost**|
|FD $51.50 SGP|Pickens 5+ ❌, Higgins 50+ ✅, Godwin 3+ ❌, Flowers 50+ ❌|**lost**|
_Fantasy scores use PrizePicks scoring (1/rec, .1/yd, 6/TD, .04/pass yd, 4/pass TD, −1/INT) from the ESPN box. Fumbles aren't netted, so they're marked ≈._

## What went well (reads we got right)
- **Bowers:** every user Bowers leg hit. We'd flagged the NYJ CB Wright and EDGE Bailey outs as helping.
- **Lamb receptions 4.5 (×3 tickets) and 6.5:** hit (7). **Higgins 68.5 and 4+:** hit (7–100, TD). Our 11:35 "Burrow locks onto CB mismatches" read: Higgins and Chase both went over 90.
- **Warren 69.5 goblin and 14.5 FS:** hit, despite our own split flag.
- **Bijan rec under-lean:** our model said under (p .41–.44), and the flag was right.
- **Good cuts** (cut legs that would have lost): Daniel Jones O192.5, J. Taylor O50.5, Tyler Warren O4.5 rec, Geno U225.5, Wilson unders, Bowers U5.5 (see per-game tables).
- **Vetted Gibbs O79.5 alt:** correct. Only §11 kept it off.

## What we missed (root causes)
1. **RB rushing overs** (table above): single-model median veto, no injury promotion, blanket dog block, no RB2/weather branch.
2. **Weather threshold:** ATL@TB passed the old rule. The new 50%/20 mph rule would have cut 7 placed legs' worth of ATL/TB receiving overs, and IND@JAX's P. Washington.
3. **QB injury risk not modeled:** Flowers sat on 6 placed legs. Lamar was coming back from a 3-game absence, and no "returning-QB fragility" haircut or exposure cap was applied.
4. **Exposure concentration:** Flowers 6 legs, London 3, Bijan 2. One bad game environment killed multiple tickets.
5. **The shootout total (LV@NYJ)** and **WR3 deep threats vs weak CBs** (Mitchell) weren't in the candidate list.
6. **The "no unders on primary stars" rule** cost us Penix U229.5 (would have hit). Keep it, but log it as a cost.

## Lessons and proposed fixes (proposals only, nothing changed)
- **A–F from RB_MISSES** + the **RB rush-first/RB-receiving haircut** above.
- **Weather rule (already adopted):** add regression fixtures from today: ATL@TB (76% precip, pregame 29 mph gusts) must cut London/Godwin/Bijan rec overs, and IND@JAX (71%) must cut P. Washington 40+.
- **Returning-QB fragility flag:** when a QB returns from 2+ missed games, cap user exposure on his WR1 at 2 tickets and price a backup-QB scenario into the sims.
- **Exposure cap per game environment:** no more than 3 legs from one weather-flagged or single-QB-dependent game across tickets.
- **Candidate list expansion:** add WR3s with a 15%+ deep-target share vs CBs allowing 12+ YPT, and every team's RB1 and RB2.
- **Re-grade with charting:** when FTN/NGS/nflverse publish, re-run pressure/blitz/time-to-throw per QB and coverage-by-defender for every leg here (play-log routine Mon/Tue).


---
# Per-game tables (auto-built from ESPN box/play-by-play)

## ARI@DAL — ARI 30, DAL 30 (In Progress)

By quarter: DAL 7-7-3-13; ARI 0-3-7-20

**Scoring log**

|Q|Clock|Team|Type|Play|Score (away-home)|
|-|-|-|-|-|-|
|1|2:33|DAL|Fumble Return Touchdown|Javonte Williams 2 Yd Rush Javonte Williams Fumble James Mitchell 0 Yd Fumble Recovery (Brandon Aubrey Kick)|0-7|
|2|5:16|DAL|Passing Touchdown|Ryan Flournoy 9 Yd pass from Dak Prescott (Brandon Aubrey Kick)|0-14|
|2|1:13|ARI|Field Goal Good|Chad Ryland 37 Yd Field Goal|3-14|
|3|6:37|DAL|Field Goal Good|Brandon Aubrey 31 Yd Field Goal|3-17|
|3|0:57|ARI|Rushing Touchdown|Tyler Allgeier 63 Yd Rush (Chad Ryland Kick)|10-17|
|4|14:20|DAL|Rushing Touchdown|Dak Prescott 5 Yd Rush (Brandon Aubrey Kick)|10-24|
|4|10:47|ARI|Passing Touchdown|Tyler Allgeier 5 Yd pass from Gardner Minshew II (Chad Ryland Kick)|17-24|
|4|3:54|DAL|Field Goal Good|Brandon Aubrey 35 Yd Field Goal|17-27|
|4|2:11|ARI|Passing Touchdown|Trey McBride 14 Yd pass from Gardner Minshew II (Chad Ryland Kick)|24-27|
|4|1:09|DAL|Field Goal Good|Brandon Aubrey 41 Yd Field Goal|24-30|
|4|0:06|ARI|Passing Touchdown|Michael Wilson 13 Yd pass from Gardner Minshew II |30-30|

**QB lines** (box; QB hits = defensive box 'QB HTS' by the opponent)

|QB|Team|C/Att|Yds|Y/A|TD|INT|Sacks|Opp QB hits|Scrambles/rush|
|-|-|-|-|-|-|-|-|-|-|
|Gardner Minshew II|ARI|15/20|173|8.7|3|0|0-0|10|0-0|
|Jacoby Brissett|ARI|10/23|119|5.2|0|1|4-36|10|3-7|
|Dak Prescott|DAL|19/27|195|7.2|1|0|3-20|5|6-21|

**Usage** (target share = player targets / team targets in box)

|Player|Team|Tgt|Tgt share|Rec|Rec yds|TD|Car|Carry share|Rush yds|Rush TD|
|-|-|-|-|-|-|-|-|-|-|-|
|Michael Wilson|ARI|15|39%|8|111|1|0|0%|0|0|
|Tyler Allgeier|ARI|5|13%|5|44|1|6|29%|128|1|
|Trey McBride|ARI|6|16%|6|64|1|0|0%|0|0|
|Elijah Higgins|ARI|4|11%|2|10|0|0|0%|0|0|
|Bam Knight|ARI|2|5%|1|10|0|3|14%|8|0|
|Jeremiyah Love|ARI|0|0%|0|0|0|9|43%|23|0|
|Kendrick Bourne|ARI|2|5%|1|29|0|0|0%|0|0|
|Reggie Virgil|ARI|2|5%|0|0|0|0|0%|0|0|
|CeeDee Lamb|DAL|10|38%|7|58|0|0|0%|0|0|
|Javonte Williams|DAL|2|8%|1|1|0|23|62%|54|0|
|Tyler Goodson|DAL|2|8%|2|19|0|7|19%|14|0|
|Ryan Flournoy|DAL|4|15%|3|38|1|1|3%|3|0|
|Brevyn Spann-Ford|DAL|4|15%|4|31|0|0|0%|0|0|
|George Pickens|DAL|4|15%|2|48|0|0|0%|0|0|

**Explosives allowed** (20+ yd completions, 10+ yd runs; tacklers from play-by-play text, *not* coverage charting): ARI defense pass20 x2; DAL defense pass20 x4; DAL defense rush15 x2

|Def|Kind|Yds|Q|Play|
|-|-|-|-|-|
|DAL|rush15|63|3|T.Allgeier up the middle for 63 yards, TOUCHDOWN. C.Ryland extra point is GOOD, Center-C.Kreiter, Holder-B.Gillikin.|
|DAL|rush15|52|4|T.Allgeier left end to DAL 28 for 52 yards (D.Bland).|
|ARI|pass20|37|3|D.Prescott pass short left to G.Pickens ran ob at ARZ 25 for 37 yards (D.Burke).|
|DAL|pass20|29|2|(Shotgun) J.Brissett pass short middle to K.Bourne to DAL 46 for 29 yards (P.Locke).|
|ARI|pass20|27|2|(Shotgun) B.Jones reported in as eligible.  D.Prescott pass deep left to C.Lamb pushed ob at ARZ 39 for 27 yards (M.Melton).|
|DAL|pass20|27|4|(Shotgun) G.Minshew pass deep right to Mi.Wilson to DAL 13 for 27 yards (D.Bland).|
|DAL|pass20|22|1|(Shotgun) J.Brissett pass deep left to Mi.Wilson ran ob at ARZ 47 for 22 yards.|
|DAL|pass20|21|4|(Shotgun) G.Minshew pass deep right to Mi.Wilson to DAL 45 for 21 yards (D.Bland).|

**Our legs graded (pregame manifests + placed tickets)**

|Source|Leg|Status|Model p (MC+GR)|Actual|Result|Main cut reason|
|-|-|-|-|-|-|-|
|ARI@DAL|Jacoby Brissett Pass Yds Under 258.5|CUT|0.4948|119.0|HIT (cut leg would have hit)|P13 FAIL: trailing-team passing/receiving under BLOCKED|
|ARI@DAL|Tyler Allgeier Rush Yds Over 13.5|CUT|0.7667|128.0|HIT (cut leg would have hit)|P6 FAIL: clutch D/F: no trailing-script overs|
|ARI@DAL|Bam Knight Rush Yds Over 19.5|CUT|0.5772|8.0|MISS (good cut)|P2 FAIL: not primary back or proj < line|
|ARI@DAL|Michael Wilson Rec Yds Under 56.5|CUT|0.5437|111.0|MISS (good cut)|P4 MISSING: defender not in PFR cache|
|ARI@DAL|Michael Wilson Receptions Under 4.5|CUT|0.4971|8.0|MISS (good cut)|P4 MISSING: defender not in PFR cache|
|ARI@DAL|Trey McBride Rec Yds Under 71.5|CUT|0.5493|64.0|HIT (cut leg would have hit)|P4 UNVERIFIED: TE defender mapping not ruled (ISS-05); man 21.3% / zone 69.9%, MOF closed |
|ARI@DAL|Trey McBride Receptions Over 7.5|CUT|0.6014|6.0|MISS (good cut)|P4 UNVERIFIED: TE defender mapping not ruled (ISS-05); man 21.3% / zone 69.9%, MOF closed |
|ARI@DAL|Dak Prescott Pass Yds Under 271.5|CUT|0.4364|195.0|HIT (cut leg would have hit)|P14 FAIL: edge +0.1 < +3; model p 0.427 < .45; a model median does not clear the line; MOD|
|ARI@DAL|Javonte Williams Rush Yds Under 76.5|CUT|0.5796|54.0|HIT (cut leg would have hit)|P13 FAIL: 6.5+ favorite rush under vs clock-killing script|
|ARI@DAL|Javonte Williams Rush+Rec Yds Under 92.5|CUT|0.5799|55.0|HIT (cut leg would have hit)|P4 UNVERIFIED: RB receiving defender mapping: no LB/S alignment source; man 9.1% / zone 70|
|ARI@DAL|CeeDee Lamb Rec Yds Over 80.5|CUT|0.556|58.0|MISS (good cut)|P14 FAIL: placed-ticket bar: Ticket 2 Lamb 60+ yds; FD 7-leg Lamb 50+; edge +2.3 < +3; a m|
|ARI@DAL|CeeDee Lamb Receptions Over 6.5|CUT|0.5295|7.0|HIT (cut leg would have hit)|P14 FAIL: placed-ticket bar: PP40/PP20/UD20 Lamb o4.5 rec; PP25 o6.5; edge +2.2 < +3; mode|
|ARI@DAL|George Pickens Rec Yds Over 59.5|CUT|0.6011|48.0|MISS (good cut)|P14 FAIL: edge +0.9 < +3; shrunk edge -1.3 not > 0|
|ARI@DAL|George Pickens Receptions Over 3.5|CUT|0.7418|2.0|MISS (good cut)|P2 FAIL: same-role teammate >=28%: [('CeeDee Lamb', 0.2967032967032967)]|
|ARI@DAL|Ryan Flournoy Rec Yds Over 36.5|CUT|0.5521|38.0|HIT (cut leg would have hit)|P2 FAIL: not top-2 target earner (#3)|
|ARI@DAL|Ryan Flournoy Receptions Over 3.5|CUT|0.4971|3.0|MISS (good cut)|P2 FAIL: not top-2 target earner (#3); 5+ tgt in <3 of last 4; same-role teammate >=28%: [|
|DFS_SLIPS|[PP $40 6-pick Power] CeeDee Lamb Receptions Over 4.5|CUT||7.0|HIT|P14 FAIL: edge -5.2 < +3; shrunk edge -11.5 not > 0|
|DFS_SLIPS|[UD $20 8-pick] CeeDee Lamb Receptions Over 4.5|CUT||7.0|HIT|P14 FAIL: edge -5.2 < +3; shrunk edge -11.5 not > 0|
|DFS_SLIPS|[PP $20 6-pick Power] CeeDee Lamb Receptions Over 4.5|CUT||7.0|HIT|P14 FAIL: edge -5.2 < +3; shrunk edge -11.5 not > 0|
|DFS_SLIPS|[PP $25 6-pick Power] CeeDee Lamb Receptions Over 6.5|CUT||7.0|HIT|P14 FAIL: edge +2.2 < +3; model p 0.449 < .45; a model median does not clear the line|
|DFS_SLIPS|[FD 7-leg +694] CeeDee Lamb Rec Yds Over 49.5|CUT||58.0|HIT|P14 FAIL: edge -4.0 < +3; shrunk edge -11.3 not > 0|
|DFS_SLIPS|[FD Ticket 2 SGP+ $63 +1508] George Pickens Receptions Over 3.5|CUT||2.0|MISS|P2 FAIL: same-role teammate >=28%: [('CeeDee Lamb', 0.2967032967032967)]|
|DFS_SLIPS|[FD Ticket 2 SGP+ $63 +1508] CeeDee Lamb Rec Yds Over 59.5|CUT||58.0|MISS|P14 FAIL: edge -2.4 < +3; shrunk edge -7.5 not > 0|
|DFS_SLIPS|[FD $51.50 8-leg SGP] George Pickens Receptions Over 4.5|CUT||2.0|MISS|P2 FAIL: same-role teammate >=28%: [('CeeDee Lamb', 0.2967032967032967)]|

## ATL@TB — ATL 0, TB 16 (Final)

By quarter: TB 6-3-7-0; ATL 0-0-0-0

**Scoring log**

|Q|Clock|Team|Type|Play|Score (away-home)|
|-|-|-|-|-|-|
|1|7:43|TB|Field Goal Good|Chase McLaughlin 46 Yd Field Goal |0-3|
|1|4:02|TB|Field Goal Good|Chase McLaughlin 34 Yd Field Goal|0-6|
|2|4:04|TB|Field Goal Good|Chase McLaughlin 42 Yd Field Goal|0-9|
|3|3:47|TB|Rushing Touchdown|Bucky Irving 4 Yd Rush (Chase McLaughlin Kick)|0-16|

**QB lines** (box; QB hits = defensive box 'QB HTS' by the opponent)

|QB|Team|C/Att|Yds|Y/A|TD|INT|Sacks|Opp QB hits|Scrambles/rush|
|-|-|-|-|-|-|-|-|-|-|
|Michael Penix Jr.|ATL|8/24|125|5.2|0|4|0-0|0|5-11|
|Baker Mayfield|TB|0/3|0|0.0|0|0|1-2|1|4-14|

**Usage** (target share = player targets / team targets in box)

|Player|Team|Tgt|Tgt share|Rec|Rec yds|TD|Car|Carry share|Rush yds|Rush TD|
|-|-|-|-|-|-|-|-|-|-|-|
|Bijan Robinson|ATL|1|4%|0|0|0|19|68%|76|0|
|Drake London|ATL|6|26%|1|8|0|0|0%|0|0|
|Jahan Dotson|ATL|5|22%|2|95|0|0|0%|0|0|
|Kyle Pitts Sr.|ATL|5|22%|2|6|0|0|0%|0|0|
|Khalil Herbert|ATL|1|4%|1|3|0|4|14%|12|0|
|Charlie Woerner|ATL|2|9%|0|0|0|0|0%|0|0|
|Olamide Zaccheaus|ATL|2|9%|1|4|0|0|0%|0|0|
|Kenny Gainwell|TB|1|33%|0|0|0|25|45%|140|0|
|Bucky Irving|TB|0|0%|0|0|0|27|48%|170|1|

**Explosives allowed** (20+ yd completions, 10+ yd runs; tacklers from play-by-play text, *not* coverage charting): ATL defense rush10 x5; ATL defense rush15 x4; TB defense pass20 x1; TB defense rush10 x1; TB defense rush15 x1

|Def|Kind|Yds|Q|Play|
|-|-|-|-|-|
|TB|pass20|76|4|(Shotgun) M.Penix pass deep left to J.Dotson to TB 22 for 76 yards (A.Winfield).|
|ATL|rush15|46|3|(Shotgun) B.Irving left end to ATL 35 for 46 yards (C.Henderson).|
|ATL|rush15|28|3|K.Gainwell left end to ATL 6 for 28 yards (K.Daniels; M.Smith).|
|TB|rush15|26|2|C.Levin reported in as eligible.  Bi.Robinson left guard pushed ob at TB 36 for 26 yards (J.Parrish).|
|ATL|rush15|24|1|B.Irving up the middle to ATL 33 for 24 yards (J.Bates; S.Ebukam).|
|ATL|rush15|20|2|(Shotgun) K.Gainwell left tackle to ATL 28 for 20 yards (A.Terrell).|
|ATL|rush10|13|2|(Shotgun) B.Irving left end to TB 49 for 13 yards (C.Thomas; X.Watts).|
|ATL|rush10|12|1|B.Irving right guard to TB 25 for 12 yards (K.Daniels).|
|ATL|rush10|12|4|K.Gainwell right guard to TB 43 for 12 yards (G.Dexter).|
|ATL|rush10|12|4|K.Gainwell right tackle to ATL 45 for 12 yards (X.Watts; K.Daniels).|
|TB|rush10|10|2|Bi.Robinson left tackle to TB 45 for 10 yards (J.Trotter; J.Parrish).|
|ATL|rush10|10|4|K.Gainwell right end to TB 43 for 10 yards (X.Watts).|

**Our legs graded (pregame manifests + placed tickets)**

|Source|Leg|Status|Model p (MC+GR)|Actual|Result|Main cut reason|
|-|-|-|-|-|-|-|
|ATL@TB|Michael Penix Jr. Pass Yds Under 229.5|CUT|0.5552|125.0|HIT (cut leg would have hit)|P14 FAIL: under on primary star (Ghost6 rule) - ATL starting QB; cut 2026-11-01 07:34 ET|
|ATL@TB|Bijan Robinson Rush Yds Under 80.5|CUT|0.6443|76.0|HIT (cut leg would have hit)|P10 UNVERIFIED: no cited caption play re-matched a fresh pbp row for this player|
|ATL@TB|Bijan Robinson Rush+Rec Yds Under 117.5|CUT|0.6984|76.0|HIT (cut leg would have hit)|P4 UNVERIFIED: RB receiving defender mapping: no LB/S alignment source; man 17.2% / zone 7|
|ATL@TB|Drake London Rec Yds Under 79.5|CUT|0.5227|8.0|HIT (cut leg would have hit)|P14 FAIL: under on primary star (Ghost6 rule) - ATL target leader (57 tgt); cut 2026-11-01|
|ATL@TB|Drake London Receptions Under 6.5|CUT|0.6018|1.0|HIT (cut leg would have hit)|P14 FAIL: placed-ticket bar: UD20 o5.5; Ticket 2 5+|
|ATL@TB|Jahan Dotson Rec Yds Under 25.5|CUT|0.5744|95.0|MISS (good cut)|WITHDRAWN by Ghost6; fails §7|
|ATL@TB|Jahan Dotson Receptions Under 2.5|CUT|0.7259|2.0|HIT (cut leg would have hit)|P14 FAIL: same-player duplicate of Dotson Rec Yds Under 25.5 (Ghost6: pick one; kept the -|
|ATL@TB|Baker Mayfield Pass Yds Under 215.5|CUT|0.7315|0.0|HIT (cut leg would have hit)|P3 FAIL: under vs top-8 pass yds allowed (rank 4)|
|ATL@TB|Bucky Irving Rush Yds Under 70.5|CUT|0.5261|170.0|MISS (good cut)|P14 FAIL: under on primary star (Ghost6 rule) - TB RB1 (120 car); cut 2026-11-01 07:34 ET|
|ATL@TB|Bucky Irving Rush+Rec Yds Under 90.5|CUT|0.5858|170.0|MISS (good cut)|P4 UNVERIFIED: RB receiving defender mapping: no LB/S alignment source; man 21.9% / zone 7|
|ATL@TB|Chris Godwin Jr. Rec Yds Under 39.5|CUT|0.5417|0.0|HIT (cut leg would have hit)|P4 UNVERIFIED: defender sample 7 tgt < 8: too thin to grade|
|ATL@TB|Chris Godwin Jr. Receptions Under 4.5|CUT|0.6482|0.0|HIT (cut leg would have hit)|P4 UNVERIFIED: defender sample 7 tgt < 8: too thin to grade|
|DFS_SLIPS|[UD $20 8-pick] Drake London Receptions Over 5.5|CUT||1.0|MISS|P14 FAIL: edge -10.2 < +3; shrunk edge -10.5 not > 0; a model median does not clear the li|
|DFS_SLIPS|[PP $25 6-pick Power] Bijan Robinson Receptions Over 3.5|CUT||0.0|MISS|P10 UNVERIFIED: no cited caption play re-matched a fresh pbp row for this player|
|DFS_SLIPS|[FD Ticket 2 SGP+ $63 +1508] Chris Godwin Jr. Receptions Over 3.5|CUT||0.0|MISS|P4 UNVERIFIED: defender sample 7 tgt < 8: too thin to grade|
|DFS_SLIPS|[FD Ticket 2 SGP+ $63 +1508] Drake London Receptions Over 4.5|CUT||1.0|MISS|P14 FAIL: edge -8.2 < +3; shrunk edge -12.9 not > 0|
|DFS_SLIPS|[FD $51.50 8-leg SGP] Chris Godwin Jr. Receptions Over 2.5|CUT||0.0|MISS|P4 UNVERIFIED: defender sample 7 tgt < 8: too thin to grade|
|FD7_REPLACEMENTS|Jahan Dotson Rec Yds Under 25.5|CUT|0.5744|95.0|MISS (good cut)|WITHDRAWN by Ghost6; fails §7|

## BAL@BUF — BAL 10, BUF 36 (In Progress)

By quarter: BUF 10-6-7-13; BAL 7-0-3-0

**Scoring log**

|Q|Clock|Team|Type|Play|Score (away-home)|
|-|-|-|-|-|-|
|1|10:10|BUF|Rushing Touchdown|Josh Allen 1 Yd Rush (Tyler Bass Kick)|0-7|
|1|6:05|BUF|Field Goal Good|Tyler Bass 56 Yd Field Goal|0-10|
|1|3:18|BAL|Rushing Touchdown|Derrick Henry 2 Yd Rush (Tyler Loop Kick)|7-10|
|2|9:50|BUF|Field Goal Good|Tyler Bass 22 Yd Field Goal|7-13|
|2|0:09|BUF|Field Goal Good|Tyler Bass 51 Yd Field Goal|7-16|
|3|11:28|BAL|Field Goal Good|Tyler Loop 26 Yd Field Goal |10-16|
|3|8:59|BUF|Rushing Touchdown|James Cook III 5 Yd Rush (Tyler Bass Kick)|10-23|
|4|12:18|BUF|Passing Touchdown|DJ Moore 11 Yd pass from Josh Allen (Two-Point Pass Conversion Failed)|10-29|
|4|5:58|BUF|Passing Touchdown|Dalton Kincaid 23 Yd pass from Josh Allen (Tyler Bass Kick)|10-36|

**QB lines** (box; QB hits = defensive box 'QB HTS' by the opponent)

|QB|Team|C/Att|Yds|Y/A|TD|INT|Sacks|Opp QB hits|Scrambles/rush|
|-|-|-|-|-|-|-|-|-|-|
|Joe Fagnano|BAL|10/21|91|4.3|0|1|3-15|12|3-4|
|Lamar Jackson|BAL|0/1|0|0.0|0|0|0-0|12|0-0|
|Tyler Huntley|BAL|2/4|0|0.0|0|0|1-8|12|0-0|
|Josh Allen|BUF|21/34|289|8.5|2|1|1-9|5|7-30|

**Usage** (target share = player targets / team targets in box)

|Player|Team|Tgt|Tgt share|Rec|Rec yds|TD|Car|Carry share|Rush yds|Rush TD|
|-|-|-|-|-|-|-|-|-|-|-|
|Justice Hill|BAL|8|31%|4|20|0|3|16%|15|0|
|Derrick Henry|BAL|2|8%|2|7|0|11|58%|53|1|
|Zay Flowers|BAL|5|19%|0|0|0|0|0%|0|0|
|Mark Andrews|BAL|4|15%|3|14|0|0|0%|0|0|
|Rashod Bateman|BAL|3|12%|1|22|0|0|0%|0|0|
|Josh Cuevas|BAL|2|8%|1|15|0|0|0%|0|0|
|James Cook III|BUF|3|9%|2|21|0|21|55%|80|1|
|DJ Moore|BUF|7|21%|4|82|1|1|3%|4|0|
|Dalton Kincaid|BUF|6|18%|4|86|1|0|0%|0|0|
|Khalil Shakir|BUF|6|18%|5|64|0|0|0%|0|0|
|Ty Johnson|BUF|3|9%|3|19|0|4|11%|4|0|
|Keon Coleman|BUF|3|9%|1|4|0|0|0%|0|0|
|Dawson Knox|BUF|2|6%|1|6|0|0|0%|0|0|
|Jackson Hawes|BUF|2|6%|1|7|0|0|0%|0|0|
|Ray Davis|BUF|0|0%|0|0|0|5|13%|23|0|

**Explosives allowed** (20+ yd completions, 10+ yd runs; tacklers from play-by-play text, *not* coverage charting): BAL defense pass20 x4; BAL defense rush10 x2; BAL defense rush15 x1; BUF defense pass20 x1; BUF defense rush10 x1

|Def|Kind|Yds|Q|Play|
|-|-|-|-|-|
|BAL|pass20|49|3|(Shotgun) J.Allen pass deep middle to D.Moore to BLT 5 for 49 yards (M.Humphrey).|
|BAL|pass20|40|4|J.Allen pass deep left to D.Kincaid to BLT 13 for 40 yards (K.Wallace).|
|BAL|pass20|26|1|J.Allen pass short right to K.Shakir to BLT 23 for 26 yards (M.Humphrey; R.Smith).|
|BAL|pass20|23|4|J.Allen pass deep left to D.Kincaid for 23 yards, TOUCHDOWN. T.Bass extra point is GOOD, Center-R.Ferguson, Holder-T.Doman.|
|BUF|pass20|22|3|(Shotgun) J.Fagnano pass deep right to R.Bateman to BUF 43 for 22 yards (D.Hamlin).PENALTY on BUF-E.Oliver, Roughing the Passer, 15 yards, enforced at BUF 43.|
|BAL|rush15|16|2|J.Cook up the middle to BUF 34 for 16 yards (T.Tampa).|
|BAL|rush10|14|2|(Shotgun) J.Allen left tackle ran ob at BLT 33 for 14 yards (R.Smith).|
|BUF|rush10|12|1|D.Henry right end pushed ob at BUF 5 for 12 yards (T.Couch).|
|BAL|rush10|12|1|(Shotgun) J.Allen scrambles up the middle to BLT 43 for 12 yards (K.Wallace).|

**Our legs graded (pregame manifests + placed tickets)**

|Source|Leg|Status|Model p (MC+GR)|Actual|Result|Main cut reason|
|-|-|-|-|-|-|-|
|BAL@BUF|Lamar Jackson Pass Yds Under 237.5|CUT|0.656|0.0|HIT (cut leg would have hit)|P2 FAIL: starter by dropbacks last game: False; proj 31.8 pa; MC mean 212.2|
|BAL@BUF|Derrick Henry Rush Yds Under 78.5|CUT|0.5863|53.0|HIT (cut leg would have hit)|P14 FAIL: under on primary star (Ghost6 rule) - BAL RB1 (148 car); cut 2026-11-01 07:34 ET|
|BAL@BUF|Derrick Henry Rush+Rec Yds Under 89.5|CUT|0.598|60.0|HIT (cut leg would have hit)|P4 UNVERIFIED: RB receiving defender mapping: no LB/S alignment source; man 16.8% / zone 7|
|BAL@BUF|Zay Flowers Rec Yds Over 82.5|CUT|0.5878|0.0|MISS (good cut)|P5 FAIL: top-10 blitz D and player blitzed share drops >4 pts|
|BAL@BUF|Zay Flowers Receptions Over 6.5|CUT|0.5538|0.0|MISS (good cut)|P5 FAIL: top-10 blitz D and player blitzed share drops >4 pts|
|BAL@BUF|Rashod Bateman Rec Yds Over 23.5|CUT|0.5308|22.0|MISS (good cut)|P2 FAIL: not top-2 target earner (#4); not 4+ tgt in each of last 3|
|BAL@BUF|Rashod Bateman Receptions Under 2.5|CUT|0.5935|1.0|HIT (cut leg would have hit)|P14 FAIL: edge +1.5 < +3; shrunk edge -1.8 not > 0|
|BAL@BUF|Mark Andrews Rec Yds Over 27.5|CUT|0.5475|14.0|MISS (good cut)|P2 FAIL: not 4+ tgt in each of last 3|
|BAL@BUF|Mark Andrews Receptions Under 3.5|CUT|0.5887|3.0|HIT (cut leg would have hit)|P3 FAIL: under vs soft TE D (YPT>=8.0)|
|BAL@BUF|Josh Allen Pass Yds Under 247.5|CUT|0.6051|289.0|MISS (good cut)|P14 UNVERIFIED: MODEL-SUSPECT: MC median 227.7 vs FD main 247.5 / book consensus 247.8 (>=|
|BAL@BUF|DJ Moore Rec Yds Over 49.5|CUT|0.3014|82.0|HIT (cut leg would have hit)|P2 FAIL: not top-2 target earner (#10); not 4+ tgt in each of last 3; proj yds 39.7 < 49.5|
|BAL@BUF|DJ Moore Receptions Under 4.5|CUT|0.7737|4.0|HIT (cut leg would have hit)|P3 FAIL: under vs soft WR D (YPT>=9.0)|
|BAL@BUF|Khalil Shakir Rec Yds Under 41.5|CUT|0.5111|64.0|MISS (good cut)|P3 FAIL: under vs soft WR D (YPT>=9.0)|
|BAL@BUF|Khalil Shakir Receptions Under 3.5|CUT|0.4767|5.0|MISS (good cut)|P3 FAIL: under vs soft WR D (YPT>=9.0)|
|BAL@BUF|Keon Coleman Rec Yds Over 29.5|CUT|0.6586|4.0|MISS (good cut)|P2 FAIL: not 4+ tgt in each of last 3|
|BAL@BUF|Keon Coleman Receptions Over 2.5|CUT|0.609|1.0|MISS (good cut)|P2 FAIL: 5+ tgt in <3 of last 4|
|BAL@BUF|Dalton Kincaid Rec Yds Under 46.5|CUT|0.646|86.0|MISS (good cut)|P4 UNVERIFIED: TE defender mapping not ruled (ISS-05); man 15.9% / zone 78.6%, MOF closed |
|BAL@BUF|Dalton Kincaid Receptions Under 3.5|CUT|0.5569|4.0|MISS (good cut)|P4 UNVERIFIED: TE defender mapping not ruled (ISS-05); man 15.9% / zone 78.6%, MOF closed |
|DFS_SLIPS|[UD $20 8-pick] Zay Flowers Rec Yds Over 49.5|CUT||0.0|MISS|P5 FAIL: top-10 blitz D and player blitzed share drops >4 pts|
|DFS_SLIPS|[PP $25 6-pick Power] Zay Flowers Receptions Over 6.5|CUT||0.0|MISS|P5 FAIL: top-10 blitz D and player blitzed share drops >4 pts|
|DFS_SLIPS|[FD 7-leg +694] Zay Flowers Rec Yds Over 59.5|CUT||0.0|MISS|P5 FAIL: top-10 blitz D and player blitzed share drops >4 pts|
|DFS_SLIPS|[FD Ticket 2 SGP+ $63 +1508] Zay Flowers Receptions Over 4.5|CUT||0.0|MISS|P5 FAIL: top-10 blitz D and player blitzed share drops >4 pts|
|DFS_SLIPS|[FD $51.50 8-leg SGP] Zay Flowers Rec Yds Over 49.5|CUT||0.0|MISS|P5 FAIL: top-10 blitz D and player blitzed share drops >4 pts|

## CLE@PIT — CLE 6, PIT 27 (Final)

By quarter: PIT 7-13-7-0; CLE 0-6-0-0

**Scoring log**

|Q|Clock|Team|Type|Play|Score (away-home)|
|-|-|-|-|-|-|
|1|7:57|PIT|Rushing Touchdown|Rico Dowdle 9 Yd Rush (Chris Boswell Kick)|0-7|
|2|14:05|PIT|Field Goal Good|Chris Boswell 20 Yd Field Goal|0-10|
|2|8:43|CLE|Field Goal Good|Andre Szmyt 32 Yd Field Goal |3-10|
|2|3:27|PIT|Field Goal Good|Chris Boswell 37 Yd Field Goal|3-13|
|2|0:45|CLE|Field Goal Good|Andre Szmyt 49 Yd Field Goal|6-13|
|2|0:01|PIT|Rushing Touchdown|Pat Freiermuth 1 Yd Rush (Chris Boswell Kick)|6-20|
|3|9:39|PIT|Rushing Touchdown|Jaylen Warren 1 Yd Rush (Chris Boswell Kick)|6-27|

**QB lines** (box; QB hits = defensive box 'QB HTS' by the opponent)

|QB|Team|C/Att|Yds|Y/A|TD|INT|Sacks|Opp QB hits|Scrambles/rush|
|-|-|-|-|-|-|-|-|-|-|
|Deshaun Watson|CLE|27/39|324|8.3|0|0|8-41|13|3-2|
|Shedeur Sanders|CLE|2/2|2|1.0|0|0|0-0|13|0-0|
|Aaron Rodgers|PIT|13/25|172|6.9|0|1|1-11|2|0-0|

**Usage** (target share = player targets / team targets in box)

|Player|Team|Tgt|Tgt share|Rec|Rec yds|TD|Car|Carry share|Rush yds|Rush TD|
|-|-|-|-|-|-|-|-|-|-|-|
|Harold Fannin Jr.|CLE|12|30%|10|154|0|0|0%|0|0|
|Denzel Boston|CLE|11|28%|6|37|0|0|0%|0|0|
|Dylan Sampson|CLE|8|20%|6|62|0|1|7%|7|0|
|Quinshon Judkins|CLE|2|5%|2|24|0|11|73%|25|0|
|KC Concepcion|CLE|4|10%|3|37|0|0|0%|0|0|
|Jaylen Warren|PIT|2|9%|1|0|0|17|52%|143|1|
|DK Metcalf|PIT|6|27%|1|4|0|0|0%|0|0|
|Darnell Washington|PIT|5|23%|3|94|0|0|0%|0|0|
|Germie Bernard|PIT|5|23%|5|30|0|0|0%|0|0|
|Rico Dowdle|PIT|0|0%|0|0|0|15|45%|56|1|
|Pat Freiermuth|PIT|2|9%|2|35|0|1|3%|1|1|

**Explosives allowed** (20+ yd completions, 10+ yd runs; tacklers from play-by-play text, *not* coverage charting): CLE defense pass20 x3; CLE defense rush10 x1; CLE defense rush15 x4; PIT defense pass20 x4

|Def|Kind|Yds|Q|Play|
|-|-|-|-|-|
|CLE|pass20|58|3|(Shotgun) A.Rodgers pass short left to D.Washington pushed ob at CLV 1 for 58 yards (C.Schwesinger).|
|CLE|rush15|51|1|(Shotgun) J.Warren up the middle to CLV 25 for 51 yards (C.Schwesinger).|
|PIT|pass20|37|4|(Shotgun) D.Watson pass deep right to H.Fannin pushed ob at PIT 2 for 37 yards (J.Brisker; R.Spears-Jennings).|
|CLE|pass20|28|2|(Shotgun) A.Rodgers pass deep middle to P.Freiermuth to CLV 16 for 28 yards (R.Hickman).|
|PIT|pass20|27|4|(Shotgun) D.Watson pass short left to H.Fannin pushed ob at CLV 40 for 27 yards (J.Brisker).|
|PIT|pass20|25|2|D.Watson pass deep right to H.Fannin to PIT 19 for 25 yards (J.Ramsey; J.Dean).|
|CLE|pass20|24|2|(Shotgun) A.Rodgers pass short right to D.Washington pushed ob at CLV 37 for 24 yards (C.Schwesinger).|
|PIT|pass20|24|2|(Shotgun) D.Watson pass deep left to K.Concepcion to PIT 44 for 24 yards (D.Everette; R.Spears-Jennings) [T.Watt].|
|CLE|rush15|23|2|(Shotgun) J.Warren up the middle pushed ob at CLV 46 for 23 yards (G.Delpit).|
|CLE|rush15|15|1|(Shotgun) R.Dowdle up the middle to CLV 18 for 15 yards (R.Hickman).|
|CLE|rush15|15|1|S.Anderson reported in as eligible.  J.Warren right guard to PIT 27 for 15 yards (R.Hickman; E.McNeil-Warren).|
|CLE|rush10|13|3|J.Warren up the middle to PIT 32 for 13 yards (E.McNeil-Warren). FUMBLES (E.McNeil-Warren), RECOVERED by CLV-E.McNeil-Warren at PIT 32.The Replay Official reviewed the ru|

**Our legs graded (pregame manifests + placed tickets)**

|Source|Leg|Status|Model p (MC+GR)|Actual|Result|Main cut reason|
|-|-|-|-|-|-|-|
|CLE@PIT|Deshaun Watson Pass Yds Under 210.5|CUT|0.5197|324.0|MISS (good cut)|P14 FAIL: under on primary star (Ghost6 rule) - CLE starting QB; cut 2026-11-01 07:34 ET|
|CLE@PIT|Quinshon Judkins Rush Yds Over 47.5|CUT|0.5559|25.0|MISS (good cut)|P3 FAIL: RB YPC allowed <=3.8 suppression|
|CLE@PIT|Quinshon Judkins Rush+Rec Yds Over 61.5|CUT|0.6508|49.0|MISS (good cut)|P4 UNVERIFIED: RB receiving defender mapping: no LB/S alignment source; man 12.6% / zone 8|
|CLE@PIT|Jerry Jeudy Rec Yds Over 21.5|CUT|0.623|0.0|MISS (good cut)|P2 FAIL: not top-2 target earner (#4)|
|CLE@PIT|Jerry Jeudy Receptions Over 2.5|CUT|0.5303|0.0|MISS (good cut)|P2 FAIL: not top-2 target earner (#4); 5+ tgt in <3 of last 4|
|CLE@PIT|KC Concepcion Rec Yds Under 46.5|CUT|0.5863|37.0|HIT (cut leg would have hit)|P14 FAIL: under on primary star (Ghost6 rule) - CLE target leader (45 tgt); cut 2026-11-01|
|CLE@PIT|KC Concepcion Receptions Under 4.5|CUT|0.6313|3.0|HIT (cut leg would have hit)|P14 UNVERIFIED: MODEL-SUSPECT: edge +18.2 pts > +15 implausible vs market (FD 4.5, consens|
|CLE@PIT|Denzel Boston Rec Yds Under 47.5|CUT|0.6144|37.0|HIT (cut leg would have hit)|P14 FAIL: placed-ticket bar: UD20 Boston o29.5; MODEL-SUSPECT: MC median 36.2 vs FD main 4|
|CLE@PIT|Denzel Boston Receptions Under 3.5|CUT|0.6567|6.0|MISS (good cut)|P14 FAIL: conflicts with placed UD Boston o29.5 rec yds (Ghost6 vet) (2026-11-01 07:36 ET)|
|CLE@PIT|Harold Fannin Jr. Rec Yds Under 34.5|CUT|0.5524|154.0|MISS (good cut)|P4 UNVERIFIED: TE defender mapping not ruled (ISS-05); man 12.6% / zone 82.2%, MOF closed |
|CLE@PIT|Harold Fannin Jr. Receptions Under 3.5|CUT|0.558|10.0|MISS (good cut)|P4 UNVERIFIED: TE defender mapping not ruled (ISS-05); man 12.6% / zone 82.2%, MOF closed |
|CLE@PIT|Aaron Rodgers Pass Yds Under 218.5|CUT|0.4493|172.0|HIT (cut leg would have hit)|P14 FAIL: edge +1.5 < +3; model p 0.443 < .45; a model median does not clear the line|
|CLE@PIT|Jaylen Warren Rush Yds Over 64.5|CUT|0.5874|143.0|HIT (cut leg would have hit)|P14 FAIL: a model median does not clear the line|
|CLE@PIT|Jaylen Warren Rush+Rec Yds Over 91.5|CUT|0.5645|143.0|HIT (cut leg would have hit)|P4 UNVERIFIED: RB receiving defender mapping: no LB/S alignment source; man 42.4% / zone 5|
|CLE@PIT|DK Metcalf Rec Yds Under 52.5|CUT|0.5456|4.0|HIT (cut leg would have hit)|P4 FAIL: yds under vs YPT>10 defender|
|CLE@PIT|DK Metcalf Receptions Under 4.5|CUT|0.5648|1.0|HIT (cut leg would have hit)|P7 UNVERIFIED: offense snap% last2 [] (snap rows missing)|
|CLE@PIT|Germie Bernard Rec Yds Over 43.5|CUT|0.5515|30.0|MISS (good cut)|P6 FAIL: no-blitz D/F vs <25% blitz D|
|CLE@PIT|Germie Bernard Receptions Under 4.5|CUT|0.5148|5.0|MISS (good cut)|P14 FAIL: edge +0.9 < +3; shrunk edge -0.2 not > 0|
|CLE@PIT|Darnell Washington Rec Yds Under 20.5|CUT|0.645|94.0|MISS (good cut)|P4 UNVERIFIED: TE defender mapping not ruled (ISS-05); man 42.4% / zone 54.0%, MOF closed |
|CLE@PIT|Darnell Washington Receptions Under 2.5|CUT|0.6335|3.0|MISS (good cut)|P4 UNVERIFIED: TE defender mapping not ruled (ISS-05); man 42.4% / zone 54.0%, MOF closed |
|DFS_SLIPS|[UD $20 8-pick] Denzel Boston Rec Yds Over 29.5|CUT||37.0|HIT|P13 FAIL: 10G: underdog over BLOCKED (no written trap/elimination exception)|
|DFS_SLIPS|[PP $25 6-pick Power] Jaylen Warren Rush+Rec Yds Over 69.5|CUT||143.0|HIT|P4 UNVERIFIED: RB receiving defender mapping: no LB/S alignment source; man 42.4% / zone 5|

## IND@JAX — IND 7, JAX 42 (Final)

By quarter: JAX 7-21-14-0; IND 0-0-7-0

**Scoring log**

|Q|Clock|Team|Type|Play|Score (away-home)|
|-|-|-|-|-|-|
|1|5:30|JAX|Passing Touchdown|Brian Thomas Jr. 12 Yd pass from Trevor Lawrence (Cam Little Kick)|0-7|
|2|7:14|JAX|Passing Touchdown|Nate Boerkircher 31 Yd pass from Trevor Lawrence (Cam Little Kick)|0-14|
|2|1:51|JAX|Rushing Touchdown|Bhayshul Tuten 39 Yd Rush (Cam Little Kick)|0-21|
|2|0:10|JAX|Interception Return Touchdown|Rayuan Lane III 92 Yd Interception Return (Cam Little Kick)|0-28|
|3|9:08|JAX|Rushing Touchdown|Chris Rodriguez Jr. 28 Yd Rush (Cam Little Kick)|0-35|
|3|3:59|IND|Passing Touchdown|Josh Downs 6 Yd pass from Daniel Jones (Spencer Shrader Kick)|7-35|
|3|0:00|JAX|Passing Touchdown|Bhayshul Tuten 25 Yd pass from Trevor Lawrence (Cam Little Kick)|7-42|

**QB lines** (box; QB hits = defensive box 'QB HTS' by the opponent)

|QB|Team|C/Att|Yds|Y/A|TD|INT|Sacks|Opp QB hits|Scrambles/rush|
|-|-|-|-|-|-|-|-|-|-|
|Daniel Jones|IND|19/28|144|5.1|1|2|3-8|11|4-7|
|Anthony Richardson Sr.|IND|2/2|8|4.0|0|0|1-10|11|2-4|
|Trevor Lawrence|JAX|10/14|210|15.0|3|0|3-35|4|3-10|
|Quinn Ewers|JAX|1/3|8|2.7|0|0|0-0|4|0-0|

**Usage** (target share = player targets / team targets in box)

|Player|Team|Tgt|Tgt share|Rec|Rec yds|TD|Car|Carry share|Rush yds|Rush TD|
|-|-|-|-|-|-|-|-|-|-|-|
|Tyler Warren|IND|10|33%|4|18|0|0|0%|0|0|
|Jonathan Taylor|IND|5|17%|4|24|0|8|31%|23|0|
|Keenan Allen|IND|7|23%|7|67|0|0|0%|0|0|
|Josh Downs|IND|5|17%|4|23|1|0|0%|0|0|
|DJ Giddens|IND|0|0%|0|0|0|6|23%|43|0|
|Laquon Treadwell|IND|2|7%|1|18|0|0|0%|0|0|
|Seth McGowan|IND|0|0%|0|0|0|5|19%|29|0|
|Bhayshul Tuten|JAX|2|12%|2|55|1|16|48%|104|1|
|Chris Rodriguez Jr.|JAX|1|6%|1|17|0|6|18%|41|1|
|Jakobi Meyers|JAX|3|18%|2|24|0|0|0%|0|0|
|Parker Washington|JAX|2|12%|1|16|0|1|3%|10|0|
|Ameer Abdullah|JAX|0|0%|0|0|0|6|18%|13|0|
|Brenton Strange|JAX|2|12%|2|55|0|0|0%|0|0|
|Brian Thomas Jr.|JAX|2|12%|1|12|1|0|0%|0|0|

**Explosives allowed** (20+ yd completions, 10+ yd runs; tacklers from play-by-play text, *not* coverage charting): IND defense pass20 x4; IND defense rush10 x1; IND defense rush15 x2; JAX defense rush10 x2; JAX defense rush15 x2

|Def|Kind|Yds|Q|Play|
|-|-|-|-|-|
|IND|pass20|46|1|W.Milum reported in as eligible.  T.Lawrence pass deep right to B.Strange pushed ob at IND 32 for 46 yards (A.Haulcy).|
|IND|rush15|39|2|B.Tuten right tackle for 39 yards, TOUCHDOWN. C.Little extra point is GOOD, Center-R.Matiscik, Holder-L.Cooke.|
|IND|pass20|31|2|T.Lawrence pass deep left to N.Boerkircher for 31 yards, TOUCHDOWN. C.Little extra point is GOOD, Center-R.Matiscik, Holder-L.Cooke.|
|IND|pass20|30|3|T.Lawrence pass short left to B.Tuten to JAX 47 for 30 yards (C.Curry).|
|IND|rush15|28|3|(Shotgun) C.Rodriguez up the middle for 28 yards, TOUCHDOWN. C.Little extra point is GOOD, Center-R.Matiscik, Holder-L.Cooke.|
|IND|pass20|25|3|(Shotgun) T.Lawrence pass short right to B.Tuten for 25 yards, TOUCHDOWN. C.Little extra point is GOOD, Center-R.Matiscik, Holder-L.Cooke.|
|JAX|rush15|19|1|(Shotgun) J.Taylor right end pushed ob at JAX 48 for 19 yards (M.Brown).|
|JAX|rush15|16|3|(Shotgun) S.McGowan up the middle to JAX 3 for 16 yards (K.Merriweather; R.Lane).|
|JAX|rush10|12|4|D.Giddens right end ran ob at IND 15 for 12 yards (J.Mcleod).|
|JAX|rush10|12|4|D.Giddens left tackle to IND 18 for 12 yards (R.Lane; J.Huskey).|
|IND|rush10|10|1|P.Washington right end to JAX 17 for 10 yards (C.Allen; J.Tuimoloau).|

**Our legs graded (pregame manifests + placed tickets)**

|Source|Leg|Status|Model p (MC+GR)|Actual|Result|Main cut reason|
|-|-|-|-|-|-|-|
|IND@JAX|Daniel Jones Pass Yds Over 192.5|CUT|0.6662|144.0|MISS (good cut)|P6 FAIL: clutch D/F: no trailing-script overs|
|IND@JAX|Jonathan Taylor Rush Yds Over 50.5|CUT|0.6446|23.0|MISS (good cut)|P3 FAIL: RB YPC allowed <=3.8 suppression|
|IND@JAX|Jonathan Taylor Rush+Rec Yds Over 70.5|CUT|0.6158|47.0|MISS (good cut)|P4 UNVERIFIED: RB receiving defender mapping: no LB/S alignment source; man 21.0% / zone 7|
|IND@JAX|Josh Downs Rec Yds Over 32.5|CUT|0.6156|23.0|MISS (good cut)|P6 FAIL: clutch D/F: no trailing-script overs|
|IND@JAX|Josh Downs Receptions Over 3.5|CUT|0.4708|4.0|HIT (cut leg would have hit)|P2 FAIL: 5+ tgt in <3 of last 4; proj rec 3.4 < 3.5|
|IND@JAX|Keenan Allen Rec Yds Over 35.5|CUT|0.7382|67.0|HIT (cut leg would have hit)|P2 FAIL: not 4+ tgt in each of last 3|
|IND@JAX|Keenan Allen Receptions Over 4.5|CUT|0.543|7.0|HIT (cut leg would have hit)|P4 FAIL: rec over vs 54.8% cmp allowed, volume margin +14% < 20%|
|IND@JAX|Tyler Warren Rec Yds Over 39.5|CUT|0.5514|18.0|MISS (good cut)|P2 FAIL: not top-2 target earner (#5)|
|IND@JAX|Tyler Warren Receptions Over 4.5|CUT|0.6772|4.0|MISS (good cut)|P2 FAIL: not top-2 target earner (#5)|
|IND@JAX|Trevor Lawrence Pass Yds Under 237.5|CUT|0.4597|210.0|HIT (cut leg would have hit)|P14 FAIL: edge +2.5 < +3; a model median does not clear the line|
|IND@JAX|Bhayshul Tuten Rush Yds Over 59.5|CUT|0.7041|104.0|HIT (cut leg would have hit)|P7 FAIL: rush over needs 60%+ carry share in 3 of last 4|
|IND@JAX|Bhayshul Tuten Rush+Rec Yds Over 83.5|CUT|0.6345|159.0|HIT (cut leg would have hit)|P4 UNVERIFIED: RB receiving defender mapping: no LB/S alignment source; man 26.2% / zone 6|
|IND@JAX|Parker Washington Rec Yds Over 59.5|CUT|0.4705|16.0|MISS (good cut)|P2 FAIL: not 4+ tgt in each of last 3|
|IND@JAX|Parker Washington Receptions Under 4.5|CUT|0.5944|1.0|HIT (cut leg would have hit)|P4 UNVERIFIED: defender sample 2 tgt < 8: too thin to grade|
|IND@JAX|Brenton Strange Rec Yds Under 41.5|CUT|0.4729|55.0|MISS (good cut)|P4 UNVERIFIED: TE defender mapping not ruled (ISS-05); man 26.2% / zone 66.5%, MOF closed |
|IND@JAX|Brenton Strange Receptions Over 2.5|CUT|0.8032|2.0|MISS (good cut)|P4 UNVERIFIED: TE defender mapping not ruled (ISS-05); man 26.2% / zone 66.5%, MOF closed |
|DFS_SLIPS|[FD 7-leg +694] Parker Washington Rec Yds Over 39.5|CUT||16.0|MISS|P2 FAIL: not 4+ tgt in each of last 3|

## LV@NYJ — LV 38, NYJ 33 (Final)

By quarter: NYJ 6-17-7-3; LV 7-7-14-10

**Scoring log**

|Q|Clock|Team|Type|Play|Score (away-home)|
|-|-|-|-|-|-|
|1|12:50|NYJ|Field Goal Good|Jason Sanders 21 Yd Field Goal|0-3|
|1|7:23|LV|Passing Touchdown|Brock Bowers 12 Yd pass from Kirk Cousins (Matt Gay Kick)|7-3|
|1|2:13|NYJ|Field Goal Good|Jason Sanders 36 Yd Field Goal|7-6|
|2|10:56|NYJ|Passing Touchdown|Isaiah Williams 18 Yd pass from Geno Smith (Jason Sanders Kick)|7-13|
|2|10:44|LV|Kickoff Return Touchdown|Dylan Laube 95 Yd Kickoff Return (Matt Gay Kick)|14-13|
|2|6:18|NYJ|Passing Touchdown|Adonai Mitchell 12 Yd pass from Geno Smith (Jason Sanders Kick)|14-20|
|2|0:09|NYJ|Field Goal Good|Jason Sanders 39 Yd Field Goal|14-23|
|3|9:59|LV|Passing Touchdown|Brock Bowers 2 Yd pass from Kirk Cousins (Matt Gay Kick)|21-23|
|3|8:20|NYJ|Rushing Touchdown|Braelon Allen 21 Yd Rush (Jason Sanders Kick)|21-30|
|3|4:14|LV|Rushing Touchdown|Kirk Cousins 1 Yd Rush (Matt Gay Kick)|28-30|
|4|11:33|LV|Passing Touchdown|Jalen Nailor 2 Yd pass from Kirk Cousins (Matt Gay Kick)|35-30|
|4|4:31|NYJ|Field Goal Good|Jason Sanders 31 Yd Field Goal|35-33|
|4|0:27|LV|Field Goal Good|Matt Gay 53 Yd Field Goal|38-33|

**QB lines** (box; QB hits = defensive box 'QB HTS' by the opponent)

|QB|Team|C/Att|Yds|Y/A|TD|INT|Sacks|Opp QB hits|Scrambles/rush|
|-|-|-|-|-|-|-|-|-|-|
|Kirk Cousins|LV|19/26|247|9.5|3|0|1-9|6|5-3|
|Geno Smith|NYJ|20/32|290|9.1|2|1|2-17|3|1-4|

**Usage** (target share = player targets / team targets in box)

|Player|Team|Tgt|Tgt share|Rec|Rec yds|TD|Car|Carry share|Rush yds|Rush TD|
|-|-|-|-|-|-|-|-|-|-|-|
|Brock Bowers|LV|10|40%|7|92|2|0|0%|0|0|
|Mike Washington Jr.|LV|0|0%|0|0|0|25|76%|83|0|
|Michael Mayer|LV|6|24%|5|53|0|0|0%|0|0|
|Ashton Jeanty|LV|4|16%|3|64|0|2|6%|9|0|
|Jalen Nailor|LV|4|16%|4|38|1|0|0%|0|0|
|Garrett Wilson|NYJ|12|39%|6|83|0|0|0%|0|0|
|Adonai Mitchell|NYJ|9|29%|7|142|1|0|0%|0|0|
|Braelon Allen|NYJ|2|6%|2|6|0|21|78%|147|1|
|Mason Taylor|NYJ|5|16%|3|19|0|0|0%|0|0|
|Kenyon Sadiq|NYJ|2|6%|1|22|0|0|0%|0|0|
|Isaiah Davis|NYJ|0|0%|0|0|0|5|19%|15|0|

**Explosives allowed** (20+ yd completions, 10+ yd runs; tacklers from play-by-play text, *not* coverage charting): LV defense pass20 x5; LV defense rush10 x1; LV defense rush15 x4; NYJ defense pass20 x3; NYJ defense rush15 x1

|Def|Kind|Yds|Q|Play|
|-|-|-|-|-|
|LV|pass20|47|4|(Shotgun) G.Smith pass deep left to A.Mitchell to LV 13 for 47 yards (T.Stukes).|
|NYJ|pass20|45|4|(Shotgun) K.Cousins pass short left to A.Jeanty to NYJ 13 for 45 yards (J.Sherwood; M.Fitzpatrick).|
|LV|pass20|31|1|G.Smith pass deep left to G.Wilson to LV 34 for 31 yards (T.Stukes). LV-D.Porter was injured during the play.|
|NYJ|pass20|27|3|K.Cousins pass deep middle to B.Bowers to NYJ 38 for 27 yards (D.Belton).|
|LV|rush15|24|2|(Shotgun) B.Allen up the middle to LV 21 for 24 yards (T.Johnson; E.Stokes).|
|NYJ|pass20|23|1|(Shotgun) K.Cousins pass short middle to B.Bowers to NYJ 7 for 23 yards (D.Belton; M.Fitzpatrick).|
|LV|pass20|22|2|G.Smith pass deep left to A.Mitchell pushed ob at LV 18 for 22 yards (J.McCoy).|
|LV|pass20|22|3|G.Smith pass deep left to K.Sadiq to LV 21 for 22 yards (T.Eichenberg).|
|LV|rush15|21|3|(Shotgun) B.Allen left end for 21 yards, TOUCHDOWN. J.Sanders extra point is GOOD, Center-T.Hennessy, Holder-A.McNamara.|
|LV|pass20|20|2|(Shotgun) G.Smith pass deep right to A.Mitchell to NYJ 49 for 20 yards (E.Stokes).|
|LV|rush15|15|1|B.Allen right end pushed ob at LV 19 for 15 yards (Q.Walker; T.Stukes).|
|LV|rush15|15|1|(Shotgun) B.Allen left guard to LV 4 for 15 yards (T.Stukes; J.Chinn).PENALTY on LV-A.Butler, Defensive Holding, 2 yards, enforced at LV 4.|
|NYJ|rush15|15|3|M.Washington left end pushed ob at NYJ 19 for 15 yards (J.Sherwood).|
|LV|rush10|11|2|B.Allen right guard to LV 28 for 11 yards (J.Chinn; T.Stukes).|

**Our legs graded (pregame manifests + placed tickets)**

|Source|Leg|Status|Model p (MC+GR)|Actual|Result|Main cut reason|
|-|-|-|-|-|-|-|
|LV@NYJ|Kirk Cousins Pass Yds Over 232.5|CUT|0.5891|247.0|HIT (cut leg would have hit)|P14 FAIL: edge +2.4 < +3; model p 0.395 < .45; a model median does not clear the line; MOD|
|LV@NYJ|Brock Bowers Rec Yds Over 68.5|CUT|0.5413|92.0|HIT (cut leg would have hit)|P4 UNVERIFIED: TE defender mapping not ruled (ISS-05); man 23.8% / zone 66.6%, MOF closed |
|LV@NYJ|Brock Bowers Receptions Under 5.5|CUT|0.415|7.0|MISS (good cut)|P4 UNVERIFIED: TE defender mapping not ruled (ISS-05); man 23.8% / zone 66.6%, MOF closed |
|LV@NYJ|Tre Tucker Rec Yds Over 48.5|CUT|0.5863|0.0|MISS (good cut)|P14 FAIL: a model median does not clear the line|
|LV@NYJ|Tre Tucker Receptions Over 3.5|PASS|0.614|0.0|MISS||
|LV@NYJ|Geno Smith Pass Yds Under 225.5|CUT|0.4851|290.0|MISS (good cut)|P14 FAIL: a model median does not clear the line|
|LV@NYJ|Garrett Wilson Rec Yds Under 63.5|CUT|0.5466|83.0|MISS (good cut)|P14 FAIL: under on primary star (Ghost6 rule) - NYJ target leader (52 tgt); cut 2026-11-01|
|LV@NYJ|Garrett Wilson Receptions Under 5.5|CUT|0.6445|6.0|MISS (good cut)|P14 FAIL: under on primary star (Ghost6 rule) - NYJ target leader (52 tgt); cut 2026-11-01|
|BONUS_SLIP|Tre Tucker Receptions Over 3.5|PASS|0.614|0.0|MISS||
|DFS_SLIPS|[PP $40 6-pick Power] Brock Bowers Rec Targets 8.5|CUT||10.0|HIT|P14 MISSING: no sim model: no sim model for targets market; leg left ungraded (not invente|
|DFS_SLIPS|[UD $20 8-pick] Brock Bowers Rec Yds Over 49.5|CUT||92.0|HIT|P4 UNVERIFIED: TE defender mapping not ruled (ISS-05); man 23.8% / zone 66.6%, MOF closed |
|DFS_SLIPS|[FD 7-leg +694] Brock Bowers Rec Yds Over 49.5|CUT||92.0|HIT|P4 UNVERIFIED: TE defender mapping not ruled (ISS-05); man 23.8% / zone 66.6%, MOF closed |
|FD7_REPLACEMENTS|Tre Tucker Receptions Over 3.5|PASS|0.614|0.0|MISS||

## MIN@DET — MIN 15, DET 19 (Final)

By quarter: DET 3-3-6-7; MIN 0-7-0-8

**Scoring log**

|Q|Clock|Team|Type|Play|Score (away-home)|
|-|-|-|-|-|-|
|1|2:18|DET|Field Goal Good|Jake Bates 25 Yd Field Goal|0-3|
|2|14:25|MIN|Passing Touchdown|Justin Jefferson 1 Yd pass from Kyler Murray (Will Reichard Kick)|7-3|
|2|0:02|DET|Field Goal Good|Jake Bates 37 Yd Field Goal|7-6|
|3|4:40|DET|Rushing Touchdown|Jahmyr Gibbs 30 Yd Rush (Two-Point Run Conversion Failed)|7-12|
|4|8:44|MIN|Passing Touchdown|T.J. Hockenson 8 Yd pass from Kyler Murray (Kyler Murray Pass to Jordan Addison for Two-Point Conversion)|15-12|
|4|4:35|DET|Passing Touchdown|Jameson Williams 7 Yd pass from Jared Goff (Jake Bates Kick)|15-19|

**QB lines** (box; QB hits = defensive box 'QB HTS' by the opponent)

|QB|Team|C/Att|Yds|Y/A|TD|INT|Sacks|Opp QB hits|Scrambles/rush|
|-|-|-|-|-|-|-|-|-|-|
|Kyler Murray|MIN|17/29|210|7.2|2|1|3-25|6|4-35|
|Jared Goff|DET|18/25|176|7.0|1|1|4-22|9|3-0|

**Usage** (target share = player targets / team targets in box)

|Player|Team|Tgt|Tgt share|Rec|Rec yds|TD|Car|Carry share|Rush yds|Rush TD|
|-|-|-|-|-|-|-|-|-|-|-|
|Jahmyr Gibbs|DET|4|16%|2|15|0|23|59%|153|1|
|Amon-Ra St. Brown|DET|8|32%|7|46|0|1|3%|10|0|
|Jameson Williams|DET|6|24%|4|70|1|0|0%|0|0|
|Sam LaPorta|DET|5|20%|3|33|0|1|3%|2|0|
|Sione Vaki|DET|1|4%|1|5|0|11|28%|65|0|
|Justin Jefferson|MIN|9|32%|5|33|1|0|0%|0|0|
|Jordan Addison|MIN|8|29%|3|66|0|0|0%|0|0|
|T.J. Hockenson|MIN|5|18%|4|58|1|0|0%|0|0|
|Aaron Jones Sr.|MIN|2|7%|2|18|0|5|28%|22|0|
|Jordan Mason|MIN|0|0%|0|0|0|8|44%|20|0|
|Ben Yurosek|MIN|2|7%|1|24|0|0|0%|0|0|
|Jauan Jennings|MIN|2|7%|2|11|0|0|0%|0|0|

**Explosives allowed** (20+ yd completions, 10+ yd runs; tacklers from play-by-play text, *not* coverage charting): DET defense pass20 x3; DET defense rush10 x2; DET defense rush15 x1; MIN defense rush10 x7; MIN defense rush15 x3

|Def|Kind|Yds|Q|Play|
|-|-|-|-|-|
|DET|pass20|51|4|K.Murray pass deep middle to J.Addison to DET 10 for 51 yards (K.Dorsey).|
|MIN|rush15|30|3|J.Gibbs up the middle for 30 yards, TOUCHDOWN. TWO-POINT CONVERSION ATTEMPT. J.Gibbs rushes right end. ATTEMPT FAILS.|
|DET|pass20|24|1|K.Murray pass short right to B.Yurosek to DET 41 for 24 yards (R.McCreary; B.Branch).|
|DET|pass20|22|1|(Shotgun) K.Murray pass deep right to T.Hockenson to DET 16 for 22 yards (B.Branch).  The player down by contact was assisted by replay.|
|DET|rush15|22|2|(Shotgun) K.Murray scrambles up the middle ran ob at MIN 47 for 22 yards (R.Ya-Sin).|
|MIN|rush15|19|2|(Shotgun) J.Gibbs up the middle to MIN 19 for 19 yards (B.Murphy).|
|MIN|rush15|17|4|J.Gibbs right tackle ran ob at DET 48 for 17 yards (J.Metellus).|
|MIN|rush10|14|4|J.Gibbs left tackle to DET 31 for 14 yards (B.Murphy).|
|MIN|rush10|12|1|J.Gibbs left tackle to MIN 12 for 12 yards (B.Murphy; H.Smith).|
|MIN|rush10|12|4|S.Vaki left tackle to MIN 35 for 12 yards (H.Smith).|
|MIN|rush10|11|3|J.Gibbs up the middle to MIN 42 for 11 yards (J.Metellus; I.Rodgers).|
|DET|rush10|11|3|J.Mason left end pushed ob at DET 30 for 11 yards (T.Nowaske).|
|DET|rush10|10|1|(Shotgun) J.Mason up the middle to MIN 20 for 10 yards (B.Branch).|
|MIN|rush10|10|2|S.Vaki right tackle to DET 14 for 10 yards (J.Metellus; T.Jackson).|
|MIN|rush10|10|3|(Shotgun) A.St. Brown right end to MIN 30 for 10 yards (H.Smith; K.Van Noy).|
|MIN|rush10|10|4|(No Huddle) S.Vaki left tackle to MIN 25 for 10 yards (B.Cashman).|

**Our legs graded (pregame manifests + placed tickets)**

|Source|Leg|Status|Model p (MC+GR)|Actual|Result|Main cut reason|
|-|-|-|-|-|-|-|
|MIN@DET|Kyler Murray Pass Yds Under 224.5|CUT|0.6819|210.0|HIT (cut leg would have hit)|P3 FAIL: under vs top-8 pass yds allowed (rank 1)|
|MIN@DET|Jordan Mason Rush Yds Over 49.5|CUT|0.645|20.0|MISS (good cut)|P1 FAIL: 2 games; last3 09-13 0t/0r/0y/15c/59ry, 10-25 2t/0r/0y/15c/68ry|
|MIN@DET|Justin Jefferson Rec Yds Under 75.5|CUT|0.7316|33.0|HIT (cut leg would have hit)|P4 MISSING: defender not in PFR cache|
|MIN@DET|Justin Jefferson Receptions Under 5.5|CUT|0.7008|5.0|HIT (cut leg would have hit)|P4 MISSING: defender not in PFR cache|
|MIN@DET|Jordan Addison Rec Yds Over 37.5|CUT|0.4346|66.0|HIT (cut leg would have hit)|P2 FAIL: not top-2 target earner (#4); not 4+ tgt in each of last 3|
|MIN@DET|Jordan Addison Receptions Under 3.5|CUT|0.6688|3.0|HIT (cut leg would have hit)|fails §7 (under hit 1 of 3 with current QB); pending Ghost6 confirmation|
|MIN@DET|T.J. Hockenson Rec Yds Under 40.5|CUT|0.509|58.0|MISS (good cut)|P3 FAIL: under vs soft TE D (YPT>=8.0)|
|MIN@DET|T.J. Hockenson Receptions Under 4.5|CUT|0.5341|4.0|HIT (cut leg would have hit)|P3 FAIL: under vs soft TE D (YPT>=8.0)|
|MIN@DET|Jared Goff Pass Yds Under 259.5|CUT|0.4765|176.0|HIT (cut leg would have hit)|P14 FAIL: a model median does not clear the line|
|MIN@DET|Jahmyr Gibbs Rush Yds Over 87.5|CUT|0.58|153.0|HIT (cut leg would have hit)|P14 FAIL: a model median does not clear the line|
|MIN@DET|Jahmyr Gibbs Rush+Rec Yds Over 121.5|CUT|0.5738|168.0|HIT (cut leg would have hit)|P4 UNVERIFIED: RB receiving defender mapping: no LB/S alignment source; man 5.3% / zone 86|
|MIN@DET|Amon-Ra St. Brown Rec Yds Under 77.5|CUT|0.4672|46.0|HIT (cut leg would have hit)|P10 UNVERIFIED: no cited caption play re-matched a fresh pbp row for this player|
|MIN@DET|Amon-Ra St. Brown Receptions Under 6.5|CUT|0.427|7.0|MISS (good cut)|P10 UNVERIFIED: no cited caption play re-matched a fresh pbp row for this player|
|MIN@DET|Jameson Williams Rec Yds Under 51.5|CUT|0.541|70.0|MISS (good cut)|P14 FAIL: rejected by Ghost6 vet (primary WR under; MC+GR edge thin +4.1/+2.9) (2026-11-01|
|MIN@DET|Jameson Williams Receptions Over 3.5|CUT|0.508|4.0|HIT (cut leg would have hit)|P2 FAIL: 5+ tgt in <3 of last 4; same-role teammate >=28%: [('Amon-Ra St. Brown', 0.304932|
|MIN@DET|Sam LaPorta Rec Yds Under 45.5|CUT|0.5567|33.0|HIT (cut leg would have hit)|P4 UNVERIFIED: TE defender mapping not ruled (ISS-05); man 5.3% / zone 86.5%, MOF closed 3|
|MIN@DET|Sam LaPorta Receptions Under 4.5|CUT|0.6562|3.0|HIT (cut leg would have hit)|P4 UNVERIFIED: TE defender mapping not ruled (ISS-05); man 5.3% / zone 86.5%, MOF closed 3|
|BONUS_SLIP|Jahmyr Gibbs Rush Yds Over 79.5 (alt)|PASS|0.58|153.0|HIT|P14 FAIL: a model median does not clear the line|
|DFS_SLIPS|[PP $40 6-pick Power] Amon-Ra St. Brown Receptions Over 5.5|CUT||7.0|HIT|P10 UNVERIFIED: no cited caption play re-matched a fresh pbp row for this player|
|DFS_SLIPS|[UD $20 8-pick] Amon-Ra St. Brown Rec Yds Over 49.5|CUT||46.0|MISS|P10 UNVERIFIED: no cited caption play re-matched a fresh pbp row for this player|
|DFS_SLIPS|[PP $25 6-pick Power] Amon-Ra St. Brown Receptions Over 7.5|CUT||7.0|MISS|P2 FAIL: proj rec 7.0 < 7.5|
|DFS_SLIPS|[FD Ticket 2 SGP+ $63 +1508] Jahmyr Gibbs Receptions Over 4.5|CUT||2.0|MISS|P14 FAIL: model p 0.436 < .45; a model median does not clear the line|
|DFS_SLIPS|[FD Ticket 2 SGP+ $63 +1508] Amon-Ra St. Brown Rec Yds Over 59.5|CUT||46.0|MISS|P10 UNVERIFIED: no cited caption play re-matched a fresh pbp row for this player|
|FD7_REPLACEMENTS|Jordan Addison Receptions Under 3.5|CUT|0.6688|3.0|HIT (cut leg would have hit)|fails §7 (under hit 1 of 3 with current QB); pending Ghost6 confirmation|

## TEN@CIN — TEN 36, CIN 36 (In Progress)

By quarter: CIN 0-14-9-13; TEN 13-0-8-15

**Scoring log**

|Q|Clock|Team|Type|Play|Score (away-home)|
|-|-|-|-|-|-|
|1|10:52|TEN|Field Goal Good|Joey Slye 46 Yd Field Goal|3-0|
|1|7:55|TEN|Rushing Touchdown|Tony Pollard 40 Yd Rush (Joey Slye Kick)|10-0|
|1|2:14|TEN|Field Goal Good|Joey Slye 29 Yd Field Goal|13-0|
|2|13:20|CIN|Passing Touchdown|Ja'Marr Chase 30 Yd pass from Joe Burrow (Evan McPherson Kick)|13-7|
|2|0:20|CIN|Passing Touchdown|Jack Endries 1 Yd pass from Joe Burrow (Evan McPherson Kick)|13-14|
|3|12:25|CIN|Passing Touchdown|Tee Higgins 17 Yd pass from Joe Burrow (Evan McPherson Kick)|13-21|
|3|7:47|TEN|Rushing Touchdown|Tony Pollard 1 Yd Rush (Cam Ward Run for Two-Point Conversion)|21-21|
|3|0:46|CIN|Safety|Tony Pollard Rush, Loss of 3 for Safety|21-23|
|4|11:29|TEN|Passing Touchdown|Chimere Dike 11 Yd pass from Cam Ward (Joey Slye Kick)|28-23|
|4|7:13|CIN|Passing Touchdown|Mike Gesicki 25 Yd pass from Joe Burrow (Two-Point Pass Conversion Failed)|28-29|
|4|3:46|TEN|Passing Touchdown|Wan'Dale Robinson 15 Yd pass from Cam Ward (Cam Ward Pass to Gunnar Helm for Two-Point Conversion)|36-29|
|4|1:17|CIN|Passing Touchdown|Tee Higgins 18 Yd pass from Joe Burrow (Evan McPherson Kick)|36-36|

**QB lines** (box; QB hits = defensive box 'QB HTS' by the opponent)

|QB|Team|C/Att|Yds|Y/A|TD|INT|Sacks|Opp QB hits|Scrambles/rush|
|-|-|-|-|-|-|-|-|-|-|
|Cam Ward|TEN|24/35|285|8.1|2|0|1-9|5|5-33|
|Joe Burrow|CIN|34/43|401|9.3|5|3|3-27|9|2-1|

**Usage** (target share = player targets / team targets in box)

|Player|Team|Tgt|Tgt share|Rec|Rec yds|TD|Car|Carry share|Rush yds|Rush TD|
|-|-|-|-|-|-|-|-|-|-|-|
|Ja'Marr Chase|CIN|13|31%|9|110|1|0|0%|0|0|
|Chase Brown|CIN|9|21%|8|46|0|11|65%|47|0|
|Tee Higgins|CIN|10|24%|9|134|2|0|0%|0|0|
|Mike Gesicki|CIN|6|14%|4|76|1|0|0%|0|0|
|Dohnte Meyers|CIN|3|7%|3|34|0|0|0%|0|0|
|Samaje Perine|CIN|0|0%|0|0|0|4|24%|10|0|
|Tony Pollard|TEN|5|14%|3|20|0|21|81%|117|2|
|Gunnar Helm|TEN|8|23%|5|76|0|0|0%|0|0|
|Wan'Dale Robinson|TEN|7|20%|6|57|1|0|0%|0|0|
|Chimere Dike|TEN|5|14%|4|65|1|0|0%|0|0|
|Daniel Bellinger|TEN|4|11%|3|36|0|0|0%|0|0|
|Calvin Ridley|TEN|3|9%|1|10|0|0|0%|0|0|
|Elic Ayomanor|TEN|3|9%|2|21|0|0|0%|0|0|

**Explosives allowed** (20+ yd completions, 10+ yd runs; tacklers from play-by-play text, *not* coverage charting): CIN defense pass20 x5; CIN defense rush10 x1; CIN defense rush15 x2; TEN defense pass20 x5; TEN defense rush10 x1

|Def|Kind|Yds|Q|Play|
|-|-|-|-|-|
|CIN|rush15|40|1|(No Huddle, Shotgun) T.Pollard right tackle for 40 yards, TOUCHDOWN. CIN-D.Knight was injured during the play. J.Slye extra point is GOOD, Center-M.Cox, Holder-T.Morstead|
|TEN|pass20|32|2|(Shotgun) J.Burrow pass deep middle to T.Higgins to TEN 26 for 32 yards (M.Harris).|
|TEN|pass20|30|2|(Shotgun) J.Burrow pass deep middle to J.Chase for 30 yards, TOUCHDOWN. E.McPherson extra point is GOOD, Center-W.Wagner, Holder-R.Rehkow.|
|TEN|pass20|28|2|(Shotgun) J.Burrow pass short middle to M.Gesicki to TEN 39 for 28 yards (A.Hill).|
|CIN|pass20|28|3|(No Huddle, Shotgun) C.Ward pass short right to C.Dike to CIN 21 for 28 yards (D.Hill).|
|TEN|pass20|25|4|(Shotgun) J.Burrow pass deep left to M.Gesicki for 25 yards, TOUCHDOWN. TWO-POINT CONVERSION ATTEMPT. J.Burrow pass to T.Higgins is incomplete. ATTEMPT FAILS.|
|CIN|pass20|25|4|(No Huddle) C.Ward pass short right to G.Helm to CIN 15 for 25 yards (J.Newton).|
|CIN|pass20|24|2|(No Huddle) C.Ward pass short left to G.Helm to CIN 48 for 24 yards (B.Cook) [M.Murphy].|
|CIN|pass20|23|1|(No Huddle, Shotgun) C.Ward pass short middle to E.Ayomanor to CIN 41 for 23 yards (J.Battle; B.Cook).|
|TEN|pass20|23|4|(Shotgun) J.Burrow pass deep right to J.Chase to TEN 25 for 23 yards (T.Adams) [J.Martin].|
|CIN|rush15|22|4|(Shotgun) T.Pollard left end to CIN 11 for 22 yards (M.Murphy). CIN-D.Turner was injured during the play.|
|CIN|pass20|21|2|(No Huddle, Shotgun) C.Ward pass deep middle to C.Dike to CIN 27 for 21 yards (J.Battle).|
|TEN|rush10|14|1|(Shotgun) C.Brown left guard to TEN 32 for 14 yards (K.Winston; A.Hooker).|
|CIN|rush10|14|3|(No Huddle, Shotgun) C.Ward left end pushed ob at TEN 43 for 14 yards (D.Hill).|

**Our legs graded (pregame manifests + placed tickets)**

|Source|Leg|Status|Model p (MC+GR)|Actual|Result|Main cut reason|
|-|-|-|-|-|-|-|
|TEN@CIN|Cam Ward Pass Yds Under 192.5|CUT|0.5536|285.0|MISS (good cut)|P3 FAIL: under vs top-8 pass yds allowed (rank 7)|
|TEN@CIN|Tony Pollard Rush Yds Over 65.5|CUT|0.6397|117.0|HIT (cut leg would have hit)|P6 FAIL: clutch D/F: no trailing-script overs|
|TEN@CIN|Tony Pollard Rush+Rec Yds Under 84.5|CUT|0.476|137.0|MISS (good cut)|P4 UNVERIFIED: RB receiving defender mapping: no LB/S alignment source; man 26.6% / zone 6|
|TEN@CIN|Joe Burrow Pass Yds Over 249.5|CUT|0.6901|401.0|HIT (cut leg would have hit)|P14 FAIL: edge -1.0 < +3; shrunk edge -4.7 not > 0; a model median does not clear the line|
|TEN@CIN|Chase Brown Rush Yds Under 58.5|CUT|0.6946|47.0|HIT (cut leg would have hit)|P13 FAIL: 6.5+ favorite rush under vs clock-killing script|
|TEN@CIN|Chase Brown Rush+Rec Yds Under 81.5|CUT|0.5018|93.0|MISS (good cut)|P4 UNVERIFIED: RB receiving defender mapping: no LB/S alignment source; man 16.5% / zone 7|
|TEN@CIN|Ja'Marr Chase Rec Yds Under 79.5|CUT|0.6901|110.0|MISS (good cut)|P3 FAIL: under vs soft WR D (YPT>=9.0)|
|TEN@CIN|Ja'Marr Chase Receptions Under 6.5|CUT|0.6724|9.0|MISS (good cut)|P3 FAIL: under vs soft WR D (YPT>=9.0)|
|TEN@CIN|Tee Higgins Rec Yds Over 69.5|CUT|0.6177|134.0|HIT (cut leg would have hit)|P14 FAIL: placed-ticket bar: PP20 Higgins o68.5 rec yds; $51.50 SGP Higgins 50+ yds; MODEL|
|TEN@CIN|Tee Higgins Receptions Over 4.5|CUT|0.6554|9.0|HIT (cut leg would have hit)|P14 FAIL: placed-ticket bar: PP40 Fantasy/PP20 rec yds/$51.50 SGP Higgins 50+ yds/FD 7-leg|
|TEN@CIN|Mike Gesicki Rec Yds Under 22.5|CUT|0.623|76.0|MISS (good cut)|P4 UNVERIFIED: TE defender mapping not ruled (ISS-05); man 16.5% / zone 77.2%, MOF closed |
|TEN@CIN|Mike Gesicki Receptions Under 2.5|CUT|0.6514|4.0|MISS (good cut)|P4 UNVERIFIED: TE defender mapping not ruled (ISS-05); man 16.5% / zone 77.2%, MOF closed |
|DFS_SLIPS|[PP $20 6-pick Power] Tee Higgins Rec Yds Over 68.5|CUT||134.0|HIT|P14 MISSING: no book price at this rung: no-vig MISSING, edge not computable; MODEL-SUSPEC|
|DFS_SLIPS|[FD 7-leg +694] Tee Higgins Receptions Over 3.5|CUT||9.0|HIT|P14 FAIL: edge +2.3 < +3; shrunk edge -5.3 not > 0|
|DFS_SLIPS|[FD $51.50 8-leg SGP] Tee Higgins Rec Yds Over 49.5|CUT||134.0|HIT|P14 FAIL: shrunk edge -3.0 not > 0; MODEL-SUSPECT: MC median 84.8 vs FD main 70.5 / book c|