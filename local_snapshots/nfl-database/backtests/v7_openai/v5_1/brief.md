# Task: improve our best model (v5) into v5.1 — pre-register, then code

## v5 method (locked commit c71af73, graded after)
- Reader: grok-4.7 (xAI), temp 0.3, JSON mode, one call per game, 88 games Weeks 3-8. Input = an AS-OF pack (all pre-kick): spread/total/implied team totals; for each team last-3-games rushers (carries/yds), targets (tgt/rec yds/air yds), QB EPA/dropback vs blitz vs no blitz; opponent season defense (YPC allowed, 10+ yd runs, 20+ yd pass plays, pass YPA by location, blitz rate); list of AVAILABLE PROPS (main lines + latest saved price, snapshot ~30 min pre-kick). No injury reports, weather, or inactives.
- System prompt = our "betting-game-brainstorm" skill, 12 steps: GAME line; SCRIPT (base + 2 flips); INJURY FALLOUT; MATCHUP (shell, pressure, where defense bleeds, target overlap); FORM; EDGE PLAYERS (max 2/game, only rushyds|recyds|rushrecyds, each with edge sentence, must_be_true, kills_it, confidence strong|lean|pass); DATA CHECK (verdict agree|flag; data disagreeing with a strong read => flag, not cut); MARKET+RUNG+PRICE; PRE-MORTEM; SLIP STORY. Reads validated, 11 re-prompts.
- Tags: SAVED_READ = Rico's own pregame chat reads (14 legs); RECONSTRUCTED = Grok legs; PRIMARY = SAVED_READ where available else RECONSTRUCTED (GROK_ON_SAVED_GAME excluded, comparison only).
- Post-read tags (NOT gates in PRIMARY): PRO_EDGE (offline: no-vig fair prob from betonlineag/consensus anchor, best saved price, lagging props; pe_pass), ZONE_MOF (opp zone rate/middle YPA; zone label is hindsight thru wk7).
- Grading: $10 flat/leg at saved main-line price; hit rate counts all settled legs, ROI only priced legs (40 of 186 unpriced). Slips <=5/week, 3-4 legs, 1 leg/game/slip, 1 leg/player, price = product of decimals.

## v5 results (PRIMARY)
- Train Wk3-6 49-63 (43.8%), ROI -13.8%; Holdout Wk7-8 31-20 (60.8%), priced 25-15 +17.2%.
- By week W-L: wk3 11-21, wk4 12-17, wk5 15-10, wk6 11-15, wk7 16-10, wk8 15-10.
- By market/side (all weeks, priced): recyds over 28-28 -6.3%; recyds under 4-5; rushrecyds over 6-3 +25%; rushrecyds under 3-3; rushyds over 21-15 +9.3%; rushyds under 3-8 -48.8%. ~75% of legs are overs.
- Slips: 4 of 29 won (wk5 1/5, wk7 1/5, wk8 2/4), +$145 (independent-product estimate).
- PRO_EDGE-pass subset: wk6 4-7, holdout 14-7 +25%. ZONE_MOF: similar to PRIMARY.
- Rush-under baseline (every main rushyds under): train 161-128 +4.3%; holdout 70-62 -0.6%.
- Context: v6 (LLM brainstorm + pro-edge, all books) Wk3-8 READS 66-90 42.3% -19.1%, slips 0/30; 9 Monte Carlo sim versions all Brier worse than market 0.2481. Your own earlier v7 (market-anchored ridge logit, FanDuel only, Wk5-8): 238-237 50.1%, -5.1%, Brier worse than market; FAIL.
## Leak audit (CLEAN, commit f80fe05): 33 prompt checks 0 leaks (PBP weeks < target, 0 quotes at/after kickoff); Grok's knowledge ends before 2025 (forced guesses coin-flip, 0 recalled legs); masked rerun (names/weeks hidden) on 16 holdout games 24-8 vs original 21-8. Caveat n=51, 95% CI ~47-74%.

## Hard constraint for v5.1 backtest
No new LLM reads can be run (budget/rate limits). v5.1 must be a DETERMINISTIC change applied on top of the LOCKED v5 reads, using only as-of data. Allowed: filters/gates, side or market rules, confidence/verdict/must_be_true use, re-pricing to the best saved book at the same line, price caps, staking, slip construction. Prompt/skill changes may be proposed but only for the forward test (Week 10+), listed separately.
Judgment priority: improvement on Weeks 3-6 (where v5 lost), Weeks 7-8 reported separately. You have only seen aggregate tables above, NOT per-pick outcomes; keep changes few and principled (each one justified a priori), because Weeks 3-6 are not a clean holdout for you.

## Files (script dir = v5_1/)
- `data/v5_reads.csv` (186 rows, NO outcomes): week,game,player,team,opp,market,side,line,price(American; NaN=unpriced),grok_ctx,confidence,verdict,why,tag,reason,zone_mof_keep,opp_zone_rate,zone_note,pe_script,pe_bestprice,pe_lag,pe_sleeper,pe_fair(no-vig fair prob for this side),pe_pass,pe_note,steps,gsis,game_id,split.
- `data/lines_noact.csv` (20,612 rows, NO outcomes): all saved main-line quotes Wk3-8, one row per (player,market,side,book): week,game_id,game,player,market,side,tier,line,price,book,snap,kickoff,gsis,team,opp,spread,total,implied_team_total,prior_games,prior_carry_share,prior_target_share,prior_yds_avg,opp_prior_allowance (prior_* use weeks<w only).
- `../data/player_games_2026.csv`: per player-game Wk1-8 (game_id,week,gsis,posteam,qb,car,rushyds,tgt,recyds,rushrecyds,team_plays,team_dropbacks,team_rushes). Contains outcomes: for week w use ONLY week<w rows; assert it.

## Deliver
A) PLAN (<=500 words): each change with its a-priori reason; pre-declared success criterion (primary: Weeks 3-6 vs v5 PRIMARY on same scoring; secondary Wk7-8); what stays identical to v5; forward Week 10+ shadow protocol (lock+sha256 picks pre-kick, ledger fields, min sample before judging, kill rule); prompt changes for forward only.
B) ```python block `v5_1.py` (<=150 lines, deterministic): reads the files, applies v5.1 to PRIMARY rows, writes `out/v5_1_picks.csv` with columns week,game,game_id,player,gsis,market,side,line,price,stake,reason_kept and `out/v5_1_slips.csv` (slip_id,week,leg rows keyed by gsis+market+side+line). Do NOT grade; our shared harness grades v5 and v5.1 identically. Also `--week W --reads FILE --lines FILE` mode for forward use that writes picks + sha256.
