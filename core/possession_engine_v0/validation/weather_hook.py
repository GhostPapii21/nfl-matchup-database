"""Optional weather scenario inputs — NO auto-downgrade from DK articles.

Parent supplies NWS-cross-checked weather before any numeric effect.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class WeatherScenario:
    status: str  # PENDING_NWS | PROVIDED | ABSENT
    source: Optional[str] = None
    as_of_et: Optional[str] = None
    wind_mph: Optional[float] = None
    precip: Optional[str] = None
    temp_f: Optional[float] = None
    auto_apply_to_props: bool = False  # always False until NWS OK
    notes: str = "Do not auto-downgrade props from DK article; wait for NWS cross-check"


def weather_scenario_from_parent(payload: Optional[dict] = None) -> dict[str, Any]:
    if not payload:
        return WeatherScenario(status="PENDING_NWS").__dict__
    sc = WeatherScenario(
        status="PROVIDED",
        source=payload.get("source"),
        as_of_et=payload.get("as_of_et"),
        wind_mph=payload.get("wind_mph"),
        precip=payload.get("precip"),
        temp_f=payload.get("temp_f"),
        auto_apply_to_props=False,
        notes=payload.get("notes") or WeatherScenario.notes,
    )
    return sc.__dict__


def nws_hourly_scenario(raw: dict, *, kickoff_et: str, hours: int = 4) -> dict[str, Any]:
    """Verified NWS hourly forecast -> scenario METADATA only. No quantitative modifier is applied."""
    from datetime import datetime, timedelta
    k = datetime.fromisoformat(kickoff_et)
    k0 = k.replace(minute=0, second=0)
    pr = raw["properties"]
    sel = []
    for p in pr["periods"]:
        s = datetime.fromisoformat(p["startTime"])
        if k0 <= s < k0 + timedelta(hours=hours):
            sel.append({"start": p["startTime"], "temp_f": p["temperature"], "wind": p["windSpeed"],
                        "wind_dir": p["windDirection"], "pop_pct": (p.get("probabilityOfPrecipitation") or {}).get("value"),
                        "short": p["shortForecast"]})
    return {
        "status": "PROVIDED_METADATA_ONLY",
        "source": "NWS api.weather.gov gridpoints/LWX/109,90/forecast/hourly",
        "nws_update_time": pr.get("updateTime"), "nws_generated_at": pr.get("generatedAt"),
        "kickoff_et": kickoff_et, "hours": sel,
        "max_pop_pct": max([h["pop_pct"] or 0 for h in sel], default=None),
        "max_wind": max([h["wind"] for h in sel], default=None),
        "quantitative_modifier": None, "auto_apply_to_props": False,
        "note": "No fitted weather effect exists in this engine; forecast is context only.",
    }
