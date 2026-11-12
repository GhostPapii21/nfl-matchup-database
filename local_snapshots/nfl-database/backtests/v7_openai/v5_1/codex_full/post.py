"""Post-run: lock reads (sha256), build picks from reads/*.json, apply locked v5.1 selector, grade with shared harness. Usage: post.py [--partial]"""
import json,sys,hashlib,subprocess,re
from pathlib import Path
import pandas as pd, numpy as np
H=Path(__file__).resolve().parent; P=Path('/workspace/nfl-database/backtests/yardage_markets_wk3_8/v4/packs')
partial='--partial' in sys.argv; tagp='PARTIAL' if partial else 'FINAL'
J=sorted((H/'reads').glob('*.json'))
(H/'reads_LOCK.sha256').write_text(''.join(f"{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.name}\n" for f in J))
rows=[]
for f in J:
    w=int(f.stem.split('_')[0][1:]); game=f.stem.split('_',1)[1]; j=json.loads(f.read_text())
    pr=pd.read_csv(P/f'w{w}'/'props_main.csv')
    pr=pr[pr.market.isin(['rushyds','recyds','rushrecyds'])&(pr.tier=='main')&(pr.game==game)].sort_values(['snap','book','candidate_id']).drop_duplicates(['player','market','side'],keep='last')
    for x in j.get('edge_players') or []:
        if x.get('confidence')=='pass':continue
        r=pr[(pr.player==x['player'])&(pr.market==x['market'])&(pr.side==x['side'])].iloc[0]
        rows.append(dict(week=w,game=game,player=r.player,team=r.team,opp=r.opp,market=r.market,side=r.side,line=r.line,price=r.price,confidence=x['confidence'],verdict=j['data_check']['verdict'],why=x.get('edge_sentence')))
pd.DataFrame(rows).to_csv(H/'codex_picks_from_json.csv',index=False)
g=pd.DataFrame(rows); l=pd.read_csv(H.parent/'data/lines_noact.csv')
ids=l[['week','player','market','side','gsis','game_id']].drop_duplicates(['week','player','market','side'])
g=g.merge(ids,on=['week','player','market','side'],how='left'); g['tag']='RECONSTRUCTED'
miss=g.gsis.isna().sum(); g=g[g.gsis.notna()]
v5=pd.read_csv(H.parent/'data/v5_reads.csv'); done={(int(f.stem.split('_')[0][1:]),f.stem.split('_',1)[1]) for f in J}
sv=v5[(v5.tag=='SAVED_READ')&np.array([(r.week,r.game) in done for r in v5.itertuples()])]
(H/'data').mkdir(exist_ok=True); fr=pd.concat([g,sv],ignore_index=True).drop_duplicates(['week','game_id','gsis','market','side','line'])
fr.to_csv(H/'data/fresh_reads.csv',index=False)
subprocess.run([sys.executable,str(H/'v5_1.py'),'--reads',str(H/'data/fresh_reads.csv'),'--lines',str(H.parent/'data/lines_noact.csv')],check=True)
# shared harness
src=(H.parent/'harness.py').read_text().split("g5=")[0].replace("B='../../'","B='/workspace/nfl-database/backtests/'").replace("'../data/player_games_2026.csv'","'/workspace/nfl-database/backtests/v7_openai/data/player_games_2026.csv'")
ns={};exec(src,ns);grade,summ,dec,B=ns['grade'],ns['summ'],ns['dec'],ns['B']
fp=grade(pd.read_csv(H/'out/v5_1_picks.csv'))
g5=pd.read_csv(B+'yardage_markets_wk3_8/v5/graded_picks.csv');v5p=grade(g5[g5.tag.isin(['SAVED_READ','RECONSTRUCTED'])][['week','game','game_id','gsis','player','market','side','line','price']])
v5same=v5p[np.array([(r.week,r.game) in done for r in v5p.itertuples()],dtype=bool)]
lk=grade(pd.read_csv(H.parent/'out/v5_1_picks.csv'))
v6=pd.read_csv(B+'v6_brainstorm_proedge/graded_picks.csv');v6=v6[v6.bucket.str.startswith('a_wk3-8')].copy();v6['split']=np.where(v6.week<=6,'train(3-6)','holdout(7-8)')
bl=pd.read_csv(B+'yardage_markets_wk3_8/v5/graded_baseline.csv');bl['split']=np.where(bl.week<=6,'train(3-6)','holdout(7-8)')
rows=[]
sets=[('v5.1 FRESH Grok (partial)',grade(pd.read_csv(H.parent/'fresh/out/v5_1_picks.csv'))),('v5.1 CODEX reads',fp),('v5 PRIMARY (all games)',v5p),('v5 PRIMARY (same games as fresh)',v5same),('v5.1 locked-reads',lk),('v6 READS',v6[v6.origin=='READ']),('v6 GATED',v6[v6.gate=='PASS']),('rush-under baseline',bl)]
for n,d in sets:
    for sp in ['train(3-6)','holdout(7-8)']:
        x=d[d.split==sp]
        if len(x)==0: rows.append([n,sp,0,0,np.nan,0,0.0,np.nan]);continue
        s=summ(x.assign(k=1),['k']).iloc[0];rows.append([n,sp,int(s.W),int(s.L),s.hit,int(s.priced),round(s.pl,2),s.roi])
T=pd.DataFrame(rows,columns=['set','split','W','L','hit','priced','pl','roi'])
tr=T[(T.set=='v5.1 CODEX reads')&(T.split=='train(3-6)')].iloc[0];v5t=T[(T.set=='v5 PRIMARY (all games)')&(T.split=='train(3-6)')].iloc[0]
c=[tr.priced>=40,tr.roi>0,tr.roi>v5t.roi,tr.pl>v5t.pl]
verdict='PASS' if all(c) else ('FAIL' if not c[1] or not (c[2] and c[3]) else 'INSUFFICIENT')
if not c[0] and verdict=='PASS': verdict='INSUFFICIENT'
# slips: pre-registered <=5/week from v5_1.py; plus <=5 per game DAY variant (same rule per kickoff date ET)
def slipgrade(sl):
    if len(sl)==0:return pd.DataFrame(columns=['slip_id','week','pl'])
    sl=grade(sl)
    def r(x):
        if (x.result=='LOSS').any():return -10.0
        live=x[(x.result=='WIN')&x.price.notna()];return 10*(np.prod(dec(live.price))-1) if len(live) else 0.0
    return sl.groupby(['slip_id','week']).apply(r,include_groups=False).rename('pl').reset_index()
S=slipgrade(pd.read_csv(H/'out/v5_1_slips.csv'))
ko=l[['game_id','kickoff']].drop_duplicates('game_id');ko['day']=pd.to_datetime(ko.kickoff,utc=True).dt.tz_convert('America/New_York').dt.date.astype(str)
ns2={'__file__':str(H/'v5_1.py')};exec((H/'v5_1.py').read_text().split('def main')[0],ns2)
pk=pd.read_csv(H/'out/v5_1_picks.csv').merge(ko[['game_id','day']],on='game_id')
D=[]
for day,gr in pk.groupby('day'):
    s=ns2['make_slips'](gr.drop(columns='day'))
    if len(s): s['slip_id']=s.slip_id+'_'+day; s['day']=day; D.append(s)
SD=slipgrade(pd.concat(D).drop(columns='day')) if D else pd.DataFrame(columns=['slip_id','week','pl'])
sw=lambda S:S.groupby('week').pl.agg(won=lambda p:f"{(p>0).sum()}/{len(p)}",pl=lambda p:round(p.sum(),2))
gap=("v5 gap resolved: Week 6 NYJ@NE Kenyon Sadiq recyds OVER 20.5 (actual 12, LOSS) carried an invalid saved price of -6. "
     "v5 grade.py treated it as unpriced (−$119.83); the first shared-harness pass decoded -6 as odds and booked −$10 (−$129.83). "
     "Harness now treats |price|<100 as unpriced; v5 Weeks 3-6 = −$119.83. The locked-reads v5.1 also kept Sadiq at -6, so its Wk3-6 moves from −$11.58 to −$1.58 (21 priced).")
nr=len(J); out=[f"# v5.1 CODEX reads — {tagp} results ({nr}/88 games read; {miss} picks unmatched to lines)\n",
 f"Pre-registered verdict (Wk3-6: >=40 priced, ROI>0, beats v5 ROI and $): **{verdict}{' (PARTIAL — not final)' if partial else ''}** — priced {tr.priced}, ROI {tr.roi}, $ {tr.pl} vs v5 {v5t.roi}/{v5t.pl}\n",
 "## Side by side\n",T.to_markdown(index=False),
 "\n## FRESH by week\n",summ(fp,['week']).to_markdown() if len(fp) else 'none',
 "\n## FRESH by split x market x side\n",summ(fp,['split','market','side']).to_markdown() if len(fp) else 'none',
 "\n## FRESH by split x side\n",summ(fp,['split','side']).to_markdown() if len(fp) else 'none',
 "\n## Slips, pre-registered (<=5/week, 3-4 legs, $10)\n",sw(S).to_markdown() if len(S) else 'none',
 "\n## Slips, <=5 per game day variant ($10)\n",sw(SD).to_markdown() if len(SD) else 'none',
 "\n## Grading gap\n",gap,
 "\n## OpenAI usage\n",f"Logged cost ${sum(json.loads(x).get('est_usd',0) for x in open(H/'usage_log.jsonl')):.2f} (est.; stop at $38 logged, $40 cap). Rejects: {sum(1 for _ in open(H/'rejects_log.jsonl')) if (H/'rejects_log.jsonl').exists() else 0}. Dropped: {', '.join(re.findall(r'DROPPED (\S+)',(H/'reads.log').read_text())) or 'none'}. Stops: {'; '.join(re.findall(r'STOPPED.*',(H/'reads.log').read_text()))[:300] or 'none'}"]
name='results_PARTIAL.md' if partial else 'results.md'
(H/name).write_text('\n'.join(out)); fp.to_csv(H/('graded_PARTIAL.csv' if partial else 'graded.csv'),index=False)
print('\n'.join(out))
if not partial:(H/'.done').write_text(verdict+'\n')
