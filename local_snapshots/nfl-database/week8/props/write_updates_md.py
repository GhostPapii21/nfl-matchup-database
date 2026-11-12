import json,statistics as st
ov=json.load(open('proj_overrides.json')); d=json.load(open('compare.json')); R=d['rows']
L=["# Week 8 projection updates (props pass, Oct 29 2026)","","Only changes with a concrete data reason. Nothing moved toward a line.","",
"## Rules","- A: missing-participation denominator (GAME_SCRIPT_2026-10-29 issue #3). Weeks with no offensive snaps in `fixes/src/snap_counts_2026.parquet` are dropped from the L3/season averages. Applied when |f-1| >= 0.08, capped at 4.0. Applied only if he played the last game, or he is Questionable and returning (then the projection assumes he plays).",
"- B: small-sample efficiency. With fewer than 20 season targets, yards/target is regressed to position average (WR 8.1, TE 6.9, RB 5.4) with a 20-target prior. Defense multiplier kept.",
"- Scope: only players whose FD main line was more than 25% from the median were audited.","- compare.py also releases the production-verdict-NO block only for rule-A players (the verdict was computed on the deflated volume), and sets NO BET for anyone with fewer than 3 games with snaps.","","## Changes (tgt / rec / rec yds / car / rush yds)",""]
f=lambda p:f"{p['tgt']}/{p['rec']}/{p['recyds']}/{p['car']}/{p['rushyds']}"
for k,v in ov.items(): L.append(f"- {k}: {f(v['old'])} -> {f(v['proj'])}. {' ; '.join(v['why'])}")
L+=["","## >25% gaps left unchanged",""]
for r in R:
  k=f"{r['game'].replace('LAC@LAR','LAC@LA').replace('PHI@WSH','PHI@WAS')}|{r['player']}"
  if abs(r['edge_pct'])>25 and k not in ov: L.append(f"- {r['game']} {r['player']} {r['market']}: FD {r['fd_line']} vs {r['median']} ({r['edge_pct']:+.0f}%). No participation or sample issue in the data.{' Questionable.' if r['q'] else ''}")
L+=["","## Calibration caveat",f"Median edge across all {len(R)} props is {st.median(r['edge_pct'] for r in R):+.1f}% (rec yds {st.median(r['edge_pct'] for r in R if r['market']=='rec_yds'):+.1f}%). The model runs above FanDuel across the board. Read the leans as a ranking, not as a calibrated win rate. Projections were not shaded toward the lines to fix this.",
"","## P(over) method","Lognormal: median = model median; 25th/75th = median x (lo/tot, hi/tot); sigma = (ln q75 - ln q25)/1.349, floored at rec yds 0.55, rush 0.40, rush+rec 0.40, receptions 0.40. Lean OVER if P >= 0.60 and edge >= 10%; UNDER if P <= 0.40 and edge <= -10%. Rung = highest FD alt rung with model P >= 0.68 (0.80 if Q or volatile), model P > implied, and odds no shorter than -250."]
open('PROJECTION_UPDATES.md','w').write('\n'.join(L)); print(len(L))
