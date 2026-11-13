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

# ---------------------------------------------------------------- countable stamp (Ghost6 review of PR #44 + follow-up)
# countable=true only when the probability FILE's embedded, digest-verified provenance says the legacy sim_v5/v6
# ensemble the Phase 4 classifier was fit on AND carries an ok QB override entry for that flag's team. The CLI
# --prob-source / --qb-override-applied flags are recorded but can never make a flag countable.
import hashlib  # noqa: E402
from pathlib import Path  # noqa: E402

FIXTURE = Path(__file__).parent / "fixtures" / "simv56_2026_10_WAS_NYG.simv56.probs.csv"
SHA40 = "4844e12db89c5848dc13e53d52c8babf71f9174b"
DEPTH = "https://github.com/nflverse/nflverse-data/releases/download/depth_charts/depth_charts_2026.parquet"
INJ = "https://github.com/nflverse/nflverse-data/releases/download/injuries/injuries_2026.parquet"


def _qb(team, starter, gsis, gate="ok", **kw):
    d = dict(team=team, starter=starter, starter_gsis=gsis, qb_gate=gate, prior_team_primary_games=6, skipped=None,
             depth_source=DEPTH, depth_dt="2026-11-14T15:00:00Z", depth_retrieved_utc="2026-11-15T12:00:00+00:00",
             injury_source=INJ, injury_retrieved_utc="2026-11-15T12:00:00+00:00", inactives_source=None,
             inactives_retrieved_utc=None, as_of="2026-11-15T12:00:05Z")
    d.update(kw)
    return d


QB_BOTH = [_qb("NYG", "J.Dart", "00-QBN"), _qb("WAS", "Jayden Daniels", "00-QB1")]


def _canon(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"))


def _write_simv56(path, *, qb=QB_BOTH, prob_source="sim_v5_v6_ensemble", code_sha=SHA40, dirty=False,
                  rows=None, tamper=None):
    """Independent writer of the nfl75-simv56-probs/1 spec (mirrors calibration/simv56_pmodel.py on PR #45)."""
    rows = rows or [("WAS", "J.Daniels", "00-QB1", "QB", 38.5, 0.8083333333333333),
                    ("NYG", "C.Skattebo", "00-RB1", "RB", 70.5, 0.675)]
    data = [dict(game_id=GAME, team=t, player=p, gsis=g, position=pos, market="rushyds", line=repr(float(ln)),
                 p_under=repr(pu), p_over=repr(1 - pu)) for t, p, g, pos, ln, pu in rows]
    srt = sorted(data, key=lambda r: (r["game_id"], r["gsis"], r["market"], float(r["line"])))
    body = "".join(",".join(r[c] for c in ("game_id", "team", "gsis", "market", "line", "p_under", "p_over")) + "\n"
                   for r in srt)
    prov = dict(prob_schema="nfl75-simv56-probs/1", prob_source=prob_source,
                p_model_settings="simv56 ens(sim_v5,sim_v6,sim_v6_fix)|opp0.5|n20000", code_git_sha=code_sha,
                code_dirty=dirty, code_sha256="c" * 64, inputs_sha256={"pbp": "a" * 64, "players": "b" * 64},
                qb_overrides=qb, generated_utc="2026-11-15T12:00:10Z",
                data_sha256=hashlib.sha256(body.encode()).hexdigest())
    text = {k: (_canon(v) if k in ("inputs_sha256", "qb_overrides") else ("true" if v is True else "false"
                if v is False else v)) for k, v in prov.items()}
    text["provenance_sha256"] = hashlib.sha256(_canon(prov).encode()).hexdigest()
    t = pd.DataFrame(data)
    for k, v in text.items():
        t[k] = v
    if tamper:
        tamper(t)
    t.to_csv(path, index=False)
    return path


def _legs_joined():
    return RJ.join_roster(_legs(), _roster(), _pbp(), **PROV).assign(p_model=np.nan)


def _stamped(tmp_path, cli_source=None, cli_qb=False, **kw):
    f = _write_simv56(tmp_path / f"{GAME}.simv56.probs.csv", **kw)
    probs, _ = EM.load_probs([f])
    out = EM.attach_probs(_legs_joined(), probs, source="simv56")
    return EM.stamp_countable(out, prob_source=cli_source, qb_override_applied=cli_qb).set_index("player")


def test_verified_legacy_file_with_team_qb_override_is_countable_without_cli_flags(tmp_path):
    out = _stamped(tmp_path)
    for p in ("Jayden Daniels", "Cam Skattebo"):
        assert bool(out.loc[p, "countable"]) is True, out.loc[p, "countable_reason"]
        assert out.loc[p, "countable_reason"] == "embedded_fit_ensemble_with_qb_override"
        assert out.loc[p, "prob_source"] == EM.FIT_ENSEMBLE_PROB_SOURCE and out.loc[p, "countable_mark"] == ""
    assert json.loads(out.loc["Jayden Daniels", "qb_override_entry"])["starter_gsis"] == "00-QB1"
    assert out.loc["Jayden Daniels", "prob_code_git_sha"] == SHA40


def test_simv56_p_model_is_the_exact_file_value_at_the_exact_line(tmp_path):
    out = _stamped(tmp_path, rows=[("WAS", "J.Daniels", "00-QB1", "QB", 38.5, 0.1 + 0.2),
                                   ("NYG", "C.Skattebo", "00-RB1", "RB", 70.5, 0.675)])
    assert out.loc["Jayden Daniels", "p_model"] == 0.1 + 0.2             # Under: p_under, no renormalisation
    assert out.loc["Jayden Daniels", "p_model_match"] == "gsis"
    legs = pd.DataFrame([dict(week=10, game_id=GAME, gsis="00-QB1", team="WAS", market="rushyds", side="Over",
                              line=30.0)])
    f = _write_simv56(tmp_path / "int.simv56.probs.csv", rows=[("WAS", "J.Daniels", "00-QB1", "QB", 30.0, 0.4)])
    o = EM.attach_probs(legs, EM.load_probs([f])[0], source="s")
    assert o.p_model.iloc[0] == 1 - 0.4                                  # integer line: P(X>=L), as in the fit
    legs.loc[0, "line"] = 30.5
    assert EM.attach_probs(legs, EM.load_probs([f])[0], source="s").p_model_match.iloc[0] == "line_off_grid"


def test_cli_flags_alone_never_make_a_flag_countable(tmp_path):
    legs = pd.DataFrame([dict(player="X", label=se.STRONG_UNDER)])
    out = EM.stamp_countable(legs, prob_source=EM.FIT_ENSEMBLE_PROB_SOURCE, qb_override_applied=True)
    assert bool(out.countable.iloc[0]) is False
    assert out.countable_reason.iloc[0] == "p_model_not_from_probs_file"
    assert out.countable_mark.iloc[0] == "[NOT COUNTABLE: p_model_not_from_probs_file]"
    # PR #43 rush_dist CDF (no embedded provenance) + both CLI flags -> still not countable
    o = EM.attach_probs(_legs_joined(), _cdf(CDF_ROWS), source="p.csv")
    o = EM.stamp_countable(o, prob_source=EM.FIT_ENSEMBLE_PROB_SOURCE, qb_override_applied=True)
    rush = o[o.p_model_match == "gsis"]
    assert len(rush) and (rush.countable == False).all()  # noqa: E712
    assert (rush.countable_reason == "prob_provenance_missing").all()


def test_embedded_non_legacy_source_is_not_countable(tmp_path):
    out = _stamped(tmp_path, prob_source="possession_engine", cli_source=EM.FIT_ENSEMBLE_PROB_SOURCE, cli_qb=True)
    assert not out.loc["Jayden Daniels", "countable"]
    assert out.loc["Jayden Daniels", "countable_reason"] == "embedded_prob_source_not_fit_ensemble"


def test_cli_prob_source_contradicting_the_file_is_not_countable(tmp_path):
    out = _stamped(tmp_path, cli_source=EM.PROB_SCHEMA)
    assert not out.loc["Jayden Daniels", "countable"]
    assert out.loc["Jayden Daniels", "countable_reason"] == "cli_prob_source_mismatch"
    assert bool(_stamped(tmp_path, cli_source=EM.FIT_ENSEMBLE_PROB_SOURCE).loc["Jayden Daniels", "countable"])


def test_qb_override_must_cover_the_flags_team(tmp_path):
    out = _stamped(tmp_path, qb=[_qb("WAS", "Jayden Daniels", "00-QB1")])          # no NYG entry
    assert bool(out.loc["Jayden Daniels", "countable"]) is True
    assert not out.loc["Cam Skattebo", "countable"]
    assert out.loc["Cam Skattebo", "countable_reason"] == "qb_override_missing_for_team"
    out = _stamped(tmp_path, qb=[])
    assert (out.loc[["Jayden Daniels", "Cam Skattebo"], "countable_reason"] == "qb_override_missing_for_team").all()


def test_qb_override_not_ok_or_incomplete_for_team_is_not_countable(tmp_path):
    out = _stamped(tmp_path, qb=[_qb("WAS", "K.Cousins", "00-QBX", gate="qb_starter_thin_history"),
                                 _qb("NYG", "J.Dart", "00-QBN", depth_retrieved_utc=None)])
    assert out.loc["Jayden Daniels", "countable_reason"] == "qb_override_not_ok_for_team"
    assert out.loc["Cam Skattebo", "countable_reason"] == "qb_override_incomplete_for_team"
    out = _stamped(tmp_path, qb=[_qb("WAS", None, None), _qb("NYG", "J.Dart", "00-QBN", depth_source="")])
    assert out.loc["Jayden Daniels", "countable_reason"] == "qb_override_incomplete_for_team"
    assert out.loc["Cam Skattebo", "countable_reason"] == "qb_override_incomplete_for_team"


def test_flag_team_must_match_the_probability_row_team(tmp_path):
    out = _stamped(tmp_path, rows=[("NYG", "J.Daniels", "00-QB1", "QB", 38.5, 0.8),
                                   ("NYG", "C.Skattebo", "00-RB1", "RB", 70.5, 0.675)])
    assert out.loc["Jayden Daniels", "countable_reason"] == "prob_team_mismatch"
    assert bool(out.loc["Cam Skattebo", "countable"]) is True


@pytest.mark.parametrize("tamper,reason", [
    (lambda t: t.__setitem__("p_under", t.p_under.where(t.gsis != "00-QB1", "0.1")), "prob_data_digest_mismatch"),
    (lambda t: t.__setitem__("qb_overrides", t.qb_overrides.str.replace("J.Dart", "Someone")),
     "prob_provenance_digest_mismatch"),
    (lambda t: t.__setitem__("prob_source", "sim_v5_v6_ensemble "), "prob_provenance_digest_mismatch"),
    (lambda t: t.drop(columns=["qb_overrides"], inplace=True), "prob_provenance_missing"),
    (lambda t: t.__setitem__("generated_utc", ["2026-11-15T12:00:10Z", "2026-11-15T12:00:11Z"]),
     "prob_provenance_inconsistent"),
    (lambda t: t.__setitem__("inputs_sha256", "not json"), "prob_provenance_incomplete"),
])
def test_tampered_or_missing_provenance_is_not_countable(tmp_path, tamper, reason):
    out = _stamped(tmp_path, tamper=tamper, cli_source=EM.FIT_ENSEMBLE_PROB_SOURCE, cli_qb=True)
    assert (out.loc[["Jayden Daniels", "Cam Skattebo"], "countable"] == False).all()  # noqa: E712
    assert (out.loc[["Jayden Daniels", "Cam Skattebo"], "countable_reason"] == reason).all()


@pytest.mark.parametrize("kw,reason", [(dict(code_sha="abc123"), "prob_provenance_incomplete"),
                                       (dict(code_sha=""), "prob_provenance_incomplete"),
                                       (dict(dirty=True), "prob_code_dirty")])
def test_code_identity_must_be_a_clean_full_git_sha(tmp_path, kw, reason):
    out = _stamped(tmp_path, **kw)
    assert out.loc["Jayden Daniels", "countable_reason"] == reason


def test_golden_file_written_by_simv56_pipeline_verifies():
    """Cross-PR spec check: a file produced by `simv56_pmodel run` (PR #45, code 4844e12) verifies here."""
    probs, shas = EM.load_probs([FIXTURE])
    assert set(probs.prov_status) == {"ok"} and set(probs.prob_source) == {EM.FIT_ENSEMBLE_PROB_SOURCE}
    assert set(probs.prov_code_git_sha) == {SHA40}
    teams = {d["team"] for d in json.loads(probs.prov_qb_overrides.iloc[0])}
    assert teams == {"WAS", "NYG"}
    assert probs.set_index("gsis").loc["00-0039910", "p_under"] == 0.7417777777777779
    assert list(shas) == [str(FIXTURE)]


def test_probs_dir_picks_up_simv56_files(tmp_path):
    _write_simv56(tmp_path / f"{GAME}.simv56.probs.csv")
    probs, shas = EM.load_probs([tmp_path])
    assert len(shas) == 1 and set(probs.prov_status) == {"ok"}


def test_same_player_in_two_probability_files_is_ambiguous(tmp_path):
    a = _write_simv56(tmp_path / "a.simv56.probs.csv")
    b = _write_simv56(tmp_path / "b.simv56.probs.csv", rows=[("WAS", "J.Daniels", "00-QB1", "QB", 38.5, 0.5)])
    out = EM.attach_probs(_legs_joined(), EM.load_probs([a, b])[0], source="s").set_index("player")
    assert out.loc["Jayden Daniels", "p_model_match"] == "ambiguous_probs"
    assert pd.isna(out.loc["Jayden Daniels", "p_model"])


def _emit_files(tmp_path, files, **kw):
    probs, shas = EM.load_probs(files)
    return EM.emit(freeze_paths=[_freeze(tmp_path)], probs=probs, probs_source="simv56", roster=_roster(),
                   pbp=_pbp(), date="2026-11-15", out_root=tmp_path / "research/runs",
                   now=_t("2026-11-15T16:00:00Z"), input_shas={"probs": shas}, **PROV, **kw)


def test_emitter_counts_verified_legacy_file_and_records_provenance(tmp_path):
    f = _write_simv56(tmp_path / f"{GAME}.simv56.probs.csv", qb=[_qb("WAS", "Jayden Daniels", "00-QB1")])
    r = _emit_files(tmp_path, [f])
    flags = pd.read_csv(r["flags_csv"])
    u = flags[flags.side == "Under"].set_index("player")
    assert u.loc["Jayden Daniels", "label"] == se.STRONG_UNDER and bool(u.loc["Jayden Daniels", "countable"])
    assert u.loc["Cam Skattebo", "countable_reason"] == "qb_override_missing_for_team"
    assert u.loc["Nobody Here", "countable_reason"] == "p_model_not_from_probs_file"
    m = json.loads(r["manifest_json"].read_text())
    assert m["countable"] is True and m["countable_counts"]["embedded_fit_ensemble_with_qb_override"] >= 1
    pf = m["prob_files_provenance"][str(f)]
    assert pf["status"] == "ok" and pf["prob_source"] == EM.FIT_ENSEMBLE_PROB_SOURCE and pf["code_git_sha"] == SHA40
    assert pf["qb_override_teams_ok"] == ["WAS"] and pf["provenance_sha256"]
    assert m["prob_source_declared"] == "" and m["qb_override_declared"] is False
    md = r["summary_md"].read_text()
    assert "[NOT COUNTABLE: qb_override_missing_for_team]" in md


def test_emitter_cli_flags_with_rush_dist_probs_are_not_countable(tmp_path):
    r = EM.emit(freeze_paths=[_freeze(tmp_path)], probs=_cdf(CDF_ROWS), probs_source="p.csv", roster=_roster(),
                pbp=_pbp(), date="2026-11-15", out_root=tmp_path / "research/runs", now=_t("2026-11-15T16:00:00Z"),
                prob_source=EM.FIT_ENSEMBLE_PROB_SOURCE, qb_override_applied=True, **PROV)
    flags = pd.read_csv(r["flags_csv"])
    assert (flags.countable == False).all()  # noqa: E712
    rush = flags[flags.p_model_match == "gsis"]
    assert len(rush) and (rush.countable_reason == "prob_provenance_missing").all()
    m = json.loads(r["manifest_json"].read_text())
    assert m["countable"] is False and m["prob_source_declared"] == EM.FIT_ENSEMBLE_PROB_SOURCE
    assert m["qb_override_declared"] is True
    assert "[NOT COUNTABLE: prob_provenance_missing]" in r["summary_md"].read_text()
