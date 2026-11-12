# CIN — Phase 8 film notes (Weeks 1–6, 2026)
> Note: games 401872950, 401872969, 401872982 were extracted by Grok via the xAI API (grok-4.20-0309-non-reasoning, same prompt/schema as Codex, cleaned captions); sidecar provenance in film/grok_meta/. All other games with notes: Codex.

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

Offense (model synthesis from this game's plays): Burrow repeatedly found Gesicki for first downs and a touchdown. / Under-center play-action produced completions to Chase and a wide-open Sample. / Brown supplied a five-yard rushing touchdown and multiple gains through or beyond initial contact. / Late advances by Perine, Higgins and Brown preceded Burrow's third-and-one conversion to help close the game.

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

Offense (model synthesis from this game's plays): Higgins repeatedly moved the chains: identified gains of 21, 17, 23, 10 and 23 yards, including underneath yards after catch and a spinning sideline reception. / Chase supplied both touchdowns: a contested 32-yard deep reception against Stingley and an 18-yard score after adjusting behind Al-Shaair as Burrow left the pocket. / Brown contributed seven- and ten-yard runs, although other rushing plays were stopped or lost yardage. / McPherson converted the captioned 51- and 57-yard field goals.

Defense weaknesses: Allowed Schultz a 35-yard catch-and-run and a late 25-yard middle reception. / Allowed additional downfield gains to Boutte and Noel, plus an open Hutchinson reception to the 17 after Stroud escaped pressure. / Stroud gained a first down on a middle run, showing at least one escape from defensive containment.

Limitations: Captions only; no frames were viewed and no commands were run. Several fragments leave receivers, play types, gains and penalty outcomes unresolved. NO DB MATCH means no confident match in the supplied selective DB excerpt, not that the play did not occur. The 04:30 gain may be Moreau's listed 25-yard reception, but conflicting and incomplete commentary prevents a firm match. The isolated word 'intercepted' at 05:42 does not establish an interception. The Houston 45-yard field goal and listed kickoff returns are not identifiable in these captions. Matched DB yardage takes precedence over conflicting spoken yardage. Formation and coverage entries use commentary only; DB shotgun labels were not imported. Rush counts and defenders at the line do not establish a coverage scheme. The defender_beaten field includes named tacklers or coverage defenders as requested; inclusion does not establish that a defender was beaten. Unmatched names remain as captioned when their full identities cannot be established.


## Week 3: CIN 27 - PIT 30 (game 401872950)
Video: Cincinnati Bengals vs. Pittsburgh Steelers Game Highlights | NFL 2026 Season Week 3 — https://www.youtube.com/watch?v=sqOhOfjHhaI  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:32|PIT|J.Warren|Dumpdown pass to Warren, creating after the catch down the sideline, spun down at CIN 42|30|unknown|unknown|unknown|unknown|verified vs DB|
|00:47|PIT|R.Wilson|Rodgers pass caught by Wilson for touchdown|38|deep shot|unknown|unknown|unknown|verified vs DB|
|01:13|CIN|J.Chase|Burrow gets rid of it quickly, catch made by Chase, picks up nine yards on the catch and run|9|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:22|CIN|D.Meyers|Burrow from the gun lets it fly, complete to Dohnte Meyers, major yards after the catch into Pittsburgh territory inside the 30|23|unknown|unknown|unknown|unknown|verified vs DB|
|01:36|CIN|T.Higgins|Burrow steps up, throws on the move and hits his man across the 20 to Tee Higgins|10|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:47|CIN|J.Chase|Burrow step to the throw out across the middle to Chase, limited to a gain of seven|7|unknown|unknown|unknown|J.Ramsey|unverified (no DB match; caption-only)|
|02:03|CIN|S.Perine|Inside run to Perine, five-yard pickup, first and goal|5|run gap/direction|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:14|CIN|J.Chase|Fake the handoff, Burrow will throw it, the catch is made, Ja'Marr Chase is in for touchdown|3|play-action|unknown|unknown|unknown|verified vs DB|
|02:32|PIT|D.Metcalf|Rodgers, the quick hitter. Metcalf is spun down but secures it and picks up 11|11|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:42|PIT|R.Wilson|Third and 11, Rodgers has time, a BB over the middle for a first down. Roman Wilson has been heavily involved|22|unknown|unknown|unknown|unknown|verified vs DB|
|02:56|PIT|J.Warren|Jaylen Warren lowering the shoulder, first down run to the outside by Warren, 13-yard rip|13|run gap/direction|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:04|PIT|D.Washington|Second and 10, they get Washington involved. He's a mountain of a man. First down.|8|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:18|PIT|M.Pittman|Rodgers step and throw. It's complete. And a first down catch is made by Pittman. Eight-yard pickup|8|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:30|PIT|B.Skowronek|Fake the handoff. Rodgers looking. End zone. Touchdown! Skowronek for the score!|23|play-action|unknown|unknown|unknown|verified vs DB|
|03:45|CIN|J.Chase|Brown remains in there. Shifts to the other side of Burrow. Fake the handoff. Burrow complete to Chase. First down, out near midfield. 13 yards through the air.|13|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:58|CIN|J.Chase|Third down and 3. Burrow looking for Chase. He's got him for the first down. The versatility Ja'Marr Chase.|10|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:07|CIN|S.Perine|Facing a third and 9. Deep drop. Burrow. Dump-off. They'll get that yardage back with Perine. Five-yard pickup through the air.|5|screen|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:23|CIN|E.McPherson|They're going to kick the field goal. From 50 yards away, Evan McPherson. The 50-yarder is pure. 14-10.|50|unknown|unknown|unknown|unknown|verified vs DB|
|04:44|PIT|J.Warren|Handoff to Jaylen Warren. Warren is still going. Finally caught from behind. Huge run for Warren.|35|run gap/direction|unknown|unknown|B.Mafe|CONFLICT (yardage 35 vs DB)|
|04:57|PIT|M.Pittman|Rodgers steps up. Rodgers zips it. The catch is made by Pittman. And he works his way inside the 25. They get some quality yards there. Eight for their field goal unit.|8|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:10|PIT|C.Boswell|Going to be a 44-yard attempt. Trying to build on the lead. Boswell knocks it through. 17-10, Steelers.|44|unknown|unknown|unknown|unknown|verified vs DB|
|05:20|CIN|C.Brown|Up in the I. Brown slices through and takes it to the 39 for a gain of eight. Tackle by Holcomb of Pittsburgh.|8|run gap/direction|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:33|CIN|S.Perine|This is a third and 4. Perine in for extra protection. Burrow will dump it off to him and broken up.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:42|PIT|P.Freiermuth|Fake the handoff. Rodgers sells it. And he flicks it downfield to Freiermuth. Finally spun down as he crosses the 45.|22|play-action|unknown|unknown|unknown|verified vs DB|
|06:07|PIT|D.Washington|Rodgers throws it into traffic. Incomplete. Darnell Washington the tight end matched up with the linebacker, Barrett Carter.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:16|PIT|P.Freiermuth|Freiermuth is back in there for Pittsburgh. Rodgers looking in that direction and forced to go over the middle. Up in the air and intercepted by Jordan Battle.|0|unknown|unknown|unknown|J.Battle|verified vs DB|
|06:27|CIN|J.Chase|Mike Gesicki is back in there for Cincinnati. Burrow, straight back. He will throw it. The hands of Ja'Marr Chase. He hauls it in at the 32.|15|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:40|CIN|T.Higgins|Burrow looking up top. And somehow ends up in the hands of Tee Higgins for a touchdown! Spectacular!|28|deep shot|unknown|unknown|unknown|verified vs DB|
|07:27|CIN|C.Brown|Six-yard gain up the middle for Chase Brown.|6|run gap/direction|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:36|CIN|C.Brown|Second and 4. That creates a hole for Brown, and he accelerates through it for a first down. 14 yards.|14|run gap/direction|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:46|CIN|J.Burrow|Second down and 2. On the roll. Burrow going to step up and run for the first down.|3|RPO|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:01|CIN|S.Perine|Third and short. Burrow, they try to pass down low to Perine, and Steelers are saying incomplete. Officials agree. And now it's fourth down.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:15|CIN|J.Chase|A fourth and 2. Burrow. One-on-one. It's caught by Chase for the first down. Asante Samuel back there defensively. Chase does his job. This drive remains alive. It's a 21-yard hookup.|21|unknown|unknown|unknown|A.Samuel|verified vs DB|
|08:32|CIN|T.Higgins|Third and 9 for Burrow and the Bengals. Burrow laces it to the sideline. Incomplete. Tee Higgins.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:39|CIN|E.McPherson|Rico, the punter holds it. 38-yard attempt. McPherson, he's got it. 20-17, Bengals.|38|unknown|unknown|unknown|unknown|verified vs DB|
|08:49|PIT|J.Warren|The first half on that final play, he's shaking it off, as he dumps to Warren. First down, Pittsburgh. It's an 11-yard catch and run.|11|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:03|PIT|D.Metcalf|Here comes the rush. Rodgers, pump, throw, lays it out there. Incomplete. Freiermuth had a step, but they could not complete it. He had that one to Metcalf in the second quarter.|0|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:27|PIT|J.Warren|Single running back is Warren. Warren breaks a tackle. They'll push him forward, just short of a first down. It's a gain of nine.|9|run gap/direction|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:44|PIT|J.Bernard|Fake the handoff. Rodgers in the crowd, makes the connection to Jeremy Bernard, the rookie from Alabama. First down, 13 yards.|13|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:55|PIT|J.Warren|Quick hitter to Warren. Slices through and nearly goes the distance. He's tripped up at the last moment. It's a gain of nine. It's going to set up third down and 1.|9|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:07|PIT|D.Metcalf|Motion man, Freiermuth. Fake it. Rodgers, looking, wide open, touchdown to Metcalf! The Steelers go back in front.|6|play-action|unknown|unknown|unknown|verified vs DB|
|10:23|CIN|T.Higgins|Bengals open up first and 10 at their own 36. Burrow, under duress, makes the connection with Higgins. And they will whistle him down after a gain of 14, out to midfield.|14|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:38|CIN|T.Higgins|It's a dime package for Pittsburgh. Burrow. Caught by Higgins. Quiets the crowd. Takes it to the 33, a gain of 17.|17|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:47|CIN|S.Perine|Third and 2. Inside run. Perine. It looked like he had a head of steam, and then the Steelers stop him. No gain on the play.|0|run gap/direction|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:58|CIN|J.Chase|Out of his hands quickly. Chase on the move. Burrow guns it downfield. It's caught! Gesicki with the go-ahead touchdown!|25|deep shot|unknown|unknown|unknown|verified vs DB|
|11:15|PIT|J.Warren|It's a give to Warren. Spin move to the 35. It's going to be just short of a first down.|9|run gap/direction|unknown|unknown|unknown|CONFLICT (yardage 9 vs DB)|
|11:24|PIT|P.Freiermuth|Line of scrimmage is the 36. Rodgers. Steps up, puts the pass downfield. Nearly intercepted. He was trying to hit Freiermuth, and Davis, the rookie, was over there.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:34|PIT|R.Wilson|Shotgun for Rodgers. Deep drop. Rodgers, up in the air, incomplete. Roman Wilson left his feet, one-on-one with Hill. Could not bring it in. It's fourth down.|0|deep shot|unknown|unknown|D.Hill|unverified (no DB match; caption-only)|
|11:48|PIT|S.Skowronek|No rush on Cameron Johnston. Ke'Shawn Williams muffs the punt. Ball was still free. Steelers got down the field in a hurry. Pittsburgh's got it. Potential game-changing play. Skowronek ends up with the football.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:19|PIT|C.Boswell|36-yard attempt for Boswell. He converts.|36|unknown|unknown|unknown|unknown|verified vs DB|
|12:37|CIN|T.Higgins|Second and 10. Burrow steps up. He slings it out near midfield. Catch is made shy of the 50 by Tee Higgins. It's a gain of 7.5.|8|unknown|unknown|unknown|R.Jenkins|unverified (no DB match; caption-only)|
|12:51|CIN|J.Chase|Motion man is Hudson. Third down and 3. Burrow stepping up in the pocket... in fact, they go back a yard.|-1|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:59|PIT|D.Metcalf|Rodgers throws it. Complete. It's Metcalf. First down across the 20-yard line for 14.|14|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:11|PIT|D.Washington|Fake the handoff. Rodgers calls for the tight end Washington. The big man works his way to the sideline! Washington! Immense play for Pittsburgh!|47|play-action|unknown|unknown|unknown|verified vs DB|
|13:38|PIT|C.Boswell|For Chris Boswell. Snap, kick, Steelers take the lead. 2:15 to play, 30-27 Pittsburgh.|33|unknown|unknown|unknown|unknown|verified vs DB|
|13:45|CIN|J.Chase|Cincinnati. Burrow, fires over the middle. Caught by Chase. Chase breaks a tackle. And spins out of another for extra yards to the 47. Brought down by Jenkins. That's good for 17 yards.|17|unknown|unknown|unknown|R.Jenkins|unverified (no DB match; caption-only)|
|13:58|CIN|C.Brown|Time-out remaining. Burrow, the dumpoff to Brown, and it is blown up by Patrick Queen. A loss of four on the play.|-4|unknown|unknown|unknown|P.Queen|unverified (no DB match; caption-only)|
|14:10|CIN|M.Gesicki|Second and 14. Burrow sees the open man, hits Gesicki, but the Steelers don't allow him to take it past midfield. It's going to bring up third down with just over a minute to go.|10|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:21|CIN|J.Chase|Inside the 40. Burrow on third and 8. To the sideline, it's caught by Chase. First down for the Bengals in Pittsburgh territory, 13-yard.|13|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:32|CIN|J.Burrow|Burrow, deep drop, and Burrow gets away for a moment, loses the ball. Derrick Harmon got there. Steelers trying to jump on to have of it, and they do!|-8|unknown|unknown|unknown|D.Harmon|verified vs DB|

Offense (model synthesis from this game's plays): Explosive deep passing game with accurate throws from Burrow to Chase, Higgins, and Gesicki for big gains and touchdowns / Effective use of play-action and RPO concepts leading to successful runs and passes / Versatile receivers like Chase who can be deployed anywhere and create after the catch / Ability to convert on third downs and sustain long drives with a mix of run and pass

Defense weaknesses: Susceptible to big runs by PIT backs like Warren (35+ yards) / Vulnerable in coverage to PIT tight ends and receivers on intermediate and deep routes leading to TDs / Missed opportunities on interceptions and allowing long pass plays (30+ yards) / Struggled to stop PIT's red zone efficiency and third down conversions

Limitations: Could not determine specific personnel formations or coverage schemes as they were not explicitly stated by commentators. Many plays in captions had approximate or no exact DB matches due to name mangling, paraphrasing, or non-highlight DB filtering; yards often had to be inferred or used from closest DB match. Some player names corrected only on clear matches. Several plays lacked explicit concept, defender, or direction details in commentary.


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

Offense (model synthesis from this game's plays): WR and TE production with Higgins, Chase, Gesicki, Meyers stepping up / Ability to convert third downs and sustain drives / Explosive passing plays and YAC / QB mobility and improvisation under pressure

Defense weaknesses: Struggled containing JAX TEs / Allowed big passing plays and YAC / Missed tackles in open field / Vulnerable on long field goals

Limitations: Could not determine specific concepts like run gaps, play-action (except one explicit), personnel, formations, or coverages as they were not explicitly stated by commentators. Many plays had unclear or no exact DB matches due to name mangling and timing. Some yardage and details were approximate or not fully specified in captions. Could not identify all defender names or exact scores on every play.


## Week 5: CIN 31 - MIA 24 (game 401872982)
Video: Cincinnati Bengals vs Miami Dolphins Game Highlights | 2026 NFL Season Week 5 — https://www.youtube.com/watch?v=veMELeUzxeo  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:28|CIN|D.Meyers|81 yard kickoff return|81|unknown|unknown|unknown|unknown|verified vs DB|
|00:45|CIN|M.Gesicki|4 yard TD pass from J.Burrow|4|unknown|unknown|unknown|unknown|verified vs DB|
|01:14|MIA|C.Washington|Rush for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:25|MIA|O.Gordon|22 yard rush|22|unknown|unknown|unknown|unknown|verified vs DB|
|01:35|MIA|O.Gordon|1 yard rushing TD|1|unknown|unknown|unknown|unknown|verified vs DB|
|02:58|CIN|T.Higgins|Pass completion on slant|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:39|CIN|S.Perine|6 yard TD pass from J.Burrow|6|unknown|unknown|unknown|unknown|verified vs DB|
|04:04|MIA|J.Tolbert|22 yard pass reception|22|unknown|unknown|unknown|unknown|verified vs DB|
|04:14|MIA|M.Willis|Pass intercepted by J.Battle|None|unknown|unknown|unknown|unknown|verified vs DB|
|05:44|CIN|J.Burrow|Fumble recovered by MIA|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:35|MIA|M.Willis|Pass intercepted by CIN|None|unknown|unknown|unknown|unknown|verified vs DB|
|06:55|CIN|T.Hudson|Pass completion for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:19|CIN|J.Chase|Pass completion to the 1 yard line|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:29|CIN|T.Hudson|2 yard TD pass from J.Burrow|2|unknown|unknown|unknown|unknown|verified vs DB|
|08:57|MIA|M.Washington|28 yard punt return|28|unknown|unknown|unknown|unknown|verified vs DB|
|09:13|MIA|C.Bell|26 yard rush|26|unknown|unknown|unknown|unknown|verified vs DB|
|10:16|MIA|R.Patterson|29 yard field goal|29|unknown|unknown|unknown|unknown|verified vs DB|
|10:55|CIN|J.Chase|45 yard TD pass from J.Burrow|45|deep shot|unknown|unknown|unknown|verified vs DB|
|11:33|MIA|M.Willis|39 yard scramble|39|unknown|unknown|unknown|unknown|verified vs DB|
|12:14|MIA|K.Coleman|3 yard TD pass from M.Willis (2pt conversion good)|3|unknown|unknown|unknown|unknown|verified vs DB|
|13:31|MIA|M.Willis|Sacked and fumbled, recovered by J.Allen|-4|unknown|unknown|unknown|J.Allen|verified vs DB|
|14:02|CIN|E.McPherson|26 yard field goal|26|unknown|unknown|unknown|unknown|verified vs DB|
|14:41|MIA|G.Dulcich|Pass reception on sideline|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:47|MIA|M.Willis|1 yard rushing TD|1|unknown|unknown|unknown|unknown|verified vs DB|

Offense (model synthesis from this game's plays): Explosive big plays in passing game with deep shots to J.Chase / Effective use of multiple tight ends and RBs in short yardage and red zone / High third down conversion rate / Quick scoring drives with accurate passing from J.Burrow

Defense weaknesses: Susceptible to big run plays allowing 20+ yard gains / Defensive penalties leading to extended drives / Vulnerable to explosive plays from opposing RBs and WRs

Limitations: Could not determine specific concepts like run gaps, play-action, screens, RPOs, personnel formations, or coverage schemes because the captions and DB rarely explicitly state them. Many plays in captions had no direct DB match due to timing or description differences. Some player names were corrected using DB where matches were clear. Defender beaten names were limited to those mentioned. Several plays lacked yardage or exact details.
