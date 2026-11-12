"""Generates fixtures/valid_run (a complete, passing run). Now = 2026-11-01T12:00 ET."""
import json, os
PHASES = ["1 Data pull","2 Opportunity","3 Defensive profile","4 Defender coverage","5 Pressure/blitz/checkdown",
 "6 QB grade card","7 Role/RB rules","8 Injuries","9 NGS","10 Film","11 Environment","12 Source audit",
 "13 Game script","14 Models/edge","15 Inactives"]
LEGS = [("Tee Higgins rec yds o58.5 -115","WR",True),("Chase Brown rush yds o62.5 -110","RB",False)]
def build(d):
    os.makedirs(d, exist_ok=True)
    rows = ["| Leg | Phase | Status | Number | Source | Pulled (ET) |","|---|---|---|---|---|---|"]
    for leg,t,rec in LEGS:
        for p in PHASES:
            st = "N/A" if (p.startswith("4 ") and not rec) else "PASS"
            rows.append(f"| {leg} | {p} | {st} | 1.0 | nflverse pbp | 2026-11-01 11:30 |")
    open(f"{d}/checklist.md","w").write("\n".join(rows)+"\n")
    open(f"{d}/report.md","w").write("# Report\n")
    src = lambda c,n,t: {"category":c,"name":n,"url_or_file":f"https://example.org/{n}","pulled_et":t,"tool":"curl"}
    m = {"game":"TEN@CIN","kickoff_et":"2026-11-01T13:00",
      "sources":[src("core_stats_pbp","nflverse","2026-11-01T09:00"),src("coverage_matchups","ftn","2026-11-01T09:00"),
        src("ngs","ngs","2026-11-01T09:00"),src("film","nfl_youtube","2026-11-01T09:00"),
        src("injuries_news","espn_injuries","2026-11-01T10:00"),src("weather","nws","2026-11-01T10:00"),
        src("odds_props","fanduel","2026-11-01T11:30")],
      "pressure_inputs":{k:{"value":0.3,"source":"ftn","pulled_et":"2026-11-01T09:00"} for k in ("blitz_rate","pressure_rate","checkdown_share")},
      "sims":[{"model":mo,"n":100000,"seed":42,"legs":{LEGS[0][0]:{"p":0.58,"median":64},LEGS[1][0]:{"p":0.57,"median":68}}}
              for mo in ("monte_carlo","bias","game_randomness")],
      "legs":[]}
    for leg,t,rec in LEGS:
        L={"name":leg,"type":t,"receiving":rec,"status":"PASS","side":"over","line":58.5 if rec else 62.5,
           "no_vig":0.52,"gaps":[],"price_fd":-115 if rec else -110,
           "recent_form":{"values":[90,80,75,40] if rec else [70,65,80,40],"games":["2026_04","2026_05","2026_06","2026_07"],
                          "qb":"J. Burrow","source":"nflverse play_by_play_2026.parquet","pulled_et":"2026-11-01T09:00"}}
        if t=="WR": L["wr_rank"]=2   # depth_rule now fails closed on a missing WR rank (Ghost6 audit 2026-11-03); Higgins = CIN WR2
        if t=="RB": L["carry_share"]={"value":0.68,"source":"nflverse play_by_play_2026.parquet"}
        if rec:
            L["coverage"]={"defenders":[{"name":"J. Flott","targets":40,"comp_pct":0.6,"ypt":7.1,"source":"pfr_cache","pulled_et":"2026-11-01T09:00","primary":True}],
              "man_zone":{"man":0.3,"zone":0.7,"source":"ftn","pulled_et":"2026-11-01T09:00"},
              "mof":{"closed":0.55,"open":0.45,"source":"ftn","pulled_et":"2026-11-01T09:00"}}
        m["legs"].append(L)
    json.dump(m, open(f"{d}/run_manifest.json","w"), indent=2)
if __name__=="__main__":
    build(os.path.join(os.path.dirname(os.path.abspath(__file__)),"fixtures","valid_run"))
