# NYJ — Phase 8 film notes (Weeks 1–6, 2026)

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

Offense (Codex synthesis from this game's plays): Cooper turned an underneath third-and-9 completion against an overload blitz into 30 yards. / Smith generated second-half explosive completions to Wilson for 31 and 22 yards and Mitchell for 40. / Hall found interior seams, followed a lead blocker for a first down, and scored on a four-yard left-end run. / Sadiq scored on misdirection; Hall's touchdown came from an explicitly described double-tight-end set. / Wilson retained a first-down catch through Kevin Winston Jr.'s hit.

Defense weaknesses: Ward escaped for a first down with his legs and produced another scramble. / Pollard gained a first down around the edge. / Robinson supplied multiple first-down receptions. / Tennessee finished a late possession with an 11-yard touchdown pass to Ayomanor.

Limitations: Captions only; no frames were viewed and no commands were run. Abrupt edits and transcription errors obscure some players, outcomes, distances and play boundaries. DB matches use the supplied authoritative subset; NO DB MATCH does not mean a play was absent from the full game. DB distances override conflicting captions. Field-goal yards are kick distances; return yards are return distances. Personnel and defensive schemes are included only when explicitly stated in commentary; no coverage shell or man/zone assignment can be established. Named tacklers or nearby defenders are identified as such and are not necessarily defenders beaten in coverage. The opening kickoff penalty and the third-quarter 27-yard return appear only in the DB and are not identifiable in the captions. Extra points are not separately identified in the captions. The 09:45-09:55 passage may splice two plays; the incomplete call and Robinson completion are recorded separately with that uncertainty.


## Week 2: GB 20 - NYJ 17 (game 401872936)
Video: Green Bay Packers vs. New York Jets Game Highlights | NFL 2026 Season Week 2 — https://www.youtube.com/watch?v=Z7OIS7hXV7E  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:14|NYJ|Geno Smith|Escapes initial pressure on third-and-13 but is taken down; Van Ness is mentioned as involved.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:30|GB|Kaleb Johnson|Runs up the middle for a first down on the final play of the first quarter.|None|run up the middle|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:43|GB|Christian Watson|Catches Love's pass for a first down; DB identifies a 20-yard completion deep middle.|20|deep middle pass|unknown|unknown|Dane Belton (DB tackler)|verified vs DB|
|00:51|GB|unknown|Runs up the middle on second-and-five for another first down. Belton is named as the tackler.|None|run up the middle|unknown|unknown|Dane Belton (tackler)|unverified (no DB match; caption-only)|
|01:03|GB|MarShawn Lloyd|Runs for a first down on second-and-seven.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:18|GB|MarShawn Lloyd|Catches Love's short-right pass for a six-yard touchdown. Commentary says his motion confirmed man coverage.|6|receiving-back motion; short right pass|unknown|man coverage|unknown|verified vs DB|
|01:43|NYJ|Garrett Wilson|Makes a sliding 16-yard catch to convert third-and-11.|16|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:54|NYJ|Adonai Mitchell|Catches a 13-yard pass on third-and-nine to set up first-and-goal. Subsequent commentary references repeated one-on-one targeting without identifying the defender.|13|unknown|unknown|one-on-one matchup mentioned; full scheme unknown|unknown|unverified (no DB match; caption-only)|
|02:11|NYJ|Braelon Allen|Scores on a five-yard run around right end. Commentary describes pressing the line to draw defenders inward before going outside.|5|right-end run|unknown|unknown|unknown|verified vs DB|
|02:34|GB|Skyy Moore|Returns the kickoff 43 yards to the GB 46.|43|kickoff return|unknown|unknown|J. Sanders; M. Moore (DB tacklers)|CONFLICT (yardage 43 vs DB)|
|02:48|GB|Bo Melton|Love's pass intended for Melton is incomplete; Green Bay will punt.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:55|NYJ|Adonai Mitchell|Smith initially cannot find anyone, then completes a 14-yard sideline pass to Mitchell on third-and-11.|14|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:14|NYJ|Adonai Mitchell|Catches a swing pass to the 46 for a first down on third-and-five.|None|swing pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:23|NYJ|Geno Smith|Spikes the ball to stop the clock.|0|clock-stopping spike|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:25|NYJ|Williams (first name not stated)|Catches Smith's pass on the final play of the first half.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:43|NYJ|Garrett Wilson|Catches a pass across midfield for a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:48|NYJ|Geno Smith|Faces intense pressure on third-and-nine; commentary names Van Ness and begins naming another defender before cutting away. Final result is not stated.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:59|GB|Jordan Love|Is pressured and hit while throwing incomplete on third-and-nine.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:06|NYJ|Geno Smith|Scrambles for a first down on third-and-four.|None|quarterback scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:21|NYJ|Breece Hall|Takes a toss across midfield for 16 yards before being forced out.|16|toss run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:35|NYJ|Isaiah Williams|Gains 16 yards and a first down. The following commentary contrasts this touch with a subsequent catch, indicating a run, but the exchange is unspecified.|16|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:47|NYJ|Isaiah Williams|Catches a pass over the middle for nine yards.|9|middle pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:57|NYJ|Braelon Allen|Catches a pass from the 19 and is taken down near the 11. A personal foul follows; the captioned endpoint is garbled.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:14|NYJ|Garrett Wilson|Catches a five-yard touchdown pass as Smith faces an impending hit. DB yardage overrides the caption's preceding reference to the six.|5|short right pass|unknown|unknown|unknown|verified vs DB|
|05:40|GB|Christian Watson|Is targeted unsuccessfully on third-and-three. Commentary identifies linebacker Davis underneath and Cisco high.|0|unknown|unknown|Davis underneath with Cisco high; full scheme unknown|unknown|unverified (no DB match; caption-only)|
|05:53|NYJ|Breece Hall|Turns a short-right reception into a 43-yard gain on third-and-12, making multiple moves before Nixon tackles him.|43|short right pass|unknown|unknown|K. Nixon (DB tackler)|verified vs DB|
|06:06|NYJ|Geno Smith|Pulls the ball down and scrambles from the 40 to the 33.|7|quarterback scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:18|NYJ|Geno Smith|Is sacked after the Jets barely get the snap away.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:32|GB|MarShawn Lloyd|Gains two yards running left tackle, then fumbles. DB credits Enagbare with the forced fumble and H. Phillips with the Jets recovery at the GB 18.|2|left-tackle run|unknown|unknown|K. Enagbare; D. Davis (DB tacklers)|verified vs DB|
|06:52|NYJ|unknown|Catches Smith's swing pass on third-and-nine but finishes short of the first down.|None|swing pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:00|NYJ|Jason Sanders|Makes a 32-yard field goal to extend the Jets' lead to 17-7.|32|field goal|unknown|unknown|unknown|verified vs DB|
|07:12|GB|Matthew Golden|Catches an 18-yard pass to the Jets 47 for a first down.|18|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:41|GB|Matthew Golden|Catches another 18-yard pass, reaching the Jets seven on second-and-ten.|18|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:54|GB|Christian Watson|Catches a three-yard touchdown on an inside slant. Commentary says Love waits for the safety to move before throwing.|3|inside slant|unknown|unknown|unknown|verified vs DB|
|08:30|NYJ|Adonai Mitchell|Makes a catch; the captions cut off before specifying the gain or result.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:42|NYJ|Isaiah Williams|Catches Smith's pass; the final result is cut off. Pre-snap commentary describes Evan Williams showing blitz and backing out.|None|unknown|unknown|Evan Williams shows blitz and drops out; full scheme unknown|unknown|unverified (no DB match; caption-only)|
|08:52|GB|Skyy Moore|Returns a punt 63 yards to the Jets 19, setting up the tying field-goal possession.|63|punt return|unknown|unknown|A. Smith (DB tackler)|verified vs DB|
|09:16|GB|Christian Watson|Love rolls right and targets Watson from the Jets 16; Thomas knocks the pass away.|0|rollout right|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:27|GB|Trey Smack|Makes a 34-yard field goal to tie the game at 17.|34|field goal|unknown|unknown|unknown|verified vs DB|
|09:41|NYJ|Garrett Wilson|Makes a catch with two flags thrown. Subsequent commentary mentions interference involving Mitchell, but the penalty disposition is unavailable.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:01|NYJ|Garrett Wilson|Catches a second-and-ten pass and is tackled two yards short of the first down.|8|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:10|NYJ|Braelon Allen|Is stuffed on a late short-yardage attempt. Commentary credits Green Bay with stops on both third and fourth down, but only one attempt is individually narrated.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:30|GB|Jordan Love|Is taken down. Commentary mentions two safeties and Cisco in the end zone before the snap; the tackler's name is cut off.|None|unknown|unknown|two safeties mentioned; full scheme unknown|unknown|unverified (no DB match; caption-only)|
|10:37|NYJ|Sadiq (as captioned)|Catches a short pass on third-and-30 in overtime and is tackled at the 22 after starting from the 10; the Jets will punt.|12|short pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:54|GB|Brooks (first name not stated)|Catches a swing pass for a first down inside the Jets 40 and makes two defenders miss. Jarvis Brownlee's late hit adds 15 penalty yards. The same play is repeated at 11:09.|None|swing pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:46|GB|Matthew Golden|Love lofts a pass toward Golden, who is knocked out of bounds by Cisco. The captions do not explicitly establish a completed catch.|None|lofted pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:56|GB|Trey Smack|Makes the winning 26-yard field goal in overtime for a 20-17 final.|26|field goal|unknown|unknown|unknown|verified vs DB|

Offense (Codex synthesis from this game's plays): Smith repeatedly converts third downs through Wilson and Mitchell and adds a third-and-four scramble conversion. / Hall supplies a 16-yard toss run and a 43-yard catch-and-run. / Isaiah Williams produces a 16-yard touch followed by a nine-yard reception. / Allen presses the line before going outside for his rushing touchdown; Smith delivers Wilson's touchdown while facing pressure.

Defense weaknesses: Concedes multiple rushing first downs on Green Bay's opening touchdown drive and Lloyd's touchdown against explicitly identified man coverage. / Allows two 18-yard Golden receptions during the fourth-quarter touchdown drive. / Safety movement opens space for Watson's three-yard touchdown slant. / Allows Brooks' overtime swing-pass conversion; Brownlee's late hit adds 15 yards.

Limitations: Captions only; no frames were viewed. Distinct identifiable plays are listed once, including the Brooks play repeated at 11:09. The supplied DB is selective, so NO DB MATCH does not establish that a play was absent from the full game. DB-only highlights without identifiable caption narration are omitted. Formation is unknown throughout because commentators do not explicitly identify a personnel package or formation; DB shotgun labels are not used for that field. Full coverage schemes, most routes, blocking assignments, and defenders actually beaten cannot be determined. Named DB tacklers are labeled as tacklers, not evidence they were beaten. Other named defenders who successfully defend plays are retained in descriptions. Null yardage indicates uncertainty; field-goal yardage is kick distance, and return yardage is return distance. Some gains are derived from explicitly narrated field positions or down-and-distance. Truncated names and outcomes remain unresolved where no clear DB match exists. The supplied fumble row's event label and team conflict with its narrative; the narrative establishes a GB offensive fumble recovered by NYJ.


## Week 3: NYJ 24 - DET 31 (game 401872954)
Video: New York Jets vs. Detroit Lions Game Highlights | NFL 2026 Season Week 3 — https://www.youtube.com/watch?v=xsJzYyK4mGE  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 4: NYJ 12 - CHI 23 (game 401872972)
Video: New York Jets vs. Chicago Bears Game Highlights | NFL 2026 Season Week 4 — https://www.youtube.com/watch?v=IlcC1zFWyVw  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 5: CLE 12 - NYJ 17 (game 401872983)
Video: Cleveland Browns vs New York Jets Game Highlights | 2026 NFL Season Week 5 — https://www.youtube.com/watch?v=p_DHFA3Sfys  | captions: yes

_No Codex film notes (no captions or run not completed)._


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

Offense (Codex synthesis from this game's plays): Play-action produced completions to Taylor and Cooper, including Cooper's 48-yard touchdown on a rollout. / Allen reached the second level and broke an initial tackle on consecutive runs; Davis also gained around the edge. / Cooper supplied the touchdown, a contested crossing completion against Marcus Jones, and an 18-yard late underneath gain.

Defense weaknesses: The three-man rush gave Maye extended time on Doubs's 42-yard touchdown; commentary also linked Douglas's touchdown to insufficient pass rush. / Safety movement opened space on Doubs's touchdown, and linebacker-safety communication failed on Henry's touchdown. / A corner blitz left Henry with substantial space on a late third-and-long completion. / Late Kiner runs gained 13 and nine yards, including a slipped tackle, while New England drained the clock.

Limitations: Analysis uses only supplied captions and DB excerpts; no frames or external sources were accessed. The DB is selective, so NO DB MATCH does not mean a play did not occur. DB matches identify the supplied quarter/clock entry; formation and coverage fields use commentary only. Names on unmatched plays remain as supported by captions, including uncertain renderings. Named tacklers, sackers, and takeaway defenders are labeled by role and are not necessarily defenders beaten in coverage. Null yards indicate an unstated or ambiguous gain; field-goal yards are kick distance. The Douglas fumble entry uses the 39-yard offensive reception, with the 20-yard defensive return described separately. Kickoffs absent from the captions, the isolated unclear penalty reference, replay explanations, and the unrelated bonus-coverage fragment were not treated as additional plays.
