import json
d=json.load(open('compare.json'));R=d['rows']
MK={'rec_yds':'Y','receptions':'R','rush_yds':'U','rush_rec_yds':'T'}
def rg(r):
  x=r['rung']
  if not x: return ''
  if 'no alt rung' in x: return 'main line'
  if 'no alt ladder' in x: return 'main line'
  return x.split(',')[0].replace(' (FD posts no alt unders)','')
def row(r): return [r['player']+(' (Q)' if r['q'] else ''),MK[r['market']],r['fd_line'],r['fd_over'],r['fd_under'],r['median'],round(r['edge_pct']),round(r['p_over']*100),{'LEAN OVER':'O','LEAN UNDER':'U'}.get(r['lean'],'N'),rg(r)]
P={}
for r in sorted(R,key=lambda r:(r['player'],r['market'])):
  gid=r['game'].replace('LAC@LAR','LAC@LA').replace('PHI@WSH','PHI@WAS')
  P.setdefault(gid,{}).setdefault(r['team'],[]).append(row(r))
st=lambda r:r['p_over'] if r['lean']=='LEAN OVER' else 1-r['p_over']
B=sorted([r for r in R if r['lean']!='NO BET' and r['gate']],key=lambda r:-st(r))[:25]
s='const PR: any = '+json.dumps(P,separators=(',',':'),ensure_ascii=False)+';\nconst BEST: any[] = '+json.dumps([[r['game']]+row(r) for r in B],separators=(',',':'),ensure_ascii=False)+';\n'
open('/tmp/P.txt','w').write(s); print(len(s))
