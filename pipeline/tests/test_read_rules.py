"""Read rules (Rico, Nov 26 2026): flags only, unknown never zero, walk-forward, hourly weather grading. Offline."""
from datetime import datetime, timezone

import pandas as pd
import pytest

import pipeline.read_rules as RR
from pipeline.read_rules import UNKNOWN
from pipeline.read_rules import defense_allowed as DA
from pipeline.read_rules import flags as FL
from pipeline.read_rules import targets_first as TF
from pipeline.read_rules import weather_grade as WG
from pipeline.read_rules.common import field, is_unknown


def _play(week, game, pos, deff, rec=None, rusher=None, comp=1, yds=10, air=5, loc="left", **kw):
    d = dict(week=week, game_id=game, posteam=pos, defteam=deff, season_type="REG", two_point_attempt=0,
             pass_attempt=int(rec is not None), rush_attempt=int(rusher is not None), receiver_player_id=rec,
             receiver_player_name=rec, rusher_player_id=rusher, complete_pass=comp if rec else 0,
             receiving_yards=yds if (rec and comp) else None, rushing_yards=yds if rusher else None,
             yards_gained=yds, air_yards=air if rec else None, pass_location=loc if rec else None, sack=0,
             qb_scramble=0, qb_kneel=0, pass_defense_1_player_id=None, pass_defense_1_player_name=None,
             pass_defense_2_player_id=None, pass_defense_2_player_name=None, interception_player_id=None,
             interception_player_name=None, penalty_type=None, penalty_player_id=None, penalty_player_name=None,
             solo_tackle_1_player_id=None, solo_tackle_1_player_name=None, assist_tackle_1_player_id=None,
             assist_tackle_1_player_name=None)
    d.update(kw)
    return d


def _team_games(team="AAA", opp="BBB", weeks=(1, 2, 3, 4), shares=None):
    """Each week: `team` throws 10 targets split per `shares` {gsis: n}."""
    shares = shares or {"wr1": 3, "wr2": 1, "te1": 2, "te2": 1, "te3": 1, "rb1": 2}
    rows = []
    for w in weeks:
        g = f"2026_{w:02d}_{team}_{opp}"
        for pid, n in shares.items():
            rows += [_play(w, g, team, opp, rec=pid) for _ in range(n)]
        rows.append(_play(w, g, team, opp, rusher="rb1", yds=4))
        rows.append(_play(w, g, opp, team, rusher="orb", yds=6))
    return pd.DataFrame(rows)


POS = {"wr1": "WR", "wr2": "WR", "te1": "TE", "te2": "TE", "te3": "TE", "rb1": "RB", "orb": "RB", "cb1": "CB"}


# ------------------------------------------------------------------ flags-only guarantees
def test_cuts_disabled_for_every_rule():
    assert set(RR.CUTS_ENABLED) == {"targets_first", "defense_allowed", "weather_grade"}
    assert not any(RR.CUTS_ENABLED.values())
    assert RR.PROJECTION_READY is False
    RR.assert_flags_only()


def test_assert_flags_only_trips_if_a_rule_is_switched_on(monkeypatch):
    monkeypatch.setitem(RR.CUTS_ENABLED, "targets_first", True)
    with pytest.raises(RuntimeError):
        RR.assert_flags_only()


def test_annotate_legs_only_adds_columns():
    pbp = _team_games()
    legs = pd.DataFrame(dict(week=[5, 5, 5], game_id=["2026_05_AAA_BBB"] * 3, gsis=["wr1", "wr2", "rb1"],
                             position=["WR", "WR", "RB"], market=["recyds", "rec", "rushyds"], label=["X", "Y", "Z"],
                             line=[50.5, 3.5, 40.5]))
    out = FL.annotate_legs(legs, pbp, POS)
    assert len(out) == len(legs)
    pd.testing.assert_frame_equal(out[legs.columns], legs)
    assert set(FL.FLAG_COLUMNS) <= set(out.columns)
    assert list(out.rr_targets_first) == [TF.PASS, TF.FLAG_LOW, TF.NA]


def test_annotate_legs_refuses_to_overwrite():
    legs = pd.DataFrame(dict(week=[5], game_id=["2026_05_AAA_BBB"], gsis=["wr1"], position=["WR"], market=["rec"],
                             rr_weather=["x"]))
    with pytest.raises(ValueError):
        FL.annotate_legs(legs, _team_games(), POS)


# ------------------------------------------------------------------ rule 1
def _tf(gsis, pos, shares, week=5, roles=None, opp="BBB"):
    pbp = _team_games(shares=shares)
    players, tt = TF.target_table(pbp)
    return TF.evaluate(gsis, week, pos, opp, players, tt, roles)


def test_wr_share_boundary():
    # 1000 team targets/week is overkill; use 199/1000 vs 200/1000 via counts per week
    lo = _tf("wr1", "WR", {"wr1": 199, "x": 801})
    hi = _tf("wr1", "WR", {"wr1": 200, "x": 800})
    assert lo["share"] == pytest.approx(0.199) and lo["status"] == TF.FLAG_LOW
    assert hi["share"] == pytest.approx(0.20) and hi["status"] == TF.PASS


def test_te_top_two_including_ties():
    assert _tf("te1", "TE", {"wr1": 5, "te1": 3, "x": 2})["status"] == TF.PASS          # rank 2
    assert _tf("te1", "TE", {"wr1": 5, "te1": 3, "x": 3})["status"] == TF.PASS          # tied at 2
    assert _tf("te1", "TE", {"wr1": 5, "x": 4, "te1": 3})["status"] == TF.FLAG_LOW      # rank 3


def test_insufficient_history_and_walk_forward():
    r = _tf("wr1", "WR", {"wr1": 5, "x": 5}, week=3)        # only weeks 1-2 are prior
    assert r["status"] == TF.INSUFF and r["n_games"] == 2
    r = _tf("wr1", "WR", {"wr1": 5, "x": 5}, week=5)
    assert max(r["window_weeks"]) < 5 and r["n_games"] == 4


def test_not_applicable_for_non_wr_te():
    assert _tf("rb1", "RB", None)["status"] == TF.NA


def test_role_exception_only_when_defense_is_soft():
    roles = pd.DataFrame(dict(defteam=["BBB"], role=["TE"], yds_pg_rank=[DA.SOFT_RANK]))
    assert _tf("te3", "TE", {"wr1": 5, "te1": 4, "te2": 4, "te3": 1}, roles=roles)["status"] == TF.PASS_EXC
    roles.loc[0, "yds_pg_rank"] = DA.SOFT_RANK + 1
    r = _tf("te3", "TE", {"wr1": 5, "te1": 4, "te2": 4, "te3": 1}, roles=roles)
    assert r["status"] == TF.FLAG_LOW and r["role_exception"] == "not_soft"


def test_unknown_role_never_passes():
    roles = pd.DataFrame(dict(defteam=["BBB"], role=["WR"], yds_pg_rank=[1]))
    r = _tf("wr2", "WR", {"wr1": 9, "wr2": 1}, roles=roles)   # WR alignment unknown -> exception unknown
    assert r["status"] == TF.FLAG_LOW and r["role_exception"] == UNKNOWN
    r = _tf("te3", "TE", {"wr1": 5, "te1": 4, "te2": 4, "te3": 1}, roles=None)
    assert r["status"] == TF.FLAG_LOW and r["role_exception"] == UNKNOWN


# ------------------------------------------------------------------ rule 2
def test_field_unknown_is_never_zero():
    assert field(None, "s", "t")["value"] == UNKNOWN
    assert field(float("nan"), "s", None) == {"value": UNKNOWN, "source": "s", "pulled_at": UNKNOWN}
    assert field(0, "s", "t")["value"] == 0          # a real zero stays zero
    assert is_unknown(pd.NA) and is_unknown("unknown") and not is_unknown(0)


def test_defense_profile_walk_forward_and_sourced(tmp_path):
    pbp = _team_games()
    late = _team_games(weeks=(6,), shares={"te1": 50})       # week 6 must not leak into as_of_week=5
    pbp = pd.concat([pbp, late], ignore_index=True)
    sharp = tmp_path / "sharp.csv"
    sharp.write_text("team,season,man_pct,zone_pct,mofc_pct,mofo_pct,source_updated,pulled_utc,source_url\n"
                     "BBB,2026,30,60,55,40,Nov 17,2026-11-24T11:26:49+00:00,u\n")
    roles = DA.role_allowed(pbp, POS, 5)
    te = roles[(roles.defteam == "BBB") & (roles.role == "TE")].iloc[0]
    assert te.targets == 16 and te.games == 4                 # 4 TE targets x 4 weeks, nothing from week 6
    prof = DA.profile("BBB", 5, pbp, "pbp", "2026-11-24T22:17:40+00:00", POS, sharp_path=sharp, pff_dir=str(tmp_path))

    def walk(x):
        if isinstance(x, dict) and "value" in x:
            assert x["source"] and x["pulled_at"]
            return
        if isinstance(x, dict):
            for v in x.values():
                walk(v)
    walk({k: v for k, v in prof.items() if k not in ("defteam", "as_of_week", "flag_only")})
    assert prof["coverage"]["mofc_pct"]["value"] == "55"
    assert prof["by_role"]["slot_WR"]["yds_pg"]["value"] == UNKNOWN
    assert prof["by_role"]["outside_WR"]["rec_pg"]["value"] == UNKNOWN
    assert prof["run_defense"]["ypc"]["value"] == pytest.approx(4.0)
    # a defense with no data: unknown, not zero
    p2 = DA.profile("ZZZ", 5, pbp, "pbp", "t", POS, sharp_path=sharp, pff_dir=str(tmp_path))
    assert p2["run_defense"]["ypc"]["value"] == UNKNOWN and p2["coverage"]["man_pct"]["value"] == UNKNOWN
    assert p2["db_allowed"]["value"] == UNKNOWN


def test_db_events_verified_vs_inferred():
    rows = [_play(1, "2026_01_AAA_BBB", "AAA", "BBB", rec="wr1", yds=20, solo_tackle_1_player_id="cb1",
                  solo_tackle_1_player_name="C.B"),
            _play(1, "2026_01_AAA_BBB", "AAA", "BBB", rec="wr1", comp=0, pass_defense_1_player_id="cb1",
                  pass_defense_1_player_name="C.B")]
    out = DA.db_events(pd.DataFrame(rows), POS, 2, "BBB")
    assert out[0]["pbu"] == 1 and out[0]["inferred_catches"] == 1 and out[0]["inferred_yards"] == 20
    assert "inferred_from_tackler" in out[0]["inferred_label"]


def test_soft_vs_role_unknowns():
    roles = pd.DataFrame(dict(defteam=["BBB"], role=["TE"], yds_pg_rank=[3]))
    assert DA.soft_vs_role(roles, "BBB", "TE") == "soft"
    assert DA.soft_vs_role(roles, "BBB", "slot_WR") == UNKNOWN
    assert DA.soft_vs_role(roles, "CCC", "TE") == UNKNOWN
    assert DA.soft_vs_role(roles, "BBB", None) == UNKNOWN


def test_parse_pff_coverage_card():
    txt = "\nZW\nZakee Wheatley\nPanthers\nCOVERAGE\nINTERCEPTIONS\n1\nPASS BREAKUPS\n0\nTARGETS\n3/4\nBO\n"
    assert DA.parse_pff_coverage_cards(txt) == [dict(name="Zakee Wheatley", team="CAR", int=1, pbu=0, rec_allowed=3, targets=4)]


# ------------------------------------------------------------------ rule 3
@pytest.mark.parametrize("rate,grade", [(0, "none"), (0.0001, "light"), (0.049, "light"), (0.05, "moderate"),
                                        (0.3, "moderate"), (0.301, "heavy"), (None, UNKNOWN), (-1, UNKNOWN)])
def test_rain_grade_boundaries(rate, grade):
    assert WG.grade_rain(rate) == grade


KO = datetime(2026, 12, 6, 18, 0, tzinfo=timezone.utc)


def _fake_fetch(url):
    if "open-meteo" in url:
        times = [f"2026-12-06T{h:02d}:00" for h in range(15, 24)]
        return {"hourly": {"time": times, "precipitation": [0, 0, 0, 0.0, 0.02, 0.06, 0.4, 0, 0],
                           "wind_speed_10m": [5] * 9, "wind_gusts_10m": [9, 9, 9, 10, 12, 30, 31, 9, 9]}}
    if "/points/" in url:
        return {"properties": {"forecastGridData": "https://api.weather.gov/gridpoints/X/1,1"}}
    return {"properties": {
        "quantitativePrecipitation": {"values": [{"validTime": "2026-12-06T18:00:00+00:00/PT6H", "value": 6.096}]},
        "windSpeed": {"values": [{"validTime": "2026-12-06T18:00:00+00:00/PT1H", "value": 16.0934},
                                 {"validTime": "2026-12-06T19:00:00+00:00/PT3H", "value": 32.1869}]},
        "windGust": {"values": [{"validTime": "2026-12-06T18:00:00+00:00/PT4H", "value": 40.2336}]}}}


def test_hourly_grade_per_source_and_hour():
    g = WG.grade_window(KO, 41.86, -87.61, "outdoors", fetch=_fake_fetch)
    assert g["graded"] and len(g["hours"]) == 4
    om = [h["open_meteo"]["rain_grade"] for h in g["hours"]]
    assert om == ["none", "light", "moderate", "heavy"]
    assert g["hours"][0]["nws"]["wind_mph"] == pytest.approx(10.0, abs=0.1)
    assert g["hours"][1]["nws"]["wind_mph"] == pytest.approx(20.0, abs=0.1)
    assert g["hours"][2]["open_meteo"]["gust_mph"] == 30
    assert g["hours"][0]["nws"]["pulled_at"] != UNKNOWN
    tilt = WG.run_tilt(g, "CHI", 0.5, 0.43)
    assert "run-tilt UP" in tilt and "Flag only" in tilt


def test_nws_qpf_spread_over_period():
    g = WG.grade_window(KO, 41.86, -87.61, "outdoors", fetch=_fake_fetch)
    # 6.096 mm over 6 h = 0.24 in / 6 h = 0.04 in/hr -> light
    assert g["hours"][0]["nws"]["rain_in_hr"] == pytest.approx(0.04, abs=1e-3)
    assert g["hours"][0]["nws"]["rain_grade"] == "light"


def test_indoor_not_graded():
    g = WG.grade_window(KO, 1, 1, "dome", fetch=_fake_fetch)
    assert not g["graded"] and g["status"] == "indoor, not graded"
    assert "no weather run-tilt" in WG.run_tilt(g, "DET")


def test_network_failure_is_unknown_not_calm():
    def boom(url):
        raise OSError("down")
    g = WG.grade_window(KO, 41.86, -87.61, "outdoors", fetch=boom)
    for h in g["hours"]:
        for k in ("nws", "open_meteo"):
            assert h[k]["rain_grade"] == UNKNOWN and h[k]["wind_mph"] == UNKNOWN and h[k]["gust_mph"] == UNKNOWN
    assert WG.worst(g["hours"])["rain"] == UNKNOWN
    assert "unknown" in WG.run_tilt(g, "CHI")


def test_sources_disagreement_flagged():
    g = WG.grade_window(KO, 41.86, -87.61, "outdoors", fetch=_fake_fetch)
    assert g["hours"][0]["sources_disagree"] is True     # NWS light vs Open-Meteo none
