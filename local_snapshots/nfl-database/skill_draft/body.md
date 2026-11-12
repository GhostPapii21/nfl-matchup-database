
# NFL game script run

A step-by-step, checkable run of the shared NFL game script. **The researcher** runs it for every game on the slate. **The chief of staff/vetter** re-checks the checklist and signs off. Nothing reaches the user until that sign-off.

Authorities (read them, don't copy them):
- Evidence rules: `/workspace/nfl-database/GAME_SCRIPT_2026-10-29.md`. Where sources conflict, it governs evidence.
- Projection model: `/workspace/nfl-database/PHASE_SCRIPT.md`.
- Staking, slip tiers, bankroll, QB grade card (§15), de-vig (§18), star unders, pre-mortem: the **nfl-betting-script** skill. This skill does not restate them; apply them at Phase 14.
- Lessons: `/workspace/nfl-database/postmortems/`. Read the latest one before every run.

## Run setup
1. Make the run folder `/workspace/nfl-database/runs/<YYYY-MM-DD>_<AWAY>@<HOME>/`. Never overwrite an earlier run; a re-run gets a new suffix (`_r2`).
2. Record the exact game identity: season, week, game ID, kickoff (ET), venue. Also record the input cutoff time, the seed and the trial count.
3. Stamp every number with its source and its pull time (ET). Evidence older than 48 h is STALE. An unknown timestamp is STALE.
4. Status words: PASS, FAIL, MISSING, STALE, UNVERIFIED, N/A. A MISSING or STALE required input **cuts the leg**. Never estimate a paid or unavailable stat.

## Phases (run in this order for every candidate leg)

**1. Data pull and reconcile**
- Pull: nflverse play-by-play, box scores, snaps, participation where it exists, and FTN charting for the season. Also pull the current depth charts.
- Rules: QB gross passing yards are kept separate from team net. Regulation is kept separate from overtime. Credits get reconciled to the official box score.
- Record: the sample window, plus each player's game log with targets, receptions, yards, carries and snaps.

**2. Opportunity gate (FIRST; nothing else runs on a leg that fails it)**
- Projected targets = projected team pass attempts (from pace and spread) × the last-3 target share. Projected carries = projected team rushes × the last-3 carry share, trimmed when the team projects to trail.
- Test: projected volume × catch rate (or × YPC/YPT) clears the line with margin. Season averages don't count as opportunity.
- **No #3/#4 receivers.** Only a team's top-2 target earners at WR/TE, or its primary receiving back, are eligible.
- Vacated-role exception: rank the candidates by snaps and routes in the games that role was open. Bet the role only when one player clearly held it.
- Catches overs: 5+ targets in 3 of the last 4 games with this QB, and no same-role teammate at 28%+ of targets.
- Record: the projected volume, the shares and the math.

**3. Defensive profile (both teams)**
- Pull:
  - Team yards allowed per game (pass and rush).
  - Points allowed.
  - WR/TE/RB targets, receptions, yards and YPT allowed. Keep the denominators, and use one consistent basis: per target.
  - Outside vs slot YPT.
  - Run YPC allowed (RB-only).
  - **Explosive plays allowed** (rec 20+, rush 15+; count and yards).
  - Red-zone TD% and 3rd-down % allowed.
- Sources: nflverse pbp; Sharp positional coverage, schemes, tendencies and advanced box scores; ESPN team stats.
- Thresholds (PHASE_SCRIPT): Outside YPT ≥10.5 soft; WR ≥9.0; TE ≥8.0 soft and ≤5.5 hard; run YPC ≤3.8 suppression and >4.4 soft.
- Test "soft against X" for volume vs efficiency and for the quality of the opponents faced.

**4. Defender coverage check (HARD, every WR/TE leg and every RB receiving leg)**
- Pull real per-defender numbers for each likely CB/S/LB: targets, completions, comp %, yards, YPT and rating allowed.
  - Sources: PFR advanced defense (cached copy, refreshed each slate) and StatRankings.
  - Add man/zone rate and MOF open/closed from FTN charting and Sharp schemes.
- Map the player to his likely defender by alignment and side, and match his routes (NGS/FTN) to that coverage.
- Fail: a catches over against a low comp % allowed, or a yards over against a low YPT allowed. Either one gets cut or moved down a rung unless the volume clears it with room.
- **No stand-ins**, such as the defender named on completions or team outside/slot splits. Missing this check means MISSING, and the leg is cut.

**5. Pressure, blitz and checkdown layer**
- Pull:
  - Defense blitz rate, season and last 4 (FTN `n_blitzers>0`, or 5+ rushers).
  - Pressure rate. Use real pressure when it's published. Otherwise use the proxy (sack or QB hit or scramble) / dropbacks, **labelled PROXY**.
  - QB time to throw (NGS passing).
  - QB aDOT, all vs blitzed.
  - Behind-the-line-of-scrimmage share.
  - **Target share by player when blitzed vs not, and when pressured vs clean** (pbp joined to FTN).
- Opponent yards allowed (e.g. RB YPT) **adjusted for the QBs faced**. Compare with the league average on the same basis.
- Test:
  - A high blitz rate cuts volume legs on primary receivers only if those receivers' blitzed share drops.
  - A checkdown boost applies only if the back's or TE's blitzed share actually rises.
  - Check the Panthers rule (top-10 blitz, top-10 pass-rush win rate, OL injury, poor QB response). Any of the first three plus the fourth means CAUTION, and the user decides.
- Record: blitzed-target samples (n). Under 15 targets, label the result LOW-SAMPLE.

**6. QB grade card**
- Run the nfl-betting-script §15 card for every slate QB. Receiver legs inherit their QB's gates.

**7. Role and RB market rules**
- Lock roles (PHASE_SCRIPT role categories).
- **Rush-receive backs are graded on rush+rec**, not on rushing alone. A rush-only over on a team that could trail needs 4+ targets per game, or switch it to rush+rec.
- Committee backs: a rushing over needs a 60%+ carry share in 3 of the last 4.
- RB receiving yards need 6+ YPT in 3 of the last 4, and an opponent allowing above-average RB YPT (QB-adjusted).

**8. Injuries, both sides**
- Pull: the ESPN injury report and official team reports. Track practice participation Wed–Fri (DNP/LP/FP), the game designation and inactive status separately.
- Check offense and defense: QB, RB, WR, TE, **OL** (LT/RT/C/interior), **DL** (edge/interior), LB, **secondary** (CB/slot CB/S).
- Effects:
  - Backup OT means more pressure and fewer deep or QB-yardage overs.
  - Missing the C or 2 interior OL caps lead-RB rushing overs.
  - A backup slot CB boosts the opposing slot WR/TE.
  - A replaced coverage defender means re-running Phase 4.
- Questionable players are NOT auto-cut (user ruling): keep them only on a lower rung, flag them, and re-check at Phase 15; drop if inactive or downgraded. No leg that only works if a questionable teammate sits. Staking follows nfl-betting-script.

**9. Next Gen Stats**
- Pull from public NGS pages only: routes, separation, rushing over expected and time to throw for both teams. Log any field that isn't available. Never use tracking feeds.

**10. Film**
- Primary source: official NFL highlights and gamebooks. Log the URL, timestamp and play for each.
- A film read is **UNVERIFIED unless every cited play matches a play-by-play row** (quarter/clock, player, yards). UNVERIFIED reads are disclosed and never count as a PASS.

**11. Environment**
- Pull: roof, sustained wind and gusts, rain and temperature for the game hours; rest and travel; stakes.
- Sustained wind of 15+ mph cuts deep legs and passing overs. These are review flags, not fitted modifiers.

**12. Source audit**
- Record for every source: its columns, its data-through time and its pull time. Anything over 48 h old is STALE, and a STALE required input cuts the leg.

**13. Game-script / underdog gate (10G)**
- Classify the game as blowout favorite, moderate favorite, toss-up or underdog from the spread, team EPA and Sharp matchup evidence.
- **Underdog legs are BLOCKED** unless the opponent has a verified, written trap or elimination exception.
- When the projected margin is 8.5 or more, check 4th-quarter minutes and use a lower alt rung.
- A script PASS never overrides a hard fail or a MISSING input.

**14. Models, price and edge**
- **Three models at 100,000 sims each**: Monte Carlo, Bias (volume −8%, catch rate −3%, yards −5%) and Game Randomness (a shared game-level shock plus a spread tilt).
  - Seeded. Record the seed and the script path.
  - YPC and YPT are regressed toward league before the opponent factor.
- Price: FanDuel main and alt ladders, both sides. No-vig with the multiplicative method; alts are de-vigged against the same stat's main two-way market.
- **Shared edge rule (all must hold):**
  - avg(p) − no-vig ≥ **+3 points**.
  - Shrunk p' = 0.5 + 0.7(p − 0.5); p' − no-vig **> 0**. This shrink applies to the **probability**, never to per-play yards.
  - Every model's p ≥ **.45**. This floor stops long-shot rungs from passing because of the shrink.
  - The sim median clears the line (over) or sits below it (under).
- Model-vs-market sanity check: a median 12+ yards off the market main is MODEL-SUSPECT and goes back through Debugging before it can pass.
- **Placed-ticket market bars:** no leg on the same player and stat (or a nested rung of that stat) as an already-placed ticket or open SGP. Same-player, different-stat stacks are flagged for the user to decide. Then apply the slip rules (nfl-betting-script §11–12).

**15. Inactives check**
- About 90 minutes before kick (Sundays ~11:30 AM ET for 1 PM games, ~2:35 PM for 4 PM games, ~6:50 PM for night games), recheck:
  - every leg against the inactives
  - the coverage defenders from Phase 4
  - weather
  - prices
- Any line move of more than 0.5 or 20 cents means a reprice through Phase 14. A leg whose reason no longer holds is dropped.

## Checklist output (REQUIRED)
Write `/workspace/nfl-database/runs/<date>_<game>/checklist.md`:

```
| Leg | Phase | Status (PASS/FAIL/MISSING/STALE/UNVERIFIED/N/A) | Number | Source | Pulled (ET) |
|-----|-------|------|--------|--------|-------------|
| <player stat rung price> | 2 Opportunity | PASS | 8.3 tgt × .66 = 5.5 rec vs 4.5 | nflverse pbp wk1-8 | 2026-..-.. 18:53 |
```
- One row per phase per leg, 15 rows per leg. Use N/A only where the phase doesn't apply (e.g. Phase 4 on a pure rushing leg), with the reason.
- Any FAIL, MISSING or STALE marks the leg CUT. Put a summary block at the bottom with the legs that passed, the legs cut and why, the seeds, the script paths and the data gaps.
- Send the checklist path to the vetter. The vetter re-runs at least the edge math and spot-checks one source per leg. The vetter then writes `VETTED: <name/role> <time ET>` or `REJECTED: <reasons>` at the top. **Nothing goes to the user before VETTED.**

## Debugging (when a number looks off or the engines disagree)
1. Stop. Don't change the leg, the model or the threshold yet.
2. Find the root cause by tracing the input → formula → output for one leg by hand. Past examples:
   - Shrink applied to per-play yards instead of the probability, which left count markets unshrunk.
   - Unregressed YPC inflated the rush medians.
   - A wrong denominator turned a 4.04 RB YPT into 1.85.
   - A parser over-counted yards against the box score.
3. Fix only that cause, and log it with its evidence in the run folder.
4. Re-run both engines unchanged otherwise, with the same seed. Claim a fix only after the re-run output shows it. Re-grade every leg the bug touched.

## Hard rules
- Never place bets or submit slips. Recommendations only; the user decides.
- Never use tracking feeds, private or undocumented APIs, or scraped sessions. Public pages and cached public files only. Outlier and any signed-in site are **read-only**.
- Never print API keys, tokens or passwords in files, logs or messages.
- No invented sims, sources or thresholds. If the engine can't run, write `SIMULATION NOT RUN`.
- No padding a card to reach a leg count. Zero qualifying legs means "no card".
