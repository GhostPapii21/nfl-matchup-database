"""Rico-approved source-list changes (2026-11-01 22:47 ET). SRC-1 weather whitelist, SRC-2 PFF re-price,
SRC-3 Sharp second source, SRC-4 pregame odds / props None-line, SRC-5 feed latest-week + season."""
import json, os, sys, unittest, datetime as dt, importlib.util
HERE=os.path.dirname(os.path.abspath(__file__)); TOOLS=os.path.join(HERE,".."); sys.path.insert(0,TOOLS); sys.path.insert(0,HERE)
from test_run_gate import Base, H
import run_gate as RG

class Weather(Base):  # SRC-1
    def test_nws_passes(self): c,o=self.run_gate(); self.assertEqual(c,0,o)
    def test_open_meteo_passes(self):
        self.m["weather"]["TEN@CIN"]["source"]="https://api.open-meteo.com/v1/forecast?latitude=39.1"; self.save(); c,o=self.run_gate(); self.assertEqual(c,0,o)
    def test_pff_weather_fails(self):
        self.m["weather"]["TEN@CIN"]["source"]="https://www.pff.com/nfl/matchups (weather widget)"; self.save(); self.assertFail("NWS/Open-Meteo only")
    def test_other_weather_fails(self):
        self.m["weather"]["TEN@CIN"]["source"]="https://weather.com/forecast"; self.save(); self.assertFail("NWS/Open-Meteo only")
    def test_weather_source_list_entry_pff_fails(self):
        for s in self.m["sources"]:
            if s["category"]=="weather": s["name"]="PFF game weather"; s["url_or_file"]="https://www.pff.com/nfl/matchups"
        self.save(); self.assertFail("NWS/Open-Meteo only")
    def test_weather_forecast_tool_output_passes(self):
        self.m["weather"]["TEN@CIN"]["source"]="/workspace/nfl-database/week9/weather/forecast.json"; self.m["weather"]["TEN@CIN"]["provider"]="open-meteo"
        self.m["weather"]["TEN@CIN"]["tool"]="tools/weather_forecast.py"; self.save(); c,o=self.run_gate(); self.assertEqual(c,0,o)
    def test_forecast_block_pff_fails(self):
        self.m["weather_forecast"]={"source":"PFF game center weather","pulled_et":"2026-11-01T10:00","games":{}}; self.save(); self.assertFail("NWS/Open-Meteo only")
    def test_forecast_block_provider_fails(self):
        self.m["weather_forecast"]={"source":"tools/weather_forecast.py","pulled_et":"2026-11-01T10:00","games":{"TEN@CIN":{"provider":"accuweather","roof":"open"}}}; self.save(); self.assertFail("NWS/Open-Meteo only")
    def test_forecast_block_nws_ok(self):
        self.m["weather_forecast"]={"source":"tools/weather_forecast.py (NWS + Open-Meteo)","pulled_et":"2026-11-01T10:00","games":{"TEN@CIN":{"provider":"open-meteo","roof":"open"}}}; self.save()
        c,o=self.run_gate(); self.assertEqual(c,0,o)
    def test_unit(self):
        self.assertTrue(RG.wx_source_ok({"source":"https://api.weather.gov/gridpoints/X"}))
        self.assertFalse(RG.wx_source_ok({"source":"https://api.weather.gov/x","name":"PFF mirror"}))
        self.assertFalse(RG.wx_source_ok({"source":"https://www.accuweather.com"}))

PICK=dict(player="Tee Higgins",market="recyds",side="over",pff_line=55.5,pff_edge_pct=9.1,book="fanduel",book_line=58.5,book_price=-115,
          pulled_et="2026-11-01T11:30",model_p={"monte_carlo":0.6,"bias":0.58,"game_randomness":0.59},edge_basis="our_model")
class PffPicks(Base):  # SRC-2
    def test_repriced_pick_passes(self):
        self.m["pff_picks"]=[dict(PICK)]; self.save(); c,o=self.run_gate(); self.assertEqual(c,0,o); self.assertIn("PFF edge % ignored",o)
    def test_edge_pct_used_fails(self):
        self.m["pff_picks"]=[dict(PICK,edge_basis="pff_edge_pct")]; self.save(); self.assertFail("PFF edge %")
    def test_uses_pff_edge_flag_fails(self):
        self.m["pff_picks"]=[dict(PICK,uses_pff_edge=True)]; self.save(); self.assertFail("PFF edge %")
    def test_not_repriced_fails(self):
        p=dict(PICK); del p["book_line"]; self.m["pff_picks"]=[p]; self.save(); self.assertFail("re-price")
    def test_missing_model_fails(self):
        p=dict(PICK,model_p={"monte_carlo":0.6,"bias":0.58}); self.m["pff_picks"]=[p]; self.save(); self.assertFail("game_randomness")
    def test_stale_book_line_fails(self):
        self.m["pff_picks"]=[dict(PICK,pulled_et="2026-11-01T09:00")]; self.save(); self.assertFail("stale")
    def test_leg_edge_from_pff_fails(self):
        self.leg()["edge_basis"]="PFF props edge"; self.save(); self.assertFail("PFF edge %")
    def test_pff_leg_at_pff_line_fails(self):
        self.leg()["pff_pick"]=True; self.m["pff_picks"]=[dict(PICK,book_line=57.5)]; self.save(); self.assertFail("book line")

SHARP=dict(category="coverage_matchups",name="Sharp Football coverage schemes",url_or_file="https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/",pulled_et="2026-11-01T09:00",tool="firecrawl")
SECOND=dict(name="StatRankings man/zone",url_or_file="https://statrankings.com/x",pulled_et="2026-11-01T09:00",agrees=True)
class Sharp(Base):  # SRC-3
    def test_sharp_alone_caution_not_fail(self):
        self.m["sources"].append(dict(SHARP)); self.save(); c,o=self.run_gate(); self.assertEqual(c,0,o); self.assertIn("SHARP CAUTION",o)
    def test_sharp_with_agreeing_second_source(self):
        self.m["sources"].append(dict(SHARP,second_source=dict(SECOND))); self.save(); c,o=self.run_gate(); self.assertEqual(c,0,o)
        self.assertNotIn("SHARP CAUTION",o); self.assertIn("confirmed by StatRankings",o)
    def test_disagree_is_caution(self):
        self.m["sources"].append(dict(SHARP,second_source=dict(SECOND,agrees=False))); self.save(); c,o=self.run_gate(); self.assertIn("SHARP CAUTION",o)
    def test_second_source_must_be_allowed(self):
        self.m["sources"].append(dict(SHARP,second_source=dict(SECOND,name="PFF coverage"))); self.save(); c,o=self.run_gate(); self.assertIn("SHARP CAUTION",o)
    def test_unit_press_block(self):
        g=RG.Gate("/nonexistent",dt.datetime(2026,11,1,12)); g.game_date="2026-11-01"
        legs={"A":{"coverage":{"mof":{"source":"Sharp coverage"}}},"B":{"coverage":{"mof":{"source":"FTN"}}},"C":{}}
        blk=g.check_sharp({"sources":[dict(SHARP)]},legs,{"A","B","C"}); self.assertEqual(sorted(blk),["A"])
        blk=g.check_sharp({"sources":[dict(SHARP,second_source=dict(SECOND))]},legs,{"A","B","C"}); self.assertEqual(blk,{})
    def test_press_live_respects_block(self):
        import press_live, tempfile, shutil
        d=tempfile.mkdtemp(); m={"legs":[{"name":"A","line":50,"side":"over","press":dict(matchup=True,coverage=True,script=True,qb=True,form7=True,line=50,side="over",
            medians=[60,61,62],weather_stop=False,injury_status="Active",on_inactives=False,sec11_conflict=False,wr_rank=1)}]}
        json.dump(m,open(os.path.join(d,"run_manifest.json"),"w")); os.environ["PRESS_TRACKER"]=os.path.join(d,"t.csv")
        out=press_live.apply(d,"2026-11-05",["A"],blocked={"A":"Sharp-only coverage"}); self.assertIn("BLOCKED",out[1]); self.assertIn("Sharp",out[1])
        out=press_live.apply(d,"2026-11-05",["A"]); self.assertIn("PRESS",out[1]); self.assertNotIn("BLOCKED",out[1])
        os.environ.pop("PRESS_TRACKER"); shutil.rmtree(d)

def feed(cat,name,wk,season=2026,kind=None,t="2026-11-05T12:00"):
    d=dict(category=cat,name=name,url_or_file="f",pulled_et=t,season=season,data_week=wk)
    if kind: d["week_kind"]=kind
    return d
class FeedWeeks(unittest.TestCase):  # SRC-5
    def g(self,date="2026-11-05"):
        g=RG.Gate("/x",dt.datetime(2026,11,5,13)); g.game_date=date; return g
    def ok(self):
        return [feed("core_stats_pbp","nflverse pbp",8),feed("ngs","NGS",8),feed("film","film",8),feed("coverage_matchups","Sharp",8),
                feed("injuries_news","ESPN injuries",9),feed("weather","NWS",9),feed("odds_props","Odds API",9)]
    def test_all_current_pass(self):
        g=self.g(); g.check_feed_weeks({"season":2026,"week":9,"sources":self.ok()}); self.assertEqual(g.miss,[])
    def test_pff_serving_week8_fails(self):
        g=self.g(); g.check_feed_weeks({"season":2026,"week":9,"sources":self.ok(),"pff_inputs":[dict(leg="x",metric="m",season=2026,data_week=8,pulled_et="2026-11-05T12:00")]})
        self.assertTrue(any("week 8" in x.lower() and "pff" in x.lower() for x in g.miss),g.miss)
    def test_injury_tool_week3_fails(self):
        s=self.ok(); s[4]["data_week"]=3; g=self.g(); g.check_feed_weeks({"season":2026,"week":9,"sources":s}); self.assertTrue(any("ESPN injuries" in x for x in g.miss))
    def test_news_stale_fails(self):
        s=self.ok()+[feed("injuries_news","team news",7)]; g=self.g(); g.check_feed_weeks({"season":2026,"week":9,"sources":s}); self.assertTrue(any("team news" in x for x in g.miss))
    def test_film_week6_fails(self):
        s=self.ok(); s[2]["data_week"]=6; g=self.g(); g.check_feed_weeks({"season":2026,"week":9,"sources":s}); self.assertTrue(any("film" in x and "behind" in x for x in g.miss),g.miss)
    def test_wrong_season_fails(self):
        s=self.ok()+[feed("coverage_matchups","StatRankings OL",8,season=2025)]; g=self.g(); g.check_feed_weeks({"season":2026,"week":9,"sources":s})
        self.assertTrue(any("2025" in x and "StatRankings" in x for x in g.miss))
    def test_missing_stamp_fails(self):
        s=self.ok(); del s[0]["data_week"]; g=self.g(); g.check_feed_weeks({"season":2026,"week":9,"sources":s}); self.assertTrue(any("data_week" in x for x in g.miss))
    def test_manifest_week_missing_fails(self):
        g=self.g(); g.check_feed_weeks({"sources":self.ok()}); self.assertTrue(any("season/week" in x for x in g.miss))
    def test_label_override(self):
        s=self.ok()+[feed("coverage_matchups","PFF matchups",8,kind="label")]; g=self.g(); g.check_feed_weeks({"season":2026,"week":9,"sources":s}); self.assertTrue(g.miss)
    def test_not_applied_before_week9(self):
        g=self.g("2026-11-01"); g.check_feed_weeks({"sources":[feed("film","film",6)]}); self.assertEqual(g.miss,[])

class FeedWeeksGate(Base):  # SRC-5 end to end through run_gate.py (other Week 9 checks may also fire; only SRC-5 lines asserted)
    def stamp(self,film=8):
        self.m.update(game_date="2026-11-05",season=2026,week=9)
        for s in self.m["sources"]:
            s.update(season=2026,data_week=9 if s["category"] in RG._src.LABEL_CATS else 8)
            if s["category"]=="film": s["data_week"]=film
        self.save()
    def test_current_feeds_no_src5(self):
        self.stamp(); c,o=self.run_gate(); self.assertNotIn("SRC-5",o)
    def test_film_week6_src5(self):
        self.stamp(film=6); c,o=self.run_gate(); self.assertNotEqual(c,0); self.assertIn("film/nfl_youtube: data through week 6, 2 week(s) behind",o)
class OddsPatch(unittest.TestCase):  # SRC-4
    P="/workspace/nfl-database/runs/2026-11-05_shared_src/pull_odds.py"
    def test_pull_odds_uses_pregame_guard(self):
        t=open(self.P).read(); self.assertIn("odds_pregame.pregame_events",t); self.assertIn("flag_inplay",t); self.assertIn('"inplay"',t)
        self.assertNotIn('"2026-11-01","2026-11-02"',t); self.assertNotIn("print(K",t)
    def test_pull_odds_drop_inplay_rows(self):
        spec=importlib.util.spec_from_file_location("po",self.P); po=importlib.util.module_from_spec(spec)
        sys.argv=["pull_odds.py","--lib"]; spec.loader.exec_module(po)
        rows=[["g","fd","m","p","Over",50,-110,"2026-11-05T23:00:00Z"],["g","fd","m","p","Over",50,-110,"2026-11-06T02:00:00Z"],["h","fd","m","p","Over",50,-110,"2026-11-05T23:00:00Z"]]
        keep,drop=po.split_inplay(rows,{"g":"2026-11-06T01:15:00Z"})
        self.assertEqual(len(keep),1); self.assertEqual(len(drop),2)  # live row + unknown-kickoff row both dropped
    def test_pull_props_none_line(self):
        t=open("/workspace/nfl-database/week8/lines/pull_props.py").read()
        self.assertNotIn("float(n['line'] or 0)",t); self.assertIn("NOLINE",t)

class W9Setup(unittest.TestCase):
    def test_feed_check_tool_reports(self):
        import feed_week_check as F
        r=F.check("/workspace/nfl-database/runs/2026-11-05_shared_src",season=2026,week=9)
        self.assertIn("feeds",r); self.assertTrue(all("status" in v for v in r["feeds"].values()))
if __name__=="__main__": unittest.main()
