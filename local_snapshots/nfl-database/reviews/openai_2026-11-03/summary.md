# OpenAI review — top 10 actionable ideas (gpt-5.5-2026-04-23, Nov 3 2026)
Source: response.md (two calls; the 10k tokens/min account cap forced a compact brief (brief_compact.md: the summary plus the first 1,700 characters of each report) and low reasoning effort; high effort used all 4,800 output tokens on reasoning and returned no text). Usage: usage_log.jsonl.

Overall verdict: the market is beating our model. Every result so far is too small to prove an edge, and rule changes made after seeing results make it worse. Switch to a single-leg loop measured on closing-line value (CLV) first, and treat parlays as a later step.

1. **Freeze each week's protocol before kickoff** (candidates, lines, probabilities, pass/fail reasons, hashes). No rule edits mid-week. A holdout week we've already dissected stops being blind. [test-design-only]
2. **Make CLV the main score**, with hit rate and ROI second. Did our side beat the closing line or price? [test-design-only; needs Odds API close snapshots, see pushback]
3. **Shrink model probabilities hard toward the market:** p = w·model + (1−w)·no-vig, with w ≤ 0.1–0.2, set in advance and not tuned weekly. The model said 67% on legs that hit 48.5%. [needs-Rico-OK: replaces NOSHRINK]
4. **Kill any sim version whose Brier score is worse than the market's.** All 9 are, so sims become a source of inputs, not the source of probabilities, and full opponent adjustment is dropped. [needs-Rico-OK: also settles the pending oppadj 0.5/1.0 call]
5. **Take rules that depend on data we don't have out of the rulebook** (film, defender matchups, coverage), or mark that version as not backtestable. SCHEME_EDGE overrides went 20–34. [needs-Rico-OK]
6. **Power math:** proving a 56% leg hit rate at −110 needs about 1,500 legs, and 60% needs about 350. A 3-leg slip breaks even at 14.4%, a 4-leg at 7.5%. Our 34-, 50- and 293-leg samples can only rule out huge overconfidence. [test-design-only]
7. **Strict leak protocol for LLM reads:** masked teams, players and dates; no postmortems in context; structured output; a manifest with prompt, input and output hashes. v5's 43.8% → 60.8% flip is "suspicious" until the masked rerun holds. [test-design-only]
8. **Let the LLM add tags, not pick bets.** Compare the baseline model, baseline plus LLM tags, and baseline plus shuffled tags as a placebo. Keep the tags only if they improve CLV, Brier or log loss out of sample. [test-design-only]
9. **Build slips by shared failure mode:** tag each leg (e.g. 4Q run-out, needs a shootout, depends on a big play). No more than 2 legs with the same failure mode, no more than one same-game pair in a 3-leg slip, no more than one depth WR, and a correlation haircut of 3–20% on the slip probability. [needs-Rico-OK: slip-building rule]
10. **Per-game checklist on free data:** price/no-vig/line move → role (snaps, routes, target or carry share, trend) → same QB → team total, pace, pass rate → broad opponent allowances, shrunk → spread-driven script risk → is the line clearable with normal volume, not a ceiling game. [needs-Rico-OK if it replaces phase steps; test-design-only as a shadow run]

## Pushback (where it conflicts with our data or constraints)
- **CLV snapshots:** it suggests 3 snapshots a week across slates. With about 250 credits a week, we can afford one pick-time pull plus one near-close pull, only for games we'd bet. CLV on every candidate isn't affordable before December.
- **Masked prompts:** masking removes exactly what our reads use (injury news, depth chart, QB identity). Use masking for leak testing only, and run live picks unmasked (live picks can't leak anyway).
- **Rush-yds unders (76.9%):** it calls this small-sample. That's fair, but it's our strongest pocket. Keep it as a pre-registered hypothesis for Weeks 10+ instead of dropping it.
- **"Single legs first":** Rico plays FanDuel/PrizePicks slips. Run single-leg grading alongside paper slips rather than stopping slips.
- **Sample sizes of 1,000+ legs** won't arrive this season at about 5 slips a week. Using CLV mostly gets around this, because CLV shows up in far fewer legs.
- **Unsure (its own words):** whether Grok memorized 2026 results, the correlation haircut sizes, and whether FanDuel/PrizePicks already price same-game correlation.
