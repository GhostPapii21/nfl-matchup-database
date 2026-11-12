# What the Ravens defense allows: snapshot for JAX@BAL TNF (Nov 5, 2026)
Built read-only from nflverse pbp_2026 (sources/nflverse/pbp_2026.csv.gz, Weeks 1-8, 8 BAL games), the free PFF file (../pff_jax_bal/), and the public ESPN/PFN depth charts. The local nflverse **participation file is missing or corrupt** (the 'Not Found' / non-parquet files under /tmp and week8/), so there's **no snap-level alignment data**. "Side" below comes from pbp `pass_location`, which is where the ball went, not where the receiver lined up. Everything here is a hypothesis, not a pick. Scripts: build.py. CSVs: rush_allowed.csv, top_receivers.csv, all_receivers.csv, zone_allowed.csv.

## Box-score check vs nflverse
- Rico's 7 games match pbp on RB lines and top receivers (Taylor 19-98, Olave 8-86 on 10 targets, Lamb 7-112, Pickens 7-82 on 11, London 7-118 on 11, Higgins 6-148, Chase 5-62, Kincaid 4-86, Moore 4-82, Jeudy 4-69, Cook 21-80).
- **He's missing a game: Week 4 vs TEN (BAL won, TEN scored 18).** TEN ran 26-85 (3.27 YPC). **C. Tate (first name not checked against the roster) had 9-145 on 12 targets, 8 of them to the left.** That fits the WR1 pattern.
- Small differences: ATL pbp passing is 21/35 274 vs Rico's Penix 19/32 240 (pbp counts every QB). BUF team rush is 39-148 in pbp (kneels removed) vs 41-146 on ESPN. IND passing in pbp is 19/31 166.

## (1) Rushing allowed
| Wk | Opp | Team rush | YPC | RB1 |
|---|---|---|---|---|
|1|IND|20-102|5.10|Taylor 19-98|
|2|NO|27-66|2.44|Kamara 9-15|
|3|DAL|30-148|4.93|J. Williams 19-98|
|4|TEN|26-85|3.27|Pollard 16-48|
|5|ATL|26-110|4.23|Bijan 17-86|
|6|CLE|29-93|3.21|Estime 9-19|
|7|CIN|20-73|3.65|C. Brown 11-39|
|8|BUF|39-148|3.79|Cook 21-80|
- 3.6+ YPC in **5 of 8** games (5 of Rico's 7). The exceptions are NO 2.4, TEN 3.3 and CLE 3.2. **Good lead backs got 5+ YPC** (Taylor, Williams, Bijan). Committee or weak backs got shut down.
- For Thursday: Etienne-type volume could work, but this doesn't overturn the locked read (JAX rush unders are on BAL's side, not this).

## (2) Top two receivers each game (pbp; L/M/R = targets by pass_location from the offense's view; aDOT = average air yards per target)
| Wk | Receiver | Line | aDOT | L/M/R | Usual alignment and type (public scouting, general knowledge) |
|---|---|---|---|---|---|
|1|A. Pierce IND|4-61, 6 tgt|17.2|2/4/0|Outside X/Z, deep vertical|
|1|J. Downs IND|2-37|9.0|0/3/1|Slot, YAC|
|2|C. Olave NO|8-86 TD, 10 tgt|10.4|6/2/2|Mostly outside Z, route runner, intermediate/deep|
|2|Juwan Johnson NO|4-66|2.8|1/1/2|TE (inline/slot), 55 YAC|
|3|C. Lamb DAL|7-112, 9 tgt|10.6|5/1/2|Moves around, heavy slot share, YAC (39)|
|3|G. Pickens DAL|7-82, 11 tgt|7.3|4/1/6|Outside X, contested catches|
|4|C. Tate TEN|9-145, 12 tgt|13.3|8/2/2|Outside, intermediate/deep|
|5|D. London ATL|7-118, 11 tgt|10.8|4/3/4|X, big possession/contested, some slot|
|5|J. Dotson / K. Pitts ATL|2-54 / 5-42 TD|18.2 / 4.3|-|Dotson deep outside; Pitts TE, seam/slot|
|6|J. Jeudy CLE|4-69|13.5|0/2/2|Outside/slot, intermediate|
|7|T. Higgins CIN|6-148 TD, 7 tgt|19.6|0/3/4|Outside X, deep|
|7|J. Chase CIN|5-62 TD|9.6|4/0/3|Z/flex, YAC|
|8|D. Kincaid BUF|4-86 TD|13.8|4/2/0|Move TE, seam/slot|
|8|D. Moore BUF|4-82 TD|14.7|3/2/2|Outside, deep|
The alignment types are general scouting knowledge with **medium-low confidence**, since there was no participation data. Confirming them needs nflverse participation `offense_formation`/routes or PFF alignment, which is Premium. I didn't pull that.

## (3) Patterns (all BAL pass defense, 249 targets)
| Zone | Tgt | Yds/tgt | EPA/play |
|---|---|---|---|
|Deep middle 15+|14|**18.4**|**+1.08**|
|Deep right|14|15.9|+0.95|
|Deep left|16|12.9|+0.66|
|Intermediate middle 5-14|26|**10.2**|+0.67|
|Intermediate left|32|7.6|+0.58|
|Short middle <5|21|2.5|-1.35|
|Short right|52|5.6|+0.19|
- **The damage comes downfield, not from short slot work.** Deep throws to every area and intermediate middle (the seam and dig window) are the leaks. Short middle is locked down.
- **Rico's "slot guy goes off" theory is only partly right.** The WR1 goes off almost every week: 6 of 8 games had a 100+ or near-100 WR1 (Lamb, Tate, London, Higgins, plus Olave 86). Most of them are outside receivers with a 10-20 aDOT. Only Lamb is a true slot-heavy player.
- **The "secondary receiver going crazy" is often a TE up the seam or middle** (Juwan Johnson, Pitts, Kincaid, plus Strange-type usage).
- **The WR1s lean to the offense's left:** Olave 6/10, Lamb 5/9, Tate 8/12, Chase 4/7. Offense-left is the **defense's right side, Humphrey's (RCB)**. That's a small sample, and pass_location isn't alignment.

## (4) BAL defenders in those spots
- LCB **Nate Wiggins** (Q on ESPN): wide 431 snaps, 103.3 passer rating allowed, 10.6 YPR.
- RCB **Marlon Humphrey**: wide 382, slot only 7, **15.8 YPR allowed** (the big-play leak; he admitted to that in 2025 too).
- Nickel/slot: **Kyle Hamilton** (slot 162, box 178, 8.3 YPR, 77.3 grade) is strong. Backups are K. Martin and Awuzie (CB3).
- Safeties: **Malaki Starks** FS. **Jaylinn Hawkins SS is listed OUT** (ESPN), so Keondre Jackson starts. That's a downgrade in exactly the deep-middle/seam area where they're already leaking. PFF injury list also has **A. Johnson S Q**.
- PFF's free matchup page disagrees on TEs: it ranks BAL top 5 vs TEs (LB 4th, S 3rd, CB 5th). But pbp shows TEs hitting the seam (Kincaid, Johnson, Pitts). I can't settle that without Premium.
Sources: ESPN depth chart https://www.espn.com/nfl/team/depth/_/name/bal , PFN depth chart, ../pff_jax_bal/defenders.csv.

## (5) Mapping onto JAX (hypotheses)
| JAX player | Where he lines up (PFF free) | Likely BAL matchup | Fit with the leak | Confidence |
|---|---|---|---|---|
|Brian Thomas Jr.|Wide 148 / slot 45; deep X|Wiggins (Q) or Humphrey outside|Best fit for the "deep outside WR1" pattern, but his own PFF form is poor (98th, 10/20)|Med-low|
|Parker Washington|Wide 179 / slot 145|Hamilton when in the slot, Humphrey outside|The slot role runs into BAL's best DB. He's better used outside and intermediate|Med-low (supports his receptions-under single)|
|Jakobi Meyers (Q)|Wide 229 / slot 102|Wiggins/Humphrey|If he's out, targets shift to BTJ, Washington and Strange|Pending injury report|
|Brenton Strange|Inline 171 / slot 80|LB/S, with Hawkins out|The seam/intermediate-middle leak plus the TE pattern matches. PFF CAUTION conflicts|Medium-low|
|Lawrence deep shots|-|Starks / K. Jackson|Deep-middle 18.4 ypt is the clearest leak|Medium|
**The one-line read:** Baltimore stops short throws and committee backs. It gets beaten by the opponent's WR1 working intermediate-to-deep, often toward Humphrey's side, and by TEs up the seam. Hawkins being out makes that worse. For JAX, that points to **BTJ deep and Strange in the seam**, with game script (JAX leading, the rush-under read) as the limiter. It's 8 games of pass-location data with no snap alignment, so treat it as a lead for Rico's call, not a gate.
