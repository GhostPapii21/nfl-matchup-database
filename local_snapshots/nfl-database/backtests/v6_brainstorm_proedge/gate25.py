"""v6 2025 lock stage (bucket c, HINDSIGHT RISK). Derived from gate.py (NO outcomes). Reads -> picks -> data check AFTER brainstorm+pro-edge.
Uses tools/depth_rule.evaluate, tools/rico4_rules.mirror_eligible and rules/rulebook params READ-ONLY (imported, not edited)."""
import sys,json,math,re
import pandas as pd,numpy as np
from scipy.stats import norm
from common import *
sys.path.insert(0,str(DB));sys.path.insert(0,str(DB/'tools'))
from rules import rulebook as RB
import depth_rule
from rico4_rules import mirror_eligible
MIN_EDGE=RB.param('NOSHRINK','min_edge');MIN_P=RB.param('NOSHRINK','min_model_p');N1MIN=RB.param('N1','min_share')
pl=pd.read_parquet(PLAYERS);POS=dict(zip(pl.gsis_id,pl.position))
def prior_pbp(w):
    pb=clean(pd.read_parquet(PB25));pb=pb[pb.week<w];assert (pb.week<w).all();return pb,f'2025 weeks < {w}'
def props(w):
    return pd.read_csv(ROOT/f'packs25/w{w}/props_standin.csv'),pd.DataFrame()
    q=pd.read_csv(V4/f'w{w}/props_main.csv');q=q[q.market.isin(MK)&(q.tier=='main')];full=q.copy()
    q=q.sort_values(['snap','book','candidate_id']).drop_duplicates(['player','market','side'],keep='last').copy();q['line_src']='saved main line ('+q.book+')';return q,full
def fair(full,r):
    if not len(full):return None
    q=full[(full.player==r.player)&(full.market==r.market)&(full.line==r.line)]
    for b in['pinnacle','circa','betonlineag','consensus']:
        qb=q[q.book==b].sort_values('snap');o=qb[qb.side=='over'];u=qb[qb.side=='under']
        if len(o) and len(u) and pd.notna(o.price.iloc[-1]) and pd.notna(u.price.iloc[-1]):
            po,pu=imp(o.price.iloc[-1]),imp(u.price.iloc[-1]);return (po if r.side=='over' else pu)/(po+pu)
    return None
rows=[]
for w in range(2,19):
    pb,lab=prior_pbp(w);L=logs(pb);q,full=props(w)
    l3w=sorted(pb.week.unique())[-3:];l3=pb[pb.week.isin(l3w)]
    for f in sorted((ROOT/'reads25').glob(f'w{w}_*.json')):
        j=json.loads(f.read_text());game=f.stem.split('_',1)[1]
        g=q[q.game==game]
        for x in [x for x in j['edge_players'] if x.get('confidence')!='pass']:
            for mirror in (False,):
                r=g[(g.player==x['player'])&(g.market==x['market'])&(g.side==x['side'])].iloc[0]
                rows.append(dict(week=w,game=game,game_id=r.game_id,gsis=r.gsis,player=r.player,team=r.team,opp=r.opp,market=r.market,side=r.side,line=r.line,price=r.price,line_src=r.line_src,
                    confidence=x['confidence'],grok_model_p=x.get('model_p'),verdict=j['data_check']['verdict'],why=x['edge_sentence'],scheme=json.dumps(x.get('scheme')),prim_def=json.dumps(x.get('primary_defender')),
                    depth_sp=x.get('depth_script_pass'),depth_dg=x.get('depth_defender_giving'),pro_edge_support=x.get('pro_edge_support',''),origin='READ'))
P=pd.DataFrame(rows)
def check(r,L,l3,full,allow_scheme=True):
    cut=[];flag=[];notes=[]
    PL=L[L.gsis==r.gsis]
    cur_qb=L[L.posteam==r.team].qb.iloc[-1] if len(L[L.posteam==r.team]) else None
    PQ=PL[PL.qb==cur_qb] if cur_qb is not None and r.week>1 else PL
    last4=PQ.tail(4)[r.market].values;allg=PL[r.market].values
    hit=lambda v:(v>r.line) if r.side=='over' else (v<r.line)
    s7=int(hit(last4).sum()) if len(last4) else None
    if s7 is None:notes.append('§7 N/A no prior games')
    elif s7<min(3,len(last4)) or (len(last4)>=4 and s7<3):cut.append(f'§7 {s7}/{len(last4)} with current QB')
    p1=hit(last4).mean() if len(last4) else np.nan;p2=hit(allg).mean() if len(allg) else np.nan
    p3=(1-norm.cdf(r.line,allg.mean(),max(allg.std(ddof=0),0.35*allg.mean()+5)) if r.side=='over' else norm.cdf(r.line,allg.mean(),max(allg.std(ddof=0),0.35*allg.mean()+5))) if len(allg) else np.nan
    mp=np.nanmean([p1,p2,p3]) if len(allg) else np.nan
    fv=fair(full,r);edge=mp-fv if fv is not None and np.isfinite(mp) else None
    if edge is None:notes.append('edge N/A (no no-vig)')
    elif edge<MIN_EDGE or mp<MIN_P:cut.append(f'edge {edge*100:+.1f} pts (p {mp:.3f} vs fair {fv:.3f})')
    sc=json.loads(r.scheme) if isinstance(r.scheme,str) else None
    scheme_ok=isinstance(sc,dict) and all(isinstance(sc.get(k),dict) and sc[k].get('ok') is True and len(str(sc[k].get('source','')))>5 for k in RB.param('SCHEME_EDGE','keys'))
    if scheme_ok and allow_scheme and cut:flag+=['SCHEME_EDGE: '+'; '.join(cut)];cut=[]
    pos=POS.get(r.gsis)
    if pos=='RB' and r.market in('rushyds','rushrecyds'):
        t=l3[(l3.posteam==r.team)&(l3.rush_attempt==1)];rbc=t[t.rusher_player_id.map(lambda z:POS.get(z)=='RB')]
        sh=(rbc.rusher_player_id==r.gsis).mean() if len(rbc) else None
        if sh is None:cut.append('N1 carry share missing')
        elif sh<N1MIN:cut.append(f'N1 DO NOT PLAY carry share {sh:.0%}')
        else:notes.append(f'N1 share {sh:.0%}')
    if r.market in('recyds','rushrecyds'):
        pd_=json.loads(r.prim_def) if isinstance(r.prim_def,str) else {}
        if not (isinstance(pd_,dict) and len(str(pd_.get('who','')))>2 and len(str(pd_.get('source','')))>5):cut.append('N2 no primary defender with source')
        else:notes.append('N2 APPROX (defender/coverage area named from pack, no charting)')
    tt=l3[(l3.posteam==r.team)&(l3.pass_attempt==1)].dropna(subset=['receiver_player_id'])
    sh=tt.receiver_player_id.value_counts(normalize=True)
    wr=[z for z in sh.index if POS.get(z)=='WR'];te=[z for z in sh.index if POS.get(z)=='TE']
    leg=dict(side=r.side,type=pos if pos in('WR','TE') else pos,wr_rank=(wr.index(r.gsis)+1 if r.gsis in wr else (9 if pos=='WR' else None)),te_rank=(te.index(r.gsis)+1 if r.gsis in te else (9 if pos=='TE' else None)),
        rung='low',price=None if pd.isna(r.price) else r.price,no_vig=fv,depth=dict(script_pass=dict(ok=bool(r.depth_sp),source='grok read script + spread'),target_share=dict(value=float(sh.get(r.gsis,0)),source='as-of pbp L3'),defender_giving=dict(ok=bool(r.depth_dg),source='grok read + pack defense YPA')))
    if r.market!='rushyds':
        ok,why=depth_rule.evaluate(leg)
        if not ok:cut.append('DEPTH_RECEIVER: '+'; '.join(why))
    if pd.notna(r.price) and r.price<=-250:flag.append('PRICE -250 or shorter')
    return dict(sec7=s7,model_p=mp,fair=fv,edge=edge,scheme_ok=scheme_ok,gate='CUT' if cut else ('FLAG' if flag else 'PASS'),cut_reasons=' | '.join(cut),flags=' | '.join(flag),notes=' | '.join(notes))
out=[];mir=[]
for w,Pw in P.groupby('week'):
    pb,_=prior_pbp(w);L=logs(pb);q,full=props(w);l3=pb[pb.week.isin(sorted(pb.week.unique())[-3:])]
    for r in Pw.itertuples():
        c=check(r,L,l3,full);out.append({**r._asdict(),**c})
        if r.side=='under' and c['gate']=='CUT' and mirror_eligible(c['cut_reasons']):
            o=q[(q.player==r.player)&(q.market==r.market)&(q.side=='over')]
            if len(o):
                o=o.iloc[0];m=r._asdict()|dict(side='over',line=o.line,price=o.price,origin='MIRROR',scheme=None,depth_sp=False,depth_dg=False)
                mr=pd.Series(m);mr=type('R',(),m)();c2=check(mr,L,l3,full,allow_scheme=False);mir.append({**m,**c2})
A=pd.DataFrame(out+mir).drop(columns=['Index'],errors='ignore')
A['steps']='BRAINSTORM(12 steps, in prompt)>PRO_EDGE(skill in prompt + precomputed inputs)>DATA_CHECK(§7,NOSHRINK+3,SCHEME_EDGE flag,N1,N2approx,DEPTH,mirror,-250 flag)'
A['priced']=False;A['bucket']='c_2025_STAND-IN_HINDSIGHT_RISK'
A.to_csv(ROOT/'locked_picks_2025.csv',index=False)
print(A.groupby(['origin','gate']).size());print(A.cut_reasons.str.extract(r'^(\w+|§7)')[0].value_counts())
