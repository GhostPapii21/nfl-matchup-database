# Feature execution matrix — pass 2 (2026-11-05 ET)
EXECUTED = changes sampled events in simulate_games / as-of / period grading. ADAPTER = input gate/metadata only.

| Feature | Status | Source | Evidence |
|---|---|---|---|
| Team empirical snap resampling (down×dist×yl, coarse fallbacks) | EXECUTED | nflverse PBP 2026 W1–8 | per-snap coarse 8.3% (data_only) |
| FTN blitz strata on CALLED passes only | EXECUTED (data_only, script_adjusted) | local free FTN charting n_blitzers, join 98.3% | 17,574 events/300 sims; run/pass never altered (tests) |
| Defense blitz rate (opponent) | EXECUTED | FTN joined over involvement games, n≥20 passes | provenance.defense_blitz_rates |
| 4th-down decision by field-position×distance cell | EXECUTED | team 4th-down rows | COARSE_4TH_* / SPARSE_4TH flags |
| FG make by kick distance (±5/±10/team) + spot-of-kick miss | EXECUTED | team FG rows kick_distance | tests |
| Punt net = kick−return; touchback→own 20 | EXECUTED | kick_distance/return_yards/touchback | tests |
| Empirical clock medians | EXECUTED (partial) | PBP game_seconds deltas | not situational (no timeouts/hurry-up) |
| H2H DEF_COND | EXECUTED but 0 uses for JAX–BAL | no H2H rows W1–8 | def_interaction_events=0 |
| Opponent-allowed defense mixture | EXECUTED in research variant only | other offenses vs defense, prior weeks | weight 0.5 = STRUCTURAL_ASSUMPTION not fitted; 17,897 events; did not improve grades |
| Player outputs (per-sim joint samples) | EXECUTED | sampled rows | foreign rows give no credit; TD credit capped at distance |
| QB forward filter | EXECUTED in script_adjusted only | config adjustments | |
| Market conditioning (Bias/GR/Pinnacle) | NOT WIRED | — | market_informed config documents only; no fake integration |
| True pressure / man-zone / coverage / routes | ADAPTER ONLY | 2026 participation unpublished (nflverse posts after postseason; local 2026 files are "Not Found" stubs) | 2025 participation descriptive only: JAX def pressure 27.9% man 25.4% (n=792); BAL 28.1% / 32.9% (n=726) — NOT executed |
| CB/S/DT replacement coefficients | MISSING | no authorized measured source | not invented |
| Weather | METADATA ONLY | NWS gridpoints/LWX/109,90 hourly (pulled 18:22 ET) | 8–11 PM ET: 66–67°F, S 3–5 mph, PoP 52–76%, showers/thunderstorms; quantitative_modifier=None |
