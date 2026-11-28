"""Build the DEN@PIT historical decision packet from the locked pregame snapshot.

Reads the lock, the published sim summary, the frozen team prices, and the
pregame direct-line file. It does not read postgame grades, play-by-play, or
the post-kickoff write-up. Player probabilities are not invented.
"""

from __future__ import annotations

import json
from pathlib import Path

from .board import build_board
from .market import normalize_market
from .report import render_markdown

ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = "snapshots/2026_12_DEN_PIT/20261127T111648Z"
DIRECT = "pregame/direct_lines/2026_12_DEN_PIT.json"
GAME_ID = "2026_12_DEN_PIT"


def _load(path: Path) -> dict:
    return json.loads(path.read_text())


def _team_quote(row: dict) -> dict:
    market = normalize_market(row["market"])
    subject = "GAME" if market == "total" else row["side_a"]
    return {
        "book": row["book"],
        "market": market,
        "subject": subject,
        "side": row["side_a"],
        "line": row["line"],
        "price": row["price_a"],
        "opposite_side": row["side_b"],
        "opposite_price": row["price_b"],
        "timestamp_utc": row["book_last_update"],
        "timestamp_kind": "book_last_update",
        "reference_only": bool(row.get("reference_only")),
        "source": f"{SNAPSHOT}/inputs/team_prices_from_packet.json",
        "supplied_novig": row.get("novig_a"),
    }


def _summary_index(summary: dict) -> dict:
    index = {}
    for row in summary["vs_market"]:
        market = normalize_market(row["market"])
        key = (market, row["side"], row.get("line"))
        if market == "spread":
            probability, kind = row["p_model_cover"], "p_cover"
        elif market == "total":
            probability, kind = row["p_model"], "p_over"
        elif market == "moneyline":
            probability, kind = row["p_model_win"], "p_win"
        else:
            continue
        payload = {
            "probability": probability,
            "kind": kind,
            "push_probability": row.get("p_model_push"),
            "ex_tie": row.get("p_model_win_ex_tie"),
        }
        previous = index.get(key)
        if previous and previous["probability"] != payload["probability"]:
            raise ValueError(f"summary published two probabilities for {key}")
        index[key] = payload
    return index


def _projection(summary: dict, market: str) -> dict:
    if market == "spread":
        margin = summary["margin_home"]
        return {"mean_margin_home": margin["mean"], "sd": margin["sd"]}
    if market == "total":
        total = summary["total"]
        return {"mean": total["mean"], "sd": total["sd"]}
    return {
        "p_home_win": summary["p_home_win"],
        "p_away_win": summary["p_away_win"],
        "p_tie": summary["p_tie"],
    }


def _team_thesis(summary: dict, lock: dict, market: str, side: str, line, published: dict) -> dict:
    flag = summary["market_divergence"]["flag"]
    uncertainty = {}
    if market == "spread":
        uncertainty["distribution_sd"] = summary["margin_home"]["sd"]
    elif market == "total":
        uncertainty["distribution_sd"] = summary["total"]["sd"]
    subject = "GAME" if market == "total" else side
    return {
        "thesis_id": f"team:{market}:{side}:{line if line is not None else 'ml'}",
        "subject": subject,
        "subject_kind": "team",
        "market": market,
        "side": side,
        "opposite_side": None,
        "line": line,
        "role_tag": "team_score",
        "projection": _projection(summary, market),
        "script_sensitive": True,
        "model_error_flag": flag,
        "models": [{
            "model_id": "possession_engine_v0",
            "method": "team_snap_resample",
            "probability": published["probability"],
            "probability_kind": published["kind"],
            "n": summary["n"],
            "seed": lock["sim"]["seed"],
            "calibration_status": "unfitted",
            "push_probability": published["push_probability"],
            "uncertainty": uncertainty,
        }],
        "evidence_for": [{
            "text": (
                f"Locked {summary['n']}-trial possession sim published "
                f"{published['kind']}={published['probability']} at this line."
            ),
            "source": f"{SNAPSHOT}/summary.json",
        }],
        "evidence_against": [{
            "severity": "invalidating",
            "text": flag,
            "source": f"{SNAPSHOT}/summary.json market_divergence",
        }],
        "defensive_suppression": [{
            "path": "not assessed",
            "material": False,
            "detail": "this snapshot is a team-score sim and does not identify a coverage shell",
        }],
        "role_volume": {
            "tag": "team_score",
            "fragile": False,
            "reason": "team market; player roles are not in this sim",
        },
        "efficiency_dependent": False,
        "contingencies": {
            "injury": {
                "supplied": True,
                "modeled": False,
                "invalidates": False,
                "detail": "data_only config: no injury/inactive adjustment; Phase 15 inactives were not applied",
            },
            "weather": {
                "supplied": True,
                "modeled": False,
                "invalidates": False,
                "detail": "the lock does not record a weather adjustment",
            },
            "game_script": {
                "supplied": True,
                "branches_retained": False,
                "detail": "one team-resample distribution; favorite, competitive, and underdog branches were not retained",
            },
        },
        "sample_quality": {
            "n": summary["n"],
            "withheld": False,
            "blocks_reads": False,
            "limitation": "team scores only; W1-8 development set; no betting edge claim",
        },
    }


def _player_shell(player: str, market: str, line, detail: str) -> dict:
    line_token = "missing" if line is None else line
    return {
        "thesis_id": f"player:{player}:{market}:Over:{line_token}",
        "subject": player,
        "subject_kind": "player",
        "market": market,
        "side": "Over",
        "opposite_side": "Under",
        "line": line,
        "role_tag": "unverified",
        "projection": None,
        "script_sensitive": True,
        "models": [],
        "evidence_for": [],
        "evidence_against": [{
            "severity": "material",
            "text": detail,
            "source": f"{SNAPSHOT}/summary.json player_outputs",
        }],
        "defensive_suppression": [{
            "path": "not assessed",
            "material": False,
            "detail": "no player projection was published, so no suppression path was tested",
        }],
        "role_volume": {
            "tag": "unverified",
            "fragile": True,
            "reason": (
                "role and volume were not established; the player projection was withheld; "
                "the direct-line name was not matched to a game roster"
            ),
        },
        "efficiency_dependent": True,
        "contingencies": {
            "injury": {
                "supplied": True,
                "modeled": False,
                "invalidates": False,
                "detail": "data_only config does not adjust player availability",
            },
            "weather": {
                "supplied": True,
                "modeled": False,
                "invalidates": False,
                "detail": "weather was not applied to a player distribution because none was published",
            },
            "game_script": {
                "supplied": True,
                "branches_retained": False,
                "detail": "player opportunity was not split across retained game scripts",
            },
        },
        "sample_quality": {
            "n": None,
            "withheld": True,
            "blocks_reads": True,
            "limitation": detail,
        },
    }


def _player_main_lines(payload: dict, kickoff: str) -> tuple[list[dict], list[dict]]:
    retrieved = payload.get("retrieved_utc")
    if not retrieved or not (str(retrieved) < str(kickoff)):
        raise ValueError("direct player lines are missing a pregame timestamp")
    groups: dict[tuple, dict] = {}
    for row in payload.get("rows") or []:
        player = row.get("player")
        market = row.get("market") or ""
        if not player or market.startswith("alt_") or row.get("book") != "fanduel":
            continue
        if row.get("side") not in {"Over", "Under"}:
            continue
        groups.setdefault((player, market, row.get("line")), {})[row["side"]] = row
    chosen: dict[tuple, tuple] = {}
    for (player, market, line), sides in groups.items():
        if "Over" not in sides or "Under" not in sides:
            continue
        distance = abs(float(sides["Over"]["american"]) - (-110))
        current = chosen.get((player, market))
        if current is None or distance < current[0] or (distance == current[0] and float(line) < current[1]):
            chosen[(player, market)] = (distance, float(line), sides)
    quotes, theses = [], []
    detail = (
        "WITHHELD: the possession sim's player credits are team-bootstrap historical rows, "
        "not a player projection model"
    )
    for (player, market), (_distance, line, sides) in sorted(chosen.items()):
        quotes.append({
            "book": "fanduel",
            "market": market,
            "subject": player,
            "side": "Over",
            "line": line,
            "price": sides["Over"]["american"],
            "opposite_side": "Under",
            "opposite_price": sides["Under"]["american"],
            "timestamp_utc": retrieved,
            "timestamp_kind": "file_retrieved_utc",
            "reference_only": False,
            "source": DIRECT,
        })
        theses.append(_player_shell(player, market, line, detail))
    return quotes, theses


def load_packet(root: Path | None = None) -> dict:
    root = root or ROOT
    snapshot = root / SNAPSHOT
    summary = _load(snapshot / "summary.json")
    lock = _load(snapshot / "LOCK.json")
    prices = _load(snapshot / "inputs" / "team_prices_from_packet.json")
    direct = _load(root / DIRECT)
    kickoff = lock["kickoff_utc"]
    if lock.get("projection_ready") is not False:
        raise ValueError("historical lock is not research-only")
    index = _summary_index(summary)
    lines = []
    theses = []
    seen = set()
    for row in prices["rows"]:
        quote = _team_quote(row)
        if not quote["timestamp_utc"] or not (str(quote["timestamp_utc"]) < str(kickoff)):
            raise ValueError("team price is missing a pregame timestamp")
        lines.append(quote)
        key = (quote["market"], quote["side"], quote["line"])
        if key in seen:
            continue
        seen.add(key)
        published = index.get(key)
        if published is None:
            raise ValueError(f"frozen price has no published model probability: {key}")
        theses.append(_team_thesis(summary, lock, quote["market"], quote["side"], quote["line"], published))
    player_lines, player_theses = _player_main_lines(direct, kickoff)
    lines.extend(player_lines)
    theses.extend(player_theses)
    theses.append(_player_shell(
        "Bo Nix",
        "passing_yards",
        None,
        "no passing-yards line in the pregame direct file and no player probability in the lock",
    ))
    theses.sort(key=lambda thesis: thesis["thesis_id"])
    return {
        "game_id": GAME_ID,
        "home": summary["home"],
        "away": summary["away"],
        "kickoff_utc": kickoff,
        "projection_ready": False,
        "research_only": True,
        "theses": theses,
        "lines": lines,
        "sources": [
            {"path": f"{SNAPSHOT}/summary.json", "role": "model_probabilities"},
            {"path": f"{SNAPSHOT}/LOCK.json", "role": "run_identity_and_limits"},
            {"path": f"{SNAPSHOT}/inputs/team_prices_from_packet.json", "role": "team_market_snapshots"},
            {"path": DIRECT, "role": "player_market_snapshots"},
        ],
    }


def write_report(out_dir: Path, root: Path | None = None) -> dict:
    packet = load_packet(root)
    report = build_board(packet)
    report["sources"] = packet["sources"]
    report["historical_game"] = packet["game_id"]
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "decision_board.json").write_text(json.dumps(report, indent=2) + "\n")
    (out_dir / "decision_board.md").write_text(render_markdown(report))
    return report
