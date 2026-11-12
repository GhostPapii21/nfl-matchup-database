# Ghost6 — Phases 8 addendum, 9, 10, 10G, sims, final card — Week 8 (Sun Nov 1, 2026)
Written Sat Oct 31, 2026, ~8:45 PM ET. Nothing posted, messaged, or bet. No API keys printed.
Sims: /workspace/nfl-database/week8/phase_walk/ghost6_sims.json (scripts /tmp/g6sim2.py; seeded, 100k/leg/model).

## Phase 8 addendum — Metcalf/Ward film claim: CONTRADICTED
nflverse PBP, wk4 CLE@PIT 2026-10-01: both INTs were NOT Metcalf targets.
- Q2 14:17 deep right → intended **M. Pittman**, INT **D. Ward**.
- Q4 0:10 deep right → intended **R. Wilson**, INT **G. Delpit**.
Metcalf 9 tgt / 5-115: locations 3L/3M/3R; defenders named Hickman, Delpit/Schwesinger, McNeil-Warren (2 PD), Harden, Campbell (2). Ward never named in coverage (only on a QB hit = blitz on the 43-yd catch). Consistent with Ward 91% LCB (no shadow). BetGuru DK_Metcalf.md likely misidentified the receiver. **Metcalf 40+ stays PASS**; Ward 8A risk noted, not a cut.
Folded from chart: NO wk7 5:03 OR go vs #29 (~40 yd), 8:12 dig (~18); TB "Metcalf not visible" = GAP. No other BetGuru film charts exist (only DK_Metcalf.md).

## Slip-rule eligibility (skill §11/§14) — decisive
| Leg | Rule result |
|---|---|
| Lamb 5+/6+ | **BARRED** — on placed Ticket 2 ("no player on more than one slip incl. placed"); Rico override only |
| Gibbs 60+ | **BARRED** — same (Ticket 2); override only |
| Higgins 5+ | **BARRED (new)** — Higgins 50+ rec yds is on the open FD 8-leg SGP (injury_sweep_2026-11-01.md) |
| McBride 7+ | 10G **BLOCK** (ARI +7 underdog, no ELIMINATED/TRAP exception) |
| Bowers 5+/6+ | 10G **BLOCK** (LV +1.5 underdog); 6+ also fails median rule (median 5) |
| Flournoy 3+ / Lamb | same QB — never on one slip (moot since Lamb barred). Flournoy shares Prescott with placed Pickens leg: flag, correlated not opposing |
| Puka, Metcalf, Tuten, A. Williams, Flournoy | eligible |
§14 checks: Metcalf yds — 4+ tgt each of last 3 (4,15,6) ✓, L4 median 74.5 ≥48 ✓; Puka L4 median ≥84 ✓; Tuten 60 L4 median 72.5 vs needed ≥72 (barely ✓); Higgins Chase share 21.5% <28% ✓ (moot); 3+ catch lines are 2.5 so 3.5+ rule n/a; nobody ≤3 tgt avg (A. Williams 4.75).

## Phase 9
**9A Weather (NWS hourly, pulled ~8:40 PM ET, 1–3 PM ET):** PIT 66–69F, SE 5 mph, 0% · CIN 70F, 3 mph, ≤4% · WSH 64F, 3 mph, ≤3% · **JAX 77F, E 14–15 mph (SOFT REVIEW), rain 37–48%** (below 70% → not a factor per §14; recheck within 2h of KO) · LAR SoFi, DAL AT&T (roof), DET Ford Field indoor. No hard flags.
**9B Rest/travel:** JAX and WSH off wk7 bye (rest edge both sides of PHI@WSH not — PHI normal); CIN bye wk6; IND travel to JAX; ARI travel to DAL. No flags.
**9C Stakes:** no eliminated/trap teams identified → no underdog exception (drives 10G blocks).
**9D Injuries (practice/designation/inactive kept separate):** Dee Winters OUT (DAL LB, helps McBride—blocked anyway). TEN without Tate/Spears, Ridley Q → CIN blowout/Q4-sit risk. Puka/D. Jackson questions → 11:30 & 2:35 checks (Phase 6). No new OUT on eligible legs as of injury_sweep file.
**9E Turnovers / 9F 3rd-down & RZ:** no leg-level flags beyond Phase 4 (from PBP). **9G:** Metcalf film misattribution logged; Higgins SGP overlap newly found.

## Phase 10 — source audit (48h policy, now Oct 31 ~8:45 PM ET)
| Source | Window | Pulled | Status |
|---|---|---|---|
| nflverse PBP/snaps/FTN/rosters | wk1–7 | Oct 31 | FRESH |
| NGS statboard (public JSON) | season | Oct 31 | FRESH |
| FanDuel fd_now.csv | — | Oct 31 6:53 PM ET | FRESH (recheck Sun) |
| NWS hourly | Sun 1–3 PM | Oct 31 ~8:40 PM ET | FRESH |
| StatRankings | season | Oct 31 | FRESH |
| PFR defense cache | season | Oct 29 6:02 AM ET | FRESH until Oct 31 ~6 AM → **STALE** now (403, not retried) |
| Sharp (coverage/schemes/tendencies/box) | season | Oct 27 | **STALE** |
| ESPN win rates | — | not pulled | GAP |
| Raiders Rundown / Hashtag Football | — | not pulled | GAP |
| FTN man/zone | — | missing | GAP (G6-03) |
| Film | — | can't watch | GAP except BetGuru chart |

## Phase 10G — game-script gate (outputs/nfl.py does not exist → weights applied by hand)
| Leg | Spread | Class | Weight |
|---|---|---|---|
| Tuten 60+ | JAX -10 | blowout fav | 1.00 (risk: lead-protect is good for rush) |
| Puka 70+ | LAR -6.5 | moderate fav, possession | 1.00 |
| Metcalf 40+ | PIT -3.5 | moderate fav, deep-ball | 0.90 |
| Flournoy 3+ | DAL -7 | blowout/moderate fav | 1.00 |
| A. Williams 3+ | WSH -5.5 | moderate fav, possession | 1.00 |
| Higgins 5+ | CIN -12.5 | blowout fav (Q4 sit risk) | 1.00 — barred by SGP anyway |
| Lamb / Gibbs | DAL -7 / DET -3 | fav / toss-up-ish (swing: DET pass rate) | 1.00 / 0.85–0.90 — barred |
| McBride 7+ | ARI +7 | underdog | **BLOCK** |
| Bowers | LV +1.5 | underdog | **BLOCK** |

## Sims — Ghost6 (100k each; MC = NB volume×binomial / bootstrapped per-play yards; Bias = volume −8%, catch −3%, yards −5%; GR = shared team-volume lognormal σ .22 + spread-signed script) vs BetGuru
| Leg | FD | Implied | G6 MC/Bias/GR | G6 avg | BG MC/Bias/GR (cons) | Edge vs price (G6 / BG) |
|---|---|---|---|---|---|---|
| Puka 70+ | -290 | .744 | .683/.649/.673 | .668 | .638/.787/.819 (.748) | −7.6 / +0.4 |
| Metcalf 40+ | -225 | .692 | .618/.594/.616 | .609 | .768/.676/.722 (.722) | −8.3 / +3.0 |
| Tuten 60+ | -158 | .612 | .580/.544/.572 | .565 | .654/.635/.768 (.686) | −4.7 / +7.4 |
| Tuten 50+ | -270 | .730 | .696/.652/.680 | .676 | — | −5.4 |
| Flournoy 3+ | -240 | .706 | .683/.622/.676 | .660 | .765/.758/.87 (.798) | −4.6 / +9.2 |
| A. Williams 3+ | -200 | .667 | .622/.556/.617 | .598 | .654/.628/.781 (.688) | −6.9 / +2.1 |
| Higgins 5+ | -166 | .624 | .577/.501/.574 | .551 | .736/.774/.684 (.731) | −7.3 / +10.7 |
| McBride 7+ | -225 | .692 | .622/.538/.614 | .591 | .650/.669/.932 (.750) | −10.1 / +5.8 |
| Bowers 5+ / 6+ | -310/-158 | .756/.612 | .619/.540/.608 · .487/.404/.486 | .589/.459 | (.818)/(.674) | −16.7/−15.3 |
| Lamb 5+ / 6+ | -440/-205 | .815/.672 | .724/.658/.717 · .609/.529/.604 | .700/.581 | (.855)/(.759) | −11.5/−9.1 |
| Gibbs 60+ / 70+ | -420/-250 | .808/.714 | .796/.767/.778 · .713/.677/.697 | .780/.696 | (.846)/— | −2.8/−1.8 |
**Finding:** my independent sims put EVERY leg below its vig-in price; medians all clear their lines (except Bowers 6+). BetGuru's sims run 8–18 pts higher, mainly in GR (e.g., McBride .932, Flournoy .87). The two model sets disagree → per §10 the legs need 4 of 4 / don't certify as +EV. My dispersion (gamma shape 8 on volume) may be wider than reality; BetGuru's GR looks overconfident. Truth is probably between.
Bonus-bet note: legs shorter than -250 (Puka -290, Tuten 50 -270, Gibbs 60 -420, Lamb 5+ -440, Bowers 5+ -310, McBride 6+ -440) are low value on a bonus bet since stake isn't returned.

## Final card (don't force legs)
Only **5** legs pass every gate. A clean 6th does not exist without an override. No second/third group possible without reusing players (§11).
**Recommended 5-leg:** Flournoy 3+ rec (-240) · Tuten 60+ rush (-158) · Metcalf 40+ rec yds (-225) · Puka 70+ rec yds (-290) · A. Williams 3+ rec (-200)
- Combined ≈ **+574** (6.74 dec). Hit: G6 **9.1% (1 in 11)**, BG cons 20.3% (1 in 4.9), break-even 14.8%. Bonus-bet EV per $1: G6 0.52, BG 1.17.
- 6-leg option ONLY with Rico override of Ticket 2 rule: + Gibbs 60+ (-420) → ≈ +735; hit G6 7.1% (1 in 14), BG 17.2%. Higgins 5+ as the 6th would need override of the open SGP (Higgins 50+ yds).
- Backups (same gates): Tuten 50+ (-270) for Tuten 60+; no other eligible backups.
**Ghost6 verdict:** by my sims this card is −EV on cash; acceptable only as a bonus-bet ticket. Not certifying.

## 11:30 AM ET inactives conditions (Sun)
- Drop Puka if limited/Q-downgraded or D. Jackson active-status change shifts LAR target tree (Phase 6; recheck 2:35 PM for 4:05/4:25 KO).
- Drop Metcalf if Rodgers out or Metcalf inactive; if Ward ruled out, upgrade only.
- Drop Tuten if JAX top-two RB returns active in full role or Tuten not RB1; recheck JAX wind/rain within 2h (rain only counts ≥70%).
- Drop Flournoy if Lamb/Pickens/Tolbert status changes put him off 60%+ snaps (watch Lewis/slot rotation).
- Drop A. Williams if he's inactive or Diggs/WSH WR room changes his slot role (G6 slot GAP).
- Recheck every price; any 20-cent move → reprice.

## Side-by-side vs BetGuru (latest groups_1031 / three_groups md)
| Item | BetGuru | Ghost6 |
|---|---|---|
| Metcalf | cut on Ward shadow + 2 INTs | INTs were on Pittman/Wilson; shadow contradicted → keep |
| Higgins 5+ | in pool | barred: open SGP has Higgins 50+ yds |
| Lamb / Gibbs | rung variants in pool | barred by Ticket 2 rule unless Rico overrides |
| McBride / Bowers | in pool | 10G underdog BLOCK |
| Treadwell / Downs | in draft groups | cut (Phase 1–4) |
| Sims | GR-heavy, all legs +EV | all legs −EV vs price; models disagree |
| Groups | 3 groups | 1 card of 5 (6 only w/ override) |

---
## Addendum (Oct 31, ~7:45 PM ET) — Gibbs rush+rec yards as 6th leg (Rico, pt650u)
**Prices:** FanDuel main line only: O121.5 at -111 (fd_now.csv, 6:53 PM ET); fd1031 had O120.5 at -115. **There are no alt rush+rec rungs** in fd_now, fd1031 or props/raw. The Odds API returned 401 with 0 requests remaining (quota used up), so no alt prices. Mid rungs below are fair-price only.

**Phase 1 log (nflverse PBP, carries-rush yds / targets-catches-rec yds = total):**
| Wk | Opp | Rush | Rec | Total |
|---|---|---|---|---|
| 1 | NO | 29-156 | 5-5-30 | 186 |
| 2 | BUF | 16-52 | 8-6-61 | 113 |
| 3 | NYJ | 20-99 | 8-7-65 | 164 |
| 4 | CAR | 15-46 | 7-4-22 | 68 |
| 5 | ARI | 25-151 | 6-5-56 | 207 |
| 7 | GB | 29-116 | 6-5-27 | 143 |
121.5+ in 4 of 6 games (L4: 3 of 4); median 153.5. **Wk4 reconcile:** play-level PBP shows 4 catches for 4+5+8+5 = **22** (no laterals). The 31 is not supported by play-by-play, so I use 22 (that game is 68 total either way).

**Phase 2 MIN:** rush defense 4.16 YPC vs league 4.33, EPA/rush -0.11 (slightly above average). RBs vs MIN get **4.5 tgt / 3.2 catches / 18.2 yds per game, 4.04 YPT** vs league ~5.75 / 4.5 / 32 / 5.54. That's a strong suppressor of RB receiving. PFR LB coverage (cache Oct 29, STALE): Cashman 9 tgt, 5 caught, 55 yds, 6.1 YPT; E. Wilson 11-9-77, 7.0 YPT; Metellus (S) 22-12-196. Zone-heavy / man-zone split is a GAP (FTN missing, G6-03).
**Phase 3:** 23.6 carries (~94 rush yds) + 6.5 targets (~0.8 catch rate; YPT cut ~25% for MIN) ≈ 26 rec yds → projection ~120. Market 121.5 is fair to slightly rich.
**10G:** DET -3 (total 46.5) = toss-up / small favorite, weight 0.85. Swing variable: DET pass rate if trailing. Rush+rec is partly script-hedged (lead → carries, trail → targets), better than straight rushing in a toss-up. §14 "could trail" (fav ≤3) applies; it only restricts unders, so no block.
**Ticket 2 correlation:** Gibbs 5+ receptions is on Ticket 2. Same player, positively correlated (catches feed rec yds), so the risk concentrates on Gibbs' volume/health. Allowed as a different prop by Rico. Flag only.

**Sims (100k each; bootstrap rush and target yards from 2026 PBP; GR carries vs targets anti-correlated by script):**
| Rung | MC | Bias | GR | Avg | Fair price |
|---|---|---|---|---|---|
| 80+ | .831 | .738 | .803 | .791 | -378 |
| 90+ | .759 | .646 | .734 | .713 | -248 |
| **100+ (mid)** | .677 | .549 | .659 | .628 | -169 |
| 110+ | .591 | .454 | .584 | .543 | -119 |
| O121.5 (FD -111, implied .526) | .495 | .356 | .498 | .450 | — |
Medians: MC 121, bias 105, GR 121. The main line fails the §14 median rule under the bias model and is −7.6 pts vs price.
**Recommendation:** 100+ is the mid rung (fair ~-169). Take it only if FD's alt is **-169 or longer**; there's no FD price to confirm, so it's **UNPRICED / PENDING Sunday pull**. Compared with Gibbs 60+ rush (-420; mine .780 vs implied .808 = −2.8 pts): 60+ rush is closer to fair but is <-250 (poor on a bonus bet). Rush+rec 100+ at about -169 adds more payout with similar edge. Do not take O121.5 -111 (−7.6).

**Six-leg recompute (with Flournoy 3+, Tuten 60+, Metcalf 40+, Puka 70+, A. Williams 3+; 5-leg = +574, G6 hit .0907):**
| 6th leg | Card price | G6 hit | 1 in X |
|---|---|---|---|
| Gibbs R+R O121.5 -111 (only priced) | ≈ +1181 | 4.1% | 24.5 (break-even 7.8%) |
| Gibbs R+R 100+ at assumed -169 | ≈ +973 | 5.7% | 17.6 (break-even 9.3%) |
| Gibbs 60+ rush -420 (prior) | ≈ +735 | 7.1% | 14.1 (break-even 12.0%) |
Still −EV on cash by my sims; bonus-bet use only. No BetGuru sim exists for rush+rec.
**Film:** Per BetGuru, README_RELIABILITY.md (not found on the box) flags the automated film charts as unreliable. All film reads (incl. DK_Metcalf.md) stay **UNVERIFIED**. The Metcalf verdict rests on PBP, not film.
**11:30 AM add:** drop Gibbs if limited or Q-tagged, or if Montgomery's status changes the carry split. Pull the FD alt rush+rec ladder then; take 100+ only at -169 or longer, else stay with 60+ rush or the 5-leg card.
