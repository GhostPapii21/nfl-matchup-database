# 2026 team penalty data: notes (built 2026-11-01 ~9 PM ET, data only; gate, sims and rules untouched)
Source: ESPN public scoreboard + summary endpoints, 119 final games (Weeks 1-8; Week 8 SNF/MNF not final when pulled). Raw JSON is in teams/espn_raw/.
Parser: penparse.py (TDD; tests/test_parser.py, 7 tests: accepted/no-play, declined, offsetting, double spaces, team-only flag, DPI normalization, kickoff "placed at").

## Files
- penalty_plays_2026.csv: 1,985 flags (accepted incl. no-play 1,736, declined 209, offsetting 44 rows), plus a drive_killer column.
- penalties_2026.csv: 238 team-games. Snaps = ESPN box `totalOffensivePlays`, which counts plays run and excludes no-play penalties.
- penalty_rates_2026.csv: 32 teams, per game and per 60 offensive plays.
- xcheck_vs_betguru_by_game.csv, xcheck_drive_killers.csv, penalty_qb_corr.csv.
- Side is relative to the team that had the drive, so a kick-play foul by the receiving team counts as "offense". BetGuru splits those out as special teams.

## Reconciliation against ESPN box totals
228 of 238 team-games match exactly on count and yards (1,736 vs 1,739 flags). The 10 that are off by 1 flag or a few yards: W2 GB, CIN, LAC, KC; W4 PIT (yards only); W6 CAR, PHI, KC; W7 MIA, CAR. These look like ESPN text-vs-box inconsistencies (foul credited to the other team, or re-enforced yardage).
Sanity checks: W8 KC 11-105 ✓. W8 LAR 8-40 ✓, with 4 false starts (+1 illegal shift declined).

## Cross-check vs BetGuru's penalties/penalties_2026.csv (not edited)
- BetGuru accepted + no-play = 1,455 vs box 1,739. Its README now says 294 off (397 before its fixes). The causes:
  1. It keeps ESPN's text abbreviations ARZ/BLT/CLV/HST, so those teams' flags never join the box rows (ARI/BAL/CLE/HOU). This is most of the gap.
  2. It catches only 1 of the 29 kickoff "placed at" fouls.
  3. 31 rows whose text says declined are coded accepted/no-play.
- 56 team-games differ from mine (listed in xcheck_vs_betguru_by_game.csv).
- Drive killers: mine 593 vs BetGuru 418, differing in 99 team-games. The causes are the same alias issue, BetGuru excluding special-teams plays, and my rule counting every accepted foul by the drive's team on any drive without a TD or FG. **The flags don't line up, so I did not merge BetGuru's flag.**

## Correlation: offensive penalties vs QB completions and passing-yard misses
- **Lines:** all are STAND-IN lines, not real. Each is the QB's prior-week median + 0.5 (floor), from nflverse pbp Weeks 1-7 + Week 8 TNF. The runs/ and playlogs graded QB legs are almost all Week 8 and too few to use, so there are 0 real-lined samples. Week 8 Sunday is not in pbp.
- **Sample:** n = 132 QB-games (≥15 attempts, ≥2 prior games).
- **Penalty measures:** all accepted offensive flags (including pre-snap no-plays), pre-snap only (false start/offside + illegal formation/shift/motion), and the rate per 60 plays.
- **Controls:** favorite/underdog (closing spread) and final margin.

| measure | completions: r (miss margin) | partial r | pass yards: r | partial r |
|-|-|-|-|-|
| accepted offensive count | +0.16 | +0.16 | +0.21 | +0.21 |
| pre-snap count | +0.09 | +0.09 | +0.15 | +0.16 |
| per 60 plays | -0.04 | -0.05 | +0.04 | +0.04 |

**Verdict:** there is no usable signal. The small positive r on raw counts is a volume effect: more plays bring more flags and more completions. When the rate is normalized per 60 plays, it goes to about 0, with or without the game-script control. At n = 132 the 90% CI is about ±0.14, so any real effect is small. This matches BetGuru's r = +0.04. Don't build a rule on it. Re-check after Week 12, and with real closing lines.
