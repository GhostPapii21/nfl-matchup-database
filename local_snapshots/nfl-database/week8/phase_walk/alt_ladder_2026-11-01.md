# Alt-ladder scan — Week 8, Sun Nov 1, 2026 (Rico pt655u: alts allowed)
Written Sat Oct 31, 2026 ~8:25 PM ET. Nothing posted, messaged or bet. No API keys printed (Odds API out of requests; not used).
**Source:** betguru_2026-11-01_raw/fd_now.csv (FanDuel, 6:53 PM ET): Alt Rushing Yds, Alt Receptions, Alt Receiving Yds, plus main two-way lines. **FD posts no alt Rush+Rec ladder**, so rush+rec can only be graded at the main line.
**Full grid:** phase_walk/alt_ladder_scan.csv (548 rungs, 25 players). Script: /tmp/altscan.py.

## Method
- **No-vig for one-sided alts:** multiplicative de-vig against the same stat's main two-way market. V = implied(Over) + implied(Under) at the main line; fair(alt) = implied(alt) / V. Main lines use Over/V. FD alt ladders usually carry more hold than the main, so this leaves some vig in the fair price (conservative against us).
- **Ghost6 scan engine (100k × MC/Bias/GR):**
  - Volume: NB (gamma shape 8 + Poisson) on season targets/carries.
  - Catch rate × opponent factor (50%-shrunk).
  - Receiving yards bootstrapped per catch × opponent YPT/CR factor.
  - Rushing: own carries bootstrapped, YPC regressed 50% to league, then × 50%-shrunk opponent YPC allowed.
  - Bias: volume −8%, catch rate −3%, yards −5%.
  - GR: shared lognormal σ .22 plus spread tilt.
  - This generalizes my earlier hand-set projections and is somewhat lower on Walker rush (80+ now .571, was .623).
- **BetGuru engine:** his corrected bg_sim_v4.py (BG_YPCREG=100, the v4 fix), run unchanged on every leg from runs/betguru_audit_20261031T195019.
- **Shared rule (both engines):** raw edge ≥ +3 vs no-vig AND (0.5 + 0.7(p−0.5)) − no-vig > 0.
  - **Artifact:** for p < .5 the shrink moves p UP, so long-shot rungs pass trivially. I add a mid-rung floor (both engines p ≥ .45) and model-vs-market sanity checks.

## Gates and bars applied
- **10G underdog BLOCK:** Bowers, McBride (ARI +7), London/Bijan (ATL +2.5), Jefferson/A. Jones (MIN +3.5), Flowers (BAL +3), J. Taylor (IND +10.5), Goedert (PHI +5.5).
  - A. Jones (main rush 29.5) and J. Taylor (49.5) also show huge "edges" from stale season roles. Market mains signal role/injury news. MODEL-SUSPECT regardless.
- **Ticket-2 / open-SGP exact-market bars:**
  - Gibbs receptions, Lamb receiving yds, St. Brown receiving yds, London receptions, Flowers receptions, Pickens receptions, Godwin.
  - Higgins alt receiving yds (SGP 50+).
  - **Flowers alt receiving yds** (SGP has Flowers 50+ yds).
  - **Cook rush+rec — BARRED:** Ticket 2's Cook 70+ rush+rec is the same Rushing+Receiving Yds stat. Any Cook rush+rec rung nests with it (O96.5 hitting implies 70+ hits), the same logic as Higgins. It also fails both engines (−6.8 / −10.3).
- **§14 RB receiving-yards rule** (6+ YPT in 3 of 4, and opponent allowing above-average RB YPT; RB YPT allowed, league 3.31 per target):
  - Gibbs: YPT ≥6 in 2 of 4; MIN allows 1.85 → **FAIL** (cuts Gibbs 25+/30+ rec yds, which passed both engines).
  - Warren: 3 of 4 ✓; CLE allows 2.06 → **FAIL** (cuts Warren 25+ rec yds).
  - Tuten: 4 of 4 ✓; IND allows 4.75 → **PASS**. But Tuten averages ≤3 targets (2.75) → max one such leg per slip, none on Basic.
- **Same QB per slip:** Kyren receptions + Puka receptions (Stafford) can't share a slip. Puka is kept.
- **RB YPC cap (2):** Walker rush and Warren rush+rec are the only legs using the YPC assumption = 2.
  - Warren rush+rec is counted as a YPC leg anyway (rushing is ~75% of his total).

## Phases 1–4 for new RBs
- **Jaylen Warren (PIT −3.5 vs CLE):**
  - Rush+rec 73, 77, 176, 126, 188, 78, 137 (≥91 in 4 of 7, 3 of last 5).
  - 10–18 carries, 4–7 targets.
  - Snaps 97 → 87 → 75 → **62%** (falling: CAUTION).
  - CLE allows 4.58 YPC (soft). Moderate favorite 1.00.
  - **PASS-CAUTION.**
- **Kyren Williams (LAR −6.5 vs LAC):**
  - Rush+rec 65, 97, 158, 147, 76, 67, 121.
  - Wk7 snaps **51% vs Corum 44%; carries 16 vs 17** (near-even split).
  - LAC allows 4.34 YPC.
  - Rush+rec main 87.5 fails both engines (−3.7 / −6.0).
  - Receptions 4+ (+114) passes both (.530/.468; +8.4/+4.1 shrunk) and §14 (5+ targets in 3 of 4 ✓), but conflicts with Puka on the same QB → **alternate only**; Corum split CAUTION.
- **Walker rush+rec (Rico's add):** main O107.5 −113 (no alt ladder). G6 .499 (−0.1 / −0.0), BG .513 (+1.3 / +0.9) → **FAILS both. No swap. Keep Walker on rushing; don't stack both.**

## Every leg passing BOTH engines (mid floor p ≥ .45, after bars and gates)
| Player | Rung | FD | No-vig | G6 MC/Bias/GR → avg | BG MC/Bias/GR avg | G6 raw/shrunk | BG raw/shrunk | Gate status |
|---|---|---|---|---|---|---|---|---|
| Puka | **9+ rec** | +124 | .417 | .501 | .510 | +8.4 / +8.4 | +9.3 / +9.0 | ✓ (8A PASS-CAUTION, D. Jackson Q) |
| Puka | 8+ rec | −138 | .542 | .593 | .593 | +5.1 / +2.3 | +5.1 / +2.3 | ✓ (consensus rung) |
| Walker | **90+ rush** | +104 | .462 | .499 | .532 | +3.7 / +3.7 | +7.0 / +6.0 | ✓ (YPC leg 1; both medians 94/99 vs FD main 85.5, CAUTION) |
| Walker | 80+ rush | −144 | .556 | .571 | .623 | **+1.5** / −0.6 | +6.7 / +3.0 | **FAILS my scan engine** |
| Tuten | **20+ rec yds** | +158 | .365 | .455 | .507 | +9.0 / +10.3 | +14.2 / +14.0 | ✓ §14 RB rec PASS; ≤3-target leg (1 per slip) |
| Tuten | 15+ rec yds | −102 | .476 | .513 | .569 | +3.7 / +3.3 | +9.3 / +7.3 | ✓ |
| Warren | **O90.5 rush+rec** | −113 | .500 | .532 | .582 | +3.2 / +2.2 | +8.2 / +5.8 | ✓ (YPC leg 2; snaps falling CAUTION) |
| Kyren | 4+ rec | +114 | .437 | .530 | .468 | +9.3 / +8.4 | +3.1 / +4.1 | alt only (same QB as Puka; Corum split) |
| Gibbs | 30+ rec yds | −106 | .485 | .533 | .546 | +4.8 / +3.8 | +6.1 / +4.7 | **CUT §14** (MIN RB YPT 1.85); also correlated with T2 Gibbs rec |
| Warren | 25+ rec yds | +114 | .440 | .487 | .489 | +4.7 / +5.1 | +4.9 / +5.2 | **CUT §14** (CLE RB YPT 2.06); one leg per player anyway |
| Lamb | 8+ rec | +168 | .349 | .411 | .408 | +6.2 / +8.8 | +5.9 / +8.7 | below the .45 floor; T2 same player (Lamb rec allowed but flagged) |
| Bowers / McBride / Flowers / J. Taylor / A. Jones | various | | | | | pass | pass | **10G BLOCK** (+ Flowers bars, A. Jones/Taylor model-suspect) |
Nothing passed for Cook (rush or rush+rec), Gibbs rush/rush+rec (rush+rec O121.5: G6 +1.1), Flournoy, Metcalf, A. Williams, St. Brown receptions, G. Wilson, P. Washington, B. Allen, Javonte Williams, Bijan (dog) or Kyren rush/rush+rec.

## Best card (best-edge rung per player; 4 legs, not padded)
| # | Leg | FD | G6 p | BG p |
|---|---|---|---|---|
| 1 | Puka Nacua 9+ receptions (LAR −6.5) | +124 | .501 | .510 |
| 2 | Kenneth Walker III 90+ rush yds (KC −1.5 @ DEN) | +104 | .499 | .532 |
| 3 | Bhayshul Tuten 20+ rec yds (JAX −10.5) | +158 | .455 | .507 |
| 4 | Jaylen Warren O90.5 rush+rec (PIT −3.5) | −113 | .532 | .582 |
- **Combined ≈ +2122** (22.2 dec; FD SGP repricing n/a, four different games). Hit: **G6 6.1% (1 in 16.5), BG 8.0% (1 in 12.5)**; break-even 4.5%.
- **Safer mid-rung version** (Puka 8+ −138, Walker 90+ +104, Tuten 15+ −102, Warren O90.5 −113): ≈ **+1213**. Hit G6 8.1% (1 in 12.4), BG 10.5% (1 in 9.6); break-even 7.6%.
- **No sixth/fifth leg:** Kyren 4+ rec is the only other pass and conflicts with Puka (same QB). Use it as Puka's backup if Puka is ruled out.
- **Low-value-on-bonus flag (< −250):** none on the card.
- **Correlation:** four separate games; YPC legs = 2 (Walker, Warren). Walker and Warren both lean on rushing models running above market mains (Walker main 85.5 vs medians 94/99), so their errors are correlated (CAUTION). No Ticket-2 or SGP overlap on any card leg.
- **vs consensus:**
  - Walker 80+ (−144) fails my generalized engine (+1.5 raw), so Walker moves up to 90+, which passes both.
  - Puka 8+ still passes; 9+ has the larger shrunk edge.

## 11:30 AM ET conditions (Puka/Walker late games → recheck 2:35 PM ET)
- **Puka:** drop if limited or downgraded; D. Jackson OUT helps. Swap to Kyren 4+ rec only if Puka is out (then recheck the Corum split).
- **Walker:** drop if KC lists a split back active in role.
- **Tuten:** drop if he isn't the JAX RB1 or the third-down back changes. JAX rain only counts at ≥70%.
- **Warren:** drop if PIT activates a back that pushes his snaps below ~55% (Wk7 62%).
- Reprice any 20-cent move; alt-ladder prices move fast.

## Near-misses (one engine passes, or blocked/barred)
| Leg | G6 raw/shrunk | BG raw/shrunk | Why out |
|---|---|---|---|
| Walker 80+ rush −144 | +1.5 / −0.6 | +6.7 / +3.0 | G6 fails |
| Gibbs O121.5 rush+rec −113 | +1.1 / +0.8 | +3.7 / +2.7 | G6 fails |
| Warren 90+ alt rush +280 | +2.1 / +9.1 | +3.3 / +9.9 | G6 raw < 3; long shot |
| Puka 125+ rec yds +280 | +2.0 / +8.9 | +4.3 / +10.6 | G6 raw < 3; long shot |
| Gibbs 30+ rec yds −106 | +4.8 / +3.8 | +6.1 / +4.7 | §14 cut (MIN) + T2 correlation |
| Kyren 4+ rec +114 | +9.3 / +8.4 | +3.1 / +4.1 | same QB as Puka |
| Lamb 8+ rec +168 | +6.2 / +8.8 | +5.9 / +8.7 | p < .45 floor; T2 same player |
| Bowers 70+ rec yds −110 | +8.8 / +6.3 | +8.6 / +6.2 | 10G underdog block (LV +1.5) |
| McBride 8+ rec −122 | +3.1 / +1.8 | +5.6 / +3.5 | 10G underdog block |
Film reads stay UNVERIFIED.

## UPDATE Oct 31, 2026 ~8:40 PM ET: superseded by pressure_checkdown_2026-11-01.md
- Warren O90.5 rush+rec has been DROPPED (fails G6 after pressure/QB adjustment).
- Gibbs O121.5 rush+rec has been REVIVED (passes both engines; needs a Rico override because Ticket 2 already has Gibbs).
- MIN RB YPT allowed was wrong: it is 4.04, not 1.85 (bad denominator); QB-adjusted it is 4.72.
- New best card: Puka 9+ / Walker 90+ / Tuten 20+ at about +1079 (G6 11.4%, BG 13.7%).
