"""Leg universe + pricing for the Nov 1 2026 run. Usage: python3 legs.py <odds_tag> <lines_tag> -> legs_<odds_tag>.json"""
import pandas as pd, numpy as np, json, sys, re, os
SH=os.path.dirname(os.path.abspath(__file__))+'/'
OT,LT=sys.argv[1],sys.argv[2]
od=pd.read_csv(SH+f'odds_{OT}.csv'); lines=json.load(open(SH+f'lines_{LT}.json'))
km=json.load(open(SH+'keymap.json'))
sb=json.load(open(SH+'espn_scoreboard.json'))
FULL={}; 
for e in sb['events']:
    for c in e['competitions'][0]['competitors']: FULL[c['team']['displayName']]=c['team']['abbreviation']
SLATE=[]
for l in open('/workspace/nfl-database/week8/slate.md'):
    m=re.match(r'\|(\d{9})\|(\w+) @ (\w+)\|Sun Nov 01 (\d\d:\d\d [AP]M) ET\|',l)
    if m: SLATE.append(dict(id=m.group(1),away=m.group(2),home=m.group(3),ko=m.group(4)))
MK={'passyds':'player_pass_yds','comp':'player_pass_completions','rushyds':'player_rush_yds','rushrec':'player_rush_reception_yds','recyds':'player_reception_yds','rec':'player_receptions'}
LAB={'passyds':'Pass Yds','comp':'Pass Completions','rushyds':'Rush Yds','rushrec':'Rush+Rec Yds','recyds':'Rec Yds','rec':'Receptions'}
BYPOS={'QB':['passyds','comp'],'RB':['rushyds','rushrec'],'WR':['recyds','rec'],'TE':['recyds','rec']}
imp=lambda a:(100/(a+100)) if a>0 else (-a/(-a+100))
def gname(g): 
    for k in lines['games']:
        a,h=k.split(' @ ')
        if FULL.get(a)==g['away'] and FULL.get(h)==g['home']: return k
def spread_for(gk,team):
    v=lines['games'][gk]['fanduel']['spreads']; 
    for o in v:
        if FULL[o['name']]==team: return float(o['point'])
def total(gk): return float(lines['games'][gk]['fanduel']['totals'][0]['point'])
def two_way(df,book,mkt,player):
    x=df[(df.book==book)&(df.market==mkt)&(df.player==player)]
    if not len(x): return None
    best=None
    for pt,g in x.groupby('point'):
        o=g[g.side=='Over'].price; u=g[g.side=='Under'].price
        if len(o) and len(u):
            o,u=int(o.iloc[0]),int(u.iloc[0]); io,iu=imp(o),imp(u); sc=abs(io-iu)
            if best is None or sc<best[0]: best=(sc,dict(point=float(pt),over=o,under=u,nv_over=io/(io+iu),nv_under=iu/(io+iu),overround=io+iu))
    return best[1] if best else None
def alt_ladder(df,mkt,player):
    x=df[(df.book=='fanduel')&(df.market==mkt+'_alternate')&(df.player==player)&(df.side=='Over')]
    return {float(r.point):int(r.price) for r in x.itertuples()}
# placed-ticket bars (player, market) -> ticket
BARS={('Tee Higgins','rec'):'PP40 Fantasy/PP20 rec yds/$51.50 SGP Higgins 50+ yds/FD 7-leg 4+ rec',('Tee Higgins','recyds'):'PP20 Higgins o68.5 rec yds; $51.50 SGP Higgins 50+ yds',
 ('CeeDee Lamb','rec'):'PP40/PP20/UD20 Lamb o4.5 rec; PP25 o6.5',('CeeDee Lamb','recyds'):'Ticket 2 Lamb 60+ yds; FD 7-leg Lamb 50+',
 ('Brock Bowers','recyds'):'UD20 Bowers o49.5; FD 7-leg 50+',('Amon-Ra St. Brown','rec'):'PP40 o5.5; PP25 o7',('Amon-Ra St. Brown','recyds'):'UD20 o49.5; Ticket 2 60+',
 ('Matthew Stafford','comp'):'PP40/PP20 Stafford o22.5 completions',('Kenneth Walker III','rushyds'):'PP40 o97.5; UD20 o69.5',('Puka Nacua','recyds'):'UD20 Puka o69.5',
 ('Drake London','rec'):'UD20 o5.5; Ticket 2 5+',('Zay Flowers','rec'):'PP25 o6; Ticket 2 5+',('Zay Flowers','recyds'):'UD20 o49.5; FD 7-leg 60+; $51.50 SGP 50+ (brief-only)',
 ('Jahmyr Gibbs','rec'):'Ticket 2 Gibbs 5+ rec',('Chris Godwin Jr.','rec'):'Ticket 2 Godwin 4+; $51.50 SGP 3+ (brief-only)',('George Pickens','rec'):'Ticket 2 Pickens 4+; $51.50 SGP 4.5+',
 ('James Cook','rushrec'):'Ticket 2 Cook 70+ rush+rec',('Denzel Boston','recyds'):'UD20 Boston o29.5',('Patrick Mahomes','passyds'):'PP20 Mahomes o0.5 pass yds',
 ('Bijan Robinson','rec'):'PP25 Bijan o3.5',('Jaylen Warren','rushrec'):'PP25 Warren o69.5 rush+rec',('Parker Washington','recyds'):'FD 7-leg Washington 40+ (CONDITIONAL: placed status unconfirmed)'}
STACK={'George Pickens':'Ticket 2 Pickens 4+ rec and $51.50 SGP 4.5+ rec (different stat: flag for user)'}
legs=[]
for g in SLATE:
    gk=gname(g); sp={g['away']:spread_for(gk,g['away']),g['home']:spread_for(gk,g['home'])}
    sub=od[od.game==gk]
    for k,v in km.items():
        if v['team'] not in (g['away'],g['home']) or not v.get('name'): continue
        name=v['name']; oname={'Chris Godwin Jr.':'Chris Godwin'}.get(name,name); team=v['team']; opp=g['home'] if team==g['away'] else g['away']
        DFSX={'Bijan Robinson':['rec'],'Jahmyr Gibbs':['rec']}
        for mk in BYPOS[v['pos']]+DFSX.get(name,[]):
            dfs_only=mk not in BYPOS[v['pos']]; fdbook='fanduel'
            fd=two_way(sub,'fanduel',MK[mk],oname)
            if not fd and (name,mk)==('Matthew Stafford','comp'): fd=two_way(sub,'pinnacle',MK[mk],oname); dfs_only=True; fdbook='pinnacle'
            if not fd: continue
            pin=two_way(sub,'pinnacle',MK[mk],oname); dk=two_way(sub,'draftkings',MK[mk],oname)
            pp=sub[(sub.book=='prizepicks')&(sub.market==MK[mk])&(sub.player==oname)].point.unique().tolist()
            ud=sub[(sub.book=='underdog')&(sub.market==MK[mk])&(sub.player==oname)].point.unique().tolist()
            legs.append(dict(game=f"{g['away']}@{g['home']}",gid=g['id'],ko=g['ko'],gk=gk,player=name,oname=oname,team=team,opp=opp,pos=v['pos'],market=mk,label=LAB[mk],
                spread=sp[team],total=total(gk),fd=fd,pin=pin,dk=dk,pp=pp,ud=ud,alts=alt_ladder(sub,MK[mk],oname),bar=BARS.get((name,mk)),stack=STACK.get(name),
                explicit=None,dfs_only=dfs_only,fdbook=fdbook))
# explicit BetGuru regrade legs (all rec yds overs)
EXP={'Keenan Allen':35.5,'Jordan Addison':37.5,'DJ Moore':53.5,'George Pickens':65.5,'Parker Washington':67.5}
for L in legs:
    if L['player'] in EXP and L['market']=='recyds': L['explicit']=dict(line=EXP[L['player']],note='BetGuru defender-regrade leg (run_additions item 1)')
json.dump(dict(slate=SLATE,legs=legs,odds_tag=OT,lines_tag=LT,odds_pulled=json.load(open(SH+f'odds_{OT}_meta.json'))['pulled_et'],lines_pulled=lines['pulled_et']),open(SH+f'legs_{OT}.json','w'),indent=0)
print(len(legs)); 
import collections; print(collections.Counter(l['game'] for l in legs))
miss=[(v['name'],v['team']) for k,v in km.items() if v.get('name') and not any(l['player']==v['name'] for l in legs)]; print('no FD line:',miss)
for L in legs:
    if L['explicit']: print(L['player'],L['fd'],L['spread'])
