"""Scan/press/cap backtest, 2026 Wk3-8, walk-forward (analysis only; nothing live).
Arms: current gate proxy, scan-only, press-only (k=2 and k=3), scan+press (k=2/k=3), and PASS-VOLUME CAP on each.
Lines: stand-in floor(prior median)+0.5 (>=2 prior games) unless a real Week-8 book main line exists in runs/ manifests.
Models: sim_v6_backtest.csv RAW medians (calibration was fitted on wk4-7 so it is not applied -> no leakage); wk3/wk8 have no
model rows, so the 3-model check is only enforceable wk4-7 (main table) and wk3-8 is shown as a form-only variant."""
import glob, json, math, os, sys
import numpy as np, pandas as pd
sys.path.insert(0, "/workspace/nfl-database/tools"); sys.path.insert(0, "/workspace/nfl-database/backtests/wk8_proposals")
import scan_data, slate_scan as ss, press_tier as pt
from harness import roi, wilson
OUT = os.path.dirname(os.path.abspath(__file__)); ROOT = "/workspace/nfl-database"
MK = {"ryds": "rushyds", "rec": "rec", "recyds": "recyds", "pyds": "passyds"}

def real_lines():
    r = {}
    for f in glob.glob(f"{ROOT}/runs/2026-11-01_*/run_manifest.json"):
        for l in json.load(open(f)).get("legs", []):
            if l.get("market") not in MK.values(): continue
            pt_ = next((b["point"] for b in (l.get("fanduel"), l.get("pinnacle"), l.get("draftkings")) if isinstance(b, dict) and b.get("point") is not None), l.get("line"))
            r.setdefault((l.get("player"), l.get("market")), pt_)
    return r

def qb_legs(pg, g, w):
    rows = []
    for gid, gr in g[g.week == w].iterrows():
        for team, opp, sp in ((gr.home, gr.away, -gr.spread), (gr.away, gr.home, gr.spread)):
            p = pg[(pg.team == team) & (pg.week < w) & (pg.att > 0)]
            if p.empty: continue
            wks = sorted(p.week.unique())[-3:]; q = p[p.week.isin(wks)].groupby("pid").att.sum().idxmax()
            vals = p[p.pid == q].sort_values("week").pyds.tolist(); line = ss.standin_line(vals)
            if line is None: continue
            rows.append(dict(week=w, team=team, opp=opp, pid=q, name=p[p.pid == q].name.iloc[-1], role="QB1", pos="QB", market="pyds", line=line,
                             line_src="standin", trigger="", rule5_conflict=False, l4=vals[-4:], form=len(vals[-4:]) >= 3 and sum(x > line for x in vals[-4:]) >= 3,
                             game_id=gid, team_spread=float(sp) if pd.notna(sp) else 0.0, score=np.nan, s_allow=0, s_explosive=0, s_qb=0, s_script=0))
    return pd.DataFrame(rows)

def build():
    D = scan_data.load(); pg, g, ex = D
    sim = pd.read_csv(f"{ROOT}/tools/sim_v6_backtest.csv"); sim = sim.set_index(["gsis", "week", "market"])
    RL = real_lines(); allr = []
    for w in range(3, 9):
        c = ss.scan_week(w, D); q = qb_legs(pg, g, w)
        c = pd.concat([c, q], ignore_index=True)
        act = pg[pg.week == w].groupby("pid")[["ryds", "rec", "recyds", "pyds"]].sum()
        c = c[c.pid.isin(act.index)].copy()
        c["actual"] = [act.loc[p, m] for p, m in zip(c.pid, c.market)]
        if w == 8:
            for i, r in c.iterrows():
                k = (r["name"], MK[r.market])
                if k in RL and RL[k] is not None: c.at[i, "line"] = float(RL[k]); c.at[i, "line_src"] = "real_wk8_main"
            c["form"] = [len(l) >= 3 and sum(x > ln for x in l[-4:]) >= 3 for l, ln in zip(c.l4, c.line)]
        meds = []
        for p, m in zip(c.pid, c.market):
            try: s = sim.loc[(p, w, MK[m])]; s = s.iloc[0] if isinstance(s, pd.DataFrame) else s; meds.append([s.pred_mc, s.pred_bias, s.pred_gr])
            except KeyError: meds.append(None)
        c["meds"] = meds
        c["n_clear"] = [sum(x > l for x in ms) if ms else np.nan for ms, l in zip(c.meds, c.line)]
        # §7 vs a stand-in line equal to the player's own prior median is ~unsatisfiable (3 of 4 above one's own median),
        # so stand-in rows use a labelled PROXY: >=2 of last 4 over the line. Real-line rows keep the true 3-of-4.
        c["form"] = [(sum(x > ln for x in l[-4:]) >= 3 and len(l) >= 3) if src != "standin" else (sum(x > ln for x in l[-4:]) >= 2 and len(l) >= 2)
                     for l, ln, src in zip(c.l4, c.line, c.line_src)]
        c["hit"] = (c.actual > c.line).astype(int); allr.append(c)
    return pd.concat(allr, ignore_index=True)

def arms(df, model_weeks):
    d = df.copy(); hasm = d.n_clear.notna()
    need_m = d.week.isin(model_weeks)
    m3 = (d.n_clear == 3) | (~need_m); m2 = (d.n_clear >= 2) | (~need_m)
    if model_weeks: d = d[~need_m | hasm]  # wk with models: legs w/o a model row are not gradeable by the gate
    m3, m2 = m3.loc[d.index], m2.loc[d.index]
    core = d.role.isin(["RB1", "WR1", "WR2", "TE1", "QB1"]) & ~d.trigger.str.contains("starter_out", na=False)
    dogblock = (d.pos == "RB") & (d.market == "ryds") & (d.team_spread > 0)
    gate = d.form & m3 & ~dogblock
    cur = core & gate
    scanpool = (d.score > 0) | d.score.isna()  # QB legs unscored -> pass through
    scan = scanpool & gate & ~d.rule5_conflict  # rule 5 left untouched: backup-RB rush overs blocked
    ctx = (d.s_allow > 0) & (d.s_explosive > 0) & (d.s_script > 0) & (d.s_qb >= -0.1) & d.form
    press = {k: ctx & (((d.n_clear >= k) & d.week.isin(model_weeks)) if model_weeks else (d.n_clear >= k)) & ~dogblock for k in (2, 3)}
    A = {"current": cur, "scan_only": cur | scan}
    for k in (2, 3):
        A[f"press_only_k{k}"] = cur | (press[k] & core)
        A[f"scan+press_k{k}"] = cur | scan | (press[k] & (core | scanpool) & ~d.rule5_conflict)
    cap = (d.team_spread <= -6) & (((d.pos == "QB") & (d.market == "pyds")) | ((d.role == "WR2") & d.market.isin(["rec", "recyds"])))
    out = {}
    for k, v in A.items():
        out[k] = d[v]; out[k + "+cap"] = d[v & ~cap]
    return d, out, press, cap

def summ(x):
    n = len(x); k = int(x.hit.sum()); h = k / n if n else float("nan"); lo, hi = wilson(k, n)
    pw = x.groupby("week").hit.agg(["size", "mean"]); 
    return dict(n=n, hit=round(h, 3) if n else None, roi_110=round(roi(h, -110), 3) if n else None, roi_130=round(roi(h, -130), 3) if n else None,
                roi_160=round(roi(h, -160), 3) if n else None, ci90=f"{lo:.2f}-{hi:.2f}" if n else "", 
                weeks=" ".join(f"w{w}:{int(r['size'])}/{r['mean']:.2f}" for w, r in pw.iterrows()),
                wk_sd=round(float(pw["mean"].std()), 3) if len(pw) > 1 else None, real_lines=int((x.line_src != "standin").sum()))

if __name__ == "__main__":
    df = build(); df.drop(columns=["l4"]).to_csv(f"{OUT}/universe.csv", index=False)
    res = {}
    for lab, mw in (("wk4-7_models", [4, 5, 6, 7]), ("wk3-8_form_only", [])):
        d, A, press, cap = arms(df[df.week.between(4, 7)] if mw else df, mw)
        res[lab] = {k: summ(v) for k, v in A.items()}
        for k, v in A.items(): v.drop(columns=["l4"]).to_csv(f"{OUT}/{lab}__{k}.csv", index=False)
        for k in (2, 3):
            pz = d[press[k]]; res[lab][f"PRESS_tier_only_k{k}"] = summ(pz)
        base = A["scan+press_k2"]; killed = base[cap.loc[base.index]]
        res[lab]["cap_killed_on_scan+press_k2"] = dict(n=len(killed), winners_killed=int(killed.hit.sum()), losers_avoided=int((1 - killed.hit).sum()),
            legs=[f"w{r.week} {r['name']} {r.market} o{r.line} act {r.actual}" for _, r in killed.iterrows()])
    # RULE5 count (pre-gate pool and form-gated)
    r5 = df[df.rule5_conflict]
    res["rule5"] = dict(candidates=len(r5), hits=int(r5.hit.sum()), hits_with_form=int(r5[r5.form].hit.sum()), n_with_form=int(r5.form.sum()),
                        legs=[f"w{r.week} {r['name']} ({r.team}, {r.trigger}) o{r.line} act {r.actual} {'HIT' if r.hit else 'miss'}" for _, r in r5.iterrows()])
    w8 = df[df.week == 8]
    res["wk8_acceptance"] = {n: w8[(w8.name == n)][["role", "market", "line", "line_src", "trigger", "rank", "score", "actual", "hit"]].to_dict("records")
                             for n in ("Kenny Gainwell", "Braelon Allen", "Adonai Mitchell", "Chase Brown", "Emmett Johnson")}
    res["wk8_cap_sanity"] = w8[(w8.pos == "QB") | (w8.team.isin(["JAX", "LA"]) & (w8.role == "WR2"))][["name", "team", "team_spread", "market", "line", "line_src", "actual", "hit"]].query("team_spread <= -6").to_dict("records")
    json.dump(res, open(f"{OUT}/results.json", "w"), indent=1, default=str); print(json.dumps({k: v for k, v in res.items() if k.startswith("wk")}, indent=1, default=str)[:6000])
