# Screenshot quote correction — JAX@BAL period markets
**Logged:** 2026-11-05 ~12:54 America/New_York  
**Source:** Rico user screenshots (FanDuel SGP UI), **not** Odds API / live feed.  
**Refs:** `screenshots_quote_ref/` (sha256 = filename without .png)  
**Prior error corrected:** Odds API `NO_QUOTE` for JAX 1H −2.5 meant **feed absence**, not that FanDuel lacked the market.

## Verified from screenshots (phone clock 12:50–12:51)

| Market | Settlement note | Quote |
|---|---|---|
| 1H Winner 3-way | Standalone HT result; tie is a ticket | JAX **−280** · Tie **+950** · BAL **+310** |
| 1H main spread | Cumulative HT margin | JAX **−6.5 (−105)** · BAL **+6.5 (−115)** |
| 1H alt −6.5 snapshot | Same market, alt ladder variation | JAX −6.5 **−108** · BAL +6.5 **−118** |
| 1H alt −0.5 | Cumulative | JAX **−0.5 (−290)** |
| 1H alt −2.5 | Cumulative (API had NO_QUOTE) | JAX **−2.5 (−235)** · BAL **+2.5 (+180)** |
| Q1 Winner 3-way | Q1-only points | JAX **−150** · Tie **+320** · BAL **+270** |
| Q1 spread | Q1-only margin | JAX **−2.5 (−124)** · BAL **+2.5 (+102)** |
| Q2 Winner 3-way | Q2-only points | JAX **−200** · Tie **+550** · BAL **+260** |
| Q2 spread | Q2-only margin | JAX **−3.5 (−106)** · BAL **+3.5 (−116)** |
| Q3 Winner 3-way | Q3-only; BAL cut off in shot | JAX **−145** · Tie **+330** · BAL **(not shown)** |

Also visible (context, not requested): 1H total 20.5 O+110/U−130; Q1 total 7.5 O+116/U−142; Q2 total 12.5 O−116/U−106.

## Rules for later pricing
- Screenshot = valid **quote evidence** (`football-period-game-flow` §1); not edge proof.
- Prefer matching opposing outcomes for no-vig; one-sided alt alone stays vig-in.
- Do not treat Odds API gaps as “market does not exist” when a dated screenshot shows it.

## Append — team totals (Rico screenshots ~1:07 window / same TNF board)
| Market | Quote | Note |
|---|---|---|
| BAL TT 14.5 | Under **−132** / Over **+104** | Screenshot; not Odds API |
| BAL TT 13.5 | Under **−108** / Over **−118** | Matches earlier live FD pull |
| JAX TT 24.5 | Over **−115** / Under **−111** | Screenshot |

Still not Pinnacle. FD screenshot ≠ `pinnacle_novig_p`.
