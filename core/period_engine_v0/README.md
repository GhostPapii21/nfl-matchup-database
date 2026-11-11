# period_engine_v0 (RESEARCH ONLY)

Research code lives at `core/period_engine_v0`. The original worktree branch was `research-period-engine-2026-11-05`.  
Implements staged plan + §9 market mirror. **Not production / not gate PASS / no betting.**

## Models
| Family | Status |
|---|---|
| Monte Carlo | IMPLEMENTED — as-of empirical joint team quarter-vector bootstrap |
| Bias | **UNIMPLEMENTED** |
| Game Randomness | Structure IMPLEMENTED (shared shock); scale UNFITTED |

## Commands
```bash
cd core/period_engine_v0
python3 -m pytest tests/ -q
python3 walkforward.py          # 2026 Wk1–8 walk-forward accuracy (no price edge)
python3 demo_jaxbal_report.py   # screenshot quotes; PINNACLE_MISSING
python3 compare_sampling.py     # independent vs matchup_pair sampler, same as-of walk-forward
```

`simulate_game` options: `sampling="independent"` (default) or `"matchup_pair"` (offence + opponent
defence, keeps real within-game structure); with `apply_gr=True`, `gr_scale="within_game_covariance"`
(default) or `"legacy_total_cv"` (old rule, inflates variance about 2x). See
`docs/EQUATION_AUDIT_2026-11-11.md`.

## Walk-forward policy
For 2026 week W: history = 2025 REG + 2026 weeks < W only. Metrics = genuine test vs as-of pool. **No historical period prices ⇒ no ROI/edge claim.**

## Optional player evidence
`player_evidence.py` + `PLAYER_EVIDENCE_SPEC.md` — Outlier CSV / screenshot ties + MISSING flags for location/defenders/miss audit. Not a prop engine.

## Reviews
`reviews/` — OpenAI, Grok, Codex artifacts; Claude/Google unavailable notes; SYNTHESIS.md
