"""Publisher as-of stamps for packet sources (NFL-56 item 2).

Freshness must be dated by when the *publisher* last updated the data, not by when we fetched it: a fresh download of
a file nobody has updated in three days is three days old. This module proves a publisher stamp for the copy that is
in the packet, or returns UNKNOWN. It never invents one.

  nflverse release assets  GitHub release API: if the asset's sha256 digest equals the packet's sha256, the asset's
                           updated_at is the publish time of our exact copy. Otherwise, if the asset was not updated
                           after our pull, our copy is the current version and updated_at still applies. If it was
                           updated after our pull, our copy is superseded and its publish time is UNKNOWN.
  NWS hourly forecast      properties.updateTime: applies to our copy only if it is not after our pull (the forecast
                           has not been regenerated since we fetched it). Otherwise UNKNOWN (superseded).
Free endpoints only, no credentials, no Odds API. Network is used only when a caller passes `fetch` or a CLI entry
point (pipeline.window / pipeline.phases / pipeline.sim100k main) calls enable_network(); library calls stay offline.
There is no environment switch.
"""
from __future__ import annotations

import json, os, re
from datetime import datetime, timedelta, timezone
from urllib.request import Request, urlopen

SKEW = timedelta(minutes=2)
NFLVERSE = re.compile(r"^https://github\.com/(?P<repo>nflverse/[\w.-]+)/releases/download/(?P<tag>[^/]+)/(?P<asset>[^/?#]+)$")
NWS = re.compile(r"^https://api\.weather\.gov/gridpoints/[^?#]+/forecast(/hourly)?$")


def _utc(s):
    if not s:
        return None
    try:
        d = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except ValueError:
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def http_json(url: str):
    h = {"User-Agent": "nfl-matchup-database/source-asof (github.com/GhostPapii21/nfl-matchup-database)", "Accept": "application/json"}
    tok = os.environ.get("GITHUB_TOKEN") if url.startswith("https://api.github.com/") else None
    if tok:
        h["Authorization"] = "Bearer " + tok
    with urlopen(Request(url, headers=h), timeout=30) as r:
        return json.loads(r.read())


def _unknown(reason, **ev):
    return {"source_updated_at": None, "as_of_basis": "UNKNOWN_NO_SOURCE_TIMESTAMP", "reason": reason, "evidence": ev}


def nflverse_asof(rec: dict, fetch, cache: dict) -> dict:
    m = NFLVERSE.match(rec.get("url") or "")
    if not m:
        return _unknown("not an nflverse release asset URL")
    api = f"https://api.github.com/repos/{m['repo']}/releases/tags/{m['tag']}"
    try:
        rel = cache[api] if api in cache else cache.setdefault(api, fetch(api))
    except Exception as e:  # network or API error: unknown, never fresh
        return _unknown(f"release lookup failed: {type(e).__name__}: {e}", api=api)
    asset = next((a for a in rel.get("assets") or [] if a.get("name") == m["asset"]), None)
    if not asset:
        return _unknown("asset not listed in the release", api=api)
    upd, got = _utc(asset.get("updated_at")), _utc(rec.get("retrieved_utc"))
    ev = {"api": api, "asset_updated_at": asset.get("updated_at"), "asset_digest": asset.get("digest"),
          "asset_size": asset.get("size"), "packet_sha256": rec.get("sha256"), "packet_bytes": rec.get("bytes"),
          "retrieved_utc": rec.get("retrieved_utc")}
    if upd is None:
        return _unknown("asset has no updated_at", **ev)
    if rec.get("sha256") and asset.get("digest") == "sha256:" + rec["sha256"]:
        return {"source_updated_at": asset["updated_at"], "as_of_basis": "nflverse_asset_digest_match", "reason": "sha256 of our copy equals the published asset", "evidence": ev}
    if got is not None and upd <= got + SKEW:
        return {"source_updated_at": asset["updated_at"], "as_of_basis": "nflverse_asset_not_updated_since_pull",
                "reason": "asset not updated after our pull, so our copy is the published version", "evidence": ev}
    return _unknown("asset was re-published after our pull; our copy is superseded and its publish time is unknown", **ev)


def nws_asof(rec: dict, fetch, cache: dict) -> dict:
    url = rec.get("url") or ""
    if not NWS.match(url):
        return _unknown("not an NWS gridpoint forecast URL")
    try:
        d = cache[url] if url in cache else cache.setdefault(url, fetch(url))
    except Exception as e:
        return _unknown(f"NWS lookup failed: {type(e).__name__}: {e}", url=url)
    props = d.get("properties") or {}
    upd, got = _utc(props.get("updateTime")), _utc(rec.get("retrieved_utc"))
    ev = {"url": url, "updateTime": props.get("updateTime"), "generatedAt": props.get("generatedAt"), "retrieved_utc": rec.get("retrieved_utc")}
    if upd is None or got is None:
        return _unknown("no updateTime or no pull time", **ev)
    if upd <= got + SKEW:
        return {"source_updated_at": props["updateTime"], "as_of_basis": "nws_update_time_not_after_pull",
                "reason": "forecast not regenerated since our pull, so updateTime is our copy's issue time", "evidence": ev}
    return _unknown("forecast regenerated after our pull; our copy's issue time is unknown", **ev)


def resolve(pk: dict, policy: dict, fetch=None, cache=None) -> dict:
    """-> {freshness source name: as-of dict} for every POLICY source whose basis is 'publisher'."""
    fetch = fetch or http_json
    cache = {} if cache is None else cache
    out = {}
    for name, (path, *_r) in policy.items():
        cur = pk
        for part in path.split("."):
            cur = cur.get(part) if isinstance(cur, dict) else None
        if not isinstance(cur, dict):
            continue
        url = cur.get("url") or ""
        if NFLVERSE.match(url):
            out[name] = nflverse_asof(cur, fetch, cache)
        elif NWS.match(url):
            out[name] = nws_asof(cur, fetch, cache)
    return out


_NETWORK = False


def enable_network() -> None:
    """Called by the CLI entry points (the production path). Turning it on can only make freshness stricter or equal:
    a stamp is either proven or UNKNOWN."""
    global _NETWORK
    _NETWORK = True


def enabled() -> bool:
    return _NETWORK
