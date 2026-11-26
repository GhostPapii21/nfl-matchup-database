import sys
from pathlib import Path

sys.dont_write_bytecode = True
# Published layout is <repo>/market_calibration/tests. The original worktree
# nested this package one level deeper, under research/.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
