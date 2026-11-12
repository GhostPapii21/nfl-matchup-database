# ESPN standings & leaders — 2026-10-29 1:45 PM ET (ESPN app screenshots supplied by user; ESPN data, not ours)
Raw: espn_standings_leaders_2026-10-29.json

## Diff vs fixes.sqlite (107 final games, Wk1–7) — run 2026-10-29 ~2:05 PM ET
- Records + PF/PA: **32/32 teams match exactly.** CAR ".500" = 3-3 (6 GP; CAR had its bye). No missing games.
- Leaders (pass/rush/rec yds, sacks, INTs): all match exactly. "R. Green SF" = Renardo Green (3 INT).
- Only diff: Fred Warner tackles ESPN 72 vs ours 71 (1 tackle; probably an ESPN stat correction). Not a game gap → no overlay change.
- fixes.sqlite NOT modified (no backup needed).

## CAR@GB script check
- Love passing yds: FD O/U 264.5 (−113/−113), Pinnacle 264.5 (−110/−110). Love: 7 games, 1958 yds, 271 att (7.2 YPA), median 276; range 145–387. Our frame (GB 35 att) → ~250. **Not a clear over → pass.**
- CAR 276 pass yds/g ≈ our 36 CAR att frame already in proj.py → Coker under not contradicted (volume priced; edge is the matchup + Bullard slot coverage).
- McKinney 3 INT / GB +5 TO margin: supports GB control script; no projection change.

## Sunday motivation/script flags (context only, no projection changes)
- LAC 0-6 (L6, 90 PF): trailing-script pass volume; low team totals.
- MIN 6-0 (74 PA, +7 TO diff): opponents in negative script; fade opposing RB rush volume.
- PHI 2-5 L5, LV 3-4 L4 (197 PA, shootout risk), IND L3, WSH 1-4-1, TEN 1-6 (Simmons traded).
- BUF/KC/SF top seeds; SEA allows 233.9 yds/g (best D), so treat SEA opponents' overs with caution.
