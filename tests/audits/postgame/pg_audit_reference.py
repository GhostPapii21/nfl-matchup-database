"""Reference helpers for the postgame grading audit (docs/audits/postgame_grading_audit.md).

These are PROPOSALS that live next to the audit tests. Nothing in grading/, pregame/, evaluation/ or any model
imports this file, and it changes no weight, formula, betting rule, projection_ready flag or database.

What it shows, each piece independently testable:
  * participation_status(): read the official NFL game summary participation lists that data/gamebooks/ already
    parses (lineups.csv = starters, participation.csv = substitution / did_not_play / not_active) so a grader can
    tell "played and recorded 0" from "inactive" from "dressed but did not play" from "not on the game-day list".
  * settlement_status(): map that participation to a prop settlement class: graded (a 0 is a real 0), void
    (inactive / did not play), or unknown (no participation source). Rules here are the audit's proposal; the
    sportsbook-specific rule (most US books void a player prop when the player takes no snap) must be confirmed
    by Rico before anything is wired in.
  * name_key(): suffix-insensitive full-name key (Jr., Sr., II, III, IV, V dropped) for book-name vs box-name joins.
  * attribute_error(): split a count-times-rate stat miss into opportunity (volume) and efficiency (per-touch rate)
    parts, so a postgame row can say "missed on targets" vs "missed on yards per target".
Missing data is the string "unknown", never 0, matching grading/core.py.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

UNKNOWN = "unknown"
SUFFIXES = {"jr", "sr", "ii", "iii", "iv", "v"}

# participation classes, in the order a gamebook can evidence them
STARTED = "started"
SUBSTITUTION = "substitution"
DID_NOT_PLAY = "did_not_play"
NOT_ACTIVE = "not_active"
NOT_LISTED = "not_listed"          # gamebook present, player on none of its lists (e.g. IR / reserve / practice squad)

GRADED = "graded"
VOID = "void"


def name_key(full_name) -> str:
    """'Michael Pittman Jr.' and 'Michael Pittman' -> 'michaelpittman'. Unknown in, unknown out."""
    if full_name is None or full_name == UNKNOWN or not str(full_name).strip():
        return UNKNOWN
    toks = [t for t in re.sub(r"[.,]", " ", str(full_name)).lower().split() if t not in SUFFIXES]
    return re.sub(r"[^a-z]", "", "".join(toks))


def gamebook_key(full_name) -> str:
    """Full name -> the gamebook's printed 'F.Surname' key, lower-cased, suffixes dropped ('t.mcbride')."""
    if full_name is None or full_name == UNKNOWN:
        return UNKNOWN
    toks = [t for t in str(full_name).replace("'", "").replace(".", " ").split() if t.lower() not in SUFFIXES]
    if len(toks) < 2:
        return UNKNOWN
    return toks[0][0].lower() + "." + re.sub(r"[^a-z]", "", toks[-1].lower())


def _printed_key(printed: str) -> str:
    """Gamebook printed name 'T.McBride' / 'Tr.Smith' / 'D.Taylor-Demerson' -> 't.mcbride' / 't.smith' / 't.taylordemerson'."""
    s = str(printed).strip()
    if "." not in s:
        return re.sub(r"[^a-z]", "", s.lower())
    first, last = s.split(".", 1)
    return first[:1].lower() + "." + re.sub(r"[^a-z]", "", last.lower())


def load_gamebook(game_dir: Path) -> dict | None:
    """{team_abbr: {printed_key: [status, ...]}} from data/gamebooks/<season>/wk<NN>/<game_id>/parsed/, or None."""
    parsed = Path(game_dir) / "parsed"
    lu, pa = parsed / "lineups.csv", parsed / "participation.csv"
    if not (lu.exists() and pa.exists()):
        return None
    out: dict[str, dict[str, list[str]]] = {}
    with lu.open(newline="") as f:
        for r in csv.DictReader(f):
            out.setdefault(r["team_abbr"], {}).setdefault(_printed_key(r["player"]), []).append(STARTED)
    with pa.open(newline="") as f:
        for r in csv.DictReader(f):
            st = {"substitution": SUBSTITUTION, "did_not_play": DID_NOT_PLAY, "not_active": NOT_ACTIVE}.get(r["list_name"])
            if st:
                out.setdefault(r["team_abbr"], {}).setdefault(_printed_key(r["player"]), []).append(st)
    return out


def participation_status(gamebook: dict | None, team_abbr: str, full_name: str) -> dict:
    """Participation for one player. Ambiguous printed keys (two players share 'J.Smith') are unknown, never guessed."""
    if gamebook is None:
        return {"status": UNKNOWN, "reason": "no parsed gamebook for this game"}
    team = gamebook.get(team_abbr)
    if team is None:
        return {"status": UNKNOWN, "reason": f"team {team_abbr} not in gamebook (printed codes differ, e.g. ARZ/BLT/CLV/HST)"}
    k = gamebook_key(full_name)
    if k == UNKNOWN:
        return {"status": UNKNOWN, "reason": "name not usable"}
    hits = team.get(k)
    if not hits:
        return {"status": NOT_LISTED, "reason": f"{k} on no {team_abbr} list (starters, substitutions, did not play, not active)"}
    if len(set(hits)) > 1 or len(hits) > 1:
        return {"status": UNKNOWN, "reason": f"{k} appears {len(hits)} times on {team_abbr} lists {sorted(set(hits))}: ambiguous"}
    return {"status": hits[0], "reason": "official game summary"}


def settlement_status(participation: str) -> str:
    """Proposed settlement class. Played -> graded (a 0 is real). Inactive / did-not-play -> void. Else unknown."""
    if participation in (STARTED, SUBSTITUTION):
        return GRADED
    if participation in (NOT_ACTIVE, DID_NOT_PLAY):
        return VOID
    return UNKNOWN


def attribute_error(proj_volume, proj_rate, act_volume, act_stat) -> dict:
    """Split (actual - projected) for a stat = volume x rate into opportunity and efficiency parts.

    projected = proj_volume * proj_rate. opportunity = (act_volume - proj_volume) * proj_rate.
    efficiency = act_stat - act_volume * proj_rate. opportunity + efficiency == actual - projected exactly.
    Any missing input -> every part unknown.
    """
    vals = (proj_volume, proj_rate, act_volume, act_stat)
    if any(v is None or v == UNKNOWN for v in vals):
        return {"projected": UNKNOWN, "total_error": UNKNOWN, "opportunity": UNKNOWN, "efficiency": UNKNOWN}
    pv, pr, av, ast = (float(v) for v in vals)
    projected = pv * pr
    opp = (av - pv) * pr
    eff = ast - av * pr
    return {"projected": round(projected, 4), "total_error": round(ast - projected, 4),
            "opportunity": round(opp, 4), "efficiency": round(eff, 4)}
