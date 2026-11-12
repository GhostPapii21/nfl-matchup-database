# Defender + route audit (Sat Oct 31 2026, ~7:20 PM ET)
Sources:
- PFR advanced defense: https://www.pro-football-reference.com/years/2026/defense_advanced.htm. The fresh pull returned 403, so this uses the cached copy from Oct 29 6:02 AM ET (pfr_def_adv_2026.html / .csv here).
- ESPN Week 8 WR/CB cheat sheet (routes, LWR/Slot/RWR alignment %, targets per route, defender alignment): https://g.espncdn.com/s/ffldraftkit/26/NFL26_CS_WRCB.pdf (espn_wrcb.txt).
- Season routes and targets per route: SumerSports https://sumersports.com/players/wide-receiver/
- Shadow note: Fantasy Points https://www.fantasypoints.com/nfl/articles/2026/week-8-wr-cb-fantasy-football-matchups
- Alignment match: StatRankings https://statrankings.com/nfl/wr-cb
Route TYPES (tree %) were not found in any free public source. The PFR-cached rule applies to every leg.

| Leg | Routes / alignment | Mapped defender: PFR allowed (Tgt-Cmp-Yds-TD, rating) | Verdict |
|---|---|---|---|
| Nacua 70+ rec yds | 169 routes; RWR 52 / slot 24 / LWR 24; 35% targets per route (ESPN); 181 routes, 0.34 TPRR (Sumer) | Donte Jackson (LCB, Q hamstring): 9-6-69-0, 89.6. If he sits: Cam Hart 16-10-167-0, 71.6. Tarheeb Still 11-5-71-1, 97.2 | Data PASS. Puka is a DNP Friday (rest); Jackson is Q. |
| Bowers 6+ rec | 168 routes; slot 57%; 28% targets per route (ESPN) | D'Angelo Ponds (slot CB, 100% slot): 0-0-0 in PFR (3 G, 0 starts; ESPN shows 32 routes covered). Underneath LB Jamien Sherwood 18-15-163-1, 122.9 | Data PASS (thin sample on Ponds) |
| Metcalf 40+ rec yds | 280 routes; LWR 47 / slot 21 / RWR 32; 20% targets per route (ESPN); 288 routes, 0.20 TPRR (Sumer) | Tyson Campbell (RCB 95%): 12-9-179-0, 116.7. Possible Denzel Ward shadow: 25-10-142, 82.0; Metcalf has 1-15 on 7 targets vs Ward over 2 games (Fantasy Points) | Data PASS but shadow risk -> flagged |
| McBride 7+ rec | No public TE alignment or route split found (the ESPN WR/CB sheet excludes TEs; its TE sheet returns 404) | Cannot map a defender with alignment evidence | CUT (route/defender data missing) |
