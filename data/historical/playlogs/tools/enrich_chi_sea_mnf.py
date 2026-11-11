"""MNF 2026-11-02 CHI@SEA: enrich playlogs/2026_wk9/CHI_SEA.csv with pre-snap score/margin, a defender TAG
(tackler / PBU / sack / INT / flagged defender from ESPN play text + nflverse pbp fields - 'tackler/PBU tag, not coverage'),
nflverse EPA/success, and explosive flags. Writes CHI_SEA_enriched.csv + CHI_SEA_explosives.csv. Read-only on inputs.
Usage: python3 enrich_chi_sea_mnf.py /path/to/play_by_play_2026.parquet"""
import sys, re, pandas as pd, numpy as np
D='/workspace/nfl-database/playlogs/2026_wk9/'
L=pd.read_csv(D+'CHI_SEA.csv')
P=pd.read_parquet(sys.argv[1]); P=P[P.game_id=='2026_08_CHI_SEA'].copy()
P['clock']=P.time.str.lstrip('0').str.replace(r'^:', '0:', regex=True)
L['clock_n']=L.clock.astype(str).str.lstrip('0').str.replace(r'^:', '0:', regex=True)
DEFC=['sack_player_name','half_sack_1_player_name','half_sack_2_player_name','interception_player_name','pass_defense_1_player_name','pass_defense_2_player_name',
      'solo_tackle_1_player_name','solo_tackle_2_player_name','tackle_with_assist_1_player_name','tackle_with_assist_2_player_name','assist_tackle_1_player_name','assist_tackle_2_player_name',
      'forced_fumble_player_1_player_name','qb_hit_1_player_name']
ROLE={'sack_player_name':'sack','half_sack_1_player_name':'sack','half_sack_2_player_name':'sack','interception_player_name':'INT','pass_defense_1_player_name':'PBU','pass_defense_2_player_name':'PBU',
      'forced_fumble_player_1_player_name':'FF','qb_hit_1_player_name':'QBhit'}
def text_tags(t):
    t=str(t); out=[]
    for m in re.finditer(r'INTERCEPTED by ([A-Z][\w\.\'-]+)',t): out.append(f'{m.group(1)} (INT)')
    for m in re.finditer(r'\[([^\]]+)\]',t): out+= [f'{x.strip()} (PBU/hit tag)' for x in m.group(1).split(';')]
    m=re.search(r'for (?:-?\d+ yards?|no gain)[^()]*\(([^)]+)\)',t) or re.search(r'sacked at [^()]*\(([^)]+)\)',t)
    if m: out+= [f'{x.strip()} (tackler)' for x in m.group(1).split(';')]
    for m in re.finditer(r'PENALTY on (CHI|SEA)-([\w\.\'-]+), ([A-Za-z \-]+?),',t): out.append(f'{m.group(1)} {m.group(2)} (flag: {m.group(3)})')
    for m in re.finditer(r'Penalty on (CHI|SEA)-([\w\.\'-]+), ([A-Za-z \-]+?), declined',t): out.append(f'{m.group(1)} {m.group(2)} (flag declined: {m.group(3)})')
    return '; '.join(dict.fromkeys(out))
sec=lambda c: (lambda a: int(a[0] or 0)*60+int(a[1]))(str(c).split(':'))
P['sec']=P.clock.map(sec)
SCRIM=('Rush','Pass Reception','Pass Incompletion','Sack','Passing Touchdown','Rushing Touchdown','Pass Interception Return','Penalty','Fumble Recovery (Opponent)','Fumble Recovery (Own)','Interception Return Touchdown')
def match(r):
    if str(r.type) not in SCRIM: return None
    c=P[(P.qtr==r.q)&(P.posteam==r.off)&P.play_type.isin(['run','pass','no_play','qb_kneel','qb_spike'])].copy()
    if not len(c): return None
    c['d']=(c.sec-sec(r.clock_n)).abs()+np.where(c.yards_gained==r.yds,0,30)
    b=c.sort_values('d').iloc[0]
    return b if b.d<=40 else None
rows=[]; prev=(0,0)
for r in L.itertuples():
    x=match(r)
    pre_hs,pre_aw=prev; prev=(r.hs,r.aw)
    sea_pre,chi_pre=(int(x.posteam_score),int(x.defteam_score))[::(1 if r.off=='SEA' else -1)] if x is not None and pd.notna(x.posteam_score) else (pre_hs,pre_aw)
    tags=[]
    if x is not None:
        for c in DEFC:
            v=x.get(c)
            if isinstance(v,str) and v: tags.append(f"{v} ({ROLE.get(c,'tackler')})")
    tt=text_tags(r.text)
    defense='CHI' if r.off=='SEA' else 'SEA'
    kind=('pass' if re.search(r'Pass|Interception|Sack',str(r.type)) else 'rush' if 'Rush' in str(r.type) else 'other')
    if x is not None and kind=='other' and str(r.type)=='Penalty': kind='penalty (no play)' if x.get('play_type')=='no_play' else str(x.get('play_type'))
    big=''
    yds=r.yds if isinstance(r.yds,(int,np.integer)) else 0
    if str(r.type) in ('Pass Reception','Passing Touchdown') and yds>=20: big='pass20'
    elif str(r.type) in ('Rush','Rushing Touchdown') and yds>=10: big='rush10'
    if big=='' and str(r.type) in ('Pass Reception','Passing Touchdown','Rush','Rushing Touchdown') and yds>=15: big='15+'
    if big and yds>=40: big+='|40+'
    rows.append(dict(off=r.off,defense=defense,q=r.q,clock=r.clock,down=r.down,dist=r.dist,yds=r.yds,type=r.type,
        sea_pre=sea_pre,chi_pre=chi_pre,off_margin_pre=(sea_pre-chi_pre) if r.off=='SEA' else (chi_pre-sea_pre),sea_post=r.hs,chi_post=r.aw,
        epa=None if x is None else x.epa, success=None if x is None else x.success, pass_location=None if x is None else x.get('pass_location'),
        pass_length=None if x is None else x.get('pass_length'), receiver=None if x is None else x.get('receiver_player_name'), rusher=None if x is None else x.get('rusher_player_name'),
        defender_tag_nflverse='; '.join(dict.fromkeys(tags)), defender_tag_text=tt, defender_label='tackler/PBU tag, not coverage', coverage_charted='not charted (no public per-play coverage for this game)',
        explosive=big, text=r.text))
E=pd.DataFrame(rows); E.to_csv(D+'CHI_SEA_enriched.csv',index=False)
X=E[E.explosive!='']; X.to_csv(D+'CHI_SEA_explosives.csv',index=False)
sc=E[E.type.isin(['Rush','Pass Reception','Pass Incompletion','Sack','Passing Touchdown','Rushing Touchdown','Pass Interception Return','Penalty'])]
print('rows',len(E),'scrimmage-type rows',len(sc),'with nflverse match',sc.epa.notna().sum(),'with any defender tag',(sc.defender_tag_text.astype(bool)|sc.defender_tag_nflverse.astype(bool)).sum())
print(X[['defense','q','clock','type','yds','receiver','rusher','pass_location','pass_length','defender_tag_text','explosive']].to_string())
