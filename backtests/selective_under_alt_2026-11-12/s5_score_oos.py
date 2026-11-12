"""Step 5: score frozen control rule, frozen strong markets and frozen selector on Weeks 8-9 (out of sample);
slip study on Weeks 8-9 only; compare with Rico's actual NFL tickets from the bet log."""
import json, re, itertools, hashlib, numpy as np, pandas as pd
from common import *
assert hashlib.sha256(open(HERE+'/selector_frozen.json','rb').read()).hexdigest() in open(HERE+'/FROZEN_WK4_7.sha256').read()
C=load_cands(); S=json.load(open(HERE+'/selector_frozen.json')); ST=json.load(open(HERE+'/strong_markets_wk4_7.json'))['strong']
IS=C[C.week.between(4,7)]; OOS=C[C.week.between(8,9)]
assert set(IS.week)&set(OOS.week)==set() and set(IS.game_id)&set(OOS.game_id)==set(), 'train/test overlap'
assert IS.week.max()<=7 and OOS.week.min()>=8
rows=[]
for X in XGRID:
    for lab,D in (('IS_wk4_7',IS),('OOS_wk8_9',OOS)):
        t=table(control_flags(D,X),['kind','market']); t.insert(0,'set',lab); t.insert(0,'X',X); rows.append(t)
R=pd.concat(rows); R.to_csv(HERE+'/results_control_is_oos.csv',index=False)
sel=[]
for lab,D in (('IS_wk4_7',IS),('OOS_wk8_9',OOS)):
    t=table(apply_selector(D,S),['kind','market']); t.insert(0,'set',lab); sel.append(t)
SR=pd.concat(sel); SR.to_csv(HERE+'/results_selector_is_oos.csv',index=False)
# per-week OOS (control X=+5 and selector)
pw=[]
for lab,f in (('control_X5',control_flags(OOS,0.05)),('selector',apply_selector(OOS,S))):
    for (wk,kd,mk),g in f.groupby(['week','kind','market']):
        sm=summarize(g,B=2000); pw.append(dict(rule=lab,week=wk,kind=kd,market=mk,**{k:sm[k] for k in ('n','hit','be','margin','roi','small')}))
pd.DataFrame(pw).to_csv(HERE+'/results_oos_by_week.csv',index=False)
# alt direction split (control X=+5)
ad=[]
for lab,D in (('IS_wk4_7',IS),('OOS_wk8_9',OOS)):
    f=control_flags(D,0.05); f=f[f.kind=='alt'].copy()
    f['direction']=np.where(f.market=='spread',np.where(f.rung>f.main_line,'alt-more-points(safer)','alt-fewer-points(riskier)'),
                            np.where(f.side=='Under','under','over'))
    for (mk,dr),g in f.groupby(['market','direction']):
        sm=summarize(g,B=2000); ad.append(dict(set=lab,market=mk,direction=dr,**{k:sm[k] for k in ('n','hit','be','margin','roi','small')}))
    cand=D[D.kind=='alt']
    for mk,g in cand.groupby('market'):
        ad.append(dict(set=lab,market=mk,direction='CANDIDATE PRICES AVAILABLE',n=len(g),hit=np.nan,be=np.nan,margin=np.nan,roi=np.nan,
                       small=','.join(sorted(g.side.astype(str).unique())) if mk not in ('spread',) else 'team sides'))
pd.DataFrame(ad).to_csv(HERE+'/results_alt_direction.csv',index=False)
# strong markets OOS
f5=control_flags(OOS,0.05); keys={(s['kind'],s['market']) for s in ST}
fs=f5[[ (k,m) in keys for k,m in zip(f5.kind,f5.market)]].copy()
strong_oos=table(fs,['kind','market']); strong_oos.to_csv(HERE+'/results_strong_oos.csv',index=False)
# slip study (Weeks 8-9 only), legs from strong markets
fs['lm']=fs.p_model-fs.be
slips=[]
for k in (2,3,4):
    for wk,g in fs.groupby('week'):
        g=g.sort_values('lm',ascending=False)
        top=g.drop_duplicates('game_id').head(k)
        if len(top)==k:
            pr=np.prod(top.dec.values); res=np.where(top.push==1,1,top.win).astype(float)
            cash=bool((res==1).all()); slips.append(dict(kind='greedy_top',k=k,week=wk,n_slips=1,cash_rate=float(cash),
                roi=float((pr*np.prod(np.where(top.push==1,1/top.dec,1)) - 1) if cash else -1),legs=';'.join(top.market+':'+top.kind)))
        # all disjoint-game combinations (descriptive; overlapping, correlated)
        # exact enumeration of ALL k-leg slips with one leg per game, via per-game generating polynomials
        cnt=np.array([1.0]); csh=np.array([1.0]); pay=np.array([1.0])
        for _,gg in g.groupby('game_id'):
            okg=((gg.win==1)|(gg.push==1)).values; dv=np.where(gg.push==1,1.0,gg.dec.values)
            cnt=np.convolve(cnt,[1,len(gg)]); csh=np.convolve(csh,[1,okg.sum()]); pay=np.convolve(pay,[1,(dv*okg).sum()])
        if len(cnt)>k and cnt[k]>0:
            slips.append(dict(kind='all_one_leg_per_game(exact)',k=k,week=wk,n_slips=int(cnt[k]),cash_rate=float(csh[k]/cnt[k]),
                              roi=float(pay[k]/cnt[k]-1),legs=f'{len(g)} flagged legs in {g.game_id.nunique()} games'))
SL=pd.DataFrame(slips); SL.to_csv(HERE+'/results_slips_oos.csv',index=False)
# Rico's actual NFL tickets (bet log)
B=pd.read_csv('/workspace/bet-log.csv'); B=B[B.sport=='NFL']
bh=hashlib.sha256(open('/workspace/bet-log.csv','rb').read()).hexdigest()
def week_of(bid,game):
    s=f'{bid} {game}'
    for pat,w in [(r'1112|11/12',10),(r'OCT11|SF @ SEA|BUF @ LAR|DAL/TB',5),(r'1015|1018|1019|HOU @ JAX|WAS @ SF',6),(r'1022|1025',7),
                  (r'1029|1030|11/1\b|Sun 11/1|Nov 2|CHI@SEA',8),(r'1105|JAX @ BAL',9)]:
        if re.search(pat,s): return w
    return None
T=B.groupby('bet_id').agg(status=('ticket_status','first'),game=('game','first'),odds=('sub_sgp_odds','first'),legs=('player','size')).reset_index()
T['week']=[week_of(b,g) for b,g in zip(T.bet_id,T.game.astype(str))]
txt=(T.bet_id.fillna('').astype(str)+' '+T.status.fillna('').astype(str)+' '+T.odds.fillna('').astype(str)).str.lower()
T['excluded']=np.select([txt.str.contains('paper|no stake|leans',regex=True).values,T.status.fillna('').astype(str).str.lower().str.contains('cashed out|pending|open',regex=True).values],
                        ['paper/no stake','void/pending/open'],'')
def price(o):
    o=str(o); m=re.search(r'([0-9.]+)x',o)
    if m: return float(m.group(1))
    m=re.search(r'\+(\d+)',o); return 1+int(m.group(1))/100 if m else np.nan
T['dec']=T.odds.map(price); T['won']=T.status.astype(str).str.startswith('Win')
T['unit_profit']=np.where(T.won,T.dec-1,-1.0)
T.loc[T.won&T.dec.isna(),'unit_profit']=np.nan
T.to_csv(OUT+'/betlog_tickets_parsed.csv',index=False)
A=T[(T.excluded=='')&T.week.between(4,9)]
act=[]
for lab,ws in (('Wk8-9',(8,9)),('Wk4-9',(4,9))):
    a=A[A.week.between(*ws)]
    act.append(dict(set=lab,tickets=len(a),cashed=int(a.won.sum()),cash_rate=float(a.won.mean()) if len(a) else np.nan,
                    unit_roi=float(a.unit_profit.mean()) if a.unit_profit.notna().all() else np.nan,
                    mean_legs=float(a.legs.mean()) if len(a) else np.nan,unknown_week=int(T.week.isna().sum())))
AC=pd.DataFrame(act); AC.to_csv(HERE+'/results_actual_slips.csv',index=False)
json.dump(dict(betlog_sha256=bh,scored_et=pd.Timestamp.now(tz='America/New_York').isoformat()),open(HERE+'/oos_run_meta.json','w'),indent=1)
pd.set_option('display.width',260)
c=['X','set','kind','market','n','W','L','P','hit','be','margin','margin_lo','margin_hi','roi','roi_lo','roi_hi','small']
print(R[c].round(3).to_string(index=False)); print(SR[c[1:]].round(3).to_string(index=False)); print(strong_oos[c[2:]].round(3).to_string(index=False))
print(SL.round(3).to_string(index=False)); print(AC.round(3).to_string(index=False))
print(T[['bet_id','week','status','dec','legs','excluded']].to_string(index=False))
