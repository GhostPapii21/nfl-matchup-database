import json,glob,os,re
AG='401872944, 401872945, 401872952, 401872962, 401872964, 401872970, 401872985, 401872989'.split(', ')
GR={os.path.basename(f)[:-5] for f in glob.glob('grok_meta/*.json')}
G={json.load(open(f))['gid']:json.load(open(f)) for f in glob.glob('games/*.json')}
for fm in glob.glob('*_film.md'):
    t=fm[:-8]; mine=[g for g in G if t in (G[g]['away'],G[g]['home'])]
    a=[g for g in mine if g in AG]; r=sorted(g for g in mine if g in GR)
    L=open(fm).read().split('\n'); ins=[]
    if a: ins.append(f"> Note: games {', '.join(AG)} were extracted by a Grok Bot agent (not Codex) from the same captions; mostly scoring/20+ plays logged.")
    if r: ins.append(f"> Note: games {', '.join(r)} were extracted by Grok via the xAI API (grok-4.20-0309-non-reasoning, same prompt/schema as Codex, cleaned captions); sidecar provenance in film/grok_meta/. All other games with notes: Codex.")
    L[1:1]=ins; s='\n'.join(L)
    s=re.sub(r"\(Codex synthesis from this game's plays\)","(model synthesis from this game's plays)",s)
    open(fm,'w').write(s)
    ap=f'teams/{t}_appendix.md'; S=open(ap).read()
    S=S.replace('Codex extraction, DB cross-check.',f"extraction by Codex (most games), Grok Bot agent ({len(a)} games), Grok via xAI API ({len(r)} games); DB cross-check.")
    open(ap,'w').write(S)
    b=f'../team_baselines/{t}.md'; B=open(b).read()
    i=B.find('\n\n## FILM NOTES (Phase 8)')
    if i<0: i=B.find('## FILM NOTES (Phase 8)')
    B=(B[:i] if i>=0 else B.rstrip('\n'))+S
    assert B.count('FILM NOTES (Phase 8)')==1; open(b,'w').write(B)
print('ok')
