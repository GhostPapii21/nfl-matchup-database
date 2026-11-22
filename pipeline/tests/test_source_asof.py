"""NFL-56: freshness is dated by the publisher's as-of time, not our fetch time. Offline: fetchers are injected."""
from datetime import datetime, timedelta, timezone

from pipeline import freshness as F, source_asof as A
from pipeline.tests.test_pipeline import KO, iso, packet

PBP_URL = "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet"
NWS_URL = "https://api.weather.gov/gridpoints/PHI/50,76/forecast/hourly"


def rows(pk, now, **hi):
    return {r["source"]: r for r in F.check(pk, now, hook_impls=hi or None)}


def test_fetch_time_alone_is_not_fresh():
    now = KO - timedelta(hours=30)
    pk = packet(now)
    del pk["sources"]["pbp"]["source_updated_at"]          # fetched a minute ago, publisher stamp unknown
    r = rows(pk, now)["play_by_play"]
    assert r["status"] == "MISSING" and r["reason"].count("UNKNOWN_NO_SOURCE_TIMESTAMP") == 1
    assert r["retrieved_utc"] == iso(now) and r["as_of_utc"] is None


def test_old_publish_of_latest_roster_release_is_fresh():
    now = KO - timedelta(hours=30)
    pk = packet(now)
    pk["sources"]["rosters"]["source_updated_at"] = iso(now - timedelta(hours=40))
    r = rows(pk, now)["rosters"]
    assert r["status"] == "FRESH" and r["cadence"] == "latest_release"
    assert r["as_of_basis"] == "record:source_updated_at"
    assert r["age_minutes"] == 2400


def test_publish_stamp_after_pull_or_in_future_is_rejected():
    now = KO - timedelta(hours=30)
    pk = packet(now - timedelta(hours=1))
    pk["sources"]["depth_charts"]["source_updated_at"] = iso(now - timedelta(minutes=10))   # after our pull
    pk["sources"]["snap_counts"]["source_updated_at"] = iso(now + timedelta(hours=1))
    pk["sources"]["snap_counts"]["retrieved_utc"] = iso(now + timedelta(hours=2))
    rr = rows(pk, now)
    assert rr["depth_charts"]["status"] == "MISSING" and "after our pull" in rr["depth_charts"]["reason"]
    assert rr["snap_counts"]["status"] == "MISSING" and "future" in rr["snap_counts"]["reason"]


def test_live_endpoints_are_labelled_pull_time():
    now = KO - timedelta(hours=30)
    rr = rows(packet(now), now)
    assert rr["news_injuries"]["status"] == "FRESH" and rr["news_injuries"]["as_of_basis"].startswith("live_pull")
    assert rr["odds"]["as_of_basis"].startswith("live_pull")


def _release(updated, digest=None, size=10):
    return {"assets": [{"name": "play_by_play_2026.parquet", "updated_at": updated, "digest": digest, "size": size}]}


def test_nflverse_digest_match_proves_publish_time():
    rec = {"url": PBP_URL, "retrieved_utc": "2026-11-21T20:46:36+00:00", "sha256": "ab" * 32, "bytes": 10}
    a = A.nflverse_asof(rec, lambda u: _release("2026-11-21T16:46:05Z", "sha256:" + "ab" * 32), {})
    assert a["source_updated_at"] == "2026-11-21T16:46:05Z" and a["as_of_basis"] == "nflverse_asset_digest_match"


def test_nflverse_not_updated_since_pull_applies_without_digest():
    rec = {"url": PBP_URL, "retrieved_utc": "2026-11-21T20:46:36+00:00", "sha256": "ab" * 32}
    a = A.nflverse_asof(rec, lambda u: _release("2026-11-21T16:46:05Z", None), {})
    assert a["as_of_basis"] == "nflverse_asset_not_updated_since_pull"


def test_nflverse_republished_after_pull_is_unknown():
    rec = {"url": PBP_URL, "retrieved_utc": "2026-11-21T20:46:36+00:00", "sha256": "ab" * 32}
    a = A.nflverse_asof(rec, lambda u: _release("2026-11-22T04:36:31Z", "sha256:" + "cd" * 32), {})
    assert a["source_updated_at"] is None and "superseded" in a["reason"]


def test_lookup_failure_is_unknown_never_fresh():
    def boom(u):
        raise OSError("offline")
    a = A.nflverse_asof({"url": PBP_URL, "retrieved_utc": "2026-11-21T20:46:36+00:00"}, boom, {})
    assert a["source_updated_at"] is None and a["as_of_basis"] == "UNKNOWN_NO_SOURCE_TIMESTAMP"


def test_nws_update_time():
    rec = {"url": NWS_URL, "retrieved_utc": "2026-11-21T20:46:55+00:00"}
    ok = A.nws_asof(rec, lambda u: {"properties": {"updateTime": "2026-11-21T19:58:00+00:00"}}, {})
    late = A.nws_asof(rec, lambda u: {"properties": {"updateTime": "2026-11-21T23:00:00+00:00"}}, {})
    assert ok["source_updated_at"] == "2026-11-21T19:58:00+00:00" and late["source_updated_at"] is None


def test_resolver_feeds_freshness_through_hook():
    now = KO - timedelta(hours=30)
    pk = packet(now)
    for k in pk["sources"]:
        pk["sources"][k].pop("source_updated_at", None)
    pk["sources"]["pbp"].update(url=PBP_URL, sha256="ab" * 32)
    got = now - timedelta(hours=2)
    pk["sources"]["pbp"]["retrieved_utc"] = iso(got)
    pub = iso(got - timedelta(hours=3))
    resolver = lambda p: A.resolve(p, F.POLICY, fetch=lambda u: _release(pub, "sha256:" + "ab" * 32))
    rr = rows(pk, now, source_asof=resolver)
    assert rr["play_by_play"]["status"] == "FRESH" and rr["play_by_play"]["as_of_utc"] == pub.replace("Z", "+00:00")
    assert rr["play_by_play"]["as_of_evidence"]["asset_digest"] == "sha256:" + "ab" * 32
    assert rr["rosters"]["status"] == "MISSING"            # no URL, no stamp: unknown


def test_network_resolution_is_off_unless_cli_enables_it(monkeypatch):
    monkeypatch.setattr(A, "_NETWORK", False)
    assert not A.enabled()
    A.enable_network()
    assert A.enabled()
    monkeypatch.setattr(A, "_NETWORK", False)
    src = (A.__file__ and open(A.__file__).read())
    assert "os.environ.get(\"NFL" not in src
