"""Week 8 (Nov 1) replay of Rico's four rules (2026-11-02). Read-only over runs/2026-11-01_* + shared_src inputs."""
import json, glob, os, sys, ast, collections
import pandas as pd
DB="/workspace/nfl-database/"; SH=DB+"runs/2026-11-01_shared_src/"; sys.path.insert(0,DB+"tools"); import rico4_rules as R4
lab=lambda x:x
P=pd.read_parquet(SH+"play_by_play_2026.parquet",columns=["week","posteam","pass_attempt","qb_dropback","passer_player_id","passer_player_name","receiver_player_name","receiver_player_id","season_type"])
P=P[(P.season_type=="REG")&(P.week<8)]
POS=dict(zip(*pd.read_parquet(SH+"players.parquet",columns=["gsis_id","position"]).values.T))
SIMS=json.load(open(SH+"sims_final.json"))["sims"]; LEGS=json.load(open(SH+"legs_final.json"))["legs"]
b6=pd.read_csv(DB+"backtests/rico_common/b6_legs.csv"); h100=pd.read_csv(DB+"backtests/rico_common/b5_100plus.csv"); h100=h100[h100.week==8]
imp=lambda o:(100/(o+100)) if o>0 else (-o/(-o+100))
def starters(team):
    d=P[(P.posteam==team)&(P.qb_dropback==1)]; return d.groupby("week").passer_player_id.agg(lambda x:x.value_counts().index[0]).to_dict()
out=collections.defaultdict(list)
man={}
for f in sorted(glob.glob(DB+"runs/2026-11-01_*/run_manifest.json")):
    run=f.split("/")[-2]
    for l in json.load(open(f))["legs"]: man[(run,l["name"])]=l
# R1
for _,r in b6[b6.press=="PRESS"].iterrows():
    l=man.get((r.run,r.leg),{}); cr=l.get("cut_reasons") or ([r.cut] if isinstance(r.cut,str) else [])
    items=[x.strip() for c in cr for x in str(c).split(":",1)[-1].split("; ")] if cr else []
    p14=all(str(c).startswith("P14") for c in cr) and cr
    ok=r.status=="CUT" and p14 and items and all(R4.MR_RX.search(x) for x in items)
    out["R1"].append(dict(run=r.run,leg=r.leg,gate_status=r.status,new="MANUAL_REVIEW" if ok else r.status,reasons="; ".join(cr)[:160] or "(none logged)",actual=r.actual,hit_full=r.hit_full))
# R2
def leg_src(l):
    c=[x for x in LEGS if x["player"]==l.get("player") and x["market"]==l.get("market")]; return c[0] if c else None
for (run,n),l in man.items():
    if l.get("side")!="under" or l.get("status")!="CUT": continue
    el=[c for c in l.get("cut_reasons",[]) if R4.mirror_eligible(c)]
    if not el: continue
    src=leg_src(l); res=dict(run=run,under=n,reasons="; ".join(el)[:140])
    if not src: res["mirror"]="no legs_final row"; out["R2"].append(res); continue
    k=f"{src['player']}|{src['market']}"; sm=SIMS.get(k)
    alts=src["alts"] if isinstance(src["alts"],dict) else ast.literal_eval(src["alts"] or "{}"); fd=src["fd"]
    rungs=[]
    for ln in sorted({float(fd["point"])}|{float(a) for a in alts}):
        kk=str(float(ln))
        if not sm or not all(kk in sm["sims"][m]["rungs"] for m in ("mc","bias","gr")): continue
        pr=fd["over"] if ln==float(fd["point"]) else int(alts.get(str(ln)) or alts.get(f"{ln:g}") or 0)
        if not pr: continue
        nvp=fd["nv_over"] if ln==float(fd["point"]) else imp(pr)/fd["overround"]
        rungs.append(dict(line=ln,price=pr,no_vig=nvp,p=[sm["sims"][m]["rungs"][kk] for m in ("mc","bias","gr")],medians=[sm["sims"][m]["median"] for m in ("mc","bias","gr")]))
    c=R4.mirror_over(dict(name=n,side="under",line=l.get("line")),rungs)
    res["mirror"]=(f"Over {c['line']:g} @ {c['price']:+d} (avg p {sum(c['model_p'])/3:.3f}, nv {c['no_vig']:.3f}) -> candidate, still must pass §7/§14/coverage/weather" if c.get("line") is not None else c["no_rung_reason"]+f" ({len(rungs)} rungs checked)")
    out["R2"].append(res)
# R3 pool + R4
teams=sorted({l.get("team") for l in man.values() if l.get("team")})
inman={l.get("player") for l in man.values()}
for t in teams:
    st=starters(t); cq=st[max(st)] if st else None
    x=P[(P.posteam==t)&(P.pass_attempt==1)&P.receiver_player_name.notna()]
    rows=[dict(week=int(w),posteam=t,passer_player_name=q,receiver_player_name=rn) for w,q,rn in zip(x.week,x.passer_player_id,x.receiver_player_name)]
    pos={}; [pos.setdefault(rn,POS.get(pid)) for rn,pid in zip(x.receiver_player_name,x.receiver_player_id)]
    l3=sorted(x.week.unique())[-3:]; tc=x[x.week.isin(l3)].groupby("receiver_player_name").size().sort_values(ascending=False)
    wrk={n:i+1 for i,n in enumerate([n for n in tc.index if pos.get(n)=="WR"])}
    pool=R4.target_share_pool(rows,t,cq,pos,wrk)
    for p_ in pool["players"]:
        full=[pl for pl in inman if pl and pl.split()[-1].rstrip(".")==p_["name"].split(".")[-1].split()[-1] and pl[0]==p_["name"][0]]
        unders_only=full and all(l.get("side")=="under" for l in man.values() if l.get("player") in full)
        out["R3"].append(dict(team=t,name=p_["name"],season=p_["share_season"],l3_cur_qb=p_["share_l3_current_qb"],
            in_pool_before=("yes (unders only)" if unders_only else "yes") if full else "NO -> added"))
    for e in pool["excluded_wr34"]: out["R3x"].append(dict(team=t,name=e["name"],season=e["share_season"],l3=e["share_l3_current_qb"]))
    # R4: qb returned from 2+ missed, or model (last-4 player games) mostly on another QB
    wk=sorted(st); has=[st[w]==cq for w in wk]; i=len(has)
    while i>0 and has[i-1]: i-=1
    miss=0
    while i>0 and not has[i-1]: miss+=1; i-=1
    for (run,n),l in man.items():
        if l.get("team")!=t or l.get("type") not in ("WR","TE"): continue
        pr=x[x.receiver_player_name.notna()]
        rf=(l.get("recent_form") or {}); 
        mq=None
        g4=wk[-4:]; mq=cq if sum(st[w]==cq for w in g4)*2>=len(g4) else "backup"
        if R4.qb_return(l,current_qb=cq,qb_missed_before=miss,model_qb=mq):
            out["R4"].append(dict(run=run,leg=n,team=t,qb_missed=miss,model_qb=mq,status=l.get("status"),recent_form_qb=rf.get("qb")))
for k in ("R1","R2","R3","R3x","R4"):
    df=pd.DataFrame(out[k]); df.to_csv(f"week8_{k}.csv",index=False); print(f"\n== {k} ({len(df)})"); print(df.to_string(max_colwidth=110) if len(df) else "none")
print("\n== Week 8 100+ games vs new pool"); 
pool=pd.DataFrame(out["R3"])
for _,h in h100.iterrows():
    m=pool[pool.name.apply(lambda n:n.split(".")[-1].strip()==h.player.split()[1] and n[0]==h.player[0])] if len(pool) else pool
    print(f"- {h.player} ({h.team}, {h.recyds:.0f} yds): "+(f"pool share season {m.season.iat[0]:.1%} / L3 cur-QB {m.l3_cur_qb.iat[0]:.1%}; {m.in_pool_before.iat[0]}" if len(m) else "not >=22% (or RB / #3-#4 WR)"))
