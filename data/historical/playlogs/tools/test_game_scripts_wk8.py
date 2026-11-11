import json,pandas as pd,unittest,os
D=os.path.dirname(__file__)+'/..'
class T(unittest.TestCase):
  def test_every_completed_wk8_game_has_two_rows_matching_espn(self):
    g=pd.read_csv(D+'/game_scripts_2026.csv');g=g[g.week==8]
    sb=json.load(open(D+'/../audits/pff_reference_2026-11-01/espn_sb_wk8.json'))
    for e in sb['events']:
      c=e['competitions'][0]
      if not c['status']['type']['completed']: continue
      t={x['homeAway']:x for x in c['competitors']};gm=f"{t['away']['team']['abbreviation']}@{t['home']['team']['abbreviation']}".replace('WSH','WAS')
      r=g[g.game==gm];self.assertEqual(len(r),2,gm)
      a=r[r.home==0].iloc[0];self.assertEqual((a.pts_for,a.pts_against),(int(t['away']['score']),int(t['home']['score'])),gm)
if __name__=='__main__': unittest.main()
