"""Restored sim_v6 identity and reproduction, plus sim_v6r1 behaviour. Runs offline against committed data."""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
import simsrc  # noqa: E402

BLOB = "ab2144f03f6ca3b57950a1f2528e305193e723cd"


def git_blob_sha(p: Path) -> str:
    b = p.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def test_restored_file_is_the_historical_blob_byte_for_byte():
    assert git_blob_sha(TOOLS / "sim_v6_ab2144f0.py") == BLOB


@pytest.fixture(scope="module")
def mods():
    simsrc.prepare(pbp=ROOT / "data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet")
    import sim_v6_ab2144f0 as V6
    import sim_v6r1 as R
    return V6, R


def test_restored_engine_reproduces_committed_1096_row_backtest(mods):
    """The committed sim_v6_backtest.csv was made by this engine with the opponent factor at 0.5 (CC_OPP=0.5)."""
    V6, _ = mods
    ref = pd.read_csv(ROOT / "calibration/simv56/engines/sim_v6_backtest.csv")
    assert len(ref) == 1096
    P = V6._P; W = 4
    E = V6.Engine(cutoff=P[P.week == W].game_date.min(), calib=None, n=4000)
    orig = V6.Engine.oppadj
    E.oppadj = lambda opp, pg, kind, shrink=0.5: orig(E, opp, pg, kind, shrink)
    PW = P[P.week == W]; checked = 0
    for _, r in ref[ref.week == W].head(12).iterrows():
        g, mkt = r.gsis, r.market
        q = PW[(PW.passer_player_id == g) | (PW.receiver_player_id == g) | (PW.rusher_player_id == g)]
        gid = q.game_id.iloc[0]; Q = PW[PW.game_id == gid]; t = q.posteam.mode().iloc[0]
        opp = Q.home_team.iloc[0] if Q.away_team.iloc[0] == t else Q.away_team.iloc[0]
        o, _ = E.sim(dict(player=g, gsis=g, team=t, opp=opp, market=mkt, spread=0.0), raw=True)
        for m in V6.MODES:
            assert o[m]["cmedian"] == pytest.approx(r[f"pred_{m}"], abs=1e-9)
        checked += 1
    assert checked == 12


def test_calibration_file_is_the_original_fit_of_its_backtest(mods):
    V6, _ = mods
    df = pd.read_csv(TOOLS / "sim_v6_backtest.csv")
    calib = json.loads((TOOLS / "sim_v6_calib.json").read_text())
    assert calib["multipliers"] == json.loads(json.dumps(V6.fit(df)))


def test_original_bias_equals_mc_multipliers_which_is_why_r1_exists():
    m = json.loads((TOOLS / "sim_v6_calib.json").read_text())["multipliers"]
    assert {k: v["M"] for k, v in m["bias"].items()} == {k: v["M"] for k, v in m["mc"].items()}


def test_r1_is_labelled_as_replacement(mods):
    _, R = mods
    assert R.VERSION == "sim_v6r1" and R.IS_ORIGINAL_SIM_V6 is False
    assert R.METHODS == ("mc_nb", "gr_share", "eb_boot")


def test_scenario_probabilities_sum_to_one(mods):
    _, R = mods
    for spread, fav in ((-7.0, True), (7.0, False), (0.0, True), (-14.5, True)):
        assert sum(R.scenario_probs(spread, fav).values()) == pytest.approx(1.0, abs=1e-9)


@pytest.fixture(scope="module")
def leg_engine(mods):
    _, R = mods
    E = R.Engine(cutoff="2026-11-03", n=3000)
    tg = E.pp[E.pp.posteam == "CIN"].receiver_player_id.value_counts().index[0]
    return E, dict(player=tg, gsis=tg, team="CIN", opp="PIT", market="recyds", spread=7.0, team_is_fav=False,
                   rungs=[50.5], game_id="t")


def test_r1_is_deterministic(leg_engine, mods):
    _, R = mods
    E, leg = leg_engine
    a, _ = E.sim_r1(dict(leg), scenarios=("competitive",), raw=True)
    b, _ = E.sim_r1(dict(leg), scenarios=("competitive",), raw=True)
    assert a == b


def test_trailing_scenario_raises_parametric_pass_volume(leg_engine, mods):
    _, R = mods
    E, leg = leg_engine   # underdog: favorite_controls means this team trails by 10+
    o, _ = E.sim_r1(dict(leg, market="rec"), scenarios=("favorite_controls", "residual"), raw=True,
                    methods=("mc_nb", "gr_share"))
    for m in ("mc_nb", "gr_share"):
        assert o[m]["favorite_controls"]["mean"] > o[m]["residual"]["mean"]


def test_methods_are_not_copies(leg_engine, mods):
    _, R = mods
    E, leg = leg_engine
    o, _ = E.sim_r1(dict(leg), scenarios=("competitive",), raw=True)
    means = [o[m]["competitive"]["mean"] for m in R.METHODS]
    assert len({round(x, 6) for x in means}) == 3
    assert all(o[m]["competitive"]["trials"] == 3000 for m in R.METHODS)
