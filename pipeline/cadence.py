"""Per-source publish cadence for the freshness gate (NFL-56, Rico 2026-11-22).

Rico: a weekly or sporadic source is CURRENT if it is still the latest published asset (release/asset
timestamp or digest unchanged) AND it covers every completed game. Missing coverage of a completed
game is GAP, not STALE. NWS is current if updateTime matches the live grid. Live sources (lines,
ESPN, schedule) keep pull-time windows. Inactives keep the T-90 rule.

Evidence and typical windows were checked 2026-11-22 02:07 AST (UTC-4). Do not invent a cadence;
comments cite the source. Full table: see the research handoff (source_cadence_2026-11-22).
"""
from __future__ import annotations

# rule:
#   latest_release  weekly/sporadic publisher files — FRESH if this copy is still the latest asset
#                   and it covers every completed game; GAP if latest but a completed game is missing;
#                   STALE if a newer asset has superseded our copy. No flat max-age clock.
#   live_window     live or frequently updated sources — existing pull-time / as-of age windows.
#   nws_live_grid   FRESH if our updateTime is the current NWS grid (not superseded). No max-age clock.
#   t90             official inactives: NOT_YET before T-90; must be pulled after they post.
#
# coverage:
#   completed_games inspect the file (or packet data_freshness for play-by-play) against completed games
#   None            no game-coverage check (rosters, depth charts, official injuries)

CADENCE = {
    "schedule": {
        "rule": "live_window",
        "coverage": None,
        # nflreadr: game/schedule data "updates very 5 minutes during the season".
        # Observed 2026-11-22: nfldata data/games.csv commits Sat 15:05–Sun 00:45 ET at :05/:15/:35/:45
        # (10 or 20 min gaps). Asset games.parquet updated_at 2026-11-22T05:46:19Z (Sun 00:46 ET).
        # Evidence: https://nflreadr.nflverse.com/articles/nflverse_data_schedule.html
        #           https://github.com/nflverse/nflverse-data/releases/tag/schedules
        #           https://github.com/nflverse/nfldata/commits/master/data/games.csv
        "evidence": "https://nflreadr.nflverse.com/articles/nflverse_data_schedule.html",
    },
    "play_by_play": {
        "rule": "latest_release",
        "coverage": "completed_games",
        # Nightly after each game day plus game-day windows (nflverse-pbp update_data.yaml crons).
        # Thursday morning is the cleanest after official Mon–Wed stat corrections.
        # Last 2026 asset at check: Sat 11:46 ET (through TNF; no Sunday games yet).
        # Evidence: https://nflreadr.nflverse.com/articles/nflverse_data_schedule.html
        #           https://github.com/nflverse/nflverse-pbp/blob/master/.github/workflows/update_data.yaml
        "evidence": "https://nflreadr.nflverse.com/articles/nflverse_data_schedule.html",
    },
    "rosters": {
        "rule": "latest_release",
        "coverage": None,
        # YAML cron 07:07 UTC daily; observed ~02:00 ET dispatch + mid-morning scheduled run.
        # Last weekly roster asset at check: Sat 10:20 ET.
        # Evidence: https://github.com/nflverse/nflverse-rosters/blob/main/.github/workflows/update_rosters.yaml
        "evidence": "https://nflreadr.nflverse.com/articles/nflverse_data_schedule.html",
    },
    "depth_charts": {
        "rule": "latest_release",
        "coverage": None,
        # Same daily job pattern as rosters. Last asset at check: Sat 10:17 ET.
        # The former 12 h-inside-48 h clock marked the newest chart STALE on Sunday. Dropped.
        # Evidence: https://github.com/nflverse/nflverse-rosters/blob/main/.github/workflows/update_depth_charts.yaml
        "evidence": "https://nflreadr.nflverse.com/articles/nflverse_data_schedule.html",
    },
    "snap_counts": {
        "rule": "latest_release",
        "coverage": "completed_games",
        # nflverse scrapes 00/06/12/18 UTC; new rows depend on PFR (upstream clock unknown).
        # Last 2026 asset at check: Fri 07:01 ET; later jobs ran with the digest unchanged.
        # File held weeks 1–10 + W11 TNF only. A 24 h clock marked it STALE from Sat 07:01 ET.
        # Evidence: https://github.com/nflverse/nflverse-pfr/blob/master/.github/workflows/update_snap_counts.yaml
        "evidence": "https://nflreadr.nflverse.com/articles/nflverse_data_schedule.html",
    },
    "ftn_charting": {
        "rule": "latest_release",
        "coverage": "completed_games",
        # nflverse job every 6 h in season; new rows depend on FTN (FTN's own clock unknown).
        # Last 2026 asset at check: Sat 09:11 ET; weeks 1–10 + W11 TNF only.
        # Evidence: https://github.com/nflverse/nflverse-ftn/blob/main/.github/workflows/update_ftn.yaml
        "evidence": "https://nflreadr.nflverse.com/articles/nflverse_data_schedule.html",
    },
    "pfr_defense": {
        "rule": "latest_release",
        "coverage": "completed_games",
        # Same 6 h nflverse scrape as snaps; new rows depend on PFR.
        # Last 2026 weekly def file at check: Thu 13:02 ET, through week 10 only (TNF missing).
        # Sunday 01:02 ET job ran; the 2026 file was not replaced.
        # Evidence: https://github.com/nflverse/nflverse-pfr/blob/master/.github/workflows/update_advanced_stats.yaml
        "evidence": "https://nflreadr.nflverse.com/articles/nflverse_data_schedule.html",
    },
    "official_injuries": {
        "rule": "latest_release",
        "coverage": None,
        # Official Practice / Game Status Reports due 4:00 p.m. New York time (or after practice);
        # day shifts with game day. See NFL 2026-27 important dates.
        # nflverse injuries: cron 07:07 UTC in season; observed ~02:00 ET + mid-morning.
        # Last asset at check: Sat 10:16 ET, including Week 11 Out/Doubtful/Questionable.
        # Evidence: https://www.nfl.com/news/2026-27-national-football-league-important-dates
        #           https://github.com/nflverse/nflverse-rosters/blob/main/.github/workflows/update_injuries.yaml
        "evidence": "https://www.nfl.com/news/2026-27-national-football-league-important-dates",
    },
    "news_injuries": {
        "rule": "live_window",
        "coverage": None,
        # ESPN live list; Cache-Control max-age=5. Pull time is the quote time.
        # Evidence: https://site.api.espn.com/apis/site/v2/sports/football/nfl/injuries (headers 2026-11-22 02:07 AST)
        "evidence": "https://site.api.espn.com/apis/site/v2/sports/football/nfl/injuries",
    },
    "weather": {
        "rule": "nws_live_grid",
        "coverage": None,
        # No fixed issuance clock. Offices often twice daily; can be ~12 h. API CDN s-maxage=3600.
        # Date by properties.updateTime matching the live grid, not by how old that stamp is.
        # Observed 2026-11-22 01:07 ET: PHI updateTime Sat 16:07 ET was still the current grid (>6 h old).
        # Evidence: https://www.weather.gov/documentation/services-web-api
        #           https://github.com/weather-gov/api/discussions/859
        "evidence": "https://www.weather.gov/documentation/services-web-api",
    },
    "odds": {
        "rule": "live_window",
        "coverage": None,
        # Live book quotes at request time. Pull time is the quote time. Tightens near kickoff.
        "evidence": "pipeline/freshness.py live_pull (book prices)",
    },
    "ngs_passing": {
        "rule": "latest_release",
        "coverage": "completed_games",
        # Public weekly NGS only (no NFL Pro). nflverse ngs-data cron 07:00 UTC; observed ~02:00 ET
        # plus mid-morning. Last assets at check: Sat 10:02 ET.
        # Evidence: https://nflreadr.nflverse.com/articles/nflverse_data_schedule.html
        #           https://github.com/nflverse/ngs-data/blob/main/.github/workflows/update_ngs.yaml
        "evidence": "https://nflreadr.nflverse.com/articles/dictionary_nextgen_stats.html",
    },
    "ngs_receiving": {
        "rule": "latest_release",
        "coverage": "completed_games",
        "evidence": "https://nflreadr.nflverse.com/articles/dictionary_nextgen_stats.html",
    },
    "ngs_rushing": {
        "rule": "latest_release",
        "coverage": "completed_games",
        "evidence": "https://nflreadr.nflverse.com/articles/dictionary_nextgen_stats.html",
    },
}

# Hooked inputs (not in POLICY paths). Official inactives keep T-90; four-book prices follow odds.
HOOKED_CADENCE = {
    "official_inactives": {
        "rule": "t90",
        "coverage": None,
        # Clubs post official Inactives articles about 90 min before kickoff. The 2026-27 important
        # dates page has no 90-minute line (checked 2026-11-22). Repo window unchanged.
        "evidence": "pipeline/freshness.py INACTIVES_POST_MINUTES_BEFORE_KICKOFF; phase15/official_inactives.py",
    },
    "four_book_prices": {
        "rule": "live_window",
        "coverage": None,
        # Same windows as odds. Default required books (owner 2026-11-21): fanduel, draftkings, betmgm, bovada.
        "evidence": "pipeline/hooks.py REQUIRED_BOOKS; pregame/direct_books.py",
    },
    "ngs_defender_matchup": {
        "rule": "latest_release",
        "coverage": "completed_games",
        # Game-day check: WR/RB route and target-location data plus QB pass-location/success splits
        # for both teams, used for the main-defender step. Public NGS weekly files do not carry those
        # splits; missing fields are listed as MISSING/unknown, never zero.
        "evidence": "https://nflreadr.nflverse.com/articles/dictionary_nextgen_stats.html",
    },
}


def rule_for(name: str) -> str:
    if name in CADENCE:
        return CADENCE[name]["rule"]
    if name in HOOKED_CADENCE:
        return HOOKED_CADENCE[name]["rule"]
    return "live_window"


def coverage_for(name: str):
    if name in CADENCE:
        return CADENCE[name]["coverage"]
    if name in HOOKED_CADENCE:
        return HOOKED_CADENCE[name]["coverage"]
    return None
