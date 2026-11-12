import sys; sys.path.insert(0, "/workspace/nfl-database/tools")
import pull_odds as P
P.PROP_MARKETS = []; P.GAME_MARKETS = ["h2h", "spreads", "totals"]
dry = "--dry-run" in sys.argv
r = P.run(sys.argv[1], sys.argv[2], sys.argv[3], out="/workspace/nfl-database/runs/line_movement_wk10",
          label=sys.argv[4], books=["fanduel", "draftkings", "pinnacle"], dry_run=dry, week=10, season=2026)
print(r)
