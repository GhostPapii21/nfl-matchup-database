"""JSON helpers. NumPy arrays are not written; callers summarize them first."""
from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime
from pathlib import Path

import numpy as np


def jsonify(value):
    if isinstance(value, dict):
        return {str(k): jsonify(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonify(v) for v in value]
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        number = float(value)
        return None if not math.isfinite(number) else number
    if isinstance(value, np.ndarray):
        raise TypeError("raw numpy arrays are not serialized; store a summary")
    if isinstance(value, float):
        return None if not math.isfinite(value) else value
    return value


def canonical(value) -> str:
    return json.dumps(jsonify(value), sort_keys=True, separators=(",", ":"))


def sha256_obj(value) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def write_json(path: Path, value) -> str:
    text = json.dumps(jsonify(value), indent=1) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return hashlib.sha256(text.encode()).hexdigest()
