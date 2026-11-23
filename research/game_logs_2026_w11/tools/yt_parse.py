import json,re,sys,os
def load(path):
    s=open(path).read()
    m=re.search(r'Full text: (\S+?\.txt)',s)
    if m: s=open(m.group(1)).read()
    i=s.index('{"conversationId"')
    return json.JSONDecoder().raw_decode(s[i:])[0]
d=load(sys.argv[1]); out='/workspace/runs/2026-11-22_W11_GAME_LOGS/video'
for it in d['data']['alexandria']:
    if 'error' in it: print('ERR',it['error']); continue
    x=it['data']
    if 'video_id' in x and 'full_text' in x:
        json.dump(x,open(f"{out}/{x['video_id']}.json",'w'),indent=1); print('TRANSCRIPT',x['video_id'],x['title'],x.get('track_name'))
    for v in x.get('videos',[])[:15]:
        print(v['video_id'],v.get('channel_name'),'|',v['title'],'|',v.get('length_text'),v.get('published_text'))
    print('---')
