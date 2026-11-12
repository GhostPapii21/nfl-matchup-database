# ARI — Phase 8 film notes (Weeks 1–6, 2026)
> Note: games 401872943, 401872958, 401872966, 401872991 were extracted by Grok via the xAI API (grok-4.20-0309-non-reasoning, same prompt/schema as Codex, cleaned captions); sidecar provenance in film/grok_meta/. All other games with notes: Codex.

Method: NFL YouTube channel full-game highlight videos were located by search and their auto-captions (broadcast commentary) downloaded via yt-dlp. Codex (codex-cli 0.163.0) extracted plays from the captions. **No video frames were viewed by any agent.** Each play was checked against the repo DB play-by-play: `verified vs DB` means the cited DB play exists and the yardage matches. Personnel, formation and coverage appear only when commentators stated them; everything else is `unknown`.


## Week 1: ARI 26 - LAC 14 (game 401872926)
Video: Arizona Cardinals vs. Los Angeles Chargers Game Highlights | NFL 2026 Season Week 1 — https://www.youtube.com/watch?v=UKqM7fT42uk  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:25|ARI|T.McBride|Brissett completes an acrobatic catch to McBride at the Chargers 43.|27|deep right pass|unknown|Commentary says coverage rotates toward McBride; specific scheme unknown.|E.Molden (DB tackler)|verified vs DB|
|00:41|ARI|J.Brissett|Quarterback carries for a first down to the 19.|None|quarterback run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:49|ARI|Kendrick Bourne|Bourne catches a pass on the wing near the first-down marker.|None|unknown|unknown|unknown|Hart (in on tackle)|unverified (no DB match; caption-only)|
|01:00|ARI|J.Love|Love takes an intended inside run outside and stiff-arms Hart while scoring.|5|left-end run; commentary says intended inside|unknown|unknown|Hart|verified vs DB|
|01:35|LAC|Ladd McConkey|McConkey makes a catch on a knee at the 45 among defenders.|19|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:54|LAC|L.McConkey|Downfield completion to the Arizona 34; captions call it 24 yards, DB records 23.|23|deep middle pass|unknown|nickel secondary|B.Baker (tackler)|verified vs DB|
|02:08|LAC|Ladd McConkey|McConkey catches a pass and works to the 15 before Baker tackles him.|19|unknown|unknown|unknown|Budda Baker (tackler)|unverified (no DB match; caption-only)|
|02:18|LAC|O.Hampton|Hampton powers through converging defenders for a touchdown; captions say nine yards, DB records eight.|8|run up the middle|unknown|unknown|unknown|verified vs DB|
|02:46|ARI|Kendrick Bourne|Quick completion in front of Derwin James gains a first down at the 41.|10|quick pass|unknown|unknown|Derwin James|unverified (no DB match; caption-only)|
|03:01|ARI|Trey McBride|McBride catches a pass on first-and-20 and carries defenders to the 47.|16|unknown|unknown|unknown|Henley (tackler)|unverified (no DB match; caption-only)|
|03:18|ARI|Trey McBride|Brissett finds McBride as a safety valve with Khalil Mack pressuring him; first down at the 42.|10|safety-valve pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:33|ARI|Wilson (intended receiver)|Third-down pass toward the 5 is knocked away with Cam Hart in coverage.|0|unknown|unknown|unknown|Cam Hart (successful coverage)|unverified (no DB match; caption-only)|
|03:50|ARI|C.Ryland|Misses a 54-yard field goal; DB specifies the right upright.|54|field goal|unknown|unknown|unknown|verified vs DB|
|04:05|LAC|Njoku|Tight end catches a pass and runs down the sideline toward the 30.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:15|LAC|O.Hampton|Hampton fumbles on a left-end run. DB identifies Wingard forcing the fumble and W.Johnson recovering for Arizona.|-1|left-end run|unknown|unknown|Wilson (caption says Hampton got past him); A.Wingard (forced fumble)|verified vs DB|
|04:39|ARI|Jeremiyah Love|Love bursts into the secondary for a first down.|21|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:50|ARI|Jacoby Brissett|Quarterback sneak gains a first down near the 8; nearby caption fragments give inconsistent field positions.|None|quarterback sneak|unknown|unknown|James (tackler)|unverified (no DB match; caption-only)|
|05:04|ARI|Kendrick Bourne|Brissett completes a pass down the middle against a five-man rush on third-and-8.|12|pass down the middle|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:17|ARI|Jacoby Brissett|Pass is knocked away and ruled incomplete; Tuipulotu is mentioned, but his precise involvement is unclear.|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:32|ARI|C.Ryland|Makes a 27-yard field goal for a 10-7 lead; commentary corrects its initial 26-yard call.|27|field goal|unknown|unknown|unknown|verified vs DB|
|05:46|LAC|Ladd McConkey|Herbert completes a sharply thrown pass to McConkey.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:58|LAC|O.Gadsden|Quick throw left becomes a long catch-and-run; captions say 25 yards to the 22, DB records 26 to the 21.|26|short left pass; catch-and-run|unknown|unknown|A.Wingard (DB tackler)|verified vs DB|
|06:14|LAC|Mitchell|Fragment describes Mitchell outside on first-and-10; result is omitted.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:25|LAC|Justin Herbert|Dante Stills sacks Herbert on fourth-and-goal, ending the possession.|None|dropback pass attempt|unknown|unknown|Dante Stills (sacker)|unverified (no DB match; caption-only)|
|06:35|ARI|Trey McBride|Quick completion up the middle; McBride hurdles toward the 35.|None|quick pass up the middle|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:45|ARI|Wilson|Completion from the Chargers 32 near the first-down marker at the 22; commentary ultimately awards a first down.|None|unknown|unknown|unknown|Jackson (coverage)|unverified (no DB match; caption-only)|
|06:57|ARI|Kendrick Bourne|Underneath completion gains 11 to the 11 with 15 seconds remaining.|11|underneath pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:10|ARI|Harrison (intended receiver)|High end-zone pass is incomplete; a flag is mentioned without its ruling.|0|end-zone pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:28|ARI|C.Ryland|Makes a 44-yard field goal as the half expires for a 13-7 lead.|44|field goal|unknown|unknown|unknown|verified vs DB|
|07:45|LAC|Hampton|Runs outside for six yards and a first down near the 36.|6|outside run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:00|LAC|Tre' Harris (intended receiver)|Third-and-5 pass falls incomplete with Max Melton covering; Chargers bring on the punt unit.|0|timing route|unknown|unknown|Max Melton (successful coverage)|unverified (no DB match; caption-only)|
|08:18|ARI|M.Harrison|Harrison wins a contested sideline catch against Hart. DB records 33 yards; later commentary says 34.|33|deep left pass|unknown|nickel secondary|C.Hart|verified vs DB|
|08:30|ARI|Kendrick Bourne|Completion to Bourne reaches the Chargers 42; Molden tackles him.|None|unknown|unknown|unknown|Molden (tackler)|unverified (no DB match; caption-only)|
|08:46|ARI|Wilson|Pass in front of Tarheeb Still gains 17 to the Chargers 25.|17|unknown|unknown|unknown|Tarheeb Still|unverified (no DB match; caption-only)|
|08:57|ARI|Allgeier|Run behind a Gaines block gains a first down; captions say 10 yards and the 14-yard line.|10|unknown|unknown|unknown|Caldwell (tackler)|unverified (no DB match; caption-only)|
|09:09|ARI|Jacoby Brissett|Pass down the middle against a four-man rush is deflected by Derwin James; intended receiver is omitted.|0|pass down the middle|unknown|unknown|Derwin James (pass breakup)|unverified (no DB match; caption-only)|
|09:24|ARI|C.Ryland|Makes a 34-yard field goal.|34|field goal|unknown|unknown|unknown|verified vs DB|
|09:32|LAC|T.Harris (intended receiver)|Deep play-action pass draws defensive pass interference on Max Melton for 48 yards; no completed pass.|48|play-action; deep left pass; outside double move|Harris aligned outside|unknown|M.Melton (defensive pass interference)|CONFLICT (yardage 48 vs DB)|
|10:00|LAC|L.McConkey|McConkey catches an outside throw and reaches around the pylon for a touchdown.|8|short right pass|unknown|unknown|unknown|verified vs DB|
|10:27|ARI|unknown receiver|Short completion on third-and-5 is stopped short by Hart; receiver identification is cut off.|None|short pass|unknown|unknown|Hart (tackler)|unverified (no DB match; caption-only)|
|10:38|LAC|Johnston (intended receiver)|Herbert throws low and incomplete with Will Johnson among the defenders.|0|unknown|unknown|unknown|Will Johnson (coverage)|unverified (no DB match; caption-only)|
|10:49|LAC|J.Scott|Arizona blocks Scott's punt. DB identifies S.Fehoko as blocker and A.Ingold recovering for LAC at its 3; captions say the 2.|0|punt block|unknown|unknown|unknown|verified vs DB|
|11:05|ARI|T.McBride|McBride works outside, rubbing past a Chargers defender, and beats Derwin James for a touchdown.|3|short left pass; outside release with described rub|unknown|one-on-one matchup with James|Derwin James|verified vs DB|
|11:36|LAC|Johnston|Fragment describes Johnston outside being shoved out of bounds by Burch; play type and gain are omitted.|None|unknown|unknown|unknown|Burch (tackler)|unverified (no DB match; caption-only)|
|11:46|LAC|Njoku|Catches a pass deflected at the line and runs through contact to the 40 for a first down.|14|deflected pass; catch-and-run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:06|LAC|J.Herbert|Deep pass intended for D.Davis is intercepted by A.Wingard at the Arizona 5 with no return. Offensive holding is declined.|0|deep right pass|unknown|unknown|A.Wingard (interceptor)|verified vs DB|
|12:21|ARI|Trey McBride|Brissett beats a five-man rush with a completion to McBride in front of James, converting a first down at the 17.|None|unknown|unknown|unknown|James|unverified (no DB match; caption-only)|
|12:30|ARI|Jacoby Brissett|After a fake with Love present, Brissett runs while Henley pursues; Troy Dye stops him short of a first down.|None|fake followed by quarterback run|unknown|unknown|Henley (pursuit); Troy Dye (tackler)|unverified (no DB match; caption-only)|
|12:42|LAC|Njoku|Herbert is flushed against a four-man rush and completes underneath to Njoku, who is knocked out of bounds.|None|underneath pass|unknown|unknown|Denzel Burke (tackler)|unverified (no DB match; caption-only)|
|12:52|LAC|Njoku|Fourth-down completion is short of the required 41-yard line; a flag follows, but its ruling is omitted.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:05|ARI|Allgeier|Third-and-5 handoff gains three yards.|3|handoff run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:19|ARI|C.Ryland|Makes a 49-yard field goal to extend Arizona's lead to 26-14.|49|field goal|unknown|unknown|unknown|verified vs DB|
|13:34|LAC|Harris|Catches a pass in front of Budda Baker just before the two-minute warning.|None|unknown|unknown|unknown|Budda Baker|unverified (no DB match; caption-only)|
|13:45|LAC|Gadsden|Fourth-and-7 completion is stopped short by Wilson, turning possession over on downs.|None|unknown|unknown|unknown|Wilson (tackler)|unverified (no DB match; caption-only)|

Offense (model synthesis from this game's plays): McBride supplied the opening 27-yard gain, repeated chain-moving catches, a pressure outlet against Mack, and the 3-yard touchdown against James. / Bourne repeatedly produced quick or underneath completions, including gains of 10, 12 and 11 yards. / Harrison's contested 33-yard catch and Wilson's 17-yard reception supplied downfield gains on a second-half scoring drive. / Love scored by taking an intended inside run outside and later produced a caption-reported 21-yard burst. / Brissett converted with quarterback sneaks and completed passes against explicitly described five-man rushes.

Defense weaknesses: McConkey repeatedly found receiving space on the opening Chargers drive, with caption-reported gains of 19 and 19 around the DB-confirmed 23-yard completion. / Hampton powered through multiple converging defenders on his 8-yard touchdown. / Gadsden turned a short left completion into 26 yards. / Max Melton conceded a 48-yard pass-interference penalty against Harris on a deep play-action attempt. / McConkey reached the pylon on an 8-yard touchdown reception.

Limitations: Captions only; no frames were available. The supplied DB is a selected-play list, so NO DB MATCH does not establish that a play was absent from the full game record. DB values take precedence for clearly matched plays; unmatched gains and names remain caption-derived. The 21-yard Love run is caption-reported but absent from the supplied DB despite its stated threshold. Some fragments omit receivers, results, penalty rulings or reliable field positions. Kickoffs and DB-only pass-interference plays were not added without identifiable caption action. Field-goal yards are kick distances; the Harris penalty's 48 yards are enforcement yards; the interception's zero yards are return yards. Named defenders include tacklers and successful defenders, explicitly labeled where applicable, and do not necessarily indicate someone was beaten. Personnel packages, route details, run gaps and coverage schemes cannot generally be established; nickel refers only to the explicitly announced defensive package. No shotgun designation was imported from DB text because formation required explicit commentary.


## Week 2: SEA 31 - ARI 7 (game 401872943)
Video: Seattle Seahawks vs. Arizona Cardinals Game Highlights | NFL 2026 Season Week 2 — https://www.youtube.com/watch?v=_k-w90zF8t4  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:53|SEA|J.Smith-Njigba|D.Lock pass deep right to J.Smith-Njigba for 82 yards, TOUCHDOWN|82|deep shot|unknown|quarters|unknown|verified vs DB|
|02:54|ARI|T.McBride|J.Brissett pass short left to T.McBride for 2 yards, TOUCHDOWN|2|unknown|unknown|unknown|unknown|verified vs DB|
|03:45|SEA|R.Shaheed|D.Lock pass short middle to R.Shaheed to SEA 49 for 23 yards|23|unknown|unknown|unknown|unknown|verified vs DB|
|04:00|SEA|J.Price|(Shotgun) J.Price up the middle to ARZ 45 for 2 yards. FUMBLES, RECOVERED by ARZ-Z.Collins at ARZ 47|2|unknown|unknown|unknown|Z.Collins|verified vs DB|
|06:48|SEA|J.Price|J.Price right end to ARZ 7 for 25 yards|25|right end|unknown|unknown|unknown|verified vs DB|
|07:01|SEA|J.Smith-Njigba|(Shotgun) D.Lock pass short middle to J.Smith-Njigba for 7 yards, TOUCHDOWN|7|unknown|unknown|unknown|unknown|verified vs DB|
|07:35|ARI|Mi.Wilson|(Shotgun) J.Brissett pass deep left intended for Mi.Wilson INTERCEPTED by J.Love at ARZ 44|0|deep shot|unknown|unknown|unknown|verified vs DB|
|08:20|SEA|J.Myers|J.Myers 33 yard field goal is GOOD|33|unknown|unknown|unknown|unknown|verified vs DB|
|09:59|SEA|J.Smith-Njigba|(Shotgun) D.Lock pass short middle to J.Smith-Njigba for 12 yards, TOUCHDOWN|12|unknown|unknown|unknown|B.Baker|verified vs DB|
|11:31|SEA|A.Barner|Direct snap to A.Barner. A.Barner up the middle for 1 yard, TOUCHDOWN|1|unknown|unknown|unknown|unknown|verified vs DB|

Offense (model synthesis from this game's plays): Red zone efficiency with TDs to T.McBride / Ability to convert first downs on short runs and passes / Explosive kickoff returns

Defense weaknesses: Poor coverage on deep passes allowing big TDs to J.Smith-Njigba / Frequent missed tackles and inability to stop runs in red zone / Susceptible to turnovers including interceptions and fumble recoveries against

Limitations: Could not determine specific personnel formations, most coverage schemes, or exact run gaps/directions beyond what was explicitly stated; many plays in captions lacked sufficient detail for full matching or concept identification; some name corrections applied from DB where matches were clear but auto-captions were inconsistent.


## Week 3: ARI 30 - SF 36 (game 401872958)
Video: Arizona Cardinals vs. San Francisco 49ers Game Highlights | NFL 2026 Season Week 3 — https://www.youtube.com/watch?v=7ngu-tT0PQs  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:20|SF|D.Samuel|Deebo Samuel breaks a tackle and runs for a touchdown on a lateral after a short pass|80|screen|unknown|unknown|unknown|verified vs DB|
|00:50|ARI|M.Harrison|Brissett pass toward Marvin Harrison Jr. on a jump ball, incomplete but a flag is thrown|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:09|SF|C.McCaffrey|McCaffrey up the gut for a first down|5|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:21|SF|C.McCaffrey|Purdy to McCaffrey on a first down, bouncing off first contact|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:32|SF|J.Watkins|Purdy pass over the middle to Jordan Watkins who runs after the catch|26|unknown|unknown|unknown|unknown|verified vs DB|
|01:55|SF|M.Evans|Purdy pass down the sideline to Mike Evans for a touchdown|23|deep shot|unknown|unknown|D.Burke|verified vs DB|
|02:21|ARI|E.Higgins|Brissett flushed and throws to Higgins on the sideline who takes a big hit|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:33|ARI|M.Harrison|Brissett to Marvin Harrison for a first down catch|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:43|ARI|T.McBride|Brissett to Trey McBride for a first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:01|ARI|M.Wilson|Brissett to Michael Wilson down to the 10 yard line, first and goal|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:07|ARI|J.Love|Brissett to Jeremiyah Love, tackled by Dre Greenlaw with nowhere to go|None|unknown|unknown|unknown|D.Greenlaw|unverified (no DB match; caption-only)|
|03:28|ARI|C.Ryland|26-yard field goal by Chad Ryland is good|26|unknown|unknown|unknown|unknown|verified vs DB|
|03:41|SF|M.Evans|Purdy to Mike Evans with a catch on a play with a flag down that stands as a first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:50|SF|unknown|Purdy pass over the middle nearly intercepted by Andrew Wingard|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:16|ARI|M.Wilson|Brissett to Michael Wilson on the sideline|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:33|ARI|M.Wilson|Diving catch by Michael Wilson|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:01|ARI|C.Ryland|41-yard field goal by Ryland is good|41|unknown|unknown|unknown|unknown|verified vs DB|
|05:20|SF|J.Watkins|Purdy to Jordan Watkins down the sideline close to field goal range|34|unknown|unknown|unknown|Ma.Wilson|verified vs DB|
|05:43|SF|E.Pineiro|57-yard field goal by Pineiro is good|57|unknown|unknown|unknown|unknown|verified vs DB|
|06:00|SF|G.Kittle|Purdy to George Kittle over the middle|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:12|SF|G.Kittle|Kittle with the catch and breaking tackles|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:24|SF|C.McCaffrey|Purdy hits McCaffrey who bounces off contact|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:35|SF|C.McCaffrey|McCaffrey up the middle for a rushing touchdown|1|run|unknown|unknown|unknown|verified vs DB|
|07:16|ARI|E.Higgins|Brissett on the roll to Higgins who gets a first down|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:29|ARI|T.McBride|Brissett finds McBride on the run|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:43|ARI|M.Wilson|Brissett to Michael Wilson who converts for a first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:52|ARI|J.Love|Pitch to Jeremiyah Love who gets a first down|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:09|ARI|M.Wilson|Michael Wilson to the goal line for an Arizona touchdown|5|unknown|unknown|unknown|unknown|verified vs DB|
|09:15|ARI|J.Love|Jeremiyah Love with the catch for a touchdown|1|unknown|unknown|unknown|unknown|verified vs DB|
|10:38|SF|D.Samuel|Swing to Deebo Samuel who breaks a tackle for a first down|None|screen|unknown|unknown|M.Wilson|unverified (no DB match; caption-only)|
|10:48|SF|G.Kittle|George Kittle diving into the end zone for a touchdown|10|unknown|unknown|unknown|B.Browning|verified vs DB|
|11:14|ARI|M.Harrison|Brissett to Marvin Harrison Jr. for a big gain|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:09|ARI|J.Brissett|Brissett sneaks toward the end zone for a touchdown (with penalty)|1|run|unknown|unknown|unknown|verified vs DB|
|12:34|SF|C.McCaffrey|Purdy to McCaffrey for a catch and first down|11|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:46|SF|C.McCaffrey|McCaffrey runs for a first down riding the wave of blockers|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:59|SF|B.Purdy|Purdy runs for a first down|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:07|SF|B.Purdy|Purdy runs for a touchdown (called back due to penalty)|None|run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:25|SF|G.Kittle|Purdy to George Kittle for a touchdown|20|play-action|unknown|unknown|unknown|verified vs DB|
|14:03|ARI|T.McBride|Brissett finds McBride|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:17|ARI|J.Love|Brissett to Jeremiyah Love for a first down|8|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:26|ARI|M.Wilson|Brissett to Michael Wilson with the catch|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:45|ARI|C.Ryland|49-yard field goal by Ryland is good|49|unknown|unknown|unknown|unknown|verified vs DB|

Offense (model synthesis from this game's plays): Red zone efficiency with multiple passing and rushing touchdowns / Effective use of motion and play design to create mismatches in the red zone / Ability to convert on third and fourth downs / Diverse receiving threats including Michael Wilson, Trey McBride, and Marvin Harrison Jr.

Defense weaknesses: Susceptible to big plays in the passing game allowing long receptions and touchdowns / Missed tackles in open field against runners like Deebo Samuel and Christian McCaffrey / Vulnerable to play-action and deep shots from Purdy / Red zone defense allowing multiple short-yardage touchdowns

Limitations: Cannot determine exact personnel, formations, or coverage schemes as they are not explicitly stated by commentators. Many plays in captions lack specific yardage or do not perfectly align with DB entries. Some player names were corrected using DB where matches were clear (e.g. Mike Evans to M.Evans, Jordan Watkins to J.Watkins). Several described plays had no direct DB match. Defender beaten only listed when named.


## Week 4: ARI 24 - NYG 36 (game 401872966)
Video: Arizona Cardinals vs. New York Giants Game Highlights | NFL 2026 Season Week 4 — https://www.youtube.com/watch?v=OdvCc-cxRz4  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:35|ARI|M.Wilson|Pass complete to Michael Wilson|17|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:59|ARI|M.Harrison|Fade pass to the end zone caught by Marvin Harrison Jr for touchdown|12|unknown|unknown|unknown|unknown|verified vs DB|
|01:26|NYG|M.Nabers|Pass caught by Malik Nabers on 3rd and 6|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:39|NYG|M.Nabers|Pass to Nabers on 3rd and 6|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:52|NYG|Skattebo|Skattebo loses yardage|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:58|NYG|D.Zvada|39-yard field goal is good|39|unknown|unknown|unknown|unknown|verified vs DB|
|02:09|ARI|M.Wilson|Play action pass caught by Wilson|20|play-action|unknown|unknown|unknown|verified vs DB|
|02:21|ARI|J.Love|Love bounces off initial tackler|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:45|ARI|T.Allgeier|Pitch play, first down for Cardinals|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:01|ARI|T.Allgeier|Run by Allgeier for touchdown, 22-yard sprint|22|left tackle|unknown|unknown|unknown|verified vs DB|
|03:16|NYG|T.Tracy|Run by Tyrone Tracy Jr up the sideline to Cardinals 45|55|unknown|unknown|unknown|K.Clark|CONFLICT (yardage 55 vs DB)|
|03:29|NYG|N.Harris|Run by Harris for 9 yards|9|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:51|NYG|I.Likely|Pass to Likely|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:56|NYG|D.Zvada|Field goal attempt|50|unknown|unknown|unknown|unknown|verified vs DB|
|04:06|ARI|M.Harrison|Pass to Harrison|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:12|ARI|J.Brissett|Pass intercepted by Newsome|0|unknown|unknown|unknown|A.Reese|verified vs DB|
|04:39|ARI|J.Brissett|Pass complete to Reese|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:09|NYG|J.Winston|Play action, flushed out of pocket|None|play-action|unknown|unknown|L.J.Collier|unverified (no DB match; caption-only)|
|05:34|NYG|I.Likely|Misdirection play action, one-handed catch by Likely|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:50|NYG|M.Fields|Pass caught for touchdown by Malachi Fields|12|unknown|unknown|unknown|unknown|verified vs DB|
|06:29|NYG|M.Nabers|Pass over the middle to Nabers for touchdown|25|unknown|unknown|unknown|D.Stills|verified vs DB|
|06:45|ARI|J.Brissett|Giants defense gets to Brissett|None|unknown|unknown|unknown|C.J.Okoe|unverified (no DB match; caption-only)|
|06:59|ARI|J.Love|Bobble for Love, going backwards|None|unknown|unknown|unknown|A.Reese|unverified (no DB match; caption-only)|
|07:05|NYG|Skattebo|Skattebo first down, forced out of bounds|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:18|NYG|J.Winston|Winston's pass intercepted by Denzell Burke|0|unknown|unknown|unknown|D.Stills|verified vs DB|
|07:41|ARI|M.Wilson|Pass to Wilson for 24 yards|24|unknown|unknown|unknown|G.Newsome|verified vs DB|
|07:48|ARI|C.Ryland|60-yard field goal is good|60|unknown|unknown|unknown|unknown|verified vs DB|
|08:01|NYG|J.Winston|Winston's pass picked by Baker|-3|unknown|unknown|unknown|unknown|verified vs DB|
|09:15|NYG|M.Nabers|Pass complete to Nabers for 28 yards|28|unknown|unknown|unknown|M.Melton|verified vs DB|
|09:38|NYG|M.Fields|Pass caught by Malachi Fields for 40 yards|40|unknown|unknown|unknown|W.Williams|verified vs DB|
|10:07|NYG|D.Zvada|34-yard field goal nullified by penalty, defensive holding|34|unknown|unknown|unknown|D.Stills|verified vs DB|
|10:23|NYG|T.Johnson|Pass to Theo Johnson for touchdown|11|unknown|unknown|unknown|unknown|verified vs DB|
|11:20|NYG|I.Likely|Pass to Likely|34|unknown|unknown|unknown|B.Baker|verified vs DB|
|11:32|NYG|N.Harris|Fumble by Harris recovered by Arizona|0|unknown|unknown|unknown|Ma.Wilson|verified vs DB|
|12:10|NYG|C.Jones|Return by Charlie Jones|23|unknown|unknown|unknown|unknown|verified vs DB|
|13:30|NYG|Skattebo|Run by Skattebo for big first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:52|NYG|D.Zvada|52-yard field goal is good|52|unknown|unknown|unknown|unknown|verified vs DB|
|15:52|ARI|J.Brissett|Pass intercepted by Deonte Banks returned 98 yards for touchdown|98|unknown|unknown|unknown|unknown|verified vs DB|

Offense (model synthesis from this game's plays): Effective running game off tackle with pulling center / Big plays from deep passes and explosive runs / Ability to convert long field goals

Defense weaknesses: Susceptible to big passing plays over the middle and deep / Multiple interceptions thrown by QB / Defensive penalties in crucial situations

Limitations: Could not determine specific concepts like exact run gaps, personnel formations, or coverage schemes because they were not explicitly stated by commentators or clearly shown in DB text. Many plays in captions did not have exact matches in the provided DB play-by-play. Some player names were corrected using DB where matches were clear. Yards sometimes approximated from context when not explicit.


## Week 5: DET 45 - ARI 21 (game 401872991)
Video: Detroit Lions vs. Arizona Cardinals Game Highlights | NFL 2026 Week 5 — https://www.youtube.com/watch?v=a7ixKMcIHHs  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:24|DET|J.Goff|Goff pressured and sacked on 3rd and 5|None|unknown|unknown|unknown|B.Baker|unverified (no DB match; caption-only)|
|00:40|ARI|J.Brissett|Brissett pass to tight end (McBride) for first down|11|unknown|3 tight ends|unknown|unknown|unverified (no DB match; caption-only)|
|00:54|ARI|J.Brissett|Play action, Brissett short pass to E.Higgins for first down|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:08|ARI|J.Brissett|Brissett pass over the middle to K.Bourne for 22 yards and first down|22|unknown|unknown|unknown|unknown|verified vs DB|
|01:19|ARI|Mi.Wilson|3rd and 6, caught by Wilson, spins away from Reed for 8 yards and first down|8|unknown|unknown|unknown|D.Reed|unverified (no DB match; caption-only)|
|01:34|ARI|Mi.Wilson|End around to Wilson, laterals to Brissett who runs to the 2|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:44|ARI|T.Quitoriano|Brissett play action pass to Quitoriano for 2 yard TD|2|play-action|unknown|unknown|unknown|verified vs DB|
|02:18|DET|J.Goff|Goff pass over the middle to S.LaPorta for huge first down (flag thrown)|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:33|DET|J.Gibbs|Gibbs rushes on first down, sifts through defense to the 4|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:44|DET|J.Gibbs|Gibbs handoff on 2nd and goal for 1 yard rushing TD|1|unknown|unknown|unknown|unknown|verified vs DB|
|03:07|ARI|J.Brissett|Brissett pass over the middle incomplete, secondary looks for flag|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:16|ARI|A.St. Brown|Amon-Ra St. Brown returns punt from 17, finds space but fumbles at the 47 (recovered by DET)|31|unknown|unknown|unknown|unknown|verified vs DB|
|03:34|DET|J.Goff|3rd and 12, Goff checks short to LaPorta who breaks tackle for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:50|DET|J.Goff|Play action, Goff to wide open S.LaPorta for TD|38|play-action|unknown|unknown|unknown|verified vs DB|
|04:18|ARI|J.Brissett|3rd and 3, Brissett pass to J.Brooks incomplete|None|unknown|unknown|unknown|R.McCreary|unverified (no DB match; caption-only)|
|04:28|DET|J.Gibbs|6th OL in, Gibbs to B.Wright for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:46|DET|J.Gibbs|Gibbs on first down bursts for 17 yards behind B.Wright|17|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:00|DET|J.Goff|4th and 4, Goff to J.Williams for 8 yard TD|8|unknown|unknown|unknown|B.Baker|verified vs DB|
|05:30|ARI|K.Bourne|Connection with K.Bourne for 8 yards|8|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:36|ARI|E.Higgins|E.Higgins for 6 yards on 3rd and short|6|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:37|ARI|J.Brissett|Brissett sacked on 3rd and short, pressure from D.J. Wonnum|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:52|DET|A.St. Brown|Quick toss to St. Brown for first down|None|screen|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:04|DET|J.Gibbs|Razzle-dazzle, pitch to Gibbs who runs for 18 yards|18|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:17|DET|J.Gibbs|Gibbs on 3rd down stopped short of first down at 23|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:31|DET|J.Bates|Bates 46 yard field goal is good|46|unknown|unknown|unknown|unknown|verified vs DB|
|06:46|ARI|J.Brissett|Brissett on the run connects with K.Bourne|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:55|ARI|J.Brissett|Brissett pressured, heaves deep to Wilson, intercepted by K.Abney|None|deep shot|unknown|unknown|unknown|verified vs DB|
|07:16|ARI|J.Brissett|Brissett on roll, pass to E.Higgins for big play down sideline|38|unknown|unknown|unknown|D.Reed|verified vs DB|
|07:33|ARI|Mi.Wilson|Brissett to Wilson at the 35, tackled by D.J. Reed|None|unknown|unknown|unknown|D.Reed|unverified (no DB match; caption-only)|
|07:39|ARI|C.Ryland|Ryland 53 yard field goal attempt is no good, wide right|53|unknown|unknown|unknown|unknown|verified vs DB|
|07:58|DET|J.Gibbs|Gibbs on 2nd down finds hole, shifty move for 10 yards and first down|10|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:12|DET|J.Williams|3rd and 10, Jameson Williams catches for TD (his 2nd of day)|39|deep shot|unknown|unknown|G.Williams|verified vs DB|
|08:41|ARI|Mi.Wilson|Sliding catch by Michael Wilson at the 45|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:49|ARI|E.Higgins|Brissett floats to E.Higgins down the sideline|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:56|ARI|T.McBride|3rd and 2, Brissett to McBride for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:09|ARI|T.Quitoriano|Brissett to Quitoriano in end zone for 13 yard TD (his 2nd)|13|unknown|unknown|unknown|C.Clark|verified vs DB|
|09:31|DET|J.Gibbs|Gibbs over left side for 6 yards and first down|6|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:44|DET|J.Goff|Play action, Goff to open A.St. Brown for 36 yards|36|play-action|unknown|unknown|M.Melton|verified vs DB|
|09:58|DET|J.Gibbs|Pitch to Gibbs from fullback spot, runs for 22 yards to the 2|22|unknown|unknown|unknown|B.Baker|verified vs DB|
|10:07|DET|J.Goff|Goff on 4th down soars across goal line for 1 yard rushing TD|1|unknown|unknown|unknown|unknown|verified vs DB|
|10:31|ARI|T.McBride|McBride gets first down before end of 3rd quarter|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:41|ARI|T.McBride|Brissett on roll to McBride for catch (7th of day)|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:53|ARI|J.Brissett|Play action, deep shot down sideline to Wilson, pass interference/roughing penalty|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:15|ARI|J.Brissett|2nd and 9, Brissett to J.Brooks for leaping grab and first catch|None|unknown|unknown|unknown|C.Clark|unverified (no DB match; caption-only)|
|11:25|DET|J.Gibbs|Gibbs with burst to the 40 yard line|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:34|DET|J.Gibbs|1st and 15 after penalty, Gibbs carry to midfield for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:53|DET|J.Goff|Goff to LaPorta who dives for catch inside 30 for 19 yards|19|unknown|unknown|unknown|M.Wilson|unverified (no DB match; caption-only)|
|12:08|DET|J.Goff|Goff to A.St. Brown who gets to the 19 for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:19|DET|J.Goff|Goff zips to St. Brown twisting through contact to first and goal|None|unknown|unknown|unknown|B.Baker|unverified (no DB match; caption-only)|
|12:29|DET|J.Gibbs|2nd and goal from 3, Gibbs bounces outside for 3 yard TD|3|unknown|unknown|unknown|D.Burke|verified vs DB|
|13:10|ARI|J.Brissett|3rd and 6, Brissett over middle to receiver for first down at 49|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:47|ARI|J.Brissett|Brissett out of bounds near the 10|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:53|ARI|T.McBride|4th and goal, Brissett to McBride for TD catch in end zone|9|unknown|unknown|unknown|unknown|verified vs DB|

Offense (model synthesis from this game's plays): Effective use of multiple TEs in formations for short and intermediate gains / Big plays via deep passes and play-action to WRs and TEs (multiple 20+ yd gains and TDs) / T.McBride and T.Quitoriano as reliable red zone targets with multiple TDs / 4th down aggression and conversions early / Quick adjustments and no-huddle to create big plays before halftime

Defense weaknesses: Struggled to stop DET on 4th downs allowing multiple conversions and TDs / Poor tackling and coverage on big runs by J.Gibbs and passes to DET skill players / Missed opportunities in red zone and on field goals / Vulnerable to play-action, motion, and deep shots allowing explosive plays / Defensive line pressure inconsistent, allowing Goff time in pocket frequently

Limitations: Could not determine specific run gaps/directions, exact personnel beyond stated, or coverage schemes as they were not explicitly mentioned in captions or matching DB; some plays in captions had no clear DB match or yardage; auto-generated captions had many name mangling issues corrected only on clear matches; limited info on some defender details and non-highlight plays.


## Week 6: ARI 18 - LAR 16 (game 401873004)
Video: Arizona Cardinals vs. Los Angeles Rams Game Highlights | NFL 2026 Season Week 6 — https://www.youtube.com/watch?v=kXX4xq2el10  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:21|LAR|Matthew Stafford|Completion on second-and-seven; receiver stopped about a yard short of the first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:33|LAR|Matthew Stafford|Backpedals under pressure from Zaven Collins and throws away.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:44|ARI|Elijah Higgins|Catches Brissett's pass for four yards.|4|unknown|Three tight ends|unknown|unknown|unverified (no DB match; caption-only)|
|00:57|ARI|Jacoby Brissett|Pass intended for Trey McBride intercepted by Quentin Lake; no return yards. DB credits Braden Fiske with a quarterback hit.|0|Short left pass|unknown|unknown|unknown|verified vs DB|
|01:24|LAR|Blake Corum|Run finishes close to a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:35|LAR|Matthew Stafford|Pump fake followed by an end-zone pass intended for Parkinson; Budda Baker breaks it up.|None|Pump fake|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:49|LAR|Matthew Stafford|Sacked on third-and-12, back at the 28-yard line.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:04|LAR|Blake Grupe|Makes a 44-yard field goal.|44|Field goal|unknown|unknown|unknown|verified vs DB|
|02:15|ARI|Trey McBride|Catches a pass over the middle and advances into Rams territory; DB records 26 yards to the LA 27.|26|Short middle pass|unknown|unknown|Kamren Curl|verified vs DB|
|02:25|ARI|Knight|Catches a pass over the middle for a first down.|None|Pass over the middle|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:40|ARI|Allgeier|Run stopped by Aaron Donald.|None|unknown|unknown|unknown|Aaron Donald|unverified (no DB match; caption-only)|
|02:48|ARI|Jacoby Brissett|Takes a hit from Aaron Donald and throws away on third-and-10.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:00|ARI|Chad Ryland|Makes the tying field goal; DB establishes a 34-yard attempt.|34|Field goal|unknown|unknown|unknown|verified vs DB|
|03:03|ARI|Devin Duvernay|Retrospective mention of a 40-yard kickoff return that set up the tying field goal. DB says Grupe forced him out and was injured on the play.|40|Kickoff return|unknown|unknown|Blake Grupe|CONFLICT (yardage 40 vs DB)|
|03:17|LAR|Williams|Gains five on third-and-seven, finishing about two yards short.|5|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:29|ARI|McBride|First-down reception gains 14 yards; tackled by Kinchens.|14|unknown|unknown|unknown|Kinchens|unverified (no DB match; caption-only)|
|03:47|ARI|Z. Knight|Runs 31 yards to the LA 10.|31|Left end run|unknown|unknown|Quentin Lake|verified vs DB|
|03:58|ARI|Allgeier|Handoff stopped behind the line by Young; captions call him Brian here and Byron shortly afterward.|None|unknown|unknown|unknown|Young|unverified (no DB match; caption-only)|
|04:07|ARI|Jacoby Brissett|Cannot find a receiver, is wrapped up under Byron Young's pressure, and throws away on third down.|None|unknown|Empty backfield|unknown|unknown|unverified (no DB match; caption-only)|
|04:16|ARI|Chad Ryland|Makes a 30-yard field goal for a 6–3 lead.|30|Field goal|unknown|unknown|unknown|verified vs DB|
|04:31|LAR|Blake Corum|Catches a pass over the middle for three yards; immediately met by Gibbens.|3|Pass over the middle|unknown|unknown|Gibbens|unverified (no DB match; caption-only)|
|04:38|LAR|Davante Adams|Third-down reception; commentary identifies a two-man stack while anticipating a target to Puka.|None|unknown|Two-man stack mentioned|unknown|unknown|unverified (no DB match; caption-only)|
|04:50|LAR|Blake Corum|Converts third-and-one on a handoff to the Arizona 16.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:58|LAR|unknown|Fragment describes a tackle by Garrett Williams before second-and-nine.|None|unknown|unknown|unknown|Garrett Williams|unverified (no DB match; caption-only)|
|05:02|LAR|Blake Corum|Catches Stafford's pass and scores from 15 yards.|15|Short right pass|unknown|unknown|unknown|verified vs DB|
|05:17|LAR|Matthew Stafford|Sacked and fumbles on the two-point attempt. Arizona recovers but does not score; DB identifies L. Collier as the recovering player.|None|Two-point pass attempt|unknown|unknown|unknown|verified vs DB|
|05:46|ARI|Jacoby Brissett|Under pressure on third-and-four; commentary credits Young, but the play's result is omitted.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:56|LAR|Matthew Stafford|Loses the football and falls on it inside the 15; Baker is mentioned celebrating.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:06|LAR|Nacua|Advances across the 25 and is stopped about six yards short of the marker.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:15|ARI|Elijah Higgins|Catch and run gains 18 yards across midfield; ruled down before the ball came loose.|18|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:28|ARI|Michael Wilson|Lunges forward to the 30 for a 10-yard gain and first down.|10|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:41|ARI|Knight|Breaks multiple tackles on a run for a first down to the Rams 20.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:56|ARI|Kendrick Bourne|Catches a third-and-six pass for a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:06|ARI|Jacoby Brissett|Incomplete pass intended for Bourne.|None|unknown|Three wide receivers|unknown|unknown|unverified (no DB match; caption-only)|
|07:17|ARI|Chad Ryland|Makes a 22-yard field goal to tie the game.|22|Field goal|unknown|unknown|unknown|verified vs DB|
|07:28|ARI|Kendrick Bourne|Catches a pass over the middle for 11 yards.|11|Pass over the middle|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:43|ARI|McBride|Reception finishes close to a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:53|ARI|Allgeier|Catches Brissett's pass inside the 35 for a first down; nearby commentary mentions a physical tackle by Speights.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:06|ARI|Allgeier|Converts third-and-two on a run, dragging multiple Rams.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:13|ARI|McBride|Five-yard reception to the 17; dragged down by Lake.|5|unknown|unknown|unknown|Lake|unverified (no DB match; caption-only)|
|08:27|ARI|Bourne|Eight-yard reception on third-and-14, stopped just inside the 20.|8|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:37|ARI|Chad Ryland|Makes a 38-yard field goal to regain the lead.|38|Field goal|unknown|unknown|unknown|verified vs DB|
|08:51|LAR|Matthew Stafford|Throws downfield toward Nacua; result omitted.|None|Downfield pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:02|LAR|Blake Corum|Second effort produces a 13-yard run and first down to the 48.|13|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:18|LAR|Davante Adams|Wide-open reception gains 16 yards to the Arizona 36.|16|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:28|LAR|Mumpfield|Third-and-10 reception stopped about a yard short of the first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:38|LAR|Davis Allen|Takes a handoff on fourth down and is stopped short; commentary names Wilson as the defender.|None|Handoff|Williams in backfield; Nacua in motion|unknown|Wilson|unverified (no DB match; caption-only)|
|09:58|ARI|Bam Knight|Runs 13 yards across the 35 for a first down.|13|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:06|ARI|Michael Wilson|Second-and-seven reception earns a first down in Rams territory.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:21|ARI|Michael Wilson|Reception reaches the Rams 12 and earns a new set of downs.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:32|ARI|Trey McBride|Catches a pass to the left for a first down on second-and-one. Opening nine-yard fragment cannot confidently be assigned to this play.|None|Pass left|Bunch left|unknown|unknown|unverified (no DB match; caption-only)|
|10:49|ARI|McBride|Third-and-goal reception stopped immediately by Jaylen Watson.|None|unknown|unknown|unknown|Jaylen Watson|unverified (no DB match; caption-only)|
|10:54|ARI|Chad Ryland|Makes a 27-yard field goal, his fifth of the game.|27|Field goal|unknown|unknown|unknown|verified vs DB|
|11:09|LAR|Davante Adams|Second-and-six reception gains 16 yards into Arizona territory.|16|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:20|LAR|Puka Nacua|Retrospective mention of a 26-yard penalty. DB identifies defensive pass interference by K. Clark on an incomplete deep-right target to Nacua; no play.|26|Deep right pass|unknown|unknown|K. Clark|verified vs DB|
|11:21|LAR|Matthew Stafford|Sacked for an 11-yard loss and fumbles; recovers after McClendon's effort knocks the ball back toward him.|-11|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:54|LAR|Tyler Higbee|Eight-yard reception followed by a fumble forced by C. Simon and recovered by Arizona's D. Burke, per DB.|8|Short right pass|unknown|unknown|C. Simon|verified vs DB|
|12:18|ARI|Bam Knight|Takes a toss; result omitted.|None|Toss run|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:25|ARI|Jacoby Brissett|Third-and-six pass bounces away; Rams defense gets off the field.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:38|LAR|Kyren Williams|Runs 14 yards across midfield to the Arizona 46.|14|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:47|LAR|unknown|Second-and-three play loses two yards on a tackle by Budda Baker.|-2|unknown|unknown|unknown|Budda Baker|unverified (no DB match; caption-only)|
|12:56|LAR|unknown|Fragment describes a first down at the 36; player and play type omitted.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:03|LAR|Matthew Stafford|Short pass goes off Williams's hands incomplete; Arizona takes over.|None|Short pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:11|ARI|Wilson|Catches a pass and is met by Wallace; penalty flag thrown, with enforcement omitted.|None|unknown|unknown|unknown|Wallace|unverified (no DB match; caption-only)|
|13:17|ARI|Jacoby Brissett|Third-and-10 throw over the middle; Wallace makes the defensive play and McVay declines a penalty. Exact pass result omitted.|None|Pass over the middle|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:27|LAR|Puka Nacua|Catches Stafford's pass for 43 yards to the Arizona 34. Commentary credits extra protection for giving Stafford time to find him on the backside.|43|Short middle pass|unknown|unknown|G. Williams|verified vs DB|
|13:50|LAR|Puka Nacua|Second-and-three reception earns a first down at the Arizona 13.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:00|LAR|Williams|Catches an underneath pass out of the backfield to the Arizona 6.|None|Underneath pass to back|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:17|LAR|Colby Parkinson|Play-action reception and reach initially ruled short; DB confirms review reversed it to a six-yard touchdown.|6|Play-action; short right pass|unknown|unknown|D. Burke|verified vs DB|
|14:42|LAR|Ethan Evans|Punter makes the extra point for a 16–15 lead.|None|Extra point|unknown|unknown|unknown|verified vs DB|
|15:31|ARI|J. Brooks|Catches a 21-yard pass to the LA 44 on an offside free play; J. Wallace's unnecessary roughness adds 15 yards, and offside is declined.|21|Deep middle pass; free play|unknown|unknown|J. Wallace|CONFLICT (yardage 21 vs DB)|
|16:15|ARI|Chad Ryland|Makes the winning 43-yard field goal, finishing six-for-six.|43|Field goal|unknown|unknown|unknown|verified vs DB|

Offense (model synthesis from this game's plays): McBride supplied a 26-yard reception and several additional chain-moving catches; Higgins, Bourne and Wilson also contributed first downs. / Knight produced a 31-yard left-end run, a later 13-yard run and another first-down run through multiple tackles. / Brooks's late 21-yard reception plus unnecessary roughness positioned Ryland for the winner. / Ryland converted all six field goals and supplied all 18 points.

Defense weaknesses: Allowed Corum's 15-yard receiving touchdown and Parkinson's six-yard play-action touchdown. / Allowed Nacua's 43-yard reception and another first-down catch during the late touchdown drive. / K. Clark's defensive pass interference conceded 26 yards.

Limitations: Captions only; no frames inspected and no commands run. The supplied DB is selective, so NO DB MATCH does not mean a play did not occur. Fragmentary plays are retained with unknown details; the isolated second-down pass fragment at 03:14 cannot establish a separate play. No specific coverage scheme is explicitly tied to a snap: general discussion of increased Rams man coverage and safety help on McBride does not establish individual-play coverage. The one-on-one remark at 10:44 does not establish a coverage scheme. Formations are included only when explicitly tied to the sequence. defender_beaten lists identified tacklers where available, as requested; this does not establish that those defenders lost coverage. Unmatched names retain caption wording where identity is uncertain. Null yards indicate unavailable or inapplicable yardage; field-goal yards are kick distances, penalty yards are enforcement distances, and Brooks's 21 excludes the added penalty. The earlier Ryland kick is incorrectly recalled as 44 yards in captions; the supplied DB establishes 34. DB-only plays without identifiable caption references are omitted.
