import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
# Same path setup and unpublished-data skip rule as market_calibration/tests.
from market_calibration.tests.conftest import (  # noqa: F401
    pytest_runtest_call,
    pytest_runtest_setup,
)
