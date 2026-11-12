# DaVon Hamilton (JAX DT/NT) + Eric Murray (JAX S) to IR: impact on JAX run defense and Henry rush U69.5 (TNF JAX@BAL)
Written 2026-11-04 ~12:20 ET. Read-only research. No odds pulls and no Grok.
Not Kyle Hamilton (BAL S); this is unrelated to hamilton_test.
Sources:
- nflverse 2026, local copies: sources/nflverse/snap_counts_2026.csv.gz and pbp_2026.csv.gz.
- jaguars.com roster move (Nov 3) and Day-After story (Nov 2).
- Florida Times-Union (O'Halloran, Nov 3).
- Big Cat Country (Nov 3).
- RotoWire (Nov 3).
- week10/injury_sweep_2026-11-04.md.

**Missing data:** 2026 participation data isn't available, so there's no per-play on/off split by snap. All on/off comparisons below are by game or by play order, and the **samples are small**.

## 1) Hamilton's snap share (defense, from the snap file)
| Wk | 1 | 2 | 3 | 4 | 5 | 6 | 8 |
|---|---|---|---|---|---|---|---|
| Snaps | 19 | 37 | 27 | 31 | 22 | 36 | 11 |
| Snap % | 37 | 60 | 43 | 41 | 35 | 57 | **18** |
- He missed no games. He was a run-down nose at about 35-60% of snaps.
- Week 8: torn quad in Q2 after 11 snaps.

**Opponent designed runs (no scrambles or kneels) vs JAX:**
| Split | Carries | YPC | 10+ rate | Stuff rate (≤0 yds) |
|---|---|---|---|---|
| Weeks 1-6 (with Hamilton) | 121 | 3.18 | 5.8% | 18.2% |
| Week 8, first 11 defensive plays (Hamilton in) | 4 | 7.50 | 25% | 25% |
| **Week 8 after the injury (about Q2 on)** | **17** | **4.00** | **17.6%** | **29.4%** |
| Season (local pbp) | 142 | 3.40 | 7.7% | 19.7% |
- Week 8 without him: 17 carries, 4.00 YPC, compared with 3.18 with him. That's +0.8 YPC on a **very small sample**, inside a 42-7 blowout with IND chasing.
- The 10+ rate rose (3 of 17), but the stuff rate was *higher* too. **It's noise, not a measurement.**
- His per-game snap % doesn't track per-game YPC either. Week 5, his 35% game, was 1.18 YPC; Week 2, his 60% game, was 4.28.
- The fagnano 3.25 / 7.5% vs these 3.18-3.40: the filters differ slightly.

## 2) Replacement (by committee, per Coen)
DT snap % by week (Weeks 1-6, then 8):

| Player | Wk1 | Wk2 | Wk3 | Wk4 | Wk5 | Wk6 | Wk8 |
|---|---|---|---|---|---|---|---|
| **Matt Dickerson** | 35 | 42 | 35 | 13 | 21 | 19 | **51** |
| Ruke Orhorhoro | 35 | 29 | 57 | 38 | 34 | 38 | **72** |
| Albert Regis | 24 | 10 | — | 5 | — | — | — |
| Arik Armstead | 57 | 68 | 57 | 75 | 79 | 78 | 54 |
- Dickerson is the lead nose (Times-Union). He's a 3-technique by trade who got nose reps at OTAs. Times-Union credits him with 132 snaps and 2 run stuffs this year.
- Austin Johnson is on the practice squad, a 2025 Jaguar and a possible elevation.
- In Week 8 Orhorhoro (72%) and Dickerson (51%) absorbed the snaps.
- Coen: "by committee... help us stop a darn good run game and... Derrick Henry."

## 3) Eric Murray
- Starting S at 59-98% (Weeks 1-4 and 6; he missed Week 5). Hurt on the opening kickoff in Week 8.
- Replacements:
  - Kaevon Merriweather: 34%, 68%, 70% in Weeks 5, 6, 8.
  - Rayuan Lane III: 100% in Weeks 5 and 8.
  - Jalen Huskey: 30% in Week 8.
  - Antonio Johnson did not play in Week 8 (no snap row). He was limited Monday; check his status.
- Run-fit relevance: Murray is the veteran communicator and tackler, so he matters most on **explosive runs** (alley fits and the last tackle on 10+ / 20+ runs). He matters little for down-to-down box YPC.
- Week 5, without Murray: 17 carries, 1.18 YPC, 47% stuff rate. Lane and Merriweather have played already without the run D cracking (n = 1 game).

## 4) Verdict on Henry rush U69.5 (r5 card, 3/4)
- **Scenario read:** a short week, a backup QB (Fagnano), and Henry's last three games at 58/45/53 on 2.65-4.82 YPC.
  - JAX scripts ahead, and BAL's run game is the only lever, so volume stays about 14-18 carries.
  - The scenario driver was volume and game script, not just JAX's YPC. Those inputs don't change.
  - Interior run D is weaker on paper, and the main risk is the explosive tail: Henry's 15 runs of 10+ and 3 of 20+. One 25-yarder decides the 69.5.
- **Stats cross-check / miss audit:**
  - The only on/off sample is Week 8 after the injury: 17 carries, 4.00 YPC.
  - It points the same direction as the risk, but it's too small and too game-script-heavy to measure anything.
  - The 3.25 YPC input is pre-injury and now stale on the high side of quality.
- **ESTIMATE of the YPC shift:**
  - Prior: losing one starting run-down nose at about 45% of snaps, plus a starting S, is worth about +0.15 to +0.35 YPC allowed (ESTIMATE, not measured from 2026 data).
  - That moves JAX from about 3.25 to about 3.4-3.6 on designed runs, still below the league's 3.95.
  - On the base 14 carries / 50 yds, that's about +2-5 yards, so a median of about 52-55.
  - U69.5 goes from 83% to about 78-80% (ESTIMATE, not re-simmed). The flip case (18 / 66) moves to about 18 / 70 or more, which is a push/loss.
  - A larger 10+ rate (from 7.5% to about 9-10%, ESTIMATE) is the bigger lever than the mean.
- **Verdict:** **U69.5 still stands** on the scenario read, which is driven by carries.
  - **FLAG TO RICO, do not cut:** the run-defense input (3.25 YPC / 7.5% 10+) predates the losses of Hamilton and Murray. The explosive-run risk is up, so the edge is thinner, about 3-5 points (ESTIMATE).
  - Don't add the overs. Don't increase the stake on the under.
  - Recheck if Tuten is out and JAX can't build a lead (more BAL carries), or if Austin Johnson isn't elevated.
