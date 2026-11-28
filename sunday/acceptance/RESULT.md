# Sunday command acceptance (NFL-92)

Recorded before this change was committed, so `git_sha` inside the packets is `4d010ede51a1acc5a1d49b5396a0463520cc0f2a`. A later replay records the new revision and a new canonical sha256. Wall time and RSS are not part of that hash. `projection_ready` is false in every file.

## Tests

```text
python3 -m pytest -q -p no:cacheprovider sunday/tests/test_sunday.py
..................                                                       [100%]
18 passed in 1.12s
```

## DEN@PIT replay

```text
python3 -m sunday replay --game 2026_12_DEN_PIT --out sunday/acceptance/den_pit_week12
sunday: 2026_12_DEN_PIT PARTIAL reproducibility=PASS
```

As-of `2026-11-27T04:31:50+00:00` (the packet `generated_utc`, before the 20:00 UTC kickoff).

| | Run A | Run B |
| --- | --- | --- |
| Result | PARTIAL | PARTIAL |
| Wall time | 0.151724 s | 0.145483 s |
| Memory | tracemalloc peak 1903308 bytes; process max RSS 28820 KB | tracemalloc peak 1794040 bytes; process max RSS 28884 KB |

Canonical sha256 (both runs): `264dd71e9ea921dfb5027ec79a5e659bf6125e42a1c30de2c88822ba3eab554d`

Critical checks: none failed. PARTIAL because the offline packet has no publisher as-of stamp on several nflverse sources, some phase rows are not AUTO, and NFL-87 through NFL-91 have no registered module. Schedule, news injuries, odds, the four-book freeze, and the NGS matchup check were FRESH at this as-of. Official inactives were NOT_YET (before T-90). The later locked snapshot, the final play log, the postgame projection, the ESPN summary, and `runs/2026-11-27_DEN@PIT/` are listed under leakage exclusions and were not read. The 100k entry point was not called.

Packet: `sunday/acceptance/den_pit_week12/run_a/2026_12_DEN_PIT/packet.json`

## Sunday 2026-11-29 slate

```text
python3 -m sunday slate --date 2026-11-29 --as-of 2026-11-29T12:00:00+00:00 --concurrency 4 --out sunday/acceptance/sunday_2026-11-29
sunday slate: 0 PASS, 10 PARTIAL, 0 BLOCKED
```

Concurrency used 4, cap 8, peak in-flight 4. Process max RSS 30300 KB. No game was BLOCKED. At this later as-of, live schedule and odds pulls from the Nov 27 packets are stale, which is why those rows are gaps here and were not gaps in the DEN replay.

| Game | Result | Wall seconds |
| --- | --- | --- |
| 2026_12_ATL_MIN | PARTIAL | 0.259409 |
| 2026_12_BAL_HOU | PARTIAL | 0.265653 |
| 2026_12_NO_CIN | PARTIAL | 0.278996 |
| 2026_12_NYG_IND | PARTIAL | 0.270407 |
| 2026_12_NYJ_MIA | PARTIAL | 0.271084 |
| 2026_12_TEN_JAX | PARTIAL | 0.269307 |
| 2026_12_NE_LAC | PARTIAL | 0.248853 |
| 2026_12_SEA_SF | PARTIAL | 0.25833 |
| 2026_12_WAS_ARI | PARTIAL | 0.101512 |
| 2026_12_LV_CLE | PARTIAL | 0.094584 |

Index: `sunday/acceptance/sunday_2026-11-29/INDEX.md`
