# Asserts explosives_allowed.md defense/offense match drive possession and box-score rush totals.
import re,glob,os,json,collections,sys
PL='/workspace/nfl-database/playlogs'
def play_key(clock,text):
  """Normalize (clock,text) for drive matching: OT/Q5 are the same period; strip ESPN leading/trailing spaces and the score suffix."""
  clock=re.sub(r'^OT\d?',"Q5",clock.strip())
  return (clock,text.split(' (score')[0].strip()[:60])
def main():
  rows=[[x.strip() for x in l.strip().strip('|').split('|')] for l in open(PL+'/explosives_allowed.md') if l.startswith('| 2026')]
  err=[]
  for g in [p for p in glob.glob(PL+'/2026_wk8/*_plays.md') if os.path.exists(p.replace('_plays.md','_box.json'))]:
    key=os.path.basename(g)[:-9].replace('_','@'); a,h=key.split('@'); off=None; poss={}
    for ln in open(g):
      m=re.match(r'## Drive: (\w+)',ln)
      if m: off=m.group(1)
      m=re.match(r'- (Q\d \d+:\d+) \[[^\]]*\] (.*)',ln)
      if m: poss[play_key(m.group(1),m.group(2))]=off
    box=json.load(open(g.replace('_plays.md','_box.json')))
    rush=collections.Counter(); 
    for r in rows:
      if r[1]!=key: continue
      o=poss.get(play_key(r[4],r[8]))
      if o is None: err.append(f'no drive match {key} {r[4]}'); continue
      if r[3]!=o: err.append(f'offense mismatch {key} {r[4]} row={r[3]} drive={o}')
      if r[2]!=({a,h}-{o}).pop(): err.append(f'defense mismatch {key} {r[4]}')
      if 'INTERCEPTED' in r[8]: err.append(f'INT return in offensive table {key} {r[4]}')
      if r[5]=='rush': rush[r[3]]+=1
    for t,n in rush.items():
      car=sum(int(p['CAR']) for p in box['teams'][t].get('rushing',[]))
      if n>car: err.append(f'{key} {t} {n} rush explosives > {car} carries')
  print('FAIL' if err else 'PASS', len(rows),'rows'); [print(' ',e) for e in err]; sys.exit(1 if err else 0)
if __name__=='__main__': main()
