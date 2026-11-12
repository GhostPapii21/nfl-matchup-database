import sqlite3,unittest,os
DB=os.path.join(os.path.dirname(__file__),'fixes.sqlite')
class T(unittest.TestCase):
    @classmethod
    def setUpClass(c): c.db=sqlite3.connect(DB)
    def one(s,q): return s.db.execute(q).fetchone()
    # Fix 1
    def test_golden_credit(s):
        r=s.one("select stored_yards,credited_yards,credit_kind,penalty_yards from fix_play_credits where play_id='401873007411'")
        s.assertEqual(r[0],7.0); s.assertEqual(r[1],37.0); s.assertEqual(r[2],'reception'); s.assertEqual(r[3],15.0)
    def test_nullified_no_credit(s):
        s.assertEqual(s.one("select count(*) from fix_play_credits where credit_status='nullified' and credited_yards is not null")[0],0)
    def test_kneels_separate(s):
        s.assertGreater(s.one("select count(*) from fix_play_credits where credit_kind='kneel'")[0],0)
        s.assertEqual(s.one("select count(*) from fix_play_credits where credit_kind='rush' and qb_kneel=1")[0],0)
    def test_rush_reconciles_to_official(s):
        r=s.one("select sum(rush_ok),count(*) from fix_credit_reconcile"); s.assertEqual(r[0],r[1])
    def test_rec_reconciles_99pct(s):
        r=s.one("select sum(rec_ok)*1.0/count(*) from fix_credit_reconcile"); s.assertGreaterEqual(r[0],0.99)
    def test_unresolved_not_zero(s):
        s.assertEqual(s.one("select count(*) from fix_play_credits where credit_status='unresolved' and credited_yards is not null")[0],0)
    def test_all_games_mapped(s):
        s.assertEqual(s.one("select count(*) from fix_game_map where nflverse_game_id is not null")[0],107)
    # Fix 2
    def test_jacobs_return(s):
        r=s.one("select games_played,games_not_on_roster,current_carry_share_l3,carries_per_game,targets_per_game,is_returning from fix_player_role where player='Josh Jacobs' and team='GB'")
        s.assertEqual(r[0],1); s.assertEqual(r[1],6); s.assertEqual(r[3],11.0); s.assertEqual(r[4],7.0); s.assertEqual(r[5],1); s.assertGreater(r[2],0.5)
    def test_savion_absences_excluded(s):
        r=s.one("select games_played,games_not_on_roster,targets_per_game from fix_player_role where player='Savion Williams' and team='GB'")
        s.assertEqual(r[0],2); s.assertEqual(r[1],5); s.assertEqual(r[2],3.5)
    # Fix 3
    def test_coker_denominator(s):
        r=s.one("select games_played,games_inactive,targets_per_game from fix_player_role where player='Jalen Coker'")
        s.assertEqual(r[0],5); s.assertEqual(r[1],1); s.assertAlmostEqual(r[2],39/5)
        s.assertEqual(s.one("select participation from fix_participation where full_name='Jalen Coker' and week=4")[0],'inactive')
    def test_no_zero_fill_participation(s):
        s.assertEqual(s.one("select count(*) from fix_participation where participation!='played' and offense_snaps>0")[0],0)
    # Fix 4
    def test_qb_split_sums(s):
        bad=s.one("select count(*) from fix_qb_rushing_game where abs(rush_yds_ex_kneel-(scramble_yds+designed_yds))>0.01")[0]; s.assertEqual(bad,0)
    def test_qb_baseline_excludes_kneels(s):
        r=s.one("select count(*) from fix_qb_rushing where kneel_yds_pg<0 and rush_yds_ex_kneel_pg<(scr_yds_pg+des_yds_pg)-0.01")[0]; s.assertEqual(r,0)
        s.assertGreaterEqual(s.one("select count(*) from fix_qb_rushing")[0],32)
if __name__=='__main__': unittest.main(verbosity=1)
