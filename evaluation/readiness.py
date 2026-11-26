"""Honest readiness evaluation for NFL-49 (four pillars) and NFL-56 (source-of-truth criteria), plus Rico's
market-readiness rule. REPORT ONLY: it never writes known_flags, never sets projection_ready, never changes a model.

  python -m evaluation.readiness            # prints the report
  python -m evaluation.readiness --write    # also writes evaluation/READINESS_REPORT.{json,md}

Market rule (Rico): a market goes live only with 30+ real-price graded spots on games the model never saw,
at least +3 points over break-even, a 95% CI on the edge above zero, and at least 4 distinct weeks.
  * spot      = a grading/results/<game>.jsonl row of kind flagged_prop or team_market with result win/loss
                (pushes and 'unknown' excluded) AND a numeric bet_price whose pull time is before kickoff
  * never saw = weeks >= HOLDOUT_FIRST_WEEK (the protocol says weeks 1-9 of 2026 were seen during development)
  * edge      = mean(win - break_even), in points; CI = percentile bootstrap, 20,000 resamples, seed 0
Every number in the report is computed from committed files and cites them; missing data is 'unknown', never 0.
"""
from __future__ import annotations

import argparse, json, random, re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "grading" / "results"
HOLDOUT_FIRST_WEEK = 10
RULE = {"min_spots": 30, "min_edge_points": 3.0, "ci_lower_above": 0.0, "min_weeks": 4}


def _utc(s):
    try:
        d = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def break_even(american: float) -> float:
    return 100 / (american + 100) if american > 0 else -american / (-american + 100)


def week_of(game_id: str):
    m = re.match(r"^\d{4}_(\d{2})_", game_id or "")
    return int(m.group(1)) if m else None


def market_of(r: dict) -> str:
    if r.get("kind") == "team_market":
        return "team:" + str(r.get("market_type"))
    return "prop:" + str(r.get("market_type"))


def spots(results_dir: Path = RESULTS):
    out, excluded = [], {"push_or_unknown": 0, "no_real_price": 0, "price_after_kickoff": 0, "seen_week": 0}
    for f in sorted(results_dir.glob("*.jsonl")):
        if f.name.endswith(".research.jsonl"):
            continue
        for line in f.read_text().splitlines():
            r = json.loads(line)
            if r.get("kind") not in ("flagged_prop", "team_market"):
                continue
            if r.get("result") not in ("win", "loss"):
                excluded["push_or_unknown"] += 1; continue
            bp = r.get("bet_price") or {}
            price = bp.get("value")
            if not isinstance(price, (int, float)) or abs(price) < 100:
                excluded["no_real_price"] += 1; continue
            pulled, ko = _utc(bp.get("pulled_utc")), _utc(r.get("kickoff_utc"))
            if pulled is None or ko is None or pulled >= ko:
                excluded["price_after_kickoff"] += 1; continue
            wk = week_of(r.get("game_id"))
            if wk is None or wk < HOLDOUT_FIRST_WEEK:
                excluded["seen_week"] += 1; continue
            out.append({"game_id": r["game_id"], "week": wk, "market": market_of(r), "win": r["result"] == "win",
                        "price": price, "break_even": break_even(price), "price_source": bp.get("source"),
                        "price_pulled_utc": bp.get("pulled_utc"), "file": f"grading/results/{f.name}"})
    return out, excluded


def _boot_ci(vals, n=20000, seed=0):
    if len(vals) < 2:
        return None, None
    rng = random.Random(seed)
    k = len(vals)
    means = sorted(sum(vals[rng.randrange(k)] for _ in range(k)) / k for _ in range(n))
    return means[int(0.025 * n)], means[int(0.975 * n) - 1]


def market_table(sp):
    by = {}
    for s in sp:
        by.setdefault(s["market"], []).append(s)
    by["ALL"] = list(sp)
    rows = []
    for m, ss in sorted(by.items()):
        n = len(ss)
        diffs = [(1.0 if s["win"] else 0.0) - s["break_even"] for s in ss]
        edge = 100 * sum(diffs) / n if n else None
        lo, hi = _boot_ci(diffs)
        weeks = sorted({s["week"] for s in ss})
        checks = {"spots>=30": n >= RULE["min_spots"],
                  "edge>=+3pts": edge is not None and edge >= RULE["min_edge_points"],
                  "ci_lower>0": lo is not None and lo > RULE["ci_lower_above"],
                  "weeks>=4": len(weeks) >= RULE["min_weeks"]}
        rows.append({"market": m, "spots": n, "wins": sum(s["win"] for s in ss),
                     "hit_rate": None if not n else round(sum(s["win"] for s in ss) / n, 4),
                     "mean_break_even": None if not n else round(sum(s["break_even"] for s in ss) / n, 4),
                     "edge_points": None if edge is None else round(edge, 2),
                     "ci95_points": None if lo is None else [round(100 * lo, 2), round(100 * hi, 2)],
                     "weeks": weeks, "checks": checks, "live": all(checks.values())})
    return rows


def _flags(root):
    return json.loads((root / "known_flags" / "KNOWN_LIMITATIONS.json").read_text())


def pillars(root: Path = ROOT, market_rows=None):
    f = _flags(root)
    ev = json.loads((root / "evaluation" / "EVALUATION.json").read_text())
    proto = json.loads((root / "evaluation" / "PRISTINE_EVALUATION_PROTOCOL.json").read_text())
    src = "known_flags/KNOWN_LIMITATIONS.json"
    p = []
    p1_fail = []
    if f.get("Phase15") != "AUTO":
        p1_fail.append(f"Phase15={f.get('Phase15')!r} ({src})")
    if f.get("quotes") in (None, "NOLINE"):
        p1_fail.append(f"quotes={f.get('quotes')!r} ({src}); no accepted quote feed for scoring")
    p.append({"pillar": "NFL-49 P1 source freshness/completeness", "pass": not p1_fail,
              "evidence": [f"Phase15={f.get('Phase15')!r} ({src})", f"quotes={f.get('quotes')!r} ({src})",
                           "per-game freshness is checked live by pipeline/freshness.py (publisher as-of time, NFL-56)"],
              "blockers": p1_fail})
    p2_fail = []
    if f.get("entrypoint_enforced") is not True:
        p2_fail.append(f"entrypoint_enforced={f.get('entrypoint_enforced')!r}")
    cv = f.get("contaminated_validator")
    if isinstance(cv, dict):   # historical record: blocks only if it was never superseded by a decontaminated validator
        sup = cv.get("superseded_by")
        if not sup or not (root / sup).exists():
            p2_fail.append(f"contaminated validator {cv.get('path')} has no existing decontaminated replacement")
    elif cv not in (None, False):
        p2_fail.append(f"contaminated_validator={cv!r}")
    if not (root / "core/possession_engine_v0/shared_accounting.py").exists():
        p2_fail.append("core/possession_engine_v0/shared_accounting.py missing (SHARED_ACCOUNTING)")
    if "ACCEPTED" not in str((f.get("nfl43") or {}).get("review", "")):
        p2_fail.append("NFL-43 semantics bounds not accepted")
    p.append({"pillar": "NFL-49 P2 integrated sim accounting", "pass": not p2_fail,
              "evidence": [f"entrypoint_enforced={f.get('entrypoint_enforced')!r} ({src})",
                           f"NFL-43 review: {(f.get('nfl43') or {}).get('review', 'unknown')[:90]}",
                           f"still unsupported (bounded, enforced): {(f.get('nfl43') or {}).get('still_unsupported')}",
                           "SHARED_ACCOUNTING: core/possession_engine_v0/shared_accounting.py",
                           f"contaminated validator superseded by {(cv or {}).get('superseded_by') if isinstance(cv, dict) else cv}"],
              "blockers": p2_fail})
    p3_fail = []
    if f.get("calibration_fitted_claim") is not True:
        p3_fail.append(f"calibration_fitted_claim={f.get('calibration_fitted_claim')!r} ({src}); no fitted calibration (NFL-45)")
    live = [r["market"] for r in (market_rows or []) if r["live"] and r["market"] != "ALL"]
    if not live:
        p3_fail.append("no market meets Rico's market-readiness rule (see market table)")
    p.append({"pillar": "NFL-49 P3 calibration evidence", "pass": not p3_fail, "evidence": [f"markets passing rule: {live or 'none'}"],
              "blockers": p3_fail})
    p4_fail = []
    if f.get("full_integration_acceptance") is not True:
        p4_fail.append(f"full_integration_acceptance={f.get('full_integration_acceptance')!r} ({src})")
    if f.get("production_validated") is not True:
        p4_fail.append(f"production_validated={f.get('production_validated')!r} ({src})")
    mc = proto.get("min_coverage", {})
    if ev.get("games_scored", 0) < mc.get("games_scored", 30) or len(ev.get("weeks_scored") or []) < mc.get("weeks", 3):
        p4_fail.append(f"pristine evaluation status={ev.get('status')!r}, games_scored={ev.get('games_scored')}, "
                       f"weeks_scored={ev.get('weeks_scored')} vs min {mc} (evaluation/EVALUATION.json)")
    if f.get("pristine_protocol_complete") is not True:
        p4_fail.append(f"pristine_protocol_complete={f.get('pristine_protocol_complete')!r} ({src})")
    p.append({"pillar": "NFL-49 P4 end-to-end acceptance", "pass": not p4_fail, "evidence": [], "blockers": p4_fail})
    return p


def nfl56_criteria(root: Path = ROOT):
    def has(path, *needles):
        fp = root / path
        if not fp.exists():
            return False
        t = fp.read_text(errors="ignore")
        return all(n in t for n in needles)
    c = [
        ("1 runnable phase workflows with explicit MISSING/NOT_YET", has("pipeline/phases.py", "MISSING", "NOT_YET") and
         has(".github/workflows/nfl-gameday-gate.yml", "pipeline.window"),
         "pipeline/phases.py statuses; .github/workflows/nfl-gameday-gate.yml runs python -m pipeline.window",
         "pipeline/workflow_to_install/nfl-source-of-truth.yml is still not installed (workflow changes need Rico)"),
        ("2 news/weather adapters documented with freshness windows", has("docs/DATA_FRESHNESS.md", "Weather", "News"),
         "docs/DATA_FRESHNESS.md (windows) + pipeline/freshness.py POLICY", ""),
        ("2b freshness dated by publisher as-of time", has("pipeline/freshness.py", "source_asof") and (root / "pipeline/source_asof.py").exists(),
         "pipeline/freshness.py + pipeline/source_asof.py", "needs the NFL-56 as-of PR merged"),
        ("3 100k entrypoint exists and fails closed", has("pipeline/sim100k.py", "TRIALS = 100_000", "REFUSED"),
         "pipeline/sim100k.py (no override; G0-G7 gates)", ""),
        ("4 routine bootstrap without continuous sessions", has(".github/workflows/nfl-gameday-gate.yml", "workflow_dispatch") and
         has(".github/workflows/nfl-pregame-packets.yml", "workflow_dispatch"),
         "workflow_dispatch on nfl-gameday-gate.yml / nfl-pregame-packets.yml, dispatched by external cron-job.org jobs "
         "(not verifiable from the repo; last verified dispatch run 44943361282 on main, success)", ""),
        ("5 README distinguishes goal vs current readiness", has("README.md", "goal vs current", "projection_ready"),
         "README.md 'Projection pipeline: goal vs current status (NFL-56)'", ""),
    ]
    return [{"criterion": a, "pass": bool(b), "evidence": e, "note": ("" if b and n.startswith("needs") else n)} for a, b, e, n in c]


def evidence_boundary(root: Path = ROOT) -> dict:
    """Stamp what this report may cite. Open draft PRs never count toward pristine holdout coverage."""
    ev = json.loads((root / "evaluation" / "EVALUATION.json").read_text())
    scored = [g for g in (ev.get("games") or []) if g.get("status") == "SCORED"]
    return {
        "evaluated_from": "committed evaluation/EVALUATION.json + known_flags/KNOWN_LIMITATIONS.json + grading/results on this tree",
        "pristine_games_scored": ev.get("games_scored"),
        "pristine_weeks_scored": ev.get("weeks_scored"),
        "pristine_scored_game_ids": [g["game_id"] for g in scored],
        "open_draft_prs_do_not_count": True,
        "note": ("Open draft research/grade PRs (including Week 12 GB@LAR PR #131) are outside this evidence "
                 "boundary until independently vetted, merged, and incorporated under the frozen pristine protocol. "
                 "Even if one additional Week 12 game were later accepted, coverage would be at most 15 games across "
                 "weeks 10–12 — still below min_coverage 30 games / 3 weeks. Research/grade packets without matched "
                 "closing prices are not player-prop calibration evidence. Refresh this report only after incorporation. "
                 "All readiness flags stay fail-closed."),
    }


def evaluate(root: Path = ROOT, results_dir: Path | None = None):
    sp, excl = spots(results_dir or root / "grading" / "results")
    mt = market_table(sp)
    pl = pillars(root, mt)
    c56 = nfl56_criteria(root)
    gate49 = all(p["pass"] for p in pl)
    gate56 = all(c["pass"] for c in c56)
    flags = _flags(root)
    return {"schema": "readiness-report/1", "evaluated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "report_only": True, "projection_ready_flag": flags.get("projection_ready"),
            "projection_ready_may_flip": gate49 and gate56,
            "nfl49_pass": gate49, "nfl56_pass": gate56, "nfl49_pillars": pl, "nfl56_criteria": c56,
            "market_rule": RULE, "holdout_first_week": HOLDOUT_FIRST_WEEK, "spots_excluded": excl, "markets": mt,
            "evidence_boundary": evidence_boundary(root)}


def render(r: dict) -> str:
    yn = lambda b: "PASS" if b else "FAIL"
    L = ["# Readiness report (report only)", "",
         f"Evaluated {r['evaluated_utc']} UTC by `python -m evaluation.readiness`. projection_ready on main: "
         f"**{r['projection_ready_flag']}**. May flip: **{r['projection_ready_may_flip']}**. Nothing here changes a flag.", ""]
    eb = r.get("evidence_boundary") or {}
    if eb:
        L += ["## Evidence boundary", "",
              f"- Stamp: `{r['evaluated_utc']}` UTC. Counts only committed files on this tree.",
              f"- Pristine holdout cited: **{eb.get('pristine_games_scored')}** scored games, weeks "
              f"**{eb.get('pristine_weeks_scored')}** (`evaluation/EVALUATION.json`).",
              f"- Open draft PRs do **not** count toward pristine coverage (including PR #131 GB@LAR research/grade).",
              f"- {eb.get('note')}", ""]
    L += [f"## NFL-49: {yn(r['nfl49_pass'])}", "", "| Pillar | Result | Evidence / blockers |", "| --- | --- | --- |"]
    for p in r["nfl49_pillars"]:
        L.append(f"| {p['pillar']} | {yn(p['pass'])} | {'; '.join(p['blockers'] or p['evidence']).replace('|', '/')} |")
    L += ["", f"## NFL-56: {yn(r['nfl56_pass'])}", "", "| Criterion | Result | Evidence | Note |", "| --- | --- | --- | --- |"]
    for c in r["nfl56_criteria"]:
        L.append(f"| {c['criterion']} | {yn(c['pass'])} | {c['evidence']} | {c['note']} |")
    L += ["", "## Market readiness (Rico's rule: 30+ real-price graded spots on unseen games, >= +3 pts over break-even, "
          "CI > 0, >= 4 weeks)", "", f"Unseen = week >= {r['holdout_first_week']}. Excluded rows: {r['spots_excluded']}.", "",
          "| Market | Spots | Hit | Mean BE | Edge (pts) | 95% CI (pts) | Weeks | Live |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for m in r["markets"]:
        L.append(f"| {m['market']} | {m['spots']} | {m['hit_rate'] if m['hit_rate'] is not None else 'unknown'} | "
                 f"{m['mean_break_even'] if m['mean_break_even'] is not None else 'unknown'} | "
                 f"{m['edge_points'] if m['edge_points'] is not None else 'unknown'} | {m['ci95_points'] or 'unknown'} | "
                 f"{','.join(map(str, m['weeks'])) or '-'} | {'YES' if m['live'] else 'no'} |")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args(argv)
    r = evaluate()
    print(render(r))
    if a.write:
        (ROOT / "evaluation" / "READINESS_REPORT.json").write_text(json.dumps(r, indent=1) + "\n")
        (ROOT / "evaluation" / "READINESS_REPORT.md").write_text(render(r))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
