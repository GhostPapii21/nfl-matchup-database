# Ghost6 — Phase 4 (Cross-reference and alerts) — Sun Nov 1 2026
Generated 2026-10-31 7:26 PM ET. Injury sources: injury_sweep_2026-11-01.md (Oct 31 1:15 PM ET, newest) over injuries.md (feed entries Oct 20–29).

Slip comparison: NOT_APPLICABLE for a new card (no new slip has been submitted). The placed slips were checked for correlation below.

## Status flags (latest file wins)
| Player | Latest status | Source | Effect |
|---|---|---|---|
| Brock Bowers (calf) | Was Q, limited Wed (feed Oct 28). **Not listed** in the Oct 31 sweep's LV Q/OUT list | sweep 10/31 | Probably cleared, but **confirm at 11:30 AM**. Availability flag |
| Puka Nacua | Active, not on the report. Sat Friday practice for rest (BetGuru) | injuries.md 10/26; sweep | Confirm at 11:30 AM |
| Donte Jackson (LAC CB, hamstring) | Q in the feed (Oct 20). **Not listed** in the 10/31 LAC Q/OUT list | sweep | Unresolved. If he plays, Puka's main defender allows 7.7 YPT. If he's out, Hart (10.4) or Still (6.5) replaces him |
| LAC S Derwin James | **OUT** | sweep | Removes LAC's best safety (3.9 YPT allowed). Positive for Puka and the LAR passing game |
| DJ Glaze (LV RT) | Q (feed Oct 28). Not in the sweep list | sweep | Check at inactives. LV OL is already weak (oneweekseason: Mayer blocking more). If Glaze is out, the TE may stay in to block, which cuts Bowers's routes |
| Elijah Wilkinson (ARI OT) | Q (feed Oct 29). Not in the sweep list. ARI G Jon Gaines II **OUT** | sweep | ARI OL down a guard, so more quick throws. Positive for McBride's catch volume, negative for depth |
| George Pickens (DAL WR) | **Q (shoulder/hamstring)** | sweep | If he's out, Lamb's targets go up. DAL WR Turpin is also **OUT**, which helps Lamb's volume |
| Gibbs (shoulder) | Q Wed (DNP), full practice Thu, **off the report** | sweep | Confirm at 11:30 AM |
| DAL LB **Dee Winters OUT** | OUT | sweep | Winters was McBride's top TE-coverage defender (17-15-88%). His replacement is unknown. The coverage-map row in Phase 2 is **stale**: re-map the replacement LB at inactives (8A gap until then; Barham 92% and Downs 90% still cover TEs) |
| ARI CB Max Melton | Q (feed Oct 27); not in the sweep | injuries.md | Minor for Lamb (Burke is his projected defender) |
| ARI TE Tip Reiman OUT | OUT | sweep | Removes a TE2, which concentrates TE targets on McBride. Positive |
| NYJ OT Mitchell, DT Sweat, DE Ossai OUT; LB Bailey D | sweep | NYJ pass rush is thinner, so LV has more time. Slight positive for Bowers's routes |
| PIT CB Slaughter, Echols OUT; CLE OT Tytus Howard Q | sweep | Doesn't affect Metcalf's coverage. CLE OL matters for game script only |
| DET S Kerby Joseph OUT | sweep | Not relevant to the Gibbs rush leg |

## Conflicting signals
- **Bowers:** the volume gate (5.8 rec at L3 share) conflicts with the Phase 2 positive (NYJ TE catch rate 72%, Cover 2 heavy). His L3 target share is falling (22.9%), and Glaze's status could pull the TE into blocking. Rung 5+ is kept.
- **Metcalf:** CLE plays the most man and single-high (bad for catch rate) while allowing 14.9 YPT through Campbell (good for yards). The yards line is consistent with this, but the variance is high. The source discrepancy on the Ward claim is resolved (it's unverified, and the actual meeting totals were 9-210 on 18 targets).
- **Gibbs:** volume (23.6 car) vs. efficiency (MIN 4.06 YPC, 4 runs of 15+ allowed in 6 games). Playing 60 resolves it, with 50 as the alternative.
- **Puka:** thin price edge (BetGuru: 3.6 points), but James OUT is positive. Availability (rest DNP) is the main risk.

## Correlations
- **Lamb 5+ rec with the placed Ticket 2 Lamb 60+ yds and Pickens 4+ rec:** this is a stack on the same player and the same passing game. PHASE_SCRIPT §11: "No player on more than one slip, including slips already placed." Rico cleared Ticket 2 players for different props, so this is **not** a cut. But the correlation is strong and positive with the placed ticket, so Lamb doesn't diversify the risk. **ALERT (needs a human decision).**
- **Gibbs 60+ rush with the placed Ticket 2 Gibbs 5+ rec:** same player. Rico's override applies here too. Rushing and receiving are only mildly correlated, but an injury or an early exit would sink both. **ALERT (human decision).**
- **McBride and Lamb are in the same game (ARI @ DAL, total 54.5):** a shootout helps both. DAL -7 blowout risk: if DAL leads big, McBride's catches go up from trailing volume while Lamb's Q4 targets go down. This is a partial hedge, not a stack. OK.
- No two legs share a QB. Puka/Bowers/Metcalf/Gibbs are each in separate games.

## PHASE_SCRIPT triggers
- **Blitz-volume cut:** MIN FTN blitz 71.9% (flagged as possibly overstated) applies to DET passing, not to the Gibbs rush leg. No trigger.
- **Run suppression ≤3.8 YPC:** MIN allows 4.06 to RBs, so it's **not triggered**. MIN's stuff rate (19.1%) and 15+ run suppression justify the rung cut anyway.
- **Soft matchup boost:** TE YPT ≥8.0: ARI 8.2 (not our TE leg), NYJ 7.30, DAL 7.24. **No boost** for Bowers or McBride. WR YPT ≥9.0: none (LAC 8.86, ARI 8.98 just under). No boost.
- **Injury boost:** Lamb (Turpin OUT, Pickens Q); McBride (Reiman OUT). Small, capped. Not applied to the rung.
- **Blowout/trailing script:** DAL -7 (Lamb Q4 risk, which is why we use 5+, not 6+). LAR -6.5 (Puka still gets 12.9 tgt at the projected share). No RB leg on a trailing team.

## Postmortem amendments applied (WEEK7_SUNDAY_2026-10-25)
- "RB legs depend on the offense sustaining drives": DET vs MIN, MIN allows 29.5% third-down and 17.6% RZ TD. DET's own offense is strong, but MIN suppresses it. This supports the Gibbs rung cut.
- "TE yards need a target-share check vs a run-heavy script (LaPorta wk7)": for Bowers, LV's rushing is down at L3 (18.3/g), so there's no run-heavy pull. McBride's team trails, so the risk is low.
- Henry wk7 trailing rule: not triggered (DET favored).

## Error classes to watch (pre-game)
Opportunity: Bowers (share falling), Metcalf (low total). Efficiency: Gibbs vs MIN. Availability: Bowers, Puka, Gibbs, D. Jackson, Glaze, Pickens. Source quality: PFR stale (Oct 29), Winters stale in the 8A map, Ward claim unverified. Model capability: projections are hand-built (no sims yet in my walk).

## Issues (stable)
- ISSUE-G6-01: PFR defense_advanced fresh pull blocked (403). Acceptance: a weekly pull via an allowed route, stored with its date.
- ISSUE-G6-02: nflverse doesn't credit receiving yards on laterals (Bijan wk7). Acceptance: the reconciler flags laterals automatically.
- ISSUE-G6-03: FTN parquet doesn't have man/zone or MOF. Acceptance: the Sharp/StatRankings weekly table is cached with a date.

## Phase 4 verdicts
| Leg | Verdict | Change? |
|---|---|---|
| Bowers 5+ rec | PASS (conditional on active + Glaze check) | none |
| Puka 70+ yds | PASS (conditional on active); James OUT is a plus | none |
| Metcalf 40+ yds | PASS | none |
| McBride 7+ rec | PASS, but **8A re-map needed** (Winters OUT) | flag |
| Lamb 5+ rec | PASS on data. **ALERT: same-player stack with the placed Ticket 2** (human decision) | flag |
| Gibbs 60+ rush (alt 50) | PASS. **ALERT: same-player stack with the placed Ticket 2 Gibbs rec** (human decision) | flag |
