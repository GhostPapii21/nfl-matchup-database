"""Ghost6 audit 2026-11-03 item 7: apply the new wiring (tools/depth_wiring.py) to the FD m1638 replay manifest, then gate_run.py.
  N1 carry_share -> RB carries only, last 4 games with the current QB (C.Williams / S.Darnold)
  depth fields   -> target_share (pbp, last 4 current-QB), defender_giving (defender, or coverage level vs 75%+ zone), te_rank, rung label kept
  Kupp           -> matchup from the ESPN WR/CB slot/primary chart (week8/sources/espn_wrcb_wk8.json holds the CHI@SEA wk9 pairings), not WR3->CB#3
Point-in-time: pbp weeks<9 (r3 src, thru 2026-10-29)."""
import json,sys,pandas as pd,numpy as np
ROOT='/workspace/nfl-database'; sys.path.insert(0,ROOT+'/tools'); import depth_wiring as DW
SRC=ROOT+'/runs/2026-11-02_CHI@SEA_r3/src/'; RUN=ROOT+'/backtests/mnf_chi_sea_replay_2026-11-03/run/run_manifest.json'
p=pd.read_parquet(SRC+'play_by_play_2026.parquet'); pl=pd.read_parquet(SRC+'players.parquet',columns=['gsis_id','position','display_name'])
POS=dict(zip(pl.gsis_id,pl.position)); F=json.load(open(SRC+'features.json'))
WRCB=json.load(open(ROOT+'/week8/sources/espn_wrcb_wk8.json'))
PFR=pd.read_html('/workspace/nfl-sim/mnf12/pfr_def_adv_2026.html')[0]; PFR.columns=[c[1] for c in PFR.columns]; PFR=PFR[PFR.Player!='Player']
QB={'CHI':'C.Williams','SEA':'S.Darnold'}
qid={t:p[(p.posteam==t)&(p.passer_player_name==n)].passer_player_id.iloc[0] for t,n in QB.items()}
def pid(name,team):
    x=p[(p.posteam==team)]; ids=pd.concat([x[['receiver_player_id','receiver_player_name']].set_axis(['i','n'],axis=1),x[['rusher_player_id','rusher_player_name']].set_axis(['i','n'],axis=1)]).dropna()
    full=pl[pl.display_name==name].gsis_id.tolist(); return next((i for i in full if i in set(ids.i)),None)
DEPCHI={'nb':['Kyler Gordon']}   # CHI nickel (ESPN depth); used only if a SEA WR is slot-majority
def pfr(n):
    x=PFR[PFR.Player==n]
    if not len(x):   # not in PFR cache -> same pbp-credit PROXY the replay template uses (INT/PBU/tackler on targeted plays, weeks<9)
        ab='.'.join([n.split()[0][0],n.split()[-1]]); x=p[(p.defteam=='CHI')&(p.pass_attempt==1)&(p.sack!=1)&p.receiver_player_id.notna()]
        c=[k for k in ['interception_player_name','pass_defense_1_player_name','pass_defense_2_player_name','solo_tackle_1_player_name','assist_tackle_1_player_name','tackle_with_assist_1_player_name'] if k in p.columns]
        h=x[x[c].eq(ab).any(axis=1)]
        return dict(name=n,pos='CB',targets=float(len(h)),comp_pct=float(h.complete_pass.mean()) if len(h) else None,ypt=round(float(h.yards_gained.fillna(0).sum())/max(len(h),1),2),primary=True,source='PROXY pbp credit (INT/PBU/tackler on targeted plays) weeks<9; nflverse pbp',pulled_et='2026-11-02T19:45',true_asof='pbp through week 8')
    r=x.iloc[0]; return dict(name=n,pos=r.Pos,targets=float(r.Tgt),comp_pct=float(r['Cmp%'])/100,ypt=float(r['Yds/Tgt']),primary=True,source='PFR advanced defense 2026 (/workspace/nfl-sim/mnf12/pfr_def_adv_2026.html)',pulled_et='2026-11-02T19:45')
lgcb=float(pd.to_numeric(PFR[PFR.Pos.isin(['CB','DB','LCB','RCB'])&(pd.to_numeric(PFR.Tgt,errors='coerce')>=8)]['Yds/Tgt'],errors='coerce').mean())
m=json.load(open(RUN)); log={}
for L in m['legs']:
    t,o=L['team'],L['opp']; i=pid(L['player'],t)
    if L['type']=='RB' and i:
        cs=DW.rb_carry_share(p,POS,t,i,qid[t],source='nflverse pbp weeks<9 (r3 src)'); old=(L.get('carry_share') or {}).get('value')
        if cs: L['carry_share']=cs; L.setdefault('rb_role',{}).update(shares=cs['shares'],share60_3of4=sum(x>=0.6 for x in cs['shares'])>=3); log[L['player']]=('N1',old,cs['value'],cs['shares'],cs['games'])
    if L['type'] in ('WR','TE') and i:
        if L['type']=='TE': L['te_rank']=DW.te_rank(p,POS,t,i,qid[t])
        w=WRCB.get(L['player'])
        if L['player']=='Cooper Kupp' and w:
            sp=DW.slot_primary(w,DEPCHI); pr=pfr(sp['name'])
            if pr: pr['basis']=sp['basis']; L['coverage']['defenders']=[pr]; log['Kupp']=('matchup','Tyrique Stevenson (WR3->CB#3)',sp['name'],sp['basis'],pr['ypt'])
            se=L.get('scheme_edge')
            if se and pr:
                thin=pr['targets']<8; ok=(not thin) and (pr['ypt']>lgcb if L['side']=='over' else pr['ypt']<lgcb)
                se['matchup'].update(ok=bool(ok),detail=f"primary {pr['name']} (slot chart) {pr['ypt']} ypt on {pr['targets']:.0f} credited tgt vs league CB {lgcb:.2f}"+(' - sample < 8 tgt: too thin to grade' if thin else ''),source=pr['source']+' + ESPN WR/CB cheatsheet')
                if not all(se[k]['ok'] for k in ('matchup','scheme_fit','script','form_trend')): se.pop('explanation',None)
        dfn=(L.get('coverage') or {}).get('defenders') or [None]; d0=dfn[0]
        zone=((L.get('coverage') or {}).get('man_zone') or {}).get('value',{}).get('zone')
        bk='wr_outside_ypt_proxy' if (L['type']=='WR' and w and float(w['slot'])<max(float(w['lwr']),float(w['rwr']))) else 'wr_middle_ypt_proxy'
        tv=[v[bk] for v in F['teams'].values() if isinstance(v,dict) and v.get(bk) is not None]
        dg=DW.defender_giving(dict(d0,targets=d0.get('targets')) if d0 else None,lgcb,zone_pct=zone,coverage_allow=dict(value=F['teams'][o][bk],bucket=bk,source='features.json teams.'+bk+' (nflverse pbp weeks<9)'),league_cov=float(np.mean(tv)))
        ts=DW.target_share(p,t,i,qid[t],source='nflverse pbp weeks<9 (r3 src)')
        L['depth']=dict(script_pass=(L.get('depth') or {}).get('script_pass') or DW.script_pass(3.25 if t=='CHI' else -3.25,46.5,'odds snapshot 2026-11-03T00:45:36Z (SEA -3.25, total 46.5)'),target_share=ts,defender_giving=dg)
        log.setdefault(L['player'],('depth',L.get('wr_rank'),L.get('te_rank'),ts and ts['value'],dg['ok'],dg['level'],dg['detail']))
json.dump(m,open(RUN,'w'),indent=1,default=str)
for k,v in log.items(): print(k,v)
