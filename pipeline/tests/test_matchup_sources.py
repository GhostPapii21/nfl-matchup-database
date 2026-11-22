"""Main-defender matchup fields (refs NFL-47, refs NFL-56): sourced or MISSING, never zero."""
import csv

import pandas as pd

from pipeline import matchup_sources as M


def _pbp(path):
    rows = []
    def add(week, pos, deff, loc, length, cmp_, succ, epa, rec="00-R1", recn="A.Rec", qb="00-Q1", qbn="Q.Back"):
        rows.append(dict(game_id=f"2026_{week:02d}_{pos}_{deff}", season_type="REG", week=week, posteam=pos, defteam=deff,
                         play_type="pass", pass_attempt=1, sack=0, qb_spike=0, two_point_attempt=0, pass_location=loc,
                         pass_length=length, complete_pass=cmp_, success=succ, epa=epa, passer_player_id=qb,
                         passer_player_name=qbn, receiver_player_id=rec, receiver_player_name=recn))
    add(1, "PIT", "XXX", "left", "short", 1, 1, 0.5)
    add(2, "PIT", "XXX", "left", "short", 0, 0, -0.5)
    add(3, "PIT", "XXX", "right", "deep", 1, 1, 2.0)
    add(11, "PIT", "XXX", "right", "deep", 1, 1, 3.0)          # target week: must be excluded
    add(1, "YYY", "PHI", "left", "short", 1, 1, 1.0, qb="00-Q9", qbn="O.Ther")
    rows.append(dict(rows[0], pass_attempt=1, sack=1))           # sack: excluded
    pd.DataFrame(rows).to_parquet(path)
    return path


def test_pbp_fields_filled_from_prior_weeks_only(tmp_path):
    p = _pbp(tmp_path / "pbp.parquet")
    f = M.fields(["PIT", "PHI"], 2026, 11, pbp_path=p, pbp_status="FRESH", pff_base=tmp_path)
    assert f["qb_pass_location"]["status"] == "FILLED"
    z = f["qb_pass_location"]["value"]["PIT"]["Q.Back (00-Q1)"]
    assert z["short_left"]["att"] == 2 and z["short_left"]["success_rate"] == 0.5
    assert z["deep_right"]["att"] == 1                          # week 11 play not counted
    vs = f["qb_success_vs_defense"]["value"]["PIT"]
    assert vs["opponent_defense"] == "PHI"
    assert vs["qbs"]["Q.Back (00-Q1)"]["short_left"]["defense_allowed"]["att"] == 1
    assert vs["qbs"]["Q.Back (00-Q1)"]["deep_right"]["defense_allowed"] == "unknown"   # no data -> unknown, not 0
    assert f["target_location"]["value"]["PIT"]["A.Rec (00-R1)"]["short_left"]["att"] == 2


def test_pbp_status_follows_freshness(tmp_path):
    p = _pbp(tmp_path / "pbp.parquet")
    f = M.fields(["PIT", "PHI"], 2026, 11, pbp_path=p, pbp_status="STALE", pff_base=tmp_path)
    assert f["target_location"]["status"] == "STALE"


def test_missing_sources_are_unknown_not_zero(tmp_path):
    f = M.fields(["PIT", "PHI"], 2026, 11, pbp_path=None, pff_base=tmp_path)
    for k in M.FIELDS:
        assert f[k]["status"] == "MISSING" and f[k]["value"] == "unknown"
    assert "signed-in browser" in f["likely_defenders"]["reason"]


def _cap(base, rows):
    d = base / "2026_w11"; d.mkdir(parents=True)
    cols = ["season", "week", "receiver", "receiver_team", "receiver_position", "opponent_team", "listed_defender",
            "defender_position", "projected_snaps", "source_url", "source_update_et", "captured_et", "routes_run",
            "assignment_evidence"]
    with (d / "receiver_matchups.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})


BASE = dict(season=2026, week=11, receiver="D.K. Metcalf", receiver_team="PIT", receiver_position="WR",
            opponent_team="PHI", listed_defender="Q. Mitchell", defender_position="CB", projected_snaps="12.3",
            source_url="https://www.pff.com/tools/matchups", source_update_et="2026-11-21 09:00 EST",
            captured_et="2026-11-22 08:00 EST")


def test_pff_projected_is_not_verified(tmp_path):
    _cap(tmp_path, [BASE])
    f = M.fields(["PIT", "PHI"], 2026, 11, pff_base=tmp_path)
    ld = f["likely_defenders"]
    assert ld["status"] == "PFF_PROJECTED"
    assert ld["value"]["D.K. Metcalf (PIT WR)"][0]["status"] == "PFF_PROJECTED"


def test_pff_verified_needs_evidence_and_routes_fill(tmp_path):
    _cap(tmp_path, [dict(BASE, assignment_evidence="charted: game film W10", routes_run="301")])
    f = M.fields(["PIT", "PHI"], 2026, 11, pff_base=tmp_path)
    assert f["likely_defenders"]["status"] == "VERIFIED"
    assert f["receiver_routes"]["status"] == "FILLED" and f["rb_routes"]["status"] == "MISSING"


def test_pff_update_after_capture_rejected(tmp_path):
    _cap(tmp_path, [dict(BASE, source_update_et="2026-11-22 09:00 EST", captured_et="2026-11-22 08:00 EST")])
    f = M.fields(["PIT", "PHI"], 2026, 11, pff_base=tmp_path)
    assert f["likely_defenders"]["status"] == "MISSING"


def test_pff_other_week_not_used(tmp_path):
    _cap(tmp_path, [dict(BASE, week=10)])
    assert M.fields(["PIT", "PHI"], 2026, 11, pff_base=tmp_path)["likely_defenders"]["status"] == "MISSING"
