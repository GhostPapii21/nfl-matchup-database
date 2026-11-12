#!/bin/bash
# Shared fresh pulls for Nov 1 2026 game-day run. Logs ET timestamps. Never prints keys.
cd "$(dirname "$0")"
B=https://github.com/nflverse/nflverse-data/releases/download
log(){ echo "$(date '+%Y-%m-%d %H:%M') $*" >> pull_log.txt; }
for f in pbp/play_by_play_2026.parquet nextgen_stats/ngs_2026_passing.parquet nextgen_stats/ngs_2026_receiving.parquet nextgen_stats/ngs_2026_rushing.parquet ftn_charting/ftn_charting_2026.parquet snap_counts/snap_counts_2026.parquet players/players.parquet pbp_participation/pbp_participation_2026.parquet; do
  o=$(basename $f); code=$(curl -sL -w '%{http_code}' -o "$o" "$B/$f"); log "curl nflverse $f -> $code $(stat -c%s "$o" 2>/dev/null) bytes magic=$(head -c4 "$o" | xxd -p) tail=$(tail -c4 "$o" | xxd -p)"
done
code=$(curl -s -w '%{http_code}' -o espn_injuries.json "https://site.api.espn.com/apis/site/v2/sports/football/nfl/injuries"); log "curl espn injuries -> $code"
code=$(curl -s -w '%{http_code}' -o pfr_def_adv_2026_fresh.html -A "Mozilla/5.0" "https://www.pro-football-reference.com/years/2026/defense_advanced.htm"); log "curl PFR defense_advanced 2026 -> $code $(stat -c%s pfr_def_adv_2026_fresh.html) bytes"
code=$(curl -s -w '%{http_code}' -o espn_scoreboard.json "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates=20261101"); log "curl espn scoreboard -> $code"
log done
