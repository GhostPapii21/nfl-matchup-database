"""Apply BUG-2026-11-01-RBSCRIPT game_script_rb blocks to the still-pregame folders (fresh odds g1529, NWS 15:30, ESPN inj 15:30)."""
import json, sys, shutil
sys.path.insert(0,'/workspace/nfl-database/tools'); import sim_v6 as S
R='/workspace/nfl-database/runs/'; NOW='2026-11-01T15:30'
L=json.load(open(R+'2026-11-01_shared_src/lines_g1529.json')); WX=json.load(open('/workspace/nfl-database/week8/weather/nws_20261101_1530.json'))
FULL={'LAC':'Los Angeles Chargers','LAR':'Los Angeles Rams','KC':'Kansas City Chiefs','DEN':'Denver Broncos','NE':'New England Patriots','MIA':'Miami Dolphins','PHI':'Philadelphia Eagles','WSH':'Washington Commanders'}
OUT=set(); inj=json.load(open('/workspace/nfl-database/week8/inactives/espn_inj_20261101_1530.json'))
for t in inj['injuries']:
    for i in t['injuries']:
        if i.get('status') in ('Out','Injured Reserve','Doubtful'): OUT.add(i['athlete']['displayName'])
E_=S.Engine(n=100_000); pl=S._PL
def top_rbs(team):
    t=S.NV.get(team,team); r=E_.ru[(E_.ru.posteam==t)&(E_.ru.pg=='RB')]
    c=r.groupby('rusher_player_id').size().sort_values(ascending=False)
    names=[pl.set_index('gsis_id').display_name.get(g) for g in c.index]
    return [n for n in names if n not in OUT][:2]
def block(g):
    a,h=g.split('@'); ev=L['games'][f"{FULL[a]} @ {FULL[h]}"]; sp={o['name']:o['point'] for o in ev['fanduel']['spreads']}
    fav=a if sp[FULL[a]]<0 else h; dog=h if fav==a else a; fs=sp[FULL[fav]]
    roof='dome' if g=='LAC@LAR' else 'open'; w=WX[g]; wx=S.__dict__.get('x',None)
    wxf=roof=='open' and (w['precip_pct']>=50 or w['gust_mph']>=20 or w['wind_mph']>=15)
    yp=S.opp_rb_ypc(E_,dog); trig=S.rb_script_trigger(fs,yp,wxf)
    b=dict(fav_team=fav,fav_spread=fs,opp_ypc=round(yp,3),wx_flag=wxf,triggered=trig,source=f"FD spread lines_g1529.json; opp RB YPC nflverse pbp thru 2026-10-29; NWS {w['source']}",pulled_et=NOW)
    if trig:
        bo=S.rb_script_boosts(fs,yp,wxf); lead,rb2=top_rbs(fav)
        fx=dict(team=fav,opp=dog,fav_spread=fs,opp_ypc=yp,wx_flag=wxf,lead=dict(player=lead,market='rushyds'),rb2=dict(player=rb2,market='rushyds'))
        r=S.price_game_script(E_,fx)
        b.update(lead_rb=lead,rb2=rb2,boost=dict(lead=bo['lead'],rb2=bo['rb2'],source=bo['source']),lead_projection=dict(market='rushyds',median=r['lead']['median']),
                 rb2_projection=dict(market='rushyds',median=r['rb2']['median']),model_order=r['model_order']+['recyds','passyds'])
    return b
games={}
for f in ['LAC@LAR','KC@DEN','NE@MIA','PHI@WSH','BONUS_SLIP_4PM','DFS_SLIPS']:
    p=R+f'2026-11-01_{f}/run_manifest.json'; shutil.copy(p,p+'.bak_1530'); m=json.load(open(p))
    m['game_script_rb']={}
    for g in m['weather']:
        if g not in games: games[g]=block(g)
        m['game_script_rb'][g]=games[g]
    json.dump(m,open(p,'w'),indent=1,default=float)
print(json.dumps(games,indent=1,default=float))
