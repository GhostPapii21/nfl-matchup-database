"""Leg universe for the confidence check (no network, no new pulls).
W3-5 recyds/rushyds/rushrec + W6-8 rushrec: backtests/yardage_markets_wk3_8/raw (Odds API historical, pre-kick snapshot).
W6-8 passyds/rec/recyds/rushyds: backtests/current_rules_wk6_8/sims_wk6_8.csv (v1 real_lines, already gsis-mapped).
MNF CHI@SEA: backtests/rulebook_replay_wk6_8/mnf_lines.csv (+ actuals from graded_legs.csv, ESPN box).
Main line = modal line across books with both sides; no-vig = mean two-way multiplicative no-vig across those books;
bet price = FanDuel at that line if quoted, else first book (same as v1 parse.py)."""
import json,glob,collections,re,numpy as np,pandas as pd
R='/workspace/nfl-database/'
P=pd.read_parquet(R+'runs/2026-11-02_shared_src/play_by_play_2026.parquet'); P=P[(P.season_type=='REG')&(P.two_point_attempt!=1)]
PL=pd.read_parquet(R+'runs/2026-11-02_shared_src/players.parquet')
AB=json.load(open(R+'backtests/rulebook_replay_wk6_8/abbr.json'))
MK={'player_reception_yds':'recyds','player_rush_yds':'rushyds','player_rush_reception_yds':'rushrec'}
imp=lambda o:100/(o+100) if o>0 else -o/(-o+100)
key=lambda s:' '.join(re.sub(r'\b(jr|sr|ii|iii|iv|v)\b','',re.sub(r'[^a-z ]','',str(s).lower())).split())
PL['k']=PL.display_name.map(key)
def actual(gid,g,mkt):
    q=P[P.game_id==gid]
    if mkt=='passyds': return float(q[(q.passer_player_id==g)&(q.pass_attempt==1)&(q.sack!=1)].passing_yards.fillna(0).sum())
    rr=q[(q.receiver_player_id==g)&(q.pass_attempt==1)&(q.sack!=1)]; uu=q[(q.rusher_player_id==g)&(q.rush_attempt==1)]
    return dict(rec=float(rr.complete_pass.sum()),recyds=float(rr.receiving_yards.fillna(0).sum()),rushyds=float(uu.rushing_yards.fillna(0).sum()),
                rushrec=float(rr.receiving_yards.fillna(0).sum()+uu.rushing_yards.fillna(0).sum()))[mkt]
rows=[]; unm=collections.Counter()
for f in sorted(glob.glob(R+'backtests/yardage_markets_wk3_8/raw/w[3-8]_*.json')):
    W=int(f.split('/')[-1][1]); j=json.load(open(f)); d=j['data']; snap=j['timestamp']
    h,a=AB[d['home_team']],AB[d['away_team']]
    G=P[(P.week==W)&(P.home_team==h)&(P.away_team==a)]
    if G.empty: unm['nogame']+=1; continue
    gid=G.game_id.iloc[0]; spl=float(G.spread_line.iloc[0])
    ids=set(G.passer_player_id.dropna())|set(G.receiver_player_id.dropna())|set(G.rusher_player_id.dropna())
    cand=PL[PL.gsis_id.isin(ids)]
    q=collections.defaultdict(dict)
    for bk in d.get('bookmakers',[]):
        for m in bk['markets']:
            if m['key'] not in MK: continue
            mk=MK[m['key']]
            if W>=6 and mk!='rushrec': continue          # W6-8 main rec/rush yds come from v1 real_lines
            for o in m['outcomes']: q[(o['description'],mk,o.get('point'),bk['key'])][o['name']]=o['price']
    agg=collections.defaultdict(list)
    for (pl,mk,pt,bk),v in q.items():
        if 'Over' in v and 'Under' in v: agg[(pl,mk)].append((pt,bk,v['Over'],v['Under']))
    for (pl,mk),L in agg.items():
        pts=collections.Counter(x[0] for x in L); main=max(pts,key=lambda p:(pts[p],-abs(p))); M=[x for x in L if x[0]==main]
        fd=[x for x in M if x[1]=='fanduel']; pk=fd[0] if fd else M[0]
        c=cand[cand.k==key(pl)]
        if len(c)!=1: unm['name']+=1; continue
        g=c.gsis_id.iloc[0]; qq=G[(G.passer_player_id==g)|(G.receiver_player_id==g)|(G.rusher_player_id==g)]
        team=qq.posteam.mode().iloc[0]; opp=a if team==h else h
        rows.append(dict(week=W,game_id=gid,commence=d['commence_time'],snap=snap,player=pl,gsis=g,team=team,opp=opp,
            team_spread=-spl if team==h else spl,market=mk,line=main,nv_over=float(np.mean([imp(o)/(imp(o)+imp(u)) for _,_,o,u in M])),
            book=pk[1],over_price=pk[2],under_price=pk[3],n_books=len(M),src='yardage_markets_wk3_8/raw',actual=actual(gid,g,mk)))
V1=pd.read_csv(R+'backtests/current_rules_wk6_8/sims_wk6_8.csv')
for _,r in V1.iterrows():
    rows.append(dict(week=r.week,game_id=r.game_id,commence=r.commence,snap=r.snap,player=r.player,gsis=r.gsis,team=r.team,opp=r.opp,team_spread=r.team_spread,
        market=r.market,line=r.line,nv_over=r.nv_over,book=r.book,over_price=r.over_price,under_price=r.under_price,n_books=r.n_books,src='current_rules_wk6_8/real_lines',actual=actual(r.game_id,r.gsis,r.market)))
MN=pd.read_csv(R+'backtests/rulebook_replay_wk6_8/mnf_lines.csv'); GL=pd.read_csv(R+'backtests/rulebook_replay_wk6_8/graded_legs.csv')
act=GL[GL.week==9].drop_duplicates(['player','market','line']).set_index(['player','market','line']).actual.to_dict()
for _,r in MN.iterrows():
    rows.append(dict(week=9,game_id='2026_MNF_CHI_SEA',commence=r.commence,snap=r.snap,player=r.player,gsis=r.gsis,team=r.team,opp=r.opp,team_spread=r.team_spread,
        market=r.market,line=r.line,nv_over=r.nv_over,book=r.book,over_price=r.over_price,under_price=r.under_price,n_books=r.n_books,src='rulebook_replay_wk6_8/mnf_lines (ESPN box actual)',actual=act.get((r.player,r.market,r.line),np.nan)))
D=pd.DataFrame(rows)
D['pre_kick_min']=(pd.to_datetime(D.commence)-pd.to_datetime(D.snap)).dt.total_seconds()/60
D=D.drop_duplicates(['week','gsis','market'])
D=D[(D.line%1!=0)&D.actual.notna()]   # half-point lines only (no pushes); graded only
D['hit_over']=(D.actual>D.line).astype(int)
D.to_csv('legs.csv',index=False)
print('unmatched',dict(unm)); print(D.groupby(['week','market']).size().unstack(fill_value=0)); print('pre-kick minutes',D.pre_kick_min.describe().round(1).to_dict())
