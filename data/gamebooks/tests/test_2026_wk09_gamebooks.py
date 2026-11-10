"""Reconciliation for every official 2026 Week 9 game summary.

Final score from the scoring summary equals the quarter totals.
Team rush and pass totals equal the sum of the individual rows.
"""

import csv
import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from parse_nfl_game_summary import SCHEMAS, parse_game_summary  # noqa: E402

WEEK = REPO / "data" / "gamebooks" / "2026" / "wk09"
MANIFEST = WEEK / "MANIFEST.csv"
SCORE_RE = re.compile(r"^[A-Z]+\s+(\d+),\s+[A-Z]+\s+(\d+)$")


def load_manifest():
    with MANIFEST.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


class Week9GamebooksTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = load_manifest()
        cls.by_id = {row["game_id"]: row for row in cls.manifest}

    def test_manifest_covers_fifteen_games(self):
        self.assertEqual(len(self.manifest), 15)
        self.assertIn("2026_09_BUF_MIN", self.by_id)
        self.assertIn("2026_09_CIN_ATL", self.by_id)
        self.assertTrue((WEEK / "combined" / "play_by_play.csv").exists())

    def test_each_game_reconciles(self):
        combined = {name: [] for name in SCHEMAS}
        for row in self.manifest:
            game_id = row["game_id"]
            folder = WEEK / game_id
            pdf = folder / f"{game_id}_gamebook.pdf"
            text_path = folder / f"{game_id}_gamebook.txt"
            self.assertEqual(hashlib.sha256(pdf.read_bytes()).hexdigest(), row["sha256"], game_id)
            provenance = json.loads((folder / "provenance.json").read_text(encoding="utf-8"))
            self.assertEqual(provenance["source_url"], row["source_url"], game_id)
            self.assertEqual(provenance["pdf_sha256"], row["sha256"], game_id)
            self.assertEqual(provenance["pdf_pages"], int(row["pages"]), game_id)
            self.assertIn("prohibited without the written permission", provenance["copyright_notice"])
            text = text_path.read_text(encoding="utf-8")
            tables = parse_game_summary(text, game_id, 9)
            for name, fields in SCHEMAS.items():
                loaded = read_csv(folder / "parsed" / f"{name}.csv")
                self.assertEqual(loaded, tables[name], f"{game_id} {name}")
                if loaded:
                    self.assertEqual(list(loaded[0].keys()), fields)
                combined[name].extend(loaded)
            self._reconcile(game_id, tables, row)
            gaps = [g["gap_id"] for g in tables["parse_gaps"] if g["severity"] == "gap"]
            self.assertEqual(gaps, ["longest_plays_unparsed"], game_id)

        for name, records in combined.items():
            on_disk = read_csv(WEEK / "combined" / f"{name}.csv")
            self.assertEqual(len(on_disk), len(records), name)
            self.assertIn("nflverse_game_id", SCHEMAS[name])
            for game_id in self.by_id:
                disk_rows = [r for r in on_disk if r["nflverse_game_id"] == game_id]
                parsed_rows = [r for r in records if r["nflverse_game_id"] == game_id]
                self.assertEqual(disk_rows, parsed_rows, f"{name} {game_id}")

    def test_madrid_header(self):
        text = (WEEK / "2026_09_CIN_ATL" / "2026_09_CIN_ATL_gamebook.txt").read_text(encoding="utf-8")
        self.assertTrue(text.lstrip().startswith("2026 Madrid Game"))
        meta = read_csv(WEEK / "2026_09_CIN_ATL" / "parsed" / "game_meta.csv")[0]
        self.assertEqual(meta["venue"], "Bernabéu Stadium, Madrid, Spain")
        self.assertIn("Retractable Roof - Closed", meta["roof"])
        self.assertEqual(meta["visitor_final"], "34")
        self.assertEqual(meta["home_final"], "17")
        self.assertEqual(meta["start_time"], "3:34 PM CET")

    def test_overtime_browns_saints(self):
        scores = read_csv(WEEK / "2026_09_CLE_NO" / "parsed" / "quarter_scores.csv")
        by = {(r["team_abbr"], r["quarter"]): int(r["points"]) for r in scores}
        self.assertEqual(by[("CLV", "OT")] + by[("CLV", "1")] + by[("CLV", "2")] + by[("CLV", "3")] + by[("CLV", "4")], 22)
        self.assertEqual(by[("NO", "OT")], 7)
        self.assertEqual(by[("NO", "Total")], 23)
        plays = read_csv(WEEK / "2026_09_CLE_NO" / "parsed" / "play_by_play.csv")
        self.assertTrue(any(r["quarter"] == "OT" and r["row_kind"] == "scrimmage" for r in plays))

    def _reconcile(self, game_id, tables, manifest_row):
        meta = tables["game_meta"][0]
        expected = SCORE_RE.match(manifest_row["final_score_from_pdf"])
        self.assertIsNotNone(expected, manifest_row["final_score_from_pdf"])
        self.assertEqual(meta["visitor_final"], expected.group(1), game_id)
        self.assertEqual(meta["home_final"], expected.group(2), game_id)
        final_stat = [
            r for r in tables["team_stats"]
            if r["scope"] == "final" and r["stat"] == "FINAL SCORE"
        ]
        self.assertEqual(len(final_stat), 1, game_id)
        self.assertEqual((final_stat[0]["visitor"], final_stat[0]["home"]),
                         (meta["visitor_final"], meta["home_final"]), game_id)
        last = tables["scoring_plays"][-1]
        self.assertEqual((last["visitor_score"], last["home_score"]),
                         (meta["visitor_final"], meta["home_final"]), game_id)
        for abbr, final in (
            (meta["visitor_abbr"], int(meta["visitor_final"])),
            (meta["home_abbr"], int(meta["home_final"])),
        ):
            by = {r["quarter"]: int(r["points"]) for r in tables["quarter_scores"] if r["team_abbr"] == abbr}
            self.assertEqual(by["1"] + by["2"] + by["3"] + by["4"] + by["OT"], final, f"{game_id} {abbr}")
            self.assertEqual(by["Total"], final, f"{game_id} {abbr}")
            for table, fields in (("rushing", ("att", "yds")), ("passing", ("att", "cmp", "yds"))):
                players = [
                    r for r in tables[table]
                    if r["scope"] == "final" and r["team_abbr"] == abbr and r["is_total"] == "false"
                ]
                totals = [
                    r for r in tables[table]
                    if r["scope"] == "final" and r["team_abbr"] == abbr and r["is_total"] == "true"
                ]
                self.assertEqual(len(totals), 1, f"{game_id} {table} {abbr}")
                for field in fields:
                    self.assertEqual(
                        sum(int(r[field]) for r in players),
                        int(totals[0][field]),
                        f"{game_id} {table} {abbr} {field}",
                    )


if __name__ == "__main__":
    unittest.main()
