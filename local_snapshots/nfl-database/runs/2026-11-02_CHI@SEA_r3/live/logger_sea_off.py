import json,time,urllib.request,re,csv,os
URL="https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event=401873036"
OUT="chi_defender_log.csv"
seen=set()
while True:
    try:
        d=json.load(urllib.request.urlopen(URL,timeout=20))
        drives=d.get('drives',{}).get('previous',[])+([d['drives']['current']] if d.get('drives',{}).get('current') else [])
        rows=[]
        for dr in drives:
            off=dr.get('team',{}).get('abbreviation','')
            for p in dr.get('plays',[]):
                pid=p.get('id')
                if pid in seen: continue
                seen.add(pid)
                t=p.get('text','')
                if off!='SEA': continue
                if not re.search(r'pass|rush|left|right|middle|scramble|sacked',t,re.I): continue
                m=re.search(r'(?:to|by) ([A-Z]\.[A-Za-z\-\' ]+?)(?: to | for | ran| pushed|\.|\s\[|\s\()',t)
                tgt=m.group(1).strip() if m else ''
                tack=';'.join(re.findall(r'\(([^)]*)\)',t))
                pd=';'.join(re.findall(r'\[([^\]]*)\]',t))
                kind='pass' if 'pass' in t.lower() else ('sack' if 'sacked' in t.lower() else 'rush')
                rows.append([p.get('period',{}).get('number'),p.get('clock',{}).get('displayValue'),kind,tgt,tack,pd,t])
        new=not os.path.exists(OUT)
        with open(OUT,'a',newline='') as f:
            w=csv.writer(f)
            if new: w.writerow(['qtr','clock','type','ball_carrier_or_target','tacklers','pass_defended_by','text'])
            w.writerows(rows)
        if d.get('header',{}).get('competitions',[{}])[0].get('status',{}).get('type',{}).get('completed'): break
    except Exception as e:
        open('err.log','a').write(str(e)+'\n')
    time.sleep(60)
