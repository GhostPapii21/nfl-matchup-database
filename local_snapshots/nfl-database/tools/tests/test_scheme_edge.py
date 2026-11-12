import os,sys,unittest
sys.path.insert(0,os.path.join(os.path.dirname(__file__),".."))
import run_gate as rg
OK={k:{"ok":True,"source":"x","detail":"y"} for k in rg.SCHEME_KEYS}
class SE(unittest.TestCase):
    def test_all_four(self): self.assertTrue(rg.scheme_edge_ok({"scheme_edge":OK}))
    def test_missing_one(self):
        d=dict(OK); d.pop("script"); self.assertFalse(rg.scheme_edge_ok({"scheme_edge":d}))
    def test_no_source(self):
        d=dict(OK); d["matchup"]={"ok":True}; self.assertFalse(rg.scheme_edge_ok({"scheme_edge":d}))
    def test_absent(self): self.assertFalse(rg.scheme_edge_ok({}))
if __name__=="__main__": unittest.main()
