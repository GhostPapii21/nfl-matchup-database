#!/usr/bin/env python3
"""verify_stamp.py <approved slip json> - exit 0 only if the slip came out of tools/door.py unchanged.
Anything shown to Rico or posted to Suave Bets must pass this. A hand-built or edited slip fails."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import door
from rules import rulebook as rb
def verify(path):
    try: rec = json.load(open(path))
    except Exception as e: return False, f"unreadable: {e}"
    if not isinstance(rec, dict) or "stamp" not in rec or "payload" not in rec: return False, "no door stamp - hand-built slip"
    if door.stamp(rec["payload"]) != rec["stamp"]: return False, "stamp does not match contents - slip was edited after the door"
    p = rec["payload"]
    if p.get("status") not in ("PASS", "OVERRIDDEN"): return False, f"status {p.get('status')}"
    if p.get("rulebook_version") != rb.version(): return False, "rulebook changed since stamp - rebuild through the door"
    if not (p.get("test_status") or {}).get("passed"): return False, "stamped without a green test suite"
    if os.path.commonpath([os.path.abspath(path), door._o("approved")]) != door._o("approved"): return False, "not in approved/ - not issued by the door"
    return True, p["status"] + (f" (overridden: {[o['rule'] for o in p['overrides']]})" if p.get("overrides") else "")
if __name__ == "__main__":
    ok, why = verify(sys.argv[1]); print(("STAMP OK: " if ok else "STAMP FAIL: ") + why); sys.exit(0 if ok else 1)
