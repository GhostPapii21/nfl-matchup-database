"""Step 1: candidate universe. Main lines (v1 real_lines, both sides), alt Over rungs below the main line
(no-vig PROXY: remove the same book's main-line margin), MNF CHI@SEA main props. Then 100k sim_v6 runs for every
player-market needing alt rungs, MNF, or a soft-run-D ypc_boost (opp RB YPC >= 4.4, season-to-date before week W)."""
import os,sys,re,json,glob,collections,numpy as np,pandas as pd
os.environ['SIMV6_SRC']='/workspace/nfl-database/runs/2026-11-02_shared_src'
sys.path.insert(0,'/workspace/nfl-database/tools'); import sim_v6 as S
N=100_000; P=S._P; PL=S._PL; HERE=os.path.dirname(os.path.abspath(__file__))
AB=json.load(open(f'{HERE}/abbr.json'))
MK={'player_reception_yds':'recyds','player_receptions':'rec','player_rush_yds':'rushyds','player_pass_yds':'passyds'}
imp=lambda o:100/(o+100) if o>0 else -o/(-o+100)
nm=lambda s:re.sub(r'\b(jr|sr|ii|iii|iv|v)\b','',re.sub(r'[^a-z ]','',str(s).lower())).split(); key=lambda s:' '.join(nm(s))
V1=pd.read_csv('../current_rules_wk6_8/sims_wk6_8.csv')
# ---- alts
alts=[]
for f in glob.glob('raw/alt_*.json'):
    j=json.load(open(f)); d=j['data']
    for bk in d.get('bookmakers',[]):
        for m in bk['markets']:
            base=m['key'].replace('_alternate','')
            if base not in MK: continue
            for o in m['outcomes']:
                if o['name']=='Over': alts.append(dict(event=d['id'],player=o['description'],market=MK[base],book=bk['key'],point=o['point'],price=o['price'],snap=j['timestamp']))
A=pd.DataFrame(alts); print('alt over quotes',len(A),'events',A.event.nunique())
# same-book main margin from v1 raw (book of v1 pick only has both prices; use v1 row margin when same book, else median v1 margin)
v1m=V1.assign(k=(V1.over_price.map(imp)+V1.under_price.map(imp)-1))
U=A.merge(v1m[['event','player','market','line','book','k','gsis','team','opp','team_spread','week','game_id','pos']].rename(columns={'book':'mainbook'}),on=['event','player','market'])
U=U[U.point<U.line]
U['nv_proxy']=U.price.map(imp)/(1+U.k)  # margin removal proxy (one-sided)
U['proxy_note']=np.where(U.book==U.mainbook,'same-book main-line margin removed','v1 main-line book margin removed (alt book differs)')
# per player-market keep up to 3 rungs closest below main, prefer fanduel then draftkings then any
U['bp']=U.book.map({'fanduel':0,'draftkings':1}).fillna(2)
U=U.sort_values('bp').drop_duplicates(['event','player','market','point'])
U=U[(U.price>=-400)&(U.price<=150)]
U=U.sort_values('point',ascending=False).groupby(['event','player','market']).head(3)
U.to_csv('alt_candidates.csv',index=False); print('alt rungs kept',len(U))
# ---- MNF props
j=json.load(open(glob.glob('raw/props_*.json')[0])); d=j['data']; q=collections.defaultdict(dict)
for bk in d['bookmakers']:
    for m in bk['markets']:
        if m['key'] in MK:
            for o in m['outcomes']: q[(o['description'],MK[m['key']],o.get('point'),bk['key'])][o['name']]=o['price']
agg=collections.defaultdict(list)
for (pl,mk,pt,bk),v in q.items():
    if 'Over' in v and 'Under' in v: agg[(pl,mk)].append((pt,bk,v['Over'],v['Under']))
mn=[]
for (pl,mk),L in agg.items():
    pts=collections.Counter(x[0] for x in L); main=max(pts,key=lambda p:(pts[p],-abs(p))); M=[x for x in L if x[0]==main]
    fd=[x for x in M if x[1]=='fanduel']; pk=fd[0] if fd else M[0]
    mn.append(dict(event=d['id'],home=d['home_team'],away=d['away_team'],commence=d['commence_time'],snap=j['timestamp'],player=pl,market=mk,line=main,
        nv_over=float(np.mean([imp(o)/(imp(o)+imp(u)) for _,_,o,u in M])),book=pk[1],over_price=pk[2],under_price=pk[3],n_books=len(M)))
MN=pd.DataFrame(mn)
# map MNF names -> gsis via ESPN box (team) + players table
es=json.load(open('espn/index.json')); mid=[k for k,v in es.items() if 'CHI' in json.dumps(v) and 'SEA' in json.dumps(v) and '11-03' in json.dumps(v)]
box=json.load(open(f'espn/{mid[0]}.json'))['boxscore']['players']; e2g=PL.dropna(subset=['espn_id']).assign(e=lambda x:x.espn_id.astype(str).str.replace(r'\.0$','',regex=True)).set_index('e').gsis_id.to_dict()
tm={}
for t in box:
    for st in t['statistics']:
        for a in st['athletes']: tm[key(a['athlete']['displayName'])]=(t['team']['abbreviation'],e2g.get(str(a['athlete']['id'])))
MN['k']=MN.player.map(key); MN['team']=MN.k.map(lambda k:tm.get(k,(None,None))[0]); MN['gsis']=MN.k.map(lambda k:tm.get(k,(None,None))[1])
print('MNF props',len(MN),'unmatched',MN.gsis.isna().sum()); MN=MN.dropna(subset=['gsis'])
G=json.load(open(glob.glob('raw/game_2026-11-03*.json')[0]))['data']
g=[x for x in G if x['id']==d['id']][0]; sp=[o for b in g['bookmakers'] for m in b['markets'] if m['key']=='spreads' for o in m['outcomes'] if o['name']=='Seattle Seahawks']
sea_sp=float(np.median([o['point'] for o in sp])); tot=float(np.median([o['point'] for b in g['bookmakers'] for m in b['markets'] if m['key']=='totals' for o in m['outcomes'] if o['name']=='Over']))
MN['opp']=np.where(MN.team=='SEA','CHI','SEA'); MN['team_spread']=np.where(MN.team=='SEA',sea_sp,-sea_sp); MN['week']=9; MN['game_id']='2026_MNF_CHI_SEA'; MN['spread_line']=-sea_sp; MN['total_line']=tot
MN['home_team']='SEA'; MN['away_team']='CHI'; MN['posteam']=MN.team
# ---- sims
def oypc(E,opp):
    try: return S.opp_rb_ypc(E,opp)
    except Exception: return None
jobs=collections.defaultdict(set)
for _,r in U.iterrows(): jobs[(r.week,r.gsis,r.team,r.opp,r.market,r.team_spread)].add(r.point+0.5 if r.market=='rec' else r.point)
for _,r in V1[V1.market=='rushyds'].iterrows(): jobs[(r.week,r.gsis,r.team,r.opp,r.market,r.team_spread)].add(r.line)
for _,r in MN.iterrows(): jobs[(9,r.gsis,r.team,r.opp,r.market,r.team_spread)].add(r.line+0.5 if r.market=='rec' else r.line)
for _,r in V1.iterrows():
    k=(r.week,r.gsis,r.team,r.opp,r.market,r.team_spread)
    if k in jobs: jobs[k].add(r.line+0.5 if r.market=='rec' else r.line)
out=[]; cuts={6:P[P.week==6].game_date.min(),7:P[P.week==7].game_date.min(),8:P[P.week==8].game_date.min(),9:'2026-11-02'}
for W in (6,7,8,9):
    E=S.Engine(cutoff=cuts[W],calib=None,n=N); ks=[k for k in jobs if k[0]==W]
    for k in ks:
        _,g_,t,o,mk,sp=k; yb=1.0; oy=None
        if mk=='rushyds':
            oy=oypc(E,o); yb=S.soft_run_d_boost(oy)['applied']
        if mk=='rushyds' and yb==1.0 and not any(True for _ in []):
            pass
        try: res,info=E.sim(dict(player=g_,gsis=g_,team=t,opp=o,market=mk,spread=sp,rungs=sorted(jobs[k]),ypc_boost=yb),raw=True)
        except Exception as e: print('ERR',k,e); continue
        for th in jobs[k]:
            out.append(dict(week=W,gsis=g_,team=t,opp=o,market=mk,team_spread=sp,thr=th,ypc_boost=yb,opp_ypc=oy,pos=info['pos'],n_games=info['n_games'],
                **{f'p_{m}':res[m]['rungs'][str(th)] for m in S.MODES},**{f'med_{m}':res[m]['cmedian'] for m in S.MODES}))
    print('week',W,len(out),flush=True)
pd.DataFrame(out).to_csv('sims_replay.csv',index=False); MN.to_csv('mnf_lines.csv',index=False)
json.dump(dict(n=N,seed_note='sim_v6 Engine default seeding',cutoffs=cuts,script='tools/sim_v6.py'),open('sims_replay_meta.json','w'),default=str)
