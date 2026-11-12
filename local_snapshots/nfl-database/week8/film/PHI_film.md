# PHI — Phase 8 film notes (Weeks 1–6, 2026)
> Note: games 401872944, 401872945, 401872952, 401872962, 401872964, 401872970, 401872985, 401872989 were extracted by a Grok Bot agent (not Codex) from the same captions; mostly scoring/20+ plays logged.
> Note: games 401872963, 401872981 were extracted by Grok via the xAI API (grok-4.20-0309-non-reasoning, same prompt/schema as Codex, cleaned captions); sidecar provenance in film/grok_meta/. All other games with notes: Codex.

Method: NFL YouTube channel full-game highlight videos were located by search and their auto-captions (broadcast commentary) downloaded via yt-dlp. Codex (codex-cli 0.163.0) extracted plays from the captions. **No video frames were viewed by any agent.** Each play was checked against the repo DB play-by-play: `verified vs DB` means the cited DB play exists and the yardage matches. Personnel, formation and coverage appear only when commentators stated them; everything else is `unknown`.


## Week 1: WSH 22 - PHI 24 (game 401872929)
Video: Washington Commanders vs Philadelphia Eagles Game Highlights | 2026 NFL Week 1 — https://www.youtube.com/watch?v=UYunnfDMXGc  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:19|WSH|Rachaad White|Runs up the middle and is hit immediately; commentary estimates a yard and a half.|None|run up the middle|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:28|WSH|Drew Stevens|Makes a 55-yard field goal.|55|field goal|unknown|unknown|unknown|verified vs DB|
|00:38|PHI|Saquon Barkley|Finds a seam for five yards.|5|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:46|PHI|Jalen Hurts|Escapes a blitz and runs for a first down.|None|scramble|shotgun|blitz|unknown|unverified (no DB match; caption-only)|
|01:01|PHI|Saquon Barkley|Run is stopped by Odafe Oweh.|None|unknown|unknown|unknown|Odafe Oweh (credited with stop)|unverified (no DB match; caption-only)|
|01:11|PHI|unknown|Third-and-eight pass falls incomplete after a big hit by Douglas; Philadelphia must punt.|None|unknown|unknown|unknown|Douglas (credited with hit)|unverified (no DB match; caption-only)|
|01:28|WSH|Jayden Daniels|Deep pass is incomplete with Warren providing stride-for-stride coverage.|None|deep shot|unknown|four-man rush; coverage unknown|Warren (credited with coverage)|unverified (no DB match; caption-only)|
|01:45|PHI|Jalen Hurts|Nick Cross delivers a tackle for a four-yard loss; the captions do not establish the play type.|-4|unknown|unknown|unknown|Nick Cross (credited with tackle)|unverified (no DB match; caption-only)|
|02:00|PHI|DeVonta Smith|Catches Hurts' pass over the middle and reaches the 35.|None|pass over the middle|unknown|four-man rush; coverage unknown|unknown|unverified (no DB match; caption-only)|
|02:06|PHI|Jalen Hurts|Frankie Luvu records Washington's first sack.|None|unknown|unknown|unknown|Frankie Luvu (credited with sack)|unverified (no DB match; caption-only)|
|02:18|WSH|John Bates|Catches a screen after a play fake and finishes just short of the first down.|None|play-action screen|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:31|WSH|Rachaad White|Stuffed on third-and-one by Jalen Carter and the defensive front.|None|unknown|jumbo|unknown|Jalen Carter (credited with stop)|unverified (no DB match; caption-only)|
|02:47|PHI|Dontayvion Wicks|Catches a deep play-action pass for 64 yards to the Washington 6. Later commentary identifies Sainristil as having been in coverage.|64|play-action deep right|three tight ends|unknown|Sainristil (coverage, retrospective commentary); Jeremy Reaves (DB tackler)|verified vs DB|
|03:02|PHI|Saquon Barkley|Wrapped up in the backfield by Javon Kinlaw.|None|unknown|unknown|unknown|Javon Kinlaw (credited with tackle)|unverified (no DB match; caption-only)|
|03:14|PHI|Dallas Goedert|Scores on a 17-yard reception. Replay commentary says Reaves loses Goedert while Washington disguises pressure and the safety cannot overlap.|17|seam pass; deep right in DB|unknown|disguised pressure; coverage unknown|Jeremy Reaves|verified vs DB|
|03:40|WSH|Chig Okonkwo|Catches an outside throw for a short gain with Quinyon Mitchell immediately on him.|None|outside pass|unknown|unknown|Quinyon Mitchell (credited with coverage/stop)|unverified (no DB match; caption-only)|
|03:52|WSH|Jayden Daniels|Throws incomplete under pressure to Diggs, who had leaked out.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:09|PHI|Saquon Barkley|Runs across the 30 for four yards.|4|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:24|WSH|Jacory Croskey-Merritt|Hit by Zack Baun on a rushing play.|None|unknown|unknown|unknown|Zack Baun (credited with hit)|unverified (no DB match; caption-only)|
|04:33|WSH|Rachaad White|Takes a handoff before Washington punts.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:47|PHI|Saquon Barkley|Runs for eight yards.|8|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:53|PHI|Saquon Barkley|Breaks a tackle on third-and-two and cuts back inside the 15 for 42 yards.|42|right guard run with cutback|unknown|unknown|Jeremy Reaves; Nick Cross (DB tacklers; broken-tackle defender unidentified)|verified vs DB|
|05:14|PHI|Dontayvion Wicks|Catches a nine-yard touchdown at the back pylon while Hurts faces pressure from Luvu. Wicks motions across and separates from Sainristil at the top of his route.|9|motion; throw to back pylon|unknown|man-to-man; middle blitz|Sainristil|verified vs DB|
|05:48|WSH|Jacory Croskey-Merritt|Runs for a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:58|WSH|Stefon Diggs|Makes an underneath reception for a first down.|None|underneath pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:07|WSH|Jayden Daniels|Runs against a blitz with Baun pursuing and finishes just short of the first down.|None|scramble|unknown|blitz|Zack Baun (pursuit)|unverified (no DB match; caption-only)|
|06:17|WSH|Jacory Croskey-Merritt|Converts fourth-and-one with a run up the middle.|None|run up the middle|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:27|WSH|Jacory Croskey-Merritt|Takes another handoff, makes a move and breaks tackles inside the 20.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:37|WSH|Antonio Williams|Catches a pass over the middle and is ruled down at the 1.|None|pass over the middle|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:49|WSH|Jacory Croskey-Merritt|Scores from one yard despite immediate contact. Commentary credits Ojomo with penetration and says the runner never went down.|1|left guard run|unknown|unknown|Moro Ojomo (penetration)|verified vs DB|
|07:25|WSH|Drew Stevens|Extra-point attempt is blocked by Jalen Carter according to the DB.|None|extra-point attempt|unknown|unknown|Jalen Carter (blocked kick)|verified vs DB|
|07:31|PHI|Will Shipley|Catches Hurts' pass under pressure and gets out of bounds.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:38|PHI|Jalen Hurts|Pass is knocked down at the line by a defender captioned as 'Charles Amenu.'|None|pass over the middle|unknown|unknown|Charles Amenu (caption rendering; pass deflection)|unverified (no DB match; caption-only)|
|07:49|PHI|Braden Mann|Punts deep over the returner's head; the ball finishes inside the 5.|None|punt|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:11|PHI|Lemon|Makes a catch and is hit immediately by Quan Martin, leaving third-and-long.|None|unknown|unknown|unknown|Quan Martin (credited with hit)|unverified (no DB match; caption-only)|
|08:19|PHI|Dallas Goedert|Catches a pass on third-and-14 but Nick Cross stops him short of the first down.|None|unknown|unknown|blitz|Nick Cross (credited with stop)|unverified (no DB match; caption-only)|
|08:34|WSH|Jacory Croskey-Merritt|Runs for four yards to the 45.|4|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:42|WSH|Rachaad White|Catches an underneath pass on third-and-six, makes a cut and is stopped well short by Baun.|None|underneath pass|unknown|four-man rush; coverage unknown|Zack Baun (credited with stop)|unverified (no DB match; caption-only)|
|08:58|PHI|Jalen Hurts|Sacked by Sonny Styles despite Barkley picking up a blitz.|None|unknown|unknown|blitz|Sonny Styles (credited with sack)|unverified (no DB match; caption-only)|
|09:05|PHI|Jalen Hurts|Underthrows Smith near the far sideline on third-and-six; Washington forces another three-and-out.|None|sideline pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:23|WSH|Chig Okonkwo|Catches a pass over the middle for a first down.|None|pass over the middle|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:36|WSH|Stefon Diggs|Commentary retrospectively reports his second drop; the actual play is omitted.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:37|WSH|Jayden Daniels|Throws incomplete against a blitz after intended receiver Brown slips.|None|unknown|unknown|blitz|unknown|unverified (no DB match; caption-only)|
|09:45|WSH|Drew Stevens|Misses a 54-yard field goal wide right.|54|field goal|unknown|unknown|unknown|verified vs DB|
|10:03|PHI|Saquon Barkley|Dropped behind the line by Sonny Styles.|None|unknown|unknown|unknown|Sonny Styles (credited with tackle)|unverified (no DB match; caption-only)|
|10:16|PHI|Jalen Hurts|Sacked on third-and-long. Commentary tentatively credits Oweh and a second defender rendered as 'Ameneh'; the referee announces no foul.|None|unknown|unknown|unknown|Odafe Oweh; Ameneh (caption rendering; tentative sack credit)|unverified (no DB match; caption-only)|
|10:33|WSH|Jaylin Lane|Catches a third-down pass but Cooper DeJean stops him well short.|None|unknown|unknown|unknown|Cooper DeJean (credited with stop)|unverified (no DB match; caption-only)|
|10:47|PHI|Jalen Hurts|Escapes near-sack pressure with a spin and runs 14 yards to the 44.|14|scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:03|PHI|DeVonta Smith|Makes a toe-tap sideline catch on third-and-five for 31 yards to the Washington 24.|31|deep right pass|unknown|blitz|Rasul Douglas (DB tackler)|verified vs DB|
|11:29|PHI|Jalen Hurts|Misses an open Goedert on third-and-short after the blitz is picked up.|None|unknown|unknown|blitz|unknown|unverified (no DB match; caption-only)|
|11:43|PHI|Jake Elliott|Makes a 35-yard field goal.|35|field goal|unknown|unknown|unknown|verified vs DB|
|11:50|WSH|Jayden Daniels|Spins away from Jihaad Campbell and makes another move on a scramble estimated at 11 or 12 yards.|None|scramble|unknown|four-man rush with an additional rusher|Jihaad Campbell|unverified (no DB match; caption-only)|
|12:24|WSH|John Bates|Receives a quick throw from Daniels.|None|quick pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:29|WSH|Jacory Croskey-Merritt|Runs patiently for a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:39|WSH|Antonio Williams|Gets behind the zone on third-and-long and catches a 33-yard pass to the Philadelphia 14.|33|deep left pass|unknown|zone|Jihaad Campbell (DB tackler)|verified vs DB|
|12:57|WSH|Rachaad White|Catches a screen, breaks a tackle and encounters Campbell.|None|screen|unknown|unknown|Jihaad Campbell (pursuit/stop; broken-tackle defender unidentified)|unverified (no DB match; caption-only)|
|13:10|WSH|Stefon Diggs|Separates from DeJean with a shoulder shimmy and catches a 10-yard touchdown underneath against a blitz. Penalized afterward for jumping on the goalpost.|10|short middle pass|unknown|blitz; commentary describes a voided zone|Cooper DeJean|verified vs DB|
|13:46|PHI|Saquon Barkley|Tackled by Nick Cross on a run.|None|unknown|unknown|unknown|Nick Cross (credited with tackle)|unverified (no DB match; caption-only)|
|13:57|PHI|Jalen Hurts|With nobody available downfield, scrambles up the middle for 22 yards and a third-and-long conversion.|22|scramble up the middle|unknown|unknown|Amik Robertson (DB tackler)|verified vs DB|
|14:19|PHI|Dallas Goedert|Turns a short middle reception into a 43-yard touchdown. Commentary describes edge communication problems, Goedert slipping behind Styles and Cross missing the tackle.|43|short middle pass with run after catch|unknown|disguised pressure; coverage unknown|Sonny Styles; Nick Cross|verified vs DB|
|14:53|WSH|Antonio Williams|Catches a pass under pressure for a first down, identified as his third reception.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:01|WSH|Stefon Diggs|Gets wide open after a late blitz is picked up, catches the pass and turns upfield to the 30.|None|unknown|unknown|late blitz|unknown|unverified (no DB match; caption-only)|
|15:16|WSH|Terry McLaurin|Makes his first catch and looks for blocks; commentary estimates eight yards.|8|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:28|WSH|Jayden Daniels|Third-and-two pass is tipped incomplete by Zack Baun.|None|unknown|unknown|unknown|Zack Baun (pass deflection)|unverified (no DB match; caption-only)|
|15:41|WSH|Terry McLaurin|Catches an underneath pass to convert fourth-and-short.|None|underneath pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:50|WSH|Antonio Williams|Catches a one-yard touchdown. The completion is reviewed and upheld in the DB.|1|short right pass|four wide receivers|unknown|unknown|verified vs DB|
|17:07|WSH|John Bates|Catches an inside shovel pass on the two-point attempt but is stopped. Ojomo defeats a block to make the decisive play.|None|inside shovel pass|unknown|unknown|Moro Ojomo (credited with stop)|verified vs DB|
|17:39|PHI|unknown|Commentary identifies the final kneel-down that ends the game.|None|kneel-down|unknown|unknown|unknown|unverified (no DB match; caption-only)|

Offense (model synthesis from this game's plays): Three-tight-end play-action produced Wicks' 64-yard reception. / Wicks separated after motion for a touchdown against man coverage and a middle blitz. / Goedert exploited Washington's communication failures for touchdowns of 17 and 43 yards. / Hurts' scrambling generated first downs, including gains of 14 and 22 yards. / Barkley's 42-yard run and Smith's 31-yard reception supplied additional explosive gains.

Defense weaknesses: Williams got behind zone coverage for a 33-yard third-down conversion. / Diggs separated from DeJean for a 10-yard touchdown and later caught a wide-open pass after a late blitz was picked up. / Daniels escaped Campbell with a spin during a productive scramble. / Allowed Croskey-Merritt to convert fourth-and-one and score despite backfield penetration. / Allowed Washington to convert a late fourth-and-short through McLaurin and finish with Williams' touchdown from a four-wide formation.

Limitations: Captions only; no video frames were available. Exact routes, blocking assignments, personnel and coverages cannot be established beyond explicit commentary; DB-only shotgun labels were therefore not used as personnel_formation. Four-man rush and blitz descriptions do not establish coverage behind them. The supplied DB is selective, so NO DB MATCH means no match in that excerpt. DB clocks are copied as supplied despite sequencing anomalies. Field positions were not converted into inferred gains; null marks unavailable, ambiguous or non-integer yardage. McLaurin's eight-yard gain is a commentary estimate. Some unmatched names remain as captioned because the DB cannot verify them. defender_beaten includes identified tacklers and successful defenders with their roles stated; their inclusion does not imply they were beaten. Extra points and the two-point attempt share their associated touchdown's DB clock. Kickoff returns listed only in the DB were not treated as caption highlights. Diggs' drops are mentioned retrospectively without enough information to separate both plays. No turnover is identifiable in these captions.


## Week 2: PHI 24 - TEN 20 (game 401872939)
Video: Philadelphia Eagles vs Tennessee Titans Game Highlights | 2026 NFL Season Week 2 — https://www.youtube.com/watch?v=qQFyOm6nFaE  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:17|PHI|D.Wicks|Hurts floats a completion into Tennessee territory. DB records 27 yards; commentary says 26.|27|deep middle pass|unknown|unknown|M.Robinson; A.Hooker (DB tacklers)|verified vs DB|
|00:33|PHI|Dallas Goedert|Catches a dump-off short of the sticks and takes a hit; defender's name is cut off after Cody.|None|dump-off|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:43|PHI|DeVonta Smith|Catches a slant for eight yards and a first down against an extra pass rusher.|8|slant|unknown|extra rusher; coverage unknown|unknown|unverified (no DB match; caption-only)|
|00:51|PHI|Wicks|Catches a pass for first-and-goal near the seven after a tempo snap.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:04|PHI|J.Hurts; A.Hooker (TEN interceptor)|Hurts' end-zone pass intended for D.Smith is intercepted by Hooker, who returns it to Philadelphia's 10.|92|short right pass|unknown|unknown|A.Hooker (interceptor); M.Lemon (DB return tackler)|verified vs DB|
|01:47|TEN|Cam Ward|Spins away from pressure and scrambles toward the end zone, going out at the one.|None|scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:59|TEN|C.Ward|Scores on a fourth-and-goal sneak with help from his tight ends.|1|quarterback sneak up the middle|unknown|unknown|unknown|verified vs DB|
|02:32|PHI|Bigsby|Catches a first-down dump-off in the flat.|None|dump-off to the flat|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:44|PHI|DeVonta Smith|Catches a middle-of-the-field pass for a first down at Tennessee's 40.|None|middle-of-the-field pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:52|PHI|Lemon|Holds onto a completion against five-man pressure for a first down at the 25.|None|unknown|unknown|five-man pressure; coverage unknown|unknown|unverified (no DB match; caption-only)|
|03:05|PHI|DeVonta Smith|Scoops up a low outside throw for nine yards.|9|outside pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:14|PHI|Tank Bigsby|Runs from the 11 through a middle hole and pushes inside the five; Cedric Gray is mentioned at contact.|None|run up the middle|unknown|unknown|Cedric Gray (mentioned at contact)|unverified (no DB match; caption-only)|
|03:31|PHI|T.Bigsby|Scores Philadelphia's first touchdown on a short middle run; commentary credits patience, power and blocking push.|2|run up the middle|unknown|unknown|unknown|verified vs DB|
|03:50|TEN|Tony Pollard|Runs behind multiple blockers for 13 yards into Philadelphia territory when Tennessee needs one.|13|run; direction unknown|two backs|unknown|unknown|unverified (no DB match; caption-only)|
|04:03|TEN|Cam Ward|Backpedals and gets rid of the ball with a flag thrown against Tennessee; penalty and pass result are unspecified.|None|intended deep shot|shotgun|unknown|unknown|unverified (no DB match; caption-only)|
|04:17|PHI|DeVonta Smith|Finds space for a sideline completion and a first down at the 46.|None|sideline pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:31|PHI|Jalen Hurts|Scrambles and slides about two yards short of the line to gain as Tennessee drops into coverage.|None|scramble|unknown|drops into coverage; specific scheme unknown|Cedric Gray (commentary identifies him at the stop)|unverified (no DB match; caption-only)|
|04:44|PHI|Wicks|Catches a pass for a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:59|PHI|Bigsby|Stumbles in the backfield and is stopped by Stackhouse.|None|run; direction unknown|unknown|unknown|Stackhouse (makes the stop)|unverified (no DB match; caption-only)|
|05:12|PHI|Dontayvion Wicks|Gets open for a third-and-long conversion after Hurts pumps and throws with Jeffery Simmons bearing down.|None|pump fake and pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:31|PHI|D.Smith|Catches a touchdown behind Amani Hooker after Hurts buys time. Commentary says the route structure occupies that side of the defense.|22|deep right pass; extended play|unknown|unknown|Amani Hooker|verified vs DB|
|06:13|TEN|E.Ayomanor|Catches Ward's throw for a first down and more on third-and-long; receiver and distance are established by the matching DB sequence.|28|short left pass|unknown|unknown|Z.Baun (DB tackler)|verified vs DB|
|06:23|TEN|T.Spears|Bustes through after a quick-release pass, completing Tennessee's second consecutive big gain.|27|short right pass|unknown|unknown|M.Epps; A.Mukuba (DB tacklers)|verified vs DB|
|06:40|TEN|Tony Pollard|Receives a conservative rushing call late in the half; the gain is not stated.|None|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:54|TEN|J.Slye|Makes a field goal to end the first half.|37|field goal|unknown|unknown|unknown|verified vs DB|
|07:00|PHI|Shipley|Catches a fluttering pass near the 40 after Hurts stays upright and is hit while throwing by Jeffery Simmons.|None|extended-play pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:28|PHI|Jalen Hurts|Sacked on third down by Jacob Martin.|None|unknown|unknown|unknown|Jacob Martin (sacker)|unverified (no DB match; caption-only)|
|07:39|TEN|Tate|Catches a throw and is tackled by Woolen. Commentary separately identifies DeJean covering Robinson.|None|unknown|unknown|man-to-man|Woolen (tackler); DeJean covering Robinson, not identified as Tate's defender|unverified (no DB match; caption-only)|
|07:58|PHI|DeVonta Smith|Comes down out of bounds on a deep attempt contested by Amani Hooker; incomplete.|0|deep shot|unknown|unknown|Amani Hooker (contesting defender)|unverified (no DB match; caption-only)|
|08:34|PHI|Jalen Hurts|Flushes left and throws the ball away as Tennessee collapses the pocket with four rushers.|0|throwaway|unknown|four-man rush; coverage unknown|unknown|unverified (no DB match; caption-only)|
|08:48|PHI|J.Elliott|Makes a long field goal.|58|field goal|unknown|unknown|unknown|verified vs DB|
|08:59|TEN|Robinson|Catches a first-down pass into the space vacated by Cooper DeJean's edge blitz.|None|pass into vacated blitz area|unknown|edge blitz; coverage unknown|Cooper DeJean (blitzer vacating the target area)|unverified (no DB match; caption-only)|
|09:09|TEN|C.Ridley|Catches a play-action deep shot to Philadelphia's 30.|25|play-action; deep right pass|unknown|unknown|T.Woolen (DB tackler)|verified vs DB|
|09:23|TEN|Calvin Ridley|Holds onto a quick slant in front of Quinyon Mitchell.|None|slant|unknown|unknown|Quinyon Mitchell|unverified (no DB match; caption-only)|
|09:35|TEN|Gunnar Helm|Catches Ward's pass against pressure and lowers his shoulder near the sticks, setting up third-and-short.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:46|TEN|C.Ward|Moves off a fake and dives for a touchdown. Commentary says Philadelphia initially covers the play-action.|1|play-action; scramble left end|unknown|unknown|unknown|verified vs DB|
|10:19|PHI|Mundt|Hurts steps up against pressure and throws to Mundt at the sideline; commentary says nothing is there but does not clearly establish the result.|None|sideline pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:36|TEN|Tony Pollard|Breaks a tackle before Quinyon Mitchell brings him down at the 39.|None|run; direction unknown|unknown|unknown|Quinyon Mitchell (final tackler); broken-tackle defender unknown|unverified (no DB match; caption-only)|
|10:45|TEN|Cam Ward; Tate (target)|Tennessee hurries to prevent substitutions; Ward throws incomplete to Tate while moving.|0|pass on the move|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:58|PHI|DeVonta Smith|Catches a pass just past the sticks for a first down at the 41.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:17|PHI|D.Cooper|Gains a first down after Philadelphia has been backed up by holding.|23|short middle pass|unknown|unknown|K.Winston (DB tackler)|verified vs DB|
|11:30|PHI|Lemon|Targeted on a screen that Harris stops; exact gain is unstated.|None|screen|unknown|four-man rush; coverage unknown|Harris (stops the screen)|unverified (no DB match; caption-only)|
|11:44|PHI|J.Hurts; M.Harris (TEN interceptor)|Hurts floats a pass toward D.Smith that Harris intercepts. Commentary credits Simmons with helping create the turnover; DB also names J.Simmons.|3|deep left pass|unknown|four-man rush; coverage unknown|M.Harris (interceptor); D.Smith (DB return tackler)|verified vs DB|
|12:08|TEN|Tony Pollard|Starts the post-interception possession with an eight-yard run.|8|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:15|TEN|E.Ayomanor|Catches a play-action deep pass, hurdles Marcus Epps and reaches inside Philadelphia's 25.|41|play-action; deep right pass|unknown|unknown|Marcus Epps (hurdled); J.Campbell (DB tackler)|verified vs DB|
|12:39|TEN|T.Spears|Breaks free past Epps for a long first-down run to Philadelphia's nine.|27|left-end run|unknown|unknown|Epps; J.Hunt (DB tackler)|verified vs DB|
|12:54|TEN|Cam Ward|Keeps the ball, but Philadelphia is not fooled; exact result is unstated.|None|quarterback keeper|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:01|TEN|Spears|Runs left and barely reaches inside the 15 after tripping over teammate Peter Skoronski. Commentary identifies the same formation and play as the earlier long third-down run, without naming the formation.|None|run left|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:15|TEN|J.Slye|Makes the go-ahead field goal.|33|field goal|unknown|unknown|unknown|verified vs DB|
|13:27|PHI|D.Wicks|Wins a downfield jump ball against Harris as Hurts delivers under Cody Barton pressure.|20|deep right pass; jump ball|unknown|unknown|Harris|verified vs DB|
|13:42|PHI|DeVonta Smith|Catches a nine-yard pass during the final touchdown drive.|9|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:54|PHI|DeVonta Smith|Catches another pass for first-and-goal; the clock stops with 14 seconds remaining.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:08|PHI|D.Cooper|Catches the winning touchdown at the back of the end zone after Hurts rolls right and buys time. Smith's out-and-in motion creates indecision among three defenders attempting to pass off man assignments.|3|rollout right; short middle pass; pre-snap motion|Smith motioned out and in; personnel grouping unknown|Cover Zero; man-to-man|unknown|verified vs DB|
|14:58|TEN|Tate|Catches Ward's pass down the middle; Tennessee calls timeout with four seconds left.|None|middle-of-the-field pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:07|TEN|Cam Ward|Throws a deflected incompletion against a Philadelphia blitz on the final play.|0|unknown|unknown|blitz; coverage unknown|unknown|unverified (no DB match; caption-only)|

Offense (model synthesis from this game's plays): Wicks supplied the opening 27-yard gain, multiple captioned first-down catches and a 20-yard contested catch on the winning drive. / Smith repeatedly converted through the air, including a slant, middle and sideline completions, a 22-yard touchdown and two late-drive catches. / Hurts buying time enabled Smith's touchdown behind Hooker and Cooper's winning touchdown against explicitly identified Cover Zero. / Bigsby's middle runs showed power and patience near the goal line and produced a two-yard touchdown. / Smith's motion created defensive assignment indecision on Cooper's winning touchdown.

Defense weaknesses: Allowed consecutive 28-yard Ayomanor and 27-yard Spears receptions before Tennessee's halftime field goal. / DeJean's edge blitz vacated space that Ward exploited with a first-down completion to Robinson. / Allowed play-action gains of 25 yards to Ridley and 41 yards to Ayomanor. / Epps was hurdled on Ayomanor's 41-yard catch and beaten on Spears' 27-yard run. / Ward escaped pressure near the goal line and later scored on a scramble after Philadelphia initially covered the play-action.

Limitations: Captions only; no routes, alignments, blocking assignments or coverage details were inferred from video. The supplied DB is a selected subset, so NO DB MATCH does not mean a play did not occur. Only caption-identifiable plays are listed; DB-only kickoffs, returns and other uncaptioned events are omitted. DB distances take precedence where clearly matched. For interceptions, yards denotes return distance; for field goals, kick distance. Null yards means the gain cannot be established. Named tacklers, interceptors and contesting defenders are labeled by role and are not necessarily defenders beaten. Unmatched names remain as captioned without speculative DB corrections. Pressure descriptions do not establish a coverage shell. The isolated swing-route fragment and retrospective references to earlier goal-line runs do not establish additional distinct plays.


## Week 3: PHI 7 - CHI 27 (game 401872963)
Video: Philadelphia Eagles vs. Chicago Bears Game Highlights | 2026 NFL Season Week 3 — https://www.youtube.com/watch?v=KScULet1ves  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:07|PHI|J.Elliott|Kickoff|63|unknown|unknown|unknown|unknown|verified vs DB|
|00:14|CHI|Z.Thomas|Kickoff return|32|unknown|unknown|unknown|K.Ringo; S.Mondon|verified vs DB|
|00:22|CHI|C.Keenum|Pass completion to Burden|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:26|CHI|L.Burden|Pass reception with missed tackle by Epps|None|unknown|unknown|unknown|M.Epps|unverified (no DB match; caption-only)|
|00:35|CHI|C.Keenum|Pass completion to K.Raymond|10|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:49|CHI|C.Keenum|Pass to Swift|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:13|CHI|C.Keenum|Pass completion to S.Roush for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:25|CHI|L.Burden|Handoff inside|7|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:36|CHI|L.Burden|Toss play, first down and into end zone|None|unknown|unknown|unknown|unknown|verified vs DB|
|01:51|PHI|J.Hurts|Play-action fake toss to Barkley, pass to M.Lemon|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:05|PHI|S.Barkley|Handoff left side for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:15|PHI|J.Hurts|Play-action, throws ball into ground|0|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:27|PHI|J.Hurts|Pass to J.Mundt|5|unknown|unknown|unknown|C.Lewis; D.Bush|unverified (no DB match; caption-only)|
|02:36|CHI|C.Keenum|Pass to D.Swift on third down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:00|CHI|R.Odunze|Incomplete pass|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:11|PHI|B.Covey|Punt return, lets ball go over head|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:31|PHI|T.Bigsby|Handoff, hit immediately, fumble|5|unknown|unknown|unknown|J.Johnson|verified vs DB|
|03:47|CHI|L.Burden|Pass reception|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:58|PHI|A.Dalton|Pass nearly intercepted by Mukuba|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:02|CHI|C.Lewis|Penalty on defense, illegal contact|None|unknown|unknown|unknown|unknown|verified vs DB|
|04:17|CHI|C.Keenum|Pass to C.Loveland for touchdown|None|unknown|unknown|unknown|unknown|verified vs DB|
|04:31|CHI|D.Swift|Run with Carter|None|unknown|pistol|unknown|unknown|unverified (no DB match; caption-only)|
|04:37|CHI|C.Keenum|QB keep and throw to back of end zone, incomplete|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:48|CHI|R.Odunze|Incomplete pass, lands out of bounds|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:59|CHI|C.Keenum|Quick throw broken up|0|unknown|unknown|unknown|Q.Mitchell|unverified (no DB match; caption-only)|
|05:08|PHI|S.Barkley|Run for breathing room|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:13|PHI|J.Hurts|Pass to D.Smith on third and one|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:27|PHI|J.Hurts|Pass to D.Smith, defensive pass interference|21|deep shot|unknown|unknown|C.Lewis|verified vs DB|
|05:48|PHI|S.Barkley|Run left side|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:54|PHI|S.Barkley|Run|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:07|PHI|S.Barkley|Run left side, out of bounds inside the 5|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:12|CHI|A.Dalton|Pass intended for D.Wicks, intercepted|0|unknown|unknown|unknown|D.Thieneman|verified vs DB|
|06:40|CHI|C.Keenum|Pass to L.Burden for 25 yards|25|unknown|unknown|unknown|A.Mukuba|verified vs DB|
|06:52|CHI|C.Keenum|Pass to R.Odunze for 22 yards|22|deep shot|unknown|unknown|M.Epps|verified vs DB|
|07:03|CHI|C.Keenum|Pass to K.Raymond|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:17|CHI|M.Monangai|Run met in backfield|None|unknown|unknown|unknown|J.Hunt|unverified (no DB match; caption-only)|
|07:26|CHI|C.Keenum|Pass incomplete between Loveland and Burden, leads to FG|0|unknown|unknown|unknown|unknown|verified vs DB|
|07:46|PHI|D.Wicks|Pass reception, out of bounds with first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:52|PHI|J.Hurts|Pass to D.Smith, good catch|30|deep shot|unknown|unknown|J.Johnson|verified vs DB|
|08:05|PHI|J.Hurts|Quick throw to Z.Ertz|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:13|PHI|J.Hurts|QB sneak or run for touchdown|1|unknown|unknown|unknown|unknown|verified vs DB|
|08:52|PHI|J.Hurts|Pass nearly picked by Edwards|0|unknown|unknown|unknown|T.Edwards|verified vs DB|
|08:55|CHI|D.Swift|Handoff for 9 yards|9|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:08|CHI|C.Keenum|Play-action, pass to Loveland for 12 yards|12|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:14|CHI|C.Keenum|Pass to K.Raymond under pressure|None|unknown|unknown|unknown|J.Hunt|unverified (no DB match; caption-only)|
|09:31|PHI|Q.Mitchell|Defensive play on the edge|None|unknown|unknown|unknown|I.Rodgers|unverified (no DB match; caption-only)|
|09:41|CHI|C.Santos|Field goal|48|unknown|unknown|unknown|unknown|verified vs DB|
|09:45|PHI|J.Hurts|Pass incomplete on third down|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:57|CHI|K.Raymond|Pass reception out of bounds near first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:11|CHI|M.Monangai|Run for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:25|CHI|K.Raymond|Pass reception for touchdown|41|unknown|unknown|unknown|unknown|verified vs DB|
|10:41|PHI|W.Shipley|Pass reception, short of first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:03|PHI|J.Hurts|Deep pass to D.Wicks|None|deep shot|unknown|unknown|J.Johnson|unverified (no DB match; caption-only)|
|11:16|PHI|J.Hurts|Quick throw to D.Smith|None|unknown|unknown|unknown|E.Hicks|unverified (no DB match; caption-only)|
|11:24|PHI|J.Hurts|Pass intercepted by Edwards|0|unknown|unknown|unknown|T.Edwards|verified vs DB|
|11:41|CHI|M.Monangai|Toss play, cut upfield for 10+ yards|10|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:52|CHI|C.Keenum|Hit by Campbell, fumble recovered by Eagles? (called against Eagles)|None|unknown|unknown|unknown|J.Campbell|unverified (no DB match; caption-only)|
|12:20|CHI|C.Keenum|Pass with holding penalty on defense|None|unknown|unknown|unknown|A.Mukuba|unverified (no DB match; caption-only)|
|12:43|CHI|D.Swift|Handoff, pushing pile to the 1|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:48|CHI|C.Keenum|QB run for touchdown|1|unknown|unknown|unknown|unknown|verified vs DB|
|13:04|PHI|M.Lemon|Pass reception, breaking tackles|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:18|PHI|J.Hurts|Run for nearly 25 yards, player down (C.Lewis injured)|20|unknown|unknown|unknown|C.Lewis|verified vs DB|

Offense (model synthesis from this game's plays): Explosive deep passes to D.Smith / Effective late-game hurry-up drives resulting in TD / Ability to convert on third and short with runs and passes

Defense weaknesses: Missed tackles in open field (e.g. Epps on Burden) / Susceptible to big passing plays downfield / Defensive penalties in secondary (DPI, holding, illegal contact) / Vulnerable to Bears' red zone efficiency and play-action

Limitations: Could not determine specific concepts like run gaps, RPOs, screens, or exact personnel formations and coverage schemes as they were not explicitly stated by commentators or clearly shown in DB text. Many caption plays had no direct DB match due to name mangling and incomplete details. Auto-generated captions had many inaccuracies in player names and play details that were corrected only where clear matches existed.


## Week 4: LAR 24 - PHI 20 (game 401872970)
Video: Los Angeles Rams vs. Philadelphia Eagles Game Highlights | NFL 2026 Season Week 4 — https://www.youtube.com/watch?v=h6eywSmXaCI  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|01:39|PHI|Jake Elliott|Field goal from 29 yards|None|field goal|unknown|unknown|unknown|verified vs DB|
|06:35|PHI|DeVonta Cooper|Touchdown (Hurts deep right to Cooper)|18|deep right|unknown|unknown|unknown|verified vs DB|
|06:57|LAR|Matthew Stafford|Nobody open, stands in, intercepted (late 2Q)|25|deep right|unknown|unknown|unknown|verified vs DB|
|07:34|PHI|DeVonta Cooper|Hurts, end zone, touchdown; illegal contact flag|10|short middle|unknown|unknown|unknown|verified vs DB|
|13:22|LAR|Tyler Higbee|Higbee first down, 20 yards|20|deep right|unknown|unknown|unknown|verified vs DB|
|14:26|LAR|Kyren Williams|Williams walks in, touchdown|1|run left guard|unknown|unknown|unknown|verified vs DB|
|16:04|LAR|Kyren Williams|Williams fights his way in, touchdown|7|run left end|unknown|unknown|unknown|verified vs DB|
|10:12|LAR|Matthew Stafford|Blitz coming, Stafford with a man wide open (unclear which play)|None|vs blitz|unknown|blitz|unknown|unverified (no DB match; caption-only)|

Offense (model synthesis from this game's plays): Cooper RZ TDs / Blitz-heavy D (commentary: "Eagles show blitz")

Defense weaknesses: Williams goal-line runs late / Nacua deep right / Blitz beaten for open man

Limitations: Captions skimmed by keyword. Coverage stated only as double coverage and repeated blitz calls by both teams. Hurts later reported out for season — PHI QB context changes.


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

Offense (model synthesis from this game's plays): Deep passing ability with accurate throws to D.Cooper and others for big gains and TDs / Effective use of play-action leading to successful passes / Ability to convert on third downs and in short-yardage with runs by Shipley and Hurts mobility / Tight end involvement with Goedert and receivers like Wicks and Lemieux making contested catches

Defense weaknesses: Susceptible to big passing plays allowing multiple 20+ yard receptions and TDs to Washington / Struggles in red zone defense allowing TDs and needing penalties to stop drives / Vulnerable to fumbles forced on opposing QB but also turnover on downs and interceptions not always capitalized / Defensive line pressure leads to hits but coverage allows YAC and deep shots

Limitations: Could not determine specific run gaps/directions, exact personnel formations, or coverage schemes as they were not explicitly stated by commentators except for a few cases like empty set, play-action, screen, and deep shots. Many plays lacked direct DB matches due to name mangling and incomplete details. Some player names corrected only on clear matches (e.g. Washington, Shipley, Lawrence). Several plays had ambiguous or incomplete descriptions from auto-generated captions.


## Week 6: CAR 25 - PHI 14 (game 401872998)
Video: Carolina Panthers vs. Philadelphia Eagles Game Highlights | NFL 2026 Season Week 6 — https://www.youtube.com/watch?v=7x-qq154bgs  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:11|CAR|unknown|Run through a big hole for a first down near midfield; Tommy Tremble credited with a block.|None|unknown|Tight end in motion|unknown|unknown|unverified (no DB match; caption-only)|
|00:24|CAR|Bryce Young to Tetairoa McMillan|Completion downfield from a clean pocket.|15|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:32|CAR|Chuba Hubbard|Stopped at the 29 on third-and-4.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:40|CAR|Ryan Fitzgerald|Makes a 47-yard field goal.|47|Field goal|unknown|unknown|unknown|verified vs DB|
|00:50|PHI|Tanner McKee|Third-and-6 pass falls incomplete after a receiver goes down; flag near the goal line. Penalty outcome is omitted.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:01|CAR|Bryce Young to Tetairoa McMillan|Completion over the middle with roughing the passer called. The caption's Philadelphia possession reference conflicts with the named passer and receiver.|None|unknown|Shotgun|unknown|unknown|unverified (no DB match; caption-only)|
|01:16|CAR|Bryce Young to Tommy Tremble|Wide-open touchdown. Replay commentary says Quinyon Mitchell reacts to the other tight end going inside and recognizes Tremble's outside release too late.|12|Tight end shows block, then releases outside; other tight end goes inside|Two tight ends mentioned; full personnel unknown|unknown|Quinyon Mitchell|verified vs DB|
|01:52|PHI|Tanner McKee to Dallas Goedert|Completion after a fake handoff.|None|Play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:00|PHI|Tanner McKee to DeVonta Smith|Completion into Carolina territory.|16|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:13|PHI|Tanner McKee to Cooper|Receiver comes back for a soft throw at the 31-yard line; first name cannot be established.|9|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:27|PHI|Dameon Pierce|Powers through a goal-line collision for a touchdown. Commentary credits Tyler Steen's block on the right side; DB records the run up the middle.|2|Up the middle; right-side blocking described|unknown|unknown|unknown|verified vs DB|
|03:01|CAR|Chuba Hubbard|Spins and carries a crowd toward midfield; penalty flag down, with no clear ruling supplied.|9|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:17|CAR|Chuba Hubbard|Takes an opening for a first down.|11|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:28|CAR|Bryce Young targeting Jalen Coker|Third-and-10 pass incomplete with DeJean covering.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:37|CAR|Ryan Fitzgerald|Makes a 52-yard field goal.|52|Field goal|unknown|unknown|unknown|verified vs DB|
|04:02|CAR|Chuba Hubbard|Stuffed for no gain needing a little more than a yard; Davis and Byron Young credited. Caption mentions Philadelphia and fourth down, leaving the exact down context uncertain.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:18|PHI|Tanner McKee to Dallas Goedert|Second-and-10 completion for a first down and additional yards after the catch.|18|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:33|PHI|Tanner McKee|Sacked; the defender's name is cut off.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:40|CAR|Bryce Young to Jalen Coker|Young leaves the pocket and completes a pass that Coker takes across the 40; Mukuba makes the tackle.|32|Short middle pass; throw outside the pocket|unknown|unknown|A. Mukuba (DB tackler)|verified vs DB|
|05:00|CAR|Bryce Young|First-down gain to just inside the 40; captions do not clearly establish whether this is a pass or run.|15|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:06|CAR|Chuba Hubbard|Converts fourth-and-less-than-a-yard and keeps driving through contact.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:22|CAR|Bryce Young|Steps up and scrambles on third-and-9, finishing just short of the first down against Jeremiah Trotter Jr.|None|Quarterback scramble|Empty shotgun|unknown|unknown|unverified (no DB match; caption-only)|
|05:41|CAR|Chuba Hubbard|Scores on second-and-goal.|1|Left end|unknown|unknown|unknown|verified vs DB|
|05:52|CAR|Bryce Young targeting John Metchie|Two-point conversion pass incomplete under pressure.|0|unknown|unknown|unknown|unknown|verified vs DB|
|06:03|PHI|Tanner McKee to Wicks|Wicks makes two defenders miss and zigzags into Carolina territory, then grabs his ankle.|17|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:18|PHI|Tanner McKee to DeVonta Smith|Line-drive completion awarded a first down. Nearby captions say both second-and-10 and gain of four, so the down-and-distance context is uncertain.|4|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:32|PHI|Tanner McKee to DeVonta Smith|Touchdown on a ball placed over Will Lee's head; Lee misses an attempted right-hand breakup.|19|Deep right shot|unknown|unknown|Will Lee|verified vs DB|
|07:02|CAR|Bryce Young targeting Tetairoa McMillan|Third-and-8 throw bounces incomplete, ending a three-and-out.|0|unknown|Shotgun|unknown|unknown|unverified (no DB match; caption-only)|
|07:18|PHI|Tanner McKee targeting DeVonta Smith|Third-and-18 throw described as lacking velocity; a flag is mentioned, but the pass result and ruling are unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:31|PHI|unknown|Philadelphia's kick is blocked by Carolina. The captions do not identify the kicker, blocker, or kick type.|None|Blocked kick|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:44|CAR|Chuba Hubbard|Needs one yard and gains five for a first down. Philadelphia number 33 receives a subsequent 15-yard unnecessary-roughness penalty.|5|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:02|CAR|Bryce Young to Tommy Tremble|Second Tremble touchdown. Young fakes the handoff, boots right and throws back left; commentary says Philadelphia loses Tremble in coverage. Tremble is penalized for taunting after the score.|19|Play-action boot right with throwback left|unknown|unknown|unknown|verified vs DB|
|08:48|PHI|Tanner McKee to Lemon|Completion as Philadelphia drives; receiver identified only as Lemon.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:57|PHI|Tanner McKee targeting DeVonta Smith|Contested deep pass incomplete with Wheatley defending.|0|Deep shot|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:08|CAR|Bryce Young to David Moore|Catch and run to the Philadelphia 13; Byron Young catches Moore from behind.|27|Short left pass|unknown|unknown|Byron Young (DB tackler)|verified vs DB|
|09:20|CAR|Chuba Hubbard|Squeezes through for a first-down run with 3:24 remaining.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:31|CAR|Chuba Hubbard|Runs for another first down, allowing Carolina to kneel out the game.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:41|CAR|Bryce Young|Takes the final kneel-down.|None|Quarterback kneel|unknown|unknown|unknown|unverified (no DB match; caption-only)|

Offense (model synthesis from this game's plays): McKee connected repeatedly with Smith, including a 16-yard gain and a 19-yard touchdown. / Goedert supplied a play-action completion and a separate 18-yard catch and run. / Pierce finished a goal-line run through contact, with commentary crediting Steen's blocking.

Defense weaknesses: Mitchell reacted to the inside tight-end movement and recognized Tremble's touchdown release too late. / The defense lost Tremble on Carolina's boot-right, throwback-left touchdown. / Carolina generated 32- and 27-yard receptions and several Hubbard first-down runs. / A late unnecessary-roughness penalty added 15 yards after Hubbard's five-yard conversion.

Limitations: Analysis uses only the supplied captions and DB excerpt; no video frames or external sources. DB matches contain the exact quarter/clock identifiers requested. The DB excerpt is selective, so NO DB MATCH does not mean a play did not occur. No captioned play clearly matches the two DB-listed 21-yard McMillan catches or the DB-listed defensive pass-interference plays. Unshown DB events were not added. Auto-caption errors and editing obscure some identities, outcomes, down-and-distance details and one 15-yard gain's play type. Full personnel groupings, coverage schemes, most run gaps and individual coverage responsibilities cannot be established. Named DB tacklers are labeled as such and do not establish a coverage defeat; defenders credited with successful stops are described without labeling them beaten. Field-goal yards are kick distances; null means the gain is undetermined. The closing caption says Young had two passing touchdowns, conflicting with the three supplied DB passing-touchdown entries; scoring follows the DB.
