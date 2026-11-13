"""NFL-75 / NFL-43 rare special-teams plays (opt-in: cfg["semantics"]["rare_plays"] = "asof_league_v1").

Covers the three NFL-43 still_unsupported special-teams items in the possession engine:
  * kick-play fouls: penalty-flagged punts and field goals, and pre-snap (no-play) fouls in punt / field-goal formation;
  * blocked kicks: blocked punts, blocked field goals, blocked extra points (incl. defensive two-point returns);
  * onside kicks (decision by game state + recovery) and fake / aborted punt- and field-goal-formation snaps.

Method (no weights, nothing fitted to scores or lines). Every rate is a COUNT RATIO over nflverse play-by-play rows,
and every outcome is RESAMPLED from the real rows of that kind (empirical outcome bootstrap): the next scrimmage
possessor, its yardline relative to the original line of scrimmage, its down and distance, and any points scored on
the play. So enforcement (half distance, spot fouls, re-kicks, first downs) is whatever actually happened on those rows;
the engine does not hand-code kick-foul enforcement.

Sources (point in time):
  * current season: data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet, weeks < target only;
  * prior seasons (REG only), all before the target: data/historical/nflverse/pbp_2018.parquet, pbp_2020.parquet,
    pbp_2022.parquet, play_by_play_2024.parquet (data/historical/MANIFEST.md: nflverse release, pulled 2026-11-06 07:28-07:29 ET).
  * Onside kicks use only the dynamic-kickoff era (2024 and the current season): earlier kickoff rules differ.
  * 2019/2021/2023/2025 are not in the repo and are not used.

Classification of kick-formation decisions (mutually exclusive, in this order), per formation (punt / field_goal):
  presnap  = no_play row, penalty 1, desc "(Punt formation)" / "(Field Goal formation)", not a timeout, down 1-4,
             not a PAT / two-point try;
  fake     = pass / run row in that formation (desc), not a two-point try. Includes aborted snaps (botched holds /
             punter fumbles): nflverse does not separate intent, so the class is "fake or aborted";
  blocked  = punt_blocked 1 (punt) / field_goal_result "blocked" (FG);
  flagged  = punt_attempt / field_goal_attempt with penalty 1 (any status; declined fouls resample their real outcome);
  clean    = everything else (the engine's existing team-pool punt / FG mechanics).
Rate of each class = class rows / all formation rows (presnap + fake + blocked + flagged + clean).
Extra points: blocked rate = blocked / attempts; defensive two-point return rate = defensive_extra_point_conv among
blocked attempts. A rate with a zero denominator is UNKNOWN (that piece stays on the existing engine path and is
flagged), never zero.
Research only, not validated.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import hashlib
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
NFLVERSE = REPO_ROOT / "data/historical/nflverse"
CURRENT_PBP_PULLED_ET = "2026-11-12 11:16 AM ET"
PRIOR_SEASON_FILES = {
    2018: ("pbp_2018.parquet", "2026-11-06 07:29 ET"),
    2020: ("pbp_2020.parquet", "2026-11-06 07:29 ET"),
    2022: ("pbp_2022.parquet", "2026-11-06 07:29 ET"),
    2024: ("play_by_play_2024.parquet", "2026-11-06 07:28 ET"),
}
DYNAMIC_KICKOFF_FIRST_SEASON = 2024  # onside kicks: kickoff rules before 2024 differ (not pooled)
MODES = ("off", "asof_league_v1")
# Onside cells: kicking-team deficit and seconds left in the 4th quarter. Bucket edges are STRUCTURAL (not fitted).
ONSIDE_SEC_EDGES = (120, 300, 600)       # <=120, 121-300, 301-600, >600
ONSIDE_DEFICIT_EDGES = (8, 16)            # 1-8, 9-16, 17+
ONSIDE_MIN_CELL_N = 10                    # STRUCTURAL: coarsen a cell with < 10 kickoffs to its seconds bucket
_COLS = ["game_id", "play_id", "season", "week", "season_type", "game_half", "qtr", "game_seconds_remaining",
         "play_type", "desc", "posteam", "defteam", "down", "ydstogo", "yardline_100", "timeout", "penalty",
         "punt_attempt", "punt_blocked", "field_goal_attempt", "field_goal_result", "extra_point_attempt",
         "extra_point_result", "two_point_attempt", "kickoff_attempt", "own_kickoff_recovery", "return_touchdown",
         "defensive_extra_point_conv", "score_differential", "posteam_score", "posteam_score_post",
         "defteam_score", "defteam_score_post", "yards_gained", "interception", "fumble_lost", "sack",
         "complete_pass", "touchback", "punt_in_endzone"]
# Outcome pools are sampled from rows whose line of scrimmage is near the live one (|row - live| <= band), widening
# through these bands until at least BAND_MIN_N rows qualify, else the whole pool. STRUCTURAL (not fitted): it bounds
# the field-position error of translating an outcome by its LOS shift (touchbacks, half-distance, goal lines).
LOS_BANDS = (0, 1, 2, 5, 10, 20)
BAND_MIN_N = 5
# Fake / aborted-snap rows are kept as full play rows and run through the engine's normal snap mechanics
# (live down, distance, goal line, turnovers, defensive returns); these are the columns that path reads.
FAKE_ROW_COLS = ("play_type", "yards_gained", "interception", "fumble_lost", "sack", "complete_pass", "yardline_100",
                 "down", "ydstogo")
_SCRIM_NEXT = ("pass", "run", "punt", "field_goal", "qb_kneel", "qb_spike", "no_play")
PUNT_FORM, FG_FORM = "(punt formation)", "(field goal formation)"


def mode_from_cfg(cfg: dict) -> str:
    m = ((cfg or {}).get("semantics") or {}).get("rare_plays", "off")
    m = "off" if m in (None, False, "", "off") else m
    if m not in MODES:
        raise ValueError(f"unknown semantics.rare_plays {m!r}; expected one of {MODES}")
    return m


def _sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _read(path: Path) -> pd.DataFrame:
    import pyarrow.parquet as pq
    have = set(pq.ParquetFile(path).schema_arrow.names)
    d = pd.read_parquet(path, columns=[c for c in _COLS if c in have])
    for c in _COLS:
        if c not in d.columns:
            d[c] = np.nan
    if d["season_type"].notna().any():
        d = d[d["season_type"] == "REG"]
    return d


def _num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce").fillna(0)


def classify(d: pd.DataFrame) -> pd.DataFrame:
    """Adds _form ("punt" / "field_goal" / None) and _cls (presnap / fake / blocked / flagged / clean) columns."""
    d = d.copy()
    desc = d["desc"].fillna("").astype(str).str.lower()
    pt = d["play_type"].astype(object)
    two = _num(d["two_point_attempt"]) == 1
    has_down = d["down"].notna()
    in_punt, in_fg = desc.str.contains(PUNT_FORM, regex=False), desc.str.contains(FG_FORM, regex=False)
    presnap = (pt == "no_play") & (_num(d["penalty"]) == 1) & (_num(d["timeout"]) != 1) & has_down & ~two
    fake = pt.isin(["pass", "run"]) & has_down & ~two
    punt_row = _num(d["punt_attempt"]) == 1
    fg_row = _num(d["field_goal_attempt"]) == 1
    form = pd.Series(None, index=d.index, dtype=object)
    cls = pd.Series(None, index=d.index, dtype=object)
    form[punt_row] = "punt"; form[fg_row] = "field_goal"
    form[(presnap | fake) & in_punt] = "punt"; form[(presnap | fake) & in_fg & ~in_punt] = "field_goal"
    cls[form.notna() & presnap] = "presnap"
    cls[form.notna() & fake & cls.isna()] = "fake"
    blk = (punt_row & (_num(d["punt_blocked"]) == 1)) | (fg_row & (d["field_goal_result"] == "blocked"))
    cls[form.notna() & blk & cls.isna()] = "blocked"
    cls[form.notna() & (punt_row | fg_row) & (_num(d["penalty"]) == 1) & cls.isna()] = "flagged"
    cls[form.notna() & (punt_row | fg_row) & cls.isna()] = "clean"
    d["_form"], d["_cls"] = form, cls
    d["_onside"] = (_num(d["kickoff_attempt"]) == 1) & desc.str.contains("onside", regex=False)
    return d


def _outcomes(d: pd.DataFrame, idx: np.ndarray, *, kicker_is_posteam: bool) -> tuple[np.ndarray, int]:
    """Empirical outcome of each row in idx (positions in d, sorted by game_id/play_id).

    Row layout: [kick_pts, recv_pts, possessor (1 kicking team / 0 receiving team), shift, down, ydstogo, abs_yl,
    los_yl (the row's own yardline_100, kicking frame; NaN for kickoffs), row_down, row_ydstogo, anchored].
    anchored = 1 for touchback rows (touchback / punt_in_endzone): their next spot is fixed by the rules (the
    receiving 20 plus any enforcement from it), so the engine uses the absolute spot instead of translating it.
    shift = next yardline_100 in the possessor's frame minus the reference: the row's own yardline_100 (kicking team)
    or 100 - yardline_100 (receiving team). Rows with no next scrimmage row in the same game half are dropped (count
    returned). Points scored on the row come from the score columns (TD 6, FG 3, safety 2; the PAT is a later row)."""
    g, gh = d["game_id"].to_numpy(), d["game_half"].to_numpy()
    pos, pt = d["posteam"].to_numpy(), d["play_type"].to_numpy()
    yl, dn, tg = d["yardline_100"].to_numpy(float), d["down"].to_numpy(float), d["ydstogo"].to_numpy(float)
    ko, to = _num(d["kickoff_attempt"]).to_numpy(), _num(d["timeout"]).to_numpy()
    ps, psp = d["posteam_score"].to_numpy(float), d["posteam_score_post"].to_numpy(float)
    ds, dsp = d["defteam_score"].to_numpy(float), d["defteam_score_post"].to_numpy(float)
    dfn = d["defteam"].to_numpy()
    z = pd.Series(0, index=d.index)
    anc = ((_num(d.get("touchback", z)) == 1) | (_num(d.get("punt_in_endzone", z)) == 1)).to_numpy().astype(float)
    out, dropped = [], 0
    for i in idx:
        dp = 0.0 if np.isnan(psp[i]) or np.isnan(ps[i]) else psp[i] - ps[i]
        dd = 0.0 if np.isnan(dsp[i]) or np.isnan(ds[i]) else dsp[i] - ds[i]
        kick_pts, recv_pts = (dp, dd) if kicker_is_posteam else (dd, dp)
        kicker = pos[i] if kicker_is_posteam else dfn[i]
        ref_yl = yl[i] if not np.isnan(yl[i]) else np.nan
        own = [ref_yl if kicker_is_posteam else np.nan, dn[i], tg[i], anc[i] if kicker_is_posteam else 0.0]
        if kick_pts > 0 or recv_pts > 0:
            out.append([kick_pts, recv_pts, -1, 0, 0, 0, -1, *own]); continue
        j = i + 1
        while j < len(d) and g[j] == g[i] and gh[j] == gh[i]:
            if ko[j] == 1:
                j = len(d); break
            if pt[j] in _SCRIM_NEXT and to[j] != 1 and not np.isnan(dn[j]) and not np.isnan(yl[j]) and isinstance(pos[j], str):
                break
            j += 1
        if j >= len(d) or g[j] != g[i] or gh[j] != gh[i]:
            dropped += 1; continue
        mine = int(pos[j] == kicker)
        if np.isnan(ref_yl):
            ref = np.nan
        else:
            ref = ref_yl if mine else 100 - ref_yl
        shift = 0 if np.isnan(ref) else int(yl[j] - ref)
        out.append([0, 0, mine, shift, int(dn[j]), int(tg[j]), int(yl[j]), *own])
    return (np.asarray(out, dtype=float) if out else np.zeros((0, 11))), dropped


@dataclass
class RarePlayModel:
    mode: str
    formation: dict          # "punt"/"field_goal" -> {"p": {cls: rate or None}, "n": {...}, "pools": {cls: ndarray}}
    xp: dict                 # {"p_block": rate|None, "p_def2_given_block": rate|None, n...}
    onside: dict             # {"cells": {key: (n, n_onside)}, "pool": ndarray, "p_recover": ...}
    clean_punt_return_td_rate: Optional[float]
    clean_kick_return_td_rate: Optional[float]
    meta: dict = field(default_factory=dict)
    # Capped research use (simulate_games research_unaccepted): games this model may still simulate; None = no cap
    # (only once the NFL-43 gate accepts rare plays). simulate_one decrements it and refuses at zero.
    research_budget: Optional[int] = None

    # ---- kick-formation decision ---------------------------------------------------------------------------------
    def draw_formation_class(self, rng: np.random.Generator, kind: str) -> str:
        """One uniform draw: presnap / fake / blocked / flagged / clean. UNKNOWN classes are never drawn."""
        f = self.formation.get(kind) or {}
        u = rng.random()
        acc = 0.0
        for c in ("presnap", "fake", "blocked", "flagged"):
            p = (f.get("p") or {}).get(c)
            pool = (f.get("pools") or {}).get(c)
            if p is None or pool is None or not len(pool):
                continue
            acc += p
            if u < acc:
                return c
        return "clean"

    def draw_outcome(self, rng: np.random.Generator, kind: str, cls: str, live_yl: int):
        """Resample one outcome of this class from rows whose LOS is within a widening band of the live LOS.
        Returns (row, tag). Fakes return a pandas row (FAKE_ROW_COLS) for the engine's snap mechanics."""
        if cls == "fake":
            rows = self.formation[kind]["fake_rows"]
            los = rows["yardline_100"].to_numpy(float)
        else:
            rows = self.formation[kind]["pools"][cls]
            los = rows[:, 7]
        idx, tag = None, "all"
        for b in LOS_BANDS:
            m = np.flatnonzero(np.abs(los - float(live_yl)) <= b)
            if len(m) >= BAND_MIN_N:
                idx, tag = m, f"band{b}"
                break
        if idx is None:
            idx = np.arange(len(los))
        k = int(idx[int(rng.integers(0, len(idx)))])
        return (rows.iloc[k] if cls == "fake" else rows[k]), tag

    # ---- onside ----------------------------------------------------------------------------------------------------
    @staticmethod
    def onside_key(qtr: int, deficit: int, secs: int) -> tuple:
        if int(qtr) != 4 or deficit <= 0:
            return ("other",)
        sb = sum(int(secs) > e for e in ONSIDE_SEC_EDGES)
        db = sum(int(deficit) > e for e in ONSIDE_DEFICIT_EDGES)
        return ("q4_trailing", sb, db)

    def onside_rate(self, qtr: int, deficit: int, secs: int) -> tuple[Optional[float], str]:
        key = self.onside_key(qtr, deficit, secs)
        cells = self.onside["cells"]
        n, k = cells.get(key, (0, 0))
        tag = "cell"
        if key[0] == "q4_trailing" and n < ONSIDE_MIN_CELL_N:
            n = sum(v[0] for kk, v in cells.items() if kk[0] == "q4_trailing" and kk[1] == key[1])
            k = sum(v[1] for kk, v in cells.items() if kk[0] == "q4_trailing" and kk[1] == key[1])
            tag = "secs_bucket"
        if n <= 0:
            return None, "unknown"
        return k / n, tag


def build_rare_play_model(pbp_path, *, season: int, week_asof_exclusive: int,
                          prior_seasons: tuple = tuple(PRIOR_SEASON_FILES), mode: str = "asof_league_v1",
                          root: Path = NFLVERSE) -> RarePlayModel:
    if mode not in MODES or mode == "off":
        raise ValueError(f"build_rare_play_model needs mode asof_league_v1, got {mode!r}")
    cur_path = Path(pbp_path).resolve()
    cur = _read(cur_path)
    cur = cur[(cur["season"] == season) & (cur["week"] < int(week_asof_exclusive))]
    sources = [{"file": str(cur_path.relative_to(REPO_ROOT)) if cur_path.is_relative_to(REPO_ROOT) else str(cur_path),
                "sha256": _sha(cur_path), "pulled_et": CURRENT_PBP_PULLED_ET, "season": season,
                "weeks": sorted(int(w) for w in cur["week"].unique()), "rows": int(len(cur)), "games": int(cur["game_id"].nunique())}]
    frames = [cur]
    for s in prior_seasons:
        if int(s) >= int(season):
            raise ValueError(f"prior season {s} is not before {season}")
        fn, pulled = PRIOR_SEASON_FILES[int(s)]
        p = Path(root) / fn
        if not p.exists():
            sources.append({"file": fn, "season": int(s), "status": "MISSING (unknown, not used)"}); continue
        d = _read(p)
        frames.append(d)
        sources.append({"file": str(p.relative_to(REPO_ROOT)) if p.is_relative_to(REPO_ROOT) else str(p),
                        "sha256": _sha(p), "pulled_et": pulled, "season": int(s), "rows": int(len(d)),
                        "games": int(d["game_id"].nunique()), "season_type": "REG"})
    d = pd.concat(frames, ignore_index=True)
    d = d.sort_values(["season", "game_id", "play_id"]).reset_index(drop=True)
    d = classify(d)
    formation, fmeta = {}, {}
    for kind in ("punt", "field_goal"):
        sub = d[d["_form"] == kind]
        n_all = int(len(sub))
        p, n, pools, dropped, cur_only = {}, {}, {}, {}, {}
        for c in ("presnap", "fake", "blocked", "flagged", "clean"):
            m = sub["_cls"] == c
            n[c] = int(m.sum())
            p[c] = (n[c] / n_all) if n_all else None
            cn = int(((sub["season"] == season) & m).sum()); cd = int((sub["season"] == season).sum())
            cur_only[c] = {"n": cn, "of": cd, "rate": (cn / cd) if cd else None}
            if c == "fake":
                fr = sub[m & sub["yardline_100"].notna()][list(FAKE_ROW_COLS)].reset_index(drop=True)
                pools["fake_rows"], dropped[c] = fr, int(m.sum()) - len(fr)
                pools[c] = np.zeros((len(fr), 11))  # placeholder so draw_formation_class sees a non-empty pool
                if not len(fr):
                    p[c] = None
            elif c != "clean":
                arr, dr = _outcomes(d, np.flatnonzero((d["_form"] == kind).to_numpy() & (d["_cls"] == c).to_numpy()),
                                    kicker_is_posteam=True)
                pools[c], dropped[c] = arr, dr
                if not len(arr):
                    p[c] = None  # no usable outcome rows: UNKNOWN, never zero
        formation[kind] = {"p": p, "n": n, "pools": pools, "fake_rows": pools.pop("fake_rows")}
        fmeta[kind] = {"formation_rows": n_all, "n": n, "rate": p, "outcome_rows_dropped_no_next_play": dropped,
                       "current_season_only": cur_only,
                       "outcome_summary": {**{c: _summ(pools[c]) for c in pools if c != "fake"},
                                           "fake": _fake_summ(formation[kind]["fake_rows"])}}
    xp = d[_num(d["extra_point_attempt"]) == 1]
    nb = int((xp["extra_point_result"] == "blocked").sum())
    nd2 = int(((xp["extra_point_result"] == "blocked") & (_num(xp["defensive_extra_point_conv"]) == 1)).sum())
    xpm = {"attempts": int(len(xp)), "blocked": nb, "def_two_point_on_block": nd2,
           "p_block": (nb / len(xp)) if len(xp) else None, "p_def2_given_block": (nd2 / nb) if nb else None}
    # onside: dynamic-kickoff era only
    ko = d[(_num(d["kickoff_attempt"]) == 1) & (d["season"] >= DYNAMIC_KICKOFF_FIRST_SEASON)]
    cells: dict = {}
    for q, sd, gs, ons in zip(ko["qtr"], ko["score_differential"], ko["game_seconds_remaining"], ko["_onside"]):
        if pd.isna(q) or pd.isna(sd) or pd.isna(gs):
            continue
        # kickoff rows: posteam = receiving team, so score_differential = receiving lead = kicking-team deficit
        key = RarePlayModel.onside_key(int(q), int(sd), int(gs))
        a, b = cells.get(key, (0, 0))
        cells[key] = (a + 1, b + int(bool(ons)))
    ons_idx = np.flatnonzero(((_num(d["kickoff_attempt"]) == 1) & d["_onside"] &
                              (d["season"] >= DYNAMIC_KICKOFF_FIRST_SEASON)).to_numpy())
    opool, odrop = _outcomes(d, ons_idx, kicker_is_posteam=False)  # onside rows use absolute spots (ref_yl None)
    n_ons = int(len(ons_idx))
    rec = int(_num(d.loc[ons_idx, "own_kickoff_recovery"]).sum()) if n_ons else 0
    onside = {"cells": cells, "pool": opool, "n_onside": n_ons, "own_recoveries": rec, "dropped": odrop}
    # clean return-TD rates (blocked / flagged punts and onside kicks are resampled from their own pools)
    cp = d[(d["_form"] == "punt") & (d["_cls"] == "clean") & (d["season"] == season)]
    # same population the engine rolls the return TD on: punts that are not touchbacks
    cp = cp[(_num(cp["touchback"]) != 1) & (_num(cp["punt_in_endzone"]) != 1)]
    nko = cur[(_num(cur["kickoff_attempt"]) == 1)]
    nko = nko[~nko["desc"].fillna("").str.lower().str.contains("onside", regex=False)]
    cprt = float(_num(cp["return_touchdown"]).sum() / len(cp)) if len(cp) else None
    ckrt = float(_num(nko["return_touchdown"]).sum() / len(nko)) if len(nko) else None
    meta = {"mode": mode, "label": "AS_OF_LEAGUE_COUNT_RATIOS_NOT_FITTED research only, not validated",
            "sources": sources, "season": season, "week_asof_exclusive": int(week_asof_exclusive),
            "formation": fmeta, "extra_point": xpm,
            "onside": {"era": f"{DYNAMIC_KICKOFF_FIRST_SEASON}+ (dynamic kickoff), current season weeks < target",
                       "kickoffs": int(len(ko)), "onside": n_ons, "own_recoveries": rec,
                       "p_recover": (rec / n_ons) if n_ons else None, "dropped_no_next_play": odrop,
                       "cells": {"|".join(map(str, k)): {"kickoffs": v[0], "onside": v[1]} for k, v in sorted(cells.items(), key=str)},
                       "structural": {"sec_edges": ONSIDE_SEC_EDGES, "deficit_edges": ONSIDE_DEFICIT_EDGES,
                                      "min_cell_n": ONSIDE_MIN_CELL_N}},
            "clean_punt_return_td_rate": {"rate": cprt, "punts": int(len(cp)),
                                          "source": "current season weeks < target, clean non-touchback punts"},
            "clean_kick_return_td_rate": {"rate": ckrt, "kickoffs": int(len(nko)),
                                          "source": "current season weeks < target, non-onside kickoffs"},
            "kickoff_fouls": "already in the as-of kickoff start pool (next scrimmage spot after each kickoff); "
                             "onside kicks are removed from that pool and resampled from the onside pool",
            "unsupported": ["extra-point fouls carried to the ensuing kickoff / re-tries (PAT result pool only)",
                            "player yardage credit on fake punts / fake FGs (team outcome only)",
                            "two-point conversions (engine always kicks)",
                            "kick-foul enforcement is resampled, not rule-coded (no per-foul type model)"]}
    return RarePlayModel(mode=mode, formation=formation, xp=xpm, onside=onside,
                         clean_punt_return_td_rate=cprt, clean_kick_return_td_rate=ckrt, meta=meta)


def _fake_summ(fr: pd.DataFrame) -> dict:
    if not len(fr):
        return {"rows": 0}
    return {"rows": int(len(fr)), "pass": int((fr["play_type"] == "pass").sum()), "run": int((fr["play_type"] == "run").sum()),
            "turnovers": int(((_num(fr["interception"]) == 1) | (_num(fr["fumble_lost"]) == 1)).sum()),
            "mean_yards": float(_num(fr["yards_gained"]).mean()),
            "gained_line_to_gain": int((_num(fr["yards_gained"]) >= _num(fr["ydstogo"])).sum())}


def _summ(arr: np.ndarray) -> dict:
    if not len(arr):
        return {"rows": 0}
    scored = arr[:, 2] == -1
    return {"rows": int(len(arr)), "kicking_team_scored": int(((arr[:, 0] > 0) & scored).sum()),
            "receiving_team_scored": int(((arr[:, 1] > 0) & scored).sum()),
            "kicking_team_keeps_ball": int((arr[:, 2] == 1).sum()), "receiving_team_ball": int((arr[:, 2] == 0).sum())}
