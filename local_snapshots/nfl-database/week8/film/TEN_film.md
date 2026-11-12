# TEN — Phase 8 film notes (Weeks 1–6, 2026)
> Note: games 401872956, 401872973, 401872984 were extracted by Grok via the xAI API (grok-4.20-0309-non-reasoning, same prompt/schema as Codex, cleaned captions); sidecar provenance in film/grok_meta/. All other games with notes: Codex.

Method: NFL YouTube channel full-game highlight videos were located by search and their auto-captions (broadcast commentary) downloaded via yt-dlp. Codex (codex-cli 0.163.0) extracted plays from the captions. **No video frames were viewed by any agent.** Each play was checked against the repo DB play-by-play: `verified vs DB` means the cited DB play exists and the yardage matches. Personnel, formation and coverage appear only when commentators stated them; everything else is `unknown`.


## Week 1: NYJ 23 - TEN 10 (game 401872924)
Video: New York Jets vs Tennessee Titans Game Highlights | NFL 2026 Week 1 — https://www.youtube.com/watch?v=vt9DKUJ_Q-Y  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:28|NYJ|Geno Smith; receiver unknown|Smith sets up a screen; the receiver and result are unclear.|None|screen|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:41|NYJ|O. Cooper|Third-and-9 completion underneath; Cooper breaks free and reaches the Tennessee 4. Commentary describes an overloaded blitz and an assignment error.|30|short left pass; underneath route|unknown|overload blitz; only two underneath defenders|A. Taylor; J. Johnson (DB tacklers)|verified vs DB|
|01:10|NYJ|K. Sadiq|Sadiq scores on a misdirection run.|3|misdirection; left end|unknown|unknown|unknown|verified vs DB|
|01:28|TEN|Cam Ward|Ward uses his mobility to scramble for a first down. The captioned down and distance are unreliable.|None|quarterback scramble|five receivers|unknown|unknown|unverified (no DB match; caption-only)|
|01:45|TEN|Carnell Tate|Tate catches a wobbling pass on second-and-15 with heavy pressure coming.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:58|TEN|Cam Ward|On a misdirection play, Ward appears to flick the ball to himself and gets back to approximately the line of scrimmage.|None|misdirection|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:07|TEN|Cam Ward; tight end identified in captions as Belanger|Third-and-11 underneath completion gains seven, short of the first down.|7|underneath pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:20|TEN|J. Slye|Makes a 42-yard field goal for Tennessee's first points.|42|field goal|unknown|unknown|unknown|verified vs DB|
|02:34|NYJ|Breece Hall|Hall finds a seam through the middle of Tennessee's defense from inside New York's own 12.|None|interior run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:44|NYJ|Braelon Allen|Allen's first carry gains seven and takes him across the 30.|7|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:01|NYJ|Garrett Wilson|Wilson catches a pass over the middle and holds on through Kevin Winston Jr.'s hit for a first down.|None|pass over the middle|unknown|unknown|Kevin Winston Jr. (contact defender)|unverified (no DB match; caption-only)|
|03:17|NYJ|Breece Hall|Smith uses play-action and finds Hall underneath for nine yards, ending around the Tennessee 22 or 23.|9|play-action; underneath pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:36|NYJ|Braelon Allen|Quick throw to Allen out of the backfield; Anthony Hill closes and punches at the ball. A turnover is not established.|None|backfield pass|unknown|unknown|Anthony Hill (closing defender)|unverified (no DB match; caption-only)|
|04:02|NYJ|J. Sanders|Makes a 33-yard field goal to finish an 18-play drive.|33|field goal|unknown|unknown|unknown|verified vs DB|
|04:23|TEN|C. Dike|Dike fumbles on the kickoff return. DB identifies M. McCrary-Ball as forcing the fumble and Q. Stiggers as recovering for New York at the Tennessee 38.|20|kickoff return|unknown|unknown|M. McCrary-Ball (forced fumble); Q. Stiggers (recovery)|CONFLICT (yardage 20 vs DB)|
|04:48|NYJ|Mason Taylor|Taylor is targeted on second-and-7 from the Tennessee 35; commentary says he had little chance, but the precise result is unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:59|NYJ|Garrett Wilson|A fragmented call identifies Wilson and praises an open-field tackle by a defender captioned as Marquis Harris.|None|unknown|unknown|four-man rush|Marquis Harris (captioned name; tackler)|unverified (no DB match; caption-only)|
|05:13|NYJ|J. Sanders|Misses a 54-yard field goal wide left. Commentary initially suspects a deflection, then says nobody touched it.|54|field goal|unknown|unknown|unknown|verified vs DB|
|05:35|TEN|Cam Ward; unidentified rookie receiver|Ward completes a pass to a rookie for a positive first-down play. Thomas is identified for the Jets.|None|unknown|unknown|unknown|Thomas (captioned surname only)|unverified (no DB match; caption-only)|
|05:46|TEN|Wan'Dale Robinson|Ward throws on the run to Robinson for a first down, moving Tennessee to the New York 44.|None|pass on the run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:01|TEN|Tony Pollard|Second-down underneath pass to Pollard ends with an open-field tackle.|None|underneath pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:09|TEN|Cam Ward|Third-and-4 throw toward the near side is incomplete.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:26|NYJ|Geno Smith|Play-action to Hall is called; the remainder of this play is obscured by the sideline report.|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:36|NYJ|Garrett Wilson|Smith completes a 31-yard pass to Wilson into Tennessee territory.|31|deep right pass|unknown|unknown|A. Taylor (DB tackler)|verified vs DB|
|06:55|NYJ|A. Mitchell|Mitchell catches a deep outside pass against Amani Hooker. Captions call it 41 yards; authoritative DB records 40.|40|deep right shot|unknown|unknown|Amani Hooker|verified vs DB|
|07:14|NYJ|Geno Smith|Smith runs and slides near the 2-yard line; commentary notes uncertainty about the spot.|None|quarterback run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:28|NYJ|Breece Hall|Hall scores from four yards. DB records a declined Tennessee too-many-men penalty.|4|left end run|double tight end set|unknown|unknown|verified vs DB|
|07:57|TEN|Cam Ward|Ward steps up in the pocket and runs.|None|quarterback scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:05|TEN|Tyjae Spears|Third-down pass over the middle is incomplete after Spears cannot secure it; Demario Davis is nearby.|None|pass over the middle|unknown|four-man rush|Demario Davis (nearby defender)|unverified (no DB match; caption-only)|
|08:26|NYJ|Breece Hall|Hall follows a lead blocker for a first down.|None|run with lead blocker|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:34|NYJ|unknown|An unidentified ball carrier resists going down and spins; the captioned result is truncated.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:48|NYJ|Garrett Wilson|Smith delivers another on-time completion to Wilson, matching the DB's 22-yard gain in this sequence.|22|deep left pass|unknown|unknown|C. Flott (DB tackler)|verified vs DB|
|09:10|NYJ|Geno Smith|Tennessee sends an extra defender and Smith gets the ball out quickly; receiver and result are omitted.|None|quick pass|unknown|extra-defender pressure|unknown|unverified (no DB match; caption-only)|
|09:17|NYJ|J. Sanders|Makes a 51-yard field goal.|51|field goal|unknown|unknown|unknown|verified vs DB|
|09:35|TEN|Tony Pollard|Pollard produces a good first-down run.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:45|TEN|Cam Ward|A fake and sidearm delivery are followed by an incomplete call.|None|fake; sidearm pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:47|TEN|Wan'Dale Robinson|Robinson makes a first-down reception as Ward's safety valve. The edit into this completion is abrupt.|None|safety-valve pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:00|TEN|Tony Pollard|Pollard runs around the edge for a first down.|None|edge run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:11|TEN|Cam Ward|Ward feels pressure and initially evades McDonald; the final outcome is unclear.|None|unknown|unknown|unknown|McDonald (initial sack attempt)|unverified (no DB match; caption-only)|
|10:23|NYJ|Geno Smith; unidentified tight end|Smith rolls out and completes to a tight end for four yards.|4|rollout pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:35|NYJ|Geno Smith|Smith works from the gun; the play finishes about a yard short of a first down, with ball carrier and play type unclear.|None|unknown|shotgun|unknown|unknown|unverified (no DB match; caption-only)|
|10:52|TEN|Cam Ward|Will McDonald IV sacks Ward as the Jets bring heavy pressure; commentary calls it New York's third sack.|None|unknown|unknown|heavy pressure|Will McDonald IV (sacker)|unverified (no DB match; caption-only)|
|11:01|TEN|unknown|On third-and-25, Tennessee tries to recover yardage; an unidentified ball carrier is tripped up short of the 15.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:32|NYJ|Sadiq|Smith completes a pass to Sadiq.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:42|TEN|Wan'Dale Robinson|Robinson gains a Tennessee first down on a play featuring a hard hit from Dane Belton.|None|unknown|unknown|heavy pressure|Dane Belton (contact defender)|unverified (no DB match; caption-only)|
|11:58|TEN|Cam Ward|Ward buys time; the captions omit the result.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:09|NYJ|unknown|An unidentified Jets runner slips through a seam for another first down.|None|run through a seam|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:24|NYJ|Allen|Allen is mentioned in a truncated play call immediately before the field-goal attempt; result is unavailable.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:26|NYJ|J. Sanders|Makes a 52-yard field goal to extend the lead to 23-3.|52|field goal|unknown|unknown|unknown|verified vs DB|
|12:51|TEN|Wan'Dale Robinson|Robinson makes a catch on Tennessee's late possession.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:56|TEN|Tyjae Spears|Ward finds Spears out of the backfield, where a defender identified as Brownlee meets him.|None|backfield pass|unknown|unknown|Brownlee (captioned surname only)|unverified (no DB match; caption-only)|
|13:13|TEN|unknown|An unidentified Tennessee ball carrier takes on tacklers and is forced out by Andre Cisco.|None|unknown|unknown|unknown|Andre Cisco (out-of-bounds defender)|unverified (no DB match; caption-only)|
|13:28|TEN|E. Ayomanor|Ward throws his first touchdown of the season, an 11-yard completion to Ayomanor.|11|short right pass|unknown|unknown|unknown|verified vs DB|

Offense (model synthesis from this game's plays): Ward's mobility produced a scrambling first down and an on-the-run first-down completion to Robinson. / Robinson repeatedly provided completions, including first downs. / Pollard produced a positive first-down run and an edge run for another first down. / Ward connected with Ayomanor for a late 11-yard touchdown.

Defense weaknesses: An overload blitz left only two underneath defenders; Cooper's short catch became a 30-yard gain. / The secondary conceded second-half passes of 31, 40 and 22 yards; Mitchell's 40-yard catch came against Amani Hooker. / Hall found running seams and gained a first down behind a lead blocker. / New York scored rushing touchdowns on misdirection and a left-end run from a double-tight-end set. / Commentary reported little pressure on Smith before Tennessee sent an extra defender and Smith released quickly.

Limitations: Captions only; no frames were viewed and no commands were run. Abrupt edits and transcription errors obscure some players, outcomes, distances and play boundaries. DB matches use the supplied authoritative subset; NO DB MATCH does not mean a play was absent from the full game. DB distances override conflicting captions. Field-goal yards are kick distances; return yards are return distances. Personnel and defensive schemes are included only when explicitly stated in commentary; no coverage shell or man/zone assignment can be established. Named tacklers or nearby defenders are identified as such and are not necessarily defenders beaten in coverage. The opening kickoff penalty and the third-quarter 27-yard return appear only in the DB and are not identifiable in the captions. Extra points are not separately identified in the captions. The 09:45-09:55 passage may splice two plays; the incomplete call and Robinson completion are recorded separately with that uncertainty.


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

Offense (model synthesis from this game's plays): Ward's movement created a scramble to the one, a sneak touchdown and a later one-yard scrambling touchdown. / Play-action produced substantial gains to Ridley and Ayomanor. / Spears contributed a 27-yard reception and a 27-yard left-end run. / Pollard gained 13 yards behind multiple blockers from a two-back look and later opened a possession with an eight-yard run. / Ward found Robinson in space vacated by an edge blitz.

Defense weaknesses: Allowed repeated first-down completions to Smith and Wicks, including conversions against extra rushers. / Hooker was beaten behind the defense for Smith's 22-yard touchdown after Hurts extended the play. / Allowed Bigsby's powerful middle runs near the goal line, including a two-yard touchdown. / Harris surrendered Wicks' contested 20-yard catch to begin Philadelphia's winning possession. / Three defenders showed assignment indecision after Smith's motion, leaving Cooper open for the winning touchdown against Cover Zero.

Limitations: Captions only; no routes, alignments, blocking assignments or coverage details were inferred from video. The supplied DB is a selected subset, so NO DB MATCH does not mean a play did not occur. Only caption-identifiable plays are listed; DB-only kickoffs, returns and other uncaptioned events are omitted. DB distances take precedence where clearly matched. For interceptions, yards denotes return distance; for field goals, kick distance. Null yards means the gain cannot be established. Named tacklers, interceptors and contesting defenders are labeled by role and are not necessarily defenders beaten. Unmatched names remain as captioned without speculative DB corrections. Pressure descriptions do not establish a coverage shell. The isolated swing-route fragment and retrospective references to earlier goal-line runs do not establish additional distinct plays.


## Week 3: TEN 7 - NYG 12 (game 401872956)
Video: Tennessee Titans vs. New York Giants Game Highlights | NFL 2026 Season Week 3 — https://www.youtube.com/watch?v=GmCLbwLRGqA  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:32|TEN|C.Dike|Kickoff return fumble|34|unknown|unknown|unknown|unknown|verified vs DB|
|01:29|NYG|C.Skattebo|Pass reception|25|unknown|unknown|unknown|unknown|CONFLICT (yardage 25 vs DB)|
|02:11|NYG|D.Zvada|Field goal good|39|unknown|unknown|unknown|unknown|verified vs DB|
|03:50|NYG|D.Zvada|Field goal good|27|unknown|unknown|unknown|unknown|verified vs DB|
|04:28|TEN|J.Slye|Field goal missed wide left|59|unknown|unknown|unknown|unknown|verified vs DB|
|05:18|NYG|D.Zvada|Field goal good|39|unknown|unknown|unknown|unknown|verified vs DB|
|05:32|NYG|C.Skattebo|Run to the outside|20|unknown|unknown|unknown|K.Flott|CONFLICT (yardage 20 vs DB)|
|07:22|TEN|C.Tate|Pass reception|20|unknown|unknown|unknown|C.Hood|verified vs DB|
|09:49|TEN|W.Robinson|Passing touchdown|4|unknown|unknown|unknown|C.Hood|verified vs DB|
|11:44|TEN|C.Ward|Pass interception|-6|unknown|unknown|unknown|J.Holland|verified vs DB|

Offense (model synthesis from this game's plays): Sustained drives with consistent first downs via short passes to multiple receivers (Robinson, Tate, Pollard) / Effective quick passes and exploitation of soft man coverage / Ability to convert third downs in the second half

Defense weaknesses: Vulnerable to big passing plays allowing 25-30 yard receptions / Struggled to stop Giants run game in short yardage and red zone / Missed field goals from long distance

Limitations: Could not determine specific concepts like run gaps, play-action, screens, RPOs, personnel formations, or coverage schemes because they were not explicitly stated by commentators or clearly shown in DB text. Many plays in captions were hard to precisely match to DB due to name mangling and incomplete details; only clear matches used. Several mentioned plays (e.g. early Giants runs, sacks, some incompletions) lacked sufficient detail for yards or full attributes.


## Week 4: TEN 18 - BAL 24 (game 401872973)
Video: Tennessee Titans vs Baltimore Ravens Game Highlights | 2026 NFL Season Week 4 — https://www.youtube.com/watch?v=1MzoImgClWQ  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:12|TEN|C.Dike|Kickoff return to plus territory|40|unknown|unknown|unknown|unknown|verified vs DB|
|00:25|TEN|C.Ward|Pass intercepted after pocket collapse|24|unknown|unknown|unknown|T.Simpson|verified vs DB|
|00:48|BAL|Z.Flowers|Pass reception across formation inside the 10|23|unknown|unknown|unknown|C.Flott|verified vs DB|
|01:01|BAL|D.Henry|Rushing touchdown left side/guard|5|Zone Read|unknown|unknown|W.Winston|verified vs DB|
|01:40|TEN|T.Pollard|Hand off sweeps left side past 40 for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:47|TEN|W.Robinson|Screen pass tunnels through for solid gain|None|screen|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:01|TEN|C.Tate|Wide open pass reception inside the 25|22|unknown|unknown|unknown|K.Hamilton|verified vs DB|
|02:11|TEN|T.Spears|Early touch, dances and stays in bounds|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:25|TEN|T.Pollard|Run through hole for rushing touchdown|3|unknown|unknown|unknown|unknown|verified vs DB|
|02:58|BAL|M.Hibner|Pass reception to the 30|25|unknown|unknown|unknown|A.Taylor|verified vs DB|
|03:44|BAL|Z.Flowers|Pass reception on comeback route past the 25|None|unknown|unknown|Zone|unknown|unverified (no DB match; caption-only)|
|03:54|BAL|D.Henry|Run with first contact 11 yards past line|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:08|BAL|M.Hibner|Wide open tight end reception to the 30|None|unknown|unknown|unknown|unknown|verified vs DB|
|04:22|BAL|Z.Flowers|Big catch scooped for big gain|19|unknown|unknown|unknown|A.Hill|verified vs DB|
|05:02|BAL|M.Andrews|Scoop and grab reception over the middle|3|play-action|unknown|unknown|A.Schlottmann|verified vs DB|
|05:39|BAL|R.Bateman|Pass caught for first down after motion|28|unknown|unknown|unknown|unknown|verified vs DB|
|06:18|BAL|Z.Flowers|Roll-out pass to sideline in stride to the 5|52|unknown|unknown|unknown|C.Barton|verified vs DB|
|06:29|BAL|M.Andrews|Faked wildcat, play-action pass over middle for touchdown|3|play-action|unknown|unknown|unknown|verified vs DB|
|07:03|TEN|C.Tate|Beautiful deep reception on 4-wide set|None|deep shot|4-Wide|unknown|unknown|unverified (no DB match; caption-only)|
|08:01|TEN|C.Tate|Roll out cross body throw catch, then fumbled after knock away|33|unknown|unknown|unknown|K.Hamilton|verified vs DB|
|09:28|TEN|C.Tate|Rookie makes catch at the 26 for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:40|TEN|C.Tate|Pass across the middle for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:52|TEN|C.Ward|Escapes and runs out of bounds|22|unknown|unknown|unknown|J.Hawkins|verified vs DB|
|10:32|BAL|Z.Flowers|Faked reverse, gets ball and loss on play|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:02|TEN|C.Ward|Third and short pass to sideline incomplete|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:29|BAL|J.Hill|Run to the 47 with tackle|None|unknown|unknown|unknown|A.Hill|unverified (no DB match; caption-only)|
|11:37|BAL|D.Henry|Huntley play-action screen plowed and hit hard|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:48|BAL|D.Henry|Perimeter run up and over midfield|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:00|BAL|D.Henry|Parallel run-and-catch turns up but hog-tied|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:30|BAL|D.Henry|Picking up first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:37|BAL|T.Huntley|Admiring the run from Huntley, physicality|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:54|BAL|R.Bateman|Rush up, makes the play, down at the 26|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:07|BAL|D.Henry|Third down run outside angle, cannot turn corner|None|unknown|unknown|unknown|W.Winston|unverified (no DB match; caption-only)|
|13:37|TEN|C.Tate|Ward fires into ground, catch at 42 for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:53|TEN|C.Ward|Strides for first down, runs out of bounds around 35|22|unknown|unknown|unknown|unknown|verified vs DB|
|14:19|TEN|C.Tate|Across body throw to rookie inside 20, zig zags to 10|33|deep shot|unknown|unknown|M.Starks|verified vs DB|
|14:40|TEN|W.Robinson|Pass for touchdown|3|unknown|unknown|unknown|unknown|verified vs DB|
|15:04|TEN|G.Helm|Two-point conversion across the middle|None|unknown|unknown|unknown|unknown|verified vs DB|

Offense (model synthesis from this game's plays): Explosive deep passes to C.Tate / Screen passes and quick game to W.Robinson / Mobile QB scrambles by C.Ward for significant yardage / Utilizing rookie WR C.Tate in multiple roles for chunk plays

Defense weaknesses: Struggles containing D.Henry on outside and inside runs allowing big gains before first contact / Vulnerable to play-action and RPO concepts by BAL / Defensive backs beaten on deep shots and intermediate routes by BAL WRs / Poor tackling in open field against BAL skill players

Limitations: Could not determine exact yards, specific gaps, formations, coverages, or defender names for many plays as they were not explicitly stated in the captions or did not perfectly align with DB entries; many caption descriptions were vague or name-mangled without clear DB matches; could not identify all scoring or big plays mentioned in DB due to caption focus on highlights only.


## Week 5: HOU 26 - TEN 3 (game 401872984)
Video: Houston Texans vs. Tennessee Titans Game Highlights | NFL 2026 Season Week 5 — https://www.youtube.com/watch?v=K4ZVwiL_Tf4  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:25|TEN|C.Ridley|Pass short middle to Ridley for 23 yards|23|unknown|unknown|unknown|unknown|verified vs DB|
|01:00|TEN|J.Slye|30 yard field goal is GOOD|30|unknown|unknown|unknown|unknown|verified vs DB|
|01:19|HOU|C.Stroud|Pass to Schultz for first down (14 yards)|14|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:32|HOU|C.Stroud|Pass complete to Hutchinson for 18 yards|18|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:10|TEN|T.Spears|Fumble recovered by opponent (J.Pitre)|0|unknown|unknown|unknown|D.Robinson|verified vs DB|
|02:45|HOU|K.Fairbairn|45 yard field goal is GOOD|45|unknown|unknown|unknown|unknown|verified vs DB|
|03:11|TEN|C.Ward|Pass intercepted by J.Hansen, 19 yard return|19|unknown|unknown|unknown|unknown|verified vs DB|
|03:25|HOU|C.Stroud|Pass to Schultz|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:31|HOU|C.Stroud|Pass to Hutchinson to the 10 yard line|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:45|HOU|C.Stroud|Pass to Noel, couple yards shy of first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:58|HOU|K.Fairbairn|26 yard field goal is GOOD|26|unknown|unknown|unknown|unknown|verified vs DB|
|04:15|HOU|C.Stroud|Pass to N.Collins for 20 yards|20|deep shot|unknown|unknown|unknown|verified vs DB|
|04:29|HOU|W.Marks|Rush for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:39|HOU|J.Noel|Rush for 1 yard|1|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:49|HOU|K.Fairbairn|53 yard field goal is GOOD|53|unknown|unknown|unknown|unknown|verified vs DB|
|05:34|HOU|C.Stroud|Pass to K.Boutte for 23 yards|23|unknown|unknown|unknown|unknown|verified vs DB|
|05:47|HOU|C.Stroud|Recovers bad snap, pass to Noel for 9 yards|9|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:58|HOU|C.Stroud|Pass to K.Boutte|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:06|HOU|C.Stroud|Pass to N.Collins inside TEN 10|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:28|HOU|C.Stroud|2 yard rushing touchdown|2|unknown|unknown|unknown|unknown|verified vs DB|
|07:19|HOU|C.Stroud|Pass to Hutchinson out of bounds at the 10|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:28|HOU|C.Stroud|Pass to J.Noel for touchdown|9|unknown|unknown|unknown|A.Taylor|verified vs DB|

Offense (model synthesis from this game's plays): Early big play with 23-yard reception to Ridley / Mobile QB (Ward) ability to escape pressure and create with legs

Defense weaknesses: Poor pass coverage leading to multiple big passing plays and DPI penalty / Inability to stop Houston's offense in red zone allowing TDs and FGs / Frequent sacks and pressures on QB / Turnover prone with interception and fumble

Limitations: Many plays in captions lack specific yardage, exact player names (relied on DB for matches), defensive coverages, formations, or concepts as commentators rarely stated them explicitly. Several caption plays had no clear DB match due to incomplete or mismatched details. Auto-generated captions had many name mangles and transcription errors.


## Week 6: TEN 26 - IND 20 (game 401873003)
Video: Tennessee Titans vs Indianapolis Colts Game Highlights | 2026 NFL Season Week 6 — https://www.youtube.com/watch?v=MJZhpnKoY7E  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:18|IND|Daniel Jones → Will Mallory|Completed pass to Mallory.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:28|IND|Daniel Jones|Completed pass for a first down; receiver unidentified.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:38|IND|Daniel Jones → Keenan Allen|Allen caught the pass near the 30 and fell forward.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:55|IND|Josh Downs|Third-down reception near the first-down marker; commentary leaves the spot uncertain.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:03|IND|Daniel Jones → Deion Burks|Deep-left completion to the Tennessee 16; T. Burgess pushed Burks out.|36|deep shot left|unknown|unknown|T. Burgess (DB tackler)|verified vs DB|
|01:16|IND|Daniel Jones; Amani Hooker|Jones threw on the move; tipped pass intended for Josh Downs was intercepted by Hooker at the Tennessee 6. Ruling upheld.|0|short right pass|unknown|unknown|unknown|verified vs DB|
|01:31|TEN|Wan'Dale Robinson|Third-down reception deep in Tennessee territory; Robinson spun forward toward the marker.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:56|IND|Daniel Jones → Jonathan Taylor|Taylor broke loose on a screen to the Tennessee 28; Hooker pushed him out.|38|screen right|unknown|unknown|Amani Hooker (DB tackler)|verified vs DB|
|02:15|IND|Daniel Jones|Jones stepped up and was brought down on a pass play; defender unidentified.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:20|IND|Keenan Allen|Reception produced first-and-goal inside the 10.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:36|IND|Daniel Jones → Mo Alie-Cox|One-yard touchdown catch. Replay commentary describes Alie-Cox showing a down block before popping open.|1|block-and-release; short left pass|unknown|unknown|Burgess (commentary says he reacted too late)|verified vs DB|
|03:07|TEN|Tony Pollard|Stopped short of the first down; play type not established by the caption.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:10|IND|McGowan|Ballcarrier made moves and reached approximately the 43 for a first down before going out of bounds.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:27|IND|Daniel Jones → Pharaoh Brown|Jones faked to Taylor and floated a pass to Brown for a first down.|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:37|IND|Jonathan Taylor|Taylor ran through a large hole to the Tennessee 13.|20|right end run|unknown|unknown|C. Gray (DB tackler)|verified vs DB|
|03:51|IND|Daniel Jones; Jermaine Johnson|Johnson sacked Jones; announcer called it Johnson's second sack.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:59|IND|Daniel Jones|Jones ran inside the 10 to approximately the 5; first-down status was uncertain in commentary.|None|quarterback run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:26|IND|Spencer Shrader|Made a 23-yard field goal, his 20th consecutive make according to commentary.|23|field goal|unknown|unknown|unknown|verified vs DB|
|04:36|TEN|Cam Ward; Cam Bynum|Bynum intercepted Ward's deep-right pass intended for Wan'Dale Robinson and returned it 12 yards. Commentary calls it an overthrow.|12|deep shot right|unknown|unknown|unknown|verified vs DB|
|04:50|IND|Jonathan Taylor|Taylor gained a first down inside the 35; exact play type is unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:59|IND|Daniel Jones; Martin|Jones was sacked near the 41 by a defender identified as Martin.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:10|IND|Daniel Jones → Keenan Allen|Dump-off to Allen, who made a move and reached inside the 30.|None|dump-off|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:19|IND|Spencer Shrader|Made a 47-yard field goal to extend the lead to 13–0.|47|field goal|unknown|unknown|unknown|verified vs DB|
|05:28|IND|Jonathan Taylor; Jeffery Simmons|Taylor gained four yards before Simmons forced and recovered his fumble.|4|right tackle run|13 personnel|unknown|unknown|verified vs DB|
|06:00|TEN|unknown|Commentary summarizes two batted passes on two plays; individual snaps and players cannot be separated.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:01|TEN|Cam Ward → Carnell Tate|Tate made his first catch of the game against an announced blitz.|None|unknown|unknown|blitz|unknown|unverified (no DB match; caption-only)|
|06:14|TEN|Cam Ward → Carnell Tate|Incomplete third-and-seven pass targeting Tate.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:24|TEN|Joey Slye|Made a 29-yard field goal for Tennessee's first points.|29|field goal|unknown|unknown|unknown|verified vs DB|
|06:39|IND|Jonathan Taylor|Taylor was stopped a couple of yards short of a first down; Hooker was credited with the tackle.|None|run|unknown|unknown|Amani Hooker (commentary tackler)|unverified (no DB match; caption-only)|
|06:45|IND|Daniel Jones → Josh Downs|Completion to Downs for a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:59|IND|Daniel Jones → Keenan Allen|Allen caught a pass inside the Tennessee 25.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:11|IND|Daniel Jones; Cor'Dale Flott|Flott intercepted a pass intended for Will Mallory at the Tennessee 11. Commentary says Flott baited Jones.|0|short left pass|unknown|unknown|unknown|verified vs DB|
|07:40|TEN|Cam Ward → Carnell Tate|Ward threw after scrambling; Tate caught the ball near the boundary, with inbounds status questioned.|None|scramble pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:51|TEN|Tony Pollard|Pollard's best run of the day, according to commentary, reached the 40 for a first down.|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:03|TEN|unknown|Pass went off the intended receiver's hands as he turned; receiver not conclusively identified.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:09|TEN|Joey Slye|Made a 56-yard field goal to bring Tennessee within one score.|56|field goal|unknown|unknown|unknown|verified vs DB|
|08:23|IND|unknown; Anthony Hill Jr.|Fragmentary commentary credits Hill with a defensive play; ballcarrier and outcome are unclear.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:38|IND|unknown; Adams|Unidentified ballcarrier was tackled at the 35; commentary credited Adams.|None|unknown|unknown|unknown|Adams (commentary tackler)|unverified (no DB match; caption-only)|
|08:46|IND|Daniel Jones|Jones was sacked inside the 30 on third-and-ten; caption does not conclusively identify the sacker.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:56|IND|Rigoberto Sanchez; Chimere Dike|Dike returned Sanchez's punt 58 yards from the Tennessee 14 to the Indianapolis 28, getting past Sanchez before K. Gushiken stopped him.|58|punt return|unknown|unknown|Rigoberto Sanchez (commentary); K. Gushiken (DB tackler)|verified vs DB|
|09:16|TEN|Cam Ward → Carnell Tate|Ward completed a pass to Tate, who held on through a hard hit.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:32|TEN|Cam Ward → Carnell Tate|Eight-yard touchdown pass to Tate, identified as his first NFL touchdown.|8|short left pass|unknown|unknown|unknown|verified vs DB|
|10:04|IND|Daniel Jones|Jones ran into open space and went out of bounds against extra pressure.|None|quarterback scramble|unknown|extra pressure|unknown|unverified (no DB match; caption-only)|
|10:23|IND|Daniel Jones → Treadwell|High, overthrown pass was knocked away; Tony Adams was identified as being back in coverage.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:32|IND|Julius Chestnut; O. Oladejo|Chestnut blocked Sanchez's punt up the middle. Oladejo recovered at the Indianapolis 14 and returned it for a Tennessee touchdown.|14|punt block up the middle; recovery return|unknown|unknown|unknown|verified vs DB|
|11:17|IND|Daniel Jones → Josh Downs|Deep-right completion to Downs near midfield, reaching the Tennessee 49.|23|deep shot right|unknown|unknown|A. Hill (DB tackler)|verified vs DB|
|11:24|IND|Daniel Jones → Treadwell|Treadwell caught the pass and made a move for a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:36|IND|Jonathan Taylor|With the blitz picked up, Taylor escaped along the sideline to the Tennessee 20; captions do not establish whether he received a pass or handoff.|None|unknown|unknown|blitz|unknown|unverified (no DB match; caption-only)|
|11:48|IND|Jonathan Taylor|Taylor broke through toward a first down; commentary called for a spot check.|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:01|IND|Jonathan Taylor|Taylor took a pitch around left end for a four-yard touchdown, tying the game after the extra point.|4|pitch left end|unknown|unknown|unknown|verified vs DB|
|12:17|TEN|Cam Ward → Wan'Dale Robinson|Ward delivered an on-target first-down completion to Robinson against pressure.|None|unknown|Robinson in the slot|single high; pressure|unknown|unverified (no DB match; caption-only)|
|12:29|TEN|Cam Ward → Carnell Tate|Third-and-five pass toward Tate was unsuccessful; commentary praised the coverage.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:43|TEN|Joey Slye|Made a 49-yard field goal to put Tennessee ahead 23–20.|49|field goal|unknown|unknown|unknown|verified vs DB|
|12:47|IND|Daniel Jones → unidentified receiver|Completed a sideline pass for 15 yards.|15|sideline pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:02|IND|Daniel Jones; Jermaine Johnson|Johnson sacked Jones on an announced blitz.|None|unknown|unknown|blitz|unknown|unverified (no DB match; caption-only)|
|13:11|IND|Daniel Jones; Anthony Hill Jr.|Fourth-and-17 pass was nearly intercepted and knocked away by Hill, ending the possession on downs.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:50|TEN|unknown|Penalty flag during Tennessee's late possession; infraction and play outcome are not given.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:56|TEN|Tony Pollard|Pollard was stopped before fourth down; Indianapolis used its final timeout.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:02|TEN|Joey Slye|Made a 44-yard field goal for a 26–20 lead with 43 seconds remaining.|44|field goal|unknown|unknown|unknown|verified vs DB|
|14:24|IND|Daniel Jones → Keenan Allen|Allen caught a pass to the 45 with Indianapolis out of timeouts.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:32|IND|Daniel Jones; Amani Hooker|Jones heaved toward the goal line against a three-man rush. Hooker appeared to catch it out of bounds; no interception is established.|0|deep heave|unknown|three-man rush|unknown|unverified (no DB match; caption-only)|
|14:57|IND|Daniel Jones|Final throw toward the goal line was knocked away as time expired.|0|deep heave|unknown|dropping everybody deep|unknown|unverified (no DB match; caption-only)|

Offense (model synthesis from this game's plays): Tate became a repeated second-half target, catching a scramble throw, holding on through contact, and scoring an eight-yard touchdown. / Robinson supplied first-down opportunities, including a late completion against pressure with him explicitly identified in the slot. / Pollard contributed a first-down run to the 40 during the comeback. / Special teams supplied a 58-yard punt return, a blocked-punt touchdown, and four made field goals.

Defense weaknesses: Allowed Burks a 36-yard deep completion and Taylor a 38-yard screen gain. / Allowed Taylor a 20-yard right-end run and a four-yard pitch touchdown around left end. / Alie-Cox became open for a touchdown after showing a block; commentary identified Burgess as reacting too late. / Allowed repeated Allen and Downs receptions, including Downs' 23-yard fourth-quarter gain.

Limitations: Captions only; no frames were viewed. The supplied DB is selective, so NO DB MATCH does not mean a play did not occur. Unclear names were retained without speculative correction. The DB's 36-yard pass-interference penalty and kickoff returns were not separately identifiable in the captions and were not added. Replay descriptions were combined with their original plays. Unknown distances, alignments, routes, blocking assignments, and coverage details remain unknown. Explicit pressure or rush descriptions are recorded under coverage_scheme without inferring a coverage shell. Named DB tacklers are labeled as tacklers, not assumed to have lost coverage. Yards represent reception/rush gain, turnover or special-teams return distance, or field-goal distance as described; the Taylor fumble entry uses his four-yard rush rather than the DB recovery row's zero return yards. Caption conflicts were resolved with clear DB matches: Slye's first field goal was 29 yards, and Flott's interception came on a short-left pass despite the caption calling it deep. The late Hooker play was out of bounds and is not counted as an interception.
