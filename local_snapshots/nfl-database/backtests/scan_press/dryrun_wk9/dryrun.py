"""Synthetic Week 9 dry-run: press_inputs.build_press -> run_manifest.json -> press_live.apply. Synthetic numbers, not real Week 9 data."""
import json, os, sys
sys.path.insert(0, '/workspace/nfl-database/tools'); import press_inputs as PI, press_live as PL
HERE = os.path.dirname(os.path.abspath(__file__)); RUN = os.path.join(HERE, '2026-11-05_JAX@BAL')
os.environ['PRESS_TRACKER'] = os.path.join(HERE, 'press_tracker_dryrun.csv')
if os.path.exists(os.environ['PRESS_TRACKER']): os.remove(os.environ['PRESS_TRACKER'])
ok = {3: 'PASS', 4: 'PASS', 6: 'PASS', 11: 'PASS', 13: 'PASS'}
base = dict(pos='WR', market='recyds', side='Over', line=60.5, meds=[72, 70, 68], phases=ok, recent_form=[75, 66, 41, 80],
            injury_status='Active', inactives=[], placed_players=[], wr_rank=1)
legs = [('Zay Flowers rec yds o60.5 (clean)', {}),
        ('Brian Thomas Jr. rec yds o60.5 (weather)', dict(phases={**ok, 11: 'FAIL'})),
        ('Travis Hunter rec yds o60.5 (injury Doubtful)', dict(injury_status='Doubtful')),
        ('Rashod Bateman rec yds o60.5 (inactive)', dict(inactives=['Rashod Bateman'])),
        ('Parker Washington rec yds o60.5 (sec11)', dict(placed_players=['Parker Washington'])),
        ('DeAndre Hopkins rec yds o60.5 (WR3)', dict(wr_rank=3)),
        ('Mark Andrews rec yds o40.5 (inactives not posted)', dict(pos='TE', inactives=None, wr_rank=None))]
M = dict(season=2026, week=9, game='JAX@BAL', game_date='2026-11-05', synthetic=True, legs=[])
for name, ch in legs:
    a = {**base, **ch}; pl = name.split(' rec')[0]
    M['legs'].append(dict(name=name, game='JAX@BAL', line=a['line'], side='over', press=PI.build_press(player=pl, **a)))
json.dump(M, open(os.path.join(RUN, 'run_manifest.json'), 'w'), indent=1)
open(os.path.join(RUN, 'report.md'), 'w').write('# SYNTHETIC dry-run report\n')
print('active_for 2026-11-05:', PL.active_for('2026-11-05'))
print('\n'.join(PL.apply(RUN, '2026-11-05', {l['name'] for l in M['legs']})))
