"""Adapter: writes gate_A/B/C run folders (run_manifest.json, checklist.md, report.md) for tools/run_gate.py from r6 data only.
Nothing is invented: phases with no r6/r5 artifact are MISSING; categories with no source are flagged_gaps. Legs set PASS so the gate tests them live."""
import json, os, datetime as dt
from zoneinfo import ZoneInfo
PBP='/workspace/nfl-database/runs/2026-11-05_JAX@BAL_r2/src/play_by_play_2026.parquet'
PBPT=dt.datetime.fromtimestamp(os.path.getmtime(PBP), ZoneInfo("America/New_York")).strftime('%Y-%m-%dT%H:%M')
ODDS=os.path.join(os.path.dirname(os.path.abspath(__file__)),'odds','odds_r6.csv'); ODT='2026-11-04T14:59'
# Exact Pinnacle two-way no-vig fractions from odds/odds_r6.csv; no rounding before gate comparisons.
L={'Strange 4+ rec (o3.5)':dict(type='TE',receiving=True,side='over',line=3.5,no_vig=(119/219)/(119/219+105/205),price=-119,price_fd=-122,market='rec',rf=[7,7,5,2],games=['2026_04_JAX_CIN','2026_05_PHI_JAX','2026_06_HOU_JAX','2026_08_IND_JAX'],qb='T.Lawrence'),
 'Strange 40+ rec yds (o39.5)':dict(type='TE',receiving=True,side='over',line=39.5,no_vig=None,price=114,price_fd=114,market='recyds',rf=[95,68,44,55],games=['2026_04_JAX_CIN','2026_05_PHI_JAX','2026_06_HOU_JAX','2026_08_IND_JAX'],qb='T.Lawrence'),
 'Washington rec yds o63.5':dict(type='WR',receiving=True,side='over',line=63.5,no_vig=(115/215)/(115/215+109/209),price=-114,price_fd=-114,market='recyds',rf=[7,124,64,16],games=['2026_04_JAX_CIN','2026_05_PHI_JAX','2026_06_HOU_JAX','2026_08_IND_JAX'],qb='T.Lawrence'),
 'JAX 1H -6.5':dict(type='GAME',receiving=False,side='over',line=6.5,no_vig=(101/201)/(101/201+112/212),price=-101,price_fd=-110,market='spread_h1',rf=[10,-7,-3,28],games=['2026_04_JAX_CIN','2026_05_PHI_JAX','2026_06_HOU_JAX','2026_08_IND_JAX'],qb='T.Lawrence'),
 'Henry 40+ rush (o39.5)':dict(type='RB',receiving=False,side='over',line=39.5,no_vig=None,price=-598,price_fd=-700,market='rushyds',rf=[53],games=['2026_08_BAL_BUF'],qb='J.Fagnano',carry_share=json.load(open(os.path.join(os.path.dirname(__file__),'codex','legs_extra.json')))['Henry 40+ rush (o39.5)']['carry_share'])}
SL={'gate_A':['Strange 4+ rec (o3.5)','Washington rec yds o63.5','JAX 1H -6.5','Henry 40+ rush (o39.5)'],
    'gate_B':['Strange 4+ rec (o3.5)','Strange 40+ rec yds (o39.5)','JAX 1H -6.5','Henry 40+ rush (o39.5)'],
    'gate_C':['Strange 40+ rec yds (o39.5)','Washington rec yds o63.5','JAX 1H -6.5','Henry 40+ rush (o39.5)']}
if __name__ == '__main__':
    from assemble import main
    raise SystemExit(main())
