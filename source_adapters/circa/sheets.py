"""Circa Sports official betting sheets: free, public, no account (NFL-40 / NFL-33 sharp-book tier).

Circa publishes its betting sheets as PDFs in a public "Media Resources" Dropbox folder, linked from
https://www.circasports.com/betting-menu-odds . Circa says the sheets are not real-time, and the app is the real-time source.
This adapter downloads the folder zip, keeps football game and prop sheets (NFL weekly, NFL props, CFB weekly, CFB
props) and records provenance for each sheet:
  pulled_utc         when we downloaded it
  sheet_created_utc  the PDF's own CreationDate, i.e. Circa's publish time (the market's as-of stamp)
  zip_entry_time     Dropbox's file time (naive, as reported)
  sha256             of the PDF bytes
The sheets are vector drawings with no text layer, so lines and prices are NOT parsed here (quotes_parsed=False).
Parsing needs an OCR toolchain. Never type prices in by hand without a second check against the PDF.
Run manually only: python -m source_adapters.circa.sheets [--out DIR]. No workflow, no credentials, no paid source."""
from __future__ import annotations

import argparse, hashlib, io, json, re, sys, zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import Request, urlopen

PAGE = "https://www.circasports.com/betting-menu-odds"
FOLDER_ZIP = "https://www.dropbox.com/sh/1irb8ylm07so85c/AADZZxekeKnj1Bphh2XElT5ma?dl=1"
ROOT = Path(__file__).resolve().parents[2]
WANT = [re.compile(p, re.I) for p in (r"^NFL Week \d+ - \d{4}\.pdf$", r"^NFL Props Week \d+\s*- ?\d{4}\.pdf$",
                                       r"^CFB Week \d+ - \d{4}\.pdf$", r"^CFB Props - \d{4}-\d{2}-\d{2}\.pdf$")]


def wanted(name: str) -> bool:
    return any(p.match(Path(name).name) for p in WANT)


def _pdfdate(raw: bytes | None):
    if not raw:
        return None
    m = re.match(rb"D:(\d{14})(Z|[+-]\d{2}'?\d{2}'?)?", raw)
    if not m:
        return None
    d = datetime.strptime(m.group(1).decode(), "%Y%m%d%H%M%S")
    tz = (m.group(2) or b"Z").decode().replace("'", "")
    off = timedelta(0) if tz in ("Z", "") else timedelta(hours=int(tz[1:3]), minutes=int(tz[3:5] or 0)) * (1 if tz[0] == "+" else -1)
    return (d - off).replace(tzinfo=timezone.utc).isoformat()


def pdf_dates(b: bytes) -> dict:
    c = re.search(rb"/CreationDate\s*\(([^)]*)\)", b)
    m = re.search(rb"/ModDate\s*\(([^)]*)\)", b)
    return {"created_utc": _pdfdate(c.group(1) if c else None), "modified_utc": _pdfdate(m.group(1) if m else None)}


def capture(zbytes: bytes, out: Path, pulled_utc: str) -> dict:
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    seen, sheets = set(), []
    with zipfile.ZipFile(io.BytesIO(zbytes)) as z:
        for info in sorted(z.infolist(), key=lambda i: i.filename):
            name = Path(info.filename).name
            if info.is_dir() or not wanted(name):
                continue
            data = z.read(info)
            h = hashlib.sha256(data).hexdigest()
            if (name, h) in seen:
                continue
            seen.add((name, h))
            (out / name).write_bytes(data)
            d = pdf_dates(data)
            chk = "UNKNOWN_NO_SHEET_TIMESTAMP" if d["created_utc"] is None else (
                "FAIL_PULLED_BEFORE_SHEET_CREATED" if pulled_utc < d["created_utc"] else "OK")
            sheets.append({"file": name, "sha256": h, "bytes": len(data), "sheet_created_utc": d["created_utc"],
                           "sheet_modified_utc": d["modified_utc"], "zip_entry_time": "%04d-%02d-%02dT%02d:%02d:%02d" % info.date_time,
                           "pulled_utc": pulled_utc, "timestamp_check": chk})
    m = {"source": "Circa Sports official betting sheets (public Dropbox folder linked from " + PAGE + ")",
         "url": FOLDER_ZIP, "access": "free, public, no account", "realtime": False,
         "quotes_parsed": False, "parse_status": "not parsed: PDFs have no text layer; needs OCR plus a human check",
         "sheets": sheets}
    (out / "MANIFEST.json").write_text(json.dumps(m, indent=2) + "\n")
    return m


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    with urlopen(Request(FOLDER_ZIP, headers={"User-Agent": "nfl-matchup-database/circa-sheets"}), timeout=120) as r:
        zb = r.read()
    pulled = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    out = Path(a.out) if a.out else ROOT / "source_adapters/circa/captures" / pulled.replace(":", "")
    m = capture(zb, out, pulled)
    print(json.dumps({"out": str(out), "sheets": [(s["file"], s["sheet_created_utc"], s["timestamp_check"]) for s in m["sheets"]]}, indent=1))


if __name__ == "__main__":
    sys.exit(main())
