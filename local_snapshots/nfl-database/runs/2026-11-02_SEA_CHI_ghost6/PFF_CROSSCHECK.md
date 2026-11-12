# PFF cross-check (Rico screenshots 05:53–05:55 ET), Ghost6 CHI@SEA, checked ~06:05 ET Nov 2
Second sources:
- **PFR** = Pro Football Reference 2026 advanced defense, "through week 7", public page via the Firecrawl API, pulled 05:06 ET (src/pfr_def.html).
- **nflverse** = play_by_play_2026 (through Nov 1, pulled 05:04 ET) plus snap_counts_2026 (src/fu).
- **ESPN** = box scores (src/fu/sum_*.json).
- **Bears.com** = official injury report; NFL.com and USA Today for news.
I did not use PFF itself (paywall). Its values are Rico's. The PFF-only grades (overall, coverage, run D, pass rush) have **no public second source**, so they are flagged SINGLE-SOURCE CAUTION.

## Jaylon Johnson (CB, CHI)
| Metric | PFF | 2nd source | Match? | Trust |
|---|---|---|---|---|
| Grade 40.9 (90/97); coverage 36.8 (92nd); run D 63.3 | as shown | none public | – | CAUTION (single source). Directionally consistent with PFR |
| Targets | n/a | PFR 31 | – | PFR |
| Receptions allowed | 20 | PFR 24 | **MISMATCH** | CAUTION: see why below |
| Yards allowed | ~346 (20×17.3) | PFR 445 | **MISMATCH** (−99) | CAUTION |
| Yds/rec | 17.3 | PFR 18.5 | close | – |
| Yds/target | n/a | PFR **14.4** (445/31) | our earlier number is correct | PFR |
| Passer rating allowed | 113.1 | PFR **129.4** | **MISMATCH** | CAUTION: both rank him among the worst |
| INT / PBU | 0 / 1 | PFR 0 INT ✓; season PBU not on PFR (FalseFinish W5 box shows 1 PD) | INT ✓, PBU partial | PFF PBU unverified |
| Pressures | 0 | PFR 1 (1 hurry, 4 blitzes) | near | minor |
| Missed tackles | 5 | PFR 7 (26.9%) | MISMATCH | charting differs |
| Solo tackles | 18 | PFR 19 combined | consistent | ✓ |
**Why they differ.** Our 14.4 is *per target*; PFF's 17.3 is *per reception*, so these two are not a conflict. The real gap is attribution: 24 vs 20 catches and 445 vs ~346 yards. PFR and PFF chart coverage responsibility separately. Busts like Watson's 42-yard TD in W5 (SI calls it "a busted coverage") can be pinned on Johnson by one charter and on a safety by the other. Snaps (nflverse) show Johnson played every game, W1–W7 (65/52/50/32/61/46/54), so both sources should cover the same 7 games. A weeks-counted gap is unlikely unless the PFF screenshot predates W7 (Oct 22); I can't verify that without PFF. **Either way he's a weak cover CB.** For quantities use PFR (public, reproducible), and keep the caution flag.

## Kyler Gordon (nickel CB, CHI)
| Metric | PFF | 2nd source | Match? |
|---|---|---|---|
| 2026 snaps | 48 | nflverse def snaps W6 17 + W7 31 = **48** | ✓ |
| Grade 92.1 | as shown | none | CAUTION, and small sample (48 snaps) |
| Coverage | – | PFR 2 tgt, 2 rec, 5 yds; 4 sacks, 4 pressures (2 G) | – |
| Status tonight | active | Not on the Bears.com final injury report → **no designation, active** | ✓ |
**Why so few snaps:** a calf injury kept him out of OTAs, minicamp and camp. His practice window opened Sept 30, and he was activated for W6 on a "pitch count" (NFL.com). In W6 at ATL he had 3 sacks and 2 forced fumbles, and he added a sack in W7 vs NE (USA Today/UW Wire, 4 sacks in 2 games). His snaps rose from 17 to 31, so expect around 35–50 tonight, still likely managed. **Slot:** he is the Bears' nickel (NFL.com: "the nickel cornerback"). Clark Phillips had the slot snaps in W6 before Gordon took over. So Gordon is the most likely slot CB tonight, and he is used heavily as a blitzer. Note also that the Bears' preview says "Simmons" (a newly acquired defender) debuts tonight; his role is unknown. PFF's "Kupp sees Gordon on ~16 snaps" is a projection with no public source to check it.

## Malik Muhammad (CB, CHI; Questionable, toe, LP Thu/Fri/Sat per Bears.com)
PFR line: 7 G / 4 GS, 31 tgt, 17 rec (54.8%), 259 yds, 15.2 Y/rec, **8.4 Y/tgt**, 1 TD, 1 INT, 79.9 rating, 3 missed tackles (12.5%). PFF ranks him 81st of 106: no public grade to check, CAUTION. His snaps fell to 18 in W7 (from 46 in W6) as Gordon returned and Stevenson came back (35).

## PFF team/matchup items
| Item | PFF | 2nd source (nflverse 2026, W1–7) | Match? |
|---|---|---|---|
| Coverage rank 26/32, grade 52.6 (23rd) | as shown | YPT allowed **8.71, 32nd** (worst); EPA/dropback allowed +0.041, 15th | Directionally match (bad); grade is single-source |
| WR receptions allowed rank 4th | 4th | 9.43 WR rec/gm = **5th fewest** | ✓ (within 1) |
| WR receiving yards rank 17th | 17th | 149.4 WR yds/gm = **21st fewest** | near; mismatch of 4 spots, CAUTION |
| Run D grade 49.1 (31st) | 31st | RB YPC allowed 4.33 = **20th** | **MISMATCH**: the public efficiency stat is mid-pack, not 31st. Trust nflverse for yards; PFF grades tackling/run fits (CAUTION) |
| Pass rush 62.7 | as shown | pressure proxy (sacks+hits / dropback) 0.176; FTN blitz 41.4% (#4) | no like-for-like |
| Kupp proj 34.5 yds / 2.7 rec; "L10" 35.6 / 3.3 | – | **2026 only (7 g): 28.4 yds, 2.6 rec, 3.9 tgt**; game log 35, 20, 46, 13, 15, 50, 20 | PFF's L10 reaches into 2025 = **STALE**. Use 2026 |
(Small note: my earlier CHI 8.57 YPT included a different play filter; with sacks and 2-pt tries excluded it is 8.71. Both are bottom-2.)

## Caleb Williams 2026 (ESPN box = nflverse, exact match)
| QB | Weeks | Cmp/Att | Yds | TD | INT | Sacks | YPA |
|---|---|---|---|---|---|---|---|
| **C. Williams** | 1, 2, 6, 7 | **88/124 (71.0%)** | **1,020** | **5** | **1** | **12** | **8.23** |
| C. Keenum | 3, 5 | 35/53 | 355 | 2 | 1 | 2 | 6.70 |
| T. Bagent | 2 (relief), 4, 5 | 42/63 | 409 | 0 | 3 | 4 | 6.49 |
By game, Williams: W1 21/29-269 2TD; W2 15/26-138 1INT (left the game, hamstring); W6 30/36-305 1TD; W7 22/33-308 2TD. He missed 3 games with the hamstring (Bears.com preview), and he's the first QB this season with back-to-back 300-yard, 0-INT starts. **"Green" fits only the backups.** Williams is efficient (8.2 YPA), but he takes sacks (12 in about 3.5 games), which matters against SEA's pressure (0.229 proxy).

## Verdict impact
- **JSN o89.5: still PASS.**
  - Gordon in the slot is the main new risk on JSN's inside snaps, plus Gordon's blitzing adds pressure on Darnold with LT Cross out.
  - Johnson outside is weak on every source (PFR 14.4 Y/tgt, 129.4 rating; PFF 113.1).
  - CHI allows the worst YPT in the league (8.71) and gives up few WR catches but more yards per catch, which fits a yardage-over leg over a receptions leg.
  - Note: JSN was a DNP on Thursday as a rest day (NIR), then full Friday and Saturday (Bears.com list).
  - The PRESS block stays (SRC-3, and now PFF single-source too).
- **Kupp: CUT, reinforced.** His 2026 averages are 28.4 yds / 2.6 rec, Gordon (an elite slot) is back, and PFF's L10 is stale.
- No other changes.
