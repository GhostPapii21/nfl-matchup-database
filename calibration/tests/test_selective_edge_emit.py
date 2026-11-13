"""Stacked on PR #40: roster join (position, gsis, season carry share with source + pull time) and the pre-kickoff
flag emitter (timestamped UTC + ET flags, refuses kicked-off games and post-kick prices, commit/push guarded).
Synthetic data only; no network, no git push. Research only; projection_ready stays false."""
from __future__ import annotations
import json
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import pytest

from calibration import selective_edge as se
from calibration import selective_edge_emit as EM
from calibration import selective_edge_roster as RJ

GAME = "2026_10_WAS_NYG"
KICK = "2026-11-15T18:00:00Z"


def _roster():
    rows = [
        dict(season=2026, week=10, team="WAS", position="QB", full_name="Jayden Daniels", football_name="Jayden",
             last_name="Daniels", gsis_id="00-QB1", status="ACT"),
        dict(season=2026, week=10, team="NYG", position="RB", full_name="Cam Skattebo", football_name="Cam",
             last_name="Skattebo", gsis_id="00-RB1", status="ACT"),
        dict(season=2026, week=10, team="WAS", position="RB", full_name="Brian Robinson Jr.", football_name="Brian",
             last_name="Robinson", gsis_id="00-RB2", status="ACT"),
        # same name on both teams in the game -> ambiguous -> unknown
        dict(season=2026, week=10, team="WAS", position="WR", full_name="Mike Smith", football_name="Mike",
             last_name="Smith", gsis_id="00-W1", status="ACT"),
        dict(season=2026, week=10, team="NYG", position="TE", full_name="Mike Smith", football_name="Mike",
             last_name="Smith", gsis_id="00-T1", status="ACT"),
        # a player on a team not in the game is never matched
        dict(season=2026, week=10, team="BUF", position="QB", full_name="Josh Allen", football_name="Josh",
             last_name="Allen", gsis_id="00-QB9", status="ACT"),
        # week 11 row must not be used for a week-10 leg
        dict(season=2026, week=11, team="NYG", position="WR", full_name="Cam Skattebo", football_name="Cam",
             last_name="Skattebo", gsis_id="00-RB1", status="ACT"),
        dict(season=2026, week=9, team="NYG", position="FB", full_name="Cam Skattebo", football_name="Cam",
             last_name="Skattebo", gsis_id="00-RB1", status="ACT"),
    ]
    return pd.DataFrame(rows)


def _pbp(weeks=range(6, 10), rb_share=7, team="NYG", rb="00-RB1", qb_team="WAS", qb="00-QB1"):
    rows = []
    for w in weeks:
        gid = f"2026_{w:02d}_X_{team}"
        for i in range(10):
            rows.append(dict(week=w, game_id=gid, posteam=team, rush_attempt=1, qb_kneel=0, pass_attempt=0,
                             rusher_player_id=(rb if i < rb_share else "00-OTHER"), receiver_player_id=None,
                             rushing_yards=6.0, receiving_yards=np.nan, complete_pass=0, two_point_attempt=0,
                             season_type="REG"))
        gq = f"2026_{w:02d}_Y_{qb_team}"
        for i in range(10):
            rows.append(dict(week=w, game_id=gq, posteam=qb_team, rush_attempt=1, qb_kneel=0, pass_attempt=0,
                             rusher_player_id=(qb if i < 2 else "00-RBX"), receiver_player_id=None,
                             rushing_yards=4.0, receiving_yards=np.nan, complete_pass=0, two_point_attempt=0,
                             season_type="REG"))
    # a week-10 play must never leak into context
    rows.append(dict(rows[0], week=10, game_id="2026_10_LEAK", rushing_yards=999.0))
    return pd.DataFrame(rows)


def _legs():
    return pd.DataFrame([
        dict(week=10, game_id=GAME, player="Jayden Daniels", market="rushyds", side="Under", kind="main", line=38.5),
        dict(week=10, game_id=GAME, player="Cam Skattebo", market="rushyds", side="Under", kind="main", line=70.5),
        dict(week=10, game_id=GAME, player="Brian Robinson", market="rushyds", side="Under", kind="main", line=30.5),
        dict(week=10, game_id=GAME, player="Mike Smith", market="rushyds", side="Under", kind="main", line=5.5),
        dict(week=10, game_id=GAME, player="Josh Allen", market="rushyds", side="Under", kind="main", line=30.5),
        dict(week=10, game_id=GAME, player="Nobody Here", market="rushyds", side="Under", kind="main", line=9.5),
    ])


PROV = dict(roster_source="nflverse roster_weekly_2026.parquet", roster_pulled_utc="2026-11-13T16:33:47Z",
            pbp_source="pbp_2026_w1_9.parquet", pbp_pulled_utc="2026-11-12T16:16:00Z")


# ---------------------------------------------------------------- roster join
def test_roster_join_populates_position_gsis_with_provenance():
    out = RJ.join_roster(_legs(), _roster(), _pbp(), **PROV).set_index("player")
    assert out.loc["Jayden Daniels", "gsis"] == "00-QB1" and out.loc["Jayden Daniels", "position"] == "QB"
    assert out.loc["Jayden Daniels", "team"] == "WAS"
    assert out.loc["Cam Skattebo", "position"] == "FB" or out.loc["Cam Skattebo", "position"] == "RB"
    for c in ("roster_source", "roster_pulled_utc", "pbp_source", "pbp_pulled_utc", "roster_match"):
        assert out[c].notna().all(), c
    assert (out.roster_pulled_utc == "2026-11-13T16:33:47Z").all()


def test_roster_join_uses_latest_week_not_after_leg_week():
    out = RJ.join_roster(_legs(), _roster(), _pbp(), **PROV).set_index("player")
    assert out.loc["Cam Skattebo", "position"] == "RB"      # week 10 row, not the week 11 WR row or week 9 FB row
    assert out.loc["Cam Skattebo", "roster_week"] == 10


def test_roster_join_normalizes_suffixes_and_punctuation():
    out = RJ.join_roster(_legs(), _roster(), _pbp(), **PROV).set_index("player")
    assert out.loc["Brian Robinson", "gsis"] == "00-RB2"


def test_roster_join_unknown_when_ambiguous_missing_or_other_team():
    out = RJ.join_roster(_legs(), _roster(), _pbp(), **PROV).set_index("player")
    for p, why in (("Mike Smith", "ambiguous"), ("Josh Allen", "no_match"), ("Nobody Here", "no_match")):
        assert pd.isna(out.loc[p, "gsis"]) and pd.isna(out.loc[p, "position"]), p
        assert out.loc[p, "roster_match"] == why


def test_roster_join_season_carry_share_prior_weeks_only():
    out = RJ.join_roster(_legs(), _roster(), _pbp(), **PROV).set_index("player")
    assert out.loc["Cam Skattebo", "season_carry_share"] == pytest.approx(0.7)
    assert out.loc["Cam Skattebo", "season_games"] == 4
    assert out.loc["Jayden Daniels", "season_carry_share"] == pytest.approx(0.2)
    assert pd.isna(out.loc["Nobody Here", "season_carry_share"])


def test_roster_join_refuses_without_pull_time():
    with pytest.raises(RJ.RosterJoinError, match="pull"):
        RJ.join_roster(_legs(), _roster(), _pbp(), **{**PROV, "roster_pulled_utc": ""})


def test_unmatched_rush_leg_classifies_insufficient():
    out = RJ.join_roster(_legs(), _roster(), _pbp(), **PROV)
    out = se.attach_context(out, _pbp()[lambda d: d.week < 10])
    out = out.assign(dec=1.91, p_nv=0.5, p_model=0.6, price_source="book:test", defender_verified=False)
    lab = se.classify(out, {"strong_markets": ["rushyds"], "alt_min_cushion": None}).set_index("player")
    for p in ("Mike Smith", "Josh Allen", "Nobody Here"):
        assert lab.loc[p, "label"] == se.INSUFFICIENT and lab.loc[p, "reason"] == "position_unknown"


# ---------------------------------------------------------------- probabilities (nfl75-rush-dist/1 cdf)
def _cdf(rows):
    out = []
    for gsis, player, team, pos, med in rows:
        for k in np.arange(-20.5, 251.0, 1.0):
            pu = float(np.clip((k - med) / 60 + 0.5, 0, 1))
            out.append(dict(game_id=GAME, team=team, player=player, gsis=gsis, position=pos, line=k, p_under=pu,
                            p_over=1 - pu))
    return pd.DataFrame(out)


CDF_ROWS = [("00-QB1", "J.Daniels", "WAS", "QB", 20.0), ("00-RB1", "C.Skattebo", "NYG", "RB", 60.0)]


def test_p_model_from_rush_dist_by_gsis_only():
    legs = RJ.join_roster(_legs(), _roster(), _pbp(), **PROV).assign(p_model=np.nan)
    out = EM.attach_probs(legs, _cdf(CDF_ROWS), source="probs.csv sha=x").set_index("player")
    assert out.loc["Jayden Daniels", "p_model"] == pytest.approx((38.5 - 20) / 60 + 0.5)
    assert out.loc["Cam Skattebo", "p_model"] == pytest.approx((70.5 - 60) / 60 + 0.5)
    assert pd.isna(out.loc["Brian Robinson", "p_model"]) and out.loc["Brian Robinson", "p_model_match"] == "no_player"
    assert pd.isna(out.loc["Nobody Here", "p_model"])  # no gsis -> no name fallback
    assert out.loc["Jayden Daniels", "p_model_source"].startswith("probs.csv")


def test_p_model_integer_line_removes_push():
    cdf = _cdf(CDF_ROWS)
    legs = pd.DataFrame([dict(week=10, game_id=GAME, gsis="00-QB1", market="rushyds", side="Under", line=30.0)])
    out = EM.attach_probs(legs, cdf, source="s")
    pu = (29.5 - 20) / 60 + 0.5
    po = 1 - ((30.5 - 20) / 60 + 0.5)
    assert out.p_model.iloc[0] == pytest.approx(pu / (pu + po))


def test_p_model_only_for_rush_yards_and_never_overwrites():
    cdf = _cdf(CDF_ROWS)
    legs = pd.DataFrame([dict(week=10, game_id=GAME, gsis="00-QB1", market="recyds", side="Under", line=30.5),
                         dict(week=10, game_id=GAME, gsis="00-QB1", market="rushyds", side="Under", line=30.5,
                              p_model=0.11)])
    out = EM.attach_probs(legs, cdf, source="s")
    assert pd.isna(out.p_model.iloc[0]) and out.p_model.iloc[1] == 0.11


def test_probs_schema_is_checked():
    with pytest.raises(EM.EmitError, match="columns"):
        EM.check_probs(pd.DataFrame([dict(game_id=GAME, gsis="x", line=1.5, p_under=0.5)]))


# ---------------------------------------------------------------- emitter
def _freeze(tmp_path, pulled="2026-11-15T15:30:00Z", kick=KICK, name="freeze_v2_a.json"):
    mk, cons = {}, {}
    for p, ln in (("Jayden Daniels", 38.5), ("Cam Skattebo", 70.5), ("Nobody Here", 9.5)):
        k = f"rushing_yards|{p}"
        mk[k] = {"best_retail_price": {"Over": {"book": "fanduel", "line": ln, "price": -110},
                                       "Under": {"book": "draftkings", "line": ln, "price": -110}}}
        cons[k] = {"consensus": {"line": ln, "no_vig": {"Over": 0.5, "Under": 0.5}}}
    d = {"meta": {"game_id": GAME, "commence_utc": kick, "lines_retrieved_utc": pulled}, "markets": mk,
         "consensus": cons}
    p = tmp_path / name
    p.write_text(json.dumps(d))
    return p


def _run(tmp_path, now, **kw):
    return EM.emit(freeze_paths=[kw.get("freeze") or _freeze(tmp_path)], probs=_cdf(CDF_ROWS), probs_source="p.csv",
                   roster=_roster(), pbp=_pbp(), date="2026-11-15", out_root=tmp_path / "research/runs", now=now,
                   **PROV)


def _t(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def test_emitter_writes_timestamped_flags_utc_and_et(tmp_path):
    r = _run(tmp_path, _t("2026-11-15T16:00:00Z"))
    d = tmp_path / "research/runs/2026-11-15_live_flags"
    assert r["out_dir"] == d and r["emitted_games"] == [GAME] and r["refused_games"] == {}
    flags = pd.read_csv(r["flags_csv"])
    assert (flags.emitted_utc == "2026-11-15T16:00:00Z").all()
    assert (flags.emitted_et == "2026-11-15 11:00:00 EST").all()
    assert (flags.kickoff_et == "2026-11-15 13:00:00 EST").all()
    assert (flags.minutes_to_kickoff == 120.0).all() and (flags.projection_ready == False).all()  # noqa: E712
    f = flags[flags.side == "Under"].set_index("player")
    assert f.loc["Jayden Daniels", "label"] == se.STRONG_UNDER  # QB, model 0.808 vs no-vig 0.5
    assert f.loc["Cam Skattebo", "label"] == se.STRONG_UNDER    # RB at 70% in 4/4 prior games
    assert f.loc["Nobody Here", "reason"] == "position_unknown"
    m = json.loads(r["manifest_json"].read_text())
    assert m["run_utc"] == "2026-11-15T16:00:00Z" and m["run_et"].endswith("EST")
    assert m["projection_ready"] is False and m["research_only"] is True
    assert m["games"][GAME]["price_pulled_utc"] == "2026-11-15T15:30:00Z"
    assert set(m["inputs_sha256"]) >= {"freeze", "probs", "roster", "pbp"} or m["inputs_sha256"]
    assert m["freeze_manifest_sha256"]


def test_emitter_refuses_game_already_kicked_off(tmp_path):
    for now in ("2026-11-15T18:00:00Z", "2026-11-15T21:00:00Z"):
        with pytest.raises(EM.EmitError, match="no game"):
            _run(tmp_path, _t(now))
    assert not list((tmp_path / "research/runs").rglob("flags_*.csv"))


def test_emitter_refuses_price_pulled_at_or_after_kickoff_or_missing(tmp_path):
    for pulled, why in (("2026-11-15T18:05:00Z", "price_pulled_after_kickoff"), ("2026-11-15T18:00:00Z",
                        "price_pulled_after_kickoff"), (None, "price_pull_time_unknown"),
                        ("2026-11-15T16:30:00Z", "price_pull_time_in_future")):
        fz = _freeze(tmp_path, pulled=pulled, name=f"fz_{pulled}.json")
        with pytest.raises(EM.EmitError, match=f"no game.*{why}"):
            _run(tmp_path, _t("2026-11-15T16:00:00Z"), freeze=fz)


def test_emitter_skips_only_the_kicked_off_game(tmp_path):
    early = _freeze(tmp_path, kick="2026-11-15T15:00:00Z", pulled="2026-11-15T14:00:00Z", name="early.json")
    d = json.loads(early.read_text())
    d["meta"]["game_id"] = "2026_10_BUF_NYJ"
    early.write_text(json.dumps(d))
    r = EM.emit(freeze_paths=[early, _freeze(tmp_path)], probs=_cdf(CDF_ROWS), probs_source="p", roster=_roster(),
                pbp=_pbp(), date="2026-11-15", out_root=tmp_path / "research/runs",
                now=_t("2026-11-15T16:00:00Z"), **PROV)
    assert r["emitted_games"] == [GAME] and "kicked_off" in r["refused_games"]["2026_10_BUF_NYJ"]
    assert set(pd.read_csv(r["flags_csv"]).game_id) == {GAME}


def test_emitter_never_overwrites_a_prior_run(tmp_path):
    a = _run(tmp_path, _t("2026-11-15T16:00:00Z"))
    b = _run(tmp_path, _t("2026-11-15T16:05:00Z"))
    assert a["flags_csv"] != b["flags_csv"] and a["flags_csv"].exists() and b["flags_csv"].exists()
    with pytest.raises(EM.EmitError, match="exists"):
        _run(tmp_path, _t("2026-11-15T16:00:00Z"))


def test_emitter_refuses_non_holdout_week(tmp_path):
    fz = _freeze(tmp_path)
    d = json.loads(fz.read_text())
    d["meta"]["game_id"] = "2026_09_WAS_NYG"
    fz.write_text(json.dumps(d))
    with pytest.raises(Exception, match="10-12"):
        _run(tmp_path, _t("2026-11-15T16:00:00Z"), freeze=fz)


# ---------------------------------------------------------------- commit / push guards (no real git)
def test_git_guard_refuses_pregame_github_and_outside_paths():
    EM.guard_paths(["research/runs/2026-11-15_live_flags/flags_x.csv"], "research/runs/2026-11-15_live_flags")
    for bad, why in (("pregame/x.json", "pregame"), (".github/workflows/a.yml", "github"),
                     ("calibration/selective_edge.py", "outside")):
        with pytest.raises(EM.EmitError, match=why):
            EM.guard_paths([bad], "research/runs/2026-11-15_live_flags")
    with pytest.raises(EM.EmitError, match="pregame"):   # even under a run dir named like pregame
        EM.guard_paths(["pregame/runs/x.csv"], "pregame/runs")


def test_git_guard_refuses_non_research_branch():
    EM.guard_branch("research/live-flags-2026-11-15")
    for b in ("main", "master", "ghost6/grading-loop", ""):
        with pytest.raises(EM.EmitError):
            EM.guard_branch(b)


def test_commit_message_refs_never_closes():
    msg = EM.commit_message("2026-11-15", "2026-11-15T16:00:00Z", [GAME])
    assert "refs NFL-75" in msg
    assert not any(w in msg.lower() for w in ("closes", "fixes", "resolves"))
