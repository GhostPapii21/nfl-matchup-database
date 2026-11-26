"""Import alias for core/period_engine_v0.

Market tests import research.period_engine_v0. The engine source stays under core/.
"""
from pathlib import Path

__path__ = [str(Path(__file__).resolve().parents[2] / "core" / "period_engine_v0")]
__version__ = "0.1.0-research"
