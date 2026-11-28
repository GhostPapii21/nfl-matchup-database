"""NFL-90: branches stay separate, methods stay under their own names."""
import inspect
import json
from pathlib import Path

import numpy as np
import pytest

from pregame import packet as PK
from sunday import script_models as SM

ROOT = Path(__file__).resolve().parents[2]


def test_partition_uses_study_edges_and_covers_every_trial():
    margin = np.array([-3.01, -3, -2.9, 0, 2.9, 3, 9.99, 10, 14])
    masks = SM.assign_branches(margin)
    assert list(np.flatnonzero(masks["residual"])) == [0]
    assert list(np.flatnonzero(masks["competitive"])) == [1, 2, 3, 4]
    assert list(np.flatnonzero(masks["underdog_chases"])) == [5, 6]
    assert list(np.flatnonzero(masks["favorite_controls"])) == [7, 8]
    covered = sum(masks[k].astype(int) for k in (*SM.BRANCHES, SM.RESIDUAL))
    assert np.all(covered == 1)


def test_partition_refuses_nan_instead_of_dropping_the_trial():
    with pytest.raises(ValueError):
        SM.assign_branches(np.array([0.0, np.nan]))


def test_board_rule_matches_the_study_and_is_not_a_new_coefficient():
    assert SM.pass_multiplier(10) == pytest.approx(0.90)
    assert SM.pass_multiplier(-10) == pytest.approx(1.10)
    assert SM.pass_multiplier(0) == pytest.approx(1.0)
    assert SM.rush_multiplier(10) == pytest.approx(1.12)
    assert SM.rush_multiplier(-10) == pytest.approx(0.88)
    assert SM.favorite_from_home_spread("PIT", "DEN", 4.5) == ("DEN", "PIT", False)


def test_writer_refuses_overwrite_and_pooling_keys(tmp_path):
    store = SM.ArtifactStore(tmp_path / "out")
    store.write("a.json", {"branch": "competitive", "n_trials": 1})
    with pytest.raises(FileExistsError):
        store.write("a.json", {"branch": "competitive", "n_trials": 2})
    with pytest.raises(ValueError):
        store.write("b.json", {"branch_average": 1})


def test_sim_v6_cannot_be_marked_ran_or_relabeled():
    seen = set()
    with pytest.raises(ValueError):
        SM.validate_model_record({
            "engine_id": "sim_v6", "method": "absent", "sampling": None,
            "simulated": True, "three_method_sim_v6_ran": True, "projection_ready": False,
        }, seen)
    with pytest.raises(ValueError):
        SM.validate_model_record({
            "engine_id": "sim_v6", "method": "monte_carlo", "sampling": None,
            "simulated": False, "three_method_sim_v6_ran": False, "projection_ready": False,
        }, seen)
    with pytest.raises(ValueError):
        SM.validate_model_record({
            "engine_id": "possession_engine_v0", "method": "game_randomness", "sampling": None,
            "simulated": True, "projection_ready": False,
        }, seen)


def test_duplicate_model_record_is_rejected():
    seen = set()
    rec = {"engine_id": "period_engine_v0", "method": "monte_carlo", "sampling": "matchup_pair",
           "simulated": True, "projection_ready": False}
    SM.validate_model_record(rec, seen)
    with pytest.raises(ValueError):
        SM.validate_model_record(dict(rec), seen)


def _scores(apply_gr):
    # favorite is DEN (away). margin = away - home.
    home = np.array([10, 20, 21, 30], dtype=float)
    away = np.array([30, 24, 21, 10], dtype=float)
    if apply_gr:
        away = away + 7
    return home, away


def _period_fake(asof, home, away, *, n, seed, apply_gr=False, sampling="matchup_pair", gr_scale=None):
    fg_home, fg_away = _scores(apply_gr)
    assert n == len(fg_home)
    arrays = {"fg_home": fg_home, "fg_away": fg_away}
    for q in ("q1", "q2", "q3", "q4"):
        arrays[f"{q}_home"] = fg_home / 4
        arrays[f"{q}_away"] = fg_away / 4
    return {"n": n, "seed": seed, "arrays": arrays, "status": {
        "bias": "UNIMPLEMENTED_NO_FITTED_CALIB",
        "game_randomness": "APPLIED" if apply_gr else "NOT_APPLIED_THIS_CALL",
        "sampling": sampling,
    }}


def _possession_fake(cfg, pbp, n, seed):
    fg_home, fg_away = _scores(False)
    assert n == len(fg_home)
    columns = [
        ["DEN", "Bo Nix", "pass_att"], ["DEN", "Bo Nix", "pass_yds"], ["DEN", "Bo Nix", "pass_td"],
        ["DEN", "Courtland Sutton", "targets"], ["DEN", "Courtland Sutton", "rec_yds"], ["DEN", "Courtland Sutton", "rec_td"],
        ["DEN", "J.K. Dobbins", "carries"], ["DEN", "J.K. Dobbins", "rush_yds"], ["DEN", "J.K. Dobbins", "rush_td"],
        ["PIT", "Mason Rudolph", "pass_att"], ["PIT", "Jaylen Warren", "carries"], ["PIT", "George Pickens", "targets"],
    ]
    # One distinct row per trial so a branch mean cannot equal another branch's mean.
    values = np.array([
        [20, 220, 1, 8, 90, 1, 22, 100, 1, 28, 12, 6],
        [40, 310, 2, 11, 120, 0, 14, 60, 0, 36, 16, 9],
        [30, 250, 1, 9, 80, 1, 18, 70, 0, 32, 18, 7],
        [45, 340, 3, 12, 130, 1, 10, 40, 0, 22, 20, 4],
    ], dtype=float)
    return {
        "status": "OK",
        "n_completed": n,
        "seed": seed,
        "pooling_silently_applied": False,
        "limitations": ["fake possession call"],
        "arrays": {
            "fg_home": fg_home, "fg_away": fg_away,
            **{f"{q}_home": fg_home / 4 for q in ("q1", "q2", "q3", "q4")},
            **{f"{q}_away": fg_away / 4 for q in ("q1", "q2", "q3", "q4")},
        },
        "player_box": {
            "columns": columns,
            "values": values,
            "team_columns": [["DEN", "plays"], ["PIT", "plays"]],
            "team_values": np.array([[62, 58], [64, 60], [60, 61], [55, 66]], dtype=float),
        },
    }


def _sim100k_fake(game_id, packet_path):
    return 2, {
        "status": "REFUSED", "projection_ready": False, "ran": False, "ok": False,
        "gates": {"G7_asof": "REFUSED"}, "reasons": ["G7: now is not before kickoff"],
    }


def _packet():
    return {
        "projection_ready": False,
        "team_projection": {"status": "KEEP"},
        "game": {"game_id": "2026_12_DEN_PIT", "season": 2026, "week": 12, "home": "PIT", "away": "DEN"},
        "market": {"home_spread": 4.5, "total": 36.5},
    }


def _load(out, rel):
    return json.loads((out / rel).read_text())


def test_fake_replay_keeps_branches_and_methods_unpooled(tmp_path):
    out = tmp_path / "replay"
    packet = _packet()
    returned = SM.attach_to_packet(
        packet, root=ROOT, out_dir=out, possession_n=4, period_n=4, packet_path=None,
        period_simulate=_period_fake, possession_simulate=_possession_fake, sim100k_run=_sim100k_fake,
    )
    assert returned is packet
    assert packet["team_projection"]["status"] == "KEEP"
    assert packet["projection_ready"] is False
    assert packet["script_models"]["branches_pooled"] is False
    manifest = _load(out, "manifest.json")
    assert manifest["sim_v6_three_method_claimed"] is False
    assert set(SM.ENGINE_IDS).issubset({m.split(":")[0] for m in manifest["models"]})

    fav = _load(out, "branches/possession_engine_v0/simulate_games/data_only/favorite_controls.json")
    chase = _load(out, "branches/possession_engine_v0/simulate_games/data_only/underdog_chases.json")
    comp = _load(out, "branches/possession_engine_v0/simulate_games/data_only/competitive.json")
    resid = _load(out, "branches/possession_engine_v0/simulate_games/data_only/residual.json")
    assert fav["trial_indices"] == [0]
    assert chase["trial_indices"] == [1]
    assert comp["trial_indices"] == [2]
    assert resid["trial_indices"] == [3]
    assert fav["n_trials"] + chase["n_trials"] + comp["n_trials"] + resid["n_trials"] == 4
    # The board rule at +10 would turn 20 attempts into 18. The branch keeps the engine's 20.
    assert fav["pace_and_plays"]["DEN"]["pass_att"]["mean"] == pytest.approx(20)
    assert fav["pace_and_plays"]["DEN"]["board_rule_applied"] is False
    assert fav["board_rule_disclosure"]["applied_to_simulated_plays"] is False
    assert fav["players"][0]["player"] == "Bo Nix"
    assert fav["players"][0]["td_opportunity"]["pass_td"]["mean"] == pytest.approx(1)
    sutton = next(p for p in fav["players"] if p["player"] == "Courtland Sutton")
    assert sutton["targets"]["mean"] == pytest.approx(8)
    assert chase["pace_and_plays"]["DEN"]["pass_att"]["mean"] == pytest.approx(40)
    assert fav["score"]["final"]["favorite_margin"]["mean"] != chase["score"]["final"]["favorite_margin"]["mean"]

    mc = _load(out, "branches/period_engine_v0/monte_carlo/matchup_pair/favorite_controls.json")
    ind = _load(out, "branches/period_engine_v0/monte_carlo/independent/favorite_controls.json")
    gr = _load(out, "branches/period_engine_v0/game_randomness/matchup_pair/favorite_controls.json")
    assert mc["plays_supported"] is False and mc["players"] is None
    assert mc["method"] == "monte_carlo" and gr["method"] == "game_randomness"
    assert mc["trial_indices"] != gr["trial_indices"] or mc["score"] != gr["score"]
    assert mc["sampling"] != ind["sampling"]
    assert "sim_v6" not in mc["engine_id"]

    sim_v6 = _load(out, "models/sim_v6.json")
    assert sim_v6["simulated"] is False
    assert sim_v6["three_method_sim_v6_ran"] is False
    assert sim_v6["status"] == "REFUSED"
    assert sim_v6["trials"] == 0
    assert sim_v6["trials_required"] == 900_000
    assert sim_v6["calibration_status"] == "UNVALIDATED"
    sim100k = _load(out, "models/pipeline.sim100k__preflight.json")
    assert sim100k["simulated"] is False and sim100k["status"] == "REFUSED"
    simv56 = _load(out, "models/simv56__verify_engines.json")
    assert simv56["simulated"] is False and simv56["distinct_from_sim_v6"] is True
    assert _load(out, "models/main.json")["status"] == "NOT_CALLABLE_IN_THIS_REPOSITORY"
    assert _load(out, "models/lightning.json")["status"] == "NOT_CALLABLE_IN_THIS_REPOSITORY"
    bias = _load(out, "models/period_engine_v0__bias.json")
    assert bias["simulated"] is False and bias["not_sim_v6"] is True

    with pytest.raises(FileExistsError):
        SM.attach_to_packet(packet, root=ROOT, out_dir=out, possession_n=4, period_n=4,
                            period_simulate=_period_fake, possession_simulate=_possession_fake,
                            sim100k_run=_sim100k_fake)


def test_packet_build_does_not_run_script_models_unless_asked():
    params = inspect.signature(PK.build).parameters
    assert params["include_script_models"].default is False
    assert params["script_model_out"].default is None


def test_historical_den_pit_replay_uses_the_real_entrypoints(tmp_path):
    packet_path = ROOT / "pregame" / "packets" / "2026_12_DEN_PIT" / "packet.json"
    packet = json.loads(packet_path.read_text())
    out = tmp_path / "den_pit"
    manifest = SM.run_historical_replay(
        packet, out, root=ROOT, packet_path=packet_path, possession_n=2, period_n=300,
    )
    assert manifest["favorite"] == "DEN" and manifest["underdog"] == "PIT"
    assert manifest["projection_ready"] is False
    assert manifest["sim_v6_three_method_claimed"] is False
    poss = _load(out, "models/possession_engine_v0__simulate_games__data_only.json")
    assert poss["simulated"] is True
    assert poss["trials"] == 2
    assert poss["not_pipeline_sim100k"] is True
    assert poss["not_sim_v6"] is True
    counts = []
    for branch in (*SM.BRANCHES, SM.RESIDUAL):
        art = _load(out, f"branches/possession_engine_v0/simulate_games/data_only/{branch}.json")
        assert art["engine_id"] == "possession_engine_v0"
        assert art["pooled_with_other_branches"] is False
        counts.append(art["n_trials"])
        if art["n_trials"]:
            assert art["score"]["quarters"]["q1"]["supported"] is True
            assert art["plays_supported"] is True
    assert sum(counts) == 2
    period = _load(out, "models/period_engine_v0__monte_carlo__matchup_pair.json")
    gr = _load(out, "models/period_engine_v0__game_randomness__matchup_pair.json")
    assert period["simulated"] and gr["simulated"]
    assert period["seed"] != gr["seed"]
    assert period["method"] != gr["method"]
    p_counts, g_counts = [], []
    for branch in (*SM.BRANCHES, SM.RESIDUAL):
        p_art = _load(out, f"branches/period_engine_v0/monte_carlo/matchup_pair/{branch}.json")
        g_art = _load(out, f"branches/period_engine_v0/game_randomness/matchup_pair/{branch}.json")
        assert p_art["plays_supported"] is False and g_art["plays_supported"] is False
        p_counts.append(p_art["n_trials"])
        g_counts.append(g_art["n_trials"])
    assert sum(p_counts) == 300 and sum(g_counts) == 300
    sim100k = _load(out, "models/pipeline.sim100k__preflight.json")
    assert sim100k["simulated"] is False
    assert sim100k["status"] == "REFUSED"
    assert sim100k["trials"] is None
    assert sim100k["gates"]["G7_asof"] == "REFUSED"
    assert any(r.startswith("G7:") for r in sim100k["reasons"])
