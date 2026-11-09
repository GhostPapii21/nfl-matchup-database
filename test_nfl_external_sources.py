"""Offline NFL connector boundary tests. No provider network calls."""
import json
import unittest
from unittest.mock import patch

from source_adapters.nfl_external_sources import (
    SPORT, HTTP, PROVIDERS, catalog, fetch_http, get_sportsdataverse_module,
)


class NFLOnlySourceTests(unittest.TestCase):
    def test_all_sources_are_nfl_only(self):
        self.assertEqual(SPORT, "NFL")
        items = catalog()
        self.assertTrue(items)
        self.assertTrue(all(item["sport"] == "NFL" for item in items))
        self.assertTrue(all(item["provider"] in PROVIDERS for item in items))
        self.assertFalse(any("nba" in key for key in PROVIDERS))
        self.assertTrue(all(v["base"].startswith("https://") for v in HTTP.values()))

    def test_fetch_requires_explicit_opt_in(self):
        with self.assertRaises(PermissionError):
            fetch_http("balldontlie_nfl", "games", key="test-secret", transport=lambda req: b'{}')
        with self.assertRaises(PermissionError):
            get_sportsdataverse_module()

    def test_secret_missing_is_not_silent_or_fetched(self):
        with patch.dict("os.environ", {"NFL_BDL_API_KEY": ""}):
            with self.assertRaisesRegex(PermissionError, "NFL_BDL_API_KEY"):
                fetch_http("balldontlie_nfl", "games", enabled=True,
                           transport=lambda req: self.fail("network not allowed"))

    def test_rejects_unknown_resource_and_cross_league_parameter(self):
        with self.assertRaises(ValueError):
            fetch_http("balldontlie_nfl", "nba/games", key="fake",
                       enabled=True, transport=lambda req: b'{}')
        with self.assertRaisesRegex(ValueError, "cross-sport"):
            fetch_http("balldontlie_nfl", "games", params={"league": "NBA"},
                       key="fake", enabled=True, transport=lambda req: b'{}')

    def test_mock_authenticated_nfl_fetch_has_provenance(self):
        def mocked_transport(req):
            self.assertIn("api.balldontlie.io/nfl/v1/games", req.full_url)
            self.assertEqual(req.get_header("Authorization"), "fake-test-key")
            self.assertEqual(req.get_method(), "GET")
            return json.dumps({"data": [{"id": 12}]}).encode()
        result = fetch_http("balldontlie_nfl", "games",
                            params={"season": 2026}, enabled=True,
                            key="fake-test-key", transport=mocked_transport)
        self.assertEqual(result["sport"], "NFL")
        self.assertEqual(result["data"]["data"][0]["id"], 12)
        self.assertTrue(result["research_only"])
        self.assertIsNone(result["source_effective_asof_utc"])
        self.assertNotIn("fake-test-key", json.dumps(result))

    def test_mock_api_sports_nfl_host(self):
        expected = "v1.american-football.api-sports.io"
        def mocked(req):
            self.assertIn(expected, req.full_url)
            self.assertEqual(req.get_header("X-apisports-key"), "fake-test-key")
            return b'{"response":[]}'
        r = fetch_http("api_sports_nfl", "games", enabled=True,
                       key="fake-test-key", transport=mocked)
        self.assertEqual(r["sport"], "NFL")

    def test_oversize_or_non_json_rejected(self):
        with self.assertRaises(ValueError):
            fetch_http("balldontlie_nfl", "teams", enabled=True, key="fake",
                       transport=lambda req: b'a'*2_000_001)
        with self.assertRaises(json.JSONDecodeError):
            fetch_http("balldontlie_nfl", "teams", enabled=True, key="fake",
                       transport=lambda req: b'<html>')


if __name__ == "__main__":
    unittest.main()
