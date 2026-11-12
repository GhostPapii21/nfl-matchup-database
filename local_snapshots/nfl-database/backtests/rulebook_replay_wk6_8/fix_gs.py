import os,sys,json,glob,traceback
os.environ['SIMV6_SRC']='/workspace/nfl-database/runs/2026-11-02_shared_src'; sys.path.insert(0,'/workspace/nfl-database/tools'); import sim_v6 as S, pandas as pd
P=pd.read_parquet(os.environ['SIMV6_SRC']+'/play_by_play_2026.parquet'); PL=pd.read_parquet(os.environ['SIMV6_SRC']+'/players.parquet'); NAME=PL.set_index('gsis_id').display_name.to_dict(); PG=PL.set_index('gsis_id').position_group.to_dict()
EN={}
for d in sorted(glob.glob('runs/*/run_manifest.json')):
    m=json.load(open(d)); W=m['week']; (gk,g),=m['game_script_rb'].items()
    if not g['triggered']: continue
    if W not in EN: EN[W]=S.Engine(cutoff=P[P.week==W].game_date.min() if W<9 else '2026-11-02',calib=None,n=100_000)
    E=EN[W]; fav=g['team']; opp=[t for t in gk.split('@') if t!=fav][0]
    gids=sorted({x for x in P[(P.posteam==fav)&(P.week<W)].game_id},key=lambda x:P[P.game_id==x].week.iloc[0])[-4:]
    ru=P[(P.game_id.isin(gids))&(P.posteam==fav)&(P.rush_attempt==1)]; q=ru[ru.rusher_player_id.map(PG)=='RB'].rusher_player_id.value_counts()
    leadleg=[l for l in m['legs'] if l['gsis']==q.index[0] and l['market']=='rushyds' and l['side']=='over' and l['rung']=='main']
    try:
        out=S.price_game_script(E,dict(team=fav,opp=opp,fav_spread=g['fav_spread'],opp_ypc=g['opp_ypc'],wx_flag=g['wx_flag'],
            lead=dict(player=NAME.get(q.index[0]),market='rushyds',line=(leadleg[0]['line'] if leadleg else None),no_vig=(leadleg[0]['no_vig'] if leadleg else None)),
            rb2=dict(player=NAME.get(q.index[1]),market='rushyds'),other_legs=[]))
        g.pop('error',None)
        g.update(boost=dict(lead=out['lead']['boost'],rb2=out['rb2']['boost'],source='tools/sim_v6.rb_script_boosts (rb_miss_fit.json)'),lead_rb=NAME.get(q.index[0]),rb2=NAME.get(q.index[1]),
                 rb2_projection=dict(median=out['rb2']['median']),model_order=out['model_order'],lead_reprice={k:v for k,v in out['lead'].items() if k in('median','p','line','edge')})
        print(d,'ok',g['boost'])
    except Exception as e: traceback.print_exc(limit=3); print(d,'ERR',e)
    json.dump(m,open(d,'w'),indent=1,default=str)
