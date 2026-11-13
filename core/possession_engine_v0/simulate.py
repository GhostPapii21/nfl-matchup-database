"""Possession/PBP Monte Carlo vertical slice — team-only empirical resampling."""
from __future__ import annotations
from pathlib import Path
from typing import Any, Optional
import hashlib
import numpy as np
import pandas as pd

from pbp_filter import load_team_history
from empirical import StateKey, lookup_plays, lookup_special, sample_play, dist_bucket, yl_bucket
from adjustments import apply_forward_qb_filter
from state import GameState, apply_kickoff, maybe_halftime, start_ot_if_tied, kickoff_spot


def stable_seed(base: int, week: int, game_id: str) -> int:
    digest = hashlib.sha256(f"{base}|{week}|{game_id}".encode()).hexdigest()
    return (base + week * 1000 + int(digest[:8], 16)) % (2**31 - 1)


def _clock_cost(play_type: str, rng: np.random.Generator, cost_map: dict | None = None) -> int:
    defaults = {"pass": 22, "run": 28, "punt": 10, "field_goal": 7, "extra_point": 4, "qb_kneel": 40, "qb_spike": 2}
    means = {**defaults, **(cost_map or {})}
    mu = float(means.get(play_type, 24))
    return int(max(3, rng.normal(mu, 4)))


def _credit_player(st: GameState, team: str, kind: str, name: Optional[str], yards: float) -> None:
    if not isinstance(name, str) or not name or name == "nan":
        return
    bucket = st.player_counts.setdefault(kind, {}).setdefault(team, {})
    bucket[name] = bucket.get(name, 0.0) + float(yards)


def _other(st: GameState, team: str) -> str:
    return st.away if team == st.home else st.home


class PlayCatalog:
    """Pre-index team snaps for fast sampling; optional defense conditioning + empirical clock."""

    def __init__(self, df: pd.DataFrame, min_n: int, games_df: Optional[pd.DataFrame] = None,
                 exclude_clock_mgmt: bool = False, rare_plays: bool = False):
        self.df = df
        self.min_n = min_n
        self.clock_df = games_df if games_df is not None and len(games_df) else df
        # NFL-75 rare plays (opt-in, rare_plays.py): kick-formation pass/run rows (fakes / aborted snaps) leave the
        # scrimmage pools and count as punt / FG decisions; blocked and penalty-flagged kicks leave the team kick pools;
        # onside kicks leave the kickoff start pool. Each is resampled from its own as-of league pool instead.
        # rare_plays=False builds exactly the pre-NFL-75 catalog.
        self.rare_plays = bool(rare_plays)
        snap_types = ["pass", "run"] if exclude_clock_mgmt else ["pass", "run", "qb_kneel", "qb_spike"]
        if self.rare_plays:
            df = _recode_kick_formation(df)
            if games_df is not None and len(games_df):
                games_df = _recode_kick_formation(games_df)
        self.snaps = df[df["play_type"].isin(snap_types)].copy()
        self.snaps["_db"] = self.snaps["ydstogo"].map(dist_bucket)
        self.snaps["_yl"] = self.snaps["yardline_100"].map(yl_bucket)
        self.cells: dict[tuple, pd.DataFrame] = {}
        self.by_down: dict[tuple, pd.DataFrame] = {}
        self.by_team: dict[str, pd.DataFrame] = {}
        self.by_team_vs_def: dict[tuple, pd.DataFrame] = {}
        self._defense_cond = False
        # NFL-49 A: head-to-head (this offense vs this defense) conditioning policy. "off" (default) = never;
        # "legacy_always" = pre-NFL-49 behaviour (every snap from the h2h pool whenever it has >= min_n rows);
        # "shrunk" = draw from the h2h pool with probability max_weight * n / (n + k), n = h2h rows for the down.
        # k and max_weight are STRUCTURAL ASSUMPTIONS (not fitted, not tuned to any market line).
        self.h2h_policy: dict = {"mode": "off"}
        self.clock_map: dict | None = None
        self.clock_meta: dict = {"source": "fixed_defaults"}
        self.goal_line_censoring = "redistribute_right"  # WP2; simulate_one sets it from cfg accounting
        self._last_pool, self._last_pool_foreign = None, False
        for team, g in self.snaps.groupby("posteam"):
            self.by_team[team] = g
            for down, gd in g.groupby("down"):
                self.by_down[(team, int(down))] = gd
                for (db, yl), cell in gd.groupby(["_db", "_yl"]):
                    self.cells[(team, int(down), str(db), str(yl))] = cell
            if "defteam" in g.columns:
                for deff, gd in g.groupby("defteam"):
                    self.by_team_vs_def[(team, str(deff))] = gd
        # Defense-allowed pools: OTHER offenses vs this defense (prior weeks only; caller enforces as-of).
        self._def_allowed_w = 0.0
        self.def_allowed_cells: dict[tuple, pd.DataFrame] = {}
        self.def_allowed_down: dict[tuple, pd.DataFrame] = {}
        if games_df is not None and len(games_df) and "defteam" in games_df.columns:
            ga = games_df[games_df["play_type"].isin(["pass", "run"]) & games_df["down"].notna()].copy()
            ga["_db"] = ga["ydstogo"].map(dist_bucket)
            for deff, g in ga.groupby("defteam"):
                g = g[g["posteam"] != deff]
                for down, gd in g.groupby("down"):
                    self.def_allowed_down[(str(deff), int(down))] = gd
                    for db, cell in gd.groupby("_db"):
                        self.def_allowed_cells[(str(deff), int(down), str(db))] = cell
        # Kickoff outcomes: receiving team's first scrimmage yardline_100 after each as-of kickoff
        # in games involving these teams (touchbacks at the 35 under the 2025 rule, returns, short kicks).
        self.kickoff_starts = kickoff_start_yardlines(games_df if games_df is not None else df,
                                                      exclude_onside=self.rare_plays)
        # State-conditioned 4th-down decisions (observed team rows only)
        self.fourth_cells: dict[tuple, pd.DataFrame] = {}
        f4 = df[(df["down"] == 4) & df["play_type"].isin(["punt", "field_goal", "pass", "run"])].copy()
        if len(f4):
            f4["_y4"] = f4["yardline_100"].map(yl4_bucket)
            f4["_t4"] = f4["ydstogo"].map(togo4_bucket)
            for team, g in f4.groupby("posteam"):
                self.fourth_cells[(team,)] = g
                for y, gy in g.groupby("_y4"):
                    self.fourth_cells[(team, y)] = gy
                    for tg, gt in gy.groupby("_t4"):
                        self.fourth_cells[(team, y, tg)] = gt
        self.fourth_probs = {}
        self.specials = {"punt": {}, "field_goal": {}, "extra_point": {}}
        for team, g in df.groupby("posteam"):
            fourth = g[g["down"] == 4]
            if len(fourth) >= 5:
                types = fourth["play_type"].value_counts(normalize=True)
                p_punt = float(types.get("punt", 0)); p_fg = float(types.get("field_goal", 0))
                p_go = float(types.get("pass", 0) + types.get("run", 0)); s = p_punt + p_fg + p_go
                self.fourth_probs[team] = (p_punt/s, p_fg/s, p_go/s) if s > 0 else (1.0, 0.0, 0.0)
            for kind, ptype in [("punt","punt"),("field_goal","field_goal"),("extra_point","extra_point")]:
                sub = g[g["play_type"] == ptype]
                if self.rare_plays:
                    sub = sub[_clean_kick_mask(sub, kind)]
                if len(sub) >= 3:
                    self.specials[kind][team] = sub.reset_index(drop=True)

    @staticmethod
    def build_empirical_clock(df: pd.DataFrame, stat: str = "legacy_median", *,
                              skip_unmodeled_rows: bool = False) -> dict:
        """Seconds consumed from a snap to the next row, by play_type, when timestamps exist.

        stat="legacy_median" (pre-NFL-49): median of deltas in [3, 55] s over the rows given (offense-only rows, so a
        "next row" can sit after the opponent's whole drive). stat="mean" (NFL-49 B): MEAN of deltas in [0, 60] s where
        the next row is in the same game AND quarter, over every row of the as-of games. Run/pass deltas are bimodal
        (clock stopped vs running), so the median overstated run 38 s vs mean 33.3 s on the W1-9 file; the means
        are what sum to the 3,600 s of regulation.

        WP1 pace fix (NFL-75, 2026-11-12), stat="mean" only:
        * "no_play_penalty": MEAN delta (same rule) of pre-snap/no-play PENALTY rows (play_type no_play, penalty 1).
          The engine charged a flat 4 s (semantics.NO_PLAY_CLOCK_SEC); the W1-9 as-of mean is about 11 s.
        * skip_unmodeled_rows=True: no_play rows that are NOT penalties (timeouts, plus ~20 odd rows on W1-9) are
          dropped BEFORE "next row" is taken, so the seconds nflverse books on them are charged to the modeled play
          before them. Otherwise that time (timeouts: about 12.8 s each, ~3.7 per team-game on W1-9) is lost and
          the simulated clock runs too fast. GAME / END QUARTER marker rows (no play_type) are kept so the last
          play of a quarter still closes on them. Same-quarter seconds are conserved before the [0, 60] s window
          (W1-9: 494,585 s vs 494,625 s); the window then drops merged intervals > 60 s, so the kept deltas cover
          about 0.1% less than the raw clock (W1-9: 494,045 of 494,625 s kept, vs 494,273 of 494,585 s without the
          drop). Not fitted to outcomes; pure clock bookkeeping.
        """
        out = {"pass": 22, "run": 28, "punt": 10, "field_goal": 7, "extra_point": 4, "qb_kneel": 40, "qb_spike": 2}
        meta_source = "fixed_defaults"
        if "game_seconds_remaining" in df.columns and "play_id" in df.columns:
            d = df.sort_values(["game_id", "play_id"]).copy()
            is_np = d["play_type"] == "no_play"
            if "penalty" in d.columns:
                pen_np = is_np & (pd.to_numeric(d["penalty"], errors="coerce").fillna(0) == 1)
            elif "timeout" in d.columns:
                pen_np = is_np & (pd.to_numeric(d["timeout"], errors="coerce").fillna(0) != 1)
            elif "desc" in d.columns:
                pen_np = is_np & ~d["desc"].astype(str).str.contains("timeout", case=False, regex=False)
            else:
                pen_np = is_np  # cannot tell timeouts apart: keep every no_play row as its own clock event
            if stat == "mean" and skip_unmodeled_rows:
                # drop only no_play rows that are not penalties (timeouts, ~20 odd rows). Rows with no play_type
                # (GAME / END QUARTER markers) stay: they close the last play's delta inside its quarter.
                keep = ~(is_np & ~pen_np)
                d, pen_np = d[keep].copy(), pen_np[keep]
                meta_skip = True
            else:
                meta_skip = False
            d["_next"] = d.groupby("game_id")["game_seconds_remaining"].shift(-1)
            d["_delta"] = d["game_seconds_remaining"] - d["_next"]
            if stat == "mean":
                same_q = (d.groupby("game_id")["qtr"].shift(-1) == d["qtr"]) if "qtr" in d.columns else True
                for pt in ("pass", "run", "punt", "field_goal", "qb_kneel", "kickoff"):
                    sub = d[(d["play_type"] == pt) & same_q & d["_delta"].between(0, 60)]
                    if len(sub) >= 30:
                        out[pt] = float(sub["_delta"].mean())
                        meta_source = "empirical_mean_delta_same_qtr"
                sub = d[pen_np & same_q & d["_delta"].between(0, 60)]
                if len(sub) >= 30:
                    out["no_play_penalty"] = float(sub["_delta"].mean())
                    out["no_play_penalty_n"] = int(len(sub))
                out["skip_unmodeled_rows"] = meta_skip
            else:
                # positive small deltas = clock ran
                for pt in ("pass", "run", "punt", "field_goal", "qb_kneel"):
                    sub = d[(d["play_type"] == pt) & d["_delta"].between(3, 55)]
                    if len(sub) >= 30:
                        out[pt] = float(sub["_delta"].median())
                        meta_source = "empirical_median_delta"
        out["source"] = meta_source
        return out

    def set_empirical_clock(self, cost_map: dict) -> None:
        self.clock_map = {k: v for k, v in cost_map.items() if k not in ("source", "no_play_penalty_n", "skip_unmodeled_rows")}
        self.clock_meta = {"source": cost_map.get("source", "custom"),
                           "no_play_penalty_n": cost_map.get("no_play_penalty_n"),
                           "skip_unmodeled_rows": cost_map.get("skip_unmodeled_rows", False)}

    def enable_defense_conditioning(self, enabled: bool = True) -> None:
        """Legacy switch: True == h2h_policy legacy_always, False == off."""
        self._defense_cond = bool(enabled)
        self.h2h_policy = {"mode": "legacy_always"} if enabled else {"mode": "off"}

    def set_h2h_policy(self, policy: Optional[dict]) -> dict:
        pol = dict(policy or {"mode": "off"})
        mode = pol.get("mode", "off")
        if mode not in H2H_MODES:
            raise ValueError(f"unknown h2h mode {mode!r}; expected one of {H2H_MODES}")
        if mode == "shrunk":
            pol["k"] = float(pol.get("k", H2H_SHRUNK_DEFAULTS["k"]))
            pol["max_weight"] = float(np.clip(pol.get("max_weight", H2H_SHRUNK_DEFAULTS["max_weight"]), 0.0, 1.0))
            if pol["k"] <= 0:
                raise ValueError("h2h shrunk k must be > 0")
        self.h2h_policy = pol
        self._defense_cond = mode != "off"
        return pol

    def h2h_weight(self, n: int) -> float:
        """Probability that a snap is drawn from an h2h pool of n rows (n >= min_n), under the current policy."""
        mode = self.h2h_policy.get("mode", "off")
        if mode == "off" or n < self.min_n:
            return 0.0
        if mode == "legacy_always":
            return 1.0
        return float(self.h2h_policy["max_weight"]) * n / (n + float(self.h2h_policy["k"]))

    def enable_defense_allowed(self, weight: float) -> None:
        """Mixture weight is a STRUCTURAL ASSUMPTION (not fitted)."""
        self._def_allowed_w = float(np.clip(weight, 0.0, 1.0))

    def sample_snap(self, rng: np.random.Generator, st: GameState, allow_pool: bool) -> tuple[Optional[pd.Series], str]:
        if self._def_allowed_w > 0 and st.possession is not None:
            defense = st.home if st.possession == st.away else st.away
            pool = self.def_allowed_cells.get((defense, int(st.down), dist_bucket(st.ydstogo)))
            tagx = "CELL"
            if pool is None or len(pool) < self.min_n:
                pool = self.def_allowed_down.get((defense, int(st.down))); tagx = "DOWN"
            if pool is not None and len(pool) >= self.min_n and rng.random() < self._def_allowed_w:
                r = pool.iloc[int(rng.integers(0, len(pool)))].copy()
                for c in ("passer_player_name", "rusher_player_name", "receiver_player_name"):
                    if c in r.index:
                        r[c] = None  # foreign offense players: outcome only, no player credit
                self._last_pool, self._last_pool_foreign = pool, True
                return r, f"DEF_ALLOWED_{tagx}_vs_{defense}_n={len(pool)}"

        # Defense-conditioned pool when enabled and enough n vs current defense
        if self._defense_cond and st.possession is not None:
            defense = st.home if st.possession == st.away else st.away
            key = (st.possession, defense)
            pool = self.by_team_vs_def.get(key)
            if pool is not None and len(pool) >= self.min_n:
                # further filter by down if possible (memoised: identical rows/order, perf only)
                ck = (key, int(st.down))
                cache = self.__dict__.setdefault("_def_down_cache", {})
                use = cache.get(ck)
                if use is None:
                    sub = pool[pool["down"] == int(st.down)] if "down" in pool.columns else pool
                    use = sub if len(sub) >= self.min_n else pool
                    cache[ck] = use
                w = self.h2h_weight(len(use))
                if w >= 1.0 or (w > 0.0 and rng.random() < w):
                    self._last_pool, self._last_pool_foreign = use, False
                    return use.iloc[int(rng.integers(0, len(use)))], f"DEF_COND_vs_{defense}_n={len(use)}"
        key = (st.possession, int(st.down), dist_bucket(st.ydstogo), yl_bucket(st.yardline_100))
        cell = self.cells.get(key)
        if cell is not None and len(cell) >= self.min_n:
            self._last_pool, self._last_pool_foreign = cell, False
            return cell.iloc[int(rng.integers(0, len(cell)))], "OK"
        down_key = (st.possession, int(st.down))
        broad = self.by_down.get(down_key)
        if broad is not None and len(broad) > 0:
            self._last_pool, self._last_pool_foreign = broad, False
            return broad.iloc[int(rng.integers(0, len(broad)))], f"COARSE_SAME_DOWN_n_cell={0 if cell is None else len(cell)}"
        team = self.by_team.get(st.possession)
        if team is not None and len(team) > 0:
            self._last_pool, self._last_pool_foreign = team, False
            return team.iloc[int(rng.integers(0, len(team)))], "COARSE_ANY_DOWN_SAME_TEAM"
        self._last_pool, self._last_pool_foreign = None, False
        return None, "EMPTY_TEAM_SNAPS"



def _recode_kick_formation(df: pd.DataFrame) -> pd.DataFrame:
    """NFL-75 rare plays: pass/run rows run from punt / field-goal formation (fakes and aborted snaps, per desc) are
    recoded to play_type "punt" / "field_goal" so the 4th-down decision counts them as kick decisions, and they leave
    every pass/run pool. They are not used as kick rows (they have no kick_distance / field_goal_result and are
    dropped from the team kick pools by _clean_kick_mask). The league fake rate and outcome pool live in rare_plays."""
    if "desc" not in df.columns or not len(df):
        return df
    desc = df["desc"].fillna("").astype(str).str.lower()
    run_pass = df["play_type"].isin(["pass", "run"]) & df["down"].notna()  # two-point tries have no down
    punt_f = run_pass & desc.str.contains("(punt formation)", regex=False)
    fg_f = run_pass & desc.str.contains("(field goal formation)", regex=False) & ~punt_f
    if not (punt_f.any() or fg_f.any()):
        return df
    out = df.copy()
    out.loc[punt_f, "play_type"] = "punt"
    out.loc[fg_f, "play_type"] = "field_goal"
    out["_kick_formation_snap"] = punt_f | fg_f
    return out


def _clean_kick_mask(sub: pd.DataFrame, kind: str) -> pd.Series:
    """Team kick rows the existing punt / FG / PAT mechanics keep under rare plays: not blocked, not penalty-flagged
    (punt / FG), not a recoded formation snap."""
    m = pd.Series(True, index=sub.index)
    if "_kick_formation_snap" in sub.columns:
        m &= ~sub["_kick_formation_snap"].fillna(False).astype(bool)
    if kind == "punt":
        if "punt_blocked" in sub.columns:
            m &= pd.to_numeric(sub["punt_blocked"], errors="coerce").fillna(0) != 1
        if "desc" in sub.columns:  # the team history (pbp_filter.COLS) has no punt_blocked column: use desc
            m &= ~sub["desc"].fillna("").astype(str).str.contains("punt is BLOCKED", case=False, regex=False)
    elif kind == "field_goal" and "field_goal_result" in sub.columns:
        m &= sub["field_goal_result"] != "blocked"
    elif kind == "extra_point" and "extra_point_result" in sub.columns:
        m &= sub["extra_point_result"] != "blocked"
    if kind in ("punt", "field_goal") and "penalty" in sub.columns:
        m &= pd.to_numeric(sub["penalty"], errors="coerce").fillna(0) != 1
    return m


ACCOUNTING_DEFAULTS = {"clock": "mean", "exclude_clock_mgmt_snaps": True, "kickoff_clock": True,
                       "no_play_clock": "asof_mean", "unmodeled_row_clock": "attribute_to_prior_play",
                       "goal_line_censoring": "redistribute_right"}
ACCOUNTING_LEGACY = {"clock": "legacy_median", "exclude_clock_mgmt_snaps": False, "kickoff_clock": False,
                     "no_play_clock": "flat_4s", "unmodeled_row_clock": "drop", "goal_line_censoring": "truncate"}
# Pre-WP1/WP2 engine (NFL-49 B accounting, 2026-11-12 main 9beb9b0): use accounting=PRE_WP12 to reproduce it.
ACCOUNTING_PRE_WP12 = {"clock": "mean", "exclude_clock_mgmt_snaps": True, "kickoff_clock": True,
                       "no_play_clock": "flat_4s", "unmodeled_row_clock": "drop", "goal_line_censoring": "truncate"}


def accounting_from_cfg(cfg: dict) -> dict:
    """NFL-49 B accounting fixes (cfg["accounting"]; "legacy" reproduces the pre-NFL-49 engine).
    clock: "mean" | "legacy_median" (see PlayCatalog.build_empirical_clock).
    exclude_clock_mgmt_snaps: kneels/spikes are end-of-half clock decisions, not play outcomes; the legacy pool let a
    random 1st-and-10 snap be a kneel (-1 yd, ~30 s) at any time.
    kickoff_clock: charge the as-of mean kickoff clock (needs clock "mean"); legacy kickoffs took 0 s.
    no_play_clock (WP1): "asof_mean" charges the as-of mean clock of no-play penalty rows (needs clock "mean" and
    >= 30 rows, else the flat 4 s); "flat_4s" = pre-WP1.
    unmodeled_row_clock (WP1): "attribute_to_prior_play" books timeout / unmodeled-row seconds on the prior modeled
    play when the mean clock is built (needs clock "mean"); "drop" = pre-WP1.
    goal_line_censoring (WP2): "redistribute_right" resolves sampled rows whose gain was cut off by THEIR goal line
    when the ball is now further out (see _resolve_goal_line_censoring); "truncate" = pre-WP2."""
    a = cfg.get("accounting")
    if a == "legacy":
        return dict(ACCOUNTING_LEGACY)
    if a == "pre_wp12":
        return dict(ACCOUNTING_PRE_WP12)
    out = dict(ACCOUNTING_DEFAULTS)
    out.update(a or {})
    if out["clock"] not in ("mean", "legacy_median"):
        raise ValueError(f"unknown accounting.clock {out['clock']!r}")
    if out["kickoff_clock"] and out["clock"] != "mean":
        out["kickoff_clock"] = False  # legacy clock map has no kickoff entry
    if out["no_play_clock"] not in ("asof_mean", "flat_4s"):
        raise ValueError(f"unknown accounting.no_play_clock {out['no_play_clock']!r}")
    if out["unmodeled_row_clock"] not in ("attribute_to_prior_play", "drop"):
        raise ValueError(f"unknown accounting.unmodeled_row_clock {out['unmodeled_row_clock']!r}")
    if out["goal_line_censoring"] not in ("redistribute_right", "truncate"):
        raise ValueError(f"unknown accounting.goal_line_censoring {out['goal_line_censoring']!r}")
    if out["clock"] != "mean":
        out["no_play_clock"], out["unmodeled_row_clock"] = "flat_4s", "drop"  # legacy median map has neither
    return out


H2H_MODES = ("off", "shrunk", "legacy_always")
H2H_SHRUNK_DEFAULTS = {"k": 200.0, "max_weight": 0.25}  # STRUCTURAL ASSUMPTION, not fitted (NFL-49 A)


def h2h_policy_from_cfg(cfg: dict) -> dict:
    """cfg["defense_interaction"]["h2h"] -> policy. Absent = "off" (NFL-49 A: the old always-on default drew 100%
    of WAS@NYG snaps from the single W5 game). Configs that need the old behaviour must say legacy_always."""
    di = cfg.get("defense_interaction") or {}
    h = di.get("h2h")
    if h is None:
        return {"mode": "off"}
    if isinstance(h, str):
        return {"mode": h}
    return dict(h)


MAX_FG_KICK = 66  # physical guard (longest observed NFL makes ~66-67); not a fitted parameter


def _fourth_down_decision(rng: np.random.Generator, catalog: PlayCatalog, st: GameState) -> str:
    """Condition on observed team 4th-down rows by field-position x distance bucket, explicit coarsening."""
    cells = getattr(catalog, "fourth_cells", {}) or {}
    team, y, tg = st.possession, yl4_bucket(st.yardline_100), togo4_bucket(st.ydstogo)
    chain = [((team, y, tg), None), ((team, y), "COARSE_4TH_YL_ONLY"), ((team,), "COARSE_4TH_TEAM_WIDE")]
    sub, flag = None, None
    for key, fl in chain:
        c = cells.get(key)
        if c is not None and len(c) >= catalog.min_n:
            sub, flag = c, fl
            break
    if sub is None:
        d = "punt" if st.yardline_100 > 40 else "go"
        st.sparse_flags.append(f"SPARSE_4TH_DECISION default_{d}")
        return d
    if flag:
        st.sparse_flags.append(f"{flag}_n={len(sub)}")
    vc = sub["play_type"].value_counts()
    p = np.array([vc.get("punt", 0), vc.get("field_goal", 0), vc.get("pass", 0) + vc.get("run", 0)], dtype=float)
    if st.yardline_100 + 18 > MAX_FG_KICK:
        p[1] = 0.0
    if p.sum() <= 0:
        st.sparse_flags.append("SPARSE_4TH_MASKED")
        return "punt" if st.yardline_100 > 40 else ("field_goal" if st.yardline_100 + 18 <= MAX_FG_KICK else "go")
    return str(rng.choice(["punt", "field_goal", "go"], p=p / p.sum()))


def _missed_fg_recv_yl(yl: int) -> int:
    """NFL: ball to defense at spot of kick (LOS+7), or its 20 if spot inside the 20."""
    return int(min(80, 100 - (yl + 7)))


def _attempt_fg(rng: np.random.Generator, catalog: PlayCatalog, st: GameState) -> None:
    plays = catalog.specials["field_goal"].get(st.possession)
    st.game_seconds_remaining -= _clock_cost("field_goal", rng, getattr(catalog, "clock_map", None))
    if plays is None or len(plays) == 0:
        st.sparse_flags.append("SPARSE_FG")
        st.possession = _other(st, st.possession)
        st.yardline_100 = _missed_fg_recv_yl(st.yardline_100)
        st.down, st.ydstogo = 1, 10
        st.events.append({"type": "fg_sparse_miss_default"})
        return
    dist = st.yardline_100 + 18
    pool = plays
    if "kick_distance" in plays.columns and plays["kick_distance"].notna().any():
        kd = pd.to_numeric(plays["kick_distance"], errors="coerce")
        near = plays[(kd - dist).abs() <= 5]
        if len(near) >= catalog.min_n:
            pool = near
        else:
            wide = plays[(kd - dist).abs() <= 10]
            if len(wide) >= catalog.min_n:
                pool = wide; st.sparse_flags.append(f"COARSE_FG_DIST10_n={len(wide)}")
            else:
                st.sparse_flags.append(f"COARSE_FG_TEAM_ALL_n={len(plays)}")
    else:
        st.sparse_flags.append("COARSE_FG_NO_KICK_DISTANCE")
    row = pool.iloc[int(rng.integers(0, len(pool)))]
    res = str(row.get("field_goal_result") or "")
    if res == "made":
        st.add_score(st.possession, 3)
        st.events.append({"type": "field_goal", "result": "made", "team": st.possession})
        apply_kickoff(st, receiving=_other(st, st.possession), yardline_100=kickoff_spot(st))
        if st.in_ot and st.ot_tracker is None:
            st.final = True
    else:
        st.events.append({"type": "field_goal", "result": res or "missed", "team": st.possession, "dist": dist})
        st.possession = _other(st, st.possession)
        st.yardline_100 = _missed_fg_recv_yl(st.yardline_100)
        st.down, st.ydstogo = 1, 10


def _rare_model(catalog):
    sem = getattr(catalog, "semantics", None)
    return sem.get("rare_plays") if isinstance(sem, dict) else None


def _attempt_pat(rng: np.random.Generator, catalog: PlayCatalog, st: GameState, scoring_team: str) -> None:
    plays = catalog.specials["extra_point"].get(scoring_team)
    # PAT is a dead-ball interval — do NOT consume game clock
    rp = _rare_model(catalog)
    if rp is not None and rp.xp.get("p_block") is not None:
        # NFL-75: as-of league blocked-PAT rate; blocked rows are out of the team PAT pool (rare plays catalog).
        if rng.random() < rp.xp["p_block"]:
            defense = _other(st, scoring_team)
            ev = {"type": "pat", "result": "blocked", "team": scoring_team, "rare_play": True}
            p2 = rp.xp.get("p_def2_given_block")
            if p2 is not None and p2 > 0 and rng.random() < p2:
                st.add_score(defense, 2)
                ev["def_two_point"] = defense
            st.events.append(ev)
            return
    if plays is None or len(plays) == 0:
        st.sparse_flags.append("SPARSE_PAT assume_made")
        st.add_score(scoring_team, 1)
        st.events.append({"type": "pat", "result": "assume_made_sparse", "team": scoring_team})
        return
    row = plays.iloc[int(rng.integers(0, len(plays)))]
    res = str(row.get("extra_point_result") or "")
    if res == "good":
        st.add_score(scoring_team, 1)
    st.events.append({"type": "pat", "result": res or "unknown", "team": scoring_team})


def _flag_true(row: pd.Series, col: str) -> bool:
    if col not in row.index or pd.isna(row.get(col)):
        return False
    try:
        return int(float(row.get(col))) == 1
    except (TypeError, ValueError):
        return False


def _punt_net_from_row(row: pd.Series) -> tuple[int, bool] | None:
    """Return (net_yards, is_touchback). yards_gained is always 0 on punts in nflfastR."""
    if "kick_distance" in row.index and pd.notna(row.get("kick_distance")):
        kick = float(row["kick_distance"])
        ret = float(row["return_yards"]) if "return_yards" in row.index and pd.notna(row.get("return_yards")) else 0.0
        is_tb = _flag_true(row, "touchback") or _flag_true(row, "punt_in_endzone")
        if is_tb:
            # Touchback: receiving team at own 20 → yardline_100=80; net implied later from kick yl.
            return 0, True
        net = int(round(kick - ret))
        return int(np.clip(net, 15, 70)), False
    return None


def _punt_fixed(rng: np.random.Generator, catalog: PlayCatalog, st: GameState) -> None:
    offense = st.possession
    yl = st.yardline_100
    plays = catalog.specials["punt"].get(offense)
    st.game_seconds_remaining -= _clock_cost("punt", rng, getattr(catalog, "clock_map", None))
    net = 40
    is_tb = False
    if plays is not None and len(plays):
        row = plays.iloc[int(rng.integers(0, len(plays)))]
        computed = _punt_net_from_row(row)
        if computed is not None:
            net, is_tb = computed
        else:
            # legacy fallback: yards_gained is useless (always 0) — keep default 40, flag
            st.sparse_flags.append("SPARSE_PUNT_NO_KICK_DISTANCE default_net40")
            net = 40
    else:
        st.sparse_flags.append("SPARSE_PUNT default_net40")
    st.possession = _other(st, offense)
    if is_tb:
        # Touchback → receiving team at own 20 (yardline_100=80)
        recv_yl = 80
        ball_yl_from_kick_opp = 20
        net = int(max(1, yl - 20))  # implied net to own-20 spot
    else:
        # Ball advances net yards toward offense's EZ; receiving team's yardline_100 flips.
        ball_yl_from_kick_opp = yl - net
        if ball_yl_from_kick_opp <= 0:
            ball_yl_from_kick_opp, recv_yl = 20, 80  # into end zone -> touchback
            is_tb, net = True, int(max(1, yl - 20))
        else:
            recv_yl = int(np.clip(100 - ball_yl_from_kick_opp, 1, 99))
    st.yardline_100 = recv_yl
    st.down, st.ydstogo = 1, 10
    st.events.append({
        "type": "punt", "from_yl": yl, "net": net, "new_yl": recv_yl,
        "kick_ball_yl": ball_yl_from_kick_opp, "team": offense, "touchback": bool(is_tb),
    })
    sem = getattr(catalog, "semantics", None)
    if sem is not None and sem.get("returns") is not None and not is_tb:
        # NFL-43: punt net stays the field-position quantity above; a return TD is a separate
        # as-of league-rate event and never adds return yards on top of the net.
        rp = sem.get("rare_plays")
        rate = sem["returns"].punt_return_td_rate
        if rp is not None and rp.clean_punt_return_td_rate is not None:
            rate = rp.clean_punt_return_td_rate  # NFL-75: blocked / flagged punts carry their own return TDs
        if rng.random() < rate:
            recv = st.possession
            st.events.append({"type": "punt_return_td", "team": recv, "from_yl": recv_yl})
            st.special_scores["punt_return_td"][recv] = st.special_scores["punt_return_td"].get(recv, 0) + 1
            st.add_score(recv, 6)
            _attempt_pat(rng, catalog, st, recv)
            apply_kickoff(st, receiving=_other(st, recv), yardline_100=kickoff_spot(st))


def _gl_censored_at(row) -> Optional[int]:
    """yardline_100 at which this historical row's gain was cut off by the goal line (an offensive pass/run that
    reached the end zone, so yards_gained >= its own yardline_100 and no turnover/sack), else None."""
    try:
        pt = row.get("play_type")
        if pt not in ("pass", "run"):
            return None
        y0, g = row.get("yardline_100"), row.get("yards_gained")
        if y0 is None or g is None or pd.isna(y0) or pd.isna(g):
            return None
        for c in ("interception", "fumble_lost", "sack"):
            v = row.get(c)
            if v is not None and not pd.isna(v) and int(v) == 1:
                return None
        return int(y0) if float(g) >= float(y0) else None
    except (TypeError, ValueError):
        return None


def _resolve_goal_line_censoring(rng: np.random.Generator, catalog, st: GameState, row):
    """WP2 (NFL-75): goal-line censoring in resampled gains.

    A sampled historical row from yardline y0 that scored (gain >= y0) only tells us the play would have gained AT
    LEAST y0 yards: the goal line cut it off. When the simulated ball is further out (y > y0) the old engine used
    the gain y0 as an ordinary gain, so e.g. a 2-yard TD plunge drawn at the 15 became a 2-yard run. On W1-9 PBP
    19.9% of red-zone pass/run rows are censored like this, which drags red-zone TD rates down.

    Fix (Efron's redistribute-to-the-right estimator for right-censored data; no tuned parameters, nothing fitted
    to outcomes; the same-pool-then-team-pool fallback order is a structural choice): the
    censored draw is replaced by a uniform draw from the rows of the SAME pool and play type that are known to have
    gained at least y0 (historical yardline_100 > y0 and gain >= y0, no turnover/sack). If that row is itself
    censored at y0' < y the step repeats (y0 strictly increases, so it terminates). If the same pool has no such row,
    the offense's whole same-play-type pool is used; if that is empty too the original row is kept and the snap is
    flagged GL_CENSOR_UNRESOLVED (old behaviour, visible; the ORIGINAL draw is returned even if a replacement
    chain had started). Ties (gain == y0) count as "gained at least y0". Rows whose y0 >= y are informative as they are and are
    never touched. Returns (row, tag) with tag None (not censored relative to y), "GL_CENSOR_RESOLVED" or
    "GL_CENSOR_UNRESOLVED"."""
    y = int(st.yardline_100)
    y0 = _gl_censored_at(row)
    if y0 is None or y0 >= y:
        return row, None
    pool = getattr(catalog, "_last_pool", None)
    foreign = bool(getattr(catalog, "_last_pool_foreign", False))
    fallback = None
    by_team = getattr(catalog, "by_team", None)
    if by_team is None and hasattr(catalog, "base"):
        by_team = getattr(catalog.base, "by_team", None)
    if isinstance(by_team, dict) and st.possession is not None:
        fallback = by_team.get(st.possession)
    pt = row.get("play_type")
    orig = row
    while True:  # y0 is an integer that strictly increases and stays < y, so this ends in < y steps
        cand = None
        for src, is_foreign in ((pool, foreign), (fallback, False)):
            if src is None or not len(src) or "yardline_100" not in src.columns:
                continue
            m = (src["play_type"] == pt) & (src["yardline_100"] > y0) & (src["yards_gained"] >= y0)
            for c in ("interception", "fumble_lost", "sack"):
                if c in src.columns:
                    m &= src[c].fillna(0) != 1
            c_ = src[m]
            if len(c_):
                cand, foreign_now = c_, is_foreign
                break
        if cand is None:
            return orig, "GL_CENSOR_UNRESOLVED"
        row = cand.iloc[int(rng.integers(0, len(cand)))]
        if foreign_now:
            row = row.copy()
            for c in ("passer_player_name", "rusher_player_name", "receiver_player_name"):
                if c in row.index:
                    row[c] = None
        y0n = _gl_censored_at(row)
        if y0n is None or y0n >= y:
            return row, "GL_CENSOR_RESOLVED"
        if y0n <= y0:  # cannot happen (candidates have yardline_100 > y0); guard keeps termination unconditional
            return orig, "GL_CENSOR_UNRESOLVED"
        y0 = y0n


def _apply_snap(rng: np.random.Generator, catalog: PlayCatalog, st: GameState, allow_pool: bool) -> None:
    row, status = catalog.sample_snap(rng, st, allow_pool)
    for part in str(status).split("|"):
        if part and part != "OK":
            st.sparse_flags.append(part)
    if row is None:
        _punt_fixed(rng, catalog, st)
        return

    gl_tag = None
    if getattr(catalog, "goal_line_censoring", "redistribute_right") == "redistribute_right":
        row, gl_tag = _resolve_goal_line_censoring(rng, catalog, st, row)
    else:
        y0 = _gl_censored_at(row)
        if y0 is not None and y0 < int(st.yardline_100):
            gl_tag = "GL_CENSOR_TRUNCATED"  # pre-WP2 behaviour, tagged only (no flag, no change)
    _apply_row(rng, catalog, st, row, gl_tag)


def _apply_row(rng: np.random.Generator, catalog, st: GameState, row, gl_tag: Optional[str] = None,
               extra_ev: Optional[dict] = None) -> None:
    """Apply one pass/run row at the LIVE state (clock, goal line, first down, turnovers, safeties, TDs).
    Split out of _apply_snap unchanged (same operations, same RNG order) so NFL-75 fake / aborted kick-formation
    rows use the same mechanics."""
    play_type = str(row["play_type"])
    yards = float(row["yards_gained"]) if pd.notna(row["yards_gained"]) else 0.0
    st.game_seconds_remaining -= _clock_cost(play_type, rng, getattr(catalog, "clock_map", None))
    hist_yards = yards
    yards = float(min(yards, st.yardline_100)) if yards > 0 else float(max(yards, -(100 - st.yardline_100)))
    # Always count the offensive play as a snap for pace/accounting (before early exits); realized yards.
    ev = {"type": "snap", "play_type": play_type, "yards": yards, "hist_yards": hist_yards, "down": st.down}
    if extra_ev:
        ev.update(extra_ev)
    if gl_tag is not None:
        ev["goal_line_censoring"] = gl_tag
        if gl_tag == "GL_CENSOR_UNRESOLVED":
            st.sparse_flags.append(gl_tag)
    st.events.append(ev)

    def _i(c):
        v = row.get(c)
        return 0 if v is None or pd.isna(v) else int(v)
    if play_type == "pass":
        if _i("complete_pass") == 1 and _i("sack") == 0:
            _credit_player(st, st.possession, "pass_yards", row.get("passer_player_name"), yards)
            _credit_player(st, st.possession, "rec_yards", row.get("receiver_player_name"), yards)
    elif play_type == "run":
        _credit_player(st, st.possession, "rush_yards", row.get("rusher_player_name"), yards)

    if _i("interception") == 1 or _i("fumble_lost") == 1:
        st.events.append({"type": "turnover", "play_type": play_type, "team": st.possession})
        st.possession = _other(st, st.possession)
        spot = st.yardline_100 - yards
        sem = getattr(catalog, "semantics", None)
        if sem is not None and sem.get("returns") is not None:
            kind = "interception" if _i("interception") == 1 else "fumble_lost"
            _defensive_return(rng, catalog, st, spot, kind)
            return
        # Turnover in opp end zone -> touchback (return yardage not modeled; declared limitation)
        st.yardline_100 = 80 if spot <= 0 else int(np.clip(100 - spot, 1, 99))
        st.down, st.ydstogo = 1, 10
        return

    # Safety: loss/backward crossing own goal (yardline_100 - yards >= 100).
    if (st.yardline_100 - yards) >= 100:
        scoring = _other(st, st.possession)
        st.add_score(scoring, 2)
        st.events.append({"type": "safety", "team": scoring, "yards": yards})
        # After safety, scored-upon team free-kicks; scoring team receives (~own 25 → yl 75).
        apply_kickoff(st, receiving=scoring, yardline_100=kickoff_spot(st))
        return

    # Score only if yards from *current* field position reach the EZ.
    # Do NOT trust historical `touchdown` flags from a different yardline context.
    if (st.yardline_100 - yards) <= 0:
        scoring = st.possession
        st.add_score(scoring, 6)
        st.events.append({"type": "touchdown", "team": scoring, "yards": yards})
        _attempt_pat(rng, catalog, st, scoring)
        apply_kickoff(st, receiving=_other(st, scoring), yardline_100=kickoff_spot(st))
        if st.in_ot and st.ot_tracker is None:
            st.final = True
            st.events.append({"type": "final_ot"})
        return

    st.yardline_100 = int(np.clip(st.yardline_100 - yards, 1, 99))
    if yards >= st.ydstogo:
        st.down = 1
        st.ydstogo = 10 if st.yardline_100 >= 10 else max(1, st.yardline_100)
    else:
        st.down += 1
        st.ydstogo = max(1, int(st.ydstogo - yards))
        if st.down > 4:
            st.events.append({"type": "turnover_on_downs", "team": st.possession})
            st.possession = _other(st, st.possession)
            st.yardline_100 = int(np.clip(100 - st.yardline_100, 1, 99))
            st.down, st.ydstogo = 1, 10
            return



def _defensive_return(rng: np.random.Generator, catalog, st: GameState, spot: float, kind: str) -> None:
    """NFL-43 (review D2 fix): defensive return drawn from the as-of LEAGUE pool for this turnover kind.

    ``st.possession`` is already the defense. ``spot`` is the offense's yardline_100 after the play (<= 0 means the
    turnover happened in the offense's target end zone). End-zone turnovers without a return TD are touchbacks.
    """
    sem = getattr(catalog, "semantics", None)
    ret, ret_td = sem["returns"].draw_def_return(rng, kind)
    start_def = 80 if spot <= 0 else int(np.clip(100 - spot, 1, 99))
    if spot <= 0 and not ret_td:
        ret = 0.0  # end-zone recovery/INT -> touchback
    new_yl = start_def - int(round(ret))
    if ret_td or new_yl <= 0:
        st.events.append({"type": "def_return_td", "team": st.possession, "from_yl": start_def, "kind": kind,
                          "return_yards": start_def, "hist_return_yards": ret, "source": "league_pool"})
        st.special_scores["def_return_td"][st.possession] = st.special_scores["def_return_td"].get(st.possession, 0) + 1
        scoring = st.possession
        st.add_score(scoring, 6)
        _attempt_pat(rng, catalog, st, scoring)
        apply_kickoff(st, receiving=_other(st, scoring), yardline_100=kickoff_spot(st))
        return
    st.yardline_100 = int(np.clip(new_yl, 1, 99))
    st.events.append({"type": "def_return", "team": st.possession, "from_yl": start_def, "kind": kind,
                      "to_yl": st.yardline_100, "return_yards": start_def - st.yardline_100, "source": "league_pool",
                      "touchback": bool(spot <= 0 and not ret_td)})
    st.down, st.ydstogo = 1, 10


def no_play_clock_sec(catalog, acc: dict) -> int:
    """WP1: seconds charged per no-play foul. "asof_mean" = as-of mean clock of no-play penalty rows from the catalog's
    clock map (PlayCatalog.build_empirical_clock, stat="mean"), rounded to whole seconds like the kickoff clock; the
    flat semantics.NO_PLAY_CLOCK_SEC (4 s) when the map has no such entry (< 30 as-of rows) or for "flat_4s"."""
    from semantics import NO_PLAY_CLOCK_SEC
    if acc.get("no_play_clock") != "asof_mean":
        return int(NO_PLAY_CLOCK_SEC)
    v = (getattr(catalog, "clock_map", None) or {}).get("no_play_penalty")
    if v is None or not np.isfinite(float(v)):
        return int(NO_PLAY_CLOCK_SEC)
    return int(round(float(v)))


def _no_play_penalty(st: GameState, pen, clock_sec: int | None = None) -> None:
    """NFL-43: enforce a no-play foul; a defensive foul as the period clock expires earns one untimed down.
    clock_sec: seconds charged (WP1: the as-of mean via no_play_clock_sec); None = flat NO_PLAY_CLOCK_SEC (4 s)."""
    from semantics import enforce_penalty, NO_PLAY_CLOCK_SEC
    enforce_penalty(st, pen, live_ball=False)
    st.game_seconds_remaining -= int(NO_PLAY_CLOCK_SEC if clock_sec is None else clock_sec)
    if st.game_seconds_remaining <= 0 and pen.side == "defense":
        # A period cannot end on an accepted defensive foul: one untimed down.
        st.game_seconds_remaining = 1
        st.events.append({"type": "untimed_down", "qtr": st.qtr})


def _live_ball_penalty(st: GameState, pen, prev_pos, prev_scores, new_events) -> bool:
    """NFL-43: enforce a live-ball foul after the snap, or drop it if the play changed possession or scored.

    Returns True if enforced, False if dropped."""
    if not st.final and st.possession == prev_pos and (st.score_home, st.score_away) == prev_scores and \
            not any(e.get("type") in ("turnover", "turnover_on_downs", "kickoff") for e in new_events):
        from semantics import enforce_penalty
        enforce_penalty(st, pen, live_ball=True)
        return True
    st.events.append({"type": "penalty_live_ball_dropped", "reason": "possession_change_or_score", "team": pen.team})
    return False


def _process_kickoff_returns(rng: np.random.Generator, catalog, st: GameState, seen: list) -> None:
    """NFL-43: roll an as-of league-rate kickoff-return TD for each new kickoff event."""
    sem = getattr(catalog, "semantics", None)
    rate = sem["returns"].kick_return_td_rate
    rp = sem.get("rare_plays")
    if rp is not None and rp.clean_kick_return_td_rate is not None:
        rate = rp.clean_kick_return_td_rate  # NFL-75: onside kicks are resampled from their own pool
    i = seen[0]
    while i < len(st.events):
        e = st.events[i]
        i += 1
        if e.get("type") != "kickoff" or st.final:
            continue
        if rp is not None and _rare_onside(rng, catalog, st, e, rp):
            continue
        if rng.random() < rate:
            recv = e["receiving"]
            st.events.append({"type": "kick_return_td", "team": recv, "qtr": st.qtr})
            st.special_scores["kick_return_td"][recv] = st.special_scores["kick_return_td"].get(recv, 0) + 1
            st.add_score(recv, 6)
            _attempt_pat(rng, catalog, st, recv)
            apply_kickoff(st, receiving=_other(st, recv), yardline_100=kickoff_spot(st))
    seen[0] = i



def _rare_kick_formation(rng: np.random.Generator, catalog, st: GameState, kind: str, rp, np_sec: int) -> bool:
    """NFL-75: one as-of league draw per punt / FG decision: presnap foul, fake (or aborted snap), blocked kick or
    penalty-flagged kick, each resampled from the real rows of that class; "clean" returns False so the existing team
    punt / FG mechanics run. Returns True when this function resolved the play."""
    cls = rp.draw_formation_class(rng, kind)
    if cls == "clean":
        return False
    yl0 = int(st.yardline_100)
    row, band = rp.draw_outcome(rng, kind, cls, yl0)
    kicker = st.possession
    if cls == "presnap":
        _apply_presnap(st, row, int(np_sec), kind, band)
    elif cls == "fake":
        _apply_fake(rng, catalog, st, row, kind, band)
    else:
        st.game_seconds_remaining -= _clock_cost(kind, rng, getattr(catalog, "clock_map", None))
        _apply_rare_outcome(rng, catalog, st, kicker, row, kind=kind, cls=cls, ref_yl=yl0, extra={"los_band": band})
    return True


def _apply_presnap(st: GameState, row, clock_sec: int, kind: str, band: str) -> None:
    """Pre-snap (no-play) foul in kick formation at the LIVE down and distance: the line of scrimmage moves by the
    resampled row's shift; a defensive foul gives a first down if its yardage reaches the live line to gain or the
    row itself was an automatic first down (next down 1 although its yardage was short of the row's own distance);
    otherwise the live down repeats with the distance adjusted. The 4th-down decision is then made again."""
    yl0 = int(st.yardline_100)
    shift = int(row[3])
    new_yl = int(np.clip(yl0 + shift, 1, 99))
    gained = yl0 - new_yl  # > 0: defensive foul
    row_gained, row_next_down, row_togo = -shift, int(row[4]), row[9]
    auto_first = gained > 0 and row_next_down == 1 and not np.isnan(row_togo) and row_gained < float(row_togo)
    st.yardline_100 = new_yl
    if gained > 0 and (gained >= st.ydstogo or auto_first):
        st.down = 1
        st.ydstogo = 10 if new_yl >= 10 else max(1, new_yl)
    else:
        st.ydstogo = int(max(1, min(st.ydstogo - gained, 40)))
        if st.ydstogo > new_yl:
            st.ydstogo = max(1, new_yl)
    st.game_seconds_remaining -= int(clock_sec)
    st.events.append({"type": "rare_play", "kind": kind, "cls": "presnap", "team": st.possession, "from_yl": yl0,
                      "new_yl": new_yl, "down": st.down, "ydstogo": st.ydstogo, "result": "kicking_team_ball",
                      "auto_first_down": bool(auto_first), "los_band": band})
    if st.game_seconds_remaining <= 0 and gained > 0:
        st.game_seconds_remaining = 1  # a period cannot end on an accepted defensive foul: one untimed down
        st.events.append({"type": "untimed_down", "qtr": st.qtr})


def _apply_fake(rng: np.random.Generator, catalog, st: GameState, row, kind: str, band: str) -> None:
    """Fake / aborted kick-formation snap: the resampled league row (no player names) runs through the normal snap
    mechanics at the LIVE down, distance and field position, so conversion, TDs, turnovers and defensive returns
    follow the live situation, not the historical one."""
    kicker, yl0 = st.possession, int(st.yardline_100)
    sc0 = (st.score_home, st.score_away)
    r = row.copy()
    for c in ("passer_player_name", "rusher_player_name", "receiver_player_name"):
        r[c] = None
    _apply_row(rng, catalog, st, r, None, extra_ev={"rare_fake": kind})
    kick_gain = (st.score_home - sc0[0]) if kicker == st.home else (st.score_away - sc0[1])
    recv_gain = (st.score_away - sc0[1]) if kicker == st.home else (st.score_home - sc0[0])
    if kick_gain >= 6:
        res = "kicking_td"
    elif recv_gain >= 6:
        res = "receiving_td"
    elif recv_gain == 2:
        res = "receiving_safety"
    else:
        res = "kicking_team_ball" if st.possession == kicker else "receiving_team_ball"
    st.events.append({"type": "rare_play", "kind": kind, "cls": "fake", "team": kicker, "from_yl": yl0,
                      "result": res, "los_band": band})


def _apply_rare_outcome(rng, catalog, st: GameState, kicker: str, row, *, kind: str, cls: str, ref_yl: Optional[int],
                        extra: Optional[dict] = None) -> None:
    """Apply one resampled rare-play outcome row (rare_plays._outcomes layout).

    Scored rows: kicking-team TD (6 + PAT, then it kicks off), kicking-team FG (3, then it kicks off), receiving-team
    TD (6 + PAT, then it kicks off), receiving-team safety (2, the kicking team free-kicks). Other rows: the next
    possessor gets the ball at (reference + shift) in its own frame, reference = the kick's line of scrimmage
    (ref_yl, kicking frame) or 100 - ref_yl (receiving frame); ref_yl None (onside) uses the row's absolute spot."""
    recv = _other(st, kicker)
    kick_pts, recv_pts, possessor, shift, down, togo, abs_yl = (float(x) for x in list(row)[:7])
    ev = {"type": "rare_play", "kind": kind, "cls": cls, "team": kicker, "from_yl": ref_yl, **(extra or {})}
    if int(possessor) == -1:
        if kick_pts > 0:
            st.add_score(kicker, int(kick_pts))
            ev["result"] = {6: "kicking_td", 3: "kicking_fg"}.get(int(kick_pts), f"kicking_{int(kick_pts)}")
            st.events.append(ev)
            if int(kick_pts) == 6:
                _attempt_pat(rng, catalog, st, kicker)
            apply_kickoff(st, receiving=recv, yardline_100=kickoff_spot(st))
        else:
            st.add_score(recv, int(recv_pts))
            ev["result"] = {6: "receiving_td", 2: "receiving_safety"}.get(int(recv_pts), f"receiving_{int(recv_pts)}")
            st.events.append(ev)
            if int(recv_pts) == 6:
                _attempt_pat(rng, catalog, st, recv)
                apply_kickoff(st, receiving=kicker, yardline_100=kickoff_spot(st))
            else:  # safety: the scored-upon (kicking) team free-kicks to the scorer
                apply_kickoff(st, receiving=recv, yardline_100=kickoff_spot(st))
        if st.in_ot and st.ot_tracker is None:
            st.final = True
            st.events.append({"type": "final_ot"})
        return
    keep = int(possessor) == 1
    if ref_yl is None:
        new_yl = int(abs_yl)
    else:
        new_yl = int(ref_yl + shift) if keep else int(100 - ref_yl + shift)
    st.possession = kicker if keep else recv
    st.yardline_100 = int(np.clip(new_yl, 1, 99))
    st.down = int(np.clip(int(down), 1, 4))
    st.ydstogo = int(max(1, min(int(togo), st.yardline_100)))
    ev.update({"result": "kicking_team_ball" if keep else "receiving_team_ball", "new_yl": st.yardline_100,
               "down": st.down, "ydstogo": st.ydstogo})
    st.events.append(ev)


def _rare_onside(rng, catalog, st: GameState, e: dict, rp) -> bool:
    """NFL-75: onside decision for a kickoff that just happened (event e), from the as-of dynamic-kickoff-era rate in
    the kicking team's (quarter, deficit, seconds) cell. Only the latest kickoff with the state still on it can be
    changed. Returns True when an onside kick was taken (its outcome replaces the kickoff and its return-TD roll)."""
    recv = e.get("receiving")
    kicker = _other(st, recv)
    if st.possession != recv or e is not next((x for x in reversed(st.events) if x.get("type") == "kickoff"), None):
        return False
    lead = (st.score_home - st.score_away) if recv == st.home else (st.score_away - st.score_home)
    rate, tag = rp.onside_rate(int(st.qtr), int(lead), int(st.game_seconds_remaining))
    if rate is None or rate <= 0 or not len(rp.onside["pool"]):
        return False
    if rng.random() >= rate:
        return False
    row = rp.onside["pool"][int(rng.integers(0, len(rp.onside["pool"])))]
    _apply_rare_outcome(rng, catalog, st, kicker, row, kind="kickoff", cls="onside", ref_yl=None,
                        extra={"onside_cell": tag, "onside_rate": rate})
    return True


def _advance_period(st: GameState, home: str) -> None:
    if st.qtr == 1:
        st.qtr = 2
        st.game_seconds_remaining = 900
        st.events.append({"type": "end_q1"})
    elif st.qtr == 2:
        maybe_halftime(st, q3_receive=home)
    elif st.qtr == 3:
        st.qtr = 4
        st.game_seconds_remaining = 900
        st.events.append({"type": "end_q3"})
    elif st.qtr == 4:
        start_ot_if_tied(st)
    elif st.qtr >= 5:
        st.final = True
        st.events.append({"type": "final_ot_tie"})


def simulate_one(df: pd.DataFrame, catalog: PlayCatalog, cfg: dict, rng: np.random.Generator) -> GameState:
    home = cfg["game"]["home"]
    away = cfg["game"]["away"]
    st = GameState.new_game(home=home, away=away)
    st.game_seconds_remaining = 900  # Q1 only
    starts = getattr(catalog, "kickoff_starts", None)
    if starts is None and hasattr(catalog, "base"):
        starts = getattr(catalog.base, "kickoff_starts", None)
    if cfg.get("kickoff_start", "empirical") == "empirical" and starts is not None and len(starts):
        st.kickoff_sampler = lambda: int(starts[rng.integers(0, len(starts))])
    apply_kickoff(st, receiving=away, yardline_100=kickoff_spot(st))
    allow_pool = bool(cfg.get("proposed_pooling", {}).get("enabled", False))
    # Default research improvements (still labeled; not market-fit).
    # Duck-type EffectsCatalog / PlayCatalog: prefer methods on wrapper, else base.
    acc = accounting_from_cfg(cfg)
    def _clock(cat):
        if acc["clock"] == "mean":
            src = getattr(cat, "clock_df", None)
            return PlayCatalog.build_empirical_clock(
                src if src is not None else df, stat="mean",
                skip_unmodeled_rows=acc["unmodeled_row_clock"] == "attribute_to_prior_play")
        return PlayCatalog.build_empirical_clock(df)
    clock_key = (acc["clock"], acc["unmodeled_row_clock"])
    def _ensure_clock(cat):
        # A map cached by an earlier run under different clock accounting is rebuilt (review: a reused catalog
        # silently kept the first run's timeout attribution). Maps set by callers (no key recorded) are respected.
        for c in (cat, getattr(cat, "base", None)):
            if c is not None and getattr(c, "clock_map", None) is not None and \
                    c.__dict__.get("_clock_key") not in (None, clock_key):
                c.clock_map = None
        target = cat
        if getattr(cat, "clock_map", None) is None and hasattr(cat, "set_empirical_clock"):
            target.set_empirical_clock(_clock(cat))
            target.__dict__["_clock_key"] = clock_key
            if hasattr(cat, "base"):
                cat.base.__dict__["_clock_key"] = clock_key
        elif getattr(cat, "clock_map", None) is None and hasattr(cat, "base"):
            if getattr(cat.base, "clock_map", None) is None:
                cat.base.set_empirical_clock(_clock(cat.base))
                cat.base.__dict__["_clock_key"] = clock_key
            # mirror attributes for getattr(catalog, "clock_map") sites
            cat.clock_map = cat.base.clock_map
            cat.clock_meta = getattr(cat.base, "clock_meta", {"source": "fixed_defaults"})
            cat.__dict__["_clock_key"] = clock_key
    # NFL-49 A: h2h conditioning is no longer forced on here; build_catalog applies cfg defense_interaction.h2h
    # (default "off"). Catalogs built elsewhere keep whatever policy they were given.
    _ensure_clock(catalog)
    catalog.goal_line_censoring = acc["goal_line_censoring"]
    sem = getattr(catalog, "semantics", None)
    rpm = sem.get("rare_plays") if isinstance(sem, dict) else None
    if rpm is not None and rpm.research_budget is not None:
        if rpm.research_budget <= 0:
            raise ValueError(f"rare plays research budget exhausted (capped at n={RESEARCH_MAX_N}); never 100k")
        rpm.research_budget -= 1
    if sem is not None:
        st.ot_rule = sem.get("overtime") or st.ot_rule
        st.ot_coin = lambda: int(rng.integers(0, 2))
    steps = 0
    max_steps = 260 if sem is not None else 220
    ko_seen = [0]
    def _post(prev_pos, prev_scores):
        if sem is not None and sem.get("returns") is not None:
            _process_kickoff_returns(rng, catalog, st, ko_seen)
        if st.in_ot and st.ot_tracker is not None and not st.final:
            st.ot_tracker.update(st, prev_pos, prev_scores)
    _post(None, (0, 0)) if (sem is not None and sem.get("returns") is not None) else None
    ko_sec = int(round(float((getattr(catalog, "clock_map", None) or {}).get("kickoff", 0.0)))) if acc["kickoff_clock"] else 0
    np_sec = no_play_clock_sec(catalog, acc)
    ev_ptr = 0
    while not st.final and steps < max_steps:
        steps += 1
        if ko_sec > 0:
            # NFL-49 B: kickoffs run the game clock (W1-9 mean 4.8 s each, about 49 s a game); legacy charged 0.
            while ev_ptr < len(st.events):
                if st.events[ev_ptr].get("type") == "kickoff" and st.game_seconds_remaining > 0:
                    st.game_seconds_remaining -= ko_sec
                ev_ptr += 1
        prev_pos, prev_scores = st.possession, (st.score_home, st.score_away)
        if st.game_seconds_remaining <= 0:
            _advance_period(st, home)
            pos_after, sc_after = st.possession, (st.score_home, st.score_away)
            if sem is not None and sem.get("returns") is not None:
                _process_kickoff_returns(rng, catalog, st, ko_seen)
            if st.in_ot and st.ot_tracker is not None and not st.final:
                st.ot_tracker.update(st, pos_after, sc_after)
            continue
        if st.down == 4:
            decision = _fourth_down_decision(rng, catalog, st)
            rp = sem.get("rare_plays") if sem is not None else None
            if rp is not None and decision in ("punt", "field_goal"):
                if _rare_kick_formation(rng, catalog, st, decision, rp, np_sec):
                    _post(prev_pos, prev_scores)
                    continue
            if decision == "punt":
                _punt_fixed(rng, catalog, st)
                _post(prev_pos, prev_scores)
                continue
            if decision == "field_goal":
                _attempt_fg(rng, catalog, st)
                _post(prev_pos, prev_scores)
                continue
        pen = None
        if sem is not None and sem.get("penalties") is not None:
            pen = sem["penalties"].draw(rng, st.possession, _other(st, st.possession))
        if pen is not None and pen.no_play:
            _no_play_penalty(st, pen, clock_sec=np_sec)
            _post(prev_pos, prev_scores)
            continue
        n_ev = len(st.events)
        _apply_snap(rng, catalog, st, allow_pool=allow_pool)
        if pen is not None:
            _live_ball_penalty(st, pen, prev_pos, prev_scores, st.events[n_ev:])
        _post(prev_pos, prev_scores)
        if st.in_ot and st.final:
            break
    if not st.final:
        if st.reg_score_home is None:
            st.reg_score_home, st.reg_score_away = st.score_home, st.score_away
        st.final = True
        st.events.append({"type": "final_max_steps" if steps >= max_steps else "final"})
    if st.reg_score_home is None:
        st.reg_score_home, st.reg_score_away = st.score_home, st.score_away
    return st


ST_COUNT_KEYS = ("fg_made", "pat_good", "pat_blocked", "def_two_point", "kick_return_td", "punt_return_td",
                 "safety", "punt_blocked", "fg_blocked", "blocked_kick_td", "fake", "fake_kicking_td", "fake_def_td",
                 "kick_foul_presnap", "kick_foul_flagged", "flagged_kick_return_td", "onside_attempt", "onside_recovered",
                 "punt_plays", "fg_plays")


def special_teams_counts(st: GameState) -> dict:
    """Per-game special-teams event counts (both teams), read from the event log. Diagnostic only; no RNG."""
    c = dict.fromkeys(ST_COUNT_KEYS, 0)
    for e in st.events:
        t = e.get("type")
        if t == "punt":
            c["punt_plays"] += 1
        elif t == "field_goal" or t == "fg_sparse_miss_default":
            c["fg_plays"] += 1
            c["fg_made"] += int(e.get("result") == "made")
        elif t == "pat":
            if e.get("result") == "good":
                c["pat_good"] += 1
            elif e.get("result") == "blocked":
                c["pat_blocked"] += 1
                c["def_two_point"] += int(e.get("def_two_point") is not None)
        elif t == "kick_return_td":
            c["kick_return_td"] += 1
        elif t == "punt_return_td":
            c["punt_return_td"] += 1
        elif t == "safety":
            c["safety"] += 1
        elif t == "rare_play":
            cls, kind, res = e.get("cls"), e.get("kind"), e.get("result")
            if cls in ("fake", "blocked", "flagged"):
                c["punt_plays" if kind == "punt" else "fg_plays"] += 1
            c["fg_made"] += int(res == "kicking_fg")
            c["safety"] += int(res == "receiving_safety" and cls != "fake")  # a fake's safety is a "safety" event
            if cls == "blocked":
                c["punt_blocked" if kind == "punt" else "fg_blocked"] += 1
                c["blocked_kick_td"] += int(res == "receiving_td")
            elif cls == "fake":
                c["fake"] += 1
                c["fake_kicking_td"] += int(res == "kicking_td")
                c["fake_def_td"] += int(res == "receiving_td")
            elif cls == "presnap":
                c["kick_foul_presnap"] += 1
            elif cls == "flagged":
                c["kick_foul_flagged"] += 1
                c["flagged_kick_return_td"] += int(res == "receiving_td")
            elif cls == "onside":
                c["onside_attempt"] += 1
                c["onside_recovered"] += int(res in ("kicking_team_ball", "kicking_td"))
                c["kick_return_td"] += int(res == "receiving_td")
    return c


def source_composition(cfg):
    weeks = cfg['history']['weeks_inclusive']
    game = cfg['game']
    return f"team_only_{game['season']}_w{min(weeks)}_{max(weeks)}_{game['away']}_{game['home']}_empirical_not_possession_EP_model"


RESEARCH_MAX_N = 20_000  # research_unaccepted runs are capped here (never a 100k / lock run)


def simulate_games(cfg: dict, *, pbp_path: str | Path, n: int, seed: int,
                   research_unaccepted: tuple = ()) -> dict[str, Any]:
    """research_unaccepted: names of still_unsupported NFL-43 semantics this RESEARCH call may run although Ghost6 has
    not accepted their bounds (only "rare_plays" is recognised). n must be <= RESEARCH_MAX_N; the output is labeled
    UNACCEPTED_RESEARCH_ONLY. Configs alone can never do this: a config that enables rare plays is refused by
    nfl43.still_unsupported in every lock / 100k / rocket path, which never pass this argument."""
    if "joint_producer" in cfg:
        # The frozen model path owns its input reads, seed policy and ledger.
        # Never reuse historical yard-row player assignments as opportunities.
        from joint_producer import simulate_joint_games
        joint = cfg["joint_producer"]
        if joint["spec"]["mode"] != cfg["mode"] or joint["spec"]["config_id"] != cfg["config_id"]:
            raise ValueError("joint producer config/mode mismatch")
        result = simulate_joint_games(joint["spec"], input_root=joint["input_root"], inputs=joint["inputs"],
                                    n=n, seed=seed, output_root=joint["output_root"])
        if joint.get("shared_accounting", False):
            from shared_accounting import shared_projection
            result["shared_projections"] = [shared_projection(t) for t in result["trials"]]
            result["path_semantics"] = "SHARED_ACCOUNTING_V1"
        return result
    wk = (cfg.get("game") or {}).get("week_asof_exclusive")
    if wk is not None and int(cfg["history"]["weeks_inclusive"][-1]) >= int(wk):
        raise ValueError(f"history weeks {cfg['history']['weeks_inclusive']} not strictly before target week {wk}")
    hist = load_team_history(
        pbp_path,
        teams=cfg["history"]["teams"],
        season=cfg["history"]["season"],
        weeks=(cfg["history"]["weeks_inclusive"][0], cfg["history"]["weeks_inclusive"][-1]),
    )
    if hist["status"] != "OK":
        return {"status": hist["status"], "n_completed": 0, "error": "history_load_failed", "pooling_silently_applied": False}

    df = hist["df"]
    adj_meta: dict = {"enabled": False}
    qb_status: dict = {}
    if (cfg.get("adjustments") or {}).get("enabled"):
        df, adj_meta = apply_forward_qb_filter(df, cfg["adjustments"])
        for team, m in adj_meta.items():
            if isinstance(m, dict) and m.get("sparse_qb"):
                qb_status[team] = f"SPARSE_QB_HISTORY n_pass={m.get('n_pass_after')}"

    catalog, effects_prov = build_catalog(df, cfg, games_df=hist.get("games_df"))
    research_unaccepted = tuple(research_unaccepted or ())
    if research_unaccepted:
        bad = [x for x in research_unaccepted if x != "rare_plays"]
        if bad:
            raise ValueError(f"research_unaccepted only allows 'rare_plays', got {bad}")
        if int(n) > RESEARCH_MAX_N:
            raise ValueError(f"research_unaccepted runs are capped at n={RESEARCH_MAX_N} (got {n}); never 100k")
    semantics_meta = attach_semantics(catalog, cfg, pbp_path, research_unaccepted=research_unaccepted, research_n=int(n))
    rng = np.random.default_rng(seed)
    buckets = {k: [] for k in [
        "q1_home","q1_away","q2_home","q2_away","q3_home","q3_away","q4_home","q4_away",
        "h1_home","h1_away","h2_home","h2_away","ot_home","ot_away",
        "reg_home","reg_away","fg_home","fg_away","went_ot",
        "pen_yds_home","pen_yds_away","n_pen","ret_td_home","ret_td_away","def_td_home","def_td_away","tie",
    ]}
    joint_acc = {"pass_yards": {}, "rush_yards": {}, "rec_yards": {}}
    st_counts = {k: [] for k in ST_COUNT_KEYS}
    sparse_counts = 0
    coarse_counts = 0
    def_cond_plays = 0
    def_inter = 0
    blitz_ev = 0
    player_samples: list[dict] = []
    n_snaps_total = 0
    n_coarse_snap_flags = 0
    n_coarse_blitz = 0
    for _ in range(n):
        st = simulate_one(df, catalog, cfg, rng)
        snap = st.period_snapshot()
        # Prefer explicit reg freeze when set
        if st.reg_score_home is not None:
            snap["reg_home"] = st.reg_score_home
            snap["reg_away"] = st.reg_score_away
        hm, aw = cfg["game"]["home"], cfg["game"]["away"]
        ss = st.special_scores
        snap.update({
            "pen_yds_home": st.penalty_yards.get(hm, 0), "pen_yds_away": st.penalty_yards.get(aw, 0),
            "n_pen": sum(1 for e in st.events if e.get("type") == "penalty"),
            "ret_td_home": ss["kick_return_td"].get(hm, 0) + ss["punt_return_td"].get(hm, 0),
            "ret_td_away": ss["kick_return_td"].get(aw, 0) + ss["punt_return_td"].get(aw, 0),
            "def_td_home": ss["def_return_td"].get(hm, 0), "def_td_away": ss["def_return_td"].get(aw, 0),
            "tie": int(st.score_home == st.score_away),
        })
        for k, v in special_teams_counts(st).items():
            st_counts[k].append(v)
        for k in buckets:
            if k == "went_ot":
                buckets[k].append(bool(st.in_ot))
            else:
                buckets[k].append(snap[k])
        hard = [f for f in st.sparse_flags if f.startswith("SPARSE") or f.startswith("EMPTY") or "FALLBACK" in f]
        coarse = [f for f in st.sparse_flags if f.startswith("COARSE")]
        # COARSE_* is expected team-only coarsening — reported separately from hard sparse
        if hard:
            sparse_counts += 1
        if coarse:
            coarse_counts += 1
        def_cond_plays += sum(1 for f in st.sparse_flags if f.startswith("DEF_COND"))
        def_inter += sum(1 for f in st.sparse_flags if f.startswith("DEF_COND") or f.startswith("DEF_ALLOWED"))
        blitz_ev += sum(1 for f in st.sparse_flags if f.startswith("EFFECT_"))
        n_snaps_total += sum(1 for e in st.events if e.get("type") == "snap")
        n_coarse_snap_flags += sum(1 for f in st.sparse_flags if f.startswith("COARSE_SAME_DOWN") or f.startswith("COARSE_ANY_DOWN"))
        n_coarse_blitz += sum(1 for f in st.sparse_flags if f.startswith("COARSE_BLITZ"))
        player_samples.append({f"{k}|{tm}|{pl}": y for k, d in st.player_counts.items() for tm, pls in d.items() for pl, y in pls.items()})
        for kind in ("pass_yards", "rush_yards", "rec_yards"):
            for team, players in st.player_counts.get(kind, {}).items():
                bucket = joint_acc.setdefault(kind, {}).setdefault(team, {})
                for plyr, yds in players.items():
                    bucket[plyr] = bucket.get(plyr, 0.0) + yds

    for kind in joint_acc:
        for team in joint_acc[kind]:
            for plyr in list(joint_acc[kind][team]):
                joint_acc[kind][team][plyr] = joint_acc[kind][team][plyr] / n

    status = "OK_WITH_SPARSE_FLAGS" if sparse_counts else "OK"
    return {
        "status": status,
        "shared_contract_status": "UNIMPLEMENTED_LEGACY_YARD_ROW_BOOTSTRAP",
        "adapter_projection_allowed": False,
        "n_completed": n,
        "n_requested": n,
        "seed": seed,
        "config_id": cfg["config_id"],
        "mode": cfg["mode"],
        "pooling_silently_applied": False,
        "proposed_pooling_enabled": bool(cfg.get("proposed_pooling", {}).get("enabled", False)),
        "history_evidence": hist["evidence"],
        "adjustments_meta": adj_meta,
        "qb_status": qb_status,
        "evidence_summary": {
            "min_n_state": cfg["min_n_state"],
            "games_with_sparse_flags": sparse_counts,
            "sparse_rate": sparse_counts / n if n else None,
            "games_with_coarse_flags": coarse_counts,
            "coarse_rate": coarse_counts / n if n else None,
            "defense_cond_flag_events": def_cond_plays,
            "def_interaction_events": def_inter,
            "blitz_strata_events": blitz_ev,
            "blitz_coarse_down_events": n_coarse_blitz,
            "per_snap_coarse_fraction": (n_coarse_snap_flags / n_snaps_total) if n_snaps_total else None,
            "note": "sparse_rate = hard SPARSE/EMPTY/FALLBACK only; coarse_rate = COARSE_* support gaps",
        },
        "arrays": {k: np.asarray(v) for k, v in buckets.items()},
        "special_teams_counts": {k: np.asarray(v, dtype=int) for k, v in st_counts.items()},
        "player_joint": joint_acc,
        "player_samples": player_samples,
        "effects_provenance": effects_prov,
        "semantics": semantics_meta,
        "limitations": [
            "Vertical slice: empirical team-only snap resampling + explicit same-team coarser fallbacks",
            "Clock costs use empirical median deltas when available else fixed means — not a situational clock model",
            ("OT rule: official 2025 regular-season (both possess, then sudden death, ties allowed)"
             if semantics_meta.get("overtime") == "official_2025_regular_season"
             else "OT rule is single-possession approx (declared)"),
            "No league silent pool; proposed pooling config default false",
            "W1-8 development set; no betting edge claim",
            "Inspired conceptually by NFLSimulatoR/nflfastR (MIT); no R source copied",
            "See FEATURE_MATRIX.md for unimplemented coverage/route/pressure fields",
            "NFL-43 still_unsupported (not invented): " + ", ".join(
                semantics_meta.get("still_unsupported") or []),
        ],
        "source_composition": source_composition(cfg),
    }


_SCRIMMAGE = ("run", "pass", "punt", "field_goal", "qb_kneel", "qb_spike")


def kickoff_start_yardlines(df: Optional[pd.DataFrame], exclude_onside: bool = False) -> Optional[np.ndarray]:
    """yardline_100 of the receiving team's first scrimmage play after each kickoff.

    Kickoffs recovered by the kicking team (onside) or returned for a score have no such
    play by the receiving team and are left out. Returns None when the columns are missing.
    exclude_onside (NFL-75 rare plays): also leave out every onside kick (desc), because rare plays resamples
    onside kicks from their own as-of pool; False keeps the pre-NFL-75 pool exactly.
    """
    need = {"game_id", "play_id", "play_type", "posteam", "yardline_100", "kickoff_attempt"}
    if df is None or not len(df) or not need <= set(df.columns):
        return None
    d = df.sort_values(["game_id", "play_id"])
    gid, pt, pos, yl = (d[c].to_numpy() for c in ("game_id", "play_type", "posteam", "yardline_100"))
    ko = d["kickoff_attempt"].fillna(0).to_numpy() == 1
    starts = ko
    if exclude_onside and "desc" in d.columns:
        starts = ko & ~d["desc"].fillna("").astype(str).str.lower().str.contains("onside", regex=False).to_numpy()
    out = []
    for i in np.flatnonzero(starts):
        j = i + 1
        while j < len(d) and gid[j] == gid[i] and pt[j] not in _SCRIMMAGE and not ko[j]:
            j += 1
        if j < len(d) and gid[j] == gid[i] and not ko[j] and pos[j] == pos[i] and pd.notna(yl[j]):
            out.append(int(yl[j]))
    return np.asarray(out, dtype=int) if out else None


def yl4_bucket(yl) -> str:
    yl = float(yl)
    return "fg_range" if yl <= 35 else ("mid" if yl <= 60 else "own")


def togo4_bucket(tg) -> str:
    tg = float(tg)
    return "short" if tg <= 2 else ("med" if tg <= 5 else "long")


def build_catalog(df: pd.DataFrame, cfg: dict, games_df: Optional[pd.DataFrame] = None):
    """Single construction path: PlayCatalog -> EffectsCatalog, with provenance. Same for all callers."""
    from effects.apply_supported import EffectsCatalog, annotate_snaps
    from effects.evidence_tables import load_ftn_join
    min_n = int(cfg["min_n_state"])
    acc = accounting_from_cfg(cfg)
    from rare_plays import mode_from_cfg
    rare = mode_from_cfg(cfg) != "off"
    base = PlayCatalog(df, min_n=min_n, games_df=games_df, exclude_clock_mgmt=acc["exclude_clock_mgmt_snaps"],
                       rare_plays=rare)
    di = cfg.get("defense_interaction") or {}
    if di.get("mode") == "opponent_allowed":
        base.enable_defense_allowed(float(di.get("weight", 0.0)))
        def_prov = {"mode": "opponent_allowed", "weight": base._def_allowed_w,
                    "label": "STRUCTURAL_ASSUMPTION_mixture_weight_not_fitted",
                    "n_defenses_with_pools": len({k[0] for k in base.def_allowed_down})}
    else:
        def_prov = {"mode": di.get("mode", "h2h_only"), "label": "DISABLED_opponent_allowed"}
    def_prov["h2h"] = base.set_h2h_policy(h2h_policy_from_cfg(cfg))
    def_prov["h2h_label"] = ("STRUCTURAL_ASSUMPTION_not_fitted" if def_prov["h2h"]["mode"] == "shrunk"
                             else "LEGACY_100PCT_H2H_KNOWN_MODEL_ERROR" if def_prov["h2h"]["mode"] == "legacy_always"
                             else "OFF")
    eff_cfg = cfg.get("effects") or {}
    want = bool(eff_cfg.get("enable_blitz_strata", False))
    ftn = load_ftn_join(df) if want else {"meta": {"status": "NOT_REQUESTED"}, "joined": None}
    ann = annotate_snaps(ftn["joined"] if ftn.get("joined") is not None else df)
    cat = EffectsCatalog(base, ann, enable_blitz_strata=want and ftn.get("joined") is not None)
    def_rates = {}
    if want and games_df is not None and ftn.get("joined") is not None:
        gj = load_ftn_join(games_df).get("joined")
        if gj is not None:
            pj = gj[(gj["play_type"] == "pass") & gj["ftn_joined"]]
            for d, g in pj.groupby("defteam"):
                if len(g) >= 20:
                    def_rates[str(d)] = float(g["is_blitz_ftn"].mean())
            cat.set_defense_blitz_rates(def_rates)
    prov = {
        "catalog_class": type(cat).__name__,
        "ftn_join": {k: v for k, v in ftn["meta"].items()},
        "blitz_strata_enabled": cat.enable_blitz_strata,
        "blitz_semantics": "conditions yards on CALLED pass only; run/pass choice from base sampler",
        "defense_blitz_rates": def_rates,
        "defense_interaction": def_prov,
        "accounting": acc,
        "rare_plays_catalog": rare,
        "pressure_coverage": "NOT_EXECUTED_adapters_only (2026 participation unpublished)",
    }
    return cat, prov


def attach_semantics(catalog, cfg: dict, pbp_path, research_unaccepted: tuple = (), research_n: Optional[int] = None) -> dict:
    """NFL-43: build opt-in penalty / return / OT semantics from cfg["semantics"].
    NFL-75: cfg["semantics"]["rare_plays"] = "asof_league_v1" adds rare_plays.py (refused by nfl43.still_unsupported
    unless this is a capped research call with research_unaccepted=("rare_plays",))."""
    from rare_plays import mode_from_cfg, build_rare_play_model
    sc = cfg.get("semantics")
    if not sc:
        return {"status": "LEGACY_UNSUPPORTED", "penalties": "UNSUPPORTED", "returns": "UNSUPPORTED",
                "overtime": "single_possession_approx_declared_limitation"}
    rare_mode = mode_from_cfg(cfg)
    gate_cfg = cfg
    research_rare = rare_mode != "off" and "rare_plays" in tuple(research_unaccepted or ())
    if research_rare and (research_n is None or not 0 < int(research_n) <= RESEARCH_MAX_N):
        raise ValueError(f"research_unaccepted needs research_n in 1..{RESEARCH_MAX_N} (got {research_n}); never 100k")
    if research_rare:
        # Only the rare_plays key is lifted for this capped research call; everything else is still checked.
        gate_cfg = {**cfg, "semantics": {k: v for k, v in sc.items() if k != "rare_plays"}}
    # NFL-43 residual R2: record still_unsupported in every opt-in run; refuse if this config enables one.
    try:
        repo = Path(__file__).resolve().parents[2]
        import sys
        if str(repo) not in sys.path:
            sys.path.insert(0, str(repo))
        from pipeline import hooks
        flags = hooks.known_flags()
        ex = hooks.nfl43_still_unsupported(flags, cfg=gate_cfg)
    except Exception as e:
        raise ValueError(f"UNSUPPORTED: nfl43.still_unsupported could not be enforced ({e!r})") from e
    if ex["status"] != "OK":
        raise ValueError("UNSUPPORTED: " + ex["reason"])
    from semantics import build_penalty_model, build_return_model, OT_RULES
    wk = int(cfg["game"]["week_asof_exclusive"])
    season = int(cfg["game"].get("season", cfg["history"]["season"]))
    sem: dict = {"penalties": None, "returns": None, "overtime": sc.get("overtime", OT_RULES[0])}
    meta: dict = {"status": "NFL43_SEMANTICS_V1", "overtime": sem["overtime"],
                  "still_unsupported": ex.get("exclusions") or [],
                  "still_unsupported_status": ex["status"]}
    if sem["overtime"] not in OT_RULES:
        raise ValueError(f"unknown ot rule {sem['overtime']}")
    if rare_mode != "off" and sc.get("returns") != "asof_league_v1":
        raise ValueError("UNSUPPORTED: semantics.rare_plays needs returns asof_league_v1 (kickoffs are processed there)")
    if sc.get("penalties") == "canonical_log_v1":
        teams = [cfg["game"]["home"], cfg["game"]["away"]]
        pm = build_penalty_model(teams, week_asof_exclusive=wk, season=season, pbp_path=pbp_path,
                                 **({"exclude_kick_formation": True} if rare_mode != "off" else {}))
        sem["penalties"] = pm
        meta["penalties"] = {"mode": "canonical_log_v1", **pm.meta}
    else:
        meta["penalties"] = "UNSUPPORTED"
    if sc.get("returns") == "asof_league_v1":
        rm = build_return_model(pbp_path, season=season, week_asof_exclusive=wk)
        sem["returns"] = rm
        meta["returns"] = {"mode": "asof_league_v1", "kick_return_td_rate": rm.kick_return_td_rate,
                           "punt_return_td_rate": rm.punt_return_td_rate, **rm.meta}
    else:
        meta["returns"] = "UNSUPPORTED"
    sem["rare_plays"] = None
    if rare_mode != "off":
        base_cat = getattr(catalog, "base", catalog)
        if not getattr(base_cat, "rare_plays", False):
            raise ValueError("UNSUPPORTED: semantics.rare_plays needs a catalog built with rare_plays=True "
                             "(build_catalog with the same cfg); a pre-NFL-75 catalog would double count")
        rpm = build_rare_play_model(pbp_path, season=season, week_asof_exclusive=wk, mode=rare_mode)
        if research_rare:
            rpm.research_budget = int(research_n)  # simulate_one refuses once this many games have run
        sem["rare_plays"] = rpm
        meta["rare_plays"] = {**rpm.meta, "gate": ("UNACCEPTED_RESEARCH_ONLY: nfl43.still_unsupported still lists these; "
                                                   "refused for locks / 100k / rocket until Ghost6 accepts the bounds")
                                                  if research_rare else "ACCEPTED_BY_GATE"}
    else:
        meta["rare_plays"] = "off"
    catalog.semantics = sem
    if hasattr(catalog, "base"):
        catalog.base.semantics = sem
    return meta
