"""Wiring for rules Rico already approved (Ghost6 audit 2026-11-03; edit hold lifted for wiring only).
Pure functions so assemble.py / replay harnesses can fill the Locked Door fields from pbp + coverage data.
  N1 carry share      : RB carries only (QB/WR/TE runs out of the denominator), last 4 games WITH THE CURRENT QB.
  depth fields        : script_pass, target_share (last-4 current-QB pbp), defender_giving, rung, te_rank   (DEPTH_RECEIVER, Rico 2026-11-02 23:59)
  defender_giving     : defender-level, or COVERAGE-level allowance vs 75%+ zone defenses (Rico: 'his defender/coverage has been giving it up')
  slot/primary matchup: WR who lines up mostly in the slot is matched to the defense's nickel from the chart, not WR-rank -> CB-rank.
Not wired here (wait for Rico): §14 cushion change, target-share MODEL-SUSPECT flag."""
ZONE_HEAVY = 75.0          # % zone (Sharp) at/above which coverage-level allowance may stand in for a single defender
SCRIPT_DOG = 3.0           # script_pass: team is a 3+ pt underdog ...
SCRIPT_TOTAL = 47.0        # ... or game total >= 47   (same definition the Wk6-8 replay used)

def _last_qb_games(pbp, team, qb_id, n=4, before=None):
    """game_dates (sorted) of the last n team games where qb_id led dropbacks."""
    d = pbp[(pbp.posteam == team) & (pbp.qb_dropback == 1)]
    if before is not None: d = d[d.game_date.astype(str).str[:10] < str(before)[:10]]
    q = d.passer_player_id.fillna(d.rusher_player_id) if "rusher_player_id" in d else d.passer_player_id
    top = q.groupby(d.game_date.astype(str).str[:10]).agg(lambda x: x.value_counts().index[0])
    return sorted(k for k, v in top.items() if v == qb_id)[-n:]

def rb_carry_share(pbp, pos_map, team, pid, qb_id, n=4, before=None, source="nflverse pbp"):
    """N1 input. -> {value, shares, games, window, source} or None if no current-QB games."""
    gs = _last_qb_games(pbp, team, qb_id, n, before)
    if not gs: return None
    r = pbp[(pbp.posteam == team) & (pbp.rush_attempt == 1) & pbp.game_date.astype(str).str[:10].isin(gs)].copy()
    r["pos"] = r.rusher_player_id.map(pos_map)
    rb = r[r.pos == "RB"]
    per = [(int((rb[rb.game_date.astype(str).str[:10] == g].rusher_player_id == pid).sum()), int((rb.game_date.astype(str).str[:10] == g).sum())) for g in gs]
    tot_c, tot_rb = sum(a for a, _ in per), sum(b for _, b in per)
    if tot_rb == 0: return None
    return dict(value=round(tot_c / tot_rb, 3), shares=[round(a / b, 3) if b else None for a, b in per], games=gs, carries=[a for a, _ in per], rb_carries=[b for _, b in per],
                window=f"last {len(gs)} games with current QB, player carries / team RB carries (QB, WR, TE runs excluded)", source=source)

def target_share(pbp, team, pid, qb_id, n=4, before=None, source="nflverse pbp"):
    """QB's target share to the player: his targets from the current QB / current-QB pass attempts (no sacks), last n current-QB games."""
    gs = _last_qb_games(pbp, team, qb_id, n, before)
    if not gs: return None
    a = pbp[(pbp.posteam == team) & (pbp.pass_attempt == 1) & (pbp.sack != 1) & (pbp.passer_player_id == qb_id) & pbp.game_date.astype(str).str[:10].isin(gs)]
    if not len(a): return None
    return dict(value=round(float((a.receiver_player_id == pid).sum()) / len(a), 4), targets=int((a.receiver_player_id == pid).sum()), attempts=int(len(a)), games=gs,
                window=f"last {len(gs)} games with current QB", source=source)

def te_rank(pbp, pos_map, team, pid, qb_id, n=4, before=None):
    """Rank among the team's TEs by targets in the last n current-QB games (1 = TE1). None if he has no TE targets/unknown."""
    gs = _last_qb_games(pbp, team, qb_id, n, before)
    a = pbp[(pbp.posteam == team) & (pbp.pass_attempt == 1) & (pbp.sack != 1) & pbp.game_date.astype(str).str[:10].isin(gs)]
    vc = a[a.receiver_player_id.map(pos_map) == "TE"].receiver_player_id.value_counts()
    return int(list(vc.index).index(pid) + 1) if pid in vc.index else None

def rung(line, main):
    line, main = float(line), float(main)
    return "low" if line < main else ("main" if line == main else "high")

def script_pass(spread, total, source):
    """Game script calls for passing for this team: 3+ pt dog or total >= 47. spread = team spread (+ = dog)."""
    if spread is None or total is None: return dict(ok=None, source=None, detail="spread/total missing")
    ok = float(spread) >= SCRIPT_DOG or float(total) >= SCRIPT_TOTAL
    return dict(ok=bool(ok), source=source, detail=f"team spread {float(spread):+g}, total {float(total):g}; ok if 3+ pt dog or total >= 47")

def defender_giving(defender=None, league_ypt=None, zone_pct=None, coverage_allow=None, league_cov=None):
    """defender: {name, ypt, targets, source}; coverage_allow: {value (YPT allowed in the zone/middle bucket), bucket, source}.
    Defender-level: ypt >= league_ypt on 8+ targets.  Coverage-level (only vs 75%+ zone): bucket YPT >= league_cov."""
    if defender and defender.get("ypt") is not None and league_ypt is not None and (defender.get("targets") or 0) >= 8 and defender.get("source"):
        if float(defender["ypt"]) >= float(league_ypt):
            return dict(ok=True, level="defender", source=defender["source"], detail=f"{defender.get('name')} {float(defender['ypt']):.2f} YPT >= league {float(league_ypt):.2f}")
        dlevel = f"{defender.get('name')} {float(defender['ypt']):.2f} YPT < league {float(league_ypt):.2f}"
    else: dlevel = "defender-level data missing/thin"
    if zone_pct is not None and float(zone_pct) >= ZONE_HEAVY and coverage_allow and coverage_allow.get("value") is not None and league_cov is not None and coverage_allow.get("source"):
        ok = float(coverage_allow["value"]) >= float(league_cov)
        return dict(ok=bool(ok), level="coverage", source=coverage_allow["source"],
                    detail=f"{zone_pct:g}% zone: {coverage_allow.get('bucket','zone/middle')} {float(coverage_allow['value']):.2f} YPT {'>=' if ok else '<'} league {float(league_cov):.2f} ({dlevel})")
    return dict(ok=False, level="defender", source=(defender or {}).get("source"), detail=dlevel)

def slot_primary(wrcb_row, opp_depth, healthy=lambda n: True):
    """Matchup from the slot/primary chart. wrcb_row = ESPN WR/CB cheatsheet row {defender, lwr, slot, rwr, pos}.
    If the player's biggest alignment is the slot, his primary is the opponent's top healthy nickel (ESPN depth 'nb'); else the charted defender."""
    if not wrcb_row: return None
    al = {k: float(wrcb_row.get(k) or 0) for k in ("lwr", "slot", "rwr")}
    if al["slot"] >= max(al["lwr"], al["rwr"]) and al["slot"] > 0:
        for nb in (opp_depth or {}).get("nb", []):
            if healthy(nb): return dict(name=nb, basis=f"slot {al['slot']:g}% (L{al['lwr']:g}/R{al['rwr']:g}) -> nickel {nb} (ESPN depth nb)", source="ESPN WR/CB cheatsheet alignment + ESPN depth chart nb")
    return dict(name=wrcb_row.get("defender"), basis=f"charted primary (L{al['lwr']:g}/S{al['slot']:g}/R{al['rwr']:g})", source="ESPN WR/CB cheatsheet")
