"""NFL-56: freshness policy, fail-closed 100k entry point, phase ledger, hooks. Offline, synthetic packets only."""
import copy
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline import freshness as F, hooks as H, phases as P, sim100k as S  # noqa: E402

KO = datetime(2026, 11, 13, 1, 15, tzinfo=timezone.utc)          # Thu 8:15 PM ET
BOOKS = list(H.REQUIRED_BOOKS)


def iso(dt):
    return dt.isoformat(timespec="seconds")


def packet(stamp, roof="outdoors"):
    src = {k: {"status": "OK", "retrieved_utc": iso(stamp)} for k in
           ("games", "pbp", "rosters", "depth_charts", "snap_counts", "ftn", "pfr_def", "injuries", "espn_injuries")}
    team = lambda: {"offense": {"players": [{"name": "x"}], "by_game": [1], "offense_snap_share": {"x": 1}, "produced": {"pts": 1}},
                    "defense": {"allowed": {"dropbacks_charted": 30, "pts": 1}, "rank": {"pts": 1}, "defenders": [{"n": "d"}]},
                    "depth_chart": {"QB": ["x"]},
                    "injuries": {"official_report": [{"p": "y"}], "espn_live": [{"p": "y"}],
                                 "official_report_status": "OK", "espn_live_status": "OK"}}
    pk = {"game": {"game_id": "2026_10_WAS_NYG", "season": 2026, "week": 10, "away": "WAS", "home": "NYG", "date": "2026-11-12",
                   "kickoff_et": "20:15", "site": "Home", "roof": roof, "listed_qbs": {"WAS": "a", "NYG": "b"}, "coaches": {"WAS": "c"}},
          "market": {"home_spread": 3.0, "total": 44.5}, "generated_utc": iso(stamp),
          "data_freshness": {"WAS": {"status": "OK"}, "NYG": {"status": "OK"}},
          "books": {"status": "OK", "retrieved_utc": iso(stamp), "markets": {"spread": {}}},
          "weather": ({"status": "INDOOR"} if roof != "outdoors" else
                      {"status": "OK", "retrieved_utc": iso(stamp), "kickoff_utc": iso(KO)}),
          "teams": {"WAS": team(), "NYG": team()}, "team_projection": {"status": "RESEARCH_ONLY_NOT_VALIDATED"},
          "sources": src}
    pk["phase_ledger"] = [{"phase": n, "status": "AUTO", "detail": ""} for n in range(1, 16)]
    return pk


def freeze_dir(tmp_path, pulled, books=BOOKS, status="OK", game="2026-11-12_WAS@NYG"):
    d = tmp_path / "price_freezes" / game
    d.mkdir(parents=True, exist_ok=True)
    stamp = pulled.strftime("%Y%m%dT%H%M%SZ")
    rows = [{"book": b, "reference_only": False} for b in books] + [{"book": "pinnacle", "reference_only": True}]
    (d / f"freeze_{stamp}.json").write_text(json.dumps({"meta": {"status": status, "pulled_utc": pulled.strftime("%Y-%m-%dT%H:%M:%SZ")}, "rows": rows}))
    return tmp_path / "price_freezes"


GOOD_FLAGS = {"DEFERRED_100K": False, "unsupported_semantics": []}
OK_INACTIVES = lambda when: (lambda pk: {"status": "OK", "retrieved_utc": iso(when), "inactives": {}})


def semantics_root(tmp_path, present=True):
    r = tmp_path / "repo"
    r.mkdir(exist_ok=True)
    if present:
        (r / "SEMANTICS_BOUNDS.md").write_text("bounds")
    return r


def all_green(tmp_path, now):
    """Everything fresh, inactives after T-90, four books, NFL-43 closed, flags clear."""
    pk = packet(now - timedelta(minutes=5))
    hi = {"price_freeze_dir": freeze_dir(tmp_path, now - timedelta(minutes=5)), "official_inactives": OK_INACTIVES(now - timedelta(minutes=2))}
    return pk, hi


# ---------------- freshness ----------------

def test_fresh_packet_far_from_kickoff_only_hooks_block():
    now = KO - timedelta(hours=30)
    rows = {r["source"]: r for r in F.check(packet(now - timedelta(minutes=30)), now)}
    assert all(rows[s]["status"] == "FRESH" for s in F.POLICY)
    assert rows["official_inactives"]["status"] == "NOT_YET"
    assert rows["four_book_prices"]["status"] == "MISSING"


def test_limits_tighten_near_kickoff():
    assert F.max_age_minutes("odds", 30) == 360
    assert F.max_age_minutes("odds", 5) == 60
    assert F.max_age_minutes("odds", 1) == 20
    assert F.max_age_minutes("news_injuries", 1) == 45
    assert F.max_age_minutes("weather", None) == 360


def test_odds_stale_at_one_hour_out():
    now = KO - timedelta(hours=1)
    rows = {r["source"]: r for r in F.check(packet(now - timedelta(minutes=30)), now)}
    assert rows["odds"]["status"] == "STALE" and "limit is 20 min" in rows["odds"]["reason"]
    assert rows["schedule"]["status"] == "FRESH"


def test_missing_timestamp_is_missing_not_fresh():
    now = KO - timedelta(hours=30)
    pk = packet(now)
    del pk["sources"]["injuries"]["retrieved_utc"]
    pk["sources"]["espn_injuries"]["status"] = "UNREACHABLE"
    del pk["books"]
    rows = {r["source"]: r for r in F.check(pk, now)}
    assert rows["official_injuries"]["status"] == "MISSING"
    assert rows["news_injuries"]["status"] == "MISSING"
    assert rows["odds"]["status"] == "MISSING"


def test_pbp_lagging_a_game_is_stale():
    now = KO - timedelta(hours=30)
    pk = packet(now)
    pk["data_freshness"]["NYG"]["status"] = "MISSING_GAMES"
    rows = {r["source"]: r for r in F.check(pk, now)}
    assert rows["play_by_play"]["status"] == "STALE" and "NYG" in rows["play_by_play"]["reason"]


def test_indoor_weather_not_required():
    now = KO - timedelta(hours=30)
    rows = {r["source"]: r for r in F.check(packet(now, roof="dome"), now)}
    assert rows["weather"]["status"] == "NOT_REQUIRED"


def test_inactives_pulled_before_t90_are_stale(tmp_path):
    now = KO - timedelta(minutes=60)
    hi = {"official_inactives": OK_INACTIVES(KO - timedelta(minutes=120))}
    rows = {r["source"]: r for r in F.check(packet(now), now, hi)}
    assert rows["official_inactives"]["status"] == "STALE"


def test_inactives_hook_unbound_after_t90_is_missing():
    now = KO - timedelta(minutes=60)
    rows = {r["source"]: r for r in F.check(packet(now), now)}
    assert rows["official_inactives"]["status"] == "MISSING"


# ---------------- four-book freeze (read-only JSON check) ----------------

def test_four_book_freeze_newest_file_used(tmp_path):
    now = KO - timedelta(hours=5)
    base = freeze_dir(tmp_path, now - timedelta(hours=10))
    freeze_dir(tmp_path, now - timedelta(minutes=10))
    r = F.four_book_row(packet(now), now, 5, {"price_freeze_dir": base})
    assert r["status"] == "FRESH" and r["age_minutes"] == pytest.approx(10, abs=0.1)


def test_four_book_freeze_stale(tmp_path):
    now = KO - timedelta(hours=1)
    base = freeze_dir(tmp_path, now - timedelta(minutes=45))
    assert F.four_book_row(packet(now), now, 1, {"price_freeze_dir": base})["status"] == "STALE"


def test_four_book_freeze_missing_book(tmp_path):
    now = KO - timedelta(hours=5)
    base = freeze_dir(tmp_path, now, books=["fanduel", "draftkings", "hardrockbet"])
    r = F.four_book_row(packet(now), now, 5, {"price_freeze_dir": base})
    assert r["status"] == "MISSING" and "williamhill_us" in r["reason"]


def test_four_book_freeze_not_ok_or_other_game(tmp_path):
    now = KO - timedelta(hours=5)
    base = freeze_dir(tmp_path, now, status="SKIPPED_CREDIT_FLOOR")
    assert F.four_book_row(packet(now), now, 5, {"price_freeze_dir": base})["status"] == "MISSING"
    base2 = freeze_dir(tmp_path / "x", now, game="2026-11-12_DAL@IND")
    assert F.four_book_row(packet(now), now, 5, {"price_freeze_dir": base2})["status"] == "MISSING"


# ---------------- fail-closed 100k entry point ----------------

def test_real_repo_flags_refuse_with_nonzero_exit(tmp_path, capsys):
    """Repo flags as committed (DEFERRED_100K, NFL-43 open, no rocket): refuse with exit 2 and plain reasons."""
    p = tmp_path / "p.json"
    p.write_text(json.dumps(packet(datetime.now(timezone.utc))))
    code = S.main(["--game", "2026_10_WAS_NYG", "--packet", str(p)])
    out = capsys.readouterr().out
    assert code == S.EXIT_REFUSED == 2
    assert "REFUSED" in out and "Nothing was simulated" in out


def test_missing_packet_refuses(tmp_path):
    code, rep = S.run("2099_01_AAA_BBB", packet=tmp_path / "nope.json", flags=GOOD_FLAGS)
    assert code == 2 and any(r.startswith("G3") for r in rep["reasons"])


def test_engine_not_called_when_refused(tmp_path):
    called = []
    now = KO - timedelta(hours=30)
    p = tmp_path / "p.json"
    p.write_text(json.dumps(packet(now)))
    code, rep = S.run("g", packet=p, engine=lambda *a: called.append(a), now=now, flags=GOOD_FLAGS,
                      root=semantics_root(tmp_path), rocket_impl=lambda g: {"status": "PASS"})
    assert code == 2 and not called and rep["projection_ready"] is False


@pytest.mark.parametrize("breaker", ["deferred", "semantics_file", "semantics_flag", "flags_unreadable", "stale_odds",
                                     "no_freeze", "inactives_not_yet", "rocket_unset", "rocket_fails", "phase_missing"])
def test_each_gate_alone_refuses(tmp_path, breaker, monkeypatch):
    now = KO - timedelta(minutes=60)
    pk, hi = all_green(tmp_path, now)
    flags = dict(GOOD_FLAGS)
    root = semantics_root(tmp_path)
    rocket = lambda g: {"status": "PASS"}
    rocket_cmd = None
    if breaker == "deferred":
        flags["DEFERRED_100K"] = True
    elif breaker == "semantics_file":
        (tmp_path / "empty").mkdir()
        root = semantics_root(tmp_path / "empty", present=False)
    elif breaker == "semantics_flag":
        flags["unsupported_semantics"] = ["official_overtime"]
    elif breaker == "flags_unreadable":
        flags = {"_error": "cannot read"}
    elif breaker == "stale_odds":
        pk["books"]["retrieved_utc"] = iso(now - timedelta(minutes=40))
    elif breaker == "no_freeze":
        hi["price_freeze_dir"] = tmp_path / "nowhere"
    elif breaker == "inactives_not_yet":
        now = KO - timedelta(hours=3)
        pk, hi = all_green(tmp_path / "b", now)
    elif breaker == "rocket_unset":
        rocket = None
        monkeypatch.setattr(H, "ROCKET_COMMAND", None)  # ROCKET_COMMAND is bound now; simulate "unset"
    elif breaker == "rocket_fails":
        rocket = None
        rocket_cmd = [sys.executable, "-c", "import sys; sys.exit(1)"]
    elif breaker == "phase_missing":
        del pk["teams"]["NYG"]["defense"]["defenders"]
    pf = S.preflight(pk, now=now, flags=flags, hook_impls=hi, root=root, rocket_impl=rocket, rocket_command=rocket_cmd)
    assert pf["ok"] is False and pf["reasons"], breaker


def test_all_green_runs_engine_with_fixed_100k(tmp_path):
    now = KO - timedelta(minutes=60)
    pk, hi = all_green(tmp_path, now)
    p = tmp_path / "p.json"
    p.write_text(json.dumps(pk))
    seen = {}
    code, rep = S.run("2026_10_WAS_NYG", packet=p, engine=lambda pk, n, seed: seen.setdefault("n", n) and {"ok": 1},
                      now=now, flags=GOOD_FLAGS, hook_impls=hi, root=semantics_root(tmp_path),
                      rocket_command=[sys.executable, "-c", "import sys; sys.exit(0)"])
    assert code == 0 and seen["n"] == 100_000 and rep["status"] == "RAN_RESEARCH_ONLY" and rep["projection_ready"] is False


def test_engine_crash_is_refusal(tmp_path):
    now = KO - timedelta(minutes=60)
    pk, hi = all_green(tmp_path, now)
    p = tmp_path / "p.json"
    p.write_text(json.dumps(pk))
    def boom(*a):
        raise RuntimeError("x")
    code, rep = S.run("g", packet=p, engine=boom, now=now, flags=GOOD_FLAGS, hook_impls=hi,
                      root=semantics_root(tmp_path), rocket_impl=lambda g: {"status": "PASS"})
    assert code == 2 and rep["status"] == "REFUSED" and "result" not in rep


def test_rocket_not_run_when_earlier_gate_refuses(tmp_path):
    ran = []
    now = KO - timedelta(minutes=60)
    pk, hi = all_green(tmp_path, now)
    pf = S.preflight(pk, now=now, flags={"DEFERRED_100K": True, "unsupported_semantics": []}, hook_impls=hi,
                     root=semantics_root(tmp_path), rocket_impl=lambda g: ran.append(g) or {"status": "PASS"})
    assert not pf["ok"] and not ran and pf["gates"]["G6_rocket"].startswith("NOT_RUN")


def test_no_override_switch():
    with pytest.raises(SystemExit):
        S.main(["--game", "2026_10_WAS_NYG", "--force"])
    src = (ROOT / "pipeline" / "sim100k.py").read_text()
    assert "os.environ" not in src and "TRIALS = 100_000" in src


def test_shipped_hooks_fail_closed():
    """Unbound hooks refuse. Update this test in the same reviewed PR that binds a hook."""
    # BetGuru bound rocket and official_inactives (NFL-49). Both still fail closed without their inputs.
    assert H.ROCKET_COMMAND == ["python3", "rocket"]
    assert H.REGISTRY["official_inactives"] == "phase15.official_inactives:hook"
    assert H.official_inactives({"game": {"game_id": "2099_01_AAA_BBB"}})["status"] == "FAILED"
    assert H.rocket_validation("g", command=None if False else [sys.executable, "-c", "import sys; sys.exit(1)"])["status"] == "FAILED"


def test_broken_hook_fails_closed():
    assert H.official_inactives({}, impl=lambda pk: 1 / 0)["status"] == "FAILED"
    assert H.official_inactives({}, impl=lambda pk: {"status": "maybe"})["status"] == "FAILED"


# ---------------- phase ledger ----------------

def test_every_phase_has_explicit_status_and_command():
    now = KO - timedelta(hours=30)
    led = P.ledger(packet(now - timedelta(minutes=5)), now, gate={"ran": False, "reasons": ["G1: deferred"]})
    assert [p["phase"] for p in led["phases"]] == list(range(1, 16))
    for p in led["phases"]:
        assert p["status"] and p["command"].endswith(f"--phase {p['phase']}")
    st = {p["phase"]: p["status"] for p in led["phases"]}
    assert st[13] == "MISSING" and st[14] == "NOT_YET" and st[15] == "NOT_YET" and st[1] == "AUTO"
    assert led["projection_ready"] is False


def test_missing_input_is_never_silently_filled():
    now = KO - timedelta(hours=30)
    pk = packet(now)
    pk["teams"]["WAS"]["offense"]["offense_snap_share"] = {}
    p4 = P.run_phase(4, pk, F.check(pk, now))
    assert p4["status"] == "MISSING" and "teams.WAS.offense.offense_snap_share" in p4["missing"]


def test_blocked_packet_ledger_is_missing():
    now = KO - timedelta(hours=30)
    pk = packet(now)
    pk["phase_ledger"][6]["status"] = "BLOCKED"
    assert P.run_phase(7, pk, F.check(pk, now))["status"] == "MISSING"


def test_phase_cli_strict_exit(tmp_path, capsys):
    now = datetime.now(timezone.utc)
    p = tmp_path / "p.json"
    p.write_text(json.dumps(packet(now)))
    assert P.main(["--game", "g", "--packet", str(p), "--phase", "1"]) == 0
    assert P.main(["--game", "g", "--packet", str(p), "--phase", "15", "--strict"]) == 3
    assert P.main(["--game", "g", "--packet", str(tmp_path / "none.json")]) == 2
