# 2026 NFL team coverage tendencies — source log

Pull window: Sunday, 2026-11-22, about 5:03–5:07 PM AST (America/Santo_Domingo).
Goal: public, free man vs zone, MOFO (two-high / middle-of-field open) vs MOFC (single-high / middle-of-field closed), blitz, and Cover 0/1/2/3/4/6/9 rates for all 32 teams.
Rule: no invented numbers; every figure in `team_coverage_rates.csv` has a source URL, the date/week range it covers, and a pull time. Missing values are left blank (unknown), not zero.
No GitHub commit was made.

Output: `/workspace/nfl-database/defense/coverage_tendencies_2026-11-22/team_coverage_rates.csv` (64 rows: 32 Sharp + 32 StatRankings).

Most recent complete 32-team table: StatRankings CoverageIQ, through games played 2026-11-20 (includes Week 11 Thursday 2026-11-19; excludes Week 11 Sunday 2026-11-22 games). Last updated 2026-11-21T23:32:09Z (2026-11-21 7:32 PM AST).
Next-best complete 32-team table, different charting: Sharp Football Analysis, updated 2026-11-17 (through Week 10; Week 11 games from 2026-11-19 not included).

The two sources do **not** use the same definitions. Do not mix them on the same slip or in the same model input. Example: Cleveland man coverage is 44.4% on Sharp (Nov 17) and 54.8% on StatRankings (through Nov 20).

---

## Local files checked first

| Path | Result |
| --- | --- |
| `/workspace/nfl-database/runs/2026-11-22_matchup_run/src/nfl-coverage-schemes.csv` | Matches the live Sharp Nov 17, 2026 32-team man/zone/MOFC/MOFO table. Used as a cross-check; live HTML was re-pulled today. |
| `/workspace/nfl-database/runs/2026-11-22_matchup_run/src/sharp_cov.html` and `pulled_log.txt` | Local Sharp HTML from today's earlier matchup run (log starts 2026-11-22T07:58). |
| `/workspace/nfl-sim/data/sharp_coverage_2026.csv` | Older 32-team Sharp snapshot, undated in-file (e.g. CLE man 46.5). Superseded by the Nov 17 table. |
| `/workspace/nfl-sim/data/sharp_def_tendencies_2026.csv` | Older Sharp blitz snapshot (e.g. MIN blitz 67.3 vs live 69.2). Superseded by the Nov 17 tendencies page. |
| `/workspace/nfl-database/runs/2026-11-15_SUNDAY_W10_SCHEDULED/src/sharp_coverage_nov10.txt` | Partial Sharp extract, earlier than Nov 17. |
| `/workspace/nfl-database/sources/sharp_2026-11-03/` | Sharp coverage + tendencies HTML/CSV as of Nov 3, 2026. Historical only. |
| `/workspace/nfl-database/runs/2026-11-05_JAX_BAL/src/fc_www_sharpfootballanalysis_com_stats-nfl_nfl-coverage-schemes_.json` | Firecrawl capture of Sharp as of Nov 3. |
| `/workspace/nfl-database/runs/2026-11-05_JAX_BAL/src/fc_statrankings_com_nfl_coverage_team_{jax,bal}.json` | Earlier StatRankings team-page captures. Headline man/zone/single-high/two-high/blitz were public then; shell-split tables were behind StatRankings+. |
| `/workspace/nfl-database/defense/pfr_defense_advanced_*.csv` | PFR advanced defense (pressure, coverage grades-style counting stats). No man/zone or MOFO/MOFC rates. |
| `/workspace/nfl-sim/data/ftn_charting_2026.parquet` and various `ftn_charting_2025.parquet` copies under `/workspace/nfl-sim`, `/workspace/nfl-database`, `/workspace/vet_scratch` | Local FTN charting files exist (the “prior FTN board” on disk). They were **not** used to invent a public 2026 table. FTN’s charting feed is a licensed/product dataset, not a free public 32-team webpage. |

---

## Sources that worked (usable public data)

### 1. Sharp Football Analysis — Coverage Scheme Stats (primary Sharp row)

- URL: https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/
- Access: public HTML table, no login required for the 32-team rates.
- Updated: November 17, 2026 (page timestamp 2026-11-17T12:59:00-05:00).
- Coverage: all 32 teams; man rate, zone rate, middle closed (MOFC), middle open (MOFO). No Cover 1/2/3/4/6 and no blitz on this page.
- Weeks: 2026 season-to-date through 2026-11-17 (through Week 10; Week 11 games starting 2026-11-19 are not in this table).
- Pulled: 2026-11-22 5:04 PM AST.
- Status: **worked**. This is the cleanest single public table for man/zone/MOFO/MOFC with all 32 teams named in HTML.

### 2. Sharp Football Analysis — Defensive Tendencies (blitz for Sharp rows)

- URL: https://www.sharpfootballanalysis.com/stats-nfl/nfl-defensive-tendencies/
- Access: public HTML table, no login required.
- Updated: November 17, 2026 (page timestamp 2026-11-17T12:58:58-05:00).
- Coverage: all 32 teams; blitz rate (also light/heavy box and sub-package rates, not copied into the main CSV).
- Pulled: 2026-11-22 5:03–5:04 PM AST.
- Status: **worked**. Blitz is attached to the Sharp rows and noted as coming from this sibling page, same update day.

### 3. StatRankings CoverageIQ — team pages (primary StatRankings rows)

- URL pattern: https://statrankings.com/nfl/coverage/team/{ari,atl,bal,buf,car,chi,cin,cle,dal,den,det,gb,hou,ind,jax,kc,lac,lar,lv,mia,min,ne,no,nyg,nyj,phi,pit,sea,sf,tb,ten,was}
- Access: public headline chips (man, zone, single-high, two-high, blitz) and coverage-snap counts. All 32 pages returned HTTP 200 today. Detailed “coverage splits” / alignment tables on the same pages are locked behind StatRankings+ (“Unlock coverage splits”). Those locked tables were **not** used.
- As-of: ranking pages for the same metrics say “through games played November 20, 2026” and “last updated 2026-11-21T23:32:09Z”. Team-page chip values match those ranking-page season rates exactly for every team named in the public articles (25/25 cross-check, zero mismatches on man, zone, blitz, single-high, and two-high).
- Coverage: all 32 teams filled for man, zone, MOFC (single-high), MOFO (two-high), and blitz.
- Notes: each team page is titled “pass defense vs WR” and shows a coverage-snap count. The chip percentages nonetheless match the league ranking pages, which define the rates as a percentage of classified coverage snaps. Single-high + two-high sum to 100 on every team. Man + zone usually land just under 100 (residual unclassified).
- Pulled: 2026-11-22 5:03 PM AST.
- Status: **worked**. This is the most recent complete 32-team public set.

### 4. StatRankings public ranking articles — Cover 0/1/2/2M/3/4/6/9 (top 25 only)

- URLs:
  - https://statrankings.com/nfl/advanced/teams/coverage/cover-0-rate
  - https://statrankings.com/nfl/advanced/teams/coverage/cover-1-rate
  - https://statrankings.com/nfl/advanced/teams/coverage/cover-2-rate
  - https://statrankings.com/nfl/advanced/teams/coverage/cover-2m-rate
  - https://statrankings.com/nfl/advanced/teams/coverage/cover-3-rate
  - https://statrankings.com/nfl/advanced/teams/coverage/cover-4-rate
  - https://statrankings.com/nfl/advanced/teams/coverage/cover-6-rate
  - https://statrankings.com/nfl/advanced/teams/coverage/cover-9-rate
  - Also used as date/definition checks: man-coverage-rate, zone-coverage-rate, single-high-rate, two-high-rate, and https://statrankings.com/nfl/advanced/teams/defense/blitz-rate
- Access: public article text lists the top 25 teams and season rates. The HTML data table often uses logo images without alt text for most rows, so the article prose was the reliable public extract. The pages include login/subscribe prompts and custom-split controls; those paid/custom views were not used. The articles themselves state that only the top 25 of 32 are listed.
- As-of: through games played 2026-11-20; last updated 2026-11-21T23:32:09Z (blitz page 2026-11-21T23:32:10Z).
- Coverage: 25 of 32 teams for each of Cover 0, 1, 2, 2 man (Cover 2M), 3, 4, 6, and 9. The other 7 teams are blank (unknown), not zero. A tied 25th team can be omitted from the prose.
- Definitions (from the public pages): Cover 0 = man with no deep safety; Cover 1 = man under one deep safety; two-high family = Cover 2, Cover 4, and Cover 6.
- Pulled: 2026-11-22 5:03–5:04 PM AST.
- Status: **worked, partial** (top 25 per shell).

---

## Sources tried that did not yield a usable 32-team public table

### ESPN

- URL tried: https://www.espn.com/nfl/stats/team/_/view/defense (HTTP 200, 2026-11-22 5:04 PM AST).
- Result: standard 2026 team defense totals (yards, pass, rush, points). No man/zone, MOFO/MOFC, blitz scheme rate, or coverage-shell columns. Rico mentioned ESPN as a place this data might live; it is not on this public team-defense stats page.

### hipa.com / HPA (Rico’s “hipa.com”)

- https://hipa.com and https://www.hipa.com: TLS connection failed (unexpected EOF). Not a usable site from this box.
- https://hpa.com: HTTP 200, domain-for-sale parking page (Aftermarket.com).
- Likely typo targets that *do* exist and were checked: Sharp Football Analysis, StatRankings (CoverageIQ), SumerSports, FTN Fantasy, Fantasy Points, PFF, Next Gen Stats, nfelo, rbsdm.com. None of the typo domains themselves provided data.

### SumerSports

- https://sumersports.com/teams/defensive/coverage/ — HTTP 404.
- https://sumersports.com/teams/defensive/formation-tendency/ — HTTP 200, last updated 2026-11-20 6:03 AM EST. Public 2026 formation-tendency table (2x2 etc.). The Man % / Zone % columns were not populated in the public page. No MOFO/MOFC table found on the attempted coverage URL.
- Status: **not usable for man/zone or MOFO/MOFC**. Login/unlock prompts are present on the site; no paywall was bypassed.

### FTN Fantasy

- https://ftnfantasy.com/nfl — HTTP 200 marketing/article hub. Public articles mention isolated team rates (for example a Packers piece citing zone/two-high rates through six weeks), but there is no free 32-team 2026 coverage board on the pages pulled. FTN’s data product is paid.
- Status: **no public 32-team table**. Isolated article figures were not copied into the CSV (partial, not season-to-date for all 32, and not a board).

### PFF

- https://www.pff.com/news/fantasy-football-wr-man-zone-coverage — “Fantasy Football Man, Zone Coverage Report: NFL Week 11,” posted 2026-11-18 5:45 AM EST.
- Status: **paywalled**. Title and byline are public; the body is not (subscribe / sign-up wall). No rates were taken from this page.

### Fantasy Points

- https://www.fantasypoints.com/ — HTTP 200 homepage. Data Suite is a paid product. No public 32-team man/zone or MOFO table was retrieved from the homepage.
- Related public articles (Mintner Substack Week 8 and Week 11, FantasyLife Week 11, Statyx Week 11) quote **partial** team MOFC/MOFO/blitz/zone rates, often attributed to Fantasy Points or similar. Those are not a complete 32-team board and were not entered as official rates.

### Next Gen Stats

- https://nextgenstats.nfl.com/ — HTTP 200 homepage, no public 2026 team coverage-rate table in the HTML.
- https://nextgenstats.nfl.com/stats/team — HTTP 404.
- AWS/NFL explainer pages describe NGS coverage classification (Cover 0/1/2/3/4/6, man Cover 2, prevent) but do not publish 2026 team rates.
- Status: **no public team-rate table found**.

### nfelo

- https://www.nfeloapp.com/nfl-power-ratings/nfl-team-tendencies/ — HTTP 200 public page.
- Result: pass rate over expected, personnel, and formation tendencies. No man/zone, MOFO/MOFC, or coverage-shell rates.

### rbsdm.com

- https://www.rbsdm.com/ — HTTP 200, but the response is an empty JS app shell (about 811 bytes, `<div id="root"></div>`). No coverage table is present in the static HTML. The client app was not executed to fish for hidden data.
- Status: **no usable table from the public static page**. Search results for the site show EPA-style team stats, not man/zone rates.

### Reddit

- Tried, all HTTP 403 from this box (JSON and old.reddit `.json`):
  - https://www.reddit.com/r/fantasyfootball/search.json?q=man%20zone%20coverage%20rate%202026&restrict_sr=1&sort=new&t=year
  - https://www.reddit.com/r/nfl/search.json?q=man%20coverage%20zone%20MOFO%20MOFC%202026&restrict_sr=1&sort=new&t=year
  - https://www.reddit.com/r/sportsbook/search.json?q=man%20zone%20coverage%20FTN%20MOFO&restrict_sr=1&sort=new&t=year
  - https://www.reddit.com/r/nfl_draft/search.json?q=man%20zone%20coverage%20rate%20MOFO&restrict_sr=1&sort=new&t=year
  - https://old.reddit.com/r/fantasyfootball/comments/1x8f6pw/20_underlying_matchups_that_could_impact_fantasy/.json
- The 403s were **not** bypassed.
- Independent web search (not a raw JSON listing) did surface public posts with **isolated** 2026 rates, not a 32-team table:
  - https://www.reddit.com/r/fantasyfootball/comments/1x8f6pw/20_underlying_matchups_that_could_impact_fantasy/ (2026-10-17): CLE man ~47%; TB zone ~83%; BUF Cover 3 28.1% (then-current, not today’s board).
  - https://www.reddit.com/r/fantasyfootball/comments/1wlljwc/nfl_week_2_data_dump/ (2026-09-20): Fantasy Points excerpts (e.g. JAX zone 81.4% over a 10-game window, WAS 2-high 59.5% over 10 games, PIT/IND/NE one-off rates).
  - Team-sub anecdotes (e.g. r/KansasCityChiefs FTN Week 1 man rates, r/detroitlions man-rate comments) — not a league board.
- Status: **blocked for direct listing; no full 32-team 2026 table found via search snippets.** Those isolated Reddit figures were not written into the CSV.

### 2025 full-season rates

- Sharp’s current pages are labeled 2026 and were not a 2025 archive.
- StatRankings ranking tables visually include a 2025 column, but the static HTML does not expose team names for the full 32-row table (logos without alts for most rows), so 2025 rates were **not** captured and are not in the CSV.
- No complete public 2025 32-team man/zone/MOFO board was extracted in this pass. Local FTN 2025 parquets were not converted into a public table.

---

## Login / paid access (do not bypass)

| Source | What’s free | What needs login or payment |
| --- | --- | --- |
| StatRankings CoverageIQ team pages | Headline man, zone, single-high, two-high, blitz, snap count | “Unlock coverage splits” and alignment-allowed tables (StatRankings+) |
| StatRankings ranking pages | Top-25 article text and some table UI | Custom week splits / full interactive table may require an account; only public article rates were used |
| PFF Week 11 man/zone report | Title, author, timestamp | Article body |
| FTN Fantasy / Fantasy Points Data Suite | Marketing pages and occasional article mentions | Full coverage boards and charting |
| SumerSports | Some formation-tendency columns | Broader coverage tools; login/unlock prompts present |
| Sharp Football Analysis | The two public 32-team tables used here | Site has login/subscribe links; the coverage and tendencies tables used today were visible without signing in |

---

## How to use the CSV

- 64 rows, two per team, `season=2026`.
- Prefer **StatRankings** rows for the most recent as-of date (through 2026-11-20) when you want man, zone, MOFC, MOFO, blitz, and (where filled) Cover 0/1/2/2M/3/4/6/9.
- Prefer **Sharp** rows when you want a single publisher’s man/zone/MOFO/MOFC + blitz, all updated 2026-11-17, with every team’s four coverage rates in one HTML table.
- Never average or splice Sharp and StatRankings percentages for the same team.
- Blank cover-shell cells mean the team was not named in that public top-25 article, not that the rate is 0.
