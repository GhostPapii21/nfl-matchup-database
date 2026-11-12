# Blitz (NFL Researcher) — Knowledge Base
Built Thu Oct 29, 2026 ~4:50 AM ET from local files only (read in place; nothing outside /workspace/nfl-database/ was created or changed; no web fetches). Every fact cites a file path. "Reported by BetGuru" = in BetGuru's handoff list but not traced to a user statement in files or shared memory.

**Week numbering (resolved):** Sun Oct 11 = Week 5 (/workspace/nfl-sim/HANDOFF_FOR_SMOKE.md; /workspace/nfl-sim/loss_review_wk5_6.md), Oct 15–19 = Week 6 (/workspace/nfl-sim/postmortem_2026-10-18.md), Oct 22–26 = Week 7 (/workspace/nfl-contest/ACCURACY_AUDIT.md: "ESPN lists it as Week 7"). So Oct 29–Nov 2 is Week 8. Some files mislabel (`week6_*` filenames hold the Week 5 slate per HANDOFF_FOR_SMOKE.md; /workspace/nfl-contest/mighty-duck.md calls Oct 25 "Week 8", penalized in ACCURACY_AUDIT.md).

---
## 1. Source index
### 1a. Core rule/method files (read in full or by section)
| Path | Date | Holds | Status |
|---|---|---|---|
| /home/box/agent-data/workflows/nfl-betting-script/SKILL.md | 2026-10-29 | Live betting script §1–20 + star-unders; §14–16 hard rules from graded misses; §15 QB grade card; §18 de-vig; §20 matchup DB / NGS / Panthers rule (added Oct 29) | **CURRENT (betting rules master)** |
| /workspace/nfl-database/SKILL_backup_2026-10-29.md | 2026-10-29 | Same as SKILL.md minus frontmatter and §20 (diff checked) | Superseded backup |
| /workspace/nfl-database/MASTER_PROMPT.md | 2026-10-29 | Rico's Phases 1–8 data-collection prompt (ingest, def/off profiles, alerts, outputs, live checks, NGS 7A–7G, film 8A–8F) | **CURRENT (data-collection master)**; not started |
| /workspace/nfl-database/PHASE_SCRIPT.md | 2026-10-29 | User's "Custom Phase Script" Oct 29: 10-step projection pipeline, 8 role categories, def-profile thresholds, percentile labels, 3-model median, FD/DK line process | **CURRENT (projection model)**; supersedes Oct 27 version |
| /workspace/nfl-sim/GAME_SCRIPT.md | 2026-10-22 (built Oct 13) | BetGuru routine guide NFL+WNBA: cost discipline, pre-game build, 3 models, approved rules, slip/bankroll, post-game recap | Partly current (routine guide; precedence: user rules > SKILL > 13 gates > this) |
| /workspace/nfl-sim/betting_script_betguru.md | 2026-10-22 (built Oct 11) | BetGuru 13(+14) gates scoring G/A/R, value gates, tiers, Gate 14 role math, user rules Oct 12–13, $150 bankroll | Superseded by SKILL.md; gate detail still referenced |
| /workspace/nfl-sim/NFL_BETTING_SCRIPT.md | 2026-10-22 (Oct 11) | 28-step Smoke+BetGuru script | Superseded (folded into SKILL.md) |
| /workspace/nfl-sim/SMOKE_BETTING_SCRIPT.md | 2026-10-22 (Oct 11) | Smoke's 12 checks + slips v2–v4 of Oct 11 | Superseded |
| /workspace/nfl-sim/notes/rules_from_videos_2026-10-13.md | 2026-10-24 | 31 rules (22 APPROVED, 9 PROPOSED) from Peabody/Rose-Berman, Bills film, Smoke | Draft by BetGuru; approval statuses partly unverified (file's own note) |
| /workspace/nfl-sim/HANDOFF_FOR_SMOKE.md | 2026-10-22 | Oct 11 (Week 5) data map for Smoke; name-join tips | Historical |
| /workspace/nfl-sim/specs/matchup_database_spec.md | 2026-10-22 | User's Oct 21 matchup-DB spec (offense/coaching/defense fields; tune 2024 test 2025) | Current spec |
| /workspace/codex_nfl9.md | 2026-10-24 | Codex task: sb-grades must carry 9 sourced NFL inputs (and 9 NBA) per row, reject rows without them | Superseded by v4 grader (14 inputs, below) |
| /workspace/sb-fix/data/grades/build_nfl_v4.py, nfl_rows_v4.json, betguru_nfl_grades.json | 2026-10-24 | v4 grader: 14 weighted inputs (line 3 of build_nfl_v4.py), missing inputs labeled "missing source" | Current grader (do not edit; live) |
### 1b. Results, postmortems, logs
| Path | Date | Holds | Status |
|---|---|---|---|
| /workspace/nfl-sim/postmortem_oct11_early.md | Oct 11 | Every Oct 11 early leg graded, calibration buckets, QB card table, 5 mistake patterns, rules written to SKILL | Evidence (source of SKILL §14–16) |
| /workspace/nfl-sim/postmortem_smoke_oct11.md | Oct 11 | Smoke's legs, unbet big lines, 10 proposed rules | Evidence (most adopted into SKILL §14) |
| /workspace/nfl-sim/loss_review_wk5_6.md | Oct 13 | Every missed leg Week 5 + MNF Oct 12, cause, knowable? | Evidence |
| /workspace/nfl-sim/postmortem_2026-10-15.md | Oct 16 | TNF SEA@DEN: 9 user tickets lost, miss classes, fixes | Evidence |
| /workspace/nfl-sim/postmortem_2026-10-18.md | Oct 19 | Week 6 Sunday: zero-bet model day; user tickets; cut audit | Evidence |
| /workspace/nfl-sim/postmortem_2026-10-19.md | Oct 20 | MNF WAS@SF: zero-bet, 7 cut winners | Evidence |
| /workspace/nfl-sim/postmortem_2026-10-22.md | Oct 23 | TNF NE@CHI + NBA: 7 user tickets, model card, proposals | Latest postmortem |
| (none) | — | **No postmortem for Sun Oct 25 (Week 7) or MNF Oct 26 found** | GAP |
| /workspace/nfl-sim/bets/bet_log.md | Oct 15 | TNF Oct 15 tickets + result | Historical |
| /workspace/nfl-sim/bets/leg_history.csv (251 rows), leg_hit_rates.md | Oct 16 | Leg-level hit rates by category | Stale after Oct 16 |
| /workspace/nfl-sim/bets/expected_vs_actual_ledger.md | Oct 22 | Expected vs actual per slate, bankroll snapshots | Current through Oct 22 |
| /workspace/nfl-sim/bets/pnl_ledger.csv | Oct 22 | Ticket-level cash P&L, cumulative | Through Oct 18 |
| /workspace/bet-log.csv (+ backups in /workspace and nfl-sim/bets/) | Oct 25 | Master leg log (bet_id, prop, line, actual, odds, result, CLV) | Current; Oct 25 partly logged (BetGuru) |
| /workspace/nfl-sim/notes/bankroll_reconcile_2026-10-22.md | Oct 22 | $90 stated vs ~$355.80 implied gap | OPEN |
| /workspace/nfl-sim/notes/tipster_summary.md, tipster_tracker.csv | Oct 24 | Verified tipster record (@MrBearBets/@GameGridAppp 3-14) | Current |
| /workspace/nfl-contest/ (ACCURACY_AUDIT.md, 10 bot submissions, FINISHES.txt, data dumps) | Oct 23–24 | Week 7 prop contest: 8 bots ranked on accuracy | Current audit; picks ungraded vs results |
| /workspace/nfl-sim/boards/*.md | Oct 19–25 | Game-day boards (MNF, TNF, Sun Oct 25) | Historical |
| /workspace/nfl-sim/notes/sunday_recheck_2026-10-25.md, sat_slip_check_2026-10-24.md | Oct 24 | Advisory recheck of user's 15-leg SGP + PrizePicks | Latest pre-game files |
### 1c. Engine, data, research
| Path | Date | Holds | Status |
|---|---|---|---|
| /workspace/nfl_engine/README.md, BACKTEST_REPORT.md, VERIFICATION.json, nfl_sim.py, matchups.py, research.py (+prepare, fit_context, validate) | Oct 22 (report Oct 11) | 500k-sim opportunity engine; backtest: did not beat our model | Research tool; not production |
| /workspace/nfl-sim/DATA_REGISTRY.md | Oct 22 | Registry of datasets (hist FD props, RB usage, routes/personnel est., free matchups) | Current registry (pre-repo) |
| /workspace/nfl-sim/blitz_db/STATUS.md, PASS3–10.md, team_profiles_2026-10-22.md, week7_*.md/csv | Oct 22–23 | DuckDB blitz/matchup DB (Weeks 1–6, 93 games), team profiles, Week 7 boards | Superseded as primary by repo DB (see §7) |
| /workspace/nfl-sim/backtest/ (REPORT, hist_props/SUMMARY, new_checks_oct19/results, rerun) | Oct 16–19 | FD 2024–25 props backtest; check backtests | Current evidence |
| /workspace/nfl-sim/notes/new_checks_backtest_2026-10-19.md | Oct 19 | 4 checks verdicts (flag/drop) | Current |
| /workspace/nfl-sim/notes/team_notes.md | Oct 24 | ESPN biggest-D-issue per team (Wk6), DvP by team, injury/news updates to Oct 24 | Current through Oct 24 |
| /workspace/nfl-sim/notes/film/ (README, teams/32 dirs, video/20 files, processed-games.json) | Oct 22–29 | Per-team weekly film+NGS notes; official highlight videos | Partial |
| /workspace/nfl-*-2025-2026.csv (16 files), nfl-coach-history.csv, nfl-coaching-profiles-2026.csv | Oct 22 | Seed tables (see §4) | Data through ~Wk 4–6 |
| /workspace/nfl-database/repo/ | snapshot 2026-10-29 08:39 UTC | User's matchup DB (SQLite, 107 games) | **PRIMARY game data going forward** (§7) |

Full automated inventory of 261 indexed files (path, mtime, size, first line) is in Appendix A. BetGuru's extra folders (models, scripts, ens, usage_sim, notes/mc, raw, data, hist, prices_1024, archetypes, suave-signup raw) are listed in Appendix B with file counts; they were indexed, not read line by line.

---
## 2. Rules and methodology (consolidated, current)
### 2a. Version lineage
1. Oct 11 AM: SMOKE_BETTING_SCRIPT.md (12 checks) + betting_script_betguru.md (13 gates, G/A/R scoring) → merged into NFL_BETTING_SCRIPT.md (28 steps).
2. Oct 11 PM: SKILL.md §14–16 written from postmortems (postmortem_oct11_early.md §6).
3. Oct 13: GAME_SCRIPT.md v1 (routine guide; precedence user rules > SKILL hard rules > 13 gates > defaults).
4. Oct 15–24: user-approved rules in shared memory (below).
5. Oct 27/29: user's Custom Phase Script (PHASE_SCRIPT.md) = projection model; Oct 29: Rico's MASTER_PROMPT.md = data collection; SKILL.md §20 links both.
**Who owns what now:** PHASE_SCRIPT.md produces projections/percentiles/leans; SKILL.md gates decide whether a leg is bettable; MASTER_PROMPT.md defines the database feeding both.

### 2b. Projection model (PHASE_SCRIPT.md)
- Pipeline: lock roles → defensive coverage profile (YPT by position/route, Outside YPT, blitz %, RZ TD%, run YPC) → role grade → triggers → recent environment match → base projection → 3-model consensus (Monte Carlo 10k + Bayesian + Game Randomness) → FD/DK main + alts → Over/Under/Alt/No Bet → sheet.
- Thresholds: Outside YPT ≥10.5 positive for Explosive; WR YPT ≥9.0 slight positive for Volume (boost capped +2–3%); TE YPT ≥8.0 positive / ≤5.5 cut TE yards; run YPC ≤3.8 = run suppression; >4.4 positive for Elite Rusher; high blitz cuts primary receivers, boosts check-downs.
- Percentiles: 5th Floor, 10th Slight Edge, 15th MAIN (primary betting number), 20th Edge, 25th Pure Edge, Median.
- Line process: score only vs actual line/alt; injury in-game = bet protect, not a miss; low total reduces soft boosts; blowout adjusts late volume; RZ usage boosts TD odds not yardage.
- Run-defense examples (Oct 27 version, kept in PHASE_SCRIPT.md per parent): Bears 4.44 YPC, Cowboys 4.72, Saints 4.81.

### 2c. Betting gates (SKILL.md, HARD unless noted)
- Injuries §5: only OUT/IR creates edges; no first-game-back full-volume overs.
- Form §7: line cleared 3 of last 4 with today's QB; catches need tgt×catch% clear and catch ≥65%.
- Area §8: no over into a defense's strength / under into its weakness.
- Game flow §9 + §14 "could trail" (dog, fav ≤3, or trails ≥35% of sims any quarter): no RB rush over on could-trail team unless 4+ tgt/g; no RB rush under on 3+ fav leading ≥50% sims; committee back needs 60%+ carry share 3 of 4; no check-down TE/RB rec-yds under, no QB pass-yds under on could-trail team.
- Price §10/§18: sim median must clear line; beat de-vigged sharp prob by ≥3 pts; bucket shrink when a bucket runs 10+ pts under sims.
- §14 cushions: yards overs at ≤-150 need L4 median ≥20% above; -113..-149 need 25% and 10%+ clear 3 of 4; WR/TE yards overs need 4+ tgt each of L3 (unless line ≤15); catches overs 3.5+ need 5+ tgt 3 of 4 and no same-role teammate ≥28%; ≤3 tgt/g players max 1 per slip, none on Basic; QB yards projection must clear by 12%; screen QB rushing weekly.
- §15 QB grade card A–F (vs blitz, no blitz, protection, money downs, clutch); blitz-blend YPA; expected sacks; cut rules (vs-blitz D/F vs 35%+ blitz; no-blitz D/F vs <25%; protection D/F with 3+ exp sacks).
- §19 wind ≥15 mph sustained cuts deep/QB yards/totals; hidden starter losses (OT/slot CB).
- §20 Panthers rule: opp blitz top-10 / pass-rush win rate top-10 / OL injury + poor QB sack rate vs that package → CAUTION, discuss with user. NGS from public pages only; paid stats marked missing.
- Slips §11–12: tiers Basic/Intermediate/Pro/Pure Edge; 1–2 unders max; no player on >1 slip; no same-QB receiver pairs; 100–200k MC per slip; stake 0.5/0.3/0.2 units.

### 2d. User-approved rules in shared memory (RecallMemory, Oct 29 search)
- Oct 13: backup RB ≥25% carries → no starter rush overs on safe tiers; freeze rule; play-volume rule; leg on ≤2 slips. **Blitz check and "no over when median under line" NOT approved** (also rules_from_videos P1/P2 "PROPOSED").
- Oct 16: no ungraded TD legs on main slips; cap split-backfield rush ladders; no spread/ML when QB fails pressure check; max 3 tickets/game, no player on >half.
- Oct 19: Questionable players no longer auto-cut; cleared/cut at ~90-min inactives; no overs on players who missed every practice. Four checks backtested: flag-only/drop (notes/new_checks_backtest_2026-10-19.md).
- Oct 21: locked board; late adds go on a separate small slip.
- Oct 24: don't play too safe — pick a modest middle rung when matchup shows an edge; factor QB blitz rate, target share, snaps, opp explosives allowed.
- Oct 14 (SKILL.md "Star unders"): star unders only with data-backed matchup reason.
- Bankroll/staking (rules_from_videos B1–B7, betting_script_betguru.md): main slips 3–4 legs; flat 1–5%; ~20% daily cap; log CLV.

### 2e. BetGuru-reported rules (verification status)
| Rule | Status |
|---|---|
| Middle rung, clears ~65–75% | Middle-rung rule traced (memory Oct 24); the 65–75% figure **reported by BetGuru** |
| RB grading vs RB-specific allowances × YPC × carries | **Reported by BetGuru** (method appears in notes/sat_slip_check_2026-10-24.md, no user statement found) |
| Matchup + game script over raw recent numbers | Partly traced: memory Oct 10 (justify by game script) and Oct 24; otherwise reported by BetGuru |
| Backup-QB target share from that QB's starts | **Reported by BetGuru**; consistent with SKILL §7 current-QB rule and betting_script_betguru.md Gate 2 |
| Source trust order (counted stats > PFF history > RotoBaller > fantasy/AI) | **Reported by BetGuru**; not found in files or memory |
| TD and rushing legs on separate small slips | Traced: notes/new_checks_backtest_2026-10-19.md ("existing slip rules … TD and rushing legs on separate small slips"); memory Oct 16 (no ungraded TD on main) |
| Max 2 unders | Traced: SKILL §11 (1–2); notes/tnf_game_script_2026-10-15.md |
| One stat per player per slip | Traced: notes/tnf_game_script_2026-10-15.md; postmortem_2026-10-22.md violations list |
| 90-min inactives check | Traced: memory Oct 19; SKILL §14 (~2 h recheck) |
| 60% snap share for WR/TE | **Reported by BetGuru**; files have 55% (SKILL §14 new-role) and ≥70%/<45% (Gate 9) |
| 55–70% bucket hit 36% | Traced: postmortem_oct11_early.md (0.55–0.70 hit 5/14, 36%, avg sim 0.61) |

---
## 3. Lessons learned (graded misses and missed wins)
Format: date | player | line | result | cause → rule. Source per block.

### Oct 11 early slate (Week 5) — /workspace/nfl-sim/postmortem_oct11_early.md
| # | Player | Line | Result | Lesson → rule |
|---|---|---|---|---|
| L1 | D'Andre Swift | 100+ rush+rec | 73 (9 carries) | committee/trailing script → SKILL §9/§14 could-trail RB rule |
| L2 | Drake Mayer | o3.5 rec | 1 | low-target TE → §14 catches need 5+ tgt 3 of 4 |
| L3 | Jonathan Taylor | 60+ | 45 | game script → §14 |
| L4 | Cam Ward | 175+ pass | 170 (4 sacks) | protection/pressure → §15 QB card |
| L5 | Malik Willis | o190.5 | 137 | QB room → §14 12% QB cushion |
| L6 | Henderson | o46.5 | 22 | split backfield → backup-RB rule |
| L7 | Tyler Shough | 10+ rush | 0 | QB rushing variance → §14 screen QB rush |
| L8 | Juwan Johnson | 40+ | 16 | TE role → §14 |
| L9 | Chris Olave | 6+ rec | 4 | catches cushion → §14 |
| L10 | Romeo Doubs | o3.5 rec | 1 | ≤3-target player → §14 max 1/slip |
| L11 | Deshaun Watson | 201+ | 155 (7 sacks) | pressure → §15 protection D/F + 3 exp sacks |
| L12 | Daniel Jones | U211.5 | 267 | QB under on trailing team → §14 no QB yds under on could-trail |
| L13 | Woody Marks | U36.5 | 62 | RB under → §9 |
| L14 | Sadiq | 15+ | 3 | low-volume TE → §14 |
| Calib | 0.55–0.70 sim bucket | — | 5/14 = 36% vs 0.61 avg sim | → §10 bucket shrink |
### Oct 11 Smoke legs — /workspace/nfl-sim/postmortem_smoke_oct11.md
| L15 | M. Washington | 45+ | 44 | yard cushion → §14 20/25% cushion |
| L16 | Judkins | 16+ | 6 | role/script |
| L17 | I. Williams | 20+ | 16 | low-target → §14 |
| L18 | T. Warren | U43.5 | 83 | check-down TE under on trailing team → §14 |
| L19–21 | Missed big lines: Gordon, Bernard, Croskey-Merritt | — | hit | vacated-role / RB volume → §14 vacated roles |
### MNF Oct 12 — /workspace/nfl-sim/bets/expected_vs_actual_ledger.md; loss_review_wk5_6.md
| L22 | Kyren Williams | 50+ | 49 | only loss on our MNF slips; committee (Kyren–Corum) → memory Oct 19 committee rule |
| L23–25 | Kincaid, Corum, Coleman legs | — | lost | low-volume roles |
### TNF Oct 15 SEA@DEN (DEN 17–14 OT) — /workspace/nfl-sim/postmortem_2026-10-15.md
| L26 | All 9 user tickets | — | lost; −$87.27 cash + $200 bonus bets; legs 35/62 | — |
| L27 | Anytime TDs | — | 0/12 | → memory Oct 16 no ungraded TDs on main |
| L28 | SEA side/spread legs | — | lost | → no spread/ML when QB fails pressure check |
| L29 | Wilson | 60+/70+ | 52 | split/volume caps |
| L30 | Missed wins: Shaheed 3+, JSN overs | — | hit | — |
| L31 | Paper tiers v2 | — | would have netted ~+$7.50 | exposure cap → max 3 tickets/game |
### Week 6 Sunday Oct 18 — /workspace/nfl-sim/postmortem_2026-10-18.md
| L32 | User DK1018-1 | — | won +$162 | week +$13.53 on $163.47 (~+8% ROI), all from one boosted ticket |
| L33 | FD1018-8L, FD1018-15L, SNF ticket | — | lost | many-leg parlays |
| L34 | Model board | — | zero bets | over-strict gates |
| L35–37 | Missed wins Bowers 70+, Strange 4+, Flowers 5+ | — | all hit (Sat Slip 1 would be 3/3) | → Oct 24 "don't play too safe" |
### MNF Oct 19 WAS@SF (SF 23–17) — /workspace/nfl-sim/postmortem_2026-10-19.md
| L38–44 | Cut winners: R. White U44.5, Kittle O66.5, CMC O4.5 rec, Purdy O249.5, Purdy O19.5 rush, Daniels O210.5 (+ correct cuts listed) | — | hit | zero-bet day; proposed: calibrate model A vs Pinnacle, vacated usage, zone-softness |
### TNF Oct 22 NE@CHI (CHI 30–24) — /workspace/nfl-sim/postmortem_2026-10-22.md
| L45 | 7 user tickets (off-model) | $240 staked vs $90 stated | −$190 settled; FD1022-3 pending (Roschon market type) | bankroll reconcile |
| L46 | Caleb Williams | O241.5 | 308 | **cut by pressure check — wrong** |
| L47 | Drake Maye | O246.5 | 321 | **cut by pressure check — wrong** (tipster also lost Maye U247.5, tipster_summary.md) |
| L48–49 | A.J. Brown U, Odunze O | — | won | **cut by Pinnacle veto — wrong** |
| L50 | Stevenson 40+ rush (tipster slip) | — | 22 | tipster_summary.md |
### Daniels MNF Oct 19 (tipster) — tipster_summary.md: Daniels 30+ rush had 10.
**Lessons logged: 50 (L1–L50).**

### Hit-rate / ROI figures (as recorded)
- All-time legs 164/247 = 66%; TDs 3/17; spread/ML 0/5; RB rush 7/23 (30%); receiving yards 46/52 — /workspace/nfl-sim/bets/leg_hit_rates.md (Oct 16).
- Week 6: +$13.53 on $163.47 (~+8%) — postmortem_2026-10-18.md.
- TNF Oct 15: −$87.27 + $200 bonus — postmortem_2026-10-15.md. TNF Oct 22: −$190 on $240 — postmortem_2026-10-22.md.
- Hist props FD 2024–25 (21,480 rows): overs lose 9–14% flat at close, unders ~breakeven; model vs market OOS negative every market (rec yds ~−5.5%, rec −6.1%, rush −1.5%, ATD −14.3% at e≥3) — backtest/hist_props/SUMMARY.md.
- Our model Wk2–5 (n=1,659): raw 54.4% / −0.2%, edge3 +2.4%; shrunk 54.3%, Brier 0.244; receptions shrunk 60.8% / +1.2%, edge3 63.4% / +10.5%; Oct 11 shrunk 56.5%, edge3 +6.6% — /workspace/nfl_engine/BACKTEST_REPORT.md.
- New checks: falling WR/TE snap share −21.8%; TD flagged −18.7% vs kept −5.1%; play-count +0.9 pt — notes/new_checks_backtest_2026-10-19.md.
- Tipster @MrBearBets/@GameGridAppp 3-14 overall, NFL 3-6 — notes/tipster_summary.md.

---
## 4. Data assets
### 4a. Seed CSVs (/workspace, dated Oct 22) — rows
archetypes 264; coaching 64; def-stickiness 64; defender-archetypes 595; direction-splits 903; game-script 6; injury-snaps 2,367; line-movement 337; ol-vs-rush 128; pace 64; personnel 338 (**2025 participation only**); qb-target-tendency 41; redzone-roles 2,250; referees 17; rest-travel 674; team-blitz 98; weather-venue 15; nfl-coach-history.csv 508 (2015+); nfl-coaching-profiles-2026.csv 96 (HC/OC/DC callers + identity_summary). Files: /workspace/nfl-<name>-2025-2026.csv.
### 4b. nflverse raw — /workspace/suave-signup/data/nfl/raw/ (23 files incl. FTN charting 2022–2026 parquet, 2026 pbp, weekly stats, snaps, backup_20261024). Also nfl-sim/raw, data, hist (BetGuru pulls). FTN blitz proxy: n_pass_rushers ≥5 or n_blitzers >0 (build_nfl_v4.py; blitz_db/STATUS.md).
### 4c. Prices — /workspace/prices_1024/ (48 files, FanDuel public JSON Oct 24; dk_try.json = DraftKings attempt, DK returns 403 from this box per BetGuru). nfl-sim/alt/fd_pull.py **not found** at that path. Hist FD props 2024–25 in nfl-sim/backtest/hist_props (Odds API credits 18,936/20,000 used).
### 4d. Archetypes — /workspace/archetypes/ (defense_vs_archetype_2025_2026.csv, te_archetypes.csv, build/def_allow scripts).
### 4e. Grader — sb-fix build_nfl_v4.py weights: usage_rate 10, target_share 10, matchup_lb_cb 12, qb_pressure_blitz 6, def_zone_rate 5, def_man_rate 5, def_explosive_allowed 7, recent_form 16, injury_status 9, coach_tendencies 6, third_down_off 4, third_down_def_allowed 4, red_zone_td_off 3, red_zone_td_def_allowed 3 (=100). Score = weighted mean of present inputs; missing labeled "missing source"; price non-weighted (FD snapshot Oct 23 05:50 ET). Data Wk 1–6 only.
### 4f. Engine — /workspace/nfl_engine: posterior opportunity sim (500k runs, OUT-only injuries). BACKTEST_REPORT.md: shipped engine fails on real nflverse data (no_play column, OTHER-bucket bug); engine 50.5–50.6%, Brier 0.29–0.33 vs ours 0.244; patched engine better only on pass yards (53.1%/+2.1%, n=98). VERIFICATION.json: synthetic_only. **Verdict: not production.**
### 4g. Other nfl-sim assets: models/ (13 per-game sim CSVs Oct 15–18), scripts/ (80), usage_sim/ (42), notes/mc (Elo538, historic projected spreads), matchup/ (build.py, matchup.py + test_matchup_phase1.py), dossier/, clv/, blitz_db (DuckDB Weeks 1–6, 93 games; 22 candidate legs all TEs — STATUS.md).
### 4h. Data gaps (cross-file)
- 2026 man/zone coverage and pass-rush win rate: none free (DATA_REGISTRY.md; blitz_db/STATUS.md; SKILL §20).
- Personnel/participation 2026 missing (seed CSV is 2025).
- NGS API 401 / downloads failed (postmortem_oct11_early.md; BACKTEST_REPORT.md) → public pages only.
- balldontlie 401, statshawk needs auth, muffed trusted (nfl-contest/new_sources_check_2026-10-24.md).
- YouTube bot-blocks video fetch (notes/film/README.md).
- bet-log Oct 25 partial; leg_hit_rates stale since Oct 16; BetGuru routines failing since Oct 25 (BetGuru report; MASTER_PROMPT Phase 6 notes).

---
## 5. Team and scheme knowledge
- ESPN Week 6 "biggest defensive issue" for all 32 teams, e.g. DAL 168.4 rush yds/g allowed (last), ARI 8.5 net YPA (worst), JAX #1 run D, MIN best NGS EPA — /workspace/nfl-sim/notes/team_notes.md.
- Injury/news through Oct 24: Lamar OUT (Huntley starts), Nacua Q, Adams IR, Egbuka OUT, J. Love OUT — team_notes.md. James Cook fumble/carry warning (memory Oct 14).
- Run-defense YPC: Bears 4.44, Cowboys 4.72, Saints 4.81 — PHASE_SCRIPT.md.
- Coaching identities (96 callers) — /workspace/nfl-coaching-profiles-2026.csv; 2026 blitz/sack/PROE per team — Appendix C (built from nfl-team-blitz, coaching, pace CSVs).
- Coverage studies: notes/coverage_study_sea_wk3_wk5.md, dvp_week6_2026.md, route_personnel_sources_2026-10-21.md; blitz_db/team_profiles_2026-10-22.md; film notes in notes/film/teams/<TEAM>/.

---
## 6. Open questions and contradictions
1. **"No over when sim median < line"**: HARD in SKILL §10, but user did NOT approve it Oct 13 (memory) and rules_from_videos P2 = PROPOSED.
2. **Blitz rule**: user did not approve blitz check Oct 13, approved QB-pressure rule Oct 15–16; GAME_SCRIPT §3 still reads "NOT approved"; pressure check then wrongly cut Caleb O241.5 (308) and Maye O246.5 (321) Oct 22.
3. **Questionable players**: SKILL §5 = only OUT creates edges/Q avoided; memory Oct 19 = Q not auto-cut, decided at 90-min inactives.
4. **Star unders**: GAME_SCRIPT "no unders on stars" vs SKILL star-unders allowed with data reason (Oct 14).
5. **Unders per slip**: SKILL §11 1–2 vs tnf notes "max 1 except Intermediate 2".
6. **Leg exposure**: SKILL "no player on >1 slip" vs memory Oct 13 "leg on at most 2 slips".
7. **Models**: PHASE_SCRIPT MC+Bayesian+Game Randomness vs GAME_SCRIPT MC + Bayesian + 0.8/0.2 ensemble.
8. **Rung choice**: SKILL cushions push to lowest rungs; memory Oct 24 says middle rung; PHASE_SCRIPT says 15th pct MAIN.
9. **Bankroll**: $90 stated vs ~$355.80 ledger; $240 staked Oct 22 (bankroll_reconcile_2026-10-22.md).
10. **Unconfirmed tickets**: FD +3582 (Oct 18), DK1019 screenshot, FD1022-3 Roschon market type.
11. **Pinnacle veto** wrong Oct 22 (Brown U, Odunze O); hist backtest says model loses to market OOS — tension on when to trust sharp line.
12. **Week labels** (see top).
13. **Snap share threshold**: 55% (SKILL) vs ≥70% (Gate 9) vs 60% (BetGuru-reported).
14. Missing: Oct 25/26 postmortem; nfl-sim/alt/fd_pull.py; repo projection model withheld.

---
## 7. User repo: nfl-matchup-database (PRIMARY game data going forward)
Path /workspace/nfl-database/repo (github.com/GhostPapii21/nfl-matchup-database). Snapshot created 2026-10-29 08:39 UTC = 4:39 AM ET (manifest.json). 107 games, 2026-09-09 → 2026-10-26, all STATUS_FINAL. Query from repo/: `python3 query.py --sql '...'` (data/nfl_matchups.sqlite). Maintainer sync checks daily 9:00 AM ET, publishes only on change (SYNC.md).
### Tables (manifest.json counts; columns from PRAGMA)
| Table | Rows | Holds |
|---|---|---|
| games | 107 | game_id, date, status, data JSON |
| plays | 19,815 | ESPN pbp: offense, down, distance, play_type, yards (all 107 games) |
| player_stats | 8,851 | ESPN player box stats by category |
| espn_boxscores | 93 | raw box scores, Weeks 1–6 (16/16/16/16/15/14 by week) |
| historical_game_audits | 93 | play-count audits, all VERIFIED |
| profiles | 428 | offense 214 + defense 214 team-game profiles (inferred layer) |
| supplemental_records | 45,715 | nflverse layers: FTN charting 15,904 (Wk1–6), depth charts 13,324, snap counts 8,671, PFR advstats def 2,668/rec 1,502/rush 736/pass 213, injuries 1,789, NGS rec 440/pass 190/rush 185, games 93 |
| supplemental_play_links | 14,735 | supplemental record ↔ play |
| external_observations | 8,963 | Sharp advanced 8,260, ESPN win rates 244, Sharp position 160/scheme 128/tendencies 128, StatRankings 43 |
| external_profile_links | 9,146 | observation ↔ profile |
| external_fetches / external_gaps | 70 / 376 | fetch log, gap records |
| external_rosters | 2,557 | team rosters |
| ngs_route_charts / ngs_carry_charts / visual_notes | 189 / 184 / 2 | NGS targeted route charts (Wk1–6 + 2 Wk7) and carry charts |
### Coverage by layer
- Full (107 games through MNF Oct 26): games, ESPN pbp, player stats, profiles.
- Weeks 1–6 only (93 games): ESPN raw box, audits, FTN, snaps, PFR, injuries, NGS, depth charts (README.md "Supplemental coverage strongest for Weeks 1–6").
- Week 7: 13 games (all 12 Oct 25 games + MNF); Sharp Week 7 EPA/success/pressure-allowed imported Oct 28 (84 obs, 28 team-games) (DATA_GAPS.md).
### Documented gaps (DATA_GAPS.md, Phase 10 run 2026-10-27 04:43 UTC)
STALE: ESPN win rates, Sharp position/scheme/tendencies; FETCH_ERROR: raiders_cb; partial paid metrics: StatRankings; incomplete: route participation, TPRR/YPRR by coverage, RB run concepts, coverage shells, player assignments, film, daily injury chronology. No green-card readiness certified.
### Open model defects (DATA_GAPS.md publication review 2026-10-29)
1. Credited play yards — game 401873007 play 401873007411 stored 7 yds vs description Golden 37-yd reception + taunting penalty.
2. Returning-player workload — Jacobs' return (11 car, 7 tgt Wk7) diluted by absence history; Savion Williams similar.
3. Participation denominator — Coker 5 appearances; missing stat row ≠ zero.
4. QB rushing — uses team designed-run templates, omits kneels.
Projection model withheld ("not promoted"); treat derived explosive counts and baseline projections as provisional.
### Overlap / conflicts with nfl-sim / nflverse
- Same nflverse FTN/snaps/PFR/NGS as suave-signup raw and blitz_db (Weeks 1–6, 93 games) — repo adds ESPN pbp for Week 7 and Sharp Week 7.
- Player IDs differ by provider (ESPN vs nflverse gsis) — join by name normalization (HANDOFF_FOR_SMOKE.md tip) or roster table.
- ESPN numeric yardage can mis-credit penalty plays (defect 1); nflverse pbp separates penalties — prefer nflverse for yardage where both exist.
- Week numbering: repo uses ESPN weeks (Oct 25 = Week 7), matching nflverse.
- Repo has no props/prices, bets, or man/zone; nfl-sim keeps those.

---
## Appendix A. File index (auto)
| Path | Modified | Size | Title / first line |
|---|---|---|---|
| /workspace/nfl-database/MASTER_PROMPT.md | 2026-10-29 | 5730 | # NFL Defensive and Offensive Matchup Database: Master Prompt (from Rico, pasted by the user to Ghost6 on Oct 29, 2026, verbatim) |
| /workspace/nfl-database/PHASE_SCRIPT.md | 2026-10-29 | 4925 | # NFL Custom Phase Script — Full Model (Updated Oct 29, 2026) |
| /workspace/nfl-database/SKILL_backup_2026-10-29.md | 2026-10-29 | 19568 | --- |
| /workspace/nfl-sim/DATA_REGISTRY.md | 2026-10-22 | 8854 | # NFL data registry (check here first) |
| /workspace/nfl-sim/GAME_SCRIPT.md | 2026-10-22 | 10266 | # GAME SCRIPT v1: NFL + WNBA (BetGuru routines follow this). Built Tue Oct 13, 2026 |
| /workspace/nfl-sim/HANDOFF_FOR_SMOKE.md | 2026-10-22 | 7867 | # HANDOFF FOR SMOKE: BetGuru's Week 5 (Sun Oct 11, 2026) data, all under /workspace/nfl-sim/ |
| /workspace/nfl-sim/NFL_BETTING_SCRIPT.md | 2026-10-22 | 3825 | # NFL Prop Betting Script (Smoke + BetGuru, Oct 11 2026) |
| /workspace/nfl-sim/SMOKE_BETTING_SCRIPT.md | 2026-10-22 | 5682 | # Smoke NFL Betting Script (locked Sun Oct 11, 2026, ~8 AM ET) |
| /workspace/nfl-sim/alternates_oct10.md | 2026-10-22 | 2035 | # Sunday Oct 11 backups (BetGuru, Sat 9:10 AM ET). FanDuel prices. Blended = avg of my two sims. |
| /workspace/nfl-sim/backtest_newscript_oct11.md | 2026-10-22 | 41077 | # Backtest: updated NFL betting script on Sun Oct 11, 2026 |
| /workspace/nfl-sim/bal_atl_build_oct11.md | 2026-10-22 | 1141 | # BAL@ATL 8:20 PM: build in progress (4:30 PM ET) |
| /workspace/nfl-sim/betguru_mnf_oct12.md | 2026-10-22 | 16715 | # BetGuru — MNF Oct 12, 2026: Buffalo Bills @ Los Angeles Rams |
| /workspace/nfl-sim/betguru_slips_oct11.md | 2026-10-22 | 38626 | # BetGuru Slips, Sun Oct 11, 2026: **v6 LOCK 9:34 AM ET (full rebuild; see the bottom section; everything above is superseded)** |
| /workspace/nfl-sim/betguru_slips_oct18.md | 2026-10-22 | 18602 | # BetGuru slips: Sunday Oct 18, 2026 (Week 6), built Mon Oct 12 ~12:30 AM ET |
| /workspace/nfl-sim/betting_script_betguru.md | 2026-10-22 | 20587 | # BetGuru BETTING SCRIPT v1 (NFL player props): built Sun Oct 11, 2026 |
| /workspace/nfl-sim/crosscheck_smoke.md | 2026-10-22 | 26712 | # Cross-check of Smoke's Sunday Oct 11 files vs /workspace/nfl-sim (built Sat Oct 10, ~1:30 AM ET) |
| /workspace/nfl-sim/dk_edges.md | 2026-10-22 | 11763 | # DraftKings edges, Sunday Oct 11 2026 (odds-bridge pull ~7:30 AM ET Sat) |
| /workspace/nfl-sim/ensemble_mnf_oct12.md | 2026-10-22 | 119478 | # Ensemble MNF: BUF @ LAR, Oct 12 2026 (500k linked sims) |
| /workspace/nfl-sim/injury_edge_oct11.md | 2026-10-22 | 15841 | # BetGuru Injury-Edge Analysis — Sun Oct 11, 2026 (Week 5) |
| /workspace/nfl-sim/injury_update_oct11_am.md | 2026-10-22 | 9616 | # Injury / Inactive / Weather / Line Update: Sun Oct 11, 2026 (AM, ~7:50-8:00 AM ET) |
| /workspace/nfl-sim/live_slips_oct11.md | 2026-10-22 | 1160 | # Live slips: DEN@LAC, DET@ARI, SF@SEA. Data pulled 4:28 PM ET (FD live event pages + ESPN summary) |
| /workspace/nfl-sim/live_tracker_last_post.md | 2026-10-22 | 977 | # Last BlueBook post (placed-slips tracker) |
| /workspace/nfl-sim/live_tracker_last_post_prepared.md | 2026-10-22 | 364 | # Prepared last_post update (apply AFTER parent sends BlueBook message) |
| /workspace/nfl-sim/live_tracker_run_1621.md | 2026-10-22 | 2287 | # Live tracker run 4:21 PM ET — Oct 11, 2026 |
| /workspace/nfl-sim/live_tracker_run_2329.md | 2026-10-22 | 957 | # Live tracker run — placed slips — 2026-10-11 11:29 PM ET |
| /workspace/nfl-sim/live_tracker_run_2359.md | 2026-10-22 | 632 | # Live tracker run — placed slips — 2026-10-11 11:59 PM ET |
| /workspace/nfl-sim/live_tracker_skip_log.md | 2026-10-22 | 535 | # Live tracker skip log |
| /workspace/nfl-sim/loss_review_wk5_6.md | 2026-10-22 | 8718 | # Loss review: NFL Week 5 (Sun Oct 11; nflverse labels it Week 5) + MNF Oct 12 BUF@LAR |
| /workspace/nfl-sim/matchup_dossier.md | 2026-10-22 | 47139 | # Matchup Dossier: NFL 2026 Week 5, Sunday Oct 11 (13 games) |
| /workspace/nfl-sim/merged_slips_sunday.md | 2026-10-22 | 9211 | # Merged Sunday Oct 11 slips (ours + Smoke). Built Sat Oct 10, ~1:40 AM ET |
| /workspace/nfl-sim/merged_slips_v2.md | 2026-10-22 | 10446 | # Merged Sunday Oct 11 slips, v2 (roster-verified rebuild) |
| /workspace/nfl-sim/placed_slips_oct11.md | 2026-10-22 | 12580 | # Sunday Oct 11, 2026 NFL slips (FanDuel), live tracker source of truth |
| /workspace/nfl-sim/postmortem_2026-10-15.md | 2026-10-22 | 8192 | # Post-game recap: TNF SEA @ DEN, Thu Oct 15 2026 (written Fri Oct 16, ~9:20 AM ET) |
| /workspace/nfl-sim/postmortem_2026-10-18.md | 2026-10-22 | 8844 | # Post-game recap: NFL Sunday Oct 18, 2026 (Week 6) — written Mon Oct 19 ~9:30 AM ET |
| /workspace/nfl-sim/postmortem_2026-10-19.md | 2026-10-22 | 7961 | # Post-game recap: MNF WAS @ SF, Mon Oct 19, 2026 (Week 6) — written Tue Oct 20 ~9:15 AM ET (morning-after routine, BetGuru) |
| /workspace/nfl-sim/postmortem_2026-10-22.md | 2026-10-23 | 15533 | # Postmortem: Thursday Oct 22, 2026 (TNF NE @ CHI + NBA CLE @ PHI, DEN @ OKC) |
| /workspace/nfl-sim/postmortem_oct11_early.md | 2026-10-22 | 24041 | # Post-mortem: NFL Sunday Oct 11, 2026 (early window: London + 1 PM) |
| /workspace/nfl-sim/postmortem_smoke_oct11.md | 2026-10-22 | 8512 | # Post-mortem: Smoke's 1 PM legs, Sun Oct 11 2026 (written 4:20 PM ET) |
| /workspace/nfl-sim/premortem_oct11.md | 2026-10-22 | 8856 | # Pre-mortem: BetGuru v4 Intermediate (+2517), Sun Oct 11, written ~8:55 AM ET |
| /workspace/nfl-sim/pure_edge_slip.md | 2026-10-22 | 1053 | # Pure Edge slip, Sunday Oct 11 (BetGuru, Sat 2:30 AM ET) |
| /workspace/nfl-sim/qb_run_pattern_wk1-5.md | 2026-10-22 | 3579 | # QB "abandon the pass and run" scan — 2026 Weeks 1-5 (nflverse pbp pulled Oct 13, 2026) |
| /workspace/nfl-sim/rescout_oct10.md | 2026-10-22 | 9409 | # Rescout: NFL Sunday Oct 11, 2026 slate (13 games), as of Sat Oct 10, ~10:25-10:45 AM ET |
| /workspace/nfl-sim/script_survival_oct11.md | 2026-10-22 | 199493 | # Game-script survival sheet: Sunday Oct 11, 2026 (13 games) |
| /workspace/nfl-sim/slip_justification.md | 2026-10-22 | 38162 | # Leg-by-leg game-script justification: Sunday Oct 11, 2026 (FanDuel) |
| /workspace/nfl-sim/slip_resim.md | 2026-10-22 | 3047 | # Slip re-sim, Sunday Oct 11 (joint Monte Carlo, 20,000 draws from sim_week5.pkl) |
| /workspace/nfl-sim/smoke_4tier_slips_oct11_noon.md | 2026-10-22 | 10241 | # Smoke 4-tier slips, Sun Oct 11 2026 (noon run, written ~12:40 PM ET) |
| /workspace/nfl-sim/smoke_6leg_slips_oct11.md | 2026-10-22 | 10449 | # Smoke 6-leg slips, Sun Oct 11 2026. UPDATE 10:30 AM ET (repeat flex applied) |
| /workspace/nfl-sim/smoke_backtest_confirm_oct11.md | 2026-10-22 | 3222 | # Oct 11 backtest: independent confirmation (Smoke, Mon Oct 12 ~1 AM ET) |
| /workspace/nfl-sim/smoke_late_slips_oct11.md | 2026-10-22 | 3067 | # Smoke late-window slips: 4:05 / 4:25 / 8:20 PM ET, Sun Oct 11 2026 (v2, ~1:15 PM ET; softened price rule) |
| /workspace/nfl-sim/smoke_mnf_oct12.md | 2026-10-22 | 10948 | # Smoke: MNF Mon Oct 12, 2026, Buffalo Bills @ Los Angeles Rams (built ~1:00 AM ET) |
| /workspace/nfl-sim/smoke_original_slips_graded_oct11.md | 2026-10-22 | 62265 | # Smoke slips, Oct 10–11, 2026: graded as-is vs final box scores (Sun Oct 11 NFL) |
| /workspace/nfl-sim/smoke_premortem_oct11.md | 2026-10-22 | 7743 | # Smoke pre-mortem, Sun Oct 11 2026 (written ~9:05 AM ET). SMOKE_BETTING_SCRIPT.md was not edited. |
| /workspace/nfl-sim/smoke_skill_run_oct11.md | 2026-10-22 | 12885 | # Smoke: nfl-betting-script SKILL run, Sun Oct 11 2026 (Week 5; ~9:45 AM ET). Pro cancelled. Analysis only; no outcome is guaranteed. |
| /workspace/nfl-sim/smoke_slips_oct18.md | 2026-10-22 | 8153 | # Smoke: Sunday Oct 18, 2026 slate (built Mon Oct 12 ~1:05 AM ET) |
| /workspace/nfl-sim/smoke_snf_slips_oct11.md | 2026-10-22 | 4565 | # Smoke SNF slips: BAL@ATL 8:20 PM ET, Sun Oct 11 2026 (written ~4:35 PM ET) |
| /workspace/nfl-sim/smoke_tracker_oct11.md | 2026-10-22 | 2125 | # Smoke slips live tracker, Sun Oct 11 2026 (FanDuel). Status: PENDING / LIVE (stat) / HIT / MISS |
| /workspace/nfl-sim/stress_test_15leg_2026-10-25.md | 2026-10-23 | 3565 | # Stress test: 15-leg FD parlay, non-TD legs (12), Sun Oct 25 2026 |
| /workspace/nfl-sim/stress_test_oct10.md | 2026-10-22 | 10431 | # Stress test: unplaced Sunday Oct 11 slips + news check on placed bets |
| /workspace/nfl-sim/trade_log.md | 2026-10-22 | 11082 | # NFL official trade log (official sources only: NFL.com, team sites, official NFL/NFL Network/team X accounts) |
| /workspace/nfl-sim/week6_report.md | 2026-10-22 | 23596 | # NFL props model: Sunday Oct 11, 2026 slate (nflverse labels this 2026 **Week 5**; Week 6 starts Oct 15) |
| /workspace/nfl-sim/specs/matchup_database_spec.md | 2026-10-22 | 1725 | # NFL Matchup Database Spec (user, Oct 21 2026) |
| /workspace/nfl-sim/bets/bet_log.md | 2026-10-22 | 3029 | ## TNF SEA vs DEN, Oct 15 2026, 8:15 PM ET (placed by user, logged 7:19 AM) |
| /workspace/nfl-sim/bets/expected_vs_actual_ledger.bak_2026-10-18.md | 2026-10-22 | 2816 | # Expected vs actual ledger (NFL) |
| /workspace/nfl-sim/bets/expected_vs_actual_ledger.md | 2026-10-22 | 10498 | # Expected vs actual ledger (NFL) |
| /workspace/nfl-sim/bets/leg_hit_rates.md | 2026-10-22 | 2289 | # Leg hit-rate tracker (updated 2026-10-16 ~12:45 AM ET) |
| /workspace/nfl-sim/bets/bet-log.backup_2026-10-16_pre_tnf.csv | 2026-10-22 | 22538 | bet_id,ticket_status,sport,game,sub_sgp_odds,player,team,prop,line,actual,leg_odds,result,closing_price,clv_pct,roi |
| /workspace/nfl-sim/bets/bet-log.backup_2026-10-19_pre_sunday.csv | 2026-10-22 | 32833 | bet_id,ticket_status,sport,game,sub_sgp_odds,player,team,prop,line,actual,leg_odds,result,closing_price,clv_pct,roi |
| /workspace/nfl-sim/bets/bet-log.backup_2026-10-20_pre_dk1019_grade.csv | 2026-10-22 | 43729 | bet_id,ticket_status,sport,game,sub_sgp_odds,player,team,prop,line,actual,leg_odds,result,closing_price,clv_pct,roi |
| /workspace/nfl-sim/bets/bet-log.backup_2026-10-20_pre_recap.csv | 2026-10-22 | 43325 | bet_id,ticket_status,sport,game,sub_sgp_odds,player,team,prop,line,actual,leg_odds,result,closing_price,clv_pct,roi |
| /workspace/nfl-sim/bets/bet-log.backup_2026-10-22_pre_fd1022.csv | 2026-10-22 | 45958 | bet_id,ticket_status,sport,game,sub_sgp_odds,player,team,prop,line,actual,leg_odds,result,closing_price,clv_pct,roi |
| /workspace/nfl-sim/bets/leg_history.csv | 2026-10-22 | 23382 | date,sport,slip,leg,category,price,implied,result |
| /workspace/nfl-sim/bets/pnl_ledger.csv | 2026-10-22 | 2324 | date,game,ticket,book,legs,odds,stake_cash,stake_bonus,result,cash_pnl,cumulative_known_cash_pnl,note |
| /workspace/nfl-sim/boards/board_2026-10-19_MNF.md | 2026-10-22 | 2562 | # Game-day board, Mon Oct 19 2026: MNF WAS @ SF, 8:15 PM ET (Levi's, outdoor). WNBA: no Finals game today. |
| /workspace/nfl-sim/boards/board_2026-10-22_TNF_gameday.md | 2026-10-22 | 1762 | # TNF NE @ CHI (Thu Oct 22, 8:15 PM ET) — game-day board, 12:25 PM ET |
| /workspace/nfl-sim/boards/board_2026-10-22_TNF_open.md | 2026-10-22 | 2118 | # TNF NE @ CHI (Thu Oct 22, 8:15 PM ET): OPENING snapshot + model, pulled Tue Oct 20 6:00 AM ET |
| /workspace/nfl-sim/boards/board_2026-10-22_TNF_pull1.md | 2026-10-22 | 1719 | # TNF NE @ CHI (Thu Oct 22, 8:15 PM ET) — pull 1 (probe), Tue Oct 20 5:57 AM ET |
| /workspace/nfl-sim/boards/board_2026-10-22_TNF_pull2.md | 2026-10-22 | 3931 | # TNF NE @ CHI (Thu Oct 22, 8:15 PM ET) — pull 2 (full), Wed Oct 21 9:36 PM ET |
| /workspace/nfl-sim/boards/board_2026-10-25_SUN_gameday.md | 2026-10-25 | 2017 | # BetGuru Sunday board, Oct 25, 2026 (built 12:25 PM ET) |
| /workspace/nfl-sim/boards/card_2026-10-22.md | 2026-10-22 | 8080 | # Thursday Oct 22, 2026 card — for the user's approval (NOTHING PLACED) |
| /workspace/nfl-sim/blitz_db/ADDENDUM.md | 2026-10-22 | 2920 | # Pass 2: the user's matchup blueprint (extend pass 1's outputs in /workspace/nfl-sim/blitz_db; do not rebuild what exists) |
| /workspace/nfl-sim/blitz_db/PASS10.md | 2026-10-23 | 3146 | # Pass 10: PER-GAME EDGE BOARDS (final graded A/B/C board). Read-only on blitz_matchup.duckdb; no bets, messages, keys or private feeds. Inp |
| /workspace/nfl-sim/blitz_db/PASS3.md | 2026-10-22 | 3710 | # Pass 3: targeted player breakdowns for the user's 7 Week 7 games (reuse blitz_matchup.duckdb + pass1/pass2 code; don't rebuild) |
| /workspace/nfl-sim/blitz_db/PASS4.md | 2026-10-23 | 2315 | # Pass 4: tighten the Week 7 focus leans (reuse blitz_matchup.duckdb + week7_focus_games_2026-10-25.md; free public data only; no paid/priva |
| /workspace/nfl-sim/blitz_db/PASS5.md | 2026-10-23 | 4923 | # Pass 5: DEFENSE LAYER for the Week 7 focus games (reuse blitz_matchup.duckdb; may read week7_focus_games_2026-10-25.md and pass-4 outputs  |
| /workspace/nfl-sim/blitz_db/PASS6.md | 2026-10-23 | 3245 | # Pass 6: RECEIVER/TE EDGE BOARD for the 7 Week 7 focus games (reuse blitz_matchup.duckdb, week7_defenders.csv, week7_defense_layer_2026-10- |
| /workspace/nfl-sim/blitz_db/PASS7.md | 2026-10-23 | 3838 | # Pass 7: user's focused deep dives (reuse blitz_matchup.duckdb and pass 3-6 outputs if present; free public data only; no paid/private APIs |
| /workspace/nfl-sim/blitz_db/PASS8.md | 2026-10-23 | 2711 | # Pass 8: FULL PROP LADDER TABLE (reuse week7_receiver_edges.csv, week7_receiver_edge_board_2026-10-25.md, week7_defense_layer_2026-10-25.md |
| /workspace/nfl-sim/blitz_db/PASS9.md | 2026-10-23 | 1918 | # Pass 9: COVERAGE SCHEME + ALIGNMENT layer from public articles (separate output; read-only on blitz_matchup.duckdb; public web pages only, |
| /workspace/nfl-sim/blitz_db/PROMPT.md | 2026-10-22 | 4103 | # Build: NFL blitz / rollout / coverage matchup database (2026 season to date) |
| /workspace/nfl-sim/blitz_db/STATUS.md | 2026-10-23 | 29267 | # Build status — 2026-10-22 |
| /workspace/nfl-sim/blitz_db/blueprint_slate_2026-10-25.md | 2026-10-22 | 301990 | # Matchup blueprint — 2026-10-25 / 2026-10-26 |
| /workspace/nfl-sim/blitz_db/slate_matchups_2026-10-22.md | 2026-10-22 | 80752 | # Slate matchup research — 2026-10-22 |
| /workspace/nfl-sim/blitz_db/team_profiles_2026-10-22.md | 2026-10-22 | 511099 | # Team profiles — 2026-10-22 |
| /workspace/nfl-sim/blitz_db/week7_coverage_alignment_2026-10-25.md | 2026-10-23 | 29666 | # Week 7 coverage scheme and alignment — October 25, 2026 |
| /workspace/nfl-sim/blitz_db/week7_defense_layer_2026-10-25.md | 2026-10-23 | 178251 | # Defense leak board — Week 7, October 25, 2026 |
| /workspace/nfl-sim/blitz_db/week7_focus_deepdive_2026-10-25.md | 2026-10-23 | 118520 | ## 1a. Watson vs Golden |
| /workspace/nfl-sim/blitz_db/week7_focus_games_2026-10-25.md | 2026-10-23 | 205776 | / game / key injury / blitz angle / best leans / confidence / |
| /workspace/nfl-sim/blitz_db/week7_game_edge_boards_2026-10-25.md | 2026-10-23 | 597698 | # Week 7 per-game edge boards — October 25, 2026 |
| /workspace/nfl-sim/blitz_db/week7_pit_defenders_no_qb_pressure_2026-10-25.md | 2026-10-23 | 17324 | # Week 7 — PIT @ NO (Stade de France, Sun Oct 25, 9:30 AM ET) — Steelers defenders + Saints QB vs blitz/pressure |
| /workspace/nfl-sim/blitz_db/week7_prop_ladder_2026-10-25.md | 2026-10-23 | 91070 | / game / player / status / market / alt below (prob, grade, price) / BASE (prob, grade, price) / alt above (prob, grade, price) / best rung  |
| /workspace/nfl-sim/blitz_db/week7_receiver_edge_board_2026-10-25.md | 2026-10-23 | 259505 | # Week 7 receiver / TE edge board — October 25, 2026 |
| /workspace/nfl-sim/blitz_db/week7_tightened_2026-10-25.md | 2026-10-23 | 108120 | / player / leg / last3 avg / season avg / trend / opp adj / model mean / P(threshold) / tier / gate / |
| /workspace/nfl-sim/notes/adkins_redzone_2026-10-15.md | 2026-10-22 | 5240 | # Nate Adkins (DEN TE) red-zone / TD usage — 2026-10-15 |
| /workspace/nfl-sim/notes/anytime_td_bigcrus_2026-10-18.md | 2026-10-22 | 1062 | # Anytime TD pricing: bigcrus four (paper only) |
| /workspace/nfl-sim/notes/bal_cle_henry_wr_2026-10-16.md | 2026-10-22 | 2421 | # BAL@CLE — Henry rushing & Ravens pass catchers (pulled 2026-10-16) |
| /workspace/nfl-sim/notes/bal_cle_routes_pressure_2026-10-16.md | 2026-10-22 | 2874 | # BAL @ CLE: Flowers/Andrews routes + CLE pressure (2026-10-16, ~5:30 PM ET) |
| /workspace/nfl-sim/notes/bal_cle_tendencies_2026-10-16.md | 2026-10-22 | 10318 | # BAL offense / CLE defense tendencies, 2026 Wk1-5 (nflverse pbp + FTN charting, file pulled through Wk5) |
| /workspace/nfl-sim/notes/bankroll_reconcile_2026-10-22.md | 2026-10-22 | 1833 | # Bankroll reconcile — 2026-10-22 |
| /workspace/nfl-sim/notes/ceedee_lamb_fri_ir_2026-10-16.md | 2026-10-22 | 2043 | # CeeDee Lamb — Friday injury designation (Week 6 DAL @ GB) |
| /workspace/nfl-sim/notes/conditions_2026-10-18.md | 2026-10-22 | 2342 | # Game conditions: Sun Oct 18, 2026 (Week 6), built Fri Oct 16 ~7:50 PM ET |
| /workspace/nfl-sim/notes/conditions_2026-10-19.md | 2026-10-22 | 775 | # Game conditions: Mon Oct 19, 2026 (MNF), built Sat Oct 17 ~7:50 PM ET |
| /workspace/nfl-sim/notes/conditions_2026-10-25.md | 2026-10-23 | 2510 | # Game conditions: Sun Oct 25, 2026 (Week 8), built Fri Oct 23 ~7:50 PM ET |
| /workspace/nfl-sim/notes/conditions_2026-10-26.md | 2026-10-24 | 771 | # Game conditions: Mon Oct 26, 2026 (MNF), built Sat Oct 24 ~7:45 PM ET |
| /workspace/nfl-sim/notes/coverage_study_sea_wk3_wk5.md | 2026-10-22 | 639 | # Coverage study (Oct 13, 2026): SEA vs WAS (Wk3) and SF (Wk5) |
| /workspace/nfl-sim/notes/data_feeds_rebuild_2026-10-22.md | 2026-10-22 | 5753 | # Data feeds rebuild plan: 2026-10-22 |
| /workspace/nfl-sim/notes/data_sources_2026-10-21.md | 2026-10-22 | 3377 | # NFL data source inventory, 2026-10-21 (ET) |
| /workspace/nfl-sim/notes/dvp_week6_2026.md | 2026-10-22 | 7184 | # Week 6 Defense vs Position — 2026/27 Season |
| /workspace/nfl-sim/notes/engram_usage_2026-10-15.md | 2026-10-22 | 2407 | # Evan Engram (DEN TE) usage, 2026 Wk1-5 (research only, nothing placed) |
| /workspace/nfl-sim/notes/fd_pricing_study_2026-10-21.md | 2026-10-22 | 2415 | # FanDuel NFL prop pricing study (black-box), 2026-10-21 ET |
| /workspace/nfl-sim/notes/gameday_board_2026-10-15.md | 2026-10-22 | 2329 | # NFL game-day board, Thu Oct 15 2026 (TNF SEA @ DEN, 8:15 PM ET), built 12:30 PM ET |
| /workspace/nfl-sim/notes/gameday_board_2026-10-18_1230.md | 2026-10-22 | 3064 | # NFL game-day board, Sun Oct 18 2026 (Week 6), built 12:30 PM ET by BetGuru. PAPER ONLY, nothing placed. |
| /workspace/nfl-sim/notes/gameday_status_2026-10-18.md | 2026-10-22 | 1080 | ## Phase 1 status rerun — Sun Oct 18, ~7:35 AM ET (BetGuru) |
| /workspace/nfl-sim/notes/gamegrid_vetting_2026-10-22.md | 2026-10-22 | 3878 | # GameGrid vetting (2026-10-22, public sources only) |
| /workspace/nfl-sim/notes/hist_hitrates_2026-10-18.md | 2026-10-22 | 7482 | # Historical hit rates: Sunday Oct 18, 2026 (Week 6) |
| /workspace/nfl-sim/notes/injury_impact_2026-10-18.md | 2026-10-22 | 11506 | # Sunday Oct 18, 2026 — NFL Week 6 injury impact report |
| /workspace/nfl-sim/notes/injury_report_2026-10-16.md | 2026-10-22 | 5035 | # NFL Week 6 final Friday injury designations, rechecked Fri Oct 16 2026 ~4:35 PM ET |
| /workspace/nfl-sim/notes/late_refresh_2026-10-18_1450.md | 2026-10-22 | 1731 | # Late-game post-inactives Pinnacle refresh, Sun Oct 18 2026, ~2:50 PM ET (Ghost6). PAPER ONLY, nothing placed. |
| /workspace/nfl-sim/notes/matchup_breakdown_BUF-LV_PIT-TB_2026-10-18.md | 2026-10-22 | 11356 | # Matchup breakdown: BUF @ LV (4:25 PM ET) and PIT @ TB (1:00 PM ET), Sun Oct 18 2026 (officially Week 6) |
| /workspace/nfl-sim/notes/matchup_db_gaps_2026-10-21.md | 2026-10-22 | 4984 | # Matchup database Phase 1 — gaps and interpretation |
| /workspace/nfl-sim/notes/new_checks_backtest_2026-10-19.md | 2026-10-22 | 9721 | # New slip checks: backtest on 2024–2025 FanDuel props (run Mon Oct 19, 2026, ET) |
| /workspace/nfl-sim/notes/nix_passing_profile_2026-10-15.md | 2026-10-22 | 7373 | # Bo Nix passing profile: TNF vs SEA (Thu Oct 15 2026). Nothing placed. |
| /workspace/nfl-sim/notes/nix_zone_rushing_2026-10-14.md | 2026-10-22 | 3819 | # Nix 20+ rush yds / SEA zone / DEN checkdowns — SEA@DEN Thu Oct 15 2026 (8:15 PM ET) |
| /workspace/nfl-sim/notes/overnight_2026-10-14.md | 2026-10-22 | 2028 | # Overnight NFL research — 2026-10-14 (changes only) |
| /workspace/nfl-sim/notes/overnight_2026-10-15.md | 2026-10-22 | 4625 | # Overnight NFL research — 2026-10-15 (changes only; written ~11:55 PM ET) |
| /workspace/nfl-sim/notes/overnight_2026-10-16.md | 2026-10-22 | 12738 | # Overnight NFL research — 2026-10-16 (changes only since overnight_2026-10-15 + practice_watch_2026-10-16; written ~12:05 AM ET Sat Oct 17) |
| /workspace/nfl-sim/notes/overnight_2026-10-17.md | 2026-10-22 | 10956 | # Overnight NFL research, 2026-10-17 (changes only; written ~12:05 AM ET Sun Oct 18) |
| /workspace/nfl-sim/notes/overnight_2026-10-18.md | 2026-10-22 | 6157 | # Overnight NFL research, 2026-10-18 (changes only; written ~11:55 PM ET Sun Oct 18) |
| /workspace/nfl-sim/notes/overnight_2026-10-19.md | 2026-10-22 | 5840 | # Overnight NFL research, 2026-10-19 (changes only; written ~12:05 AM ET Tue Oct 20) |
| /workspace/nfl-sim/notes/overnight_2026-10-21.md | 2026-10-22 | 5161 | # Overnight NFL research — Wed Oct 21, 2026 (run 11:48 PM ET) — for 9 AM huddle |
| /workspace/nfl-sim/notes/overnight_2026-10-22.md | 2026-10-22 | 4945 | # Overnight NFL research — Thu Oct 22, 2026 (run 11:50 PM ET) — for 9 AM huddle |
| /workspace/nfl-sim/notes/overnight_2026-10-23.md | 2026-10-23 | 5211 | # Overnight NFL research — Fri Oct 23, 2026 (run 11:50 PM ET) — for 9 AM huddle |
| /workspace/nfl-sim/notes/overnight_2026-10-24.md | 2026-10-24 | 3885 | # Overnight NFL research — Sat Oct 24, 2026 (run 11:55 PM ET) — for the Sunday huddle |
| /workspace/nfl-sim/notes/placed_slips_graded_2026-10-15.md | 2026-10-22 | 3533 | # Placed TNF slips graded: SEA @ DEN, Oct 15 2026 (graded 7:45 AM ET) |
| /workspace/nfl-sim/notes/practice_watch_2026-10-14.md | 2026-10-22 | 1270 | # Practice watch — Wed Oct 14, 2026 ~5:40 PM ET |
| /workspace/nfl-sim/notes/practice_watch_2026-10-15.md | 2026-10-22 | 4018 | # Practice watch — Thu Oct 15, 2026 ~5:45 PM ET |
| /workspace/nfl-sim/notes/practice_watch_2026-10-16.md | 2026-10-22 | 2110 | # Practice watch: Fri Oct 16, 2026 ~5:55 PM ET |
| /workspace/nfl-sim/notes/practice_watch_2026-10-17.md | 2026-10-22 | 1478 | # Practice watch: Sat Oct 17, 2026 ~5:50 PM ET |
| /workspace/nfl-sim/notes/practice_watch_2026-10-21.md | 2026-10-22 | 564 | # Practice watch 2026-10-21 (Wed, TNF final statuses + first Sunday reports) |
| /workspace/nfl-sim/notes/practice_watch_2026-10-22.md | 2026-10-22 | 565 | # Practice watch 2026-10-22 (Thu) |
| /workspace/nfl-sim/notes/practice_watch_2026-10-23.md | 2026-10-23 | 685 | # Practice watch 2026-10-23 (Fri, final reports) |
| /workspace/nfl-sim/notes/practice_watch_2026-10-24.md | 2026-10-24 | 723 | # Practice watch 2026-10-24 (Sat) |
| /workspace/nfl-sim/notes/questionable_history_2026-10-19.md | 2026-10-22 | 3861 | # Questionable history: Evans, Diggs, Kirk (built 2026-10-19 ~2:50 PM ET) |
| /workspace/nfl-sim/notes/route_personnel_sources_2026-10-21.md | 2026-10-22 | 3941 | # 2026 route / personnel data sources — 2026-10-21 |
| /workspace/nfl-sim/notes/rules_from_videos_2026-10-13.md | 2026-10-24 | 35467 | # Rules and lessons from the Oct 13, 2026 videos and discussion (DRAFT, compiled by BetGuru) |
| /workspace/nfl-sim/notes/sat_slip_check_2026-10-24.md | 2026-10-24 | 6121 | # Sat night slip check for Sun Oct 25 (run 2026-10-24 ~9:45 PM ET) |
| /workspace/nfl-sim/notes/sea_den_line_moves_2026-10-15.md | 2026-10-22 | 19103 | # SEA @ DEN (TNF, Thu Oct 15 2026, 8:15 PM ET): line moves |
| /workspace/nfl-sim/notes/sea_den_matchup_research_2026-10-15.md | 2026-10-22 | 6093 | # SEA @ DEN (TNF Oct 15 2026) – matchup research, 2026 Wks 1-5 |
| /workspace/nfl-sim/notes/slip_build_2026-10-17_1822.md | 2026-10-22 | 2844 | # Sunday Oct 18 slip build pass — Sat Oct 17 2026 ~6:25 PM ET (routine "NFL slip build"). Paper only, nothing placed. |
| /workspace/nfl-sim/notes/slip_build_2026-10-18_1830.md | 2026-10-22 | 1889 | # MNF slip build pass — Sun Oct 18 2026 ~6:30 PM ET (routine "NFL slip build"). Paper only, nothing placed. |
| /workspace/nfl-sim/notes/sunday_board_2026-10-18.md | 2026-10-22 | 3395 | # Sunday Oct 18 2026 NFL board vs Pinnacle (built Sat Oct 17 ~7:25 PM ET). PAPER ONLY, nothing placed. |
| /workspace/nfl-sim/notes/sunday_pins_2026-10-18.md | 2026-10-22 | 260 | # Sunday Oct 18 pins (user, 5:32 PM ET Fri) — recheck after 11:30 AM ET inactives; not placed |
| /workspace/nfl-sim/notes/sunday_recheck_2026-10-25.md | 2026-10-24 | 6159 | # Sunday Oct 25 recheck (Sat Oct 24, ~8:10 AM ET) |
| /workspace/nfl-sim/notes/sunday_slips_2026-10-18.md | 2026-10-22 | 2858 | # DRAFT Sunday slips — Oct 18, 2026 (Week 6) — NOT PLACED, NOT APPROVED |
| /workspace/nfl-sim/notes/sunday_slips_final_2026-10-18.md | 2026-10-22 | 5566 | # Sunday Week 6 final slips: 2026-10-18 (FanDuel pull 2026-10-16T20:47:37Z UTC) |
| /workspace/nfl-sim/notes/team_notes.md | 2026-10-24 | 44346 | ## BUF - James Cook fumbles (Oct 13, 2026, ESPN) |
| /workspace/nfl-sim/notes/tipster_summary.md | 2026-10-24 | 7418 | # Tipster summary: @MrBearBets + @GameGridAppp (one linked source) |
| /workspace/nfl-sim/notes/tnf_2026-10-22_receiving.md | 2026-10-22 | 6906 | # TNF Thu Oct 22, 2026: NE @ CHI (Soldier Field). Receiving half (BetGuru) |
| /workspace/nfl-sim/notes/tnf_backtest_pinnacle_2026-10-22.md | 2026-10-22 | 38263 | # TNF walk-forward backtest and Pinnacle — 2026-10-22 |
| /workspace/nfl-sim/notes/tnf_barner_wilson_alts_2026-10-14.md | 2026-10-22 | 5681 | # TNF SEA@DEN — Barner + Wilson alt ladders (Wed Oct 14 2026, 9:25 PM ET) |
| /workspace/nfl-sim/notes/tnf_build_pass_2026-10-14_1830.md | 2026-10-22 | 1101 | # TNF SEA@DEN build pass — Wed Oct 14 2026, ~6:30 PM ET (routine "NFL slip build"). v3 kept unchanged (freeze rule). |
| /workspace/nfl-sim/notes/tnf_denver_rerun_2026-10-15.md | 2026-10-22 | 6220 | # TNF SEA @ DEN: Denver rerun (Thu Oct 15 2026, 4:45 AM ET). Nothing placed. |
| /workspace/nfl-sim/notes/tnf_game_script_2026-10-15.md | 2026-10-22 | 25057 | # TNF SEA @ DEN: game-script build (Thu Oct 15 2026, ~5:10 AM ET). Nothing placed. |
| /workspace/nfl-sim/notes/tnf_jsn_backup_secondary_2026-10-14.md | 2026-10-22 | 1262 | # JSN vs DEN backup secondary — Wed Oct 14 6:05 PM ET (research note; slip unchanged = tnf_locked_v3) |
| /workspace/nfl-sim/notes/tnf_locked_2026-10-14.md | 2026-10-22 | 1961 | # TNF SEA@DEN LOCKED slips. Locked Wed Oct 14 2026, 10:20 AM ET |
| /workspace/nfl-sim/notes/tnf_locked_v2_2026-10-14.md | 2026-10-22 | 2397 | # TNF SEA@DEN locked v2. Wed Oct 14 2026, 10:30 AM ET |
| /workspace/nfl-sim/notes/tnf_locked_v3_2026-10-14.md | 2026-10-22 | 1667 | # TNF SEA@DEN locked v3. Wed Oct 14 2026, 5:15 PM ET (supersedes v2; v2 kept unchanged) |
| /workspace/nfl-sim/notes/tnf_locked_v4_2026-10-14.md | 2026-10-22 | 1627 | # TNF SEA@DEN locked v4. Wed Oct 14 2026, 6:55 PM ET (supersedes v3; v3 kept) |
| /workspace/nfl-sim/notes/tnf_locked_v5_2026-10-14.md | 2026-10-22 | 1500 | # TNF SEA@DEN locked v5. Wed Oct 14 2026, 9:20 PM ET (supersedes v4; v4 kept) |
| /workspace/nfl-sim/notes/tnf_matchups_2026-10-22.md | 2026-10-22 | 16491 | # NE @ CHI — October 22, 2026 matchup context |
| /workspace/nfl-sim/notes/tnf_projections_2026-10-22.md | 2026-10-22 | 42298 | # TNF NE @ CHI — 2026-10-22 injury-adjusted projections |
| /workspace/nfl-sim/notes/tnf_routes_2026-10-22.md | 2026-10-22 | 10362 | # NE / CHI routes and personnel — 2026-10-22 |
| /workspace/nfl-sim/notes/tnf_sea_den_predictions_2026-10-14.md | 2026-10-22 | 3496 | # TNF SEA @ DEN — Thu Oct 15 2026, 8:15 PM ET (Empower Field, outdoor) — built Wed Oct 14 ~9:30 AM ET |
| /workspace/nfl-sim/notes/tnf_tiers_2026-10-14.md | 2026-10-22 | 3058 | # TNF SEA@DEN tiers — Wed Oct 14 2026, 9:40 PM ET (nothing placed) |
| /workspace/nfl-sim/notes/tnf_tiers_v2_2026-10-14.md | 2026-10-22 | 3856 | # TNF SEA@DEN tiers v2 (built Wed Oct 14, ~10:00 AM ET) |
| /workspace/nfl-sim/notes/tnf_tiers_v3_2026-10-14.md | 2026-10-22 | 2504 | # TNF SEA@DEN tiers v3 (Wed Oct 14, ~10:15 AM ET). Replaces v2 Wilson legs and slips. |
| /workspace/nfl-sim/notes/tnf_wide_board_2026-10-15.md | 2026-10-22 | 4915 | # TNF SEA @ DEN wide board (Thu Oct 15 2026, kickoff 8:15 PM ET). Nothing placed. |
| /workspace/nfl-sim/notes/travel_history.md | 2026-10-23 | 2575 | # NFL travel history (international / long-haul spots) |
| /workspace/nfl-sim/notes/usage_wr_2026-10-25.md | 2026-10-24 | 1530 | # WR usage, 2026 Weeks 1-6 (pulled 2026-10-24 04:30 ET) |
| /workspace/nfl-sim/notes/waddle_sutton_vs_sea_cb_2026-10-15.md | 2026-10-22 | 5551 | # Waddle / Sutton vs Seattle CBs: TNF Oct 15 2026 (research only, nothing placed) |
| /workspace/nfl-sim/notes/was_sf_flags_2026-10-17.md | 2026-10-22 | 3759 | # WAS @ SF flag breakdown: MNF Mon Oct 19 2026, 8:15 PM ET, Levi's Stadium (outdoor). Paper only. |
| /workspace/nfl-sim/notes/week6_board_2026-10-15.md | 2026-10-22 | 3662 | # SEA @ DEN Week 6 board (TNF Oct 15 2026), FanDuel re-pull |
| /workspace/nfl-sim/notes/week6_matchup_scan.md | 2026-10-22 | 14757 | # Week 6 matchup scan: Sun Oct 18, 2026 (12 games; SEA-DEN was TNF) |
| /workspace/nfl-sim/notes/week6_tendencies.md | 2026-10-22 | 27000 | # Week 6 offensive tendencies (W1–5) |
| /workspace/nfl-sim/notes/film/README.md | 2026-10-22 | 899 | # NFL Film + NGS notes |
| /workspace/nfl-sim/notes/film/run_log.md | 2026-10-22 | 2106 | - 2026-10-14 01:30 ET / run 1 (bootstrap, W5 only) / games processed 15/15 + 2 byes (CAR, KC) / film complete 6 (SF@SEA, DEN@LAC, BUF@LA, DE |
| /workspace/nfl-sim/backtest/REPORT.md | 2026-10-22 | 8848 | # NFL model backtest, 2024 and 2025 seasons (Suave Bets) |
| /workspace/nfl-sim/backtest/alt_summary.md | 2026-10-22 | 4844 | # Alt-line backtest |
| /workspace/nfl-sim/backtest/summary.md | 2026-10-22 | 2584 | # Backtest (walk-forward, frozen-on-2024 parameters) |
| /workspace/nfl-sim/backtest/compare/REPORT.md | 2026-10-22 | 540 | # Outside-model comparison (2026-10-17) |
| /workspace/nfl-sim/backtest/features/README.md | 2026-10-22 | 937 | # Feature-enhanced props backtest (2026-10-17) |
| /workspace/nfl-sim/backtest/hist_props/SUMMARY.md | 2026-10-22 | 14540 | # FanDuel historical props backtest, 2024–2025 NFL regular season |
| /workspace/nfl-sim/backtest/hist_props/model_section.md | 2026-10-22 | 6531 | ## Model vs FanDuel closing prices (walk-forward) |
| /workspace/nfl-sim/backtest/hist_props_oddsapi/README.md | 2026-10-22 | 2701 | # Historical NFL player props — Odds API |
| /workspace/nfl-sim/backtest/new_checks_oct19/results.md | 2026-10-22 | 6418 | ## Check 1: play-count / time-of-possession projection |
| /workspace/nfl-sim/backtest/rerun/SUMMARY.md | 2026-10-22 | 14540 | # FanDuel historical props backtest, 2024–2025 NFL regular season |
| /workspace/nfl-sim/backtest/rerun/model_section.md | 2026-10-22 | 6531 | ## Model vs FanDuel closing prices (walk-forward) |
| /workspace/nfl-contest/ACCURACY_AUDIT.md | 2026-10-23 | 15378 | # Accuracy audit: NFL Sunday Oct 25, 2026 (Week 7) prop contest, final round-2 files |
| /workspace/nfl-contest/ApexTitan-part1.md | 2026-10-23 | 13394 | # ApexTitan – Part 1: Sunday Oct 25, 2026 (Week 7), early games (Paris 9:30 AM ET + all 1:00 PM ET) |
| /workspace/nfl-contest/ApexTitan-part2.md | 2026-10-23 | 15148 | # ApexTitan, Part 2: NFL Week 7 late games and SNF (Sun Oct 25, 2026) |
| /workspace/nfl-contest/ApexTitan.md | 2026-10-23 | 30249 | # ApexTitan — NFL Sunday Oct 25, 2026 edge plays |
| /workspace/nfl-contest/BetGuru.md | 2026-10-23 | 65265 | # BetGuru: NFL Sunday Oct 25, 2026 plus-edge plays (all 12 games) |
| /workspace/nfl-contest/ChatGPT_Bridge.md | 2026-10-23 | 108915 | # ChatGPT Bridge — Sunday, October 25, 2026 NFL props |
| /workspace/nfl-contest/College-DropOut.md | 2026-10-23 | 51034 | # College DropOut: NFL Sunday Oct 25, 2026, plus-edge player props |
| /workspace/nfl-contest/Einstein.md | 2026-10-23 | 40622 | # NFL Sunday Oct 25, 2026 (ESPN lists it as Week 7) - plus-edge player plays - Einstein |
| /workspace/nfl-contest/GHOST6_PROMPT.md | 2026-10-23 | 1390 | Contest entry for Ghost6 (speed matters). Today is Fri Oct 23, 2026. Research every NFL game this Sunday Oct 25, 2026 and write the best plu |
| /workspace/nfl-contest/Ghost6.md | 2026-10-23 | 113926 | # Ghost6 — NFL Sunday Oct 25, 2026 (Week 7) plus-edge player board |
| /workspace/nfl-contest/TopShotta.md | 2026-10-23 | 101233 | # TopShotta — NFL Week 7 Sunday (Oct 25, 2026) plus-edge player plays |
| /workspace/nfl-contest/coverage_check_2026-10-25.md | 2026-10-23 | 4774 | # Coverage check, Sun Oct 25 2026 legs (Einstein, analytics hub). Built Fri Oct 23, 9:55 PM ET |
| /workspace/nfl-contest/games_body.md | 2026-10-23 | 93770 | ## PIT @ NO — Sun Oct 25, 9:30 AM ET (early international window per Odds API commence time; venue NOT VERIFIED) |
| /workspace/nfl-contest/head.md | 2026-10-23 | 4807 | # TopShotta — NFL Week 7 Sunday (Oct 25, 2026) plus-edge player plays |
| /workspace/nfl-contest/history-buff.md | 2026-10-23 | 25166 | # NFL Sunday Oct 25, 2026 (Week 7): plus-edge player plays, all 12 games |
| /workspace/nfl-contest/mighty-duck.md | 2026-10-23 | 24235 | # NFL Sunday Oct 25, 2026 (Week 8): plus-edge player props across all 12 games. Worker: mighty-duck |
| /workspace/nfl-contest/new_sources_check_2026-10-24.md | 2026-10-24 | 4182 | # New data sources spot-check — 2026-10-24 (~8:00 AM ET) |
| /workspace/nfl-contest/FINISHES.txt | 2026-10-23 | 1101 | Einstein DONE msg 15:44 EDT (lines stamped 15:41, before restart) |
| /workspace/nfl-contest/RESTART.txt | 2026-10-23 | 24 | 2026-10-23 15:43:56 EDT |
| /workspace/nfl-contest/START.txt | 2026-10-23 | 24 | 2026-10-23 15:40:57 EDT |
| /workspace/nfl-contest/props.txt | 2026-10-23 | 6561 | ===== 401873017 |
| /workspace/nfl-contest/ts.txt | 2026-10-23 | 23 | 2026-10-23 03:50 PM ET |
| /workspace/nfl_engine/BACKTEST_REPORT.md | 2026-10-22 | 16687 | # Engine backtest on real 2026 data vs. our model |
| /workspace/nfl_engine/README.md | 2026-10-22 | 16669 | # NFL betting research engine — v1.0 |
| /workspace/nfl_engine/RESEARCH_AI_PROMPT.md | 2026-10-22 | 4636 | # Research instructions for an AI platform using this package |
| /workspace/nfl_engine/fit_context.py | 2026-10-22 | 4999 | #!/usr/bin/env python3 |
| /workspace/nfl_engine/live_scan.py | 2026-10-22 | 3048 | #!/usr/bin/env python3 |
| /workspace/nfl_engine/make_demo.py | 2026-10-22 | 3794 | """Synthetic fixtures ONLY. No current NFL players, lines, weather or betting advice.""" |
| /workspace/nfl_engine/matchups.py | 2026-10-22 | 5651 | #!/usr/bin/env python3 |
| /workspace/nfl_engine/nfl_sim.py | 2026-10-22 | 23317 | #!/usr/bin/env python3 |
| /workspace/nfl_engine/prepare.py | 2026-10-22 | 7573 | #!/usr/bin/env python3 |
| /workspace/nfl_engine/replay.py | 2026-10-22 | 1520 | #!/usr/bin/env python3 |
| /workspace/nfl_engine/research.py | 2026-10-22 | 9652 | #!/usr/bin/env python3 |
| /workspace/nfl_engine/validate.py | 2026-10-22 | 6036 | #!/usr/bin/env python3 |
| /workspace/nfl_engine/VERIFICATION.json | 2026-10-22 | 347 | { |
| /workspace/codex_nfl9.md | 2026-10-24 | 1904 | Work in /workspace/sb-grades (branch feat/pick-grades). Do NOT push, open PRs, publish. Never read/print secrets or env files. Commit locall |
| /workspace/nfl-archetypes-2025-2026.csv | 2026-10-22 | 66547 | gsis_id,full_name,position,team,games,games_2026,car,car_pg,car_share,inside_share,ypc,expl_rate,ngs_ryoe_per_att,ngs_rush_efficiency,ngs_8b |
| /workspace/nfl-coach-history.csv | 2026-10-22 | 135600 | coach,role,team,season,calls,neutral_pass_rate,early_down_pass_rate,third_short_run_rate,third_medium_pass_rate,neutral_sec_per_play,pa_rate |
| /workspace/nfl-coaching-2025-2026.csv | 2026-10-22 | 5381 | season,posteam,fourth_downs,go_rate,go_rate_4th_short,go_rate_short_midfield,pa_rate,motion_rate,no_huddle_rate,screen_rate,rpo_rate,head_co |
| /workspace/nfl-coaching-profiles-2026.csv | 2026-10-22 | 95081 | team,role,coach,caller_confidence,hc,oc,dc,seasons_calling_since_2015,history_teams,same_team_as_history,history_span,hist_z_neutral_pass_ra |
| /workspace/nfl-def-stickiness-2025-2026.csv | 2026-10-22 | 10012 | defteam,plays,run_look_rate,base_rate,nickel_dime_rate,box7plus_rate,light_box_rate,run_look_vs_11,run_look_vs_heavy,run_look_vs_runheavy_ga |
| /workspace/nfl-defender-archetypes-2025-2026.csv | 2026-10-22 | 172345 | gsis_id,name,team,group,espn_pos,pos,def_archetype,games,games26,def_snaps,ff,ints,pbu,qb_hits,rb_tackles,run_stops,run_tackles,sacks,tackle |
| /workspace/nfl-direction-splits-2025-2026.csv | 2026-10-22 | 132213 | side,kind,gsis_id,player,team,n,share_left,ypc_left,success_left,share_middle,ypc_middle,success_middle,share_right,ypc_right,success_right, |
| /workspace/nfl-game-script-2025-2026.csv | 2026-10-22 | 356 | bucket,games,pass_rate,rb_car,wr_tgt,te_tgt,plays,dropbacks |
| /workspace/nfl-injury-snaps-2025-2026.csv | 2026-10-22 | 255173 | season,team,game_id,role,leader,leader_out,wr_tgt_share,te_tgt_share,rb_tgt_share,top_other_wr_share,rb2_car_share,team_dropbacks,team_pass_ |
| /workspace/nfl-line-movement-2025-2026.csv | 2026-10-22 | 33951 | game_id,provider,home_spread_open,home_spread_close,home_ml_open,home_ml_close,total_open,total_close,result,total,spread_line,total_line,se |
| /workspace/nfl-ol-vs-rush-2025-2026.csv | 2026-10-22 | 8358 | season,team,dropbacks,sack_rate_allowed,hit_rate_allowed,pressure_rate_allowed_2025,ttt_2025,side,sack_rate,hit_rate,pressure_rate_2025 |
| /workspace/nfl-pace-2025-2026.csv | 2026-10-22 | 2707 | season,posteam,games,plays,plays_pg,neutral_pass_rate,proe,neutral_sec_per_play |
| /workspace/nfl-personnel-2025-2026.csv | 2026-10-22 | 62656 | row_type,season,team,grouping,plays,pass_rate,neutral_pass_rate,epa,epa_pass,epa_run,success,pa_rate,shotgun_rate,adot,deep_rate,tgt_share_W |
| /workspace/nfl-qb-target-tendency-2025-2026.csv | 2026-10-22 | 7088 | passer_player_id,qb,team,att,air,WR_tgt_share,WR_air_share,WR_adot,TE_tgt_share,TE_air_share,TE_adot,RB_tgt_share,RB_air_share,RB_adot,deep_ |
| /workspace/nfl-redzone-roles-2025-2026.csv | 2026-10-22 | 146279 | season,team,gsis_id,zone,stat,n,share,player,pos,season_tds |
| /workspace/nfl-referees-2025-2026.csv | 2026-10-22 | 826 | referee,games,pen_pg,pen_yds_pg,tot_resid,over_rate,pen_pg_shrunk |
| /workspace/nfl-rest-travel-2025-2026.csv | 2026-10-22 | 58971 | game_id,season,team,opp,home,rest,opp_rest,rest_diff,short_week,post_bye,thursday,west_early_east,travel_miles,margin,exp_margin,ats,neutral |
| /workspace/nfl-team-blitz-2025-2026.csv | 2026-10-22 | 24193 | defteam,season,dropbacks,games,blitz_rate,blitz_rate_pg_sd,blitz_rate_pg_min,blitz_rate_pg_max,avg_pass_rushers,rush5plus_rate,avg_blitzers_ |
| /workspace/nfl-weather-venue-2025-2026.csv | 2026-10-22 | 859 | wind_b,games,epa_db,total_pts,total_line,tot_resid,over_rate,fg_pct_40plus,table,temp_b,outdoor,surface,total |

_261 files indexed_

## Appendix B. BetGuru extra folders (counts)
- /workspace/nfl-sim/models: 13 entries
- /workspace/nfl-sim/scripts: 80 entries
- /workspace/nfl-sim/specs: 1 entries
- /workspace/nfl-sim/tests: 1 entries
- /workspace/nfl-sim/ens: 225 entries
- /workspace/nfl-sim/usage_sim: 42 entries
- /workspace/nfl-sim/notes/mc: 7 entries
- /workspace/nfl-sim/raw: 300 entries
- /workspace/nfl-sim/data: 140 entries
- /workspace/nfl-sim/hist: 7 entries
- /workspace/nfl-sim/matchup: 8 entries
- /workspace/nfl-sim/dossier: 8 entries
- /workspace/nfl-sim/clv: 1 entries
- /workspace/prices_1024: 48 entries
- /workspace/archetypes: 8 entries
- /workspace/suave-signup/data/nfl/raw: 23 entries
- /workspace/nfl-sim/backtest: 14 entries

## Appendix C. 32-team scheme table
| Team | HC | Off. caller (identity) | Def. caller (identity) | 2026 blitz rate | sack rate blitz/no | 2026 neutral pass rate / PROE |
|---|---|---|---|---|---|---|
| ARI | Mike LaFleur | Mike LaFleur: no strong persistent tendencies | Nick Rallis: 3-DL fronts high (hist z +1.6); pressure rate low (hist z -1.3); avg box low (hist z -1.2) | 23.4% | 13.8%/4.2% | 48.6% / -0.024 |
| ATL | Kevin Stefanski | Tommy Rees: 11 personnel low (hist z -1.2) | Jeff Ulbrich: 3-DL fronts high (hist z +1.3) | 23.0% | 4.7%/3.5% | 42.0% / -0.069 |
| BAL | Jesse Minter | Declan Doyle: neutral sec/play 36.3 in 2026 (z +2.3, new caller); middle-of-field target share 33% in 2026 (z +2.0, new caller); inside-10 run rate 73% in 2026 (z +1.7, new c | Anthony Weaver: 8+ box rate high (hist z +1.1); dime low (hist z -1.0) | 30.8% | 10.4%/1.8% | 44.7% / -0.054 |
| BUF | Joe Brady | Joe Brady: no strong persistent tendencies | Jim Leonhard: no strong persistent tendencies | 32.9% | 7.3%/5.4% | 53.9% / +0.017 |
| CAR | Dave Canales | Brad Idzik: inside-10 run rate 30% in 2026 (z -1.6, new caller); neutral sec/play 30.0 in 2026 (z -1.6, new caller); RB target share 11% in 2026 (z -1.6, new caller) | Ejiro Evero: pressure rate low (hist z -2.0) | 36.1% | 8.2%/2.8% | 60.2% / +0.083 |
| CHI | Ben Johnson | Ben Johnson: play-action rate high (hist z +1.9); 3rd-and-medium pass rate low (hist z -1.8); 12 personnel high (hist z +1.0) | Dennis Allen: man coverage rate high (hist z +1.2); 3-DL fronts low (hist z -1.1) | 39.7% | 6.5%/10.0% | 45.2% / -0.048 |
| CIN | Zac Taylor | Zac Taylor: neutral pass rate high (hist z +1.6); early-down pass rate high (hist z +1.5); play-action rate low (hist z -1.4); 3rd-and-medium pass rate high (hist z +1.2) | Al Golden: 5+ rusher rate low (hist z -1.6); blitz rate low (hist z -1.3); 3-DL fronts low (hist z -1.3) | 16.2% | 11.5%/8.2% | 63.4% / +0.089 |
| CLE | Todd Monken | Todd Monken: 11 personnel low (hist z -2.4); 21 personnel high (hist z +1.4) | Mike Rutenberg: no strong persistent tendencies | 24.4% | 12.8%/5.8% | 56.0% / +0.056 |
| DAL | Brian Schottenheimer | Brian Schottenheimer: 3rd-and-short run rate low (hist z -1.9); 3rd-and-medium pass rate high (hist z +1.3); neutral sec/play low (hist z -1.1); RB target share low (hist z -1.0) | Christian Parker: EPA/play allowed +0.19 in 2026 (z +2.1, new caller) | 26.9% | 2.9%/3.2% | 56.6% / +0.068 |
| DEN | Sean Payton | Davis Webb: middle-of-field target share 8% in 2026 (z -2.1, new caller); RB target share 28% in 2026 (z +2.0, new caller); aDOT 6.0 in 2026 (z -1.5, new caller) | Vance Joseph: man coverage rate high (hist z +1.3); 5+ rusher rate high (hist z +1.2); pressure rate high (hist z +1.1) | 39.4% | 3.3%/6.4% | 58.0% / +0.046 |
| DET | Dan Campbell | Drew Petzing: no strong persistent tendencies | Kelvin Sheppard: base package high (hist z +2.8); avg box high (hist z +2.3); 8+ box rate high (hist z +2.2); nickel low (hist z -2.1) | 31.2% | 8.3%/7.6% | 52.9% / +0.019 |
| GB | Matt LaFleur | Matt LaFleur: deep (20+) target rate high (hist z +1.4); early-down pass rate low (hist z -1.1); neutral sec/play high (hist z +1.0) | Jonathan Gannon: blitz rate low (hist z -1.6) | 39.7% | 12.5%/3.5% | 50.0% / -0.020 |
| HOU | DeMeco Ryans | Nick Caley: neutral sec/play low (hist z -1.4); 11 personnel high (hist z +1.3); 12 personnel low (hist z -1.2) | DeMeco Ryans: 3-DL fronts low (hist z -1.4); nickel high (hist z +1.1); blitz rate low (hist z -1.0) | 20.6% | 9.1%/8.7% | 52.4% / +0.010 |
| IND | Shane Steichen | Shane Steichen: inside-10 run rate high (hist z +1.1); 3rd-and-medium pass rate low (hist z -1.1); neutral sec/play low (hist z -1.1) | Lou Anarumo: 3-DL fronts low (hist z -1.2) | 20.4% | 6.5%/5.8% | 58.8% / +0.068 |
| JAX | Liam Coen | Liam Coen: 11 personnel high (hist z +1.0); 3rd-and-medium pass rate low (hist z -1.0); neutral pass rate high (hist z +1.0) | Anthony Campanile: no strong persistent tendencies | 26.3% | 12.2%/4.3% | 54.1% / -0.001 |
| KC | Andy Reid | Andy Reid: neutral pass rate high (hist z +1.7); early-down pass rate high (hist z +1.4); play-action rate low (hist z -1.3); TE target share high (hist z +1.2) | Steve Spagnuolo: blitz rate high (hist z +1.2) | 28.5% | 2.2%/2.6% | 55.1% / +0.056 |
| LA | Sean McVay | Sean McVay: play-action rate high (hist z +1.9); 13 personnel high (hist z +1.8); RB target share low (hist z -1.8); motion rate high (hist z +1.6) | Chris Shula: dime high (hist z +2.5); nickel low (hist z -1.9) | 32.4% | 4.4%/5.3% | 58.0% / +0.078 |
| LAC | Jim Harbaugh | Mike McDaniel: 21 personnel high (hist z +2.7); 11 personnel low (hist z -1.7) | Chris O'Leary: no strong persistent tendencies | 26.6% | 14.7%/5.3% | 40.7% / -0.099 |
| LV | Klint Kubiak | Klint Kubiak: 11 personnel low (hist z -1.6) | Rob Leonard: no strong persistent tendencies | 25.2% | 21.6%/3.6% | 54.9% / +0.035 |
| MIA | Jeff Hafley | Bobby Slowik: no strong persistent tendencies | Sean Duggan: no strong persistent tendencies | 29.0% | 0.0%/4.5% | 51.7% / -0.039 |
| MIN | Kevin O'Connell | Kevin O'Connell: inside-10 run rate low (hist z -1.8); red-zone pass rate high (hist z +1.5); 3rd-and-medium pass rate high (hist z +1.4); 3rd-and-short run rate low (hist z -1. | Brian Flores: blitz rate high (hist z +3.1); 5+ rusher rate high (hist z +2.9); man coverage rate low (hist z -1.8); nickel low (hist z -1.5) | 72.5% | 10.8%/9.5% | 44.1% / -0.095 |
| NE | Mike Vrabel | Josh McDaniels: 21 personnel high (hist z +1.3) | Zak Kuhr: no strong persistent tendencies | 37.1% | 9.6%/3.4% | 53.5% / +0.028 |
| NO | Kellen Moore | Kellen Moore: neutral sec/play low (hist z -1.7); inside-10 run rate high (hist z +1.2); 3rd-and-medium pass rate low (hist z -1.1) | Brandon Staley: no strong persistent tendencies | 34.1% | 4.3%/6.6% | 55.3% / +0.045 |
| NYG | John Harbaugh | Matt Nagy: no strong persistent tendencies | Dennard Wilson: no strong persistent tendencies | 33.6% | 4.2%/1.1% | 40.7% / -0.128 |
| NYJ | Aaron Glenn | Frank Reich: play-action rate low (hist z -1.5); 11 personnel high (hist z +1.2) | Brian Duker: no strong persistent tendencies | 37.1% | 7.5%/5.6% | 47.9% / -0.008 |
| PHI | Nick Sirianni | Sean Mannion: no strong persistent tendencies | Vic Fangio: man coverage rate high (hist z +1.5); nickel high (hist z +1.1); 5+ rusher rate low (hist z -1.1); avg box low (hist z -1.0) | 19.7% | 3.3%/2.5% | 45.5% / -0.074 |
| PIT | Mike McCarthy | Mike McCarthy: no strong persistent tendencies | Patrick Graham: no strong persistent tendencies | 28.5% | 2.7%/9.7% | 58.7% / +0.085 |
| SEA | Mike Macdonald | Brian Fleury: play-action rate 35% in 2026 (z +2.0, new caller); neutral sec/play 35.4 in 2026 (z +1.7, new caller) | Mike Macdonald: base package low (hist z -1.2); nickel high (hist z +1.0) | 21.5% | 9.4%/6.8% | 43.5% / -0.063 |
| SF | Kyle Shanahan | Kyle Shanahan: 21 personnel high (hist z +3.3); motion rate high (hist z +1.7); RB target share high (hist z +1.7); 11 personnel low (hist z -1.3) | Raheem Morris: avg box low (hist z -1.7); 8+ box rate low (hist z -1.1) | 31.2% | 4.2%/3.8% | 51.9% / +0.022 |
| TB | Todd Bowles | Zac Robinson: play-action rate low (hist z -1.1) | Todd Bowles: blitz rate high (hist z +1.6); avg box high (hist z +1.2); 8+ box rate high (hist z +1.2); 5+ rusher rate high (hist z +1.2) | 41.9% | 5.3%/3.8% | 45.5% / -0.061 |
| TEN | Robert Saleh | Brian Daboll: no strong persistent tendencies | Gus Bradley: blitz rate low (hist z -1.4); 3-DL fronts low (hist z -1.4); 5+ rusher rate low (hist z -1.2) | 22.1% | 7.1%/6.1% | 45.5% / -0.064 |
| WAS | Dan Quinn | David Blough: WR target share 72% in 2026 (z +1.9, new caller); deep (20+) target rate 20% in 2026 (z +1.8, new caller); neutral sec/play 30.1 in 2026 (z -1.5, new caller) | Daronte Jones: blitz rate 47% in 2026 (z +1.6, new caller) | 47.4% | 6.9%/2.5% | 46.9% / -0.045 |
