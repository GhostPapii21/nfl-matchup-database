# Circa betting-sheet parser (refs NFL-40, refs NFL-33)

Circa's public betting sheets (captured by `source_adapters/circa/sheets.py`, PR #71) are vector glyph outlines with
no text layer and a raster watermark. `source_adapters/circa/` now turns the NFL sheets into rows.

## Run (manual only: no network, no credentials, no paid source)

    apt-get install tesseract-ocr && pip install -r requirements-circa-ocr.txt
    python -m source_adapters.circa.build_rows source_adapters/circa/captures/<stamp> --tokens-cache source_adapters/circa/captures/<stamp>/parsed/tokens

Output: `<capture>/parsed/rows.csv`, `<capture>/parsed/PARSE_REPORT.json` and the OCR token cache (json.gz per sheet,
keyed by sheet sha256). The offline tests use the token cache, so CI does not need tesseract.

## How it reads the sheet

1. Delete the raster images (watermark, logo) and render at 600 dpi.
2. Connected components become glyphs; glyphs become words (same text band, small gap; a sign after a digit starts a
   new number, so "-1/2 +125" is two values).
3. Tesseract reads each word twice (full charset, numeric whitelist).
4. Numeric glyphs are classified by pixel templates bootstrapped from the words tesseract read cleanly. That is what
   reads the "1/2" glyph, which tesseract drops or reads as 1 or 4. A glyph that does not match a template is "?"
   and its cell is dropped and reported, never guessed.
5. Layout parsers by page type: weekly game page (full game, 1st half, 1st quarter: spread, total, moneyline), early
   lines page, team totals and player props (stacked rotation pairs), and the anytime-touchdown YES/NO grid.

## Row rules

* Every row has: source URL, sheet file and sha256, `sheet_created_utc` (PDF CreationDate = Circa publish time, the
  as-of stamp), the sheet's own printed "Updated" footer as OCR'd, `pulled_utc` and `parsed_utc`.
* A price Circa did not print is empty (`price_printed=False`). We do not assume -110.
* Circa prints the spread only on the favourite's row. The other side is its negation, flagged `line_derived=True`.
  "PK" is line 0.
* Totals and pair markets: upper stacked price = over, lower = under. This matches the sheet's own convention
  (odd rotation = OVER, printed in the Grand Salami block). `side_basis` records this on every row.
* Player names and kickoff times are raw OCR (e.g. `KYLE MONANGAT`, `'ANDRE SWIFT`) and need a roster join before use.
  Team codes are repaired only to real NFL codes (OCR reads this font's I as T: CHT->CHI); anything else gets a "?" prefix.

## Coverage, capture 2026-11-21T22:55:14Z (pulled), parsed 2026-11-22

| Sheet | Published (UTC) | Rows | Dropped cells |
|---|---|---|---|
| NFL Week 11 - 2026.pdf (game lines p1, team totals p2) | 2026-11-21 19:51:28 | 216 + 48 | 0 |
| NFL Props Week 11- 2026.pdf (props p1, anytime TD p2) | 2026-11-21 19:39:39 | 238 + 144 | 0 |
| NFL Week 12 - 2026.pdf (early lines) | 2026-11-17 20:47:22 | 64 | 0 |
| CFB Week 12 / CFB Props | — | not parsed (NFL scope) | — |

Hand check (2026-11-22, against 170-dpi renders of the PDFs): every Week 11 page-1 cell for all 12 games, all 24
team totals, all 16 Week 12 early lines, the QB TD-pass, QB rushing and RB rushing blocks, and a sample of anytime-TD
prices. No mismatches found. The values pinned in `test_circa_parse.py` come from that check.

Not done: CFB sheets; the NFL props sheet's 1st-TD-scorer and futures PDFs (not captured by sheets.py); a roster join
for OCR'd names. The rows are research input only and are not wired into any model, gate or slip.
