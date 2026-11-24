# 80-yard stars: which groups are accurate, why stars missed, why we missed 80-yard games (Nov 23, 2026)

`python3 study.py --data DIR` -> `results.json` (DIR as for `research/game_types_2026-11-16/test_rb.py`).

## Which star group is most accurate
Held-out 2025-26 (weights fitted on 2022-24 only), 22 weeks:

| Stars | Players | Predicted | Hit 80+ | Gap | Receivers (pred/hit) | Backs (pred/hit) |
|---|---|---|---|---|---|---|
| ★★★ | 82 | 55.8% | 51.2% | -4.5 | 55.2 / 57.9 | 56.2 / **45.5** |
| ★★ | 123 | 43.9% | 43.1% | -0.9 | 44.6 / 40.7 | 43.5 / 44.9 |
| ★ | 249 | 34.3% | 34.5% | +0.2 | 34.2 / 30.3 | 34.4 / 38.6 |

★★ and ★ are on target. ★★★ backs ran 11 points hot. With the split-backfield weight below: ★★★ backs 56.9 / 50.0,
★★★ overall 56.1 / 53.8 (gap -2.3), ★★ 44.4 / 45.0, ★ 34.4 / 33.3.

Week 11 Sunday (27 stars): ★★★ 3 of 3, ★★ 4 of 9 (expected 4.0), ★ 5 of 15 (expected 5.1).

## Starred players who missed (15) and the reason
| Reason | Players | Visible before kickoff? | Now in the model |
|---|---|---|---|
| Backup QB | DeVonta Smith (Milton) | Yes | Yes: true-backup factor (research/qb_script_2026-11-22) |
| Poor QB play, veteran | Malik Nabers (McCarthy 18/38) | Partly | No (veteran fill-ins showed no reliable effect) |
| Split backfield | D'Andre Swift, Kyle Monangai, Braelon Allen (75), Jaylen Warren | Yes | Yes: `mate_car` in the backs' star weights (below) |
| Model far above the book's price (15+ points) | Smith, Monangai, Allen | Yes | Yes: stars from the model+price blend; gap flagged |
| Team threw far less than usual | Luther Burden (23 att), Rashee Rice (KC led 27-7), Garrett Wilson (21 att), Amon-Ra St. Brown (28 att) | Not reliably: "big favourite runs more" did not predict 80+ games (z = -1.0) | No |
| Hurt in the game | Bhayshul Tuten | No | No |
| Near misses / normal variance | Bucky Irving 68, Javonte Williams 67, Tetairoa McMillan 71, Carnell Tate 58 | No | No |

## 80-yard games we did not star (10) and the reason
| Reason | Players | Now in the model |
|---|---|---|
| Market rated him higher than we did | Zay Flowers, Jonah Coleman, Derrick Henry, Breece Hall | Blend stars Flowers and Coleman |
| His team threw far more than projected | Khalil Shakir, DJ Moore (BUF: 46 att vs 24 projected), Jakobi Meyers (JAX 47 att) | Game-script refit (research/qb_script_2026-11-22) |
| One long play | Ashton Jeanty (68-yard catch), Jameson Williams (57) | No (not predictable) |
| Not in the projection at all | Jack Bech | No |

## Tested on 2022-2026 (fit 2022-24, held out 2025-26); kept only if log loss and Brier both improve and |z| >= 2
| Candidate | Receivers | Backs |
|---|---|---|
| True backup QB | z -0.8, no gain (the yards factor stays in the simulation, where it did test) | z +1.0, no gain |
| Veteran new starter | z -0.5, no | |
| Point spread (run-heavy favourite) | z -1.0, no | already in |
| Split backfield (other back's carries a game) | | **z -2.1, log loss 0.5809 -> 0.5752, Brier 0.1972 -> 0.1948: kept** |

Stars from the model+price blend: the blend was the most accurate on the held-out weeks 8-9 FanDuel ladders
(`research/watch_model_2026-11-16`, Brier 0.1118 vs 0.1136); Week 11: blend stars 14 of 26, model stars 12 of 27.
Research only.

## Follow-ups from the owner's box-score review (same day)
| Point | What the data says | Change |
|---|---|---|
| Flowers/Henry: what does CAR allow? | CAR ranked 12th vs running backs and among the tougher defenses vs WRs going in: no matchup trigger. RB yards allowed is already one of the backs' star weights (`l_d`). Yards allowed to opposing lead receivers did not predict 80+ games (watch_model_2026-11-16). Henry's 94 came on 13 carries (7.2 a carry). | None |
| Baltimore's QB | The board listed **Tyler Huntley** (schedule file); **Jacoby Brissett** started. | `dashboard/build.py` `starting_qb`: if the listed QB is Out/IR or a game-day inactive, the team's most-used active QB is used. A coach's choice with nobody ruled out still can't be seen before the inactives. |
| Breece Hall vs LAC | LAC ranked 18th vs backs (middle). Hall's 20 carries vs 13.7 projected was the split with Braelon Allen going his way. Rush+receiving yards and touchdown props are not in our book feed yet. | None yet |
| Josh Allen throwing while ahead | Teams with a high pass rate when leading by 7+ threw no more than the refit rule as favourites (2025-26 thirds: 1.00 / 1.00 / 0.99 of expected; 710 favourite games). BUF threw 22 times in Week 10. | None (`research/qb_script_2026-11-22/pass_when_ahead.py`) |
