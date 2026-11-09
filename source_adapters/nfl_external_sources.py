"""NFL-only optional read-only research connectors. No production imports.

These adapters do not activate external MCP servers and never ingest on import.
All network operations require explicit enabled=True, an API key, an allowlisted
resource, and an explicit caller. Responses are raw sourced *research evidence*,
not validated model features or market quotes. Never merge across leagues.
"""
from __future__ import annotations

from datetime import datetime, timezone
import importlib
import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen

SPORT = "NFL"
MAX_RESPONSE_BYTES = 2_000_000
# No provider token or user-supplied base URL is ever serialized.
PROVIDERS = {
    "sportsdataverse_nfl": {
        "status": "optional_package_not_activated",
        "url": "https://github.com/sportsdataverse/sportsdataverse-py",
        "purpose": "NFL research-only Python loaders; verify individual dataset provenance",
    },
    "balldontlie_nfl": {
        "status": "read_only_http_adapter_requires_key",
        "url": "https://nfl.balldontlie.io/",
        "purpose": "NFL team, player and game stats; separate premium endpoint entitlements",
    },
    "api_sports_nfl": {
        "status": "read_only_http_adapter_requires_key",
        "url": "https://api-sports.io/documentation/nfl/v1",
        "purpose": "NFL game schedule, results; requires relevant provider subscription",
    },
    "cloudbet_nfl_mcp": {
        "status": "candidate_disabled", "url": "https://github.com/cloudbet/sports-mcp-server",
        "purpose": "Optional NFL odds context only; no trading, no auto-fetch",
    },
}
HTTP = {
    "balldontlie_nfl": {
        "base": "https://api.balldontlie.io/nfl/v1/",
        "env": "NFL_BDL_API_KEY",
        "header": "Authorization",
        "resources": {"games", "teams", "players", "stats", "plays"},
    },
    "api_sports_nfl": {
        "base": "https://v1.american-football.api-sports.io/",
        "env": "NFL_API_SPORTS_KEY",
        "header": "x-apisports-key",
        "resources": {"games"},
    },
}
ALLOWED_PARAMS = {
    "season", "week", "date", "dates[]", "per_page", "cursor", "page",
    "team_ids[]", "player_ids[]", "game_ids[]", "id",
}


def catalog() -> list[dict]:
    """Sport-bound source catalog, without credentials or remote access."""
    return [dict(provider=name, sport=SPORT, **config)
            for name, config in PROVIDERS.items()]


def get_sportsdataverse_module(*, enabled: bool = False):
    """Explicit opt-in only. Import is not a data fetch or proof of data quality."""
    if enabled is not True:
        raise PermissionError("sportsdataverse import disabled until opt-in")
    return importlib.import_module("sportsdataverse.nfl")


def fetch_http(provider: str, resource: str, *, params: dict | None = None,
               enabled: bool = False, key: str | None = None,
               transport=None) -> dict:
    """Opt-in GET from exactly one league/provider host, never writes/trades.

    Inject `transport(request) -> bytes` for offline tests. Production use
    requires source entitlement and a caller that validates game IDs, license,
    clocks, and fields BEFORE any model-facing transformation.
    """
    if enabled is not True:
        raise PermissionError("network disabled: explicit enabled=True required")
    if provider not in HTTP:
        raise ValueError("provider is not an allowed NFL read-only HTTP source")
    item = HTTP[provider]
    if resource not in item["resources"]:
        raise ValueError("resource not approved for this sport/provider")
    params = dict(params or {})
    if not set(params).issubset(ALLOWED_PARAMS):
        raise ValueError("unknown or cross-sport parameter rejected")
    if any(not isinstance(v, (str, int, list, tuple)) for v in params.values()):
        raise ValueError("unsupported query parameter type")
    token = key or os.environ.get(item["env"])
    if not token:
        raise PermissionError(f"required secret missing: {item['env']}")
    url = item["base"] + resource
    if params:
        url += "?" + urlencode(sorted(params.items()), doseq=True)
    request = Request(
        url, headers={"Accept": "application/json", item["header"]: token},
        method="GET",
    )
    if transport is not None:
        raw = transport(request)
    else:
        with urlopen(request, timeout=12) as response:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
    if not isinstance(raw, bytes) or len(raw) > MAX_RESPONSE_BYTES:
        raise ValueError("invalid or oversized provider response")
    payload = json.loads(raw)
    if not isinstance(payload, (dict, list)):
        raise ValueError("unexpected provider response schema")
    return {
        "sport": SPORT,
        "provider": provider,
        "resource": resource,
        "source_url": url,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_effective_asof_utc": None,  # Not the retrieval time.
        "research_only": True,
        "data": payload,
    }


if __name__ == "__main__":
    print(json.dumps({"sport": SPORT, "sources": catalog()}, indent=2))
