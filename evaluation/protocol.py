"""NFL-44 pristine evaluation protocol + NFL-45 quote provenance ledger (research only; no stakes).

    python3 -m evaluation.protocol freeze     # hash protocol + all not-yet-kicked-off locks -> PROTOCOL_FREEZE.json
    python3 -m evaluation.protocol ledger     # quote provenance ledger -> evaluation/quote_ledger.json
    python3 -m evaluation.protocol evaluate   # aggregate SCORE.json files -> evaluation/EVALUATION.json

Fail-closed: no freeze -> every game NO_PROTOCOL_FREEZE; below min coverage -> UNSCORABLE_INSUFFICIENT_COVERAGE;
no frozen quote -> NOLINE (market comparison not scored). independently_calibrated is always false here:
only the raw model is scored; no market-anchored output exists (kept separate by construction).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "evaluation"
PROTOCOL = EVAL / "PRISTINE_EVALUATION_PROTOCOL.json"
FREEZE = EVAL / "PROTOCOL_FREEZE.json"


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _utc(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)


def _locks(root: Path):
    return sorted((root / "snapshots").glob("*/*/LOCK.json"))


def freeze(root: Path = ROOT, now: datetime | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    fz = root / "evaluation/PROTOCOL_FREEZE.json"
    if fz.exists():
        raise SystemExit("freeze: REFUSED, PROTOCOL_FREEZE.json already exists (locks made after it are covered)")
    locks = []
    for p in _locks(root):
        lk = json.loads(p.read_text())
        if _utc(lk["kickoff_utc"]) <= now or (p.parent / "SCORE.json").exists():
            continue  # outcome may be known: never hashed into the freeze
        locks.append({"path": str(p.relative_to(root)), "lock_sha256": _sha(p), "game_id": lk["game_id"],
                      "kickoff_utc": lk["kickoff_utc"], "locked_utc": lk["locked_utc"]})
    out = {"schema": "protocol-freeze/1", "frozen_utc": now.isoformat(timespec="seconds"),
           "protocol_sha256": _sha(root / "evaluation/PRISTINE_EVALUATION_PROTOCOL.json"),
           "historical_pristine_claim": False, "locks": locks}
    fz.write_text(json.dumps(out, indent=1) + "\n")
    return out


def quote_ledger(root: Path = ROOT) -> dict:
    rows = []
    for p in _locks(root):
        lk = json.loads(p.read_text())
        inp = lk.get("inputs") or {}
        files = sorted((p.parent / "inputs").glob("team_prices*.json"))
        base = {"game_id": lk["game_id"], "lock": str(p.parent.relative_to(root)),
                "source_origin": inp.get("price_freeze_origin") or inp.get("packet_path"),
                "source_sha256": inp.get("price_freeze_sha256") or inp.get("packet_sha256"),
                "pulled_utc": inp.get("price_freeze_pulled_utc"), "price_status": inp.get("price_status", "NOLINE")}
        quotes = []
        for f in files:
            for r in json.loads(f.read_text()).get("rows") or []:
                if r.get("player") or r.get("price_a") is None:
                    continue
                quotes.append({k: r.get(k) for k in ("book", "market", "side_a", "side_b", "line", "price_a", "price_b",
                                                    "novig_a", "novig_b", "book_last_update", "reference_only")})
        if not quotes or not base["pulled_utc"] or _utc(base["pulled_utc"]) >= _utc(lk["locked_utc"]):
            base["price_status"] = "NOLINE"
        rows.append({**base, "n_quotes": len(quotes), "quotes": quotes})
    return {"schema": "quote-ledger/1", "built_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "independently_calibrated": False, "raw_model_only": True, "market_anchored": "NOT_PRODUCED",
            "games": rows}


def classify(p: Path, root: Path, fz: dict | None, proto: dict) -> tuple[str, dict | None]:
    lk = json.loads(p.read_text())
    if fz is None:
        return "NO_PROTOCOL_FREEZE", None
    listed = {x["path"]: x["lock_sha256"] for x in fz["locks"]}
    rel = str(p.relative_to(root))
    if not ((listed.get(rel) == _sha(p)) or _utc(lk["locked_utc"]) > _utc(fz["frozen_utc"])):
        return "NOT_COVERED_BY_PROTOCOL_FREEZE", None
    for f, h in (lk.get("files") or {}).items():
        if not (p.parent / f).exists() or _sha(p.parent / f) != h:
            return "LOCK_HASH_MISMATCH", None
    if _utc(lk["locked_utc"]) >= _utc(lk["kickoff_utc"]):
        return "LOCKED_AFTER_KICKOFF", None
    if lk.get("code_dirty") is not False:
        return "CODE_DIRTY", None
    if (lk.get("sim") or {}).get("n") != proto["eligible_snapshot"]["n_sims"]:
        return "N_SIMS_NOT_100K", None
    if lk.get("asof_checks") != "PASS":
        return "ASOF_NOT_PASS", None
    sc = p.parent / "SCORE.json"
    if not sc.exists():
        return "NOT_FINAL", None
    return "SCORED", json.loads(sc.read_text())


def evaluate(root: Path = ROOT) -> dict:
    proto = json.loads((root / "evaluation/PRISTINE_EVALUATION_PROTOCOL.json").read_text())
    fzp = root / "evaluation/PROTOCOL_FREEZE.json"
    fz = json.loads(fzp.read_text()) if fzp.exists() else None
    if fz and fz["protocol_sha256"] != _sha(root / "evaluation/PRISTINE_EVALUATION_PROTOCOL.json"):
        raise SystemExit("evaluate: REFUSED, protocol changed after freeze")
    ledger = {g["lock"]: g for g in quote_ledger(root)["games"]}
    by_game: dict[str, list[Path]] = {}
    for p in _locks(root):
        by_game.setdefault(json.loads(p.read_text())["game_id"], []).append(p)
    games, scored = [], []
    for gid, ps in sorted(by_game.items()):
        ps = sorted(ps, key=lambda q: json.loads(q.read_text())["locked_utc"])
        for i, p in enumerate(ps):
            status, sc = classify(p, root, fz, proto)
            if status == "SCORED" and any(classify(q, root, fz, proto)[0] in ("SCORED", "NOT_FINAL") for q in ps[i + 1:]):
                status, sc = "DUPLICATE_LATER_LOCK", None
            line = (ledger.get(str(p.parent.relative_to(root))) or {}).get("price_status", "NOLINE")
            rec = {"game_id": gid, "lock": str(p.parent.relative_to(root)), "status": status,
                   "market_comparison": "NOLINE" if line == "NOLINE" else "SCORED_VS_FROZEN_QUOTES"}
            if sc:
                rec["metrics"] = {k: sc["metrics"].get(k) for k in proto["primary_metrics"] + proto["secondary_metrics"]}
                if line == "NOLINE":
                    rec["metrics"]["brier_model_mean_lines"] = rec["metrics"]["brier_book_mean_lines"] = None
                scored.append(rec)
            games.append(rec)
    weeks = {g["game_id"].split("_")[1] for g in scored}
    need = proto["min_coverage"]
    agg = {}
    for k in proto["primary_metrics"]:
        v = [g["metrics"][k] for g in scored if g["metrics"].get(k) is not None]
        agg[k] = (sum(v) / len(v)) if v else None
    status = "OK" if len(scored) >= need["games_scored"] and len(weeks) >= need["weeks"] else proto["insufficient_coverage_status"]
    return {"schema": "evaluation/1", "status": status, "games_scored": len(scored), "weeks_scored": sorted(weeks),
            "min_coverage": need, "aggregate_primary": agg, "historical_pristine_claim": False,
            "independently_calibrated": False, "games": games}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["freeze", "ledger", "evaluate"])
    a = ap.parse_args(argv)
    if a.cmd == "freeze":
        r = freeze(); print(f"freeze: {len(r['locks'])} locks hashed at {r['frozen_utc']}")
    elif a.cmd == "ledger":
        r = quote_ledger(); (EVAL / "quote_ledger.json").write_text(json.dumps(r, indent=1) + "\n")
        print(f"ledger: {len(r['games'])} locks, NOLINE={sum(g['price_status']=='NOLINE' for g in r['games'])}")
    else:
        r = evaluate(); (EVAL / "EVALUATION.json").write_text(json.dumps(r, indent=1) + "\n")
        print(f"evaluate: {r['status']} games_scored={r['games_scored']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
