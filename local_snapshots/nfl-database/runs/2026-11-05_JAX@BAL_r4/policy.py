"""r3 policy overlay (parent steer 2026-11-03 19:31 ET). Read-only on held master files.
Date gate 2026-11-10 (mirrors 3b3560b rico4 CALIBRATED_SHRINK): before it, anchored and raw-sim edges FLAG only.
Pre-gate judgement: locked read fit, N1 (hard cut), §7 3-of-4 (MISSING/FAIL cut), last-2 (hard downgrade), depth/role.
+7 bar only for backup-QB-dependent legs (BAL pass/receiving). Best price shopped FD/DK/Pinnacle same point; CLV open at best book.
PFF 2-defender blend = FLAG only."""
import json, math, datetime as dt, pandas as pd
GATE=dt.date(2026,11,10); TODAY=dt.date(2026,11,3); PRE=TODAY<GATE
A,B=-0.014863178010206913,0.022983299151190368
lg=lambda p:math.log(min(max(p,1e-6),1-1e-6)/(1-min(max(p,1e-6),1-1e-6)))
cal=lambda s,n:1/(1+math.exp(-(lg(n)+A+B*(lg(s)-lg(n)))))
R2='../2026-11-05_JAX@BAL_r2/'
legs=json.load(open(R2+'legs.json'))['legs']
O=pd.read_csv('odds/odds_jaxbal.csv'); MK={'rushyds':'player_rush_yds','recyds':'player_reception_yds','rec':'player_receptions','rushrec':'player_rush_reception_yds'}
P4=dict(pd.read_csv('phase4_receivers.csv')[['receiver','phase4']].values)
pbp=pd.read_parquet(R2+'src/play_by_play_2026.parquet',columns=['game_id','game_date','week','home_team','away_team','posteam','rusher_player_name','receiver_player_name','passer_player_name','rushing_yards','rush_attempt','total_home_score','total_away_score','qtr'])
ABBR=lambda n:n.split()[0][0]+'.'+n.split()[1]
def rush_last4(n,t):
    """r4 fix (Ghost6): window = last 4 games PLAYED (pbp presence as rusher, receiver or passer for team t), 0 carries filled.
    Limitation: a snaps-only game with no touch/target is invisible in pbp (no participation/snap file locally) -> flag."""
    a=ABBR(n); tp=pbp[pbp.posteam==t]
    pres=tp[(tp.rusher_player_name==a)|(tp.receiver_player_name==a)|(tp.passer_player_name==a)].game_date.unique()
    r=tp[(tp.rush_attempt==1)&(tp.rusher_player_name==a)].groupby('game_date').rushing_yards.sum()
    return [float(r.get(g,0.0)) for g in sorted(pres)[-4:]]
# locked read (r2 brainstorm_read.md sha 76b563a3…5685) mapped to legs
READ={('Derrick Henry','rushyds','under'):'EDGE1',('Derrick Henry','rushrec','under'):'EDGE1-family',('Justice Hill','rec','over'):'EDGE2',
      ('Justice Hill','recyds','over'):'EDGE2-family',('Trevor Lawrence','rushyds','under'):'SLIP-STORY',('Justice Hill','rushyds','under'):'BASE-consistent (BAL pass-heavy, Hill checkdown role)'}
AVOID={'Zay Flowers','Rashod Bateman'}
def to_dec(a): return 1+(a/100 if a>0 else 100/-a)
def shop(L):
    """Best decimal price across FD/DK/Pinnacle at the same point. No FD fallback: a missing quote is flagged NO_QUOTE."""
    side='Over' if L['side']=='over' else 'Under'; mk=MK[L['market']]; mk=mk+('_alternate' if L['rung']!='main' else '')
    q=O[(O.player==L['player'])&(O.market==mk)&(O.side==side)&(O.point==L['line'])&O.book.isin(['fanduel','draftkings','pinnacle'])]
    if q.empty: return 'NO_QUOTE',None,{}
    b=q.loc[q.price.map(to_dec).idxmax()]; return b.book,int(b.price),dict(zip(q.book,q.price))
out=[]
for L in legs:
    k=(L['player'],L['market'],L['side']); ps=[v for v in L['p'].values()]; s=sum(ps)/len(ps); nv=L['no_vig']
    qb_dep=L['team']=='BAL' and L['market'] in('rec','recyds')
    if L['market']=='rushyds':
        v=[float(x) for x in rush_last4(L["player"],L["team"])]; src7='pbp last 4 games (any QB; rush leg not QB-dependent)'
    else:
        v=L['last4_cur_qb']; src7='last 4 with current QB'
    hit=lambda x:(x<L['line']) if L['side']=='under' else (x>L['line'])
    s7='MISSING' if len(v)<4 else ('PASS' if sum(map(hit,v))>=3 else 'FAIL'); s7=f"{s7} {sum(map(hit,v))}/{len(v)} {v} ({src7})"
    l2=v[-2:]; l2s='n/a' if len(l2)<2 else ('OK' if all(map(hit,l2)) else 'DOWNGRADE')
    n1='n/a (not rush over)'
    QBS={'Trevor Lawrence','Joe Fagnano'}
    if L['market']=='rushyds' and L['side']=='over' and L['player'] in QBS: n1='n/a (QB; N1 is an RB rule)'
    elif L['market']=='rushyds' and L['side']=='over':
        cs=L.get('carry_share'); n1='CUT (unsourced)' if cs is None else ('CUT <60%' if cs<.6 else f'OK {cs:.0%}')
    if L['market']=='rushyds' and L['side']=='under': n1=f"exempt (under); carry share {L.get('carry_share')}"
    role=[w for w in L['why'] if w.startswith('#3/#4') or 'DEPTH' in w]
    opp=(L['player'],L['market'],'over' if L['side']=='under' else 'under')
    read=READ.get(k,'AVOID (read)' if (L['player'] in AVOID and L['side']=='over') else ('AVOID (opposite of locked read '+READ[opp]+')' if opp in READ else 'off-read'))
    bar=7 if qb_dep else 5; pa=cal(s,nv); ae=(pa-nv)*100; re=(s-nv)*100
    flags=[f'anchored {ae:+.2f} vs +{bar}' + (' (FLAG pre-11-10)' if PRE else ''), f'raw sim {re:+.1f} (FLAG)']
    if L['player'] in P4: flags.append('PFF/P4: '+P4[L['player']])
    cut=[]
    if n1.startswith('CUT'): cut.append('N1')
    if not s7.startswith('PASS'): cut.append('§7 '+s7.split()[0])
    if role: cut+=role
    if read.startswith('AVOID'): cut.append('locked read AVOID')
    if not PRE and ae<bar: cut.append('edge bar')
    st='CUT' if cut else ('PASS-DOWNGRADE' if l2s=='DOWNGRADE' else ('PASS' if read!='off-read' else 'PASS (off-read, singles only)'))
    bk,bp,allp=shop(L)
    if bk=='NO_QUOTE': flags.append('NO_QUOTE at FD/DK/Pinnacle for this point')
    out.append(dict(player=L['player'],team=L['team'],market=L['market'],side=L['side'],line=L['line'],rung=L['rung'],status=st,read=read,
        N1=n1,s7=s7,last2=f"{l2s} {l2}",role='; '.join(role) or 'ok',cut='; '.join(cut),fd_price=L['price'],best_book=bk,best_price=bp,shop=allp,
        clv_open_book=bk,clv_open_price=bp,clv_close=None,fd_no_vig=round(nv,4),sim_avg3=round(s,4),anchored_edge=round(ae,2),raw_edge=round(re,1),bar=bar,flags=' | '.join(flags)))
df=pd.DataFrame(out); df.to_csv('policy_legs.csv',index=False)
print('pre-gate' if PRE else 'post-gate', df.status.value_counts().to_dict())
print(df[~df.status.eq('CUT')][['player','market','side','line','status','read','N1','s7','last2','best_book','best_price','shop','anchored_edge','raw_edge']].to_string())
