"""Strict adapters for unavailable charted features — never invent coefficients."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Optional


@dataclass
class FeatureGate:
    feature_id: str
    status: str  # MISSING | PROXY | AVAILABLE | SCENARIO_ONLY
    source: Optional[str]
    allows_sim_effect: bool
    scenario_payload_schema: dict
    notes: str

    def accept_scenario(self, payload: Optional[dict]) -> dict[str, Any]:
        if self.status == "AVAILABLE" and self.allows_sim_effect:
            return {"accepted": True, "mode": "measured", "payload": payload}
        if self.status in {"MISSING", "SCENARIO_ONLY", "PROXY"}:
            if not payload:
                return {"accepted": False, "mode": "absent", "reason": self.status}
            # scenario plumbing only — must be explicitly labeled
            if not payload.get("label", "").startswith("SCENARIO"):
                return {"accepted": False, "mode": "rejected", "reason": "scenario payloads require label starting with SCENARIO"}
            if payload.get("claim_fitted") or payload.get("claim_measured"):
                return {"accepted": False, "mode": "rejected", "reason": "cannot claim fitted/measured for unmeasured feature"}
            return {"accepted": True, "mode": "scenario_only", "payload": payload, "applies_to_sim": False}
        return {"accepted": False, "mode": "rejected", "reason": "unknown status"}


GATES = [
    FeatureGate("true_pressure_qbp", "MISSING", "paid FTN catalog (not in nflverse 29-col)", False,
                {"label": "str", "pressure_rate": "float|optional"}, "No free qbp field"),
    FeatureGate("man_zone_mofo", "MISSING", "not in free FTN", False,
                {"label": "str"}, "Sensitivity only if parent supplies charted file"),
    FeatureGate("cb_s_dt_replacement", "SCENARIO_ONLY", "r6 coverage.json UNVERIFIED", False,
                {"label": "str", "players": "list"}, "UNVERIFIED assignments — no coefficients"),
    FeatureGate("qb_hit_proxy", "PROXY", "pbp qb_hit", True,
                {"label": "str"}, "PROXY_NOT_MEASURED_PRESSURE — may annotate only"),
]


def gate_map() -> dict[str, dict]:
    return {g.feature_id: asdict(g) for g in GATES}
