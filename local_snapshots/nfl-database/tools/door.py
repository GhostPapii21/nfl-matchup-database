#!/usr/bin/env python3
"""THE LOCKED DOOR - the only way to make a slip (Rico 2026-11-03 00:32 ET).

  door.py test                       run the full suite; records pass/fail for the current code (needed for any stamp)
  door.py check <slip.json>          run every rule, print result, write nothing to approved/
  door.py build <slip.json>          PASS -> approved/<date>/<slip_id>.json with stamp; FAIL -> exit 1 + blocked/<date>/<slip_id>.md/.json
  door.py swap <slip_id>             propose next-best fully-passing leg(s) -> proposals/<slip_id>_swap.json (NOT applied)
  door.py swap <slip_id> --approve --approved-by Rico --at <ts> --text "<Rico's words>"   apply it (re-runs the door)
  door.py override <slip_id> --rule <id> [--rule <id>] --reason '...' --approved-by Rico --at <ts> --text "<Rico's words>"

Slip file: {"slip_id": "...", "date": "YYYY-MM-DD", "sport": "NFL", "legs": [{"run": "runs/<dir>", "leg": "<manifest leg name>"}]}
NBA slip: sport "NBA", legs [{"leg": "...", "gate_inputs": {...gates.evaluate kwargs...}}] - NBA logic unchanged, stamped only.
The CLI always uses the real clock (no --now). Rules come from rules/rulebook.py."""
import argparse, glob, hashlib, json, os, re, subprocess, sys
from datetime import datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); TOOLS = os.path.join(ROOT, "tools")
sys.path.insert(0, ROOT); sys.path.insert(0, TOOLS)
from rules import rulebook as rb
import depth_rule
NBA_DIR = "/workspace/nba-codex-2026-11-02"
PASSYDS_RX = re.compile(r"\bpass(?:ing)?[ _]?y(?:ar)?ds\b|\bpassyds\b", re.I)
TD_RX = re.compile(r"\bTDs?\b|touchdown|anytime", re.I)
RUSH_RX = re.compile(r"rush", re.I)

def _p(*a): return os.path.join(ROOT, *a)
OUT = os.environ.get("DOOR_OUT") or ROOT   # where approved/ blocked/ proposals/ alerts/ overrides.log teams/ .door/ live (tests point this at a tmp dir)
def _o(*a): return os.path.join(OUT, *a)
def canon(o): return json.dumps(o, sort_keys=True, separators=(",", ":"), default=str)

# ---------------- test-suite status ----------------
def code_hash():
    h = hashlib.sha256()
    for f in sorted(glob.glob(_p("tools", "*.py")) + glob.glob(_p("tools", "tests", "*.py")) + glob.glob(_p("rules", "*.py"))):
        h.update(os.path.relpath(f, ROOT).encode()); h.update(open(f, "rb").read())
    return h.hexdigest()[:16]
def status_f(): return _o(".door", "test_status.json")
def run_tests():
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", _p("tools", "tests")], capture_output=True, text=True, cwd=ROOT)
    tail = (r.stdout.strip().splitlines() or [""])[-1]
    st = dict(passed=r.returncode == 0, summary=tail, code_hash=code_hash(), rulebook=rb.version(), at=datetime.now().isoformat(timespec="seconds"))
    os.makedirs(os.path.dirname(status_f()), exist_ok=True); json.dump(st, open(status_f(), "w"), indent=1); return st
def test_status():
    try: st = json.load(open(status_f()))
    except Exception: return dict(passed=False, why="no test run recorded (run: door.py test)")
    if st.get("code_hash") != code_hash(): return dict(st, passed=False, why="code changed since last test run (run: door.py test)")
    return st

# ---------------- leg + slip rules ----------------
def F(rule, leg, value, threshold, words): return dict(rule=rule, sev=rb.rule(rule)["sev"], leg=leg, value=value, threshold=threshold, words=words)

def run_gate(run_dir, now):
    cmd = [sys.executable, os.path.join(TOOLS, "run_gate.py"), run_dir, "--now", now.strftime("%Y-%m-%dT%H:%M")]
    r = subprocess.run(cmd, capture_output=True, text=True); out = r.stdout + r.stderr
    m = re.search(r"^Live legs: (.*)$", out, re.M); live = []
    if m and m[1].strip() != "none":
        try: live = eval(m[1], {"__builtins__": {}})   # gate prints a python list literal
        except Exception: live = []
    se = out.split("SCHEME_EDGE ALERT", 1)[1].split("\nMISSES", 1)[0] if "SCHEME_EDGE ALERT" in out else ""
    return dict(ok=r.returncode == 0, live=live, out=out, scheme_alert=se)

def load_leg(run_dir, name):
    try: m = json.load(open(os.path.join(run_dir, "run_manifest.json")))
    except Exception: return None, None
    for l in m.get("legs", []):
        if l.get("name") == name: return m, l
    return m, None

def leg_rules(n, l, m):
    """Door-level per-leg rules on top of run_gate (which already ran §7, edge, N1-N3, coverage age, forecast, depth...)."""
    f = []
    price = l.get("price", l.get("price_fd"))
    if price in (None, "") or l.get("no_vig") in (None, ""): f.append(F("FAIR_PRICE", n, dict(price=price, no_vig=l.get("no_vig")), "both present", "no real book price / no-vig fair price - missing data"))
    elif float(price) <= rb.param("SHORT_PRICE", "price"): f.append(F("SHORT_PRICE", n, price, rb.param("SHORT_PRICE", "price"), f"priced {price}, at or shorter than -250 - Rico must see it"))
    inj = l.get("injury_status", (l.get("press") or {}).get("injury_status"))
    if inj in (None, ""): f.append(F("INJURY", n, None, "injury_status", "injury status missing - missing data, fail closed"))
    elif str(inj).lower() in rb.param("INJURY", "bad"): f.append(F("INJURY", n, inj, "active/questionable", f"player is {inj}"))
    if l.get("weather_stop") or (l.get("press") or {}).get("weather_stop"): f.append(F("WEATHER", n, True, False, "weather stop on this game"))
    rf = l.get("recent_form") or {}
    if not rf.get("values") or not rf.get("source"): f.append(F("RECENT_DATA", n, None, "recent_form values+source", "recent form (last 4 with current QB) missing - missing data"))
    if TD_RX.search(str(l.get("name", "")) + " " + str(l.get("market", ""))): f.append(F("NO_TD", n, l.get("name"), "no TD legs", "touchdown leg on a main slip"))
    if PASSYDS_RX.search(str(l.get("name", "")) + " " + str(l.get("market", ""))): f.append(F("NO_PASS_YDS", n, l.get("name"), "no passing-yards legs (main or alt)", "passing-yards leg on a slip"))
    if str(l.get("type")).upper() == "RB" and str(l.get("side")).lower() == "over" and RUSH_RX.search(str(l.get("name", "")) + str(l.get("market", ""))):
        r = l.get("rb_role") or {}
        if r.get("share60_3of4") is None or not r.get("source"): f.append(F("RB_TRAIL", n, None, "rb_role share60_3of4+source", "RB 60%-carries-in-3-of-4 check missing - missing data"))
        elif not r["share60_3of4"]: f.append(F("RB_TRAIL", n, r.get("shares"), ">=60% in 3 of last 4", "RB did not have 60%+ of carries in 3 of his last 4"))
        elif r.get("may_trail") and float(r.get("tgt_pg") or 0) < rb.param("RB_TRAIL", "tgt"): f.append(F("RB_TRAIL", n, r.get("tgt_pg"), ">=4 targets/g", "team may trail and the RB is under 4 targets a game"))
    ok, why = depth_rule.evaluate(l)
    if not ok: f.append(F("DEPTH_RECEIVER", n, why, "all depth conditions", "; ".join(why)))
    return f

def team_files(teams):
    f, loaded = [], {}
    for t in sorted(teams):
        p = _o(rb.param("TEAM_FILES", "path").format(team=t))
        try: loaded[t] = json.load(open(p))
        except Exception: f.append(F("TEAM_FILES", "-", t, os.path.relpath(p, OUT), f"team file for {t} missing/unreadable ({os.path.relpath(p, OUT)}) - build stops"))
    return f, loaded

def ledger():
    r = subprocess.run([sys.executable, os.path.join(TOOLS, "ledger_coverage_check.py")], capture_output=True, text=True)
    return [] if r.returncode == 0 else [F("LEDGER", "-", r.stdout.strip(), "exit 0", "a logged game is missing from defender_ledger.csv")]

def evaluate(slip, now):
    fails, legs, gates, alerts, teams = [], [], {}, [], set()
    if slip.get("sport", "NFL").upper() == "NBA": return evaluate_nba(slip)
    for x in slip.get("legs", []):
        rd = x.get("run") if os.path.isabs(x.get("run", "")) else _p(x.get("run", ""))
        n = x.get("leg")
        if rd not in gates: gates[rd] = run_gate(rd, now)
        g = gates[rd]
        m, l = load_leg(rd, n)
        if l is None: fails.append(F("GATE_PASS", n, rd, "leg in run_manifest.json", "leg not found in its run - hand-built leg")); continue
        if not g["ok"]: fails.append(F("GATE_PASS", n, "FAIL", "PASS", "the run did not pass run_gate on the real clock"))
        elif n not in g["live"]: fails.append(F("GATE_PASS", n, "not live", "live", "leg is not a live leg in the passing gate run"))
        if g["scheme_alert"] and n in g["scheme_alert"]: alerts.append(dict(leg=n, breakdown=g["scheme_alert"].strip()))
        fails += leg_rules(n, l, m)
        gm = l.get("game") or m.get("game") or ""
        teams |= set(t for t in re.split(r"[@ ]+(?:vs\.? )?", gm) if t) | {t for t in (l.get("team"), l.get("opp")) if t}
        legs.append(dict(ref=x, leg=l, game=gm))
    k = len(slip.get("legs", []))
    if not rb.param("SLIP_SIZE", "min") <= k <= rb.param("SLIP_SIZE", "max"): fails.append(F("SLIP_SIZE", "-", k, "3-4", f"slip has {k} legs; main slips are 3 or 4"))
    d = sum(1 for z in legs if depth_rule.is_depth(z["leg"]) and str(z["leg"].get("side")).lower() == "over")
    if d > rb.param("DEPTH_CAP", "max"): fails.append(F("DEPTH_CAP", "-", d, 1, f"{d} depth receivers on one slip (warning only)"))
    tf, loaded = team_files(teams); fails += tf; fails += ledger()
    for a in alerts: fails.append(F("SCHEME_EDGE", a["leg"], "under +3 / sim flag", "+3", "SCHEME_EDGE leg under +3 - check at the real price; full breakdown in alerts/"))
    return dict(fails=fails, legs=legs, alerts=alerts, teams=sorted(teams), team_files=sorted(loaded), gate_out={k2: v["out"] for k2, v in gates.items()})

def evaluate_nba(slip):
    sys.path.insert(0, NBA_DIR); import gates as G
    fails, legs = [], []
    for x in slip.get("legs", []):
        try: r = G.evaluate(**x["gate_inputs"])
        except Exception as e: fails.append(F("GATE_PASS", x.get("leg"), str(e), "gates.evaluate", "NBA gate inputs missing/invalid")); continue
        bad = r.get("failures") if isinstance(r, dict) else None
        if bad or (isinstance(r, dict) and r.get("unknown")): fails.append(F("GATE_PASS", x.get("leg"), bad or r.get("unknown"), "no failures/unknowns", "NBA gates.py did not pass"))
        legs.append(dict(ref=x, leg=r))
    return dict(fails=fails, legs=legs, alerts=[], teams=[], team_files=[], gate_out={})

def blocking(fails): return [f for f in fails if f["sev"] == "BLOCK"]

def stamp_payload(slip, res, status, overrides=None, ts=None):
    return dict(slip=slip, legs=[z["leg"] for z in res["legs"]], status=status, rulebook_version=rb.version(),
                test_status=dict(passed=ts.get("passed"), summary=ts.get("summary"), code_hash=ts.get("code_hash")),
                flags=[f for f in res["fails"] if f["sev"] == "FLAG"], warns=[f for f in res["fails"] if f["sev"] == "WARN"],
                overrides=overrides or [], team_files=res["team_files"])
def stamp(payload): return hashlib.sha256(canon(payload).encode()).hexdigest()

def words(slip, res):
    L = [f"# BLOCKED slip {slip.get('slip_id')} ({slip.get('date')})", "", "| rule | sev | leg | value | threshold | plain words |", "|---|---|---|---|---|---|"]
    L += [f"| {f['rule']} | {f['sev']} | {f['leg']} | {f['value']} | {f['threshold']} | {f['words']} |" for f in res["fails"]]
    L += ["", "Choices (never automatic, Rico only):", f"1. SWAP: `python3 tools/door.py swap {slip.get('slip_id')}` then `--approve --approved-by Rico --at <ts> --text '<Rico>'`",
          f"2. OVERRIDE: `python3 tools/door.py override {slip.get('slip_id')} --rule <id> --reason '...' --approved-by Rico --at <ts> --text '<Rico>'`"]
    return "\n".join(L) + "\n"

def write_alerts(slip, res):
    if not res["alerts"] and not any(f["rule"] == "SCHEME_EDGE" for f in res["fails"]): return None
    p = _o("alerts", slip["date"], f"{slip['slip_id']}_scheme_edge.md"); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(f"# SCHEME_EDGE alert - slip {slip['slip_id']}\n\n" + "\n\n".join(f"## {a['leg']}\n```\n{a['breakdown']}\n```" for a in res["alerts"]) + "\n"); return p

def build(slip, now=None, write=True, overrides=None):
    now = now or datetime.now()
    res = evaluate(slip, now); ts = test_status()
    if not ts.get("passed"): res["fails"].append(F("TEST_SUITE", "-", ts.get("why") or ts.get("summary"), "suite passed on current code", "test suite not green for the current code"))
    ov_rules = {o["rule"] for o in (overrides or [])}
    blk = [f for f in blocking(res["fails"]) if f["rule"] not in ov_rules or f["rule"] in ("TEST_SUITE", "OVERRIDE")]
    status = "BLOCKED" if blk else ("OVERRIDDEN" if overrides else "PASS")
    out = dict(status=status, fails=res["fails"], blocking=blk, alerts=res["alerts"], res=res)
    if not write: return out
    sid, day = slip["slip_id"], slip["date"]
    out["alert_file"] = write_alerts(slip, res)
    if blk:
        b = _o("blocked", day); os.makedirs(b, exist_ok=True)
        json.dump(dict(slip=slip, fails=res["fails"], checked_at=now.isoformat(timespec="minutes"), rulebook_version=rb.version()), open(os.path.join(b, f"{sid}.json"), "w"), indent=1, default=str)
        open(os.path.join(b, f"{sid}.md"), "w").write(words(slip, res)); out["file"] = os.path.join(b, f"{sid}.md")
    else:
        pl = stamp_payload(slip, res, status, overrides, ts); a = _o("approved", day); os.makedirs(a, exist_ok=True)
        rec = dict(payload=pl, stamp=stamp(pl), stamped_at=now.isoformat(timespec="minutes"))
        json.dump(rec, open(os.path.join(a, f"{sid}.json"), "w"), indent=1, default=str); out["file"] = os.path.join(a, f"{sid}.json"); out["stamp"] = rec["stamp"]
    return out

# ---------------- approval (swap / override) ----------------
BOT_RX = re.compile(r"ghost|blitz|grok|bot|agent|codex|claude|gpt|assistant", re.I)
RELAY_RX = re.compile(r"relay|on behalf|said (that )?rico|rico said|per rico|forwarded", re.I)
def check_approval(by, at, text):
    if not by: return "override/swap needs --approved-by Rico"
    if by not in rb.param("OVERRIDE", "approvers") or BOT_RX.search(by): return f"approved-by {by!r} is not Rico; bots can't self-approve"
    if not at: return "needs --at <timestamp> of Rico's approval"
    try: datetime.fromisoformat(at)
    except ValueError: return f"--at {at!r} is not an ISO timestamp"
    if not (text or "").strip(): return "needs --text with Rico's own approval words"
    if RELAY_RX.search(text): return "relayed approval doesn't count - Rico must approve directly"
    return None

def find_blocked(sid):
    c = sorted(glob.glob(_o("blocked", "*", f"{sid}.json")))
    return json.load(open(c[-1])) if c else None

def propose_swap(sid, now=None):
    now = now or datetime.now(); b = find_blocked(sid)
    if not b: return dict(error=f"no blocked report for {sid}")
    slip = b["slip"]; bad = {f["leg"] for f in b["fails"] if f["sev"] == "BLOCK" and f["leg"] != "-"}
    keep = [x for x in slip["legs"] if x["leg"] not in bad]; used = {x["leg"] for x in slip["legs"]}
    cands = []
    for rd in sorted({x["run"] for x in slip["legs"]}):
        absd = rd if os.path.isabs(rd) else _p(rd); g = run_gate(absd, now)
        if not g["ok"]: continue
        m = json.load(open(os.path.join(absd, "run_manifest.json")))
        for l in m.get("legs", []):
            if l["name"] in used or l["name"] not in g["live"]: continue
            if blocking(leg_rules(l["name"], l, m)): continue
            cands.append((float(l.get("edge_3", l.get("edge", 0)) or 0), rd, l["name"]))
    cands.sort(reverse=True); need = len(slip["legs"]) - len(keep)
    if need == 0 or len(cands) < need: return dict(error=f"no fully-passing replacement ({len(cands)} candidates for {need} slots)", slip_id=sid)
    new = dict(slip, slip_id=f"{sid}_swap", legs=keep + [dict(run=r, leg=n) for _, r, n in cands[:need]], swapped_from=sid)
    pre = build(new, now, write=False)
    prop = dict(proposal=new, replaced=sorted(bad), with_=[n for _, _, n in cands[:need]], would_status=pre["status"],
                would_stamp=stamp(stamp_payload(new, pre["res"], pre["status"], None, test_status())) if pre["status"] == "PASS" else None, applied=False)
    p = _o("proposals", f"{sid}_swap.json"); os.makedirs(os.path.dirname(p), exist_ok=True); json.dump(prop, open(p, "w"), indent=1, default=str)
    prop["file"] = p; return prop

def apply_swap(sid, by, at, text, now=None):
    e = check_approval(by, at, text)
    if e: return dict(error=e)
    p = _o("proposals", f"{sid}_swap.json")
    if not os.path.exists(p): return dict(error="no swap proposal; run door.py swap <slip_id> first")
    prop = json.load(open(p)); new = dict(prop["proposal"], swap_approval=dict(by=by, at=at, text=text))
    r = build(new, now); prop["applied"] = r["status"] == "PASS"; json.dump(prop, open(p, "w"), indent=1, default=str); return r

def override(sid, rules, reason, by, at, text, now=None):
    e = check_approval(by, at, text)
    if e: return dict(error=e)
    if not (reason or "").strip(): return dict(error="override needs --reason")
    if not rules: return dict(error="override needs at least one --rule")
    b = find_blocked(sid)
    if not b: return dict(error=f"no blocked report for {sid}")
    failed = {f["rule"] for f in b["fails"] if f["sev"] == "BLOCK"}
    bad = [r for r in rules if r not in failed or r in ("TEST_SUITE", "OVERRIDE")]
    if bad: return dict(error=f"can only override rules that actually blocked this slip (not TEST_SUITE): {bad}")
    ovs = [dict(rule=r, reason=reason, approved_by=by, at=at, text=text) for r in rules]
    r = build(b["slip"], now, overrides=ovs)
    if r["status"] == "OVERRIDDEN":
        with open(_o("overrides.log"), "a") as f: f.write(canon(dict(slip_id=sid, date=b["slip"]["date"], rules=rules, reason=reason, approved_by=by, at=at, text=text, stamp=r.get("stamp"), logged=datetime.now().isoformat(timespec="seconds"))) + "\n")
    return r

def _print(r):
    if r.get("error"): print("DOOR: REFUSED -", r["error"]); return 1
    if "proposal" in r:
        print(f"DOOR: SWAP PROPOSED (not applied) replace {r['replaced']} with {r['with_']}; would be {r['would_status']} -> {r['file']}"); return 0
    print(f"DOOR: {r['status']}" + (f"  stamp={r['stamp']}" if r.get("stamp") else ""))
    for f in r["fails"]: print(f"  [{f['sev']}] {f['rule']} leg={f['leg']}: {f['words']} (value {f['value']} vs {f['threshold']})")
    if r.get("file"): print("  ->", r["file"])
    if r.get("alert_file"): print("  SCHEME_EDGE alert ->", r["alert_file"])
    return 0 if r["status"] in ("PASS", "OVERRIDDEN") else 1

def main(argv=None):
    a = argparse.ArgumentParser(); a.add_argument("cmd", choices=["test", "check", "build", "swap", "override"]); a.add_argument("target", nargs="?")
    a.add_argument("--approve", action="store_true"); a.add_argument("--approved-by"); a.add_argument("--at"); a.add_argument("--text")
    a.add_argument("--rule", action="append"); a.add_argument("--reason")
    o = a.parse_args(argv)
    if o.cmd == "test": st = run_tests(); print("TESTS:", "PASS" if st["passed"] else "FAIL", st["summary"]); return 0 if st["passed"] else 1
    if o.cmd in ("check", "build"):
        r = build(json.load(open(o.target)), write=o.cmd == "build")
        if o.cmd == "check": r.pop("file", None)
        return _print(r)
    if o.cmd == "swap": return _print(apply_swap(o.target, o.approved_by, o.at, o.text) if o.approve else propose_swap(o.target))
    if o.cmd == "override": return _print(override(o.target, o.rule or [], o.reason, o.approved_by, o.at, o.text))

if __name__ == "__main__": sys.exit(main())
