# Historical integration record

`test_historical_pre_rebind.py` retains the original SHA assertion and all five
progressive missing-field expectations. Every case is skipped with explicit reason
`HISTORICAL_PRE_REBIND_RECORD`; this suite does not gate live acceptance.

Run separately using the same PYTHONPATH as the live suite:

```bash
python3 -m pytest integration/tests/historical -q -rs -p no:cacheprovider
```

The `.pre_refresh.txt` files are byte-for-byte snapshots of the previous live
suite, protected inventory, packet, and packet builder. They are archival data,
not runnable live code. The previous logs and JSON evidence remain at their
original paths. Frozen wire metadata keeps its historical binding and is not
rewritten. Current authority is `wire/CONTRACT_BINDING_AUTHORIZATION_2026-11-06.md`.
