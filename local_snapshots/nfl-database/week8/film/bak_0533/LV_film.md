# LV — Phase 8 film notes (Weeks 1–6, 2026)

Method: NFL YouTube channel full-game highlight videos were located by search and their auto-captions (broadcast commentary) downloaded via yt-dlp. Codex (codex-cli 0.163.0) extracted plays from the captions. **No video frames were viewed by any agent.** Each play was checked against the repo DB play-by-play: `verified vs DB` means the cited DB play exists and the yardage matches. Personnel, formation and coverage appear only when commentators stated them; everything else is `unknown`.


## Week 1: MIA 13 - LV 27 (game 401872928)
Video: Miami Dolphins vs Las Vegas Raiders Game Highlights | 2026 NFL Week 1 — https://www.youtube.com/watch?v=bi4dvOh4tPA  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:18|MIA|De'Von Achane|Handles a bobbled snap and carries to just short of the 30.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:33|MIA|Malik Willis|Fakes a throw and runs across the 35 for a first down; commentary specifies seven yards.|7|Run after a pass fake|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:47|MIA|unknown|Miami ball carrier is stopped immediately by two Raiders, including Kwity Paye.|None|unknown|unknown|unknown|Kwity Paye (stop)|unverified (no DB match; caption-only)|
|00:58|MIA|De'Von Achane|Catches a floated Willis pass near the 45 and falls forward.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:11|MIA|unknown|Miami is flagged for delay of game before third-and-10.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:19|LV|Ashton Jeanty|Runs straight ahead for a first down across the 17.|None|Run straight ahead|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:30|LV|Ashton Jeanty|Stopped for a loss of one, as specified in the following commentary.|-1|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:38|LV|Kirk Cousins; unidentified receiver|Completes a pass for a first down at the 30.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:46|LV|Michael Mayer|Catches a Cousins pass for a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:58|LV|Ashton Jeanty|Finds a hole and keeps pushing to the Miami 21 for a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:08|LV|Jack Bech|Catches a 15-yard touchdown from Cousins. Commentary describes Bech crossing above Mayer, whose underneath route holds the underneath coverage.|15|Crossing route with an underneath route holding coverage|unknown|unknown|unknown|verified vs DB|
|02:33|MIA|Caleb Douglas|Catches a quick third-and-15 pass but cannot escape to reach the first-down marker.|None|Quick pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:49|LV|Jack Bech|Catches a pass short of the 30. The reference to a loss of eight appears to describe the preceding situation, not this completion's yardage.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:59|LV|Ashton Jeanty|Runs for a first down and more, reaching approximately the 37. The following commentary references Jeanty and two tight ends.|None|unknown|Two tight ends|unknown|unknown|unverified (no DB match; caption-only)|
|03:11|LV|Michael Mayer|Catches an out route and apparently loses the ball on contact involving JuJu Brents; Zayne Anderson is mentioned at the loose ball. Replay commentary says Mayer's elbow was down with possession. No confirmed turnover.|None|Out route|unknown|unknown|JuJu Brents (contact)|unverified (no DB match; caption-only)|
|03:53|LV|M. Gay|Makes a 47-yard field goal for a 10-0 lead.|47|Field goal|unknown|unknown|unknown|verified vs DB|
|04:03|MIA|De'Von Achane|Runs from the 35 and surges across the 45 for a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:14|MIA|De'Von Achane|Picks up a first down, falling just inside the Raiders' 45.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:27|MIA|Dulcich|Catches a pass for an apparent first down with a flag down. Subsequent commentary mentions back-to-back holding penalties; the precise enforcement is unavailable.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:38|MIA|Washington|Catches a Willis dump-off, slips one tackle and is forced out of bounds.|None|Dump-off pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:51|MIA|C. Douglas|Gets open between defenders for a 25-yard completion down the right side to the LV 22.|25|Deep right pass|unknown|unknown|T. Stukes (forced out of bounds)|verified vs DB|
|05:03|MIA|De'Von Achane|Stopped and pushed back on third-and-one, bringing up fourth down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:11|MIA|Riley Patterson|Makes a 41-yard field goal to cut the deficit to 10-3.|41|Field goal|unknown|unknown|unknown|verified vs DB|
|05:25|LV|Washington|Picks up a first down and powers inside the Miami 30. The commentary identifies a rookie from Arkansas, but the supplied DB does not identify this play.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:37|LV|Jalen Nailor|Catches a Cousins pass while sliding near the 15.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:44|LV|Ashton Jeanty|Catches a 13-yard touchdown on third-and-eight. Commentary says he shakes nickelback Chris Johnson inside coming out of the backfield.|13|Backfield receiving route with an inside move|unknown|unknown|Chris Johnson|verified vs DB|
|06:19|MIA|C. Douglas|Catches a 30-yard pass down the middle to the LV 19, setting up a field-goal attempt.|30|Deep middle pass|unknown|unknown|Q. Walker (tackler)|verified vs DB|
|06:30|MIA|Riley Patterson|Makes a 37-yard field goal to end the half.|37|Field goal|unknown|unknown|unknown|verified vs DB|
|06:42|LV|K. Cousins|Throws deep left for J. Bech and is intercepted by M. Taaffe, who returns it two yards.|2|Deep left pass|unknown|unknown|M. Taaffe (interceptor)|verified vs DB|
|06:58|MIA|C. Bell|Catches a 25-yard Willis pass down the right side to the LV 27 following the interception.|25|Deep right pass|unknown|unknown|T. Stukes (tackler); M. Crosby (QB hit)|verified vs DB|
|07:09|MIA|Malik Willis; unidentified intended receiver|Throws to an open target inside the 15, but the following commentary says the receiver could not hang on. Receiver identity is unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:24|MIA|M. Willis|Scrambles right for a 14-yard touchdown. Commentary says Achane was covered and Willis chose to run.|14|Scramble right end|unknown|unknown|unknown|verified vs DB|
|07:54|LV|D. Laube|Breaks loose on a kickoff return to midfield. DB records a 50-yard return, forced out by the kicker.|50|Kickoff return|unknown|unknown|R. Patterson (forced out of bounds)|CONFLICT (yardage 50 vs DB)|
|08:11|LV|T. Tucker|Gets wide open for a 21-yard completion down the left side to the Miami 24.|21|Deep left pass|unknown|unknown|M. Taaffe (tackler); J. Phillips (QB hit)|verified vs DB|
|08:23|LV|A. Jeanty|Catches a short left pass and reaches the end zone for a 13-yard touchdown. Commentary credits play-action with stopping Rodriguez's and Brooks's feet.|13|Play-action; short left pass|unknown|unknown|Rodriguez; Brooks (identified in the play-action explanation)|verified vs DB|
|08:51|MIA|M. Willis|Overthrows a deep middle pass intended for C. Douglas after the blitz is picked up. T. Stukes intercepts with no return.|0|Deep middle pass|unknown|Blitz; coverage unknown|T. Stukes (interceptor)|verified vs DB|
|09:11|LV|Ashton Jeanty|Takes a handoff, breaks loose and spins in the air while gaining a first down.|None|Handoff run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:20|LV|Nailor|Catches a pass after a backfield fake and advances inside the 25.|None|Play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:32|LV|Kirk Cousins; Tre Tucker|Pass intended for Tucker is incomplete near the five.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:38|LV|Ashton Jeanty|Catches an underneath pass on third down and falls at the seven, leaving a field-goal attempt.|None|Underneath pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:48|LV|M. Gay|A field-goal sequence is reset. DB records an initial 25-yard make nullified by offensive offside on C. Rogers; captions do not clearly narrate that initial kick.|25|Field goal nullified by penalty|unknown|unknown|unknown|verified vs DB|
|09:51|LV|M. Gay|Makes the reset 30-yard field goal, extending the lead to 27-13.|30|Field goal|unknown|unknown|unknown|verified vs DB|
|10:01|MIA|J. Wright|Breaks through a kickoff-return hole and crosses midfield before C. White runs him down. DB places the end of the 79-yard return at the LV 18, despite the caption's inside-the-15 call.|79|Kickoff return|unknown|unknown|C. White (touchdown-saving pursuit)|CONFLICT (yardage 79 vs DB)|
|10:22|MIA|Malik Willis|Sacked hard by Nakobe Dean after pressure arrives.|None|unknown|unknown|unknown|Nakobe Dean (sack)|unverified (no DB match; caption-only)|
|10:32|MIA|R. Patterson|Misses a 41-yard field goal wide left following the long kickoff return and sacks.|41|Field goal|unknown|unknown|unknown|verified vs DB|
|10:42|LV|Ashton Jeanty|Reaches inside the 40 but is stopped short of a first down by Jordyn Brooks. Commentary explicitly describes a two-back offense with Dylan Laube.|None|unknown|Two backs: Ashton Jeanty and Dylan Laube|unknown|Jordyn Brooks (tackler)|unverified (no DB match; caption-only)|
|10:55|MIA|Malik Willis|Sacked by Maxx Crosby; commentary calls it the Raiders' third sack and Crosby's first.|None|unknown|unknown|unknown|Maxx Crosby (sack)|unverified (no DB match; caption-only)|
|11:12|LV|Ashton Jeanty|Tackled promptly; the caption cuts off before providing the result.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:24|LV|K. Cousins|Throws his second interception. DB identifies a deep middle pass intended for J. Nailor, intercepted by D. Trader and returned 14 yards to the LV 44.|14|Deep middle pass|unknown|unknown|D. Trader (interceptor)|verified vs DB|
|11:31|MIA|Malik Willis|Sacked back at the 46 by Maxx Crosby and Kwity Paye.|None|unknown|unknown|unknown|Maxx Crosby; Kwity Paye (sack)|unverified (no DB match; caption-only)|
|11:44|LV|Ashton Jeanty|Takes another carry; the result is not provided.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:56|LV|Unidentified tight end|Catches a Cousins pass, slips a tackle and gains a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:08|LV|Michael Mayer|Catches a dump-off and is tackled immediately.|None|Dump-off pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:14|LV|Kirk Cousins|Brought down while falling forward against a blitz. The captions do not reliably identify the defender.|None|unknown|unknown|Blitz; coverage unknown|unknown|unverified (no DB match; caption-only)|
|12:31|MIA|M. Washington|Catches a 30-yard pass down the middle, crossing midfield to the LV 44.|30|Deep middle pass|unknown|unknown|T. Stukes (tackler)|verified vs DB|
|12:36|MIA|Malik Willis; unidentified intended receiver|Pass is batted away, bringing up fourth down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:54|MIA|Malik Willis; unidentified intended receiver|Fourth-down pass falls incomplete and the Raiders take over.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:56|LV|Ashton Jeanty|Brought down immediately; Zach Sieler is named in the following commentary.|None|unknown|unknown|unknown|Zach Sieler (mentioned after the stop)|unverified (no DB match; caption-only)|
|13:13|LV|Mike Washington|Commentary identifies Washington during the late possession but provides no clear action or result.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:22|LV|Cole|Punts deep; the ball bounces inside the five and Raiders coverage players save it near the goal line.|None|Punt with coverage near the goal line|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:42|MIA|De'Von Achane|Catches a short completion; Quay Walker is named immediately afterward in discussion of his hitting.|None|Short pass|unknown|unknown|Quay Walker (mentioned after the completion)|unverified (no DB match; caption-only)|
|13:46|MIA|Malik Willis|Pressured in his own end zone and shoved backward by Kwity Paye. Commentary discusses forward progress barely beyond the line of scrimmage; no safety is established.|None|unknown|unknown|unknown|Kwity Paye (stop)|unverified (no DB match; caption-only)|
|14:06|MIA|M. Washington|Catches a 26-yard pass down the middle, then loses a fumble on J. Chinn's punch-out. LV's Q. Walker recovers at the Miami 34.|26|Deep middle pass|unknown|unknown|J. Chinn (tackle and forced fumble); Q. Walker (recovery)|verified vs DB|

Offense (Codex synthesis from this game's plays): Jeanty produced first downs on the ground and two 13-yard receiving touchdowns. / Used complementary receiving routes on Bech's touchdown and play-action on Jeanty's second touchdown and a Nailor completion. / Mayer supplied first-down receptions and an underneath route that helped create Bech's touchdown. / Cousins had time on several highlighted completions, including Tucker's 21-yard gain.

Defense weaknesses: Allowed multiple completions of at least 25 yards to Douglas, Bell and Washington. / Allowed Willis to convert a run after a pass fake and escape for a 14-yard touchdown. / Allowed Achane to gain first downs on consecutive highlighted carries.

Limitations: Analysis uses only the supplied captions and DB excerpt; no video frames or external sources were inspected. db_match contains the matching DB quarter and clock. The DB excerpt is selective, so NO DB MATCH does not mean a play did not occur. Unknown yardage, identities, formations and coverage are left unresolved. Shotgun and no-huddle details appearing only in DB text were not used as personnel_formation because that field requires explicit commentary. Blitz is recorded only when explicitly called; it does not establish the coverage behind it. Named tacklers, interceptors and sackers in defender_beaten are labeled by their actual roles and are not assertions that they were beaten. Interception yardage denotes return yards; field-goal yardage denotes kick distance. Return plays use the receiving team in team. The reset field-goal sequence is matched with DB assistance; the initial nullified kick is not clearly narrated. Mayer's apparent fumble is not treated as a confirmed turnover. The early delay penalty and late Washington identification are included as identifiable highlight events despite limited action detail. DB-only kickoffs, returns and other events not individually identifiable in these captions were omitted.


## Week 2: LV 26 - LAC 14 (game 401872941)
Video: Las Vegas Raiders vs Los Angeles Chargers Game Highlights | 2026 NFL Season Week 2 — https://www.youtube.com/watch?v=cyk5Vci3k-c  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 3: LV 35 - NO 27 (game 401872961)
Video: Las Vegas Raiders vs. New Orleans Saints Game Highlights | NFL 2026 Season Week 3 — https://www.youtube.com/watch?v=xcj0NwyEJUk  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 4: KC 30 - LV 27 (game 401872976)
Video: Kansas City Chiefs vs. Las Vegas Raiders Game Highlights | NFL 2026 Season Week 4 — https://www.youtube.com/watch?v=UH-pYLB0KQ4  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 5: LV 17 - NE 45 (game 401872986)
Video: Las Vegas Raiders vs. New England Patriots Game Highlights | 2026 NFL Season Week 5 — https://www.youtube.com/watch?v=fLKLrtqun84  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 6: BUF 33 - LV 30 (game 401873005)
Video: Buffalo Bills vs. Las Vegas Raiders Game Highlights | NFL 2026 Season Week 6 — https://www.youtube.com/watch?v=JCwv4Mrkdd8  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:19|BUF|James Cook|Escapes Crosby's early tackle attempt and gains nine.|9|unknown|unknown|unknown|Crosby|unverified (no DB match; caption-only)|
|00:28|BUF|Johnson|Allen is flushed from the pocket and completes a pass to Johnson for a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:40|BUF|Josh Allen|Walker gets to Allen for an apparent sack.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:45|BUF|Tyler Bass|Makes a 44-yard field goal.|44|unknown|unknown|unknown|unknown|verified vs DB|
|00:55|LV|Ashton Jeanty|Runs behind Rogers for approximately eight yards.|8|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:07|LV|Ashton Jeanty|Runs and is brought down by Bernard near the Buffalo 21.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:18|LV|unknown|Converts third-and-one; commentary references a tight end, but the receiver's identity is unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:28|LV|Brock Bowers|Draws defensive pass interference in the end zone after a fake, producing an automatic first down.|None|play-action|unknown|unknown|Buffalo number 21|unverified (no DB match; caption-only)|
|01:49|LV|Ashton Jeanty|Powers across the goal line with help from Rogers.|1|left tackle run|unknown|unknown|unknown|verified vs DB|
|02:23|BUF|Joshua Palmer|Allen extends the play with Crosby approaching and finds Palmer wide open for 37 yards.|37|deep right pass|unknown|unknown|Jeremy Chinn|verified vs DB|
|02:45|BUF|Johnson|Catches Allen's pass, gets past a defender and reaches approximately the 20.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:53|BUF|Dalton Kincaid|Catches a second-and-eight pass and is marked approximately a yard short of the first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:08|BUF|unknown|Third-and-goal end-zone pass is knocked away by Stukes.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:22|BUF|Tyler Bass|Makes a 28-yard field goal.|28|unknown|unknown|unknown|unknown|verified vs DB|
|03:30|LV|Kirk Cousins|Pass is knocked away by a defender captioned as 'Beneson,' with Rousseau applying pressure.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:45|BUF|James Cook|Catches an underneath pass on second-and-four, double-clutches the ball and is brought down.|None|underneath pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:04|BUF|James Cook|Fragmentary commentary identifies another ball to Cook; outcome is omitted.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:07|BUF|Keon Coleman|Catches a pass down the middle to the Las Vegas 31. Commentary calls it 22 yards; DB records 21.|21|short middle pass|unknown|unknown|Jeremy Chinn|verified vs DB|
|04:19|BUF|James Cook|Takes a dump-off into open space and goes out of bounds after 23 yards.|23|short right dump-off|unknown|unknown|Eric Stokes|verified vs DB|
|04:31|BUF|Khalil Shakir|Scores on a short pass with a perimeter block from Bell and offensive linemen leading outside.|9|swing pass|unknown|unknown|unknown|verified vs DB|
|05:04|unknown|unclear; caption says Shakir|A throw gains a first down. The surrounding captions conflict about team and receiver identity.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:08|LV|unclear; caption says Shakir|With Tucker in motion, a first-down play ends with Bishop tripping the ball carrier. Receiver name is unreliable.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:26|LV|Michael Mayer|Makes a catch for a first down, getting past Johnson.|None|unknown|unknown|unknown|Johnson|unverified (no DB match; caption-only)|
|05:37|LV|Washington|Breaks a run initially described as approximately 13 yards, then as 14.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:49|LV|Ashton Jeanty|Commentary references a six-yard gain by Jeanty.|6|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:49|LV|Ashton Jeanty|Called upon on third-and-four and gets pushed; final result is unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:56|LV|Matt Gay|Makes a 35-yard field goal.|35|unknown|unknown|unknown|unknown|verified vs DB|
|06:03|BUF|Josh Allen|With receivers flooding the left side, Allen is slung down by Max Crosby.|None|left-side flood|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:16|LV|Michael Mayer|Catches a pass for 11 yards.|11|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:24|LV|Michael Mayer|Catches another pass after a straight drop, with Chubb pressuring Cousins; stays in bounds and gains an unspecified amount.|None|straight dropback|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:41|LV|Tre Tucker|Catches Cousins' pass to the Buffalo eight late in the half.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:49|LV|Matt Gay|Makes a 27-yard field goal to end the half.|27|unknown|unknown|unknown|unknown|verified vs DB|
|06:58|LV|Nailer|Catches a third-and-ten pass well short of the first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:12|BUF|James Cook|Runs behind a blocker for more than ten yards.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:22|BUF|unknown|Commentary references a three-yard gain amid discussion of running rather than sliding; ball carrier is not explicit.|3|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:25|BUF|James Cook|Runs and is barely tripped up.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:34|BUF|Dalton Kincaid|Catches a pass but gains only one yard while fighting Stukes' tackle.|1|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:39|BUF|Tyler Bass|Makes a 47-yard field goal for a 16-13 lead.|47|unknown|unknown|unknown|unknown|verified vs DB|
|07:49|LV|Kirk Cousins|Short middle pass intended for Michael Mayer is intercepted by D. Williams, with no return.|0|short middle pass|unknown|unknown|unknown|verified vs DB|
|07:58|BUF|Dalton Kincaid|Third-and-eight target is ruled incomplete; defensive holding on number 31 gives Buffalo an automatic first down.|5|unknown|unknown|unknown|Las Vegas number 31|unverified (no DB match; caption-only)|
|08:32|BUF|unknown|Draws defensive pass interference on number 35, identified by commentary as Stukes.|None|unknown|unknown|unknown|Stukes|unverified (no DB match; caption-only)|
|08:49|BUF|Keon Coleman|Allen moves on third-and-eight and delivers a touchdown pass; commentary describes Coleman flipping into the end zone.|12|short middle pass|unknown|unknown|unknown|verified vs DB|
|09:09|LV|Michael Mayer|Catches a pass with blockers ahead and gains approximately 16-17 yards.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:26|LV|Brock Bowers|Catches a pass for approximately seven yards.|7|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:33|LV|Michael Mayer|Catches a deep middle pass. Commentary says 29 yards to the Buffalo 29; DB records 28 yards to the Buffalo 30.|28|deep middle pass|unknown|unknown|K. Elarms-Orr|verified vs DB|
|09:45|LV|Nailer|Makes a catch for a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:53|LV|Brock Bowers|Catches a third-and-ten pass inside the five with Benford on his back.|None|unknown|unknown|unknown|Benford|unverified (no DB match; caption-only)|
|10:04|LV|Kody|After Bowers moves across, a third-and-goal pass at the goal line goes in and out of the target's hands and is broken up.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:18|LV|Matt Gay|Makes a 23-yard field goal.|23|unknown|unknown|unknown|unknown|verified vs DB|
|10:28|BUF|Josh Allen|Hit as he releases a third-and-ten pass; Stokes is named in coverage and commentary identifies a slot blitz. Completion status is unclear.|None|unknown|unknown|slot blitz|unknown|unverified (no DB match; caption-only)|
|10:47|LV|Washington|Runs through a large opening for 18 yards before Hamlin tackles him.|18|middle run|unknown|unknown|Hamlin|unverified (no DB match; caption-only)|
|11:00|LV|Brock Bowers|Finds open space for an 18-yard reception with Cousins given ample time.|18|unknown|unknown|zone|unknown|unverified (no DB match; caption-only)|
|11:13|LV|Brock Bowers|Catches a deep left pass from the Buffalo 42 and is forced out at the 13 by Hamlin.|29|deep left pass|unknown|unknown|Damar Hamlin|verified vs DB|
|11:24|LV|Tre Tucker|Catches an 11-yard touchdown on third-and-eight; Cousins floats the ball over the top into a hole.|11|short right pass|unknown|unknown|unknown|verified vs DB|
|11:50|BUF|James Cook|Runs for approximately 11 yards, slipping through tackle attempts behind praised offensive-line blocking.|11|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:08|BUF|Dalton Kincaid|Catches a pass and breaks Quay Walker's tackle for 14 yards.|14|unknown|unknown|unknown|Quay Walker|unverified (no DB match; caption-only)|
|12:17|BUF|James Cook|Takes a short toss into open space for 26 yards; Chinn prevents the touchdown at the three.|26|short left pass|unknown|unknown|Jeremy Chinn|verified vs DB|
|12:32|BUF|James Cook|Scores from three yards out with offensive linemen pushing him across.|3|left guard run|unknown|unknown|unknown|verified vs DB|
|13:04|LV|Kirk Cousins|Pass is knocked down by Kilgore.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:15|BUF|Keon Coleman|Pulls down a pass for an unspecified gain.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:26|BUF|Khalil Shakir|Catches a third-and-nine pass and is immediately wrestled down by Stukes.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:42|BUF|Tyler Bass|Makes a 38-yard field goal, extending Buffalo's lead to 33-23.|38|unknown|unknown|unknown|unknown|verified vs DB|
|13:48|LV|Tre Tucker|Outruns two unnamed defenders down the middle and makes a diving 44-yard touchdown catch.|44|deep middle pass|unknown|unknown|two unnamed defenders|verified vs DB|
|14:29|LV|Khalil Shakir (BUF recovery)|Shakir secures Las Vegas' onside kick without advancing, clinching the game for Buffalo. DB records a 20-yard kick.|20|onside kick|unknown|unknown|unknown|CONFLICT (yardage 20 vs DB)|

Offense (Codex synthesis from this game's plays): Mayer supplied repeated completions and first downs, including a 28-yard gain. / Bowers produced consecutive fourth-quarter gains of 18 and 29 yards. / Tucker finished two passing touchdowns, including a diving 44-yard catch. / Washington supplied a run described as 13-14 yards and a later 18-yard middle run; Jeanty finished a one-yard touchdown with help from Rogers.

Defense weaknesses: Palmer became wide open for 37 yards while Allen extended the play. / Cook gained 23 and 26 yards on short receptions. / Defensive holding and pass interference extended Buffalo's possession after the interception. / Walker missed a tackle on Kincaid's 14-yard catch, and Buffalo's blocking supported Shakir's receiving touchdown and Cook's late rushing touchdown.

Limitations: Captions only; no frames were viewed and no external verification was performed. The supplied DB is a selected-play list, so NO DB MATCH does not establish that a play did not happen. DB-only plays without identifiable caption action were excluded, including Tucker's first-quarter 26-yard catch, most returns and the late 22-yard interference penalty. Matching DB yardage takes precedence over conflicting caption estimates. Null yards indicate an unspecified or conflicting gain; penalty and kick distances are identified in descriptions. Names without clear DB matches remain as captioned or unknown. Tacklers listed under defender_beaten identify the supplied matchup, not necessarily a missed tackle. No complete personnel formation was unambiguously stated for a specific play; the fragmented '11-B' discussion could not be reliably assigned. Zone and a slot blitz were explicitly described; other coverages, routes, blocking assignments and defensive responsibilities could not be determined.
