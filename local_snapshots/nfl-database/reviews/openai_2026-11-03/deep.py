import os,json,time,urllib.request,urllib.error
K=os.environ["OPENAI_API_KEY"]
def call(model,inp,effort,maxo):
  r=urllib.request.Request("https://api.openai.com/v1/responses",data=json.dumps({"model":model,"input":inp,"reasoning":{"effort":effort},"max_output_tokens":maxo}).encode(),headers={"Authorization":"Bearer "+K,"Content-Type":"application/json"})
  try: d=json.load(urllib.request.urlopen(r,timeout=900))
  except urllib.error.HTTPError as e:
    b=e.read().decode()[:400]; print("ERR",model,b,flush=True)
    if "insufficient_quota" in b: raise SystemExit("QUOTA")
    return None,None
  t="".join(c.get("text","") for o in d["output"] if o["type"]=="message" for c in o["content"])
  open('usage_log.jsonl','a').write(json.dumps({"model":d["model"],"effort":effort,"usage":d["usage"]})+"\n")
  print(d["model"],effort,d["usage"]["input_tokens"],d["usage"]["output_tokens"],len(t),flush=True); return t,d["model"]
b=open('brief_deep.md').read(); N=23000
chunks=[b[i:i+N] for i in range(0,len(b),N)]
M="gpt-6.1-sol"; revs=[]
for i,c in enumerate(chunks):
  q=f"You are a senior sports-betting quant and experimental-design reviewer. This is chunk {i+1}/{len(chunks)} of a brief on an amateur NFL player-prop (yardage, 3-4 leg slips) backtest program. Write a detailed, frank section review of THIS chunk: what the evidence shows, design flaws, leakage/overfitting risks, what should have been done, and concrete fixes. Cite numbers/files from the chunk. Note uncertainties. Compact Markdown, <=1200 words.\n\n"+c
  t=None
  for eff in ["high","medium"]:
    t,m=call(M,q,eff,3300); time.sleep(70)
    if t and len(t)>500: break
  revs.append(f"## Section review {i+1}/{len(chunks)}\n\n"+(t or "(empty)"))
  open('section_reviews.md','w').write("\n\n".join(revs))
s="Using ONLY these section reviews of an NFL player-prop backtest program (constraints: free data only, no PFF/film/coverage data, Odds API ~250 credits/week, no historical odds pulls until Dec; plays FanDuel/PrizePicks 3-4 leg yardage slips, no TDs, no passing yards), write the complete deep-dive: 1) statistical design fix list (sample size/power, overfitting, leakage protocol, CLV, calibration); 2) per-version review: v1 100k sims, rulebook replays wk6-8, Rico method wk8, v5, v6; 3) per-game reasoning checklist; 4) slip/correlation advice; 5) top-5 plan under constraints; 6) uncertainties. Markdown, <=2200 words.\n\n"+"\n\n".join(revs)
for eff in ["high","medium"]:
  t,m=call(M,s,eff,4000); 
  if t and len(t)>1000: break
  time.sleep(70)
open('response_deep.md','w').write(f"# Deep-dive review ({m}; per-chunk reviews in section_reviews.md)\n\n"+(t or "(empty)"))
print("DONE",flush=True)
