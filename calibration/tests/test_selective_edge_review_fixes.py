"""Ghost6's PR #40 review (APPROVE WITH CHANGES), required fixes 1-4, written before the fixes.
1. A rushing leg with an unknown / blank / non-canonical position, or no player id, must be INSUFFICIENT EVIDENCE
   (the RB 60%-carry gate must never be skipped because position is missing). Live grading fails loudly when the
   legs have no position/gsis columns.
2. N1 boundary: a back at 59% of team carries in his last 4 games is do-not-play; at 60% he passes.
3. freeze_v2 adapter: a best price quoted at a line different from the consensus line is dropped (no dec, no source).
4. selective_edge_freeze.py hashes itself (it is in CODE_FILES).
Synthetic data only. Research only; projection_ready stays false."""
from __future__ import annotations
import json
import shutil

import numpy as np
import pandas as pd
import pytest

from calibration import selective_edge as se
from calibration import selective_edge_freeze as FZ
from calibration import selective_edge_live as LV

PARAMS = {"strong_markets": ["rushyds", "rushrec"], "alt_min_cushion": 0.20, "train_weeks": [4, 5, 6, 7]}


def leg(**kw):
    d = dict(week=8, game_id="2026_08_AAA_BBB", gsis="00-1", player="P", position="RB", market="rushyds",
             side="Under", kind="main", line=60.5, dec=1.91, p_nv=0.50, p_model=0.55, defender_verified=False,
             carry_n_prior=np.nan, carry_n60=np.nan, usual=np.nan, price_source="book:test", actual=np.nan,
             source="live")
    d.update(kw)
    return d


def lab(rows, params=PARAMS):
    return se.classify(pd.DataFrame(rows), params)


# ---------- fix 1: unknown position never bypasses the N1 gate ----------
@pytest.mark.parametrize("pos", [np.nan, None, "", "  ", "nan", "None", "XYZ", "OL", "K"])
@pytest.mark.parametrize("market", ["rushyds", "rushrec"])
def test_rush_leg_with_unknown_position_is_insufficient(pos, market):
    out = lab([leg(position=pos, market=market, defender_verified=True)])
    assert out.label.iloc[0] == se.INSUFFICIENT, (pos, market, out.label.iloc[0])
    assert out.reason.iloc[0] == "position_unknown"


def test_rush_leg_without_player_id_is_insufficient():
    for g in (np.nan, None, ""):
        out = lab([leg(position="QB", gsis=g)])
        assert out.label.iloc[0] == se.INSUFFICIENT and out.reason.iloc[0] == "player_id_unknown"


def test_lower_case_rb_is_still_carry_gated():
    out = lab([leg(position="rb"), leg(position=" Rb ", carry_n_prior=4, carry_n60=1),
               leg(position="rb", carry_n_prior=4, carry_n60=4)])
    assert out.label.tolist() == [se.INSUFFICIENT, se.NO_EDGE, se.STRONG_UNDER]
    assert out.reason.tolist()[:2] == ["carry_history_unknown", "do_not_play_rb_carry_lt_60"]


def test_reviewer_repro_no_carry_history_never_strong_under():
    # Ghost6's position_gap repro: position NaN / None / "rb", rushyds Under, no carry history -> was STRONG UNDER
    out = lab([leg(position=np.nan), leg(position=None), leg(position="rb")])
    assert (out.label == se.INSUFFICIENT).all()


def test_qb_and_wr_rush_legs_unchanged_by_position_rule():
    out = lab([leg(position="QB"), leg(position="qb"), leg(position="WR")])
    assert (out.label == se.STRONG_UNDER).all()


def test_receiving_leg_with_unknown_position_still_needs_defender_only():
    out = lab([leg(market="recyds", position=np.nan, defender_verified=False)])
    assert out.reason.iloc[0] == "main_defender_unverified"


def test_live_grader_fails_loudly_without_position_or_gsis_columns():
    base = leg(week=10, actual=40.0)
    for drop in ("position", "gsis"):
        d = {k: v for k, v in base.items() if k != drop}
        with pytest.raises(LV.LiveGradeError, match=drop):
            LV.grade_live(pd.DataFrame([d]), pbp=pd.DataFrame())


# ---------- fix 2: N1 boundary through the real point-in-time context ----------
def _pbp_share(rb_carries: int, team_carries: int = 100, weeks=range(1, 5)):
    rows = []
    for w in weeks:
        for i in range(team_carries):
            rows.append(dict(week=w, game_id=f"g{w}", posteam="T", rush_attempt=1, qb_kneel=0, pass_attempt=0,
                             rusher_player_id=("A" if i < rb_carries else "B"), receiver_player_id=None,
                             rushing_yards=1.0, receiving_yards=np.nan, complete_pass=0, two_point_attempt=0,
                             season_type="REG"))
    return pd.DataFrame(rows)


@pytest.mark.parametrize("carries,label,reason", [(59, se.NO_EDGE, "do_not_play_rb_carry_lt_60"),
                                                  (60, se.STRONG_UNDER, "gated_under_strong_market")])
def test_n1_boundary_59_is_do_not_play_60_passes(carries, label, reason):
    legs = se.attach_context(pd.DataFrame([leg(gsis="A", week=5)]), _pbp_share(carries))
    assert legs.carry_n_prior.iloc[0] == 4
    assert legs.carry_share.iloc[0] == pytest.approx(carries / 100)
    out = se.classify(legs, PARAMS)
    assert out.label.iloc[0] == label
    if label == se.NO_EDGE:
        assert out.reason.iloc[0] == reason


def test_n1_needs_three_of_last_four_at_60():
    # 60% in exactly 3 of 4 passes; in 2 of 4 fails
    def pbp(shares):
        return pd.concat([_pbp_share(s, weeks=[w]) for w, s in zip(range(1, 5), shares)], ignore_index=True)
    a = se.classify(se.attach_context(pd.DataFrame([leg(gsis="A", week=5)]), pbp([60, 60, 60, 59])), PARAMS)
    b = se.classify(se.attach_context(pd.DataFrame([leg(gsis="A", week=5)]), pbp([60, 60, 59, 59])), PARAMS)
    assert a.label.iloc[0] == se.STRONG_UNDER and b.label.iloc[0] == se.NO_EDGE


def test_carry_share_threshold_constant_is_sixty():
    assert se.CARRY_SHARE_MIN == pytest.approx(0.60)


# ---------- fix 3: freeze_v2 price at a different line than consensus is dropped ----------
def _freeze(tmp_path, over_line=29.5, under_line=29.5, cons_line=29.5):
    d = {"meta": {"game_id": "2026_10_WAS_NYG", "pulled_utc": "2026-11-13T00:01:35Z",
                  "commence_utc": "2026-11-13T01:15:00Z"},
         "markets": {"rushing_yards|Austin Ekeler": {"best_retail_price": {
             "Over": {"book": "fanduel", "line": over_line, "price": -113},
             "Under": {"book": "draftkings", "line": under_line, "price": -108}}}},
         "consensus": {"rushing_yards|Austin Ekeler": {"consensus": {"line": cons_line,
                                                                     "no_vig": {"Over": 0.5028, "Under": 0.4972}}}}}
    p = tmp_path / "freeze_v2_test.json"
    p.write_text(json.dumps(d))
    return p


def test_freeze_v2_drops_price_quoted_off_consensus_line(tmp_path):
    df = LV.legs_from_freeze_v2(str(_freeze(tmp_path, under_line=30.5))).set_index("side")
    assert np.isnan(df.loc["Under", "dec"]) and pd.isna(df.loc["Under", "price_source"])
    assert np.isnan(df.loc["Under", "p_nv"])
    assert df.loc["Over", "dec"] == pytest.approx(1 + 100 / 113) and df.loc["Over", "line"] == 29.5
    assert "draftkings" not in str(df.loc["Over", "price_source"])


def test_freeze_v2_off_line_leg_classifies_insufficient(tmp_path):
    df = LV.legs_from_freeze_v2(str(_freeze(tmp_path, under_line=28.5))).assign(
        p_model=0.6, position="QB", gsis="00-9")
    out = se.classify(df, PARAMS).set_index("side")
    assert out.loc["Under", "label"] == se.INSUFFICIENT and out.loc["Under", "reason"] == "price_missing"


def test_freeze_v2_line_match_is_numeric(tmp_path):
    df = LV.legs_from_freeze_v2(str(_freeze(tmp_path, under_line="29.5"))).set_index("side")
    assert df.loc["Under", "dec"] == pytest.approx(1 + 100 / 108)


# ---------- fix 4: the freeze checker hashes itself ----------
def test_freeze_checker_is_in_code_files():
    assert "calibration/selective_edge_freeze.py" in FZ.CODE_FILES
    m = json.loads(FZ.MANIFEST.read_text())
    assert "calibration/selective_edge_freeze.py" in m["code_sha256"]


def test_editing_freeze_checker_trips_the_freeze(tmp_path):
    for f in FZ.CODE_FILES + (FZ.PARAMS_FILE,):
        d = tmp_path / f
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(FZ.ROOT / f, d)
    mp = tmp_path / FZ.MANIFEST.relative_to(FZ.ROOT)
    mp.parent.mkdir(parents=True, exist_ok=True)
    mp.write_text(FZ.MANIFEST.read_text())
    FZ.check_freeze(10, root=tmp_path)
    f = tmp_path / "calibration/selective_edge_freeze.py"
    f.write_text(f.read_text() + "\n# tweak\n")
    with pytest.raises(FZ.FreezeError, match="differ"):
        FZ.check_freeze(10, root=tmp_path)
