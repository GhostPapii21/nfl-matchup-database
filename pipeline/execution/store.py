"""Append-only execution receipts. A second write of the same attempt is refused."""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

_SAFE = re.compile(r"^[A-Za-z0-9_.-]+$")


class ReceiptStore:
    def __init__(self, root: Path):
        self.root = Path(root)

    def path_for(self, receipt: dict) -> Path:
        return self._path(receipt["game_id"], receipt["run_id"], int(receipt["phase_id"]), int(receipt["attempt"]))

    def attempts(self, game_id: str, run_id: str, phase_id: int) -> list[dict]:
        folder = self._phase_dir(game_id, run_id, phase_id)
        if not folder.is_dir():
            return []
        out = []
        for path in sorted(folder.glob("attempt_*.json")):
            out.append(json.loads(path.read_text()))
        return out

    def write_new(self, receipt: dict) -> Path:
        path = self.path_for(receipt)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(receipt, indent=1, sort_keys=True) + "\n"
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        except FileExistsError:
            raise
        except OSError as exc:
            if exc.errno == 17:  # EEXIST
                raise FileExistsError(path) from exc
            raise
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(payload)
        return path

    def _phase_dir(self, game_id: str, run_id: str, phase_id: int) -> Path:
        self._check(game_id, "game_id")
        self._check(run_id, "run_id")
        if not isinstance(phase_id, int) or isinstance(phase_id, bool) or not 1 <= phase_id <= 15:
            raise ValueError(f"phase_id {phase_id!r} is outside 1..15")
        return self.root / game_id / run_id / f"phase_{phase_id:02d}"

    def _path(self, game_id: str, run_id: str, phase_id: int, attempt: int) -> Path:
        if not isinstance(attempt, int) or isinstance(attempt, bool) or attempt < 1:
            raise ValueError(f"attempt {attempt!r} is not a positive integer")
        return self._phase_dir(game_id, run_id, phase_id) / f"attempt_{attempt:03d}.json"

    @staticmethod
    def _check(value: str, label: str) -> None:
        if not isinstance(value, str) or not _SAFE.match(value):
            raise ValueError(f"{label} {value!r} is not a safe receipt id")
