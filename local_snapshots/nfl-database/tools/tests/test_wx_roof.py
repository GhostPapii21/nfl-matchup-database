"""BUG-2026-11-02-WXROOF: Phase 11 weather check must FAIL CLOSED (not crash) when a game's weather entry has no
roof object (null / string / list). Written before the fix (RED: AttributeError traceback)."""
import json, os, shutil, subprocess, sys, tempfile, unittest
HERE=os.path.dirname(os.path.abspath(__file__)); GATE=os.path.join(HERE,"..","run_gate.py")
FIX=os.path.join(HERE,"fixtures","valid_run"); NOW="2026-11-01T12:00"
class WxRoof(unittest.TestCase):
    def go(self, entry):
        d=os.path.join(tempfile.mkdtemp(),"run"); shutil.copytree(FIX,d); mp=os.path.join(d,"run_manifest.json")
        m=json.load(open(mp)); m["weather"]={m["game"]: entry}; json.dump(m,open(mp,"w"))
        r=subprocess.run([sys.executable,GATE,d,"--now",NOW],capture_output=True,text=True); return r.returncode, r.stdout+r.stderr
    def check(self, entry):
        c,o=self.go(entry)
        self.assertNotIn("Traceback",o,o); self.assertNotEqual(c,0,o); self.assertIn("GATE: FAIL",o)
        self.assertIn("roof status missing (fail closed)",o)
    def test_null_entry(self): self.check(None)
    def test_string_entry(self): self.check("n/a")
    def test_list_entry(self): self.check([])
    def test_dict_without_roof(self): self.check({"precip_pct":10,"gust_mph":8,"wind_mph":5,"source":"https://api.weather.gov/x","pulled_et":"2026-11-01T10:00"})
if __name__=="__main__": unittest.main()
