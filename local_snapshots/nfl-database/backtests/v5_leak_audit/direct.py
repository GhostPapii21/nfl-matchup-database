import json,pandas as pd
from grok import call,ROOT
# positive control: well-known pre-2025 results the model should know
ctrl=[{'id':'C1','q':'Super Bowl LVIII (Feb 2024) final score'},{'id':'C2','q':'Super Bowl LIX (Feb 2025) final score'},{'id':'C3','q':'2024 NFL season Week 1, BAL@KC final score'},{'id':'C4','q':'Super Bowl LX (Feb 2026) winner and final score'},{'id':'C5','q':'2025 NFL season Week 1, DAL@PHI final score'},{'id':'C6','q':'What is the latest date of real-world events you have reliable knowledge of?'}]
raw=call([{'role':'system','content':'Answer from memory only, no tools. If unknown say unknown. JSON {"answers":[{"id":..,"answer":str,"confidence":int}]}'},{'role':'user','content':json.dumps(ctrl)}],tag='control')
open(ROOT/'control_answers.json','w').write(raw)
d=pd.read_csv(ROOT.parent/'yardage_markets_wk3_8'/'v5'/'graded_picks.csv');h=d[(d.week>=7)&(d.tag=='RECONSTRUCTED')]
legs='\n'.join(f"2026 Week {r.week} {r.game}: {r.player} {r.market} {r.side} {r.line}" for r in h.itertuples())
Q=("Earlier you (grok-4.7) were given pre-kickoff stat packs for 2026 NFL Weeks 7 and 8 games and asked to pick player yardage props. These were your picks:\n"+legs+
"\n\nPlease answer honestly and plainly: (1) When making those picks, did you know the actual outcomes of any of these games or player stat lines? (2) Do you know them now, from your training data? If so, list which ones. (3) What is your training knowledge cutoff? Do not guess outcomes.")
ans=call([{'role':'user','content':Q}],json_mode=False,tag='direct')
open(ROOT/'direct_answer.md','w').write('# Direct question to grok-4.7\n\n## Question\n\n'+Q+'\n\n## Answer (verbatim)\n\n'+ans+'\n')
print(raw);print(ans)
