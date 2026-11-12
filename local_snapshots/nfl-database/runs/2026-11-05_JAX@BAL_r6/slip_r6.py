"""r6 prop gates + Rico 4-leg slip. Same §7 rule as r5 policy.py (last 4 games played, 0 if no touch), last-2 downgrade, N1 (RB rush over >=60% carry share).
Best price FD/DK/Pinnacle same point; NO_QUOTE if missing. No-vig only where a two-way exists (Pinnacle preferred, else FD). Model p = r2 sim mean (mc/bias/gr) where that exact line was simulated; else NONE. Tiers = flag only."""
import pandas as pd, json
O=pd.read_csv('odds/odds_r6.csv'); BK=['fanduel','draftkings','pinnacle']
L2=json.load(open('../2026-11-05_JAX@BAL_r2/legs.json'))['legs']
dec=lambda a:1+(a/100 if a>0 else 100/-a); imp=lambda a:1/dec(a)
def q(pl,mk,side,pt):
    x=O[(O.player==pl)&(O.side==side)&(O.point==pt)&O.book.isin(BK)&O.market.isin([mk,mk+'_alternate'])]
    return x.groupby('book').price.max().to_dict()
def nv(pl,mk,side,pt):
    for b in ['pinnacle','fanduel','draftkings']:
        a=O[(O.player==pl)&(O.market==mk)&(O.point==pt)&(O.book==b)]
        if set(a.side)>={'Over','Under'}:
            p=imp(a[a.side==side].price.iloc[0]); o=imp(a[a.side!=side].price.iloc[0]); return round(p/(p+o),3),b
    return None,'no two-way'
def mp(pl,mk,side,pt):
    m={'player_reception_yds':'recyds','player_receptions':'rec','player_rush_yds':'rushyds'}[mk]
    for l in L2:
        if l['player']==pl and l['market']==m and l['side']==side.lower() and l['line']==pt: return round(sum(l['p'].values())/3,3)
    return None
# last-4 game logs from r2 pbp (computed this run; Wk8 = 2026_08_IND_JAX)
LOG={'Strange_rec':[7,7,5,2],'Strange_yds':[95,68,44,55],'Strange_h1yds':[49,27,29,55],
 'Wash_yds_wk8':[7,124,64,16],'Wash_yds_noWk8':[40,7,124,64],'Wash_rec_wk8':[1,6,4,1],'Wash_rec_noWk8':[3,1,6,4],
 'Henry_ryds':[102,58,45,53],'Henry_cshare':[.76,.89,.68,.65]}
LEGS=[('Strange 4+ rec (o3.5)','Brenton Strange','player_receptions','Over',3.5,'Strange_rec'),
 ('Strange 5+ rec (o4.5)','Brenton Strange','player_receptions','Over',4.5,'Strange_rec'),
 ('Strange rec yds o35.5','Brenton Strange','player_reception_yds','Over',35.5,'Strange_yds'),
 ('Strange 40+ rec yds (o39.5)','Brenton Strange','player_reception_yds','Over',39.5,'Strange_yds'),
 ('Washington rec yds o63.5 (main)','Parker Washington','player_reception_yds','Over',63.5,'Wash_yds'),
 ('Washington rec yds o59.5','Parker Washington','player_reception_yds','Over',59.5,'Wash_yds'),
 ('Washington rec yds o49.5','Parker Washington','player_reception_yds','Over',49.5,'Wash_yds'),
 ('Washington rec yds o39.5','Parker Washington','player_reception_yds','Over',39.5,'Wash_yds'),
 ('Washington rec yds o29.5','Parker Washington','player_reception_yds','Over',29.5,'Wash_yds'),
 ('Washington rec yds o19.5','Parker Washington','player_reception_yds','Over',19.5,'Wash_yds'),
 ('Washington 5+ rec (o4.5)','Parker Washington','player_receptions','Over',4.5,'Wash_rec'),
 ('Washington 4+ rec (o3.5)','Parker Washington','player_receptions','Over',3.5,'Wash_rec'),
 ('Washington 3+ rec (o2.5)','Parker Washington','player_receptions','Over',2.5,'Wash_rec'),
 ('Henry 40+ rush (o39.5)','Derrick Henry','player_rush_yds','Over',39.5,'Henry_ryds'),
 ('Henry rush o49.5','Derrick Henry','player_rush_yds','Over',49.5,'Henry_ryds'),
 ('Henry rush o59.5','Derrick Henry','player_rush_yds','Over',59.5,'Henry_ryds'),
 ('Henry rush U69.5 (single)','Derrick Henry','player_rush_yds','Under',69.5,'Henry_ryds')]
out=[]
for n,pl,mk,sd,pt,lk in LEGS:
    sh=q(pl,mk,sd,pt); bb=max(sh,key=lambda b:dec(sh[b])) if sh else 'NO_QUOTE'
    hit=(lambda v:v>pt) if sd=='Over' else (lambda v:v<pt)
    keys=[lk+'_noWk8',lk+'_wk8'] if lk.startswith('Wash') else [lk]
    s7=[];l2=[]
    for k in keys:
        v=LOG[k];h=sum(map(hit,v)); s7.append(f"{'PASS' if h>=3 else 'FAIL'} {h}/4 {v}"+(' ['+k.split('_')[-1]+']' if len(keys)>1 else '')); l2.append('OK' if all(map(hit,v[-2:])) else 'DOWNGRADE')
    n1=('OK all 4 >=60% '+str(LOG['Henry_cshare'])) if pl=='Derrick Henry' and sd=='Over' else ('exempt (under)' if pl=='Derrick Henry' else 'n/a')
    p,nb=nv(pl,mk.replace('_alternate',''),sd,pt); m=mp(pl,mk,sd,pt)
    out.append(dict(leg=n,best_book=bb,best_price=sh.get(bb) if sh else None,shop=sh,no_vig=p,no_vig_src=nb,model_p_r2=m,edge_pts=(round((m-p)*100,1) if m and p else None),s7=' | '.join(s7),last2='/'.join(l2),N1=n1,cap130_hit=bool(sh) and sh.get(bb,0)<-130))
D=pd.DataFrame(out); D.to_csv('prop_legs_r6.csv',index=False); pd.set_option('display.width',300); print(D.drop(columns='shop').to_string())
def slip(prices): d=1
for _ in [0]: pass
def comb(ps):
    d=1
    for a in ps: d*=dec(a)
    return round(d,3), round((d-1)*100)
S={'REC: Strange 4+ / Wash o63.5 / JAX 1H -6.5 / Henry 40+ (best)':[-119,-114,-101,-598],
   'same, FanDuel-only prices':[-122,-114,-110,-700],
   'ALT: Strange 40+ yds instead of 4+ rec (best)':[114,-114,-101,-598],
   'ALT FD-only: Strange 40+ yds':[114,-114,-110,-700]}
for k,v in S.items(): print(k,v,'decimal %.3f -> +%d'%comb(v))
