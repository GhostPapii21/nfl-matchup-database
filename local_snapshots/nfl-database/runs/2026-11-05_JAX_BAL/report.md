# Projection report — TNF Jacksonville @ Baltimore, Thu 2026-11-05 8:15 PM ET (2026 week 9)

## Gate output (tools/run_gate.py, pasted verbatim)
```
GATE: FAIL  run=/workspace/nfl-database/runs/2026-11-05_JAX_BAL  checked_at=2026-11-05 16:57 ET
Live legs: ['Lawrence rush yds U12.5']
Cut legs: ['BAL team total U13.5', 'Flowers rec U4.5', 'Game total U39.5', 'Henry rush yds U71.5', 'JAX -9.5', 'JAX 1H -6.5', 'Meyers rec yds U38.5', 'Strange 4+ rec (O3.5)', 'Strange rec yds O32.5', 'Tuten rush yds O (no line)', 'Washington rec yds O60.5']
WEATHER ALERT: JAX@BAL flagged (precip 76%). User's placed legs in this game:
  - none found
WEATHER FORECAST ALERT: JAX@BAL kickoff 2026-11-05T20:15 forecast precip 75% (pulled 2026-11-05T16:43 ET). Rushing overs first; live wx-sensitive overs: none
GAME SCRIPT: JAX@BAL triggered (spread -9.5, opp YPC 3.749, wx True); boost lead x1.0727 rb2 x1.1099; RB2 Chris Rodriguez Jr. medians {'mc': 23.230141315296436, 'bias': 23.230141315296436, 'gr': 22.882640189757257}
SHARP coverage confirmed by StatRankings CoverageIQ team pages BAL/JAX
MISSES (1):
  - leg Lawrence rush yds U12.5: phases [15] flagged FAIL/MISSING/STALE/UNVERIFIED/HOLD but leg not CUT/HOLD
Notes:
  - Lawrence rush yds U12.5: avg p 0.638, no-vig 0.500, raw edge +13.8
  - cross-check (pick-side only, not a gated source): PFF matchup tool projected defender snaps (alignment only, Nov 3) pulled 2026-11-03T19:23
  - cross-check (pick-side only, not a gated source): Outlier props TNF (read-only) pulled 2026-11-05T10:14
PRESS TIER (on for runs >= 2026-11-02; models_required=2):
  - Lawrence rush yds U12.5: STANDARD (no press inputs on leg)
```

**Header.** Run dir `runs/2026-11-05_JAX_BAL` · read: r2 locked read + `read_addendum5_2026-11-05.md` (sha256 `590b5c875e84a251375e5d2358b6b541c95baedb114a49f1326be5307daec9ba`, hashed pre-kick) · odds file `odds_r1_1650.csv` · Market: JAX -9.5 FD (-10 DK/Pinnacle), total 39.5, BAL TT 13.5, 1H JAX -6.5 · QBs: Lawrence vs undrafted rookie Fagnano (Lamar out, Huntley IR) · Weather: open air, NWS 76% rain 8-9 PM, wind ≤5 mph → WEATHER FLAG. Read-only run: no bets placed, Outlier read only.

## Phases (counts across all legs)
| Phase | PASS | FAIL | MISSING | UNVERIFIED | HOLD | N/A |
|---|---|---|---|---|---|---|
| 1 Data pull | 12 | 0 | 0 | 0 | 0 | 0 |
| 2 Opportunity | 6 | 1 | 1 | 0 | 0 | 4 |
| 3 Defensive profile | 12 | 0 | 0 | 0 | 0 | 0 |
| 4 Defender coverage | 4 | 0 | 1 | 0 | 0 | 7 |
| 5 Pressure/blitz | 12 | 0 | 0 | 0 | 0 | 0 |
| 6 QB grade card | 9 | 3 | 0 | 0 | 0 | 0 |
| 7 Role/RB rules + §7 | 4 | 2 | 2 | 0 | 0 | 4 |
| 8 Injuries | 11 | 1 | 0 | 0 | 0 | 0 |
| 9 Next Gen Stats | 12 | 0 | 0 | 0 | 0 | 0 |
| 10 Film | 6 | 0 | 0 | 6 | 0 | 0 |
| 11 Environment | 9 | 3 | 0 | 0 | 0 | 0 |
| 12 Source audit | 12 | 0 | 0 | 0 | 0 | 0 |
| 13 Game script/10G | 12 | 0 | 0 | 0 | 0 | 0 |
| 14 Models/price/edge | 5 | 2 | 5 | 0 | 0 | 0 |
| 15 Inactives | 0 | 0 | 0 | 0 | 1 | 11 |

## Sources by category (tool, ET pull time, data week)
- **core_stats_pbp**: nflverse play_by_play_2026 (thru MNF wk8) (curl (nflverse release, 10 AM routine reuse), 2026-11-05 06:07, wk8); ESPN depth charts JAX/BAL (curl, 2026-11-05 16:43, wk9)
- **coverage_matchups**: Sharp Football coverage schemes (man/zone, MOF) (firecrawl, 2026-11-05 16:42, wk8); StatRankings CoverageIQ BAL/JAX (firecrawl, 2026-11-05 16:42, wk8); PFR advanced defense (per-defender) cache (existing PFR extraction (live 403 Nov 5; cache), 2026-11-04 07:05, wk8); FTN charting via nflverse (blitzers/rushers) (curl (nflverse release), 2026-11-05 06:07, wk8)
- **ngs**: nflverse Next Gen Stats passing/receiving/rushing (curl, 2026-11-05 16:43, wk8)
- **film**: Official NFL YouTube highlights (captions matched to pbp) (yt-dlp metadata+captions, 2026-11-05 16:48, wk8)
- **injuries_news**: ESPN injuries API (curl, 2026-11-05 16:43, wk9)
- **weather**: NWS hourly forecast (api.weather.gov) M&T Bank Stadium (curl, 2026-11-05 16:52, wk9); tools/weather_forecast.py (NWS + Open-Meteo) (tools/weather_forecast.py, 2026-11-05 16:43, wk9)
- **odds_props**: The Odds API event odds FD/DK/Pinnacle (urllib (pull_odds_tnf.py), 2026-11-05 16:49, wk9)
- **MISSING / backups:** none at category level. Leg-level: PFR live 403 → Nov 4 07:05 ET PFR cache for BAL defenders; FTN has no man/zone (Sharp+StatRankings used); pressure = PROXY (FTN blitz + sack/hit), PFF pressure splits paywalled; JAX per-defender table not built (Flowers leg already cut). Pick-side cross-checks only: PFF matchup tool (Nov 3), Outlier 10:14 ET.
- **Film (official NFL YouTube):** https://www.youtube.com/watch?v=SQT1S7J4s-o, https://www.youtube.com/watch?v=WXw2IIj01Sg, https://www.youtube.com/watch?v=R7zUguz0Aag, https://www.youtube.com/watch?v=3xMS3qL2KwY — caption-to-pbp matches in film_verified.json.

## Models
Each model ran n = 100,000 with seed 20261101 via tools/sim_v6.py (code sha 1c81119e879a; SIMV6_SRC = nflverse pbp pulled 06:07 ET). sim_v5 not used. Unit tests `test_sim_v6 test_run_gate` passed before the run. Bias multipliers == MC (BIASDUP, see BUGLOG): Bias is not independent of MC. Sandbox refit on today's pbp changed no leg status (BUGLOG NOTE-REFIT).

| Leg | Status | FD line/price | No-vig (FD) | Pinnacle no-vig | MC p / med | Bias p / med | GR p / med | Avg edge |
|---|---|---|---|---|---|---|---|---|
| Lawrence rush yds U12.5 | PASS | 12.5 -113 | 0.5 | 0.5 | 0.636 / 8.0 | 0.640 / 8.0 | 0.638 / 8.2 | +13.8 |
| Henry rush yds U71.5 | CUT | 71.5 -113 | 0.5 | None | 0.763 / 53.7 | 0.761 / 53.7 | 0.738 / 54.0 | +25.4 |
| Meyers rec yds U38.5 | CUT | 38.5 -113 | 0.5 | 0.49031841652323577 | 0.466 / 41.5 | 0.466 / 41.5 | 0.492 / 40.3 | -2.5 |
| Strange rec yds O32.5 | CUT | 32.5 -113 | 0.5 | 0.5021645958699511 | 0.622 / 41.0 | 0.621 / 41.9 | 0.574 / 38.9 | +10.5 |
| Strange 4+ rec (O3.5) | CUT | 3.5 +102 | 0.462 | 0.5 | 0.562 / 4.0 | 0.562 / 4.0 | 0.526 / 4.0 | +8.8 |
| Washington rec yds O60.5 | CUT | 60.5 -113 | 0.5 | None | 0.455 / 54.9 | 0.453 / 54.9 | 0.446 / 54.1 | -4.8 |
| Flowers rec U4.5 | CUT | 4.5 -114 | 0.5 | 0.4956702459300312 | 0.262 / 6.0 | 0.264 / 6.0 | 0.287 / 6.0 | -22.9 |
| Tuten rush yds O (no line) | CUT | no line | None | None | n/a | n/a | n/a | n/a |
| JAX -9.5 | CUT | -9.5 -120 | None | None | n/a | n/a | n/a | n/a |
| Game total U39.5 | CUT | 39.5 -110 | 0.5 | 0.4931277775232511 | n/a | n/a | n/a | n/a |
| BAL team total U13.5 | CUT | 13.5 -108 | 0.49 | None | n/a | n/a | n/a | n/a |
| JAX 1H -6.5 | CUT | -6.5 -105 | None | None | n/a | n/a | n/a | n/a |

## Legs (live after gate)
- **Lawrence rush yds U12.5** — FD 12.5 -113 (Pinnacle 12.5 -110/-110, DK 11.5). Independent model: avg p 0.638 vs no-vig .500 → raw edge +13.8 (tier flag only: ≥+3 'full'). Medians 8.0/8.0/8.2 all under 12.5. §7 [2,25,12,10] = 3/4 under, last 2 under.
  - Market-informed view (kept separate): Pinnacle and FD both de-vig to 50.0% at 12.5; FD alt over 9.5 at -180 (64.3% vig-in) vs model P(10+) ≈ .44. The market prices more Lawrence rushing than our model does → MARKET_GAP flag. A 50/50 blend of model and Pinnacle would be ≈ .57 (+7), still positive but this is shown for context only (no shrink rule).
  - Flags: SCRAMBLE_CONFLICT: BAL allows 7.3% scramble rate vs 4.8% league; own-rate projection 11.0 but opp-adjusted 14.8 > 12.5 (flag, not a cut; Rico Nov 4 6:17 AM); build/lawrence_opp.json; MARKET_GAP: FD alt over 9.5 at -180 = 64.3% vig-in (one-sided alt) vs sim P(10+) .445/.440/.440 (build/law_alt_out.json); independent model and market-informed view kept separate
  - Scenario read (addendum5): JAX leads, rain + 9.5 spread → run-heavy JAX second half, late kneels; Lawrence has 9 scrambles in 220 dropbacks (4.1%). Own-rate projection 11.0 vs BAL-adjusted 14.8 (BAL allows 7.3% scrambles, 34% blitz) — the conflict is flagged to Rico, not used to drop the read (Rico Nov 4 6:17 AM). QB card: vs-blitz C, no-blitz A, protection D, money C, clutch A (no gate trips on an under). Note: addendum5 quoted 10.7 / 14.2 from an earlier scratch calc; the reproducible recompute in build/lawrence_opp.json gives 11.0 / 14.8 (6 JAX kneels, not 3) — same conclusion, both numbers flagged.

## Cuts
- **Henry rush yds U71.5**: §7 MISSING: only 1 game with current QB Fagnano (need 3 of 3 or 3 of 4); P14 MODEL-SUSPECT: all 3 sim medians ~54 vs line 71.5 (17+ yds off the market main) · mirror: every Henry over rung also fails §7 (1 game with Fagnano); rain + run-first BAL plan is the Flip B risk to the under
- **Meyers rec yds U38.5**: P14 edge -2.5 pts < +3; P14 median does not clear ([41.5, 41.5, 40.28] vs 38.5) · mirror: mirror over is a receiving OVER in a weather-flagged game (stop)
- **Strange rec yds O32.5**: Phase 11 WEATHER FORECAST + NWS: precip 75% in the game window (open air) - receiving OVER must be CUT (stop, no mirror)
- **Strange 4+ rec (O3.5)**: Phase 11 WEATHER FORECAST + NWS: precip 75% in the game window (open air) - receiving OVER must be CUT (stop, no mirror)
- **Washington rec yds O60.5**: Phase 11 WEATHER FORECAST + NWS: precip 75% in the game window (open air) - receiving OVER must be CUT (stop, no mirror)
- **Flowers rec U4.5**: §7 MISSING: only 1 game with current QB Fagnano; sims built on Lamar/Huntley-era BAL targets (QB-RETURN-type flag; model on wrong QB) · mirror: mirror over is a receiving OVER in a weather-flagged game (stop)
- **Tuten rush yds O (no line)**: NOLINE: no FanDuel/DK/Pinnacle rush line posted (Q, DNP all week); Phase 7: 60%+ carry share in only 2 of last 4 (74,100,52,57%)
- **JAX -9.5**: P14 MISSING: tools/sim_v6.py has no game-line (spread/total/team-total/period) model - 3 model p unavailable
- **Game total U39.5**: P14 MISSING: tools/sim_v6.py has no game-line (spread/total/team-total/period) model - 3 model p unavailable · mirror: no game-line model in sim_v6: the over 39.5 is equally unpriced (P14 MISSING); code note to Ghost6
- **BAL team total U13.5**: P14 MISSING: tools/sim_v6.py has no game-line (spread/total/team-total/period) model - 3 model p unavailable · mirror: no game-line model in sim_v6: BAL TT over 13.5 equally unpriced (P14 MISSING); code note to Ghost6
- **JAX 1H -6.5**: P14 MISSING: tools/sim_v6.py has no game-line (spread/total/team-total/period) model - 3 model p unavailable

## Rico flags for review (not cuts)
- **Henry rush U71.5** (edge player #1 in the locked read; the one backtested edge class) is cut only because §7 needs 3 games with Fagnano (has 1). Models .76/.76/.74 vs .500 no-vig, medians ~54 — MODEL-SUSPECT: 18 yards under the market median; the model has no Fagnano-era volume. Pinnacle 68.5 (-123/+102). Rico could override via the door's logged-override path; Grok Bot did not.
- **Tuten** Q (ankle/foot), no book line posted; if active at inactives, the wx/script-boosted rush over (median ~61.6) still fails the 60%-carry rule in 2 of last 4 and has no price.
- **Strange / Washington overs** (on the 12:35 PM proposed slips) are now weather-cut (NWS 76% in the window).

## Risks / pre-mortem
- Lawrence U12.5 loses if BAL's 34% blitz flushes him (BAL allows 7.3% scramble rate) and 1-2 scrambles go 10+ (wk5: 16-yd 3rd-down scramble). One-run variance on a 12.5 line is large (p90 ≈ 23).
- Flip A (slog, rain) helps; Flip B (BAL keeps it close with Henry in the rain) means more JAX dropbacks in late downs → more scramble chances.
- Market disagrees (FD alt 9.5 at -180). If the line moves to 11.5 or lower before kick, edge shrinks; CLV tracked from 12.5 -113.
- Data risks: pressure is PROXY; Bias==MC (2 independent models); no game-line model; Fagnano sample = 1 game.

## CLV
Opening reference for CLV: FD 12.5 -113/-113 at 2026-11-05 16:49 ET. Close to be graded from the final pre-kick pull.
