# Week 9 1:00 p.m. ET live quarter/PBP snapshot

Captured 2026-11-08 14:45:40 ET. Live CBS clocks differed by game page retrieval time; each game-state field carries the page's clock, so this is a near-live snapshot rather than one synchronized instant. Sources are linked per game.

“Quarter spread” below means actual quarter scoring margin (away points minus home points), not a sportsbook handicap or odds quote. A partial quarter is not a final winner. The PBP CSV contains scoring plays only; full drive/play logs are linked in the source URLs.

| Game | Q1 (away-home; margin) | Q2 (away-home; margin/status) | Q3 so far | Game at capture |
|---|---|---|---|---|
| Browns–Saints | 0–3 (-3; NO) | 3–0 (+3; CLE), final | — | Halftime 3–3 |
| Cowboys–Colts | 3–7 (-4; IND) | 7–0 (+7 DAL, partial) | — | Q2 1:12, DAL 10–IND 7 |
| Broncos–Panthers | 10–0 (+10 DEN) | 0–7 (-7 CAR, partial) | — | Q2 0:04, DEN 13–CAR 7 |
| Lions–Dolphins | 3–3 (tie) | 3–0 (+3 DET), final | 3–0 (+3 DET, partial) | Q3 9:14, DET 9–MIA 3 |
| Giants–Eagles | 6–8 (-2; PHI) | 0–0 (partial) | — | Q2 0:27, NYG 6–PHI 8 |
| Jets–Chiefs | 6–0 (+6 NYJ) | 6–14 (-8 KC, partial) | — | Q2 1:41, NYJ 12–KC 14 |
| Rams–Commanders | 3–3 (tie) | 0–7 (-7 WAS, partial) | — | Q2 1:33, LAR 3–WAS 10 |

## Current scoring play log
Scoring event details are in `WEEK9_1PM_SCORING_PLAYS_20261108_1445ET.csv`. Per-game full PBP references:

- Browns–Saints: https://www.cbssports.com/nfl/gametracker/playbyplay/NFL_20261108_CLE@NO/
- Cowboys–Colts: https://www.cbssports.com/nfl/gametracker/playbyplay/NFL_20261108_DAL@IND/
- Broncos–Panthers: https://www.cbssports.com/nfl/gametracker/playbyplay/NFL_20261108_DEN@CAR/
- Lions–Dolphins: https://www.cbssports.com/nfl/gametracker/playbyplay/NFL_20261108_DET@MIA/
- Giants–Eagles: https://www.cbssports.com/nfl/gametracker/playbyplay/NFL_20261108_NYG@PHI/
- Jets–Chiefs: https://www.cbssports.com/nfl/gametracker/playbyplay/NFL_20261108_NYJ@KC/
- Rams–Commanders: https://www.cbssports.com/nfl/gametracker/playbyplay/NFL_20261108_LAR@WAS/

Full per-quarter score rows (including partial quarter flags) are in `WEEK9_1PM_QUARTER_SCORES_20261108_1445ET.csv`. This is a midgame checkpoint; refresh after games finish before computing final quarter winners or calibration metrics.
