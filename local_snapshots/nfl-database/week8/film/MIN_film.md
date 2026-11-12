# MIN — Phase 8 film notes (Weeks 1–6, 2026)
> Note: games 401872959, 401872974, 401872987 were extracted by Grok via the xAI API (grok-4.20-0309-non-reasoning, same prompt/schema as Codex, cleaned captions); sidecar provenance in film/grok_meta/. All other games with notes: Codex.

Method: NFL YouTube channel full-game highlight videos were located by search and their auto-captions (broadcast commentary) downloaded via yt-dlp. Codex (codex-cli 0.163.0) extracted plays from the captions. **No video frames were viewed by any agent.** Each play was checked against the repo DB play-by-play: `verified vs DB` means the cited DB play exists and the yardage matches. Personnel, formation and coverage appear only when commentators stated them; everything else is `unknown`.


## Week 1: GB 22 - MIN 39 (game 401872927)
Video: Green Bay Packers vs. Minnesota Vikings Game Highlights | NFL 2026 Season Week 1 — https://www.youtube.com/watch?v=d6wKdU-5kME  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:21|MIN|Kyler Murray|Deep pass intended for Jauan Jennings is intercepted by Keisean Nixon. Commentary identifies double coverage and pressure from Zaire Franklin. Nixon returns it 11 yards.|11|deep right pass|shotgun|double coverage|unknown|verified vs DB|
|00:38|GB|Chris Brooks|Runs for a first down to Minnesota's 39, following a blocker captioned as Monk on the right.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:50|GB|Jordan Love|Rolls on third-and-12 and throws out of bounds off his back foot.|0|rollout|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:00|GB|Trey Smack|Makes a 59-yard field goal.|59|field goal|unknown|unknown|unknown|verified vs DB|
|01:09|MIN|Justin Jefferson|Makes a difficult catch from Murray on third-and-four.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:24|MIN|Kyler Murray|Escapes around the edge and gains six yards, adding yardage with a late move.|6|quarterback scramble around edge|shotgun|unknown|unknown|unverified (no DB match; caption-only)|
|01:39|MIN|T.J. Hockenson|Catches a tight end screen on third-and-17 and reaches approximately the 45, leaving fourth-and-10.|None|tight end screen|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:54|GB|Christian Watson|Turns Love's first completion into an 81-yard touchdown, racing down the sideline. Commentary credits 60 yards after the catch and Matthew Golden's legal side-contact block; a flag is picked up.|81|deep middle pass|unknown|unknown|unknown|verified vs DB|
|02:49|GB|Trey Smack|Misses the extra point wide right after Watson's touchdown.|None|extra point|unknown|unknown|unknown|verified vs DB|
|03:00|MIN|Kyler Murray|Scrambles and takes a collision, then clutches his left knee. An unnecessary-roughness penalty adds 15 yards; commentary identifies Bullard.|None|quarterback scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:27|MIN|Justin Jefferson|Catches a pass for a first down on third-and-six.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:38|MIN|Carson Wentz|Has time against a four-man rush but misses an open Jordan Addison on third-and-five at the 20.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:49|MIN|Will Reichard|Makes a 38-yard field goal despite a Packers rusher nearly reaching the kick.|38|field goal|unknown|unknown|unknown|verified vs DB|
|04:08|GB|Bo Melton|Returns the kickoff 59 yards to Minnesota's 40 before James Pierre forces him out.|59|kickoff return|unknown|unknown|James Pierre (DB credited tackler)|CONFLICT (yardage 59 vs DB)|
|04:23|GB|unknown|A left tackle misses his block and Pace makes a tackle in the backfield. The ballcarrier and loss are not identified.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:26|GB|Christian Watson|Catches a pass for a first down at approximately Minnesota's 27.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:35|GB|unknown|Right-side completion on third-and-nine is stopped short of the first down. Commentary names a defender captioned as Rogers.|None|right-side pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:46|GB|Trey Smack|Makes a 43-yard field goal, giving Green Bay scores on its first three drives.|43|field goal|unknown|unknown|unknown|verified vs DB|
|05:00|MIN|Justin Jefferson|Makes a catch on third-and-eight. Commentary discusses a possible hit to the quarterback's head.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:20|MIN|T.J. Hockenson|Holds onto a catch with two defenders nearby for another conversion.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:34|MIN|Justin Jefferson|Catches Wentz's 39-yard touchdown on a free play caused by Lukas Van Ness being offside. Commentary describes a one-on-one matchup against an unnamed rookie.|39|deep left shot on free play|unknown|one-on-one matchup; overall scheme unknown|unknown|verified vs DB|
|06:26|GB|Tucker Kraft|Makes a catch and run for 23 yards. Captions call the throw down the middle; the DB records short left.|23|short left pass|unknown|unknown|Byron Murphy (DB credited tackler)|verified vs DB|
|06:35|GB|Tucker Kraft|Commentary retrospectively identifies an earlier 30-yard reception; the original play call is absent from the supplied captions.|30|deep left pass|unknown|unknown|Byron Murphy (DB credited tackler)|verified vs DB|
|06:41|GB|Bo Melton|Catches Love's pass under pressure from Turner with 41 seconds remaining in the half. Love takes a hit after releasing.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:55|GB|Christian Watson|Makes a 32-yard deep catch to Minnesota's seven despite defensive pass interference by Byron Murphy; the penalty is declined.|32|deep left pass|unknown|unknown|Byron Murphy|verified vs DB|
|07:15|GB|Christian Watson|Catches a two-yard touchdown. Commentary says defensive backs look into the backfield, allowing Watson to slip behind them.|2|short right pass|unknown|unknown|unknown|verified vs DB|
|07:44|MIN|unknown|A handoff is mentioned immediately before halftime; the runner and result are unidentified.|None|handoff run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:58|GB|Matthew Golden|Catches a 13-yard pass thrown by Love on the run.|13|pass on the run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:23|GB|Jayden Reed|Makes a first-down catch after commentary notes four consecutive running plays.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:39|GB|Jonnu Smith|Gains 43 yards on a reception to Minnesota's seven. Isaiah Rodgers recovers ground to prevent a touchdown.|43|deep right pass|unknown|unknown|Isaiah Rodgers (recovery tackler)|verified vs DB|
|08:54|GB|Jordan Love|Misses Reed near the goal line as Van Ginkel and Cashman force a quick throw.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:06|GB|Trey Smack|Makes a 26-yard field goal to extend the lead to 22-10.|26|field goal|unknown|unknown|unknown|verified vs DB|
|09:28|MIN|M. Price|Returns the kickoff 68 yards to Green Bay's 28. Commentary calls attention to DeeJay Dallas during the return.|68|kickoff return|unknown|unknown|K. Welch (DB credited tackler)|CONFLICT (yardage 68 vs DB)|
|09:49|MIN|Josh Oliver|Catches a quick pass after the long kickoff return.|None|quick pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:08|MIN|T.J. Hockenson|Catches Wentz's 16-yard touchdown inside. Commentary says space is cleared in the middle for Hockenson.|16|deep middle pass|unknown|unknown|unknown|verified vs DB|
|10:42|GB|Matthew Golden|Catches a jump pass from Love and makes a move after the catch.|None|jump pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:51|GB|Matthew Golden|Catches Love's pass on second-and-20 and cuts through the defense for 42 yards to Minnesota's 26.|42|deep middle pass|unknown|unknown|Josh Metellus (DB credited tackler)|verified vs DB|
|11:16|GB|Jordan Love|Pass intended for Golden is deflected and nearly intercepted. Harrison Smith is identified contesting the coverage.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:26|GB|Trey Smack|Commentary retrospectively refers to taking points off the board before the fourth-down attempt. The DB identifies a made 40-yard field goal nullified by Dallas Turner's offside penalty.|40|field goal nullified by penalty|unknown|unknown|unknown|verified vs DB|
|11:33|GB|Jordan Love|Fourth-down attempt comes up short according to the initial spot. Subsequent commentary discusses a tush push and identifies the situation as fourth-and-one; captions mangle the action as a 'kick by Love.'|None|tush push / quarterback sneak|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:51|MIN|T.J. Hockenson|Makes a first-down reception. Commentary mentions contact to the helmet and subsequently references two third-down penalties.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:04|MIN|Jordan Mason|Breaks into the secondary for 28 yards to Green Bay's 11 and is tackled by Evan Williams. Commentary credits help from two tight ends without specifying the formation.|28|left end run|unknown|unknown|Evan Williams (DB credited tackler)|verified vs DB|
|12:17|MIN|Carson Wentz|Throws an apparent end-zone interception with Jefferson described as one-on-one outside. A defensive penalty on number 29, identified as McKinney, gives Minnesota an automatic first down; the interception does not stand.|None|end-zone pass|unknown|one-on-one matchup; overall scheme unknown|unknown|unverified (no DB match; caption-only)|
|12:45|MIN|Aaron Jones|Scores from three yards on a toss around the left end. Commentary credits edge blocking, including Jennings coming down to block.|3|toss left / left end run|unknown|unknown|unknown|verified vs DB|
|13:34|MIN|Justin Jefferson|Catches Wentz's two-point conversion at the back of the end zone after Wentz escapes pressure.|None|scramble-extension pass|unknown|unknown|unknown|verified vs DB|
|14:03|GB|Jordan Love|Is hit on second-and-13 and loses the ball. Commentary credits Dallas Turner with creating the disruption and mentions a smart recovery without clearly identifying the recovering player. This precedes the separate third-down turnover.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:13|GB|Jordan Love|On third-and-17, is sacked for a 12-yard loss by Andrew Van Ginkel and Blake Cashman. Van Ginkel forces and recovers the fumble, returning it seven yards to Green Bay's one.|-12|unknown|unknown|unknown|unknown|verified vs DB|
|14:33|MIN|Jordan Mason|Scores a one-yard rushing touchdown despite Wentz falling during the exchange. Replay commentary says Mason powers through Xavier McKinney and reaches across as Franklin closes. Green Bay's offside penalty is declined.|1|right guard run|unknown|unknown|Xavier McKinney|verified vs DB|
|15:30|GB|Jordan Love|Pass intended for Watson is intercepted by James Pierre after a Harrison Smith deflection. Pierre returns it 28 yards to Green Bay's 14.|28|short middle pass|unknown|unknown|Jordan Love (DB credited return tackler)|verified vs DB|
|15:46|MIN|Justin Jefferson|Catches a short right pass on third-and-five and dives through the air to the pylon for a nine-yard touchdown.|9|short right pass|unknown|unknown|unknown|verified vs DB|
|16:29|GB|Christian Watson|Catches a pass down the middle on second-and-10 late in the game.|None|middle pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|16:36|GB|Matthew Golden|Makes a 20-yard first-down reception on second-and-15. Love takes a heavy hit from Dallas Turner after releasing.|20|deep right pass|unknown|unknown|James Pierre (DB credited tackler)|verified vs DB|
|16:57|GB|Jonnu Smith|Is tackled by Harrison Smith on a late play immediately before the two-minute warning; the action leading to the tackle and yardage are omitted.|None|unknown|unknown|unknown|Harrison Smith (credited tackler in commentary)|unverified (no DB match; caption-only)|
|17:00|GB|unknown|A late pass intended for Skyy Moore is unsuccessful, ending Green Bay's possession on a fourth-down stop.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|

Offense (model synthesis from this game's plays): Jefferson made multiple third-down catches, scored twice, and caught the successful two-point conversion. / Hockenson contributed conversions and a 16-yard touchdown into space cleared in the middle. / The fourth-quarter running game produced Mason's 28-yard gain, Jones's edge touchdown, and Mason's one-yard score through contact. / Wentz exploited an offside free play with a deep touchdown to Jefferson and extended the two-point play before completing it.

Defense weaknesses: Allowed multiple explosive passes to four different Green Bay targets, including Watson's 81-yard touchdown with 60 yards after the catch. / Defensive backs' attention to the backfield allowed Watson to slip behind them for his short touchdown. / Murphy committed pass interference on Watson's 32-yard catch; the completion stood with the penalty declined. / Turner's offside penalty on a made fourth-quarter field goal gave Green Bay an opportunity to continue its possession.

Limitations: Analysis uses only the supplied captions and DB excerpt; no video frames or external sources were consulted. The DB excerpt is selective, so NO DB MATCH does not mean a play did not occur. Caption timestamps mark the relevant call or retrospective reference, not game time. Personnel and formations remain unknown unless explicitly stated in commentary; DB shotgun labels alone were not used for that field. One-on-one and double coverage describe stated matchups, not a verified full defensive scheme. Named DB tacklers are labeled as such and are not necessarily defenders beaten in coverage. Yards on interception entries are return yards; the sack-fumble entry uses the offensive loss and states the separate return in its description. Field-goal yards are kick distances. Null yards indicate unavailable or inapplicable yardage. Several names, play transitions, penalties, and late-game actions are garbled or incomplete. The nullified interception and field goal are not counted as a turnover or score. Generic references to earlier running plays and the final snap lack enough detail to enumerate individual plays.


## Week 2: MIN 9 - CHI 3 (game 401872937)
Video: Minnesota Vikings vs. Chicago Bears Game Highlights | NFL 2026 Season Week 2 — https://www.youtube.com/watch?v=hwqFHBP3_VM  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:20|MIN|Justin Jefferson|Adjusts to catch Wentz's deep pass; pushed out by Tyrique Stevenson.|30|deep left pass|unknown|unknown|T.Stevenson (DB tackler)|verified vs DB|
|00:28|MIN|T.J. Hockenson|Catches Wentz's third-down pass for a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:34|MIN|Carson Wentz|Steps up on third-and-six and throws incomplete toward Jefferson in the end zone; Thieneman is there.|0|end-zone pass|unknown|unknown|Thieneman (coverage; pass incomplete)|unverified (no DB match; caption-only)|
|00:42|MIN|Will Reichard|Makes a 35-yard field goal to finish Minnesota's opening drive.|35|field goal|unknown|unknown|unknown|verified vs DB|
|00:54|CHI|Caleb Williams|Recovers a fumbled snap and runs into Minnesota territory; caption cuts off before the result.|None|run after fumbled snap|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:14|CHI|Caleb Williams|Escapes pressure, directs traffic, makes a defender miss and runs out inside the 35 for four yards.|4|scramble|unknown|five-man pressure|unknown|unverified (no DB match; caption-only)|
|01:31|CHI|Cairo Santos|Makes a 50-yard field goal after a high snap.|50|field goal|unknown|unknown|unknown|verified vs DB|
|01:45|MIN|Carson Wentz|Snap from Blake Brandel goes through his hands on third-and-short; Wentz recovers at the 12.|None|fumbled snap|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:55|CHI|Caleb Williams|Steps up against pressure and throws deep middle toward Luther Burden; Byron Murphy intercepts and returns minus one yard.|-1|deep middle pass|unknown|pressure; exact scheme unknown|B.Murphy (interceptor); R.Odunze (DB return tackler)|verified vs DB|
|02:11|MIN|Carson Wentz|Protection picks up Chicago's blitz, but the pass toward Addison is incomplete.|0|unknown|unknown|blitz|unknown|unverified (no DB match; caption-only)|
|02:19|CHI|unknown|Pass is not caught after Minnesota shows everyone at the line and drops some defenders; receiver and covering defender's names are garbled.|0|unknown|unknown|all-at-line presentation with defenders dropping; exact scheme unknown|unknown|unverified (no DB match; caption-only)|
|02:32|MIN|Justin Jefferson|Catches a pass for 16 yards and a first down with flags down; commentary says the penalty is against Chicago.|16|unknown|unknown|all-at-line presentation; post-snap coverage unknown|unknown|unverified (no DB match; caption-only)|
|02:44|MIN|Jones|Runs for a first-down gain described as seven or eight yards.|None|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:52|MIN|Claiborne (caption identification)|Receives Wentz's third-and-long dump-off against pressure; T.J. Edwards trips him up short of a first down. Commentary says the tackle potentially saved a touchdown.|None|dump-off pass|unknown|blitz|T.J. Edwards (successful tackler)|unverified (no DB match; caption-only)|
|03:01|MIN|Will Reichard|Makes a 49-yard field goal for a 6-3 lead.|49|field goal|unknown|unknown|unknown|verified vs DB|
|03:15|CHI|unknown|Third-down play mentions a player transcribed as 'Marcus Freeman'; the action and result are cut off.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:20|CHI|Swift|Catches a pass out of the backfield after Loveland motions away, loses his footing, gets up and reaches a first down.|None|pass to running back out of backfield|Loveland motions away; personnel grouping unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:33|CHI|Caleb Williams|With nothing open downfield, is hit while throwing an incompletion; Dallas Turner and Jalen Redmond close in.|0|unknown|unknown|unknown|Dallas Turner; Jalen Redmond (pressure defenders)|unverified (no DB match; caption-only)|
|03:48|MIN|Aaron Jones|Lowers his shoulder against Thieneman and gains eight yards to the 28.|8|run; direction unknown|unknown|unknown|Thieneman|unverified (no DB match; caption-only)|
|04:03|MIN|Carson Wentz|Initially has time, but receivers are covered downfield and Austin Booker sacks him.|None|unknown|unknown|unknown|Austin Booker (sacker)|unverified (no DB match; caption-only)|
|04:13|CHI|Caleb Williams|Dallas Turner reaches him and Andrew Van Ginkel finishes the sack near the end of the first half.|None|unknown|unknown|unknown|Dallas Turner; Andrew Van Ginkel (sack defenders)|unverified (no DB match; caption-only)|
|04:28|CHI|D'Andre Swift|Runs for 13 yards near midfield on his first carry of the second half.|13|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:44|CHI|Caleb Williams|Waits for a receiver to come open, then runs for a first down.|None|scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:53|CHI|Monangai|Breaks free for a 15-yard run.|15|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:05|CHI|Monangai|Finds room for 11 yards and a first down inside the 15.|11|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:13|CHI|Kalif Raymond|Catches a first-down pass after Williams escapes Dallas Turner and extends the play.|None|extended-play pass|unknown|pressure; exact scheme unknown|Dallas Turner (evaded by quarterback)|unverified (no DB match; caption-only)|
|05:27|CHI|D'Andre Swift|Runs right tackle from the Minnesota 1 for no gain and fumbles. Jalen Redmond forces it; Isaiah Rodgers recovers for Minnesota.|0|right tackle run|unknown|unknown|J.Redmond; I.Pace (DB tacklers); I.Rodgers (recovery)|verified vs DB|
|05:38|MIN|Aaron Jones|Finds room through right tackle and crosses the 20 on a 20-yard gain to the Minnesota 24.|20|right tackle run|unknown|unknown|T.Stevenson; X.Woods (DB tacklers)|verified vs DB|
|05:46|MIN|Carson Wentz|Goes down on a third-and-two pass play with a flag thrown; Odeyingbo is named. Penalty outcome is omitted.|None|unknown|unknown|unknown|Odeyingbo (defender reaching quarterback)|unverified (no DB match; caption-only)|
|06:03|CHI|Caleb Williams|Scrambles on third-and-five, spins away with Van Ginkel pursuing and gains a first down.|None|scramble|unknown|unknown|Van Ginkel|unverified (no DB match; caption-only)|
|06:10|CHI|Raymond|Is dropped by Metellus on a third-and-ten pass play with a flag down; penalty outcome is omitted.|None|unknown|unknown|all-at-line presentation; post-snap coverage unknown|Metellus (successful tackler)|unverified (no DB match; caption-only)|
|06:18|MIN|DeeJay Dallas|Takes Wentz's dump-off with blockers ahead; T.J. Edwards tackles him one yard short of a first down.|None|dump-off pass|unknown|unknown|T.J. Edwards (successful tackler)|unverified (no DB match; caption-only)|
|06:33|CHI|D'Andre Swift|Takes a short-left screen for 32 yards to the Minnesota 32, staying on his feet through the run.|32|screen left|unknown|unknown|E.Wilson (DB tackler)|verified vs DB|
|06:42|CHI|Rome Odunze|Catches Williams's pass for 15 yards and a first down after a fake to Monangai and quarterback movement.|15|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:54|CHI|Monangai|Runs straight ahead on third down, lowers his pads and is stopped one yard short.|None|straight-ahead run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:01|CHI|Monangai|Gets just enough on the ensuing fourth-down run to convert.|None|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:13|CHI|Caleb Williams|Keeps the ball on a boot after a fake; Van Ginkel trips him up. Williams is in pain afterward and Bagent replaces him.|None|bootleg keeper|unknown|unknown|Van Ginkel (successful tackler)|unverified (no DB match; caption-only)|
|07:40|CHI|Tyson Bagent|Rolls out and dumps off a pass for one yard to the 5; receiver and tackler names are garbled.|1|rollout dump-off|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:51|CHI|Cairo Santos|Isaiah Rodgers blocks the 23-yard field goal off the edge; Chicago's T.Taylor recovers at the Minnesota 12.|0|field goal; edge block|unknown|unknown|I.Rodgers (kick blocker)|verified vs DB|
|08:01|MIN|Jordan Addison|Catches Wentz's pass against a blitz on third-and-five for 14 yards and a first down across the 30.|14|unknown|unknown|blitz|unknown|unverified (no DB match; caption-only)|
|08:19|MIN|T.J. Hockenson (commentator's correction)|Catches a pass for a stated 20 yards into Chicago territory; initially called Josh Oliver before the commentator corrects himself.|20|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:26|MIN|Aaron Jones|Takes a flip from the 39 behind a Darrisaw block, reaches the secondary and is brought down inside the 25.|None|flip to running back; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:37|MIN|Hockenson|Catches Wentz's pass and is driven back by Woods and Edwards, bringing up fourth down.|None|unknown|unknown|unknown|Woods; Edwards (successful tacklers)|unverified (no DB match; caption-only)|
|08:46|MIN|Will Reichard|Makes a 39-yard field goal off the upright for a 9-3 lead.|39|field goal|unknown|unknown|unknown|verified vs DB|
|08:59|CHI|Burden|Makes a juggling catch over the middle during Chicago's final possession.|None|middle-of-field pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:07|CHI|Rome Odunze|Bagent steps up under pressure and completes a deep-right pass to Odunze for 21 yards; Odunze is pushed out at the Minnesota 20.|21|deep right pass|unknown|unknown|I.Rodgers (DB tackler)|verified vs DB|
|09:20|CHI|Bagent|Dallas Turner finishes the final play against Chicago's quarterback; commentary indicates a game-ending sack but supplies no yardage.|None|unknown|unknown|unknown|Dallas Turner (sack defender)|unverified (no DB match; caption-only)|

Offense (model synthesis from this game's plays): Jefferson supplied an early 30-yard reception and a later stated 16-yard first down. / Jones produced a 20-yard right-tackle run, an eight-yard run and a late advance behind Darrisaw's block. / Late passing conversions included Addison's 14-yard catch against a blitz and Hockenson's stated 20-yard reception. / Reichard made all three highlighted field goals, accounting for Minnesota's nine points.

Defense weaknesses: Williams repeatedly extended plays or scrambled for first downs, including a spin away from Van Ginkel and an escape from Turner before finding Raymond. / Chicago gained 13 yards with Swift and consecutive gains of 15 and 11 with Monangai on its opening second-half drive. / Swift's fourth-quarter screen gained 32 yards. / Chicago completed late passes to Burden over the middle and Odunze for 21 yards.

Limitations: Captions only; no frames were viewed and no commands were run. The supplied DB is selective, so NO DB MATCH does not establish that a play did not happen. Partial plays at 02:19 and 03:15 have uncertain identities or outcomes; the isolated Swift mention at 01:02 does not describe enough action to identify another play. Names on unmatched plays are retained as heard rather than repaired from unrelated DB entries. No explicit personnel grouping or named man/zone coverage can be assigned confidently to an individual play; explicit motion and pressure descriptions are preserved. General references to pistol, man coverage and zone principles were not assigned to particular snaps. DB shotgun labels were not used for personnel_formation because that field requires explicit commentary. Defender entries include tacklers, pressure defenders and successful defenders, not necessarily players who were beaten. Interception yards represent the return; field-goal yards represent kick distance, and the blocked kick uses DB play yardage. Penalty dispositions and several play yardages are unavailable. The late Hockenson catch at 08:19 cannot be matched to the DB's Q3 4:01 Oliver reception for 24 yards: quarter context, stated yardage and corrected receiver differ. That Oliver reception, the listed kick returns and the 24-yard punt return are not identifiable in these captions.


## Week 3: MIN 23 - TB 16 (game 401872959)
Video: Minnesota Vikings vs Tampa Bay Buccaneers Game Highlights | 2026 NFL Season Week 3 — https://www.youtube.com/watch?v=PwKZhQg5n6w  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:58|MIN|J.Jefferson|Pass caught at the 46 yard line by Justin Jefferson|22|unknown|unknown|unknown|unknown|verified vs DB|
|01:37|MIN|W.Reichard|54-yard field goal attempt is good|54|unknown|unknown|unknown|unknown|verified vs DB|
|02:14|MIN|M.Price|Punt return for 86 yards touchdown|86|unknown|unknown|unknown|unknown|verified vs DB|
|02:52|TB|C.Otton|Pass to Cade Otton for a first down|37|unknown|unknown|unknown|J.Metellus|verified vs DB|
|03:13|TB|T.Hurst|Pass to Ted Hurst for a touchdown|40|deep shot|unknown|unknown|unknown|verified vs DB|
|06:53|MIN|J.Addison|Deep pass to Jordan Addison ruled a catch for 30 yards|30|deep shot|unknown|unknown|unknown|verified vs DB|
|07:13|MIN|J.Addison|41 yard touchdown pass from Kyler Murray to Jordan Addison|41|deep shot|unknown|unknown|unknown|verified vs DB|
|09:03|MIN|K.Murray|Pass batted and intercepted by A'Shawn Robinson|0|unknown|unknown|unknown|unknown|verified vs DB|
|10:04|TB|C.McLaughlin|38-yard field goal is good|38|unknown|unknown|unknown|unknown|verified vs DB|
|12:50|TB|C.McLaughlin|54-yard field goal is good|54|unknown|unknown|unknown|unknown|verified vs DB|
|14:04|MIN|W.Reichard|56-yard field goal is good|56|unknown|unknown|unknown|unknown|verified vs DB|
|15:06|TB|B.Mayfield|Pass intercepted by A.Van Ginkel|0|unknown|unknown|unknown|unknown|verified vs DB|
|15:47|MIN|W.Reichard|43-yard field goal is good|43|unknown|unknown|unknown|unknown|verified vs DB|
|16:08|TB|J.Daniels|Pass intercepted by I.Rodgers|0|unknown|unknown|unknown|I.Rodgers|verified vs DB|

Offense (model synthesis from this game's plays): Deep passing game with accurate throws to speed receivers like J.Addison / Explosive punt return ability / Effective use of quarterback mobility on third downs / Reliable long-range field goal kicking

Defense weaknesses: Communication breakdowns leading to busted coverages on deep middle passes / Susceptibility to big passing plays over the middle / Allowing long punt returns

Limitations: Could not determine specific concepts like run gaps, play-action, screens, RPOs, personnel formations, or coverage schemes because the captions and commentary rarely explicitly stated them. Many names were mangled in captions and had to be corrected via clear DB matches. Several plays in captions lacked sufficient detail for yards or exact defender beaten. Non-highlight plays and those without clear DB matches were omitted.


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

Offense (model synthesis from this game's plays): Consistent field goal kicking by W.Reichard going 5/5 / Frequent successful passes to T.Hockenson for first downs and big gains / Explosive plays including 27-yard and 22-yard receptions by J.Addison and T.Hockenson / Effective use of play-action and scrambling by K.Murray

Defense weaknesses: Allowed explosive 53-yard run by O.Gordon / Gave up a rushing touchdown to O.Gordon / Missed tackles on runs by J.Wright and O.Gordon / Vulnerable to MIA short passes and scrambles on third downs allowing conversions and a FG

Limitations: Could not determine specific personnel formations, coverage schemes, or run gaps/directions in most cases as they were not explicitly stated by commentators or clearly shown in DB text. Many plays in captions did not have exact DB matches due to name mangling and incomplete details. Some yardage and exact player names corrected only where clear matches existed. Several plays lacked enough detail for yards, concepts, or defenders beaten.


## Week 5: MIN 23 - NO 13 (game 401872987)
Video: Minnesota Vikings vs New Orleans Saint Game Highlights | NFL 2026 Season Week 5 — https://www.youtube.com/watch?v=OeaSf-kDpYA  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:18|MIN|T.J. Hockenson|Murray pass underneath to tight end for first down into New Orleans territory|None|unknown|unknown|unknown|unknown|verified vs DB|
|00:38|MIN|Tai Felton|Fake to Jones, Murray finds open man downfield Tai Felton|None|play-action|unknown|unknown|unknown|verified vs DB|
|00:52|MIN|Claiborne|Murray gets rid of it on 3rd and 12, finds rookie Claiborne who takes it to the 21|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:58|MIN|W. Reichard|Field goal good from 40 yards, perfect on kicks|40|unknown|unknown|unknown|unknown|verified vs DB|
|01:12|NO|T. Shough|Pressure on Shough, stands in on fourth down resulting in three and out|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:17|MIN|J. Jefferson|Murray keeps it on 3rd and 2, Jefferson gets free at 30-yard line for 19-yard pickup|19|RPO|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:30|MIN|M. Price|Screen pass for Myles Price|None|screen|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:41|MIN|A. Jones|Ball comes out from Aaron Jones, fumbled into hands of Chase Young who returns upfield across 30|None|unknown|unknown|unknown|C. Young|verified vs DB|
|01:59|NO|C. Olave|Shough quick throw to Olave past the sticks|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:09|NO|Vele|Chunk play, takes it almost to the line, stopped a yard short|None|unknown|unknown|unknown|Cashman|unverified (no DB match; caption-only)|
|02:19|NO|Vele|Quick throw again, good job in tight window by Vele to hold on for conversion|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:34|NO|K. Miller|Miller again, flung by Metellus towards the sticks, first down inside the ten|None|unknown|unknown|unknown|Metellus|unverified (no DB match; caption-only)|
|02:49|NO|K. Miller|Hand off to Miller for touchdown from inside the ten|2|unknown|unknown|unknown|unknown|verified vs DB|
|03:17|MIN|A. Jones|Third down and two, Jones gets stuck behind line|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:26|NO|Vele|Third down, Shough puts it up for grabs with Vele against Isaiah Rogers|None|unknown|unknown|unknown|I. Rogers|unverified (no DB match; caption-only)|
|03:41|MIN|M. Price|Boomer of a punt, 60 plus to Price, outstanding return into New Orleans territory|43|unknown|unknown|unknown|unknown|verified vs DB|
|04:02|MIN|M. Price|Murray finds connection, dive ahead by Myles Price who makes up for the drop, picks up nine|9|screen|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:09|MIN|J. Jefferson|No Hockenson no Addison, one on one for Jefferson who holds on|21|deep shot|unknown|unknown|unknown|verified vs DB|
|04:25|MIN|W. Reichard|54-yard field goal good|54|unknown|unknown|unknown|unknown|verified vs DB|
|04:58|MIN|K. Murray|Murray running for his life under pressure, takes off for first down into red zone|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:10|MIN|J. Jefferson|Jefferson trying to get free against double coverage, show-stopping catch with multiple defenders|15|unknown|unknown|unknown|Sanker; Riley|verified vs DB|
|05:47|NO|T. Shough|Tyler Shough finds country, top target takes it past the 40-yard line|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:54|NO|unknown|Third and three, four man rush, quick throw|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:07|NO|T. Shough|Flag thrown and Shough throws it into hands of Byron Murphy Jr for interception|14|unknown|unknown|unknown|unknown|verified vs DB|
|06:16|MIN|K. Murray|Saints bring four and get to Murray, flush him out, throws on the move, catch by D.J. Dallas for first down|None|unknown|unknown|unknown|Grunderson|unverified (no DB match; caption-only)|
|06:30|MIN|unknown|Third and seven, Murray middle of the field wide open but ball not close|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:38|MIN|M. Price|Screen pass to Price, grabbed by Warner, ball comes out, Sanker recovers and returns 87 yards for touchdown|87|screen|unknown|unknown|M. Emerson|verified vs DB|
|07:38|MIN|J. Jones|Murray has time, man gets loose, busted coverage, pass to Jones for first NFL reception|32|unknown|unknown|busted coverage|unknown|verified vs DB|
|08:01|MIN|A. Jones|To the ground, hold for Jones, keeps feet, spins and takes it|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:08|MIN|J. Jefferson|Third and one, Murray kept it, floated ahead to Justin for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:17|MIN|A. Jones|Hand off for Jones, straight up, pounds ahead for touchdown|8|unknown|unknown|unknown|Blackmon|verified vs DB|
|08:53|NO|unknown|Quick throw off target and off time|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:08|MIN|K. Murray|Murray with the fake, rolling to the right, gets the first down|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:18|MIN|A. Jones|Jefferson lined up in backfield as decoy, Jones hand off for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:32|MIN|K. Murray|Bring four, Murray looking for window, takes off again thinking field goal|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:44|MIN|W. Reichard|55-yard field goal good|55|unknown|unknown|unknown|unknown|verified vs DB|
|09:56|NO|T. Shough|Shough throws it for grabs, second pick of the day for Byron Murphy Jr|0|unknown|unknown|unknown|unknown|verified vs DB|

Offense (model synthesis from this game's plays): Explosive plays through deep passes and screens to receivers like Jefferson and Felton / Effective red zone efficiency converting to touchdowns and field goals / Versatile quarterback runs and play-action leading to first downs and scores / Strong special teams with consistent long field goals

Defense weaknesses: Vulnerable to fumbles in red zone leading to opponent returns for touchdowns / Occasional busted coverage in secondary allowing big receptions

Limitations: Could not determine exact personnel formations, most coverage schemes, specific run gaps/directions, or all defender names due to lack of explicit commentary; some plays in captions had no clear DB match or were mangled; yardage only assigned when explicitly stated or matched to DB; many auto-generated caption names corrected only on clear matches to DB plays.
