import csv,json
rows=list(csv.reader(open('fd_now.csv')))[1:]
def imp(o): o=float(o); return 100/(o+100) if o>0 else -o/(-o+100)
def find(mk,run):
    for r in rows:
        if r[2]==mk and r[3]==run: return r
L={"Walker 80+ rush":("Kenneth Walker III","Alt Rushing Yds","80+ Yards","Rushing Yds"),
"Puka 8+ rec":("Puka Nacua","Alt Receptions","8+ Receptions","Total Receptions"),
"Puka 70+ yds":("Puka Nacua","Alt Receiving Yds","70+ Yards","Receiving Yds"),
"Lamb 60+ yds":("CeeDee Lamb","Alt Receiving Yds","60+ Yards","Receiving Yds"),
"McBride 7+ rec":("Trey McBride","Alt Receptions","7+ Receptions","Total Receptions"),
"Bowers 6+ rec":("Brock Bowers","Alt Receptions","6+ Receptions","Total Receptions"),
"Metcalf 40+ yds":("DK Metcalf","Alt Receiving Yds","40+ Yards","Receiving Yds"),
"Gibbs 70+ rush":("Jahmyr Gibbs","Alt Rushing Yds","70+ Yards","Rushing Yds"),
"Higgins 5+ rec":("Tee Higgins","Alt Receptions","5+ Receptions","Total Receptions"),
"Higgins 60+ yds":("Tee Higgins","Alt Receiving Yds","60+ Yards","Receiving Yds"),
"Tuten 60+ rush":("Bhayshul Tuten","Alt Rushing Yds","60+ Yards","Rushing Yds"),
"Treadwell 20+ yds":("Laquon Treadwell","Alt Receiving Yds","20+ Yards","Receiving Yds"),
"Treadwell 2+ rec":("Laquon Treadwell","Alt Receptions","2+ Receptions","Total Receptions"),
"A.Williams 3+ rec":("Antonio Williams","Alt Receptions","3+ Receptions","Total Receptions"),
"Downs 3+ rec":("Josh Downs","Alt Receptions","3+ Receptions","Total Receptions"),
"Flournoy 3+ rec":("Ryan Flournoy","Alt Receptions","3+ Receptions","Total Receptions"),
"Cook 70+ rush":("James Cook","Alt Rushing Yds","70+ Yards","Rushing Yds")}
S=json.load(open('g6_sims.json')); legs={l['id']:l for l in json.load(open('legs.json'))}
out=[]
for k,(pn,am,rn,mm) in L.items():
    a=find(f"{pn} - {am}",f"{pn} {rn}"); o=find(f"{pn} - {mm}",f"{pn} Over"); u=find(f"{pn} - {mm}",f"{pn} Under")
    ov=imp(o[5])+imp(u[5]); nv=imp(a[5])/ov
    s=S[k]['sims']; ps=[s[m][0] for m in ('mc','bias','gr')]; avg=sum(ps)/3; sh=0.5+0.7*(avg-0.5)
    raw=(avg-nv)*100; she=(sh-nv)*100; rung=legs[k]['rung']
    med_ok=s['mc'][1]>=rung and s['gr'][1]>=rung
    ok= raw>=3 and raw<=15 and she>0 and min(ps)>=.45 and med_ok
    out.append(dict(leg=k,fd=a[5],main=f"{o[4]} {o[5]}/{u[5]}",nv=round(nv,3),mc=s['mc'],bias=s['bias'],gr=s['gr'],avg=round(avg,3),raw=round(raw,1),pshr=round(sh,3),shr=round(she,1),med_ok=med_ok,edge_pass=ok))
for r in out: print(r)
json.dump(out,open('edges.json','w'),indent=1)
