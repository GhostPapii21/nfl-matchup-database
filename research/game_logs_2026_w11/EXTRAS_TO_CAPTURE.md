# Extras worth capturing that Rico hasn't asked for yet (Blitz, refs NFL-56)

Already captured in every game file (from free data):
- Explosive plays (pass 20+, rush 15+) with the tackler named, and explosives allowed per defense.
- Sack rate and QB-hit rate (QB hits are the `[bracketed]` names in NFL play text; a pressure proxy, not true pressure rate).
- Early-down (1st/2nd) pass rate, completed air yards vs YAC (ESPN yardsAfterCatch), penalties by type, in-game injuries from play text, garbage-time flag per play (ESPN win prob), weather at kickoff (ESPN + Open-Meteo model hour) vs pre-game forecast notes.
- Third downs by distance bucket (short/medium/long), drive-by-drive outcomes, red-zone trips and usage inside the 20.
- Paper slip legs graded against results (SLIP_LEG_RESULTS.md; unofficial, the 11:45 PM ET routine is official).

Still to add (needs a later run or a source that posts later):
- Snap shares / routes run (nflverse snap counts + PFR, Mon-Tue). Route participation is the best predictor of receiving props.
- Intended air yards on every target, aDOT, EPA/CPOE, pass_defense_1/2 fields (nflverse pbp overnight rebuild).
- NGS final week-11 statboard (separation, cushion, RYOE, time to throw) Monday; route charts are images only.
- Official highlight transcripts for each game (NFL posts full-game highlights 1-3 hours after the final) to attach more defenders by name.
- Two-minute-drill / end-of-half usage, personnel groupings (11/12/21), and play-action rate: not in free play text; FTN charting is paid, so these stay unknown.
- Kicker distance/accuracy and punt/kick return yardage (in ESPN pbp already; not summarized yet).
- Officiating crew per game (ESPN gameInfo.officials, already in the raw JSON) joined to penalty counts for the referee table.
- Closing-line value: our 12:39 PM AST prices vs the AN close, per slip leg.
- Live-test check for the model: each locked projection vs actual (NFL-49 scorer handles this tonight; not touched here).
