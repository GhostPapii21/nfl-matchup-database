# QB behavior log

Tendencies seen in games (tunnel vision, progression, pressure reactions). Numbers from ESPN box scores.

## Bryce Young (CAR), 2026-10-29 @ GB, snapshot 2:33 Q4, GB 27-19
- Line: 22/39, 200 yds, 5.1 YPA, 1 TD, 1 INT, 5 sacks (-29). Through 12:12 Q4 he was 14/27 for 117.
- Lock-on (user observed live): he looked for McMillan all game. McMillan had 10 targets (about 26% of 39 attempts) but only 5 catches for 50 yds (50% catch rate). Forced looks to his WR1 are inefficient.
- Under pressure he checks down to the RB: Hubbard 8 targets, 7 catches, 38 yds.
- Coker was frozen out until late (0 catches on 3 targets through Q3), then 2 catches for 35 and a TD in garbage time.
- Model use:
  - McMillan targets/receptions: volume is reliable, so target-based overs are fine.
  - McMillan yards: risky against pressure or blitz. A low catch rate means fade yards and big rec rungs.
  - Young passing yds/completions: under against heavy-blitz defenses, stronger with a depleted CAR OL.
  - Hubbard receptions: a solid floor.
  - Secondary WRs: only late garbage-time production.

### Play-by-play check (ESPN PBP, every CAR dropback, through 2:33 Q4; raw at week8/tnf/raw/car_dropbacks.txt)
- Depth: every attempt was "short" except 1 deep throw (Q3 4:55, deep left to McMillan, incomplete). He never pushed the ball downfield.
- McMillan's 10 targets: 2 in the 1st half, 8 in the 2nd half. 5 catches for 50 yds, long of 14. 4 of his 5 incompletions came in the 2nd half, including the 4th & 5 at 2:46 Q4. B. Cisse is the GB defender named on 3 of his targets.
- On 3rd/4th down, Young spread the ball: Hubbard 3 (1 was a no-play), Tremble 2, Waller 2, Coker 2 (INT and 26-yd TD), Metchie 1, Tremayne 1, McMillan 1 (incomplete). He was sacked twice and threw 3 unaimed incompletions. McMillan was NOT his money-down read.
- Pressure: 5 sacks (D.Wyatt, B.Cox, T.Hopper, L.Van Ness, B.Sorrell), 2 on 3rd down.
- T.Hopper (GB) was the defender of the game: INT (on a Coker target), sack, 2 PBUs, 7 or more tackles on short throws.
- Verdict: the user's read is PARTLY confirmed. McMillan was the top target (10 of 39, 26%) and was forced the ball in the 2nd half, but in the 1st half Young spread it short to Hubbard and the TEs. Every throw was short, and the money-down throws went to the RB and TEs, not McMillan. Main tendency: short, quick throws under pressure; lock onto McMillan on early downs in the 2nd half.


## Deshaun Watson (CLE) and Aaron Rodgers (PIT), 2026 Wk4 PIT@CLE (CLE 27-24). Source: ESPN PBP
- Watson: 24/33, 268 yds, 2 sacks, 3 QB-hit plays, 7 rushes for 22 yds. Scrambles: 3rd&4 left end for 21 (+ holding on Samuel); 3rd&9 right end for 2 with a fumble he recovered. Designed or other runs: right end 7, up the middle -5 (fumble, Watt), up the middle 1. Checkdown: Judkins (6-42, all short) and Concepcion short left. After pressure, he went to Boston 3 of 8.
- Rodgers: 45 dropbacks, 5 sacks (-30), 5 hit plays, 0 scrambles. On 3rd down he looked to Metcalf (3 of 9); after pressure he went to R. Wilson and Warren (3 of 12 each).
- Blitz and hurry are NOT in the PBP; proxies are sack, [hit] and scramble. Season 3rd-down and vs-blitz target shares: unknown (not public).
### Pressure / 3rd-down tree / 3rd-down tree (pressure proxies = sack, [QB hit], scramble; blitz/hurry NOT in PBP)

### PIT: 45 dropbacks counted (49 incl. nullified); sacks 5; QB-hit plays 5; scrambles 0

| Q | clk | D&D | score | play | hit by | tag |
|-|-|-|-|-|-|-|
| 1 | 12:04 | 3rd & 11 | PIT 0-CLE 0 | D.Metcalf short right rec 15 | — | 3rd/4th |
| 1 | 10:02 | 3rd & 3 | PIT 0-CLE 0 | D.Metcalf short middle rec 7 | — | 3rd/4th |
| 1 | 6:31 | 2nd & 9 | PIT 0-CLE 0 | SACK -7 (M.Collins) | — | pressure |
| 1 | 5:49 | 3rd & 16 | PIT 0-CLE 0 | M.Pittman short right rec 9 | — | 3rd/4th, next-after-pressure |
| 2 | 10:50 | 3rd & 5 | PIT 7-CLE 7 | D.Metcalf short middle inc 0 | — | 3rd/4th |
| 2 | 6:06 | 3rd & 4 | PIT 7-CLE 14 | SACK -6 (I.McGuire) | — | 3rd/4th, pressure |
| 2 | 1:14 | 1st & 10 | PIT 7-CLE 21 | P.Freiermuth deep left inc 0 | — | next-after-pressure |
| 2 | 0:37 | 1st & 10 | PIT 7-CLE 21 | R.Wilson short right inc 0 [nullified] | J.Verse | pressure |
| 2 | 0:32 | 1st & 10 | PIT 7-CLE 21 | SACK -6 (A.Huntington) [nullified] | — | pressure |
| 2 | 0:26 | 1st & 10 | PIT 7-CLE 21 | R.Wilson short middle inc 0 | A.Huntington | pressure, next-after-pressure |
| 2 | 0:22 | 2nd & 10 | PIT 7-CLE 21 | J.Warren short left inc 0 | — | next-after-pressure |
| 2 | 0:16 | 3rd & 10 | PIT 7-CLE 21 | ? short middle inc 0 | D.Barnett | 3rd/4th, pressure |
| 3 | 13:40 | 3rd & 10 | PIT 10-CLE 21 | J.Warren short left inc 0 | — | 3rd/4th, next-after-pressure |
| 3 | 9:28 | 3rd & 5 | PIT 10-CLE 21 | SACK -3 (A.Huntington) | — | 3rd/4th, pressure |
| 3 | 4:13 | 1st & 10 | PIT 10-CLE 21 | B.Skowronek short left rec 7 | — | next-after-pressure |
| 3 | 2:16 | 1st & 15 | PIT 10-CLE 21 | R.Wilson deep right inc 0 | S.Williams | pressure |
| 3 | 2:12 | 2nd & 15 | PIT 10-CLE 21 | D.Metcalf deep middle inc 0 | A.Huntington | pressure, next-after-pressure |
| 3 | 2:04 | 3rd & 15 | PIT 10-CLE 21 | SACK -10 (M.Hall) | — | 3rd/4th, pressure |
| 4 | 13:07 | 2nd & 8 | PIT 10-CLE 21 | D.Metcalf deep right rec 43 | D.Ward | pressure, next-after-pressure |
| 4 | 12:27 | 1st & 10 | PIT 10-CLE 21 | SACK -4 (S.Williams) | — | pressure |
| 4 | 11:42 | 2nd & 14 | PIT 10-CLE 21 | J.Warren short right rec 13 | — | next-after-pressure |
| 4 | 5:44 | 3rd & 5 | PIT 16-CLE 24 | P.Freiermuth short left inc 0 | — | 3rd/4th |
| 4 | 1:55 | 3rd & 10 | PIT 16-CLE 24 | D.Washington short middle inc 0 | — | 3rd/4th |
| 4 | 1:51 | 4th & 10 | PIT 16-CLE 24 | D.Washington short middle inc 0 [nullified] | — | 3rd/4th |

- 3rd/4th-down target share: D.Metcalf 3/9 (33%), D.Washington 2/9 (22%), M.Pittman 1/9 (11%), ? 1/9 (11%), J.Warren 1/9 (11%), P.Freiermuth 1/9 (11%)
- Under pressure (hit on throw) or next throw after a sack/hit/scramble: R.Wilson 3/12 (25%), J.Warren 3/12 (25%), D.Metcalf 2/12 (17%), M.Pittman 1/12 (8%), P.Freiermuth 1/12 (8%), ? 1/12 (8%), B.Skowronek 1/12 (8%)

### CLE: 37 dropbacks counted (39 incl. nullified); sacks 2; QB-hit plays 3; scrambles 2

| Q | clk | D&D | score | play | hit by | tag |
|-|-|-|-|-|-|-|
| 1 | 13:44 | 3rd & 3 | PIT 0-CLE 0 | I.Bond short left rec 2 | T.Watt | 3rd/4th, pressure |
| 1 | 2:59 | 1st & 10 | PIT 7-CLE 0 | K.Concepcion deep left rec 21 | C.Heyward | pressure, next-after-pressure |
| 1 | 2:21 | 1st & 10 | PIT 7-CLE 0 | D.Boston deep left inc 0 | — | next-after-pressure |
| 1 | 1:36 | 3rd & 9 | PIT 7-CLE 0 | D.Boston deep right inc 0 | — | 3rd/4th |
| 2 | 4:00 | 3rd & 6 | PIT 7-CLE 14 | D.Boston short left rec 9 | — | 3rd/4th |
| 2 | 1:22 | 3rd & Goal | PIT 7-CLE 21 | H.Fannin short right TD 2 | — | 3rd/4th |
| 3 | 10:24 | 3rd & 13 | PIT 10-CLE 21 | Q.Judkins short right inc 0 | — | 3rd/4th |
| 4 | 14:19 | 1st & 10 | PIT 10-CLE 21 | D.Boston deep middle INT 0 | J.Sawyer | pressure |
| 4 | 10:04 | 1st & 10 | PIT 16-CLE 21 | SACK -4 (T.Watt) | — | pressure |
| 4 | 9:26 | 2nd & 14 | PIT 16-CLE 21 | Q.Judkins short left rec 10 | — | next-after-pressure |
| 4 | 8:45 | 3rd & 4 | PIT 16-CLE 21 | SCRAMBLE left end 21 yds (R.Spears-Jennings) +  on PIT-A.Samuel, Defensive Holding, 5 yards, enforced at PI | — | 3rd/4th, pressure |
| 4 | 7:43 | 2nd & 9 | PIT 16-CLE 21 | H.Fannin short left inc 0 | — | next-after-pressure |
| 4 | 7:39 | 3rd & 9 | PIT 16-CLE 21 | SCRAMBLE right end 2 yds (C.Heyward, C.Heyward) | — | 3rd/4th, pressure |
| 4 | 5:18 | 2nd & 9 | PIT 16-CLE 24 | D.Boston short right rec 15 | — | next-after-pressure |
| 4 | 3:47 | 3rd & 8 | PIT 16-CLE 24 | H.Fannin deep left inc 0 | — | 3rd/4th |
| 4 | 0:38 | 2nd & 4 | PIT 24-CLE 24 | SACK -4 (P.Wilson) | — | pressure |
| 4 | 0:19 | 3rd & 8 | PIT 24-CLE 24 | K.Concepcion short right inc 0 | — | 3rd/4th, next-after-pressure |

- 3rd/4th-down target share: D.Boston 2/7 (29%), H.Fannin 2/7 (29%), I.Bond 1/7 (14%), Q.Judkins 1/7 (14%), K.Concepcion 1/7 (14%)
- Under pressure (hit on throw) or next throw after a sack/hit/scramble: D.Boston 3/8 (38%), K.Concepcion 2/8 (25%), I.Bond 1/8 (12%), Q.Judkins 1/8 (12%), H.Fannin 1/8 (12%)



## Baker Mayfield (TB), pre-Wk8 2026 vs ATL. Sources: ESPN PBP plus labeled public data
- 2025 (NGS): vs blitz 50.7% comp (2nd-lowest), 5.2 YPA (lowest); 356 scramble yds under pressure (2nd). 2026 (The Rundown/FTN, 4 games): under pressure 45.8%, 4.3 YPA; vs blitz 62.5%, 7.1 YPA; sack rate 10.8%.
- PBP 2026: 129 dropbacks, 13 sacks, 9 scrambles for 63 yds. 3rd/4th: Egbuka/Godwin 7/33 each. Under pressure or next throw: Egbuka 8/32, Otton 7/32, Irving 6/32.
## Michael Penix Jr. (ATL), pre-Wk8 2026 vs TB
- Muffed (FTN): blitzed 44.7% (2nd); EPA/db 0.09 blitz vs 0.21 no blitz. The Rundown: under pressure 22.7% comp; vs blitz 60%, 8.2 YPA, 0 INT. Scrambles rarely (4 for 11 in PBP).
- PBP 2026: 156 dropbacks, 9 sacks. 3rd/4th: London 19/45, Dotson 7, Pitts 5, Bijan 3. Under pressure or next: London 6/22, Pitts 4, Bijan 3. Bijan 4+ rec: 2/5 with Penix, 3/7 overall.
### Mayfield tree

- Wk1 TB@CIN: dropbacks 36, sacks 4, hit plays 4, scrambles 4 for 31 yds
- Wk2 CLE@TB: dropbacks 40, sacks 3, hit plays 2, scrambles 3 for 26 yds
- Wk3 MIN@TB: dropbacks 42, sacks 6, hit plays 4, scrambles 2 for 6 yds
- Wk7 TB@CAR: dropbacks 11, sacks 0, hit plays 1, scrambles 0 for 0 yds

| wk | Q | clk | D&D | play | result | defender (tackler/PBU) | hit by | tag |
|-|-|-|-|-|-|-|-|-|
| 1 | 1 | 14:23 | 3rd & 1 | E.Egbuka short left | rec 17 | D.Turner | — | 3rd/4th |
| 1 | 1 | 11:22 | 3rd & 4 | C.Godwin short right | rec 5 | B.Cook | — | 3rd/4th |
| 1 | 1 | 9:19 | 3rd & 5 | ? short left | inc 0 | — | M.Murphy | 3rd/4th, pressure |
| 1 | 1 | 6:58 | 2nd & 10 | B.Irving short right | rec 0 | J.Davis; B.Carter | — | next-after-pressure |
| 1 | 1 | 6:18 | 3rd & 9 | SACK |  -8 | sack split by M.Murphy and B.Carter; M.Murphy | B.Carter | 3rd/4th, pressure |
| 1 | 1 | 6:12 | 1st & 10 | SACK |  -4 | K.Jenkins | — | pressure |
| 1 | 1 | 5:41 | 2nd & 14 | C.Otton short middle | inc 0 | — | — | next-after-pressure |
| 1 | 1 | 5:38 | 3rd & 14 | B.Irving short right | rec 7 | B.Cook; B.Cook | D.Lawrence | 3rd/4th, pressure |
| 1 | 1 | 1:42 | 1st & 10 | C.Godwin short left | rec 4 | D.Turner | — | next-after-pressure |
| 1 | 2 | 12:15 | 1st & 5 | SCRAMBLE up the middle |  8 | B.Carter; B.Carter | — | pressure |
| 1 | 2 | 5:26 | 1st & 10 | B.Irving short right | rec -4 | B.Carter | — | next-after-pressure |
| 1 | 2 | 3:56 | 3rd & 3 | C.Godwin short middle | rec 30 | D.Knight | — | 3rd/4th |
| 1 | 3 | 9:13 | 2nd & 9 | SCRAMBLE right end |  6 | D.Hill | — | pressure |
| 1 | 3 | 8:34 | 3rd & 3 | B.Irving short left | rec 22 | B.Cook | — | 3rd/4th, next-after-pressure |
| 1 | 3 | 4:29 | 3rd & 6 | SACK |  -9 | J.Allen | — | 3rd/4th, pressure |
| 1 | 4 | 13:58 | 1st & 10 | B.Irving short left | rec 4 | J.Davis | — | next-after-pressure |
| 1 | 4 | 11:24 | 3rd & 9 | B.Irving short left | rec 11 | J.Battle | — | 3rd/4th |
| 1 | 4 | 10:41 | 1st & 15 | SACK |  -7 | B.Mafe; B.Mafe | B.Mafe | pressure |
| 1 | 4 | 5:11 | 1st & 15 | T.Hurst deep left | rec 16 | D.Hill | — | next-after-pressure |
| 1 | 4 | 4:01 | 1st & 10 | SCRAMBLE left end |  8 | D.Knight | — | pressure |
| 1 | 4 | 3:54 | 2nd & 2 | C.Otton short left | rec 3 | D.Knight | — | next-after-pressure |
| 1 | 4 | 3:19 | 2nd & Goal | SCRAMBLE up the middle |  9 | — | — | pressure |
| 2 | 1 | 12:02 | 3rd & 13 | C.Otton short right | rec 9 | M.Harden; D.Ward | — | 3rd/4th |
| 2 | 1 | 4:09 | 3rd & 4 | K.Gainwell short middle | inc 0 | — | — | 3rd/4th |
| 2 | 1 | 2:28 | 1st & 10 | SACK |  0 | G.Delpit | — | pressure |
| 2 | 1 | 1:53 | 2nd & 10 | C.Otton deep right | inc 0 | — | M.Graham | pressure, next-after-pressure |
| 2 | 1 | 1:48 | 3rd & 10 | SCRAMBLE right end |  14 | M.Harden | — | 3rd/4th, pressure |
| 2 | 1 | 1:19 | 1st & 10 | T.Hurst deep left | INT 0 | M.Harden | — | next-after-pressure |
| 2 | 2 | 12:11 | 3rd & 18 | T.Hurst deep left | rec 21 | T.Campbell | — | 3rd/4th |
| 2 | 2 | 10:21 | 3rd & 7 | SACK |  0 | R.Hickman | — | 3rd/4th, pressure |
| 2 | 2 | 7:08 | 1st & 10 | K.Gainwell short left | rec 2 | M.Harden; Q.Williams | — | next-after-pressure |
| 2 | 2 | 5:18 | 3rd & 15 | SACK |  -6 | M.Graham | — | 3rd/4th, pressure |
| 2 | 2 | 2:00 | 2nd & 9 | E.Egbuka short right | rec 7 | — | — | next-after-pressure |
| 2 | 2 | 0:19 | 3rd & 12 | T.Johnson short left | inc 0 | — | — | 3rd/4th |
| 2 | 3 | 10:20 | 3rd & 9 | SCRAMBLE up the middle |  9 | G.Delpit | — | 3rd/4th, pressure |
| 2 | 3 | 9:33 | 1st & Goal | E.Egbuka short left | TD 5 | — | — | next-after-pressure |
| 2 | 3 | 2:43 | 3rd & 15 | T.Johnson deep right | inc 0 | — | — | 3rd/4th |
| 2 | 4 | 15:00 | 3rd & 8 | T.Hurst deep right | inc 0 | — | — | 3rd/4th |
| 2 | 4 | 10:08 | 3rd & 2 | T.Hurst short right | inc 0 | M.Harden | J.Verse | 3rd/4th, pressure |
| 2 | 4 | 3:44 | 1st & 10 | C.Otton short right | rec 4 | Q.Williams | — | next-after-pressure |
| 2 | 4 | 2:37 | 3rd & 1 | C.Godwin short left | rec 8 | M.Harden | — | 3rd/4th |
| 2 | 4 | 0:33 | 3rd & 14 | SCRAMBLE right end |  3 | C.Schwesinger | — | 3rd/4th, pressure |
| 2 | 4 | 0:22 | 4th & 11 | E.Egbuka deep middle | inc 0 | — | — | 3rd/4th, next-after-pressure |
| 3 | 1 | 9:05 | 3rd & 5 | J.McMillan short left | inc 0 | J.Metellus | — | 3rd/4th |
| 3 | 1 | 1:56 | 3rd & 6 | E.Egbuka short right | rec 4 | I.Rodgers | — | 3rd/4th |
| 3 | 2 | 13:49 | 1st & 10 | SACK |  -7 | K.Van Noy | — | pressure |
| 3 | 2 | 13:00 | 2nd & 17 | C.Godwin short right | inc 0 | — | — | next-after-pressure |
| 3 | 2 | 12:56 | 3rd & 17 | C.Godwin short right | rec 13 | I.Rodgers; J.Metellus | — | 3rd/4th |
| 3 | 2 | 8:42 | 3rd & 2 | C.Otton short right | rec 37 | J.Metellus; E.Wilson | — | 3rd/4th |
| 3 | 2 | 5:41 | 3rd & Goal | K.Gainwell short right | inc 0 | — | — | 3rd/4th |
| 3 | 2 | 3:22 | 2nd & 6 | SCRAMBLE left end |  4 | J.Pierre | — | pressure |
| 3 | 2 | 2:36 | 3rd & 2 | SCRAMBLE up the middle |  2 | D.Turner | — | 3rd/4th, pressure |
| 3 | 2 | 2:00 | 1st & 10 | C.Otton short middle | inc 0 | E.Wilson | — | next-after-pressure |
| 3 | 2 | 1:53 | 3rd & 10 | ? short right | inc 0 | — | — | 3rd/4th |
| 3 | 2 | 0:56 | 1st & 10 | C.Otton deep right | inc 0 | — | A.Van Ginkel | pressure |
| 3 | 2 | 0:52 | 2nd & 10 | E.Egbuka short middle | rec 14 | H.Smith | — | next-after-pressure |
| 3 | 2 | 0:34 | 1st & 10 | SACK |  -5 | sack split by A.Van Ginkel and E.Wilson | — | pressure |
| 3 | 2 | 0:27 | 2nd & 15 | T.Johnson short left | rec 8 | J.Pierre | — | next-after-pressure |
| 3 | 2 | 0:12 | 3rd & 7 | T.Johnson deep left | inc 0 | — | — | 3rd/4th |
| 3 | 3 | 12:34 | 3rd & 9 | E.Egbuka deep middle | inc 0 | — | E.Wilson | 3rd/4th, pressure |
| 3 | 3 | 10:19 | 1st & 10 | C.Otton short middle | rec 5 | J.Metellus | I.Pace | pressure, next-after-pressure |
| 3 | 3 | 9:44 | 2nd & 5 | E.Egbuka short middle | inc 0 | — | — | next-after-pressure |
| 3 | 3 | 9:41 | 3rd & 5 | E.Egbuka short right | inc 0 | — | — | 3rd/4th |
| 3 | 3 | 7:51 | 3rd & 7 | SACK |  -1 | E.Wilson | — | 3rd/4th, pressure |
| 3 | 3 | 5:18 | 2nd & 9 | SACK |  -6 | sack split by I.Pace and K.Van Noy | — | pressure |
| 3 | 3 | 0:40 | 2nd & 5 | C.Godwin short left | rec 3 | E.Wilson | — | next-after-pressure |
| 3 | 4 | 15:00 | 3rd & 2 | SACK |  -2 | sack split by D.Turner and J.Metellus | — | 3rd/4th, pressure |
| 3 | 4 | 13:23 | 1st & 10 | E.Egbuka short middle | rec 21 | J.Metellus | — | next-after-pressure |
| 3 | 4 | 11:33 | 2nd & 19 | SACK |  -10 | B.Cashman | — | pressure |
| 3 | 4 | 10:49 | 3rd & 29 | E.Egbuka short right | rec 10 | J.Metellus; B.Murphy | — | 3rd/4th, next-after-pressure |
| 3 | 4 | 9:46 | 3rd & 16 | C.Godwin short left | rec 9 | B.Cashman; J.Pierre | — | 3rd/4th |
| 3 | 4 | 2:00 | 3rd & 13 | E.Egbuka short right | inc 0 | — | — | 3rd/4th |
| 3 | 4 | 1:54 | 4th & 13 | K.Gainwell short right | INT 0 | A.Van | B.Cashman | 3rd/4th, pressure |
| 7 | 1 | 12:50 | 1st & 10 | B.Irving short middle | inc 0 | D.Brown | D.Lloyd | pressure |
| 7 | 1 | 12:00 | 3rd & 10 | T.Johnson deep right | rec 19 | A.Evans | — | 3rd/4th, next-after-pressure |
| 7 | 2 | 14:18 | 3rd & Goal | T.Hurst short right | inc 0 | B.Okereke | — | 3rd/4th |
| 7 | 2 | 0:59 | 3rd & 2 | C.Godwin short left | rec 5 | B.Okereke | — | 3rd/4th |
| 7 | 3 | 7:15 | 3rd & 13 | C.Godwin short left | rec 9 | T.Wharton | — | 3rd/4th |

- 3rd/4th-down target share: E.Egbuka 7/33 (21%), C.Godwin 7/33 (21%), T.Hurst 4/33 (12%), T.Johnson 4/33 (12%), B.Irving 3/33 (9%), K.Gainwell 3/33 (9%), ? 2/33 (6%), C.Otton 2/33 (6%), J.McMillan 1/33 (3%)
- Under pressure (QB hit on throw) or next throw after sack/hit/scramble: E.Egbuka 8/32 (25%), C.Otton 7/32 (22%), B.Irving 6/32 (19%), C.Godwin 3/32 (9%), T.Hurst 3/32 (9%), K.Gainwell 2/32 (6%), T.Johnson 2/32 (6%), ? 1/32 (3%)


### Penix tree
- Wk3 ATL@GB: dropbacks 25, sacks 0, hit plays 1, scrambles 0 for 0 yds
- Wk4 ATL@NO: dropbacks 21, sacks 1, hit plays 0, scrambles 0 for 0 yds
- Wk5 BAL@ATL: dropbacks 37, sacks 3, hit plays 4, scrambles 2 for 8 yds
- Wk6 CHI@ATL: dropbacks 39, sacks 5, hit plays 3, scrambles 1 for 1 yds
- Wk7 SF@ATL: dropbacks 34, sacks 0, hit plays 0, scrambles 1 for 2 yds

| wk | Q | clk | D&D | play | result | defender (tackler/PBU) | hit by | tag |
|-|-|-|-|-|-|-|-|-|
| 3 | 1 | 10:19 | 3rd & 11 | Z.Branch deep left | inc 0 | — | — | 3rd/4th |
| 3 | 1 | 3:14 | 2nd & 1 | ? short middle | inc 0 | — | L.Van Ness | pressure |
| 3 | 2 | 14:48 | 1st & 10 | Z.Branch short left | rec 7 | E.Cooper; Z.Franklin | — | next-after-pressure |
| 3 | 2 | 11:12 | 3rd & 10 | D.London short right | rec 4 | J.Bullard | — | 3rd/4th |
| 3 | 2 | 5:34 | 3rd & 6 | O.Zaccheaus short right | rec 4 | E.Cooper; K.Nixon | — | 3rd/4th |
| 3 | 2 | 2:00 | 3rd & 1 | D.London deep left | rec 16 | B.Cisse | — | 3rd/4th |
| 3 | 2 | 0:59 | 3rd & Goal | A.Hooper short left | TD 5 | — | — | 3rd/4th |
| 3 | 3 | 5:41 | 3rd & 7 | D.London short middle | rec 16 | X.McKinney | — | 3rd/4th |
| 3 | 4 | 14:17 | 3rd & 2 | D.London deep left | rec 68 | B.Cisse | — | 3rd/4th |
| 3 | 4 | 11:47 | 3rd & 23 | D.London short left | rec 16 | B.Cisse | — | 3rd/4th |
| 4 | 1 | 10:29 | 3rd & 7 | J.Dotson deep right | inc 0 | — | — | 3rd/4th |
| 4 | 1 | 3:49 | 3rd & 6 | SACK |  -8 | T.Wilson | — | 3rd/4th, pressure |
| 4 | 1 | 2:25 | 1st & 10 | Bi.Robinson short left | inc 0 | C.Young | — | next-after-pressure |
| 4 | 2 | 3:14 | 3rd & 7 | O.Zaccheaus short right | inc 0 | — | — | 3rd/4th |
| 4 | 3 | 3:40 | 3rd & 10 | D.London short left | rec 14 | Q.Riley | — | 3rd/4th |
| 5 | 1 | 9:46 | 3rd & 6 | Bi.Robinson short right | inc 0 | T.Robinson | — | 3rd/4th |
| 5 | 1 | 3:24 | 3rd & 7 | SCRAMBLE right end |  5 | K.Hamilton | — | 3rd/4th, pressure |
| 5 | 2 | 10:50 | 3rd & 5 | D.London short right | inc 0 | — | — | 3rd/4th, next-after-pressure |
| 5 | 2 | 7:59 | 1st & 10 | SACK |  -6 | M.Green | — | pressure |
| 5 | 2 | 7:16 | 2nd & 16 | K.Pitts short right | rec 13 | T.Robinson | — | next-after-pressure |
| 5 | 2 | 6:30 | 3rd & 3 | D.London deep right | rec 25 | M.Starks | — | 3rd/4th |
| 5 | 2 | 4:34 | 3rd & 6 | J.Dotson deep right | rec 36 | C.Rivers | — | 3rd/4th |
| 5 | 2 | 2:24 | 3rd & Goal | K.Pitts short middle | TD 5 | — | — | 3rd/4th |
| 5 | 3 | 14:06 | 2nd & 10 | SACK |  -1 | T.Simpson | — | pressure |
| 5 | 3 | 13:23 | 3rd & 11 | K.Pitts short right | rec 13 | K.Hamilton | — | 3rd/4th, next-after-pressure |
| 5 | 3 | 9:59 | 3rd & Goal | J.Dotson short right | inc 0 | — | — | 3rd/4th |
| 5 | 3 | 3:47 | 4th & 2 | C.Woerner short left | inc 0 | — | M.Humphrey | 3rd/4th, pressure |
| 5 | 3 | 0:05 | 3rd & 2 | D.London short left | rec 14 | J.Hawkins | — | 3rd/4th, next-after-pressure |
| 5 | 4 | 13:38 | 3rd & 10 | D.London short right | rec 13 | J.Hawkins | — | 3rd/4th |
| 5 | 4 | 12:24 | 2nd & 18 | SCRAMBLE left end |  3 | K.Hamilton | — | pressure |
| 5 | 4 | 11:35 | 3rd & 15 | D.London deep left | rec 19 | M.Humphrey | — | 3rd/4th, next-after-pressure |
| 5 | 4 | 9:32 | 3rd & 1 | D.London deep right | rec 15 | K.Hamilton | — | 3rd/4th |
| 5 | 4 | 8:15 | 2nd & 9 | K.Pitts deep middle | inc 0 | — | N.Madubuike | pressure |
| 5 | 4 | 8:11 | 3rd & 9 | J.Dotson deep left | inc 0 | — | — | 3rd/4th, next-after-pressure |
| 5 | 4 | 6:23 | 1st & 10 | Br.Robinson short right | inc 0 | — | T.Jones | pressure |
| 5 | 4 | 6:18 | 2nd & 10 | Bi.Robinson short left | inc 0 | — | — | next-after-pressure |
| 5 | 4 | 6:15 | 3rd & 10 | Z.Branch short right | rec 23 | M.Humphrey; R.Smith | — | 3rd/4th |
| 5 | 4 | 2:38 | 3rd & 5 | Bi.Robinson short right | inc 0 | — | — | 3rd/4th |
| 5 | 4 | 0:27 | 1st & 10 | SACK |  -10 | T.Robinson; T.Robinson | T.Robinson | pressure |
| 5 | 4 | 0:13 | 3rd & 6 | ? short left | inc 0 | — | — | 3rd/4th, next-after-pressure |
| 6 | 1 | 6:56 | 3rd & 9 | K.Pitts short right | inc 0 | D.Hardy | — | 3rd/4th |
| 6 | 2 | 15:00 | 3rd & 8 | O.Zaccheaus short left | inc 0 | — | — | 3rd/4th |
| 6 | 2 | 9:29 | 4th & 5 | O.Zaccheaus short right | inc 0 | J.Lynch | — | 3rd/4th |
| 6 | 2 | 5:45 | 3rd & 8 | J.Dotson short left | TD 13 | — | — | 3rd/4th |
| 6 | 2 | 1:05 | 2nd & 10 | SACK |  -10 | D.Hardy | — | pressure |
| 6 | 3 | 14:49 | 1st & 10 | A.Hooper short middle | rec 6 | D.Bush | — | next-after-pressure |
| 6 | 3 | 13:33 | 3rd & 3 | SACK |  -8 | D.Thieneman | — | 3rd/4th, pressure |
| 6 | 3 | 12:03 | 2nd & 9 | SACK |  -6 | K.Gordon | — | pressure |
| 6 | 3 | 11:23 | 3rd & 15 | D.London short right | rec 12 | D.Jackson | — | 3rd/4th, next-after-pressure |
| 6 | 3 | 10:38 | 4th & 3 | D.London short right | inc 0 | J.Johnson | D.Hardy | 3rd/4th, pressure |
| 6 | 3 | 5:41 | 3rd & 6 | SACK |  -8 | K.Gordon; K.Gordon | — | 3rd/4th, pressure |
| 6 | 4 | 14:50 | 1st & 10 | D.London deep left | inc 0 | — | — | next-after-pressure |
| 6 | 4 | 14:42 | 3rd & 10 | D.London short right | inc 0 | D.Thieneman | — | 3rd/4th |
| 6 | 4 | 14:38 | 4th & 10 | Z.Branch short left | rec 5 | C.Lewis | C.Phillips | 3rd/4th, pressure |
| 6 | 4 | 12:12 | 1st & 10 | Br.Robinson short middle | rec 5 | J.Sanborn | — | next-after-pressure |
| 6 | 4 | 9:34 | 3rd & 6 | K.Pitts short left | TD 10 | — | — | 3rd/4th |
| 6 | 4 | 6:37 | 2nd & 10 | SCRAMBLE up the middle |  1 | A.Booker | — | pressure |
| 6 | 4 | 6:10 | 3rd & 9 | K.Pitts short right | rec 10 | C.Lewis | — | 3rd/4th, next-after-pressure |
| 6 | 4 | 3:01 | 3rd & 16 | SACK |  -8 | K.Gordon; K.Gordon; M.Bergeron | K.Gordon | 3rd/4th, pressure |
| 7 | 1 | 2:14 | 3rd & 15 | A.Hooper short middle | rec 10 | D.Lenoir; F.Warner | — | 3rd/4th |
| 7 | 2 | 14:47 | 1st & 10 | SCRAMBLE right end |  2 | F.Warner | — | pressure |
| 7 | 2 | 14:05 | 2nd & 8 | Bi.Robinson short right | rec 15 | J.Jones; M.Mustapha | — | next-after-pressure |
| 7 | 2 | 12:04 | 3rd & 3 | D.London short right | rec 5 | J.Jones; F.Warner | — | 3rd/4th |
| 7 | 2 | 0:33 | 3rd & 4 | J.Dotson short middle | inc 0 | — | — | 3rd/4th |
| 7 | 2 | 0:06 | 3rd & 1 | D.London short left | inc 0 | — | — | 3rd/4th |
| 7 | 3 | 11:19 | 3rd & 7 | D.London short middle | rec 10 | J.Jones; D.Greenlaw | — | 3rd/4th |
| 7 | 3 | 2:26 | 3rd & 3 | Bi.Robinson short right | rec 19 | D.Greenlaw | — | 3rd/4th |
| 7 | 4 | 10:20 | 3rd & 17 | D.London short left | rec 2 | M.Mustapha; J.Brown | — | 3rd/4th |
| 7 | 4 | 4:16 | 3rd & 12 | J.Dotson deep middle | inc 0 | — | — | 3rd/4th |

- 3rd/4th-down target share: D.London 19/45 (42%), J.Dotson 7/45 (16%), K.Pitts 5/45 (11%), O.Zaccheaus 4/45 (9%), Z.Branch 3/45 (7%), Bi.Robinson 3/45 (7%), A.Hooper 2/45 (4%), C.Woerner 1/45 (2%), ? 1/45 (2%)
- Under pressure (QB hit on throw) or next throw after sack/hit/scramble: D.London 6/22 (27%), K.Pitts 4/22 (18%), Bi.Robinson 3/22 (14%), ? 2/22 (9%), Z.Branch 2/22 (9%), Br.Robinson 2/22 (9%), C.Woerner 1/22 (5%), J.Dotson 1/22 (5%), A.Hooper 1/22 (5%)


## Penix (ATL) — pressure target tree (added 2026-10-30, ESPN PBP proxies; see week8/ATL_TB/penix_pressure_targets.md)
- Wk3-7, 156 dropbacks. Under pressure he takes sacks (8 in BAL/CHI) or scrambles; he does NOT check down to Bijan (8-5-10 total in high-pressure games, 0 third-and-long targets).
- Primary read is London: 44% of 3rd-down targets and 45% of 3rd-and-7+ targets. London in pressure games: 19-10-160 (53% catch). #2 read under pressure is Pitts (13-10-102).
- Yards held up in pressure games (240 and 225) because trailing added volume.
