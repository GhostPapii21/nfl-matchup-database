import csv, subprocess, datetime, pathlib, time
from zoneinfo import ZoneInfo
ROOT=pathlib.Path(__file__).resolve().parent
(ROOT/'raw').mkdir(exist_ok=True)
def fetch(name,url,pfr=False):
    if pfr: time.sleep(3)
    start=datetime.datetime.now(ZoneInfo('America/New_York')).isoformat(timespec='seconds')
    out=ROOT/'raw'/f'{name}.html'
    r=subprocess.run(['curl','--location','--max-time','45','--silent','--show-error','--user-agent','Mozilla/5.0','--output',str(out),'--write-out','%{http_code}\t%{url_effective}',url],capture_output=True,text=True)
    parts=r.stdout.split('\t',1)
    with (ROOT/'fetch_log.csv').open('a',newline='') as f:
        csv.writer(f).writerow([name,url,start,parts[0] or '000',parts[1] if len(parts)>1 else '',str(out.relative_to(ROOT)),r.returncode,r.stderr.strip()])
    print(name,parts[0],out.stat().st_size if out.exists() else 0,flush=True)
    return out
if __name__=='__main__':
    with (ROOT/'fetch_log.csv').open('w',newline='') as f: csv.writer(f).writerow(['attempt','url','fetch_time_ET','http_status','effective_url','raw_file','curl_exit','error'])
    for typ in ['receiving','passing']:
        fetch('ngs_'+typ+'_season',f'https://nextgenstats.nfl.com/stats/{typ}/2026/REG/all/ypa' if typ=='passing' else f'https://nextgenstats.nfl.com/stats/{typ}/2026/REG/all/yards')
    fetch('espn_jax_roster','https://www.espn.com/nfl/team/roster/_/name/jax/jacksonville-jaguars')
    for name,url in [
      ('pfr_opp','https://www.pro-football-reference.com/years/2026/opp.htm'),
      ('pfr_jax','https://www.pro-football-reference.com/teams/jax/2026.htm'),
      ('pfr_meyers','https://www.pro-football-reference.com/players/M/MeyeJa01/gamelog/2026/advanced/'),
      ('pfr_washington','https://www.pro-football-reference.com/players/W/WashPa00/gamelog/2026/advanced/'),
      ('pfr_strange','https://www.pro-football-reference.com/players/S/StraBr00/gamelog/2026/advanced/'),
      ('pfr_lawrence','https://www.pro-football-reference.com/players/L/LawrTr00/gamelog/2026/advanced/')]: fetch(name,url,True)
