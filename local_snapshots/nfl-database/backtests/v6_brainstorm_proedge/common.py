"""v6 shared data loaders. AS-OF only: every stats frame is filtered to weeks < target week. No outcomes here."""
import pandas as pd,numpy as np,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent;DB=ROOT.parents[1];V4=DB/'backtests/yardage_markets_wk3_8/v4/packs'
PB26=DB/'runs/2026-11-02_shared_src/play_by_play_2026.parquet';FT26=DB/'runs/2026-11-02_shared_src/ftn_charting_2026.parquet'
PB25=DB/'week8/phase_walk/src/pbp25.parquet';PLAYERS=DB/'runs/2026-11-02_shared_src/players.parquet'
INJ=DB/'fixes/src/injuries_2026.parquet';GAMES=ROOT/'packs/nflverse_games.csv'
MK=['rushyds','recyds','rushrecyds']
def nm(s):return re.sub('[^a-z]','',str(s).lower())
def clean(pb):return pb[(pb.season_type=='REG')&pb.play_type.isin(['run','pass'])&(pb.get('two_point_attempt',0)!=1)]
def prior_pbp(w):
    """Returns (pbp, label). wk1 -> full 2025 REG (prior season, labelled). wk>=2 -> 2026 weeks < w."""
    if w==1:return clean(pd.read_parquet(PB25)),'2025 full regular season (prior season; 2026 roster from players table)'
    if w>=3:pb=pd.read_parquet(V4/f'w{w}/pbp_prior.parquet')
    else:pb=pd.read_parquet(PB26);pb=pb[pb.week<w]
    assert (pb.week<w).all() and (pb.season==2026).all();return clean(pb),f'2026 weeks < {w}'
def prior_ftn(w):
    if w==1:return None
    if w>=3:return pd.read_parquet(V4/f'w{w}/ftn_prior.parquet')
    f=pd.read_parquet(FT26);return f[f.week<w] if 'week' in f else None
def logs(pb):
    """per player-game yardage logs from as-of pbp"""
    r=pb[pb.rush_attempt==1].groupby(['game_id','week','rusher_player_id']).agg(car=('rushing_yards','size'),rush=('rushing_yards','sum')).reset_index().rename(columns={'rusher_player_id':'gsis'})
    c=pb[pb.pass_attempt==1].dropna(subset=['receiver_player_id']).groupby(['game_id','week','receiver_player_id']).agg(tgt=('receiving_yards','size'),rec=('receiving_yards','sum')).reset_index().rename(columns={'receiver_player_id':'gsis'})
    L=r.merge(c,on=['game_id','week','gsis'],how='outer').fillna({'car':0,'rush':0,'tgt':0,'rec':0})
    L['rushyds']=L.rush;L['recyds']=L.rec;L['rushrecyds']=L.rush+L.rec
    tm=pd.concat([pb[['game_id','rusher_player_id','posteam']].rename(columns={'rusher_player_id':'gsis'}),pb[['game_id','receiver_player_id','posteam']].rename(columns={'receiver_player_id':'gsis'})]).dropna().drop_duplicates(['game_id','gsis'])
    qb=pb[pb.pass_attempt==1].groupby(['game_id','posteam']).passer_player_id.agg(lambda s:s.value_counts().index[0]).rename('qb').reset_index()
    L=L.merge(tm,on=['game_id','gsis'],how='left').merge(qb,on=['game_id','posteam'],how='left')
    return L.sort_values('week')
def imp(a):return 100/(a+100) if a>0 else -a/(-a+100)
