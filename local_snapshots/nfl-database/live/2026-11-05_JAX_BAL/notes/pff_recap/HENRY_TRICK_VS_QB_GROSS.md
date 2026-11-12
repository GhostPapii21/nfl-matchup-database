# Henry trick pass (−3) vs Fagnano QB 60 / team gross 57 — verified

## Local ESPN/PBP audit
- Joe Fagnano: **10/18, 60 yds**, 2 INT, 1 sack (−2)
- Trick pass: Direct snap to **D.Henry**, Henry pass to Z.Flowers for **−3** yards (`actual_trick_plays.csv`)

## nflverse PBP `2026_09_JAX_BAL` (pull verify)
| Passer | Completions (passing_yards count) | Sum passing_yards |
|---|---:|---:|
| T.Lawrence | 16 | **242** |
| J.Fagnano | 10 | **60** |
| D.Henry | 1 | **−3** |

## PFF public recap
- QB compare widget: Fagnano **18 att / 10 comp / 60** (QB-only)
- Team passing: BAL completions **11**, gross pass **57**, attempts **19**

## Reconcile (definitional, not an error)
**Team gross BAL 57 = Fagnano 60 + Henry (−3).**  
Fagnano’s **60** is QB passing yards only; Henry’s trick completion is a separate passer in nflverse/ESPN and is included in **team** pass totals (11 completions / 57 gross) but **not** in Fagnano’s individual 60.  
No contradiction once passer identity is split.
