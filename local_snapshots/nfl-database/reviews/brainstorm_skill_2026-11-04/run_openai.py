import os,json,urllib.request
skill=open('/home/box/agent-data/workflows/betting-game-brainstorm/SKILL.md').read()
ctx="""Context: The user (Rico) set a new philosophy today: the game scenario (opponent QB, possession, blitz read, routes vs defenders, defense leaks) sets the projection. A recent game log is only a cross-check with a miss audit (why he missed and whether that cause is present this week), never a standalone veto. Stat gates that disagree get flagged to Rico, not used to cut. Trigger: the agent built a full scenario read showing Parker Washington (JAX WR1, top target vs blitz, BAL on a third-string QB, JAX holding the ball more) should clear 4+ catches, then reversed itself citing his 2-of-5 game log. Track record: legs picked from averages or sims lost at real prices; rush unders are the only proven backtested edge (231-190, +2.8% ROI on 421 priced legs); models rating legs 70-80% hit about 50%. House gates: 3-of-4 line check, last-2 downgrade, N1 under-60%-carry rush-over cut, edge tiers flag-only, best-price shop, 3-4 leg slips.
NOTE: judge whether the file as written actually implements the scenario-first philosophy."""
ask="""Review this betting brainstorm SKILL.md. Give: (1) what's strong; (2) concrete edits that make it stronger, with exact replacement wording keyed to step/line; (3) parts that could hurt judgment: confirmation bias, unfalsifiable scenario stories, the miss audit becoming an excuse machine, double-counting multipliers (e.g. more plays x higher share x better efficiency all from the same story), overconfidence, missing calibration/tracking of scenario reads, conflicts with house stat gates. Be specific and line-level. Markdown."""
body={"model":None,"input":[{"role":"user","content":ctx+"\n\n"+ask+"\n\n---SKILL.md---\n"+skill}]}
for m in ["gpt-5","o3","gpt-4.1"]:
    body["model"]=m
    req=urllib.request.Request("https://api.openai.com/v1/responses",json.dumps(body).encode(),{"Authorization":"Bearer "+os.environ["OPENAI_API_KEY"],"Content-Type":"application/json"})
    try:
        r=json.load(urllib.request.urlopen(req,timeout=600)); break
    except Exception as e: print(m,"failed",e)
txt="".join(c.get("text","") for o in r["output"] if o.get("type")=="message" for c in o["content"])
u=r["usage"]; print(r["model"],u)
open("openai_review.md","w").write(f"# OpenAI review\nModel: {r['model']}  \nUsage: {json.dumps(u)}\n\n"+txt)
