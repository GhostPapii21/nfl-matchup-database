# Official NFL game summaries

Postgame research inputs. Each game lives at `data/gamebooks/{season}/wk{week}/{nflverse_game_id}/`.

The PDF and the `pdftotext -layout` text are the source. `parsed/` holds tidy CSVs produced by `parse_nfl_game_summary.py` (Python standard library only). Printed numbers are copied as text. The parser does not change model weights, formulas, simulators, or `projection_ready`.

| Game | nflverse id | Final |
| --- | --- | --- |
| 2026 Week 9, Buffalo Bills at Minnesota Vikings, Mon Nov 9 2026, U.S. Bank Stadium | `2026_09_BUF_MIN` | BUF 23, MIN 6 |

NFL game summaries are media-use documents. Read the README in each game folder before reuse.
