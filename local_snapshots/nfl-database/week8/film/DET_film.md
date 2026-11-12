# DET — Phase 8 film notes (Weeks 1–6, 2026)
> Note: games 401872954, 401872978, 401872991 were extracted by Grok via the xAI API (grok-4.20-0309-non-reasoning, same prompt/schema as Codex, cleaned captions); sidecar provenance in film/grok_meta/. All other games with notes: Codex.

Method: NFL YouTube channel full-game highlight videos were located by search and their auto-captions (broadcast commentary) downloaded via yt-dlp. Codex (codex-cli 0.163.0) extracted plays from the captions. **No video frames were viewed by any agent.** Each play was checked against the repo DB play-by-play: `verified vs DB` means the cited DB play exists and the yardage matches. Personnel, formation and coverage appear only when commentators stated them; everything else is `unknown`.


## Week 1: NO 30 - DET 31 (game 401872923)
Video: New Orleans Saints vs. Detroit Lions Game Highlights | NFL 2026 Season Week 1 — https://www.youtube.com/watch?v=KC4OW2m3hjs  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:16|DET|Sam LaPorta|Named on third-and-five; the captions omit the result.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:24|DET|Jahmyr Gibbs|Catches Goff's pass over the middle, breaks tackles and gains a first down.|11|pass over the middle|empty backfield|unknown|unknown|unverified (no DB match; caption-only)|
|00:55|DET|Jahmyr Gibbs|Takes a toss for 21 yards; Julian Blackmon makes the tackle.|21|toss; right end|unknown|unknown|J.Blackmon (DB tackler)|verified vs DB|
|01:03|DET|Jahmyr Gibbs|Carries from the Saints' 24; the result is cut off.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:21|DET|Jared Goff; unidentified receiver|Completes a pass over the middle, short of the goal line but sufficient for a first down.|None|pass over the middle|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:31|DET|Jahmyr Gibbs|Runs for a one-yard touchdown. Commentary credits Sewell and LaPorta with opening the hole.|1|run up the middle|unknown|unknown|unknown|verified vs DB|
|01:52|NO|Brown (first name unspecified)|Mentioned as the first-down receiver; commentary names Rock Ya-Sin as the tackler.|None|unknown|unknown|unknown|Rock Ya-Sin (commentary tackler)|unverified (no DB match; caption-only)|
|01:53|NO|Chris Olave|With Shough increasing the tempo, catches a wide-open pass over the middle for 22 yards.|22|short middle pass; tempo|unknown|unknown|T.Harper (DB tackler)|verified vs DB|
|02:08|NO|Tyler Shough; Chris Olave|Shough targets Olave on third-and-ten; the outcome is cut off.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:24|DET|Jahmyr Gibbs|Gains a first down on second-and-three; play type is unspecified.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:31|DET|Jared Goff|Hit as the ball comes loose. Commentary explains that forward throwing motion makes it a forward pass; Detroit subsequently punts. No turnover touchdown is confirmed.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:05|DET|Unidentified punter|Detroit punts; Brown backpedals to receive it. Return result is omitted.|None|punt|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:14|NO|Chris Olave|Catches a pass across the 25-yard line for a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:27|DET|Jahmyr Gibbs|Catches a short pass and loses the ball on V.Broughton's hit. Captions give the initial down-by-contact ruling; the DB confirms reversal to a Broughton recovery.|4|short right pass|empty formation|zone; specific scheme unknown|V.Broughton (forced fumble and recovery)|verified vs DB|
|03:42|NO|Miller|Takes a toss on third-and-two for a first down.|None|toss|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:53|NO|Tyler Shough|Throws an interception intended for Noah Fant; C.Clark returns it one yard.|None|short left pass|unknown|unknown|C.Clark (interceptor)|verified vs DB|
|04:20|NO|Chris Olave|Targeted on third-and-six and described as body-checked by 'D.J.'; completion status is omitted.|None|unknown|unknown|unknown|D.J. (incomplete name in captions)|unverified (no DB match; caption-only)|
|04:30|NO|Tyler Shough; unidentified receiver|Completes a pass across midfield late in the half.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:35|NO|Tyler Shough|Sacked by Aidan Hutchinson near midfield on third-and-six with 32 seconds remaining.|None|unknown|unknown|unknown|Aidan Hutchinson (sacker)|unverified (no DB match; caption-only)|
|04:58|DET|Jahmyr Gibbs|Spins during a play that ends the half; gain and play type are omitted.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:00|NO|Tyler Shough|Opens the second half with a pass intended for Noah Fant intercepted by Derrick Barnes, who returns it three yards.|None|short middle pass|unknown|unknown|Derrick Barnes (interceptor)|verified vs DB|
|05:18|DET|Jared Goff; unidentified receiver|Runs play-action on first down and targets a player out of the backfield; the outcome is omitted.|None|play-action; backfield target|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:45|DET|Jahmyr Gibbs|Scores his second rushing touchdown, a one-yard run through left guard.|1|left guard run|unknown|unknown|unknown|verified vs DB|
|06:12|NO|Tyler Shough|Roger McCreary sacks Shough and forces a fumble recovered by D.Wonnum.|-8|unknown|unknown|unknown|Roger McCreary (sack and forced fumble); D.Wonnum (recovery)|verified vs DB|
|06:43|DET|Amon-Ra St. Brown|Catches a 19-yard touchdown. Commentary emphasizes his strength and describes a push-off in the route.|19|deep right pass|unknown|unknown|unknown|verified vs DB|
|07:00|NO|Chris Olave|Shough rolls right and throws downfield; Olave adjusts for a 47-yard catch.|47|rollout right; deep right pass|unknown|unknown|D.Reed (DB tackler)|verified vs DB|
|07:15|NO|Tyler Shough|Looks to throw on third-and-one, then dives forward for an apparent first down.|None|scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:29|NO|Etienne|Catches a pass on third-and-three; the result after the catch is truncated.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:37|NO|Kendre Miller|Runs eight yards for a touchdown. Commentary describes following the right side and a block on Jack Campbell.|8|run up the middle (DB); right-side blocking described|unknown|unknown|Jack Campbell (blocked, per commentary)|verified vs DB|
|07:59|DET|Jared Goff|Throws on third-and-four; intended receiver and outcome are cut off.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:18|NO|Unidentified ball carrier|A fake to Etienne produces a Saints first down; the captions do not identify who advances the ball.|None|fake to Etienne|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:20|NO|Etienne|Catches an outside throw for a first down inside Detroit's 25.|None|outside pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:35|NO|Devaughn Vele|End-zone target draws defensive pass interference on Rock Ya-Sin, placing the ball at the one. DB records a 21-yard penalty and no play.|21|deep right pass|unknown|unknown|Rock Ya-Sin (defensive pass interference)|verified vs DB|
|08:49|NO|Devaughn Vele|Makes a diving one-yard touchdown catch. Commentary describes an inside move followed by a move back outside against Ya-Sin.|1|inside move then outside; short left pass|unknown|one-on-one matchup; full scheme unknown|Rock Ya-Sin (name mangled as 'Asim' in commentary)|verified vs DB|
|09:28|DET|Jahmyr Gibbs|Picks up a Lions first down; play type and gain are unspecified.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:54|NO|Etienne|Runs through a large hole for a first down.|None|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:04|NO|Etienne|Named as another play begins; action and outcome are omitted.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:12|NO|Devaughn Vele|Makes a diving catch on third-and-five for 31 yards.|31|deep right pass|unknown|unknown|T.Harper (DB tackler)|verified vs DB|
|10:29|NO|Etienne|Goes out of bounds on third-and-five; gain and play type are omitted.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:33|NO|Daniel Carlson|Makes a 28-yard field goal. Caption wording is truncated; the DB confirms the kick was good.|28|field goal|unknown|unknown|unknown|verified vs DB|
|10:45|DET|Jahmyr Gibbs|Produces another big run on first down; exact gain is omitted.|None|run; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:57|DET|Jahmyr Gibbs|Breaks a tackle on his 26th touch; gain and play type are unspecified.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:04|DET|Amon-Ra St. Brown|Gets the ball on third down and is tackled at the five, bringing out the field-goal unit.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:12|DET|Jake Bates|Makes a 23-yard field goal from the left hash to extend Detroit's lead to seven.|23|field goal|unknown|unknown|unknown|verified vs DB|
|11:22|NO|Tyler Shough; unidentified receiver|Under pressure on fourth-and-12, completes a pass; receiver and gain are cut off.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:45|NO|Vele|Catches another Shough pass; the result is truncated.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:49|NO|Chris Olave|Makes a 42-yard deep catch to Detroit's nine. DB records a declined interference penalty on D.Reed and an injury to Olave.|42|deep middle pass|unknown|unknown|D.Reed (DB tackler; declined defensive pass interference)|verified vs DB|
|12:05|NO|Juwan Johnson|Catches a nine-yard touchdown after getting behind Jack Campbell's missed jam.|9|short right pass; release past jam|unknown|unknown|Jack Campbell|verified vs DB|
|12:47|DET|Jared Goff; Jameson Williams|Goff targets Williams on third-and-two; the result is omitted.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:02|NO|Etienne|Takes a handoff from the Saints' 20 to their 38.|18|handoff; direction unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:16|NO|Tyler Shough; unidentified receiver|From the Saints' 38, completes a diving catch at the 44. Which team's 44 is not stated.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:34|NO|Tyler Shough|Throws out of bounds before the long field-goal attempt.|0|throwaway|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:40|NO|Daniel Carlson|Misses a 62-yard field goal wide right, sending the game to overtime.|62|field goal|unknown|unknown|unknown|verified vs DB|
|13:55|DET|Jared Goff; unidentified receiver|Fakes to Gibbs from Detroit's 30 and completes a pass.|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:09|DET|Jahmyr Gibbs|Catches a pass out of the backfield from the 49 and is brought down by Pete Werner.|None|backfield pass|unknown|unknown|Pete Werner (commentary tackler)|unverified (no DB match; caption-only)|
|14:19|DET|Unidentified player|Commentary calls another first down during Detroit's overtime drive; action is omitted.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:23|DET|Jahmyr Gibbs|On second-and-ten, advances inside the 30 and plows forward close to a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:39|DET|Jared Goff|A second-down play is introduced, but the action and result are missing. It cannot be securely identified as the DB's 22-yard Williams reception.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:47|DET|Amon-Ra St. Brown|Catches a four-yard overtime touchdown on a slant. Commentary describes motion inward from outside and beating Quincy Riley with strength.|4|slant; motion inward|unknown|unknown|Quincy Riley|verified vs DB|
|15:14|NO|Chris Olave|Catches a 20-yard pass on fourth-and-three for a first down.|20|deep right pass|unknown|unknown|A.Maddox (DB tackler)|verified vs DB|
|15:27|NO|Tyler Shough; unidentified receiver|Completes an outside pass for a first down. Receiver's name is garbled.|None|outside pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:42|NO|Unidentified player|Fragment references the Lions' 35 and then the eight in overtime. This is consistent with the DB's Johnson reception, but contains too little action or identification for a secure match.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:45|NO|Noah Fant|Catches an eight-yard touchdown on the drive's tenth play. The live call is truncated, but the ensuing Fant analysis and two-point attempt identify the score.|8|short right pass|unknown|unknown|unknown|verified vs DB|
|16:06|NO|Tyler Shough; B.Lance|Two-point pass intended for B.Lance is incomplete, ending the game. Commentary anticipates rub routes at the top.|None|rub routes described before snap|unknown|unknown|unknown|verified vs DB|

Offense (model synthesis from this game's plays): Gibbs contributed as a runner and receiver: a 21-yard toss, two rushing touchdowns, an 11-yard tackle-breaking reception and an overtime backfield catch. / Commentary credited Sewell and LaPorta with opening the hole on Gibbs' first touchdown. / St. Brown scored twice; commentary emphasized his route strength and described motion into an overtime slant.

Defense weaknesses: Allowed Olave's four matched receptions of at least 20 yards and Vele's 31-yard catch. / Ya-Sin's end-zone interference placed the ball at the one before Vele's touchdown. / Jack Campbell missed his jam on Johnson's nine-yard touchdown. / Allowed New Orleans to recover from 21-0 down to tie regulation and then score an overtime touchdown.

Limitations: Analysis uses only the supplied captions and DB excerpt; no video frames, browsing or commands were used. Caption timestamps mark the available call or lead-in, not necessarily the snap. Truncated plays are retained with unknown outcomes; isolated discussion without identifiable action is omitted. The DB's Williams 22-yard overtime reception and Johnson 27-yard overtime reception cannot be securely matched to the missing caption action. DB-only kickoffs and returns are not added. Formations and coverage are reported only when explicitly stated in commentary; no personnel groupings can be established. Defender fields distinguish tacklers, interceptors and other named participants from defenders explicitly beaten. Interception yards are null because the listed DB yardage describes the return rather than an offensive gain. Field-goal yards are kick distance, and the interference entry's yards are penalty yardage. The failed two-point attempt shares its DB timestamp with Fant's touchdown.


## Week 2: DET 31 - BUF 41 (game 401872932)
Video: Detroit Lions vs Buffalo Bills Game Highlights | 2026 NFL Season Week 2 — https://www.youtube.com/watch?v=ULjOfKcZl4o  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:25|BUF|unknown|Run on second and short gains a first down and reaches the 36; runner is not named.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:35|BUF|Josh Allen|Aidan Hutchinson sacks Allen at the 32 and strips the ball; Buffalo recovers. Commentary identifies Spencer Brown as Hutchinson's blocking matchup.|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:01|BUF|Josh Allen|Scrambles for a first down; a flag is mentioned, but its outcome is omitted.|None|scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:12|BUF|Khalil Shakir|Catches Allen's throw from the 38 at approximately the 25.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:24|BUF|Josh Allen|Rolls left and keeps the ball, gaining a first down and reaching the one.|None|rollout left; quarterback keeper|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:36|BUF|Josh Allen|Keeps the ball for the opening touchdown.|1|quarterback keeper; left guard|unknown|unknown|unknown|verified vs DB|
|01:49|DET|Sam LaPorta|Catches a pass in the flat and advances to approximately the 39.|None|pass to the flat|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:02|DET|Jared Goff|Sacked at the 30 on third and eight; commentary credits Greg Rousseau and describes the pocket collapsing.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:23|BUF|Keon Coleman|Catches an outside throw for six yards and a first down.|6|outside pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:33|BUF|Dalton Kincaid|Catches Allen's pass near midfield and advances into Detroit territory; DB places the finish at the Detroit 42.|25|deep middle pass|unknown|unknown|Avonte Maddox; D.J. Reed (DB tacklers)|verified vs DB|
|02:44|BUF|Josh Allen|Throws incomplete under pressure and is hit by Jack Campbell.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:56|BUF|Joshua Palmer|Allen pump-fakes and finds Palmer wide open for a touchdown. Replay commentary describes a defender reacting to Shakir's crosser and Maddox expecting help that never arrives.|43|pump fake; deep middle shot|unknown|unknown|Maddox (commentary identifies missing expected help)|verified vs DB|
|03:22|DET|Jahmyr Gibbs|Runs out to midfield.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:33|DET|Jahmyr Gibbs|Takes a handoff and finishes just short of a first down, pushed out by Benford.|None|handoff|unknown|unknown|Christian Benford (commentary tackler)|unverified (no DB match; caption-only)|
|03:43|DET|Jared Goff|Taken down near midfield on second and short; commentary identifies Rousseau.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:54|DET|Jared Goff|Falls on a high snap back at the 37.|None|aborted snap|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:07|BUF|James Cook|Gains nine yards on first down, running toward Aidan Hutchinson.|9|run right|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:15|BUF|Dalton Kincaid|Catches a throw from Allen on the move for another first down.|None|rollout pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:24|BUF|Keon Coleman|Catches Allen's pocket throw and reaches the Detroit 13.|22|short right pass|unknown|unknown|C. Clark (DB tackler)|verified vs DB|
|04:34|BUF|Dawson Knox|Allen rolls off a fake and throws to Knox for a touchdown. Commentary identifies Knox aligned as a fullback.|1|play-action rollout; short right pass|13 personnel; Knox aligned at fullback|unknown|unknown|verified vs DB|
|05:01|DET|Gibbs (caption identification uncertain)|Goff steps up and completes a pass beyond the 40 to approximately the 45; captions render the receiver as 'Richard Gibbs.'|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:14|DET|unknown|Outside completion on second and 20; receiver fights for yardage to set up a manageable third down.|None|outside pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:25|DET|Jahmyr Gibbs|Converts for a first down on the ground to the right side.|None|run right|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:38|DET|Amon-Ra St. Brown|Catches an outside pass for a first down on second and ten, with good protection noted.|None|outside pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:51|DET|Jahmyr Gibbs|Catches a touchdown after motion creates separation from a linebacker and he works inside into the seam.|11|motion; seam route|unknown|unknown|unknown|verified vs DB|
|06:22|BUF|James Cook|Breaks a run for a first down and more.|20|run up the middle|unknown|unknown|R. Ya-Sin (DB tackler)|verified vs DB|
|06:37|BUF|James Cook|Exploits a left-side hole behind Dawkins and Anderson. Captions say the 11; DB records the Detroit 13.|35|run left guard|unknown|unknown|D. Reed (DB tackler)|verified vs DB|
|06:47|BUF|Dalton Kincaid|Catches a 16-yard touchdown working into the middle seam; Allen looks left to hold the safety before returning to Kincaid.|16|seam route; safety manipulation with eyes|unknown|unknown|unknown|verified vs DB|
|07:23|BUF|Tyler Bass|Commentary retrospectively identifies a missed extra point; DB specifies wide left.|None|extra-point kick|unknown|unknown|unknown|verified vs DB|
|07:32|DET|Sam LaPorta|Catches a pass while open and is pushed out of bounds for a first down.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:40|DET|Jared Goff|Bradley Chubb sacks Goff back at the 30 on third and five.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:52|BUF|Dalton Kincaid|Catches a pass out to the 24.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:00|BUF|Josh Allen; Khalil Shakir|Shovel pass falls incomplete on third and five; commentary says Shakir has his back to the play.|None|shovel pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:10|DET|Sam LaPorta|Catches a pass over the middle for a first down against a stated four-man rush.|None|middle pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:19|DET|Amon-Ra St. Brown|Goff completes a pass under pressure for a first down near the Buffalo 44; captions say the 43 and describe the receiver's second catch.|22|short right pass|unknown|unknown|J. Hancock; C. Benford (DB tacklers)|verified vs DB|
|08:31|DET|Williams (as captioned)|Catches an outside pass on second and 15; commentary identifies Hairston in coverage.|None|outside pass|unknown|unknown|Hairston (commentary coverage matchup)|unverified (no DB match; caption-only)|
|08:43|DET|Jake Bates|Makes the field goal before halftime.|31|field goal|unknown|unknown|unknown|verified vs DB|
|08:54|DET|Amon-Ra St. Brown|Catches an outside pass over Christian Benford for a first down.|21|deep right pass|unknown|unknown|Christian Benford|verified vs DB|
|09:09|DET|Amon-Ra St. Brown|Catches an underneath pass near the 40, leaving fourth down.|None|underneath pass|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:15|DET|Sam LaPorta|Goff finds LaPorta open for the fourth-down conversion.|None|unknown|three receivers to the right|unknown|unknown|unverified (no DB match; caption-only)|
|09:30|DET|Jahmyr Gibbs|Catches Goff's pass and reaches the 11 with an apparent first down; a flag is mentioned without its ruling.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:44|DET|Amon-Ra St. Brown|Catches a quick touchdown pass, setting up Benford before working inside; commentary praises Goff's low placement away from the defender.|2|quick short left pass; inside release|unknown|unknown|Christian Benford|verified vs DB|
|10:14|BUF|Josh Allen|Pump-fakes, rolls and keeps the ball for approximately eight yards. Captions identify the tackler as 'Caleb Williams,' which cannot be verified.|None|pump fake; rollout scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:27|BUF|Keon Coleman|Goes to the ground to catch a pass, leaving third and one.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:39|BUF|Dalton Kincaid|Catches an outside pass while wide open and sets up first and goal at the six.|23|short left pass|unknown|unknown|C. Clark; D. White (DB tacklers)|verified vs DB|
|10:50|BUF|Josh Allen|Rolls and runs into the end zone to finish a 15-play drive.|2|rollout; scramble right end|unknown|unknown|unknown|verified vs DB|
|11:17|DET|Amon-Ra St. Brown|Makes an open sideline catch for a large gain.|34|deep left pass|unknown|unknown|D. Igbinosun (DB tackler)|verified vs DB|
|11:25|DET|Jared Goff|Throws incomplete as the fourth quarter begins.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:35|DET|Amon-Ra St. Brown|Catches an outside pass for a first down; commentary identifies Alford making the tackle and later calls it a fourth-down conversion.|None|outside pass|unknown|unknown|Alford (commentary tackler)|unverified (no DB match; caption-only)|
|11:52|DET|Jared Goff|Chased out of bounds near the line of scrimmage and pushed down afterward; commentary says no flag.|None|scramble|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:02|DET|Sam LaPorta|Catches a wide-open touchdown after Goff sells a toss fake and LaPorta delays before coming across. Commentary says Dorian Williams is completely fooled.|1|play-action toss fake right; delayed crossing route|three-tight-end look|unknown|Dorian Williams|verified vs DB|
|12:37|BUF|Keon Coleman|Catches Allen's pass for a conversion on third and eight.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:47|BUF|Khalil Shakir|Catches a pass for a first down. Replay commentary describes him motioning from the left into the backfield and a subsequent fake.|None|motion into backfield; fake|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:01|BUF|Keon Coleman|Catches a pass and extends a nine-yard gain into 11 yards and a first down.|11|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:16|BUF|James Cook|Gets outside and around the corner before being forced out at the one.|22|run right tackle; outside|unknown|unknown|C. Clark (DB tackler)|verified vs DB|
|13:29|BUF|James Cook|Runs for the final yard and a touchdown.|1|run right tackle|unknown|unknown|unknown|verified vs DB|
|13:49|DET|Jared Goff|Sacked back near the 23. Captions name the defender as 'Michael Boyd'; identity is unverified.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:00|DET|Isaac TeSlaa|Catches a pass to convert fourth and 18.|20|deep left pass|unknown|unknown|C. Benford (DB tackler)|verified vs DB|
|14:11|DET|Williams (as captioned)|Catches a pass and reaches approximately the Buffalo 26.|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:23|DET|Amon-Ra St. Brown|Catches Goff's touchdown pass. Replay commentary says he beats Alford, with another defender coming down from deeper alignment.|27|deep middle pass|unknown|unknown|Alford|verified vs DB|

Offense (model synthesis from this game's plays): Goff completed throws in rhythm when protected, particularly on the Gibbs touchdown drive. / St. Brown supplied explosive catches of 22, 21 and 34 yards plus touchdowns of two and 27 yards. / LaPorta supplied first-down catches, a fourth-down conversion and a touchdown off a delayed route after a toss fake. / Motion created receiving separation for Gibbs, who also contributed first-down runs.

Defense weaknesses: A coverage communication failure left Palmer open for a 43-yard touchdown, with Maddox expecting help. / Buffalo's tight ends repeatedly found space, including Kincaid's explosive gains and seam touchdown and Knox's play-action score. / Cook broke substantial gains through the middle, behind the left side and around the right edge. / Allen escaped for first downs and scored twice on the ground. / Buffalo sustained a 15-play touchdown drive and later converted through Coleman and Shakir while protecting its lead.

Limitations: Analysis uses only the supplied captions and DB excerpt; no video frames or external sources were consulted. The DB excerpt omits ordinary plays, sacks and incompletions, so NO DB MATCH does not establish that a play is absent from the full database. Null yards indicate that exact official yardage cannot be established; approximate field positions were not converted into exact gains. Caption names and field positions can be wrong, and uncertain unmatched names remain qualified. No specific coverage scheme was explicitly identified. Personnel and alignment are reported only where commentary states them; DB shotgun labels were therefore not used for that field. Named DB tacklers are labeled as tacklers and do not establish that they lost a coverage assignment. Flagged-play outcomes are unavailable where commentary omits the ruling. Kickoffs and the punt return listed only in the DB were excluded because the captions do not identify those highlights. The missed extra point is identified retrospectively in commentary.


## Week 3: NYJ 24 - DET 31 (game 401872954)
Video: New York Jets vs. Detroit Lions Game Highlights | NFL 2026 Season Week 3 — https://www.youtube.com/watch?v=xsJzYyK4mGE  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|00:15|DET|I.Williams|Kickoff return|24|unknown|unknown|unknown|unknown|verified vs DB|
|00:34|NYJ|G.Wilson|Quick hitter catch|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|00:42|NYJ|G.Smith|Pass attempt, dove ahead|None|unknown|unknown|unknown|D.Barnes|unverified (no DB match; caption-only)|
|00:56|DET|J.Goff|Play action fake to Gibbs, throw to Jameson Williams|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:12|DET|J.Williams|Back to back play action, catch|None|play-action|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:15|DET|S.LaPorta|Catch|28|unknown|unknown|unknown|D.Davis|verified vs DB|
|01:22|DET|B.Wright|Catch for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:31|DET|J.Goff|Third and two check down to Gibbs|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:43|DET|J.Goff|Trickery, throw back to Gibbs|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:51|NYJ|A.Cisco|Sack on Goff|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:08|NYJ|B.Hall|Run to 22 yard line|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:16|NYJ|B.Hall|Second and short run|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:36|NYJ|G.Smith|Pressure from Lions, steps up|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:49|NYJ|D.J.Wonnum|Sack on Smith|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:55|DET|J.Goff|Pass to Amon-Ra St. Brown|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:08|DET|J.Goff|Deep drop, spinning into trouble, sacked by Davis|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:15|NYJ|D.Davis|Sack on Goff|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:23|DET|A.St.Brown|Catch for chunk yardage|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:36|DET|J.Goff|Pass to sideline for Wilson, broken up|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:44|NYJ|G.Smith|Quick throw to Wilson|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:58|DET|J.Gibbs|Run for 9 yards|9|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:18|DET|J.Gibbs|Pass game catch, slant to the 13|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:36|DET|J.Goff|Man to man, dump underneath to St. Brown|None|unknown|unknown|man|unknown|unverified (no DB match; caption-only)|
|04:41|DET|A.St.Brown|Knocked down for no gain|0|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:48|DET|J.Bates|30 yard field goal|30|unknown|unknown|unknown|unknown|verified vs DB|
|05:01|NYJ|B.Hall|Catch on third down for 12 yards|12|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:11|NYJ|J.Ruckert|Catch in space for first down|None|unknown|unknown|unknown|R.McCreary|unverified (no DB match; caption-only)|
|05:19|NYJ|J.Ruckert|Chain moving catch and run|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:24|NYJ|J.Ruckert|Three catches|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:37|NYJ|G.Smith|Pass to Kenyon Sadiq for touchdown|24|deep shot|unknown|unknown|unknown|verified vs DB|
|06:04|DET|J.Saylors|Kickoff return|44|unknown|unknown|unknown|unknown|CONFLICT (yardage 44 vs DB)|
|06:20|DET|Vaki|Short yardage run|None|unknown|unknown|unknown|D.Bailey|unverified (no DB match; caption-only)|
|06:31|DET|J.Goff|Drop, wants to go downfield, finds Isaac|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:48|DET|J.Gibbs|Strong run|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:54|DET|J.Goff|Pass over middle to Gibbs|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:09|DET|J.Goff|Throwing back in end zone to LaPorta|4|unknown|unknown|unknown|unknown|verified vs DB|
|07:17|NYJ|D.Belton|Nice play on the back end|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:26|DET|J.Goff|Aggressive on fourth down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:38|DET|A.St.Brown|Touchdown catch|4|unknown|unknown|unknown|unknown|verified vs DB|
|07:53|NYJ|G.Smith|Steps up, one on one with Mitchell, catch|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:48|DET|J.Goff|Play action fake, shot down field for LaPorta|28|play-action|unknown|unknown|D.Davis|verified vs DB|
|09:10|DET|J.Gibbs|12 yard run|12|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:17|DET|J.Gibbs|Toss play, cuts back, touchdown|17|unknown|unknown|unknown|unknown|verified vs DB|
|09:37|NYJ|G.Smith|Escapes pressure|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|09:52|NYJ|G.Smith|Tough throw down the middle to G.Wilson for 32 yards|32|deep shot|unknown|unknown|unknown|verified vs DB|
|10:02|NYJ|B.Hall|Patient run, bouncing outside|None|unknown|unknown|unknown|D.Reed|unverified (no DB match; caption-only)|
|10:18|NYJ|G.Smith|Wrapped up, sacked by McNeill|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:29|NYJ|D.J.Wonnum|Sack on Smith|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:38|NYJ|J.Sanders|Field goal to make it 17-10|42|unknown|unknown|unknown|unknown|verified vs DB|
|10:48|DET|J.Gibbs|Hard hit from Belton, good run|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|10:55|DET|J.Gibbs|Third and two|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:04|DET|J.Gibbs|Strong run to the 46|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:16|DET|J.Gibbs|Strong run, flag thrown|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:28|DET|J.Goff|Pass to Jamison Williams for catch|21|deep shot|unknown|unknown|unknown|verified vs DB|
|11:41|DET|J.Goff|Fake to Vaki, pass to Williams for 9 yards|9|RPO|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:54|DET|J.Gibbs|Run, stayed on feet, pushed inside the 5|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:04|DET|J.Gibbs|Knifing in for touchdown|1|unknown|unknown|unknown|unknown|verified vs DB|
|12:22|NYJ|I.Williams|Third and seven conversion catch|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:39|NYJ|G.Smith|Under pressure, maneuvering in pocket, pass inside 15|21|unknown|unknown|unknown|unknown|verified vs DB|
|12:49|NYJ|K.Sadiq|43 yard connection|43|deep shot|unknown|unknown|R.McCreary|verified vs DB|
|13:05|NYJ|G.Smith|Shot to end zone for Wilson, flag thrown|None|deep shot|unknown|unknown|D.Reed|verified vs DB|
|13:29|NYJ|G.Smith|Throw over middle to J.Ruckert for touchdown|4|unknown|unknown|unknown|unknown|verified vs DB|
|13:50|NYJ|G.Smith|Two point conversion attempt incomplete|None|unknown|unknown|unknown|unknown|verified vs DB|
|14:03|DET|Vaki|Pick up 11 yards|11|unknown|unknown|unknown|D.Davis|unverified (no DB match; caption-only)|
|14:17|NYJ|K.Kingsley|Stop on Davis|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:29|NYJ|G.Smith|Throw to Wilson for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:42|NYJ|G.Wilson|Catch staying inbounds|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:54|NYJ|G.Smith|Dump off, defensive play by Christian|None|unknown|unknown|unknown|C.Clark|unverified (no DB match; caption-only)|
|15:09|NYJ|G.Smith|Shot one on one to Wilson, flag thrown|23|deep shot|unknown|unknown|D.Reed|verified vs DB|
|15:22|NYJ|G.Smith|Two point conversion to Sterling Shepard|None|unknown|unknown|unknown|unknown|verified vs DB|
|15:38|DET|J.Goff|Pass to TeSlaa for 49 yards|49|deep shot|unknown|unknown|A.Cisco|CONFLICT (yardage 49 vs DB)|
|15:58|DET|J.Gibbs|Run for touchdown, third of the day|11|unknown|unknown|unknown|unknown|verified vs DB|
|16:13|NYJ|G.Smith|Pass underneath to Sadiq for first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|16:29|NYJ|G.Wilson|Catch at 40 yard line against McCreary|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|16:47|NYJ|G.Smith|Pass to Braelon Allen for 8 yards|8|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|16:55|NYJ|G.Smith|Sacked and fumble recovered by Detroit|-13|unknown|unknown|unknown|C.Clark|verified vs DB|

Offense (model synthesis from this game's plays): Explosive run game with Jahmyr Gibbs multiple rushing touchdowns and big gains / Effective play action passing leading to big plays and scores / Versatile use of multiple tight ends and trick plays to create mismatches and first downs

Defense weaknesses: Allowed multiple deep completions and big passing plays to Jets receivers including Wilson and Sadiq / Sacked the quarterback several times but still gave up key third down conversions and red zone touchdowns / Defensive penalties including pass interference that extended Jets drives

Limitations: Could not determine exact personnel formations, specific run gaps/directions, or coverage schemes beyond one mention of man coverage as they were not explicitly stated in the commentary. Many plays in captions did not have direct DB matches or exact yardage. Name corrections applied only for clear matches between captions and DB. Several descriptions lack specific yardage or defender details when not mentioned.


## Week 4: DET 26 - CAR 32 (game 401872978)
Video: Detroit Lions vs Carolina Panthers Game Highlights | 2026 NFL Season Week 4 — https://www.youtube.com/watch?v=sD0WZLGybRw  | captions: yes

|ts|off|player|play|yds|concept|personnel/formation|coverage|defender|status|
|-|-|-|-|-|-|-|-|-|-|
|01:01|DET|J.Bates|54-yard field goal is GOOD|54|unknown|unknown|unknown|unknown|verified vs DB|
|01:16|CAR|C.Hubbard|Chuba Hubbard the back on first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:20|CAR|B.Tremayne|Young to Tremble the tight end out to the 42|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:30|CAR|T.McMillan|Tetairoa McMillan the tackle|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:36|CAR|T.McMillan|Again McMillan complete to the 45 yard line|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|01:51|CAR|A.McNeill|McNeill brings him down, third sack|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:09|DET|J.Williams|Deep shots to Jameson Williams|None|deep shot|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|02:36|CAR|C.Hubbard|Hubbard with a good first down gain of five, stopped by Jack Campbell at the 46|5|unknown|unknown|unknown|J.Campbell|unverified (no DB match; caption-only)|
|03:00|CAR|B.Young|Out of the pocket using the legs too, first down|None|RPO|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|03:13|CAR|T.McMillan|Over the top throw to McMillan into the red zone to the 15 yard line, gain of 22|22|unknown|unknown|unknown|unknown|CONFLICT (yardage 22 vs DB)|
|03:30|CAR|C.Hubbard|Hubbard touchdown Panthers|15|left tackle|unknown|unknown|unknown|verified vs DB|
|04:01|DET|S.LaPorta|Sam LaPorta caught the last one for a loss of two|-2|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:20|DET|J.Gibbs|Jahmyr Gibbs turns the corner for a first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:33|DET|A.St.Brown|Lost it picked up and run in by St. Brown|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|04:57|CAR|C.Hubbard|A gain of five|5|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|05:05|CAR|T.McMillan|Tetairoa McMillan off to a quick start, gain of 25 and Panthers first down|25|unknown|unknown|unknown|unknown|CONFLICT (yardage 25 vs DB)|
|05:42|CAR|T.McMillan|Young McMillan in man coverage touchdown Carolina|32|deep right|unknown|man|D.J.Reed|verified vs DB|
|06:29|DET|J.Gibbs|Third and five, pressure comes, to Jameson Williams who has it for the first down at the 39 yard line|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|06:51|DET|J.Williams|Goff to the 23 yard line, Jameson Williams first down to the 6 yard line|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|07:24|DET|J.Gibbs|The touchdown Jahmyr Gibbs|1|left guard|unknown|unknown|unknown|verified vs DB|
|07:51|CAR|T.McMillan|Tetairoa McMillan having a big night, gain of ten and a first down|10|unknown|unknown|unknown|unknown|verified vs DB|
|08:06|CAR|T.McMillan|McMillan to the 28 yard line, gain of 19 out of bounds|19|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|08:40|DET|J.Williams|Jameson Williams streaking downfield to the 24 yard line|49|deep right|unknown|unknown|unknown|verified vs DB|
|09:30|CAR|T.McMillan|Young complete for the first down, touchdown Tetairoa McMillan|10|short middle|unknown|unknown|unknown|verified vs DB|
|10:41|DET|I.TeSlaa|Downfield wide open, down around the 12 yard line|57|deep left|unknown|unknown|unknown|verified vs DB|
|11:15|CAR|B.Tremayne|The throw and the completion to Waller|21|deep middle|unknown|unknown|unknown|verified vs DB|
|11:34|CAR|J.Metchie|Metchie to the 27 yard line, gain of 18|18|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|11:46|CAR|C.Hubbard|Hubbard is on his feet, Chuba Hubbard to the 2|25|right guard|unknown|unknown|unknown|verified vs DB|
|11:57|CAR|C.Hubbard|To the goal line touchdown|2|up the middle|unknown|unknown|unknown|verified vs DB|
|12:23|DET|J.Williams|Caleb Evans Williams on the offensive right side, has Williams|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|12:33|DET|J.Williams|Five for Jameson Williams on the night for 88 yards including 49 yard deep ball|49|deep right|unknown|unknown|unknown|verified vs DB|
|12:59|CAR|C.Hubbard|Flag down, reverses field, chased by Nowaske, around the 45 yard line|32|left tackle|unknown|unknown|T.Nowaske|verified vs DB|
|13:17|CAR|C.Hubbard|Hubbard again|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|13:39|CAR|T.McMillan|Young McMillan forward progress about half a yard|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:02|CAR|B.Young|Young complete first down|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|14:19|CAR|R.Fitzgerald|From 32 Fitzgerald knocks it through|33|unknown|unknown|unknown|unknown|verified vs DB|
|14:34|DET|S.LaPorta|Tight end just shy of midfield and a gain of 25|25|short middle|unknown|unknown|unknown|verified vs DB|
|15:01|DET|J.Williams|Fires complete to Jameson Williams at the 14 yard line|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:50|DET|I.TeSlaa|Goff to the sideline TeSlaa ruled a catch at the 49|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|15:59|DET|S.LaPorta|The pressure and in the middle again to the 35|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|16:06|DET|S.LaPorta|The Lions get something underneath, Goff in the middle, it's LaPorta to the 15 yard line|21|short middle|unknown|unknown|unknown|verified vs DB|
|16:17|DET|S.LaPorta|Goff LaPorta got the first down inside the 4|None|unknown|unknown|unknown|unknown|unverified (no DB match; caption-only)|
|16:24|DET|S.LaPorta|Goff LaPorta brings it down and Detroit stays alive|8|short right|unknown|unknown|unknown|verified vs DB|

Offense (model synthesis from this game's plays): Deep passing shots to Jameson Williams / Utilizing Jahmyr Gibbs in run and pass game to set up play action and one-on-one matchups / Sam LaPorta as reliable target underneath and in red zone / Aggressive play calling on fourth downs and late in halves

Defense weaknesses: Struggles in man coverage especially vs talented receivers like Tetairoa McMillan / Vulnerable to RPOs and mobile QB play from Bryce Young / Defensive line pressure inconsistent allowing big gains / Secondary and linebacker issues vs run and pass in red zone

Limitations: Could not determine exact personnel formations, most coverage schemes, or all exact defender beaten names due to captions not explicitly stating them; some plays in captions did not have clear DB matches or yardage; auto-generated captions mangled several names and play details requiring cross-reference with DB for corrections only on clear matches; unable to identify every single play mentioned due to incomplete or vague commentary.


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

Offense (model synthesis from this game's plays): Explosive plays on 4th down (3/3 in first half, multiple TDs) / Effective use of play-action and motion leading to big gains and TDs / J.Gibbs versatile in run, pass protection, and receiving with multiple big runs and TDs / Deep shots and quick passes to J.Williams, S.LaPorta, A.St. Brown yielding multiple TDs / Red zone efficiency with multiple rushing and passing TDs

Defense weaknesses: Allowed multiple big passing plays to ARI TEs and WRs (22+ yd gains, multiple TDs) / Vulnerable to ARI play-action and bootleg concepts / Missed tackles and pursuit issues on returns and runs / Secondary penalties and missed coverage on deep shots and TEs

Limitations: Could not determine specific run gaps/directions, exact personnel beyond stated, or coverage schemes as they were not explicitly mentioned in captions or matching DB; some plays in captions had no clear DB match or yardage; auto-generated captions had many name mangling issues corrected only on clear matches; limited info on some defender details and non-highlight plays.
