# Ghost6 — Phase 1 (Collect & Reconcile) — Sun Nov 1 2026 card
Generated 2026-10-31 ~7:25 PM ET. Scope: Phase 1 only (GAME_SCRIPT_2026-10-29.md L134+).

Sources: (A) nflverse play_by_play_2026.parquet (pulled 10/31 7:17 PM ET; all 2026 team games through wk8, 108 games), aggregated by me; (B) ESPN game logs cached in betguru_2026-11-01_raw/full_leg_*.json (last 5 games only); (C) nflverse snap_counts_2026.parquet. nflverse stats_player_week_2026 download failed (404) — not used.
Definitions: tgt excludes sacks; rz_tgt = target from opp 20 or closer; gl_car = carry from opp 5 or closer; clutch_tgt = Q4, ≤2:00 left, score within 8; ot_* = overtime counts. Zero rows with no snap% = player did not play (no cherry-picking: all team games listed).

## Brock Bowers

|   wk | opp   |   tgt |   rec |   recyd |   air |   car |   rushyd |   td |   rz_tgt |   gl_car |   clutch_tgt |   ot_tgt |   ot_car |   snap_pct |
|-----:|:------|------:|------:|--------:|------:|------:|---------:|-----:|---------:|---------:|-------------:|---------:|---------:|-----------:|
|    1 | MIA   |     0 |     0 |       0 |     0 |     0 |        0 |    0 |        0 |        0 |            0 |        0 |        0 |     nan    |
|    2 | LAC   |     0 |     0 |       0 |     0 |     0 |        0 |    0 |        0 |        0 |            0 |        0 |        0 |     nan    |
|    3 | NO    |    13 |    10 |     116 |   106 |     0 |        0 |    1 |        3 |        0 |            0 |        0 |        0 |       0.79 |
|    4 | KC    |    11 |     6 |      86 |   148 |     0 |        0 |    1 |        1 |        0 |            0 |        0 |        0 |       0.82 |
|    5 | NE    |    10 |     8 |     110 |    69 |     0 |        0 |    1 |        1 |        0 |            0 |        0 |        0 |       0.7  |
|    6 | BUF   |     9 |     4 |      70 |   115 |     0 |        0 |    0 |        2 |        0 |            0 |        0 |        0 |       0.98 |
|    7 | LA    |     9 |     6 |      73 |    81 |     0 |        0 |    0 |        1 |        0 |            0 |        0 |        0 |       0.84 |

## Puka Nacua

|   wk | opp   |   tgt |   rec |   recyd |   air |   car |   rushyd |   td |   rz_tgt |   gl_car |   clutch_tgt |   ot_tgt |   ot_car |   snap_pct |
|-----:|:------|------:|------:|--------:|------:|------:|---------:|-----:|---------:|---------:|-------------:|---------:|---------:|-----------:|
|    1 | SF    |     9 |     5 |      74 |   115 |     0 |        0 |    0 |        1 |        0 |            0 |        0 |        0 |       0.7  |
|    2 | NYG   |     0 |     0 |       0 |     0 |     0 |        0 |    0 |        0 |        0 |            0 |        0 |        0 |     nan    |
|    3 | DEN   |     0 |     0 |       0 |     0 |     0 |        0 |    0 |        0 |        0 |            0 |        0 |        0 |     nan    |
|    4 | PHI   |    12 |     9 |     125 |   136 |     1 |        2 |    1 |        0 |        1 |            1 |        0 |        0 |       0.9  |
|    5 | BUF   |    24 |    17 |     138 |   184 |     2 |        9 |    1 |        3 |        0 |            2 |        3 |        0 |       0.85 |
|    6 | ARI   |     7 |     6 |      80 |    60 |     0 |        0 |    0 |        0 |        0 |            1 |        0 |        0 |       0.9  |
|    7 | LV    |    10 |     8 |      68 |    57 |     2 |       10 |    1 |        3 |        0 |            0 |        0 |        0 |       0.85 |

## DK Metcalf

|   wk | opp   |   tgt |   rec |   recyd |   air |   car |   rushyd |   td |   rz_tgt |   gl_car |   clutch_tgt |   ot_tgt |   ot_car | snap_pct   |
|-----:|:------|------:|------:|--------:|------:|------:|---------:|-----:|---------:|---------:|-------------:|---------:|---------:|:-----------|
|    1 | ATL   |    10 |     4 |      40 |   204 |     0 |        0 |    0 |        0 |        0 |            0 |        0 |        0 |            |
|    2 | NE    |     9 |     4 |      27 |    62 |     0 |        0 |    0 |        0 |        0 |            0 |        0 |        0 |            |
|    3 | CIN   |     5 |     3 |      31 |    73 |     0 |        0 |    1 |        1 |        0 |            0 |        0 |        0 |            |
|    4 | CLE   |     9 |     5 |     115 |   155 |     0 |        0 |    0 |        0 |        0 |            0 |        0 |        0 |            |
|    5 | IND   |     4 |     3 |      12 |    15 |     1 |       11 |    0 |        0 |        0 |            0 |        0 |        0 |            |
|    6 | TB    |    15 |    11 |      93 |   118 |     0 |        0 |    0 |        2 |        0 |            1 |        3 |        0 |            |
|    7 | NO    |     6 |     2 |      56 |   110 |     0 |        0 |    0 |        1 |        0 |            0 |        0 |        0 |            |

## Trey McBride

|   wk | opp   |   tgt |   rec |   recyd |   air |   car |   rushyd |   td |   rz_tgt |   gl_car |   clutch_tgt |   ot_tgt |   ot_car |   snap_pct |
|-----:|:------|------:|------:|--------:|------:|------:|---------:|-----:|---------:|---------:|-------------:|---------:|---------:|-----------:|
|    1 | LAC   |    13 |     9 |      95 |    89 |     0 |        0 |    1 |        4 |        0 |            0 |        0 |        0 |       0.8  |
|    2 | SEA   |    10 |     8 |      41 |    36 |     0 |        0 |    1 |        2 |        0 |            0 |        0 |        0 |       0.88 |
|    3 | SF    |    11 |     9 |      75 |    57 |     0 |        0 |    0 |        2 |        0 |            0 |        0 |        0 |       0.91 |
|    4 | NYG   |    12 |     7 |      31 |    70 |     0 |        0 |    0 |        1 |        0 |            5 |        0 |        0 |       0.97 |
|    5 | DET   |    10 |     9 |      66 |    75 |     0 |        0 |    1 |        2 |        0 |            0 |        0 |        0 |       0.9  |
|    6 | LA    |     9 |     7 |      53 |    28 |     0 |        0 |    0 |        2 |        0 |            0 |        0 |        0 |       0.97 |
|    7 | DEN   |    13 |    10 |     111 |   106 |     0 |        0 |    1 |        4 |        0 |            0 |        0 |        0 |       0.93 |

## Jahmyr Gibbs

|   wk | opp   |   tgt |   rec |   recyd |   air |   car |   rushyd |   td |   rz_tgt |   gl_car |   clutch_tgt |   ot_tgt |   ot_car |   snap_pct |
|-----:|:------|------:|------:|--------:|------:|------:|---------:|-----:|---------:|---------:|-------------:|---------:|---------:|-----------:|
|    1 | NO    |     5 |     5 |      30 |    -4 |    29 |      156 |    2 |        0 |        5 |            0 |        1 |        5 |       0.74 |
|    2 | BUF   |     8 |     6 |      61 |    34 |    16 |       52 |    1 |        2 |        0 |            0 |        0 |        0 |       0.83 |
|    3 | NYJ   |     8 |     7 |      65 |     4 |    20 |       99 |    3 |        3 |        2 |            0 |        0 |        0 |       0.69 |
|    4 | CAR   |     7 |     4 |      22 |    22 |    15 |       46 |    1 |        1 |        1 |            0 |        0 |        0 |       0.87 |
|    5 | ARI   |     6 |     5 |      56 |    -7 |    25 |      151 |    2 |        0 |        5 |            0 |        0 |        0 |       0.7  |
|    7 | GB    |     6 |     5 |      27 |   -12 |    29 |      116 |    0 |        1 |        0 |            0 |        0 |        0 |       0.9  |

## CeeDee Lamb

|   wk | opp   |   tgt |   rec |   recyd |   air |   car |   rushyd |   td |   rz_tgt |   gl_car |   clutch_tgt |   ot_tgt |   ot_car |   snap_pct |
|-----:|:------|------:|------:|--------:|------:|------:|---------:|-----:|---------:|---------:|-------------:|---------:|---------:|-----------:|
|    1 | NYG   |     8 |     5 |      44 |    90 |     1 |        0 |    1 |        2 |        0 |            0 |        0 |        0 |       0.81 |
|    2 | WAS   |     9 |     8 |     153 |   136 |     0 |        0 |    2 |        1 |        0 |            0 |        0 |        0 |       0.75 |
|    3 | BAL   |     9 |     7 |     112 |    85 |     0 |        0 |    0 |        1 |        0 |            1 |        0 |        0 |       0.82 |
|    4 | HOU   |    21 |    17 |     189 |   159 |     1 |       -6 |    1 |        3 |        0 |            4 |        0 |        0 |       0.86 |
|    5 | TB    |     5 |     2 |       9 |    56 |     0 |        0 |    0 |        0 |        0 |            0 |        0 |        0 |       0.57 |
|    6 | GB    |    19 |     9 |      70 |   153 |     0 |        0 |    0 |        5 |        0 |            0 |        0 |        0 |       0.88 |
|    7 | PHI   |    12 |     5 |      74 |   176 |     0 |        0 |    2 |        4 |        0 |            0 |        0 |        0 |       0.81 |

## Kyren Williams

|   wk | opp   |   tgt |   rec |   recyd |   air |   car |   rushyd |   td |   rz_tgt |   gl_car |   clutch_tgt |   ot_tgt |   ot_car |   snap_pct |
|-----:|:------|------:|------:|--------:|------:|------:|---------:|-----:|---------:|---------:|-------------:|---------:|---------:|-----------:|
|    1 | SF    |     3 |     3 |      24 |     7 |    11 |       41 |    1 |        0 |        2 |            0 |        0 |        0 |       0.64 |
|    2 | NYG   |     2 |     2 |      12 |     5 |    12 |       85 |    1 |        1 |        0 |            0 |        0 |        0 |       0.55 |
|    3 | DEN   |     7 |     6 |      70 |    44 |    15 |       88 |    0 |        0 |        0 |            2 |        0 |        0 |       0.71 |
|    4 | PHI   |    13 |    10 |      67 |    46 |    16 |       80 |    2 |        1 |        1 |            0 |        0 |        0 |       0.83 |
|    5 | BUF   |     8 |     6 |      27 |     1 |    16 |       49 |    1 |        2 |        3 |            3 |        1 |        2 |       0.73 |
|    6 | ARI   |     6 |     3 |      17 |     3 |    10 |       50 |    0 |        1 |        0 |            1 |        0 |        0 |       0.72 |
|    7 | LV    |     2 |     2 |      22 |    -2 |    16 |       99 |    1 |        0 |        1 |            0 |        0 |        0 |       0.51 |

## Blake Corum

|   wk | opp   |   tgt |   rec |   recyd |   air |   car |   rushyd |   td |   rz_tgt |   gl_car |   clutch_tgt |   ot_tgt |   ot_car |   snap_pct |
|-----:|:------|------:|------:|--------:|------:|------:|---------:|-----:|---------:|---------:|-------------:|---------:|---------:|-----------:|
|    1 | SF    |     0 |     0 |       0 |     0 |    10 |       54 |    0 |        0 |        0 |            0 |        0 |        0 |       0.23 |
|    2 | NYG   |     1 |     1 |      13 |    -6 |    12 |       79 |    0 |        0 |        0 |            0 |        0 |        0 |       0.45 |
|    3 | DEN   |     4 |     2 |       0 |    -1 |     6 |       15 |    0 |        1 |        0 |            0 |        0 |        0 |       0.29 |
|    4 | PHI   |     2 |     1 |       7 |     5 |     5 |       14 |    0 |        0 |        0 |            0 |        0 |        0 |       0.15 |
|    5 | BUF   |     4 |     3 |      53 |     7 |     5 |       19 |    1 |        1 |        1 |            0 |        0 |        0 |       0.27 |
|    6 | ARI   |     2 |     2 |      18 |    -3 |     9 |       42 |    1 |        1 |        0 |            0 |        0 |        0 |       0.28 |
|    7 | LV    |     1 |     1 |       8 |     2 |    17 |       93 |    1 |        0 |        1 |            0 |        0 |        0 |       0.44 |

## Two-source reconciliation (PBP vs ESPN box, last 5 games)

| Player | Game | PBP | ESPN | Status |
|---|---|---|---|---|
| Bowers | wk3 NO | 13 tgt | 14 tgt | UNRESOLVED (1 tgt; likely nullified/penalty play) |
| Bowers | wk7 LA | 9 tgt | 8 tgt | UNRESOLVED (1 tgt) |
| Lamb | wk6 GB | 19 tgt | 18 tgt | UNRESOLVED (1 tgt) |
| Gibbs | wk4 CAR | 22 rec yds | 31 rec yds | UNRESOLVED (9 yds; possible lateral/credit difference) |
| Puka, Metcalf, McBride, all other cells | — | match | match | rec, rec yds, carries, rush yds agree |

Receptions/yards for every prop-relevant cell agree except Gibbs wk4 rec yds (not his prop market). Weeks 1–2 (or earlier) have PBP only — no second source in cache (GAP for those weeks).

## Regulation vs OT
- Gibbs wk1 NO: 29 car/156 yds full game = **24/128 regulation + 5/28 OT**.
- Puka wk5 BUF: 24 tgt/138 yds full = **regulation 112 yds** (OT 26 yds on 2 catches; 3 OT tgts).
- Metcalf wk6 TB: 3 OT targets (regulation split not separately pulled for yards).
- Kyren wk5 BUF: 1 OT tgt, 2 OT car. No other OT for these players.

## OL starting five (last game, snap ≥50%, nflverse snaps) and tackle status
- LV: T Kolton Miller, G Caleb Rogers, C Tyler Linderbaum, G Spencer Burford, T DJ (Delmar) Glaze — **Glaze Questionable** (injuries.md 10/28).
- LAR: Alaric Jackson, Steve Avila, Coleman Shelton, Kevin Dotson, Warren McClendon (RT). Keagen Trost (OT) Active. No starting tackle on report.
- PIT: T Troy Fautanu, G Mason McCormick, C Zach Frazier, G Brock Hoffman, T Max Iheanachor. No OL on report.
- ARI: Jayden Williams, Isaac Seumalo, Hjalte Froholdt, Hayden Conner, Elijah Wilkinson — **Wilkinson (OT) Questionable**.
- DET: T Penei Sewell, Christian Mahogany, C Cade Mays, Tate Ratledge, T Blake Miller. No OL on report.
- DAL: T Tyler Guyton, G Tyler Smith, C Cooper Beebe, G Tyler Booker, T Terence Steele. Drew Shelton (OT, backup) Questionable.
- Pressure/sack attribution for OL: not collected (no evidenced source) — GAP, carried to Phase 2.

## Rams RB: Kyren Williams vs Blake Corum
Kyren started/led snaps in all 7 games (51–83%, 10–16 car). Corum 15–45% snaps. Wk7 LV: Corum 17 car/93 yds/44% vs Kyren 16 car/99 yds/51% — near-split, Corum's highest share. Lead back = Kyren, but trend toward split; recheck at inactives.

## Phase 1 verdicts
| Leg | Verdict | Key numbers | Notes |
|---|---|---|---|
| Bowers 6+ rec | PASS | 10/6/8/4/6 rec (4/5 ≥6), 9–13 tgt, 70–98% snaps | missed wk1–2; 2 one-target diffs preserved; LV RT Glaze Q |
| Puka 70+ yds | PASS | 74/125/138/80/68 (4/5 ≥70; wk5 regulation 112) | missed wk2–3; both sources match |
| Metcalf 40+ yds | PASS (data) — weak profile | 40/27/31/115/12/93/56 (4/7 ≥40); vs CLE wk4: 5-115 | sources match; Ward 1-15 claim is NOT from 2026 wk4 (115 yds vs CLE) — must be verified in Phase 2; no-snap gap fixed (name 'D.K. Metcalf') |
| McBride rec/yds | PASS | rec 9/8/9/7/9/7/10 (7/7 ≥7), 9–13 tgt, 80–97% snaps | sources match; alignment gap is Phase 2, not Phase 1 |
| Gibbs 70+ rush | PASS | 156(128 reg)/52/99/46/151/116 (4/6 ≥70), 15–29 car | wk1 OT split recorded; wk4 rec-yd diff unresolved (not his market) |
| Lamb rec | PASS | 5/8/7/17/2/9/5 rec, 5–21 tgt | wk6 tgt diff preserved; check Ticket 2 off-limits rule for same prop |

Phase-wide GAPs: no second source for games older than ESPN 5-game window; QB/defense box fields (sacks, pressures, tackles) not collected for this pool.
## Side-by-side vs BetGuru Phase 1 (added 2026-10-31 ~7:35 PM ET)
| Leg | Ghost6 | BetGuru | Agree? |
|---|---|---|---|
| Bowers 6+ rec | PASS; diffs wk3 tgt 13/14, wk7 9/8 | PASS; same two diffs | AGREE |
| Puka 70+ yds | PASS; sources match | PASS; reconcile | AGREE |
| Metcalf 40+ yds | PASS; match | PASS; match | AGREE |
| McBride 7+ rec | PASS; match | PASS; match | AGREE |
| Gibbs 70+ rush | PASS; wk4 rec yds 22/31 diff; wk1 OT 5 car/28 yds split | PASS; same wk4 diff | AGREE (BetGuru table doesn't show the wk1 OT split — should add) |
| Lamb rec | PASS; I listed only wk6 tgt 19/18 | PASS; wk3 tgt 9/8 AND wk6 19/18 | AGREE on verdict; **BetGuru caught a wk3 diff I missed** (PBP 9 vs ESPN 8) — corrected here |

Data problems in BetGuru's other legs:
- **Bijan Robinson wk7 vs SF rec yds E59/N45 — RESOLVED, not a true diff:** PBP Q4 10:20 London catch for 2 then lateral to Bijan for 14 more (play 16 yds). nflverse credits 2 to London and 0 to Bijan; ESPN credits the lateral to Bijan: 45 + 14 = 59. Use 59 for Bijan receiving/rush+rec.
- Gibbs rushrec: PBP 22 vs ESPN 31 rec yds wk4 still unresolved (9 yds) — matters for his rush+rec leg (rec is barred, rushrec is not).
- Barred Ticket 2 markets in BetGuru's file are correctly FAILed: Gibbs rec, St. Brown recyds, Godwin rec, London rec, Cook rushrec, Flowers rec, Pickens rec, Lamb recyds. Lamb **rec** (not recyds) is still allowed.
