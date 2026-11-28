"""Research-only matchup adjustments from existing pregame board splits."""
import numpy as np

def mixture(a,b,w,key):
    return (1-w)*float(a[key])+w*float(b[key])

def ratio(a,b):
    return float(np.clip(a/b, .75, 1.25)) if b>0 else 1.

def profiles(board):
    out={}
    for s in board.get("sides",{}).values():
        q=s.get("qb") or {}
        c=s.get("coverage_profile") or {}
        old=q.get("last_season") or {}
        now=q.get("this_season") or {}
        p={"qb_id":q.get("player_id"),"completion":1.,"yards_per_completion":1.,"attempts":1.,"evidence":{}}
        for label,lo,hi,weight in (
            ("coverage",old.get("vs_zone"),old.get("vs_man"),c.get("man_rate")),
            ("pressure",old.get("clean"),old.get("pressured"),c.get("pressure_rate")),
            ("blitz",now.get("no_blitz"),now.get("vs_blitz"),(c.get("blitz_this_season") or {}).get("blitz_rate"))):
            if not lo or not hi or weight is None or not 0<=weight<=1: continue
            if min(lo.get("attempts",0),hi.get("attempts",0))<30: continue
            baseline=hi["dropbacks"]/(lo["dropbacks"]+hi["dropbacks"])
            cr=ratio(mixture(lo,hi,weight,"completion_pct"),mixture(lo,hi,baseline,"completion_pct"))
            yp=ratio(mixture(lo,hi,weight,"yards_per_attempt"),mixture(lo,hi,baseline,"yards_per_attempt"))
            ar=ratio(1-mixture(lo,hi,weight,"sack_rate"),1-mixture(lo,hi,baseline,"sack_rate"))
            p["evidence"][label]={"expected_rate":weight,"historical_rate":baseline,"completion_factor":cr,"yards_per_attempt_factor":yp,"attempt_factor":ar,"samples":[lo["attempts"],hi["attempts"]]}
        # Pressure and blitz overlap: use pressure when available, blitz as fallback.
        for label in ("coverage","pressure" if "pressure" in p["evidence"] else "blitz"):
            e=p["evidence"].get(label)
            if e:
                p["completion"]*=e["completion_factor"]
                p["yards_per_completion"]*=e["yards_per_attempt_factor"]/e["completion_factor"]
                p["attempts"]*=e["attempt_factor"]
        p["status"]="EXPERIMENTAL_UNVALIDATED" if p["evidence"] else "MISSING"
        out[s["offense"]]=p
    return out
