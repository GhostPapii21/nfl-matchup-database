"""v2 INFERRED coverage-window ("zone of responsibility") credit. Research only.

    python3 data/coverage/defender_profiles_2026/coverage_sim.py --raw <dir>

Rico's rule (Nov 27): whoever's window the ball was caught in gave up the play. If a receiver catches it near safety X for
30 yards, X allowed the 30. Tackler evidence then raises or splits the credit.

How:
 1. Shell mix per defense: StatRankings Cover 0/1/2/2-man/3/4/6 rates (public top-25 articles, through 2026-11-20). A team
    missing from a top-25 list gets 0.8 x the lowest listed value for that shell (IMPUTED, flagged). Normalised to 1.
 2. Roles per game from that game's snap counts: the two most-used CBs are the outside corners, put on the offense's left
    or right by their own side history; 3rd CB (or a low-depth DB/S) = nickel; two most-used S (deeper one = FS,
    other = SS; the more-left one takes the left half in two-high looks); two most-used LBs = MLB and LB2.
    Side/depth history = verified PBU/INT/DPI zones + tackle-after-catch zones.
 3. Field grid (offense's view): depth bands behind LOS / 0-9 / 10-19 / 20+ (air yards at the catch point) x width
    L / L-slot / M / R-slot / R. pbp gives only left/middle/right, so outside vs slot is sampled (WR 60% outside,
    TE 15%, RB 30%; middle throws 70% M, 15% each slot).
 4. Simulation: for each target, draw N=10,000 (shell, width, strength side, middle split) from the mix and read who owns
    that window (zone shells) or who is matched on that receiver (man: outside WR -> that side's CB, slot WR -> nickel,
    TE -> SS, RB -> MLB; Cover 1 deep middle -> FS). Ownership probability per defender = share of draws.
 5. Tackler blend (completions): YAC < 10 and the tackler is one of the role players -> credit = 0.7 window + 0.3 tackler.
    YAC >= 10 -> credit = window owner only; the tackler is logged as 'help' (he was the pursuit, not the beaten man).
Everything written is INFERRED.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

import build as B

HERE = Path(__file__).resolve().parent
SHELLS = ["C0", "C1", "C2", "C2M", "C3", "C4", "C6"]
COLS = ["L", "LS", "M", "RS", "R"]
BANDS = ["behind", "0-9", "10-19", "20+"]
ROLES = ["CB_L", "CB_R", "NB", "FS", "SS", "S_L", "S_R", "MLB", "LB2"]
N_SIM = 10_000
SR_FULL = {v: k for k, v in B.SHARP_NAME.items()}


def band_of(ay):
    return 0 if ay < 0 else 1 if ay < 10 else 2 if ay < 20 else 3


def shell_mix(raw: Path):
    d = pd.read_csv(raw / "sr_cover_types_2026-11-22.csv")
    d = d[d.source_url.str.contains("statrankings", na=False)].copy()
    d["team"] = d.team.map(B.SHARP_NAME)
    cols = ["cover0_pct", "cover1_pct", "cover2_pct", "cover2m_pct", "cover3_pct", "cover4_pct", "cover6_pct"]
    imputed = d[cols].isna()
    for c in cols:
        d[c] = d[c].fillna(0.8 * d[c].min())
    m = d.set_index("team")[cols].to_numpy()
    m = m / m.sum(axis=1, keepdims=True)
    mix = {tm: m[i] for i, tm in enumerate(d.team)}
    imp = {tm: [SHELLS[j] for j in range(len(cols)) if imputed.iloc[i, j]] for i, tm in enumerate(d.team)}
    return mix, imp


def tendencies(links: pd.DataFrame):
    l = links[links.zone.isin([f"{a}_{b}" for a in ("short", "deep") for b in ("left", "middle", "right")])]
    g = l.groupby("def_id").zone.agg(list)
    out = {}
    for d, zs in g.items():
        zs = pd.Series(zs)
        left, right = zs.str.endswith("left").sum(), zs.str.endswith("right").sum()
        out[d] = {"left_share": (left + 1) / (left + right + 2), "deep_share": (zs.str.startswith("deep").sum() + 1) / (len(zs) + 3), "n": len(zs)}
    return out


def assign_roles(cands: pd.DataFrame, tend: dict):
    """cands: gsis, grp (CB/S/DB/LB), pct. Returns role -> gsis."""
    td = lambda g, k: tend.get(g, {}).get(k, 0.5 if k == "left_share" else 0.3)
    c = cands.copy()
    c.loc[c.grp == "DB", "grp"] = np.where(c.loc[c.grp == "DB", "gsis"].map(lambda g: td(g, "deep_share")) > 0.4, "S", "CB")
    cbs = c[c.grp == "CB"].sort_values("pct", ascending=False)
    ss = c[c.grp == "S"].sort_values("pct", ascending=False)
    lbs = c[c.grp == "LB"].sort_values("pct", ascending=False)
    r = {}
    if len(cbs) >= 2:
        a, b = cbs.gsis.iloc[0], cbs.gsis.iloc[1]
        r["CB_L"], r["CB_R"] = (a, b) if td(a, "left_share") >= td(b, "left_share") else (b, a)
    elif len(cbs) == 1:
        r["CB_L"] = r["CB_R"] = cbs.gsis.iloc[0]
    if len(cbs) >= 3 and cbs.pct.iloc[2] >= 0.35:
        r["NB"] = cbs.gsis.iloc[2]
    if len(ss) >= 2:
        a, b = ss.gsis.iloc[0], ss.gsis.iloc[1]
        r["FS"], r["SS"] = (a, b) if td(a, "deep_share") >= td(b, "deep_share") else (b, a)
        r["S_L"], r["S_R"] = (a, b) if td(a, "left_share") >= td(b, "left_share") else (b, a)
    elif len(ss) == 1:
        r["FS"] = r["SS"] = r["S_L"] = r["S_R"] = ss.gsis.iloc[0]
    if "NB" not in r:
        r["NB"] = r.get("SS")
    if len(lbs):
        r["MLB"] = lbs.gsis.iloc[0]
        r["LB2"] = lbs.gsis.iloc[1] if len(lbs) > 1 else lbs.gsis.iloc[0]
    for k in ROLES:  # fallbacks
        if r.get(k) is None:
            r[k] = r.get({"NB": "SS", "SS": "FS", "FS": "SS", "S_L": "FS", "S_R": "SS", "LB2": "MLB", "MLB": "LB2", "CB_L": "CB_R", "CB_R": "CB_L"}[k])
    return r


def owner_role(shell, band, col, rpos, strong_left, coin):
    """Vectorised: arrays of equal length -> array of role names (offense's view)."""
    n = len(shell)
    out = np.empty(n, dtype=object)
    L, LS, M, RS, R = 0, 1, 2, 3, 4
    deep, inter, short = band == 3, band == 2, band <= 1
    # man defender on this receiver's alignment
    man = np.where(rpos == "TE", "SS", np.where(rpos == "RB", "MLB",
                   np.where(col == L, "CB_L", np.where(col == R, "CB_R", "NB"))))
    side_s = np.where(col <= LS, "S_L", np.where(col >= RS, "S_R", np.where(coin, "S_L", "S_R")))
    hook = np.where(col == M, "MLB", np.where((col == LS) == strong_left, "LB2", "MLB"))
    flat = np.where((col == L) == strong_left, "SS", "NB")
    for s in SHELLS:
        k = shell == s
        if not k.any():
            continue
        if s == "C0":
            out[k] = man[k]
        elif s == "C1":
            out[k] = np.where(deep[k] & (col[k] == M), "FS", man[k])
        elif s == "C2M":
            out[k] = np.where(deep[k], side_s[k], man[k])
        elif s == "C3":
            o = np.where(col[k] <= LS, "CB_L", np.where(col[k] >= RS, "CB_R", "FS"))
            i = np.where(col[k] == L, "CB_L", np.where(col[k] == R, "CB_R", np.where(col[k] == M, "MLB", np.where(col[k] == LS, np.where(strong_left[k], "SS", "NB"), np.where(strong_left[k], "NB", "SS")))))
            sh = np.where(col[k] == L, np.where(strong_left[k], "SS", "NB"), np.where(col[k] == R, np.where(strong_left[k], "NB", "SS"), hook[k]))
            out[k] = np.where(deep[k], o, np.where(inter[k], i, sh))
        elif s == "C2":
            o = side_s[k]
            i = np.where(col[k] == L, np.where(coin[k], "S_L", "CB_L"), np.where(col[k] == R, np.where(coin[k], "S_R", "CB_R"), np.where(col[k] == M, "MLB", np.where(col[k] == LS, np.where(strong_left[k], "NB", "LB2"), np.where(strong_left[k], "LB2", "NB")))))
            sh = np.where(col[k] == L, "CB_L", np.where(col[k] == R, "CB_R", np.where(col[k] == M, "MLB", np.where((col[k] == LS) == strong_left[k], "NB", "LB2"))))
            out[k] = np.where(deep[k], o, np.where(inter[k], i, sh))
        elif s in ("C4", "C6"):
            q = np.where(col[k] == L, "CB_L", np.where(col[k] == R, "CB_R", side_s[k]))
            c2 = side_s[k]
            if s == "C6":  # quarters to one half, cover 2 to the other (half chosen by strong side)
                quarter_half = np.where(strong_left[k], col[k] <= M, col[k] >= M)
                deep_o = np.where(quarter_half, q, c2)
            else:
                deep_o = q
            sh = np.where(col[k] == L, flat[k], np.where(col[k] == R, np.where(strong_left[k], "NB", "SS"), hook[k]))
            out[k] = np.where(deep[k] | inter[k], deep_o, sh)
    return out


def width_probs(loc, rpos):
    p_out = {"WR": 0.6, "TE": 0.15, "RB": 0.3}.get(rpos, 0.4)
    if loc == "left":
        return np.array([p_out, 1 - p_out, 0, 0, 0])
    if loc == "right":
        return np.array([0, 0, 0, 1 - p_out, p_out])
    return np.array([0, 0.15, 0.7, 0.15, 0])


def simulate(row, mix, roles, rng, n=N_SIM):
    shell = rng.choice(SHELLS, size=n, p=mix)
    col = rng.choice(5, size=n, p=width_probs(row.pass_location, row.rpos))
    band = np.full(n, band_of(row.air_yards))
    sl = rng.random(n) < 0.5
    coin = rng.random(n) < 0.5
    rp = np.full(n, row.rpos if row.rpos in ("WR", "TE", "RB") else "WR", dtype=object)
    own = owner_role(shell, band, col, rp, sl, coin)
    ids = pd.Series(own).map(roles)
    vc = ids.value_counts(normalize=True)
    rc = pd.Series(own).value_counts(normalize=True)
    cell = pd.Series([COLS[c] for c in col]).value_counts(normalize=True)
    return vc, rc, cell.idxmax()


def prepare(raw: Path):
    p, a, s, ro, ngs, ftn = B.load(raw, None)
    cover_pos, off_pos, names, pfr2gsis, gsis2pfr, pos_snap = B.id_maps(ro, s)
    t = B.target_plays(p, off_pos)
    links = B.defender_links(p, t, off_pos)
    s = s[s.defense_snaps > 0].copy()
    s["gsis"] = s.pfr_player_id.map(pfr2gsis)
    s["grp"] = s.position.map(B.COVER_POS)
    s = s.dropna(subset=["gsis", "grp"])
    s = s[s.grp.isin(["CB", "S", "DB", "LB"])]
    # snap counts list some backs only as "DB": use the roster depth-chart position (CB vs FS/SS) when it has one
    dc = ro.dropna(subset=["gsis_id"]).sort_values("week").groupby("gsis_id").depth_chart_position.last().map(B.COVER_POS)
    m = s.grp == "DB"
    s.loc[m, "grp"] = s.loc[m, "gsis"].map(dc).where(lambda x: x.isin(["CB", "S"]), "DB")
    s["team"] = s.team.replace({"LAR": "LA"})
    return p, t, links, s, names, off_pos


def run(raw: Path, tend_links_filter=None, only=None, seed=7):
    p, t, links, s, names, off_pos = prepare(raw)
    mix, imp = shell_mix(raw)
    tl = links if tend_links_filter is None else tend_links_filter(links)
    tend = tendencies(tl)
    rng = np.random.default_rng(seed)
    snaps_g = {k: v for k, v in s.groupby(["game_id", "team"])}
    rows = []
    tt = t[t.air_yards.notna() & t.pass_location.notna()]
    if only is not None:
        tt = tt[only(tt)]
    roles_by_game = {}
    for (g, tm), plays in tt.groupby(["game_id", "defteam"]):
        c = snaps_g.get((g, tm))
        if c is None or tm not in mix:
            continue
        c = c.groupby("gsis").agg(grp=("grp", "first"), pct=("defense_pct", "max")).reset_index()
        roles = assign_roles(c, tend)
        roles_by_game[(g, tm)] = roles
        for _, x in plays.iterrows():
            vc, rc, cell = simulate(x, mix[tm], roles, rng)
            rows.append((g, tm, x.play_id, vc, rc, cell))
    return t, links, names, rows, roles_by_game, mix, imp, s


def role_class(role):
    return {"CB_L": "CB-left", "CB_R": "CB-right", "NB": "nickel/slot", "FS": "S", "SS": "S", "S_L": "S", "S_R": "S", "MLB": "LB", "LB2": "LB"}.get(role, "other")


def pos_class(role):
    return {"CB_L": "CB", "CB_R": "CB", "NB": "CB", "FS": "S", "SS": "S", "S_L": "S", "S_R": "S", "MLB": "LB", "LB2": "LB"}.get(role, "other")


# ---------------------------------------------------------------- production outputs, charts, upcoming view
XPOS = {"L": -20.0, "LS": -9.0, "M": 0.0, "RS": 9.0, "R": 20.0}


def tier(p1):
    return "high" if p1 >= 0.6 else "med" if p1 >= 0.4 else "low"


def credit_table(t, rows, roles_by_game, names):
    tt = t.set_index(["game_id", "play_id"])
    out = []
    for g, tm, pl, vc, rc, cell in rows:
        x = tt.loc[(g, pl)]
        roles = roles_by_game[(g, tm)]
        win = vc.copy()
        tk = next((x[c] for c in ("solo_tackle_1_player_id", "tackle_with_assist_1_player_id", "assist_tackle_1_player_id") if pd.notna(x[c])), None)
        yac = x.yards_after_catch if pd.notna(x.yards_after_catch) else 0
        cmp_ = x.cmp == 1
        help_ = None
        credit = win
        if cmp_ and tk is not None and tk in set(roles.values()):
            if yac < 10:
                credit = 0.7 * win.add(pd.Series({tk: 0.0}), fill_value=0)
                credit[tk] = credit.get(tk, 0) + 0.3
            elif tk != win.index[0]:
                help_ = tk
        credit = credit.sort_values(ascending=False)
        role_of = {}
        for r, d in roles.items():
            role_of.setdefault(d, r)
        d1 = credit.index[0]
        d2 = credit.index[1] if len(credit) > 1 else None
        out.append({"week": int(x.week), "game_id": g, "play_id": pl, "defteam": tm, "posteam": x.posteam, "qtr": x.qtr, "time": x.time,
                    "receiver": x.receiver_player_name, "rpos": x.rpos, "pass_location": x.pass_location, "air_yards": x.air_yards,
                    "yac": yac, "yards": x.yds, "result": "INT" if x.int else ("TD" if x.td else ("complete" if cmp_ else "incomplete")),
                    "explosive20": bool(cmp_ and x.yds >= 20), "catch_band": BANDS[band_of(x.air_yards)], "likely_width": cell,
                    "window_owner": names.get(win.index[0], win.index[0]), "window_owner_role": role_of.get(win.index[0]),
                    "window_prob": round(float(win.iloc[0]), 3),
                    "window_runner_up": names.get(win.index[1], win.index[1]) if len(win) > 1 else None,
                    "window_runner_up_prob": round(float(win.iloc[1]), 3) if len(win) > 1 else None,
                    "tackler": names.get(tk, tk) if tk else None, "help_defender": names.get(help_, help_) if help_ else None,
                    "credited_defender": names.get(d1, d1), "credited_defender_id": d1, "credit_prob": round(float(credit.iloc[0]), 3),
                    "credited_role": role_of.get(d1), "confidence": tier(float(credit.iloc[0])),
                    "_credit": credit.to_dict(), "label": "INFERRED window credit"})
    return pd.DataFrame(out)


def explosive_table(cr, names, s):
    rows = {}
    for _, r in cr.iterrows():
        for d, q in r._credit.items():
            k = (d, r.defteam)
            a = rows.setdefault(k, np.zeros(6))
            a[0] += q
            if r.result in ("complete", "TD"):
                a[1] += q
                a[2] += q * r.yards
            if r.explosive20:
                a[3] += q
                a[4] += q * r.yards
        k = (r.credited_defender_id, r.defteam)
        if r.explosive20:
            rows.setdefault(k, np.zeros(6))[5] += 1
    pos = s.groupby("gsis").grp.last()
    df = pd.DataFrame([{"team": tm, "player": names.get(d, d), "gsis_id": d, "pos": pos.get(d), "window_targets": round(a[0], 1),
                        "window_rec": round(a[1], 1), "window_yds": round(a[2], 1), "explosive20_credit": round(a[3], 2),
                        "explosive20_yds_credit": round(a[4], 1), "explosive20_top_credited": int(a[5])} for (d, tm), a in rows.items()])
    df["window_ypt"] = (df.window_yds / df.window_targets).round(2)
    df["label"] = "INFERRED window credit (zone of responsibility), not charted coverage"
    return df.sort_values("explosive20_credit", ascending=False)


def rush_explosives(p, names):
    r = p[(p.rush_attempt == 1) & (p.rushing_yards >= 10)].copy()
    r["tk"] = r[["solo_tackle_1_player_id", "tackle_with_assist_1_player_id", "assist_tackle_1_player_id"]].bfill(axis=1).iloc[:, 0]
    g = r.groupby(["defteam", "tk"]).agg(rush10_tackled=("play_id", "size"), rush10_yds=("rushing_yards", "sum")).reset_index()
    g["player"] = g.tk.map(names)
    g["label"] = "tackler on a 10+ yard run (pursuit evidence, not a window model)"
    td = r[r.tk.isna()].groupby("defteam").size().rename("rush10_no_tackler_eg_TD")
    return g.sort_values("rush10_tackled", ascending=False), td


def cell_owner_names(mix, roles, names, rng, n=4000):
    """Most likely owner for each grid cell (band x width) under the team's shell mix, WR receiver."""
    out = {}
    for b in range(4):
        for ci, cn in enumerate(COLS):
            shell = rng.choice(SHELLS, size=n, p=mix)
            own = owner_role(shell, np.full(n, b), np.full(n, ci), np.full(n, "WR", dtype=object), rng.random(n) < 0.5, rng.random(n) < 0.5)
            vc = pd.Series(own).map(roles).value_counts(normalize=True)
            out[(b, cn)] = (names.get(vc.index[0], vc.index[0]), vc.iloc[0])
    return out


def short(n):
    n = str(n)
    if "." in n.split()[0]:
        return n
    parts = n.split()
    return n if len(parts) < 2 else f"{parts[0][0]}.{' '.join(parts[1:])}"


def chart_game(cr, g, tm, roles, mix, names, path, rng, title):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    d = cr[(cr.game_id == g) & (cr.defteam == tm)]
    fig, ax = plt.subplots(figsize=(11, 8.5))
    ax.set_facecolor("#2e7d32")
    for y in (0, 10, 20):
        ax.axhline(y, color="white", lw=1.2 if y else 2.5, alpha=0.8)
    for xb in (-14.5, -4.5, 4.5, 14.5):
        ax.axvline(xb, color="white", lw=0.8, ls="--", alpha=0.6)
    owners = cell_owner_names(mix, roles, names, rng)
    yc = {0: -3, 1: 5, 2: 15, 3: 30}
    for (b, cn), (nm, q) in owners.items():
        ax.text(XPOS[cn], yc[b] + 2.8, f"{short(nm)} {q:.0%}", ha="center", va="center", fontsize=7, color="white", alpha=0.75)
    comp = d[d.result.isin(["complete", "TD"])]
    cols = {nm: plt.cm.tab20(i % 20) for i, nm in enumerate(comp.credited_defender.value_counts().index)}
    jit = np.random.default_rng(1).uniform(-3, 3, len(comp))
    k_ex = 0
    for (_, r), j in zip(comp.iterrows(), jit):
        x = XPOS.get(r.likely_width, 0) + j
        y = min(r.air_yards, 42)
        ax.plot([x, x], [y, min(r.air_yards + r.yac, 45)], color=cols[r.credited_defender], lw=1, alpha=0.6)
        ax.scatter(x, y, s=170 if r.explosive20 else 55, marker="*" if r.explosive20 else "o", color=cols[r.credited_defender],
                   edgecolor="black", zorder=3)
        if r.explosive20:
            ax.annotate(f"{short(r.receiver)} {int(r.yards)}", (x, y), xytext=(-70 if x > 15 else 6, 4 + 10 * (k_ex % 3)), textcoords="offset points", fontsize=8, color="yellow")
            k_ex += 1
    for nm, c in cols.items():
        ax.scatter([], [], color=c, edgecolor="black", label=f"{nm} ({(comp.credited_defender == nm).sum()})")
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=8, title="Credited defender (catches)")
    ax.set_xlim(-26.7, 26.7)
    ax.set_ylim(-8, 45)
    ax.set_xticks([XPOS[c] for c in COLS], ["Left", "L-slot", "Middle", "R-slot", "Right"])
    ax.set_ylabel("Catch point: air yards from LOS (line = YAC to end spot)")
    ax.set_title(f"{title}\nINFERRED window credit, offense's view. Star = 20+ yd catch. Cell labels = most likely window owner under {tm}'s shell mix", fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def chart_heat(cr, tm, path, names):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    d = cr[cr.defteam == tm].copy()
    d["band"] = d.catch_band
    lg = cr.groupby(["catch_band", "pass_location"]).yards.mean()
    fig, ax = plt.subplots(figsize=(9, 7))
    M = np.full((4, 3), np.nan)
    for i, b in enumerate(BANDS):
        for j, l in enumerate(["left", "middle", "right"]):
            x = d[(d.band == b) & (d.pass_location == l)]
            if len(x) >= 3:
                M[i, j] = x.yards.mean() - lg.get((b, l), np.nan)
                top = x[x.explosive20].credited_defender.value_counts()
                txt = f"{x.yards.mean():.1f} yds/tgt\n(lg {lg.get((b, l), np.nan):.1f}), n={len(x)}\n20+: {int(x.explosive20.sum())}"
                if len(top):
                    txt += f"\n{short(top.index[0])} x{top.iloc[0]}"
                ax.text(j, i, txt, ha="center", va="center", fontsize=8)
    im = ax.imshow(M, cmap="RdYlGn_r", vmin=-4, vmax=4, origin="lower", aspect="auto")
    ax.set_xticks(range(3), ["Left", "Middle", "Right"])
    ax.set_yticks(range(4), ["Behind LOS", "0-9", "10-19", "20+"])
    ax.set_ylabel("Catch depth (air yards)")
    fig.colorbar(im, label="Yards per target vs league (red = beaten more)")
    ax.set_title(f"{tm}: where they get beat (2026 wk1-12, offense's view)\nINFERRED: name = most-credited defender on 20+ catches in that window", fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def upcoming(raw, t, mix, tend, s, names, expl, rng):
    g = pd.read_csv(raw / "games.csv")
    g = g[(g.season == 2026) & g.away_score.isna() & (g.week == 12)]
    last4 = t[t.week > t.week.max() - 4]
    ex = expl.set_index(["gsis_id", "team"])
    rows = []
    for _, gm in g.iterrows():
        for off, dfn in ((gm.away_team, gm.home_team), (gm.home_team, gm.away_team)):
            ls = s[s.team == dfn]
            if not len(ls) or dfn not in mix:
                continue
            lastg = ls.sort_values("week").game_id.iloc[-1]
            c = ls[ls.game_id == lastg].groupby("gsis").agg(grp=("grp", "first"), pct=("defense_pct", "max")).reset_index()
            roles = assign_roles(c, tend)
            top = last4[last4.posteam == off].groupby(["receiver_player_id", "receiver_player_name", "rpos"]).size().nlargest(4)
            for (rid, rn, rp), n4 in top.items():
                h = t[(t.receiver_player_id == rid) & t.air_yards.notna() & t.pass_location.notna()]
                if not len(h):
                    continue
                acc = pd.Series(dtype=float)
                for _, x in h.iterrows():
                    vc, _, _ = simulate(x, mix[dfn], roles, rng, n=2000)
                    acc = acc.add(vc, fill_value=0)
                acc = (acc / len(h)).sort_values(ascending=False)
                deep = (h.air_yards >= 20).mean()
                rec = {"week": 12, "gameday": gm.gameday, "offense": off, "defense": dfn, "receiver": rn, "rpos": rp, "tgts_last4wks": int(n4),
                       "deep20_target_share": round(deep, 2), "roles_from_game": lastg}
                for i in range(2):
                    d = acc.index[i]
                    e = ex.loc[(d, dfn)] if (d, dfn) in ex.index else None
                    rec[f"window_defender_{i+1}"] = names.get(d, d)
                    rec[f"share_{i+1}"] = round(float(acc.iloc[i]), 3)
                    rec[f"def{i+1}_explosive20_credit"] = float(e.explosive20_credit) if e is not None else None
                    rec[f"def{i+1}_window_ypt"] = float(e.window_ypt) if e is not None else None
                rec["label"] = "INFERRED (not verified; not usable for the verified-defender rule)"
                rows.append(rec)
    return pd.DataFrame(rows)


MARK2 = "<!-- V2-WINDOW-CREDIT -->"


def write_sections(pdir, expl, up, valtxt):
    for f in pdir.glob("*.md"):
        tm = f.stem
        body = f.read_text().split(MARK2)[0].rstrip() + "\n\n" + MARK2 + "\n"
        L = ["## v2 INFERRED window credit (zone of responsibility)", "",
             "Who owned the window where the ball was caught, from the team's shell mix + defender roles + catch spot (pbp direction + air yards), "
             f"blended with the tackler. **INFERRED only.** {valtxt}", "",
             "| Defender | Pos | Window tgts | Window rec | Window yds | YPT | 20+ catches credited (prob-weighted) | 20+ yds credited | 20+ as top credit |",
             "|---|---|---|---|---|---|---|---|---|"]
        for _, x in expl[(expl.team == tm) & (expl.window_targets >= 5)].sort_values("explosive20_credit", ascending=False).head(12).iterrows():
            L.append(f"| {x.player} | {x.pos} | {x.window_targets} | {x.window_rec} | {x.window_yds} | {x.window_ypt} | {x.explosive20_credit} | {x.explosive20_yds_credit} | {x.explosive20_top_credited} |")
        u = up[up.defense == tm] if len(up) else up
        if len(u):
            L += ["", f"### Rest of Week 12: receivers vs likely {tm} window defender (INFERRED)", "",
                  "| Date | Offense | Receiver | Tgts last 4 | 20+ air tgt share | Window defender (share, his 20+ credit) | Next |", "|---|---|---|---|---|---|---|"]
            for _, x in u.iterrows():
                L.append(f"| {x.gameday} | {x.offense} | {x.receiver} ({x.rpos}) | {x.tgts_last4wks} | {x.deep20_target_share:.0%} | "
                         f"{x.window_defender_1} ({x.share_1:.0%}, {x.def1_explosive20_credit}) | {x.window_defender_2} ({x.share_2:.0%}, {x.def2_explosive20_credit}) |")
        f.write_text(body + "\n".join(L) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True, type=Path)
    ap.add_argument("--out", type=Path, default=HERE)
    ap.add_argument("--charts-copy", type=Path)
    a = ap.parse_args()
    out = a.out
    t, links, names, rows, rbg, mix, imp, s = run(a.raw)
    cr = credit_table(t, rows, rbg, names)
    expl = explosive_table(cr, names, s)
    cr.drop(columns="_credit").to_csv(out / "defender_window_credit_inferred.csv", index=False)
    expl.to_csv(out / "defender_explosives_allowed_inferred.csv", index=False)
    p = B.load(a.raw, None)[0]
    re_, nt = rush_explosives(p, names)
    re_.to_csv(out / "rush_explosives_10plus_tackler.csv", index=False)
    json.dump({"shell_mix": {k: dict(zip(SHELLS, np.round(v, 3).tolist())) for k, v in mix.items()}, "imputed_shells": imp},
              open(out / "team_shell_mix.json", "w"), indent=1)
    rng = np.random.default_rng(11)
    cd = out / "charts"
    cd.mkdir(exist_ok=True)
    for g, title in (("2026_12_PHI_DAL", "PHI@DAL Thanksgiving"), ("2026_12_CHI_DET", "CHI@DET Thanksgiving")):
        for tm in g.split("_")[2:]:
            chart_game(cr, g, tm, rbg[(g, tm)], mix[tm], names, cd / f"{g}_{tm}_defense_window_credit.png", rng, f"{title}: {tm} defense")
    for tm in ("DAL", "PHI"):
        chart_heat(cr, tm, cd / f"{tm}_where_beaten_heat.png", names)
    up = upcoming(a.raw, t, mix, tendencies(links), s, names, expl, rng)
    up.to_csv(out / "upcoming_w12_window_matchups_inferred.csv", index=False)
    vs = pd.read_csv(out / "attribution_v2_validation_summary.csv") if (out / "attribution_v2_validation_summary.csv").exists() else None
    valtxt = ""
    if vs is not None:
        r = vs.set_index("method").loc["v2_window"]
        valtxt = (f"Held-out wk 9–12 verified PBU/INT (n={int(r.n)}): exact defender {r.top1:.0%} (top-2 {r.top2:.0%}); "
                  f"window class (CB-left/CB-right/nickel/S/LB) {r.window:.0%}; position group {r.pos:.0%}.")
    write_sections(out / "profiles", expl, up, valtxt)
    if a.charts_copy:
        a.charts_copy.mkdir(parents=True, exist_ok=True)
        for f in cd.glob("*.png"):
            (a.charts_copy / f.name).write_bytes(f.read_bytes())
    print(json.dumps({"targets_credited": len(cr), "by_conf": cr.confidence.value_counts().to_dict(),
                      "explosive20": int(cr.explosive20.sum()), "upcoming_rows": len(up)}, indent=1))


if __name__ == "__main__":
    main()
