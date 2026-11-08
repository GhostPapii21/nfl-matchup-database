import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validation.weather_hook import nws_hourly_scenario

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "scenarios/nws_LWX_109_90_hourly_pulled_2026-11-05T1822EST.json"


def test_nws_hourly_is_metadata_only_no_modifier():
    sc = nws_hourly_scenario(json.loads(RAW.read_text()), kickoff_et="2026-11-05T20:15:00-05:00", hours=4)
    assert sc["status"] == "PROVIDED_METADATA_ONLY"
    assert sc["source"].startswith("NWS api.weather.gov gridpoints/LWX/109,90")
    assert sc["quantitative_modifier"] is None and sc["auto_apply_to_props"] is False
    assert len(sc["hours"]) == 4 and sc["hours"][0]["start"].startswith("2026-11-05T20:00")
    assert sc["max_pop_pct"] >= 0
