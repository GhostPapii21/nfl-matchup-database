# MIA — Phase 8 film notes (Weeks 1–6, 2026)
> Note: games 401872944, 401872945, 401872952, 401872962, 401872964, 401872970, 401872985, 401872989 were extracted by a Grok Bot agent (not Codex) from the same captions; mostly scoring/20+ plays logged.
> Note: games 401872942, 401872974, 401872982 were extracted by Grok via the xAI API (grok-4.20-0309-non-reasoning, same prompt/schema as Codex, cleaned captions); sidecar provenance in film/grok_meta/. All other games with notes: Codex.

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

Offense (model synthesis from this game's plays): Willis generated first downs with his legs, including a seven-yard run after a pass fake and a 14-yard touchdown scramble. / Explosive completions included Douglas for 25 and 30 yards, Bell for 25, and Washington for 30; Washington also gained 26 before fumbling. / Achane contributed first-down carries and short receiving gains.

Defense weaknesses: Allowed Bech's touchdown crosser above Mayer's underneath route. / Allowed two receiving touchdowns to Jeanty: one after an inside move against Chris Johnson and one on play-action that commentary said froze Rodriguez and Brooks. / Allowed Tucker to get wide open for a 21-yard completion and several Raiders first downs through runs and tight-end receptions. / Commentary credited the Raiders' interior blocking with controlling Miami's interior defensive front.

Limitations: Analysis uses only the supplied captions and DB excerpt; no video frames or external sources were inspected. db_match contains the matching DB quarter and clock. The DB excerpt is selective, so NO DB MATCH does not mean a play did not occur. Unknown yardage, identities, formations and coverage are left unresolved. Shotgun and no-huddle details appearing only in DB text were not used as personnel_formation because that field requires explicit commentary. Blitz is recorded only when explicitly called; it does not establish the coverage behind it. Named tacklers, interceptors and sackers in defender_beaten are labeled by their actual roles and are not assertions that they were beaten. Interception yardage denotes return yards; field-goal yardage denotes kick distance. Return plays use the receiving team in team. The reset field-goal sequence is matched with DB assistance; the initial nullified kick is not clearly narrated. Mayer's apparent fumble is not treated as a confirmed turnover. The early delay penalty and late Washington identification are included as identifiable highlight events despite limited action detail. DB-only kickoffs, returns and other events not individually identifiable in these captions were omitted.


## Week 2: MIA 13 - SF 35 (game 401872942)
Video: Miami Dolphins vs. San Francisco 49ers Game Highlights | NFL 2026 Week 2 — https://www.youtube.com/watch?v=pV8FmQa0a5w  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:12|MIA|M.Willis|Willis with time, pass to DJ Herman on the sideline, fullback fumbles but out of bounds|None|unknown|unknown|unknown|F.Warner|unverified (no DB match; caption-only)|
|00:28|MIA|D.Achane|Achane patient run, ends up a yard shy of first down|None|run|unknown|unknown|G.Holden|unverified (no DB match; caption-only)|
|00:39|MIA|M.Willis|Willis over the middle to Achane to the 33 yard line, short of first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:47|MIA|R.Patterson|51 yard field goal attempt drifting wide right, no good|51|unknown|unknown|unknown|unknown|verified vs DB|
|01:01|SF|B.Purdy|Play fake, Purdy drops a dime on the near sideline to Demarcus Robinson for first down|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:17|SF|C.McCaffrey|McCaffrey gets the first down|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:24|SF|B.Purdy|Pressure coming, Purdy trying to break free, buys time, pass to Mike Evans|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:35|SF|B.Purdy|Third and 5, over the middle to McCaffrey inside the 10, rolls to the 1|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:49|SF|C.McCaffrey|McCaffrey second and goal in for the touchdown|1|run gap|unknown|unknown|unknown|verified vs DB|
|02:24|MIA|M.Washington|Breaking a tackle is Malik Washington with a first down to 39 yard line|None|unknown|unknown|unknown|D.Greenlaw|unverified (no DB match; caption-only)|
|02:34|MIA|D.Achane|Nice jump cut, De'Von Achane with a good run to the 40 yard line|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:44|MIA|D.Achane|Achane on third and long, burst up the middle, twists his way close to a first down|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:52|MIA|M.Willis|Short, fourth and inches, Malik Willis tush push with shove from DJ Herman for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:01|MIA|J.Wright|Wright gets the carry with an opening down to the 10 yard line|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:29|MIA|M.Willis|Third and goal from the 10, Willis under pressure from Bosa, gets away, chased out of bounds by Romello Height|None|unknown|unknown|unknown|N.Bosa|unverified (no DB match; caption-only)|
|03:40|MIA|R.Patterson|Field goal is true, Dolphins on the board|28|unknown|unknown|unknown|unknown|verified vs DB|
|03:58|SF|B.Purdy|Purdy zips this one in to Demarcus Robinson|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:14|SF|B.Purdy|Purdy on the run down the sideline and out of bounds|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:34|SF|B.Purdy|Purdy chugging to the goal line for the touchdown|2|scramble|unknown|unknown|unknown|verified vs DB|
|04:54|MIA|M.Willis|Willis in trouble, gets away from Bosa to the sideline, finds Washington for first down at the 20|23|unknown|unknown|unknown|N.Bosa|verified vs DB|
|05:06|MIA|M.Willis|Third down and 5, Willis with protection, pass to Caleb Douglas for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:15|MIA|D.Achane|Handoff to Achane, down at the 5|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:26|MIA|R.Patterson|24-yard field goal try is good|24|unknown|unknown|unknown|unknown|verified vs DB|
|05:38|SF|B.Purdy|Purdy over the middle, wide open to George Kittle on the run down to the 25|40|unknown|unknown|unknown|Z.Anderson|verified vs DB|
|05:48|SF|B.Purdy|Purdy with time, to the end zone, it's Kittle for the touchdown|12|unknown|unknown|unknown|W.Gay|verified vs DB|
|06:09|MIA|M.Washington|Third and 10, swing it to Washington, blockers in front but getting blown up|None|screen|unknown|unknown|R.Green|unverified (no DB match; caption-only)|
|06:25|SF|B.Purdy|Over the middle to Deebo Samuel, middle of the field to the 21|21|unknown|unknown|unknown|J.Brents|verified vs DB|
|06:41|SF|B.Purdy|Kaelon Black in the backfield, motions out, Purdy with a blitz up the middle, threads it to Mike Evans for 17 and first down|17|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:05|SF|B.Purdy|On third and 3, play action, Juszczyk down the sideline for touchdown|6|play-action|unknown|unknown|Z.Anderson|verified vs DB|
|07:36|SF|A.Dulich|Dulich the tight end out of bounds with a first down near the 45|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:40|SF|B.Purdy|Kittle in motion, fake the toss, Purdy with time, little pump fake, resets, finds Evans out of bounds at the 1|27|play-action|unknown|unknown|J.Uche|verified vs DB|
|07:55|SF|C.McCaffrey|First and goal at the 1, McCaffrey leaping in for the touchdown|1|run|unknown|unknown|unknown|verified vs DB|
|08:18|MIA|M.Willis|Willis short toss, nowhere to go|None|screen|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:29|SF|B.Purdy|Purdy over the middle, Kittle with the run and first down at the 42 yard line|26|unknown|unknown|unknown|M.Taaffe|verified vs DB|
|08:40|SF|B.Purdy|Purdy finding Khadarel Hodge dancing out to the 48 yard line|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:58|SF|C.McCaffrey|First down for San Francisco on the toss to McCaffrey to the Dolphins 44 yard line|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:05|SF|B.Purdy|Third down and 5, Purdy under pressure, dancing away, and the pass is incomplete|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:19|MIA|M.Willis|Willis to the air, catch made by Caleb Douglas for first down at the 31, converting on third and 7|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:28|MIA|M.Willis|Willis under all kinds of heat and down he goes, sacked by Keion White|None|unknown|unknown|unknown|K.White|unverified (no DB match; caption-only)|
|09:40|MIA|K.Black|Handoff to Kaelon Black, gets to the 36, pickup of 6|6|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:58|MIA|M.Willis|Deep shot down the sideline, it's Ryan Miller, takes it all the way for a Miami touchdown|77|deep shot|unknown|unknown|unknown|verified vs DB|

Offense (model synthesis from this game's plays): Explosive deep passing with big plays from Willis to Washington and Miller / Mobile QB Willis escaping pressure and extending plays / Run after catch ability from receivers like Washington and Douglas / Short yardage conversions with QB sneaks/tush push

Defense weaknesses: Struggled to stop SF run game in short yardage and goal line situations / Defenders losing assignments on motion and play action leading to big gains by Kittle and others / Missed tackles in open field allowing YAC / Vulnerable to deep middle passes and seam routes

Limitations: Could not determine specific personnel, formations, or coverage schemes as they were not explicitly stated by commentators. Many plays in captions had no direct match in the provided DB (only key scoring/big plays listed in DB). Some names mangled in captions (e.g. DJ Herman, Grayson Holden, Romello Height, Kaelon Black, Dulcich, Khadarel Hodge) and corrected only where clear match to DB. Could not determine exact yardage or defender for every play from captions alone. No video so concepts limited to what was said.


## Week 3: KC 24 - MIA 10 (game 401872952)
Video: Kansas City Chiefs vs. Miami Dolphins Game Highlights | NFL 2026 Season Week 3 — https://www.youtube.com/watch?v=eyM7QUODW6c  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:35|KC|Travis Kelce|Mahomes to Kelce on the move, downfield inside the 20, chased by Dante Trader|48|deep middle|unknown|unknown|Dante Trader (tackler)|verified vs DB|
|01:05|KC|Kenneth Walker|Walker gets the call, touchdown|10|run up the middle|unknown|unknown|unknown|verified vs DB|
|02:16|MIA|Ollie Gordon|Gordon drives to the 3, then touchdown run|3|goal-line run|unknown|unknown|unknown|verified vs DB|
|04:04|KC|Kenneth Walker|Walker touchdown (DB: 5-yd pass from Mahomes); commentary mentions fake left|5|short pass to RB|unknown|unknown|unknown|verified vs DB|
|05:41|MIA|Chris Bell|Play-action on the fly, catch and run of 44, out of bounds in Chiefs territory|44|play-action|unknown|unknown|unknown|verified vs DB|
|06:36|MIA|Malik Willis|Willis sidesteps, fumbles; ruled down then reversed, Chiefs recover|0|QB run|unknown|unknown|L.Sneed (forced/recovered)|verified vs DB|
|06:48|KC|Kenneth Walker|On the run, bursting into the secondary|22|run right tackle|unknown|unknown|unknown|verified vs DB|
|07:05|KC|Patrick Mahomes|Downfield for Rice, picked by Rodriguez|18|deep middle|unknown|unknown|J.Rodriguez (INT)|verified vs DB|
|08:07|MIA|Greg Dulcich|Play-action by Willis, downfield catch, 42-yard strike|42|play-action deep middle|unknown|unknown|unknown|verified vs DB|
|08:43|MIA|Riley Patterson|37-yard field goal good|None|field goal|unknown|unknown|unknown|verified vs DB|
|11:38|KC|Harrison Butker|34-yard field goal good|None|field goal|unknown|unknown|unknown|verified vs DB|
|12:29|KC|Rashee Rice|They got Rice, waylaid on the side by Johnson|34|deep right|unknown|unknown|C.Johnson|verified vs DB|
|12:44|KC|Travis Kelce|Touchdown Kelce; Trent: flat corner and sit down|11|short right|unknown|unknown|unknown|verified vs DB|
|13:19|MIA|Malik Willis|On the ricochet intercepted by Karlaftis|0|short right|unknown|unknown|G.Karlaftis (INT)|verified vs DB|
|13:38|KC|Harrison Butker|50-yarder missed|None|field goal|unknown|unknown|unknown|verified vs DB|
|11:17|KC|Noah Gray|Gain of 23, Rodriguez covering, Gray down near the 5 (DB lists 24)|23|deep left|unknown|unknown|Rodriguez (covering)|CONFLICT (yardage 23 vs DB)|

Offense (model synthesis from this game's plays): Play-action shots by Willis to Bell/Dulcich

Defense weaknesses: Kelce 48 deep middle / Walker TD runs and 22-yd burst / Rice 34 deep

Limitations: Captions only; no frames; captions are partly mangled and out of order. No coverage shells stated (only blitz counts: Chiefs bring 5 / 4). Noah Gray caption yardage 23 vs DB 24 kept as stated.


## Week 4: MIA 10 - MIN 15 (game 401872974)
Video: Miami Dolphins vs Minnesota Vikings Game Highlights | 2026 NFL Season Week 4 — https://www.youtube.com/watch?v=YHo13wCIHT4  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:38|MIN|K.Murray|Murray with pressure, swallowed up at the 40|None|unknown|unknown|unknown|Z.Sieler|unverified (no DB match; caption-only)|
|00:55|MIN|D.Dallas|Check short to Deejay Dallas, ends up short by about seven yards|None|unknown|unknown|unknown|J.Rodriguez|unverified (no DB match; caption-only)|
|01:12|MIA|J.Wright|Willis on the short toss, first down to the 25|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:15|MIA|W.Kacmarek|Kacmarek the rookie from Ohio State picks up 15|15|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:27|MIA|J.Wright|Wright going nowhere, first there the veteran Kyle Van Noy|None|unknown|unknown|unknown|K.Van Noy|unverified (no DB match; caption-only)|
|01:36|MIA|M.Willis|Willis throws it up for grabs and it's incomplete|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:49|MIN|M.Price|Price from the 26, looking for the edge, to the 40 down the sideline into Dolphins territory out of bounds near the 40 yard line|36|unknown|unknown|unknown|unknown|verified vs DB|
|02:07|MIN|K.Murray|Murray directing traffic, he's going to run and Kyler Murray with a slide, first down scramble to the 25|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:14|MIN|J.Jennings|Murray over the middle and there's Jauan Jennings down to the 30 yard line|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:26|MIN|M.Price|Price in the flat, stopped short by Jacob Rodriguez|None|unknown|unknown|unknown|J.Rodriguez|unverified (no DB match; caption-only)|
|02:32|MIN|W.Reichard|Will Reichard from 47 for the early lead, and the kick by Reichard is good|47|unknown|unknown|unknown|unknown|verified vs DB|
|02:48|MIA|O.Gordon|Gordon a burst up the middle and Ollie Gordon with a first down to the 33 yard line|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:02|MIA|M.Willis|Willis going to scramble and bouncing off contact, Willis was short but that second effort gets him the first down|None|unknown|unknown|unknown|B.Cashman|unverified (no DB match; caption-only)|
|03:19|MIA|M.Willis|Second and 20, Willis short to the sideline, nice move by Malik Washington for 15|15|unknown|unknown|unknown|B.Murphy|unverified (no DB match; caption-only)|
|03:38|MIA|M.Willis|Pressure comes, he's in trouble, couldn't go this time, Dallas Turner is there|None|unknown|unknown|unknown|D.Turner|verified vs DB|
|03:50|MIN|A.Jones|On second and six, it's Jones to the outside and Jones stopped at the 29|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:58|MIN|J.Addison|Murray on the roll, there's Addison with the catch, immediately tackled by the rookie Chris Johnson right at the 31|None|unknown|unknown|unknown|C.Johnson|unverified (no DB match; caption-only)|
|04:16|MIA|M.Willis|In trouble and down for the second time today, it's Josh Uche with his first sack|None|unknown|unknown|unknown|J.Uche|unverified (no DB match; caption-only)|
|04:29|MIA|M.Willis|Willis in trouble, chased from behind, got away from Van Ginkel, floating it down the sideline, he's got Chris Bell, Bell on the run, Bell towards the end zone, it's a touchdown for Miami but illegal touching offense|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:55|MIN|T.Hockenson|Off the play fake, Murray zips it into T.J. Hockenson, going up high to pull it in at the 49 on a first down|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:07|MIN|A.Jones|A little confusion on the handoff and Jones able to burst through a gaping hole|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:17|MIN|K.Murray|Third down and eight, Murray pressure from Robinson, tried to get rid of that football, they're going to call that an incomplete|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:30|MIN|W.Reichard|Reichard lines it up and drills it once more, 50 yard field goal is good|50|unknown|unknown|unknown|unknown|verified vs DB|
|05:37|MIA|J.Wright|First and 15, it's Wright, broke initial contact, Wright struggles out to the 47 yard line, Dallas Turner had a shot to bring him down for no gain but he fought through for six|6|unknown|unknown|unknown|D.Turner|unverified (no DB match; caption-only)|
|05:49|MIA|M.Willis|Second and eight at the 48, Willis in trouble, it's Turner with the heat and the pass incomplete|None|unknown|unknown|unknown|D.Turner|unverified (no DB match; caption-only)|
|06:22|MIN|K.Murray|Murray will throw over the middle, off the fingertips of Jordan Addison, just could not pull it in and the Dolphins defense gets the stop|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:42|MIA|M.Washington|Willis flips it out on the sideline and a burst for Washington across the 30 and down to the 31|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:54|MIA|M.Willis|Willis, nobody open, zips it to the sideline, he found Kevin Coleman a little late and couldn't get it to him at the 40 yard line|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:10|MIN|J.Addison|Kyler Murray down the sideline, there's Addison and a first down, Addison open with Juju Brents|None|deep shot|unknown|unknown|J.Brents|unverified (no DB match; caption-only)|
|07:22|MIN|K.Murray|A broken play but Kyler Murray making something out of nothing|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:29|MIN|T.Hockenson|Here's Murray on first down, open it's Hockenson and Hockenson down at the Dolphin 26, Anderson on the tackle but 20 yards through the air to the tight end T.J. Hockenson|20|unknown|unknown|unknown|Z.Anderson|verified vs DB|
|07:45|MIN|K.Murray|Murray in trouble, what a hit, it's Zach Sieler second time today that he's met Murray and he blasted the quarterback|None|unknown|unknown|unknown|Z.Sieler|unverified (no DB match; caption-only)|
|07:56|MIN|T.Hockenson|Third down and three, Murray backside pressure comes, finds Hockenson over the middle, that's a first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:11|MIN|K.Murray|Murray pressure coming, incomplete and it's second down, Michael Taaffe providing the heat|None|unknown|unknown|unknown|M.Taaffe|unverified (no DB match; caption-only)|
|08:20|MIN|W.Reichard|The field goal by Reichard is good and it is a 9-0 Minnesota lead|33|unknown|unknown|unknown|unknown|verified vs DB|
|08:35|MIA|O.Gordon|Third and five, it's Gordon again, he's got room and a first down plus more, Gordon down the sideline breaking away from Harrison Smith and Gordon all the way inside the Vikings 20 before Byron Murphy can track him down near the 12|53|unknown|unknown|unknown|H.Smith|verified vs DB|
|08:56|MIA|M.Willis|Third and eight, the low snap, Willis evades the rush, Willis still looking, directing traffic, trying to get it into the hands of Kevin Coleman but it's incomplete with Isaiah Rodgers in coverage and it's fourth down|None|unknown|unknown|unknown|I.Rodgers|unverified (no DB match; caption-only)|
|09:09|MIA|R.Patterson|27-yard try for Riley Patterson and the Dolphins are on the board|27|unknown|unknown|unknown|unknown|verified vs DB|
|09:25|MIN|A.Jones|It's Jones who will get the carry, has the edge, first down and more to the 35 of Miami, Brooks ran him out after he ran for 19|19|unknown|unknown|unknown|J.Brooks|unverified (no DB match; caption-only)|
|09:39|MIN|K.Murray|Third and 18, Murray steps away from Chop Robinson providing the heat, now Murray going to scramble, wanted a block and there's Rodriguez, tenth tackle, Rodriguez jarring him out of bounds inside the 25|None|unknown|unknown|unknown|C.Robinson|unverified (no DB match; caption-only)|
|09:51|MIN|W.Reichard|For Will Reichard and Reichard as usual perfect|41|unknown|unknown|unknown|unknown|verified vs DB|
|10:01|MIA|M.Willis|First and ten at the 33, Malik Willis off the play fake, finds Washington, some good moves in space, he ends up at the 39 in the arms of Blake Cashman|None|play-action|unknown|unknown|B.Cashman|unverified (no DB match; caption-only)|
|10:17|MIA|O.Gordon|Third and short, right bounced off one looking for a block, he'll find none, that defense stifling again and it's Kyle Van Noy|None|unknown|unknown|unknown|K.Van Noy|unverified (no DB match; caption-only)|
|10:29|MIN|T.Hockenson|Second and six, Murray dancing away from pressure, finds Hockenson on the sideline and Hockenson fights his way about a yard short of the first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:46|MIN|K.Murray|And Kyler in trouble, down he goes, it's Chop Robinson, he gets his first sack|None|unknown|unknown|unknown|C.Robinson|unverified (no DB match; caption-only)|
|10:57|MIA|M.Washington|Malik Willis on first down, he's got an open down and it's a first down to Malik Washington|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:09|MIA|M.Washington|Willis on the roll, it's Washington, a toe tap inside the 15 and it's first down for Miami at the 13 of Minnesota, 16 yards on that completion|16|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:21|MIA|O.Gordon|Washington the motion man, it's Gordon again, hops over a man, Gordon to the five all the way in for Miami touchdown|12|unknown|unknown|unknown|unknown|verified vs DB|
|12:11|MIN|T.Hockenson|Big play for the confidence of the Vikings here, Murray over the middle, it's Hockenson, T.J. Hockenson down near the 43 yard line with his eighth catch of the afternoon|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:24|MIN|T.Hockenson|On third and six, Murray over the middle, it's Hockenson again, look at Hockenson go inside the 40 and down to the 39|None|unknown|unknown|unknown|J.Marshall|unverified (no DB match; caption-only)|
|12:38|MIN|K.Murray|Ninth play of the drive and a third and six, this bring pressure, Murray in trouble able to get away, floats it out, it's Price who rolls forward, did he get enough? The last little tumble but he's just short|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:54|MIN|A.Jones|Murray the handoff to Jones who has the first down, good push on the left side|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:02|MIN|A.Jones|Murray short, good catch off the turf, Jones fumbles it but out of bounds, he's going to end up short of the first down, Josh Uche knocked it out of the hands of Aaron Jones|None|unknown|unknown|unknown|J.Uche|unverified (no DB match; caption-only)|
|13:22|MIN|W.Reichard|Has provided all of the points today for Minnesota and he adds three more to make it a 15-10 advantage|29|unknown|unknown|unknown|unknown|verified vs DB|
|13:30|MIA|M.Willis|For Malik Willis and the Dolphins offense, here comes the heat, Willis lofting it over the middle, jump ball incomplete, he wanted Chris Bell, Harrison Smith the veteran in coverage and it's fourth down|None|unknown|unknown|unknown|H.Smith|unverified (no DB match; caption-only)|
|13:45|MIN|A.Jones|First and ten from the 19, it's Jones and Jones into the secondary, bursts to the 34|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:56|MIN|J.Addison|Second and ten at the 33, off play action, Murray over the middle, finds Addison, Jordan Addison twisting his way all the way to the Miami 40, 27 yards through the air|27|play-action|unknown|unknown|C.Johnson|verified vs DB|
|14:11|MIN|T.Hockenson|Murray on second down over the middle for Hockenson again, catch number 11 and a first down to the Miami 15, picks up 22|22|unknown|unknown|unknown|J.Brooks|verified vs DB|

Offense (model synthesis from this game's plays): Explosive runs by O.Gordon including a 53-yard run and a 12-yard TD / Effective scrambling and second effort by M.Willis to gain first downs / Successful play-action passes leading to positive gains / Ability to convert on third downs with mobility and short passes

Defense weaknesses: Susceptible to big punt returns by M.Price / Vulnerable to deep passes and passes over the middle to T.Hockenson and J.Addison / Multiple sacks allowed on M.Willis and K.Murray / Struggled to stop MIN field goal drives

Limitations: Could not determine specific personnel formations, coverage schemes, or run gaps/directions in most cases as they were not explicitly stated by commentators or clearly shown in DB text. Many plays in captions did not have exact DB matches due to name mangling and incomplete details. Some yardage and exact player names corrected only where clear matches existed. Several plays lacked enough detail for yards, concepts, or defenders beaten.


## Week 5: CIN 31 - MIA 24 (game 401872982)
Video: Cincinnati Bengals vs Miami Dolphins Game Highlights | 2026 NFL Season Week 5 — https://www.youtube.com/watch?v=veMELeUzxeo  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:28|CIN|D.Meyers|81 yard kickoff return|81|unknown|unknown|unknown|unknown|verified vs DB|
|00:45|CIN|M.Gesicki|4 yard TD pass from J.Burrow|4|unknown|unknown|unknown|unknown|verified vs DB|
|01:14|MIA|C.Washington|Rush for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:25|MIA|O.Gordon|22 yard rush|22|unknown|unknown|unknown|unknown|verified vs DB|
|01:35|MIA|O.Gordon|1 yard rushing TD|1|unknown|unknown|unknown|unknown|verified vs DB|
|02:58|CIN|T.Higgins|Pass completion on slant|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:39|CIN|S.Perine|6 yard TD pass from J.Burrow|6|unknown|unknown|unknown|unknown|verified vs DB|
|04:04|MIA|J.Tolbert|22 yard pass reception|22|unknown|unknown|unknown|unknown|verified vs DB|
|04:14|MIA|M.Willis|Pass intercepted by J.Battle|None|unknown|unknown|unknown|unknown|verified vs DB|
|05:44|CIN|J.Burrow|Fumble recovered by MIA|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:35|MIA|M.Willis|Pass intercepted by CIN|None|unknown|unknown|unknown|unknown|verified vs DB|
|06:55|CIN|T.Hudson|Pass completion for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:19|CIN|J.Chase|Pass completion to the 1 yard line|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:29|CIN|T.Hudson|2 yard TD pass from J.Burrow|2|unknown|unknown|unknown|unknown|verified vs DB|
|08:57|MIA|M.Washington|28 yard punt return|28|unknown|unknown|unknown|unknown|verified vs DB|
|09:13|MIA|C.Bell|26 yard rush|26|unknown|unknown|unknown|unknown|verified vs DB|
|10:16|MIA|R.Patterson|29 yard field goal|29|unknown|unknown|unknown|unknown|verified vs DB|
|10:55|CIN|J.Chase|45 yard TD pass from J.Burrow|45|deep shot|unknown|unknown|unknown|verified vs DB|
|11:33|MIA|M.Willis|39 yard scramble|39|unknown|unknown|unknown|unknown|verified vs DB|
|12:14|MIA|K.Coleman|3 yard TD pass from M.Willis (2pt conversion good)|3|unknown|unknown|unknown|unknown|verified vs DB|
|13:31|MIA|M.Willis|Sacked and fumbled, recovered by J.Allen|-4|unknown|unknown|unknown|J.Allen|verified vs DB|
|14:02|CIN|E.McPherson|26 yard field goal|26|unknown|unknown|unknown|unknown|verified vs DB|
|14:41|MIA|G.Dulcich|Pass reception on sideline|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:47|MIA|M.Willis|1 yard rushing TD|1|unknown|unknown|unknown|unknown|verified vs DB|

Offense (model synthesis from this game's plays): Explosive run game with multiple RBs gaining 20+ yards / Ability to create big plays through scrambles and deep passes / Red zone efficiency in scoring TDs

Defense weaknesses: Poor tackling allowing long returns and big gains / Frequent turnovers via interceptions / Inability to stop short yardage and red zone passing attacks / Susceptible to fumbles in critical moments

Limitations: Could not determine specific concepts like run gaps, play-action, screens, RPOs, personnel formations, or coverage schemes because the captions and DB rarely explicitly state them. Many plays in captions had no direct DB match due to timing or description differences. Some player names were corrected using DB where matches were clear. Defender beaten names were limited to those mentioned. Several plays lacked yardage or exact details.
