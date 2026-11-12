# Code notes for Ghost6, Nov 3 2026 (Blitz): TEAM DATABASE

No held files were edited (run_gate.py, assemble.py, rico*_rules.py, press_tier.py, rules/rulebook.py, sims, tools/*). The builders sit outside tools/, so door code_hash doesn't change.

## What the door loads (no rulebook change needed)
- TEAM_FILES path `teams/{team}.json` now exists for all 32 teams (repo codes: LAR, WSH). Checked: `door.team_files([...])` returns no failures.
- JSON keys: team, built_at, builder, season, weeks_covered, games, sources,
  defense{games, sharp_thru_wk7_2026_10_29, by_receiver_type, by_receiver_type_last4, by_air_depth, by_depth_direction, by_receiver_archetype,
          explosives_pass20_by_pos, explosives_pass20_by_depth_dir, explosives_rush15_by_pos, rush_allowed_by_pos, beaten_by, holds, weekly, defenders, defender_label},
  offense{current_qb, current_qb_id, qb_games_last4, last4_team_games, qb_target_order_last4, deep_20plus_air_season, never_looked_at,
          backfield_last4{carries, rb_carry_share}, run_pass_by_score_season, run_pass_by_score_last4, neutral_early_down_pass_rate, q4_lead8_pass_rate}
- So the rulebook comment's "update when notes land" can be closed out as-is. The path is unchanged, and any edit is Rico's call.

## Human-readable + flat files
- teams/defense/<TEAM>.md, teams/offense/<TEAM>.md (32 each)
- teams/defense/defense_db.csv: team, defender, short, gsis_id, pos, scope(season|game), week, game, games, tags, rec, yds, ypt, td, exp20, pbu, ints, dpi, tags_pg, yds_pg, def_snap_pct, receivers, explosives, method
- teams/offense/offense_db.csv: team, section(qb_target_order_last4|deep_20plus_air_season|never_looked_at_last4|backfield_last4|run_pass_by_score_season), qb, player, gsis_id, pos, rank, games, tgt, share, rec, yds, deep_tgt, aDOT, by_week, snap_pct, carries, carry_share, flag
- Suggested assemble.py wiring (for Ghost6, not done): N2 verified-defender check → defense_db.csv scope=season by defender name + team. N1 60% carry share → offense.backfield_last4.rb_carry_share. Depth-receiver 5% target rule → offense.qb_target_order_last4[].share. Scheme check → defense.sharp_* + beaten_by.

## Caveats
- Defender numbers are a TACKLER/PBU TAG, NOT TRUE COVERAGE (first defensive tackler on a catch, PBU on an incompletion, interceptor, DPI player). TD and out-of-bounds catches are unattributed (the share is in weekly.unattributed_share).
- Man/zone/MOF/blitz come only from Sharp Football Analysis (thru wk7, dateModified 2026-10-29). nflverse FTN has no coverage and there's no 2026 participation file.
- WR1/WR2/WR3+ = the offense's season target rank at the position, so injured stars can show as WR3+ (e.g. McLaurin).
- CHI@SEA (Nov 2) is Week 8 in nflverse (2026_08_CHI_SEA), but its repo play log is playlogs/2026_wk9/CHI_SEA.csv (left as is).
- Rebuild: `python3 teams/build_team_db.py` (about 40s). Refresh sources/nflverse/pbp_2026.csv.gz first (public nflverse-data release).

## Backfill
- `python3 playlogs/tools/backfill_pbp_wk1_8.py` wrote 107 play logs (wk1-6 all, wk7 all but DAL_PHI, wk8 CAR_GB) in the wk8 column format plus extras (week, play_id, air_yards, td, down, ydstogo, score_diff, pbu, int_by).
- Ledger backup: defender_ledger.csv.pre_teamdb_backfill.bak (722 rows). Appended 4,970 rows for 105 games, so the ledger now covers all 121 played games. `tools/ledger_coverage_check.py` → OK.

---
# Code notes for Ghost6, Nov 3 2026 ~8:18 AM ET (Blitz): MNF CHI@SEA postmortem
EDIT HOLD respected. None of these are coded; they are for Ghost6's build. Evidence is in backtests/mnf_chi_sea_replay_2026-11-03/ and postmortems/2026-11-03_MNF_CHI_SEA.md.

## Already covered by the build (no action)
- (a, ledger part) The door runs ledger_coverage_check.py as the LEDGER rule. It is OK today, and CHI@SEA has 41 ledger rows.
- (b) Mirror overs: rico4_rules.mirror_eligible() covers any non-stop reason, and assemble.mirrors() builds them.
- (c) Shrink: press_tier.py and rico4_rules.py both say "no shrink / NOSHRINK" and nothing is left that shrinks.
- (g) sim_v6_fix: deprecated (DEPRECATED.md, commit 6322cc5). tools/sim_v6.py is the only source.

## Not covered
1. **(a) assemble does not write the depth-rule fields.** runs/2026-11-05_shared_src/assemble.py never writes `depth` (script_pass, target_share, defender_giving, rung) or `te_rank`. Any assembled #3/#4 WR or TE2 over therefore fails DEPTH_RECEIVER for missing fields. That fails closed, which is safe, but Rico's Nov 3 depth loosening can't produce a live leg until those fields are written.
2. **(h) The depth rule fails open when ranks are missing.** depth_rule.is_depth() treats `wr_rank=None` (assemble sets None when the rank isn't found) and a missing `te_rank` (it defaults to 1) as "not a depth receiver". Those legs skip all depth checks. Proposed: treat a missing rank on WR/TE overs as a fail ("rank unknown").
3. **(h) target_share window isn't checked.** The rule says 5%+ of targets over the last 4 games with the current QB. The code only checks `share >= .05` plus a source string. The MNF harness had Raymond at 7% while Caleb's actual last-4 share was 6.3% (it passes either way). Proposed: compute the share from pbp in assemble using the same last-4/current-QB window as rico4.target_share_pool.
4. **(h) defender_giving vs zone teams.** Raymond's depth legs were blocked on one mapped CB: Pritchett allowed 4.22 ypt against a league CB average of 8.80, on 13 snaps (19%). SEA plays about 90% zone. Rico's wording allows "defender **or coverage**". Proposed: let defender_giving use a coverage-level allowance (opponent's allowed YPT/targets to slot and middle-of-field receivers, from pbp pass_location=middle) when the opponent is 75%+ zone.
5. **Passing-yards ban (Rico Nov 3 6:17 AM ET) isn't coded** in door.py or rules/rulebook.py. In the replay, Darnold O238.5 and Caleb O224.5 were still built and graded. They were filtered only by hand. Proposed: a door rule NO_PASS_YDS (regex `passyds|passing yards`, covering overs, unders and alts).
6. **§14 cushion: price-dependent inconsistency.** JSN recyds O99.5 at -113 was BLOCKED by §14 (needed a 124.4 median, had 118), and it hit (118). JSN O109.5 [high] at +124 PASSED because §14 only applies at -113 or shorter. So the gate allows a harder rung on the same player and blocks the easier one. This needs a Rico decision: either apply §14 to every rung of a player, or make §14 a flag when SCHEME_EDGE is all four. (JSN O99.5 was all four, and it was the leg that cost the most.)
7. **Target-share sanity check for MODEL-SUSPECT receivers.** Loveland had a 30.2% Caleb share and a sim median of 25.3 yds against a 42.5 line. share × team attempts (about 33) × YPT (about 7) is about 70 yds. Burden and Odunze show the same pattern. All their overs had negative edge at every FanDuel rung, so the fixed rules (no shrink, mirror overs, SCHEME_EDGE) did not catch any of them. Proposed: when the sim median is below 0.6× the share-implied median, mark the leg MODEL-SUSPECT, and send the mirror over to MANUAL_REVIEW instead of an edge cut.
8. **SCHEME_EDGE auto-matchup picked the wrong CB for Kupp.** It mapped Stevenson at 11.5 ypt, which raised 7 SCHEME_EDGE alerts on Kupp overs. All of those lost (Kupp went 1-7), and the depth rule blocked them. Kupp's targets drew J. Johnson (DPI) and Phillips (holding). The matchup field should come from the slot/primary-coverage chart, not WR rank → CB rank.
9. **Leftover wording:** the assemble.py line 365 comment still says "edge-shrink", and the variable `shr=avg` is still in place. Cosmetic only.
