import csv, datetime as dt, json, os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import pull_odds as P

NOW = dt.datetime(2026, 11, 5, 23, 0, tzinfo=dt.timezone.utc)
EV = {"id": "e1", "away_team": "A", "home_team": "B", "commence_time": "2026-11-06T01:15:00Z"}
def ev_odds(upd="2026-11-05T22:55:00Z"):
    mk = lambda k, outs: {"key": k, "last_update": upd, "outcomes": outs}
    return dict(EV, bookmakers=[
        {"key": "fanduel", "last_update": upd, "markets": [
            mk("player_receptions", [{"name": "Over", "description": "X Y", "point": 4.5, "price": -120}]),
            mk("spreads_h1", [{"name": "A", "point": 1.5, "price": -110}, {"name": "B", "point": -1.5, "price": -110}]),
            mk("h2h", [{"name": "A", "price": 150}, {"name": "B", "price": -170}])]},
        {"key": "pinnacle", "last_update": upd, "markets": [mk("totals_q1", [{"name": "Over", "point": 10.5, "price": -105}])]}])

class Markets(unittest.TestCase):
    def test_props_and_alts_kept(self):
        for m in ["player_pass_yds", "player_reception_yds", "player_rush_yds", "player_receptions", "player_rush_reception_yds",
                  "player_pass_completions", "player_reception_yds_alternate", "player_rush_yds_alternate"]:
            self.assertIn(m, P.PROP_MARKETS)
    def test_game_and_period_markets(self):
        for m in ["h2h", "spreads", "totals", "alternate_spreads", "alternate_totals", "team_totals"]:
            self.assertIn(m, P.GAME_MARKETS)
        for per in ["h1", "h2", "q1", "q2", "q3", "q4"]:
            for b in ["h2h", "spreads", "totals"]:
                self.assertIn(f"{b}_{per}", P.GAME_MARKETS)
    def test_books_include_fd_dk_pinnacle_and_prior(self):
        for b in ["fanduel", "draftkings", "pinnacle", "prizepicks", "underdog"]: self.assertIn(b, P.BOOKS)

class Checkpoint(unittest.TestCase):
    def test_labels(self):
        c = dt.datetime(2026, 11, 6, 1, 15, tzinfo=dt.timezone.utc)
        self.assertEqual(P.checkpoint(c - dt.timedelta(minutes=30), c, done=["open"]), "T-30")
        self.assertEqual(P.checkpoint(c - dt.timedelta(minutes=118), c, done=["open"]), "T-120")
        self.assertEqual(P.checkpoint(c - dt.timedelta(hours=20), c, done=[]), "open")
        self.assertEqual(P.checkpoint(c - dt.timedelta(minutes=5), c, done=["open"]), "close")
        self.assertIsNone(P.checkpoint(c + dt.timedelta(minutes=1), c, done=["open"]))

class Rows(unittest.TestCase):
    def test_split_props_game_and_legacy_columns(self):
        props, game, stale = P.rows_from_event(ev_odds(), NOW, label="open", max_age_min=30)
        self.assertEqual(P.COLS[:9], ["game", "book", "market", "player", "side", "point", "price", "last_update_utc", "inplay"])
        self.assertEqual([r["market"] for r in props], ["player_receptions"])
        self.assertEqual(sorted(r["market"] for r in game), ["h2h", "h2h", "spreads_h1", "spreads_h1", "totals_q1"])
        self.assertEqual(props[0]["snapshot"], "open"); self.assertEqual(props[0]["pulled_utc"], "2026-11-05T23:00:00Z")
        self.assertEqual(props[0]["quote_age_min"], 5.0); self.assertFalse(stale)
    def test_max_quote_age_enforced(self):
        props, game, stale = P.rows_from_event(ev_odds("2026-11-05T22:00:00Z"), NOW, label="open", max_age_min=30)
        self.assertEqual(props, []); self.assertEqual(game, []); self.assertEqual(len(stale), 6)
    def test_inplay_quotes_dropped(self):
        props, game, stale = P.rows_from_event(ev_odds("2026-11-06T01:20:00Z"), NOW + dt.timedelta(hours=3), "close", 30)
        self.assertEqual(props + game, [])

class Plan(unittest.TestCase):
    def test_plan_prints_estimate_without_calls(self):
        calls = []
        p = P.plan([EV, dict(EV, id="e2")], P.PROP_MARKETS + P.GAME_MARKETS, P.BOOKS)
        self.assertEqual(p["estimate"], 2 * (len(P.PROP_MARKETS) + len(P.GAME_MARKETS)))

class Run(unittest.TestCase):
    def test_run_writes_files_snapshots_and_quota_log(self):
        d = tempfile.mkdtemp()
        def fetch(path, **q):
            if path.endswith("/events"): return [EV], {}
            return ev_odds(), {"x-requests-remaining": "9000", "x-requests-used": "1000", "x-requests-last": "35"}
        out = P.run("t1", "2026-11-06T00:00:00Z", "2026-11-06T06:00:00Z", out=d, fetch=fetch, now=NOW, label=None)
        self.assertEqual(out["status"], "ok")
        for f in ["odds_t1.csv", "odds_t1_game.csv", "odds_t1_meta.json", "quota_log.csv", "snapshots/odds_snapshots.csv"]:
            self.assertTrue(os.path.exists(os.path.join(d, f)), f)
        self.assertEqual(next(csv.reader(open(os.path.join(d, "odds_t1.csv"))))[:9], P.COLS[:9])
        self.assertEqual(len(list(csv.DictReader(open(os.path.join(d, "snapshots/odds_snapshots.csv"))))), 6)
        self.assertEqual(json.load(open(os.path.join(d, "odds_t1_meta.json")))["remaining"], "9000")
    def test_run_stops_at_floor(self):
        d = tempfile.mkdtemp(); hit = []
        def fetch(path, **q):
            hit.append(path)
            if path.endswith("/events"): return [EV], {"x-requests-remaining": "50", "x-requests-used": "9950"}
            raise AssertionError("must not call odds")
        out = P.run("t2", "2026-11-06T00:00:00Z", "2026-11-06T06:00:00Z", out=d, fetch=fetch, now=NOW)
        self.assertEqual(out["status"], "stopped_quota_floor"); self.assertEqual(len(hit), 1)
    def test_dry_run_makes_no_odds_calls(self):
        d = tempfile.mkdtemp(); hit = []
        def fetch(path, **q):
            hit.append(path); return [EV], {}
        out = P.run("t3", "2026-11-06T00:00:00Z", "2026-11-06T06:00:00Z", out=d, fetch=fetch, now=NOW, dry_run=True)
        self.assertEqual(out["status"], "dry_run"); self.assertEqual(hit, ["/sports/americanfootball_nfl/events"])
    def test_secret_not_in_errors(self):
        d = tempfile.mkdtemp()
        def fetch(path, **q):
            if path.endswith("/events"): return [EV], {}
            raise RuntimeError("boom apiKey=SECRETVALUE")
        os.environ["ODDS_API_KEY"] = "SECRETVALUE"
        try:
            P.run("t4", "2026-11-06T00:00:00Z", "2026-11-06T06:00:00Z", out=d, fetch=fetch, now=NOW)
        finally: del os.environ["ODDS_API_KEY"]
        self.assertNotIn("SECRETVALUE", open(os.path.join(d, "odds_t4_meta.json")).read())

if __name__ == "__main__": unittest.main()
