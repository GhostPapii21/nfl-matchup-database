import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fair_price as F  # noqa: E402


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
