"""NFL-75 per-player box recorder for the legacy yard-row engine (the path pipeline.sim100k runs).

OBSERVATIONAL ONLY. It is called once per snap from simulate._apply_row, after the engine has drawn the row and
before the state transition, reads the row and the pre-play state, and writes into its own ledger. It never touches
the RNG, the game state, the events list or the existing player_counts yard ledger, so game results are bit-identical
with it on or off (tests/test_player_box.py checks 4 configs x 2 seeds against digests from main 3dad900).

Attribution (one sampled historical row = one snap at the LIVE state; yards are the engine's realized yards, i.e.
capped at the live goal line exactly as simulate._apply_row credits its yard ledger):
  pass, sack == 0  -> passer pass_att. Target when the row names a receiver, or when it is a completion, or when the
                      engine nulled the names on a foreign row (opponent-allowed pool / league fake rows) and the
                      original row named a receiver; otherwise untargeted_att (throwaway etc.).
                      complete_pass -> passer pass_cmp/pass_yds, receiver rec/rec_yds; TD (live state) -> pass_td/rec_td.
                      interception -> passer int_thrown, defender def_int.
  pass, sack == 1  -> passer sacks_taken/sack_yds; defense sacks_made: sack_player_name 1, or half_sack_1/2 0.5 each.
  run              -> rusher carries/rush_yds (QB scrambles are runs, as in nflverse); TD -> rush_td.
  qb_kneel/qb_spike-> kneels/kneel_yds (rusher) and spikes (passer), kept out of carries/pass_att (the existing yard
                      ledger does not credit them either). Present only when accounting keeps clock-mgmt snaps.
  fumble_lost      -> fumbles_lost to fumbled_1_player_name (an interception that is also flagged fumble_lost is one
                      turnover and counts as the interception, like the engine's single turnover event).
Names missing, or the row is from another offense (posteam != offense) -> the UNASSIGNED line of that team, so team
totals always equal the sum of the player lines. Defensive names (sacks_made, def_int) are credited only when the row's
posteam/defteam are the live offense/defense; otherwise UNASSIGNED.

Known accounting choices (not fixes, documented): a live-ball penalty enforced after the snap (NFL-43 semantics)
does not erase the snap's stats; return TDs, kick/punt plays and special-teams scores are not player lines here.
Research only. projection_ready stays false."""
from __future__ import annotations
from pathlib import Path
from typing import Optional

import numpy as np

SCHEMA = "nfl75-player-box/1"
UNASSIGNED = "UNASSIGNED"
PLAYER_STATS = ("pass_att", "pass_cmp", "pass_yds", "pass_td", "int_thrown", "sacks_taken", "sack_yds",
                "targets", "rec", "rec_yds", "rec_td", "carries", "rush_yds", "rush_td", "fumbles_lost",
                "kneels", "kneel_yds", "spikes", "sacks_made", "def_int")
TEAM_ONLY_STATS = ("plays", "untargeted_att", "other_plays", "other_yds", "other_td", "safeties_allowed")
LOOKUP_COLS = ("sack_player_name", "half_sack_1_player_name", "half_sack_2_player_name", "interception_player_name",
               "fumbled_1_player_name", "receiver_player_name")


def _name(v) -> Optional[str]:
    """Same validity rule as simulate._credit_player."""
    if not isinstance(v, str) or not v or v == "nan":
        return None
    return v


def _int(row, c) -> int:
    v = row.get(c) if hasattr(row, "get") else None
    try:
        if v is None or v != v:
            return 0
        return int(v)
    except (TypeError, ValueError):
        return 0


def load_lookup(pbp_path, game_ids) -> dict:
    """(game_id, play_id) -> defensive / original-receiver names for the history rows. Read-only side table, so the
    engine's catalog dataframe (and therefore every draw) is unchanged."""
    path = Path(pbp_path)
    if not path.exists():
        return {}
    import pyarrow.parquet as pq
    import pandas as pd
    have = set(pq.ParquetFile(path).schema_arrow.names)
    cols = ["game_id", "play_id"] + [c for c in LOOKUP_COLS if c in have]
    df = pd.read_parquet(path, columns=cols)
    df = df[df["game_id"].isin(set(game_ids))]
    out = {}
    for rec in df.to_dict("records"):
        pid = rec.pop("play_id")
        if pid is None or pid != pid:
            continue
        out[(str(rec.pop("game_id")), int(pid))] = {k: v for k, v in rec.items() if _name(v)}
    return out


class BoxRecorder:
    """One game's per-player box lines + an independent team ledger."""

    def __init__(self, home: str, away: str, lookup: Optional[dict] = None):
        self.home, self.away = home, away
        self.lookup = lookup or {}
        self.players: dict = {home: {}, away: {}}
        self.team: dict = {home: {}, away: {}}

    # -- ledger helpers
    def _t(self, team, stat, v=1):
        d = self.team.setdefault(team, {})
        d[stat] = d.get(stat, 0) + v

    def _p(self, team, name, stat, v=1):
        d = self.players.setdefault(team, {}).setdefault(name or UNASSIGNED, {})
        d[stat] = d.get(stat, 0) + v
        self._t(team, stat, v)

    def _look(self, row) -> dict:
        try:
            gid, pid = row.get("game_id"), row.get("play_id")
            if gid is None or pid is None or pid != pid:
                return {}
            return self.lookup.get((str(gid), int(pid)), {})
        except (TypeError, ValueError):
            return {}

    # -- the hook
    def snap(self, st, row, play_type: str, yards: float) -> None:
        """Called by simulate._apply_row after the snap event is appended and BEFORE any state change."""
        off = st.possession
        de = self.away if off == self.home else self.home
        y0 = int(st.yardline_100)
        same_off = row.get("posteam") == off if hasattr(row, "get") else False
        same_def = same_off and row.get("defteam") == de
        lk = self._look(row)
        nm = lambda c: _name(row.get(c)) if same_off else None  # noqa: E731
        dn = lambda c: _name(lk.get(c)) if same_def else None  # noqa: E731
        is_int = _int(row, "interception") == 1
        is_fum = (not is_int) and _int(row, "fumble_lost") == 1
        turnover = is_int or is_fum
        safety = (not turnover) and (y0 - yards) >= 100
        td = (not turnover) and (not safety) and (y0 - yards) <= 0
        self._t(off, "plays")
        credited_td = False
        if play_type == "pass" and _int(row, "sack") == 1:
            p = nm("passer_player_name")
            self._p(off, p, "sacks_taken")
            self._p(off, p, "sack_yds", yards)
            full, h1, h2 = dn("sack_player_name"), dn("half_sack_1_player_name"), dn("half_sack_2_player_name")
            if full:
                self._p(de, full, "sacks_made", 1.0)
            elif h1 and h2:
                self._p(de, h1, "sacks_made", 0.5)
                self._p(de, h2, "sacks_made", 0.5)
            else:
                self._p(de, h1 or h2, "sacks_made", 1.0)  # one half name only (or none): whole sack, unassigned if none
        elif play_type == "pass":
            p = nm("passer_player_name")
            self._p(off, p, "pass_att")
            r = nm("receiver_player_name")
            complete = _int(row, "complete_pass") == 1
            nulled_had_receiver = (_name(row.get("receiver_player_name")) is None and
                                   _name(lk.get("receiver_player_name")) is not None)
            if r is not None or complete or nulled_had_receiver:
                self._p(off, r, "targets")
            else:
                self._t(off, "untargeted_att")
            if complete:
                self._p(off, p, "pass_cmp")
                self._p(off, p, "pass_yds", yards)
                self._p(off, r, "rec")
                self._p(off, r, "rec_yds", yards)
                if td:
                    self._p(off, p, "pass_td")
                    self._p(off, r, "rec_td")
                    credited_td = True
            else:
                self._t(off, "other_yds", yards)
            if is_int:
                self._p(off, p, "int_thrown")
                self._p(de, dn("interception_player_name"), "def_int")
        elif play_type == "run":
            r = nm("rusher_player_name")
            self._p(off, r, "carries")
            self._p(off, r, "rush_yds", yards)
            if td:
                self._p(off, r, "rush_td")
                credited_td = True
        elif play_type == "qb_kneel":
            r = nm("rusher_player_name")
            self._p(off, r, "kneels")
            self._p(off, r, "kneel_yds", yards)
        elif play_type == "qb_spike":
            self._p(off, nm("passer_player_name"), "spikes")
            self._t(off, "other_yds", yards)
        else:
            self._t(off, "other_plays")
            self._t(off, "other_yds", yards)
        if td and not credited_td:
            self._t(off, "other_td")
        if is_fum:
            self._p(off, _name(lk.get("fumbled_1_player_name")) if same_off else None, "fumbles_lost")
        if safety:
            self._t(off, "safeties_allowed")

    # -- per-trial reconciliation against the engine's own records
    def reconcile(self, st) -> list[str]:
        bad = []
        g = lambda t, s: self.team.get(t, {}).get(s, 0)  # noqa: E731
        for t in (self.home, self.away):
            sums: dict = {}
            for pl in self.players.get(t, {}).values():
                for s, v in pl.items():
                    sums[s] = sums.get(s, 0) + v
            for s in set(sums) | {s for s in self.team.get(t, {}) if s in PLAYER_STATS}:
                if sums.get(s, 0) != g(t, s):
                    bad.append(f"player_sum_eq_team:{t}:{s}:{sums.get(s, 0)}!={g(t, s)}")
            types = g(t, "pass_att") + g(t, "sacks_taken") + g(t, "carries") + g(t, "kneels") + g(t, "spikes") + \
                g(t, "other_plays")
            if types != g(t, "plays"):
                bad.append(f"plays_eq_play_types:{t}:{types}!={g(t, 'plays')}")
            if g(t, "targets") + g(t, "untargeted_att") != g(t, "pass_att"):
                bad.append(f"pass_att_eq_targets_plus_untargeted:{t}")
            td_ev = sum(1 for e in st.events if e.get("type") == "touchdown" and e.get("team") == t)
            if g(t, "rush_td") + g(t, "rec_td") + g(t, "other_td") != td_ev:
                bad.append(f"off_td_eq_engine_td_events:{t}:{td_ev}")
            to_ev = sum(1 for e in st.events if e.get("type") == "turnover" and e.get("team") == t)
            if g(t, "int_thrown") + g(t, "fumbles_lost") != to_ev:
                bad.append(f"turnovers_eq_engine_turnover_events:{t}:{to_ev}")
            for stat, kind in (("rec_yds", "rec_yards"), ("rush_yds", "rush_yards"), ("pass_yds", "pass_yards")):
                eng = st.player_counts.get(kind, {}).get(t, {})
                mine = {n: v.get(stat, 0) for n, v in self.players.get(t, {}).items()
                        if n != UNASSIGNED and v.get(stat, 0) != 0}
                if {n: float(v) for n, v in mine.items()} != {n: float(v) for n, v in eng.items() if v != 0}:
                    bad.append(f"{stat}_eq_engine_ledger:{t}")
        opp = {self.home: self.away, self.away: self.home}
        for t in (self.home, self.away):
            if g(opp[t], "sacks_made") != g(t, "sacks_taken"):
                bad.append(f"sacks_made_eq_sacks_taken:{t}")
        snaps = [e for e in st.events if e.get("type") == "snap"]
        if g(self.home, "plays") + g(self.away, "plays") != len(snaps):
            bad.append(f"plays_eq_engine_snaps:{len(snaps)}")
        yds = sum(g(t, s) for t in (self.home, self.away)
                  for s in ("pass_yds", "sack_yds", "rush_yds", "kneel_yds", "other_yds"))
        if float(yds) != float(sum(e["yards"] for e in snaps)):
            bad.append("yards_eq_engine_snap_yards")
        return bad


RECON_CHECKS = ("player_sum_eq_team", "plays_eq_engine_snaps", "plays_eq_play_types",
                "pass_att_eq_targets_plus_untargeted", "off_td_eq_engine_td_events",
                "turnovers_eq_engine_turnover_events", "yards_eq_engine_snap_yards", "rec_yds_eq_engine_ledger",
                "rush_yds_eq_engine_ledger", "pass_yds_eq_engine_ledger", "sacks_made_eq_sacks_taken")


class Accumulator:
    """Per-trial lines -> dense (trials x columns) float64 matrices. Columns appear on first use; earlier trials
    are zero for them (a player who never registers a stat in a trial has 0 in that trial)."""

    def __init__(self):
        self.cols: dict = {}
        self.tcols: dict = {}
        self.rows: list = []
        self.trows: list = []
        self.failures = 0
        self.first_failures: list = []

    def add(self, box: BoxRecorder, st) -> None:
        r, tr = {}, {}
        for t, pls in box.players.items():
            for p, stats in pls.items():
                for s, v in stats.items():
                    r[self.cols.setdefault((t, p, s), len(self.cols))] = v
        for t, stats in box.team.items():
            for s, v in stats.items():
                tr[self.tcols.setdefault((t, s), len(self.tcols))] = v
        self.rows.append(r)
        self.trows.append(tr)
        bad = box.reconcile(st)
        if bad:
            self.failures += 1
            if len(self.first_failures) < 5:
                self.first_failures.append({"trial": len(self.rows) - 1, "checks": bad[:10]})

    @staticmethod
    def _dense(rows, ncol):
        m = np.zeros((len(rows), ncol), dtype=np.float64)
        for i, r in enumerate(rows):
            for j, v in r.items():
                m[i, j] = v
        return m

    def result(self) -> dict:
        return {"schema": SCHEMA,
                "columns": [list(k) for k in self.cols], "values": self._dense(self.rows, len(self.cols)),
                "team_columns": [list(k) for k in self.tcols], "team_values": self._dense(self.trows, len(self.tcols)),
                "player_stats": list(PLAYER_STATS), "team_only_stats": list(TEAM_ONLY_STATS),
                "reconciliation": {"trials": len(self.rows), "failures": self.failures,
                                   "first_failures": self.first_failures, "checks": list(RECON_CHECKS)},
                "attribution": "player_box.py module docstring", "research_only": True}


def merge(parts: list) -> dict:
    """Concatenate chunk results (lock.run_sim) on the union of columns, chunk order preserved."""
    parts = [p for p in parts if p]
    if not parts:
        return {}
    cols, tcols = [], []
    for p in parts:
        for c in p["columns"]:
            if tuple(c) not in {tuple(x) for x in cols}:
                cols.append(list(c))
        for c in p["team_columns"]:
            if tuple(c) not in {tuple(x) for x in tcols}:
                tcols.append(list(c))
    ci = {tuple(c): j for j, c in enumerate(cols)}
    ti = {tuple(c): j for j, c in enumerate(tcols)}
    vals, tvals = [], []
    for p in parts:
        n = p["values"].shape[0]
        m = np.zeros((n, len(cols)))
        m[:, [ci[tuple(c)] for c in p["columns"]]] = p["values"]
        tm = np.zeros((n, len(tcols)))
        tm[:, [ti[tuple(c)] for c in p["team_columns"]]] = p["team_values"]
        vals.append(m)
        tvals.append(tm)
    rec = {"trials": sum(p["reconciliation"]["trials"] for p in parts),
           "failures": sum(p["reconciliation"]["failures"] for p in parts),
           "first_failures": [f for p in parts for f in p["reconciliation"]["first_failures"]][:5],
           "checks": parts[0]["reconciliation"]["checks"]}
    return {**{k: v for k, v in parts[0].items() if k not in ("columns", "values", "team_columns", "team_values",
                                                               "reconciliation")},
            "columns": cols, "values": np.concatenate(vals), "team_columns": tcols,
            "team_values": np.concatenate(tvals), "reconciliation": rec}


def summarize(columns, values) -> dict:
    """{team: {player: {stat: mean, median, p10, p25, p75, p90}}} over trials."""
    out: dict = {}
    if len(columns) == 0:
        return out
    v = np.asarray(values, dtype=float)
    q = np.percentile(v, [10, 25, 50, 75, 90], axis=0)
    mean = v.mean(axis=0)
    for j, (t, p, s) in enumerate(columns):
        out.setdefault(t, {}).setdefault(p, {})[s] = {
            "mean": float(mean[j]), "median": float(q[2, j]), "p10": float(q[0, j]), "p25": float(q[1, j]),
            "p75": float(q[3, j]), "p90": float(q[4, j])}
    return out
