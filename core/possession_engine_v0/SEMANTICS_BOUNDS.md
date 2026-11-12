# NFL-43 semantics bounds: penalties, returns, official overtime

Written 2026-11-12 (BetGuru). Engine: `core/possession_engine_v0` possession game-state path (`simulate.py` +
`semantics.py`), opt-in through `cfg["semantics"]`. Configs without that block are unchanged (legacy,
`LEGACY_UNSUPPORTED`). The frozen joint producer (`joint_producer.py`) still rejects penalties and return yards
as UNSUPPORTED; nothing here changes it. No model weights changed. Research only; `projection_ready=false`.

These are **descriptive sensitivity bounds**, not causal claims. The causal score impact of penalties in real
games is still `NOT_IDENTIFIED_FROM_DESCRIPTIVE_PBP`; what is bounded below is (a) how much of the game the
data says these events touch and (b) how much switching each path on moves the simulator's own outputs.

## 1. What is now SUPPORTED (and how)

| Semantics | Mode | Source | Rule implemented |
|---|---|---|---|
| Penalties (scrimmage) | `canonical_log_v1` | `data/redistributable/teams/penalty_plays_2026.csv` (canonical; 228/238 team-games match ESPN box totals) + `penalties_2026.csv` snaps; weeks strictly before target | Per-snap foul probability = offense's accepted offensive fouls/snap + defense's accepted defensive fouls/snap. Yards, no-play, auto-first-down resampled from that team-side's own accepted fouls. Half-distance rule. No-play fouls replay the down; live-ball fouls enforced after the play and dropped if the play changed possession or scored. Defensive foul with time expired -> one untimed down. Never scores, never changes possession. |
| Kick / punt return TDs | `asof_league_v1` | nflverse PBP, league, weeks < target | Kick-return TD and punt-return TD at the as-of league rate (W1-9 2026: 1/1,404 kickoffs, 1/1,033 punts). Field position after returns still comes from the empirical first-scrimmage spot (kickoffs) and punt **net** (punts). |
| Defensive returns | `asof_league_v1` | the sampled historical INT / fumble-lost row | `return_yards` moves the ball; `return_touchdown` (or reaching the goal line) scores 6 + try for the defense. End-zone turnovers without a return TD are touchbacks. |
| Overtime | `official_2025_regular_season` | NFL rule (2025 regular season) | 10-minute period, coin-toss receiver, both teams guaranteed a possession, then sudden death. Defensive score on the opening possession ends it. Clock expiry = tie. |

Punt net remains a separate PBP field-position quantity (`_punt_net_from_row`). Punt return yards are implied
(`kick_distance - net`) and never added a second time; a punt-return TD is a separate event.

## 2. Still UNSUPPORTED (rejected, not invented)

* Kick-play fouls (kickoff/punt/FG/try rows): excluded from the foul model. Exposure: 224 of 1,736 accepted
  flags (12.9%), 1,921 of 14,068 yards (13.7%) in W1-8. Their field-position effect is partly inside the
  empirical kickoff start spots and punt nets already.
* Declined / offsetting fouls (249 rows): no effect by definition; not simulated.
* Blocked punts/FGs, onside kicks, fake punts, 2-point tries after penalties: not modeled.
* Penalty-specific clock rules (10-second runoff, clock start/stop): a flat 4 s per no-play.
* Joint producer (player opportunity path): still raises UNSUPPORTED on penalties/return yards.
* Team-specific return-TD rates: league rate only (team samples are 0-1 events).

## 3. Descriptive exposure (canonical log, W1-8 2026, 119 games / 238 team-games)

| Quantity | Value |
|---|---|
| Accepted flags per team-game | 7.29 (59.1 yards); team-game yards p10/p50/p90 = 29 / 53 / 97 |
| Share no-play / auto-first-down | 72.8% / 20.0% |
| Flags that extended a drive / killed a drive (log columns) | 484 / 593 |
| League rows with a penalty (materiality_metrics.json, W1-8) | 8.3% of 21,191 rows |
| Mean kick return / punt return yards (nflverse W1-9) | 20.6 / 4.0 |
| Return TDs per game, league (kick+punt) | 2 in 136 games |
| Defensive return TDs, league W1-9 | 9 of 197 INTs, 6 of 157 fumbles lost |
| OT game rate W1-8 (materiality_metrics.json) | 9.1% (11/121) |

## 4. Simulator sensitivity (WAS @ NYG, as-of W1-9, n = 6,000 per arm, same seed 777)

| Arm | NYG pts | WAS pts | Total | NYG margin | P(NYG win) | P(tie) | P(OT) | flags/g | pen yds NYG/WAS |
|---|---|---|---|---|---|---|---|---|---|
| legacy (all UNSUPPORTED) | 13.00 | 21.92 | 34.92 | -8.92 | 0.222 | 0.009 | 0.033 | 0 | 0 / 0 |
| penalties only | 12.64 | 22.11 | 34.75 | -9.47 | 0.208 | 0.008 | 0.033 | 11.95 | 45.6 / 44.4 |
| returns only | 13.08 | 22.22 | 35.30 | -9.14 | 0.216 | 0.010 | 0.035 | 0 | 0 / 0 |
| official OT only | 13.02 | 22.03 | 35.05 | -9.01 | 0.220 | 0.012 | 0.033 | 0 | 0 / 0 |
| all NFL-43 paths | 12.47 | 22.10 | 34.57 | -9.64 | 0.204 | 0.010 | 0.033 | 11.97 | 45.1 / 44.7 |

Standard error of a mean total at n=6,000 is about 0.14 points; margin about 0.15. Bounds for this matchup:
penalties move the total by about -0.2 to -0.4 and the margin by about -0.4 to -0.7 points (NYG commits more
scrimmage fouls per snap, 5.9% vs WAS defense 3.1%); return TDs add about +0.1 to +0.4 to the total
(0.015 TDs/game); the OT rule changes P(tie) by ~+0.3 pp and barely moves means. Simulated flags per game
(~12, ~45 yards per team) sit below the league's 7.3 flags / 59 yards per team-game mostly because kick-play
fouls are excluded (12.9%) and the half-distance rule clips some yardage.

The engine's level problem is much larger than any of these effects: its WAS @ NYG total (~34.6) is ~6 points
under the four-book consensus (40.5-41.5) and its NYG win probability (~0.20) is ~35 pp below the no-vig
market (~0.55). That gap is a model problem (team-only empirical bootstrap, no QB/injury adjustment), not a
semantics problem, and is why `projection_ready` stays false.

## 5. Conservation tests

`core/possession_engine_v0/tests/test_nfl43_semantics.py` (21 tests): half-distance cases; 5,000 random
enforcements conserve yards, never score, never flip possession, stay in 1-99; canonical-log alias (WSH/LAR) and
as-of week filter; unknown team fails closed; zero rates never invent penalties or return TDs; OT (FG answered,
both TDs -> sudden death, second team takes lead, defensive score on opening possession, clock-expiry tie);
full-sim ledgers (scores == score_credit ledger, penalty yards == event deltas, punt net unchanged, return TDs
scored once); legacy configs still report UNSUPPORTED.

## 6. Review

These bounds need Ghost6's review (NFL-43 AC 4) before they count as accepted. The PR is the review; nothing
is merged by BetGuru.
