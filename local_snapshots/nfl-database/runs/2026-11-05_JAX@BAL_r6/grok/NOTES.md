# GROK verification notes
Start: 2026-11-04 15:20 ET. End: 2026-11-04 15:37 ET (see individual artifact pulled_et for exact retrieval/inspection minute).

Read CONTRACT first, then gate documentation, gate implementation, adapter leg definitions, shared assembly logic, CHI@SEA template, r2 locked read and r3-r5 reports/addenda, usage/pressure/defender files, injury sweep, drive simulation source/output and 1H miss audit. Used cloud-environment runtime skill; environment_status tool and local network-policy snapshot were unavailable. Public HTTP calls succeeded through existing environment configuration.

## Delivered
- checklist_rows.json: 70 rows, phases 1-6 and 8-15 for all five exact leg names. Statistical disagreements are explicit flags, not instructions to cut the read. Phase 7 is the other agent's assignment.
- sources.json: coverage, NGS gap, film, refreshed public team injuries/news, NWS/Open-Meteo weather and target-share evidence. Actual ESPN scheduling is Week 9; week10 is the existing folder label. Pbp data are through Week 8.
- weather_forecast.json: actually called tools/weather_forecast.py for 39.278,-76.623 (M&T Bank Stadium), kickoff Nov 5 20:15 ET; saved its native output. Combined game-window maxima: precip 25%, gust 9.2 mph, sustained 3 mph. No weather flag. NWS gust missing; Open-Meteo supplies gust. Forecast is not a pre-kick observation.
- target_share_pool.json: recomputed from r2 nflverse parquet, 195 named JAX targets. Washington 48/195, last-three current-QB-week window 22/96, weeks 5,6,8. Listed every JAX targeted player, including below-threshold players with skip reasons. Exact fractions retained rather than copying rounded ~24.5 claims. Conditional skip reasons support the user-defined different slips.
- film_index.md, film_verified.json, film_play_matches.json, film_probe.json and logs: all URLs came from requested yt-dlp search command then full metadata. Five actual MP4 downloads, official NFL channel ID UCDVYQ4Zhbm3S2dlz7P1GBDg, each independently ffprobe-confirmed 1280x720. Saved info JSON and auto-captions alongside films. Targets cover BUF relief, two preseason TDs, BAL defense vs BUF/CIN slot/TE, and latest JAX first-half passing. Caption-to-pbp matches: Strange Q2 11:33 nine yards (play 1151), Washington Q2 3:57 sixteen yards/QB hit (play 1711). No private API or NFL Pro.
- injury_refresh.json and saved official HTML/text: actual public pulls today. Both official team tables show three practice columns: Hawkins/Jackson/Huntley OUT, Wiggins QUESTIONABLE, Fagnano FP, Jenkins/Rosengarten/Simpson FP/no designation, Tuten QUESTIONABLE/DNP, Meyers LP/UNSPECIFIED. Preserve UNSPECIFIED verbatim. Jaguars Nov 3 news explicitly puts Austin Johnson on practice squad; he is distinct from Antonio Johnson, safety with ankle issue. No Austin injury designation found. Team pages supersede stale Tuesday/addendum assumptions; saved HTML permits inspection.
- n3_1h_script.json/.md: sourced base/flip script, full-game BAL estimate scenarios and exact historical first-half margins; no unsupported probability. The drive sim is explicitly ESTIMATES and is not a quantitative first-half cover model.

## Remaining MISSING / limits
- Real numeric NGS separation/cushion/YAC-over-expected, time-to-throw and Henry RYOE/box rate. Existing route screenshots were inspected but their original pull time is unknown; sources entry is explicitly MISSING and cannot count as fresh numeric NGS. Pbp location proxies are not NGS/alignment.
- Man/zone and MOFO/MOFC; conditional defender mapping lacks actual alignment. PFR defender table is real but cannot fill shells.
- Native, validated quantitative JAX/BAL 1H model. The other agent's sims file labels the half extension UNVERIFIED; its numbers are recorded as flags, never elevated into sourced truth or an N3 probability.
- Exact-alt two-way no-vig for Strange 40+ and Henry 40+ remains absent in adapter; no guessed no-vig. Henry is a very short-price flag. No Odds API calls made.
- Final pre-kick inactives, fresh price/weather and placed-ticket audit. Slip B contains two Strange stats; no joint probability or ticket approval inferred.
- Film highlights omit failed plays. Only Strange and Washington phase10 have unique caption/pbp mappings; Henry/1H formal phase10 remain MISSING rather than pretending full play-level validation. Auto-captions misspell Fagnano/Strange; original text and context retained.

Validation: parsed every output JSON; asserted five legs and all 14 required phases, allowed statuses, nonempty source and ET-naive timestamps. Verified five real downloaded films and actual video stream height <=720 using ffprobe. Did not rerun/modify shared assembly or gate folders, did not touch codex/ or assemble.py, and did not commit. Prior grok_cli_attempt1 was not used as evidence.

## Superpowers review corrections (2026-11-04)

Offline rebuild preserves the original injury/news inspection time instead of restamping saved HTML as a fresh pull. Target-pool provenance uses the underlying pbp pull time. Film availability is checked before crediting downloaded-film evidence. N3 now exports the sourced qualitative JAX first-half read; its quantitative status remains MISSING. Henry's opportunity row reflects 11/16 carries in the one current-QB game. Phase 14 uses exact saved two-way no-vig fractions. See review_superpowers.md.
