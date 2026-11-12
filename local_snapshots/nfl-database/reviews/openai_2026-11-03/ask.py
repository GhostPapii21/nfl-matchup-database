import os,json,urllib.request
brief=open('brief_compact.md').read()
q="""You are a senior sports-betting quant and experimental-design reviewer. Read the brief and give a frank, structured critique:
1. Statistical design fix list: sample size/power (how many legs needed to detect a real edge at -110 / parlay odds), overfitting from repeated rule tweaks, a strict LLM-leakage protocol, CLV as primary metric, calibration.
2. Per-version review (sims, rulebook replays, Rico method wk8, v5, v6 plan): what went wrong and what we should have done.
3. A better per-game reasoning checklist for yardage props using only free data.
4. Parlay/correlation advice for 3-4 leg slips.
5. Prioritized next-5-steps plan feasible under our constraints (no PFF/film, ~250 odds credits/week, no history pulls).
Say explicitly where you are unsure. Use compact Markdown bullets, under 1800 words.\n\n"""+brief
for model in ["gpt-5.5"]:
  try:
    r=urllib.request.Request("https://api.openai.com/v1/responses",data=json.dumps({"model":model,"input":q,"reasoning":{"effort":"low"},"max_output_tokens":3000}).encode(),headers={"Authorization":"Bearer "+os.environ["OPENAI_API_KEY"],"Content-Type":"application/json"})
    d=json.load(urllib.request.urlopen(r,timeout=900));break
  except Exception as e: print(model,"fail",getattr(e,'read',lambda:b'')()[:300])
txt="".join(c.get("text","") for o in d["output"] if o["type"]=="message" for c in o["content"])
open('response.md','w').write(f"# OpenAI response ({d['model']}, reasoning low (10k TPM cap))\n\n"+txt)
open('usage_log.jsonl','a').write(json.dumps({"model":d["model"],"usage":d["usage"]})+"\n")
print(d["model"],d["usage"])
