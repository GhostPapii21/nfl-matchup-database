"""NFL-75: per-player rushing-yards distribution + P(under L) artifact from the per-player box recorder.

OPT-IN, OBSERVATIONAL. Reads the per-trial per-player box lines the possession engine already records
(core/possession_engine_v0/player_box.py, merged by snapshots/lock.run_sim, written by
``pipeline.sim100k --write`` as ``pipeline/ledgers/<game>.sim100k.player_box.npz``). It never runs, seeds or changes the
engine, its weights or its outputs; ``pipeline.sim100k`` only calls it when ``--rush-dist`` is given.

Who is included: every player line (not UNASSIGNED) with a carry in at least one trial -- QBs, RBs and anyone else
with rush attempts. A trial where the player has no carries counts as 0 rushing yards.

rush_yds definition (default): box ``rush_yds + kneel_yds``. Official NFL stats (what books settle on) count
kneel-downs as rushes; the box keeps them apart. ``include_kneels=False`` gives box ``rush_yds`` alone.
Engine yards are whole yards; non-integer values are refused.

Outputs (``write``), all in one directory (default ``pipeline/ledgers/``):
  <game>.rush_dist.summary.csv  one row per player: SUMMARY_COLUMNS (mean, sd, quantiles q05..q95, p_any_carry)
  <game>.rush_dist.cdf.csv      long table CDF_COLUMNS: for every half-yard line L on the grid,
                                p_under = P(rush_yds < L), p_over = 1 - p_under (half lines cannot push).
                                The grid covers GRID_MIN..GRID_MAX and the whole simulated support, so
                                p_under is exactly 0 below the first row and 1 above the last.
  <game>.rush_dist.json         meta: schema, game, trials, seed, source, definitions, research_only, projection_ready
``p_under(cdf, team=, player=, line=)`` answers ANY line exactly (integer lines return p_push too).

Phase 4 hand-off: ``attach_p_model(legs, cdf)`` fills ``p_model`` (graded-side probability) on rows of the
calibration/selective_edge_live.py legs schema where market == "rushyds" and p_model is blank, matched by gsis (else a
unique first-initial.last name within the game). p_model = P(graded side | no push), which equals P(side) on half lines.
Columns are only appended (p_model_match, p_model_source); the frozen classifier is not touched.

    python -m pipeline.rush_dist build  --npz pipeline/ledgers/<game>.sim100k.player_box.npz --game <game> \
        [--pbp <as-of pbp parquet>] [--roster data/historical/nflverse/ros_2026.parquet] [--out pipeline/ledgers]
    python -m pipeline.rush_dist attach --legs legs.csv --dist pipeline/ledgers [--dist ...] --out legs_p.csv

No network, no API credits. Research only; projection_ready stays false."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

SCHEMA = "nfl75-rush-dist/1"
UNASSIGNED = "UNASSIGNED"
QUANTILES = (0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95)
GRID_MIN, GRID_MAX = -20.5, 250.5
ID_COLS = ("game_id", "team", "player", "gsis", "position", "full_name")
SUMMARY_COLUMNS = ID_COLS + ("n_trials", "p_any_carry", "carries_mean", "mean", "sd", "min", "max") + tuple(
    f"q{int(round(q * 100)):02d}" for q in QUANTILES)
CDF_COLUMNS = ("game_id", "team", "player", "gsis", "position", "line", "p_under", "p_over")
RUSH_YDS_DEF = ("player_box rush_yds + kneel_yds (official-stat convention: kneel-downs are rushes); "
                "0 in trials with no carry")
P_UNDER_DEF = "p_under = P(rush_yds < line) over all sim trials; p_over = P(rush_yds > line); half lines never push"
P_MODEL_DEF = "p_model = P(graded side) / (P(under) + P(over)) at the leg line (push removed; equal to P(side) on x.5)"
DEFAULT_ROSTER = Path(__file__).resolve().parents[1] / "data/historical/nflverse/ros_2026.parquet"


def _short(full: str) -> str | None:
    parts = [p for p in str(full).replace(".", ". ").split() if p not in ("Jr.", "Sr.", "II", "III", "IV", "V")]
    return f"{parts[0][0]}.{parts[-1]}" if len(parts) >= 2 else None


def gsis_map_from_pbp(pbp: pd.DataFrame) -> dict:
    """(team, nflverse short name) -> gsis id from the as-of play-by-play (rusher / passer / receiver columns).
    A (team, name) seen with more than one id is left out (never guessed)."""
    seen: dict = {}
    for role in ("rusher", "passer", "receiver"):
        n, i = f"{role}_player_name", f"{role}_player_id"
        if n not in pbp or i not in pbp or "posteam" not in pbp:
            continue
        d = pbp[["posteam", n, i]].dropna()
        for t, nm, g in d.drop_duplicates().itertuples(index=False):
            seen.setdefault((str(t), str(nm)), set()).add(str(g))
    return {k: next(iter(v)) for k, v in seen.items() if len(v) == 1}


def _player_series(columns, values, include_kneels: bool):
    v = np.asarray(values, dtype=float)
    ix = {tuple(c): j for j, c in enumerate(columns)}
    players = sorted({(t, p) for (t, p, s) in ix if s == "carries" and p != UNASSIGNED
                      and (v[:, ix[(t, p, s)]] > 0).any()})
    for t, p in players:
        y = np.zeros(v.shape[0])
        for s in ("rush_yds",) + (("kneel_yds",) if include_kneels else ()):
            if (t, p, s) in ix:
                y = y + v[:, ix[(t, p, s)]]
        car = v[:, ix[(t, p, "carries")]]
        yield t, p, y, car


def build(columns, values, game_id: str, gsis_map: dict | None = None, roster: pd.DataFrame | None = None,
          include_kneels: bool = True, meta: dict | None = None) -> dict:
    """columns: [[team, player, stat], ...]; values: (n_trials x columns). Returns {"summary", "cdf", "meta"}."""
    gsis_map = gsis_map or {}
    ros = {}
    if roster is not None and len(roster):
        r = roster.dropna(subset=["gsis_id"]).drop_duplicates("gsis_id", keep="last")
        ros = {g: (pos, fn) for g, pos, fn in zip(r.gsis_id, r.position, r.full_name)}
    srows, crows = [], []
    n = int(np.asarray(values).shape[0])
    for t, p, y, car in _player_series(columns, values, include_kneels):
        if not np.all(y == np.round(y)):
            raise ValueError(f"{t} {p}: rushing yards are not integer-valued; refusing to build a yard-line CDF")
        g = gsis_map.get((t, p))
        pos, fn = ros.get(g, (None, None)) if g else (None, None)
        ids = dict(game_id=game_id, team=t, player=p, gsis=g, position=pos, full_name=fn)
        qs = np.quantile(y, QUANTILES)
        srows.append(dict(ids, n_trials=n, p_any_carry=float(np.mean(car > 0)), carries_mean=float(car.mean()),
                          mean=float(y.mean()), sd=float(y.std()), min=float(y.min()), max=float(y.max()),
                          **{f"q{int(round(q * 100)):02d}": float(v) for q, v in zip(QUANTILES, qs)}))
        lo = min(GRID_MIN, math.floor(y.min()) - 0.5)
        hi = max(GRID_MAX, math.ceil(y.max()) + 0.5)
        grid = np.arange(lo, hi + 0.5, 1.0)
        ys = np.sort(y)
        pu = np.searchsorted(ys, grid, side="left") / n
        for L, u in zip(grid, pu):
            crows.append((game_id, t, p, g, pos, float(L), float(u), float(1.0 - u)))
    summary = pd.DataFrame(srows, columns=list(SUMMARY_COLUMNS))
    cdf = pd.DataFrame(crows, columns=list(CDF_COLUMNS))
    m = {"schema": SCHEMA, "game_id": game_id, "n_trials": n, "n_players": len(summary),
         "rush_yds_definition": RUSH_YDS_DEF if include_kneels else "player_box rush_yds only (kneels excluded)",
         "p_under_definition": P_UNDER_DEF, "p_model_definition": P_MODEL_DEF, "quantiles": list(QUANTILES),
         "grid": {"min": GRID_MIN, "max": GRID_MAX, "step": 1.0, "half_lines": True},
         "source": "core/possession_engine_v0/player_box.py per-trial lines (observational; engine unchanged)",
         "research_only": True, "projection_ready": False, **(meta or {})}
    m["projection_ready"] = False
    m["research_only"] = True
    return {"summary": summary, "cdf": cdf, "meta": m}


def p_under(cdf: pd.DataFrame, line: float, team: str | None = None, player: str | None = None,
            gsis: str | None = None) -> dict:
    """Exact P(under / push / over) at any line from the half-line CDF (integer yards)."""
    g = cdf[(cdf.gsis == gsis)] if gsis is not None else cdf[(cdf.team == team) & (cdf.player == player)]
    if g.empty:
        raise KeyError(f"no rush distribution for {gsis or (team, player)}")
    lines, pu = g.line.to_numpy(), g.p_under.to_numpy()

    def lt(k: float) -> float:  # P(X < k) for a half line k
        if k < lines[0]:
            return 0.0
        if k > lines[-1]:
            return 1.0
        return float(pu[int(round(k - lines[0]))])
    c = math.ceil(line)
    under = lt(c - 0.5)                                   # P(X <= ceil(L)-1) = P(X < L) for integer X
    push = (lt(line + 0.5) - lt(line - 0.5)) if float(line).is_integer() else 0.0
    return {"p_under": under, "p_push": push, "p_over": 1.0 - under - push}


def attach_p_model(legs: pd.DataFrame, cdf: pd.DataFrame | list, label: str | None = None) -> pd.DataFrame:
    """Fill blank p_model on rushyds legs (selective_edge_live schema). Only appends columns; input not mutated."""
    if isinstance(cdf, list):
        cdf = pd.concat(cdf, ignore_index=True)
    out = legs.copy()
    if "p_model" not in out:
        out["p_model"] = np.nan
    out["p_model"] = out["p_model"].astype(float)
    match, src = [], []
    srcname = label or "pipeline/rush_dist " + SCHEMA
    by_game = {gid: g for gid, g in cdf.groupby("game_id")}
    for i, r in out.iterrows():
        if str(r.get("market")) != "rushyds":
            match.append(None); src.append(None); continue
        if pd.notna(r.get("p_model")):
            match.append("preset"); src.append(None); continue
        g = by_game.get(r.get("game_id"))
        hit, how = None, "no_player"
        if g is not None:
            gs = r.get("gsis")
            if pd.notna(gs) and (g.gsis == gs).any():
                hit, how = g[g.gsis == gs], "gsis"
            else:
                sn = _short(r.get("player", ""))
                cand = g[g.player == sn] if sn else g.iloc[0:0]
                if cand.empty and "full_name" in g:
                    cand = g[g.get("full_name") == r.get("player")]
                if cand[["team", "player"]].drop_duplicates().shape[0] == 1:
                    hit, how = cand, "name"
                elif len(cand):
                    how = "ambiguous_name"
        if hit is None or pd.isna(r.get("line")):
            match.append(how if hit is None else "no_line"); src.append(None); continue
        p = p_under(hit, float(r.line), team=hit.team.iloc[0], player=hit.player.iloc[0])
        denom = p["p_under"] + p["p_over"]
        side = str(r.get("side"))
        if denom <= 0 or side not in ("Under", "Over"):
            match.append("undefined"); src.append(None); continue
        out.at[i, "p_model"] = (p["p_under"] if side == "Under" else p["p_over"]) / denom
        match.append(how); src.append(f"{srcname} {hit.team.iloc[0]} {hit.player.iloc[0]}")
    out["p_model_match"] = match
    out["p_model_source"] = src
    return out


def _paths(out_dir: Path, game_id: str) -> dict:
    out_dir = Path(out_dir)
    return {"json": out_dir / f"{game_id}.rush_dist.json", "cdf": out_dir / f"{game_id}.rush_dist.cdf.csv",
            "summary": out_dir / f"{game_id}.rush_dist.summary.csv"}


def write(d: dict, out_dir) -> dict:
    p = _paths(Path(out_dir), d["meta"]["game_id"])
    p["json"].parent.mkdir(parents=True, exist_ok=True)
    d["summary"].to_csv(p["summary"], index=False)
    d["cdf"].to_csv(p["cdf"], index=False, float_format="%.6f")
    meta = dict(d["meta"], files={k: v.name for k, v in p.items() if k != "json"},
                cdf_sha256=hashlib.sha256(p["cdf"].read_bytes()).hexdigest())
    p["json"].write_text(json.dumps(meta, indent=1, sort_keys=True, default=str) + "\n")
    return p


def read(out_dir, game_id: str) -> dict:
    p = _paths(Path(out_dir), game_id)
    dt = {"gsis": "string", "position": "string", "full_name": "string"}
    cdf = pd.read_csv(p["cdf"], dtype={k: v for k, v in dt.items() if k in CDF_COLUMNS})
    cdf["gsis"] = cdf.gsis.astype(object).where(cdf.gsis.notna(), None)
    cdf["position"] = cdf.position.astype(object).where(cdf.position.notna(), None)
    return {"meta": json.loads(p["json"].read_text()), "cdf": cdf,
            "summary": pd.read_csv(p["summary"], dtype=dt)}


def load_npz(path) -> tuple[list, np.ndarray]:
    z = np.load(path, allow_pickle=False)
    cols = [str(c).split("|") for c in z["columns"]]
    return cols, z["values"].astype(np.float64)


def build_from_box(columns, values, game_id: str, pbp_path=None, roster_path=DEFAULT_ROSTER, meta=None) -> dict:
    gm = {}
    if pbp_path:
        use = ["posteam"] + [f"{r}_player_{k}" for r in ("rusher", "passer", "receiver") for k in ("name", "id")]
        gm = gsis_map_from_pbp(pd.read_parquet(pbp_path, columns=use))
    ros = pd.read_parquet(roster_path, columns=["gsis_id", "position", "full_name"]) if roster_path and \
        Path(roster_path).exists() else None
    return build(columns, values, game_id=game_id, gsis_map=gm, roster=ros, meta=meta)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="NFL-75 rushing-yards distribution artifact (research only).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--npz", required=True)
    b.add_argument("--game", required=True)
    b.add_argument("--pbp")
    b.add_argument("--roster", default=str(DEFAULT_ROSTER))
    b.add_argument("--out", default=str(Path(__file__).resolve().parent / "ledgers"))
    at = sub.add_parser("attach")
    at.add_argument("--legs", required=True)
    at.add_argument("--dist", required=True, action="append", help="directory holding <game>.rush_dist.* files")
    at.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "build":
        cols, vals = load_npz(a.npz)
        meta = {"source_npz": Path(a.npz).name, "source_npz_sha256": hashlib.sha256(Path(a.npz).read_bytes()).hexdigest()}
        sj = Path(a.npz).with_name(f"{a.game}.sim100k.json")
        if sj.exists():
            res = (json.loads(sj.read_text()).get("result") or {})
            meta.update({k: res.get(k) for k in ("n", "seed", "config_id", "pbp") if k in res})
        d = build_from_box(cols, vals, a.game, pbp_path=a.pbp, roster_path=a.roster, meta=meta)
        p = write(d, a.out)
        print(f"rush_dist: {d['meta']['n_players']} players, {d['meta']['n_trials']:,} trials -> {p['cdf']}")
        return 0
    legs = pd.read_csv(a.legs)
    cdfs = []
    for dd in a.dist:
        for j in sorted(Path(dd).glob("*.rush_dist.json")):
            cdfs.append(read(dd, json.loads(j.read_text())["game_id"])["cdf"])
    if not cdfs:
        raise SystemExit(f"no *.rush_dist.json under {a.dist}")
    out = attach_p_model(legs, cdfs)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(a.out, index=False)
    rm = out[out.market == "rushyds"]
    print(f"rush_dist attach: p_model filled on {int(rm.p_model.notna().sum())}/{len(rm)} rushyds legs -> {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
