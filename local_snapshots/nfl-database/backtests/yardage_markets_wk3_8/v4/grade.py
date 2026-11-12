"""Stage B only. Written in Stage A; do not execute until Stage B is authorized.
Slip construction approximates v2: stable player order, disjoint groups of 3–4,
no duplicate player per slip, at most two legs per game; independent product odds.
Exact v2 source was outside the Stage A read boundary.
"""
from pathlib import Path
import argparse
import json
import math
import pandas as pd
ROOT=Path(__file__).resolve().parent

def decimal(price):
    if pd.isna(price) or abs(price)<100:return float('nan')
    return 1+price/100 if price>0 else 1+100/abs(price)

def grade(rows,pbp):
    output=[]
    for _,r in rows.iterrows():
        p=pbp[(pbp.week==r.week)&(pbp.game_id==r.game_id)]
        # No participation means void; zero carries by a participating player is zero.
        ids=['rusher_player_id','receiver_player_id','passer_player_id']
        participates=any((p[c]==r.gsis).any() for c in ids)
        rush=p.loc[p.rusher_player_id==r.gsis,'rushing_yards'].sum()
        rec=p.loc[p.receiver_player_id==r.gsis,'receiving_yards'].sum()
        catches=p.loc[p.receiver_player_id==r.gsis,'complete_pass'].sum()
        value={'rushyds':rush,'recyds':rec,'rushrecyds':rush+rec,'receptions':catches}[r.market]
        # Participation caveat: a player with snaps but zero touches cannot be
        # resolved from PBP alone. Mark unresolved instead of claiming a void.
        status='UNRESOLVED' if not participates else 'PUSH' if value==r.line else 'WIN' if ((value>r.line)==(r.side=='over')) else 'LOSS'
        odds=decimal(r.price)
        pl=10*(odds-1) if status=='WIN' and math.isfinite(odds) else -10 if status=='LOSS' and math.isfinite(odds) else 0 if status=='PUSH' else float('nan')
        output.append({**r.to_dict(),'actual':value,'result':status,'decimal':odds,'pl':pl})
    return pd.DataFrame(output)

def summary(df,keys):
    output=[]
    for key,g in df.groupby(keys,dropna=False):
        keys_tuple=key if isinstance(key,tuple) else (key,)
        settled=g[g.result.isin(['WIN','LOSS'])&g.pl.notna()]
        stake=len(settled)*10
        output.append(dict(zip(keys,keys_tuple))|dict(won=int((settled.result=='WIN').sum()),lost=int((settled.result=='LOSS').sum()),push=int((g.result=='PUSH').sum()),unresolved=int((g.result=='UNRESOLVED').sum()),unpriced=int(g.decimal.isna().sum()),pl=round(settled.pl.sum(),2),roi=round(settled.pl.sum()/stake,4) if stake else None))
    return pd.DataFrame(output).to_string(index=False)

def slips(df):
    out=[]
    for w,g in df.groupby('week'):
        pool=list(g.sort_values(['game','player']).drop_duplicates('player').to_dict('records'))
        while len(pool)>=3:
            selected=[];counts={}
            for r in pool:
                if counts.get(r['game'],0)<2 and math.isfinite(r['decimal']):
                    selected.append(r);counts[r['game']]=counts.get(r['game'],0)+1
                if len(selected)==4:break
            if len(selected)<3:break
            names={r['player'] for r in selected};pool=[r for r in pool if r['player'] not in names]
            unresolved=any(r['result']=='UNRESOLVED' for r in selected)
            lost=any(r['result']=='LOSS' for r in selected)
            odds=math.prod(r['decimal'] for r in selected if r['result']!='PUSH')
            pl=float('nan') if unresolved else -10 if lost else 10*(odds-1)
            out.append(dict(week=w,players=';'.join(r['player'] for r in selected),legs=len(selected),product_decimal=odds,pl=pl))
    return pd.DataFrame(out)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--pbp',type=Path,default=ROOT.parents[2]/'runs/2026-11-02_shared_src/play_by_play_2026.parquet');args=parser.parse_args()
    pb=pd.read_parquet(args.pbp)
    pb=pb[(pb.season_type=='REG')&(pb.two_point_attempt!=1)&pb.play_type.isin(['run','pass'])]
    picks=pd.read_csv(ROOT/'picks.csv');all_quotes=[]
    for w in range(3,9):
        q=pd.read_csv(ROOT/'packs'/f'w{w}'/'props_main.csv')
        q=q.sort_values(['snap','book','candidate_id']).drop_duplicates(['week','game','player','market','side'],keep='last');all_quotes.append(q)
    quotes=pd.concat(all_quotes,ignore_index=True)
    merged=picks.merge(quotes[['week','game','player','market','side','gsis','game_id']],on=['week','game','player','market','side'],validate='one_to_one')
    graded=grade(merged,pb);graded['split']=graded.week.map(lambda w:'train(3-6)' if w<=6 else 'holdout(7-8)')
    baseline=grade(quotes[(quotes.market=='rushyds')&(quotes.side=='under')&(quotes.tier=='main')],pb)
    tickets=slips(graded)
    graded.to_csv(ROOT/'graded_picks.csv',index=False);baseline.to_csv(ROOT/'graded_baseline.csv',index=False);tickets.to_csv(ROOT/'graded_slips.csv',index=False)
    sections=['# Stage B results','PBP cannot establish a zero-touch player’s participation; these rows remain UNRESOLVED. Injury bet-protect cannot be inferred reliably and is not fabricated. Missing/malformed prices are excluded from monetary ROI. Product odds assume independence; same-game correlations are not priced. Exact v2 slip parity was not verifiable under Stage A restrictions.']
    for title,keys in [('By provenance',['tag']),('FLAG legs',['flag']),('By week',['week']),('By market-side',['market','side']),('Train/holdout',['split'])]:sections.extend(['## '+title,'```\n'+summary(graded,keys)+'\n```'])
    sections.extend(['## Baseline: all main rushing unders by week','```\n'+summary(baseline,['week'])+'\n```','## Slips by week','```\n'+(tickets.groupby('week').agg(slips=('pl','size'),priced_settled=('pl','count'),pl=('pl','sum')).to_string() if len(tickets) else 'No eligible slips')+'\n```'])
    (ROOT/'results.md').write_text('\n\n'.join(sections)+'\n')
if __name__=='__main__':main()
