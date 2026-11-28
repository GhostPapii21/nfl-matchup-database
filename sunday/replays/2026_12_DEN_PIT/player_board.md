# Player board 2026_12_DEN_PIT

Schema `sunday-player-board/1`. projection_ready=False. Research only.
As of: packet generated 2026-11-27T04:31:50+00:00; usage is the pregame window, weeks before 12.

## Models
- `pregame.metrics.offense_players` — ran. targets, carries, depth of target, red-zone counts, game logs
- `pregame.packet.snap_shares` — ran. offensive snap share over the packet window
- `pregame.packet.depth_chart` — ran. starter and second-string labels
- `pregame.packet.injuries_for` — ran. official report and ESPN availability
- `dashboard.opportunity._volume` — ran. gamma-Poisson target and carry draws, including the fitted volume correction
- `dashboard.opportunity.simulate_receiver` — ran. reception and receiving-yard draws
- `dashboard.opportunity.simulate_rusher` — ran. carry and rushing-yard draws
- `dashboard.opportunity.shrink` — ran. catch rate, yards per catch and yards per carry shrunk toward the league
- `dashboard.opportunity.def_factor` — ran. positional yards and catch rate versus this defense
- `dashboard.opportunity.script_multipliers` — ran. pass and rush attempt multipliers from the implied margin
- `dashboard.opportunity.teammate_out` — ran. OUT_TOP_SAME, OUT_REST_SAME, OUT_OTHER_GROUP, OUT_TOP_RB, OUT_REST_RB
- `research/projections_2026_w12/project.py QF` — not run. questionable snap factors for RB, TE and WR only
- `dashboard.extras.receiver_roles` — ran. existing role labels mapped onto the issue tags
- `dashboard.extras.opportunity_label` — ran. expanding, shrinking, volume-supported, efficiency-driven
- `pregame.packet.player_baselines` — not run. attached under separate_models; not an input to the draws
- `core.possession_engine_v0.opportunity.OpportunityRecorder` — not run. Snap-level role draws and red-zone event allocation. Not executed, so no TD probability is taken from it.
- `core.possession_engine_v0.joint_producer.OpportunityModel` — not run. Frozen usage-cell producer. Not executed.
- `core.period_engine_v0.monte_carlo` — not run. Team quarter-score engine. It does not project a player.

## Blocked for every player
- routes: no route column on this play-by-play; route participation was not imputed from snaps
- coverage_route_access: no coverage column on this play-by-play; team defender totals were not used as a player route adjustment

## DEN offense vs PIT
Team pass attempts 32.31, rush attempts 25.33. Script: APPLIED.

| Player | Pos | Depth | Snap | Targets | Share used | Tags | Receiving | Rushing | Warnings |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| J.Waddle | WR | starter | 0.555 | 0.191 | 0.165 | volume, shrinking | 31.2 yds (OK), 2.8 catches | — | — |
| C.Sutton | WR | second_string | 0.776 | 0.166 | 0.159 | red-zone | 30.3 yds (OK), 2.6 catches | — | role_change |
| E.Engram | TE | starter | 0.512 | 0.136 | 0.145 | expanding | 29.9 yds (OK), 2.9 catches | — | — |
| R.Harvey | RB | second_string | 0.366 | 0.102 | 0.145 | — | 28.5 yds (OK), 3.5 catches | 15.1 yds (OK), 4.3 carries | role_change |
| M.Mims | WR | unlisted | 0.249 | 0.077 | 0.08 | efficiency-dependent | 18.0 yds (OK), 1.5 catches | — | — |
| J.Coleman | RB | starter | 0.693 | 0.068 | 0.131 | red-zone, volume | 25.0 yds (OK), 3.2 catches | 51.0 yds (OK), 13.7 carries | — |
| T.Franklin | WR | unlisted | 0.482 | 0.06 | 0.074 | — | 15.5 yds (OK), 1.3 catches | — | — |
| P.Bryant | WR | unlisted | 0.573 | 0.06 | 0.101 | efficiency-dependent | 26.2 yds (OK), 2.0 catches | — | — |
| J.Dobbins | RB | second_string | 0.306 | 0.043 | — | shrinking | BLOCKED | BLOCKED | out |
| B.Nix | QB | starter | 0.998 | — | — | — | — | — | — |

Target column is the window target share. Receiving and rushing cells are engine means, or BLOCKED with the reason on the JSON row.

## PIT offense vs DEN
Team pass attempts 34.71, rush attempts 21.79. Script: APPLIED.

| Player | Pos | Depth | Snap | Targets | Share used | Tags | Receiving | Rushing | Warnings |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D.Metcalf | WR | starter | 0.884 | 0.207 | 0.173 | volume, explosive, shrinking | 36.6 yds (OK), 2.8 catches | — | — |
| G.Bernard | WR | unlisted | 0.772 | 0.177 | 0.164 | red-zone | 33.6 yds (OK), 3.3 catches | — | — |
| J.Warren | RB | starter | 0.719 | 0.132 | 0.113 | red-zone, shrinking | 25.9 yds (OK), 2.5 catches | 49.9 yds (OK), 9.4 carries | — |
| P.Freiermuth | TE | starter | 0.616 | 0.124 | 0.105 | — | 23.7 yds (OK), 2.3 catches | — | — |
| D.Washington | TE | second_string | 0.634 | 0.113 | 0.103 | — | 25.4 yds (OK), 2.2 catches | — | role_change |
| R.Wilson | WR | unlisted | 0.43 | 0.071 | 0.12 | explosive, efficiency-dependent | 28.7 yds (OK), 2.0 catches | — | — |
| R.Dowdle | RB | second_string | 0.398 | 0.064 | 0.106 | — | 19.9 yds (OK), 2.6 catches | 26.6 yds (OK), 6.1 carries | — |
| M.Pittman | WR | unlisted | 0.725 | 0.034 | 0.116 | — | BLOCKED | — | role_change |
| M.Hurleman | WR | unlisted | 0.31 | 0.026 | — | volume | — | — | — |
| L.Nichols | RB | second_string | 0.08 | — | 0.119 | efficiency-dependent | — | 11.9 yds (OK), 2.7 carries | — |
| T.Homer | RB | unlisted | — | — | — | — | — | — | snap_share_missing |
| A.Rodgers | QB | unlisted | 0.968 | — | — | — | — | — | practice |
| M.Rudolph | QB | starter | 0.087 | — | — | — | — | — | — |

Target column is the window target share. Receiving and rushing cells are engine means, or BLOCKED with the reason on the JSON row.

Baselines from `pregame.packet.player_baselines` are stored on each team under `separate_models` and are not the numbers above.
