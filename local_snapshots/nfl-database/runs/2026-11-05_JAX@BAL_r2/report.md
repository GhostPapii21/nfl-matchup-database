# JAX @ BAL — TNF Thu Nov 5 2026, 8:15 PM ET — game script r2 (built 2026-11-03 ~19:20 ET)

**Verdict: NO CARD.** 0 of 112 prop rungs and 0 game/half/quarter lines clear the bar under the current rules.

## Starter
Joe Fagnano (#12, UDFA rookie, the No. 3 QB) is confirmed as the starter by HC Jesse Minter on Nov 3. Sources: baltimoreravens.com (Mink), NFL.com (Patra), ESPN (Hensley) and the ESPN injury feed. Jackson is OUT (IR, thumb). Huntley is Doubtful (toe). PFF's free page also lists Fagnano (grade 38.4); used as a cross-check only.

## Fagnano vs BUF (Wk8, 24 dropbacks, LOW-SAMPLE)
10/21, 91 yds, INT, 3 sacks, EPA/db -0.43. aDOT 4.3; 24% of throws behind the LOS.
- Blitzed (n14): 6/12, 63 yds, EPA -0.12.
- Not blitzed (n10): EPA -0.86.
- Pressured (PROXY, n9): 2/6, 22 yds, 3 sacks.
- Targets: J. Hill 6 (aDOT -3.3), Andrews 4, Flowers 4 (0 catches, 1 INT), Bateman 3.

## JAX D (Wk1–8)
- Blitz 30.4% (16th). Pressure PROXY 21.5% (10th). EPA/db -0.050 (6th).
- Gives up yards to WRs (9.72 YPT vs league 8.02) and on deep middle/right balls. Holds TEs down (4.81 YPT). Lets RBs catch at 81.8%.
- Run D: 3.28 YPC.
- Man/zone and MOF: MISSING.

## Locked read (sha 76b563a3…5685)
- **Base:** JAX leads by 10–14 at the half, then runs out the clock.
- **Edges:** Henry rush U; J. Hill receptions O.
- **Secondary:** JAX spread/1H; BAL team total U.
- **Avoid:** Flowers and Bateman overs.

## Market (FanDuel, 19:15 ET)
- Full game: JAX -9.5 (-120) / BAL +9.5 (-102). Total 40.5 (o-108 / u-112). Pinnacle: JAX -10, 40.
- 1H: JAX -6.5, total 20.5. Q1: JAX -2.5, total 7.5. FD BAL team total 14.5.
- Weather: dry, wind about 3 mph, gusts 10, 26% precip. No weather leg.

## Pricing
- Anchored p = logit(FD no-vig) + a + b·(logit(sim avg3) − logit(no-vig)), using avg3|0.5 weights a=-0.0149, b=0.0230.
- b≈0.02, so anchored p stays within ±0.5 pt of no-vig. The **best anchored edge is +0.47** (bar +5, or +7 for BAL/backup-QB/injury legs).
- Raw sim edges, shown as flags only: Flowers rec/yds O +31–32 (contradicts the read), J. Hill rush U +27.8, Henry rush U 69.5 (-114) +23.5, Henry rush+rec U 80.5 +17.7, Lane rec yds O +22, Lawrence rush U 12.5 +13.8, Strange rec yds O 35.5 +6.1, P. Washington rec U 4.5 +8.5. **J. Hill rec O 2.5 (+110)** is +1.7 raw.
- Every BAL player leg also fails §7 3-of-4 (MISSING: Fagnano has 1 game).
- No model probability exists for game, half or quarter lines, so anchored = no-vig and edge = 0. All cut. The 1H/Q spreads match the script direction, but there is no edge.
- Full table with CLV open prices for every candidate, including rejected ones: policy_legs.csv. Rows per leg: checklist.md.

## Slips
None. No legs pass, so there's no 3–4 leg slip. The read's story ("JAX controls, BAL stalls": Henry U + BAL TT U / JAX spread + Lawrence rush U) is directional only.

## Where the live gate differs
- Live build.py (old gate) uses +3 on raw sim edge, with sims and min-p able to cut. Under it, 5 rungs screen-pass: Strange rec yds O 35.5/29.5, Strange rec O 3.5, P. Washington rec U 4.5, Lawrence rush U 12.5.
- Under today's rules (anchored p, +5/+7, sims flag only), none pass.
- Missing defender data is flag-only here, while depth_rule fails closed in the gate.

## Pre-mortem
- The anchored model has almost no sim weight (b 0.02), so it can't produce a +5 edge on any market. Under these rules the "no card" result is structural, not specific to this game.
- The sims lean hard on BAL overs (Flowers) against a 1-game QB sample. Treat that as noise.

## Gaps
- MISSING: man/zone and MOF, NGS, film, Wed–Fri practice reports, inactives.
- PFF: premium locked; coverage, pressure and target splits pending.
- FTN charting only goes through Wk8.
- Week label: odds and schedule files call this game wk9; the parent calls it wk10.

## Budget
- Odds API: one event pull, 35 credits (3,610 → 3,575). Log: odds/quota_log.csv.
- Zero Grok/xAI or OpenAI calls.
