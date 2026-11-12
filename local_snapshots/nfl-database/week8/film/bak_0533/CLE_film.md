# CLE — Phase 8 film notes (Weeks 1–6, 2026)

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

Offense (Codex synthesis from this game's plays): Produced explosive completions to Jeudy for 20 yards, Concepcion for 25 and Boston for a 46-yard touchdown. / Completed several passes off play fakes, including throws to Fannin and Judkins; Watson also gained six yards on a keep. / Sampson's 37-yard opening return and Sanders's 74-yard return supplied favorable field position.

Defense weaknesses: Allowed four Lawrence touchdown passes, including Washington's 30-yarder after commentary identified defensive miscommunication. / Allowed repeated Washington receptions, including 22 yards with Hickman involved and 15 yards in front of Campbell on third-and-six. / Allowed Tuten's 22-yard screen gain with a missed tackle and a separate 12-yard edge run. / Pressure did not prevent Lawrence from escaping and completing the 32-yard touchdown to Meyers.

Limitations: Captions only; no frames were available. Personnel, routes, blocking assignments, coverage and individual responsibility generally cannot be established. Explicit defensive-front observations are recorded separately from unknown coverage within coverage_scheme. Named defenders include tacklers, pressure players and interceptors; their inclusion does not establish that they were beaten. DB facts control clearly matched plays, including Washington's 22-yard gain and the interception location. The interception entry's yards describe the return; field-goal yards describe kick distance. Unmatched gains remain null unless commentary supplies yardage. Names absent from clearly matching DB entries remain as recognizable caption renderings; the first Tuten entry contains a transcription spacing artifact. The early Watson fumble has no matching supplied DB entry and no established recovery. The supplied DB is selective, so NO DB MATCH does not establish that a play did not occur. DB-only kickoffs and returns without identifiable caption calls are omitted. Extra points are not separately called in these captions. The drop-man/three-man-rush comment appears immediately before the final first-half deep attempt, but edited-caption timing limits certainty about its attachment.


## Week 2: CLE 23 - TB 19 (game 401872935)
Video: Cleveland Browns vs Tampa Bay Buccaneers Game Highlights — https://www.youtube.com/watch?v=Q5PgGZKMUqk  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:15|CLE|Deshaun Watson / Concepcion|Completion near the first-down marker while Watson throws on the run; Winfield tackles.|None|play-action|unknown|unknown|Winfield (tackler)|unverified (no DB match; caption-only)|
|00:26|CLE|Concepcion|Jet sweep stopped for a loss by Yaya Diaby.|None|jet sweep|Jones as extra offensive lineman; Concepcion in motion|unknown|unknown|unverified (no DB match; caption-only)|
|00:40|CLE|Judkins|Handoff gains a couple of yards; flag thrown.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:49|TB|Chris Godwin|Gets outside and into Cleveland territory before Denzel Ward tackles.|None|unknown|unknown|unknown|Denzel Ward (tackler)|unverified (no DB match; caption-only)|
|01:04|TB|Baker Mayfield / Otton|Mayfield steps up and completes a pass on the run to Otton outside, short of the first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:14|TB|C. McLaughlin|Makes a 59-yard field goal.|59|field goal|unknown|unknown|unknown|verified vs DB|
|01:26|CLE|Judkins|Runs up the middle for close to 10 yards; Josiah Trotter tackles.|None|run up middle|unknown|unknown|Josiah Trotter (tackler)|unverified (no DB match; caption-only)|
|01:39|CLE|Deshaun Watson / H. Fannin|Short-left completion to Fannin, who is pushed out of bounds.|21|short-left pass|unknown|unknown|A. Anzalone; A. Winfield (DB tacklers)|verified vs DB|
|01:50|CLE|unknown|Quick completion with Fannin blocking; receiver moves the pile but appears short of the first down.|None|quick pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:01|CLE|A. Szmyt|Makes a 50-yard field goal.|50|field goal|unknown|unknown|unknown|verified vs DB|
|02:11|TB|B. Irving|Breaks into Cleveland territory on a left-end run; C. Schwesinger tracks him down.|38|left-end run|Gainwell in motion|unknown|C. Schwesinger (DB tackler)|verified vs DB|
|02:26|TB|unknown|Pass goes off the intended receiver's fingertips, bringing up fourth down.|None|unknown|Gainwell in wing position|unknown|unknown|unverified (no DB match; caption-only)|
|02:35|TB|C. McLaughlin|Makes a 45-yard field goal for a 6-3 lead.|45|field goal|unknown|unknown|unknown|verified vs DB|
|02:47|CLE|unknown|Fragmentary play description praises Tampa Bay's strong pursuit; ball carrier and result are unclear.|None|unknown|I formation|unknown|unknown|unverified (no DB match; caption-only)|
|02:56|CLE|Deshaun Watson / Fannin|Third-down rollout pass underneath is dropped by Fannin.|None|rollout; underneath pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:10|TB|Baker Mayfield|Escapes pressure to the right and runs to the first-down marker; flag thrown and final enforcement unclear.|None|scramble right|Egbuka in motion|pressure coming; scheme unknown|unknown|unverified (no DB match; caption-only)|
|03:26|TB|B. Mayfield|Play-action throw deep left intended for T. Hurst is intercepted by M. Harden, who returns it 25 yards.|25|play-action; deep-left pass|unknown|unknown|unknown|verified vs DB|
|03:38|CLE|Deshaun Watson|Sacked at the 21-yard line by David Walker.|None|unknown|motion mentioned; player unspecified|unknown|unknown|unverified (no DB match; caption-only)|
|03:47|CLE|A. Szmyt|Makes a 34-yard field goal to tie the game 6-6.|34|field goal|unknown|unknown|unknown|verified vs DB|
|03:59|TB|B. Mayfield / T. Hurst|Third-down completion left to Hurst for a first down.|21|deep-left pass|Godwin in motion|unknown|T. Campbell (DB tackler)|verified vs DB|
|04:12|TB|Irving|Stopped for a one-yard loss by Derrick Barnette, as transcribed.|-1|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:20|TB|Baker Mayfield|Tripped and taken down while trying to escape; Ronnie Hickman is credited in commentary.|None|unknown|motion mentioned; player unspecified|unknown|unknown|unverified (no DB match; caption-only)|
|04:31|CLE|Deshaun Watson|Keionte Scott sacks Watson inside the 5-yard line against a blitz.|None|unknown|Sanders motions into backfield|blitz|unknown|unverified (no DB match; caption-only)|
|04:44|CLE|Sanders|Handoff and dive forward to the 7-yard line; Scott and Winfield tackle.|None|unknown|unknown|unknown|Scott; Winfield (tacklers)|unverified (no DB match; caption-only)|
|04:52|TB|Baker Mayfield / Otton|Near-side pass to Otton, who loses the ball; commentary says officials ruled a catch, but recovery and final outcome are not supplied.|None|unknown|empty backfield|unknown|unknown|unverified (no DB match; caption-only)|
|05:01|TB|Baker Mayfield|Flushed out and sacked on third-and-15; Mason Graham receives sack credit.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:14|CLE|Deshaun Watson / Concepcion|Underneath completion short of the first down; McCollum tackles.|None|underneath pass|unknown|unknown|McCollum (tackler)|unverified (no DB match; caption-only)|
|05:23|CLE|Judkins|Handoff stopped by a pile of defenders.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:31|TB|Gainwell|Runs for a first down; Tyson Campbell and Sam Williams miss before Schwesinger tackles.|None|unknown|unknown|unknown|Tyson Campbell; Sam Williams|unverified (no DB match; caption-only)|
|05:46|TB|Baker Mayfield / Tez Johnson|Third-and-12 pass toward the goal line falls incomplete; commentary mentions contact.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:55|TB|C. McLaughlin|Makes a 31-yard field goal with 12 seconds left in the half.|31|field goal|unknown|unknown|unknown|verified vs DB|
|06:04|TB|B. Mayfield / C. Godwin|Godwin advances past midfield to approximately the Cleveland 41-yard line on the opening second-half possession.|24|deep-right pass|unknown|unknown|N. Igbinoghene (DB tackler)|verified vs DB|
|06:17|TB|Irving|Cuts back left; commentary also credits Mayfield with helping gain extra yards to the 26-yard line.|None|cutback left|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:29|TB|unknown|Fragmentary second-down play; Isaiah McGuire is named in coverage, but target and result are missing.|None|unknown|Otton in motion|unknown|unknown|unverified (no DB match; caption-only)|
|06:41|TB|Baker Mayfield|Runs left from the pocket for an apparent first down; Delpit hits him.|None|scramble left|Egbuka in motion|unknown|Delpit (tackler)|unverified (no DB match; caption-only)|
|06:52|TB|B. Mayfield / E. Egbuka|Under pressure after a play fake, Mayfield throws left to Egbuka for a sliding touchdown catch.|5|play-action; short-left pass|unknown|pressure mentioned; scheme unknown|unknown|verified vs DB|
|07:22|CLE|Deshaun Watson|Keeps the ball and runs for a first down across the 30; Keionte Scott tackles.|None|quarterback keeper|three-point stance mentioned; personnel unspecified|unknown|Keionte Scott (tackler)|unverified (no DB match; caption-only)|
|07:33|CLE|Deshaun Watson / Boston|Boston completes a sideline catch with both feet in bounds against McCollum.|None|unknown|unknown|unknown|McCollum (in coverage)|unverified (no DB match; caption-only)|
|07:44|CLE|Concepcion|Catches a pass for a first down with Tampa Bay showing blitz.|None|unknown|unknown|showing blitz; actual rush unknown|unknown|unverified (no DB match; caption-only)|
|07:53|CLE|unknown|Pass to the left is mentioned, but the receiver and result are unintelligible.|None|pass left|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:04|CLE|Deshaun Watson / Boston|Boston initially has the third-down pass, but Morrison knocks it away for an incompletion.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:22|CLE|A. Szmyt|Makes a field goal; captions say 33 yards, while the DB records 34.|34|field goal|unknown|unknown|unknown|verified vs DB|
|08:29|TB|Baker Mayfield / unknown|Pass after a play fake is incomplete despite an attempted one-handed catch.|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:38|TB|Baker Mayfield / Tez Johnson|On third-and-15, Mayfield has time but overthrows Johnson downfield.|None|downfield pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:48|CLE|Deshaun Watson / Fannin|Watson rolls out after a play fake and dumps the ball to Fannin; Anzalone misses him.|None|play-action; rollout; dump-off|unknown|unknown|Anzalone|unverified (no DB match; caption-only)|
|09:03|CLE|D. Watson / D. Boston|Short-middle completion; Boston makes an unnamed defender miss and runs for a 55-yard touchdown.|55|short-middle pass; run after catch|unknown|unknown|unknown|verified vs DB|
|09:29|CLE|Deshaun Watson|Rolls the pocket, directs traffic, then runs out of bounds with Anzalone escorting him; precise play context is unclear.|None|rollout; scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:44|TB|Baker Mayfield / Chris Godwin|Underneath completion to Godwin for 14 yards and a first down; Delpit in coverage.|14|underneath pass|unknown|unknown|Delpit (in coverage)|unverified (no DB match; caption-only)|
|09:55|TB|B. Mayfield / T. Johnson|Mayfield slips but completes a deep-middle pass to Johnson, who beats Tyson Campbell and reaches the Cleveland 21.|49|deep-middle pass|unknown|unknown|Tyson Campbell|verified vs DB|
|10:09|TB|Baker Mayfield|On third-and-two, eludes pressure and throws incomplete to the back of the end zone.|None|end-zone pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:21|TB|C. McLaughlin|Makes a 31-yard field goal to put Tampa Bay ahead 19-16; commentary notes Denzel Ward's near blocks.|31|field goal|unknown|unknown|unknown|verified vs DB|
|10:28|CLE|unknown|Ball carrier splits the defense and hurdles a defender on a first-down gain to the 45; Trotter is mentioned.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:42|CLE|Deshaun Watson / Boston|Completion right to Boston for a first down in front of McCollum near Tampa Bay's 40 or 41.|None|pass right|unknown|unknown|McCollum (in coverage)|unverified (no DB match; caption-only)|
|10:49|CLE|D. Watson / B. Whiteheart|On third-and-two, Whiteheart slips wide open after a play fake and scores; commentary credits his balance and Jerry Jeudy's blocking.|17|play-action; short-left pass|unknown|unknown|unknown|verified vs DB|
|11:37|TB|Baker Mayfield / Chris Godwin|Completion left to Godwin for a first down in front of Myles Harden. A subsequent loose-ball remark does not establish a turnover.|None|pass left|unknown|unknown|Myles Harden (in coverage)|unverified (no DB match; caption-only)|
|11:46|TB|Irving|Runs over the left side for a first down; ending yard line is garbled.|None|run left|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:59|TB|Baker Mayfield / unknown|Slant completed on a sliding catch with less than a minute remaining.|None|slant|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:04|TB|Baker Mayfield / Hurst|Throw left initially reaches Hurst but comes out of his hands for an incompletion.|None|pass left|shotgun|unknown|unknown|unverified (no DB match; caption-only)|
|12:18|TB|Baker Mayfield|Under pressure on third-and-14, escapes right, stiff-arms a defender, then is wrapped up and taken down.|None|scramble right|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:33|TB|Baker Mayfield / unknown|Fourth-down throw to the end zone falls incomplete, ending Tampa Bay's final opportunity.|None|end-zone pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:48|CLE|unknown|Kneeldown ends the game.|None|kneeldown|victory formation|unknown|unknown|unverified (no DB match; caption-only)|

Offense (Codex synthesis from this game's plays): Play-action produced Fannin's later dump-off with an Anzalone miss and Whiteheart's decisive 17-yard touchdown. / Boston supplied sideline and first-down catches plus a 55-yard touchdown after making a defender miss. / Watson's keeper and Concepcion's reception produced first downs during the second-half scoring sequence.

Defense weaknesses: Allowed Irving's 38-yard left-end run and another late first-down run left. / Campbell and Sam Williams missed tackles on Gainwell's first-down run. / Allowed Hurst's 21-yard catch, Godwin's 24-yard catch and Johnson's 49-yard reception; commentary explicitly says Johnson beat Campbell. / Godwin repeatedly supplied first-down receptions, including a 14-yard underneath gain with Delpit in coverage.

Limitations: Captions only; no video frames were viewed and no commands were run. The supplied DB is a selected-play list, so NO DB MATCH does not mean a play did not occur. DB matches contain the requested quarter and clock identifier. Formation and coverage details were not inferred from DB shotgun labels; only explicit commentary details are included. Named tacklers or coverage defenders are labeled as such and do not necessarily indicate a defender was beaten. Null yards indicate an undetermined gain, including incompletions; interception yards represent return distance and field-goal yards represent kick distance. Fragmentary passages leave some players, outcomes, penalties, and possible replay boundaries uncertain. The Otton loose-ball sequence does not establish a turnover. Kickoff returns listed in the DB were not described in the captions and are not included. Extra points are documented in the DB but not separately identifiable in these captions.


## Week 3: CAR 18 - CLE 21 (game 401872949)
Video: Carolina Panthers vs. Cleveland Browns Game Highlights | NFL 2026 Season Week 3 — https://www.youtube.com/watch?v=EyGW6pqjIgs  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 4: PIT 24 - CLE 27 (game 401872964)
Video: Pittsburgh Steelers vs Cleveland Browns Game Highlights | 2026 NFL Season Week 4 — https://www.youtube.com/watch?v=qJn2zHTs9BY  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 5: CLE 12 - NYJ 17 (game 401872983)
Video: Cleveland Browns vs New York Jets Game Highlights | 2026 NFL Season Week 5 — https://www.youtube.com/watch?v=p_DHFA3Sfys  | captions: yes

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

Offense (Codex synthesis from this game's plays): Jeudy supplied repeated first-down receptions, including a 14-yard sliding catch and the decisive 33-yard gain. / Concepcion contributed middle-field completions, including a first down on first-and-15 and a 15-yard third-down conversion. / Burton converted a short-yardage carry, and Estime finished the tying drive with a 2-yard touchdown.

Defense weaknesses: Baltimore found early rushing gains through Henry and a substantial Huntley scramble near the goal line. / Lane repeatedly moved the chains, including on third downs. / Cuevas was open for the fourth-down play-action touchdown and later gained 29 yards on a short right pass. / Huntley escaped pressure to produce Flowers' 31-yard reception.

Limitations: Analysis uses only the supplied captions and DB excerpt; no video frames or commands were used. The DB excerpt is selective, so NO DB MATCH does not mean a play did not occur. No personnel grouping, formation, or coverage scheme is explicitly stated in the commentary; all are unknown, including plays whose DB text says shotgun. Rush counts do not establish coverage. Defender_beaten records named tacklers, pursuers, or pass defenders where available and does not necessarily mean they lost coverage. Some names remain caption spellings because no matching DB play permits correction. Null yards indicate an unstated or uncertain gain; the 10-yard Lane catch and 8-yard Concepcion catch are inferred from stated field position or distance remaining. Henry's fumble entry uses the underlying 5-yard rushing gain rather than the DB turnover summary's 0-yard recovery value. Kick distances are attempt lengths. The adjacent Lane catches at 01:06 and 01:12 are listed separately because the captions introduce a new third-and-six, although an edited replay cannot be ruled out. Several calls cut off before their outcomes, and penalty enforcement is sometimes omitted. The initial blocked kick was nullified and is separate from the winning field goal. Kickoffs and returns present only in the DB are excluded because the captions do not identify them.
