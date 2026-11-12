#!/usr/bin/env python3
"""NFL Week 10 matchup build — Phases 1–10 — RUN_ID 2026-11-12_thu0600.
Adapted from runs/2026-11-05_matchup_run/build.py. Append-only to matchup_master."""
import pandas as pd, numpy as np, json, datetime, os, re, csv

RUN = "/workspace/nfl-database/runs/2026-11-12_matchup_run"
S = f"{RUN}/src"
NOW = datetime.datetime.now()
TS = f"{NOW:%Y-%m-%dT%H:%M}"
RUN_ID = "2026-11-12_thu0600"

pbp = pd.read_parquet(f"{S}/play_by_play_2026.parquet")
pbp = pbp[pbp.season_type == "REG"]
pl = pd.read_parquet(f"{S}/players.parquet")[["gsis_id", "display_name", "position"]]
pos = dict(zip(pl.gsis_id, pl.position))
nm = dict(zip(pl.gsis_id, pl.display_name))
ftn = pd.read_parquet(f"{S}/ftn_charting_2026.parquet")
ab = {"LA": "LAR", "WAS": "WSH"}
fix = lambda t: ab.get(t, t)
pbp["posteam"] = pbp.posteam.map(fix)
pbp["defteam"] = pbp.defteam.map(fix)

GAMES = [
    ("WSH", "NYG", "Thu 8:15 PM TNF"),
    ("NE", "DET", "Sun 9:30 AM Munich"),
    ("KC", "ATL", "Sun 1:00 PM"),
    ("HOU", "CLE", "Sun 1:00 PM"),
    ("MIN", "GB", "Sun 1:00 PM"),
    ("JAX", "TEN", "Sun 1:00 PM"),
    ("MIA", "IND", "Sun 1:00 PM"),
    ("CAR", "NO", "Sun 1:00 PM"),
    ("BUF", "NYJ", "Sun 1:00 PM"),
    ("SEA", "LV", "Sun 4:05 PM"),
    ("LAR", "ARI", "Sun 4:05 PM"),
    ("SF", "DAL", "Sun 4:25 PM"),
    ("PIT", "CIN", "Sun 8:20 PM SNF"),
    ("LAC", "BAL", "Mon 8:15 PM MNF"),
]

FULL = {
    "Arizona Cardinals": "ARI", "Atlanta Falcons": "ATL", "Baltimore Ravens": "BAL",
    "Buffalo Bills": "BUF", "Carolina Panthers": "CAR", "Chicago Bears": "CHI",
    "Cincinnati Bengals": "CIN", "Cleveland Browns": "CLE", "Dallas Cowboys": "DAL",
    "Denver Broncos": "DEN", "Detroit Lions": "DET", "Green Bay Packers": "GB",
    "Houston Texans": "HOU", "Indianapolis Colts": "IND", "Jacksonville Jaguars": "JAX",
    "Kansas City Chiefs": "KC", "Las Vegas Raiders": "LV", "Los Angeles Chargers": "LAC",
    "Los Angeles Rams": "LAR", "Miami Dolphins": "MIA", "Minnesota Vikings": "MIN",
    "New England Patriots": "NE", "New Orleans Saints": "NO", "New York Giants": "NYG",
    "New York Jets": "NYJ", "Philadelphia Eagles": "PHI", "Pittsburgh Steelers": "PIT",
    "San Francisco 49ers": "SF", "Seattle Seahawks": "SEA", "Tampa Bay Buccaneers": "TB",
    "Tennessee Titans": "TEN", "Washington Commanders": "WSH",
}

# ---- lines (ESPN DK consensus, home_spread negative = home favored)
LN_RAW = json.load(open(f"{RUN}/lines.json"))
LN = {}
for gkey, v in LN_RAW["games"].items():
    a, h = gkey.split("@")
    LN[(a, h)] = dict(home_spread=v["home_spread"], total=v["total"], book=v.get("provider", "DraftKings"), details=v.get("details"))
lt = LN_RAW["pulled_et"]

# ---- weather
wx_raw = json.load(open(f"{RUN}/weather.json"))
WX = wx_raw["games"]

# ---- injuries
inj = json.load(open(f"{RUN}/espn_injuries.json"))
INJ = {}
for t in inj.get("injuries", []):
    code = FULL.get(t.get("displayName"))
    if not code:
        continue
    for i in t.get("injuries", []):
        st = i.get("status")
        a = i.get("athlete", {})
        if st in ("Out", "Doubtful", "Questionable", "Injured Reserve"):
            INJ.setdefault(code, []).append(
                (a.get("displayName"), (a.get("position") or {}).get("abbreviation"), st, (i.get("shortComment") or "")[:90])
            )

# Manual key notes (injury sweep 2026-11-04) — ensure starters flagged even if ESPN lags
MANUAL_NOTES = {
    "NYG": "J.J. McCarthy QB Questionable (hip; ESPN text says full Tue). Cam Skattebo RB listed OUT but ESPN text says full participant Tue — contradictory, verify official report before any NYG RB leg.",
    "WSH": "Yankoff TE ruled out; Lucas Patrick G out; DL Payne/Kinlaw on IR (run-D downgrade vs NYG). Burks WR no designation.",
    "MIN": "QB UNSETTLED: Kirk Cousins acquired from LV, O'Connell not committing to a Week 10 starter; Wentz Questionable (ankle, limited); Kyler Murray Doubtful. Hold all MIN pass-catcher legs until starter named.",
    "LV": "NEW STARTER: Fernando Mendoza (rookie) starts vs SEA after Cousins trade; O'Connell QB2. Backup/new-QB flag on LV pass catchers.",
    "ARI": "NEW STARTER: Carson Beck starts vs LAR (HC LaFleur, Wed); Minshew out for season (UCL surgery). New-QB flag on ARI pass catchers.",
    "MIA": "NEW STARTER: Kyle McCord starts at IND; Malik Willis on IR. New-QB flag on MIA pass catchers.",
    "CLE": "Browns announced Deshaun Watson (cleared from concussion) starts vs HOU; Shedeur Sanders back to backup (ESPN status field still says Out — text says starting; verify).",
    "BAL": "QB: HC Minter 'expects' Jacoby Brissett to start MNF vs LAC; Lamar on IR (thumb surgery), Huntley IR. Backup-QB flag on BAL pass catchers.",
    "SEA": "QB: Drew Lock Questionable (elbow/oblique, limited Wed); Darnold OUT; Milroe getting added reps. OL: Charles Cross OT and Quenton Nelson G both Doubtful — Panthers-rule OL risk.",
    "DET": "Jared Goff Questionable (chest, limited Wed). Munich neutral site, early kick.",
    "KC": "Mahomes Questionable (elbow/knee) but full participant Wed.",
    "LAC": "Herbert Questionable (finger); Harbaugh says he 'should be good to go' for MNF.",
    "PHI": "(bye) —",
    "LAR": "Puka Nacua OUT — target redistribution; L3 shares below include his games, so re-check the opportunity gate.",
    "GB": "Josh Jacobs RB OUT — carry share shifts; L3 carry shares below are stale for GB RBs.",
    "NE": "TreVeyon Henderson RB OUT, Rhamondre Stevenson Doubtful, C Ben Brown OUT — RB room and interior OL thin.",
    "DAL": "Jake Ferguson TE OUT; Tyler Goodson RB out (ACL/MCL).",
    "NO": "C Erik McCoy Doubtful (interior OL).",
    "IND": "OT Jalen Travis Doubtful.",
    "JAX": "Script: JAX BLOWOUT FAVORITE (-10.5 at TEN). Late-clock JAX pass overs blocked. Passing yards stay off NFL slips completely.",
}

# ---- Sharp coverage schemes (cache Nov 3; free refresh page fetched but CSV used)
cov = {}
with open(f"{S}/nfl-coverage-schemes.csv") as fh:
    for row in csv.DictReader(fh):
        code = FULL.get(row["Team"])
        if code:
            cov[code] = (
                float(row["Man Rate"]),
                float(row["Zone Rate"]),
                float(row["Middle Closed Rate"]),
                float(row["Middle Open Rate"]),
            )

# ---- PFR advanced defense (fresh pull 403; use Oct 29 cache)
pfr = pd.read_html("/workspace/nfl-sim/mnf12/pfr_def_adv_2026.html")[0]
pfr.columns = [c[1] for c in pfr.columns]
pfr = pfr[pfr.Player != "Player"].copy()
for c in ["Tgt", "Cmp", "Yds", "Yds/Tgt", "Rat", "Prss", "Bltz", "Sk", "G", "Cmp%"]:
    if c in pfr.columns:
        pfr[c] = pd.to_numeric(pfr[c], errors="coerce")
pfr["Team"] = pfr.Team.replace({"LAR": "LAR", "WAS": "WSH"})
PFRT = {
    "ARI": "ARI", "ATL": "ATL", "BAL": "BAL", "BUF": "BUF", "CAR": "CAR", "CHI": "CHI",
    "CIN": "CIN", "CLE": "CLE", "DAL": "DAL", "DEN": "DEN", "DET": "DET", "GB": "GNB",
    "HOU": "HOU", "IND": "IND", "JAX": "JAX", "KC": "KAN", "LV": "LVR", "LAC": "LAC",
    "LAR": "LAR", "MIA": "MIA", "MIN": "MIN", "NE": "NWE", "NO": "NOR", "NYG": "NYG",
    "NYJ": "NYJ", "PHI": "PHI", "PIT": "PIT", "SEA": "SEA", "SF": "SFO", "TB": "TAM",
    "TEN": "TEN", "WSH": "WAS",
}
# Also accept alternate PFR codes that appear as-is
PFR_ALT = {"GNB": "GB", "KAN": "KC", "LVR": "LV", "NWE": "NE", "NOR": "NO", "SFO": "SF", "TAM": "TB", "WAS": "WSH"}

# ---- profiles
pp = pbp[pbp.play_type.isin(["pass", "run"])].copy()
pp["rpos"] = pp.receiver_player_id.map(pos)
pp["explo"] = ((pp.play_type == "pass") & (pp.yards_gained >= 20)) | ((pp.play_type == "run") & (pp.yards_gained >= 10))
f2 = ftn[["nflverse_game_id", "nflverse_play_id", "n_blitzers", "n_pass_rushers"]].rename(
    columns={"nflverse_game_id": "game_id", "nflverse_play_id": "play_id"}
)
pp = pp.merge(f2, on=["game_id", "play_id"], how="left")


def side(df, team, key):
    d = df[df[key] == team]
    g = d.game_id.nunique()
    if g == 0:
        return {k: np.nan for k in [
            "games", "plays_pg", "pass_rate", "pass_yds_pg", "ypa", "rush_ypc", "rush_yds_pg",
            "sack_rate", "pressure_proxy", "explo_pg", "blitz_rate_ftn", "third_conv", "rz_td",
            "WR_tgt_pg", "WR_rec_yds_pg", "WR_ypt", "TE_tgt_pg", "TE_rec_yds_pg", "TE_ypt",
            "RB_tgt_pg", "RB_rec_yds_pg", "RB_ypt",
        ]}
    db = d[d.qb_dropback == 1]
    ps = d[d.play_type == "pass"]
    ru = d[(d.play_type == "run") & (d.qb_scramble != 1)]
    o = dict(
        games=g,
        plays_pg=len(d) / g,
        pass_rate=len(db) / len(d) if len(d) else np.nan,
        pass_yds_pg=ps.yards_gained.sum() / g,
        ypa=ps[ps.pass_attempt == 1].yards_gained.mean(),
        rush_ypc=ru.yards_gained.mean(),
        rush_yds_pg=ru.yards_gained.sum() / g,
        sack_rate=db.sack.mean() if len(db) else np.nan,
        pressure_proxy=(db.sack.astype(bool) | db.qb_hit.astype(bool)).mean() if len(db) else np.nan,
        explo_pg=d.explo.sum() / g,
    )
    ch = db[db.n_pass_rushers.notna()]
    o["blitz_rate_ftn"] = (ch.n_pass_rushers >= 5).mean() if len(ch) else np.nan
    third = d[d.down == 3]
    o["third_conv"] = third.third_down_converted.sum() / max(1, (third.third_down_converted + third.third_down_failed).sum())
    rz = d[d.yardline_100 <= 20].groupby(["game_id", "drive"]).touchdown.max()
    o["rz_td"] = rz.mean() if len(rz) else np.nan
    for P, lab in [("WR", "WR"), ("TE", "TE"), ("RB", "RB")]:
        t = ps[ps.rpos == P]
        o[f"{lab}_tgt_pg"] = len(t) / g
        o[f"{lab}_rec_yds_pg"] = t.yards_gained.where(t.complete_pass == 1, 0).sum() / g
        o[f"{lab}_ypt"] = t.yards_gained.where(t.complete_pass == 1, 0).mean()
    return o


TEAMS = sorted({t for a, h, _ in GAMES for t in (a, h)})
OFF = {t: side(pp, t, "posteam") for t in TEAMS}
DEF = {t: side(pp, t, "defteam") for t in TEAMS}
for t in TEAMS:
    q = pfr[pfr.Team == PFRT.get(t, t)]
    if q.empty:
        # try raw code
        q = pfr[pfr.Team == t]
    db = pp[(pp.defteam == t) & (pp.qb_dropback == 1)]
    DEF[t]["pfr_pressure_rate"] = q.Prss.sum() / max(1, len(db)) if q.Prss.notna().any() else np.nan


def usage(t):
    d = pp[pp.posteam == t]
    gids = sorted(d.game_id.unique(), key=lambda x: d[d.game_id == x].week.iloc[0])[-3:]
    d = d[d.game_id.isin(gids)]
    ps = d[d.play_type == "pass"]
    ru = d[(d.play_type == "run") & (d.qb_scramble != 1)]
    ts = ps.receiver_player_id.value_counts(normalize=True).head(5)
    cs = ru.rusher_player_id.value_counts(normalize=True).head(2)
    return [(nm.get(k, k), pos.get(k, "?"), v) for k, v in ts.items()], [(nm.get(k, k), v) for k, v in cs.items()]


def label(spread):
    if spread is None:
        return "UNKNOWN"
    if spread <= -7:
        return "BLOWOUT FAVORITE"
    if spread <= -3.5:
        return "MODERATE FAVORITE"
    if spread < 3.5:
        return "TOSS-UP"
    if spread < 7:
        return "MODERATE UNDERDOG"
    return "UNDERDOG (big)"


def inj_tag(name, team):
    for n, p, st, _ in INJ.get(team, []):
        if n and name and n.lower() == name.lower():
            return f" [{st.upper()}]"
    return ""


OL = {"T", "G", "C", "OT", "OG", "OL"}

pbp_max_week = int(pbp.week.max())
pbp_max_date = str(pbp.game_date.max())[:10]

cards = [
    f"# NFL Matchup Cards — Week 10 TNF–MNF, 2026 (run {RUN_ID}, built {TS} ET)\n",
    "Sources: nflverse play_by_play_2026 + FTN charting + players "
    f"(thru Week {pbp_max_week}, max date {pbp_max_date}, fresh nflverse release pull 2026-11-12 05:53 ET); "
    "Sharp Football coverage schemes (free page fetched and parsed fresh 2026-11-12 05:55 ET); "
    "PFR advanced defense cache (Oct 29 at /workspace/nfl-sim/mnf12/pfr_def_adv_2026.html — fresh pull 403 again 2026-11-12 — CB leaderboards are 2 weeks stale); "
    f"ESPN injuries API ({TS} ET) + ESPN injury comment text for QB/starter notes; "
    f"ESPN scoreboard Week 10 DraftKings consensus spreads/totals (pulled {lt} ET); "
    f"Open-Meteo + NWS hourly via tools/weather_forecast.py (pulled {wx_raw.get('pulled_et')} ET).",
    "Gaps: NGS route/gap data not refreshed (nextgenstats.nfl.com / nflverse NGS not pulled this run — same gap as Nov 1/Nov 5). "
    "WR outside-vs-slot splits allowed are NOT in free pbp, so they're shown as WR combined. "
    "No FanDuel live prop pull this morning (Odds API budget lean); lines are ESPN DK consensus. "
    "PFR pressure rate = Oct 29 PFR pressures / season dropbacks + pbp sack+hit proxy. "
    "No per-game gate/sim PASS stamps this run — cards are matchup/projection only. "
    "PASSING YARDS stay off NFL slips completely (Rico rule) — pass volume noted in opportunity only, never as a bet highlight. "
    "Late-clock QB passing overs blocked on BLOWOUT FAVORITE script gates.\n"
    "Key starter notes: new/backup QBs at ARI (Beck), MIA (McCord), LV (Mendoza), BAL (Brissett expected), CLE (Watson back); MIN QB unsettled (Cousins/Wentz/Murray); SEA Lock Q with OL Cross+Nelson Doubtful. Puka OUT, Josh Jacobs OUT, Ferguson OUT. PHI on bye.\n",
]

rows = []
soft_all = []
panthers_all = []
script_labels = {}

for a, h, ko in GAMES:
    ln = LN.get((a, h), {})
    hs = ln.get("home_spread")
    tot = ln.get("total")
    lab = {h: label(hs), a: label(-hs if hs is not None else None)}
    script_labels[f"{a}@{h}"] = {h: lab[h], a: lab[a], "hs": hs, "tot": tot}
    book = ln.get("book", "DraftKings")
    c = [
        f"\n## {a} @ {h} — {ko} ET",
        f"**Line (ESPN {book} consensus {lt} ET):** {h} {hs:+}, total {tot} (details: {ln.get('details')}). "
        f"**Script gate:** {h} {lab[h]}, {a} {lab[a]}.",
    ]
    # weather
    w = WX.get(f"{a}@{h}", {})
    roof = w.get("roof", "?")
    if w.get("status") == "INDOOR":
        c.append(f"**Weather ({roof}):** Indoor — weather ignored.")
    else:
        tmin, tmax = w.get("temp_min"), w.get("temp_max")
        temp_s = f"{tmin:.0f}–{tmax:.0f}°F" if tmin is not None and tmax is not None else "temp n/a"
        wind = w.get("wind_mph")
        gust = w.get("gust_mph")
        precip = w.get("precip_pct")
        why = w.get("why") or []
        flag_s = f" **WX FLAG:** {', '.join(why)}." if why else ""
        c.append(
            f"**Weather ({roof}):** {temp_s}, wind {wind if wind is not None else '?'} mph "
            f"(gusts {gust if gust is not None else '?'}), precip chance up to {precip if precip is not None else '?'}%.{flag_s}"
        )
    # blowout late-clock note
    for side_t in (a, h):
        if lab[side_t] == "BLOWOUT FAVORITE":
            c.append(
                f"**Script note:** {side_t} is a BLOWOUT FAVORITE — late-clock QB passing overs blocked; "
                f"passing-yards props stay off slips entirely (Rico rule)."
            )
    # backup QB / manual notes
    for t in (a, h):
        if t in MANUAL_NOTES:
            c.append(f"**Starter / injury note ({t}):** {MANUAL_NOTES[t]}")

    flags = []
    for o, dd in [(a, h), (h, a)]:
        O, D = OFF[o], DEF[dd]
        tu, cu = usage(o)
        cv = cov.get(dd)
        cbs = pfr[(pfr.Team == PFRT.get(dd, dd)) & (pfr.Pos.isin(["CB", "S", "FS", "SS", "DB"])) & (pfr.Tgt >= 15)].sort_values(
            "Yds", ascending=False
        )
        if cbs.empty:
            cbs = pfr[(pfr.Team == dd) & (pfr.Pos.isin(["CB", "S", "FS", "SS", "DB"])) & (pfr.Tgt >= 15)].sort_values(
                "Yds", ascending=False
            )
        cbl = "; ".join(
            f"{r.Player} ({r.Pos}) {int(r.Tgt)} tgt, {r['Cmp%']}% comp, {r['Yds/Tgt']} YPT, {int(r.Yds)} yds"
            for _, r in cbs.head(4).iterrows()
        )
        projp = O["plays_pg"] * (1.03 if "UNDERDOG" in lab[o] else 0.98 if "BLOWOUT" in lab[o] else 1)
        prate = min(0.72, max(0.45, O["pass_rate"] + (0.04 if "UNDERDOG" in lab[o] else -0.04 if "FAVORITE" in lab[o] else 0)))
        patt = projp * prate
        ratt = projp * (1 - prate) * 0.93
        c.append(f"\n**{o} offense vs {dd} defense**")
        c.append(
            f"- {dd} D allows (per game): WR {D['WR_tgt_pg']:.1f} tgt / {D['WR_rec_yds_pg']:.0f} yds ({D['WR_ypt']:.1f} YPT); "
            f"TE {D['TE_tgt_pg']:.1f} / {D['TE_rec_yds_pg']:.0f} ({D['TE_ypt']:.1f}); "
            f"RB rec {D['RB_tgt_pg']:.1f} / {D['RB_rec_yds_pg']:.0f} ({D['RB_ypt']:.1f}); "
            f"rush {D['rush_yds_pg']:.0f} yds at {D['rush_ypc']:.2f} YPC; {D['explo_pg']:.1f} explosive plays."
        )
        c.append(
            f"- {dd} coverage (Sharp): "
            + (f"man {cv[0]}% / zone {cv[1]}%, MOF closed {cv[2]}% / open {cv[3]}%." if cv else "not found in Sharp table — gap.")
            + f" Blitz (FTN 5+ rushers) {D['blitz_rate_ftn']:.0%}; pressure (PFR) {D['pfr_pressure_rate']:.0%}; "
            f"sack+hit proxy {D['pressure_proxy']:.0%}."
        )
        c.append(f"- {dd} defenders giving up the most yards (PFR, Oct 29): {cbl or 'none with 15+ targets'}.")
        c.append(
            f"- 3rd down: {o} converts {O['third_conv']:.0%}, {dd} allows {D['third_conv']:.0%}. "
            f"Red-zone TD per trip: {o} {O['rz_td']:.0%}, {dd} allows {D['rz_td']:.0%}."
        )
        tgt_s = ", ".join(
            f"{n}{inj_tag(n, o)} ({p}) {s:.0%} ≈ {s * patt * 0.93:.1f} tgt" for n, p, s in tu
        )
        car_s = ", ".join(f"{n}{inj_tag(n, o)} {s:.0%} ≈ {s * ratt:.0f}" for n, s in cu)
        c.append(
            f"- Opportunity projection: ~{projp:.0f} plays, ~{patt:.0f} dropbacks, ~{ratt:.0f} RB carries. "
            f"L3 target shares: {tgt_s}. Carries: {car_s}."
        )
        c.append(
            f"- Pass volume note only (NOT a slip candidate): ~{patt:.0f} dropbacks projected — passing-yards props stay off NFL slips."
        )
        oinj = [x for x in INJ.get(o, []) if x[2] != "Injured Reserve"]
        olh = [x for x in oinj if x[1] in OL]
        pr = D.get("pfr_pressure_rate") or 0
        bl = D.get("blitz_rate_ftn") or 0
        sk = O.get("sack_rate") or 0
        risk = (pr >= 0.25 or bl >= 0.33) and (sk >= 0.07 or len(olh) >= 1)
        if risk:
            msg = (
                f"PANTHERS RULE — {o} QB: {dd} pressure {pr:.0%} / blitz {bl:.0%}, "
                f"{o} sack rate {sk:.1%}, OL on report: {', '.join(f'{x[0]} {x[1]} {x[2]}' for x in olh) or 'none'}. "
                f"Lean unders/checkdowns on {o} pass volume."
            )
            flags.append(msg)
            panthers_all.append(f"{a}@{h} {o}: {msg}")
        elif olh:
            flags.append(
                f"{o} OL on report: {', '.join(f'{x[0]} {x[1]} {x[2]}' for x in olh)} "
                f"(sack rate {sk:.1%} vs {dd} pressure {pr:.0%})."
            )
        soft = []
        if D["WR_ypt"] >= 9.0:
            soft.append(f"WR YPT {D['WR_ypt']:.1f}")
        if D["TE_ypt"] >= 8.0:
            soft.append(f"TE YPT {D['TE_ypt']:.1f}")
        if D["rush_ypc"] > 4.4:
            soft.append(f"run D {D['rush_ypc']:.2f} YPC")
        if D["rush_ypc"] <= 3.8:
            flags.append(f"{dd} run suppression ({D['rush_ypc']:.2f} YPC) — cut {o} rush yards.")
        if D["TE_ypt"] <= 5.5:
            flags.append(f"{dd} hard on TEs ({D['TE_ypt']:.1f} YPT) — cut {o} TE yards.")
        if soft:
            c.append(
                f"- SOFT-MATCHUP FLAG for {o}: {dd} {'; '.join(soft)} "
                f"(still needs the opportunity gate and game-by-game opponent adjustment before any leg)."
            )
            soft_all.append(f"{a}@{h} {o} vs {dd}: {'; '.join(soft)}")
        rows.append(
            dict(
                run_ts=TS,
                run_id=RUN_ID,
                game=f"{a}@{h}",
                offense=o,
                defense=dd,
                home_spread=hs,
                total=tot,
                script_label=lab[o],
                proj_plays=round(projp, 1),
                proj_dropbacks=round(patt, 1),
                proj_rb_carries=round(ratt, 1),
                **{f"def_{k}": (round(v, 4) if isinstance(v, float) else v) for k, v in D.items()},
                **{f"off_{k}": (round(v, 4) if isinstance(v, float) else v) for k, v in O.items()},
                man=cv[0] if cv else None,
                zone=cv[1] if cv else None,
                mof_closed=cv[2] if cv else None,
                mof_open=cv[3] if cv else None,
                panthers_flag=bool(risk),
                soft_flags="; ".join(soft),
                top_targets=json.dumps([(n, p, round(s, 3)) for n, p, s in tu]),
                top_carries=json.dumps([(n, round(s, 3)) for n, s in cu]),
            )
        )

    allinj = []
    for t in (a, h):
        live = [x for x in INJ.get(t, []) if x[2] != "Injured Reserve"]
        # also surface a few key IR QBs if relevant
        ir_key = [x for x in INJ.get(t, []) if x[2] == "Injured Reserve" and x[1] == "QB"]
        shown = live[:12]
        s = f"{t}: " + (", ".join(f"{x[0]} ({x[1]}) {x[2]}" for x in shown) if shown else "none listed Out/Doubtful/Q")
        if ir_key:
            s += " | IR QB: " + ", ".join(f"{x[0]}" for x in ir_key[:3])
        allinj.append(s)
    c.append(
        f"\n**Injuries (ESPN ~{TS} ET, Out/Doubtful/Questionable):** "
        + " | ".join(allinj)
        + ". Questionable players get low rungs or a fade, not an automatic cut."
    )
    c.append("**Gate-passed legs:** none yet this run — matchup cards only; props need a full gate run before kick.")
    c.append("**Caution flags:** " + (" ".join(flags) if flags else "none beyond the standard rules."))
    cards += c

# write cards
cards_path = f"/workspace/nfl-database/cards/{RUN_ID}.md"
open(cards_path, "w").write("\n".join(cards) + "\n")

# append master
df = pd.DataFrame(rows)
mf = "/workspace/nfl-database/matchup_master.csv"
jf = "/workspace/nfl-database/matchup_master.jsonl"
before_csv = sum(1 for _ in open(mf)) - 1 if os.path.exists(mf) else 0
before_jsonl = sum(1 for _ in open(jf)) if os.path.exists(jf) else 0
if os.path.exists(mf):
    old = pd.read_csv(mf, nrows=0).columns.tolist()
    df = df.reindex(columns=old + [c for c in df.columns if c not in old])
df.to_csv(mf, mode="a", header=not os.path.exists(mf), index=False)
with open(jf, "a") as fh:
    for r in rows:
        fh.write(json.dumps(r, default=str) + "\n")
after_csv = sum(1 for _ in open(mf)) - 1
after_jsonl = sum(1 for _ in open(jf))

# save gate notes / summary artifact
summary = {
    "run_id": RUN_ID,
    "built_et": TS,
    "games": len(GAMES),
    "rows_appended": len(rows),
    "master_csv_before": before_csv,
    "master_csv_after": after_csv,
    "master_jsonl_before": before_jsonl,
    "master_jsonl_after": after_jsonl,
    "script_labels": script_labels,
    "soft_flags": soft_all,
    "panthers_flags": panthers_all,
    "cards_path": cards_path,
    "sources": {
        "pbp": f"{S}/play_by_play_2026.parquet (thru wk {pbp_max_week}, {pbp_max_date})",
        "sharp": f"{S}/nfl-coverage-schemes.csv (fresh 2026-11-12)",
        "pfr": "nfl-sim/mnf12/pfr_def_adv_2026.html (Oct 29 cache; fresh 403 on 2026-11-12)",
        "injuries": f"{RUN}/espn_injuries.json + ESPN comment text",
        "weather": f"{RUN}/weather.json",
        "lines": f"{RUN}/lines.json (ESPN DK)",
    },
    "gaps": ["NGS not refreshed", "PFR fresh pull 403", "no FanDuel prop pull", "no gate/sim PASS this run"],
}
json.dump(summary, open(f"{RUN}/run_summary.json", "w"), indent=2)
open(f"{RUN}/gate_notes.txt", "w").write(
    "No per-game gate/sim PASS this morning run. Matchup cards + master append only.\n"
    + "Soft flags:\n"
    + "\n".join(soft_all)
    + "\n\nPanthers:\n"
    + "\n".join(panthers_all)
    + "\n"
)

print("OK rows", len(rows), "csv", before_csv, "->", after_csv, "jsonl", before_jsonl, "->", after_jsonl)
print("cards", cards_path)
print("SOFT", len(soft_all))
print("PANTHERS", len(panthers_all))
for g, v in script_labels.items():
    print(g, v)
