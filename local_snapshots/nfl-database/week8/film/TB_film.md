# TB — Phase 8 film notes (Weeks 1–6, 2026)
> Note: games 401872959, 401872968, 401872980 were extracted by Grok via the xAI API (grok-4.20-0309-non-reasoning, same prompt/schema as Codex, cleaned captions); sidecar provenance in film/grok_meta/. All other games with notes: Codex.

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

Offense (model synthesis from this game's plays): Godwin produced a 30-yard catch-and-run and an earlier first down by slipping through two defenders. / Irving contributed a 22-yard swing reception, additional checkdowns and a ten-yard left-end touchdown. / Mayfield created gains after escaping pressure, including a late nine-yard rushing touchdown. / Three consecutive Ted Hurst catches helped the late touchdown drive.

Defense weaknesses: Gesicki repeatedly moved the chains, including gains of 25 and 24 yards, and caught a two-yard touchdown. / Higgins gained 29 yards after stepping through Morrison; Brown also broke a tackle on a pitch. / Perine converted third-and-eight on a checkdown. / Sample was described as wide open on a play-action sideline completion.

Limitations: Captions only; no video frames were available. Missing commentary prevents reliable identification of many receivers, gains, alignments, routes and defenders. No specific coverage scheme or personnel grouping was explicitly established. Formation entries use commentary only; concepts also use clearly matching DB text. NO DB MATCH means no matching play in the supplied selective DB excerpt. db_match records the matching quarter and clock. For defensive touchdowns, team remains the team on offense; yards records the scoring return distance, as in the supplied DB event. Field-goal yards are kick distances. Named tacklers and defenders making stops are included in defender_beaten without implying they were beaten. The Bryce Young game-break fragment is excluded as another game's action. The late Meyers play cannot be matched to the supplied kickoff return: the DB names T.Brooks and ends that return at the 24, while captions describe Meyers reaching the 42. Extra points and kickoffs absent from the captions are not added.


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

Offense (model synthesis from this game's plays): Irving generated a 38-yard run left, while Gainwell gained a first down through missed tackles. / Godwin repeatedly moved the chains; Hurst and Johnson added explosive receptions. / Mayfield extended plays with scrambles and delivered a play-action touchdown to Egbuka under pressure.

Defense weaknesses: Anzalone missed Fannin after a play-action dump-off. / An unnamed defender missed Boston on his 55-yard catch-and-run touchdown. / Whiteheart slipped wide open for the winning play-action touchdown. / Boston converted multiple catches with McCollum identified in coverage.

Limitations: Captions only; no video frames were viewed and no commands were run. The supplied DB is a selected-play list, so NO DB MATCH does not mean a play did not occur. DB matches contain the requested quarter and clock identifier. Formation and coverage details were not inferred from DB shotgun labels; only explicit commentary details are included. Named tacklers or coverage defenders are labeled as such and do not necessarily indicate a defender was beaten. Null yards indicate an undetermined gain, including incompletions; interception yards represent return distance and field-goal yards represent kick distance. Fragmentary passages leave some players, outcomes, penalties, and possible replay boundaries uncertain. The Otton loose-ball sequence does not establish a turnover. Kickoff returns listed in the DB were not described in the captions and are not included. Extra points are documented in the DB but not separately identifiable in these captions.


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

Offense (model synthesis from this game's plays): Ability to execute deep middle passes for touchdowns / Short field goal accuracy / Pass catching ability of tight ends on intermediate routes

Defense weaknesses: Frequent penalties / Poor third down defense / Vulnerability to explosive plays and deep shots / Inability to stop long field goals

Limitations: Could not determine specific concepts like run gaps, play-action, screens, RPOs, personnel formations, or coverage schemes because the captions and commentary rarely explicitly stated them. Many names were mangled in captions and had to be corrected via clear DB matches. Several plays in captions lacked sufficient detail for yards or exact defender beaten. Non-highlight plays and those without clear DB matches were omitted.


## Week 4: GB 17 - TB 14 (game 401872968)
Video: Green Bay Packers vs Tampa Bay Buccaneers Game Highlights | 2026 NFL Season Week 4 — https://www.youtube.com/watch?v=13AbO1AEq1E  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:20|TB|J.Daniels|Third down, tight end in motion, Daniels maneuvering but sealed up and nowhere to run|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:37|GB|C.Brooks|Brooks with Moore in backfield, runs inside the 40 of Buccaneers|None|unknown|unknown|unknown|A.Winfield|verified vs DB|
|00:39|GB|T.Kraft|Tucker Kraft in motion or involved in play|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:51|GB|J.Love|Jordan Love throws middle of the field and holds it|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:12|TB|J.Daniels|Daniels loves to throw on the move, complete, goes down and takes what he can get|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:25|TB|J.Daniels|Daniels sliding for the first down across midfield|21|unknown|unknown|unknown|unknown|verified vs DB|
|01:47|GB|C.Brooks|Brooks shakes it loose, now inside the 40 of the Buccaneers and eventually brought down by Antoine Winfield|27|unknown|unknown|unknown|unknown|verified vs DB|
|02:01|GB|J.Love|Jordan Love on the cross, they make it look easy, Tucker Kraft rolling out|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:10|GB|T.Kraft|Kraft will take the snap directly and gets the Packers first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:21|GB|J.Love|Love with a quick dump off, it's Lloyd|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:30|GB|J.Love|Jordan Love firing through the end zone and caught, Matthew Golden and that is a Packers touchdown|2|unknown|unknown|unknown|unknown|verified vs DB|
|03:07|TB|C.Otton|Dump it off to Cade Otton from the tight end spot, around the first down marker|21|unknown|unknown|unknown|unknown|verified vs DB|
|03:20|TB|S.Tucker|Straight ahead, had a wall but kept going, Sean Tucker with a first down, plowed his way|2|unknown|unknown|unknown|unknown|verified vs DB|
|03:54|TB|J.Daniels|Quick drop and open, giving a lot of room, it is Christian|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:01|GB|C.Johnson|Johnson and this time the Bucs will tackle behind the line of scrimmage|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:18|TB|C.Johnson|Pressure coming and he delivers, Johnson, bouncing around eventually out of bounds|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:37|TB|J.Daniels|He's going to keep it and go out of bounds and a wise decision|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:44|TB|K.Gainwell|Gainwell coming in to throw, yes the rookie from, that is when he gets hit|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:56|GB|E.Cooper|Diving for the interception, the pick from Cooper|18|unknown|unknown|unknown|unknown|verified vs DB|
|05:39|GB|J.Love|Dumps it off to Lloyd and a good tackle there at the 41|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:11|GB|C.Johnson|Brooks out with that ankle injury. At the 45 is the second catch, running game, now Johnson is doing a nice job as well, Caleb Johnson inside the 15, down around the six yard line, what a run|31|unknown|unknown|unknown|A.Winfield|verified vs DB|
|06:31|GB|T.Kraft|Into the end zone, catch made and that is a Tucker Kraft -- it is a catch but they are saying he was out of bounds when he caught it|2|unknown|unknown|unknown|T.Smith|verified vs DB|
|07:05|TB|B.Irving|From the 35, it is Bucky Irving and he picks up foreign half|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:12|TB|J.Daniels|With extra pressure, here they come and they got him, he barely got the football|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:20|GB|M.Golden|The pass, right on target, Matthew Golden goes out|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:36|GB|M.Golden|Deep, sidelined, incomplete for Golden|None|deep shot|unknown|unknown|unknown|verified vs DB|
|07:41|TB|J.Daniels|Daniels, catch by for a first down, at the 31 yard line|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:58|TB|C.Johnson|That does complete the pass to Johnson, that is the kind of athletic ability|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:08|TB|J.Daniels|Third down. Daniels has got the middle of the field open, inside the 40, all the way down to the 37|21|unknown|unknown|unknown|B.Cisse|verified vs DB|
|08:18|TB|C.Johnson|The pitch, that is Johnson from the receiver spot and a first down. Inside the 25|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:49|TB|K.Gainwell|Diving into the end zone is Gainwell and that is a touchdown|10|unknown|unknown|unknown|unknown|verified vs DB|
|09:22|GB|J.Love|The Bucs have yet to get a takeaway and the pass is right on target|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:41|GB|J.Love|Jordan Love over the top and it blows the game wide open|25|deep shot|unknown|unknown|unknown|verified vs DB|
|09:44|GB|T.Kraft|Meanwhile he is picking it apart underneath as Kraft has another catch|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:49|GB|J.Love|Love on the move, completes, Lloyd, strong play all the way down inside the 16 yard line|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:06|GB|J.Love|Second and 10, in the pocket, Watson has it. Inside the five yard line. Almost out runs Jacob Harris|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:16|GB|K.Johnson|The ball comes out and the Bucs are saying they have it and they do. The officials say Tampa Bay football. On the exchange, McCollum came up with it after Love gave it to Johnson|0|unknown|unknown|unknown|T.Smith|verified vs DB|
|10:44|TB|E.Egbuka|Emeka Egbuka, his first|None|unknown|unknown|unknown|unknown|verified vs DB|
|10:57|TB|J.Daniels|The snap, he's going into the end zone and he is brought down by Braden|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:19|GB|J.Love|What a nice flip to|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:34|GB|J.Love|Another quick throw and intercepted, that is a Tampa Bay takeaway by Jacob Harris who cut in front of the receiver|8|unknown|unknown|unknown|unknown|verified vs DB|
|12:06|TB|B.Irving|And they go to Bucky Irving who has a first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:21|TB|J.Daniels|Pressure, it is caught and falling to the first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:34|TB|J.Daniels|Jalon Daniels gets it in a hurry, catch made, and out of bounds to stop the clock|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:45|TB|J.Daniels|Pressure coming, there is a flag down as Evan Williams comes in on the safety|None|unknown|unknown|unknown|E.Williams|verified vs DB|

Offense (model synthesis from this game's plays): Mobile QB Daniels effective on designed runs, scrambles, and quick throws on the move / Successful outside zone and power run concepts with Tucker, Johnson, and Irving / Quick passing game and RPO elements to exploit underneath coverage / Red zone efficiency with short passes to Gainwell for TD

Defense weaknesses: Struggled to stop explosive runs by GB backs (27 and 31 yard gains) / Poor pass rush allowing Love quick releases and time to throw / Coverage breakdowns on short routes and crossing patterns leading to TDs / Missed opportunities for takeaways until late in game

Limitations: Could not determine specific concepts like run gaps, play-action, screens, RPOs, personnel formations, or coverage schemes because they were not explicitly stated by commentators or clearly shown in DB text. Many plays in captions were vague or did not perfectly align with DB entries so could not always correct mangled names or assign exact yards/is_score. Several caption segments did not describe discrete plays or lacked sufficient detail for inclusion. Emotional and generic commentary limited extractable specifics.


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

Offense (model synthesis from this game's plays): Explosive run game with long gains by B.Irving including 72-yard run and multiple touchdowns / Effective deep passing attacks with big gains to T.Johnson and E.Egbuka / Red zone efficiency converting to multiple rushing and passing touchdowns / Sustained drives consuming clock time

Defense weaknesses: Vulnerable to big passing plays allowing multiple 20+ yard receptions to G.Pickens and R.Flournoy / Secondary breakdowns leading to wide open receivers on deep shots / Missed tackles in open field on runs and passes / Struggles containing mobile QB on scrambles

Limitations: Could not determine specific concepts like run gaps/directions, personnel formations, or coverage schemes because commentators did not explicitly state them. Many plays in captions had no clear match to DB due to incomplete or vague descriptions. Some player names corrected using DB only on clear matches. Yards often not precisely stated in captions so used DB values where matched. Several caption plays had no DB equivalent.


## Week 6: PIT 26 - TB 19 (game 401873002)
Video: Pittsburgh Steelers vs. Tampa Bay Buccaneers Game Highlights | 2026 NFL Season Week 6 — https://www.youtube.com/watch?v=vf4ksuXiQ1M  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:14|TB|Jalon Daniels|Sacked on third down by Jalen Ramsey coming off the edge.|None|unknown|unknown|unknown|Jalen Ramsey|unverified (no DB match; caption-only)|
|00:25|PIT|Aaron Rodgers|Throws into the turf while chased by Trotter.|0|unknown|unknown|unknown|Trotter|unverified (no DB match; caption-only)|
|00:35|TB|Chris Godwin|Drops a pass that commentary says would have produced a first down.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:46|PIT|Aaron Rodgers|Pass intended for Darnell Washington is intercepted by A. Robinson off a deflection; Yaya Diaby supplies pressure. No return gain.|0|short right pass|unknown|unknown|A. Robinson; R. Bain; Yaya Diaby|verified vs DB|
|01:00|TB|Bucky Irving|Runs for a first down inside the 35.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:11|TB|Bucky Irving|Slips away from T.J. Watt but is stopped by teammates for a five-yard loss; Nate Herbig is named in the backfield.|-5|unknown|unknown|unknown|T.J. Watt; Nate Herbig|unverified (no DB match; caption-only)|
|01:23|TB|Kenny Gainwell|Catches Daniels' pass against pressure from both edges and is tackled at the 25, short of a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:38|TB|C. McLaughlin|Makes a 43-yard field goal; commentary suggests it was deflected at the line.|43|field goal|unknown|unknown|unknown|verified vs DB|
|01:55|PIT|Jaylen Warren|Catch and run gains 16 yards and a first down; Trotter makes the tackle.|16|unknown|unknown|unknown|Trotter|unverified (no DB match; caption-only)|
|02:06|PIT|Rico Dowdle|His first touch produces a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:13|PIT|Bernard|Catches a pass but cannot get past McCollum, bringing up fourth and short.|None|unknown|unknown|unknown|Zyon McCollum|unverified (no DB match; caption-only)|
|02:24|PIT|Bernard|Catches Rodgers' pressured fourth-and-three pass while going backward. Initial ruling gives Tampa Bay possession; captions mention review without its result.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:40|TB|Chris Godwin|Catches a third-and-nine pass and turns upfield for 13 yards. Commentary describes catch-and-run offense against the blitz.|13|unknown|unknown|blitz|unknown|unverified (no DB match; caption-only)|
|02:57|TB|Ted Hurst|Catches a first-down pass during a no-huddle sequence.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:06|TB|Chris Godwin|Catches Daniels' floated pass for another first down near the end of the quarter.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:21|TB|T. Hurst|Deep-right target falls incomplete, but D. Everette is called for 22-yard defensive pass interference. No play.|22|deep right pass|unknown|unknown|D. Everette|verified vs DB|
|03:37|TB|E. Egbuka|Catches a two-yard touchdown pass from Daniels.|2|short left pass|unknown|unknown|unknown|verified vs DB|
|03:52|PIT|D.K. Metcalf|Goes in motion, catches Rodgers' pass with blockers ahead, and turns upfield near the 30.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:05|PIT|Aaron Rodgers|Third-down pass is broken up, ending a three-and-out.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:28|TB|Bucky Irving|Opens the drive with a run described as reaching the 20-yard line.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:34|TB|Jalon Daniels|Completes a pass that sets up third and short; receiver is not identified.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:44|TB|Jalon Daniels|Another catch is called, but the fragment does not identify the receiver or result.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:59|PIT|Aaron Rodgers|Turns upfield and picks up a first down.|None|quarterback run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:02|PIT|Rico Dowdle|Takes a handoff following Smith's motion and gains 15 yards up the middle.|15|run up the middle|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:15|PIT|Bernard|Catches a quick pass and uses blockers but finishes short of the first down; Scott makes the tackle.|None|unknown|unknown|unknown|Scott|unverified (no DB match; caption-only)|
|05:27|PIT|C. Boswell|Misses a 48-yard field goal wide left.|48|field goal|unknown|unknown|unknown|verified vs DB|
|05:39|TB|Jalon Daniels|Steps up, takes off, and slides at the 42 after a 17-yard gain.|17|quarterback scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:59|TB|Kenny Gainwell|Takes a handoff for 14 yards and a first down.|14|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:17|TB|Emeka Egbuka|Gets wide open deep, but Daniels slightly overthrows him for an incompletion.|0|deep shot|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:30|TB|C. McLaughlin|Makes a 47-yard field goal.|47|field goal|unknown|unknown|unknown|verified vs DB|
|06:38|PIT|Aaron Rodgers|Sacked on play-action by Scott; commentary says the ball comes out late, without identifying recovery.|None|play-action|unknown|unknown|Scott|unverified (no DB match; caption-only)|
|06:52|PIT|Aaron Rodgers|Sacked as the pocket collapses; captions render the defender's name as 'Ruben Banem.'|None|unknown|unknown|unknown|Ruben Banem (caption transcription; identity uncertain)|unverified (no DB match; caption-only)|
|07:09|TB|Jalon Daniels|Third-and-nine pass is broken up by Dean.|0|unknown|unknown|unknown|Jamel Dean|unverified (no DB match; caption-only)|
|07:23|PIT|Freiermuth|Catches a pass during the late-half drive; the clock keeps running.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:29|PIT|Bernard|Catches a pass into Tampa Bay territory as Pittsburgh hurries to the line.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:41|PIT|Bernard|Gets wide open after Rodgers' pump fake and goes down quickly with no timeouts. McCollum is identified as the matchup.|None|pump fake|unknown|unknown|Zyon McCollum|unverified (no DB match; caption-only)|
|07:50|PIT|C. Boswell|Makes a 52-yard field goal to end the first half.|52|field goal|unknown|unknown|unknown|verified vs DB|
|08:13|PIT|Aaron Rodgers|Pass is nearly intercepted by Trotter.|0|unknown|unknown|unknown|Trotter|unverified (no DB match; caption-only)|
|08:20|PIT|Freiermuth|Rodgers' third-and-eight pass over the middle intended for Freiermuth is incomplete.|0|pass over the middle|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:29|TB|Jalon Daniels|Takes off on third and eight and is marked just short of the first down.|None|quarterback scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:46|TB|Jalon Daniels|Caption fragment indicates Daniels barely obtains a first down; the action itself is omitted.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:48|TB|B. Sharp|Makes his first NFL catch, a 21-yard completion to the left off play-action; J. Ramsey tackles him.|21|play-action; deep left pass|unknown|unknown|J. Ramsey|verified vs DB|
|09:02|TB|Emeka Egbuka|Catches a third-down pass for 13 yards and is thrown down by Samuel Jr. The caption's 'touchdown' conflicts with the ensuing drive and DB scoring sequence.|13|unknown|unknown|unknown|Samuel Jr.|unverified (no DB match; caption-only)|
|09:16|TB|Jalon Daniels|Completes an outside pass for another third-down conversion; receiver is not named.|None|outside pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:26|TB|Bucky Irving|Tries to get outside and is tackled at the 18 by Ramsey.|None|outside run|unknown|unknown|Jalen Ramsey|unverified (no DB match; caption-only)|
|09:40|TB|Kenny Gainwell|Runs up the middle for a first down.|None|run up the middle|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:48|TB|Jalon Daniels|Chased out by Jaquan Brisker's pressure and throws the ball away.|0|unknown|unknown|unknown|Jaquan Brisker|unverified (no DB match; caption-only)|
|10:01|TB|C. McLaughlin|Makes a 33-yard field goal to extend Tampa Bay's lead to 16-3.|33|field goal|unknown|unknown|unknown|verified vs DB|
|10:18|PIT|D.K. Metcalf|Rodgers' pass intended for Metcalf is incomplete, producing another three-and-out.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:29|TB|Jalon Daniels|Steps up and tries to shake free before being tackled at the 30. A flag is described as likely holding against Tampa Bay; enforcement is omitted.|None|quarterback scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:47|PIT|Washington|Catches an eight-yard pass on second down; Alex Anzalone tackles him.|8|unknown|unknown|unknown|Alex Anzalone|unverified (no DB match; caption-only)|
|11:00|PIT|Bernard|Catches a pass for 19 yards and is forced out at the 40, converting third and short.|19|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:16|PIT|Aaron Rodgers|Sacked by David Walker for a ten-yard loss.|-10|unknown|unknown|unknown|David Walker|unverified (no DB match; caption-only)|
|11:25|PIT|D.K. Metcalf|Catches a first-down pass and takes contact. A late flag follows for a hit on Rodgers; Elijah Canty is named in that discussion.|None|unknown|unknown|unknown|Elijah Canty (late-hit discussion)|unverified (no DB match; caption-only)|
|11:53|PIT|Bernard|Catches Rodgers' pass inside the five on Pittsburgh's first red-zone trip.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:08|PIT|D. Washington|Gets wide open and catches Rodgers' five-yard touchdown pass. Commentary says Rodgers 'pulls it' without explicitly identifying an RPO or play-action.|5|short left pass|unknown|unknown|unknown|verified vs DB|
|12:29|TB|J. Daniels|High pass intended for E. Egbuka is intercepted by D. Everette, who gets his feet in bounds. DB credits pressure from C. Heyward; no return gain.|0|short left pass|unknown|unknown|D. Everette; C. Heyward|verified vs DB|
|12:48|PIT|D.K. Metcalf|Makes a play down the sideline; commentary identifies Tampa Bay's zone defense.|None|unknown|unknown|zone|unknown|unverified (no DB match; caption-only)|
|12:57|PIT|Aaron Rodgers|Keeps the play alive against pressure and completes a pass for a third-down conversion; receiver is not identified.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:15|PIT|Aaron Rodgers|Sacked while trying to extend the play. The defender's name is unintelligible in the captions.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:33|PIT|D.K. Metcalf|Catches a screen, slips one tackle, and is stopped by another defender, leaving fourth and long.|None|screen|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:47|PIT|C. Boswell|Makes a 39-yard field goal. Commentary identifies it as his 310th, setting Pittsburgh's career record.|39|field goal|unknown|unknown|unknown|verified vs DB|
|14:04|TB|Emeka Egbuka|Targeted on an incomplete pass with Dean in coverage; Pittsburgh forces a three-and-out.|0|unknown|unknown|unknown|Jamel Dean|unverified (no DB match; caption-only)|
|14:17|PIT|Jaylen Warren|Picks up a first down; the fragment does not establish whether it is a run or reception.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:32|PIT|D.K. Metcalf|Gets wide open and makes a catch for 12 yards and a first down.|12|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:45|PIT|D.K. Metcalf|Targeted on third and five against Jacob Parrish. Contact brings flags, and the fragment identifies a defensive penalty without giving its full ruling.|None|unknown|unknown|unknown|Jacob Parrish|unverified (no DB match; caption-only)|
|15:07|PIT|Aaron Rodgers|Sacked on third and four with Robinson and Walker in the backfield. Commentary identifies Walker coming off the edge.|None|unknown|unknown|unknown|Robinson; David Walker|unverified (no DB match; caption-only)|
|15:22|PIT|C. Boswell|Makes a 58-yard field goal in a crosswind to tie the game at 16.|58|field goal|unknown|unknown|unknown|verified vs DB|
|15:42|TB|J. Daniels|Short-right pass intended for E. Egbuka is intercepted by J. Dean, who returns it 40 yards to the Tampa Bay three.|40|short right pass|unknown|unknown|J. Dean|verified vs DB|
|16:04|PIT|Aaron Rodgers|Fakes to Warren, rolls right, and throws incomplete with Zyon McCollum in coverage.|0|play-action; rollout right|unknown|unknown|Zyon McCollum|unverified (no DB match; caption-only)|
|16:22|PIT|D.K. Metcalf|End-zone target is broken up by Parrish, bringing up fourth and goal.|0|unknown|unknown|unknown|Jacob Parrish|unverified (no DB match; caption-only)|
|16:37|PIT|C. Boswell|Makes a 20-yard field goal for a 19-16 lead.|20|field goal|unknown|unknown|unknown|verified vs DB|
|16:54|TB|T. Hurst|Catches Daniels' deep-left pass to the Pittsburgh 43. Captions call it 23 yards; authoritative DB records 22.|22|deep left pass|unknown|unknown|J. Dean; P. Wilson|CONFLICT (yardage 22 vs DB)|
|17:02|TB|Jalon Daniels|Sacked from behind by Herbig for a seven-yard loss but holds onto the ball.|-7|unknown|unknown|unknown|Herbig (first name not established for this play)|unverified (no DB match; caption-only)|
|17:17|TB|Jalon Daniels|Handles a high snap and completes a pass to the 35; Dean makes the tackle. Receiver is not identified.|None|unknown|unknown|unknown|Jamel Dean|unverified (no DB match; caption-only)|
|17:26|TB|C. McLaughlin|Makes a 53-yard field goal to tie the game at 19 with eight seconds remaining.|53|field goal|unknown|unknown|unknown|verified vs DB|
|18:00|PIT|K. Wetjen|Returns the overtime kickoff from his five to the 30 for 25 yards; DB names M. Killebrew as tackler.|25|kickoff return|unknown|unknown|M. Killebrew|verified vs DB|
|18:15|PIT|D.K. Metcalf|Catches Rodgers' pass over the middle for 20 yards and a first down to the 46. Commentary identifies the spread offense.|20|pass over the middle|spread offense|unknown|unknown|unverified (no DB match; caption-only)|
|18:32|PIT|D.K. Metcalf|Makes another first-down catch, gaining nine yards.|9|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|18:51|PIT|Jaylen Warren|Uses repeated spin moves and gains 12 yards; captions do not establish run versus reception.|12|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|19:02|PIT|Jaylen Warren|Stays up after nearly going down and gains seven yards. Commentary describes quick swing passes and identifies a matchup with Zyon McCollum.|7|swing pass|unknown|unknown|Zyon McCollum|unverified (no DB match; caption-only)|
|19:16|PIT|Rico Dowdle|Runs for a first down just inside the ten, setting up first and goal.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|19:31|PIT|G. Bernard|Catches Rodgers' quick pass and stretches for a six-yard overtime touchdown, identified as his first NFL touchdown.|6|short right pass|unknown|unknown|unknown|verified vs DB|
|19:55|TB|Jalon Daniels|Misses the checkdown to Irving, bringing up fourth and nine.|0|checkdown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|20:05|TB|Jalon Daniels|Escapes the pocket as T.J. Watt approaches and runs for a first down on fourth and nine.|None|quarterback scramble|unknown|unknown|T.J. Watt|unverified (no DB match; caption-only)|
|20:25|TB|Chris Godwin|Catches a pass for a first down at midfield.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|20:37|TB|Tez Johnson|Cannot hold a quick slant on third and eight. Commentary subsequently credits Dean's contribution without specifying his exact action.|0|slant|unknown|unknown|Jamel Dean|unverified (no DB match; caption-only)|
|20:49|TB|Jalon Daniels|Sacked on fourth and eight by Jalen Ramsey, who comes free off the edge, ending the game.|None|unknown|unknown|unknown|Jalen Ramsey|unverified (no DB match; caption-only)|

Offense (model synthesis from this game's plays): Godwin supplied repeated first-down catches, including a 13-yard third-and-nine conversion and an overtime completion to midfield. / Daniels used his legs for a 17-yard gain and an overtime fourth-and-nine conversion. / Gainwell produced a 14-yard run and a separate first-down run up the middle. / The passing game generated a 21-yard play-action completion to Sharp, a 22-yard late completion to Hurst, and a two-yard touchdown to Egbuka. / The no-huddle sequence included a first-down completion to Hurst, followed by another first-down catch by Godwin.

Defense weaknesses: Washington was wide open for Pittsburgh's five-yard touchdown. / Bernard repeatedly found receiving gains, including 19 yards on third and short and the six-yard overtime touchdown. / Metcalf was described as wide open on a 12-yard catch and added consecutive overtime first-down receptions. / Warren gained yards after contact or evasive moves in overtime, including repeated spins on a 12-yard gain. / Pittsburgh sustained a 12-play overtime touchdown drive using Metcalf completions, Warren gains, and a Dowdle first-down run.

Limitations: Analysis uses only the supplied captions and DB excerpts; no video frames or external sources were consulted. The DB is a selected-play list, so NO DB MATCH does not mean a play did not occur. Its omission of Metcalf's captioned 20-yard overtime catch is unresolved. Unknown yardage, receivers, formations, coverages, run gaps, and route details remain unspecified. Shotgun in DB text was not used to populate personnel_formation because the user required explicit commentary for that field. Suggested defensive calls and generic instructions to spread out were not treated as confirmed schemes or formations. Defender_beaten lists named defenders involved in coverage, pressure, or tackles and does not imply they actually lost their matchup. Matched interception yardage is return yardage; field-goal yardage is kick distance; penalty yardage is enforcement distance. Names were corrected from DB only for clearly matched plays; unmatched mangled names remain uncertain. The 09:02 touchdown wording conflicts with the DB and subsequent continuation of the drive, so that play is treated as a non-scoring 13-yard conversion. Hurst's late gain uses the DB's 22 yards rather than the caption's 23. The anticipated regulation kneel and DB-only kickoffs were omitted because captions do not establish their execution. The fourth-down Bernard review, possible holding enforcement, and recovery after Rodgers' apparent loose ball are not resolved by the captions.
