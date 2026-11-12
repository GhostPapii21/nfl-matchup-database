"""Frozen selection and slip construction; no outcomes used."""
import json
from pathlib import Path
import pandas as pd
HERE=Path(__file__).resolve().parent

def passing(df,sharp=False):
 rules=json.loads((HERE/'locked_rules.json').read_text());mask=pd.Series(False,index=df.index)
 for r in rules:
  mask|=(df.market==r['market'])&(df.side==r['side'])&(df.tier==r['tier'])&(df.form_edge>=r['min_form_edge'])
 z=df[mask].copy()
 # Sharp ON is a labeled hindsight sensitivity filter, fixed before holdout.
 if sharp:z=z[(z.side=='over')&(z.HINDSIGHT_sharp_man>=30)|(z.side=='under')&(z.HINDSIGHT_sharp_man<30)]
 return z.sort_values(['week','form_edge','price','candidate_id'],ascending=[True,False,False,True]).drop_duplicates(['week','player'])

def slips(df):
 out=[]
 for week,z in df.groupby('week',sort=True):
  pool=z.to_dict('records');number=0
  while pool:
   chosen=[];counts={}
   for r in pool:
    if counts.get(r['game_id'],0)<2:
     chosen.append(r);counts[r['game_id']]=counts.get(r['game_id'],0)+1
    if len(chosen)==4:break
   if len(chosen)<3:break
   number+=1;out.append((week,number,chosen));used={r['candidate_id'] for r in chosen};pool=[r for r in pool if r['candidate_id'] not in used]
 return out
