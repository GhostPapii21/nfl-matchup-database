import time,re
exec(open('deep.py').read().split('b=open')[0])
M="gpt-6.1-sol"
txt=open('section_reviews.md').read()
parts=re.split(r'(?m)^(?=## (?:Section review|Review of))',txt); parts=[p for p in parts if p.strip()]
dig=[]
for p in parts:
  t,_=call(M,"Condense this review into dense bullet notes (<=350 words), keeping every number, finding, rule name, YES/NO rule-undo marks and recommendation:\n\n"+p,"low",900)
  dig.append(p.splitlines()[0]+"\n"+(t or p[:1500])); time.sleep(65)
open('section_digests.md','w').write("\n\n".join(dig))
s="Using ONLY these condensed section reviews of an NFL player-prop backtest program (constraints: free data only, no PFF/film/coverage data, Odds API ~250 credits/week, no historical odds pulls until Dec; plays FanDuel/PrizePicks 3-4 leg yardage slips, no TDs, no passing yards), write the complete deep-dive: 1) statistical design fix list (sample size/power, overfitting, leakage protocol, CLV, calibration); 2) per-version review: v1 100k sims, rulebook replays wk6-8, Rico method wk8, v5, v6; 3) verdict on the ChatGPT MNF audit proposals, marking which would undo Rico-approved rules (N1, N2, #3/#4 rule, -250 flag); 4) per-game reasoning checklist; 5) slip/correlation advice; 6) top-5 plan under constraints; 7) uncertainties. Markdown, <=2000 words.\n\n"+"\n\n".join(dig)
for eff in ["high","medium"]:
  t,m=call(M,s,eff,4500)
  if t and len(t)>1000: break
  time.sleep(70)
open('response_deep.md','w').write(f"# Deep-dive review ({m}; full per-chunk reviews in section_reviews.md)\n\n"+(t or "(empty)"))
print("DONE",flush=True)
