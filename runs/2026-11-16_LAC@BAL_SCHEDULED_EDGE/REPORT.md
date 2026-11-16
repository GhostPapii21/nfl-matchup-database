# LAC @ BAL — Week 10 MNF — SCHEDULED RUN (enhanced edge analysis)
Run 2026-11-16 ~8:55 AM ET; Ghost6 vet fixes applied 8:57 AM ET Nov 16. Status: research only, nothing graded as a pick. projection_ready=false (unchanged); no re-sim; gates NFL-49/NFL-56 unmet. No slips. No Odds API credits spent (801 remaining, floor 800).

## 1. Header
- Game: Los Angeles Chargers (0-8) at Baltimore Ravens (4-5), M&T Bank Stadium, outdoors, grass. Kickoff Mon Nov 16, 8:15 PM ET (ESPN).
- Packet: pregame/packets/2026_10_LAC_BAL, built 2026-11-15 9:57 PM ET (commit 4ba7902), about 11 h old, so under 24 h. Built after Saturday's final report and includes ESPN's McConkey OUT. **The packet's listed BAL QB (Huntley) is STALE.** Huntley (toe) and Lamar Jackson (thumb) are both on IR. **Official starter confirmation: Jacoby Brissett.** baltimoreravens.com official depth chart (pulled 8:55 AM ET Nov 16) lists QB1 Jacoby Brissett, QB2 Joe Fagnano, QB3 Kedon Slovis. Official News & Notes (Clifton Brown, Nov 9, 2026 at 5:21 PM ET): "Minter confirmed that the Ravens expect Brissett to be their starter Monday night against the Los Angeles Chargers." Official 50 Words or Less (Clifton Brown, Nov 15, 2026 at 8:55 AM ET): "It will be Brissett's first start for Baltimore." The NFL.com official Week 10 injury report (pulled 8:55 AM ET Nov 16) does not name a starting QB; Brissett is not listed. Sportsnet/CBS (7:57 AM ET Nov 16) also had him starting, used only as secondary. **Every BAL passing and pace baseline in the packet is STALE (built on Huntley/Jackson/Fagnano, not Brissett). Not re-simmed.**
- Book prices: packet has none (SKIPPED_CREDIT_FLOOR, 801 credits vs the 800 floor). No Odds API credits were spent. Public quotes used instead: CBS Sports (Nov 16, 7:57 AM ET), USA Today/BetMGM (Nov 16, 6:54 AM ET), FanDuel Research (Data Skrive, about 4 days old, so STALE), OOSTA Pro line-moves (checked 8:52 AM ET; openers PAYWALLED).
- Weather: NWS, pulled 9:57 PM ET Nov 15. 45°F, NW wind 5 mph, 0% precipitation, mostly clear. No flags.
- Tools: GitHub API (packet, ANALYST_PROMPT), web search/fetch (chargers.com injury report, Sportsnet, CBS, USA Today, FanDuel Research, OOSTA, baltimoreravens.com depth chart and official articles, NFL.com official injury report, NFL Next Gen Stats team trends). PFR pages returned 403 and ESPN pages returned 202 this session (8:55 AM ET Nov 16), so no fresh PFR/ESPN figures were taken.
- Live checks: official QB confirmation, injury report, lines, NGS pass-rush rates. Not checked: PFR splits (blocked), Sharp, NFL.com inactives (they post about 6:45 PM ET; the 6:50 PM ET inactives routine covers them).

## 2. Five-line summary
1. Market (Nov 16 morning): BAL -4.5, total 38.5 to 39, ML BAL -225 / LAC +185 to +190.
2. Biggest news since the packet: Brissett's first BAL start on under a week in the system. McConkey is OUT (didn't travel). Njoku is questionable (21-day window).
3. Script read: a low-volume grind. BAL leans on Henry (73% carry share). LAC protection is still weak on the packet (10.5% sack rate allowed, 19.3% pressure allowed, both FTN/PFR as of 9:57 PM ET Nov 15), but a blitz rate is not pressure: NGS has BAL at 38% pressure when blitzing (28th) and 35% without a blitz (7th).
4. No priced edge survives. Without book prices or props there's no no-vig base for props, and the total and side sit where my read sits.
5. Research watch-list: Henry rush-yards floor (UNPRICED LEAN, not an edge), Herbert sacks over (WATCH), total under (WEAKEN).

## 3. Game script
BAL has 11 days of rest and LAC has 8 plus a west-to-east trip. Under new head coach Jesse Minter (LAC's DC the past two seasons), BAL should script short, quick Brissett throws and lean on Henry. BAL's offense with backup QBs in Weeks 6-9 scored 10, 13, 10, 10. LAC is last in scoring (15.1 per game) and scored 6 and 9 in its last two road games. LAC's run game (Hampton 3.62 YPC) faces BAL's 3.37 YPC allowed (2nd). The likely path is BAL up by one score into the second half, more Henry carries and a shortened game. The other path: LAC's turnovers (Herbert 11 INT) hand BAL short fields, which pushes points up even if yards stay low.

## 4. Breakdown (packet numbers, nflverse/FTN/PFR as of 9:57 PM ET Nov 15)
- **LAC offense:** 15.1 points per game (32nd), 201.9 passing yards (24th), 6.70 yards per attempt, 34.2% on 3rd down (31st), 50% red-zone TDs (26th), 10.5% sack rate allowed (32nd), 19.3% pressure allowed (31st). 62.0 plays per game, 40.7% neutral pass rate. Herbert: 61.8% completions, 6 TD / 11 INT, 31 sacks in 8 games, 8 of them in Week 9.
- **BAL defense:** 26.6 points allowed (26th). WR yards allowed 177.8 per game (29th), RB receiving yards allowed 16.5 (1st), 3.37 YPC allowed (2nd), blitz rate 34.6%, sack rate 5.1% (23rd) — sack rate and blitz rate from the packet (nflverse/FTN/PFR as of 9:57 PM ET Nov 15). NGS team trends (pulled 8:55 AM ET Nov 16, nfl.com/stats/ngs/trends/teams/baltimore-ravens): blitz rate 33% (52nd percentile, 13th), pressure when blitzing 38% (14th percentile, 28th), pressure without a blitz 35% (81st percentile, 7th). Allowed 35, 36 and 33 points in Weeks 7-9. Weakest run gap: left tackle, 5.2 YPC.
- **BAL offense:** 18.5 points per game (27th), 113.5 rushing yards (9th), 8.1% sack rate allowed, 18.5% pressure allowed (29th). **Passing and pace baselines here are STALE (built on Huntley/Jackson/Fagnano, not Brissett).** Henry rushing (not a passing baseline): 151 carries, 545 yards, 3.61 YPC, game log 68 89 73 102 58 45 53 57.
- **LAC defense:** 27.4 points allowed (29th), 105.5 RB rushing yards allowed (23rd), 4.26 YPC, left end 6.55 YPC. TE receptions allowed 4.1 (4th) and RB receptions allowed 3.4 (4th). Allowed 44 and 391 passing yards to HOU in Week 9. Blitz rate 24.7%.
- **Injuries:** LAC: McConkey OUT, Waxter (CB) OUT, Williamson (S) OUT, B. Taylor (G) OUT, B. Thompson (WR) doubtful; Njoku, Perryman, Pipkins, Awosika (starting LG) and Eboigbe questionable (chargers.com). Mack, Henley, Harris, Hart and Mitchell were cleared. BAL: Jackson IR, Huntley IR, Hawkins (S) OUT; Stanley (LT) and Campbell (DT) were DNP in the packet's practice data with no game status listed, so UNKNOWN until inactives.
- **Pass rush vs protection:** LAC's Tuipulotu (12 pressures) and Mack (11) face BAL's 18.5% pressure allowed (packet; **STALE**, built on Huntley/Jackson/Fagnano). On the other side, packet FTN/PFR (9:57 PM ET Nov 15) has LAC pressure allowed 19.3% (31st) and sack rate allowed 10.5% (32nd). A pass-block win rate was not confirmed this session (ESPN 202, PFR 403). NGS does not publish an LAC offensive pressure-allowed or pass-block win rate on the team-trends page. BAL's Mike Green (10 pressures, 3.5 sacks) plus a Roquan Smith/Simpson blitz package faces that weak LAC protection, but NGS has BAL converting blitzes to pressure at only 38% (28th).

## 5. Opportunity table (my read; volume ranges built from packet shares)
| Player | Role | Projected volume | Label | Notes |
|---|---|---|---|---|
| D. Henry (BAL RB) | 73% of carries, 34 RZ carries | 18-23 carries | volume-supported / expanding | Passes the 60% gate. Favorite script plus a new QB pushes carries up. Efficiency is weak (3.61 YPC). |
| J. Hill (BAL RB) | 13% of carries, 12% of targets | 3-6 carries, 2-4 targets | efficiency-driven (8.22 YPC on 27 carries) | Under 60%: DO-NOT-PLAY |
| Z. Flowers (BAL WR) | 27% target share, aDOT 6.8 (STALE; built on Huntley/Jackson/Fagnano) | 6-9 targets | volume-supported, QB-dependent | Weeks 8-9 went 0 and 6 yards with Huntley hurt and Fagnano starting. No verified main defender, so not playable. |
| M. Andrews (BAL TE) | 17% target share (STALE; built on Huntley/Jackson/Fagnano) | 3-5 targets | shrinking vs LAC TE defense (4.1 receptions allowed, 4th) | No verified defender |
| T. Harris (LAC WR) | 15% target share, 20% air share | 5-7 targets | expanding (McConkey out) | Yards log 20 53 76 60 16 31 6 is volatile. No verified main defender (Humphrey/Wiggins inferred only). |
| Q. Johnston (LAC WR) | 13% target share, aDOT 14.3 | 4-6 targets | expanding, efficiency-driven | 13 catches on 30 targets |
| O. Gadsden / C. Kolar (LAC TE) | 12% / 9% target share | 3-5 each | expanding if Njoku is out | vs BAL TE yards allowed 57.1 (21st) |
| O. Hampton (LAC RB) | 51% of carries | 12-16 carries | shrinking | Under 60%: DO-NOT-PLAY. Faces the 2nd-ranked YPC defense. |
| Herbert / Brissett passing | n/a | n/a | n/a | Passing yards are banned |

## 6. Brainstorm and critical review
| # | Angle (the number behind it) | Verdict | Reason / case against |
|---|---|---|---|
| 1 | Henry rush floor: 73% share, 8 straight games of 45+, LAC allows 105.5 RB rushing yards | UNPRICED LEAN (not an edge) | Volume-supported, but there is no FD/DK alt price, so it cannot be graded against break-even. No Odds API credits spent (801, floor 800). Against: 3.61 YPC, and BAL's line could miss Stanley. |
| 2 | Herbert sacks over: LAC 10.5% sack rate allowed / 19.3% pressure allowed (packet FTN/PFR, 9:57 PM ET Nov 15) vs BAL sack rate 5.1% (23rd, same packet) and NGS pressure 38% when blitzing (28th) / 35% without (7th), pulled 8:55 AM ET Nov 16 | WATCH (downgraded) | A blitz rate is not pressure. BAL's blitz-to-pressure conversion is 28th, and the sack rate is only 23rd. LAC protection is still weak on the packet, but that is not enough to keep a lean without a market. No pass-block win rate confirmed this session (PFR 403, ESPN 202). No market. No re-sim. |
| 3 | Total under 38.5/39: LAC 15.1 ppg, 2 of 8 LAC games over, BAL backup-QB games 10/13/10/10 | WEAKEN | Both defenses allow 26-27 per game. LAC's turnovers create short fields. The packet samplers lean over (62-74%) but ignore injuries and the QB change. The market already moved 38.5 to 39 toward the over, against this read. Already priced near my read. |
| 4 | LAC WR volume up with McConkey out (10% target share to redistribute) | WEAKEN | Volatile logs, no verified defender, BAL allows 177.8 WR yards. Needs a defender check before it's live. |
| 5 | Flowers bounce-back with a competent QB | WEAKEN | Brissett has under a week in the system, there's no Brissett-Flowers sample, and the defender is inferred. |
| 6 | Andrews receptions under vs LAC (4th in TE receptions allowed) | WEAKEN | No defender, no price, small edge. |
| 7 | BAL side: rest 11 vs 8, LAC 0-8 straight up | DROP | Spread steady at 4.5, which already prices it. No validated side model. numberFire's 70.7% vs 66.7% no-vig is a third-party number, not ours. |
| 8 | LAC run game vs 3.37 YPC allowed | DROP as a leg | Hampton is under 60%: do-not-play. It only feeds the low-LAC-points read. |
| 9 | Minter knows LAC's system | DROP | Can't measure it, and it's a narrative. |

**Strongest case against the overall read (low-scoring BAL grind):** BAL's defense gave up 33+ in three straight games and LAC's 44-point Week 9 allowance shows both units can break. A new QB facing a defense that saw him in Week 1 could turn the ball over and turn this into a sloppy, higher-scoring game.

## 7. Market table
De-vig working (two-sided quotes fetched this session, multiplicative):
- FanDuel ML -230/+190 (STALE, about 4 days old): 0.6970 + 0.3448 = 1.0418, so BAL 66.9% / LAC 33.1%.
- BetMGM ML -225/+185 (Nov 16, 6:54 AM ET, via USA Today): 0.6923 + 0.3509 = 1.0432, so BAL 66.4%.
- CBS ML -225/+190 (Nov 16, 7:57 AM ET): 0.6923 + 0.3448 = 1.0371, so BAL 66.8%.
- FanDuel total 38.5 O -115 / U -105 (STALE): 0.5349 + 0.5122 = 1.0471, so over 51.1% / under 48.9%.
- FanDuel spread -110/-110: 50.0/50.0.

| Market | Our fair | Pinnacle no-vig | FTN | DK | FD | Edge | Best price / BE | Movement | Label | Driver | Kill-switches |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Spread BAL -4.5 | no validated number | MISSING (no credits) | MISSING (gated) | MISSING | -110/-110 (stale) | n/a | n/a | Steady at 4.5 (OOSTA, CBS, FD) | none | n/a | n/a |
| Total 38.5-39 | lean under, about 38-39 (my read) | MISSING | MISSING | MISSING | U -105, 48.9% NV (stale) | not quantifiable | n/a | 38.5 to 39 (CBS/OOSTA, Nov 16 AM), toward the over | none (WEAKEN) | QB downgrade, LAC offense | 40+ or Stanley out |
| ML | n/a | MISSING | MISSING | MISSING | BAL 66.9% NV | n/a | n/a | -225 to -230 range | none | n/a | n/a |
| Henry rush yds | median about 70 on 18-23 carries (packet wtd 70.3, median 67.3, p15 56.8; my adjustment: more carries, flat) | no market data | MISSING | no market data | no market data | n/a (cannot grade vs break-even until a real FD/DK alt price exists; no credits spent, 801 / floor 800) | n/a | n/a | UNPRICED LEAN (not an edge) | injury-adjusted volume | Henry limited/inactive, Stanley out, BAL trailing by 10+ |
| Herbert sacks | no new projection (no re-sim); prior "about 3" was my unsourced read only | no market data | MISSING | no market data | no market data | n/a | n/a | n/a | WATCH | LAC protection (packet) vs weak BAL blitz-to-pressure (NGS 28th) and 5.1% sack rate (23rd) | Awosika active and LAC ditching dropbacks for a quick game |

Movement: the true opener is PAYWALLED (OOSTA Pro). No odds-freeze snapshot was found for this game. The spread holding at 4.5 through the Brissett news (announced Nov 9 per NBC/Rotoworld) suggests the QB change was priced early. Public betting %: not used.

## 8. Projections (research)
- Game: research range BAL by 3-7 with a total around 33-41 (my read: BAL backup-QB scoring of 10-13 plus LAC's road 6-9 offset by both defenses' 26-27 allowed). The packet's samplers (45.0 / 43.1, BAL +1.2 / +3.8) are pre-injury, pre-QB-change and unvalidated, so not used.
- Henry: packet weighted mean 70.3, my read about 70 (+carries from script, -efficiency). Harris: packet 38.6, my read a little higher on targets with McConkey out, variance wide. Flowers: packet 62.2, but the QB switch makes it unknown.
- The three 100k-sim models were NOT RUN: gates NFL-49/NFL-56 are unmet, plus the low-usage directive.

## 9. Open items before kickoff
- NFL.com inactives (about 6:45 PM ET): Henry, Stanley, Campbell, Njoku, Awosika, Eboigbe.
- Real prices: Pinnacle/DK/FD main and props. An Odds API pull needs Rico's OK at 801 credits (floor 800). No credits were spent on this vet. Prop lines (Henry rushing yards, Herbert sacks) haven't been seen, so the Henry floor stays an UNPRICED LEAN and cannot be graded against break-even.
- Verified main defenders for every receiving angle (FTN/Sharp) are still missing, so all receiving reads stay estimates.
- Brissett: no BAL snaps, and his Week 1 ARI vs LAC log wasn't pulled.
- The packet should be re-run with the BAL QB set to Brissett.

## 10. Sources and freshness
- Packet brief.md/packet.json (nflverse pbp, rosters, injuries, depth charts, snaps, FTN, PFR, ESPN, NWS): 9:57 PM ET Nov 15.
- ANALYST_PROMPT.md v2: main @4ba7902.
- chargers.com injury report (McConkey out, Njoku and others questionable): checked 8:51 AM ET Nov 16.
- baltimoreravens.com official depth chart: QB1 Brissett, QB2 Fagnano, QB3 Slovis. Pulled 8:55 AM ET Nov 16. https://www.baltimoreravens.com/team/depth-chart
- baltimoreravens.com News & Notes (Clifton Brown), Nov 9, 2026 at 5:21 PM ET: Minter confirmed Brissett is expected to start Monday night. https://www.baltimoreravens.com/news/kyle-hamilton-injury-update-jacoby-brissett-starting-against-chargers-monday-night-minter-lamar-jackson-injury-conversations-private
- baltimoreravens.com 50 Words or Less (Clifton Brown), Nov 15, 2026 at 8:55 AM ET: "It will be Brissett's first start for Baltimore." https://www.baltimoreravens.com/news/jacoby-brissett-leadership-experience-andrew-luck-possible-lineup-changes-derrick-henry-zay-flowers-50-words-ravens-chargers-2026
- NFL.com official Week 10 injury report, pulled 8:55 AM ET Nov 16: does not name a starting QB. BAL OUT Hawkins; QUESTIONABLE Randall. https://www.nfl.com/news/nfl-week-10-injury-report-2026-season and https://www.nfl.com/injuries/
- NFL Next Gen Stats team trends, pulled 8:55 AM ET Nov 16: BAL blitz 33% (13th), pressure when blitzing 38% (28th), pressure without a blitz 35% (7th). https://www.nfl.com/stats/ngs/trends/teams/baltimore-ravens — LAC team-trends page had no offensive pressure-allowed or pass-block win rate.
- PFR team/advanced pages and ESPN win-rate / team-stat pages: attempted 8:55 AM ET Nov 16; PFR returned 403, ESPN returned 202. No figures taken from those attempts.
- Sportsnet / Field Level Media / NBC: Brissett expected to start, Huntley and Jackson on IR. Checked 8:51 AM ET. Secondary to the official team sources above.
- CBS Sports, published 7:57 AM ET Nov 16: BAL -4.5, total 39, ML -225/+190.
- USA Today, 6:54 AM ET Nov 16 (BetMGM): BAL -4.5, total 38.5, ML -225/+185.
- FanDuel Research (Data Skrive, about 4 days old, STALE): -4.5 -110/-110, 38.5 O -115/U -105, ML -230/+190.
- OOSTA Pro line-moves, checked 8:52 AM ET: BAL -4.5, total 39.0, -225. Openers paywalled.

## Slate-wide surviving edges (MNF only)
| Rank | Game | Play | Label | Driver | Status |
|---|---|---|---|---|---|
| 1 | LAC@BAL | Henry rushing-yards floor (alt, at or below about 55) | UNPRICED LEAN (not an edge) | Injury-adjusted volume (73% share) | No FD/DK alt price, so it cannot be graded vs break-even. No credits spent (801, floor 800). Research only. |
| 2 | LAC@BAL | Herbert sacks over | WATCH | Packet LAC pressure/sack-rate allowed vs NGS BAL pressure and 5.1% sack rate | No price. Downgraded: blitz rate is not pressure. Research only. |
| — | LAC@BAL | Total under | WEAKEN, not surviving | — | Market already near my read |
No priced +EV edge found. That's a valid result.

Research only. Not validated. Not betting advice.
