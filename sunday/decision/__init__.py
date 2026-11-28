"""Market comparison, adversarial review, and the final projection board.

Call ``build_board`` with a joined packet from the per-game run. The board
never fills a pick quota and never turns a model-versus-price gap into a
bettable edge. ``projection_ready`` stays false.

Historical acceptance replay::

    python3 -m sunday.decision
"""

from .board import build_board
from .report import render_markdown

__all__ = ["build_board", "render_markdown"]
