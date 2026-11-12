# MIA — Phase 8 film notes (Weeks 1–6, 2026)

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

Offense (Codex synthesis from this game's plays): Willis generated first downs with his legs, including a seven-yard run after a pass fake and a 14-yard touchdown scramble. / Explosive completions included Douglas for 25 and 30 yards, Bell for 25, and Washington for 30; Washington also gained 26 before fumbling. / Achane contributed first-down carries and short receiving gains.

Defense weaknesses: Allowed Bech's touchdown crosser above Mayer's underneath route. / Allowed two receiving touchdowns to Jeanty: one after an inside move against Chris Johnson and one on play-action that commentary said froze Rodriguez and Brooks. / Allowed Tucker to get wide open for a 21-yard completion and several Raiders first downs through runs and tight-end receptions. / Commentary credited the Raiders' interior blocking with controlling Miami's interior defensive front.

Limitations: Analysis uses only the supplied captions and DB excerpt; no video frames or external sources were inspected. db_match contains the matching DB quarter and clock. The DB excerpt is selective, so NO DB MATCH does not mean a play did not occur. Unknown yardage, identities, formations and coverage are left unresolved. Shotgun and no-huddle details appearing only in DB text were not used as personnel_formation because that field requires explicit commentary. Blitz is recorded only when explicitly called; it does not establish the coverage behind it. Named tacklers, interceptors and sackers in defender_beaten are labeled by their actual roles and are not assertions that they were beaten. Interception yardage denotes return yards; field-goal yardage denotes kick distance. Return plays use the receiving team in team. The reset field-goal sequence is matched with DB assistance; the initial nullified kick is not clearly narrated. Mayer's apparent fumble is not treated as a confirmed turnover. The early delay penalty and late Washington identification are included as identifiable highlight events despite limited action detail. DB-only kickoffs, returns and other events not individually identifiable in these captions were omitted.


## Week 2: MIA 13 - SF 35 (game 401872942)
Video: Miami Dolphins vs. San Francisco 49ers Game Highlights | NFL 2026 Week 2 — https://www.youtube.com/watch?v=pV8FmQa0a5w  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 3: KC 24 - MIA 10 (game 401872952)
Video: Kansas City Chiefs vs. Miami Dolphins Game Highlights | NFL 2026 Season Week 3 — https://www.youtube.com/watch?v=eyM7QUODW6c  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 4: MIA 10 - MIN 15 (game 401872974)
Video: Miami Dolphins vs Minnesota Vikings Game Highlights | 2026 NFL Season Week 4 — https://www.youtube.com/watch?v=YHo13wCIHT4  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 5: CIN 31 - MIA 24 (game 401872982)
Video: Cincinnati Bengals vs Miami Dolphins Game Highlights | 2026 NFL Season Week 5 — https://www.youtube.com/watch?v=veMELeUzxeo  | captions: yes

_No Codex film notes (no captions or run not completed)._
