# Official NFL game summaries

Postgame research inputs. Each game lives at `data/gamebooks/{season}/wk{week}/{nflverse_game_id}/`.

The PDF and the `pdftotext -layout` text are the source. `parsed/` holds tidy CSVs produced by `parse_nfl_game_summary.py` (Python standard library only). Printed numbers are copied as text. The parser does not change model weights, formulas, simulators, or `projection_ready`.

2026 Week 9 is `data/gamebooks/2026/wk09/`. `MANIFEST.csv` is the owner fetch list (nflverse game id, NFL.com Game Center PDF URL, sha256, pages, final score). `combined/` is one CSV per table for all 15 games. The game id column is `nflverse_game_id`.

| Game | nflverse id | Final |
| --- | --- | --- |
| Thu Nov 5, Jacksonville at Baltimore | `2026_09_JAX_BAL` | 33–10 |
| Sun Nov 8, Cincinnati at Atlanta (Madrid, Bernabéu) | `2026_09_CIN_ATL` | 34–17 |
| Sun Nov 8, Denver at Carolina | `2026_09_DEN_CAR` | 26–21 |
| Sun Nov 8, Dallas at Indianapolis | `2026_09_DAL_IND` | 27–23 |
| Sun Nov 8, NY Jets at Kansas City | `2026_09_NYJ_KC` | 12–35 |
| Sun Nov 8, Detroit at Miami | `2026_09_DET_MIA` | 19–9 |
| Sun Nov 8, Cleveland at New Orleans (overtime) | `2026_09_CLE_NO` | 22–23 |
| Sun Nov 8, NY Giants at Philadelphia | `2026_09_NYG_PHI` | 19–11 |
| Sun Nov 8, LA Rams at Washington | `2026_09_LA_WAS` | 20–13 |
| Sun Nov 8, Houston at LA Chargers | `2026_09_HOU_LAC` | 44–22 |
| Sun Nov 8, Las Vegas at San Francisco | `2026_09_LV_SF` | 17–38 |
| Sun Nov 8, Green Bay at New England | `2026_09_GB_NE` | 45–27 |
| Sun Nov 8, Arizona at Seattle | `2026_09_ARI_SEA` | 3–17 |
| Sun Nov 8, Tampa Bay at Chicago | `2026_09_TB_CHI` | 24–27 |
| Mon Nov 9, Buffalo at Minnesota | `2026_09_BUF_MIN` | 23–6 |

The gamebook prints ARZ, BLT, CLV, HST, LA, and WAS where the nflverse id uses ARI, BAL, CLE, HOU, LA, and WAS. `team_abbr` keeps the printed code. Cincinnati at Atlanta is the Madrid game: the PDF title line is `2026 Madrid Game`, and the venue is Bernabéu Stadium.

NFL game summaries are media-use documents. Read the README in each game folder before reuse.
