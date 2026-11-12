"""Masked rerun: same as-of packs + same SYS prompt/skill as v5 reads.py, but team names, player names, week numbers and dates replaced by codes. No outcomes loaded until grading."""
import json,re,random,sys,pandas as pd
from pathlib import Path
from grok import call,ROOT
V=ROOT.parent/'yardage_markets_wk3_8';PK=V/'v4'/'packs'
src=(V/'v5'/'reads.py').read_text();SYS=re.search(r'SKILL=open.*?\n(SYS=\(.*?\}\"\))',src,re.S)
SKILL=open('/home/box/agent-data/workflows/betting-game-brainstorm/SKILL.md').read()
exec(SYS.group(1))
SYS=SYS.replace('Every section must be game-specific (names, numbers from the pack).','Every section must be game-specific (use the codes and numbers from the pack). Teams and players are anonymized codes; reason from the numbers only.')
random.seed(11)
gp=pd.read_csv(V/'v5'/'grok_picks.csv')
orig=gp[(gp.week>=7)&(gp.grok_ctx.isin(['RECONSTRUCTED','SAVED_READ_CONTEXT']))]
G7=sorted(orig[orig.week==7].game.unique());G8=sorted(orig[orig.week==8].game.unique())
sample=[(7,g) for g in random.sample(G7,8)]+[(8,g) for g in random.sample(G8,8)]
def nm(s):return re.sub('[^a-z]','',str(s).lower())
def match(short,pid):
    if '.' not in str(short):return False
    f,l=short.split('.',1);return pid.endswith(nm(l)) and pid.startswith(nm(f)) 
json.dump(sample,open(ROOT/'masked_sample.json','w'))
out=[];OUT=ROOT/'masked_reads';OUT.mkdir(exist_ok=True)
for w,game in sample:
    d=PK/f'w{w}';pb=pd.read_parquet(d/'pbp_prior.parquet');ft=pd.read_parquet(d/'ftn_prior.parquet');assert (pb.week<w).all()
    pb=pb[(pb.season_type=='REG')&pb.play_type.isin(['run','pass'])]
    pr=pd.read_csv(d/'props_main.csv');gl=pd.read_csv(d/'game_lines.csv')
    pr=pr[pr.market.isin(['rushyds','recyds','rushrecyds'])&(pr.tier=='main')].sort_values(['snap','book','candidate_id']).drop_duplicates(['player','market','side'],keep='last')
    g=pr[pr.game==game];away,home=game.split('@');T={away:'AWAY',home:'HOME'}
    pids=sorted(g.player.unique());random.shuffle(pids);P={p:f'PLY{i+1:02d}' for i,p in enumerate(pids)}
    shortmap={}
    def code(short,team):
        if short in shortmap:return shortmap[short]
        c=[p for p in pids if match(short,p)]
        shortmap[short]=P[c[0]] if len(c)==1 else f'X{len(shortmap)+1:02d}';return shortmap[short]
    def ctx(team,opp):
        off=pb[pb.posteam==team];de=pb[pb.defteam==opp];wk=sorted(off.week.unique())[-3:];l3=off[off.week.isin(wk)]
        rush=l3[l3.rush_attempt==1].groupby('rusher_player_name').agg(car=('rushing_yards','size'),yds=('rushing_yards','sum')).sort_values('car',ascending=False).head(4)
        tg=l3[l3.pass_attempt==1].dropna(subset=['receiver_player_name']).groupby('receiver_player_name').agg(tgt=('receiving_yards','size'),yds=('receiving_yards','sum'),airy=('air_yards','sum')).sort_values('tgt',ascending=False).head(7)
        n=len(wk) or 1;pa=de[de.pass_attempt==1];loc=pa.groupby('pass_location').agg(att=('yards_gained','size'),ypa=('yards_gained','mean')).round(2);rr=de[de.rush_attempt==1]
        m=pb.merge(ft[['nflverse_game_id','nflverse_play_id','n_blitzers']],left_on=['game_id','play_id'],right_on=['nflverse_game_id','nflverse_play_id'],how='left')
        db=m[(m.posteam==team)&(m.qb_dropback==1)&m.n_blitzers.notna()];ob=m[(m.defteam==opp)&(m.qb_dropback==1)&m.n_blitzers.notna()]
        t,o=T[team],T[opp]
        return (f"## {t} offense (last {n} games)\nRushers (carries/yds over L3): "+'; '.join(f"{code(i,team)} {r.car}/{int(r.yds)}" for i,r in rush.iterrows())+
          "\nTargets (tgt/rec yds/air yds over L3): "+'; '.join(f"{code(i,team)} {r.tgt}/{int(r.yds)}/{int(r.airy)}" for i,r in tg.iterrows())+
          f"\n{t} QB EPA/dropback vs blitz {db[db.n_blitzers>0].epa.mean():.2f} (n={int((db.n_blitzers>0).sum())}) vs no blitz {db[db.n_blitzers==0].epa.mean():.2f}"+
          f"\n## {o} defense (season to date, {de.game_id.nunique()} games)\nRush YPC allowed {rr.yards_gained.mean():.2f}; 10+ yd runs allowed {int((rr.yards_gained>=10).sum())}; 20+ yd pass plays allowed {int((pa.yards_gained>=20).sum())}/{len(pa)} att"+
          f"\nPass YPA allowed by location: "+'; '.join(f"{i} {r.ypa} ({r.att} att)" for i,r in loc.iterrows())+f"\n{o} blitz rate {(ob.n_blitzers>0).mean():.0%}")
    lines=gl[gl.game==game];sp=lines[(lines.market=='spreads')&(lines.name==home)].sort_values('timestamp');to=lines[lines.market=='totals'].sort_values('timestamp')
    env=f"HOME spread {sp.iloc[-1].point:+g}, total {to.iloc[-1].point:g}" if len(sp) and len(to) else "Spread/total NOT saved for this game; infer script only from team form, say so."
    body=ctx(away,home)+"\n"+ctx(home,away)
    def tm(t):return T.get(t,'UNK') if isinstance(t,str) else 'UNK'
    props='\n'.join(f"{P[r.player]} ({tm(r.team)}) {r.market} {r.side} {r.line:g} {r.price:+g}" for r in g.itertuples())
    c=f"# Anonymized game AWAY@HOME (season and week withheld)\n{env}\nWeather: not saved.\n"+body+"\n# AVAILABLE PROPS (main line)\n"+props
    stem=f'w{w}_{game}';(OUT/f'{stem}.prompt.txt').write_text(c)
    cands={(P[r.player],r.market,r.side) for r in g.itertuples()};inv={v:k for k,v in P.items()}
    j=json.loads((OUT/f'{stem}.json').read_text()) if (OUT/f'{stem}.json').exists() else None
    msgs=[{'role':'system','content':SYS},{'role':'user','content':c}]
    for att in range(0 if j else 3):
        try:raw=call(msgs,temp=0.3,tag='masked')
        except SystemExit:raw='{}';print('API_FAIL',stem,flush=True);break
        try:jj=json.loads(raw)
        except Exception:jj={}
        p=[x for x in (jj.get('edge_players') or []) if x.get('confidence')!='pass']
        bad=[x for x in p if (x.get('player'),x.get('market'),x.get('side')) not in cands]
        if 1<=len(p)<=2 and not bad and len({x['player'] for x in p})==len(p):j=jj;break
        msgs+=[{'role':'assistant','content':raw},{'role':'user','content':'Rejected: need 1-2 non-pass edge players exactly from AVAILABLE PROPS (player code, market, side). Redo.'}]
    if j is None:print('DROPPED',stem);continue
    (OUT/f'{stem}.json').write_text(json.dumps(j,indent=1))
    for x in [x for x in j['edge_players'] if x.get('confidence')!='pass']:
        r=g[(g.player==inv[x['player']])&(g.market==x['market'])&(g.side==x['side'])].iloc[0]
        out.append(dict(week=w,game=game,code=x['player'],player=r.player,market=r.market,side=r.side,line=r.line,price=r.price,confidence=x['confidence']))
    print(stem,'ok',flush=True)
pd.DataFrame(out).to_csv(ROOT/'masked_picks_LOCKED.csv',index=False)
