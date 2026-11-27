"""Rule 1, TARGETS FIRST (flag only).

A WR/TE receiving leg needs a real target share over recent games:
  * WR: >= 20% of team targets over the window.
  * TE: a top-two target on the team over the window (ties at rank 2 count).
A low-share player ("mostly just on the field") counts only when the opposing defense allows a lot to his role
(yards-per-game rank <= 10 of 32 vs TE / RB / slot WR / outside WR, prior weeks only). Slot vs outside alignment
has no free source in the repo, so a WR's role exception is "unknown" and can never make him PASS.

Window: the player's last 4 games before the leg's week in which he recorded a target or carry in play-by-play
(an appearance proxy; snap-level "active" is not used), needs >= 3. Team targets are counted in those same games.
Statuses: PASS | PASS_ROLE_EXCEPTION | FLAG_LOW_TARGET_SHARE | INSUFFICIENT_HISTORY | NOT_APPLICABLE.
A flag never cuts (CUTS_ENABLED["targets_first"] is False). Research only.
"""
from __future__ import annotations

import pandas as pd

from pipeline.read_rules import UNKNOWN
from pipeline.read_rules.common import clean_plays
from pipeline.read_rules.defense_allowed import SOFT_RANK, soft_vs_role, role_of

WR_SHARE_MIN = 0.20
TE_TOP_N = 2
LAST_N, NEED = 4, 3
RECEIVING_MARKETS = ("recyds", "rec", "rushrec")
PASS, PASS_EXC, FLAG_LOW, INSUFF, NA = ("PASS", "PASS_ROLE_EXCEPTION", "FLAG_LOW_TARGET_SHARE",
                                        "INSUFFICIENT_HISTORY", "NOT_APPLICABLE")


def target_table(pbp: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(player rows: week, game_id, posteam, gsis, targets, carries) and (team rows: game_id, posteam, team_targets)."""
    p = clean_plays(pbp)
    pa = p[(p.pass_attempt == 1) & p.receiver_player_id.notna() & p.posteam.notna()]
    tt = pa.groupby(["game_id", "posteam"]).size().rename("team_targets").reset_index()
    t = (pa.groupby(["week", "game_id", "posteam", "receiver_player_id"]).size().rename("targets").reset_index()
         .rename(columns={"receiver_player_id": "gsis"}))
    ru = p[(p.rush_attempt == 1) & p.rusher_player_id.notna() & p.posteam.notna()]
    c = (ru.groupby(["week", "game_id", "posteam", "rusher_player_id"]).size().rename("carries").reset_index()
         .rename(columns={"rusher_player_id": "gsis"}))
    pl = t.merge(c, how="outer", on=["week", "game_id", "posteam", "gsis"]).fillna({"targets": 0, "carries": 0})
    return pl, tt


def evaluate(gsis: str, week: int, position: str | None, opponent: str | None, players: pd.DataFrame,
             team_targets: pd.DataFrame, roles: pd.DataFrame | None = None, role: str | None = None) -> dict:
    pos = (position or "").upper()
    out = dict(rule="targets_first", gsis=gsis, week=week, position=pos or UNKNOWN, flag_only=True,
               share=UNKNOWN, team_rank=UNKNOWN, n_games=0, window_weeks=[], role_exception=UNKNOWN)
    if pos not in ("WR", "TE"):
        out.update(status=NA, note="rule names WR/TE receiving legs only")
        return out
    h = players[(players.gsis == gsis) & (players.week < week)].sort_values("week").tail(LAST_N)
    out["n_games"] = int(len(h))
    out["window_weeks"] = [int(w) for w in h.week]
    if len(h) < NEED:
        out.update(status=INSUFF, note=f"needs >= {NEED} prior games, has {len(h)}")
        return out
    keys = h[["game_id", "posteam"]]
    tt = keys.merge(team_targets, on=["game_id", "posteam"], how="left").team_targets.sum()
    share = float(h.targets.sum() / tt) if tt > 0 else None
    out["share"] = round(share, 4) if share is not None else UNKNOWN
    out["player_targets"], out["team_targets"] = int(h.targets.sum()), int(tt)
    mates = players.merge(keys, on=["game_id", "posteam"]).groupby("gsis").targets.sum()
    rank = int(mates.rank(ascending=False, method="min").get(gsis, 0)) or None
    out["team_rank"] = rank if rank else UNKNOWN
    passes = (pos == "WR" and share is not None and share >= WR_SHARE_MIN - 1e-12) or (
        pos == "TE" and rank is not None and rank <= TE_TOP_N)
    if passes:
        out.update(status=PASS, note=("WR share >= 20%" if pos == "WR" else "TE top-two team target"))
        return out
    use_role = role or role_of(pos)
    if pos == "WR" and role is None:
        use_role = None   # alignment (slot/outside) unknown: the role exception cannot be checked
    soft = soft_vs_role(roles, opponent, use_role) if (roles is not None and opponent) else UNKNOWN
    out["role_exception"] = soft
    out["role_checked"] = use_role or UNKNOWN
    if soft == "soft":
        out.update(status=PASS_EXC, note=f"low share, but {opponent} is top-{SOFT_RANK} in yards allowed to {use_role}")
    else:
        out.update(status=FLAG_LOW, note=("low share; role exception " + ("not met" if soft == "not_soft" else "unknown")))
    return out
