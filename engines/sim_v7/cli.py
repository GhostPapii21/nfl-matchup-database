"""sim_v7 CLI + callable interface (integration contract for PR #163 / NFL-85 / NFL-92).

  python3 -m engines.sim_v7.cli run --game 2026_12_NO_CIN --n 100000 --out runs/sim_v7_2026-11-28/out/
  python3 -m engines.sim_v7.cli run --slate 2026-11-29 --n 100000 --out ...
  python3 -m engines.sim_v7.cli smoke

Python:
  from engines.sim_v7.cli import simulate_game
  doc = simulate_game("2026_12_NO_CIN", n=100_000)   # -> dict with "records": [...]

Inputs (read-only): dashboard/data/<game_id>.json (schedule, consensus spread/total, book prop lines, injury
lists) and nflverse pbp 2024-26. Outputs never touch a database; nothing is promoted to projection_ready.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
import time

import numpy as np

from . import data as D
from . import engine as E
from . import defensive as DEF

CALIB_FILE = os.path.join(os.path.dirname(__file__), "calibration_v7.json")
SOURCE_CUTOFF = "2026-11-24"   # first date NOT included (pbp through 2026-11-23, week 11)
BOOK_MARKETS = {"receptions": "receptions", "receiving_yards": "rec_yds", "rushing_yards": "rush_yds",
                "passing_yards": "pass_yds", "passing_tds": "pass_td", "passing_completions": "pass_cmp",
                "passing_attempts": "pass_att", "rushing_attempts": "rush_att"}
OUT_STATUSES = {"out", "injured reserve", "doubtful", "physically unable to perform", "suspended"}


def norm(name: str) -> str:
    s = re.sub(r"[^a-z ]", "", str(name).lower().replace("-", " "))
    return " ".join(w for w in s.split() if w not in {"jr", "sr", "ii", "iii", "iv", "v"})


def load_calib():
    return json.load(open(CALIB_FILE)) if os.path.exists(CALIB_FILE) else None


def game_config(game_id: str) -> tuple[dict, dict]:
    path = os.path.join(D.REPO, "dashboard", "data", f"{game_id}.json")
    b = json.load(open(path))
    g = b["game"]
    home, away = D.NV.get(g["home"], g["home"]), D.NV.get(g["away"], g["away"])
    hs, tot = b["market"].get("home_spread"), b["market"].get("total")
    implied = None
    if hs is not None and tot is not None:   # dashboard home_spread: negative = home favoured
        implied = {home: (tot - hs) / 2, away: (tot + hs) / 2}
    fav = home if (hs is None or hs <= 0) else away
    excl = set()
    pl = D.load_players()
    for side in b.get("sides", {}).values():
        for inj in side.get("offense_injuries", []) or []:
            st = {str(inj.get("espn") or "").lower(), str(inj.get("game_status") or "").lower()}
            if st & OUT_STATUSES:
                m = pl[(pl.display_name.map(norm) == norm(inj.get("player"))) & pl.latest_team.map(lambda t: D.NV.get(t, t)).isin([home, away])]
                excl.update(m.gsis_id.tolist())
    cfg = dict(game_id=game_id, home=home, away=away, cutoff=SOURCE_CUTOFF, fav=fav, implied=implied,
               exclude=sorted(excl), market_source=b["market"].get("source"), board_file=os.path.relpath(path, D.REPO),
               board_sha256=D.sha256_file(path))
    cfg["defensive_profiles"] = {D.NV.get(t, t): p for t, p in DEF.profiles(b, cutoff=SOURCE_CUTOFF).items()}
    return cfg, b


def book_lines(board: dict, ctxs: dict) -> dict:
    """{(gsis, our_market): [{book, line}]} plus game-level {'spread'|'total': [...]}."""
    name2id = {}
    for ctx in ctxs.values():
        for gs, nm in zip(ctx.players.gsis, ctx.players.name):
            name2id[norm(nm)] = gs
    out = {}
    for key, mk in board.get("books", {}).get("markets", {}).items():
        kind, _, who = key.partition("|")
        books = mk.get("books", {})
        lines = [dict(book=bk, line=v["line"]) for bk, v in books.items() if v.get("line") is not None]
        if kind in ("spread", "total"):
            out[kind] = dict(sides=mk.get("sides"), lines=lines)
        elif kind in BOOK_MARKETS and norm(who) in name2id:
            out.setdefault((name2id[norm(who)], BOOK_MARKETS[kind]), []).extend(lines)
    return out


def _player_series(X: dict, ctx) -> dict:
    res = {}
    for gs, role in zip(ctx.players.gsis, ctx.players.role):
        stats = E.QB_STATS if role == "QB" else E.SK_STATS
        for st in stats:
            res[(gs, E.MARKET[st])] = X[f"{gs}|{st}"]
        if role != "QB":
            res[(gs, "anytime_td")] = (X[f"{gs}|rectd"] + X[f"{gs}|rushtd"] > 0).astype(np.float32)
            res[(gs, "rush_rec_yds")] = X[f"{gs}|recyds"] + X[f"{gs}|rushyds"]
    return res


def _game_records(X, cfg, fav, dog, lines):
    h, a = cfg["home"], cfg["away"]
    recs = []
    hq = np.stack([X[f"{h}|q{i}"] for i in (1, 2, 3, 4)], 1)
    aq = np.stack([X[f"{a}|q{i}"] for i in (1, 2, 3, 4)], 1)
    series = {f"{h}_points": X[f"{h}|pts"], f"{a}_points": X[f"{a}|pts"], "total_points": X[f"{h}|pts"] + X[f"{a}|pts"],
              "home_margin": X[f"{h}|pts"] - X[f"{a}|pts"], f"{h}_1h_points": hq[:, :2].sum(1), f"{a}_1h_points": aq[:, :2].sum(1)}
    for i in range(4):
        series[f"{h}_q{i+1}_points"], series[f"{a}_q{i+1}_points"] = hq[:, i], aq[:, i]
    for k, v in series.items():
        lp = []
        if k == "total_points" and "total" in lines:
            lp = E.line_probs(v, lines["total"]["lines"])
        if k == "home_margin" and "spread" in lines:   # book spread is quoted for sides[0]
            s0 = lines["spread"]["sides"][0]
            lp = [dict(book=L["book"], line=L["line"], side=s0,
                       p_cover=round(float(((v if s0 == h else -v) + L["line"] > 0).mean()), 5),
                       p_push=round(float(((v if s0 == h else -v) + L["line"] == 0).mean()), 5)) for L in lines["spread"]["lines"]]
        recs.append(dict(player_id=None, market=k, distribution=E.summarize(v), line_probabilities=lp))
    def wl(x, y):
        return dict(home=round(float((x > y).mean()), 5), away=round(float((x < y).mean()), 5), tie=round(float((x == y).mean()), 5))
    for i in range(4):
        recs.append(dict(player_id=None, market=f"q{i+1}_winner", distribution=wl(hq[:, i], aq[:, i]), line_probabilities=[]))
    recs.append(dict(player_id=None, market="1h_winner", distribution=wl(hq[:, :2].sum(1), aq[:, :2].sum(1)), line_probabilities=[]))
    recs.append(dict(player_id=None, market="game_winner_regulation", distribution=wl(X[f"{h}|pts"], X[f"{a}|pts"]),
                     line_probabilities=[], note="regulation only; no overtime simulated"))
    return recs


def _calib_status(method: str, market: str, calib: dict | None, is_residual: bool) -> str:
    """After defensive integration, never inherit prior VALIDATED labels."""
    if is_residual:
        base = "RESIDUAL_EXPERIMENTAL_UNVALIDATED"
    elif method != "bias":
        return "NOT_APPLICABLE"
    else:
        prior = (calib or {}).get("markets", {}).get(market, {}).get("status", "UNCALIBRATED_MARKET_PASSTHROUGH")
        base = "EXPERIMENTAL_UNVALIDATED_DEFENSE_CHANGED"
        if prior:
            base = f"{base}|prior={prior}"
    return base


def _unconditional_from_cells(method_result: dict, key_series_fn) -> list:
    """Mixture of scenario-conditional draws weighted by actual scenario frequencies."""
    cells = method_result.get("cells") or {}
    freq = method_result.get("scenario_frequency") or {}
    if not cells or not freq:
        return []
    bags = {}
    for s, cell in cells.items():
        X = cell.get("X") or {}
        if not X:
            continue
        series = key_series_fn(X)
        w = float(freq.get(s, 0.0))
        if w <= 0:
            continue
        for k, v in series.items():
            bags.setdefault(k, []).append((w, np.asarray(v, dtype=np.float64)))
    out = []
    for k, parts in bags.items():
        chunks = []
        total_w = sum(w for w, _ in parts) or 1.0
        for w, arr in parts:
            take = max(int(round(len(arr) * (w / total_w))), 1)
            chunks.append(arr[:take])
        mix = np.concatenate(chunks) if chunks else np.zeros(1)
        player_id, market = k if isinstance(k, tuple) else (None, k)
        out.append(dict(player_id=player_id, market=market, distribution=E.summarize(mix),
                        draws=mix, scenario="unconditional", scenario_frequency=freq,
                        note="mixture of exhaustive scenarios weighted by acceptance frequencies"))
    return out


def simulate_game(game_id: str, n: int = 100_000, seed: int = 20261129, methods=E.METHODS, scenarios=E.SCENARIOS,
                  batch: int = 100_000, log=print, include_residual: bool = True) -> dict:
    t0 = time.time()
    cfg, board = game_config(game_id)
    calib = load_calib()
    run = E.run_cells(cfg, methods, scenarios, n=n, seed=seed, batch=batch, calib=calib, log=log,
                      include_residual=include_residual)
    ctxs = run["ctxs"]
    lines = book_lines(board, ctxs)
    input_hash = D.context_hash(cfg, {t: c.game_ids for t, c in ctxs.items()}, E.ENGINE_VERSION,
                                (calib or {}).get("as_of"), "defense_v1")
    names = {gs: (nm, c.team, pos) for c in ctxs.values() for gs, nm, pos in zip(c.players.gsis, c.players.name, c.players.pos)}
    records = []
    residual_records = []
    unconditional_records = []
    for method in methods:
        R = run["results"][method]
        if "cells" not in R:
            for s in list(scenarios) + ([E.RESIDUAL_SCENARIO] if include_residual else []):
                records.append(dict(game_id=game_id, player_id=None, market="*", method=method, scenario=s, trial_count=0,
                                    seed=None, distribution=None, line_probabilities=[], calibration_status="MISSING",
                                    input_hash=input_hash, source_cutoff=SOURCE_CUTOFF, execution_status=R["execution_status"]))
            continue
        for s, cell in R["cells"].items():
            X = cell["X"]
            is_res = bool(cell.get("is_residual"))
            common = dict(game_id=game_id, method=method, scenario=s, trial_count=cell["trial_count"], seed=R["seed"],
                          input_hash=input_hash, source_cutoff=SOURCE_CUTOFF, execution_status=cell["execution_status"],
                          scenario_acceptance_rate=cell["acceptance_rate"], raw_trials_generated=R["raw_trials"],
                          scenario_frequency=(R.get("scenario_frequency") or {}).get(s),
                          is_residual=is_res)
            bucket = residual_records if is_res else records
            for r in _game_records(X, cfg, run["fav"], run["dog"], lines):
                cs = _calib_status(method, r["market"], calib, is_res)
                bucket.append(dict(common, **r, calibration_status=cs))
            for ctx in ctxs.values():
                for (gs, mk), v in _player_series(X, ctx).items():
                    cs = _calib_status(method, mk, calib, is_res)
                    nm, team, pos = names[gs]
                    bucket.append(dict(common, player_id=gs, player_name=nm, team=team, position=pos, market=mk,
                                       distribution=E.summarize(v), line_probabilities=E.line_probs(v, lines.get((gs, mk), [])),
                                       calibration_status=cs))
        def series_fn(X):
            out = {}
            h, a = cfg["home"], cfg["away"]
            out[f"{h}_points"] = X[f"{h}|pts"]
            out[f"{a}_points"] = X[f"{a}|pts"]
            out["total_points"] = X[f"{h}|pts"] + X[f"{a}|pts"]
            out["home_margin"] = X[f"{h}|pts"] - X[f"{a}|pts"]
            for ctx in ctxs.values():
                for (gs, mk), v in _player_series(X, ctx).items():
                    out[(gs, mk)] = v
            return out
        for u in _unconditional_from_cells(R, series_fn):
            pid = u.get("player_id")
            mk = u["market"]
            draws = u.pop("draws", None)
            lp = []
            if draws is not None and pid is not None:
                lp = E.line_probs(draws, lines.get((pid, mk), []))
            elif draws is not None and mk == "total_points" and "total" in lines:
                lp = E.line_probs(draws, lines["total"]["lines"])
            row = dict(game_id=game_id, method=method, scenario="unconditional",
                       trial_count=sum(c["trial_count"] for c in R["cells"].values()),
                       seed=R["seed"], input_hash=input_hash, source_cutoff=SOURCE_CUTOFF,
                       execution_status="OK", distribution=u["distribution"],
                       line_probabilities=lp,
                       calibration_status="EXPERIMENTAL_UNVALIDATED_DEFENSE_CHANGED",
                       scenario_frequency=R.get("scenario_frequency"),
                       note=u.get("note"))
            if pid:
                nm, team, pos = names[pid]
                row.update(player_id=pid, player_name=nm, team=team, position=pos, market=mk)
            else:
                row.update(player_id=None, market=mk)
            unconditional_records.append(row)
    meta = dict(engine=E.ENGINE_VERSION, not_original_sim_v6=True, game=cfg, fav=run["fav"],
                methods={m: run["results"][m].get("seconds") for m in methods},
                players={t: c.players.to_dict("records") for t, c in ctxs.items()},
                history_games={t: c.game_ids for t, c in ctxs.items()},
                calibration_artifact=dict(file=os.path.relpath(CALIB_FILE, D.REPO), as_of=(calib or {}).get("as_of"),
                                          K=(calib or {}).get("K_selected"),
                                          status_after_defense="EXPERIMENTAL_UNVALIDATED_DEFENSE_CHANGED",
                                          note="prior holdout labels not inherited after defensive integration") if calib else None,
                defensive_integration={t: {
                    "status": p.get("status"),
                    "integration": p.get("integration"),
                    "calibration_status": p.get("calibration_status"),
                    "scramble_status": (p.get("scramble") or {}).get("status"),
                    "coverage_alloc_status": (p.get("coverage_allocation") or {}).get("status"),
                    "sharp_status": (p.get("sharp_defense") or {}).get("status"),
                    "charting": ((p.get("coverage_allocation") or {}).get("charting")),
                } for t, p in (cfg.get("defensive_profiles") or {}).items()},
                provenance=D.provenance(), runtime_seconds=round(time.time() - t0, 2),
                status="RESEARCH_ONLY_NOT_PROJECTION_READY",
                scenario_definitions={"favorite_controls": "fav leads at half and wins by >=10",
                                      "competitive": "|half margin|<=6 and |final margin|<=7",
                                      "underdog_chases": "dog trails by >=7 at half and final fav margin <10",
                                      "residual": "exhaustive complement of the three primary scripts",
                                      "unconditional": "mixture weighted by actual scenario frequencies"},
                scenario_frequency_by_method={m: run["results"][m].get("scenario_frequency")
                                              for m in methods if "cells" in run["results"][m]})
    return dict(meta=meta, records=records, residual_records=residual_records,
                unconditional_records=unconditional_records)


def write(doc: dict, out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    gid = doc["meta"]["game"]["game_id"]
    p = os.path.join(out_dir, f"{gid}.sim_v7.json")
    with open(p, "w") as f:
        json.dump(doc, f, default=float)
    # Residual + unconditional kept beside primary artifact for Sunday receipts
    if doc.get("residual_records") is not None:
        rp = os.path.join(out_dir, f"{gid}.sim_v7.residual.json")
        with open(rp, "w") as f:
            json.dump({"meta": doc["meta"], "residual_records": doc["residual_records"],
                       "unconditional_records": doc.get("unconditional_records", [])}, f, default=float)
    return p


def acceptance_receipt(doc: dict, n_required: int = 100_000) -> dict:
    """Sunday-stack receipt: 3 methods x 3 primary scenarios x n_required, residual separate."""
    primary = {}
    residual = {}
    for r in doc.get("records") or []:
        if r.get("market") != "total_points":
            continue
        primary[(r["method"], r["scenario"])] = r
    for r in doc.get("residual_records") or []:
        if r.get("market") != "total_points":
            continue
        residual[(r["method"], r["scenario"])] = r
    cells = []
    ok = True
    for m in E.METHODS:
        for s in E.PRIMARY_SCENARIOS:
            row = primary.get((m, s))
            trials = (row or {}).get("trial_count", 0) or 0
            status = (row or {}).get("execution_status", "MISSING")
            if trials < n_required or status != "OK":
                ok = False
            cells.append(dict(method=m, scenario=s, trial_count=trials, status=status,
                              acceptance_rate=(row or {}).get("scenario_acceptance_rate")))
    res_cells = []
    for m in E.METHODS:
        row = residual.get((m, E.RESIDUAL_SCENARIO))
        res_cells.append(dict(method=m, scenario=E.RESIDUAL_SCENARIO,
                              trial_count=(row or {}).get("trial_count", 0),
                              status=(row or {}).get("execution_status", "MISSING"),
                              acceptance_rate=(row or {}).get("scenario_acceptance_rate")))
    return {
        "schema": "sim-v7-acceptance-receipt/1",
        "engine_id": "sim_v7",
        "engine_version": doc.get("meta", {}).get("engine"),
        "entrypoint": "engines.sim_v7.cli:simulate_game",
        "not_original_sim_v6": True,
        "projection_ready": False,
        "fallback_used": False,
        "status": "EXECUTED" if ok else "PARTIAL",
        "trials_required_per_primary_cell": n_required,
        "primary_cells_required": 9,
        "primary_cells": cells,
        "residual_cells": res_cells,
        "scenario_frequency_by_method": doc.get("meta", {}).get("scenario_frequency_by_method"),
        "defensive_integration": doc.get("meta", {}).get("defensive_integration"),
        "calibration": doc.get("meta", {}).get("calibration_artifact"),
        "input_hash": (doc.get("records") or [{}])[0].get("input_hash"),
        "source_cutoff": SOURCE_CUTOFF,
        "game_id": doc.get("meta", {}).get("game", {}).get("game_id"),
        "runtime_seconds": doc.get("meta", {}).get("runtime_seconds"),
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    r = sp.add_parser("run")
    r.add_argument("--game", action="append")
    r.add_argument("--slate", help="YYYY-MM-DD: every dashboard board with that date")
    r.add_argument("--n", type=int, default=100_000)
    r.add_argument("--seed", type=int, default=20261129)
    r.add_argument("--out", required=True)
    s = sp.add_parser("smoke")
    s.add_argument("--game", default="2026_12_NO_CIN")
    a = ap.parse_args(argv)
    if a.cmd == "smoke":
        d1 = simulate_game(a.game, n=2000, seed=1, batch=10_000, log=lambda *_: None)
        d2 = simulate_game(a.game, n=2000, seed=1, batch=10_000, log=lambda *_: None)
        same = json.dumps(d1["records"], default=float) == json.dumps(d2["records"], default=float)
        print(json.dumps(dict(deterministic=same, records=len(d1["records"])), indent=1))
        return 0 if same else 1
    games = list(a.game or [])
    if a.slate:
        for f in sorted(glob.glob(os.path.join(D.REPO, "dashboard", "data", "2026_*.json"))):
            try:
                if json.load(open(f))["game"]["date"] == a.slate:
                    games.append(os.path.basename(f)[:-5])
            except Exception:
                pass
    games = list(dict.fromkeys(games))
    if not games:
        print('No games selected', file=sys.stderr)
        return 2
    failed = False
    for gid in games:
        t0 = time.time()
        try:
            doc = simulate_game(gid, n=a.n, seed=a.seed, log=lambda m: print(m, flush=True))
            p = write(doc, a.out)
            print(f"{gid}: {len(doc['records'])} records -> {p} ({time.time()-t0:.1f}s)", flush=True)
        except Exception as ex:
            failed = True
            print(f"{gid}: FAILED {ex!r}", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
