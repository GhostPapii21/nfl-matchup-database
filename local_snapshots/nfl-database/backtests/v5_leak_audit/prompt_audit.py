import re,pandas as pd
from pathlib import Path
ROOT=Path(__file__).resolve().parent;V=ROOT.parent/'yardage_markets_wk3_8';R=V/'v5'/'reads';PK=V/'v4'/'packs'
rows=[]
for w in (7,8):
    pb=pd.read_parquet(PK/f'w{w}'/'pbp_prior.parquet',columns=['week']);pr=pd.read_csv(PK/f'w{w}'/'props_main.csv');gl=pd.read_csv(PK/f'w{w}'/'game_lines.csv')
    ko=pd.to_datetime(pr.kickoff,utc=True);sn=pd.to_datetime(pr.snap,utc=True)
    gk=pd.to_datetime(gl.kickoff,utc=True);gt=pd.to_datetime(gl.timestamp,utc=True)
    rows.append(dict(check=f'w{w} pbp weeks',value=str(sorted(set(pb.week))),leak=int(pb.week.max()>=w)))
    rows.append(dict(check=f'w{w} prop quotes at/after kickoff',value=f'{int((sn>=ko).sum())}/{len(pr)} (min lead {((ko-sn).dt.total_seconds()/3600).min():.2f}h)',leak=int((sn>=ko).any())))
    rows.append(dict(check=f'w{w} game-line quotes at/after kickoff',value=f'{int((gt>=gk).sum())}/{len(gl)}',leak=int((gt>=gk).any())))
    for f in sorted(R.glob(f'w{w}_*.prompt.txt')):
        t=f.read_text();game=f.name.split('_')[1].split('.')[0]
        kick=ko[pr.game==game].min()
        dates=[pd.Timestamp(d,tz='America/New_York') for d in re.findall(r'20\d\d-\d\d-\d\d',t)]
        late=[str(d.date()) for d in dates if pd.notna(kick) and d>=kick.tz_convert('America/New_York').normalize()]
        lw=[int(x) for m in re.findall(r'weeks \[([\d, ]+)\]',t) for x in m.split(',')]
        words=re.findall(r'(?i)\b(final score|won \d|lost \d|postgame|recap|box ?score:|inactive[s]? (?:list|announced)|ruled out .* (?:during|in) the game)\b',t)
        rows.append(dict(check=f.name,value=f'dates>=kickday:{late} L3weeks max:{max(lw) if lw else None} result-words:{words}',leak=int(bool(late) or (lw and max(lw)>=w) or bool(words))))
df=pd.DataFrame(rows);df.to_csv(ROOT/'prompt_audit.csv',index=False);print(df[df.leak==1].to_string() if df.leak.any() else 'CLEAN');print(df.head(6).to_string())
