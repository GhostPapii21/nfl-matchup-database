# Checklist: MNF CHI@SEA r3 (2026-11-02, kickoff 8:15 PM ET)

Inputs pulled 16:38 ET (odds, injuries, weather, pbp); coverage 05:09 ET; PFR 05:10/06:40 ET. All times ET.

## Summary
- Legs evaluated: 23. PASS: 0. CUT: 23. MANUAL_REVIEW: 0 (JSN O89.5 would be manual review but is barred by the open JSN 70+ ticket).
- Phase 1 sample: FAIL 1, PASS 22
- Phase 2 opportunity: FAIL 3, PASS 20
- Phase 3 defense profile: FAIL 3, PASS 20
- Phase 4 defender: PASS 17, UNVERIFIED 6
- Phase 5 blitz/pressure: PASS 23
- Phase 6 QB: PASS 23
- Phase 7 role/snaps: FAIL 13, PASS 10
- Phase 8 injuries: FAIL 1, PASS 22
- Phase 9 NGS: PASS 23
- Phase 10 film: PASS 17, UNVERIFIED 6
- Phase 11 weather: PASS 23
- Phase 12 market/price: PASS 23
- Phase 13 game script: FAIL 6, PASS 17
- Phase 14 edge/sims: FAIL 13, PASS 10
- Phase 15 correlation/ticket bar: FAIL 10, PASS 13

| Leg | Phase | Status | Number | Source | Pulled (ET) |
|---|---|---|---|---|---|
| Caleb Williams Pass Yds Over 224.5 | 1 sample | PASS | 4 games w/ current QB C.Williams; season sample through Wk8 | nflverse pbp (src/play_by_play_2026.parquet) | 2026-11-02 16:38 |
| Caleb Williams Pass Yds Over 224.5 | 2 opportunity | PASS | role per snaps/carries | nflverse pbp + snap_counts | 2026-11-02 16:38 |
| Caleb Williams Pass Yds Over 224.5 | 3 defense profile | PASS | opp defense profile (advstats_season_def, coverage_profile) | advstats_season_def + coverage_profile.json | 2026-11-02 05:09 |
| Caleb Williams Pass Yds Over 224.5 | 4 defender | PASS | see coverage block | PFR adv defense CHI (05:10) / SEA (Firecrawl 06:40) | 2026-11-02 05:10 |
| Caleb Williams Pass Yds Over 224.5 | 5 blitz/pressure | PASS | blitz CHI .411/SEA .221 (FTN); pressure PROXY; flag: Sweat+Simmons first game, not in CHI rate | FTN charting + features.json | 2026-11-02 05:03 |
| Caleb Williams Pass Yds Over 224.5 | 6 QB | PASS | QB C.Williams (Williams back from injury Wk6: QB-RETURN flag + form recheck) | nflverse pbp/NGS passing | 2026-11-02 16:38 |
| Caleb Williams Pass Yds Over 224.5 | 7 role/snaps | PASS | snap share stable L4; §7 3/4 [269.0, 138.0, 305.0, 308.0] | snap_counts_2026.parquet | 2026-11-02 05:03 |
| Caleb Williams Pass Yds Over 224.5 | 8 injuries | PASS | ESPN injuries 16:38 ET | ESPN injuries API | 2026-11-02 16:38 |
| Caleb Williams Pass Yds Over 224.5 | 9 NGS | PASS | NGS thru Wk8 | nflverse NGS | 2026-11-02 05:03 |
| Caleb Williams Pass Yds Over 224.5 | 10 film | PASS | matched to pbp rows, src/film_matches.md | NFL YouTube captions (yt-dlp) + pbp | 2026-11-02 16:42 |
| Caleb Williams Pass Yds Over 224.5 | 11 weather | PASS | NWS+Open-Meteo 16:38 ET: precip 2%, wind 2.7, gust 3.4 mph, no flag | tools/weather_forecast.py | 2026-11-02 16:38 |
| Caleb Williams Pass Yds Over 224.5 | 12 market/price | PASS | FD 224.5 -113, no-vig 0.500 (16:38 ET) | The Odds API pull_odds.py (FD/DK/Pinnacle) | 2026-11-02 16:38 |
| Caleb Williams Pass Yds Over 224.5 | 13 game script | FAIL | 10G CHI underdog over | lines_m1638.json + 10G rule | 2026-11-02 16:38 |
| Caleb Williams Pass Yds Over 224.5 | 14 edge/sims | FAIL | edge +.026 < .03 | tools/sim_v6.py 3x100k seed 20261101 | 2026-11-02 16:44 |
| Caleb Williams Pass Yds Over 224.5 | 15 correlation/ticket bar | PASS | no open ticket on this player+stat | Ghost6 bankroll_slips.md + bet-log.csv | 2026-11-02 16:45 |
| Luther Burden III Rec Yds Under 52.5 | 1 sample | PASS | 4 games w/ current QB C.Williams; season sample through Wk8 | nflverse pbp (src/play_by_play_2026.parquet) | 2026-11-02 16:38 |
| Luther Burden III Rec Yds Under 52.5 | 2 opportunity | PASS | targets L4 [5, 7, 8, 4] | nflverse pbp + snap_counts | 2026-11-02 16:38 |
| Luther Burden III Rec Yds Under 52.5 | 3 defense profile | PASS | opp defense profile (advstats_season_def, coverage_profile) | advstats_season_def + coverage_profile.json | 2026-11-02 05:09 |
| Luther Burden III Rec Yds Under 52.5 | 4 defender | PASS | see coverage block | PFR adv defense CHI (05:10) / SEA (Firecrawl 06:40) | 2026-11-02 05:10 |
| Luther Burden III Rec Yds Under 52.5 | 5 blitz/pressure | PASS | blitz CHI .411/SEA .221 (FTN); pressure PROXY; flag: Sweat+Simmons first game, not in CHI rate | FTN charting + features.json | 2026-11-02 05:03 |
| Luther Burden III Rec Yds Under 52.5 | 6 QB | PASS | QB C.Williams (Williams back from injury Wk6: QB-RETURN flag + form recheck) | nflverse pbp/NGS passing | 2026-11-02 16:38 |
| Luther Burden III Rec Yds Under 52.5 | 7 role/snaps | FAIL | §7 1/4 with Williams; §7 1/4 [63.0, 32.0, 95.0, 130.0] | snap_counts_2026.parquet | 2026-11-02 05:03 |
| Luther Burden III Rec Yds Under 52.5 | 8 injuries | PASS | ESPN injuries 16:38 ET | ESPN injuries API | 2026-11-02 16:38 |
| Luther Burden III Rec Yds Under 52.5 | 9 NGS | PASS | NGS thru Wk8 | nflverse NGS | 2026-11-02 05:03 |
| Luther Burden III Rec Yds Under 52.5 | 10 film | PASS | matched to pbp rows, src/film_matches.md | NFL YouTube captions (yt-dlp) + pbp | 2026-11-02 16:42 |
| Luther Burden III Rec Yds Under 52.5 | 11 weather | PASS | NWS+Open-Meteo 16:38 ET: precip 2%, wind 2.7, gust 3.4 mph, no flag | tools/weather_forecast.py | 2026-11-02 16:38 |
| Luther Burden III Rec Yds Under 52.5 | 12 market/price | PASS | FD 52.5 -113, no-vig 0.500 (16:38 ET) | The Odds API pull_odds.py (FD/DK/Pinnacle) | 2026-11-02 16:38 |
| Luther Burden III Rec Yds Under 52.5 | 13 game script | PASS | SEA -3.5 / total 46.5 | lines_m1638.json + 10G rule | 2026-11-02 16:38 |
| Luther Burden III Rec Yds Under 52.5 | 14 edge/sims | PASS | avg p 0.555 edge +0.055 shrunk +0.038 | tools/sim_v6.py 3x100k seed 20261101 | 2026-11-02 16:44 |
| Luther Burden III Rec Yds Under 52.5 | 15 correlation/ticket bar | PASS | no open ticket on this player+stat | Ghost6 bankroll_slips.md + bet-log.csv | 2026-11-02 16:45 |
| Luther Burden III Receptions Under 4.5 | 1 sample | PASS | 4 games w/ current QB C.Williams; season sample through Wk8 | nflverse pbp (src/play_by_play_2026.parquet) | 2026-11-02 16:38 |
| Luther Burden III Receptions Under 4.5 | 2 opportunity | PASS | targets L4 [5, 7, 8, 4] | nflverse pbp + snap_counts | 2026-11-02 16:38 |
| Luther Burden III Receptions Under 4.5 | 3 defense profile | PASS | opp defense profile (advstats_season_def, coverage_profile) | advstats_season_def + coverage_profile.json | 2026-11-02 05:09 |
| Luther Burden III Receptions Under 4.5 | 4 defender | PASS | see coverage block | PFR adv defense CHI (05:10) / SEA (Firecrawl 06:40) | 2026-11-02 05:10 |
| Luther Burden III Receptions Under 4.5 | 5 blitz/pressure | PASS | blitz CHI .411/SEA .221 (FTN); pressure PROXY; flag: Sweat+Simmons first game, not in CHI rate | FTN charting + features.json | 2026-11-02 05:03 |
| Luther Burden III Receptions Under 4.5 | 6 QB | PASS | QB C.Williams (Williams back from injury Wk6: QB-RETURN flag + form recheck) | nflverse pbp/NGS passing | 2026-11-02 16:38 |
| Luther Burden III Receptions Under 4.5 | 7 role/snaps | PASS | snap share stable L4; §7 2/4 [5.0, 3.0, 8.0, 4.0] | snap_counts_2026.parquet | 2026-11-02 05:03 |
| Luther Burden III Receptions Under 4.5 | 8 injuries | PASS | ESPN injuries 16:38 ET | ESPN injuries API | 2026-11-02 16:38 |
| Luther Burden III Receptions Under 4.5 | 9 NGS | PASS | NGS thru Wk8 | nflverse NGS | 2026-11-02 05:03 |
| Luther Burden III Receptions Under 4.5 | 10 film | PASS | matched to pbp rows, src/film_matches.md | NFL YouTube captions (yt-dlp) + pbp | 2026-11-02 16:42 |
| Luther Burden III Receptions Under 4.5 | 11 weather | PASS | NWS+Open-Meteo 16:38 ET: precip 2%, wind 2.7, gust 3.4 mph, no flag | tools/weather_forecast.py | 2026-11-02 16:38 |
| Luther Burden III Receptions Under 4.5 | 12 market/price | PASS | FD 4.5 -158, no-vig 0.572 (16:38 ET) | The Odds API pull_odds.py (FD/DK/Pinnacle) | 2026-11-02 16:38 |
| Luther Burden III Receptions Under 4.5 | 13 game script | PASS | SEA -3.5 / total 46.5 | lines_m1638.json + 10G rule | 2026-11-02 16:38 |
| Luther Burden III Receptions Under 4.5 | 14 edge/sims | FAIL | negative edge | tools/sim_v6.py 3x100k seed 20261101 | 2026-11-02 16:44 |
| Luther Burden III Receptions Under 4.5 | 15 correlation/ticket bar | PASS | no open ticket on this player+stat | Ghost6 bankroll_slips.md + bet-log.csv | 2026-11-02 16:45 |
| Rome Odunze Rec Yds Under 38.5 | 1 sample | PASS | 4 games w/ current QB C.Williams; season sample through Wk8 | nflverse pbp (src/play_by_play_2026.parquet) | 2026-11-02 16:38 |
| Rome Odunze Rec Yds Under 38.5 | 2 opportunity | PASS | targets L4 [3, 4, 4, 5] | nflverse pbp + snap_counts | 2026-11-02 16:38 |
| Rome Odunze Rec Yds Under 38.5 | 3 defense profile | PASS | opp defense profile (advstats_season_def, coverage_profile) | advstats_season_def + coverage_profile.json | 2026-11-02 05:09 |
| Rome Odunze Rec Yds Under 38.5 | 4 defender | PASS | see coverage block | PFR adv defense CHI (05:10) / SEA (Firecrawl 06:40) | 2026-11-02 05:10 |
| Rome Odunze Rec Yds Under 38.5 | 5 blitz/pressure | PASS | blitz CHI .411/SEA .221 (FTN); pressure PROXY; flag: Sweat+Simmons first game, not in CHI rate | FTN charting + features.json | 2026-11-02 05:03 |
| Rome Odunze Rec Yds Under 38.5 | 6 QB | PASS | QB C.Williams (Williams back from injury Wk6: QB-RETURN flag + form recheck) | nflverse pbp/NGS passing | 2026-11-02 16:38 |
| Rome Odunze Rec Yds Under 38.5 | 7 role/snaps | FAIL | §7 0/4; §7 0/4 [52.0, 43.0, 39.0, 69.0] | snap_counts_2026.parquet | 2026-11-02 05:03 |
| Rome Odunze Rec Yds Under 38.5 | 8 injuries | PASS | ESPN injuries 16:38 ET | ESPN injuries API | 2026-11-02 16:38 |
| Rome Odunze Rec Yds Under 38.5 | 9 NGS | PASS | NGS thru Wk8 | nflverse NGS | 2026-11-02 05:03 |
| Rome Odunze Rec Yds Under 38.5 | 10 film | PASS | matched to pbp rows, src/film_matches.md | NFL YouTube captions (yt-dlp) + pbp | 2026-11-02 16:42 |
| Rome Odunze Rec Yds Under 38.5 | 11 weather | PASS | NWS+Open-Meteo 16:38 ET: precip 2%, wind 2.7, gust 3.4 mph, no flag | tools/weather_forecast.py | 2026-11-02 16:38 |
| Rome Odunze Rec Yds Under 38.5 | 12 market/price | PASS | FD 38.5 -113, no-vig 0.500 (16:38 ET) | The Odds API pull_odds.py (FD/DK/Pinnacle) | 2026-11-02 16:38 |
| Rome Odunze Rec Yds Under 38.5 | 13 game script | PASS | SEA -3.5 / total 46.5 | lines_m1638.json + 10G rule | 2026-11-02 16:38 |
| Rome Odunze Rec Yds Under 38.5 | 14 edge/sims | FAIL | edge < .03 | tools/sim_v6.py 3x100k seed 20261101 | 2026-11-02 16:44 |
| Rome Odunze Rec Yds Under 38.5 | 15 correlation/ticket bar | PASS | no open ticket on this player+stat | Ghost6 bankroll_slips.md + bet-log.csv | 2026-11-02 16:45 |
| Rome Odunze Receptions Under 3.5 | 1 sample | PASS | 4 games w/ current QB C.Williams; season sample through Wk8 | nflverse pbp (src/play_by_play_2026.parquet) | 2026-11-02 16:38 |
| Rome Odunze Receptions Under 3.5 | 2 opportunity | PASS | targets L4 [3, 4, 4, 5] | nflverse pbp + snap_counts | 2026-11-02 16:38 |
| Rome Odunze Receptions Under 3.5 | 3 defense profile | PASS | opp defense profile (advstats_season_def, coverage_profile) | advstats_season_def + coverage_profile.json | 2026-11-02 05:09 |
| Rome Odunze Receptions Under 3.5 | 4 defender | PASS | see coverage block | PFR adv defense CHI (05:10) / SEA (Firecrawl 06:40) | 2026-11-02 05:10 |
| Rome Odunze Receptions Under 3.5 | 5 blitz/pressure | PASS | blitz CHI .411/SEA .221 (FTN); pressure PROXY; flag: Sweat+Simmons first game, not in CHI rate | FTN charting + features.json | 2026-11-02 05:03 |
| Rome Odunze Receptions Under 3.5 | 6 QB | PASS | QB C.Williams (Williams back from injury Wk6: QB-RETURN flag + form recheck) | nflverse pbp/NGS passing | 2026-11-02 16:38 |
| Rome Odunze Receptions Under 3.5 | 7 role/snaps | PASS | snap share stable L4; §7 3/4 [2.0, 3.0, 3.0, 4.0] | snap_counts_2026.parquet | 2026-11-02 05:03 |
| Rome Odunze Receptions Under 3.5 | 8 injuries | PASS | ESPN injuries 16:38 ET | ESPN injuries API | 2026-11-02 16:38 |
| Rome Odunze Receptions Under 3.5 | 9 NGS | PASS | NGS thru Wk8 | nflverse NGS | 2026-11-02 05:03 |
| Rome Odunze Receptions Under 3.5 | 10 film | PASS | matched to pbp rows, src/film_matches.md | NFL YouTube captions (yt-dlp) + pbp | 2026-11-02 16:42 |
| Rome Odunze Receptions Under 3.5 | 11 weather | PASS | NWS+Open-Meteo 16:38 ET: precip 2%, wind 2.7, gust 3.4 mph, no flag | tools/weather_forecast.py | 2026-11-02 16:38 |
| Rome Odunze Receptions Under 3.5 | 12 market/price | PASS | FD 3.5 -180, no-vig 0.601 (16:38 ET) | The Odds API pull_odds.py (FD/DK/Pinnacle) | 2026-11-02 16:38 |
| Rome Odunze Receptions Under 3.5 | 13 game script | PASS | SEA -3.5 / total 46.5 | lines_m1638.json + 10G rule | 2026-11-02 16:38 |
| Rome Odunze Receptions Under 3.5 | 14 edge/sims | FAIL | negative edge | tools/sim_v6.py 3x100k seed 20261101 | 2026-11-02 16:44 |
| Rome Odunze Receptions Under 3.5 | 15 correlation/ticket bar | PASS | no open ticket on this player+stat | Ghost6 bankroll_slips.md + bet-log.csv | 2026-11-02 16:45 |
| Colston Loveland Rec Yds Under 42.5 | 1 sample | PASS | 4 games w/ current QB C.Williams; season sample through Wk8 | nflverse pbp (src/play_by_play_2026.parquet) | 2026-11-02 16:38 |
| Colston Loveland Rec Yds Under 42.5 | 2 opportunity | PASS | targets L4 [2, 3, 7, 12] | nflverse pbp + snap_counts | 2026-11-02 16:38 |
| Colston Loveland Rec Yds Under 42.5 | 3 defense profile | PASS | opp defense profile (advstats_season_def, coverage_profile) | advstats_season_def + coverage_profile.json | 2026-11-02 05:09 |
| Colston Loveland Rec Yds Under 42.5 | 4 defender | UNVERIFIED | ISS-05: no per-defender TE coverage data | PFR adv defense CHI (05:10) / SEA (Firecrawl 06:40) | 2026-11-02 05:10 |
| Colston Loveland Rec Yds Under 42.5 | 5 blitz/pressure | PASS | blitz CHI .411/SEA .221 (FTN); pressure PROXY; flag: Sweat+Simmons first game, not in CHI rate | FTN charting + features.json | 2026-11-02 05:03 |
| Colston Loveland Rec Yds Under 42.5 | 6 QB | PASS | QB C.Williams (Williams back from injury Wk6: QB-RETURN flag + form recheck) | nflverse pbp/NGS passing | 2026-11-02 16:38 |
| Colston Loveland Rec Yds Under 42.5 | 7 role/snaps | FAIL | §7 2/4; §7 2/4 [0.0, 3.0, 65.0, 69.0] | snap_counts_2026.parquet | 2026-11-02 05:03 |
| Colston Loveland Rec Yds Under 42.5 | 8 injuries | PASS | ESPN injuries 16:38 ET | ESPN injuries API | 2026-11-02 16:38 |
| Colston Loveland Rec Yds Under 42.5 | 9 NGS | PASS | NGS thru Wk8 | nflverse NGS | 2026-11-02 05:03 |
| Colston Loveland Rec Yds Under 42.5 | 10 film | PASS | matched to pbp rows, src/film_matches.md | NFL YouTube captions (yt-dlp) + pbp | 2026-11-02 16:42 |
| Colston Loveland Rec Yds Under 42.5 | 11 weather | PASS | NWS+Open-Meteo 16:38 ET: precip 2%, wind 2.7, gust 3.4 mph, no flag | tools/weather_forecast.py | 2026-11-02 16:38 |
| Colston Loveland Rec Yds Under 42.5 | 12 market/price | PASS | FD 42.5 -113, no-vig 0.500 (16:38 ET) | The Odds API pull_odds.py (FD/DK/Pinnacle) | 2026-11-02 16:38 |
| Colston Loveland Rec Yds Under 42.5 | 13 game script | FAIL | CHI could trail -> TE volume up | lines_m1638.json + 10G rule | 2026-11-02 16:38 |
| Colston Loveland Rec Yds Under 42.5 | 14 edge/sims | FAIL | MODEL-SUSPECT | tools/sim_v6.py 3x100k seed 20261101 | 2026-11-02 16:44 |
| Colston Loveland Rec Yds Under 42.5 | 15 correlation/ticket bar | PASS | no open ticket on this player+stat | Ghost6 bankroll_slips.md + bet-log.csv | 2026-11-02 16:45 |
| Colston Loveland Receptions Under 4.5 | 1 sample | PASS | 4 games w/ current QB C.Williams; season sample through Wk8 | nflverse pbp (src/play_by_play_2026.parquet) | 2026-11-02 16:38 |
| Colston Loveland Receptions Under 4.5 | 2 opportunity | PASS | targets L4 [2, 3, 7, 12] | nflverse pbp + snap_counts | 2026-11-02 16:38 |
| Colston Loveland Receptions Under 4.5 | 3 defense profile | PASS | opp defense profile (advstats_season_def, coverage_profile) | advstats_season_def + coverage_profile.json | 2026-11-02 05:09 |
| Colston Loveland Receptions Under 4.5 | 4 defender | UNVERIFIED | ISS-05 | PFR adv defense CHI (05:10) / SEA (Firecrawl 06:40) | 2026-11-02 05:10 |
| Colston Loveland Receptions Under 4.5 | 5 blitz/pressure | PASS | blitz CHI .411/SEA .221 (FTN); pressure PROXY; flag: Sweat+Simmons first game, not in CHI rate | FTN charting + features.json | 2026-11-02 05:03 |
| Colston Loveland Receptions Under 4.5 | 6 QB | PASS | QB C.Williams (Williams back from injury Wk6: QB-RETURN flag + form recheck) | nflverse pbp/NGS passing | 2026-11-02 16:38 |
| Colston Loveland Receptions Under 4.5 | 7 role/snaps | FAIL | §7 2/4; §7 2/4 [0.0, 1.0, 6.0, 7.0] | snap_counts_2026.parquet | 2026-11-02 05:03 |
| Colston Loveland Receptions Under 4.5 | 8 injuries | PASS | ESPN injuries 16:38 ET | ESPN injuries API | 2026-11-02 16:38 |
| Colston Loveland Receptions Under 4.5 | 9 NGS | PASS | NGS thru Wk8 | nflverse NGS | 2026-11-02 05:03 |
| Colston Loveland Receptions Under 4.5 | 10 film | PASS | matched to pbp rows, src/film_matches.md | NFL YouTube captions (yt-dlp) + pbp | 2026-11-02 16:42 |
| Colston Loveland Receptions Under 4.5 | 11 weather | PASS | NWS+Open-Meteo 16:38 ET: precip 2%, wind 2.7, gust 3.4 mph, no flag | tools/weather_forecast.py | 2026-11-02 16:38 |
| Colston Loveland Receptions Under 4.5 | 12 market/price | PASS | FD 4.5 -154, no-vig 0.567 (16:38 ET) | The Odds API pull_odds.py (FD/DK/Pinnacle) | 2026-11-02 16:38 |
| Colston Loveland Receptions Under 4.5 | 13 game script | PASS | SEA -3.5 / total 46.5 | lines_m1638.json + 10G rule | 2026-11-02 16:38 |
| Colston Loveland Receptions Under 4.5 | 14 edge/sims | PASS | avg p 0.614 edge +0.047 shrunk +0.013 | tools/sim_v6.py 3x100k seed 20261101 | 2026-11-02 16:44 |
| Colston Loveland Receptions Under 4.5 | 15 correlation/ticket bar | PASS | no open ticket on this player+stat | Ghost6 bankroll_slips.md + bet-log.csv | 2026-11-02 16:45 |
| D'Andre Swift Rush Yds Under 59.5 | 1 sample | PASS | 4 games w/ current QB C.Williams; season sample through Wk8 | nflverse pbp (src/play_by_play_2026.parquet) | 2026-11-02 16:38 |
| D'Andre Swift Rush Yds Under 59.5 | 2 opportunity | PASS | role per snaps/carries | nflverse pbp + snap_counts | 2026-11-02 16:38 |
| D'Andre Swift Rush Yds Under 59.5 | 3 defense profile | PASS | opp defense profile (advstats_season_def, coverage_profile) | advstats_season_def + coverage_profile.json | 2026-11-02 05:09 |
| D'Andre Swift Rush Yds Under 59.5 | 4 defender | PASS | see coverage block | PFR adv defense CHI (05:10) / SEA (Firecrawl 06:40) | 2026-11-02 05:10 |
| D'Andre Swift Rush Yds Under 59.5 | 5 blitz/pressure | PASS | blitz CHI .411/SEA .221 (FTN); pressure PROXY; flag: Sweat+Simmons first game, not in CHI rate | FTN charting + features.json | 2026-11-02 05:03 |
| D'Andre Swift Rush Yds Under 59.5 | 6 QB | PASS | QB C.Williams (Williams back from injury Wk6: QB-RETURN flag + form recheck) | nflverse pbp/NGS passing | 2026-11-02 16:38 |
| D'Andre Swift Rush Yds Under 59.5 | 7 role/snaps | FAIL | §7 2/4; §7 2/4 [124.0, 45.0, 44.0, 78.0] | snap_counts_2026.parquet | 2026-11-02 05:03 |
| D'Andre Swift Rush Yds Under 59.5 | 8 injuries | PASS | ESPN injuries 16:38 ET | ESPN injuries API | 2026-11-02 16:38 |
| D'Andre Swift Rush Yds Under 59.5 | 9 NGS | PASS | NGS thru Wk8 | nflverse NGS | 2026-11-02 05:03 |
| D'Andre Swift Rush Yds Under 59.5 | 10 film | PASS | matched to pbp rows, src/film_matches.md | NFL YouTube captions (yt-dlp) + pbp | 2026-11-02 16:42 |
| D'Andre Swift Rush Yds Under 59.5 | 11 weather | PASS | NWS+Open-Meteo 16:38 ET: precip 2%, wind 2.7, gust 3.4 mph, no flag | tools/weather_forecast.py | 2026-11-02 16:38 |
| D'Andre Swift Rush Yds Under 59.5 | 12 market/price | PASS | FD 59.5 -113, no-vig 0.500 (16:38 ET) | The Odds API pull_odds.py (FD/DK/Pinnacle) | 2026-11-02 16:38 |
| D'Andre Swift Rush Yds Under 59.5 | 13 game script | PASS | SEA -3.5 / total 46.5 | lines_m1638.json + 10G rule | 2026-11-02 16:38 |
| D'Andre Swift Rush Yds Under 59.5 | 14 edge/sims | PASS | avg p 0.646 edge +0.146 shrunk +0.102 | tools/sim_v6.py 3x100k seed 20261101 | 2026-11-02 16:44 |
| D'Andre Swift Rush Yds Under 59.5 | 15 correlation/ticket bar | FAIL | §11 same player as open SGP (Swift 50+ rush+rec/Swift TD; Wilson 15+) | Ghost6 bankroll_slips.md + bet-log.csv | 2026-11-02 16:45 |
| D'Andre Swift Rush+Rec Yds Under 86.5 | 1 sample | PASS | 4 games w/ current QB C.Williams; season sample through Wk8 | nflverse pbp (src/play_by_play_2026.parquet) | 2026-11-02 16:38 |
| D'Andre Swift Rush+Rec Yds Under 86.5 | 2 opportunity | PASS | targets L4 [1, 5, 5, 4] | nflverse pbp + snap_counts | 2026-11-02 16:38 |
| D'Andre Swift Rush+Rec Yds Under 86.5 | 3 defense profile | PASS | opp defense profile (advstats_season_def, coverage_profile) | advstats_season_def + coverage_profile.json | 2026-11-02 05:09 |
| D'Andre Swift Rush+Rec Yds Under 86.5 | 4 defender | PASS | see coverage block | PFR adv defense CHI (05:10) / SEA (Firecrawl 06:40) | 2026-11-02 05:10 |
| D'Andre Swift Rush+Rec Yds Under 86.5 | 5 blitz/pressure | PASS | blitz CHI .411/SEA .221 (FTN); pressure PROXY; flag: Sweat+Simmons first game, not in CHI rate | FTN charting + features.json | 2026-11-02 05:03 |
| D'Andre Swift Rush+Rec Yds Under 86.5 | 6 QB | PASS | QB C.Williams (Williams back from injury Wk6: QB-RETURN flag + form recheck) | nflverse pbp/NGS passing | 2026-11-02 16:38 |
| D'Andre Swift Rush+Rec Yds Under 86.5 | 7 role/snaps | FAIL | §7 1/4; §7 1/4 [134.0, 99.0, 70.0, 90.0] | snap_counts_2026.parquet | 2026-11-02 05:03 |
| D'Andre Swift Rush+Rec Yds Under 86.5 | 8 injuries | PASS | ESPN injuries 16:38 ET | ESPN injuries API | 2026-11-02 16:38 |
| D'Andre Swift Rush+Rec Yds Under 86.5 | 9 NGS | PASS | NGS thru Wk8 | nflverse NGS | 2026-11-02 05:03 |
| D'Andre Swift Rush+Rec Yds Under 86.5 | 10 film | PASS | matched to pbp rows, src/film_matches.md | NFL YouTube captions (yt-dlp) + pbp | 2026-11-02 16:42 |
| D'Andre Swift Rush+Rec Yds Under 86.5 | 11 weather | PASS | NWS+Open-Meteo 16:38 ET: precip 2%, wind 2.7, gust 3.4 mph, no flag | tools/weather_forecast.py | 2026-11-02 16:38 |
| D'Andre Swift Rush+Rec Yds Under 86.5 | 12 market/price | PASS | FD 86.5 -113, no-vig 0.500 (16:38 ET) | The Odds API pull_odds.py (FD/DK/Pinnacle) | 2026-11-02 16:38 |
| D'Andre Swift Rush+Rec Yds Under 86.5 | 13 game script | FAIL | 10G | lines_m1638.json + 10G rule | 2026-11-02 16:38 |
| D'Andre Swift Rush+Rec Yds Under 86.5 | 14 edge/sims | PASS | avg p 0.617 edge +0.117 shrunk +0.082 | tools/sim_v6.py 3x100k seed 20261101 | 2026-11-02 16:44 |
| D'Andre Swift Rush+Rec Yds Under 86.5 | 15 correlation/ticket bar | FAIL | §11 same player as open SGP (Swift 50+ rush+rec/Swift TD; Wilson 15+) | Ghost6 bankroll_slips.md + bet-log.csv | 2026-11-02 16:45 |
| D'Andre Swift Rec Yds Over 21.5 | 1 sample | PASS | 4 games w/ current QB C.Williams; season sample through Wk8 | nflverse pbp (src/play_by_play_2026.parquet) | 2026-11-02 16:38 |
| D'Andre Swift Rec Yds Over 21.5 | 2 opportunity | PASS | targets L4 [1, 5, 5, 4] | nflverse pbp + snap_counts | 2026-11-02 16:38 |
| D'Andre Swift Rec Yds Over 21.5 | 3 defense profile | PASS | opp defense profile (advstats_season_def, coverage_profile) | advstats_season_def + coverage_profile.json | 2026-11-02 05:09 |
| D'Andre Swift Rec Yds Over 21.5 | 4 defender | PASS | see coverage block | PFR adv defense CHI (05:10) / SEA (Firecrawl 06:40) | 2026-11-02 05:10 |
| D'Andre Swift Rec Yds Over 21.5 | 5 blitz/pressure | PASS | blitz CHI .411/SEA .221 (FTN); pressure PROXY; flag: Sweat+Simmons first game, not in CHI rate | FTN charting + features.json | 2026-11-02 05:03 |
| D'Andre Swift Rec Yds Over 21.5 | 6 QB | PASS | QB C.Williams (Williams back from injury Wk6: QB-RETURN flag + form recheck) | nflverse pbp/NGS passing | 2026-11-02 16:38 |
| D'Andre Swift Rec Yds Over 21.5 | 7 role/snaps | PASS | snap share stable L4; §7 2/4 [10.0, 54.0, 26.0, 12.0] | snap_counts_2026.parquet | 2026-11-02 05:03 |
| D'Andre Swift Rec Yds Over 21.5 | 8 injuries | PASS | ESPN injuries 16:38 ET | ESPN injuries API | 2026-11-02 16:38 |
| D'Andre Swift Rec Yds Over 21.5 | 9 NGS | PASS | NGS thru Wk8 | nflverse NGS | 2026-11-02 05:03 |
| D'Andre Swift Rec Yds Over 21.5 | 10 film | PASS | matched to pbp rows, src/film_matches.md | NFL YouTube captions (yt-dlp) + pbp | 2026-11-02 16:42 |
| D'Andre Swift Rec Yds Over 21.5 | 11 weather | PASS | NWS+Open-Meteo 16:38 ET: precip 2%, wind 2.7, gust 3.4 mph, no flag | tools/weather_forecast.py | 2026-11-02 16:38 |
| D'Andre Swift Rec Yds Over 21.5 | 12 market/price | PASS | FD 21.5 -113, no-vig 0.500 (16:38 ET) | The Odds API pull_odds.py (FD/DK/Pinnacle) | 2026-11-02 16:38 |
| D'Andre Swift Rec Yds Over 21.5 | 13 game script | FAIL | 10G | lines_m1638.json + 10G rule | 2026-11-02 16:38 |
| D'Andre Swift Rec Yds Over 21.5 | 14 edge/sims | FAIL | p < .45 | tools/sim_v6.py 3x100k seed 20261101 | 2026-11-02 16:44 |
| D'Andre Swift Rec Yds Over 21.5 | 15 correlation/ticket bar | FAIL | §11 same player as open SGP (Swift 50+ rush+rec/Swift TD; Wilson 15+) | Ghost6 bankroll_slips.md + bet-log.csv | 2026-11-02 16:45 |
| D'Andre Swift Receptions Over 3.5 | 1 sample | PASS | 4 games w/ current QB C.Williams; season sample through Wk8 | nflverse pbp (src/play_by_play_2026.parquet) | 2026-11-02 16:38 |
| D'Andre Swift Receptions Over 3.5 | 2 opportunity | FAIL | 5+ tgt in 2 of L4 | nflverse pbp + snap_counts | 2026-11-02 16:38 |
| D'Andre Swift Receptions Over 3.5 | 3 defense profile | PASS | opp defense profile (advstats_season_def, coverage_profile) | advstats_season_def + coverage_profile.json | 2026-11-02 05:09 |
| D'Andre Swift Receptions Over 3.5 | 4 defender | PASS | see coverage block | PFR adv defense CHI (05:10) / SEA (Firecrawl 06:40) | 2026-11-02 05:10 |
| D'Andre Swift Receptions Over 3.5 | 5 blitz/pressure | PASS | blitz CHI .411/SEA .221 (FTN); pressure PROXY; flag: Sweat+Simmons first game, not in CHI rate | FTN charting + features.json | 2026-11-02 05:03 |
| D'Andre Swift Receptions Over 3.5 | 6 QB | PASS | QB C.Williams (Williams back from injury Wk6: QB-RETURN flag + form recheck) | nflverse pbp/NGS passing | 2026-11-02 16:38 |
| D'Andre Swift Receptions Over 3.5 | 7 role/snaps | PASS | snap share stable L4; §7 3/4 [1.0, 5.0, 4.0, 4.0] | snap_counts_2026.parquet | 2026-11-02 05:03 |
| D'Andre Swift Receptions Over 3.5 | 8 injuries | PASS | ESPN injuries 16:38 ET | ESPN injuries API | 2026-11-02 16:38 |
| D'Andre Swift Receptions Over 3.5 | 9 NGS | PASS | NGS thru Wk8 | nflverse NGS | 2026-11-02 05:03 |
| D'Andre Swift Receptions Over 3.5 | 10 film | PASS | matched to pbp rows, src/film_matches.md | NFL YouTube captions (yt-dlp) + pbp | 2026-11-02 16:42 |
| D'Andre Swift Receptions Over 3.5 | 11 weather | PASS | NWS+Open-Meteo 16:38 ET: precip 2%, wind 2.7, gust 3.4 mph, no flag | tools/weather_forecast.py | 2026-11-02 16:38 |
| D'Andre Swift Receptions Over 3.5 | 12 market/price | PASS | FD 3.5 +112, no-vig 0.441 (16:38 ET) | The Odds API pull_odds.py (FD/DK/Pinnacle) | 2026-11-02 16:38 |
| D'Andre Swift Receptions Over 3.5 | 13 game script | FAIL | 10G | lines_m1638.json + 10G rule | 2026-11-02 16:38 |
| D'Andre Swift Receptions Over 3.5 | 14 edge/sims | FAIL | edge +.025, medians 3.0 | tools/sim_v6.py 3x100k seed 20261101 | 2026-11-02 16:44 |
| D'Andre Swift Receptions Over 3.5 | 15 correlation/ticket bar | FAIL | open-ticket status of Swift 3+ rec UNCONFIRMED (r2/odunze/results.md ~1:20 PM ET says placed; the 7-leg ticket holding it was cashed out per Ghost6 4:10 PM ET); barred fail-closed as nested rung | Ghost6 bankroll_slips.md + bet-log.csv | 2026-11-02 16:45 |
| D'Andre Swift Receptions Over 2.5 | 1 sample | PASS | 4 games w/ current QB C.Williams; season sample through Wk8 | nflverse pbp (src/play_by_play_2026.parquet) | 2026-11-02 16:38 |
| D'Andre Swift Receptions Over 2.5 | 2 opportunity | FAIL | 5+ tgt 2/4 | nflverse pbp + snap_counts | 2026-11-02 16:38 |
| D'Andre Swift Receptions Over 2.5 | 3 defense profile | PASS | opp defense profile (advstats_season_def, coverage_profile) | advstats_season_def + coverage_profile.json | 2026-11-02 05:09 |
| D'Andre Swift Receptions Over 2.5 | 4 defender | PASS | see coverage block | PFR adv defense CHI (05:10) / SEA (Firecrawl 06:40) | 2026-11-02 05:10 |
| D'Andre Swift Receptions Over 2.5 | 5 blitz/pressure | PASS | blitz CHI .411/SEA .221 (FTN); pressure PROXY; flag: Sweat+Simmons first game, not in CHI rate | FTN charting + features.json | 2026-11-02 05:03 |
| D'Andre Swift Receptions Over 2.5 | 6 QB | PASS | QB C.Williams (Williams back from injury Wk6: QB-RETURN flag + form recheck) | nflverse pbp/NGS passing | 2026-11-02 16:38 |
| D'Andre Swift Receptions Over 2.5 | 7 role/snaps | PASS | snap share stable L4; §7 3/4 [1.0, 5.0, 4.0, 4.0] | snap_counts_2026.parquet | 2026-11-02 05:03 |
| D'Andre Swift Receptions Over 2.5 | 8 injuries | PASS | ESPN injuries 16:38 ET | ESPN injuries API | 2026-11-02 16:38 |
| D'Andre Swift Receptions Over 2.5 | 9 NGS | PASS | NGS thru Wk8 | nflverse NGS | 2026-11-02 05:03 |
| D'Andre Swift Receptions Over 2.5 | 10 film | PASS | matched to pbp rows, src/film_matches.md | NFL YouTube captions (yt-dlp) + pbp | 2026-11-02 16:42 |
| D'Andre Swift Receptions Over 2.5 | 11 weather | PASS | NWS+Open-Meteo 16:38 ET: precip 2%, wind 2.7, gust 3.4 mph, no flag | tools/weather_forecast.py | 2026-11-02 16:38 |
| D'Andre Swift Receptions Over 2.5 | 12 market/price | PASS | FD 2.5 -225, no-vig 0.648 (16:38 ET) | The Odds API pull_odds.py (FD/DK/Pinnacle) | 2026-11-02 16:38 |
| D'Andre Swift Receptions Over 2.5 | 13 game script | PASS | SEA -3.5 / total 46.5 | lines_m1638.json + 10G rule | 2026-11-02 16:38 |
| D'Andre Swift Receptions Over 2.5 | 14 edge/sims | FAIL | shrunk -.031 | tools/sim_v6.py 3x100k seed 20261101 | 2026-11-02 16:44 |
| D'Andre Swift Receptions Over 2.5 | 15 correlation/ticket bar | FAIL | open-ticket status of Swift 3+ rec UNCONFIRMED (r2/odunze/results.md ~1:20 PM ET says placed; the 7-leg ticket holding it was cashed out per Ghost6 4:10 PM ET); barred fail-closed as nested rung | Ghost6 bankroll_slips.md + bet-log.csv | 2026-11-02 16:45 |
| Roschon Johnson Rush Yds Over 10.5 | 1 sample | FAIL | 2 games (LOW-SAMPLE) | nflverse pbp (src/play_by_play_2026.parquet) | 2026-11-02 16:38 |
| Roschon Johnson Rush Yds Over 10.5 | 2 opportunity | PASS | role per snaps/carries | nflverse pbp + snap_counts | 2026-11-02 16:38 |
| Roschon Johnson Rush Yds Over 10.5 | 3 defense profile | FAIL | SEA 3.40 YPC | advstats_season_def + coverage_profile.json | 2026-11-02 05:09 |
| Roschon Johnson Rush Yds Over 10.5 | 4 defender | PASS | see coverage block | PFR adv defense CHI (05:10) / SEA (Firecrawl 06:40) | 2026-11-02 05:10 |
| Roschon Johnson Rush Yds Over 10.5 | 5 blitz/pressure | PASS | blitz CHI .411/SEA .221 (FTN); pressure PROXY; flag: Sweat+Simmons first game, not in CHI rate | FTN charting + features.json | 2026-11-02 05:03 |
| Roschon Johnson Rush Yds Over 10.5 | 6 QB | PASS | QB C.Williams (Williams back from injury Wk6: QB-RETURN flag + form recheck) | nflverse pbp/NGS passing | 2026-11-02 16:38 |
| Roschon Johnson Rush Yds Over 10.5 | 7 role/snaps | FAIL | RB2; §7 2/2 [51.0, 13.0] | snap_counts_2026.parquet | 2026-11-02 05:03 |
| Roschon Johnson Rush Yds Over 10.5 | 8 injuries | PASS | ESPN injuries 16:38 ET | ESPN injuries API | 2026-11-02 16:38 |
| Roschon Johnson Rush Yds Over 10.5 | 9 NGS | PASS | NGS thru Wk8 | nflverse NGS | 2026-11-02 05:03 |
| Roschon Johnson Rush Yds Over 10.5 | 10 film | UNVERIFIED | no caption cue matched to pbp | NFL YouTube captions (yt-dlp) + pbp | 2026-11-02 16:42 |
| Roschon Johnson Rush Yds Over 10.5 | 11 weather | PASS | NWS+Open-Meteo 16:38 ET: precip 2%, wind 2.7, gust 3.4 mph, no flag | tools/weather_forecast.py | 2026-11-02 16:38 |
| Roschon Johnson Rush Yds Over 10.5 | 12 market/price | PASS | FD 10.5 -113, no-vig 0.500 (16:38 ET) | The Odds API pull_odds.py (FD/DK/Pinnacle) | 2026-11-02 16:38 |
| Roschon Johnson Rush Yds Over 10.5 | 13 game script | FAIL | dog | lines_m1638.json + 10G rule | 2026-11-02 16:38 |
| Roschon Johnson Rush Yds Over 10.5 | 14 edge/sims | FAIL | MODEL-SUSPECT | tools/sim_v6.py 3x100k seed 20261101 | 2026-11-02 16:44 |
| Roschon Johnson Rush Yds Over 10.5 | 15 correlation/ticket bar | PASS | no open ticket on this player+stat | Ghost6 bankroll_slips.md + bet-log.csv | 2026-11-02 16:45 |
| Sam Darnold Pass Yds Over 238.5 | 1 sample | PASS | 4 games w/ current QB S.Darnold; season sample through Wk8 | nflverse pbp (src/play_by_play_2026.parquet) | 2026-11-02 16:38 |
| Sam Darnold Pass Yds Over 238.5 | 2 opportunity | PASS | role per snaps/carries | nflverse pbp + snap_counts | 2026-11-02 16:38 |
| Sam Darnold Pass Yds Over 238.5 | 3 defense profile | PASS | opp defense profile (advstats_season_def, coverage_profile) | advstats_season_def + coverage_profile.json | 2026-11-02 05:09 |
| Sam Darnold Pass Yds Over 238.5 | 4 defender | PASS | see coverage block | PFR adv defense CHI (05:10) / SEA (Firecrawl 06:40) | 2026-11-02 05:10 |
| Sam Darnold Pass Yds Over 238.5 | 5 blitz/pressure | PASS | blitz CHI .411/SEA .221 (FTN); pressure PROXY; flag: Sweat+Simmons first game, not in CHI rate | FTN charting + features.json | 2026-11-02 05:03 |
| Sam Darnold Pass Yds Over 238.5 | 6 QB | PASS | QB S.Darnold; LT Cross OUT, Nelson (G) added | nflverse pbp/NGS passing | 2026-11-02 16:38 |
| Sam Darnold Pass Yds Over 238.5 | 7 role/snaps | FAIL | §7 2/4; §7 2/4 [168.0, 195.0, 278.0, 257.0] | snap_counts_2026.parquet | 2026-11-02 05:03 |
| Sam Darnold Pass Yds Over 238.5 | 8 injuries | FAIL | LT Cross OUT; Nelson is a guard | ESPN injuries API | 2026-11-02 16:38 |
| Sam Darnold Pass Yds Over 238.5 | 9 NGS | PASS | NGS thru Wk8 | nflverse NGS | 2026-11-02 05:03 |
| Sam Darnold Pass Yds Over 238.5 | 10 film | PASS | matched to pbp rows, src/film_matches.md | NFL YouTube captions (yt-dlp) + pbp | 2026-11-02 16:42 |
| Sam Darnold Pass Yds Over 238.5 | 11 weather | PASS | NWS+Open-Meteo 16:38 ET: precip 2%, wind 2.7, gust 3.4 mph, no flag | tools/weather_forecast.py | 2026-11-02 16:38 |
| Sam Darnold Pass Yds Over 238.5 | 12 market/price | PASS | FD 238.5 -113, no-vig 0.500 (16:38 ET) | The Odds API pull_odds.py (FD/DK/Pinnacle) | 2026-11-02 16:38 |
| Sam Darnold Pass Yds Over 238.5 | 13 game script | PASS | SEA -3.5 / total 46.5 | lines_m1638.json + 10G rule | 2026-11-02 16:38 |
| Sam Darnold Pass Yds Over 238.5 | 14 edge/sims | PASS | avg p 0.538 edge +0.038 shrunk +0.027 | tools/sim_v6.py 3x100k seed 20261101 | 2026-11-02 16:44 |
| Sam Darnold Pass Yds Over 238.5 | 15 correlation/ticket bar | PASS | no open ticket on this player+stat | Ghost6 bankroll_slips.md + bet-log.csv | 2026-11-02 16:45 |
| Jaxon Smith-Njigba Rec Yds Over 99.5 | 1 sample | PASS | 4 games w/ current QB S.Darnold; season sample through Wk8 | nflverse pbp (src/play_by_play_2026.parquet) | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Rec Yds Over 99.5 | 2 opportunity | PASS | targets L4 [6, 8, 16, 12] | nflverse pbp + snap_counts | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Rec Yds Over 99.5 | 3 defense profile | PASS | opp defense profile (advstats_season_def, coverage_profile) | advstats_season_def + coverage_profile.json | 2026-11-02 05:09 |
| Jaxon Smith-Njigba Rec Yds Over 99.5 | 4 defender | PASS | see coverage block | PFR adv defense CHI (05:10) / SEA (Firecrawl 06:40) | 2026-11-02 05:10 |
| Jaxon Smith-Njigba Rec Yds Over 99.5 | 5 blitz/pressure | PASS | blitz CHI .411/SEA .221 (FTN); pressure PROXY; flag: Sweat+Simmons first game, not in CHI rate | FTN charting + features.json | 2026-11-02 05:03 |
| Jaxon Smith-Njigba Rec Yds Over 99.5 | 6 QB | PASS | QB S.Darnold; LT Cross OUT, Nelson (G) added | nflverse pbp/NGS passing | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Rec Yds Over 99.5 | 7 role/snaps | PASS | snap share stable L4; §7 3/4 [76.0, 102.0, 134.0, 150.0] | snap_counts_2026.parquet | 2026-11-02 05:03 |
| Jaxon Smith-Njigba Rec Yds Over 99.5 | 8 injuries | PASS | ESPN injuries 16:38 ET | ESPN injuries API | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Rec Yds Over 99.5 | 9 NGS | PASS | NGS thru Wk8 | nflverse NGS | 2026-11-02 05:03 |
| Jaxon Smith-Njigba Rec Yds Over 99.5 | 10 film | PASS | matched to pbp rows, src/film_matches.md | NFL YouTube captions (yt-dlp) + pbp | 2026-11-02 16:42 |
| Jaxon Smith-Njigba Rec Yds Over 99.5 | 11 weather | PASS | NWS+Open-Meteo 16:38 ET: precip 2%, wind 2.7, gust 3.4 mph, no flag | tools/weather_forecast.py | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Rec Yds Over 99.5 | 12 market/price | PASS | FD 99.5 -113, no-vig 0.500 (16:38 ET) | The Odds API pull_odds.py (FD/DK/Pinnacle) | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Rec Yds Over 99.5 | 13 game script | PASS | SEA -3.5 / total 46.5 | lines_m1638.json + 10G rule | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Rec Yds Over 99.5 | 14 edge/sims | FAIL | §14 cushion; MODEL-SUSPECT | tools/sim_v6.py 3x100k seed 20261101 | 2026-11-02 16:44 |
| Jaxon Smith-Njigba Rec Yds Over 99.5 | 15 correlation/ticket bar | FAIL | §11/§15 BAR: nested rung of open ticket JSN 70+ rec yds (live SGP, Ghost6 bankroll_slips.md 4:11 PM ET) | Ghost6 bankroll_slips.md + bet-log.csv | 2026-11-02 16:45 |
| Jaxon Smith-Njigba Rec Yds Over 89.5 | 1 sample | PASS | 4 games w/ current QB S.Darnold; season sample through Wk8 | nflverse pbp (src/play_by_play_2026.parquet) | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Rec Yds Over 89.5 | 2 opportunity | PASS | targets L4 [6, 8, 16, 12] | nflverse pbp + snap_counts | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Rec Yds Over 89.5 | 3 defense profile | PASS | opp defense profile (advstats_season_def, coverage_profile) | advstats_season_def + coverage_profile.json | 2026-11-02 05:09 |
| Jaxon Smith-Njigba Rec Yds Over 89.5 | 4 defender | PASS | see coverage block | PFR adv defense CHI (05:10) / SEA (Firecrawl 06:40) | 2026-11-02 05:10 |
| Jaxon Smith-Njigba Rec Yds Over 89.5 | 5 blitz/pressure | PASS | blitz CHI .411/SEA .221 (FTN); pressure PROXY; flag: Sweat+Simmons first game, not in CHI rate | FTN charting + features.json | 2026-11-02 05:03 |
| Jaxon Smith-Njigba Rec Yds Over 89.5 | 6 QB | PASS | QB S.Darnold; LT Cross OUT, Nelson (G) added | nflverse pbp/NGS passing | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Rec Yds Over 89.5 | 7 role/snaps | PASS | snap share stable L4; §7 3/4 [76.0, 102.0, 134.0, 150.0] | snap_counts_2026.parquet | 2026-11-02 05:03 |
| Jaxon Smith-Njigba Rec Yds Over 89.5 | 8 injuries | PASS | ESPN injuries 16:38 ET | ESPN injuries API | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Rec Yds Over 89.5 | 9 NGS | PASS | NGS thru Wk8 | nflverse NGS | 2026-11-02 05:03 |
| Jaxon Smith-Njigba Rec Yds Over 89.5 | 10 film | PASS | matched to pbp rows, src/film_matches.md | NFL YouTube captions (yt-dlp) + pbp | 2026-11-02 16:42 |
| Jaxon Smith-Njigba Rec Yds Over 89.5 | 11 weather | PASS | NWS+Open-Meteo 16:38 ET: precip 2%, wind 2.7, gust 3.4 mph, no flag | tools/weather_forecast.py | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Rec Yds Over 89.5 | 12 market/price | PASS | FD 89.5 -166, no-vig 0.588 (16:38 ET) | The Odds API pull_odds.py (FD/DK/Pinnacle) | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Rec Yds Over 89.5 | 13 game script | PASS | SEA -3.5 / total 46.5 | lines_m1638.json + 10G rule | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Rec Yds Over 89.5 | 14 edge/sims | PASS | edge +.103 shrunk +.046; §14 118 >= 107.4; MODEL-SUSPECT flag | tools/sim_v6.py 3x100k seed 20261101 | 2026-11-02 16:44 |
| Jaxon Smith-Njigba Rec Yds Over 89.5 | 15 correlation/ticket bar | FAIL | §11/§15 BAR: nested rung of open ticket JSN 70+ rec yds (live SGP, Ghost6 bankroll_slips.md 4:11 PM ET) | Ghost6 bankroll_slips.md + bet-log.csv | 2026-11-02 16:45 |
| Jaxon Smith-Njigba Rec Yds Over 109.5 | 1 sample | PASS | 4 games w/ current QB S.Darnold; season sample through Wk8 | nflverse pbp (src/play_by_play_2026.parquet) | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Rec Yds Over 109.5 | 2 opportunity | PASS | targets L4 [6, 8, 16, 12] | nflverse pbp + snap_counts | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Rec Yds Over 109.5 | 3 defense profile | PASS | opp defense profile (advstats_season_def, coverage_profile) | advstats_season_def + coverage_profile.json | 2026-11-02 05:09 |
| Jaxon Smith-Njigba Rec Yds Over 109.5 | 4 defender | PASS | see coverage block | PFR adv defense CHI (05:10) / SEA (Firecrawl 06:40) | 2026-11-02 05:10 |
| Jaxon Smith-Njigba Rec Yds Over 109.5 | 5 blitz/pressure | PASS | blitz CHI .411/SEA .221 (FTN); pressure PROXY; flag: Sweat+Simmons first game, not in CHI rate | FTN charting + features.json | 2026-11-02 05:03 |
| Jaxon Smith-Njigba Rec Yds Over 109.5 | 6 QB | PASS | QB S.Darnold; LT Cross OUT, Nelson (G) added | nflverse pbp/NGS passing | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Rec Yds Over 109.5 | 7 role/snaps | FAIL | §7 2/4; §7 2/4 [76.0, 102.0, 134.0, 150.0] | snap_counts_2026.parquet | 2026-11-02 05:03 |
| Jaxon Smith-Njigba Rec Yds Over 109.5 | 8 injuries | PASS | ESPN injuries 16:38 ET | ESPN injuries API | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Rec Yds Over 109.5 | 9 NGS | PASS | NGS thru Wk8 | nflverse NGS | 2026-11-02 05:03 |
| Jaxon Smith-Njigba Rec Yds Over 109.5 | 10 film | PASS | matched to pbp rows, src/film_matches.md | NFL YouTube captions (yt-dlp) + pbp | 2026-11-02 16:42 |
| Jaxon Smith-Njigba Rec Yds Over 109.5 | 11 weather | PASS | NWS+Open-Meteo 16:38 ET: precip 2%, wind 2.7, gust 3.4 mph, no flag | tools/weather_forecast.py | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Rec Yds Over 109.5 | 12 market/price | PASS | FD 109.5 +124, no-vig 0.421 (16:38 ET) | The Odds API pull_odds.py (FD/DK/Pinnacle) | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Rec Yds Over 109.5 | 13 game script | PASS | SEA -3.5 / total 46.5 | lines_m1638.json + 10G rule | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Rec Yds Over 109.5 | 14 edge/sims | PASS | avg p 0.556 edge +0.135 shrunk +0.118 | tools/sim_v6.py 3x100k seed 20261101 | 2026-11-02 16:44 |
| Jaxon Smith-Njigba Rec Yds Over 109.5 | 15 correlation/ticket bar | FAIL | §11/§15 BAR: nested rung of open ticket JSN 70+ rec yds (live SGP, Ghost6 bankroll_slips.md 4:11 PM ET) | Ghost6 bankroll_slips.md + bet-log.csv | 2026-11-02 16:45 |
| Jaxon Smith-Njigba Receptions Over 7.5 | 1 sample | PASS | 4 games w/ current QB S.Darnold; season sample through Wk8 | nflverse pbp (src/play_by_play_2026.parquet) | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Receptions Over 7.5 | 2 opportunity | PASS | targets L4 [6, 8, 16, 12] | nflverse pbp + snap_counts | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Receptions Over 7.5 | 3 defense profile | PASS | opp defense profile (advstats_season_def, coverage_profile) | advstats_season_def + coverage_profile.json | 2026-11-02 05:09 |
| Jaxon Smith-Njigba Receptions Over 7.5 | 4 defender | PASS | see coverage block | PFR adv defense CHI (05:10) / SEA (Firecrawl 06:40) | 2026-11-02 05:10 |
| Jaxon Smith-Njigba Receptions Over 7.5 | 5 blitz/pressure | PASS | blitz CHI .411/SEA .221 (FTN); pressure PROXY; flag: Sweat+Simmons first game, not in CHI rate | FTN charting + features.json | 2026-11-02 05:03 |
| Jaxon Smith-Njigba Receptions Over 7.5 | 6 QB | PASS | QB S.Darnold; LT Cross OUT, Nelson (G) added | nflverse pbp/NGS passing | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Receptions Over 7.5 | 7 role/snaps | FAIL | §7 2/4; §7 2/4 [5.0, 5.0, 12.0, 9.0] | snap_counts_2026.parquet | 2026-11-02 05:03 |
| Jaxon Smith-Njigba Receptions Over 7.5 | 8 injuries | PASS | ESPN injuries 16:38 ET | ESPN injuries API | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Receptions Over 7.5 | 9 NGS | PASS | NGS thru Wk8 | nflverse NGS | 2026-11-02 05:03 |
| Jaxon Smith-Njigba Receptions Over 7.5 | 10 film | PASS | matched to pbp rows, src/film_matches.md | NFL YouTube captions (yt-dlp) + pbp | 2026-11-02 16:42 |
| Jaxon Smith-Njigba Receptions Over 7.5 | 11 weather | PASS | NWS+Open-Meteo 16:38 ET: precip 2%, wind 2.7, gust 3.4 mph, no flag | tools/weather_forecast.py | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Receptions Over 7.5 | 12 market/price | PASS | FD 7.5 +106, no-vig 0.454 (16:38 ET) | The Odds API pull_odds.py (FD/DK/Pinnacle) | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Receptions Over 7.5 | 13 game script | PASS | SEA -3.5 / total 46.5 | lines_m1638.json + 10G rule | 2026-11-02 16:38 |
| Jaxon Smith-Njigba Receptions Over 7.5 | 14 edge/sims | PASS | avg p 0.550 edge +0.096 shrunk +0.081 | tools/sim_v6.py 3x100k seed 20261101 | 2026-11-02 16:44 |
| Jaxon Smith-Njigba Receptions Over 7.5 | 15 correlation/ticket bar | FAIL | §11 one slip per player | Ghost6 bankroll_slips.md + bet-log.csv | 2026-11-02 16:45 |
| Cooper Kupp Rec Yds Over 29.5 | 1 sample | PASS | 4 games w/ current QB S.Darnold; season sample through Wk8 | nflverse pbp (src/play_by_play_2026.parquet) | 2026-11-02 16:38 |
| Cooper Kupp Rec Yds Over 29.5 | 2 opportunity | PASS | targets L4 [2, 3, 10, 2] | nflverse pbp + snap_counts | 2026-11-02 16:38 |
| Cooper Kupp Rec Yds Over 29.5 | 3 defense profile | PASS | opp defense profile (advstats_season_def, coverage_profile) | advstats_season_def + coverage_profile.json | 2026-11-02 05:09 |
| Cooper Kupp Rec Yds Over 29.5 | 4 defender | UNVERIFIED | no per-defender numbers (Kyler Gordon slot: no PFR row pulled) | PFR adv defense CHI (05:10) / SEA (Firecrawl 06:40) | 2026-11-02 05:10 |
| Cooper Kupp Rec Yds Over 29.5 | 5 blitz/pressure | PASS | blitz CHI .411/SEA .221 (FTN); pressure PROXY; flag: Sweat+Simmons first game, not in CHI rate | FTN charting + features.json | 2026-11-02 05:03 |
| Cooper Kupp Rec Yds Over 29.5 | 6 QB | PASS | QB S.Darnold; LT Cross OUT, Nelson (G) added | nflverse pbp/NGS passing | 2026-11-02 16:38 |
| Cooper Kupp Rec Yds Over 29.5 | 7 role/snaps | FAIL | §7 1/4; §7 1/4 [13.0, 15.0, 50.0, 20.0] | snap_counts_2026.parquet | 2026-11-02 05:03 |
| Cooper Kupp Rec Yds Over 29.5 | 8 injuries | PASS | ESPN injuries 16:38 ET | ESPN injuries API | 2026-11-02 16:38 |
| Cooper Kupp Rec Yds Over 29.5 | 9 NGS | PASS | NGS thru Wk8 | nflverse NGS | 2026-11-02 05:03 |
| Cooper Kupp Rec Yds Over 29.5 | 10 film | UNVERIFIED | no caption cue matched to pbp | NFL YouTube captions (yt-dlp) + pbp | 2026-11-02 16:42 |
| Cooper Kupp Rec Yds Over 29.5 | 11 weather | PASS | NWS+Open-Meteo 16:38 ET: precip 2%, wind 2.7, gust 3.4 mph, no flag | tools/weather_forecast.py | 2026-11-02 16:38 |
| Cooper Kupp Rec Yds Over 29.5 | 12 market/price | PASS | FD 29.5 -113, no-vig 0.500 (16:38 ET) | The Odds API pull_odds.py (FD/DK/Pinnacle) | 2026-11-02 16:38 |
| Cooper Kupp Rec Yds Over 29.5 | 13 game script | PASS | SEA -3.5 / total 46.5 | lines_m1638.json + 10G rule | 2026-11-02 16:38 |
| Cooper Kupp Rec Yds Over 29.5 | 14 edge/sims | FAIL | no edge | tools/sim_v6.py 3x100k seed 20261101 | 2026-11-02 16:44 |
| Cooper Kupp Rec Yds Over 29.5 | 15 correlation/ticket bar | PASS | no open ticket on this player+stat | Ghost6 bankroll_slips.md + bet-log.csv | 2026-11-02 16:45 |
| Cooper Kupp Receptions Over 2.5 | 1 sample | PASS | 4 games w/ current QB S.Darnold; season sample through Wk8 | nflverse pbp (src/play_by_play_2026.parquet) | 2026-11-02 16:38 |
| Cooper Kupp Receptions Over 2.5 | 2 opportunity | PASS | targets L4 [2, 3, 10, 2] | nflverse pbp + snap_counts | 2026-11-02 16:38 |
| Cooper Kupp Receptions Over 2.5 | 3 defense profile | PASS | opp defense profile (advstats_season_def, coverage_profile) | advstats_season_def + coverage_profile.json | 2026-11-02 05:09 |
| Cooper Kupp Receptions Over 2.5 | 4 defender | UNVERIFIED | no per-defender numbers (Kyler Gordon slot: no PFR row pulled) | PFR adv defense CHI (05:10) / SEA (Firecrawl 06:40) | 2026-11-02 05:10 |
| Cooper Kupp Receptions Over 2.5 | 5 blitz/pressure | PASS | blitz CHI .411/SEA .221 (FTN); pressure PROXY; flag: Sweat+Simmons first game, not in CHI rate | FTN charting + features.json | 2026-11-02 05:03 |
| Cooper Kupp Receptions Over 2.5 | 6 QB | PASS | QB S.Darnold; LT Cross OUT, Nelson (G) added | nflverse pbp/NGS passing | 2026-11-02 16:38 |
| Cooper Kupp Receptions Over 2.5 | 7 role/snaps | FAIL | §7 1/4; §7 1/4 [1.0, 2.0, 5.0, 2.0] | snap_counts_2026.parquet | 2026-11-02 05:03 |
| Cooper Kupp Receptions Over 2.5 | 8 injuries | PASS | ESPN injuries 16:38 ET | ESPN injuries API | 2026-11-02 16:38 |
| Cooper Kupp Receptions Over 2.5 | 9 NGS | PASS | NGS thru Wk8 | nflverse NGS | 2026-11-02 05:03 |
| Cooper Kupp Receptions Over 2.5 | 10 film | UNVERIFIED | no caption cue matched to pbp | NFL YouTube captions (yt-dlp) + pbp | 2026-11-02 16:42 |
| Cooper Kupp Receptions Over 2.5 | 11 weather | PASS | NWS+Open-Meteo 16:38 ET: precip 2%, wind 2.7, gust 3.4 mph, no flag | tools/weather_forecast.py | 2026-11-02 16:38 |
| Cooper Kupp Receptions Over 2.5 | 12 market/price | PASS | FD 2.5 -160, no-vig 0.575 (16:38 ET) | The Odds API pull_odds.py (FD/DK/Pinnacle) | 2026-11-02 16:38 |
| Cooper Kupp Receptions Over 2.5 | 13 game script | PASS | SEA -3.5 / total 46.5 | lines_m1638.json + 10G rule | 2026-11-02 16:38 |
| Cooper Kupp Receptions Over 2.5 | 14 edge/sims | FAIL | negative edge | tools/sim_v6.py 3x100k seed 20261101 | 2026-11-02 16:44 |
| Cooper Kupp Receptions Over 2.5 | 15 correlation/ticket bar | PASS | no open ticket on this player+stat | Ghost6 bankroll_slips.md + bet-log.csv | 2026-11-02 16:45 |
| AJ Barner Rec Yds Under 29.5 | 1 sample | PASS | 4 games w/ current QB S.Darnold; season sample through Wk8 | nflverse pbp (src/play_by_play_2026.parquet) | 2026-11-02 16:38 |
| AJ Barner Rec Yds Under 29.5 | 2 opportunity | PASS | targets L4 [3, 5, 4, 5] | nflverse pbp + snap_counts | 2026-11-02 16:38 |
| AJ Barner Rec Yds Under 29.5 | 3 defense profile | FAIL | soft TE D | advstats_season_def + coverage_profile.json | 2026-11-02 05:09 |
| AJ Barner Rec Yds Under 29.5 | 4 defender | UNVERIFIED | ISS-05 | PFR adv defense CHI (05:10) / SEA (Firecrawl 06:40) | 2026-11-02 05:10 |
| AJ Barner Rec Yds Under 29.5 | 5 blitz/pressure | PASS | blitz CHI .411/SEA .221 (FTN); pressure PROXY; flag: Sweat+Simmons first game, not in CHI rate | FTN charting + features.json | 2026-11-02 05:03 |
| AJ Barner Rec Yds Under 29.5 | 6 QB | PASS | QB S.Darnold; LT Cross OUT, Nelson (G) added | nflverse pbp/NGS passing | 2026-11-02 16:38 |
| AJ Barner Rec Yds Under 29.5 | 7 role/snaps | PASS | snap share stable L4; §7 3/4 [12.0, 20.0, 16.0, 42.0] | snap_counts_2026.parquet | 2026-11-02 05:03 |
| AJ Barner Rec Yds Under 29.5 | 8 injuries | PASS | ESPN injuries 16:38 ET | ESPN injuries API | 2026-11-02 16:38 |
| AJ Barner Rec Yds Under 29.5 | 9 NGS | PASS | NGS thru Wk8 | nflverse NGS | 2026-11-02 05:03 |
| AJ Barner Rec Yds Under 29.5 | 10 film | UNVERIFIED | no caption cue matched to pbp | NFL YouTube captions (yt-dlp) + pbp | 2026-11-02 16:42 |
| AJ Barner Rec Yds Under 29.5 | 11 weather | PASS | NWS+Open-Meteo 16:38 ET: precip 2%, wind 2.7, gust 3.4 mph, no flag | tools/weather_forecast.py | 2026-11-02 16:38 |
| AJ Barner Rec Yds Under 29.5 | 12 market/price | PASS | FD 29.5 -113, no-vig 0.500 (16:38 ET) | The Odds API pull_odds.py (FD/DK/Pinnacle) | 2026-11-02 16:38 |
| AJ Barner Rec Yds Under 29.5 | 13 game script | PASS | SEA -3.5 / total 46.5 | lines_m1638.json + 10G rule | 2026-11-02 16:38 |
| AJ Barner Rec Yds Under 29.5 | 14 edge/sims | PASS | avg p 0.588 edge +0.088 shrunk +0.061 | tools/sim_v6.py 3x100k seed 20261101 | 2026-11-02 16:44 |
| AJ Barner Rec Yds Under 29.5 | 15 correlation/ticket bar | PASS | no open ticket on this player+stat | Ghost6 bankroll_slips.md + bet-log.csv | 2026-11-02 16:45 |
| AJ Barner Receptions Under 3.5 | 1 sample | PASS | 4 games w/ current QB S.Darnold; season sample through Wk8 | nflverse pbp (src/play_by_play_2026.parquet) | 2026-11-02 16:38 |
| AJ Barner Receptions Under 3.5 | 2 opportunity | PASS | targets L4 [3, 5, 4, 5] | nflverse pbp + snap_counts | 2026-11-02 16:38 |
| AJ Barner Receptions Under 3.5 | 3 defense profile | FAIL | soft TE D | advstats_season_def + coverage_profile.json | 2026-11-02 05:09 |
| AJ Barner Receptions Under 3.5 | 4 defender | UNVERIFIED | ISS-05 | PFR adv defense CHI (05:10) / SEA (Firecrawl 06:40) | 2026-11-02 05:10 |
| AJ Barner Receptions Under 3.5 | 5 blitz/pressure | PASS | blitz CHI .411/SEA .221 (FTN); pressure PROXY; flag: Sweat+Simmons first game, not in CHI rate | FTN charting + features.json | 2026-11-02 05:03 |
| AJ Barner Receptions Under 3.5 | 6 QB | PASS | QB S.Darnold; LT Cross OUT, Nelson (G) added | nflverse pbp/NGS passing | 2026-11-02 16:38 |
| AJ Barner Receptions Under 3.5 | 7 role/snaps | PASS | snap share stable L4; §7 3/4 [1.0, 3.0, 3.0, 4.0] | snap_counts_2026.parquet | 2026-11-02 05:03 |
| AJ Barner Receptions Under 3.5 | 8 injuries | PASS | ESPN injuries 16:38 ET | ESPN injuries API | 2026-11-02 16:38 |
| AJ Barner Receptions Under 3.5 | 9 NGS | PASS | NGS thru Wk8 | nflverse NGS | 2026-11-02 05:03 |
| AJ Barner Receptions Under 3.5 | 10 film | UNVERIFIED | no caption cue matched to pbp | NFL YouTube captions (yt-dlp) + pbp | 2026-11-02 16:42 |
| AJ Barner Receptions Under 3.5 | 11 weather | PASS | NWS+Open-Meteo 16:38 ET: precip 2%, wind 2.7, gust 3.4 mph, no flag | tools/weather_forecast.py | 2026-11-02 16:38 |
| AJ Barner Receptions Under 3.5 | 12 market/price | PASS | FD 3.5 -168, no-vig 0.586 (16:38 ET) | The Odds API pull_odds.py (FD/DK/Pinnacle) | 2026-11-02 16:38 |
| AJ Barner Receptions Under 3.5 | 13 game script | PASS | SEA -3.5 / total 46.5 | lines_m1638.json + 10G rule | 2026-11-02 16:38 |
| AJ Barner Receptions Under 3.5 | 14 edge/sims | PASS | avg p 0.684 edge +0.098 shrunk +0.043 | tools/sim_v6.py 3x100k seed 20261101 | 2026-11-02 16:44 |
| AJ Barner Receptions Under 3.5 | 15 correlation/ticket bar | PASS | no open ticket on this player+stat | Ghost6 bankroll_slips.md + bet-log.csv | 2026-11-02 16:45 |
| Emanuel Wilson Rush Yds Over 19.5 | 1 sample | PASS | 4 games w/ current QB S.Darnold; season sample through Wk8 | nflverse pbp (src/play_by_play_2026.parquet) | 2026-11-02 16:38 |
| Emanuel Wilson Rush Yds Over 19.5 | 2 opportunity | FAIL | committee | nflverse pbp + snap_counts | 2026-11-02 16:38 |
| Emanuel Wilson Rush Yds Over 19.5 | 3 defense profile | PASS | opp defense profile (advstats_season_def, coverage_profile) | advstats_season_def + coverage_profile.json | 2026-11-02 05:09 |
| Emanuel Wilson Rush Yds Over 19.5 | 4 defender | PASS | see coverage block | PFR adv defense CHI (05:10) / SEA (Firecrawl 06:40) | 2026-11-02 05:10 |
| Emanuel Wilson Rush Yds Over 19.5 | 5 blitz/pressure | PASS | blitz CHI .411/SEA .221 (FTN); pressure PROXY; flag: Sweat+Simmons first game, not in CHI rate | FTN charting + features.json | 2026-11-02 05:03 |
| Emanuel Wilson Rush Yds Over 19.5 | 6 QB | PASS | QB S.Darnold; LT Cross OUT, Nelson (G) added | nflverse pbp/NGS passing | 2026-11-02 16:38 |
| Emanuel Wilson Rush Yds Over 19.5 | 7 role/snaps | FAIL | role UNVERIFIED; §7 4/4 [81.0, 61.0, 52.0, 100.0] | snap_counts_2026.parquet | 2026-11-02 05:03 |
| Emanuel Wilson Rush Yds Over 19.5 | 8 injuries | PASS | ESPN injuries 16:38 ET | ESPN injuries API | 2026-11-02 16:38 |
| Emanuel Wilson Rush Yds Over 19.5 | 9 NGS | PASS | NGS thru Wk8 | nflverse NGS | 2026-11-02 05:03 |
| Emanuel Wilson Rush Yds Over 19.5 | 10 film | UNVERIFIED | no caption cue matched to pbp | NFL YouTube captions (yt-dlp) + pbp | 2026-11-02 16:42 |
| Emanuel Wilson Rush Yds Over 19.5 | 11 weather | PASS | NWS+Open-Meteo 16:38 ET: precip 2%, wind 2.7, gust 3.4 mph, no flag | tools/weather_forecast.py | 2026-11-02 16:38 |
| Emanuel Wilson Rush Yds Over 19.5 | 12 market/price | PASS | FD 19.5 -113, no-vig 0.500 (16:38 ET) | The Odds API pull_odds.py (FD/DK/Pinnacle) | 2026-11-02 16:38 |
| Emanuel Wilson Rush Yds Over 19.5 | 13 game script | PASS | SEA -3.5 / total 46.5 | lines_m1638.json + 10G rule | 2026-11-02 16:38 |
| Emanuel Wilson Rush Yds Over 19.5 | 14 edge/sims | FAIL | MODEL-SUSPECT | tools/sim_v6.py 3x100k seed 20261101 | 2026-11-02 16:44 |
| Emanuel Wilson Rush Yds Over 19.5 | 15 correlation/ticket bar | FAIL | §11 same player as open SGP (Swift 50+ rush+rec/Swift TD; Wilson 15+) | Ghost6 bankroll_slips.md + bet-log.csv | 2026-11-02 16:45 |

## Cut reasons by leg
- Caleb Williams Pass Yds Over 224.5 (-113): P13 10G underdog over BLOCKED (CHI +3.5); P14 edge +2.6 < +3
- Luther Burden III Rec Yds Under 52.5 (-113): §7 HARD: Williams-only form 1/4 unders (63,32,95,130)
- Luther Burden III Receptions Under 4.5 (-158): P14 negative edge
- Rome Odunze Rec Yds Under 38.5 (-113): P14 edge < +3; §7 0/4 unders
- Rome Odunze Receptions Under 3.5 (-180): P14 negative edge
- Colston Loveland Rec Yds Under 42.5 (-113): §7 2/4; P4 ISS-05 TE defender UNVERIFIED; P13 could-trail TE under; P14 MODEL-SUSPECT (median 12+ below line)
- Colston Loveland Receptions Under 4.5 (-154): §7 2/4 (0,1,6,7); P4 ISS-05
- D'Andre Swift Rush Yds Under 59.5 (-113): §7 HARD: Williams-only 2/4 (124,45,44,78); §11 one slip per player (open SGP)
- D'Andre Swift Rush+Rec Yds Under 86.5 (-113): P13 10G underdog rush+rec under BLOCKED; §7 1/4 (134,99,70,90); §11 one slip per player (open SGP)
- D'Andre Swift Rec Yds Over 21.5 (-113): P13 10G underdog over; P14 model p < .45; §11 one slip per player (open SGP)
- D'Andre Swift Receptions Over 3.5 (+112): P2 catches over needs 5+ tgt in 3 of L4 (1,5,5,4 = 2/4); P13 10G underdog over; P14 edge +2.5 < +3 and medians 3.0 do not clear 3.5; P15 open-ticket status of Swift 3+ rec UNCONFIRMED (r2/odunze/results.md ~1:20 PM ET says placed; the 7-leg ticket holding it was cashed out per Ghost6 4:10 PM ET); barred fail-closed as nested rung
- D'Andre Swift Receptions Over 2.5 (-225): P14 shrunk edge -3.1; P15 open-ticket status of Swift 3+ rec UNCONFIRMED (r2/odunze/results.md ~1:20 PM ET says placed; the 7-leg ticket holding it was cashed out per Ghost6 4:10 PM ET); barred fail-closed as nested rung; P2 tgt
- Roschon Johnson Rush Yds Over 10.5 (-113): P3 SEA allows 3.40 YPC; P7 RB2 role; P13 underdog RB; P14 MODEL-SUSPECT (fixA boost); §7 only 2 games with carries
- Sam Darnold Pass Yds Over 238.5 (-113): P8 backup LT (Cross OUT) -> no QB yardage over; §7 2/4
- Jaxon Smith-Njigba Rec Yds Over 99.5 (-113): §14 cushion FAIL at -113 (L4 median 118 < 124.4; 1.10x hit 2/4); P14 MODEL-SUSPECT (MC median 119.1, +19.6 vs line; press -> manual review); §11/§15 BAR: nested rung of open ticket JSN 70+ rec yds (live SGP, Ghost6 bankroll_slips.md 4:11 PM ET)
- Jaxon Smith-Njigba Rec Yds Over 89.5 (-166): P14 MODEL-SUSPECT (press -> MANUAL_REVIEW on numbers alone); §11/§15 BAR: nested rung of open ticket JSN 70+ rec yds (live SGP, Ghost6 bankroll_slips.md 4:11 PM ET)
- Jaxon Smith-Njigba Rec Yds Over 109.5 (+124): §7 2/4 at 109.5; §11/§15 BAR: nested rung of open ticket JSN 70+ rec yds (live SGP, Ghost6 bankroll_slips.md 4:11 PM ET)
- Jaxon Smith-Njigba Receptions Over 7.5 (+106): §7 2/4 (5,5,12,9); §11 same player as open SGP (JSN 70+, JSN TD)
- Cooper Kupp Rec Yds Over 29.5 (-113): P14 no edge; §7 1/4
- Cooper Kupp Receptions Over 2.5 (-160): P14 negative edge; §7 1/4
- AJ Barner Rec Yds Under 29.5 (-113): P3 soft CHI TE D (TE YPT 8.61); P4 ISS-05
- AJ Barner Receptions Under 3.5 (-168): P3; P4 ISS-05
- Emanuel Wilson Rush Yds Over 19.5 (-113): P2/P7 role change: Charbonnet (no designation) + Price activated 4:05 PM ET -> 3-way committee; P14 MODEL-SUSPECT (sim p .95 on 63 median; no split data); §11 one slip per player (open SGP)

---
## Phase 15: inactives and reprice (run 7:00 PM ET Nov 2; kickoff 8:15 PM ET)
Sources: ESPN summary API event 401873036 (inactives stamped 6:47–6:51 PM ET, saved phase15/espn_summary_1858.json); @seahawksPR, Brad Biggs, Courtney Cronin, Brady Henderson on X (6:45–6:57 PM ET); The Odds API FD/PrizePicks/Pinnacle pull 7:00 PM ET (phase15/odds_m1900.csv, odds_td_tot_m1900.json; in-play filter ON, 0 dropped); Open-Meteo Lumen Field hourly 7:00 PM ET.

### Official inactives
- **CHI:** CB Malik Muhammad II (toe; was QUESTIONABLE, limited all week; NEW, first missed game), RB Kyle Monangai (thumb/toe, expected), G Jordan McFadden, DT Jayden Loving, DT Jordan van den Berg, QB Case Keenum (emergency 3rd QB).
- **SEA:** WR Rashid Shaheed (knee), LT Charles Cross (ankle), OLB Uchenna Nwosu (ankle; was Doubtful), RB Velus Jones Jr. (hamstring), NT Brandon Pili (back), G Beau Stephens, QB Drew Lock (emergency 3rd QB).
- **Active / confirmed:** Montez Sweat and Jeffery Simmons (CHI) and Quenton Nelson (SEA) not on inactive lists. SEA activated RB Jadarian Price from IR; gameday elevations WR Montorie Foster, OT Bobby Hart (SEA), TE Stephen Carlson (CHI).
- No late scratch of any player on a placed ticket.

### Placed-ticket legs (live SGP per Ghost6 bankroll_slips.md 4:11 PM ET)
| Leg | Status | Reason | Line 4:38 PM | Line 7:00 PM |
|---|---|---|---|---|
| JSN 70+ rec yds | HELPED | Muhammad (the RCB he was mapped to, 55% of his snaps, defense_profile.md) is OUT; Shaheed OUT keeps his target share up. Muhammad's backup isn't in the CB data (gap). | FD 69.5 -360 | FD 69.5 -360 (unchanged); main 99.5 -113 |
| JSN anytime TD | HELPED (slightly) | Same CB news | — | FD -105 (Pinnacle -110/-110) |
| Swift 50+ rush+rec | HELPED | Monangai OUT, so Swift leads; Roschon Johnson is the only other CHI RB with a line (O10.5) | FD main 86.5 -113 | FD 86.5 -113 (unchanged); rush 49.5 -210 |
| Swift anytime TD | NEUTRAL | No change | — | FD -105 |
| E. Wilson 15+ rush | NEUTRAL (risk already known) | 4-way SEA split stays: Charbonnet, Price, Wilson, Holani active; Velus Jones OUT (was not a carry threat) | FD 14.5 -178 | FD 14.5 -192 (market moved toward him) |
| Under 58.5 total | NEUTRAL | Main total unchanged | FD 46.5 -110 | FD 46.5 -110 |
| Swift 3+ rec (ticket status UNCONFIRMED) | SLIGHTLY HURT on price | Market drifting off his catches | FD 2.5 -225, 3.5 +112 | FD 2.5 -205, 3.5 +118/+120 |
| Burden 4+ rec / Burden 30+ yds (ticket status UNCONFIRMED) | NEUTRAL | No news | FD 3.5 -188, 29.5 -420 | FD 3.5 -192, 29.5 -440 |
No leg is voided. No placed leg is on a Questionable player (JSN, Swift, Wilson, Burden had no designation), so no backup swap is needed.

### Backfield-split check (placed RB legs)
- **CHI (Swift 50+ rush+rec, Swift TD):** Active RBs are Swift and Roschon Johnson (Monangai OUT). There's no returning back. Swift's rush and rush+rec lines didn't move after the news, so the market had priced Monangai out. Flag: none.
- **SEA (Wilson 15+ rush):** Active RBs are Charbonnet (back from knee, no designation), Jadarian Price (activated from IR, per Schefter at 4:05 PM ET), Wilson, and Holani. Earlier projection: Price ~30, Charbonnet ~25, Wilson ~21, Holani ~8 rush yds. There's no new beat report on the snap plan after inactives. **FLAG: Wilson's leg sits in a committee with two returning backs who could take carries.** The market still prices 14.5 at -192.

### Exposure per player (all known open tickets)
- JSN: 2 legs (70+ rec yds and TD, same SGP).
- Swift: 2 confirmed legs (50+ R+R and TD, same SGP), plus Swift 3+ rec if that ticket is still open (UNCONFIRMED). That's up to 3. **FLAG.**
- Burden: 4+ rec and 30+ yds, UNCONFIRMED.
- Wilson: 1. Game total: 1 (Under 58.5).

### New-info effects on the r3 card (all 23 still CUT)
- Muhammad OUT is the one real change. It helps every SEA WR rung, but JSN rec-yds rungs stay barred as nested in the open JSN 70+ ticket. CHI is missing 1 confirmed CB tonight (Muhammad). A second missing corner is not confirmed, so the WR3-over exception (2+ corners) is **not** triggered.
- Weather (Open-Meteo, 5–7 PM PT): 44–45°F, 1–2% precip, wind 2–5 mph with gusts up to 8 mph. No flag.
- Read only. No bets placed.
