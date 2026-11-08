# Week 9 1 PM games: per-game receiver, defense, and quarter audit

**Captured:** 2026-11-08 15:52 ET / 20:52 UTC.  
**Purpose:** create a reusable opponent profile from each game: which position produced, which receiving opportunities converted, what the team did by quarter, and what the available PBP can and cannot say about defenders. This is a live diagnostic log, not a recalibration or a bet recommendation.

## Snapshot and interpretation rules

- The DraftKings Scores connector returned a game/quarter snapshot at **20:52:23Z**. Current-quarter points are partial for games marked Live; they are not final quarter results.
- CBS Gametracker pages were fetched in the same research pass, but their displayed game states are behind the DraftKings score feed for CLE–NO, DEN–CAR, NYG–PHI, and LAR–WAS. CBS player/team statistics below are labeled **CBS page snapshot** and must not be combined with a later score as if synchronized. DAL–IND, NYJ–KC, and DET–MIA were aligned at the score level at retrieval.
- Baselines are pregame Week 1–8 verified history already in the repo. Where shown as “L5,” it is the historical last-five game average (including recorded zero stat games); it is a comparison point, not a calibrated projection.
- **Explosive = 20+ yards from scrimmage on one play.** This audit adds two verified plays absent from the 15:12 CSV. The resulting 14-play set is still provisional until a complete postgame PBP sweep is performed.
- PBP contact/tackle names identify players recorded at the end of a play. They do **not** prove individual coverage responsibility. No nearest-defender attribution is treated as “yards allowed.”
- Standard play-by-play does not provide defensively charted MFO/MFC shell, man/zone rates, blitz rate, or pressure rate. Sacks are logged separately and are not a substitute for those rates.

## Seven-game board

| Game | Score feed at 15:52 ET | Q1 | Q2 | Q3 | Q4 | Status |
|---|---:|---:|---:|---:|---:|---|
| CLE at NO | CLE 13–9 | NO +3 | CLE +3 | Tie | CLE +4* | Live |
| DAL at IND | DAL 20–17 | IND +4 | DAL +14 | IND +7 | Tie* | Live |
| DEN at CAR | DEN 26–14 | DEN +10 | CAR +4 | CAR +7 | DEN +13* | Live |
| DET at MIA | DET 19–9 | Tie | DET +3 | DET +7 | Tie | Final |
| NYG at PHI | NYG 16–8 | PHI +2 | Tie | NYG +7 | NYG +3* | Live |
| NYJ at KC | KC 28–12 | NYJ +6 | KC +8 | KC +14 | Tie* | Live |
| LAR at WAS | LAR 20–13 | Tie | WAS +4 | LAR +4 | LAR +7* | Live |

*Q4 values are incomplete at retrieval. Quarter margins come from the returned score-by-period fields and should be rechecked at final.

## CLE at NO

**Current quarter/score snapshot:** DraftKings feed CLE 13–9, late Q4. CBS page remains at CLE 6–6 through Q3, so its player and team-stat table is an earlier snapshot.

**Explosives against New Orleans:** Denzel Boston (WR), 60-yard catch in Q3. The PBP names K. McKinstry at the play’s finish; this does not establish McKinstry as the coverage assignment. Among the previously captured set, this is the longest WR explosive in the seven-game window.

**Receiver opportunity and baseline:** CBS snapshot Boston 4 targets, 3 catches, 71 yards; Week 1–8 L5 baseline 3.4 catches / 42.8 receiving yards. The 60-yard play accounts for most of the yardage lift: this is an explosive-play profile, not high catch volume. Chris Olave had 8 targets, 5 catches, 58 yards; L5 baseline 6.2 catches / 73.6 yards. Olave received target volume above his catch count but fell short in both catches and yards. The 62.5% catch conversion alone does not distinguish quarterback accuracy, receiver drops, coverage, or throwaways; play-level charting is needed.

**Team/QB context from CBS snapshot:** Shedeur Sanders 9/15, 120 pass yards, 0 TD/0 INT; Tyler Shough 10/18, 156, 0/0. Third down CLE 4/12, NO 2/8; red zone CLE 0/2, NO 0/3; two Saints fumbles lost shown. Score-feed sacks: 5 each. Pressure/blitz rate unavailable.

**Defensive position takeaway:** NO allowed a WR explosive; CLE also allowed explosive receiving production to a WR. No source-backed shell, man/zone rate, or individual coverage assignment is present in this PBP pull.

## DAL at IND

**Score:** score feed and CBS page both show DAL 20–17 at retrieval. DraftKings has the game live in Q4; CBS team totals are a separate capture.

**Explosives against Indianapolis:** Jonathan Mingo (WR) 23 yards; CeeDee Lamb (WR) 22 yards and a 44-yard TD. Three WR explosives, 89 combined yards. PBP contact names in the existing event CSV: K. Harris / H. Wohler for Mingo; B. Boettcher for the 22-yard Lamb catch; the TD scoring line does not identify a coverage defender. A separate 48-yard Lamb play late in the CBS PBP was reversed after a fumble and must **not** be counted as a completed explosive.

**Receiver opportunity and baseline:** Lamb 11 targets, 7 catches, 155 yards, 1 TD in the CBS player table; Week 1–8 L5 baseline 8 catches / 80 yards. He exceeded yardage by 75 despite two fewer catches than baseline: high explosive yield, not extra catch volume. Mingo 3 targets, 1 catch, 23 yards; L5 record is too thin in the model baseline to treat as stable. Jake Ferguson 2 targets, 2 catches, 21 yards, TD; L5 receiving-yards baseline 13.2.

**Team/QB context:** Prescott 17/27, 249, 2 TD/0 INT in CBS; historical L5 passing-yards baseline 263.2. Daniel Jones 17/26, 154, 1/0. Team net yards DAL 392–IND 190; 3rd down DAL 5/14, IND 3/10; red zone DAL 1/2, IND 1/1. Score-feed sacks: IND defense 3, DAL defense 2. No blitz/pressure rate available.

**Defensive position takeaway:** Indianapolis has given up repeated explosive receiving plays to WRs in this game. That can inform future WR archetype comparisons, but player coverage assignment is not proven by tackle/contact names.

## DEN at CAR

**Score:** DraftKings current score DEN 26–14, Q4; CBS stat page shows an earlier 13–14 through Q3. Treat CBS player/team stats as earlier.

**Explosives against Denver:** Tetairoa McMillan (WR) 20; Chuba Hubbard (RB rush) 23; Darren Waller (TE) 21. Three plays / 64 yards across three position groups. PBP contact names: P. Surtain on McMillan, T. Rapp on Hubbard, J. Skinner on Waller. Those are contacts, not verified coverage assignments.

**Receiver opportunity and baseline:** McMillan 4 targets, 2 catches, 32 yards in CBS; L5 baseline 6.4 catches / 78.6 yards. An explosive catch did not produce normal volume. Waller 8 targets, 7 catches, 90 yards, TD; historical L5 receiving-yard baseline 29.6, a large breakout relative to recent production. Hubbard had 16 carries / 79 rushing yards in CBS; L5 rushing-yard baseline 87.6, below baseline at that snapshot, while his 23-yard run supplied an explosive component.

**Team/QB context:** Nix 22/33, 190, 1 TD/1 INT; Young 19/25, 189, 2 TD/1 INT. Team net yards DEN 233–CAR 285; third down DEN 4/7, CAR 3/7; red zone DEN 1/4, CAR 2/3. Score-feed sacks: 1 each. The completion rate/yard totals do not provide blitz rate or pressure timing.

**Defensive position takeaway:** Denver allowed a WR, RB, and TE explosive. Carolina’s TE Waller is the receiving outlier in the CBS snapshot. This is the clearest single-game evidence in this set that the matchup can be position-specific rather than “the defense is weak against receivers” generally.

## DET at MIA

**Final score:** DET 19–9. CBS and score feed agree.

**Explosives:** Miami WR Caleb Douglas 20 and RB Keaton Allen 46 receiving yards allowed by Detroit. Detroit WR Jameson Williams 31 receiving yards allowed by Miami. PBP contact names: Douglas—R. McCreary and B. Branch; Keaton Allen—J. Bachie and T. Martin; Jameson Williams—D. Trader. These remain contact names, not coverage assignments. Position totals: WR 2 plays / 51 yards, RB 1 / 46.

**Receiver opportunity vs baseline:** Amon-Ra St. Brown 10 targets, 8 catches, 86 yards; Week 1–8 L5 baseline 6.8 catches / 72.4 yards, so he cleared both historical averages. Sam LaPorta 5 targets, 4 catches, 32 yards; L5 4 catches / 53.4 yards—normal receptions, lower yards per catch. Jared Goff 17/25, 170, 0 pass TD, 1 INT; L5 passing-yard baseline 286.2, a large underperformance even with Amon-Ra’s volume and catch efficiency. Gibbs 19 carries, 72 yards, 1 TD against an L5 rushing-yard baseline of 113.0. Miami’s Caleb Douglas 8 targets, 6 catches, 70 yards; Keaton Allen 1 target, 1 catch, 46 yards.

**Team context:** Total yards DET 269–MIA 228; third down DET 3/11, MIA 4/12; red zone DET 1/3, MIA 0/3. This final game shows the receiver/QB distinction the audit is meant to capture: Amon-Ra exceeded his receiving baseline while Goff’s passing yardage did not; separate play-level review is needed before assigning that difference to pressure or pass accuracy. Pressure/blitz counts unavailable from this standard PBP snapshot.

## NYG at PHI

**Score conflict:** DraftKings feed NYG 16–8 in Q4; CBS page and player/team tables show NYG 13–8 through Q3. CBS also shows no Q4 scoring, so this game’s latest event state is unresolved between feeds.

**Explosives against NYG:** Darius Cooper (WR) 20 yards for Philadelphia; contact names A. Washington and A. Reese. Cooper’s CBS line: 6 targets, 2 catches, 25 yards. Week 1–8 L5 baseline 1.8 catches / 29.8 yards. He had an explosive gain and target volume but low catch conversion (2/6); do not attribute the other four targets to QB or receiver without reviewing play outcome labels.

**Other receiving production:** NYG Malik Nabers 7 targets, 5 catches, 43 yards vs L5 8.2 catches / 107 yards; he was below baseline despite a 71% catch rate. TE Isaiah Likely 6 targets, 5 catches, 53 yards, TD—TE led the team’s receiving output in the CBS snapshot. QB stats there: J.J. McCarthy 12/18, 128; Jameis Winston 6/8, 71, TD; Philadelphia’s Jalen Milton III 10/19, 98, and 36 rush yards. Team yards NYG 229–PHI 131; third down 6/14 vs 3/12; red zone 1/1 each. Score-feed sacks: PHI defense 6, NYG defense 5.

**Defensive position takeaway:** The logged explosive is a WR play allowed by NYG; the largest PHI pass production in the CBS snapshot came from a TE. This suggests two different matchup signals, not a single one. Coverage structure and direct assignments remain unknown.

## NYJ at KC

**Score:** DraftKings and CBS both show KC 28–12, live Q4 at retrieval.

**Explosive against New York:** Kenneth Walker III (RB) 25-yard receiving TD. PBP scoring line does not name a defender in coverage. KC also completed a 7-yard TD to Walker. Walker CBS line: 18 carries / 102 rush yards / 1 rush TD, plus 4 targets / 4 catches / 41 receiving yards / 2 receiving TDs. Week 1–8 L5 baseline 2.6 catches / 10.4 receiving yards / 96.0 rushing yards. He had a large receiving-game spike and modestly exceeded the rushing baseline. Travis Kelce: 3 catches / 67 yards; L5 3.4 catches / 47.6 yards—yardage exceeded with slightly fewer receptions.

**QB and team context:** Geno Smith 16/27, 138, 0 TD/0 INT; Patrick Mahomes 22/30, 237, 2 TD/0 INT in CBS. Team net yards NYJ 201–KC 360; third down 2/11 vs 4/9; red zone NYJ 0/1, KC 3/3. Score-feed sacks: KC defense 5, NYJ defense 2. Sacks support that KC generated QB disruption, but do not tell us blitz frequency or pressure at decision time.

**Defensive position takeaway:** KC’s RB receiving usage generated the one logged explosive against NYJ; KC’s own offense had a high red-zone conversion snapshot. This is a clear RB receiving matchup example, not evidence of NYJ’s overall RB coverage rate.

## LAR at WAS

**Score conflict:** DraftKings feed shows LAR 20–13 in Q4; CBS remains 13–13 through Q3. The current Q4 event is not in CBS’s displayed game totals.

**Explosives:** Washington RB Rachaad White 45-yard reception against LAR; contact names K. Curl and O. Speights. Rams WR Puka Nacua 21-yard catch against WAS; contact name S. Styles. Puka’s CBS line: 18 targets, 13 catches, 143 yards; Week 1–8 L5 baseline 10.2 catches / 98.2 yards, well above both. White: 3 targets, 2 catches, 41 credited receiving yards, long 45 (the PBP gain and final credited total differ by 4 yards; retain both with source fields, do not silently reconcile). Van Jefferson 3/25/TD for Washington. Rams RB split: Blake Corum 8/52/TD rushing; Kyren Williams 10/36 rushing plus 3/16 receiving.

**QB and team context:** Stafford 25/40, 221, 0 TD/1 INT in CBS vs historical L5 passing-yard baseline 254.8; Jayden Daniels 13/17, 131, 1 TD/0 INT. Total yards LAR 301–WAS 182; third down 2/11 vs 1/7; red zone LAR 1/3, WAS 1/2. Score-feed sacks: LAR defense 2, WAS defense 1. Puka’s output was strong despite Stafford below his historical yardage baseline; do not treat the WR result as proof that QB pressure was absent.

## Matchup and video evidence that is still open

| Evidence | Captured | Still required |
|---|---|---|
| Explosive play position and gain | 14 identified events in the companion CSV, threshold 20+ | Full postgame PBP scan for each game; current set is not yet declared exhaustive |
| Defender who covered the receiver | None verified from standard PBP | PFF/PFF charting or tracking assignment, or manual video charting |
| PBP contact/tackler names | Logged where CBS lists them | Never relabel as coverage assignment without film/chart support |
| MFO/MFC, man/zone rates | Not supplied by standard game tracker | Charted coverage source with definition and sample denominator |
| Blitz/pressure rate and decision timing | Not supplied; score feed only gives some sack totals | Per-play charted pressure/blitz data; sack totals are outcomes, not rates |
| Routes, route participation, target-per-route | Not in these PBP tables | Verified route/snap source |
| Official NFL YouTube highlights | Search of official NFL highlight channel/page returned the Bengals–Falcons early-game clips; no Week 9 1 PM matchup-specific NFL YouTube highlight surfaced in the indexed search at this capture | Recheck after the six remaining live games finish; review each scoring/explosive play and log video timecode, shell, alignment, defender(s), and confidence |
| Projection scoring | Detroit only is final; remaining six are live or status-conflicted | Final box/PBP and a frozen pregame projection row for every player/market before hit/miss scoring |

**No projection or calibration parameters were changed.** These logs are postgame research inputs. Keep calibration and production readiness false until the established untouched forward test passes.

## Source ledger

- CBS Gametracker PBP and box/player/team tables (one URL per matchup):
  - [CLE–NO](https://www.cbssports.com/nfl/gametracker/playbyplay/NFL_20261108_CLE@NO/)
  - [DAL–IND](https://www.cbssports.com/nfl/gametracker/playbyplay/NFL_20261108_DAL@IND/)
  - [DEN–CAR](https://www.cbssports.com/nfl/gametracker/playbyplay/NFL_20261108_DEN@CAR/)
  - [DET–MIA](https://www.cbssports.com/nfl/gametracker/playbyplay/NFL_20261108_DET@MIA/)
  - [NYG–PHI](https://www.cbssports.com/nfl/gametracker/playbyplay/NFL_20261108_NYG@PHI/)
  - [NYJ–KC](https://www.cbssports.com/nfl/gametracker/playbyplay/NFL_20261108_NYJ@KC/)
  - [LAR–WAS](https://www.cbssports.com/nfl/gametracker/playbyplay/NFL_20261108_LAR@WAS/)
- Official NFL video index: [NFL Game Highlights](https://www.nfl.com/videos/channel/game-highlights-vc), checked 2026-11-08; one-PM matchup highlight clips were not located in the indexed results for this pass.
- Pregame history and rolling averages: `research/WEEK9_VERIFIED_HISTORICAL_REFERENCE_20261107.csv`; frozen market/model board: `research/week9_1pm_live/WEEK9_1PM_PROJECTIONS.md`.
- Current score/quarter feed: DraftKings Scores connector search, 2026-11-08T20:52:23.271Z, request `20a4dbba-66b0-4395-9f99-adf4afc03548`. Connector does not expose a stable per-game source URL; quarter snapshot saved in companion CSV.
