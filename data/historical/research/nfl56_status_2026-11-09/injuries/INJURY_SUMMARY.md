# BUF @ MIN injuries / inactives (research only)
Pulls (ET, 2026-11-09):
- ESPN injuries API: 15:01:35, feed ts 2026-11-09T20:01:34Z (15:01 ET), sha256 a9aa5064ea48…
- ESPN game summary 401873051: 15:01:44.
- NFL.com /injuries/league/2026/reg9: 15:02.
- Official team final reports read via web search at about 15:05:
  - Bills, published Nov 7 2:10 PM ET, plus the buffalobills.com injury-report table.
  - Vikings (vikings.com), published Nov 7 1:15 PM ET.

**Official 90-min inactives: NOT_YET.** They are due about 6:45 PM ET and were not posted at 15:05 ET.

## CONFIRMED OUT (official Saturday final report; multiple sources agree)
| Team | Player | Pos | Injury | Thu/Fri/Sat |
|---|---|---|---|---|
| MIN | Kyler Murray | QB | Hamstring (Grade 2 per whynfl, unverified tier) | DNP/DNP/DNP |
| MIN | Jauan Jennings | WR | Calf | LP/DNP/DNP |
| MIN | Demond Claiborne | RB | Knee | LP/DNP/DNP |
| BUF | Joshua Palmer | WR | Hamstring | DNP/DNP/DNP |

## Reserve lists (not active unless activated by Monday afternoon; officially listed QUESTIONABLE)
| BUF | Jordan Hancock | DB/CB | Hamstring; IR, 21-day window opened this week | LP/LP/LP; Q |
| BUF | Tyrell Shavers | WR | Knee (ACL); reserve/PUP, window opened Oct 28 | FP/FP/FP; Q |
No activation for either was found as of 15:05 ET. That is not proof none happened; re-check at inactives.

## QUESTIONABLE (official)
| BUF | Dion Dawkins | LT | Ribs | DNP/DNP/DNP (backup LT Tylan Grable per Bills site) |
| BUF | Alec Anderson | LG (Bills: C/G; NFL.com: G) | Ankle | DNP/DNP/LP (backup Austin Corbett) |
| BUF | Greg Gaines | DL | Calf | DNP/DNP/LP |
| MIN | Theo Jackson | S | Quad | DNP/DNP/LP |
| MIN | Jay Ward | S | Knee | LP/LP/LP |

## No designation / other notes
- BUF: Spencer Brown (RT), DJ Moore, Keon Coleman, Dalton Kincaid and Khalil Shakir have no designation.
- MIN: Darrisaw, Van Ginkel, Golday and Rodgers have no designation and are expected to play (vikings.com).
- MIN QB: Carson Wentz starts and Max Brosmer backs up (ESPN notes citing Rapoport and Alec Lewis; vikings.com preview).
- Odell Beckham Jr. was signed to MIN's 53-man roster: ESPN 2026-11-08T16:15Z (11:15 AM ET), Pelissero.
- DeeJay Dallas (RB) was signed to MIN's active roster Wednesday.

## Feed conflicts
1. **Shavers:** ESPN `status=Out` (type "Knee - ACL", dated 2026-11-07 4:01 PM ET), yet ESPN's own comment says "listed as questionable." NFL.com and Bills say **Questionable**. Official wins: Q, pending PUP activation.
2. **Hancock:** ESPN says `Injured Reserve`; NFL.com and Bills say **Questionable**. Both are true: he's on IR with a practice window and needs activation to play.
3. **Alec Anderson's position:** ESPN says OT (BetGuru followed it). Bills say C/G and the Bills article says "LG", while NFL.com says G. So only one questionable Bills starter is a tackle (Dawkins).
4. **Theo Jackson:** missing from ESPN's league-wide injuries feed, but present in the ESPN game summary (dated Nov 1) and on official reports as Q.
5. **Greg Gaines:** official Q and ESPN league feed Q (dated Nov 3), but missing from the ESPN game summary and from BetGuru's list.
6. **thighdoctor.com** calls Claiborne "questionable", which contradicts the official OUT. It's a low-tier source and was ignored.
7. **Line context (not priced):** all DK via ESPN.
   - 03:11 ET (GitHub board): BUF -3, total 43.5.
   - About 12:17 ET (BetGuru): -3, 44.5, ML -185/+154.
   - 15:01 ET (this pull): **BUF -3.5, total 45.5**.

## BetGuru assertions (ESPN, ~12:17 PM ET): verification
| Assertion | Verdict |
|---|---|
| MIN Kyler Murray QB OUT | VERIFIED (official) |
| MIN Jauan Jennings WR OUT | VERIFIED |
| MIN Demond Claiborne RB OUT | VERIFIED |
| MIN S Jay Ward Q | VERIFIED |
| MIN S Theo Jackson Q | VERIFIED (official; absent in ESPN league feed) |
| BUF Joshua Palmer WR OUT | VERIFIED |
| BUF Tyrell Shavers WR OUT | **CONFLICT**: official = Questionable (on PUP, needs activation); "OUT" is ESPN's status field only |
| BUF CB Jordan Hancock IR | PARTIAL: on IR, but official game status = Questionable (activation possible) |
| BUF OTs Dion Dawkins and Alec Anderson Q | PARTIAL: both Q, but Anderson is a guard (LG), not an OT |
| (omitted) BUF DL Greg Gaines Q | MISSING from BetGuru list |

## nflsavant.com (user-supplied, pt1059u): what it offers
- It's a client-rendered single-page app. The homepage HTML (`injuries/nflsavant_home.html`, 15:02 ET) has no data.
- Its public JS bundle lists pages for games, matchups, players, teams, leaderboards, usage, WR/QB routes, OL grades, referees, coaches, combine, fantasy opportunity and a weather-splits panel.
- No injury, inactive or depth-chart feed was found.
- The data loads from the site's own undocumented JSON `/api/...` endpoints. Per the hard rule against private/undocumented APIs, those were **not called**.
- WebFetch of `/matchup/buf-min` returned HTTP 500.
- Status: NOT_USED for injuries. It may serve as a secondary stats cross-check viewed in a browser, but licensing and provenance aren't documented.
