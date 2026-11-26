import zipfile, io, pandas as pd, gzip, hashlib, csv
Z=zipfile.ZipFile('../NFL_HISTORICAL_ODDS_2026_W1_9_v2.zip')
raw=Z.read('SCOPED_2026_W1_9_STRICT_PREGAME.csv')
D=pd.read_csv(io.BytesIO(raw),dtype=str,keep_default_na=False); cols=list(D.columns); N0=len(D)
D['_ord']=range(N0)
snap=pd.to_datetime(D.snapshot_ts_utc,utc=True,errors='coerce'); kick=pd.to_datetime(D.commence_time_utc,utc=True,errors='coerce')
D['_snap']=snap
ex={'snapshot_blank_or_invalid':int(snap.isna().sum()),'kickoff_blank_or_invalid':int((kick.isna()&snap.notna()).sum()),'snapshot_equal_kickoff':int((snap==kick).sum()),'snapshot_after_kickoff':int((snap>kick).sum())}
V=D[snap.notna()&kick.notna()&(snap<kick)].copy()
V['_gid']=V.game_id.where(V.game_id!='',V.event_id)
# line key: exact string; check numeric normalization necessity
def nl(x):
  try: return repr(float(x)) if x!='' else ''
  except: return x
K=['_gid','book','market','period','player','outcome']
grp_str=V.groupby(K+['line']).ngroups; V['_lnum']=V.line.map(nl); grp_num=V.groupby(K+['_lnum']).ngroups
V['_line']=V.line
null_audit={c:int((V[c]=='').sum()) for c in ['game_id','event_id','book','market','period','player','outcome','line']}
KK=K+['_line']
V=V.sort_values(['_snap','_ord'],kind='mergesort')
g=V.groupby(KK,sort=False)
V['_n']=g._ord.transform('size'); V['_np']=g.price.transform('nunique')
mins=g._snap.transform('min'); E=V[V._snap==mins]
ge=E.groupby(KK,sort=False)
tie_n=ge._ord.transform('size'); tie_price=ge.price.transform('nunique')
other=[c for c in cols if c not in('snapshot_ts_utc',)]
tie_other=ge[other].transform(lambda s:s.nunique()).max(axis=1) if False else None
C=E.drop_duplicates(KK,keep='first').copy()
# collision audit
dupg=V[V._n>1].groupby(KK).agg(rows=('_ord','size'),distinct_prices=('price','nunique'),price_variants=('price',lambda s:'|'.join(sorted(set(s)))),first_snap=('snapshot_ts_utc','min'),last_snap=('snapshot_ts_utc','max')).reset_index()
Et=E[tie_n>1].copy()
tie=Et.groupby(KK).agg(tie_rows=('_ord','size'),tie_distinct_prices=('price','nunique'),tie_price_variants=('price',lambda s:'|'.join(sorted(set(s)))),tie_distinct_rowvalues=('_ord',lambda i: Et.loc[i.index,cols].drop_duplicates().shape[0])).reset_index()
dupg=dupg.merge(tie,on=KK,how='left').rename(columns={'_gid':'game_or_event_id','_line':'line'})
dupg.to_csv('COLLISION_AUDIT.csv',index=False)
C=C.sort_values('_ord')
C['canonical_source']='Blitz'
C['provenance_notes']='source_path='+C.source_path+'; observation_pregame_status='+C.observation_pregame_status+'; quote_update_before_kick='+C.quote_update_before_kick+'; snapshot_verified_before_kickoff=True'
out=C[cols+['canonical_source','provenance_notes']]
b=out.to_csv(index=False).encode()
with gzip.open('CANONICAL_PREGAME_BLITZ.csv.gz','wb',9) as f: f.write(b)
out.head(20).to_csv('CANONICAL_PREGAME_BLITZ_FIRST20.csv',index=False)
# validations
chk=pd.read_csv(gzip.open('CANONICAL_PREGAME_BLITZ.csv.gz'),dtype=str,keep_default_na=False)
assert list(chk.columns)==cols+['canonical_source','provenance_notes'] and len(chk)==len(out)
kc=chk.game_id.where(chk.game_id!='',chk.event_id)
assert not pd.concat([kc,chk[['book','market','period','player','outcome','line']]],axis=1).duplicated().any()
assert (pd.to_datetime(chk.snapshot_ts_utc,utc=True)<pd.to_datetime(chk.commence_time_utc,utc=True)).all()
m=V.groupby(KK)._snap.min(); cc=C.set_index(KK)._snap; assert (cc.reindex(m.index)==m).all()
for c in cols: assert (chk[c].values==D.loc[C._ord.values,c].values).all()
sha=hashlib.sha256(open('CANONICAL_PREGAME_BLITZ.csv.gz','rb').read()).hexdigest()
nd=int((dupg.rows>1).sum()); npc=int((dupg.distinct_prices>1).sum())
tg=dupg[dupg.tie_rows>1]
S=dict(N0=N0,valid=len(V),excluded=N0-len(V),ex=ex,after=len(C),removed=len(V)-len(C),dup_groups=nd,price_conflict_groups=npc,tie_groups=len(tg),tie_price_conflict=int((tg.tie_distinct_prices>1).sum()),tie_other_conflict=int((tg.tie_distinct_rowvalues>1).sum()),grp_str=grp_str,grp_num=grp_num,null=null_audit,sha=sha,uncompressed=len(b),wk=C.groupby('week').size().to_dict())
open('CANONICAL_SUMMARY.md','w').write(f'''# CANONICAL_PREGAME_BLITZ summary
Source: NFL_HISTORICAL_ODDS_2026_W1_9_v2.zip :: SCOPED_2026_W1_9_STRICT_PREGAME.csv (package unchanged). Read as strings; all original raw values preserved.
- Input rows: {N0}
- Timing re-check (snapshot_ts_utc vs commence_time_utc, parsed tz-aware UTC; prior status field ignored): excluded {N0-len(V)} {ex}; valid {len(V)}
- After dedup: {len(C)} (removed {len(V)-len(C)})
- Key: (game_id if nonblank else event_id, book, market, period, player, outcome, line). Price not in key. Exact strings. Line compared as exact string; numeric normalization would give {grp_num} groups vs {grp_str} exact, so {"no normalization needed" if grp_num==grp_str else "normalization would change grouping; exact string kept"}.
- Null/blank key audit (valid rows): {null_audit}. Blank player = game-line markets (kept, blank is a key value).
- Duplicate key groups (>1 row): {nd}; groups with >1 distinct price across snapshots: {npc}
- Earliest-snapshot ties (>1 row at min snapshot): {len(tg)}; with conflicting prices: {S["tie_price_conflict"]}; with any differing original values: {S["tie_other_conflict"]}
- Rules: keep earliest snapshot < kickoff; ties are broken by stable original input order (first row in source file). Output is the retained rows in original input order. Added columns: canonical_source='Blitz', provenance_notes.
- Retained by week: {S["wk"]}
- CANONICAL_PREGAME_BLITZ.csv.gz sha256 {sha}; uncompressed {len(b)} bytes. COLLISION_AUDIT.csv = per duplicate group rows, price variants, and tie stats.
- Validations passed: unique keys, all snapshots < kickoff, earliest per key, column order = original + 2, raw values equal source, gzip readable.
''')
print(S)
