import os,json,sys,urllib.request,urllib.error
def call(model,inp,effort,maxo,tag):
  r=urllib.request.Request("https://api.openai.com/v1/responses",data=json.dumps({"model":model,"input":inp,"reasoning":{"effort":effort},"max_output_tokens":maxo}).encode(),headers={"Authorization":"Bearer "+os.environ["OPENAI_API_KEY"],"Content-Type":"application/json"})
  try: d=json.load(urllib.request.urlopen(r,timeout=900))
  except urllib.error.HTTPError as e:
    b=e.read().decode()[:400]; print("ERR",model,b,flush=True); return None
  t="".join(c.get("text","") for o in d["output"] if o["type"]=="message" for c in o["content"])
  open('usage_log.jsonl','a').write(json.dumps({"tag":tag,"model":d["model"],"effort":effort,"status":d.get("status"),"usage":d["usage"]})+"\n")
  print(tag,d["model"],effort,d.get("status"),d["usage"]["input_tokens"],d["usage"]["output_tokens"],len(t),flush=True); return t
if __name__=="__main__":
  model,effort,maxo,tag,inf,outf=sys.argv[1:7]
  t=call(model,open(inf).read(),effort,int(maxo),tag)
  if t: open(outf,'w').write(t)
