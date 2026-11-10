# 2026 Week 9 official gamebooks

Fifteen owner-supplied NFL Game Summaries. One folder per nflverse `game_id`. `MANIFEST.csv` is the fetch list: source URL on `static.www.nfl.com`, sha256, pages, and the final score read from the PDF. The links were taken from each NFL.com Game Center "Download Game Book (PDF)" control at about 12:32 AM ET on 2026-11-10.

`combined/` stacks every per-game CSV. The game id column is `nflverse_game_id`.

`team_abbr` is the code printed in the book. That differs from the nflverse id for Arizona (`ARZ` / `ARI`), Baltimore (`BLT` / `BAL`), Cleveland (`CLV` / `CLE`), and Houston (`HST` / `HOU`). Rams and Washington are `LA` and `WAS` in both the book and these ids.

Cincinnati at Atlanta is the Madrid game. The PDF opens with `2026 Madrid Game` instead of the usual title line. The venue is Bernabéu Stadium, kickoff 3:34 PM CET, retractable roof closed. Final 34–17.

Cleveland at New Orleans went to overtime, 22–23. Those overtime rows use `scope=overtime` and play-by-play quarter `OT`. They are not added into the final stat lines.

For six books (CIN@ATL, DAL@IND, CLE@NO, NYG@PHI, LA@WAS, TB@CHI), a fresh `pdftotext -layout` with poppler 24.02.0 matches the committed text through the play-by-play and differs only after "Ten Longest Plays". That section is not parsed. The committed text is the owner-supplied extract. Each `provenance.json` records the PDF sha256 and source URL.

Check the week with:

```sh
python3 -m unittest data/gamebooks/tests/test_2026_wk09_gamebooks.py data/gamebooks/tests/test_2026_09_buf_min.py
```
