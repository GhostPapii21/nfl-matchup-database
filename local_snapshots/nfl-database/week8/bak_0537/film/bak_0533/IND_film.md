# IND — Phase 8 film notes (Weeks 1–6, 2026)

Method: NFL YouTube channel full-game highlight videos were located by search and their auto-captions (broadcast commentary) downloaded via yt-dlp. Codex (codex-cli 0.163.0) extracted plays from the captions. **No video frames were viewed by any agent.** Each play was checked against the repo DB play-by-play: `verified vs DB` means the cited DB play exists and the yardage matches. Personnel, formation and coverage appear only when commentators stated them; everything else is `unknown`.


## Week 1: BAL 41 - IND 23 (game 401872659)
Video: Baltimore Ravens vs. Indianapolis Colts Game Highlights | NFL 2026 Season Week 1 — https://www.youtube.com/watch?v=iyDolDtuiT0  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:35|IND|Keenan Allen|Makes his first catch; gain unspecified.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:39|IND|Josh Downs|Catches a first-down pass and holds on through Kyle Hamilton's attempt to dislodge it.|25|short middle pass|shotgun|unknown|Kyle Hamilton (DB tackler; commentary describes attempted strip)|verified vs DB|
|00:55|IND|Josh Downs|Converts third down with a catch over the middle against pressure.|12|middle pass|unknown|pressure; coverage unknown|unknown|unverified (no DB match; caption-only)|
|01:05|IND|Alec Pierce|Fragmentary call identifies Pierce reaching the six-yard line; play type and gain unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:13|IND|Jonathan Taylor|Scores untouched behind lead blockers.|1|right end run|unknown|unknown|unknown|verified vs DB|
|01:42|IND|Spencer Shrader|Misses the extra point wide right.|None|extra point|unknown|unknown|unknown|verified vs DB|
|01:50|BAL|Chris Moore|Returns the kickoff down the sideline to the Baltimore 49.|42|kickoff return|unknown|unknown|Spencer Shrader; Adetomiwa Adebawore (DB tacklers)|CONFLICT (yardage 42 vs DB)|
|02:05|BAL|Zay Flowers|Takes Lamar Jackson's completion to the Indianapolis two-yard line.|49|deep left pass|unknown|unknown|J. Walley (DB tackler)|verified vs DB|
|02:29|BAL|Lamar Jackson|Keeps left for a touchdown; analyst says nobody accounts for Jackson.|5|left end quarterback keeper|shotgun|unknown|unknown|verified vs DB|
|02:56|IND|Daniel Jones|Roquan Smith intercepts the pass intended for Laquon Treadwell and returns it one yard.|1|short middle pass|unknown|unknown|unknown; Roquan Smith makes the interception|verified vs DB|
|03:05|BAL|Derrick Henry|Lowers his shoulder and carries a defender called Cam for extra yardage.|7|unknown|unknown|unknown|Cam (surname not stated on this play)|unverified (no DB match; caption-only)|
|03:22|BAL|Lamar Jackson|Escapes pressure, stays upright and scrambles outside, nearly reaching a first down.|17|quarterback scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:37|BAL|Matt Hibner|Catches Jackson's checkdown.|None|checkdown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:48|BAL|Derrick Henry|Scores on second-and-goal; analyst describes a stretch run with a cutback and an untouched finish.|4|stretch run with cutback; DB right tackle|unknown|unknown|unknown|verified vs DB|
|04:14|IND|Jonathan Taylor|Runs on third-and-long and is brought down by Robinson; illegal shift is announced.|None|unknown|unknown|unknown|unknown; Robinson makes the tackle|unverified (no DB match; caption-only)|
|04:31|BAL|Zay Flowers|Catches a quick, tight-window throw for a first down against pressure and man coverage.|18|quick pass|unknown|man-to-man with pressure|unknown|unverified (no DB match; caption-only)|
|04:48|BAL|Derrick Henry|Takes a screen inside the ten for first-and-goal.|19|screen|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:58|BAL|Ja'Kobi Lane|Catches a third-down pass with good protection and is stopped at the three.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:10|BAL|Lamar Jackson|With Flowers in motion, is chased out and throws incomplete across his body on fourth down.|0|pass under pressure|Flowers in motion; personnel unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:28|IND|Jonathan Taylor|Runs up the middle for a first down; Robinson makes the tackle.|10|middle run|unknown|unknown|Robinson (commentary tackler)|unverified (no DB match; caption-only)|
|05:39|IND|Daniel Jones|Corner blitz is picked up, but Tavius Robinson pursues Jones outside and forces a throwaway.|0|scramble and throwaway|unknown|Humphrey corner blitz; coverage unknown|unknown; Tavius Robinson contains Jones|unverified (no DB match; caption-only)|
|05:57|BAL|Mark Andrews|Catches a wide-open pass over the middle for a first down.|None|middle pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:08|BAL|Zay Flowers|Catches the pass with room, accelerates and splits the defense for a touchdown; analyst cites miscommunication.|54|motion out of backfield into angle route; short middle pass|Flowers initially in backfield, then motions out; personnel unknown|unknown|unknown|verified vs DB|
|06:55|IND|Jonathan Taylor|Catches a pass and gains a first down behind a Tanor Bortolini block, then loses a fumble forced and recovered by Marlon Humphrey.|14|short left pass|unknown|unknown|Marlon Humphrey; J. Hawkins (DB tacklers; Humphrey forces turnover)|verified vs DB|
|07:35|BAL|Zay Flowers|Catches Jackson's throw on the run with Sauce Gardner in coverage.|None|pass on the run|unknown|unknown|Sauce Gardner (explicit coverage matchup)|unverified (no DB match; caption-only)|
|07:51|BAL|Derrick Henry|Finds a hole, cuts back and stiff-arms Cam Bynum on a touchdown run.|32|left tackle run with cutback|unknown|unknown|Cam Bynum|verified vs DB|
|08:21|IND|Alec Pierce|Targeted on an incomplete deep shot on third-and-ten.|0|deep shot|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:37|BAL|Lamar Jackson|Sacked by Arden Key and Laiatu Latu; Key forces the fumble and DeForest Buckner recovers at the Baltimore 15.|-10|unknown|unknown|unknown|unknown; Key and Latu create the sack|verified vs DB|
|08:52|IND|Jonathan Taylor|Runs inside the ten after the turnover; Malaki Starks tackles him.|None|unknown|unknown|unknown|Malaki Starks (commentary tackler)|unverified (no DB match; caption-only)|
|09:07|IND|Jonathan Taylor|Scores to capitalize on the defensive takeaway.|3|right tackle run|unknown|unknown|unknown|verified vs DB|
|09:38|BAL|Wester|Catches Jackson's first-down pass; gain unspecified.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:46|BAL|Lamar Jackson|Scrambles through open space and gets out of bounds to stop the clock.|20|quarterback scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:01|BAL|Justice Hill|Picks up a first down before Baltimore prepares to spike; play type unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:15|BAL|Tyler Loop|Makes a 57-yard field goal as the first half ends.|57|field goal|unknown|unknown|unknown|verified vs DB|
|10:36|IND|Jonathan Taylor|Opens the Colts' first second-half drive with a first-down run.|19|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:47|IND|Alec Pierce|Catches a first-down pass and slides at the 46.|11|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:56|IND|Daniel Jones|Steps up and runs for just enough yardage to convert second-and-two.|None|quarterback scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:09|IND|McGowan|Finishes well short on third-and-six after Trey Hendrickson gets a hand on Jones; exact play type unclear.|None|unknown|unknown|unknown|unknown; Trey Hendrickson pressures Jones|unverified (no DB match; caption-only)|
|11:22|IND|Spencer Shrader|Makes a field goal; captions say 48 yards, authoritative DB says 58.|58|field goal|unknown|unknown|unknown|verified vs DB|
|11:34|BAL|Derrick Henry|Runs for 13 yards after a player called Chris War goes in motion.|13|unknown|motion mentioned; player identity and personnel unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:42|BAL|Derrick Henry|Runs to midfield for a first down; authoritative DB places the finish at the Indianapolis 49.|22|left tackle run|unknown|unknown|A. Haulcy (DB tackler)|verified vs DB|
|11:53|BAL|Chris Moore|Targeted deep on third-and-eleven with Bynum coming off the edge; pass incomplete and Baltimore flagged for holding.|0|deep shot|unknown|Bynum edge pressure; coverage unknown|unknown|unverified (no DB match; caption-only)|
|12:09|IND|Jonathan Taylor|Finds room and reaches the second level to give Indianapolis breathing room.|21|right tackle run|unknown|unknown|Nate Wiggins (DB tackler)|verified vs DB|
|12:24|IND|Jonathan Taylor|Finds another hole for a first-down run.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:35|IND|Alec Pierce|Deep middle target on third-and-seven is broken up by Wiggins.|0|deep middle pass|unknown|unknown|unknown; Wiggins breaks up the pass|unverified (no DB match; caption-only)|
|12:49|BAL|Chris Moore|Gets separation down the sideline and is tripped from behind by Bynum near the Indianapolis 19.|53|deep left pass|unknown|man-to-man|Cam Bynum (pursuit tackler); initial coverage defender unknown|verified vs DB|
|13:08|BAL|Derrick Henry|Takes a handoff inside the ten.|None|handoff run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:15|BAL|Derrick Henry|Races to the corner for his third touchdown; analyst criticizes Indianapolis for failing to set the edge.|3|left end run|unknown|unknown|unknown|verified vs DB|
|13:45|IND|Keenan Allen|Catches a first-down pass from Jones.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:03|IND|Alec Pierce|Catches the pass near the 15 and carries defenders inside the ten for first-and-goal.|23|deep middle pass|unknown|unknown|Roquan Smith; Malaki Starks (DB tacklers)|verified vs DB|
|14:22|IND|Tyler Warren|Catches Jones's pass and leaps into the end zone.|9|short middle pass|unknown|unknown|unknown|verified vs DB|
|14:57|BAL|Derrick Henry|Runs for a first down during Baltimore's clock-consuming possession.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:02|BAL|Mark Andrews|Gets open for a first-down catch; Cam Bynum makes the tackle.|None|unknown|unknown|unknown|Cam Bynum (commentary tackler)|unverified (no DB match; caption-only)|
|15:10|BAL|Justice Hill|Catches a quick pass, stays upright down the sideline and earns a first down.|None|quick pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:29|BAL|Justice Hill|Runs but comes up short of the line to gain with under five minutes remaining.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:38|BAL|Tyler Loop|Makes a field goal to extend Baltimore's lead to 41–23.|45|field goal|unknown|unknown|unknown|verified vs DB|
|15:54|IND|S. McGowan|Returns the kickoff from the four down the sideline to the Baltimore 30 before C. Jones forces him out.|66|kickoff return|unknown|unknown|C. Jones (DB tackler); Loop identified as a remaining obstacle|CONFLICT (yardage 66 vs DB)|
|16:13|IND|Daniel Jones|Sacked on fourth down by Jaylinn Hawkins and Malaki Starks.|None|unknown|unknown|unknown|unknown; Jaylinn Hawkins and Malaki Starks make the sack|unverified (no DB match; caption-only)|
|16:32|BAL|Derrick Henry|Runs for nine yards on first down as Baltimore closes out the game.|9|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|

Offense (Codex synthesis from this game's plays): Opening-drive passing included consecutive first-down catches by Downs before Taylor finished with a touchdown. / Taylor supplied repeated productive runs, including 19- and 21-yard gains, and converted the short field after Buckner's recovery into a touchdown. / The late touchdown drive included a 23-yard Pierce reception and Warren's scoring catch; commentary reported Jones was 5-for-5 for 54 yards during that drive.

Defense weaknesses: Allowed Flowers's 49-yard gain and 54-yard touchdown; commentary explicitly identified miscommunication on the touchdown. / Allowed an 18-yard Flowers conversion against pressure and man coverage, plus Moore's 53-yard gain against stated man coverage. / Failed to account for Jackson on his touchdown keeper and allowed substantial scrambling gains. / Henry exploited cutback space and poor edge setting on scoring runs; his screen also gained 19 yards. / Allowed open first-down catches to Andrews, including one over the middle.

Limitations: Analysis uses only the supplied captions and DB excerpt; no frames, browsing or commands. DB matches are identified by quarter and clock. The DB excerpt is selective, so NO DB MATCH does not establish that a play was absent from the full game record; Jackson's caption-reported 20-yard scramble is one such unmatched play. Formations and coverage are supplied only when explicitly stated by commentators; shotgun appearing solely in DB text is not used for those fields. Route and run concepts may come from DB text. Named tacklers are labeled as tacklers and do not establish who lost the original coverage assignment. Fragmentary captions leave several gains, identities and play types unresolved. Sack yardage is distinguished from fumble-return yardage, and the interception's one yard is return yardage. Return teams occupy the team field for kickoff returns. The missed extra point shares its touchdown's DB entry. The field-goal distance conflict is resolved using the authoritative DB. Unshown DB-only plays, routine implied extra points and a proposed but unconfirmed spike are omitted.


## Week 2: IND 30 - KC 33 (game 401872945)
Video: Indianapolis Colts vs Kansas City Chiefs Game Highlights | 2026 NFL Season Week 2 — https://www.youtube.com/watch?v=baPzspvJv5Q  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 3: HOU 17 - IND 19 (game 401872951)
Video: Houston Texans vs Indianapolis Colts Game Highlights | 2026 NFL Season Week 3 — https://www.youtube.com/watch?v=LwBJf78vzjY  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 4: IND 30 - WSH 13 (game 401872965)
Video: Indianapolis Colts vs. Washington Commanders Game Highlights | 2026 NFL Season Week 4 — https://www.youtube.com/watch?v=VSkRsq4Tlfg  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 5: IND 22 - PIT 34 (game 401872985)
Video: Indianapolis Colts vs. Pittsburgh Steelers Game Highlights | 2026 NFL Season Week 5 — https://www.youtube.com/watch?v=padeBx3DEdM  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 6: TEN 26 - IND 20 (game 401873003)
Video: Tennessee Titans vs Indianapolis Colts Game Highlights | 2026 NFL Season Week 6 — https://www.youtube.com/watch?v=MJZhpnKoY7E  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:18|IND|Daniel Jones → Will Mallory|Completed pass to Mallory.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:28|IND|Daniel Jones|Completed pass for a first down; receiver unidentified.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:38|IND|Daniel Jones → Keenan Allen|Allen caught the pass near the 30 and fell forward.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:55|IND|Josh Downs|Third-down reception near the first-down marker; commentary leaves the spot uncertain.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:03|IND|Daniel Jones → Deion Burks|Deep-left completion to the Tennessee 16; T. Burgess pushed Burks out.|36|deep shot left|unknown|unknown|T. Burgess (DB tackler)|verified vs DB|
|01:16|IND|Daniel Jones; Amani Hooker|Jones threw on the move; tipped pass intended for Josh Downs was intercepted by Hooker at the Tennessee 6. Ruling upheld.|0|short right pass|unknown|unknown|unknown|verified vs DB|
|01:31|TEN|Wan'Dale Robinson|Third-down reception deep in Tennessee territory; Robinson spun forward toward the marker.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:56|IND|Daniel Jones → Jonathan Taylor|Taylor broke loose on a screen to the Tennessee 28; Hooker pushed him out.|38|screen right|unknown|unknown|Amani Hooker (DB tackler)|verified vs DB|
|02:15|IND|Daniel Jones|Jones stepped up and was brought down on a pass play; defender unidentified.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:20|IND|Keenan Allen|Reception produced first-and-goal inside the 10.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:36|IND|Daniel Jones → Mo Alie-Cox|One-yard touchdown catch. Replay commentary describes Alie-Cox showing a down block before popping open.|1|block-and-release; short left pass|unknown|unknown|Burgess (commentary says he reacted too late)|verified vs DB|
|03:07|TEN|Tony Pollard|Stopped short of the first down; play type not established by the caption.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:10|IND|McGowan|Ballcarrier made moves and reached approximately the 43 for a first down before going out of bounds.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:27|IND|Daniel Jones → Pharaoh Brown|Jones faked to Taylor and floated a pass to Brown for a first down.|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:37|IND|Jonathan Taylor|Taylor ran through a large hole to the Tennessee 13.|20|right end run|unknown|unknown|C. Gray (DB tackler)|verified vs DB|
|03:51|IND|Daniel Jones; Jermaine Johnson|Johnson sacked Jones; announcer called it Johnson's second sack.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:59|IND|Daniel Jones|Jones ran inside the 10 to approximately the 5; first-down status was uncertain in commentary.|None|quarterback run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:26|IND|Spencer Shrader|Made a 23-yard field goal, his 20th consecutive make according to commentary.|23|field goal|unknown|unknown|unknown|verified vs DB|
|04:36|TEN|Cam Ward; Cam Bynum|Bynum intercepted Ward's deep-right pass intended for Wan'Dale Robinson and returned it 12 yards. Commentary calls it an overthrow.|12|deep shot right|unknown|unknown|unknown|verified vs DB|
|04:50|IND|Jonathan Taylor|Taylor gained a first down inside the 35; exact play type is unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:59|IND|Daniel Jones; Martin|Jones was sacked near the 41 by a defender identified as Martin.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:10|IND|Daniel Jones → Keenan Allen|Dump-off to Allen, who made a move and reached inside the 30.|None|dump-off|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:19|IND|Spencer Shrader|Made a 47-yard field goal to extend the lead to 13–0.|47|field goal|unknown|unknown|unknown|verified vs DB|
|05:28|IND|Jonathan Taylor; Jeffery Simmons|Taylor gained four yards before Simmons forced and recovered his fumble.|4|right tackle run|13 personnel|unknown|unknown|verified vs DB|
|06:00|TEN|unknown|Commentary summarizes two batted passes on two plays; individual snaps and players cannot be separated.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:01|TEN|Cam Ward → Carnell Tate|Tate made his first catch of the game against an announced blitz.|None|unknown|unknown|blitz|unknown|unverified (no DB match; caption-only)|
|06:14|TEN|Cam Ward → Carnell Tate|Incomplete third-and-seven pass targeting Tate.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:24|TEN|Joey Slye|Made a 29-yard field goal for Tennessee's first points.|29|field goal|unknown|unknown|unknown|verified vs DB|
|06:39|IND|Jonathan Taylor|Taylor was stopped a couple of yards short of a first down; Hooker was credited with the tackle.|None|run|unknown|unknown|Amani Hooker (commentary tackler)|unverified (no DB match; caption-only)|
|06:45|IND|Daniel Jones → Josh Downs|Completion to Downs for a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:59|IND|Daniel Jones → Keenan Allen|Allen caught a pass inside the Tennessee 25.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:11|IND|Daniel Jones; Cor'Dale Flott|Flott intercepted a pass intended for Will Mallory at the Tennessee 11. Commentary says Flott baited Jones.|0|short left pass|unknown|unknown|unknown|verified vs DB|
|07:40|TEN|Cam Ward → Carnell Tate|Ward threw after scrambling; Tate caught the ball near the boundary, with inbounds status questioned.|None|scramble pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:51|TEN|Tony Pollard|Pollard's best run of the day, according to commentary, reached the 40 for a first down.|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:03|TEN|unknown|Pass went off the intended receiver's hands as he turned; receiver not conclusively identified.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:09|TEN|Joey Slye|Made a 56-yard field goal to bring Tennessee within one score.|56|field goal|unknown|unknown|unknown|verified vs DB|
|08:23|IND|unknown; Anthony Hill Jr.|Fragmentary commentary credits Hill with a defensive play; ballcarrier and outcome are unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:38|IND|unknown; Adams|Unidentified ballcarrier was tackled at the 35; commentary credited Adams.|None|unknown|unknown|unknown|Adams (commentary tackler)|unverified (no DB match; caption-only)|
|08:46|IND|Daniel Jones|Jones was sacked inside the 30 on third-and-ten; caption does not conclusively identify the sacker.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:56|IND|Rigoberto Sanchez; Chimere Dike|Dike returned Sanchez's punt 58 yards from the Tennessee 14 to the Indianapolis 28, getting past Sanchez before K. Gushiken stopped him.|58|punt return|unknown|unknown|Rigoberto Sanchez (commentary); K. Gushiken (DB tackler)|verified vs DB|
|09:16|TEN|Cam Ward → Carnell Tate|Ward completed a pass to Tate, who held on through a hard hit.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:32|TEN|Cam Ward → Carnell Tate|Eight-yard touchdown pass to Tate, identified as his first NFL touchdown.|8|short left pass|unknown|unknown|unknown|verified vs DB|
|10:04|IND|Daniel Jones|Jones ran into open space and went out of bounds against extra pressure.|None|quarterback scramble|unknown|extra pressure|unknown|unverified (no DB match; caption-only)|
|10:23|IND|Daniel Jones → Treadwell|High, overthrown pass was knocked away; Tony Adams was identified as being back in coverage.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:32|IND|Julius Chestnut; O. Oladejo|Chestnut blocked Sanchez's punt up the middle. Oladejo recovered at the Indianapolis 14 and returned it for a Tennessee touchdown.|14|punt block up the middle; recovery return|unknown|unknown|unknown|verified vs DB|
|11:17|IND|Daniel Jones → Josh Downs|Deep-right completion to Downs near midfield, reaching the Tennessee 49.|23|deep shot right|unknown|unknown|A. Hill (DB tackler)|verified vs DB|
|11:24|IND|Daniel Jones → Treadwell|Treadwell caught the pass and made a move for a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:36|IND|Jonathan Taylor|With the blitz picked up, Taylor escaped along the sideline to the Tennessee 20; captions do not establish whether he received a pass or handoff.|None|unknown|unknown|blitz|unknown|unverified (no DB match; caption-only)|
|11:48|IND|Jonathan Taylor|Taylor broke through toward a first down; commentary called for a spot check.|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:01|IND|Jonathan Taylor|Taylor took a pitch around left end for a four-yard touchdown, tying the game after the extra point.|4|pitch left end|unknown|unknown|unknown|verified vs DB|
|12:17|TEN|Cam Ward → Wan'Dale Robinson|Ward delivered an on-target first-down completion to Robinson against pressure.|None|unknown|Robinson in the slot|single high; pressure|unknown|unverified (no DB match; caption-only)|
|12:29|TEN|Cam Ward → Carnell Tate|Third-and-five pass toward Tate was unsuccessful; commentary praised the coverage.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:43|TEN|Joey Slye|Made a 49-yard field goal to put Tennessee ahead 23–20.|49|field goal|unknown|unknown|unknown|verified vs DB|
|12:47|IND|Daniel Jones → unidentified receiver|Completed a sideline pass for 15 yards.|15|sideline pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:02|IND|Daniel Jones; Jermaine Johnson|Johnson sacked Jones on an announced blitz.|None|unknown|unknown|blitz|unknown|unverified (no DB match; caption-only)|
|13:11|IND|Daniel Jones; Anthony Hill Jr.|Fourth-and-17 pass was nearly intercepted and knocked away by Hill, ending the possession on downs.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:50|TEN|unknown|Penalty flag during Tennessee's late possession; infraction and play outcome are not given.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:56|TEN|Tony Pollard|Pollard was stopped before fourth down; Indianapolis used its final timeout.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:02|TEN|Joey Slye|Made a 44-yard field goal for a 26–20 lead with 43 seconds remaining.|44|field goal|unknown|unknown|unknown|verified vs DB|
|14:24|IND|Daniel Jones → Keenan Allen|Allen caught a pass to the 45 with Indianapolis out of timeouts.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:32|IND|Daniel Jones; Amani Hooker|Jones heaved toward the goal line against a three-man rush. Hooker appeared to catch it out of bounds; no interception is established.|0|deep heave|unknown|three-man rush|unknown|unverified (no DB match; caption-only)|
|14:57|IND|Daniel Jones|Final throw toward the goal line was knocked away as time expired.|0|deep heave|unknown|dropping everybody deep|unknown|unverified (no DB match; caption-only)|

Offense (Codex synthesis from this game's plays): Taylor generated explosive gains through a screen and an outside run, then scored on a left-end pitch. / Allen repeatedly supplied completions and first-down opportunities. / Play-action produced a first-down completion to Pharaoh Brown. / Burks and Downs supplied verified deep completions of 36 and 23 yards.

Defense weaknesses: Allowed repeated second-half Tate catches, including the tying touchdown. / Allowed Robinson a late first-down reception against pressure. / Allowed Pollard a first-down run to the 40. / Punt coverage conceded Dike's 58-yard return, and punt protection allowed Chestnut's block and Oladejo's touchdown return.

Limitations: Captions only; no frames were viewed. The supplied DB is selective, so NO DB MATCH does not mean a play did not occur. Unclear names were retained without speculative correction. The DB's 36-yard pass-interference penalty and kickoff returns were not separately identifiable in the captions and were not added. Replay descriptions were combined with their original plays. Unknown distances, alignments, routes, blocking assignments, and coverage details remain unknown. Explicit pressure or rush descriptions are recorded under coverage_scheme without inferring a coverage shell. Named DB tacklers are labeled as tacklers, not assumed to have lost coverage. Yards represent reception/rush gain, turnover or special-teams return distance, or field-goal distance as described; the Taylor fumble entry uses his four-yard rush rather than the DB recovery row's zero return yards. Caption conflicts were resolved with clear DB matches: Slye's first field goal was 29 yards, and Flott's interception came on a short-left pass despite the caption calling it deep. The late Hooker play was out of bounds and is not counted as an interception.
