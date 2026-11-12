# NFL Custom Phase Script — Full Model (Updated Oct 29, 2026)
<!-- Permanent projection model, stored verbatim from the user on Oct 29, 2026. Supersedes the Oct 27 version. Rico's data-collection phases 1-8 live in MASTER_PROMPT.md. -->

## CORE PIPELINE
1. Identify locked roles for both teams
2. Pull defensive coverage profile (YPT by position/route, Outside YPT, blitz %, RZ TD%, run YPC allowed)
3. Grade each player by role vs opponent defense
4. Apply triggers (blitz volume cut, run suppression ≤3.8 YPC, soft matchup boost, injury boost)
5. Recent environment match (did player hit high numbers in similar defensive profiles this season / 2025)
6. Generate base projections
7. Run through three-model consensus (Monte Carlo 10k + Bayesian + Game Randomness) → true median
8. Pull FanDuel or DraftKings main line (and relevant alts)
9. Compare model MAIN/Median to the line → call Over / Under / Alt / No Bet
10. Output projection sheet with percentile labels and betting lean

## ROLE CATEGORIES (Locked Guidelines)
- **Rush-Receive Back**: Significant receiving volume + rush production (e.g. McCaffrey, Kyren when targeted, Stevenson, Josh Jacobs when involved)
- **Goal-Line / RZ Back**: Primary red-zone / goal-line carries
- **Elite Rusher**: High YPC or volume; soft run D (>4.4 YPC) = Positive grade
- **Volume Receiver**: High target share, steady receptions (boost capped +2–3%)
- **Explosive Receiver**: Big plays, deep/outside routes; grade primarily off Outside YPT
- **TE-as-Primary**: Tight end used as the main receiving option (e.g. McBride, Kittle, Bowers)
- **WR2 / WR3 / Check-Down**: Secondary options; lower volume expectations
- **Blitz Check-Down**: Primary target when defense blitzes (often RB or TE)

## DEFENSIVE PROFILE RULES
- Soft Outside YPT (≥10.5) → Positive for Explosive / Boundary receivers
- Soft WR YPT (≥9.0) → Slight Positive for Volume receivers (capped)
- Soft TE YPT (≥8.0) → Positive for TE-as-Primary
- Soft RB receiving YPT → Positive for Rush-Receive backs
- Hard TE YPT (≤5.5) → Cut yards on TE-as-Primary (volume may still hold)
- Run YPC allowed ≤3.8 → Run Suppression trigger (cut rush yards)
- Run YPC allowed >4.4 → Positive for Elite Rushers
- High blitz rate → Volume cut on primary receivers; boost check-down roles

## PERCENTILE STRUCTURE (Projection Sheet Labels)
- Floor (5th percentile)
- Slight Edge (10th)
- MAIN (15th) — primary betting number
- Edge (20th)
- Pure Edge (25th)
- Median (three-model consensus)

## BETTING LINE PROCESS (New — Oct 27 / Updated Oct 29)
1. After three-model true median is set, pull FanDuel or DraftKings main line for the prop.
2. Compare model number to the available line.
3. If model is clearly under the line, consider lower alt lines (e.g. if main is 75.5 and model sees under 65, check 60.5 or 55.5 alts for better price).
4. Call the side only when there is separation. If price is poor or line is already close, mark No Bet.
5. Post-game scoring is done only against the actual line (or chosen alt), not against the raw model number.
6. Injury during game = bet protect (do not count as miss).

## ADDITIONAL TRIGGERS & NOTES
- Injury boost: Clear opportunity increase for remaining players.
- Recent performance environment match: If player has hit high marks vs similar defensive profiles this season or 2025, slight additional boost.
- Low game total / low-volume script: Reduce soft-matchup boosts (do not force Overs in low-scoring environments).
- Blowout risk: Adjust volume in later quarters when one team is heavily favored.
- Red-zone usage: Boost TD probability for primary RZ players; do not automatically boost yardage.

## OUTPUT FORMAT
For each key player:
- Role
- Grade (Positive / Neutral / Slight Negative) + reason
- Percentiles (5th / 10th / 15th MAIN / 20th / 25th / Median)
- Available FanDuel/DraftKings line
- Lean (Over / Under / Alt X.X / No Bet)
- Notes (triggers applied, injury protect if applicable)

## EXAMPLE ROLE LOCKS (Reference)
- Rams: Puka Nacua (Volume), Davante Adams (Explosive/RZ), Kyren Williams (Rush-Receive)
- Cardinals: Trey McBride (TE-Primary), Michael Wilson (Explosive)
- 49ers: McCaffrey (Rush-Receive + Elite), Kittle (TE-Primary), Evans/Deebo (Explosive)
- Buccaneers: Irving (Rush-Receive), Godwin (Volume), Egbuka (Outside), Otton (TE)
- Packers: Josh Jacobs (Rush-Receive), Christian Watson (Volume/Outside), Matthew Golden (Explosive), Tucker Kraft (TE)
- Panthers: Chuba Hubbard (Elite Rusher), Tetairoa McMillan (Volume), Jalen Coker (WR2)

## RUN DEFENSE EXAMPLES (from the Oct 27 version)
- Bears: 4.44 YPC, 87.6 yds/G (Mixed)
- Cowboys: 4.72 YPC, 145.7 yds/G (Soft)
- Saints: 4.81 YPC, 139.4 yds/G (Soft)

Full model is permanent. Use this pipeline for every matchup. All role guidelines, defensive profile rules, three-model consensus, and FanDuel/DraftKings line comparison are required before final leans.

## OPPORTUNITY GATE (User rule, Oct 29, 2026 — runs BEFORE any matchup boost)
A soft defensive matchup only matters if the player gets the volume to use it. Season averages are not opportunity.
1. Project this game's volume first: expected team plays (pace + spread/game script), pass/run split, then the player's share.
   - Receivers/TEs: projected targets = projected team pass attempts × player's L3 target share (fix_player_role / fix_player_game_usage). Receptions line needs projected targets × catch rate ≥ line with margin; yards = targets × yards per target.
   - RBs: projected carries = projected team rushes × L3 carry share; adjust down when the team projects to trail (Henry Wk7, Walker Wk7).
2. Check the opponent's tendency against this team's structure: does this defense force the ball elsewhere (e.g., run-heavy script pulls targets off the TE — LaPorta Wk7: 97% snaps, 2 targets; DET ran Gibbs 29 times)?
3. Check the offense can sustain drives against this defense (3rd-down rate, red-zone rate, explosive allowed). If not, cap RB yards and kill TD legs (Walker Wk7: 14 of 16 KC carries, 36 yds, KC scored 3).
4. Only then apply the defensive-profile boost (outside vs slot, explosive allowed, zone/man).
5. If projected volume does not support the line → No Bet or a lower rung, no matter how soft the matchup.
6. Volatile-yards receivers (big week-to-week swings) get moderate rungs even on high volume (Golden Wk7: 12 targets, 39 yds).
7. Avoid volume legs on players whose team projects to be blown out, except receivers in garbage-time volume roles (with caution).
