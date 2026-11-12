"""Quote provenance ledger: book, as-of, path, and hash for every saved quote.

NFL-45 names the package at research/market_calibration/. That path does not
exist in this repository. market_calibration/ is canonical and is not moved.

Actionable status stays NOLINE until an authenticated refresh succeeds.
This module never invents prices, never copies unpublished CSVs into
saved_quotes/, and never claims a fitted calibration.
"""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

CANONICAL_PACKAGE_PATH = "market_calibration"
ISSUE_NAMED_PATH = "research/market_calibration"
REQUIRED_FIELDS = ("book", "as_of", "path", "hash")

_PKG = Path(__file__).resolve().parent
_REPO = _PKG.parent
_SAVED = _PKG / "saved_quotes"
_PACKAGE_CSV = (
    "odds_jaxbal_game.csv",
    "period_q1_q2_q3_fd_dk_cleared.csv",
    "period_line_grades.csv",
)

# In-repo inventories already published on main. Paths are repo-relative.
_INVENTORIES = (
    {
        "id": "certified_asof",
        "records_dir": "research/nfl_sim_integration_2026-11-06/integration/certified_asof/records",
        "base": "research/nfl_sim_integration_2026-11-06/integration/certified_asof",
        "files": (
            "DK_saved_quotes.json",
            "FD_saved_quotes.json",
            "Pinnacle_saved_quotes.json",
        ),
    },
    {
        "id": "asof_sources",
        "records_dir": "research/nfl_sim_integration_2026-11-06/integration/asof_sources/records",
        "base": "research/nfl_sim_integration_2026-11-06/integration/asof_sources",
        "files": (
            "DK_saved_quotes.json",
            "FD_saved_quotes.json",
            "Pinnacle_saved_quotes.json",
        ),
    },
)


def repo_root() -> Path:
    return _REPO


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def relpath(path: Path, root: Path | None = None) -> str:
    root = Path(root or _REPO).resolve()
    return path.resolve().relative_to(root).as_posix()


def ledger_entry(*, book, as_of, path, digest, **extra) -> dict:
    entry = {"book": book, "as_of": as_of, "path": path, "hash": digest}
    entry.update(extra)
    return entry


def entry_complete(entry: dict) -> bool:
    return all(
        isinstance(entry.get(key), str) and entry[key]
        and (key != "hash" or _is_sha256(entry[key]))
        for key in REQUIRED_FIELDS
    )


def _is_sha256(value: str) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(
        c in "0123456789abcdef" for c in value.lower()
    ) and value == value.lower()


def _norm_book(value: str | None) -> str | None:
    if not value or not str(value).strip():
        return None
    value = str(value).strip().lower()
    return {"fd": "fanduel", "dk": "draftkings", "pin": "pinnacle"}.get(value, value)


def _raw_fields(record: dict) -> dict:
    raw = record.get("raw_quote_fields")
    return raw if isinstance(raw, dict) else {}


def _package_csv_status() -> dict:
    files = []
    present = True
    for name in _PACKAGE_CSV:
        path = _SAVED / name
        item = {"path": relpath(path), "present": path.is_file()}
        if path.is_file():
            item["hash"] = file_sha256(path)
            item["bytes"] = path.stat().st_size
        else:
            present = False
        files.append(item)
    return {
        "status": "SAVED_CSVS_PRESENT" if present else "ABSENT_NOLINE",
        "note": (
            "Package CSVs are intentionally unpublished; see saved_quotes/README.md."
            if not present else "Local saved CSVs are present; still research-only."
        ),
        "files": files,
    }


def _resolve_source(record: dict, inventory: dict, root: Path) -> tuple[Path | None, str | None, str | None]:
    raw = _raw_fields(record)
    relative = record.get("source_path") or record.get("source_snapshot") or raw.get("source_file")
    if not relative or not isinstance(relative, str):
        return None, None, "MISSING_SOURCE_PATH"
    base = root / inventory["base"]
    candidate = (base / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None, relative, "SOURCE_PATH_OUT_OF_REPO"
    if not candidate.is_file():
        return None, relative, "SOURCE_FILE_MISSING"
    return candidate, relpath(candidate, root), None


def _entry_from_record(record: dict, inventory: dict, inventory_path: Path, root: Path) -> tuple[dict, str | None]:
    raw = _raw_fields(record)
    book = _norm_book(record.get("book") or raw.get("book"))
    # quotes.py uses the same snapshot_* aliases when last_update_utc is absent.
    as_of = (
        raw.get("last_update_utc") or record.get("last_update_utc")
        or raw.get("snapshot_last_update_utc") or record.get("snapshot_last_update_utc")
    )
    retrieval = (
        raw.get("pulled_utc") or record.get("pulled_utc")
        or raw.get("snapshot_pulled_utc") or record.get("snapshot_pulled_utc")
    )
    source, path, path_flag = _resolve_source(record, inventory, root)
    recorded = record.get("source_sha256")
    if isinstance(recorded, str) and recorded.startswith("sha256:"):
        recorded = recorded[len("sha256:"):]
    digest = None
    flag = path_flag
    if source is not None:
        digest = file_sha256(source)
        if recorded and recorded.lower() != digest:
            flag = "HASH_MISMATCH"
            digest = None
    if not book:
        flag = flag or "MISSING_BOOK"
    if not isinstance(as_of, str) or not as_of:
        flag = flag or "MISSING_AS_OF"
    entry = ledger_entry(
        book=book or "",
        as_of=as_of or "",
        path=path or "",
        digest=digest or "",
        retrieval_utc=retrieval,
        inventory=inventory["id"],
        inventory_path=relpath(inventory_path, root),
        row_number=record.get("source_row_number") or record.get("row_number"),
        scope="research",
        actionable_status=record.get("actionable_status") or "NOLINE",
        status=record.get("status") or "SAVED_ONLY",
        usable_for_run=False,
    )
    if flag:
        entry["flag"] = flag
        if recorded:
            entry["recorded_hash"] = recorded
    if not entry_complete(entry) or flag:
        return entry, flag or "INCOMPLETE"
    return entry, None


def _entries_from_package_csvs(root: Path) -> tuple[list[dict], list[dict]]:
    status = _package_csv_status()
    if status["status"] != "SAVED_CSVS_PRESENT":
        return [], []
    from .quotes import load_saved_quotes

    complete, incomplete = [], []
    for quote in load_saved_quotes():
        path = quote.source_file
        try:
            path = relpath(Path(quote.source_file), root)
        except ValueError:
            path = quote.source_file
        entry = ledger_entry(
            book=quote.book,
            as_of=quote.last_update_utc,
            path=path,
            digest=quote.source_sha256,
            retrieval_utc=quote.pulled_utc,
            inventory="package_saved_quotes",
            row_number=quote.row_number,
            scope="research",
            actionable_status="NOLINE",
            status="SAVED_ONLY",
            usable_for_run=False,
        )
        if entry_complete(entry):
            complete.append(entry)
        else:
            entry["flag"] = "INCOMPLETE"
            incomplete.append(entry)
    return complete, incomplete


def build_quote_provenance_ledger(repo_root_path: Path | None = None) -> dict:
    root = Path(repo_root_path or _REPO).resolve()
    research: list[dict] = []
    incomplete: list[dict] = []
    sources: dict[str, dict] = {}

    package = _package_csv_status()
    pkg_complete, pkg_incomplete = _entries_from_package_csvs(root)
    research.extend(pkg_complete)
    incomplete.extend(pkg_incomplete)

    for inventory in _INVENTORIES:
        records_dir = root / inventory["records_dir"]
        for name in inventory["files"]:
            inventory_path = records_dir / name
            if not inventory_path.is_file():
                incomplete.append({
                    "book": "", "as_of": "", "path": relpath(inventory_path, root) if records_dir.exists() else inventory["records_dir"] + "/" + name,
                    "hash": "", "flag": "INVENTORY_FILE_MISSING", "inventory": inventory["id"],
                })
                continue
            sources[relpath(inventory_path, root)] = {
                "path": relpath(inventory_path, root),
                "hash": file_sha256(inventory_path),
                "bytes": inventory_path.stat().st_size,
            }
            rows = json.loads(inventory_path.read_text())
            if not isinstance(rows, list):
                incomplete.append({
                    "book": "", "as_of": "", "path": relpath(inventory_path, root),
                    "hash": sources[relpath(inventory_path, root)]["hash"],
                    "flag": "INVENTORY_NOT_A_LIST", "inventory": inventory["id"],
                })
                continue
            for record in rows:
                if not isinstance(record, dict):
                    incomplete.append({
                        "book": "", "as_of": "", "path": relpath(inventory_path, root),
                        "hash": "", "flag": "RECORD_NOT_AN_OBJECT", "inventory": inventory["id"],
                    })
                    continue
                entry, flag = _entry_from_record(record, inventory, inventory_path, root)
                if flag:
                    incomplete.append(entry)
                else:
                    research.append(entry)
                    sources.setdefault(entry["path"], {
                        "path": entry["path"], "hash": entry["hash"],
                        "bytes": (root / entry["path"]).stat().st_size,
                    })

    issue_path = root / ISSUE_NAMED_PATH
    return {
        "canonical_package_path": CANONICAL_PACKAGE_PATH,
        "issue_named_path": ISSUE_NAMED_PATH,
        "issue_named_path_exists": issue_path.exists(),
        "path_policy": "EXISTING_PATH_IS_CANONICAL_NOT_MOVED",
        "fitted_calibration": False,
        "independently_calibrated": False,
        "actionable_status": "NOLINE",
        "actionable_quotes": [],
        "package_saved_quotes": package,
        "research_quotes": research,
        "incomplete": incomplete,
        "counts": {
            "research": len(research),
            "actionable": 0,
            "incomplete": len(incomplete),
        },
        "sources": sorted(sources.values(), key=lambda item: item["path"]),
        "validation_claim": "NONE",
        "note": (
            "Research quotes are saved inventory only. Actionable quotes stay empty "
            "(NOLINE) until an authenticated refresh succeeds. Fitted calibration "
            "remains false until the live holdout (NFL-7) is graded."
        ),
    }


def match_provenance(quote) -> dict:
    """Complete book / as-of / path / hash fields for a matched QuoteRecord."""
    return {
        "book": quote.book,
        "as_of": quote.last_update_utc,
        "path": quote.source_file,
        "hash": quote.source_sha256,
        "source_file": quote.source_file,
        "source_sha256": quote.source_sha256,
        "row_number": quote.row_number,
        "snapshot_source": quote.snapshot_source,
        "pulled_utc": quote.pulled_utc,
        "last_update_utc": quote.last_update_utc,
    }
