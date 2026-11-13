"""NFL-75: Week 10+ rush-yards p_model from the SAME sim ensemble the Phase 4 fit used, with a QB starter gate.

How Phase 4 got p_model for historical legs (traced; reproduced bit-for-bit, see tests):
  calibration/selective_edge_run.py build  reads backtests/selective_under_alt_2026-11-12 candidates.csv (p_model)
  <- s3_candidates.py: L = confidence_check_2026-11-03/legs_with_probs.csv; p_over = L[ENS].mean(axis=1) with
     ENS = sim_v5|0.5, sim_v6|0.5, sim_v6_fix|0.5; main Under p_model = 1 - p_over
  <- analyze.py: "<engine>|0.5" = sims/<engine>_opp0.5_w<W>.csv [p_mc, p_bias, p_gr].mean(axis=1)
  <- run_sims.py <engine> 0.5 <W>: CC_OPP=0.5, N=20,000, PBP cut at game_date < first game date of week W
     (W9: < 2026-11-02), sim_v6 / sim_v6_fix multipliers refit from engines/<engine>_backtest.csv weeks < min(W, 8),
     one sim per leg with rungs=[line]; p_* = P(stat >= line).
This module runs those three engines (vendored byte-identical in calibration/simv56/engines, sha256-pinned and checked
before every run) with exactly those settings, each in its own subprocess (the engines read CC_* env vars and the PBP
at import). Inputs: the committed as-of nflverse PBP and the Nov 2 players table the original runs used
(data/historical/nflverse/derived_pit/players_slim_shared_src_20261102.parquet: the 4 columns the engines read).
The engines seed each draw from md5(player name | market | mode), so the leg's player NAME must be the book's display
name (as in the original legs and in freeze_v2), and every line for one player is answered from one sim.

QB / availability gate (new, outside the engines and outside the frozen classifier; blocks by leaving p_model blank,
which the classifier labels INSUFFICIENT EVIDENCE / model_prob_missing):
  starter per team = lowest pos_rank QB in the newest nflverse depth-chart snapshot at or before as_of, skipping QBs
  with this week's injury report_status Out / Doubtful or listed in an inactives file; QB legs for anyone else ->
  qb_not_starter; no depth chart for the team -> qb_starter_unknown; any leg whose player is Out / Doubtful / inactive
  -> out_or_doubtful; a starter with fewer than 2 prior games as primary passer (>= 10 attempts) before the cutoff ->
  qb_starter_thin_history (the engines model a player from his own active games, so a backup-turned-starter would be
  priced off relief snaps). Every gated row carries the depth-chart / injury source URL and timestamps.

    python -m calibration.simv56_pmodel fetch --out <dir>        # nflverse depth charts + injuries (public, no Odds API)
    python -m calibration.simv56_pmodel run --legs legs.csv --week 10 --sources <fetch dir> \
        [--inactives inactives.csv] [--freeze-glob 'pregame/price_freezes/*/freeze_v2_*.json'] --out <dir>
    python -m calibration.simv56_pmodel grade --legs <dir>/legs_p.csv --out <dir>/graded   # frozen grade_live
Research only; projection_ready stays false. No Odds API calls."""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ENGINE_DIR = ROOT / "calibration" / "simv56" / "engines"
PBP_DEFAULT = ROOT / "data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet"
PLAYERS_DEFAULT = ROOT / "data/historical/nflverse/derived_pit/players_slim_shared_src_20261102.parquet"
GAMES_CSV = ROOT / "data/historical/nflverse/games.csv"
ENGINES = ("sim_v5", "sim_v6", "sim_v6_fix")
OPP = "0.5"
N_TRIALS = 20000
ENS = [f"{e}|{OPP}" for e in ENGINES]
CALIB_WEEKS_RULE = "backtest weeks < min(W, 8)"
CUTOFF_OVERRIDES = {9: "2026-11-02"}          # run_sims.py: W9 cut at 2026-11-02 (MNF), not the week's first game
OUT_STATUSES = ("Out", "Doubtful")
MIN_STARTER_GAMES, PRIMARY_PASS_ATT = 2, 10
SOURCE_URLS = {
    "depth_charts": "https://github.com/nflverse/nflverse-data/releases/download/depth_charts/depth_charts_2026.parquet",
    "injuries": "https://github.com/nflverse/nflverse-data/releases/download/injuries/injuries_2026.parquet"}
P_MODEL_SOURCE = f"simv56 ens({','.join(ENGINES)})|opp{OPP}|n{N_TRIALS}"


class SimV56Error(RuntimeError):
    pass


def _sha(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def verify_engines(engine_dir: Path = ENGINE_DIR) -> dict:
    sums = {}
    for line in (ENGINE_DIR / "SHA256SUMS").read_text().split("\n"):
        if line.strip():
            h, f = line.split()
            sums[f] = h
    bad = [f for f, h in sums.items() if not (Path(engine_dir) / f).exists() or _sha(Path(engine_dir) / f) != h]
    if bad:
        raise SimV56Error(f"vendored engine files differ from SHA256SUMS: {bad}")
    return sums


def cutoff_for_week(week: int, games_csv: Path = GAMES_CSV) -> str:
    if week in CUTOFF_OVERRIDES:
        return CUTOFF_OVERRIDES[week]
    g = pd.read_csv(games_csv, usecols=["season", "week", "game_type", "gameday"])
    g = g[(g.season == 2026) & (g.week == week) & (g.game_type == "REG")]
    if g.empty:
        raise SimV56Error(f"no 2026 week {week} games in {games_csv}")
    return str(g.gameday.min())


def make_src(dest: Path, pbp: Path = PBP_DEFAULT, players: Path = PLAYERS_DEFAULT) -> Path:
    """Engine SRC dir: symlinks named as the engines expect (no copy, no disk cost)."""
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    for name, target in (("play_by_play_2026.parquet", pbp), ("players.parquet", players)):
        link = dest / name
        if link.is_symlink() or link.exists():
            link.unlink()
        link.symlink_to(Path(target).resolve())
    return dest


# ------------------------------------------------------------------ engine worker (one engine per subprocess)
def _worker(engine: str, legs_json: str, week: int, cutoff: str, src: str, n: int, out: str) -> None:
    """Exactly confidence_check_2026-11-03/run_sims.py, one leg = one sim with rungs = its lines."""
    os.environ.update(CC_OPP=OPP, CC_SRC=src, CC_CUTOFF=cutoff, SIMV6_SRC=src)
    sys.path.insert(0, str(ENGINE_DIR))
    import importlib
    import warnings
    warnings.filterwarnings("ignore")
    legs = json.loads(Path(legs_json).read_text())
    if engine == "sim_v5":
        M = importlib.import_module("cc_sim_v5")
        M.N = n

        def run(leg):
            return M.sim(leg)[0]
        calib = None
    else:
        M = importlib.import_module("cc_sim_" + engine.split("sim_")[1])
        bt = pd.read_csv(ENGINE_DIR / f"{engine}_backtest.csv", float_precision=FLOAT_PRECISION)
        tr = bt[bt.week < min(week, 8)]
        calib = M.fit(tr) if len(tr) else None
        E = M.Engine(cutoff=cutoff, calib=calib, n=n)

        def run(leg):
            return E.sim(leg)[0]
    rows = []
    for L in legs:
        leg = dict(player=L["player"], gsis=L["gsis"], team=L["team"], opp=L["opp"], market=L["market"],
                   spread=L["spread"], rungs=list(L["lines"]))
        try:
            o = run(leg)
        except Exception as ex:  # noqa: BLE001  (same as run_sims: error row, no probability)
            for ln in L["lines"]:
                rows.append(dict(gsis=L["gsis"], player=L["player"], market=L["market"], line=ln, err=repr(ex)[:120]))
            continue
        for ln in L["lines"]:
            rows.append(dict(gsis=L["gsis"], player=L["player"], market=L["market"], line=ln,
                             **{f"p_{m}": o[m]["rungs"][str(ln)] for m in ("mc", "bias", "gr")},
                             **{f"med_{m}": o[m]["median"] for m in ("mc", "bias", "gr")}))
    pd.DataFrame(rows).to_csv(out, index=False)
    Path(out).with_suffix(".json").write_text(json.dumps(dict(
        engine=engine, opp=OPP, week=week, cutoff=cutoff, n=n, calib_rule=CALIB_WEEKS_RULE, calib=calib), default=str,
        indent=1))


def run_all(legs: pd.DataFrame, week: int, src: Path, workdir: Path, n: int = N_TRIALS,
            cutoff: str | None = None) -> dict:
    """legs: player, gsis, team, opp, market, spread, line (one row per line). Returns {engine: DataFrame}."""
    verify_engines()
    cutoff = cutoff or cutoff_for_week(week)
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    grp = (legs.groupby(["player", "gsis", "team", "opp", "market", "spread"], dropna=False, sort=True)
           .line.apply(lambda s: sorted({float(x) for x in s})).reset_index().rename(columns={"line": "lines"}))
    recs = []
    for r in grp.to_dict("records"):
        r["gsis"] = None if pd.isna(r["gsis"]) else r["gsis"]
        r["spread"] = float(r["spread"])
        recs.append(r)
    lj = workdir / "engine_legs.json"
    lj.write_text(json.dumps(recs, indent=1))
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    procs = {}
    for e in ENGINES:
        out = workdir / f"{e}_opp{OPP}_w{week}.csv"
        cmd = [sys.executable, "-m", "calibration.simv56_pmodel", "_worker", e, str(lj), str(week), cutoff,
               str(Path(src).resolve()), str(n), str(out)]
        procs[e] = (subprocess.Popen(cmd, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE), out)
    res = {}
    for e, (p, out) in procs.items():
        so, se = p.communicate()
        if p.returncode != 0:
            raise SimV56Error(f"{e} worker failed: {se.decode()[-600:]}")
        res[e] = pd.read_csv(out, float_precision=FLOAT_PRECISION)
    return res


# The original pipeline ran on the box's pandas 3.0.6, whose C float parser ("high", the default) can land 1 ulp off
# the written text. pandas 3.1.x parses the text exactly under every float_precision, so the Phase 4 values are only
# bit-reproducible on pandas 3.0.6 (on 3.1.x a few legs differ by 1 ulp, ~2e-16). The parser is pinned to "high" and
# the run records whether it is in the bit-exact environment.
FLOAT_PRECISION = "high"
PHASE4_PANDAS = "3.0.6"
BIT_EXACT_ENV = pd.__version__ == PHASE4_PANDAS


def _csv_rt(df: pd.DataFrame) -> pd.DataFrame:
    """One pandas to_csv -> read_csv round trip, as the original pipeline did between stages (parser pinned, see FLOAT_PRECISION)."""
    import io
    return pd.read_csv(io.StringIO(df.to_csv(index=False)), float_precision=FLOAT_PRECISION)


def ensemble(per: dict) -> pd.DataFrame:
    """Same arithmetic AND the same CSV hand-offs as the original pipeline: run_sims writes sims/*.csv, analyze.py
    reads them (default parser), row-means p_mc/p_bias/p_gr, writes legs_with_probs.csv; s3_candidates.py reads it
    (default parser) and row-means the three engines. The default C float parser can land one ulp off the written
    text, so each hand-off is replayed to stay bit-identical."""
    K = ["gsis", "market", "line"]
    D = None
    for e in ENGINES:
        d = per[e].copy()
        if "err" in d:
            d = d[d.err.isna()]
        d = _csv_rt(d[K + ["p_mc", "p_bias", "p_gr"]])                  # sims/<engine>_opp0.5_w<W>.csv
        d["p"] = d[["p_mc", "p_bias", "p_gr"]].mean(axis=1)
        d = d[K + ["p"]].rename(columns={"p": f"{e}|{OPP}"})
        D = d if D is None else D.merge(d, on=K, how="inner")
    D = _csv_rt(D)                                                      # legs_with_probs.csv
    D["p_over"] = D[ENS].mean(axis=1)
    D["p_under"] = 1 - D.p_over
    return D


# ------------------------------------------------------------------ QB / availability gate
def _week_inj(inj: pd.DataFrame, week: int) -> pd.DataFrame:
    i = inj[inj.week == week] if "week" in inj else inj
    return i[i.report_status.isin(OUT_STATUSES)]


def qb_starters(depth: pd.DataFrame, inj: pd.DataFrame, week: int, as_of: str, source: dict,
                inactives: pd.DataFrame | None = None) -> pd.DataFrame:
    d = depth[(depth.pos_abb == "QB") & (depth.dt <= as_of)]
    out_ids = set(_week_inj(inj, week).gsis_id.dropna())
    ina_ids = set(inactives.gsis_id.dropna()) if inactives is not None and len(inactives) else set()
    rows = []
    for team, g in d.groupby("team"):
        snap = g[g.dt == g.dt.max()].sort_values("pos_rank")
        skipped, starter = [], None
        for r in snap.itertuples():
            if r.gsis_id in out_ids or r.gsis_id in ina_ids:
                skipped.append(f"{r.player_name} ({'inactive' if r.gsis_id in ina_ids else 'Out/Doubtful'})")
                continue
            starter = r
            break
        rows.append(dict(team=team, starter=starter.player_name if starter else None,
                         starter_gsis=starter.gsis_id if starter else None, depth_dt=snap.dt.iloc[0],
                         skipped="; ".join(skipped),
                         depth_source=(source.get("depth_charts") or {}).get("url"),
                         depth_retrieved_utc=(source.get("depth_charts") or {}).get("retrieved_utc"),
                         injury_source=(source.get("injuries") or {}).get("url"),
                         injury_retrieved_utc=(source.get("injuries") or {}).get("retrieved_utc"),
                         inactives_source=(inactives.source.iloc[0] if inactives is not None and len(inactives)
                                           and "source" in inactives else None),
                         inactives_retrieved_utc=(inactives.retrieved_utc.iloc[0] if inactives is not None
                                                  and len(inactives) and "retrieved_utc" in inactives else None),
                         as_of=as_of, week=week))
    return pd.DataFrame(rows)


def starter_history(pbp: pd.DataFrame, cutoff: str) -> dict:
    p = pbp[(pbp.game_date < cutoff) & (pbp.season_type == "REG") & (pbp.two_point_attempt.fillna(0) != 1)]
    p = p[p.pass_attempt == 1]
    by = ["passer_player_id", "posteam"] if "posteam" in p else ["passer_player_id"]   # the engines only read the
    c = p.groupby(by + ["game_id"]).size()                                            # leg team's games
    c = c[c >= PRIMARY_PASS_ATT].reset_index().groupby(by).size()
    return {k: int(v) for k, v in c.items()}


def gate_legs(legs: pd.DataFrame, starters: pd.DataFrame, inj: pd.DataFrame, week: int, starter_history: dict,
              inactives: pd.DataFrame | None = None) -> pd.DataFrame:
    st = starters.set_index("team") if len(starters) else pd.DataFrame()
    out_ids = set(_week_inj(inj, week).gsis_id.dropna())
    ina_ids = set(inactives.gsis_id.dropna()) if inactives is not None and len(inactives) else set()
    meta_cols = ["depth_source", "depth_dt", "depth_retrieved_utc", "injury_source", "injury_retrieved_utc",
                 "inactives_source", "inactives_retrieved_utc"]
    rows = []
    for r in legs.itertuples(index=False):
        team, g = getattr(r, "team", None), getattr(r, "gsis", None)
        m = {c: (st.loc[team, c] if team in st.index else None) for c in meta_cols}
        if g in ina_ids or g in out_ids:
            gate, det = "out_or_doubtful", "inactive" if g in ina_ids else "injury report Out/Doubtful"
        elif str(getattr(r, "position", "")) == "QB":
            if team not in st.index or pd.isna(st.loc[team, "starter_gsis"]):
                gate, det = "qb_starter_unknown", f"no depth-chart QB for {team}"
            elif st.loc[team, "starter_gsis"] != g:
                gate, det = "qb_not_starter", f"starter {st.loc[team, 'starter']}"
            elif starter_history.get((g, team), starter_history.get(g, 0)) < MIN_STARTER_GAMES:
                n = starter_history.get((g, team), starter_history.get(g, 0))
                gate, det = "qb_starter_thin_history", f"{n} prior {team} games with >={PRIMARY_PASS_ATT} att"
            else:
                n = starter_history.get((g, team), starter_history.get(g, 0))
                gate, det = "ok", f"depth-chart starter, {n} prior {team} primary games"
        else:
            gate, det = "ok", ""
        rows.append(dict(gate=gate, gate_detail=det, **m))
    g = pd.DataFrame(rows, index=legs.index)
    ids = [c for c in ("player", "gsis", "team", "position") if c in legs]
    return pd.concat([legs[ids], g], axis=1)


# ------------------------------------------------------------------ legs plumbing
def home_spread_from_freeze(path) -> tuple:
    d = json.loads(Path(path).read_text())
    c = (d.get("consensus") or {}).get("spread") or {}
    c = c.get("consensus") if isinstance(c, dict) else None
    line = c.get("line") if isinstance(c, dict) else None
    return d["meta"]["game_id"], (None if line is None else float(line))


def team_of_from_pbp(pbp: pd.DataFrame, cutoff: str) -> dict:
    """gsis -> the offense he appeared for most recently before the cutoff (rusher / passer / receiver rows)."""
    p = pbp[pbp.game_date < cutoff]
    parts = [p[["game_date", "posteam", f"{r}_player_id"]].dropna().rename(columns={f"{r}_player_id": "g"})
             for r in ("rusher", "passer", "receiver")]
    d = pd.concat(parts).sort_values("game_date", kind="stable")
    return d.groupby("g").posteam.last().to_dict()


def leg_inputs(legs: pd.DataFrame, team_of: dict, home_spread: dict) -> pd.DataFrame:
    x = legs.copy()
    if "team" not in x or x.team.isna().any():
        x["team"] = [t if isinstance(t, str) else team_of.get(g) for t, g in
                     zip(x.get("team", pd.Series([None] * len(x), index=x.index)), x.gsis)]
    home = x.game_id.str.split("_").str[3]
    away = x.game_id.str.split("_").str[2]
    x["opp"] = np.where(x.team == home, away, np.where(x.team == away, home, None))
    hs = x.game_id.map(home_spread)
    x["spread"] = np.where(x.team == home, hs, -hs.astype(float))
    return x


def attach(legs: pd.DataFrame, ens: pd.DataFrame, gate: pd.DataFrame) -> pd.DataFrame:
    out = legs.copy()
    if "p_model" not in out:
        out["p_model"] = np.nan
    out["p_model"] = out.p_model.astype(float)
    key = {(g, m, float(l)): (po, pu) for g, m, l, po, pu in
           zip(ens.gsis, ens.market, ens.line, ens.p_over, ens.p_under)}
    gates = list(gate.gate)
    src, match = [], []
    for i, (idx, r) in enumerate(out.iterrows()):
        if r.market != "rushyds":
            src.append(None); match.append(None); continue
        if pd.notna(r.p_model):
            src.append(None); match.append("preset"); continue
        if gates[i] != "ok":
            src.append(None); match.append(f"gated:{gates[i]}"); continue
        hit = key.get((r.gsis, "rushyds", float(r.line))) if pd.notna(r.line) else None
        if hit is None:
            src.append(None); match.append("no_sim"); continue
        out.at[idx, "p_model"] = hit[1] if r.side == "Under" else hit[0]
        src.append(P_MODEL_SOURCE); match.append("gsis")
    out["p_model_source"], out["p_model_match"], out["gate"] = src, match, gates
    for c in [c for c in gate.columns if c.startswith(("gate_", "depth_", "injury_", "inactives_"))]:
        out[c] = list(gate[c])
    return out


# ------------------------------------------------------------------ CLI
def fetch(out_dir: Path) -> dict:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    man = {}
    for k, url in SOURCE_URLS.items():
        f = out_dir / Path(url).name
        with urllib.request.urlopen(url, timeout=60) as r:
            f.write_bytes(r.read())
        man[k] = dict(url=url, file=f.name, sha256=_sha(f),
                      retrieved_utc=datetime.now(timezone.utc).isoformat(timespec="seconds"))
    (out_dir / "sources.json").write_text(json.dumps(man, indent=1))
    return man


def run_cli(a) -> int:
    week = int(a.week)
    cutoff = cutoff_for_week(week)
    src_dir = Path(a.sources)
    man = json.loads((src_dir / "sources.json").read_text())
    depth = pd.read_parquet(src_dir / man["depth_charts"]["file"])
    inj = pd.read_parquet(src_dir / man["injuries"]["file"])
    ina = pd.read_csv(a.inactives) if a.inactives else None
    if ina is not None and not {"gsis_id", "source", "retrieved_utc"} <= set(ina.columns):
        raise SimV56Error("inactives CSV needs gsis_id, source, retrieved_utc columns")
    as_of = a.as_of or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    pbp = pd.read_parquet(a.pbp, columns=["game_id", "game_date", "season_type", "pass_attempt", "two_point_attempt",
                                          "passer_player_id", "rusher_player_id", "receiver_player_id", "posteam"])
    if (pbp.game_date >= cutoff).any():
        pbp = pbp[pbp.game_date < cutoff]                    # as-of: nothing on or after the cutoff
    legs = pd.read_csv(a.legs)
    legs = legs[legs.week == week].reset_index(drop=True)
    hs = {}
    for f in sorted(glob.glob(str(ROOT / a.freeze_glob))):
        gid, line = home_spread_from_freeze(f)
        if gid.startswith(f"2026_{week:02d}_") and line is not None:
            hs[gid] = line                                   # newest freeze per game wins (sorted by name/time)
    if a.home_spreads:
        hs.update({r.game_id: float(r.home_spread) for r in pd.read_csv(a.home_spreads).itertuples()})
    x = leg_inputs(legs, team_of_from_pbp(pbp, cutoff), hs)
    st = qb_starters(depth, inj, week, as_of, man, ina)
    gate = gate_legs(x, st, inj, week, starter_history(pbp, cutoff), ina)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    st.to_csv(out / "qb_starters.csv", index=False)
    runnable = x[(x.market == "rushyds") & (gate.gate == "ok") & x.spread.notna() & x.opp.notna() & x.line.notna()]
    import time
    t0 = time.time()
    per = run_all(runnable[["player", "gsis", "team", "opp", "market", "spread", "line"]].drop_duplicates(),
                  week, make_src(out / "src", pbp=Path(a.pbp)), out, n=N_TRIALS, cutoff=cutoff) if len(runnable) \
        else {e: pd.DataFrame(columns=["gsis", "market", "line", "p_mc", "p_bias", "p_gr"]) for e in ENGINES}
    ens = ensemble(per)
    ens.to_csv(out / "ensemble.csv", index=False)
    res = attach(x, ens, gate)
    res.to_csv(out / "legs_p.csv", index=False)
    meta = dict(schema="nfl75-simv56-pmodel/1", pandas_version=pd.__version__,
                phase4_bit_exact_env=BIT_EXACT_ENV, week=week, cutoff=cutoff, as_of=as_of, n=N_TRIALS, opp=OPP,
                engines=list(ENGINES), engine_sha256=verify_engines(), pbp=Path(a.pbp).name, pbp_sha256=_sha(a.pbp),
                players=PLAYERS_DEFAULT.name, sources=man, inactives=a.inactives, runtime_sec=round(time.time() - t0, 1),
                n_rush_legs=int((x.market == "rushyds").sum()), n_sim_players=int(runnable.gsis.nunique()),
                gate_counts=res[res.market == "rushyds"].gate.value_counts().to_dict(),
                p_model_filled=int(res[res.market == "rushyds"].p_model.notna().sum()),
                research_only=True, projection_ready=False)
    (out / "meta.json").write_text(json.dumps(meta, indent=1, default=str))
    print(json.dumps({k: meta[k] for k in ("week", "cutoff", "as_of", "runtime_sec", "n_rush_legs", "n_sim_players",
                                           "gate_counts", "p_model_filled")}, indent=1, default=str))
    return 0


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "_worker":
        e, lj, w, cut, src, n, out = argv[1:8]
        _worker(e, lj, int(w), cut, src, int(n), out)
        return 0
    ap = argparse.ArgumentParser(description="NFL-75 simv56 p_model (research only)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch")
    f.add_argument("--out", required=True)
    r = sub.add_parser("run")
    r.add_argument("--legs", required=True)
    r.add_argument("--week", required=True, type=int)
    r.add_argument("--sources", required=True, help="dir written by `fetch` (sources.json + parquet files)")
    r.add_argument("--pbp", default=str(PBP_DEFAULT))
    r.add_argument("--inactives", help="CSV: team, gsis_id, player, source, retrieved_utc (post-T-90 re-run)")
    r.add_argument("--freeze-glob", default="pregame/price_freezes/*/freeze_v2_*.json")
    r.add_argument("--home-spreads", help="CSV game_id, home_spread (overrides freezes)")
    r.add_argument("--as-of", help="UTC ISO; depth-chart snapshots after this are ignored (default now)")
    r.add_argument("--out", required=True)
    gr = sub.add_parser("grade", help="frozen selective_edge_live.grade_live on legs_p.csv (labels only, pre-game safe)")
    gr.add_argument("--legs", required=True)
    gr.add_argument("--pbp", default=str(PBP_DEFAULT))
    gr.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "grade":
        from calibration.selective_edge_live import grade_live
        g = grade_live(pd.read_csv(a.legs), pd.read_parquet(a.pbp, columns=[
            "week", "game_id", "posteam", "rush_attempt", "rusher_player_id", "receiver_player_id", "qb_kneel",
            "pass_attempt", "rushing_yards", "receiving_yards", "complete_pass", "two_point_attempt", "season_type"]))
        Path(a.out).mkdir(parents=True, exist_ok=True)
        g.to_csv(Path(a.out) / "live_graded.csv", index=False)
        print(g.groupby(["market", "label"]).size().to_string())
        return 0
    if a.cmd == "fetch":
        print(json.dumps(fetch(Path(a.out)), indent=1))
        return 0
    return run_cli(a)


if __name__ == "__main__":
    raise SystemExit(main())
