"""Packet-summary helpers are not phase execution.

NFL-83 review: a count of players, snaps, defenders, or markets does not prove an
equation ran. Canonical calls live in pipeline.execution.canonical. This module
exports nothing that a phase may PASS on.
"""


def __getattr__(name: str):
    raise AttributeError(f"{name} is not an analytical implementation; refusing a packet summary")
