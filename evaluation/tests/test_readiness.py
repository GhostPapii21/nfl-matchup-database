"""Readiness evaluator (NFL-49 / NFL-56, report only)."""
import json
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


def test_evidence_boundary_excludes_open_draft_prs():
    """Holdout is only SCORED snapshot LOCKs; W12 packets/freezes and #131 do not raise the count."""
    r = R.evaluate()
    eb = r["evidence_boundary"]
    assert eb["open_draft_prs_do_not_count"] is True
    assert eb["pristine_games_scored"] == 14
    assert eb["pristine_weeks_scored"] == ["10", "11"]
    assert "2026_12_GB_LA" not in eb["pristine_scored_game_ids"]
    assert "LOCK.json" in eb["pristine_requires"]
    snaps = Path(R.ROOT) / "snapshots"
    assert not (snaps / "2026_12_GB_LA").exists()
    assert not any(p.is_dir() and p.name.startswith("2026_12_") for p in snaps.iterdir())
    assert len(list((Path(R.ROOT) / "pregame" / "packets").glob("2026_12_*"))) == 16
    md = R.render(r)
    assert "Evidence boundary" in md and "14+15=29" in md
    assert "Week 13" in md and "fail-closed" in md.lower()
