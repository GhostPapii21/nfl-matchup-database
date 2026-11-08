---
name: betting-game-brainstorm
description: >-
  Use before building any sports betting projection, prop pick, parlay or slip
  (NFL first, NBA/CFB too): a brainstorm-first, critical-thinking game read that
  forms an edge hypothesis from matchup, script, injuries, coverage, the
  defense's opponent box scores, a layered receiving matchup ladder (QB vs
  pressure, targets, route trees, defenders, shell), QB throw logs, line play
  and weather, then tests it with data, which can cut it.
---
# Betting game brainstorm

The read comes first and the data comes second. The read is a hypothesis; data tests it. Data also answers "how much" and "which market." Legs picked from averages or sims alone have lost at real prices in every test, so every leg still starts from a written game read. Do this for every game before any number touches a leg, and write it out. If you can't write the edge in one plain sentence, there's no leg.

This skill sits in front of the sport's own checklist (for NFL, `nfl-game-script-run` and `nfl-betting-script`). Those still run afterward to choose the line, price it and stamp it.

## Ground rules
- Use only information available before kickoff or tip, and record when each fact was known.
- Write down a source for every claim: box score, play-by-play, injury report, beat writer, coverage charting, weather service.
- Data that clearly disagrees with a read can cut it; close calls get flagged. Data that agrees sizes it.
- Reads are tracked hypotheses: lock and hash each read before kickoff, and grade the read separately from the result.
- Never place bets. Never use private or back-door feeds.

## Step 1. Slate snapshot
For each game, note the spread, total, implied team totals, moneyline, kickoff time, venue (dome or outdoor), rest and travel, and any line movement since open. Start with the questions the market is answering: who does the book expect to lead, and how many points?

## Step 2. Game script hypothesis
Write the most likely flow in 2–3 sentences: who leads, by halftime or late, pace, run/pass lean, and garbage time. Then write the two biggest ways it flips, for example:
- The favorite gets up big early, runs the clock, and its QB and WR yards stall (DAL 38–21 vs PHI: Dak finished with 212).
- The underdog falls behind and abandons the run, so its RB's rushing line dies (KC was shut out vs SEA, and Walker went 14–36).
- A shootout: both QBs and the WR2s and TEs clear their lines, and correlated over legs all hit together (the London 31–28 ticket went 9 for 9).
- A defensive slog, or weather drags the total down.
Every leg you pick must survive the base script and at least one flip, or be tagged script-dependent.

## Step 3. Injury and news fallout (both sides of the ball)
- **Offense out or limited:** who absorbs the targets and carries? Name the next man up, his carries or targets per game, his yards per carry or per target, and his past share when the starter sat.
- **Defense out:** which coverage player or pass rusher is missing, and which offensive player now faces a backup? Missing slot corners and linebackers help TEs, RBs and slot WRs. Missing safeties help deep shots.
- **Offensive line out:** pressure rate up, rushing efficiency down, more quick throws (RB and TE catches up, deep WR yards down).
- Practice status trend (DNP, limited, full), questionable tags, game-time decisions, and a snap or rep limit for players coming back from injury.
- Checkpoints: the final injury report and the inactives about 90 minutes before kickoff. Re-run anything a late scratch touches.

## Step 4. Coverage and scheme matchup
- **Defensive shell:** MOFO vs MOFC (middle of the field open or closed), and the man vs zone rate. Against zone-heavy teams, the matchup is the hook, middle and slot area, not the outside corner. Map the WR, TE and RB to the zone defenders who cover them.
- **Pressure:** blitz rate and pressure rate, and how this QB performs when blitzed (time to throw, sacks, check-downs). Pressure that gets home kills deep WR yards and boosts RB and TE catches.
- **Where the defense gets beat:** yards and targets allowed by position (WR1, WR2, slot, TE, RB receiving), explosive plays allowed, and yards after the catch allowed.
- **Run defense:** yards per carry and rush EPA allowed, stuff rate, and box count tendencies, compared against this offense's line health and the RB's carry share.
- **Offensive tendencies:** primary target and his share, TE usage (is the TE a real receiving weapon?), motion and play-action rate, red-zone usage.
- **Primary target vs the defense's weak spot:** does the offense's top option attack exactly where this defense gives it up? That overlap is the core of an edge.

## Step 4b. Read the defense's box scores (what it allows)
Pull the box scores of every team that played this defense in its last 4–7 games and read them like a scout, looking for anything that stands out and repeats:
- **Rushing allowed:** team YPC and the RB1 line in each game. Note how many games went over a threshold (for example 3.6+ YPC) and any outliers, with the reason (script, QB, injuries).
- **Who went off:** the top 2 receivers in each game by yards and targets. Is it the same kind of player every week, like the primary target, the slot, the TE or the deep X? Check the secondary receiver too, not just the WR1.
- **Where they line up:** for each of those receivers, find his alignment (slot, wide left or right, inline TE) and type (X/Z/slot, deep vs YAC vs possession) from participation or alignment data, pass location, air yards or public scouting. Cite the source.
- **The pattern:** is the damage coming from the slot, one side, the middle or seams, deep or short?
- **Who covers that spot:** name the defenders who line up there (slot CB, each outside CB, safeties) and their current health.
- **Map it to this offense:** which of this week's receivers lines up in that spot and will draw that defender? That overlap is a hypothesis, which Steps 7–8 then test.
Write it as a short snapshot, with each claim's games and source, and flag any pattern built on fewer than 4 games.

## Step 4c. Receiving matchup ladder (run in this order)
Build the passing-game picture one layer at a time, and don't name receivers before the earlier layers are done:
1. **Possession script:** who has the ball more? A backup or third-string QB on the other side usually means shorter drives and more plays for this offense. Estimate plays and time of possession for each side.
2. **QB vs this pass rush:** the defense's pressure rate and blitz rate. This QB's numbers when blitzed vs not and pressured vs clean: completion %, yards per attempt, sack rate, time to throw, third-down conversions, and how often he still gets the ball out. Who he throws to under pressure.
3. **Target ladder:** rank the offense's targets 1, 2 and 3 for the season (and the last 3–4 games), with target share.
4. **Route trees:** use NFL Next Gen Stats route charts (or pass location by air yards as a stand-in) to find where each receiver, TE and pass-catching RB runs his routes, and whether he lines up in the slot or out wide.
5. **Who covers those routes:** map those areas to the defenders (each CB, the nickel, the safeties, the LBs) using PFF's free matchup page and the injury report, plus each defender's allowed numbers (yards per catch, rating).
6. **Shell and leaks:** is the defense middle-of-field open or closed, and man or zone, over its last 4–8 games? Where do the yards leak (for example, TEs up the middle against a MOFO team)?
7. **Test any "lockdown" claim:** a defender or unit only counts as strong if the players it covered actually finished below their usual numbers against it. Otherwise ignore the label.
Then name the receivers and backs who gain receptions or yards from this picture. They're hypotheses for Steps 7–8.

## Step 5. Box score and recent-form edges
Avoid season averages. Look at:
- The last 3–4 games' role: snaps, routes, targets, carries, air yards, red-zone looks.
- Role changes: new OC or play-caller, QB change, a returning or departing teammate.
- Games against similar defenses or similar scripts.
- Results that look fluky: TD-dependent games, one long play inflating yards, blowouts where starters sat late, or efficiency that won't repeat.
- What this defense allowed to similar players in its last 3–4 games.

## Step 5b. QB throw log (new, backup or changed QB)
Box scores and season data won't show how a new QB actually plays. When a team starts a backup, a rookie, a returning QB or a new play-caller, go through his snaps in the play-by-play (plus any public highlights) and write a throw log before building any leg from his offense:
- Every dropback: down and distance, blitzed or not, pressured or clean, intended target, air yards (short, intermediate or deep), and the result (catch, incompletion, INT, sack, scramble).
- Who he looks for under the blitz and pressure (his "hot" outlet, often an RB or TE) vs. who he looks for on clean pockets.
- Whether he can push the ball downfield, or lives on check-downs and short or intermediate throws, and which receivers that helps or hurts.
- The story in plain words: "what he was doing" in that game, and how it lines up with the coming opponent's blitz and pressure rates.
Use the log to build the receiving legs and early-game spreads. A small sample (one or two games) is a read, not a stat gate. Flag it as a small sample and leave the call to the user instead of quietly cutting the leg as missing data.

## Step 6. Weather and environment
Wind of 15+ mph hurts deep passing and kicking, so lean toward rushing and short passing. Rain or snow lowers efficiency and helps unders. Extreme cold, altitude, turf vs grass, and dome-to-outdoor travel also matter. Check the forecast close to kickoff, not days out.

## Step 7. Write the edge
Pick 1–2 edge players per game at most. For each, write:
- **Edge sentence:** why this player beats this line today, in plain words.
- **What has to be true:** script, health, snap share.
- **What kills it:** the scenario that loses the leg.
- **Confidence:** strong, lean, or pass.

## Step 8. Data check (test the read)
- Run the projection and sims, and compare to the no-vig price from the sharp book (Pinnacle).
- Agree: size it and pick the rung.
- Disagree on a strong read: cut it if the data gap is clear, flag it if it's close.
- Disagree on a lean: drop it.
- Treat model probabilities above about 70% with suspicion. Past calibration showed legs rated 70–80% hitting about 50%.

## Step 9. Choose the market
- **Volume edge** (more targets because the defense gives up short and middle, or pressure forces quick throws): receptions.
- **Efficiency or explosive edge** (weak secondary, deep shots, a bad safety matchup): receiving yards, or a higher rung.
- **Carry share plus a weak run defense in a positive script:** rushing yards. A bad script or a strong run defense: rushing under.
- **Script edge for the whole game:** game or half spread and total, team totals.
- Price the rung. Short-priced alts have lost money over and over, so only take them as correlated anchors.

## Step 10. Pre-mortem and red team
For each leg and slip, argue the opposite side for one paragraph: "It's Monday and this lost. Why?" Check for an injury, a script flip, a snap limit, the backup vulture, the weather, or the defense taking him away. If the counter-case is stronger than the read, drop the leg.

## Step 11. Build slips around one story
Each slip tells one script. Legs that win together belong together, for example a shootout stack or a favorite-runs-the-clock stack (RB over, opposing QB attempts over). Don't mix legs that need opposite scripts (a total under with same-game overs). Keep main slips to 3–4 legs with no TDs, and follow the house rules on depth receivers and one market per player.

## Step 12. Log it and postmortem it
Save the written read with its timestamp before kickoff. After the game, grade the READ (was the script right? was the edge right?) separately from the RESULT (did the leg hit?). Note which brainstorm step would have caught each miss, and feed that into the team and player files.

## Output format (per game)
```
GAME / kickoff / spread / total / weather
SCRIPT: base case + 2 flips
INJURY FALLOUT: who gains, who loses, next man up's per-game numbers (sources)
MATCHUP: shell, pressure, where the D bleeds, primary target overlap
DEFENSE BOX-SCORE READ: rush allowed per game, who went off + where they line up, the pattern, the defender in that spot, this week's receiver who draws him
RECEIVING LADDER: possession script, QB vs pressure/blitz, targets 1-2-3, route trees, who covers them, MOFO/MOFC + leaks, lockdown claims tested
FORM: last 3-4 games role notes
QB THROW LOG: (new/backup QB only) targets by blitz/pressure and depth, plain-words story
EDGE PLAYERS (max 2): edge sentence / must be true / kills it / confidence
DATA CHECK: model, sim median, no-vig, agree / flag / cut / drop
MARKET + RUNG + price
PRE-MORTEM: strongest case against
SLIP STORY: which script stack it belongs to
```
