"""Build market rows from a Circa sheet capture (NFL-40 / NFL-33). Manual run only; no network, no credits.

  python -m source_adapters.circa.build_rows source_adapters/circa/captures/<stamp> [--out DIR] [--tokens-cache DIR]

Reads the capture's MANIFEST.json for provenance, OCRs each NFL sheet (source_adapters.circa.ocr), parses the
layouts (source_adapters.circa.parse) and writes rows.csv + PARSE_REPORT.json. Every row carries the source URL, the
sheet file and sha256, the sheet's publish time (PDF CreationDate, UTC), the sheet's own printed 'Updated' stamp as
OCR'd, and the pull time. CFB sheets are captured but not parsed here (NFL scope).
"""
from __future__ import annotations

import argparse, csv, gzip, hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path

from source_adapters.circa import parse as P

PARSER_VERSION = "circa-ocr-1"
NFL_PREFIX = ("NFL Week", "NFL Props")
FIELDS = ["source", "source_url", "sheet_file", "sheet_sha256", "sheet_created_utc", "sheet_updated_printed_ocr", "pulled_utc",
          "parsed_utc", "parser_version", "layout", "page", "section", "game_date", "kickoff_raw_ocr", "away_rot", "home_rot",
          "away", "home", "period", "market", "prop", "player", "team", "side", "side_rot", "line", "price", "price_printed",
          "line_derived", "side_basis"]


def rows_for_sheet(tokens, sheet: dict, manifest: dict, parsed_utc: str):
    rows, report = P.parse_tokens(tokens)
    upd = P.updated_stamp(tokens)
    out = []
    for r in rows:
        d = r.as_dict()
        out.append({
            "source": "Circa Sports betting sheet (public PDF)", "source_url": manifest.get("url", ""),
            "sheet_file": sheet["file"], "sheet_sha256": sheet["sha256"], "sheet_created_utc": sheet.get("sheet_created_utc"),
            "sheet_updated_printed_ocr": upd, "pulled_utc": sheet.get("pulled_utc"), "parsed_utc": parsed_utc,
            "parser_version": PARSER_VERSION, "layout": d["layout"], "page": d["page"], "section": d["section"],
            "game_date": d["game_date"], "kickoff_raw_ocr": d["kickoff_raw"], "away_rot": d["away_rot"], "home_rot": d["home_rot"],
            "away": d["away"], "home": d["home"], "period": d["period"], "market": d["market"], "prop": d["prop"],
            "player": d["player"], "team": d["team"], "side": d["side"], "side_rot": d["side_rot"], "line": d["line"],
            "price": d["price"], "price_printed": d["price_printed"], "line_derived": d["line_derived"], "side_basis": d["side_basis"]})
    return out, report, upd


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("capture")
    ap.add_argument("--out")
    ap.add_argument("--tokens-cache", help="read/write OCR tokens here (json.gz per sheet)")
    a = ap.parse_args(argv)
    cap = Path(a.capture)
    man = json.loads((cap / "MANIFEST.json").read_text())
    out = Path(a.out) if a.out else cap / "parsed"
    out.mkdir(parents=True, exist_ok=True)
    parsed_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    all_rows, report = [], {"parser_version": PARSER_VERSION, "parsed_utc": parsed_utc, "capture": cap.name, "sheets": []}
    for s in man["sheets"]:
        entry = {"file": s["file"], "sha256": s["sha256"], "sheet_created_utc": s.get("sheet_created_utc")}
        if not s["file"].startswith(NFL_PREFIX):
            entry.update(status="not parsed (CFB sheet; NFL scope only)")
            report["sheets"].append(entry); continue
        pdf = cap / s["file"]
        if hashlib.sha256(pdf.read_bytes()).hexdigest() != s["sha256"]:
            entry.update(status="FAIL sha256 mismatch vs MANIFEST"); report["sheets"].append(entry); continue
        tok = None
        if a.tokens_cache:
            cp = Path(a.tokens_cache) / (s["sha256"][:16] + ".tokens.json.gz")
            if cp.exists():
                tok = json.loads(gzip.decompress(cp.read_bytes()))
        if tok is None:
            from source_adapters.circa import ocr
            tok = [t.as_dict() for t in ocr.pdf_tokens(pdf)]
            if a.tokens_cache:
                Path(a.tokens_cache).mkdir(parents=True, exist_ok=True)
                cp.write_bytes(gzip.compress(json.dumps(tok).encode()))
        rows, rep, upd = rows_for_sheet(tok, s, man, parsed_utc)
        all_rows.extend(rows)
        entry.update(status="parsed", rows=len(rows), updated_printed_ocr=upd,
                     pages={str(k): v for k, v in rep.items()},
                     prices_printed=sum(1 for r in rows if r["price_printed"]),
                     prices_not_printed=sum(1 for r in rows if not r["price_printed"]),
                     derived_lines=sum(1 for r in rows if r["line_derived"]))
        report["sheets"].append(entry)
    with open(out / "rows.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(all_rows)
    report["rows_total"] = len(all_rows)
    (out / "PARSE_REPORT.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("rows_total", "parsed_utc")} | {"sheets": [(e["file"], e["status"], e.get("rows")) for e in report["sheets"]]}, indent=1))


if __name__ == "__main__":
    sys.exit(main())
