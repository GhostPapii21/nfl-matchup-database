"""Post-lock: apply Nov-4 rules to codex reads and grade. Pre-registered arm = v5.1 selector (strong+agree).
Exploratory arm (POST-HOC, disclosed): lean|strong + agree, because gpt-6.1-sol tagged only 3/149 legs 'strong'.
Rules: no TD/pass-yds (already), N1 cut (RB rushyds OVERS only: <60% of non-QB team carries over prior <=3 games),
§7 3-of-4 cut (last 4 games played per snap counts, zero-touch=0, line cleared on pick side >=3), last-2 both-against = downgrade FLAG,
arms A/B/C: edges flag-only; arm CT: Rico +1/+3 anchored tiers (<+1 cut, +1..+3 lean, >=+3 full; former +7 = flag), sims flag-only (none used),
best saved pre-kick price at same line (lines_noact), slips 3-4 legs <=5 per game DAY, one slip per player, $10."""
import pandas as pd,numpy as np,json
from pathlib import Path
H=Path(__file__).resolve().parent
src=(H.parent/'harness.py').read_text().split("g5=")[0].replace("B='../../'","B='/workspace/nfl-database/backtests/'").replace("'../data/player_games_2026.csv'","'/workspace/nfl-database/backtests/v7_openai/data/player_games_2026.csv'")
ns={};exec(src,ns);grade,summ,dec,pg=ns['grade'],ns['summ'],ns['dec'],ns['pg']
L=pd.read_csv(H.parent/'data/lines_noact.csv');L=L[L.price.abs()>=100]
r=pd.read_csv(H/'data/fresh_reads.csv')
r=r[(r.tag=='RECONSTRUCTED')]  # codex reads only (saved Rico reads excluded so arm = model)
import re as _re
nm=lambda z:_re.sub('[^a-z]','',str(z).lower())
# FIX (Ghost6 vet 5): games played = nflverse snap counts (offense_snaps>0, pre-kick weeks only); zero-touch games kept with 0 filled in
SN=pd.read_parquet('/workspace/nfl-database/runs/2026-11-01_shared_src/snap_counts_2026.parquet');SN=SN[(SN.offense_snaps>0)&(SN.game_type=='REG')]
SN['pk']=SN.player.map(nm)
key=r[['player','team','gsis']].drop_duplicates()
GP=SN.merge(key,left_on=['pk','team'],right_on=['player','team'])[['game_id','week','gsis','team']].drop_duplicates()
TM=pg[['game_id','posteam','team_rushes']].drop_duplicates(['game_id','posteam'])
QB=pg[pg.gsis==pg.qb][['game_id','posteam','car']].rename(columns={'car':'qc'})
TM=TM.merge(QB,on=['game_id','posteam'],how='left').fillna({'qc':0})
ST=pg[['game_id','gsis','car','rushyds','tgt','recyds','rushrecyds','qb']]
G=GP.merge(ST,on=['game_id','gsis'],how='outer',indicator=True)
G['week']=G.week.fillna(G.game_id.str.slice(5,7).astype(float))
G=G.merge(TM,left_on=['game_id',G.team.fillna(G.game_id)],right_on=['game_id','posteam'],how='left') if False else G
for c in ['car','rushyds','tgt','recyds','rushrecyds']:G[c]=G[c].fillna(0)
G['zero_touch']=G._merge=='left_only'
pt=pg[['game_id','gsis','posteam']];G=G.merge(pt,on=['game_id','gsis'],how='left');G['posteam']=G.posteam.fillna(G.team)
G=G.merge(TM,on=['game_id','posteam'],how='left')
def feats(x):
    h=G[(G.gsis==x.gsis)&(G.week<x.week)].sort_values('week')
    v=h[x.market].fillna(0).tolist()
    ok=[(a>x.line) if x.side=='over' else (a<x.line) for a in v]
    l4=ok[-4:];s7=sum(l4)>=3 and len(l4)>=4
    l2=len(ok)>=2 and not ok[-1] and not ok[-2]
    h3=h.tail(3);rbc=(h3.team_rushes-h3.qc).sum()
    n1=None
    # FIX (Ghost6 vet 1): N1 = RB rushyds OVERS only (B13; review-branch rico_nov2_rules excludes rushrec and unders)
    if x.market=='rushyds' and x.side=='over' and not (h3.gsis==h3.qb).all() and rbc>0:n1=h3.car.sum()/rbc
    return pd.Series({'s7_pass':s7,'s7_hits':f"{sum(l4)}/{len(l4)}",'s7_vals':[round(a) for a in v[-4:]],'zero_touch_in_l4':int(h.tail(4).zero_touch.sum()),'last2_down':l2,'n1_share':n1})
r=pd.concat([r.reset_index(drop=True),r.reset_index(drop=True).apply(feats,axis=1)],axis=1)
r['n1_cut']=r.n1_share.notna()&(r.n1_share<0.6)
# best saved pre-kick price, same line, any book
b=L.sort_values('price',key=lambda p:dec(p.values)).drop_duplicates(['week','gsis','market','side','line'],keep='last')[['week','gsis','market','side','line','price','book','kickoff']]
r=r.drop(columns='price').merge(b,on=['week','gsis','market','side','line'],how='left')
o=L.drop_duplicates(['week','gsis','market','side','line','book'])
def novig(x):
    q=o[(o.week==x.week)&(o.gsis==x.gsis)&(o.market==x.market)&(o.line==x.line)&(o.book==x.book)]
    a=q[q.side==x.side].price;c=q[q.side!=x.side].price
    if len(a)==0 or len(c)==0:return np.nan
    pa,pc=1/dec(a.iloc[0:1].values)[0],1/dec(c.iloc[0:1].values)[0];return pa/(pa+pc)
r['p_mkt']=r.apply(novig,axis=1)
# Rico +1/+3 anchored-edge tiers (Nov 4 04:37 ET, effective now): <+1 cut, +1..<+3 lean, >=+3 full. Former +7 legs: flag only (no role labels in backtest data -> no effect).
# anchored p = market-anchored Platt (avg3|0.5: a=-0.01486, b=+0.02298) on the 3-sim avg from rulebook_replay_wk6_8/sims_replay.csv (Wk6-8 only). No sim -> no model edge -> cut (same as r5).
SM=pd.read_csv('/workspace/nfl-database/backtests/rulebook_replay_wk6_8/sims_replay.csv');SM['avg3']=SM[['p_mc','p_bias','p_gr']].mean(axis=1)
SM=SM.drop_duplicates(['week','gsis','market','thr'])[['week','gsis','market','thr','avg3']]
r=r.merge(SM,left_on=['week','gsis','market','line'],right_on=['week','gsis','market','thr'],how='left').drop(columns='thr')
lg=lambda p:np.log(np.clip(p,1e-6,1-1e-6)/(1-np.clip(p,1e-6,1-1e-6)))
ps=np.where(r.side=='over',r.avg3,1-r.avg3)
r['p_anch']=1/(1+np.exp(-(lg(r.p_mkt)-0.014863178010206913+0.022983299151190368*(lg(ps)-lg(r.p_mkt)))))
r['anch_edge']=100*(r.p_anch-r.p_mkt)
r['tier']=np.select([r.anch_edge.isna(),r.anch_edge>=3,r.anch_edge>=1],['cut (no model edge)','full','lean'],'cut')
r.to_csv(H/'data/legs_today_rules.csv',index=False)
def arm(df):
    k=df[(df.verdict=='agree')&~df.n1_cut&df.s7_pass&df.price.notna()]
    return grade(k[['week','game','game_id','gsis','player','market','side','line','price','book','kickoff','last2_down','p_mkt','confidence','tier','anch_edge']])
A=grade(r[(r.confidence=='strong')&(r.verdict=='agree')&r.price.notna()][['week','game','game_id','gsis','player','market','side','line','price','p_mkt','kickoff']])
B=arm(r[r.confidence=='strong']);C=arm(r[r.confidence.isin(['strong','lean'])]);CT=C[C.tier.isin(['lean','full'])];C0=grade(r[r.confidence.isin(['strong','lean'])&(r.verdict=='agree')&r.price.notna()][['week','game','game_id','gsis','player','market','side','line','price','p_mkt','kickoff']])
def slips(d):
    d=d[d.result.isin(['WIN','LOSS','PUSH'])].copy();d['day']=pd.to_datetime(d.kickoff,utc=True).dt.tz_convert('America/New_York').dt.date.astype(str)
    out=[]
    for day,g in d.groupby('day'):
        pool=g.sort_values(['last2_down','game_id','gsis'],kind='mergesort') if 'last2_down' in g else g.sort_values(['game_id','gsis'])
        used=set()
        for n in range(5):
            ch=[];gs=set()
            for i,x in pool.iterrows():
                if x.gsis in used or x.game_id in gs:continue
                ch.append(i);gs.add(x.game_id);used.add(x.gsis)
                if len(ch)==4:break
            if len(ch)<3:break
            s=pool.loc[ch];pool=pool.drop(index=ch)
            pl=-10.0 if (s.result=='LOSS').any() else 10*(np.prod(dec(s[s.result=='WIN'].price.values))-1)
            out.append(dict(week=int(s.week.iloc[0]),day=day,legs=len(s),pl=pl))
    return pd.DataFrame(out,columns=['week','day','legs','pl'])
def brier(d):
    x=d[d.result.isin(['WIN','LOSS'])&d.p_mkt.notna()];y=(x.result=='WIN').astype(float)
    return len(x),round(((x.p_mkt-y)**2).mean(),4) if len(x) else np.nan
rep=["# EXPLORATORY / POST-HOC — NOT AN EDGE. v5.1 CODEX full rerun (gpt-6.1-sol), Nov-4 rules applied after grading was visible\n",__doc__,"\nModel p = market-anchored (Platt b≈0.02 ⇒ p≈no-vig), so Brier(model)≈Brier(market); reported as market Brier on picked side.\n"]
for n,d in [('A pre-registered v5.1 (strong+agree)',A),('B A + Nov-4 rules',B),('C0 EXPLORATORY lean|strong+agree, no Nov-4 rules',C0),('C EXPLORATORY lean|strong+agree + Nov-4 rules (no tiers)',C),('CT EXPLORATORY C + Rico +1/+3 tiers',CT)]:
    rep.append(f"\n## {n}\n")
    if len(d)==0:rep.append('no legs');continue
    u=d[d.result=='UNRESOLVED']
    if len(u):rep.append('UNRESOLVED (no nflverse player-game row; not graded, not dropped silently):\n'+u[['week','game','player','market','side','line','price']].to_markdown(index=False)+'\n')
    rep.append(summ(d.assign(k=1),['week']).to_markdown());s=summ(d.assign(k=1),['k']).iloc[0]
    nb,bs=brier(d);rep.append(f"\nTOTAL {int(s.W)}-{int(s.L)} hit {s.hit} priced {int(s.priced)} P/L ${s.pl:.2f} ROI {s.roi:+.1%}; market Brier {bs} (n={nb})")
    S=slips(d)
    if len(S):
        t=S.groupby('week').agg(slips=('pl','size'),won=('pl',lambda p:(p>0).sum()),pl=('pl','sum')).round(2);rep.append('\nSlips (<=5/game day, 3-4 legs, $10):\n'+t.to_markdown()+f"\nSlips total {int((S.pl>0).sum())}/{len(S)} won, P/L ${S.pl.sum():.2f}, ROI {S.pl.sum()/(10*len(S)):+.1%}")
    else:rep.append('\nSlips: none (fewer than 3 eligible legs per day)')
    d.to_csv(H/f"graded_{n.split()[0]}.csv",index=False)
cut=r[r.confidence.isin(['strong','lean'])&(r.verdict=='agree')]
rep.append(f"\nTier counts (C pool): {C.tier.value_counts().to_dict() if len(C) else {}}; anchored edge range {r.anch_edge.min():+.2f}..{r.anch_edge.max():+.2f} pts (n with sim={r.anch_edge.notna().sum()})")
rep.append(f"\n## Rule attrition (lean|strong+agree, n={len(cut)})\nN1 cut {int(cut.n1_cut.sum())}; §7 fail {int((~cut.s7_pass).sum())}; last-2 downgrades {int(cut.last2_down.sum())}; unpriced {int(cut.price.isna().sum())}")
(H/'results_today_rules.md').write_text('\n'.join(rep));print('\n'.join(rep))
