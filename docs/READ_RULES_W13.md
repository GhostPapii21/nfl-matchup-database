# Read rules for Week 13 on: targets first, defense-allowed profile, hourly weather grade (FLAGS ONLY)

refs NFL-56. Research only; `projection_ready` stays false. 0 Odds API credits. Approved by Rico Nov 26, 2026,
7:11 PM ET ("Yes, have Blitz add all three rules", card answered via Ghost6).

**Policy.** All three rules are flags. `pipeline/read_rules/__init__.py` sets `CUTS_ENABLED` False for each rule and
every entry point calls `assert_flags_only()`. `annotate_legs` only adds `rr_*` columns; it never drops a row or
changes an existing column (tested). A rule may become a cut only after the backtest below shows it beating the
rushing-under baseline (n >= 30 and a paired diff CI lower bound > 0) **and** Rico approves that change separately.
`pregame/` is not modified (it is only imported for stadium coordinates and kickoff time).

## Run it

```sh
python -m pipeline.read_rules --game 2026_13_JAX_CHI            # live NWS + Open-Meteo pull
python -m pipeline.read_rules --game 2026_13_JAX_CHI --offline  # no network: weather = unknown
```

Writes `pipeline/ledgers/read_rules/READ_RULES_<game>.md` and `.json`. The game-script run copies each item into its
checklist with status FLAG. Proposed skill text: [proposed_skill_changes/READ_RULES_SKILL_PATCH.md](proposed_skill_changes/READ_RULES_SKILL_PATCH.md).

## The rules as built

1. **Targets first** (`targets_first.py`). WR/TE receiving legs: share of team targets over the player's last 4
   prior games with a target or carry (needs 3; walk-forward). WR passes at >= 20%; TE passes as a top-two team
   target (ties count). A low-share player gets PASS_ROLE_EXCEPTION only when the opponent ranks top-10 in yards per
   game allowed to his role. Slot vs outside alignment has no free source, so a WR's exception is "unknown" and
   never passes him. RB receiving legs are NOT_APPLICABLE (the rule names WR/TE).
2. **Defense-allowed profile** (`defense_allowed.py`), both defenses in the game, weeks before the game only:
   - Sharp free coverage table (`data/coverage/sharp_coverage_2026.csv`): MOF closed/open, man/zone, with its
     `pulled_utc`. Season-to-date as of the pull, so not point-in-time for past weeks.
   - nflverse play-by-play: catches/yards allowed to TE, RB, WR (slot_WR and outside_WR are "unknown"; a
     pass_location proxy, middle vs left/right, is reported under its own clearly named fields); short (<10 air
     yards) / intermediate (10-19) / deep (20+) allowed; designed-run YPC allowed (no scrambles/kneels); DBs ranked by
     inferred catches/yards (first tackler on a completion, labelled `inferred_from_tackler`) with verified PBU, INT
     and DPI counts.
   - PFF free recap pages W1-8 (`data/pff_captures_w1_8`, no paid content): the one featured COVERAGE card per game
     (INT, PBU, receptions/targets). Sparse, reported as-is.
   - NGS (`data/ngs`, verified on main): no defender or alignment fields, so it adds nothing to this profile.
   Every figure is `{value, source, pulled_at}`; missing is "unknown", never 0.
3. **Hourly weather grade** (`weather_grade.py`). NWS gridpoint forecast (QPF, windSpeed, windGust; a multi-hour QPF
   period is spread evenly over its hours) and Open-Meteo hourly (precipitation in inches, wind and gusts in mph).
   For kickoff hour + 3: rain none (0) / light (>0 and <0.05 in/hr) / moderate (0.05-0.3) / heavy (>0.3), sustained
   and gust mph per source, side by side, `sources_disagree` when grades differ. Dome/closed = not graded. Failed pull =
   unknown. One run-tilt sentence per team (moderate+ rain, sustained >= 15 mph or gusts >= 25 mph = run-tilt up),
   with the team's prior rush rate vs league.

## Backtest vs the rushing-under baseline (0 credits, box/repo data only)

`SELECTIVE_EDGE_WORK=/tmp/read_rules_bt_work python3 -m calibration.selective_edge_run build` then
`python3 -m calibration.read_rules_backtest`. Full tables: [research/runs/2026-11-26_read_rules_flags/REPORT.md](../research/runs/2026-11-26_read_rules_flags/REPORT.md).
The rebuilt legs file matches the Phase 4 freeze sha256, and the baseline reproduces exactly: STRONG UNDER rushyds
W4-7 101 legs 60-41 (+6.2 pts [-4.0, +16.0]); W8-9 27 legs 21-6 (+24.8 [+7.2, +38.2]); W4-9 combined 128 legs 81-47,
63.3% vs 53.1% break-even, +10.1 [+1.2, +18.6], ROI +18.8%.

| rule | test (W4-9) | n | result | vs baseline |
|---|---|---|---|---|
| 1 targets first | WR/TE main unders, PASS | 349 | 56.5% vs 53.7% BE, +2.7 [-4.0, +9.7], ROI +5.1% | below baseline; CI includes 0 |
| 1 targets first | WR/TE main unders, FLAG_LOW_TARGET_SHARE | 544 | 46.7% vs 53.9%, -7.2 [-12.2, -2.3], ROI -14.0% | low-share players beat their UNDERS |
| 1 targets first | WR/TE alt overs, PASS rungs | 4,188 | 30.3% vs 35.8%, -5.6 [-9.5, -1.5], ROI -27.2% | passing the rule did not help overs |
| 1 targets first | as a filter on the baseline | - | not applicable (baseline is rushing legs) | - |
| 2 defense allowed | baseline vs NOT-soft run D (YPC rank > 10) | 93 | 62-31, +13.7 [+2.7, +24.1] | drop-soft filter: +3.5 [-1.8, +9.4]; W8-9 alone -1.7 |
| 2 defense allowed | baseline vs soft run D (top-10 YPC allowed) | 35 | 19-16, +0.7 [-15.6, +16.9] | insufficient sample |
| 3 weather (kickoff obs. proxy) | baseline in precip/wind>=15 games | 12 | 10-2, +30.5 | keep-only filter +20.4 [-6.7, +40.6], n=12: insufficient |
| 3 weather (Open-Meteo W6-8 saved) | baseline in windy games | 7 | 5-2, +19.1 | keep-only filter +6.2 [-17.9, +36.9], n=7: insufficient |

**Conclusion: no rule beats the baseline. All three stay flags.** Rule 2's "skip rushing unders against soft run
defenses" is the only direction worth watching (+3.5 pts, CI crosses 0, reverses in W8-9). Rule 1 did not
separate winners on this data. Rule 3's hourly rain-rate grade cannot be backtested: no saved hourly rain-rate
forecasts cover Weeks 4-9; both weather proxies are kickoff-window and too small.

## Known gaps
- Slot/outside alignment, coverage assignments and route data: no free source -> unknown.
- Play-by-play in the repo runs through Week 11 (`pbp_2026_w1_11_pulled_20261124T1717ET`); Week 12 is not in it yet.
- PFF captures cover W1-8 only, one featured coverage card per game.
- Sharp coverage is season-to-date, not point-in-time.
