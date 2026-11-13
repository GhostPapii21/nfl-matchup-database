"""Grade the research artifacts committed for one game (analyst runs, previews, locked snapshots, 100k ledgers).

Called from grading.grade after the packet is graded. Discovers, for game <season>_<wk>_<AWAY>_<HOME>:
  * research/runs/*_<AWAY>_<HOME>*/legs.json          leg ladder (analyst read probabilities)
  * research/runs/*_<AWAY>_<HOME>*/script_layer.json  script scores, side probabilities, legs
  * research/runs/*_<AWAY>_<HOME>*/*preview_result.json  engine preview (team scores and probabilities)
  * research/runs/*_<AWAY>_<HOME>*/grading_spec.json  flagged props, team reads and slips transcribed from REPORT.md
  * snapshots/<game>/*/summary.json                    locked 100k snapshot (team scores and probabilities)
  * pipeline/ledgers/<game>.sim100k.json               official 100k ledger (graded only if it ran)

Probabilities typed or computed by an analyst are labelled "analyst read", never "edge" (work order item 4).
Alt-ladder legs (X+) have no saved alt price in the repo, so their closing line is "unknown"; the latest saved
pre-kickoff main line for the same player and stat is shown as reference only. Nothing here changes a model.
"""
from __future__ import annotations

import glob
import json
import re
from pathlib import Path

from . import core as C
from .sources import ROOT

ANALYST = "analyst read (not an engine or fitted-model edge)"
LEG_RE = re.compile(r"^(?:(?P<init>[A-Z])\.)?(?P<name>[A-Za-z'\-]+) (?:(?P<thr>\d+)\+|O(?P<over>\d+(?:\.5)?)) (?P<kind>rec yds|yds|rec|rush\+rec|R\+R|rush)$")
TOTAL_RE = re.compile(r"^(?P<side>Under|Over) (?P<line>\d+(?:\.5)?)$")
KIND_STAT = {"yds": "receiving_yards", "rec yds": "receiving_yards", "rec": "receptions", "rush": "rushing_yards",
             "R+R": "rush_rec_yards", "rush+rec": "rush_rec_yards"}


def parse_leg(name: str) -> dict | None:
    m = LEG_RE.match(name.strip())
    if m:
        line = float(m["thr"]) - 0.5 if m["thr"] else float(m["over"])
        return {"type": "player", "surname": m["name"], "initial": m["init"], "stat": KIND_STAT[m["kind"]],
                "side": "Over", "line": line}
    m = TOTAL_RE.match(name.strip())
    if m:
        return {"type": "game_total", "side": m["side"], "line": float(m["line"])}
    m = re.match(r"^(?P<team>[A-Z]{2,3}) 1H 3-way$", name.strip())
    if m:
        return {"type": "first_half_win", "team": m["team"]}
    return None


def run_dirs(game_id: str, root: Path = ROOT) -> list[Path]:
    _, _, away, home = game_id.split("_")
    return [Path(p) for p in sorted(glob.glob(str(root / "research" / "runs" / f"*_{away}_{home}*"))) if Path(p).is_dir()]


def _rel(p: Path, root: Path) -> str:
    try:
        return str(p.relative_to(root))
    except ValueError:
        return str(p)


def _commit_time(path: Path, root: Path) -> str:
    import subprocess
    try:
        out = subprocess.run(["git", "-C", str(root), "log", "-1", "--format=%cI", "--", _rel(path, root)],
                             capture_output=True, text=True, check=True).stdout.strip()
        return out or C.UNKNOWN
    except Exception:
        return C.UNKNOWN


class Ctx:
    def __init__(self, game_id, actuals, snapshots, kickoff, home, away, root, now):
        self.game_id, self.a, self.snaps, self.kickoff, self.home, self.away, self.root, self.now = \
            game_id, actuals, snapshots, kickoff, home, away, root, now
        self.src, self.pulled = actuals.src("pbp")
        hs, as_ = actuals.score(home), actuals.score(away)
        self.hs, self.as_ = hs, as_
        self.total = hs + as_ if C.known(hs) and C.known(as_) else C.UNKNOWN
        self.margin = hs - as_ if C.known(hs) and C.known(as_) else C.UNKNOWN

    def base(self, kind, artifact, committed, extra):
        return {"schema": "grading.research.v1", "game_id": self.game_id, "kickoff_utc": self.kickoff.isoformat(),
                "graded_utc": self.now.isoformat(timespec="seconds"), "kind": kind, "projection_ready": False,
                "artifact": {"path": artifact, "committed_utc": committed}, **extra}

    def player_actual(self, leg, team=None):
        if hasattr(self.a, "resolve_surname"):
            who = self.a.resolve_surname(leg["surname"], team, leg.get("initial"))
        else:
            who = {"gsis_id": C.UNKNOWN, "team": C.UNKNOWN, "reason": "surname matching needs the ESPN box score"}
        t = who.get("team")
        if leg["stat"] == "rush_rec_yards":
            r = self.a.stat(who.get("gsis_id"), who.get("full_name"), t, "rushing_yards")
            c = self.a.stat(who.get("gsis_id"), who.get("full_name"), t, "receiving_yards")
            val = r + c if C.known(r) and C.known(c) else C.UNKNOWN
        else:
            val = self.a.stat(who.get("gsis_id"), who.get("full_name"), t, leg["stat"])
        return who, val

    def main_line_ref(self, full_name, stat, book="fanduel"):
        if stat == "rush_rec_yards" or not C.known(full_name):
            return C.fig(None, note="no saved main market for this stat")
        cq = C.closing_quote(self.snaps, f"{stat}|{full_name}", book, self.kickoff)
        if not cq:
            return C.fig(None, note=f"no saved pre-kickoff {book} main line")
        return C.fig(cq.get("line"), cq.get("source"), cq.get("snapshot_utc"), book=book, prices=json.dumps(cq.get("prices")),
                     note="reference only: main line, not the alt rung graded")

    def grade_leg(self, name, artifact, committed, probs: dict, kind="research_leg"):
        leg = parse_leg(name)
        extra = {"leg": name, "parsed": leg or C.UNKNOWN,
                 "analyst_probabilities": {k: C.fig(v, artifact, committed, label=ANALYST) for k, v in probs.items()}}
        if leg is None:
            return self.base(kind, artifact, committed, {**extra, "actual": C.fig(None), "result": C.UNKNOWN,
                                                         "closing_line": C.fig(None, note="leg name not parseable")})
        if leg["type"] == "player":
            who, val = self.player_actual(leg)
            extra.update(player=who.get("full_name", C.UNKNOWN), team=C.u(who.get("team")),
                         player_match=who.get("reason") or "surname (+initial) in ESPN box score",
                         actual=C.fig(val, self.src, self.pulled, stat=leg["stat"]),
                         result=C.prop_result(val, leg["side"], leg["line"]),
                         margin_vs_rung=round(float(val) - leg["line"], 1) if C.known(val) else C.UNKNOWN,
                         closing_line=C.fig(None, note="alt rung: no alt price saved in the repo; closing line unknown"),
                         clv={"positive": C.UNKNOWN, "reason": "no saved alt-rung price before or at close"},
                         closing_main_line_reference=self.main_line_ref(who.get("full_name"), leg["stat"]))
        elif leg["type"] == "game_total":
            extra.update(actual=C.fig(self.total, self.src, self.pulled, stat="total_points"),
                         result=C.prop_result(self.total, leg["side"], leg["line"]),
                         closing_line=C.fig(None, note="alt total: no alt price saved; closing line unknown"),
                         clv={"positive": C.UNKNOWN, "reason": "no saved alt total price"},
                         closing_main_line_reference=self._team_ref("total"))
        else:
            t = leg["team"]; o = self.away if t == self.home else self.home
            h1t = self.a.half_score(t, 1) if hasattr(self.a, "half_score") else C.UNKNOWN
            h1o = self.a.half_score(o, 1) if hasattr(self.a, "half_score") else C.UNKNOWN
            res = C.UNKNOWN if not (C.known(h1t) and C.known(h1o)) else ("win" if h1t > h1o else "loss")
            extra.update(actual=C.fig(f"{t} {h1t} - {o} {h1o}" if C.known(h1t) else None, self.src, self.pulled, stat="first_half_score"),
                         result=res, closing_line=C.fig(None, note="1H 3-way price MISSING from packet (REPORT.md:57)"),
                         clv={"positive": C.UNKNOWN, "reason": "no saved price"})
        return self.base(kind, artifact, committed, extra)

    def _team_ref(self, market, book="fanduel"):
        cq = C.closing_quote(self.snaps, market, book, self.kickoff)
        if not cq:
            return C.fig(None, note=f"no saved pre-kickoff {book} {market}")
        return C.fig(cq.get("line"), cq.get("source"), cq.get("snapshot_utc"), book=book, prices=json.dumps(cq.get("prices")))

    def team_projection(self, artifact, committed, label, proj: dict):
        rows = []
        actual = {"home_points": self.hs, "away_points": self.as_, "total": self.total, "home_margin": self.margin}
        for q, v in proj.items():
            if q not in actual:
                continue
            err = round(float(actual[q]) - float(v), 2) if C.known(actual[q]) and C.known(v) else C.UNKNOWN
            rows.append(self.base("research_team_projection", artifact, committed, {
                "source_label": label, "quantity": q, "projection": C.fig(v, artifact, committed),
                "actual": C.fig(actual[q], self.src, self.pulled), "error_actual_minus_projection": err}))
        return rows

    def team_prob(self, artifact, committed, label, name, p, outcome):
        """A probability for an event; Brier = (p - outcome)^2 with outcome 1/0, unknown if either is unknown."""
        brier = round((float(p) - outcome) ** 2, 4) if C.known(p) and outcome in (0, 1) else C.UNKNOWN
        return self.base("research_team_probability", artifact, committed, {
            "source_label": label, "event": name, "probability": C.fig(p, artifact, committed, label=ANALYST if "script" in label else "engine output, research only"),
            "outcome": outcome if outcome in (0, 1) else C.UNKNOWN, "brier": brier})

    def outcome(self, event: str):
        """Resolve NYG -1.5 / NYG ML / Under 40.5 / Over 40.5 / NYG win style events to 1/0/'push'/unknown."""
        if not C.known(self.margin):
            return C.UNKNOWN
        m = re.match(r"^(?P<t>[A-Z]{2,3}) (?P<l>[+-]\d+(?:\.\d)?)$", event)
        if m:
            t, l = m["t"], float(m["l"])
            mt = self.margin if t == self.home else -self.margin
            return "push" if mt + l == 0 else int(mt + l > 0)
        m = re.match(r"^(?P<t>[A-Z]{2,3}) (ML|win)$", event)
        if m:
            mt = self.margin if m["t"] == self.home else -self.margin
            return C.UNKNOWN if mt == 0 else int(mt > 0)
        m = TOTAL_RE.match(event)
        if m:
            l = float(m["line"])
            if self.total == l:
                return "push"
            return int((self.total > l) == (m["side"] == "Over"))
        return C.UNKNOWN


def _bet_quote(snaps, key, book, before):
    """Latest snapshot from the packet books section (the quote the report used)."""
    cands = [s for s in snaps if s.get("market_key") == key and s.get("book") == book and "#books" in str(s.get("source"))]
    cands = [s for s in cands if C.parse_utc(s.get("snapshot_utc")) and C.parse_utc(s["snapshot_utc"]) < before]
    return max(cands, key=lambda s: C.parse_utc(s["snapshot_utc"])) if cands else None


def grade_research(game_id, actuals, snapshots, kickoff, home, away, now, root: Path = ROOT) -> list[dict]:
    ctx = Ctx(game_id, actuals, snapshots, kickoff, home, away, root, now)
    rows: list[dict] = []
    for d in run_dirs(game_id, root):
        legs_p = d / "legs.json"
        if legs_p.exists():
            art, com = _rel(legs_p, root), _commit_time(legs_p, root)
            for name, probs in json.loads(legs_p.read_text()).items():
                rows.append(ctx.grade_leg(name, art, com, probs if isinstance(probs, dict) else {"p": probs}))
        sl_p = d / "script_layer.json"
        if sl_p.exists():
            art, com = _rel(sl_p, root), _commit_time(sl_p, root)
            sl = json.loads(sl_p.read_text())
            h, a = sl.get(home.lower()), sl.get(away.lower())
            proj = {"home_points": h, "away_points": a}
            if C.known(h) and C.known(a):
                proj.update(total=round(h + a, 2), home_margin=round(h - a, 2))
            rows += ctx.team_projection(art, com, "game script (script-based, not a sim)", proj)
            for ev, p in (sl.get("p") or {}).items():
                if "1H" in ev:
                    r = ctx.grade_leg(ev, art, com, {"script": p}, kind="research_team_probability")
                    r["source_label"] = "game script"
                    rows.append(r)
                    continue
                rows.append(ctx.team_prob(art, com, "game script (script-based, not a sim)", ev, p, ctx.outcome(ev)))
            for name, p in (sl.get("legs") or {}).items():
                rows.append(ctx.grade_leg(name, art, com, {"script": p}))
        for pv in sorted(d.glob("*preview_result.json")):
            art, com = _rel(pv, root), _commit_time(pv, root)
            r = json.loads(pv.read_text())
            lab = f"engine preview n={r.get('n')} seed={r.get('seed')} commit={r.get('commit')} (research only)"
            rows += ctx.team_projection(art, com, lab, {"home_points": r.get(f"{home}_mean"), "away_points": r.get(f"{away}_mean"),
                                                        "total": r.get("total_mean"), "home_margin": r.get("margin_mean")})
            for k, v in r.items():
                m = re.match(rf"^p_({home}|{away})_(win|cover_)(.*)$", k)
                if m:
                    ev = f"{m[1]} win" if m[2] == "win" else f"{m[1]} {m[3].replace('_', '.')}"
                    rows.append(ctx.team_prob(art, com, lab, ev, v, ctx.outcome(ev)))
                m = re.match(r"^p_(over|under)_(\d+)_(\d)$", k)
                if m:
                    ev = f"{m[1].title()} {m[2]}.{m[3]}"
                    rows.append(ctx.team_prob(art, com, lab, ev, v, ctx.outcome(ev)))
        sp = d / "grading_spec.json"
        if sp.exists():
            rows += _grade_spec(ctx, sp, root, rows)
    for s in sorted(glob.glob(str(root / "snapshots" / game_id / "*" / "summary.json"))):
        sp = Path(s)
        art, com = _rel(sp, root), _commit_time(sp, root)
        r = json.loads(sp.read_text())
        lab = f"locked snapshot {sp.parent.name} n={r.get('n')} (research only)"
        pts = r.get("points") or {}
        rows += ctx.team_projection(art, com, lab, {"home_points": pts.get(home), "away_points": pts.get(away),
                                                    "total": (r.get("total") or {}).get("mean"),
                                                    "home_margin": (r.get("margin_home") or {}).get("mean")})
        rows.append(ctx.team_prob(art, com, lab, f"{home} win", r.get("p_home_win"), ctx.outcome(f"{home} win")))
    led = root / "pipeline" / "ledgers" / f"{game_id}.sim100k.json"
    if led.exists():
        r = json.loads(led.read_text())
        rows.append(ctx.base("official_100k", _rel(led, root), _commit_time(led, root), {
            "status": r.get("status", C.UNKNOWN), "ran": r.get("ran", C.UNKNOWN),
            "note": "nothing to grade: the official 100k did not run" if not r.get("ran") else "ran; see ledger",
            "reasons": r.get("reasons") or []}))
    return rows


def _grade_spec(ctx: Ctx, sp: Path, root: Path, prior_rows: list[dict]) -> list[dict]:
    spec = json.loads(sp.read_text())
    art, com = _rel(sp, root), _commit_time(sp, root)
    rows = []
    for f in spec.get("flagged_props") or []:
        who = ctx.a.resolve_full(f["player"], f.get("team"))
        val = ctx.a.stat(who.get("gsis_id"), f["player"], who.get("team"), f["stat"])
        key = f"{f['stat']}|{f['player']}"
        bq = _bet_quote(ctx.snaps, key, f["book"], ctx.kickoff)
        cq = C.closing_quote(ctx.snaps, key, f["book"], ctx.kickoff)
        side = f.get("side")
        clv = C.clv(f["stat"], side, ctx.home, (bq or {}).get("line"), (bq or {}).get("prices") or {}, cq,
                    bet_utc=(bq or {}).get("snapshot_utc")) if side and bq else {"positive": C.UNKNOWN, "reason": "no side (Pass) or no saved bet quote"}
        rows.append(ctx.base("report_flagged_prop", art, com, {
            "cite": f.get("cite"), "player": f["player"], "team": f.get("team"), "stat": f["stat"], "side": C.u(side),
            "tier": f.get("tier"), "analyst_read": C.fig(f.get("analyst_read"), art, com, label=ANALYST),
            "book": f["book"], "report_line": f["line"],
            "bet_quote": C.fig((bq or {}).get("line"), (bq or {}).get("source"), (bq or {}).get("snapshot_utc"),
                               prices=json.dumps((bq or {}).get("prices")) if bq else None),
            "actual": C.fig(val, ctx.src, ctx.pulled), "result": C.prop_result(val, side, f["line"]) if side else C.UNKNOWN,
            "actual_vs_line": ("over" if C.known(val) and val > f["line"] else "under" if C.known(val) else C.UNKNOWN),
            "closing_line": C.fig((cq or {}).get("line"), (cq or {}).get("source"), (cq or {}).get("snapshot_utc"),
                                  book=f["book"], prices=json.dumps((cq or {}).get("prices")) if cq else None,
                                  note="latest snapshot saved in this repo before kickoff; not claimed to be the true close"),
            "clv": clv}))
    for t in spec.get("team_reads") or []:
        mkt, book, side = t["market"], t["book"], t["side"]
        bq = _bet_quote(ctx.snaps, mkt, book, ctx.kickoff)
        cq = C.closing_quote(ctx.snaps, mkt, book, ctx.kickoff)
        if mkt == "spread":
            res = C.spread_result(ctx.hs, ctx.as_, t["home_line"], side, ctx.home)
        elif mkt == "total":
            res = C.prop_result(ctx.total, side, t["line"])
        else:
            res = C.moneyline_result(ctx.hs, ctx.as_, side, ctx.home)
        clv = C.clv(mkt, side, ctx.home, (bq or {}).get("line"), (bq or {}).get("prices") or {}, cq,
                    bet_utc=(bq or {}).get("snapshot_utc")) if bq else {"positive": C.UNKNOWN, "reason": "no saved bet quote"}
        rows.append(ctx.base("report_team_read", art, com, {
            "cite": t.get("cite"), "market": mkt, "side": side, "tier": t.get("tier"), "book": book,
            "report_line": t.get("home_line", t.get("line")),
            "bet_quote": C.fig((bq or {}).get("line"), (bq or {}).get("source"), (bq or {}).get("snapshot_utc"),
                               prices=json.dumps((bq or {}).get("prices")) if bq else None),
            "actual": C.fig(ctx.margin if mkt != "total" else ctx.total, ctx.src, ctx.pulled,
                            stat="home_margin" if mkt != "total" else "total_points"),
            "result": res,
            "closing_line": C.fig((cq or {}).get("line"), (cq or {}).get("source"), (cq or {}).get("snapshot_utc"),
                                  book=book, prices=json.dumps((cq or {}).get("prices")) if cq else None),
            "clv": clv}))
    for s in spec.get("slips") or []:
        legs = [ctx.grade_leg(n, art, com, {}, kind="slip_leg") for n in s["legs"]]
        results = [l["result"] for l in legs]
        if any(r == "loss" for r in results):
            slip = "loss"
        elif not s.get("complete", True) or any(r not in ("win",) for r in results):
            slip = C.UNKNOWN
        else:
            slip = "win"
        rows.append(ctx.base("report_slip", art, com, {
            "cite": s.get("cite"), "slip": s["slip"], "price": s.get("price"), "stake_usd": s.get("stake_usd"),
            "complete_leg_list": s.get("complete", True), "note": s.get("note", ""),
            "legs": [{"leg": l["leg"], "actual": l["actual"]["value"], "result": l["result"],
                      "margin_vs_rung": l.get("margin_vs_rung", C.UNKNOWN)} for l in legs],
            "legs_hit": sum(r == "win" for r in results), "legs_listed": len(results), "result": slip,
            "closing_line": C.fig(None, note="SGP price at close not saved; unknown")}))
    return rows


def summarize_research(rows: list[dict]) -> dict:
    out = {}
    for r in rows:
        k = out.setdefault(r["kind"], {"rows": 0, "win": 0, "loss": 0, "push": 0, "unknown": 0})
        k["rows"] += 1
        res = r.get("result")
        if res in ("win", "loss", "push"):
            k[res] += 1
        elif "result" in r:
            k["unknown"] += 1
    return out


def _v(f):
    return f.get("value", C.UNKNOWN) if isinstance(f, dict) else f


def render_markdown(game_id: str, summ: dict, rows: list[dict], rrows: list[dict]) -> str:
    """Human-readable digest of the stored grades. Every figure is copied from the jsonl rows."""
    fs = summ.get("final_score") or {}
    L = [f"# Grading: {game_id} (research only, projection_ready=false)", "",
         f"Final: {', '.join(f'{k} {v}' for k, v in fs.items() if k not in ('source', 'pulled_utc'))}",
         f"Result source: {fs.get('source')} (pulled {fs.get('pulled_utc')})",
         f"Kickoff (UTC): {summ.get('kickoff_utc')} | packet graded: {summ.get('packet_source')} | freezes read from: {summ.get('freeze_ref')}",
         f"Graded (UTC): {summ.get('graded_utc')}", "",
         "Closing line = latest snapshot saved in this repo before kickoff (not claimed to be the true close). "
         "Missing = unknown. Probabilities from analyst work are 'analyst read', not edges.", ""]
    L += ["## Report flagged props", "", "| Read | Side | Line | Actual | Result | Close (book, saved UTC) | CLV |", "|---|---|---|---|---|---|---|"]
    for r in rrows:
        if r["kind"] == "report_flagged_prop":
            cl = r["closing_line"]
            L.append(f"| {r['player']} {r['stat']} ({r['cite']}) | {r['side']} | {r['report_line']} | {_v(r['actual'])} | {r['result']} | "
                     f"{_v(cl)} ({cl.get('book')}, {cl.get('pulled_utc')}) | {r['clv'].get('positive')} {r['clv'].get('line_points', '')} {r['clv'].get('prob', '')} |")
    L += ["", "## Report team reads", "", "| Read | Tier | Actual | Result | Close (book, saved UTC) | CLV |", "|---|---|---|---|---|---|"]
    for r in rrows:
        if r["kind"] == "report_team_read":
            cl = r["closing_line"]
            L.append(f"| {r['market']} {r['side']} {r['report_line'] if r['report_line'] is not None else ''} ({r['cite']}) | {r['tier']} | "
                     f"{_v(r['actual'])} | {r['result']} | {_v(cl)} {cl.get('prices', '')} ({cl.get('book')}, {cl.get('pulled_utc')}) | "
                     f"{r['clv'].get('positive')} pts={r['clv'].get('line_points', '')} prob={r['clv'].get('prob', '')} |")
    L += ["", "## Slips", "", "| Slip | Price / stake | Legs hit | Result | Missed legs |", "|---|---|---|---|---|"]
    for r in rrows:
        if r["kind"] == "report_slip":
            miss = ", ".join(f"{l['leg']} (actual {l['actual']})" for l in r["legs"] if l["result"] != "win") or "none"
            L.append(f"| {r['slip']} ({r['cite']}) | {r['price']} / ${r['stake_usd']} | {r['legs_hit']}/{r['legs_listed']}"
                     f"{'' if r['complete_leg_list'] else ' (leg list incomplete)'} | {r['result']} | {miss} |")
    L += ["", "## Leg ladder (legs.json / script_layer.json)", "", "| Leg | Player | Actual | Result | Margin vs rung | Analyst read | FD main line at close (ref) |", "|---|---|---|---|---|---|---|"]
    for r in rrows:
        if r["kind"] == "research_leg":
            pr = "; ".join(f"{k}={round(_v(v), 3) if isinstance(_v(v), float) else _v(v)}" for k, v in r["analyst_probabilities"].items())
            ref = r.get("closing_main_line_reference") or {}
            L.append(f"| {r['leg']} | {r.get('player', '')} | {_v(r['actual'])} | {r['result']} | {r.get('margin_vs_rung', '')} | {pr} | {_v(ref)} |")
    L += ["", "## Team projections and probabilities", "", "| Source | Quantity / event | Projection | Actual | Error or Brier |", "|---|---|---|---|---|"]
    for r in rrows:
        if r["kind"] == "research_team_projection":
            L.append(f"| {r['source_label']} | {r['quantity']} | {_v(r['projection'])} | {_v(r['actual'])} | err {r['error_actual_minus_projection']} |")
        elif r["kind"] == "research_team_probability" and "event" in r:
            L.append(f"| {r['source_label']} | P({r['event']}) | {_v(r['probability'])} | outcome {r['outcome']} | Brier {r['brier']} |")
        elif r["kind"] == "research_team_probability":
            L.append(f"| {r.get('source_label')} | {r['leg']} | {list(r['analyst_probabilities'].values())[0]['value']} | {_v(r['actual'])} | {r['result']} |")
        elif r["kind"] == "official_100k":
            L.append(f"| official 100k ({r['artifact']['path']}) | status | {r['status']} | | {r['note']} |")
    c = summ.get("counts") or {}
    L += ["", "## Packet grading (grading/results/" + game_id + ".jsonl)", ""]
    for k, v in c.items():
        L.append(f"- {k}: {v}")
    L += ["", f"Validation: {summ.get('validation')}. projection_ready stays false.", ""]
    return "\n".join(L)
