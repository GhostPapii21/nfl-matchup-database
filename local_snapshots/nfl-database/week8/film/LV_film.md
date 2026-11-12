# LV — Phase 8 film notes (Weeks 1–6, 2026)
> Note: games 401872941, 401872961, 401872976, 401872986 were extracted by Grok via the xAI API (grok-4.20-0309-non-reasoning, same prompt/schema as Codex, cleaned captions); sidecar provenance in film/grok_meta/. All other games with notes: Codex.

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

Offense (model synthesis from this game's plays): Jeanty produced first downs on the ground and two 13-yard receiving touchdowns. / Used complementary receiving routes on Bech's touchdown and play-action on Jeanty's second touchdown and a Nailor completion. / Mayer supplied first-down receptions and an underneath route that helped create Bech's touchdown. / Cousins had time on several highlighted completions, including Tucker's 21-yard gain.

Defense weaknesses: Allowed multiple completions of at least 25 yards to Douglas, Bell and Washington. / Allowed Willis to convert a run after a pass fake and escape for a 14-yard touchdown. / Allowed Achane to gain first downs on consecutive highlighted carries.

Limitations: Analysis uses only the supplied captions and DB excerpt; no video frames or external sources were inspected. db_match contains the matching DB quarter and clock. The DB excerpt is selective, so NO DB MATCH does not mean a play did not occur. Unknown yardage, identities, formations and coverage are left unresolved. Shotgun and no-huddle details appearing only in DB text were not used as personnel_formation because that field requires explicit commentary. Blitz is recorded only when explicitly called; it does not establish the coverage behind it. Named tacklers, interceptors and sackers in defender_beaten are labeled by their actual roles and are not assertions that they were beaten. Interception yardage denotes return yards; field-goal yardage denotes kick distance. Return plays use the receiving team in team. The reset field-goal sequence is matched with DB assistance; the initial nullified kick is not clearly narrated. Mayer's apparent fumble is not treated as a confirmed turnover. The early delay penalty and late Washington identification are included as identifiable highlight events despite limited action detail. DB-only kickoffs, returns and other events not individually identifiable in these captions were omitted.


## Week 2: LV 26 - LAC 14 (game 401872941)
Video: Las Vegas Raiders vs Los Angeles Chargers Game Highlights | 2026 NFL Season Week 2 — https://www.youtube.com/watch?v=cyk5Vci3k-c  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:26|LAC|Johnson|Johnson trying to turn the corner and tackled near first down marker|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:39|LAC|Herbert|Herbert gets it out quickly and out of bounds|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:50|LAC|Hampton|Hampton up the middle, gain of 7|7|run|unknown|unknown|Walker|unverified (no DB match; caption-only)|
|01:01|LAC|Herbert|Herbert to the air, pump fakes, in trouble, incomplete|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:12|LAC|Dicker|Cameron from 58 yards, field goal attempt, massive doink, no good|58|unknown|unknown|unknown|unknown|verified vs DB|
|01:24|LV|Mayer|Screen to Michael Mayer, gets back to line of scrimmage|0|screen|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:41|LV|Tucker|Cousins down the middle, first down, Tre Tucker making the catch|None|unknown|unknown|unknown|Jefferson|unverified (no DB match; caption-only)|
|01:48|LV|Cousins|Cousins over the middle, receiver slipped and picked off|0|unknown|unknown|unknown|unknown|verified vs DB|
|02:02|LAC|Hampton|Get it to Hampton on first down, hit hard and dragged down|None|run|unknown|unknown|Hezekiah|unverified (no DB match; caption-only)|
|02:12|LAC|Herbert|Herbert looking left, fires left, ruled a catch by Brennan Thompson then ruled no|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:27|LAC|Herbert|Herbert is brought down, good coverage downfield|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:01|LV|Cousins|Cousins is sacked by Tomlinson|None|unknown|unknown|unknown|Tomlinson|unverified (no DB match; caption-only)|
|03:10|LAC|Davis|Davis fair catch at the 16|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:19|LAC|Mitchell|Mitchell gets the call to the 21 yard line|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:30|LAC|Herbert|Herbert looking left, throws, juggled and intercepted by Hezekiah Masses|0|unknown|unknown|unknown|unknown|verified vs DB|
|03:44|LV|Cousins|Cousins pump fakes, now fires, at the 10, five, poked away but recovered|None|unknown|unknown|unknown|Johnson|unverified (no DB match; caption-only)|
|03:58|LV|Jeanty|Give it to Jeanty left side, tripped up|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:06|LV|Jeanty|Jeanty bobbles it, not going to get there|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:17|LAC|Hampton|They do run it, Hampton tackled at the four yard line|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:27|LV|Tucker|To Tucker for a first down, tight window throw by Kirk Cousins|None|unknown|unknown|unknown|Hart|unverified (no DB match; caption-only)|
|04:40|LV|Tucker|Cousins back into the air, looking deep, takes a shot, Tucker touchdown, 40-yard strike|40|deep shot|unknown|unknown|unknown|verified vs DB|
|05:15|LAC|McConkey|Third and 11, McConkey, fires and he's got the catch|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:22|LAC|Hampton|Blitz coming by Johnson, Herbert gets rid of it, Hampton has plenty of room to run, first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:30|LAC|Hampton|Hampton again right up the middle and picks up the first down|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:39|LAC|Hampton|Hampton back in, left side at the five, down at the one|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:54|LAC|Hampton|First and goal, Hampton and this time he's in there for touchdown|1|run|unknown|unknown|unknown|verified vs DB|
|06:14|LV|Mayer|Cousins to Mayer, good for a first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:22|LV|Cousins|Third and nine, pressure coming, Cousins in trouble and sacked|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:36|LAC|Herbert|Herbert to the right side, he's got the first down, Charlie Cooler bringing that one in|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:44|LAC|Herbert|Herbert pressure coming, hit and incomplete|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:01|LV|Tucker|Second and 10, Cousins has time, takes a big shot downfield for Tucker and Tucker holds on for 42 yards|42|deep shot|unknown|unknown|unknown|verified vs DB|
|07:16|LV|Jeanty|Third and nine, they run it with Jeanty, big tackle|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:24|LV|Gay|Field goal attempt for Matt Gay, new career long, good from 59 yards|59|unknown|unknown|unknown|unknown|verified vs DB|
|07:35|LAC|Hampton|They will just run it right up the middle, Hampton|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:49|LAC|Hampton|Hampton with a punishing run, gain of 6 and a first down|6|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:58|LAC|Herbert|Third and five, here comes Crosby, Herbert steps up, throws, wide open Harris for 53 yards to the 5|53|deep shot|unknown|unknown|Crosby|verified vs DB|
|08:15|LAC|Herbert|Fakes it to Hampton, Crosby is coming, Herbert touchdown to tight end|10|play-action|unknown|unknown|Crosby|verified vs DB|
|08:52|LV|Thomas|Play action, Cousins to Ian Thomas, tight end, takes a shot and bounces right off and gets some extra yards|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:07|LV|Young|Throws it back to Chychun, Chychun has a wide open man to Young inside the 20 for 27 yards|27|unknown|unknown|unknown|unknown|verified vs DB|
|09:23|LV|White|Cousins throwing, end zone and it is caught by Codey White for 13 yard touchdown|13|unknown|unknown|unknown|unknown|verified vs DB|
|09:44|LAC|Harris|Snap, hit Harris, ball is loose|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:49|LAC|Herbert|Herbert lost the football, Hampton picks it up|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:49|LAC|Mitchell|Herbert gets it out quickly to Mitchell, makes the catch, down the sideline and out of bounds by Eichenberg, pickup of 14 yards|14|unknown|unknown|unknown|Eichenberg|unverified (no DB match; caption-only)|
|11:03|LAC|Hampton|Third down and three, Hampton number 21, he's not going to get there|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:20|LV|Jeanty|Second and six, here's Jeanty, gets by one tackle, breaks another|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:31|LV|Jeanty|Fake it to Jeanty, pressure coming and Jeanty dropped it|None|RPO|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:04|LAC|Herbert|Herbert gets hit from behind and he lost the football, fumble recovered by Chinn for 43 yards|43|unknown|unknown|unknown|unknown|verified vs DB|
|12:33|LV|White|Third down and five, Cousins into the end zone, wide open, touchdown Codey White|11|unknown|unknown|unknown|unknown|verified vs DB|
|13:04|LAC|Herbert|Herbert with time, fires, picked off, Masses does it again|0|unknown|unknown|unknown|unknown|verified vs DB|
|13:24|LAC|Crosby|Incomplete, flag down in end zone, holding on 76, results in a safety|0|unknown|unknown|unknown|unknown|verified vs DB|

Offense (model synthesis from this game's plays): Deep passing game with Cousins to Tucker / Red zone efficiency with multiple passing touchdowns / Exploiting safeties in two-high coverage on deep shots

Defense weaknesses: Susceptible to big passing plays allowing 50+ yard receptions / Run defense challenged by Hampton's inside runs / Missed tackles in open field on returns and runs

Limitations: Could not determine specific personnel formations, coverage schemes, or exact run gaps/directions in most cases as they were not explicitly stated by commentators. Many caption plays had no direct DB match due to name mangling and incomplete details. Yardage often not specified in captions. Some player names corrected only on clear matches.


## Week 3: LV 35 - NO 27 (game 401872961)
Video: Las Vegas Raiders vs. New Orleans Saints Game Highlights | NFL 2026 Season Week 3 — https://www.youtube.com/watch?v=xcj0NwyEJUk  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:26|LV|Naylor|Cousins to Naylor for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:37|LV|Bowers|Cousins to Bowers to the 35|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:46|LV|Bowers|They find Bowers again|None|unknown|unknown|man|Justin Early|unverified (no DB match; caption-only)|
|01:09|LV|Gay|Matt Gay field goal|41|unknown|unknown|unknown|unknown|verified vs DB|
|01:25|NO|Shough|Shough off and running, 36 yards|36|scramble right end|unknown|unknown|unknown|verified vs DB|
|01:42|NO|Vele|Lasers over the middle to Devin Vele|None|slant pattern|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:00|NO|Johnson|Third and goal from the two, touchdown Saints!|2|out route|unknown|unknown|Pola-Mao|verified vs DB|
|02:45|LV|Bowers|Bowers catch number four|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:57|LV|Mayer|Michael Mayer picks up the first down|None|unknown|unknown|unknown|Elliss|unverified (no DB match; caption-only)|
|03:10|LV|Tucker|To Tre Tucker on slant route|None|slant|unknown|unknown|McKinstry|unverified (no DB match; caption-only)|
|03:28|LV|Gay|Gay from 37 ties game at 6-6|37|unknown|unknown|unknown|unknown|verified vs DB|
|03:51|LV|Mayer|Cousins to Mayer second catch|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:03|LV|Bowers|Cousins finds Bowers to the 20-yard line|19|unknown|unknown|unknown|Elliss|unverified (no DB match; caption-only)|
|04:55|LV|Mayer|Cousins zips it to Mayer, touchdown Raiders|3|play-action|two tight ends two backs|unknown|Reid|verified vs DB|
|05:26|NO|Olave|Chris Olave second catch down the sideline|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:49|NO|Fant|Noah Fant second tight end wins the race to the sideline|None|unknown|unknown|man|Pola-Mao|unverified (no DB match; caption-only)|
|06:06|NO|Fant|Shough fires, touchdown Noah Fant|3|quick slant|unknown|man|Pola-Mao|verified vs DB|
|06:40|LV|Bowers|Cousins floater caught by Bowers|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:47|LV|Tucker|Checkdown to Tre Tucker|None|checkdown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:01|LV|Jeanty|Cousins for Jeanty to the 25|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:19|LV|Bowers|Brock Bowers after the catch|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:43|LV|Gay|Gay from 25 connects at end of half|25|unknown|unknown|unknown|unknown|verified vs DB|
|07:56|NO|Shough|Shough on the run, throw, picks up 11|11|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:07|NO|Achane|Achane zigzags for first to the 36|None|unknown|unknown|unknown|Dean|unverified (no DB match; caption-only)|
|08:20|NO|Kamara|Kamara picks up 10|10|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:31|NO|Kamara|Kamara keeps it going|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:38|NO|Achane|Achane carries for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:52|NO|Johnson|Johnson the tight end has the first|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:13|NO|Johnson|Shough to Johnson, Saints strike back, touchdown|1|play-action|unknown|unknown|unknown|verified vs DB|
|10:10|NO|Achane|Achane down the sideline hammered around the 15|None|unknown|unknown|unknown|Chinn|unverified (no DB match; caption-only)|
|10:24|NO|Fant|Fant spreading by the pylon for touchdown|16|unknown|unknown|unknown|unknown|verified vs DB|
|10:52|LV|Bowers|Cousins to Bowers on sideline for first down|None|unknown|unknown|unknown|McKinstry|verified vs DB|
|11:11|LV|Washington|Handoff to Washington, touchdown Raiders|36|unknown|unknown|unknown|Reid|verified vs DB|
|12:14|NO|Olave|Olave climbs the ladder and brings it in|22|unknown|unknown|unknown|unknown|verified vs DB|
|12:37|NO|Shough|Shough hit as he throws, ruled a fumble recovered by Raiders|0|unknown|unknown|unknown|Crosby|verified vs DB|
|12:54|LV|Jeanty|Cousins to Jeanty, lowers shoulder inside the 35|22|unknown|unknown|unknown|Elliss|verified vs DB|
|13:21|LV|Tucker|Cousins finds Tucker, first and goal|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:38|LV|White|Cousins throws a dart to Cody White, touchdown|4|play-action|unknown|unknown|unknown|verified vs DB|
|14:35|LV|Bowers|Cousins fires to Bowers, touchdown Raiders|4|unknown|unknown|man|unknown|verified vs DB|
|15:41|NO|Johnson|Shough finds Johnson, tight end makes one miss|22|unknown|unknown|unknown|Pola-Mao|verified vs DB|
|15:54|NO|Olave|Shough zips to Olave right at the 20|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|16:05|NO|Shough|Shough got rid of it, lost the ball, fumble recovered by Raiders|0|unknown|unknown|unknown|Chinn|verified vs DB|
|16:57|NO|Olave|Shough to Olave for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|17:10|NO|Johnson|Johnson lost the ball, fumble recovered by Raiders|1|checkdown|unknown|unknown|Dean|verified vs DB|

Offense (model synthesis from this game's plays): Frequent targeting of tight ends especially Brock Bowers with multiple catches early and in red zone / Effective use of play-action passes leading to tight end touchdowns / Successful field goal kicking by Matt Gay / Ability to execute quick passes and checkdowns to maintain drives / Explosive runs including long touchdown by Washington

Defense weaknesses: Vulnerable to tight end receptions allowing multiple Saints TDs to Fant and Johnson / Susceptible to quarterback scrambles and mobile QB plays / Allowed big passing plays and first downs to Saints receivers and tight ends

Limitations: Could not determine exact personnel formations, most coverage schemes, or all run gaps/directions as they were rarely explicitly stated by commentators. Many plays in captions did not perfectly align with DB entries so used 'NO DB MATCH' where no clear match. Auto-generated captions had many name mangles corrected only on clear matches to DB. Some yardage and details inferred from context but stuck to explicit mentions.


## Week 4: KC 30 - LV 27 (game 401872976)
Video: Kansas City Chiefs vs. Las Vegas Raiders Game Highlights | NFL 2026 Season Week 4 — https://www.youtube.com/watch?v=UH-pYLB0KQ4  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:08|LV|unknown|Raiders force a three and out|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:15|LV|unknown|Fake punt, wide open space and a first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:21|LV|unknown|Raiders rue the decision for the re-kick, fake and a first|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:28|LV|Tonga|Third and a yard to go, full house backfield, Tonga gets the handoff up the middle|None|run gap/direction|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:45|LV|K.Cousins|Come out with three tight ends, Cousins threatening to keep it, stops and completes it|None|unknown|13 personnel with three tight ends|unknown|unknown|unverified (no DB match; caption-only)|
|00:52|LV|Mayer|Mayer able to repurchase it|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:59|LV|Jeanty|Jeanty behind him, they fake it to him|None|RPO|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:01|LV|D.Young|He rose left, sets, fires, completes the pass to Young|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:12|LV|unknown|Classes, fakes a toss to him down the field, there it is and a touchdown! Thomas!|27|deep shot|unknown|unknown|unknown|verified vs DB|
|01:29|LV|I.Thomas|Ian Thomas with the touchdown grab|27|deep shot|13 personnel with three tight ends|unknown|unknown|verified vs DB|
|01:39|KC|Rashee Rice|The pass over to Rashee Rice. Rice pulls up, was looking upfield|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:49|KC|P.Mahomes|Third and one, second and one. Mahomes rolling out, he fought for it right off of Walker|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:06|KC|Noah Gray|Finds the safety valve and got the first down with Noah Gray|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:15|KC|X.Worthy|Mahomes likes the default to Worthy, and he makes the catch|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:22|KC|T.Thornton|Third and goal. Thornton wide open for the touchdown!|2|unknown|unknown|unknown|unknown|verified vs DB|
|02:26|KC|T.Thornton|That is almost the identical play they won the Super Bowl against San Francisco in overtime with that play|2|unknown|unknown|unknown|unknown|verified vs DB|
|02:49|LV|K.Cousins|Third and 9, down the field, not there. Tried to go to Bowers for the first time|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:55|LV|B.Bowers|One-on-one coverage, the rookie on Brock Bowers. It is a pure one-on-one|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:03|KC|K.Walker|Walker, Chinn tries to fight him off, but fights through the tackle and picks up the first|21|run gap/direction|unknown|unknown|unknown|verified vs DB|
|03:14|KC|K.Walker|Second and 8. Patrick hands it back off to Walker. Another one. Another first down!|None|run gap/direction|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:31|LV|K.Cousins|Now forced out of the pocket, able to release it. Almost intercepted. Stukes had a play on it|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:41|LV|B.Bowers|They start this drive at the 12. He has got his man out past the 30-yard line. Bowers goes for 18|18|unknown|unknown|unknown|J.Cochrane|CONFLICT (yardage 18 vs DB)|
|03:52|LV|B.Bowers|Bowers is going to slip behind Jack Cochrane in coverage|18|unknown|unknown|unknown|J.Cochrane|CONFLICT (yardage 18 vs DB)|
|03:56|LV|Mayer|The pass play to Mayer. They are going to spot him short of the 40|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:01|LV|T.Tucker|Second and 10. Driving for the first down is Tre Tucker|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:17|LV|A.Jeanty|Here is Jeanty. Jeanty patient|None|run gap/direction|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:25|LV|M.Washington|Now at the Kansas City 38. Second and two, they go with the rookie Washington. It paid off. He has got the first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:44|LV|K.Cousins|Third and 8. Cousins down the middle. That comes out on Williams as Naylor is laid out at the 5|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:55|LV|unknown|Personal foul, unnecessary roughness. Defense number 20. 15-yard penalty. Automatic first down|None|unknown|unknown|unknown|unknown|verified vs DB|
|05:06|LV|A.Jeanty|Third and 13. They go screen. They go Jeanty. Jeanty trying to get past. He will not be able to do that|None|screen|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:14|LV|unknown|Matt Gay, 32 yards. The kick is good|32|unknown|unknown|unknown|unknown|verified vs DB|
|05:26|KC|Kelce|Second and 4. Across the middle. Kelce has the catch|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:43|KC|P.Mahomes|Mahomes backpedaled, flings, wide open|42|deep shot|unknown|unknown|unknown|verified vs DB|
|05:54|KC|K.Walker|It is second and goal. Pressure from behind. Walker got to him|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:58|KC|unknown|Quay Walker chased him down! And a loss of seven|-7|unknown|unknown|unknown|Q.Walker|unverified (no DB match; caption-only)|
|06:02|KC|unknown|Butker. To tie the game, it is good|28|unknown|unknown|unknown|unknown|verified vs DB|
|06:11|LV|K.Cousins|Third and 9. Cousins steps up, fires. It is somehow caught. Bowers stayed on the coverage|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:20|LV|unknown|Second penalty on Nohl Williams. 17 seconds, no timeouts. Takes it down to the 29|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:40|LV|unknown|Matt Gay to close out the half. To give Las Vegas the lead at halftime. And the kick is true|48|unknown|unknown|unknown|unknown|verified vs DB|
|06:53|LV|A.Jeanty|Second and 3. They stay with Jeanty. That move, very good vision by Jeanty that time|28|run gap/direction|unknown|unknown|unknown|verified vs DB|
|07:11|LV|A.Jeanty|Jennettey is racing down the sideline. Look at him keep that balance and the Raiders strike with a big one|28|run gap/direction|unknown|unknown|unknown|verified vs DB|
|07:23|LV|K.Cousins|Pass, dangerous. And knocked down, trying to find|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:28|LV|K.Cousins|Out of the gun, Jeanty flanking him. Looking for Bowers. It's not there. He throws and it's incomplete|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:58|KC|P.Mahomes|Ha moments has all kinds of time and now the pass is over the head of Thornton|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:08|LV|unknown|Goes back instead across the middle and got a first down. Back to Thomas who scored their touchdown from 27 yards out in the first quarter|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:28|LV|M.Washington|Klint Kubiak has talked about how Mike Washington has earned more recommends in this offense|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:34|LV|unknown|Third and 3. Jurisdiction neither, they got the first. The catch was made at the 26|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:44|LV|K.Cousins|Laube is the running back. Cousins flushed out, now throws and incomplete. Again|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:01|KC|K.Walker|Walker is going to change that in one big run! Will they catch him? At the 20, the 30, stiff arming out of bounds at the 10|76|run gap/direction|unknown|unknown|T.Johnson|verified vs DB|
|09:13|KC|T.Thornton|Mahomes to the end zone. Wide open. Thornton has the seconds touchdown catch and Kansas City has taken the lead|8|unknown|unknown|unknown|unknown|verified vs DB|
|09:24|KC|T.Thornton|He's just going to sift through all this coverage. The Raiders aren't able to figure out who has who and he ends it wide open in the back|8|unknown|unknown|unknown|unknown|verified vs DB|
|09:33|KC|T.Thornton|Back shoulder, Patrick Mahomes. Thornton, touchdown|8|unknown|unknown|unknown|unknown|verified vs DB|
|09:53|LV|unknown|They tried to slip it. He's forced out and suddenly the Raiders get the jolt they needed|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:04|LV|B.Bowers|Pressure. Able to get away and the ball is held on the by Bowers|21|unknown|unknown|unknown|M.Delane|verified vs DB|
|10:13|LV|T.Tucker|The Chiefs gave up four conversions last week of third and 8 or longer as Tucker is not going to be able to add to that cause as they are shut down again at the line|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:22|LV|unknown|Wasn't a whole lot and Gay will you have this family 44 yards. Cole on the hold and the kick is good|44|unknown|unknown|unknown|unknown|verified vs DB|
|10:46|LV|C.White|Downfield. It's caught! What a catch and an adjustment. Colby White has made plays|27|deep shot|unknown|unknown|M.Delane|verified vs DB|
|10:58|LV|A.Jeanty|Second and 4. Jeanty broke through. Able to get away and Williams finally pushes him out. The longest running play of the afternoon goes for 19|19|run gap/direction|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:06|LV|Mayer|On a first down. Cousins adjusting and going across his body to Mayer and another catch for the kind corps|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:17|LV|A.Jeanty|Third and 2. Extra line man in. Not a long two. Jeanty trying to back his way there and he's going to be short|None|run gap/direction|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:33|LV|unknown|Gay from 48. Ball corrected itself and it's good. And he's 10-10 on the season and field with the lead|48|unknown|unknown|unknown|unknown|verified vs DB|
|11:43|KC|T.Thornton|Raiders are going to bring it. Mahomes is going to launch it and has Thornton there in stride! And Thornton is all the way to the 4-yard line. They beat the blitz for the big one|55|deep shot|unknown|unknown|T.Stukes|verified vs DB|
|11:55|KC|K.Walker|The give. It's Walker and he breezes in too give Kansas City the lead right back|2|run gap/direction|unknown|unknown|unknown|verified vs DB|
|12:07|KC|K.Walker|They go behind Kalian other and the undrafted rookie Benton and Walker steps his way into the end zone to take the lead|22|run gap/direction|unknown|unknown|unknown|verified vs DB|
|12:46|LV|D.Young|The ball is on the ground. And the Chiefs think they have it! Young was the returner. Oh, Kansas City has recovered!|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:06|KC|K.Walker|Walker breaking outside. He's got room. Walker is taking it, diving. Sailing in and a touchdown again for Walker. Two touchdowns seconds apart|22|run gap/direction|unknown|unknown|unknown|verified vs DB|
|13:48|LV|A.Jeanty|So they have two completions and the 15-yard penalty. Hesitated far meet then unloads it to Jeanty who lowers the shoulder for 11|11|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:59|LV|unknown|Want to hurry up and try to get now and then trying an onside, touchdown with the two-pointer|20|unknown|unknown|unknown|unknown|verified vs DB|
|14:04|LV|K.Cousins|Cousins so now got away. The 38-year-old throws it to the end zone and caught! What a play! Remarkable. Bowers has the touchdown|20|deep shot|unknown|unknown|unknown|verified vs DB|
|14:32|LV|unknown|Now the two-point attempt. To bring it to three. Cousins zips it. Caught. Back of the end zone and it's 30-27|None|unknown|unknown|unknown|unknown|verified vs DB|
|14:43|KC|P.Mahomes|Mahomes. Back in the shotgun. Low snap! On the ground! Running around and heaving it down the field, incomplete|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:02|LV|Mayer|As the pass goes to Mayer and look at Bolton just sling him to the turf|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:10|LV|B.Bowers|Find a way to get the ball to Brock Bowers. Here he is on the near side. Bowers|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:13|LV|A.Jeanty|Pass to Jeanty. Racing out of bounds. They got the first on fourth and 10|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:23|LV|T.Tucker|There's your down the middle they go Tucker off the turf. They call it a catch|23|unknown|unknown|unknown|C.Conner|verified vs DB|
|15:31|LV|K.Cousins|With 10 seconds. Cousins, flag down. Got hit when he threw it, got intercepted|None|unknown|unknown|unknown|X.Nwankpa|verified vs DB|

Offense (model synthesis from this game's plays): Heavy use of multiple TEs (B.Bowers, I.Thomas, Mayer) for big gains and TDs / Successful deep shots and one-on-one matchups / Effective screen and RPO plays with A.Jeanty / Long sustained drives and clutch plays in final minutes

Defense weaknesses: Struggled to contain KC RBs especially K.Walker on long runs / Inability to cover KC WRs and TEs in the redzone leading to TDs / Missed tackles and penalties / Vulnerable to big passing plays from P.Mahomes

Limitations: Could not determine exact concepts, personnel, coverage schemes, or defender names for many plays as they were not explicitly stated in the captions or clearly matched to DB; many captions had garbled names and unclear play details; some plays had no clear DB match; could not identify all specific yardage or if every play was a highlight without video.


## Week 5: LV 17 - NE 45 (game 401872986)
Video: Las Vegas Raiders vs. New England Patriots Game Highlights | 2026 NFL Season Week 5 — https://www.youtube.com/watch?v=fLKLrtqun84  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:22|LV|D.Thompkins|Kickoff return sailing into the Patriot bench|34|unknown|unknown|unknown|unknown|CONFLICT (yardage 34 vs DB)|
|00:44|NE|D.Maye|Incomplete deep right to R.Doubs with flag thrown for coverage in Raiders secondary|0|deep shot|unknown|unknown|E.Stokes|verified vs DB|
|01:15|NE|D.Douglas|Touchdown reception on deep pass|35|deep shot|unknown|unknown|unknown|verified vs DB|
|01:28|LV|B.Bowers|Terrific reception working on Marcus Jones into Patriot territory|24|unknown|unknown|unknown|M.Jones|verified vs DB|
|02:09|LV|B.Bowers|Touchdown reception in the end zone|13|unknown|unknown|unknown|unknown|verified vs DB|
|02:24|NE|R.Stevenson|Pull it up the middle to the first down|11|run|unknown|unknown|N.Dean|unverified (no DB match; caption-only)|
|03:06|NE|D.Douglas|First down reception|6|unknown|unknown|unknown|T.Johnson|unverified (no DB match; caption-only)|
|03:47|NE|H.Henry|Catch down to the 1 with pickup of seven|7|unknown|unknown|unknown|E.Stokes|unverified (no DB match; caption-only)|
|04:01|NE|R.Stevenson|Knifing corkscrew touchdown run with blocking ahead|5|run|unknown|unknown|unknown|verified vs DB|
|04:44|NE|R.Stevenson|Breaking tackles up to the 40-yard line|20|run|unknown|unknown|unknown|verified vs DB|
|08:03|NE|H.Henry|Catch and run to the 11-yard line|26|unknown|unknown|unknown|unknown|verified vs DB|
|08:15|NE|H.Henry|Caught touchdown|11|unknown|unknown|unknown|unknown|verified vs DB|
|09:03|NE|E.Raridon|Rookie ridden out of bounds|31|unknown|unknown|unknown|D.Porter|verified vs DB|
|09:55|NE|K.Williams|Touchdown reception|34|unknown|unknown|unknown|unknown|verified vs DB|
|10:31|LV|B.Bowers|Catch and run inside the 25|27|unknown|unknown|unknown|M.Jones|verified vs DB|
|12:28|NE|D.Maye|Three-yard touchdown run|3|run|unknown|unknown|unknown|verified vs DB|
|12:48|LV|B.Bowers|Completion then fumble recovered by Patriots|15|unknown|unknown|unknown|K.Vildor|verified vs DB|
|13:11|NE|K.Williams|Big throw completion working on Porter|49|deep shot|unknown|unknown|D.Porter|verified vs DB|
|13:29|NE|A.Borregales|28-yard field goal|28|unknown|unknown|unknown|unknown|verified vs DB|
|13:40|LV|A.Jeanty|Screen to Jeanty with block, catch and run to the 38|28|screen|unknown|unknown|unknown|verified vs DB|
|14:15|LV|D.Laube|Knifing driving touchdown run|2|run|unknown|unknown|unknown|verified vs DB|
|15:04|NE|D.Douglas|Wide open second touchdown reception|8|unknown|unknown|unknown|unknown|verified vs DB|
|16:13|NE|C.Kiner|Burst outside in a footrace|32|run|unknown|unknown|J.Chinn|verified vs DB|

Offense (model synthesis from this game's plays): Frequent use of tight end Brock Bowers on receptions gaining significant yardage / Screen passes and short middle/deep left passes to create big gains / Ability to score touchdowns on short yardage runs and passes when in the red zone

Defense weaknesses: Multiple defensive pass interference penalties on cornerbacks allowing big gains / Susceptible to big passing plays over the top and in the middle of the field / Struggled to contain running backs on outside runs and broken tackles

Limitations: Could not determine specific personnel formations or coverage schemes as they were not explicitly stated by commentators. Many plays in captions had mangled names and incomplete details making exact matching to DB difficult; only clear matches were used. Several described plays had no direct DB match. Yardage sometimes estimated from commentary without exact confirmation. Auto-generated captions had many errors and jumps in continuity.


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

Offense (model synthesis from this game's plays): Mayer supplied repeated completions and first downs, including a 28-yard gain. / Bowers produced consecutive fourth-quarter gains of 18 and 29 yards. / Tucker finished two passing touchdowns, including a diving 44-yard catch. / Washington supplied a run described as 13-14 yards and a later 18-yard middle run; Jeanty finished a one-yard touchdown with help from Rogers.

Defense weaknesses: Palmer became wide open for 37 yards while Allen extended the play. / Cook gained 23 and 26 yards on short receptions. / Defensive holding and pass interference extended Buffalo's possession after the interception. / Walker missed a tackle on Kincaid's 14-yard catch, and Buffalo's blocking supported Shakir's receiving touchdown and Cook's late rushing touchdown.

Limitations: Captions only; no frames were viewed and no external verification was performed. The supplied DB is a selected-play list, so NO DB MATCH does not establish that a play did not happen. DB-only plays without identifiable caption action were excluded, including Tucker's first-quarter 26-yard catch, most returns and the late 22-yard interference penalty. Matching DB yardage takes precedence over conflicting caption estimates. Null yards indicate an unspecified or conflicting gain; penalty and kick distances are identified in descriptions. Names without clear DB matches remain as captioned or unknown. Tacklers listed under defender_beaten identify the supplied matchup, not necessarily a missed tackle. No complete personnel formation was unambiguously stated for a specific play; the fragmented '11-B' discussion could not be reliably assigned. Zone and a slot blitz were explicitly described; other coverages, routes, blocking assignments and defensive responsibilities could not be determined.
