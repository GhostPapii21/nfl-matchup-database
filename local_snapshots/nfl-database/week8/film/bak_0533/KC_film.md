# KC — Phase 8 film notes (Weeks 1–6, 2026)

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

Offense (Codex synthesis from this game's plays): Walker produced sustained rushing gains, with left-side runs and cutbacks repeatedly highlighted; he scored on a 60-yard run and a 2-yard forward toss. / Mahomes escaped pressure for a 15-yard rushing touchdown. / Short completions generated major gains: Rice's 13-yard touchdown, Kelce's 59-yard reception and Johnson's 25-yard reception. / Johnson supplied additional rushing gains and broken tackles.

Defense weaknesses: Denver exploited zone coverage for Engram's touchdown by occupying the corner with Waddle's flat route. / Bryant caught three passes on Denver's touchdown drive, including a third-down conversion. / Sneed missed Harvey on a backfield reception, and Noel Williams missed Engram on a play-action first down.

Limitations: Captions only; no frames were reviewed. Many plays lack gains, identities, outcomes or complete context. NO DB MATCH means no clear match in the supplied selective DB excerpt, not that the play is absent from the full database. Replay descriptions are merged with their original plays. Fragmentary calls are retained with uncertainty. Names without a clear DB match remain as captioned or are identified as uncertain. Personnel and coverage details are included only when explicitly stated by commentators; DB shotgun labels were not used for personnel_formation. Named tacklers are labeled as tacklers and do not imply they were beaten in coverage. Interception yards are return yards; field-goal yards are kick distances. For the strip-sack, yards is the stated 9-yard sack loss, while the DB event's recovery-yardage field is 0. DB kickoff returns were not added without identifiable caption descriptions. Extra points are not separately identifiable in the captions. No exact run gaps, full coverage calls, route combinations or blocking assignments can be established beyond the supplied commentary and DB text.


## Week 2: IND 30 - KC 33 (game 401872945)
Video: Indianapolis Colts vs Kansas City Chiefs Game Highlights | 2026 NFL Season Week 2 — https://www.youtube.com/watch?v=baPzspvJv5Q  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 3: KC 24 - MIA 10 (game 401872952)
Video: Kansas City Chiefs vs. Miami Dolphins Game Highlights | NFL 2026 Season Week 3 — https://www.youtube.com/watch?v=eyM7QUODW6c  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 4: KC 30 - LV 27 (game 401872976)
Video: Kansas City Chiefs vs. Las Vegas Raiders Game Highlights | NFL 2026 Season Week 4 — https://www.youtube.com/watch?v=UH-pYLB0KQ4  | captions: yes

_No Codex film notes (no captions or run not completed)._


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

Offense (Codex synthesis from this game's plays): Walker scored twice on the ground; commentary credited supporting blocks from Kelce, Mahomes, Smith and Worthy on highlighted runs. / Kelce produced gains of 16, 24 and 11 yards, including completions against blitzes. / Gray’s sideline adjustment and Mahomes’ scrambles extended plays outside the initial pocket.

Defense weaknesses: Delane allowed Johnston’s 57-yard reception to the 1. / Allowed Hampton’s 15-yard catch and run and Gadsden’s 11-yard sideline reception on the same highlighted possession. / Allowed an early 17-yard McConkey gain and Herbert’s third-down run.

Limitations: Analysis uses only the supplied captions and DB excerpt; no video, browsing or commands were used. Caption fragments leave some receivers, play types, gains and results uncertain. Names on unmatched plays retain recognizable caption spellings rather than inferred DB corrections. The DB excerpt is selective, so NO DB MATCH does not mean a play did not occur. db_match contains the supplied quarter and clock identifier. For the Herbert interception, yards is the DB’s 48-yard interception return, not offensive gain; field-goal yards are kick distances. Named tacklers, interceptors and successful coverage defenders appear in defender_beaten with their actual roles and are not necessarily defenders who were beaten. Rush counts and blitz calls do not establish a coverage shell. Motion, backfield occupants and two-tight-end usage are recorded only where spoken; complete personnel packages and defensive coverages cannot be determined. Replays are consolidated with their original plays. The isolated 11:21 fourth-down fragment cannot be assigned a play result. Supplied DB kickoffs, the defensive pass-interference play and the Araiza punt return lack identifiable caption counterparts and are not added as caption highlights. The made extra point following Walker’s second touchdown is in the DB but is not separately identified in the captions.
