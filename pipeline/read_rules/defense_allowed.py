"""Rule 2, DEFENSE-ALLOWED PROFILE (flag only). What each defense allows, for both teams in a game.

Walk-forward: every play-by-play figure uses only weeks < as_of_week. Each figure is {value, source, pulled_at};
a figure with no data is "unknown" (never 0) and can never cut a leg by itself.

Sources actually in the repo (verified Nov 26, 2026):
  * Sharp Football Analysis free coverage table -> data/coverage/sharp_coverage_2026.csv (man/zone, MOF closed/open;
    season-to-date as of its pulled_utc, so it is NOT point-in-time for past weeks).
  * nflverse play-by-play -> by-role catches/yards allowed, air-yard depth buckets, designed-run YPC, and DB events:
    PBU / INT / DPI are VERIFIED defender events; the tackler on a completion is INFERRED, never verified.
  * PFF free recap pages W1-8 (data/pff_captures_w1_8, no paid content) -> one featured "COVERAGE" card per game
    (INT, PBU, receptions/targets). Sparse; reported as-is.
  * NGS (data/ngs) has no defender or alignment fields, so it adds nothing here.
Slot WR vs outside WR needs alignment, which no free source in the repo has: those two are "unknown". A labelled
proxy by pass_location (middle vs left/right) is reported separately and is NOT called slot/outside.
"""
from __future__ import annotations

import csv
import re
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

from pipeline.read_rules import UNKNOWN
from pipeline.read_rules.common import PFF_DIR_DEFAULT, SHARP_DEFAULT, clean_plays, field

ROLES = ("TE", "RB", "WR", "slot_WR", "outside_WR", "WR_middle_proxy", "WR_outside_proxy")
ALIGNMENT_ROLES = ("slot_WR", "outside_WR")   # no free alignment source -> always unknown
SOFT_RANK = 10                                 # "allows a lot" = top-10 of 32 in yards allowed per game
DEPTHS = (("short", -99, 10), ("intermediate", 10, 20), ("deep", 20, 999))
DB_POS = ("CB", "S", "FS", "SS", "SAF", "NB", "DB")
DPI = "Defensive Pass Interference"


def _prior(pbp: pd.DataFrame, as_of_week: int) -> pd.DataFrame:
    return clean_plays(pbp[pbp.week < as_of_week])


def _games(p: pd.DataFrame) -> pd.Series:
    return p.dropna(subset=["defteam"]).groupby("defteam").game_id.nunique()


def _rank(s: pd.Series) -> pd.Series:
    """1 = allows the most. Teams with no data are absent (unknown), never ranked as 0."""
    return s.rank(ascending=False, method="min").astype("Int64")


def role_of(position: str | None, pass_location: str | None = None) -> str | None:
    pos = (position or "").upper()
    if pos in ("TE",):
        return "TE"
    if pos in ("RB", "FB"):
        return "RB"
    if pos == "WR":
        return "WR"
    return None


def role_allowed(pbp: pd.DataFrame, positions: dict, as_of_week: int) -> pd.DataFrame:
    """Per (defteam, role): games, targets, catches, yards, per-game and rank. Long format."""
    p = _prior(pbp, as_of_week)
    pa = p[(p.pass_attempt == 1) & p.receiver_player_id.notna() & p.defteam.notna()].copy()
    g = _games(p)
    pa["pos"] = pa.receiver_player_id.map(positions)
    pa["role"] = [role_of(x) for x in pa.pos]
    pa = pa[pa.role.notna()]
    pa["rec"] = pa.complete_pass.fillna(0)
    pa["yds"] = pa.receiving_yards.fillna(0).where(pa.complete_pass.fillna(0) == 1, 0)
    wr = pa[pa.role == "WR"]
    parts = [pa, wr.assign(role="WR_middle_proxy")[wr.pass_location == "middle"],
             wr.assign(role="WR_outside_proxy")[wr.pass_location.isin(["left", "right"])]]
    a = pd.concat(parts).groupby(["defteam", "role"]).agg(targets=("rec", "size"), rec=("rec", "sum"),
                                                          yds=("yds", "sum")).reset_index()
    a["games"] = a.defteam.map(g)
    for c in ("targets", "rec", "yds"):
        a[f"{c}_pg"] = a[c] / a.games
    a["yds_pg_rank"] = a.groupby("role").yds_pg.transform(_rank)
    a["rec_pg_rank"] = a.groupby("role").rec_pg.transform(_rank)
    a["n_teams_ranked"] = a.groupby("role").defteam.transform("size")
    return a


def depth_allowed(pbp: pd.DataFrame, as_of_week: int) -> pd.DataFrame:
    p = _prior(pbp, as_of_week)
    pa = p[(p.pass_attempt == 1) & p.air_yards.notna() & p.defteam.notna() & (p.sack.fillna(0) != 1)].copy()
    g = _games(p)
    pa["bucket"] = pd.cut(pa.air_yards, [-99, 10, 20, 999], right=False, labels=[d[0] for d in DEPTHS])
    pa["yds"] = pa.yards_gained.fillna(0).where(pa.complete_pass.fillna(0) == 1, 0)
    a = pa.groupby(["defteam", "bucket"], observed=True).agg(att=("yds", "size"), comp=("complete_pass", "sum"),
                                                             yds=("yds", "sum")).reset_index()
    a["games"] = a.defteam.map(g)
    a["yds_pg"] = a.yds / a.games
    a["comp_pct"] = a.comp / a.att
    a["yds_pg_rank"] = a.groupby("bucket", observed=True).yds_pg.transform(_rank)
    return a


def run_allowed(pbp: pd.DataFrame, as_of_week: int) -> pd.DataFrame:
    """Designed rushes only: rush_attempt, not a QB scramble, not a kneel."""
    p = _prior(pbp, as_of_week)
    r = p[(p.rush_attempt == 1) & (p.qb_scramble.fillna(0) != 1) & (p.qb_kneel.fillna(0) != 1) & p.defteam.notna()]
    a = r.groupby("defteam").agg(carries=("rushing_yards", "size"), yds=("rushing_yards", "sum")).reset_index()
    a["ypc"] = a.yds / a.carries
    a["ypc_rank"] = _rank(a.ypc)
    return a


def db_events(pbp: pd.DataFrame, positions: dict, as_of_week: int, defteam: str, top: int = 5) -> list[dict]:
    """Per DB of `defteam`: VERIFIED events (PBU, INT, DPI) and INFERRED catches/yards (first tackler on a completion)."""
    p = _prior(pbp, as_of_week)
    p = p[p.defteam == defteam]
    rows: dict[str, dict] = {}

    def bump(pid, name, k, v=1):
        if pid is None or (isinstance(pid, float) and np.isnan(pid)):
            return
        if positions.get(pid, "") not in DB_POS:
            return
        d = rows.setdefault(pid, dict(gsis=pid, name=name, position=positions.get(pid), pbu=0, int=0, dpi=0,
                                      inferred_catches=0, inferred_yards=0.0))
        d[k] += v
        if name and not d.get("name"):
            d["name"] = name

    for c in ("pass_defense_1", "pass_defense_2"):
        for pid, nm in zip(p[f"{c}_player_id"], p[f"{c}_player_name"]):
            bump(pid, nm, "pbu")
    for pid, nm in zip(p.interception_player_id, p.interception_player_name):
        bump(pid, nm, "int")
    dpi = p[p.penalty_type.fillna("") == DPI]
    for pid, nm in zip(dpi.penalty_player_id, dpi.penalty_player_name):
        bump(pid, nm, "dpi")
    comp = p[(p.complete_pass == 1)]
    tid = comp.solo_tackle_1_player_id.where(comp.solo_tackle_1_player_id.notna(), comp.assist_tackle_1_player_id)
    tnm = comp.solo_tackle_1_player_name.where(comp.solo_tackle_1_player_id.notna(), comp.assist_tackle_1_player_name)
    for pid, nm, y in zip(tid, tnm, comp.receiving_yards.fillna(0)):
        bump(pid, nm, "inferred_catches")
        bump(pid, nm, "inferred_yards", float(y))
    out = sorted(rows.values(), key=lambda d: (-d["inferred_yards"], -d["inferred_catches"]))[:top]
    for d in out:
        d["verified_events"] = d["pbu"] + d["int"] + d["dpi"]
        d["inferred_label"] = "inferred_from_tackler (not a verified coverage assignment)"
    return out


def sharp_row(team: str, path: Path | str | None = None) -> dict | None:
    p = Path(path) if path else SHARP_DEFAULT
    if not p.exists():
        return None
    with open(p, newline="") as f:
        for r in csv.DictReader(f):
            if r.get("team") == team:
                return r
    return None


NICK = {"Cardinals": "ARI", "Falcons": "ATL", "Ravens": "BAL", "Bills": "BUF", "Panthers": "CAR", "Bears": "CHI",
        "Bengals": "CIN", "Browns": "CLE", "Cowboys": "DAL", "Broncos": "DEN", "Lions": "DET", "Packers": "GB",
        "Texans": "HOU", "Colts": "IND", "Jaguars": "JAX", "Chiefs": "KC", "Raiders": "LV", "Chargers": "LAC",
        "Rams": "LA", "Dolphins": "MIA", "Vikings": "MIN", "Patriots": "NE", "Saints": "NO", "Giants": "NYG",
        "Jets": "NYJ", "Eagles": "PHI", "Steelers": "PIT", "49ers": "SF", "Seahawks": "SEA", "Buccaneers": "TB",
        "Titans": "TEN", "Commanders": "WAS"}
_CARD = re.compile(r"\n([^\n]+)\n([A-Za-z0-9]+)\nCOVERAGE\nINTERCEPTIONS\n(\d+)\nPASS BREAKUPS\n(\d+)\nTARGETS\n(\d+)/(\d+)\n")


def parse_pff_coverage_cards(text: str) -> list[dict]:
    """Featured COVERAGE cards on a PFF free recap page: name, team, INT, PBU, receptions allowed / targets."""
    out = []
    for name, nick, i, pbu, rec, tgt in _CARD.findall(text):
        out.append(dict(name=name.strip(), team=NICK.get(nick, UNKNOWN), int=int(i), pbu=int(pbu),
                        rec_allowed=int(rec), targets=int(tgt)))
    return out


@lru_cache(maxsize=4)
def pff_cards(pff_dir: str = str(PFF_DIR_DEFAULT)) -> pd.DataFrame:
    rows = []
    d = Path(pff_dir)
    for man in sorted(d.glob("week0*/manifest.csv")):
        meta = {r["game_id"]: r for r in csv.DictReader(open(man, newline=""))}
        for txt in sorted((man.parent / "games").glob("*_accessible-recap-text.txt")):
            gid = txt.name.split("_")[0]
            m = meta.get(gid, {})
            for c in parse_pff_coverage_cards(txt.read_text(errors="ignore")):
                rows.append(dict(c, week=int(m.get("week") or 0) or None, pff_game_id=gid,
                                 recap_url=m.get("recap_url", UNKNOWN), retrieved_at=m.get("retrieved_at_et", UNKNOWN)))
    return pd.DataFrame(rows)


def profile(defteam: str, as_of_week: int, pbp: pd.DataFrame, pbp_source: str, pbp_pulled: str, positions: dict,
            *, roles: pd.DataFrame | None = None, depth: pd.DataFrame | None = None, run: pd.DataFrame | None = None,
            sharp_path=None, pff_dir: str | None = None) -> dict:
    """Full defense-allowed profile for one defense. Every figure has a source and pull time."""
    roles = role_allowed(pbp, positions, as_of_week) if roles is None else roles
    depth = depth_allowed(pbp, as_of_week) if depth is None else depth
    run = run_allowed(pbp, as_of_week) if run is None else run
    src = f"{pbp_source}, weeks < {as_of_week}"
    out: dict = {"defteam": defteam, "as_of_week": as_of_week, "flag_only": True}

    sh = sharp_row(defteam, sharp_path)
    ssrc = "Sharp Football Analysis free coverage table (data/coverage/sharp_coverage_2026.csv; season-to-date, not point-in-time)"
    spt = sh.get("pulled_utc") if sh else None
    out["coverage"] = {k: field(sh.get(k) if sh else None, ssrc, spt) for k in ("mofc_pct", "mofo_pct", "man_pct", "zone_pct")}

    r = roles[roles.defteam == defteam].set_index("role")
    out["by_role"] = {}
    for role in ROLES:
        if role in ALIGNMENT_ROLES:
            out["by_role"][role] = {k: field(None, "no free alignment source in repo (slot/outside unknown)", None)
                                    for k in ("rec_pg", "yds_pg", "yds_pg_rank")}
            continue
        has = role in r.index
        rs = src + (" (proxy by pass_location; NOT slot/outside)" if "proxy" in role else "")
        out["by_role"][role] = {k: field(r.at[role, k] if has else None, rs, pbp_pulled)
                                for k in ("games", "targets", "rec", "yds", "rec_pg", "yds_pg", "yds_pg_rank", "rec_pg_rank")}

    d = depth[depth.defteam == defteam].set_index("bucket")
    out["by_depth"] = {b: {k: field(d.at[b, k] if b in d.index else None, src + " (air_yards: short <10, intermediate 10-19, deep >=20)",
                                    pbp_pulled) for k in ("att", "comp", "comp_pct", "yds", "yds_pg", "yds_pg_rank")}
                       for b, _, _ in DEPTHS}
    rr = run[run.defteam == defteam]
    out["run_defense"] = {k: field(rr[k].iloc[0] if len(rr) else None, src + " (designed rushes: no scrambles/kneels)", pbp_pulled)
                          for k in ("carries", "ypc", "ypc_rank")}
    dbs = db_events(pbp, positions, as_of_week, defteam)
    out["db_allowed"] = field(dbs if dbs else None, src + " (PBU/INT/DPI verified; catches/yards inferred from first tackler)",
                              pbp_pulled)
    cards = pff_cards(pff_dir or str(PFF_DIR_DEFAULT))
    if len(cards):
        c = cards[(cards.team == defteam) & (cards.week < as_of_week)]
        out["pff_featured_coverage"] = field(c.drop(columns=["team"]).to_dict("records") if len(c) else None,
                                             "PFF free game-recap featured COVERAGE card (one per game, W1-8 only; no paid content)",
                                             c.retrieved_at.max() if len(c) else None)
    else:
        out["pff_featured_coverage"] = field(None, "PFF free recap captures not found", None)
    return out


def soft_vs_role(roles: pd.DataFrame, defteam: str, role: str | None) -> str:
    """'soft' if yards-per-game rank <= SOFT_RANK for that role, 'not_soft' if ranked worse, else 'unknown'."""
    if role is None or role in ALIGNMENT_ROLES:
        return UNKNOWN
    r = roles[(roles.defteam == defteam) & (roles.role == role)]
    if not len(r) or pd.isna(r.yds_pg_rank.iloc[0]):
        return UNKNOWN
    return "soft" if r.yds_pg_rank.iloc[0] <= SOFT_RANK else "not_soft"
