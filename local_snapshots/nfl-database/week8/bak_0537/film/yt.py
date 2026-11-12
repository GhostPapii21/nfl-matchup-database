import json,glob,subprocess,re,os
from concurrent.futures import ThreadPoolExecutor
os.makedirs('captions',exist_ok=True)
def clean(vtt):
    out=[];last=''
    for blk in open(vtt).read().split('\n\n'):
        ls=blk.strip().split('\n')
        if not ls or '-->' not in ls[0]: continue
        t=ls[0].split('.')[0][3:]
        txt=' '.join(re.sub('<[^>]+>','',l) for l in ls[1:]).strip()
        if txt and txt!=last and not last.endswith(txt):
            nl=txt[len(last):].strip() if txt.startswith(last) else txt
            if nl: out.append(f'[{t}] {nl}')
            last=txt
    return '\n'.join(out)
def do(f):
    g=json.load(open(f))
    if g.get('yt'): return
    q=f"ytsearch6:{g['awayName']} vs {g['homeName']} Game Highlights 2026 NFL Season Week {g['week']}"
    r=subprocess.run(['yt-dlp','--flat-playlist','-J',q],capture_output=True,text=True)
    try: ents=json.loads(r.stdout)['entries']
    except Exception: g['yt']={'error':'search failed'}; json.dump(g,open(f,'w'),indent=1); return
    an,hn=g['awayName'].split()[-1],g['homeName'].split()[-1]
    pick=None
    for e in ents:
        t=e.get('title','')
        ch=(e.get('channel') or e.get('uploader') or ''); okw=(f"Week {g['week']}" in t) or ('Week' not in t)
        if an[:5] in t and hn[:5] in t and okw and 'Highlights' in t and ch.startswith('NFL'):
            pick=e;break
    if not pick: g['yt']={'error':'no matching NFL-channel video','candidates':[(e.get('title'),e.get('channel')) for e in ents]}; json.dump(g,open(f,'w'),indent=1); return
    url='https://www.youtube.com/watch?v='+pick['id']
    g['yt']={'url':url,'title':pick['title'],'channel':pick.get('channel'),'duration':pick.get('duration')}
    base=f"captions/{g['gid']}"
    subprocess.run(['yt-dlp','--skip-download','--write-auto-subs','--write-subs','--sub-langs','en.*,en','--sub-format','vtt','-o',base,url],capture_output=True)
    v=sorted(glob.glob(base+'*.vtt'))
    if v: open(base+'.txt','w').write(clean(v[0])); g['yt']['captions']=base+'.txt'
    else: g['yt']['captions']=None
    json.dump(g,open(f,'w'),indent=1)
with ThreadPoolExecutor(6) as ex: list(ex.map(do,glob.glob('games/*.json')))
ok=sum(1 for f in glob.glob('games/*.json') if json.load(open(f))['yt'].get('captions'))
print('with captions',ok)
for f in glob.glob('games/*.json'):
    y=json.load(open(f))['yt']
    if not y.get('captions'): print(f,y)
