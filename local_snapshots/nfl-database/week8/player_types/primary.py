import pandas as pd,json
p=pd.read_parquet('/workspace/nfl-database/fixes/src/play_by_play_2026.parquet');p=p[(p.season_type=='REG')&(p.week<=7)]
J=json.load(open('player_types.json'));T=J['teams']
pa=p[(p.pass_attempt==1)&p.receiver_player_id.notna()]
pa=pa.assign(tl=(pa.down==3)&(pa.ydstogo>=7),pr=(pa.qb_hit==1))
lines=['','# USER PRIMARY LABELS (authoritative taxonomy, v2)','Each team lists its power backs, rush-receive backs, TE-as-receiver, high-volume WRs, explosive WRs and safety valves, plus whether it relies on the run.','']
for t,L in T.items():
  tp=p[(p.posteam==t)&((p.pass_attempt==1)|(p.rush_attempt==1))&(p.qb_kneel!=1)]
  rs=round(100*(tp.rush_attempt==1).mean(),1); gms=tp.game_id.nunique()
  tl_tot=pa[(pa.posteam==t)&pa.tl].shape[0]; pr_tot=pa[(pa.posteam==t)&pa.pr].shape[0]
  bk={k:[] for k in['POWER/VOLUME BACK','RUSH-RECEIVE BACK','TE-AS-RECEIVER','WR HIGH-VOLUME','WR EXPLOSIVE','SAFETY VALVE']}
  rec_rank=sorted([q for q in L if q['pos']!='QB'],key=lambda q:-max(q.get('tgt_share_l3') or 0,q.get('tgt_share_season') or 0))[:2]
  for q in L:
    if q['pos']=='QB': continue
    gp=max(q['gp'],1); g=lambda k:q.get(k) or 0
    rpg=g('rec')/gp; ypg=g('rec_yds')/gp; tpg=g('tg')/gp; rypg=g('rush_yds')/gp; cpg=g('car')/gp
    ypr=g('rec_yds')/max(g('rec'),1)
    x=pa[(pa.posteam==t)&(pa.receiver_player_id==q['gsis'])]
    tl=round(100*x.tl.sum()/max(tl_tot,1),1); pr=round(100*x.pr.sum()/max(pr_tot,1),1)
    q.update(rec_pg=round(rpg,1),rec_ypg=round(ypg,1),rush_ypg=round(rypg,1),yds_per_rec=round(ypr,1),third_long_tgt_share=tl,qbhit_tgt_share=pr)
    P=[]
    if q['pos'] in('RB','FB'):
      if cpg>=14 and rypg>=65 and g('ypc')>=4.2: P.append('POWER/VOLUME BACK'+(' (RYOE+)' if g('ngs_ryoe_att')>0 else ' (RYOE n/a or ≤0)'))
      if cpg>=8 and rpg>=2.5 and ypg>=18: P.append('RUSH-RECEIVE BACK')
    if q['pos']=='TE' and q in rec_rank and ypg>=45: P.append('TE-AS-RECEIVER')
    if q['pos']=='WR' and tpg>=7 and rpg>=5 and ypg>=60: P.append('WR HIGH-VOLUME')
    if q['pos']=='WR' and ypr>=14.5 and rpg<=4.5 and g('rec')>=8 and (ypg>=45 or g('rec20')>=4): P.append('WR EXPLOSIVE')
    if g('tg')>=10 and g('adot')<=6.5 and ypg<45 and rpg>=1.5 and not any(k.startswith('POWER') for k in P) and (tl>=15 or (pr>=15 and x.pr.sum()>=3)): P.append('SAFETY VALVE')
    q['user_labels']=P
    for k in P: bk[k.split(' (')[0]].append(f"{q['player']} ({q['rec_pg']} rec/{q['rec_ypg']} yds/g" + (f", {round(cpg,1)} car/{q['rush_ypg']} rush yds/g, YPC {q.get('ypc')}, RYOE/att {q.get('ngs_ryoe_att')}" if q['pos'] in('RB','FB') else f", aDOT {q.get('adot')}, Y/R {q['yds_per_rec']}") + f", 3rd&7+ tgt {tl}%, QB-hit tgt {pr}%; {q['injury']})")
  pb=bk['POWER/VOLUME BACK']; rely='YES' if rs>=45 and pb else ('lean' if rs>=43 or pb else 'no')
  J.setdefault('team_run_reliance',{})[t]=dict(rush_share=rs,relies_on_run=rely)
  lines.append(f"## {t}: rush share {rs}% of plays, relies on run: **{rely}**")
  lines+= [f"- {k}: "+('; '.join(v) if v else '—') for k,v in bk.items()]; lines.append('')
  s=f'{t}.md'; md=open(s).read().split('\n## USER PRIMARY')[0]
  open(s,'w').write(md+'\n\n## USER PRIMARY LABELS\n'+'\n'.join(lines[-8:]))
json.dump(J,open('player_types.json','w'),indent=1,default=str)
open('USER_LABELS.md','w').write('\n'.join(lines))
