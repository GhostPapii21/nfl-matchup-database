"""Phase 4 live: pre-kickoff flag emitter (stacked on PR #40, refs NFL-75). Research only; not picks.

    python3 -m calibration.selective_edge_emit --date 2026-11-15 \
        --freeze pregame/price_freezes/<date>_<AWAY>@<HOME>/freeze_v2_<stamp>.json [--freeze ...] \
        --probs <dir or <game>.rush_dist.cdf.csv> [--probs ...] \
        --roster /tmp/nflverse_rosters/roster_weekly_2026.parquet --roster-pulled-utc 2026-11-13T16:33:47Z \
        --pbp data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet --pbp-pulled-utc 2026-11-12T16:16:00Z \
        [--commit] [--push]

Inputs
  * price freeze: pregame/price_freezes/*/freeze_v2_*.json (read only; main-line two-sided props, best retail price at
    the consensus line, consensus no-vig). Off-consensus-line prices are dropped by legs_from_freeze_v2.
  * probabilities: the `nfl75-rush-dist/1` CDF from pipeline/rush_dist.py (branch research/rush-dist-artifact-2026-11-13):
    columns game_id, team, player, gsis, position, line, p_under, p_over on half-yard lines; p_under = P(rush_yds < line).
    p_model is attached to rushyds legs by (game_id, gsis) only: p_model = P(side) / (P(under) + P(over)) at the leg
    line (x.5 line read directly; integer line L uses P(X<L) = p_under(L-0.5), P(X>L) = p_over(L+0.5)). No name
    fallback; an unmatched leg keeps p_model blank -> INSUFFICIENT EVIDENCE (model_prob_missing).
  * roster + usage: calibration.selective_edge_roster.join_roster (nflverse weekly roster, pbp weeks < leg week).

Refusals (per game, recorded in the manifest): kickoff unknown; now >= kickoff ("kicked_off"); price pull time unknown,
at/after kickoff or in the future. If no game survives, nothing is written. Weeks outside 10-12 are refused, and the
frozen classifier's freeze manifest is checked by selective_edge_live.grade_live before anything is labeled.

Outputs (never overwritten): research/runs/<date>_live_flags/flags_<UTCstamp>.csv (every leg, its label, reason,
edge, prices, provenance, emitted_utc, emitted_et, kickoff_utc, kickoff_et, minutes_to_kickoff, countable,
prob_source, countable_reason), flags_<UTCstamp>.json (run manifest: UTC + ET run time, input sha256s, code sha256s,
freeze-manifest sha256, per-game kickoff / price pull / refusal, prob_source, countable) and flags_<UTCstamp>.md
(candidate labels only; non-countable flags are marked "[NOT COUNTABLE: <reason>]").
--prob-source and --qb-override-applied are the caller's declaration of where p_model came from. countable=true only
when --prob-source is sim_v5_v6_ensemble (the legacy ensemble the Phase 4 classifier was fit on) AND
--qb-override-applied (depth-chart/inactives QB override). Missing or unknown sources, and PR #43's
nfl75-rush-dist/1 possession-engine output, are fail-closed countable=false. STRONG UNDER labels are still written.
--commit stages only that run's files on the current research/* branch; --push pushes that branch. Both refuse if any
staged path is outside the run directory or if the branch diff vs origin/main touches pregame/ or .github/.
projection_ready is always false. Receiving legs stay INSUFFICIENT EVIDENCE (no verified main defender)."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

from calibration import selective_edge as se
from calibration import selective_edge_live as LV
from calibration import selective_edge_roster as RJ
from calibration.selective_edge_freeze import MANIFEST, ROOT

ET = ZoneInfo("America/New_York")
PROB_COLS = ("game_id", "gsis", "line", "p_under", "p_over")
PROB_SCHEMA = "nfl75-rush-dist/1"
SCHEMA = "nfl75-selective-edge-live-flags/1"
# Declared p_model family. countable=true only for the legacy ensemble the Phase 4 classifier was fit on,
# and only when the caller also certifies the depth-chart/inactives QB override was applied.
FIT_ENSEMBLE_PROB_SOURCE = "sim_v5_v6_ensemble"
# Known sources that are not the fit ensemble, including PR #43's possession-engine rush_dist.
NON_FIT_PROB_SOURCES = frozenset({PROB_SCHEMA, "possession_engine"})


class EmitError(RuntimeError):
    pass


def _sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _sha(p) -> str:
    return _sha_bytes(Path(p).read_bytes())


def _utc(s) -> datetime | None:
    if s is None or (isinstance(s, float) and np.isnan(s)) or str(s).strip() == "":
        return None
    d = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def fmt_utc(d: datetime) -> str:
    return d.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fmt_et(d: datetime) -> str:
    return d.astimezone(ET).strftime("%Y-%m-%d %H:%M:%S %Z")


# ---------------------------------------------------------------- probabilities
def check_probs(cdf: pd.DataFrame) -> pd.DataFrame:
    miss = [c for c in PROB_COLS if c not in cdf]
    if miss:
        raise EmitError(f"probabilities file lacks columns {miss} (schema {PROB_SCHEMA})")
    return cdf


def load_probs(paths) -> tuple[pd.DataFrame, dict]:
    files = []
    for p in paths:
        p = Path(p)
        files += sorted(p.glob("*.rush_dist.cdf.csv")) if p.is_dir() else [p]
    if not files:
        raise EmitError("no rush_dist CDF files found")
    shas, dfs = {}, []
    for f in files:
        meta = f.with_name(f.name.replace(".cdf.csv", ".json"))
        if meta.exists():
            m = json.loads(meta.read_text())
            if m.get("schema") != PROB_SCHEMA or m.get("projection_ready") not in (False, None):
                raise EmitError(f"{meta.name}: schema {m.get('schema')!r} is not {PROB_SCHEMA}")
        shas[str(f)] = _sha(f)
        dfs.append(check_probs(pd.read_csv(f, dtype={"gsis": str})))
    return pd.concat(dfs, ignore_index=True), shas


def attach_probs(legs: pd.DataFrame, cdf: pd.DataFrame, source: str) -> pd.DataFrame:
    check_probs(cdf)
    out = legs.copy()
    if "p_model" not in out:
        out["p_model"] = np.nan
    out["p_model"] = out.p_model.astype(float)
    idx = {k: g.set_index(g.line.round(1)) for k, g in cdf.groupby(["game_id", "gsis"])}
    match, src = [], []
    for i, r in out.iterrows():
        if str(r.get("market")) != "rushyds":
            match.append(None); src.append(None); continue
        if pd.notna(r.p_model):
            match.append("preset"); src.append(None); continue
        g = r.get("gsis")
        if g is None or (isinstance(g, float) and np.isnan(g)) or str(g).strip() == "":
            match.append("no_gsis"); src.append(None); continue
        h = idx.get((r.game_id, g))
        if h is None:
            match.append("no_player"); src.append(None); continue
        L = float(r.line)
        if abs(L - round(L)) < 1e-9:
            ku, ko = round(L - 0.5, 1), round(L + 0.5, 1)
        else:
            ku = ko = round(L, 1)
        if ku not in h.index or ko not in h.index:
            match.append("line_off_grid"); src.append(None); continue
        pu, po = float(h.loc[ku, "p_under"]), float(h.loc[ko, "p_over"])
        side = str(r.side)
        if pu + po <= 0 or side not in ("Under", "Over"):
            match.append("undefined"); src.append(None); continue
        out.at[i, "p_model"] = (pu if side == "Under" else po) / (pu + po)
        match.append("gsis"); src.append(source)
    out["p_model_match"], out["p_model_source"] = match, src
    return out


# ---------------------------------------------------------------- countable stamp
def _declared_prob_source(prob_source) -> str:
    if prob_source is None or (isinstance(prob_source, float) and np.isnan(prob_source)):
        return ""
    return str(prob_source).strip()


def countable_decision(prob_source: str | None = None, qb_override_applied: bool = False) -> tuple[bool, str, str]:
    """Return (countable, canonical source, reason). Fail closed on a missing or unknown source."""
    src = _declared_prob_source(prob_source)
    if not src:
        return False, "", "prob_source_missing"
    if src == FIT_ENSEMBLE_PROB_SOURCE:
        if not qb_override_applied:
            return False, src, "qb_override_missing"
        return True, src, "fit_ensemble_with_qb_override"
    if src in NON_FIT_PROB_SOURCES:
        return False, src, "prob_source_not_fit_ensemble"
    return False, src, "prob_source_unknown"


def not_countable_mark(countable: bool, reason: str) -> str:
    return "" if countable else f"[NOT COUNTABLE: {reason}]"


def stamp_countable(legs: pd.DataFrame, *, prob_source: str | None = None,
                    qb_override_applied: bool = False) -> pd.DataFrame:
    """Stamp every flag with countable, prob_source, countable_reason, and a writer mark.

    countable=true only when the declared source is the legacy sim_v5/v6 ensemble the Phase 4
    classifier was fit on AND qb_override_applied is true. PR #43's nfl75-rush-dist/1 output,
    a missing source, an unknown source, or a missing QB override are all countable=false.
    Labels are left unchanged.
    """
    countable, src, reason = countable_decision(prob_source, bool(qb_override_applied))
    out = legs.copy()
    out["prob_source"] = src
    out["countable"] = countable
    out["countable_reason"] = reason
    out["countable_mark"] = not_countable_mark(countable, reason)
    return out


# ---------------------------------------------------------------- git guards
def guard_paths(paths, run_dir: str):
    run_dir = str(run_dir).rstrip("/") + "/"
    for p in paths:
        if p.startswith("pregame/") or p.startswith(".github/"):
            raise EmitError(f"refuse: {p} touches pregame/ or .github/ (pregame workflow spends Odds API credits)")
        if not p.startswith(run_dir):
            raise EmitError(f"refuse: staged path {p} is outside {run_dir}")


def guard_branch(branch: str):
    if not branch or not branch.startswith("research/"):
        raise EmitError(f"refuse to commit/push on branch {branch!r}: live flags go to a research/* branch only")


def commit_message(date: str, run_utc: str, games) -> str:
    return (f"Live flags {date} run {run_utc}: {len(games)} game(s) {', '.join(games)}; research only, "
            f"projection_ready false (refs NFL-75)")


def _git(*a, cwd=ROOT) -> str:
    r = subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True)
    if r.returncode:
        raise EmitError(f"git {' '.join(a)} failed: {r.stderr.strip()}")
    return r.stdout.strip()


def commit_and_push(files, run_dir_rel: str, date: str, run_utc: str, games, push: bool, cwd=ROOT):
    branch = _git("rev-parse", "--abbrev-ref", "HEAD", cwd=cwd)
    guard_branch(branch)
    _git("add", "--", *[str(f) for f in files], cwd=cwd)
    staged = [p for p in _git("diff", "--cached", "--name-only", cwd=cwd).splitlines() if p]
    guard_paths(staged, run_dir_rel)
    _git("commit", "-m", commit_message(date, run_utc, games), cwd=cwd)
    sha = _git("rev-parse", "HEAD", cwd=cwd)
    if push:
        _git("fetch", "-q", "origin", "main", cwd=cwd)
        touched = [p for p in _git("diff", "--name-only", "origin/main...HEAD", cwd=cwd).splitlines()
                   if p.startswith("pregame/") or p.startswith(".github/")]
        if touched:
            raise EmitError(f"refuse to push: branch diff vs origin/main touches {touched}")
        _git("push", "origin", branch, cwd=cwd)
    return branch, sha


# ---------------------------------------------------------------- emit
def _game_meta(path) -> dict:
    d = json.loads(Path(path).read_text())
    m = d.get("meta", {})
    return dict(game_id=m.get("game_id"), commence_utc=m.get("commence_utc"),
                pulled_utc=m.get("pulled_utc") or m.get("lines_retrieved_utc"))


def emit(*, freeze_paths, probs: pd.DataFrame, probs_source: str, roster: pd.DataFrame, pbp: pd.DataFrame,
         date: str, roster_source: str, roster_pulled_utc: str, pbp_source: str, pbp_pulled_utc: str,
         out_root=None, now: datetime | None = None, input_shas: dict | None = None,
         prob_source: str | None = None, qb_override_applied: bool = False) -> dict:
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc).replace(microsecond=0)
    out_root = Path(out_root) if out_root is not None else ROOT / "research/runs"
    games, refused, legs = {}, {}, []
    for f in freeze_paths:
        g = _game_meta(f)
        gid = g["game_id"]
        try:
            wk = int(str(gid).split("_")[1])
        except (IndexError, ValueError):
            raise EmitError(f"{f}: cannot read the week from game_id {gid!r}")
        if wk not in se.HOLDOUT_WEEKS:
            raise EmitError(f"{gid}: live flags are emitted for weeks 10-12 only (holdout); got week {wk}")
        kick, pulled = _utc(g["commence_utc"]), _utc(g["pulled_utc"])
        info = dict(freeze=str(f), kickoff_utc=g["commence_utc"], price_pulled_utc=g["pulled_utc"])
        why = None
        if kick is None:
            why = "kickoff_unknown"
        elif now >= kick:
            why = f"kicked_off (kickoff {fmt_et(kick)}, now {fmt_et(now)})"
        elif pulled is None:
            why = "price_pull_time_unknown"
        elif pulled >= kick:
            why = f"price_pulled_after_kickoff ({fmt_utc(pulled)} >= {fmt_utc(kick)})"
        elif pulled > now:
            why = "price_pull_time_in_future"
        if why:
            refused[gid] = why
            games[gid] = dict(info, refused=why)
            continue
        L = LV.legs_from_freeze_v2(str(f)).drop(columns=["gsis", "position"], errors="ignore")
        if len(L):
            ps = L.price_source.notna()
            L.loc[ps, "price_source"] = L.loc[ps, "price_source"].str.replace(
                "pulled None", f"pulled {g['pulled_utc']}", regex=False)
        L["kickoff_utc"], L["kickoff_et"] = fmt_utc(kick), fmt_et(kick)
        L["price_pulled_utc"] = fmt_utc(pulled)
        L["minutes_to_kickoff"] = (kick - now).total_seconds() / 60.0
        L["price_minutes_before_kickoff"] = (kick - pulled).total_seconds() / 60.0
        games[gid] = dict(info, kickoff_et=fmt_et(kick), minutes_to_kickoff=(kick - now).total_seconds() / 60.0,
                          price_minutes_before_kickoff=(kick - pulled).total_seconds() / 60.0, n_legs=int(len(L)))
        legs.append(L)
    if not legs:
        raise EmitError(f"no game eligible to emit: {refused}")
    legs = pd.concat(legs, ignore_index=True)
    legs = RJ.join_roster(legs, roster, pbp, roster_source=roster_source, roster_pulled_utc=roster_pulled_utc,
                          pbp_source=pbp_source, pbp_pulled_utc=pbp_pulled_utc)
    legs = attach_probs(legs, probs, probs_source)
    graded = LV.grade_live(legs, pbp)          # weeks 10-12 + freeze manifest checked here; frozen params; no refit
    run_utc, run_et = fmt_utc(now), fmt_et(now)
    graded["emitted_utc"], graded["emitted_et"] = run_utc, run_et
    graded["projection_ready"] = False
    graded = stamp_countable(graded, prob_source=prob_source, qb_override_applied=qb_override_applied)
    countable, declared_src, countable_reason = countable_decision(prob_source, bool(qb_override_applied))
    out_dir = out_root / f"{date}_live_flags"
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    paths = {k: out_dir / f"flags_{stamp}.{k}" for k in ("csv", "json", "md")}
    if any(p.exists() for p in paths.values()):
        raise EmitError(f"{paths['csv']} exists; a run is never overwritten")
    out_dir.mkdir(parents=True, exist_ok=True)
    graded.to_csv(paths["csv"], index=False)
    inputs = dict(input_shas or {})
    inputs.setdefault("freeze", {str(f): _sha(f) for f in freeze_paths if Path(f).exists()})
    inputs.setdefault("probs", _sha_bytes(probs.to_csv(index=False).encode()))
    inputs.setdefault("roster", _sha_bytes(roster.to_csv(index=False).encode()))
    inputs.setdefault("pbp", _sha_bytes(pd.util.hash_pandas_object(pbp, index=False).values.tobytes()))
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    counts = graded.groupby(["game_id", "label"]).size().rename("n").reset_index()
    manifest = {
        "schema": SCHEMA, "run_utc": run_utc, "run_et": run_et, "date": date, "code_commit": head,
        "code_sha256": {f: _sha(ROOT / f) for f in ("calibration/selective_edge_emit.py",
                                                     "calibration/selective_edge_roster.py")},
        "freeze_manifest_sha256": _sha(MANIFEST), "inputs_sha256": inputs, "probs_source": probs_source,
        "roster": {"source": roster_source, "pulled_utc": roster_pulled_utc},
        "pbp": {"source": pbp_source, "pulled_utc": pbp_pulled_utc},
        "games": games, "refused_games": refused, "emitted_games": sorted(set(graded.game_id)),
        "label_counts": counts.to_dict("records"), "files": {k: p.name for k, p in paths.items()},
        "prob_source": declared_src, "qb_override_applied": bool(qb_override_applied),
        "countable": countable, "countable_reason": countable_reason,
        "research_only": True, "projection_ready": False,
        "note": "Research flags from the frozen Phase 4 classifier; not picks, not vetted. Receiving legs stay "
                "INSUFFICIENT EVIDENCE without a verified main defender. A flag is countable toward a Sunday "
                "graduation spot only when p_model is the legacy sim_v5/v6 ensemble the classifier was fit on "
                "and the depth-chart/inactives QB override was applied; otherwise countable=false. The file "
                "must still be committed with a timestamp before kickoff."}
    paths["json"].write_text(json.dumps(manifest, indent=1, default=str) + "\n")
    cand = graded[graded.label.isin(se.CANDIDATE_LABELS)]
    show = ["game_id", "player", "position", "market", "side", "line", "dec", "p_nv", "p_model", "edge", "edge_tier",
            "label", "countable", "countable_mark", "season_carry_share", "price_source"]
    countable_line = (
        f"countable={str(countable).lower()} prob_source={declared_src or '(missing)'} "
        f"qb_override_applied={str(bool(qb_override_applied)).lower()}"
        + ("" if countable else f". Non-countable flags are marked [NOT COUNTABLE: {countable_reason}].")
    )
    md = [f"# Live flags {date}, run {run_utc} ({run_et})", "",
          "Research only, not picks, not vetted. projection_ready false. refs NFL-75.",
          countable_line, "",
          f"Games emitted: {', '.join(manifest['emitted_games'])}. Refused: {refused or 'none'}.", "",
          "Candidate labels:" if len(cand) else "No candidate labels (every leg is INSUFFICIENT EVIDENCE or NO EDGE).",
          ""]
    if len(cand):
        md.append(cand[[c for c in show if c in cand]].to_string(index=False))  # no tabulate dependency
    md += ["", "Reasons:", "", graded.groupby(["label", "reason"]).size().rename("n").reset_index()
           .to_string(index=False)]
    paths["md"].write_text("\n".join(md) + "\n")
    return dict(out_dir=out_dir, flags_csv=paths["csv"], manifest_json=paths["json"], summary_md=paths["md"],
                emitted_games=manifest["emitted_games"], refused_games=refused, run_utc=run_utc, run_et=run_et)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--date", required=True, help="slate date YYYY-MM-DD (output dir research/runs/<date>_live_flags)")
    ap.add_argument("--freeze", action="append", required=True)
    ap.add_argument("--probs", action="append", required=True, help="rush_dist dir or *.rush_dist.cdf.csv")
    ap.add_argument("--roster", required=True)
    ap.add_argument("--roster-pulled-utc", help="defaults to <roster>.retrieved_utc sidecar")
    ap.add_argument("--pbp", required=True)
    ap.add_argument("--pbp-pulled-utc", help="defaults to <pbp>.retrieved_utc sidecar or provenance.json")
    ap.add_argument("--prob-source", default=None,
                    help="Declared p_model family. countable=true only for sim_v5_v6_ensemble with "
                         "--qb-override-applied. Missing or unknown sources default to countable=false.")
    ap.add_argument("--qb-override-applied", action="store_true",
                    help="Caller certifies the depth-chart/inactives QB override was applied to these probabilities.")
    ap.add_argument("--commit", action="store_true")
    ap.add_argument("--push", action="store_true")
    a = ap.parse_args(argv)

    def pulled(path, given):
        if given:
            return given
        side = Path(str(path) + ".retrieved_utc")
        if side.exists():
            return side.read_text().strip()
        prov = Path(str(path).replace(".parquet", ".provenance.json"))
        if prov.exists():
            return json.loads(prov.read_text()).get("pulled_et")
        raise EmitError(f"no pull time for {path}: pass it explicitly")

    probs, prob_shas = load_probs(a.probs)
    roster = pd.read_parquet(a.roster)
    pbp = pd.read_parquet(a.pbp)
    shas = {"freeze": {f: _sha(f) for f in a.freeze}, "probs": prob_shas, "roster": _sha(a.roster),
            "pbp": _sha(a.pbp)}
    r = emit(freeze_paths=a.freeze, probs=probs, probs_source=f"{PROB_SCHEMA} " + ", ".join(
                 f"{Path(k).name} sha256={v[:12]}" for k, v in prob_shas.items()),
             roster=roster, pbp=pbp, date=a.date, roster_source=f"{a.roster} sha256={shas['roster'][:12]}",
             roster_pulled_utc=pulled(a.roster, a.roster_pulled_utc),
             pbp_source=f"{a.pbp} sha256={shas['pbp'][:12]}", pbp_pulled_utc=pulled(a.pbp, a.pbp_pulled_utc),
             input_shas=shas, prob_source=a.prob_source, qb_override_applied=a.qb_override_applied)
    print(json.dumps({k: str(v) for k, v in r.items()}, indent=1))
    if a.commit or a.push:
        rel = str(r["out_dir"].relative_to(ROOT))
        branch, sha = commit_and_push([r["flags_csv"], r["manifest_json"], r["summary_md"]], rel, a.date,
                                      r["run_utc"], r["emitted_games"], push=a.push)
        print(f"committed {sha} on {branch}" + (" and pushed" if a.push else ""))


if __name__ == "__main__":
    main()
