from sunday.joinflow import _player_theses

def test_skill_players_and_evidence_are_joined_without_fake_probabilities():
    distribution = {"status": "OK", "mean": 63.0, "thresholds": {"50": 0.7}}
    players = {"teams": [{"team": "A", "players": [
        {"player": "Receiver", "player_id": "wr1", "pos": "WR",
         "projections": {"receiving": {"receiving_yards": distribution}},
         "situational": {"pressure_targets": {"evidence_tier": "inferred"}}},
        {"player": "Runner", "player_id": "rb1", "pos": "RB",
         "projections": {"rushing": {"rushing_yards": distribution},
                         "td_opportunity": {"status": "VOLUME_ONLY"}}},
        {"player": "Tight end", "player_id": "te1", "pos": "TE",
         "projections": {"receiving": {"receptions": {"mean": 4}}}},
    ]}]}
    rows = {r["thesis_id"]: r for r in _player_theses(players, None)}
    assert rows["player:wr1:rec_yds"]["projection"] == distribution
    assert rows["player:wr1:rec_yds"]["joined_evidence"]["pressure_targets"]["evidence_tier"] == "inferred"
    assert "player:rb1:rush_yds" in rows
    assert "player:rb1:td_opportunity" in rows
    assert "player:te1:receptions" in rows
    assert all(r["models"] == [] and r["sample_quality"]["blocks_reads"] for r in rows.values())
