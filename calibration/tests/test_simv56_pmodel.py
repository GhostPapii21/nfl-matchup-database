"""NFL-75: Week 10 rush-under p_model from the SAME sim_v5 / sim_v6 / sim_v6_fix ensemble (opp 0.5, n=20,000) that
produced the Phase 4 fit's p_model, plus a QB starter gate. Written BEFORE calibration/simv56_pmodel.py (tests first).
Research only; projection_ready stays false."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from calibration import simv56_pmodel as SV  # noqa: E402

# Phase 4 input for this leg: candidates.csv (sha256 5aa84712...6f23 in the Phase 4 freeze manifest), kind=under,
# week 8, Jacoby Brissett (00-0033119) rushyds 9.5. The file stores p_model as the text 0.42037777777777774 (exact repr);
# selective_edge_run.build reads it with pandas' default C float parser, which yields 0.4203777777777777 in memory
# (one ulp lower). The Sunday path goes through the same CSV read in selective_edge_live, so both are checked. The per-engine
# (p_mc, p_bias, p_gr) triples are the saved confidence_check_2026-11-03 sims/<engine>_opp0.5_w8.csv rows.
W8_LEG = dict(player="Jacoby Brissett", gsis="00-0033119", team="ARI", opp="DAL", market="rushyds",
              spread=7.0, line=9.5)
W8_TRIPLES = {"sim_v5": (0.5985, 0.566, 0.56415), "sim_v6": (0.5985, 0.60605, 0.56415),
              "sim_v6_fix": (0.5985, 0.5566, 0.56415)}
W8_P_MODEL_UNDER = 0.42037777777777774            # candidates.csv text, exact
W8_P_MODEL_PHASE4_IN_MEMORY = 0.4203777777777777  # after pd.read_csv (default parser), as Phase 4 used it


def test_settings_are_the_phase4_ones():
    assert SV.ENGINES == ("sim_v5", "sim_v6", "sim_v6_fix")
    assert SV.OPP == "0.5" and SV.N_TRIALS == 20000
    assert SV.ENS == ["sim_v5|0.5", "sim_v6|0.5", "sim_v6_fix|0.5"]
    assert SV.CALIB_WEEKS_RULE == "backtest weeks < min(W, 8)"


def test_vendored_engines_are_byte_identical_to_pinned_sums(tmp_path):
    SV.verify_engines()                                  # raises on any mismatch
    bad = tmp_path / "engines"
    bad.mkdir()
    for f in SV.ENGINE_DIR.iterdir():
        (bad / f.name).write_bytes(f.read_bytes())
    (bad / "cc_sim_v5.py").write_text((bad / "cc_sim_v5.py").read_text() + "\n# edit\n")
    with pytest.raises(SV.SimV56Error, match="cc_sim_v5.py"):
        SV.verify_engines(bad)


@pytest.mark.parametrize("week,cut", [(8, "2026-10-29"), (9, "2026-11-02"), (10, "2026-11-12")])
def test_cutoff_rule_matches_run_sims(week, cut):
    assert SV.cutoff_for_week(week) == cut


def test_ensemble_arithmetic_reproduces_phase4_p_model_bit_for_bit():
    per = {e: pd.DataFrame([dict(gsis=W8_LEG["gsis"], market="rushyds", line=9.5, p_mc=t[0], p_bias=t[1], p_gr=t[2])])
           for e, t in W8_TRIPLES.items()}
    ens = SV.ensemble(per)
    assert ens.p_under.iloc[0] == W8_P_MODEL_UNDER       # exact float equality, not approx
    assert ens.p_over.iloc[0] == 1 - W8_P_MODEL_UNDER
    import io
    buf = io.StringIO()
    ens[["p_under"]].to_csv(buf, index=False)
    assert pd.read_csv(io.StringIO(buf.getvalue())).p_under.iloc[0] == W8_P_MODEL_PHASE4_IN_MEMORY


def test_reproduce_w8_leg_from_committed_inputs_bit_for_bit(tmp_path):
    """Runs the three vendored engines on the committed W1-9 PBP (cut at the W8 rule) + committed players table."""
    src = SV.make_src(tmp_path / "src")
    legs = pd.DataFrame([W8_LEG])
    per = SV.run_all(legs, week=8, src=src, workdir=tmp_path)
    for e, t in W8_TRIPLES.items():
        r = per[e].iloc[0]
        assert (r.p_mc, r.p_bias, r.p_gr) == t, e
    assert SV.ensemble(per).p_under.iloc[0] == W8_P_MODEL_UNDER


# ------------------------------------------------------------------ QB / availability gate
def _depth(rows, dt="2026-11-15T11:00:00Z"):
    return pd.DataFrame([dict(dt=dt, team=t, player_name=n, gsis_id=g, pos_abb="QB", pos_rank=r)
                         for t, n, g, r in rows])


DEPTH = pd.concat([
    _depth([("MIN", "Kirk Cousins", "00-C", 1), ("MIN", "Kyler Murray", "00-M", 2), ("MIN", "Carson Wentz", "00-W", 3),
            ("BUF", "Josh Allen", "00-A", 1), ("BUF", "Kyle Allen", "00-K", 2)]),
    _depth([("MIN", "Carson Wentz", "00-W", 1)], dt="2026-11-15T20:00:00Z"),   # a snapshot AFTER as_of: never used
], ignore_index=True)
INJ = pd.DataFrame([dict(week=10, team="MIN", gsis_id="00-C", full_name="Kirk Cousins", position="QB",
                         report_status="Out"),
                    dict(week=10, team="BUF", gsis_id="00-R", full_name="Ray Davis", position="RB",
                         report_status="Doubtful"),
                    dict(week=9, team="BUF", gsis_id="00-A", full_name="Josh Allen", position="QB",
                         report_status="Out")])          # other week: ignored
SRC_META = {"depth_charts": {"url": "u1", "retrieved_utc": "2026-11-15T11:05:00Z"},
            "injuries": {"url": "u2", "retrieved_utc": "2026-11-15T11:05:00Z"}}


def test_starter_skips_out_and_doubtful_and_ignores_future_snapshots():
    st = SV.qb_starters(DEPTH, INJ, week=10, as_of="2026-11-15T12:00:00Z", source=SRC_META)
    s = st.set_index("team")
    assert s.loc["MIN", "starter_gsis"] == "00-M"          # Cousins Out -> next on the depth chart
    assert s.loc["BUF", "starter_gsis"] == "00-A"          # week 9 Out status is not this week's
    assert s.loc["MIN", "depth_dt"] == "2026-11-15T11:00:00Z"
    assert s.loc["MIN", "depth_source"] == "u1" and s.loc["MIN", "injury_retrieved_utc"] == "2026-11-15T11:05:00Z"
    assert "Kirk Cousins" in s.loc["MIN", "skipped"]


def test_inactives_override_after_t90():
    ina = pd.DataFrame([dict(team="MIN", gsis_id="00-M", player="Kyler Murray", source="gamebook",
                             retrieved_utc="2026-11-15T16:35:00Z")])
    st = SV.qb_starters(DEPTH, INJ, week=10, as_of="2026-11-15T12:00:00Z", source=SRC_META, inactives=ina)
    assert st.set_index("team").loc["MIN", "starter_gsis"] == "00-W"


def _legs():
    base = dict(week=10, kind="main", dec=1.9, p_nv=0.5, defender_verified=False, price_source="fixture",
                actual=np.nan, source="live", p_model=np.nan, market="rushyds", side="Under", line=20.5)
    return pd.DataFrame([dict(base, game_id="2026_10_MIN_GB", player="Carson Wentz", gsis="00-W", position="QB"),
                         dict(base, game_id="2026_10_MIN_GB", player="Kyler Murray", gsis="00-M", position="QB"),
                         dict(base, game_id="2026_10_MIN_GB", player="Kirk Cousins", gsis="00-C", position="QB"),
                         dict(base, game_id="2026_10_BUF_NYJ", player="Ray Davis", gsis="00-R", position="RB"),
                         dict(base, game_id="2026_10_BUF_NYJ", player="Josh Allen", gsis="00-A", position="QB"),
                         dict(base, game_id="2026_10_SEA_LV", player="Sam Darnold", gsis="00-D", position="QB")])


def test_gate_blocks_non_starters_out_doubtful_and_unknown_teams():
    legs = _legs().assign(team=["MIN", "MIN", "MIN", "BUF", "BUF", "SEA"])
    st = SV.qb_starters(DEPTH, INJ, week=10, as_of="2026-11-15T12:00:00Z", source=SRC_META)
    hist = {"00-M": 6, "00-W": 4, "00-A": 8, "00-C": 0}
    g = SV.gate_legs(legs, st, INJ, week=10, starter_history=hist)
    r = dict(zip(legs.player, g.gate))
    assert r["Carson Wentz"] == "qb_not_starter"
    assert r["Kyler Murray"] == "ok"
    assert r["Kirk Cousins"] == "out_or_doubtful"
    assert r["Ray Davis"] == "out_or_doubtful"            # availability gate applies to every position
    assert r["Josh Allen"] == "ok"
    assert r["Sam Darnold"] == "qb_starter_unknown"       # no depth chart for SEA -> fail closed
    assert set(g.columns) >= {"gate", "gate_detail", "depth_source", "depth_dt", "injury_source",
                              "injury_retrieved_utc"}


def test_gate_blocks_starter_with_thin_history():
    legs = _legs().iloc[[1]].assign(team="MIN")
    st = SV.qb_starters(DEPTH, INJ, week=10, as_of="2026-11-15T12:00:00Z", source=SRC_META)
    g = SV.gate_legs(legs, st, INJ, week=10, starter_history={"00-M": 1})
    assert g.gate.iloc[0] == "qb_starter_thin_history"


def test_starter_history_counts_primary_passer_games_before_cutoff():
    pbp = pd.DataFrame({"game_id": ["g1"] * 12 + ["g2"] * 3 + ["g3"] * 12,
                        "game_date": ["2026-10-01"] * 15 + ["2026-11-20"] * 12,
                        "season_type": "REG", "pass_attempt": 1, "passer_player_id": "00-M", "two_point_attempt": 0})
    assert SV.starter_history(pbp, cutoff="2026-11-12") == {"00-M": 1}


# ------------------------------------------------------------------ legs -> engine inputs -> p_model
def test_leg_inputs_team_opp_and_home_spread_sign():
    legs = _legs().iloc[[1, 4]]
    team = {"00-M": "MIN", "00-A": "BUF"}
    spreads = {"2026_10_MIN_GB": -2.5, "2026_10_BUF_NYJ": 4.0}    # home team's handicap (freeze_v2 convention)
    x = SV.leg_inputs(legs, team_of=team, home_spread=spreads)
    m = x.set_index("player")
    assert m.loc["Kyler Murray", "team"] == "MIN" and m.loc["Kyler Murray", "opp"] == "GB"
    assert m.loc["Kyler Murray", "spread"] == 2.5             # away team: -home line
    assert m.loc["Josh Allen", "team"] == "BUF" and m.loc["Josh Allen", "opp"] == "NYJ"
    assert m.loc["Josh Allen", "spread"] == -4.0


def test_home_spread_from_freeze_v2_consensus(tmp_path):
    f = tmp_path / "freeze_v2_x.json"
    f.write_text(json.dumps({"meta": {"game_id": "2026_10_BUF_NYJ"}, "markets": {},
                             "consensus": {"spread": {"consensus": {"line": 3.5}}}}))
    assert SV.home_spread_from_freeze(f) == ("2026_10_BUF_NYJ", 3.5)
    f.write_text(json.dumps({"meta": {"game_id": "2026_10_BUF_NYJ"}, "markets": {},
                             "consensus": {"spread": {"consensus": "no consensus"}}}))
    assert SV.home_spread_from_freeze(f) == ("2026_10_BUF_NYJ", None)


def test_attach_fills_graded_side_only_when_gate_ok():
    legs = _legs().assign(team=["MIN", "MIN", "MIN", "BUF", "BUF", "SEA"])
    legs = pd.concat([legs, legs.iloc[[1]].assign(side="Over")], ignore_index=True)
    legs.loc[len(legs)] = dict(legs.iloc[1], market="recyds")
    gate = pd.DataFrame({"gate": ["qb_not_starter", "ok", "out_or_doubtful", "out_or_doubtful", "ok",
                                  "qb_starter_unknown", "ok", "ok"]})
    ens = pd.DataFrame([dict(gsis="00-M", market="rushyds", line=20.5, p_over=0.4, p_under=0.6),
                        dict(gsis="00-A", market="rushyds", line=20.5, p_over=0.7, p_under=0.3)])
    out = SV.attach(legs, ens, gate)
    pm = list(out.p_model)
    assert pm[1] == 0.6 and pm[6] == 0.4 and pm[4] == 0.3
    assert all(pd.isna(pm[i]) for i in (0, 2, 3, 5, 7))
    assert out.p_model_source[1].startswith("simv56 ens")
    assert list(legs.columns) == list(out.columns[:len(legs.columns)])


def test_attach_never_overwrites_preset_p_model():
    legs = _legs().iloc[[1]].assign(team="MIN", p_model=0.11)
    ens = pd.DataFrame([dict(gsis="00-M", market="rushyds", line=20.5, p_over=0.4, p_under=0.6)])
    out = SV.attach(legs, ens, pd.DataFrame({"gate": ["ok"]}))
    assert out.p_model.iloc[0] == 0.11


def test_attached_legs_go_through_frozen_classifier_unchanged():
    from calibration.selective_edge_freeze import verify_hashes
    from calibration.selective_edge_live import grade_live
    verify_hashes()
    legs = _legs().iloc[[1, 4]].assign(team=["MIN", "BUF"])
    ens = pd.DataFrame([dict(gsis="00-M", market="rushyds", line=20.5, p_over=0.4, p_under=0.6),
                        dict(gsis="00-A", market="rushyds", line=20.5, p_over=0.7, p_under=0.3)])
    out = SV.attach(legs, ens, pd.DataFrame({"gate": ["ok", "ok"]}))
    ctx = pd.DataFrame({"carry_n_prior": [4.0, 4.0], "carry_n60": [0.0, 0.0], "carry_share": [0.1, 0.1],
                        "usual": [20.0, 20.0]})
    g = grade_live(out.reset_index(drop=True), pd.DataFrame(), context=ctx)
    assert list(g.label) == ["STRONG UNDER", "NO EDGE"] and (g.projection_ready == False).all()  # noqa: E712


def test_module_has_no_odds_api_and_only_allowlisted_urls():
    src = (ROOT / "calibration" / "simv56_pmodel.py").read_text()
    assert "the-odds-api" not in src and "ODDS_API" not in src and "projection_ready=True" not in src
    import re
    urls = set(re.findall(r"https?://[^\s\"']+", src))
    assert urls and all(u.startswith("https://github.com/nflverse/nflverse-data/releases/download/") for u in urls)
