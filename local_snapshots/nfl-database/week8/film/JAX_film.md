# JAX — Phase 8 film notes (Weeks 1–6, 2026)
> Note: games 401872957, 401872969, 401872981 were extracted by Grok via the xAI API (grok-4.20-0309-non-reasoning, same prompt/schema as Codex, cleaned captions); sidecar provenance in film/grok_meta/. All other games with notes: Codex.

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

Offense (model synthesis from this game's plays): Lawrence distributed touchdown passes to Washington, Cameron, Strange and Meyers. / Repeated play-action completions included Washington, Thomas and Cameron. / Tuten supplied tackle-breaking runs and a 22-yard screen reception; one first-down run used multiple tight ends. / Converted both matched Cleveland turnovers into touchdowns.

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

Offense (model synthesis from this game's plays): Lawrence produced chunk completions to Thomas, Washington, and Meyers, with DB gains of 22, 32, and 28 yards. / Tuten scored on a direct snap and gained first downs on an outside toss and another corner-turning run. / Late-first-half completions helped set up Little's 44-yard field goal.

Defense weaknesses: Allowed Waddle receptions of 49, 20, and 29 yards, plus additional underneath and middle catches. / Allowed consecutive 27-yard receptions to Badie and Franklin on a second-quarter possession. / Commentary explicitly identified motion-induced assignment confusion on Adkins's tying touchdown. / Denver's right-side down blocks and pulling guard opened Coleman's go-ahead touchdown run.

Limitations: Captions only; no frames were viewed and no commands were run. The supplied DB is selective, so NO DB MATCH does not mean a play did not occur. Some caption-to-DB links rely on sequence, especially the 00:56 completion and fragmentary 08:19 field-goal reference. The Meyers captions conflict with the DB on completion status; the DB controls the recorded result. Unmatched names remain as captioned when identification is uncertain. Personnel and coverage are unknown unless explicitly stated; the slot-matchup and outside-blitz discussion cannot be assigned confidently to a specific play. Named tacklers, interceptors, and successful coverage defenders in defender_beaten are identified by role and do not imply they were beaten. Interception yards represent return yards; field-goal yards represent kick distance. Kickoffs, the Sutton pass-interference penalty, extra points, and other DB events without identifiable caption coverage were not added as separate highlights.


## Week 3: NE 6 - JAX 35 (game 401872957)
Video: New England Patriots vs Jacksonville Jaguars Game Highlights | 2026 NFL Season Week 3 — https://www.youtube.com/watch?v=Oi9HQlp-ysA  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:13|NE|M.Hollins|3rd and 5, complete first down reception|21|unknown|unknown|unknown|T.Hunter|verified vs DB|
|00:33|NE|H.Henry|3rd and 9 pass to Hunter Henry|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:45|JAX|B.Tuten|Run around the edge, first down|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:58|JAX|J.Meyers|Pass complete to Jakobi Meyers|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:12|NE|D.Maye|Sacked and fumbled, recovered by JAX|-7|unknown|unknown|unknown|unknown|verified vs DB|
|01:19|JAX|T.Lawrence|Play action, scrambles and tripped up|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:47|JAX|P.Washington|Pass complete to Parker Washington|17|unknown|unknown|unknown|unknown|verified vs DB|
|02:01|JAX|C.Rodriguez|Run first down and more, into second level|5|run|unknown|unknown|unknown|verified vs DB|
|02:24|JAX|J.Cameron|Pass over the middle, touchdown|12|unknown|unknown|unknown|unknown|verified vs DB|
|03:30|JAX|T.Lawrence|Pass deflected and intercepted by M.Jones|12|unknown|unknown|unknown|M.Jones|verified vs DB|
|04:04|NE|M.Hollins|Deflected pass caught by Hollins|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:45|JAX|B.Tuten|Downhill run, picks up 9|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:53|JAX|B.Strange|Play action pass to Strange, showing wheels|23|play-action|unknown|unknown|C.Davis|verified vs DB|
|05:03|JAX|J.Meyers|Pump fake, pass to end zone, touchdown|10|play-action|unknown|unknown|unknown|verified vs DB|
|05:43|NE|D.Douglas|Pass caught by Douglas|38|unknown|unknown|unknown|T.Hunter|verified vs DB|
|06:18|NE|D.Maye|Pass picked off by T.Hunter|0|unknown|unknown|unknown|T.Hunter|verified vs DB|
|07:38|NE|A.Borregales|38 yard field goal attempt, missed wide right|38|unknown|unknown|unknown|unknown|verified vs DB|
|07:49|JAX|B.Tuten|Play action, somehow gets it out to Tuten|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:20|JAX|J.Meyers|Pass complete to Meyers under pressure|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:42|JAX|J.Meyers|Pass to Meyers, dancing inside the 5|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:05|JAX|P.Washington|Pass to Washington, touchdown (after DPI penalty)|17|unknown|unknown|unknown|M.Jones|verified vs DB|
|09:43|NE|D.Maye|Pass intercepted by J.Jones, return to the 5|31|unknown|unknown|unknown|J.Jones|verified vs DB|
|10:19|JAX|C.Rodriguez|Run, touchdown|5|run|unknown|unknown|unknown|verified vs DB|
|11:20|NE|R.Doubs|Pass complete to Doubs, first down|21|unknown|unknown|unknown|A.Johnson|verified vs DB|
|11:28|NE|K.Williams|Pass complete to K.Williams, out of bounds|34|unknown|unknown|unknown|J.Jones|verified vs DB|
|12:06|NE|A.Borregales|Field goal is good|40|unknown|unknown|unknown|unknown|verified vs DB|
|12:16|JAX|J.Cameron|Kickoff return after muff, long return|42|unknown|unknown|unknown|unknown|CONFLICT (yardage 42 vs DB)|
|12:32|JAX|J.Meyers|Pass to Jakobi Meyers, pickup of 13|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:42|JAX|T.Lawrence|Design run, breaking tackles|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:51|JAX|B.Tuten|Handoff, touchdown run|1|run|unknown|unknown|unknown|verified vs DB|
|13:16|NE|R.Doubs|Pass complete to Doubs|20|unknown|unknown|unknown|C.Ransaw|verified vs DB|

Offense (model synthesis from this game's plays): Effective play-action passing leading to big plays and TDs / Explosive run game with multiple RBs contributing (Tuten, Rodriguez) / Red zone efficiency with multiple passing and rushing touchdowns / Protection allowing Lawrence to make plays under pressure

Defense weaknesses: Allowed several long pass completions in second half / Penalties in secondary (DPI)

Limitations: Could not determine specific personnel, formations, or coverage schemes as they were not explicitly stated by commentators. Some plays in captions were vague or did not perfectly align with DB details so yards and exact concepts were conservatively assigned only when clear. Many caption name manglings were corrected only for clear DB matches. Could not identify every single play mentioned due to caption incompleteness and lack of video.


## Week 4: JAX 22 - CIN 17 (game 401872969)
Video: Jacksonville Jaguars vs Cincinnati Bengals Game Highlights | 2026 NFL Season Week 4 — https://www.youtube.com/watch?v=a2zogEoiXV0  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:18|JAX|Tuten|Tuten run, gain of 15 yards|15|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:32|JAX|Tuten|Tuten hit in backfield, loss of 4 yards|-4|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:43|JAX|Meyers|Lawrence pass underneath complete to Meyers, short gain of 5 yards|5|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:54|CIN|Higgins|Fake handoff on jet sweep, pass complete to Higgins, out of bounds at 23|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:03|CIN|Meyers|Burrow quick toss to outside, Meyers breaks tackle, first down at 35|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:18|CIN|Higgins|Higgins bounces off one, shy of first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:36|JAX|Lawrence|Lawrence under pressure, wrapped up and taken down by Myles Murphy, loss of 7|-7|unknown|unknown|unknown|Myles Murphy|unverified (no DB match; caption-only)|
|01:46|JAX|Lawrence|Lawrence from gun, pass complete to Strange who breaks tackle for first down, gain of 23|23|unknown|unknown|unknown|unknown|verified vs DB|
|02:06|JAX|Meyers|Pass complete to Meyers who makes defender miss, to the 40|None|unknown|unknown|unknown|unknown|verified vs DB|
|02:16|JAX|Strange|Strange in motion, Lawrence underneath to him, brought down by Battle|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:28|JAX|Little|Field goal attempt is good (55 yards)|55|unknown|unknown|unknown|unknown|verified vs DB|
|02:40|CIN|Chase|Burrow to Chase, trying to make man miss, thrown out by Hunter, gain of 6|6|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:54|CIN|Higgins|Burrow looking middle to Higgins for first down, gain of 10, tackled by Hines-Allen|10|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:05|CIN|Chase|Pressure from Jags, Burrow throws to Chase who gets first down to 22|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:21|CIN|Burrow|Burrow under pressure, sacked, loss (by Armstead and others)|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:36|CIN|Chase|Quick toss to Chase who makes man miss then hit, flag for facemask/roughing|None|unknown|unknown|unknown|unknown|verified vs DB|
|04:03|CIN|Brown|Pass underneath to Brown inside the 15|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:15|CIN|Burrow|Burrow runs left and sits down close to 10-yard line|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:24|CIN|McPherson|Field goal is good (29 yards), ties franchise record|29|unknown|unknown|unknown|unknown|verified vs DB|
|04:35|JAX|Strange|Lawrence throws to tight end Strange for first down, gain of 12|12|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:47|JAX|Cameron|Lawrence throws middle underneath, complete to tight end (Cameron), first down gain of 15|15|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:02|JAX|Thomas|Toss to left, pass complete to Thomas inside the 39|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:13|JAX|Rodriguez|Hand off to Rodriguez for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:18|JAX|Cameron|Lawrence looking for Cameron, zips it along outside, inside 10 stopped out of bounds|None|unknown|unknown|unknown|unknown|verified vs DB|
|05:39|JAX|Little|Field goal attempt 28 yards is good, Jags lead 6-3|28|unknown|unknown|unknown|unknown|verified vs DB|
|05:49|CIN|Meyers|Burrow rolls right, throw on run complete to Meyers for first down inside JAX territory, gain of 10|10|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:02|CIN|Burrow|Burrow out of gun, lobs it intercepted by Lewis (hit as threw), return to inside 20|45|unknown|unknown|unknown|unknown|verified vs DB|
|06:18|JAX|Tuten|Tuten slips through defense to 8-yard line|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:30|JAX|Thomas|Lawrence looking left, throws to back of end zone, caught for touchdown by Brian Thomas (7 yards)|7|unknown|unknown|unknown|unknown|verified vs DB|
|07:01|CIN|Higgins|Burrow underneath to Higgins|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:14|CIN|Higgins|Burrow zips to Higgins trying to get out of bounds, marked at 41|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:28|CIN|Brown|Burrow out of gun under pressure, throws underneath to Brown stopped at 45|None|unknown|unknown|unknown|Lewis|unverified (no DB match; caption-only)|
|07:47|CIN|Burrow|Hines-Allen pressuring, Burrow steps up sacked by Armstead, loss of 3|-3|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:00|CIN|Higgins|Burrow throw far side, leaping catch by Higgins|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:27|CIN|Higgins|Burrow to Higgins for first down, tackled by Murray|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:34|CIN|Meyers|Toss pass complete to Dante Meyers on right side to 18, first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:47|CIN|Gesicki|Burrow throwing left, caught by Gesicki for touchdown (15 yards)|15|unknown|unknown|unknown|unknown|verified vs DB|
|09:10|JAX|Lawrence|Lawrence steps up and sacked, loss of 5|-5|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:22|JAX|Meyers|Strange in motion, pass complete underneath to Meyers (Jakobi) for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:32|JAX|Cameron|Lawrence pitches left then throws right to Cameron who sheds tackle inside CIN territory|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:49|JAX|Strange|Lawrence to Strange who hurdles defender then fumbles, punched out of bounds by Meyers|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:01|JAX|Lawrence|Lawrence brought down and sacked at 39|-39|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:11|JAX|Washington|Lawrence looking long to Parker Washington in end zone, diving attempt can't hang on|None|deep shot|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:23|JAX|Little|54-yard field goal attempt is good|54|unknown|unknown|unknown|unknown|verified vs DB|
|10:40|CIN|Brown|Burrow steps up, throws near sideline caught by Brown|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:51|CIN|Brown|Burrow dumps to Chase Brown on third down for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:04|CIN|Higgins|Meyers in motion, Burrow steps up hit as throws, complete to Higgins to 10, gain of 26|26|unknown|unknown|unknown|unknown|verified vs DB|
|11:23|CIN|Burrow|Burrow will throw again, intercepted by Oluokun in front of Tinsley|5|unknown|unknown|unknown|unknown|verified vs DB|
|11:52|JAX|Tuten|Give to Tuten who bounces right across 30 to 35|20|unknown|unknown|unknown|unknown|verified vs DB|
|12:06|JAX|Rodriguez|Hand off to Rodriguez, nothing there, loss of 2 (blown up by Lawrence and Murphy)|-2|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:22|CIN|Higgins|Burrow sets up, pass to Higgins over 100 yards to 38|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:31|CIN|Burrow|Burrow hit as throws to far side, incomplete intended for Tinsley, broken up by Hunter|0|unknown|unknown|unknown|Travis Hunter|unverified (no DB match; caption-only)|
|12:46|JAX|Tuten|Lawrence out of backfield as Tuten stumbles just shy of first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:56|JAX|Strange|Lawrence in middle of field, pass complete to Strange on diving catch|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:03|JAX|Rodriguez|Rodriguez in daylight inside 5 for touchdown (25 yards)|25|unknown|unknown|unknown|unknown|verified vs DB|
|13:47|CIN|Higgins|Tee Higgins kept feet in bounds, gain of 19|19|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:54|CIN|Higgins|Burrow pressure eludes, throws middle to Higgins for first down at 32, gain of 16|16|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:08|CIN|Gesicki|Burrow steps up in pocket, throws on run to Gesicki out of bounds at 23|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:24|CIN|Tinsley|Burrow looking toward end zone, slant pass caught by Tinsley to 1-yard line, gain of 9|9|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:35|CIN|Burrow|Burrow QB sneak/keeper for touchdown from 1 yard|1|unknown|unknown|unknown|Oluokun|verified vs DB|
|15:09|JAX|Strange|Lawrence throws middle complete to Strange for first down at 45|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:20|JAX|Lawrence|Off play fake, Lawrence thrown down by Dexter Lawrence, loss of 1 (sack)|-1|play-action|unknown|unknown|Dexter Lawrence|unverified (no DB match; caption-only)|
|15:37|JAX|Washington|Washington along sidelines for first down inside 20 to 15|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|16:18|CIN|Tinsley|Burrow looking sidelines, lofts to far side, leaping catch by Tinsley behind Jones|29|deep shot|unknown|unknown|Jarrian Jones|verified vs DB|
|16:37|CIN|Gesicki|Burrow to Gesicki caught|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|16:43|CIN|Meyers|Burrow zips to far side caught by Meyers|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|16:53|CIN|unknown|Burrow out of gun, pass complete upended close to first down marker, short|None|unknown|unknown|unknown|Lane|unverified (no DB match; caption-only)|

Offense (model synthesis from this game's plays): Tight end usage and production (multiple TEs catching for first downs and TDs) / Explosive plays including long passes to receivers and TEs / Red zone efficiency with TDs and FGs / Run after catch and broken tackles by skill players

Defense weaknesses: Susceptible to penalties including roughing the passer / Allowing chunk plays to opposing TEs and WRs in passing game / Red zone defense vulnerable to TDs

Limitations: Could not determine specific concepts like run gaps, play-action (except one explicit), personnel, formations, or coverages as they were not explicitly stated by commentators. Many plays had unclear or no exact DB matches due to name mangling and timing. Some yardage and details were approximate or not fully specified in captions. Could not identify all defender names or exact scores on every play.


## Week 5: PHI 17 - JAX 19 (game 401872981)
Video: Philadelphia Eagles vs. Jacksonville Jaguars Game Highlights | 2026 NFL Season Week 5 — https://www.youtube.com/watch?v=WXw2IIj01Sg  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:27|JAX|J.Cameron|Kickoff return for touchdown (nullified by penalties)|90|unknown|unknown|unknown|unknown|verified vs DB|
|01:15|JAX|T.Lawrence|Pass over the middle caught for first down|11|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:30|JAX|T.Lawrence|Loses the ball on sack/fumble, recovered by JAX|0|unknown|unknown|unknown|J.Carter|unverified (no DB match; caption-only)|
|01:41|JAX|P.Washington|Quick throw out in space, pushed out|0|unknown|unknown|unknown|R.Woolen|unverified (no DB match; caption-only)|
|01:50|PHI|J.Hurts|Empty set pass over the middle short of first down|0|unknown|empty|unknown|unknown|unverified (no DB match; caption-only)|
|02:06|PHI|J.Hurts|Pass to D.Goedert, stadium reacts|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:17|PHI|W.Shipley|Swing pass out in space, gain of 7, knocked out of bounds|7|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:32|PHI|J.Hurts|Senses pressure, runs and gets first down|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:46|PHI|W.Shipley|Fourth and one handoff, spins out for first down|0|unknown|unknown|unknown|D.Hamilton|unverified (no DB match; caption-only)|
|03:14|JAX|T.Lawrence|Pass to Hunter for first down near midfield|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:21|JAX|T.Lawrence|Play fake boot, pass to P.Washington who slips tackle and scores TD|51|play-action|unknown|unknown|unknown|verified vs DB|
|03:42|PHI|B.Covey|Kick return, stays in bounds, gets leveled|0|unknown|unknown|unknown|unknown|verified vs DB|
|03:51|PHI|J.Hurts|Pass thrown out of bounds|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:02|PHI|T.Atkinson|Handoff through seam, wrapped up near line to gain|0|unknown|unknown|unknown|Z.Bourne|unverified (no DB match; caption-only)|
|04:13|JAX|B.Strange|Pass underneath short of sticks, fourth down|0|unknown|unknown|unknown|Q.Mitchell|unverified (no DB match; caption-only)|
|04:25|PHI|J.Hurts|Off play action, zips pass over middle to L.Lemieux for first down|0|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:34|PHI|J.Hurts|Pass to D.Goedert for first down|8|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:41|PHI|J.Hurts|Under pressure, gets rid of it to Wicks for first down|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:50|PHI|J.Hurts|Pass to Wicks for first down, gain of 19, first and goal|19|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:01|PHI|J.Hurts|Pass with contact along goal line, PI called on T.Hunter|0|unknown|unknown|unknown|T.Hunter|unverified (no DB match; caption-only)|
|05:19|PHI|W.Shipley|Run up the middle, busts tackle for TD|2|unknown|unknown|unknown|unknown|verified vs DB|
|05:35|JAX|T.Lawrence|Hit and loses ball (fumble)|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:01|PHI|D.Cooper|Deep fade pulled in for TD|62|deep shot|unknown|unknown|unknown|verified vs DB|
|06:19|JAX|T.Lawrence|Pass to J.Meyers for gain of 18 and first down|18|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:28|JAX|T.Lawrence|Pass caught on third down, Washington gets out of bounds|16|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:55|JAX|T.Atkinson|Dump off, breaks tackle, brought down at 21|0|unknown|unknown|unknown|Z.Vaughn|unverified (no DB match; caption-only)|
|07:08|JAX|T.Lawrence|Pocket breaks down, takes off and dragged down short of first down|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:19|JAX|T.Atkinson|Pitch on speed option, dragged for extra yard and first down|0|RPO|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:30|JAX|T.Lawrence|Screen pass over middle to J.Cameron to the 9|0|screen|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:47|JAX|T.Lawrence|Throw on third and short complete for first down|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:49|JAX|B.Strange|Catch, hit, down at the one|0|unknown|unknown|unknown|M.Mukuba|unverified (no DB match; caption-only)|
|07:57|JAX|Rodriguez|Run, hit by Carter, bounces off, may have lost ball|0|unknown|unknown|unknown|J.Carter|unverified (no DB match; caption-only)|
|08:20|JAX|T.Lawrence|Fires to end zone incomplete (intended for B.Thomas)|0|unknown|unknown|unknown|Q.Mitchell|verified vs DB|
|09:10|PHI|B.Covey|Kick return, tackled at 30|22|unknown|unknown|unknown|unknown|verified vs DB|
|09:16|PHI|J.Hurts|Low snap, ball batted in air, recovered by JAX|0|unknown|unknown|unknown|T.Walker|unverified (no DB match; caption-only)|
|09:27|JAX|T.Lawrence|Five-man pressure, pass over middle to J.Cameron|32|unknown|unknown|unknown|unknown|verified vs DB|
|09:40|JAX|T.Atkinson|Screen pass, blockers, knocked down at 27|0|screen|unknown|unknown|C.Dejean|unverified (no DB match; caption-only)|
|09:54|JAX|T.Lawrence|Pass back across body to B.Strange for gain of 13|13|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:08|JAX|T.Lawrence|Pressure, almost intercepted, then FG attempt|0|unknown|unknown|unknown|unknown|verified vs DB|
|10:24|PHI|J.Hurts|Looking deep, pass caught by Wicks for 19 yards|19|unknown|unknown|unknown|T.Hunter|unverified (no DB match; caption-only)|
|10:42|PHI|J.Hurts|Contact, flag for holding/PI on J.Jones|0|unknown|unknown|unknown|J.Jones|unverified (no DB match; caption-only)|
|10:51|PHI|Pierce|Run, hit in backfield for loss|-5|unknown|unknown|unknown|A.Johnson|unverified (no DB match; caption-only)|
|11:03|PHI|J.Hurts|Short throw to Pierce, makes miss but stood up short|0|unknown|unknown|unknown|T.Hunter|unverified (no DB match; caption-only)|
|11:15|PHI|J.Hurts|Fourth and three, slant pass incomplete|0|unknown|unknown|unknown|T.Hunter|unverified (no DB match; caption-only)|
|11:28|JAX|T.Lawrence|Blitzed, steps up, hit, throws deep - intercepted|0|unknown|unknown|unknown|Q.Mitchell|verified vs DB|
|11:41|PHI|J.Hurts|Pass to L.Lemieux across middle for first down, gain of 19|19|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:51|PHI|J.Hurts|Lobs downfield, dropped by Wicks (would have been TD)|0|deep shot|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:24|JAX|T.Lawrence|Step up, shovels ball forward while sacked, ruled incomplete|0|unknown|unknown|unknown|Z.Vaughn|unverified (no DB match; caption-only)|
|12:35|PHI|J.Hurts|Trying to set up screen, miscommunication, fourth down|0|screen|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:45|JAX|T.Lawrence|Dumps off to P.Washington, slips tackle, +15 yards|27|unknown|unknown|unknown|unknown|verified vs DB|
|12:59|JAX|T.Lawrence|Steps up, takes off for first down, gain of 16|16|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:09|JAX|T.Atkinson|Counter run up middle, gain of 12|12|counter|unknown|unknown|C.Dejean|unverified (no DB match; caption-only)|
|13:21|JAX|T.Lawrence|Pass caught inside five, down to one (B.Strange)|27|unknown|unknown|unknown|unknown|verified vs DB|
|13:36|JAX|T.Lawrence|Penalty (delay of game), spikes ball|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:45|JAX|T.Lawrence|Pass to B.Thomas incomplete out of bounds|0|unknown|unknown|unknown|R.Woolen|unverified (no DB match; caption-only)|
|14:05|JAX|T.Lawrence|Another delay of game penalty|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:14|JAX|T.Lawrence|Underneath pass to P.Washington, pushed out at 5|0|unknown|unknown|unknown|Q.Mitchell|unverified (no DB match; caption-only)|
|14:28|JAX|T.Lawrence|Fourth and goal, throws out of back of end zone incomplete|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:39|PHI|J.Hurts|Bad snap, secures it, throws away (possible grounding/safety discussion)|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:02|JAX|P.Washington|Fields punt at 48, cuts up, slips tackle, out of bounds|0|unknown|unknown|unknown|A.Ebiketie|unverified (no DB match; caption-only)|
|15:20|JAX|T.Lawrence|Off play action, complete to J.Meyers|0|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:30|JAX|T.Lawrence|Play action, pass batted at line incomplete|0|play-action|unknown|unknown|A.Epenesa|unverified (no DB match; caption-only)|
|15:37|JAX|T.Lawrence|Deep pass to P.Washington for TD|27|deep shot|unknown|unknown|unknown|verified vs DB|
|16:13|PHI|J.Hurts|Pressure, sandwiched for loss of 10|-10|unknown|unknown|unknown|A.Johnson|unverified (no DB match; caption-only)|
|16:24|PHI|J.Hurts|Check down to D.Goedert for short gain|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|16:40|PHI|Pierce|Run, hit at 30, short of first down|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|16:52|PHI|J.Hurts|Pass to Wicks for 9 yards|9|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|17:01|PHI|J.Hurts|Pass to Wicks for first down|0|unknown|unknown|unknown|T.Hunter|unverified (no DB match; caption-only)|
|17:16|PHI|J.Hurts|Pass over middle to D.Goedert for first down|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|17:28|PHI|J.Hurts|Pass to L.Lemieux, pushed out of bounds|0|unknown|unknown|unknown|J.Lewis|unverified (no DB match; caption-only)|
|17:43|PHI|Pierce|Run, loses yardage but keeps in FG range|-2|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|17:52|PHI|J.Elliott|48 yard field goal is good|48|unknown|unknown|unknown|unknown|verified vs DB|
|18:05|JAX|A.Abdullah|Kickoff return for 53 yards|53|unknown|unknown|unknown|unknown|CONFLICT (yardage 53 vs DB)|
|18:27|JAX|C.Little|57 yard field goal is good to win game|57|unknown|unknown|unknown|unknown|verified vs DB|

Offense (model synthesis from this game's plays): Explosive big plays through the air with Lawrence connecting on 50+ and 20+ yard TDs / Strong red zone efficiency converting first-and-goal situations into scores / Effective screen and short passes converting to first downs and YAC / Mobile QB with scrambling and designed runs/RPOs gaining key first downs

Defense weaknesses: High penalty count including offsetting, holding, delay of game, and pass interference / Special teams inconsistencies with high snaps affecting kicks and returns / Difficulty stopping Eagles run game in short yardage allowing TDs up the middle / Secondary allows deep passes and TDs despite coverage on some plays like the Cooper TD

Limitations: Could not determine specific run gaps/directions, exact personnel formations, or coverage schemes as they were not explicitly stated by commentators except for a few cases like empty set, play-action, screen, and deep shots. Many plays lacked direct DB matches due to name mangling and incomplete details. Some player names corrected only on clear matches (e.g. Washington, Shipley, Lawrence). Several plays had ambiguous or incomplete descriptions from auto-generated captions.


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

Offense (model synthesis from this game's plays): Lawrence distributed explosive passes to Strange, Washington, Meyers and Hunter. / Screens and short throws produced substantial gains: Tuten's 27-yard touchdown, Hunter's slant and throwback screen, and an eight-yard late screen. / Motion and backfield deployments featured in Meyers' third-down conversion, Hunter's throwback screen and Hunter's touchdown. / Rodriguez supplied repeated gains through contact and a red-zone third-down conversion. / Short scoring passes reached Tuten twice and Boerkircher once.

Defense weaknesses: Houston completed gains of 42 yards to Collins and 34 and 50 yards to Noel. / Commentary explicitly called Moreau's first touchdown a blown coverage. / Pass-interference penalties against Hunter and Jaron Jones helped Houston advance on scoring possessions. / A defender failing to leave the field erased a Houston punt and extended the possession that ended with Noel's touchdown. / Jordan found a cutback lane and broke a secondary tackle on his 25-yard touchdown. / Marks was wide open on a late catch-and-run; commentary credited his release with freezing the linebackers.

Limitations: Analysis uses only supplied captions and DB excerpts; no video frames, browsing or commands. The DB excerpt omits many ordinary plays, so NO DB MATCH means no matching supplied line, not that the play did not occur. Caption times identify commentary segments and may include replay discussion. Unmatched garbled names remain unresolved; prior-play fragments and general discussion were not treated as separate plays. Exact gains are null when absent or only approximate; DB yardage takes precedence on clear matches. Field-goal yards are kick distances. The nullified rushing touchdown is not counted as a score. DB tacklers, pressure players, penalty offenders and pass-breakup defenders are labeled in defender_beaten for traceability; their inclusion does not establish they were beaten. Formations and coverage are limited to explicit commentary, with rush counts and partial descriptions distinguished from full schemes. No complete personnel groupings, route combinations, blocking assignments or coverage responsibilities can be established from these captions.
