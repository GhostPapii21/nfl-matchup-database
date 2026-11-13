"""NFL-75 Phase 2: player OPPORTUNITY model for the legacy yard-row engine (opt-in, research only).

Why. The engine resamples historical rows that still carry their original player names, with no availability or role
filter (name-locked resampling): NYG's sampled dropbacks split Winston/McCarthy/Dart in proportion to Weeks 1-9 rows,
although McCarthy started Nov 12, and a player can only ever record an event that is in his own rows (Daniels has no
interception rows, so the name-locked recorder never gives him one).

What this module does. It is a SECOND observational recorder that runs next to player_box.BoxRecorder on the same
snaps. The engine still draws the same rows with the same RNG; game results, the existing yard ledger and the
name-locked box are byte-identical with this model on or off. Only the attribution of each sampled opportunity changes:

  slot         rows                                                           candidates
  dropback     pass rows (attempts and sacks), QB scrambles / designed QB    QBs (and any player with passer rows)
               runs (qb_scramble == 1 or the original rusher is a QB),
               kneels and spikes
  carry        other run rows                                                 non-QB rushers
  target       pass rows that had a receiver (or were completions)            receivers

For each trial and team: (1) availability draw: a candidate listed Questionable/Doubtful on the point-in-time injury
report plays with the fitted probability for that status (Out players are not candidates at all); (2) the shares of
players who do not play are redistributed by the fitted rule `redistribute` (a fraction alpha to the same position
group in proportion to share, the rest to everyone in proportion to share); (3) the trial's share vector is a
Dirichlet draw around those shares with the fitted concentration kappa (game-to-game role noise). For each snap in the
slot the player is drawn with probability  pi_p * L_p(f)  normalised, where f is the snap's feature cell (zone at the
LIVE state x depth/yards bucket x result) and L_p is the player's empirical-Bayes feature distribution
(n_pf + m * prior_pos(f)) / (n_p + m), prior_pos fitted on league rows before the eval week. So every listed player can
record any event (INT, TD, deep target) with a probability shrunk toward his position prior, and the per-player yard
profile is kept (a deep receiver still gets more deep rows).

All randomness comes from this recorder's own numpy Generator (seeded from the run seed and SALT), never from the
engine RNG. Team totals are untouched, so per trial the sum of player lines equals the name-locked team ledger exactly
(checked in reconcile()). UNLISTED is the bucket for opportunities going to players outside the candidate list
(fitted share; e.g. a call-up) and is credited as its own line. Defensive credits (sacks_made, def_int) keep the name-locked rule.

The model dict is built by calibration/opportunity_fit.py (fit only on data before the eval week) and is plain JSON.
Research only. projection_ready stays false."""
from __future__ import annotations
from typing import Optional

import numpy as np

from player_box import BoxRecorder, _int, _name, RECON_CHECKS as _BASE_CHECKS

SCHEMA = "nfl75-opportunity/1"
SALT = 75_002  # mixed into the opportunity RNG seed so it never coincides with the engine stream
SLOTS = ("dropback", "carry", "target")
UNLISTED = "UNLISTED"
POS_GROUPS = {"QB": "QB", "RB": "RB", "FB": "RB", "HB": "RB", "WR": "WR", "TE": "TE"}
EXTRA_STATS = ("rz_targets", "i5_targets", "rz_carries", "i5_carries")
RECON_CHECKS = tuple(c for c in _BASE_CHECKS if not c.endswith("_eq_engine_ledger")) + ("team_ledger_eq_name_locked",)


# ------------------------------------------------------------------ feature cells (shared with the fitter)
def zone(y0) -> str:
    y0 = int(y0)
    return "i5" if y0 <= 5 else ("rz" if y0 <= 20 else "op")


def depth(air) -> str:
    try:
        a = float(air)
    except (TypeError, ValueError):
        return "u"
    if a != a:
        return "u"
    return "bl" if a < 0 else ("s" if a < 10 else ("m" if a < 20 else "d"))


def ybin(yards) -> str:
    y = float(yards)
    return "le0" if y <= 0 else ("1_3" if y < 4 else ("4_9" if y < 10 else "10p"))


def feat_target(y0, air, complete: bool, td: bool, is_int: bool) -> str:
    res = "int" if is_int else ("td" if td else ("comp" if complete else "inc"))
    return f"{zone(y0)}|{depth(air)}|{res}"


def feat_carry(y0, yards, td: bool) -> str:
    return f"{zone(y0)}|{ybin(yards)}|{'td' if td else 'no'}"


def feat_dropback(y0, kind: str) -> str:
    """kind: comp, inc, int, sack, td, run (scramble / QB run)."""
    return f"{zone(y0)}|{kind}"


def group(pos) -> str:
    return POS_GROUPS.get(str(pos), "OTH")


# ------------------------------------------------------------------ the documented redistribution rule
def redistribute(shares, positions, out_mask, alpha: float) -> np.ndarray:
    """shares: base shares (sum 1, UNLISTED included with position 'UNLISTED'); out_mask: True = does not play.
    Each out player's share s goes alpha*s to the remaining players of his position group (in proportion to their
    shares) and (1-alpha)*s to all remaining players (in proportion to their shares). If his group has nobody left,
    all of s goes to everyone remaining. If nobody remains, everything goes to UNLISTED (or uniform)."""
    s = np.asarray(shares, dtype=float).copy()
    out = np.asarray(out_mask, dtype=bool)
    if not out.any():
        return s / s.sum() if s.sum() > 0 else s
    grp = np.array([group(p) if p != UNLISTED else UNLISTED for p in positions])
    keep = ~out
    new = np.where(keep, s, 0.0)
    if not keep.any() or new.sum() <= 0:
        r = np.zeros_like(s)
        if UNLISTED in positions:
            r[list(positions).index(UNLISTED)] = 1.0
        else:
            r[:] = 1.0 / len(s)
        return r
    base_all = new / new.sum()
    add = np.zeros_like(s)
    for i in np.where(out)[0]:
        same = keep & (grp == grp[i])
        if same.any() and new[same].sum() > 0:
            w_same = np.where(same, new, 0.0) / new[same].sum()
            add += alpha * s[i] * w_same + (1 - alpha) * s[i] * base_all
        else:
            add += s[i] * base_all
    r = new + add
    return r / r.sum()


def eb_lik(counts: dict, prior: dict, m: float) -> dict:
    """Empirical-Bayes feature distribution: (n_f + m*prior_f) / (n + m). prior must be strictly positive."""
    n = float(sum(counts.values()))
    return {f: (counts.get(f, 0.0) + m * p) / (n + m) for f, p in prior.items()}


# ------------------------------------------------------------------ recorder
class _Row(dict):
    """Proxy row for BoxRecorder.snap: same keys, offense forced to the live offense, names replaced."""


class OpportunityRecorder(BoxRecorder):
    def __init__(self, home: str, away: str, lookup: Optional[dict], model: dict, rng: np.random.Generator,
                 opp_lookup: Optional[dict] = None, name_locked: Optional[BoxRecorder] = None):
        super().__init__(home=home, away=away, lookup=lookup)
        self.model, self.rng = model, rng
        self.opp_lookup = opp_lookup or {}
        self.name_locked = name_locked
        self.qb_ids = set(model.get("qb_ids", ()))
        self._fum_map: dict = {}
        self.pi: dict = {}
        self.lik: dict = {}
        self.active: dict = {}
        for t in (home, away):
            tm = model["teams"].get(t)
            if tm is None:
                raise KeyError(f"opportunity model has no team {t}")
            for slot in SLOTS:
                sm = tm["slots"][slot]
                names, pos = list(sm["players"]), list(sm["pos"])
                base = np.asarray(sm["share"], dtype=float)
                avail = np.asarray(sm.get("avail", [1.0] * len(names)), dtype=float)
                # same availability draw for a player across slots: one uniform per (team, player) per trial
                out = np.zeros(len(names), dtype=bool)
                for i, nm in enumerate(names):
                    if avail[i] < 1.0:
                        key = (t, nm)
                        if key not in self.active:
                            self.active[key] = bool(self.rng.random() < avail[i])
                        out[i] = not self.active[key]
                if sm.get("mode") == "starter":
                    pi = self._starter_pi(names, base, out, sm)
                    self.pi[(t, slot)] = (names, pi)
                    self._lik_rows(t, slot, tm, names, pos)
                    continue
                s = redistribute(base, pos, out, float(sm["alpha"]))
                kappa = sm.get("kappa")
                if kappa is not None and np.isfinite(kappa) and kappa > 0:
                    a = np.maximum(s * float(kappa), 1e-9)
                    pi = self.rng.dirichlet(a)
                    pi[s <= 0] = 0.0
                    pi = pi / pi.sum() if pi.sum() > 0 else s
                else:
                    pi = s
                self.pi[(t, slot)] = (names, pi)
                self._lik_rows(t, slot, tm, names, pos)

    def _lik_rows(self, t, slot, tm, names, pos):
        lk = tm["lik"][slot]
        floor = float(lk.get("floor", 1e-6))
        prior = lk["prior"]
        rows = []
        for nm, p in zip(names, pos):
            d = lk["players"].get(nm)
            if d is None:
                d = prior.get(group(p) if nm != UNLISTED else UNLISTED) or prior.get("ALL") or {}
            rows.append(d)
        self.lik[(t, slot)] = (rows, floor)

    def _starter_pi(self, names, base, out, sm) -> np.ndarray:
        """Dropback slot, starter mixture (fitted in calibration/opportunity_fit.fit_starter): one starter per trial
        drawn with P ~ share^start_gamma (x exp(beta_last) for last game's top passer, x exp(beta_dc) for the point-in-time depth-chart QB1) among players who play (UNLISTED with u_start); he takes rho of the
        dropbacks, the rest is spread over the other players who play in proportion to share."""
        s = np.asarray(base, dtype=float)
        unl = np.array([n == UNLISTED for n in names])
        avail = ~np.asarray(out, dtype=bool)
        u = float(sm["u_start"])
        w = np.where(avail & ~unl, np.maximum(s, 0.0) ** float(sm["start_gamma"]), 0.0)
        if sm.get("last_top") in names:  # most dropbacks in the team's most recent game: exp(beta_last) boost
            w[names.index(sm["last_top"])] *= float(np.exp(float(sm.get("beta_last", 0.0))))
        u_w = u
        dq = sm.get("depth_qb1")  # point-in-time depth-chart QB1: exp(beta_dc) boost (UNLISTED if not a candidate)
        if dq == UNLISTED:
            u_w = u * float(np.exp(float(sm.get("beta_dc", 0.0))))
        elif dq in names:
            w[names.index(dq)] *= float(np.exp(float(sm.get("beta_dc", 0.0))))
        p = np.zeros(len(s))
        if w.sum() > 0:
            p = (1 - u) * w / w.sum()
            p[unl] = u_w
        else:
            p[unl] = 1.0
        if p.sum() <= 0:
            return np.full(len(s), 1.0 / len(s))
        i = int(np.searchsorted(np.cumsum(p / p.sum()), self.rng.random(), side="right"))
        i = min(i, len(s) - 1)
        rest = np.where(avail, np.maximum(s, 0.0), 0.0)
        rest[i] = 0.0
        pi = np.zeros(len(s))
        if rest.sum() > 0:
            pi = (1 - float(sm["rho"])) * rest / rest.sum()
        pi[i] = float(sm["rho"]) if rest.sum() > 0 else 1.0
        return pi

    # -- drawing
    def _draw(self, team: str, slot: str, feat: Optional[str]) -> Optional[str]:
        names, pi = self.pi[(team, slot)]
        if not names:
            return None
        if feat is None:
            w = pi
        else:
            rows, floor = self.lik[(team, slot)]
            w = pi * np.array([r.get(feat, floor) for r in rows])
        tot = w.sum()
        if tot <= 0:
            w, tot = pi, pi.sum()
            if tot <= 0:
                return None
        u = self.rng.random() * tot
        i = int(np.searchsorted(np.cumsum(w), u, side="right"))
        return names[min(i, len(names) - 1)]  # UNLISTED is credited as its own line

    def _look(self, row) -> dict:
        lk = super()._look(row)
        if lk and "fumbled_1_player_name" in lk:
            lk = dict(lk)
            f = lk["fumbled_1_player_name"]
            lk["fumbled_1_player_name"] = self._fum_map.get(f)  # original carrier -> assigned player; else None
            if lk["fumbled_1_player_name"] is None:
                del lk["fumbled_1_player_name"]
        return lk

    def _orig(self, row) -> dict:
        try:
            gid, pid = row.get("game_id"), row.get("play_id")
            if gid is None or pid is None or pid != pid:
                return {}
            return self.opp_lookup.get((str(gid), int(pid)), {})
        except (TypeError, ValueError):
            return {}

    # -- the hook (same call site and pre-play state as BoxRecorder.snap)
    def snap(self, st, row, play_type: str, yards: float) -> None:
        off = st.possession
        y0 = int(st.yardline_100)
        is_int = _int(row, "interception") == 1
        is_fum = (not is_int) and _int(row, "fumble_lost") == 1
        turnover = is_int or is_fum
        safety = (not turnover) and (y0 - yards) >= 100
        td = (not turnover) and (not safety) and (y0 - yards) <= 0
        org = self._orig(row)
        base_lk = BoxRecorder._look(self, row)
        prow = _Row({k: row.get(k) for k in ("posteam", "defteam", "game_id", "play_id", "complete_pass",
                                              "interception", "fumble_lost", "sack")})
        prow["posteam"] = off
        orig_names = {c: (_name(row.get(c)) or _name(org.get(c)) or _name(base_lk.get(c)))
                      for c in ("passer_player_name", "rusher_player_name", "receiver_player_name")}
        new = {"passer_player_name": None, "rusher_player_name": None, "receiver_player_name": None}
        if play_type == "pass":
            complete = _int(row, "complete_pass") == 1
            if _int(row, "sack") == 1:
                new["passer_player_name"] = self._draw(off, "dropback", feat_dropback(y0, "sack"))
            else:
                kind = "int" if is_int else ("td" if td else ("comp" if complete else "inc"))
                new["passer_player_name"] = self._draw(off, "dropback", feat_dropback(y0, kind))
                had_rec = (orig_names["receiver_player_name"] is not None) or complete
                if had_rec:
                    new["receiver_player_name"] = self._draw(
                        off, "target", feat_target(y0, row.get("air_yards"), complete, td, is_int))
        elif play_type == "run":
            rid = org.get("rusher_player_id")
            qb_run = _int(row, "qb_scramble") == 1 or (rid is not None and rid in self.qb_ids)
            if qb_run:
                new["rusher_player_name"] = self._draw(off, "dropback", feat_dropback(y0, "run"))
            else:
                new["rusher_player_name"] = self._draw(off, "carry", feat_carry(y0, yards, td))
        elif play_type == "qb_kneel":
            new["rusher_player_name"] = self._draw(off, "dropback", None)
        elif play_type == "qb_spike":
            new["passer_player_name"] = self._draw(off, "dropback", None)
        prow.update(new)
        # fumbler: the original carrier's assigned replacement
        self._fum_map = {}
        for c in new:
            if orig_names[c] is not None:
                self._fum_map[orig_names[c]] = new[c]
        super().snap(st, prow, play_type, yards)
        # red-zone / inside-5 opportunity lines (extra stats; not part of the name-locked ledger comparison)
        z = zone(y0)
        if z != "op":
            if play_type == "pass" and _int(row, "sack") == 0 and (
                    orig_names["receiver_player_name"] is not None or _int(row, "complete_pass") == 1):
                self._p(off, new["receiver_player_name"], "rz_targets")
                if z == "i5":
                    self._p(off, new["receiver_player_name"], "i5_targets")
            elif play_type == "run":
                self._p(off, new["rusher_player_name"], "rz_carries")
                if z == "i5":
                    self._p(off, new["rusher_player_name"], "i5_carries")

    def reconcile(self, st) -> list[str]:
        bad = [b for b in super().reconcile(st) if "_eq_engine_ledger" not in b]
        if self.name_locked is not None:
            for t in (self.home, self.away):
                a, b = self.team.get(t, {}), self.name_locked.team.get(t, {})
                keys = (set(a) | set(b)) - set(EXTRA_STATS)
                if any(float(a.get(k, 0)) != float(b.get(k, 0)) for k in keys):
                    bad.append(f"team_ledger_eq_name_locked:{t}")
        return bad


def load_opp_lookup(pbp_path, game_ids) -> dict:
    """(game_id, play_id) -> original ids/names the engine may have nulled (foreign rows). Read-only side table."""
    from pathlib import Path
    path = Path(pbp_path)
    if not path.exists():
        return {}
    import pandas as pd
    import pyarrow.parquet as pq
    have = set(pq.ParquetFile(path).schema_arrow.names)
    want = ["rusher_player_id", "passer_player_name", "rusher_player_name", "receiver_player_name"]
    cols = ["game_id", "play_id"] + [c for c in want if c in have]
    df = pd.read_parquet(path, columns=cols)
    df = df[df["game_id"].isin(set(game_ids))]
    out = {}
    for rec in df.to_dict("records"):
        pid = rec.pop("play_id")
        if pid is None or pid != pid:
            continue
        out[(str(rec.pop("game_id")), int(pid))] = {k: v for k, v in rec.items() if _name(v)}
    return out
