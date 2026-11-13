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
W8_P_MODEL_PHASE4_IN_MEMORY = 0.4203777777777777  # after pd.read_csv on box pandas 3.0.6 (1 ulp below the text)
TOL = 1e-12                                       # cross-pandas-version tolerance (Ghost6)


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


def test_reproduce_w8_leg_from_committed_inputs_bit_for_bit(tmp_path):
    """Runs the three vendored engines on the committed W1-9 PBP (cut at the W8 rule) + committed players table."""
    src = SV.make_src(tmp_path / "src")
    legs = pd.DataFrame([W8_LEG])
    per = SV.run_all(legs, week=8, src=src, workdir=tmp_path)
    for e, t in W8_TRIPLES.items():
        r = per[e].iloc[0]
        assert (r.p_mc, r.p_bias, r.p_gr) == t, e
    assert SV.ensemble(per).p_under.iloc[0] == W8_P_MODEL_UNDER


PHASE4_LEGS = Path(__file__).parent / "fixtures" / "simv56_phase4_w8_w9_legs.csv"


def test_phase4_in_memory_value_is_within_tolerance_on_any_pandas():
    """Replaces the pandas-3.0.6-only test: the CSV hand-off moves the value by at most 1 ulp on any version."""
    import io
    buf = io.StringIO()
    pd.DataFrame({"p_under": [W8_P_MODEL_UNDER]}).to_csv(buf, index=False)
    for fp in (None, "high", "round_trip", "legacy"):
        v = pd.read_csv(io.StringIO(buf.getvalue()), float_precision=fp).p_under.iloc[0]
        assert abs(v - W8_P_MODEL_UNDER) <= TOL and abs(v - W8_P_MODEL_PHASE4_IN_MEMORY) <= TOL
    assert abs(SV._csv_rt(pd.DataFrame({"p_under": [W8_P_MODEL_UNDER]})).p_under.iloc[0] - W8_P_MODEL_UNDER) <= TOL


def test_phase4_legs_fixture_matches_the_committed_reproduction():
    f = pd.read_csv(PHASE4_LEGS, dtype={"gsis": str, "phase4_p_model": str})
    assert f.groupby("week").size().to_dict() == {8: 83, 9: 5} and f.phase4_p_model.notna().all()
    r = pd.read_csv(Path(SV.ROOT) / "research/runs/2026-11-13_simv56_pmodel/reproduction_w8_w9.csv",
                    dtype={"gsis": str}, float_precision="round_trip")
    m = f.assign(p=f.phase4_p_model.astype(float)).merge(r, on=["week", "gsis", "line"])
    assert len(m) == 88 and (m.p == m.p_model).all()


def test_reproduce_every_w8_w9_phase4_leg_within_tolerance_on_any_pandas(tmp_path):
    """All 83 Week 8 + 5 Week 9 Phase 4 rush-yds Under legs, run on the committed PBP + players table with the
    vendored engines; |p_under - Phase 4 p_model| <= 1e-12 on every pandas version (bit-exact on the box's 3.0.6)."""
    f = pd.read_csv(PHASE4_LEGS, dtype={"gsis": str, "phase4_p_model": str})
    src = SV.make_src(tmp_path / "src")
    for w, n in ((8, 83), (9, 5)):
        lw = f[f.week == w]
        per = SV.run_all(lw[["player", "gsis", "team", "opp", "market", "spread", "line"]], week=w, src=src,
                         workdir=tmp_path / f"w{w}")
        m = SV.ensemble(per).merge(lw.assign(want=lw.phase4_p_model.astype(float))[["gsis", "line", "want"]],
                                   on=["gsis", "line"])
        assert len(m) == n, (w, len(m))
        d = (m.p_under - m.want).abs()
        assert d.max() <= TOL, (w, m.loc[d.idxmax()].to_dict())


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


def test_thin_history_counts_only_the_leg_teams_games():
    """The engines build a player's log from his CURRENT team's games, so prior games for another team don't count."""
    pbp = pd.DataFrame({"game_id": ["a"] * 12 + ["b"] * 12, "game_date": "2026-10-01", "season_type": "REG",
                        "pass_attempt": 1, "two_point_attempt": 0, "passer_player_id": "00-C",
                        "posteam": ["LV"] * 12 + ["LV"] * 12})
    hist = SV.starter_history(pbp, cutoff="2026-11-12")
    assert hist == {("00-C", "LV"): 2}
    st = SV.qb_starters(DEPTH, INJ.iloc[[1]], week=10, as_of="2026-11-15T12:00:00Z", source=SRC_META)
    legs = _legs().iloc[[2]].assign(team="MIN")
    assert SV.gate_legs(legs, st, INJ.iloc[[1]], week=10, starter_history=hist).gate.iloc[0] == "qb_starter_thin_history"


def test_grade_subcommand_labels_unsettled_legs_without_crashing(tmp_path):
    """selective_edge_live's CLI writes live_graded.csv and then crashes in graduation() when no leg is settled yet
    (pre-game); `grade` calls the frozen grade_live() and writes the labels only."""
    legs = _legs().iloc[[1]].assign(team="MIN", p_model=0.6, gsis="00-0035228")
    f = tmp_path / "legs_p.csv"
    legs.to_csv(f, index=False)
    out = tmp_path / "g"
    assert SV.main(["grade", "--legs", str(f), "--out", str(out)]) == 0
    g = pd.read_csv(out / "live_graded.csv")
    assert g.label.iloc[0] == "STRONG UNDER" and (g.projection_ready == False).all()  # noqa: E712


# ------------------------------------------------------------------ embedded provenance (Ghost6, PR #44 follow-up)
import hashlib as _hl  # noqa: E402
import re as _re  # noqa: E402


def test_csv_handoff_parser_is_pinned():
    assert SV.FLOAT_PRECISION == "high"


def _prov_fixture():
    st = pd.DataFrame([
        dict(team="WAS", starter="J.Daniels", starter_gsis="00-0039910", depth_dt="2026-11-12T00:00:00Z", skipped="",
             depth_source=SV.SOURCE_URLS["depth_charts"], depth_retrieved_utc="2026-11-15T12:00:00+00:00",
             injury_source=SV.SOURCE_URLS["injuries"], injury_retrieved_utc="2026-11-15T12:00:01+00:00",
             inactives_source=None, inactives_retrieved_utc=None, as_of="2026-11-15T12:00:05Z", week=10),
        dict(team="NYG", starter="J.Dart", starter_gsis="00-0040000", depth_dt="2026-11-12T00:00:00Z", skipped="",
             depth_source=SV.SOURCE_URLS["depth_charts"], depth_retrieved_utc="2026-11-15T12:00:00+00:00",
             injury_source=SV.SOURCE_URLS["injuries"], injury_retrieved_utc="2026-11-15T12:00:01+00:00",
             inactives_source=None, inactives_retrieved_utc=None, as_of="2026-11-15T12:00:05Z", week=10),
        dict(team="MIN", starter="K.Cousins", starter_gsis="00-0029604", depth_dt="2026-11-12T00:00:00Z", skipped="",
             depth_source=SV.SOURCE_URLS["depth_charts"], depth_retrieved_utc="2026-11-15T12:00:00+00:00",
             injury_source=SV.SOURCE_URLS["injuries"], injury_retrieved_utc="2026-11-15T12:00:01+00:00",
             inactives_source=None, inactives_retrieved_utc=None, as_of="2026-11-15T12:00:05Z", week=10)])
    hist = {("00-0039910", "WAS"): 7, ("00-0040000", "NYG"): 6, ("00-0029604", "LV"): 9}
    res = pd.DataFrame([
        dict(week=10, game_id="2026_10_WAS_NYG", player="Jayden Daniels", gsis="00-0039910", team="WAS",
             position="QB", market="rushyds", side="Under", line=34.5, p_model=0.742, p_model_match="gsis"),
        dict(week=10, game_id="2026_10_WAS_NYG", player="Jayden Daniels", gsis="00-0039910", team="WAS",
             position="QB", market="rushyds", side="Over", line=34.5, p_model=0.258, p_model_match="gsis"),
        dict(week=10, game_id="2026_10_WAS_NYG", player="Cam Skattebo", gsis="00-0040001", team="NYG",
             position="RB", market="rushyds", side="Under", line=60.0, p_model=0.5, p_model_match="gsis"),
        dict(week=10, game_id="2026_10_WAS_NYG", player="Gated Guy", gsis="00-0040002", team="NYG",
             position="QB", market="rushyds", side="Under", line=9.5, p_model=np.nan,
             p_model_match="gated:qb_not_starter")])
    ens = pd.DataFrame([dict(gsis="00-0039910", market="rushyds", line=34.5, p_over=0.1 + 0.2, p_under=1 - (0.1 + 0.2)),
                        dict(gsis="00-0040001", market="rushyds", line=60.0, p_over=0.5, p_under=0.5)])
    return st, hist, res, ens


def _prov(st, hist, teams=None):
    return SV.build_provenance(st, hist, inputs_sha256={"pbp": "a" * 64, "players": "b" * 64}, teams=teams,
                               generated_utc="2026-11-15T12:00:10Z")


def test_qb_override_list_carries_team_starter_source_timestamp_and_gate():
    st, hist, _, _ = _prov_fixture()
    q = {d["team"]: d for d in SV.qb_override_list(st, hist)}
    assert q["WAS"]["starter_gsis"] == "00-0039910" and q["WAS"]["qb_gate"] == "ok"
    assert q["WAS"]["depth_source"].startswith("https://github.com/nflverse/") and q["WAS"]["depth_retrieved_utc"]
    assert q["WAS"]["injury_retrieved_utc"] and q["WAS"]["prior_team_primary_games"] == 7
    assert q["MIN"]["qb_gate"] == "qb_starter_thin_history"        # Cousins: 0 MIN games
    assert all(v is None or isinstance(v, (str, int)) for d in q.values() for v in d.values())   # JSON-clean, no NaN


def test_build_provenance_has_source_code_sha_inputs_and_digest():
    st, hist, _, _ = _prov_fixture()
    p = _prov(st, hist)
    assert p["prob_source"] == "sim_v5_v6_ensemble" == SV.PROB_SOURCE_ID
    assert p["prob_schema"] == SV.PROBS_SCHEMA and p["p_model_settings"] == SV.P_MODEL_SOURCE
    assert _re.fullmatch(r"[0-9a-f]{40}", p["code_git_sha"])
    assert p["code_sha256"] == SV._sha(Path(SV.__file__))
    assert p["inputs_sha256"] == {"pbp": "a" * 64, "players": "b" * 64}
    assert {d["team"] for d in p["qb_overrides"]} == {"WAS", "NYG", "MIN"}
    assert {d["team"] for d in _prov(st, hist, teams=["WAS", "NYG"])["qb_overrides"]} == {"WAS", "NYG"}


def test_probs_file_embeds_verifiable_provenance_per_game(tmp_path):
    st, hist, res, ens = _prov_fixture()
    files = SV.write_probs_files(res, ens, st, hist, {"pbp": "a" * 64}, tmp_path, generated_utc="2026-11-15T12:00:10Z")
    assert [f.name for f in files] == ["2026_10_WAS_NYG.simv56.probs.csv"]
    t = pd.read_csv(files[0], dtype=str, keep_default_na=False)
    assert list(t.columns) == list(SV.PROBS_COLUMNS)
    assert len(t) == 2 and set(t.gsis) == {"00-0039910", "00-0040001"}           # gated / no-sim legs not written
    assert (t.prob_source == "sim_v5_v6_ensemble").all() and (t.prob_schema == SV.PROBS_SCHEMA).all()
    for c in SV.PROVENANCE_FIELDS:
        assert t[c].nunique() == 1                                               # identical on every row
    q = json.loads(t.qb_overrides.iloc[0])
    assert {d["team"] for d in q} == {"WAS", "NYG"}                             # the game's two teams
    r = t.set_index("gsis").loc["00-0039910"]
    assert float(r.p_under) == 1 - (0.1 + 0.2) and float(r.p_over) == 0.1 + 0.2  # exact text round trip
    assert r.p_under == repr(1 - (0.1 + 0.2))
    # both digests recompute from the file text alone
    assert SV.data_digest(t) == t.data_sha256.iloc[0]
    prov = SV.provenance_from_row(t.iloc[0])
    assert SV.provenance_digest(prov) == t.provenance_sha256.iloc[0]
    canon = json.dumps(prov, sort_keys=True, separators=(",", ":"))
    assert _hl.sha256(canon.encode()).hexdigest() == t.provenance_sha256.iloc[0]


def test_ensemble_and_legs_outputs_carry_run_provenance_columns():
    st, hist, res, ens = _prov_fixture()
    p = _prov(st, hist)
    for df in (res, ens):
        out = SV.stamp_provenance(df, p)
        assert (out.prob_source == "sim_v5_v6_ensemble").all()
        assert (out.code_git_sha == p["code_git_sha"]).all()
        assert json.loads(out.qb_overrides.iloc[0]) == p["qb_overrides"]
        assert json.loads(out.inputs_sha256.iloc[0]) == p["inputs_sha256"]
        assert (out.provenance_sha256 == SV.provenance_digest(p)).all()
