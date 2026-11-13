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
countable is decided per flag from the probability FILE's embedded provenance, never from the CLI. --probs also
accepts `<game_id>.simv56.probs.csv` (schema nfl75-simv56-probs/1, written by calibration/simv56_pmodel.py). These
files carry prob_source, the code git sha, input sha256s, the applied per-team QB override list (starter, source URLs,
retrieved-UTC timestamps, qb_gate), plus a data digest and a provenance digest; p_model is the file's exact
P(X>=L)-based value at the priced line, the way the Phase 4 fit used it. countable=true only when the file verifies
(digests match, full 40-hex git sha, clean code), says prob_source=sim_v5_v6_ensemble, the flag's team equals the
probability row's team, and the file has an ok QB override entry for that team. Otherwise countable=false with a
reason: p_model_not_from_probs_file, prob_provenance_missing (e.g. PR #43 rush_dist CDF), prob_provenance_incomplete,
prob_provenance_inconsistent, prob_code_dirty, prob_schema_unknown, prob_data_digest_mismatch,
prob_provenance_digest_mismatch, embedded_prob_source_not_fit_ensemble, cli_prob_source_mismatch, prob_team_mismatch,
qb_override_missing_for_team, qb_override_incomplete_for_team, qb_override_not_ok_for_team.
--prob-source / --qb-override-applied are recorded (prob_source_declared, qb_override_declared); a declared source
that contradicts the file vetoes, but neither flag can make a flag countable. STRONG UNDER labels are still written.
--commit stages only that run's files on the current research/* branch; --push pushes that branch. Both refuse if any
staged path is outside the run directory or if the branch diff vs origin/main touches pregame/ or .github/.
projection_ready is always false. Receiving legs stay INSUFFICIENT EVIDENCE (no verified main defender)."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
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
# Probability files that embed their own provenance (calibration/simv56_pmodel.py, PR #45). Spec, all CSV text:
#   data        game_id, team, player, gsis, position, market, line, p_under, p_over (floats as repr())
#   provenance  prob_schema, prob_source, p_model_settings, code_git_sha, code_dirty, code_sha256, inputs_sha256
#               (canonical JSON), qb_overrides (canonical JSON list), generated_utc, data_sha256, provenance_sha256
#   data_sha256       = sha256("game_id,team,gsis,market,line,p_under,p_over\n" per row, sorted by
#                       (game_id, gsis, market, float(line)))
#   provenance_sha256 = sha256(canonical JSON of the provenance fields except itself; JSON fields as objects,
#                       code_dirty as bool)
SIMV56_SCHEMA = "nfl75-simv56-probs/1"
SIMV56_GLOB = "*.simv56.probs.csv"
SIMV56_DATA = ("game_id", "team", "player", "gsis", "position", "market", "line", "p_under", "p_over")
SIMV56_PROV = ("prob_schema", "prob_source", "p_model_settings", "code_git_sha", "code_dirty", "code_sha256",
               "inputs_sha256", "qb_overrides", "generated_utc", "data_sha256", "provenance_sha256")
_JSON_FIELDS = ("inputs_sha256", "qb_overrides")
_HEX40, _HEX64 = re.compile(r"[0-9a-f]{40}"), re.compile(r"[0-9a-f]{64}")
QB_ENTRY_REQUIRED = ("starter", "starter_gsis", "depth_source", "depth_retrieved_utc", "injury_source",
                     "injury_retrieved_utc")
PROV_COLS = ("prob_schema", "prob_source", "prov_status", "prov_file", "prov_sha256", "prov_code_git_sha",
             "prov_qb_overrides", "prob_team")


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


def _canon(x) -> str:
    return json.dumps(x, sort_keys=True, separators=(",", ":"))


def _simv56_data_digest(t: pd.DataFrame) -> str:
    rows = sorted(t[list(SIMV56_DATA)].to_dict("records"),
                  key=lambda r: (r["game_id"], r["gsis"], r["market"], float(r["line"])))
    body = "".join(",".join(r[c] for c in ("game_id", "team", "gsis", "market", "line", "p_under", "p_over")) + "\n"
                   for r in rows)
    return _sha_bytes(body.encode())


def verify_simv56(t: pd.DataFrame) -> tuple[str, dict | None]:
    """Verify one nfl75-simv56-probs/1 file read as text. Returns (status, provenance); status 'ok' or a reason."""
    if any(c not in t for c in SIMV56_DATA + SIMV56_PROV) or t.empty:
        return "prob_provenance_missing", None
    if any(t[c].nunique(dropna=False) != 1 for c in SIMV56_PROV):
        return "prob_provenance_inconsistent", None
    row = t.iloc[0]
    prov = {}
    try:
        for k in SIMV56_PROV[:-1]:
            v = row[k]
            prov[k] = json.loads(v) if k in _JSON_FIELDS else v
    except (TypeError, ValueError):
        return "prob_provenance_incomplete", None
    if row["code_dirty"] not in ("true", "false"):
        return "prob_provenance_incomplete", None
    prov["code_dirty"] = row["code_dirty"] == "true"
    if prov["prob_schema"] != SIMV56_SCHEMA:
        return "prob_schema_unknown", None
    ins, qb = prov["inputs_sha256"], prov["qb_overrides"]
    if (not _HEX40.fullmatch(str(prov["code_git_sha"])) or not _HEX64.fullmatch(str(prov["code_sha256"]))
            or not isinstance(ins, dict) or not ins or not all(_HEX64.fullmatch(str(v)) for v in ins.values())
            or not isinstance(qb, list) or not all(isinstance(d, dict) for d in qb)
            or not str(prov["prob_source"]).strip() or not str(prov["generated_utc"]).strip()):
        return "prob_provenance_incomplete", None
    if prov["code_dirty"]:
        return "prob_code_dirty", None
    try:
        if _simv56_data_digest(t) != prov["data_sha256"]:
            return "prob_data_digest_mismatch", None
    except ValueError:
        return "prob_data_digest_mismatch", None
    if _sha_bytes(_canon(prov).encode()) != row["provenance_sha256"]:
        return "prob_provenance_digest_mismatch", None
    return "ok", dict(prov, provenance_sha256=row["provenance_sha256"])


def _load_simv56(f: Path) -> pd.DataFrame:
    t = pd.read_csv(f, dtype=str, keep_default_na=False)
    status, prov = verify_simv56(t)
    out = pd.DataFrame({c: t[c] if c in t else "" for c in ("game_id", "team", "player", "gsis", "position")})
    for c in ("line", "p_under", "p_over"):
        out[c] = [float(v) if v not in ("", None) else np.nan for v in (t[c] if c in t else [""] * len(t))]
    out["prob_schema"] = SIMV56_SCHEMA
    ok = status == "ok"
    out["prob_source"] = prov["prob_source"] if ok else ""
    out["prov_status"], out["prov_file"] = status, str(f)
    out["prov_sha256"] = prov["provenance_sha256"] if ok else ""
    out["prov_code_git_sha"] = prov["code_git_sha"] if ok else ""
    out["prov_qb_overrides"] = _canon(prov["qb_overrides"]) if ok else ""
    out["prob_team"] = out["team"]
    return out


def load_probs(paths) -> tuple[pd.DataFrame, dict]:
    files = []
    for p in paths:
        p = Path(p)
        files += (sorted(p.glob("*.rush_dist.cdf.csv")) + sorted(p.glob(SIMV56_GLOB))) if p.is_dir() else [p]
    if not files:
        raise EmitError("no rush_dist CDF or simv56 probability files found")
    shas, dfs = {}, []
    for f in files:
        if f.name.endswith(".simv56.probs.csv"):
            shas[str(f)] = _sha(f)
            dfs.append(_load_simv56(f))
            continue
        meta = f.with_name(f.name.replace(".cdf.csv", ".json"))
        if meta.exists():
            m = json.loads(meta.read_text())
            if m.get("schema") != PROB_SCHEMA or m.get("projection_ready") not in (False, None):
                raise EmitError(f"{meta.name}: schema {m.get('schema')!r} is not {PROB_SCHEMA}")
        shas[str(f)] = _sha(f)
        d = check_probs(pd.read_csv(f, dtype={"gsis": str}))
        d["prob_schema"], d["prob_source"], d["prov_status"], d["prov_file"] = PROB_SCHEMA, "", \
            "prob_provenance_missing", str(f)
        dfs.append(d)
    return pd.concat(dfs, ignore_index=True), shas


def attach_probs(legs: pd.DataFrame, cdf: pd.DataFrame, source: str) -> pd.DataFrame:
    check_probs(cdf)
    out = legs.copy()
    if "p_model" not in out:
        out["p_model"] = np.nan
    out["p_model"] = out.p_model.astype(float)
    idx = {k: g.set_index(g.line.round(1)) for k, g in cdf.groupby(["game_id", "gsis"])}
    prov = {c: [None] * len(out) for c in PROV_COLS}
    match, src = [], []
    for n, (i, r) in enumerate(out.iterrows()):
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
        if "prov_file" in h and h.prov_file.nunique() > 1:
            match.append("ambiguous_probs"); src.append(None); continue
        L = float(r.line)
        if "prob_schema" in h and h.prob_schema.iloc[0] == SIMV56_SCHEMA:
            # legacy ensemble file: P(X>=L) / 1-P(X>=L) at the exact priced line, as the Phase 4 fit used it
            k = round(L, 1)
            side = str(r.side)
            if k not in h.index or side not in ("Under", "Over"):
                match.append("line_off_grid" if k not in h.index else "undefined"); src.append(None); continue
            out.at[i, "p_model"] = float(h.loc[k, "p_under" if side == "Under" else "p_over"])
            match.append("gsis"); src.append(source)
            for c in PROV_COLS:
                prov[c][n] = h[c].iloc[0] if c in h else None
            continue
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
        for c in PROV_COLS:
            prov[c][n] = h[c].iloc[0] if c in h else None
        if "prov_status" not in h:
            prov["prov_status"][n] = "prob_provenance_missing"
    out["p_model_match"], out["p_model_source"] = match, src
    for c in PROV_COLS:
        out[c] = prov[c]
    return out


# ---------------------------------------------------------------- countable stamp
def _declared_prob_source(prob_source) -> str:
    if prob_source is None or (isinstance(prob_source, float) and np.isnan(prob_source)):
        return ""
    return str(prob_source).strip()


def not_countable_mark(countable: bool, reason: str) -> str:
    return "" if countable else f"[NOT COUNTABLE: {reason}]"


def _blank(v) -> bool:
    return v is None or (isinstance(v, float) and np.isnan(v)) or str(v).strip() == ""


def _team_qb_entry(qb_json, team):
    if _blank(qb_json) or _blank(team):
        return None
    for d in json.loads(qb_json):
        if d.get("team") == team:
            return d
    return None


def row_countable(r, declared_source: str) -> tuple[bool, str, dict | None]:
    """Countable from the probability file's verified, embedded provenance only. The CLI declaration can veto
    (cli_prob_source_mismatch) but can never make a flag countable."""
    if r.get("p_model_match") != "gsis":
        return False, "p_model_not_from_probs_file", None
    status = r.get("prov_status")
    if _blank(status):
        return False, "prob_provenance_missing", None
    if status != "ok":
        return False, str(status), None
    emb = str(r.get("prob_source") or "")
    if emb != FIT_ENSEMBLE_PROB_SOURCE:
        return False, "embedded_prob_source_not_fit_ensemble", None
    if declared_source and declared_source != emb:
        return False, "cli_prob_source_mismatch", None
    team = r.get("team")
    if _blank(team) or team != r.get("prob_team"):
        return False, "prob_team_mismatch", None
    e = _team_qb_entry(r.get("prov_qb_overrides"), team)
    if e is None:
        return False, "qb_override_missing_for_team", None
    if any(_blank(e.get(k)) for k in QB_ENTRY_REQUIRED):
        return False, "qb_override_incomplete_for_team", e
    if e.get("qb_gate") != "ok":
        return False, "qb_override_not_ok_for_team", e
    return True, "embedded_fit_ensemble_with_qb_override", e


def stamp_countable(legs: pd.DataFrame, *, prob_source: str | None = None,
                    qb_override_applied: bool = False) -> pd.DataFrame:
    """Stamp every flag with countable, prob_source (embedded, verified), countable_reason and a writer mark.

    countable=true only when the flag's p_model came from a probability file whose embedded provenance verifies
    (digests match, full git sha, clean code), says prob_source=sim_v5_v6_ensemble (the legacy ensemble the Phase 4
    classifier was fit on), and carries an ok QB override entry (starter, source, timestamps) for the flag's team.
    --prob-source / --qb-override-applied are recorded as prob_source_declared / qb_override_declared; a declared
    source that contradicts the file vetoes, but neither flag can make a flag countable. Labels are unchanged.
    """
    declared = _declared_prob_source(prob_source)
    out = legs.copy()
    dec = [row_countable(r, declared) for r in out.to_dict("records")]
    out["prob_source"] = [str(r.get("prob_source") or "") if d[0] or r.get("prov_status") == "ok" else ""
                          for r, d in zip(out.to_dict("records"), dec)]
    out["prob_source_declared"] = declared
    out["qb_override_declared"] = bool(qb_override_applied)
    out["countable"] = [d[0] for d in dec]
    out["countable_reason"] = [d[1] for d in dec]
    out["countable_mark"] = [not_countable_mark(d[0], d[1]) for d in dec]
    out["qb_override_entry"] = [_canon(d[2]) if d[2] else "" for d in dec]
    out["prob_provenance_sha256"] = out["prov_sha256"] if "prov_sha256" in out else ""
    out["prob_code_git_sha"] = out["prov_code_git_sha"] if "prov_code_git_sha" in out else ""
    return out


def prob_files_provenance(probs: pd.DataFrame) -> dict:
    if "prov_file" not in probs:
        return {}
    res = {}
    for f, g in probs.groupby("prov_file", sort=True):
        r = g.iloc[0]
        qb = json.loads(r["prov_qb_overrides"]) if not _blank(r.get("prov_qb_overrides")) else []
        res[str(f)] = dict(schema=r.get("prob_schema"), status=r.get("prov_status"),
                           prob_source=r.get("prob_source") or "", code_git_sha=r.get("prov_code_git_sha") or "",
                           provenance_sha256=r.get("prov_sha256") or "",
                           qb_override_teams_ok=sorted(d.get("team") for d in qb if d.get("qb_gate") == "ok"
                                                       and not any(_blank(d.get(k)) for k in QB_ENTRY_REQUIRED)),
                           qb_overrides=qb)
    return res


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
    declared_src = _declared_prob_source(prob_source)
    countable = bool(graded.countable.any())
    countable_counts = {str(k): int(v) for k, v in graded.countable_reason.value_counts().items()}
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
        "prob_source_declared": declared_src, "qb_override_declared": bool(qb_override_applied),
        "prob_files_provenance": prob_files_provenance(probs),
        "countable": countable, "countable_counts": countable_counts,
        "n_countable": int(graded.countable.sum()),
        "research_only": True, "projection_ready": False,
        "note": "Research flags from the frozen Phase 4 classifier; not picks, not vetted. Receiving legs stay "
                "INSUFFICIENT EVIDENCE without a verified main defender. A flag is countable toward a Sunday "
                "graduation spot only when its probability file's embedded, digest-verified provenance says the legacy "
                "sim_v5/v6 ensemble the classifier was fit on and carries an ok QB override for the flag's team; "
                "the CLI flags cannot make a flag countable; otherwise countable=false. The file "
                "must still be committed with a timestamp before kickoff."}
    paths["json"].write_text(json.dumps(manifest, indent=1, default=str) + "\n")
    cand = graded[graded.label.isin(se.CANDIDATE_LABELS)]
    show = ["game_id", "player", "position", "market", "side", "line", "dec", "p_nv", "p_model", "edge", "edge_tier",
            "label", "countable", "countable_mark", "season_carry_share", "price_source"]
    countable_line = (
        f"countable flags: {int(graded.countable.sum())} of {len(graded)} (from embedded, verified probability-file "
        f"provenance; declared --prob-source={declared_src or '(none)'}, "
        f"--qb-override-applied={str(bool(qb_override_applied)).lower()} are not trusted). "
        f"Reasons: {countable_counts}. Non-countable flags are marked [NOT COUNTABLE: <reason>]."
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
    ap.add_argument("--probs", action="append", required=True,
                    help="dir, *.rush_dist.cdf.csv or *.simv56.probs.csv (embedded provenance)")
    ap.add_argument("--roster", required=True)
    ap.add_argument("--roster-pulled-utc", help="defaults to <roster>.retrieved_utc sidecar")
    ap.add_argument("--pbp", required=True)
    ap.add_argument("--pbp-pulled-utc", help="defaults to <pbp>.retrieved_utc sidecar or provenance.json")
    ap.add_argument("--prob-source", default=None,
                    help="Declared p_model family (recorded only). countable comes from the probability "
                         "file's embedded provenance; a declaration that contradicts it vetoes countable.")
    ap.add_argument("--qb-override-applied", action="store_true",
                    help="Recorded only; the QB override must be embedded in the probability file per team.")
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
    r = emit(freeze_paths=a.freeze, probs=probs, probs_source=" + ".join(sorted(set(probs.prob_schema))) + " " + ", ".join(
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
