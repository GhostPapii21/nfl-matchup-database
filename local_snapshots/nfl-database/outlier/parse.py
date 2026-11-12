import sys,re,csv,os
# usage: parse.py GAME AWAY HOME < rows ; appends to csv
game,away,home=sys.argv[1:4]
teams=dict(x.split('=') for x in sys.argv[4:])
out='outlier_props_2026-11-05.csv'
new=not os.path.exists(out)
w=csv.writer(open(out,'a',newline=''))
if new: w.writerow('player,team,opponent,market,line,side,odds_FD,odds_PP,odds_DK,IP,Opp_Rank,L5,L10,H2H,hit_2026,hit_2025,source,notes'.split(','))
n=0
for ln in sys.stdin:
    p=ln.strip().strip('|').split('|')
    if not p or len(p)<8: continue
    if p[0]=='EV+': p=p[1:]
    pl=p[0]; m=re.match(r'(Over|Under) ([\d.]+) (.*)',p[1])
    if not m: continue
    side,line,mk=m.groups(); i=3; od={}
    while i<len(p) and p[i] in('FD','DK','PP'): od[p[i]]=p[i+1]; i+=2
    rest=p[i:]; ip=rest[0]; 
    if re.match(r'\d+(st|nd|rd|th)',rest[1]): rk=rest[1]+' '+rest[2]; rest=rest[3:]
    else: rk=''; rest=rest[1:]
    l5,l10,h2h,s26,s25=rest[:5]
    t=teams.get(pl,''); opp=away if t==home else home
    w.writerow([pl,t,opp,mk,line,side,od.get('FD',''),od.get('PP',''),od.get('DK',''),ip,rk,l5,l10,h2h,s26,s25,'outlier NFL/props (player+market filter)',game+('; PP odds -119 = pick-em/PP line' if 'PP' in od else '')])
    n+=1
print(n)
