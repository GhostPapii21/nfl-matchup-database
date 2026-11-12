# v6 GAPS
- **Grok may know results.** grok-4.7's training data may include 2026 and 2025 outcomes. The prompt says to ignore them and the leak test passed, but the reads can't be proven blind. 2025 is labeled HINDSIGHT RISK for this reason.
- **No free historical prop lines.** 2026 Weeks 1–2 and all of 2025 use STAND-IN lines (the as-of median, floor + 0.5) with no prices, so those buckets are hit rate only. Week 2 uses n = 1.
- **Free line source for spreads and totals:** nflverse/nfldata `games.csv` closing lines.
- **2026 Week 1 used 2026 rosters** (players.latest_team) on top of 2025 stats. This is a small roster-hindsight risk.
- **N2 is approximated:** Grok names the primary defender from the pack, with no coverage charting. **N3 is N/A** because there are no period spreads.
- Main lines are treated as the low rung in the depth rule. Weather wasn't saved for Weeks 1–2 or 2025. Pro-edge-scan can't run live, so its inputs were precomputed. The anchor fallback order is pinnacle, circa, betonlineag, then consensus.
- **2025 Week 1 was skipped.** If the Grok allowance runs out, the 2025 weeks without reads stay ungraded; see QUOTA_STOP and the LOCK commit message.
- **API issues:** about 16 timeouts were retried. Concurrency was cut from 16 to 8 workers, and a stream wall-timeout was added.
- **Cost:** the measured cost is about $0.19–0.22 per game. That's a slow and expensive way to get a result that's worse than the baseline.
