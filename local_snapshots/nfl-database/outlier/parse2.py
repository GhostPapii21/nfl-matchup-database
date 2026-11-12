import sys,re,csv
game=sys.argv[1]
w=csv.writer(open('outlier_props_2026-11-05.csv','a',newline=''))
n=0
for ln in sys.stdin:
    if '~' not in ln: continue
    t,rest=ln.strip().split('~',1)
    p=rest.strip('|').split('|')
    while p and (p[0].startswith('Team injuries') or p[0]=='EV+'): p=p[1:]
    pl=p[0]; m=re.match(r'(Over|Under) ([\d.]+) (.*)',p[1])
    if not m: continue
    side,line,mk=m.groups(); i=3; od={}
    while i<len(p) and p[i] in('FD','DK','PP'): od[p[i]]=p[i+1]; i+=2
    r=p[i:]; ip=r[0]
    if re.match(r'\d+(st|nd|rd|th)',r[1]): rk=r[1]; opp=r[2]; r=r[3:]
    else: rk=''; opp=''; r=r[1:]
    w.writerow([pl,t,opp,mk,line,side,od.get('FD',''),od.get('PP',''),od.get('DK',''),ip,rk,*r[:5],'outlier NFL/props (player+market filter)',game]); n+=1
print(n)
