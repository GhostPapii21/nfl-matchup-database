# JSN yards vs Darnold pressure — CHI@SEA MNF 2026-11-02
Source: ESPN summary API (event ids per game), play-by-play parsed for JSN targets. "deep" = ESPN pbp text tag (pass deep). QB hits not in ESPN team box -> unavailable.

| Wk | Opp | Sacks-yds | SEA YPA | JSN tgt/rec/yds | YPR | long | short rec/yds | deep rec/yds | 90+? |
|---|---|---|---|---|---|---|---|---|---|
|1|NE|2-12|7.2|11/8/122|15.3|45|7/101|1/21|Y|
|2|ARI|1-16|8.1|10/9/155|17.2|82|8/73|1/82|Y|
|3|WSH|0-0|8.5|15/10/128|12.8|26|7/64|3/64|Y|
|4|LAC|3-20|5.9|6/5/76|15.2|28|4/48|1/28|N|
|5|SF|5-33|4.8|8/5/102|20.4|38|3/29|2/73|Y|
|6|DEN|5-38|4.3|16/12/134|11.2|32|11/102|1/32|Y|
|7|KC|0-0|9.2|12/9/149*|16.6|33|7/94|2/55|Y|
*pbp sum 149; game log 150.

High-sack games (3+: LAC, SF, DEN): avg 104 yds, 2/3 cleared 90, 3/3 cleared 70. Low (0-2): avg 139, 4/4 cleared 90.
Under pressure the shape shifts (DEN: 11 short catches; SF: fewer catches, 2 deep hits) but yards held. Only miss (LAC) was low volume (6 tgts), not pressure.

Local features.json (PFF-derived tgt share): JSN 34.5% overall, 32.1% vs blitz, 25.0% when pressured (n=8 small), 36.1% clean.
wrcb_fresh.txt: JSN (L/slot mix) vs CHI Malik Muhammad; Kupp vs Kyler Gordon (slot).

CHI defense: blitz 41.1% (4th, league median 29.1%) https://muffed.ai/stats/defense-blitz-rate/CHI ; pressure 37.9% (12th), sack rate 8.5% (3rd) https://bearswire.usatoday.com/story/sports/nfl/bears/2026/10/30/bears-defense-evaluation-analytics-through-seven-weeks/92488696007/ ; 19 sacks in 7 (2.7/g), opp pass 8.7 YPA allowed? (team page lists 1689 pass yds, 126/194) https://www.chicagobears.com/team/stats/2026/reg ; NGS: 20th in total pressures (85) https://roundtable.io/sports/nfl/bears/news/bears-defense-ranks-among-the-top-of-the-league-in-havoc-metric
Unavailable (not pulled in time/paywalled): Darnold 2026 comp%/YPA under pressure & vs blitz, time to throw, JSN aDOT/YAC/separation from NGS, CHI yds allowed to WR1/slot, explosive passes allowed.

Read (judgment, not simmed): 70+ ~85-88%; 90+ ~70-75% (7/7 and 6/7 raw, shrunk for sample + CHI blitz-heavy, pressure cuts his target share).
