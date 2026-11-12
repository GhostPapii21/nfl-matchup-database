import sys; sys.path.insert(0, "/workspace/nfl-database/tools")
"""Week-8 proposal backtest (analysis only; does not touch run_gate/sim_v6/PHASE_SCRIPT).
Walk-forward: every input for week w uses only weeks < w. Lines are PROXY lines (no historical
prop lines stored for wk1-7): floor(prior-game median)+0.5, min 2 prior games."""
import math, os, json
import numpy as np, pandas as pd
ROOT = "/workspace/nfl-database"
PBP = f"{ROOT}/runs/2026-11-01_shared_src/play_by_play_2026.parquet"
ROS = f"{ROOT}/fixes/src/roster_weekly_2026.parquet"
SIM = f"{ROOT}/tools/sim_v6_backtest.csv"
CAL = f"{ROOT}/tools/sim_v6_calib.json"
OUT = os.path.dirname(os.path.abspath(__file__))
TAU_CURRENT = 0.3923

def roi(h, odds):
    pay = 100/abs(odds) if odds < 0 else odds/100
    return h*pay - (1-h)
def proxy_line(vals):
    v = [x for x in vals if x is not None and not (isinstance(x, float) and math.isnan(x))]
    if len(v) < 2: return None
    return math.floor(float(np.median(v))) + 0.5
def prior_vals(pg, pid, week, col):
    return pg[(pg.pid == pid) & (pg.week < week)].sort_values("week")[col].tolist()
def clears(meds, line, need=3, side="over"):
    return sum((m > line) if side == "over" else (m < line) for m in meds) >= need
def wilson(k, n, z=1.645):
    if n == 0: return (float("nan"),)*2
    p = k/n; d = 1+z*z/n; c = p + z*z/(2*n); r = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))
    return ((c-r)/d, (c+r)/d)
def summarize(hits):
    n = len(hits); k = int(sum(hits)); h = k/n if n else float("nan"); lo, hi = wilson(k, n)
    return {"n": n, "hit": h, "roi_110": roi(h,-110) if n else None, "roi_130": roi(h,-130) if n else None,
            "roi_160": roi(h,-160) if n else None, "ci_lo": lo, "ci_hi": hi, "small_sample": n < 50}

def load():
    d = pd.read_parquet(PBP); d = d[(d.season_type == "REG") & (d.two_point_attempt != 1)]
    ros = pd.read_parquet(ROS)[["gsis_id", "position"]].dropna().drop_duplicates("gsis_id").set_index("gsis_id").position
    g = d.groupby("game_id").agg(week=("week","first"), home=("home_team","first"), away=("away_team","first"),
                                 spread=("spread_line","first"), weather=("weather","first"), roof=("roof","first"), wind=("wind","first"))
    wxs = g.weather.fillna("").str.lower()
    g["wx"] = (g.roof.isin(["outdoors","open"])) & (wxs.str.contains("rain|shower|storm|snow") | (__import__("scan_data")._wind_mph(g.wind, g.weather) >= 15))
    ru = d[(d.rush_attempt == 1) & (d.qb_kneel != 1) & d.rusher_player_id.notna()].groupby(["game_id","posteam","rusher_player_id"]).agg(car=("rush_attempt","sum"), ryds=("rushing_yards","sum")).reset_index().rename(columns={"rusher_player_id":"pid"})
    rc = d[(d.pass_attempt == 1) & d.receiver_player_id.notna()].groupby(["game_id","posteam","receiver_player_id"]).agg(tgt=("pass_attempt","sum"), rec=("complete_pass","sum"), recyds=("receiving_yards","sum")).reset_index().rename(columns={"receiver_player_id":"pid"})
    pg = ru.merge(rc, on=["game_id","posteam","pid"], how="outer").fillna({"car":0,"ryds":0,"tgt":0,"rec":0,"recyds":0})
    pg = pg.rename(columns={"posteam":"team"}).merge(g, left_on="game_id", right_index=True)
    pg["pos"] = pg.pid.map(ros).fillna("UNK")
    pg["opp"] = np.where(pg.team == pg.home, pg.away, pg.home)
    # team spread: nflverse spread_line >0 = home favored
    pg["team_spread"] = np.where(pg.team == pg.home, -pg.spread, pg.spread)  # negative = favored
    pg["dog"] = pg.team_spread > 0
    return d, g, pg

def rb_roles(pg, team, week):
    pr = pg[(pg.team == team) & (pg.week < week) & (pg.pos == "RB")]
    s = pr.groupby("pid").agg(car=("car","sum"), gp=("game_id","nunique"))
    s = s[s.gp >= 2].sort_values("car", ascending=False)
    return list(s.index[:2])

def leg_rows(pg, pid, week, col, actual):
    line = proxy_line(prior_vals(pg, pid, week, col))
    if line is None: return None
    return line, int(actual > line)

def form_ok(vals, line):  # §7: >=3 of last 4 over line
    v = vals[-4:]; return len(v) >= 3 and sum(x > line for x in v) >= 3

# ---------- P1 ----------
def p1(pg):
    rows = []
    for (gid, team), grp in pg.groupby(["game_id","team"]):
        wk = grp.week.iat[0]
        if wk < 3: continue
        roles = rb_roles(pg, team, wk)
        if len(roles) < 2: continue
        lead, rb2 = roles
        lead_row = grp[grp.pid == lead]
        promo = lead_row.empty or lead_row.car.iat[0] == 0
        wx = bool(grp.wx.iat[0])
        for role, pid in (("lead", lead), ("rb2", rb2)):
            r = grp[grp.pid == pid]
            if r.empty: continue
            prev = prior_vals(pg, pid, wk, "ryds"); line = proxy_line(prev)
            if line is None: continue
            rows.append(dict(game_id=gid, week=wk, team=team, pid=pid, role=role, wx=wx, promo=bool(promo),
                             line=line, actual=r.ryds.iat[0], hit=int(r.ryds.iat[0] > line), form=form_ok(prev, line)))
    df = pd.DataFrame(rows)
    df["current"] = (df.role == "lead") & df.form              # RB1 default + §7 form gate
    trig = df.wx | df.promo
    df["proposal"] = df.current | (trig & ((df.role == "lead") | (df.role == "rb2")) & (df.form | (df.role == "rb2") & df.promo))
    return df

# ---------- P2 / P3 (3-model medians from sim_v6_backtest, wk4-7) ----------
def sim_rows(pg):
    s = pd.read_csv(SIM); cal = json.load(open(CAL))["multipliers"]
    for mo, col in (("mc","pred_mc"),("bias","pred_bias"),("gr","pred_gr")):
        if mo in cal:
            s[col+"_c"] = [r[col]*cal[mo].get(r.market,{}).get("M",1.0) for _, r in s.iterrows()]
        else: s[col+"_c"] = s[col]
    colmap = {"rushyds":"ryds","rec":"rec","recyds":"recyds"}
    out = []
    pgi = pg.set_index(["pid","week"])
    for _, r in s[s.market.isin(colmap)].iterrows():
        prev = prior_vals(pg, r.gsis, r.week, colmap[r.market]); line = proxy_line(prev)
        if line is None: continue
        try: x = pgi.loc[(r.gsis, r.week)]; x = x.iloc[0] if isinstance(x, pd.DataFrame) else x
        except KeyError: continue
        out.append(dict(week=r.week, pid=r.gsis, market=r.market, pos=x.pos, dog=bool(x.dog), line=line, actual=r.actual,
                        hit=int(r.actual > line), meds=[r.pred_mc_c, r.pred_bias_c, r.pred_gr_c]))
    return pd.DataFrame(out)

def p2(sr):
    df = sr[(sr.market == "rushyds") & (sr.pos == "RB")].copy()
    df["n_clear"] = df.meds.apply(lambda m: sum(x > 0 for x in m) and 0)  # placeholder overwritten below
    df["n_clear"] = [sum(m > l for m in ms) for ms, l in zip(df.meds, df.line)]
    df["current"] = (df.n_clear == 3) & ~df.dog                # all 3 clear + underdog block
    df["proposal"] = ((df.n_clear >= 2) & ~df.dog) | ((df.n_clear == 3) & df.dog)
    return df

def p_over(meds, line, sd):
    from scipy.stats import norm
    return float(np.mean([1 - norm.cdf((line - m)/sd) for m in meds]))

def p3(sr):
    """Per-market shrink fitted walk-forward by calibration (Brier) vs the global 0.7; bet when p' > 0.5238 (-110 BE)."""
    rows = []
    for mkt in ("rushyds", "rec", "recyds"):
        df = sr[sr.market == mkt].copy()
        for wk in sorted(df.week.unique()):
            tr, te = df[df.week < wk], df[df.week == wk]
            if len(tr) < 20:
                sd = df[df.week <= wk].actual.std()*0.0 + None if False else None
            # residual SD from prior weeks only (or the first test week's own prior pbp spread fallback)
            base = tr if len(tr) >= 20 else None
            sd = float(np.std([a - np.mean(m) for a, m in zip(base.actual, base.meds)])) if base is not None else None
            if sd is None: continue
            ptr = np.array([p_over(m, l, sd) for m, l in zip(tr.meds, tr.line)])
            best = min(np.arange(0.0, 1.51, 0.05), key=lambda s: np.mean((0.5 + s*(ptr-0.5) - tr.hit.values)**2))
            # RB receiving cap: fitted ratio actual/mean(pred) for RB rows prior weeks
            capr = None
            if mkt in ("rec", "recyds"):
                rbt = tr[tr.pos == "RB"]
                if len(rbt) >= 10: capr = min(1.0, rbt.actual.sum()/sum(np.mean(m) for m in rbt.meds))
            for _, r in te.iterrows():
                meds = r.meds
                if capr is not None and r.pos == "RB": meds_c = [m*capr for m in meds]
                else: meds_c = meds
                p = p_over(meds, r.line, sd); pc = p_over(meds_c, r.line, sd)
                rows.append(dict(week=wk, market=mkt, pid=r.pid, pos=r.pos, line=r.line, actual=r.actual, hit=r.hit,
                                 p=p, s_fit=float(best), cap=capr, current=(0.5+0.7*(p-0.5)) > 0.5238,
                                 proposal=(0.5+best*(pc-0.5)) > 0.5238))
    return pd.DataFrame(rows)

# ---------- P4 ----------
def p4(pg, taus=(TAU_CURRENT, 0.75)):
    rows = []
    for (gid, team), grp in pg.groupby(["game_id","team"]):
        wk = grp.week.iat[0]
        if wk < 3: continue
        roles = rb_roles(pg, team, wk)
        if len(roles) < 2: continue
        lead, rb2 = roles
        if not grp[(grp.pid == lead) & (grp.car > 0)].empty: continue
        r = grp[grp.pid == rb2]
        if r.empty: continue
        pr = pg[(pg.team == team) & (pg.week < wk)]
        tm = pr[pr.pos == "RB"].groupby("game_id").car.sum().mean()
        sh = lambda p: pr[pr.pid == p].car.sum() / max(1, pr[pr.pos == "RB"].car.sum())
        prev = prior_vals(pg, rb2, wk, "ryds"); line = proxy_line(prev)
        if line is None: continue
        ypc = max(2.5, pr[pr.pid == rb2].ryds.sum()/max(1, pr[pr.pid == rb2].car.sum()))
        d = dict(game_id=gid, week=wk, team=team, pid=rb2, line=line, actual_car=r.car.iat[0], actual=r.ryds.iat[0], hit=int(r.ryds.iat[0] > line))
        for t in taus:
            car = tm*(sh(rb2) + t*sh(lead)); d[f"proj_car_{t}"] = car; d[f"proj_yds_{t}"] = car*ypc
        rows.append(d)
    df = pd.DataFrame(rows)
    df["current"] = df[f"proj_yds_{TAU_CURRENT}"] >= 1.10*df.line
    df["proposal"] = df["proj_yds_0.75"] >= 1.10*df.line
    return df

# ---------- P5 ----------
def p5(pg):
    rows = []
    for (gid, team), grp in pg.groupby(["game_id","team"]):
        wk = grp.week.iat[0]
        if wk < 3: continue
        pr = pg[(pg.team == team) & (pg.week < wk)]
        wr = pr[pr.pos == "WR"].groupby("pid").tgt.sum().sort_values(ascending=False)
        te = pr[pr.pos == "TE"].groupby("pid").tgt.sum().sort_values(ascending=False)
        opp = grp.opp.iat[0]
        # weak defender proxy: opponent's prior yards/target allowed to WR3+TE-type targets (team level; no per-defender history)
        allowed = pg[(pg.opp == opp) & (pg.week < wk) & pg.pos.isin(["WR","TE"])]
        lg = pg[(pg.week < wk) & pg.pos.isin(["WR","TE"])]
        if allowed.tgt.sum() < 30: continue
        ypt = allowed.recyds.sum()/allowed.tgt.sum(); lypt = lg.recyds.sum()/lg.tgt.sum()
        weak = ypt >= 1.10*lypt
        for role, pid in (("WR3", wr.index[2] if len(wr) > 2 else None), ("TE1", te.index[0] if len(te) else None)):
            if pid is None: continue
            r = grp[grp.pid == pid]
            if r.empty: continue
            for col in ("rec", "recyds"):
                line = proxy_line(prior_vals(pg, pid, wk, col))
                if line is None: continue
                rows.append(dict(game_id=gid, week=wk, team=team, opp=opp, pid=pid, role=role, market=col, weak=bool(weak),
                                 opp_ypt=ypt, lg_ypt=lypt, line=line, actual=r[col].iat[0], hit=int(r[col].iat[0] > line)))
    df = pd.DataFrame(rows)
    df["current"] = False   # standing ban on #3/#4 receivers (TE1 also not in default pool)
    df["proposal"] = df.weak
    return df

def compare(df):
    cur, pro = df[df.current], df[df.proposal]
    added, removed = df[df.proposal & ~df.current], df[df.current & ~df.proposal]
    return {"current": summarize(cur.hit.tolist()), "proposal": summarize(pro.hit.tolist()),
            "added": summarize(added.hit.tolist()), "removed": summarize(removed.hit.tolist()),
            "universe": summarize(df.hit.tolist())}

def main():
    d, g, pg = load()
    sr = sim_rows(pg)
    res = {}
    for name, df in (("P1_carries_leader_rb2", p1(pg)), ("P2_two_of_three_medians", p2(sr)),
                     ("P3_per_market_shrink_rbcap", p3(sr)), ("P4_injury_promotion", p4(pg)), ("P5_wr3_te_weak_def", p5(pg))):
        df.drop(columns=[c for c in ("meds",) if c in df.columns]).to_csv(f"{OUT}/{name}.csv", index=False)
        res[name] = compare(df)
        if name.startswith("P3"): res[name]["s_fit_by_market_week"] = df.groupby(["market","week"]).s_fit.first().to_dict().__repr__()
    json.dump(res, open(f"{OUT}/results.json","w"), indent=1, default=str)
    return res

if __name__ == "__main__":
    r = main()
    for k, v in r.items():
        print(k); [print("  ", s, {kk: (round(vv,3) if isinstance(vv,float) else vv) for kk, vv in v[s].items()}) for s in ("universe","current","proposal","added","removed")]
