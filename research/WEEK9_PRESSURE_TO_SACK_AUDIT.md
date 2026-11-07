# WEEK9 Pressure-to-Sack Audit (Weeks 1–8)

**As of:** 2026-11-07 ~11:53 ET
**Status:** Research evidence only. No model or code changes. Model NOT READY.
**Retrieval date:** 2026-11-07.

## Definitions (kept separate)
- **Blitz:** Extra rusher beyond base four (source-defined).
- **Pressure:** Charted pressure (hurry, hit, or sack) where the source provides it. Not inferred from hits alone.
- **QB Hit:** Official or charted hit on the quarterback.
- **Sack:** Official sack.
- **Pressure-to-sack rate:** Sacks / charted pressures (not sacks / (sacks + hits)).
- **Sack rate per dropback:** Sacks / dropbacks.
- Events are kept separate. No proxy substitution where charted pressure is missing.

## Sources checked

### 1. Pro-Football-Reference Advanced Passing 2026 (through Week 8)
- **URL:** https://www.pro-football-reference.com/years/2026/advanced.htm
- **Available fields (team-level, offense faced):** Bltz, Hrry, Hits, Prss, Prss%, Sk, PktTime, Scrm.
- **What it provides:** Team-level blitz count, pressure count (Prss), pressure rate (Prss%), hits, sacks.
- **Limitation:** Prss appears to be a composite; it is not confirmed as full charted pressure with blitz/no-blitz splits. No defender-level pressure charting. No explicit pressure-on-blitz vs pressure-without-blitz split.
- **Usable:** Sack rate per dropback (Sk / Att) can be approximated; pressure-to-sack cannot be computed cleanly because the pressure denominator is not fully charted with the required splits.

### 2. Muffed.ai / FTN via nflverse (public)
- **URL example:** https://muffed.ai/stats/defense-blitz-rate
- **Available:** Team blitz rate with denominators (Blitzes / DB) for all 32 teams. Example: MIN 72.8% (171/235), WAS 43.6% (126/289).
- **Source note:** Verified play-level charting from FTN Data via nflverse.
- **Missing:** Pressure rate on blitzes, pressure rate without blitzes, charted pressure counts, sack rate per pressure.

### 3. Sharp Football Analysis Defensive Tendencies (updated 2026-11-03)
- **URL:** https://www.sharpfootballanalysis.com/stats-nfl/nfl-defensive-tendencies/
- **Available:** Team blitz rate for all 32 teams (e.g., MIN 69.8, WAS 40.3).
- **Missing:** Pressure splits, charted pressure denominator, sack rates.

### 4. PFF charted pressure (restricted)
- PFF publishes pressure rates, pressure-to-sack rates, and blitz/pressure splits in premium content and data viz tools.
- Free public pages show example pressure rates (e.g., early-season QB pressure rates) but do not provide a complete Weeks 1–8 team or defender export with the required splits.
- **Flag:** Charted pressure with blitz/no-blitz splits and pressure-to-sack conversion is **unavailable** from free sources. Rates left unavailable rather than substituting a proxy.

## Requested rates — availability summary
| Rate | Denominator | Available free? | Source if available | Notes |
|------|-------------|-----------------|---------------------|-------|
| Blitz rate | Dropbacks | Yes (team) | Muffed/FTN, Sharp Football | With counts |
| Pressure rate on blitzes | Blitzed dropbacks | No | — | Charted pressure split unavailable free |
| Pressure rate without blitzes | Non-blitz dropbacks | No | — | Charted pressure split unavailable free |
| Sack rate per pressure | Charted pressures | No | — | Not computed from sacks/(sacks+hits) |
| Sack rate per dropback | Dropbacks | Partial | PFR Sk / Att | Official sacks only |

## Uncertainty
- Blitz rates vary slightly by source (Muffed vs Sharp) due to definition differences; both are reported with denominators where available.
- PFR Prss% is not used as a substitute for charted pressure-to-sack.
- No defender-level pressure charting available free for all 32 teams.
- Small-sample warning applies to any weekly splits.

## What remains unavailable
- Charted pressure counts with blitz/no-blitz splits for all 32 teams.
- Pressure rate on blitzes and without blitzes.
- Sack rate per charted pressure.
- Defender-level pressure-to-sack data.

**Rules followed:** Blitz, pressure, QB hit, and sack kept as separate events. No proxy used for missing charted pressure. No model or code changes.
