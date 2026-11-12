```text
GATE: FAIL  run=/workspace/nfl-database/runs/2026-11-05_JAX@BAL_r6/gate_B  checked_at=2026-11-05 19:02 ET
Live legs: ['Henry 40+ rush (o39.5)', 'JAX 1H -6.5', 'Strange 4+ rec (o3.5)', 'Strange 40+ rec yds (o39.5)']
Cut legs: none
RICO NOV 2 RULES (N1-N3):
  - Henry 40+ rush (o39.5): N1 carry share 69% (>= 60%)
  - JAX 1H -6.5: N3 period spread matches script read (JAX)
MISSES (29):
  - leg Henry 40+ rush (o39.5): phases [3, 6, 7, 9, 10, 12, 13, 14, 15] flagged FAIL/MISSING/STALE/UNVERIFIED/HOLD but leg not CUT/HOLD
  - leg Henry 40+ rush (o39.5): has flagged gaps ['MISSING recent_form: fewer than three games with current QB'] but leg not CUT
  - leg Strange 4+ rec (o3.5): phases [4, 9, 12, 15] flagged FAIL/MISSING/STALE/UNVERIFIED/HOLD but leg not CUT/HOLD
  - leg Strange 4+ rec (o3.5): has flagged gaps ['MISSING coverage.man_zone numeric rates', 'MISSING coverage.mof numeric rates', 'MISSING pressure_inputs.time_to_throw'] but leg not CUT
  - leg JAX 1H -6.5: phases [2, 4, 6, 7, 9, 10, 12, 14, 15] flagged FAIL/MISSING/STALE/UNVERIFIED/HOLD but leg not CUT/HOLD
  - leg JAX 1H -6.5: has flagged gaps ['UNVERIFIED monte_carlo pricing for JAX 1H -6.5', 'UNVERIFIED bias pricing for JAX 1H -6.5', 'UNVERIFIED game_randomness pricing for JAX 1H -6.5'] but leg not CUT
  - leg Strange 40+ rec yds (o39.5): phases [2, 4, 9, 12, 14, 15] flagged FAIL/MISSING/STALE/UNVERIFIED/HOLD but leg not CUT/HOLD
  - leg Strange 40+ rec yds (o39.5): has flagged gaps ['MISSING coverage.man_zone numeric rates', 'MISSING coverage.mof numeric rates', 'MISSING pressure_inputs.time_to_throw'] but leg not CUT
  - category ngs gap flagged but legs ['Henry 40+ rush (o39.5)', 'JAX 1H -6.5', 'Strange 4+ rec (o3.5)', 'Strange 40+ rec yds (o39.5)'] not CUT
  - source injuries_news/Jaguars official injury report: STALE (27.4 h old > 6 h limit)
  - source injuries_news/Ravens official injury report: STALE (27.4 h old > 6 h limit)
  - source injuries_news/Jaguars Austin Johnson practice-squad news: STALE (27.4 h old > 6 h limit)
  - source category injuries_news: missing or no fresh source
  - source weather/NWS hourly + Open-Meteo via tools/weather_forecast.py: STALE (27.7 h old > 6 h limit)
  - source category weather: missing or no fresh source
  - source odds_props/Saved r6 FD/DK/Pinnacle odds; no API calls: STALE (28.1 h old > 1 h limit)
  - source category odds_props: missing or no fresh source
  - leg Henry 40+ rush (o39.5): edge-rule inputs missing (need no_vig, line, side, 3 model p)
  - leg JAX 1H -6.5: edge avg(p)-no_vig = -6.9 pts < +3
  - leg JAX 1H -6.5: edge a model p 0.414 < .45
  - leg JAX 1H -6.5: edge sim median 5.0 does not clear over 6.5
  - leg JAX 1H -6.5: edge sim median 4.0 does not clear over 6.5
  - leg JAX 1H -6.5: edge sim median 4.0 does not clear over 6.5
  - leg JAX 1H -6.5: §7 FAIL over 6.5 hit 2 of 4 last games with current QB [10, -7, -3, 28]
  - leg Strange 40+ rec yds (o39.5): edge-rule inputs missing (need no_vig, line, side, 3 model p)
  - Phase 11 weather JAX@BAL: STALE (27.7 h old > 6 h limit)
  - weather forecast: STALE (27.7 h old > 24 h limit) — re-run tools/weather_forecast.py
  - leg Strange 4+ rec (o3.5): N2 no verified primary defender (receiving legs can't go on a slip without one; WR3 team-profile fallback no longer enough)
  - leg Strange 40+ rec yds (o39.5): N2 no verified primary defender (receiving legs can't go on a slip without one; WR3 team-profile fallback no longer enough)
Notes:
  - JAX 1H -6.5: avg p 0.419, no-vig 0.487, raw edge -6.9
  - Strange 4+ rec (o3.5): avg p 0.545, no-vig 0.515, raw edge +3.0
PRESS TIER (on for runs >= 2026-11-02; models_required=2):
  - Strange 4+ rec (o3.5): STANDARD (no press inputs on leg)
  - Strange 40+ rec yds (o39.5): STANDARD (no press inputs on leg)
  - JAX 1H -6.5: STANDARD (no press inputs on leg)
  - Henry 40+ rush (o39.5): STANDARD (no press inputs on leg)
```

# JAX@BAL r6 gate_B

All requested legs remain live for evaluation. Stat/model disagreement is flagged, never an automatic read cut. A failed gate does not authorize a slip.

## Simulations

100,000 per model, fixed seed 20261104. Native player-market engine: tools/sim_v6.py; wrapper: codex/run_sims.py. Fagnano base estimates are the manifest case; rico/flip sensitivities and assumptions are in codex/sims_audit.json.

**JAX 1H is an UNVERIFIED wrapper extension, not a native or calibrated sim_v6 spread model.** No native spread_h1 market exists; its numeric sensitivity must not be treated as approved pricing.

| Leg | Monte Carlo p / median | Bias p / median | Game randomness p / median |
|---|---|---|---|
| Strange 4+ rec (o3.5) | 0.55768 / 4.00 | 0.55784 / 4.00 | 0.51985 / 4.00 |
| Strange 40+ rec yds (o39.5) | 0.52311 / 41.91 | 0.51956 / 40.98 | 0.49598 / 38.92 |
| JAX 1H -6.5 | 0.42173 / 5.00 | 0.42035 / 4.00 | 0.41393 / 4.00 |
| Henry 40+ rush (o39.5) | 0.53654 / 41.83 | 0.53745 / 41.83 | 0.53918 / 41.87 |

## Risks

Hamilton and CB assignments are hypotheses. No verified primary defender; Hamilton suppression is NOT COUNTED per r5 addendum 3. PFR performance does not verify future matchups. Man/zone, MOF and time-to-throw remain MISSING. Pressure/checkdown measures are labelled proxies.

Per-source timestamps and season/data_week are preserved; missing, stale, or incorrectly labelled GROK feeds remain visible to SRC-5. No staleness exceptions applied. Missing opposite-side prices leave Strange yards and Henry no_vig missing. Exact Pinnacle two-way no-vig fractions are used without rounding. No Odds API calls.

Forecast values do not replace the Phase 11 pre-kick weather/inactives recheck. Placed legs are unknown unless supplied. Phase 7 uses gate_adapter recent_form values and is independent of GROK rows.

Missing artifacts: none

## Checklist flags

- Strange 4+ rec (o3.5) phase 4: MISSING — Defender table available but man/zone and MOFO/MOFC unavailable; mapping is conditional on injuries
- Strange 4+ rec (o3.5) phase 9: MISSING — Route screenshots exist for Strange/Washington/Meyers; no verified numeric NGS separation/cushion/YAC-over-expected or Henry RYOE/box rate, no original screenshot pull timestamp. Pbp proxy cannot substitute.
- Strange 4+ rec (o3.5) phase 12: MISSING — Source audit incomplete: NGS numeric data, shell rates, final inactives and full quantitative 1H model absent. Odds 14:59 ET preserved; no new API call.
- Strange 4+ rec (o3.5) phase 15: MISSING — Pre-kick inactive/price/weather and placed-ticket audit unavailable. Slip B has two Strange stats: correlated same-player exposure; no joint probability supplied. No ticket approval inferred.
- Strange 40+ rec yds (o39.5) phase 2: FAIL — last4 targets [8, 8, 7, 2]; 4+ targets each last three; historical volume flag, not a read cut
- Strange 40+ rec yds (o39.5) phase 4: MISSING — Defender table available but man/zone and MOFO/MOFC unavailable; mapping is conditional on injuries
- Strange 40+ rec yds (o39.5) phase 9: MISSING — Route screenshots exist for Strange/Washington/Meyers; no verified numeric NGS separation/cushion/YAC-over-expected or Henry RYOE/box rate, no original screenshot pull timestamp. Pbp proxy cannot substitute.
- Strange 40+ rec yds (o39.5) phase 12: MISSING — Source audit incomplete: NGS numeric data, shell rates, final inactives and full quantitative 1H model absent. Odds 14:59 ET preserved; no new API call.
- Strange 40+ rec yds (o39.5) phase 14: MISSING — p=[0.52311, 0.51956, 0.49598]; medians=[41.91376939072847, 40.98235229315673, 38.92401753013751]; two-way no-vig at exact alt rung missing
- Strange 40+ rec yds (o39.5) phase 15: MISSING — Pre-kick inactive/price/weather and placed-ticket audit unavailable. Slip B has two Strange stats: correlated same-player exposure; no joint probability supplied. No ticket approval inferred.
- JAX 1H -6.5 phase 2: MISSING — No sourced first-half possession/opportunity projection; full-game BAL drive estimates are not 1H opportunities
- JAX 1H -6.5 phase 4: MISSING — Defender table available but man/zone and MOFO/MOFC unavailable; mapping is conditional on injuries
- JAX 1H -6.5 phase 6: MISSING — Fagnano confirmed starter, but only one relief game; no three-game current-QB baseline. Run/script thesis remains a hypothesis.
- JAX 1H -6.5 phase 7: FAIL — 2/4 [10, -7, -3, 28]; current QB T.Lawrence; flag only, no auto-cut
- JAX 1H -6.5 phase 9: MISSING — Route screenshots exist for Strange/Washington/Meyers; no verified numeric NGS separation/cushion/YAC-over-expected or Henry RYOE/box rate, no original screenshot pull timestamp. Pbp proxy cannot substitute.
- JAX 1H -6.5 phase 10: MISSING — Five official NFL videos downloaded and metadata/captions verified; no rigorous caption-to-pbp play-ID mapping yet. Retrieval fulfilled, formal phase10 remains incomplete.
- JAX 1H -6.5 phase 12: MISSING — Source audit incomplete: NGS numeric data, shell rates, final inactives and full quantitative 1H model absent. Odds 14:59 ET preserved; no new API call.
- JAX 1H -6.5 phase 14: MISSING — p=[0.42173, 0.42035, 0.41393]; medians=[5.0, 4.0, 4.0]; wrapper flags unverified extension, not native sim_v6 spread_h1; flag against read
- JAX 1H -6.5 phase 15: MISSING — Pre-kick inactive/price/weather and placed-ticket audit unavailable. Slip B has two Strange stats: correlated same-player exposure; no joint probability supplied. No ticket approval inferred.
- Henry 40+ rush (o39.5) phase 3: FAIL — JAX RB run defense 3.28 YPC / 123 carries opposes rush over; original read was Henry UNDER. Flag only.
- Henry 40+ rush (o39.5) phase 6: MISSING — Fagnano confirmed starter, but only one relief game; no three-game current-QB baseline. Run/script thesis remains a hypothesis.
- Henry 40+ rush (o39.5) phase 7: FAIL — 1/1 [53]; current QB J.Fagnano; flag only, no auto-cut
- Henry 40+ rush (o39.5) phase 9: MISSING — Route screenshots exist for Strange/Washington/Meyers; no verified numeric NGS separation/cushion/YAC-over-expected or Henry RYOE/box rate, no original screenshot pull timestamp. Pbp proxy cannot substitute.
- Henry 40+ rush (o39.5) phase 10: MISSING — Five official NFL videos downloaded and metadata/captions verified; no rigorous caption-to-pbp play-ID mapping yet. Retrieval fulfilled, formal phase10 remains incomplete.
- Henry 40+ rush (o39.5) phase 12: MISSING — Source audit incomplete: NGS numeric data, shell rates, final inactives and full quantitative 1H model absent. Odds 14:59 ET preserved; no new API call.
- Henry 40+ rush (o39.5) phase 13: FAIL — Henry over conflicts with original trailing/run-volume read; low rung may coexist through early carries. Game-script disagreement flagged, not a cut.
- Henry 40+ rush (o39.5) phase 14: MISSING — p=[0.53654, 0.53745, 0.53918]; medians=[41.828373096152276, 41.828373096152276, 41.86901016159314]; two-way no-vig at exact alt rung missing
- Henry 40+ rush (o39.5) phase 15: MISSING — Pre-kick inactive/price/weather and placed-ticket audit unavailable. Slip B has two Strange stats: correlated same-player exposure; no joint probability supplied. No ticket approval inferred.
