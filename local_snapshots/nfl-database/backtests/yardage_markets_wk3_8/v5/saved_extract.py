"""Extract SAVED_READ legs from verbatim pregame chat (13d41b9) + w8 pack checklists via Grok (extraction only, no outcomes)."""
import json,re,sys
from pathlib import Path
import pandas as pd
sys.argv=['x'];import importlib.util
ROOT=Path(__file__).resolve().parent;PK=ROOT.parent/'v4'/'packs';SR=ROOT.parent/'v4'/'saved_reads'
src=open(ROOT/'reads.py').read();ns={'__file__':str(ROOT/'reads.py')};exec(src[:src.index('SYS=')],ns)  # reuse call()/usage
call=ns['call'];usage=ns['usage']
SYS=("Extract betting edges from verbatim PRE-GAME chat about one NFL game. Keep only legs on rushing yards, receiving yards, or rush+rec yards "
"for a player in THIS game, that the authors actually endorse AND give a game-specific reason for. Drop chatter, generic lists with no reason, passing yards, TDs, receptions. "
"Return JSON {\"legs\":[{\"player\":full name,\"market\":\"rushyds|recyds|rushrecyds\",\"side\":\"over|under\",\"reason\":short quote}]} (empty list if none).")
def nm(s):return re.sub('[^a-z]','',str(s).lower()).removesuffix('jr').removesuffix('sr').removesuffix('iii').removesuffix('ii')
d=pd.read_json(SR/'reads_by_game.jsonl',lines=True).drop_duplicates(['week','game','quoted_text'])
texts={(r.week,r.game):'\n---\n'.join(g.quoted_text) for (r),g in [((type('R',(),{'week':k[0],'game':k[1]})),g) for k,g in d.groupby(['week','game'])]}
idx=pd.read_csv(PK/'w8/saved_reads/INDEX.csv')
for r in idx.itertuples():
    for gm in str(r.games).split(';'):texts[(8,gm.replace('LAR','LA'))]=(PK/'w8'/r.path).read_text()
from concurrent.futures import ThreadPoolExecutor
out=[];stats=[]
def job(item):
    (w,game),t=item
    pr=pd.read_csv(PK/f'w{w}/props_main.csv')
    pr=pr[pr.market.isin(['rushyds','recyds','rushrecyds'])&(pr.tier=='main')].sort_values(['snap','book','candidate_id']).drop_duplicates(['game','player','market','side'],keep='last')
    g=pr[pr.game==game]
    try:j=json.loads(call([{'role':'system','content':SYS},{'role':'user','content':f'Game: Week {w} {game}\n'+t[:30000]}]))
    except Exception:j={'legs':[]}
    n=0;rows=[]
    for L in j.get('legs',[]):
        m=g[(g.player==nm(L.get('player')))&(g.market==L.get('market'))&(g.side==L.get('side'))]
        if len(m) and str(L.get('reason','')).strip():
            r=m.iloc[0];rows.append(dict(week=w,game=game,player=r.player,team=r.team,opp=r.opp,market=r.market,side=r.side,line=r.line,price=r.price,reason=L['reason']));n+=1
    print(w,game,n,flush=True)
    return rows,dict(week=w,game=game,extracted=len(j.get('legs',[])),matched_to_main_prop=n,raw=json.dumps(j.get('legs',[])))
with ThreadPoolExecutor(12) as ex:
    for rows,st in ex.map(job,sorted(texts.items())):out+=rows;stats.append(st)
o=pd.DataFrame(out).drop_duplicates(['week','player']);o.to_csv(ROOT/'saved_picks.csv',index=False)
pd.DataFrame(stats).to_csv(ROOT/'saved_extract_stats.csv',index=False)
(ROOT/'usage_saved_extract.json').write_text(json.dumps(usage,indent=1))
