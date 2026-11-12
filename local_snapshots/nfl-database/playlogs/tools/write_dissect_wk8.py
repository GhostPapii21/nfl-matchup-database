import json,os,shutil,collections as C,glob
B='/workspace/nfl-database'; W=B+'/playlogs/2026_wk8'; S='2026-11-01'
P=json.load(open(W+'/_dissect_plays.json')); R=json.load(open(W+'/_dissect_posallow.json')); D=json.load(open(W+'/_dissect_defenders.json'))
X=[p for p in P if p['x']]
def row(p): return f"| {p['game']} | {p['defn']} | {p['off']} | {p['when']} | {'Rush' if p['kind']=='rush' else 'Rec'} | {p['fullname']} ({p['pos']}) | {p['yds']} | {p['dfr'] or '—'} | {p['conf']} | {p['src'] or '—'} | {p['align']} | {p['shell_tend']} | Y |"
HDR="| Game | Defense | Offense | When | Type | Player (pos) | Yds | Defender at fault / tackler | Confidence | Source | Receiver alignment (labeled) | Shell (season tendency, labeled) | expl_v2 (rush15+/rec20+) |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
# 1 explosives_allowed append
EA=B+'/playlogs/explosives_allowed.md'; shutil.copy(EA,EA+'.pre_wk8dissect.bak')
with open(EA,'a') as f:
  f.write(f"\n\n## Week 8 ({S}) — expl_v2 flag table (rush 15+, reception 20+), all 8 final 1 PM games\nAppended; rows above are unchanged. Every row here has expl_v2=Y. Rows above that are 10–14 yd rushes are expl_v2=N. Coverage shell: no FTN/participation for Week 8 yet, so the shell shown is the defense's PREGAME SEASON TENDENCY (Sharp), not the call on the play. 'Inferred' = the pregame primary matchup (ESPN Mike Clay cheat sheet + coverage.json), not charted coverage. 'tackler-of-record' = ESPN play-text parentheses (single source), not the gap/fit defender.\n\n"+HDR+''.join(row(p)+'\n' for p in X))
# per-defense summary
def dsum(d,g):
  xs=[p for p in X if p['defn']==d and p['game']==g]
  return xs
md=[]
def block(g,d):
  xs=dsum(d,g); r=[r for r in R if r['game']==g and r['defn']==d][0]
  o=[f"\n\n## Week 8 ({S}) — {d} defense vs {[t for t in g.split('@') if t!=d][0]} ({g})\nAppended {S}; season numbers above are untouched. Sources: ESPN summary API play-by-play (single source), pregame matchups week8/breakdown/coverage/coverage.json + ESPN cheat sheet, nflverse pbp wk1–7 for QB baselines. Freshness: coverage tendencies are from 10/27–10/29 pulls, older than 48h → STALE for shell; Week 8 FTN not released.\n",
     f"**Explosives allowed (rush 15+/rec 20+): {len(xs)}** ({sum(p['kind']=='rush' for p in xs)} rush, {sum(p['kind']=='rec' for p in xs)} rec)\n"]
  for p in xs: o.append(f"- {p['when']} {p['fullname']} ({p['pos']}) {p['kind']} {p['yds']} — {p['dfr'] or 'defender unknown'} [{p['conf']}; {p['src'] or 'no public source'}]; alignment: {p['align']}\n")
  o.append("\n**Yards allowed by position (QB-adjusted, features.py residual method):** YPT vs this D minus the passer's own wk1–7 YPT to that group (fallback: league YPT when <8 tgts). Positive = worse than that QB normally gets.\n\n| Group | Tgt | Rec | Yds | QB-adj YPT resid | QB baseline |\n|---|---|---|---|---|---|\n")
  for k,v in r['out'].items(): o.append(f"| {k} | {v[0]} | {v[1]} | {v[2]} | {v[3] if v[3] is not None else '—'} | {v[4]} |\n")
  o.append(f"| RB rush | {r['rbrush'][0]} car | — | {r['rbrush'][1]} | {round(r['rbrush'][1]/max(r['rbrush'][0],1),2)} ypc | — |\n")
  o.append("\nWR_out/WR_mid split uses ESPN pass_location (left/right=outside proxy, middle=slot/middle proxy), the same proxy as the season WR_outside/WR_middle numbers.\n\n**Defenders (ESPN-text proxy; per-defender targets are NOT public free — PFF/FTN-premium only):** catches/yards = first tackler after the catch (CAR_secondary.md method), PBU = named on an incompletion.\n\n| Defender | Pos | Rec charged | Yds | 20+ | PBU | INT | Pen (DPI/hold/IC) | Receivers |\n|---|---|---|---|---|---|---|---|---|\n")
  dd=sorted([(k.split('|')[1],v) for k,v in D.items() if k.split('|')[0]==g and v['team']==d],key=lambda x:-x[1]['yds'])
  for n,v in dd:
    if v['pos'] in ('CB','SS','FS','S','DB','ILB','OLB','LB','MLB') or v['pbu'] or v['int'] or v['pen']:
      o.append(f"| {n} | {v['pos']} | {v['rec']} | {v['yds']} | {v['x']} | {v['pbu']} | {v['int']} | {v['pen']} | {', '.join(f'{a}×{b}' for a,b in v['recv'].items())} |\n")
  inf=C.defaultdict(lambda:[0,0,0])
  for p in P:
    if p['defn']==d and p['game']==g and p['conf']=='inferred' and p['kind'] in('rec','inc'):
      a=inf[(p['dfr'],p['fullname'])]; a[0]+=1; a[1]+=p['kind']=='rec'; a[2]+=p['yds']
  o.append("\n**Inferred matchups (labeled INFERRED: receiver's line when targeted vs his pregame primary defender):**\n")
  for (df,rc),a in sorted(inf.items(),key=lambda x:-x[1][2]): o.append(f"- {df} ← {rc}: {a[0]} tgt, {a[1]} rec, {a[2]} yds{' — limited his man' if a[0]>=3 and a[2]/a[0]<6 else ''}\n")
  return ''.join(o)
games=sorted({p['game'] for p in P})
for f in glob.glob(B+'/week8/defense/*_at_*.md'): shutil.copy(f,f+'.pre_wk8dissect.bak')
os.makedirs(B+'/defenders',exist_ok=True)
for f in glob.glob(B+'/defenders/*.md'): shutil.copy(f,f+'.pre_wk8dissect.bak')
paths=[]
blocks={}
for g in games:
  a,h=g.split('@'); wf=f"{B}/week8/defense/{a}_at_{h}.md"
  for d in (a,h):
    b=block(g,d); blocks[(g,d)]=b
    if os.path.exists(wf): open(wf,'a').write(b); paths.append(wf)
    df=f"{B}/defenders/{d}_secondary.md"
    if not os.path.exists(df): open(df,'w').write(f"# {d} secondary / defense coverage ledger\nCreated {S} by wk8 dissection. Method: see defenders/CAR_secondary.md and postmortems/WEEK8_DEFENSE_DISSECTION_{S}.md.\n")
    open(df,'a').write(b); paths.append(df)
# stubs
done={t for g in games for t in g.split('@')}
for f in sorted(glob.glob(B+'/week8/defense/*_at_*.md')):
  if f.endswith('.bak'): continue
  a,h=os.path.basename(f)[:-3].split('_at_')
  if a in done: continue
  open(f,'a').write(f"\n\n## Week 8 ({S}) — STUB: {a}@{h} not final at time of dissection (4 PM / SNF). Fill with playlogs/tools/defense_dissect_wk8.py once box/plays are pulled.\n"); paths.append(f)
json.dump(sorted(set(paths)),open(W+'/_dissect_paths.json','w'),indent=0)
print(len(set(paths)))
