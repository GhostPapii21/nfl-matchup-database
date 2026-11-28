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


def simulate_game(game_id: str, n: int = 100_000, seed: int = 20261129, methods=E.METHODS, scenarios=E.SCENARIOS,
                  batch: int = 100_000, log=print) -> dict:
    t0 = time.time()
    cfg, board = game_config(game_id)
    calib = load_calib()
    run = E.run_cells(cfg, methods, scenarios, n=n, seed=seed, batch=batch, calib=calib, log=log)
    ctxs = run["ctxs"]
    lines = book_lines(board, ctxs)
    input_hash = D.context_hash(cfg, {t: c.game_ids for t, c in ctxs.items()}, E.ENGINE_VERSION,
                                (calib or {}).get("as_of"))
    names = {gs: (nm, c.team, pos) for c in ctxs.values() for gs, nm, pos in zip(c.players.gsis, c.players.name, c.players.pos)}
    records = []
    for method in methods:
        R = run["results"][method]
        if "cells" not in R:
            for s in scenarios:
                records.append(dict(game_id=game_id, player_id=None, market="*", method=method, scenario=s, trial_count=0,
                                    seed=None, distribution=None, line_probabilities=[], calibration_status="MISSING",
                                    input_hash=input_hash, source_cutoff=SOURCE_CUTOFF, execution_status=R["execution_status"]))
            continue
        for s, cell in R["cells"].items():
            X = cell["X"]
            common = dict(game_id=game_id, method=method, scenario=s, trial_count=cell["trial_count"], seed=R["seed"],
                          input_hash=input_hash, source_cutoff=SOURCE_CUTOFF, execution_status=cell["execution_status"],
                          scenario_acceptance_rate=cell["acceptance_rate"], raw_trials_generated=R["raw_trials"])
            for r in _game_records(X, cfg, run["fav"], run["dog"], lines):
                cs = "NOT_APPLICABLE" if method != "bias" else "INHERITED_FROM_MC_NOT_CALIBRATED"
                records.append(dict(common, **r, calibration_status=cs))
            for ctx in ctxs.values():
                for (gs, mk), v in _player_series(X, ctx).items():
                    if method == "bias":
                        cs = calib["markets"].get(mk, {}).get("status", "UNCALIBRATED_MARKET_PASSTHROUGH")
                    else:
                        cs = "NOT_APPLICABLE"
                    nm, team, pos = names[gs]
                    records.append(dict(common, player_id=gs, player_name=nm, team=team, position=pos, market=mk,
                                        distribution=E.summarize(v), line_probabilities=E.line_probs(v, lines.get((gs, mk), [])),
                                        calibration_status=cs))
    meta = dict(engine=E.ENGINE_VERSION, not_original_sim_v6=True, game=cfg, fav=run["fav"],
                methods={m: run["results"][m].get("seconds") for m in methods},
                players={t: c.players.to_dict("records") for t, c in ctxs.items()},
                history_games={t: c.game_ids for t, c in ctxs.items()},
                calibration_artifact=dict(file=os.path.relpath(CALIB_FILE, D.REPO), as_of=(calib or {}).get("as_of"),
                                          K=(calib or {}).get("K_selected")) if calib else None,
                provenance=D.provenance(), runtime_seconds=round(time.time() - t0, 2),
                status="RESEARCH_ONLY_NOT_PROJECTION_READY",
                scenario_definitions={"favorite_controls": "fav leads at half and wins by >=10",
                                      "competitive": "|half margin|<=6 and |final margin|<=7",
                                      "underdog_chases": "dog trails by >=7 at half and final fav margin <10"})
    return dict(meta=meta, records=records)


def write(doc: dict, out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    p = os.path.join(out_dir, f"{doc['meta']['game']['game_id']}.sim_v7.json")
    with open(p, "w") as f:
        json.dump(doc, f, default=float)
    return p


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
    for gid in games:
        t0 = time.time()
        try:
            doc = simulate_game(gid, n=a.n, seed=a.seed, log=lambda m: print(m, flush=True))
            p = write(doc, a.out)
            print(f"{gid}: {len(doc['records'])} records -> {p} ({time.time()-t0:.1f}s)", flush=True)
        except Exception as ex:
            print(f"{gid}: FAILED {ex!r}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
