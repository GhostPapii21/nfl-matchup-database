import unittest
from research.third_down.wentz_third_down_receiver_prop_join import generate

class WentzPropCrossTest(unittest.TestCase):
    def test_all_five_2025_starts_and_high_sack_join(self):
        r=generate()
        self.assertEqual(r["all_five_wentz_starts"]["games"],5)
        self.assertEqual(r["third_down_sacks_2plus"]["games"],4)
        x=r["third_down_sacks_2plus"]["thresholds"]
        self.assertEqual(x["jefferson_over_70_5_yds"]["clears"],4)
        self.assertEqual(x["jefferson_over_77_5_yds"]["clears"],2)
        self.assertEqual(x["jefferson_7plus_rec"]["clears"],3)
        self.assertEqual(x["jefferson_8plus_rec"]["clears"],1)
        self.assertEqual(x["hockenson_over_4_5_rec"]["clears"],2)
    def test_receiver_outcomes_and_qb_sacks_not_mixed(self):
        r=generate()
        p={x["week"]:x for x in r["per_game"]}
        self.assertEqual((p[4]["wentz_third_down_sacks"],p[4]["jefferson_rec"],p[4]["jefferson_yds"]),(4,10,126))
        self.assertEqual((p[8]["wentz_third_down_sacks"],p[8]["hockenson_rec"]),(2,2))
        self.assertFalse(p[4]["prop_clears"]["hockenson_over_4_5_rec"])
