import json,re
R='/workspace/nfl-database/runs/'; O=json.load(open(R+'2026-11-01_shared_src/refresh_r0835_results.json'))
PFF={'Jahan Dotson':'PFF UNDER 25.5 (proj 19.5) - agrees','Xavier Worthy|recyds':'PFF OVER 29.5 (proj 34.5; 57.3% per Ghost6) - agrees',
 'Stefon Diggs|recyds':'no csv row; per Ghost6 PFF leans UNDER 42.5 at 53.7% on 5.6 targets - CONFLICT','Stefon Diggs|rec':'no csv row; ~5.6 targets per Ghost6, thin for 4+, against 5+',
 'Puka Nacua':'no receptions row (only rush yds)','Tre Tucker':'no receptions row; PFF UNDER rec yds 48.5 (proj 41.5) - soft conflict',
 'Jordan Addison':'no row','Matthew Stafford':'PFF OVER 22.5 completions (proj 23.54) - agrees','Rashee Rice':'no receptions row; PFF UNDER rec yds 51.5 (proj 39.5)',
 'Xavier Worthy|rec':'no receptions row'}
def pff(n):
    p=n.split(']')[-1].strip(); pl=' '.join(p.split()[:2]); mk='recyds' if 'Rec Yds' in n else 'rec'
    return PFF.get(f'{pl}|{mk}') or PFF.get(pl,'')
def f(x): return f'{x*100:+.1f}'
def row(o):
    v5=f"{f(o['v5_gate'])} / {f(o['v5_shr'])} | {f(o['v5_mcgr'])}" if 'v5_gate' in o else 'n/a | n/a'
    st='PASS' if o['v6_ok'] and o['status_before']=='PASS' else ('CUT (stays cut)' if o['status_before']=='CUT' else 'FAIL')
    md=o['v6_med']; p=o['v6_p']
    return (f"| {o['leg']} | {o['old_price']:+d} / {o['old_nv']:.3f} | {o['new_price']:+d} / {o['new_nv']:.3f} ({o['price_src']}) | {v5} | "
            f"{p['monte_carlo']:.3f}/{p['bias']:.3f}/{p['game_randomness']:.3f} | {md['monte_carlo']:g}/{md['bias']:g}/{md['game_randomness']:g} | {f(o['v6_gate'])} / {f(o['v6_shr'])} | {pff(o['leg'])} | {st} |")
HDR=("| Leg | 07:30-07:44 price / no-vig | 08:36 price / no-vig | v5 gate edge / shrunk | v5 MC+GR edge | v6 p MC/Bias/GR | v6 medians | v6 gate edge / shrunk | PFF side | Status |\n"
     "|---|---|---|---|---|---|---|---|---|---|")
RISK=("- 08:25 refresh (run 08:36 ET): tools/sim_v6.py (calibrated bias model; BUG-2026-11-01-BIAS fixed; tools/tests 35/35 OK at 08:36) replaced sim_v5.py for this re-score, "
      "100,000 sims x 3 models, seed 20261101; v5 numbers kept in run_manifest.json `sims_v5`. Odds re-pulled 08:36 ET via The Odds API (pull_odds.py/pull_lines.py, odds_r0835.csv / lines_r0835.json); "
      "the 08:36 odds go stale at 09:36 ET. PFF props csv (captured 07:40 ET) is a pick-side cross-check only and was moved from `sources` to `cross_checks` because it is over 1 h old. "
      "PFR per-defender cache pfr_def_adv_2026.html exception still applies (Rico, valid 2026-11-01 only). Pre-refresh files saved as *.pre0825.*.")
for d in ['ATL@TB','KC@DEN','LAC@LAR','LV@NYJ','MIN@DET','PHI@WSH','DFS_SLIPS','FD7_REPLACEMENTS']:
    p=R+'2026-11-01_'+d+'/report.md'; t=open(p).read()
    rows=[row(o) for k,o in O.items() if k.startswith(d+'::')]
    sec=f"\n## 08:25 ET refresh — re-priced 08:36 ET, re-scored on sim_v6 (v5 shown side by side)\n\nAll lines unchanged vs the vetted run. Spreads unchanged; FD totals moved KC@DEN 40.5→41.5 and LV@NYJ 45.5→46.5 (sims use spread, not total).\n\n{HDR}\n"+'\n'.join(rows)+'\n'
    if d=='FD7_REPLACEMENTS':
        sec+=("\n### TD slots as receptions props (Rico) — 08:36 prices, v6 edges\n\n"
        "| Candidate | Price | v6 gate edge / shrunk | Slot A (-280 or longer, replaces Kyren/Corum TD) | Slot B (-140 or longer, replaces Walker TD) | Notes |\n|---|---|---|---|---|---|\n")
        G=lambda n: O['FD7_REPLACEMENTS::'+n]
        for n,a,b,note in [('Jordan Addison Receptions Under 3.5','eligible','too short (-160)','MIN@DET; St. Brown (DET, excluded) is in this game, under on MIN WR is not same-side with him'),
                           ('Stefon Diggs Receptions Over 3.5','eligible','too short (-166)','PHI@WSH; do not pair with Diggs rec yds; PFF ~5.6 targets thin'),
                           ('Puka Nacua Receptions Over 7.5','eligible','eligible (only clean receptions leg)','LAC@LAR; same-player stack with Rico UD Puka o69.5 rec yds'),
                           ('Tre Tucker Receptions Over 3.5','price ok','price ok','EXCLUDED: LV game correlates with Bowers'),
                           ('Jahan Dotson Rec Yds Under 25.5','price ok','Ghost6 alternative (-113), not receptions','ATL@TB; no overlap with excluded players'),
                           ('Rashee Rice Receptions Over 4.5','CUT','CUT','KC: adds to Walker 80+ rush+rec exposure; fails edge'),
                           ('Xavier Worthy Receptions Over 3.5','CUT','CUT','KC: adds to Walker 80+ exposure; fails edge')]:
            o=G(n); sec+=f"| {n} | {o['new_price']:+d} | {f(o['v6_gate'])} / {f(o['v6_shr'])} | {a} | {b} | {note} |\n"
        sec+=("\nReceptions pairing on v6: Slot A Addison U3.5 (-160, +10.0) or Diggs 4+ (-166, +8.7); Slot B Puka O7.5 (-138, +7.3, shrunk +3.9). Ghost6's alternative for Slot B: Dotson U25.5 (-113, +8.4). "
              "Ghost6's yards pair (Worthy 30+ A, Diggs 43+ B) still passes on v6 (+8.9, +10.7), but Worthy is a second KC leg next to Rico's placed Kenneth Walker 80+ rush+rec, so KC exposure doubles; "
              "and the Diggs 43+ leg runs against PFF's UNDER lean. Rice/Worthy receptions stay CUT.\n")
    m=re.search(r'^#+\s*[^\n]*Risks[^\n]*\n',t,re.M|re.I)
    t=t[:m.end()]+RISK+'\n'+t[m.end():] if m else t+'\n## Risks\n'+RISK+'\n'
    open(p,'w').write(t.rstrip('\n')+'\n'+sec)
print('ok')
