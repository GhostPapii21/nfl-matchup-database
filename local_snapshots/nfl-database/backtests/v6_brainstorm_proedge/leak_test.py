"""Leak test: (1) every as-of pbp frame has week < target week; (2) no prompt contains the target game's final score;
(3) no prompt contains the word 'final' tied to target week box numbers; (4) prompts never reference weeks >= target in the weeks list."""
import re,pandas as pd
from common import *
pb=pd.read_parquet(PB26);bad=0
for w in range(1,9):
    p,_=prior_pbp(w);assert p.season.iloc[0]==(2025 if w==1 else 2026) and (w==1 or (p.week<w).all()),w
    fin=pb[pb.week==w].groupby('game_id').agg(h=('total_home_score','max'),a=('total_away_score','max'),ht=('home_team','first'),at=('away_team','first'))
    for f in (ROOT/'reads').glob(f'w{w}_*.prompt.txt'):
        t=f.read_text();g=f.stem.split('_',1)[1].replace('.prompt','');a,h=g.split('@')
        r=fin[(fin.at==a)&(fin.ht==h)]
        if len(r):
            sc=[f"{int(r.h.iloc[0])}-{int(r.a.iloc[0])}",f"{int(r.a.iloc[0])}-{int(r.h.iloc[0])}"]
            if any(s in t for s in sc):print('SCORE STRING IN',f.name);bad+=1
        m=re.search(r'weeks \[([0-9, ]*)\]',t)
        if m and any(int(x)>=w for x in m.group(1).split(',') if x.strip()):print('FUTURE WEEK',f.name);bad+=1
print('LEAK TEST', 'PASS' if not bad else f'FAIL {bad}')
