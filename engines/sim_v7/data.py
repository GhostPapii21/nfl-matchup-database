"""sim_v7 data layer: leak-free, as-of-cutoff team/player/drive contexts from nflverse pbp (2024-2026).

Every context is built only from plays with game_date < cutoff. Nothing here reads a future game.
"""
from __future__ import annotations

import glob
import hashlib
import json
import os
import re
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PBP_FILES = {
    2024: "data/historical/nflverse/play_by_play_2024.parquet",
    2025: "fixtures/week8/phase_walk/src/pbp25.parquet",
    2026: "data/historical/nflverse/pbp_2026_w1_11_pulled_20261124T1717ET.parquet",
}
PLAYERS_FILE = "fixtures/players.parquet"
GAMES_FILE = "data/historical/nflverse/games.csv"
NV = {"LAR": "LA", "WSH": "WAS", "JAC": "JAX"}

COLS = [
    "game_id", "season", "week", "game_date", "season_type", "home_team", "away_team", "posteam", "defteam",
    "fixed_drive", "fixed_drive_result", "drive_time_of_possession", "qtr", "score_differential",
    "posteam_score", "defteam_score", "posteam_score_post", "defteam_score_post",
    "play_type", "pass_attempt", "rush_attempt", "sack", "two_point_attempt", "complete_pass",
    "passer_player_id", "receiver_player_id", "rusher_player_id",
    "passing_yards", "receiving_yards", "rushing_yards", "pass_touchdown", "rush_touchdown", "td_player_id",
    "yardline_100", "total_home_score", "total_away_score", "home_score", "away_score",
]

_CACHE: dict = {}


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_pbp() -> pd.DataFrame:
    if "pbp" in _CACHE:
        return _CACHE["pbp"]
    frames = []
    for season, rel in PBP_FILES.items():
        p = pd.read_parquet(os.path.join(REPO, rel), columns=COLS)
        frames.append(p[p.season_type == "REG"])
    p = pd.concat(frames, ignore_index=True)
    p["game_date"] = p["game_date"].astype(str)
    _CACHE["pbp"] = p
    return p


def load_players() -> pd.DataFrame:
    if "players" not in _CACHE:
        _CACHE["players"] = pd.read_parquet(os.path.join(REPO, PLAYERS_FILE),
                                            columns=["gsis_id", "display_name", "position_group", "latest_team"])
    return _CACHE["players"]


def provenance() -> dict:
    if "prov" not in _CACHE:
        files = {**{str(k): v for k, v in PBP_FILES.items()}, "players": PLAYERS_FILE}
        _CACHE["prov"] = {k: {"path": v, "sha256": sha256_file(os.path.join(REPO, v))} for k, v in files.items()}
    return _CACHE["prov"]


def lock_game_ids() -> set[str]:
    """Every game_id named in a frozen evaluation lock file. These are excluded from calibration fitting/validation."""
    ids: set[str] = set()
    pat = re.compile(r"20\d\d_\d\d_[A-Z]{2,3}_[A-Z]{2,3}")
    for f in glob.glob(os.path.join(REPO, "**", "*LOCK*.json"), recursive=True):
        try:
            ids.update(pat.findall(open(f, encoding="utf-8", errors="ignore").read()))
        except OSError:
            pass
        ids.update(pat.findall(f))
    return ids


def _secs(s) -> float:
    try:
        m, ss = str(s).split(":")
        return float(m) * 60 + float(ss)
    except Exception:
        return np.nan


@dataclass
class TeamContext:
    team: str
    cutoff: str
    game_ids: list
    games: pd.DataFrame            # per team-game: pa, ra, pts, td, fg, pass_td, rush_td, q1..q4 pts, margin
    players: pd.DataFrame          # modeled players: gsis, name, pos, role
    pgame: pd.DataFrame            # per player-game stats (modeled players, all games in window)
    drives: pd.DataFrame           # per drive: dur, off_pts, def_pts, state, half, pa, ra + player stat columns
    drive_cols: list
    rec_yards: dict                # gsis -> array of yards per reception (window)
    rush_yards: dict               # gsis -> array of yards per carry (window)
    rz: dict                       # gsis -> (rz targets, rz carries)
    league: dict = field(default_factory=dict)


STATS = ("tgt", "rec", "recyds", "rectd", "car", "rushyds", "rushtd", "att", "cmp", "passyds", "passtd")


def _player_stats(df: pd.DataFrame, keys: list) -> pd.DataFrame:
    """Aggregate per-player stats over grouping keys (e.g. game_id or game_id+fixed_drive)."""
    df = df.assign(receiving_yards=df.receiving_yards.fillna(0), rushing_yards=df.rushing_yards.fillna(0),
                   passing_yards=df.passing_yards.fillna(0))
    pas = df[(df.pass_attempt == 1) & (df.sack != 1)]
    ru = df[df.rush_attempt == 1]
    r = pas.groupby(keys + ["receiver_player_id"]).agg(
        tgt=("pass_attempt", "size"), rec=("complete_pass", "sum"),
        recyds=("receiving_yards", "sum"), rectd=("pass_touchdown", "sum")).reset_index()
    r = r.rename(columns={"receiver_player_id": "gsis"})
    u = ru.groupby(keys + ["rusher_player_id"]).agg(
        car=("rush_attempt", "size"), rushyds=("rushing_yards", "sum"),
        rushtd=("rush_touchdown", "sum")).reset_index().rename(columns={"rusher_player_id": "gsis"})
    q = pas.groupby(keys + ["passer_player_id"]).agg(
        att=("pass_attempt", "size"), cmp=("complete_pass", "sum"),
        passyds=("passing_yards", "sum"), passtd=("pass_touchdown", "sum")).reset_index()
    q = q.rename(columns={"passer_player_id": "gsis"})
    out = r.merge(u, on=keys + ["gsis"], how="outer").merge(q, on=keys + ["gsis"], how="outer")
    out = out[out.gsis.notna()]
    for c in STATS:
        if c not in out:
            out[c] = 0.0
        out[c] = out[c].fillna(0).astype(float)
    return out


def _quarter_points(g: pd.DataFrame, team: str) -> dict:
    """Regulation quarter points for team in one game from cumulative totals (OT folded out)."""
    home = g.home_team.iloc[0] == team
    col = "total_home_score" if home else "total_away_score"
    out, prev = {}, 0.0
    for q in (1, 2, 3, 4):
        s = g[g.qtr <= q][col].max()
        s = prev if s != s else float(s)
        out[f"q{q}"] = s - prev
        prev = s
    return out


def league_params(cutoff: str) -> dict:
    """League-wide priors and slopes, fitted only on plays before cutoff (last ~2 seasons)."""
    key = ("league", cutoff)
    if key in _CACHE:
        return _CACHE[key]
    p = load_pbp()
    p = p[(p.game_date < cutoff) & (p.two_point_attempt != 1)]
    yrs = sorted(p.season.unique())[-2:]
    p = p[p.season.isin(yrs)]
    pas = p[(p.pass_attempt == 1) & (p.sack != 1)]
    ru = p[p.rush_attempt == 1]
    pa =pas.groupby(["game_id", "posteam"]).size().rename("pa")
    ra = ru.groupby(["game_id", "posteam"]).size().rename("ra")
    fin = p.groupby("game_id").agg(h=("home_team", "first"), hs=("home_score", "max"), as_=("away_score", "max"))
    tg = pd.concat([pa, ra], axis=1).dropna().reset_index().merge(fin.reset_index(), on="game_id")
    tg["margin"] = np.where(tg.posteam == tg.h, tg.hs - tg.as_, tg.as_ - tg.hs)
    tg["pts"] = np.where(tg.posteam == tg.h, tg.hs, tg.as_)
    bP = float(np.polyfit(tg.margin, np.log(tg.pa), 1)[0])
    bR = float(np.polyfit(tg.margin, np.log(tg.ra), 1)[0])
    pos = load_players().set_index("gsis_id").position_group.to_dict()
    pas = pas.assign(pg=pas.receiver_player_id.map(pos))
    comp = pas[pas.complete_pass == 1]
    lg = dict(bP=bP, bR=bR, cutoff=cutoff, seasons=[int(y) for y in yrs])
    lg["cr"] = {k: float(v) for k, v in pas.groupby("pg").complete_pass.mean().items()}
    lg["ypr"] = {k: float(v) for k, v in comp.groupby("pg").receiving_yards.mean().items()}
    lg["ypr_var"] = {k: float(v) for k, v in comp.groupby("pg").receiving_yards.var().items()}
    lg["ypc"] = float(ru.rushing_yards.mean())
    lg["ypc_var"] = float(ru.rushing_yards.var())
    lg["cr_all"] = float(pas.complete_pass.mean())
    lg["ypr_all"] = float(comp.receiving_yards.mean())
    lg["ypr_var_all"] = float(comp.receiving_yards.var())
    # team-game efficiency dispersion (log yards per play), used for the shared efficiency shock
    yp = (pas.groupby(["game_id", "posteam"]).receiving_yards.sum() + ru.groupby(["game_id", "posteam"]).rushing_yards.sum())
    pl = pas.groupby(["game_id", "posteam"]).size() + ru.groupby(["game_id", "posteam"]).size()
    lg["sd_log_ypp"] = float(np.nanstd(np.log((yp / pl).clip(lower=0.5))))
    lg["pts_mean"] = float(tg.pts.mean())
    # opponent allowances by position group (ratio to league), and defence points allowed
    lg["opp_cr"] = {}
    lg["opp_ypt"] = {}
    for (d, pg), x in pas.groupby(["defteam", "pg"]):
        base = pas[pas.pg == pg]
        if len(x) >= 25 and len(base):
            lg["opp_cr"][(d, pg)] = float(x.complete_pass.mean() / base.complete_pass.mean())
            lg["opp_ypt"][(d, pg)] = float(x.receiving_yards.fillna(0).mean() / base.receiving_yards.fillna(0).mean())
    lg["opp_ypc"] = {d: float(x.rushing_yards.mean() / ru.rushing_yards.mean()) for d, x in ru.groupby("defteam") if len(x) >= 60}
    _CACHE[key] = lg
    return lg


def team_context(team: str, cutoff: str, n_games: int = 8, exclude: set | None = None,
                 max_rec: int = 8, max_rush: int = 4) -> TeamContext:
    team = NV.get(team, team)
    key = ("team", team, cutoff, n_games, tuple(sorted(exclude or ())))
    if key in _CACHE:
        return _CACHE[key]
    P = load_pbp()
    p = P[(P.game_date < cutoff) & (P.posteam == team)]
    gids = (p.groupby("game_id").game_date.first().sort_values().index.tolist())[-n_games:]
    if len(gids) < 3:
        raise ValueError(f"{team}: fewer than 3 games before {cutoff}")
    p = p[p.game_id.isin(gids)]
    full = P[P.game_id.isin(gids)]
    s = p[p.two_point_attempt != 1]
    pos = load_players().set_index("gsis_id")
    pg = _player_stats(s, ["game_id"])
    # --- modeled players: usage in the last 3 team games
    last3 = gids[-3:]
    u3 = pg[pg.game_id.isin(last3)].groupby("gsis")[["tgt", "car", "att"]].sum()
    u3 = u3[~u3.index.isin(exclude or set())]
    qb = u3.att.idxmax()
    recv = u3[(u3.tgt > 0) & (u3.index != qb)].sort_values("tgt", ascending=False).head(max_rec).index.tolist()
    rush = u3[(u3.car > 0) & (u3.index != qb)].sort_values("car", ascending=False).head(max_rush).index.tolist()
    ids = [qb] + list(dict.fromkeys(recv + rush))
    players = pd.DataFrame({"gsis": ids})
    players["name"] = players.gsis.map(pos.display_name).fillna(players.gsis)
    players["pos"] = players.gsis.map(pos.position_group).fillna("WR")
    players.loc[players.gsis == qb, "pos"] = "QB"
    players["role"] = ["QB"] + ["SKILL"] * (len(ids) - 1)
    # --- team games
    rows = []
    for gid in gids:
        g = full[full.game_id == gid]
        gg = s[s.game_id == gid]
        home = g.home_team.iloc[0] == team
        pts = float(g.home_score.iloc[0] if home else g.away_score.iloc[0])
        opp_pts = float(g.away_score.iloc[0] if home else g.home_score.iloc[0])
        pas = gg[(gg.pass_attempt == 1) & (gg.sack != 1)]
        rows.append(dict(game_id=gid, date=g.game_date.iloc[0], opp=(g.away_team.iloc[0] if home else g.home_team.iloc[0]),
                         pa=len(pas), ra=int((gg.rush_attempt == 1).sum()), pts=pts, opp_pts=opp_pts, margin=pts - opp_pts,
                         pass_td=float(gg.pass_touchdown.sum()), rush_td=float(gg.rush_touchdown.sum()),
                         fg=float(g[(g.posteam == team) & (g.fixed_drive_result == "Field goal")].fixed_drive.nunique()),
                         **_quarter_points(g, team)))
    games = pd.DataFrame(rows)
    games["td"] = games.pass_td + games.rush_td
    # --- per-drive table (possession engine)
    d = p.groupby(["game_id", "fixed_drive"]).agg(
        result=("fixed_drive_result", "first"), top=("drive_time_of_possession", "first"), qtr=("qtr", "min"),
        state=("score_differential", "first"), s0=("posteam_score", "min"), s1=("posteam_score_post", "max"),
        d0=("defteam_score", "min"), d1=("defteam_score_post", "max")).reset_index()
    d["dur"] = d.top.map(_secs).fillna(120.0).clip(10, 600)
    d["off_pts"] = (d.s1 - d.s0).clip(0, 8).fillna(0)
    d["def_pts"] = (d.d1 - d.d0).clip(0, 8).fillna(0)
    d["state"] = d.state.fillna(0)
    d["half"] = np.where(d.qtr <= 2, 1, 2)
    ds = _player_stats(s[s.gsis_any.isin(ids)] if "gsis_any" in s else s, ["game_id", "fixed_drive"])
    ds = ds[ds.gsis.isin(ids)]
    idx = pd.MultiIndex.from_frame(d[["game_id", "fixed_drive"]])
    wide = ds.set_index(["game_id", "fixed_drive", "gsis"])[list(STATS)].unstack("gsis").reindex(idx).fillna(0.0)
    cols, extra = [], {}
    for gs in ids:
        for c in STATS:
            name = f"{gs}|{c}"
            cols.append(name)
            extra[name] = wide[(c, gs)].to_numpy(float) if (c, gs) in wide.columns else np.zeros(len(d))
    dpas = s[(s.pass_attempt == 1) & (s.sack != 1)].groupby(["game_id", "fixed_drive"]).size()
    dra = s[s.rush_attempt == 1].groupby(["game_id", "fixed_drive"]).size()
    extra["pa"] = idx.map(dpas).fillna(0).astype(float).to_numpy()
    extra["ra"] = idx.map(dra).fillna(0).astype(float).to_numpy()
    d = pd.concat([d.reset_index(drop=True), pd.DataFrame(extra)], axis=1)
    # --- efficiency samples + red zone
    pas = s[(s.pass_attempt == 1) & (s.sack != 1)]
    ru = s[s.rush_attempt == 1]
    rec_y = {gs: pas[(pas.receiver_player_id == gs) & (pas.complete_pass == 1)].receiving_yards.dropna().values for gs in ids}
    rush_y = {gs: ru[ru.rusher_player_id == gs].rushing_yards.dropna().values for gs in ids}
    rzp, rzr = pas[pas.yardline_100 <= 20], ru[ru.yardline_100 <= 20]
    rz = {gs: (float((rzp.receiver_player_id == gs).sum()), float((rzr.rusher_player_id == gs).sum())) for gs in ids}
    rz["_team"] = (float(len(rzp)), float(len(rzr)))
    ctx = TeamContext(team, cutoff, gids, games, players, pg[pg.gsis.isin(ids)], d, cols, rec_y, rush_y, rz,
                      league_params(cutoff))
    _CACHE[key] = ctx
    return ctx


def actual_player_stats(game_id: str) -> pd.DataFrame:
    P = load_pbp()
    g = P[(P.game_id == game_id) & (P.two_point_attempt != 1)]
    return _player_stats(g, ["game_id"]).set_index("gsis")


def actual_game(game_id: str) -> dict:
    P = load_pbp()
    g = P[P.game_id == game_id]
    h, a = g.home_team.iloc[0], g.away_team.iloc[0]
    out = dict(home=h, away=a, home_pts=float(g.home_score.iloc[0]), away_pts=float(g.away_score.iloc[0]))
    out["home_q"] = _quarter_points(g, h)
    out["away_q"] = _quarter_points(g, a)
    return out


def context_hash(*objs) -> str:
    h = hashlib.sha256()
    h.update(json.dumps(provenance(), sort_keys=True).encode())
    for o in objs:
        h.update(json.dumps(o, sort_keys=True, default=str).encode())
    return h.hexdigest()
