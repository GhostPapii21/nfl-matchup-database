"""Offline tests for scripts/live_pbp.py defender attribution (refs NFL-56).

Play texts are verbatim from ESPN's public summary JSON for 2026 Week 11, pulled 2026-11-22 17:20 AST
(site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event=<id>). No network.
"""
import csv
import importlib.util
import io
from pathlib import Path

_spec = importlib.util.spec_from_file_location("live_pbp", Path(__file__).resolve().parent / "scripts" / "live_pbp.py")
lp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lp)

# key: (game, quarter, clock, ESPN play type, statYardage, text)
PLAYS = {
    'injury': ('BAL @ CAR', 1, '4:50', 'Pass Reception', 9,
        '(Shotgun) J.Brissett pass short right to J.Hill to CAR 24 for 9 yards (T.Dodson; D.Brown). CAR-T.Dodson was injured during the play.'),
    'replay': ('ARI @ KC', 1, '12:41', 'Pass Reception', 15,
        '(Shotgun) P.Mahomes pass short right to R.Rice to ARZ 24 for 15 yards (K.Clark).  The penalty was assisted by replay.'),
    'declined': ('ARI @ KC', 3, '0:31', 'Pass Reception', 13,
        '(Shotgun) P.Mahomes pass short right to J.Downs to ARZ 44 for 13 yards (K.Clark).Penalty on ARZ-J.Sweat, Defensive Offside, declined.'),
    'pressure': ('ARI @ KC', 3, '13:02', 'Pass Reception', 10,
        'J.Johnson pass short middle to H.Wallace to KC 49 for 10 yards (D.Tranquill) [G.Karlaftis].'),
    'timeout1': ('NO @ CHI', 1, '10:01', 'Pass Reception', 14,
        'T.Shough pass short left to C.Olave ran ob at CHI 40 for 14 yards.Chicago challenged the pass completion ruling, and the play was Upheld. The ruling on the field stands. (Timeout #1.)'),
    'timeout3': ('NO @ CHI', 4, '7:32', 'Pass Reception', 16,
        'L.Newman reported in as eligible.  C.Williams pass deep left to Z.Thomas ran ob at CHI 36 for 16 yards (K.McKinstry).New Orleans challenged the pass completion ruling, and the play was Upheld. The ruling on the field stands. (Timeout #3.)'),
    'pbu': ('ARI @ KC', 1, '8:25', 'Pass Incompletion', 0,
        '(Shotgun) J.Johnson pass incomplete short left to H.Wallace (N.Bolton) [N.Williams].'),
    'int': ('BAL @ CAR', 4, '0:36', 'Pass Interception Return', 0,
        ' (No Huddle, Shotgun) J.Brissett pass short right intended for R.Bateman INTERCEPTED by T.Dodson (W.Lee) [T.Wharton] at BLT 44. T.Dodson to BLT 44 for no gain.'),
    'dpi': ('TB @ DET', 4, '1:11', 'Penalty', 16,
        '(No Huddle, Shotgun) B.Mayfield pass incomplete deep right to T.Hurst.PENALTY on DET-B.Branch, Defensive Pass Interference, 16 yards, enforced at 50 - No Play.'),
    'reversed': ('BAL @ CAR', 4, '14:23', 'Fumble Recovery (Opponent)', 0,
        '(Shotgun) J.Brissett pass incomplete short right to D.Henry (W.Lee).Carolina challenged the incomplete pass ruling, and the play was REVERSED.(Shotgun) J.Brissett pass short right to D.Henry to BLT 49 for 3 yards (W.Lee). FUMBLES (W.Lee), RECOVERED by CAR-T.Dodson at 50.'),
    'int_return_tackler': ('MIA @ BUF', 2, '0:13', 'Penalty', -1,
        '(Shotgun) J.Allen pass deep right intended for K.Shakir INTERCEPTED by J.Wood at MIA 7. J.Wood to MIA 10 for 3 yards (T.Johnson; D.Moore). FUMBLES (T.Johnson), recovered by MIA-C.Johnson at MIA 6. C.Johnson pushed ob at MIA 15 for 9 yards (K.Coleman; T.Johnson).PENALTY on MIA-J.Brents, Defensive Holding, 5 yards, enforced at BUF 47 - No Play.'),
    'no_play': ('PIT @ PHI', 2, '6:26', 'Penalty', 11,
        '(No Huddle) A.Rodgers pass short right to B.Skowronek to PHI 37 for 11 yards (T.Woolen). ** Injury Update: PHI-J.Campbell has returned to the game. PENALTY on PIT-B.Skowronek, Illegal Shift, 5 yards, enforced at PHI 48 - No Play.')
}


def _play(key, offense="X", receiver="R"):
    game, q, clock, typ, yards, text = PLAYS[key]
    return {"type": typ, "yards": yards, "receiver": receiver, "offense": offense, "text": text,
            "attribution": lp.attribute(text)}


def test_trailing_injury_note_keeps_first_tackler():
    a = lp.attribute(PLAYS["injury"][5])
    assert a["tacklers"] == ["T.Dodson", "D.Brown"] and a["pbu"] is None and a["int"] is None


def test_trailing_replay_note():
    assert lp.attribute(PLAYS["replay"][5])["tacklers"] == ["K.Clark"]


def test_trailing_declined_penalty():
    assert lp.attribute(PLAYS["declined"][5])["tacklers"] == ["K.Clark"]


def test_pressure_bracket_is_not_the_defender():
    a = lp.attribute(PLAYS["pressure"][5])
    assert a["tacklers"] == ["D.Tranquill"]


def test_timeout_group_with_no_tackler_names_nobody():
    a = lp.attribute(PLAYS["timeout1"][5])  # NO@CHI Q1 10:01, main had "Timeout #1." as a defender
    assert a == {"pbu": None, "int": None, "dpi": [], "tacklers": [], "catch_yards": None, "no_play": False}


def test_timeout_group_after_real_tackler():
    a = lp.attribute(PLAYS["timeout3"][5])  # NO@CHI Q4 7:32, main had "Timeout #3." as a defender
    assert a["tacklers"] == ["K.McKinstry"]


def test_names_filter_rejects_timeout_and_formation_groups():
    assert lp._names("Timeout #3.") == [] and lp._names("Shotgun") == [] and lp._names("11:59") == []


def test_incompletion_names_verified_pbu():
    a = lp.attribute(PLAYS["pbu"][5])
    assert a["pbu"] == "N.Bolton" and a["tacklers"] == []


def test_interception_credits_interceptor_not_return_tacklers():
    assert lp.attribute(PLAYS["int"][5])["int"] == "T.Dodson"
    a = lp.attribute(PLAYS["int_return_tackler"][5])  # MIA@BUF Q2 0:13: defensive holding accepted - No Play
    assert a["no_play"] and a["int"] is None and a["tacklers"] == []


def test_dpi_flag_is_verified():
    assert lp.attribute(PLAYS["dpi"][5])["dpi"] == ["B.Branch"]


def test_replay_reversal_reads_final_ruling():
    a = lp.attribute(PLAYS["reversed"][5])
    assert a["pbu"] is None and a["tacklers"][:1] == ["W.Lee"]


def test_coverage_keeps_tacklers_out_of_verified_counts():
    plays = [_play(k, offense="ARI", receiver="H.Wallace") for k in ("pressure", "pbu")]
    cov = lp.coverage(plays)
    assert cov[("ARI", "D.Tranquill", lp.TACKLER)]["catches_allowed"] == 1
    assert cov[("ARI", "D.Tranquill", lp.TACKLER)]["yards_allowed"] == 10
    assert ("ARI", "D.Tranquill", lp.VERIFIED) not in cov
    assert cov[("ARI", "N.Bolton", lp.VERIFIED)]["breakups_or_ints"] == 1
    assert cov[("ARI", "N.Bolton", lp.VERIFIED)]["catches_allowed"] == 0


def test_two_tacklers_write_only_first_as_inferred():
    cov = lp.coverage([_play("injury", offense="BAL", receiver="J.Hill")])
    assert list(cov) == [("BAL", "T.Dodson", lp.TACKLER)]


def test_timeout_rows_disappear_from_coverage():
    cov = lp.coverage([_play("timeout1", "NO", "C.Olave"), _play("timeout3", "CHI", "Z.Thomas")])
    assert not any(k[1].startswith("Timeout") for k in cov)
    assert cov[("CHI", "K.McKinstry", lp.TACKLER)]["yards_allowed"] == 16


def test_dpi_and_int_counted_as_verified():
    cov = lp.coverage([_play("dpi", "TB", "T.Hurst"), _play("int", "BAL", "R.Bateman")])
    assert cov[("TB", "B.Branch", lp.VERIFIED)]["dpi"] == 1
    assert cov[("BAL", "T.Dodson", lp.VERIFIED)]["breakups_or_ints"] == 1


def test_csv_keeps_original_columns_first():
    assert lp.COVERAGE_HEADER[:7] == ["defense_vs_offense", "defender", "targets_against", "catches_allowed",
                                      "yards_allowed", "breakups_or_ints", "receivers_yards"]
    assert lp.COVERAGE_HEADER[7:] == ["evidence", "dpi"]
    b = io.StringIO()
    w = csv.writer(b)
    w.writerow(lp.COVERAGE_HEADER)
    w.writerows(lp.coverage_rows(lp.coverage([_play("pressure", "ARI", "H.Wallace")])))
    row = next(csv.DictReader(io.StringIO(b.getvalue())))
    assert row["defender"] == "D.Tranquill" and row["evidence"] == "tackler, not coverage" and row["receivers_yards"] == "H.Wallace 10"


def test_no_play_accepted_penalty_writes_no_rows():
    # PIT@PHI Q2 6:26: catch tackled by T.Woolen, then PIT illegal shift accepted - No Play
    a = lp.attribute(PLAYS["no_play"][5])
    assert a["no_play"] and a["tacklers"] == [] and a["pbu"] is None and a["int"] is None
    assert lp.coverage([_play("no_play", "PIT", "B.Skowronek")]) == {}


def test_declined_penalty_keeps_rows():
    # ARI@KC Q3 0:31: defensive offside declined, so the catch and K.Clark's tackle stand
    a = lp.attribute(PLAYS["declined"][5])
    assert not a["no_play"] and a["tacklers"] == ["K.Clark"]
    cov = lp.coverage([_play("declined", "KC", "J.Downs")])
    assert cov[("KC", "K.Clark", lp.TACKLER)]["yards_allowed"] == 13
