import re,pandas as pd,json
pl=pd.read_parquet('players.parquet')
od=pd.read_csv('odds_a0715.csv'); onames=set(od.player.dropna())
NV={'LAR':'LA','WSH':'WAS'}
txt=open('/workspace/nfl-database/key_players.md').read()
out={};miss=[]
for blk in re.split(r'\n## ',txt)[1:]:
    team=blk.split('\n')[0].strip()
    if team in('CHI','SEA'):continue
    line=[l for l in blk.split('\n') if l.startswith('- Players:')][0][len('- Players:'):]
    for ent in line.split(';'):
        ent=ent.strip(); m=re.match(r'(QB|RB|WR|TE)\s+(.+)',ent)
        if not m: continue
        pos,nm=m.group(1),re.sub(r'\s*\(.*?\)','',m.group(2)).strip()
        if 'OUT' in ent or 'when he returns' in ent: out[f'{team}|{nm}']={'team':team,'pos':pos,'name':None,'note':ent};continue
        c=pl[(pl.latest_team==NV.get(team,team))&(pl.position==pos)]
        cand=c[(c.display_name==nm)|(c.display_name.str.split().str[-1].str.replace('.','')==nm.split()[-1].replace('.',''))|(c.last_name==nm.split()[-1])]
        names=[n for n in cand.display_name if n in onames] or list(cand.display_name)
        out[f'{team}|{nm}']={'team':team,'pos':pos,'name':names[0] if len(names)==1 else None,'cands':names,'note':ent}
        if len(names)!=1: miss.append((team,ent,names))
json.dump(out,open('keymap.json','w'),indent=1)
for k,v in out.items(): print(k,'->',v['name'],v.get('cands'))
print('AMBIG',miss)
