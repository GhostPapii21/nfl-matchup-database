# sportsbook-odds-bridge data audit (Phase 1, read-only exploration)
Date: 2026-11-03 (ET). Author: Ghost6 executor. Nothing was edited, pushed, merged or deployed.
Sources: GitHub `GhostPapii21/sportsbook-odds-bridge` (main, via the connector), Render (read-only), local box files.
Line numbers for `server.py` come from GitHub main as of today. `odds_edge_scanner.py` was read from the local copy `/workspace/bridge/odds_edge_scanner.py`, which has the same byte size as main (13,801 bytes) but was not hash-checked.

## 0. Where it lives
- GitHub: private repo `GhostPapii21/sportsbook-odds-bridge`, Python, default branch `main`, last push 2026-10-29 04:40 ET.
- No full local clone exists. Partial, older copies: `/workspace/bridge/` (server.py 18.6 KB vs 35.3 KB on main, so stale), `/workspace/bridge-tools/` (betting_tools.py, data_sources.py and injury_lag.py match main's sizes), and `/workspace/sb-grades/reference/sportsbook-odds-bridge/` (a reference subfolder inside the suave-bets repo, not this repo).
- Render (workspace "My Workspace"):
  - `sportsbook-odds-bridge`, srv-darrmogjo6nc7395uba0, main, autoDeploy yes. The live deploy is commit ac5e8f8 (merge of PR #22), finished 2026-10-24 09:49 ET.
  - `sportsbook-odds-bridge-staging`, branch feat/sports-leader-adapter, autoDeploy no.
  - `sports-leader-mcp`, a separate Node service.
- Superpowers: there is no `/home/box/agent-data/plugins/superpowers` directory. The Superpowers skills (brainstorming, writing-plans, TDD, requesting-code-review, verification-before-completion and the rest) are loaded as agent skills. Existing spec/plan folders: `/workspace/nfl-database/docs/superpowers/{specs,plans}`.

## 1. What the bridge is
- **It's a remote MCP server for Grok**, not a scheduled data pipeline. server.py docstring: "Remote MCP wrapper around odds_edge_scanner.py, with OAuth for Grok" (server.py L1). It uses Starlette + uvicorn with an OAuth gateway (L778–797, `build_app`) and two POST import routes: `/data-packages/import` and `/ngs-weekly/import` (L788–789).
- **MCP tools** (server.py), grouped:
  - Odds Api tools: `list_active_sports`, `list_events` (L112–133), `scan_player_prop` (L134), `grade_player_prop_projection` (L181), `scan_odds` (L449), `get_prop_board` (L555).
  - Math tools: `devig_odds` (L700), `market_hold` (L709), `half_point_value` (L716), `kelly_stake` (L726), `hedge_calc` (L734).
  - Models and history: `project_player_prop_model` (L252), `list_historical_packages`, `get_player_game_history`, `lookup_player_history` (L362–446).
  - NFL context: `nfelo_*` (L629–653), `nfl_injuries`, `nfl_official_injuries`, `combined_injuries`, `nfl_game_recap`, `ngs_*` (L654–760).
  - Other: Sports Leader slate/injuries (L511–530), `nba_pregame_research` (L532), source-intelligence tools.
  - **Bug:** `list_sports_data_sources`, `research_sports_platform` and `plan_sports_metric_source` are defined twice (L80–98 and L761–776). The import at L36–39 is also duplicated.
- **Odds Api adapter** (`odds_edge_scanner.py`):
  - The Odds API v4 (L4, L20), 30 s timeout (L65), decimal odds and ISO dates (L81, L95–96).
  - `find_edges` (L149–200) builds a leave-one-book-out mean no-vig consensus (L163–166). It flags quotes older than 10–30 min or "unchanged while others moved" as stale (L176–181).
  - It has a standalone CLI with webhook alerts (L203–280).
- **Defaults:**
  - `scan_odds`: sports WNBA, NFL, NCAAF, FCS and MLB; regions `us,us2`; markets `h2h,spreads,totals` (L450–453).
  - `get_prop_board`: `player_pass_yds,player_rush_yds,player_reception_yds,player_receptions`, books `draftkings,fanduel`, region `us`, at most 10 markets (L558–576).
  - `scan_player_prop`: regions `us,us2` (L144).
- **Schedule/cron:** the server has no internal scheduler. Scheduled work runs in GitHub Actions: `build-historical-packages.yml`, `nfl-weekly-matchup-research.yml`, `ngs-weekly-public.yml`, `test-nba-pregame.yml` and `test-sports-pipelines.yml` (contents not read in this pass). None of them is an odds snapshot job.
- **Output:** JSON returned to the MCP caller (Grok chats), with no odds persisted. Packages and NGS go to a `PackageStore` through the import routes. `check_server` only reports whether the key is set (L505–507).
- **Who consumes it:** the research code on the box mostly does NOT use the bridge. No file in `nfl-database/tools`, `nba-matchup` or `pro-edge` references the bridge. Each one calls the Odds API directly:
  - NFL: per-run copies of `pull_odds.py`. There are 13 copies under `nfl-database/runs/*` with 3 distinct versions by md5 (11 identical). The canonical one is `runs/2026-11-05_shared_src/pull_odds.py`.
  - pro-edge: `pro-edge/edge_scan.py` and `pro-edge/game_mkts.py`.
  - NBA: `nba-matchup/line_tracker/snapshot.py` + `core.py`.
  - `run_gate.py` takes `no_vig` per leg as input (run_gate.py L456–464) and does not fetch it.

## 2. Data map: what is pulled vs. what the rules need
| Need (research rules) | Bridge | Actual research pullers |
|---|---|---|
| No-vig from sharp books | Mean of all other books, no sharp weighting (scanner L163–166); books limited to us/us2 or DK+FD | NFL pull_odds: FD, DK, **pinnacle**, prizepicks, underdog (L26). pro-edge: SHARP priority pinnacle > circa > betonline > lowvig > FD > DK (edge_scan L13), regions us,us2,eu |
| Alt lines (NFL props) | Only if the caller passes `_alternate` keys (L567) | NFL pull_odds MK: pass/rush/rec/receptions/rush+rec + alternates for all except completions (L25) |
| Game spreads/totals | `scan_odds` h2h/spreads/totals | **NFL pull_odds pulls no game markets.** pro-edge/game_mkts pulls them (L5) |
| 1H/2H/quarter spreads (N3) | Not in defaults | Only `pro-edge/game_mkts.py` L5: h1, h2 and q1–q4 h2h/spreads/totals, alternates, team totals |
| NBA PRA, P, R, A, PA, PR + alts | Not in defaults (NBA only adds a "research not verified" notice, L607–628) | line_tracker MAIN/ALT (core.py L5–7), FD+DK only (snapshot.py L29), region us. **No pinnacle, so no sharp no-vig for NBA** |
| Opening to close movement | None; nothing persisted (`previous` is only held in memory by the CLI) | NBA line_tracker checkpoints open/T-120/60/30/every 3h (core.py L9–31), alts only at open and T-30. NFL: single pull per run, no open/close series. `nfl-database/tools` has no closing snapshot (pro-edge? not verified) |
| Timestamps | `updated_at` = market/book last_update (L596); commence_time | NFL keeps `last_update_utc` + in-play flag (pull_odds L10–14); NBA ts_et/ts_utc/minutes_to_tip |
| Errors / quota | scan_odds collects per-sport errors and the x-requests headers (L478–487); get_prop_board has no try/except | pull_odds catches per event (L35) and logs remaining quota; key is read from env (L24) |

**Gaps:**
1. The bridge and the research use different market sets and books, and nothing reconciles them. There's no single source of truth.
2. No NFL period markets (1H/2H/Q) in the NFL pull, even though rule N3 judges them.
3. NBA has no sharp book, so "no-vig" for NBA legs comes from FD+DK, which are the books being bet.
4. NFL has no open-to-close line history.
5. The bridge's consensus is unweighted and ignores pinnacle unless the region includes it (pinnacle is in `eu`, not `us,us2`).
6. Logic is copy-pasted into 13 run-folder copies of pull_odds.py, so drift is already present (3 versions).

**Pulled but never used:** prizepicks/underdog pick'em lines in NFL pull_odds (no consumer found in run_gate; not exhaustively verified). The bridge's `scan_odds` edge output is not read by any box tool.

**Staleness:** the bridge defines it (10–30 min quote age). NFL pull_odds drops in-play rows but has no age cutoff. run_gate has a staleness-waiver log (L522) for inputs.

## 3. PRs, issues, commits
- Open: PR #24 "Add cached NBA cloud research and experimental opportunity model" (Codex, 2026-10-28; its own PR text says v6 fails the promotion gate). PR #23 "Add conservative QB and backup-QB prop gates" (2026-10-26). Issue #21 "Integrate Sports Leader MCP as read-only data adapter". Issue #15 "NBA: automatically ingest historical shot-zone and matchup data". **There is no open #6** (closed or never existed; not checked).
- Recent main commits: ac5e8f8 merge #22 Sports Leader adapter (2026-10-24 09:30 ET), c3c2e88 Fantasy WR-CB importer (#20), d6b3f04 NFL research board branch (#19), 940573c defender wording (#18), NGS commits (#17). Nothing on main since 10-24, so production has run that same commit since then.

## 4. Options for the "Superpowers review"
Superpowers is a skill workflow for coding agents. "Adding it to the bridge" can mean:
- (a) Repo-level instructions so any agent follows the workflow. The repo already has `.codex/skills/`; there's no AGENTS.md or CLAUDE.md at the root.
- (b) A runtime data-audit job.

**Option A: workflow only.** Add AGENTS.md plus `.codex/skills/data-audit/` requiring brainstorm → spec → plan → TDD → code review for any change. This is cheap, but it doesn't check the data itself.

**Option B: data-audit job (recommended, combined with A).** Add a `data_contract.yaml` in the repo listing what the research needs: per sport, the markets (incl. alternates, h1/h2/q1–q4), the sharp anchor books, the required fields (last_update, commence_time) and max staleness. Then add:
1. `audit_data.py` + MCP tool `audit_research_data`. It compares the contract against (i) what the bridge and each box puller request, from static scans of their market and book strings, and (ii) one cheap live sample per sport. It reports missing markets, missing sharp anchors, stale quotes, unused pulls and puller drift.
2. A GitHub Actions cron that runs it in dry-run and fails on any contract gap.

This turns "are we pulling the right things" into a pass/fail check.

**Option C: make the bridge the single odds gateway.** Move NFL, NBA and pro-edge pulls into one bridge module driven by the contract, with snapshot persistence for open-to-close history, and have every puller call it. Highest value, but it touches live research code, so do it after the Nov 3 "locked door" build.

**Recommendation:** A+B now, then C as a later phase. Open decisions for Rico:
- Quota budget for live samples.
- Whether NBA gets pinnacle/eu.
- Whether NFL pulls period markets by default.

All of it needs Rico's OK before any PR or merge.
