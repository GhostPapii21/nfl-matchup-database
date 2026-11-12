# Deterministic per-team opportunity + projection build (Week 8). Reads only; writes breakdown/full/.
import json,re,pandas as pd,numpy as np
W='/workspace/nfl-database/week8/'
B=json.load(open(W+'breakdown/breakdown.json')); C=json.load(open(W+'breakdown/coverage/coverage.json'))
F=json.load(open(W+'breakdown/final/final.json')); S=json.load(open(W+'slate.json'))['games']
PT=json.load(open(W+'player_types/player_types.json'))['teams']; INJ=json.load(open(W+'injuries.json'))['teams']
INJ.update(json.load(open(W+'breakdown/final/tnf_injuries_espn_roster.json')))
RA={'LA':'LAR','WAS':'WSH'}
def roster(t):
    try: return json.load(open(W+f'rosters/{RA.get(t,t)}.json'))['players']
    except FileNotFoundError: return None
def inj(t): return INJ.get(RA.get(t,t)) or INJ.get(t) or []
pbp=pd.read_parquet('/tmp/play_by_play_2026.parquet'); pbp=pbp[(pbp.week<=7)]
p25=pd.read_parquet('/tmp/play_by_play_2025.parquet')
ps=pbp[(pbp.play_type=='pass')&pbp.receiver_player_id.notna()]
ru=pbp[(pbp.play_type=='run')&pbp.rusher_player_id.notna()]
norm=lambda s:re.sub(r'[^a-z]','',re.sub(r'\b(jr|sr|ii|iii|iv)\b\.?','',s.lower()))
def key(full):
    p=full.replace('.',' ').split(); p=[x for x in p if x.lower().strip('.') not in('jr','sr','ii','iii','iv')]
    return (p[0][0].lower(),norm(p[-1]))
def skey(short):
    m=re.match(r'([A-Za-z])[A-Za-z]*\.(.+)',short or ''); return (m.group(1).lower(),norm(m.group(2).split()[-1] if m else '')) if m else None
# team-level
tg=pbp.groupby('posteam').game_id.nunique()
plays=pbp[pbp.play_type.isin(['pass','run'])]
tplays=plays.groupby('posteam').size()/tg; tpass=(plays.play_type=='pass').groupby(plays.posteam).mean()
pts=pbp.groupby(['posteam','game_id']).posteam_score_post.max().groupby('posteam').mean()
# defense allowed rates by receiver position (via roster pos lookup per player id)
posmap={}
for t in PT:
    for p in PT[t]:
        if p.get('gsis'): posmap[p['gsis']]=p['pos']
ps=ps.assign(rpos=ps.receiver_player_id.map(posmap))
def drate(df,grp):
    a=df.groupby(grp).agg(t=('play_id','size'),c=('complete_pass','sum'),y=('yards_gained','sum'))
    return a
dpos=ps.groupby(['defteam','rpos']).agg(t=('play_id','size'),c=('complete_pass','sum'),y=('yards_gained','sum'))
lpos=ps.groupby('rpos').agg(t=('play_id','size'),c=('complete_pass','sum'),y=('yards_gained','sum'))
rbr=ru[ru.rusher_player_id.map(posmap)=='RB']; dypc=rbr.groupby('defteam').yards_gained.mean(); lypc=rbr.yards_gained.mean()
def mult(D,pos):
    pg='RB' if pos=='RB' else pos
    try: d=dpos.loc[(D,pg)]; l=lpos.loc[pg]
    except KeyError: return 1.0,1.0
    cm=np.clip((d.c/d.t)/(l.c/l.t),.92,1.08); ym=np.clip((d.y/d.t)/(l.y/l.t),.85,1.15)
    return round(cm,3),round(ym,3)
def h2h(gsis,team,opp):
    r=[]
    for yr,df in((2025,p25),(2026,pbp)):
        d=df[(df.defteam==opp)&(df.week<=(7 if yr==2026 else 99))&((df.receiver_player_id==gsis)|(df.rusher_player_id==gsis))]
        for w in sorted(d.week.unique()):
            q=d[(d.week==w)&(d.receiver_player_id==gsis)&(d.play_type=='pass')]; c=d[(d.week==w)&(d.rusher_player_id==gsis)&(d.play_type=='run')]
            if len(q) or len(c):
                s=f"{yr} W{w}: {len(q)}t {int(q.complete_pass.sum())}-{int(q[q.complete_pass==1].yards_gained.sum())}"
                if len(c): s+=f", {len(c)}c-{int(c.yards_gained.sum())}"
                r.append(s)
    return r or ['no prior meeting in DB']
def tree(lst,n):
    k=key(n)
    for s in lst or []:
        m=re.match(r'(.+?) \((\w+)\) ([\d.]+)%',s)
        if m and skey(m.group(1))==k: return float(m.group(3))
    return None
def film(team):
    fn={'LA':'LAR','WAS':'WSH'}.get(team,team)
    try: txt=open(W+f'film/{fn}_film.md').read()
    except: return {}
    out={}
    for ln in txt.splitlines():
        c=ln.split('|')
        if len(c)>10 and c[2]==team or (len(c)>10 and c[2]==fn):
            if 'verified vs DB' not in c[10]: continue
            for nm in re.split(r';\s*',c[3]):
                y=c[5]
                try: y=int(float(y))
                except: y=None
                out.setdefault(nm.strip(),[]).append(y)
    # merge abbreviated/full spellings of the same player (e.g. 'Derrick Henry' + 'D.Henry')
    def fk(n): n=re.sub(r'\s+(Jr|Sr|II|III|IV)\.?$','',n.strip()); return (n[:1]+'|'+re.split(r'[ .]+',n)[-1]).lower()
    m={}
    for k,v in out.items():
        c=fk(k); best=m.get(c)
        if best is None: m[c]=[k,list(v)]
        else:
            if len(k)>len(best[0]): best[0]=k
            best[1]+=v
    return {k:v for k,v in m.values()}
FIN={g['id']:g for g in F['games']}
def card_lookup(game,O,full):
    for s in FIN[game]['sides']:
        if s['label'].startswith(O+' '):
            for c in s['rec']['cards']:
                if c['name'].split(' (')[0]==full: return c
    return None
out={'built':'2026-10-29','method':None,'games':[]}
for g in B['games']:
    a,h=list(g['sides']); gid=f'{a}@{h}'
    sl=next((x for x in S if x['matchup'].replace('WSH','WAS').replace('LAR','LA')==f'{a} @ {h}' or x['matchup']==f'{a} @ {h}'),None)
    if sl: sp=sl['spread']; tot=sl['total']
    else:
        sp='GB -3.5'; tot=46.5; sl={'odds_provider':'DraftKings via ESPN scoreboard 2026-10-29 pull'}
    m=re.match(r'(\w+) ([-+]?[\d.]+)',sp or '')
    fav,line=(m.group(1),float(m.group(2))) if m else (None,0.0)
    cov={s['offense']:s for s in next(x for x in C['games'] if x['game']==g['game'])['sides']}
    G={'id':gid,'line':f"{sp}, total {tot} ({sl.get('odds_provider')})",'teams':[]}
    for O in (a,h):
        D=h if O==a else a; o=g['sides'][O]['offense']; d=g['sides'][O]['opp_defense']
        favO = (fav==O or (fav in RA.values() and RA.get(O)==fav))
        spr = line if favO else -line  # negative = favored
        imp=round(tot/2-spr/2,1)
        lab='favorite' if spr<=-3 else ('underdog' if spr>=3 else 'toss-up')
        pr_adj={'favorite':-0.03,'underdog':0.03,'toss-up':0.0}[lab]
        if spr<=-7: pr_adj=-0.05
        if spr>=7: pr_adj=0.05
        basepl=tplays[O]; pf=np.clip(1+0.5*(imp/pts[O]-1),.92,1.08)
        PL=round(basepl*pf,1); PR=float(np.clip(tpass[O]+pr_adj,.4,.72))
        PA=round(PL*PR,1); RA_=round(PL-PA,1)
        rost=roster(O); rkeys={key(p['name']):p for p in rost} if rost else {}; rex={norm(p['name']):p for p in rost} if rost else {}
        tq={norm(x['name']):x['designation'] for x in inj(O)}
        wks=sorted(pbp[pbp.posteam==O].week.unique()); L3=wks[-3:]
        tp=ps[ps.posteam==O]; tr=ru[ru.posteam==O]
        ids=set(tp.receiver_player_id)|set(tr.rusher_player_id)
        players=[]
        for pid in ids:
            pt=next((p for p in PT.get(O,[]) if p.get('gsis')==pid),None)
            short=(tp[tp.receiver_player_id==pid].receiver_player_name.tolist()+tr[tr.rusher_player_id==pid].rusher_player_name.tolist())[0]
            pos=(pt or {}).get('pos') or posmap.get(pid)
            if pos not in('WR','TE','RB'): continue
            full=(pt or {}).get('player') or short
            rp=rex.get(norm(full)) or (None if (pt and rex) and norm(full) not in rex and sum(1 for k in rkeys if k==key(full))==0 else rkeys.get(key(full))) or (rkeys.get(skey(short)) if not pt else None)
            if rost is not None and not rp: players.append({'name':full,'pos':pos,'off_roster':True}); continue
            if rp: full=rp['name']
            st=tq.get(norm(full),'')
            if st in('Out','Injured Reserve','Doubtful') : players.append({'name':full,'pos':pos,'out':st}); continue
            q=tp[tp.receiver_player_id==pid]; r=tr[tr.rusher_player_id==pid]
            gl=[]
            for w in wks:
                qq=q[q.week==w]; rr=r[r.week==w]
                gl.append((int(w),len(qq),int(qq.complete_pass.sum()),int(qq[qq.complete_pass==1].yards_gained.sum()),len(rr),int(rr.yards_gained.sum())))
            played=[x for x in gl if x[1] or x[4]]; gp=max(len(played),1)
            l3=[x for x in gl if x[0] in L3]
            pg=lambda L,i: round(sum(x[i] for x in L)/max(len(L),1),1)
            tt=len(tp.groupby('week')); 
            def share(L,i,df):
                tot_=len(df[df.week.isin([x[0] for x in L])]); return round(100*sum(x[i] for x in L)/max(tot_,1),1)
            seasonL=played
            tpg_s=round(sum(x[1] for x in gl)/gp,1); tpg_3=pg(l3,1); cpg_s=round(sum(x[4] for x in gl)/gp,1); cpg_3=pg(l3,4)
            ts_s=share(gl,1,tp); ts_3=share(l3,1,tp); cs_s=share(gl,4,tr); cs_3=share(l3,4,tr)
            gate = (tpg_s>=3 or tpg_3>=3) if pos in('WR','TE') else (cpg_s>=5 or cpg_3>=5 or tpg_s>=2 or tpg_3>=2)
            tg_=len(q); rec=int(q.complete_pass.sum()); ry=int(q[q.complete_pass==1].yards_gained.sum())
            cr=rec/tg_ if tg_ else 0; ypt=ry/tg_ if tg_ else 0
            adot=round(q.air_yards.mean(),1) if tg_ else None
            rz_t=int((q.yardline_100<=20).sum()); rz_c=int((r.yardline_100<=20).sum())
            third=int((q.down==3).sum())
            mid=round(100*(q.pass_location=='middle').mean(),0) if tg_ else None
            cv=next((mm for mm in cov.get(O,{}).get('matchups',[]) if key(mm['receiver'])==key(full)),None)
            card=card_lookup(gid,O,full) or card_lookup(gid,O,(pt or {}).get('player',''))
            b05=tree(o.get('blitz_tree_0_5'),full); b515=tree(o.get('blitz_tree_5_15'),full)
            # projection
            sh_t=(0.6*ts_3+0.4*ts_s)/100; sh_c=(0.6*cs_3+0.4*cs_s)/100
            cm,ym=mult(D,pos)
            if pos=='RB':
                ym_r=float(np.clip(dypc.get(D,lypc)/lypc,.85,1.15)); ypc=r.yards_gained.mean() if len(r) else 0
            pt_=PA*sh_t; prec=pt_*cr*cm; pyd=pt_*ypt*ym
            pc=RA_*sh_c if pos=='RB' else 0; pry=pc*ypc*ym_r if pos=='RB' and len(r) else 0
            if pos!='RB' and len(r): pc=round(len(r)/gp,1); pry=pc*(r.yards_gained.mean())
            tot_med=pyd+pry
            hist=np.array([x[3]+x[5] for x in played]) if played else np.array([0])
            md=np.median(hist) or max(hist.mean(),1)
            lo=round(tot_med*np.percentile(hist,25)/md) if md else 0; hi=round(tot_med*np.percentile(hist,75)/md) if md else 0
            if lo>tot_med: lo=round(tot_med*.6)
            if hi<tot_med: hi=round(tot_med*1.4)
            rating=(card or {}).get('rating') or (cv or {}).get('rating') or 'n/a'
            l3y=round(pg(l3,3)+pg(l3,5),1); sy=round(sum(x[3]+x[5] for x in gl)/gp,1)
            trend='up' if l3y>sy*1.15 else ('down' if l3y<sy*.85 else 'flat')
            shr=ts_3 if pos!='RB' else max(cs_3,ts_3)
            vol_ok= shr>=(18 if pos=='WR' else 14 if pos=='TE' else 40) or (pos=='RB' and ts_3>=12)
            if vol_ok and trend!='down' and rating!='TOUGH': v='YES'
            elif not vol_ok and (trend=='down' or rating=='TOUGH'): v='NO'
            else: v='MIXED'
            why=f"{'carry' if pos=='RB' else 'target'} share L3 {shr}%, L3 {l3y} vs season {sy} yds/g ({trend}), matchup {rating}"
            dfl=(f"{cv['likely_defender']} ({cv['defender_depth']}): {cv['defender_line']} [{cv['defender_flag']}]" if cv else (f"RB coverage: {D} allows {d['rb_recyds_pg']} RB rec yds/g (#{d['rb_recyds_rank_most_allowed']} most)" if pos=='RB' else 'GAP: no inferred defender'))
            reasons=[]
            if not gate: reasons.append(f"tgt/g {tpg_s} szn/{tpg_3} L3" + (f", car/g {cpg_s}/{cpg_3}" if pos=='RB' else ''))
            players.append({'name':full,'pos':pos,'q':st if st=='Questionable' else '','gate':gate,'gate_why':'; '.join(reasons),
              'type':', '.join((pt or {}).get('user_labels') or [(pt or {}).get('primary') or 'GAP (no type label)']),
              'tpg':[tpg_3,tpg_s],'rpg':[pg(l3,2),round(rec/gp,1)],'cpg':[cpg_3,cpg_s],'ts':[ts_3,ts_s],'cs':[cs_3,cs_s],
              'log':' '.join(f"W{x[0]} {x[1]}-{x[2]}-{x[3]}"+(f"/{x[4]}c{x[5]}" if x[4] else '') for x in gl),
              'eff':f"catch {round(100*cr)}%, aDOT {adot}, {round(ry/rec,1) if rec else '-'} y/rec, {int(((q.complete_pass==1)&(q.yards_gained>=20)).sum())} 20+ catches"+(f", {round(ypc,2)} YPC" if pos=='RB' and len(r) else ''),
              'rz':f"RZ {rz_t} tgt / {rz_c} car",
              'habits':f"middle-of-field tgt {mid}% ({(cv or {}).get('inferred_alignment','alignment n/a')}); blitz hot-read 0-5 {b05 if b05 else '<top4'}% / 5-15 {b515 if b515 else '<top4'}%; 3rd-down tgts {third}; per-player pressure & man/zone splits GAP",
              'h2h':'; '.join(h2h(pid,O,D)),'def':dfl,'rating':rating,'verdict':v,'vwhy':why,
              'score':(card or {}).get('score'),
              'proj':{'tgt':round(pt_,1),'rec':round(prec,1),'recyds':round(pyd),'car':round(pc,1),'rushyds':round(pry),'tot':round(tot_med),'lo':lo,'hi':hi}})
        # keep: gate pass + forced top3 WR, top TE, top2 RB
        act=[p for p in players if 'proj' in p]
        def top(pos,n,k): return [p['name'] for p in sorted([x for x in act if x['pos']==pos],key=k,reverse=True)[:n]]
        force=set(top('WR',3,lambda x:x['tpg'][1]+x['tpg'][0]))|set(top('TE',1,lambda x:x['tpg'][1]))|set(top('RB',2,lambda x:x['cpg'][1]+x['tpg'][1]))
        keep=[p for p in act if p['gate'] or p['name'] in force]
        for p in keep:
            if not p['gate']: p['tag']='fails gate: '+p['gate_why']
        keep.sort(key=lambda p:-(p['score'] if p['score'] is not None else -99) if p['pos']!='RB' else 0)
        rk=[p for p in keep if p['pos']!='RB' and p['score'] is not None]; rk.sort(key=lambda p:-p['score'])
        rest=[p for p in keep if p not in rk]; rest.sort(key=lambda p:-p['proj']['tot'])
        keep=rk+rest
        best=next(s['rec']['best'] for s in FIN[gid]['sides'] if s['label'].startswith(O+' '))
        excluded=[f"{p['name']} ({p.get('out') or 'not on current roster'})" for p in players if 'proj' not in p and (p.get('out') or p.get('off_roster'))]
        # narrative
        tpw=[p for p in keep if p['pos']!='RB']; tw=sorted(tpw,key=lambda p:-p['ts'][0])[:3]; trb=sorted([p for p in keep if p['pos']=='RB'],key=lambda p:-p['cs'][0])[:2]
        fm=film(O); fmn=sorted(((k,len(v),max([y for y in v if y] or [0])) for k,v in fm.items() if any(key(k)==key(p['name']) for p in keep)),key=lambda x:-x[1])[:3]
        ss=[x for x in o.get('seesaw',[]) if 'strong' in x['label'].lower() or 'weak inverse' in x['label'].lower()]
        nar=(f"{O} is {'an' if lab=='underdog' else 'a'} {lab} ({'+' if spr>0 else ''}{spr}, implied {imp} pts vs {round(pts[O],1)} season avg). Projected {PL} offensive plays, {PA} pass / {RA_} run ({round(PR*100)}% pass vs {round(tpass[O]*100)}% season). "
             f"{D} allows {d['rb_ypc_allowed']} YPC to RBs and {d['pts_allowed_pg']} pts/g, blitzes {d.get('ftn_blitz_pct')}% ({d.get('3rd_blitz_pct')}% on 3rd down), weak run gap: {d['weak_dir']}; pass YPT by spot: {cov.get(O,{}).get('sharp_ypt') and ' / '.join(k+' '+str(v['ypt']) for k,v in cov[O]['sharp_ypt'].items())}. "
             f"Target tree L3: "+', '.join(f"{p['name']} {p['ts'][0]}%" for p in tw)+f"; backfield carry share L3: "+', '.join(f"{p['name']} {p['cs'][0]}%" for p in trb)+'. '
             f"QB vs blitz: {o.get('qb')} {o.get('qb_blitz',{}).get('ypa')} YPA, {o.get('qb_blitz',{}).get('sacks')} sacks; hot reads go to "+', '.join((o.get('blitz_tree_0_5') or [])[:2])+'. '
             +("Seesaw: "+'; '.join(f"{x['pair']} {x['label']} (n={x['n']})" for x in ss)+'. ' if ss else 'No meaningful receiver seesaw. ')
             +("Verified film plays (Wk1-6): "+', '.join(f"{k} {n} plays (long {y})" for k,n,y in fmn)+'.' if fmn else 'No verified film notes.'))
        G['teams'].append({'team':O,'opp':D,'script':lab,'plays':PL,'pa':PA,'ra':RA_,'imp':imp,'nar':nar,'best':best,'excluded':excluded,'players':keep})
    out['games'].append(G)
out['method']=("Model projection, simulation not run (100k engine is on the user's Mac); no prop lines compared yet. Team plays = season plays/g x (1+0.5*(implied total/season pts -1)), capped +/-8%; pass rate = season rate +/-3 pts by 10G script (+/-5 at 7+ pt spread). "
  "Player targets = pass att x (0.6 L3 + 0.4 season target share); carries = rush att x blended carry share. Receptions = targets x catch rate x defense catch-rate multiplier (0.92-1.08 vs league for that position); rec yds = targets x yds/target x defense yds/target multiplier (0.85-1.15); rush yds = carries x YPC x defense RB YPC multiplier (0.85-1.15). "
  "Low/high = median scaled by the player's own 25th/75th percentile game (rush+rec yds) Wks 1-7. Gate: WR/TE 3+ tgt/g season or L3; RB 5+ car/g or 2+ tgt/g. Top 3 WR, top TE, top 2 RB always shown, tagged if they fail.")
json.dump(out,open(W+'breakdown/full/full.json','w'))
for G in out['games']:
    for t in G['teams']:
        print(G['id'],t['team'],t['script'],t['pa'],t['ra'],len(t['players']),'|',', '.join(f"{p['name']}{'*' if p.get('tag') else ''} {p['proj']['tot']}" for p in t['players']),'| excl',t['excluded'])
