# CHI secondary pass-catchers vs SEA, MNF Nov 2 2026 (written ~2:30 PM ET)
Sources: nflverse pbp (src/play_by_play_2026.parquet, wks 1-7), PFR defense (src/pfr_def_seachi.csv, pulled 5:06 AM ET today, season through wk7), Sharp coverage (src/sharp_cov.md, upd Oct 27), odds.json (5 AM ET pull, stale), public previews (Bears.com, FantraxHQ, RotoBaller, Bears Wire, fetched today).
Targets = pbp pass plays with a receiver (sacks excluded). Caleb games = Wks 1,2,6,7.

## 1. Usage (Caleb games | season 7g)
| Player | Tgt/g | Tgt sh | Rec/g | Catch% | Yds/g | aDOT | RZ tgt | 20+ rec |
|---|---|---|---|---|---|---|---|---|
| Burden (ref) | 6.0 / 6.7 | 20.2% / 21.0% | 5.0 / 5.0 | 83% / 74% | 80.0 / 70.1 | 8.6 / 8.5 | 3 / 9 | 7 / 11 |
| Loveland TE | 6.0 / 6.0 | 20.2% / 18.8% | 3.5 / 3.7 | 58% / 62% | 34.2 / 34.9 | 7.8 / 6.9 | 6 / 10 | 1 / 1 |
| Raymond | 4.5 / 4.4 | 15.1% / 13.8% | 3.8 / 3.7 | 83% / 84% | 35.5 / 34.9 | 4.7 / 6.1 | 2 / 4 | 1 / 2 |
| Odunze | 4.0 / 5.4 | 13.4% / 17.0% | 3.0 / 3.4 | 75% / 63% | 50.8 / 54.4 | 14.9 / 13.3 | 1 / 5 | 6 / 11 |
| Swift (ref) | 3.8 / 3.6 | 12.6% / 11.2% | 3.5 / 3.1 | 93% / 88% | 25.5 / 21.7 | -1.3 / -1.4 | 2 / 2 | 1 / 1 |
Routes/snap share: NOT available (ngs_rec.parquet and part.parquet are empty 9-byte files). Gap.

Caleb game logs tgt/rec/yds (Wk1, 2, 6, 7):
- Burden 5/5/63, 7/3/32, 8/8/95, 4/4/130
- Loveland 2/0/0, 3/1/3, 7/6/65, 12/7/69  (rising: 19 tgt last 2)
- Raymond 9/8/84, 5/5/40, 2/2/18, 2/0/0  (falling)
- Odunze 3/2/52, 4/3/43, 4/3/39, 5/4/69  (steady, deep)
- Swift 1/1/10, 5/5/54, 5/4/26, 4/4/12
CHI WR order by Caleb-game targets: Burden 24, Raymond 18, Odunze 16 (Loveland 24 is TE). Odunze = WR3 -> #3/#4 ban. Raymond = WR2 on totals but 2 tgt in each of last 2.

Ranking (who absorbs "the other" volume):
1. Loveland - co-leads Caleb-game targets (24), 6 RZ targets, 19 tgt last 2; catch rate only 58%, low aDOT.
2. Odunze - fewest targets but deepest aDOT (14.9) and most yards/target; volume capped (WR3).
3. Raymond - high catch rate on short throws, but role collapsed to 2 tgt in Wks 6-7 as Loveland rose.

## 2. Coverage matchups
Alignment data: NOT in FTN (no alignment fields), NGS file empty, PFF unavailable. Proxy only. Seattle plays 90.0% zone / 5.4% man (Sharp, Oct 27, lowest man rate in NFL) -> matchups are by zone area, not shadows.
Likely: Witherspoon (nickel/slot CB) - Bears.com names "Burden vs Witherspoon" as key matchup; Blitz's file cites ESPN putting Witherspoon on Odunze (conflict, unresolved). Jobe = outside CB (likely Odunze/Raymond outside). Loveland: LB Ernest Jones / Drake Thomas, S Emmanwori/Love. Riq Woolen does NOT appear on SEA in PFR 2026 data - do not assume him.

PFR 2026 (7 G, pulled 5:06 AM ET today; data <48h old as a pull, covers thru wk7):
| Defender | Pos | G | Tgt | Rec | Yds | Rec/g | Yds/g | TD | Rate |
|---|---|---|---|---|---|---|---|---|---|
| Devon Witherspoon | CB | 7 | 41 | 26 | 170 | 3.7 | 24.3 | 0 | 72.2 |
| Josh Jobe | CB | 7 | 32 | 23 | 211 | 3.3 | 30.1 | 2 | 97.3 |
| Nehemiah Pritchett | CB | 7 | 15 | 8 | 97 | 1.1 | 13.9 | 0 | 33.9 |
| Ernest Jones | LB | 7 | 38 | 24 | 190 | 3.4 | 27.1 | 0 | 64.6 |
| Drake Thomas | LB | 5 | 17 | 10 | 72 | 2.0 | 14.4 | 1 | 63.8 |
| Nick Emmanwori | S | 6 | 17 | 9 | 74 | 1.5 | 12.3 | 0 | 64.3 |
| Rodney Thomas II | S | 7 | 15 | 8 | 92 | 1.1 | 13.1 | 1 | 94.3 |
| Julian Love | S | 6 | 13 | 5 | 50 | 0.8 | 8.3 | 0 | 10.6 |
Yds/coverage snap: not available (PFF only). Second-source cross-check per defender: not done (StatRankings/FTN defender data not found); Sharp only gives team scheme. Jobe is the softest CB (97.3 rate, 2 TD, 9.2 yds/cmp).

## 3. SEA allowed by position (pbp, defteam SEA)
| Wk | Opp | WR tgt/rec/yds | TE tgt/rec/yds | RB tgt/rec/yds | 20+ rec (WR) |
|---|---|---|---|---|---|
| 1 | NE | 19/12/97 | 4/4/28 | 8/7/53 | 0 |
| 2 | ARI | 11/4/29 | 10/8/41 | 5/5/25 | 0 |
| 3 | WAS | 24/15/159 | 4/2/11 | 2/2/13 | 2 |
| 4 | LAC | 11/5/110 | 8/5/36 | 11/9/43 | 3 |
| 5 | SF | 18/11/150 | 7/5/24 | 3/3/15 | 3 |
| 6 | DEN | 15/9/58 | 2/2/13 | 7/6/36 | 0 |
| 7 | KC | 13/6/39 | 11/7/88 | 8/6/38 | 0 |
Per game: WR 15.9 tgt / 8.9 rec / 91.7 yds; TE 6.6 tgt / 4.7 rec / 34.4 yds; RB 6.3/5.4/31.9.
TE check: Rico's 5-6/g is slightly high - 4.7/g avg, 5 in 4 of 7 games, 2 in two games, 7-8 in two (ARI, KC). TE yards are low (34.4/g; only KC topped 41).
Explosives (20+ yd receptions): 8 in 7 games (1.1/g), ALL to WRs; 0 to TEs, 0 to RBs. Four games with zero.
Box-score screenshots: not reconciled (38 attachments, not individually verified in this pass) - gap.

## 4. Prices (odds.json, 5 AM ET pull - stale) and §7 (3 of last 4 Caleb games)
| Leg | FD | DK | Last 4 | §7 |
|---|---|---|---|---|
| Loveland rec 4.5 | O +116 / U -154 | O +118 | 0,1,6,7 -> 2/4 | FAIL |
| Loveland 3.5+ (alt) | -198 | -179 | 2/4 | FAIL |
| Loveland yds 42.5 (DK 41.5) | -113 | -114 | 0,3,65,69 -> 2/4 | FAIL |
| Odunze rec 3.5 | O +134 | (DK 2.5 -170) | 1/4 at 3.5; 3/4 at 2.5 | FAIL/ WR3 ban |
| Odunze yds 38.5 | -113 | -115 | 52,43,39,69 -> 4/4 | PASS, but WR3 ban |
| Raymond rec 2.5 | O +140 | +145 | 8,5,2,0 -> 2/4 | FAIL |
| Raymond yds 16.5 (DK 15.5) | -113 | -112 | 84,40,18,0 -> 3/4 | PASS, trend 18 then 0 |
Correlation: all compete with Rico's held Swift 3+, Burden 4+, Burden 30+ yds, Swift 50+ for the same targets; one slip per player.

## Verdict
Nothing clears cleanly. Worth modeling only if Rico wants: Loveland 3.5+ rec (best usage trend; fails §7 because wks 1-2 were 0 and 1) and Odunze 38.5 yds (passes §7 4/4, but blocked by WR3 ban unless Rico overrides). Raymond: no.
Gaps PFF session would fill: alignment (slot/wide/inline %) for each CHI target, routes run / route share, SEA defender yds per coverage snap & slot-vs-outside splits, who covers TEs in SEA zone, Witherspoon slot vs Burden/Odunze conflict.
