# Paid Odds API files not on origin/main

**refs NFL-75. Data only. Not a pick list. `projection_ready` unchanged. No new API calls.**

Rico asked to save what was already paid for. These files were on disk (mostly the local `nfl-database` tree on `mws-matchup-2026-11-04`, plus the 2026-11-07 research inventory) and were **not** on `origin/main` of `GhostPapii21/nfl-matchup-database`. They are copied here under `data/odds_history/paid_uncommitted/` so this draft PR does not touch `pregame/` or `.github/`.

Every copied file was scanned for the live Odds API secret and for key query parameters or JSON key fields in stored URLs or bodies. **No keys were found; nothing was redacted.**

Per-file source path, pull time, credit headers when known, and sha256 are in [MANIFEST.csv](MANIFEST.csv).

## 1. Week 9 daily slate pulls (7)

Live Odds API slate snapshots from `/workspace/nfl-database/week9/model/raw/`, each with a saved HTTP header. Cost is `x-requests-last` from that header (2 credits each). Pull times are the HTTP `Date` values, converted to America/New_York.

| File | Pull time (ET) | Pull time (UTC) | x-requests-last | remaining | used | sha256 |
|---|---|---|---:|---:|---:|---|
| `odds_20261101_2125.json` | 2026-11-01 09:20:19 PM ET | 2026-11-02T02:20:19Z | 2 | 18484 | 1516 | `88bb7c54c5981be5f4114a4586de7c2c5dab8d16da091e6482e1a4f67c696e40` |
| `odds_20261102_1002.json` | 2026-11-02 10:02:38 AM ET | 2026-11-02T15:02:38Z | 2 | 18081 | 1919 | `936089545158960ed0b9a82cd13c82ed18c20b529ae0164d3876570e700417c3` |
| `odds_20261103_1004.json` | 2026-11-03 10:04:20 AM ET | 2026-11-03T15:04:20Z | 2 | 3610 | 16390 | `15d5fd659ef4b33067b1d437670161e00a41d88102dc6711039d3bea39377ac0` |
| `odds_20261104_1003.json` | 2026-11-04 10:03:49 AM ET | 2026-11-04T15:03:49Z | 2 | 3539 | 16461 | `b9c95a920458fde7f8994f73eb2f52e228ccfd6d38bf3091a57d49a9b66b5b32` |
| `odds_20261105_1006.json` | 2026-11-05 10:06:56 AM ET | 2026-11-05T15:06:56Z | 2 | 3354 | 16646 | `3bc0f75cfcce51c481ccca15128ab43d33161d5383d02620b5bd35974729b43f` |
| `odds_20261106_1003.json` | 2026-11-06 10:03:28 AM ET | 2026-11-06T15:03:28Z | 2 | 2311 | 17689 | `10b2f16850aaa4d8f9897dd711c978ebb604919fa4bef556e0e40d867a950f15` |
| `odds_20261107_1001.json` | 2026-11-07 10:01:42 AM ET | 2026-11-07T15:01:42Z | 2 | 2309 | 17691 | `bd1e8163c2fd3dacff371bec270bf2bd8f7ee120a99581071514e27fece4dbc8` |

Headers are stored next to each JSON (`hdr.txt` belongs to `odds_20261101_2125.json`; the others use matching `hdr_YYYYMMDD_HHMM.txt` names). Combined paid cost for these seven slates: 14 credits.

Also copied from the same folder: `props_JAXBAL_20261102_1004.json` (JAX@BAL event-odds body, 5458 bytes, sha256 `b7fea331206e422436581c2ecef901d39a41415a10c180d109cd2fe84f82b598`). Pull time and cost are **unknown** (no header). Filename suggests about 10:04 AM ET on Nov 2, 2026, but that is not a saved header.

## 2. Week 10 daily slate (Nov 11)

- File: `odds_20261111_1000.json` (28277 bytes)
- Pull time: 2026-11-11 09:55:00 AM ET (2026-11-11T14:55:00Z)
- Cost: 2 credits; remaining 2156
- Time/cost source: `week10/model/REFRESH_2026-11-11_1000.md (no saved HTTP header)` — **no saved HTTP header** for this file. Figures come from that refresh writeup.
- sha256: `d55373f5a23a599d015ffa4a1330a291b47b2baeff6bf864a8bc4a94ff3862da`

## 3. JAX@BAL / BUF@MIN line-movement pulls (9)

Nine live event-odds checkpoints from `/workspace/nfl-database/runs/line_movement_wk10/`. Each pull is stored as four files (`*.csv`, `*_game.csv`, `*_meta.json`, `*_stale.csv`). Cost is 3 credits per `/odds` call from `quota_log.csv` (the `cost` column; equivalent to `x-requests-last`). Accompanying `/events` discovery rows in the quota log cost 0 and were not separate snapshot bodies.

JAX@BAL (event `c75744790b7acf6260c78ba5e739c0e5`):

| Checkpoint | Pull time (ET) | Pull time (UTC) | cost | remaining | used |
|---|---|---|---:|---:|---:|
| open | 2026-11-05 09:02:23 AM ET | 2026-11-05T14:02:23Z | 3 | 3356 | 16644 |
| T120 | 2026-11-05 06:19:38 PM ET | 2026-11-05T23:19:38Z | 3 | 2402 | 17598 |
| T60 | 2026-11-05 07:21:08 PM ET | 2026-11-06T00:21:08Z | 3 | 2343 | 17657 |
| T30 | 2026-11-05 07:54:50 PM ET | 2026-11-06T00:54:50Z | 3 | 2316 | 17684 |
| close | 2026-11-05 08:12:42 PM ET | 2026-11-06T01:12:42Z | 3 | 2313 | 17687 |

BUF@MIN (event `17ad7eff2f7875e20a8109abe40470e3`); no saved open snapshot:

| Checkpoint | Pull time (ET) | Pull time (UTC) | cost | remaining | used |
|---|---|---|---:|---:|---:|
| T120 | 2026-11-09 06:21:20 PM ET | 2026-11-09T23:21:20Z | 3 | 2271 | 17729 |
| T60 | 2026-11-09 07:19:25 PM ET | 2026-11-10T00:19:25Z | 3 | 2268 | 17732 |
| T30 | 2026-11-09 07:54:30 PM ET | 2026-11-10T00:54:30Z | 3 | 2265 | 17735 |
| close | 2026-11-09 08:14:01 PM ET | 2026-11-10T01:14:01Z | 3 | 2222 | 17778 |

Combined paid cost for these nine `/odds` calls: 27 credits. `quota_log.csv` is included as the credit ledger. The wrapper script `.snap_gamelines_wrapper.py` was not copied (it is code, not a paid response).

## 4. Week 3–8 yardage raw and the 2026-11-07 raw_oddsapi inventory

These were to be skipped if large, and included only if combined size was under 20 MB. Measured source size was **16.56 MiB** (1.28 MiB + 15.29 MiB), so both corpora are included.

- `yardage_markets_wk3_8_raw/`: 95 files, 1,337,993 bytes. Source: `/workspace/nfl-database/backtests/yardage_markets_wk3_8/raw`. Local nfl-database commit `282e20c` (Nov 3, 2026, 6:52 AM ET). Per-file `x-requests-last` was not saved in a sidecar header.
- `raw_oddsapi_inventory_2026-11-07/`: 760 files, 16,028,012 bytes. Source: `/workspace/research/nfl_historical_odds_2026-11-07/raw_oddsapi`. Mixed NFL historical/live Odds API JSON, including older seasons. Per-file credit headers were not in sidecars; some JSON objects have `timestamp` / `previous_timestamp` / `next_timestamp` from the historical endpoint.

## Totals

- Payload files in MANIFEST.csv: **908**
- Payload bytes: **17,609,251** (16.79 MiB), not counting MANIFEST.csv / MANIFEST.md

