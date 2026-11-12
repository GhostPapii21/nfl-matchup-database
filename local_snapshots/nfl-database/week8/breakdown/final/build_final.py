import json,re,pandas as pd,numpy as np,os
W='/workspace/nfl-database/week8/'
B=json.load(open(W+'breakdown/breakdown.json')); C=json.load(open(W+'breakdown/coverage/coverage.json'))
PT=json.load(open(W+'player_types/player_types.json'))['teams']; INJ=json.load(open(W+'injuries.json'))['teams']
RM=json.load(open(W+'rematches/first_meetings.json'))
ESPN={'LA':'LAR','WAS':'WSH'}; ES=lambda t:ESPN.get(t,t)
def inj(t): return INJ.get(ES(t)) or INJ.get(t) or []
# CLE verification: ESPN team roster API (teams/5/roster) confirms Verse (traded for Garrett), Howard, Jenkins on CLE; add Outs missing from league list
cle_extra=[('Jeremiah Owusu-Koramoah','LB','Out'),('Joe Royer','TE','Out'),('Bub Means','WR','Out'),('Nathaniel Watson','LB','Out')]
names={a['name'] for a in inj('CLE')}
for n,pz,d in cle_extra:
    if n not in names: INJ.setdefault('CLE',[]).append({'name':n,'pos':pz,'designation':d})
INJ.update(json.load(open(W+'breakdown/final/tnf_injuries_espn_roster.json')))
pbp=pd.read_parquet('/tmp/play_by_play_2026.parquet'); pbp=pbp[pbp.week<=7]
s25=pd.read_parquet('/tmp/stats_player_week_2025.parquet')
ps=pbp[(pbp.play_type=='pass')&pbp.receiver_player_id.notna()]
gpd=pbp.groupby('defteam').game_id.nunique()
exp_allowed=(pbp[(pbp.play_type=='pass')&(pbp.yards_gained>=20)].groupby('defteam').size()/gpd).round(2)
rk_exp=exp_allowed.rank(ascending=False,method='min').astype(int)
lgexp=round(exp_allowed.mean(),2)
team_g={t:sorted(pbp[pbp.posteam==t].week.unique()) for t in pbp.posteam.dropna().unique()}
def l3(gs,team):
    wk=team_g[team][-3:]; d=ps[(ps.receiver_player_id==gs)&(ps.posteam==team)]
    out=[]
    for w in wk:
        z=d[d.week==w]; out.append((w,len(z),int(z.complete_pass.sum()),int(z[z.complete_pass==1].yards_gained.sum())))
    return out
def h2h(gs,team,opp):
    r=[]
    z=s25[(s25.player_id==gs)&(s25.opponent_team==opp)]
    for _,x in z.iterrows(): r.append(f"2025 Wk{x.week}: {int(x.targets)} tgt, {int(x.receptions)}-{int(x.receiving_yards)}"+(f", {int(x.carries)} car {int(x.rushing_yards)} yds" if x.carries else ''))
    d=pbp[(pbp.posteam==team)&(pbp.defteam==opp)]
    for w in sorted(d.week.unique()):
        q=ps[(ps.week==w)&(ps.receiver_player_id==gs)&(ps.posteam==team)]
        ru=d[(d.week==w)&(d.rusher_player_id==gs)]
        s=f"2026 Wk{w}: {len(q)} tgt, {int(q.complete_pass.sum())}-{int(q[q.complete_pass==1].yards_gained.sum())}"
        if len(ru): s+=f", {len(ru)} car {int(ru.yards_gained.sum())} yds"
        r.append(s)
    return r or ['no prior meeting in DB (2025 + 2026 Wk1-7)']
def abbr(n): p=n.replace('.',' ').split(); return (p[0][0]+'.'+p[-1]) if len(p)>1 else n
def tree(lst,n):
    for s in lst or []:
        m=re.match(r'(.+?) \((\w+)\) ([\d.]+)%',s)
        if m and (m.group(1)==abbr(n) or m.group(1).split('.')[-1]==n.split()[-1] and m.group(1)[0]==n[0]): return float(m.group(3))
    return 0.0
def ptinfo(team,name):
    for p in PT.get(team,[]):
        if p['player']==name or abbr(p['player'])==name or (p['player'].split()[-1]==name.split('.')[-1] and p['player'][0]==name[0]): return p
lg=B['league_rb_ypc']
defs={}
for g in B['games']:
    for t,s in g['sides'].items(): defs[s['opp_defense'].get('name',None) or t]=None
# rank YPC allowed among 26 slate defenses
alld=[]
for g in B['games']:
    a,h=list(g['sides'])
    alld+= [(h,g['sides'][a]['opp_defense']),(a,g['sides'][h]['opp_defense'])]
ypcs=sorted([d['rb_ypc_allowed'] for _,d in alld],reverse=True); tds=sorted([d['rb_rush_td_pg'] for _,d in alld],reverse=True)
rk=lambda v,l:l.index(v)+1
OL={'OT','T','G','OG','C','OL'}
def tone(v): return {'SOFT':'success','TOUGH':'danger'}.get(v)
out={'built':'2026-10-29','games':[]}
for g in B['games']:
    a,h=list(g['sides']); game={'id':f'{a}@{h}','odds':' '.join(map(str,g['odds'])).strip(),'sides':[]}
    cov={s['offense']:s for s in next(x for x in C['games'] if x['game']==g['game'])['sides']}
    md=[f"# {a} @ {h} — Week 8 Run & Receiver Breakdown\nLine: {game['odds']}. Matchup ranking, not a bet (no props pulled). Data through Week 7.\n"]
    for O in (a,h):
        D=h if O==a else a; s=g['sides'][O]; o=s['offense']; d=s['opp_defense']
        side={'label':f'{O} offense vs {D} defense','run':{},'rec':{}}
        # PART1
        props=[['YPC allowed to RBs',f"{d['rb_ypc_allowed']} (#{rk(d['rb_ypc_allowed'],ypcs)} most of 26 slate D; lg {lg})"],
               ['RB rush yds/g allowed',str(d['rb_rush_yds_pg'])],['RB rush TD/g allowed',f"{d['rb_rush_td_pg']} (#{rk(d['rb_rush_td_pg'],tds)} of 26)"],
               ['RB receiving allowed/g',f"{d['rb_recyds_pg']} yds, {d['rb_rec_pg']} rec, {d['rb_tgt_pg']} tgt (#{d['rb_recyds_rank_most_allowed']} most in NFL)"],
               ['Total rush yds / points allowed/g',f"{d['rush_yds_pg']} / {d['pts_allowed_pg']}"],
               ['Weak side/gap',f"{d['weak_dir']} ({d['by_dir'][d['weak_dir']]['ypc']} YPC on {d['by_dir'][d['weak_dir']]['car']} car vs lg {d['by_dir'][d['weak_dir']]['lg']})"],
               ['Box / blitz',f"Blitz {d.get('ftn_blitz_pct')}%, 3rd-down blitz {d.get('3rd_blitz_pct')}%, heavy box {d['sharp'].get('Heavy Box Rate')}%, man {d['sharp'].get('Man Rate')}% / zone {d['sharp'].get('Zone Rate')}%"]]
        rbrows=[];rbcards=[]
        bad={abbr(x['name']) for x in inj(O) if x['designation'] in ('Out','Injured Reserve')}
        rbs=[r for r in o['rbs'] if (r['car_pg_l3']>=4 or r['tgt_pg_l3']>=2) and r['name'] not in bad][:3]
        for r in rbs:
            pt=ptinfo(O,r['name']) or {}
            lab=', '.join(pt.get('user_labels') or [pt.get('primary','GAP')])
            top=sorted(r['dir_share'].items(),key=lambda x:-x[1])[:2]
            gate='PASS' if r['car_pg_l3']>=12 else ('rec-only' if r['tgt_pg_l3']>=3 else 'FAIL')
            note=' (1-game sample)' if r['gp']<=1 else ''
            rbrows.append([r['name']+note,lab,f"{r['car_pg_l3']} / {r['car_pg']}",str(r['ypc']),', '.join(f'{k} {v}%' for k,v in top),f"{r['tgt_pg_l3']}/{r['rec_pg_l3']}/{r['recyds_pg_l3']}",f"{r['tgt_pg']}/{r['rec_pg']}/{r['recyds_pg']}",gate])
        f=rbs[0] if rbs else None
        dinj=[x for x in d.get('front_injuries',[])+[y for y in d.get('db_injuries',[]) if '(S,' in y] if 'Active' not in x]
        if D in('GB','CAR'): dinj=[f"{x['name']} ({x['pos']}, {x['designation']})" for x in inj(D) if x['pos'] in('DE','DT','LB','S') and x['designation'] in('Out','Questionable','Doubtful')]
        oinj=[f"{x['name']} ({x['pos']}, {x['designation']})" for x in inj(O) if (x['pos'] in OL or x['pos']=='RB') and x['designation']!='Active']
        injrows=[[x,'Helps run: '+('front-seven body down' if '(S,' not in x else 'run-support safety down')] for x in dinj]+[[x,('Hurts run: OL depth/blocking' if x.split('(')[1][:2]!='RB' else 'RB status: if he sits, carries shift to the next back (check 90-min inactives)')] for x in oinj]
        verdict='NEUTRAL'
        if f:
            if f['car_pg_l3']>=12 and d['rb_ypc_allowed']>=lg+0.3: verdict='RUN EDGE'
            elif d['rb_ypc_allowed']<=lg-0.3: verdict='TRAP'
            elif f['car_pg_l3']<12: verdict='NEUTRAL (volume gate fails)'
        recb=[r for r in rbs if r['tgt_pg_l3']>=3 and d['rb_recyds_rank_most_allowed']<=10]
        rv=('YES: '+', '.join(r['name'] for r in recb)) if recb else 'NO'
        vline=f"{verdict} for {f['name'] if f else 'n/a'} ({f['ypc'] if f else '-'} YPC vs {d['rb_ypc_allowed']} allowed); receiving-back edge: {rv}"
        if O=='GB': vline+='. Jacobs carries a 1-game sample in the corrected data; verify before use.'
        side['run']={'props':props,'rbs':rbrows,'inj':injrows,'verdict':vline,'tone':'success' if verdict=='RUN EDGE' else ('danger' if verdict=='TRAP' else None)}
        # PART2
        cv=cov.get(O,{}); mm={m['receiver']:m for m in cv.get('matchups',[])}
        sy=cv.get('sharp_ypt',{})
        zone=' | '.join(f"{k.upper()} {v['ypt']} YPT (#{v['rank_of_32']} most of 32, lg {v['lg']})" for k,v in sy.items())
        qbb,qbn=o.get('qb_blitz',{}),o.get('qb_noblitz',{})
        qbline=f"{o.get('qb')} vs blitz: {qbb.get('comp_pct')}% comp, {qbb.get('ypa')} YPA, {qbb.get('sacks')} sk, {qbb.get('int')} INT, EPA {qbb.get('epa')} ({qbb.get('dropbacks')} db) | no blitz: {qbn.get('comp_pct')}%, {qbn.get('ypa')} YPA, EPA {qbn.get('epa')}. {D} blitzes {d.get('ftn_blitz_pct')}%."
        if O=='PHI': qbline+=' NOTE: these splits are Hurts\'s; McKee has no sample.'
        cards=[];
        recs=[r for r in o['receivers'] if r.get('injury') not in ('Out','Injured Reserve')]
        allp=[(r['player'],r['pos'],r) for r in recs]+[(r['name'],'RB',r) for r in rbs if r['tgt_pg_l3']>=2]
        for nm,pos,r in allp:
            pt=ptinfo(O,nm) or {}
            if pt and pt.get('team')!=O: continue
            if pt and pt.get('on_current_roster') is False: continue
            gs=pt.get('gsis'); full=pt.get('player',nm)
            L=l3(gs,O) if gs else []
            l3t=sum(x[1] for x in L)/max(len(L),1); l3y=sum(x[3] for x in L)/max(len(L),1)
            sy_pg=pt.get('rec_ypg') or 0
            trend='up' if l3y>sy_pg*1.15 else ('down' if l3y<sy_pg*0.85 else 'flat')
            H=h2h(gs,O,D) if gs else ['GAP (no id)']
            b05=tree(o.get('blitz_tree_0_5'),full); b515=tree(o.get('blitz_tree_5_15'),full)
            m=mm.get(full) or mm.get(nm) or {}
            rating=m.get('rating','n/a') if pos!='RB' else ('SOFT' if d['rb_recyds_rank_most_allowed']<=8 else ('TOUGH' if d['rb_recyds_rank_most_allowed']>=25 else 'NEUTRAL'))
            ts_l3=pt.get('tgt_share_l3',r.get('tgt_share_l3')); ts_s=pt.get('tgt_share_season',r.get('tgt_share_season'))
            rec20=pt.get('rec20',0); ex=exp_allowed.get(D)
            sc=(ts_l3 or 0)*1.0+{'SOFT':8,'NEUTRAL':0,'TOUGH':-8}.get(rating,0)+{'up':3,'flat':0,'down':-3}[trend]+(b05+b515)/10*(1 if d.get('ftn_blitz_pct',0)>=35 else .5)+ (2 if rec20>=3 and rk_exp.get(D,32)<=10 else 0)+(pt.get('rz_tgts',0) or 0)*.3
            gate=l3t>=(2 if pos=='RB' else 3) and ((ts_l3 or 0)>=(12 if pos in('TE','RB') else 15) or (pos=='RB' and l3t>=3))
            if not gate: sc-=10
            st=next((x['designation'] for x in inj(O) if x['name']==full),r.get('injury'));q=' (Q)' if st=='Questionable' else (' (D)' if st=='Doubtful' else '')
            ul=', '.join(pt.get('user_labels') or [pt.get('primary','GAP')])
            defl=(f"{m.get('likely_defender')} {m.get('defender_depth')}: {m.get('defender_line')} [{m.get('defender_flag')}] ({m.get('inferred_alignment')})" if m else (f"RB coverage: {D} allows {d['rb_recyds_pg']} RB rec yds/g (#{d['rb_recyds_rank_most_allowed']})" if pos=='RB' else 'GAP: no inferred defender'))
            cards.append({'name':full+q,'pos':pos,'type':ul,'score':round(sc,1),'gate':gate,'rating':rating,
              'rows':[['Type / position',f"{ul} / {pos}, aDOT {pt.get('adot','GAP')}, {('slot' if 'slot' in str(m.get('inferred_alignment','')) else m.get('inferred_alignment','RB'))}"],
                ['Target share L3 / season',f"{ts_l3}% / {ts_s}%"],
                ['Last 3 (tgt-rec-yds)',' | '.join(f"Wk{w}: {t}-{c}-{y}" for w,t,c,y in L)+f"  trend {trend} (L3 {l3y:.0f} vs season {sy_pg} yds/g)"],
                ['Season per game',f"{pt.get('rec_pg','GAP')} rec, {sy_pg} yds"],
                ['Head-to-head vs '+D,'; '.join(H)],
                ['Blitz hot-read share','0-5 air yds: '+(f'{b05}%' if b05 else 'not in top 4')+'; 5-15: '+(f'{b515}%' if b515 else 'not in top 4')],
                ['Explosive / RZ',f"{rec20} catches of 20+; {D} allows {ex} 20+ pass plays/g (#{rk_exp.get(D)} most, lg {lgexp}); RZ targets {pt.get('rz_tgts','GAP')}"],
                ['Defender / mismatch',defl+f" -> {rating}"],
                ['Coverage shell',f"{D} man {d['sharp'].get('Man Rate')}% / zone {d['sharp'].get('Zone Rate')}%; player man/zone split GAP"]]})
        cards.sort(key=lambda c:-c['score'])
        best=next((c for c in cards if c['gate'] and c['pos']!='RB'),cards[0] if cards else None)
        rank=[f"{i+1}. {c['name']} ({c['pos']}, {c['rating']}, score {c['score']}){'' if c['gate'] else ' — fails volume gate'}" for i,c in enumerate(cards)]
        ss=[f"{x['pair']}: {x['label']} (n={x['n']}, r={x['r_yds']}){'; flips '+', '.join(x['flip_games']) if x['flip_games'] else ''}" for x in o.get('seesaw',[])]
        if O=='NYJ': ss=['NOISE, ignore: '+x+' (Allen rec yds never top 30)' if 'Allen' in x else x for x in ss]
        side['rec']={'zone':zone,'qb':qbline,'seesaw':ss,'cards':cards,'rank':rank,'best':best['name'] if best else 'n/a','bestwhy':(f"{best['score']} score: {best['rows'][1][1]} share, {best['rating']} matchup, {best['rows'][7][1]}" if best else '')}
        game['sides'].append(side)
        # markdown
        md.append(f"\n## PART 1 — RUN: {side['label']}\n"+'\n'.join(f"- **{k}:** {v}" for k,v in props))
        md.append('\n| RB | Type | Car/g L3 / season | YPC | Top directions | L3 tgt/rec/yds | Season tgt/rec/yds | Gate |\n|'+'---|'*8+'\n'+'\n'.join('| '+' | '.join(r)+' |' for r in rbrows))
        md.append('\n**Injuries:**\n'+('\n'.join(f'- {x}: {y}' for x,y in injrows) or '- none listed that affect the run'))
        md.append(f"\n**Verdict:** {vline}\n")
    for side in game['sides']:
        r=side['rec']; md.append(f"\n## PART 2 — RECEIVERS: {side['label']}\n- Coverage YPT: {r['zone']}\n- {r['qb']}\n- Seesaw: "+('; '.join(r['seesaw']) or 'none tested'))
        for c in r['cards']:
            md.append(f"\n### {c['name']} — {c['pos']}\n"+'\n'.join(f"- **{k}:** {v}" for k,v in c['rows']))
        md.append('\n**Ranking (matchup, not a bet):**\n'+'\n'.join(r['rank'])+f"\n\n> **BEST PICK {side['label'].split()[0]}: {r['best']}** — {r['bestwhy']}\n")
    allc=[(c,s['label'].split()[0]) for s in game['sides'] for c in s['rec']['cards'] if c['gate'] and c['pos']!='RB']
    bo=max(allc,key=lambda x:x[0]['score']) if allc else None
    game['best_overall']=f"{bo[0]['name']} ({bo[1]})" if bo else 'n/a'
    md.append(f"\n> **Best overall in game: {game['best_overall']}**\n")
    open(W+f"breakdown/final/{a}_at_{h}.md",'w').write('\n'.join(md))
    out['games'].append(game)
json.dump(out,open(W+'breakdown/final/final.json','w'))
for g in out['games']:
    print(g['id'],'|',' || '.join(f"{s['label'].split()[0]}: {s['run']['verdict'].split(' (')[0]} / best {s['rec']['best']}" for s in g['sides']),'| overall',g['best_overall'])
