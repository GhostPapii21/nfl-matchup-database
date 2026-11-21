#!/usr/bin/env python3
"""Source gap ledger (NFL-10, NFL-47). Read-only over nfl_matchups.sqlite.gz; writes
inventory/SOURCE_GAP_LEDGER.json and docs/SOURCE_GAP_LEDGER.md with --write.

Rules:
- Freshness comes from the publisher's own `source_updated_at`. `retrieved_at` (our fetch time) is reported but is
  never used to call a source fresh.
- The reference point is the last FINAL game in the database. A source updated before that game's ET calendar day
  ended is STALE. An update after it is UPDATED_AFTER_LAST_FINAL, but `data_through` stays "unknown" because no
  source here states an explicit data-through cutoff.
- No publisher stamp means UNKNOWN_NO_SOURCE_TIMESTAMP, never fresh and never zero.
- Repeated gap rows are deduplicated by (source_id, reason).
- Coverage, route, NGS, FTN and PFF effects stay disabled unless a source is both authorized and verified.
  Nothing in this file marks one authorized.
No network. No model, weight, formula or projection_ready change."""
from __future__ import annotations

import argparse, gzip, json, sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
ET = ZoneInfo("America/New_York")

# Coverage-family sources (NFL-47). Status text is taken from docs/SOURCE_STATUS.md and the NFL-47 Linear comments
# of 2026-11-07. authorized/verified stay False until Rico authorizes the source and the row-level fields are checked.
COVERAGE_FAMILY = [
    {"family": "FTN charting coverage/blitz effects", "status": "MISSING for effects; charting parquet is hash-only",
     "authorized": False, "verified": False, "evidence": "docs/SOURCE_STATUS.md; NFL-47",
     "needed": "Verify FTN charting field definitions at row level (nflverse CC-BY-SA dictionary); the definitions alone do not establish defender assignment or decision-time pressure."},
    {"family": "NGS coverage responsibility (NFL Pro)", "status": "NOT_HELD: Rico has public NGS access only (2026-11-21)",
     "authorized": False, "verified": False, "evidence": "NFL-47 comment 2026-11-07; Rico 2026-11-21 18:46 AST",
     "needed": "Not available on public NGS. Plans are limited to public nextgenstats.nfl.com leaderboards and charts. Don't attempt NFL Pro data."},
    {"family": "PFF coverage / coverage_matchup / pass_rush", "status": "TIER_LIMITED: Rico holds PFF's first paid tier, not PFF Pro (2026-11-21)",
     "authorized": False, "verified": False, "evidence": "docs/SOURCE_STATUS.md; NFL-47 comment 2026-11-07; NFL-48; Rico 2026-11-21 18:46 AST",
     "needed": "Only what the first paid tier shows on screen or in its downloads (premium player and team grades, per-report CSVs where offered). Pro-only API and coverage_matchup facets are out of scope. A refresh needs Rico's OK (NFL-48)."},
    {"family": "Full RB/TE route participation", "status": "PARTIAL",
     "authorized": False, "verified": False, "evidence": "NFL-10 description (2026-10-28 update)",
     "needed": "A complete per-game route source; public participation shows on-field presence only, not routes or coverage."},
    {"family": "NGS public route/carry chart images", "status": "RESEARCH_CONTEXT_ONLY",
     "authorized": False, "verified": False, "evidence": "SQLite ngs_route_charts / ngs_carry_charts",
     "needed": "Images are not a play-level feed. Context only, not a model input."},
]


def effects_enabled(rec: dict) -> bool:
    return bool(rec.get("authorized")) and bool(rec.get("verified"))


def open_db(path) -> sqlite3.Connection:
    c = sqlite3.connect(":memory:")
    c.deserialize(gzip.open(path).read())
    return c


def _utc(s):
    if not s:
        return None
    d = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def build(c: sqlite3.Connection) -> dict:
    last = c.execute("SELECT max(date) FROM games WHERE status='STATUS_FINAL'").fetchone()[0]
    cutoff = None
    if last:
        cutoff = (datetime.fromisoformat(last).replace(tzinfo=ET) + timedelta(days=1)).astimezone(timezone.utc)
    sources = []
    for (sid,) in c.execute("SELECT DISTINCT source_id FROM external_fetches ORDER BY source_id").fetchall():
        rows = c.execute("SELECT retrieved_at, source_updated_at, status FROM external_fetches WHERE source_id=?", (sid,)).fetchall()
        latest = max(rows, key=lambda r: _utc(r[0]) or datetime.min.replace(tzinfo=timezone.utc))
        stamps = [r[1] for r in rows if r[1] and str(r[2]).startswith("OK")]
        upd = max(stamps, key=_utc) if stamps else None
        if upd is None:
            fr = "UNKNOWN_NO_SOURCE_TIMESTAMP"
        elif cutoff is None:
            fr = "UNKNOWN_NO_FINAL_GAMES"
        elif _utc(upd) < cutoff:
            fr = "STALE_SOURCE_UPDATED_BEFORE_LAST_FINAL"
        else:
            fr = "UPDATED_AFTER_LAST_FINAL"
        sources.append({"source_id": sid, "freshness": fr, "freshness_basis": "source_updated_at",
                        "source_updated_at": upd, "data_through": "unknown",
                        "latest_retrieved_at_not_used_for_freshness": latest[0], "latest_fetch_status": latest[2],
                        "fetches": len(rows)})
    gaps = []
    for sid, reason, n, first, lastobs in c.execute(
            "SELECT source_id, reason, count(*), min(observed_at), max(observed_at) FROM external_gaps "
            "GROUP BY source_id, reason ORDER BY source_id, reason"):
        gaps.append({"source_id": sid, "reason": reason, "occurrences": n,
                     "first_observed_at": first, "last_observed_at": lastobs})
    raw = c.execute("SELECT count(*) FROM external_gaps").fetchone()[0]
    cov = [dict(r, effects_enabled=effects_enabled(r)) for r in COVERAGE_FAMILY]
    return {"reference_last_final_game_date_et": last,
            "reference_cutoff_utc": cutoff.isoformat() if cutoff else None,
            "sources": sources, "gaps": gaps, "raw_gap_rows": raw, "deduplicated_gap_rows": len(gaps),
            "coverage_family": cov, "projection_ready_changed": False}


def to_md(d: dict) -> str:
    out = ["# Source gap ledger (NFL-10, NFL-47)", "",
           "Generated by `python3 source_gap_ledger.py --write` from `nfl_matchups.sqlite.gz`. Do not edit by hand.",
           "Freshness comes from the publisher's `source_updated_at`, never from our fetch time. `data_through` is "
           "unknown wherever the source does not state a cutoff.", "",
           f"Reference: last FINAL game in the database is {d['reference_last_final_game_date_et']} ET (cutoff "
           f"{d['reference_cutoff_utc']}). The database snapshot itself ends there, so every row is also behind the "
           "current week. UPDATED_AFTER_LAST_FINAL only means the source is not older than this database.", "",
           "| Source | Freshness | Publisher updated | Data through | Our latest fetch (not used) | Fetch status |",
           "| --- | --- | --- | --- | --- | --- |"]
    for s in d["sources"]:
        out.append(f"| {s['source_id']} | {s['freshness']} | {s['source_updated_at'] or 'unknown'} | {s['data_through']} | "
                   f"{s['latest_retrieved_at_not_used_for_freshness']} | {s['latest_fetch_status']} |")
    out += ["", f"## Gaps, deduplicated ({d['raw_gap_rows']} raw rows to {d['deduplicated_gap_rows']})", "",
            "| Source | Reason | Occurrences | First seen | Last seen |", "| --- | --- | --- | --- | --- |"]
    for g in d["gaps"]:
        out.append(f"| {g['source_id']} | {g['reason']} | {g['occurrences']} | {g['first_observed_at']} | {g['last_observed_at']} |")
    out += ["", "## Coverage / NGS / FTN / PFF family (effects stay disabled)", "",
            "| Family | Status | Authorized | Verified | Effects enabled | Needed | Evidence |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for r in d["coverage_family"]:
        out.append(f"| {r['family']} | {r['status']} | {r['authorized']} | {r['verified']} | {r['effects_enabled']} | {r['needed']} | {r['evidence']} |")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(ROOT / "nfl_matchups.sqlite.gz"))
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    d = build(open_db(a.db))
    if a.write:
        (ROOT / "inventory/SOURCE_GAP_LEDGER.json").write_text(json.dumps(d, indent=2) + "\n")
        (ROOT / "docs/SOURCE_GAP_LEDGER.md").write_text(to_md(d))
    print(json.dumps({k: d[k] for k in ("reference_last_final_game_date_et", "raw_gap_rows", "deduplicated_gap_rows")}))


if __name__ == "__main__":
    main()
