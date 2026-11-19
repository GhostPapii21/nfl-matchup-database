import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fair_price as F  # noqa: E402
import ladder as L  # noqa: E402
import clv as C  # noqa: E402


def test_devig_sums_to_one_and_removes_vig():
    po, pu = F.devig(-110, -110)
    assert abs(po - 0.5) < 1e-9 and abs(po + pu - 1) < 1e-9
    po, pu = F.devig(-150, 120)
    assert 0.5 < po < F.implied(-150)


def test_names_match_across_books():
    assert F.norm_name("Marvin Harrison Jr.") == F.norm_name("Marvin Harrison")
    assert F.norm_name("Ja'Marr Chase") == F.norm_name("JaMarr Chase")


def test_edge_only_on_same_line():
    doc = {"game_id": "g", "rows": [
        {"book": "pinnacle", "market": "receptions", "player": "A B", "side": "Over", "line": 4.5, "american": -110},
        {"book": "pinnacle", "market": "receptions", "player": "A B", "side": "Under", "line": 4.5, "american": -110},
        {"book": "draftkings", "market": "receptions", "player": "A B", "side": "Over", "line": 4.5, "american": 110},
        {"book": "draftkings", "market": "receptions", "player": "A B", "side": "Over", "line": 5.5, "american": 200}]}
    _, edges, c = F.game_edges(doc)
    assert len(edges) == 1 and edges[0]["line"] == 4.5 and abs(edges[0]["edge"] - (0.5 - 100 / 210)) < 1e-3
    assert c["line_mismatch"] == 1


def test_line_shift_uses_distribution_and_marks_reference_line():
    doc = {"game_id": "g", "rows": [
        {"book": "pinnacle", "market": "receiving_yards", "player": "A B", "side": "Over", "line": 50.5, "american": -110},
        {"book": "pinnacle", "market": "receiving_yards", "player": "A B", "side": "Under", "line": 50.5, "american": -110},
        {"book": "draftkings", "market": "receiving_yards", "player": "A B", "side": "Over", "line": 40.5, "american": 100},
    ]}
    model = {"receiving_yards|WR|mid": {"n": 100, "n_positive": 95, "zero_mass": 0.05, "shape": 2.0}}
    contexts = {"g|a b": {"position": "WR", "adot": 8.0}}
    _, edges, counts = F.game_edges(doc, distribution=model, player_contexts=contexts)
    assert len(edges) == 1
    assert edges[0]["line_shifted"] is True
    assert edges[0]["pinnacle_line"] == 50.5
    assert counts["line_shifted"] == 1


def test_open_close_selection_uses_first_and_last_pregame_prices():
    from datetime import datetime, timezone

    kickoff = datetime(2026, 11, 20, 1, 0, tzinfo=timezone.utc)
    as_of = datetime(2026, 11, 20, 2, 0, tzinfo=timezone.utc)
    observations = [
        {"time": datetime(2026, 11, 19, 18, 0, tzinfo=timezone.utc), "american": -110},
        {"time": datetime(2026, 11, 19, 22, 0, tzinfo=timezone.utc), "american": -130},
        {"time": datetime(2026, 11, 20, 1, 1, tzinfo=timezone.utc), "american": -150},
    ]
    selected = C.select_open_last(observations, kickoff, as_of)
    assert selected["status"] == "closed"
    assert selected["open"]["american"] == -110
    assert selected["last"]["american"] == -130
    assert abs(selected["clv"] - (F.implied(-130) - F.implied(-110))) < 1e-12


def test_features_exclude_current_and_future_weeks():
    import pandas as pd

    history = pd.DataFrame([
        {"season": 2022, "week": 1, "player_id": "p", "market": "receiving_yards", "yards": 40.0, "opportunities": 5, "air_yards": 50.0},
        {"season": 2022, "week": 2, "player_id": "p", "market": "receiving_yards", "yards": 60.0, "opportunities": 5, "air_yards": 50.0},
        {"season": 2022, "week": 3, "player_id": "p", "market": "receiving_yards", "yards": 900.0, "opportunities": 10, "air_yards": 1000.0},
    ])
    pregame = L.asof_rows(history, event_week=3)
    assert pregame["week"].max() == 2
    assert abs(pregame["yards"].mean() - 50.0) < 1e-12
    adot = L._adot_by_player_week(history)
    assert adot[("p", 3)] == 10.0
