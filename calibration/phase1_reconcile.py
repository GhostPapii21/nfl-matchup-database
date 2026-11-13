"""Phase 1 leftovers (refs NFL-75): reconcile simulated per-team-game counts and the clock budget with the SAME teams'
actual weeks 1..w-1 rates from the PBP the sim samples from. Research only, not validated.

    python3 -m calibration.phase1_reconcile --weeks 4-9 --n 200 --workers 6 --tag main
    python3 -m calibration.phase1_reconcile --weeks 4-9 --n 200 --accounting '{"clock_rounding":"round"}' --tag round

Instrumentation is diagnostic-only and in memory (module attributes wrapped for the run, restored after); engine
logic is not changed. Counts: snaps, pass plays, targets, carries, sacks, no-play penalties, turnovers, offensive
TDs, punts, FG attempts, kickoffs, 4th-down decisions by field-position band, inside-10 snap TD share split by
goal-line censoring status, and seconds charged by event type.
"""
from __future__ import annotations
import argparse, json, sys, time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from calibration.common import PBP, PBP_PULLED_ET, MAX_N, LABEL, ROOT, engine_path, engine_version, make_cfg, sha256

BANDS = [(10, "01_10"), (20, "11_20"), (35, "21_35"), (45, "36_45"), (60, "46_60"), (100, "61_99")]
DRIVE_END = {"touchdown", "punt", "field_goal", "turnover", "turnover_on_downs", "safety", "halftime", "def_return",
             "def_return_td", "fg_sparse_miss_default", "kickoff", "ot_start"}
GL_TAGS = ("uncensored", "GL_CENSOR_RESOLVED", "GL_CENSOR_UNRESOLVED", "GL_CENSOR_TRUNCATED")


def band(y):
    for hi, b in BANDS:
        if y <= hi:
            return b
    return "61_99"


def sim_counts(job):
    home, away, week, n, seed, accounting = job
    engine_path()
    import simulate
    from pbp_filter import load_team_history
    cfg = make_cfg(home, away, week, h2h="off")
    if accounting:
        cfg["accounting"] = accounting
    C, secs = Counter(), Counter()
    o_cost, o_row, o_4th = simulate._clock_cost, simulate._apply_row, simulate._fourth_down_decision

    def cost(play_type, rng, cost_map=None, *a, **k):
        v = o_cost(play_type, rng, cost_map, *a, **k)
        secs[f"clock_cost_{play_type}"] += v
        C[f"clock_events_{play_type}"] += 1
        return v

    last = {"st": None, "team": None, "n_ev": 0}

    def row_wrap(rng, catalog, st, row, gl_tag=None, extra_ev=None):
        team, y = st.possession, int(st.yardline_100)
        # possession with >= 1 snap: a new drive starts when the offense changes or a drive-ending event
        # (score, punt, FG try, turnover, downs, half end) happened since this team's previous snap
        ended = any(e.get("type") in DRIVE_END for e in st.events[last["n_ev"]:]) if last["st"] is st else True
        if last["st"] is not st or team != last["team"] or ended:
            C[f"{team}|drives"] += 1
        n0 = len(st.events)
        o_row(rng, catalog, st, row, gl_tag, extra_ev)
        pt = str(row.get("play_type"))
        g = lambda c: 0 if row.get(c) is None or pd.isna(row.get(c)) else int(row.get(c))
        C[f"{team}|snaps"] += 1
        C[f"{team}|{pt}"] += 1
        if pt == "pass":
            if g("sack") == 1:
                C[f"{team}|sacks"] += 1
            elif isinstance(row.get("receiver_player_name"), str):
                C[f"{team}|targets"] += 1
        if pt == "run":
            C[f"{team}|carries"] += 1
        td = any(e.get("type") == "touchdown" and e.get("team") == team for e in st.events[n0:])
        last.update(st=st, team=team, n_ev=len(st.events))
        if y <= 10:
            tag = gl_tag or "uncensored"
            C[f"in10|snaps|{tag}"] += 1
            C[f"in10|td|{tag}"] += int(td)

    def fourth(rng, catalog, st):
        d = o_4th(rng, catalog, st)
        C[f"4th|{band(int(st.yardline_100))}|{d}"] += 1
        return d

    simulate._clock_cost, simulate._apply_row, simulate._fourth_down_decision = cost, row_wrap, fourth
    try:
        h = load_team_history(str(PBP), teams=cfg["history"]["teams"], season=cfg["history"]["season"],
                              weeks=(cfg["history"]["weeks_inclusive"][0], cfg["history"]["weeks_inclusive"][-1]))
        cat, prov = simulate.build_catalog(h["df"], cfg, games_df=h.get("games_df"))
        simulate.attach_semantics(cat, cfg, str(PBP))
        rng = np.random.default_rng(seed)
        for _ in range(n):
            st = simulate.simulate_one(h["df"], cat, cfg, rng)
            for e in st.events:
                ty = e.get("type")
                if ty == "kickoff":
                    C["kickoffs"] += 1
                elif ty == "penalty":
                    C[f"{e.get('offense')}|penalty_events"] += 1
                    if e.get("no_play") and not e.get("live_ball"):
                        C[f"{e.get('offense')}|no_play_penalties"] += 1
                elif ty == "turnover":
                    C[f"{e.get('team')}|turnovers"] += 1
                elif ty == "touchdown":
                    C[f"{e.get('team')}|tds"] += 1
                elif ty == "punt":
                    C["punts"] += 1
                elif ty == "field_goal":
                    C["fga"] += 1
                elif ty == "turnover_on_downs":
                    C["downs"] += 1
            C["ot_games"] += int(any(e.get("type") == "ot_start" for e in st.events))
            C["points"] += st.score_home + st.score_away
        acc = simulate.accounting_from_cfg(cfg)
        ko_sec = int(round(float((cat.clock_map or {}).get("kickoff", 0.0)))) if acc["kickoff_clock"] else 0
        np_sec = simulate.no_play_clock_sec(cat, acc)
    finally:
        simulate._clock_cost, simulate._apply_row, simulate._fourth_down_decision = o_cost, o_row, o_4th
    secs["kickoff_fixed"] = C["kickoffs"] * ko_sec
    return {"game": cfg["game"]["game_id"], "teams": [home, away], "n": n, "counts": dict(C), "secs": dict(secs),
            "clock_map": {k: float(v) for k, v in (cat.clock_map or {}).items()}, "ko_sec": ko_sec, "np_sec": np_sec,
            "accounting": acc}


def actual_counts(pbp, teams, weeks) -> dict:
    d = pbp[pbp["week"].isin(weeks)]
    out = Counter(); games = 0
    for gid, g in d[d["posteam"].isin(teams) | d["defteam"].isin(teams)].groupby("game_id"):
        for t in teams:
            if t not in (g.home_team.iloc[0], g.away_team.iloc[0]):
                continue
            games += 1
            x = g[g.posteam == t]
            sn = x[x.play_type.isin(["pass", "run"]) & x.down.notna()]
            out["snaps"] += len(sn)
            out["pass"] += int((sn.play_type == "pass").sum()); out["run"] += int((sn.play_type == "run").sum())
            out["carries"] += int((sn.play_type == "run").sum())
            out["sacks"] += int((sn.sack == 1).sum())
            out["targets"] += int(((sn.play_type == "pass") & (sn.sack != 1) & sn.receiver_player_name.notna()).sum())
            out["kneels"] += int((x.play_type == "qb_kneel").sum())
            out["no_play_penalties"] += int(((x.play_type == "no_play") & (x.penalty == 1)).sum())
            out["turnovers"] += int(((x.interception == 1) | (x.fumble_lost == 1)).sum())
            out["tds"] += int(((x.touchdown == 1) & (x.td_team == t) & x.play_type.isin(["pass", "run"])).sum())
            out["punts"] += int((x.play_type == "punt").sum()); out["fga"] += int((x.play_type == "field_goal").sum())
            out["drives"] += int(sn.drive.dropna().nunique())
            f4 = x[(x.down == 4) & x.play_type.isin(["punt", "field_goal", "pass", "run"])]
            for r in f4.itertuples():
                out[f"4th|{band(int(r.yardline_100))}|{'go' if r.play_type in ('pass', 'run') else r.play_type}"] += 1
            r10 = sn[sn.yardline_100 <= 10]
            out["in10|snaps"] += len(r10)
            out["in10|td"] += int(((r10.touchdown == 1) & (r10.td_team == t)).sum())
    return {"team_games": games, **dict(out)}


def summarize(res, jobs, pbp) -> dict:
    S, secs, A = Counter(), Counter(), Counter()
    tg = games = atg = 0
    for r, j in zip(res, jobs):
        n = r["n"]; games += n; tg += 2 * n
        for k, v in r["counts"].items():
            head, _, rest = k.partition("|")
            S[rest if head in r["teams"] else k] += v
        secs.update(r["secs"])
        ac = actual_counts(pbp, r["teams"], list(range(1, j[2])))
        atg += ac.pop("team_games"); A.update(ac)
    keys = ["snaps", "pass", "run", "targets", "carries", "sacks", "penalty_events", "no_play_penalties", "turnovers", "tds"]
    table = {k: {"sim": round(S.get(k, 0) / tg, 3), "actual": round(A.get(k, 0) / atg, 3)} for k in keys}
    table["penalty_events"]["note"] = "sim: all enforced fouls (no-play + live-ball); actual column counts only no-play rows here"
    table["penalty_events"]["actual"] = None
    table["punts"] = {"sim": round(S["punts"] / tg, 3), "actual": round(A["punts"] / atg, 3)}
    table["fga"] = {"sim": round(S["fga"] / tg, 3), "actual": round(A["fga"] / atg, 3)}
    table["kneels"] = {"sim": 0.0, "actual": round(A["kneels"] / atg, 3)}
    table["drives"] = {"sim": round(S.get("drives", 0) / tg, 3), "actual": round(A["drives"] / atg, 3),
                       "note": "possessions with >= 1 pass/run snap (both sides)"}
    for k, v in table.items():
        if v["sim"] is not None and v["actual"] is not None:
            v["sim_minus_actual"] = round(v["sim"] - v["actual"], 3)
    fourth = {}
    for _, b in BANDS:
        sd = {d: S.get(f"4th|{b}|{d}", 0) for d in ("punt", "field_goal", "go")}
        ad = {d: A.get(f"4th|{b}|{d}", 0) for d in ("punt", "field_goal", "go")}
        ss, as_ = sum(sd.values()) or 1, sum(ad.values()) or 1
        fourth[b] = {"sim_per_team_game": round(sum(sd.values()) / tg, 3), "actual_per_team_game": round(sum(ad.values()) / atg, 3),
                     "sim_mix": {d: round(v / ss, 3) for d, v in sd.items()}, "actual_mix": {d: round(v / as_, 3) for d, v in ad.items()}}
    gl = {}
    for tag in GL_TAGS:
        s, t = S.get(f"in10|snaps|{tag}", 0), S.get(f"in10|td|{tag}", 0)
        if s:
            gl[tag] = {"snaps_per_team_game": round(s / tg, 3), "td_share": round(t / s, 4)}
    s_all = sum(S.get(f"in10|snaps|{t}", 0) for t in GL_TAGS); t_all = sum(S.get(f"in10|td|{t}", 0) for t in GL_TAGS)
    gl["all_sim"] = {"snaps_per_team_game": round(s_all / tg, 3), "td_share": round(t_all / max(s_all, 1), 4)}
    gl["actual"] = {"snaps_per_team_game": round(A["in10|snaps"] / atg, 3), "td_share": round(A["in10|td"] / max(A["in10|snaps"], 1), 4)}
    clock = {k: round(v / games, 2) for k, v in sorted(secs.items())}
    clock["total_charged_via_clock_cost_and_kickoff_per_game"] = round(sum(secs.values()) / games, 1)
    clock["mean_charged_per_event"] = {k[11:]: round(secs[k] / max(S.get("clock_events_" + k[11:], 0), 1), 3)
                                       for k in secs if k.startswith("clock_cost_")}
    clock["events_per_game"] = {k[13:]: round(S[k] / games, 2) for k in S if k.startswith("clock_events_")}
    cm = Counter()
    for r in res:
        cm.update(r["clock_map"])
    clock["mean_clock_map_target"] = {k: round(v / len(res), 3) for k, v in cm.items()}
    return {"sim_games": games, "sim_team_games": tg, "actual_team_games": atg, "per_team_game": table,
            "fourth_down_by_band": fourth, "inside10": gl, "clock_seconds_per_game": clock,
            "sim_points_per_game": round(S["points"] / games, 3), "sim_ot_rate": round(S["ot_games"] / games, 4)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--weeks", default="4-9")
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--seed", type=int, default=4949)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--accounting", default="")
    ap.add_argument("--tag", default="main")
    a = ap.parse_args(argv)
    if a.n > MAX_N:
        print("refused"); return 2
    acc = json.loads(a.accounting) if a.accounting else None
    lo, _, hi = a.weeks.partition("-")
    weeks = list(range(int(lo), int(hi or lo) + 1))
    pbp = pd.read_parquet(PBP)
    sched = pbp.drop_duplicates("game_id")
    sched = sched[sched.week.isin(weeks) & (sched.season == 2026)]
    jobs = [(r.home_team, r.away_team, int(r.week), a.n, a.seed, acc) for r in sched.itertuples()]
    t0 = time.time(); res = []
    with ProcessPoolExecutor(max_workers=a.workers) as ex:
        for r in ex.map(sim_counts, jobs):
            res.append(r); print(r["game"], flush=True)
    doc = {"label": LABEL, "generated_by": "calibration/phase1_reconcile.py",
           "command": "python3 -m calibration.phase1_reconcile " + " ".join(sys.argv[1:] if argv is None else argv),
           "run_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "runtime_sec": round(time.time() - t0, 1),
           "engine": engine_version(), "accounting_override": acc, "n_per_game": a.n, "seed": a.seed, "weeks": weeks,
           "pbp": {"path": str(PBP.relative_to(ROOT)), "sha256": sha256(PBP), "pulled_et": PBP_PULLED_ET},
           **summarize(res, jobs, pbp)}
    out = ROOT / f"calibration/outputs/phase1_reconcile_{a.tag}_n{a.n}.json"
    out.write_text(json.dumps(doc, indent=1, default=float) + "\n")
    print(json.dumps({k: doc[k] for k in ("per_team_game", "fourth_down_by_band", "inside10", "clock_seconds_per_game")}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
