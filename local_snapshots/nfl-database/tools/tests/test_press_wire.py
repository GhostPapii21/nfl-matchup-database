import csv, json, os, sys, tempfile, unittest, hashlib
HERE=os.path.dirname(os.path.abspath(__file__)); TOOLS=os.path.join(HERE,".."); ROOT=os.path.join(TOOLS,"..")
sys.path.insert(0,TOOLS); import press_tier as pt

def base(**kw):
    a=dict(player="Brian Thomas Jr.",pos="WR",market="recyds",side="over",line=58.5,meds=[70,66,52],
           phases={3:"PASS",4:"PASS",6:"PASS",11:"PASS",13:"PASS"},recent_form=[70,65,40,80],injury_status="Active",
           inactives=[],placed_players=[],wr_rank=1)
    a.update(kw); return a
def P(**kw):
    import press_inputs as pi; return pi.build_press(**base(**kw))
def tier(**kw): return pt.evaluate(P(**kw))["tier"]

class Build(unittest.TestCase):
    def test_all_aligned_is_press(self): self.assertEqual(tier(),"PRESS")
    def test_fields_present(self):
        p=P()
        for k in ("matchup","coverage","script","qb","form7","medians","line","side","weather_stop","injury_status","on_inactives","sec11_conflict","wr_rank","sources"): self.assertIn(k,p)
    def test_missing_context_never_passes(self):
        for ph,k in ((3,"matchup"),(4,"coverage"),(6,"qb"),(13,"script")):
            for st in ("MISSING","UNVERIFIED",None,"STALE"):
                ps=dict(base()["phases"]); ps[ph]=st
                if st is None: del ps[ph]
                p=P(phases=ps); self.assertNotEqual(p[k],True,(k,st)); self.assertEqual(pt.evaluate(p)["tier"],"STANDARD",(k,st))
            ps=dict(base()["phases"]); ps[ph]="FAIL"; self.assertIs(P(phases=ps)[k],False)
    def test_form7(self):
        self.assertIs(P()["form7"],True); self.assertIs(P(recent_form=[70,40,40,80])["form7"],False)
        self.assertIs(P(recent_form=[70,65,60])["form7"],True)
        self.assertEqual(P(recent_form=None)["form7"],"MISSING"); self.assertEqual(P(recent_form=[70,65])["form7"],"MISSING")
        self.assertIs(P(side="under",line=50,recent_form=[40,45,60,30])["form7"],True)
    def test_medians_missing(self):
        self.assertEqual(P(meds=[70,66])["medians"],"MISSING"); self.assertEqual(tier(meds=[70,66]),"STANDARD")
        self.assertEqual(P(meds=None)["medians"],"MISSING")
    def test_coverage_na_only_for_pure_rush(self):
        ps=dict(base()["phases"]); ps[4]="N/A"
        self.assertIs(P(pos="RB",market="rushyds",phases=ps,wr_rank=None)["coverage"],True)
        self.assertEqual(P(phases=ps)["coverage"],"MISSING")
    def test_weather_override(self):
        ps=dict(base()["phases"]); ps[11]="FAIL"; self.assertEqual(tier(phases=ps),"BLOCKED")
        del ps[11]; self.assertEqual(P(phases=ps)["weather_stop"],"MISSING"); self.assertEqual(tier(phases=ps),"BLOCKED")
    def test_injury_override(self):
        self.assertEqual(tier(injury_status="Out"),"BLOCKED"); self.assertEqual(tier(injury_status=None),"BLOCKED")
    def test_inactives_override(self):
        self.assertEqual(tier(inactives=["Brian Thomas Jr."]),"BLOCKED"); self.assertEqual(tier(inactives=None),"BLOCKED")
        self.assertEqual(P(inactives=None)["on_inactives"],"MISSING")
    def test_sec11_override(self):
        self.assertEqual(tier(placed_players=["Brian Thomas Jr."]),"BLOCKED"); self.assertEqual(tier(placed_players=None),"BLOCKED")
    def test_wr_ban_override(self):
        for k in (3,4): self.assertEqual(tier(wr_rank=k),"BLOCKED")
        self.assertEqual(tier(wr_rank=None),"BLOCKED")
        self.assertEqual(P(pos="RB",market="rushyds",wr_rank=None)["wr_rank"],"N/A")
        self.assertEqual(P(pos="TE",wr_rank=None)["wr_rank"],"N/A")

class EvaluateFailClosed(unittest.TestCase):
    def test_missing_override_key_blocks(self):
        p=P()
        for k in ("weather_stop","injury_status","on_inactives","sec11_conflict","wr_rank"):
            q=dict(p); del q[k]; self.assertEqual(pt.evaluate(q)["tier"],"BLOCKED",k)
            q=dict(p); q[k]="MISSING"; self.assertEqual(pt.evaluate(q)["tier"],"BLOCKED",k)

class WrRank(unittest.TestCase):
    def test_rank(self):
        import press_inputs as pi
        t={"A":30,"B":25,"C":20,"D":10}
        self.assertEqual(pi.wr_rank("C",t),3); self.assertEqual(pi.wr_rank("A",t),1); self.assertIsNone(pi.wr_rank("Z",t)); self.assertIsNone(pi.wr_rank("A",None))

class Assembly(unittest.TestCase):
    NEW=os.path.join(ROOT,"runs","2026-11-05_shared_src","assemble.py")
    def test_copied_forward_and_wired(self):
        s=open(self.NEW).read(); self.assertIn("press_inputs",s); self.assertIn("d['press']=",s); self.assertIn("game_date=GAME_DATE",s)
    def test_past_assemble_untouched(self):
        p=os.path.join(ROOT,"runs","2026-11-01_shared_src","assemble.py"); self.assertNotIn("press_inputs",open(p).read())

class GradeQB(unittest.TestCase):
    def test_pass_yds_from_box(self):
        import grade_press as gp
        t=tempfile.mkdtemp(); bx=os.path.join(t,"X_Y_box.json"); tr=os.path.join(t,"tr.csv")
        json.dump({"game":"X@Y","teams":{"X":{"passing":[{"C/ATT":"14/25","YDS":"157","player":"Matthew Stafford"}],"rushing":[{"CAR":"10","YDS":"40","player":"Kyren Williams"}],
                   "receiving":[{"REC":"5","YDS":"60","player":"Puka Nacua"}]}}},open(bx,"w"))
        with open(tr,"w",newline="") as f:
            w=csv.DictWriter(f,fieldnames=gp.FIELDS); w.writeheader()
            for leg in ("Matthew Stafford pass yds o250.5 -110","Matthew Stafford pass yds u260.5 -110","Puka Nacua receptions o4.5 -120","Kyren Williams rush yds o55.5 -110"):
                w.writerow(dict(date="2026-11-08",game="X@Y",leg=leg,line=0,book="FD",price=-110,models_cleared=2,result=""))
        self.assertEqual(gp.grade(tr,[bx]),4); r=[x["result"] for x in csv.DictReader(open(tr))]
        self.assertEqual(r,["MISS (157)","HIT (157)","HIT (5)","MISS (40)"])
