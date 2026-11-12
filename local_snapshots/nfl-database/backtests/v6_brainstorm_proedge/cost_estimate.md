# v6 Grok cost estimate (written before any v6 call)
Basis: v5 grok-4.7 logged usage: cost_in_usd_ticks per read call ~$0.10-0.16 (75 calls = $7.93 logged; ~$15-17 incl. unlogged killed runs).
v6 prompt is larger (both skills' full steps + pro-edge features + L4 logs per prop): est. +30-40% prompt tokens; reasoning dominates.
- Per game: ~$0.17 per call x ~1.15 (re-prompts on validation reject) = ~$0.20/game.
- 2026 Wk1-8: 16+16 (wk1-2) + 88 (wk3-8) = ~120 games -> ~$24 (range $18-30).
- Hard stop: running spend is checked before every call; stops if spend reaches $40 for 2026 Wk1-8.
- 2025 full regular season (272 games, NOT started, cost-gated): ~272 x $0.20 = ~$55 (range $40-70).
Odds API: 0 credits (ODDS_API_KEY not read).
