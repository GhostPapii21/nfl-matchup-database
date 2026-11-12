import pandas as pd,openpyxl,re
b=pd.read_csv('/workspace/bet-log.csv'); b=b[b.sport.str.upper().str.contains('NFL',na=False)].copy()
import csv
_r=list(csv.reader(open('/workspace/nfl-sim/bets/pnl_ledger.csv')))
p=pd.DataFrame([row[:11]+[','.join(row[11:])] for row in _r[1:]],columns=_r[0])
wb=openpyxl.load_workbook('/workspace/bet-log.xlsx',read_only=True)
x=pd.DataFrame(list(wb['Tickets'].iter_rows(values_only=True))[1:],columns=list(wb['Tickets'].iter_rows(values_only=True))[0])
meta={}
for r in x.itertuples(): meta[str(r[1])]=dict(placed=r[2],book='FanDuel' if 'FanDuel' in str(r[15]) else '',odds=r[5],stake=r[6],result=r[10],pnl=r[9])
for r in p.itertuples(): meta.setdefault(r.ticket,{}).update(dict(placed=meta.get(r.ticket,{}).get('placed') or r.date,book=r.book,odds=r.odds,stake=(r.stake_cash if float(r.stake_cash or 0)>0 else f'bonus {r.stake_bonus}'),result=r.result,pnl=r.cash_pnl,note=r.note))
def wk(d):
    d=str(d)[:10]
    for w,(a,z) in {5:('2026-10-08','2026-10-12'),6:('2026-10-15','2026-10-19'),7:('2026-10-22','2026-10-26'),8:('2026-10-29','2026-11-02'),3:('2026-09-24','2026-09-28'),4:('2026-10-01','2026-10-05')}.items():
        if a<=d<=z: return w
    return ''
b['leg_odds_or_note']=b.leg_odds
sl=[];oc=[]
for r in b.itertuples():
    m=meta.get(r.bet_id,{})
    if not m:
        for k in meta:
            if r.bet_id.startswith(k[:20]): m=meta[k]
    sl.append(dict(week=wk(m.get('placed','')),placed_et=m.get('placed',''),book=m.get('book',''),ticket=r.bet_id,game=r.game,ticket_odds=r.sub_sgp_odds if pd.notna(r.sub_sgp_odds) else m.get('odds',''),stake=m.get('stake',''),player=r.player,team=r.team,market=r.prop,line=r.line,leg_odds_or_note=r.leg_odds if pd.notna(r.leg_odds) else ''))
    oc.append(dict(week=wk(m.get('placed','')),ticket=r.bet_id,game=r.game,player=r.player,market=r.prop,line=r.line,actual=r.actual,leg_result=r.result,ticket_status=r.ticket_status,ticket_cash_pnl=m.get('pnl',''),source='bet-log.csv + nfl-sim/bets/pnl_ledger.csv + bet-log.xlsx Tickets'))
# tickets in pnl ledger without legs in bet-log
have=set(b.bet_id)
for r in p.itertuples():
    if r.ticket not in have and not any(h.startswith(r.ticket[:20]) for h in have):
        sl.append(dict(week=wk(r.date),placed_et=r.date,book=r.book,ticket=r.ticket,game=r.game,ticket_odds=r.odds,stake=meta[r.ticket]['stake'],player='(legs not itemized in bet-log)',team='',market='',line='',leg_odds_or_note=''))
        oc.append(dict(week=wk(r.date),ticket=r.ticket,game=r.game,player='(ticket level)',market='',line='',actual='',leg_result='',ticket_status=r.result,ticket_cash_pnl=r.cash_pnl,source='nfl-sim/bets/pnl_ledger.csv note: '+str(r.note)))
FIX={'FD1025-BONUS':7,'TNF1029-LEANS':8,'us-nc:01m6e2iw':8,'UNKNOWN-NFL':5}
for L in (sl,oc):
    for d in L:
        if d['week']=='':
            for k,v in FIX.items():
                if str(d['ticket']).startswith(k): d['week']=v
pd.DataFrame(sl).sort_values(['week','placed_et','ticket']).to_csv('slips_placed.csv',index=False)
o=pd.DataFrame(oc).sort_values(['week','ticket']); o.to_csv('outcomes.csv',index=False)
t=o.drop_duplicates('ticket')
t['pnl']=pd.to_numeric(t.ticket_cash_pnl,errors='coerce')
print(t.groupby('week').agg(tickets=('ticket','count'),wins=('ticket_status',lambda s:s.astype(str).str.startswith('Win').sum()),pnl=('pnl','sum')))
print(t[['week','ticket','ticket_status','ticket_cash_pnl']].to_string())
