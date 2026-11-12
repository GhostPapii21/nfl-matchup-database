# JAX @ BAL final audit — findings

- Confirmed Final via sports-leader `get_scoreboard`/`get_game_summary` + ESPN summary refresh: **JAX 33 – BAL 10** at **2026-11-05 23:14:40 ET** (America/New_York).
- Linescores (independent Q pts): JAX **10 | 7 | 3 | 13** · BAL **3 | 0 | 0 | 7**
- No new paid odds. No historical reconstruction of missing lines.

## Possessions / TOP / 3rd / RZ (audited)

| Team | Drives | TOP drive-sum | Box TOP | 3rd derived | Box 3rd | RZ trips | RZ TD | RZ FG | Box RZ (Made-Att) | No-play pens |
|------|-------:|---------------|---------|-------------|---------|---------:|------:|------:|-------------------|-------------:|
| JAX | 12 | 29:15 | 29:15 | 4/12 | 4-12 | 4 | 2 | 2 | 2-4 | 3 |
| BAL | 12 | 30:45 | 30:45 | 4/14 | 4-14 | 0 | 0 | 0 | 0-0 | 6 |

### Source vs derived
- TOP: **match** both teams.
- 3rd-down: **match** both teams after excluding No Play from denom and forcing INT ≠ conversion.
- INT on 3rd (prior false-conversion path): 1 row(s); now `converted=0`.
  - Q3 13:49 BAL 3rd & 14: converted=0 — (Shotgun) J.Fagnano pass short left intended for Z.Flowers INTERCEPTED by M.Brown at BLT 32. M.Brown to BLT 26 for 6 yards (J.Hill).
- NA_NO_PLAY 3rd rows excluded from denom: 2
- RZ: trip = yte 1–20 (timeouts/yte=0 excluded). FG separate from TD. BAL never entered RZ. JAX 2 TD + 2 FG on 4 trips (= box 2-4).
- BAL Q1 53-yd FG was **not** an RZ trip.

## Period lines cleared (FanDuel / DraftKings) — saved snaps only

Grading uses independent Q scores: Q1 10-3 · Q2 7-0 · Q3 3-0 (JAX–BAL).

| Period | Book | Market | Side | Line | Price | Snap | last_update_utc | Result |
|--------|------|--------|------|------|------:|------|-----------------|--------|
| Q1 | draftkings | h2h_q1 | Baltimore Ravens | ML | 195 | pregame/r6_odds_jaxbal_game | 2026-11-04T19:59:15Z | **L** |
| Q1 | draftkings | h2h_q1 | Jacksonville Jaguars | ML | -238 | pregame/r6_odds_jaxbal_game | 2026-11-04T19:59:15Z | **W** |
| Q1 | draftkings | spreads_q1 | Baltimore Ravens | 2.5 | 102 | pregame/r6_odds_jaxbal_game | 2026-11-04T19:59:15Z | **L** |
| Q1 | draftkings | spreads_q1 | Jacksonville Jaguars | -2.5 | -122 | pregame/r6_odds_jaxbal_game | 2026-11-04T19:59:15Z | **W** |
| Q1 | draftkings | totals_q1 | Over | 7.5 | 105 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:04Z | **W** |
| Q1 | draftkings | totals_q1 | Under | 7.5 | -125 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:04Z | **L** |
| Q1 | fanduel | h2h_q1 | Baltimore Ravens | ML | 198 | pregame_post_inactives/r6_fd_post_inactives_1902 | 2026-11-06T00:03:30Z | **L** |
| Q1 | fanduel | h2h_q1 | Jacksonville Jaguars | ML | -250 | pregame_post_inactives/r6_fd_post_inactives_1902 | 2026-11-06T00:03:30Z | **W** |
| Q1 | fanduel | spreads_q1 | Baltimore Ravens | 2.5 | -102 | pregame_post_inactives/r6_fd_post_inactives_1902 | 2026-11-06T00:03:30Z | **L** |
| Q1 | fanduel | spreads_q1 | Jacksonville Jaguars | -2.5 | -120 | pregame_post_inactives/r6_fd_post_inactives_1902 | 2026-11-06T00:03:30Z | **W** |
| Q1 | fanduel | totals_q1 | Over | 7.5 | 112 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:16Z | **W** |
| Q1 | fanduel | totals_q1 | Under | 7.5 | -138 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:16Z | **L** |
| Q2 | draftkings | h2h_q2 | Baltimore Ravens | ML | 210 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:04Z | **L** |
| Q2 | draftkings | h2h_q2 | Jacksonville Jaguars | ML | -280 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:04Z | **W** |
| Q2 | draftkings | spreads_q2 | Baltimore Ravens | 3.5 | -120 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:04Z | **L** |
| Q2 | draftkings | spreads_q2 | Jacksonville Jaguars | -3.5 | -110 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:04Z | **W** |
| Q2 | draftkings | totals_q2 | Over | 12.5 | -140 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:04Z | **L** |
| Q2 | draftkings | totals_q2 | Under | 12.5 | 110 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:04Z | **W** |
| Q2 | fanduel | h2h_q2 | Baltimore Ravens | ML | 225 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:16Z | **L** |
| Q2 | fanduel | h2h_q2 | Jacksonville Jaguars | ML | -290 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:16Z | **W** |
| Q2 | fanduel | spreads_q2 | Baltimore Ravens | 3.5 | -114 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:16Z | **L** |
| Q2 | fanduel | spreads_q2 | Jacksonville Jaguars | -3.5 | -108 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:16Z | **W** |
| Q2 | fanduel | totals_q2 | Over | 12.5 | -134 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:16Z | **L** |
| Q2 | fanduel | totals_q2 | Under | 12.5 | 110 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:16Z | **W** |
| Q3 | draftkings | h2h_q3 | Baltimore Ravens | ML | 165 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:04Z | **L** |
| Q3 | draftkings | h2h_q3 | Jacksonville Jaguars | ML | -215 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:04Z | **W** |
| Q3 | draftkings | spreads_q3 | Baltimore Ravens | 2.5 | -115 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:04Z | **L** |
| Q3 | draftkings | spreads_q3 | Jacksonville Jaguars | -2.5 | -115 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:04Z | **W** |
| Q3 | draftkings | totals_q3 | Over | 7.5 | 105 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:04Z | **L** |
| Q3 | draftkings | totals_q3 | Under | 7.5 | -135 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:04Z | **W** |
| Q3 | fanduel | h2h_q3 | Baltimore Ravens | ML | 198 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:16Z | **L** |
| Q3 | fanduel | h2h_q3 | Jacksonville Jaguars | ML | -250 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:16Z | **W** |
| Q3 | fanduel | spreads_q3 | Baltimore Ravens | 2.5 | -104 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:16Z | **L** |
| Q3 | fanduel | spreads_q3 | Jacksonville Jaguars | -2.5 | -118 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:16Z | **W** |
| Q3 | fanduel | totals_q3 | Over | 7.5 | 106 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:16Z | **L** |
| Q3 | fanduel | totals_q3 | Under | 7.5 | -128 | pregame/r2_odds_jaxbal_game | 2026-11-04T00:14:16Z | **W** |

### Availability notes (NA where absent)
- **Q2/Q3 spreads, totals, ML**: in early **r2** FD/DK `odds_jaxbal_game` / snapshots (pregame ~2026-11-04T00:14Z). Later **r6** pulls mostly Q1/H1 only.
- **Q1**: FD+DK in r2/r6; FD also same-day 17:35Z and post-inactives ~00:03:30Z.
- **In-play Q1/Q2/Q3**: **NA_NO_INPLAY_PERIOD_SNAP** (none saved; no new pull). Marked in full ledger.
- Full ledger: `period_lines_cleared_ledger.csv`. Concise Q1–Q3: `period_q1_q2_q3_fd_dk_cleared.csv`.

## QB / targets (box facts; no coverage inference)
- Trevor Lawrence: 16/26, 242 yds, 1 TD, **0 INT**, **0 sacks**.
- Joe Fagnano: 10/18, 60 yds, 0 TD, **2 INT**, **1 sack (−2)**. Henry trick pass 1/1, −3.
- JAX targets: Washington **7** (2 REC / 61 / 1 TD / long 50) · Meyers **6** (4 / 65 / long 18) · Boerkircher 3 · Strange **2/2/22** · Koziol 2 · Rodriguez 2 · Allen 0/2 · Hunter 1 · Cameron 1.
- Strange vs other TEs: Strange 2/2/22; Boerkircher 2/3/61 (52-yd chunk); Koziol 2/2/15. Strange volume low; chunk TE play was Boerkircher.
- Meyers long 18 → no explosive (≥20) reception; Washington 50-yd TD and Boerkircher 52-yd are the primary chunk completions.
- Do **not** infer drops from incompletes, beaten CB from tackler, or coverage from pass direction.

### Explosive completed passes (PBP flags / ≥20 yds)
- Q1 tgt=N.Boerkircher yds=52 — T.Lawrence pass deep right to N.Boerkircher to BLT 21 for 52 yards (M.Humphrey).
- Q2 tgt=P.Washington yds=50 — (No Huddle, Shotgun) T.Lawrence pass deep left to P.Washington for 50 yards, TOUCHDOWN. C.Little extra point is GOOD, Ce

## BAL Q4 run/pass sequence (offensive snaps)

| Clock | Kind | Text |
|------:|------|------|
| 13:35 | OTHER | C.Little kicks 62 yards from JAX 35 to BLT 3. J.Hill to BLT 29 for 26 yards (J.Tavai). |
| 13:28 | PASS | (Shotgun) J.Fagnano pass short left intended for Z.Flowers INTERCEPTED by J.Lewis at BLT 27. J.Lewis to BLT 23 for 4 yards (Z.Flowers). |
| 11:52 | OTHER | C.Little kicks 61 yards from JAX 35 to BLT 4. L.Wester to BLT 31 for 27 yards (J.Mcleod).Jacksonville challenged the runner was down by contact ruling, and the  |
| 7:26 | OTHER | C.Little kicks 65 yards from JAX 35 to end zone, Touchback to the BLT 35. |
| 7:15 | RUN | (Shotgun) C.Vinson reported in as eligible.  J.Hill right tackle for 65 yards, TOUCHDOWN. J.Moody extra point is GOOD, Center-N.Moore, Holder-R.Eckley. |
| 4:52 | RUN | (Shotgun) J.Hill right tackle to BLT 16 for 3 yards (D.Striggow). |
| 4:17 | RUN | (Shotgun) J.Hill right tackle to BLT 17 for 1 yard (J.Tavai). |
| 3:35 | PASS | (Shotgun) J.Fagnano pass short left to L.Wester pushed ob at BLT 31 for 14 yards (M.Brown) [Jar.Jones]. |
| 3:27 | RUN | (Shotgun) J.Hill right tackle to BLT 30 for -1 yards (J.Tavai, B.Combs). |
| 2:46 | RUN | (Shotgun) D.Henry left end to BLT 32 for 2 yards (A.Regis; B.Combs). |
| 2:02 | RUN | (Shotgun) J.Fagnano scrambles left end to BLT 41 for 9 yards (B.Combs). |
| 1:53 | OTHER | Two-Minute Warning |
| 1:53 | RUN | J.Hill right tackle to BLT 46 for 5 yards (D.Striggow; B.Combs). |
| 1:15 | RUN | (Shotgun) J.Hill right end to BLT 47 for 1 yard (J.Tavai). |
| 0:30 | RUN |  (Shotgun) J.Hill left tackle to BLT 49 for 2 yards (B.Combs). |
| 0:00 | OTHER | END GAME |

Q4 BAL classified: **RUN 9 / PASS 2** (excl. timeouts). Descriptive only.

### INT timeline
- Q3 13:49 (BAL drive #10): (Shotgun) J.Fagnano pass short left intended for Z.Flowers INTERCEPTED by M.Brown at BLT 32. M.Brown to BLT 26 for 6 yards (J.Hill).
- Q4 13:28 (BAL drive #18): (Shotgun) J.Fagnano pass short left intended for Z.Flowers INTERCEPTED by J.Lewis at BLT 27. J.Lewis to BLT 23 for 4 yards (Z.Flowers).

