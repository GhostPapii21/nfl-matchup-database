# Postgame grading and historical learning: independent audit

Written by Ghost6, Friday Nov 27, 2026, evening (America/New_York). Research only. `projection_ready` stays false.
Nothing in this audit changes a model weight, formula, betting rule, `projection_ready`, a calibration or readiness
status field, a workflow, a secret, or a database. The only new files are this report and `tests/audits/postgame/`.

**Audited tree:** `main` at `ef4cc690` (merge of PR #146, 6:22:59 PM ET Nov 27). **Regression case:** DEN@PIT Week 12,
Fri Nov 27, 2026, ESPN `401873083`, final PIT 27, DEN 5, from PR #146 (commit `fbfde112`, "Week 12 DEN@PIT postgame
package (refs NFL-75)").

**How the audit was done:** read the code under `grading/`, `evaluation/readiness.py`, `snapshots/score.py`,
`calibration/backtest.py`, `calibration/opportunity_backtest.py`, `data/gamebooks/` and the weekly workflow (read only);
ran the existing grader on DEN@PIT offline against the committed ESPN final summary
(`runs/2026-11-27_DEN@PIT/pbp/summary_FINAL.json`), with output written to `/tmp` only; checked every finding with a test.
No network calls were made for grading, and no paid API was used.

Every number below comes from a committed file or a command that can be run again. Anything that could not be
checked says **unknown**.

---

## 1. Summary

| # | Question | Verdict | One line |
|---|---|---|---|
| 1 | Where official gamebooks and final stats enter | **Partial** | Final stats enter through nflverse play-by-play (`grading/sources.py`) or the ESPN summary (`grading/espn.py`). The official NFL game summaries in `data/gamebooks/` (Weeks 1–11, 179 games) are **not read by any grader**. DEN@PIT has no gamebook yet. |
| 2 | Props graded against the exact original projection and line | **Partial** | Packet props are graded against the newest packet generated before kickoff and its own book line, with source and pull time. For DEN@PIT that packet is byte-identical to the one hashed in the PR #141 lock. **Rico's slips and the PR #146 package are graded by hand in Markdown**; the grader cannot parse any of the 13 leg strings and never looks in `runs/`. |
| 3 | Zero-stat games and inactive players | **Partial** | A player in the box with no catches is a real 0 (Engram 0-for-2 tested). A player with no box line is `unknown`, which is safe but **cannot tell inactive from a name miss from a played-with-no-stats game**. A special-teams-only player is `unknown`. |
| 4 | Voids, DNPs, substitutions, limited appearances kept distinct | **No** | There is no void, DNP, inactive, substitution or snap-share field on a graded row. The ledger has `V` (void) but is empty. The gamebook lists that would separate them are already parsed and unused. |
| 5 | Original prediction timestamp and line preserved | **Mostly** | Every row carries the packet git sha, `generated_utc`, the line's pull time and source. Gaps: the packet's commit time is not checked, research artifacts record the latest commit time only, Rico's FanDuel prices exist only as screenshots and Markdown, and the DEN@PIT "closing line" is the bet quote itself (last saved quote 11:26 PM ET the night before). |
| 6 | Errors attributed to opportunity, efficiency, script, injury, coverage, assumptions | **No (in code)** | Graded rows carry one number, `error_actual_minus_projection`. Attribution exists only as prose in `POSTGAME_REVIEW.md`. |
| 7 | Postgame information leaking into pregame training | **No leak found in code paths; two guards missing** | Graded results feed only `evaluation/readiness.py` and `grading/scorecard.py`, not model fitting. The holdout uses earlier games only. But packet selection trusts the packet's own `generated_utc`, and research artifacts committed after kickoff are graded without a flag. |
| 8 | Walk-forward evaluation from historical results | **Partial** | Rows are ordered by `kickoff_utc` and the CLV holdout is walk-forward. Calibration backtests are walk-forward on already-seen Weeks 4–9. But readiness counts **1,067 "spots" that are only 288 distinct bets** (each book quote counted separately), 823 of 1,876 graded props have no side, and results are regraded and overwritten weekly with no version pin. |

---

## 2. The grading workflow as it exists today

### 2.1 Automated path (packet grading)

```
pregame/packets/<game>/packet.json  (committed many times before kickoff)
        │  grading/sources.py::packet_before_kickoff()    newest git version whose generated_utc < kickoff
        ▼
pre-kickoff packet ──► props: books.prop_check rows (player, stat, book, line, prices, baseline_minus_line)
                   ──► player baselines: matchup.*.player_baselines
                   ──► team samplers: team_projection.samplers.*
        │
        │  price snapshots: sources.packet_snapshots(), sources.line_history_snapshots(),
        │                   sources.freeze_data() (pregame/price_freezes/*_<AWAY>@<HOME>/freeze*.json, optional --freeze-ref)
        ▼
actual results ──► nflverse (sources.load_actuals → Actuals: games, pbp, weekly rosters, snap counts)  when final
               ──► else ESPN public summary (espn.load → ESPNActuals), saved under grading/results/sources/
        │
        │  grading/grade.py::grade_game()
        │     flagged_prop      side = sign(baseline_minus_line); result = core.prop_result(); CLV = core.clv()
        │                       vs core.closing_quote() (same book, latest snapshot before kickoff);
        │                       edge label = core.edge_decision() (model prob, volume_check, clv_record holdout)
        │     player_projection actual vs weighted mean; error_actual_minus_projection
        │     team_projection   points/total/margin error
        │     team_market       spread/total/moneyline result, CLV
        │  grading/research_runs.py::grade_research()
        │     research/runs/*_<AWAY>_<HOME>*/{legs.json, script_layer.json, *preview_result.json, grading_spec.json}
        │     snapshots/<game>/*/summary.json (locked 100k), pipeline/ledgers/<game>.sim100k.json
        ▼
grading/results/<game>.jsonl, .research.jsonl, .summary.json, .md     (grade.py::main --write)
        │
        ├─► evaluation/readiness.py::spots()   Rico's market rule (30+ spots, +3 pts, CI > 0, 4 weeks; weeks >= 10)
        ├─► grading/scorecard.py               season scorecard (reads dashboard boards by commit time)
        └─► grade.py::load_graded_rows()       CLV holdout for later games (core.clv_record: earlier kickoffs only)
```

Separately, `snapshots/score.py` scores locked 100k snapshots against the ESPN scoreboard (writes `SCORE.json`), and
`evaluation/protocol.py` aggregates those under the pristine protocol. DEN@PIT's lock has no `SCORE.json` on `main`;
scoring it is open work in PR #148.

**Schedule:** `.github/workflows/nfl-season-data.yml` runs Tuesdays about 7 AM ET (retries Wednesday). It fetches
gamebooks (`data/gamebooks/fetch_gamebooks.py`), scores snapshots, writes readiness, then regrades **every** packet game:
`for d in pregame/packets/2026_*/; do python -m grading.grade --game ... --write >/dev/null 2>&1 || true; done`.
Refusals and errors are discarded. DEN@PIT would first be graded automatically about Tue Dec 1, 7 AM ET, if nflverse
or ESPN is final for it by then.

### 2.2 Manual path (what PR #146 actually did)

PR #146 did not run `grading.grade`. Blitz built a run folder by hand:

| File | What it is | Machine-graded? |
|---|---|---|
| `runs/2026-11-27_DEN@PIT/pbp/summary_FINAL.json`, `plays_FINAL.csv`, `coreplays_FINAL.json` | ESPN final summary, PBP, core plays, pulled 6:06:58 PM ET by `pbp/poll_live.py` | Source data only |
| `RICO_SLIPS_LOCK.md` | Rico's three FanDuel slips, locked 2:58:25 PM ET, from screenshots | **No.** Prose list; no prices per leg, no JSON |
| `PREGAME_PROJECTION.md` | Restatement of the PR #141 lock, written 3:02:19 PM ET, **after** the scheduled kick (the review says so) | No |
| `POSTGAME_REVIEW.md` | Hand grades (HIT/MISS), team box, narrative attribution | No |
| `matchup_master_postgame_rows.csv`, `data/historical/projections/matchup_master_postgame_DEN_PIT.csv` | One-row postgame summary with leg verdicts as JSON text | No consumer found in code |
| `data/historical/playlogs/2026_wk12/DEN_PIT.csv` | 170-play log | No consumer found in code |

`grading/research_runs.py::run_dirs()` only scans `research/runs/*_<AWAY>_<HOME>*`, so nothing in `runs/` is ever
graded by code.

### 2.3 What the grader produces for DEN@PIT today (offline rerun, not committed)

Inputs: packet `git:aa60efa4…:pregame/packets/2026_12_DEN_PIT/packet.json` (`generated_utc` 11:31:50 PM ET Nov 26),
1,592 per-book freeze quotes from 6 freeze files, ESPN final summary from PR #146. Kickoff from ESPN: 3:00 PM ET.

| Kind | Rows | Result |
|---|---|---|
| flagged_prop | 221 | 34 win, 55 loss, **132 unknown** |
| player_projection | 37 | 29 with an actual, 8 unknown (J.Dobbins, R.Harvey, D.Washington) |
| team_projection | 8 | errors computed |
| team_market | 6 | 3 win, 3 loss |
| research (lock `20261127T111648Z`) | 5 | 4 team means, 1 win probability (PIT win p 0.4866, Brier 0.2636; total 40.22 vs 32, error −8.22; home margin −0.21 vs +22, error +22.21) |

Why 132 props are `unknown`: 121 have no side (116 `prop_check` rows carry no baseline, 5 have `baseline_minus_line`
exactly 0), and 36 have no actual (Marvin Mims ×14 and Michael Pittman ×11 are spelling misses; Darnell Washington ×11
has no box line and his status is in no committed source). These overlap. **CLV is unknown on all 221 props**: the
last saved DEN@PIT quote is 11:26:21 PM ET Nov 26, the same pull as the bet quote, about 15.5 hours before kick.

The box numbers the grader reads match `POSTGAME_REVIEW.md` for every leg checked (Coleman 15–26 and 8–46, Sutton
1–4 on 8 targets, Engram 0 on 2 targets, Freiermuth 1 catch, Warren 20–46 and 1 catch, Metcalf 36, Nix 169 on 40
attempts).

---

## 3. Findings by question

### Q1. Where official NFL gamebooks and final statistics enter

- **nflverse** (`grading/sources.py::fetch_nflverse`, `load_actuals`, `Actuals.stat`): games, play-by-play, weekly
  rosters, snap counts from the public release URLs, cached with URL, sha256 and pull time. Player stats are summed
  from PBP (no laterals). The README reports 223 of 224 values matched nflverse weekly stats on 2026_09_BUF_MIN.
- **ESPN public summary** (`grading/espn.py::find_event`, `fetch_summary`, `ESPNActuals`): used when nflverse is not
  final. The header and box score are saved with the sha256 of the full response. It refuses unless `STATUS_FINAL`
  and the teams match.
- **ESPN scoreboard** for locked-snapshot scoring (`snapshots/score.py::espn_final`). Its docstring says the
  cross-check against nflverse is still TODO.
- **Official NFL game summaries** (`data/gamebooks/`): PDFs, `pdftotext` text and parsed CSVs, Weeks 1–11 (16, 16, 16,
  16, 15, 14, 14, 14, 15, 14, 13 games). Includes `lineups.csv` (starters) and `participation.csv` (substitution,
  did_not_play, not_active). **No file under `grading/` mentions gamebooks** (tested). Week 12 is not fetched yet.
- **PR #146** used the ESPN summary and PBP pulled by its own live poller (`runs/…/pbp/poll_live.py`) and graded by hand.
- **ESPN injuries block:** the final summary carries Out / Coach's Decision entries (DEN: Ehlinger, Rapp, Ortega,
  Casey, Humphrey; PIT: Holcomb, Wetjen, Allar). `ESPNActuals` does not read it.

### Q2. Are props graded against the exact original pregame projection and line?

- **Packet props: yes, with one caveat.** `packet_before_kickoff` takes the newest packet whose `generated_utc` is
  before kickoff. Each row stores the line and price with the `#books` source and `books.retrieved_utc`. For DEN@PIT the
  packet chosen (`aa60efa4`) has sha256 `08a4ce43…e2d`, **identical to `inputs.packet_sha256` in the PR #141 LOCK.json**,
  and the lock's `price_freeze_pulled_utc` equals the packet's books pull (11:26:21 PM ET Nov 26). All 221 graded lines
  equal the packet's lines (tested). Caveat: "original" means the last pre-kickoff packet, not the packet that existed
  when a projection was first shown to Rico. If a packet is refreshed between the projection and kickoff, the grade
  uses the newer line.
- **Projection = research baseline**, not a model probability. `model_prob` is `unknown` on every row ("packet carries
  no model probability"), so no prop can ever pass edge condition 1 (as the README says).
- **Rico's slips: no.** The 13 leg strings in `RICO_SLIPS_LOCK.md` ("Jonah Coleman anytime TD", "Pat Freiermuth 2+
  receptions", "Jonah Coleman 70+ rush+rec yds", …) are not parseable by `research_runs.parse_leg()` (tested, 13 of 13
  return None). Anytime-TD and first-half-TD legs have no stat in `Actuals.STATS` or `ESPNActuals.STATS`. FanDuel
  prices per leg are not recorded anywhere machine-readable; only the slip odds (+483, +628 boosted, +7264) are in
  Markdown. The grades in `POSTGAME_REVIEW.md` (A/B 1-for-6, C 2-for-7) are hand grades. I spot-checked them against the
  ESPN box and they are consistent, but no code reproduces them.
- **PR #141 lock comparisons:** `PREGAME_PROJECTION.md` reports P(Under 51.5) 84.08%, Over 36.5 61.60%, PIT +4.5 63.08%
  from the locked `sim_arrays.npz`. The research grader grades only the lock's team means and home-win probability.
  The derived probabilities were computed at 3:02:19 PM ET, after kickoff, from pre-kickoff arrays. The arrays are
  pre-kick, but the choice of which thresholds to report was made after kick.

### Q3. Zero-stat games and inactive players

- **Correct:** a player who appears in the ESPN box with no catches is a real 0. Engram (0 receptions on 2 targets) is
  0, not unknown (tested). On the nflverse path, a player with offensive snaps but no touch is a real 0 (tested on a
  synthetic frame).
- **Correct and conservative:** a player absent from the box is `unknown`, never 0 (Dobbins, suspended; Allar,
  inactive; tested).
- **Gap:** `unknown` merges three different things: inactive or did not play (should be void), played with no stat
  (should be a real 0, so an Over loses), and a name-join miss. They share the reason text "0 ESPN box-score matches"
  (tested with Allar vs "Michael Pittman"). Darnell Washington (11 DEN@PIT prop rows) is the live example. He is not in
  the box or in ESPN's injury block, and his status is **unknown** from committed sources. The DEN@PIT gamebook would
  settle it.
- **Gap:** on the nflverse path `_played()` counts offensive snaps only. A special-teams-only player is `unknown`
  (tested). If the snap-count file is missing, a player who played with no touch is also `unknown` (tested).
- **Gap (names):** `resolve_full` compares `norm()` strings, which keep "jr", "ii", "iii". DEN@PIT has 25 prop rows lost
  this way ("Marvin Mims" ×14 vs box "Marvin Mims Jr."; "Michael Pittman" ×11 vs "Michael Pittman Jr."). Across all
  committed results, 101 prop rows have no name match. For 74 of them (39 with a side), the suffix-free name exists in
  the committed roster snapshot `data/historical/nflverse/roster_weekly_2026.parquet` (for example Luther Burden III,
  Chris Godwin Jr., Ollie Gordon II, Oronde Gadsden II). The other 27 are nicknames or truncations ("Amon" for
  Amon-Ra St. Brown, Zonovan vs Bam Knight, Kenneth vs Kenny Gainwell, Chigoziem vs Chig Okonkwo), which need an alias
  table. The Week 11 gamebook shows Z.Knight (ARZ) played as a substitution, yet his 6 rows were graded `unknown`.

### Q4. Voids, DNPs, substitutions and limited appearances

- Graded rows have no `settlement`, `participation`, `snap_share` or `void` field. `prop_result` returns only
  win/loss/push/unknown (`grading/core.py`).
- `grading/bets/LEDGER.csv` allows `V` (void) but has only a header row, no bets.
- The official game summaries already separate **started** (`lineups.csv`), **substitution**, **did_not_play** and
  **not_active** (`participation.csv`). The reference reader in `tests/audits/postgame/pg_audit_reference.py`
  classifies Week 11 ARI@KC correctly: T.McBride started, Z.Knight substitution, J.Aguilar did not play, C.Beck not
  active, K.Walker not active (tested). 65 of 17,633 printed name keys across Weeks 1–11 are ambiguous (two players
  share "J.Smith" on one team). The reader returns `unknown` for those and never guesses.
- **Limited appearances** (for example a player who left injured) cannot be identified from the gamebook. nflverse
  snap counts carry `offense_pct`, but the grader reads only `offense_snaps > 0`. The ESPN PBP has in-game injury
  notes (Heyward, McMillian, Franklin in DEN@PIT), which only the hand review uses.

### Q5. Is the original prediction timestamp and line preserved?

- **Packet rows: yes.** Source `git:<sha>:<path>`, `packet.generated_utc`, line and price `pulled_utc`, closing
  snapshot time and minutes before kick, `graded_utc`, `kickoff_utc`.
- **Gaps:**
  - The packet's own commit time is never checked or recorded. A packet committed after kickoff but stamped earlier
    would be accepted (tested in a throwaway repo). `grading/scorecard.py::pregame_board` uses commit time instead, so
    the two graders disagree on what "pre-kickoff" means.
  - Research artifacts record `git log -1` commit time (the **latest** change), and the working-tree content is
    graded, not the pre-kickoff blob.
  - Rico's lines exist only as three FanDuel screenshots (`runs/2026-11-27_DEN@PIT/rico_slips/*.png`, committed in
    PR #146) and Markdown. Per-leg prices and the screenshot time are not in any structured file.
  - For DEN@PIT no quote was saved after 11:26:21 PM ET Nov 26, so `closing_line` is the bet quote and CLV is unknown on
    every prop (tested). The README's T-60 to T-90 freeze did not happen for this game.
  - `--write` overwrites `grading/results/<game>.*` on every weekly run. The original grade survives only in git
    history.

### Q6. Error attribution

- Code: `grade_game` writes `error_actual_minus_projection` for player and team projections. No field splits the miss
  into opportunity (volume), efficiency (per-touch), game script, injury, coverage or assumption (tested: none of those
  words appear in `grading/grade.py`).
- Prose: `POSTGAME_REVIEW.md` attributes the DEN@PIT miss to an unmodeled QB change ("data_only on Rodgers-era
  Pittsburgh snaps"), weather logged but not applied, player outputs withheld, and turnovers (14 PIT points were
  defensive TDs). That is useful, but nothing turns it into data.
- `calibration/opportunity_backtest.py` (NFL-75 Phase 2) scores an opportunity model walk-forward on Weeks 4–9, which
  is the right building block for an opportunity/efficiency split, but it does not run on postgame rows.
- The reference `attribute_error()` shows an exact split: opportunity = (actual volume − projected volume) × projected
  rate; efficiency = actual stat − actual volume × projected rate; the two sum to the total error (tested).

### Q7. Does grading leak postgame information into pregame training?

- **No leak found along the code paths checked.** `grading/results` is read only by `evaluation/readiness.py`,
  `grading/scorecard.py` and the grader's own CLV holdout. No fitting code under `calibration/`, `core/` or `pregame/`
  reads it (grep). `core.clv_record` uses only games with an earlier kickoff and excludes the current game (tested).
  `core.closing_quote` ignores snapshots at or after kickoff (tested). CLV against the bet quote itself is `unknown`,
  not a fake tie (tested). Readiness drops prices pulled at or after kickoff.
- **Guards missing:**
  - G-07: packet selection trusts the packet's self-reported `generated_utc`.
  - G-08: research artifacts committed after kickoff are graded with no flag (tested: a `legs.json` committed 6 hours
    after kick grades as a win with no marker).
  - Postgame artifacts sit in folders named like inputs: `data/historical/projections/matchup_master_postgame_DEN_PIT.csv`
    and `data/historical/playlogs/2026_wk12/`. No code reads them today. A future loader that globs
    `data/historical/projections/*` would pick up outcomes. Pregame fitting filters history by week
    (`calibration/common.py`, "history weeks 1..w-1"), and the PR #141 lock pins its PBP by sha256, so this is a risk,
    not a leak.
  - Unverified: `calibration/selective_edge_roster.py` uses the nflverse weekly roster row with `week <= leg week`. If
    that row's status reflects game-day inactives, it is same-day information. **Unknown**; not tested here.

### Q8. Can historical results support walk-forward evaluation?

- **Yes, in part.** Every row has `kickoff_utc` and `game_id`. The CLV holdout is strictly earlier-games-only.
  `calibration/backtest.py` and `calibration/opportunity_backtest.py` are walk-forward (history weeks 1..w−1, Weeks 4–9,
  labelled "already-seen data"). The pristine protocol (`evaluation/PRISTINE_EVALUATION_PROTOCOL.md`) scores only locks
  made before kickoff, for Week 10 onward.
- **Gaps:**
  - G-11: `evaluation/readiness.py::spots` counts one spot per book row. On `main` that is **1,067 spots for 288
    distinct (game, market, side) bets**, about 3.7 quotes per bet. The bootstrap CI treats them as independent, so it
    is too narrow (current ALL row: −5.88 points, CI [−8.79, −2.88]). `clv_record` already dedupes; readiness does not.
  - G-05: 823 of 1,876 graded props (44%) have no side and therefore no result, so they contribute nothing to
    calibration even when the actual and the line are both known.
  - Weekly regrade-and-overwrite means a result can change when nflverse corrects a stat, and nothing pins which data
    version produced a given grade other than the sha256 in the summary.
  - Graded rows do not record the engine or packet-builder code commit. The packet sha is recorded, the code that built
    it is not.

---

## 4. Missing or incomplete components, ranked

Severity: **High** = can produce a wrong or unmeasurable grade today. **Medium** = loses data or weakens evaluation.
**Low** = hygiene.

| ID | Sev | Component | Evidence | Fix direction |
|---|---|---|---|---|
| G-11 | High | Readiness counts every book quote as an independent spot | `evaluation/readiness.py::spots`; 1,067 spots vs 288 distinct bets | One spot per (game, market_key, side), best-priced quote, like `core.clv_record`. Touches `evaluation/readiness.py` (also changed in open PR #134), so proposal only |
| G-03 | High | No participation source: inactive, DNP, played-with-0 and name miss all read `unknown` | `sources.Actuals._played`, `ESPNActuals.stat`; Darnell Washington ×11 rows | Read `data/gamebooks/.../parsed/{lineups,participation}.csv` (reference reader in tests) and add a `settlement` field: graded / void / unknown. Rico sets the void rule |
| G-02 | High | Rico's slips and run-folder legs are not machine-gradable | 13/13 leg strings unparsed; no TD stats; no per-leg prices | A `legs.json` (or `grading_spec.json`) per run with player, stat, side, line, book, price, quote time; add TD and first-half-TD stats from PBP |
| G-06 | High | No post-bet price snapshot, so CLV is unknown | DEN@PIT last quote 11:26:21 PM ET Nov 26 | Save a T-60 to T-90 freeze per game. Free sources only; no paid pulls |
| G-01 | Medium | PR #146 package lives in `runs/`, which the grader never scans | `research_runs.run_dirs` | Either write run packages under `research/runs/<date>_<AWAY>_<HOME>/` or extend discovery |
| G-04 | Medium | Name joins miss Jr./II/III and nicknames | DEN@PIT 25 rows; 74 of 101 unmatched rows across all results (39 with a side) | Suffix-insensitive fallback (patch in §6, tested), plus an alias table for nicknames |
| G-05 | Medium | Props without a baseline get no outcome | 121 of 221 DEN@PIT; 823 of 1,876 overall | Add a side-neutral `line_outcome` (over/under/push) whenever the actual and line are known |
| G-07 | Medium | Packet pre-kickoff check uses self-reported time only | `sources.packet_before_kickoff`; throwaway-repo test | Also require commit time before kickoff, or record it and flag |
| G-08 | Medium | Research artifacts graded from the working tree with no pre-kickoff check | `research_runs.grade_research`, `_commit_time` | Read the newest blob committed before kickoff; add `pre_kickoff` to each row |
| G-10 | Medium | No error attribution in data | `grade.py` writes one error number | Add opportunity/efficiency split from packet volume and rate fields (reference `attribute_error`); script/injury/coverage as tagged fields |
| G-09 | Medium | Special-teams-only and limited appearances undefined | `_played` uses `offense_snaps > 0` | Use gamebook participation; record `offense_pct` from snap counts |
| G-12 | Low | Weekly regrade hides refusals and errors | `nfl-season-data.yml`: `>/dev/null 2>&1 \|\| true` | Log refusals to the step summary. Workflow change, so Rico's call |
| G-13 | Low | Postgame outputs stored next to input folders | `data/historical/projections/matchup_master_postgame_DEN_PIT.csv` | Keep postgame artifacts under a `postgame/` or `grading/` path, or mark them in the manifest |
| G-14 | Low | Graded rows do not pin code version | rows carry packet sha, not builder/engine commit | Add the grader commit and packet-builder commit to the summary |
| G-15 | Low | Snapshot scorer final score not cross-checked with nflverse | `snapshots/score.py` docstring TODO | Cross-check once nflverse is final |

---

## 5. Test suite (`tests/audits/postgame/`)

New files only. They import grading code read-only, build git history in pytest's `tmp_path`, and write nothing inside
the repository.

| File | Tests | What it covers |
|---|---|---|
| `test_audit_pg_denpit_regression.py` | 45 | DEN@PIT final and box numbers, packet hash vs PR #141 lock, line provenance, CLV, side-less props, absent players, suffix misses, Rico's leg strings, `runs/` discovery, lock research grade |
| `test_audit_pg_leakage.py` | 12 | post-kick packet ignored, missing packet refused, packet commit-time gap, post-kick research artifact, closing-quote cut-off, self-CLV, holdout ordering, readiness spot counting |
| `test_audit_pg_participation.py` | 26 | gamebook participation classes, team-code mapping, settlement mapping, ambiguity, ST-only and no-snap-file cases, suffix-insensitive key, error split, no attribution fields today |

Run: `python3 -m pytest -q -p no:cacheprovider -rx tests/audits/postgame` → **77 passed, 6 xfailed** (Nov 27, 2026, on
this branch). `test_current_*` tests pin today's behaviour. The 6 `xfail(strict=True)` tests state proposed behaviour
(G-03, G-04, G-05, G-07, G-08, G-11). Each turns into a failure when its fix lands, which is the cue to remove the
marker. Tests that walk packet git history skip on a depth-1 checkout (checked on a depth-1 clone of this branch:
72 passed, 7 skipped, 4 xfailed). The folder is not added to
`scripts/test_offline.sh`; that would be a separate, reviewed change.

Existing suites are unchanged: the 13 invocations in `scripts/test_offline.sh` collect the same 1,402 tests before and
after these files, and `grading/tests` passes 63 of 63.

### Test proposals that cannot be written yet

1. **DEN@PIT gamebook participation:** once `data/gamebooks/2026/wk12/2026_12_DEN_PIT/` exists, assert Darnell
   Washington's status, Dobbins absent, Allar and Ehlinger `not_active`, and that the 11 Washington rows settle as graded
   (played) or void. Blocked on the Week 12 gamebook fetch (weekly workflow, Tuesday).
2. **nflverse vs ESPN parity for DEN@PIT:** once nflverse posts Week 12 PBP, grade both ways and require identical
   actuals for the 13 box values in the regression test (allowing documented lateral differences).
3. **Rico slip regrade:** once a machine-readable slip file exists (G-02), assert A/B 1-for-6 and C 2-for-7, and that
   the per-leg FanDuel price and quote time round-trip.
4. **CLV with a real close:** once a T-60/T-90 freeze exists for a game, assert CLV is known for every prop with a
   same-book quote, and that `minutes_before_kickoff` is between 60 and 90.
5. **Pristine scoring:** after PR #148 lands, assert DEN@PIT `SCORE.json` agrees with the research grade on total
   (32) and home margin (+22).
6. **Regrade stability:** run the grader twice on the same inputs and require identical rows except `graded_utc`.
7. **Roster-status look-ahead (Q7):** confirm whether nflverse weekly-roster `status` for week w reflects game-day
   inactives before `selective_edge_roster` may use the `week <= leg week` row.

---

## 6. Proposed corrections (not applied)

None of these were applied to existing files. Conflict check: I listed the files of open PRs #107, #113, #116, #119,
#120, #131, #132, #134–#140, #142–#145 and #148–#152. None touches `grading/sources.py`, `grading/espn.py`,
`grading/core.py`, `grading/grade.py` or `grading/research_runs.py`. #119, #131 and #132 add files under
`grading/results/` or `grading/backfill_w1_9/`. #134 edits `evaluation/readiness.py`, so G-11 is a proposal only.

### 6.1 G-04 suffix-insensitive name fallback (concrete, tested)

When the exact spelling has 0 matches, retry without Jr./Sr./II/III/IV/V, still requiring exactly one match on the
same team. Exact matches behave as before.

```diff
--- a/grading/sources.py
+++ b/grading/sources.py
@@ def norm(name: str) -> str:
     return re.sub(r"[^a-z]", "", str(name).lower())
 
 
+def name_key(full_name: str) -> str:
+    """Suffix-insensitive full-name key: 'Michael Pittman Jr.' and 'Michael Pittman' -> 'michaelpittman'."""
+    return norm(" ".join(t for t in str(full_name).replace("'", "").split() if t.lower() not in SUFFIXES))
+
+
 def abbrev(full_name: str) -> str:
@@ class Actuals: def resolve_full
         m = r[r.full_name.map(norm) == norm(full_name)]
         if team:
             m = m[m.team == team]
+        if len(m) == 0:   # exact spelling missed: retry without Jr./Sr./II/III/IV/V, still exactly one match or unknown
+            m = r[r.full_name.map(name_key) == name_key(full_name)]
+            if team:
+                m = m[m.team == team]
         if len(m) != 1:
--- a/grading/espn.py
+++ b/grading/espn.py
-from .sources import ROOT, UA, abbrev, norm, short_key
+from .sources import ROOT, UA, abbrev, name_key, norm, short_key
@@ class ESPNActuals:
     def resolve_full(self, full_name: str, team_: str | None = None) -> dict:
-        return self._match(lambda p: norm(p["name"]) == norm(full_name) and (not team_ or p["team"] == team_),
-                           f"'{full_name}' {team_ or ''}".strip())
+        what = f"'{full_name}' {team_ or ''}".strip()
+        hit = self._match(lambda p: norm(p["name"]) == norm(full_name) and (not team_ or p["team"] == team_), what)
+        if hit["reason"].startswith("0 "):   # exact spelling missed: retry without Jr./Sr./II/III/IV/V
+            hit = self._match(lambda p: name_key(p["name"]) == name_key(full_name) and (not team_ or p["team"] == team_), what)
+        return hit
```

Verified in a separate scratch worktree (not this branch): `grading/tests` still 63/63 passed. DEN@PIT props with a
known actual go from 185 to 210 of 221. The win/loss counts for DEN@PIT do not change, because the recovered "Michael
Pittman" and "Marvin Mims" rows have no baseline and so no side (G-05). As designed, the audit's G-04 xfail flips to
XPASS, and two `test_current_*` tests that pin the miss fail. Those markers would be updated in the same change.
Regrading earlier weeks would recover up to 39 side-bearing rows (upper bound; roster snapshot caveat in Q3).

### 6.2 G-07 packet commit-time guard (proposal)

In `packet_before_kickoff`, read `git log --format=%H %cI` and skip a version whose commit time is at or after
kickoff. Record `committed_utc` next to `generated_utc` in each row's `packet` block.

### 6.3 G-08 research artifacts as of kickoff (proposal)

In `grade_research`, read each artifact with `git show <sha>:<path>` from the newest commit before kickoff (the same
way packets are read), add `pre_kickoff: true|false` to every row, and keep post-kick artifacts out of summaries.

### 6.4 G-03 / G-09 participation and settlement (proposal; needs Rico's void rule)

Load the game's parsed gamebook with the reference reader (map nflverse ARI/BAL/CLE/HOU to printed ARZ/BLT/CLV/HST).
Add `participation` and `settlement` to prop rows: started or substitution → graded (a missing stat is a real 0);
did_not_play or not_active → void; not listed or no gamebook → unknown. Most US books void a player prop when the
player takes no snap; whether a special-teams snap counts is Rico's decision.

### 6.5 G-05 side-neutral outcome (proposal)

Add `line_outcome` = over / under / push whenever the actual and line are known, independent of `side`. This lets
side-less rows feed calibration (for example the hit rate of Overs by market) without inventing a pick.

### 6.6 G-11 readiness dedupe (proposal; overlaps open PR #134)

Before `market_table`, keep one spot per `(game_id, kind, market_key, side)`, choosing the lowest break-even quote,
matching `core.clv_record`.

---

## 7. Limits of this audit

- The nflverse path for DEN@PIT was not run (Week 12 nflverse PBP not checked; no download made). The regression uses
  the ESPN final summary committed in PR #146.
- The suffix analysis for earlier weeks uses the committed roster snapshot, which covers 2026 Weeks 1–5. Rows marked
  recoverable are an upper bound.
- Rico's three slip screenshots (`runs/2026-11-27_DEN@PIT/rico_slips/`) were not OCR'd or re-read for this audit; the
  leg text is taken from `RICO_SLIPS_LOCK.md`.
- Darnell Washington's DEN@PIT status is **unknown** from committed sources.
- The leak review is by code path and grep, not a full data-lineage trace of every research script under `research/`.
