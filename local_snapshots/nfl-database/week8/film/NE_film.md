# NE — Phase 8 film notes (Weeks 1–6, 2026)
> Note: games 401872946, 401872957, 401872971, 401872986 were extracted by Grok via the xAI API (grok-4.20-0309-non-reasoning, same prompt/schema as Codex, cleaned captions); sidecar provenance in film/grok_meta/. All other games with notes: Codex.

Method: NFL YouTube channel full-game highlight videos were located by search and their auto-captions (broadcast commentary) downloaded via yt-dlp. Codex (codex-cli 0.163.0) extracted plays from the captions. **No video frames were viewed by any agent.** Each play was checked against the repo DB play-by-play: `verified vs DB` means the cited DB play exists and the yardage matches. Personnel, formation and coverage appear only when commentators stated them; everything else is `unknown`.


## Week 1: NE 10 - SEA 13 (game 401872656)
Video: New England Patriots vs. Seattle Seahawks Game Highlights Week 1 | NFL 2026 — https://www.youtube.com/watch?v=hyEng1b5j8o  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:24|SEA|Jadarian Price|Opening rushing play; commentary reports a gain of 13.|13|run, direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:41|SEA|Sam Darnold|Pumps on third-and-6 and is sacked by Jones against an extra rusher.|None|unknown|unknown|man-to-man on the outside, described immediately afterward|Jones (sacker; first name unspecified)|unverified (no DB match; caption-only)|
|00:54|SEA|unknown|Retrospective commentary says Carlton Davis nearly intercepted the first throw for a potential pick-six.|None|unknown|unknown|man-to-man on the outside|Carlton Davis (nearly intercepted)|unverified (no DB match; caption-only)|
|00:59|SEA|George Holani|Receives a handoff; result is missing.|None|run, direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:44|NE|Drake Maye|Escapes pursuit on third-and-5. An out-of-bounds hit draws an unnecessary-roughness penalty; commentary tentatively identifies Derick Hall.|None|unknown|unknown|unknown|Derick Hall (tentative identification of penalized defender)|unverified (no DB match; caption-only)|
|02:32|NE|unknown|Commentary credits an unnamed receiver with a key third-down conversion against Devon Witherspoon.|None|unknown|unknown|unknown|Devon Witherspoon|unverified (no DB match; caption-only)|
|02:55|NE|Drake Maye / A.J. Brown|Third-and-2 flea-flicker deep toward Brown draws defensive pass interference on Josh Jobe. DB records a 34-yard penalty and no play; captions say 35.|34|flea-flicker deep shot|unknown|unknown|Josh Jobe|verified vs DB|
|03:38|NE|Eli Raridon|Catches Maye's 2-yard touchdown pass short left.|2|short-left pass|Gilliam at fullback; Stevenson at tailback|unknown|unknown|verified vs DB|
|04:11|SEA|Jaxon Smith-Njigba|Drew Lock completes a deep-middle pass for 21 yards on the third-and-22 sequence. Receiver and yardage are supplied by the matching DB entry.|21|deep-middle pass|unknown|unknown|C. Woodson (DB tackler)|verified vs DB|
|04:27|NE|Rhamondre Stevenson|Runs left and runs into his offensive lineman; final result is missing.|None|run left|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:29|NE|Mitch Wishnowsky|On fourth-and-4, Chazz Surratt gets to the punter and a personal foul gives New England a first down.|None|punt|unknown|unknown|Chazz Surratt (penalized defender)|unverified (no DB match; caption-only)|
|05:53|NE|Rhamondre Stevenson|Stevenson play stopped by Nwosu; commentary praises the defensive play without supplying yardage.|None|unknown|three receivers|unknown|Nwosu (made the defensive play)|unverified (no DB match; caption-only)|
|06:12|NE|A. Borregales|Makes a 50-yard field goal, extending New England's lead to 10-0; success is established by the DB.|50|field goal|unknown|unknown|unknown|verified vs DB|
|06:44|NE|Rhamondre Stevenson|Catches Maye's underneath throw from the end zone and is stopped at the NE 10 against a four-man rush.|None|underneath pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:07|SEA|Cooper Kupp|Catches Lock's deep-right pass for 24 yards on third-and-3, reaching the NE 13. Commentary describes stacking Kupp behind another player to ensure his release; Holani stays in to block.|24|deep-right pass|Kupp stacked behind another player; Holani stays in to block|unknown|M. Jones (DB tackler)|verified vs DB|
|07:40|SEA|Drew Lock|Patriots bring pressure. Commentary describes separation involving Carlton Davis, but disrupted timing produces a missed pass; target is unclear.|None|unknown|unknown|man coverage described in the surrounding sequence|Carlton Davis (disrupted timing)|unverified (no DB match; caption-only)|
|07:46|SEA|Jason Myers|Makes a 30-yard field goal to cut the deficit to 10-3; success is established by the DB.|30|field goal|unknown|unknown|unknown|verified vs DB|
|08:13|NE|Drake Maye / Romeo Doubs|Protected play-action deep left toward Doubs is deflected with Rodney Thomas covering and intercepted by Nehemiah Pritchett. DB records a 30-yard return to SEA 33; captions say the 34.|None|play-action deep shot|unknown|unknown|Rodney Thomas (coverage); Nehemiah Pritchett (interception)|verified vs DB|
|09:27|SEA|Jaxon Smith-Njigba|Catches Lock's short-left pass and scores a 45-yard touchdown. Commentary anticipates a one-on-one opportunity and then describes ample space. Later commentary identifies the touchdown pass as occurring on fourth-and-short.|45|short-left pass|unknown|one-on-one matchup anticipated by commentator; full scheme unknown|unknown|verified vs DB|
|09:54|NE|unknown|A defender gets around Jared Wilson on a play resulting in a loss of 4. Ball carrier and play type are unclear.|-4|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:06|NE|Drake Maye|Moves outside, keeps his eyes downfield and throws; the unidentified target cannot bring it in.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:17|NE|Drake Maye / D. Douglas|On third-and-14 against a twisting four-man rush, Maye throws deep middle and Julian Love intercepts. DB records no return, despite captions describing a return to the 32.|None|deep-middle pass|unknown|unknown|Julian Love (interception)|verified vs DB|
|10:38|SEA|unknown|Retrospective commentary identifies a third-and-3 run that set up fourth-and-very-short before the touchdown pass.|None|run, direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:59|SEA|Drew Lock|Looks toward Cooper Kupp and throws; destination and outcome are cut off.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:11|SEA|Drew Lock|With receivers covered, scrambles from the NE 17 and turns the corner, finishing just short of a first down.|None|quarterback scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:43|SEA|Drew Lock / Jaxon Smith-Njigba|On third-and-6, Lock goes left and throws toward Smith-Njigba from a backfield alignment. Exact result is missing; Seattle subsequently settles for a field goal.|None|pass left|Smith-Njigba in the backfield|unknown|unknown|unverified (no DB match; caption-only)|
|11:54|SEA|Jason Myers|Makes the go-ahead 26-yard field goal for a 13-10 lead; success is established by the DB.|26|field goal|unknown|unknown|unknown|verified vs DB|
|11:59|NE|unknown|An offensive player restricts Derick Hall with his left hand on the shoulder pad, drawing a penalty that leaves first-and-20.|None|unknown|unknown|unknown|Derick Hall (held)|unverified (no DB match; caption-only)|
|12:14|NE|Drake Maye|Murphy pressures up the middle and additional defenders finish the sack.|None|unknown|unknown|unknown|Murphy (initial pressure); finishers unidentified|unverified (no DB match; caption-only)|
|12:26|NE|Drake Maye|Takes a deep drop and completes a middle throw from a clean pocket; receiver and gain are missing.|None|pass middle|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:39|NE|Drake Maye|Runs out of bounds on a fourth-down conversion, confirmed retrospectively at 13:48.|None|quarterback run, design unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:53|NE|Rhamondre Stevenson|Makes a run praised by the announcer with 3:42 remaining; gain and direction are missing.|None|run, direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:54|NE|Drake Maye|Commentary describes an available tight-end screen that Maye did not throw and Vera-Tucker starting early; a penalty backs New England up.|None|intended tight-end screen|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:19|NE|Drake Maye|Faces pressure on the late drive; the caption cuts off before the outcome.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:30|NE|Hunter Henry|Maye has time on third-and-long and throws toward Henry; completion and gain are not explicitly preserved.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:41|NE|Mack Hollins|Fourth-and-9 conversion attributed to Hollins in the surrounding commentary. Seattle shows pressure and backs out; commentary calls Hollins the team's zone buster.|None|unknown|unknown|zone|unknown|unverified (no DB match; caption-only)|
|14:44|NE|Drake Maye / Mack Hollins|After the quick look is closed, Maye throws a deep-right end-zone jump ball for Hollins. Josh Jobe intercepts for a touchback; DB also credits pressure to D. Lawrence.|None|deep-right end-zone jump ball|unknown|unknown|Josh Jobe (interception)|verified vs DB|
|15:34|SEA|Drew Lock|Takes a knee to close the game.|None|quarterback kneel|unknown|unknown|unknown|unverified (no DB match; caption-only)|

Offense (model synthesis from this game's plays): The flea-flicker toward A.J. Brown drew a 34-yard pass-interference penalty, followed by Raridon's 2-yard touchdown reception. / The final drive included fourth-down conversions through Maye's running and a play attributed to Hollins against zone. / An unnamed receiver converted a third down against Witherspoon.

Defense weaknesses: Allowed Lock's 21-yard middle completion to Smith-Njigba and 24-yard deep-right completion to Kupp. / Allowed Smith-Njigba's 45-yard touchdown on a short-left pass after commentary anticipated a one-on-one opportunity.

Limitations: Captions only; no frames were viewed or commands run. Fragmented captions leave many gains, targets, outcomes and play boundaries unknown. Isolated pre-snap discussion and fragments without an identifiable action were omitted. DB entries were matched only where the sequence clearly supported them; DB-only kickoffs were not added. For interceptions, yards is null because passing yardage is not supplied; return yardage is described separately. Field-goal yards denotes kick distance, and the flea-flicker entry uses penalty yardage. Named defenders include tacklers, interceptors and defenders who won their matchup; their inclusion does not mean they were beaten. Formation and coverage details come only from commentary; nearby coverage discussion may not establish a complete scheme. Caption/DB discrepancies were resolved in favor of the supplied authoritative DB.


## Week 2: PIT 3 - NE 20 (game 401872946)
Video: Pittsburgh Steelers vs. New England Patriots Game Highlights | NFL Week 2 — https://www.youtube.com/watch?v=HMeTHt77nYE  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:18|NE|Borregales|Kickoff|61|unknown|unknown|unknown|unknown|verified vs DB|
|00:21|PIT|Wetjen|Kickoff return|26|unknown|unknown|unknown|unknown|verified vs DB|
|00:44|NE|Maye|Pass across the middle to Pop Douglas|9|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:00|NE|Maye|Pass to Henry for a gain of 30|30|deep shot|unknown|unknown|unknown|verified vs DB|
|01:15|NE|Maye|Pass to Stevenson, fumble|3|unknown|unknown|unknown|Herbig|verified vs DB|
|01:33|PIT|Rodgers|Pass intended for Freiermuth, incomplete on 3rd and 6|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:48|NE|Marcus Jones|Punt return|48|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:02|PIT|Ramsey|Penalty on defense (offside)|5|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:18|NE|Henderson|Rushing touchdown left guard|39|run gap/direction|Shotgun|unknown|unknown|verified vs DB|
|02:36|PIT|Rodgers|Completion to Freiermuth, first completion|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:53|PIT|Washington|Run for 7 yards|7|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:00|PIT|Rodgers|Pass on 3rd and 6, blitzed and incomplete|0|unknown|unknown|unknown|Spillane|unverified (no DB match; caption-only)|
|03:09|PIT|Boswell|57 yard field goal missed wide left|57|unknown|unknown|unknown|unknown|verified vs DB|
|03:23|NE|Dodd|First catch as a Patriot, lost football going out of bounds but ruled catch|None|unknown|unknown|unknown|Dean|unverified (no DB match; caption-only)|
|03:39|NE|Raridon|Catch of 29 yards (first and goal from the 11)|29|deep shot|unknown|unknown|Wilson|CONFLICT (yardage 29 vs DB)|
|03:45|NE|Maye|Sacked at the 14 by T.J. Watt|-3|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:12|NE|Borregales|30 yard field goal good|30|unknown|unknown|unknown|unknown|verified vs DB|
|04:24|PIT|Rodgers|High snap, handoff to Warren short of first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:37|PIT|Freiermuth|Push from behind for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:48|PIT|Rodgers|Pass to Bernard for first down, gain of 19|19|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:00|PIT|Rodgers|Pass to Bernard|None|unknown|unknown|unknown|Farmer|unverified (no DB match; caption-only)|
|05:13|PIT|Rodgers|Sacked and fumble recovered by Fautanu|-9|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:38|NE|Maye|Pass to Mack Hollins near the sticks|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:51|NE|Maye|Pass batted down by Highsmith|0|unknown|unknown|unknown|Highsmith|unverified (no DB match; caption-only)|
|06:00|NE|Homer|Run up the middle for 14 yards|14|run gap/direction|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:16|NE|Maye|Pass almost caught by Freiermuth, flag out|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:24|NE|Maye|Pass incomplete down the middle, covered by Marcus Jones|0|unknown|unknown|unknown|Marcus Jones|unverified (no DB match; caption-only)|
|06:37|NE|Maye|Sacked by T.J. Watt inside the 10|-10|unknown|unknown|unknown|Watt|unverified (no DB match; caption-only)|
|06:50|NE|Henderson|Run across the 20|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:00|PIT|Freiermuth|Stopped a yard short|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:09|PIT|Freiermuth|Gets around the corner for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:24|PIT|Rodgers|Delay of game penalty|5|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:39|PIT|Rodgers|Pass to Wilson for gain of 9|9|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:51|PIT|Boswell|56 yard field goal good|56|unknown|unknown|unknown|unknown|verified vs DB|
|08:18|NE|Williams|Kickoff return for 29 yards|29|unknown|unknown|unknown|unknown|verified vs DB|
|08:25|NE|Maye|Pass deep to Doubs for 63 yards|63|deep shot|unknown|unknown|unknown|verified vs DB|
|08:37|NE|Maye|Pass intercepted by Patrick Queen|3|unknown|unknown|unknown|unknown|verified vs DB|
|09:16|PIT|Warren|Run for gain of 8|8|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:24|PIT|Rodgers|Pass incomplete on 3rd and 6|0|unknown|unknown|unknown|Woods|unverified (no DB match; caption-only)|
|09:39|PIT|Rodgers|Pass complete to Hollins|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:50|NE|Maye|Pass up the middle caught by Williams for 9 yards|9|unknown|unknown|unknown|Jacobs|unverified (no DB match; caption-only)|
|10:02|NE|Stevenson|Run for 24 yards to the 35 (jersey ripped)|24|run gap/direction|unknown|unknown|Samuel|verified vs DB|
|10:11|NE|Chism|Quick toss, immediate contact|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:20|NE|Borregales|47 yard field goal missed wide right|47|unknown|unknown|unknown|unknown|verified vs DB|
|10:37|PIT|Metcalf|Drop|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:46|NE|Maye|Pass to Doubs for big play of about 60 yards|60|deep shot|unknown|unknown|unknown|CONFLICT (yardage 60 vs DB)|
|11:02|NE|Maye|Pass thrown away under pressure on 3rd and 8|0|unknown|unknown|unknown|Wilson|unverified (no DB match; caption-only)|
|11:10|NE|Borregales|45 yard field goal good|45|unknown|unknown|unknown|unknown|verified vs DB|
|11:26|NE|Dowdle|Run for first down, 13 yards|13|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:36|PIT|Rodgers|Pass to Metcalf, holding penalty on offense|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:01|PIT|Rodgers|Sacked, fumble recovered by Ponder for touchdown|-9|unknown|Shotgun|unknown|Barmore|verified vs DB|
|12:18|PIT|Rodgers|Sacked for loss of 11 on 3rd and 5|-11|unknown|unknown|unknown|Elliss|unverified (no DB match; caption-only)|
|12:28|NE|Maye|Scramble for first down, 13 yards|13|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:39|NE|Maye|Pass dropped by Doubs on 3rd and 9|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:53|PIT|Warren|Run, tripped up by Gonzalez|None|unknown|unknown|unknown|Gonzalez|unverified (no DB match; caption-only)|
|13:05|PIT|Wilson|Scoop up low pass for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:18|PIT|Metcalf|Catch, twisted down at NE 45|None|unknown|unknown|unknown|Byard|unverified (no DB match; caption-only)|
|13:24|PIT|Washington|Run for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:34|PIT|Warren|Run inside the 2, down to the 3|None|unknown|unknown|unknown|unknown|verified vs DB|
|13:52|PIT|Rodgers|Sacked at the 20 by Ponder|-17|unknown|unknown|unknown|Ponder|unverified (no DB match; caption-only)|
|14:06|PIT|Rodgers|Pass intercepted by Jacas|11|unknown|unknown|unknown|unknown|verified vs DB|
|14:19|NE|Henderson|Run for 5 yards on 3rd and 10|5|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|

Offense (model synthesis from this game's plays): Explosive deep passing attacks with multiple 29+ yard completions to receivers like Doubs and Henry / Effective outside runs and scrambles by RBs and QB Maye gaining 20+ yards / Capitalizing on short fields and turnovers for scoring opportunities

Defense weaknesses: Allowing sustained drives and third down conversions by Pittsburgh / Vulnerable to runs by Warren getting inside the 5-yard line / Missed opportunities on sacks and pressures not resulting in turnovers until late

Limitations: Could not determine specific concepts like RPO/play-action, personnel formations, or coverage schemes as they were not explicitly stated by commentators; many plays in captions did not have direct DB matches due to name mangling and incomplete details; exact yardage often not specified in captions for non-highlighted plays.


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

Offense (model synthesis from this game's plays): Explosive deep passes and long receptions (38yd to Douglas, 34yd to Williams, 21yd to Hollins) / Ability to convert on third downs with accurate passing

Defense weaknesses: Susceptible to big passing plays over the middle and in zone coverage / Frequent turnovers forced by pressure (multiple INTs and fumble) / Poor red zone defense allowing multiple touchdowns / Vulnerable to run game in short yardage and goal line situations

Limitations: Could not determine specific personnel, formations, or coverage schemes as they were not explicitly stated by commentators. Some plays in captions were vague or did not perfectly align with DB details so yards and exact concepts were conservatively assigned only when clear. Many caption name manglings were corrected only for clear DB matches. Could not identify every single play mentioned due to caption incompleteness and lack of video.


## Week 4: NE 29 - BUF 26 (game 401872971)
Video: New England Patriots vs. Buffalo Bills Game Highlights | NFL 2026 Season Week 4 — https://www.youtube.com/watch?v=Z5zAM_GLGI0  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:25|NE|D.Maye|Maye gets out of the end zone, tucks and runs for a first down|15|unknown|unknown|unknown|D.Williams|unverified (no DB match; caption-only)|
|00:41|NE|D.Maye|Maye throws to the open man, sliding grab by tight end|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:53|NE|D.Maye|Maye hooks up with tight end Hunter Henry for a first down|None|unknown|unknown|unknown|unknown|verified vs DB|
|01:23|NE|D.Maye|Maye to Romeo Doubs for a first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:33|NE|D.Maye|Maye play-action, touchdown to Romeo Doubs|14|play-action|unknown|man to man|Hairston; C.Bishop|verified vs DB|
|02:04|BUF|J.Allen|Allen downfield to D.J. Moore for 10 yards and a first down|10|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:15|BUF|J.Allen|Allen to D.J. Moore, tackled short of first down by Spillane|None|unknown|unknown|unknown|R.Spillane|unverified (no DB match; caption-only)|
|02:21|BUF|J.Allen|Allen fakes handoff, flips it ahead to Shakir for 5-yard pickup|5|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:33|BUF|J.Allen|Allen puts one high, Keon Coleman climbs the ladder for first down|None|unknown|unknown|zone|unknown|unverified (no DB match; caption-only)|
|02:45|BUF|J.Allen|Allen puts it underneath to Shakir for first down|None|unknown|unknown|unknown|C.Davis|unverified (no DB match; caption-only)|
|02:59|BUF|J.Cook|James Cook hurdles for touchdown|8|unknown|unknown|unknown|C.Davis|verified vs DB|
|03:39|NE|D.Maye|Shovel pass to Hunter Henry|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:49|NE|Unknown|Up the middle run for Henderson, 3-yard pickup|3|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:56|NE|D.Maye|Maye loses the ball, fumble recovered by Greg Gaines|-7|unknown|unknown|unknown|T.Parker; E.Oliver|verified vs DB|
|04:17|BUF|J.Allen|Allen takes a deep shot downfield, dropped by Palmer|None|deep shot|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:41|NE|D.Maye|Maye downfield to Hollins for a first down|26|unknown|unknown|unknown|D.Igbinosun|verified vs DB|
|04:51|NE|D.Maye|Maye out of the pocket, scrambles for 26 yards to the 1|26|unknown|unknown|unknown|D.Alford; C.Bishop|verified vs DB|
|05:01|NE|R.Stevenson|Stevenson takes it in for the touchdown|1|unknown|unknown|unknown|unknown|verified vs DB|
|05:23|BUF|J.Allen|Allen short one to Knox, falls forward just short of first down|None|unknown|unknown|unknown|C.Elliss|unverified (no DB match; caption-only)|
|05:39|BUF|J.Allen|Allen avoids pressure, throws on the move, catch and run by Shakir|51|unknown|unknown|unknown|C.Woods; C.Woodson|verified vs DB|
|05:56|BUF|J.Allen|Quarterback sneak, touchdown Buffalo|2|QB sneak|unknown|unknown|unknown|verified vs DB|
|06:24|NE|D.Maye|Maye hit as he throws, incomplete|0|unknown|unknown|unknown|B.Chubb|unverified (no DB match; caption-only)|
|06:31|BUF|J.Allen|Allen finds open man, Keon Coleman steps out of bounds|22|unknown|unknown|unknown|unknown|verified vs DB|
|06:53|BUF|J.Allen|Allen with a short pass to Shakir, who loses the ball, fumble recovered by NE|8|unknown|unknown|unknown|R.Spillane|verified vs DB|
|07:09|NE|D.Maye|Maye throws, ball popped up, intercepted|0|unknown|unknown|unknown|D.Alford|verified vs DB|
|07:40|BUF|Unknown|27-yard field goal for Tyler Bass, Bills take the lead|27|unknown|unknown|unknown|unknown|verified vs DB|
|07:51|NE|D.Maye|Maye fakes handoff, out of pocket, throws caught along sideline|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:02|NE|D.Maye|Maye steps up, on the move, 13-yard tuck and run|13|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:16|NE|D.Maye|Maye to Mack Hollins for 19 yards|19|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:26|NE|D.Maye|Maye on the out route complete to Doubs|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:42|NE|D.Maye|One-handed snare by Doubs for the touchdown|2|unknown|unknown|unknown|G.Rousseau|verified vs DB|
|09:05|BUF|J.Allen|Allen underneath to Coleman, nowhere to go|None|unknown|unknown|unknown|C.Davis|unverified (no DB match; caption-only)|
|09:16|NE|D.Maye|Maye hit as he throws, connection with Douglas for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:24|NE|D.Maye|Big-time throw for 9 yards, took a shot from Deone Walker|9|unknown|unknown|unknown|D.Walker|unverified (no DB match; caption-only)|
|09:29|NE|D.Maye|Maye hit as he throws once again, incomplete|0|unknown|unknown|unknown|G.Rousseau|unverified (no DB match; caption-only)|
|09:38|BUF|J.Cook|Cook's got room, works the sideline, longest run of the day|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:49|BUF|J.Cook|Cook again, back-to-back long runs, 10-yard pickup|10|unknown|unknown|unknown|C.Elliss|unverified (no DB match; caption-only)|
|10:06|BUF|J.Allen|Allen, on a 50-50 ball, Keon Coleman makes the adjustment for first down|22|unknown|unknown|unknown|K.Vildor|verified vs DB|
|10:19|BUF|J.Allen|Allen dials it up, Johnson could not get around the defender, no gain|0|unknown|unknown|unknown|M.Jones|unverified (no DB match; caption-only)|
|10:29|BUF|Unknown|Field goal is good, 21-20 Patriots lead|38|unknown|unknown|unknown|unknown|verified vs DB|
|10:42|NE|Unknown|Toss to Henderson, splits defenders, 7.5 yards on the carry|8|unknown|unknown|unknown|D.Hamlin|unverified (no DB match; caption-only)|
|10:55|NE|D.Maye|Maye throws underneath to Stevenson, marked down at the 42|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:07|BUF|J.Cook|Cook with a running lane, caught from behind by Craig Woodson|16|unknown|unknown|unknown|C.Woodson|unverified (no DB match; caption-only)|
|11:29|BUF|J.Allen|Allen on time to Keon Coleman for a big gain, 24 yards|24|unknown|unknown|unknown|K.Byard|verified vs DB|
|11:47|BUF|J.Allen|Allen to the end zone, touchdown to Keon Coleman|34|deep post|unknown|unknown|C.Woods|verified vs DB|
|12:28|NE|D.Maye|Maye loads it up, sliding grab by Henry for a first down, 14 yards|14|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:40|NE|D.Maye|Maye gets it downfield, catch by Doubs for 12 yards|12|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:53|NE|D.Maye|Maye rifles downfield, hauled in by Chism for 19 yards|19|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:03|NE|D.Maye|Maye out of the pocket, launches downfield, touchdown to Chism|23|unknown|unknown|unknown|D.Igbinosun|verified vs DB|
|13:54|NE|D.Maye|Maye throws, catch by Stevenson for two-point conversion|None|unknown|unknown|unknown|unknown|verified vs DB|
|14:13|BUF|J.Allen|Allen downfield, intercepted by Craig Woodson|0|unknown|unknown|unknown|C.Woodson|verified vs DB|

Offense (model synthesis from this game's plays): Red zone efficiency (3-3 on TDs) / Improvisation by QB Drake Maye leading to big gains and TDs / Effective use of play-action and shovel passes / Explosive plays including long scrambles, deep passes, and contested catches by receivers like Doubs, Hollins, Henry, and Chism

Defense weaknesses: Struggled to contain mobile QB Josh Allen on scrambles and sneaks / Missed tackles and poor pursuit on runs by James Cook allowing long gains / Vulnerable to big passing plays over the middle and deep, especially to Keon Coleman / Defensive backs beaten on 50-50 balls and in coverage on TDs

Limitations: Could not determine exact personnel formations, most specific run gaps/directions, or coverage schemes beyond what was explicitly stated in commentary; many plays had no direct DB match or lacked specific yardage/defender details in captions; some names mangled in auto-captions (e.g. RARIDON for Henry, HENDERSON for possible RB, DOUGLAS for possible receiver) corrected only where clear match to DB; several non-highlight or non-scoring plays not listed if no clear identification.


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

Offense (model synthesis from this game's plays): Efficient deep passing attacks with multiple touchdown passes over 30 yards / Strong red zone efficiency with both rushing and passing touchdowns / Explosive plays from running backs on outside runs and receivers on catch and runs

Defense weaknesses: Allowed multiple chunk plays to tight end Bowers and other receivers in the middle of the field / Defensive holding penalties that were declined but indicated pressure issues / Vulnerable to screen plays and quick passes leading to long gains

Limitations: Could not determine specific personnel formations or coverage schemes as they were not explicitly stated by commentators. Many plays in captions had mangled names and incomplete details making exact matching to DB difficult; only clear matches were used. Several described plays had no direct DB match. Yardage sometimes estimated from commentary without exact confirmation. Auto-generated captions had many errors and jumps in continuity.


## Week 6: NYJ 19 - NE 26 (game 401873001)
Video: New York Jets vs New England Patriots Game Highlights | 2026 NFL Season Week 6 — https://www.youtube.com/watch?v=CDcGaEkMy6s  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:16|NYJ|Geno Smith; Mason Taylor|Play-action completion to Taylor to begin the drive.|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:26|NYJ|Allen|Handoff to Allen; result is cut off.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:31|NYJ|Geno Smith; Garrett Wilson|Completion to Wilson; endpoint and gain are unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:41|NYJ|Geno Smith; Mason Taylor|Pass intended for Taylor is batted down near the end zone.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:52|NYJ|J. Sanders|Makes a 42-yard field goal for the opening points.|42|field goal|unknown|unknown|unknown|verified vs DB|
|00:59|NE|Drake Maye|Third-and-three pass is batted down at the line by a defender identified as Davis.|0|unknown|unknown|unknown|Davis (pass deflection; not beaten)|unverified (no DB match; caption-only)|
|01:11|NYJ|Geno Smith|Sacked against a Patriots blitz on second-and-nine.|None|unknown|unknown|blitz|unknown|unverified (no DB match; caption-only)|
|01:26|NYJ|Geno Smith|Sacked again as New England sends five; commentary credits Farmer.|None|unknown|unknown|five-man pressure|Farmer (sack; not beaten)|unverified (no DB match; caption-only)|
|01:33|NE|Drake Maye; A.J. Brown|Misdirection and a fake to Henderson precede an apparent Brown catch. Commentary mentions a challenge; its outcome is unclear.|None|misdirection; play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:45|NE|D. Maye; R. Doubs|With only three rushing, Maye has time to find Doubs deep right for a 42-yard touchdown. Commentary describes a safety coming down on an in-cut and vacating the middle.|42|deep shot|unknown|three-man rush; safety vacates middle|unknown|verified vs DB|
|02:23|NYJ|Geno Smith; Allen|Smith gets the ball to Allen, who takes on tacklers, including a defender captioned as Craig Woodson. Delivery type is unclear.|None|unknown|unknown|unknown|Craig Woodson (caption rendering; tackle interaction)|unverified (no DB match; caption-only)|
|02:33|NYJ|Allen|Run reaches the second level for a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:43|NYJ|Allen|Another run breaks the initial tackle. Analyst says the Jets repeated the same play to the opposite side.|None|repeat run to opposite side; specific run concept unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:54|NYJ|Geno Smith; Davis|Smith releases to Davis under pressure on a screen described as well set up.|None|screen|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:06|NYJ|Allen|Allen is stopped short with Spillane at the tackle; Patriots show six at the line.|None|unknown|unknown|six defenders shown at line; rush and coverage unknown|Spillane (stop; not beaten)|unverified (no DB match; caption-only)|
|03:15|NE|Rhamondre Stevenson|Fights forward to the 35-yard line.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:25|NE|Drake Maye; A.J. Brown|Shot toward Brown falls incomplete through his hands as pressure comes up the middle.|0|deep shot|shotgun|unknown|unknown|unverified (no DB match; caption-only)|
|03:50|NE|Drake Maye|High pass to the far side is incomplete, leading to a punt.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:01|NYJ|Geno Smith; Omar Cooper Jr.|Play-action completion to Cooper with Allen picking up the blitz.|None|play-action|unknown|blitz|unknown|unverified (no DB match; caption-only)|
|04:11|NYJ|Davis|Davis runs around the edge with Wilson in motion; Gonzalez comes over to finish the play.|None|edge run; direction unspecified|Wilson in motion; personnel unknown|unknown|Christian Gonzalez (tackle involvement)|unverified (no DB match; caption-only)|
|04:22|NYJ|Geno Smith|Smith keeps the ball after commentary anticipates a 58-yard field-goal attempt. Conversion depends on the spot; outcome is not stated.|None|quarterback keeper|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:31|NE|Rhamondre Stevenson|Stays on his feet for a 12-yard first-down run, brought down by Sherwood.|12|unknown|unknown|unknown|Jamie Sherwood (tackler)|unverified (no DB match; caption-only)|
|04:44|NE|Drake Maye; Douglas|Trick sequence described as a backward lateral ends with Maye getting the ball to Douglas for an apparent first down.|None|backward-lateral trick play; exact sequence unclear|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:58|NE|Drake Maye; A.J. Brown|Underneath completion to Brown.|None|underneath pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:05|NE|Drake Maye; A.J. Brown|Third-and-four pass intended for Brown is incomplete against a five-man rush.|0|unknown|unknown|five-man pressure|unknown|unverified (no DB match; caption-only)|
|05:15|NE|A. Borregales|Makes a 32-yard field goal, extending the lead to 10-3.|32|field goal|unknown|unknown|unknown|verified vs DB|
|05:27|NYJ|Cooper|Pass to Cooper finishes short of the line to gain; preceding context is clipped.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:40|NE|Drake Maye; A.J. Brown|Completion to Brown gains 15 yards and a first down.|15|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:55|NE|Drake Maye; Douglas|Sidearm completion to Douglas; Maye is slow getting up afterward.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:01|NE|Drake Maye; receiver captioned as Eli Reardon|End-zone pass initially called a touchdown is ruled incomplete because the receiver cannot get his second foot down.|0|end-zone pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:18|NE|D. Maye; D. Douglas|Maye fakes and throws a nine-yard touchdown to Douglas. Commentary credits extended pocket time and Douglas uncovering.|9|fake before pass; extended-play touchdown|unknown|unknown|unknown|verified vs DB|
|06:39|NE|D. Maye|Steps up against pressure and scrambles 21 yards, tackled by Fitzpatrick.|21|scramble through right guard|unknown|unknown|M. Fitzpatrick (DB tackler)|verified vs DB|
|06:52|NE|Drake Maye; Douglas|Completion to Douglas finishes considerably short of a first down.|None|unknown|tight ends in backfield; personnel count unclear|unknown|unknown|unverified (no DB match; caption-only)|
|07:01|NE|Drake Maye; A.J. Brown|Fourth-and-five pass to Brown is incomplete; Stephens is credited with the defensive play.|0|unknown|unknown|unknown|Brandon Stephens (pass defense; not beaten)|unverified (no DB match; caption-only)|
|07:22|NYJ|Geno Smith; Jelani Woods|Smith rolls out off a fake and appears to complete to Woods for a drive-opening first down; captions are fragmented.|None|play-action rollout|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:32|NYJ|G. Smith; O. Cooper|Play-action rollout produces a 48-yard touchdown to Cooper deep left. Analyst describes a safety expecting help while the other safety plays low.|48|play-action rollout; deep shot|unknown|safety help breakdown; exact scheme unknown|Safety captioned as Craig Woodson (plays low); other defender's name unclear|verified vs DB|
|08:00|NE|Drake Maye; Douglas|On third-and-three, Maye escapes pursuit and completes along the sideline to Douglas.|None|extended-play sideline pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:15|NE|T. Henderson|Six-yard right-guard run ends with Bailey stripping the ball; Sherwood recovers for NYJ. DB says review upheld the fumble.|6|right-guard run|unknown|unknown|D. Bailey (forced fumble); J. Briggs (DB co-tackler); J. Sherwood (recovery)|verified vs DB|
|08:43|NYJ|Geno Smith; Sadiq|Second-and-short completion to an open Sadiq.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:53|NYJ|Geno Smith|Sacked on third-and-five back at the 21; defender's name is captioned as Ponder.|None|unknown|unknown|unknown|Ponder (caption rendering; sack, not beaten)|unverified (no DB match; caption-only)|
|09:04|NYJ|J. Sanders|Makes a 36-yard field goal after the takeaway, cutting the deficit to four.|36|field goal|unknown|unknown|unknown|verified vs DB|
|09:16|NE|Henderson|Misdirection gets Henderson to the edge for eight yards and a first down.|8|misdirection; edge run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:25|NE|Drake Maye; Kyle Williams|Protected throw to Williams gains a first down. Captions mention a man route but do not establish defensive man coverage.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:40|NE|Drake Maye; Hunter Henry|Completion over the middle to Henry gains another first down.|None|pass over middle|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:50|NE|D. Maye; H. Henry|Seven-yard touchdown pass to Henry. Analyst identifies linebacker-safety confusion and Davis expecting help.|7|short right pass|unknown|linebacker-safety assignment confusion; exact scheme unknown|Davis; unnamed safety|verified vs DB|
|10:16|NE|A. Borregales|Misses the extra point wide left after Henry's touchdown.|None|extra point|unknown|unknown|unknown|verified vs DB|
|10:25|NYJ|Geno Smith; Garrett Wilson|Completion to Wilson against Gonzalez as New England threatens pressure.|None|unknown|unknown|pressure shown; actual rush unknown|Christian Gonzalez|unverified (no DB match; caption-only)|
|10:33|NYJ|Geno Smith; Garrett Wilson|Hard fake precedes a third-and-two completion to Wilson. A flag is checked; Jets have a first down after the penalty.|None|hard fake before pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:53|NYJ|G. Smith; K. Sadiq|Deep-left pass intended for Sadiq is intercepted by C. Woods at the NE 24, with no return.|0|deep left pass|unknown|unknown|C. Woods (interception; not beaten)|verified vs DB|
|10:58|NE|D. Maye; D. Douglas|Third-and-six deep-right completion gains 39 yards before Sherwood forces a fumble. Fitzpatrick recovers and returns it 20 yards.|39|deep right pass|unknown|unknown|J. Sherwood (tackle and forced fumble); H. Henry (DB return tackler)|verified vs DB|
|11:24|NYJ|Geno Smith; Cooper|Cooper bobbles then secures a completion crossing the middle against Marcus Jones as New England sends an extra rusher.|None|crossing route|Sadiq in motion; personnel unknown|extra-rusher pressure|Marcus Jones|unverified (no DB match; caption-only)|
|11:38|NYJ|Geno Smith; Mason Taylor|Completion over the middle finishes just short of the line to gain; commentary calls it nine-plus yards.|None|pass over middle|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:48|NYJ|Geno Smith|Throws into the turf against a blitz.|0|unknown|unknown|blitz|unknown|unverified (no DB match; caption-only)|
|11:57|NYJ|J. Sanders|Makes a 40-yard field goal to cut the score to 23-16.|40|field goal|unknown|unknown|unknown|verified vs DB|
|12:05|NE|Drake Maye; Hunter Henry|Third-and-long completion to Henry finds substantial open space against a corner blitz.|None|unknown|unknown|corner blitz|Blitzer captioned as D'Angelo Ponce; coverage defender unknown|unverified (no DB match; caption-only)|
|12:20|NE|Kiner|Runs into the second level for 13 yards.|13|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:25|NE|Kiner|Slips a tackle and gains nine yards running downhill.|9|downhill run; gap unspecified|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:43|NE|Kiner|Another clock-draining run; gain is unstated.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:49|NE|Rhamondre Stevenson|Handoff ends with the result dependent on the spot; final ruling is absent.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:00|NE|A. Borregales|Makes a 27-yard field goal with 1:12 remaining for a 26-16 lead.|27|field goal|unknown|unknown|unknown|verified vs DB|
|13:13|NYJ|Geno Smith; Cooper Jr.|Underneath completion with blockers ahead gains 18 yards; Cooper exits out of bounds.|18|underneath pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:22|NYJ|Geno Smith; Mason Taylor|Late pass sequence names Taylor; catch result and yardage are not clearly stated.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:36|NYJ|Geno Smith; Mason Taylor|Pass intended for Taylor is batted down and incomplete.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:44|NYJ|J. Sanders|Makes a 36-yard field goal with 32 seconds remaining, making the score 26-19.|36|field goal|unknown|unknown|unknown|verified vs DB|
|13:53|NYJ|Kicker unidentified in captions; Douglas (NE recovery)|Onside kick sequence ends with Douglas jumping on the ball for New England, according to commentary.|None|onside kick|unknown|unknown|unknown|unverified (no DB match; caption-only)|

Offense (model synthesis from this game's plays): Maye converted extended pocket time into touchdowns to Doubs and Douglas and added a 21-yard scramble against pressure. / Henry supplied consecutive first-down and touchdown catches, then a significant late third-and-long completion. / Misdirection produced Henderson's eight-yard edge gain; Kiner contributed productive late clock-draining runs.

Defense weaknesses: The Jets repeatedly gained on Allen runs, including second-level access and a broken initial tackle. / A safety-help breakdown allowed Cooper's 48-yard play-action touchdown. / Cooper completed a crossing catch against Marcus Jones, and Wilson caught a pass against Gonzalez.

Limitations: Analysis uses only supplied captions and DB excerpts; no frames or external sources were accessed. The DB is selective, so NO DB MATCH does not mean a play did not occur. DB matches identify the supplied quarter/clock entry; formation and coverage fields use commentary only. Names on unmatched plays remain as supported by captions, including uncertain renderings. Named tacklers, sackers, and takeaway defenders are labeled by role and are not necessarily defenders beaten in coverage. Null yards indicate an unstated or ambiguous gain; field-goal yards are kick distance. The Douglas fumble entry uses the 39-yard offensive reception, with the 20-yard defensive return described separately. Kickoffs absent from the captions, the isolated unclear penalty reference, replay explanations, and the unrelated bonus-coverage fragment were not treated as additional plays.
