# Ghost6 — Phases 1–4 on BetGuru's DRAFT-card extra legs — Sun Nov 1 2026
Generated 2026-10-31 ~7:45 PM ET.

Sources:
- nflverse play-by-play and snap counts 2026 (through wk7/8).
- BetGuru's full_leg_*.json (ESPN game logs).
- FanDuel prices from betguru_2026-11-01_raw/fd_now.csv (pulled 6:53 PM ET).
- PFR defense_advanced, cached Oct 29 6:02 AM ET (stale ~2 games; fresh pulls 403).
- Coverage: Sharp man/zone and MOF (via BetGuru's leg files and my Phase 2), plus StatRankings.
- Injuries: injury_sweep_2026-11-01.md (Oct 31 1:15 PM ET).

## Phase 1 — game logs and reconciliation
ESPN logs (BetGuru) and nflverse play-by-play **match on every game for all six players**. Format: targets-catches-yards by week (rushes for Tuten), plus snap %.

| Player (team) | Logs | Snap% L3 | Target/carry share L3 |
|---|---|---|---|
| Tee Higgins (CIN) | 6-3-59, 10-5-95, 7-6-90, 16-11-157, 4-2-22, (wk6 DNP), 7-6-148 | 79/69/87 | 30/13/25% tgt |
| Bhayshul Tuten (JAX, bye wk7) | rush 15-66, 13-65, 15-73, 17-73, 22-72, 12-39 | 59/68/58 | 68/92/50% carries |
| Laquon Treadwell (IND) | 1-0-0, 3-3-61, 1-1-20, 6-5-42, 8-2-34, 5-2-21, 2-2-19 | 80/93/74 | 19/13/10% (falling) |
| Antonio Williams (WSH, bye wk7) | 4-4-64, 3-3-24, 4-2-15, 8-3-21, 3-3-31, 4-3-50 | 69/68/67 | 22/13/11% |
| Josh Downs (IND) | 4-2-37, 9-7-72, 11-5-77, 4-3-16, 6-3-47, 8-4-40, 4-2-18 | 85/86/85 | 14/21/19% |
| Ryan Flournoy (DAL) | 4-2-22, 6-5-23, 8-2-22, 5-4-37, 5-3-90, 9-7-40, 4-4-70 | 68/87/78 | 12/16/15% |

How often each player has cleared the leg this season:
- Higgins 5+ catches: 4 of 6.
- Tuten 60+ rushing yards: 5 of 6 (the miss was wk6, 39 yards).
- Treadwell 20+ yards: 5 of 7 (missed wk7 with 19). Treadwell 2+ catches: 5 of 7.
- Antonio Williams 3+ catches: 5 of 6.
- Downs 3+ catches: 5 of 7 (2 catches last game).
- Flournoy 3+ catches: 5 of 7.

Context:
- Downs **requested a trade** but is expected to play (sweep).
- IND traded G Quenton Nelson and DT DeForest Buckner.
- WSH WR Terry McLaurin is out for the season, which concentrates WSH targets.

## Phase 2 — 8A defender check, plus man/zone and middle-of-field (MOF) coverage
Man/zone % and MOF closed/open % are from Sharp; YPT = yards per target.

| Leg | Defense / mapped CB (PFR: tgt-catches, comp%, YPT) | Scheme (man/zone; MOF closed/open) | 8A |
|---|---|---|---|
| Higgins 5+ catches | TEN: Cordale Flott 9-6, 66.7%, 9.2 YPT (4 games). TEN allows the 5th-most YPT to WRs and ranks 1st in slot YPT. CIN S Dugger OUT (irrelevant to the leg) | man 16.5 / zone 77.2; MOF 45.6 / 51.2 | PASS |
| Tuten 60+ rushing | IND run D: 4.59 YPC allowed overall, 3.87 since wk6. **DT Buckner traded**, so the interior is weaker (the 3.87 is pre-trade) | n/a | PASS (run-suppression trigger ≤3.8 not hit) |
| Treadwell 20+ yds / 2+ catches | JAX: Travis Hunter 19-12, 63.2%, 7.5 YPT. JAX allows **10.0 YPT to WRs (rank 1)**, 10.4 outside. JAX S Antonio Johnson OUT | man 21.0 / zone 73.4; MOF 46.0 / 51.1 | PASS |
| Antonio Williams 3+ catches | PHI: Quinyon Mitchell 20-13, 65%, 7.0 YPT. **Mismatch: AW lines up in the slot about 50% of the time and Mitchell plays outside**, so the slot defender isn't mapped (GAP). PHI CB Jonathan Jones OUT | man 15.1 / zone 72.8; MOF 49.1 / 43.4 | PASS on the numbers; alignment GAP |
| Downs 3+ catches | JAX: **Jourdan Lewis 18-10, 55.6%, 6.0 YPT, 52.3 rating**. That's under my 60% completion line, and Downs catches only 56.5% of his targets (NGS) | man 21.0 / zone 73.4 | **FAIL (under 60%)** |
| Flournoy 3+ catches | ARI: Garrett Williams 6-4, 66.7%, 3.5 YPT (thin: 3 games). ARI allows 8.98 YPT to WRs. ARI CB Melton was Q in the feed but isn't on the latest sweep | man 9.1 / zone 70.9; MOF 21.9 / 56.7 (zone-heavy, middle open) | PASS for catches; yards correctly cut |

## Phase 3 — Opportunity Gate
| Leg | FanDuel price (implied) | Volume projection | Median | Gate |
|---|---|---|---|---|
| Higgins 5+ catches | -166 (62%) | ~8.3 tgt × 66% catch rate | ~5.3–5.5 | **THIN**. CIN -12.5 puts blowout pressure on late volume, and his 14.2 aDOT means a lower catch rate. CAUTION |
| Tuten 60+ rushing | -158 (61%); 50+ at -270 | 15–16 carries (share .65), JAX -10 | ~66–69 | PASS |
| Treadwell 20+ yds | -178 (64%) | 3–4 tgt (share falling, wk7 had 2) | ~24–28 | **THIN**: his L4 yards are 42/34/21/19, trending down |
| Treadwell 2+ catches | -245 (71%) | 3–4 tgt × 58% | ~2.2 | Coin-flip vs 71% implied → **FAIL** |
| Antonio Williams 3+ catches | -200 (67%) | 4.5–5.5 tgt (McLaurin out) × 69% | ~3.4 | PASS, thin |
| Downs 3+ catches | -225 (69%) | ~6 tgt × 56% | ~3.3 | FAIL (8A plus price) |
| Flournoy 3+ catches | -240 (71%) | ~5.5–6 tgt (Turpin OUT, Pickens Q) × 67.5% | ~3.8 | PASS |

## Phase 4 — Alerts
- **IND@JAX stack (Downs, Treadwell, Tuten). FLAGGED.**
  - All three ride one game script (JAX -10). JAX leading means more Tuten carries and more IND trailing passes, so the legs are positively correlated.
  - That correlation also concentrates the risk: an IND-controlled game or JAX passing in the red zone sinks Tuten. A low-volume IND game (wk7: 21 team targets) sinks both IND receivers.
  - Treadwell's two legs are the same player and should never both be used.
  - Recommendation: **at most one IND@JAX leg (Tuten)**.
- **Treadwell and Downs overlap:** both depend on Daniel Jones's volume. Tyler Warren is cleared, which takes targets from both.
- **DAL passing concentration:** Flournoy, Lamb 5+, the placed Ticket 2 (Lamb 60+, Pickens 4+) and McBride (same game). The Flournoy and Lamb boost comes from the same source (Turpin OUT, Pickens Q). If Pickens is active, the boost shrinks for both.
- **CIN -12.5 blowout risk:** affects Higgins's 4th-quarter volume.
- **Downs trade request:** role or motivation risk. Unquantified.
- **Antonio Williams:** slot alignment GAP. PHI is missing CB Jones, a plus.
- **Ticket 2 overlap:** none of the six is on Ticket 2.

## Verdicts
| Leg | Ghost6 verdict | BetGuru draft |
|---|---|---|
| Higgins 5+ catches -166 | PASS with CAUTION (blowout, deep aDOT) | Groups 1 and 2 |
| Tuten 60+ rushing -158 | **PASS** (50+ at -270 is the safer alternative) | Groups 1 and 3 |
| Treadwell 20+ yds -178 | **CUT/THIN**: falling share, IND@JAX stack | Group 1 |
| Treadwell 2+ catches -245 | **CUT**: median ~2.2 vs 71% implied | Group 3 |
| Antonio Williams 3+ catches -200 | PASS (thin), slot GAP | Groups 1 and 3 |
| Downs 3+ catches -225 | **CUT**: 8A Lewis 55.6% < 60%, 56.5% catch rate, trade noise | Groups 1 and 3 |
| Flournoy 3+ catches -240 | PASS (DAL stack noted) | Groups 2 and 3 |

## Side-by-side with BetGuru's phase files
- betguru_phase1.md and betguru_phase2.md cover the original 41 legs. **Neither has rows for Tuten, Treadwell, Antonio Williams, Downs or Flournoy**, and Higgins appears only as a receiving-yards leg (Phase 1 PASS; Phase 2 PASS, PENDING_FILM, Flott). That means BetGuru's DRAFT legs skipped its own Phase 1–2 files and went straight to the group builder.
- BetGuru labels Downs's 55.6% "borderline, cleared by 6.6 tgt/g". I cut it under the 60% rule I applied to McBride.
- BetGuru's own Phase 2 lists McBride as "GAP — missing PFR mapped defender". Mine maps Winters → replacement (see ghost6_phase7_8.md).
