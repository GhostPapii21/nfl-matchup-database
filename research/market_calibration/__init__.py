"""Import alias for the published market_calibration package.

The tests were written as research.market_calibration. The implementation
lives at the repository root so it stays separate from the integration tree.
"""
from pathlib import Path

__path__ = [str(Path(__file__).resolve().parents[2] / "market_calibration")]

from .delivery_guard import ANOMALY_EDGE_PP_THRESHOLD, guard_edge_delivery
