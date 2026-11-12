# CIN — Phase 8 film notes (Weeks 1–6, 2026)

Method: NFL YouTube channel full-game highlight videos were located by search and their auto-captions (broadcast commentary) downloaded via yt-dlp. Codex (codex-cli 0.163.0) extracted plays from the captions. **No video frames were viewed by any agent.** Each play was checked against the repo DB play-by-play: `verified vs DB` means the cited DB play exists and the yardage matches. Personnel, formation and coverage appear only when commentators stated them; everything else is `unknown`.


## Week 1: TB 27 - CIN 33 (game 401872925)
Video: Tampa Bay Buccaneers vs. Cincinnati Bengals Game Highlights | NFL 2026 Season Week 1 — https://www.youtube.com/watch?v=6Jc-OI39Qng  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:18|TB|K.Johnson|Returns the opening kickoff to the TB 28.|23|kickoff return|unknown|unknown|J.Battle|verified vs DB|
|00:28|TB|Bucky Irving|Takes a handoff for approximately 8.5 yards before Turner tackles him.|None|unknown|unknown|unknown|Turner|unverified (no DB match; caption-only)|
|00:39|TB|Baker Mayfield; receiver unidentified|Completes a 17-yard pass on third-and-one; Turner makes the tackle near the 45.|17|play-action|unknown|unknown|Turner|unverified (no DB match; caption-only)|
|00:49|TB|Bucky Irving|Slips while cutting, then gains nine yards to the Cincinnati 32 for a first down.|9|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:05|TB|Chris Godwin|Slips through two unnamed defenders for a first down at the 21.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:12|TB|Baker Mayfield|Buys time and throws the ball away.|0|throwaway|empty backfield|unknown|unknown|unverified (no DB match; caption-only)|
|01:21|TB|C.McLaughlin|Makes a 34-yard field goal.|34|field goal|unknown|unknown|unknown|verified vs DB|
|01:30|CIN|Joe Burrow; Ja'Marr Chase|Third-and-six pass goes off Chase's hands with McCollum covering, ending a three-and-out.|0|unknown|unknown|unknown|McCollum (in coverage; not beaten)|unverified (no DB match; caption-only)|
|01:47|TB|B.Mayfield; D.Knight|Mayfield loses a sack fumble forced by M.Murphy, with B.Carter sharing the sack. Knight returns the recovery 27 yards for a Cincinnati touchdown.|27|strip sack; fumble return|unknown|unknown|M.Murphy; B.Carter (sack/forced fumble)|verified vs DB|
|02:12|TB|Baker Mayfield|Goes down with a flag on the play; the caption does not establish the penalty or final result.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:13|TB|B.Irving|Catches a checkdown for seven yards, then loses a fumble forced by B.Cook and recovered by CIN-B.Mafe.|7|checkdown|unknown|unknown|B.Cook|verified vs DB|
|02:34|CIN|Joe Burrow; receiver unidentified|Fragment indicates a completion, but the receiver and result are missing.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:43|CIN|Joe Burrow; Ja'Marr Chase|Throws left toward Chase through contact; the catch result is unclear.|None|unknown|Iosivas in motion|unknown|unknown|unverified (no DB match; caption-only)|
|02:51|CIN|Joe Burrow|Escapes pressure and scrambles, diving after contact near the third-and-six line to gain.|None|scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:09|CIN|unidentified runner|Runs through a large hole up the middle to near the three-yard line.|None|run up the middle|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:20|CIN|J.Burrow; M.Gesicki|Burrow finds Gesicki for a two-yard touchdown pass to the left.|2|short left pass|unknown|unknown|unknown|verified vs DB|
|03:32|TB|Chris Godwin|Catches a pass on the edge, powers forward and is driven down near the 40.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:41|TB|Gainwell|Bursts up the middle for a first down at the 45.|None|run up the middle|Egbuka in motion|unknown|unknown|unverified (no DB match; caption-only)|
|03:55|TB|Cade Otton|Catches a checkdown with blockers ahead and gains 13 yards to the Cincinnati 42.|13|checkdown with blockers|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:06|TB|unidentified|Gains a first down on second-and-12; the action and ball carrier are omitted.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:15|TB|B.Mayfield|Escapes pressure and scrambles eight yards before B.Carter forces a fumble. B.Cook recovers in the end zone for a touchback.|8|scramble up the middle|unknown|unknown|B.Carter|verified vs DB|
|04:28|CIN|Samaje Perine|Turns a checkdown into a first down on third-and-eight against a four-man rush.|None|checkdown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:42|CIN|Chase Brown|Bounces off Tampa Bay defenders for nearly ten yards.|None|unknown|Chase in motion; Brown on the other side|unknown|unknown|unverified (no DB match; caption-only)|
|04:53|CIN|Joe Burrow; Ja'Marr Chase|Burrow floats a pass to Chase, who taps his toes for a first down.|None|play-action|under center|unknown|unknown|unverified (no DB match; caption-only)|
|05:14|CIN|Samaje Perine|Catches a pass over the middle, close to another first down.|None|pass over the middle|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:22|CIN|Joe Burrow; Tee Higgins|Higgins catches Burrow's pass on the run and lunges for a first down at the 16.|None|unknown|shotgun|unknown|unknown|unverified (no DB match; caption-only)|
|05:29|CIN|Joe Burrow; Drew Sample|Burrow finds a wide-open Sample down the sideline, close to a first down.|None|play-action|under center|unknown|unknown|unverified (no DB match; caption-only)|
|05:41|CIN|C.Brown|Scores on a five-yard run up the middle.|5|run up the middle|unknown|unknown|unknown|verified vs DB|
|05:55|TB|Baker Mayfield; receiver unidentified|Sets up a screen off play-action; Barrett Carter shuts it down at the 21.|None|play-action screen|unknown|unknown|Barrett Carter (stops the play)|unverified (no DB match; caption-only)|
|06:04|TB|B.Mayfield; C.Godwin|Godwin catches a short middle pass and runs to the Cincinnati 38 for 30 yards against a four-man rush.|30|short middle pass|unknown|unknown|D.Knight|verified vs DB|
|06:21|TB|Baker Mayfield; Egbuka|Egbuka holds a catch over the middle through a big hit near the 20.|None|pass over the middle|Gainwell in motion|unknown|unknown|unverified (no DB match; caption-only)|
|06:30|TB|Baker Mayfield; Cade Otton|Finds Otton up the far sideline off a play fake, close to a first down.|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:40|TB|B.Irving|Runs outside left for a ten-yard touchdown.|10|left-end run|unknown|unknown|unknown|verified vs DB|
|06:53|CIN|Joe Burrow; Mike Gesicki|Gesicki gains 16 yards to the 44 for a first down.|16|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:07|CIN|Joe Burrow; Mike Gesicki|With good protection, Burrow finds Gesicki for another first down at the Tampa Bay 45.|None|unknown|unknown|unknown|Trotter|unverified (no DB match; caption-only)|
|07:23|CIN|J.Burrow; M.Gesicki|Gesicki catches a short right pass for 25 yards to the Tampa Bay 20.|25|short right pass|unknown|unknown|Z.McCollum|verified vs DB|
|07:28|CIN|Joe Burrow|Keeps the ball and slides for a first down.|None|quarterback keeper|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:35|CIN|Joe Burrow; receiver unidentified|Completes a third-and-goal pass; the receiver and gain are omitted. The subsequent field goal establishes no touchdown.|None|unknown|Chase Brown in the backfield|unknown|unknown|unverified (no DB match; caption-only)|
|07:44|CIN|E.McPherson|Makes a 20-yard field goal after the holder handles a high snap.|20|field goal|unknown|unknown|unknown|verified vs DB|
|08:05|CIN|T.Brooks|Recovers his muffed kickoff catch and returns to the Cincinnati 27.|26|kickoff return|unknown|unknown|K.Knowles|verified vs DB|
|08:10|CIN|J.Burrow; T.Higgins|Burrow escapes pressure and finds Higgins, who steps through Morrison and gains 29 yards to the Tampa Bay 44.|29|short middle pass|unknown|unknown|Morrison; A.Winfield|verified vs DB|
|08:23|CIN|Chase Brown|Takes a pitch, breaks a tackle and reaches the Tampa Bay 31.|None|pitch|Erick All in motion|unknown|unknown|unverified (no DB match; caption-only)|
|08:37|CIN|Joe Burrow|Sacked by Josiah Trotter, identified as Trotter's first NFL sack.|None|unknown|unknown|unknown|Josiah Trotter (sack)|unverified (no DB match; caption-only)|
|08:43|CIN|E.McPherson|Makes a 55-yard field goal with distance to spare.|55|field goal|unknown|unknown|unknown|verified vs DB|
|08:55|TB|B.Irving|Catches a swing pass on third-and-two and gains 22 yards to the Cincinnati 42.|22|swing pass left|unknown|unknown|B.Cook|verified vs DB|
|09:14|TB|Baker Mayfield; Bucky Irving|Checks down to Irving, who reaches the 35 for his fifth catch.|None|checkdown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:21|TB|Baker Mayfield|Jonathan Allen sacks Mayfield for a nine-yard loss on third-and-seven.|-9|unknown|unknown|unknown|Jonathan Allen (sack)|unverified (no DB match; caption-only)|
|09:31|TB|C.McLaughlin|Makes a 51-yard field goal.|51|field goal|unknown|unknown|unknown|verified vs DB|
|09:41|CIN|J.Burrow; J.Trotter|Burrow's short right pass intended for A.Iosivas is intercepted by Trotter and returned 38 yards for a Tampa Bay touchdown.|38|short right pass; interception return|unknown|unknown|J.Trotter (interception)|verified vs DB|
|09:57|CIN|J.Burrow; M.Gesicki|Finds a wide-open Gesicki for 24 yards and a first down on third-and-ten against a four-man rush.|24|deep left pass|unknown|unknown|A.Winfield|verified vs DB|
|10:09|CIN|Meyers|Takes a handoff, breaks a tackle and gains a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:18|CIN|Joe Burrow|Flushed right by pressure and throws away with nobody open downfield.|0|throwaway|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:28|CIN|E.McPherson|Makes a 58-yard field goal.|58|field goal|unknown|unknown|unknown|verified vs DB|
|10:38|TB|Bucky Irving|Bursts forward for a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:43|TB|Baker Mayfield; Bucky Irving|Mayfield escapes pressure and finds Irving in open space for a first down.|None|pass after escaping pressure|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:57|TB|B.Mayfield|B.Mafe sacks Mayfield for a seven-yard loss and forces a fumble recovered by CIN-T.Slaton.|-7|strip sack|unknown|unknown|B.Mafe (sack/forced fumble)|verified vs DB|
|11:12|CIN|Samaje Perine|Breaks through initial resistance for a first down; Alex Anzalone tackles him.|None|unknown|unknown|unknown|Alex Anzalone|unverified (no DB match; caption-only)|
|11:21|CIN|Chase Brown|Finds room and stumbles forward to the 16.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:29|CIN|Joe Burrow; Chase Brown|Short toss to Brown on third-and-five ends short of the first down; captions place the finish at the nine.|None|short pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:37|CIN|E.McPherson|Makes a 32-yard field goal, his fourth successful attempt.|32|field goal|unknown|unknown|unknown|verified vs DB|
|11:54|TB|J.Williams|Returns the kickoff 47 yards to the TB 49.|47|kickoff return|unknown|unknown|E.McPherson|CONFLICT (yardage 47 vs DB)|
|12:07|TB|Baker Mayfield; Ted Hurst|Completes a sideline pass on first-and-15, identified by subsequent commentary as the first of three straight Hurst catches.|None|sideline pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:17|TB|Ted Hurst|Catches another pass for eight yards to the 32.|8|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:35|TB|Ted Hurst|Commentary confirms a third consecutive catch on the drive; the action and gain are omitted.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:38|TB|Baker Mayfield|Escapes pressure and scrambles up the sideline, going out inside the 15.|None|scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:45|TB|B.Mayfield|Scrambles nine yards for a touchdown, breaking Barrett Carter's tackle attempt.|9|scramble up the middle|unknown|unknown|Barrett Carter|verified vs DB|
|12:58|CIN|Dohnte Meyers|Runs in open space to the 42; captions do not establish how he received the ball.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:16|CIN|Samaje Perine|Advances into Tampa Bay territory to the 44.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:24|CIN|Joe Burrow; Tee Higgins|Higgins makes a leaping catch over the middle late in the closing drive.|None|pass over the middle|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:33|CIN|Chase Brown|Takes a handoff outside on second-and-six and stays inbounds, just short of a first down.|None|outside run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:47|CIN|Joe Burrow|Falls forward for a first down on third-and-one.|None|quarterback run|unknown|unknown|unknown|unverified (no DB match; caption-only)|

Offense (Codex synthesis from this game's plays): Burrow repeatedly found Gesicki for first downs and a touchdown. / Under-center play-action produced completions to Chase and a wide-open Sample. / Brown supplied a five-yard rushing touchdown and multiple gains through or beyond initial contact. / Late advances by Perine, Higgins and Brown preceded Burrow's third-and-one conversion to help close the game.

Defense weaknesses: Allowed Godwin's 30-yard reception and Irving's 22-yard swing reception. / Allowed Irving to score on a ten-yard outside run. / Mayfield escaped pressure for first downs and broke Carter's tackle attempt on his late touchdown. / Allowed three consecutive Hurst catches during Tampa Bay's final touchdown drive.

Limitations: Captions only; no video frames were available. Missing commentary prevents reliable identification of many receivers, gains, alignments, routes and defenders. No specific coverage scheme or personnel grouping was explicitly established. Formation entries use commentary only; concepts also use clearly matching DB text. NO DB MATCH means no matching play in the supplied selective DB excerpt. db_match records the matching quarter and clock. For defensive touchdowns, team remains the team on offense; yards records the scoring return distance, as in the supplied DB event. Field-goal yards are kick distances. Named tacklers and defenders making stops are included in defender_beaten without implying they were beaten. The Bryce Young game-break fragment is excluded as another game's action. The late Meyers play cannot be matched to the supplied kickoff return: the DB names T.Brooks and ends that return at the 24, while captions describe Meyers reaching the 42. Extra points and kickoffs absent from the captions are not added.


## Week 2: CIN 20 - HOU 6 (game 401872934)
Video: Cincinnati Bengals vs Houston Texans Game Highlights | 2026 NFL Season Week 2 — https://www.youtube.com/watch?v=Bi13ofXC0xY  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:18|CIN|unknown|Burrow completes a pass for eight yards; Al-Shaair finishes the tackle against a stated four-man rush.|8|unknown|unknown|unknown|Azeez Al-Shaair|unverified (no DB match; caption-only)|
|00:31|CIN|Joe Burrow|Sacked on third-and-11; Anderson holds him and Hall finishes.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:43|HOU|Montgomery|Runs for four yards on first-and-10.|4|unknown|pistol|unknown|unknown|unverified (no DB match; caption-only)|
|00:59|HOU|Hutchinson|Stroud throws outside incomplete on third-and-five, with Hill covering.|0|outside pass|unknown|unknown|Hill (coverage; pass incomplete)|unverified (no DB match; caption-only)|
|01:17|CIN|unknown|Gains ten yards to the 45 for a first down; ball carrier and play type are unclear.|10|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:24|CIN|Colby Young|Catches a quick pass up the middle for seven yards on first-and-20.|7|quick middle pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:36|CIN|Chase Brown|Gains six yards up the middle; the captions do not establish whether this was a handoff or reception.|6|up the middle; play type unclear|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:48|HOU|unknown tight end|Second-and-ten completion to a tight end around the 14; Woody Marks is identified as the running back.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:05|HOU|Dalton Schultz|Catches Stroud's short right pass, escapes along the sideline and gains 35 yards to midfield.|35|short right pass with yards after catch|unknown|unknown|J.Battle|verified vs DB|
|02:19|HOU|unknown|Receiver described as a former Patriot acquired by trade catches a pass for 15 yards to the 45.|15|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:35|HOU|unknown|Fragment describes a defender coming through and knocking a player down; a sack cannot be established.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:47|HOU|unknown|Underneath completion on third-and-12 from the 34 gains a first down inside the 12; exact gain and receiver are unclear.|None|underneath pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:00|HOU|Woody Marks|Stroud dumps a pass toward Marks from a messy pocket on third-and-eight; coverage and a flag are mentioned, but the outcome is unclear.|None|dump-off|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:14|HOU|unknown|Bobbed snap on an apparent field-goal attempt leads to a chased player throwing the ball away. Cincinnati takes over at its 16.|None|broken field-goal operation|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:43|CIN|Chase Brown|Runs up the middle for seven yards to approximately the 23.|7|run up the middle|motion mentioned; formation unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:52|CIN|Tee Higgins|Burrow throws on the move to Higgins for 21 yards to the Cincinnati 44.|21|short middle pass; quarterback on the move|unknown|unknown|R.Blankenship; D.Stingley|verified vs DB|
|04:05|CIN|Joe Burrow|Danielle Hunter sacks Burrow for a seven-yard loss.|-7|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:17|CIN|Chase Brown|Shovel pass gains one yard; Rankins reads it and stops Brown short of the first down.|1|shovel pass|unknown|unknown|Rankins (successful stop)|unverified (no DB match; caption-only)|
|04:30|HOU|unknown|Middle gain with a hurdle reaches approximately the Cincinnati 41; commentary says 26 yards. This may correspond to the DB's 25-yard Moreau reception, but the captions do not establish the receiver or play type clearly enough.|26|up the middle; play type unclear|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:49|HOU|Dalton Schultz|Reception gains 11 yards and a first down; Davis makes the tackle.|11|unknown|unknown|unknown|Davis|unverified (no DB match; caption-only)|
|05:05|HOU|Montgomery|Catches a middle pass on third-and-nine and finishes approximately two inches short; Hill makes initial contact.|None|middle pass|unknown|unknown|Hill|unverified (no DB match; caption-only)|
|05:17|HOU|Montgomery|Stopped on the ensuing short-yardage run; Dexter Lawrence and Carter are credited.|None|short-yardage run|unknown|unknown|Dexter Lawrence; Carter (successful stop)|unverified (no DB match; caption-only)|
|05:29|CIN|Tee Higgins|Third-and-eight reception gains 17 yards to the 41.|17|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:46|CIN|Tee Higgins|Underneath reception on third-and-four becomes a 23-yard catch-and-run; commentary says nobody is on Higgins.|23|short middle pass with yards after catch|unknown|unknown|A.Al-Shaair|verified vs DB|
|06:00|CIN|Ja'Marr Chase|Catches a contested 32-yard touchdown over Stingley, securing possession and getting both feet down.|32|deep right shot|unknown|unknown|Derek Stingley|verified vs DB|
|06:51|HOU|Hutchinson|Middle reception gains 13 yards to the 40; Hill tackles from behind.|13|middle pass with yards after catch|unknown|unknown|Hill|unverified (no DB match; caption-only)|
|07:06|HOU|Hutchinson|Stroud escapes a messy pocket and finds an open Hutchinson downfield to the 17.|None|downfield pass after quarterback escape|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:17|HOU|C.J. Stroud|Throws away on third-and-13 against five rushers; Lawrence applies pressure and Davis is also mentioned.|0|throwaway|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:35|HOU|Ka'imi Fairbairn|Makes a 37-yard field goal to cut the deficit to 7-3.|37|field goal|unknown|unknown|unknown|verified vs DB|
|07:49|CIN|Tee Higgins|Dives for a first down on a ten-yard reception; Al-Shaair tackles him.|10|unknown|unknown|unknown|Azeez Al-Shaair|unverified (no DB match; caption-only)|
|08:02|CIN|Joe Burrow|Sacked by Anderson on second-and-ten against a four-man rush.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:18|CIN|Chase Brown|Receives a pass from Burrow on third-and-15; Rankins and others make the stop.|None|unknown|unknown|unknown|Rankins|unverified (no DB match; caption-only)|
|08:34|HOU|unknown|Stroud completes a first-and-ten pass up the middle in front of a defender whose name is transcribed as 'Max Hill.'|None|middle pass|unknown|unknown|Hill (first name unclear)|unverified (no DB match; caption-only)|
|08:49|CIN|unknown tight end|Burrow completes a short pass to a tight end; Henderson makes the tackle.|None|short pass|unknown|unknown|Henderson|unverified (no DB match; caption-only)|
|09:06|CIN|unknown|Handoff loses four yards, pushing Cincinnati back to the 40.|-4|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:09|CIN|unknown|Underneath completion finishes short of the first down near the Houston 33; Blankenship makes the tackle.|None|underneath pass|unknown|unknown|Blankenship|unverified (no DB match; caption-only)|
|09:21|CIN|Evan McPherson|Makes a 51-yard field goal for a 10-3 lead.|51|field goal|unknown|unknown|unknown|verified vs DB|
|09:44|HOU|unknown|Fragment describes a player wrestled down at the 39 for a first down; play type and gain are unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:45|HOU|C.J. Stroud|Runs up the middle for a first down; Knight is mentioned on the stop.|None|quarterback run up the middle|unknown|unknown|Knight|unverified (no DB match; caption-only)|
|09:56|HOU|Woody Marks|Catches a pass for nine yards to the Cincinnati 40. Captions conflict about whether it earns a first down or sets up second-and-one.|9|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:09|HOU|unknown|Third-and-one carry is stopped by T.J. Slaton, bringing up fourth down.|None|short-yardage run|unknown|unknown|T.J. Slaton (successful stop)|unverified (no DB match; caption-only)|
|10:22|HOU|Ka'imi Fairbairn|Misses a 58-yard field goal short.|58|field goal|unknown|unknown|unknown|verified vs DB|
|10:36|CIN|Joe Burrow|Escapes pressure and gains a first down to the Houston 33; wording suggests a scramble but does not conclusively establish the finish.|None|quarterback escape; apparent scramble|two tight ends with Higgins and Chase; full personnel unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:51|CIN|Chase Brown|Runs for ten yards and a first down on second-and-ten.|10|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:02|CIN|Ja'Marr Chase|Catches an 18-yard touchdown on third-and-six against four rushers. Commentary explains that Chase goes behind Al-Shaair as Burrow breaks the pocket.|18|deep right pass; scramble adjustment behind Al-Shaair|unknown|unknown|Azeez Al-Shaair|verified vs DB|
|11:32|HOU|Kayshon Boutte|Catches Stroud's deep left pass for 21 yards; commentary places the catch near the 25, while the DB ends it at the Cincinnati 26.|21|deep left pass|empty backfield|unknown|J.Davis|verified vs DB|
|11:43|HOU|C.J. Stroud|Hit while throwing on third-and-11; an apparent incompletion brings up fourth down. Seven defenders are stated to be at the line.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:58|CIN|Tee Higgins|Makes a spinning sideline catch on third-and-five for 23 yards.|23|deep right sideline pass|unknown|unknown|D.Stingley|verified vs DB|
|12:15|CIN|Tee Higgins|Cannot complete a catch with Pitre right there.|0|unknown|unknown|unknown|Pitre (coverage; pass incomplete)|unverified (no DB match; caption-only)|
|12:20|CIN|Evan McPherson|Makes a 57-yard field goal to extend the lead to 20-6.|57|field goal|unknown|unknown|unknown|verified vs DB|
|12:40|HOU|Jaylin Noel|Catches a deep left pass to the Cincinnati 49. Commentary says 32 yards; the matching DB play records 31.|31|deep left shot|unknown|unknown|Turner (nearby in commentary)|CONFLICT (yardage 31 vs DB)|
|12:49|HOU|Woody Marks|Run finds no room; Allen makes the initial hit and Knight finishes.|None|run; direction unknown|unknown|unknown|Allen; Knight (successful stop)|unverified (no DB match; caption-only)|
|13:02|HOU|C.J. Stroud|Lawrence brings down the quarterback on third-and-11; a flag is thrown, leaving the official result unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:16|CIN|Ja'Marr Chase|Gains approximately five yards on a pass described first as a swing pass and then as a jet sweep pass.|5|swing pass / jet sweep pass, both stated in commentary|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:30|CIN|unknown|Burrow's quick throw is broken up by Stingley.|0|quick pass|unknown|unknown|Stingley (pass breakup)|unverified (no DB match; caption-only)|
|13:41|HOU|C.J. Stroud|Sacked on second-and-six; Jenkins brings him down and Howell is credited with a hit.|None|unknown|empty backfield; Montgomery split wide|unknown|unknown|unverified (no DB match; caption-only)|
|13:52|HOU|Kayshon Boutte|Drops a third-and-11 pass with Lawrence pressuring Stroud against a four-man rush.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:04|CIN|Joe Burrow|Rankins sacks Burrow on third-and-eight against six rushers.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:12|HOU|C.J. Stroud|Against a four-man rush, a fragment describes a player staggering and being tripped by Allen before fourth-and-one. Whether this is a scramble or a completion is unclear.|None|unknown|unknown|unknown|Allen|unverified (no DB match; caption-only)|
|14:24|HOU|unknown|Fourth-and-one pass falls incomplete with Battle there; Cincinnati takes over on downs.|0|unknown|unknown|unknown|Battle (coverage; pass incomplete)|unverified (no DB match; caption-only)|
|14:35|CIN|Chase Brown|Takes a handoff, bounces outside and is driven back by Anderson; the official gain or loss is not stated.|None|run bouncing outside|quarterback under center|unknown|Anderson (successful stop)|unverified (no DB match; caption-only)|
|14:47|CIN|Chase Brown|Runs on third-and-13 to near the 39; Jake Hanson makes the tackle.|None|run; direction unknown|unknown|unknown|Jake Hanson|unverified (no DB match; caption-only)|
|14:57|HOU|Dalton Schultz|Stroud is flushed against four rushers and completes to Schultz for a first down near the 30; Hill and others tackle him. The captioned gain of '111' is unusable.|None|pass after quarterback escape|unknown|unknown|Hill|unverified (no DB match; caption-only)|
|15:13|HOU|Dalton Schultz|Makes a 25-yard catch to the Cincinnati 40 in front of Battle on third-and-five.|25|deep middle pass|unknown|unknown|J.Battle|verified vs DB|
|15:26|HOU|C.J. Stroud|Cedric Johnson sacks Stroud after an attempted escape. Commentary describes three rushers and eight defenders inside the five-yard line.|None|unknown|unknown|eight defenders inside the five-yard line; coverage type unknown|unknown|unverified (no DB match; caption-only)|

Offense (Codex synthesis from this game's plays): Higgins repeatedly moved the chains: identified gains of 21, 17, 23, 10 and 23 yards, including underneath yards after catch and a spinning sideline reception. / Chase supplied both touchdowns: a contested 32-yard deep reception against Stingley and an 18-yard score after adjusting behind Al-Shaair as Burrow left the pocket. / Brown contributed seven- and ten-yard runs, although other rushing plays were stopped or lost yardage. / McPherson converted the captioned 51- and 57-yard field goals.

Defense weaknesses: Allowed Schultz a 35-yard catch-and-run and a late 25-yard middle reception. / Allowed additional downfield gains to Boutte and Noel, plus an open Hutchinson reception to the 17 after Stroud escaped pressure. / Stroud gained a first down on a middle run, showing at least one escape from defensive containment.

Limitations: Captions only; no frames were viewed and no commands were run. Several fragments leave receivers, play types, gains and penalty outcomes unresolved. NO DB MATCH means no confident match in the supplied selective DB excerpt, not that the play did not occur. The 04:30 gain may be Moreau's listed 25-yard reception, but conflicting and incomplete commentary prevents a firm match. The isolated word 'intercepted' at 05:42 does not establish an interception. The Houston 45-yard field goal and listed kickoff returns are not identifiable in these captions. Matched DB yardage takes precedence over conflicting spoken yardage. Formation and coverage entries use commentary only; DB shotgun labels were not imported. Rush counts and defenders at the line do not establish a coverage scheme. The defender_beaten field includes named tacklers or coverage defenders as requested; inclusion does not establish that a defender was beaten. Unmatched names remain as captioned when their full identities cannot be established.


## Week 3: CIN 27 - PIT 30 (game 401872950)
Video: Cincinnati Bengals vs. Pittsburgh Steelers Game Highlights | NFL 2026 Season Week 3 — https://www.youtube.com/watch?v=sqOhOfjHhaI  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 4: JAX 22 - CIN 17 (game 401872969)
Video: Jacksonville Jaguars vs Cincinnati Bengals Game Highlights | 2026 NFL Season Week 4 — https://www.youtube.com/watch?v=a2zogEoiXV0  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 5: CIN 31 - MIA 24 (game 401872982)
Video: Cincinnati Bengals vs Miami Dolphins Game Highlights | 2026 NFL Season Week 5 — https://www.youtube.com/watch?v=veMELeUzxeo  | captions: yes

_No Codex film notes (no captions or run not completed)._
