import json,glob,re,pandas as pd,numpy as np
W='/workspace/nfl-database/week8';R=W+'/betguru_2026-11-01_raw';C=R+'/coverage_routes'
pb=pd.read_parquet('play_by_play_2026.parquet');pb=pb[pb.season_type=='REG']
pl=pd.read_parquet('players.parquet')[['gsis_id','position']].drop_duplicates('gsis_id')
pos=dict(zip(pl.gsis_id,pl.position))
ftn=pd.read_parquet(C+'/ftn_charting_2026.parquet')
pfr=pd.read_csv(C+'/pfr_def_adv_2026.csv');pfr=pfr[pfr.Player.notna()&(pfr.Player!='Player')]
for c in pfr.columns[5:-1]: pfr[c]=pd.to_numeric(pfr[c],errors='coerce')
inj=json.load(open('espn_inj.json'))['injuries']
NAME={'LA':'Los Angeles Rams','LAC':'Los Angeles Chargers'}
espn_ab={'LA':'LAR','CLE':'CLV','ARI':'ARZ','BAL':'BLT'}
wrcb=open(C+'/espn_wrcb.txt').read().splitlines()
# scheme from Sharp (via defense/*.md)
scheme={}
for f in glob.glob(W+'/defense/*_at_*.md'):
    cur=None
    for l in open(f):
        m=re.match(r'## (\w+) DEFENSE',l)
        if m:cur=m.group(1)
        if cur and l.startswith('| Man / Zone'): scheme[cur]=l.split('|')[2].strip()
        if cur and l.startswith('| Sharp YPT Outside'): scheme[cur+'_os']=l.split('|')[2].strip()+' (rank '+l.split('|')[3].strip()+')'
# phase1 passes
p1=open('../betguru_phase1.md').read()
legs=[]
for f in sorted(glob.glob(R+'/leg_*.json')):
    d=json.load(open(f));
    m=re.search(r'\|'+re.escape(d['player'])+r'\|'+d['market']+r'\|[^|]*\|[^|]*\|(\w+)\|',p1)
    st=m.group(1) if m else 'NEW(no P1)'
    if st=='PASS': legs.append(d)
real=pb[pb.play_type.isin(['pass','run'])&(pb.two_point_attempt!=1)]
def prof(t):
    g=pb[pb.defteam==t];gids=sorted(g.game_id.unique());n=len(gids)
    pts=sum(int(pb[pb.game_id==x].iloc[-1].total_away_score if pb[pb.game_id==x].iloc[0].home_team==t else pb[pb.game_id==x].iloc[-1].total_home_score) for x in gids)
    r=real[real.defteam==t];ps=r[r.pass_attempt==1];ru=r[(r.play_type=='run')]
    gross=ps.passing_yards.fillna(0).sum();sky=-ps[ps.sack==1].yards_gained.sum();net=gross-sky
    sacks=int(ps.sack.sum());hits=int(ps.qb_hit.sum())
    wk=sorted(g.week.unique());l3=r[r.week.isin(wk[-3:])&(r.pass_attempt==1)]
    pr=pfr[pfr.Team==t];prss=pr['Pass Rush_Prss'].sum();bl=pr['Pass Rush_Bltz'].sum()
    fj=ftn.merge(ps[['game_id','play_id']],left_on=['nflverse_game_id','nflverse_play_id'],right_on=['game_id','play_id'])
    blitz=(fj.n_blitzers>0).mean() if len(fj) else np.nan
    tg=ps[ps.receiver_player_id.notna()&(ps.sack!=1)].copy();tg['P']=tg.receiver_player_id.map(pos)
    out=[f"\n## {t} DEFENSE — window: 2026 REG wks {wk[0]}–{wk[-1]}, {n} games ({', '.join(gids)})",
     f"- Points allowed: {pts} ({pts/n:.1f}/g). Pass yds allowed: gross {int(gross)} ({gross/n:.1f}/g); net of sack yds {int(net)} ({net/n:.1f}/g; {sacks} sacks for {int(sky)}). Rush yds allowed (all runs incl. QB, excl. kneels? kneels incl.) {int(ru.rushing_yards.fillna(0).sum())} ({ru.rushing_yards.fillna(0).sum()/n:.1f}/g). [nflverse pbp]",
     f"- Sacks {sacks}, QB hits {hits} [pbp]; pressures {int(prss)} (sum of PFR player Prss), PFR player blitzes {int(bl)} [PFR cache Oct 29]; FTN blitz rate {blitz:.1%} of {len(fj)} charted dropbacks (n_blitzers>0) [FTN parquet].",
     f"- Last-3 trend (wks {[int(x) for x in wk[-3:]]}): sacks+hits per dropback {((l3.sack==1)|(l3.qb_hit==1)).mean():.1%} vs season {((ps.sack==1)|(ps.qb_hit==1)).mean():.1%} [pbp; true per-game pressure not free → proxy]",
     "\n|Pos|Tgt|Rec|Yds|Tgt/g|Rec/g|Yds/g|YPT|YAC/cmp|Explosive (≥20)|Expl yds|\n|-|-|-|-|-|-|-|-|-|-|-|"]
    for P in ['WR','TE','RB']:
        x=tg[tg.P==P];c=x[x.complete_pass==1];e=c[c.receiving_yards>=20]
        out.append(f"|{P}|{len(x)}|{len(c)}|{int(c.receiving_yards.sum())}|{len(x)/n:.1f}|{len(c)/n:.1f}|{c.receiving_yards.sum()/n:.1f}|{c.receiving_yards.sum()/max(len(x),1):.2f}|{c.yards_after_catch.mean():.1f}|{len(e)}|{int(e.receiving_yards.sum())}|")
    rb=ru[ru.rusher_player_id.map(pos)=='RB'];ex=rb[rb.rushing_yards>=15]
    out.append(f"- Receiving explosives (all): {int((tg.receiving_yards>=20).sum())}; mean air depth of targets {tg.air_yards.mean():.1f}. [pbp]")
    out.append(f"- RB run defense: {len(rb)} car ({len(rb)/n:.1f}/g), {int(rb.rushing_yards.sum())} yds, YPC {rb.rushing_yards.mean():.2f}, success {rb.success.mean():.1%}, ≤0 yds {(rb.rushing_yards<=0).mean():.1%} (stuff proxy), negative {(rb.rushing_yards<0).mean():.1%}, explosive ≥15: {len(ex)} for {int(ex.rushing_yards.sum())} yds. Direction L/M/R carries: {dict(rb.run_location.value_counts())}. 1H/2H YPC {rb[rb.qtr<=2].rushing_yards.mean():.2f}/{rb[rb.qtr>=3].rushing_yards.mean():.2f}; leading/trailing (def persp.) YPC {rb[rb.score_differential<0].rushing_yards.mean():.2f}/{rb[rb.score_differential>0].rushing_yards.mean():.2f}. Gap/concept: GAP (direction ≠ concept). [pbp]")
    fr=ftn.merge(rb[['game_id','play_id']],left_on=['nflverse_game_id','nflverse_play_id'],right_on=['game_id','play_id'])
    out.append(f"- Box count on RB carries (FTN): mean {fr.n_defense_box.mean():.1f}, 8+ box {(fr.n_defense_box>=8).mean():.1%} (n={len(fr)}). Personnel/front: GAP (2026 nflverse participation not published — 404).")
    out.append(f"- Coverage (Sharp Football Analysis, via week8/defense/*.md, page dated 2026-10-20): Man/Zone/MOFC/MOFO % {scheme.get(t,'GAP')}; Outside/Slot YPT {scheme.get(t+'_os','GAP')}. FTN free parquet has NO man/zone/MOF columns; nflverse 2026 participation (defense_man_zone_type) not published → FTN/nflverse scheme = GAP; Sharp is the only scheme source. Press/off: GAP.")
    out.append("\n|Defender|Pos|G/GS|Tgt|Cmp|Cmp%|Yds|YPT|TD|INT|Rat|YAC|Prss|Sk|MTkl%|\n|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|")
    for grp in [['CB'],['S','FS','SS','DB'],['LB','ILB','OLB','MLB']]:
        for _,a in pr[pr.Pos.isin(grp)].sort_values('Pass Coverage_Tgt',ascending=False).head(3 if grp==['CB'] else 2).iterrows():
            out.append(f"|{a.Player}|{a.Pos}|{a.G:.0f}/{a.GS:.0f}|{a['Pass Coverage_Tgt']:.0f}|{a['Pass Coverage_Cmp']:.0f}|{a['Pass Coverage_Cmp%']}|{a['Pass Coverage_Yds']:.0f}|{a['Pass Coverage_Yds/Tgt']}|{a['Pass Coverage_TD']:.0f}|{a['Pass Coverage_Int']:.0f}|{a['Pass Coverage_Rat']}|{a['Pass Coverage_YAC']}|{a['Pass Rush_Prss']}|{a['Pass Rush_Sk']}|{a['Tackles_MTkl%']}|")
    out.append("(PFR advanced defense, cached 2026-10-29 06:02 ET; tackler ≠ coverage defender. PBUs not in this table → GAP.)")
    tn=[x for x in inj if x['displayName'].split()[-1] in NAME.get(t,'') or x.get('displayName','').startswith(NAME.get(t,'@@'))]
    team_inj=[x for x in inj if any(t==y.get('athlete',{}).get('team',{}).get('abbreviation') for y in x['injuries'][:1])] or tn
    L=[]
    for x in team_inj:
        for y in x['injuries']:
            p=y['athlete'].get('position',{}).get('abbreviation','')
            if p in('CB','S','FS','SS','DB','LB','ILB','OLB','DE','DT','NT','DL','EDGE'):L.append(f"{y['athlete']['displayName']} {p} — {y['status']}")
    out.append(f"- Defensive injuries (ESPN injuries API, pulled 2026-10-31 ~7:30 PM ET): {'; '.join(L) or 'none listed / GAP if team not matched'}")
    return '\n'.join(out),scheme.get(t)
teams=sorted({d['opp'] for d in legs});P={};S={}
for t in teams: P[t],S[t]=prof(t)
# 8A
rows=[];det=[]
for d in legs:
    rec=d['market'] in('rec','recyds','rushrec') and not (d['market']=='rushrec' and d['pos']=='RB' and False)
    nm=d['player'];o=d['opp']
    if d['market']=='rushyds': rows.append((nm,d['market'],o,'PASS','N/A (rushing leg)','')) ;continue
    line=next((l for l in wrcb if re.search(r'\s'+re.escape(nm.replace(' Jr.',''))+r'\s',l)),None)
    pfrok=False;mp=''
    if line:
        pt=re.split(r'\s{2,}',line.strip());k=13
        if pt[k].endswith('%'):k+=1
        cb,side=pt[k],pt[k+1];al=' '.join(pt[k+4:])[:20]
        a=pfr[pfr.Player.fillna('').str.replace('*','').str.strip().isin([cb,cb.replace(' Jr.','')])]
        if len(a):
            a=a.iloc[0];pfrok=bool(a['Pass Coverage_Tgt']>0)
            mp=f"{cb} ({side}; ESPN CB align cols {al.split()[0:3]}): PFR {a['Pass Coverage_Tgt']:.0f}-{a['Pass Coverage_Cmp']:.0f}-{a['Pass Coverage_Yds']:.0f}, cmp {a['Pass Coverage_Cmp%']}%, YPT {a['Pass Coverage_Yds/Tgt']}, rat {a['Pass Coverage_Rat']}" + (' — THIN (0 tgt)' if a['Pass Coverage_Tgt']==0 else '')
        else: mp=f"{cb} mapped (ESPN) but no PFR row → GAP"
    elif d['pos'] in('TE','RB'):
        mp='no free TE/RB→defender alignment map (ESPN TE sheet 404; 2026 participation 404)'
    else: mp='player not on ESPN WR/CB sheet'
    sch=S.get(o)
    v8='PENDING_FILM' if (pfrok and sch) else 'GAP'
    why='defender+PFR+scheme collected; routes/alignment film PENDING_FILM' if v8=='PENDING_FILM' else 'missing: '+(', '.join([x for x,ok in (('PFR mapped defender',pfrok),('scheme',bool(sch))) if not ok]))
    rows.append((nm,d['market'],o,'PASS' if sch else 'GAP',v8+' — '+why,mp))
hdr=f"""# BetGuru — PHASE 2 (Build both defensive profiles) + 8A defender check — Sun Nov 1, 2026
Script: GAME_SCRIPT_2026-10-29.md lines 208–301; 8A = nfl-betting-script §8A / PHASE_SCRIPT.md step 2A. Phase 3+ NOT run. Generated by src/phase2.py.

## Sources
- nflverse pbp 2026 (fresh 2026-10-31 7:17 PM ET) https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet
- FTN charting (nflverse) https://github.com/nflverse/nflverse-data/releases/download/ftn_charting/ftn_charting_2026.parquet — blitzers, box. **Has no man/zone or MOF fields.**
- nflverse pbp_participation_2026: **404 (not published)**; the cached copy in coverage_routes/ is not a valid parquet.
- PFR advanced defense https://www.pro-football-reference.com/years/2026/defense_advanced.htm — **fresh pull 403 at ~7:26 PM ET; using cache from 2026-10-29 06:02 ET** (coverage_routes/pfr_def_adv_2026.csv). PFR cache G column shows ≤5 games for most players (cache predates the latest weeks), so PFR defender numbers lag the pbp window — flagged per table.
- Sharp Football Analysis coverage schemes (page 2026-10-20) via week8/defense/*.md — man/zone/MOF.
- ESPN WR/CB cheat sheet https://g.espncdn.com/s/ffldraftkit/26/NFL26_CS_WRCB.pdf — WR→CB mapping & alignment.
- ESPN injuries API https://site.api.espn.com/apis/site/v2/sports/football/nfl/injuries (pulled 7:30 PM ET).

## Metcalf "1-for-15 on 7 targets vs Ward" — VERDICT: UNVERIFIED, DROPPED
- Origin: coverage_routes/defender_route_audit.md cites Fantasy Points' Week 8 WR/CB article (https://www.fantasypoints.com/nfl/articles/2026/week-8-wr-cb-fantasy-football-matchups) — a third-party charted (likely paid-charting-derived) matchup stat, never checked against a free source. Game set/season not stated.
- Free-source check of the last two Metcalf-vs-CLE meetings (nflverse pbp): **2025 Wk6 2025_06_CLE_PIT: 9 tgt, 4 rec, 95 yds; 2026 Wk4 vs CLE: 9 tgt, 5 rec, 115 yds** (2025 Wk18 he was suspended). Neither nflverse pbp nor PFR assigns a coverage defender per target, so "targets with Ward as the defender" cannot be verified from any allowed source. The claim is removed from the card.
- Rebuilt read: Metcalf vs CLE 2026 Wk4 = 5-115 on 9 targets (pbp). ESPN sheet maps him to Tyson Campbell (RCB 95%), not Ward. PFR (cache): Campbell 12-9-179, rat 116.7; Ward 25-10-142, rat 82.0. Ward shadow = unproven; film check pending. Metcalf no longer fails 8A on the Ward shadow; he is PENDING_FILM like the others.

## Leg table
|Player|Market|Opp D|Phase 2|8A|Mapped defender (PFR)|
|-|-|-|-|-|-|
"""+'\n'.join(f"|{a}|{b}|{c}|{s}|{v}|{m}|" for a,b,c,s,v,m in rows)+"\n\nPhase 2 PASS = full defensive profile built from cited sources (scheme from Sharp; FTN/nflverse scheme fields are GAP for every team). 8A cannot be PASS until film routes/alignment land.\n\n# Defensive profiles\n"
open('../betguru_phase2.md','w').write(hdr+'\n'.join(P[t] for t in teams))
for r in rows: print(r[:5])
