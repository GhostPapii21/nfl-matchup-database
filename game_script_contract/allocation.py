"""Probability-allocation contract and integrity detectors for game-script scenario outputs.

Contract (full text: docs/specs/game_script_probability_contract.md):
  1. Exactly three branches: favorite_controls, competitive, underdog_chases. No missing, extra or duplicate keys.
  2. Every branch probability is a finite real number in [0, 1]; the three total 1 within TOLERANCE (1e-6).
  3. When probability_basis == "trial_partition", P(branch) == n_trials(branch) / n_trials_total and the branch
     counts add to n_trials_total.
  4. A player/team prop probability is a mixture of per-branch conditional probabilities:
         P(prop) = sum_b P(b) * P(prop | b)
     where P(prop | b) is computed from branch b's OWN distribution. It is never computed from a pooled (averaged)
     stat line, and no branch may borrow another branch's distribution.
  5. Branches must not be pooled (collapsed to the same values) or duplicated (same payload / same object).

Nothing here simulates anything; it only validates payloads and computes the mixture from what the payload carries.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Any, Iterable, Optional

import numpy as np

from .schema import BRANCH_IDS, DIMENSIONS, load_json_schema

TOLERANCE = 1e-6          # branch probabilities must total 1 within this
_EQ_ATOL = 1e-12          # absolute tolerance when comparing values that should differ between branches
TEAM_DIST_FIELDS = ("points", "plays", "possessions", "pass_attempts", "rush_attempts", "sec_per_play",
                    "red_zone_trips", "touchdowns", "pressure_rate_faced")
PLAYER_DIST_FIELDS = ("targets", "receptions", "carries", "rush_opportunities", "red_zone_targets",
                      "red_zone_carries", "td_opportunities", "snap_share_q4")
QUARTERS = ("q1", "q2", "q3", "q4")
# Dimensions where "derived" (trial selection from a game-state-blind engine) means the branch carries no change in
# team BEHAVIOUR, only in which trials were kept. Flagged as a warning so it is visible, never silently accepted.
BEHAVIOURAL_DIMENSIONS = ("plays_possessions", "pass_run", "pace", "player_opportunity", "red_zone",
                          "touchdown_opportunity", "pressure_coverage", "late_game_rotation")


class ContractError(ValueError):
    """Raised when a payload cannot be priced or validated under the contract."""


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str          # "error" | "warning"
    message: str
    location: str = ""

    def __str__(self) -> str:  # pragma: no cover - display only
        return f"[{self.severity}] {self.code} @ {self.location}: {self.message}"


def errors(findings: Iterable[Finding]) -> list[Finding]:
    return [f for f in findings if f.severity == "error"]


# ----------------------------------------------------------------------------------------------- strict JSON loading
def loads_strict(text: str) -> dict:
    """json.loads that rejects duplicate object keys (a duplicated branch key would otherwise silently overwrite)."""
    def hook(pairs):
        seen = {}
        for k, v in pairs:
            if k in seen:
                raise ContractError(f"duplicate key {k!r} in JSON object")
            seen[k] = v
        return seen
    return json.loads(text, object_pairs_hook=hook)


# ------------------------------------------------------------------------------------------------ branch partition
def classify_margin(margin: float, definition: dict) -> str:
    """Branch for a favorite-perspective margin under the payload's branch_definition (disjoint and exhaustive)."""
    if margin >= definition["favorite_controls_min_margin"]:
        return "favorite_controls"
    if margin <= definition["underdog_chases_max_margin"]:
        return "underdog_chases"
    return "competitive"


# ---------------------------------------------------------------------------------------------- distribution helpers
def _support(dist: dict) -> tuple[np.ndarray, np.ndarray]:
    """(values, probabilities) of a distribution object; samples take precedence over pmf."""
    if dist.get("samples") is not None:
        vals, counts = np.unique(np.asarray(dist["samples"], dtype=float), return_counts=True)
        return vals, counts / counts.sum()
    if dist.get("pmf"):
        items = sorted((float(k), float(v)) for k, v in dist["pmf"].items())
        vals = np.array([k for k, _ in items]); probs = np.array([v for _, v in items])
        s = probs.sum()
        if not math.isfinite(s) or s <= 0 or abs(s - 1) > 1e-6:
            raise ContractError(f"pmf does not sum to 1 (sum={s})")
        return vals, probs
    raise ContractError("distribution has neither samples nor pmf")


def dist_mean(dist: dict) -> float:
    v, p = _support(dist)
    return float((v * p).sum())


def _tail(dist: dict, line: float, side: str) -> tuple[float, float]:
    v, p = _support(dist)
    push = float(p[np.isclose(v, line, rtol=0, atol=1e-12)].sum())
    if side == "over":
        return float(p[v > line + 1e-12].sum()), push
    if side == "under":
        return float(p[v < line - 1e-12].sum()), push
    raise ContractError(f"side must be 'over' or 'under', not {side!r}")


def _same_distribution(a: dict, b: dict, rel_tol: float) -> bool:
    va, pa = _support(a); vb, pb = _support(b)
    return va.shape == vb.shape and np.allclose(va, vb, rtol=rel_tol, atol=_EQ_ATOL) and \
        np.allclose(pa, pb, rtol=rel_tol, atol=_EQ_ATOL)


# ------------------------------------------------------------------------------------------- probability allocation
def _is_real(x: Any) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def validate_allocation(obj: dict, *, tol: float = TOLERANCE, check_counts: bool = True) -> list[Finding]:
    """Check the probability allocation. `obj` is a full payload or a plain {branch_id: probability} mapping."""
    out: list[Finding] = []
    is_payload = isinstance(obj, dict) and "branches" in obj
    branches = obj["branches"] if is_payload else obj
    if not isinstance(branches, dict):
        return [Finding("ALLOCATION_NOT_MAPPING", "error", "branches must be a mapping keyed by branch id")]
    keys = set(branches)
    for k in sorted(set(BRANCH_IDS) - keys):
        out.append(Finding("BRANCH_MISSING", "error", f"required branch {k!r} is missing", k))
    for k in sorted(keys - set(BRANCH_IDS), key=str):
        out.append(Finding("BRANCH_EXTRA", "error", f"unknown branch {k!r}; exactly {BRANCH_IDS} are allowed", str(k)))
    probs: dict[str, float] = {}
    for k in BRANCH_IDS:
        if k not in branches:
            continue
        b = branches[k]
        p = b.get("probability") if is_payload else b
        if is_payload and b.get("branch_id") != k:
            out.append(Finding("BRANCH_ID_MISMATCH", "error", f"branch under key {k!r} says branch_id={b.get('branch_id')!r}", k))
        if not _is_real(p) or not math.isfinite(float(p)):
            out.append(Finding("PROBABILITY_NOT_FINITE", "error", f"probability {p!r} is not a finite number", k))
            continue
        if p < 0:
            out.append(Finding("PROBABILITY_NEGATIVE", "error", f"probability {p} < 0", k))
        if p > 1:
            out.append(Finding("PROBABILITY_ABOVE_ONE", "error", f"probability {p} > 1", k))
        probs[k] = float(p)
    if len(probs) == len(BRANCH_IDS) and not any(f.code in ("BRANCH_EXTRA",) for f in out):
        total = math.fsum(probs.values())
        if abs(total - 1.0) > tol:
            out.append(Finding("PROBABILITY_SUM", "error",
                               f"branch probabilities total {total:.9f} ({100 * total:.6f}%), not 100% within {tol}"))
    if is_payload and check_counts and (obj.get("provenance") or {}).get("probability_basis") == "trial_partition" \
            and len(probs) == len(BRANCH_IDS):
        n_total = obj["provenance"].get("n_trials_total")
        counts = {k: branches[k].get("n_trials") for k in BRANCH_IDS}
        if all(isinstance(c, int) for c in counts.values()) and isinstance(n_total, int) and n_total > 0:
            if sum(counts.values()) != n_total:
                out.append(Finding("COUNT_TOTAL_MISMATCH", "error",
                                   f"branch n_trials total {sum(counts.values())} != n_trials_total {n_total}"))
            for k in BRANCH_IDS:
                if abs(probs[k] - counts[k] / n_total) > tol:
                    out.append(Finding("COUNT_PROBABILITY_MISMATCH", "error",
                                       f"probability {probs[k]} != n_trials/n_trials_total {counts[k]}/{n_total}", k))
    return out


# ---------------------------------------------------------------------------------------------------- prop pricing
def _entity(branch: dict, player_id: Optional[str], team: Optional[str]) -> Optional[dict]:
    if player_id is not None:
        return next((p for p in branch.get("players", []) if p.get("player_id") == player_id), None)
    return (branch.get("teams") or {}).get(team)


def prop_probability(payload: dict, *, stat: str, line: float, side: str = "over",
                     player_id: Optional[str] = None, team: Optional[str] = None) -> dict:
    """P(prop) = sum_b P(b) * P(prop | b), each conditional from that branch's own distribution.

    Raises ContractError (never falls back to another branch or a pooled line) when a branch with positive
    probability cannot be priced."""
    if (player_id is None) == (team is None):
        raise ContractError("give exactly one of player_id or team")
    bad = errors(validate_allocation(payload))
    if bad:
        raise ContractError("allocation invalid: " + "; ".join(f.code for f in bad))
    per_branch, total, push_total = {}, 0.0, 0.0
    for b in BRANCH_IDS:
        br = payload["branches"][b]
        w = float(br["probability"])
        ent = _entity(br, player_id, team)
        dist = None if ent is None else ent.get(stat)
        if dist is None:
            if w > 0:
                raise ContractError(f"branch {b} (P={w}) has no {stat!r} distribution for "
                                    f"{player_id or team}; refusing to borrow another branch or a pooled line")
            per_branch[b] = {"weight": w, "conditional": None, "push": None}
            continue
        cond, push = _tail(dist, float(line), side)
        per_branch[b] = {"weight": w, "conditional": cond, "push": push, "mean": dist_mean(dist)}
        total += w * cond
        push_total += w * push
    return {"probability": total, "push": push_total, "per_branch": per_branch, "method": "branch_mixture_v1",
            "stat": stat, "line": line, "side": side, "player_id": player_id, "team": team}


def check_prop_probability(payload: dict, claimed: float, *, stat: str, line: float, side: str = "over",
                           player_id: Optional[str] = None, team: Optional[str] = None,
                           tol: float = 1e-6) -> list[Finding]:
    """Flag a reported prop probability that is not the branch mixture, naming the pooling pattern it matches."""
    mix = prop_probability(payload, stat=stat, line=line, side=side, player_id=player_id, team=team)
    if abs(claimed - mix["probability"]) <= tol:
        return []
    loc = f"{player_id or team}:{stat}:{side}{line}"
    pooled_mean = sum(v["weight"] * v["mean"] for v in mix["per_branch"].values() if v.get("mean") is not None)
    matches = []
    # Pooled-line signatures: the averaged stat line pushed through a single distribution.
    from math import exp, lgamma, log
    k = math.floor(line) if side == "over" else math.ceil(line) - 1
    if pooled_mean > 0 and k >= 0:
        cdf = sum(exp(i * log(pooled_mean) - pooled_mean - lgamma(i + 1)) for i in range(int(k) + 1))
        pois = 1 - cdf if side == "over" else cdf
        if abs(claimed - pois) <= max(tol, 1e-4):
            matches.append("Poisson(pooled mean)")
    point = float(pooled_mean > line) if side == "over" else float(pooled_mean < line)
    if abs(claimed - point) <= tol:
        matches.append("indicator(pooled mean vs line)")
    for b, v in mix["per_branch"].items():
        if v["conditional"] is not None and abs(claimed - v["conditional"]) <= tol:
            matches.append(f"single branch {b} only")
    hint = (" matches " + ", ".join(matches)) if matches else ""
    return [Finding("PROP_NOT_BRANCH_MIXTURE", "error",
                    f"claimed {claimed:.6f} != branch mixture {mix['probability']:.6f} (pooled mean "
                    f"{pooled_mean:.4f}){hint}", loc)]


# ------------------------------------------------------------------------------------------------- tree utilities
def _dist_fields(branch: dict):
    """Yield (path, distribution) for every distribution in a branch."""
    for t, tb in sorted((branch.get("teams") or {}).items()):
        for f in TEAM_DIST_FIELDS:
            if tb.get(f) is not None:
                yield f"teams.{t}.{f}", tb[f]
        qp = tb.get("quarter_points")
        if qp:
            for q in (*QUARTERS, "ot"):
                if qp.get(q) is not None:
                    yield f"teams.{t}.quarter_points.{q}", qp[q]
    for p in branch.get("players") or []:
        for f in PLAYER_DIST_FIELDS:
            if p.get(f) is not None:
                yield f"players.{p.get('player_id')}.{f}", p[f]


def _containers(obj, path=""):
    if isinstance(obj, dict):
        yield id(obj), path, obj
        for k, v in obj.items():
            yield from _containers(v, f"{path}.{k}" if path else str(k))
    elif isinstance(obj, list):
        yield id(obj), path, obj
        for i, v in enumerate(obj):
            if isinstance(v, (dict, list)):
                yield from _containers(v, f"{path}[{i}]")


def _numeric_leaves(obj, path=""):
    if isinstance(obj, dict):
        for k in sorted(obj):
            yield from _numeric_leaves(obj[k], f"{path}.{k}" if path else str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _numeric_leaves(v, f"{path}[{i}]")
    elif _is_real(obj):
        yield path, float(obj)
    else:
        yield path, obj


_BRANCH_META = ("branch_id", "probability", "n_trials")


def _strip(branch: dict) -> dict:
    return {k: v for k, v in branch.items() if k not in _BRANCH_META}


# ---------------------------------------------------------------------------------------------- duplicate detection
def detect_duplicate_branches(payload: dict, rel_tol: float = 1e-9) -> list[Finding]:
    """Find duplicated scenario outputs: shared objects, identical payloads, near-identical payloads, copied fields."""
    out: list[Finding] = []
    br = payload.get("branches") or {}
    ids = [b for b in BRANCH_IDS if isinstance(br.get(b), dict)]
    owners: dict[int, tuple[str, str]] = {}
    for b in ids:
        for oid, path, _ in _containers(br[b]):
            if oid in owners and owners[oid][0] != b:
                a, apath = owners[oid]
                code = "SHARED_BRANCH_OBJECT" if path == "" else "SHARED_SUBOBJECT"
                out.append(Finding(code, "error", f"{b}.{path or '<branch>'} is the same object as "
                                   f"{a}.{apath or '<branch>'} (copy-by-reference)", f"{a}/{b}"))
            else:
                owners.setdefault(oid, (b, path))
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            A, B = _strip(br[a]), _strip(br[b])
            pair = f"{a}/{b}"
            if json.dumps(A, sort_keys=True) == json.dumps(B, sort_keys=True):
                out.append(Finding("IDENTICAL_BRANCH_PAYLOAD", "error",
                                   "branch payloads are identical apart from branch_id/probability/n_trials", pair))
                continue
            la, lb = list(_numeric_leaves(A)), list(_numeric_leaves(B))
            if [p for p, _ in la] == [p for p, _ in lb]:
                close = True
                for (_, x), (_, y) in zip(la, lb):
                    if _is_real(x) and _is_real(y):
                        if not math.isclose(x, y, rel_tol=rel_tol, abs_tol=_EQ_ATOL):
                            close = False; break
                    elif x != y:
                        close = False; break
                if close:
                    out.append(Finding("NEAR_IDENTICAL_BRANCH_PAYLOAD", "error",
                                       f"every numeric value matches within rel_tol={rel_tol}", pair))
                    continue
            fa, fb = dict(_dist_fields(br[a])), dict(_dist_fields(br[b]))
            for dim, fields in DIMENSIONS.items():
                st_a = br[a]["dimension_status"][dim]["status"]
                paths = [p for p in fa if p in fb and _field_dim(p) == dim]
                dup = [p for p in paths if _same_distribution(fa[p], fb[p], rel_tol)]
                for p in dup:
                    out.append(Finding("DUPLICATED_FIELD", "warning", "identical distribution in both branches", f"{pair}:{p}"))
                if paths and len(dup) == len(paths) and st_a != "not_modeled":
                    out.append(Finding("DUPLICATED_DIMENSION", "error",
                                       f"every {dim} distribution is identical across the two branches", f"{pair}:{dim}"))
    return out


def _field_dim(path: str) -> str:
    parts = path.split(".")
    kind = "team" if parts[0] == "teams" else "player"
    field = "quarter_points" if "quarter_points" in parts else parts[2]
    for dim, fields in DIMENSIONS.items():
        if (kind, field) in fields:
            return dim
    return ""


# ------------------------------------------------------------------------------------------------ pooling detection
def _fav_margin_samples(payload: dict, branch: dict) -> Optional[np.ndarray]:
    g, d = payload["game"], payload["branch_definition"]
    teams = branch.get("teams") or {}
    fav, dog = teams.get(g["favorite"]), teams.get(g["underdog"])
    if fav is None or dog is None:
        return None
    var = d["classifier_variable"]
    try:
        if var == "final_margin_favorite":
            fs, ds = fav["points"]["samples"], dog["points"]["samples"]
            return np.asarray(fs, float) - np.asarray(ds, float) if len(fs) == len(ds) else None
        qs = QUARTERS if var == "regulation_margin_favorite" else QUARTERS[:3]
        f = sum(np.asarray(fav["quarter_points"][q]["samples"], float) for q in qs)
        a = sum(np.asarray(dog["quarter_points"][q]["samples"], float) for q in qs)
        return f - a
    except (TypeError, KeyError, ValueError):
        return None


def detect_branch_pooling(payload: dict, rel_tol: float = 1e-9) -> list[Finding]:
    """Find branches collapsed into one projection: identical means/distributions across all three branches, score
    samples that fall outside their branch's definition (pooled scores), and mis-ordered branch margins."""
    out: list[Finding] = []
    br = payload.get("branches") or {}
    if any(not isinstance(br.get(b), dict) for b in BRANCH_IDS):
        return out
    fields = [dict(_dist_fields(br[b])) for b in BRANCH_IDS]
    common = set(fields[0]) & set(fields[1]) & set(fields[2])
    for path in sorted(common):
        dists = [f[path] for f in fields]
        means = [dist_mean(d) for d in dists]
        if all(math.isclose(means[0], m, rel_tol=rel_tol, abs_tol=_EQ_ATOL) for m in means[1:]):
            same = all(_same_distribution(dists[0], d, rel_tol) for d in dists[1:])
            code = "BRANCH_DISTRIBUTIONS_IDENTICAL" if same else "BRANCH_MEANS_COLLAPSED"
            msg = ("all three branches carry the same distribution (pooled before branching)" if same else
                   f"all three branches share mean {means[0]:.6g} (collapsed to one projection)")
            out.append(Finding(code, "error", msg, path))
    # Score partition: every trial in a branch must satisfy that branch's definition.
    d = payload.get("branch_definition") or {}
    margin_means = {}
    for b in BRANCH_IDS:
        m = _fav_margin_samples(payload, br[b])
        if m is None or not len(m):
            continue
        margin_means[b] = float(m.mean())
        wrong = sum(classify_margin(x, d) != b for x in m)
        if wrong:
            out.append(Finding("SCORE_OUTSIDE_BRANCH", "error",
                               f"{wrong}/{len(m)} score trials violate the {b} definition "
                               f"({d.get('classifier_variable')}); scores look pooled or mislabeled", b))
    if len(margin_means) == 3 and not (margin_means["favorite_controls"] > margin_means["competitive"]
                                       > margin_means["underdog_chases"]):
        out.append(Finding("BRANCH_ORDER_VIOLATION", "error",
                           f"favorite-perspective mean margins not ordered A > B > C: {margin_means}"))
    # Visibility: behavioural dimensions that are only trial selections, not state-dependent behaviour.
    for b in BRANCH_IDS:
        for dim in BEHAVIOURAL_DIMENSIONS:
            if br[b]["dimension_status"][dim]["status"] == "derived":
                out.append(Finding("DERIVED_NOT_MODELED", "warning",
                                   f"{dim} is a trial selection from a game-state-blind engine, not branch behaviour",
                                   f"{b}:{dim}"))
    return out


# --------------------------------------------------------------------------------------------- full payload check
def _schema_findings(payload: dict) -> list[Finding]:
    try:
        import jsonschema
    except ImportError:  # pragma: no cover - requirements-test.txt pins jsonschema
        return [Finding("SCHEMA_UNCHECKED", "warning", "jsonschema not installed")]
    v = jsonschema.Draft202012Validator(load_json_schema())
    return [Finding("SCHEMA", "error", e.message[:300], "/".join(map(str, e.absolute_path)))
            for e in sorted(v.iter_errors(payload), key=lambda e: list(map(str, e.absolute_path)))]


def _dimension_findings(branch_id: str, branch: dict) -> list[Finding]:
    out = []
    for dim, fields in DIMENSIONS.items():
        status = branch["dimension_status"][dim]["status"]
        for kind, field in fields:
            holders = list((branch.get("teams") or {}).items()) if kind == "team" else \
                [(p["player_id"], p) for p in branch.get("players") or []]
            for name, h in holders:
                val = h.get(field)
                loc = f"{branch_id}:{'teams' if kind == 'team' else 'players'}.{name}.{field}"
                if status == "not_modeled" and val is not None:
                    out.append(Finding("FAKED_DIMENSION", "error",
                                       f"{dim} is not_modeled but carries a value (fill-in / copied value)", loc))
                elif status != "not_modeled" and val is None:
                    out.append(Finding("MISSING_DIMENSION_OUTPUT", "error", f"{dim} is {status} but value is null", loc))
    return out


def validate_payload(payload: dict, *, tol: float = TOLERANCE, rel_tol: float = 1e-9) -> list[Finding]:
    """Schema + allocation + semantic + pooling + duplication checks. Returns findings (errors and warnings)."""
    out = _schema_findings(payload)
    if out:
        return out + [f for f in validate_allocation(payload, tol=tol) if f.code not in {o.code for o in out}]
    out += validate_allocation(payload, tol=tol)
    g, d, br = payload["game"], payload["branch_definition"], payload["branches"]
    if g["favorite"] == g["underdog"] or {g["favorite"], g["underdog"]} != {g["home"], g["away"]}:
        out.append(Finding("FAVORITE_UNDERDOG_INVALID", "error", "favorite/underdog must be the two teams of the game"))
    if d["favorite_controls_min_margin"] <= 0:
        out.append(Finding("DEFINITION_FAVORITE_NOT_LEADING", "error", "favorite_controls_min_margin must be > 0"))
    if not d["underdog_chases_max_margin"] < d["favorite_controls_min_margin"]:
        out.append(Finding("DEFINITION_OVERLAP", "error", "underdog_chases_max_margin must be < favorite_controls_min_margin"))
    elif math.floor(d["favorite_controls_min_margin"] - 1e-9) <= d["underdog_chases_max_margin"]:
        out.append(Finding("DEFINITION_EMPTY_COMPETITIVE", "warning", "no integer margin falls in the competitive branch"))
    players = {}
    for b in BRANCH_IDS:
        branch = br[b]
        if set(branch["teams"]) != {g["home"], g["away"]}:
            out.append(Finding("TEAM_SET_MISMATCH", "error", f"teams {sorted(branch['teams'])} != game teams", b))
        players[b] = sorted(p["player_id"] for p in branch["players"])
        if len(set(players[b])) != len(players[b]):
            out.append(Finding("PLAYER_DUPLICATED", "error", "a player appears twice in one branch", b))
        out += _dimension_findings(b, branch)
        if payload["provenance"]["probability_basis"] == "trial_partition":
            for path, dist in _dist_fields(branch):
                if dist.get("samples") is not None and len(dist["samples"]) != branch["n_trials"]:
                    out.append(Finding("SAMPLE_COUNT_MISMATCH", "error",
                                       f"{len(dist['samples'])} samples but branch n_trials={branch['n_trials']} "
                                       "(samples not from this branch's trials)", f"{b}:{path}"))
    if not (players["favorite_controls"] == players["competitive"] == players["underdog_chases"]):
        out.append(Finding("PLAYER_SET_MISMATCH", "error",
                           "every branch must carry the same players (a player absent from a branch cannot be mixed)"))
    out += detect_branch_pooling(payload, rel_tol=rel_tol)
    out += detect_duplicate_branches(payload, rel_tol=rel_tol)
    return out


def assert_valid(payload: dict, **kw) -> list[Finding]:
    """Raise ContractError on any error finding; return the warnings."""
    f = validate_payload(payload, **kw)
    bad = errors(f)
    if bad:
        raise ContractError("; ".join(f"{x.code}@{x.location}" for x in bad[:20]))
    return f
