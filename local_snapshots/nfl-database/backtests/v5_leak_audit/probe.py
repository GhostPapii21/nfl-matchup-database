import json,random,pandas as pd
from grok import call,ROOT
V5=ROOT.parent/'yardage_markets_wk3_8'/'v5'
random.seed(7)
s26=pd.read_csv('/tmp/play_by_play_2026.parquet.csv');s25=pd.read_csv('/tmp/pbp25.parquet.csv');s25=s25[s25.season_type=='REG']
w8={('CAR','GB'):(19,27),('BAL','BUF'):(10,36),('TEN','CIN'):(36,43),('ARI','DAL'):(33,30),('MIN','DET'):(15,19),('LV','NYJ'):(38,33),('CLE','PIT'):(6,27),('ATL','TB'):(0,16),('IND','JAX'):(7,42),('LAC','LA'):(9,24),('KC','DEN'):(24,28),('NE','MIA'):(24,19),('PHI','WAS'):(10,27)}
games=[]
hold7={'CIN@BAL','CLE@TEN','DAL@PHI','DEN@ARI','GB@DET','IND@MIN','KC@SEA','LA@LV','MIA@NYJ','NE@CHI','NYG@HOU','PIT@NO','SF@ATL','TB@CAR'}
for r in s26.itertuples():
    g=f'{r.away_team}@{r.home_team}'
    if r.week==7 and g in hold7:games.append(dict(id=f'G{len(games)}',season=2026,week=7,game=g,a=r.away_score,h=r.home_score,kind='holdout'))
for (a,h),(sa,sh) in w8.items():games.append(dict(id=f'G{len(games)}',season=2026,week=8,game=f'{a}@{h}',a=sa,h=sh,kind='holdout'))
for w in range(1,7):
    for r in s26[s26.week==w].sample(2,random_state=w).itertuples():games.append(dict(id=f'G{len(games)}',season=2026,week=w,game=f'{r.away_team}@{r.home_team}',a=r.away_score,h=r.home_score,kind='2026_early'))
for r in s25.sample(10,random_state=3).itertuples():games.append(dict(id=f'G{len(games)}',season=2025,week=int(r.week),game=f'{r.away_team}@{r.home_team}',a=r.away_score,h=r.home_score,kind='2025'))
# fakes: matchups that did not occur that week
played={(x['season'],x['week'],x['game']) for x in games}
allp26={(int(r.week),f'{r.away_team}@{r.home_team}') for r in s26.itertuples()}|{(8,f'{a}@{h}') for a,h in w8}
for w,g in [(3,'NYJ@SEA'),(5,'LV@PHI'),(7,'BUF@ARI'),(8,'SF@NYG'),(2,'CHI@MIA')]:
    assert (w,g) not in allp26;games.append(dict(id=f'G{len(games)}',season=2026,week=w,game=g,a=None,h=None,kind='fake'))
games.append(dict(id=f'G{len(games)}',season=2025,week=4,game='DET@NE',a=None,h=None,kind='fake'))
SYSP=("Answer only from your own memory. No tools, no browsing. For each NFL regular-season game listed (away@home, season, week), give the final score if you actually know it. "
 "If you are not confident, or you think the game did not happen, set known=false. Do NOT guess. Return JSON {\"answers\":[{\"id\":..,\"known\":bool,\"away_score\":int|null,\"home_score\":int|null,\"did_not_happen\":bool}]}")
q=[{k:x[k] for k in ('id','season','week','game')} for x in games];random.shuffle(q)
ans={}
for i in range(0,len(q),25):
    raw=call([{'role':'system','content':SYSP},{'role':'user','content':json.dumps(q[i:i+25])}],tag='scores')
    for a in json.loads(raw)['answers']:ans[a['id']]=a
rows=[]
for x in games:
    a=ans.get(x['id'],{});k=bool(a.get('known'))
    if x['kind']=='fake':res='HALLUCINATED' if k and a.get('away_score') is not None else 'correct_refusal'
    elif not k or a.get('away_score') is None:res='refused'
    elif (a['away_score'],a['home_score'])==(x['a'],x['h']):res='exact'
    elif (a['away_score']>a['home_score'])==(x['a']>x['h']):res='winner_only'
    else:res='wrong'
    rows.append({**x,'g_away':a.get('away_score'),'g_home':a.get('home_score'),'known':k,'result':res})
pd.DataFrame(rows).to_csv(ROOT/'probe_scores.csv',index=False)
# player stats
d=pd.read_csv(V5/'graded_picks.csv');h=d[(d.week>=7)&d.tag.isin(['RECONSTRUCTED','SAVED_READ'])].copy()
NAMES={}
for r in pd.read_csv(ROOT.parent/'yardage_markets_wk3_8'/'v4'/'packs'/'w7'/'props_main.csv').itertuples():pass
items=[]
for r in h.itertuples():
    items.append(dict(id=f'P{len(items)}',season=2026,week=int(r.week),game=r.game,player_id=r.player,team=r.team,stat={'rushyds':'rushing yards','recyds':'receiving yards','rushrecyds':'rushing+receiving yards'}[r.market],truth=r.actual,line=r.line,side=r.side,result_v5=r.result,tag=r.tag,kind='leg'))
for (w,g,p,t,s) in [(6,'NYJ@SEA','braelonallen','NYJ','rushing yards'),(4,'PIT@ARI','jaylenwarren','PIT','rushing yards'),(7,'TB@BUF','buckyirving','TB','rushing yards'),(8,'DET@NYG','jahmyrgibbs','DET','rushing+receiving yards'),(5,'CIN@SF','teehiggins','CIN','receiving yards'),(3,'NYG@DAL','maliknabers','NYG','receiving yards')]:
    assert (w,g) not in allp26;items.append(dict(id=f'P{len(items)}',season=2026,week=w,game=g,player_id=p,team=t,stat=s,truth=None,kind='fake'))
SYSB=("Answer only from your own memory. No tools. For each item give the player's stat in that exact NFL game (season, week, away@home; player_id is the name lowercased without spaces). "
 "If you do not actually remember it, or the game did not happen, set known=false. Do NOT estimate from season averages. Return JSON {\"answers\":[{\"id\":..,\"known\":bool,\"value\":int|null,\"did_not_happen\":bool}]}")
q=[{k:x[k] for k in ('id','season','week','game','player_id','team','stat')} for x in items];random.shuffle(q)
ans={}
for i in range(0,len(q),30):
    raw=call([{'role':'system','content':SYSB},{'role':'user','content':json.dumps(q[i:i+30])}],tag='stats')
    for a in json.loads(raw)['answers']:ans[a['id']]=a
rows=[]
for x in items:
    a=ans.get(x['id'],{});k=bool(a.get('known'));v=a.get('value')
    if x['kind']=='fake':res='HALLUCINATED' if k and v is not None else 'correct_refusal'
    elif not k or v is None:res='refused'
    elif v==x['truth']:res='exact'
    elif abs(v-x['truth'])<=10:res='within10'
    else:res='wrong'
    sidecorrect=None
    if x['kind']=='leg' and k and v is not None: sidecorrect=((v>x['line'])==(x['side']=='over'))
    rows.append({**x,'g_value':v,'known':k,'result':res,'grok_value_implies_win':sidecorrect})
pd.DataFrame(rows).to_csv(ROOT/'probe_stats.csv',index=False)
print(pd.DataFrame(rows).groupby(['kind','result']).size())
print(pd.read_csv(ROOT/'probe_scores.csv').groupby(['kind','result']).size())
