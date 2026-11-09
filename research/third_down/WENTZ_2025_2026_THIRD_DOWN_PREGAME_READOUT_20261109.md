# Wentz third-down and possession opportunity, 2025 + 2026 pregame

**Game:** Buffalo Bills at Minnesota Vikings, Monday November 9, 2026, 8:15 PM ET. **Data:** nflverse 2025 regular-season Wentz five starts (Weeks 3,4,5,7,8); nflverse 2026 REG Weeks 1–8 (MNF not included). This is a source-audited, pregame, **research-only** readout. No outcome, quote, projection parameter, or production model changed.

**Machine-audited source & per-game evidence:** [wentz_2025_third_down_audit_20261109.json](wentz_2025_third_down_audit_20261109.json). Includes full source download URLs and SHA-256, the per-opponent third-down categories, source flags and their limitations. Verified by [GitHub Actions](https://github.com/GhostPapii21/nfl-matchup-database/actions/workflows/nfl-wentz-third-down-audit.yml).

## Exact source definitions

1. **Team third down:** all official third-down conversion/failure flags, rushing, QB drops and penalties.
2. **QB third-down dropback:** pass throw, sack, or scramble. Wentz 2025 has 50 qualifying dropbacks.
3. **Thrown pass:** nflverse **marks sacks with `pass_attempt=1`**, so passing completions must use `pass_attempt=1` AND `sack=0` AND `qb_scramble=0`. Audited Wentz 2025 = 32 actual third-down throws, 17 completions = **53.1%**. Eleven sacks and seven scrambles account for the other 18 dropbacks. The alternate NextLevelStats figure of 44 third-down 'att' / 38.6% completed uses a different play inclusion or denominator; **do not mix those**.
4. **QB hit:** nflverse flag means recorded QB hit or sack, **not** complete charted pressure and certainly **not blitz**. The absence of a flag does not prove clean pocket.
5. **Score differential:** pre-play score; trailing and leading categories show association, not what caused a third-down outcome.

## Wentz: 2025 team-level conversion in five starts

| Week / game | Vikings team 3rd-down conversions |
|---|---:|
| Week 3 vs CIN | 4/12 (33.3%) |
| Week 4 at PIT | 4/14 (28.6%) |
| Week 5 at CLE | 3/9 (33.3%) |
| Week 7 vs PHI | 7/15 (46.7%) |
| Week 8 at LAC | 3/11 (27.3%) |
| **TOTAL** | **21/61 (34.4%)** |

2025 Wentz only: **17 conversions/50 QB third-down dropbacks = 34.0%**. The 11 others team third downs were runs or non-QB-drive plays. Third-and-10+ Wentz: **4 conversions/16 QB dropbacks (25%), with 5 sacks (31.3%)**. Third-and-4–6: 7/14 conversions (50%). The long-distance versus manageable-distance gap deserves an early-down and sack-risk adjustment.

## Sack/recorded-hit warning (pressure not fully available)

| QB sample | Third-down dropbacks | Official sacks | Sack rate | Third downs converted |
|---|---:|---:|---:|---:|
| Wentz, 2025 | 50 | 11 | **22.0%** | 17/50 = **34.0%** |
| Wentz, 2026 W1–2 | 20 | 3 | **15.0%** | 8/20 = **40.0%** |
| Wentz, combined | 70 | 14 | **20.0%** | 25/70 = **35.7%** |
| Allen, 2026 Weeks 1–8 | 58 | 6 | **10.3%** | 25/58 = **43.1%** |

Recorded QB-hit flags in Wentz's **2025** third-down sample: 17 hit-flagged, 1 conversion (5.9%), 11 sacks; 33 without a recorded QB hit, 16 conversions (48.5%). In his **2026 W1–2** appearances: 4 hit-flagged, 1 conversion; 16 with no hit flag, 7 conversions. Combined across both years: **2/21 conversions with a hit flag (9.5%), compared with 23/49 (46.9%) without one**.

**DO NOT translate these into P(convert | charted pressure)**. Hits are only observed subset of pressure, and a sack automatically ends the play. Third-and-long and score state can confound this comparison. It is a clear **sack/contested-dropback warning** to investigate with verified pressure charting.

## Exactly who moved the chains for Wentz on third down?

These are passes **thrown on third down by Wentz**, not total receiver targets or conditional blitz-target rates.

| Receiver | 2025 3D targets; catches; converted | 2026 Wentz 3D targets; catches; converted | Combined chain-moving pattern |
|---|---|---|---|
| Justin Jefferson | 8 targets, 6 catches, 5 first downs | 6 targets, 5 catches, 4 first downs | **14 targets, 11 catches, 9 third-down conversions** |
| T.J. Hockenson | 4 targets, 2 catches, 1 first down | 4 targets, 4 catches, 3 first downs | **8 targets, 6 catches, 4 conversions** |
| Jordan Addison | 2 targets, 1 catch, 1 first down | 4 targets, 1 catch, 1 first down | **6 targets, 2 catches, 2 conversions** |

2025 Wentz also looked to Jalen Nailor six times on third down (two catches/two conversions) and Adam Thielen four times (three catches/three conversions). The lineup is different in 2026. **The fresh 2026 evidence puts Jefferson first and Hockenson second as Wentz's third-down chain movers.** That is stronger mechanism evidence for Hockenson's possible short/middle targets than his raw season yards average, but **does not prove a checkdown or hot-route under pressure** without route-depth and blitz snapshots.

## Other factors controlling possession vs Josh Allen / James Cook

| Unit | Through Week8 2026 third down |
|---|---:|
| Bills offense, all runs and passes | 34/77 = **44.2%** |
| Vikings defense allowed to opposing teams | 27/91 = **29.7%** |
| Vikings offense, primarily Murray at QB | 36/100 = **36.0%** |
| Bills defense allowed | 39/93 = **41.9%** |

The key **counterargument** to an automatic Bills possession advantage: Minnesota's defense is far stronger on third down than Buffalo's defense. A 2025 Wentz 34.4% rate versus Bills 2026 44.2% is **not** an apples-to-apples matchup prediction. On 2026 drives, BUF has **429 pass/run scrimmage plays over 73 recorded offensive drives (5.88/drive)**; MIN has **402/73 (5.51/drive)**. Wentz's five 2025 starts had **304 pass/run plays across 52 drives (5.85/drive)**, similar to BUF's plays/drive. Neither is game-clock time of possession, and different schedules/defenses matter.

**Game-script mechanism:**
- Allen/Cook gains on first/second down (Buffalo 4.79 rush YPC) can **avoid** Minnesota's stingy third-down defense. A Buffalo lead and longer rush-heavy drives could raise Bills offensive play share/time on field and lower total game possessions, benefiting Cook attempts but potentially limiting high BUF receiving volume.
- If Minnesota falls behind and Wentz enters repeated third-and-7+, the source shows a high sack/drive-stall hazard. Fewer sustained drives may decrease total Jefferson/Addison/Hockenson target opportunities even if Wentz's **pass rate per play** increases.
- If Wentz has manageable third downs and is protected, Jefferson and Hockenson's demonstrated 3D conversion roles strengthen volume, including when BUF uses its newly observed high-blitz looks.
- **Buffalo itself** must still convert against a Minnesota defense that allows 29.7% third downs; rushing success and score alone do not guarantee an actual time-of-possession edge.

## Proposed model feature layer and gates

At **every pregame offensive play**, estimate first/second-down success, resulting third-down distance distribution, then joint QB/RB third-down play selection, conditional QB third-down conversion/sack/scramble and drive survival, opponent defensive 3D allowance, and score state. Simulated possession count and pass attempts must be jointly generated **before** distributing player targets, carries or catch depths.

Target opportunity estimate depends on expected **team dropbacks × receiver route participation × QB receiver-target allocation**, with completion efficiency and air yards conditional on pressure and coverage when these have verified denominators.

Keep QB-hit/sack flags distinct from true pressure/blitz, and separate preseason prior QB data from current team quarterback. No fake CB shadow assignments or use of Week9 outcome as predictor. Do not promote this module into the live main model without multiweek holdouts and a prospective freeze.

**Research decision:** Strong reason to build a third-down drive-survival factor and downgrade overconfidence in Wentz third-and-long. **Not** proof Bills will win time of possession or Jefferson/Hockenson unders.
