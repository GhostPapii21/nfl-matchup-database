"""NFL-40 / NFL-33 (Circa tier): capture Circa's free official betting-sheet PDFs with provenance.
Offline tests only: a fixture zip stands in for the public Dropbox folder."""
import io, json, zipfile
from pathlib import Path

from source_adapters.circa import sheets as S


def _pdf(created):
    return b"%PDF-1.4\n1 0 obj << /CreationDate (D:" + created + b") /ModDate (D:" + created + b") >> endobj\n%%EOF"


def _zip(entries):
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w") as z:
        for name, data in entries:
            z.writestr(zipfile.ZipInfo(name, (2026, 11, 21, 15, 39, 38)), data)
    return b.getvalue()


def test_pdf_creation_date_parsed_with_offset():
    assert S.pdf_dates(_pdf(b"20261121113939-08'00'"))["created_utc"] == "2026-11-21T19:39:39+00:00"


def test_pdf_without_date_is_unknown():
    assert S.pdf_dates(b"%PDF-1.4 nothing")["created_utc"] is None


def test_only_football_sheets_kept():
    names = ["NFL Week 11 - 2026.pdf", "NFL Props Week 11- 2026.pdf", "CFB Props - 2026-11-21.pdf", "CFB Week 12 - 2026.pdf",
             "NBA - 2026-11-21.pdf", "NFL Futures 2026-27.pdf", "NFL Week 11 - 1st TD Scorer.pdf", "Betting Limits.pdf"]
    kept = sorted(n for n in names if S.wanted(n))
    assert kept == ["CFB Props - 2026-11-21.pdf", "CFB Week 12 - 2026.pdf", "NFL Props Week 11- 2026.pdf", "NFL Week 11 - 2026.pdf"]


def test_capture_writes_files_and_manifest(tmp_path):
    z = _zip([("NFL Props Week 11- 2026.pdf", _pdf(b"20261121113939-08'00'")), ("NBA - 2026-11-21.pdf", _pdf(b"20261121070000-08'00'")),
              ("Dropbox/Circa Sports sheets/NFL Props Week 11- 2026.pdf", _pdf(b"20261121113939-08'00'"))])
    m = S.capture(z, tmp_path, pulled_utc="2026-11-21T23:00:00+00:00")
    assert [e["file"] for e in m["sheets"]] == ["NFL Props Week 11- 2026.pdf"]   # duplicate path deduplicated by name+hash
    e = m["sheets"][0]
    assert e["sheet_created_utc"] == "2026-11-21T19:39:39+00:00"
    assert e["pulled_utc"] == "2026-11-21T23:00:00+00:00"
    assert len(e["sha256"]) == 64 and (tmp_path / e["file"]).exists()
    assert m["quotes_parsed"] is False and "OCR" in m["parse_status"]
    assert json.loads((tmp_path / "MANIFEST.json").read_text()) == m


def test_capture_rejects_pull_older_than_sheet(tmp_path):
    z = _zip([("NFL Week 11 - 2026.pdf", _pdf(b"20261121115128-08'00'"))])
    m = S.capture(z, tmp_path, pulled_utc="2026-11-21T10:00:00+00:00")
    assert m["sheets"][0]["timestamp_check"] == "FAIL_PULLED_BEFORE_SHEET_CREATED"
