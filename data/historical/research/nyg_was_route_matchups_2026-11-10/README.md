# NYG pass catchers vs WAS defenders: inferred route and zone matchup estimate

TNF Thursday Nov 12, 2026, WAS at NYG (MetLife). Built Tue Nov 10, 2026, 12:22 to 12:31 PM ET. **Research only.** No picks, no model changes, `projection_ready` not touched. Passing-yards legs stay banned from slips.

**Every matchup number in this folder is an INFERRED ESTIMATE built from target locations, alignment, scheme and snaps. None of it is charted coverage.** No public 2026 source publishes defender-on-receiver assignments. StatRankings' shadow-coverage page has that data, but it's subscriber-only, and it was not bypassed.

## 1. What NGS route data exists (and what doesn't)
- **NGS route charts** come from `nextgenstats.nfl.com/api/content/microsite/chart?type=route`, pulled 12:23 PM ET. They're **JPEG images of targeted routes only**, color-coded incomplete, route and after-catch. There are **no route-type labels, no coordinates, and no untargeted routes.** NGS only publishes charts for some player-games:
  - Nabers: Weeks 3, 4, **5**, 7. There's no chart for Weeks 1, 6 or 9.
  - Likely: Weeks 1, 2, **5**, 6, 9.
  - **Fields: none** all season.
  - Images are saved in `raw/ngs_chart_images/`, along with Winston's Week 5 pass chart (dots not tied to receivers).
- **NGS weekly receiving** comes from nflverse `nextgen_stats/ngs_receiving.parquet`. It covers separation, cushion, intended air yards, air-yard share and YAC over expected, season (week 0) and weekly. Weeks below NGS's target threshold are missing, so there's **no Fields Week 5 row** (he had 2 targets). The data is in `ngs_routes.csv`.
- **NGS statboard** (`/api/statboard/receiving`, threshold 23 targets) gives season numbers that match the nflverse week-0 rows.
- **Route types and route trees are NOT exposed** by NGS, NFL Savant (`routes_json` is empty, `route_tree_available=False`), or the public FTN columns. So the zone mapping uses **target location** (gamebook/pbp `pass_location` plus nflverse `air_yards`) instead of route type. Any route shapes mentioned below are visual reads of the NGS images, not labels.

### Visual read of the NGS Week 5 charts (not labeled data)
- **Nabers, 20 targets, 11 catches, 121 yards, 1 TD, 33 YAC:** most targets are on the offense's right. They're short in-and-out breaks with YAC, plus a cluster of **4–5 incomplete vertical stems up the right side**. On the left he ran crossing and in-breaking routes into the middle, and the 17-yard TD came over the middle.
- **Likely, 13 targets, 11 catches, 94 yards, 2 TDs, 38 YAC:** short crossers and in-breaks between the hashes, a few flat or out-breakers to the right, and two incomplete stems deep left-middle.

## 2. Receiver profiles
NGS numbers are from the nflverse NGS file. Zone shares are from the nflverse pbp file, Weeks 1–9 (Giants bye was Week 8).

| | Season targets | Side L / M / R | Depth short / int / deep | NGS sep | cushion | intended air yds | YACOE | Alignment |
|---|---|---|---|---|---|---|---|---|
| Nabers | 78 | 38 / 22 / 40% | 54 / 23 / 23% | 3.02 | 7.34 | 11.48 | -0.55 | mostly outside. PlayerProfiler: 40 slot snaps through Week 5 (~15% of his snaps). Giants.com: 41.3% slot in Week 6 (season high) |
| Nabers, Week 5 | 20 | 25 / 25 / 50% | 45 / 25 / 30% | 3.02 | 7.70 | 12.54 | -1.35 | The Athletic: Douglas "shadowed Nabers on the perimeter for parts"; Nabers went 4-73-1 from the slot |
| Likely | 69 | 36 / 30 / 33% | 62 / 29 / 9% | 2.90 | 5.14 | 7.64 | +0.17 | StatRankings slot rate 84.0% (2nd in NFL), move TE 83.2% (1st), 291 slot snaps |
| Likely, Week 5 | 13 | 23 / 38 / 38% | 62 / 23 / 15% | 2.41 | 5.91 | 8.60 | -0.30 | |
| Fields | 35 | 34 / 29 / 37% | 46 / 34 / 20% | 2.16 | 6.31 | 13.27 | +2.28 | StatRankings perimeter 78.8%, left-aligned 43.2% |
| Fields, Week 5 | 2 | 0 / 0 / 100% | short only | n/a | n/a | n/a | n/a | 2 short-right catches (13 and 7 yards) |

## 3. Washington alignment and scheme inputs (`alignment_sources.csv`)
- **Shell:**
  - StatRankings (Nov 10): two-high 61.8%, man 17.9%, so single-high zone is about 20.3%. Blitz rate is 44.4%.
  - Sharp (Nov 3): MOFO 61.0%, MOFC 32.1%, man 12.2%.
  - The model uses the StatRankings rates for both games. As a sensitivity check, StatRankings' away split is 69.7% two-high.
- **Cornerback sides:** StatRankings' *right coverage rate* measures how often the receiver a defender covers is lined up on the **offense's** right. Douglas is at 61.3%, Moreau 64.0% and Sainristil 62.3%. That fits Douglas at LCB on the depth chart, stationed on the defense's left. Robertson and Amos aren't on the public top-25 boards.
- **Week 5 roles:**
  - DC Jones said Sainristil handled **deep-zone assignments** against New York (SI).
  - The staff had moved Sainristil to nickel, with Robertson, Douglas and Moreau handling outside work (SI).
  - The Athletic: Nabers' TD and his 28-yard OT catch came against **Sainristil** (via Heavy, Oct 15). Those two plays are weighted 50% to Sainristil.
- **Current depth chart** (PFM, Nov 9): LCB Douglas, RCB Amos, NB Robertson, FS Reaves, SS Cross, LILB Luvu (offense's right hook), RILB Styles (offense's left hook).
- **Snap math:** In Week 9 the DBs add up to about 433% of snaps, with Cross 100, Reaves 60 and Martin 56. That points to frequent **three-safety looks**. The model treats Martin as the third safety / big nickel and moves Robertson outside when Douglas is off the field. **That role inference is ours.**

## 4. Method
1. The 35 official Week 5 targets (Nabers 20, Likely 13, Fields 2) each get a side and a depth band: short is 9 air yards or less, intermediate is 10–19, deep is 20+.
2. Each target area gets zone roles based on the shell:
   - **Two-high (Cover 2/6 family):** outside corners take the flats, LBs the hooks, the nickel the slot/curl, and the safeties the deep halves.
   - **Single-high (Cover 3):** the outside corners take the deep thirds, plus a free safety in the middle and a robber/curl-flat defender.
   - **Man:** the defender follows the receiver's alignment. Douglas is weighted toward Nabers because of the shadow note.
   - Likely's outside weights are cut because he's 84% slot.
3. Each role is filled by a probability pool of defenders built from Week 5 snaps and roles (`model_assumptions.json`).
4. That prior is blended with the **official gamebook tackler/PD credit**: 60% prior and 40% credit. Where there's a media attribution, it's 50% prior and 50% media. The credit tells you who was **near the ball at the catch or breakup**, not who was covering.
5. For each receiver and defender, the target-weighted sum is the **estimated target-time crossings**. Confidence labels:
   - **high:** at least 15% share, named on 2 or more targets, and at least 10% zone prior
   - **medium:** at least 8% share, plus either a credit or a zone prior of at least 12%
   - **low:** everything else
6. **Thursday:** the same zone rules run with the Week 8–9 personnel pools over (a) the season target heat and (b) the Week 5 target spots.
- **Validation:** the credited defender was in the zone-prior top 3 on **13 of 24 credited official targets (54%)**. The prior alone is only a rough guide. Moreau's 3 Nabers credits on the right side all came late, suggesting he played more of the 4th quarter and OT than his 29% snap share implies.

## 5. Results (estimates)
**Week 5 crossing estimate** (`crossing_estimate.csv`):
- Nabers: Douglas 22.5% (high), Robertson 16.3% (high), Martin 13.5% (med), Sainristil 12.4% (med, from the 2 media plays), Moreau 10.8% (med), Reaves 9.7% (med), Styles 8.6% (med)
- Likely: Styles 16.5% (high), Luvu 16.3% (high), Martin 15.5% (med), Reaves 14.7% (med), Douglas 13.2% (med), Sainristil 11.1% (med)
- Fields (2 targets, tiny sample): Moreau 27%, Douglas 24%, Sainristil 16%, Martin 13%. All medium.

**Thursday projection** (`thursday_projection.csv`, season heat scope):
- Nabers: Robertson 19% (med), **Amos 18% (med, never faced him)**, Martin 13%, Douglas 12%, Cross 10%
- Likely: Styles 18% (med), Martin 18%, Luvu 16.5%, **Cross 15% (never faced him)**, Robertson 12.5%
- Fields: Robertson 17.5%, Amos 15%, Martin 14%, Douglas 12%, Cross 11%. All low.

Read this together with `/workspace/was_pass_def_2026-11-10/` (Amos and Robertson era: 5.71 YPA allowed in Weeks 8–9) and the Week 5 credit availability table there.

## 6. Gaps (not filled in)
- No route types, route trees or route coordinates from any public source. The NGS images cover targeted routes only, and Fields has none.
- No 2026 nflverse participation file, no FTN coverage column, and no public defender-on-receiver charting. StatRankings shadow coverage, player alignment and coverage splits are subscriber-only.
- Nabers' season slot rate isn't public. The model uses the 15% derived figure through Week 5 and the 41.3% Week 6 media figure only as context.
- Robertson's and Amos's side splits aren't public. Which safety plays which deep half is unknown, so it's split 50/50.
- Week-specific Week 5 shell rates don't exist publicly. The model uses season rates.
- Thursday inactives and the Week 10 injury report aren't final: Moreau is uncertain, and Tuttle is questionable, though he's not a coverage player.
- The estimates only count **targets** (35 in Week 5). Crossings on untargeted routes can't be seen.

## Files
- `ngs_routes.csv`: NGS weekly and season receiving rows, plus chart availability and image paths
- `target_zone_profile.csv`: target counts by side and depth band, season and Week 5
- `alignment_sources.csv`
- `wk5_target_zone_map.csv`: every Week 5 target with zone roles, prior top 3, official credit, estimated top 3 and basis
- `crossing_estimate.csv`
- `thursday_projection.csv`
- `model_assumptions.json`
- `wk5_targets_vs_was_zones.png`
- `thursday_projection_was_zones.png`
- `raw/`: NGS JSON/parquet/images and StatRankings HTML
- `build.py`, `plots.py`, `alignment_sources.py`
