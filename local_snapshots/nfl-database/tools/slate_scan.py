"""Phase-0 full-slate opportunity scan (Week 9+: R3 22% target-share WR/TE pool, trigger tgt_share22) (OPT-IN, analysis only; not wired into run_gate).
Candidates per team: RB1, RB2 (only on a trigger), WR1, WR2, TE1. DEPTH_RECEIVER rule (rules/rulebook.py) replaced the #3/#4 ban; WR3+ are not auto-listed here and
surface unless a WR1/WR2 is OUT and they are promoted into the WR2 slot. Every input for week w uses weeks < w
(plus the week-w inactive list, which is public ~90 min pregame). Backup-RB rushing overs are flagged
RULE5_CONFLICT (PHASE_SCRIPT 'what not to do' rule 5) and are never auto-cleared by this module.
Usage: python3 slate_scan.py 8 [out.csv]"""
import math, sys
import numpy as np, pandas as pd
MKTS = {"RB": ("ryds", "rec", "recyds"), "WR": ("recyds", "rec"), "TE": ("recyds", "rec")}
SHARE = 0.20  # an RB with >=20% of team carries in either of his last 2 games always gets a rush-yds candidate
FAV = -3.0  # team_spread <= -3 counts as favored for the RB2 trigger

def standin_line(vals):
    v = [float(x) for x in vals if x is not None and not (isinstance(x, float) and math.isnan(x))]
    return None if len(v) < 2 else math.floor(float(np.median(v))) + 0.5

def roles(pg, team, week, out=frozenset()):
    p = pg[(pg.team == team) & (pg.week < week)]
    wks = sorted(p.week.unique())[-3:]; r = p[p.week.isin(wks)]
    def rank(pos, col):
        s = r[r.pos == pos].groupby("pid")[col].sum().sort_values(ascending=False, kind="mergesort")
        return [x for x in s.index if s[x] > 0]
    rb, wr, te = rank("RB", "car"), rank("WR", "tgt"), rank("TE", "tgt")
    o = {}; promo = {}
    act = [x for x in rb if x not in out]
    if rb and rb[0] in out: promo["RB"] = True
    o["RB1"], o["RB2"] = (act + [None, None])[:2]
    wact = [x for x in wr if x not in out]
    if any(x in out for x in wr[:2]): promo["WR"] = True
    o["WR1"], o["WR2"] = (wact + [None, None])[:2]
    o["TE1"] = ([x for x in te if x not in out] + [None])[0]
    o["_promo"] = promo
    return o

def rb_share(pg, team, week, out=frozenset()):
    """{pid: max share of team carries over the team's last 2 games (weeks < week)} for active RBs."""
    p = pg[(pg.team == team) & (pg.week < week)]; wks = sorted(p.week.unique())[-2:]; o = {}
    for w in wks:
        x = p[p.week == w]; tot = x.car.fillna(0).sum()
        if tot <= 0: continue
        for _, r in x[x.pos == "RB"].iterrows():
            if r.pid not in out and r.car > 0: o[r.pid] = max(o.get(r.pid, 0.0), float(r.car) / tot)
    return o

POOL_FROM_WEEK = 9   # Rico R3 2026-11-02 05:01 ET (runs dated >= 2026-11-05 = Week 9)
TGT_SHARE = 0.22

def tgt_share(pg, team, week, qb_weeks=None):
    """{pid: (season share, last-3 current-QB share)} of team targets, weeks < week (nflverse pbp-derived player-games).
    qb_weeks: weeks the current QB started (default: all prior weeks)."""
    p = pg[(pg.team == team) & (pg.week < week)]
    if p.empty or "tgt" not in p: return {}
    tot = p.tgt.fillna(0).sum(); s = p.groupby("pid").tgt.sum() / tot if tot else p.groupby("pid").tgt.sum() * 0
    qw = sorted(w for w in p.week.unique() if qb_weeks is None or w in set(qb_weeks))[-3:]
    q = p[p.week.isin(qw)]; qt = q.tgt.fillna(0).sum(); s3 = q.groupby("pid").tgt.sum() / qt if qt else s * 0
    return {k: (float(s.get(k, 0)), float(s3.get(k, 0))) for k in set(s.index) | set(s3.index)}

def candidates(pg, team, week, ctx, out=frozenset(), depth_rb1=None):
    R = roles(pg, team, week, out); prior = pg[pg.week < week]; rows = []
    pool = {}
    if week >= POOL_FROM_WEEK:   # R3: WR/TE with >= 22% target share join the pool; WR3/4 must meet DEPTH_RECEIVER
        ts = tgt_share(pg, team, week, ctx.get("qb_weeks")); tp = prior[prior.team == team]
        posmap = tp.groupby("pid").pos.last() if "pos" in tp else {}
        wr_top = {R.get("WR1"), R.get("WR2")}
        for pid, (s, s3) in ts.items():
            if pid in out or max(s, s3) < TGT_SHARE: continue
            ps = posmap.get(pid)
            if ps == "WR" and pid not in wr_top: continue
            if ps not in ("WR", "TE"): continue
            pool[pid] = (ps, round(s, 3), round(s3, 3))
        n = 2
        for pid, (ps, _, _) in sorted(pool.items()):
            if pid not in R.values(): R[f"TE{n}"] = pid; n += 1
    # role flip: RB2 out-carried RB1 in the team's last game -> promote and flag
    flip = False
    if R.get("RB1") and R.get("RB2"):
        tp = prior[prior.team == team]; lw = tp.week.max(); lg = tp[tp.week == lw].groupby("pid").car.sum()
        if lg.get(R["RB2"], 0) > lg.get(R["RB1"], 0): R["RB1"], R["RB2"] = R["RB2"], R["RB1"]; flip = True
    if depth_rb1 is not None and depth_rb1 not in out and depth_rb1 != R.get("RB1"):
        if depth_rb1 == R.get("RB2"): R["RB1"], R["RB2"] = R["RB2"], R["RB1"]
    share = rb_share(pg, team, week, out); extra = [x for x in share if share[x] >= SHARE and x not in (R.get("RB1"), R.get("RB2"))]
    if depth_rb1 is not None and depth_rb1 not in out and depth_rb1 not in (R.get("RB1"), R.get("RB2")) and depth_rb1 not in extra: extra.insert(0, depth_rb1)
    for i, x in enumerate(extra): R[f"RB{3 + i}"] = x
    rb_roles = ("RB1", "RB2") + tuple(f"RB{3 + i}" for i in range(len(extra)))
    fav = ctx.get("team_spread", 0) <= FAV; wx = bool(ctx.get("wx")); dog = ctx.get("team_spread", 0) > 0
    for role in rb_roles + ("WR1", "WR2", "TE1") + tuple(k for k in R if k.startswith("TE") and k != "TE1"):
        pid = R.get(role)
        if pid is None: continue
        pos = role[:2]; mk = MKTS[pos]; trig = []
        if role == "RB1" and R["_promo"].get("RB"): trig.append("starter_out")
        if role == "RB1" and flip: trig.append("role_flip")
        if pos == "RB" and pid == depth_rb1: trig.append("depth_rb1")
        if pos == "RB" and role != "RB1" and share.get(pid, 0) >= SHARE: trig.append("carry_share")
        if role == "WR2" and R["_promo"].get("WR"): trig.append("starter_out")
        if pid in pool: trig.append("tgt_share22")
        if role == "RB2":
            if R["_promo"].get("RB"): trig.append("starter_out")
            if wx: trig.append("weather")
            if fav: trig.append("favored")
            if not trig and dog: trig, mk = ["dog_receiving"], ("rec", "recyds")
            if not trig: continue
        if pos == "RB" and role not in ("RB1", "RB2") and not trig: continue
        me = prior[prior.pid == pid].sort_values("week")
        for m in mk:
            vals = me[m].tolist(); line = standin_line(vals)
            if line is None: continue
            # starter-out promotion: RB1 promoted from RB2 gets the starter's prior line as the bar (harder, not easier)
            rows.append(dict(week=week, team=team, opp=ctx.get("opp"), pid=pid, name=me.name.iloc[-1] if "name" in me else pid,
                             role=role, pos=pos, market=m, line=line, line_src="standin", trigger=",".join(trig),
                             rule5_conflict=bool(pos == "RB" and role != "RB1" and m == "ryds"),
                             l4=vals[-4:], form=sum(x > line for x in vals[-4:]) >= 3 and len(vals[-4:]) >= 3))
    return pd.DataFrame(rows, columns=["week", "team", "opp", "pid", "name", "role", "pos", "market", "line", "line_src", "trigger", "rule5_conflict", "l4", "form"])

def _weights():
    import json, os
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scan_weights.json")
    return json.load(open(p)) if os.path.exists(p) else None

def score(c, pg, ex, g, week):
    """Higher = better over. Components (weeks < week only)."""
    if c.empty: return c
    prior = pg[pg.week < week]; c = c.copy()
    allow = prior.groupby(["opp", "pos"])[["ryds", "rec", "recyds"]].sum().div(prior.groupby("opp").game_id.nunique(), axis=0, level=0)
    lg = allow.groupby(level="pos").mean()
    exp = ex.merge(g[["week"]], left_on="game_id", right_index=True); exp = exp[exp.week < week].groupby("defteam")[["xr", "xu"]].mean()
    tp = prior.groupby(["team", "week"]).pyds.sum().groupby("team").mean(); lgp = tp.mean()
    adot = prior.groupby("pid").adot.mean() if "adot" in prior else pd.Series(dtype=float)
    out = []
    for _, r in c.iterrows():
        try: a = allow.loc[(r.opp, r.pos), r.market] / lg.loc[r.pos, r.market] - 1
        except KeyError: a = 0.0
        a = 0.0 if pd.isna(a) else float(a)
        rush = r.market == "ryds"
        xx = exp.loc[r.opp, "xu" if rush else "xr"] / exp["xu" if rush else "xr"].mean() - 1 if r.opp in exp.index else 0.0
        qb = 0.0 if rush else tp.get(r.team, lgp) / lgp - 1
        gi = g[(g.week == week) & ((g.home == r.team) | (g.away == r.team))]
        sp = (-gi.spread.iat[0] if gi.home.iat[0] == r.team else gi.spread.iat[0]) if len(gi) else 0.0
        tot = gi.total.iat[0] if len(gi) and pd.notna(gi.total.iat[0]) else 44.0; wxf = bool(gi.wx.iat[0]) if len(gi) else False
        script = (-sp / 7 if rush else sp / 14) + (tot / 44 - 1)
        w = (0.3 if rush else -0.2) if wxf else 0.0
        promo = 0.5 if "starter_out" in r.trigger else 0.0
        rb2 = 0.2 if r.role == "RB2" and ("weather" in r.trigger or "favored" in r.trigger) else 0.0
        deep = 0.3 if r.pos == "WR" and adot.get(r.pid, 0) >= 12 and xx > 0 else 0.0
        rep = 0.2 if sum(x > r.line for x in r.l4[-2:]) == 2 else 0.0
        out.append(dict(s_allow=a, s_explosive=xx, s_qb=qb, s_script=script, s_weather=w, s_promo=promo, s_rb2=rb2, s_deep=deep, s_repeat=rep))
    s = pd.DataFrame(out, index=c.index); c = pd.concat([c, s], axis=1)
    c["score"] = s.sum(axis=1).round(4)
    W = _weights()
    if W and week >= W["valid_from_week"]:  # walk-forward fitted weights (fit on weeks < valid_from_week only)
        w = W["weights_fit_wk3_7"]; lin = W["intercept"] + sum(s[k] * w[k] for k in s.columns if k in w)
        for m in ("ryds", "rec", "recyds"): lin = lin + (c.market == m).astype(float) * w.get("m_" + m, 0.0)
        c["score_equal"] = c["score"]; c["score"] = lin.round(4)
    c = c.sort_values(["score", "name", "market"], ascending=[False, True, True]).reset_index(drop=True); c["rank"] = c.index + 1
    return c

def week_out(pg, team, week):
    """Prior (last-3-game) skill players absent from the week-w box: proxy for the inactive list (public ~90 min
    pregame). Caveat: a player active but with zero touches also looks absent."""
    here = set(pg[(pg.team == team) & (pg.week == week)].pid)
    if not here: return set()
    p = pg[(pg.team == team) & (pg.week < week)]; wks = sorted(p.week.unique())[-3:]
    return set(p[p.week.isin(wks) & p.pos.isin(["RB", "WR", "TE"])].pid) - here

def scan_week(week, data=None):
    import scan_data
    pg, g, ex = data or scan_data.load()
    rows = []
    for gid, gr in g[g.week == week].iterrows():
        for team, opp, sp in ((gr.home, gr.away, -gr.spread), (gr.away, gr.home, gr.spread)):
            ctx = dict(wx=bool(gr.wx), team_spread=float(sp) if pd.notna(sp) else 0.0, total=gr.total, opp=opp)
            c = candidates(pg, team, week, ctx, out=week_out(pg, team, week))
            if not c.empty: c["game_id"] = gid; c["team_spread"] = ctx["team_spread"]; rows.append(c)
    return score(pd.concat(rows, ignore_index=True), pg, ex, g, week)

if __name__ == "__main__":
    w = int(sys.argv[1]); c = scan_week(w); p = sys.argv[2] if len(sys.argv) > 2 else f"slate_scan_wk{w}.csv"
    c.drop(columns=["l4"]).to_csv(p, index=False); print(f"{len(c)} candidates -> {p}")
