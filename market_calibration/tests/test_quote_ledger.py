"""NFL-45: complete book / as-of / path / hash ledger; canonical path; no fitted claim."""
from hashlib import sha256
from pathlib import Path

from market_calibration.quote_ledger import (
    CANONICAL_PACKAGE_PATH, ISSUE_NAMED_PATH, REQUIRED_FIELDS,
    build_quote_provenance_ledger, entry_complete, file_sha256, match_provenance,
)
from market_calibration.manifest import validate_manifest
from market_calibration.calibration import CalibrationBias
import json


ROOT = Path(__file__).resolve().parents[2]
PKG = Path(__file__).resolve().parents[1]


def test_canonical_path_is_market_calibration_and_is_not_moved():
    ledger = build_quote_provenance_ledger(ROOT)
    assert ledger["canonical_package_path"] == CANONICAL_PACKAGE_PATH == "market_calibration"
    assert ledger["issue_named_path"] == ISSUE_NAMED_PATH == "research/market_calibration"
    assert ledger["path_policy"] == "EXISTING_PATH_IS_CANONICAL_NOT_MOVED"
    assert (ROOT / CANONICAL_PACKAGE_PATH / "quotes.py").is_file()
    assert not (ROOT / ISSUE_NAMED_PATH).exists()
    assert ledger["issue_named_path_exists"] is False


def test_fitted_and_actionable_claims_stay_false():
    ledger = build_quote_provenance_ledger(ROOT)
    assert ledger["fitted_calibration"] is False
    assert ledger["independently_calibrated"] is False
    assert ledger["actionable_status"] == "NOLINE"
    assert ledger["actionable_quotes"] == []
    assert ledger["counts"]["actionable"] == 0
    assert ledger["validation_claim"] == "NONE"
    manifest = json.loads((PKG / "MANIFEST.json").read_text())
    validate_manifest(manifest, PKG)
    assert manifest["calibration"]["fitted"] is False
    assert manifest["calibration"]["status"] == "UNIMPLEMENTED_NO_FITTED_CALIB"
    assert manifest["canonical_package_path"] == "market_calibration/"
    assert CalibrationBias.fitted is False
    assert CalibrationBias().coefficients is None


def test_every_research_quote_has_book_as_of_path_and_hash():
    ledger = build_quote_provenance_ledger(ROOT)
    assert ledger["counts"]["research"] >= 132
    assert ledger["package_saved_quotes"]["status"] == "ABSENT_NOLINE"
    assert ledger["counts"]["incomplete"] == 0
    seen = set()
    for entry in ledger["research_quotes"]:
        assert entry_complete(entry)
        for key in REQUIRED_FIELDS:
            assert entry[key]
        assert entry["book"] in {"fanduel", "draftkings", "pinnacle"}
        assert entry["as_of"].endswith("Z") or "+" in entry["as_of"]
        assert entry["scope"] == "research"
        assert entry["actionable_status"] == "NOLINE"
        path = ROOT / entry["path"]
        assert path.is_file(), entry["path"]
        assert file_sha256(path) == entry["hash"]
        seen.add((entry["inventory"], entry["path"], entry["row_number"], entry["book"], entry["as_of"]))
    assert len(seen) == len(ledger["research_quotes"])
    inventories = {entry["inventory"] for entry in ledger["research_quotes"]}
    assert inventories == {"certified_asof", "asof_sources"}
    asof = [e for e in ledger["research_quotes"] if e["inventory"] == "asof_sources"]
    certified = [e for e in ledger["research_quotes"] if e["inventory"] == "certified_asof"]
    assert len(asof) == 132
    assert len(certified) == 68


def test_source_hashes_are_recomputed_not_invented():
    ledger = build_quote_provenance_ledger(ROOT)
    assert ledger["sources"]
    for source in ledger["sources"]:
        path = ROOT / source["path"]
        assert path.is_file()
        digest = sha256(path.read_bytes()).hexdigest()
        assert source["hash"] == digest
        assert source["bytes"] == path.stat().st_size


def test_hash_mismatch_is_fail_closed(tmp_path):
    # A recorded digest that does not match the file must not enter the complete ledger.
    inventory = tmp_path / "records"
    snaps = tmp_path / "snapshots"
    inventory.mkdir()
    snaps.mkdir()
    csv_path = snaps / "odds.csv"
    csv_path.write_text("book,price\ndraftkings,-110\n")
    record = [{
        "book": "draftkings",
        "actionable_status": "NOLINE",
        "status": "SAVED_ONLY",
        "source_path": "snapshots/odds.csv",
        "source_row_number": 2,
        "source_sha256": "0" * 64,
        "raw_quote_fields": {
            "book": "draftkings",
            "last_update_utc": "2026-11-06T01:12:01Z",
            "pulled_utc": "2026-11-06T01:12:42Z",
        },
    }]
    (inventory / "DK_saved_quotes.json").write_text(json.dumps(record))
    # Point a one-off inventory by calling the internal helper via a patched build is heavy;
    # instead, assert the helper flags HASH_MISMATCH directly.
    from market_calibration.quote_ledger import _entry_from_record
    entry, flag = _entry_from_record(
        record[0],
        {"id": "fixture", "base": "", "records_dir": "records", "files": ("DK_saved_quotes.json",)},
        inventory / "DK_saved_quotes.json",
        tmp_path,
    )
    assert flag == "HASH_MISMATCH"
    assert not entry_complete(entry)
    assert entry["hash"] == ""


def test_match_provenance_carries_required_fields():
    class Quote:
        book = "pinnacle"
        last_update_utc = "2026-11-04T19:59:09Z"
        source_file = "market_calibration/saved_quotes/odds_jaxbal_game.csv"
        source_sha256 = "a" * 64
        row_number = 2
        snapshot_source = "odds_jaxbal_game.csv"
        pulled_utc = "2026-11-04T19:59:57Z"

    entry = match_provenance(Quote())
    for key in REQUIRED_FIELDS:
        assert entry[key]
    assert entry["book"] == "pinnacle"
    assert entry["as_of"] == Quote.last_update_utc
    assert entry["hash"] == "a" * 64
    assert entry["source_file"] == entry["path"]
    assert entry["source_sha256"] == entry["hash"]
