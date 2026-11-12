"""Root conftest: make `pytest` from the repo root collect tools/tests cleanly.

tools/sim_v6_fix/ is deprecated (see tools/sim_v6_fix/DEPRECATED.md) and holds byte-identical
copies of tools/tests/test_sim_v6.py and test_rbmiss_sim.py. Same basenames in rootdir-less test
dirs cause pytest "import file mismatch" errors, so skip the deprecated copy. Also put tools/ on
sys.path so the tools/tests modules can `import sim_v6` etc. regardless of cwd.
"""
import os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
_TOOLS = os.path.join(_HERE, "tools")
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)
collect_ignore = ["tools/sim_v6_fix", "backtests/yardage_markets_wk3_8/v5"]
