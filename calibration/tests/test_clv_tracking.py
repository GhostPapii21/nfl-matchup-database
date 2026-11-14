"""Closing-line tracking plan + CLV grading (NFL-75 memo item 6; refs NFL-75).

Dry-run / fixtures only: the injected fetch is never a live Odds API client, and credits_used stays 0.
"""
from __future__ import annotations

import io
from contextlib import redirect_stdout

import numpy as np
import pandas as pd
import pytest

from calibration import clv_tracking as clv


def _leg(**kw):
    row = dict(week=10, game_id="2026_10_BUF_MIN", gsis="00-0030001", player="Test Back",
               market="rushyds", side="Under", line=60.5, dec=1.91, price_source="book:fanduel",
               label=clv.STRONG_UNDER, flagged=True)
    row.update(kw)
    return row


def _legs(*rows):
    return pd.DataFrame(list(rows))


def test_estimate_is_markets_times_region_units():
    assert clv.estimate_event_cost(0) == 0
    assert clv.estimate_event_cost(3, n_books=5) == 3    # ceil(5/10)=1
    assert clv.estimate_event_cost(3, n_books=10) == 3
    assert clv.estimate_event_cost(3, n_books=11) == 6    # two region units


def test_plan_estimates_cost_per_game_for_flagged_legs_only():
    df = _legs(
        _leg(game_id="g1", market="rushyds"),
        _leg(game_id="g1", market="recyds"),
        _leg(game_id="g2", market="rushyds"),
        _leg(game_id="g3", market="rushyds", flagged=False, label="INSUFFICIENT"),  # not flagged
    )
    plan = clv.plan_closing_pull(df, remaining_credits=2000)
    assert plan["n_flagged_legs"] == 3 and plan["n_games"] == 2
    assert plan["estimate_credits"] == 3        # g1: 2 markets, g2: 1 market
    assert {g["game_id"]: g["estimate_credits"] for g in plan["games"]} == {"g1": 2, "g2": 1}
    assert plan["allowed"] is True and plan["remaining_after"] == 1997
    assert plan["credits_used"] == 0 and plan["dry_run"] is True
    assert plan["projection_ready"] is False


def test_plan_report_prints_cost_before_any_fetch_and_dry_run_does_not_call_fetch():
    df = _legs(_leg())
    plan = clv.plan_closing_pull(df, remaining_credits=1800)
    assert "estimate: 1 credits" in plan["report"]
    assert "remaining: 1800" in plan["report"]
    assert "Sunday reserve: 950" in plan["report"] and "hard floor: 800" in plan["report"]
    called = []

    def fetch(_game):
        called.append(1)
        raise AssertionError("fetch must not run on dry-run")

    out = clv.execute_closing_pull(plan, fetch=fetch, dry_run=True)
    assert out["status"] == "DRY_RUN" and out["credits_used"] == 0 and called == []
    # The report with the estimate is on the result *before* any pull would have happened
    assert "estimate: 1 credits" in out["report"]


def test_refuses_when_remaining_would_drop_below_950_reserve():
    df = _legs(_leg(game_id="g1", market="rushyds"), _leg(game_id="g1", market="recyds"),
               _leg(game_id="g2", market="rushyds"))  # estimate 3
    plan = clv.plan_closing_pull(df, remaining_credits=952)
    assert plan["estimate_credits"] == 3 and plan["allowed"] is False
    assert plan["remaining_after"] == 949
    assert "SKIPPED_SUNDAY_RESERVE" in plan["reason"]
    # refuse happens at plan time; execute still does not fetch
    called = []
    out = clv.execute_closing_pull({**plan, "dry_run": False}, fetch=lambda g: called.append(g), dry_run=False)
    assert out["status"] == "REFUSED" and called == [] and out["credits_used"] == 0


def test_refuses_when_remaining_would_drop_below_800_hard_floor():
    # Reserve is lowered so the hard floor is the binding constraint.
    df = _legs(_leg(), _leg(game_id="g2"), _leg(game_id="g3"))  # 3 credits
    plan = clv.plan_closing_pull(df, remaining_credits=802, reserve=0, floor=800)
    assert plan["allowed"] is False and plan["remaining_after"] == 799
    assert "SKIPPED_CREDIT_FLOOR" in plan["reason"]


def test_default_rules_refuse_unknown_balance_and_satisfy_both_thresholds():
    df = _legs(_leg())
    unknown = clv.plan_closing_pull(df, remaining_credits=None)
    assert unknown["allowed"] is False and "UNKNOWN_BALANCE" in unknown["reason"]
    # 810 remaining, 1 credit: after=809 is above 800 but below the 950 reserve -> reserve wins
    reserved = clv.plan_closing_pull(df, remaining_credits=810)
    assert reserved["allowed"] is False and "SKIPPED_SUNDAY_RESERVE" in reserved["reason"]
    ok = clv.plan_closing_pull(df, remaining_credits=2000)
    assert ok["allowed"] is True and ok["remaining_after"] == 1999


def test_execute_without_injected_fetch_does_not_spend_credits():
    plan = clv.plan_closing_pull(_legs(_leg()), remaining_credits=2000, dry_run=False)
    out = clv.execute_closing_pull(plan, fetch=None, dry_run=False)
    assert out["credits_used"] == 0
    assert "NO_FETCH_INJECTED" in out["status"]


def test_never_prints_keys():
    key = "supersecret-odds-key-abcdef012345"
    df = _legs(_leg())
    plan = clv.plan_closing_pull(df, remaining_credits=2000)
    # even if a key leaks into a reason string, format_plan / redact must strip it
    plan["reason"] = f"error calling https://api.the-odds-api.com/v4/events?apiKey={key}"
    text = clv.format_plan(plan)
    assert key not in text and "apiKey=***" in text
    with redirect_stdout(io.StringIO()) as buf:
        print(clv.redact(f"ODDS_API_KEY={key} used"))
    assert key not in buf.getvalue()


def test_record_clv_same_line_and_book_uses_no_vig_close_ev():
    # Taken Under -110 (dec 1.91). Close still -110 / Over +100 -> p_nv_under = implied(-110)/(imp(-110)+imp(+100))
    # implied(-110)=110/210≈0.52381, implied(+100)=0.5, p_nv=0.52381/1.02381≈0.51163
    # ev = p*(1.91-1) - (1-p) = 0.51163*0.91 - 0.48837 ≈ -0.0228 (juice, no CLV)
    legs = _legs(_leg(dec=1.91, line=60.5, price_source="book:fanduel"))
    closes = pd.DataFrame([{
        "game_id": "2026_10_BUF_MIN", "gsis": "00-0030001", "market": "rushyds", "side": "Under",
        "line": 60.5, "book": "fanduel", "american_close": -110, "american_opp": 100,
    }])
    out = clv.record_clv(legs, closes).iloc[0]
    assert out.clv_status == "ok"
    p = clv.devig(-110, 100)[0]
    assert out.p_nv_close == pytest.approx(p)
    assert out.dec_taken == pytest.approx(1.91)
    assert out.dec_close == pytest.approx(clv.american_to_dec(-110))
    ev = p * (1.91 - 1) - (1 - p)
    assert out.ev_at_close == pytest.approx(ev)
    # Close moved toward Under (-130 / opp +110): we bought Under at -110, so ev_at_close vs no-vig close is > 0.
    closer_under = pd.DataFrame([{**closes.iloc[0].to_dict(), "american_close": -130, "american_opp": 110}])
    ev_us = clv.record_clv(legs, closer_under).iloc[0].ev_at_close
    assert ev_us > 0 and ev_us > ev


def test_record_clv_unknown_when_line_or_book_differs_is_not_zero():
    legs = _legs(_leg(line=60.5, price_source="book:fanduel"),
                 _leg(gsis="00-0030002", player="Other", line=60.5, price_source="book:fanduel"))
    # first leg: same book, different line; second: no close row at all
    closes = pd.DataFrame([{
        "game_id": "2026_10_BUF_MIN", "gsis": "00-0030001", "market": "rushyds", "side": "Under",
        "line": 62.5, "book": "fanduel", "american_close": -110, "american_opp": 100,
    }])
    out = clv.record_clv(legs, closes)
    assert list(out.clv_status) == ["unknown", "unknown"]
    assert out.clv_note.iloc[0] == "different line"
    assert out.clv_note.iloc[1] == "no closing price"
    assert out.ev_at_close.isna().all() and out.p_nv_close.isna().all()
    # different book, same line
    closes2 = pd.DataFrame([{
        "game_id": "2026_10_BUF_MIN", "gsis": "00-0030001", "market": "rushyds", "side": "Under",
        "line": 60.5, "book": "draftkings", "american_close": -110, "american_opp": 100,
    }])
    one = clv.record_clv(legs.iloc[[0]], closes2).iloc[0]
    assert one.clv_status == "unknown" and one.clv_note == "different book or book missing"
    assert pd.isna(one.ev_at_close) and one.ev_at_close != 0


def test_record_clv_skips_non_flagged_legs():
    df = _legs(_leg(flagged=True), _leg(gsis="00-x", flagged=False, label="INSUFFICIENT"))
    closes = pd.DataFrame([{
        "game_id": "2026_10_BUF_MIN", "gsis": "00-0030001", "market": "rushyds", "side": "Under",
        "line": 60.5, "book": "fanduel", "american_close": -110, "american_opp": 100,
    }])
    out = clv.record_clv(df, closes)
    assert out.clv_status.tolist() == ["ok", "not_flagged"]
    assert pd.isna(out.ev_at_close.iloc[1])


def test_flagged_allowlist_rejects_the_string_false():
    df = _legs(_leg(flagged="false"), _leg(gsis="00-2", flagged="true"), _leg(gsis="00-3", flagged=False))
    plan = clv.plan_closing_pull(df, remaining_credits=2000)
    assert plan["n_flagged_legs"] == 1


def test_cli_prints_plan_and_uses_zero_credits(tmp_path, capsys):
    path = tmp_path / "legs.csv"
    _legs(_leg(), _leg(game_id="g2")).to_csv(path, index=False)
    rc = clv._cli(["--legs", str(path), "--remaining", "1800"])
    text = capsys.readouterr().out
    assert rc == 0 and "estimate: 2 credits" in text and "DRY-RUN" in text
    assert "1800" in text and "supersecret" not in text


def test_label_flagging_uses_candidate_strings_when_no_flagged_column():
    df = pd.DataFrame([
        {**_leg(flagged=True), "label": clv.STRONG_UNDER},
        {**_leg(gsis="00-2", flagged=True), "label": "STANDARD-LINE CANDIDATE"},
        {**_leg(gsis="00-3", flagged=True), "label": "INSUFFICIENT EVIDENCE"},
    ]).drop(columns=["flagged"])
    plan = clv.plan_closing_pull(df, remaining_credits=2000)
    assert plan["n_flagged_legs"] == 2
