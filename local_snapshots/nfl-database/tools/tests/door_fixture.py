"""Builds a Week-9 run that passes run_gate at NOW, with extra cloned legs, plus a DOOR_OUT tmp dir with team files + green test status."""
import copy, json, os, sys, tempfile, unittest
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import test_press_live as tpl
NOW = "2026-11-08T12:00"
class _L(tpl.LiveRun):
    def runTest(self): pass
def clone(d, src, new, **kw):
    mp = os.path.join(d, "run_manifest.json"); m = json.load(open(mp))
    l = copy.deepcopy(next(x for x in m["legs"] if x["name"] == src)); l["name"] = new; l.update(kw); m["legs"].append(l)
    for s in m["sims"]: s["legs"][new] = dict(s["legs"][src])
    json.dump(m, open(mp, "w"))
    for f in ("checklist.md", "report.md"):
        p = os.path.join(d, f); t = open(p).read()
        rows = [r.replace(src, new) for r in t.splitlines() if src in r]
        open(p, "w").write(t + ("\n" if not t.endswith("\n") else "") + "\n".join(rows) + "\n")
def edit_leg(d, name, **kw):
    mp = os.path.join(d, "run_manifest.json"); m = json.load(open(mp))
    for l in m["legs"]:
        if l["name"] == name: l.update(kw)
    json.dump(m, open(mp, "w"))
def make():
    x = _L(); x.setUp(); d = x.d
    out = tempfile.mkdtemp(); os.environ["DOOR_OUT"] = out
    os.makedirs(os.path.join(out, "teams")); [json.dump({"team": t}, open(os.path.join(out, "teams", f"{t}.json"), "w")) for t in ("TEN", "CIN")]
    edit_leg(d, "Tee Higgins rec yds o58.5 -115", injury_status="Active")
    edit_leg(d, "Chase Brown rush yds o62.5 -110", injury_status="Active", rb_role=dict(share60_3of4=True, shares=[.7, .65, .62, .5], tgt_pg=4.5, may_trail=True, source="nflverse pbp"))
    clone(d, "Tee Higgins rec yds o58.5 -115", "Ja'Marr Chase rec yds o70.5 -120", price_fd=-120, edge_3=0.06)
    clone(d, "Tee Higgins rec yds o58.5 -115", "Mike Gesicki rec yds o30.5 -110", price_fd=-110, edge_3=0.04)
    return d, out
def slip(d, legs, sid="T1"):
    return dict(slip_id=sid, date="2026-11-08", sport="NFL", legs=[dict(run=d, leg=n) for n in legs])
def green(door):
    os.makedirs(door._o(".door"), exist_ok=True)
    json.dump(dict(passed=True, summary="test", code_hash=door.code_hash(), rulebook=door.rb.version()), open(door.status_f(), "w"))
