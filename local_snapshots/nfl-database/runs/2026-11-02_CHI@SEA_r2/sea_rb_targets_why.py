import pandas as pd,re
p=pd.read_parquet('tools/sim_v6_fix/sim_v6_src/play_by_play_2026.parquet')
f=pd.read_parquet('runs/2026-11-02_CHI@SEA_r2/src/ftn_charting_2026.parquet')[['nflverse_game_id','nflverse_play_id','n_blitzers','is_play_action','is_screen_pass']]
f.columns=['game_id','play_id','nbl','pa','scr']; p=p.merge(f,on=['game_id','play_id'],how='left')
pl=pd.read_parquet('runs/2026-11-02_CHI@SEA_r2/src/players.parquet'); rb=set(pl[pl.position.isin(['RB','FB'])].gsis_id)
sh={}
for l in open('runs/2026-11-01_shared_src/sharp_cov_schemes.md'):
    m=re.match(r'\| \[?([A-Z][A-Za-z0-9 .]+?)\]?(\(.*?\))? \| ([\d.]+) \| ([\d.]+) \|',l)
    if m: sh[m.group(1).split()[-1]]=float(m.group(3))
nick={'LAC':'Chargers','SF':'49ers','KC':'Chiefs','ARI':'Cardinals','PIT':'Steelers','NO':'Saints','TB':'Buccaneers','HOU':'Texans','WAS':'Commanders','LA':'Rams','JAX':'Jaguars','CAR':'Panthers','NE':'Patriots','ATL':'Falcons','NYJ':'Jets','MIN':'Vikings','PHI':'Eagles','GB':'Packers','SEA':'Seahawks','CHI':'Bears','DEN':'Broncos','DAL':'Cowboys','DET':'Lions','NYG':'Giants','LV':'Raiders','MIA':'Dolphins','BUF':'Bills','BAL':'Ravens','CIN':'Bengals','CLE':'Browns','IND':'Colts','TEN':'Titans'}
db=p[(p.qb_dropback==1)]
db=db.assign(rbt=(db.pass_attempt==1)&db.receiver_player_id.isin(rb),blz=db.nbl>=5,prs=(db.qb_hit==1)|(db.sack==1))
def game_rows(off):
    out=[]
    for (w,opp),g in db[db.posteam==off].groupby(['week','defteam']):
        r=g[g.rbt]
        out.append(dict(wk=w,opp=opp,qb=g.passer_player_name.mode().iat[0] if g.passer_player_name.notna().any() else '',db=len(g),rb_tgt=len(r),rate=round(len(r)/len(g),3),rec=int(r.complete_pass.sum()),yds=int(r.receiving_yards.fillna(0).sum()),
          backs=r.receiver_player_name.value_counts().to_dict(),blitz=round(g.blz.mean(),3),press=round(g.prs.mean(),3),trail_share=round((g.score_differential<0).mean(),2),
          rb_tgt_trailing=int((r.score_differential<0).sum()),rb_3rd=int((r.down==3).sum()),rb_scr=int(r.scr.fillna(0).sum()),rb_pa=int(r.pa.fillna(0).sum()),rb_blz=int(r.blz.sum()),
          rb_scores=list(r.score_differential.astype(int)),opp_man_season=sh.get(nick.get(opp,''))))
    return pd.DataFrame(out)
S=game_rows('SEA'); 
rb_vs_chi=db[(db.defteam=='CHI')]
C=[]
for (w,o),g in rb_vs_chi.groupby(['week','posteam']):
    r=g[g.rbt];C.append(dict(wk=w,off=o,db=len(g),rb_tgt=len(r),rec=int(r.complete_pass.sum()),yds=int(r.receiving_yards.fillna(0).sum()),backs=r.receiver_player_name.value_counts().to_dict(),
      chi_blitz=round(g.blz.mean(),3),chi_press=round(g.prs.mean(),3),off_trail_share=round((g.score_differential<0).mean(),2),rb_scr=int(r.scr.fillna(0).sum()),rb_3rd=int((r.down==3).sum()),rb_trailing=int((r.score_differential<0).sum()),rb_yac=int(r.yards_after_catch.fillna(0).sum())))
C=pd.DataFrame(C)
T=db[(db.posteam=='SEA')&db.rbt][['week','defteam','qtr','score_differential','down','ydstogo','air_yards','pass_location','nbl','blz','qb_hit','sack','scr','pa','shotgun','receiver_player_name','complete_pass','receiving_yards']]
pd.set_option('display.width',250)
print(S.to_string());print(C.to_string())
s=db[db.posteam=='SEA'];
for k,m in [('trailing',s.score_differential<0),('leading/tied',s.score_differential>=0),('3rd down',s.down==3),('blitz5+',s.blz),('no blitz',~s.blz),('pressured',s.prs)]:
    print(k, len(s[m]), round(s[m].rbt.mean(),3))
c=db[db.defteam=='CHI'];print('CHI blitz',round(c.blz.mean(),3),'press',round(c.prs.mean(),3),'| league blitz',round(db.blz.mean(),3),'press',round(db.prs.mean(),3))
S.to_csv('/tmp/S.csv');C.to_csv('/tmp/C.csv');T.to_csv('/tmp/T.csv')
