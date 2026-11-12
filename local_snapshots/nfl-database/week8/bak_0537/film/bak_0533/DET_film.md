# DET — Phase 8 film notes (Weeks 1–6, 2026)

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

Offense (Codex synthesis from this game's plays): Gibbs contributed as a runner and receiver: a 21-yard toss, two rushing touchdowns, an 11-yard tackle-breaking reception and an overtime backfield catch. / Commentary credited Sewell and LaPorta with opening the hole on Gibbs' first touchdown. / St. Brown scored twice; commentary emphasized his route strength and described motion into an overtime slant.

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

Offense (Codex synthesis from this game's plays): Goff completed throws in rhythm when protected, particularly on the Gibbs touchdown drive. / St. Brown supplied explosive catches of 22, 21 and 34 yards plus touchdowns of two and 27 yards. / LaPorta supplied first-down catches, a fourth-down conversion and a touchdown off a delayed route after a toss fake. / Motion created receiving separation for Gibbs, who also contributed first-down runs.

Defense weaknesses: A coverage communication failure left Palmer open for a 43-yard touchdown, with Maddox expecting help. / Buffalo's tight ends repeatedly found space, including Kincaid's explosive gains and seam touchdown and Knox's play-action score. / Cook broke substantial gains through the middle, behind the left side and around the right edge. / Allen escaped for first downs and scored twice on the ground. / Buffalo sustained a 15-play touchdown drive and later converted through Coleman and Shakir while protecting its lead.

Limitations: Analysis uses only the supplied captions and DB excerpt; no video frames or external sources were consulted. The DB excerpt omits ordinary plays, sacks and incompletions, so NO DB MATCH does not establish that a play is absent from the full database. Null yards indicate that exact official yardage cannot be established; approximate field positions were not converted into exact gains. Caption names and field positions can be wrong, and uncertain unmatched names remain qualified. No specific coverage scheme was explicitly identified. Personnel and alignment are reported only where commentary states them; DB shotgun labels were therefore not used for that field. Named DB tacklers are labeled as tacklers and do not establish that they lost a coverage assignment. Flagged-play outcomes are unavailable where commentary omits the ruling. Kickoffs and the punt return listed only in the DB were excluded because the captions do not identify those highlights. The missed extra point is identified retrospectively in commentary.


## Week 3: NYJ 24 - DET 31 (game 401872954)
Video: New York Jets vs. Detroit Lions Game Highlights | NFL 2026 Season Week 3 — https://www.youtube.com/watch?v=xsJzYyK4mGE  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 4: DET 26 - CAR 32 (game 401872978)
Video: Detroit Lions vs Carolina Panthers Game Highlights | 2026 NFL Season Week 4 — https://www.youtube.com/watch?v=sD0WZLGybRw  | captions: yes

_No Codex film notes (no captions or run not completed)._


## Week 5: DET 45 - ARI 21 (game 401872991)
Video: Detroit Lions vs. Arizona Cardinals Game Highlights | NFL 2026 Week 5 — https://www.youtube.com/watch?v=a7ixKMcIHHs  | captions: yes

_No Codex film notes (no captions or run not completed)._
