"""Week 9 slate + projected script. RERUN DAILY (lines move). Sources: The Odds API (FanDuel price of record, DraftKings compare),
ESPN scoreboard (schedule/venue), nflverse pbp 2026 Wk1-7 + Wk8 TNF (volume). Exploratory research only, no legs."""
import json,glob,datetime,pandas as pd,numpy as np,os
now=datetime.datetime.now()
odds=json.load(open(sorted(glob.glob('raw/odds_*.json'))[-1])); ofile=sorted(glob.glob('raw/odds_*.json'))[-1]
AB={'Arizona Cardinals':'ARI','Atlanta Falcons':'ATL','Baltimore Ravens':'BAL','Buffalo Bills':'BUF','Carolina Panthers':'CAR','Chicago Bears':'CHI','Cincinnati Bengals':'CIN','Cleveland Browns':'CLE','Dallas Cowboys':'DAL','Denver Broncos':'DEN','Detroit Lions':'DET','Green Bay Packers':'GB','Houston Texans':'HOU','Indianapolis Colts':'IND','Jacksonville Jaguars':'JAX','Kansas City Chiefs':'KC','Las Vegas Raiders':'LV','Los Angeles Chargers':'LAC','Los Angeles Rams':'LA','Miami Dolphins':'MIA','Minnesota Vikings':'MIN','New England Patriots':'NE','New Orleans Saints':'NO','New York Giants':'NYG','New York Jets':'NYJ','Philadelphia Eagles':'PHI','Pittsburgh Steelers':'PIT','San Francisco 49ers':'SF','Seattle Seahawks':'SEA','Tampa Bay Buccaneers':'TB','Tennessee Titans':'TEN','Washington Commanders':'WAS'}
p=pd.read_parquet('/workspace/nfl-database/runs/2026-11-01_shared_src/play_by_play_2026.parquet')
sc=p[(p.pass_attempt==1)|(p.rush_attempt==1)]
T=pd.read_csv('team_volume_2026-11-01.csv',index_col=0)
A=sc.groupby('defteam').agg(g=('game_id','nunique'),pa=('pass_attempt','sum'),ru=('rush_attempt','sum')); A['pa_a']=A.pa/A.g; A['ru_a']=A.ru/A.g
LP=T.pa_pg.mean(); LR=T.ru_pg.mean()
RD=pd.read_csv('run_defense_tiers_2026-11-01.csv',index_col=0)
W={}
wf=sorted(glob.glob('weather/WEATHER_*.md'))
if wf:
    for l in open(wf[-1]).read().split('## Pull')[-1].splitlines():
        if l.startswith('| ') and 'Game' not in l and '---' not in l:
            c=[x.strip() for x in l.strip('|').split('|')]; W[c[0]]=c[-1]
SCHED=[('JAX','BAL','2026-11-05 20:15 Thu'),('CIN','ATL','2026-11-08 09:30 Madrid (ATL home)'),('DAL','IND','11-08 13:00'),('NYJ','KC','11-08 13:00'),('DET','MIA','11-08 13:00'),('CLE','NO','11-08 13:00'),('NYG','PHI','11-08 13:00'),('LA','WAS','11-08 13:00'),('DEN','CAR','11-08 13:00'),('HOU','LAC','11-08 16:05'),('LV','SF','11-08 16:25'),('ARI','SEA','11-08 16:25'),('GB','NE','11-08 16:25'),('TB','CHI','11-08 20:20 SNF'),('BUF','MIN','11-09 20:15 MNF')]
def line(a,h):
    for g in odds:
        s={AB[g['home_team']],AB[g['away_team']]}
        if s=={a,h} and g['commence_time']>'2026-11-04':
            r={}
            for b in g['bookmakers']:
                for m in b['markets']:
                    for o in m['outcomes']:
                        k=AB.get(o['name'],o['name']); r[(b['key'],m['key'],k)]=(o.get('point'),o['price'])
            return r
def exp(team,opp,fav):
    pa=T.pa_pg[team]+0.5*(A.pa_a[opp]-LP)-0.064*fav; ru=T.ru_pg[team]+0.5*(A.ru_a[opp]-LR)+0.029*fav
    return pa,ru
rows=[]
for a,h,ko in SCHED:
    L=line(a,h)
    if not L:
        rows.append(dict(game=f'{a}@{h}',ko=ko,fd_spread='MISSING (off board until PHI@WAS SNF settles)',fd_total='MISSING',dk='MISSING'));continue
    fs={t:L.get(('fanduel','spreads',t)) for t in (a,h)}; ft=L.get(('fanduel','totals','Over')); ds={t:L.get(('draftkings','spreads',t)) for t in (a,h)}; dt=L.get(('draftkings','totals','Over'))
    fav=a if fs[a][0]<0 else h; dog=h if fav==a else a; sp=-fs[fav][0]; tot=ft[0]
    ftot=(tot+sp)/2; dtot=(tot-sp)/2
    pf,rf=exp(fav,dog,sp); pd_,rd=exp(dog,fav,-sp)
    q4='HIGH (8.5+; Q4 lead-9+ run rate 72%)' if sp>=8.5 else ('MODERATE (6-8)' if sp>=6 else '-')
    wkey=[k for k in W if k.startswith(f'{a}@{h}') or (a=='CIN' and 'Madrid' in k) or k.startswith(f'{a}@{h.replace("WAS","WSH")}') or k.startswith(f'{a.replace("LA","LAR")}@')]
    wx=W.get(wkey[0],'-') if wkey else 'dome/roof'
    rule=[]
    if sp>=7 and RD.loc[dog,'ypc']>=4.4: rule.append('FAV7+ & opp RB YPC>=4.4')
    if wx not in('-','dome/roof') and 'roof' not in wx: rule.append('WEATHER '+wx)
    rows.append(dict(game=f'{a}@{h}',ko=ko,fd_spread=f'{fav} -{sp}',fd_total=tot,dk=f"{fav} {ds[fav][0]} / {dt[0]}",fav=fav,imp=f'{fav} {ftot:.1f} – {dog} {dtot:.1f}',
        fav_split=f'{100*pf/(pf+rf):.0f}/{100*rf/(pf+rf):.0f}',dog_split=f'{100*pd_/(pd_+rd):.0f}/{100*rd/(pd_+rd):.0f}',fav_att=round(pf,1),dog_att=round(pd_,1),q4=q4,
        dog_rb_ypc_allowed=RD.loc[dog,'ypc'],fav_rb_ypc_allowed=RD.loc[fav,'ypc'],wx=wx,rb_rule=('TRIGGERS: '+'; '.join(rule)) if rule else 'no trigger'))
df=pd.DataFrame(rows); os.makedirs('slate',exist_ok=True); fn=f'slate/SLATE_{now:%Y-%m-%d}.md'
with open(fn,'a') as f:
    f.write(f"\n## Pull {now:%Y-%m-%d %H:%M} ET\nLines: The Odds API ({os.path.basename(ofile)}, pulled 2026-11-01 21:20 ET) — FanDuel = price of record, DraftKings shown for comparison. Schedule/venue: ESPN scoreboard week 9.\n"
      "Script model (exploratory, NOT a sim): exp pass att = team pa/g + 0.5×(opp pass att faced/g − lg) − 0.064×spread (fitted on 216 team-games, 2026 pbp: favorites barely shed attempts pre-Q4); runs same with +0.029×spread. Split = pass/run share of called plays. RB rule = approved BUG-2026-11-01-RBSCRIPT (fav 7+ AND opp RB YPC≥4.4, OR Phase-11 weather flag). Opp RB YPC = RB-only rush YPC allowed, pbp Wk1-7+TNF + Wk8 Sunday ESPN play logs where available.\n\n")
    f.write(df.to_markdown(index=False)); f.write('\n')
print(df.to_markdown(index=False))
