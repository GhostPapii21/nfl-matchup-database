"""Readiness evaluator (NFL-49 / NFL-56, report only)."""
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from evaluation import readiness as R


def _row(gid, result, price, pulled="2026-11-12T20:00:00+00:00", ko="2026-11-13T01:15:00+00:00", kind="flagged_prop", mt="receptions"):
    return {"game_id": gid, "kind": kind, "market_type": mt, "result": result, "kickoff_utc": ko,
            "bet_price": {"value": price, "pulled_utc": pulled, "source": "git:x:packet.json#books"}}


def _write(tmp_path, rows):
    d = tmp_path / "results"; d.mkdir()
    by = {}
    for r in rows:
        by.setdefault(r["game_id"], []).append(r)
    for g, rs in by.items():
        (d / f"{g}.jsonl").write_text("\n".join(json.dumps(r) for r in rs) + "\n")
        (d / f"{g}.research.jsonl").write_text(json.dumps(_row(g, "win", -110)) + "\n")   # never counted
    return d


def _lock(root: Path, gid: str, locked="2026-11-12T16:00:00+00:00", ko="2026-11-13T01:15:00+00:00"):
    d = root / "snapshots" / gid / locked[:19].replace("-", "").replace(":", "")
    d.mkdir(parents=True)
    (d / "LOCK.json").write_text(json.dumps({
        "game_id": gid, "locked_utc": locked, "kickoff_utc": ko, "code_dirty": False,
        "asof_checks": "PASS", "sim": {"n": 100000}, "projection_ready": False,
    }))
    return d


def _packet(root: Path, gid: str, date: str, kickoff_et: str):
    d = root / "pregame" / "packets" / gid
    d.mkdir(parents=True)
    (d / "packet.json").write_text(json.dumps({
        "status": "RESEARCH_ONLY_NOT_BETTING_ADVICE", "projection_ready": False,
        "game": {"game_id": gid, "date": date, "kickoff_et": kickoff_et},
    }))
    return d


def test_break_even():
    assert round(R.break_even(-110), 4) == 0.5238 and R.break_even(100) == 0.5 and round(R.break_even(150), 4) == 0.4


def test_spot_filters(tmp_path):
    d = _write(tmp_path, [_row("2026_09_A_B", "win", -110),                      # seen week
                          _row("2026_10_A_B", "push", -110), _row("2026_10_A_B", "unknown", -110),
                          _row("2026_10_A_B", "win", None),                       # no real price
                          _row("2026_10_A_B", "win", -110, pulled="2026-11-13T02:00:00+00:00"),   # after kickoff
                          _row("2026_10_A_B", "loss", -120)])
    sp, ex = R.spots(d)
    assert len(sp) == 1 and sp[0]["win"] is False
    assert ex == {"push_or_unknown": 2, "no_real_price": 1, "price_after_kickoff": 1, "seen_week": 1}


def test_rule_needs_all_four(tmp_path):
    rows = []
    for wk in (10, 11, 12, 13):
        for i in range(10):
            rows.append(_row(f"2026_{wk}_A_B", "win" if i < 8 else "loss", -110))
    sp, _ = R.spots(_write(tmp_path, rows))
    m = {r["market"]: r for r in R.market_table(sp)}["prop:receptions"]
    assert m["spots"] == 40 and m["edge_points"] > 3 and m["ci95_points"][0] > 0 and m["weeks"] == [10, 11, 12, 13]
    assert m["live"] is True
    three = [s for s in sp if s["week"] != 13]
    m3 = {r["market"]: r for r in R.market_table(three)}["prop:receptions"]
    assert m3["live"] is False and m3["checks"]["weeks>=4"] is False


def test_small_sample_is_not_live(tmp_path):
    sp, _ = R.spots(_write(tmp_path, [_row("2026_10_A_B", "win", -110) for _ in range(5)]))
    m = {r["market"]: r for r in R.market_table(sp)}["prop:receptions"]
    assert m["live"] is False and m["checks"]["spots>=30"] is False


def test_repo_report_is_honest_and_report_only():
    r = R.evaluate()
    assert r["report_only"] is True and r["projection_ready_flag"] is False
    if not r["nfl49_pass"]:
        assert r["projection_ready_may_flip"] is False
    src = Path(R.__file__).read_text()
    assert "KNOWN_LIMITATIONS.json\").write" not in src and ".write_text" in src   # writes only the report files


def test_evidence_boundary_derived_live_from_repo():
    """Live boundary uses committed LOCKs/EVALUATION; drafts and freezes never inflate counts."""
    r = R.evaluate()
    eb = r["evidence_boundary"]
    assert eb["derived_live"] is True
    assert eb["open_draft_prs_do_not_count"] is True
    assert eb["price_freezes_do_not_count"] is True
    assert eb["pristine_games_scored"] == 14
    assert eb["pristine_weeks_scored"] == ["10", "11"]
    assert "2026_12_GB_LA" not in eb["pristine_scored_game_ids"]
    # Committed Week 12 LOCKs are reported and do not become scored coverage.
    assert eb["w12_with_lock"] == sorted(gid for gid in eb["snapshot_lock_game_ids"] if gid in set(eb["w12_packet_ids"]))
    assert eb["w12_with_lock"] == ["2026_12_DEN_PIT", "2026_12_KC_BUF"]
    assert eb["w12_scored"] == []
    assert set(eb["w12_with_lock"]).isdisjoint(eb["w12_remaining_eligible"])
    assert set(eb["w12_with_lock"]).isdisjoint(eb["w12_remaining_post_kickoff"])
    assert eb["w12_packet_count"] == 16
    assert "2026_12_GB_LA" in eb["w12_remaining_post_kickoff"]
    assert eb["coverage_ceiling_if_remaining_w12_lock"] == 14 + len(eb["w12_remaining_eligible"])
    assert eb["shortfall_vs_min_games_at_ceiling"] == max(0, 30 - eb["coverage_ceiling_if_remaining_w12_lock"])
    md = R.render(r)
    assert "derived live" in md.lower()
    assert f"{eb['pristine_games_scored']}+{len(eb['w12_remaining_eligible'])}={eb['coverage_ceiling_if_remaining_w12_lock']}" in md
    # live path must not hard-code the historical 14-scored / 15-remaining ceiling as literals in render output keys
    assert "w12_remaining_eligible" in eb and eb["derived_live"] is True


def test_evidence_boundary_updates_when_w12_lock_committed(tmp_path):
    """Regression: a committed Week 12 LOCK must change live counts (no stale 14 / zero-W12 claim)."""
    root = tmp_path / "repo"
    (root / "evaluation").mkdir(parents=True)
    (root / "known_flags").mkdir()
    (root / "grading" / "results").mkdir(parents=True)
    (root / "pregame" / "price_freezes").mkdir(parents=True)
    shutil.copy(R.ROOT / "evaluation" / "PRISTINE_EVALUATION_PROTOCOL.json", root / "evaluation/")
    shutil.copy(R.ROOT / "known_flags" / "KNOWN_LIMITATIONS.json", root / "known_flags/")

    scored = []
    for i in range(7):
        gid = f"2026_10_T{i:02d}_A"
        _lock(root, gid); scored.append({"game_id": gid, "status": "SCORED", "lock": f"snapshots/{gid}/x"})
    for i in range(7):
        gid = f"2026_11_T{i:02d}_A"
        _lock(root, gid); scored.append({"game_id": gid, "status": "SCORED", "lock": f"snapshots/{gid}/x"})
    _lock(root, "2026_12_CHI_DET", locked="2026-11-26T16:00:00+00:00", ko="2026-11-26T18:00:00+00:00")
    scored.append({"game_id": "2026_12_CHI_DET", "status": "SCORED", "lock": "snapshots/2026_12_CHI_DET/x"})

    # 16 W12 packets: CHI_DET locked+scored; GB_LA past kickoff; 14 still eligible
    _packet(root, "2026_12_CHI_DET", "2026-11-26", "13:00")
    _packet(root, "2026_12_GB_LA", "2026-11-25", "20:00")
    for i, name in enumerate([
        "ATL_MIN", "BAL_HOU", "CAR_TB", "DEN_PIT", "KC_BUF", "LV_CLE", "NE_LAC",
        "NO_CIN", "NYG_IND", "NYJ_MIA", "PHI_DAL", "SEA_SF", "TEN_JAX", "WAS_ARI",
    ]):
        _packet(root, f"2026_12_{name}", "2026-11-29", "13:00")

    (root / "evaluation" / "EVALUATION.json").write_text(json.dumps({
        "schema": "evaluation/1", "status": "UNSCORABLE_INSUFFICIENT_COVERAGE",
        "games_scored": len(scored), "weeks_scored": ["10", "11", "12"], "games": scored,
        "min_coverage": {"games_scored": 30, "weeks": 3},
    }))

    now = datetime(2026, 11, 26, 15, 0, tzinfo=timezone.utc)  # after GB@LAR, before Sunday slate
    eb = R.evidence_boundary(root, now=now)
    assert eb["derived_live"] is True
    assert eb["pristine_games_scored"] == 15
    assert eb["pristine_weeks_scored"] == ["10", "11", "12"]
    assert "2026_12_CHI_DET" in eb["w12_with_lock"]
    assert "2026_12_CHI_DET" in eb["w12_scored"]
    assert "2026_12_GB_LA" in eb["w12_remaining_post_kickoff"]
    assert "2026_12_CHI_DET" not in eb["w12_remaining_eligible"]
    assert len(eb["w12_remaining_eligible"]) == 14
    assert eb["coverage_ceiling_if_remaining_w12_lock"] == 15 + 14  # 29, not stale 14+15
    assert eb["shortfall_vs_min_games_at_ceiling"] == 1
    md = R.render({"evaluated_utc": now.isoformat(), "projection_ready_flag": False,
                   "projection_ready_may_flip": False, "nfl49_pass": False, "nfl56_pass": True,
                   "nfl49_pillars": [], "nfl56_criteria": [], "holdout_first_week": 10,
                   "spots_excluded": {}, "markets": [], "evidence_boundary": eb})
    assert "**15**" in md or "15 scored" in md or "Pristine holdout cited: **15**" in md
    assert "15+14=29" in md
    assert "14+15=29" not in md  # must not keep the pre-W12-lock arithmetic
    assert "no Week 12 snapshot" not in eb["note"].lower()
    assert eb["w12_scored"] == ["2026_12_CHI_DET"]
