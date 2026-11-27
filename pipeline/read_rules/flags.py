"""Glue: annotate legs with the three read-rule flags (adds columns only) and build a per-game read-rules report."""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from pipeline.read_rules import APPROVED, CUTS_ENABLED, UNKNOWN, assert_flags_only
from pipeline.read_rules import defense_allowed as DA
from pipeline.read_rules import targets_first as TF
from pipeline.read_rules import weather_grade as WG
from pipeline.read_rules.common import NFLVERSE, ROOT, clean_plays, load_pbp, load_positions

FLAG_COLUMNS = ("rr_targets_first", "rr_target_share", "rr_target_team_rank", "rr_def_vs_role", "rr_def_run_ypc_rank",
                "rr_weather")
GAMES_CSV = NFLVERSE / "games.csv"


def teams_from_game_id(game_id: str) -> tuple[str, str]:
    parts = str(game_id).split("_")
    return parts[2], parts[3]


def player_team(players: pd.DataFrame, gsis: str, week: int) -> str | None:
    h = players[(players.gsis == gsis) & (players.week < week)].sort_values("week")
    return None if not len(h) else str(h.posteam.iloc[-1])


def annotate_legs(legs: pd.DataFrame, pbp: pd.DataFrame, positions: dict, weather: dict | None = None) -> pd.DataFrame:
    """Return a copy of `legs` with FLAG_COLUMNS added. Never drops a row and never changes an existing column.
    `legs` needs week, game_id, gsis, position, market. `weather` maps game_id -> grade string (else unknown)."""
    assert_flags_only()
    clash = [c for c in FLAG_COLUMNS if c in legs.columns]
    if clash:
        raise ValueError(f"legs already carry read-rule columns {clash}; refusing to overwrite")
    out = legs.copy()
    players, team_t = TF.target_table(pbp)
    roles_cache: dict[int, pd.DataFrame] = {}
    run_cache: dict[int, pd.DataFrame] = {}
    res = {c: [] for c in FLAG_COLUMNS}
    for r in legs.itertuples(index=False):
        wk = int(r.week)
        if wk not in roles_cache:
            roles_cache[wk] = DA.role_allowed(pbp, positions, wk)
            run_cache[wk] = DA.run_allowed(pbp, wk)
        away, home = teams_from_game_id(r.game_id)
        team = player_team(players, r.gsis, wk)
        opp = (home if team == away else away if team == home else None) if team else None
        pos = str(getattr(r, "position", "") or "").upper()
        if str(r.market) in TF.RECEIVING_MARKETS:
            t = TF.evaluate(r.gsis, wk, pos, opp, players, team_t, roles_cache[wk])
        else:
            t = dict(status=TF.NA, share=UNKNOWN, team_rank=UNKNOWN)
        res["rr_targets_first"].append(t["status"])
        res["rr_target_share"].append(t["share"])
        res["rr_target_team_rank"].append(t["team_rank"])
        res["rr_def_vs_role"].append(DA.soft_vs_role(roles_cache[wk], opp, DA.role_of(pos) if pos != "WR" else "WR")
                                     if opp else UNKNOWN)
        rr = run_cache[wk]
        rk = rr[rr.defteam == opp].ypc_rank if opp else pd.Series(dtype=float)
        res["rr_def_run_ypc_rank"].append(int(rk.iloc[0]) if len(rk) else UNKNOWN)
        res["rr_weather"].append((weather or {}).get(r.game_id, UNKNOWN))
    for c in FLAG_COLUMNS:
        out[c] = res[c]
    return out


def game_row(game_id: str) -> dict | None:
    if not GAMES_CSV.exists():
        return None
    with open(GAMES_CSV, newline="") as f:
        for r in csv.DictReader(f):
            if r["game_id"] == game_id:
                return r
    return None


def team_rush_rates(pbp: pd.DataFrame, as_of_week: int) -> tuple[dict, float | None]:
    p = clean_plays(pbp[pbp.week < as_of_week])
    p = p[(p.rush_attempt == 1) | (p.pass_attempt == 1)]
    if not len(p):
        return {}, None
    rr = p.groupby("posteam").rush_attempt.mean().to_dict()
    return rr, float(p.rush_attempt.mean())


def game_report(game_id: str, as_of_week: int | None = None, *, offline: bool = False, pbp_path=None, fetch=None,
                weather_sources=None) -> dict:
    assert_flags_only()
    away, home = teams_from_game_id(game_id)
    wk = int(as_of_week or int(game_id.split("_")[1]))
    pbp, psrc, ppull = load_pbp(pbp_path)
    pos = load_positions()
    roles, depth, run = DA.role_allowed(pbp, pos, wk), DA.depth_allowed(pbp, wk), DA.run_allowed(pbp, wk)
    prof = {t: DA.profile(t, wk, pbp, psrc, ppull, pos, roles=roles, depth=depth, run=run) for t in (away, home)}
    g = game_row(game_id) or {}
    weather: dict
    try:
        from pregame.weather import STADIUM, kickoff_utc  # read-only import; pregame/ is not modified
    except Exception:  # noqa: BLE001
        STADIUM, kickoff_utc = {}, None
    if offline and weather_sources is None:
        weather = dict(graded=False, status="SKIPPED_OFFLINE (unknown)", hours=[], sources=[])
    elif not g or kickoff_utc is None:
        weather = dict(graded=False, status=UNKNOWN, note="game not in games.csv", hours=[], sources=[])
    elif g.get("location") not in ("Home", "") or home not in STADIUM:
        weather = dict(graded=False, status="NOT_MAPPED (neutral/international site): check by hand", hours=[], sources=[])
    else:
        lat, lon = STADIUM[home]
        kw = dict(fetch=fetch) if fetch else {}
        weather = WG.grade_window(kickoff_utc(g["gameday"], g["gametime"]), lat, lon, g.get("roof"),
                                  sources=weather_sources, **kw)
    rr, lg = team_rush_rates(pbp, wk)
    tilt = {t: WG.run_tilt(weather, t, rr.get(t), lg) for t in (away, home)}
    players, team_t = TF.target_table(pbp)
    tf = {}
    for team, opp in ((away, home), (home, away)):
        recent = players[(players.posteam == team) & (players.week < wk)]
        ids = recent.groupby("gsis").targets.sum().sort_values(ascending=False)
        ids = [i for i in ids.index if pos.get(i) in ("WR", "TE")][:8]
        tf[team] = [dict(TF.evaluate(i, wk, pos.get(i), opp, players, team_t, roles), name=_name(pbp, i)) for i in ids]
    return dict(game_id=game_id, away=away, home=home, as_of_week=wk, approved=APPROVED, flags_only=True,
                cuts_enabled=dict(CUTS_ENABLED), projection_ready=False,
                built_utc=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                pbp_source=psrc, pbp_pulled=ppull, pbp_weeks=sorted(int(w) for w in pbp.week.dropna().unique()),
                targets_first=tf,
                defense_allowed={f"{t} defense (faces {away if t == home else home})": prof[t] for t in (away, home)},
                weather=weather, run_tilt=tilt)


def _name(pbp: pd.DataFrame, gsis: str) -> str:
    s = pbp.loc[pbp.receiver_player_id == gsis, "receiver_player_name"].dropna()
    return str(s.iloc[-1]) if len(s) else UNKNOWN


def _v(f):
    return f["value"] if isinstance(f, dict) and "value" in f else f


def render_md(rep: dict) -> str:
    L = [f"# Read rules (FLAGS ONLY) — {rep['game_id']}", "",
         f"Research only. projection_ready=false. Flags never cut a leg (cuts_enabled={rep['cuts_enabled']}). "
         f"Approved: {rep['approved']}. Built {rep['built_utc']}. PBP: {rep['pbp_source']} pulled {rep['pbp_pulled']}, "
         f"weeks present {rep['pbp_weeks'][0]}-{rep['pbp_weeks'][-1]} (later weeks not yet in the release).", "",
         "## 1. Targets first (last 4 prior games, need 3)", "",
         "| team | player | pos | share | team rank | games | status | note |", "|---|---|---|---|---|---|---|---|"]
    for team, rows in rep["targets_first"].items():
        for t in rows:
            L.append(f"| {team} | {t['name']} | {t['position']} | {t['share']} | {t['team_rank']} | {t['n_games']} | "
                     f"{t['status']} | {t.get('note', '')} |")
    L += ["", "## 2. Defense-allowed profile (weeks before this game; unknown = no data, never zero)", ""]
    for label, p in rep["defense_allowed"].items():
        c = p["coverage"]
        L += [f"### {label}", "",
              f"- Coverage (Sharp, pulled {c['mofc_pct']['pulled_at']}): MOF closed {_v(c['mofc_pct'])}%, "
              f"open {_v(c['mofo_pct'])}%, man {_v(c['man_pct'])}%, zone {_v(c['zone_pct'])}%",
              f"- Run defense: YPC {_v(p['run_defense']['ypc'])} (rank {_v(p['run_defense']['ypc_rank'])}, 1 = most allowed)",
              "", "| role | catches/g | yards/g | yds rank |", "|---|---|---|---|"]
        for role, f in p["by_role"].items():
            L.append(f"| {role} | {_v(f['rec_pg'])} | {_v(f['yds_pg'])} | {_v(f['yds_pg_rank'])} |")
        L += ["", "| depth | att | comp% | yards/g | rank |", "|---|---|---|---|---|"]
        for b, f in p["by_depth"].items():
            L.append(f"| {b} | {_v(f['att'])} | {_v(f['comp_pct'])} | {_v(f['yds_pg'])} | {_v(f['yds_pg_rank'])} |")
        dbs = _v(p["db_allowed"])
        L += ["", "DBs (PBU/INT/DPI verified; catches/yards INFERRED from first tackler):"]
        if dbs == UNKNOWN:
            L.append("- unknown")
        else:
            for d in dbs:
                L.append(f"- {d['name']} ({d['position']}): inferred {d['inferred_catches']} catches / "
                         f"{d['inferred_yards']:.0f} yds; verified PBU {d['pbu']}, INT {d['int']}, DPI {d['dpi']}")
        L.append(f"- Source: {p['db_allowed']['source']}, pulled {p['db_allowed']['pulled_at']}")
        L.append("")
    w = rep["weather"]
    L += ["## 3. Hourly weather grade (NWS + Open-Meteo only)", "", f"Status: {w.get('status')}", ""]
    if w.get("hours"):
        L += ["| hour (UTC) | NWS rain in/hr (grade) | NWS wind/gust | Open-Meteo rain in/hr (grade) | OM wind/gust | disagree |",
              "|---|---|---|---|---|---|"]
        for h in w["hours"]:
            n, o = h.get("nws", {}), h.get("open_meteo", {})
            L.append(f"| {h['hour_utc']} | {n.get('rain_in_hr')} ({n.get('rain_grade')}) | {n.get('wind_mph')}/{n.get('gust_mph')} | "
                     f"{o.get('rain_in_hr')} ({o.get('rain_grade')}) | {o.get('wind_mph')}/{o.get('gust_mph')} | {h['sources_disagree']} |")
        for s in w.get("sources", []):
            L.append(f"- {s.get('source')}: pulled {s.get('pulled_at')} ok={s.get('ok')}")
    L += ["", "Run-tilt reads (flag only):"] + [f"- {t}" for t in rep["run_tilt"].values()]
    return "\n".join(L) + "\n"


def write_report(rep: dict, out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    j = out_dir / f"READ_RULES_{rep['game_id']}.json"
    m = out_dir / f"READ_RULES_{rep['game_id']}.md"
    j.write_text(json.dumps(rep, indent=1, default=str) + "\n")
    m.write_text(render_md(rep))
    return j, m
