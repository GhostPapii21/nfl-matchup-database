import json,glob,re,pandas as pd,numpy as np
W='/workspace/nfl-database/week8';R=W+'/betguru_2026-11-01_raw'
pb=pd.read_parquet('play_by_play_2026.parquet');pb=pb[(pb.season_type=='REG')&pb.play_type.isin(['pass','run'])&(pb.two_point_attempt!=1)]
sn=pd.read_parquet('snap_counts_2026.parquet');pl=pd.read_parquet('players.parquet')
inj=json.load(open('espn_inj.json'))['injuries']
TEAMN={'ARI':'Arizona Cardinals','ATL':'Atlanta Falcons','BAL':'Baltimore Ravens','BUF':'Buffalo Bills','CIN':'Cincinnati Bengals','CLE':'Cleveland Browns','DAL':'Dallas Cowboys','DEN':'Denver Broncos','DET':'Detroit Lions','IND':'Indianapolis Colts','JAX':'Jacksonville Jaguars','KC':'Kansas City Chiefs','LA':'Los Angeles Rams','LAC':'Los Angeles Chargers','LV':'Las Vegas Raiders','MIA':'Miami Dolphins','MIN':'Minnesota Vikings','NE':'New England Patriots','NYJ':'New York Jets','PHI':'Philadelphia Eagles','PIT':'Pittsburgh Steelers','SEA':'Seattle Seahawks','TB':'Tampa Bay Buccaneers','TEN':'Tennessee Titans','WAS':'Washington Commanders'}
p3=open('../betguru_phase3.md').read()
st3={(a,b):c for a,b,_,c in re.findall(r"^\|([^|]+)\|(rec|recyds|rushyds)\|([^|]+)\|([^|]+)\|",p3,re.M) for _ in [0]} if False else {}
for m in re.finditer(r"^\|([^|]+)\|(rec|recyds|rushyds)\|([^|]+)\|([^|]+)\|",p3,re.M): st3[(m[1],m[2])]=m[4]
def norm(s): return re.sub(r'[^a-z]','',s.replace(' Jr.','').replace(' III','').lower())
db=pb[pb.qb_dropback==1]
sackr=db.groupby('defteam').sack.mean();sackrk=sackr.rank(ascending=False).astype(int)
allow=db.groupby('posteam').sack.mean()
def injt(tm,pos=None,stat=('Out','Doubtful','Questionable','Injured Reserve')):
    return [(y['athlete']['displayName'],y['athlete'].get('position',{}).get('abbreviation',''),y['status']) for x in inj if x['displayName']==TEAMN.get(tm) for y in x['injuries'] if y['status'] in stat and (pos is None or y['athlete'].get('position',{}).get('abbreviation','') in pos)]
FILM={'DK Metcalf':'CORRECTED chart: INSUFFICIENT FILM; no shadow evidence; mapped Tyson Campbell (PFR cache Oct 29: CB CLE G4, 12-9-179, YPT 14.9, rat 116.7). Chart graphic "3 REC 65 YDS" vs pbp 5-115 (likely in-game graphic) — discrepancy logged.',
 'Tee Higgins':'chart UNVERIFIED: cites 2 TDs at BAL (pbp: 1 TD, 6-148, long 44) and 3 catches + drop at MIA (pbp: 2-22); clips carry video timestamps, not game clock → cannot match.',
 'Jahmyr Gibbs':'chart UNVERIFIED (5/11 plays match; fumble attribution wrong).','Trey McBride':'chart UNVERIFIED (2/6 match); alignment unclear.',
 'Puka Nacua':'summary UNVERIFIED (implausible 40-play count).','Brock Bowers':'summary UNVERIFIED (implausible 62-play count).','CeeDee Lamb':'summary UNVERIFIED (two 40-yd TDs at PHI vs actual 5-74).'}
legs=[];md=[];issues=[]
for f in sorted(glob.glob(R+'/leg_*.json')):
    d=json.load(open(f));nm=d['player'];mk=d['market']
    if (nm,mk) not in st3: continue
    tm,o=d['team'],d['opp'];sp=d.get('spread');tot=d.get('total')
    c=pl[pl.display_name.map(norm)==norm(nm)]
    if len(c)>1 and (c.latest_team==tm).any(): c=c[c.latest_team==tm]
    gid=c.gsis_id.iloc[0]
    T=pb[pb.posteam==tm];rec=mk!='rushyds'
    me=T[(T.receiver_player_id==gid)&(T.pass_attempt==1)&(T.sack!=1)] if rec else T[(T.rusher_player_id==gid)&(T.play_type=='run')]
    s=sn[(sn.team==tm)&(sn.pfr_player_id==c.pfr_id.iloc[0])];act=sorted(s.week)
    wk=me.groupby('week').size().reindex(act,fill_value=0)
    yv=(me.groupby('week').receiving_yards.sum() if rec else me.groupby('week').rushing_yards.sum()).reindex(act,fill_value=0)
    cv=wk.std()/wk.mean() if wk.mean() else np.nan
    F=[];E=[]
    # OL/rusher
    olq=injt(tm,('OT','G','C'));rk=sackrk.get(o)
    olflag=(rk is not None and rk<=8) or len([x for x in olq if x[2] in('Out','Doubtful')])>=1
    F.append(f"OL/rusher: {tm} OL on report {olq or 'none'}; {o} defense sack rate {sackr.get(o,np.nan):.1%} (rank {rk}/32); {tm} OL allows {allow.get(tm,np.nan):.1%} [pbp, ESPN] → {'FLAG' if olflag else 'ok'}")
    if olflag: E.append('Efficiency')
    # injuries
    me_inj=[x for x in injt(tm,None,('Out','Doubtful','Questionable')) if norm(x[0])==norm(nm)]
    mates=[x for x in injt(tm,('WR','TE','RB'),('Out','Doubtful','Questionable')) if norm(x[0])!=norm(nm)]
    F.append(f"Injuries/replacement: player {me_inj or d.get('status')}; skill teammates Out/Doubtful/Q {mates or 'none'} (IR excluded: already in baseline); redistribution unverified (no boost) → {'FLAG' if me_inj or mates else 'ok'}")
    if me_inj: E.append('Availability')
    # backup QB
    qbs=T[T.qb_dropback==1].groupby('week').passer_player_name.agg(lambda x:x.value_counts().index[0]);qi=injt(tm,('QB',))
    chg=qbs.nunique()>1
    F.append(f"Backup-QB: primary passer by week {qbs.to_dict()}; QBs on report {qi or 'none'} → {'FLAG (starter changed this season)' if chg or qi else 'ok'}")
    # game flow
    gf=''
    if sp is not None:
        if not rec and sp>=6: gf='FLAG: RB on a ≥6-pt underdog (negative script risk)'
        elif not rec and sp<=-7: gf='note: big favorite; positive script for rush volume'
        elif rec and sp<=-7: gf='FLAG: ≥7-pt favorite; second-half pass volume may drop'
        elif rec and sp>=6: gf='note: underdog; pass volume up, efficiency risk'
    if tot is not None and tot<=41: gf=(gf+'; ' if gf else '')+f'FLAG: low total {tot}'
    F.append(f"Game flow: spread {sp:+} total {tot} [ESPN scoreboard / leg file] → {gf or 'ok'}")
    if 'FLAG' in gf: E.append('Opportunity')
    # workload
    unst=cv>0.45 or (wk<0.5*wk.median()).any()
    F.append(f"Workload: weekly {'targets' if rec else 'carries'} {wk.to_dict()} (CV {cv:.2f}); weekly yds {yv.round(0).astype(int).to_dict()} → {'FLAG unstable' if unst else 'ok'}")
    if unst: E.append('Opportunity')
    # sources
    src=['PFR cache Oct 29 (fresh pull 403); PFR G≈5 lags pbp'] if rec else []
    if o in('DAL','JAX'): src.append(f'Sharp vs StatRankings man-rank DIFFERS for {o}')
    if nm in FILM: src.append('film: '+FILM[nm])
    F.append(f"Source discrepancies: {'; '.join(src) or 'none found'}")
    if src: E.append('Source quality')
    mech=[]
    if rec: mech.append('route participation per dropback GAP (2026 participation 404)')
    if 'Trey McBride' in nm or 'Bowers' in nm or 'Goedert' in nm or 'Warren' in nm: mech+=['TE alignment GAP','TE/slot→LB/S 8A mapping awaiting Rico ruling']
    if not rec: mech.append('run concept (OZ/IZ) not in free data; run_location/gap proxy only')
    F.append(f"Unsupported model mechanics: {'; '.join(mech)} → disclosed, no mechanic credited")
    E.append('Model capability')
    film8a=f"8A film read: {'UNVERIFIED → alignment/route item GAP (disclosed); counts only if every cited play matches nflverse pbp (qtr/clock, receiver, yds)' if rec else 'n/a (rushing)'}"
    nflag=sum('FLAG' in x for x in F)
    st=st3[(nm,mk)];ph4='GAP' if st.startswith('GAP') else ('CAUTION' if nflag>=2 or 'CAUTION' in st else 'PASS')
    md+= [f"\n### {nm} ({tm} vs {o}) — {mk} · rung {d.get('rung')} @ {d.get('price')}",f"- **PHASE 4: {ph4}** ({nflag} flags) · Phase 3: {st}",f"- Slip comparison: NOT_APPLICABLE (no slip supplied for this leg). Postgame screening: NOT_APPLICABLE (pregame)."]+['- '+x for x in F]+[f"- {film8a}",f"- Possible-error buckets: {', '.join(dict.fromkeys(E))}. No causation assigned (no box score)."]
    legs.append((nm,mk,o,st,ph4,nflag,'; '.join(x.split(':')[0] for x in F if 'FLAG' in x) or '—'))
SAME={'Jahmyr Gibbs':'Gibbs rec','Amon-Ra St. Brown':'St. Brown recyds','Drake London':'London rec','CeeDee Lamb':'Lamb recyds','Zay Flowers':'Flowers rec','James Cook':'Cook rushrec'}
hdr="""# BetGuru — PHASE 4 (Cross-reference and alerts) — Sun Nov 1, 2026
Script lines 409–444. Phases 5+ NOT run. src/phase4.py. Legs = every Phase 3 survivor, plus Metcalf 40+ (alive per corrected chart: INSUFFICIENT FILM, no shadow, mapped Tyson Campbell).
Sources: nflverse pbp/snaps 2026 (Oct 31 7:17 PM ET); ESPN injuries API (~7:30 PM ET); ESPN scoreboard odds Nov 1 (defense/espn_scoreboard_20261101.json); PFR cache Oct 29 (fresh pull 403); Phase 3 file.
**Slip comparison: NOT_APPLICABLE** — no slip supplied for comparison. **Postgame screening triggers (60+ rec yds, 100+ rush, 2+ TD, 5+ rec): NOT_APPLICABLE**; games not played. These are review triggers, not proof of value.
**8A film rule (all rows):** a film route/alignment read counts only if every cited catch/target matches an nflverse pbp play (quarter/clock, receiver, yards). Unmatched = UNVERIFIED → GAP, disclosed. All current charts (Metcalf, Gibbs, McBride, Puka, Bowers, Lamb, Higgins) are UNVERIFIED; A. Williams has no film (GAP).
Flag thresholds: opp sack-rate top 8 or OL starter Out/Doubtful; RB on a ≥6-pt dog / pass-catcher on a ≥7-pt favorite / total ≤41; weekly CV >0.45 or a week <50% of median.

|Player|Market|Opp|Phase 3|Phase 4|#Flags|Flags|
|-|-|-|-|-|-|-|
"""+'\n'.join(f"|{a}|{b}|{c}|{s}|{p}|{n}|{g}|" for a,b,c,s,p,n,g in legs)
corr="\n\n## Same-player correlation with placed Ticket 2 (barred markets, not re-bet)\n"+'\n'.join(f"- {k} live leg overlaps placed **{v}**. Exposure stacks on one player; disclose in sizing." for k,v in SAME.items() if any(l[0]==k for l in legs))
iss="""

## Stable issues (material data/model defects)
- **ISS-01 Film charts unreliable.** Evidence: Metcalf INTs were really Pittman/R. Wilson targets; Lamb 2×40-yd TDs vs actual 5-74; Gibbs 5/11 match; McBride 2/6; Higgins 2 TDs vs 1. Acceptance: every cited play joins to an nflverse play_id on qtr/clock ±15 s, receiver and yds ±3; otherwise UNVERIFIED.
- **ISS-02 PFR coverage cache stale (Oct 29; fresh pull 403; G≈5).** Acceptance: re-pull with G equal to games played, or label every row cache-dated.
- **ISS-03 Scheme source disagreement (Sharp vs StatRankings; DAL #12 vs #4, JAX #13 vs #23).** Acceptance: state both sources; no man/zone-based edge unless their ranks agree within 5.
- **ISS-04 No free route participation (nflverse 2026 participation 404).** Acceptance: participation file published, or routes stay GAP.
- **ISS-05 TE/slot→LB/S mapping unruled (Bowers, McBride, Goedert, Warren).** Acceptance: Rico ruling recorded; 8A re-run.
- **ISS-06 Run concept absent (OZ/IZ).** Acceptance: a verified concept source; until then run_location/run_gap proxy is labeled.
- **ISS-07 Metcalf chart graphic "3 REC 65 YDS" vs pbp 5-115.** Acceptance: treat the graphic as in-game, the pbp as final.

## Pending for later phases (noted, not run)
- Price and evaluate Gibbs 60+ rush (50+ fallback) and Lamb 5+ rec on their own edge (Phase 7+).
- 10G end: side-by-side vs Ghost6's card (~+735: Flournoy 3+ rec, Tuten 60+ rush, Metcalf 40+, Puka 70+, A. Williams 3+ rec, Gibbs 60+ rush), with sims, edge vs no-vig, and where we disagree and why.
"""
open('../betguru_phase4.md','w').write(hdr+corr+iss+'\n'.join(md))
for l in legs: print(l)
