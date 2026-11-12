import json,glob,os,re,sys,time,requests,threading
from concurrent.futures import ThreadPoolExecutor
MODEL=os.environ.get('GROK_MODEL','grok-4.20-0309-non-reasoning')
SCHEMA=json.load(open('schema.json')); os.makedirs('grok_meta',exist_ok=True)
lock=threading.Lock()
def log(m):
    with lock: open('run_grok.log','a').write(time.strftime('%H:%M:%S ')+m+'\n')
def clean(v):
    out=[];prev=None;ts=None
    for l in open(v).read().splitlines():
        m=re.match(r'(\d\d:\d\d:\d\d)\.\d+ -->',l)
        if m: ts=m.group(1);continue
        if not l.strip() or l.startswith(('WEBVTT','Kind:','Language:')) or l.strip().isdigit(): continue
        t=re.sub(r'<[^>]+>','',l).strip()
        if t and t!=prev: out.append(f'[{ts}] {t}');prev=t
    return '\n'.join(out)
def valid(o):
    try:
        import jsonschema; jsonschema.validate(o,SCHEMA); return True
    except ImportError:
        return all(k in o for k in SCHEMA['required'])
    except Exception as e: log(f'schema fail {e.message[:200]}'); return False
def call(p):
    body={'model':MODEL,'messages':[{'role':'user','content':p}],'temperature':0,
          'response_format':{'type':'json_schema','json_schema':{'name':'film','schema':SCHEMA,'strict':True}}}
    for a in range(6):
        r=requests.post('https://api.x.ai/v1/chat/completions',headers={'Authorization':'Bearer '+os.environ['XAI_API_KEY']},json=body,timeout=600)
        if r.status_code==429 or r.status_code>=500: log(f'HTTP {r.status_code} retry {a}');time.sleep(5*2**a);continue
        r.raise_for_status();return r.json()
    raise RuntimeError('retries exhausted')
def do(f):
    g=json.load(open(f)); gid=g['gid']; out=f'codex_out/{gid}.json'
    if os.path.exists(out): return
    if not g.get('yt',{}).get('captions'): log(f'{gid} SKIP no captions'); return
    cap=clean(g['yt']['captions'])
    p=f"""You are reviewing an NFL highlight video via its auto-generated CAPTIONS ONLY (broadcast commentary audio). You cannot see video frames. Game: {g['score']} (2026 Week {g['week']}, game_id {gid}). Video: {g['yt']['title']} {g['yt']['url']}

Authoritative DB play-by-play (scoring plays, plays >=20 yds, turnovers):
{chr(10).join(g['key_plays'])}

Captions (timestamps = position in video):
{cap}

Task: list every highlight play you can identify in the captions. For each: caption_ts (from captions), team (abbr on offense), player, description, yards, is_score, concept (run gap/direction, play-action, screen, deep shot, RPO, etc. ONLY if the commentary says it or the DB text shows it, else 'unknown'), personnel_formation and coverage_scheme ONLY if commentators explicitly state it else 'unknown', defender_beaten (named in commentary or DB tackler text, else 'unknown'), db_match = the exact matching DB play line (copy 'Q# clock') or 'NO DB MATCH'. Captions are auto-generated and mangle names; use the DB to correct names only when the play clearly matches. Then team_notes for both teams: offensive strengths/patterns and defensive weaknesses supported by the plays above (no generic claims). limitations: what you could not determine. Never invent. Output JSON only matching the schema; game_id="{gid}"."""
    for a in range(2):
        try:
            j=call(p); o=json.loads(j['choices'][0]['message']['content'])
            if valid(o):
                o['game_id']=gid; json.dump(o,open(out,'w'),indent=1)
                json.dump({'source':'grok via xAI API','model':j.get('model',MODEL),'usage':j.get('usage'),'ts':time.strftime('%Y-%m-%d %H:%M ET')},open(f'grok_meta/{gid}.json','w'),indent=1)
                log(f"{gid} OK plays={len(o['plays'])} usage={j.get('usage',{}).get('total_tokens')}");return
        except Exception as e: log(f'{gid} attempt {a} error {str(e)[:200]}')
    log(f'{gid} FAILED')
fs=sorted(glob.glob('games/*.json'))
if len(sys.argv)>1: fs=[f for f in fs if sys.argv[1] in f]
with ThreadPoolExecutor(3) as ex: list(ex.map(do,fs))
