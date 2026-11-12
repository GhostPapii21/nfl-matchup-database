import json,sqlite3,pandas as pd,numpy as np
B='/workspace/nfl-database';D=B+'/week8/defense'
J=json.load(open(D+'/defense_profiles.json'));T=J['teams']
fx=lambda t:{'WSH':'WAS','LAR':'LA'}.get(t,t)
c=sqlite3.connect(B+'/fixes/fixes.sqlite')
role=pd.read_sql('select * from fix_player_role where last_played_week>=6',c)
inj=pd.read_parquet(B+'/fixes/src/injuries_2026.parquet');inj=inj[inj.week==8]
inj=inj.fillna('');injd={r.gsis_id:f"report {r.report_status or '—'} / practice {r.practice_status or '—'} ({r.report_primary_injury or r.practice_primary_injury or 'n/a'})" for r in inj.itertuples()}
ngr=pd.read_parquet(D+'/raw/ngs_receiving.parquet');ngr=ngr[(ngr.season==2026)&(ngr.week==0)].set_index('player_gsis_id')
ngu=pd.read_parquet(D+'/raw/ngs_rushing.parquet');ngu=ngu[(ngu.season==2026)&(ngu.week==0)].set_index('player_gsis_id')
ngp=pd.read_parquet(D+'/raw/ngs_passing.parquet');ngp=ngp[(ngp.season==2026)&(ngp.week==0)]
fp=pd.read_csv(D+'/power_rankings_flex_ppr.csv');fpr={str(r.Player).replace('start/sit →','').replace('start/sit','').strip():int(r['#']) for _,r in fp.iterrows()}
qbr=pd.read_sql('select * from fix_qb_rushing',c)
db=sqlite3.connect(B+'/repo/data/nfl_matchups.sqlite')
rc=pd.read_sql('select team_id,count(*) n,max(week) w from ngs_route_charts group by 1',db); cc=pd.read_sql('select team_id,count(*) n,max(week) w from ngs_carry_charts group by 1',db)
f1=lambda x:'—' if x is None or (isinstance(x,float) and np.isnan(x)) else f'{x:.1f}'
def soft(t):
    d=T[t];s=d['sharp'];r=d['ranks'];S=[];H=[]
    if s['YPT Allowed Outside']>=10.5 or r['sh_out']<=8: S.append(('soft for outside WRs',f"Sharp outside YPT {s['YPT Allowed Outside']} (rank {r['sh_out']}/32 most allowed{'; ≥10.5 model trigger' if s['YPT Allowed Outside']>=10.5 else ''}); pbp L/R-location WR proxy {f1(d['WR_outside_proxy']['ypt'])} YPT, {f1(d['WR_outside_proxy']['yds_pg'])} yds/g",'WR'))
    if r['sh_slot']<=8: S.append(('soft for slot',f"Sharp slot YPT {s['YPT Allowed Slot']} (rank {r['sh_slot']}/32); pbp middle-location WR proxy {f1(d['WR_middle_proxy']['ypt'])} YPT",'WR'))
    if s['YPT Allowed WR']>=9.0: S.append(('soft for volume WRs (capped boost)',f"Sharp WR YPT {s['YPT Allowed WR']} (≥9.0 trigger); WRs {f1(d['WR']['rec_pg'])} rec/{f1(d['WR']['yds_pg'])} yds per game allowed (rank {r['WR_yds_pg']})",'WR'))
    if s['YPT Allowed TE']>=8.0 or (r['TE_yds_pg']<=6 and r['sh_te']<=12): S.append(('soft for TEs',f"Sharp TE YPT {s['YPT Allowed TE']} (rank {r['sh_te']}{'; ≥8.0 trigger' if s['YPT Allowed TE']>=8 else ''}); TEs {f1(d['TE']['tgt_pg'])} tgt/{f1(d['TE']['rec_pg'])} rec/{f1(d['TE']['yds_pg'])} yds per game (yds rank {r['TE_yds_pg']})",'TE'))
    if d['RB_rush']['ypc']>4.4: S.append(('good RB rushing environment',f"RB YPC allowed {d['RB_rush']['ypc']:.2f} (>4.4 trigger, rank {r['RB_ypc']}); {f1(d['RB_rush']['yds_pg'])} RB rush yds/g; RB 10+ runs allowed {d.get('explosives_allowed_pg',{}).get('rb_explosive_rush10')}/g",'RB'))
    if r['sh_rb']<=8 or r['RB_rec_pg']<=6: S.append(('soft for rush-receive RBs',f"Sharp RB YPT {s['YPT Allowed RB']} (rank {r['sh_rb']}); RBs {f1(d['RB']['tgt_pg'])} tgt/{f1(d['RB']['rec_pg'])} rec/{f1(d['RB']['yds_pg'])} rec yds per game (rec rank {r['RB_rec_pg']}); RB rush+rec {f1(d['RB_total_yds_pg'])} yds/g (rank {r['RB_total']})",'RB'))
    if s['YPT Allowed TE']<=5.5: H.append(f"HARD for TEs: Sharp TE YPT {s['YPT Allowed TE']} (≤5.5 cut trigger)")
    if d['RB_rush']['ypc']<=3.8: H.append(f"RUN SUPPRESSION: RB YPC allowed {d['RB_rush']['ypc']:.2f} (≤3.8 trigger)")
    if r['sh_out']>=25: H.append(f"Hard outside: Sharp outside YPT {s['YPT Allowed Outside']} (rank {r['sh_out']}/32)")
    if r['sh_slot']>=25: H.append(f"Hard slot: Sharp slot YPT {s['YPT Allowed Slot']} (rank {r['sh_slot']}/32)")
    if r['sh_wr']>=25: H.append(f"Hard vs WRs overall: Sharp WR YPT {s['YPT Allowed WR']} (rank {r['sh_wr']}/32)")
    return S,H
def cands(off,P,n=3):
    x=role[(role.team==off)&(role.position==P)].copy()
    k='current_carry_share_l3' if P=='RB' else 'current_target_share_l3'
    x=x.sort_values(k,ascending=False).head(n);L=[]
    for r in x.itertuples():
        ng='';
        if r.gsis_id in ngr.index: g=ngr.loc[r.gsis_id]; ng+=f"; NGS sep {g.avg_separation:.1f}, cushion {g.avg_cushion:.1f}, YACOE {g.avg_yac_above_expectation:+.1f}, catch% {g.catch_percentage:.0f}"
        if P=='RB' and r.gsis_id in ngu.index: g=ngu.loc[r.gsis_id]; ng+=f"; NGS RYOE/att {g.rush_yards_over_expected_per_att:+.2f}, 8+ box {g.percent_attempts_gte_eight_defenders:.0f}%, eff {g.efficiency:.2f}"
        L.append(f"{r.player} ({P}) — L3 tgt share {100*r.current_target_share_l3:.0f}%, L3 carry share {100*r.current_carry_share_l3:.0f}%, L3 snap {100*r.current_snap_pct_l3:.0f}%, {r.targets_per_game:.1f} tgt/g, {r.carries_per_game:.1f} car/g ({r.games_played} GP){ng}; FP flex rank {fpr.get(r.player,'—')}; Wk8 inj: {injd.get(r.gsis_id,'not listed')}")
    return L
def prof(t):
    d=T[t];s=d['sharp'];r=d['ranks'];e=d.get('explosives_allowed_pg',{})
    return f"""| Metric | Value | Rank (1 = most allowed) |
|---|---|---|
| Sharp YPT WR / TE / RB | {s['YPT Allowed WR']} / {s['YPT Allowed TE']} / {s['YPT Allowed RB']} | {r['sh_wr']} / {r['sh_te']} / {r['sh_rb']} |
| Sharp YPT Outside / Slot | {s['YPT Allowed Outside']} / {s['YPT Allowed Slot']} | {r['sh_out']} / {r['sh_slot']} |
| Man / Zone / MOFC / MOFO % | {s['Man Rate']} / {s['Zone Rate']} / {s['Middle Closed Rate']} / {s['Middle Open Rate']} | |
| Blitz % (Sharp) / FTN blitz % (n={d['ftn_charted_db']}) | {s['Blitz Rate']} / {f1(d['ftn_blitz_rate'])} | {r['blitz']} (1 = most blitz) |
| Light / Heavy box %, Sub % | {s['Light Box Rate']} / {s['Heavy Box Rate']}, {s['Sub Package Rate']} | |
| Pressure rate proxy (opp. Sharp pressure-allowed avg) | {f1(d['sharp_def_pressure_rate_proxy'])}% | {r['press']} (1 = most pressure) |
| ESPN pass-rush win rate (team, thru wk6) | {d.get('defense.pass_rush_win_rate_pct')} | |
| Sack % / hit+sack % per dropback (pbp) | {f1(d['sack_rate'])} / {f1(d['qb_hit_plus_sack_rate_proxy'])} | |
| WR tgt / rec / yds per g (pbp) | {f1(d['WR']['tgt_pg'])} / {f1(d['WR']['rec_pg'])} / {f1(d['WR']['yds_pg'])} | yds {r['WR_yds_pg']} |
| WR outside-proxy (L/R) YPT, middle-proxy YPT | {f1(d['WR_outside_proxy']['ypt'])}, {f1(d['WR_middle_proxy']['ypt'])} | {r['out_ypt']}, {r['mid_ypt']} |
| TE tgt / rec / yds per g | {f1(d['TE']['tgt_pg'])} / {f1(d['TE']['rec_pg'])} / {f1(d['TE']['yds_pg'])} | rec {r['TE_rec_pg']}, yds {r['TE_yds_pg']} |
| RB rec tgt / rec / yds per g | {f1(d['RB']['tgt_pg'])} / {f1(d['RB']['rec_pg'])} / {f1(d['RB']['yds_pg'])} | rec {r['RB_rec_pg']} |
| RB rush car / yds per g, YPC | {f1(d['RB_rush']['car_pg'])} / {f1(d['RB_rush']['yds_pg'])}, {d['RB_rush']['ypc']:.2f} | ypc {r['RB_ypc']} |
| RB rush+rec yds per g | {f1(d['RB_total_yds_pg'])} | {r['RB_total']} |
| Explosives/g: WR 20+ rec, TE 20+, RB 10+ run, RB 20+ rec, stuffs | {e.get('wr_explosive_rec20')}, {e.get('te_explosive_rec20')}, {e.get('rb_explosive_rush10')}, {e.get('rb_explosive_rec20')}, {e.get('run_stuffs_le0')} | |
| 3rd-down % allowed / RZ TD % allowed (trips) | {f1(d['third_down_pct_allowed'])} / {f1(d['rz_td_pct_allowed'])} ({d['rz_trips']}) | {r['third']} / {r['rz']} |
| EPA/play allowed (pbp) | {d['epa_play_allowed']:+.3f} | {r['epa']} |
| Games in sample | {d['games']} | |
"""
def qbline(off):
    q=ngp[ngp.team_abbr==off].sort_values('attempts',ascending=False).head(1)
    o=T[off]; s=''
    if len(q): q=q.iloc[0]; s=f"{q.player_display_name}: NGS TTT {q.avg_time_to_throw:.2f}s, aggressiveness {q.aggressiveness:.1f}%, CPOE {q.completion_percentage_above_expectation:+.1f}, IAY {q.avg_intended_air_yards:.1f}. "
    return s+f"Offense EPA/dropback vs blitz {o['off_epa_vs_blitz']:+.2f} vs no blitz {o['off_epa_no_blitz']:+.2f} (FTN; blitzed on {o['off_blitz_faced']:.0f}% of charted dropbacks); sack% allowed {o['off_sack_rate_allowed']:.1f}; Sharp pressure-allowed avg {f1(o['sharp_off_pressure_allowed_avg'])}%; ESPN pass-block win rate {o.get('offense.pass_block_win_rate_pct')}."
summary=[]
for g in J['games']:
    A,H=fx(g['away']),fx(g['home'])
    md=[f"# {g['away']} @ {g['home']} — Week 8, {pd.Timestamp(g['date']).tz_convert('America/New_York'):%a %b %d %I:%M %p} ET (ESPN {g['id']})\n",
        f"ESPN odds (scoreboard, retrieved 2026-10-29 ~05:08 ET): {g['odds'][0] if g['odds'] else 'n/a'}, O/U {g['odds'][1] if g['odds'] else 'n/a'}. Records {g['away']} {g['awayrec']}, {g['home']} {g['homerec']}.\n"]
    for dfn,off in [(H,A),(A,H)]:
        S,Hd=soft(dfn)
        md.append(f"\n## {dfn} DEFENSE (faced by {off} offense)\n\n"+prof(dfn))
        md.append("\n### Soft spots\n"+("\n".join(f"- **{l}** — {e}" for l,e,_ in S) or "- None met the model triggers / top-8 rank screens.\n"))
        md.append("\n### Hard spots\n"+("\n".join(f"- {h}" for h in Hd) or "- None flagged."))
        md.append(f"\n### Blitz/pressure vs {off} QB\n- {dfn} blitz {T[dfn]['sharp']['Blitz Rate']}% (Sharp), pressure proxy {f1(T[dfn]['sharp_def_pressure_rate_proxy'])}%.\n- {qbline(off)}"+("\n- **Panthers QB CAUTION rule applies (CAR offense).**" if off=='CAR' else "")+(f"\n- Heavy-blitz defense (rank {T[dfn]['ranks']['blitz']}): trigger = cut main-receiver volume, boost check-down roles." if T[dfn]['ranks']['blitz']<=6 else ""))
        md.append(f"\n### {off} candidates fitting the soft spots (opportunity evidence)")
        seen=set()
        for l,e,P in S:
            if P in seen: continue
            seen.add(P); md.append(f"\n*{P} ({', '.join(x for x,_,p in S if p==P)})*\n"+"\n".join("- "+x for x in cands(off,P)))
        if not S: md.append("\n- No soft-spot candidates (no triggers).")
        summary.append((f"{g['away']}@{g['home']}",f"{dfn} D vs {off}","; ".join(l for l,_,_ in S) or "—","; ".join(h.split(':')[0] for h in Hd) or "—"))
    # 10G
    ea,eh=T[A]['sharp_game_epa_series'],T[H]['sharp_game_epa_series']
    md.append(f"\n## Game-script lean (Phase 10G)\n- Evidence: spread {g['odds'][0] if g['odds'] else 'n/a'}; Sharp game EPA/play mean {A} {np.mean(ea):+.2f} (n={len(ea)}), {H} {np.mean(eh):+.2f} (n={len(eh)}); pbp offense EPA/play {A} {T[A]['off_epa_play']:+.3f}, {H} {T[H]['off_epa_play']:+.3f}; defense EPA allowed {A} {T[A]['epa_play_allowed']:+.3f}, {H} {T[H]['epa_play_allowed']:+.3f}.\n- **No formal 10G class assigned**: the script supplies no numeric thresholds and no validated method; stakes/motivation evidence not collected. Descriptive lean only: favorite per market = {g['odds'][0].split()[0] if g['odds'] and g['odds'][0] else 'n/a'}. Underdog-side volume legs need the reviewed exception before use.\n")
    md.append(f"\n## Data notes\n- NGS route charts in DB: {A} {rc[rc.team_id==A].n.sum()} / {H} {rc[rc.team_id==H].n.sum()}; carry charts {A} {cc[cc.team_id==A].n.sum()} / {H} {cc[cc.team_id==H].n.sum()} (indexes only; images not re-read here).\n- See SOURCES.md for URLs/timestamps and gaps.\n")
    open(f"{D}/{g['away']}_at_{g['home']}.md",'w').write("\n".join(md))
S=["# Week 8 Sunday soft-spot overview\n\nRank 1 = most allowed. Triggers from PHASE_SCRIPT (Outside YPT ≥10.5, WR ≥9.0, TE ≥8.0, TE ≤5.5 hard, RB YPC >4.4 / ≤3.8) plus labeled rank screens (top-8 most allowed). Opportunity evidence is in each game file; a soft spot is NOT a bet without the opportunity gate.\n","| Game | Defense (vs offense) | Soft spots | Hard spots |","|---|---|---|---|"]
S+= [f"| {a} | {b} | {c} | {d} |" for a,b,c,d in summary]
open(D+'/SUMMARY.md','w').write("\n".join(S)+"\n")
print("\n".join(S))
