# KC — Phase 8 film notes (Weeks 1–6, 2026)
> Note: games 401872944, 401872945, 401872952, 401872962, 401872964, 401872970, 401872985, 401872989 were extracted by a Grok Bot agent (not Codex) from the same captions; mostly scoring/20+ plays logged.
> Note: games 401872976 were extracted by Grok via the xAI API (grok-4.20-0309-non-reasoning, same prompt/schema as Codex, cleaned captions); sidecar provenance in film/grok_meta/. All other games with notes: Codex.

Method: NFL YouTube channel full-game highlight videos were located by search and their auto-captions (broadcast commentary) downloaded via yt-dlp. Codex (codex-cli 0.163.0) extracted plays from the captions. **No video frames were viewed by any agent.** Each play was checked against the repo DB play-by-play: `verified vs DB` means the cited DB play exists and the yardage matches. Personnel, formation and coverage appear only when commentators stated them; everything else is `unknown`.


## Week 1: DEN 10 - KC 31 (game 401872931)
Video: Denver Broncos vs Kansas City Chiefs Game Highlights | 2026 NFL Season Week 1 — https://www.youtube.com/watch?v=RYh8_uw45Fw  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:30|DEN|RJ Harvey|Takes a knee on the opening kickoff.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:10|DEN|Bo Nix|Steps up and is sacked; commentary credits Noel Williams.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:38|DEN|Bo Nix|Replay describes Nix moving off a doubled Waddle and throwing an interception to M. Delane on a deep middle pass intended for Courtland Sutton. Delane returns it 5 yards.|5|deep middle pass|unknown|Underneath coverage with help over the top; Waddle doubled|unknown|verified vs DB|
|02:04|KC|Kenneth Walker|Handoff with Tonga in the backfield gains a first down. Fragmented commentary may span multiple carries.|None|handoff|Tonga in the backfield|unknown|unknown|unverified (no DB match; caption-only)|
|02:23|KC|Xavier Worthy|Makes a spinning catch on a quick throw; Rylie Moss is mentioned immediately afterward.|None|quick pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:32|KC|Kenneth Walker|Runs for 12 yards and a first down.|12|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:45|KC|Patrick Mahomes|Escapes pressure, breaks a tackle and scrambles up the middle for a touchdown.|15|scramble up the middle|unknown|unknown|unknown|verified vs DB|
|03:27|DEN|Pat Bryant|Catches a first-down bullet from Nix.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:37|DEN|Pat Bryant|Converts third-and-five with a reception against a four-man rush.|None|unknown|unknown|Four-man rush; coverage unknown|unknown|unverified (no DB match; caption-only)|
|03:48|DEN|Pat Bryant|Motions before making his third catch of the possession.|None|unknown|Bryant in motion|unknown|unknown|unverified (no DB match; caption-only)|
|03:58|DEN|Evan Engram|Catches a 19-yard touchdown to the left. Waddle releases from the backfield to the flat, occupying the corner and opening space behind him.|19|flat route creating space for a deeper receiver|Waddle in the backfield|Zone|unknown|verified vs DB|
|04:26|KC|Emmett Johnson|Takes a handoff for a pickup; exact gain is not stated.|None|handoff|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:39|KC|Patrick Mahomes|Third-and-seven throw toward Xavier Worthy is nearly intercepted by McMillan.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:52|DEN|Evan Engram|Catches a pass behind him as Nix rolls left off play-action; commentary questions the favorable spot.|None|play-action rollout left|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:08|DEN|RJ Harvey|Runs for 6 yards and a first down; Nick Bolton makes the tackle.|6|unknown|unknown|unknown|Nick Bolton (tackler)|unverified (no DB match; caption-only)|
|05:21|DEN|RJ Harvey|Catches a screen with blockers ahead but is stopped short, bringing up fourth down. Tranquill is involved in the stop.|None|screen|unknown|unknown|Tranquill (stop participant)|unverified (no DB match; caption-only)|
|05:33|KC|Kenneth Walker|Starts left, bends the run back and gains 9 yards. DJ Jones and Uwazurike miss tackles.|9|left run with cutback|unknown|unknown|DJ Jones; Uwazurike|unverified (no DB match; caption-only)|
|05:46|KC|Patrick Mahomes|Pass intended for Cyrus Allen is tipped and falls short, bringing up fourth down.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:04|DEN|Troy Franklin|Takes a handoff for 5 yards on the edge; Bolton brings him down.|5|edge run|unknown|unknown|Bolton (tackler)|unverified (no DB match; caption-only)|
|06:15|DEN|RJ Harvey|Makes a backfield reception, stays on his feet through a missed tackle by Sneed and gains 4 yards.|4|pass to back out of backfield|unknown|unknown|Sneed|unverified (no DB match; caption-only)|
|06:28|DEN|Bo Nix|Moves right looking for a receiver on third-and-a-long-one; sequence ends with fourth down. Exact result is unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:42|KC|Kenneth Walker|Catches a pass after a bad snap and dives for a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:53|KC|Kenneth Walker|Breaks tackles on a left-end run for 28 yards to the Denver 41.|28|left end run|unknown|unknown|B. Jones (DB tackler)|verified vs DB|
|07:12|KC|Noah Gray|Catches a pass over the middle and is stopped at the marker by McMillan.|None|pass over the middle|unknown|unknown|McMillan (tackler)|unverified (no DB match; caption-only)|
|07:24|KC|Rashee Rice|Turns a short right reception into a 13-yard touchdown. Moss misses the tackle; commentary also describes Jonah Ellis failing to wrap up.|13|short right pass|unknown|unknown|Rylie Moss; Jonah Ellis|verified vs DB|
|07:42|DEN|Bo Nix|Pulls the ball down and is sacked by rookie R. Mason Thomas.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:00|DEN|Pat Bryant|Makes a strong catch; subsequent commentary says Denver hurries.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:04|DEN|Bo Nix|Backpedals against extra rushers and throws incomplete, bringing up fourth down. A defender's name is unclear in the captions.|0|unknown|unknown|Extra rushers; coverage unknown|unknown|unverified (no DB match; caption-only)|
|08:18|KC|Rashee Rice|Quick reception is stopped a yard short of the first down by Rylie Moss.|None|quick pass|unknown|unknown|Rylie Moss (tackler)|unverified (no DB match; caption-only)|
|08:26|KC|Kenneth Walker|Converts fourth-and-one and continues for a 60-yard touchdown around left end.|60|left end run|Tonga aligned left of Walker|unknown|unknown|verified vs DB|
|08:56|DEN|JK Dobbins|Finds room for 3 yards on second-and-six; Karlaftis makes the tackle.|3|unknown|Dobbins stays in; Harvey checks out|unknown|Karlaftis (tackler)|unverified (no DB match; caption-only)|
|09:12|DEN|Waddle|Cannot hold onto a third-down pass. Commentary discusses Spagnuolo disguising pressure.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:22|KC|Patrick Mahomes|After a run fake, throws deep middle toward Worthy and is intercepted by Brandon Jones, who returns it 24 yards to the KC 5. Commentary says Worthy was unaware the ball was coming.|24|play-action deep middle pass|unknown|Middle safety described; full coverage unknown|unknown|verified vs DB|
|09:55|DEN|Bo Nix|Completes a pass down to the 10 following mention of a penalty; receiver and gain are unstated.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:02|DEN|Bo Nix|Moves right and back left, then loses the ball while preparing to throw. Sneed touches it while out of bounds; officials rule a fumble retained by Denver at that spot.|None|unknown|Dobbins in the backfield|unknown|unknown|unverified (no DB match; caption-only)|
|10:54|DEN|Bo Nix|Handles a bad snap on third-and-goal from outside the 16 and throws unsuccessfully toward Waddle, who cannot separate from Christian Fulton.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:09|DEN|Wil Lutz|Makes a 31-yard field goal after Denver fails to convert first-and-goal from the 5 into a touchdown.|31|field goal|unknown|unknown|unknown|verified vs DB|
|11:24|KC|Travis Kelce|Catches a short left pass against a blitz and gains 59 yards to the Denver 4. Replay commentary credits his patience selling the route against one-on-one coverage.|59|short left pass|unknown|Blitz with one-on-one coverage on Kelce|J. Barron (DB tackler; initial coverage assignment unknown)|verified vs DB|
|11:59|KC|Patrick Mahomes|Is tripped up and sacked on third-and-goal; commentary says Kelce was open in the end zone.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:07|KC|Harrison Butker|Makes a 28-yard field goal.|28|field goal|unknown|unknown|unknown|verified vs DB|
|12:16|DEN|Evan Engram|Catches a play-action pass, breaks Noel Williams' tackle and gains a first down.|None|play-action|unknown|unknown|Noel Williams|unverified (no DB match; caption-only)|
|12:26|DEN|JK Dobbins|Is identified as the ball carrier or target, but the caption cuts away before establishing the play's action or result.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:32|DEN|Bo Nix|Is strip-sacked by Felix Anudike-Uzomah; Chris Jones recovers. Commentary says Kansas City showed blitz and backed out, while Denver linemen moved downfield on a dropback pass.|-9|dropback pass|unknown|Showed blitz, then backed out; full coverage unknown|unknown|verified vs DB|
|13:11|KC|Xavier Worthy|Catches a pass in stride and is tackled by McMillan, bringing up third down.|None|unknown|unknown|unknown|McMillan (tackler)|unverified (no DB match; caption-only)|
|13:19|KC|Emmett Johnson|Converts third-and-five with a short left reception, breaks a tackle and gains 25 yards to the Denver 4. A subsequent unnecessary-roughness penalty moves the ball 2 yards closer.|25|short left pass|unknown|Four-man rush|J. Barron (DB tackler; missed tackler unidentified)|verified vs DB|
|13:39|KC|Kenneth Walker|Scores on a 2-yard forward toss, officially a touchdown pass from Mahomes. Commentary states Fields is in the game without specifying his role.|2|short forward toss|Fields in the game; alignment unknown|unknown|unknown|verified vs DB|
|14:10|DEN|Courtland Sutton|Makes his second catch and is tackled immediately by Kristian Fulton.|None|unknown|unknown|unknown|Kristian Fulton (tackler)|unverified (no DB match; caption-only)|
|14:16|DEN|Bo Nix|Is flushed on third-and-five and throws into the ground while chased by Bolton and Chris Jones.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:28|KC|Kenneth Walker|Bends a run back on second-and-nine and adds to his rushing total.|None|cutback run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:56|KC|Emmett Johnson|Breaks tackles on a run and is eventually brought down downfield. Malcolm Roach is named in a fragmented discussion of the tackle and a missed tackle.|None|unknown|unknown|unknown|Malcolm Roach (exact role unclear)|unverified (no DB match; caption-only)|
|15:14|KC|Patrick Mahomes|Is sacked by Zach Allen, Denver's second sack of the night.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:21|DEN|Harvey (caption rendered as 'Herbie')|A brief call identifies Harvey, but does not establish the action or outcome.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:32|DEN|Evan Engram|Makes a catch for a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:40|DEN|Bo Nix|Fails to secure the snap and the ball hits the ground; recovery is not stated.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:49|DEN|RJ Harvey|Catches a short pass that results in Kansas City's ninth consecutive third-down stop.|None|short pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|16:09|DEN|Bo Nix|Escapes pressure on fourth-and-eight and throws across his body toward Troy Franklin. Noel Williams breaks up the pass.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|16:17|KC|Emmett Johnson|Takes a third-down carry; commentary praises his effort and mentions Khalil Benson, but does not clearly state the gain or conversion.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|

Offense (model synthesis from this game's plays): Walker produced sustained rushing gains, with left-side runs and cutbacks repeatedly highlighted; he scored on a 60-yard run and a 2-yard forward toss. / Mahomes escaped pressure for a 15-yard rushing touchdown. / Short completions generated major gains: Rice's 13-yard touchdown, Kelce's 59-yard reception and Johnson's 25-yard reception. / Johnson supplied additional rushing gains and broken tackles.

Defense weaknesses: Denver exploited zone coverage for Engram's touchdown by occupying the corner with Waddle's flat route. / Bryant caught three passes on Denver's touchdown drive, including a third-down conversion. / Sneed missed Harvey on a backfield reception, and Noel Williams missed Engram on a play-action first down.

Limitations: Captions only; no frames were reviewed. Many plays lack gains, identities, outcomes or complete context. NO DB MATCH means no clear match in the supplied selective DB excerpt, not that the play is absent from the full database. Replay descriptions are merged with their original plays. Fragmentary calls are retained with uncertainty. Names without a clear DB match remain as captioned or are identified as uncertain. Personnel and coverage details are included only when explicitly stated by commentators; DB shotgun labels were not used for personnel_formation. Named tacklers are labeled as tacklers and do not imply they were beaten in coverage. Interception yards are return yards; field-goal yards are kick distances. For the strip-sack, yards is the stated 9-yard sack loss, while the DB event's recovery-yardage field is 0. DB kickoff returns were not added without identifiable caption descriptions. Extra points are not separately identifiable in the captions. No exact run gaps, full coverage calls, route combinations or blocking assignments can be established beyond the supplied commentary and DB text.


## Week 2: IND 30 - KC 33 (game 401872945)
Video: Indianapolis Colts vs Kansas City Chiefs Game Highlights | 2026 NFL Season Week 2 — https://www.youtube.com/watch?v=baPzspvJv5Q  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|01:36|IND|Tyler Warren|Warren sneaks through the back of the end zone; motion shifted coverage, move outside-in vs Sneed|1|motion; RZ route|unknown|unknown|L'Jarius Sneed|verified vs DB|
|02:28|KC|Harrison Butker|Field goal rockets through|None|field goal|unknown|unknown|unknown|verified vs DB|
|02:57|IND|Daniel Jones|Slant for Allen, Fulton rips ball out, INT|0|slant|unknown|unknown|K.Fulton (INT)|verified vs DB|
|03:24|KC|Travis Kelce|From the 13, Kelce touchdown; commentary: given too much space|13|short right|unknown|unknown|unknown|verified vs DB|
|04:53|KC|Rashee Rice|Rashee Rice inside the 40|30|short right|unknown|unknown|A.Gardner|verified vs DB|
|05:37|IND|Laquon Treadwell|26-yard pass interference penalty|None|deep left|unknown|unknown|K.Fulton (DPI)|verified vs DB|
|05:57|IND|Spencer Shrader|49-yard field goal|None|field goal|unknown|unknown|unknown|verified vs DB|
|07:19|KC|Xavier Worthy|Touchdown pass, number two on the night, to Worthy|1|short right|unknown|unknown|unknown|verified vs DB|
|08:24|IND|Jonathan Taylor|Taylor runs right for the touchdown|24|run right end|unknown|unknown|unknown|verified vs DB|
|09:13|KC|Tyquan Thornton|Big hit on Thornton who hangs on; big play to the 1|45|deep right|unknown|unknown|J.Carlies|verified vs DB|
|10:20|KC|Jaylen Royals|Rolls, touchdown|1|rollout|unknown|unknown|unknown|verified vs DB|
|12:31|KC|Harrison Butker|28-yard FG|None|field goal|unknown|unknown|unknown|verified vs DB|
|14:14|IND|Jonathan Taylor|Taylor, end zone, touchdown|5|run|unknown|unknown|unknown|verified vs DB|
|17:29|KC|Tyquan Thornton|OT: man-to-man coverage; Mahomes downfield for Thornton, hangs on, Wohler hit him|30|deep right|unknown|man-to-man|H.Wohler|verified vs DB|
|18:21|KC|Harrison Butker|31-yard FG for the lead|None|field goal|unknown|unknown|unknown|verified vs DB|
|18:32|IND|Laquon Treadwell|Throwing deep downfield, down at the 16/17, ruled down by contact on review|48|deep shot|unknown|unknown|unknown|verified vs DB|
|20:52|IND|Spencer Shrader|FG to tie at 30|None|field goal|unknown|unknown|unknown|verified vs DB|
|21:20|KC|Kenneth Walker|Walker open field inside the 30 to the 25|22|pass short left to RB|unknown|unknown|unknown|verified vs DB|
|21:39|KC|Harrison Butker|40-yard FG for the win|None|field goal|unknown|unknown|unknown|verified vs DB|

Offense (model synthesis from this game's plays): Thornton as the deep shot WR (45, 30) / Kelce RZ TD with space / Walker receiving in space for game-winner setup (22) / Rice intermediate (30, 31)

Defense weaknesses: Taylor outside runs right (24 TD) / Deep shots to Treadwell (48) and DPI on Fulton (26, 23) / TE Warren TD via motion vs Sneed

Limitations: Captions only; middle section partly skimmed by keyword. Coverage stated only once (OT man-to-man). Commentary says KC blitzing was a non-factor.


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

Offense (model synthesis from this game's plays): Kelce explosive down the seam (48) and RZ TD / Walker scores rushing and receiving; 22-yd burst / Mahomes downfield to Rice late (34)

Defense weaknesses: Play-action explosives allowed: Bell 44, Dulcich 42 / Washington 30-yd catch / Goal-line run TD allowed to Gordon

Limitations: Captions only; no frames; captions are partly mangled and out of order. No coverage shells stated (only blitz counts: Chiefs bring 5 / 4). Noah Gray caption yardage 23 vs DB 24 kept as stated.


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

Offense (model synthesis from this game's plays): Explosive big plays through deep passes to T.Thornton and X.Worthy / Effective use of RBs like K.Walker for long runs and goal line scores / Quick adjustments and play calling leading to multiple first downs and TDs / Utilizing TEs like Noah Gray and Kelce as safety valves

Defense weaknesses: Susceptible to big runs by LV RBs like A.Jeanty / Penalties leading to automatic first downs and nullified kicks / Allowing conversions on third and long / Vulnerable to LV TEs especially in one-on-one matchups

Limitations: Could not determine exact concepts, personnel, coverage schemes, or defender names for many plays as they were not explicitly stated in the captions or clearly matched to DB; many captions had garbled names and unclear play details; some plays had no clear DB match; could not identify all specific yardage or if every play was a highlight without video.


## Week 6: LAC 6 - KC 22 (game 401873006)
Video: Los Angeles Chargers vs Kansas City Chiefs Game Highlights | 2026 NFL Season Week 6 — https://www.youtube.com/watch?v=B5OVcasfeTU  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:33|KC|Worthy|Catches a downfield pass on first-and-5.|None|downfield pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:39|KC|Walker|Mack prevents a completion to Walker.|0|unknown|unknown|unknown|Mack (prevented completion)|unverified (no DB match; caption-only)|
|00:45|KC|Gray|Catches a pass over the middle for 16 yards, short of the first down.|16|pass over middle|unknown|unknown|Jefferson (tackler)|unverified (no DB match; caption-only)|
|00:51|KC|H.Butker|Makes a 44-yard field goal for a 3-0 lead.|44|field goal|unknown|unknown|unknown|verified vs DB|
|01:04|LAC|Herbert|Third-and-11 pass falls incomplete against a blitz.|0|unknown|unknown|blitz|unknown|unverified (no DB match; caption-only)|
|01:19|KC|Worthy|Gains 17 yards and a first down; the captions do not establish the play type.|17|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:29|KC|Royals|Bobbles and secures a play-action pass with Jefferson nearby.|None|play-action|unknown|unknown|Jefferson|unverified (no DB match; caption-only)|
|01:42|KC|K.Walker|Runs up the middle for a 33-yard touchdown, outrunning Still. Replay commentary identifies a lead block but mangles the blocker’s name.|33|run up middle; lead block|unknown|unknown|Still|verified vs DB|
|02:46|KC|H.Butker|Misses the extra point wide left, leaving the score 9-0.|None|extra point|unknown|unknown|unknown|verified vs DB|
|02:58|LAC|McConkey|Gains 17 yards to the Kansas City 48 with a downfield blocker mentioned.|17|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:10|LAC|Herbert|Runs for a first down on third-and-3; a late flag is described as against Kansas City.|None|quarterback scramble|McConkey in motion|unknown|unknown|unverified (no DB match; caption-only)|
|03:23|LAC|Herbert; unidentified tight end|Completes a pressured third-down pass to a tight end at the 5, short of the first down. Receiver name and gain are unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:35|LAC|C.Dicker|Makes a 23-yard field goal, cutting the deficit to 9-3.|23|field goal|unknown|unknown|unknown|verified vs DB|
|03:42|KC|Emmett Johnson|Takes a carry and is stopped by Jefferson.|None|unknown|unknown|unknown|Jefferson (tackler)|unverified (no DB match; caption-only)|
|03:55|KC|Allen|Gains four on an outside play on third-and-6; commentary says he stepped out, leaving fourth down.|4|outside play; play type unclear|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:14|LAC|Omarion Hampton|Takes his first carry of the game and is brought down by Karloftis.|None|unknown|unknown|unknown|Karloftis (tackler)|unverified (no DB match; caption-only)|
|04:27|LAC|Vidal|Catches a downfield pass on third-and-11 with Mason Thomas rushing.|None|downfield pass to running back|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:45|LAC|J.Herbert|Under A.Gillotte’s pressure, throws a pass intended for K.Lambert-Smith that J.Cochrane intercepts and returns 48 yards. Illegal formation is declined.|48|short right pass; commentary describes intended corner route|unknown|unknown|J.Cochrane (interceptor); A.Gillotte (pressure)|verified vs DB|
|05:22|KC|unknown|An unidentified ball carrier is upended by Mack on second-and-3.|None|unknown|unknown|unknown|Mack (tackler)|unverified (no DB match; caption-only)|
|05:31|KC|P.Mahomes|Third-and-goal pass intended for A.Armstrong is intercepted by C.Hart in the end zone for a touchback.|0|short right pass; commentary discusses corner-flat combination as an alternative|unknown|unknown|C.Hart (interceptor); T.Tart (DB-listed pressure)|verified vs DB|
|05:59|LAC|Herbert; unidentified receiver|Completes a seven-yard pass on third-and-5 to the Chargers’ 32. Receiver name is garbled.|7|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:09|LAC|Herbert|With the pocket collapsing, gains seven on third-and-9 and is stopped short by Bolton; play type is unclear.|7|unknown|unknown|unknown|Bolton (tackler)|unverified (no DB match; caption-only)|
|06:27|KC|Mahomes|Runs into the secondary and is tackled; defender’s name is garbled.|None|quarterback scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:37|KC|Kelce|Makes his first reception, a 16-yard gain near midfield, with Henley making the stop.|16|unknown|unknown|unknown|Henley (tackler)|unverified (no DB match; caption-only)|
|06:51|KC|T.Kelce|Turns a short middle completion against a blitz into a 24-yard gain to the Chargers’ 21.|24|short middle pass; catch and run|unknown|blitz|K.Mack (DB tackler)|verified vs DB|
|07:03|KC|Andrew Armstrong|Catches a pass at the 8 after the play starts at the 21.|None|unknown|Worthy in motion; Walker at running back|unknown|unknown|unverified (no DB match; caption-only)|
|07:16|KC|K.Walker|Runs left tackle for a two-yard touchdown. Commentary credits blocks by Kelce and Mahomes.|2|left tackle run|Worthy in motion; Kelce on field|unknown|unknown|verified vs DB|
|07:40|LAC|unknown|Brief return-like sequence mentions a Davis block and the runner colliding with his own blocker; play identity is unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:53|LAC|Herbert|Throws high and incomplete toward KeAndre Lambert-Smith on third down while under pressure.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:09|KC|Emmett Johnson|Runs behind blocks credited to Benson, Humphrey and Trey Smith before being tackled from behind.|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:22|KC|H.Butker|Makes a 50-yard field goal with two seconds left in the half for a 19-3 lead.|50|field goal|unknown|unknown|unknown|verified vs DB|
|08:37|LAC|KeAndre Lambert-Smith|Catches a downfield play-action pass near the 43.|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:58|LAC|Q.Johnston|Makes a 57-yard catch on a deep left pass to the Kansas City 1, working against rookie M.Delane.|57|deep left shot|unknown|unknown|M.Delane|verified vs DB|
|09:05|LAC|Lambert-Smith|An underneath third-and-goal pass is incomplete with Williams credited for coverage.|0|underneath pass|unknown|unknown|Williams (successful coverage)|unverified (no DB match; caption-only)|
|09:17|LAC|C.Dicker|Makes a 30-yard field goal, bringing the score to 19-6.|30|field goal|unknown|unknown|unknown|verified vs DB|
|09:32|KC|Walker|Runs for 11 yards on first down and is ushered out by Still.|11|run|unknown|unknown|Still (tackler)|unverified (no DB match; caption-only)|
|09:42|KC|N.Gray|Catches a short right pass and gains 31 yards to the Chargers’ 21 as Mahomes escapes pressure. Gray works up the sideline and attempts a hurdle.|31|scramble adjustment up sideline; short right pass|unknown|unknown|E.Molden (DB tackler)|verified vs DB|
|10:00|KC|unknown|A brief play fragment mentions a receiver, a block and a tackle; the ball carrier and gain are unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:06|KC|Walker|Runs left behind a Smith block for six yards and dives to roughly half a yard short of the goal line.|6|left run|unknown|unknown|Phillips (tackler)|unverified (no DB match; caption-only)|
|10:17|KC|Walker|Stopped for no gain on fourth-and-goal, with Tony Jefferson credited for the goal-line hit.|0|goal-line run|unknown|unknown|Tony Jefferson (stop)|unverified (no DB match; caption-only)|
|10:29|LAC|Herbert|Is hit inside near his own goal line; commentary describes a loss of approximately half a yard.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:40|LAC|Omarion Hampton|Runs on third-and-10 deep in Chargers territory and gains approximately half a yard.|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:51|LAC|JK Scott|Punts from deep in Chargers territory. Remigio fields the bouncing ball and nearly loses it; commentary says Kansas City retains possession and mentions a Bruningstool penalty.|None|punt|unknown|no punt rush|unknown|unverified (no DB match; caption-only)|
|11:27|LAC|Herbert|Sacked by Gillotte on second-and-8; described as Kansas City’s first sack.|None|unknown|unknown|unknown|Gillotte (sack)|unverified (no DB match; caption-only)|
|11:40|LAC|Gadsden|Receives an outside third-and-13 throw; Kansas City is credited with reading the play well. Exact gain is unclear.|None|outside pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:50|KC|Worthy|Makes an outside reception on second-and-8; commentary subsequently gives a six-yard gain.|6|outside pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:00|KC|Mahomes|Runs through a middle gap against a four-man rush on third-and-3 and is stopped two yards short.|None|quarterback scramble up middle|unknown|four-man rush|Phillips; Molden (involved in stop)|unverified (no DB match; caption-only)|
|12:16|LAC|Hampton|Turns an underneath completion into a 15-yard first down to the Chiefs’ 47; Wallace and Tonga make the stop.|15|underneath pass; catch and run|unknown|unknown|Wallace; Tonga (tacklers)|unverified (no DB match; caption-only)|
|12:27|LAC|Gadsden|Makes an 11-yard sideline catch in front of Bolton as Herbert is chased by Jones. Replay describes the receiver stopping and coming back.|11|sideline comeback adjustment|Keaton Mitchell at running back|four-man rush|Bolton|unverified (no DB match; caption-only)|
|12:49|LAC|Lambert-Smith|Catches a fourth-and-6 pass and lunges but is stopped short by Williams.|None|unknown|unknown|blitz|Williams (stop)|unverified (no DB match; caption-only)|
|13:02|KC|Royals|Catches a downfield pass after Mahomes is chased; Still helps force him out.|None|downfield pass|Walker at running back|unknown|Still (tackler)|unverified (no DB match; caption-only)|
|13:15|KC|Mahomes|Scrambles with Tart chasing and receives a downfield block from Royals before going out of bounds.|None|quarterback scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:27|KC|Mahomes|Throws short and incomplete toward Royals on third-and-1, with Marleau Wax credited for coverage.|0|short pass|two tight ends|unknown|Marleau Wax (successful coverage)|unverified (no DB match; caption-only)|
|13:36|KC|H.Butker|Misses a 52-yard field goal wide right.|52|field goal|unknown|unknown|unknown|verified vs DB|
|13:55|LAC|Charlie Kolar|Catches a pass over the middle on second-and-10 and is upended.|None|pass over middle|Keaton Mitchell at running back|unknown|unknown|unverified (no DB match; caption-only)|
|14:07|LAC|K.Lambert-Smith|Catches a one-yard short right pass and fumbles on L.Sneed’s tackle; D.Tranquill recovers for Kansas City.|1|short right pass|unknown|unknown|L.Sneed (forced fumble); D.Tranquill (recovery)|verified vs DB|
|14:31|KC|C.Allen|Catches a deep middle pass for 23 yards to the Chargers’ 49.|23|deep middle pass|unknown|unknown|G.Smith (DB tackler)|verified vs DB|
|14:41|KC|Kelce|Makes an 11-yard catch against pressure.|11|unknown|Johnson at running back|blitz|unknown|unverified (no DB match; caption-only)|
|14:52|KC|Kenneth Walker|Runs into the secondary behind a Worthy block for a first down to the 12; Smith makes the hit.|None|run|unknown|unknown|Smith (tackler)|unverified (no DB match; caption-only)|
|15:05|KC|Mahomes|Third-and-10 end-zone pass appears incomplete; commentary credits coverage, but the defender’s name is garbled.|0|end-zone pass|Johnson at running back|unknown|unknown|unverified (no DB match; caption-only)|
|15:14|KC|H.Butker|Makes a 30-yard field goal for a 22-6 lead; the announcer initially miscalls the result, then corrects it.|30|field goal|unknown|unknown|unknown|verified vs DB|
|15:26|LAC|Herbert; unidentified receiver|Completes a pass under pressure; the receiver goes down in the middle. Felix Anudike-Uzomah is described as slow getting up.|None|unknown|Vidal at running back|unknown|unknown|unverified (no DB match; caption-only)|
|15:39|LAC|Herbert|Sacked against a six-man rush; the tackler’s identity is unclear.|None|unknown|unknown|six-man rush|unknown|unverified (no DB match; caption-only)|
|15:50|LAC|Kolar|Catches a six-yard pass on second-and-10 and is tackled low by Sneed.|6|unknown|unknown|unknown|Sneed (tackler)|unverified (no DB match; caption-only)|
|16:03|LAC|Herbert|Fourth-and-4 pass hits the ground incomplete, giving Kansas City possession.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|

Offense (model synthesis from this game's plays): Walker scored twice on the ground; commentary credited supporting blocks from Kelce, Mahomes, Smith and Worthy on highlighted runs. / Kelce produced gains of 16, 24 and 11 yards, including completions against blitzes. / Gray’s sideline adjustment and Mahomes’ scrambles extended plays outside the initial pocket.

Defense weaknesses: Delane allowed Johnston’s 57-yard reception to the 1. / Allowed Hampton’s 15-yard catch and run and Gadsden’s 11-yard sideline reception on the same highlighted possession. / Allowed an early 17-yard McConkey gain and Herbert’s third-down run.

Limitations: Analysis uses only the supplied captions and DB excerpt; no video, browsing or commands were used. Caption fragments leave some receivers, play types, gains and results uncertain. Names on unmatched plays retain recognizable caption spellings rather than inferred DB corrections. The DB excerpt is selective, so NO DB MATCH does not mean a play did not occur. db_match contains the supplied quarter and clock identifier. For the Herbert interception, yards is the DB’s 48-yard interception return, not offensive gain; field-goal yards are kick distances. Named tacklers, interceptors and successful coverage defenders appear in defender_beaten with their actual roles and are not necessarily defenders who were beaten. Rush counts and blitz calls do not establish a coverage shell. Motion, backfield occupants and two-tight-end usage are recorded only where spoken; complete personnel packages and defensive coverages cannot be determined. Replays are consolidated with their original plays. The isolated 11:21 fourth-down fragment cannot be assigned a play result. Supplied DB kickoffs, the defensive pass-interference play and the Araiza punt return lack identifiable caption counterparts and are not added as caption highlights. The made extra point following Walker’s second touchdown is in the DB but is not separately identified in the captions.
