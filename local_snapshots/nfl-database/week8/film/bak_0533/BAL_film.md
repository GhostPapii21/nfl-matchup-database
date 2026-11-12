# BAL — Phase 8 film notes (Weeks 1–6, 2026)

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

Offense (Codex synthesis from this game's plays): Explosive receiving gains: Flowers gained 49 yards and scored from 54; Moore added a 53-yard catch. / Flowers's backfield motion into an angle route produced a touchdown against explicitly described Indianapolis miscommunication. / Henry scored three rushing touchdowns, including a 32-yard cutback with a stiff-arm and a three-yard run to the corner. / Jackson extended possessions with caption-reported scrambles of 17 and 20 yards and scored on a five-yard keeper. / Henry's 19-yard screen and late first-down catches by Andrews and Hill supplied additional chain-moving options.

Defense weaknesses: Taylor produced first-down runs of 10, 19 and 21 yards, another unspecified first-down run, and two short touchdowns. / Allowed Downs's 25- and 12-yard catches on the opening possession. / Allowed a late 23-yard Pierce catch followed by Warren's nine-yard touchdown. / Kickoff coverage surrendered McGowan's 66-yard return to the Baltimore 30.

Limitations: Analysis uses only the supplied captions and DB excerpt; no frames, browsing or commands. DB matches are identified by quarter and clock. The DB excerpt is selective, so NO DB MATCH does not establish that a play was absent from the full game record; Jackson's caption-reported 20-yard scramble is one such unmatched play. Formations and coverage are supplied only when explicitly stated by commentators; shotgun appearing solely in DB text is not used for those fields. Route and run concepts may come from DB text. Named tacklers are labeled as tacklers and do not establish who lost the original coverage assignment. Fragmentary captions leave several gains, identities and play types unresolved. Sack yardage is distinguished from fumble-return yardage, and the interception's one yard is return yardage. Return teams occupy the team field for kickoff returns. The missed extra point shares its touchdown's DB entry. The field-goal distance conflict is resolved using the authoritative DB. Unshown DB-only plays, routine implied extra points and a proposed but unconfirmed spike are omitted.


## Week 2: NO 24 - BAL 17 (game 401872938)
Video: New Orleans Saints vs. Baltimore Ravens Game Highlights | NFL 2026 Season Week 2 — https://www.youtube.com/watch?v=ZhFUgsuEgV4  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:24|BAL|unknown|Play-action pass toward the backfield; receiver and result are unclear.|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:35|NO|unknown|Third-and-short play with fakes and Ravens pressure; commentary names Robinson, but the outcome is unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:50|BAL|Mark Andrews|Catches Jackson's pass for an apparent first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:01|BAL|Mark Andrews|Makes another catch on third-and-six; final spot is omitted.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:09|BAL|Derrick Henry|Takes an underneath pass downhill. Commentary says 19 yards; DB records 20.|20|short right pass|unknown|unknown|J.Reid (DB tackler)|verified vs DB|
|01:29|BAL|Rashod Bateman|Catches a sharply thrown Jackson pass.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:41|BAL|Derrick Henry|Picks up a first down and takes a hard hit at the finish.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:49|BAL|Derrick Henry|Scores on a direct snap around right end. Replay commentary credits Andrews getting to the second level and criticizes the defensive edge.|1|direct snap; right-end run|unknown|unknown|unknown|verified vs DB|
|02:20|NO|Chris Olave|Catches a lofted pass.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:31|NO|unknown|Shough completes a third-and-six pass for a first down; commentary describes a high, imperfect throw.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:46|NO|unknown tight end|Catches Shough's pass well short of the first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:52|BAL|D.Walker|Makes a long catch off Jackson's play action; DB records a declined defensive holding penalty on Emerson.|47|play-action; deep left pass|unknown|unknown|M.Emerson (DB tackler; defensive holding)|verified vs DB|
|03:08|BAL|Wester|Picks up 15 yards and a first down, forced out by the defender captioned as Julian Blackman. Play type is unclear.|15|unknown|unknown|unknown|Julian Blackman (captioned tackler)|unverified (no DB match; caption-only)|
|03:26|BAL|unknown|Fragment describes a flagged play with Martin Emerson among those involved; action and result are unclear.|None|unknown|unknown|unknown|Martin Emerson (mentioned among tacklers)|unverified (no DB match; caption-only)|
|03:39|BAL|T.Loop|49-yard field-goal attempt is blocked. Commentary tentatively credits Justin Reid; DB credits C.Granderson.|0|field goal|unknown|unknown|unknown|verified vs DB|
|03:46|NO|D.Vele|Catches Shough's third-and-long pass for 29 yards.|29|deep middle pass|unknown|unknown|J.Hawkins (DB tackler)|verified vs DB|
|04:03|NO|Chris Olave|Shough threads a pass to Olave.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:11|NO|Tyler Shough|Tucks the ball and runs; commentary says Zion Young had a chance to bring him down.|None|quarterback scramble|unknown|unknown|Zion Young (missed opportunity described)|unverified (no DB match; caption-only)|
|04:21|NO|Tyler Shough|Faces third-and-long pressure with Hendrickson coming around the edge; final outcome is unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:37|NO|D.Carlson|Makes a 23-yard field goal for New Orleans' first points.|23|field goal|unknown|unknown|unknown|verified vs DB|
|04:48|BAL|Derrick Henry|Takes a handoff and engages tacklers.|None|handoff run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:57|BAL|Chris Moore|Catches a pass from a well-protected Jackson during the two-minute drive.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:05|BAL|Rashod Bateman|Makes a reception that officials rule a catch.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:18|BAL|Lamar Jackson|Scrambles inside for a dozen yards.|12|quarterback scramble inside|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:33|BAL|R.Bateman|Scores on a 22-yard pass. Analysis describes widening his release, a stutter step, and working inside the numbers while the safety is across the field.|22|deep middle pass; widened release with stutter step|unknown|unknown|unknown|verified vs DB|
|06:02|NO|Vele|Makes a late-half catch, with commentary discussing his second foot.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:11|NO|Tyler Shough|Throws out of bounds, leaving two seconds.|0|throwaway|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:25|NO|D.Carlson|Makes the half-ending 47-yard field goal.|47|field goal|unknown|unknown|unknown|verified vs DB|
|06:27|NO|B.Brown|Retrospective mention of the excellent kick return setting up the half-ending score; DB identifies the 53-yard return.|53|kickoff return|unknown|unknown|T.Loop (DB tackler)|CONFLICT (yardage 53 vs DB)|
|06:30|NO|Etienne|Fragment appears to call an Etienne play; action and result are unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:44|NO|J.Johnson|Turns an underneath third-and-13 catch into a 25-yard first down.|25|short right pass|unknown|unknown|N.Wiggins (DB tackler)|verified vs DB|
|06:56|NO|Chris Olave|Targeted on an incomplete third-and-four pass under well-timed pressure.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:07|NO|D.Carlson|Field-goal sequence following the stated 51-yard setup. Captions omit a clear result call; DB confirms the make.|51|field goal|unknown|unknown|unknown|verified vs DB|
|07:23|BAL|Mark Andrews|Catches Jackson's pass.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:27|BAL|Derrick Henry|Commentary references a Henry run producing a fresh set of downs.|None|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:29|BAL|Justice Hill|Gets the ball and advances; captions inconsistently describe the territory.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:46|BAL|Lamar Jackson|Throws under pressure; a defender captioned as Sankar is mentioned, but the result is missing.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:49|BAL|Rashod Bateman|Catches a lofted play-action pass with Quincy Riley identified in coverage.|None|play-action|unknown|unknown|Quincy Riley (commentary coverage)|unverified (no DB match; caption-only)|
|08:16|BAL|Lamar Jackson|Sacked on third-and-long. Young gets there, with Nathan Shepherd arriving behind him.|None|unknown|unknown|four-man rush|unknown|unverified (no DB match; caption-only)|
|08:27|BAL|T.Loop|Makes a 49-yard field goal after the sack.|49|field goal|unknown|unknown|unknown|verified vs DB|
|08:38|NO|unknown|Commentary calls out Mike Greene making a Ravens defensive play; precise action and outcome are omitted.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:56|BAL|Chris Moore|Jackson steps up and takes a downfield shot toward Moore, incomplete with Jonah Sankar nearby.|0|deep shot|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:09|NO|Tyler Shough|Faces Ravens pressure; escape-related commentary is truncated and the outcome is unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:16|NO|Chris Olave|Catches a pass for 13 yards.|13|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:26|NO|C.Olave|Scores on a 21-yard pass. Commentary identifies a scissors concept and says the safety bites on the corner route.|21|scissors routes; deep middle pass|unknown|unknown|unknown|verified vs DB|
|10:00|NO|Tyler Shough|Runs and goes down on the initial two-point attempt. Defensive holding on number 21 causes the attempt to be replayed.|None|quarterback run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:16|NO|T.Etienne|Runs behind blockers for the successful two-point conversion, tying the game.|None|handoff; right-end run|unknown|unknown|unknown|verified vs DB|
|10:33|BAL|Lamar Jackson|Throws incomplete after Andrews motions. Commentary notes an extra rusher and credits Kool-Aid McKinstry.|0|unknown|Andrews in motion|extra rusher|unknown|unverified (no DB match; caption-only)|
|10:47|NO|Chris Olave|Catches a pass from a protected Shough.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:05|NO|Vele|Catches a pass and is marked about half a yard short, setting up fourth down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:13|NO|Tyler Shough|Attempts an under-center push on fourth-and-short; captions omit a definitive ruling.|None|quarterback sneak|quarterback under center|unknown|unknown|unverified (no DB match; caption-only)|
|11:27|NO|Chris Olave|Catches Shough's pass against pressure for a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:39|NO|Vele|Makes a second-and-14 catch working against Humphrey inside three minutes.|None|unknown|unknown|unknown|Humphrey (commentary matchup)|unverified (no DB match; caption-only)|
|11:50|NO|J.Johnson|Makes a 25-yard catch to the Baltimore 5. Roughing the passer on T.Hendrickson adds three yards.|25|short right pass|unknown|unknown|J.Hawkins (DB tackler)|verified vs DB|
|12:09|NO|unknown|Commentary references a goal-line incompletion and its clock effect.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:16|NO|unknown|Breaks a tackle and lunges, but is marked short of the end zone.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:29|NO|T.Shough|Scores the go-ahead touchdown on a one-yard keeper up the middle. Extended replay debate follows; DB confirms the ruling stands.|1|quarterback keeper up the middle|unknown|unknown|Marlon Humphrey; Roquan Smith (commentary identifies involvement)|verified vs DB|
|14:39|BAL|Mark Andrews|Catches a pass for a first down on the final drive.|None|unknown|unknown|zone pressure|unknown|unverified (no DB match; caption-only)|
|14:54|BAL|unknown|Jackson finds a receiver through a seam; the clock continues running.|None|seam pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:07|BAL|L.Jackson|Deep-left pass intended for R.Bateman is intercepted by J.Blackmon at the Saints 7 and returned two yards.|2|deep left pass|unknown|unknown|R.Bateman (DB return tackler)|verified vs DB|

Offense (Codex synthesis from this game's plays): Jackson repeatedly connected with Andrews and Bateman; Bateman supplied the 22-yard touchdown. / Play action produced Walker's 47-yard reception and another Bateman completion. / Henry contributed a 20-yard reception, first-down gains, and a direct-snap rushing touchdown. / Jackson added a 12-yard inside scramble during the late-first-half scoring drive.

Defense weaknesses: Allowed Vele's 29-yard completion and two 25-yard Johnson receptions, including an underneath conversion on third-and-13. / A safety biting on the corner route opened Olave's 21-yard scissors touchdown. / Defensive holding gave New Orleans another two-point attempt, which Etienne converted. / Hendrickson's roughing penalty moved New Orleans closer after Johnson's late 25-yard catch. / Allowed repeated fourth-quarter completions to Olave and a Vele catch against Humphrey during the winning drive.

Limitations: Analysis uses only the supplied captions and DB excerpt; no frames, browsing, or commands were used. Fragmentary play descriptions are retained with uncertainty, and replay commentary is consolidated with the original play. NO DB MATCH means no confident match in the supplied excerpt, which omits many ordinary plays. Team assignments for the earliest fragments are inferred from possession context. Names on unmatched plays retain caption wording where identity is uncertain. Personnel counts, most formations, coverage shells, route details, and individual blocking assignments cannot be established. Named tacklers or coverage defenders do not necessarily represent a defender beaten; field text identifies their actual stated role. Null yards means undetermined; field-goal yards are kick distance, blocked-field-goal yards follow the DB's zero, and interception yards are return yards. is_score identifies scoring on that listed action, so Henry's preceding reception and Brown's return are not scores. No reliable caption evidence identifies the other listed kickoff returns or the reversed kickoff fumble, so they are not added.


## Week 3: BAL 34 - DAL 31 (game 401872960)
Video: Baltimore Ravens vs Dallas Cowboys Game Highlights from Rio | 2026 NFL Season Week 3 — https://www.youtube.com/watch?v=7gWPdESD1og  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 4: TEN 18 - BAL 24 (game 401872973)
Video: Tennessee Titans vs Baltimore Ravens Game Highlights | 2026 NFL Season Week 4 — https://www.youtube.com/watch?v=1MzoImgClWQ  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 5: BAL 30 - ATL 23 (game 401872993)
Video: Baltimore Ravens vs Atlanta Falcons Game Highlights | 2026 NFL Season Week 5 — https://www.youtube.com/watch?v=fVlmow2jCDA  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 6: BAL 10 - CLE 13 (game 401872997)
Video: Baltimore Ravens vs. Cleveland Browns Game Highlights | 2026 NFL Season Week 6 — https://www.youtube.com/watch?v=agBZnbbPCq0  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:35|BAL|Derrick Henry|Takes the handoff for 11 yards to the 45 and a first down; Mark Andrews motions before the snap.|11|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:51|BAL|Derrick Henry|Gets the edge on second-and-four and is upended near midfield. Ja'Kobi Lane is credited with a key block.|None|outside run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:06|BAL|Ja'Kobi Lane|Catches Huntley's pass and holds on through Schwesinger's attempt to strip it for a first down.|None|unknown|unknown|unknown|Carson Schwesinger|unverified (no DB match; caption-only)|
|01:12|BAL|Ja'Kobi Lane|Makes a fingertip catch on third-and-six for a first down. Schwesinger attempts to punch the ball out; Ward makes the tackle.|None|unknown|unknown|unknown|Carson Schwesinger; Denzel Ward|unverified (no DB match; caption-only)|
|01:29|BAL|Tyler Huntley|Dodges the rush and scrambles to approximately the 1-yard line after Flowers motions.|None|quarterback scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:39|BAL|Derrick Henry|Is upended on third-and-goal, bringing up fourth-and-goal.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:53|BAL|Tyler Huntley; Josh Cuevas|Following a shift, Huntley uses a play fake and throws to an open Cuevas for a fourth-down touchdown.|2|play-action; short middle pass|unknown|unknown|unknown|verified vs DB|
|02:14|CLE|Deshaun Watson|Attempts to escape the pocket. The call cuts off; the subsequent discussion of Calais Campbell suggests a sack, but the result is not stated completely.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:30|BAL|Josh Cuevas|Makes a sideline reception and runs downfield. Commentary estimates 30 yards to the 31; the DB records 29 yards to the CLE 32 plus roughing the passer on Maliek Collins.|29|short right pass|unknown|unknown|Ronnie Hickman|verified vs DB|
|02:52|BAL|Tyler Loop|Makes a 34-yard field goal for a 10-0 lead.|34|field goal|unknown|unknown|unknown|verified vs DB|
|03:04|CLE|Deshaun Watson; Jerry Jeudy|Watson has time and completes a pass to Jeudy for a first down on second-and-nine.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:15|CLE|Deshaun Watson|Faces pressure up the middle on third down and tries to get rid of the ball. Commentary says Fannin was in the area and grounding should not apply.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:31|BAL|Derrick Henry|Bursts up the middle for 10 yards to the 36.|10|middle run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:38|BAL|Tyler Huntley; Justice Hill|Against four-man pressure, Huntley checks down to Hill out of the backfield. Tyson Campbell forces him out well short of the first down.|None|checkdown to running back|unknown|unknown|Tyson Campbell|unverified (no DB match; caption-only)|
|04:03|BAL|Keondre Jackson; unidentified punter|A 59-yard punt is saved back into play by Jackson and leaves Cleveland inside its own 5.|59|punt|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:21|CLE|Audric Estime|Takes a handoff from near his own 4 and gains a stated six yards for breathing room. The caption's 'first and goal' is inconsistent with this field position.|6|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:38|CLE|Deshaun Watson|Tries to get to the edge on third-and-nine and gains four yards before Kyle Hamilton tackles him short at the 21.|4|quarterback run toward edge; design unknown|unknown|unknown|Kyle Hamilton|unverified (no DB match; caption-only)|
|04:57|BAL|Tyler Huntley; Zay Flowers|Huntley takes a hit on a pass completed to Flowers, who is tackled at the 24. The tackler's name cuts off after 'Carson.'|None|unknown|unknown|unknown|Carson (surname not stated in this call)|unverified (no DB match; caption-only)|
|05:06|CLE|Deshaun Watson; Jerry Jeudy|Jeudy makes a sliding catch for 14 yards to the Baltimore 47 on second-and-four.|14|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:18|CLE|Deshaun Watson; Fannin|Against a four-man rush on third-and-eight, Watson's pass to Fannin is tipped incomplete by Malaki Starks.|0|unknown|unknown|unknown|Malaki Starks (pass breakup)|unverified (no DB match; caption-only)|
|05:33|CLE|Unidentified punter and coverage player|Punt bounces near the 5 and is downed inside Baltimore's 2.|None|punt|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:47|BAL|Derrick Henry|Loses one yard to the 2 on second-and-nine. Maliek Collins gets help from Daniel Thomas.|-1|unknown|unknown|unknown|Maliek Collins; Daniel Thomas|unverified (no DB match; caption-only)|
|05:59|BAL|Tyler Huntley; Ja'Kobi Lane|From his own end zone on third-and-ten, Huntley completes to Lane, who rolls forward for a first down at the 12.|10|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:22|BAL|Zay Flowers|Takes a pass to the 29 for 17 yards and a third-down conversion, with Schwesinger pursuing.|17|unknown|unknown|unknown|Carson Schwesinger|unverified (no DB match; caption-only)|
|06:30|BAL|Tyler Huntley|Is sacked back at the 20 by Maliek Collins, with pressure described as coming through the middle.|None|unknown|unknown|unknown|Maliek Collins (sack)|unverified (no DB match; caption-only)|
|06:48|BAL|Tyler Huntley|Escapes backside pressure on third-and-17, is chased by Barnett, and runs across the 30 short of the first down.|None|quarterback scramble|unknown|unknown|Barnett (pursuit)|unverified (no DB match; caption-only)|
|07:06|CLE|Deshaun Watson|Cannot escape incoming pressure and is sacked. The following commentary calls it Cleveland's third sack allowed.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:18|CLE|Deshaun Watson; KC Concepcion|Against four-man pressure, Watson throws too high for Concepcion.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:24|BAL|Tyler Huntley; Mark Andrews|Andrews makes a low catch on third down for a first down, followed by a timeout.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:39|BAL|Tyler Huntley; Devontez Walker|Deep pass down the middle intended for Walker is broken up over his shoulder by Myles Harden.|0|deep middle shot|unknown|unknown|Myles Harden (pass breakup)|unverified (no DB match; caption-only)|
|07:57|BAL|Tyler Huntley; Zay Flowers|Huntley rolls and floats a third-and-long pass toward Flowers; Myles Harden deflects it.|0|pass on the move|unknown|unknown|Myles Harden (pass breakup)|unverified (no DB match; caption-only)|
|08:13|CLE|Deshaun Watson; Fannin|Facing pressure on third-and-ten, Watson rolls and completes to Fannin, who lunges close to the first-down marker with Tavius Robinson involved.|None|pass on the move|unknown|unknown|Tavius Robinson|unverified (no DB match; caption-only)|
|08:26|CLE|Michael Burton|Carries and fights forward for a Cleveland first down. The precise down and distance are cut off.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:46|CLE|Deshaun Watson; KC Concepcion|Watson has time on first-and-15 and completes over the middle to Concepcion for a first down.|None|middle pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:02|CLE|Deshaun Watson; KC Concepcion|Concepcion catches a pass over the middle on third-and-13 and reaches the 30, five yards short.|8|middle pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:13|CLE|Andre Szmyt|Makes a 48-yard field goal to put Cleveland on the board.|48|field goal|unknown|unknown|unknown|verified vs DB|
|09:34|BAL|Ja'Kobi Lane|Makes a catch for a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:35|BAL|Tyler Huntley|Throws wide of an unnamed target over the middle from a clean pocket on third-and-ten.|0|middle pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:54|CLE|Deshaun Watson|Is sacked at the 15 on third-and-four despite Baltimore rushing only three. The sack credit cuts off.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:05|BAL|Tyler Huntley; Zay Flowers|Against four-man pressure, Huntley moves right and throws across his body to Flowers, who spins after the catch for a 31-yard gain.|31|deep left pass; throw on the move|unknown|unknown|Myles Harden|verified vs DB|
|10:38|BAL|Tyler Huntley; Josh Cuevas|Under pressure on third-and-22, Huntley throws over the middle and Cuevas makes a diving catch.|None|middle pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:48|BAL|Tyler Loop|Misses a 49-yard field goal wide left after a slightly high snap. The caption's proposed '14-3' score is erroneous.|49|field goal|unknown|unknown|unknown|verified vs DB|
|11:02|CLE|Deshaun Watson; Boston|Third-and-four sideline pass to the player called Boston is initially called caught, then corrected to a drop.|0|sideline pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:07|BAL|Derrick Henry|Gains five yards off left tackle and fumbles. Carson Schwesinger forces it; Tyson Campbell recovers for Cleveland at the BAL 35.|5|left tackle run|unknown|unknown|Carson Schwesinger; Tyson Campbell|verified vs DB|
|11:39|CLE|Deshaun Watson; KC Concepcion|Concepcion goes up for a pass over the middle on third-and-four and gains 15 yards to the Baltimore 14.|15|middle pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:58|CLE|Deshaun Watson; KC Concepcion|Third-and-seven pass over the middle to Concepcion is batted away by the defender captioned as Keyon Martin. The subsequent discussion suggests a disputed contact call, but the ruling is omitted.|0|middle pass; commentary references an intended rub involving Fannin|unknown|unknown|Keyon Martin (caption spelling; pass breakup)|unverified (no DB match; caption-only)|
|12:17|CLE|Audric Estime|With Fannin in motion, runs through right guard for a 2-yard touchdown that ties the game after the extra point.|2|right guard run|unknown|unknown|unknown|verified vs DB|
|12:30|BAL|Tyler Huntley; Mark Andrews|Third-and-three pass over the middle to Andrews is broken up by Denzel Ward, completing a three-and-out.|0|middle pass|unknown|unknown|Denzel Ward (pass breakup)|unverified (no DB match; caption-only)|
|12:45|CLE|Deshaun Watson; unidentified receiver|Watson flips a short pass and the receiver advances up the sideline. Receiver and gain are omitted.|None|short pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:56|CLE|Deshaun Watson; Jerry Jeudy|Against pressure up the middle, Watson finds Jeudy over the middle for a first down; Starks tackles him.|None|middle pass|unknown|unknown|Malaki Starks|unverified (no DB match; caption-only)|
|13:11|CLE|Deshaun Watson; Michael Burton|In trouble on third-and-nine, Watson attempts a dump-off to Burton. The result is not explicitly stated.|None|dump-off|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:19|CLE|Andre Szmyt|Misses a 48-yard field goal wide left with the score tied.|48|field goal|unknown|unknown|unknown|verified vs DB|
|13:31|BAL|Tyler Huntley; unidentified target|Pass against a four-man rush is nearly intercepted. The defender's name is not supplied.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:47|BAL|Tyler Huntley|Leaves the pocket under pressure and breaks away on a key third down; the call cuts off before the result.|None|quarterback escape; final action unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:54|CLE|Deshaun Watson; McLaughlin|McLaughlin gains a stated nine yards on first down, with a flag down. The exchange type and penalty ruling are omitted.|9|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:06|CLE|Deshaun Watson|Evades backside pressure while looking downfield and makes a move on Calais Campbell. Final action and gain are omitted.|None|quarterback escape|unknown|unknown|Calais Campbell|unverified (no DB match; caption-only)|
|14:22|CLE|Deshaun Watson; Jerry Jeudy|On third-and-five with 42 seconds remaining, Watson finds Jeudy open over the middle for 33 yards to the Baltimore 29; Starks makes the DB-recorded tackle.|33|deep middle pass|unknown|unknown|Malaki Starks|verified vs DB|
|14:41|CLE|Deshaun Watson|Moves left on third-and-five with 11 seconds left to position the ball for Szmyt. Gain and exact finish are not stated.|None|quarterback positioning run left|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:59|CLE|Andre Szmyt|Kick is called blocked by the defender captioned as Keyon Martin, but a flag follows. Commentary identifies an early start and neutral-zone entry; Cleveland receives a first down.|None|field goal; nullified blocked attempt|unknown|unknown|Keyon Martin (caption spelling; block and neutral-zone violation)|unverified (no DB match; caption-only)|
|15:17|CLE|Andre Szmyt|Makes the winning 37-yard field goal as time expires, giving Cleveland a 13-10 win.|37|field goal|unknown|unknown|unknown|verified vs DB|

Offense (Codex synthesis from this game's plays): Henry produced an opening 11-yard gain, an edge run near midfield, and a later 10-yard burst up the middle. / Lane repeatedly converted receptions into first downs, including third-and-six and a third-and-ten completion from Baltimore's end zone. / Huntley's movement created a near-goal-line scramble, the play-action touchdown to Cuevas, and the 31-yard completion to Flowers. / Cuevas supplied the 2-yard touchdown and a 29-yard reception.

Defense weaknesses: Cleveland converted multiple middle-field passes to Concepcion, including a 15-yard third-and-four gain after Henry's fumble. / Jeudy repeatedly gained first downs, culminating in the 33-yard third-and-five completion that set up the winning kick. / Baltimore allowed Estime's tying 2-yard right-guard touchdown. / The late neutral-zone violation erased a blocked field-goal attempt and gave Cleveland another opportunity.

Limitations: Analysis uses only the supplied captions and DB excerpt; no video frames or commands were used. The DB excerpt is selective, so NO DB MATCH does not mean a play did not occur. No personnel grouping, formation, or coverage scheme is explicitly stated in the commentary; all are unknown, including plays whose DB text says shotgun. Rush counts do not establish coverage. Defender_beaten records named tacklers, pursuers, or pass defenders where available and does not necessarily mean they lost coverage. Some names remain caption spellings because no matching DB play permits correction. Null yards indicate an unstated or uncertain gain; the 10-yard Lane catch and 8-yard Concepcion catch are inferred from stated field position or distance remaining. Henry's fumble entry uses the underlying 5-yard rushing gain rather than the DB turnover summary's 0-yard recovery value. Kick distances are attempt lengths. The adjacent Lane catches at 01:06 and 01:12 are listed separately because the captions introduce a new third-and-six, although an edited replay cannot be ruled out. Several calls cut off before their outcomes, and penalty enforcement is sometimes omitted. The initial blocked kick was nullified and is separate from the winning field goal. Kickoffs and returns present only in the DB are excluded because the captions do not identify them.
