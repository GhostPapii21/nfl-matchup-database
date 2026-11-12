"""Source-list rules (Rico 2026-11-01 22:47 ET; audits/SOURCE_AUDIT_2026-11-01.md, audits/2026-11-01_srclist/).
Mixed into run_gate.Gate. SRC-1 weather whitelist, SRC-2 PFF picks re-priced at our book line, SRC-3 Sharp needs an
agreeing second source, SRC-5 every feed on the latest week and right season. (SRC-4 lives in pull_odds.py / pull_props.py.)"""
import re
from datetime import datetime
MODELS = ["monte_carlo","bias","game_randomness"]
# SRC-1: NWS (api.weather.gov) or Open-Meteo only; matches tools/weather_forecast.py providers "nws" / "open-meteo".
WX_ALLOWED = re.compile(r"api\.weather\.gov|(^|[^a-z.])weather\.gov|open-meteo|\bnws\b|nws_|weather_forecast\.py", re.I)
WX_PROVIDERS = ("nws", "open-meteo", "open_meteo", "nws+open-meteo")
PFF_RX = re.compile(r"pff", re.I)
SHARP_RX = re.compile(r"sharp", re.I)
SHARP_SECOND_OK = re.compile(r"statrankings|ftn|nflverse|play.?by.?play|\bpbp\b", re.I)
FEEDWEEK_FROM = "2026-11-05"
LABEL_CATS = ("injuries_news", "weather", "odds_props")   # must be labelled THIS week; other categories = data through last week
def _pt(s):
    try: return datetime.fromisoformat(str(s).strip().replace(" ", "T")[:16]) if s else None
    except ValueError: return None
def wx_source_ok(w):
    """True only if the weather input names NWS/Open-Meteo and nothing PFF (fail closed)."""
    txt = " ".join(str(w.get(k) or "") for k in ("source", "url_or_file", "file", "name", "tool", "provider"))
    if PFF_RX.search(txt): return False
    prov = str(w.get("provider") or "").lower()
    if prov and not all(p.strip() in WX_PROVIDERS for p in re.split(r"[;,+ ]+", prov) if p.strip()) and prov not in WX_PROVIDERS: return False
    return bool(WX_ALLOWED.search(txt))

def check_wx_sources(self, m):
    """SRC-1: weather block entries, weather sources and the weather_forecast block must be NWS/Open-Meteo, never PFF."""
    W = m.get("weather") if isinstance(m.get("weather"), dict) else {}
    if "roof" in W: W = {str(m.get("game")): W}
    for g, w in W.items():
        if isinstance(w, dict) and (w.get("source") or w.get("url_or_file")) and not wx_source_ok(w):
            self.fail(f"Phase 11 weather {g}: source {w.get('source') or w.get('url_or_file')!r} not allowed — weather from NWS/Open-Meteo only, never PFF (SRC-1)")
    for s in m.get("sources", []):
        if s.get("category") == "weather" and s.get("url_or_file") and not wx_source_ok(s):
            self.fail(f"source weather/{s.get('name')}: not allowed — weather from NWS/Open-Meteo only, never PFF (SRC-1)")
    F = m.get("weather_forecast")
    if isinstance(F, dict):
        if (F.get("source") or F.get("file")) and not wx_source_ok(F):
            self.fail(f"weather forecast: source {F.get('source') or F.get('file')!r} not allowed — NWS/Open-Meteo only, never PFF (SRC-1)")
        for g, e in (F.get("games") or {}).items():
            if isinstance(e, dict) and any(e.get(k) for k in ("provider", "source", "url_or_file")) and not wx_source_ok(e):
                self.fail(f"weather forecast {g}: provider/source {e.get('provider') or e.get('source')!r} not allowed — NWS/Open-Meteo only (SRC-1)")

def check_pff_picks(self, m, legs, live):
    """SRC-2: re-price every PFF pick at our book's current line (odds age rule) and recompute p with all 3 of our models.
    PFF's edge % is never used: edge_basis must be 'our_model'; uses_pff_edge must not be set."""
    for n, l in legs.items():
        if PFF_RX.search(str(l.get("edge_basis") or "")) or l.get("uses_pff_edge"):
            self.fail(f"leg {n}: edge taken from PFF edge % (edge_basis {l.get('edge_basis')!r}) — PFF edge % is ignored; use our model at our book line (SRC-2)")
    P = m.get("pff_picks")
    if not P: return
    picks = {}; self.pff_pick_notes = ["PFF PICKS (re-priced at our book line; PFF edge % ignored):"]
    for x in P:
        lab = f"PFF pick {x.get('player','?')} {x.get('market','?')} {x.get('side','?')}"
        if x.get("uses_pff_edge") or str(x.get("edge_basis") or "") != "our_model":
            self.fail(f"{lab}: edge_basis {x.get('edge_basis')!r} — PFF edge % is ignored; edge_basis must be 'our_model' (SRC-2)"); continue
        if not isinstance(x.get("book_line"), (int, float)) or not x.get("book") or not isinstance(x.get("book_price"), (int, float)):
            self.fail(f"{lab}: not re-priced — book, book_line and book_price at our book are required (SRC-2)"); continue
        if PFF_RX.search(str(x.get("book"))): self.fail(f"{lab}: book is PFF — re-price at our book (SRC-2)"); continue
        if not self.age_ok(f"{lab} book line", x.get("pulled_et"), "odds_props"): continue
        mp = x.get("model_p") or {}
        lack = [mo for mo in MODELS if not isinstance(mp.get(mo), (int, float))]
        if lack: self.fail(f"{lab}: our model p missing for {lack} — recompute with all 3 models (SRC-2)"); continue
        picks[(x.get("player"), str(x.get("market","")).lower(), str(x.get("side","")).lower())] = x
        self.pff_pick_notes.append(f"  - {lab}: PFF line {x.get('pff_line')} -> {x['book']} {x['book_line']} @ {x['book_price']:+.0f}; our avg p {sum(mp[mo] for mo in MODELS)/3:.3f} (PFF edge % ignored)")
    for n, l in legs.items():
        if not l.get("pff_pick"): continue
        k = (l.get("player"), str(l.get("market","")).lower(), str(l.get("side","")).lower())
        x = picks.get(k) or (next(iter(picks.values())) if len(picks) == 1 and not l.get("player") else None)
        if not x: self.fail(f"leg {n}: flagged pff_pick but no re-priced pff_picks entry (SRC-2)"); continue
        if l.get("line") != x.get("book_line"): self.fail(f"leg {n}: line {l.get('line')} is not our book line {x.get('book_line')} from the re-price (SRC-2)")

def check_sharp(self, m, legs, live):
    """SRC-3: Sharp coverage counts only with an agreeing second source (StatRankings, FTN/nflverse or our pbp).
    Sharp alone / disagreeing = SHARP CAUTION (never a fail) and legs citing Sharp coverage cannot be PRESS. Returns {leg: reason}."""
    sh = [s for s in m.get("sources", []) if s.get("category") == "coverage_matchups" and SHARP_RX.search(f"{s.get('name','')} {s.get('url_or_file','')}")]
    self.sharp_notes = []
    if not sh: return {}
    why = []
    for s in sh:
        ss = s.get("second_source")
        if not isinstance(ss, dict): why.append(f"{s.get('name')}: no second source"); continue
        nm = f"{ss.get('name','')} {ss.get('url_or_file') or ss.get('source') or ''}"
        if PFF_RX.search(nm) or SHARP_RX.search(nm) or not SHARP_SECOND_OK.search(nm): why.append(f"{s.get('name')}: second source {ss.get('name')!r} is not StatRankings/FTN/nflverse/our pbp"); continue
        if not (ss.get("url_or_file") or ss.get("source")) or _pt(ss.get("pulled_et")) is None: why.append(f"{s.get('name')}: second source lacks file/pull time"); continue
        if ss.get("agrees") is not True: why.append(f"{s.get('name')}: {ss.get('name')} disagrees"); continue
    if not why:
        self.sharp_notes = [f"SHARP coverage confirmed by {s['second_source'].get('name')}" for s in sh]; return {}
    self.sharp_notes = [f"SHARP CAUTION: Sharp coverage not confirmed ({'; '.join(why)}); legs citing Sharp coverage cannot be PRESS (SRC-3)"]
    blk = {}
    for n in live:
        cv = legs.get(n, {}).get("coverage") or {}
        if any(isinstance(v, dict) and SHARP_RX.search(str(v.get("source") or "")) for v in cv.values()):
            blk[n] = "Sharp-only coverage (no agreeing second source)"
    if blk: self.sharp_notes.append(f"  - press blocked: {sorted(blk)}")
    return blk

def check_feed_weeks(self, m):
    """SRC-5 (runs dated >= FEEDWEEK_FROM): every source, PFF input and PFF pick records season, data_week and pulled_et.
    Fails: wrong season; label feed (injuries/news, weather, odds, PFF) not on this week; results feed (pbp, NGS, film,
    coverage) whose data stops before last week."""
    if str(getattr(self, "game_date", "")) < FEEDWEEK_FROM: return
    season, week = m.get("season"), m.get("week")
    if not isinstance(season, int) or not isinstance(week, int): self.fail("feed weeks: manifest season/week missing (fail closed, SRC-5)"); return
    items = [(f"source {s.get('category')}/{s.get('name','?')}", s, s.get("category")) for s in m.get("sources", [])]
    items += [(f"PFF input {x.get('leg','?')}/{x.get('metric','?')}", dict(x, week_kind=x.get("week_kind", "label")), "pff") for x in m.get("pff_inputs", []) or []]
    items += [(f"PFF pick {x.get('player','?')}", dict(x, week_kind=x.get("week_kind", "label")), "pff") for x in m.get("pff_picks", []) or []]
    for lab, s, cat in items:
        lack = [k for k in ("season", "data_week", "pulled_et") if s.get(k) in (None, "")]
        if lack: self.fail(f"{lab}: feed stamp missing {lack} (fail closed, SRC-5)"); continue
        try: fs, fw = int(s["season"]), int(s["data_week"])
        except (TypeError, ValueError): self.fail(f"{lab}: season/data_week not integers (SRC-5)"); continue
        if fs != season: self.fail(f"{lab}: season {fs} != run season {season} — wrong season (SRC-5)"); continue
        kind = s.get("week_kind") or ("label" if cat in LABEL_CATS else "through")
        if kind == "label" and fw != week: self.fail(f"{lab}: serving week {fw} for a week {week} run — feed not on the latest week (SRC-5)")
        elif kind != "label" and fw < week - 1: self.fail(f"{lab}: data through week {fw}, {week - 1 - fw} week(s) behind (need through week {week - 1}) (SRC-5)")

def run_all(self, m, legs, live):
    check_wx_sources(self, m); check_pff_picks(self, m, legs, live)
    self.press_blocked = check_sharp(self, m, legs, live); check_feed_weeks(self, m)
def install(Gate):
    Gate.check_wx_sources = check_wx_sources; Gate.check_pff_picks = check_pff_picks
    Gate.check_sharp = check_sharp; Gate.check_feed_weeks = check_feed_weeks; Gate.check_srclist = run_all
