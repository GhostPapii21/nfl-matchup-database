"""Markdown brief for one packet: the same numbers as packet.json, laid out for a person or a chat model."""
from __future__ import annotations


def f(v, d=1, pct=False):
    if v is None:
        return "n/a"
    return f"{100 * v:.{d}f}%" if pct else (f"{v:.{d}f}" if isinstance(v, float) else str(v))


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def rk(rank, key):
    r = rank.get(key)
    return f"{r['rank']}/{r['of']}" if r else "n/a"


DEF_ROWS = [("Points allowed / game", "points_pg", 1, False), ("Pass yards allowed / game", "pass_yards_pg", 1, False),
            ("Yards per pass attempt allowed", "yards_per_pass_attempt", 2, False), ("Rush yards allowed / game", "rush_yards_pg", 1, False),
            ("Yards per carry allowed", "yards_per_carry", 2, False), ("RB rush yards allowed / game", "rb_rush_yards_pg", 1, False),
            ("WR yards allowed / game", "wr_rec_yards_pg", 1, False), ("WR receptions allowed / game", "wr_receptions_pg", 1, False),
            ("TE yards allowed / game", "te_rec_yards_pg", 1, False), ("TE receptions allowed / game", "te_receptions_pg", 1, False),
            ("RB receiving yards allowed / game", "rb_rec_yards_pg", 1, False), ("RB receptions allowed / game", "rb_receptions_pg", 1, False),
            ("Explosive passes (20+) allowed / game", "explosive_pass_pg", 2, False), ("Explosive runs (15+) allowed / game", "explosive_rush_pg", 2, False),
            ("Sack rate", "sack_rate", 1, True), ("Pressure rate (sacks + hits)", "pressure_rate", 1, True),
            ("Third-down conversions allowed", "third_down_rate", 1, True), ("Red-zone TD rate allowed", "red_zone_td_rate", 1, True),
            ("Takeaways / game", "takeaways_pg", 2, False)]
OFF_ROWS = [("Points / game", "points_pg", 1, False), ("Pass yards / game", "pass_yards_pg", 1, False), ("Yards per pass attempt", "yards_per_pass_attempt", 2, False),
            ("Rush yards / game", "rush_yards_pg", 1, False), ("Yards per carry", "yards_per_carry", 2, False), ("RB rush yards / game", "rb_rush_yards_pg", 1, False),
            ("WR yards / game", "wr_rec_yards_pg", 1, False), ("TE yards / game", "te_rec_yards_pg", 1, False), ("RB receiving yards / game", "rb_rec_yards_pg", 1, False),
            ("Explosive passes (20+) / game", "explosive_pass_pg", 2, False), ("Explosive runs (15+) / game", "explosive_rush_pg", 2, False),
            ("Sack rate allowed", "sack_rate", 1, True), ("Pressure rate allowed (sacks + hits)", "pressure_rate", 1, True),
            ("Third-down conversion rate", "third_down_rate", 1, True), ("Red-zone TD rate", "red_zone_td_rate", 1, True)]


def team_section(team, t):
    if "defense" not in t:
        return f"## {team}\n\nNo completed games this season: {t.get('status')}.\n"
    d, o, w = t["defense"], t["offense"], t["window"]
    L = [f"## {team} (last {w['games']} games: weeks {', '.join(map(str, w['weeks']))})", ""]
    L += [f"### {team} defense: what it allows (rank 1 = best defense)", "",
          table(["Metric", "Value", "Rank", "League avg"], [[lab, f(d["allowed"].get(k), dd, pc), rk(d["rank"], k),
                f((d["rank"].get(k) or {}).get("league_avg"), dd, pc)] for lab, k, dd, pc in DEF_ROWS]), ""]
    a = d["allowed"]
    L += [f"Blitz rate {f(a.get('blitz_rate'), 1, True)} and play-action faced {f(a.get('play_action_rate'), 1, True)} on {a.get('dropbacks_charted')} charted dropbacks (FTN). "
          f"Deep passes (20+ air yards) faced {f(a.get('deep_attempts_pg'))} per game, {f(a.get('deep_completion_rate'), 1, True)} completed.", ""]
    L += [f"### {team} defense, game by game", "",
          table(["Wk", "Opp", "Pts", "Pass yds", "Rush yds", "RB rush", "WR rec-yds", "TE rec-yds", "RB rec-yds", "Expl pass", "Expl run", "Sacks"],
                [[g["week"], g["opp"], f(g["points"]), g["pass_yards"], g["rush_yards"], g["rb_rush_yards"],
                  f"{g['wr_receptions']}-{g['wr_rec_yards']}", f"{g['te_receptions']}-{g['te_rec_yards']}", f"{g['rb_receptions']}-{g['rb_rec_yards']}",
                  g["explosive_pass"], g["explosive_rush"], g["sacks"]] for g in d["by_game"]]), ""]
    L += [f"### Best individual lines allowed by {team}", "",
          table(["Wk", "Opp", "Top receiver", "Top rusher"],
                [[x["week"], x["opp"],
                  (lambda r: f"{r['player']} ({r['pos'] or '?'}) {r['receptions']}/{r['targets']} for {r['yards']}, {r['td']} TD" if r else "n/a")(x.get("top_receiver")),
                  (lambda r: f"{r['player']} ({r['pos'] or '?'}) {r['carries']} for {r['yards']}, {r['td']} TD" if r else "n/a")(x.get("top_rusher"))]
                 for x in d["top_lines_allowed"]]), ""]
    if d["run_defense_by_direction"]:
        L += [f"### {team} run defense by direction", "", table(["Direction", "Carries", "Yards", "YPC", "15+"],
              [[r["direction"], r["carries"], r["yards"], r["ypc"], r["explosive"]] for r in d["run_defense_by_direction"]]), ""]
    dv = d["defenders"]
    if dv.get("coverage"):
        L += [f"### {team} defenders in coverage (Pro Football Reference)", "",
              table(["Defender", "G", "Targets", "Comp", "Yards", "Yds/tgt", "TD", "INT", "Missed tkl"],
                    [[r["player"], r["games"], r["targets"], r["completions"], r["yards"], f(r["yards_per_target"], 1), r["td_allowed"], r["interceptions"], r["missed_tackles"]] for r in dv["coverage"]]), ""]
    if dv.get("pass_rush"):
        L += [f"### {team} pass rushers", "", table(["Defender", "G", "Pressures", "Sacks", "Hurries", "Blitzes"],
              [[r["player"], r["games"], r["pressures"], r["sacks"], r["hurries"], r["blitzes"]] for r in dv["pass_rush"]]), ""]
    L += [f"### {team} offense: what it produces (rank 1 = best offense)", "",
          table(["Metric", "Value", "Rank", "League avg"], [[lab, f(o["produced"].get(k), dd, pc), rk(o["rank"], k),
                f((o["rank"].get(k) or {}).get("league_avg"), dd, pc)] for lab, k, dd, pc in OFF_ROWS]), ""]
    pr = o["produced"]
    L += [f"Neutral-situation pass rate {f(pr.get('neutral_pass_rate'), 1, True)}; {f(pr.get('plays_pg'))} plays per game; "
          f"target share WR {f(pr.get('wr_target_share'), 0, True)} / TE {f(pr.get('te_target_share'), 0, True)} / RB {f(pr.get('rb_target_share'), 0, True)}.", ""]
    L += [f"### {team} offense, game by game", "",
          table(["Wk", "Opp", "Pts", "Pass yds", "Rush yds", "RB rush", "WR rec-yds", "TE rec-yds", "RB rec-yds", "Expl pass", "Expl run", "Sacks taken"],
                [[g["week"], g["opp"], f(g["points"]), g["pass_yards"], g["rush_yards"], g["rb_rush_yards"],
                  f"{g['wr_receptions']}-{g['wr_rec_yards']}", f"{g['te_receptions']}-{g['te_rec_yards']}", f"{g['rb_receptions']}-{g['rb_rec_yards']}",
                  g["explosive_pass"], g["explosive_rush"], g["sacks"]] for g in o["by_game"]]), ""]
    P = o["players"]
    for q in P["quarterbacks"]:
        L += [f"**QB {q['player']}** ({q['games']} games): {q['completions']}/{q['attempts']}, {q['yards']} yds, {q['td']} TD, {q['int']} INT, {q['sacks']} sacks, "
              f"{f(q['yards_per_attempt'], 2)} yds/att, depth of target {f(q['avg_depth_of_target'])}, pressured on {f(q['pressure_rate_faced'], 1, True)} of dropbacks. "
              "Yards by game: " + ", ".join(f"W{g['week']} {g['yards']}" for g in q["log"]) + ".", ""]
    L += [f"### {team} receivers", "",
          table(["Player", "Pos", "G", "Tgt", "Rec", "Yds", "TD", "Tgt share", "Air share", "aDOT", "RZ tgt", "20+", "Yards by game"],
                [[r["player"], r["pos"] or "?", r["games"], r["targets"], r["receptions"], r["yards"], r["td"], f(r["target_share"], 0, True), f(r["air_yards_share"], 0, True),
                  f(r["avg_depth_of_target"]), r["red_zone_targets"], r["explosive"], " ".join(str(g["yards"]) for g in r["log"])] for r in P["receivers"]]), ""]
    L += [f"### {team} rushers", "",
          table(["Player", "Pos", "G", "Car", "Yds", "YPC", "TD", "Carry share", "RZ car", "15+", "Yards by game"],
                [[r["player"], r["pos"] or "?", r["games"], r["carries"], r["yards"], f(r["yards_per_carry"], 2), r["td"], f(r["carry_share"], 0, True),
                  r["red_zone_carries"], r["explosive"], " ".join(str(g["yards"]) for g in r["log"])] for r in P["rushers"]]), ""]
    if o["run_game_by_direction"]:
        L += [f"### {team} run game by direction", "", table(["Direction", "Carries", "Yards", "YPC", "15+"],
              [[r["direction"], r["carries"], r["yards"], r["ypc"], r["explosive"]] for r in o["run_game_by_direction"]]), ""]
    fz = t.get("formation_zone_splits") or {}
    if fz.get("offense_by_formation") or fz.get("defense_vs_formation"):
        L += [f"### {team} by formation and pass zone", "",
              table(["Side", "Formation", "Plays", "Share", "Pass rate", "Yards / play", "EPA / play"],
                    [["offense", r["formation"], r["plays"], f(r["share"], 0, True), f(r["pass_rate"], 0, True), r["yards_per_play"], r["epa_per_play"]] for r in fz["offense_by_formation"]]
                    + [["defense vs", r["formation"], r["plays"], f(r["share"], 0, True), f(r["pass_rate"], 0, True), r["yards_per_play"], r["epa_per_play"]] for r in fz["defense_vs_formation"]]), "",
              table(["Side", "Pass zone", "Attempts", "Share", "Completion", "Yards / attempt", "20+"],
                    [["offense", r["zone"], r["attempts"], f(r["share"], 0, True), f(r["completion_rate"], 0, True), r["yards_per_attempt"], r["explosive"]] for r in fz["offense_pass_zones"]]
                    + [["defense allows", r["zone"], r["attempts"], f(r["share"], 0, True), f(r["completion_rate"], 0, True), r["yards_per_attempt"], r["explosive"]] for r in fz["defense_pass_zones_allowed"]]), ""]
    dc = t["depth_chart"]
    if dc.get("starters"):
        ol = [s for s in dc["starters"] if s["slot"] in ("LT", "LG", "C", "RG", "RT")]
        dl = [s for s in dc["starters"] if s["slot"] in ("LDE", "RDE", "LDT", "RDT", "NT", "DE", "DT", "LOLB", "ROLB", "WLB", "SLB", "EDGE")]
        L += [f"### {team} lines (depth chart as of {dc['as_of']})", "",
              "Offensive line: " + (", ".join(f"{s['slot']} {s['player']}" for s in ol) or "n/a") + ".  ",
              "Defensive front: " + (", ".join(f"{s['slot']} {s['player']}" for s in dl) or "n/a") + ".", ""]
    inj = t["injuries"]
    L += [f"### {team} injuries", ""]
    if inj["official_report"]:
        L += [table(["Player", "Pos", "Starter", "Game status", "Practice", "Injury"],
                    [[r["player"], r["position"], "yes" if r["starter"] else "", r["game_status"] or "none listed", r["practice_status"] or "", r["injury"] or ""] for r in inj["official_report"]]), ""]
    else:
        L += ["Official report not posted yet for this week.", ""]
    if inj["espn_live"]:
        L += ["ESPN live list: " + "; ".join(f"{r['player']} ({r['position']}) {r['status']}" for r in inj["espn_live"][:25]) + ".", ""]
    else:
        L += [f"ESPN live list: {inj['espn_live_status']}.", ""]
    L += [inj["note"], ""]
    mv = t["roster_moves"]
    if mv["arrivals_from_other_teams"] or mv["departures_to_other_teams"]:
        L += [f"### {team} roster moves (last {mv['window_weeks']} weeks)", "",
              "Arrived: " + ("; ".join(f"{m['player']} ({m['position']}) from {m['from']}" for m in mv["arrivals_from_other_teams"]) or "none") + ".  ",
              "Left for another team: " + ("; ".join(f"{m['player']} ({m['position']}) to {m['to']}" for m in mv["departures_to_other_teams"]) or "none") + ".", ""]
    return "\n".join(L)


def _px(v):
    return "n/a" if v is None else format(int(v), "+d")


def market_section(pk):
    g, bk, wx = pk["game"], pk.get("books") or {}, pk.get("weather") or {}
    L = ["## Weather", ""]
    if wx.get("status") == "OK":
        k, d = wx["at_kickoff"], wx["during_game"]
        L += [f"National Weather Service, retrieved {wx['retrieved_utc']} UTC. At kickoff: {k['temp_f']} F, wind {k['wind_mph']:g} mph {k['wind_dir']}, "
              f"{k['precip_chance_pct']}% chance of precipitation, {k['summary']}. During the game: low {d['temp_f_min']} F, wind up to {d['wind_mph_max']:g} mph, "
              f"precipitation chance up to {d['precip_chance_pct_max']}%. Roof: {wx['roof']}. Flags: {', '.join(wx['flags']) or 'none'}.", ""]
    else:
        L += [f"{wx.get('status', 'NOT_REQUESTED')}", ""]
    L += ["## Book prices and no-vig", ""]
    mk = bk.get("markets")
    if not mk:
        return L + [f"No book prices in this packet: {bk.get('status', 'NOT_REQUESTED')}. Do not quote Pinnacle, DraftKings or FanDuel numbers from memory.", ""]
    rows = []
    for label in ("spread", "total", "moneyline"):
        m = mk.get(label)
        if not m:
            continue
        a, b = m["sides"]
        for book, q in m["books"].items():
            ln = "" if q["line"] is None else (format(q["line"], "+g") if label == "spread" else f"{q['line']:g}")
            rows.append([label, book, f"{a} {ln}".strip(), _px(q["prices"][a]), _px(q["prices"][b]), f(q["no_vig"][a], 1, True), f(q["no_vig"][b], 1, True), f(q["hold"], 1, True), q.get("last_update") or ""])
    L += [f"Retrieved {bk.get('retrieved_utc')} UTC. No-vig = each side's share of the two implied probabilities. Pinnacle is the sharp reference; DraftKings and FanDuel are the prices available to bet.", "",
          table(["Market", "Book", "Side A / line", "Price A", "Price B", "No-vig A", "No-vig B", "Hold", "Book updated"], rows), ""]
    mv = bk.get("movement") or {}
    if mv.get("moves"):
        L += [f"### Line movement: first seen {mv['first_seen_utc']} to {mv['current_utc']} ({mv['snapshots']} snapshots)", "",
              table(["Market", "Book", "First line", "Now", "Move", "First prices", "Prices now"],
                    [[r["market"], r["book"], f(r["first_line"]), f(r["current_line"]), f(r.get("line_move")), " / ".join(_px(v) for v in r["first_prices"].values()),
                      " / ".join(_px(v) for v in r["current_prices"].values())] for r in mv["moves"]]), "", mv["note"], ""]
    pc = bk.get("prop_check")
    if pc:
        L += ["### Player props beside the research baseline", "",
              table(["Player", "Stat", "Book", "Line", "Over / Under", "No-vig over", "Pinnacle no-vig over (same line)", "Baseline mean", "Baseline median", "G", "Baseline - line"],
                    [[r["player"], r["stat"].replace("_", " "), r["book"], f(r["line"]), f"{_px(r['prices']['Over'])} / {_px(r['prices']['Under'])}", f(r["no_vig_over"], 1, True),
                      f(r["sharp_no_vig_over"], 1, True), f(r["baseline_weighted_mean"]), f(r["baseline_median"]), f(r["baseline_games"]), f(r["baseline_minus_line"])] for r in pc["rows"][:40]]), "", pc["note"], ""]
    else:
        L += [f"Player props: {bk.get('props_status', 'not fetched')}.", ""]
    return L


def brief(pk):
    g, m = pk["game"], pk["market"]
    L = [f"# {g['away']} at {g['home']}: Week {g['week']}, {g['slot']}", "",
         f"**{g['weekday']} {g['date']}, {g['kickoff_et']} ET.** Site: {g['site']}; roof: {g['roof'] or 'not listed'}; surface: {g['surface'] or 'not listed'}. "
         f"Rest: {g['away']} {g['away_rest_days']} days, {g['home']} {g['home_rest_days']} days. Listed QBs: {g['listed_qbs'][g['away']]} ({g['away']}), {g['listed_qbs'][g['home']]} ({g['home']}).", "",
         f"Market (schedule consensus, not a timestamped quote): {g['home']} {f(m['home_spread']) if m['home_spread'] is None else format(m['home_spread'], '+g')}, total {f(m['total'])}.", "",
         f"Generated {pk['generated_utc']} UTC. **Research only. `projection_ready` is false. Not betting advice.** "
         "Every number below is a count of recorded plays; a missing value is unknown, not zero.", ""]
    L += market_section(pk)
    L += ["## Matchup edges", ""]
    for key, mu in pk["matchup"].items():
        L += [f"### {key.replace('_', ' ')}", ""]
        if mu["edges"]:
            v = lambda e, x: f(x, 1, True) if e["is_rate"] else f(x, 1)
            L += [table(["Flag", "Area", "Offense (per game or rate)", "Defense (allowed, or its own sack/pressure rate)", "League avg", "Ranks"],
                        [[e["edge"], e["area"], v(e, e["offense_value"]), v(e, e["defense_value"]), v(e, e["league_avg"]), e["why"]] for e in mu["edges"]]), ""]
        else:
            L += ["No top-10 versus bottom-10 mismatch in the tracked areas.", ""]
    tp = pk["team_projection"]
    L += ["## Team score projection (research only)", ""]
    if tp.get("samplers"):
        rows = []
        for name, s in tp["samplers"].items():
            if "error" in s:
                rows.append([name, s["error"], "", "", "", "", "", ""]); continue
            rows.append([name, f"{g['away']} {s['away_points']} - {g['home']} {s['home_points']}", s["total"], format(s["home_margin"], "+g"), f(s["home_win"], 1, True),
                         f(s.get("home_covers_market_spread"), 1, True), f(s.get("over_market_total"), 1, True),
                         f"{g['away']} {s['first_half']['away']} - {g['home']} {s['first_half']['home']}"])
        L += [table(["Sampler", "Mean score", "Total", "Home margin", "Home win", "Home covers", "Over", "First half"], rows), "", tp.get("note", ""), ""]
    else:
        L += [f"Unavailable: {tp.get('status')}", ""]
    L += ["## Player baselines (research only)", ""]
    for key, mu in pk["matchup"].items():
        pb = mu["player_baselines"]
        rows = []
        for r in pb["players"]:
            for stat in ("passing_yards", "receiving_yards", "receptions", "rushing_yards"):
                b = r.get(stat)
                if b:
                    rows.append([r["player"], r["pos"], stat.replace("_", " "), b["games"], b["weighted_mean"], b["opponent_factor"], b["p5"], b["p10"], b["p15"], b["p20"], b["p25"], b["p50"]])
        if rows:
            L += [f"### {key.replace('_', ' ')}", "", table(["Player", "Pos", "Stat", "G", "Wtd mean", "Opp factor", "Floor p5", "p10", "MAIN p15", "p20", "p25", "Median"], rows), ""]
    if pk["matchup"]:
        L += [next(iter(pk["matchup"].values()))["player_baselines"]["method"], ""]
    for team, t in pk["teams"].items():
        L += [team_section(team, t)]
    cn = pk.get("connectors") or {}
    if cn.get("sources"):
        L += ["## Keyed connectors in this run", "",
              table(["Secret", "Provider", "Status", "Used for"], [[k, v["provider"], v["status"] + (f" (slate {v['slate_check']})" if v.get("slate_check") else "") + (f": {v['provider_message']}" if v.get("provider_message") else ""), v["used_for"]] for k, v in cn["sources"].items()]),
              "", cn["note"], ""]
    L += ["## Phase ledger", "", table(["Phase", "Name", "Status", "What this packet has / what is missing"],
                                       [[p["phase"], p["name"], p["status"], p["detail"]] for p in pk["phase_ledger"]]), ""]
    L += ["## Sources", "", table(["Dataset", "Status", "Retrieved (UTC)", "SHA-256 (first 12)"],
                                  [[k, v.get("status"), v.get("retrieved_utc") or "", (v.get("sha256") or "")[:12]] for k, v in pk["sources"].items()]), "",
          "Play-by-play, rosters, injuries, depth charts, snap counts and PFR advanced defense: nflverse (github.com/nflverse/nflverse-data). "
          "FTN charting via nflverse: FTN Data, CC-BY-SA 4.0. Third-party data keep their own terms; see SOURCES.md.", ""]
    return "\n".join(L)
