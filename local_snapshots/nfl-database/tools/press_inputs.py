"""Build the per-leg `press` block written by game-day assembly (runs/2026-11-05_shared_src/assemble.py onward).
Fail-closed: any input that is absent, MISSING, STALE or UNVERIFIED becomes "MISSING", never True. Context checks map to
the gate's phase results: matchup=P3 defense profile, coverage=P4 defender coverage, qb=P6 QB card, script=P13 game
script, form7=skill §7 (clears the exact line in 3 of last 4 with the current QB, or 3 of 3). Overrides:
weather_stop=P11 environment, injury_status=ESPN injuries, on_inactives=posted inactives list, sec11_conflict=player
already on a placed slip/ticket (§11), wr_rank=WR target rank last 3 games with current QB (#3/#4 ban)."""
M = "MISSING"
def _phase(st):
    if st == "PASS": return True
    if st == "FAIL": return False
    return M
def form7(values, line, side):
    if not isinstance(values, (list, tuple)) or len(values) < 3 or not all(isinstance(v, (int, float)) for v in values): return M
    v = list(values)[-4:]; ok = sum((x > line) if side == "over" else (x < line) for x in v)
    return ok >= 3
def wr_rank(player, team_wr_targets):
    if not team_wr_targets or player not in team_wr_targets: return None
    order = sorted(team_wr_targets, key=lambda k: -team_wr_targets[k]); return order.index(player) + 1
def build_press(player, pos, market, side, line, meds, phases, recent_form, injury_status, inactives, placed_players, wr_rank, sources=None):
    side = str(side).lower(); ph = phases or {}
    cov = _phase(ph.get(4))
    if ph.get(4) == "N/A" and market == "rushyds": cov = True  # pure rushing leg: phase 4 itself rules no coverage defender
    md = [float(x) for x in meds] if isinstance(meds, (list, tuple)) and len(meds) == 3 and all(isinstance(x, (int, float)) for x in meds) else M
    wx = {"PASS": False, "FAIL": True}.get(ph.get(11), M)
    inj = injury_status if injury_status else M
    ina = M if inactives is None else (player in inactives)
    s11 = M if placed_players is None else (player in placed_players)
    wr = "N/A" if pos != "WR" else (wr_rank if isinstance(wr_rank, int) else M)
    return dict(matchup=_phase(ph.get(3)), coverage=cov, script=_phase(ph.get(13)), qb=_phase(ph.get(6)),
                form7=form7(recent_form, line, side), medians=md, line=line, side=side,
                weather_stop=wx, injury_status=inj, on_inactives=ina, sec11_conflict=s11, wr_rank=wr,
                sources=sources or {"matchup": "phase 3", "coverage": "phase 4", "qb": "phase 6", "script": "phase 13",
                                    "form7": "recent_form (current QB)", "weather_stop": "phase 11", "injury_status": "ESPN injuries",
                                    "on_inactives": "posted inactives", "sec11_conflict": "placed slips/tickets", "wr_rank": "WR targets last 3 (current QB)"})
