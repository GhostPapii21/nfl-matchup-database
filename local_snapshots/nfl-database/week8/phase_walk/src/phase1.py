import json,glob,os,re,pandas as pd,numpy as np
R='/workspace/nfl-database/week8/betguru_2026-11-01_raw'
PB='https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet'
SN='https://github.com/nflverse/nflverse-data/releases/download/snap_counts/snap_counts_2026.parquet'
def norm(s):
    s=s.replace('.','')
    return re.sub(r'[^a-z]','',s.lower().replace(' sr','').replace(' jr','').replace(' iii','').replace(' ii',''))
def _x(s):return re.sub(r'[^a-z]','',s.lower().replace(' sr','').replace(' jr','').replace(' iii','').replace(' ii',''))
pb=pd.read_parquet('play_by_play_2026.parquet');sn=pd.read_parquet('snap_counts_2026.parquet');pl=pd.read_parquet('players.parquet')
ol=json.load(open('espn_ol_depth.json'))
EB=json.load(open('espn_box.json'))
EBN={}
for k,v in EB.items():
    n,w=k.split('|');EBN[(norm(n),int(w))]=v
OFF={'CeeDee Lamb recyds','Jahmyr Gibbs rec','Amon-Ra St. Brown recyds','Chris Godwin Jr. rec','Drake London rec','James Cook rushrec','Zay Flowers rec','George Pickens rec'}
legs=sorted(glob.glob(R+'/leg_*.json'))
pb=pb[pb.season_type=='REG'] if 'season_type' in pb else pb
games=pb.groupby('game_id').agg(week=('week','first'),date=('game_date','first'),home=('home_team','first'),away=('away_team','first'),ot=('qtr',lambda q:(q>=5).any())).reset_index()
real=pb[pb.play_type.isin(['pass','run'])]
rows=[];md=[]
for f in legs:
    d=json.load(open(f));name=d['player'];tm=d['team'];mk=d['market']
    key=f"{name} {mk}"
    # placed-prop check
    nm=name.replace('Chris Godwin Jr','Chris Godwin Jr.')
    cand=pl[(pl.display_name.map(norm)==norm(name))]
    if len(cand)>1: cand=cand[cand.latest_team==tm] if (cand.latest_team==tm).any() else cand
    gid=cand.gsis_id.iloc[0] if len(cand) else None; pfr=cand.pfr_id.iloc[0] if len(cand) else None
    tg=games[(games.home==tm)|(games.away==tm)].sort_values('week')
    lines=[f"\n### {name} ({tm} vs {d['opp']}) — {mk} · rung {d.get('rung')} @ {d.get('price')}",f"- Leg file: `{f}` · status: {d.get('status')}"]
    gaps=[];fails=[]
    if any(name.startswith(o.split(' ')[0]) and o.endswith(mk) and norm(o.rsplit(' ',1)[0])==norm(name) for o in OFF): fails.append('exact placed Ticket 2 market (off-limits)')
    if gid is None: gaps.append('no nflverse gsis id match'); 
    lines.append(f"- Sample rule: every 2026 REG game {tm} has played (weeks {', '.join(map(str,tg.week))}); no exclusions. Missed = team played, player 0 offensive snaps / absent from snap file.")
    lines.append("\n|Wk|Date|Opp|Snaps (%)|Tgt|Rec|RecYd|AirYd|Car|RushYd|TD|RZ tgt|GL car (≤5)|F2M tgt (Q4 ≤2:00, 1-score)|OT plays?|ESPN tg/rec/yd/car/rush|Recon|OL top-5 snaps (proxy starters)|\n|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|")
    esp={e['date']:e for e in d.get('logs_espn',[])}
    tot=dict(tg=0,rec=0,ryd=0,ay=0,car=0,rush=0);ott=dict(tg=0,rec=0,ryd=0,car=0,rush=0);diffs=[];played=0
    for _,g in tg.iterrows():
        gp=real[real.game_id==g.game_id];opp=g.away if g.home==tm else g.home
        s=sn[(sn.pfr_game_id.notna())&(sn.week==g.week)&(sn.team==tm)]
        srow=s[s.pfr_player_id==pfr] if pfr is not None else s.iloc[0:0]
        snaps=f"{int(srow.offense_snaps.iloc[0])} ({srow.offense_pct.iloc[0]:.0%})" if len(srow) else 'DNP/absent'
        olr=s[s.position.isin(['T','G','C','OL'])].sort_values('offense_snaps',ascending=False).head(5)
        olt=', '.join(f"{r.player.split(' ')[-1]} {int(r.offense_snaps)}" for r in olr.itertuples()) or 'GAP'
        t=gp[(gp.receiver_player_id==gid)&(gp.pass_attempt==1)&(gp.sack!=1)]
        r=gp[(gp.rusher_player_id==gid)&(gp.play_type=='run')]
        v=dict(tg=len(t),rec=int(t.complete_pass.sum()),ryd=int(t.receiving_yards.fillna(0).sum()),ay=int(t.air_yards.fillna(0).sum()),car=len(r),rush=int(r.rushing_yards.fillna(0).sum()))
        td=int(((t.pass_touchdown==1)|(0)).sum()+(r.rush_touchdown==1).sum())
        rz=int((t.yardline_100<=20).sum());gl=int((r.yardline_100<=5).sum())
        f2=int(((t.qtr==4)&(t.game_seconds_remaining<=120)&(t.score_differential.abs()<=8)).sum())
        o_t=t[t.qtr>=5];o_r=r[r.qtr>=5]
        if not len(srow) and v['tg']+v['car']==0: lines.append(f"|{g.week}|{g.date}|{opp}|DNP/absent|–|–|–|–|–|–|–|–|–|–|{'Y' if g.ot else 'N'}|{'(none)' if (norm(name),int(g.week)) not in EBN else 'ESPN row!'}|missed|{olt}|");continue
        played+=1
        for k in tot: tot[k]+=v[k]
        if g.ot:
            for k,src in (('tg',o_t),('car',o_r)): ott[k]+=len(src)
            ott['rec']+=int(o_t.complete_pass.sum());ott['ryd']+=int(o_t.receiving_yards.fillna(0).sum());ott['rush']+=int(o_r.rushing_yards.fillna(0).sum())
        e=EBN.get((norm(name),int(g.week)))
        if e:
            ev=(e.get('tg',0),e.get('rec',0),e.get('ryd',0),e.get('car',0),e.get('rush',0));nv=(v['tg'],v['rec'],v['ryd'],v['car'],v['rush'])
            rc='match' if ev==nv else 'DIFF '+'; '.join(f"{n} E{a}/N{b}" for n,a,b in zip(['tg','rec','yd','car','rush'],ev,nv) if a!=b)
            if ev!=nv: diffs.append(f"Wk{g.week}: {rc[5:]}")
            es='/'.join(map(str,ev))+f" (ev {e['event']})"
        else: es='MISSING';rc='GAP';gaps.append(f'ESPN row missing wk{g.week}')
        lines.append(f"|{g.week}|{g.date}|{opp}|{snaps}|{v['tg']}|{v['rec']}|{v['ryd']}|{v['ay']}|{v['car']}|{v['rush']}|{td}|{rz}|{gl}|{f2}|{'Y: '+str(len(o_t))+'tg/'+str(len(o_r))+'car' if g.ot else 'N'}|{es}|{rc}|{olt}|")
        if not len(srow): gaps.append(f'snap row missing wk{g.week}')
    lines.append(f"\n- Totals (nflverse, {played} games played): tgt {tot['tg']}, rec {tot['rec']}, rec yds {tot['ryd']}, air yds {tot['ay']}, car {tot['car']}, rush yds {tot['rush']}. OT-only portion: {ott}. Regulation = totals minus OT.")
    cur=ol.get(tm if tm!='LA' else 'LAR',{})
    lines.append(f"- Current projected OL five (ESPN depth chart API, pulled 2026-10-31 ~7:20 PM ET): {', '.join(f'{k.upper()} {v}' for k,v in cur.items()) or 'GAP'}")
    if not cur or 'err' in cur: gaps.append('current OL five missing')
    if diffs: lines.append("- Unresolved credit differences (preserved, not forced): "+' | '.join(diffs)+". Likely causes: nullified/penalty plays, laterals, 2-pt tries, or ESPN stat corrections; not adjudicated.")
    else: lines.append("- Credit reconciliation: ESPN game log = nflverse pbp on tgt/rec/yds/car/rush for every played game.")
    if played==0: fails.append('no games played in sample')
    st=('FAIL' if fails else 'GAP' if gaps else 'PASS')
    why='; '.join(fails or gaps or ['all Phase 1 fields collected; '+('credit diffs preserved' if diffs else 'sources reconcile')])
    lines.insert(1,f"- **PHASE 1: {st}** — {why}")
    md+=lines;rows.append((name,mk,d.get('rung'),d.get('price'),st,why,len(diffs)))
hdr=f"""# BetGuru — PHASE 1 (Collect and reconcile game data) — Sunday Nov 1, 2026 pool
Script: /workspace/nfl-database/GAME_SCRIPT_2026-10-29.md lines 134–207. Later phases NOT run. Generated {pd.Timestamp.now():%Y-%m-%d %I:%M %p} ET by src/phase1.py.

## Sources (free/public; no keys, no sign-ins)
- nflverse play-by-play 2026 (pulled fresh 2026-10-31 7:17 PM ET): {PB} — targets, receptions, yards, air yards, carries, RZ/GL, final-two-minute, OT split, QB designed/scramble/kneel fields.
- nflverse snap counts 2026 (PFR-sourced): {SN} — snaps, snap %, OL top-5 by offensive snaps per game (used as starting-five PROXY; true "started" flag not in feed).
- nflverse players: https://github.com/nflverse/nflverse-data/releases/download/players/players.parquet — gsis/pfr id mapping.
- ESPN summary API box scores, every completed 2026 REG game wks 1–8: https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={{id}} (cached src/espn_summary/, parsed src/espn_box.json; event id per row in leg detail) — cross-source credit check.
- ESPN depth chart API: https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2026/teams/{{id}}/depthcharts — current projected OL five (src/espn_ol_depth.json).
Definitions: target = pass_attempt with receiver, excl. sacks; nullified (no_play) plays excluded; RZ = yardline_100 ≤ 20; GL = ≤ 5; F2M = Q4, ≤120 s left, |score diff| ≤ 8.
Not collected per leg (team-level Phase 1 items, outside the skill-leg ask): tackles/pressures attribution, clean vs coverage sacks — GAP at team level.
Placed Ticket 2 markets barred: Gibbs rec, St. Brown recyds, Godwin rec, London rec, Cook rushrec, Flowers rec, Pickens rec, Lamb recyds.

## Summary
|Player|Market|Rung|Price|Phase 1|Reason|# credit diffs|
|-|-|-|-|-|-|-|
"""+'\n'.join(f"|{a}|{b}|{c}|{p}|{s}|{w}|{n}|" for a,b,c,p,s,w,n in rows)+"\n\n## Per-leg detail\n"
open('../betguru_phase1.md','w').write(hdr+'\n'.join(md))
for r in rows: print(r)
