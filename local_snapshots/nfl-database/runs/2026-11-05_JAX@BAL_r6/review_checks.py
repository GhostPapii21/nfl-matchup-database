"""Offline source reconciliation and fail-closed regressions for the r6 review."""
import copy
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import pandas as pd

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[1]
sys.path[:0] = [str(RUN), str(ROOT / 'tools')]
import assemble
from run_gate import Gate


def read(path):
    return json.loads((RUN / path).read_text())


class ReviewChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = pd.read_parquet(assemble.PBP)
        cls.p = cls.p[(cls.p.season_type == 'REG') & (cls.p.two_point_attempt != 1) & (cls.p.game_date < '2026-11-05')]
        cls.m = read('gate_A/run_manifest.json')

    def test_ranks_and_current_qb_carries(self):
        extra = read('codex/legs_extra.json')
        self.assertEqual(extra['Strange 4+ rec (o3.5)']['te_rank'], 1)
        self.assertEqual(extra['Washington rec yds o63.5']['wr_rank'], 1)
        cs = extra['Henry 40+ rush (o39.5)']['carry_share']
        self.assertEqual((cs['numerator'], cs['denominator'], cs['value']), (11, 16, 11 / 16))
        self.assertEqual(cs['games'], ['2026_08_BAL_BUF'])
        henry = next(l for l in self.m['legs'] if l['type'] == 'RB')
        self.assertEqual(henry['recent_form']['values'], [53])
        self.assertEqual(henry['recent_form']['qb'], 'J.Fagnano')

    def test_coverage_matches_pfr_extraction(self):
        df = pd.read_csv(ROOT / 'week10/bal_secondary/defender_table.csv').set_index('defender')
        for cov in read('codex/coverage.json').values():
            for d in cov['defenders']:
                row = df.loc[d['name']]
                self.assertEqual(d['targets'], row.tgt)
                self.assertAlmostEqual(d['comp_pct'], row.cmp_pct / 100)
                self.assertEqual(d['ypt'], row.y_per_tgt)
                self.assertIs(d['primary'], False)
            for key in ('man_zone', 'mof'):
                self.assertEqual(cov[key]['status'], 'MISSING')
                self.assertIsNone(cov[key]['value'])
                self.assertIn('source', cov[key])
                self.assertIn('pulled_et', cov[key])

    def test_pressure_counts_reconcile_sources(self):
        p = self.p
        f = pd.read_parquet(ROOT / 'week10/bal_secondary/raw/ftn_charting_2026.parquet')
        f = f.rename(columns={'nflverse_game_id':'game_id','nflverse_play_id':'play_id'})
        x = p.merge(f, on=['game_id','play_id'], how='left', suffixes=('','_ftn'), validate='one_to_one')
        bal = x[(x.defteam == 'BAL') & ((x.qb_dropback == 1) | (x.pass_attempt == 1))]
        chart = bal[bal.n_pass_rushers.notna()]
        pi = read('codex/pressure_inputs.json')
        self.assertEqual(len(chart), 300)
        self.assertAlmostEqual(pi['blitz_rate']['value'], (chart.n_pass_rushers >= 5).mean())
        self.assertAlmostEqual(pi['pressure_rate']['value'], (bal.sack.eq(1) | bal.qb_hit.eq(1) | bal.qb_scramble.eq(1)).mean())
        q = x[(x.posteam == 'JAX') & (x.passer_player_name == 'T.Lawrence') & ((x.qb_dropback == 1) | (x.pass_attempt == 1))]
        pressured = q.sack.eq(1) | q.qb_hit.eq(1) | q.qb_scramble.eq(1) | q.is_qb_out_of_pocket.fillna(False).eq(True)
        tp = q[pressured & q.receiver_player_id.notna()]
        self.assertEqual(pi['targets_under_pressure']['value']['total'], len(tp))
        self.assertEqual(pi['targets_under_pressure']['value']['by_receiver'], tp.receiver_player_name.value_counts().to_dict())
        pl = pd.read_parquet(ROOT / 'runs/2026-11-01_shared_src/players.parquet')
        pos = pl.drop_duplicates('gsis_id').set_index('gsis_id').position_group
        att = q[(q.pass_attempt == 1) & (q.sack != 1)]
        self.assertAlmostEqual(pi['checkdown_share']['value'], (att.air_yards.le(0) | att.receiver_player_id.map(pos).eq('RB')).mean())

    def test_no_vig_matches_exact_two_way_saved_prices(self):
        odds = pd.read_csv(RUN / 'odds/odds_r6.csv')
        for name, player, market, side, point in [
            ('Strange 4+ rec (o3.5)', 'Brenton Strange', 'player_receptions', 'Over', 3.5),
            ('Washington rec yds o63.5', 'Parker Washington', 'player_reception_yds', 'Over', 63.5),
            ('JAX 1H -6.5', None, 'spreads_h1', 'Jacksonville Jaguars', -6.5),
        ]:
            q = odds[(odds.book == 'pinnacle') & (odds.market == market)]
            if player:
                q = q[(q.player == player) & (q.point == point)]
            a = int(q[q.side == side].price.iloc[0])
            b = int(q[q.side != side].price.iloc[0])
            implied = lambda price: -price / (100-price) if price < 0 else 100 / (100+price)
            leg = next(l for l in self.m['legs'] if l['name'] == name)
            self.assertAlmostEqual(leg['no_vig'], implied(a) / (implied(a)+implied(b)), places=14)

    def test_target_pool_reconciles_every_count(self):
        pool = read('grok/target_share_pool.json')
        j = self.p[(self.p.posteam == 'JAX') & (self.p.pass_attempt == 1) & self.p.receiver_player_name.notna()]
        weeks = sorted(j[j.passer_player_name == 'T.Lawrence'].week.unique())[-3:]
        last = j[j.week.isin(weeks)]
        for player in pool['players']:
            n = player['name']
            self.assertEqual(player['targets'], int((j.receiver_player_name == n).sum()))
            self.assertEqual(player['targets_l3'], int((last.receiver_player_name == n).sum()))
            self.assertAlmostEqual(player['share_season'], player['targets'] / len(j))
            self.assertAlmostEqual(player['share_l3_current_qb'], player['targets_l3'] / len(last))
        self.assertEqual([p['name'] for p in pool['players'] if p['qualifies']], ['P.Washington'])
        self.assertEqual((len(j), len(last)), (195, 96))

    def test_film_files_metadata_resolution_and_pbp_matches(self):
        entries = read('grok/film_verified.json')
        self.assertEqual(len(entries), 5)
        for e in entries:
            file = Path(e['local_file'])
            meta = json.loads(file.with_suffix('.info.json').read_text())
            self.assertEqual(meta['channel_id'], 'UCDVYQ4Zhbm3S2dlz7P1GBDg')
            self.assertEqual((e['url'], e['title'], e['date']), (meta['webpage_url'], meta['title'], meta['upload_date']))
            self.assertTrue(file.exists())
            self.assertEqual(file.stat().st_size, e['bytes'])
            probe = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=height', '-of', 'json', str(file)], capture_output=True, text=True, check=True)
            self.assertLessEqual(json.loads(probe.stdout)['streams'][0]['height'], 720)
        for e in read('grok/film_play_matches.json'):
            play = self.p[(self.p.game_id == e['game_id']) & (self.p.play_id == e['play_id'])].iloc[0]
            self.assertEqual((e['player'], e['yards'], e['qtr']), (play.receiver_player_name, play.yards_gained, play.qtr))
            captions = (RUN / 'film/R7zUguz0Aag.en.vtt').read_text()
            self.assertIn(e['video_timestamp'], captions)

    def test_sim_reproduction_hashes(self):
        for name, sha in read('codex/verification_hashes.json').items():
            self.assertEqual(hashlib.sha256((RUN / 'codex' / name).read_bytes()).hexdigest(), sha)
        sims = read('codex/sims.json')
        self.assertEqual({s['model'] for s in sims}, {'monte_carlo', 'bias', 'game_randomness'})
        self.assertTrue(all(s['n'] == 100000 and s['seed'] == 20261104 for s in sims))

    def test_missing_evidence_cannot_pass_on_provenance_or_checklist(self):
        # Isolate the real risk: run_gate.stamped accepts a fresh sourced MISSING
        # block. The assembler must explicitly propagate its semantic gap.
        g = Gate(str(RUN / 'gate_A'), dt.datetime(2026, 11, 4, 15, 37))
        block = self.m['pressure_inputs']['time_to_throw']
        self.assertTrue(g.stamped('time_to_throw', block, 'coverage_matchups'))
        m = copy.deepcopy(self.m)
        for leg in m['legs']:
            leg['gaps'] = assemble.evidence_gaps(leg, m['pressure_inputs'], m['sims'], [])
            self.assertTrue(leg['gaps'] if leg['receiving'] or leg['type'] == 'GAME' else True)
        with tempfile.TemporaryDirectory(prefix='.review-check-', dir=RUN) as folder:
            d = Path(folder)
            (d / 'run_manifest.json').write_text(json.dumps(m))
            (d / 'report.md').write_text('# Risks\nReview fixture.\n')
            rows = ['| Leg | Phase | Status | Number | Source | Pulled (ET) |', '|---|---|---|---|---|---|']
            rows += [f"| {leg['name']} | {ph} | PASS | supplied | fixture | 2026-11-04 15:37 |" for leg in m['legs'] for ph in range(1, 16)]
            (d / 'checklist.md').write_text('\n'.join(rows))
            gate = Gate(str(d), dt.datetime(2026, 11, 4, 15, 37))
            gate.run()
            self.assertTrue(any('MISSING pressure_inputs.time_to_throw' in miss and 'flagged gaps' in miss for miss in gate.miss))
            self.assertTrue(any('UNVERIFIED' in miss and 'flagged gaps' in miss for miss in gate.miss))

    def test_missing_artifact_forces_gap(self):
        leg = {'name': 'example', 'receiving': False}
        self.assertIn('Missing artifact: grok/target_share_pool.json', assemble.evidence_gaps(leg, {}, [], ['grok/target_share_pool.json']))


if __name__ == '__main__':
    unittest.main(verbosity=2)
