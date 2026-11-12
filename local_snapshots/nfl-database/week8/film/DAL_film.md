# DAL — Phase 8 film notes (Weeks 1–6, 2026)
> Note: games 401872944, 401872945, 401872952, 401872962, 401872964, 401872970, 401872985, 401872989 were extracted by a Grok Bot agent (not Codex) from the same captions; mostly scoring/20+ plays logged.
> Note: games 401872960, 401872967, 401872980 were extracted by Grok via the xAI API (grok-4.20-0309-non-reasoning, same prompt/schema as Codex, cleaned captions); sidecar provenance in film/grok_meta/. All other games with notes: Codex.

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

Offense (model synthesis from this game's plays): Prescott converted first downs with a scramble and sideline completions to Pickens and an unidentified late-game receiver. / Lamb supplied a goal-line touchdown and a third-down catch on which he escaped a safety. / Williams scored both behind blockers at right tackle and on a 17-yard reception.

Defense weaknesses: Dart's 22-yard keeper was compounded by Overshown's unnecessary-roughness penalty. / Commentary identified a coverage breakdown on Likely's 15-yard touchdown, with two defenders following a shallow receiver and the end-zone corner left open. / Dallas repeatedly allowed Singletary swing passes, including a broken tackle against Thompson on third and nine and a subsequent touchdown. / A five-man rush did not prevent Dart's third-and-ten completion to Likely. / Downs missed a tackle on Skattebo's first-down run, and a late facemask extended a Giants possession.

Limitations: Captions only; no frames were viewed. Fragmentary snaps are included with uncertain results explicitly marked. Supplied DB entries are selective, so NO DB MATCH does not mean a play did not occur. No caption evidence identifies the supplied kick returns or 38-yard pass-interference play. Yards are null unless established by a clear DB match or explicit caption field positions. The interception's zero yards denotes return yardage; Tracy's eight yards denotes the run before his fumble. Named tacklers in defender_beaten are not necessarily defenders who lost their matchup. Personnel and coverage details are limited to explicit commentary; DB shotgun labels alone were not used. The hit involving the receiver transcribed as Runyan cannot safely be merged with Tracy's separately referenced fumble. Unclear receiver names were left unresolved, and speculative pick-route commentary was not treated as a confirmed concept.


## Week 2: WSH 20 - DAL 37 (game 401872944)
Video: Washington Commanders vs Dallas Cowboys Game Highlights | 2026 NFL Season Week 2 — https://www.youtube.com/watch?v=s6KiKu6PZgk  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|01:26|DAL|CeeDee Lamb|Lamb touchdown; Tom B: came with a play-action fake|3|play-action|unknown|unknown|unknown|verified vs DB|
|02:15|DAL|CeeDee Lamb|Lamb again (commentary says touchdown; DB shows 38-yd catch to WAS 26 — treat as uncertain)|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:21|DAL|Jake Ferguson|Caught, touchdown Cowboys|10|short middle|unknown|unknown|unknown|verified vs DB|
|06:13|WSH|Terry McLaurin|Going deep, has a man, McLaurin (DB 24 deep right)|24|deep shot|unknown|unknown|unknown|verified vs DB|
|09:03|WSH|Jayden Daniels|Blitz coming, Daniels gets a first down with his legs|20|QB scramble vs blitz|unknown|blitz|unknown|verified vs DB|
|11:58|WSH|Terry McLaurin|What a throw (Mariota) — DB 26-yd catch|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:25|WSH|Drew Stevens|47-yard FG|None|field goal|unknown|unknown|unknown|verified vs DB|
|14:24|DAL|Jake Ferguson|Touchdown Jake Ferguson, number two|12|short middle|unknown|unknown|unknown|verified vs DB|
|16:39|DAL|Brandon Aubrey|Another 60-yard field goal|None|field goal|unknown|unknown|unknown|verified vs DB|
|17:10|WSH|Stefon Diggs|Mariota throwing end zone corner, touchdown; corner vacates the zone|20|corner route vs zone|unknown|zone (corner vacated)|unknown|verified vs DB|
|18:11|DAL|CeeDee Lamb|Touchdown Dallas; Lamb 8 catches 153 yards 2 TD per commentary|24|deep right|unknown|unknown|unknown|verified vs DB|

Offense (model synthesis from this game's plays): Lamb volume + explosives (23, 38, 35, 24 TD) / Ferguson RZ TE (2 TD) / Play-action TD

Defense weaknesses: Daniels scrambles vs blitz / Corner route vs zone TD to Diggs / McLaurin deep 24

Limitations: Captions skimmed by keyword (TD/yardage/coverage terms); plays <20 yds mostly not logged. Coverage stated: zone on Diggs TD; blitz references. Note: Washington QB Daniels left, Mariota played second half.


## Week 3: BAL 34 - DAL 31 (game 401872960)
Video: Baltimore Ravens vs Dallas Cowboys Game Highlights from Rio | 2026 NFL Season Week 3 — https://www.youtube.com/watch?v=7gWPdESD1og  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:37|BAL|D.Henry|Henry rushes ahead out to about the 29|6|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:52|BAL|L.Jackson|Jackson back cutting all the way to the 16|13|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:19|DAL|D.Prescott|Prescott zips ahead through the middle and fires it for the completion to Pickens for 14|14|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:34|DAL|J.Williams|Javonte Williams carry for 17 yards|17|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:48|DAL|J.Williams|Williams to the 5 yard line, first and goal|12|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:11|DAL|B.Aubrey|Aubrey 28 yard field goal is good|28|unknown|unknown|unknown|unknown|verified vs DB|
|02:24|BAL|M.Andrews|Pass to Andrews with a pirouette, almost got him to the sticks, a foot short|9|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:32|BAL|D.Henry|Henry fighting for it and scores the touchdown|1|unknown|unknown|unknown|unknown|CONFLICT (yardage 1 vs DB)|
|03:21|BAL|L.Jackson|Lamar takes it and gives the Ravens their first big play of the game for 21 yards|21|unknown|unknown|unknown|M.Bell|CONFLICT (yardage 21 vs DB)|
|03:40|BAL|Z.Flowers|Flowers between two defenders for 22 yards|22|unknown|unknown|unknown|M.Bell|verified vs DB|
|04:02|BAL|D.Henry|Henry cuts off the left tackle and goes in for the touchdown|4|unknown|unknown|unknown|unknown|verified vs DB|
|04:28|DAL|C.Lamb|Pass to Lamb for 11 yards|11|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:09|BAL|Z.Flowers|Flowers got the first down, wrestled down by Revel|5|unknown|unknown|unknown|S.Revel|unverified (no DB match; caption-only)|
|05:26|BAL|L.Jackson|Pass incomplete deep middle to Walker, defensive pass interference on Bell for 49 yards|49|deep shot|unknown|unknown|M.Bell|verified vs DB|
|05:43|BAL|D.Henry|Henry breaks outside and scores the touchdown|3|unknown|unknown|unknown|unknown|verified vs DB|
|06:33|BAL|R.Bateman|Bateman with his first catch|8|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:47|BAL|L.Jackson|Jackson has a nice gain with the rookie out of Alabama for 13 yards|13|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:06|BAL|T.Loop|27-yard attempt for Loop is good|27|unknown|unknown|unknown|unknown|verified vs DB|
|07:37|DAL|T.Goodson|Handoff to Goodson picks up 10 on a nice run|10|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:52|DAL|D.Prescott|Prescott steps up and hits Lamb, Cowboys convert|13|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:06|DAL|T.Goodson|Gain of about 9 running behind TJ Bass|9|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:25|DAL|B.Aubrey|Aubrey good from 38|38|unknown|unknown|unknown|unknown|verified vs DB|
|08:45|DAL|G.Pickens|Finds Pickens for about 11-12 yards|12|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:58|DAL|C.Lamb|Lamb making the catch for 13 yards|13|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:07|DAL|D.Prescott|Prescott takes off for the first down|8|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:21|DAL|D.Prescott|Little pass inside, ball on the ground, fumble recovered by Simpson|-1|screen|unknown|unknown|T.Simpson|verified vs DB|
|09:51|BAL|D.Henry|Henry, loss of 5|-5|unknown|unknown|unknown|Q.Williams|unverified (no DB match; caption-only)|
|10:28|DAL|J.Williams|Williams into the secondary for 22 yards|22|unknown|unknown|unknown|unknown|verified vs DB|
|11:00|DAL|B.Aubrey|59-yard field goal is blocked|0|unknown|unknown|unknown|K.Jackson|verified vs DB|
|11:34|BAL|D.Henry|Henry with the stiff arm down the sideline for 29 yards|29|unknown|unknown|unknown|S.Revel|verified vs DB|
|12:07|BAL|L.Jackson|Fakes the end around, touchdown to Moore|4|play-action|unknown|unknown|unknown|verified vs DB|
|12:41|DAL|G.Pickens|Pass to Pickens for about 14 yards|14|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:13|DAL|D.Prescott|Prescott to Ferguson for the touchdown|19|unknown|unknown|unknown|unknown|verified vs DB|
|13:42|BAL|C.Lamb|Pass caught by CeeDee Lamb for 21 yards|21|unknown|unknown|unknown|M.Bell|CONFLICT (yardage 21 vs DB)|
|13:55|BAL|M.Hibner|Hibner going for 22 yards on his second catch|22|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:11|BAL|L.Jackson|Jackson throws to Bateman for 31 yards|31|deep shot|unknown|unknown|A.Clark|verified vs DB|
|14:49|BAL|D.Henry|Henry rushes for 20 yards to the 3|20|unknown|unknown|unknown|S.Revel|verified vs DB|
|15:28|DAL|C.Lamb|Pass to Lamb for 49-50 yards|49|deep shot|unknown|unknown|M.Humphrey|verified vs DB|
|16:10|DAL|K.Turpin|Turpin scores the rushing touchdown|9|unknown|unknown|unknown|unknown|verified vs DB|
|18:19|BAL|M.Hibner|Jackson to Hibner for the touchdown|2|unknown|unknown|unknown|unknown|verified vs DB|
|18:51|DAL|C.Lamb|Pass to Lamb, out of bounds|20|unknown|unknown|unknown|N.Wiggins|verified vs DB|
|19:41|DAL|B.Aubrey|Aubrey 23 yard field goal good to tie the game|23|unknown|unknown|unknown|unknown|verified vs DB|
|19:54|BAL|Z.Flowers|Jackson down the middle to Flowers for 27 yards|27|deep shot|unknown|unknown|R.Steward|CONFLICT (yardage 27 vs DB)|
|20:04|BAL|T.Loop|Loop 56 yard field goal is good, walk-off winner|56|unknown|unknown|unknown|unknown|verified vs DB|

Offense (model synthesis from this game's plays): Explosive plays through run game with Javonte Williams and KaVontae Turpin scoring TDs / Dak Prescott's ability to make big throws downfield to CeeDee Lamb, George Pickens, and Jake Ferguson for TDs / Resilient scoring drives including game-tying FG / Effective use of play-action

Defense weaknesses: Struggled to stop Baltimore's run game, allowing multiple big runs and TDs by Henry / Defensive pass interference penalties costing big yards and setting up scores / Blocked field goal and fumble turnover / Injuries impacting secondary and run defense

Limitations: Could not determine specific concepts like run gaps/directions, personnel formations, or coverage schemes because they were not explicitly stated by commentators or clearly shown in DB text. Many caption plays had no exact DB match due to name mangling, timing, or non-highlight DB entries. Auto-generated captions had frequent name errors (e.g. Pickens for Lamb, various tight end names) corrected only on clear matches. Yards sometimes estimated from description when not explicit.


## Week 4: DAL 34 - HOU 30 (game 401872967)
Video: Dallas Cowboys vs. Houston Texans Game Highlights | NFL 2026 Season Week 4 — https://www.youtube.com/watch?v=Yayn1UWwu1Y  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:18|HOU|N.Collins|Pass reception, first down|15|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:45|HOU|J.Schultz|Pass reception, first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:15|HOU|N.Collins|Pass to end zone, touchdown|7|unknown|unknown|unknown|unknown|verified vs DB|
|01:45|DAL|D.Prescott|Rush, gain of 6|6|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:04|DAL|C.Lamb|Pass reception, first down, gain of 8|8|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:13|DAL|C.Lamb|Pass reception, first down and more|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:39|DAL|B.Aubrey|39-yard field goal, good|39|unknown|unknown|unknown|unknown|verified vs DB|
|02:54|HOU|W.Marks|Rush, good gain|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:06|HOU|J.Noel|Deep pass reception|45|deep shot|unknown|unknown|unknown|CONFLICT (yardage 45 vs DB)|
|03:31|HOU|K.Fairbairn|51-yard field goal, good|51|unknown|unknown|unknown|unknown|verified vs DB|
|03:45|DAL|J.Williams|Dump off pass, out of bounds|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:06|DAL|C.Lamb|Pass reception on third down, first down, gain of 7|7|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:24|DAL|J.Williams|Pass reception, third down stop by defense|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:30|DAL|B.Aubrey|50-yard field goal, good|50|unknown|unknown|unknown|unknown|verified vs DB|
|04:45|HOU|X.Hutchinson|Pass too hard, incomplete|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:51|DAL|C.Lamb|Pass reception, first down, gain of 11|11|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:04|DAL|D.Prescott|Third and 11, incomplete due to pressure|0|unknown|unknown|unknown|L.Hall|unverified (no DB match; caption-only)|
|05:15|DAL|B.Aubrey|62-yard field goal attempt, blocked|0|unknown|unknown|unknown|unknown|verified vs DB|
|05:43|HOU|N.Collins|Pass reception, first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:51|HOU|C.Stroud|Under pressure, throw away|0|unknown|unknown|unknown|R.Gary|unverified (no DB match; caption-only)|
|05:59|HOU|K.Fairbairn|39-yard field goal, good|39|unknown|unknown|unknown|unknown|verified vs DB|
|06:21|DAL|J.Williams|Rush, gain of 14, first down|14|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:36|DAL|C.Lamb|Pass caught|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:48|DAL|D.Prescott|Sacked|-7|unknown|unknown|unknown|W.Anderson|unverified (no DB match; caption-only)|
|06:58|DAL|B.Aubrey|65-yard field goal, no good wide left|65|unknown|unknown|unknown|unknown|verified vs DB|
|07:13|HOU|K.Fairbairn|53-yard field goal, good|54|unknown|unknown|unknown|unknown|verified vs DB|
|07:36|DAL|K.Turpin|Kickoff return, 46 yards|46|unknown|unknown|unknown|unknown|CONFLICT (yardage 46 vs DB)|
|07:56|DAL|J.Williams|Toss play, first down|None|run gap/direction|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:09|DAL|C.Lamb|Wide open pass reception inside the 10|None|play-action|unknown|unknown|unknown|verified vs DB|
|08:25|DAL|J.Williams|Rushing touchdown|8|run gap/direction|unknown|unknown|unknown|verified vs DB|
|09:02|HOU|J.Noel|Kick return, 53 yards|53|unknown|unknown|unknown|A.Speed|CONFLICT (yardage 53 vs DB)|
|09:35|HOU|N.Collins|Pass to end zone, touchdown|22|unknown|unknown|unknown|unknown|verified vs DB|
|10:19|DAL|G.Pickens|Deep pass, incredible catch|53|deep shot|unknown|unknown|unknown|verified vs DB|
|10:36|DAL|J.Williams|Rushing touchdown|1|run gap/direction|unknown|unknown|unknown|verified vs DB|
|11:17|HOU|C.Stover|Pass reception|20|unknown|unknown|unknown|M.Hooker|verified vs DB|
|11:38|DAL|C.Lamb|Deflected pass, reception|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:54|DAL|C.Lamb|Pass reception, second and eight|None|unknown|unknown|unknown|unknown|verified vs DB|
|12:06|DAL|C.Lamb|Pass reception, first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:35|DAL|C.Lamb|Pass reception, first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:45|DAL|C.Lamb|Pass reception inside the 10|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:57|DAL|J.Williams|Rushing touchdown|2|run gap/direction|unknown|unknown|unknown|verified vs DB|
|13:28|HOU|K.Boutte|Pass reception|21|unknown|unknown|unknown|unknown|verified vs DB|
|13:40|HOU|C.Stroud|Sacked on third down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:51|DAL|D.Prescott|Pass caught after hit, not enough for first down|None|unknown|unknown|unknown|W.Anderson|unverified (no DB match; caption-only)|
|14:06|HOU|X.Hutchinson|Pass reception, first down and more|26|unknown|unknown|unknown|R.Steward|verified vs DB|
|14:23|HOU|N.Collins|Pass reception on third down, conversion|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:44|HOU|J.Noel|Pass reception, first down|22|unknown|unknown|unknown|C.Downs|verified vs DB|
|14:54|HOU|D.Montgomery|Pass to Montgomery, lateral, big gain|21|unknown|unknown|unknown|unknown|verified vs DB|
|15:05|HOU|W.Marks|Rushing touchdown|6|run gap/direction|unknown|unknown|unknown|verified vs DB|
|15:35|DAL|C.Lamb|Pass reception|21|unknown|unknown|unknown|unknown|CONFLICT (yardage 21 vs DB)|
|16:02|DAL|C.Lamb|Pass reception|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|16:13|DAL|C.Lamb|Pass reception|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|16:20|DAL|G.Pickens|Pass reception inside the 15|22|unknown|unknown|unknown|R.Blankenship|verified vs DB|
|16:37|DAL|C.Lamb|Passing touchdown|12|unknown|unknown|unknown|unknown|verified vs DB|
|17:11|HOU|N.Collins|Pass reception under pressure|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|

Offense (model synthesis from this game's plays): Explosive plays through deep passes to multiple receivers including C.Lamb, G.Pickens / Effective red zone rushing with J.Williams scoring multiple touchdowns / High volume targeting of C.Lamb with 17 receptions / Strong third down conversion rate

Defense weaknesses: Susceptible to big passing plays allowing multiple 20+ yard receptions and touchdowns to N.Collins / Struggled to pressure quarterback consistently early, allowing sustained drives / Vulnerable to kick returns yielding good field position to opponent

Limitations: Cannot determine exact personnel, formations, or coverage schemes as they were not explicitly stated by commentators. Many plays in captions lack specific yardage or defender details. Some plays could not be precisely matched to DB due to caption mangling and lack of exact timing/yardage. Auto-generated captions have timing and transcription errors.


## Week 5: TB 24 - DAL 16 (game 401872980)
Video: Tampa Bay Buccaneers vs Dallas Cowboys Game Highlights | 2026 NFL Season Week 5 — https://www.youtube.com/watch?v=OmJqJI7pJpI  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:29|DAL|D.Prescott|Prescott slides left, throws along the sideline. Juggle and caught by George Pickens.|21|unknown|unknown|unknown|unknown|verified vs DB|
|00:43|DAL|J.Williams|Big hole inside the 40 to the 29 yard line. Javonte Williams.|21|unknown|unknown|unknown|unknown|verified vs DB|
|00:55|DAL|D.Prescott|Prescott throws deep middle. Pickens makes the grab inside the 9 yard line. First and goal.|21|deep shot|unknown|unknown|unknown|verified vs DB|
|01:08|DAL|J.Williams|Williams up the middle for the touchdown.|1|unknown|unknown|unknown|T.Smith|verified vs DB|
|02:02|TB|C.Godwin|Pass caught inside the 25 to the 20 by Chris Godwin.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:12|TB|E.Egbuka|Daniels throws, hauled in inside the 10 yard line by Egbuka. First and goal.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:27|TB|B.Irving|Floater taken to the end zone. Irving for the touchdown.|5|unknown|unknown|unknown|unknown|verified vs DB|
|03:06|DAL|D.Prescott|Pressure gets it away. Incomplete, intended for Pickens. Parrish breaks it up.|None|unknown|unknown|unknown|J.Parrish|unverified (no DB match; caption-only)|
|04:07|DAL|J.Williams|Throws underneath. Caught on the outside. 10 yard gain for Javonte Williams.|10|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:19|DAL|D.Prescott|Pressure. Escapes then throws. Picked off at the 25 yard line by Tykee Smith.|None|unknown|unknown|unknown|unknown|verified vs DB|
|04:36|TB|B.Irving|Bucky Irving big hole over the right side. First down across midfield.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:48|TB|E.Egbuka|Egbuka goes to the outside. Daniels looking to run. Stopped after gain of 1.|1|unknown|unknown|unknown|D.Winters|unverified (no DB match; caption-only)|
|06:00|DAL|R.Flournoy|Deep into traffic. Hauled in by Flournoy who takes it into Tampa Bay territory. 48 yard gain.|48|deep shot|unknown|unknown|unknown|verified vs DB|
|06:19|DAL|G.Pickens|Prescott goes to work quickly to the outside. Pass caught by Pickens stays in bounds.|27|unknown|unknown|unknown|unknown|verified vs DB|
|06:33|DAL|C.Lamb|Pressure to the outside. Pass caught and inbounds by Lamb staying in.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:46|DAL|D.Prescott|Third down and six. Down he goes before he can get the pass away. Sacked by David Walker.|None|unknown|unknown|unknown|D.Walker|unverified (no DB match; caption-only)|
|06:57|DAL|B.Aubrey|41 yard field goal attempt for Aubrey is good.|41|unknown|unknown|unknown|unknown|verified vs DB|
|07:15|TB|B.Irving|Keep it on the ground. Irving this way and that way. Past the 40 into Dallas territory. 72 yard run.|72|unknown|unknown|unknown|unknown|verified vs DB|
|07:49|TB|E.Egbuka|On the end around inside the 10 all the way to the end zone. Egbuka for the touchdown.|14|unknown|unknown|unknown|unknown|verified vs DB|
|08:19|DAL|G.Pickens|Dak looks that way back. Throws. Caught by Pickens to the 32 yard line.|27|unknown|unknown|unknown|I.Melifonwu|verified vs DB|
|08:36|DAL|D.Prescott|Tipped and in the air. Picked off by Yaya Diaby.|None|unknown|unknown|unknown|unknown|verified vs DB|
|08:50|TB|T.Johnson|Daniels deep down wide open. Tez Johnson all the way deep into Dallas territory. 64 yard gain.|64|deep shot|unknown|unknown|M.Hooker|verified vs DB|
|09:22|TB|B.Irving|Irving for the touchdown from 1 yard out.|1|unknown|unknown|unknown|unknown|verified vs DB|
|09:42|DAL|K.Turpin|Turpin fumbles out past the 30 yard line. Recovered by Buccaneers.|None|unknown|unknown|unknown|M.Killebrew|verified vs DB|
|10:51|TB|E.Egbuka|Rush for pressure thrown. That is Egbuka. 21 yard gain to the 27.|21|unknown|unknown|unknown|D.Bland|verified vs DB|
|11:19|TB|unknown|Flips it caught. Stumbles Gainwell to the 23. 41 yard field goal attempt coming up.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:29|TB|C.McLaughlin|41 yard field goal attempt. Right down the middle. Good.|41|unknown|unknown|unknown|unknown|verified vs DB|
|12:16|TB|B.Irving|Breaks two tackles. Bucky Irving takes it to the 32 yard line.|22|unknown|unknown|unknown|unknown|verified vs DB|
|13:24|DAL|R.Flournoy|Breathing room and the pass is caught. Flournoy gets him out to the 18 yard line.|26|unknown|unknown|unknown|unknown|verified vs DB|
|13:41|DAL|K.Turpin|Prescott jostled. Throws up at the 32 that is caught there by Turpin. First down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:50|DAL|G.Pickens|Catch made Pickens. Gain of 13. Quick slants.|20|unknown|unknown|unknown|T.Smith|verified vs DB|
|14:05|DAL|G.Pickens|Pickens on the move. Little hurdle job there. Takes the ball to the 31 yard line.|18|unknown|unknown|unknown|unknown|verified vs DB|
|14:25|DAL|G.Pickens|To the end zone. Reaching up. Pickens catches it for the touchdown.|18|unknown|unknown|unknown|unknown|verified vs DB|
|15:20|DAL|J.Ferguson|Ferguson wide open cuts to the inside to the 31.|26|unknown|unknown|unknown|unknown|verified vs DB|
|15:34|DAL|R.Flournoy|Pass to the outside. Spinning around picking up the first and a lot more. Ryan Flournoy to the 44 yard line.|26|unknown|unknown|unknown|unknown|verified vs DB|
|15:49|DAL|G.Pickens|Dak throws caught on the other side of the 50. Pickens taken down by a quartet of Bucs.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|16:04|DAL|unknown|Prescott fires loose. The catch is there. A yard shy of the first down for Mingo.|None|unknown|unknown|unknown|K.Scott|unverified (no DB match; caption-only)|
|16:36|DAL|D.Prescott|Prescott under pressure. Fires over the middle. It's deflected and picked off by Alex Anzalone. Intended for Jake Ferguson.|None|unknown|unknown|unknown|A.Anzalone|verified vs DB|

Offense (model synthesis from this game's plays): Big play passing with multiple 20+ yard completions to G.Pickens and R.Flournoy / Ability to score quickly in bunches with deep shots and red zone efficiency / Versatile run game mixing inside and outside concepts

Defense weaknesses: Poor tackling allowing long runs by B.Irving for big gains and TDs / Secondary issues with blown coverages leading to wide open deep receptions / Frequent missed tackles and inability to set the edge on outside runs / Vulnerable to sustained offensive drives by opponent

Limitations: Could not determine specific concepts like run gaps/directions, personnel formations, or coverage schemes because commentators did not explicitly state them. Many plays in captions had no clear match to DB due to incomplete or vague descriptions. Some player names corrected using DB only on clear matches. Yards often not precisely stated in captions so used DB values where matched. Several caption plays had no DB equivalent.


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

Offense (model synthesis from this game's plays): The goal-line touchdown used an extra eligible lineman and Spann-Ford at fullback for Williams's middle run. / Commentary identifies slants as available against Green Bay's blitz looks near the 11:42 completion. / Flournoy supplied a first-down reception with a broken tackle and the late receiving touchdown.

Defense weaknesses: Love completed the 21-yard pass to Golden despite Downs's pressure and hit. / Porter Jr.'s 37-yard pass-interference penalty extended Green Bay's late-first-half possession. / The defensive front yielded Love's 1-yard sneak touchdown; commentary specifically describes Clark being moved backward.

Limitations: Captions are fragmented and provide no visual evidence. Several entries identify only partial actions or pre-snap situations; these are explicitly marked. Formation and coverage details are included only when spoken, with tentative calls preserved as tentative. Named tacklers do not establish who lost coverage. Interception yards follow DB return yardage; the nullified Valentine return has null yards. No caption segment confidently establishes either Watson gain, Golden's 21-yard first-half catch, Pickens's late 21-yard catch, any kickoff, or a made field goal, so those DB events are not added independently. DB-only shotgun labels are excluded from personnel_formation. Reversed and nullified touchdowns/interceptions are not counted as scores or valid turnovers.
