import pandas as pd, numpy as np, json, datetime, os, glob, re
S="/workspace/nfl-database/runs/2026-11-01_shared_src"; R="/workspace/nfl-database/runs"
NOW=datetime.datetime.now(); TS=f"{NOW:%Y-%m-%dT%H:%M}"; RUN_ID="2026-11-01_sun0800"
pbp=pd.read_parquet(f"{S}/play_by_play_2026.parquet"); pbp=pbp[pbp.season_type=="REG"]
pl=pd.read_parquet(f"{S}/players.parquet")[["gsis_id","display_name","position"]]
pos=dict(zip(pl.gsis_id,pl.position)); nm=dict(zip(pl.gsis_id,pl.display_name))
ftn=pd.read_parquet(f"{S}/ftn_charting_2026.parquet")
ab={"LA":"LAR","WAS":"WSH"}; fix=lambda t: ab.get(t,t)
pbp["posteam"]=pbp.posteam.map(fix); pbp["defteam"]=pbp.defteam.map(fix)
GAMES=[("BAL","BUF","1:00 PM"),("TEN","CIN","1:00 PM"),("ARI","DAL","1:00 PM"),("MIN","DET","1:00 PM"),("LV","NYJ","1:00 PM"),("CLE","PIT","1:00 PM"),("ATL","TB","1:00 PM"),("IND","JAX","1:00 PM"),("LAC","LAR","4:05 PM"),("KC","DEN","4:25 PM"),("NE","MIA","4:25 PM"),("PHI","WSH","8:20 PM SNF"),("CHI","SEA","Mon 8:15 PM MNF")]
FULL={"Arizona Cardinals":"ARI","Atlanta Falcons":"ATL","Baltimore Ravens":"BAL","Buffalo Bills":"BUF","Chicago Bears":"CHI","Cincinnati Bengals":"CIN","Cleveland Browns":"CLE","Dallas Cowboys":"DAL","Denver Broncos":"DEN","Detroit Lions":"DET","Indianapolis Colts":"IND","Jacksonville Jaguars":"JAX","Kansas City Chiefs":"KC","Las Vegas Raiders":"LV","Los Angeles Chargers":"LAC","Los Angeles Rams":"LAR","Miami Dolphins":"MIA","Minnesota Vikings":"MIN","New England Patriots":"NE","New York Jets":"NYJ","Philadelphia Eagles":"PHI","Pittsburgh Steelers":"PIT","Seattle Seahawks":"SEA","Tampa Bay Buccaneers":"TB","Tennessee Titans":"TEN","Washington Commanders":"WSH"}
# ---- lines (fresh vs 07:20)
def lines(f):
    L=json.load(open(f)); out={}
    for g,v in L["games"].items():
        a,h=[FULL.get(x) for x in g.split(" @ ")]
        bk=v.get("fanduel") or v.get("draftkings") or v.get("pinnacle")
        if not bk or not a or not h: continue
        sp={o["name"]:o["point"] for o in bk.get("spreads",[])}; to=[o["point"] for o in bk.get("totals",[]) if o["name"]=="Over"]
        out[(a,h)]=dict(home_spread=sp.get([k for k,c in FULL.items() if c==h][0]),total=to[0] if to else None,book="fanduel" if v.get("fanduel") else "dk/pinn")
    return out,L["pulled_et"]
LN,lt=lines(f"{S}/lines_r0810.json")
try: LO,lot=lines(f"{S}/lines_a0720.json")
except Exception: LO,lot={}, None
wx=json.load(open("weather_0810.json"))
inj=json.load(open("espn_injuries_0810.json")); INJ={}
for t in inj.get("injuries",[]):
    code=FULL.get(t.get("displayName"))
    for i in t.get("injuries",[]):
        st=i.get("status"); a=i.get("athlete",{})
        if st in ("Out","Doubtful","Questionable","Injured Reserve"):
            INJ.setdefault(code,[]).append((a.get("displayName"),a.get("position",{}).get("abbreviation"),st,(i.get("shortComment") or "")[:90]))
cov={}
for line in open(f"{S}/sharp_cov_schemes.md"):
    m=re.match(r"\| ([A-Z][\w\. ]+?) \| ([\d\.]+) \| ([\d\.]+) \| ([\d\.]+) \| ([\d\.]+) \|",line)
    if m and m.group(1) in FULL: cov[FULL[m.group(1)]]=tuple(map(float,m.groups()[1:]))
pfr=pd.read_html("/workspace/nfl-sim/mnf12/pfr_def_adv_2026.html")[0]; pfr.columns=[c[1] for c in pfr.columns]
pfr=pfr[pfr.Player!="Player"].copy()
for c in ["Tgt","Cmp","Yds","Yds/Tgt","Rat","Prss","Bltz","Sk","G"]: pfr[c]=pd.to_numeric(pfr[c],errors="coerce")
pfr["Team"]=pfr.Team.replace({"LAR":"LAR","WAS":"WSH"})
PFRT={"ARI":"ARI","ATL":"ATL","BAL":"BAL","BUF":"BUF","CHI":"CHI","CIN":"CIN","CLE":"CLE","DAL":"DAL","DEN":"DEN","DET":"DET","IND":"IND","JAX":"JAX","KC":"KAN","LV":"LVR","LAC":"LAC","LAR":"LAR","MIA":"MIA","MIN":"MIN","NE":"NWE","NYJ":"NYJ","PHI":"PHI","PIT":"PIT","SEA":"SEA","TB":"TAM","TEN":"TEN","WSH":"WAS"}
# ---- profiles
pp=pbp[pbp.play_type.isin(["pass","run"])].copy()
pp["rpos"]=pp.receiver_player_id.map(pos); pp["explo"]=((pp.play_type=="pass")&(pp.yards_gained>=20))|((pp.play_type=="run")&(pp.yards_gained>=10))
f2=ftn[["nflverse_game_id","nflverse_play_id","n_blitzers","n_pass_rushers"]].rename(columns={"nflverse_game_id":"game_id","nflverse_play_id":"play_id"})
pp=pp.merge(f2,on=["game_id","play_id"],how="left")
def side(df,team,key):
    d=df[df[key]==team]; g=d.game_id.nunique(); db=d[d.qb_dropback==1]; ps=d[d.play_type=="pass"]; ru=d[(d.play_type=="run")&(d.qb_scramble!=1)]
    o=dict(games=g,plays_pg=len(d)/g,pass_rate=len(db)/len(d),pass_yds_pg=ps.yards_gained.sum()/g,ypa=ps[ps.pass_attempt==1].yards_gained.mean(),rush_ypc=ru.yards_gained.mean(),rush_yds_pg=ru.yards_gained.sum()/g,
           sack_rate=db.sack.mean(),pressure_proxy=(db.sack.astype(bool)|db.qb_hit.astype(bool)).mean(),explo_pg=d.explo.sum()/g)
    ch=db[db.n_pass_rushers.notna()]; o["blitz_rate_ftn"]=(ch.n_pass_rushers>=5).mean() if len(ch) else np.nan
    third=d[d.down==3]; o["third_conv"]=third.third_down_converted.sum()/max(1,(third.third_down_converted+third.third_down_failed).sum())
    rz=d[d.yardline_100<=20].groupby(["game_id","drive"]).touchdown.max(); o["rz_td"]=rz.mean()
    for P,lab in [("WR","WR"),("TE","TE"),("RB","RB")]:
        t=ps[ps.rpos==P]; o[f"{lab}_tgt_pg"]=len(t)/g; o[f"{lab}_rec_yds_pg"]=t.yards_gained.where(t.complete_pass==1,0).sum()/g; o[f"{lab}_ypt"]=t.yards_gained.where(t.complete_pass==1,0).mean()
    return o
TEAMS=sorted({t for a,h,_ in GAMES for t in (a,h)})
OFF={t:side(pp,t,"posteam") for t in TEAMS}; DEF={t:side(pp,t,"defteam") for t in TEAMS}
for t in TEAMS:
    q=pfr[pfr.Team==PFRT[t]]; db=pp[(pp.defteam==t)&(pp.qb_dropback==1)]
    DEF[t]["pfr_pressure_rate"]=q.Prss.sum()/max(1,len(db)) if q.Prss.notna().any() else np.nan
# shares L3
def usage(t):
    d=pp[pp.posteam==t]; gids=sorted(d.game_id.unique(),key=lambda x:d[d.game_id==x].week.iloc[0])[-3:]; d=d[d.game_id.isin(gids)]
    ps=d[d.play_type=="pass"]; ru=d[(d.play_type=="run")&(d.qb_scramble!=1)]
    ts=ps.receiver_player_id.value_counts(normalize=True).head(5); cs=ru.rusher_player_id.value_counts(normalize=True).head(2)
    return [(nm.get(k,k),pos.get(k,"?"),v) for k,v in ts.items()],[(nm.get(k,k),v) for k,v in cs.items()]
def label(spread):  # spread from this team's view (negative=fav)
    if spread is None: return "UNKNOWN"
    if spread<=-7: return "BLOWOUT FAVORITE"
    if spread<=-3.5: return "MODERATE FAVORITE"
    if spread<3.5: return "TOSS-UP"
    if spread<7: return "MODERATE UNDERDOG"
    return "UNDERDOG (big)"
OL={"T","G","C","OT","OG","OL"}
rows=[]; cards=[f"# NFL Matchup Cards — Sun Nov 1 + Mon Nov 2, 2026 (run {RUN_ID}, built {TS} ET)\n",
 "Sources: nflverse play_by_play_2026 + FTN charting + players (thru Wk8 TNF, pulled 07:09 ET); Sharp Football coverage schemes (data thru Oct 27, pulled 07:09 ET); PFR advanced defense cache (Oct 29, PFR fresh pull 403 today); ESPN injuries API (08:10 ET); The Odds API FanDuel spreads/totals (08:10 ET, vs 07:20 ET); Open-Meteo hourly (08:10 ET); per-game gate runs in runs/2026-11-01_<game>/ (three 100k sims, gate PASS 07:38 ET).",
 "Gaps: NGS route/gap data not refreshed (nextgenstats.nfl.com on hold; nflverse NGS copy thru Wk8 used in per-game runs). WR outside-vs-slot splits allowed are NOT in free pbp, so they're shown as WR combined. ESPN win rates not pulled this run. Pressure rate = PFR pressures/dropbacks (Oct 29) plus a pbp sack+hit proxy.\n"]
gate={}
for d in glob.glob(f"{R}/2026-11-01_*@*/run_manifest.json"):
    m=json.load(open(d)); g=m["game"]; live=[]
    for l in m["legs"]:
        if l["status"]=="PASS":
            ps=[s["legs"].get(l["name"],{}) for s in m["sims"]]
            live.append(f"{l['name']} (FD {l.get('price_fd')}, no-vig {l['no_vig']:.2f}, sim p {np.mean([x.get('p',np.nan) for x in ps]):.2f}, medians {[x.get('median') for x in ps]})")
    gate[g]=(live,len(m["legs"]))
for a,h,ko in GAMES:
    ln=LN.get((a,h),{}); old=LO.get((a,h),{}); hs=ln.get("home_spread"); tot=ln.get("total")
    lab={h:label(hs),a:label(-hs if hs is not None else None)}
    mv=f" (07:20 ET: {old.get('home_spread')}/{old.get('total')})" if old and (old.get("home_spread"),old.get("total"))!=(hs,tot) else " (no move since 07:20 ET)"
    w=wx.get(h,{}); c=[f"\n## {a} @ {h} — {ko} ET",f"**Line (FanDuel {lt} ET):** {h} {hs:+}, total {tot}{mv}. **Script gate:** {h} {lab[h]}, {a} {lab[a]}."]
    if w.get("wind"): c.append(f"**Weather ({w['roof']}):** {min(w['temp']):.0f}–{max(w['temp']):.0f}°F, wind {max(w['wind']):.0f} mph (gusts {max(w['gust']):.0f}), precip chance up to {max(w['pop'])}%."+(" Indoors, so ignore." if w['roof'] in ("dome","indoor") else ""))
    flags=[]
    for o,dd in [(a,h),(h,a)]:
        O,D=OFF[o],DEF[dd]; tu,cu=usage(o); cv=cov.get(dd)
        cbs=pfr[(pfr.Team==PFRT[dd])&(pfr.Pos.isin(["CB","S","FS","SS","DB"]))&(pfr.Tgt>=15)].sort_values("Yds",ascending=False)
        cbl="; ".join(f"{r.Player} ({r.Pos}) {int(r.Tgt)} tgt, {r['Cmp%']}% comp, {r['Yds/Tgt']} YPT, {int(r.Yds)} yds" for _,r in cbs.head(4).iterrows())
        projp=O["plays_pg"]*(1.03 if "UNDERDOG" in lab[o] else 0.98 if "BLOWOUT" in lab[o] else 1)
        prate=min(.72,max(.45,O["pass_rate"]+(0.04 if "UNDERDOG" in lab[o] else -0.04 if "FAVORITE" in lab[o] else 0)))
        patt=projp*prate; ratt=projp*(1-prate)*0.93
        c.append(f"\n**{o} offense vs {dd} defense**")
        c.append(f"- {dd} D allows (per game): WR {D['WR_tgt_pg']:.1f} tgt / {D['WR_rec_yds_pg']:.0f} yds ({D['WR_ypt']:.1f} YPT); TE {D['TE_tgt_pg']:.1f} / {D['TE_rec_yds_pg']:.0f} ({D['TE_ypt']:.1f}); RB rec {D['RB_tgt_pg']:.1f} / {D['RB_rec_yds_pg']:.0f} ({D['RB_ypt']:.1f}); rush {D['rush_yds_pg']:.0f} yds at {D['rush_ypc']:.2f} YPC; {D['explo_pg']:.1f} explosive plays.")
        c.append(f"- {dd} coverage (Sharp): "+(f"man {cv[0]}% / zone {cv[1]}%, MOF closed {cv[2]}% / open {cv[3]}%." if cv else "not found in Sharp table — gap.")+f" Blitz (FTN 5+ rushers) {D['blitz_rate_ftn']:.0%}; pressure (PFR) {D['pfr_pressure_rate']:.0%}; sack+hit proxy {D['pressure_proxy']:.0%}.")
        c.append(f"- {dd} defenders giving up the most yards (PFR, Oct 29): {cbl or 'none with 15+ targets'}.")
        c.append(f"- 3rd down: {o} converts {O['third_conv']:.0%}, {dd} allows {D['third_conv']:.0%}. Red-zone TD per trip: {o} {O['rz_td']:.0%}, {dd} allows {D['rz_td']:.0%}.")
        c.append(f"- Opportunity projection: ~{projp:.0f} plays, ~{patt:.0f} dropbacks, ~{ratt:.0f} RB carries. L3 target shares: "+", ".join(f"{n} ({p}) {s:.0%} ≈ {s*patt*0.93:.1f} tgt" for n,p,s in tu)+". Carries: "+", ".join(f"{n} {s:.0%} ≈ {s*ratt:.0f}" for n,s in cu)+".")
        oinj=[x for x in INJ.get(o,[]) if x[2]!="Injured Reserve"]; olh=[x for x in oinj if x[1] in OL]
        risk=(D['pfr_pressure_rate']>=0.25 or D['blitz_rate_ftn']>=0.33) and (O['sack_rate']>=0.07 or len(olh)>=1)
        if risk: flags.append(f"PANTHERS RULE — {o} QB: {dd} pressure {D['pfr_pressure_rate']:.0%} / blitz {D['blitz_rate_ftn']:.0%}, {o} sack rate {O['sack_rate']:.1%}, OL on report: {', '.join(f'{x[0]} {x[1]} {x[2]}' for x in olh) or 'none'}. Lean unders/checkdowns on {o} pass volume.")
        elif olh: flags.append(f"{o} OL on report: {', '.join(f'{x[0]} {x[1]} {x[2]}' for x in olh)} (sack rate {O['sack_rate']:.1%} vs {dd} pressure {D['pfr_pressure_rate']:.0%}).")
        soft=[]
        if D['WR_ypt']>=9.0: soft.append(f"WR YPT {D['WR_ypt']:.1f}")
        if D['TE_ypt']>=8.0: soft.append(f"TE YPT {D['TE_ypt']:.1f}")
        if D['rush_ypc']>4.4: soft.append(f"run D {D['rush_ypc']:.2f} YPC")
        if D['rush_ypc']<=3.8: flags.append(f"{dd} run suppression ({D['rush_ypc']:.2f} YPC) — cut {o} rush yards.")
        if D['TE_ypt']<=5.5: flags.append(f"{dd} hard on TEs ({D['TE_ypt']:.1f} YPT) — cut {o} TE yards.")
        if soft: c.append(f"- SOFT-MATCHUP FLAG for {o}: {dd} {'; '.join(soft)} (still needs the opportunity gate and game-by-game opponent adjustment before any leg).")
        rows.append(dict(run_ts=TS,run_id=RUN_ID,game=f"{a}@{h}",offense=o,defense=dd,home_spread=hs,total=tot,script_label=lab[o],proj_plays=round(projp,1),proj_dropbacks=round(patt,1),proj_rb_carries=round(ratt,1),
            **{f"def_{k}":(round(v,4) if isinstance(v,float) else v) for k,v in D.items()},**{f"off_{k}":(round(v,4) if isinstance(v,float) else v) for k,v in O.items()},
            man=cv[0] if cv else None,zone=cv[1] if cv else None,mof_closed=cv[2] if cv else None,mof_open=cv[3] if cv else None,panthers_flag=bool(risk),soft_flags="; ".join(soft),
            top_targets=json.dumps([(n,p,round(s,3)) for n,p,s in tu]),top_carries=json.dumps([(n,round(s,3)) for n,s in cu])))
    allinj=[f"{t}: "+", ".join(f"{x[0]} ({x[1]}) {x[2]}" for x in INJ.get(t,[]) if x[2]!="Injured Reserve") for t in (a,h)]
    c.append("\n**Injuries (ESPN 08:10 ET, Out/Doubtful/Questionable):** "+" | ".join(allinj)+". Questionable players get low rungs or a fade, not an automatic cut.")
    gk=f"{a}@{h}"
    if gk in gate:
        lv,n=gate[gk]; c.append(f"**Gate-passed legs (07:38 ET gate, {n} legs graded):** "+("; ".join(lv) if lv else "none — every leg was cut."))
    else: c.append("**Gate-passed legs:** none yet. No player-prop run for this game (MNF added this run); props need a full run before Monday.")
    c.append("**Caution flags:** "+(" ".join(flags) if flags else "none beyond the standard rules."))
    cards+=c
open(f"/workspace/nfl-database/cards/2026-11-01_sun0800.md","w").write("\n".join(cards)+"\n")
df=pd.DataFrame(rows); mf="/workspace/nfl-database/matchup_master.csv"
before=sum(1 for _ in open(mf))-1 if os.path.exists(mf) else 0
if os.path.exists(mf):
    old=pd.read_csv(mf,nrows=0).columns.tolist(); df=df.reindex(columns=old+[c for c in df.columns if c not in old])
df.to_csv(mf,mode="a",header=not os.path.exists(mf),index=False)
with open("/workspace/nfl-database/matchup_master.jsonl","a") as fh:
    for r in rows: fh.write(json.dumps(r,default=str)+"\n")
print("rows",len(rows),"before",before)
