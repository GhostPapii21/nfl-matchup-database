# MNF postmortem: CHI 34, SEA 17 (Mon Nov 2 2026; nflverse 2026_08_CHI_SEA, folder playlogs/2026_wk9)
Blitz, Nov 3 2026, 8 AM ET routine. Public sources only: nflverse pbp and snap counts, ESPN box/play-by-play, Sharp coverage table. No bets, no messages.

## 1. Play log
- `playlogs/2026_wk9/CHI_SEA_enriched.csv` has 182 rows. All 135 scrimmage plays carry down, distance, score and EPA from nflverse, and 108 have a defender tag. Tags are tackler/PBU, **not coverage**; no public per-play coverage chart exists for this game.
- `CHI_SEA_explosives.csv` lists 14 explosives (pass 20+, rush 10+, 15+). The tally is in `playlogs/explosives_allowed.md`.
  - **SEA D allowed 7:** Odunze 4, Burden 1, Raymond 39-yd end-around, TE 1. CB tags: Pritchett 2 (13 snaps), Witherspoon 1, Jobe 1. Safety tags: J. Love 2. Four of the five WR explosives came **over the middle**.
  - **CHI D allowed 7:** JSN 4, Barner 1, Charbonnet 1, QB 1. Tags: Stevenson 2, Lewis 1, Thieneman 1, Bush 2. The JSN 43-yd TD had no tackler.
- Builder script: `playlogs/tools/enrich_chi_sea_mnf.py`.

## 2. SEA run calls: running was a losing call
- **Overall:** designed runs went 17 for 61 yds (3.59 YPC), -0.173 EPA/run, 17.6% success rate. Dropbacks: 40 at -0.158 EPA, 37.5% success rate.
- **Down 9+:** runs -0.072 EPA, 22% SR (9 runs, -0.65 EPA total, -0.082 WPA). Passes +0.033 EPA, 44% SR (+0.83 EPA, +0.099 WPA).
- **By situation:** first-down runs -0.255 EPA vs passes +0.101. Q3 run rate was 55%.
- **Costly drives:**
  - The late-Q3 4-run drive ended with an OPI and then a blocked FG.
  - The Q4 7:13/6:33 runs led into the Lynch INT (-5.36 EPA).
- **Context, Weeks 1-7:** CHI's run D was league-average (4.03 YPC, -0.097 EPA). SEA's dropbacks were +0.098 EPA vs runs -0.225.
- **Verdict:** SEA should have thrown while down 9+.

## 2b. SEA run/pass by quarter (from pbp, playlogs/2026_wk9/CHI_SEA.csv)
Pass = dropbacks (completions, incompletions, sacks, pass TDs, INT); run = designed rushes. Penalty/no-play rows excluded.

| | Pass | Run |
|---|---|---|
| Q1 | 6 | 4 |
| Q2 | 10 | 4 |
| Q3 | 5 | 6 |
| Q4 | 16 | 5 |
| Trailing by 9+ (pre-snap score) | 24 | 10 |
| **Total** | **37** | **19** |

Matches Ghost6's counts and ESPN totals. (If the score *after* each play is used instead of pre-snap, trailing-9+ is 22/10.) SEA still ran 29% of the time while down 9+.

## 3. Read grades
### r3 gate (runs/2026-11-02_CHI@SEA_r3): 23 legs, all cut
The model's direction was right on 11 and wrong on 12. Of the 23 cuts, 15 were correct and 8 would have hit.

**Cuts that would have hit:**
| Leg | Actual | Cut by / what should have caught it |
|---|---|---|
| Caleb O224.5 | 247 | Passing yards are now banned anyway |
| Swift R+R U86.5 | 79 | Under +3 |
| Roschon O10.5 | 17 | — |
| JSN O89.5, O99.5, O109.5 | 118 | §14 cushion and model-suspect. O89.5 was also barred as a nested rung of the open 70+ ticket |
| Barner U29.5 | 23 | — |
| Barner rec U3.5 | 2 | — |

**Misses in the model direction (the cuts were right, the model was wrong):**
- Burden, Odunze and Loveland unders, both yards and receptions. Actuals: Loveland 7-65 (9 tgts), Odunze 4-87 (6 tgts), Burden 7-56 with a TD (9 tgts; corrected 2026-11-03 from a wrong "3-41", verified vs ESPN box in playlogs/2026_wk9/CHI_SEA_espn_summary.json). Burden U52.5 (56) and rec U4.5 (7) both lost, so these remain model-direction misses. Raymond 2-14 on 3 tgts.
- Swift rush U59.5 (69), Darnold O238.5 (188), JSN rec O7.5 (6), Kupp O29.5 (7), Wilson O19.5 (0).

### Rico's slips
Graded in `slips/2026-11-02_MNF_CHI_SEA_graded.md`: 13 of 20 legs hit.
- **$75:** lost on Kupp 7 and Wilson 0.
- **$20:** lost on Charbonnet 29 and SEA 2H (8-21).
- **$15 cash-out:** right call; Barner, Kupp and Swift rec would have missed.

**Wilson:** 0 offensive snaps and 7 special-teams snaps. The leg most likely stands as a loss and does not void (FanDuel voids only for no snaps). Ask FanDuel support to confirm.

### Biggest misses and why
1. **Loveland, Odunze and Burden: the sim was too low.** Caleb-era form plus a full-strength opponent adjustment against SEA's low allowed YPT set the medians. Loveland's was 25 yds on a 30% target share. SEA plays about 90% zone, and the damage came in the middle zones (LB/S/CB3 tags), not on the mapped outside CBs.
2. **Kupp:** CHI's coverage plus SEA's script (running while trailing) left him 1 catch.
3. **Wilson:** no offensive role in a 4-back committee. N1 now marks him do-not-play.
4. **SEA 2H -1.5:** the script read had SEA in control, but CHI went 21-8 in the 2H off SEA turnovers.

### Ghost6 grades (runs/2026-11-02_SEA_CHI_ghost6/defense_profile.md)
**Game reads: 6 of 9 right.**
| Read | Ghost6 call | Result |
|---|---|---|
| CHI 1H +1.5 | supported | ✓ |
| SEA 2H -1.5 | supported | ✗ |
| JSN 70+/90+ | supported | ✓ |
| Burden 30+ | supported | ✓ (7-56) |
| U58.5 | supported | ✓ |
| Loveland ATD | challenged | ✓ (no TD) |
| Kupp 10+, Swift 50+, Wilson 15+ | neutral | Kupp ✗, Swift ✓, Wilson ✗ |

**Defender calls: 2 right, 2 wrong, 1 gap.**
- Kupp limited by Gordon: right result, mechanism unverified. Gordon played 62%, and the DPI was on J. Johnson.
- Burden's edge vs Emmanwori: right.
- **Odunze limited by Witherspoon/Jobe: wrong.** Odunze went 4-87, all four catches explosives, mostly over the middle.
- **Loveland held: wrong** (7-65).
- JSN with Muhammad out: flagged as a gap. Stevenson took the most tags.

**Our checklist coverage block** mapped outside CBs against a zone defense. The fix is a middle-of-field / zone-hole allowance input (code note 4/8).

## 4. Replay under the fixed rules
Setup:
- Rules: no shrink, SCHEME_EDGE with alerts, mirror overs, N1-N3, depth_rule.
- Pool: 209 legs at FanDuel prices plus FD alt rungs for Loveland, Burden, Odunze and Raymond (and Rico's other players), at kickoff minus 30 min.
- Sims: current tools/sim_v6.py.
- Location: `backtests/mnf_chi_sea_replay_2026-11-03/`. The run fails strict on the run-level "film" source only; that miss was waived for the leg grades.

**19 legs pass: 12 hit, -$2.59 at $10 flat.** The 190 blocked legs went 75 hits.
- JSN recyds O49.5-O109.5: 6 rungs, all hit. O124.5 lost.
- JSN rec O4.5 and O5.5 hit. O6.5, O7.5, O8.5 and O9.5 lost.
- Barner U29.5 and rec U3.5 hit.
- Kupp rec U2.5 at +120 hit.
- Horton U23.5 and rec U2.5 lost.
- Darnold rush O4.5 hit (DraftKings price; consensus template line).

**Loveland, Burden, Odunze: NOT caught.** Their overs had negative or near-zero edge at every rung:
- Loveland rec O3.5: -8.8
- Burden O29.5: -10.6
- Odunze rec O1.5: +0.4

None of them were SCHEME_EDGE all four, because matchup and scheme_fit were False against the mapped CBs. The fix is in code notes 4 and 7: zone-hole allowance, plus a target-share sanity check → MODEL-SUSPECT → mirror over to manual review.

**Depth rule:**
- **Raymond:** a depth receiver (WR3, 6.3% Caleb share, script_pass OK). Every rung was **BLOCKED** on defender_giving, because Pritchett had allowed 4.22 ypt (and the high/main rungs are not "low"). His low rungs that would have hit: yds O4.5 and O9.5, rec O0.5 and O1.5. He had 2-14 receiving.
- **Odunze:** WR2 by Caleb-era share (Burden 19.0 > Odunze 14.3 > Raymond 6.3), so the depth rule does not apply.
- **Kupp/Horton:** blocked because the script did not call for passing. Correct: Kupp went 1-7.

**SCHEME_EDGE alerts:** 7, all on Kupp overs, and all would have lost. The depth rule blocked them.

**§14:** blocked JSN O99.5 (-113), which was SCHEME_EDGE all four and would have hit. The same gate passed O109.5 at +124 (code note 6).

**Rico's slips under the fixed rules:**
- Only JSN 60+, 70+ and 110+ pass.
- No slip as placed could be built (5-8 legs, TD legs, N1 backs, depth and edge cuts).
- That is $0 risked against the actual -$95 plus the $15 cash-out.

**Door check (read-only):** `door.py` evaluate() in-process, DOOR_OUT=/tmp, gate result from the harness; see `door_check.py` / `door_check.json`.
- A rules-built slip using the top edge per FanDuel player passes the door with 0 fails, in both versions:
  - 4 legs: JSN O124.5, Horton U23.5, Kupp rec U2.5, Barner rec U3.5
  - 3 legs: the same minus Barner
- Both versions **lose** (JSN 118, Horton 26), so -$10 per slip.
- Rico's $15 slip as built gets 11 fails: GATE_PASS ×6, SHORT_PRICE ×3, DEPTH_RECEIVER, SLIP_SIZE.

## 5. Code
- Notes are appended to `postmortems/2026-11-03_code_notes_for_ghost6.md`. Already covered by the build: (a) ledger part, (b), (c), (g). Uncovered: 9 items.
- Deleted `tools/tests/make_fixture.pre_form.py`; `test_run_gate.pre_form.py` was not present.
- `cd tools && python3 -m pytest -q tests`: **406 passed**.
- `ledger_coverage_check.py`: OK.
