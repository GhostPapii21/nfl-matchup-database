"""NFL-75 (outside-AI review memo B4): the QB starter / availability gate runs on EVERY leg, before a preset p_model is
kept, and position / depth-chart / injury-status matches are case-insensitive. Synthetic data only; no network.
Research only; projection_ready stays false."""
from __future__ import annotations

import numpy as np
import pandas as pd

from calibration import simv56_pmodel as SV
from calibration.tests import test_simv56_pmodel as T

AS_OF = "2026-11-15T12:00:00Z"
ENS = pd.DataFrame([dict(gsis="00-M", market="rushyds", line=20.5, p_over=0.4, p_under=0.6)])


def _gate(legs, hist=None, depth=None, inj=None):
    st = SV.qb_starters(T.DEPTH if depth is None else depth, T.INJ if inj is None else inj, week=10, as_of=AS_OF,
                        source=T.SRC_META)
    return SV.gate_legs(legs, st, T.INJ if inj is None else inj, week=10,
                        starter_history=hist or {"00-M": 6, "00-W": 4, "00-A": 8, "00-C": 0})


def test_preset_p_model_on_a_blocked_leg_is_blanked():
    """Wentz (not the starter) and Cousins (Out) arrive already priced: the gate still blocks them."""
    legs = T._legs().iloc[[0, 1, 2, 3]].assign(team=["MIN", "MIN", "MIN", "BUF"], p_model=[0.9, 0.11, 0.8, 0.7])
    out = SV.attach(legs, ENS, _gate(legs))
    assert list(out.gate) == ["qb_not_starter", "ok", "out_or_doubtful", "out_or_doubtful"]
    assert pd.isna(out.p_model.iloc[0]) and pd.isna(out.p_model.iloc[2]) and pd.isna(out.p_model.iloc[3])
    assert out.p_model.iloc[1] == 0.11 and out.p_model_match.iloc[1] == "preset"     # gate ok: preset kept
    assert list(out.p_model_match[[0, 2, 3]]) == ["gated:qb_not_starter", "gated:out_or_doubtful",
                                                 "gated:out_or_doubtful"]


def test_gate_applies_to_non_rush_markets_too():
    legs = T._legs().iloc[[0, 1]].assign(team="MIN", market="recyds", p_model=[0.7, 0.6])
    out = SV.attach(legs, ENS, _gate(legs))
    assert pd.isna(out.p_model.iloc[0]) and out.p_model_match.iloc[0] == "gated:qb_not_starter"
    assert out.p_model.iloc[1] == 0.6 and pd.isna(out.p_model_match.iloc[1])


def test_blocked_preset_leg_is_insufficient_in_the_frozen_classifier():
    from calibration.selective_edge_live import grade_live
    legs = T._legs().iloc[[0, 1]].assign(team="MIN", p_model=[0.9, np.nan])
    out = SV.attach(legs, ENS, _gate(legs))
    ctx = pd.DataFrame({"carry_n_prior": [4.0, 4.0], "carry_n60": [0.0, 0.0], "carry_share": [0.1, 0.1],
                        "usual": [20.0, 20.0]})
    g = grade_live(out.reset_index(drop=True), pd.DataFrame(), context=ctx)
    assert g.label.iloc[0] == "INSUFFICIENT EVIDENCE" and g.reason.iloc[0] == "model_prob_missing"
    assert (g.projection_ready == False).all()  # noqa: E712


def test_lowercase_or_padded_qb_position_does_not_skip_the_gate():
    legs = T._legs().iloc[[0, 0, 0, 1]].assign(team="MIN", position=["qb", " Qb ", "QB", "qb"])
    g = _gate(legs)
    assert list(g.gate) == ["qb_not_starter"] * 3 + ["ok"]


def test_depth_chart_and_injury_status_are_case_insensitive():
    depth = T.DEPTH.assign(pos_abb=T.DEPTH.pos_abb.str.lower())
    inj = T.INJ.assign(report_status=T.INJ.report_status.str.upper())        # "OUT" / "DOUBTFUL"
    st = SV.qb_starters(depth, inj, week=10, as_of=AS_OF, source=T.SRC_META).set_index("team")
    assert st.loc["MIN", "starter_gsis"] == "00-M"                            # Cousins OUT still skipped
    legs = T._legs().iloc[[2, 3]].assign(team=["MIN", "BUF"], p_model=[0.8, 0.7])
    g = SV.gate_legs(legs, st.reset_index(), inj, week=10, starter_history={"00-M": 6})
    assert list(g.gate) == ["out_or_doubtful", "out_or_doubtful"]
