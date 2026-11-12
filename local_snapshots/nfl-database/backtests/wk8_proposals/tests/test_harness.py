import unittest, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import harness as H

class T(unittest.TestCase):
    def test_roi(self):
        self.assertAlmostEqual(H.roi(1.0, -110), 100/110)
        self.assertAlmostEqual(H.roi(0.0, -160), -1.0)
        self.assertAlmostEqual(H.roi(110/210, -110), 0.0, places=9)
    def test_proxy_line_half_point(self):
        self.assertEqual(H.proxy_line([50, 60, 70]), 60.5)
        self.assertEqual(H.proxy_line([3, 4]), 3.5)
    def test_proxy_line_none_when_short(self):
        self.assertIsNone(H.proxy_line([10]))
    def test_no_lookahead(self):
        import pandas as pd
        pg = pd.DataFrame({"pid":["a"]*4,"week":[1,2,3,4],"val":[10,20,30,1000]})
        self.assertEqual(H.prior_vals(pg, "a", 4, "val"), [10,20,30])
        self.assertNotIn(1000, H.prior_vals(pg, "a", 4, "val"))
    def test_two_of_three(self):
        self.assertTrue(H.clears([70,50,61], 60, need=2))
        self.assertFalse(H.clears([70,50,61], 60, need=3))
    def test_wilson(self):
        lo, hi = H.wilson(5, 10); self.assertTrue(lo < .5 < hi)
    def test_summary_keys(self):
        s = H.summarize([1,0,1,1])
        for k in ("n","hit","roi_110","roi_130","roi_160","ci_lo","ci_hi"): self.assertIn(k, s)
if __name__ == "__main__": unittest.main()
