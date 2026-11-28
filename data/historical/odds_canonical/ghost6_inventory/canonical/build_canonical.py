import csv,json,gzip,collections
from datetime import datetime
csv.field_size_limit(10**9)
src='sportsbook_observations.csv'; out='canonical/CANONICAL_PREGAME_GHOST6.csv'
def ts(s):
    try:
        d=datetime.fromisoformat(s); return d if d.tzinfo else None
    except Exception: return None
with open(src,newline='') as f:
    r=csv.DictReader(f); H=r.fieldnames; rows=list(r)
ex=collections.Counter(); status_all=collections.Counter(r['pregame_status'] for r in rows)
elig=[]
for i,x in enumerate(rows):
    s=ts(x['snapshot_timestamp']); e=ts(x['event_start_timestamp'])
    if s is None: ex['missing_or_invalid_or_naive_snapshot_timestamp']+=1; continue
    if e is None: ex['missing_or_invalid_event_start']+=1; continue
    if not s<e: ex['snapshot_not_strictly_before_start']+=1; continue
    if x['pregame_status']!='verified_capture_before_start': ex['status_not_verified:'+x['pregame_status']]+=1; continue
    elig.append((s,x['source_filepath'],x['source_row_id'],x['observation_id'],i,x))
# audit: verified status but fails time test
inconsist=sum(1 for x in rows if x['pregame_status']=='verified_capture_before_start' and not (ts(x['snapshot_timestamp']) and ts(x['event_start_timestamp']) and ts(x['snapshot_timestamp'])<ts(x['event_start_timestamp'])))
K=('game_id','bookmaker','market','period','player','selection','line')
g=collections.defaultdict(list)
for t in elig: g[tuple(t[5][k] for k in K)].append(t)
best=[];dupg=0;conf=[];tied=0
for k,v in g.items():
    v.sort(key=lambda t:t[:5]); best.append(v[0])
    if len(v)>1: dupg+=1
    e=[t for t in v if t[0]==v[0][0]]
    if len(e)>1:
        tied+=1
        if len({t[5]['price'] for t in e})>1: conf.append({'key':list(k),'snapshot':e[0][5]['snapshot_timestamp'],'prices':[t[5]['price'] for t in e],'observation_ids':[t[3] for t in e],'kept':v[0][3]})
best.sort(key=lambda t:t[4])
# line format collisions: keys identical except line numeric-equal but text differs
lf=collections.defaultdict(set)
for k in g:
    try: lf[k[:6]+(float(k[6]),)].add(k[6])
    except: pass
linecoll=[[list(k[:6]),sorted(s)] for k,s in lf.items() if len(s)>1]
OH=H+['canonical_source','provenance_notes']
with open(out,'w',newline='') as f:
    w=csv.writer(f); w.writerow(OH)
    for t in best:
        x=t[5]; w.writerow([x[h] for h in H]+['Ghost6',f"source_filepath={x['source_filepath']} | flags={x['flags']}"])
# validation
with open(out,newline='') as f: o=list(csv.DictReader(f))
assert len({tuple(x[k] for k in K) for x in o})==len(o)
assert all(ts(x['snapshot_timestamp'])<ts(x['event_start_timestamp']) for x in o)
mins={k:min(t[0] for t in v) for k,v in g.items()}
assert all(ts(x['snapshot_timestamp'])==mins[tuple(x[k] for k in K)] for x in o)
import hashlib
with open(out,'rb') as f, gzip.open(out+'.gz','wb') as z: z.write(f.read())
with open(out) as f: prev=[next(f) for _ in range(21)]
open('canonical/first20_preview.csv','w').writelines(prev)
S=dict(input_rows=len(rows),pregame_status_counts=status_all,exclusions=ex,eligible_rows=len(elig),verified_status_but_fails_time_test=inconsist,unique_keys_output_rows=len(o),duplicate_key_groups=dupg,rows_removed_by_dedup=len(elig)-len(o),tied_earliest_groups=tied,tied_earliest_price_conflicts=len(conf),line_format_collisions=len(linecoll),tie_break='snapshot_timestamp, source_filepath, source_row_id, observation_id, source row order',provenance_sep="'source_filepath=<path> | flags=<flags>'",validation='unique keys, strict pregame, earliest-per-key, columns preserved: PASS')
json.dump(S,open('canonical/summary.json','w'),indent=1,default=dict)
json.dump({'price_conflicts':conf,'line_format_collisions':linecoll},open('canonical/audit_conflicts.json','w'),indent=1)
print(json.dumps(S,indent=1,default=dict))
