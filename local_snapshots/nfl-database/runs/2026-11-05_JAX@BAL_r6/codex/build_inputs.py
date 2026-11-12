"""Rebuild sourced r6 inputs; no network requests or changes to earlier runs."""
import json, datetime as dt, sys
from pathlib import Path
from zoneinfo import ZoneInfo
import pandas as pd
ROOT=Path(__file__).resolve().parents[3]; RUN=Path(__file__).resolve().parents[1]; OUT=RUN/'codex'
PBP=ROOT/'runs/2026-11-05_JAX@BAL_r2/src/play_by_play_2026.parquet'
def stamp(p): return dt.datetime.fromtimestamp(Path(p).stat().st_mtime,ZoneInfo('America/New_York')).strftime('%Y-%m-%dT%H:%M')
def dump(n,x): (OUT/n).write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
p=pd.read_parquet(PBP); p=p[(p.season_type=='REG')&(p.two_point_attempt!=1)&(p.game_date<'2026-11-05')]
pl=pd.read_parquet(ROOT/'runs/2026-11-01_shared_src/players.parquet'); pos=pl.drop_duplicates('gsis_id').set_index('gsis_id').position_group
sys.path.insert(0,str(ROOT/'tools'))
import depth_wiring as wiring
r=p[(p.posteam=='BAL')&(p.rush_attempt==1)&(p.qb_kneel!=1)&p.rusher_player_id.map(pos).eq('RB')]
historical_games=r.groupby('game_id').game_date.first().sort_values().tail(4).index
bal_db=p[(p.posteam=='BAL')&(p.qb_dropback==1)]
latest=bal_db[bal_db.game_date==bal_db.game_date.max()]
qb_id=latest.passer_player_id.fillna(latest.rusher_player_id).value_counts().index[0]
qb_name=latest[latest.passer_player_id==qb_id].passer_player_name.iloc[0]
qb_dates=wiring._last_qb_games(p,'BAL',qb_id,before='2026-11-05')
games=r[r.game_date.isin(qb_dates)].groupby('game_id').game_date.first().sort_values().index
last=r[r.game_id.isin(games)]; hen=last[last.rusher_player_name=='D.Henry']
cs=dict(value=len(hen)/len(last),source=str(PBP),pulled_et=stamp(PBP),definition='Henry designed carries / all BAL RB designed carries in latest up to 4 BAL games led by current QB; QB runs and kneels excluded',numerator=len(hen),denominator=len(last),games=list(games),by_game=[dict(game=g,henry=int((hen.game_id==g).sum()),team_rb=int((last.game_id==g).sum())) for g in games])
cs['current_qb']=qb_name
hist=r[r.game_id.isin(historical_games)]
cs['historical_last4']=dict(numerator=int((hist.rusher_player_name=='D.Henry').sum()),denominator=len(hist),games=list(historical_games),note='Mixed starting QBs; context only, not current-QB N1 window')
extras={'Henry 40+ rush (o39.5)':{'carry_share':cs}}
# Position ranks are historical target ranks, not an invented depth-chart assignment.
jdb=p[(p.posteam=='JAX')&(p.qb_dropback==1)]
jlatest=jdb[jdb.game_date==jdb.game_date.max()]
jqb=jlatest.passer_player_id.value_counts().index[0]
dates=wiring._last_qb_games(p,'JAX',jqb,before='2026-11-05')
a=p[(p.posteam=='JAX')&(p.pass_attempt==1)&(p.sack!=1)&p.game_date.isin(dates)]
for name,short,position in [('Strange 4+ rec (o3.5)','B.Strange','TE'),('Strange 40+ rec yds (o39.5)','B.Strange','TE'),('Washington rec yds o63.5','P.Washington','WR')]:
 pid=a[a.receiver_player_name==short].receiver_player_id.iloc[0]
 vc=a[a.receiver_player_id.map(pos)==position].receiver_player_id.value_counts()
 rank=wiring.te_rank(p,pos,'JAX',pid,jqb,before='2026-11-05') if position=='TE' else int(list(vc.index).index(pid)+1)
 extras[name]={position.lower()+'_rank':rank,'rank_evidence':dict(source=str(PBP),pulled_et=stamp(PBP),games=sorted(a.game_id.unique()),definition='Position target rank in last four team games led by current QB; depth_wiring convention',targets=int(vc[pid]))}
dump('legs_extra.json',extras)
# Defender performance is observed; individual future assignments are hypotheses, not verified shadow coverage.
table=ROOT/'week10/bal_secondary/defender_table.csv'; df=pd.read_csv(table).set_index('defender'); cov={}
missing_source=ROOT/'week10/brainstorm_layers/layers.md'
def missing(reason): return dict(status='MISSING',reason=reason,value=None,source=str(missing_source),pulled_et=stamp(missing_source))
def defender(name,assignment):
 x=df.loc[name]; return dict(name=name,targets=int(x.tgt),completions=int(x.cmp),comp_pct=float(x.cmp_pct)/100,ypt=float(x.y_per_tgt),source=str(ROOT/'week10/bal_secondary/pfr_bal_defense_advanced.csv'),pulled_et='2026-11-04T07:05',season=2026,data_week=8,primary=False,assignment_status='UNVERIFIED',assignment=assignment,alignment=x.pff_alignment,alignment_source=str(ROOT/'week10/pff_jax_bal/defenders.csv'))
for leg in ['Strange 4+ rec (o3.5)','Strange 40+ rec yds (o39.5)','Washington rec yds o63.5']:
 strange=leg.startswith('Strange')
 ds=[defender('Kyle Hamilton','Candidate safety/slot defender; no charted Strange assignment. Addendum 3 removes suppression weight.')] if strange else [defender('Marlon Humphrey','RCB candidate against Washington offense-left targets; pass_location is not alignment.'),defender('Nate Wiggins','Outside CB candidate; PFF projects 7.48 matchup snaps, equal to Humphrey.'),defender('Kyle Hamilton','Slot candidate; PFF projects 13.52 snaps; not a verified primary assignment.')]
 cov[leg]=dict(defenders=ds,man_zone=missing('No actual BAL man/zone rates in r2-r5, snapshot or free PFF; participation unavailable.'),mof=missing('No actual BAL MOFO/MOFC rates; pass-location areas cannot substitute for coverage shells.'),assignment_source=str(ROOT/'runs/2026-11-05_JAX@BAL_r5/read_addendum3_2026-11-04.md'),assignment_status='UNVERIFIED',caution='Hamilton suppression is NOT COUNTED per addendum 3; no verified primary defender. PFR and PFF use different samples/definitions.',matchup_source=str(ROOT/'week10/pff_jax_bal/receiver_matchups.csv'))
_ovp=OUT/'coverage_overrides_2026-11-04.json'
if _ovp.exists():
    for _leg,_o in json.loads(_ovp.read_text()).items():
        if _leg=='_meta' or _leg not in cov: continue
        _have={d['name'] for d in cov[_leg]['defenders']}
        cov[_leg]['defenders']+=[d for d in _o.get('defenders',[]) if d['name'] not in _have]
        if 'injury_note' in _o: cov[_leg]['injury_note']=_o['injury_note']
dump('coverage.json',cov)
ftpath=ROOT/'week10/bal_secondary/raw/ftn_charting_2026.parquet'; f=pd.read_parquet(ftpath)
f=f.rename(columns={'nflverse_game_id':'game_id','nflverse_play_id':'play_id'})
x=p.merge(f,on=['game_id','play_id'],how='left',suffixes=('','_ftn'),validate='one_to_one')
db=x[(x.defteam=='BAL')&((x.qb_dropback==1)|(x.pass_attempt==1))]; chart=db[db.n_pass_rushers.notna()]
q=x[(x.posteam=='JAX')&(x.passer_player_name=='T.Lawrence')&((x.qb_dropback==1)|(x.pass_attempt==1))]
a=q[(q.pass_attempt==1)&(q.sack!=1)]; target=a[a.receiver_player_id.notna()]
press=(q.sack.eq(1)|q.qb_hit.eq(1)|q.qb_scramble.eq(1)|q.is_qb_out_of_pocket.fillna(False).eq(True))
tp=q[press&q.receiver_player_id.notna()]; source=str(PBP); time=stamp(PBP)
def block(value,definition,src=source,**kw): return dict(value=value,definition=definition,source=src,pulled_et=time,season=2026,data_week=8,**kw)
pi=dict(blitz_rate=block(float(chart.n_pass_rushers.ge(5).mean()),'BAL defense: >=5 pass rushers / FTN-charted dropbacks',source+' + '+str(ftpath),sample=len(chart)),pressure_rate=block(float((db.sack.eq(1)|db.qb_hit.eq(1)|db.qb_scramble.eq(1)).mean()),'BAL defense (sack OR qb_hit OR qb_scramble) / dropbacks',label='PROXY',sample=len(db)),checkdown_share=block(float((a.air_yards.le(0)|a.receiver_player_id.map(pos).eq('RB')).mean()),'Lawrence attempts with air_yards<=0 OR RB target / non-sack attempts',label='PROXY',sample=len(a)),time_to_throw=missing('No valid NGS time-to-throw source; pbp has no time-to-throw field. Do not substitute play clock.'),targets_under_pressure=block(dict(total=len(tp),by_receiver={str(k):int(v) for k,v in tp.receiver_player_name.value_counts().items()},share_of_targets=len(tp)/len(target)),'Lawrence targeted attempts under sack/hit/scramble/FTN out-of-pocket proxy; sacks cannot be targeted attempts',source+' + '+str(ftpath),label='PROXY',dropbacks_under_proxy=int(press.sum())))
dump('pressure_inputs.json',pi)
# Explicit stamps for assembler sources; source acquisition timestamps remain unchanged.
dump('sources.json',[dict(category='coverage_matchups',name='PFR BAL advanced defense (G=8)',url_or_file=str(ROOT/'week10/bal_secondary/pfr_bal_defense_advanced.csv'),pulled_et='2026-11-04T07:05',tool='existing PFR extraction',season=2026,data_week=8),dict(category='coverage_matchups',name='FTN charting via nflverse + pbp',url_or_file=str(ftpath),pulled_et=stamp(ftpath),tool='existing nflverse parquet',season=2026,data_week=int(f.week.max()))])
print('Henry carry share',cs['value'],cs['numerator'],cs['denominator']); print('pressure',json.dumps(pi,indent=1))
