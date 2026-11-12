import os,json,time,urllib.request,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
KEY=os.environ.get('GROK_API_KEY') or os.environ.get('XAI_API_KEY');MODEL='grok-4.7'
def call(msgs,json_mode=True,temp=0.0,tag=''):
    b={'model':MODEL,'messages':msgs,'temperature':temp}
    if json_mode:b['response_format']={'type':'json_object'}
    body=json.dumps(b).encode()
    for a in range(2):
        try:
            r=urllib.request.Request('https://api.x.ai/v1/chat/completions',body,{'Authorization':'Bearer '+KEY,'Content-Type':'application/json'})
            with urllib.request.urlopen(r,timeout=900) as resp:d=json.load(resp)
            u=d.get('usage',{});u['tag']=tag;open(ROOT/'usage_log.jsonl','a').write(json.dumps(u)+'\n')
            return d['choices'][0]['message']['content']
        except Exception as e:
            print('API error',type(e).__name__,getattr(e,'code',''),file=sys.stderr);time.sleep(15*(a+1))
    raise SystemExit('API failed')
