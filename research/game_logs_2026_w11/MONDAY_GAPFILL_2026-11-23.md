# Week 11 completeness audit + Monday gap-fill (2026-11-23, Blitz; refs NFL-56, refs NFL-49)

Request (Rico, Nov 23 7:08 AM AST): make sure every game is logged and locked and has no missing data. Research only; projection_ready untouched; no Odds API calls; no PFF/paywalled content.

Scope: Week 11 is 13 games. 12 are final and logged here (TNF IND@HOU 11/19 through SNF MIN@SF 11/22). MNF CIN@WAS (11/23, 9:15 PM AST) has not been played, so it has no log yet; its locks are in LOCK_AUDIT_W11.md.

## Defects found in the logs already on main, and fixed here

1. **Every interception was missing from the pass-defender logs.** ESPN writes INTs as "pass ... intended for X INTERCEPTED by Y", or with no receiver at all. The builder's pass parser only matched "pass ... to X", so it dropped all 14 INT plays in the 12 games. They were missing from VERIFIED counts, leaks by position, depth/location splits, defense_db rows and team profiles. Every INT credit in the old index read 0, including for the players who made the 14 picks. Fix: `tools/build_logs.py` parse_pass now matches "intended for" and receiver-less INTs. The defender named in parentheses on an INT (the NFL feed's pass-defensed credit) gets a VERIFIED PBU.
2. **Replay reversals were graded on the overturned call.** Two PBUs credited on main were reversed to completions with forced fumbles: NYJ@LAC Q4 8:24 J.Sherwood and BAL@CAR Q4 14:23 W.Lee. Both are now tackler (inferred) rows. One reversed IND@HOU INT (C.Bynum, Q2 5:54) is now graded as the final ruling, an incompletion with no defender named. Fix: parse_pass grades only the text after "REVERSED.".
3. All 12 games were rebuilt offline from the cached raw pulls (ESPN summary JSON, Action Network pre-game lines, ESPN rosters). Nothing in the game logs was re-pulled, so lines, scores and pull stamps are unchanged. Only the NGS snapshot was re-pulled, on purpose, for final Monday values. The diff against main is only the INT and reversal changes. defense_db.csv: the 240 W11 builder rows on main were replaced by 248 corrected rows, with 0 duplicate keys.

After the fix, every game's ESPN-text PBU/INT named-defender rows match nflverse's pass_defense / interception fields exactly (see table). DPI rows come from the penalty text and are not in those nflverse fields.

## Per-game status

| Game | Logged | VERIFIED rows main -> fixed | INT plays added | PBU/INT match vs nflverse | Filled today | Still unknown (reason) | Lock |
|---|---|---|---|---|---|---|---|
| IND@HOU | Y | 7 -> 9 | 2 | 9/9 | intended air yds + per-receiver air share; NFL-feed weather; NGS Monday re-pull; snap counts; QB vs blitz / 5+ rushers / PA (FTN) | man/zone, MOF shell, true pressure, route trees, slot/outside, assigned defender on completions (no free source) | MISSING (no lock ever made) |
| MIA@BUF | Y | 15 -> 18 | 3 | 17/17 | intended air yds + per-receiver air share; NFL-feed weather; NGS Monday re-pull; video checked | snap shares (not posted: nflverse snap_counts last updated 11/20; PFR Cloudflare-blocked to box); blitz/rushers (FTN via nflverse not posted yet); man/zone, MOF shell, true pressure, route trees, slot/outside, assigned defender on completions (no free source) | VALID (2 locks) |
| NO@CHI | Y | 6 -> 8 | 2 | 8/8 | intended air yds + per-receiver air share; NFL-feed weather; NGS Monday re-pull; video checked | snap shares (not posted: nflverse snap_counts last updated 11/20; PFR Cloudflare-blocked to box); blitz/rushers (FTN via nflverse not posted yet); man/zone, MOF shell, true pressure, route trees, slot/outside, assigned defender on completions (no free source) | VALID (2) |
| TEN@DAL | Y | 5 -> 5 | 0 | 4/4 | intended air yds + per-receiver air share; NFL-feed weather; NGS Monday re-pull | snap shares (not posted: nflverse snap_counts last updated 11/20; PFR Cloudflare-blocked to box); blitz/rushers (FTN via nflverse not posted yet); man/zone, MOF shell, true pressure, route trees, slot/outside, assigned defender on completions (no free source) | VALID (2) |
| TB@DET | Y | 12 -> 12 | 0 | 10/10 | intended air yds + per-receiver air share; roof confirmed (indoor); NGS Monday re-pull | snap shares (not posted: nflverse snap_counts last updated 11/20; PFR Cloudflare-blocked to box); blitz/rushers (FTN via nflverse not posted yet); man/zone, MOF shell, true pressure, route trees, slot/outside, assigned defender on completions (no free source) | VALID (2) |
| ARI@KC | Y | 7 -> 7 | 0 | 7/7 | intended air yds + per-receiver air share; NFL-feed weather; NGS Monday re-pull | snap shares (not posted: nflverse snap_counts last updated 11/20; PFR Cloudflare-blocked to box); blitz/rushers (FTN via nflverse not posted yet); man/zone, MOF shell, true pressure, route trees, slot/outside, assigned defender on completions (no free source) | VALID (1) |
| PIT@PHI | Y | 11 -> 11 | 0 | 11/11 | intended air yds + per-receiver air share; NFL-feed weather; NGS Monday re-pull | snap shares (not posted: nflverse snap_counts last updated 11/20; PFR Cloudflare-blocked to box); blitz/rushers (FTN via nflverse not posted yet); man/zone, MOF shell, true pressure, route trees, slot/outside, assigned defender on completions (no free source) | VALID (2); kickoff_utc field wrong |
| BAL@CAR | Y | 10 -> 11 | 2 | 10/10 | intended air yds + per-receiver air share; NFL-feed weather; NGS Monday re-pull; video checked | snap shares (not posted: nflverse snap_counts last updated 11/20; PFR Cloudflare-blocked to box); blitz/rushers (FTN via nflverse not posted yet); man/zone, MOF shell, true pressure, route trees, slot/outside, assigned defender on completions (no free source) | VALID (1) |
| NYJ@LAC | Y | 4 -> 3 | 0 | 3/3 | intended air yds + per-receiver air share; NFL-feed weather; NGS Monday re-pull | snap shares (not posted: nflverse snap_counts last updated 11/20; PFR Cloudflare-blocked to box); blitz/rushers (FTN via nflverse not posted yet); man/zone, MOF shell, true pressure, route trees, slot/outside, assigned defender on completions (no free source) | VALID (3) |
| LV@DEN | Y | 12 -> 14 | 2 | 13/13 | intended air yds + per-receiver air share; NFL-feed weather; NGS Monday re-pull | snap shares (not posted: nflverse snap_counts last updated 11/20; PFR Cloudflare-blocked to box); blitz/rushers (FTN via nflverse not posted yet); man/zone, MOF shell, true pressure, route trees, slot/outside, assigned defender on completions (no free source) | VALID (3) |
| JAX@NYG | Y | 21 -> 23 | 2 | 22/22 | intended air yds + per-receiver air share; NFL-feed weather; NGS Monday re-pull | snap shares (not posted: nflverse snap_counts last updated 11/20; PFR Cloudflare-blocked to box); blitz/rushers (FTN via nflverse not posted yet); man/zone, MOF shell, true pressure, route trees, slot/outside, assigned defender on completions (no free source) | VALID (1); kickoff_utc field wrong |
| MIN@SF | Y | 6 -> 7 | 1 | 7/7 | intended air yds + per-receiver air share; NFL-feed weather; NGS Monday re-pull | snap shares (not posted: nflverse snap_counts last updated 11/20; PFR Cloudflare-blocked to box); blitz/rushers (FTN via nflverse not posted yet); man/zone, MOF shell, true pressure, route trees, slot/outside, assigned defender on completions (no free source) | VALID (2) |
| CIN@WAS | N (MNF tonight, not played) | - | - | - | - | whole game pending: log after final | VALID (2 locks, Sun Nov 22) |

## Field-by-field (Rico spec) for the 12 final games

| Field | Status |
|---|---|
| Full PBP reconciled to ESPN play count | filled, all 12 match ESPN box Total Plays |
| Q1-Q4, 1H/2H, quarter/half spread and total winners, Q2 leader | filled |
| Final vs close: outright / cover / total / push | filled. Lines are Action Network pre-game (is_live=false), per book plus consensus, with pull time. AN does not publish a timestamp for each line, so the exact time each line was last moved is unknown (feed limit). |
| 3rd/4th downs, red zone trips/outcomes/touches, turnovers, drives/TOP, scoring breakdown | filled. RZ usage now counts INT targets inside the 20. |
| WR/TE/RB targets, rec, catch %, yds, target share | filled. Cross-checked against nflverse: targets agree for every receiver in all 12 games (BAL Matt/Matthew Hibner is a name-spelling difference, 2 targets on both sides). |
| Coverage defender per pass play | VERIFIED = named PBU/INT/DPI (now including INTs); tackler = inferred; unattributed where the text names nobody. No Play rule kept. Assigned defender on completions is unknown (no free source). |
| QB vs zone/man, blitz, MOF | blitz, 5+ rushers, play action and out-of-pocket filled for IND@HOU (FTN via nflverse). Not yet posted for the Sunday games. Man/zone and MOF are unknown for all games (no free play-level source). |
| Leaks by position | filled (INT targets now included); slot vs outside unknown |
| Weather | ESPN has no block. Filled from the NFL game-feed string (nflverse pbp) plus the Open-Meteo kickoff hour. TB@DET is a dome with no feed string. |
| Extras: explosives, sacks, QB-hit proxy, early-down pass rate, completed air/YAC, penalties, injuries, garbage time | filled. Intended air yards (including incompletions) filled today. True pressure rate is unknown (charting is paid). |
| Snap shares | IND@HOU filled. Sunday games are unknown until nflverse snap_counts updates. |
| defense_db rows / DEFENSE_PROFILES.md | rebuilt with INT/reversal fixes, 0 duplicate keys |
| SLIP_LEG_RESULTS.md | all Sunday legs graded; CIN@WAS legs pending tonight (unchanged by the fix) |

## Sources pulled today (2026-11-23 AST)

- nflverse-data releases (pbp 2026, weekly rosters, snap_counts, ftn_charting, NGS): asset update times and sha256 are in monday_fill/MANIFEST.json. Files are on the box at /tmp/w11fill and not committed (size).
- NGS statboard re-pull (nextgenstats.nfl.com public API), 2026-11-23 07:18 AM AST.
- Official NFL YouTube highlight captions (English - CC1) via yt-dlp: MIA@BUF F69kepglAY0, NO@CHI TAvO7hOMR70, BAL@CAR wdlsXc0by8U. No new coverage rows: every caption-named defender on a pass play is already a pbp-VERIFIED PBU/INT/DPI. Scheme mentions (e.g. "ends up being zone coverage", "press man coverage against Lane") are listed in VIDEO_EVIDENCE.md as video-level notes and are not charted per play.
- Pro Football Reference snap counts: the box got a Cloudflare challenge, which was not bypassed.

## Still open / for Rico

- IND@HOU (TNF) never got a pre-kickoff lock. It cannot be fixed now; a post-kickoff lock would be invalid.
- CIN@WAS: valid Sunday locks exist. A fresher pre-kickoff lock today (after inactives) is optional and Rico's call. Log the game after it goes final.
- Sunday snap counts and FTN blitz charting: re-run `tools/monday_fill.py` + `tools/monday_md.py` once nflverse posts them (usually Tue-Wed).
- FTN data via nflverse is open-licensed (CC-BY-SA 4.0). The earlier logs said "FTN is paid, not used"; that applies to FTN's own site. Rico or Ghost6 should confirm the nflverse copy is acceptable as a source.
