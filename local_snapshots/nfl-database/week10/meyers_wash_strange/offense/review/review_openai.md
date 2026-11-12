# OpenAI review (gpt-5.5-2026-04-23)

- **High — BAL pressure denominator is wrong/misleading.** Report says BAL defense Wks 1-8 has `N=99/300 charted dropbacks`, sack `17/300`, hit `51/300`. Independent recompute shows **303 BAL dropbacks** and 8 BAL games. If 300 is only non-null FTN charting for blitz/rushers, then sack/QB-hit denominators should not be presented as the same “charted dropbacks” denominator unless those flags are also only known for 300. Label each metric’s denominator separately.

- **High — “Blitz rate” and “5+ rushers” are duplicated suspiciously.** Both are reported as exactly `33.0%, 99/300`, league `31.8%`. That may be true, but it is unlikely enough that it needs audit. In code, `blitz_rate = n_blitzers > 0`; `rush5plus_rate = n_pass_rushers > 4`. If `n_blitzers` means “extra rushers” or is populated only when 5+ rush, then calling it “blitz rate” is OK; otherwise this could conflate two different concepts.

- **High — pressure split is not actual pressure, and some claims overstate it.** The proxy is `qb_hit OR sack OR out_of_pocket OR scramble`; that captures movement/design/scrambles, not necessarily pressure. Claims like “under pressure his share drops” and “top target under pressure” should be explicitly “under pressure proxy,” not treated as charted pressure.

- **High — pressured sack rate is structurally inflated/circular.** The report admits this, but the table still presents “pressured sack rate 20.0%” beside normal splits. Because `sack` defines the pressure proxy, that rate is not comparable to clean/blitz/no-blitz splits and should be footnoted in-table or removed.

- **Medium — “Check-down guy = RB Tuten” is stronger than the data supports.** Code defines checkdowns as `air_yards <= 2`, which includes screens, RPOs, designed flats, and quick throws. The generated notes correctly call it a “shallow target proxy,” but the report upgrades it to “check-down guy.” Use “short/LOS target leader,” not check-down.

- **Medium — screen denominators may be wrong/incomplete.** Report says Washington `2 of 48`, Meyers `3 of 31`, Strange `2 of 35`. Code computes screen rate over `is_screen_pass.dropna()` but reports total targets separately. If any FTN screen flags are missing, “2 of 48” is not the true charted denominator. Need disclose `screen_charted_n`.

- **Medium — “BAL leakiest = middle; tightest = short outside” is unsupported in this excerpt/code.** It is attributed to “defense half,” but no data, denominator, weeks, or source is shown here. Since several player conclusions depend on that defensive-area read, include the BAL defensive table or mark it as external context.

- **Medium — PFF alignment snaps are unaudited by the provided code.** Alignment rows come from `receiver_matchups.csv`, not from `build_a.py`, and there is no validation of player IDs, season/week freshness, whether snaps are routes vs total snaps, or whether PFF free-page data is complete. Treat alignment as third-party scraped context, not a computed fact.

- **Medium — NGS season aggregates are stale/partial versus the rest of the report.** NGS separation/cushion/air-yards share are Weeks 1-6 only, while the main target/snap analysis is Weeks 1-8. The report notes this, but the table header “NGS season aggregates” is misleading; call it “Weeks 1-6 NGS aggregates.”

- **Medium — one-game NGS screenshot route reads are too anecdotal for role claims.** “Meyers: middle-of-field guy,” “Washington lives outside,” etc. are mostly supported by target-location tables, not by route types. Avoid blending “route” language with targeted area; targets are not routes run.

- **Low — “Strange: safest volume/top 3 in all 7 games” needs a team-wide weekly verification.** The report lists weekly targets for only the three players. Code can produce full weekly target ranks, but the report does not show them. If “top 3” means among JAX receivers every week, prove it; if it means among these three, say that.

- **Low — timing/trade claim relies partly on memory.** The code supports “Meyers has JAX roster/PBP receiving involvement in all observed 2026 JAX games.” It does **not** establish the LV→JAX transaction date. The report properly caveats this, but “trade happened in 2025” should be removed or sourced.