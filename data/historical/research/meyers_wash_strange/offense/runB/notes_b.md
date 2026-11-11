# JAX Weeks 1–8, 2026 / BAL defense — run B

All network fetches used curl against public HTML pages. No login, private API, undocumented API, or PFF Premium was used. Raw responses, including errors/challenges, are in `raw/`. Times below are America/New_York with UTC offsets; they record request start. `fetch_log.csv` records every curl attempt, redirects, status, and curl exit. PFR requests were sequential with a 3-second sleep before each.

## Verified receiving game logs

Values below are transcribed from fetched ESPN tables, not independently confirmed against NGS/PFR. Each row links to its source and records fetch time. ESPN labels all three logs **2026 Regular Season (JAX)**. Meyers therefore played for **JAX in every listed game**. Week 7 is a bye, not an observed zero-stat game.

| Player | Week | Date | Opponent | Team | Targets | Receptions | Yards | URL | Fetch time ET |
|---|---|---|---|---|---|---|---|---|---|
| Meyers | 1 | Sun 9/13 | vs CLE | JAX | 2 | 2 | 40 | [espn_meyers](https://www.espn.com/nfl/player/gamelog/_/id/3916433/type/nfl/year/2026) | 2026-11-04T17:10:09-05:00 |
| Meyers | 2 | Sun 9/20 | @ DEN | JAX | 1 | 1 | 28 | [espn_meyers](https://www.espn.com/nfl/player/gamelog/_/id/3916433/type/nfl/year/2026) | 2026-11-04T17:10:09-05:00 |
| Meyers | 3 | Sun 9/27 | vs NE | JAX | 8 | 7 | 64 | [espn_meyers](https://www.espn.com/nfl/player/gamelog/_/id/3916433/type/nfl/year/2026) | 2026-11-04T17:10:09-05:00 |
| Meyers | 4 | Sun 10/4 | @ CIN | JAX | 4 | 3 | 33 | [espn_meyers](https://www.espn.com/nfl/player/gamelog/_/id/3916433/type/nfl/year/2026) | 2026-11-04T17:10:09-05:00 |
| Meyers | 5 | Sun 10/11 | vs PHI | JAX | 3 | 2 | 37 | [espn_meyers](https://www.espn.com/nfl/player/gamelog/_/id/3916433/type/nfl/year/2026) | 2026-11-04T17:10:09-05:00 |
| Meyers | 6 | Sun 10/18 | vs HOU | JAX | 10 | 5 | 83 | [espn_meyers](https://www.espn.com/nfl/player/gamelog/_/id/3916433/type/nfl/year/2026) | 2026-11-04T17:10:09-05:00 |
| Meyers | 8 | Sun 11/1 | vs IND | JAX | 3 | 2 | 24 | [espn_meyers](https://www.espn.com/nfl/player/gamelog/_/id/3916433/type/nfl/year/2026) | 2026-11-04T17:10:09-05:00 |
| Meyers | 7 | BYE | — | JAX (season affiliation) | N/A (bye) | N/A (bye) | N/A (bye) | [espn_jax_schedule](https://www.espn.com/nfl/team/schedule/_/name/jax/season/2026) | 2026-11-04T17:10:33-05:00 |
| Washington | 1 | Sun 9/13 | vs CLE | JAX | 6 | 5 | 83 | [espn_washington](https://www.espn.com/nfl/player/gamelog/_/id/4432620/type/nfl/year/2026) | 2026-11-04T17:10:09-05:00 |
| Washington | 2 | Sun 9/20 | @ DEN | JAX | 12 | 7 | 98 | [espn_washington](https://www.espn.com/nfl/player/gamelog/_/id/4432620/type/nfl/year/2026) | 2026-11-04T17:10:09-05:00 |
| Washington | 3 | Sun 9/27 | vs NE | JAX | 5 | 3 | 40 | [espn_washington](https://www.espn.com/nfl/player/gamelog/_/id/4432620/type/nfl/year/2026) | 2026-11-04T17:10:09-05:00 |
| Washington | 4 | Sun 10/4 | @ CIN | JAX | 3 | 1 | 7 | [espn_washington](https://www.espn.com/nfl/player/gamelog/_/id/4432620/type/nfl/year/2026) | 2026-11-04T17:10:09-05:00 |
| Washington | 5 | Sun 10/11 | vs PHI | JAX | 9 | 6 | 124 | [espn_washington](https://www.espn.com/nfl/player/gamelog/_/id/4432620/type/nfl/year/2026) | 2026-11-04T17:10:09-05:00 |
| Washington | 6 | Sun 10/18 | vs HOU | JAX | 11 | 4 | 64 | [espn_washington](https://www.espn.com/nfl/player/gamelog/_/id/4432620/type/nfl/year/2026) | 2026-11-04T17:10:09-05:00 |
| Washington | 8 | Sun 11/1 | vs IND | JAX | 2 | 1 | 16 | [espn_washington](https://www.espn.com/nfl/player/gamelog/_/id/4432620/type/nfl/year/2026) | 2026-11-04T17:10:09-05:00 |
| Washington | 7 | BYE | — | JAX (season affiliation) | N/A (bye) | N/A (bye) | N/A (bye) | [espn_jax_schedule](https://www.espn.com/nfl/team/schedule/_/name/jax/season/2026) | 2026-11-04T17:10:33-05:00 |
| Strange | 1 | Sun 9/13 | vs CLE | JAX | 3 | 2 | 23 | [espn_strange](https://www.espn.com/nfl/player/gamelog/_/id/4430539/type/nfl/year/2026) | 2026-11-04T17:10:09-05:00 |
| Strange | 2 | Sun 9/20 | @ DEN | JAX | 2 | 2 | 17 | [espn_strange](https://www.espn.com/nfl/player/gamelog/_/id/4430539/type/nfl/year/2026) | 2026-11-04T17:10:09-05:00 |
| Strange | 3 | Sun 9/27 | vs NE | JAX | 5 | 3 | 32 | [espn_strange](https://www.espn.com/nfl/player/gamelog/_/id/4430539/type/nfl/year/2026) | 2026-11-04T17:10:09-05:00 |
| Strange | 4 | Sun 10/4 | @ CIN | JAX | 8 | 7 | 95 | [espn_strange](https://www.espn.com/nfl/player/gamelog/_/id/4430539/type/nfl/year/2026) | 2026-11-04T17:10:09-05:00 |
| Strange | 5 | Sun 10/11 | vs PHI | JAX | 8 | 7 | 68 | [espn_strange](https://www.espn.com/nfl/player/gamelog/_/id/4430539/type/nfl/year/2026) | 2026-11-04T17:10:09-05:00 |
| Strange | 6 | Sun 10/18 | vs HOU | JAX | 7 | 5 | 44 | [espn_strange](https://www.espn.com/nfl/player/gamelog/_/id/4430539/type/nfl/year/2026) | 2026-11-04T17:10:09-05:00 |
| Strange | 8 | Sun 11/1 | vs IND | JAX | 2 | 2 | 55 | [espn_strange](https://www.espn.com/nfl/player/gamelog/_/id/4430539/type/nfl/year/2026) | 2026-11-04T17:10:09-05:00 |
| Strange | 7 | BYE | — | JAX (season affiliation) | N/A (bye) | N/A (bye) | N/A (bye) | [espn_jax_schedule](https://www.espn.com/nfl/team/schedule/_/name/jax/season/2026) | 2026-11-04T17:10:33-05:00 |

Schedule/week mapping and Week 7 bye source: [espn_jax_schedule](https://www.espn.com/nfl/team/schedule/_/name/jax/season/2026) | 2026-11-04T17:10:33-05:00. The fetched schedule labels the forthcoming Baltimore game Week 9; the requested directory name is retained. No Weeks 9+ stats are used.

## Requested advanced metrics

| Subject | Requested values | Result / reason | URL | Fetch time ET |
|---|---|---|---|---|
| Meyers, Weeks 1–8 | Average separation; cushion; share of team air yards; aDOT / average intended air yards | UNAVAILABLE: NGS HTML is an application shell; no player rows or metric data. Season sorted URL returned 404. All/week routes returned 200 shells. | [ngs_receiving_all](https://nextgenstats.nfl.com/stats/receiving/2026/REG/all) | 2026-11-04T17:10:34-05:00 |
| Meyers, Weeks 1–8 | PFR advanced receiving fields | UNAVAILABLE: HTTP 403 challenge; no regular or comment-hidden tables. | [pfr_meyers](https://www.pro-football-reference.com/players/M/MeyeJa01/gamelog/2026/advanced/) | 2026-11-04T17:10:08-05:00 |
| Washington, Weeks 1–8 | Average separation; cushion; share of team air yards; aDOT / average intended air yards | UNAVAILABLE: NGS HTML is an application shell; no player rows or metric data. Season sorted URL returned 404. All/week routes returned 200 shells. | [ngs_receiving_all](https://nextgenstats.nfl.com/stats/receiving/2026/REG/all) | 2026-11-04T17:10:34-05:00 |
| Washington, Weeks 1–8 | PFR advanced receiving fields | UNAVAILABLE: HTTP 403 challenge; no regular or comment-hidden tables. | [pfr_washington](https://www.pro-football-reference.com/players/W/WashPa00/gamelog/2026/advanced/) | 2026-11-04T17:10:12-05:00 |
| Strange, Weeks 1–8 | Average separation; cushion; share of team air yards; aDOT / average intended air yards | UNAVAILABLE: NGS HTML is an application shell; no player rows or metric data. Season sorted URL returned 404. All/week routes returned 200 shells. | [ngs_receiving_all](https://nextgenstats.nfl.com/stats/receiving/2026/REG/all) | 2026-11-04T17:10:34-05:00 |
| Strange, Weeks 1–8 | PFR advanced receiving fields | UNAVAILABLE: HTTP 403 challenge; no regular or comment-hidden tables. | [pfr_strange](https://www.pro-football-reference.com/players/S/StraBr00/gamelog/2026/advanced/) | 2026-11-04T17:10:15-05:00 |
| Trevor Lawrence, Weeks 1–8 | Time to throw; aggressiveness | UNAVAILABLE: NGS passing pages return application shells without player metrics. | [ngs_passing_all](https://nextgenstats.nfl.com/stats/passing/2026/REG/all) | 2026-11-04T17:10:36-05:00 |
| Trevor Lawrence, Weeks 1–8 | Pressure%; bad throw%; other advanced passing fields | UNAVAILABLE: PFR HTTP 403 challenge; no regular or comment-hidden tables. | [pfr_lawrence](https://www.pro-football-reference.com/players/L/LawrTr00/gamelog/2026/advanced/) | 2026-11-04T17:10:18-05:00 |
| BAL defense, Weeks 1–8 | Blitz%; pressure%; hurries; QB knockdowns (and rates if present) | UNAVAILABLE: PFR opponent page HTTP 403 challenge; no tables. No verified Week 1–8 aggregate. | [pfr_opp](https://www.pro-football-reference.com/years/2026/opp.htm) | 2026-11-04T17:10:02-05:00 |
| JAX team, 2026 | Team receiving/passing cross-check | UNAVAILABLE: PFR team page HTTP 403 challenge. | [pfr_jax](https://www.pro-football-reference.com/teams/jax/2026.htm) | 2026-11-04T17:10:05-05:00 |

## HTML/comment parsing audit

BeautifulSoup parsed every saved response and separately parsed each HTML comment for `<table>` elements. The audit is saved in `parse_audit.json`. All six PFR responses have title “Just a moment...” and contain no tables, including in comments. Successful NGS responses contain no tables and expose only the NGS title as visible text; HTTP 200 does not establish data availability. No attempt was made to bypass the challenge or obtain backing API data.

## Existing local images (visually inspected)

These are existing artifacts, not fresh page fetches. Original capture time and full route-chart URL are UNAVAILABLE. Filenames supply week/opponent context where not visible in the crop. Route names below are visual interpretations of shapes, not official play-call classifications. Green tracks are after-catch movement, not additional routes.

| File under `week10/ngs/` | Visible content / interpretation |
|---|---|
| `route_meyers_wk3_vsNE.png` | Chart explicitly labels Jakobi Meyers / 2026 vs Patriots. Shows crossing/in-breaking and out-breaking shapes across the shallow and intermediate field, with a blue touchdown marker in the intermediate middle. Green extensions show after-catch movement across the middle and toward the right side. Crop cuts off statistical totals. |
| `route_parker_washington_wk6.png` | Page explicitly labels Parker Washington, Jacksonville, Week 6, season 2026. Shows shallow lateral/crossing shapes near the line, intermediate breaks from both sides, and deeper stems/breaks on both sides. Several green paths run toward the left sideline and upfield. Cookie overlay dims the chart. |
| `route_strange_wk4_vsCIN.png` | Chart explicitly labels Brenton Strange / 2026 vs Bengals. Shows short flat/underneath shapes around and behind the line, intermediate diagonal/crossing and out-breaking shapes, and green extensions through the middle and toward the right sideline. Gray incomplete paths also appear. Crop cuts off statistical totals. |
| `receiving_table_page.webp` | Address bar shows `https://nextgenstats.nfl.com/stats/receiving/2026/REG/all/yards`. Table headers include CUSH, SEP, TAY, TAY%, REC, TAR and YDS. The visible player rows do not include Meyers, Washington or Strange. Thus their requested numbers are UNAVAILABLE from this image. Regular Season selection does not establish a Week 1–8 cutoff. |

## Explicit missing-data list

- NGS separation, cushion, team air-yard share and aDOT for each of Meyers, Washington and Strange, weekly and Week 1–8 aggregate: UNAVAILABLE; no values in fetched HTML or visible target-player screenshot rows.
- Lawrence NGS time to throw and aggressiveness, weekly and Week 1–8 aggregate: UNAVAILABLE; application shells only.
- BAL defensive blitz%, pressure%, hurries and QB knockdowns for Weeks 1–8: UNAVAILABLE; PFR blocked.
- PFR advanced receiving for all three players and Lawrence advanced passing (including pressure% and bad throw%): UNAVAILABLE; PFR blocked, comments empty of tables.
- Independent cross-source numerical confirmation of ESPN receiving logs: UNAVAILABLE; NGS/PFR did not supply accessible values.
- Week 7 receiving statistics: N/A because ESPN schedule explicitly shows BYE WEEK; no zeros invented.
- Local screenshot original capture times and full route-chart page URLs: UNAVAILABLE; not recorded in the images.

## Complete fetch manifest

| Attempt | URL | Fetch time ET | HTTP | Raw HTML |
|---|---|---|---|---|
| ngs_receiving_season | https://nextgenstats.nfl.com/stats/receiving/2026/REG/all/yards | 2026-11-04T17:09:59-05:00 | 404 | [raw/ngs_receiving_season.html](raw/ngs_receiving_season.html) |
| ngs_passing_season | https://nextgenstats.nfl.com/stats/passing/2026/REG/all/ypa | 2026-11-04T17:09:59-05:00 | 404 | [raw/ngs_passing_season.html](raw/ngs_passing_season.html) |
| espn_jax_roster | https://www.espn.com/nfl/team/roster/_/name/jax/jacksonville-jaguars | 2026-11-04T17:09:59-05:00 | 200 | [raw/espn_jax_roster.html](raw/espn_jax_roster.html) |
| pfr_opp | https://www.pro-football-reference.com/years/2026/opp.htm | 2026-11-04T17:10:02-05:00 | 403 | [raw/pfr_opp.html](raw/pfr_opp.html) |
| pfr_jax | https://www.pro-football-reference.com/teams/jax/2026.htm | 2026-11-04T17:10:05-05:00 | 403 | [raw/pfr_jax.html](raw/pfr_jax.html) |
| pfr_meyers | https://www.pro-football-reference.com/players/M/MeyeJa01/gamelog/2026/advanced/ | 2026-11-04T17:10:08-05:00 | 403 | [raw/pfr_meyers.html](raw/pfr_meyers.html) |
| espn_meyers | https://www.espn.com/nfl/player/gamelog/_/id/3916433/type/nfl/year/2026 | 2026-11-04T17:10:09-05:00 | 200 | [raw/espn_meyers.html](raw/espn_meyers.html) |
| espn_washington | https://www.espn.com/nfl/player/gamelog/_/id/4432620/type/nfl/year/2026 | 2026-11-04T17:10:09-05:00 | 200 | [raw/espn_washington.html](raw/espn_washington.html) |
| espn_strange | https://www.espn.com/nfl/player/gamelog/_/id/4430539/type/nfl/year/2026 | 2026-11-04T17:10:09-05:00 | 200 | [raw/espn_strange.html](raw/espn_strange.html) |
| ngs_receiving_week8 | https://nextgenstats.nfl.com/stats/receiving/2026/REG/8 | 2026-11-04T17:10:10-05:00 | 200 | [raw/ngs_receiving_week8.html](raw/ngs_receiving_week8.html) |
| ngs_passing_week8 | https://nextgenstats.nfl.com/stats/passing/2026/REG/8 | 2026-11-04T17:10:10-05:00 | 200 | [raw/ngs_passing_week8.html](raw/ngs_passing_week8.html) |
| pfr_washington | https://www.pro-football-reference.com/players/W/WashPa00/gamelog/2026/advanced/ | 2026-11-04T17:10:12-05:00 | 403 | [raw/pfr_washington.html](raw/pfr_washington.html) |
| pfr_strange | https://www.pro-football-reference.com/players/S/StraBr00/gamelog/2026/advanced/ | 2026-11-04T17:10:15-05:00 | 403 | [raw/pfr_strange.html](raw/pfr_strange.html) |
| pfr_lawrence | https://www.pro-football-reference.com/players/L/LawrTr00/gamelog/2026/advanced/ | 2026-11-04T17:10:18-05:00 | 403 | [raw/pfr_lawrence.html](raw/pfr_lawrence.html) |
| espn_jax_schedule | https://www.espn.com/nfl/team/schedule/_/name/jax/season/2026 | 2026-11-04T17:10:33-05:00 | 200 | [raw/espn_jax_schedule.html](raw/espn_jax_schedule.html) |
| ngs_receiving_all | https://nextgenstats.nfl.com/stats/receiving/2026/REG/all | 2026-11-04T17:10:34-05:00 | 200 | [raw/ngs_receiving_all.html](raw/ngs_receiving_all.html) |
| ngs_receiving_week1 | https://nextgenstats.nfl.com/stats/receiving/2026/REG/1 | 2026-11-04T17:10:34-05:00 | 200 | [raw/ngs_receiving_week1.html](raw/ngs_receiving_week1.html) |
| ngs_receiving_week2 | https://nextgenstats.nfl.com/stats/receiving/2026/REG/2 | 2026-11-04T17:10:34-05:00 | 200 | [raw/ngs_receiving_week2.html](raw/ngs_receiving_week2.html) |
| ngs_receiving_week3 | https://nextgenstats.nfl.com/stats/receiving/2026/REG/3 | 2026-11-04T17:10:35-05:00 | 200 | [raw/ngs_receiving_week3.html](raw/ngs_receiving_week3.html) |
| ngs_receiving_week4 | https://nextgenstats.nfl.com/stats/receiving/2026/REG/4 | 2026-11-04T17:10:35-05:00 | 200 | [raw/ngs_receiving_week4.html](raw/ngs_receiving_week4.html) |
| ngs_receiving_week5 | https://nextgenstats.nfl.com/stats/receiving/2026/REG/5 | 2026-11-04T17:10:35-05:00 | 200 | [raw/ngs_receiving_week5.html](raw/ngs_receiving_week5.html) |
| ngs_receiving_week6 | https://nextgenstats.nfl.com/stats/receiving/2026/REG/6 | 2026-11-04T17:10:36-05:00 | 200 | [raw/ngs_receiving_week6.html](raw/ngs_receiving_week6.html) |
| ngs_receiving_week7 | https://nextgenstats.nfl.com/stats/receiving/2026/REG/7 | 2026-11-04T17:10:36-05:00 | 200 | [raw/ngs_receiving_week7.html](raw/ngs_receiving_week7.html) |
| ngs_passing_all | https://nextgenstats.nfl.com/stats/passing/2026/REG/all | 2026-11-04T17:10:36-05:00 | 200 | [raw/ngs_passing_all.html](raw/ngs_passing_all.html) |
| ngs_passing_week1 | https://nextgenstats.nfl.com/stats/passing/2026/REG/1 | 2026-11-04T17:10:37-05:00 | 200 | [raw/ngs_passing_week1.html](raw/ngs_passing_week1.html) |
| ngs_passing_week2 | https://nextgenstats.nfl.com/stats/passing/2026/REG/2 | 2026-11-04T17:10:37-05:00 | 200 | [raw/ngs_passing_week2.html](raw/ngs_passing_week2.html) |
| ngs_passing_week3 | https://nextgenstats.nfl.com/stats/passing/2026/REG/3 | 2026-11-04T17:10:38-05:00 | 200 | [raw/ngs_passing_week3.html](raw/ngs_passing_week3.html) |
| ngs_passing_week4 | https://nextgenstats.nfl.com/stats/passing/2026/REG/4 | 2026-11-04T17:10:38-05:00 | 200 | [raw/ngs_passing_week4.html](raw/ngs_passing_week4.html) |
| ngs_passing_week5 | https://nextgenstats.nfl.com/stats/passing/2026/REG/5 | 2026-11-04T17:10:38-05:00 | 200 | [raw/ngs_passing_week5.html](raw/ngs_passing_week5.html) |
| ngs_passing_week6 | https://nextgenstats.nfl.com/stats/passing/2026/REG/6 | 2026-11-04T17:10:39-05:00 | 200 | [raw/ngs_passing_week6.html](raw/ngs_passing_week6.html) |
| ngs_passing_week7 | https://nextgenstats.nfl.com/stats/passing/2026/REG/7 | 2026-11-04T17:10:39-05:00 | 200 | [raw/ngs_passing_week7.html](raw/ngs_passing_week7.html) |
