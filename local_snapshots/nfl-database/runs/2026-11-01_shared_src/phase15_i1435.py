"""Phase 15 (inactives + reprice) for 4 PM ET games (LAC@LAR 4:05, KC@DEN 4:25, NE@MIA 4:25), run 2026-11-01 14:41-15:05 ET.
Appends Phase 15 rows (append-only; concurrent BUG-WX weather edits left intact); refreshes injury stamps, odds stamps only if older than 14:35."""
import json,re
R='/workspace/nfl-database/runs'; S=R+'/2026-11-01_shared_src'; T='2026-11-01 15:01'
INJ='/workspace/nfl-database/week8/inactives/espn_inj_20261101_1501.json'
r6=json.load(open(S+'/rescore_v6_i1435.json'))
def P(k,r):
    v=r6[k]['sims']; return '/'.join(f"{v[m]['rungs'][r]:.2f}" for m in ('mc','bias','gr'))
INACTIVE={'Donte Jackson','Rodney Shelley','Deane Leonard','Kayode Awosika','Brenen Thompson','Theo Wease Jr.','Ty Simpson','Joe Cardona','Bill Murray','Keagen Trost','Colby Parkinson','Desjuan Johnson',
 'Talanoa Hufanga','Sam Ehlinger','Gavin Ortega','Kage Casey','Dallen Bentley','Jordan Jackson','Tyler Onyedim',
 'A.J. Brown','TreVeyon Henderson','Karon Prunty','Elliott Davison','Channing Canada','Behren Morton',
 'Kadyn Proctor','Justin Joly','Marcellas Dial Jr.','Jaylin Simpson','Christian Haynes','Jared Wayne','Jamree Kromah','Mansoor Delane','Omarr Norman-Lott'}
NOTE={
 'Kenneth Walker III':f"ACTIVE (ESPN 15:01 Active; no designation). Backfield: Emmett Johnson ACTIVE (18-36% snaps, 2-8 car wk1-7), Brashard Smith IR; Walker snaps 68-82%, carries 23/24/18/22/19/14 (wk7 low 14-36). Rice ACTIVE returning (hamstring): wk1-2 w/ Rice Walker had 6/10 tgts, wk3 2 -> mixed, mild target risk to rush+rec. DEN S Hufanga INACTIVE (helped); DEN DT Z. Allen + LT Bolles ACTIVE. Lines: FD rush 85.5 unch (Pinnacle O -112->-119), alt 69.5 -235->-240, 79.5 -148 unch, rush+rec 108.5 -113->-115; PP rush+rec 113.5->110.5. v6 (KC -1.5) P(rush 69.5) {P('Kenneth Walker III|rushyds','69.5')}, P(rush 97.5) {P('Kenneth Walker III|rushyds','97.5')}, P(rush+rec 79.5) {P('Kenneth Walker III|rushrec','79.5')}; median rush 95, rush+rec 119",
 'Puka Nacua':f"ACTIVE. HELPED: Phase 4 defender CB Donte Jackson INACTIVE; LAC also without CBs Shelley + Leonard (3 CBs down; McDuffie active). Lines: rec 7.5 -138 unch, yds 91.5 unch, alt 69.5 -280->-290, rush+rec 101.5->102.5. v6 (LAR -6.5) P(rec 7.5) {P('Puka Nacua|rec','7.5')}, P(yds 59.5) {P('Puka Nacua|recyds','59.5')}, P(yds 69.5) {P('Puka Nacua|recyds','69.5')}",
 'Matthew Stafford':"ACTIVE. Completions: Pinnacle O22.5 -124 unch; PP 22.5->23.0 (0.5, not material). LAC 3 CBs inactive helps volume/efficiency; LAR -6.5 lead risk caps attempts late. sim_v6 has no completions market (graded off Pinnacle no-vig + Phase 14 at 07:30)",
 'Patrick Mahomes':f"ACTIVE; Rice + Kelce active. Pass yds 220.5 unch. v6 P(0.5) {P('Patrick Mahomes|passyds','0.5')} (near lock), P(220.5) {P('Patrick Mahomes|passyds','220.5')}",
 'Kyren Williams':f"ACTIVE. FLAG: TD share with Blake Corum (Corum snaps 27%->28%->44% wk5-7; wk7 carries Corum 17 / Kyren 16). Lines: rec 3.5 +114->-102 (16c), rec yds 23.5->24.5, rush+rec 86.5->87.5 (not a ticket market). v6 P(rush 58.5) {P('Kyren Williams|rushyds','58.5')}",
}
TEAMS={'LAR','LAC','KC','DEN','NE','MIA'}
def who(name):
    for p in NOTE:
        if p.split()[0] in name and p.split()[-1].split()[0] in name: return p
    for p in INACTIVE:
        if p in name: return p
out={}
for g in ['KC@DEN','LAC@LAR','NE@MIA','DFS_SLIPS','FD7_REPLACEMENTS']:
    d=f'{R}/2026-11-01_{g}'; mp=d+'/run_manifest.json'; m=json.load(open(mp))
    rows=[]
    for l in m['legs']:
        tm=l.get('team','')
        if g in('DFS_SLIPS','FD7_REPLACEMENTS') and tm not in TEAMS: continue
        p=who(l['name']); st=l.get('status','PASS').upper()
        if p in INACTIVE and st=='PASS': st='CUT'; l['status']='CUT'; l.setdefault('cut_reasons',[]).append('P15 15:01 inactive')
        note=NOTE.get(p) if p in NOTE else (f"{p} INACTIVE" if p in INACTIVE else "ACTIVE (not on any team's official inactives / ESPN 15:01); no material line move (<0.5 / <20c) 11:35->14:35")
        if g=='NE@MIA': note+="; Phase 11 WEATHER FLAG NE@MIA (NWS PoP 53-69% t-storms, Open-Meteo gusts 20-22 mph, lightning-delay risk): all pass/rec overs pulled"
        rows.append(f"| {l['name']} | 15 Inactives | {st} | 15:01 ET: {note} | team inactives on X (@Patriots, @MikeReiss, @ParkerJGabriel, @ZacStevens, @Marcel_LJ, @chargers, @bynoahfurtado, @LATimesklein) + ESPN injuries API 15:01 + ESPN summaries 14:53 + The Odds API 14:42 (i1435) + sim_v6 100k x3 seed 20261101 | {T} |")
    hdr=(f"\n\n## Phase 15 re-check — inactives & reprice, 4 PM ET games (run 2026-11-01 14:41–15:05 ET)\nSupersedes earlier Phase 15 rows for the legs below. Read only; no bets placed. Re-sim: {S}/rescore_v6_i1435.json. "
         "KC official inactives tweet not yet posted at 15:01; ESPN 15:01 lists Walker, Rice, Mahomes, E. Johnson, Worthy, Kelce Active (Delane, Norman-Lott Out).\n\n| Leg | Phase | Status | Number | Source | Pulled (ET) |\n|-----|-------|------|--------|--------|-------------|\n")
    open(d+'/checklist.md','a').write(hdr+'\n'.join(rows)+'\n')
    for s in m['sources']:
        if s['category']=='odds_props' and s.get('pulled_et','')<'2026-11-01T14:35':
            s['pulled_et']='2026-11-01T14:42'; s['url_or_file']=S+('/lines_i1435.json' if 'spread' in s['name'] else '/odds_i1435.csv'); s['name']=re.sub(r'\(re-pull \d\d:\d\d\)','',s['name']).strip()+' (re-pull 14:35)'
        if s['category']=='injuries_news' and s['name']=='ESPN injuries API':
            s['pulled_et']='2026-11-01T15:01'; s['url_or_file']=INJ
    for s in m['sources']:
        if s['name'].startswith('X reporters'): s['pulled_et']='2026-11-01T15:01'
    if not any(s['name'].startswith('X reporters') for s in m['sources']):
        m['sources'].append(dict(category='injuries_news',name='X reporters/beat writers inactives posts via x connector',url_or_file='https://x.com/search (x connector search_posts_all)',pulled_et='2026-11-01T15:01',tool='x connector'))
    json.dump(m,open(mp,'w'),indent=1); out[g]=len(rows); print(g,len(rows),'rows')
