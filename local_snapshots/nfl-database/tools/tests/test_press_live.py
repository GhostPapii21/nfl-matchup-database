import re
import csv, glob, json, os, shutil, subprocess, sys, tempfile, unittest
HERE=os.path.dirname(os.path.abspath(__file__)); TOOLS=os.path.join(HERE,".."); ROOT=os.path.join(TOOLS,"..")
sys.path.insert(0,TOOLS); import press_tier as pt
GATE=os.path.join(TOOLS,"run_gate.py"); FIX=os.path.join(HERE,"fixtures","valid_run")
PRESS=dict(matchup=True,coverage=True,script=True,qb=True,form7=True,side="over",line=58.5,medians=[70,65,50],
           weather_stop=False,injury_status="Active",on_inactives=False,sec11_conflict=False,wr_rank=1)

class Config(unittest.TestCase):
    def test_config_on_for_week9(self):
        c=json.load(open(os.path.join(TOOLS,"gate_config.json")))
        self.assertTrue(c["press_tier"]["enabled"]); self.assertEqual(c["press_tier"]["enabled_from"],"2026-11-02")  # Rico 2026-11-02 21:13 ET
        self.assertEqual(c["press_tier"]["models_required"],2); self.assertFalse(c["pass_volume_cap"]["enabled"])
    def test_active_for(self):
        import press_live as pl
        self.assertFalse(pl.active_for("2026-11-01")); self.assertTrue(pl.active_for("2026-11-08")); self.assertTrue(pl.active_for("2026-11-05"))

class Overrides(unittest.TestCase):
    def test_press_baseline(self): self.assertEqual(pt.evaluate(PRESS)["tier"],"PRESS")
    def test_one_model_never(self):
        self.assertEqual(pt.evaluate(dict(PRESS,medians=[70,50,50]))["tier"],"STANDARD")
        with self.assertRaises(ValueError): pt.evaluate(PRESS,1)
    def test_context_must_align(self):
        for k in pt.CTX: self.assertEqual(pt.evaluate(dict(PRESS,**{k:False}))["tier"],"STANDARD",k)
    def test_weather_beats_press(self): self.assertEqual(pt.evaluate(dict(PRESS,weather_stop=True))["tier"],"BLOCKED")
    def test_injury_beats_press(self):
        for s in ("Out","Doubtful","inactive"): self.assertEqual(pt.evaluate(dict(PRESS,injury_status=s))["tier"],"BLOCKED")
    def test_inactive_list_beats_press(self): self.assertEqual(pt.evaluate(dict(PRESS,on_inactives=True))["tier"],"BLOCKED")
    def test_sec11_beats_press(self):
        r=pt.evaluate(dict(PRESS,sec11_conflict=True)); self.assertEqual(r["tier"],"BLOCKED"); self.assertIn("11",r["reason"])
    def test_wr34_ban_beats_press(self):
        for k in (3,4): self.assertEqual(pt.evaluate(dict(PRESS,wr_rank=k))["tier"],"BLOCKED")
        self.assertEqual(pt.evaluate(dict(PRESS,wr_rank=2))["tier"],"PRESS")
    def test_cap_not_applied(self):  # pass-volume cap stays OFF: big favorite QB pass over still PRESS
        self.assertEqual(pt.evaluate(dict(PRESS,team_spread=-10,market="pyds"))["tier"],"PRESS")

def gate(d,now,*extra): r=subprocess.run([sys.executable,GATE,d,"--now",now,*extra],capture_output=True,text=True); return r.returncode,r.stdout

class LiveRun(unittest.TestCase):
    def setUp(self):
        t=tempfile.mkdtemp(); self.d=os.path.join(t,"run"); shutil.copytree(FIX,self.d)
        self.tr=os.path.join(t,"press_live.csv"); os.environ["PRESS_TRACKER"]=self.tr
        self.mp=os.path.join(self.d,"run_manifest.json"); s=open(self.mp).read().replace("2026-11-01T","2026-11-08T")
        m=json.loads(s); m["legs"][0]["press"]=dict(PRESS); m["legs"][0]["book"]="FD"
        for _s in m["sims"]: _s["script"]="/workspace/nfl-database/tools/sim_v6.py"  # Week 9+ runs must name sim_v6 (BUG-2026-11-01-SIMV6)
        for _k in ("time_to_throw","targets_under_pressure"): m["pressure_inputs"][_k]=dict(value=1,source="https://nextgenstats.nfl.com",pulled_et="2026-11-08T10:00")  # lesson 5, Week 9+
        m["weather_forecast"]=dict(source="tools/weather_forecast.py",file="fx",pulled_et="2026-11-08T10:00",games={"TEN@CIN":dict(roof="open",status="OK",precip_pct=10,gust_mph=8,wind_mph=5)})  # Rico 2026-11-01 forecast gate
        json.dump(m,open(self.mp,"w"))
        for f in ("checklist.md","report.md"):
            p=os.path.join(self.d,f); t=open(p).read(); open(p,"w").write(t.replace("2026-11-01","2026-11-08"))
    def tearDown(self): os.environ.pop("PRESS_TRACKER",None)
    def test_tags_manifest_report_tracker(self):
        c,o=gate(self.d,"2026-11-08T12:00"); self.assertEqual(c,0,o); self.assertIn("PRESS TIER",o)
        m=json.load(open(self.mp)); l=m["legs"][0]
        self.assertEqual(l["press_tier"]["tier"],"PRESS"); self.assertEqual(l["press_tier"]["models_clear"],2)
        self.assertEqual(m["legs"][1]["press_tier"]["tier"],"STANDARD")
        self.assertIn("[PRESS]",open(os.path.join(self.d,"report.md")).read())
        rows=list(csv.DictReader(open(self.tr))); self.assertEqual(len(rows),1)
        self.assertEqual(set(rows[0]),{"date","game","leg","line","book","price","models_cleared","result"})
        self.assertEqual(rows[0]["models_cleared"],"2"); self.assertEqual(rows[0]["result"],"")
        gate(self.d,"2026-11-08T12:00"); self.assertEqual(len(list(csv.DictReader(open(self.tr)))),1)  # idempotent

class PastRunsUnchanged(unittest.TestCase):
    def test_byte_identical(self):
        bak=os.path.join(TOOLS,"run_gate.py.pre_scanpress.bak")
        for d in sorted(glob.glob(os.path.join(ROOT,"runs","2026-11-01_*/"))):
            if not os.path.exists(os.path.join(d,"run_manifest.json")): continue
            t=tempfile.mkdtemp(); a=os.path.join(t,"a"); b=os.path.join(t,"b"); shutil.copytree(d,a); shutil.copytree(d,b)
            ga=gate(a,"2026-11-01T12:00"); ga=(ga[0],re.sub(r"(?m)^(SHARP CAUTION: .*|  - press blocked: .*)\n","",ga[1]))  # SRC-3 intended new lines only
            gb=gate_bak(bak,b); norm=lambda t:re.sub(r"edge ([+-][\d.]+), shrunk [+-][\d.]+",r"raw edge \1",t)  # NOSHRINK note wording only
            self.assertEqual(ga[0],gb[0],d)
            self.assertEqual(open(os.path.join(a,"run_manifest.json")).read(),open(os.path.join(d,"run_manifest.json")).read(),d)

def gate_bak(bak,d):
    r=subprocess.run([sys.executable,bak,d,"--now","2026-11-01T12:00"],capture_output=True,text=True,cwd=TOOLS); return r.returncode,r.stdout.replace(os.path.dirname(d)+"/b",os.path.dirname(d)+"/a")

class Grade(unittest.TestCase):
    def test_grade_from_playlog(self):
        import grade_press as gp
        t=tempfile.mkdtemp(); pl=os.path.join(t,"X_Y.csv"); tr=os.path.join(t,"tr.csv")
        open(pl,"w").write("game,off,defn,when,kind,tgt,fullname,pos,yds\nX@Y,X,Y,Q1,rec,T.H,Tee Higgins,WR,40\nX@Y,X,Y,Q2,rec,T.H,Tee Higgins,WR,25\nX@Y,X,Y,Q2,rush,C.B,Chase Brown,RB,30\n")
        f=open(tr,"w",newline=""); w=csv.DictWriter(f,fieldnames=gp.FIELDS); w.writeheader()
        w.writerow(dict(date="2026-11-08",game="X@Y",leg="Tee Higgins rec yds o58.5 -115",line=58.5,book="FD",price=-115,models_cleared=2,result=""))
        w.writerow(dict(date="2026-11-08",game="X@Y",leg="Chase Brown rush yds o62.5 -110",line=62.5,book="FD",price=-110,models_cleared=3,result=""))
        f.close(); n=gp.grade(tr,[pl]); rows=list(csv.DictReader(open(tr)))
        self.assertEqual(n,2); self.assertEqual(rows[0]["result"],"HIT (65)"); self.assertEqual(rows[1]["result"],"MISS (30)")
        self.assertEqual(open(pl).read().count("\n"),4)  # play log read-only
