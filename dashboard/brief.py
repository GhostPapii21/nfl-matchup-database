"""Game-day brief: one page per game, written after the official inactives (about T-90), built from the board's
projections (owner, after MNF Nov 23, 2026: "I should have stuck to the projections; the read could have been tighter
with the weather, the blitz and what the defense does").

    python3 -m dashboard.brief --game 2026_12_KC_BUF            # writes research/briefs/<season>/<game>/BRIEF.md and brief.json
    python3 -m dashboard.brief --game ... --offline              # no network: skips the live weather check

Sections:
  1. Weather now: a fresh NWS hourly forecast plus the latest observation near the stadium, flagged when it is worse
     than what the board was built on (rain, or wind 15+ mph / 6+ mph more than the board said).
  2. Who is out: projected players who are game-day inactives (projection void), Questionable/Doubtful tags, and "role in
     doubt" (last game's target share under a third of his season share while not on the report: the McLaurin case).
  3. Each defense now: this season's blitz and 5+ rusher rate (FTN), pressure, what it allows by position (ranks),
     separation it allows vs receivers' norms (Next Gen Stats, this season), coverage defenders who allow the most.
  4. Reads: every player prop with book lines; our chance at the books' main line, blended with the market's fair
     chance on the logit scale (the blend tested better than either alone). Flags: WR1 yards vs a blitz-heavy defense,
     QB rushing (no model: one long run beats an under), weather-hit receiver yards.
  5. Six picks: the strongest blended chances, at most one pick per player and three per team, never a player ruled
     out or a flagged WR1-yards over. A ranking aid, not a bet; every pick shows its numbers.
Research only.
"""
from __future__ import annotations

import argparse
import json
import math
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "nfl-matchup-database research (github.com/GhostPapii21)", "Accept": "application/geo+json"}
BLITZ_HEAVY = 0.40
UNDER_PENALTY = 0.03    # owner's preference (as in dashboard/bestbet.py): an under must be clearly better to be picked
WR1_SHARE = 0.22
MIN_PICK = 0.56
WET = ("rain", "shower", "drizzle", "snow", "sleet", "storm", "thunder")


def _get_json(url, fetch=None):
    if fetch:
        return fetch(url)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25) as r:
        return json.loads(r.read())


def _sig(z):
    return 1 / (1 + math.exp(-z))


def _logit(p):
    p = min(max(p, 1e-4), 1 - 1e-4)
    return math.log(p / (1 - p))


# ------------------------------------------------------------------------------------------------ 1. weather now
def weather_now(board: dict, *, offline=False, fetch=None) -> dict:
    w = board.get("weather") or {}
    roof = (w.get("roof") or (board.get("game") or {}).get("roof") or "").lower()
    if roof in ("dome", "closed", "indoors"):
        return {"status": "INDOORS", "flag": None, "note": "indoors: weather does not apply"}
    was = {"wind_mph_max": (w.get("during_game") or {}).get("wind_mph_max"), "precip_pct_max": (w.get("during_game") or {}).get("precip_chance_pct_max"),
           "retrieved_utc": w.get("retrieved_utc")}
    out = {"status": "BOARD_ONLY", "board": was, "flag": None}
    if offline or not w.get("url"):
        return out
    try:
        ko = datetime.fromisoformat(w["kickoff_utc"].replace("Z", "+00:00"))
        periods = _get_json(w["url"], fetch)["properties"]["periods"]
        win = [p for p in periods if -3600 < (datetime.fromisoformat(p["startTime"]).astimezone(timezone.utc) - ko).total_seconds() < 4 * 3600]   # the hour holding kickoff starts before it
        wind = max((float(str(p.get("windSpeed", "0")).split()[0].split("-")[-1] or 0) for p in win), default=None)
        precip = max(((p.get("probabilityOfPrecipitation") or {}).get("value") or 0 for p in win), default=None)
        out["forecast_now"] = {"wind_mph_max": wind, "precip_pct_max": precip, "summary": win[0].get("shortForecast") if win else None}
        out["status"] = "OK"
    except Exception as e:  # noqa: BLE001
        out["forecast_error"] = f"{type(e).__name__}: {e}"[:120]
    try:
        st = _get_json(w["url"].replace("/forecast/hourly", "/stations"), fetch)["features"][0]["properties"]["stationIdentifier"]
        ob = _get_json(f"https://api.weather.gov/stations/{st}/observations/latest", fetch)["properties"]
        kmh = (ob.get("windSpeed") or {}).get("value")
        out["observed_now"] = {"station": st, "at": ob.get("timestamp"), "text": ob.get("textDescription"),
                               "wind_mph": round(kmh / 1.609, 1) if kmh is not None else None}
    except Exception as e:  # noqa: BLE001
        out["observation_error"] = f"{type(e).__name__}: {e}"[:120]
    reasons = []
    fn, ob = out.get("forecast_now") or {}, out.get("observed_now") or {}
    bw, bp = was["wind_mph_max"] or 0, was["precip_pct_max"] or 0
    if any(x in str(ob.get("text") or "").lower() for x in WET):
        reasons.append(f"it is {ob['text'].lower()} at {ob.get('station')} now")
    if (fn.get("precip_pct_max") or 0) >= 30 and (fn.get("precip_pct_max") or 0) - bp >= 20:
        reasons.append(f"rain chance now {fn['precip_pct_max']}% (board had {bp}%)")
    for v, lab in ((fn.get("wind_mph_max"), "forecast"), (ob.get("wind_mph"), "observed")):
        if v and (v >= 15 or v - bw >= 6) and v > bw:
            reasons.append(f"{lab} wind {v:.0f} mph (board had {bw:.0f})")
    if reasons:
        out["flag"] = ("WORSE THAN THE BOARD: " + "; ".join(reasons) +
                       ". Rain cuts receiver yards about 16% and 15+ mph wind about 8% (research/context_effects_2026-11-22): "
                       "shade WR yards down; tight-end and running-back catches hold up better.")
    return out


# ------------------------------------------------------------------------------------------------ 2. who is out
def availability(board: dict, inactive: dict) -> list:
    from dashboard.bestbet import _norm
    rows = []
    for s in board["sides"].values():
        off = s["offense"]
        out = {_norm(n) for n in inactive.get(off, [])}
        inj = {_norm(x["player"]): x for x in s.get("offense_injuries") or []}
        sh = {_norm(p["player"]): p.get("shadow") or {} for p in (s.get("watch") or {}).get("receivers") or []}
        for kind in ("receivers", "rushers"):
            for e in (s.get("opportunity") or {}).get(kind) or []:
                n = _norm(e["player"])
                if e.get("status"):
                    continue
                if n in out:
                    rows.append({"team": off, "player": e["player"], "flag": "INACTIVE", "note": "on the game-day inactive list: projection void"})
                    continue
                st = (inj.get(n) or {}).get("game_status")
                if st in ("Questionable", "Doubtful"):
                    rows.append({"team": off, "player": e["player"], "flag": st.upper(), "note": f"{st} ({inj[n].get('injury')}): confirm he is active"})
                x = sh.get(n) or {}
                if kind == "receivers" and x.get("season_share") and x.get("last_game_share") is not None and not st \
                        and x["last_game_share"] < x["season_share"] / 3 and x["season_share"] >= 0.10:
                    rows.append({"team": off, "player": e["player"], "flag": "ROLE IN DOUBT",
                                 "note": f"{x['last_game_share']:.0%} of targets last game vs {x['season_share']:.0%} on the season, not on the report: his targets may go elsewhere"})
    seen, uniq = set(), []
    for r in rows:
        if (r["team"], r["player"], r["flag"]) not in seen:
            seen.add((r["team"], r["player"], r["flag"])); uniq.append(r)
    return uniq


# ------------------------------------------------------------------------------------------------ 3. defenses
def separation_allowed(data, season: int) -> dict:
    """Receivers' separation vs their own norm against each defense this season (Next Gen Stats), in yards."""
    import pandas as pd
    n = data.get("ngs_receiving") if data is not None else None
    g = data.get("games") if data is not None else None
    if n is None or g is None:
        return {}
    n = n[(n.season == season) & (n.season_type == "REG") & (n.week > 0) & (n.targets >= 3)].copy()
    g = g[(g.season == season) & (g.game_type == "REG")]
    opp = pd.concat([g[["week", "home_team", "away_team"]].rename(columns={"home_team": "team", "away_team": "opp"}),
                     g[["week", "away_team", "home_team"]].rename(columns={"away_team": "team", "home_team": "opp"})])
    n = n.rename(columns={"team_abbr": "team"}).merge(opp, on=["week", "team"]).sort_values(["player_gsis_id", "week"])
    n["prior"] = n.groupby("player_gsis_id").avg_separation.transform(lambda s: s.shift().expanding().mean())
    n = n.dropna(subset=["prior"])
    n["gap"] = (n.avg_separation - n.prior) * n.targets
    t = n.groupby("opp").agg(gap=("gap", "sum"), w=("targets", "sum"))
    t = t[t.w >= 40]
    t["sep"] = t.gap / t.w
    t["rank"] = t.sep.rank(method="min").astype(int)          # 1 = takes away the most separation
    return {k: {"vs_norm_yards": round(float(v.sep), 2), "rank": int(v["rank"]), "of": int(len(t))} for k, v in t.iterrows()}


def defense_card(side: dict, sep: dict) -> dict:
    da, dr, cp = side.get("defense_allowed") or {}, side.get("defense_rank") or {}, side.get("coverage_profile") or {}
    bt = cp.get("blitz_this_season") or {}
    rk = lambda k: (dr.get(k) or {}).get("rank")
    cov = sorted(((side.get("defenders") or {}).get("coverage") or []), key=lambda c: -(c.get("yards") or 0))[:3]
    sc = cp.get("coverage_this_season") or {}
    return {"defense": side["defense"], "man_rate": cp.get("man_rate"), "zone_rate": cp.get("zone_rate"), "two_high_rate": sc.get("two_high_rate"),
            "coverage_season": cp.get("man_zone_season") or cp.get("season"),
            "blitz_rate": bt.get("blitz_rate") or cp.get("five_plus_rushers_rate"), "blitz_rank": bt.get("blitz_rank"),
            "blitz_season": bt.get("season") or cp.get("five_plus_rushers_season") or cp.get("season"),
            "pressure_rank": rk("pressure_rate"), "pass_yards_rank": rk("pass_yards_pg"), "wr_rank": rk("wr_rec_yards_pg"),
            "te_rank": rk("te_rec_yards_pg"), "rb_rush_rank": rk("rb_rush_yards_pg"), "separation": sep.get(side["defense"]),
            "most_yards_allowed": [{"player": c["player"], "pos": c.get("position"), "yards": c.get("yards"), "targets": c.get("targets"),
                                    "grade": c.get("grade")} for c in cov]}


# ------------------------------------------------------------------------------------------------ 4. reads
def reads(board: dict, weather_flag: str | None) -> list:
    from dashboard.bestbet import p_over
    out, raw = [], []
    for s in board["sides"].values():
        off = s["offense"]
        cp = s.get("coverage_profile") or {}
        blitz = (cp.get("blitz_this_season") or {}).get("blitz_rate") or cp.get("five_plus_rushers_rate") or 0
        roles = {r.get("player_id"): r for r in (s.get("roles") or {}).get("receivers") or []}
        for kind, markets in (("receivers", (("receptions", "receptions", True), ("receiving_yards", "yards", False))),
                              ("rushers", (("rushing_yards", "yards", False),))):
            for e in (s.get("opportunity") or {}).get(kind) or []:
                if e.get("status"):
                    continue
                bl = e.get("book_lines") or {}
                share = (roles.get(e.get("player_id")) or {}).get("target_share") or 0
                for mk, table, integer in markets:
                    L = bl.get(mk)
                    if not L or L.get("fair_over") is None or L.get("fair_line") is None:
                        continue
                    pm = p_over(e.get(table), L["fair_line"], integer)
                    if pm is None:
                        continue
                    raw.append((off, e, mk, L, pm, share, blitz))
    # The simulation runs below the books across whole slates (known, graded weekly). Remove each market's average gap on
    # the logit scale so a read is this player's edge relative to the market, not the model's general lean.
    shift = {}
    for mk in {r[2] for r in raw}:
        gaps = [_logit(pm) - _logit(L["fair_over"]) for _, _, m, L, pm, _, _ in raw if m == mk]
        shift[mk] = sum(gaps) / len(gaps) if len(gaps) >= 6 else 0.0
    for off, e, mk, L, pm_raw, share, blitz in raw:
        pm = _sig(_logit(pm_raw) - shift[mk])
        pb = _sig((_logit(pm) + _logit(L["fair_over"])) / 2)
        side, p = ("Over", pb) if pb >= 0.5 else ("Under", 1 - pb)
        flags = []
        if mk == "receiving_yards" and e.get("pos") == "WR" and share >= WR1_SHARE and blitz >= BLITZ_HEAVY:
            flags.append(f"WR1 vs a blitz-heavy defense ({blitz:.0%}): quick throws go to TEs and backs; fade his yards over")
        if mk == "receiving_yards" and weather_flag:
            flags.append("weather worse than the board: shade yards down")
        out.append({"team": off, "player": e["player"], "pos": e.get("pos"), "market": mk, "line": L["fair_line"], "side": side,
                    "p_model": round(pm if side == "Over" else 1 - pm, 3), "p_market": round(L["fair_over"] if side == "Over" else 1 - L["fair_over"], 3),
                    "p_blend": round(p, 3), "rank_score": round(p - (UNDER_PENALTY if side == "Under" else 0.0), 3),
                    "model_shift_removed": round(shift[mk], 3), "books": L.get("n"), "flags": flags})
    return sorted(out, key=lambda r: -r["rank_score"])


def six_picks(rs: list, avail: list, k: int = 6) -> list:
    bad = {(a["team"], a["player"]) for a in avail if a["flag"] in ("INACTIVE", "DOUBTFUL", "ROLE IN DOUBT")}
    picks, per_player, per_team = [], set(), {}
    for r in rs:
        if r["rank_score"] < MIN_PICK or (r["team"], r["player"]) in bad or r["player"] in per_player or per_team.get(r["team"], 0) >= 3:
            continue
        if r["side"] == "Over" and any("WR1 vs a blitz-heavy" in f for f in r["flags"]):
            continue
        picks.append(r); per_player.add(r["player"]); per_team[r["team"]] = per_team.get(r["team"], 0) + 1
        if len(picks) == k:
            break
    return picks


# ------------------------------------------------------------------------------------------------ assemble
MK = {"receptions": "catches", "receiving_yards": "receiving yards", "rushing_yards": "rushing yards"}


def build(gid: str, *, offline=False, fetch=None, data=None, inactive=None, now=None) -> dict:
    board = json.loads((ROOT / "dashboard" / "data" / f"{gid}.json").read_text())
    if inactive is None:
        try:
            from dashboard.build import official_inactives
            inactive = official_inactives(json.loads((ROOT / "pregame" / "packets" / gid / "packet.json").read_text()))
        except Exception:  # noqa: BLE001
            inactive = {}
    season = int(board["game"]["season"])
    try:
        sep = separation_allowed(data, season) if data is not None else {}
    except Exception:  # noqa: BLE001
        sep = {}
    wx = weather_now(board, offline=offline, fetch=fetch)
    av = availability(board, inactive or {})
    rs = reads(board, wx.get("flag"))
    return {"game_id": gid, "made_utc": (now or datetime.now(timezone.utc)).isoformat(timespec="seconds"),
            "board_built_utc": board.get("board_built_utc"), "game": board.get("game"), "implied_points": board.get("implied_points"),
            "market": board.get("market"), "weather": wx, "inactives_used": inactive or {}, "availability": av,
            "defenses": [defense_card(s, sep) for s in board["sides"].values()], "reads": rs, "picks": six_picks(rs, av)}


def to_md(b: dict) -> str:
    g, ip, m = b["game"], b.get("implied_points") or {}, b.get("market") or {}
    pct = lambda x: "–" if x is None else f"{x:.0%}"
    L = [f"# Game-day brief: {g['away']} at {g['home']} ({g['date']} {g['kickoff_et']} ET)", "",
         f"Made {b['made_utc']} from the board built {b['board_built_utc']}. Projected score: "
         + ", ".join(f"{t} {v}" for t, v in ip.items()) + f". Spread (home) {m.get('home_spread')}, total {m.get('total')}. Research only.", "",
         "## 1. Weather now"]
    w = b["weather"]
    if w.get("status") == "INDOORS":
        L.append("Indoors.")
    else:
        bo, fn, ob = w.get("board") or {}, w.get("forecast_now") or {}, w.get("observed_now") or {}
        L.append(f"- Board: wind up to {bo.get('wind_mph_max')} mph, rain chance up to {bo.get('precip_pct_max')}% (forecast {bo.get('retrieved_utc')}).")
        if fn:
            L.append(f"- Forecast now: wind up to {fn.get('wind_mph_max')} mph, rain chance up to {fn.get('precip_pct_max')}%, {fn.get('summary')}.")
        if ob:
            L.append(f"- Observed now at {ob.get('station')} ({ob.get('at')}): {ob.get('text')}, wind {ob.get('wind_mph')} mph.")
        L.append(f"- **{w['flag']}**" if w.get("flag") else "- No change from the board.")
    L += ["", "## 2. Who is out / in doubt"]
    L += [f"- **{a['flag']}** {a['player']} ({a['team']}): {a['note']}" for a in b["availability"]] or ["- Nothing flagged."]
    if not b["inactives_used"]:
        L.append("- Official inactives not pulled yet: re-run after T-90.")
    L += ["", "## 3. Each defense now", "| Defense | Man / zone / two-high | Blitz | Pressure rank | Pass yds rank | vs WR / TE / RB-rush rank | Separation vs norm | Allows the most |",
          "|---|---|---|---|---|---|---|---|"]
    for d in b["defenses"]:
        s = d.get("separation") or {}
        L.append(f"| {d['defense']} | {pct(d.get('man_rate'))} / {pct(d.get('zone_rate'))} / {pct(d.get('two_high_rate'))} ({d.get('coverage_season') or ''}) | {pct(d['blitz_rate'])}{' (rank ' + str(d['blitz_rank']) + ')' if d.get('blitz_rank') else ''} {d.get('blitz_season') or ''} | "
                 f"{d.get('pressure_rank') or '–'} | {d.get('pass_yards_rank') or '–'} | {d.get('wr_rank') or '–'} / {d.get('te_rank') or '–'} / {d.get('rb_rush_rank') or '–'} | "
                 f"{('%+.2f yds (rank %s of %s)' % (s['vs_norm_yards'], s['rank'], s['of'])) if s else '–'} | "
                 + "; ".join(f"{c['player']} {c['yards']} yds" for c in d["most_yards_allowed"]) + " |")
    L.append("Ranks: 32 = allows the most (blitz: 1 = blitzes most; separation: 1 = takes away the most).")
    L += ["", "## 4. Strongest reads (our chance, with the model's slate-wide lean removed, blended with the market's fair chance)", "| Player | Pick | Blend | Model | Market | Flags |", "|---|---|---|---|---|---|"]
    for r in b["reads"][:16]:
        L.append(f"| {r['player']} ({r['team']}) | {r['side']} {r['line']:g} {MK[r['market']]} | **{pct(r['p_blend'])}** | {pct(r['p_model'])} | {pct(r['p_market'])} | {'; '.join(r['flags'])} |")
    L.append("QB rushing has no model: a single long scramble beats an under, so treat QB rushing unders as risky.")
    L += ["", "## 5. Six picks (one per player, at most three per team)"]
    if b["picks"]:
        L += [f"{i}. **{r['player']} {r['side']} {r['line']:g} {MK[r['market']]}**: {pct(r['p_blend'])} (model {pct(r['p_model'])}, market {pct(r['p_market'])})"
              for i, r in enumerate(b["picks"], 1)]
        p = 1.0
        for r in b["picks"]:
            p *= r["p_blend"]
        L.append(f"\nAll {len(b['picks'])} hit together about {p:.1%} of the time if they were independent. Smaller entries fit the model better.")
    else:
        L.append("No read clears the bar yet (book lines missing or too close to even).")
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--game", action="append", required=True)
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--cache", default=str(ROOT / "pregame" / ".cache"))
    a = ap.parse_args(argv)
    from dashboard import extras as X
    from dashboard.build import _get
    data = X.Data(Path(a.cache), offline=a.offline, fetch=_get)
    for gid in a.game:
        b = build(gid, offline=a.offline, data=data)
        d = ROOT / "research" / "briefs" / str(b["game"]["season"]) / gid
        d.mkdir(parents=True, exist_ok=True)
        (d / "brief.json").write_text(json.dumps(b, indent=1, default=str) + "\n")
        (d / "BRIEF.md").write_text(to_md(b))
        print(f"brief: {d.relative_to(ROOT)}/BRIEF.md  picks={len(b['picks'])} weather_flag={'yes' if b['weather'].get('flag') else 'no'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
