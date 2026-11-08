from __future__ import annotations
import json
from pathlib import Path
from typing import Any


def load_config(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    cfg = json.loads(p.read_text())
    if "joint_producer" in cfg:
        for key in ("config_id", "mode"):
            if key not in cfg:
                raise ValueError(f"config missing {key}")
        return cfg
    required = ["config_id", "mode", "game", "history", "min_n_state", "proposed_pooling", "adjustments", "seed_base"]
    for k in required:
        if k not in cfg:
            raise ValueError(f"config missing {k}")
    if cfg["history"].get("no_league_fallback") is not True:
        raise ValueError("no_league_fallback must be true")
    return cfg
