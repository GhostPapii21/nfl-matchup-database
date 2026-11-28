"""Historical matchup-research fan-out. No network. projection_ready stays false."""
from __future__ import annotations

import json

import pandas as pd
import pytest

from pipeline.matchup_research.build import (
    ROOT,
    SECTION_FUNCS,
    _rate,
    build_packet,
    load_prior_plays,
)

GAME = "2026_12_DEN_PIT"
PBP = ROOT / "data/historical/nflverse/pbp_2026_w1_11_pulled_20261124T1717ET.parquet"


def test_zero_denominator_is_unknown_not_zero():
    row = _rate(0, 0, source={"module": "test"}, as_of="t", definition="empty rate")
    assert row["kind"] == "unavailable"
    assert row["value"] == "unknown"
    assert row["unavailable"] is True
    assert row["denominator"] == 0


def test_prior_plays_exclude_the_target_game_and_later_weeks(tmp_path):
    path = tmp_path / "pbp.parquet"
    pd.DataFrame([
        {"game_id": "2026_11_LV_DEN", "season": 2026, "season_type": "REG", "week": 11, "game_date": "2026-11-22", "posteam": "LV", "defteam": "DEN"},
        {"game_id": GAME, "season": 2026, "season_type": "REG", "week": 12, "game_date": "2026-11-27", "posteam": "DEN", "defteam": "PIT"},
        {"game_id": "2026_13_PIT_BAL", "season": 2026, "season_type": "REG", "week": 13, "game_date": "2026-12-06", "posteam": "PIT", "defteam": "BAL"},
    ]).to_parquet(path)
    game = {"game_id": GAME, "season": 2026, "week": 12, "gameday": "2026-11-27"}
    plays, scan = load_prior_plays(path, game)
    assert set(plays["game_id"]) == {"2026_11_LV_DEN"}
    assert scan["max_week"] == 11


def test_one_section_failure_does_not_drop_the_others(monkeypatch):
    def boom(ctx):
        raise RuntimeError("coverage down")

    monkeypatch.setitem(SECTION_FUNCS, "coverage", boom)
    packet = build_packet(GAME)
    by_name = {r["section"]: r for r in packet["receipts"]}
    assert by_name["coverage"]["status"] == "FAILED"
    assert "coverage down" in by_name["coverage"]["error"]
    assert by_name["situational"]["status"] == "EXECUTED"
    assert packet["projection_ready"] is False
    third = packet["sections"]["situational"]["teams"]["PIT"]["defense"]["third_down_conversion_rate"]
    assert third["kind"] == "measured"
    assert third["denominator"] > 0


@pytest.mark.skipif(not PBP.exists(), reason="week 1-11 play-by-play pull is not in this checkout")
def test_den_pit_week12_replay_uses_prior_weeks_only():
    packet = build_packet(GAME)
    assert packet["schema"] == "matchup-research/1"
    assert packet["projection_ready"] is False
    assert packet["research_only"] is True
    assert packet["game"]["schedule_score_status"] == "absent"
    assert packet["as_of"]["max_play_week"] == 11
    assert packet["as_of"]["week_exclusive"] == 12
    blob = json.dumps(packet["sections"])
    assert GAME not in blob

    threads = {r["thread"] for r in packet["receipts"]}
    assert len(threads) > 1
    assert all(r["status"] == "EXECUTED" for r in packet["receipts"])

    from pregame.coverage_rates import load
    sharp = load(2026)
    for team in ("DEN", "PIT"):
        man = packet["sections"]["coverage"]["teams"][team]["sharp_canonical"]["man_pct"]
        assert man["kind"] == "measured"
        assert man["value"] == sharp[team]["man_pct"]
        mofo = packet["sections"]["coverage"]["teams"][team]["sharp_canonical"]["mofo_pct"]
        mofc = packet["sections"]["coverage"]["teams"][team]["sharp_canonical"]["mofc_pct"]
        assert mofo["kind"] == "measured" and mofc["kind"] == "measured"
        sharp_blitz = packet["sections"]["coverage"]["teams"][team]["sharp_tendencies_pull"]["blitz_pct"]["value"]
        sr_blitz = packet["sections"]["coverage"]["teams"][team]["statrankings"]["blitz_pct"]["value"]
        assert sharp_blitz != sr_blitz
        scan = packet["sections"]["situational"]["teams"][team]["scan"]
        assert GAME not in scan["game_ids"]
        assert all(not gid.startswith("2026_12_") for gid in scan["game_ids"])
        third = packet["sections"]["situational"]["teams"][team]["defense"]["third_down_conversion_rate"]
        assert third["kind"] == "measured"
        assert third["denominator"] > 0
        assert third["value"] == round(third["numerator"] / third["denominator"], 6)
        early = packet["sections"]["situational"]["teams"][team]["offense"]["early_down_pass_rate"]
        assert early["kind"] == "measured" and early["denominator"] > 0
        rz = packet["sections"]["situational"]["teams"][team]["defense"]["red_zone_drive_touchdown_rate"]
        assert rz["kind"] == "measured" and rz["denominator"] > 0
        pace = packet["sections"]["situational"]["teams"][team]["pace_plays_per_game"]
        assert pace["kind"] == "measured" and pace["unit"] == "plays_per_game"
        hit = packet["sections"]["pressure"]["teams"][team]["defense"]["qb_hit_rate"]
        assert hit["kind"] == "measured" and hit["denominator"] > 0
        sack_p = packet["sections"]["pressure"]["teams"][team]["defense"]["sack_rate"]
        sack_s = packet["sections"]["situational"]["teams"][team]["defense"]["sack_rate"]
        assert sack_p["numerator"] == sack_s["numerator"]
        assert sack_p["denominator"] == sack_s["denominator"]
        rush = packet["sections"]["pressure"]["teams"][team]["defense"]["rush_four_vs_blitz"]
        assert rush["kind"] == "measured"
        assert rush["missing_rows"] >= 0
        assert rush["downgrades_only_this_output"] is True
        assert packet["sections"]["pressure"]["teams"][team]["defense"]["ftn_pressure_rate"]["kind"] == "unavailable"
        assert packet["sections"]["pressure"]["optional_gap_blocks_game"] is False
        assert packet["sections"]["pressure"]["teams"][team]["defense"]["quick_pressure"]["kind"] == "unavailable"
        assert packet["sections"]["assignments"]["teams"][team]["slot_vs_outside_alignment"]["kind"] == "unavailable"
        events = packet["sections"]["assignments"]["teams"][team]["verified_pbp_events"]
        assert events["kind"] == "measured" and events["sample_size"] > 0
        assert events["not_a_coverage_assignment"] is True

    assert packet["sections"]["assignments"]["matchup_sources"]["likely_defenders"]["status"] == "MISSING"
    assert packet["sections"]["assignments"]["matchup_sources"]["target_location"]["status"] == "FILLED"
    assert packet["sections"]["coverage"]["blended_rate"]["kind"] == "unavailable"
    assert packet["sections"]["coverage"]["sources_not_blended"] is True
    assert packet["sections"]["trenches"]["teams"]["PIT"]["box_structure"]["kind"] == "unavailable"
    assert packet["sections"]["trenches"]["teams"]["PIT"]["opponent_adjusted_allowances"]["kind"] == "unavailable"
    assert "144" in packet["sections"]["trenches"]["teams"]["PIT"]["opponent_adjusted_allowances"]["reason"]
    assert packet["sections"]["open_prs"]["pr_140_defense_allowed"]["kind"] == "unavailable"
    assert packet["sections"]["open_prs"]["pr_143_defender_profiles"]["kind"] == "unavailable"
    assert packet["sections"]["open_prs"]["pr_144_positional_allowances"]["kind"] == "unavailable"
    assert packet["sections"]["context"]["weather"]["pregame_forecast"]["kind"] == "unavailable"
    assert packet["sections"]["context"]["weather"]["roof"]["value"] == "outdoors"
    assert packet["sections"]["context"]["teams"]["DEN"]["rest_days"]["value"] == 5
    assert packet["sections"]["context"]["teams"]["PIT"]["rest_days"]["value"] == 5
    assert packet["sections"]["context"]["teams"]["DEN"]["travel_miles_from_previous_site"]["kind"] == "estimate"
    assert packet["sections"]["context"]["teams"]["DEN"]["coach"]["value"] == "Sean Payton"
    assert packet["sections"]["context"]["teams"]["PIT"]["coach"]["value"] == "Mike McCarthy"
    assert packet["sections"]["context"]["teams"]["DEN"]["previous_site"]["game_id"] == "2026_11_LV_DEN"

    def no_ready(obj):
        if isinstance(obj, dict):
            assert obj.get("projection_ready") is not True
            for value in obj.values():
                no_ready(value)
        elif isinstance(obj, list):
            for value in obj:
                no_ready(value)

    no_ready(packet)
