# JAX — Phase 8 film notes (Weeks 1–6, 2026)

Method: NFL YouTube channel full-game highlight videos were located by search and their auto-captions (broadcast commentary) downloaded via yt-dlp. Codex (codex-cli 0.163.0) extracted plays from the captions. **No video frames were viewed by any agent.** Each play was checked against the repo DB play-by-play: `verified vs DB` means the cited DB play exists and the yardage matches. Personnel, formation and coverage appear only when commentators stated them; everything else is `unknown`.


## Week 1: CLE 10 - JAX 34 (game 401872922)
Video: Cleveland Browns vs Jacksonville Jaguars Game Highlights | NFL 2026 Week 1 — https://www.youtube.com/watch?v=T5D7UViL1L0  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:46|CLE|Dylan Sampson|Returns the opening kickoff to the Cleveland 40.|37|kickoff return|unknown|unknown|J.Cameron; M.Brown (DB tacklers)|verified vs DB|
|01:05|CLE|Whitehart|Catches an underneath pass; Miller makes the tackle. Receiver name is caption-rendered.|None|underneath pass|unknown|unknown|Miller (tackler)|unverified (no DB match; caption-only)|
|01:16|CLE|KC Concepcion|Catches an underneath pass for a first down at the 33.|None|underneath pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:29|CLE|Deshaun Watson|Pass intended for Jerry Jeudy is intercepted by F.Oluokun, who returns it 22 yards. Captions give a conflicting interception location.|22|short left pass|unknown|unknown|F.Oluokun (interceptor); E.Jenkins (return tackler)|verified vs DB|
|01:51|JAX|B hayshul Tuten|Takes a handoff, slips a tackle and reaches midfield, close to a first down.|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:03|JAX|Parker Washington|Catches a pass off a play fake for a first down at the 33.|None|play-action|unknown|unknown|Tyson Campbell (tackler)|unverified (no DB match; caption-only)|
|02:14|JAX|Parker Washington|Catches a 30-yard touchdown from Trevor Lawrence. Commentary attributes his separation to defensive miscommunication.|30|deep right pass|unknown|unknown|unknown|verified vs DB|
|02:52|CLE|Judkins|Bounces off a defender and runs to the 21; gain announcement is cut off.|None|run|Whitehearth comes in motion (caption-rendered name); personnel unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:57|CLE|Deshaun Watson|Throws an almost-intercepted pass as the pocket collapses and Allen arrives.|None|unknown|unknown|unknown|Allen (pressure)|unverified (no DB match; caption-only)|
|03:11|JAX|Brian Thomas|Makes a toe-tap reception near the sideline.|None|sideline pass|unknown|four-man defensive front; coverage unknown|unknown|unverified (no DB match; caption-only)|
|03:20|JAX|Brian Thomas|Catches Lawrence's pass off a play fake, then fumbles; Jacksonville recovers.|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:36|JAX|Parker Washington|Makes a reception on second-and-20. Commentary says 23 yards; DB records 22.|22|deep left pass|unknown|unknown|Ronnie Hickman (coverage; DB tackler)|verified vs DB|
|03:51|JAX|Brian Thomas|Catches a tight-window throw over the middle inside the 10.|None|play-action; middle pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:02|JAX|J.Cameron|Catches a four-yard touchdown toward the back of the end zone.|4|short middle pass|Meyers goes in motion; personnel unknown|unknown|unknown|verified vs DB|
|04:26|CLE|unknown|Unidentified ball carrier is shoved out of bounds by Walker for a loss.|None|unknown|unknown|four-man defensive front; coverage unknown|Walker (tackler)|unverified (no DB match; caption-only)|
|04:40|CLE|Deshaun Watson|Steps up under pressure and loses the football. Commentary identifies Josh Hines-Allen's pressure but does not establish recovery.|None|unknown|Sanders in the backfield; personnel unknown|unknown|Josh Hines-Allen (pressure)|unverified (no DB match; caption-only)|
|05:19|JAX|unknown|Fragmentary call describes a Jacksonville gain close to a first down; ball carrier and play type are unavailable.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:24|JAX|Jakobi Meyers|Gets the ball with blockers and powers toward midfield for a first down.|None|unknown|unknown|unknown|Tyson Campbell (tackler)|unverified (no DB match; caption-only)|
|05:40|JAX|Bhayshul Tuten|Takes a handoff and sidesteps left for a first down at the 38.|None|run left|multiple tight ends, including Morris; exact personnel unknown|unknown|Ronnie Hickman (tackler)|unverified (no DB match; caption-only)|
|05:56|JAX|Travis Hunter|Advances inside the 35 to approximately the 29. Captions do not establish how he received the ball.|None|unknown|unknown|unknown|Mason Graham (tackler)|unverified (no DB match; caption-only)|
|06:23|JAX|Cam Little|Makes a 47-yard field goal for a 17-0 lead.|47|field goal|unknown|unknown|unknown|verified vs DB|
|06:35|CLE|KC Concepcion|Catches a five-yard pass and fumbles. V.Miller forces the fumble; J.Hines-Allen recovers.|5|screen left|unknown|unknown|V.Miller (tackler and forced fumble); T.Walker (QB hit)|verified vs DB|
|07:18|JAX|Bhayshul Tuten|Runs inside the 35, shedding tackles and apparently gaining a first down.|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:30|JAX|Parker Washington|Makes a 15-yard sideline reception on third-and-six, keeping his feet inbounds in front of Campbell.|15|sideline pass|unknown|unknown|Tyson Campbell (coverage)|unverified (no DB match; caption-only)|
|07:41|JAX|Brenton Strange|Catches a 14-yard touchdown after Lawrence hitches right. Commentary discusses Hunter's presence drawing attention.|14|short middle pass|Hunter on the field; exact personnel unknown|unknown|unknown|verified vs DB|
|08:08|CLE|KC Concepcion|Gets the ball and advances to the 43. Play type is unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:19|CLE|Deshaun Watson|Rolls away on third-and-10 with receivers covered, evades a defender and is taken down; Cleveland must punt.|None|unknown|unknown|unknown|Oluokun (tackler)|unverified (no DB match; caption-only)|
|08:35|JAX|Amir Abdullah|Runs to the 33 and is knocked by Campbell.|None|run|unknown|unknown|Campbell (tackler)|unverified (no DB match; caption-only)|
|08:52|JAX|Trevor Lawrence|Is sacked by Mason Graham.|None|unknown|unknown|unknown|Mason Graham (sacker)|unverified (no DB match; caption-only)|
|09:02|CLE|Jerry Jeudy|Catches a 20-yard pass near midfield. Commentary identifies inside-breaking routes as his strength.|20|inside-breaking route|unknown|unknown|C.Ransaw; F.Oluokun (DB tacklers)|verified vs DB|
|09:14|CLE|Sanders|Catches a near-side dump-off, breaks a tackle and reaches inside the 40.|None|dump-off pass|unknown|unknown|Antonio Johnson (tackler)|unverified (no DB match; caption-only)|
|09:34|CLE|Deshaun Watson|Throws an incomplete deep pass toward Boston near the end of the half.|None|deep shot|unknown|drop man coverage; three-man rush, as stated immediately before the snap|unknown|unverified (no DB match; caption-only)|
|09:56|JAX|A.Abdullah|Returns the second-half kickoff. Captions say across the 40; DB ends the return at the 40.|35|kickoff return|unknown|unknown|C.Ryan; D.McMillon (DB tacklers)|verified vs DB|
|10:06|JAX|B.Tuten|Catches a screen against pressure, follows a blocker and makes a defender miss before reaching the Cleveland 23.|22|screen left|unknown|unknown|G.Delpit (DB tackler); unidentified missed tackler|verified vs DB|
|10:23|JAX|Bhayshul Tuten|Is spun down for a four-yard loss, with Graham arriving first.|-4|run|Strange comes in motion; exact personnel unknown|four-man defensive front; coverage unknown|Mason Graham (tackler)|unverified (no DB match; caption-only)|
|10:33|JAX|Jakobi Meyers|Catches a 32-yard touchdown after Lawrence escapes pressure and throws toward the back of the end zone.|32|deep left pass; throw after escaping pressure|shotgun|front four pressure; coverage unknown|unknown|verified vs DB|
|11:14|CLE|R.Sanders|Breaks through on a 74-yard kickoff return, makes a defender miss and is stopped by Brown at the Jacksonville 23.|74|kickoff return|unknown|unknown|M.Brown (DB tackler); unidentified missed tackler|CONFLICT (yardage 74 vs DB)|
|11:39|CLE|KC Concepcion|Catches an outside pass; commentary says he was down before the ball came loose.|None|outside pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:46|CLE|Deshaun Watson|Keeps the ball off a play fake and gains six yards inside the five.|6|play-action; quarterback keep|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:57|CLE|Deshaun Watson|Throws left and misses Boston, bringing up fourth down.|None|pass left|shotgun|unknown|unknown|unverified (no DB match; caption-only)|
|12:07|CLE|A.Szmyt|Makes a 26-yard field goal for Cleveland's first points.|26|field goal|unknown|unknown|unknown|verified vs DB|
|12:16|JAX|Cameron|Catches another pass from Lawrence off a play fake, with Ward in coverage.|None|play-action|unknown|unknown|Denzel Ward (coverage)|unverified (no DB match; caption-only)|
|12:30|JAX|Bhayshul Tuten|Runs to the edge, breaks free and spins inside the 25 for 12 yards.|12|edge run; side unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:47|JAX|Abdullah|Runs hard inside the 25 to the 22.|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:54|JAX|Cam Little|Makes a 40-yard field goal for a 34-3 lead.|40|field goal|unknown|unknown|unknown|verified vs DB|
|13:09|CLE|Fannin|Catches a pass off a play fake; the remainder of the call is truncated.|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:20|CLE|Fannin|Catches a pass after a fake handoff, lowers his shoulder and crosses the 35. Watson is hit while throwing.|None|play-action|unknown|defensive linemen aligned tightly; coverage unknown|Matt Dickerson (QB pressure)|unverified (no DB match; caption-only)|
|13:31|CLE|Deshaun Watson|Is hit and sacked near the end of the third quarter. Miller receives partial credit; the other defender's captioned name is unclear.|None|unknown|unknown|unknown|Miller (shared sack)|unverified (no DB match; caption-only)|
|13:53|CLE|KC Concepcion|Catches a deep pass for 25 yards and a first down at the Jacksonville 43.|25|deep right pass|unknown|unknown|J.Lewis (DB tackler)|verified vs DB|
|14:09|CLE|KC Concepcion|Takes a reverse that Jacksonville reads well; Brown makes the tackle.|None|reverse|unknown|unknown|Brown (tackler)|unverified (no DB match; caption-only)|
|14:21|CLE|Boston|Catches Watson's pass to the left and turns for a first down on second-and-13.|None|pass left|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:31|CLE|Deshaun Watson|Steps up on third-and-three, escapes Hines-Allen initially but is sacked.|None|unknown|unknown|unknown|Hines-Allen (pressure; final sacker unspecified)|unverified (no DB match; caption-only)|
|14:49|CLE|Deshaun Watson|Flips the ball to Sanders under pressure, but officials rule Watson down by contact before the apparent first-down completion.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:08|JAX|Bhayshul Tuten|Runs for an unspecified gain and is taken down by Verse.|None|run|unknown|unknown|Verse (tackler)|unverified (no DB match; caption-only)|
|15:17|JAX|Bhayshul Tuten|Is hit in the backfield by Graham and stood up by Verse and other Cleveland defenders on second-and-three.|None|run|unknown|unknown|Graham; Verse (tacklers)|unverified (no DB match; caption-only)|
|15:27|CLE|Judkins|Catches an underneath pass off a play fake, makes a defender miss, runs along the sideline and cuts left before going out at the 49.|None|play-action; underneath pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:45|CLE|Denzel Boston|Catches a 46-yard touchdown from Watson, who has ample time. Commentary highlights Boston getting free and making an athletic catch.|46|deep shot|unknown|unknown|unknown|verified vs DB|

Offense (Codex synthesis from this game's plays): Lawrence distributed touchdown passes to Washington, Cameron, Strange and Meyers. / Repeated play-action completions included Washington, Thomas and Cameron. / Tuten supplied tackle-breaking runs and a 22-yard screen reception; one first-down run used multiple tight ends. / Converted both matched Cleveland turnovers into touchdowns.

Defense weaknesses: Allowed the 20-yard Jeudy reception, 25-yard Concepcion reception and late 46-yard Boston touchdown. / Allowed several Cleveland play-action completions to Fannin and Judkins. / Kick coverage allowed Sampson's 37-yard return and Sanders's 74-yard return.

Limitations: Captions only; no frames were available. Personnel, routes, blocking assignments, coverage and individual responsibility generally cannot be established. Explicit defensive-front observations are recorded separately from unknown coverage within coverage_scheme. Named defenders include tacklers, pressure players and interceptors; their inclusion does not establish that they were beaten. DB facts control clearly matched plays, including Washington's 22-yard gain and the interception location. The interception entry's yards describe the return; field-goal yards describe kick distance. Unmatched gains remain null unless commentary supplies yardage. Names absent from clearly matching DB entries remain as recognizable caption renderings; the first Tuten entry contains a transcription spacing artifact. The early Watson fumble has no matching supplied DB entry and no established recovery. The supplied DB is selective, so NO DB MATCH does not establish that a play did not occur. DB-only kickoffs and returns without identifiable caption calls are omitted. Extra points are not separately called in these captions. The drop-man/three-man-rush comment appears immediately before the final first-half deep attempt, but edited-caption timing limits certainty about its attachment.


## Week 2: JAX 13 - DEN 20 (game 401872940)
Video: Jacksonville Jaguars vs. Denver Broncos Game Highlights | NFL 2026 Season Week 2 — https://www.youtube.com/watch?v=bGoj6Mktog0  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:12|DEN|J.K. Dobbins|Takes a handoff and accelerates across the 25; commentary names Gardeck and Washington on the stop.|None|handoff|unknown|unknown|Gardeck; Washington (credited with stop)|unverified (no DB match; caption-only)|
|00:25|DEN|Tyler Badie|Stopped for one yard on third-and-11; the captions do not establish whether this was a run or reception.|1|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:36|JAX|Brenton Strange|Comes back for Lawrence's off-back-foot throw and gains 14 into Denver territory.|14|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:56|JAX|Bri. Thomas|Lawrence completes a pass; sequence matches the DB's 22-yard short-left reception.|22|short left pass|unknown|unknown|B. Jones (DB tackler)|verified vs DB|
|01:01|JAX|Parker Washington|Catches Lawrence's downfield throw and extends to the Denver 1; Brandon Jones makes the tackle.|32|deep middle pass|shotgun|unknown|Brandon Jones (tackler)|verified vs DB|
|01:13|JAX|B. Tuten|Scores on a direct snap around right end. Commentary credits a pulling block to a player captioned as Van Lennon.|1|direct snap; right end run; pulling blocker|unknown|unknown|unknown|verified vs DB|
|01:45|DEN|Jaylen Waddle|With Sutton in motion, Nix leaves the pocket and throws deep. Waddle wins a contested catch against Buster Brown at the Jacksonville 1.|49|deep middle shot; quarterback outside pocket|unknown|unknown|Buster Brown|verified vs DB|
|02:04|DEN|J.K. Dobbins|Doubles back near the goal line but is contained by Hines-Allen without scoring.|None|run with cutback|unknown|unknown|Hines-Allen (contains runner)|unverified (no DB match; caption-only)|
|02:19|DEN|Wil Lutz|Makes a short field goal. Captions call it 21 yards; the authoritative DB records 20.|20|field goal|unknown|unknown|unknown|verified vs DB|
|02:33|JAX|Trevor Lawrence|Sacked as the pocket collapses; Malcolm Roach grabs his ankles. Commentary also mentions Zach Allen's pressure.|None|unknown|unknown|unknown|Malcolm Roach (sacker); Zach Allen (pressure mentioned)|unverified (no DB match; caption-only)|
|02:47|DEN|Jaylen Waddle|Makes an on-time reception from Nix; matches the 20-yard short-right completion.|20|short right pass|unknown|unknown|A. Johnson (DB tackler)|verified vs DB|
|02:55|DEN|Tyler Badie|Turns a reception into a big gain into Jacksonville territory.|27|short left pass|unknown|unknown|J. Lewis (DB tackler)|verified vs DB|
|03:08|DEN|Troy Franklin|Hauls in Nix's deep throw down the left side.|27|deep left shot|unknown|unknown|unknown|verified vs DB|
|03:24|DEN|Bo Nix|Pass intended for Courtland Sutton is intercepted by Jourdan Lewis in the back of the end zone for a touchback.|0|deep left pass|unknown|unknown|Jourdan Lewis (interceptor)|verified vs DB|
|03:36|JAX|Trevor Lawrence; unidentified receiver|With Thomas in motion, Lawrence completes a nine-yard pass to the 30.|9|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:48|JAX|Parker Washington|Makes a sliding attempt on a low throw; officials award a first down despite Denver disputing the catch.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:00|JAX|Thomas|Catches an outside throw for a first down across the 40 late in the half.|None|outside pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:12|JAX|Quintin Morris|Catches a seven-yard pass with the clock running; a flag follows.|7|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:22|JAX|Cam Little|Makes a 44-yard field goal to give Jacksonville a 10-3 halftime lead.|44|field goal|unknown|unknown|unknown|verified vs DB|
|04:36|JAX|Tuten|Takes a toss outside for a first down.|None|outside toss run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:50|JAX|Washington|Tries to work outside and is tripped up by Surtain; the captions do not establish the play type.|None|unknown|unknown|unknown|Surtain (tackler)|unverified (no DB match; caption-only)|
|04:58|JAX|Tuten|Takes a handoff, uses a stutter step, and is wrapped up crossing the 25.|None|handoff|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:16|JAX|Tuten|Turns the corner for a first down.|None|outside run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:19|JAX|Trevor Lawrence|Throws incomplete short of the goal line. Commentary names Allen and Singleton as waiting for the target.|0|unknown|shotgun|unknown|Allen; Singleton (defenders near target)|unverified (no DB match; caption-only)|
|05:31|JAX|Cam Little|Makes a 23-yard field goal to extend Jacksonville's lead to 13-3.|23|field goal|unknown|unknown|unknown|verified vs DB|
|05:41|DEN|Waddle|Apparently makes a first-down reception from Nix; the caption says 'tackle made by Waddle,' leaving the wording uncertain.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:51|DEN|Pat Bryant|Takes a reverse from the 48 to the 32; exact official yardage is unavailable.|None|reverse|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:01|DEN|Bo Nix|Avoids pressure and tosses the ball ahead on third-and-five; a flag is thrown and Gardeck is mentioned applying pressure. The result is unclear.|None|unknown|unknown|unknown|Gardeck (pressure)|unverified (no DB match; caption-only)|
|06:11|DEN|Wil Lutz|Makes a 45-yard field goal, cutting Jacksonville's lead to 13-6.|45|field goal|unknown|unknown|unknown|verified vs DB|
|06:26|JAX|A. Abdullah|Cuts outside on the kickoff return following Lutz's field goal.|30|kickoff return|unknown|unknown|D. Key; D. Tillman (DB tacklers)|CONFLICT (yardage 30 vs DB)|
|06:29|JAX|Trevor Lawrence|Third-and-six throw intended for Parker Washington is intercepted by R. Moss, who steps in front. DB records a three-yard return and Bonitto involvement.|3|deep left pass|unknown|unknown|R. Moss (interceptor); N. Bonitto (DB pressure credit)|verified vs DB|
|06:48|DEN|Bo Nix|Keeps the ball on third-and-six and veers toward the sideline.|None|quarterback keeper|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:56|DEN|Nate Adkins|Catches a pass following a fake handoff. Commentary corrects the receiver's name to Adkins.|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:09|DEN|Waddle|Catches a pass over the middle for a first down.|None|middle pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:19|DEN|Waddle|Makes an underneath catch on second-and-eight with Buster Brown in coverage.|None|underneath pass|shotgun|unknown|Buster Brown (coverage)|unverified (no DB match; caption-only)|
|07:28|DEN|N. Adkins|Scores wide open on a short-right pass after a run fake and Nix movement. Commentary attributes Jacksonville's assignment confusion to Bryant's motion inside number 45.|7|play-action; quarterback movement; short right pass; pre-snap motion|unknown|unknown|unknown|verified vs DB|
|07:55|JAX|J. Meyers|Lawrence targets Meyers downfield on third-and-eight. Captions say 'incomplete,' but the corresponding DB play records a 28-yard completion.|28|deep left pass|no huddle|unknown|T. Hufanga (DB tackler)|verified vs DB|
|08:06|JAX|Trevor Lawrence; Washington|Lawrence double-clutches and throws outside toward Washington; the pass is broken up. The defender's captioned name is too garbled to identify reliably.|0|outside pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:19|JAX|Cam Little|Fragmentary commentary refers to trying to put Jacksonville ahead. Sequence is consistent with the DB's missed 54-yard field goal, but the captions do not explicitly identify the kick or result.|54|field goal|unknown|unknown|unknown|verified vs DB|
|08:37|DEN|Courtland Sutton|Catches a pass into Jacksonville territory at the 45.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:43|DEN|Evan Engram|Makes a difficult catch on a long downfield throw from Nix.|None|downfield pass|shotgun|unknown|unknown|unverified (no DB match; caption-only)|
|08:55|DEN|J. Coleman|Scores through right tackle. Commentary credits right-side down blocks, Franklin's blocking, and pulling guard Powers, number 71.|3|right tackle run; down blocks; pulling guard|tight formation; single setback|unknown|unknown|verified vs DB|
|09:29|JAX|Tuten|Rips through for eight yards before Riley Moss makes the tackle.|8|handoff|unknown|unknown|Riley Moss (tackler)|unverified (no DB match; caption-only)|
|09:42|JAX|Trevor Lawrence; Thomas|Deep third-and-11 throw toward Thomas falls incomplete with Patrick Surtain running stride for stride.|0|deep shot|unknown|unknown|Patrick Surtain (successful coverage)|unverified (no DB match; caption-only)|
|09:56|DEN|Jaylen Waddle|Motions before the snap and catches Nix's throw after Nix leaves the pocket. Flags follow; DB records declined defensive holding on M. Brown.|29|deep right pass; quarterback outside pocket; pre-snap motion|unknown|unknown|J. Lewis (DB tackler); M. Brown (declined holding)|verified vs DB|
|10:12|DEN|Coleman|Runs up the middle for 12 yards and a first down near the two-minute warning. Commentary mentions left guard Powers.|12|middle run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:27|DEN|Coleman|Runs outside and deliberately goes down to help close out the game.|None|outside run|unknown|unknown|unknown|unverified (no DB match; caption-only)|

Offense (Codex synthesis from this game's plays): Lawrence produced chunk completions to Thomas, Washington, and Meyers, with DB gains of 22, 32, and 28 yards. / Tuten scored on a direct snap and gained first downs on an outside toss and another corner-turning run. / Late-first-half completions helped set up Little's 44-yard field goal.

Defense weaknesses: Allowed Waddle receptions of 49, 20, and 29 yards, plus additional underneath and middle catches. / Allowed consecutive 27-yard receptions to Badie and Franklin on a second-quarter possession. / Commentary explicitly identified motion-induced assignment confusion on Adkins's tying touchdown. / Denver's right-side down blocks and pulling guard opened Coleman's go-ahead touchdown run.

Limitations: Captions only; no frames were viewed and no commands were run. The supplied DB is selective, so NO DB MATCH does not mean a play did not occur. Some caption-to-DB links rely on sequence, especially the 00:56 completion and fragmentary 08:19 field-goal reference. The Meyers captions conflict with the DB on completion status; the DB controls the recorded result. Unmatched names remain as captioned when identification is uncertain. Personnel and coverage are unknown unless explicitly stated; the slot-matchup and outside-blitz discussion cannot be assigned confidently to a specific play. Named tacklers, interceptors, and successful coverage defenders in defender_beaten are identified by role and do not imply they were beaten. Interception yards represent return yards; field-goal yards represent kick distance. Kickoffs, the Sutton pass-interference penalty, extra points, and other DB events without identifiable caption coverage were not added as separate highlights.


## Week 3: NE 6 - JAX 35 (game 401872957)
Video: New England Patriots vs Jacksonville Jaguars Game Highlights | 2026 NFL Season Week 3 — https://www.youtube.com/watch?v=Oi9HQlp-ysA  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 4: JAX 22 - CIN 17 (game 401872969)
Video: Jacksonville Jaguars vs Cincinnati Bengals Game Highlights | 2026 NFL Season Week 4 — https://www.youtube.com/watch?v=a2zogEoiXV0  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 5: PHI 17 - JAX 19 (game 401872981)
Video: Philadelphia Eagles vs. Jacksonville Jaguars Game Highlights | 2026 NFL Season Week 5 — https://www.youtube.com/watch?v=WXw2IIj01Sg  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 6: HOU 34 - JAX 31 (game 401872996)
Video: Houston Texans vs. Jacksonville Jaguars Game Highlights | 2026 NFL Season Week 6 — https://www.youtube.com/watch?v=SQT1S7J4s-o  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:24|JAX|Brenton Strange|Lawrence completes a seam pass on the opening offensive play.|24|seam pass|unknown|unknown|C.Bullock (DB tackler)|verified vs DB|
|00:35|JAX|Brian Thomas Jr.|Lawrence throws incomplete to Thomas.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:44|JAX|Lequint Allen|Swing-pass completion fails to reach the third-down marker; gain unspecified.|None|swing pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:51|HOU|Dalton Schultz|Schultz catches a high throw and is tackled by Dennis Gardeck; Houston goes three-and-out.|None|unknown|unknown|showed zero blitz, then dropped into coverage|Dennis Gardeck (tackler)|unverified (no DB match; caption-only)|
|01:03|JAX|Trevor Lawrence|Lawrence escapes pressure from Will Anderson and dives near midfield.|None|quarterback scramble|empty|unknown|Will Anderson Jr. (pressure)|unverified (no DB match; caption-only)|
|01:13|JAX|unknown|A downhill pitch gains a first down; ball carrier and yardage are not identified.|None|pitch run|tight bunch|unknown|unknown|unverified (no DB match; caption-only)|
|01:22|JAX|Parker Washington|Lawrence targets Washington on an in-breaking route against a blitz; the next shown snap is fourth down.|None|in-breaking route|unknown|blitz|unknown|unverified (no DB match; caption-only)|
|01:34|JAX|Parker Washington|Lawrence extends the fourth-down play, but Tremon Smith jumps the route and breaks up the pass.|0|extended passing play|unknown|unknown|Tremon Smith (pass breakup)|unverified (no DB match; caption-only)|
|01:50|HOU|Xavier Hutchinson|Stroud quickly finds his hot read against an edge blitz for a first down.|None|hot-read pass|unknown|edge blitz|unknown|unverified (no DB match; caption-only)|
|02:00|HOU|Nico Collins|Stroud uses play-action and a shoulder fake before finding Collins inside the 10.|42|play-action deep shot right|unknown|unknown|T.Hunter (DB tackler)|verified vs DB|
|02:13|HOU|Foster Moreau|Moreau catches a quick touchdown pass while wide open after a coverage breakdown.|6|quick pass right|empty; Woody Marks motions out of backfield|blown coverage; scheme unspecified|unknown|verified vs DB|
|02:31|JAX|Chris Rodriguez Jr.|Rodriguez breaks tackles and runs through arm tackles toward midfield.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:38|JAX|Brenton Strange|Strange catches a third-down pass over the middle and gains enough for a first down.|10|pass over middle|Brian Thomas Jr. in motion|unknown|unknown|unverified (no DB match; caption-only)|
|02:53|JAX|Chris Rodriguez Jr.|Rodriguez breaks a tackle and reaches approximately the 30-yard line; commentary estimates eight to eight-and-a-half yards.|None|unknown|unknown|unknown|Kaylen Bullock (caption-rendered name; tackler)|unverified (no DB match; caption-only)|
|03:02|JAX|Chris Rodriguez Jr.|Rodriguez finds a large crease and bounces the run for approximately seven or eight yards.|None|power running game; bounce outside|three tight ends|unknown|unknown|unverified (no DB match; caption-only)|
|03:12|JAX|unknown (caption renders name as 'Titan')|Runner gets an extra push and reaches the line to gain.|None|power running game|unknown|unknown|To'oto'o (tackler)|unverified (no DB match; caption-only)|
|03:23|JAX|Parker Washington|Washington catches a sideline pass and steps out at the six.|8|sideline pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:34|JAX|unknown (caption renders name as 'Tyutin')|A toss reaches the end zone, but a holding penalty on Brenton Strange nullifies the touchdown.|None|toss run to edge|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:58|JAX|Trevor Lawrence|Lawrence's third-and-goal pass intended for Jakobi Meyers is intercepted by Calen Bullock in the end zone for a touchback.|0|pass to back of end zone|empty backfield|unknown|C.Bullock (interceptor)|verified vs DB|
|04:15|HOU|Woody Marks|Marks is stopped short on a third-down run.|None|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:28|JAX|Parker Washington|Washington gets loose against a blitz, reaches the edge and gains a first down before Logan Hall stops him.|None|unknown|unknown|blitz|Logan Hall (tackler)|unverified (no DB match; caption-only)|
|04:44|JAX|Parker Washington|Lawrence drops a sideline pass over Kamari Lassiter's shoulder on third down.|27|deep sideline pass left|unknown|man-to-man; blitz|Kamari Lassiter|verified vs DB|
|04:58|JAX|Bhayshul Tuten|Tuten catches a pass in the flat, follows Jakobi Meyers' block and weaves down the sideline for a touchdown.|27|pass to right flat; yards after catch|unknown|unknown|unknown|verified vs DB|
|05:19|HOU|Jaylin Noel|Noel breaks free after the catch and reaches the Jacksonville 35.|34|short middle pass; yards after catch|unknown|unknown|A.Johnson (DB tackler)|verified vs DB|
|05:33|HOU|Marvin Harrison Jr.|Stroud connects with Harrison on a crossing route near the goal line; exact spot and gain are unclear.|None|crossing route|Harrison aligned tight right|unknown|unknown|unverified (no DB match; caption-only)|
|05:46|HOU|Dalton Schultz|Schultz catches a tipped pass against a blitz and finishes approximately half a yard short of the first-down marker.|None|unknown|Marks to Stroud's right|blitz|unknown|unverified (no DB match; caption-only)|
|05:58|HOU|Ka'imi Fairbairn|Fairbairn makes a 25-yard field goal to give Houston a 10–7 lead.|25|field goal|unknown|unknown|unknown|verified vs DB|
|06:14|JAX|Josh Cameron|Cameron returns the kickoff past midfield, giving Jacksonville the ball at the Houston 48.|46|kickoff return|unknown|unknown|K.Fairbairn; J.Hansen (DB tacklers)|CONFLICT (yardage 46 vs DB)|
|06:39|JAX|Chris Rodriguez Jr.|Rodriguez runs through contact for seven yards.|7|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:43|JAX|Jakobi Meyers|Meyers converts third-and-eight on an in-cutting route.|None|in-cutting route|tight bunch right; Meyers in motion|unknown|unknown|unverified (no DB match; caption-only)|
|06:54|JAX|Travis Hunter|Hunter catches a pass over the middle down to the four with Tremon Smith trying to stay with him.|None|pass over middle|unknown|unknown|Tremon Smith|unverified (no DB match; caption-only)|
|07:07|JAX|Bhayshul Tuten|Lawrence rolls out and finds Tuten wide open for his second receiving touchdown.|2|rollout pass right|unknown|unknown|unknown|verified vs DB|
|07:29|HOU|Jaylin Noel|Stroud completes a deep shot down the middle to Noel.|50|deep shot middle|unknown|unknown|Jar.Jones (DB tackler)|verified vs DB|
|07:38|HOU|Nico Collins|A pass to the right side of the end zone is incomplete, but defensive pass interference is called on Travis Hunter.|None|end-zone deep shot|unknown|four-man rush; coverage unspecified|Travis Hunter (pass-interference penalty)|unverified (no DB match; caption-only)|
|07:56|HOU|Foster Moreau|Moreau makes a one-handed touchdown catch over the defender's outstretched arms.|1|short pass left|unknown|unknown|Jar.Jones (commentary renders name as 'Jerry Jones')|verified vs DB|
|08:26|HOU|Dalton Schultz|Schultz catches a slant for nine yards, with Antonio Johnson stopping him short of the first down.|9|slant|unknown|unknown|Antonio Johnson (tackler)|unverified (no DB match; caption-only)|
|08:36|HOU|unknown (punter)|Houston's punt bounces into the end zone, but Jacksonville's failure to get a defender off the field produces a five-yard penalty and a Houston first down.|None|punt; defensive substitution penalty|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:57|HOU|Marvin Harrison Jr.|Harrison catches Stroud's pass and gains 15 yards on an RPO.|15|RPO|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:12|HOU|Jaylin Noel|Stroud releases quickly to Noel for a 10-yard first down.|10|quick pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:20|HOU|Jawhar Jordan|Jordan takes a toss into the red zone behind an extra offensive lineman.|None|toss run|extra offensive lineman|unknown|unknown|unverified (no DB match; caption-only)|
|09:30|HOU|Marvin Harrison Jr.|Houston uses tempo and a quick snap; Harrison catches another first-down pass against a three-man rush.|None|quick-snap passing play|unknown|three-man rush; coverage unspecified|unknown|unverified (no DB match; caption-only)|
|09:38|HOU|Jaylin Noel|Stroud floats a touchdown pass to Noel; commentary praises the route.|13|short pass right|Marvin Harrison Jr. in slot as No. 3 receiver|unknown|unknown|verified vs DB|
|09:54|JAX|Jakobi Meyers|Lawrence throws incomplete off his back foot after play-action; a defender rendered as 'usher' gets an arm in the passing lane.|0|play-action|unknown|unknown|unknown (caption renders defender as 'usher')|unverified (no DB match; caption-only)|
|10:05|JAX|Jakobi Meyers|Lawrence initially avoids the rush, but Tremon Smith knocks away the sideline pass to force a three-and-out.|0|sideline pass|unknown|unknown|Tremon Smith (pass breakup)|unverified (no DB match; caption-only)|
|10:17|HOU|unknown (caption renders receiver as 'Booty')|Receiver makes a toe-tapping sideline catch for a first down on Stroud's rollout.|None|rollout pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:26|HOU|C.J. Stroud|Jacksonville drops into zone and rushes four; Stroud scrambles toward the sideline but falls short of the first down.|None|quarterback scramble|unknown|zone; four-man rush|unknown|unverified (no DB match; caption-only)|
|10:38|JAX|Jakobi Meyers|Meyers catches a wide-open pass over the middle and runs beyond midfield. Commentary says 21 yards; the DB records 22.|22|short middle pass; yards after catch|unknown|unknown|H.To'oTo'o; C.Bullock (DB tacklers)|verified vs DB|
|10:54|JAX|Jakobi Meyers|Jacksonville picks up the blitz, allowing Lawrence to find Meyers on a long sideline throw.|28|deep sideline pass left|unknown|blitz|C.Bullock (DB tackler)|verified vs DB|
|11:04|JAX|unknown (caption renders name as 'Tyutin')|A screen reaches the edge and finishes inside the five, with Derek Stingley Jr. forcing the runner out; commentary also identifies a late defensive substitution.|None|screen|unknown|unknown|Derek Stingley Jr. (tackler); Jadeveon Clowney (late substitution)|unverified (no DB match; caption-only)|
|11:15|JAX|Nate Boerkircher|Boerkircher makes a one-handed touchdown catch on a short pop pass after quarterback-run action.|1|quarterback-run action; pop pass right|unknown|unknown|unknown|verified vs DB|
|11:28|HOU|Dalton Schultz|Schultz catches a seam pass for 16 yards before Kaevon Merriweather stops him.|16|seam pass|unknown|unknown|Kaevon Merriweather (tackler)|unverified (no DB match; caption-only)|
|11:39|HOU|Xavier Hutchinson|Stroud moves out of the pocket and throws sidearm to Hutchinson at the sideline.|None|extended passing play|empty backfield; Woody Marks in motion|three-man rush; coverage unspecified|unknown|unverified (no DB match; caption-only)|
|11:51|HOU|Nico Collins|Houston targets Collins down the sideline against one-on-one coverage; Jaron Jones is called for pass interference.|None|sideline shot|unknown|one-on-one|Jaron Jones (pass-interference penalty)|unverified (no DB match; caption-only)|
|12:03|HOU|Jawhar Jordan|Jordan takes a toss, finds a cutback lane and breaks a secondary tackle for a touchdown; DB records a run at left tackle.|25|toss; cutback; left tackle|unknown|unknown|unknown|verified vs DB|
|12:18|JAX|Travis Hunter|Hunter catches a slant, breaks tackles and uses a stiff arm before reaching the Houston 30.|26|slant; yards after catch|Hunter in slot|unknown|A.Al-Shaair; H.To'oTo'o (DB tacklers)|verified vs DB|
|12:34|JAX|Parker Washington|Washington catches a quick pass, stays in bounds and fights for a first down.|None|quick pass|unknown|four-man rush; coverage unspecified|unknown|unverified (no DB match; caption-only)|
|12:46|JAX|Travis Hunter|Following a fake to the motioning Jakobi Meyers, Hunter catches a throwback screen and splits defenders to reach the 11.|None|motion fake; throwback screen|Jakobi Meyers in motion|unknown|unknown|unverified (no DB match; caption-only)|
|12:57|JAX|Chris Rodriguez Jr.|Rodriguez converts a third-down run to set up first-and-goal at the seven.|None|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:05|JAX|Travis Hunter|Hunter aligns in the backfield and catches a touchdown pass at the goal line.|7|short pass left|Hunter in backfield|unknown|unknown|verified vs DB|
|13:25|HOU|unknown (caption renders receiver as 'booty')|Receiver holds on to a tight-window catch despite being driven backward by Kaevon Merriweather.|None|unknown|unknown|unknown|Kaevon Merriweather (tackler)|unverified (no DB match; caption-only)|
|13:34|HOU|Cade Stover|Stover takes a direct snap and gains a first down behind a push.|None|direct-snap run; push|tight end at quarterback|unknown|unknown|unverified (no DB match; caption-only)|
|13:44|HOU|Woody Marks|Marks gains seven yards on first down to the Jacksonville 46.|7|run; direction unknown|unknown|unknown|Ventrell Miller (one of the tacklers)|unverified (no DB match; caption-only)|
|13:56|HOU|Nico Collins|Collins comes back to help Stroud and converts for a first down against Travis Hunter.|21|short pass right; return toward quarterback|unknown|four-man rush; coverage unspecified|Travis Hunter; K.Merriweather (additional DB tackler)|verified vs DB|
|14:11|HOU|Woody Marks|Marks makes a subtle move near the 25 and runs for a first down.|None|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:19|HOU|Nico Collins|Collins catches a receiver screen in a one-on-one situation and reaches the nine before stepping out; Jordan Lewis brings him down.|None|wide receiver screen|Nico Collins in motion|one-on-one on screen; broader scheme unspecified|Jordan Lewis (caption-rendered name; tackler)|unverified (no DB match; caption-only)|
|14:35|HOU|C.J. Stroud|Travis Hunter undercuts the route intended for Xavier Hutchinson and intercepts Stroud's play-action pass in the end zone for a touchback.|0|play-action; short pass right|unknown|Hunter in trail on replay commentary; broader scheme unspecified|Travis Hunter (interceptor)|verified vs DB|
|15:00|JAX|Jakobi Meyers|Meyers bobbles but secures a pass over the middle.|None|pass over middle|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:06|JAX|Marshall (caption-rendered name)|Screen receiver follows a block and cutback lane for eight yards.|8|screen; cutback|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:19|JAX|Trevor Lawrence|Lawrence looks left before returning over the middle; Bullock nearly intercepts the pass.|0|pass over middle|unknown|outside leverage mentioned; full scheme unspecified|Kaylen Bullock (caption-rendered name; near interception)|unverified (no DB match; caption-only)|
|15:29|JAX|Brenton Strange|Houston shows an all-out blitz and brings pressure; Strange reaches back for a catch at the 42.|None|unknown|unknown|all-out blitz look; pressure sent|unknown|unverified (no DB match; caption-only)|
|15:38|JAX|Cam Little|Little makes a 60-yard field goal to tie the game at 31.|60|field goal|unknown|unknown|unknown|verified vs DB|
|15:49|HOU|unknown (receiver)|Stroud completes a pass against a blitz, approximately two yards short of the first down, while Josh Allen pressures him.|None|pass against blitz|unknown|blitz|Josh Allen (caption-rendered name; pressure)|unverified (no DB match; caption-only)|
|16:04|HOU|Woody Marks|Marks catches a wide-open pass and runs to the sideline; replay commentary credits his release with freezing the linebackers.|None|pass to running back; yards after catch|unknown|four-man rush; coverage unspecified|unknown|unverified (no DB match; caption-only)|
|16:18|HOU|Jawhar Jordan|Jordan runs to the Jacksonville 32 to improve field-goal position with 47 seconds remaining.|None|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|16:27|HOU|Cade Stover|Stover takes another direct snap and gets a short push before Houston drains the clock.|None|direct-snap run; push|tight end at quarterback|unknown|unknown|unverified (no DB match; caption-only)|
|16:39|HOU|Ka'imi Fairbairn|Fairbairn makes the winning 49-yard field goal as time expires.|49|field goal|unknown|unknown|unknown|verified vs DB|

Offense (Codex synthesis from this game's plays): Lawrence distributed explosive passes to Strange, Washington, Meyers and Hunter. / Screens and short throws produced substantial gains: Tuten's 27-yard touchdown, Hunter's slant and throwback screen, and an eight-yard late screen. / Motion and backfield deployments featured in Meyers' third-down conversion, Hunter's throwback screen and Hunter's touchdown. / Rodriguez supplied repeated gains through contact and a red-zone third-down conversion. / Short scoring passes reached Tuten twice and Boerkircher once.

Defense weaknesses: Houston completed gains of 42 yards to Collins and 34 and 50 yards to Noel. / Commentary explicitly called Moreau's first touchdown a blown coverage. / Pass-interference penalties against Hunter and Jaron Jones helped Houston advance on scoring possessions. / A defender failing to leave the field erased a Houston punt and extended the possession that ended with Noel's touchdown. / Jordan found a cutback lane and broke a secondary tackle on his 25-yard touchdown. / Marks was wide open on a late catch-and-run; commentary credited his release with freezing the linebackers.

Limitations: Analysis uses only supplied captions and DB excerpts; no video frames, browsing or commands. The DB excerpt omits many ordinary plays, so NO DB MATCH means no matching supplied line, not that the play did not occur. Caption times identify commentary segments and may include replay discussion. Unmatched garbled names remain unresolved; prior-play fragments and general discussion were not treated as separate plays. Exact gains are null when absent or only approximate; DB yardage takes precedence on clear matches. Field-goal yards are kick distances. The nullified rushing touchdown is not counted as a score. DB tacklers, pressure players, penalty offenders and pass-breakup defenders are labeled in defender_beaten for traceability; their inclusion does not establish they were beaten. Formations and coverage are limited to explicit commentary, with rush counts and partial descriptions distinguished from full schemes. No complete personnel groupings, route combinations, blocking assignments or coverage responsibilities can be established from these captions.
