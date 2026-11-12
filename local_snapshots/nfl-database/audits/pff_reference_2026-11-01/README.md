# PFF audit reference set (pulled 2026-11-01, 22:28-22:34 ET)
| File | Source URL | What |
|---|---|---|
| om_archive_{TPA,MIA,ATL}.json / om_forecast_* | archive-api.open-meteo.com/v1/archive, api.open-meteo.com/v1/forecast | Hourly actual + forecast (ATL coords = wrong venue, kept as a control) |
| nws_KTPA.json, nws_KMIA.json | api.weather.gov/stations/{KTPA,KMIA}/observations | Station obs, 17:00-22:00Z |
| weather_wk8.json | (summary of above) + nflverse pbp weather strings for Wk7 open-air | Game-window summary |
| espn_winrates.html / espn_winrates_thru_wk7.json | espn.com/nfl/story/_/id/49742016 | PRWR/RSWR/PBWR/RBWR, "thru Wk7, Oct 27 10 AM ET" |
| own_ol.py / own_ol_run_blocking.json | nflverse pbp parquet (mtime Nov 1 07:09) | Our opp-adjusted run-block composite thru Wk7 |
| player_stats_wk8.json | site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event=… | Wk8 box lines |
| injury_status_wk8.txt | ESPN injuries API files 11:52 + 18:52 ET | Status |
| espn_sb_wk1..8.json, espn_standings.json | site.api.espn.com …/scoreboard?week=N, …/apis/v2/…/standings | Records + finals |
