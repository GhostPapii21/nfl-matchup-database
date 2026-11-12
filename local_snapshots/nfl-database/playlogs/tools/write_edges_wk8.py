import json,csv,os,collections,re
B='/workspace/nfl-database'; PL=B+'/playlogs'; W=PL+'/2026_wk8'
E=json.load(open(W+'/_edges_raw.json')); S=json.load(open(W+'/_explosive_summary.json'))
prof=json.load(open(B+'/week8/defense/defense_profiles.json'))['teams']
SHELL={'TB':'17 man/78 zone, MOFC 59','ATL':'22/70, MOFC 60','PIT':'13/82, MOFO 52 (two-high zone)','CLE':'42 man/54, MOFC 73 (single-high man)','JAX':'21/73, MOFO 51','IND':'26/67, MOFC 50','NYJ':'24/67, MOFO 50','LV':'21/70, MOFC/MOFO 47/47','DET':'18/76, MOFO 49','MIN':'5 man/87 zone, MOFO 61, blitz 71%'}
# archetype corrections from pregame alignment (slot proxy) / film knowledge in week8 player_types
FIX={'Amon-Ra St. Brown':'WR-slot separator','Keenan Allen':'WR-slot separator','Josh Downs':'WR-slot separator','Parker Washington':'WR-slot separator','Jalen Nailor':'WR-deep speed','Jameson Williams':'WR-deep speed','Adonai Mitchell':'WR-deep speed','Isaiah Williams':'WR-slot separator','Dylan Sampson':'RB-receiving/scat','Kenny Gainwell':'RB-receiving/scat (used as volume back in rain)','Darnell Washington':'TE-inline (YAC big body)','Bucky Irving':'RB-home-run zone runner','Braelon Allen':'RB-power/volume early-down','Bhayshul Tuten':'RB-home-run zone runner','Brian Thomas Jr.':'WR-deep speed','Garrett Wilson':'WR-X outside volume','Penix':''}
WHY={
'Bucky Irving':'Rain (5.7mm) + TB lead → 56 rushes/3 passes; ATL run D 4.09 YPC, missed fits by Bates/Daniels/Henderson on 4 explosives (46y Henderson). Game-script RB rule spot.',
'Kenny Gainwell':'RB2 volume in rain run-fest (25 car); ATL edge contain failed (left/right end 28y, 20y). RB2 should be modeled when weather-flagged.',
'Jahan Dotson':'One 76y deep left shot vs TB zone (MOFC 59) — pregame matchup McCollum (outside right, inferred), Winfield tackled. Deep-speed WR vs single-high zone in garbage time.',
'Jaylen Warren':'PIT favored, CLE run D 4.61 YPC; 51y up the middle (Schwesinger tackled) vs CLE single-high man front; clock-kill second half.',
'Harold Fannin Jr.':'Trailing-script volume (Watson 39 att); PIT two-high zone (MOFO 52) leaves seams/underneath; pregame TE matchup S Spears-Jennings (inferred) — 10/12 for 154.',
'Darnell Washington':'Big-body inline TE YAC vs CLE man (42%) — 94y on 3 catches incl. 58y; coverage defender unknown.',
'Deshaun Watson':'Trailing all game → 324y garbage volume vs PIT soft-zone; losing-QB-in-blowout pattern.',
'Dylan Sampson':'Check-down valve vs PIT zone while trailing (6/8).',
'Bhayshul Tuten':'JAX -10 favorite, IND run D 4.49/RB rec YPT 7.7 (soft vs RB receiving); 104 rush + 55 rec, 2 TD.',
'Trevor Lawrence':'10/14 210y 3TD — efficiency, not volume; IND zone (MOFC 50) beaten deep (46y, inferred Haulcy).',
'Keenan Allen':'Trailing IND slot volume (7/7) vs JAX middle-of-field zone (JAX WR-mid YPT 15.7 season — softest area).',
'Brock Bowers':'TE-primary vs NYJ zone (67%), 2 TD; DPI declined on J.Brownlee on TD — NYJ LB/S seam coverage weak. TE YPT allowed 7.3.',
'Braelon Allen':'Backup promoted (Hall out) vs LV run D 5.17 YPC (worst-tier); 147 on 7.0 YPC, 5 run explosives.',
'Adonai Mitchell':'Deep shots vs LV boundary CB Darien Porter (pregame outside-left, inferred; 3 explosives incl. 47y) in shootout; LV WR-outside YPT 8.7.',
'Garrett Wilson':'Target volume (12) in shootout vs LV zone; pregame CB Eric Stokes (inferred).',
'Geno Smith':'Shootout (38-33) vs LV zone; 290y 2TD.',
'Kirk Cousins':'Efficient vs NYJ zone; 3 TD went to TE/slot (Bowers, Nailor).',
'Ashton Jeanty':'Receiving role (3/4, 64y incl. 23/27y vs Ponds-area, inferred) though only 2 carries.',
'Jalen Nailor':'Red-zone TD vs NYJ zone.',
'Jahmyr Gibbs':'DET run-heavy (39 rushes; Goff sacked 4); MIN zone 87%/MOFO 61 + 71% blitz = light boxes; 6 run explosives, 153y. Rushing was the edge, not receiving.',
'Sione Vaki':'RB2 in DET run script (11-65).',
'Jameson Williams':'Deep speed vs MIN two-high zone when blitz left 1-on-1; 70y TD.',
'Amon-Ra St. Brown':'Slot volume (7/8) but capped 46y — MIN soft-middle zone gave catches, not yards.',
'T.J. Hockenson':'Seam TE vs DET (TE YPT 8.2 allowed, top-tier soft); pregame matchup S Izien (inferred) 22y.',
'Jordan Addison':'51y vs D.J. Reed (inferred, outside-left).',
'Kyler Murray':'Scrambler 4-35 rush + 2 TD vs DET zone.',
'Justin Jefferson':'TD only; 33y — DET bracket/zone capped yards.'}
def defl(e):
  # defenders beaten: inferred from explosives table
  rows=[l for l in open(PL+'/explosives_allowed.md') if l.startswith('| 2026')]
  last=e['name'].split()[-1] if not e['name'].endswith(('Jr.','Sr.')) else e['name'].split()[-2]
  out=[]
  for l in rows:
    c=[x.strip() for x in l.strip().strip('|').split('|')]
    if c[3]==e['team'] and re.search(r'\b[A-Z][a-z]?\.'+re.escape(last)+r'\b',c[8]): out.append(f"{c[6]}y {c[5]} — {c[9] or '?'} [{c[10].split(' (')[0]}]")
  return out
score=lambda e: e['td']*20+len(e['ex'])*8+sum(int(x) for x in [e['ru'].get('YDS',0) or 0,e['re'].get('YDS',0) or 0])+ (int(e['pa'].get('YDS',0))//5 if e['pa'] else 0) - (60 if e['pa'] and int(e['pa'].get('INT',0))>=3 else 0)
E=[e for e in E if not (e['pa'] and int(e['pa'].get('INT',0))>=3)]
for e in E:
  e['arch']=FIX.get(e['name'],e['arch']); e['why']=WHY.get(e['name'],'Script/volume; no specific matchup attribution — see explosives table.'); e['beaten']=defl(e)
E.sort(key=score,reverse=True)
TAX='''## Archetype taxonomy (consistent labels used in CSV)
- **WR-X outside volume**: boundary WR1, high target share, intermediate aDOT (London, Wilson, Jefferson).
- **WR-slot separator**: inside alignment (ESPN slot% / middle-target proxy ≥50%), short aDOT, catch volume (St. Brown, K. Allen, Downs).
- **WR-deep speed**: aDOT 14+, 20+air% high, boom/bust (Dotson, Jam. Williams, A. Mitchell).
- **WR-YAC/screen**, **WR-contested-catch big**, **WR-rotational depth** (<10% tgt).
- **TE-move/seam**: TE-as-primary, detached/seam usage (Bowers, Fannin, Hockenson, Pitts).
- **TE-inline**: in-line/blocking TE with occasional chunk (D. Washington, Boerkircher).
- **RB-power/volume early-down**: lead back, carries > targets (Irving-type volume, B. Allen, Taylor).
- **RB-home-run zone runner**: elite RYOE/explosive-run rate (Gibbs, Warren, Tuten, Irving).
- **RB-receiving/scat**: target-heavy back (Sampson, Gainwell normally).
- **RB-committee/change-of-pace**.
- **QB-pocket / QB-scrambler / QB-checkdown game-manager**.
Defender labels: **press/man boundary CB beaten deep**, **zone safety late on seam**, **nickel vs big slot**, **run-fit: edge contain lost / interior fit missed (tackler of record)**.
Labels come from week8/player_types/*.md (data thru Wk7) mapped to the taxonomy, corrected with ESPN alignment data in week8/breakdown/coverage.
'''
with open(W+'/EDGE_PLAYERS_1PM.md','w') as f:
  f.write('# Week 8 1 PM edge players (2026-11-01)\n\nEdge = TD, explosive play, beat a pregame standard line (PrizePicks/FanDuel 10/30 pull, where one existed), or ≥70 rush/rec yds, ≥6 rec, ≥250 pass yds. Games: '+', '.join(sorted({e['game'] for e in E}))+'.\n\n'+TAX+'\n')
  f.write('## Edge players (ranked by impact)\n| # | Game | Player | Team vs Def | Archetype | Line | Beat line | Explosives (defender, confidence) | Why the edge |\n|---|---|---|---|---|---|---|---|---|\n')
  for i,e in enumerate(E,1):
    f.write(f"| {i} | {e['game']} | {e['name']} | {e['team']} vs {e['opp']} ({SHELL.get(e['opp'],'')}) | {e['arch']} | {e['line']} | {'; '.join(e['beats']) or '—'} | {'<br>'.join(e['beaten']) or '—'} | {e['why']} |\n")
  f.write('\n## Defensive vulnerability profiles (this week + season)\n')
  vt=collections.defaultdict(list)
  for e in E: vt[e['opp']].append(f"{e['name']} ({e['arch']})")
  for d in sorted(vt):
    p=prof[d]; pe=S['per_def']
    k=[v for kk,v in pe.items() if kk.endswith('|'+d)][0]
    f.write(f"### {d} defense — shell {SHELL.get(d,'?')}\n- Week 8 explosives allowed: {k[0]} pass 20+, {k[1]} rush 10+ ({k[2]} yds)\n- Beaten by: {', '.join(vt[d])}\n- Season (thru Wk7): RB YPC {p['RB_rush']['ypc']:.2f}, RB rec YPT {p['RB']['ypt']:.1f}, TE YPT {p['TE']['ypt']:.1f}, WR outside YPT {p['WR_outside_proxy']['ypt']:.1f}, WR middle YPT {p['WR_middle_proxy']['ypt']:.1f}, FTN blitz {p['ftn_blitz_rate']:.0f}%\n\n")
# CSV append-only
fn=PL+'/archetype_vs_defense_2026.csv'; new=not os.path.exists(fn)
seen=set()
if not new:
  for r in csv.DictReader(open(fn)): seen.add((r['week'],r['game'],r['offense_player']))
with open(fn,'a',newline='') as f:
  w=csv.writer(f)
  if new: w.writerow(['week','game','offense_player','archetype','defense','defenders','coverage_shell','result_line','edge_reason','attribution_confidence'])
  n=0
  for e in E:
    if ('8',e['game'],e['name']) in seen: continue
    conf=set(re.findall(r'\[(.*?)\]',' '.join(e['beaten']))) or {'none (no explosive)'}
    w.writerow([8,e['game'],e['name'],e['arch'],e['opp'],' / '.join(e['beaten']) or '',SHELL.get(e['opp'],''),e['line'],e['why'],';'.join(sorted(conf))]); n+=1
print('rows',n); 
for i,e in enumerate(E[:12],1): print(i,e['name'],e['arch'],e['line'],len(e['ex']))
