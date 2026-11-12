# Player type definitions: working definitions, v1 (2026-10-29, data through Wk7)
Sources: fixes.sqlite fix_player_role (season/L3 shares, snap L3; denominators count only games the player played), fix_player_game_usage (last game), fix_qb_rushing; nflverse pbp 2026 REG wk1-7 (air_yards, pass_location, YAC, run_location, yardline); nflverse NGS season (aDOT, separation, cushion, YACOE, RYOE/att, 8+ box %). Injury: week8/injuries.json (ESPN 10/29 AM).
"Meaningful" means season or L3 target share ≥8%, OR carry share ≥15%, OR L3 snap share ≥40%. A player can hold several types. Each type requires ≥12 targets unless stated, and samples under 15 targets are flagged ⚠.
Shares use max(season, L3) for eligibility. The opportunity gate (below) uses L3 only.

## WR
- Volume/possession: target share ≥20% and (aDOT ≤10.5 or catch ≥66%). "Volume (target-share)" means share ≥20% but deeper or less efficient.
- Explosive/deep: aDOT ≥13, or 20+ air-yard target rate ≥25%, or (20+ yd catches ≥25% of catches and ≥6 catches).
- Slot vs Boundary are PROXIES only. Middle-of-field target share ≥35% counts as Slot proxy and ≤20% as Boundary proxy. True alignment is NOT available in these sources, so this is a gap.
- Screen/YAC: aDOT ≤6.5 and (YAC/rec ≥6 or NGS YACOE ≥+1).
- Red-zone target: ≥4 targets inside the 20 and ≥20% of team RZ targets.
- 3rd-down chain mover: ≥6 3rd-down targets and ≥22% of team 3rd-down targets.
- WR2/WR3 depth: share 10–20%. Rotational: <10%.
## TE
- TE-as-primary: top-2 in team target share (non-QB) and share ≥15%.
- Move/seam: aDOT ≥8 and middle share ≥40%.
- Blocking/inline: L3 snap ≥70% and L3 target share <12%. A separate flag, "Blocking usage spike (last game)", fires on ≥80% snaps with ≤2 targets in the last game (LaPorta Wk7). Route-participation rate is NOT available, so this is a gap.
- Red-zone TE: ≥3 RZ targets and ≥15% of team RZ targets. Check-down/blitz-beater: aDOT ≤6.
## RB
- Early-down lead back: carry share ≥40%. It becomes "between-tackles" when the run_location=middle share is ≥45%. Run tendency: inside ≥55%, outside ≤35%, otherwise balanced (needs ≥20 carries).
- Rush-receive: carry share ≥35% and (≥3 targets/g or target share ≥10%).
- Receiving/3rd-down back: carry share <35% and (target share ≥8% or ≥2.5 targets/g).
- Goal-line/RZ back: ≥3 carries inside the 10 and ≥40% of team inside-10 carries.
- Elite rusher: NGS RYOE/att ≥+0.5 and ≥12 carries/g. Committee: carry share 15–50%.
## QB
- Volume: ≥36 att/g high, ≤28 low. aDOT ≥8.5 aggressive, ≤6.5 short-area.
- Designed-run QB: ≥3 designed runs/g. Scrambler: scramble rate ≥6% of dropbacks.
## Type → defensive weakness (PHASE_SCRIPT rules)
Explosive/Boundary → outside YPT ≥10.5. Slot proxy → slot YPT ≥10.0 (working; PHASE_SCRIPT has no slot threshold). Volume → WR YPT ≥9.0, capped at +2–3%. TE-primary/Move → TE YPT ≥8.0, and ≤5.5 cuts yards. Rush-receive/Receiving RB → Sharp RB YPT ≥7.0 or a top-8 defense in RB receptions allowed per game. Early-down/Elite → run YPC >4.4 is a plus, ≤3.8 triggers suppression. Blitz ≥35% (working) boosts check-down TE, receiving RB and Screen/YAC, and cuts primary WR volume.
Does NOT apply: a blocking or secondary TE vs a soft TE defense, committee backs vs a soft run D without the carry share, and receiving-back legs for early-down-only backs.
## Opportunity gate (in MATCHUP_FIT)
WR L3 target share ≥18% (about 6+ targets), TE ≥15%, RB L3 carry share ≥50% for rushing, ≥3 targets/g for receiving. Out/IR/Doubtful players are excluded. Questionable players stay in, flagged (user rule: low alts or fade).
Caveat: L3 shares are per games played, so two backs can sum past 100% when one missed games (NYJ Hall/Allen).

# v2: USER PRIMARY LABELS (authoritative; the v1 types above are secondary). Working thresholds, per game played:
- RB POWER/VOLUME BACK: ≥14 carries/g, ≥65 rush yds/g, YPC ≥4.2. Tagged RYOE+ when NGS RYOE/att >0. Yards after contact and broken tackles are NOT in public free sources, so that part is a gap and RYOE stands in as the proxy.
- RB RUSH-RECEIVE BACK: ≥8 carries/g, ≥2.5 rec/g and ≥18 rec yds/g.
- TE-AS-RECEIVER: top-2 team target share (non-QB) and ≥45 rec yds/g.
- WR HIGH-VOLUME: ≥7 targets/g, ≥5 rec/g and ≥60 yds/g.
- WR EXPLOSIVE: ≥14.5 yds/rec, ≤4.5 rec/g, ≥8 catches, and (≥45 yds/g or ≥4 catches of 20+ yds).
- SAFETY VALVE (any position): ≥10 targets, aDOT ≤6.5, <45 yds/g, ≥1.5 rec/g, not a power back, and (≥15% of team 3rd-and-7+ targets, or ≥15% of team targets on QB-hit plays with ≥3 such targets). The nflverse qb_hit flag stands in for pressure because true pressure/blitz-by-play is not in free pbp, so it is labeled a proxy.
- Relies on run: YES = team rush share ≥45% of plays and a power back. lean = one of the two. no = neither.
Output: USER_LABELS.md, the "USER PRIMARY LABELS" section in each <TEAM>.md, and player_types.json (user_labels, team_run_reliance).
