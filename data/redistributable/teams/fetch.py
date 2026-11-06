import json,subprocess,time,os
for w in range(1,9):
  for e in json.load(open(f'espn_raw/sb_{w}.json'))['events']:
    if not e['status']['type']['completed']: continue
    f=f"espn_raw/sum_{e['id']}.json"
    if os.path.exists(f) and os.path.getsize(f)>1000: continue
    subprocess.run(['curl','-s','--max-time','30',f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={e['id']}",'-o',f]); time.sleep(0.4)
