"""SRC-5 preflight (Rico 2026-11-01 22:47 ET): before each run, every feed must be on the latest week and the right season.
Each puller writes <shared_src>/feed_stamps.json: {feed_key: {file, category, season, data_week, week_kind, pulled_et}}.
label feeds must equal the run week; 'through' feeds must have data through run week - 1.
Usage: python3 feed_week_check.py <shared_src_dir> --season 2026 --week 9 [--probe <dir with parquets>]   exit 1 if any feed fails."""
import json, os, sys
# key: (category, kind, files relative to shared_src, what the stamp must say)
FEEDS = {
    "pbp":          ("core_stats_pbp", "through", ["play_by_play_2026.parquet"]),
    "snap_counts":  ("core_stats_pbp", "through", ["snap_counts_2026.parquet"]),
    "espn_depth":   ("core_stats_pbp", "label",   ["espn_depth_all.json"]),
    "espn_box":     ("core_stats_pbp", "through", ["../../week{W}/phase_walk/src/espn_box.json"]),
    "ftn":          ("coverage_matchups", "through", ["ftn_charting_2026.parquet"]),
    "sharp":        ("coverage_matchups", "through", ["sharp_cov_schemes.md"]),
    "sharp_second": ("coverage_matchups", "through", ["sharp_second_source.json"]),
    "espn_wrcb":    ("coverage_matchups", "label",   ["../../week{W}/sources/espn_wrcb_wk{W}.json"]),
    "statrankings_ol": ("coverage_matchups", "through", ["statrankings_ol.json"]),
    "qb_pressure":  ("coverage_matchups", "through", ["qb_pressure.json"]),
    "ngs":          ("ngs", "through", ["ngs_passing.parquet", "ngs_receiving.parquet", "ngs_rushing.parquet"]),
    "film":         ("film", "through", ["film_verified.json"]),
    "injuries":     ("injuries_news", "label", ["injuries_parsed.csv"]),
    "news":         ("injuries_news", "label", ["team_news.json"]),
    "inactives":    ("injuries_news", "label", ["inactives.json"]),
    "weather":      ("weather", "label", ["weather.json"]),
    "odds_props":   ("odds_props", "label", ["odds_*.csv"]),
    "pff":          ("coverage_matchups", "label", ["pff_matchups.json"]),
}
OPTIONAL = {"pff", "statrankings_ol", "news"}   # only checked if used; if present they must be current
def _exists(sh, pat, W):
    import glob
    p = os.path.normpath(os.path.join(sh, pat.format(W=W))); return bool(glob.glob(p)), p
def probe_week(path):
    """Max week actually inside a parquet (nflverse pbp/NGS/FTN/snap counts). None if unreadable."""
    try:
        import pandas as pd
        df = pd.read_parquet(path, columns=None); s = df["season"].max() if "season" in df else None
        if s is not None: df = df[df["season"] == s]
        if "season_type" in df: df = df[df["season_type"].astype(str).str.upper().isin(["REG", "POST"])]
        return (int(s) if s is not None else None), int(df["week"].max())
    except Exception: return None
def check(sh, season=2026, week=9, probe=None):
    st = {}
    sp = os.path.join(sh, "feed_stamps.json")
    try: S = json.load(open(sp)) if os.path.exists(sp) else {}
    except Exception: S = {}
    for k, (cat, kind, files) in FEEDS.items():
        r = dict(category=cat, week_kind=kind, need=(f"week {week}" if kind == "label" else f"data through week {week-1}"), problems=[])
        for f in files:
            ok, p = _exists(sh, f, week)
            if not ok: r["problems"].append(f"file missing: {p}")
        s = S.get(k)
        if not s: r["problems"].append("no feed_stamps.json entry (season/data_week/pulled_et)")
        else:
            lack = [x for x in ("season", "data_week", "pulled_et") if s.get(x) in (None, "")]
            if lack: r["problems"].append(f"stamp missing {lack}")
            else:
                if int(s["season"]) != season: r["problems"].append(f"wrong season {s['season']} (need {season})")
                fw = int(s["data_week"]); kd = s.get("week_kind", kind)
                if kd == "label" and fw != week: r["problems"].append(f"serving week {fw}, need week {week}")
                if kd != "label" and fw < week - 1: r["problems"].append(f"data through week {fw}, need week {week-1}")
        if probe:
            for f in files:
                if f.endswith(".parquet") and os.path.exists(os.path.join(probe, f)):
                    pw = probe_week(os.path.join(probe, f))
                    if pw: r.setdefault("probe", {})[f] = f"latest copy {probe}: season {pw[0]} max week {pw[1]}"
        r["status"] = "OK" if not r["problems"] else ("NOT USED (optional)" if k in OPTIONAL and all(p.startswith(("file missing", "no feed_stamps")) for p in r["problems"]) else "FAIL")
        st[k] = r
    return {"shared_src": os.path.abspath(sh), "season": season, "week": week, "feeds": st,
            "ok": all(v["status"] != "FAIL" for v in st.values())}
def stamp_for(sh, key):
    """For assemble.py: the stamp fields to copy onto a manifest source entry ({} if absent -> gate fails closed)."""
    try: s = json.load(open(os.path.join(sh, "feed_stamps.json"))).get(key) or {}
    except Exception: s = {}
    return {k: s[k] for k in ("season", "data_week", "week_kind") if k in s}
if __name__ == "__main__":
    a = sys.argv; sh = a[1]; g = lambda k, d: a[a.index(k)+1] if k in a else d
    r = check(sh, int(g("--season", 2026)), int(g("--week", 9)), g("--probe", None))
    for k, v in r["feeds"].items():
        print(f"{v['status']:<20} {k:<16} ({v['category']}, need {v['need']})" + "".join(f"\n    - {p}" for p in v["problems"]) + "".join(f"\n    * {p}" for p in (v.get("probe") or {}).values()))
    print("FEEDS:", "PASS" if r["ok"] else "FAIL"); sys.exit(0 if r["ok"] else 1)
