# Jacksonville TE usage comparison — W1–8 vs Nov 5 BAL (sourced)

Recorded Nov 6, 2026, 5:08 AM ET from Rico’s direct request (preserved from prior pending note).
Follow-up completed 2026-11-06 05:11:22 ET (America/New_York): Ghost6 W1–8 originals verified; pending status replaced with sourced comparison.

## Request provenance (unchanged)
Rico reports that Weeks 1–8 did not show the additional-tight-end **receiving** usage seen against Baltimore Nov 5. Compare TE targets/snaps against Nov 5 to distinguish **target redistribution** from unverified personnel-package claims. Missing route and package counts must remain missing. No inferred motivation from betting popularity. Finite database follow-up only — no projections, no code/model/rule changes.

## Sources
- Ghost6 review: `week10/jax_usage/targets_by_game.csv`, `week10/jax_usage/usage.md` (built from nflverse; script `build.py`)
- nflverse originals: `sources/nflverse/pbp_2026.csv.gz`, `sources/nflverse/snap_counts_2026.csv.gz`
- Nov 5 final: `live/2026-11-05_JAX_BAL/pbp_live.csv` + ESPN summary boxscore receiving
- Comparative CSV: `week10/jax_usage/te_usage_w1_8_vs_nov5_BAL.csv` (copy also under this notes/ folder)

## Verified receiving (tgt/rec/yds)

| Game | Strange | Boerkircher | Koziol | Status |
|------|---------|-------------|--------|--------|
| W1 | 3/2/23 | 1/1/9 | 0 | VERIFIED (Ghost CSV = nflverse PBP = claim) |
| W2 | 2/2/17 | 0 | 0 | VERIFIED |
| W3 | 5/3/32 | 1/0/0 | 0 | VERIFIED |
| W4 | 8/7/95 | 2/1/15 | 0 | VERIFIED |
| W5 | 8/7/68 | 2/2/20 | 0 | VERIFIED |
| W6 | 7/5/44 | 2/2/8 | 0 | VERIFIED |
| W7 | bye | bye | bye | BYE |
| W8 | 2/2/55 | 1/1/31 | 1/1/8 | VERIFIED |
| Nov 5 vs BAL | 2/2/22 | 3/2/61 | 2/2/15 | VERIFIED (local PBP = ESPN box) |

**Mismatches:** none on tgt/rec/yds across claimed ↔ Ghost CSV ↔ nflverse PBP (W1–8) and claimed ↔ local final PBP/box (Nov 5).

## Claimed contrast (also verified)
- Prior W1–8 **Boerkircher+Koziol** single-game max: **2 targets**, **39 yards** (W8: B 1/1/31 + K 1/1/8). No prior game exceeded 2 combined B+K targets.
- Koziol season targets before Nov 5: **1** (W8 only).
- Nov 5 B+K: **5 targets, 76 yards** (B 3/2/61 + K 2/2/15).
- Nov 5 first two TE targets of game: **Koziol 4 yards** (Q1 14:54), then **Boerkircher 52 yards** (Q1 14:17). **Strange’s first target: Q2 1:57** (15-yard catch).

## What is / is not shown
- **Shown (sourced):** unprecedented **receiving redistribution** toward Boerkircher+Koziol in the 7 reviewed games (W1–6, W8) relative to Nov 5 target/yard totals.
- **NOT verified:** new “12/13 personnel package.” Snap counts show Boerkircher (and later Koziol) took offense snaps in prior weeks, but snaps do **not** prove routes, blocking assignments, simultaneous multi-TE use, or that a Boerkircher/Koziol target implies Strange was off the field.
- **FTN charting** (`sources/nflverse/ftn_charting_2026.csv`): no personnel/route columns usable for this; JAX rows not present in a team-keyed sense for package proof.
- **2026 participation** file: **missing** on disk — Nov 5 offense snap % for these TEs marked NA.

## Files written
- `/workspace/nfl-database/week10/jax_usage/te_usage_w1_8_vs_nov5_BAL.csv`
- `/workspace/nfl-database/live/2026-11-05_JAX_BAL/notes/te_usage_w1_8_vs_nov5_BAL.csv`
- This note replaces `te_usage_comparison_pending.md` (pending file removed after write).


---

## Follow-up 2026-11-06 05:17:50 ET: multi-TE package hypothesis test (snaps / gamebook / film URL)

Rico 5:13 AM ET direct: test whether a new two/multi-TE package caused Boerkircher/Koziol work; compare offensive snaps vs W1–8; seek simultaneous personnel and blocking-vs-routes via gamebook/participation/official film. **This agent cannot watch video** — highlight URLs/paths returned for parent `watchVideo` dispatch only.

### Sources checked (sanctioned / public; no paid odds, no sign-ins, no hidden endpoints)
| Source | Result |
|--------|--------|
| sports-leader ESPN search | ESPN highlight clip page + story links |
| muffed metrics search | No snap-level personnel/route board for this game |
| nflverse `snap_counts_2026` (local + fresh GitHub release) | **Max week still 8** — Nov 5 / Week 9 **MISSING** |
| FootballDB JAX snap counts | Week **9 column blank (`--`)** for all players as of fetch |
| PFR boxscore HTML fetch | Cloudflare interstitial only (no snap table retrieved) |
| **NFL.com Game Center** | Game book PDF link present |
| **NFL official gamebook PDF** | Downloaded; contains unofficial playtime % **and** listed starting offense |
| NFL.com / Jaguars.com / Ravens.com highlight pages | Official highlight **page** URLs (stream in browser) |
| ESPN CDN MP4 | Downloadable highlight file saved locally for parent |

### Nov 5 (= NFL **Week 9**, not Week 10) offensive snaps — official gamebook (unofficial %)
Team offense snaps: **56** (OL/QB 56 = 100%).

| Player | Off snaps | Off % | ST snaps | vs W1–8 offense snap range (nflverse) |
|--------|----------:|------:|---------:|----------------------------------------|
| Brenton Strange | **44** | **79%** | 0 | 28–58 snaps; 52–87% — Nov5 **within prior range**; still **led** TE snaps |
| Nate Boerkircher | **31** | **55%** | 3 | 21–39 snaps; 34–67% — Nov5 **within prior range** (matches W6 ~55%) |
| Tanner Koziol | **12** | **21%** | 3 | 3–19 snaps; 5–35% — Nov5 **within prior range** (below W8 19/35%) |

Source URL (gamebook PDF): `https://static.www.nfl.com/image/upload/v1793954916/gamecenter/ab380826-4feb-11f1-abca-2c54536568a9.pdf`  
Local copy: `live/2026-11-05_JAX_BAL/notes/evidence_nov5/nfl_gamebook_JAX_at_BAL_20261105.pdf`  
Parsed text: `.../nfl_gamebook_JAX_at_BAL_20261105.txt`  
Snap CSV: `week10/jax_usage/te_snaps_w1_8_vs_nov5_BAL.csv` (+ notes/ copy)

**Do not equate targets to snaps.** Strange 2 targets on 44 snaps; Boerkircher 3 targets on 31 snaps; Koziol 2 targets on 12 snaps.

### Starting lineup evidence (gamebook) — personnel package
Gamebook **Jacksonville starting offense** lists:
- TE 87 N.Boerkircher
- TE 85 B.Strange
- TE 88 T.Koziol
- WR 11 P.Washington
- RB 33 B.Tuten
- (+ OL + QB)

That is a listed **1 RB / 1 WR / 3 TE** starting grouping (**13 personnel** by standard RB-TE-WR coding). This supports that a **multi-TE base package was listed**, not that every snap or every B/K target used that exact grouping.

**Still MISSING / not proven from aggregate snaps:**
- Play-by-play personnel codes (11/12/13) for each target
- Whether Strange was on the field on Boerkircher/Koziol targets
- Blocking vs route role for any TE
- FTN/participation 2026 Week 9: unavailable/corrupt or not released in local trees

### Target timing vs blowout (local final PBP — scores at throw)
| Clock | Score (JAX–BAL) | Margin | Target | Result |
|------:|-----------------|-------:|--------|--------|
| Q1 14:54 | 0–0 | 0 | Koziol | 4 yd catch |
| Q1 14:17 | 0–0 | 0 | Boerkircher | 52 yd catch |
| Q1 12:08 | 0–0 | 0 | Boerkircher | incomplete (W.Milum reported eligible — 6th OL look, not TE personnel proof) |
| Q2 1:57 | 10–3 | +7 | Strange | 15 yd catch (Strange’s first target) |
| Q3 8:18 | 20–3 | +17 | Strange | 7 yd catch |
| Q3 5:50 | 20–3 | +17 | Boerkircher | 9 yd catch |
| Q3 1:06 | 20–3 | +17 | Koziol | 11 yd catch |

First three TE targets occurred at **0–0 before any score** — not garbage-time redistribution. Later B/K targets came with JAX already up 17.

### Hypothesis verdict (factual)
| Claim | Status |
|-------|--------|
| New multi-TE package existed as listed starters | **Supported by gamebook lineup** (3 TEs listed with 1 WR / 1 RB) |
| Multi-TE package **caused** B/K receiving spike | **NOT verified** — causation missing; snaps alone cannot prove |
| B/K out-snapped Strange | **False** — Strange 44 > Boerkircher 31 > Koziol 12 |
| Nov5 B/K snap shares unprecedented vs W1–8 | **False** — both within prior snap ranges |
| Blocking TE vs route runner identifiable here | **MISSING** — no film review performed by this agent |
| Aggregate snaps ⇒ 12 personnel or Strange absence | **Invalid inference** — explicitly rejected |

### Official highlights (for parent watchVideo — no film claims by this agent)
| Item | URL / path |
|------|------------|
| NFL.com highlights page (Week 9) | https://www.nfl.com/videos/jaguars-vs-ravens-highlights-week-9 |
| NFL.com alt highlights page | https://www.nfl.com/videos/game-highlights-jaguars-vs-ravens-highlights-week-9 |
| Jaguars.com highlights | https://www.jaguars.com/video/jaguars-vs-ravens-week-9-highlights |
| Ravens.com full highlights | https://www.baltimoreravens.com/video/ravens-jaguars-full-highlights-week-9-nfl |
| NFL Game Center | https://www.nfl.com/games/jaguars-at-ravens-2026-reg-9 |
| ESPN clip page | https://www.espn.com/video/clip/_/id/50396514 |
| **Downloadable MP4 (ESPN CDN)** | `https://espnmedia-cdn.akamaized.net/espn/media/16x9/wsc/2026/1106/70aefe4e-ae80-444d-af7f-fd8ed3590fde/70aefe4e-ae80-444d-af7f-fd8ed3590fde.mp4` |
| **Local video path for parent** | `/workspace/nfl-database/live/2026-11-05_JAX_BAL/notes/evidence_nov5/espn_jaguars_ravens_highlights_wsc.mp4` (~83.6 MB, ftyp isom) |

NFL.com pages are streamable in-browser; no direct `.mp4` extracted from nfl.com HTML. ESPN CDN MP4 **is** downloadable and saved locally for parent analysis dispatch.

### Evidence directory
`live/2026-11-05_JAX_BAL/notes/evidence_nov5/` — gamebook PDF/TXT, NFL/ESPN HTML captures, local MP4, attempted fresh snap_counts gz (still through W8).


## Selected highlight review — Nov 6, 5:21 AM ET
The downloaded ESPN scoring-highlight clip omits the opening Koziol 4-yard and Boerkircher 52-yard catches and Strange’s late-Q2 15-yard catch. Corrected video analysis could not reliably identify Strange during active blocking or routing; celebration identification does not establish his assignment. No usable passing-play personnel or blocking-role confirmation from this clip. An initial video interpretation misidentified Baltimore’s Q3 interception as Jacksonville offense and inferred Strange blocking; both claims were withdrawn and are excluded from findings. Full-play footage/participation remains required to resolve mechanism.
