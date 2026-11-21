import pandas as pd, json, glob
from extract import short
p = pd.read_parquet('pbp_2026.parquet', columns=['week','season_type','posteam','defteam','rusher_player_id','rusher_player_name','passer_player_id','passer_player_name','rushing_yards','qb_scramble','qb_kneel','two_point_attempt','rush_attempt','pass_attempt','sack'])
p = p[(p.season_type=='REG')]
passers = p[p.passer_player_id.notna()].groupby(['passer_player_id','passer_player_name']).size().reset_index(name='dropbacks')
passers = passers[passers.dropbacks >= 15]
out = {}
for f in sorted(glob.glob('facts_*.json')):
    fx = json.load(open(f))
    for nm, d in fx['props'].items():
        if not any(v for v in d['rushing_yards'].values()): continue
        cand = passers[passers.passer_player_name.map(lambda x: short(x)) == short(nm)]
        if cand.empty: continue
        pid = cand.sort_values('dropbacks').passer_player_id.iloc[-1]
        r = p[(p.rusher_player_id == pid) & (p.two_point_attempt != 1)]
        db = p[(p.passer_player_id == pid)]
        wk = sorted(set(db.week))
        log = []
        for w in wk:
            rw = r[r.week == w]
            log.append({'week': int(w), 'team': str(db[db.week==w].posteam.iloc[0]), 'opp': str(db[db.week==w].defteam.iloc[0]), 'dropbacks': int(len(db[db.week==w])), 'car': int(len(rw)), 'scr': int(rw.qb_scramble.fillna(0).sum()), 'kneel': int(rw.qb_kneel.fillna(0).sum()), 'yds': float(rw.rushing_yards.fillna(0).sum())})
        out[nm] = {'game': fx['gid'], 'pid': pid, 'log': log}
json.dump(out, open('qb_rush_logs.json','w'), indent=1)
for k, v in out.items():
    print(v['game'], k, [(x['week'], x['team'], x['dropbacks'], x['car'], x['scr'], int(x['yds'])) for x in v['log']])
