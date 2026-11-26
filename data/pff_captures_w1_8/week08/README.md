# PFF 2026 NFL Week 8 recap capture

## Coverage
All 14 games listed on the 2026 Week 8 schedule have an accessible recap transcription under `games/`, along with a PDF, extracted text file, and metadata JSON. `manifest.csv` tracks game ID, source URLs, retrieved ET time, section card counts, visible text length, and flags.

For every game, the visible recap iframe text included generated key takeaways and all of these carousel sections/cards through their final card marker: Game Overview (12), Team Rushing Reports (4), Team Passing Reports (11), Quarterback Comparison (5), Player Participation & Snap Counts (4), Initial PFF Grades (12), and Box Score Breakdown (12). These are complete captures of the rendered recap text available in the UI, not a claim that every underlying PFF database item or paid Premium Stats view was accessed.

## Capture method and provenance
Used the supported browser interaction tools to open each schedule-listed 2026 game, select Recap, activate Generate Key Takeaways, and read the rendered recap iframe text. The text was saved as local PDF transcriptions and extracted `.txt` files. These PDFs are not PFF-provided downloads; they are locally generated from visible UI text. A few non-ASCII punctuation glyphs were normalized to ASCII in the PDF transcription (for example, bullets/arrows); numeric values and textual rows were retained. The extracted `.txt` is the most convenient review copy.

PFF-generated hindsight/analysis is preserved as the distinct “Biggest Team Differences” and “Box Score Standouts” block. It is not merged with the measured/report carousel text. Initial PFF grades remain explicitly initial and subject to review.

## Validation and flags
- Every page visibly identified Week 8 and the 2026 season.
- All listed carousel sections ended at their expected last marker (for example, 12/12 or 4/4); no missing-card/count flags were detected.
- Compared the first recap-header final score pair with the visible schedule score for all 14 games; all matched. Titans–Bengals and Cardinals–Cowboys were marked F/OT in the schedule and are retained as such.
- No purchase, subscription change, export, or Git write was performed. Separate Premium Stats locked areas were not accessed or bypassed.

## Prior sample note
The earlier `30713_*_partial.md` file and screenshot preserve the earlier selective sample. The later `30713_*_accessible-recap-text.pdf/.txt` and metadata file are the full accessible recap-text capture for this batch and supersede the partial sample for Week 8 coverage.

Generated-summary comparisons versus the corresponding measured rows were preserved side by side but not exhaustively reconciled metric-by-metric. The manifest's flags therefore cover the tested schedule-score and carousel-marker checks only; do not treat them as a full statistical audit.
