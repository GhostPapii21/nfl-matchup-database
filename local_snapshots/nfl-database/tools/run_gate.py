#!/usr/bin/env python3
"""Fail-closed completeness gate for NFL game-script runs. See README_run_gate.md.
Usage: python3 run_gate.py <run_dir> [--now 2026-11-01T12:00]   (times are ET, naive ISO)"""
import argparse, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rules import rulebook as _rb   # Locked Door: thresholds + activation come from rules/rulebook.py
from datetime import datetime

PHASES = list(range(1, 16))
CATEGORIES = ["core_stats_pbp","coverage_matchups","ngs","film","injuries_news","weather","odds_props"]
MAX_AGE_H = {"coverage_matchups":_rb.param("COVERAGE_AGE","max_h"),"injuries_news":6,"odds_props":1,"weather":6}
DEFAULT_AGE_H = 48
MODELS = ["monte_carlo","bias","game_randomness"]
PRESSURE = ["blitz_rate","pressure_rate","checkdown_share"]
PRESSURE_W9 = ["time_to_throw","targets_under_pressure"]
BAD = {"FAIL","MISSING","STALE","UNVERIFIED"}

YARDS_MKTS = ("passyds","recyds","rushyds","rushrec")
def is_yards(l):
    mk = str(l.get("market") or "").lower()
    if mk: return mk in YARDS_MKTS
    return bool(re.search(r"\byds\b|yards", str(l.get("name","")), re.I))
def leg_price(l):
    for k in ("price","price_fd"):
        v = l.get(k)
        if v is not None:
            try: return float(v)
            except (TypeError, ValueError): return None
    return None
WX_PRECIP, WX_GUST, WX_WIND = (_rb.param("WEATHER", k) for k in ("precip","gust","wind"))   # BUG-2026-11-01-WX thresholds (>=)
INDOOR = ("dome","closed","indoor","retractable_closed")
SLIPS = "/workspace/nfl-database/week8/slips/slips_2026-11-01.md"
SLIPS_DATE = "2026-11-01"   # BUG-2026-11-01-WXSLIPS: the Week 8 slips file only describes Nov 1 games
SIMV6_FROM = _rb.rule("SIMV6")["effective"]   # BUG-2026-11-01-SIMV6: runs dated >= this must name tools/sim_v6.py as the sim script
FORECAST_FROM, FORECAST_MAX_H = _rb.rule("FORECAST")["effective"], _rb.param("WEATHER","forecast_max_h")   # BUG-2026-11-01-WXDAYS (Rico): multi-day forecast at slip build
COVPROF_FROM = _rb.rule("COVPROF")["effective"]   # Rico 2026-11-01: defensive coverage profile required on every receiving AND passing leg
PASS_MKTS = ("passyds","passcomp","completions","passtd","passatt","pass_att","pass_tds")
def is_passing(l):
    mk = str(l.get("market") or "").lower()
    if mk: return mk in PASS_MKTS
    return l.get("type") == "QB" and bool(re.search(r"pass|complet", str(l.get("name","")), re.I))
PFF_BANNED_SCOPES = ("weather","game_script","script","prop_projection","projection")   # PFF = matchups only (Rico 2026-11-01)
def wx_sensitive(l):
    """passing/receiving OVER: rec, rec yds, pass yds, completions, rush+rec."""
    mk = str(l.get("market") or "").lower()
    if mk: return mk in ("rec","receptions","recyds","passyds","passcomp","completions","rushrec")
    return bool(re.search(r"\brec\b|recept|rec yds|pass yds|passing|complet|rush\s*\+\s*rec", str(l.get("name","")), re.I))
GS_SPREAD, GS_YPC = -7.0, 4.4   # BUG-2026-11-01-RBSCRIPT trigger (inclusive)
RUSH_MKTS = ("rushyds","rushrec")
RB_OUT = {"OUT","IR","INACTIVE","PUP","SUSPENDED"}; SOFT_YPC = 4.4; DOG_SHARE = 0.70; DOG_PHASES = (6, 7, 13)
DOG_RX = re.compile(r"underdog|trail|dog\b|10G", re.I)   # only script-based blocks are waivable
def wx_flag_of(w):
    if not isinstance(w, dict) or str(w.get("roof") or "").lower() in INDOOR: return False
    v = [w.get(k) for k in ("precip_pct","gust_mph","wind_mph")]
    return any(isinstance(x,(int,float)) and x >= t for x, t in zip(v, (WX_PRECIP, WX_GUST, WX_WIND)))
def median(v):
    v = sorted(v); n = len(v); return v[n//2] if n % 2 else (v[n//2-1]+v[n//2])/2

def parse_t(s):
    if not s: return None
    try: return datetime.fromisoformat(str(s).strip().replace(" ", "T")[:16])
    except ValueError: return None

SCHEME_KEYS = _rb.param("SCHEME_EDGE","keys")
def se_explained(l): return bool(str((l.get("scheme_edge") or {}).get("explanation") or "").strip())
def scheme_edge_ok(l):
    """SCHEME_EDGE (Rico 2026-11-02 21:13 ET): matchup, scheme/coverage fit (QB usage vs the defense's coverage),
    game script and recent-form trend all line up -> averages (§7) and sim models alone cannot cut the leg; they become flags.
    Each key must be {"ok": true, "source": ..., "detail": ...}. Weather, inactives, §11, DEPTH_RECEIVER, -250 flag still apply."""
    se = l.get("scheme_edge")
    if not isinstance(se, dict): return False
    return all(isinstance(se.get(k), dict) and se[k].get("ok") is True and se[k].get("source") for k in SCHEME_KEYS)

class Gate:
    def __init__(self, d, now):
        self.d, self.now, self.miss, self.notes = d, now, [], []
        self.exceptions, self.applied = [], []
    def fail(self, m): self.miss.append(m)
    def age_ok(self, label, ts, cat=None):
        t = parse_t(ts)
        if t is None: self.fail(f"{label}: missing/unparseable pull timestamp (counts as STALE)"); return False
        lim = MAX_AGE_H.get(cat, DEFAULT_AGE_H); age = (self.now - t).total_seconds()/3600
        if age > lim: self.fail(f"{label}: STALE ({age:.1f} h old > {lim} h limit)"); return False
        if age < -0.01: self.fail(f"{label}: pull timestamp {ts} is in the future"); return False
        return True
    def exc_for(self, inp, src):
        for e in self.exceptions:
            if e["input"] == inp and src and os.path.basename(str(src)) == os.path.basename(e["source"]): return e
        return None
    def check_risks(self):
        if not self.applied: return
        p = os.path.join(self.d, "report.md")
        txt = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
        mt = re.search(r"^#+\s*[^\n]*Risks[^\n]*\n(.*?)(?=^#+\s|\Z)", txt, re.S | re.M | re.I)
        sec = mt.group(1) if mt else ""
        for e in {id(e): e for _, e in self.applied}.values():
            if os.path.basename(e["source"]) not in sec:
                self.fail(f"report.md Risks section does not mention applied exception {os.path.basename(e['source'])}")
    def stamped(self, label, obj, cat=None, src_key="source"):
        if not isinstance(obj, dict): self.fail(f"{label}: missing"); return False
        if not (obj.get(src_key) or obj.get("url_or_file")): self.fail(f"{label}: no source url/file"); return False
        return self.age_ok(label, obj.get("pulled_et"), cat)

    def check_form(self, n, l, line, side):
        """Skill §7 HARD (clears exact line in 3 of last 4 with current QB, or 3 of 3) and §14 yards-over cushion."""
        rf = l.get("recent_form")
        if not isinstance(rf, dict): self.fail(f"leg {n}: recent_form missing (§7 last-4 with current QB) — fail closed"); return
        vals = rf.get("values")
        if not rf.get("source"): self.fail(f"leg {n}: recent_form has no source")
        else: self.age_ok(f"leg {n} recent_form", rf.get("pulled_et"), "core_stats_pbp")
        if not rf.get("qb"): self.fail(f"leg {n}: recent_form qb (current QB) missing")
        if not isinstance(vals, list) or not all(isinstance(v, (int, float)) for v in vals):
            self.fail(f"leg {n}: recent_form values missing/non-numeric"); return
        if not isinstance(rf.get("games"), list) or len(rf["games"]) != len(vals):
            self.fail(f"leg {n}: recent_form games must list one game id per value"); return
        vals = vals[-4:]
        if len(vals) < 3: self.fail(f"leg {n}: §7 FAIL only {len(vals)} games with current QB (need 3 of 3 or 3 of 4)"); return
        hits = sum((v > line) if side == "over" else (v < line) for v in vals)
        if hits < 3 and scheme_edge_ok(l):
            last2 = sum((v > line) if side == "over" else (v < line) for v in vals[-2:])
            self.notes.append(f"leg {n}: SCHEME_EDGE §7 flag (not a cut): {hits} of {len(vals)} {vals}")
            if not se_explained(l): self.fail(f"leg {n}: SCHEME_EDGE needs a plain-words edge explanation (scheme_edge.explanation) to waive §7 - missing data, fail closed")
            if last2 < 2: self.notes.append(f"WARN SCHEME_EDGE_LAST2 leg {n}: last 2 games with current QB did not both clear ({vals[-2:]}) - warning only (Rico 2026-11-03 00:31 ET)")
        elif hits < 3: self.fail(f"leg {n}: §7 FAIL {side} {line} hit {hits} of {len(vals)} last games with current QB {vals}")
        if side == "over" and is_yards(l):
            pr = leg_price(l)
            if pr is None: self.fail(f"leg {n}: §14 yards-over cushion needs the price (price/price_fd) — fail closed"); return
            md = median(vals)
            if pr <= -150:
                if md < 1.20*line: self.fail(f"leg {n}: §14 FAIL at {pr:+.0f} last-4 median {md} < 20% over line {line} (need {1.2*line:.1f})")
            elif pr <= -113:
                if md < 1.25*line: self.fail(f"leg {n}: §14 FAIL at {pr:+.0f} last-4 median {md} < 25% over line {line} (need {1.25*line:.1f})")
                c10 = sum(v >= 1.10*line for v in vals)
                if c10 < 3: self.fail(f"leg {n}: §14 FAIL at {pr:+.0f} cleared line by 10%+ ({1.1*line:.1f}) in only {c10} of {len(vals)}")
            else:
                self.notes.append(f"{n}: §14 cushion not triggered at {pr:+.0f} (skill sets it only at -113 or longer)")
    def check_cross_checks(self, m):
        for c in m.get("cross_checks", []) or []:
            lab = f"cross_check {c.get('name','?')}"
            if not (c.get("url_or_file") or c.get("source")): self.fail(f"{lab}: no source url/file"); continue
            t = parse_t(c.get("pulled_et"))
            if t is None: self.fail(f"{lab}: missing/unparseable pulled_et"); continue
            if (self.now - t).total_seconds() < -36: self.fail(f"{lab}: pull timestamp {c['pulled_et']} is in the future"); continue
            self.notes.append(f"cross-check (pick-side only, not a gated source): {c.get('name')} pulled {c['pulled_et']}")

    def check_pff(self, m, legs, live):
        """BUG-2026-11-01-PFFX (Rico 2026-11-01 22:17 ET): PFF counts for matchups only and every PFF input needs a
        second public source (ESPN win rates / NFL.com NGS / our pbp). Missing or disagreeing second source = CAUTION (not a block).
        PFF used for weather or game script = FAIL (never allowed)."""
        P = m.get("pff_inputs")
        if not P: return
        self.pff_notes = ["PFF CROSS-CHECK (caution flags only; never a pass reason):"]
        for i, x in enumerate(P):
            lab = f"PFF input {x.get('leg','?')} / {x.get('metric','?')}"
            if str(x.get("scope","")).lower() in PFF_BANNED_SCOPES:
                self.fail(f"{lab}: PFF used for scope '{x.get('scope')}' — PFF counts for matchups only, never weather/game script/projections"); continue
            c = []
            ss = x.get("second_source")
            if not isinstance(ss, dict) or ss.get("value") is None: c.append("no second source value")
            else:
                if not (ss.get("source") or ss.get("url_or_file")) or parse_t(ss.get("pulled_et")) is None: c.append("second source lacks source/pull time")
                if re.search(r"pff", f"{ss.get('name','')} {ss.get('source','')}", re.I): c.append("second source is PFF itself")
                try:
                    tol = float(x.get("tolerance", 0)); dv = abs(float(x.get("value")) - float(ss.get("value")))
                    if dv > tol: c.append(f"sources disagree (PFF {x.get('value')} vs {ss.get('name')} {ss.get('value')}, tol {tol:g})")
                except (TypeError, ValueError): c.append("values not comparable")
            if str(x.get("pff_projection_side","")).lower() == "under" and str(x.get("pff_matchup_side","")).lower() == "over":
                c.append("PFF under while PFF's own matchup page supports the over")
            self.pff_notes.append(f"  - PFF CAUTION {lab}: {'; '.join(c)}" if c else f"  - {lab}: confirmed by {ss.get('name')}")
    def check_simv6(self, m):
        if not _rb.active("SIMV6", self.game_date, self.now): return
        for s in m.get("sims", []):
            if not re.search(r"sim_v6\.py$", str(s.get("script") or "")):
                self.fail(f"sim {s.get('model')}: script {s.get('script')!r} is not tools/sim_v6.py (runs dated >= {SIMV6_FROM} must use sim_v6)")
    def check_weather(self, m, legs, live):
        """Phase 11 (BUG-2026-11-01-WX): fail closed; flagged open-air game => wx-sensitive overs must be CUT."""
        W = m.get("weather")
        if not isinstance(W, dict) or not W: self.fail("Phase 11 weather: manifest 'weather' block missing (fail closed)"); return
        if "roof" in W: W = {str(m.get("game")): W}
        self.wx_alerts = []
        one = next(iter(W)) if len(W) == 1 else None
        for g, w in W.items():
            lab = f"Phase 11 weather {g}"
            if not isinstance(w, dict): self.fail(f"{lab}: roof status missing (fail closed) — weather entry is {type(w).__name__}, not an object"); continue   # BUG-2026-11-02-WXROOF
            roof = str(w.get("roof") or "").lower()
            if not roof: self.fail(f"{lab}: roof status missing (fail closed)"); continue
            if not (w.get("source") or w.get("url_or_file")): self.fail(f"{lab}: no source url/file")
            self.age_ok(lab, w.get("pulled_et"), "weather")
            if roof in INDOOR: continue
            vals = {k: w.get(k) for k in ("precip_pct","gust_mph","wind_mph")}
            if any(not isinstance(v, (int, float)) for v in vals.values()):
                self.fail(f"{lab}: open-air weather inputs missing {[k for k,v in vals.items() if not isinstance(v,(int,float))]} (fail closed)"); continue
            why = [x for x, c in ((f"precip {vals['precip_pct']}%", vals["precip_pct"] >= WX_PRECIP),
                                  (f"gusts {vals['gust_mph']} mph", vals["gust_mph"] >= WX_GUST),
                                  (f"sustained wind {vals['wind_mph']} mph", vals["wind_mph"] >= WX_WIND)) if c]
            if not why: continue
            gl = [n for n, l in legs.items() if (l.get("game") or one) == g]
            bad = [n for n in gl if n in live and str(l_side := legs[n].get("side","")).lower() == "over" and wx_sensitive(legs[n])]
            for n in bad: self.fail(f"leg {n}: WEATHER flagged game {g} ({', '.join(why)}) — passing/receiving OVER must be CUT")
            self.wx_alerts.append((g, why, self.placed_in(m, g)))
        for n in live:
            g = legs[n].get("game") or one
            if g not in W: self.fail(f"leg {n}: Phase 11 weather missing for game {g} (fail closed)")
    def check_forecast(self, m, legs, live):
        """BUG-2026-11-01-WXDAYS: runs dated >= FORECAST_FROM need a weather_forecast block (tools/weather_forecast.py) pulled
        within 24h with an entry for every game in the run; open-air games need numbers. Flag is recomputed from the numbers."""
        self.fc_alerts = []
        if not _rb.active("FORECAST", self.game_date, self.now): return
        F = m.get("weather_forecast")
        if not isinstance(F, dict) or not isinstance(F.get("games"), dict):
            self.fail("weather forecast: manifest 'weather_forecast' block missing (run tools/weather_forecast.py at slip build; fail closed)"); return
        if not (F.get("source") or F.get("file")): self.fail("weather forecast: no source/file")
        t = parse_t(F.get("pulled_et"))
        if t is None: self.fail("weather forecast: missing/unparseable pulled_et (fail closed)")
        else:
            age = (self.now - t).total_seconds()/3600
            if age > FORECAST_MAX_H: self.fail(f"weather forecast: STALE ({age:.1f} h old > {FORECAST_MAX_H} h limit) — re-run tools/weather_forecast.py")
            elif age < -0.01: self.fail(f"weather forecast: pull timestamp {F.get('pulled_et')} is in the future")
        games = {l.get("game") for l in legs.values() if l.get("game")} | ({m.get("game")} if m.get("game") else set())
        one = m.get("game")
        for g in sorted(games, key=str):
            e = F["games"].get(g)
            if not isinstance(e, dict): self.fail(f"weather forecast {g}: no forecast for this game (fail closed)"); continue
            roof = str(e.get("roof") or "").lower()
            if not roof: self.fail(f"weather forecast {g}: roof missing (fail closed)"); continue
            if any(x in roof for x in ("dome","indoor","closed")): continue
            v = [e.get(k) for k in ("precip_pct","gust_mph","wind_mph")]
            if str(e.get("status","")).upper() != "OK" or not isinstance(v[0], (int, float)) or not any(isinstance(x, (int, float)) for x in v[1:]):
                self.fail(f"weather forecast {g}: no forecast numbers for open-air game (status {e.get('status')}; fail closed)"); continue
            why = [x for x, c in ((f"precip {v[0]}%", v[0] >= WX_PRECIP), (f"gusts {v[1]} mph", isinstance(v[1], (int, float)) and v[1] >= WX_GUST),
                                  (f"sustained wind {v[2]} mph", isinstance(v[2], (int, float)) and v[2] >= WX_WIND)) if c]
            if not why: continue
            bad = [n for n in sorted(live) if (legs[n].get("game") or one) == g and str(legs[n].get("side","")).lower() == "over" and wx_sensitive(legs[n])]
            for n in bad: self.fail(f"leg {n}: WEATHER FORECAST flagged game {g} ({', '.join(why)}) — passing/receiving OVER must be CUT")
            self.fc_alerts.append(f"WEATHER FORECAST ALERT: {g} kickoff {e.get('kickoff_et')} forecast {', '.join(why)} (pulled {F.get('pulled_et')} ET). Rushing overs first; live wx-sensitive overs: {bad or 'none'}")
    def check_game_script(self, m, legs, live):
        """BUG-2026-11-01-RBSCRIPT. Returns live legs whose Phase 7 carry-share FAIL is waived (re-priced on boosted script)."""
        B = m.get("game_script_rb") or {}; W = m.get("weather") if isinstance(m.get("weather"), dict) else {}
        if "roof" in W: W = {str(m.get("game")): W}
        one = next(iter(W)) if len(W) == 1 else None
        games = set(W) | {l.get("game") or one for l in legs.values()}; games.discard(None)
        sims = {s.get("model"): s for s in m.get("sims", [])}; waived = set(); self.gs_notes = []
        for g in sorted(games, key=str):
            wx = wx_flag_of(W.get(g)); b = B.get(g)
            gl = [n for n, l in legs.items() if (l.get("game") or one) == g]
            big = any(isinstance(legs[n].get("spread"), (int, float)) and legs[n]["spread"] <= GS_SPREAD for n in gl)
            if not isinstance(b, dict):
                if wx or big: self.fail(f"game_script_rb {g}: block missing but trigger possible ({'weather-flagged' if wx else 'favored by 7+'}) (fail closed)")
                continue
            lab = f"game_script_rb {g}"
            fs, yp = b.get("fav_spread"), b.get("opp_ypc")
            if not isinstance(fs, (int, float)) or not isinstance(yp, (int, float)): self.fail(f"{lab}: fav_spread/opp_ypc missing (fail closed)"); continue
            if not b.get("source"): self.fail(f"{lab}: no source")
            self.age_ok(lab, b.get("pulled_et"))
            trig = wx or (fs <= GS_SPREAD and yp >= GS_YPC)
            if bool(b.get("wx_flag")) != wx: self.fail(f"{lab}: wx_flag {b.get('wx_flag')} disagrees with Phase 11 weather ({wx})")
            if bool(b.get("triggered")) != trig: self.fail(f"{lab}: triggered={b.get('triggered')} but rule says {trig} (spread {fs}, opp YPC {yp}, wx {wx})"); continue
            if not trig: continue
            bo = b.get("boost") or {}
            if not all(isinstance(bo.get(k), (int, float)) for k in ("lead","rb2")) or not bo.get("source"): self.fail(f"{lab}: fitted boost lead/rb2 + source missing")
            if not b.get("lead_rb") or not b.get("rb2"): self.fail(f"{lab}: lead_rb/rb2 names missing")
            rp = b.get("rb2_projection") or {}
            if not isinstance(rp.get("median"), dict) or not all(k in rp["median"] for k in ("mc","bias","gr")): self.fail(f"{lab}: rb2 projection (3 models) missing")
            if wx:
                mo = list(b.get("model_order") or [])
                if not mo: self.fail(f"{lab}: model_order missing in weather-flagged game")
                else:
                    ri = [i for i, x in enumerate(mo) if x in RUSH_MKTS]; oi = [i for i, x in enumerate(mo) if x not in RUSH_MKTS]
                    if ri and oi and max(ri) > min(oi): self.fail(f"{lab}: model order {mo} — rushing overs must be modeled before passing overs")
            self.gs_notes.append(f"GAME SCRIPT: {g} triggered (spread {fs}, opp YPC {yp}, wx {wx}); boost lead x{bo.get('lead')} rb2 x{bo.get('rb2')}; RB2 {b.get('rb2')} medians {rp.get('median')}")
            for n in gl:
                l = legs[n]
                if n in live and l.get("player") == b.get("lead_rb") and str(l.get("market","")).lower() in RUSH_MKTS and l.get("repriced_game_script") is True \
                   and all((sims.get(mo, {}).get("legs", {}).get(n) or {}).get("script") == "boosted" for mo in MODELS):
                    waived.add(n); self.gs_notes.append(f"GAME SCRIPT: {n} Phase 7 carry-share FAIL waived — re-priced on boosted script; all other checks applied")
        return waived
    # ---------- BUG-2026-11-01-RBMISS ----------
    def check_rbmiss(self, m, legs, live):
        """A promotion record, D dog-RB exception, E split re-price, F soft run D. Returns legs whose underdog/trailing
        phase FAILs (6/7/13) are waived under D. Every other check still applies (B and C are NOT implemented)."""
        self.rm_notes = []; waived = {}; st = m.get("rb_status") or {}; pr = m.get("rb_promotions") or {}; sp = m.get("split_reprice") or {}
        sims = {s.get("model"): s for s in m.get("sims", [])}
        for team, r in st.items():                                   # A
            if str(r.get("rb1_status", "")).upper() not in RB_OUT: continue
            lab = f"rb_promotion {team}"; b = pr.get(team)
            if not isinstance(b, dict): self.fail(f"{lab}: RB1 {r.get('rb1')} {r.get('rb1_status')} but RB2 {r.get('rb2')} not built/priced (fail closed)"); continue
            if b.get("rb2") != r.get("rb2"): self.fail(f"{lab}: promoted {b.get('rb2')} != rb_status rb2 {r.get('rb2')}")
            if not isinstance(b.get("tau"), (int, float)) or not b.get("tau_source"): self.fail(f"{lab}: fitted tau + source missing")
            if not (isinstance(b.get("share_new"), (int, float)) and isinstance(b.get("share_own"), (int, float)) and b["share_new"] > b["share_own"]): self.fail(f"{lab}: share_new must exceed own share")
            if not all(isinstance((b.get(k) or {}).get(mo), (int, float)) for k in ("p", "median") for mo in ("mc", "bias", "gr")): self.fail(f"{lab}: p/median for all 3 models missing")
            self.age_ok(lab, b.get("pulled_et"))
            self.rm_notes.append(f"RB PROMOTION: {team} {r.get('rb1')} {r.get('rb1_status')} -> {b.get('rb2')} share {b.get('share_own')}->{b.get('share_new')} (tau {b.get('tau')}); p {b.get('p')}")
        for n, l in legs.items():
            if n not in live: continue
            mk = str(l.get("market", "")).lower(); team = l.get("team")
            if l.get("split_flag"):                                   # E
                b = sp.get(team); backs = (b or {}).get("backs") or []
                ok = isinstance(b, dict) and len(backs) >= 2 and all(isinstance(x.get("share_range"), list) and len(x["share_range"]) == 2 and x["share_range"][0] < x["share_range"][1]
                     and all(isinstance(((x.get("p") or {}).get(k) or {}).get(mo), (int, float)) for k in ("lo", "mid", "hi") for mo in ("mc", "bias", "gr")) for x in backs) \
                     and l.get("player") in [x.get("player") for x in backs]
                if not ok: self.fail(f"split_reprice {team}: leg {n} split-flagged but both backs not priced over a carry-share range in 3 models (fail closed)")
            if mk in RUSH_MKTS and isinstance(l.get("opp_rb_ypc"), (int, float)) and l["opp_rb_ypc"] >= SOFT_YPC:   # F
                sr = l.get("soft_run_d") or {}
                if not isinstance(sr.get("applied"), (int, float)) or not sr.get("source"): self.fail(f"soft_run_d {n}: opp allows {l['opp_rb_ypc']} RB YPC (>= {SOFT_YPC}) but fitted YPC boost not recorded")
            ex = l.get("dog_rb_exception")                            # D
            if not isinstance(ex, dict): continue
            lab = f"dog_rb_exception {n}"; med = ex.get("medians") or {}; line = l.get("line")
            simmed = [(sims.get(mo, {}).get("legs", {}).get(n) or {}).get("median") for mo in MODELS]
            conds = [mk == "rushyds", str(l.get("side", "")).lower() == "over", isinstance(l.get("spread"), (int, float)) and l["spread"] > 0,
                     isinstance(line, (int, float)) and all(isinstance(med.get(k), (int, float)) and med[k] > line for k in ("mc", "bias", "gr")),
                     all(isinstance(v, (int, float)) and v > line for v in simmed) if any(v is not None for v in simmed) else True,
                     bool(ex.get("backup_out")) or (isinstance(ex.get("carry_share"), (int, float)) and ex["carry_share"] >= DOG_SHARE),
                     isinstance(ex.get("main_line"), (int, float)) and isinstance(line, (int, float)) and line <= ex["main_line"]]
            if ex.get("backup_out"):
                ts = st.get(team) or {}
                if not (ts.get("rb2") == ex.get("backup") and str(ts.get("rb2_status", "")).upper() in RB_OUT):
                    self.fail(f"{lab}: backup_out claimed but rb_status for {team} does not show {ex.get('backup')} out"); continue
            if all(conds):
                waived[n] = {ph for ph in DOG_PHASES if DOG_RX.search(self.detail.get((n, ph), ""))}
                self.rm_notes.append(f"DOG RB EXCEPTION: {n} — all 3 medians {med} clear {line}; backup_out {ex.get('backup_out')}, share {ex.get('carry_share')}; waives underdog/trailing FAILs on phases {sorted(waived[n])}")
        return waived
    def placed_in(self, m, g):
        if isinstance(m.get("placed_legs"), list):
            return [p.get("leg") for p in m["placed_legs"] if p.get("game") == g]
        teams = [t for t in re.split(r"[@ ]+", str(g)) if t]
        out = []
        if getattr(self, "game_date", "") != SLIPS_DATE:
            return ["placed legs unknown (no manifest placed_legs for this date; check placed_slips.json)"]
        if os.path.exists(SLIPS):
            for line in open(SLIPS, encoding="utf-8"):
                if line.startswith("- ") and any(re.search(rf"\b{re.escape(t)}\b", line) for t in teams): out.append(line[2:].strip())
        return out
    def checklist(self, legs):
        p = os.path.join(self.d, "checklist.md")
        if not os.path.exists(p): self.fail("checklist.md missing"); return {}
        rows = {}; self.detail = {}
        for line in open(p, encoding="utf-8"):
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(c) < 6 or not re.match(r"^\d+", c[1]): continue
            leg, ph, st = c[0], int(re.match(r"^\d+", c[1]).group()), c[2].upper()
            rows.setdefault(leg, {})[ph] = st; self.detail[(leg, ph)] = c[3]
            if st not in BAD | {"PASS","N/A","HOLD"}: self.fail(f"checklist {leg} phase {ph}: unknown status '{c[2]}'")
            if st != "N/A" and (not c[4] or not parse_t(c[5])):
                self.fail(f"checklist {leg} phase {ph}: missing source or Pulled (ET) timestamp")
        for name in legs:
            if name not in rows: self.fail(f"checklist: no rows for leg '{name}'"); continue
            for ph in PHASES:
                if ph not in rows[name]: self.fail(f"checklist {name}: phase {ph} row missing")
        for name in rows:
            if name not in legs: self.fail(f"checklist leg '{name}' not in run_manifest legs")
        return rows

    def run(self):
        mp = os.path.join(self.d, "run_manifest.json")
        if not os.path.exists(os.path.join(self.d, "report.md")): self.fail("report.md missing")
        try: m = json.load(open(mp, encoding="utf-8"))
        except Exception as e: self.fail(f"run_manifest.json unreadable: {e}"); return
        legs = {l.get("name"): l for l in m.get("legs", [])}
        self.game_date = str(m.get("game_date") or str(m.get("kickoff_et", ""))[:10])
        req = ("input","source","approved_by","approved_on","valid_for_date","scope","reason")
        for e in m.get("approved_exceptions", []):
            lack = [k for k in req if not e.get(k)]
            if lack: self.fail(f"approved_exception {e.get('source')}: missing fields {lack}"); continue
            if e["input"] != "coverage.defenders":
                self.notes.append(f"exception for {e['input']} ignored (only coverage.defenders is exemptable)"); continue
            if e["valid_for_date"] != self.game_date:
                self.notes.append(f"exception {e['source']} ignored: valid_for_date {e['valid_for_date']} != game_date {self.game_date}"); continue
            self.exceptions.append(e)
        if not legs: self.fail("manifest: no legs")
        rows = self.checklist(legs)
        live = {n for n, l in legs.items() if str(l.get("status","")).upper() not in ("CUT","HOLD","MANUAL_REVIEW")}  # MANUAL_REVIEW never live (Rico R1 2026-11-02)
        self.held = sorted(n for n, l in legs.items() if str(l.get("status","")).upper() == "HOLD")
        for n, l in legs.items():
            if str(l.get("status","")).upper() not in _r4.valid_statuses(self.game_date, self.now): self.fail(f"leg {n}: status must be PASS, CUT or HOLD" + (" or MANUAL_REVIEW" if _rb.active("RICO4", self.game_date, self.now) else ""))
        for n in self.held:  # BUGLOG 2026-11-01: missing model/price -> re-pull then HOLD, fail-closed
            h = legs[n].get("hold") or {}
            if not h.get("repull_attempted_et") or not h.get("reason"): self.fail(f"leg {n}: HOLD without a logged re-pull attempt (reason + repull_attempted_et)")
        # flagged gaps: checklist bad statuses must be on CUT legs
        self.gs_waived = self.check_game_script(m, legs, live)
        self.rm_waived = self.check_rbmiss(m, legs, live)
        for n in live:
            bad = [ph for ph, st in rows.get(n, {}).items() if st in BAD | {"HOLD"}]
            if bad == [7] and n in self.gs_waived: bad = []
            if n in self.rm_waived: bad = [ph for ph in bad if ph not in self.rm_waived[n]]
            if bad: self.fail(f"leg {n}: phases {bad} flagged FAIL/MISSING/STALE/UNVERIFIED/HOLD but leg not CUT/HOLD")
            if l_gaps := legs[n].get("gaps"): self.fail(f"leg {n}: has flagged gaps {l_gaps} but leg not CUT")
        # sources
        gflag = {g.get("category"): g for g in m.get("flagged_gaps", [])}
        for cat in CATEGORIES:
            ss = [s for s in m.get("sources", []) if s.get("category") == cat]
            good = False
            for s in ss:
                lab = f"source {cat}/{s.get('name','?')}"
                if not s.get("url_or_file"): self.fail(f"{lab}: no source url/file"); continue
                if self.age_ok(lab, s.get("pulled_et"), cat): good = True
            if not good:
                if cat in gflag and not live: self.notes.append(f"category {cat} gap flagged; all legs CUT")
                elif cat in gflag: self.fail(f"category {cat} gap flagged but legs {sorted(live)} not CUT")
                else: self.fail(f"source category {cat}: missing or no fresh source")
        for s in m.get("sources", []):
            if s.get("category") not in CATEGORIES: self.fail(f"source {s.get('name')}: unknown category {s.get('category')}")
        # pressure inputs (required whenever any leg is live)
        pi = m.get("pressure_inputs", {})
        for k in PRESSURE:
            if k not in pi:
                if live: self.fail(f"pressure/blitz/checkdown input {k} missing")
            else: self.stamped(f"pressure input {k}", pi[k], "coverage_matchups")
        # Lesson 5 (2026-11-01): receiving legs also need QB time to throw and targets under pressure (runs dated >= SIMV6_FROM)
        if _rb.active("SIMV6", self.game_date, self.now) and any(legs[n].get("receiving") or legs[n].get("type") in ("WR","TE") for n in live):
            for k in PRESSURE_W9:
                if k not in pi: self.fail(f"pressure input {k} missing (receiving legs, runs dated >= {SIMV6_FROM})")
                else: self.stamped(f"pressure input {k}", pi[k], "coverage_matchups")
        # sims
        sims = {s.get("model"): s for s in m.get("sims", [])}
        for mo in MODELS:
            s = sims.get(mo)
            if not s:
                if live: self.fail(f"sim model {mo} missing")
                continue
            if not isinstance(s.get("n"), int) or s["n"] < 100000: self.fail(f"sim {mo}: n={s.get('n')} < 100000")
            if s.get("seed") is None: self.fail(f"sim {mo}: seed missing")
            for n in live:
                r = s.get("legs", {}).get(n)
                if not r or r.get("p") is None or r.get("median") is None:
                    self.fail(f"sim {mo}: leg {n} lacks p/median")
        # per live leg: coverage + edge
        for n in sorted(live):
            l = legs[n]
            rec = l.get("receiving") or l.get("type") in ("WR","TE")
            if not rec and _rb.active("COVPROF", self.game_date, self.now) and is_passing(l):   # Rico 2026-11-01: coverage profile every passing leg
                cv = l.get("coverage") or {}
                for k, lab in (("man_zone","man/zone"),("mof","MOF")):
                    if k not in cv: self.fail(f"leg {n}: passing leg defensive coverage profile {lab} missing (opponent man/zone + MOF required)")
                    else: self.stamped(f"leg {n} coverage profile {lab}", cv[k], "coverage_matchups")
            if rec:
                cv = l.get("coverage") or {}
                ds = cv.get("defenders") or []
                if not ds and _rb.active("SNF", self.game_date, self.now) and _snf.wr3_under_team_cov(l):   # SNF S2 Rico Nov 2 8:14 AM ET
                    l.setdefault("flags", []).append("WR3_TEAM_COV"); self.notes.append(f"{n}: WR3+ under passes defender check on team coverage profile (flag WR3_TEAM_COV)")
                elif not ds: self.fail(f"leg {n}: per-defender coverage numbers missing")
                for d in ds:
                    if not all(d.get(k) is not None for k in ("targets","comp_pct","ypt")):
                        self.fail(f"leg {n}: defender {d.get('name')} missing targets/comp_pct/ypt")
                    lab = f"leg {n} defender {d.get('name')}"
                    ex = self.exc_for("coverage.defenders", d.get("source") or d.get("url_or_file"))
                    if ex and parse_t(d.get("pulled_et")):
                        self.applied.append((lab, ex))
                    else:
                        self.stamped(lab, d, "coverage_matchups")
                for k, lab in (("man_zone","man/zone"),("mof","MOF")):
                    if k not in cv: self.fail(f"leg {n}: {lab} coverage missing")
                    else: self.stamped(f"leg {n} {lab}", cv[k], "coverage_matchups")
            ps, meds = [], []
            for mo in MODELS:
                r = sims.get(mo, {}).get("legs", {}).get(n) or {}
                if r.get("p") is not None: ps.append(float(r["p"]))
                if r.get("median") is not None: meds.append(float(r["median"]))
            nv, line, side = l.get("no_vig"), l.get("line"), str(l.get("side","")).lower()
            if nv is None or line is None or side not in ("over","under") or len(ps) < 3:
                self.fail(f"leg {n}: edge-rule inputs missing (need no_vig, line, side, 3 model p)"); continue
            avg = sum(ps)/3   # NOSHRINK (Rico 2026-11-02 21:13 ET): raw model p vs no-vig, the 30% shrink is removed
            se = scheme_edge_ok(l)
            sim_fails = []
            if avg - nv < _rb.param("NOSHRINK","min_edge"): sim_fails.append(f"edge avg(p)-no_vig = {100*(avg-nv):+.1f} pts < +3")
            if min(ps) < _rb.param("NOSHRINK","min_model_p"): sim_fails.append(f"edge a model p {min(ps):.3f} < .45")
            for md in meds:
                if (side == "over" and md <= line) or (side == "under" and md >= line):
                    sim_fails.append(f"edge sim median {md} does not clear {side} {line}")
            if se and sim_fails and not se_explained(l):
                self.fail(f"leg {n}: SCHEME_EDGE needs a plain-words edge explanation (scheme_edge.explanation) to waive the edge cut - missing data, fail closed")
            for f_ in sim_fails:
                if se: self.notes.append(f"{n}: SCHEME_EDGE flag (not a cut): {f_}")
                else: self.fail(f"leg {n}: {f_}")
            if se and sim_fails:   # Rico 2026-11-02 23:52 ET: flag, Ghost6 checks at real price, Rico gets full breakdown
                bd = [f"{n} [{side} {line}, book price {l.get('price_fd', l.get('price'))}]",
                      f"  price: no-vig {nv:.3f}, avg model p {avg:.3f}, raw edge {100*(avg-nv):+.1f} pts (+3 bar waived by SCHEME_EDGE; check at real price)"]
                for mo in MODELS:
                    r = sims.get(mo, {}).get("legs", {}).get(n) or {}
                    p_, md = r.get("p"), r.get("median")
                    clr = (p_ is not None and p_ >= 0.45) and (md is not None and ((side == "over" and md > line) or (side == "under" and md < line)))
                    bd.append(f"  model {mo}: p {p_}, sim median {md} vs {line} -> {'CLEARS' if clr else 'DOES NOT CLEAR'}")
                for k in SCHEME_KEYS:
                    c = l["scheme_edge"][k]; bd.append(f"  {k}: {c.get('detail','')} (source: {c['source']})")
                bd.append(f"  edge in plain words: {l['scheme_edge'].get('explanation') or 'MISSING - build must write why this player beats this defense'}")
                bd.append("  flags: " + "; ".join(sim_fails))
                self.__dict__.setdefault("se_breakdowns", []).append(bd)
            self.notes.append(f"{n}: avg p {avg:.3f}, no-vig {nv:.3f}, raw edge {100*(avg-nv):+.1f}" + (" [SCHEME_EDGE]" if se else ""))
            self.check_form(n, l, line, side)
        self.check_weather(m, legs, live)
        self.check_forecast(m, legs, live)
        self.check_cross_checks(m)
        self.check_pff(m, legs, live)
        self.check_simv6(m)
        self.check_srclist(m, legs, live)   # SRC-1/2/3/5 (srclist_rules.py, Rico 2026-11-01 22:47 ET)
        self.check_snf(m, legs, live)       # SNF postmortem S1-S4 (snf_rules.py), Rico Nov 2 8:14 AM ET; runs >= 2026-11-02 (MNF) per Rico card 8:19 AM ET
        self.check_rico4(m, legs, live)     # Rico 2026-11-02 05:01 ET R1-R4 (rico4_rules.py), runs >= 2026-11-05
        self.check_depth(m, legs, live)     # DEPTH_RECEIVER (depth_rule.py) replaces the #3/#4 ban
        _n2.check(self, m, legs, live)      # Rico 2026-11-02 23:31 ET N1 RB 60% share, N2 primary defender, N3 period spreads match script (rico_nov2_rules.py)
        self.manual = sorted(n for n, l in legs.items() if str(l.get("status","")).upper() == "MANUAL_REVIEW")
        self.live, self.cut = sorted(live), sorted(set(legs) - live - set(getattr(self, "held", [])) - set(self.manual))
        self.check_risks()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import srclist_rules as _src; _src.install(Gate); wx_source_ok = _src.wx_source_ok
import rico4_rules as _r4; _r4.install(Gate)
import snf_rules as _snf; _snf.install(Gate)
import rico_nov2_rules as _n2
import depth_rule as _dr; _dr.install(Gate)
def main():
    a = argparse.ArgumentParser(); a.add_argument("run_dir"); a.add_argument("--now")
    a.add_argument("--press-tier", action="store_true", help="OPT-IN advisory PRESS tier (press_tier.py); never changes pass/fail")
    a.add_argument("--press-models", type=int, default=None)
    o = a.parse_args()
    now = parse_t(o.now) if o.now else datetime.now()
    g = Gate(o.run_dir, now); g.live = g.cut = []; g.applied = []; g.wx_alerts = []
    g.run()
    ok = not g.miss
    out = [f"GATE: {'PASS' if ok else 'FAIL'}  run={os.path.abspath(o.run_dir)}  checked_at={now:%Y-%m-%d %H:%M} ET",
           f"Live legs: {g.live or 'none'}", f"Cut legs: {g.cut or 'none'}"]
    if getattr(g, "held", None): out += [f"Held legs (missing model/price after re-pull; blocked, fail-closed): {g.held}"]
    if g.applied:
        out += ["APPROVED EXCEPTIONS:"]
        for lab, e in g.applied:
            out.append(f"  - {lab}: {e['input']} from {e['source']} (staleness waived; approved by {e['approved_by']} on {e['approved_on']}, valid {e['valid_for_date']}, scope {e['scope']}) — {e['reason']}")
    for gm, why, placed in g.wx_alerts:
        out += [f"WEATHER ALERT: {gm} flagged ({', '.join(why)}). User's placed legs in this game:"] + ([f"  - {p}" for p in placed] or ["  - none found"])
    out += getattr(g, "fc_alerts", [])
    out += getattr(g, "gs_notes", [])
    out += getattr(g, "rm_notes", [])
    out += getattr(g, "pff_notes", [])
    out += getattr(g, "pff_pick_notes", []) + getattr(g, "sharp_notes", [])
    out += g.mr_section() if hasattr(g, "mr_section") else []
    out += (["SNF RULES:"] + [f"  - {x}" for x in g.snf_notes]) if getattr(g, "snf_notes", None) else []
    out += (["RICO NOV 2 RULES (N1-N3):"] + [f"  - {x}" for x in g.nov2_notes]) if getattr(g, "nov2_notes", None) else []
    for bd in getattr(g, "se_breakdowns", []): out += ["SCHEME_EDGE ALERT (under +3 or sim flag; Ghost6 checks at real price, send Rico this breakdown):"] + bd
    if g.miss: out += [f"MISSES ({len(g.miss)}):"] + [f"  - {x}" for x in g.miss]
    if g.notes: out += ["Notes:"] + [f"  - {x}" for x in g.notes]
    import press_live as _pl
    if not o.press_tier and _pl.active_for(getattr(g, "game_date", "")):  # Week 9+ default ON via gate_config.json; never touches ok / exit code
        try: out += _pl.apply(o.run_dir, g.game_date, g.live or [], blocked=getattr(g, "press_blocked", None))
        except Exception as e: out += [f"PRESS TIER: not applied ({e}); all legs STANDARD"]
    if o.press_tier:  # opt-in, advisory only: does not touch ok / exit code
        import press_tier as _pt
        try: _legs = json.load(open(os.path.join(o.run_dir, "run_manifest.json"), encoding="utf-8")).get("legs", [])
        except Exception: _legs = []
        out += [f"PRESS TIER (advisory, opt-in; models_required={o.press_models or _pt.DEFAULT_MODELS_REQUIRED}):"]
        for l in _legs:
            if l.get("name") in (g.live or []):
                r = _pt.evaluate(l.get("press") or {}, o.press_models or _pt.DEFAULT_MODELS_REQUIRED)
                if l["name"] in (getattr(g, "press_blocked", None) or {}): r = dict(tier="BLOCKED", reason=f"{g.press_blocked[l['name']]} overrides PRESS (SRC-3)")
                out.append(f"  - {l['name']}: {r['tier']} ({r['reason']})")
    txt = "\n".join(out) + "\n"; print(txt, end="")
    try: open(os.path.join(o.run_dir, "gate_output.txt"), "w").write(txt)
    except OSError as e: print(f"could not write gate_output.txt: {e}", file=sys.stderr)
    sys.exit(0 if ok else 1)

if __name__ == "__main__": main()
