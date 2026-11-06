"""Optional sourced player-volume / form evidence for period+prop reads.

RESEARCH SPEC INTERFACE ONLY — not a player-prop engine, not gate PASS.
Does not invent H2H overlays, target-location grids, or defender maps.
Absent fields → explicit MISSING flags. No browser/Outlier login from this module.
Green Outlier chart ≠ automatic edge (Rico 2026-11-05).
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional
import csv
import json

_OPTIONAL = Path(__file__).resolve().parent / "optional_inputs"
DEFAULT_OUTLIER_CSV = _OPTIONAL / "outlier_props.csv"
SCREENSHOT_DIR = _OPTIONAL / "screenshots_quote_ref"


@dataclass
class MarketSourceTie:
    """Exact market/rung tied to a chart or screenshot hash."""
    market: str
    line: Optional[float]
    side: str
    source_type: str  # outlier_csv | screenshot | pbp | MISSING
    source_path: Optional[str]
    source_hash_or_row: Optional[str]
    pulled_et: Optional[str]
    notes: str = ""


@dataclass
class PlayerEvidenceBundle:
    player: str
    team: str
    opponent: str
    market_tie: MarketSourceTie
    outlier_row: Optional[dict] = None
    h2h: dict = field(default_factory=dict)  # {n, rate, status, notes}
    recent_form: dict = field(default_factory=dict)  # L5/L10 etc from CSV only
    location_overlay: dict = field(default_factory=dict)  # short/int/deep x L/M/R
    alignment_route: dict = field(default_factory=dict)
    verified_defenders: dict = field(default_factory=dict)
    qb_role_injury_coverage_changes: dict = field(default_factory=dict)
    miss_audit: dict = field(default_factory=dict)
    flags: list[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)


def load_outlier_csv(path: Path = DEFAULT_OUTLIER_CSV) -> list[dict]:
    if not path.exists():
        return []
    with path.open() as f:
        return list(csv.DictReader(f))


def find_outlier_rows(player: str, market: Optional[str] = None, path: Path = DEFAULT_OUTLIER_CSV) -> list[dict]:
    rows = load_outlier_csv(path)
    out = []
    for r in rows:
        if r.get("player", "").lower() != player.lower():
            continue
        if market and r.get("market", "").lower() != market.lower():
            continue
        out.append(r)
    return out


def bundle_from_outlier(
    player: str,
    *,
    market: str,
    line: Optional[float],
    side: str,
    team: str = "",
    opponent: str = "",
    path: Path = DEFAULT_OUTLIER_CSV,
    screenshot_hash: Optional[str] = None,
    pulled_et: Optional[str] = None,
) -> PlayerEvidenceBundle:
    rows = find_outlier_rows(player, market, path)
    # prefer matching line if provided
    row = None
    if line is not None:
        for r in rows:
            try:
                if abs(float(r.get("line", "nan")) - float(line)) < 1e-9 and r.get("side", "").lower() == side.lower():
                    row = r
                    break
            except ValueError:
                continue
    if row is None and rows:
        row = rows[0]

    flags = []
    if not path.exists():
        flags.append("OUTLIER_CSV_MISSING")
    if row is None:
        flags.append("OUTLIER_ROW_MISSING")

    h2h_raw = (row or {}).get("H2H", "-")
    h2h = {
        "raw": h2h_raw,
        "n": None,
        "rate": None,
        "status": "MISSING" if (not h2h_raw or h2h_raw.strip() in {"-", ""}) else "PRESENT_UNPARSED",
        "notes": "Outlier H2H cell only; n and role/QB match not verified here",
    }
    if h2h["status"] == "MISSING":
        flags.append("H2H_MISSING_OR_DASH")

    form = {
        "L5": (row or {}).get("L5"),
        "L10": (row or {}).get("L10"),
        "hit_2026": (row or {}).get("hit_2026"),
        "hit_2025": (row or {}).get("hit_2025"),
        "status": "FROM_OUTLIER_CSV" if row else "MISSING",
        "notes": "Green hit-rate chart ≠ automatic edge",
    }

    # Location / alignment / defenders: not in this CSV → explicit gaps (no invention)
    location = {
        "grid": "short|intermediate|deep x left|middle|right",
        "status": "MISSING",
        "notes": "No target-location overlay in Outlier CSV; need charting/NGS or labeled screenshot tied to market",
    }
    flags.append("LOCATION_OVERLAY_MISSING")

    alignment = {"status": "MISSING", "notes": "Alignment/route not in CSV"}
    flags.append("ALIGNMENT_ROUTE_MISSING")

    defenders = {
        "status": "MISSING",
        "primary_verified": False,
        "notes": "Verified responsible defenders require Phase-4 sources; not inventable from Outlier props CSV",
    }
    flags.append("VERIFIED_DEFENDER_MISSING")

    changes = {
        "qb_change": "UNKNOWN",
        "role_change": "UNKNOWN",
        "injury_context": "UNKNOWN",
        "coverage_change": "UNKNOWN",
        "status": "MISSING_UNLESS_SUPPLIED_BY_CALLER",
        "notes": "Caller may attach as-of injury/QB notes; module does not scrape",
    }
    flags.append("QB_ROLE_INJURY_COVERAGE_NOT_ATTACHED")

    miss = {
        "status": "MISSING",
        "notes": "Miss audit (why line missed; cause present this week?) must be written by researcher — not auto from L5",
    }
    flags.append("MISS_AUDIT_NOT_ATTACHED")

    if screenshot_hash:
        tie = MarketSourceTie(
            market=market, line=line, side=side,
            source_type="screenshot",
            source_path=str(SCREENSHOT_DIR / f"{screenshot_hash}.png") if SCREENSHOT_DIR.exists() else None,
            source_hash_or_row=screenshot_hash,
            pulled_et=pulled_et,
            notes="Screenshot must depict the exact market/rung",
        )
    elif row:
        tie = MarketSourceTie(
            market=market, line=float(row["line"]) if row.get("line") not in (None, "") else line,
            side=row.get("side", side),
            source_type="outlier_csv",
            source_path=str(path),
            source_hash_or_row=json.dumps({k: row.get(k) for k in ("player","market","line","side","source")}),
            pulled_et=pulled_et or "csv_file_mtime_unknown",
            notes=(row or {}).get("notes", ""),
        )
    else:
        tie = MarketSourceTie(market=market, line=line, side=side, source_type="MISSING",
                              source_path=None, source_hash_or_row=None, pulled_et=pulled_et)
        flags.append("MARKET_SOURCE_UNTIED")

    flags.append("GREEN_CHART_NOT_AUTOMATIC_EDGE")

    return PlayerEvidenceBundle(
        player=player,
        team=team or (row or {}).get("team", ""),
        opponent=opponent or (row or {}).get("opponent", ""),
        market_tie=tie,
        outlier_row=row,
        h2h=h2h,
        recent_form=form,
        location_overlay=location,
        alignment_route=alignment,
        verified_defenders=defenders,
        qb_role_injury_coverage_changes=changes,
        miss_audit=miss,
        flags=flags,
    )
