import json,sqlite3,pandas as pd
B='/workspace/nfl-database'
J=json.load(open('player_types.json'));T=J['teams']
u=pd.read_sql('select * from fix_player_game_usage',sqlite3.connect(f'{B}/fixes/fixes.sqlite'))
for t,L in T.items():
  for q in L:
    if q['pos']=='QB': continue
    h=u[u.gsis_id==q['gsis']].sort_values('week')
    if len(h):
      z=h.iloc[-1]; q['last_game']=dict(week=int(z.week),snap=round(100*z.offense_pct,1) if z.offense_pct<=1 else z.offense_pct,targets=z.targets,carries=z.carries)
      sp=q['last_game']['snap']
      if q['pos']=='TE' and sp>=80 and (z.targets or 0)<=2:
        q['types'].append('Blocking usage spike (last game)'); q['secondary']=q['types'][1:]
json.dump(J,open('player_types.json','w'),indent=1,default=str)
D=json.load(open(f'{B}/week8/defense/defense_profiles.json'))['teams']
slate=json.load(open(f'{B}/week8/slate.json'))['games']
M={'LAR':'LA','WSH':'WAS'};n=lambda t:M.get(t,t)
games=[(n(g['matchup'].split(' @ ')[0]),n(g['matchup'].split(' @ ')[1]),g.get('spread'),g.get('total')) for g in slate]+[('CAR','GB','see TNF','')]
rbrec_rank=sorted(D,key=lambda t:-D[t]['RB']['rec_pg'])
def dv(t):
  d=D[t];s=d.get('sharp') or {}
  return dict(out=s.get('YPT Allowed Outside'),slot=s.get('YPT Allowed Slot'),wr=s.get('YPT Allowed WR',round(d['WR']['ypt'],1)),te=s.get('YPT Allowed TE',round(d['TE']['ypt'],1)),rb=s.get('YPT Allowed RB'),rb_rec_pg=round(d['RB']['rec_pg'],1),rb_rec_rank=rbrec_rank.index(t)+1,ypc=round(d['RB_rush']['ypc'],2),blitz=s.get('Blitz Rate',round(d['ftn_blitz_rate'],1)))
OUT={'Out','Injured Reserve','Doubtful','Suspension'}
def fits(off,de):
  v=dv(de);F=[];X=[]
  hb=v['blitz'] is not None and v['blitz']>=35
  for q in T[off]:
    if q['pos']=='QB': continue
    ty=q['types'];ts=q.get('tgt_share_l3') or 0;cs=q.get('car_share_l3') or 0;tpg=(q.get('tg') or 0)/max(q['gp'],1)
    out=q['injury'] in OUT; tag=f" [{q['injury']}]" if q['injury'] not in('none listed','Active') else ''
    def add(why,gate,num):
      (F if gate and not out else X).append(f"{q['player']} ({'/'.join(ty[:2])}){tag}: {why} | gate {'PASS' if gate else 'FAIL'} ({num})"+(' — OUT/IR' if out else ''))
    if any(k in ' '.join(ty) for k in('Explosive','Boundary')) and v['out'] and v['out']>=10.5: add(f"outside YPT {v['out']} ≥10.5",ts>=18,f"L3 tgt {ts}%")
    if 'Slot' in ' '.join(ty) and v['slot'] and v['slot']>=10.0: add(f"slot YPT {v['slot']} ≥10.0 (working)",ts>=18,f"L3 tgt {ts}%")
    if any(k.startswith('Volume') for k in ty) and v['wr']>=9.0: add(f"WR YPT {v['wr']} ≥9.0 (capped +2–3%)",ts>=18,f"L3 tgt {ts}%")
    if q['pos']=='TE':
      if v['te']>=8.0:
        if 'TE-as-primary' in ty or 'Move/seam TE' in ty: add(f"TE YPT {v['te']} ≥8.0",ts>=15,f"L3 tgt {ts}%, snap {q.get('snap_l3')}%")
        else: X.append(f"{q['player']} ({'/'.join(ty)}): TE YPT {v['te']} soft but WRONG TYPE — no edge (L3 tgt {ts}%)")
      if v['te']<=5.5 and 'TE-as-primary' in ty: X.append(f"{q['player']}: TE YPT {v['te']} ≤5.5 → cut yards")
    if q['pos'] in('RB','FB'):
      if ('Rush-receive' in ty or 'Receiving/3rd-down back' in ty) and ((v['rb'] or 0)>=7.0 or v['rb_rec_rank']<=8): add(f"RB YPT {v['rb']}, RB rec/g {v['rb_rec_pg']} (rank {v['rb_rec_rank']})",tpg>=3,f"{tpg:.1f} tgt/g")
      if any(k in ' '.join(ty) for k in('Early-down','Elite')):
        if v['ypc']>4.4: add(f"run YPC allowed {v['ypc']} >4.4",cs>=50,f"L3 carry {cs}%")
        elif v['ypc']<=3.8: X.append(f"{q['player']}: run YPC allowed {v['ypc']} ≤3.8 → RUN SUPPRESSION")
      elif v['ypc']>4.4 and cs>=15: X.append(f"{q['player']} ({'/'.join(ty)}): soft run D {v['ypc']} but committee/role — gate L3 carry {cs}%")
    if hb:
      if 'Check-down/blitz-beater TE' in ty or 'Receiving/3rd-down back' in ty or 'Screen/YAC' in ty: add(f"blitz {v['blitz']}% ≥35 boosts check-down",ts>=12 or tpg>=3,f"L3 tgt {ts}%")
      if any(k.startswith('Volume') or k=='Explosive/deep' for k in ty) and ts>=20: X.append(f"{q['player']}: heavy blitz {v['blitz']}% → volume cut on primary")
  return v,F,X
md=['# MATCHUP_FIT — Week 8 (data thru Wk7)','Defense numbers: Sharp Football (updated Oct 20) where present; run YPC & RB rec/g from nflverse pbp (defense_profiles.json). Gate = L3 target share ≥18% WR / ≥15% TE, RB L3 carry share ≥50% (rush) or ≥3 tgt/g (receiving). Slot/outside on OFFENSE side is a pass_location proxy. Injury per ESPN 10/29 AM; Questionable = low alts/fade per user rule, not cut.','']
summary={}
for a,h,sp,tot in games:
  md.append(f'## {a} @ {h}  ({sp} / {tot})')
  for off,de in((a,h),(h,a)):
    v,F,X=fits(off,de)
    md.append(f'**{off} offense vs {de} D** — out {v["out"]}, slot {v["slot"]}, WR {v["wr"]}, TE {v["te"]}, RB YPT {v["rb"]}, RB rec/g {v["rb_rec_pg"]} (#{v["rb_rec_rank"]}), run YPC {v["ypc"]}, blitz {v["blitz"]}%')
    md+=['- FIT: '+f for f in F] or ['- FIT: none pass type+gate']
    md+=['- trap/no edge: '+x for x in X]
    summary[f'{off} vs {de}']=dict(fits=F,traps=X)
  md.append('')
open('MATCHUP_FIT.md','w').write('\n'.join(md));json.dump(summary,open('matchup_fit.json','w'),indent=1)
cols=['player','pos','primary','secondary','tgt_share_season','tgt_share_l3','car_share_season','car_share_l3','snap_l3','adot','catch_pct','yac_per_rec','ngs_yacoe','deep20_rate','middle_share','rz_tgts','third_tgts','car','ypc','i10_car','inside_run_share','ngs_ryoe_att','injury']
EX={'Explosive/deep':'outside YPT ≥10.5','Boundary (L/R-target proxy)':'outside YPT ≥10.5','Slot (middle-target proxy)':'slot YPT (working ≥10.0)','Volume/possession':'WR YPT ≥9.0 (capped)','Volume (target-share) receiver':'WR YPT ≥9.0 (capped)','TE-as-primary':'TE YPT ≥8.0','Move/seam TE':'TE YPT ≥8.0 + middle-open','Blocking/inline TE':'NONE — soft TE D gives no edge','Rush-receive':'RB YPT / RB rec allowed + run YPC','Receiving/3rd-down back':'RB YPT/RB catches, high blitz','Early-down/between-tackles':'run YPC >4.4; ≤3.8 suppress','Early-down lead back':'run YPC >4.4; ≤3.8 suppress','Elite rusher (RYOE)':'run YPC >4.4','Check-down/blitz-beater TE':'high blitz','Screen/YAC':'high blitz, poor tackling (gap)','Goal-line/RZ back':'RZ TD% allowed (TD slips only)','Committee member':'capped — volume gate usually fails'}
for t,L in T.items():
  r=[f'# {t} player types (data thru Wk7; working definitions in TYPES.md)','']
  for pos in ['WR','TE','RB','FB','QB']:
    P=[q for q in L if q['pos']==pos]
    if not P: continue
    r.append(f'## {pos}')
    if pos=='QB':
      r.append('| QB | types | att/g | aDOT | 20+ air % | scramble %/db | scr att/g | designed runs/g | rush yds/g | injury |\n|-|-|-|-|-|-|-|-|-|-|')
      for q in P: r.append(f"| {q['player']} | {', '.join(q['types'])} | {q['att_pg']} | {q['adot']} | {q['deep20_rate']} | {q['scramble_rate']} | {q['scr_att_pg']} | {q['designed_runs_pg']} | {q['rush_yds_pg']} | {q['injury']} |")
    else:
      r.append('| player | types | tgt% szn/L3 | car% szn/L3 | snap L3 | aDOT | catch% | YAC/rec | YACOE | 20+air% | mid% | RZ tgt | 3rd tgt | car | YPC | inside10 car | inside-run% | RYOE/att | last game | injury | exploits |\n|'+'-|'*21)
      for q in sorted(P,key=lambda q:-max(q.get('tgt_share_l3') or 0,(q.get('car_share_l3') or 0)/2)):
        g=lambda k:'' if q.get(k) is None else q.get(k)
        lg=q.get('last_game');lgs=f"W{lg['week']} {lg['snap']}% {int(lg['targets'] or 0)}t/{int(lg['carries'] or 0)}c" if lg else ''
        ex='; '.join(sorted({EX[x] for x in q['types'] if x in EX}))
        r.append(f"| {q['player']} | **{q['primary']}**{(' + '+', '.join(q['secondary'])) if q['secondary'] else ''}{' ⚠'+q['sample_note'] if q.get('sample_note') else ''} | {g('tgt_share_season')}/{g('tgt_share_l3')} | {g('car_share_season')}/{g('car_share_l3')} | {g('snap_l3')} | {g('adot')} | {g('catch_pct')} | {g('yac_per_rec')} | {g('ngs_yacoe')} | {g('deep20_rate')} | {g('middle_share')} | {g('rz_tgts')} | {g('third_tgts')} | {g('car')} | {g('ypc')} | {g('i10_car')} | {g('inside_run_share')} | {g('ngs_ryoe_att')} | {lgs} | {q['injury']} | {ex} |")
    r.append('')
  r.append('Gaps: true alignment (slot/wide), route participation, personnel packages, PFF grades — not in sources. NGS fields blank = below NGS qualifying minimum.')
  open(f'{t}.md','w').write('\n'.join(r))
print('ok')
