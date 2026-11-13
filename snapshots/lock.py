"""Lock a pre-kickoff game snapshot WITH sim output (NFL-49 calibration evidence; Ghost6: snapshots without
sim output only test hand reads).

    python3 -m snapshots.lock --config core/possession_engine_v0/config/was_nyg_2026-11-12_data_only_nfl43.json \
        --pbp /path/play_by_play_2026.parquet --price-freeze <freeze_*.json> [--n 100000] [--workers 7]

Refuses (exit 2) when: now >= kickoff; the PBP contains the target game or any week >= target week for the
history used; history weeks are not strictly before the target week; the price freeze was pulled after now /
kickoff. Engine: core/possession_engine_v0 legacy possession path + NFL-43 semantics (``cfg['semantics']``).
Model weights unchanged. Output: snapshots/<game_id>/<locked_utc>/ with LOCK.json (sha256 of every file,
git commit, seed, n, runtime). Research only: projection_ready=false, no stakes, no picks.

NFL-43 review guard (Ghost6 d65ad98, F1): refuses (exit 2) BEFORE any sim while the NFL-43 bounds review is not
ACCEPTED for the current SEMANTICS_BOUNDS.md, or 100k is DEFERRED, or semantics are still listed unsupported
(pipeline.hooks.nfl43_semantics). The review state is written into LOCK.json.

NFL-42 entrypoint guard: also refuses (exit 2) BEFORE any sim unless pipeline.hooks.nfl42_entrypoint is OK (the
single validation entrypoint routes only to the decontam validator and still rejects the contaminated suite_fix files).

This is NOT the 100k entry point (that is Ghost6's `python -m pipeline.sim100k`); it is the snapshot locker.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "core" / "possession_engine_v0"
OUT = ROOT / "snapshots"
FORBIDDEN_KEYS = ("stake", "bankroll", "wager", "units_risked", "bet_amount", "payout")


def sha256(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _utc(s: str) -> datetime:
    return datetime.fromisoformat(str(s).replace("Z", "+00:00")).astimezone(timezone.utc)


def review_guard(root: Path = ROOT) -> dict:
    """NFL-43 AC4: no 100k lock while the bounds review is pending. Read-only."""
    sys.path.insert(0, str(root))
    from pipeline import hooks
    flags = hooks.known_flags(root / "known_flags" / "KNOWN_LIMITATIONS.json")
    return hooks.nfl43_semantics(flags, root=root)


def _chunk(args):
    cfg, pbp, n, seed = args
    sys.path.insert(0, str(ENGINE))
    from simulate import simulate_games
    out = simulate_games(cfg, pbp_path=pbp, n=n, seed=seed)
    arrays = {k: np.asarray(v) for k, v in out["arrays"].items()}
    joint = out.get("player_joint") or {}
    return {"arrays": arrays, "joint": joint, "n": out["n_completed"], "status": out["status"],
            "player_box": out.get("player_box"),
            "semantics": out.get("semantics"), "evidence_summary": out.get("evidence_summary"),
            "limitations": out.get("limitations"), "history_evidence": out.get("history_evidence")}


def _require_nfl42() -> None:
    """NFL-42 guard on the shared orchestration path (main(), pipeline.sim100k default_engine, direct callers)."""
    sys.path.insert(0, str(ROOT))
    from pipeline import hooks as _h
    ep = _h.nfl42_entrypoint(ROOT)
    if ep.get("status") != "OK":
        raise RuntimeError("NFL-42 single validation entrypoint not enforced; refusing to simulate: " + str(ep.get("reason")))


def run_sim(cfg: dict, pbp: str, n: int, seed: int, workers: int) -> dict:
    for _k in ("opportunity_model", "opportunity", "int_pool"):  # NFL-75 Phase 2 opportunity model is research only
        if _k in cfg:
            raise ValueError(f"UNSUPPORTED: lock / 100k path refuses {_k!r} (research only, simulate_games kwarg)")
    _require_nfl42()
    k = max(1, workers)
    sizes = [n // k + (1 if i < n % k else 0) for i in range(k)]
    jobs = [(cfg, pbp, s, seed + 1000003 * i) for i, s in enumerate(sizes) if s > 0]
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=k) as ex:
        parts = list(ex.map(_chunk, jobs))
    arrays = {key: np.concatenate([p["arrays"][key] for p in parts]) for key in parts[0]["arrays"]}
    # player mean yards: weighted by chunk n
    joint: dict = {}
    for p in parts:
        for kind, teams in p["joint"].items():
            for team, players in teams.items():
                for pl, v in players.items():
                    joint.setdefault(kind, {}).setdefault(team, {}).setdefault(pl, 0.0)
                    joint[kind][team][pl] += v * p["n"] / n
    # NFL-75: per-trial per-player box lines, chunk order preserved (same order as arrays)
    if str(ENGINE) not in sys.path:
        sys.path.insert(0, str(ENGINE))
    from player_box import merge as _merge_box
    player_box = _merge_box([p.get("player_box") for p in parts])
    return {"arrays": arrays, "joint": joint, "n": int(sum(p["n"] for p in parts)), "chunks": len(parts),
            "player_box": player_box,
            "chunk_seeds": [j[3] for j in jobs], "runtime_sec": round(time.time() - t0, 1),
            "statuses": sorted({p["status"] for p in parts}), "semantics": parts[0]["semantics"],
            "evidence_summary": parts[0]["evidence_summary"], "limitations": parts[0]["limitations"],
            "history_evidence": parts[0]["history_evidence"]}


def market_lines(freeze: dict | None, home_name: str, away_name: str) -> dict:
    """Book lines from a four-book freeze (Blitz's pregame.multibook format) or a packet 'books' block."""
    out = {"spreads": [], "totals": [], "h2h": []}
    if not freeze:
        return out
    for r in freeze.get("rows") or []:
        m = r.get("market")
        if m not in out or r.get("player"):
            continue
        rec = {"book": r["book"], "reference_only": bool(r.get("reference_only")), "line": r.get("line"),
               "side_a": r.get("side_a"), "novig_a": r.get("novig_a"), "price_a": r.get("price_a"), "price_b": r.get("price_b"),
               "book_last_update": r.get("book_last_update")}
        out[m].append(rec)
    return out


def summarize(arrays: dict, lines: dict, home: str, away: str, home_name: str, away_name: str) -> dict:
    h = arrays["fg_home"].astype(float); a = arrays["fg_away"].astype(float)
    margin, total = h - a, h + a
    q = lambda x: [float(np.percentile(x, p)) for p in (10, 25, 50, 75, 90)]
    s = {"n": int(len(h)), "home": home, "away": away,
         "points": {home: float(h.mean()), away: float(a.mean())},
         "margin_home": {"mean": float(margin.mean()), "sd": float(margin.std()), "p10_25_50_75_90": q(margin)},
         "total": {"mean": float(total.mean()), "sd": float(total.std()), "p10_25_50_75_90": q(total)},
         "p_home_win": float((h > a).mean()), "p_away_win": float((a > h).mean()), "p_tie": float((h == a).mean()),
         "p_ot": float(arrays["went_ot"].astype(float).mean()),
         "halves": {k: float(arrays[k].astype(float).mean()) for k in ("h1_home", "h1_away", "h2_home", "h2_away")},
         "quarters": {k: float(arrays[k].astype(float).mean()) for k in arrays if k[:2] in ("q1", "q2", "q3", "q4")},
         "nfl43": {k: float(arrays[k].astype(float).mean()) for k in ("pen_yds_home", "pen_yds_away", "n_pen", "ret_td_home",
                                                                        "ret_td_away", "def_td_home", "def_td_away") if k in arrays}}
    priced = []
    for r in lines.get("spreads", []):
        if r["line"] is None:
            continue
        ln = float(r["line"])  # applies to side_a
        side_home = r["side_a"] == home_name
        adj = (margin + ln) if side_home else (-margin + ln)
        priced.append({"market": "spread", "book": r["book"], "side": r["side_a"], "line": ln,
                       "p_model_cover": float((adj > 0).mean()), "p_model_push": float((adj == 0).mean()),
                       "p_book_novig": r["novig_a"], "reference_only": r["reference_only"]})
    for r in lines.get("totals", []):
        if r["line"] is None:
            continue
        ln = float(r["line"])
        over = r["side_a"].lower().startswith("over")
        priced.append({"market": "total", "book": r["book"], "side": r["side_a"], "line": ln,
                       "p_model": float(((total > ln) if over else (total < ln)).mean()), "p_model_push": float((total == ln).mean()),
                       "p_book_novig": r["novig_a"], "reference_only": r["reference_only"]})
    for r in lines.get("h2h", []):
        side_home = r["side_a"] == home_name
        p_win = s["p_home_win"] if side_home else s["p_away_win"]
        p_ex_tie = p_win / max(1e-9, 1 - s["p_tie"])
        priced.append({"market": "moneyline", "book": r["book"], "side": r["side_a"], "p_model_win": p_win,
                       "p_model_win_ex_tie": p_ex_tie, "p_book_novig": r["novig_a"], "reference_only": r["reference_only"]})
    s["vs_market"] = priced
    gaps = [abs(x["p_model_win_ex_tie"] - x["p_book_novig"]) for x in priced if x["market"] == "moneyline" and x["p_book_novig"] is not None]
    gap = max(gaps) if gaps else None
    s["market_divergence"] = {"max_abs_moneyline_gap": gap,
                              "flag": None if gap is None else ("QUARANTINE_LIKELY_MODEL_ERROR" if gap >= 0.40 else
                                                                 "LARGE_DIVERGENCE_TREAT_AS_MODEL_ERROR_UNTIL_SHOWN_OTHERWISE" if gap >= 0.15 else "WITHIN_0.15")}
    return s


def asof_checks(cfg: dict, pbp: str, now: datetime, kickoff: datetime, freeze: dict | None) -> list[str]:
    import pandas as pd
    why = []
    wk = int(cfg["game"]["week_asof_exclusive"])
    if now >= kickoff:
        why.append(f"now {now.isoformat()} is not before kickoff {kickoff.isoformat()} (no post-kickoff locks)")
    if max(cfg["history"]["weeks_inclusive"]) >= wk:
        why.append("history weeks not strictly before target week")
    d = pd.read_parquet(pbp, columns=["game_id", "week", "season"])
    gid = cfg["game"].get("game_id")
    if gid and (d["game_id"] == gid).any():
        why.append(f"PBP already contains target game {gid} (leakage)")
    if freeze:
        pulled = (freeze.get("meta") or {}).get("pulled_utc")
        if pulled and _utc(pulled) > min(now, kickoff):
            why.append(f"price freeze pulled {pulled} after lock time/kickoff")
    return why


def _git(*a) -> str:
    try:
        return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return "UNKNOWN"


def _code_dirty() -> bool:
    """True when any engine/config/snapshot-tool source differs from HEAD (docs excluded)."""
    out = _git("status", "--porcelain", "--", "core/possession_engine_v0", "snapshots/lock.py", "data/redistributable/teams")
    if out == "UNKNOWN":
        return True
    return any(l[3:].endswith((".py", ".json", ".csv")) for l in out.splitlines())


def packet_prices(packet: dict) -> dict:
    """Two-book (DraftKings, FanDuel) + Pinnacle-reference rows from a pregame packet, in freeze-row format.
    Used only when no four-book freeze exists for the game (flagged PACKET_TWO_BOOK_NOT_FOUR_BOOK)."""
    b = packet.get("books") or {}
    rows = []
    mk = {"moneyline": "h2h", "spread": "spreads", "total": "totals"}
    for name, m in (b.get("markets") or {}).items():
        if name not in mk:
            continue
        a_side, b_side = m["sides"][0], m["sides"][1]
        for book, q in (m.get("books") or {}).items():
            rows.append({"book": book, "market": mk[name], "line": q.get("line"), "side_a": a_side, "side_b": b_side,
                         "novig_a": (q.get("no_vig") or {}).get(a_side), "price_a": (q.get("prices") or {}).get(a_side),
                         "price_b": (q.get("prices") or {}).get(b_side), "book_last_update": q.get("last_update"),
                         "reference_only": book == "pinnacle", "player": None})
    books = sorted({r["book"] for r in rows})
    return {"meta": {"status": "PACKET_TWO_BOOK_NOT_FOUR_BOOK" if rows else "NOLINE", "pulled_utc": b.get("retrieved_utc"),
                     "books": books, "source": "pregame packet books block (Odds API via packet builder)"}, "rows": rows}


def write_report(dirp: Path, s: dict, lock: dict, cfg: dict) -> None:
    g = cfg["game"]
    L = [f"# Locked snapshot {g['away']} @ {g['home']} ({g.get('game_id')})", "",
         "RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.", "",
         f"- Locked (UTC): {lock['locked_utc']}  | kickoff (UTC): {lock['kickoff_utc']}",
         f"- Engine: core/possession_engine_v0 + NFL-43 semantics; config `{cfg['config_id']}`; code commit `{lock['code_commit']}`",
         f"- Trials: {s['n']:,} in {lock['sim']['chunks']} chunks, seed {lock['sim']['seed']}, runtime {lock['sim']['runtime_sec']} s",
         f"- History: weeks {cfg['history']['weeks_inclusive']} (strictly before week {g['week_asof_exclusive']}); PBP sha256 `{lock['inputs']['pbp_sha256'][:16]}...`", "",
         "| | mean |", "|---|---|",
         f"| {s['home']} points | {s['points'][s['home']]:.2f} |", f"| {s['away']} points | {s['points'][s['away']]:.2f} |",
         f"| home margin | {s['margin_home']['mean']:.2f} (sd {s['margin_home']['sd']:.2f}) |",
         f"| total | {s['total']['mean']:.2f} (sd {s['total']['sd']:.2f}) |",
         f"| P(home win) / P(away win) / P(tie) | {s['p_home_win']:.3f} / {s['p_away_win']:.3f} / {s['p_tie']:.4f} |",
         f"| P(OT) | {s['p_ot']:.3f} |",
         f"| penalties per game / yards home, away | {s['nfl43'].get('n_pen', 0):.2f} / {s['nfl43'].get('pen_yds_home', 0):.1f}, {s['nfl43'].get('pen_yds_away', 0):.1f} |", "",
         "## Against the frozen book lines (research comparison, not an edge claim)", "",
         "| market | book | side | line | model P | book no-vig P |", "|---|---|---|---|---|---|"]
    for x in s["vs_market"]:
        p = x.get("p_model_cover", x.get("p_model", x.get("p_model_win_ex_tie")))
        L.append(f"| {x['market']} | {x['book']}{' (ref)' if x['reference_only'] else ''} | {x['side']} | {x.get('line', '')} | {p:.3f} | {x['p_book_novig']} |")
    L += ["", f"Market divergence: {s['market_divergence']}", "",
          "## Known limits", *[f"- {l}" for l in lock["limitations"]], ""]
    (dirp / "report.md").write_text("\n".join(L))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--pbp", required=True)
    ap.add_argument("--pbp-url", default="https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet")
    ap.add_argument("--price-freeze", help="four-book freeze json (copied into the snapshot, hashed)")
    ap.add_argument("--price-freeze-origin", default="", help="where the freeze came from (branch@commit:path)")
    ap.add_argument("--packet", help="pregame packet.json (copied; source timestamps)")
    ap.add_argument("--n", type=int, default=100_000)
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    a = ap.parse_args(argv)
    guard = review_guard()
    if guard["status"] != "OK":
        print("lock: REFUSED  " + guard["reason"] + " Nothing was simulated.")
        return 2
    sys.path.insert(0, str(ROOT))
    from pipeline import hooks as _hooks
    ep = _hooks.nfl42_entrypoint(ROOT)  # NFL-42: same single-entrypoint enforcement as the 100k gate (G0)
    if ep["status"] != "OK":
        print("lock: REFUSED  " + ep["reason"] + " Nothing was simulated.")
        return 2
    sys.path.insert(0, str(ENGINE))
    from config_load import load_config
    from simulate import stable_seed
    cfg_path = Path(a.config)
    cfg = load_config(cfg_path)
    sys.path.insert(0, str(ROOT))
    from pipeline import hooks
    ex = hooks.nfl43_still_unsupported(hooks.known_flags(), cfg=cfg)
    if ex["status"] != "OK":
        print("lock: REFUSED  " + ex["reason"] + " Nothing was simulated.")
        return 2
    g = cfg["game"]
    kickoff = _utc(g["kickoff_et"])
    now = datetime.now(timezone.utc)
    freeze = json.loads(Path(a.price_freeze).read_text()) if a.price_freeze else None
    packet = json.loads(Path(a.packet).read_text()) if a.packet else None
    if freeze is None and packet is not None:
        freeze = packet_prices(packet)
        g.setdefault("home_name", g["home"]); g.setdefault("away_name", g["away"])
    why = asof_checks(cfg, a.pbp, now, kickoff, freeze)
    if why:
        print("lock: REFUSED\n  - " + "\n  - ".join(why))
        return 2
    seed = stable_seed(int(cfg["seed_base"]), int(g["week_asof_exclusive"]), cfg["config_id"])
    sim = run_sim(cfg, a.pbp, a.n, seed, a.workers)
    if sim["n"] != a.n:
        print(f"lock: REFUSED  completed {sim['n']} != requested {a.n}")
        return 2
    locked = datetime.now(timezone.utc)
    if locked >= kickoff:
        print("lock: REFUSED  sim finished after kickoff")
        return 2
    d = OUT / g["game_id"] / locked.strftime("%Y%m%dT%H%M%SZ")
    (d / "inputs").mkdir(parents=True, exist_ok=True)
    shutil.copy2(cfg_path, d / "inputs" / cfg_path.name)
    # Only team-level markets are republished here. Player rows (props) and the packet itself are NOT copied:
    # this repo publishes no player numbers from this track (Rico/NFL-49). Source files are pinned by sha256.
    if freeze is not None:
        team_only = {"meta": {k: v for k, v in (freeze.get("meta") or {}).items() if k != "consensus"},
                     "rows": [r for r in freeze.get("rows") or [] if not r.get("player")
                              and r.get("market") in ("h2h", "spreads", "totals")],
                     "note": "team markets only; player rows stripped; full source pinned in LOCK.inputs"}
        name = ("team_prices_" + Path(a.price_freeze).name) if a.price_freeze else "team_prices_from_packet.json"
        (d / "inputs" / name).write_text(json.dumps(team_only, indent=1) + "\n")
    np.savez_compressed(d / "sim_arrays.npz", **{k: v.astype(np.int16 if v.dtype != bool else bool) for k, v in sim["arrays"].items()})
    home_name = away_name = None
    for r in (freeze or {}).get("rows") or []:
        if r.get("market") == "h2h":
            names = {r["side_a"], r["side_b"]}
            home_name = next((x for x in names if x == g.get("home_name")), None) or \
                next((x for x in names if g.get("home_name") and g["home_name"] in x), None)
            away_name = next((x for x in names if x == g.get("away_name")), None) or \
                next((x for x in names if g.get("away_name") and g["away_name"] in x), None)
            break
    lines = market_lines(freeze, home_name, away_name)
    s = summarize(sim["arrays"], lines, g["home"], g["away"], home_name, away_name)
    s["player_outputs"] = ("WITHHELD: the possession sim's player credits are team-bootstrap historical rows, not a "
                           "player projection model; no player numbers are published from this snapshot.")
    (d / "summary.json").write_text(json.dumps(s, indent=1) + "\n")
    meta = {"semantics": sim["semantics"], "evidence_summary": sim["evidence_summary"], "history_evidence": sim["history_evidence"]}
    (d / "sim_meta.json").write_text(json.dumps(meta, indent=1, default=str) + "\n")
    lock = {"schema": "snapshot-lock/1", "game_id": g["game_id"], "locked_utc": locked.isoformat(timespec="seconds"),
            "kickoff_utc": kickoff.isoformat(), "projection_ready": False, "research_only": True,
            "code_commit": _git("rev-parse", "HEAD"), "code_dirty": _code_dirty(),
            "engine_tree_sha256": hashlib.sha256(b"".join(sha256(p).encode() for p in sorted(ENGINE.glob("*.py")))).hexdigest(),
            "config_id": cfg["config_id"], "model_weights_changed": False,
            "nfl43_review": guard.get("review"),
            "still_unsupported": ex.get("exclusions") or [],
            "sim": {"n": sim["n"], "seed": seed, "chunks": sim["chunks"], "chunk_seeds": sim["chunk_seeds"],
                    "runtime_sec": sim["runtime_sec"], "statuses": sim["statuses"]},
            "inputs": {"pbp_url": a.pbp_url, "pbp_sha256": sha256(a.pbp), "pbp_local_name": Path(a.pbp).name,
                       "price_freeze_origin": a.price_freeze_origin,
                       "price_freeze_sha256": sha256(a.price_freeze) if a.price_freeze else None,
                       "packet_path": a.packet, "packet_sha256": sha256(a.packet) if a.packet else None,
                       "packet_generated_utc": (packet or {}).get("generated_utc"),
                       "price_freeze_pulled_utc": ((freeze or {}).get("meta") or {}).get("pulled_utc"),
                       "price_status": ((freeze or {}).get("meta") or {}).get("status", "NOLINE"),
                       "price_freeze_books": ((freeze or {}).get("meta") or {}).get("books")},
            "asof_checks": "PASS", "limitations": sim["limitations"] + [
                "data_only config: no injury/inactive adjustment; Phase 15 inactives not applied to the sim",
                "team scores only; player yards are bootstrap credits, not a player projection model"],
            "scoring": {"command": f"python3 -m snapshots.score --snapshot snapshots/{g['game_id']}/{locked:%Y%m%dT%H%M%SZ}",
                        "status": "NOT_SCORED_UNTIL_FINAL"}}
    write_report(d, s, lock, cfg)
    lock["files"] = {str(p.relative_to(d)): sha256(p) for p in sorted(d.rglob("*")) if p.is_file()}
    text = json.dumps(lock, indent=1)
    if any(k in text.lower() for k in FORBIDDEN_KEYS):
        raise SystemExit("lock: forbidden money/stake key present")
    (d / "LOCK.json").write_text(text + "\n")
    print(f"lock: OK {d.relative_to(ROOT)}  n={sim['n']} runtime={sim['runtime_sec']}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
