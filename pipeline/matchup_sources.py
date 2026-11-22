"""Main-defender matchup fields for the game-day check (refs NFL-47, refs NFL-56).

Fills the six fields `pipeline/ngs_matchup.py` lists as MISSING in public NGS, from sources that actually carry them,
under the newest-release rule. Nothing is estimated: a field with no source is MISSING / "unknown", never zero.

  field                  source                                              status when filled
  target_location        nflverse play-by-play (pass_location x pass_length,  FILLED (inherits the play_by_play
                         receiver targets), weeks before the target week       freshness row: FRESH / STALE / GAP)
  qb_pass_location       nflverse play-by-play (passer attempts by location,   FILLED (same)
                         completions, nflverse `success`, EPA)
  qb_success_vs_defense  nflverse play-by-play: QB success by zone next to     FILLED (same). Side by side only,
                         this defense's allowed success by the same zone       no blended number.
  receiver_routes,       nflverse pbp_participation `route` (season file),     FILLED when that season file exists;
  rb_routes              else a PFF capture with a routes column               the 2026 participation file was not
                                                                               published when this was written
  likely_defenders       PFF matchups tool capture (paid tier, browser)        PFF_PROJECTED (unverified) unless a row
                                                                               carries assignment evidence -> VERIFIED

PFF captures are read from a local folder outside the repo (PFF_MATCHUPS_DIR, default
/workspace/nfl-database/pff_matchups/<season>_w<WW>/receiver_matchups.csv). The repo is public and PFF is paid
content, so captures are never committed. Capture CSV columns (extra columns are kept as-is):
  season, week, receiver, receiver_team, receiver_position, opponent_team, listed_defender, defender_position,
  projected_snaps, source_url, source_update_et (PFF page header time), captured_et,
  [routes_run], [assignment_evidence]  (evidence = URL/file showing the defender actually covered him, e.g. charted)
Newest-release rule for PFF: a capture is FRESH when it is for the target week, has a PFF page-update stamp not later
than the capture time, and was captured after every earlier-week game finished. Another week -> STALE.
No capture -> MISSING.
"""
from __future__ import annotations

import csv
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
PFF_DIR_DEFAULT = "/workspace/nfl-database/pff_matchups"
PFF_URL = "https://www.pff.com/tools/matchups"
PBP_COLS = ["game_id", "season_type", "week", "posteam", "defteam", "play_type", "pass_attempt", "sack", "qb_spike",
            "two_point_attempt", "pass_location", "pass_length", "complete_pass", "success", "epa",
            "passer_player_id", "passer_player_name", "receiver_player_id", "receiver_player_name"]
FIELDS = ("receiver_routes", "rb_routes", "target_location", "qb_pass_location", "qb_success_vs_defense", "likely_defenders")


def _f(name, status, source, reason, value=None, as_of=None):
    return {"field": name, "status": status, "source": source, "reason": reason, "as_of": as_of,
            "value": "unknown" if value is None else value}


def _pbp_attempts(pbp_path, season, week):
    """Regular-season dropback pass attempts with a location, weeks strictly before `week`. None if unreadable."""
    try:
        import pandas as pd
        import pyarrow.parquet as pq
        cols = [c for c in PBP_COLS if c in pq.read_schema(pbp_path).names]
        d = pd.read_parquet(pbp_path, columns=cols)
    except Exception:
        return None
    need = {"week", "posteam", "defteam", "pass_location", "pass_length", "passer_player_id", "pass_attempt"}
    if not need <= set(d.columns):
        return None
    if "season_type" in d.columns:
        d = d[d["season_type"] == "REG"]
    d = d[(d["week"] < int(week)) & (d["pass_attempt"] == 1)]
    for c in ("sack", "qb_spike", "two_point_attempt"):
        if c in d.columns:
            d = d[d[c].fillna(0) != 1]
    d = d[d["pass_location"].notna() & d["pass_length"].notna()].copy()
    d["zone"] = d["pass_length"].astype(str) + "_" + d["pass_location"].astype(str)
    return d


def _zone_table(d, key_cols):
    """Counts and rates per zone. Rates are None (unknown) when n == 0; nothing is filled with zero."""
    out = {}
    for keys, g in d.groupby(key_cols + ["zone"], dropna=False):
        *k, zone = keys if isinstance(keys, tuple) else (keys,)
        n = int(len(g))
        row = {"att": n,
               "cmp": int(g["complete_pass"].fillna(0).sum()) if "complete_pass" in g else None,
               "success_rate": round(float(g["success"].mean()), 3) if "success" in g and g["success"].notna().any() else None,
               "epa_per_att": round(float(g["epa"].mean()), 3) if "epa" in g and g["epa"].notna().any() else None}
        out.setdefault(tuple(k) if len(k) > 1 else k[0], {})[zone] = row
    return out


def pbp_fields(pbp_path, teams, season, week, pbp_status="unknown", pbp_as_of=None):
    """target_location, qb_pass_location, qb_success_vs_defense from nflverse pbp. Status mirrors the pbp row."""
    src = f"nflverse play-by-play {season} (weeks 1-{int(week) - 1}, REG); {pbp_path}"
    if not pbp_path or not Path(pbp_path).is_file():
        return {k: _f(k, "MISSING", src, "No play-by-play file to read.") for k in
                ("target_location", "qb_pass_location", "qb_success_vs_defense")}
    d = _pbp_attempts(pbp_path, season, week)
    if d is None:
        return {k: _f(k, "MISSING", src, "Play-by-play unreadable or lacks pass_location/pass_length.") for k in
                ("target_location", "qb_pass_location", "qb_success_vs_defense")}
    status = "FILLED" if pbp_status == "FRESH" else (pbp_status if pbp_status in ("STALE", "GAP", "MISSING") else "MISSING")
    why = ("" if status == "FILLED" else f" Play-by-play freshness is {pbp_status}, so this field is not current.")
    away, home = teams
    opp = {away: home, home: away}
    tl, ql, qs = {}, {}, {}
    for team in teams:
        off = d[d["posteam"] == team]
        if "receiver_player_id" in off.columns:
            r = off[off["receiver_player_id"].notna()]
            names = r.groupby("receiver_player_id")["receiver_player_name"].first().to_dict()
            tab = _zone_table(r, ["receiver_player_id"])
            tl[team] = {f"{names.get(pid, pid)} ({pid})": z for pid, z in tab.items()}
        pn = off.groupby("passer_player_id")["passer_player_name"].first().to_dict()
        qtab = _zone_table(off, ["passer_player_id"])
        ql[team] = {f"{pn.get(pid, pid)} ({pid})": z for pid, z in qtab.items()}
        allowed = _zone_table(d[d["defteam"] == opp[team]], ["defteam"]).get(opp[team], {})
        qs[team] = {"opponent_defense": opp[team], "defense_allowed_by_zone": allowed,
                    "qbs": {q: {zone: {"qb": z, "defense_allowed": allowed.get(zone, "unknown")}
                                for zone, z in zones.items()} for q, zones in ql[team].items()},
                    "note": "Side by side only (QB's own rate | this defense's allowed rate, same zone). No blend."}
    return {
        "target_location": _f("target_location", status, src, "Receiver targets by pass_length x pass_location." + why, tl, pbp_as_of),
        "qb_pass_location": _f("qb_pass_location", status, src, "Passer attempts, completions, nflverse success and EPA by zone." + why, ql, pbp_as_of),
        "qb_success_vs_defense": _f("qb_success_vs_defense", status, src,
                                    "QB success by zone next to the opponent defense's allowed success by zone." + why, qs, pbp_as_of),
    }


def _parse_et(s):
    if not s:
        return None
    s = str(s).split(" (")[0].replace(" EST", "").replace(" EDT", "").replace(" ET", "").strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M"):
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=ET)
        except ValueError:
            continue
    try:
        d = datetime.fromisoformat(s)
        return d if d.tzinfo else d.replace(tzinfo=ET)
    except ValueError:
        return None


def pff_capture_path(season, week, base=None) -> Path:
    base = Path(base or os.environ.get("PFF_MATCHUPS_DIR") or PFF_DIR_DEFAULT)
    return base / f"{int(season)}_w{int(week):02d}" / "receiver_matchups.csv"


def pff_fields(teams, season, week, base=None, last_prior_game_end_et=None):
    """likely_defenders (and routes, if the capture has them) from a PFF matchups capture."""
    p = pff_capture_path(season, week, base)
    if not p.is_file():
        need = (f"No PFF matchups capture at {p}. Needs a signed-in browser pass on {PFF_URL} (Rico's PFF tier) for "
                f"week {int(week)}, saved with the columns in pipeline/matchup_sources.py.")
        return {"likely_defenders": _f("likely_defenders", "MISSING", PFF_URL, need)}, None
    with p.open(newline="") as fh:
        rows = [r for r in csv.DictReader(fh)
                if str(r.get("week", "")).strip() == str(int(week)) and str(r.get("season", "")).strip() == str(int(season))
                and (r.get("receiver_team") in teams or r.get("opponent_team") in teams)]
    upd = [_parse_et(r.get("source_update_et")) for r in rows]
    cap = [_parse_et(r.get("captured_et")) for r in rows]
    if not rows:
        return {"likely_defenders": _f("likely_defenders", "MISSING", str(p), "Capture has no rows for these teams in this week.")}, None
    problems = []
    if any(u is None for u in upd):
        problems.append("a row has no PFF page-update stamp (source_update_et)")
    if any(c is None for c in cap):
        problems.append("a row has no capture time (captured_et)")
    if not problems and any(u > c for u, c in zip(upd, cap)):
        problems.append("a PFF page-update stamp is after its capture time")
    if not problems and last_prior_game_end_et is not None and min(cap) < last_prior_game_end_et:
        problems.append("captured before the previous week's last game finished")
    as_of = max(u for u in upd if u).isoformat() if any(upd) else None
    if problems:
        return {"likely_defenders": _f("likely_defenders", "MISSING", str(p), "Capture not accepted: " + "; ".join(problems) + ".")}, as_of
    by_rec = {}
    for r in rows:
        ev = (r.get("assignment_evidence") or "").strip()
        by_rec.setdefault(f"{r.get('receiver')} ({r.get('receiver_team')} {r.get('receiver_position')})", []).append({
            "defender": r.get("listed_defender"), "defender_position": r.get("defender_position") or r.get("defender_position_as_shown"),
            "projected_snaps": r.get("projected_snaps") or "unknown",
            "status": "VERIFIED" if ev else "PFF_PROJECTED",
            "evidence": ev or "none: PFF projected candidate, not a confirmed assignment",
            "source_url": r.get("source_url") or PFF_URL, "source_update_et": r.get("source_update_et"),
            "captured_et": r.get("captured_et")})
    n_ver = sum(1 for v in by_rec.values() for x in v if x["status"] == "VERIFIED")
    st = "VERIFIED" if n_ver and all(x["status"] == "VERIFIED" for v in by_rec.values() for x in v) else (
        "PARTIAL_VERIFIED" if n_ver else "PFF_PROJECTED")
    out = {"likely_defenders": _f("likely_defenders", st, str(p),
                                  f"{len(by_rec)} receivers, {n_ver} defender rows with assignment evidence; the rest are "
                                  "PFF projected candidates (not verified, cannot back a receiving leg).", by_rec, as_of)}
    if any((r.get("routes_run") or "").strip() for r in rows):
        rt = {f"{r.get('receiver')} ({r.get('receiver_team')} {r.get('receiver_position')})": r.get("routes_run")
              for r in rows if (r.get("routes_run") or "").strip()}
        wr = {k: v for k, v in rt.items() if " RB)" not in k}
        rb = {k: v for k, v in rt.items() if " RB)" in k}
        if wr:
            out["receiver_routes"] = _f("receiver_routes", "FILLED", str(p), "Routes run as shown by PFF.", wr, as_of)
        if rb:
            out["rb_routes"] = _f("rb_routes", "FILLED", str(p), "RB routes run as shown by PFF.", rb, as_of)
    return out, as_of


def participation_routes(part_path, teams, season, week):
    """receiver_routes / rb_routes from nflverse pbp_participation `route`, if the season file exists."""
    src = f"nflverse pbp_participation {season}"
    if not part_path or not Path(part_path).is_file():
        why = (f"No {src} file. nflverse had not published the {season} participation release "
               "(releases/download/pbp_participation/pbp_participation_2026.parquet returned 404 on 2026-11-22).")
        return {k: _f(k, "MISSING", src, why) for k in ("receiver_routes", "rb_routes")}
    return {k: _f(k, "MISSING", src, "Participation file present but player-level route attribution is not wired yet.")
            for k in ("receiver_routes", "rb_routes")}


def fields(teams, season, week, pbp_path=None, pbp_status="unknown", pbp_as_of=None, part_path=None,
           pff_base=None, last_prior_game_end_et=None) -> dict:
    """All six main-defender fields with per-field status, source and as-of. Unfilled -> MISSING / unknown."""
    out = participation_routes(part_path, teams, season, week)
    out.update(pbp_fields(pbp_path, teams, season, week, pbp_status, pbp_as_of))
    pff, _ = pff_fields(teams, season, week, pff_base, last_prior_game_end_et)
    for k, v in pff.items():
        if k == "likely_defenders" or out.get(k, {}).get("status") == "MISSING":
            out[k] = v
    return {k: out[k] for k in FIELDS}
