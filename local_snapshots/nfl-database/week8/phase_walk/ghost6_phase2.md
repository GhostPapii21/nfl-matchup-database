# Ghost6 — Phase 2 (Defensive profiles + 8A defender coverage check) — Sun Nov 1 2026
Generated 2026-10-31 ~7:40 PM ET. Phase 2 only.

## Sources and dates
- PFR advanced defense 2026: **fresh pull blocked (HTTP 403, 7:20 PM ET)**. I used the cached copy `/workspace/nfl-sim/mnf12/pfr_def_adv_2026.html`, saved Oct 29 6:02 AM ET. Most defenders show G=5, so it **misses the last ~2 games** for each team.
- nflverse PBP 2026 (pulled Oct 31 7:17 PM ET; all games through wk8) + nflverse weekly rosters for receiver position.
- nflverse FTN charting 2026: **this file has no man/zone, MOF open/closed or press columns** (it only has n_blitzers, n_pass_rushers, box, PA, screen). So man/zone and MOF are a **GAP** from free nflverse data. Blitz % = share of charted dropbacks with n_blitzers>0, using FTN's own definition. MIN's 71.9% looks unusually high, so treat it with caution.
- ESPN Week 8 WR/CB matchup cheatsheet (cached by BetGuru: `betguru_2026-11-01_raw/coverage_routes/espn_wrcb.txt`): WR alignment (LWR/slot/RWR %), the projected defender, the defender's side-of-field %, and team zone %.
- I didn't do play-by-play film coverage attribution. A PBP tackler is NOT the coverage defender (I only use them below as supporting context).

### Team defense (nflverse PBP 2026, all games; PassYds = gross credited passing yds excl. sacks; rank 1 = most allowed among these 25)

| DEF   |   G |   PA_g |   PassYds_g |   RushYds_g |   RB_ypc |   Stuff_pct |   Sacks_g |   Hits_g |   Blitz_pct |   ExpRec20 |   ExpRush15 |   ThirdConv |   RZ_TD_pct |   PassYds_g_rk |   RushYds_g_rk |
|:------|----:|-------:|------------:|------------:|---------:|------------:|----------:|---------:|------------:|-----------:|------------:|------------:|------------:|---------------:|---------------:|
| NYJ   |   7 |   21.4 |       202.9 |       128.9 |     4.08 |        14.4 |       2.7 |      4.9 |        38.4 |         17 |           6 |        38.6 |        50   |             22 |              5 |
| LAC   |   6 |   25.2 |       216.2 |       125.8 |     4.19 |        14.4 |       1.8 |      5.7 |        26.4 |         17 |           9 |        31.9 |        40   |             21 |              7 |
| CLE   |   7 |   20.9 |       220.7 |       117.1 |     4.64 |        21   |       2.9 |      6.7 |        23.3 |         20 |           9 |        40.4 |        34.6 |             20 |             10 |
| DAL   |   7 |   25.7 |       235.1 |       147   |     4.36 |        14.4 |       1.4 |      4.3 |        26.5 |         22 |          11 |        54.1 |        64.5 |             13 |              1 |
| ARI   |   7 |   29.7 |       243.7 |       126.7 |     4.29 |        15.4 |       2.1 |      4.3 |        30.7 |         22 |           9 |        41   |        51.5 |             11 |              6 |
| MIN   |   6 |   12.3 |       180.8 |        97.8 |     4.06 |        19.1 |       3.5 |      8.2 |        71.9 |         12 |           4 |        29.5 |        17.6 |             24 |             17 |
| TB    |   7 |   21.6 |       233.7 |        79.6 |     3.6  |        19.4 |       2.3 |      5.1 |        40.7 |         16 |           6 |        36.4 |        45.5 |             15 |             24 |
| ATL   |   7 |   24.7 |       271.4 |        90.3 |     4.12 |        19.7 |       2.4 |      7.4 |        24.7 |         23 |           6 |        43.3 |        64.3 |              4 |             20 |
| IND   |   7 |   25.7 |       227.4 |       125.6 |     4.49 |        13.7 |       1.9 |      4.3 |        22.1 |         19 |          10 |        30.4 |        48   |             18 |              8 |
| BUF   |   6 |   28.5 |       298.7 |       101.3 |     3.6  |        21.8 |       1.8 |      7   |        34.9 |         26 |           7 |        45.6 |        62.1 |              2 |             13 |
| BAL   |   7 |   23.9 |       235.1 |        96.7 |     3.76 |        20.2 |       2.3 |      6.7 |        33.1 |         20 |           9 |        41.3 |        61.5 |             13 |             18 |
| PHI   |   7 |   25   |       247.9 |       132.1 |     4.26 |        14.9 |       1.1 |      3.1 |        25.2 |         23 |           8 |        42.7 |        48.5 |              9 |              4 |
| WAS   |   6 |   28.7 |       268   |       101.5 |     3.82 |        15.8 |       1.8 |      5.3 |        47.4 |         20 |           4 |        46.2 |        75   |              5 |             12 |
| CIN   |   6 |   20.3 |       253.8 |       117.2 |     4.13 |        23.6 |       3.5 |      6.3 |        16.9 |         19 |          10 |        48.1 |        29.2 |              7 |              9 |
| JAX   |   6 |   17.3 |       283   |        72.7 |     2.97 |        16.8 |       1.8 |      5.5 |        31.8 |         21 |           3 |        38.2 |        33.3 |              3 |             25 |
| SEA   |   7 |   17.9 |       158   |        90.1 |     3.4  |        20.6 |       2.4 |      7.3 |        23.4 |          8 |           7 |        32.3 |        73.3 |             25 |             21 |
| SF    |   7 |   19.9 |       223.9 |        89.7 |     3.59 |        14.9 |       2.1 |      5.1 |        31.9 |         14 |           2 |        38.3 |        44   |             19 |             22 |
| HOU   |   7 |   24.3 |       262.7 |        98.4 |     4.1  |        13.1 |       3   |      6.3 |        26.1 |         29 |           5 |        42   |        52   |              6 |             16 |
| LV    |   7 |   28.1 |       245.1 |       145.1 |     5.17 |        13.5 |       2.3 |      6.6 |        27.6 |         19 |          11 |        45.1 |        66.7 |             10 |              2 |
| PIT   |   7 |   19.7 |       230   |        91.7 |     3.64 |        21.7 |       2.6 |      5.6 |        27.2 |         23 |           8 |        35.9 |        33.3 |             16 |             19 |
| DET   |   6 |   27.5 |       313.5 |       100.3 |     4.12 |        16.4 |       3.5 |      8.3 |        27   |         29 |           8 |        48.2 |        56.7 |              1 |             14 |
| LA    |   7 |   22.7 |       193   |       115.7 |     3.77 |        18.2 |       1.4 |      4   |        30.3 |         14 |          12 |        32.2 |        41.4 |             23 |             11 |
| CHI   |   7 |   20.4 |       241.3 |        87.9 |     4.33 |        16.9 |       2.7 |      5.1 |        41.7 |         21 |           8 |        26.1 |        45.8 |             12 |             23 |
| KC    |   6 |   17.2 |       229.5 |        99.7 |     3.29 |        18.1 |       1.3 |      5   |        27.6 |         16 |           4 |        43   |        25   |             17 |             15 |
| NO    |   7 |   27.7 |       249.7 |       140.9 |     4.9  |        12.4 |       2.6 |      4.9 |        33.7 |         24 |          13 |        50   |        51.4 |              8 |              3 |

### Positional receiving allowed

| DEF   | POS   |   G |   Tgt |   Rec |   Yds |   Tgt_g |   Rec_g |   Yds_g |   YPT |   Exp20 |
|:------|:------|----:|------:|------:|------:|--------:|--------:|--------:|------:|--------:|
| NYJ   | WR    |   7 |   122 |    75 |   933 |    17.4 |    10.7 |   133.3 |  7.65 |      15 |
| NYJ   | TE    |   7 |    46 |    33 |   336 |     6.6 |     4.7 |    48   |  7.3  |       2 |
| NYJ   | RB    |   7 |    45 |    24 |   151 |     6.4 |     3.4 |    21.6 |  3.36 |       0 |
| LAC   | WR    |   6 |    90 |    62 |   797 |    15   |    10.3 |   132.8 |  8.86 |      10 |
| LAC   | TE    |   6 |    38 |    28 |   345 |     6.3 |     4.7 |    57.5 |  9.08 |       5 |
| LAC   | RB    |   6 |    42 |    23 |   154 |     7   |     3.8 |    25.7 |  3.67 |       2 |
| CLE   | WR    |   7 |   133 |    77 |  1060 |    19   |    11   |   151.4 |  7.97 |      16 |
| CLE   | TE    |   7 |    57 |    39 |   345 |     8.1 |     5.6 |    49.3 |  6.05 |       2 |
| CLE   | RB    |   7 |    47 |    27 |   140 |     6.7 |     3.9 |    20   |  2.98 |       2 |
| DAL   | WR    |   7 |   127 |    83 |  1142 |    18.1 |    11.9 |   163.1 |  8.99 |      20 |
| DAL   | TE    |   7 |    45 |    36 |   326 |     6.4 |     5.1 |    46.6 |  7.24 |       2 |
| DAL   | RB    |   7 |    44 |    28 |   159 |     6.3 |     4   |    22.7 |  3.61 |       0 |
| ARI   | WR    |   7 |   110 |    66 |   988 |    15.7 |     9.4 |   141.1 |  8.98 |      16 |
| ARI   | TE    |   7 |    51 |    40 |   418 |     7.3 |     5.7 |    59.7 |  8.2  |       4 |
| ARI   | RB    |   7 |    40 |    22 |   220 |     5.7 |     3.1 |    31.4 |  5.5  |       2 |
| MIN   | WR    |   6 |   102 |    59 |   743 |    17   |     9.8 |   123.8 |  7.28 |       7 |
| MIN   | TE    |   6 |    38 |    18 |   233 |     6.3 |     3   |    38.8 |  6.13 |       4 |
| MIN   | RB    |   6 |    38 |    19 |   109 |     6.3 |     3.2 |    18.2 |  2.87 |       1 |
| TB    | WR    |   7 |   131 |    82 |   943 |    18.7 |    11.7 |   134.7 |  7.2  |      10 |
| TB    | TE    |   7 |    57 |    40 |   434 |     8.1 |     5.7 |    62   |  7.61 |       6 |
| TB    | RB    |   7 |    58 |    38 |   259 |     8.3 |     5.4 |    37   |  4.47 |       0 |
| ATL   | WR    |   7 |   149 |    96 |  1189 |    21.3 |    13.7 |   169.9 |  7.98 |      19 |
| ATL   | TE    |   7 |    61 |    47 |   439 |     8.7 |     6.7 |    62.7 |  7.2  |       3 |
| ATL   | RB    |   7 |    76 |    43 |   260 |    10.9 |     6.1 |    37.1 |  3.42 |       1 |
| IND   | WR    |   7 |   118 |    71 |   991 |    16.9 |    10.1 |   141.6 |  8.4  |      15 |
| IND   | TE    |   7 |    50 |    34 |   317 |     7.1 |     4.9 |    45.3 |  6.34 |       1 |
| IND   | RB    |   7 |    44 |    24 |   271 |     6.3 |     3.4 |    38.7 |  6.16 |       3 |
| BUF   | WR    |   6 |   129 |    82 |  1043 |    21.5 |    13.7 |   173.8 |  8.09 |      18 |
| BUF   | TE    |   6 |    57 |    39 |   465 |     9.5 |     6.5 |    77.5 |  8.16 |       6 |
| BUF   | RB    |   6 |    56 |    36 |   284 |     9.3 |     6   |    47.3 |  5.07 |       2 |
| BAL   | WR    |   7 |   137 |    92 |  1271 |    19.6 |    13.1 |   181.6 |  9.28 |      18 |
| BAL   | TE    |   7 |    38 |    29 |   273 |     5.4 |     4.1 |    39   |  7.18 |       2 |
| BAL   | RB    |   7 |    51 |    29 |   102 |     7.3 |     4.1 |    14.6 |  2    |       0 |
| PHI   | WR    |   7 |   154 |    92 |  1297 |    22   |    13.1 |   185.3 |  8.42 |      20 |
| PHI   | TE    |   7 |    43 |    31 |   301 |     6.1 |     4.4 |    43   |  7    |       2 |
| PHI   | RB    |   7 |    47 |    23 |   137 |     6.7 |     3.3 |    19.6 |  2.91 |       1 |
| WAS   | WR    |   6 |   117 |    78 |   950 |    19.5 |    13   |   158.3 |  8.12 |      14 |
| WAS   | TE    |   6 |    49 |    37 |   441 |     8.2 |     6.2 |    73.5 |  9    |       4 |
| WAS   | RB    |   6 |    53 |    30 |   217 |     8.8 |     5   |    36.2 |  4.09 |       2 |
| CIN   | WR    |   6 |   109 |    63 |   825 |    18.2 |    10.5 |   137.5 |  7.57 |      11 |
| CIN   | TE    |   6 |    54 |    41 |   509 |     9   |     6.8 |    84.8 |  9.43 |       6 |
| CIN   | RB    |   6 |    39 |    24 |   189 |     6.5 |     4   |    31.5 |  4.85 |       2 |
| JAX   | WR    |   6 |   126 |    82 |  1260 |    21   |    13.7 |   210   | 10    |      20 |
| JAX   | TE    |   6 |    37 |    25 |   208 |     6.2 |     4.2 |    34.7 |  5.62 |       0 |
| JAX   | RB    |   6 |    49 |    33 |   230 |     8.2 |     5.5 |    38.3 |  4.69 |       1 |
| SEA   | WR    |   7 |   110 |    62 |   642 |    15.7 |     8.9 |    91.7 |  5.84 |       8 |
| SEA   | TE    |   7 |    46 |    33 |   241 |     6.6 |     4.7 |    34.4 |  5.24 |       0 |
| SEA   | RB    |   7 |    56 |    38 |   223 |     8   |     5.4 |    31.9 |  3.98 |       0 |
| SF    | WR    |   7 |   122 |    75 |   908 |    17.4 |    10.7 |   129.7 |  7.44 |      12 |
| SF    | TE    |   7 |    55 |    42 |   305 |     7.9 |     6   |    43.6 |  5.55 |       1 |
| SF    | RB    |   7 |    71 |    49 |   340 |    10.1 |     7   |    48.6 |  4.79 |       1 |
| HOU   | WR    |   7 |   156 |    98 |  1361 |    22.3 |    14   |   194.4 |  8.72 |      23 |
| HOU   | TE    |   7 |    44 |    32 |   322 |     6.3 |     4.6 |    46   |  7.32 |       5 |
| HOU   | RB    |   7 |    46 |    33 |   146 |     6.6 |     4.7 |    20.9 |  3.17 |       1 |
| LV    | WR    |   7 |   118 |    67 |  1049 |    16.9 |     9.6 |   149.9 |  8.89 |      14 |
| LV    | TE    |   7 |    62 |    51 |   405 |     8.9 |     7.3 |    57.9 |  6.53 |       3 |
| LV    | RB    |   7 |    42 |    28 |   250 |     6   |     4   |    35.7 |  5.95 |       2 |
| PIT   | WR    |   7 |   142 |    86 |  1031 |    20.3 |    12.3 |   147.3 |  7.26 |      14 |
| PIT   | TE    |   7 |    40 |    29 |   293 |     5.7 |     4.1 |    41.9 |  7.32 |       6 |
| PIT   | RB    |   7 |    56 |    38 |   289 |     8   |     5.4 |    41.3 |  5.16 |       3 |
| DET   | WR    |   6 |   134 |    89 |  1121 |    22.3 |    14.8 |   186.8 |  8.37 |      20 |
| DET   | TE    |   6 |    73 |    56 |   602 |    12.2 |     9.3 |   100.3 |  8.25 |       8 |
| DET   | RB    |   6 |    50 |    26 |   146 |     8.3 |     4.3 |    24.3 |  2.92 |       1 |
| LA    | WR    |   7 |   111 |    59 |   742 |    15.9 |     8.4 |   106   |  6.68 |       9 |
| LA    | TE    |   7 |    58 |    34 |   292 |     8.3 |     4.9 |    41.7 |  5.03 |       1 |
| LA    | RB    |   7 |    56 |    37 |   315 |     8   |     5.3 |    45   |  5.62 |       4 |
| CHI   | WR    |   7 |   110 |    66 |  1046 |    15.7 |     9.4 |   149.4 |  9.51 |      14 |
| CHI   | TE    |   7 |    46 |    34 |   396 |     6.6 |     4.9 |    56.6 |  8.61 |       4 |
| CHI   | RB    |   7 |    38 |    26 |   247 |     5.4 |     3.7 |    35.3 |  6.5  |       3 |
| KC    | WR    |   6 |   105 |    60 |   732 |    17.5 |    10   |   122   |  6.97 |      11 |
| KC    | TE    |   6 |    63 |    44 |   425 |    10.5 |     7.3 |    70.8 |  6.75 |       4 |
| KC    | RB    |   6 |    44 |    28 |   220 |     7.3 |     4.7 |    36.7 |  5    |       1 |
| NO    | WR    |   7 |   120 |    74 |  1005 |    17.1 |    10.6 |   143.6 |  8.38 |      16 |
| NO    | TE    |   7 |    62 |    45 |   479 |     8.9 |     6.4 |    68.4 |  7.73 |       5 |
| NO    | RB    |   7 |    48 |    33 |   264 |     6.9 |     4.7 |    37.7 |  5.5  |       3 |

## 8A defender maps (PFR cached Oct 29: Tgt-Cmp-Cmp%-Yds-YPT-TD-Rating)

### Bowers 6+ rec (LV @ NYJ). Alignment: slot 57%, LWR 21%, RWR 21% (ESPN). NYJ zone 60%.
- Slot CB D'Angelo Ponds (100% slot): **not in PFR (no qualifying targets)**. ESPN shows only 23–32 routes faced, so the sample is too thin. GAP.
- LB Jamien Sherwood: 18-15-83.3%-163-9.1-1-122.9 (doesn't limit catches)
- LB Demario Davis: 18-12-66.7%-133-7.4-0-88.4
- S Dane Belton 13-7-53.8%-78-6.0 · S Andre Cisco 12-6-50.0%-75-6.3 · NB Jarvis Brownlee 14-8-57.1%-56-4.0-2
- NYJ vs TEs: 6.6 tgt / 4.7 rec / 48.0 yds per game, 72% catch rate, 7.30 YPT, 2 receiving explosives on 46 targets.
- **Verdict: PASS.** The defenders most likely to cover him allow a high catch rate (Sherwood 83%, Davis 67%), and NYJ allows 4.7 TE catches per game. His volume (9–13 targets) is well above what the line needs. Gaps: the Ponds sample and MOF.

### Puka 70+ yds (LAC @ LAR). Alignment: RWR 52%, LWR 24%, slot 24%.
- LCB Donte Jackson (LCB 64%, Q-hamstring): 9-6-66.7%-69-7.7-0-89.6
- Cam Hart: 16-10-62.5%-167-10.4-0-71.6 · Tarheeb Still: 11-5-45.5%-71-6.5-1-97.2 (limits catches, not yards) · S Derwin James 11-7-63.6%-43-3.9-1 · S Tony Jefferson 8-5-62.5%-67-8.4 · Rodney Shelley 6-5-83.3%-99-16.5
- LAC vs WRs: 15.0 tgt / 10.3 rec / 132.8 yds per game, **8.86 YPT**, 10 explosives. Pass yds allowed 216.2/g.
- **Verdict: PASS.** The defender who'd cover him most (Jackson) and his likely replacements (Hart, Shelley) all allow 7.7+ YPT. Still allows only 6.5 YPT, which is a modest risk if Jackson sits. Recheck Jackson at inactives.

### Metcalf 40+ yds (CLE @ PIT). Alignment: LWR 47%, RWR 32%, slot 21%. Line-up vs RCB.
- RCB Tyson Campbell (RCB 95%): 12-9-75.0%-179-**14.9**-0-116.7
- LCB Denzel Ward (LCB **91%**, slot 1%): 25-10-40.0%-142-5.7-3-82.0 (limits both catches and yards)
- Myles Harden 25-14-56.0%-230-9.2-2 · Mekhi Blackmon 17-8-47.1%-91-5.4 · S Delpit 20-10-50%-140-7.0 · S Hickman 17-11-64.7%-150-8.8-3
- CLE vs WRs: 19.0 tgt / 11.0 rec / 151.4 yds per game, 7.97 YPT, 16 explosives.

**The "1 catch for 15 yards on 7 targets vs Ward in the last two meetings" claim:**
- Source: BetGuru's `coverage_routes/defender_route_audit.md` cites **Fantasy Points**, which is paywalled. Nobody pulled the raw data, so it **can't be verified with free data**.
- The last two meetings were 2025 wk6 (Metcalf 4-95 on 9 targets) and 2026 wk4 (5-115 on 9 targets). Metcalf missed 2025 wk17 vs CLE: he isn't among PIT's targeted receivers in nflverse PBP for that game. **Overall he caught 9 for 210 on 18 targets.**
- Ward's name appears on only **one** Metcalf play across both games: a pass breakup in 2025 Q3 (6-yard air, left side). A Ward-specific 1-15 on 7 split can't be confirmed or ruled out without charting. As a description of how Metcalf did against CLE, though, it's misleading.
- **Did Ward shadow him in 2026 wk4?** The evidence says no:
  - Ward plays LCB 91% of snaps with 1% slot (ESPN), which isn't how a shadow corner plays.
  - Metcalf's 9 targets were spread evenly: right 3, middle 3, left 3.
  - The catches were tackled by Hickman (15), Delpit (7), Harden (43) and **Campbell twice (22 and 28, both on left-side throws)**. That matches Metcalf at LWR facing RCB Campbell.
  - Ward isn't named on any of the 9 plays.
- **Verdict: PASS.** No shadow evidence, his main defender allows 14.9 YPT, and the 40-yard line sits under his usual yardage. The risk: on his 32% of RWR snaps he faces Ward. He's 4/7 at 40+ (Phase 1), which is a modest rate.

### McBride 7+ rec (ARI @ DAL)
- Free data doesn't show where TEs line up. Defenders who usually cover TEs:
  - LB Dee Winters 17-15-**88.2%**-132-7.8
  - LB Jaishawn Barham 12-11-**91.7%**-80-6.7
  - Slot S Caleb Downs (98% slot) 10-9-**90.0%**-71-7.1
  - S Malik Hooker 7-4-57.1%-54
- DAL vs TEs: 6.4 tgt / 5.1 rec / 46.6 yds per game, **80% catch rate**. DAL allows 25.7 pts and 54.1% third-down conversions (worst of the 25 teams).
- **Verdict: PASS.** Every likely coverage defender allows a 88–92% catch rate. Alignment is still a GAP (it's the one BetGuru cut him for). The film charting Rico suggested would close it.

### Lamb rec (ARI @ DAL; recyds barred). Alignment: slot 38%, RWR 34%, LWR 28%.
- Projected defender Denzel Burke (LCB 46%/RCB 41%/slot 13%): 15-10-66.7%-114-7.6-2-101.1
- Max Melton 17-10-58.8%-137-8.1 · Will Johnson 14-7-50.0%-105-7.5 · slot Garrett Williams 6-4-66.7%-21-3.5 (small sample) · S Budda Baker 16-8-50%-200-12.5
- ARI vs WRs: 15.7 tgt / 9.4 rec / 141.1 yds per game, 8.98 YPT. Allows 29.7 pts/g (most of the 25).
- **Verdict: PASS** (catch-rate check: no defender allows under 50%, and Burke allows 67%). The rung depends on his line: he's had 6+ catches in 3/7 games. **CUT RUNG** to 5+ if the price allows.

### Gibbs 70+ rush (MIN @ DET)
- MIN run defense: 97.8 rush yds/g (rank 17/25 by most allowed), **RB 4.06 YPC, 19.1% of carries for 0 or fewer yards, only 4 rushes of 15+ yards allowed in 6 games (the fewest here)**. MIN allows just 12.3 pts/g and 29.5% third-down conversions.
- Blitz rate (FTN): 71.9%, flagged as possibly overstated. 3.5 sacks/g.
- Gibbs went 4/6 at 70+, and his total includes 28 OT yards in wk1.
- **Verdict: CUT RUNG.** MIN is the toughest run defense and the stingiest scoring defense on this card, and it takes away the explosive runs Gibbs's totals rely on. I'd go down to about 50–60+, or switch to rush+rec if that market is open (rec alone is barred).

## Opponents of BetGuru's other PASS legs
The team table above also covers TB, ATL, IND, BUF, BAL, PHI, WAS, CIN, JAX, SEA, SF, HOU, CHI, KC and NO, plus positional rows in the same format (in /tmp/def_profiles.md; the 6 priority opponents plus TB are shown above). I didn't build defender maps for those legs because I ran out of time. GAP.

## Phase 2 verdict summary
| Leg | Verdict | Key reason |
|---|---|---|
| Bowers 6+ rec | PASS | Sherwood 83% / Davis 67% catch rate allowed; NYJ allows 4.7 TE rec/g; Ponds sample GAP |
| Puka 70+ yds | PASS (Jackson Q) | Jackson 7.7 YPT, Hart 10.4; LAC allows 8.86 WR YPT |
| Metcalf 40+ yds | PASS | Ward plays LCB 91%, no shadow in wk4; Campbell allows 14.9 YPT; "1-15 on 7" claim unverified and misleading (9-210 on 18 over the last 2 meetings) |
| McBride 7+ rec | PASS (alignment GAP) | DAL TE coverage defenders allow 88–92% catch rate |
| Lamb rec | PASS / CUT RUNG to 5+ | Burke 67% catch rate allowed; ARI 29.7 pts/g |
| Gibbs 70+ rush | CUT RUNG | MIN 4.06 RB YPC, 4 runs of 15+ allowed in 6 games, 12.3 pts/g |

Phase-wide GAPs: man/zone, MOF and press (not in free FTN data); PFR is 2 days stale and missing the last ~2 games; pressure attribution.

## ADDENDUM (Oct 31 ~7:50 PM ET): Man/zone and MOF gap filled
Source 1: Sharp Football Analysis, "NFL Coverage Scheme Stats & Rates," updated Oct 27, 2026. https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/
Source 2: StatRankings man-coverage-rate and single-high-rate pages, updated Oct 31, 2026, through Oct 30 games. https://statrankings.com/nfl/advanced/teams/coverage/man-coverage-rate and /single-high-rate. Free search excerpts only list ranks 1–18; ARI and MIN aren't in those ranks (so they're lower).
Source 3 (context only): Fantasy Points Week 5 shells article (CLE 52% man, 79% single-high; NYJ 62% two-high, 1st in Cover 2) and oneweekseason.com Week 8 (NYJ man 37.5%, two-high 56.2%, blitz 40.0%).

| DEF | Sharp man % | Sharp zone % | Sharp MOF closed % | Sharp MOF open % | StatRankings man % | StatRankings single-high % | Read |
|---|---|---|---|---|---|---|---|
| NYJ | 23.8 | 66.6 | 45.2 | 50.0 | 37.5 (12th) | n/a (two-high 56.2%, OWS) | zone/two-high lean, Cover 2 heavy, allows few deep passes, which favors underneath TE volume (Bowers catches) |
| LAC | 10.6 | 58.0 | 33.9 | 40.7 | 34.6 (15th) | 49.4 (18th) | zone, middle open, which favors Puka's intermediate volume |
| CLE | 42.4 | 54.0 | **72.6** | 24.4 | **55.8 (1st)** | **69.9 (1st)** | most man / single-high (Cover 1) in the league. Metcalf gets one-on-one outside vs Campbell. Single-high is vulnerable deep outside, but man defenders limit catches (Metcalf only catches 55%) |
| DAL | 21.3 | 69.9 | 60.2 | 35.7 | 46.5 (4th) | 60.0 (4th) | middle closed, rising man rate. The middle-closed hook/curl zone is where TEs like McBride feed |
| ARI | 9.1 | 70.9 | 21.9 | 56.7 | not top 18 | not top 18 | heavy zone, middle open, which favors Lamb's slot/intermediate catch volume |
| MIN | 5.3 | 86.5 | 31.6 | 61.2 | not top 18 | not top 18 | heaviest zone, two-high. Light boxes in theory help the run, but the measured MIN run D is still stingy (Phase 2) |

**The two sources disagree on size:** StatRankings' man % runs about 10–25 points higher than Sharp's, which likely means a different definition or date. They agree on rank order (CLE most man; CLE/DAL single-high/middle closed). I kept both.

**The gap is closed for all six legs.** No verdict changes. Metcalf's note: CLE plays the most man in the league, so he gets one-on-one coverage, but man corners limit catch rate. His line is a yards line, though, and Campbell allows 14.9 YPT in that scheme, so his PASS stands.

**PFR fresh pull, one retry:** a desktop-browser UA plus a #fragment URL returned **HTTP 403** again at ~7:45 PM ET. I didn't retry further. The cached Oct 29 6:02 AM ET copy is still the source.
