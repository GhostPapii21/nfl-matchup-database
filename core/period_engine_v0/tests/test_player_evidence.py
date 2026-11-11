import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pytest
from player_evidence import DEFAULT_OUTLIER_CSV, bundle_from_outlier, load_outlier_csv


@pytest.mark.skipif(not DEFAULT_OUTLIER_CSV.exists(), reason="optional_inputs/outlier_props.csv is a local-only input and is not published")
def test_outlier_csv_loads_and_flags_gaps():
    rows = load_outlier_csv()
    assert len(rows) > 0
    b = bundle_from_outlier("Jakobi Meyers", market="Receptions", line=3.5, side="Over", pulled_et="2026-11-05")
    d = b.to_dict()
    assert d["outlier_row"] is not None
    assert "LOCATION_OVERLAY_MISSING" in d["flags"]
    assert "VERIFIED_DEFENDER_MISSING" in d["flags"]
    assert "GREEN_CHART_NOT_AUTOMATIC_EDGE" in d["flags"]
    assert d["location_overlay"]["status"] == "MISSING"
    assert d["h2h"]["status"] in {"MISSING", "PRESENT_UNPARSED"}


def test_missing_player_flags():
    b = bundle_from_outlier("Nobody Fake", market="Receptions", line=1.5, side="Over")
    assert "OUTLIER_ROW_MISSING" in b.flags
