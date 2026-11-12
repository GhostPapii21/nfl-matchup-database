# DAL — Phase 8 film notes (Weeks 1–6, 2026)

Method: NFL YouTube channel full-game highlight videos were located by search and their auto-captions (broadcast commentary) downloaded via yt-dlp. Codex (codex-cli 0.163.0) extracted plays from the captions. **No video frames were viewed by any agent.** Each play was checked against the repo DB play-by-play: `verified vs DB` means the cited DB play exists and the yardage matches. Personnel, formation and coverage appear only when commentators stated them; everything else is `unknown`.


## Week 1: DAL 20 - NYG 28 (game 401872930)
Video: Dallas Cowboys vs New York Giants Game Highlights | NFL 2026 Season Week 1 — https://www.youtube.com/watch?v=9R8P93W2iKE  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|01:10|DAL|Dak Prescott; unidentified receiver|Quick third-down completion near the first-down marker; result is cut off.|None|quick pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:28|DAL|unknown|Hard count without a snap results in delay of game.|-5|hard count; no snap|Javonte Williams alone in backfield; no fullback|unknown|unknown|unverified (no DB match; caption-only)|
|01:51|NYG|Cam Skattebo|Run to the 22-yard line.|None|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:57|NYG|Jaxson Dart; Malik Nabers|Dart completes a pass to Nabers after Nabers motions.|None|pass following receiver motion|Nabers in motion|unknown|unknown|unverified (no DB match; caption-only)|
|02:10|NYG|Jaxson Dart|Keeps the ball for 22 yards into Dallas territory; unnecessary roughness adds 15 yards.|22|quarterback keeper; left end|unknown|unknown|DeMarvion Overshown|verified vs DB|
|02:22|NYG|Cam Skattebo|Red-zone run ends around the 15 after a collision with Overshown.|None|run; direction unknown|unknown|unknown|DeMarvion Overshown|unverified (no DB match; caption-only)|
|02:33|NYG|Cam Skattebo|Three-yard touchdown run. Commentary credits Patrick Ricard's lead block and Isaiah Likely's blocking.|3|left-end run behind lead blocking|unknown|unknown|unknown|verified vs DB|
|03:03|DAL|Dak Prescott; George Pickens|Third-and-five sideline completion for a first down at the 26.|None|sideline pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:14|DAL|Dak Prescott; unidentified tight end|Fragment appears to describe a tight-end reception; receiver and result are incomplete.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:25|DAL|Dak Prescott; Brevyn Spann-Ford|Completion to Spann-Ford.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:31|DAL|Dak Prescott|On third and four, throws over the middle with a flag down and pressure arriving; outcome omitted.|None|pass over middle|Fullback Hunter mentioned|unknown|unknown|unverified (no DB match; caption-only)|
|03:39|NYG|unknown|Fragment references Rashan Gary's pass rush and a ball to Likely over the middle; full result is unavailable.|None|pass over middle|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:59|NYG|unknown|Giants retain a loose ball in a pile; Ricard is mentioned, but the recoverer is not established.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:10|NYG|Jaxson Dart; Malik Nabers|Pocket completion to Nabers, stopped about a yard and a half short of a first down.|None|pocket pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:22|NYG|Cam Skattebo|Stopped on third and two, with Kenny Clark identified in the tackle.|None|run; direction unknown|unknown|unknown|Kenny Clark|unverified (no DB match; caption-only)|
|04:36|DAL|Dak Prescott|Takes off and slides for a first down on a drive starting at Dallas's 15.|None|quarterback scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:57|DAL|Dak Prescott; CeeDee Lamb|One-yard touchdown pass on third and goal. Commentary describes Lamb creating separation in a one-on-one matchup.|1|short-left pass|shotgun|One-on-one matchup on Lamb; overall scheme unknown|unknown|verified vs DB|
|05:32|NYG|Jaxson Dart|Runs through open space and exits out of bounds.|None|quarterback scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:40|NYG|Jaxson Dart; Isaiah Likely|Third-and-ten completion across midfield for a first down against a five-man rush.|None|unknown|unknown|Five-man rush; coverage unknown|unknown|unverified (no DB match; caption-only)|
|05:50|NYG|Jaxson Dart; Malachi Fields|Second-and-seven completion for a first down at the 28.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:06|NYG|Jaxson Dart; receiver transcribed as Runyan|Dart takes a hit from Caleb Downs; captions describe a catch and loose ball without establishing the full outcome.|None|unknown|unknown|Downs described as unblocked; scheme unknown|unknown|unverified (no DB match; caption-only)|
|06:34|NYG|Tyrone Tracy|Retrospective commentary identifies Quinnen Williams forcing the turnover that gives Dallas possession at its 16. DB identifies Tracy's eight-yard run, fumble, and Shavon Revel's recovery with a minus-three-yard return.|8|left-end run|unknown|unknown|Quinnen Williams; Andrew Thomas tackled the returner|verified vs DB|
|06:38|DAL|Javonte Williams|Inside run from Dallas's 16 to its 22.|6|inside run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:44|DAL|Dak Prescott; CeeDee Lamb|Third-and-four completion on the edge; Lamb escapes an unnamed safety for a first down. Edmunds shows pressure and backs out.|None|edge pass|unknown|Edmunds shows pressure then drops; full scheme unknown|unknown|unverified (no DB match; caption-only)|
|06:55|DAL|Dak Prescott|Retreats under pressure on third and five and throws an interception to Jevon Holland, who records no return yardage.|0|deep-right pass under pressure|unknown|unknown|unknown|verified vs DB|
|07:31|NYG|Jaxson Dart; Malik Nabers|Sideline completion for a first down; Nabers exits out of bounds.|None|sideline pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:39|NYG|Jaxson Dart; receiver transcribed as Moony|Completion during the late-half scoring drive; receiver's identity is uncertain.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:55|NYG|Jaxson Dart; Isaiah Likely|Fifteen-yard touchdown reception with two feet down. Commentary says Dallas leaves the corner of the end zone open while two defenders chase a shallow receiver.|15|short-right touchdown pass|unknown|Coverage breakdown on defensive left; underlying scheme unknown|unknown|verified vs DB|
|08:58|NYG|Cam Skattebo|Changes direction and breaks a tackle for a first down; Caleb Downs cannot bring him down.|None|run with change of direction|unknown|unknown|Caleb Downs|unverified (no DB match; caption-only)|
|09:16|NYG|Jaxson Dart; unidentified tight end|Throws outside to a tight end; result is cut off.|None|outside pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:42|NYG|Jaxson Dart|Second-down fragment describes Dart sliding into the middle; exact action and result are unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:55|NYG|Jaxson Dart; Isaiah Likely|Two-yard touchdown pass after a fake to Berrios. Replay commentary describes short motion and a feigned crackback block before the reception.|2|fake to Berrios; short motion and fake crackback block into pass|short motion|unknown|unknown|verified vs DB|
|11:00|DAL|Dak Prescott; Javonte Williams|Completion to Williams with nowhere to go; Arvell Reese is credited with the defensive play.|None|unknown|shotgun|unknown|Arvell Reese|unverified (no DB match; caption-only)|
|11:18|DAL|Dak Prescott; CeeDee Lamb|Prescott retreats and throws toward Lamb; outcome is omitted. Commentary references covering the flats.|None|unknown|unknown|Flats coverage mentioned; full scheme unknown|unknown|unverified (no DB match; caption-only)|
|11:30|DAL|Javonte Williams|Follows blockers for a one-yard touchdown run.|1|right-tackle run|unknown|unknown|unknown|verified vs DB|
|11:49|NYG|Jaxson Dart|Runs with Likely leading and finishes just short of a first down; Lawrence makes the tackle.|None|quarterback run with lead blocker|unknown|unknown|Lawrence; full identity not established|unverified (no DB match; caption-only)|
|12:02|NYG|Cam Skattebo|Takes a handoff, makes a move, fumbles, and recovers the ball.|None|handoff run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:16|NYG|Jaxson Dart; Devin Singletary|First-and-ten completion to Singletary, tackled by Barham.|None|unknown|unknown|unknown|Barham|unverified (no DB match; caption-only)|
|12:22|NYG|Jaxson Dart; Devin Singletary|Third-and-nine swing pass converted for a first down through Thompson's tackle.|None|swing pass|unknown|unknown|Thompson|unverified (no DB match; caption-only)|
|12:41|NYG|Jaxson Dart; Devin Singletary|Nine-yard touchdown on another swing pass, on third and five. Replay commentary identifies motion across the formation.|9|swing pass left following motion|motion across formation|unknown|unknown|verified vs DB|
|13:39|DAL|Dak Prescott; target transcribed as Deebo|Prescott has time to throw; ensuing commentary indicates a missed touchdown opportunity, but the target and exact result are unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:49|DAL|Dak Prescott; unidentified receiver|Third-and-ten sideline completion against a five-man rush; subsequent commentary mentions a stiff-arm on Holland.|None|sideline pass|unknown|Five-man rush; coverage unknown|Jevon Holland|unverified (no DB match; caption-only)|
|14:04|DAL|Dak Prescott; Javonte Williams|Seventeen-yard touchdown pass to a wide-open Williams. Commentary says Arvell Reese was fooled. Williams receives a taunting penalty; DB records the subsequent missed extra point.|17|short-left pass|unknown|unknown|Arvell Reese|verified vs DB|
|14:57|NYG|unknown|Third-and-long snap against another Dallas five-man rush; play result is missing.|None|unknown|unknown|Five-man rush; coverage unknown|unknown|unverified (no DB match; caption-only)|
|15:11|NYG|Cam Skattebo|Second-and-16 play involving Skattebo; action and result are cut off.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:24|NYG|Jaxson Dart; Isaiah Likely|Third-and-three completion underneath to Likely. Pregame-snap commentary anticipates pressure and one-on-one matchups; a pick route is suggested but not confirmed.|None|underneath pass|spread alignment|Commentator anticipates one-on-one coverage; actual scheme unconfirmed|unknown|unverified (no DB match; caption-only)|
|15:39|NYG|unknown|Late play draws a facemask on Dallas number 6, awarding a first down and 15 penalty yards; ballcarrier and underlying gain are not stated.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|

Offense (Codex synthesis from this game's plays): Prescott converted first downs with a scramble and sideline completions to Pickens and an unidentified late-game receiver. / Lamb supplied a goal-line touchdown and a third-down catch on which he escaped a safety. / Williams scored both behind blockers at right tackle and on a 17-yard reception.

Defense weaknesses: Dart's 22-yard keeper was compounded by Overshown's unnecessary-roughness penalty. / Commentary identified a coverage breakdown on Likely's 15-yard touchdown, with two defenders following a shallow receiver and the end-zone corner left open. / Dallas repeatedly allowed Singletary swing passes, including a broken tackle against Thompson on third and nine and a subsequent touchdown. / A five-man rush did not prevent Dart's third-and-ten completion to Likely. / Downs missed a tackle on Skattebo's first-down run, and a late facemask extended a Giants possession.

Limitations: Captions only; no frames were viewed. Fragmentary snaps are included with uncertain results explicitly marked. Supplied DB entries are selective, so NO DB MATCH does not mean a play did not occur. No caption evidence identifies the supplied kick returns or 38-yard pass-interference play. Yards are null unless established by a clear DB match or explicit caption field positions. The interception's zero yards denotes return yardage; Tracy's eight yards denotes the run before his fumble. Named tacklers in defender_beaten are not necessarily defenders who lost their matchup. Personnel and coverage details are limited to explicit commentary; DB shotgun labels alone were not used. The hit involving the receiver transcribed as Runyan cannot safely be merged with Tracy's separately referenced fumble. Unclear receiver names were left unresolved, and speculative pick-route commentary was not treated as a confirmed concept.


## Week 2: WSH 20 - DAL 37 (game 401872944)
Video: Washington Commanders vs Dallas Cowboys Game Highlights | 2026 NFL Season Week 2 — https://www.youtube.com/watch?v=s6KiKu6PZgk  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 3: BAL 34 - DAL 31 (game 401872960)
Video: Baltimore Ravens vs Dallas Cowboys Game Highlights from Rio | 2026 NFL Season Week 3 — https://www.youtube.com/watch?v=7gWPdESD1og  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 4: DAL 34 - HOU 30 (game 401872967)
Video: Dallas Cowboys vs. Houston Texans Game Highlights | NFL 2026 Season Week 4 — https://www.youtube.com/watch?v=Yayn1UWwu1Y  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 5: TB 24 - DAL 16 (game 401872980)
Video: Tampa Bay Buccaneers vs Dallas Cowboys Game Highlights | 2026 NFL Season Week 5 — https://www.youtube.com/watch?v=OmJqJI7pJpI  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 6: DAL 13 - GB 23 (game 401873007)
Video: Dallas Cowboys vs Green Bay Packers Game Highlights | 2026 NFL Season Week 6 — https://www.youtube.com/watch?v=5xB0vJWbJG4  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:32|DAL|unknown|Commentary reports a loss of a couple, leaving third-and-4; ball carrier and play type are missing.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:52|GB|unknown|Joey Porter Jr. makes a backfield tackle for loss. The ball carrier and yardage are not identified.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:28|GB|Strong (caption surname; identity unverified)|Strong is stopped for no gain.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:08|GB|Matthew Golden|Jordan Love throws a 9-yard touchdown to Golden on third-and-6, with Bo Melton in motion. Commentary mentions a defensive stunt.|9|short middle pass|Bo Melton in motion; personnel unspecified|unknown|unknown|verified vs DB|
|03:06|GB|Jordan Love|Dee Winters intercepts Love's quick out intended for Matthew Golden. The apparent touchdown return is reversed because Winters was down by contact at the GB 42.|0|quick out|Motion/shift mentioned; personnel unspecified|Commentary says motion suggested zone; actual coverage unconfirmed|unknown|verified vs DB|
|04:27|DAL|Dak Prescott|Prescott's third-and-8 throw over the middle intended for CeeDee Lamb is intercepted by E. Williams, who returns it 17 yards.|17|short middle pass|unknown|unknown|unknown|verified vs DB|
|04:31|GB|Christian Watson|Retrospective commentary references Watson being one-on-one on the preceding play. The catch, result and yardage are omitted, preventing a confident match to either listed Watson reception.|None|unknown|unknown|One-on-one matchup mentioned; full scheme unspecified|unknown|unverified (no DB match; caption-only)|
|06:01|DAL|Dak Prescott|On second-and-inches, Prescott rolls and throws; the captions cut away before identifying the target or result.|None|rollout pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:17|DAL|Pickens (caption surname)|Commentary describes Prescott hitting Pickens downfield after improvising inside the pocket. No yardage is supplied.|None|downfield pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:41|DAL|Dak Prescott|Prescott is intercepted by Brandon Cisse after intended receiver CeeDee Lamb falls down. Cisse returns the interception 5 yards.|5|short left pass|unknown|unknown|unknown|verified vs DB|
|07:20|GB|Bo Melton|On third-and-8, Joey Porter Jr. is flagged for defensive pass interference on Love's deep right target to Melton. The DB records a 37-yard penalty and no play.|37|deep shot right|unknown|unknown|Joey Porter Jr. (penalized defender)|verified vs DB|
|07:49|GB|Jordan Love|Love escapes the pocket on third-and-6. The target and result are missing; a match to Golden's subsequent 21-yard reception cannot be established confidently.|None|pass after pocket escape|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:03|GB|Jordan Love|Love sneaks over the goal line for a 1-yard touchdown. Replay commentary describes the offensive line moving Kenny Clark backward.|1|quarterback sneak up the middle|unknown|unknown|Kenny Clark|verified vs DB|
|08:26|DAL|Dak Prescott|A third-and-9 play is followed by references to the first-down marker and Prescott's leadership. The action and result are too incomplete to establish a conversion.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:06|DAL|Javonte Williams|Williams scores a 1-yard rushing touchdown. Commentary identifies an extra eligible lineman and Brevyn Spann-Ford serving as fullback.|1|run up the middle|Extra eligible offensive lineman; Brevyn Spann-Ford at fullback|unknown|unknown|verified vs DB|
|09:53|GB|Jordan Love|A fake handoff is called, followed by praise for Porter Jr. and an announcement of fourth-and-3. The target, yardage and exact result are missing.|None|fake handoff|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:23|GB|Jordan Love|Replay commentary describes an unnamed Dallas edge rusher getting fingers on Love's throw while standing in the end zone. The final result is unspecified.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:42|DAL|Dak Prescott|Prescott completes a third-and-6 pass to an unnamed receiver. Commentary immediately identifies slants as available against Green Bay's blitz looks, but the captions do not establish the gain.|None|slant, as described in adjacent commentary|unknown|Blitz look mentioned; coverage unspecified|unknown|unverified (no DB match; caption-only)|
|12:06|GB|Matthew Golden|Love gets the ball to Golden before being hit by C. Downs. The DB identifies a 21-yard reception to the right, ending out of bounds.|21|short right pass|unknown|unknown|M. Bell (DB tackler); C. Downs (pressure)|verified vs DB|
|12:24|GB|unknown|Dallas crowds the line before a snap. Commentary suggests Cover 0 and anticipates a post or go route, but supplies no actual route or play result.|None|unknown|unknown|Apparent Cover 0/man-to-man, explicitly tentative in commentary|unknown|unverified (no DB match; caption-only)|
|13:00|DAL|Pickens (caption surname)|Prescott throws quickly to Pickens, who attempts to evade defenders with CeeDee Lamb nearby. The gain is missing.|None|quick pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:32|DAL|Dak Prescott|Carrington Valentine intercepts a pass intended for Jonathan Mingo and returns it 21 yards, but Lukas Van Ness's roughing-the-passer penalty nullifies the play.|None|short left pass; nullified|unknown|Defenders back out with help over the top; exact coverage unspecified|unknown|verified vs DB|
|14:03|DAL|Dak Prescott|With Green Bay rushing four, Prescott launches downfield. The target and outcome are absent.|None|deep shot|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:20|DAL|Flournoy (caption surname)|Flournoy catches Prescott's pass for a first down and spins off a tackle.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:30|DAL|Dak Prescott|Prescott throws toward the end zone with Valentine in coverage; the target and result are omitted.|None|end-zone pass|unknown|Commentary describes backing off and late help toward Pickens; exact scheme unspecified|unknown|unverified (no DB match; caption-only)|
|14:44|DAL|unknown|Dallas faces fourth-and-11 with Green Bay showing pressure. The captions omit the action and outcome.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:51|DAL|Ryan Flournoy|Prescott slips at the top of his drop, then completes a 6-yard touchdown to Flournoy. Commentary describes an unidentified defender being knocked backward on the route.|6|short right pass|unknown|unknown|unknown|verified vs DB|
|16:08|DAL|Dak Prescott|Dallas attempts two to make it a one-score game. The DB supplies the outcome: Prescott's pass to CeeDee Lamb is incomplete; offensive holding is declined.|None|pass|unknown|unknown|unknown|verified vs DB|

Offense (Codex synthesis from this game's plays): The goal-line touchdown used an extra eligible lineman and Spann-Ford at fullback for Williams's middle run. / Commentary identifies slants as available against Green Bay's blitz looks near the 11:42 completion. / Flournoy supplied a first-down reception with a broken tackle and the late receiving touchdown.

Defense weaknesses: Love completed the 21-yard pass to Golden despite Downs's pressure and hit. / Porter Jr.'s 37-yard pass-interference penalty extended Green Bay's late-first-half possession. / The defensive front yielded Love's 1-yard sneak touchdown; commentary specifically describes Clark being moved backward.

Limitations: Captions are fragmented and provide no visual evidence. Several entries identify only partial actions or pre-snap situations; these are explicitly marked. Formation and coverage details are included only when spoken, with tentative calls preserved as tentative. Named tacklers do not establish who lost coverage. Interception yards follow DB return yardage; the nullified Valentine return has null yards. No caption segment confidently establishes either Watson gain, Golden's 21-yard first-half catch, Pickens's late 21-yard catch, any kickoff, or a made field goal, so those DB events are not added independently. DB-only shotgun labels are excluded from personnel_formation. Reversed and nullified touchdowns/interceptions are not counted as scores or valid turnovers.
