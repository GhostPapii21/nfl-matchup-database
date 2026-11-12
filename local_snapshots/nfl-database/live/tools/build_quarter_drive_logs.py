#!/usr/bin/env python3
"""Build quarter_results + drive/3rd-down/RZ logs for a live NFL game folder.

Uses existing espn_summary JSON + pbp_live.csv + stored r6 odds CSVs.
No new paid odds pulls.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import re
from collections import defaultdict
from pathlib import Path

BASE = Path("/workspace/nfl-database/live/2026-11-05_JAX_BAL")
R6_ODDS = Path("/workspace/nfl-database/runs/2026-11-05_JAX@BAL_r6/odds")
EVENT = "401873037"


def now_et() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S ET")


def load_odds(path: Path) -> list[dict]:
    with path.open() as f:
        return list(csv.DictReader(f))


def grade_spread(side_team, line, away_pts, home_pts, away_team, home_team):
    if side_team == away_team:
        adj = away_pts + float(line) - home_pts
    else:
        adj = home_pts + float(line) - away_pts
    if abs(adj) < 1e-9:
        return "P", 0.0
    return ("W" if adj > 0 else "L"), adj


def grade_ml(side_team, away_pts, home_pts, away_team, home_team):
    if away_pts == home_pts:
        return "P"
    winner = away_team if away_pts > home_pts else home_team
    return "W" if side_team == winner else "L"


def qscore(teams, side, q):
    ls = teams[side]["linescores"]
    return ls[q - 1] if len(ls) >= q else None


def main() -> None:
    NOW = now_et()
    meta = json.loads((BASE / "live_meta.json").read_text())
    summary = json.loads((BASE / "raw" / f"espn_summary_{EVENT}.json").read_text())
    hc = summary["header"]["competitions"][0]
    status = hc["status"]["type"]
    status_detail = status.get("detail") or status.get("description")
    state = status.get("state")
    period = hc["status"].get("period")

    teams = {}
    for c in hc["competitors"]:
        ls_raw = c.get("linescores") or []
        ls = []
        for x in ls_raw:
            if isinstance(x, dict):
                ls.append(int(float(x.get("value") or x.get("displayValue") or 0)))
            else:
                ls.append(int(float(x)))
        teams[c["homeAway"]] = {
            "abbrev": c["team"]["abbreviation"],
            "score": int(c.get("score") or 0),
            "linescores": ls,
            "id": str(c["team"]["id"]),
        }
    away, home = teams["away"]["abbrev"], teams["home"]["abbrev"]

    # Halftime still has ESPN state=in + period=2; treat it as end of Q2/H1.
    status_name = (status.get("name") or "").upper()
    is_halftime = status_name == "STATUS_HALFTIME" or "halftime" in (status_detail or "").lower()

    # ---- Quarter rows ----
    q_rows = []
    for q in range(1, 5):
        aq, hq = qscore(teams, "away", q), qscore(teams, "home", q)
        finalized = in_progress = False
        if state == "post":
            finalized = True
        elif is_halftime and period is not None and q <= int(period):
            finalized = True
        elif period is not None:
            if q < int(period):
                finalized = True
            elif q == int(period) and state == "in":
                in_progress = True
        if aq is None and hq is None and not finalized and not in_progress:
            q_rows.append(
                {
                    "game_id": EVENT,
                    "game_date": "2026-11-05",
                    "away_team": away,
                    "home_team": home,
                    "quarter": q,
                    "status": "not_started",
                    "as_of_et": NOW,
                    "game_clock": status_detail,
                    "away_q_points": "",
                    "home_q_points": "",
                    "q_margin_away_minus_home": "",
                    "quarter_winner": "",
                    "quarter_leader_in_progress": "",
                    "cum_away_score": "",
                    "cum_home_score": "",
                    "cum_leader": "",
                    "score_source": "espn_header_linescores",
                    "notes": "Independent quarter points from linescores; distinct from cumulative game lead",
                }
            )
            continue
        aq = 0 if aq is None else aq
        hq = 0 if hq is None else hq
        cum_a = sum(teams["away"]["linescores"][:q]) if teams["away"]["linescores"] else 0
        cum_h = sum(teams["home"]["linescores"][:q]) if teams["home"]["linescores"] else 0
        if finalized:
            status_q = "final"
            winner = away if aq > hq else home if hq > aq else "TIE"
            leader = ""
        elif in_progress:
            status_q = "in_progress"
            winner = ""
            leader = away if aq > hq else home if hq > aq else "TIE"
        else:
            status_q = "not_started"
            winner = leader = ""
        q_rows.append(
            {
                "game_id": EVENT,
                "game_date": "2026-11-05",
                "away_team": away,
                "home_team": home,
                "quarter": q,
                "status": status_q,
                "as_of_et": NOW,
                "game_clock": status_detail,
                "away_q_points": aq,
                "home_q_points": hq,
                "q_margin_away_minus_home": aq - hq,
                "quarter_winner": winner,
                "quarter_leader_in_progress": leader,
                "cum_away_score": cum_a,
                "cum_home_score": cum_h,
                "cum_leader": away if cum_a > cum_h else home if cum_h > cum_a else "TIE",
                "score_source": "espn_header_linescores",
                "notes": "Independent quarter points from linescores; distinct from cumulative game lead",
            }
        )

    q1 = next(r for r in q_rows if r["quarter"] == 1)
    q1_away, q1_home = int(q1["away_q_points"]), int(q1["home_q_points"])

    # ---- Period line grades from stored r6 odds ----
    snapshots = [
        ("odds_jaxbal_game", R6_ODDS / "odds_jaxbal_game.csv", "pregame", "2026-11-04T19:59:57Z"),
        ("odds_r6", R6_ODDS / "odds_r6.csv", "pregame", "2026-11-04T19:59:57Z"),
        ("odds_live_fd_2026-11-05", R6_ODDS / "odds_live_fd_2026-11-05.csv", "pregame_same_day", "2026-11-05T17:35:33Z"),
        (
            "odds_post_inactives_fd_1902",
            R6_ODDS / "odds_post_inactives_fd_2026-11-05_1902.csv",
            "pregame_post_inactives",
            "2026-11-06T00:04:02Z",
        ),
    ]
    period_line_grades = []
    seen = set()
    for snap_name, path, timing, pulled in snapshots:
        if not path.exists():
            continue
        for r in load_odds(path):
            mkt = r["market"]
            if mkt not in ("spreads_q1", "h2h_q1", "spreads_h1", "h2h_h1"):
                continue
            side = r["side"]
            team = "JAX" if "Jaguar" in side else ("BAL" if "Raven" in side else side)
            key = (snap_name, mkt, team, r.get("point") or "", r["book"])
            if key in seen:
                continue
            seen.add(key)
            point = r.get("point") or ""
            price = r.get("price") or ""
            if mkt.endswith("_q1"):
                per = "Q1"
            elif mkt.endswith("_h1"):
                per = "H1"
            else:
                per = mkt
            result = ""
            margin = ""
            denom = ""
            gradeable = "0"
            if per == "Q1" and q1["status"] == "final":
                gradeable = "1"
                if mkt.startswith("spreads"):
                    res, mar = grade_spread(team, float(point), q1_away, q1_home, away, home)
                    result, margin, denom = res, f"{mar:.1f}", "ats_q1"
                else:
                    result = grade_ml(team, q1_away, q1_home, away, home)
                    margin = str(q1_away - q1_home)
                    denom = "score_only_q1_ml"
            elif per == "H1":
                denom = "ats_h1" if mkt.startswith("spreads") else "score_only_h1_ml"
                # H1 settles at halftime or once Q3+ is underway / game over.
                half_final = bool(
                    is_halftime
                    or state == "post"
                    or (period is not None and int(period) >= 3)
                )
                h1_away = sum(teams["away"]["linescores"][:2]) if len(teams["away"]["linescores"]) >= 2 else None
                h1_home = sum(teams["home"]["linescores"][:2]) if len(teams["home"]["linescores"]) >= 2 else None
                if half_final and h1_away is not None and h1_home is not None:
                    gradeable = "1"
                    if mkt.startswith("spreads"):
                        res, mar = grade_spread(team, float(point), h1_away, h1_home, away, home)
                        result, margin = res, f"{mar:.1f}"
                    else:
                        result = grade_ml(team, h1_away, h1_home, away, home)
                        margin = str(h1_away - h1_home)
                else:
                    result = "IN_PROGRESS" if state == "in" else "PENDING"
            period_line_grades.append(
                {
                    "game_id": EVENT,
                    "snapshot_id": snap_name,
                    "line_timing": timing,
                    "snapshot_pulled_utc": pulled,
                    "snapshot_last_update_utc": r.get("last_update_utc", ""),
                    "book": r["book"],
                    "market": mkt,
                    "period": per,
                    "selection_team": team,
                    "line_point": point,
                    "price_american": price,
                    "source_file": str(path),
                    "is_in_play_line": "0",
                    "result_W_L_P": result,
                    "cover_margin_or_score_diff": margin,
                    "denominator_type": denom,
                    "gradeable_now": gradeable,
                    "q1_away_pts": q1_away,
                    "q1_home_pts": q1_home,
                    "graded_as_of_et": NOW,
                    "notes": "No new odds pull; graded from stored r6 snapshots only. Pregame vs post-inactives distinguished via line_timing.",
                }
            )

    # ---- Drives ----
    drives_obj = summary.get("drives") or {}
    drives_prev = list(drives_obj.get("previous") or [])
    drives_cur = drives_obj.get("current")
    # ESPN often keeps the current drive in `previous` as well — dedupe by id
    seen_ids = set()
    all_drives = []
    for dr in drives_prev + ([drives_cur] if drives_cur else []):
        did = dr.get("id")
        if did is not None and did in seen_ids:
            continue
        if did is not None:
            seen_ids.add(did)
        all_drives.append(dr)
    cur_id = (drives_cur or {}).get("id")

    drive_rows = []
    third_rows = []
    rz_rows = []
    team_agg = {away: defaultdict(float), home: defaultdict(float)}

    for idx, dr in enumerate(all_drives, 1):
        off = ((dr.get("team") or {}).get("abbreviation")) or ""
        ongoing = bool(drives_cur) and (
            (cur_id is not None and dr.get("id") == cur_id) or (cur_id is None and dr is drives_cur)
        )
        result_desc = dr.get("displayResult") or dr.get("result") or ""
        desc = dr.get("description") or ""
        plays = dr.get("plays") or []
        top = dr.get("timeElapsed") or dr.get("timeOfPossession") or ""
        if isinstance(top, dict):
            top = top.get("displayValue") or ""
        top_sec = ""
        if isinstance(top, str) and ":" in top:
            mm, ss = top.split(":")[:2]
            try:
                top_sec = int(mm) * 60 + int(ss)
            except ValueError:
                top_sec = ""
        start = dr.get("start") or {}
        end = dr.get("end") or {}
        start_yl = start.get("text") or start.get("downDistanceText") or ""
        end_yl = end.get("text") or end.get("downDistanceText") or ""
        yards = dr.get("yards") if dr.get("yards") is not None else ""
        nplays = dr.get("offensivePlays")
        if nplays is None:
            nplays = len(plays)
        period_start = start.get("period")
        if isinstance(period_start, dict):
            period_start = period_start.get("number", "")
        clock_start = start.get("clock")
        if isinstance(clock_start, dict):
            clock_start = clock_start.get("displayValue", "")

        third_att = third_conv = no_play_pens = 0
        rz_entered = rz_td = rz_fg = False

        for p in plays:
            text = p.get("text") or ""
            st = p.get("start") or {}
            endp = p.get("end") or {}
            down = st.get("down")
            dist = st.get("distance")
            yte = st.get("yardsToEndzone")
            down_raw = st.get("down")
            # Official Timeout / clock stoppages often have yardsToEndzone=0 — not RZ
            is_clock_stop = (
                down_raw in (-1, "-1")
                or "Official Timeout" in text
                or text.strip().startswith("Timeout")
            )
            if (
                not is_clock_stop
                and yte is not None
                and 1 <= int(yte) <= 20
            ):
                rz_entered = True
            if "No Play" in text:
                no_play_pens += 1
            if down == 3 and not is_clock_stop:
                if "No Play" in text:
                    third_rows.append(
                        {
                            "game_id": EVENT,
                            "drive_num": idx,
                            "offense": off,
                            "quarter": (p.get("period") or {}).get("number", ""),
                            "clock": (p.get("clock") or {}).get("displayValue", ""),
                            "down_distance": f"3rd & {dist}",
                            "yards_to_endzone": yte if yte is not None else "",
                            "play_text": text,
                            "converted": "NA_NO_PLAY",
                            "source": "espn_drive_play",
                            "notes": "Penalty/no-play; excluded from conversion denominator",
                        }
                    )
                    continue
                third_att += 1
                converted = False
                # INT / turnover on downs ≠ conversion (known false-positive path)
                if re.search(r"intercept", text, re.I):
                    converted = False
                elif p.get("scoringPlay") and "TOUCHDOWN" in text.upper() and "No Play" not in text:
                    converted = True
                else:
                    stat_y = p.get("statYardage")
                    if stat_y is None:
                        m = re.search(r"for (-?\d+) yards?", text)
                        stat_y = int(m.group(1)) if m else None
                    if dist is not None and stat_y is not None and stat_y >= dist:
                        converted = True
                    if endp.get("down") == 1 and st.get("down") == 3:
                        converted = True
                    # first-down language
                    if re.search(r"first down|1ST DOWN", text, re.I):
                        converted = True
                if converted:
                    third_conv += 1
                third_rows.append(
                    {
                        "game_id": EVENT,
                        "drive_num": idx,
                        "offense": off,
                        "quarter": (p.get("period") or {}).get("number", ""),
                        "clock": (p.get("clock") or {}).get("displayValue", ""),
                        "down_distance": f"3rd & {dist}",
                        "yards_to_endzone": yte if yte is not None else "",
                        "play_text": text,
                        "converted": "1" if converted else "0",
                        "source": "espn_drive_play_derived",
                        "notes": "Derived from yards vs distance / TD / resulting 1st; not ESPN boxstat",
                    }
                )
            if rz_entered and p.get("scoringPlay") and "No Play" not in text:
                if "TOUCHDOWN" in text.upper():
                    rz_td = True
                if "field goal" in text.lower() and "GOOD" in text.upper():
                    rz_fg = True

        res_u = (result_desc or "").upper()
        if "TOUCHDOWN" in res_u and rz_entered:
            rz_td = True
        if "FIELD GOAL" in res_u and rz_entered:
            rz_fg = True

        if rz_entered:
            if rz_td:
                trip_result = "TD"
            elif rz_fg:
                trip_result = "FG"
            elif ongoing:
                trip_result = "ONGOING"
            else:
                trip_result = result_desc or "NO_SCORE"
            rz_rows.append(
                {
                    "game_id": EVENT,
                    "drive_num": idx,
                    "offense": off,
                    "trip_result": trip_result,
                    "td": "1" if rz_td else "0",
                    "fg": "1" if rz_fg else "0",
                    "ongoing_drive": "1" if ongoing else "0",
                    "drive_result": result_desc,
                    "source": "espn_drives+plays",
                    "notes": "FG separate from TD; trip=any play yardsToEndzone<=20",
                }
            )

        drive_rows.append(
            {
                "game_id": EVENT,
                "drive_num": idx,
                "offense": off,
                "ongoing": "1" if ongoing else "0",
                "result": result_desc,
                "description": desc,
                "time_of_possession": top if isinstance(top, str) else "",
                "top_seconds": top_sec,
                "plays": nplays,
                "yards": yards,
                "start": start_yl,
                "end": end_yl,
                "period_start": period_start,
                "clock_start": clock_start,
                "third_down_att": third_att,
                "third_down_conv": third_conv,
                "no_play_penalties": no_play_pens,
                "red_zone_trip": "1" if rz_entered else "0",
                "red_zone_td": "1" if rz_td else "0",
                "red_zone_fg": "1" if rz_fg else "0",
                "source": "espn_site_summary.drives",
                "as_of_et": NOW,
                "game_status": status_detail,
            }
        )

        if off in team_agg:
            if top_sec != "":
                team_agg[off]["top_seconds"] += float(top_sec)
            team_agg[off]["drives"] += 0 if ongoing else 1
            team_agg[off]["drives_all"] += 1
            team_agg[off]["third_att"] += third_att
            team_agg[off]["third_conv"] += third_conv
            team_agg[off]["rz_trips"] += 1 if rz_entered else 0
            team_agg[off]["rz_td"] += 1 if rz_td else 0
            team_agg[off]["rz_fg"] += 1 if rz_fg else 0
            team_agg[off]["no_play_pens"] += no_play_pens

    # Boxscore comparison
    box_third = {}
    box_top = {}
    for tstat in (summary.get("boxscore") or {}).get("teams") or []:
        abbr = ((tstat.get("team") or {}).get("abbreviation")) or ""
        for cat in tstat.get("statistics") or []:
            name = (cat.get("name") or "").lower()
            dn = (cat.get("displayName") or "").lower()
            val = cat.get("displayValue") or cat.get("value")
            if "thirddown" in name.replace("_", "") or "3rd down" in dn:
                box_third[abbr] = val
            if "possession" in name or "possession" in dn or "timeofposs" in name.replace("_", ""):
                box_top[abbr] = val

    def write_csv(path: Path, rows: list[dict]) -> None:
        if not rows:
            path.write_text("")
            return
        with path.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

    write_csv(BASE / "quarter_results.csv", q_rows)
    write_csv(BASE / "period_line_grades.csv", period_line_grades)
    write_csv(BASE / "drive_log.csv", drive_rows)
    write_csv(BASE / "third_down_log.csv", third_rows)
    write_csv(BASE / "red_zone_log.csv", rz_rows)

    # Team summary rows
    team_rows = []
    for tm in (away, home):
        a = team_agg[tm]
        top_s = int(a["top_seconds"])
        team_rows.append(
            {
                "game_id": EVENT,
                "team": tm,
                "as_of_et": NOW,
                "game_status": status_detail,
                "top_seconds_sum_drives": top_s,
                "top_mmss_sum_drives": f"{top_s//60}:{top_s%60:02d}",
                "boxscore_possession": box_top.get(tm, "NA"),
                "drives_completed": int(a["drives"]),
                "drives_including_ongoing": int(a["drives_all"]),
                "third_down_conv": int(a["third_conv"]),
                "third_down_att": int(a["third_att"]),
                "third_down_pct_derived": round(100 * a["third_conv"] / a["third_att"], 1) if a["third_att"] else "",
                "boxscore_third_down": box_third.get(tm, "NA"),
                "rz_trips": int(a["rz_trips"]),
                "rz_td": int(a["rz_td"]),
                "rz_fg": int(a["rz_fg"]),
                "no_play_penalties": int(a["no_play_pens"]),
                "notes": "3rd-down derived from PBP; compare to boxscore when present",
            }
        )
    write_csv(BASE / "team_conversion_summary.csv", team_rows)


    # ---- Markdown quarter_results.md ----
    lines = []
    lines.append("# Quarter results — JAX @ BAL (TNF 2026-11-05)")
    lines.append("")
    lines.append(f"- As of: **{NOW}** (America/New_York)")
    lines.append(f"- Game status: **{status_detail}** (state={state})")
    lines.append(f"- Scoreboard: **{away} {teams['away']['score']} – {home} {teams['home']['score']}**")
    lines.append(f"- Source: ESPN header linescores + drives (`{EVENT}`)")
    lines.append("- Independent quarter points are separate from cumulative game lead.")
    lines.append("")
    lines.append("## Quarter board")
    lines.append("")
    lines.append("| Q | Status | JAX Q pts | BAL Q pts | Q winner / in-progress leader | Cum JAX | Cum BAL | Cum leader |")
    lines.append("|---|--------|----------:|----------:|-------------------------------|--------:|--------:|------------|")
    for r in q_rows:
        if r["status"] == "not_started":
            wl = "—"
            aq = hq = ca = ch = cl = "—"
        else:
            if r["status"] == "final":
                wl = r["quarter_winner"]
            else:
                wl = f"{r['quarter_leader_in_progress']} (in progress)"
            aq, hq = r["away_q_points"], r["home_q_points"]
            ca, ch, cl = r["cum_away_score"], r["cum_home_score"], r["cum_leader"]
        lines.append(f"| {r['quarter']} | {r['status']} | {aq} | {hq} | {wl} | {ca} | {ch} | {cl} |")
    lines.append("")
    lines.append("## Stored period-line grades (no new odds pull)")
    lines.append("")
    lines.append("Primary leg of interest: **JAX 1Q -2.5** from r6 stored FanDuel/DK/Pinnacle snapshots.")
    lines.append("")
    lines.append(f"Q1 final (independent): **JAX {q1_away} – BAL {q1_home}** → margin JAX +{q1_away-q1_home}.")
    lines.append("")
    # highlight JAX -2.5 rows
    lines.append("| Snapshot | Timing | Book | Market | Sel | Line | Price | Result | Denominator |")
    lines.append("|----------|--------|------|--------|-----|------|------:|--------|-------------|")
    for r in period_line_grades:
        if r["selection_team"] == "JAX" and r["period"] in ("Q1", "H1"):
            lines.append(
                f"| {r['snapshot_id']} | {r['line_timing']} | {r['book']} | {r['market']} | {r['selection_team']} | {r['line_point'] or 'ML'} | {r['price_american']} | **{r['result_W_L_P']}** | {r['denominator_type']} |"
            )
    lines.append("")
    lines.append("In-play period lines: **NA** (not stored; no new pull).")
    lines.append("")
    lines.append("### Aggregation schema notes")
    lines.append("- `denominator_type=ats_q1` → include in ATS W/L/P counts for quarter spreads.")
    lines.append("- `denominator_type=score_only_q1_ml` → moneyline / score-only period winner counts.")
    lines.append("- `gradeable_now=0` rows (H1 before halftime) excluded from settled denominators; H1 grades settle at STATUS_HALFTIME.")
    lines.append("- One game is a sample of 1; no predictive claim.")
    lines.append("")
    lines.append("## Possession / drives / conversions (both teams)")
    lines.append("")
    lines.append("| Team | TOP sum (drives) | Box TOP | 3rd conv/att (derived) | Box 3rd | RZ trips | RZ TD | RZ FG | Completed drives |")
    lines.append("|------|------------------|---------|------------------------|---------|----------|------:|------:|------------------|")
    for tr in team_rows:
        lines.append(
            f"| {tr['team']} | {tr['top_mmss_sum_drives']} | {tr['boxscore_possession']} | {tr['third_down_conv']}/{tr['third_down_att']} ({tr['third_down_pct_derived']}%) | {tr['boxscore_third_down']} | {tr['rz_trips']} | {tr['rz_td']} | {tr['rz_fg']} | {tr['drives_completed']} |"
        )
    lines.append("")
    disc = []
    for tr in team_rows:
        if tr["boxscore_third_down"] not in ("", "NA", None) and tr["third_down_att"]:
            disc.append(
                f"- {tr['team']}: derived 3rd-down {tr['third_down_conv']}/{tr['third_down_att']} vs boxscore `{tr['boxscore_third_down']}`"
            )
        if tr["boxscore_possession"] not in ("", "NA", None):
            disc.append(
                f"- {tr['team']}: drive-sum TOP {tr['top_mmss_sum_drives']} vs boxscore `{tr['boxscore_possession']}` (ongoing drive / kickoffs may differ)"
            )
    lines.append("### Source vs derived")
    if disc:
        lines.extend(disc)
    else:
        lines.append("- Boxscore third-down / possession fields not present or NA in this summary snapshot; derived PBP values stand alone.")
    lines.append("- 3rd-down conversions are **derived** from drive plays (yards ≥ distance, TD, or resulting 1st). NA_NO_PLAY rows excluded.")
    lines.append("- Red-zone trip = any play with `yardsToEndzone` in 1–20 (Official Timeout / yte=0 excluded). FG counted separately from TD; long FGs from outside the RZ are not RZ trips.")
    ongoing = [d for d in drive_rows if d["ongoing"] == "1"]
    if ongoing:
        o = ongoing[0]
        lines.append(
            f"- **Ongoing drive:** #{o['drive_num']} {o['offense']} — result=`{o['result'] or 'in progress'}`, 3rd={o['third_down_conv']}/{o['third_down_att']}, RZ={o['red_zone_trip']}"
        )
    lines.append("")
    lines.append("Files: `quarter_results.csv`, `period_line_grades.csv`, `drive_log.csv`, `third_down_log.csv`, `red_zone_log.csv`, `team_conversion_summary.csv`.")
    (BASE / "quarter_results.md").write_text("\n".join(lines) + "\n")

    # drive_conversions.md short
    dlines = [
        "# Drive / conversion log — JAX @ BAL",
        "",
        f"- As of: **{NOW}** · {status_detail}",
        "",
        "| # | Off | Ongoing | Result | TOP | Plays | Yds | 3rd | RZ trip/TD/FG | No-play pens |",
        "|---|-----|---------|--------|-----|------:|----:|-----|---------------|--------------|",
    ]
    for d in drive_rows:
        dlines.append(
            f"| {d['drive_num']} | {d['offense']} | {d['ongoing']} | {d['result'] or '—'} | {d['time_of_possession'] or '—'} | {d['plays']} | {d['yards']} | {d['third_down_conv']}/{d['third_down_att']} | {d['red_zone_trip']}/{d['red_zone_td']}/{d['red_zone_fg']} | {d['no_play_penalties']} |"
        )
    (BASE / "drive_conversions.md").write_text("\n".join(dlines) + "\n")

    # compact stdout summary
    out = {
        "as_of_et": NOW,
        "status": status_detail,
        "score": f"{away} {teams['away']['score']}-{home} {teams['home']['score']}",
        "q1": f"{away} {q1_away}-{home} {q1_home} winner={q1['quarter_winner']}",
        "q2": next(r for r in q_rows if r["quarter"] == 2),
        "jax_q1_spread_grades": [
            r
            for r in period_line_grades
            if r["selection_team"] == "JAX" and r["market"] == "spreads_q1"
        ],
        "team_rows": team_rows,
        "n_drives": len(drive_rows),
        "n_third": len(third_rows),
        "n_rz": len(rz_rows),
    }
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
