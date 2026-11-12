# r5 FINAL (rebuilt 2026-11-04 ~05:10 ET under Rico 05:03 ET: "Keep the tiers as a flag only; the read and the other gates decide")
The +1/+3 anchored tiers are now a LABEL only (under +1 / LEAN / FULL) and never cut. What decides each leg: the locked read plus addenda 1 and 2, N1, §3-of-4, the last-2 downgrade, depth/role rules and best price. Legs with no model edge are not cut for that.
Every leg sits under +1 anchored, so every leg carries the "under +1" flag, and former +7 legs also carry "former +7 leg: higher bar pending Rico".

## CARD (singles first)
| leg | best price | gates | tier flag |
|---|---|---|---|
| Henry rush U69.5 (read EDGE1) | DK -114 (FD -114; Pin U70.5 -118) | §3 3/4 [102,58,45,53], last-2 OK, N1 ok | under +1 (+0.21) |
| Lawrence rush U12.5 (read SLIP-STORY) | FD -114 (Pin -114) | §3 3/4 any-QB window (Rico's call), last-2 OK | under +1 (-0.05) |
| BAL team total U14.5 (read SECONDARY) | FD -120 | §3 3/4 [30,10,13,10], last-2 OK | n/a (no game model) |
| JAX 1Q -2.5 (addendum 1) | Pinnacle -109 (DK -122, FD -128) | §3 3/4 [3,7,-7,7], **last-2 DOWNGRADE** | n/a |
| JAX 1Q ML (addendum 1) | Pinnacle -217 (DK -230, FD -265) | §3 3/4, **last-2 DOWNGRADE** | n/a |

- CUT by the gates: JAX -10 / -9.5 (1/4), JAX 1H -6.5 (2/4), JAX 1H ML (2/4).
- Off-read passes (singles only, not on the card): Strange rec yds o35.5 FD -114 (4/4, OK); Washington rec u4.5 DK -125 (3/4, OK); BTJ rec u1.5 DK -195 (3/4, OK); plus downgraded Meyers/Hunter unders. See policy_legs.csv.
- **Addendum 3 (sha b420a4d6…), 05:20 ET:**
  - Washington rec u4.5 is DROPPED from the off-read list. The Hamilton reason is "not counted", Washington is the WR1, and the leg is DOWNGRADE once Wk8 is left out.
  - Washington overs FAIL 3-of-4. The o39.5/o29.5 mirror rungs pass only without Wk8, at -332/-610 (short-price flag). Candidate only.
  - Strange o35.5 passes with and without Wk8; the PFF CAUTION is "not counted". Off-read, singles only.
  - Rodriguez legs are conditional on Tuten OUT, and the Wednesday report is not posted, so PENDING. N1 projects a pass; no quote in the file (NO_QUOTE).
- **Addendum 4 (layers, 05:30 ET):**
  - Washington u4.5 stays OFF. His overs miss §3, so they are a Rico decision only.
  - Strange is re-mapped to right-side TE production (11 tgt, 114 yds right).
  - **Lawrence U12.5 carries a scramble-conflict flag:** 53 of 80 rush yds came on scrambles, and BAL allows a 7.3% scramble rate vs 4.8% league.
  - Gaps: no NGS; no coverage shell.
- **Errata (Ghost6 vet, 2026-11-04 ~09:00 ET; the hashed addenda are left unedited):**
  - Washington's main rec-yds line is **o63.5 FD -114** (policy_legs.csv already uses 63.5). The "o62.5 DK -112" in addenda 3 and 4 was DK's alternate quote.
  - 3-of-4 at 63.5: with Wk8 [7,124,64,16] 2/4; without Wk8 [40,7,124,64] 2/4. FAIL, so nothing changes.
  - The 1Q/1H ML shop rows showed book "nan" because the point is empty on ML rows. Fixed in game_lines.py and game_legs.csv.
  - 1Q ML: Pinnacle -217 verified (DK -230, FD -265). 1H ML: Pinnacle -318 (DK -345, FD -380).
- Optional slip: Henry U69.5 + Lawrence U12.5 + BAL TT U14.5. The SGP is unpriced; the product of singles is about +546.
- The 1Q legs are downgraded and come from a thesis the blitz data weakens (see below), so they're singles only.
- The Fagnano-only BAL receiving legs are still a **decision for Rico** (table below). If he says yes, 6 legs clear §3, and their tier labels are only flags.

---
(Text below is the earlier tiers-as-cuts write-up, SUPERSEDED as to cut/pass. The check data is still valid.)
# r5 FINAL: TNF Thu Nov 5, 2026, JAX @ BAL (ESPN Week 9; the "week10" folder name is a mislabel)
Tiers (Rico 2026-11-04 04:37 ET "Use +1 to +3"): anchored edge under +1 = CUT; +1 to under +3 = LEAN; +3 or more = FULL.
- Former +7 legs use the same tiers plus the flag "former +7 leg: higher bar pending Rico".
- The r4 checks are unchanged: §3-of-4, last-2 downgrade, N1 (RBs only), shopping/NO_QUOTE, PFF flags. The any-QB rush window is still Rico's call.
- Reads:
  - Locked read 76b563a3... is untouched.
  - Addendum read_addendum_2026-11-04.md, sha256 4c6f0999cfdf88c7866b737c31191283e38d83a760328d7b97d6e9b131229562. It is pre-kick, so it counts as a locked read.
- Odds: pulled 2026-11-03 19:15 ET. No new credits.

## CARD UNDER TIERS: NO CARD
- All 112 prop legs are CUT. The highest anchored edge is +0.47 (Flowers rec yds over, which is also a read-AVOID). Henry U69.5 is +0.21 and Lawrence U12.5 is -0.05.
- Game lines are "no model edge = cut under tiers". The policy has no game model, so there is no anchored p from no-vig, and these legs cannot show +1.

## r4 flag-only view (comparison only, NOT a card)
- Henry rush U69.5: DK/FD -114.
- Lawrence rush U12.5: FD/Pinnacle -114.
- BAL TT U14.5: FD -120.
- Optional 3-leg slip: product of singles about +546.
Under the tiers, all of these are CUT.

## New game legs (from the addendum), checks
Window: JAX's last 4 games (bye in Week 7).
- 1Q margins: [3, 7, -7, 7]
- 1H margins: [10, -7, -3, 28]
| leg | §3-of-4 | last-2 | best price (FD/DK/Pin) | r4 flag-only | tiers |
|---|---|---|---|---|---|
| JAX 1Q -2.5 | PASS 3/4 | DOWNGRADE [-7, 7] | Pinnacle -109 (DK -122, FD -128) | PASS-DOWNGRADE | CUT (no model edge) |
| JAX 1Q ML | PASS 3/4 (W/L) | DOWNGRADE | Pinnacle -217 (DK -230, FD -265) | PASS-DOWNGRADE | CUT (no model edge) |
| JAX 1H -6.5 | FAIL 2/4 | DOWNGRADE | DK/Pinnacle -102 (FD -110) | CUT | CUT |
| JAX 1H ML | FAIL 2/4 (W/L) | DOWNGRADE | Pinnacle -318 (DK -345, FD -380) | CUT | CUT |

**Thesis test.** I verified both JAX numbers against pbp+FTN: blitz rate 30.4% and pressure proxy 21.5% (Weeks 1-8, n=270 dropbacks). Fagnano had 3 sacks on 24 dropbacks.
- Against Rico's blitz idea: Fagnano was **better when blitzed** (50% completions, 5.2 YPA, 0 INT) than when not blitzed (44%, 3.1 YPA, 1 INT).
- For the pressure idea: 2 of his 3 sacks came when blitzed, and the proxy shows 3 sacks on 9 pressured dropbacks.
- Net: blitz rate alone doesn't back the 1Q/1H case, the sack and pressure angle does, and the sample is 1 game. The 1Q legs clear §3-of-4 on JAX's own margins, not on the Fagnano read.

## DECISION FOR RICO: "OK a 1-game read for these legs?"
Fagnano has 1 game, so these legs are MISSING under §3-of-4. They are neither silently cut nor silently passed.
| leg | best price | 1-game result | if YES: §3 | anchored | tier | flags |
|---|---|---|---|---|---|---|
| Hill rec o2.5 | Pinnacle +116 | 4 rec (3 from Fagnano) | 1/1 pass | -0.33 | CUT | former +7; PFF MISSING |
| Hill rec yds o13.5 | FD -114 | 20 yds | 1/1 pass | -0.35 | CUT | former +7; PFF MISSING |
| Andrews rec yds u18.5 | FD -114 | 14 yds | 1/1 pass | -0.20 | CUT | former +7; PFF agree |
| Andrews rec u2.5 | Pinnacle +109 | 3 rec | 0/1 FAIL | -0.29 | CUT | former +7 |
| Flowers rec u4.5 | DK -140 | 0 rec | 1/1 pass | -1.12 | CUT | former +7; raw sim -32 opposes; locked read AVOID on Flowers |
| Flowers rec yds u47.5 | FD -114 | 0 yds | 1/1 pass | -1.21 | CUT | former +7; raw sim -31 opposes |
| Bateman rec yds o14.5 | DK -114 | 22 yds | 1/1 pass | +0.02 | CUT | former +7 |

- **If Rico says YES:** 6 legs clear §3 (all except Andrews u2.5). Under the tiers, **nothing plays**, because every leg's anchored edge is under +1.
- Under r4's flag-only view, those same 6 would be 1/1 passes. The two Flowers unders also carry a strong sim-opposition flag and conflict with the locked read.
- **If Rico says NO:** they stay MISSING, which means cut.

Files: fagnano_throw_log.md/.csv, fagnano_profile.md/.csv, fagnano_splits.csv, read_addendum_2026-11-04.md (+ .sha256), policy_legs.csv, game_legs.csv, game_lines_out.txt.

## Addendum 2 (BAL D snapshot -> JAX), sha256 in read_addendum2_2026-11-04.sha256
- BTJ-as-WR1 is REFUTED: he's a depth target. Washington is the one who fits the WR1-left pattern, which CONFLICTS with the Washington under.
- Strange seam: partial. His volume fits, the seam doesn't (0 deep-middle targets). PFF CAUTION stands as a flag.
- Etienne has no JAX carries. Tuten DNP. No RB props quoted.
- Hawkins is PENDING (official report: DNP, no game status).
- Participation 2026 isn't published (404), so alignment is ball-location only (FLAG).
- Every leg is under +1 = CUT. The card is unchanged: NO CARD.
