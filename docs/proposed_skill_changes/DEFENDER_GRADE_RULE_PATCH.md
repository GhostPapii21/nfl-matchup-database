# PROPOSED (not applied): defender-grade rule for receiving legs

Status: draft for Rico's decision (t548u, 2026-11-27). Nothing in the skills, rulebook or `pregame/` is changed by this file.

## Current rule (to be replaced)
> No receiving leg without a verified main defender (named on a PBU, INT or DPI; a tackler alone is inferred).

## Proposed rule text
> **Receiving legs: team profile + defender grade.** A receiving leg may rest on (1) the defense's team-allowed profile (yards/target and yards/game
> allowed to the receiver's position, plus its weak zones) and (2) the grade of the likely matchup defender. The likely defender is the outside corner
> on the receiver's usual side, or the slot/nickel or safety for slot WRs and TEs, taken from `data/coverage/defender_profiles_2026`. A verified
> defender is **no longer required**.
> - Opposing defender is **LOCKDOWN** → FLAG. Overs need the team profile to be bottom-10 against that position, or the leg is CUT. Unders get a plus.
> - Opposing defender is **WEAK LINK** or **TARGET MAGNET** → supporting evidence for overs. It never clears a leg on its own.
> - Defender grade has fewer than 35 targets or comes from inferred columns only → FLAG (small sample). Label the leg INFERRED MATCHUP.
> - Likely defender is out or questionable → use the next defender on the depth chart and his grade. No grade → team profile only, with a flag.

## How it fits the existing checklist
- The volume/opportunity gates, the WR3 rule (Nov 2: WR3 overs only vs a secondary missing 2+ corners, 4+ targets/game with the current QB) and the
  #3/#4 WR and #2 TE rule (Nov 3: QB targets them 5%+ over the last 4) are unchanged. This rule replaces only the "verified main defender" requirement.
  The WR3 rule's "named matchup defender or coverage giving up production" check is met by this grade or the team profile.
- WR3+ unders can still pass on the team coverage profile with a flag (Nov 2), as now.
- Every other gate is unchanged: no passing-yards legs, no game-total under with same-game player overs, weather kill test, Ghost6 VETTED before anything is
  called a pick, `projection_ready=false`.
- Evidence: the backtest in `data/coverage/defender_profiles_2026/GRADES.md` (weeks 4–11, own-average benchmark) shows LOCKDOWN secondaries cutting
  receivers by about 6 yards and 9 points of beat-average rate. That supports the LOCKDOWN flag. WEAK LINK / MAGNET showed no edge, which is why it's
  supporting evidence only.
