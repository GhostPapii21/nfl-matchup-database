"""Hermetic pipeline tests: never read the developer's pregame/.cache or committed inactives."""
import pytest


@pytest.fixture(autouse=True)
def _isolate_pregame_cache(tmp_path_factory, monkeypatch):
    from pipeline import freshness as F
    monkeypatch.setattr(F, "CACHE", tmp_path_factory.mktemp("pregame_cache"))
