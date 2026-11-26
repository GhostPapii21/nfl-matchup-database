import csv,json,collections,zipfile,hashlib,random,re
from pathlib import Path
from datetime import datetime
P=Path(__file__).parent
s=json.loads((P/'summary.json').read_text())
rs=list(csv.DictReader((P/'sportsbook_observations.csv').open()))
fields=list(rs[0]);latest={};w9=[]
for r in rs:
 if r['pregame_status']!='verified_capture_before_start':continue
 if r['week']=='9':w9.append(r)
 k=tuple(r[x] for x in ['game_id','bookmaker','market','period','player','selection','line'])
 if k not in latest or datetime.fromisoformat(r['snapshot_timestamp'])>datetime.fromisoformat(latest[k]['snapshot_timestamp']):latest[k]=r
for name,data in [('sportsbook_latest_verified_pregame.csv',latest.values()),('week9_verified_pregame.csv',w9)]:
 with (P/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(data)
s['latest_verified_pregame_quote_rows']=len(latest);s['week9_verified_pregame_rows']=len(w9)
periods=collections.defaultdict(lambda:collections.Counter())
for r in rs:
 if r['pregame_status']=='verified_capture_before_start':periods[r['week']][r['period']]+=1
s['verified_pregame_periods_by_week']={k:dict(v) for k,v in periods.items()}
(P/'summary.json').write_text(json.dumps(s,indent=2))
readme=f'''# Existing historical NFL odds inventory — November 7, 2026 (ET)

Local-only research export. No network/API requests, credits, repository writes, PR updates, model changes, or messages. Originals preserved. This is source recovery, not independent verification that cached vendor responses were accurate or executable.

## Recommended staging files
- `sportsbook_latest_verified_pregame.csv`: {len(latest):,} outcome quotes; latest explicitly captured pre-start observation for each game/book/market/period/player/selection/line. Different lines remain separate. Not a closing-line claim.
- `week9_verified_pregame.csv`: {len(w9):,} explicitly captured pre-start Week 9 observations, retaining historical snapshots.
- `sportsbook_observations.csv`: {s['sportsbook_rows']:,} normalized historical sportsbook observations across {s['sportsbook_games']} games, 12 named books, actual schedule Weeks 3–9. Includes unknown-capture and after-start rows: FILTER `pregame_status` before using for pregame research.
- `retrospective_game_lines_book_unknown.csv`: {s['retrospective_feed_rows']:,} full-game outcome rows from saved nflverse schedule, Weeks 1–9, book and quote timestamp unknown. Not point-in-time observations and not verified closing prices. No prices filled in.
- `non_sportsbook_platform_observations.csv`: {s['non_sportsbook_rows']:,} pick'em/exchange observations kept separate, not counted as sportsbook coverage.
- `coverage_by_week_book_market.csv`, `summary.json`, `source_manifest.csv`, `provenance.csv`: counts and complete per-observation source-file/row mapping.
- `source_artifacts/`: content-deduplicated source copies keyed by SHA256. Manifest maps each original path to packaged copy and records original and packaged hashes. JSON canonicalized and credential keys/query parameters redacted; schedule copy filtered to 2026 REG Weeks 1–9. No credential files opened or packaged.

## Coverage / limits
Books: {', '.join(s['sportsbook_books'])}.

| Actual week | Sportsbook observations | Games | Explicitly captured pre-start |
|---|---:|---:|---:|
'''
for week,v in s['by_week'].items():readme+=f"| {week} | {v['rows']:,} | {v['games']} | {v['pregame_rows']:,} |\n"
readme+='''
- Weeks 1–2: only retrospective full-game lines in saved schedule found; no priced, named-book point-in-time sportsbook props recovered. Stand-in/simulated prop lines in the v6 hit-rate backtest are excluded.
- Weeks 3–5: recovered full-game player rushing, receiving, and rush+receiving yardage markets. No quarter/half game markets recovered there.
- Week 6: full game plus selected H1/Q1 markets, sparse Q2–Q4 spreads/totals. Player Q1 receiving/rushing yards and H1 rushing yards exist, not a comprehensive slate. IMPORTANT: all recovered Week 6 quarter/half observations lack explicit capture timestamps; none qualify for the verified-pregame subset (book updates alone are insufficient).
- Weeks 7–8: full-game game lines and props; no quarter/half coverage in recovered sources.
- Week 9: full-game game lines and selected props across 15 games; quarter/half markets limited to JAX@BAL. Sunday line-watch covers 13 games; DraftKings game lines and FanDuel game/prop lines have differing availability. Preserve native market names (`spread` vs `spreads`, `receiving_yards` vs `player_reception_yds`); not economically deduplicated across vendor taxonomies.
- Missing Q/H/prop books/markets are gaps, not evidence no markets existed. No wholesale historic slate, no executable SGP quotes, no guaranteed opener/closing observations.
- `hist_props_oddsapi/lines.parquet` was checked via its README: intentionally EMPTY, exhausted quota, zero historical games. It is NOT included as odds evidence. Historical raw files under `hist_props` also contain January 2026 games from a prior season; these are excluded by game schedule matching.
- A saved source folder may be mislabeled: Nov 1/Nov 2 = actual Week 8; JAX@BAL Nov 5 = Week 9, although `line_movement_wk10` calls it Week 10. Use the saved 2026 NFL regular-season schedule `game_id`/week, not directory names. All datetime matching uses America/New_York calendar date, so UTC next-day kickoffs map correctly.
- `pregame_status=verified_capture_before_start` means source explicitly records snapshot/pull/fetch time before event start (not external authentication of the quote). Source update alone cannot prove capture before start; these are `update_before_start_capture_unknown`. At/after-start rows are never in recommended pregame files. Historical snapshot timestamp may differ from pull time; historical API snapshot is used when present. File mtime is NEVER quote/capture time.
- Preserve source timestamp offsets; normalized timestamps are ISO8601 with offsets and supplementary `snapshot_et`/`event_start_et` fields. ET is America/New_York (-04:00 or -05:00 as appropriate). Source originals remain in packaged copies. Naive explicitly-labeled `pulled_et` metadata localized to America/New_York.
- `odds_format` inferred from numeric scale (absolute value >=100 American, positive >1 and <100 decimal) where absent; flagged as inferred. No conversion or implied/no-vig probability calculation. NULL CSV values are empty cells. nflverse handicap signs translated from home-favored spread_line into selection handicap; source feed retains original sign in schedule copy.
- Exact normalized rows deduplicated with all timestamp/flag fields retained. Different snapshots, source feeds, update timestamps, and quote lines remain distinct; counts are correlated outcome observations, NOT independent bets. `source_occurrences` and `provenance.csv` preserve duplicates. Latest quote file is a compact per-line view, not a single final market.
- Discovery was bounded to canonical local NFL repositories/caches and existing NFL line-watch ledger. Worktree/review clone copies were not re-read; no claim all data anywhere on disk was found. Oversized/nonmatching JSON and non-supported formats were not mined. Raw sources with out-of-scope dates can remain in source copies; only normalized requested-week data should be staged as usable evidence.
'''
(P/'README.md').write_text(readme)
# Verify counts, hashes, provenance accounting, timestamps, and representative exact outcomes against JSON/CSV sources.
assert len(rs)==s['sportsbook_rows']
allids=set();occ=0
for name in ['sportsbook_observations.csv','retrospective_game_lines_book_unknown.csv','non_sportsbook_platform_observations.csv']:
 for r in csv.DictReader((P/name).open()):
  assert r['observation_id'] not in allids;allids.add(r['observation_id']);occ+=int(r['source_occurrences'])
assert occ==s['source_occurrences']
assert sum(1 for _ in csv.DictReader((P/'provenance.csv').open()))==occ
for r in latest.values():assert datetime.fromisoformat(r['snapshot_timestamp'])<datetime.fromisoformat(r['event_start_timestamp'])
for r in csv.DictReader((P/'source_manifest.csv').open()):assert hashlib.sha256((P/r['packaged_path']).read_bytes()).hexdigest()==r['packaged_sha256']
checks=[]
for r in random.Random(7).sample(rs,30):
 src=Path(r['source_filepath']);ptr=r['source_row_id']
 if ptr.startswith('csv_line:'):
  with src.open() as f:orig=next(x for i,x in enumerate(csv.DictReader(f),2) if i==int(ptr.split(':')[1]))
  assert float(orig['price'])==float(r['price'])
 elif ptr.startswith('$'):
  obj=json.loads(src.read_text());tokens=re.findall(r'\.([^\.\[\]]+)|\[(\d+)\]',ptr)
  for a,b in tokens:obj=obj[a] if a else obj[int(b)]
  assert float(obj['price'])==float(r['price']);assert obj.get('point') is None or float(obj['point'])==float(r['line'])
 elif ptr.startswith('jsonl_line:'):
  orig=json.loads(next(l for i,l in enumerate(src.open(),1) if i==int(ptr.split(':')[1])))
  assert float(orig['price'])==float(r['price'])
 checks.append(r['observation_id'])
validation={'status':'passed','total_unique_observations':len(allids),'provenance_occurrences_checked':occ,'source_hash_checks':len(list(csv.DictReader((P/'source_manifest.csv').open()))),'sampled_sportsbook_outcome_price_checks':len(checks),'sample_ids':checks,'latest_verified_pregame_rows':len(latest),'week9_verified_pregame_games':len({r['game_id'] for r in w9})}
(P/'validation.json').write_text(json.dumps(validation,indent=2))
zip_path=P/'historical_nfl_odds_2026_weeks1_9.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(P.rglob('*')):
  if p.is_file() and p!=zip_path and p.suffix not in ['.py']:z.write(p,p.relative_to(P))
with zipfile.ZipFile(zip_path) as z:assert z.testzip() is None
assert zip_path.stat().st_size<25000000
print(json.dumps({'zip_path':str(zip_path),'zip_bytes':zip_path.stat().st_size,'latest_pregame_rows':len(latest),'validation':validation,'pregame_periods':s['verified_pregame_periods_by_week']},indent=2))
