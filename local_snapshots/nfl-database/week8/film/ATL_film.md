# ATL — Phase 8 film notes (Weeks 1–6, 2026)
> Note: games 401872948, 401872979, 401872993 were extracted by Grok via the xAI API (grok-4.20-0309-non-reasoning, same prompt/schema as Codex, cleaned captions); sidecar provenance in film/grok_meta/. All other games with notes: Codex.

Method: NFL YouTube channel full-game highlight videos were located by search and their auto-captions (broadcast commentary) downloaded via yt-dlp. Codex (codex-cli 0.163.0) extracted plays from the captions. **No video frames were viewed by any agent.** Each play was checked against the repo DB play-by-play: `verified vs DB` means the cited DB play exists and the yardage matches. Personnel, formation and coverage appear only when commentators stated them; everything else is `unknown`.


## Week 1: ATL 13 - PIT 20 (game 401872658)
Video: Atlanta Falcons vs. Pittsburgh Steelers Game Highlights | NFL 2026 Season Week 1 — https://www.youtube.com/watch?v=TQcletbGnAk  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:15|ATL|N.Folk; K.Wetjen (PIT returner)|Opening kickoff returned by Wetjen to PIT 38.|27|kickoff return|unknown|unknown|D.Hellams (DB tackler)|verified vs DB|
|00:29|PIT|Aaron Rodgers; DK Metcalf|Third-and-six deep attempt for Metcalf is incomplete; Rodgers wants a flag.|None|deep shot|unknown|unknown|A.J. Terrell (coverage; not beaten on the result)|unverified (no DB match; caption-only)|
|00:38|ATL|Cooper Rush|Highsmith sacks Rush; offensive holding is announced. Penalty disposition is not provided.|None|unknown|unknown|unknown|Alex Highsmith (sacker)|unverified (no DB match; caption-only)|
|00:54|PIT|Pat Freiermuth|Reception gains ten and Pittsburgh's first first down.|10|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:04|PIT|Aaron Rodgers; Michael Pittman|Rodgers steps up and completes to Pittman for 21.|21|short left pass|unknown|unknown|K.Daniels; A.J. Terrell (DB tacklers)|verified vs DB|
|01:21|PIT|Aaron Rodgers|Third-and-nine snap against a four-man rush; captions omit the play's outcome.|None|unknown|unknown|four-man rush; coverage unknown|unknown|unverified (no DB match; caption-only)|
|01:30|PIT|Chris Boswell|Makes a 43-yard field goal for a 3-0 lead.|43|field goal|unknown|unknown|unknown|verified vs DB|
|01:44|ATL|Cooper Rush; Bijan Robinson|Dump-off secured one-handed by Robinson gains seven.|7|dump-off pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:55|ATL|Cooper Rush; Bijan Robinson|First-down pass to Robinson gains six.|6|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:06|ATL|Cooper Rush; Kyle Pitts|Second-and-19 downfield attempt to Pitts is broken up by Ramsey.|None|deep shot|unknown|unknown|Jalen Ramsey (pass breakup)|unverified (no DB match; caption-only)|
|02:17|ATL|Cooper Rush; Jahan Dotson|Third-and-long sideline attempt to Dotson is incomplete; Atlanta punts afterward.|None|sideline pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:24|PIT|Aaron Rodgers; DK Metcalf|Play-action completion to Metcalf working against Hughes.|None|play-action|under center|unknown|Mike Hughes|unverified (no DB match; caption-only)|
|02:42|PIT|Jaylen Warren; Divine Deablo (ATL recovery)|Warren fumbles a no-gain reception; Cameron Thomas forces it and Deablo recovers at PIT 25.|0|short right pass|unknown|unknown|Mike Hughes; Cameron Thomas (DB tacklers; Thomas forces fumble)|verified vs DB|
|02:47|ATL|Cooper Rush; Bijan Robinson|Third-and-eight quick pass to Robinson becomes a 23-yard touchdown.|23|quick short right pass|unknown|defense shows blitz, then backs off; coverage unknown|unknown|verified vs DB|
|03:09|PIT|Aaron Rodgers; Roman Wilson|Deep attempt to Wilson draws a 37-yard defensive pass interference penalty on Terrell; no play.|37|deep right pass|unknown|all 11 defenders within five yards of the line; coverage unknown|A.J. Terrell (penalized)|verified vs DB|
|03:20|PIT|Aaron Rodgers; DK Metcalf|Hughes jars the pass to Metcalf loose for an incompletion.|None|unknown|unknown|unknown|Mike Hughes (pass breakup)|unverified (no DB match; caption-only)|
|03:37|PIT|Aaron Rodgers; DK Metcalf|Rodgers beats a secondary blitz with a completion to Metcalf, who loses the ball. Captions do not establish the recovery.|None|unknown|unknown|secondary blitz; coverage unknown|unknown|unverified (no DB match; caption-only)|
|03:44|PIT|Aaron Rodgers; Roman Wilson|Third-and-five end-zone attempt is incomplete; commentary describes a miscommunication with Wilson.|None|end-zone pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:04|PIT|Chris Boswell|Makes a 28-yard field goal to cut Atlanta's lead to 7-6.|28|field goal|unknown|unknown|unknown|verified vs DB|
|04:22|ATL|Cooper Rush; Jaquan Brisker (PIT interception)|Rush steps up and throws high; Brisker intercepts the pass intended for Dotson and returns it ten yards.|10|deep middle pass|unknown|unknown|Jaquan Brisker (interceptor)|verified vs DB|
|04:37|PIT|Aaron Rodgers; Jaylen Warren|Trick play returns the ball to Rodgers; with Metcalf covered, he checks down to Warren for a first down.|19|trick play; checkdown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:55|PIT|Aaron Rodgers; Pat Freiermuth|On third-and-three, Rodgers scrambles and finds Freiermuth in the back of the end zone for a six-yard touchdown.|6|scramble pass; short middle|unknown|unknown|unknown|verified vs DB|
|05:12|ATL|Robinson (first name unspecified)|Robinson slips away from Queen and gains a first down; captions do not specify whether this is a run or reception.|None|unknown|unknown|unknown|Queen|unverified (no DB match; caption-only)|
|05:21|ATL|Cooper Rush; Robinson (first name unspecified)|Underneath completion gains ten before Brisker's hit.|10|underneath pass|empty; multiple tight ends, exact personnel unknown|unknown|Jaquan Brisker (tackler)|unverified (no DB match; caption-only)|
|05:35|ATL|Robinson (first name unspecified)|Handoff loses six as corner Jamel Dean comes untouched and knocks the ball free; possession afterward is unspecified.|-6|handoff; direction unknown|trips; Pitts aligned inside as a pseudo wide receiver|unknown|Jamel Dean (backfield stop)|unverified (no DB match; caption-only)|
|05:46|PIT|Aaron Rodgers|Rodgers is tackled from behind by Cameron Thomas; offensive facemask on number 60 is announced.|None|unknown|empty|unknown|Cameron Thomas (tackler)|unverified (no DB match; caption-only)|
|06:11|PIT|Aaron Rodgers; DK Metcalf|On third-and-20 from his own end zone, Rodgers escapes and throws toward Metcalf with Terrell defending. A flag follows; ruling is omitted.|None|scramble pass|unknown|unknown|A.J. Terrell (coverage)|unverified (no DB match; caption-only)|
|06:26|ATL|Cooper Rush; Drake London|London's first target produces an eight-yard sideline reception.|8|sideline pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:41|ATL|Cooper Rush; Robinson (first name unspecified)|Third-and-long dump-off reaches the 36 to set up a field goal attempt.|None|dump-off pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:56|ATL|Nick Folk|Misses a 54-yard field goal wide right.|54|field goal|unknown|unknown|unknown|verified vs DB|
|07:09|PIT|Aaron Rodgers; Roman Wilson|Third-and-15 completion to Wilson gains 20.|20|deep middle pass|unknown|unknown|Divine Deablo (DB tackler)|verified vs DB|
|07:15|PIT|Aaron Rodgers; Roman Wilson|Third-and-13 deep attempt briefly reaches Wilson's hands before Hughes jars it out.|None|deep shot|unknown|unknown|Mike Hughes (pass breakup)|unverified (no DB match; caption-only)|
|07:30|PIT|Recipient captioned as 'Johnson John'|From an apparent 62-yard field goal setup, Pittsburgh flips the ball to a recipient who is immediately hit. Identity and official outcome are unclear.|None|apparent field goal fake or aborted attempt; exact design unknown|apparent field goal setup|unknown|unknown|unverified (no DB match; caption-only)|
|07:47|ATL|Cooper Rush; Robinson (first name unspecified)|Underneath pass toward Robinson ends out of bounds; captions do not reliably establish completion.|None|underneath pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:07|PIT|Chris Boswell; Brian Robinson (ATL returner)|Second-half kickoff returned by Brian Robinson to ATL 43.|40|kickoff return|unknown|unknown|R.Jenkins (DB tackler)|verified vs DB|
|08:19|ATL|Bijan Robinson|Robinson carries on the ground early in the second half; gain is unspecified.|None|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:28|ATL|Bijan Robinson|Second-and-five run appears to gain a first down, but a flag is thrown; commentary suggests an infraction in the back without a final ruling.|None|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:34|ATL|Cooper Rush|Third-and-nine pass is batted at the line by Heyward.|None|unknown|unknown|unknown|Cameron Heyward (batted pass)|unverified (no DB match; caption-only)|
|08:46|ATL|Nick Folk|Misses a 45-yard field goal wide right.|45|field goal|unknown|unknown|unknown|verified vs DB|
|08:56|PIT|Aaron Rodgers; DK Metcalf|Third-and-six deep shot is incomplete despite Metcalf getting a step on Terrell.|None|deep shot|unknown|unknown|A.J. Terrell|unverified (no DB match; caption-only)|
|09:10|ATL|Cooper Rush; Drake London|Play-action sideline completion gains 21; Samuel adds a 15-yard unnecessary roughness penalty.|21|play-action; deep left pass|unknown|unknown|A.Samuel (DB tackler; penalized)|verified vs DB|
|09:27|ATL|Cooper Rush; Drake London|Rush throws behind a wide-open London for an incompletion that brings up fourth down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:32|PIT|Aaron Rodgers; Michael Pittman|Play-action completion to Pittman gains 28 to PIT 48; captions mangle Pittman's name.|28|play-action; deep left pass|unknown|unknown|C.Henderson (DB tackler); S.Ebukam (DB quarterback hit)|verified vs DB|
|09:45|PIT|Aaron Rodgers|Rodgers throws downfield into coverage; incomplete. Intended receiver is unspecified.|None|deep shot|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:54|PIT|Aaron Rodgers; DK Metcalf|Fourth-and-three attempt from the 45 reaches Metcalf out of bounds, turning possession over on downs.|None|unknown|unknown|one-on-one matchup on Metcalf; overall coverage unknown|Henderson (coverage)|unverified (no DB match; caption-only)|
|10:06|ATL|Cooper Rush; Bijan Robinson; Jahan Dotson|Boot action into a screen back to Robinson gains 24 before Ramsey forces a fumble; Dotson recovers at PIT 28. DB records 27 total yards including the recovery advance.|27|bootleg; screen back to the left|unknown|unknown|Jalen Ramsey (DB tackler; forces fumble)|verified vs DB|
|10:22|ATL|Cooper Rush|Watt sacks Rush from behind on second-and-long.|None|unknown|unknown|unknown|T.J. Watt (sacker)|unverified (no DB match; caption-only)|
|10:30|ATL|Nick Folk|Makes a 51-yard field goal to cut the deficit to 13-10; captions call it 50.|51|field goal|unknown|unknown|unknown|verified vs DB|
|10:44|PIT|Aaron Rodgers; DK Metcalf|Metcalf drops a pass over the middle.|None|middle pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:56|ATL|Bijan Robinson|Robinson gains 20 on the first play of the drive.|20|right-end run|unknown|unknown|Jaquan Brisker; C.Holcomb (DB tacklers)|verified vs DB|
|11:02|ATL|Cooper Rush; T.J. Watt (PIT interception return)|Watt intercepts a short right pass intended for Bijan Robinson and returns it 35 yards for a Pittsburgh touchdown.|35|short right pass|unknown|unknown|T.J. Watt (interceptor)|verified vs DB|
|11:28|ATL|Brian Robinson|Brian Robinson escapes a backfield tackle and turns a potential loss into a gain of 13.|13|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:43|ATL|Cooper Rush; Jahan Dotson|After a fake to Robinson, Dotson's first catch as a Falcon is announced as a 20-yard gain. No matching line appears in the supplied DB subset.|20|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:51|ATL|Bijan Robinson|Robinson runs left, cuts back and is hit by Heyward; gain is unspecified.|None|left-side run; cutback|unknown|unknown|Cameron Heyward (tackler)|unverified (no DB match; caption-only)|
|12:01|ATL|Nick Folk|Makes a 43-yard field goal to bring Atlanta within 20-13.|43|field goal|unknown|unknown|unknown|verified vs DB|
|12:14|PIT|Jaylen Warren|Warren makes a stop or cut on a play beginning at the 40; captions cut off before the result.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:31|PIT|Jaylen Warren|Warren fights ahead to the 35 for a 17-yard rushing first down.|17|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:40|PIT|Aaron Rodgers|Za'Darius Smith sacks Rodgers on third-and-five.|None|unknown|unknown|unknown|Za'Darius Smith (sacker)|unverified (no DB match; caption-only)|
|12:52|ATL|Bijan Robinson|Robinson finds a seam and gains 14 into Pittsburgh territory on the drive's first play.|14|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:04|ATL|Cooper Rush|Highsmith sacks Rush on a called pass.|None|unknown|unknown|unknown|Alex Highsmith (sacker)|unverified (no DB match; caption-only)|
|13:19|PIT|DK Metcalf|Metcalf goes up for a reception against Terrell; yardage is unspecified.|None|unknown|unknown|unknown|A.J. Terrell|unverified (no DB match; caption-only)|
|13:27|PIT|Aaron Rodgers; Michael Pittman|Pittman catches the pass and stays in bounds, finishing short of a first down.|None|unknown|unknown|unknown|Sydney Brown (captioned as making the stop)|unverified (no DB match; caption-only)|
|13:38|PIT|Aaron Rodgers; Washington|Third-and-two completion to Washington gains 14; he throws a defender to the ground.|14|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:53|PIT|Jaylen Warren|On second-and-six with Atlanta out of timeouts, Warren takes a flip and goes straight ahead for a first down.|None|flip to Warren; straight-ahead advance|unknown|unknown|unknown|unverified (no DB match; caption-only)|

Offense (model synthesis from this game's plays): Bijan Robinson supplied repeated receiving gains, including the 23-yard touchdown and the screen that gained 24 before a fumble and Atlanta recovery. / The second-half ground game produced Bijan Robinson gains of 20 and 14; Brian Robinson also escaped a backfield tackle for 13. / Play-action produced London's 21-yard reception and a caption-reported 20-yard Dotson reception.

Defense weaknesses: Pittman gained 21 and 28 through the air, and Roman Wilson converted third-and-15 with a 20-yard catch. / Terrell committed a 37-yard pass interference penalty against Wilson and was beaten for a step on an incomplete deep attempt to Metcalf. / A secondary blitz was beaten by a completion to Metcalf. / Late in the game, Warren gained 17 on the ground, Washington gained 14 on third-and-two, and Warren gained another first down with Atlanta out of timeouts.

Limitations: Captions only; no frames were viewed and no commands were run. Entries include identifiable snaps with incomplete outcomes. NO DB MATCH means no clear match in the supplied selective DB list, not that the play did not occur. DB-only plays without an identifiable caption were omitted, including several kickoffs and Boswell's fourth-quarter missed field goal. db_match contains the supplied quarter and clock identifier. For interceptions, yards is return yardage; for kicks it is kick distance or explicitly described return yardage; the DPI entry uses penalty yards. The Robinson screen entry uses the DB's 27 total yards, with the 24-yard reception distinguished in its description. Named tacklers, pass defenders and sackers in defender_beaten are identified by role and do not necessarily represent defenders actually beaten. Exact personnel groups, coverage shells, routes, blocking assignments and most run gaps cannot be established. Shotgun listed only in DB text was not used to infer personnel_formation, per the requirement for explicit commentary. Some Robinson references lack a first name, and the apparent field goal trick play has an unintelligible recipient name. The caption-reported 20-yard Dotson catch has no matching supplied DB line. Extra points were not separately identifiable in the captions.


## Week 2: CAR 34 - ATL 3 (game 401872933)
Video: Carolina Panthers vs. Atlanta Falcons Game Highlights | NFL Week 2 — https://www.youtube.com/watch?v=6zdUT_bY1Gg  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:08|unknown|unknown|Opening kick results in a touchback; the captions do not identify the kicking team or returner.|None|kickoff|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:16|ATL|Cooper Rush|After a fake to Robinson, Rush scrambles and fumbles. Carolina recovers; review upholds the ruling. DB identifies Z. Wheatley as forcing the fumble and Nick Scott as recovering.|9|play-action; scramble right end|unknown|unknown|Z. Wheatley (DB tackler and forced fumble; not beaten)|verified vs DB|
|00:32|CAR|Bryce Young|Completes a dump-off inside the 30 to the 28; receiver is not explicitly identified.|None|dump-off|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:49|CAR|Tetairoa McMillan|Catches Young's deep-right pass for 26 yards to the Atlanta 5. Commentary says he had plenty of room. DB also records roughing the passer.|26|deep pass right|unknown|unknown|A.J. Terrell (DB tackler)|verified vs DB|
|00:55|CAR|Bryce Young|On third-and-goal, tries to create a play himself before throwing incomplete toward Jalen Coker.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:07|CAR|Chuba Hubbard|Catches a wide-open 3-yard touchdown pass from Young.|3|short pass left|unknown|unknown|unknown|verified vs DB|
|01:14|ATL|Cooper Rush|Play fake to Robinson followed by commentary mentioning Drake London; the pass result is missing.|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:30|ATL|Cooper Rush|Quick-drop pass is tipped and intercepted. DB identifies Bobby Okereke as the interceptor, Devin Lloyd with the deflection, and Bijan Robinson as the intended receiver; return gains 3 yards.|3|quick drop; short pass middle|unknown|unknown|unknown|verified vs DB|
|01:41|CAR|Bryce Young|On third-and-15, pressure hits Young and causes the ball to flail away; final ruling is not stated.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:58|ATL|Kyle Pitts|Rush targets Pitts; Jaycee Horn slaps the ball away.|0|unknown|unknown|unknown|Jaycee Horn (pass breakup; not beaten)|unverified (no DB match; caption-only)|
|02:13|ATL|Jalen Coker (CAR returner)|Returns Atlanta's punt down the sideline with a flag down. DB records a 36-yard return and an Atlanta illegal-formation penalty.|36|punt return|unknown|unknown|J. Bailey; C. Woerner (DB tacklers)|verified vs DB|
|02:32|CAR|Xavier Legette|Commentary identifies Legette during a preceding play fragment; action and result are absent.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:34|CAR|Bryce Young|Under edge pressure, throws incomplete to Legette in the corner from the Atlanta 19. Commentary credits Henderson's coverage.|0|pass to corner|unknown|unknown|Henderson (credited with good coverage; not beaten)|unverified (no DB match; caption-only)|
|02:47|CAR|Ryan Fitzgerald|Attempts a 37-yard field goal; DB confirms it is good.|37|field goal|unknown|unknown|unknown|verified vs DB|
|02:57|ATL|unknown|A slant is called from shotgun; receiver and result are missing. Captions call the backfield player Brian Robinson, but the identity cannot be resolved from this fragment.|None|slant|shotgun|unknown|unknown|unverified (no DB match; caption-only)|
|03:07|ATL|Robinson (captioned as Brian; identity uncertain)|Run gets close to another first down; surrounding commentary calls it Atlanta's longest play.|None|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:26|ATL|unknown|Atlanta goes for a conversion with a reverse. Carolina reads it and stops it; commentary credits the linebackers and names Devin Lloyd.|None|reverse|unknown|unknown|Devin Lloyd (credited with stop; not beaten)|unverified (no DB match; caption-only)|
|03:40|CAR|Bryce Young|Quarterback is thrown down for an apparent sack; commentary names Dexter among the defenders. Carolina possession is inferred from the surrounding sequence.|None|unknown|unknown|unknown|Dexter (credited on sack; not beaten)|unverified (no DB match; caption-only)|
|03:51|ATL|Jahan Dotson|Makes a catch; distance and spot are omitted.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:12|ATL|unknown|Commentary references another big stop by Devin Lloyd; the offensive action and yardage are missing.|None|unknown|unknown|unknown|Devin Lloyd (credited with stop; not beaten)|unverified (no DB match; caption-only)|
|04:18|CAR|Tetairoa McMillan|Catches Young's third-down pass beyond the 35 to the 37 for a first down.|None|unknown|shotgun|unknown|unknown|unverified (no DB match; caption-only)|
|04:31|CAR|Tetairoa McMillan|Catches a 27-yard pass from Young to the Atlanta 36.|27|deep pass left|unknown|unknown|X. Watts (DB tackler)|verified vs DB|
|04:45|CAR|Jalen Coker|Caption fragment places the ball at the Atlanta 11. In the supplied sequence, this matches Coker's 25-yard reception; captions omit his name and the catch call.|25|deep pass right|unknown|unknown|unknown|verified vs DB|
|04:53|CAR|Bryce Young|Makes a spin move, rolls left and throws incomplete toward McMillan.|0|rollout left|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:05|CAR|Ryan Fitzgerald|Makes a 25-yard field goal to finish the drive.|25|field goal|unknown|unknown|unknown|verified vs DB|
|05:18|ATL|Cooper Rush|Under pressure on third-and-2, tries to make a play and reaches the sticks. Captions do not establish whether this was a scramble or a pass.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:33|ATL|Kyle Pitts|Catches a pass from Rush. The isolated word 'screen' does not clearly describe this play.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:45|ATL|Bijan Robinson|Runs through the left side on first-and-10.|None|run left|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:57|ATL|Drake London|Catches a crossing route on third down, struggles to keep his balance and falls forward to the 42.|None|crossing route|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:18|ATL|Bijan Robinson|Runs for a first down to the 29.|None|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:27|ATL|Cooper Rush|On third-and-4 just outside the 20, commentary calls an interception. No supplied DB turnover matches this point in the sequence; the subsequent score reference is 13-3.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:38|ATL|Nick Folk|The kicker-age and 13-3 score fragment aligns with Atlanta's 41-yard field goal in the DB; the actual kick call is absent.|41|field goal|unknown|unknown|unknown|verified vs DB|
|06:48|CAR|Darren Waller|Catches a seam pass against an inside blitz from a five-wide alignment. A flag is down; enforcement and final play status are not stated.|None|seam pass|five wides|inside blitz; coverage unknown|unknown|unverified (no DB match; caption-only)|
|07:01|CAR|Bryce Young|Jonathon Brooks stays in to block, but Young is sacked.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:14|CAR|Xavier Legette|Wide open for a 55-yard reception to the Atlanta 10. Mike Hughes makes the touchdown-saving tackle.|55|deep pass middle|unknown|unknown|Mike Hughes (commentary and DB tackler)|verified vs DB|
|07:30|CAR|Darren Waller|Catches Young's 7-yard touchdown throw to the corner on third-and-goal. Commentary praises the coverage, throw and route.|7|short pass right; pass to corner|unknown|unknown|unknown|verified vs DB|
|07:54|ATL|John Metchie (CAR returner)|Returns the second-half kickoff to the Carolina 27.|27|kickoff return|unknown|unknown|S. Brown (DB tackler)|verified vs DB|
|07:59|CAR|Jalen Coker|Catches a third-and-12 pass initially described as a yard short. Subsequent commentary says the ruling is reversed to a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:15|CAR|Chuba Hubbard|Brief Hubbard play reference follows the first-down reversal; action and result are missing.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:25|CAR|Tetairoa McMillan|Makes a catch against a blitz for 28 yards to the Atlanta 24. Commentary praises both catch and throw.|28|deep pass left|unknown|blitz; coverage unknown|C. Henderson (DB tackler)|verified vs DB|
|08:35|CAR|unknown|Ballcarrier has open grass ahead and is marked at the 18. Captions do not identify the player or distinguish a run from a reception.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:53|CAR|Darren Waller|Catches a 12-yard touchdown pass, his second touchdown of the day.|12|short pass right|unknown|unknown|unknown|verified vs DB|
|10:03|CAR|Bryce Young|With Brooks beside him in shotgun, Young throws incomplete under pressure. Dexter gets a hand in.|0|unknown|shotgun; Brooks beside quarterback|unknown|Dexter (disrupts pass; not beaten)|unverified (no DB match; caption-only)|
|10:19|ATL|J. Strand|Pass intended for Dotson is tipped and intercepted by Devin Lloyd, who returns it 16 yards for a Carolina touchdown. DB credits Jaycee Horn with the deflection.|16|short pass right|unknown|unknown|unknown|verified vs DB|
|10:36|ATL|Robinson (captioned as Brian; identity uncertain)|Catches Strand's dump-off, stays on his feet and reaches midfield.|None|dump-off|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:52|ATL|J. Strand|Commentary describes a sack by an outside linebacker coming off the edge; defender's name is missing.|None|unknown|unknown|edge pressure; coverage unknown|unknown|unverified (no DB match; caption-only)|
|10:56|ATL|J. Strand|On third-and-12 against pressure, completes a crossing pass. Ransom is immediately on the receiver.|None|crossing route|unknown|pressure; coverage unknown|Ransom (commentary defender at catch)|unverified (no DB match; caption-only)|
|11:11|CAR|Chuba Hubbard|Lone-setback play reaches the 15; the captions do not explicitly state whether Hubbard runs or receives.|None|unknown|lone setback|unknown|unknown|unverified (no DB match; caption-only)|
|11:20|CAR|unknown|Commentators praise a nicely set-up play and note a player is slow to get up. Action and player identities are absent; Carolina possession is inferred from sequence.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:33|ATL|Austin Hooper|Catches Strand's dump-off for a first down.|None|dump-off|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:46|ATL|J. Strand|Scrambles for a first down inside the 40.|None|scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:51|ATL|Robinson (first name uncertain)|Reaches the 26; announcer corrects an initial call of the 16. Play type is not stated.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:04|ATL|J. Strand|Steps up against edge pressure and targets Hooper. Will Lee makes the defensive play; context indicates an incompletion.|0|unknown|unknown|edge pressure; coverage unknown|Will Lee (credited with defensive play; not beaten)|unverified (no DB match; caption-only)|
|12:14|ATL|Nick Folk|Misses a long field goal. Commentary calls it 54 yards; authoritative DB records 53 yards, wide right.|53|field goal|unknown|unknown|unknown|verified vs DB|
|12:33|ATL|unknown|Commentary says a player will touch the ball while discussing rest for Bijan Robinson; action and outcome are missing.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:58|ATL|Robinson (first name uncertain)|Catches Strand's underneath checkdown against edge pressure at the 46.|None|checkdown|unknown|edge pressure; coverage unknown|unknown|unverified (no DB match; caption-only)|
|13:27|ATL|J. Strand|Carolina recovers a fumble. DB identifies a 6-yard sack of Strand followed by A. Hall's recovery at the Atlanta 46.|-6|unknown|unknown|unknown|unknown|verified vs DB|

Offense (model synthesis from this game's plays): Bijan Robinson produced a left-side run and a separate first-down run to the 29. / London's crossing route and underneath completions to Pitts, Robinson and Hooper supplied gains. / Strand added a first down with his legs.

Defense weaknesses: Allowed McMillan's three matched receptions of at least 26 yards and Legette's 55-yard gain. / Commentary explicitly described Hubbard as far too open on his touchdown and Legette as wide open on the long reception. / Allowed Waller two touchdown receptions, including a third-and-goal score before halftime. / A called blitz did not prevent McMillan's 28-yard catch on Carolina's third-quarter touchdown drive.

Limitations: Captions only; no routes, blocking, leverage, personnel counts or coverage shells were inferred visually. The early prediction of frequent 12/13 personnel was not assigned to a specific snap. Shotgun and other formations were entered only when commentary explicitly stated them, even when DB text supplied shotgun. Named tacklers do not establish who was responsible for coverage or beaten; their roles are labeled. Yards are gains for offensive plays, return distances for returns, and kick distances for field goals; null means unavailable. Teams on return plays identify the kicking/offensive team as requested. Some fragments lack enough information to establish a complete play, and two possession assignments are explicitly identified as sequence-based inferences. The apparent interception at 06:31 conflicts with the supplied DB sequence and remains unmatched. The 09:03–09:44 Jets/Williams segment appears to be unrelated game commentary and was excluded. No caption passage reliably identifies the DB's Q3 7:13 Lloyd interception and 53-yard return, the negated Q2 5:48 London reception, or several listed kickoff returns, so those were not added as observed highlights. Auto-caption uses of Brian/Bijan Robinson were left unresolved where no clear DB match exists. Score flags include defensive return touchdowns.


## Week 3: ATL 35 - GB 14 (game 401872948)
Video: Atlanta Falcons vs Green Bay Packers Game Highlights | 2026 NFL Season Week 3 — https://www.youtube.com/watch?v=sbXZBAUOkDw  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:30|ATL|B.Robinson|Bijan Robinson rush for 16 yards|16|unknown|unknown|unknown|Z.Franklin|unverified (no DB match; caption-only)|
|01:01|ATL|M.Penix|M.Penix pass intercepted by X.McKinney|5|unknown|unknown|unknown|unknown|verified vs DB|
|01:23|GB|T.Kraft|J.Love pass to T.Kraft|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:13|GB|M.Golden|J.Love deep pass to M.Golden for 45 yards|45|deep shot|unknown|unknown|M.Hughes|verified vs DB|
|02:34|GB|J.Jacobs|J.Jacobs rush|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:59|GB|T.Kraft|J.Love pass to T.Kraft for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:11|GB|C.Watson|J.Love pass to C.Watson for touchdown|4|unknown|unknown|unknown|M.Hughes|verified vs DB|
|03:36|ATL|B.Robinson|B.Robinson rush for 9 yards|9|unknown|unknown|unknown|J.Bullard|unverified (no DB match; caption-only)|
|04:24|ATL|B.Robinson|B.Robinson rush for 55 yards|55|run gap/direction|unknown|unknown|unknown|verified vs DB|
|05:01|ATL|B.Robinson|B.Robinson rush for 3 yard touchdown|3|run gap/direction|unknown|unknown|unknown|verified vs DB|
|05:58|ATL|B.Robinson|B.Robinson rush for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:58|ATL|B.Robinson|B.Robinson rush for big gain|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:07|ATL|B.Robinson|B.Robinson rush for loss of a couple yards|-2|unknown|unknown|unknown|E.Cooper|unverified (no DB match; caption-only)|
|07:18|ATL|L.Zacchaeus|M.Penix pass to L.Zacchaeus|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:27|ATL|N.Folk|N.Folk 44 yard field goal|44|unknown|unknown|unknown|unknown|verified vs DB|
|07:41|GB|M.Golden|Pass interference on M.Hughes vs M.Golden, 34 yards|34|unknown|unknown|unknown|M.Hughes|verified vs DB|
|08:11|ATL|D.London|M.Penix pass to D.London for 20 yards|20|unknown|unknown|unknown|X.McKinney|verified vs DB|
|08:30|ATL|A.Hooper|M.Penix pass to A.Hooper for 5 yard touchdown|5|unknown|unknown|unknown|unknown|verified vs DB|
|09:04|GB|M.Golden|J.Love pass to M.Golden for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:13|GB|C.Watson|J.Love pass to C.Watson for 22 yards|22|deep shot|unknown|unknown|unknown|verified vs DB|
|09:27|GB|C.Watson|J.Love pass to C.Watson short of first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:46|ATL|B.Robinson|B.Robinson rush for 7 yards|7|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:00|ATL|B.Robinson|B.Robinson rush for 31 yards|31|run gap/direction|unknown|unknown|J.Bullard|verified vs DB|
|10:46|ATL|B.Robinson|B.Robinson rush for 7 yard touchdown|7|run gap/direction|unknown|unknown|unknown|verified vs DB|
|12:09|ATL|D.London|M.Penix deep pass to D.London for 68 yards|68|deep shot|unknown|unknown|B.Cisse|verified vs DB|
|12:34|ATL|N.Folk|N.Folk 31 yard field goal|31|unknown|unknown|unknown|unknown|verified vs DB|
|12:46|GB|C.Watson|J.Love pass to C.Watson for 34 yards|34|deep shot|unknown|unknown|C.Henderson|verified vs DB|
|13:14|GB|M.Golden|J.Love pass to M.Golden for 15 yard touchdown|15|unknown|unknown|unknown|unknown|verified vs DB|
|13:24|ATL|D.London|M.Penix pass to D.London for 40 yards|40|deep shot|unknown|unknown|E.Williams|verified vs DB|
|13:46|ATL|B.Robinson|B.Robinson rush for 2 yard touchdown (2pt conversion succeeds)|2|run gap/direction|unknown|unknown|unknown|verified vs DB|
|14:18|GB|J.Smith|J.Love pass intercepted by X.Watts|17|unknown|unknown|unknown|unknown|verified vs DB|

Offense (model synthesis from this game's plays): Explosive run game with Bijan Robinson showing elite vision, balance, speed and cutback ability leading to multiple big gains over 20 yards and multiple rushing TDs / Effective play-action passing off successful runs allowing deep shots and big plays to Drake London who had multiple receptions over 20 yards / Red zone efficiency converting short yardage into scores including rushing TDs and a passing TD

Defense weaknesses: Vulnerable to deep passes and big plays allowing multiple receptions of 20+ yards to Packers receivers including Christian Watson and Matthew Golden / Communication breakdowns in secondary leading to blown coverages and TDs allowed / Defensive penalties including pass interference and roughing the passer giving opponent automatic first downs

Limitations: Could not determine specific personnel formations, coverage schemes, or exact run concepts/gaps beyond what was explicitly mentioned; many plays in captions lacked specific yardage or defender details and did not perfectly align with DB entries; some names were mangled in captions and corrected only for clear matches; several described plays had no direct DB match.


## Week 4: ATL 45 - NO 24 (game 401872979)
Video: Atlanta Falcons vs New Orleans Saints Game Highlights | 2026 NFL Season Week 4 — https://www.youtube.com/watch?v=8qB8fHEgpkg  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:18|ATL|D.London|Quick throw to London, one-on-one, makes a move, breaks a tackle and gets 12|12|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:28|ATL|B.Robinson|To Robinson and sets up a screen. That's Cooper, the tight end, and two nice chunk plays|None|screen|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:40|ATL|B.Robinson|Bijan Robinson! There are no flags and that is a touchdown!|59|left end|unknown|unknown|unknown|verified vs DB|
|01:17|NO|D.Vele|Shough throws. Able to complete. A short gain to DeVaughn Vele. A gain of two.|2|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:41|ATL|B.Robinson|Robinson cuts back and gets a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:51|ATL|D.London|They fake it to him and will throw to the sideline. A diving try by London, incomplete.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:07|NO|J.Johnson|Play-action from Shough. In trouble, lets it fly! And he has Johnson! Big play. Juwan Johnson for 23.|23|play-action|unknown|unknown|Z.Harrison|verified vs DB|
|02:42|NO|J.Johnson|Quick throw, Juwan Johnson needs blocks. And he won't get it.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:04|ATL|B.Robinson|Robinson tries the left side and doesn't get much.|None|left side|unknown|unknown|C.Wooden|unverified (no DB match; caption-only)|
|03:14|ATL|M.Penix|Third down and six. Penix, sacked! Tyree Wilson.|-1|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:27|NO|K.Miller|From the 20. Kendre Miller. The ball came out, but they're going to say he was down. A gain of just three.|3|left guard|unknown|unknown|unknown|verified vs DB|
|03:52|ATL|B.Robinson|Penix out to his left and a great play with Robinson the target.|None|unknown|unknown|unknown|C.Young|unverified (no DB match; caption-only)|
|04:25|ATL|B.Robinson|Robinson, touchdown, Atlanta! The second of the night.|4|left guard|unknown|unknown|unknown|verified vs DB|
|04:37|NO|C.Olave|Play-action from Shough. Floats it. Olave! A lot of room. Cuts back, inside the 10.|44|play-action|unknown|unknown|X.Watts|verified vs DB|
|04:52|NO|A.Kamara|The handoff is to Kamara! Touchdown, Saints.|3|up the middle|unknown|unknown|unknown|verified vs DB|
|05:06|ATL|D.London|Werner in motion. Penix keeps. Fires. Wide open, London. Spins his way down near the 12.|27|unknown|unknown|unknown|Q.Riley|verified vs DB|
|05:27|ATL|B.Robinson|Penix in trouble, setting up the screen. He got it to Brian Robinson who spins his way down inside the 5 with a gain of six.|6|screen|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:45|ATL|B.Robinson|Robinson again, strong run! Touchdown, Atlanta.|4|right guard|unknown|unknown|unknown|verified vs DB|
|06:01|NO|D.Vele|Well protected here, floated and incomplete with Vele the target and great coverage by Sydney Brown|0|unknown|unknown|unknown|S.Brown|unverified (no DB match; caption-only)|
|06:11|NO|C.Olave|Extra man on the rush, Shough. Olave. Never saw it.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:21|ATL|D.London|Penix over the middle, flag on the play, and Drake London is spinning down inside Saints territory.|37|deep middle|unknown|unknown|K.McKinstry|verified vs DB|
|06:48|ATL|B.Robinson|Bijan Robinson cuts back, makes one man miss. Breaking tackles and down to the|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:01|ATL|K.Pitts|Penix slings it. Catch and a first down inside the 15.|28|short left|unknown|unknown|J.Blackmon|verified vs DB|
|07:59|NO|J.Johnson|Shough fires and that is a strong throw. Juwan Johnson with a first down and a nice pickup on second down of 18 yards.|18|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:14|NO|C.Olave|Olave, first down. Working against Mike Hughes and no match for Olave on that route.|None|unknown|unknown|unknown|M.Hughes|unverified (no DB match; caption-only)|
|08:21|NO|T.Shough|Here's a sack. Big hit by Xavier Watts.|-1|unknown|unknown|unknown|X.Watts|unverified (no DB match; caption-only)|
|08:45|NO|C.Olave|What a catch by Olave. Lost his footing and somehow able to reach up while on the ground and haul it in for a first down, a gain of 11.|11|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:03|NO|C.Olave|Shough, sideline, caught.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:11|NO|C.Olave|Third and seven. What a catch by Olave! Brilliant. Perfect throw and Olave with the|23|deep left|unknown|unknown|B.Bowman|verified vs DB|
|09:20|NO|K.Miller|Long drive. Miller, spinning catch, and a strong tackle is made by Perkins.|None|unknown|unknown|unknown|H.Perkins|unverified (no DB match; caption-only)|
|09:55|ATL|J.Dotson|Penix floats it. He has Dotson with a catch but a flag is down, back inside the|23|short left|unknown|unknown|K.McKinstry|verified vs DB|
|10:08|ATL|B.Robinson|Handoff to Bijan Robinson with that burst he is able to get eight.|8|unknown|unknown|unknown|unknown|verified vs DB|
|10:21|ATL|B.Robinson|Robinson with the easy first down pickup.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:32|ATL|D.London|Quick snap, Penix. London for the first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:43|ATL|B.Robinson|Brian Robinson, touchdown. His second of the night.|8|right tackle|unknown|unknown|unknown|verified vs DB|
|10:57|NO|D.Vele|Fourth down and ten. They have to go for it. Shough hangs in and a completion. First down, DeVaughn Vele.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:07|NO|D.Vele|A diving catch by Vele. They put it down very close to first down yardage, just short.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:25|NO|A.Kamara|They're going to get the first down -- they're going to get the touchdown! Kamara, his second of the night.|5|up the middle|unknown|unknown|unknown|verified vs DB|
|11:33|ATL|K.Pitts|Penix keeps. Pitts, catch. There's nobody over there for New Orleans. Nice cutback. And it's a big catch and run|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:49|ATL|B.Robinson|Bijan Robinson breaking tackles and a couple short of a first|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:03|ATL|J.Dotson|Penix keeps. He's going to go for it all. He's got a man, Dotson, touchdown!|31|deep middle|unknown|unknown|unknown|verified vs DB|
|12:42|NO|T.Shough|Pressure on Shough and he is sacked! Sampson makes the play.|-1|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:02|ATL|B.Robinson|Another nice carry by Brian Robinson for the touchdown! How about three on the night for number 15.|11|left guard|unknown|unknown|unknown|verified vs DB|
|13:30|NO|C.Donaldson|Donaldson with the catch for a first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|

Offense (model synthesis from this game's plays): Explosive run game with Bijan Robinson and Brian Robinson breaking tackles and scoring multiple TDs / Effective use of play-action and screens to set up big passing plays to receivers like Drake London and J.Dotson / Ability to capitalize on defensive penalties and convert on third downs

Defense weaknesses: Vulnerable to big passing plays downfield to C.Olave and occasional chunk gains by Saints receivers / Occasional missed tackles in run defense allowing yards after contact

Limitations: Could not determine exact personnel formations, coverage schemes, or many specific defender names as they were rarely explicitly stated by commentators. Many plays in captions did not perfectly align with DB entries so used 'NO DB MATCH' where no clear timestamp/clock match. Auto-generated captions had name mangling (e.g. Brian/Bijan Robinson confusion, Werner possibly a mis-transcription) corrected only on clear matches to DB. Several described plays lacked yardage or concept specifics in commentary.


## Week 5: BAL 30 - ATL 23 (game 401872993)
Video: Baltimore Ravens vs Atlanta Falcons Game Highlights | 2026 NFL Season Week 5 — https://www.youtube.com/watch?v=fVlmow2jCDA  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:20|BAL|J.Hill|J.Hill left tackle for 21 yards|21|run gap/direction|unknown|unknown|M.Hughes|verified vs DB|
|01:20|BAL|unknown|Ravens drive 57 yards on 6 plays to first and goal|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:40|ATL|unknown|Falcons defense stands on first and goal|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:19|BAL|T.Huntley|Huntley pressured|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:34|BAL|M.Andrews|Andrews fumbles, recovered by J.Bates for 36 yard touchdown|36|unknown|unknown|unknown|S.Brown|verified vs DB|
|03:13|BAL|J.Hill|Hill to the outside|None|run gap/direction|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:38|ATL|Bi.Robinson|Bijan Robinson up the middle for 20 yards|20|run gap/direction|unknown|unknown|R.Smith|verified vs DB|
|04:58|BAL|unknown|Ravens begin from the 47|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:24|BAL|unknown|Third and ten, low snap|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:27|BAL|T.Loop|Tyler Loop 51 yard field goal|51|unknown|unknown|unknown|unknown|verified vs DB|
|06:12|ATL|D.London|Penix downfield to London for 25 yards|25|deep shot|unknown|unknown|M.Starks|verified vs DB|
|06:28|ATL|K.Pitts|Touchdown to Pitts for 5 yards|5|unknown|unknown|unknown|unknown|verified vs DB|
|07:25|BAL|T.Loop|Loop 51 yard field goal|51|unknown|unknown|unknown|unknown|verified vs DB|
|08:44|ATL|Bi.Robinson|Bijan Robinson left tackle for 38 yards|38|run gap/direction|unknown|unknown|M.Starks|verified vs DB|
|09:51|ATL|N.Folk|Folk 23 yard field goal|23|unknown|unknown|unknown|unknown|verified vs DB|
|09:51|BAL|R.Ali|R.Ali kickoff return for 21 yards|21|unknown|unknown|unknown|J.Woods|CONFLICT (yardage 21 vs DB)|
|10:01|BAL|J.Hill|Justice Hill up the middle for 47 yards|47|run gap/direction|unknown|unknown|Av.Terrell|verified vs DB|
|10:16|BAL|D.Henry|Huntley pass to Henry for 18 yard touchdown|18|unknown|unknown|unknown|unknown|verified vs DB|
|10:16|ATL|Br.Robinson|Br.Robinson kickoff return for 40 yards|40|unknown|unknown|unknown|M.Starks|CONFLICT (yardage 40 vs DB)|
|11:56|ATL|Z.Branch|Rookie Branch run for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:22|ATL|N.Folk|Folk 34 yard field goal|34|unknown|unknown|unknown|unknown|verified vs DB|
|12:31|BAL|L.Wester|L.Wester kickoff return for 30 yards|30|unknown|unknown|unknown|S.Brown|CONFLICT (yardage 30 vs DB)|
|12:57|ATL|Z.Branch|Branch 23 yard reception|23|unknown|unknown|unknown|M.Humphrey; R.Smith|verified vs DB|
|13:21|ATL|N.Folk|Folk 48 yard field goal|48|unknown|unknown|unknown|unknown|verified vs DB|
|13:21|BAL|L.Wester|L.Wester kickoff return for 24 yards|24|unknown|unknown|unknown|N.Muse|CONFLICT (yardage 24 vs DB)|
|13:32|BAL|Z.Flowers|Huntley pass to Flowers, DPI penalty on X.Watts for 29 yards|29|deep shot|unknown|unknown|X.Watts|verified vs DB|
|13:38|BAL|R.Bateman|Huntley pass to Bateman for 20 yards|20|unknown|unknown|unknown|X.Watts; H.Perkins|verified vs DB|
|13:43|BAL|D.Walker|Huntley pass to Walker for 7 yard touchdown|7|unknown|unknown|unknown|unknown|verified vs DB|
|14:40|ATL|unknown|Tua Tagovailoa enters at QB|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:30|ATL|T.Tagovailoa|Tagovailoa pass to London for 20 yards|20|unknown|unknown|unknown|M.Starks|verified vs DB|
|16:44|BAL|T.Huntley|Huntley 1 yard rushing touchdown|1|unknown|unknown|unknown|unknown|verified vs DB|
|17:07|ATL|T.Tagovailoa|Tagovailoa pass intercepted by K.Hamilton for 2 yards|2|unknown|unknown|unknown|unknown|verified vs DB|

Offense (model synthesis from this game's plays): Big plays from Bijan Robinson rushes (20, 38 yards) / Deep and intermediate passing success with Penix to London, Dotson, Pitts for TDs and long gains / Resilient scoring drives resulting in multiple FGs and a TD to lead in regulation

Defense weaknesses: Allowed Ravens explosive runs (47 yards by Hill) and multiple passing TDs / Defensive penalties including DPI leading to Ravens scores / Failed to stop Ravens in OT, allowing game-winning rushing TD and final interception

Limitations: Could not determine specific concepts like play-action, RPO, screens, personnel formations, or coverage schemes as they were not explicitly stated in the captions or DB text. Many plays in captions were vague or did not perfectly align with DB, leading to 'unknown' or 'NO DB MATCH'. Auto-generated captions mangled names and details extensively; corrections applied only for clear matches. Injury mentions and non-play commentary limited full play identification.


## Week 6: CHI 31 - ATL 23 (game 401872999)
Video: Chicago Bears vs Atlanta Falcons Game Highlights | 2026 NFL Season Week 6 — https://www.youtube.com/watch?v=H82sLvw_lcU  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:11|CHI|unknown|Receiver holds on through a big hit on a rollout completion.|None|play-action rollout|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:25|CHI|Johnson (first name uncertain)|Underneath completion followed by a lateral to Johnson for a first down.|None|hook and ladder|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:37|CHI|Johnson (first name uncertain)|Downhill run to around the 11.|None|downhill run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:50|CHI|C.Williams → C.Loveland|Williams escapes pressure and throws across his body to Loveland for a touchdown. Commentary credits extended-play secondary routes and Loveland's frame.|14|scramble extension; short right pass|unknown|unknown|unknown|verified vs DB|
|01:18|ATL|M.Penix|Play-fake screen is disrupted by Kentavius Street; exact result is unclear.|None|play-action screen|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:32|ATL|M.Penix|Escapes initial pressure but throws incomplete with Cam Lewis nearby.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:46|CHI|C.Williams → R.Odunze|Third-and-long completion over the middle for a first down.|23|deep middle pass|unknown|unknown|M.Hughes (DB tackler)|verified vs DB|
|02:05|CHI|C.Williams → L.Burden|Play-action completion to a wide-open receiver, pushed out near the 20; DB places the ball at the 18.|25|play-action; short right pass|unknown|unknown|S.Brown (DB tackler)|verified vs DB|
|02:17|CHI|C.Williams → D.Swift|Screen after multiple fakes; Swift breaks a tackle and reaches inside the 10.|None|screen with backfield fakes|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:34|CHI|D.Swift|Short rushing touchdown.|4|left guard run|unknown|unknown|unknown|verified vs DB|
|02:43|ATL|unknown|Motion and a designed touch are stopped with no blocking room; Noah Sewell blows up the play.|None|motion; designed outside touch|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:05|ATL|M.Penix → Zaccheaus|Incomplete pass near the first-down marker.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:13|CHI|C.Williams → unknown|Completion to another wide-open receiver.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:26|CHI|D.Swift|Run stopped immediately by a defender captioned as Kendal Daniels.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:37|CHI|C.Williams|First incompletion of the day against a blitz.|None|unknown|unknown|blitz|unknown|unverified (no DB match; caption-only)|
|03:41|ATL|Bijan Robinson|Run ends with Cam Lewis upending Robinson; commentary credits Lewis with preventing a touchdown.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:56|ATL|Bi.Robinson|Explosive run into the open field, stopped by Elijah Hicks.|23|right guard run|unknown|unknown|E.Hicks (DB tackler)|verified vs DB|
|04:10|ATL|M.Penix → unknown|Has time after a play fake but overthrows a wide-open deep target.|None|play-action deep shot|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:24|ATL|Bijan Robinson|Stopped by Kyler Gordon on third-and-four.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:34|ATL|M.Penix|Knocked down against a blitz; Chicago takes possession. Captions do not establish whether this was a sack or an incomplete pass.|None|unknown|unknown|blitz|unknown|unverified (no DB match; caption-only)|
|04:47|CHI|C.Williams → Roschon Johnson|Under pressure on first-and-long, Williams completes a pass toward the sideline to Johnson.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:07|CHI|unknown|Fragment describes Watts and teammates bringing down the ball carrier to force third down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:14|CHI|C.Williams|On third-and-seven, escapes interior pressure and throws incomplete toward the far side. Captioned pressure attribution is unreliable.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:28|CHI|C.Santos|Misses a 56-yard field goal wide left.|56|field goal|unknown|unknown|unknown|verified vs DB|
|05:44|ATL|M.Penix → D.London|London makes a move after the catch for a large gain; DB places him at the Chicago 15.|39|deep left pass|unknown|unknown|N.Sewell (DB tackler)|verified vs DB|
|05:53|ATL|M.Penix → J.Dotson|Corner fade touchdown against rookie Muhammad in an explicitly described one-on-one matchup.|13|fade|unknown|one-on-one matchup; overall scheme unknown|M.Muhammad|verified vs DB|
|06:20|CHI|C.Williams → D.Swift|Williams buys time on a play-action rollout and finds Swift for a called first down; a secondary flag is mentioned.|None|play-action rollout|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:31|CHI|C.Williams → C.Loveland|Third-and-17 completion over the middle; Falcons converge short of the needed distance, followed by a punt.|None|middle pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:46|CHI|Taylor; Josh Blackwell|Chicago punt is muffed after a fair-catch call; Blackwell recovers near the Atlanta 10. Later commentary identifies Branch as the earlier fumbler.|None|punt; muff recovery|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:11|CHI|C.Williams → C.Loveland|Fake to Swift opens Loveland, but the pass is behind him and apparently incomplete.|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:22|CHI|D.Swift|Third-and-goal rushing touchdown to the right.|2|right guard run|unknown|unknown|unknown|verified vs DB|
|07:47|ATL|M.Penix|Sacked by a rusher captioned as Hardy. An apparent loose ball and Chicago recovery are followed by replay commentary that Penix was down; do not count a confirmed turnover.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:17|ATL|Bijan Robinson|Run to around the 35 late in the half.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:26|CHI|C.Williams|Sacked for Atlanta's first sack of the day; captioned rusher name is incomplete.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:38|ATL|M.Penix → receiver captioned as Cooper|Checkdown completion underneath.|None|checkdown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:53|ATL|M.Penix|Cannot find a receiver and is sacked by a safety whose name is rendered inconsistently as Feinman/Thieneman.|None|unknown|unknown|safety blitz|unknown|unverified (no DB match; caption-only)|
|09:08|ATL|unknown|Contact on the corner results in a first down. Exact foul and participants cannot be established.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:23|ATL|M.Penix|With seven Bears showing at the line, pressure arrives and Kyler Gordon drops Penix.|None|unknown|unknown|blitz; seven defenders showing at line|unknown|unverified (no DB match; caption-only)|
|09:37|ATL|M.Penix|Under pressure, throws to the far side; Jalen Johnson tips the pass incomplete and Chicago takes over.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:52|CHI|C.Williams → receiver captioned as Burton|Completion out across the 34. No clear DB match supports correcting the receiver's name.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:01|CHI|C.Williams → Rome Odunze|Wide-open completion on third-and-one into Atlanta territory.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:14|CHI|receiver captioned as Luther Burton|Third-and-five swing pass toward the edge; commentary initially considers the receiver short, then the caption cuts off the final spot.|None|swing pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:24|CHI|C.Williams → C.Loveland|Loveland catches against a blitz, continues into the end zone, and a pass-interference flag follows. The apparent touchdown is not supported as a valid score by the DB.|None|option route|unknown|blitz|unknown|unverified (no DB match; caption-only)|
|10:52|ATL|unknown|Fragment describes an Atlanta player being hit inside the five during the ensuing special-teams sequence; exact play type and player are unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:09|ATL|M.Penix|Third-down sack and loose ball; Atlanta recovers. Commentary names Gordon and describes a speed rush against a blocker captioned as Warner.|None|unknown|unknown|unknown|Warner (captioned blocker name; uncertain)|unverified (no DB match; caption-only)|
|11:38|CHI|C.Williams → L.Burden|Wide-open completion held through a big hit. Commentary names Terrell on the hit; DB lists S.Brown as tackler.|22|deep right pass|unknown|unknown|Terrell (commentary hit); S.Brown (DB tackler)|verified vs DB|
|11:51|CHI|receiver captioned as Luther Burton|Quick outside completion with a blocker sought ahead; reaches first-and-goal.|None|quick outside pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:01|CHI|R.Johnson|Battles forward on the right side for a touchdown.|4|right guard run|unknown|unknown|unknown|verified vs DB|
|12:21|CHI|Z.Branch; Z.Scott; N.McCloud|Atlanta returner Branch fumbles; Scott forces it and McCloud recovers for Chicago. Captions call this a punt return, but the matching DB play is a kickoff. Team denotes the kicking team.|26|kickoff return; forced fumble|unknown|unknown|unknown|CONFLICT (yardage 26 vs DB)|
|12:43|CHI|C.Williams|Pressure reaches Williams; commentary indicates Dor lus gets him, but the caption truncates the outcome.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:54|CHI|C.Santos|Makes a 50-yard field goal for a 31-7 lead.|50|field goal|unknown|unknown|unknown|verified vs DB|
|13:08|ATL|M.Penix → Zaccheaus|Captions call a pressured throw an interception. No interception appears in the authoritative turnover list, so a valid turnover cannot be confirmed.|None|middle pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:19|ATL|M.Penix|Third-and-long pass is described as nearly intercepted; Chicago is expected to get possession.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:34|ATL|Branch|Catches a pass and takes a heavy hit. A hold and Chicago gaining possession are mentioned; final ruling is unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:49|CHI|C.Williams|Escapes initial pressure but is sacked again. Rusher identification is unreliable in the captions.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:03|CHI|D.Swift|Draw has little running room.|None|draw|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:18|ATL|M.Penix → J.Dotson|Completion into Chicago territory; commentary describes a clean-pocket throw to an outside one-on-one matchup.|33|short right pass|unknown|one-on-one outside matchup; overall scheme unknown|C.Phillips (DB tackler)|verified vs DB|
|14:34|ATL|M.Penix → K.Pitts|Pitts secures the ball around Hicks, breaks tackles and leaps over defenders to near the 15.|29|short right pass|unknown|unknown|Hicks (commentary); J.Blackwell (DB tackler)|verified vs DB|
|14:59|ATL|M.Penix → K.Pitts|Third-and-six touchdown under pressure. Caption wording suggests someone walks in; DB establishes a touchdown pass to Pitts.|10|short left pass|unknown|unknown|unknown|verified vs DB|
|15:14|ATL|M.Penix → Z.Branch|Rookie holds on for the successful two-point conversion, reducing the deficit to 16.|None|two-point conversion pass|unknown|unknown|unknown|verified vs DB|
|15:24|CHI|C.Williams → Thomas|Quick slant completion for a first down out to the 42 against a four-man rush.|None|slant|unknown|four-man rush; coverage unknown|unknown|unverified (no DB match; caption-only)|
|15:36|CHI|R.Johnson|Johnson fumbles on an inside run; Bates forces the fumble and Perkins recovers for Atlanta.|4|run up the middle|unknown|unknown|J.Bates (DB tackler and forced fumble)|verified vs DB|
|15:57|ATL|M.Penix → J.Dotson|Protected deep throw; Dotson breaks free and catches it near the Chicago 15.|41|deep left shot|unknown|unknown|D.Thieneman (DB tackler)|verified vs DB|
|16:12|ATL|M.Penix → Kyle Pitts|Pitts gains a first down against pressure; commentary identifies a quick five-yard option route.|None|option route|unknown|blitz described as everyone coming|unknown|unverified (no DB match; caption-only)|
|16:27|ATL|M.Penix → K.Pitts|Pitts scores, reaching the ball out; commentary names Thieneman in the matchup.|5|short right pass|unknown|unknown|Thieneman|verified vs DB|
|16:42|ATL|M.Penix → D.London|Successful two-point conversion makes it a one-score game.|None|two-point conversion pass|unknown|unknown|unknown|verified vs DB|
|17:00|CHI|C.Williams|Pass against a blitz is knocked away incomplete; a late flag is mentioned without a ruling.|None|unknown|unknown|blitz|unknown|unverified (no DB match; caption-only)|
|17:08|ATL|Bijan Robinson|Run to around the 32, described as a two-yard gain.|2|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|17:16|ATL|M.Penix|Gordon strip-sacks Penix on third-and-long; Bush recovers for Chicago.|-8|unknown|unknown|unknown|unknown|verified vs DB|
|17:43|CHI|Roschon Johnson|Clock-killing run with secure ball handling; Atlanta calls its second timeout.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|18:01|CHI|Roschon Johnson|Another late run as Chicago works to exhaust the clock.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|18:08|CHI|Roschon Johnson|Breaks toward the edge for a first down and slides to seal the game.|8|run toward the edge|unknown|unknown|unknown|unverified (no DB match; caption-only)|

Offense (model synthesis from this game's plays): Robinson generated an explosive 23-yard run through right guard. / London and Dotson produced gains of 39 and 41 yards; Dotson also won a corner fade against Muhammad. / Pitts generated a 29-yard catch-and-run, converted an option route against pressure and scored twice in the fourth quarter. / Late touchdown drives included successful two-point passes to Branch and London.

Defense weaknesses: Repeatedly allowed wide-open Chicago completions, including Burden's 25-yard play-action gain and Odunze's third-and-one conversion. / Could not contain Williams' extended plays on Loveland's touchdown and Swift's first-down catch. / Conceded three short rushing touchdowns through guard gaps. / Allowed Burden a 22-yard reception and Johnson the final eight-yard first-down run.

Limitations: Captions only; no frames were available. The supplied DB is a selected-play list, so NO DB MATCH does not establish that a play did not occur. Several names, play boundaries, penalties and outcomes are garbled. Unmatched names were left as captioned or unknown. No offensive personnel grouping or formation was explicitly stated by commentators; DB shotgun labels were therefore not used for personnel_formation. Broad coverage identities cannot be inferred from blitzes, rush counts or individual matchups. Named DB tacklers do not establish coverage responsibility or that they were beaten. Special-teams team fields identify the team initiating the kick. Return yards and field-goal distances are not offensive gains. Johnson's fumble entry reports a four-yard rush despite the DB event's zero-yard recovery classification; the final strip-sack reports the explicitly stated eight-yard loss. The apparent Loveland touchdown, apparent earlier Penix fumble and captioned interception lack authoritative confirmation as valid scores or turnovers. Some fragmentary sequences may overlap adjacent plays or replays. DB-only plays without identifiable caption coverage were not added.
