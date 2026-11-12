import json, os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from test_run_gate import Base, H, rd, wr
import price_hold as ph

class PriceHold(unittest.TestCase):
    def test_repull_success_returns_price(self):
        r = ph.resolve_price("over", 68.5, {}, repull=lambda: {"point": 68.5, "over": -115, "nv_over": .52})
        self.assertEqual(r["status"], "PASS"); self.assertAlmostEqual(r["nv"], .52)
    def test_conservative_bracket(self):
        q = {"rungs": [{"point": 67.5, "nv_over": .55}, {"point": 69.5, "nv_over": .51}]}
        r = ph.resolve_price("over", 68.5, q, repull=lambda: None)
        self.assertEqual(r["status"], "DERIVED"); self.assertAlmostEqual(r["nv"], .55)  # higher p = harder bar
    def test_no_data_is_hold_not_cut(self):
        r = ph.resolve_price("over", 68.5, {}, repull=lambda: None)
        self.assertEqual(r["status"], "HOLD"); self.assertTrue(r["repull_attempted"])
    def test_repull_exception_is_hold(self):
        def boom(): raise RuntimeError("http 500")
        r = ph.resolve_price("over", 68.5, {}, repull=boom)
        self.assertEqual(r["status"], "HOLD"); self.assertIn("http 500", r["note"])

class GateHold(Base):
    def _hold(self, leg_status="HOLD", attempt=True):
        l = self.leg(); l["status"] = leg_status
        if attempt: l["hold"] = {"reason": "no-vig MISSING at DFS line", "repull_attempted_et": "2026-11-01 11:40", "repull_result": "no book rung"}
        self.save(); p = os.path.join(self.d, "checklist.md"); s = rd(p)
        s = s.replace(f"| {H} | 14 Models/edge | PASS |", f"| {H} | 14 Models/edge | HOLD |"); wr(p, s)
    def test_hold_leg_is_reported_and_blocked(self):
        self._hold(); c, o = self.run_gate()
        self.assertNotIn("unknown status", o); self.assertNotIn("must be PASS or CUT", o)
        self.assertIn("Held legs", o); self.assertNotIn(H, o.split("Live legs:")[1].split("\n")[0])
    def test_pass_leg_with_hold_phase_fails(self):
        self._hold(leg_status="PASS"); self.assertFail("HOLD")
    def test_hold_without_repull_fails(self):
        self._hold(attempt=False); self.assertFail("re-pull")
if __name__ == "__main__": unittest.main()
