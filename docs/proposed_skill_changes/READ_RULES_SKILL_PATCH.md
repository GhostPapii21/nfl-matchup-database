# Proposed skill text: three read rules (flags only), Week 13 on

refs NFL-56. Rico approved the three rules Nov 26, 2026, 7:11 PM ET ("Yes, have Blitz add all three rules", via
Ghost6). This PR does not edit any skill. The blocks below are for the bot owner to paste. They keep every rule a
FLAG: none may mark a leg FAIL or CUT until a backtest beats the rushing-under baseline and Rico approves the switch.

## 1. `nfl-game-script-run/SKILL.md`

### 1a. New section, insert after "## Repo pregame packets and ANALYST_PROMPT.md" (end of file)

```markdown
## Read rules: targets first, defense-allowed profile, hourly weather (Rico, Nov 26, 2026, 7:11 PM ET; every run from Week 13; FLAGS ONLY)
Run once per game before the phases: `python -m pipeline.read_rules --game <nflverse game_id>` in the
nfl-matchup-database repo (writes `pipeline/ledgers/read_rules/READ_RULES_<game>.md/.json`). Copy each flag into the
checklist with status **FLAG** (never FAIL), its number, source and pull time. These three rules never cut, demote or
re-label a leg. They may become cuts only after `python3 -m calibration.read_rules_backtest` shows the rule beating the
rushing-under baseline (n >= 30, paired diff CI lower bound > 0) AND Rico approves. As of Nov 26 none does.

1. **Targets first.** Every WR/TE receiving leg shows the player's share of team targets over his last 4 games
   (needs 3): WR needs about 20%+, TE needs to be a top-two team target. A low-share, "mostly on the field" player is
   credited only when the opposing defense allows a lot to his role (top-10 in yards per game allowed to TE / RB /
   slot WR / outside WR). Slot vs outside has no free source, so a WR's role exception is "unknown" and never makes
   him pass. Statuses: PASS, PASS_ROLE_EXCEPTION, FLAG_LOW_TARGET_SHARE, INSUFFICIENT_HISTORY.
2. **Defense-allowed profile, both sides of the ball, every opponent.** Sharp (MOF closed vs open, man/zone),
   PFF free recap pages only (no paid content, never PFF weather) and NGS where they carry the field, plus
   play-by-play: which CBs and safeties allow the most (PBU/INT/DPI are verified; catches/yards from the tackler are
   inferred and labelled so), catches and yards allowed to TE, RB, slot WR, outside WR, short/intermediate/deep
   allowed, and designed-run YPC allowed. Every figure carries a source and a pull time. Missing data is
   "unknown", never zero, and never cuts a leg by itself.
3. **Hourly weather grade.** NWS and Open-Meteo only, each hour of the game window: rain rate none / light (<0.05
   in/hr) / moderate (0.05-0.3) / heavy (>0.3), sustained wind and gusts, sources side by side (a disagreement is
   shown, never averaged). Dome or closed roof = not graded. Finish with a stated run-tilt read for each team.
   A failed pull is "unknown", never calm.
```

### 1b. Phase 2 "Opportunity gate", append one bullet

```markdown
- Read rule 1 (targets first) is reported here as a FLAG with the share, the team rank and the window. It does not
  replace or loosen this gate and it never cuts on its own (see "Read rules" section).
```

### 1c. Phase 3 "Defensive profile (both teams)", append one bullet

```markdown
- Attach the read-rule 2 defense-allowed profile from `READ_RULES_<game>.md` for both defenses (MOF closed/open,
  top DBs allowed with verified vs inferred labels, by-role and by-depth allowed, run YPC). Unknown stays unknown.
```

### 1d. "Checklist output (REQUIRED)", append after "Any FAIL, MISSING or STALE marks the leg CUT."

```markdown
- Read-rule rows use status FLAG (or PASS) and are excluded from that cut rule: a FLAG is information for the
  vetter and the user, not a cut.
```

## 2. `betting-game-brainstorm/SKILL.md`

### 2a. Step 4b "Read the defense's box scores (what it allows)", append

```markdown
- Pull the read-rule 2 profile (`python -m pipeline.read_rules --game <id>`) for BOTH defenses: MOF closed vs open
  share (Sharp), the CBs/safeties allowing the most (verified PBU/INT/DPI vs inferred-from-tackler, labelled),
  catches and yards allowed to TE, RB, slot WR and outside WR (slot/outside "unknown" until a free alignment
  source exists), short/intermediate/deep allowed, and run YPC allowed. Every figure keeps its source and pull time;
  unknown is never zero and never cuts a leg. Flag only (Rico, Nov 26, 2026).
```

### 2b. Step 4c "Receiving matchup ladder", insert as the first rung

```markdown
0. **Targets first (flag).** Before the ladder, write the player's last-4 share of team targets (WR ~20%+, TE
   top-two). A low-share "on the field" player only gets credit when this defense allows a lot to his role
   (top-10 vs TE/RB/slot/outside). Thanksgiving example: Pickens had 2 catches. This is a flag; it does not cut
   until the backtest says so.
```

### 2c. Step 6 "Weather and environment", append

```markdown
Grade each hour of the game window from NWS and Open-Meteo only (never PFF weather): rain none / light (<0.05 in/hr)
/ moderate (0.05-0.3) / heavy (>0.3), sustained wind and gusts per hour, both sources side by side. End with one
stated run-tilt read per team (e.g. "BUF: run-tilt up, deep passing and kicking down; already run-leaning"). Flag
only; a failed pull is unknown, not calm.
```
