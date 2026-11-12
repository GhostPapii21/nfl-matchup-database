"""Recompute local nflverse analysis; write only beside this script. Python 3 + pandas."""
from pathlib import Path
import pandas as pd
import numpy as np

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
SRC = ROOT / 'sources/nflverse'

def save(df, name):
    df.to_csv(OUT / (name + '.csv'), index=False, float_format='%.6f')
    return df

def ratio(a, b):
    return a / b if b else np.nan

p0 = pd.read_csv(SRC / 'pbp_2026.csv.gz', low_memory=False)
f = pd.read_csv(SRC / 'ftn_charting_2026.csv', low_memory=False)
r = pd.read_csv(SRC / 'roster_weekly_2026.csv.gz', low_memory=False)
s = pd.read_csv(SRC / 'snap_counts_2026.csv.gz')
assert not p0.duplicated(['game_id', 'play_id']).any()
assert not f.duplicated(['nflverse_game_id', 'nflverse_play_id']).any()
fc = [c for c in f if c not in ['season', 'week']]
p = p0.merge(f[fc], left_on=['game_id','play_id'], right_on=['nflverse_game_id','nflverse_play_id'], how='left', validate='one_to_one', indicator='ftn_merge')
p = p[p.week.between(1,8) & p.season_type.eq('REG')].copy()
valid = p.two_point_attempt.ne(1) & p.play_type.ne('no_play') & p.play_deleted.ne(1)
j = p[valid & p.posteam.eq('JAX')].copy()
rr = r[r.week.between(1,8)]
names = ['Jakobi Meyers','Parker Washington','Brenton Strange','Brian Thomas Jr.']
ids = {n: rr.loc[rr.full_name.eq(n),'gsis_id'].dropna().unique().item() for n in names}
pfr = {n: rr.loc[rr.full_name.eq(n),'pfr_id'].dropna().unique().item() for n in names}
rr_ids = rr[rr.gsis_id.notna() & rr.gsis_id.astype(str).str.strip().ne('')]  # bugfix: blank/null gsis_id mapped NaN receivers to Al-Jay Henderson
idnames = rr_ids.drop_duplicates('gsis_id').set_index('gsis_id').full_name.to_dict()
assert not any(pd.isna(k) or str(k).strip()=='' for k in idnames)
p['receiver'] = p.receiver_player_id.map(idnames).fillna(p.receiver_player_name)
j['receiver'] = j.receiver_player_id.map(idnames).fillna(j.receiver_player_name)
games = j[['week','game_id']].drop_duplicates().sort_values('week')
assert games.week.tolist() == [1,2,3,4,5,6,8]
ss = s[s.team.eq('JAX') & s.week.between(1,8) & s.game_type.eq('REG') & s.pfr_player_id.isin(pfr.values())].copy()
ss['player'] = ss.pfr_player_id.map({v:k for k,v in pfr.items()})
assert not ss.duplicated(['game_id','player']).any()
ss['row_type']='game'; ss['games_n']=1
# Source percentage is rounded; exact team offensive-snap denominator isn't supplied.
ss['offense_pct_source_games_n'] = ss.offense_pct.notna().astype(int)
av = ss.groupby('player').agg(offense_snaps=('offense_snaps','mean'),offense_pct=('offense_pct','mean'),games_n=('game_id','nunique'),offense_pct_source_games_n=('offense_pct','count')).reset_index()
av['row_type']='average_games_played'
snaps=save(pd.concat([ss[['row_type','player','week','game_id','offense_snaps','offense_pct','games_n','offense_pct_source_games_n']],av],ignore_index=True),'snaps')

attempts = j[j.pass_attempt.eq(1) & j.sack.ne(1)].copy()
lt = attempts[attempts.passer_player_name.eq('T.Lawrence')]
def target_summary(a, scope):
    t=a[a.receiver_player_id.notna() | a.receiver_player_name.notna()]
    z=t.groupby(['receiver_player_id','receiver'],dropna=False).agg(targets=('play_id','size'),receptions=('complete_pass','sum'),yards=('receiving_yards','sum'),air_yards_sum=('air_yards','sum'),adot_n=('air_yards','count')).reset_index()
    z['scope']=scope; z['targets_n']=len(t); z['target_share']=z.targets / len(t)
    z['adot']=z.air_yards_sum.div(z.adot_n.replace(0,np.nan));z['rank']=z.targets.rank(method='min',ascending=False).astype(int)
    return z.sort_values(['rank','receiver'])
targets=save(pd.concat([target_summary(lt,'Lawrence'),target_summary(attempts,'team_all_QB')],ignore_index=True),'targets')
weekly=[]
for scope,a in [('Lawrence',lt),('team_all_QB',attempts)]:
    for w,g in games.itertuples(index=False):
        t=a[a.game_id.eq(g) & a.receiver_player_id.notna()]
        for n in names[:3]:
            x=t[t.receiver_player_id.eq(ids[n])]
            weekly.append(dict(scope=scope,week=w,game_id=g,player=n,targets=len(x),targets_n=len(t),target_share=ratio(len(x),len(t))))
save(pd.DataFrame(weekly),'targets_weekly')
# Roster membership is not proof of participation. PBP receiving involvement is affirmative evidence.
timing=[]
for w in sorted(r.week.dropna().unique()):
    rost=r[r.week.eq(w)&r.gsis_id.eq(ids[names[0]])]
    plays=p0[p0.week.eq(w)&p0.receiver_player_id.eq(ids[names[0]])]
    timing.append(dict(week=w,roster_teams='|'.join(sorted(rost.team.dropna().unique())),roster_rows_n=len(rost),pbp_posteams='|'.join(sorted(plays.posteam.dropna().unique())),pbp_receiving_plays_n=len(plays),jax_game_n=int(games.week.eq(w).sum())))
save(pd.DataFrame(timing),'meyers_timing')

db=p[valid & p.qb_dropback.eq(1)].copy()
pressure_rows=[]
for label,x in [('BAL',db[db.defteam.eq('BAL')]),('league',db),('league_ex_BAL',db[db.defteam.ne('BAL')])]:
    row=dict(row_type='defense',scope=label,dropbacks=len(x),games_n=x.game_id.nunique())
    for metric,col,threshold in [('blitz_rate','n_blitzers',0),('rush5plus_rate','n_pass_rushers',4),('sack_rate','sack',0),('qb_hit_rate','qb_hit',0)]:
        a=x[col].dropna();row[metric+'_n']=len(a);row[metric+'_count']=int((a>threshold).sum());row[metric]=ratio(row[metric+'_count'],len(a))
    pressure_rows.append(row)
lawrence_db = db.passer_player_name.eq('T.Lawrence') | (db.qb_scramble.eq(1) & db.rusher_player_name.eq('T.Lawrence'))
l=db[db.posteam.eq('JAX') & lawrence_db].copy()
l['receiver']=l.receiver_player_id.map(idnames).fillna(l.receiver_player_name)
l['blitz']=np.where(l.n_blitzers.isna(),'unknown',np.where(l.n_blitzers.gt(0),'blitz','no_blitz'))
proxycols=['qb_hit','sack','is_qb_out_of_pocket','qb_scramble']
positive=l[proxycols].eq(1).any(axis=1)
known=l[proxycols].notna().all(axis=1)
l['pressure_proxy']=np.where(positive,'pressure_proxy',np.where(known,'clean_proxy','unknown'))
if 'was_pressure' in p0:
    l['pressure']=np.where(l.was_pressure.isna(),'unknown',np.where(l.was_pressure.eq(1),'pressured','clean'))
else:
    l['pressure']=l.pressure_proxy
splits=[('all','all',l)]
for axis in ['blitz','pressure_proxy'] + (['pressure'] if 'was_pressure' in p0 else []):
    splits += [(axis,str(label),x) for label,x in l.groupby(axis)]
for axis,label,x in splits:
    a=x[x.pass_attempt.eq(1)&x.sack.ne(1)]
    pressure_rows.append(dict(row_type='QB',scope='T.Lawrence',split_axis=axis,split=label,dropbacks=len(x),att=len(a),completions=int(a.complete_pass.sum()),cmp_pct=ratio(a.complete_pass.sum(),a.complete_pass.count()),cmp_pct_n=int(a.complete_pass.count()),passing_yards=float(a.passing_yards.fillna(0).sum()),ypa=ratio(a.passing_yards.fillna(0).sum(),len(a)),ypa_n=len(a),sacks=int(x.sack.sum()),sack_rate=ratio(x.sack.sum(),x.sack.count()),sack_rate_n=int(x.sack.count()),epa=x.epa.mean(),epa_n=int(x.epa.count())))
pressure=save(pd.DataFrame(pressure_rows),'pressure')

def distribution(x, axis, label):
    t=x[x.pass_attempt.eq(1)&x.sack.ne(1)&x.receiver.notna()]
    z=t.groupby('receiver').size().rename('targets').reset_index()
    z['split_axis']=axis;z['split']=label;z['targets_n']=len(t);z['share']=z.targets/len(t);z['rank']=z.targets.rank(method='min',ascending=False).astype(int)
    return z.sort_values(['rank','receiver'])
dists=[distribution(x,axis,label) for axis,label,x in splits if axis!='all']
save(pd.concat(dists,ignore_index=True),'target_pressure_distribution')
checks=[]
for label,x in [('all',l),('pressure_proxy',l[l.pressure_proxy.eq('pressure_proxy')])]:
    checks.append(distribution(x[x.air_yards.le(2)],'air_yards_le_2',label))
check=save(pd.concat(checks,ignore_index=True),'checkdowns')

route=[];screen=[]
for scope,a in [('Lawrence',lt),('team_all_QB',attempts)]:
    for n in names[:3]:
        x=a[a.receiver_player_id.eq(ids[n])].copy()
        x['depth']=pd.cut(x.air_yards,[-np.inf,0,4,14,np.inf],labels=['at_or_behind_LOS','1_to_4','5_to_14','15_plus']).astype('object').fillna('unknown')
        x['location']=x.pass_location.fillna('unknown')
        z=x.groupby(['location','depth'],observed=True).agg(targets=('play_id','size'),receptions=('complete_pass','sum'),yards=('receiving_yards','sum')).reset_index()
        z['player']=n;z['scope']=scope;z['targets_n']=len(x);z['share']=z.targets/len(x);route.append(z)
        chart=x.is_screen_pass.dropna()
        screen.append(dict(scope=scope,player=n,targets=len(x),screen_charted_n=len(chart),screen_pass_targets=int(chart.eq(1).sum()),screen_rate=ratio(chart.eq(1).sum(),len(chart))))
save(pd.concat(route,ignore_index=True),'route_area_proxy');save(pd.DataFrame(screen),'screens')
save(pd.DataFrame({'column':f.columns,'dtype':[str(f[c].dtype) for c in f]}),'ftn_columns')
# Any receiver alignment / route data would be summarized generically if supplied.
route_fields=[c for c in f if any(k in c.lower() for k in ['alignment','route'])]
if route_fields:
    rows=[]
    for c in route_fields:
        x=j[j.receiver_player_id.isin([ids[n] for n in names[:3]]) & j.pass_attempt.eq(1)]
        z=x.groupby(['receiver',c],dropna=False).size().rename('targets').reset_index().rename(columns={c:'value'})
        z['field']=c;rows.append(z)
    save(pd.concat(rows,ignore_index=True),'ftn_route_fields')

assert targets.groupby('scope').targets.sum().eq(targets.groupby('scope').targets_n.first()).all()
assert targets.groupby('scope').target_share.sum().sub(1).abs().lt(1e-9).all()
assert len(ss)==28 and av.games_n.eq(7).all()
assert sum(len(x) for _,x in l.groupby('blitz'))==len(l)
notes=[]
notes += ['# JAX offense, Weeks 1–8, 2026', '', 'Source: local nflverse CC-BY snapshot, pulled 2026-11-03 08:04 ET. Recomputed from the four supplied files; reference build.py informed the join and split logic, with no copied results. Run: `python3 week10/meyers_wash_strange/offense/runA/build_a.py`.', '', 'Seven JAX games: Weeks 1–6 and 8; Week 7 bye. Regular season only. PBP excludes two-point attempts, no-play rows and deleted plays. Attempts exclude sacks; named/identified receivers define targets, excluding untargeted throwaways/spikes. Lawrence attribution uses passer T.Lawrence for throws/sacks or rusher T.Lawrence for scrambles; no other-QB sacks are assigned to him. QB splits use qb_dropback=1, which excludes one Lawrence clock spike; the attempt/target tables retain official pass attempts including that untargeted spike.', '', 'All rates are fractions, with denominator `_n` columns (or att/dropbacks/targets_n); counts appear alongside rates. aDOT uses non-null air yards; YPA treats null passing yards on incomplete passes as zero. EPA is mean per dropback with epa_n. Receiving yards are summed. Snap averages are arithmetic means of source game percentages over source appearances (games played), not snap-weighted percentages. Source offense_pct is rounded and has no exact team-snap denominator; games_n and offense_pct_source_games_n accompany it.', '', '## Snap averages', av.to_markdown(index=False), '', '## Targets', targets[['scope','receiver','rank','targets','receptions','yards','targets_n','target_share','adot','adot_n']].to_markdown(index=False), '', '## Meyers timing', 'Meyers is JAX in every available roster week (1–6, 8), and receiving PBP posteam is JAX in those same seven games. There is no within-2026 team transition in this snapshot. A trade to JAX may predate this sample, but these files cannot establish a transaction or trade date. Week 7 has no roster/receiving entry and is JAX’s bye; it is not evidence of a team change. Only seven JAX games are observed.', '', '## Pressure', 'FTN n_blitzers > 0 and n_pass_rushers >= 5 are distinct measures, each using its own non-null charted dropback denominator. Sack and QB-hit rates use all eligible dropbacks with known respective PBP flags. League includes BAL; league_ex_BAL is also supplied.', pressure.to_markdown(index=False), '', f'PBP was_pressure column present: {"was_pressure" in p0}. Proxy = qb_hit OR sack OR FTN is_qb_out_of_pocket OR qb_scramble. Positive known signals establish proxy pressure; clean requires all four known and false. Otherwise unknown. This proxy includes movement and is not a direct pressure measure. If was_pressure exists it additionally supplies the primary pressure split; proxy remains separately available.', '', 'Time to throw is not in PBP. qb_location/read_thrown are not time-to-throw or receiver alignment/route measurements.', '', '## Shallow target / check-down proxy', 'air_yards <= 2 includes designed screens and short throws; it does not prove a progression check-down. Targets with null air yards cannot qualify. All tied rank-1 receivers below are leaders.', check[check['rank'].eq(1)].to_markdown(index=False), '', '## Route-area proxy and FTN coverage', 'route_area_proxy.csv uses pass_location × depth: <=0, 1–4, 5–14, >=15 air yards, plus unknowns. These are targeted-pass areas, not routes run or slot/outside alignments. Both Lawrence and team-all-QB versions are supplied. screens.csv counts FTN screen-target flags with charted N. FTN alignment/route fields found: '+(', '.join(route_fields) or 'none')+'.', '', 'FTN columns: '+', '.join(f.columns)+'.', '', '## Verification', 'Assertions passed: unique PBP/FTN join keys; one-to-one join; seven expected JAX weeks; 28 selected snap rows and seven appearances per player; target shares/counts reconcile; Lawrence blitz groups partition all dropbacks.', '', '## Anomalies and limitations (final audit)']
notes += ['- Brian Thomas Jr. is Brian Thomas in snaps and '+', '.join(sorted(j.loc[j.receiver_player_id.eq(ids[names[3]]),'receiver_player_name'].dropna().unique()))+' in PBP. IDs distinguish him from DE Bryan Thomas Jr.; identities are normalized using GSIS/PFR IDs.']
notes += [f'- QB attempt counts: {attempts.groupby("passer_player_name").size().to_dict()}; all-QB and Lawrence target tables therefore differ.']
notes += [f'- JAX target nulls: air_yards={int(attempts.loc[attempts.receiver_player_id.notna(),"air_yards"].isna().sum())}; pass_location={int(attempts.loc[attempts.receiver_player_id.notna(),"pass_location"].isna().sum())}; attempts without named/identified receiver={int((attempts.receiver_player_id.isna() & attempts.receiver_player_name.isna()).sum())}.']
notes += [f'- Lawrence dropbacks={len(l)}; FTN unmatched={int(l.ftn_merge.ne("both").sum())}; missing n_blitzers={int(l.n_blitzers.isna().sum())}; missing n_pass_rushers={int(l.n_pass_rushers.isna().sum())}; missing out-of-pocket={int(l.is_qb_out_of_pocket.isna().sum())}; pressure-proxy unknown={int(l.pressure_proxy.eq("unknown").sum())}.']
notes += [f'- JAX dropbacks with null passer: {int((db.posteam.eq("JAX") & db.passer_player_name.isna()).sum())}; all nine are Lawrence scrambles attributed using rusher identity and included in his dropbacks.', '- Snap and PBP game counts match for all four players (7 each); roster has no Week 7 JAX entries. Snapshot cannot answer later weeks or establish an exact historical trade date.', '- Missing FTN observations are never interpreted as no blitz. Small split samples and seven-game player samples limit conclusions. No receiver route/alignment or time-to-throw data supplied.']
(OUT/'notes_a.md').write_text('\n\n'.join(notes)+'\n')
print(f'Wrote {len(list(OUT.glob("*.csv")))} CSVs and notes_a.md; assertions passed.')
