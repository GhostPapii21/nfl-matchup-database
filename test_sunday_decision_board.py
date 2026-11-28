"""Decision board: market comparison, red team, and section membership.

The historical DEN@PIT case uses the locked snapshot only. Synthetic cases
cover downgrade, reverse, rejection, and the refusal to fill a pick quota.
"""

from __future__ import annotations

import json
import unittest

from sunday.decision.board import build_board
from sunday.decision.historical import load_packet
from sunday.decision.report import render_markdown

KICKOFF = "2026-11-27T20:00:00+00:00"
STAMP = "2026-11-27T04:26:21+00:00"


def _line(**overrides):
    quote = {
        "book": "fanduel",
        "market": "receptions",
        "subject": "Courtland Sutton",
        "side": "Over",
        "line": 4.5,
        "price": -110,
        "opposite_side": "Under",
        "opposite_price": -110,
        "timestamp_utc": STAMP,
        "reference_only": False,
        "source": "fixture",
    }
    quote.update(overrides)
    return quote


def _thesis(**overrides):
    thesis = {
        "thesis_id": "sutton-receptions",
        "subject": "Courtland Sutton",
        "subject_kind": "player",
        "market": "receptions",
        "side": "Over",
        "opposite_side": "Under",
        "line": 4.5,
        "role_tag": "lead_wr",
        "projection": {"mean": 6.1, "sd": 2.0, "median": 6},
        "script_sensitive": True,
        "models": [
            {"model_id": "opportunity_v1", "probability": 0.71, "n": 20000, "calibration_status": "unfitted"},
            {"model_id": "possession_v0", "probability": 0.69, "n": 20000, "calibration_status": "unfitted"},
        ],
        "evidence_for": [{"text": "target share supports the over", "source": "fixture"}],
        "evidence_against": [],
        "defensive_suppression": [{"path": "single-high", "material": False}],
        "role_volume": {"tag": "lead_wr", "fragile": False, "reason": "stable snap share"},
        "efficiency_dependent": False,
        "contingencies": {
            "injury": {"modeled": True, "invalidates": False, "detail": "active"},
            "weather": {"modeled": True, "invalidates": False, "detail": "dome"},
            "game_script": {"branches_retained": True, "detail": "three scripts retained separately"},
        },
        "sample_quality": {"n": 20000, "withheld": False, "blocks_reads": False, "limitation": ""},
    }
    thesis.update(overrides)
    return thesis


def _packet(*theses, lines=None, **extra):
    return {
        "game_id": "fixture",
        "kickoff_utc": KICKOFF,
        "projection_ready": True,
        "theses": list(theses),
        "lines": list(lines if lines is not None else [_line()]),
        **extra,
    }


class BoardRuleTests(unittest.TestCase):
    def test_strong_read_keeps_probabilities_and_refuses_an_edge_claim(self):
        report = build_board(_packet(_thesis()))
        self.assertFalse(report["projection_ready"])
        self.assertFalse(report["edge_claim_allowed"])
        self.assertEqual(report["caller_projection_ready_ignored"], True)
        self.assertEqual(len(report["board"]["strong_reads"]), 1)
        row = report["board"]["strong_reads"][0]
        self.assertEqual(row["threshold_probability"], 0.69)
        self.assertEqual(row["model_consensus"], "agree")
        self.assertEqual(row["confidence"], "high")
        self.assertEqual(row["role_tag"], "lead_wr")
        self.assertFalse(row["edge_claim"])
        self.assertEqual(row["edge_status"], "COMPARISON_ONLY_NOT_AN_EDGE_CLAIM")
        self.assertAlmostEqual(row["no_vig_probability"], 0.5)
        self.assertAlmostEqual(row["edge"], 0.19)
        self.assertEqual(report["market_snapshots"][0]["models"][0]["probability"], 0.71)
        self.assertNotIn("hit_rate", report)

    def test_minor_contradiction_downgrades_a_strong_read(self):
        thesis = _thesis(evidence_against=[{
            "severity": "minor",
            "text": "a short-area defender is a small efficiency drag",
            "source": "fixture",
        }])
        report = build_board(_packet(thesis))
        self.assertEqual(report["board"]["strong_reads"], [])
        self.assertEqual(report["board"]["soft_leans"][0]["decision"], "downgrade")
        self.assertEqual(report["board"]["soft_leans"][0]["confidence"], "medium")

    def test_reverse_lands_on_a_soft_lean_only_with_its_own_evidence(self):
        thesis = _thesis(
            thesis_id="reverse-supported",
            models=[{"model_id": "opportunity_v1", "probability": 0.42, "n": 20000}],
            opposite_probability=0.58,
            evidence_for=[
                {"text": "the over is the stated side", "source": "fixture"},
                {"text": "the under is supported by the target-share drop", "source": "fixture", "side": "opposite"},
            ],
            evidence_against=[{"severity": "material", "text": "volume moved off this player", "source": "fixture"}],
        )
        report = build_board(_packet(thesis))
        row = report["board"]["soft_leans"][0]
        self.assertEqual(row["decision"], "reverse")
        self.assertEqual(row["original_side"], "Over")
        self.assertEqual(row["side"], "Under")
        self.assertEqual(row["threshold_probability"], 0.58)
        self.assertEqual(report["board"]["strong_reads"], [])

    def test_reverse_then_abstain_does_not_invent_the_other_side(self):
        thesis = _thesis(
            thesis_id="fragile-over",
            market="rushing_yards",
            models=[{"model_id": "opportunity_v1", "probability": 0.36, "n": 20000}],
            role_volume={"tag": "committee_rb", "fragile": True, "reason": "lead back suspended; carries are unsettled"},
            evidence_against=[{"severity": "material", "text": "the carry share is not his", "source": "fixture"}],
        )
        report = build_board(_packet(thesis, lines=[_line(market="rushing_yards")]))
        self.assertEqual(report["board"]["strong_reads"], [])
        self.assertEqual(report["board"]["soft_leans"], [])
        row = report["board"]["avoids"][0]
        self.assertEqual(row["decision"], "reverse_then_abstain")
        self.assertEqual(row["side"], "Over")
        self.assertIn("abstained", " ".join(row["reasons"]))
        self.assertIn("fragility", " ".join(row["reasons"]))

    def test_missing_model_does_not_calculate_implied_or_edge(self):
        thesis = _thesis(models=[], sample_quality={"withheld": True, "blocks_reads": True, "limitation": "withheld"})
        report = build_board(_packet(thesis))
        snapshot = report["market_snapshots"][0]["snapshots"][0]
        self.assertIsNone(snapshot["implied_probability"])
        self.assertIsNone(snapshot["edge"])
        self.assertEqual(snapshot["edge_status"], "NOT_COMPUTED_MODEL_PROBABILITY_ABSENT")
        self.assertEqual(snapshot["price"], -110)
        self.assertFalse(snapshot["missing_line"])
        self.assertEqual(report["board"]["no_plays"][0]["decision"], "reject")
        self.assertIn("NO PLAY", report["board"]["no_plays"][0]["reasons"][0])

    def test_missing_line_is_recorded_and_abstains(self):
        report = build_board(_packet(_thesis(), lines=[]))
        snapshot = report["market_snapshots"][0]["snapshots"][0]
        self.assertTrue(snapshot["missing_line"])
        self.assertIsNone(snapshot["book"])
        self.assertIsNone(snapshot["price"])
        self.assertIsNone(snapshot["timestamp_utc"])
        self.assertIsNone(snapshot["edge"])
        self.assertEqual(snapshot["edge_status"], "NOT_COMPUTED_MISSING_LINE")
        self.assertEqual(report["board"]["no_plays"][0]["decision"], "reject")

    def test_one_sided_price_does_not_produce_an_edge(self):
        report = build_board(_packet(_thesis(), lines=[_line(opposite_price=None)]))
        snapshot = report["market_snapshots"][0]["snapshots"][0]
        self.assertIsNotNone(snapshot["implied_probability"])
        self.assertIsNone(snapshot["edge"])
        self.assertEqual(snapshot["edge_status"], "NOT_COMPUTED_OPPOSITE_PRICE_ABSENT")
        self.assertEqual(report["board"]["strong_reads"], [])

    def test_disagreement_is_not_averaged(self):
        thesis = _thesis(models=[
            {"model_id": "a", "probability": 0.80, "n": 20000},
            {"model_id": "b", "probability": 0.40, "n": 20000},
        ])
        report = build_board(_packet(thesis))
        comparison = report["market_snapshots"][0]
        self.assertEqual(comparison["model_consensus"], "disagree")
        self.assertIsNone(comparison["threshold_probability"])
        self.assertIsNone(comparison["disclosed_mean"])
        self.assertEqual([view["probability"] for view in comparison["models"]], [0.80, 0.40])
        snapshot = comparison["snapshots"][0]
        self.assertIsNone(snapshot["edge"])
        self.assertEqual(snapshot["edge_status"], "NOT_COMPUTED_MODELS_DISAGREE")
        self.assertEqual([item["probability"] for item in snapshot["model_edges"]], [0.80, 0.40])
        self.assertEqual(report["board"]["no_plays"][0]["decision"], "reject")

    def test_probabilities_are_not_shrunk(self):
        high = build_board(_packet(_thesis(models=[{"model_id": "a", "probability": 0.99, "n": 20000}])))
        low = build_board(_packet(_thesis(
            models=[{"model_id": "a", "probability": 0.01, "n": 20000}],
            evidence_against=[],
        )))
        self.assertEqual(high["market_snapshots"][0]["models"][0]["probability"], 0.99)
        self.assertEqual(low["market_snapshots"][0]["models"][0]["probability"], 0.01)
        self.assertEqual(low["board"]["strong_reads"], [])
        self.assertEqual(low["board"]["soft_leans"], [])

    def test_pick_target_is_rejected(self):
        with self.assertRaises(ValueError):
            build_board(_packet(_thesis()), pick_target=3)
        with self.assertRaises(ValueError):
            build_board(_packet(_thesis(), target_picks=5))

    def test_empty_sections_are_kept_when_nothing_clears(self):
        theses = []
        for index in range(8):
            theses.append(_thesis(
                thesis_id=f"weak-{index}",
                subject=f"Player {index}",
                models=[{"model_id": "a", "probability": 0.52, "n": 20000}],
            ))
        lines = [_line(subject=thesis["subject"]) for thesis in theses]
        report = build_board(_packet(*theses, lines=lines))
        self.assertEqual(report["section_counts"]["strong_reads"], 0)
        self.assertEqual(report["section_counts"]["soft_leans"], 0)
        self.assertEqual(report["section_counts"]["no_plays"], 8)

    def test_post_kickoff_quote_is_excluded(self):
        report = build_board(_packet(_thesis(), lines=[_line(timestamp_utc="2026-11-27T21:00:00+00:00")]))
        snapshot = report["market_snapshots"][0]["snapshots"][0]
        self.assertEqual(snapshot["edge_status"], "NOT_COMPUTED_POST_KICKOFF_EXCLUDED")
        self.assertTrue(snapshot["missing_line"])
        self.assertEqual(report["market_snapshots"][0]["rejected_lines"][0]["reject_reason"], "POST_KICKOFF_EXCLUDED")

    def test_input_order_is_preserved(self):
        first = _thesis(thesis_id="first", models=[{"model_id": "a", "probability": 0.57, "n": 20000}])
        second = _thesis(
            thesis_id="second",
            subject="Other",
            models=[{"model_id": "a", "probability": 0.61, "n": 20000}],
        )
        report = build_board(_packet(
            first,
            second,
            lines=[_line(), _line(subject="Other")],
        ))
        self.assertEqual([row["thesis_id"] for row in report["board"]["soft_leans"]], ["first", "second"])


class HistoricalDenPitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = load_packet()
        cls.report = build_board(cls.packet)
        cls.markdown = render_markdown(cls.report)

    def test_sources_are_pregame_snapshots(self):
        paths = [item["path"] for item in self.packet["sources"]]
        self.assertEqual(paths, [
            "snapshots/2026_12_DEN_PIT/20261127T111648Z/summary.json",
            "snapshots/2026_12_DEN_PIT/20261127T111648Z/LOCK.json",
            "snapshots/2026_12_DEN_PIT/20261127T111648Z/inputs/team_prices_from_packet.json",
            "pregame/direct_lines/2026_12_DEN_PIT.json",
        ])
        blob = json.dumps(self.packet["sources"])
        self.assertNotIn("postgame", blob)
        self.assertNotIn("playlogs", blob)

    def test_board_does_not_promote_the_flagged_sim(self):
        self.assertFalse(self.report["projection_ready"])
        self.assertEqual(self.report["board"]["strong_reads"], [])
        self.assertEqual(self.report["board"]["soft_leans"], [])
        self.assertGreater(self.report["section_counts"]["avoids"], 0)
        self.assertGreater(self.report["section_counts"]["no_plays"], 0)
        self.assertNotIn("hit_rate", self.report)

    def test_spread_snapshot_matches_the_lock_and_is_avoided(self):
        comparison = next(
            item for item in self.report["market_snapshots"]
            if item["thesis_id"] == "team:spread:PIT:4.5"
        )
        fanduel = next(snapshot for snapshot in comparison["snapshots"] if snapshot["book"] == "fanduel")
        self.assertEqual(fanduel["price"], -113.0)
        self.assertEqual(fanduel["line"], 4.5)
        self.assertEqual(fanduel["timestamp_utc"], "2026-11-27T04:26:21+00:00")
        self.assertFalse(fanduel["missing_line"])
        self.assertEqual(comparison["models"][0]["probability"], 0.63081)
        self.assertEqual(comparison["models"][0]["calibration_status"], "unfitted")
        self.assertEqual(fanduel["edge_status"], "COMPARISON_ONLY_NOT_AN_EDGE_CLAIM")
        self.assertFalse(fanduel["edge_claim"])
        row = next(row for row in self.report["board"]["avoids"] if row["thesis_id"] == comparison["thesis_id"])
        self.assertIn("AVOID", " ".join(row["reasons"]))
        self.assertIn("model error", " ".join(row["reasons"]).lower())
        self.assertEqual(row["book"], "fanduel")
        pinnacle = next(snapshot for snapshot in comparison["snapshots"] if snapshot["book"] == "pinnacle")
        self.assertTrue(pinnacle["reference_only"])

    def test_moneyline_positive_gap_is_an_abstention(self):
        comparison = next(item for item in self.report["market_snapshots"] if item["market"] == "moneyline")
        fanduel = next(snapshot for snapshot in comparison["snapshots"] if snapshot["book"] == "fanduel")
        self.assertEqual(comparison["models"][0]["probability"], 0.4866)
        self.assertEqual(fanduel["price"], 194.0)
        self.assertLess(comparison["models"][0]["probability"], 0.5)
        self.assertGreater(fanduel["edge"], 0)
        review = next(item for item in self.report["adversarial_reviews"] if item["thesis_id"] == comparison["thesis_id"])
        self.assertEqual(review["decision"], "reverse_then_abstain")
        self.assertEqual(review["section"], "avoids")
        self.assertFalse(review["red_team"]["game_script"]["branches_retained"])
        self.assertFalse(review["red_team"]["injury"]["modeled"])
        text = " ".join(review["reasons"])
        self.assertIn("below one half", text)
        self.assertNotIn(comparison["thesis_id"], [row["thesis_id"] for row in self.report["board"]["strong_reads"]])

    def test_player_price_without_a_model_is_a_no_play(self):
        comparison = next(
            item for item in self.report["market_snapshots"]
            if item["subject"] == "Courtland Sutton" and item["market"] == "receptions"
        )
        snapshot = comparison["snapshots"][0]
        self.assertEqual(snapshot["book"], "fanduel")
        self.assertIsNotNone(snapshot["price"])
        self.assertIsNotNone(snapshot["timestamp_utc"])
        self.assertLess(snapshot["timestamp_utc"], KICKOFF)
        self.assertFalse(snapshot["missing_line"])
        self.assertIsNone(snapshot["implied_probability"])
        self.assertIsNone(snapshot["edge"])
        self.assertEqual(snapshot["edge_status"], "NOT_COMPUTED_MODEL_PROBABILITY_ABSENT")
        row = next(row for row in self.report["board"]["no_plays"] if row["thesis_id"] == comparison["thesis_id"])
        self.assertIn("NO PLAY", row["reasons"][0])
        self.assertEqual(row["role_tag"], "unverified")
        self.assertEqual(row["model_consensus"], "absent")

    def test_missing_passing_yards_line_abstains(self):
        comparison = next(item for item in self.report["market_snapshots"] if item["market"] == "passing_yards")
        snapshot = comparison["snapshots"][0]
        self.assertTrue(snapshot["missing_line"])
        self.assertIsNone(snapshot["price"])
        self.assertIsNone(snapshot["implied_probability"])
        self.assertIsNone(snapshot["edge"])
        self.assertEqual(snapshot["edge_status"], "NOT_COMPUTED_MISSING_LINE")
        review = next(item for item in self.report["adversarial_reviews"] if item["thesis_id"] == comparison["thesis_id"])
        self.assertEqual(review["decision"], "reject")
        self.assertTrue(any("line is also missing" in reason for reason in review["reasons"]))

    def test_markdown_has_the_four_sections_and_the_abstention(self):
        for title in ("Strong Reads", "Soft Leans", "Avoids", "No Plays"):
            self.assertIn(f"### {title}", self.markdown)
        self.assertIn("None.", self.markdown)
        self.assertIn("reverse_then_abstain", self.markdown)
        self.assertIn("NO PLAY", self.markdown)
        self.assertIn("AVOID", self.markdown)
        self.assertIn("projection_ready=false", self.markdown)
        self.assertNotIn("hit_rate", self.markdown)


if __name__ == "__main__":
    unittest.main()
