# Actual role / coverage audit — JAX @ BAL Final (evidence only)

- Written: **2026-11-06 05:30:14 ET** (America/New_York)
- Event `401873037` Final **JAX 33–BAL 10** (NFL Week 9)
- **Ghost6 owns engine reruns — this pass did not run or edit the engine.**
- Coverage on all targets: **UNKNOWN**. Routes / 11-12-13 personnel: **MISSING**.

## Artifacts (for Ghost6 independent model audit)
| File | Contents |
|------|----------|
| `actual_receiving_by_quarter.csv` | Target/catch/yard shares by team & quarter |
| `actual_receiving_play_log.csv` | Play-level targets; No Play / INT / fumble flags |
| `actual_rushing_by_quarter.csv` | Named RB carry/yard shares + other rush kinds |
| `actual_rushing_play_log.csv` | Every rush with parsed carrier + kind (incl. aborted_snap) |
| `actual_explosives_ledger.csv` | Pass≥20 / rush≥10; coverage UNKNOWN |
| `actual_box_reconcile.csv` | PBP vs ESPN box |
| `actual_jax_rb_touch_order.csv` | Chronological JAX RB touches |
| `actual_trick_plays.csv` | Henry trick pass |
| `actual_role_coverage_audit.md` | This note |

## Receiving reconcile
- JAX Jakobi Meyers: box 6/4/65 · pbp 6/4/65.0 → **VERIFIED**
- JAX Parker Washington: box 7/2/61 · pbp 7/2/61.0 → **VERIFIED**
- JAX Nate Boerkircher: box 3/2/61 · pbp 3/2/61.0 → **VERIFIED**
- JAX Brenton Strange: box 2/2/22 · pbp 2/2/22.0 → **VERIFIED**
- JAX Tanner Koziol: box 2/2/15 · pbp 2/2/15.0 → **VERIFIED**
- JAX Chris Rodriguez Jr.: box 2/2/13 · pbp 2/2/13.0 → **VERIFIED**
- JAX Josh Cameron: box 1/1/6 · pbp 1/1/6.0 → **VERIFIED**
- JAX LeQuint Allen Jr.: box 2/0/0 · pbp 2/0/0.0 → **VERIFIED**
- JAX Travis Hunter: box 1/1/-1 · pbp 1/1/-3.0 → **YARDS_SRC_DISCREPANCY** — PBP text "for -3 yards" then FUMBLES; ESPN box REC YDS=-1. Agree 1 tgt/1 rec. Keep both values for Ghost6.
- BAL Mark Andrews: box 2/2/19 · pbp 2/2/19.0 → **VERIFIED**
- BAL LaJohntay Wester: box 1/1/14 · pbp 1/1/14.0 → **VERIFIED**
- BAL Justice Hill: box 3/3/7 · pbp 3/3/7.0 → **VERIFIED**
- BAL Rashod Bateman: box 2/1/6 · pbp 2/1/6.0 → **VERIFIED**
- BAL Zay Flowers: box 6/3/6 · pbp 6/3/6.0 → **VERIFIED**
- BAL Matt Hibner: box 2/1/5 · pbp 2/1/5.0 → **VERIFIED**

## Rushing reconcile
- JAX Ameer Abdullah: box 7 car/30 yds · pbp 7/30.0 → **VERIFIED**
- JAX Bhayshul Tuten: box 12 car/29 yds · pbp 12/29.0 → **VERIFIED**
- JAX Chris Rodriguez Jr.: box 10 car/19 yds · pbp 10/19.0 → **VERIFIED**
- JAX Trevor Lawrence: box 1 car/-1 yds · pbp 1/-1.0 → **VERIFIED**
- BAL Justice Hill: box 9 car/85 yds · pbp 9/85.0 → **VERIFIED**
- BAL Derrick Henry: box 17 car/57 yds · pbp 17/57.0 → **VERIFIED**
- BAL Zay Flowers: box 3 car/17 yds · pbp 3/17.0 → **VERIFIED**
- BAL Joe Fagnano: box 3 car/13 yds · pbp 3/13.0 → **VERIFIED** — includes aborted_snap as 1 car / 0 yds (matches ESPN box convention)
- BAL Mark Andrews: box 2 car/0 yds · pbp 2/0.0 → **VERIFIED** — includes aborted_snap as 1 car / 0 yds (matches ESPN box convention)

### Counts: VERIFIED 23 · flagged 1

## Scrambles / kneels / trick / aborted
- Rush kind counts: {'rb_carry': 55, 'non_rb_rush': 4, 'qb_rush': 1, 'kneel': 1, 'qb_scramble': 1, 'aborted_snap': 2}
- Trick pass: Q1 7:38 — (Shotgun) Direct snap to D.Henry.  D.Henry pass short middle to Z.Flowers to JAX 37 for -3 yards (T.Walker, V.Miller).
- Aborted snap (box rush): Q3 4:25 Joe Fagnano — J.Fagnano FUMBLES (Aborted) at JAX 46, and recovers at JAX 47. J.Fagnano to JAX 45 for 2 yards (V.Miller).
- Aborted snap (box rush): Q3 3:07 Mark Andrews — M.Andrews FUMBLES (Aborted) at JAX 41, and recovers at JAX 41.
- Classification: direct-snap RB who then runs = `rb_carry` (not gadget). Flowers end-around after Direct snap to Henry = `non_rb_rush`. QB designed run = `qb_rush`; scramble = `qb_scramble`; kneel = `kneel`.

## First third-RB touch (JAX)
Pregame (`week10/jax_usage/usage.md`): Tuten RB1; **Rodriguez = RB2 / next man up**; Allen receiving back; **Abdullah mostly garbage-time**. No announcement assumed.
- First touch by distinct RBs: Bhayshul Tuten Q1 13:31 (rush), Chris Rodriguez Jr. Q1 12:04 (rush), Ameer Abdullah Q4 12:39 (rush)
- **First third-RB touch:** **Ameer Abdullah** · Q4 12:39 · rush · 2.0 yds — A.Abdullah right end pushed ob at BLT 15 for 2 yards (T.Tampa).
- Matches pregame RB3/garbage-time profile for Abdullah (4th quarter, JAX already up big).

## Explosives (coverage UNKNOWN; no tackler→coverage)
- Q1 14:17 JAX PASS **52.0** · N.Boerkircher · coverage **UNKNOWN**
- Q2 0:58 JAX PASS **50.0** · P.Washington · coverage **UNKNOWN**
- Q4 7:15 BAL RUSH **65.0** · Justice Hill · coverage **UNKNOWN**

## Highlight evidence (corrected)
- NFL.com: https://www.nfl.com/videos/jaguars-vs-ravens-highlights-week-9
- Local MP4: `notes/evidence_nov5/espn_jaguars_ravens_highlights_wsc.mp4`
- **Correction:** highlight clip **omits TE catches**; **no** confirmed Strange blocking; **no** per-play personnel from clip.
- NFL.com blurb text mentioned Boerkircher 52-yard completion (page text only — not a film review by this agent).

## Missing for Ghost6 (routes 12/13)
- Route charting; **11/12/13 personnel per play**; coverage IDs
- Week 9 participation file (upstream still missing)
- Full official film — only highlight package available here

## Provenance
- `/workspace/nfl-database/live/2026-11-05_JAX_BAL/pbp_live.csv` final ESPN-backed log
- Box: ESPN summary `raw/espn_summary_401873037.json` Final boxscore
- Pregame RB roles: `week10/jax_usage/usage.md`
- Prior TE snap/package note: `notes/te_usage_comparison.md` + gamebook PDF
