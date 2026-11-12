import json
b=json.load(open('breakdown.json')); L=b['league_rb_ypc']
def kv(d): return ', '.join(f"{k} {v}" for k,v in d.items()) or 'none'
for g in b['games']:
    a,h=g['game'].split('@'); M=[f"# {g['game']} — Week 8 matchup breakdown\nOdds (ESPN/DK, no prop lines pulled): {g['odds']}. Data Wks1-7 nflverse PBP+FTN, PFR defender stats, Sharp Oct 20, ESPN injuries. No bets/lines.\n"]
    for t,s in g['sides'].items():
        o,d=s['offense'],s['opp_defense']; opp=h if t==a else a
        qbinj=[x for x in o['inj'] if '(QB' in x]
        M.append(f"\n## {t} offense vs {opp} defense\n")
        M.append(f"**Injuries ({t}):** {'; '.join(o['inj']) or 'none listed'}\n")
        if qbinj: M.append(f"**QB NOTE:** {'; '.join(qbinj)} — season QB splits below are for {o['qb']}; confirm starter.\n")
        M.append("### 1. Run game\n| RB | car/g (L3) | car share | YPC | rush TD | direction share | YPC by dir (≥5 car) | tgt/rec/rec yds pg season | L3 |\n|---|---|---|---|---|---|---|---|---|")
        for r in o['rbs']:
            M.append(f"| {r['name']} | {r['car_pg']} ({r['car_pg_l3']}) | {r['car_share']}% | {r['ypc']} | {r['rush_td']} | {kv(r['dir_share'])} | {kv(r['dir_ypc'])} | {r['tgt_pg']}/{r['rec_pg']}/{r['recyds_pg']} | {r['tgt_pg_l3']}/{r['rec_pg_l3']}/{r['recyds_pg_l3']} |")
        M.append(f"\n**{opp} run D vs RBs:** {d['rb_car_pg']} car/g, **{d['rb_ypc_allowed']} YPC allowed** (league {L}), {d['rb_rush_yds_pg']} rush yds/g, **{d['rb_rush_td_pg']} RB rush TD/g** ({d['rb_rush_td_total']} total). RB receiving allowed: {d['rb_tgt_pg']} tgt / {d['rb_rec_pg']} rec / **{d['rb_recyds_pg']} yds per game (rank #{d['rb_recyds_rank_most_allowed']} most of 32)**.")
        M.append(f"By direction (≥8 RB carries; def YPC vs league): " + '; '.join(f"{k} {v['ypc']} (lg {v['lg']}, n={v['car']})" for k,v in d['by_dir'].items()) + f". **Weakest side: {d.get('weak_dir')}**.")
        M.append(f"Front injuries: {'; '.join(d['front_injuries']) or 'none listed'}. Weak individual DT/edge YPC allowed: GAP (no public per-defender run data; direction split is the proxy).\n")
        sh=d['sharp']
        M.append(f"### 2. WR/TE vs coverage\n{opp} coverage (Sharp): Man {sh.get('Man Rate')}% / Zone {sh.get('Zone Rate')}%; YPT allowed WR {sh.get('YPT Allowed WR')}, TE {sh.get('YPT Allowed TE')}, RB {sh.get('YPT Allowed RB')}, Outside {sh.get('YPT Allowed Outside')}, Slot {sh.get('YPT Allowed Slot')}. Allowed per game: WR {d.get('WR_allowed_pg')}, TE {d.get('TE_allowed_pg')}.\n")
        M.append("| Receiver | pos | type | tgt share szn / L3 | tgt/g | aDOT | RZ tgts |\n|---|---|---|---|---|---|---|")
        for p in o['receivers']: M.append(f"| {p['player']} | {p['pos']} | {p['primary']} | {p['tgt_share_season']} / {p['tgt_share_l3']} | {p['tgt_pg']} | {p['adot']} | {p['rz_tgts']} |")
        M.append(f"\n{opp} most-targeted defensive backs (PFR; **alignment GAP**, likely matchups inferred: the top 2 targeted = primary outside CBs, a nickel/slot DB if listed):\n")
        M.append("| DB | gp | tgt/g | rec/g allowed | yds/g allowed | TD |\n|---|---|---|---|---|---|")
        for c in d['cover']: M.append(f"| {c['name']} | {c['gp']} | {c['tgt_pg']} | {c['rec_pg']} | {c['yds_pg']} | {c['td']} |")
        M.append(f"DB injuries: {'; '.join(d['db_injuries']) or 'none listed'}\n")
        M.append("### 2b. Seesaw (inverse correlation, top 3 receivers, Wks1-7)\n")
        for x in o['seesaw']: M.append(f"- **{x['pair']}** (n={x['n']}): r(yds)={x['r_yds']}, r(tgt share)={x['r_tgt_share']} → **{x['label']}** (small sample). Game yds: {kv(x['games'])}. Flip games: {'; '.join(x['flip_games']) or 'none'}")
        if o['film_receiver_notes']: M.append("Film notes (week8/film, PBP-verified plays):\n" + '\n'.join('  - '+n for n in o['film_receiver_notes']))
        M.append(f"\n### 3. {opp} pressure/blitz\nBlitz {d['ftn_blitz_pct']}% (FTN) | Sharp blitz {sh.get('Blitz Rate')}% | sacks {d['sacks']} (sack rate {d['sack_rate']}%) | PFR pressures/g {d['pfr_pressures_pg']} | pass-rush win rate {d['pass_rush_win_rate']} | 3rd down: blitz {d['3rd_blitz_pct']}%, avg box {d['3rd_avg_box']}, 7+ box {d['3rd_box7plus_pct']}%, 5+ rushers {d['3rd_5plus_rushers_pct']}%. Light/heavy box (Sharp): {sh.get('Light Box Rate')}/{sh.get('Heavy Box Rate')}.\nTop rushers: " + '; '.join(f"{r['name']} {r['pressures']} pr / {r['sacks']} sk" for r in d['top_rushers']) + "\n")
        bb,nb=o['qb_blitz'],o['qb_noblitz']
        M.append(f"### 4. {o['qb']} vs blitz (FTN-charted dropbacks)\nBlitz faced {o['blitz_faced_pct']}%. **Blitzed:** {bb}  \n**Not blitzed:** {nb}  \n(Pressure-split on non-blitz pressure = GAP; FTN has no pressure flag.)\n")
        M.append(f"### 5. Target tree when blitzed (n={o['blitz_n']} targets)\nBy position: {kv(o['blitz_pos_share'])}  \n0-5 air yds: {'; '.join(o['blitz_tree_0_5'])}  \n5-15 air yds: {'; '.join(o['blitz_tree_5_15'])}\n")
        M.append(f"### 6. {opp} defense totals\n{d['pass_yds_pg']} pass yds/g, {d['rush_yds_pg']} rush yds/g, **{d['pts_allowed_pg']} pts/g**, {d['pass_td']} pass TD, {d['rush_td']} rush TD allowed.\n")
        M.append(f"### 7. Red zone\n{t} RZ TD% {o['rz_td_pct']} vs {opp} allowed {d['rz_td_pct_allowed']}. Inside 20 tgts: {kv(o['rz20_tgts'])}; carries: {kv(o['rz20_car'])}. Inside 10 tgts: {kv(o['rz10_tgts'])}; carries: {kv(o['rz10_car'])}.\n")
        M.append(f"### 8. Coaching\n3rd down: pass {o['3rd_pass_pct']}%, conv {o['3rd_conv']}% (opp D allows {d['3rd_conv_allowed']}%). 4th down: went for it {o['4th_go']} of {o['4th_att_total']} 4th downs, conv {o['4th_conv_pct']}%. Neutral early-down pass rate {o['pass_rate_neutral']}%. HC/OC/DC notes: see team_baselines/{t}.md (not re-pulled).\n")
        M.append(f"### 9. Personnel\n11/12/13 rates: GAP (2026 participation not published). TEs: " + '; '.join(f"{x['name']} snap {x['snap_pct']}%, {x['tgts']} tgts ({x['tgt_per_100snaps']}/100 snaps)" for x in o['tes']) + f". {o.get('te_roles','')}\n")
        M.append(f"### 10. Bottom line ({t}) — opportunity gate applied, no prop lines yet\n**Edges:**\n" + ('\n'.join('- '+e for e in s['edges']) or '- none clear') + "\n**Traps:**\n" + ('\n'.join('- '+e for e in s['traps']) or '- none flagged'))
        tr=[f"neutral pass rate {o['pass_rate_neutral']}%", f"blitzed {o['blitz_faced_pct']}%", f"RZ TD {o['rz_td_pct']}%", f"blitz tree leans {max(o['blitz_pos_share'],key=o['blitz_pos_share'].get) if o['blitz_pos_share'] else '?'}"]
        M.append("\n**Team traits (box score):** " + ', '.join(tr))
    open(f"{a}_at_{h}.md",'w').write('\n'.join(M))
print('done')
