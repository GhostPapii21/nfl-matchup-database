import json,glob,re,pandas as pd,numpy as np
W='/workspace/nfl-database/week8';R=W+'/betguru_2026-11-01_raw';C=R+'/coverage_routes'
pb=pd.read_parquet('play_by_play_2026.parquet');pb=pb[pb.season_type=='REG']
sn=pd.read_parquet('snap_counts_2026.parquet');pl=pd.read_parquet('players.parquet')
ftn=pd.read_parquet(C+'/ftn_charting_2026.parquet')
ngp=pd.read_parquet('ngs_passing.parquet');ngp=ngp[(ngp.season==2026)&(ngp.week==0)]
ngr=pd.read_parquet('ngs_receiving.parquet');ngr=ngr[(ngr.season==2026)&(ngr.week==0)]
ngu=pd.read_parquet('ngs_rushing.parquet');ngu=ngu[(ngu.season==2026)&(ngu.week==0)]
pfr=pd.read_csv(C+'/pfr_def_adv_2026.csv');pfr=pfr[pfr.Player.notna()]
inj=json.load(open('espn_inj.json'))['injuries'];ol=json.load(open('espn_ol_depth.json'))
wrcb=open(C+'/espn_wrcb.txt').read().splitlines()
import io;sharp=pd.read_html(io.StringIO(open('sharp_cov_schemes.html').read()))[0]
TEAMN={'ARI':'Arizona Cardinals','ATL':'Atlanta Falcons','BAL':'Baltimore Ravens','BUF':'Buffalo Bills','CIN':'Cincinnati Bengals','CLE':'Cleveland Browns','DAL':'Dallas Cowboys','DEN':'Denver Broncos','DET':'Detroit Lions','IND':'Indianapolis Colts','JAX':'Jacksonville Jaguars','KC':'Kansas City Chiefs','LA':'Los Angeles Rams','LAC':'Los Angeles Chargers','LV':'Las Vegas Raiders','MIA':'Miami Dolphins','MIN':'Minnesota Vikings','NE':'New England Patriots','NYJ':'New York Jets','PHI':'Philadelphia Eagles','PIT':'Pittsburgh Steelers','SEA':'Seattle Seahawks','TB':'Tampa Bay Buccaneers','TEN':'Tennessee Titans','WAS':'Washington Commanders'}
# StatRankings man/zone (Oct 30 data, page updated 10/31) parsed from sentences
def srparse(f):
    t=re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',open(f).read())).replace('&amp;','&');out={}
    for nm,pct in re.findall(r"((?:the )?(?:[A-Z][a-z]+ ?){1,3}) (?:has the highest .*? at|leads .*? at|is \w+ at|\w+ at|(?:second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth) at|\d+\w\w at) (\d+\.\d)%",t):
        nm=nm.replace('the ','').strip()
        for ab,full in TEAMN.items():
            if nm and (full.endswith(nm) or full.startswith(nm) or nm in full) and ab not in out: out[ab]=float(pct);break
    return out
srz=srparse('sr_zone.html')
_o='CLE NYG IND DAL KC CIN DEN LA CHI HOU DET NYJ ATL PHI LAC LV BAL NO MIA TB SF NE JAX TEN BUF'.split()
_v=[55.8,51.3,49.6,46.5,43.9,42.7,42.7,41.9,39.4,37.7,37.6,37.5,35.9,34.6,34.6,34.3,32.7,32.5,32.4,32.3,31.9,31.7,29.1,27.8,26.3]
srm=dict(zip(_o,_v))
sharp['ab']=sharp.Team.map({v:k for k,v in TEAMN.items()})
sharp['man_rk']=sharp['Man Rate'].rank(ascending=False,method='min')
srm_rk={k:i+1 for i,k in enumerate(_o)}
def scheme(o):
    s=sharp[sharp.ab==o]
    if not len(s): return 'GAP'
    s=s.iloc[0];m=srm.get(o);rk=srm_rk.get(o)
    agree='' if m is None else (' — rank order AGREES (within 5 spots)' if abs(rk-s.man_rk)<=5 else f' — rank order DIFFERS (Sharp #{int(s.man_rk)} vs SR #{rk})')
    return f"Sharp (Updated Oct 27; page modified 2026-10-29 15:53 ET) man {s['Man Rate']}/zone {s['Zone Rate']}/MOFC {s['Middle Closed Rate']}/MOFO {s['Middle Open Rate']} (man rank #{int(s.man_rk)} of 32). StatRankings (thru Oct 30, upd 10/31): man {m if m is not None else 'not in top-25 list (bottom 7) '}% rank {rk or '26-32'}, zone {srz.get(o,'n/a')}%{agree if m else ' — both put it in the low-man group' if s.man_rk>=26 else ''}"
legs_alive={('DK Metcalf','recyds'),('Puka Nacua','rec'),('Puka Nacua','recyds'),('CeeDee Lamb','rec'),('Drake London','recyds'),('Amon-Ra St. Brown','rec'),('Justin Jefferson','recyds'),('Garrett Wilson','recyds'),('Tee Higgins','recyds'),('Parker Washington','recyds'),('Zay Flowers','recyds'),
 ('Brock Bowers','rec'),('Brock Bowers','recyds'),('Trey McBride','rec'),('Trey McBride','recyds'),('Dallas Goedert','rec'),('Tyler Warren','recyds'),
 ('Jahmyr Gibbs','rushyds'),('Aaron Jones','rushyds'),('Bijan Robinson','rushyds'),('Braelon Allen','rushyds'),('James Cook','rushyds'),('Javonte Williams','rushyds'),('Jonathan Taylor','rushyds'),('Kenneth Walker III','rushyds')}
PEND={'Brock Bowers':['Jamien Sherwood','Demario Davis','Dane Belton'],'Trey McBride':['Shemar James','DeMarvion Overshown','Caleb Downs'],'Dallas Goedert':['Frankie Luvu','Sonny Styles','Nick Cross'],'Tyler Warren':['Foyesade Oluokun','Ventrell Miller','Eric Murray']}
def norm(s): return re.sub(r'[^a-z]','',s.replace('.','').lower().replace(' sr','').replace(' jr','').replace(' iii','').replace(' ii',''))
def pfrline(n):
    a=pfr[pfr.Player.str.replace('*','').str.strip().isin([n,n.replace(' Jr.','')])]
    if not len(a): return f"{n}: no PFR row (GAP)"
    a=a.iloc[0];return f"{n} ({a.Pos}, {a.Team}, G{float(a.G):.0f}): {float(a['Pass Coverage_Tgt']):.0f}-{float(a['Pass Coverage_Cmp']):.0f}-{float(a['Pass Coverage_Yds']):.0f}, cmp {a['Pass Coverage_Cmp%']}%, YPT {a['Pass Coverage_Yds/Tgt']}, rat {a['Pass Coverage_Rat']}"
real=pb[pb.play_type.isin(['pass','run'])&(pb.two_point_attempt!=1)]
def qb(tm):
    d=real[(real.posteam==tm)&(real.qb_dropback==1)];att=d[(d.pass_attempt==1)&(d.sack!=1)]
    f=ftn.merge(d[['game_id','play_id','sack','yards_gained','complete_pass','pass_attempt']],left_on=['nflverse_game_id','nflverse_play_id'],right_on=['game_id','play_id'])
    bl=f[f.n_blitzers>0];nb=f[f.n_blitzers==0]
    q=d.passer_player_name.value_counts().index[0] if len(d) else '?'
    n=ngp[ngp.team_abbr==tm].sort_values('attempts',ascending=False)
    ttt=f"{n.iloc[0].player_display_name} TTT {n.iloc[0].avg_time_to_throw:.2f}s, CPOE {n.iloc[0].completion_percentage_above_expectation:+.1f}, intended air {n.iloc[0].avg_intended_air_yards:.1f}" if len(n) else 'NGS GAP'
    olinj=[f"{y['athlete']['displayName']} {y['athlete'].get('position',{}).get('abbreviation','')} {y['status']}" for x in inj if x['displayName']==TEAMN.get(tm) for y in x['injuries'] if y['athlete'].get('position',{}).get('abbreviation','') in ('OT','G','C','T','OL')]
    return (f"QB ({tm}; primary {q}): {len(d)} dropbacks, {len(att)} att, cmp {att.complete_pass.mean():.1%}, YPA {att.passing_yards.fillna(0).sum()/max(len(att),1):.2f}, EPA/db {d.epa.mean():+.3f}, sacks {int(d.sack.sum())} ({d.sack.mean():.1%}), scrambles {int(d.qb_scramble.sum())} [pbp]. vs blitz (FTN n_blitzers>0, n={len(bl)}): sack {bl.sack.mean():.1%}, yds/db {bl.yards_gained.mean():.2f}; no blitz (n={len(nb)}): sack {nb.sack.mean():.1%}, yds/db {nb.yards_gained.mean():.2f}. NGS: {ttt}. OL now: {', '.join(f'{k.upper()} {v}' for k,v in ol.get('LAR' if tm=='LA' else ('WSH' if tm=='WAS' else tm),{}).items())}; OL injuries: {'; '.join(olinj) or 'none listed'} [ESPN].")
rows=[];md=[]
for f in sorted(glob.glob(R+'/leg_*.json')):
    d=json.load(open(f));nm=d['player'];mk=d['market']
    if (nm,mk) not in legs_alive: continue
    tm=d['team'];o=d['opp'];c=pl[pl.display_name.map(norm)==norm(nm)]
    if len(c)>1 and (c.latest_team==tm).any(): c=c[c.latest_team==tm]
    gid=c.gsis_id.iloc[0];pfrid=c.pfr_id.iloc[0]
    T=real[real.posteam==tm];wks=sorted(T.week.unique());l3=wks[-3:]
    s=sn[(sn.team==tm)&(sn.pfr_player_id==pfrid)].set_index('week')
    act=[w for w in wks if w in s.index];l3=act[-3:]
    snapl3=s.loc[[w for w in l3 if w in s.index],'offense_pct'];snaps=s.offense_pct
    missed=[int(w) for w in wks if w not in s.index]
    tg=T[(T.pass_attempt==1)&(T.sack!=1)&T.receiver_player_id.notna()]
    me=tg[tg.receiver_player_id==gid];ru=T[T.play_type=='run'];mr=ru[ru.rusher_player_id==gid]
    def sh(a,b,w=None):
        if w is not None: a=a[a.week.isin(w)];b=b[b.week.isin(w)]
        return len(a)/max(len(b),1)
    L=[f"\n### {nm} ({tm} vs {o}) — {mk} · rung {d.get('rung')} @ {d.get('price')}"]
    L.append(f"- Window: declared baseline = all {len(wks)} {tm} games (wks {[int(x) for x in wks]}); L3 = player's last 3 ACTIVE games, wks {[int(x) for x in l3]} (inactive weeks excluded, not counted as zeros). Missed/absent: {missed or 'none'} (verified via snap file absence; injury reason not adjudicated).")
    L.append(f"- Participation: snap % season {snaps.mean():.0%}, L3 {snapl3.mean():.0%} (per wk {', '.join(f'{int(w)}:{v:.0%}' for w,v in snaps.items())}) [nflverse snap counts]. 60% snap gate: {'PASS' if snapl3.mean()>=0.6 else 'FAIL'}.")
    status=next((f"{y['status']} — {y.get('shortComment','')[:120]}" for x in inj for y in x['injuries'] if norm(y['athlete']['displayName'])==norm(nm)),'not on ESPN injury report')
    L.append(f"- Availability: {status} [ESPN injuries API 7:30 PM ET]")
    rec=mk in('rec','recyds')
    gate=[]
    if rec:
        line=next((l for l in wrcb if re.search(r'\s'+re.escape(nm.replace(' Jr.',''))+r'\s',l)),None)
        if line:
            p=re.split(r'\s{2,}',line.strip());L.append(f"- Alignment/routes (ESPN WR/CB sheet, season-to-date): align tag {p[2]}, LWR/slot/RWR {p[5].split()[-1]}/{p[6]}/{p[7]}; routes {p[8]}; targets/route {p[9]}; YPRR {p[10]}. Route participation per dropback: GAP (no free per-game routes; nflverse 2026 participation 404).")
        else: L.append("- Alignment/routes: GAP (not on ESPN WR/CB sheet; TE sheet 404). PENDING_FILM.")
        ng=ngr[ngr.player_gsis_id==gid]
        ngs=f"NGS: sep {ng.avg_separation.iloc[0]:.2f}, cushion {ng.avg_cushion.iloc[0]:.2f}, YAC {ng.avg_yac.iloc[0]:.2f} vs exp {ng.avg_expected_yac.iloc[0]:.2f}, share of team intended air yds {ng.percent_share_of_intended_air_yards.iloc[0]:.1f}%" if len(ng) else 'NGS receiving: not qualified (GAP)'
        cm=me[me.complete_pass==1]
        L.append(f"- Opportunity: targets {len(me)} (L3 {len(me[me.week.isin(l3)])}); target share (player tgt / team receiver tgt) season {sh(me,tg):.1%}, L3 {sh(me,tg,l3):.1%} — share of pass attempts is not used. Receptions {len(cm)} (L3 {len(cm[cm.week.isin(l3)])}). aDOT {me.air_yards.mean():.1f}; RZ tgt {int((me.yardline_100<=20).sum())}; 3rd-down tgt {int((me.down==3).sum())} ({(me.down==3).sum()/max((tg.down==3).sum(),1):.0%} of team 3rd-down tgt); 2-min (≤120s left in half) tgt {int((me.half_seconds_remaining<=120).sum())} [pbp].")
        L.append(f"- Conversion/efficiency/explosive: catch rate {len(cm)/max(len(me),1):.1%}; YPT {cm.receiving_yards.sum()/max(len(me),1):.2f}; YAC/rec {cm.yards_after_catch.mean():.1f}; 20+ yd catches {int((cm.receiving_yards>=20).sum())}; {ngs} [pbp, NGS].")
        sl=me.week.isin(l3);a=sh(me,tg,l3);b=sh(me,tg)
        role='volume/possession' if b>=0.24 and me.air_yards.mean()<10 else 'explosive/deep' if me.air_yards.mean()>=12 else 'secondary target' if b<0.18 else 'primary target'
        if (me.yardline_100<=20).sum()>=6: role+=' + red-zone option'
        L.append(f"- Archetype (supported by numbers above): {role}. Trend: L3 share {a:.1%} vs season {b:.1%} → {'stable/up' if a>=0.85*b else 'DOWN (role change check)'}.")
        if a<0.85*b: gate.append('target share down >15% L3')
        L.append(f"- Scheme: {scheme(o)}")
        L.append("- PFR: **PFR cache Oct 29 (fresh pull 403)**.")
        if nm in PEND: L.append("- 8A status: PENDING (Rico ruling on TE/slot→LB/S mapping). Candidate defenders (PFR cache Oct 29, fresh pull 403): "+' | '.join(pfrline(x) for x in PEND[nm])+(". DAL: Dee Winters OUT (calf) per ESPN injuries API; ESPN depth chart RILB next = Shemar James." if nm=='Trey McBride' else ''))
        else: L.append("- 8A status: PENDING_FILM (defender per Phase 2).")
    else:
        rb=ru[ru.rusher_player_id.map(dict(zip(pl.gsis_id,pl.position)))=='RB']
        ng=ngu[ngu.player_gsis_id==gid]
        ngs=f"NGS: RYOE/att {ng.rush_yards_over_expected_per_att.iloc[0]:+.2f}, 8+ box {ng.percent_attempts_gte_eight_defenders.iloc[0]:.1f}%, time to LOS {ng.avg_time_to_los.iloc[0]:.2f}s" if len(ng) else 'NGS rushing: not qualified (GAP)'
        a=sh(mr,rb,l3);b=sh(mr,rb)
        L.append(f"- Opportunity: carries {len(mr)} (L3 {len(mr[mr.week.isin(l3)])}); RB carry share season {b:.1%}, L3 {a:.1%}; GL carries (≤5) {int((mr.yardline_100<=5).sum())}; targets {len(me)}, catches {int(me.complete_pass.sum())}; receiving routes GAP [pbp].")
        L.append(f"- Efficiency/explosive: YPC {mr.rushing_yards.mean():.2f}; success {mr.success.mean():.1%}; ≤0 yds {(mr.rushing_yards<=0).mean():.1%}; 15+ runs {int((mr.rushing_yards>=15).sum())}; {ngs} [pbp, NGS].")
        L.append(f"- Run direction/gap (carry direction, not concept): {dict(mr.run_location.value_counts())} / {dict(mr.run_gap.value_counts())}. Concept: GAP.")
        role=('early-down' if (mr.down<=2).mean()>=0.75 else 'all-down')+(' + goal-line' if (mr.yardline_100<=5).sum()>=4 else '')+(' + receiving' if len(me)>=20 else '')
        L.append(f"- Archetype: {role} RB. Trend: L3 carry share {a:.1%} vs {b:.1%} → {'stable/up' if a>=0.85*b else 'DOWN'}.")
        if a<0.85*b: gate.append('carry share down >15% L3')
    L.append("- "+qb(tm))
    outs=[f"{y['athlete']['displayName']} ({y['athlete'].get('position',{}).get('abbreviation','')}, {y['status']})" for x in inj if x['displayName']==TEAMN.get(tm) for y in x['injuries'] if y['status'] in('Out','Doubtful','Questionable','Injured Reserve') and y['athlete'].get('position',{}).get('abbreviation','') in('WR','TE','RB')]
    L.append(f"- Teammate injuries / redistribution: {'; '.join(outs) or 'none (skill)'} [ESPN]. No automatic transfer assumed; redistribution evidence not verified → no boost applied.")
    if snapl3.mean()<0.6: gate.append(f'L3 snap {snapl3.mean():.0%} <60%')
    if missed and not any(w>max(missed) for w in act): gate.append(f'INJURY RETURN after missing wks {missed} — no post-return sample; role-regime unverified')
    if missed and any(w>max(missed) for w in act): L.append(f'- Injury return: back since wk {int(min(w for w in act if w>max(missed)))} ({sum(w>max(missed) for w in act)} active games post-return).')
    low=[int(w) for w,v in snaps.items() if v<0.4]
    if low: L.append(f"- Partial games (snap <40%, treated as in-game exit, not role change): wks {low}.")
    st='FAIL' if any('snap' in g or 'down' in g for g in gate) else ('GAP' if gate else 'PASS')
    if any('INJURY RETURN' in g for g in gate) and st=='FAIL': st='GAP'
    if nm in PEND and st=='PASS': st='PASS (8A PENDING)'
    L.insert(1,f"- **PHASE 3: {st}** — {'; '.join(gate) or 'role, participation and opportunity verified'}")
    md+=L;rows.append((nm,mk,o,st,'; '.join(gate) or '—'))
hdr=f"""# BetGuru — PHASE 3 (Offense, player type, opportunity) — Sun Nov 1, 2026
Script lines 302–408. Phases 4+ NOT run. src/phase3.py. Alive legs = Phase 2 PASS and 8A not GAP/FAIL (+ Bowers/McBride/Goedert/T. Warren held PENDING on LB/S mapping per parent). **DK Metcalf 40+ CUT** (8A FAIL on film; see Phase 2 addendum).
Sources: nflverse pbp/snap counts 2026 (Oct 31 7:17 PM ET); nflverse NGS passing/receiving/rushing season rows (https://github.com/nflverse/nflverse-data/releases/download/nextgen_stats/ngs_*.parquet); FTN charting (blitz); ESPN WR/CB sheet; ESPN injuries + depth charts (Oct 31 ~7:30 PM ET); PFR cache Oct 29 (fresh pull 403); Sharp coverage schemes (Updated Oct 27) + StatRankings man/zone coverage rate (thru Oct 30, upd 10/31) https://statrankings.com/nfl/advanced/teams/coverage/man-coverage-rate.
Gates: 60% L3 snap gate (user rule); target/carry share L3 not down >15% vs season; missing input = GAP.

|Player|Market|Opp|Phase 3|Gate notes|
|-|-|-|-|-|
"""+'\n'.join(f"|{a}|{b}|{c}|{s}|{g}|" for a,b,c,s,g in rows)+"\n"
open('../betguru_phase3.md','w').write(hdr+'\n'.join(md))
for r in rows: print(r)
print(srm,srz)
# --- hand edits re-applied (film reliability; Gibbs caution) ---
s=open('../betguru_phase3.md').read()
s=s.replace("**DK Metcalf 40+ CUT** (8A FAIL on film; see Phase 2 addendum)","**DK Metcalf 40+: ALIVE** (corrected chart INSUFFICIENT FILM; no shadow; mapped Tyson Campbell; film GAP disclosed)")
s=s.replace("|Jahmyr Gibbs|rushyds|MIN|PASS|—|","|Jahmyr Gibbs|rushyds|MIN|PASS — CAUTION (pbp/FTN)|MIN #1 vs edge runs, fewer light boxes; film UNVERIFIED|")
for k in['rec','recyds']: s=s.replace(f"|Trey McBride|{k}|DAL|PASS (8A PENDING)|—|",f"|Trey McBride|{k}|DAL|PASS (8A PENDING)|film UNVERIFIED; alignment GAP (disclosed)|")
s=s.replace("|DK Metcalf|recyds|CLE|PASS|","|DK Metcalf|recyds|CLE|PASS (alive; no shadow evidence, mapped T. Campbell; film GAP disclosed)|")
s=s.replace("- 8A status: PENDING_FILM (defender per Phase 2).","- 8A status: PENDING_FILM; film route/alignment read counts only if every cited play matches pbp, otherwise UNVERIFIED → GAP (disclosed).")
h=open('phase3_handedits.md').read().replace("- **Metcalf:** PENDING_FILM_RECHECK. His Phase 3 profile isn't in the table above (he was cut when it ran); it is in Phase 4.","- **Metcalf:** PENDING_FILM_RECHECK; Phase 3 profile is included above.")
open('../betguru_phase3.md','w').write(s+'\n\n'+h)
