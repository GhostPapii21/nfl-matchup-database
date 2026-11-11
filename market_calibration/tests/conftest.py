import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# The saved quote CSVs (and the audit artifact derived from them) are not published
# with this repository; see market_calibration/README.md. When they are absent, tests
# that need them are reported as skipped with that reason instead of erroring, so the
# rest of the suite stays a usable signal. Once the files are supplied locally under
# market_calibration/saved_quotes/, these tests run (and fail closed) as before.
_PKG = Path(__file__).resolve().parents[1]
_SAVED = _PKG / "saved_quotes"
_SAVED_FILES = ("odds_jaxbal_game.csv", "period_q1_q2_q3_fd_dk_cleared.csv", "period_line_grades.csv")
_SAVED_ABSENT = not all((_SAVED / name).is_file() for name in _SAVED_FILES)
_REASON = "saved quote CSVs are not published; supply them under market_calibration/saved_quotes/ to run"


def _needs_unpublished_data(exc: BaseException) -> bool:
    if not _SAVED_ABSENT:
        return False
    if isinstance(exc, FileNotFoundError):
        return str(_SAVED) in str(getattr(exc, "filename", "") or "")
    if isinstance(exc, ValueError):
        return "artifacts/saved_quote_audit.json" in str(exc)
    return False


def _skip_if_unpublished():
    try:
        return (yield)
    except (FileNotFoundError, ValueError) as exc:
        if _needs_unpublished_data(exc):
            pytest.skip(_REASON)
        raise


@pytest.hookimpl(wrapper=True)
def pytest_runtest_setup(item):
    return (yield from _skip_if_unpublished())


@pytest.hookimpl(wrapper=True)
def pytest_runtest_call(item):
    return (yield from _skip_if_unpublished())
